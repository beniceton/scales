#!/usr/bin/env python3
"""
Generate any missing clips with ElevenLabs. Reads src/script.json, writes clips/<voice_id>/<id>.mp3.
Needs ELEVENLABS_API_KEY in the environment. Never regenerates a clip that already exists.
"""
import json, os, sys, time, urllib.request, urllib.error
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
from voicelines import all_lines, line_id

key = os.environ.get("ELEVENLABS_API_KEY")
script = json.load(open(os.path.join(ROOT, "src/script.json"), encoding="utf-8"))
lines = all_lines(script)

def tts(text, voice_id):
    body = json.dumps({"text": text, "model_id": "eleven_multilingual_v2",
                       "voice_settings": {"stability": 0.65, "similarity_boost": 0.8, "style": 0.15, "use_speaker_boost": True}}).encode()
    req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}?output_format=mp3_44100_64", data=body,
                                 headers={"xi-api-key": key, "Content-Type": "application/json", "Accept": "audio/mpeg"}, method="POST")
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=120) as r: return r.read()
        except urllib.error.HTTPError as e:
            msg = e.read().decode(errors="replace")[:300]
            if e.code in (429, 500, 502, 503, 504) and attempt < 3: time.sleep(2 ** attempt); continue
            raise SystemExit(f"ElevenLabs HTTP {e.code}: {msg}")

todo = []
for n in script["narrators"]:
    d = os.path.join(ROOT, "clips", n["voice_id"]); os.makedirs(d, exist_ok=True)
    for text in lines:
        p = os.path.join(d, line_id(text) + ".mp3")
        if not os.path.exists(p) or os.path.getsize(p) < 1000: todo.append((n, text, p))
print(f"{len(todo)} clips to generate across {len(script['narrators'])} narrators")
if todo and not key: raise SystemExit("ELEVENLABS_API_KEY is not set")
for i, (n, text, p) in enumerate(todo, 1):
    print(f"[{i}/{len(todo)}] {n['name']}: {text[:60]}")
    audio = tts(text, n["voice_id"])
    if len(audio) < 1000: raise SystemExit("Empty audio returned; stopping.")
    with open(p + ".tmp", "wb") as f: f.write(audio)
    os.replace(p + ".tmp", p); time.sleep(0.2)
print("done")
