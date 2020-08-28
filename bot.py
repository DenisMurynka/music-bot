import pafy
import telebot                            #pip install telebot
import youtube_dl
import urllib.request
import re,os
from admin import TOKEN
#init
bot = telebot.TeleBot(TOKEN)
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
    bot.reply_to(message, """Hi there, I am EchoBot.""")



# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):

    # print('this is your audio:  ',download_from_youTube(message.text))
    download_from_youTube(message.text)

    bot.reply_to(message,
                 bot.send_audio(
                                message.chat.id,
                                open(get_title(message.text), 'rb'),
                                timeout=20
                                )
                 )


bot.polling(none_stop=True)