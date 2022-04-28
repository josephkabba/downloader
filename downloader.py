from aifc import Error
from ast import List
from genericpath import isdir
import os
import youtube_dl

# arrange file in music directory
def move_files(id: str):

    save_location_path = "music/" + id + ".mp3"
    residue_path = "music/" +  id + ".webm"

    new_save_location_path = "music/output/" + id + ".mp3"
    new_residue_path = "music/residue/" +  id + ".webm"

    if not os.path.isdir("music/residue/"):
        os.mkdir("music/residue/")

    if not os.path.isdir("music/output/"):
        os.mkdir("music/output/")

    os.replace(save_location_path, new_save_location_path)
    os.replace(residue_path, new_residue_path)



def download_audio(link: str) -> str:
   ydl_opts = {
       'format': 'bestaudio/best',
       'postprocessors': [{
           'key': 'FFmpegExtractAudio',
           'preferredcodec': 'mp3',
           'preferredquality': '192',
       }],
       'ffmpeg-location': './',
       'outtmpl': "./music/%(id)s.%(ext)s",
       'keepvideo': 'False'
   }
   _id = link.strip()
   meta = youtube_dl.YoutubeDL(ydl_opts).extract_info(_id)
   name = meta["id"] + ".mp3"

   move_files(meta["id"])

   return name


def build_url(id: str) -> str:
    url = "http://www.youtube.com/watch?v=" + id
    return url


def read_info_from_file(filename: str) -> list:
    urls = []

    if os.path.getsize(filename) == 0:
        raise Error("videos.txt file is empty")

    with open(filename, "r") as file:
        for line in file:
            data = line.strip().split("###")
            url = build_url(data[0])
            urls.append(url)
       

    return urls


def main():
    urls = read_info_from_file("videos.txt")
    for url in urls:
        name = download_audio(url)
        print("filename: {} \n".format(name))


if __name__ == "__main__":
    main()
