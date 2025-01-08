import yt_dlp
from typing import List, Optional, Tuple
import re
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Confirm
from urllib.parse import urlparse, parse_qs
from downloader import Media

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

def extract_playlist_id(url: str) -> Optional[str]:
    """Extract playlist ID from various playlist URL formats"""
    # First try to get the list parameter
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    playlist_id = query_params.get('list', [None])[0]
    
    if not playlist_id:
        return None

    # Handle different playlist types
    if playlist_id.startswith(('RD', 'UU', 'PL', 'LL', 'FL', 'WL')):
        return playlist_id
    
    # For standard playlists without prefix
    if re.match(r'^[A-Za-z0-9_-]+$', playlist_id):
        return f"PL{playlist_id}"
        
    return playlist_id

def is_likely_music(video_info: dict) -> bool:
    """
    Determine if a video is likely to be music based on various factors
    """
    # Get the necessary information
    title = video_info.get('title', '').lower()
    description = video_info.get('description', '').lower()
    categories = video_info.get('categories', [])
    tags = [tag.lower() for tag in video_info.get('tags', [])]
    
    # Music-related keywords
    music_keywords = {
        'official music video', 'official video', 'official audio',
        'lyrics', 'music video', 'ft.', 'feat.', 'remix',
        'official lyric video', 'audio', 'album', 'single'
    }
    
    # Check various indicators
    indicators = [
        'Music' in categories,  # YouTube category
        any(keyword in title for keyword in music_keywords),
        any(keyword in description.split()[:50] for keyword in music_keywords),  # Check first 50 words
        any('music' in tag or 'song' in tag for tag in tags),
        bool(re.search(r'(\d{4}|\d{2})', title))  # Year in title
    ]
    
    # If at least 2 indicators are True, it's likely music
    return sum(indicators) >= 2


