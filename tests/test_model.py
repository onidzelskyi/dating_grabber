"""Test DB model schema definition."""
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from unittest import TestCase

from dating_grabber.models import User, Question, config, Base

# global application scope.  create Session class, engine
Session = sessionmaker()
engine = create_engine(config.get('sqlalchemy', 'test_db_uri'))
Base.metadata.create_all(engine)


class ModelTest(TestCase):
    """Class for testing DB operations with table schema."""
    user_name = 'Samantha'
    user_age = 28
    question_text = 'Awesome question'

    def setUp(self):
        # connect to the database
        self.connection = engine.connect()

        # begin a non-ORM transaction
        self.trans = self.connection.begin()

        # bind an individual Session to the connection
        self.session = Session(bind=self.connection)

    def tearDown(self):
        self.session.close()

        # rollback - everything that happened with the
        # Session above (including calls to commit())
        # is rolled back.
        self.trans.rollback()

        # return connection to the Engine
        self.connection.close()

    def test_add_user_relationship(self):
        """Add user and check her relationships with other tables.
        She mustn't have any choices or questions."""
        user = User(self.user_name, self.user_age)

        assert user.questions == []
        assert user.choices == []

        self.session.add(user)
        self.session.commit()

    def test_add_user_question(self):
        """Add user and question adn check her relationships with other tables.
        She must have one question in questions table."""
        user = User(self.user_name, self.user_age)
        question = Question(self.question_text, 0)
        user.questions = [question]

        assert len(user.questions) == 1
        assert user.questions[0].text == self.question_text
        assert user.questions[0].user.name == user.name

        self.session.add(user)
        self.session.commit()

    def test_delete_user(self):
        """Add user and question adn check her relationships with other tables.
        She must have one question in questions table.
        After deleting user questions table must be empty."""
        user = User(self.user_name, self.user_age)
        question = Question(self.question_text, 0)
        user.questions = [question]

        self.session.add(user)
        self.session.commit()

        self.session.delete(user)
        self.session.commit()

        questions = self.session.query(Question).all()
        assert len(questions) == 0
