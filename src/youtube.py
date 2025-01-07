from pytube import Playlist
from typing import List
import re
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from downloader import Song

console = Console()

def sanitize_filename(filename: str) -> str:
    """Remove invalid characters from filename"""
    return re.sub(r'[<>:"/\\|?*]', '', filename)

def get_playlist_songs(url: str) -> List[Song]:
    """Extract songs from YouTube playlist"""
    try:
        console.print("[cyan]Fetching playlist information...")
        playlist = Playlist(url)
        songs = []

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("[cyan]Processing videos...", total=len(playlist.videos))

            for video in playlist.videos:
                try:
                    meta = video.metadata
                    if meta and meta[0].get("Song"):
                        song = Song(
                            id=video.video_id,
                            duration=str(video.length),
                            title=sanitize_filename(meta[0]["Song"]),
                            is_from_metadata=True
                        )
                        songs.append(song)
                    progress.advance(task)
                except Exception as e:
                    console.print(f"[yellow]Warning: Could not process video {video.video_id}: {str(e)}")
                    progress.advance(task)

        return songs
    except Exception as e:
        console.print(f"[red]Error processing playlist: {str(e)}")
        return []