from sqlalchemy import Integer, String, ForeignKey, Column
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True, index=True)
    vk_id = Column(Integer, nullable=False, index=True)
    age = Column(Integer)
    city = Column(String)
    sex = Column(Integer)

    def __repr__(self):
        return f'{self.vk_id} --- {self.user_id}'


class Condidate(Base):
    __tablename__ = 'condidate'
    condidate_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.user_id'), nullable=False, index=True)
    name = Column(String)
    condidate_vk_id = Column(Integer, nullable=False)
    foto1 = Column(String)
    foto2 = Column(String)
    foto3 = Column(String)
    userss = relationship('User', backref='user_acount')

    def __repr__(self):
        return f'{self.name}  --- Link = https://vk.com/id{self.condidate_vk_id}'


class Favorit(Base):
    __tablename__ = 'favorit'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.user_id'), nullable=False)
    condidate_id = Column(Integer, ForeignKey('condidate.condidate_id'), nullable=False)
    name = Column(String)
    link = Column(String)
    users_favorit = relationship('User', backref='acount_user')
    condidat = relationship('Condidate', backref='condidat')

    def __repr__(self):
        return f'{self.condidate_id} --- '


class Block(Base):
    __tablename__ = 'block'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.user_id'), nullable=False)
    condidate_id = Column(Integer, ForeignKey('condidate.condidate_id'), nullable=False)
    users_block = relationship('User', backref='acounts_user')
    condidat = relationship('Condidate', backref='condidats')
