import argparse
import sys
from pathlib import Path

# Add project root to PYTHONPATH
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from app.services.downloader_service import YouTubeAudioDownloader


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True, help="YouTube video URL")
    args = parser.parse_args()

    downloader = YouTubeAudioDownloader()

    print("\n======================================")
    print("     DOWNLOADING AUDIO VIA YT-DLP     ")
    print("======================================\n")

    try:
        meta = downloader.download_audio(args.url)

        print("\n=== DOWNLOAD COMPLETE ===")
        print("Video ID:", meta["video_id"])
        print("Audio File:", meta["audio_file"])
        print("Metadata saved successfully!\n")

    except Exception as e:
        print("\n❌ ERROR OCCURRED")
        print(str(e))
        sys.exit(1)
