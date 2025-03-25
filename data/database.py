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

    url = 'postgresql://data_8uxi_user:1hhFW6tstY4wJwSNmqAtbvMTo8xlyzdk@dpg-cv6mnkan91rc73bglbbg-a.oregon-postgres.render.com/data_8uxi'
    engine = create_engine(url)
    __factory = sessionmaker(bind=engine)

    # Импорт моделей ПОСЛЕ инициализации engine
    SqlAlchemyBase.metadata.create_all(engine)


def create_session():
    if not __factory:
        global_init()
    return __factory()
