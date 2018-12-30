from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from DB_setup import Base, DummyCategory, DummyItem, User

engine = create_engine('sqlite:///catalogandusers.db', connect_args={'check_same_thread': False})

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

dummyCategory1 = DummyCategory(name='category1',attribute='blabla')
session.add(dummyCategory1)
session.commit()

dummyCategory2 = DummyCategory(name='category2',attribute='blabla2')
session.add(dummyCategory2)
session.commit()

dummyCategory3 = DummyCategory(name='category3',attribute='blabla3')
session.add(dummyCategory3)
session.commit()

dummyCategory4 = DummyCategory(name='category4',attribute='blabla4')
session.add(dummyCategory4)
session.commit()

dummyCategory5 = DummyCategory(name='category5',attribute='blabl5')
session.add(dummyCategory5)
session.commit()

dummyItem1 = DummyItem(name='item1',attribute='BLABLA', category=dummyCategory1, user_id=1)
session.add(dummyItem1)
session.commit()

User1 = User(name="Robo Barista", email="tinnyTim@udacity.com",picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()