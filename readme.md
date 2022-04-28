This is the playlist music youtube downloader.

The software can detect music in a playlist and download it.

How to use the software.

1.  Download ffmpeg, ffprobe, ffplay
2.  Configure ffmpeg, ffprobe and ffplay into your file system.
3.  Download python and pip onto your system.
4.  Run the "pip install -r requirements.txt" command with the requirements.txt as an arguement.
5.  Create a credentials.txt file.
6.  Add your api key and playlist id on two different lines.
    example:

        api_key
        playlist_id

    NB: Please generate the api_key from your Google api IAM.
    Check google documentation for more information

7.  Run youtube.py
8.  Run downloader.py
9.  Th music will be available in the music directory.
