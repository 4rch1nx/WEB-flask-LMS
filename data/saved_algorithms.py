import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Saved_algorithm(SqlAlchemyBase):
    __tablename__ = 'saved_algorithms'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    algorithm = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    user = orm.relationship('User')