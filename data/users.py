import datetime

from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy import Column, String, Integer, DateTime, Date, ForeignKey, Table, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
from .database import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    phone = Column(String, unique=True)
    email = Column(String, unique=True)  # email пользователя (уникальный)
    address = Column(String)  # адрес доставки
    password = Column(String)
    modified_date = Column(DateTime, default=datetime.datetime.now())


    # Связь с корзинами
    baskets = relationship("Basket", back_populates="user")


class Photo(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'photos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    detail_id = Column(Integer, ForeignKey('details.id'))
    photo = Column(BYTEA)

    # Обратная связь с моделью Detail
    detail = relationship("Detail", back_populates="photos")


class Detail(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'details'

    id = Column(Integer, primary_key=True, autoincrement=True)
    creator_id = Column(Integer)
    sklad = Column(String)
    ID_detail = Column(String, unique=True)
    brand = Column(String)
    model_and_year = Column(String)
    name = Column(String)
    price = Column(String)
    price_w_discount = Column(String)
    comment = Column(String)
    orig_number = Column(String)
    condition = Column(String)
    percent = Column(Integer)
    color = Column(String)
    data_created = Column(Date, default=datetime.date.today())

    # Связь с корзинами
    baskets = relationship("Basket", secondary="basket_details", back_populates="details")

    # Связь с фотографиями
    photos = relationship("Photo", back_populates="detail")


# Ассоциативная таблица для связи между Basket и Detail
basket_details = Table(
    'basket_details',
    SqlAlchemyBase.metadata,
    Column('basket_id', Integer, ForeignKey('baskets.id')),
    Column('detail_id', Integer, ForeignKey('details.id'))
)


class Basket(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'baskets'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))  # Связь с пользователем
    user = relationship("User", back_populates="baskets")  # Связь с классом User
    details = relationship("Detail", secondary=basket_details, back_populates="baskets")  # Связь с классом Detail