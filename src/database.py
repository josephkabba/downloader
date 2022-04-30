from aifc import Error
import os


def read_file_data(filename: str) -> list:
    data = []

    if os.path.getsize(filename) == 0:
        raise Error("file is empty")

    with open(filename, "r") as file:
        for line in file:
            song_data = (line.strip().split("###")[0], line.strip())
            data.append(song_data)
       
    return data

def clean_database():
    pending_data = read_file_data("../work/database.txt")
    downloaded_files = read_file_data("../work/downloaded_files.txt")

    last_song = downloaded_files[len(downloaded_files) - 1]
    save_files = False

    new_pending_data = []

    for id, song in pending_data:
        if save_files:
            new_pending_data.append(song)

        if id == last_song[0]:
            save_files = True

    if len(new_pending_data) > 0:
        with open("../work/database.txt", "w") as file:
            for song in new_pending_data:
                file.write(song + "\n")

