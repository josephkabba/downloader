from concurrent.futures import ThreadPoolExecutor
import os
import yt_dlp
from typing import List, Optional
from dataclasses import dataclass
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

@dataclass
class Song:
    id: str
    title: str
    duration: str
    is_from_metadata: bool = False

    def to_save_format(self) -> str:
        return f"{self.id}###{self.duration}###{self.title}###{self.title}"

    @classmethod
    def from_save_format(cls, line: str) -> 'Song':
        data = line.strip().split("###")
        return cls(
            id=data[0],
            duration=data[1],
            title=data[3],
            is_from_metadata=False
        )

class YouTubeDownloader:
    def __init__(self, output_dir: str = "../work/music/", max_workers: int = 4):
        self.output_dir = output_dir
        self.max_workers = max_workers
        self._ensure_directories()

    def _ensure_directories(self):
        """Create necessary directories if they don't exist"""
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(os.path.join(self.output_dir, "output"), exist_ok=True)

    def _get_ydl_opts(self) -> dict:
        return {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'retries': 10,
            'ignoreerrors': True,
            'ffmpeg-location': './ffmpeg/bin/',  # Updated ffmpeg location
            'outtmpl': os.path.join(self.output_dir, "%(id)s.%(ext)s"),
            'keepvideo': False,
            'quiet': True,
            'no_warnings': True,
            'extract_flat': 'in_playlist',
            'concurrent_fragments': 4  # Enable parallel fragment downloads
        }

    def download_audio(self, song: Song, progress: Optional[Progress] = None) -> bool:
        """Download a single audio file"""
        try:
            task_id = progress.add_task(f"[cyan]Downloading {song.title}...", total=None) if progress else None
            
            with yt_dlp.YoutubeDL(self._get_ydl_opts()) as ydl:
                url = f"http://www.youtube.com/watch?v={song.id}"
                ydl.download([url])

            # Move file to output directory
            old_path = os.path.join(self.output_dir, f"{song.id}.mp3")
            new_path = os.path.join(self.output_dir, "output", f"{song.title}.mp3")
            
            # Check if the file exists before trying to move it
            if os.path.exists(old_path):
                # If destination file already exists, remove it
                if os.path.exists(new_path):
                    os.remove(new_path)
                os.rename(old_path, new_path)
                console.print(f"[green]Successfully downloaded: {song.title}")
            else:
                console.print(f"[yellow]Warning: Download completed but file not found: {song.title}")
                if progress:
                    progress.remove_task(task_id)
                return False

            if progress:
                progress.remove_task(task_id)
            return True

        except Exception as e:
            console.print(f"[red]Error downloading {song.title}: {str(e)}")
            if progress:
                progress.remove_task(task_id)
            return False

    def download_playlist(self, songs: List[Song]):
        """Download multiple songs using thread pool"""
        total_songs = len(songs)
        success_count = 0
        failed_count = 0

        console.print(f"[cyan]Starting download of {total_songs} songs...")

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = [
                    executor.submit(self.download_audio, song, progress)
                    for song in songs
                ]
                for future in futures:
                    if future.result():
                        success_count += 1
                    else:
                        failed_count += 1

        # Print summary
        console.print(f"\n[green]Download Summary:")
        console.print(f"[green]Successfully downloaded: {success_count} songs")
        if failed_count > 0:
            console.print(f"[yellow]Failed downloads: {failed_count} songs")