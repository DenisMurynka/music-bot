# by Denis Murynka
import pafy
import telebot                            #pip install telebot
import youtube_dl
import urllib.request
import re,os
import datetime
from sqlalchemy import create_engine,Table, Column, Integer, String, MetaData,Date,DateTime
from admin import TOKEN

bot = telebot.TeleBot(TOKEN)

engine = create_engine('sqlite:///college.db', echo = True)
meta = MetaData()

users = Table(
   'users', meta,
   Column('id', Integer, primary_key = True),
   Column('name', String),
   Column('lastname', String),
   Column('username', String),
   Column('songname', String),
   Column('date', DateTime,default=datetime.datetime.utcnow),
)


#meta.create_all(engine) #run once time

def db_inserting(message,songname):
    users.insert().values(name=message.from_user.first_name)
    users.insert().values(lastname=message.from_user.last_name)
    users.insert().values(username=message.from_user.username)
    users.insert().values(songname=songname)

def get_title(youtube_string):
    video_title = pafy.new(youtube_string)  # instant created
    regex = re.compile(
        r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?(?P<id>[A-Za-z0-9\-=_]{11})')
    match = regex.match(youtube_string)

    os.rename(video_title.title + '-' + match.group('id') + '.mp3', video_title.title)

    return video_title.title
def download_from_youTube(youtube_string):  ##Download from YOUTUBE
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '64',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_string])



# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message,'Hi, '+str(message.from_user.first_name)+'!')



# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):

    # print('this is your audio:  ',download_from_youTube(message.text))
    download_from_youTube(message.text)


    bot.send_audio(
                   message.chat.id,
                   open(get_title(message.text), 'rb'),
                   timeout=20
                  )

    db_inserting(message, (pafy.new(message.text)).title)

    os.remove((pafy.new(message.text)).title) #free memory

bot.polling(none_stop=True)