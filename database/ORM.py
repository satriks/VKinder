from sqlalchemy import create_engine, select, Column
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy_utils import database_exists, create_database

from .models import  User, Condidate, Favorit, Block, Base
from settings import database_cinfig

# Base = declarative_base(
engine = create_engine(database_cinfig.url, echo=False)
Session = sessionmaker(bind=engine)


def check_bd():
    engine = create_engine(database_cinfig.url)
    if not database_exists(engine.url):
        create_database(engine.url)
    print(f'База данных VKinder созданна : {database_exists(engine.url)}')

def get_user_id_bd(vk_id):
    session = Session()
    user = session.query(User).filter(User.vk_id == vk_id).first()
    session.close()
    return user.user_id

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

def add_block(condidate_vk_id):
    session = Session()
    condidat = session.query(Condidate).filter(Condidate.condidate_vk_id == condidate_vk_id).first()
    block = session.query(Block).filter(Block.condidate_id == condidat.condidate_id).first()
    user = session.query(Condidate).filter(Condidate.condidate_vk_id == condidate_vk_id).first()

    if block is None:
        new_block = Block(user_id=user.user_id, condidate_id=condidat.condidate_id)
        session.add(new_block)
        session.commit()
        session.close()

def get_block(user_id):
    session = Session()
    blo = session.query(Block).filter(Block.user_id == user_id).all()
    session.close()
    return [i.condidate_id for i in blo]

def add_favorit(condidate_vk_id):
    session = Session()
    condidat = session.query(Condidate).filter(Condidate.condidate_vk_id == condidate_vk_id).first()
    favorit = session.query(Favorit).filter(Favorit.condidate_id == condidat.condidate_id).first()
    user = session.query(Condidate).filter(Condidate.condidate_vk_id == condidate_vk_id).first()

    if favorit is None:
        new_favorit = Favorit(user_id=user.user_id, condidate_id=condidat.condidate_id)
        session.add(new_favorit)
        session.commit()
        session.close()
'''        
def get_favorit(user_id):
    session = Session()
    blo = session.query(Favorit).filter(Favorit.user_id == user_id).all()
    return [i.condidate_id for i in blo]     # можно попробовать через репр вывод сделть , смотря как буду выводить избранное 
'''




def get_condidat(id):
    session = Session()
    condidat = session.query(Condidate).filter(Condidate.condidate_id == id).first()
    return condidat



def clear_table():
    Base.metadata.drop_all(engine)

def create_bd():
    check_bd()
    Base.metadata.create_all(engine)
    print('Таблицы созданы, база готова к работе')

if __name__ == '__main__':
    clear_table()
    create_bd()

    # print(get_serch_data(1153507))
    #
    # Base.metadata.drop_all(engine)
