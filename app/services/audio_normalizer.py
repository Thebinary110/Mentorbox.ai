import os
import subprocess
from pathlib import Path


class AudioNormalizer:
    def __init__(self, base_data_dir: str):
        self.data_dir = Path(base_data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

        print("DEBUG: Using data dir:", self.data_dir.resolve())

    def normalize(self, video_id: str) -> str:
        """Normalize YouTube audio → 16kHz mono WAV"""

        in_file = self.data_dir / video_id / f"{video_id}.webm"
        out_file = self.data_dir / video_id / f"{video_id}_normalized.wav"

        print("DEBUG: Input file:", in_file.resolve())
        print("DEBUG: Exists:", in_file.exists())

        if not in_file.exists():
            raise FileNotFoundError(f"Audio file not found: {in_file}")

        ffmpeg_bin = r"C:\Users\Dell\Downloads\ffmpeg-2025-11-12-git-6cdd2cbe32-full_build\bin\ffmpeg.exe"  # ffmpeg is working globally on your machine

        cmd = [
            ffmpeg_bin,
            "-y",
            "-i", str(in_file),
            "-ar", "16000",   # resample to 16kHz
            "-ac", "1",       # mono
            str(out_file)
        ]

        print("DEBUG: Running command:", " ".join(cmd))

        subprocess.run(cmd, check=True)

        print("DEBUG: Output file created:", out_file.resolve())

        return str(out_file)
