import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from urllib.parse import quote

SqlAlchemyBase = declarative_base()
__factory = None


def global_init():
    global __factory

    # # Получаем URL из переменных окружения Render
    # db_url = os.getenv('DATABASE_URL')
    #
    # # Исправляем для SQLAlchemy
    # if db_url.startswith("postgres://"):
    #     db_url = db_url.replace("postgres://", "postgresql://", 1)
    # postgresql://username:password@hostname:port/database

    url = 'postgresql://autonova_user:z22NMhDXEQuDGEVh120XBDQR7XDHTLmh@dpg-d189fbuuk2gs73fmis7g-a.oregon-postgres.render.com/autonova'
    engine = create_engine(url)
    __factory = sessionmaker(bind=engine)

    # Импорт моделей ПОСЛЕ инициализации engine
    SqlAlchemyBase.metadata.create_all(engine)


def create_session():
    if not __factory:
        global_init()
    return __factory()
