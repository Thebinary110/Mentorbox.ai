import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from app.services.vad_service import VADService


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", required=True)
    parser.add_argument("--threshold", type=float, default=0.5)
    args = parser.parse_args()

    audio_path = f"{ROOT}/data/{args.id}/{args.id}_normalized.wav"

    print("Using audio:", audio_path)

    vad = VADService(device="cpu", threshold=args.threshold)

    timestamps = vad.run(audio_path)

    print("\n=== SPEECH SEGMENTS ===")
    print(timestamps)
