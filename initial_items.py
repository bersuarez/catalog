from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from DB_setup import Base, EventType, Event, User

engine = create_engine('sqlite:///catalogandusers.db', connect_args={'check_same_thread': False})

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

dummyCategory1 = EventType(name='sports', description='blabla')
session.add(dummyCategory1)
session.commit()

dummyCategory2 = EventType(name='social', description='blabla2')
session.add(dummyCategory2)
session.commit()

dummyCategory3 = EventType(name='work', description='blabla3')
session.add(dummyCategory3)
session.commit()

dummyCategory4 = EventType(name='spiritual', description='blabla4')
session.add(dummyCategory4)
session.commit()

dummyCategory5 = EventType(name='leisure', description='blabl5')
session.add(dummyCategory5)
session.commit()

User1 = User(name="Juan Perez", email="juan@perez.com",picture='https://i.pinimg.com/originals/63/a5/e8/63a5e8ee8cdcfab2f952bcd46a73e5c4.jpg')
session.add(User1)
session.commit()

User2 = User(name="Mr Robot", email="mr@robot.com",picture='https://www.avaus.fi/wp-content/uploads/2015/08/AMI_newsletter_blog_strategia_tiimi_850x650.jpg')
session.add(User2)
session.commit()

User3 = User(name="Obama", email="mr@barack.com",picture='https://pbs.twimg.com/profile_images/822547732376207360/5g0FC8XX_400x400.jpg')
session.add(User3)
session.commit()

dummyItem1 = Event(name='Trip', description='This year we decided to go to Morocco, mainly because it seemed inexpensive, but after the vacation we were definitely in love with the place.', category=dummyCategory5, location = 'Marrakech', user_id=1)
session.add(dummyItem1)
session.commit()

dummyItem2 = Event(name='Retreat',description='Eye oppening retreat to a marvelous place', category=dummyCategory4, location = 'Bali', user_id=2)
session.add(dummyItem2)
session.commit()

dummyItem3 = Event(name='Cool party',description='Got to hang out with my pals', category=dummyCategory2, location = 'Cancun', user_id=3)
session.add(dummyItem3)
session.commit()



