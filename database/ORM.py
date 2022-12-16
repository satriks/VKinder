from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy_utils import database_exists, create_database

from .models import  User, Condidate, Favorit, Block
from settings import database_cinfig

Base = declarative_base()
engine = create_engine(database_cinfig.url, echo=False)
Session = sessionmaker(bind=engine)


def create_bd():
    engine = create_engine(database_cinfig.url)
    if not database_exists(engine.url):
        create_database(engine.url)
    print(f'База данных VKinder созданна : {database_exists(engine.url)}')


def add_user(vk_id, age, city, sex):
    session = Session()
    user = session.query(User).filter(User.vk_id == vk_id).first()
    if user is None:
        new_user = User(vk_id=vk_id)
        session.add(new_user)
        session.commit()
        user = session.query(User).filter(User.vk_id == vk_id).first()
    user.age = age
    user.city = city
    user.sex = sex
    session.commit()
def clear_table():
    session = Session()


# if __name__ == '__main__':
    # create_bd()
    # Base.metadata.create_all(engine)
    # Base.metadata.drop_all(engine)
