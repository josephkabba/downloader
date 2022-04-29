from youtube import create_list_of_songs
from downloader import download
import os

def main():
    print("Welcome to youtube playlist downloader" + "\n")
    print("Please read the readme.md file, if your new")

    if not os.path.isdir("../work/"):
        os.mkdir("../work/")

    while True:
        command = input("Enter command: ")
        if command == "h":
            print("h - help")
            print("cs - create save format")
            print("dl - download audio")
            print("a - run download song ids and download audio files")
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
        elif command == "q":
            print("Quitting")
            break
        else:
            print("Invalid command")
            print("Please enter \"h\" to know available commands")
        print("\n")


if __name__ == "__main__":
    main()