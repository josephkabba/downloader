from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from downloader import YouTubeDownloader
from youtube import get_playlist_media, get_single_video_info, process_url
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
    console.print("  [cyan]dl <url> [options][/cyan] - Download single video/audio")
    console.print("  [cyan]pl <playlist_url> [options][/cyan] - Download from playlist")
    console.print("  [cyan]apl <playlist_url> [options][/cyan] - Auto-download playlist (no confirmation)")
    console.print("    Options:")
    console.print("      [dim]-n <number>[/dim] - Download only first N items")
    console.print("      [dim]-r[/dim] - Reverse playlist order")
    console.print("      [dim]-b <bitrate>[/dim] - Set MP3 bitrate (128, 192, 256, 320)")
    console.print("      [dim]-v[/dim] - Download video (default is audio only)")
    console.print("      [dim]-ka[/dim] - Keep audio when downloading video")
    console.print("      [dim]-kv[/dim] - Keep video files (default for video downloads)")
    console.print("      [dim]-o <output_dir>[/dim] - Specify output directory")
    console.print("      [dim]-pn <name>[/dim] - Custom playlist folder name")
    console.print("      [dim]-so[/dim] - Download only songs from playlist (filters out non-music content)")
    console.print("    Example: pl URL -n 5 -r -b 320 -v -ka -o /downloads")
    console.print("  [cyan]help[/cyan] - Show this help message")
    console.print("  [cyan]quit[/cyan] - Exit the program\n")

def parse_options(args):
    """Parse command options"""
    options = {
        'url': None,
        'limit': None,
        'reverse': False,
        'bitrate': '192',
        'download_video': False,
        'keep_video': True,
        'convert_to_audio': False,
        'output_dir': 'output',
        'playlist_name': None,
        'songs_only': False
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
        elif args[i] == '-v':
            options['download_video'] = True
        elif args[i] == '-ka':
            options['convert_to_audio'] = True
        elif args[i] == '-kv':
            options['keep_video'] = True
        elif args[i] == '-o' and i + 1 < len(args):
            path_parts = []
            j = i + 1
            while j < len(args) and not args[j].startswith('-'):
                path_parts.append(args[j])
                j += 1
            options['output_dir'] = ' '.join(path_parts)
            i = j - 1
        elif args[i] == '-pn' and i + 1 < len(args):
            options['playlist_name'] = args[i + 1]
            i += 1
        elif args[i] == '-so':
            options['songs_only'] = True
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

    console.print("[bold green]Tube Media Downloader[/bold green]")
    display_help()

    while True:
        try:
            command = Prompt.ask("[cyan]Enter command").strip().split()
            
            if not command:
                continue

            if command[0] == "quit":
                break
            elif command[0] == "help":
                display_help()
            elif command[0] in ["dl", "pl", "apl"]:
                try:
                    options = parse_options(command)
                    downloader = YouTubeDownloader(output_dir=options['output_dir'])

                    # Process and validate the URL first
                    console.print("[cyan]Processing URL...[/cyan]")
                    processed_url, is_playlist = process_url(options['url'])
                    
                    # Validate command matches URL type
                    if command[0] == "dl" and is_playlist:
                        console.print("[yellow]Use 'pl' or 'apl' commands for playlist downloads")
                        continue
                    elif command[0] in ["pl", "apl"] and not is_playlist:
                        console.print("[yellow]Use 'dl' command for single video downloads")
                        continue

                    # Update the URL with the processed one
                    options['url'] = processed_url

                    if command[0] == "dl":
                        # Single video/audio download
                        console.print("[cyan]Fetching video information...[/cyan]")
                        media = get_single_video_info(options['url'])
                        if media:
                            downloader.download_media(
                                media,
                                download_video=options['download_video'],
                                keep_video=options['keep_video'],
                                convert_to_audio=options['convert_to_audio'],
                                bitrate=options['bitrate']
                            )
                            console.print("[green]Download complete!")
                    else:  # pl or apl
                        # Playlist download
                        console.print("[cyan]Fetching playlist...[/cyan]")
                        media_items = get_playlist_media(
                            options['url'],
                            playlist_name=options['playlist_name'],
                            reverse=options['reverse'],
                            limit=options['limit'],
                            songs_only=options['songs_only']
                        )
                        
                        if not media_items:
                            console.print("[red]No items found in playlist")
                            continue

                        if options['limit']:
                            original_count = len(media_items)
                            media_items = media_items[:options['limit']]
                            console.print(f"[green]Selected {len(media_items)} of {original_count} items from playlist")
                            if options['reverse']:
                                console.print("[cyan]Note: Items are taken from the end of the playlist")
                        else:
                            console.print(f"[green]Found {len(media_items)} items in playlist")
                            if options['reverse']:
                                console.print("[cyan]Note: Playlist order is reversed")

                        if command[0] == "apl" or Prompt.ask("Do you want to download them?", choices=["y", "n"]) == "y":
                            downloader.download_playlist(
                                media_items,
                                download_video=options['download_video'],
                                keep_video=options['keep_video'],
                                convert_to_audio=options['convert_to_audio'],
                                bitrate=options['bitrate']
                            )
                            console.print("[green]Download complete!")

                except ValueError as e:
                    console.print(f"[red]Error: {str(e)}")
                    continue
                except Exception as e:
                    console.print(f"[red]Error processing request: {str(e)}")
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