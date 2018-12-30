from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy import Column, ForeignKey, Integer, String

Base = declarative_base()

class User(Base):
    __tablename__='user'
    id = Column(Integer,primary_key=True)
    name = Column(String(250), nullable = False)
    email = Column(String(250), nullable = False)
    picture = Column(String(250)) 

class DummyCategory(Base):
    __tablename__='dummy_category'
    id=Column(Integer,primary_key=True)
    name =Column(String(80), nullable = False)
    attribute=Column(String(100))

    @property
    def serialize(self):
        return{
            'name' : self.name,
            'attribute' : self.attribute
        }

class DummyItem(Base):
    __tablename__ = 'dummy_item'
    id = Column(Integer,primary_key=True)
    name = Column(String(80), nullable = False)
    attribute = Column(String(100))
    category_id = Column(Integer, ForeignKey('dummy_category.id'))
    category = relationship(DummyCategory)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    
    @property
    def serialize(self):
        return{
            'name' : self.name,
            'attribute' : self.attribute
        }

engine = create_engine('sqlite:///catalogandusers.db')

Base.metadata.create_all(engine)