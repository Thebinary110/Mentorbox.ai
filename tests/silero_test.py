import torch

print("Loading Silero VAD model...")
result = torch.hub.load(
    repo_or_dir="snakers4/silero-vad",
    model="silero_vad",
    trust_repo=True
)

print("\n=== RETURNED OBJECT ===")
print(result)
print("\nType:", type(result))
print("Length (if tuple):", len(result) if isinstance(result, tuple) else "N/A")

# If tuple, print each element type
if isinstance(result, tuple):
    for i, r in enumerate(result):
        print(f" [{i}] Type: {type(r)}")
