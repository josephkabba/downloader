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
   - `dl <playlist_url> [options]` : Download songs from a YouTube playlist (with confirmation)
   - `adl <playlist_url> [options]` : Auto-download songs from playlist (no confirmation)
     - Options:
       - `-n <number>` : Download only first N songs
       - `-r` : Reverse playlist order
       - `-b <bitrate>` : Set MP3 bitrate (128, 192, 256, or 320)
   - `help` : Show available commands
   - `quit` : Exit the program

3. Examples:
```
# Download entire playlist (with confirmation)
dl https://www.youtube.com/playlist?list=YOUR_PLAYLIST_ID

# Download first 5 songs at 320kbps
dl https://www.youtube.com/playlist?list=YOUR_PLAYLIST_ID -n 5 -b 320

# Auto-download last 3 songs at 256kbps
adl https://www.youtube.com/playlist?list=YOUR_PLAYLIST_ID -n 3 -r -b 256

# Download all songs in reverse order at default quality (192kbps)
dl https://www.youtube.com/playlist?list=YOUR_PLAYLIST_ID -r

# Auto-download entire playlist at 128kbps
adl https://www.youtube.com/playlist?list=YOUR_PLAYLIST_ID -b 128
```

## Directory Structure:
- `/work/music/output/` : Contains the downloaded MP3 files
- `/work/` : Contains program output and temporary files
- `/ffmpeg/` : Place FFmpeg files here and then add the bin of ffmpeg to your path environmental virables of your system (Windows only)
- `/src/` : Source code files

## Creating an Executable (Windows)

Using Command Prompt (This is an example get the dependencies from the requirements.txt):
```
pyinstaller --noconfirm --onefile --windowed ^
  --icon="icons/icon-96.ico" ^
  --collect-all rich ^
  --collect-all certifi ^
  --collect-all charset_normalizer ^
  --collect-all requests ^
  --collect-all urllib3 ^
  --collect-all idna ^
  --collect-all ffmpeg_python ^
  --collect-data beautifulsoup4 ^
  --hidden-import=rich.console ^
  --hidden-import=rich.prompt ^
  --hidden-import=rich.progress ^
  --hidden-import=rich.panel ^
  --hidden-import=soupsieve ^
  --hidden-import=requests ^
  --hidden-import=urllib3 ^
  --hidden-import=certifi ^
  --hidden-import=charset_normalizer ^
  --hidden-import=idna ^
  --hidden-import=ffmpeg_python ^
  --hidden-import=ffmpeg-python ^
  src/main.py
```

Using PowerShell (This is an example get the dependencies from the requirements.txt):
```
pyinstaller --noconfirm --onefile --windowed `
  --icon="icons/icon-96.ico" `
  --collect-all rich `
  --collect-all certifi `
  --collect-all charset_normalizer `
  --collect-all requests `
  --collect-all urllib3 `
  --collect-all idna `
  --collect-all ffmpeg_python `
  --collect-data beautifulsoup4 `
  --hidden-import=rich.console `
  --hidden-import=rich.prompt `
  --hidden-import=rich.progress `
  --hidden-import=rich.panel `
  --hidden-import=soupsieve `
  --hidden-import=requests `
  --hidden-import=urllib3 `
  --hidden-import=certifi `
  --hidden-import=charset_normalizer `
  --hidden-import=idna `
  --hidden-import=ffmpeg_python `
  --hidden-import=ffmpeg-python `
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