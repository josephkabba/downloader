import yt_dlp
from typing import List
import re
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from urllib.parse import urlparse, parse_qs
from downloader import Song

console = Console()

def sanitize_filename(filename: str) -> str:
    """Remove invalid characters from filename"""
    # Remove or replace invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Remove leading/trailing spaces and dots
    filename = filename.strip('. ')
    return filename

def clean_title(title: str) -> str:
    """Clean up video title by removing common patterns"""
    patterns = [
        r'\(Official Video\)',
        r'\(Official Music Video\)',
        r'\[Official Video\]',
        r'\[Official Music Video\]',
        r'\(Lyrics\)',
        r'\[Lyrics\]',
        r'\(Audio\)',
        r'\[Audio\]',
        r'\(Official Audio\)',
        r'\[Official Audio\]',
        r'Official Video',
        r'Official Music Video',
        r'Music Video',
        r'HD',
        r'HQ',
        r'4K',
        r'\d{4}',  # Year
        r'\(\d+\)', # Year in parentheses
        r'\[\d+\]'  # Year in brackets
    ]
    
    for pattern in patterns:
        title = re.sub(pattern, '', title, flags=re.IGNORECASE)
    
    return title.strip()

def get_playlist_id(url: str) -> str:
    """Extract playlist ID from URL"""
    parsed_url = urlparse(url)
    if 'youtube.com' not in parsed_url.netloc:
        raise ValueError("Not a valid YouTube URL")
    
    query_params = parse_qs(parsed_url.query)
    playlist_id = query_params.get('list', [None])[0]
    
    if not playlist_id:
        raise ValueError("No playlist ID found in URL")
    
    return playlist_id

def get_playlist_songs(url: str, reverse: bool = False) -> List[Song]:
    """Extract songs from YouTube playlist"""
    try:
        console.print("[cyan]Fetching playlist information...")
        
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,
            'ignoreerrors': True   
        }

        songs = []
        failed_count = 0

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            playlist_info = ydl.extract_info(url, download=False)
            
            if not playlist_info:
                console.print("[red]Could not fetch playlist information[/red]")
                return []

            entries = playlist_info.get('entries', [])
            valid_entries = [e for e in entries if e is not None]
            
            # Apply reverse if requested
            if reverse:
                valid_entries = valid_entries[::-1]
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task("[cyan]Processing videos...", total=len(valid_entries))

                for entry in valid_entries:
                    try:
                        video_info = ydl.extract_info(
                            f"https://www.youtube.com/watch?v={entry['id']}", 
                            download=False
                        )
                        
                        if video_info:
                            title = clean_title(video_info.get('title', ''))
                            song = Song(
                                id=video_info['id'],
                                title=sanitize_filename(title),
                                duration=str(video_info.get('duration', '0')),
                                is_from_metadata=False
                            )
                            songs.append(song)
                            console.print(f"[green]Processed: {title}")
                        else:
                            failed_count += 1
                    except Exception as e:
                        failed_count += 1
                        console.print(f"[yellow]Warning: Could not process video {entry.get('id', 'unknown')}: {str(e)}[/yellow]")
                    finally:
                        progress.advance(task)

        console.print(f"[green]Successfully processed {len(songs)} songs")
        if failed_count > 0:
            console.print(f"[yellow]Failed to process {failed_count} videos")

        return songs
    except Exception as e:
        console.print(f"[red]Error processing playlist: {str(e)}[/red]")
        return []