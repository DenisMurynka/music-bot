import youtube_dl               #pip install youtube_dl
import re, pafy, os             #pip install pafy


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
