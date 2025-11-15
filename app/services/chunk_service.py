import os
import soundfile as sf
from pathlib import Path
import numpy as np


class ChunkService:
    """
    Splits normalized audio using VAD timestamps into separate chunks.
    """

    def __init__(self, base_data_dir="data"):
        self.data_dir = Path(base_data_dir)

    def chunk_audio(self, video_id: str, timestamps: list):
        video_dir = self.data_dir / video_id
        in_file = video_dir / f"{video_id}_normalized.wav"
        chunks_dir = video_dir / "chunks"

        if not in_file.exists():
            raise FileNotFoundError(f"Normalized file not found: {in_file}")

        chunks_dir.mkdir(exist_ok=True)

        print(f"\n🔊 Loading normalized audio: {in_file}")
        audio, sr = sf.read(str(in_file))

        created_chunks = []

        for idx, ts in enumerate(timestamps):
            start = int(ts["start"])
            end = int(ts["end"])

            # Extract chunk
            chunk_audio = audio[start:end]

            chunk_path = chunks_dir / f"chunk_{idx:04d}.wav"
            sf.write(chunk_path, chunk_audio, sr)

            created_chunks.append(str(chunk_path))

        print(f"\n✅ Total chunks created: {len(created_chunks)}")
        return created_chunks
