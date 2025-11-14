import json
import subprocess
from pathlib import Path
from datetime import datetime


class YouTubeAudioDownloader:
    """
    Stable YouTube audio downloader using yt-dlp (subprocess).
    Stores audio in C:/MentorBoxData always.
    """

    def __init__(self, base_data_dir: str = r"C:\Users\Dell\Desktop\hackRx-1\MentorBox.ai\rag_video_chat\data"):
        self.base_dir = Path(base_data_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        print(f"[DEBUG] Base data directory: {self.base_dir}")

    def extract_video_id(self, url: str) -> str:
        from urllib.parse import urlparse, parse_qs
        parsed = urlparse(url)

        if parsed.hostname == "youtu.be":
            return parsed.path.lstrip("/")

        qs = parse_qs(parsed.query)
        if "v" in qs:
            return qs["v"][0]

        return Path(parsed.path).name

    def download_audio(self, url: str) -> dict:
        video_id = self.extract_video_id(url)

        video_dir = self.base_dir / video_id
        video_dir.mkdir(parents=True, exist_ok=True)
        print(f"[DEBUG] Video directory: {video_dir}")

        output_template = str(video_dir / f"{video_id}.%(ext)s")
        print(f"[DEBUG] Output template: {output_template}")

        cmd = [
            "yt-dlp",
            "-f", "bestaudio",
            "-o", output_template,
            url,
        ]

        print("[DEBUG] Running yt-dlp...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(f"[DEBUG] Return code: {result.returncode}")
        print(f"[DEBUG] STDOUT:\n{result.stdout}")
        print(f"[DEBUG] STDERR:\n{result.stderr}")

        if result.returncode != 0:
            raise RuntimeError(f"yt-dlp failed:\n{result.stderr}")

        audio_file = None
        for ext in ["webm", "m4a", "opus", "mp3"]:
            fpath = video_dir / f"{video_id}.{ext}"
            print(f"[DEBUG] Checking: {fpath}")
            if fpath.exists():
                audio_file = str(fpath)
                break

        if not audio_file:
            raise RuntimeError("Audio file not found after yt-dlp execution.")

        metadata = {
            "video_id": video_id,
            "audio_file": audio_file,
            "downloaded_at": datetime.utcnow().isoformat(),
        }

        with open(video_dir / "metadata.json", "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)

        return metadata
