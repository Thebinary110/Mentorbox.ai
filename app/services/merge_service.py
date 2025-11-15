from pathlib import Path
import json


class MergeService:
    """
    Merge VAD micro-chunks into larger segments (10–20 seconds).
    """

    def __init__(self, min_gap_ms=1500, max_chunk_ms=20000):
        self.min_gap = min_gap_ms
        self.max_chunk = max_chunk_ms

    def merge_timestamps(self, timestamps: list):
        if not timestamps:
            return []

        merged = []
        cur = timestamps[0].copy()

        for ts in timestamps[1:]:
            gap = ts["start"] - cur["end"]
            chunk_len = cur["end"] - cur["start"]

            if gap < self.min_gap or chunk_len < self.max_chunk:
                # merge
                cur["end"] = ts["end"]
            else:
                # start a new chunk
                merged.append(cur)
                cur = ts.copy()

        merged.append(cur)
        return merged

    def save(self, video_id, merged):
        out_path = Path("data") / video_id / "merged_timestamps.json"
        json.dump(merged, open(out_path, "w"), indent=2)
        return out_path
