from aifc import Error
import os
from resource import error
from pytube import Playlist
from utils import create_save_format

def insert_items_in_file(items: list, filename: str) -> None:
    with open(filename, "w") as file:
        for item in items:
            file.write(item + "\n")


def get_credentials(filename: str) -> list:
    credentials = []

    if not os.path.isfile(filename):
        raise Error("auth file don't exist")
    
    if os.path.getsize(filename) == 0:
        raise Error("auth file is empty")

    with open(filename, "r") as file:
        for credential in file:
            credentials.append(credential.strip())
    
    return credentials


def create_list_of_songs():
    url = "https://www.youtube.com/playlist?list=" + get_credentials("../credentials.txt")[0]
    playlist = Playlist(url)

    items = []

    for video in playlist.videos:
        meta = video.metadata

        try:
            data = meta[0]
            if data["Song"]:
                song = create_save_format(video.video_id, str(video.length), data["Song"], True)
                items.append(song)
                print(song)
        except:
            pass
    
    if len(items) != 0:
        insert_items_in_file(items, "../work/database.txt")
 