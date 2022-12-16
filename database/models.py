from sqlalchemy import Integer,String, ForeignKey, Column
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True)
    vk_id = Column(Integer, nullable=False)
    age = Column(Integer )
    city = Column(String)
    sex = Column(Integer)

    def __repr__(self):
        return f'{self.vk_id} --- {self.user_id}'

class Condidate(Base):
    __tablename__ = 'condidate'
    condidate_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.user_id'), nullable=False)
    name = Column(String, nullable=False)
    condidate_vk_id = Column(Integer, nullable=False)
    foto1 = Column(String)
    foto2 = Column(String)
    foto3 = Column(String)
    user = relationship('User', backref = 'user_acount')

    def __repr__(self):
        return f'{self.name}  --- vk_id ={self.condidate_vk_id} --- id_bd ={self.condidat_id}'

class Favorit(Base):
    __tablename__ = 'favorit'
    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey('user.user_id'), nullable=False)
    condidate_id = Column(Integer, ForeignKey('condidate.condidate_id'), nullable=False)
    user = relationship('User', backref='user_acount')
    condidat = relationship('Condidate', backref='condidat')

class Block(Base):
    __tablename__ = 'block'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.user_id'), nullable=False)
    condidate_id = Column(Integer, ForeignKey('condidate.condidate_id'), nullable=False)
    user = relationship('User', backref='user_acount')
    condidat = relationship('Condidate', backref='condidat')