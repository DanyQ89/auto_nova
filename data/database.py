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

    # url = 'postgresql://autonova_4ouz_user:NMZ7nt0fNY0QEcDGMGqQZF288GMJnLE0@dpg-d1akqk15pdvs73auhlpg-a.oregon-postgres.render.com:5432/autonova_4ouz'
    url = 'postgresql://root:12345@amvera-svarog1980-cnpg-autonova-db-rw:80/data_db'


    engine = create_engine(url)
    __factory = sessionmaker(bind=engine)

    # Импорт моделей ПОСЛЕ инициализации engine
    SqlAlchemyBase.metadata.create_all(engine)


def create_session():
    if not __factory:
        global_init()
    return __factory()
