from aifc import Error
import os
from resource import error
from pytube import Playlist

def insert_items_in_file(items: list) -> None:
    with open("videos.txt", "w") as file:
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

def create_save_format(id: str, duration: str, title: str) -> str:
    return id + "###" + duration + "###" + title


def main():
    url = "https://www.youtube.com/playlist?list=" + get_credentials("credentials.txt")[0]
    playlist = Playlist(url)

    items = []

    for video in playlist.videos:
        meta = video.metadata

        try:
            data = meta[0]
            if data["Song"]:
                song = create_save_format(video.video_id, str(video.length), data["Song"])
                items.append(song)
                print(song)
        except:
            pass
    
    if len(items) != 0:
        insert_items_in_file(items)
 

if __name__ == "__main__":
    main()