"""Define DB models for tables."""
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

import os
import logging
import configparser

# Logger
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='dating.log',
                    filemode='w')
logger = logging.getLogger(__name__)

config = configparser.ConfigParser()
config.read(['{}/config.cfg'.format(os.getcwd()), '{}/../config.cfg'.format(os.path.dirname(__file__))])

Base = declarative_base()
engine = create_engine(config.get('sqlalchemy', 'local_db_uri'))


class User(Base):
    """Class User keeps user' info."""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(length=128))
    age = Column(Integer)
    page = Column(String(length=512))
    images = relationship('Image', back_populates='user',
                          cascade='all, delete, delete-orphan')
    questions = relationship('Question', back_populates='user',
                             cascade='all, delete, delete-orphan')
    choices = relationship('Choice', back_populates='user',
                           cascade='all, delete, delete-orphan')

    def __init__(self, name: str, age: int, page=None) -> None:
        """Initialize sclass attributes.
        @:arg name - user' name, a string
        @:arg age - user' age, an integer
        @:arg page - user' page, an url string."""
        self.name = name
        self.age = age
        self.page = page

    def __str__(self):
        """User' object representation format."""
        return '<{self.name}, {self.age}>'.format(self=self)

    __table_args__ = ({'mysql_engine': 'InnoDB',
                       'mysql_charset': 'utf8mb4'},)


class Image(Base):
    """Class Image keeps user' images."""
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True)
    url = Column(String(length=512))
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='images')

    def __init__(self, url: str) -> None:
        """Initialize object.
        @:arg url - image url as a string."""
        self.url = url

    def __str__(self):
        return self.url

    __table_args__ = ({'mysql_engine': 'InnoDB',
                       'mysql_charset': 'utf8mb4'},)


class Question(Base):
    """Class Question keeps user' questions."""
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    text = Column(String(length=4096))
    likes = Column(Integer, default=0)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='questions')
    choices = relationship('Choice', back_populates='question',
                           cascade='all, delete, delete-orphan')

    def __init__(self, text: str, likes: int) -> None:
        """Initialize sclass attributes.
        @:arg text - user' question, a string.
        @:arg likes - question' likes, an unsigned integer."""
        self.text = text
        self.likes = likes

    def __str__(self):
        return self.text

    __table_args__ = ({'mysql_engine': 'InnoDB',
                       'mysql_charset': 'utf8mb4'},)


class Choice(Base):
    """Class Choice keeps user' choices for question."""
    __tablename__ = 'choices'

    id = Column(Integer, primary_key=True)
    text = Column(String(length=4096, ))
    likes = Column(Integer, default=0)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='choices')
    question_id = Column(Integer, ForeignKey('questions.id'))
    question = relationship('Question', back_populates='choices')

    def __init__(self, text: str, likes: int) -> None:
        """Initialize object.
        @:arg text - choice' text as a string.
        @:arg likes - question' likes, an unsigned integer."""
        self.text = text
        self.likes = likes

    def __str__(self):
        return self.text

    __table_args__ = ({'mysql_engine': 'InnoDB',
                       'mysql_charset': 'utf8mb4'},)
