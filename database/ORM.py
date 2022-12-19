from sqlalchemy import create_engine, select, Column
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy_utils import database_exists, create_database

from database.models import  User, Condidate, Favorit, Block, Base
from settings import database_cinfig

# Base = declarative_base()
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
    try:
        condidat.foto2 = data[3]
        condidat.foto3 = data[4]
    except IndexError:
        condidat.foto2 = None
        condidat.foto3 = None
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

def add_block(c_vk_id):
    session = Session()
    condidat = session.query(Condidate).filter(Condidate.condidate_vk_id == c_vk_id).first()
    block = session.query(Block).filter(Block.condidate_id == condidat.condidate_id).first()
    user = session.query(Condidate).filter(Condidate.condidate_vk_id == c_vk_id).first()
    session.close()

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
        new_favorit = Favorit(user_id=user.user_id, condidate_id=condidat.condidate_id, name = condidat.name, link = f'https://vk.com/id + {condidat.condidate_vk_id}')
        session.add(new_favorit)
        session.commit()
        session.close()
    else: session.close()

def last_id():
    session = Session()
    condidat = session.query(Condidate).order_by(Condidate.condidate_id.desc()).first()
    session.close()
    return condidat.condidate_id
def get_condidat(id):
    session = Session()
    condidat = session.query(Condidate).get(id)
    session.close()
    return condidat

def get_favorit(id):
    session = Session()
    favorit = session.query(Condidate).join(Favorit).filter(Favorit.user_id == id).all()
    session.close()
    return favorit

def clear_table():
    Base.metadata.drop_all(engine)

def create_bd():
    check_bd()
    Base.metadata.create_all(engine)
    print('Таблицы созданы, база готова к работе')

def check_none_bd():
    session = Session()
    session.query(Condidate).filter(Condidate.name == None).delete(synchronize_session='fetch')
    session.commit()
    session.close()


if __name__ == '__main__':
    # print(last_id())
    # session = Session()
    # session.close()
    # engine.dispose()
    # session = Session()
    # print(session.query(Condidate).first())
    # print(*session.query(Favorit).all(), sep='\n')
    # print(session.query(User).first())
    # print(session.query(Favorit).first())
    # print(session.query(Block).first())
    # a = session.query(Condidate).first()
    # print(a)
    # session = Session()
    # condidat = session.query(Condidate).filter(Condidate.condidate_vk_id == c_vk_id).first()
#     print(get_user_id_bd(1153507))
#     print(get_condidat(1).name)
    clear_table()
    create_bd()

    # print(get_serch_data(1153507))
    #
    # Base.metadata.drop_all(engine)
