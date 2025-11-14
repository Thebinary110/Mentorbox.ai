import json
import subprocess
from pathlib import Path
from datetime import datetime


class YouTubeAudioDownloader:
    """
    Ultra-stable YouTube audio downloader using yt-dlp (subprocess).
    """

    def __init__(self, base_data_dir: str = "rag_video_chat/data"):
        self.base_dir = Path(base_data_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def extract_video_id(self, url: str) -> str:
        from urllib.parse import urlparse, parse_qs
        parsed = urlparse(url)

        # youtu.be/<id>
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

        output_template = f"{video_dir}/{video_id}.%(ext)s"

        # Run yt-dlp using subprocess — this is 100% reliable
        cmd = [
            "yt-dlp",
            "-f", "bestaudio",
            "-o", output_template,
            url
        ]

        process = subprocess.run(cmd, capture_output=True, text=True)

        if process.returncode != 0:
            raise RuntimeError(
                f"yt-dlp failed:\n{process.stderr}"
            )

        # Find downloaded file
        audio_file = None
        for ext in ["m4a", "webm", "opus", "mp3"]:
            p = video_dir / f"{video_id}.{ext}"
            if p.exists():
                audio_file = str(p)
                break

        if not audio_file:
            raise RuntimeError("Audio file not found after yt-dlp download.")

        metadata = {
            "video_id": video_id,
            "audio_file": audio_file,
            "downloaded_at": datetime.utcnow().isoformat(),
        }

        with open(video_dir / "metadata.json", "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)

        return metadata
