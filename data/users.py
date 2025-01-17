import datetime

from flask_login import UserMixin
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy_serializer import SerializerMixin

from .database import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    phone = Column(String, unique=True)
    address = Column(String) #адрес доставки
    password = Column(String)
    modified_date = Column(DateTime, default=datetime.datetime.now())
