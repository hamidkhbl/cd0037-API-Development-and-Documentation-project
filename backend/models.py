import os
from sqlalchemy import Column, String, Integer, create_engine, func, and_, or_
from flask_sqlalchemy import SQLAlchemy
import json

database_name = 'trivia2'
database_path = 'postgresql://{}/{}'.format('localhost:5432', database_name)

db = SQLAlchemy()

"""
setup_db(app)
    binds a flask application and a SQLAlchemy service
"""


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


"""
Question

"""


class Question(db.Model):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    category = Column(Integer)
    difficulty = Column(Integer)

    def __init__(self, question, answer, category, difficulty):
        self.question = question
        self.answer = answer
        self.category = category
        self.difficulty = difficulty

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def search_by_question(search_phrase):
        return [q.format() for q in Question.query.filter(
            func.lower(Question.question).contains(search_phrase.lower()))]

    def get_new_question(old_question_ids, category):
        if category == 0:
            return Question.query.filter(
                ~Question.id.in_(old_question_ids)).first().format()
        else:
            return Question.query.filter(
                and_(~Question.id.in_(old_question_ids),
                     Question.category == category)).first().format()

    def format(self):
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'category': self.category,
            'difficulty': self.difficulty
            }


"""
Category

"""


class Category(db.Model):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    type = Column(String)

    def __init__(self, type):
        self.type = type

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'type': self.type
            }
