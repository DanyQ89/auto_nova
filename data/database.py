import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from urllib.parse import quote

SqlAlchemyBase = declarative_base()
__factory = None


def global_init():
    global __factory

    # URL базы данных PostgreSQL
    url = 'postgresql://autonova_db_user:Vv6PmPNfM6eMUbRan4xa0QhojlOORJcI@dpg-d1ptpoidbo4c73bubu1g-a.oregon-postgres.render.com/autonova_db'

    engine = create_engine(url)
    __factory = sessionmaker(bind=engine)

    # Создаем таблицы после инициализации engine
    SqlAlchemyBase.metadata.create_all(engine)


def create_session():
    if not __factory:
        global_init()
    return __factory()
