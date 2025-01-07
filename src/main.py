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
    console.print("  [cyan]dl <playlist_url> [options][/cyan] - Download songs from a YouTube playlist")
    console.print("  [cyan]adl <playlist_url> [options][/cyan] - Auto-download songs (no confirmation)")
    console.print("    Options:")
    console.print("      [dim]-n <number>[/dim] - Download only first N songs")
    console.print("      [dim]-r[/dim] - Reverse playlist order")
    console.print("      [dim]-b <bitrate>[/dim] - Set MP3 bitrate (e.g., 128, 192, 320)")
    console.print("    Example: dl URL -n 5 -r -b 320")
    console.print("  [cyan]help[/cyan] - Show this help message")
    console.print("  [cyan]quit[/cyan] - Exit the program\n")
    
def parse_dl_options(args):
    """Parse download command options"""
    options = {
        'url': None,
        'limit': None,
        'reverse': False,
        'bitrate': '192'  # default bitrate
    }
    
    i = 1
    while i < len(args):
        if i == 1:
            options['url'] = args[i]
        elif args[i] == '-n' and i + 1 < len(args):
            try:
                limit = int(args[i + 1])
                if limit <= 0:
                    raise ValueError("Limit must be positive")
                options['limit'] = limit
                i += 1
            except ValueError as e:
                raise ValueError(f"Invalid limit value: {e}")
        elif args[i] == '-r':
            options['reverse'] = True
        elif args[i] == '-b' and i + 1 < len(args):
            try:
                bitrate = args[i + 1]
                if bitrate not in ['128', '192', '256', '320']:
                    raise ValueError("Bitrate must be 128, 192, 256, or 320")
                options['bitrate'] = bitrate
                i += 1
            except ValueError as e:
                raise ValueError(f"Invalid bitrate value: {e}")
        i += 1
    
    if not options['url']:
        raise ValueError("No URL provided")
    
    return options

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
            elif command[0] in ["dl", "adl"]:
                try:
                    options = parse_dl_options(command)
                    console.print("[cyan]Fetching playlist...[/cyan]")
                    songs = get_playlist_songs(
                        options['url'], 
                        reverse=options['reverse'],
                        limit=options['limit']
                    )
                    
                    if not songs:
                        console.print("[red]No songs found in playlist")
                        continue

                    # Apply limit if specified
                    if options['limit']:
                        original_count = len(songs)
                        songs = songs[:options['limit']]
                        console.print(f"[green]Selected {len(songs)} of {original_count} songs from playlist")
                        if options['reverse']:
                            console.print("[cyan]Note: Songs are taken from the end of the playlist")
                    else:
                        console.print(f"[green]Found {len(songs)} songs in playlist")
                        if options['reverse']:
                            console.print("[cyan]Note: Playlist order is reversed")

                    if command[0] == "adl" or Prompt.ask("Do you want to download them?", choices=["y", "n"]) == "y":
                        downloader.download_playlist(songs, bitrate=options['bitrate'])
                        console.print("[green]Download complete!")
                except ValueError as e:
                    console.print(f"[red]Error: {str(e)}")
                    continue
                except Exception as e:
                    console.print(f"[red]Error processing playlist: {str(e)}")
                    continue
            else:
                console.print("[red]Invalid command. Type 'help' for available commands")

        except KeyboardInterrupt:
            console.print("\n[yellow]Operation cancelled by user")
            break
        except Exception as e:
            console.print(f"[red]Error: {str(e)}")

    console.print("[yellow]Goodbye!")

if __name__ == "__main__":
    main()