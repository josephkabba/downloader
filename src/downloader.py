from concurrent.futures import ThreadPoolExecutor
import os
from datetime import datetime
import yt_dlp
from typing import List, Optional
from dataclasses import dataclass
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
import glob

console = Console()

@dataclass
class Media:
    id: str
    title: str
    duration: str
    is_from_metadata: bool = False
    playlist_name: Optional[str] = None

    def to_save_format(self) -> str:
        return f"{self.id}###{self.duration}###{self.title}###{self.title}"

    @classmethod
    def from_save_format(cls, line: str) -> 'Media':
        data = line.strip().split("###")
        return cls(
            id=data[0],
            duration=data[1],
            title=data[3],
            is_from_metadata=False
        )

class YouTubeDownloader:
    
    def __init__(self, output_dir: str = "output", max_workers: int = 4):
        self.output_dir = output_dir
        self.max_workers = max_workers
        self._ensure_directories()

    def _ensure_directories(self):
        """Create necessary directories if they don't exist"""
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(os.path.join(self.output_dir, "playlist"), exist_ok=True)
        os.makedirs(os.path.join(self.output_dir, "video"), exist_ok=True)
        os.makedirs(os.path.join(self.output_dir, "audio"), exist_ok=True)

    def _get_output_path(self, media: Media, is_playlist: bool, is_audio_output: bool) -> str:
        """Generate appropriate output path based on media type and context"""
        # Determine the media type directory
        media_type = "audio" if is_audio_output else "video"
        
        if is_playlist:
            # For playlists, use playlist name or timestamp
            playlist_name = media.playlist_name or datetime.now().strftime("%Y%m%d_%H%M%S")
            return os.path.join(self.output_dir, "playlist", playlist_name, media_type)
        else:
            # For single files, use direct media type directory
            return os.path.join(self.output_dir, media_type)

    def _clean_temp_files(self, output_path: str, base_filename: str):
        """Clean up temporary and duplicate video files"""
        # Remove temporary .part files
        for part_file in glob.glob(os.path.join(output_path, "*.part")):
            try:
                os.remove(part_file)
            except Exception:
                pass

        # Remove duplicate video files with codes
        pattern = os.path.join(output_path, f"{base_filename}.*[.][fF][0-9]*.*")
        for dup_file in glob.glob(pattern):
            try:
                os.remove(dup_file)
            except Exception:
                pass
                
        # Clean up web audio formats
        web_audio_patterns = [
            "*.m4a",
            "*.webm",
            "*.ogg",
            "*.opus",
            "*.weba",
            "*.wav"
        ]
        
        for pattern in web_audio_patterns:
            for audio_file in glob.glob(os.path.join(output_path, pattern)):
                try:
                    os.remove(audio_file)
                except Exception:
                    pass
    
    def _get_ydl_opts(self, 
                     media: Media, 
                     is_playlist: bool,
                     download_video: bool = False, 
                     keep_video: bool = True,
                     convert_to_audio: bool = False,
                     bitrate: str = '192') -> dict:
        """Configure yt-dlp options based on download preferences"""
        # Determine if final output will be audio
        is_audio_output = convert_to_audio or not download_video
        
        # Get appropriate output path
        output_path = self._get_output_path(media, is_playlist, is_audio_output)
        os.makedirs(output_path, exist_ok=True)

        opts = {
            'format': 'bestaudio/best' if is_audio_output else 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'keepvideo': keep_video,
            'quiet': True,
            'no_warnings': True,
            'writethumbnail': True,
            'postprocessors': []
        }

        # Add audio conversion if needed
        if is_audio_output:
            opts['format'] = 'bestaudio/best'
            opts['postprocessors'] = [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': bitrate,
                },
                {
                    'key': 'FFmpegMetadata',
                    'add_metadata': True,
                },
                {
                    'key': 'EmbedThumbnail',
                    'already_have_thumbnail': False
                },
            ]
            # Set additional FFmpeg options
            opts['postprocessor_args'] = [
                '-id3v2_version', '3',
                '-metadata', 'title=%(title)s',
            ]
            # Additional options for better audio handling
            opts['extract_audio'] = True
            opts['audio_format'] = 'mp3'
            opts['audio_quality'] = bitrate
            
        return opts

    def download_media(self, 
                      media: Media,
                      progress: Optional[Progress] = None,
                      is_playlist: bool = False,
                      download_video: bool = False,
                      keep_video: bool = True,
                      convert_to_audio: bool = False,
                      bitrate: str = '192') -> bool:
        """Download a single media file"""
        try:
            task_id = progress.add_task(f"[cyan]Downloading {media.title}...", total=None) if progress else None
            
            opts = self._get_ydl_opts(
                media,
                is_playlist,
                download_video,
                keep_video,
                convert_to_audio,
                bitrate
            )
            
            with yt_dlp.YoutubeDL(opts) as ydl:
                url = f"http://www.youtube.com/watch?v={media.id}"
                ydl.download([url])
            
            # Clean up temporary and duplicate files
            if download_video:
                video_path = self._get_output_path(media, is_playlist, "video")
                self._clean_temp_files(video_path, media.title)
            if convert_to_audio or not download_video:
                audio_path = self._get_output_path(media, is_playlist, "audio")
                self._clean_temp_files(audio_path, media.title)
                
            console.print(f"[green]Successfully downloaded: {media.title}")
            
            if progress:
                progress.remove_task(task_id)
            return True

        except Exception as e:
            console.print(f"[red]Error downloading {media.title}: {str(e)}")
            if progress:
                progress.remove_task(task_id)
            return False

    def download_playlist(self, 
                         media_list: List[Media],
                         download_video: bool = False,
                         keep_video: bool = True,
                         convert_to_audio: bool = False,
                         bitrate: str = '192'):
        """Download multiple media files using thread pool"""
        total_items = len(media_list)
        success_count = 0
        failed_count = 0

        console.print(f"[cyan]Starting download of {total_items} items...")

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = [
                    executor.submit(
                        self.download_media,
                        media,
                        progress,
                        True,
                        download_video,
                        keep_video,
                        convert_to_audio,
                        bitrate
                    )
                    for media in media_list
                ]
                for future in futures:
                    if future.result():
                        success_count += 1
                    else:
                        failed_count += 1

        # Print summary
        console.print(f"\n[green]Download Summary:")
        console.print(f"[green]Successfully downloaded: {success_count} items")
        if failed_count > 0:
            console.print(f"[yellow]Failed downloads: {failed_count} items")