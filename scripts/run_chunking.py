import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from app.services.chunk_service import ChunkService

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", required=True, help="YouTube Video ID")
    args = parser.parse_args()

    video_id = args.id
    video_dir = Path("data") / video_id

    # Use merged timestamps instead of raw VAD timestamps
    merged_path = video_dir / "merged_timestamps.json"

    print("\n=============================")
    print("      AUDIO CHUNKING")
    print("=============================\n")

    if not merged_path.exists():
        print("❌ ERROR: Merged timestamp file not found!")
        print("Run: python scripts/run_merge.py --id", video_id)
        exit()

    timestamps = json.load(open(merged_path, "r"))

    chunker = ChunkService()
    try:
        chunks = chunker.chunk_audio(video_id, timestamps)
        print("\n🎉 Chunking completed successfully!")
        print("Example chunk:", chunks[0])
    except Exception as e:
        print("\n❌ ERROR:", e)
