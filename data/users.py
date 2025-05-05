import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin



from .db_session import SqlAlchemyBase
from Other.constants import DEFAULT_PROFILE_PHOTO

from api.api_key_generator import *

class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    api_key = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    hashed_api_key = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    src_avatar = sqlalchemy.Column(sqlalchemy.String, nullable=False, default=DEFAULT_PROFILE_PHOTO)
    warning_message_when_connecting_to_esp = sqlalchemy.Column(sqlalchemy.String, nullable=False, default="true")
    saved_algorithms = orm.relationship("Saved_algorithm", back_populates='user')
    devices = orm.relationship("Devices", back_populates='user')
    questions = orm.relationship("Question", back_populates='user')

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def set_api_key(self):
        api_key = generate_api_key()
        self.hashed_api_key = generate_password_hash(api_key)
        self.api_key = api_key
