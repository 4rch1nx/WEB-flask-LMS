import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Question(SqlAlchemyBase):
    __tablename__ = 'questions'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    theme = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    question = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    is_answered = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, default=False)
    user = orm.relationship('User')
    answers = orm.relationship("Answer", back_populates='questions')

class Answer(SqlAlchemyBase):
    __tablename__ = 'answers'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    question_theme = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    question = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    answer = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    question_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("questions.id"))
    questions = orm.relationship('Question')
