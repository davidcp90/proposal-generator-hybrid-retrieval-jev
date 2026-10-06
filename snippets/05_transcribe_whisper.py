import json, torch, whisper

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
whisper_model = None

def transcribe(path):
    """Returns [{start, end, text}] using local Whisper."""
    global whisper_model
    if whisper_model is None:
        whisper_model = whisper.load_model("turbo" if DEVICE == "cuda" else "base", device=DEVICE)
    r = whisper_model.transcribe(path, language="es", fp16=(DEVICE == "cuda"))   # the call is in Spanish
    return [{"start": s["start"], "end": s["end"], "text": s["text"].strip()} for s in r["segments"]]

if FILE.endswith(".json"):                        # fallback without audio
    segments = json.load(open(FILE))
else:
    segments = transcribe(FILE)
    json.dump(segments, open("transcript.json", "w"), ensure_ascii=False, indent=1)

print(DEVICE, len(segments), "segments")
for s in segments[:5]:
    print(f"[{s['start']:6.1f}s] {s['text']}")
