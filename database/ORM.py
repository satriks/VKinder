from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy_utils import database_exists, create_database

from .models import  User, Condidate, Favorit, Block, Base
from settings import database_cinfig

# Base = declarative_base()
engine = create_engine(database_cinfig.url, echo=False)
Session = sessionmaker(bind=engine)


def check_bd():
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
    session.close()

def add_candidat(condidate_vk_id, data, user_vk_id):
    session = Session()
    condidat = session.query(Condidate).filter(Condidate.condidate_vk_id == condidate_vk_id).first()
    user = session.query(User).filter(User.vk_id == user_vk_id).first()
    if condidat is None:
        new_condidate = Condidate(condidate_vk_id=condidate_vk_id ,user_id = user.user_id)
        session.add(new_condidate)
        session.commit()
        condidat = session.query(Condidate).filter(Condidate.condidate_vk_id == condidate_vk_id).first()
    condidat.name = data[0]
    condidat.foto1 = data[2]
    condidat.foto2 = data[3]
    condidat.foto3 = data[4]

    condidat.user_id = user.user_id
    session.commit()
    session.close()

def get_serch_data(vk_id):
    session = Session()
    user = session.query(User).filter(User.vk_id == vk_id).first()
    if user.sex == 2:
        sex = 1
    else: sex = 2
    session.close()
    return (user.age, sex, user.city)


def clear_table():
    Base.metadata.drop_all(engine)

def create_bd():
    check_bd()
    Base.metadata.create_all(engine)
    print('Таблицы созданы, база готова к работе')

if __name__ == '__main__':
    clear_table()

    # print(get_serch_data(1153507))
    #
    # Base.metadata.drop_all(engine)
