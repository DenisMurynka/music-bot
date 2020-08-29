
from sqlalchemy import create_engine,Table, Column, Integer, String, MetaData, DateTime
from datetime import datetime,date

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session,sessionmaker

###
engine = create_engine('sqlite:///telegrambotDB.db', echo = True)
meta = MetaData()
###
mysession = sessionmaker(bind=engine)
mysession.configure(bind=engine)
##
#meta.create_all(engine) #run once time
##
session = Session()
###
now = datetime.now()
today = date.today()
###
Base = declarative_base()
###
# users = Table(
#    'users', meta,
#    Column('id', Integer, primary_key = True),
#    Column('name', String),
#    Column('lastname', String),
#    Column('username', String),
#    Column('date', DateTime),
# )
class Users(Base):

    __tablename__ = 'users'

    id          = Column(Integer, primary_key=True)
    name        = Column(String(50))
    lastname    = Column(String(50))
    username    = Column(String(50))
    regDate     = Column(DateTime)

    def __init__(self, name, lastname, username):
        self.name = name
        self.lastname = lastname
        self.username = username
        self.regDate =  today.strftime("%d/%m/%Y") +' '+ now.strftime("%H:%M:%S")


    def createSession(self):
        Session = sessionmaker()
        self.session = Session.configure(bind=engine)


using = Table(
   'using', meta,
   Column('id', Integer, primary_key = True),
   Column('name', String),
   Column('lastname', String),
   Column('username', String),
   Column('songname', String),
   Column('date', DateTime),
)

def db_inserting(message,songname):

    engine.execute('INSERT INTO "using" (name,lastname,username,songname,date ) VALUES (?,?,?,?,?) ',
                   (message.from_user.first_name,
                    message.from_user.last_name,
                    message.from_user.username,
                    songname,
                    today.strftime("%d/%m/%Y") +' '+ now.strftime("%H:%M:%S")));


