from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


# class User(Base):
#     __tablename__ = 'users'
#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String(50), unique=True, index=True)
#     hashed_password = Column(String(100))
#     is_admin = Column(Integer, default=0)

#     results = relationship("Result", back_populates="user")
class User(Base):
    __tablename__ = 'users'
    username = Column(String(255), unique=True, index=True, nullable=False)
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_admin = Column(Integer, default=0)

    results = relationship("UserTest", back_populates="user")


class Test(Base):
    __tablename__ = 'tests'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))

    questions = relationship("Question", back_populates="test")


class Question(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(255))
    test_id = Column(Integer, ForeignKey('tests.id'))

    test = relationship("Test", back_populates="questions")
    answers = relationship("Answer", back_populates="question")


class Answer(Base):
    __tablename__ = 'answers'
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(255))
    question_id = Column(Integer, ForeignKey('questions.id'))

    question = relationship("Question", back_populates="answers")


# class Result(Base):
#     __tablename__ = 'results'
#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey('users.id'))
#     test_id = Column(Integer, ForeignKey('tests.id'))
#     score = Column(Integer)

#     user = relationship("User", back_populates="results")
#     test = relationship("Test")

class UserTest(Base):
    __tablename__ = 'user_tests'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    test_id = Column(Integer, ForeignKey('tests.id'))
    score = Column(Integer, nullable=False)
    user = relationship("User", back_populates="results")
    test = relationship("Test")
