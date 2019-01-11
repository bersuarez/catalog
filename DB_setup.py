from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy import Column, ForeignKey, Integer, String

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))

    @property
    def serialize(self):
        return{
            'name': self.name,
            'email': self.email,
            'picture': self.picture
        }


class EventType(Base):
    __tablename__ = 'event_type'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(String(100))


class Event(Base):
    __tablename__ = 'event'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(String(100))
    location = Column(String(100))
    category_id = Column(Integer, ForeignKey('event_type.id'))
    category = relationship(EventType)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return{
            'name': self.name,
            'attribute': self.description,
            'location': self.location,
            'creator': self.user.name,
            'creatorpic': self.user.picture,
            'category': self.category.name
        }


engine = create_engine('sqlite:///catalogandusers.db')

Base.metadata.create_all(engine)
