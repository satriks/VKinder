from sqlalchemy import create_engine
from models import Base
from settings import database_cinfig
from sqlalchemy_utils import database_exists, create_database

engine = create_engine(database_cinfig.url, echo=False)

def create_bd():
    engine = create_engine(database_cinfig.url)
    if not database_exists(engine.url):
        create_database(engine.url)
    print(f'База данных VKinder созданна : {database_exists(engine.url)}')


if __name__ == '__main__':
    create_bd()
    Base.metadata.create_all(engine)
