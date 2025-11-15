import argparse
import json
from pathlib import Path
import sys
import torch

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from app.services.vad_service import VADService

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", required=True, help="YouTube video ID")
    parser.add_argument("--threshold", type=float, default=0.5)
    args = parser.parse_args()

    video_id = args.id
    base_dir = Path("data") / video_id
    wav_path = base_dir / f"{video_id}_normalized.wav"

    print(f"\nUsing audio: {wav_path}")

    if not wav_path.exists():
        print("❌ ERROR: Normalized WAV not found! Run normalize step.")
        exit()

    # Load VAD
    print("🔄 Loading Silero VAD model...")

    vad = VADService(device="cpu", threshold=args.threshold)

    # Read audio
    wav = vad.read_audio(str(wav_path))

    print("🔍 Running VAD... (speech detection)")
    timestamps = vad.get_speech_timestamps(
        wav,
        vad.model,
        sampling_rate=16000
    )

    print(f"🔹 Speech segments detected: {len(timestamps)}")

    # Save timestamps
    out_file = base_dir / "vad_timestamps.json"
    json.dump(timestamps, open(out_file, "w"), indent=2)

    print(f"\n💾 Saved VAD timestamps → {out_file}\n")
    print("🎉 VAD COMPLETED SUCCESSFULLY")
