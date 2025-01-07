# YouTube Playlist Music Downloader

A powerful command-line tool that automatically detects and downloads music from YouTube playlists.
The software downloads songs in high-quality MP3 format with custom naming and ordering options.

## Features:
- Multi-threaded downloads for faster processing  
- High-quality MP3 conversion (192kbps)
- Progress tracking with visual feedback
- Simple command-line interface
- Flexible download options (limit number of songs, reverse order)
- Smart file naming and duplicate handling

## Prerequisites:
1. FFmpeg Components
   - Download ffmpeg, ffprobe from: https://github.com/BtbN/FFmpeg-Builds/releases
   - Extract to `ffmpeg` folder in project root
   - No PATH configuration needed

2. Python Requirements
   - Python 3.7 or higher
   - pip (Python package manager)

## Installation:

1. Clone or download this repository
2. Install Python dependencies:
```
pip install -r requirements.txt
```

## Usage:

1. Run the program:
```
python src/main.py
```

2. Available Commands:
   - `dl <playlist_url> [options]` : Download songs from a YouTube playlist
     - Options:
       - `-n <number>` : Download only first N songs
       - `-r` : Reverse playlist order
   - `help` : Show available commands
   - `quit` : Exit the program

3. Examples:
```
# Download entire playlist
dl https://www.youtube.com/playlist?list=YOUR_PLAYLIST_ID

# Download first 5 songs
dl https://www.youtube.com/playlist?list=YOUR_PLAYLIST_ID -n 5

# Download last 3 songs
dl https://www.youtube.com/playlist?list=YOUR_PLAYLIST_ID -n 3 -r

# Download all songs in reverse order
dl https://www.youtube.com/playlist?list=YOUR_PLAYLIST_ID -r
```

## Directory Structure:
- `/work/music/output/` : Contains the downloaded MP3 files
- `/work/` : Contains program output and temporary files
- `/ffmpeg/` : Place FFmpeg files here
- `/src/` : Source code files

## Creating an Executable (Windows)

Using Command Prompt:
```
pyinstaller --noconfirm --onefile --windowed ^
  --add-data "ffmpeg/bin/ffmpeg.exe;." ^
  --add-data "ffmpeg/bin/ffprobe.exe;." ^
  --icon="icons/icon-96.ico" ^
  --hidden-import=rich.console ^
  --hidden-import=rich.prompt ^
  --hidden-import=rich.progress ^
  --hidden-import=rich.panel ^
  --hidden-import=yt_dlp ^
  src/main.py
```

Using PowerShell:
```
pyinstaller --noconfirm --onefile --windowed `
  --add-data "ffmpeg/bin/ffmpeg.exe;." `
  --add-data "ffmpeg/bin/ffprobe.exe;." `
  --icon="icons/icon-96.ico" `
  --hidden-import=rich.console `
  --hidden-import=rich.prompt `
  --hidden-import=rich.progress `
  --hidden-import=rich.panel `
  --hidden-import=yt_dlp `
  src/main.py
```

## Notes:
- Downloads are automatically converted to 192kbps MP3 format
- Files are named according to cleaned up video titles
- Common suffixes like "Official Video", "Lyrics", etc. are automatically removed
- Duplicate files are handled automatically

## Troubleshooting:
1. If FFmpeg errors occur:
   - Ensure FFmpeg files are in the correct location
   - Check that both ffmpeg.exe and ffprobe.exe are present
2. For download errors:
   - Check your internet connection
   - Verify the playlist URL is correct and accessible
   - Try updating yt-dlp: `pip install -U yt-dlp`

## Requirements:
- yt-dlp
- rich
- ffmpeg-python
- pyinstaller (for creating executable)

## License:
This software is open source and available under the MIT License.