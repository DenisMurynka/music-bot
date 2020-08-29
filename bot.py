# by Denis Murynka
import pafy                               #pip install pafy
import telebot                            #pip install telebot
import logging                            #pip install logging
import os
from datetime import datetime
from database import engine, Users, Using
from sqlalchemy.orm import sessionmaker
from ytbURLmanagement import download_from_youTube, get_title
from admin import TOKEN  #TOKEN is yours bot private key

bot = telebot.TeleBot(TOKEN)

day = datetime.today()

Session = sessionmaker(bind=engine)
session = Session()



logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
log = logging.getLogger("ex")


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):

    bot.reply_to(message, 'Hi, ' + message.from_user.first_name + '!')
    session.add(
                Users(
                        name=message.from_user.first_name,
                        lastname=message.from_user.last_name,
                        username=message.from_user.username
                )
    )
    session.commit()


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


        session.add(
                    Using(
                        name=message.from_user.first_name,
                        lastname=message.from_user.last_name,
                        username=message.from_user.username,
                        songname =(pafy.new(message.text)).title,
                        date=day
                    )
        )
        session.commit()

        os.remove((pafy.new(message.text)).title)  #free memory

        raise RuntimeError
    except Exception as e:
        logging.exception("Exception occurred")
        log.exception(e)





bot.polling(none_stop=True)