def extract_video_id(url: str) -> Optional[str]:
    """Extract video ID from various YouTube URL formats"""
    patterns = [
        # Standard watch URL
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        # Shortened youtu.be URL
        r'youtu\.be/([0-9A-Za-z_-]{11})',
        # Embed URL
        r'embed/([0-9A-Za-z_-]{11})',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def validate_url(url: str) -> Tuple[Optional[str], Optional[str], bool, str]:
    """
    Validate and parse YouTube URL
    Returns: (video_id, playlist_id, is_mix, error_message)
    """
    try:
        parsed_url = urlparse(url)
        
        # Check if it's a YouTube URL
        if 'youtube.com' not in parsed_url.netloc and 'youtu.be' not in parsed_url.netloc:
            return None, None, False, "Not a valid YouTube URL"

        # Extract IDs
        video_id = extract_video_id(url)
        playlist_id = extract_playlist_id(url)
        is_mix = bool(playlist_id and playlist_id.startswith('RD'))

        # Validate we got at least one ID
        if not video_id and not playlist_id:
            return None, None, False, "No video or playlist ID found in URL"

        return video_id, playlist_id, is_mix, ""

    except Exception as e:
        return None, None, False, f"Error parsing URL: {str(e)}"

def get_single_video_info(url: str) -> Optional[Media]:
    """Extract information for a single video"""
    try:
        # First validate the URL
        video_id, _, _, error = validate_url(url)
        if error:
            raise ValueError(error)
        if not video_id:
            raise ValueError("No video ID found in URL")

        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'ignoreerrors': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            video_info = ydl.extract_info(
                f"https://www.youtube.com/watch?v={video_id}", 
                download=False
            )
            
            if not video_info:
                raise ValueError("Could not fetch video information")

            title = clean_title(video_info.get('title', ''))
            return Media(
                id=video_info['id'],
                title=sanitize_filename(title),
                duration=str(video_info.get('duration', '0')),
                is_from_metadata=False
            )

    except Exception as e:
        console.print(f"[red]Error processing video: {str(e)}[/red]")
        return None

def get_playlist_media(url: str, 
                      playlist_name: Optional[str] = None,
                      reverse: bool = False, 
                      limit: Optional[int] = None,
                      songs_only: bool = False) -> List[Media]:
    """Extract media items from YouTube playlist"""
    try:
        # Special handling for Mix playlists
        if 'RD' in url:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': 'in_playlist',
                'ignoreerrors': True,
                'format': 'best'
            }
        else:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': True,
                'ignoreerrors': True
            }

        media_items = []
        failed_count = 0
        skipped_count = 0  # Add counter for skipped non-music content

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            playlist_info = ydl.extract_info(url, download=False)
            
            if not playlist_info:
                console.print("[red]Could not fetch playlist information[/red]")
                return []

            # Use playlist title if no custom name provided
            if not playlist_name:
                playlist_name = sanitize_filename(playlist_info.get('title', ''))

            entries = playlist_info.get('entries', [])
            valid_entries = [e for e in entries if e is not None]
            
            if reverse:
                valid_entries = valid_entries[::-1]
            
            if limit:
                valid_entries = valid_entries[:limit]
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task("[cyan]Processing videos...", total=len(valid_entries))

                for entry in valid_entries:
                    try:
                        if isinstance(entry, dict) and entry.get('url'):
                            video_url = entry['url']
                        else:
                            video_url = f"https://www.youtube.com/watch?v={entry['id']}"
                            
                        video_info = ydl.extract_info(video_url, download=False)
                        
                        if video_info:
                            # Check if we're filtering for songs only
                            if songs_only:
                                if not is_likely_music(video_info):
                                    console.print(f"[yellow]Skipping non-music content: {video_info.get('title', '')}")
                                    skipped_count += 1
                                    progress.advance(task)
                                    continue

                            title = clean_title(video_info.get('title', ''))
                            media = Media(
                                id=video_info['id'],
                                title=sanitize_filename(title),
                                duration=str(video_info.get('duration', '0')),
                                is_from_metadata=False,
                                playlist_name=playlist_name
                            )
                            media_items.append(media)
                            console.print(f"[green]Processed: {title}")
                        else:
                            failed_count += 1
                    except Exception as e:
                        failed_count += 1
                        console.print(f"[yellow]Warning: Could not process video {entry.get('id', 'unknown')}: {str(e)}[/yellow]")
                    finally:
                        progress.advance(task)

        console.print(f"[green]Successfully processed {len(media_items)} items")
        if skipped_count > 0:
            console.print(f"[yellow]Skipped {skipped_count} non-music items")
        if failed_count > 0:
            console.print(f"[yellow]Failed to process {failed_count} items")

        return media_items

    except Exception as e:
        console.print(f"[red]Error processing playlist: {str(e)}[/red]")
        return []

def process_url(url: str) -> Tuple[str, bool]:
    """
    Process YouTube URL and determine its type
    Returns: (processed_url, is_playlist)
    """
    try:
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        
        video_id = query_params.get('v', [None])[0]
        if not video_id and 'youtu.be' in parsed_url.netloc:
            video_id = parsed_url.path.lstrip('/')
            
        playlist_id = extract_playlist_id(url)
        
        # Check if it's a Mix playlist
        is_mix = bool(playlist_id and playlist_id.startswith(('RD', 'RDMM', 'RDQM')))
        
        # For Mix playlists, we need to use the video URL as the base for the mix
        if is_mix and video_id:
            return f"https://www.youtube.com/watch?v={video_id}&list={playlist_id}", True
            
        # For regular playlists
        if playlist_id:
            if video_id:
                message = "\n[yellow]This URL contains both a video and a playlist. "
                message += "\nWould you like to download the entire playlist?[/yellow]"
                
                download_playlist = Confirm.ask(message)
                if download_playlist:
                    return f"https://www.youtube.com/playlist?list={playlist_id}", True
                return f"https://www.youtube.com/watch?v={video_id}", False
            return f"https://www.youtube.com/playlist?list={playlist_id}", True

        # For single video
        if video_id:
            return f"https://www.youtube.com/watch?v={video_id}", False

        raise ValueError("Could not process URL")
        
    except Exception as e:
        raise ValueError(f"Error processing URL: {str(e)}")