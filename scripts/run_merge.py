import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from app.services.merge_service import MergeService


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", required=True)
    parser.add_argument("--gap", type=int, default=1500)
    parser.add_argument("--max", type=int, default=20000)
    args = parser.parse_args()

    video_id = args.id
    base_dir = Path("data") / video_id

    vad_file = base_dir / "vad_timestamps.json"
    if not vad_file.exists():
        print("❌ ERROR: Run VAD first.")
        exit()

    timestamps = json.load(open(vad_file))

    print(f"\n🔄 Merging timestamps for {video_id} ...")

    merger = MergeService(args.gap, args.max)
    merged = merger.merge_timestamps(timestamps)

    out_path = merger.save(video_id, merged)

    print(f"📌 Original chunks: {len(timestamps)}")
    print(f"📌 Merged chunks  : {len(merged)}")
    print(f"💾 Saved → {out_path}\n")
    print("🎉 Merging complete!")
