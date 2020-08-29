
from sqlalchemy import create_engine,Table, Column, Integer, String, MetaData, DateTime
from datetime import datetime,date

###
engine = create_engine('sqlite:///college.db', echo = True)
meta = MetaData()
###
now = datetime.now()
users = Table(
   'users', meta,
   Column('id', Integer, primary_key = True),
   Column('name', String),
   Column('lastname', String),
   Column('username', String),
   Column('songname', String),
   Column('date', DateTime),
)

def db_inserting(message,songname):
    today = date.today()
    engine.execute('INSERT INTO "users" (name,lastname,username,songname,date ) VALUES (?,?,?,?,?) ',
                   (message.from_user.first_name,
                    message.from_user.last_name,
                    message.from_user.username,
                    songname,
                    today.strftime("%d/%m/%Y") +' '+ now.strftime("%H:%M:%S")));
