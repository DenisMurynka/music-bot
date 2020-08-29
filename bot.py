# by Denis Murynka
import pafy                               #pip install pafy
import telebot                            #pip install telebot
import logging                            #pip install logging
import os

from database import db_inserting
from ytbURLmanagement import download_from_youTube, get_title
from admin import TOKEN  #TOKEN is yours bot private key
from database import Users
bot = telebot.TeleBot(TOKEN)

from sqlalchemy.orm import Session,sessionmaker

logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
log = logging.getLogger("ex")


#session = Session()

# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, 'Hi, ' + message.from_user.first_name + '!')



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

        os.remove((pafy.new(message.text)).title)  #free memory
        raise RuntimeError
    except Exception as e:
        logging.exception("Exception occurred")
        log.exception(e)


    #
    # session.add(
    # Users(
    #                 name=message.from_user.first_name,
    #                 lastname=message.from_user.last_name,
    #                 username=message.from_user.username
    #             )
    # )
    #
    # session.commit()
    # session.close()


bot.polling(none_stop=True)