import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"

sys.path.append(str(ROOT))

from app.services.audio_normalizer import AudioNormalizer

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", required=True)
    args = parser.parse_args()

    normalizer = AudioNormalizer(base_data_dir=str(DATA_DIR))

    print("\n==========================")
    print("     AUDIO NORMALIZER")
    print("==========================\n")

    try:
        out = normalizer.normalize(args.id)
        print("Normalization complete!")
        print("Output file:", out)
    except Exception as e:
        print("\n❌ ERROR:", e)
