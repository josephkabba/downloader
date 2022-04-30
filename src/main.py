from database import clean_database
from youtube import create_list_of_songs
from downloader import download
import os

def console():
    try:
        while True:
            command = input("Enter command: ")
            if command == "h":
                print("h - help")
                print("cs - create save format")
                print("dl - download audio")
                print("a - run download song ids and download audio files")
                print("dbclean - cleans the database file")
                print("q - quit")
            elif command == "cs":
                print("Starting: creating song list")
                create_list_of_songs()
                print("Finished: creating song list")
            elif command == "dl":
                print("Downloading songs")
                download()
                print("Downloading songs complete")
            elif command == "a":
                print("Starting: creating song list")
                create_list_of_songs()
                print("Finished: creating song list")
                print("Downloading songs")
                download()
                print("Downloading songs complete")
            elif command == "dbclean":
                print("Cleaning database file")
                clean_database()
                print("Database cleaning complete")
            elif command == "q":
                print("Quitting")
                break
            else:
                print("Invalid command")
                print("Please enter \"h\" to know available commands")
                print("\n")
    except Exception as e:
            print(e)

def main():
    print("Welcome to youtube playlist downloader" + "\n")
    print("Please read the readme.md file, if your new")

    if not os.path.isdir("../work/"):
        os.mkdir("../work/")

    console()


if __name__ == "__main__":
    main()