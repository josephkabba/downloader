from aifc import Error
from ast import List
from genericpath import isdir
import os
import youtube_dl
from utils import create_save_format, format_name

# arrange file in music directory
def move_files(id: str, title: str):

    save_location_path = "../work/music/" + id + ".mp3"

    new_save_location_path = "../work/music/output/" + id + ".mp3"

    if not os.path.isdir("../work/music/output/"):
        os.mkdir("../work/music/output/")

    os.replace(save_location_path, new_save_location_path)

    if len(title) != 0:
        title_src = "../work/music/output/" + title + ".mp3"
        os.rename(new_save_location_path, title_src)



def download_audio(link: str) -> tuple:
   ydl_opts = {
       'format': 'bestaudio/best',
       'postprocessors': [{
           'key': 'FFmpegExtractAudio',
           'preferredcodec': 'mp3',
           'preferredquality': '192',
       }],
       'retries': 10,
       'continuedl': 'True',
       'ffmpeg-location': './',
       'outtmpl': "../work/music/%(id)s.%(ext)s",
       'keepvideo': 'False'
   }
   _id = link.strip()
   meta = youtube_dl.YoutubeDL(ydl_opts).extract_info(_id)
   id = meta["id"].strip()
   name = meta["title"].strip()

   return (id, name)


def build_url(id: str) -> str:
    url = "http://www.youtube.com/watch?v=" + id
    return url


def read_info_from_file(filename: str) -> list:
    urls_and_names = []

    if os.path.getsize(filename) == 0:
        raise Error("database.txt file is empty")

    with open(filename, "r") as file:
        for line in file:
            data = line.strip().split("###") 
            url = build_url(data[0])
            name = data[3]
            urls_and_names.append((url, name))
       
    return urls_and_names


def write_info_to_file(id: str, name: str, filename: str, duration = "0",):
    with open(filename, "a+") as file:
        item = create_save_format(id, duration, name, False)
        file.write(item + "\n")

def download():
    filename = "../work/database.txt"
    urls_and_names = read_info_from_file(filename)
    for url, name in urls_and_names:
        try:
            id, audio_name = download_audio(url)
            move_files(id, format_name(name))
            write_info_to_file(id, name, "../work/downloaded_files.txt")
            print("filename: {} \n".format(audio_name))
        except Error as e:
            print(e)

