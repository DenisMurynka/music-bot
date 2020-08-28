# by Denis Murynka
import pafy
import telebot                            #pip install telebot
import youtube_dl
import logging
import re,os
from datetime import datetime,date
from sqlalchemy import create_engine,Table, Column, Integer, String, MetaData,Date,DateTime

from admin import TOKEN

now = datetime.now()

bot = telebot.TeleBot(TOKEN)

engine = create_engine('sqlite:///college.db', echo = True)
meta = MetaData()
###
logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
log = logging.getLogger("ex")
##
users = Table(
   'users', meta,
   Column('id', Integer, primary_key = True),
   Column('name', String),
   Column('lastname', String),
   Column('username', String),
   Column('songname', String),
   Column('date', DateTime),
)


#meta.create_all(engine) #run once time

def db_inserting(message,songname):
    today = date.today()
    engine.execute('INSERT INTO "users" (name,lastname,username,songname,date ) VALUES (?,?,?,?,?) ',
                   (message.from_user.first_name,
                    message.from_user.last_name,
                    message.from_user.username,
                    songname,
                    today.strftime("%d/%m/%Y") +' '+ now.strftime("%H:%M:%S")));


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
    try:
        download_from_youTube(message.text)

        bot.send_audio(
                       message.chat.id,
                       open(get_title(message.text), 'rb'),
                       timeout=20
                      )

        db_inserting(message, (pafy.new(message.text)).title)

        os.remove((pafy.new(message.text)).title) #free memory
        raise RuntimeError
    except Exception as e:
        logging.exception("Exception occurred")
        log.exception(e)


bot.polling(none_stop=True)