 # YouTube Media Downloader

 A powerful command-line tool that downloads videos and audio from YouTube, supporting both single videos and playlists.
 The software supports high-quality video downloads and MP3 conversion with custom naming and organization options.

 ## Features:
 - Video and audio download support
 - Single video/audio downloads
 - Playlist download with custom naming
 - Multi-threaded downloads for faster processing  
 - High-quality MP3 conversion (up to 320kbps)
 - Flexible output organization
 - Progress tracking with visual feedback
 - Simple command-line interface
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
     ```bash
     pip install -r requirements.txt
     ```

 ## Usage:

 1. Run the program:
     ```bash
     python src/main.py
     ```

 2. Available Commands:
     - `dl <url> [options]` : Download single video/audio
     - `pl <playlist_url> [options]` : Download from playlist (with confirmation)
     - `apl <playlist_url> [options]` : Auto-download playlist (no confirmation)
         - Options:
             - `-n <number>` : Download only first N items
             - `-r` : Reverse playlist order
             - `-b <bitrate>` : Set MP3 bitrate (128, 192, 256, or 320)
             - `-v` : Download video (default is audio only)
             - `-ka` : Keep audio when downloading video
             - `-kv` : Keep video files (default for video downloads)
             - `-o <output_dir>` : Specify output directory
             - `-pn <name>` : Custom playlist folder name

 3. Examples:
     ```bash
     # Download single video
     dl https://www.youtube.com/watch?v=VIDEO_ID -v

     # Download single audio
     dl https://www.youtube.com/watch?v=VIDEO_ID

     # Download playlist videos with audio conversion
     pl https://www.youtube.com/playlist?list=PLAYLIST_ID -v -ka

     # Download first 5 songs at 320kbps
     pl https://www.youtube.com/playlist?list=PLAYLIST_ID -n 5 -b 320

     # Auto-download last 3 videos with custom folder
     apl https://www.youtube.com/playlist?list=PLAYLIST_ID -n 3 -r -v -pn "My Videos"

     # Download all playlist items in reverse order
     pl https://www.youtube.com/playlist?list=PLAYLIST_ID -r

     # Auto-download entire playlist as audio at 128kbps
     apl https://www.youtube.com/playlist?list=PLAYLIST_ID -b 128
     ```

 ## Directory Structure:
 - `/output/` : Root output directory
     - `/output/video/` : Single video downloads
     - `/output/audio/` : Single audio downloads
     - `/output/playlist/` : Playlist downloads
         - `/output/playlist/[playlist-name]/video/` : Playlist video files
         - `/output/playlist/[playlist-name]/audio/` : Playlist audio files
 - `/ffmpeg/` : Place FFmpeg files here
 - `/src/` : Source code files

 ## Creating an Executable (Windows)

 Using Command Prompt:
 ```bash
 pyinstaller --noconfirm --onefile --windowed ^
     --icon="icons/icon-96.ico" ^
     --collect-all rich ^
     --collect-all certifi ^
     --collect-all charset_normalizer ^
     --collect-all requests ^
     --collect-all urllib3 ^
     --collect-all idna ^
     --collect-all ffmpeg_python ^
     --collect-all yt_dlp ^
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

 Using PowerShell:
 ```powershell
 pyinstaller --noconfirm --onefile --windowed `
     --icon="icons/icon-96.ico" `
     --collect-all rich `
     --collect-all certifi `
     --collect-all charset_normalizer `
     --collect-all requests `
     --collect-all urllib3 `
     --collect-all idna `
     --collect-all ffmpeg_python `
     --collect-all yt_dlp `
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
 - Default audio quality is 192kbps MP3 format
 - Video downloads preserve original quality
 - Files are named according to cleaned up video titles
 - Common suffixes like "Official Video", "Lyrics", etc. are automatically removed
 - Duplicate files are handled automatically
 - Playlist downloads are organized in dedicated folders

 ## Troubleshooting:
 1. If FFmpeg errors occur:
     - Ensure FFmpeg files are in the correct location
     - Check that both ffmpeg.exe and ffprobe.exe are present
 2. For download errors:
     - Check your internet connection
     - Verify the URL is correct and accessible
     - Try updating yt-dlp: `pip install -U yt-dlp`
 3. For video quality issues:
     - Check your internet connection speed
     - Try downloading audio only if video quality is poor

 ## Requirements:
 - yt-dlp
 - rich
 - ffmpeg-python
 - pyinstaller (for creating executable)

 ## License:
 This software is open source and available under the MIT License.