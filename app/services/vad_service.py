import torch
import torchaudio


class VADService:
    def __init__(self, device="cpu", threshold=0.5):
        print("🔄 Loading Silero VAD model via torch.hub...")

        model, utils = torch.hub.load(
            repo_or_dir="snakers4/silero-vad",
            model="silero_vad",
            trust_repo=True
        )

        # utils is a tuple → unpack correctly
        (
            self.get_speech_timestamps,
            self.save_audio,
            self.read_audio,
            self.VADIterator,
            self.collect_chunks
        ) = utils

        self.model = model.to(device)
        self.device = device
        self.threshold = threshold

        print("✅ Silero VAD successfully loaded (2-value format detected)")

    def run(self, audio_path: str):
        print(f"🎵 Loading audio: {audio_path}")

        wav = self.read_audio(audio_path)
        wav = wav.to(self.device)

        print("🔍 Running VAD...")
        timestamps = self.get_speech_timestamps(
            wav,
            self.model,
            threshold=self.threshold
        )

        return timestamps
