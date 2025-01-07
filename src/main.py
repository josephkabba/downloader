from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from downloader import YouTubeDownloader
from youtube import get_playlist_songs
import subprocess
import sys
import platform

console = Console()

def check_ffmpeg():
    """Check if FFmpeg is installed and accessible"""
    try:
        subprocess.run(['ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        return False

def display_ffmpeg_instructions():
    """Display FFmpeg installation instructions based on the operating system"""
    os_type = platform.system().lower()
    
    instructions = {
        'windows': """[yellow]FFmpeg is not installed or not in PATH. To install FFmpeg on Windows:

1. Download FFmpeg from: https://github.com/BtbN/FFmpeg-Builds/releases
2. Download the file: ffmpeg-master-latest-win64-gpl.zip
3. Extract the zip file
4. Add the bin folder to your system PATH:
   - Right-click 'This PC' → Properties
   - Click 'Advanced system settings'
   - Click 'Environment Variables'
   - Under 'System Variables', select 'Path'
   - Click 'Edit' → 'New'
   - Add the path to ffmpeg's bin folder
   - Click 'OK' on all windows
5. Restart your terminal[/yellow]""",
        
        'darwin': """[yellow]FFmpeg is not installed. To install FFmpeg on macOS:

1. Using Homebrew:
   brew install ffmpeg

2. Or using MacPorts:
   sudo port install ffmpeg[/yellow]""",
        
        'linux': """[yellow]FFmpeg is not installed. To install FFmpeg on Linux:

Ubuntu/Debian:
   sudo apt update
   sudo apt install ffmpeg

Fedora:
   sudo dnf install ffmpeg

Arch Linux:
   sudo pacman -S ffmpeg[/yellow]"""
    }
    
    console.print(Panel(
        instructions.get(os_type, "[yellow]Please install FFmpeg from: https://ffmpeg.org/download.html[/yellow]"),
        title="[red]FFmpeg Not Found[/red]",
        expand=False
    ))

def display_help():
    console.print("\n[green]Available commands:")
    console.print("  [cyan]dl <playlist_url>[/cyan] - Download songs from a YouTube playlist")
    console.print("  [cyan]help[/cyan] - Show this help message")
    console.print("  [cyan]quit[/cyan] - Exit the program\n")

def main():
    # Check for FFmpeg before starting
    if not check_ffmpeg():
        display_ffmpeg_instructions()
        console.print("\n[red]Please install FFmpeg and try again.[/red]")
        sys.exit(1)

    console.print("[bold green]YouTube Playlist Downloader[/bold green]")
    display_help()

    downloader = YouTubeDownloader(max_workers=4)

    while True:
        try:
            command = Prompt.ask("[cyan]Enter command").strip().split()
            
            if not command:
                continue

            if command[0] == "quit":
                break
            elif command[0] == "help":
                display_help()
            elif command[0] == "dl":
                if len(command) < 2:
                    console.print("[red]Error: Please provide a playlist URL")
                    continue

                url = command[1]
                songs = get_playlist_songs(url)
                
                if not songs:
                    console.print("[red]No songs found in playlist")
                    continue

                console.print(f"[green]Found {len(songs)} songs in playlist")
                if Prompt.ask("Do you want to download them?", choices=["y", "n"]) == "y":
                    downloader.download_playlist(songs)
                    console.print("[green]Download complete!")
            else:
                console.print("[red]Invalid command. Type 'help' for available commands")

        except KeyboardInterrupt:
            console.print("\n[yellow]Operation cancelled by user")
        except Exception as e:
            console.print(f"[red]Error: {str(e)}")

if __name__ == "__main__":
    main()