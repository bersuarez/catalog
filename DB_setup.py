from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy import Column, ForeignKey, Integer, String

Base = declarative_base()

class DummyCategory(Base):
    __tablename__='dummy_category'
    id=Column(Integer,primary_key=True)
    attribute=Column(String(100))

class DummyItem(Base):
    __tablename__='dummy_item'
    id=Column(Integer,primary_key=True)
    attribute=Column(String(100))
    category_id = Column(Integer, ForeignKey('dummy_category.id'))
    category=relationship(DummyCategory)


engine = create_engine('sqlite:///catalog.db')

Base.metadata.create_all(engine)