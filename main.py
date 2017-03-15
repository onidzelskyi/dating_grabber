"""Main script for questonare grabbing."""
from selenium import webdriver
from selenium.webdriver.remote.remote_connection import LOGGER

from scrapy import Selector

from sqlalchemy import and_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine

import time
import logging

from dating_grabber.models import logger, Question, User, Image, Choice, config, engine


timeout = config.getint('general', 'timeout')
question_url = 'http://www.mamba.ru/ru/questions/list.phtml?from_item=10'
xpath_comments = '//ul[@class="answers-container"]/li[@class="comment"]'
xpath_next_question = '//div[@class="question_module__next"]'

LOGGER.setLevel(logging.WARNING)
driver = webdriver.Firefox()

# engine = create_engine(config.get('sqlalchemy', 'local_db_uri'))
connection = engine.connect()
Session = sessionmaker()
session = Session(bind=connection)


def _add_user(user_name: str, user_age: str, user_avatar: str) -> User:
    """Add user to the system.
    @:arg user_name - user' name, a string.
    @:arg user_age - user' age, a string.
    @:arg user_avatar - user' photo profile, a string.
    @:return User as object."""
    # Find out if user already exists in DB
    user = session.query(User).filter(and_(User.name == user_name, User.age == user_age)).one_or_none()

    # User not found in DB. Add new user
    if not user:
        user = User(user_name, user_age)
        # user_avatar can be empty or None. Add image to user only if user_avatar exists.
        if user_avatar:
            image = Image(user_avatar)
            user.images.append(image)
    return user


def main():
    """Main routine."""
    driver.get(question_url)

    _exit = False
    i = 1

    while not _exit:
        # Extract relevant information from page
        sel = Selector(text=driver.page_source)

        xpath_prefix = '//*[@id="QuestionCarousel"]/div[1]'
        xpath_suffix_a = 'ul/li[{}]/div/div/div/ul/li/div/div/div'.format(i)
        xpath_suffix_b = 'ul/li[{}]/div/div[2]/div/span/img/@src'.format(i)
        xpath_suffix_c = 'div[1]/ul/li[{}]/div/div/div/ul/li/div/div/div/div/span[1]/span[2]/text()'.format(i)

        user_question = sel.xpath('{}/div[1]/{}/h1/text()'.format(xpath_prefix, xpath_suffix_a)).extract_first()
        question_likes = sel.xpath('{}/{}'.format(xpath_prefix, xpath_suffix_c)).extract_first()
        user_name = sel.xpath('{}/div[1]/{}/p/span[1]/text()'.format(xpath_prefix, xpath_suffix_a)).extract_first()
        user_age = sel.xpath('{}/div[1]/{}/p/span[2]/text()'.format(xpath_prefix, xpath_suffix_a)).extract_first()
        user_avatar = sel.xpath('{}/{}'.format(xpath_prefix, xpath_suffix_b)).extract_first()

        # Add user
        user = _add_user(user_name, user_age, user_avatar)

        # Find out if user already has a question
        question = session.query(Question).filter(User.id == Question.user_id).filter(
            Question.text == user_question).one_or_none()
        if not question:
            question = Question(user_question, question_likes)
            user.questions.append(question)
        else:
            question.likes = question_likes

        logger.debug('Question: {} {}'.format(user, question))

        # Add items in table for inserting
        session.add(user)
        try:
            session.commit()
        except IntegrityError as err:
            logger.error(err)
            session.roolback()

        # Gathering choices
        comments = driver.find_elements_by_xpath(xpath_comments)
        for comment in comments:
            choice_text = comment.find_element_by_class_name('comment__data').text
            choice_likes = comment.find_elements_by_class_name('icon-counter')[1].text
            user_info = comment.find_elements_by_class_name('comment__data')[1].text.split(', ')
            user_name = user_info[0]
            user_age = user_info[1] if len(user_info) == 2 else None
            user_avatar = comment.find_element_by_xpath('//img[@class="avatar"]').get_attribute('src')

            # Add user
            user = _add_user(user_name, user_age, user_avatar)

            # Find out if user already has a question
            choice = session.query(Choice).filter(User.id == Choice.user_id).filter(
                Choice.text == choice_text).one_or_none()
            if not choice:
                choice = Choice(choice_text, choice_likes)
                user.choices.append(choice)
                question.choices.append(choice)
            else:
                choice.likes = choice_likes

            logger.debug('Choice: {} {}'.format(user, choice))

            session.add(user)

            try:
                session.commit()
            except IntegrityError as err:
                logger.error(err)
                session.roolback()

        # Next question
        driver.find_element_by_xpath(xpath_next_question).click()
        time.sleep(timeout)

        # Time delay to prevent banning from remote host.
        i = 2


if __name__ == '__main__':
    main()
