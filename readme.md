 YouTube Playlist Music Downloader

 A powerful command-line tool that automatically detects and downloads music from YouTube playlists.
 The software specifically identifies songs from video metadata and downloads them in high-quality MP3 format.

 Features:
 - Multi-threaded downloads for faster processing
 - Automatic music detection from playlist videos
 - High-quality MP3 conversion
 - Progress tracking with visual feedback
 - Simple command-line interface

 Prerequisites:
 1. FFmpeg Components
    - Download ffmpeg, ffprobe, and ffplay from: https://ffmpeg.org/download.html
    - Add them to your system PATH or place them in the same directory as the script

 2. Python Requirements
    - Python 3.7 or higher
    - pip (Python package manager)

 Installation:
 1. Install Python dependencies:
    ```
    pip install -r requirements.txt
    ```

 Usage:
 1. Run the program:
    ```
    python main.py
    ```

 2. Available Commands:
    - dl <playlist_url> : Download songs from a YouTube playlist
    - help             : Show available commands
    - quit            : Exit the program

 Example:
    ```
    Enter command: dl https://www.youtube.com/playlist?list=YOUR_PLAYLIST_ID
    ```

 Directory Structure:
 - /work/music/output/ : Contains the downloaded MP3 files
 - /work/             : Contains program output and temporary files

 Notes:
 - Only videos with proper music metadata will be detected and downloaded
 - Downloads are automatically converted to 192kbps MP3 format
 - Files are named according to the song title from the video metadata

 Troubleshooting:
 1. If FFmpeg errors occur, ensure FFmpeg components are properly installed
 2. For download errors, check your internet connection and playlist URL
 3. If no songs are detected, ensure the playlist videos have proper music metadata

 Requirements:
 - youtube_dl
 - pytube
 - rich
 - ffmpeg-python

License:
This software is open source and available under the MIT License.