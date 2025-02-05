import datetime

from flask_login import UserMixin
from sqlalchemy import Column, String, Integer, DateTime, BLOB, Date
from sqlalchemy_serializer import SerializerMixin

from .database import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    phone = Column(String, unique=True)
    address = Column(String)  # адрес доставки
    password = Column(String)
    modified_date = Column(DateTime, default=datetime.datetime.now())


class Detail(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'details'
    id = Column(Integer, primary_key=True, autoincrement=True)
    creator_id = Column(Integer)
    sklad = Column(String)
    ID_detail = Column(String)
    brand = Column(String)
    model_and_year = Column(String)
    name = Column(String)
    price = Column(String)
    price_w_discount = Column(String)
    comment = Column(String)
    orig_number = Column(String)
    condition = Column(String)
    percent = Column(Integer)
    CpK = Column(String)
    color = Column(String)
    photo = Column(BLOB)
    data_created = Column(Date, default=datetime.date.today())

# from data.database import global_init
#
# global_init('../db/data.sqlite')
