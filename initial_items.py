from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from DB_setup import Base, DummyCategory, DummyItem

engine = create_engine('sqlite:///catalog.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

dummyCategory1 = DummyCategory(name='category1',attribute='blabla')
session.add(dummyCategory1)
session.commit()

dummyItem1 = DummyItem(name='item1',attribute='BLABLA', category=dummyCategory1)
session.add(dummyItem1)
session.commit()