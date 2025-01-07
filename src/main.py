from rich import _console
from rich.prompt import Prompt
from downloader import YouTubeDownloader
from youtube import get_playlist_songs

def display_help():
    _console.print("\n[green]Available commands:")
    _console.print("  [cyan]dl <playlist_url>[/cyan] - Download songs from a YouTube playlist")
    _console.print("  [cyan]help[/cyan] - Show this help message")
    _console.print("  [cyan]quit[/cyan] - Exit the program\n")

def main():
    _console.print("[bold green]YouTube Playlist Downloader[/bold green]")
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
                    _console.print("[red]Error: Please provide a playlist URL")
                    continue

                url = command[1]
                songs = get_playlist_songs(url)
                
                if not songs:
                    _console.print("[red]No songs found in playlist")
                    continue

                _console.print(f"[green]Found {len(songs)} songs in playlist")
                if Prompt.ask("Do you want to download them?", choices=["y", "n"]) == "y":
                    downloader.download_playlist(songs)
                    _console.print("[green]Download complete!")
            else:
                _console.print("[red]Invalid command. Type 'help' for available commands")

        except KeyboardInterrupt:
            _console.print("\n[yellow]Operation cancelled by user")
        except Exception as e:
            _console.print(f"[red]Error: {str(e)}")

if __name__ == "__main__":
    main()