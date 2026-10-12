#!/usr/bin/env python3
"""
Build index.html from src/script.json, src/template.html and the clip cache in clips/<voice_id>/.
Run by the GitHub Action after voices have been generated; can also be run locally:  python3 src/build.py
"""
import base64, datetime, io, json, os, struct, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
from voicelines import all_lines, line_id

script = json.load(open(os.path.join(ROOT, "src/script.json"), encoding="utf-8"))

def mp3_duration(raw):
    try:
        from mutagen.mp3 import MP3
        return round(MP3(io.BytesIO(raw)).info.length, 1)
    except Exception:
        return None

# ---- voice packs from the clip cache ----
packs = []
for n in script["narrators"]:
    d = os.path.join(ROOT, "clips", n["voice_id"])
    clips, durs = {}, {}
    for text in all_lines(script):
        cid = line_id(text); p = os.path.join(d, cid + ".mp3")
        if os.path.exists(p) and os.path.getsize(p) > 1000:
            raw = open(p, "rb").read(); clips[cid] = base64.b64encode(raw).decode()
            dur = mp3_duration(raw)
            if dur: durs[cid] = dur
    packs.append({"voice": n["name"], "provider": "elevenlabs", "dur": durs, "clips": clips})
    print(f"{n['name']}: {len(clips)}/{len(all_lines(script))} clips")
# default narrator first
packs.sort(key=lambda p: 0 if any(n["name"] == p["voice"] and n.get("default") for n in script["narrators"]) else 1)

# ---- texts block the app reads ----
texts = {
    "all": all_lines(script),
    "breath": [[c["t"], c["text"]] for c in script["breath"]],
    "intro": script["intro"],
    "scaleCues": [[0, ""], [0, ""], [0, ""], [0, script["timed_release_lead"]]] + [[0, x] for x in script["release"]],
    "numbers": [],
    "endBreath": script["end_breath"], "endScales": script["end_scales"],
    "sample": (script.get("sensations") or script.get("perceptions"))[0] + ".",
    "perceptions": script.get("sensations", []) + script.get("places", []) + script.get("perceptions", []),
    "decks": {"sensations": script.get("sensations", []), "places": script.get("places", [])},
    "exercises": script.get("exercises", {}),
}
n = 400; data = bytes([128]) * n
wav = b"RIFF" + struct.pack("<I", 36 + n) + b"WAVEfmt " + struct.pack("<IHHIIHH", 16, 1, 1, 8000, 8000, 1, 8) + b"data" + struct.pack("<I", n) + data
silent = "data:audio/wav;base64," + base64.b64encode(wav).decode()
stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d-%H%M")

html = open(os.path.join(ROOT, "src/template.html"), encoding="utf-8").read()
html = (html.replace("__VERSION__", stamp)
            .replace("__PACKS__", json.dumps(packs).replace("</", "<\\/"))
            .replace("__TEXTS__", json.dumps(texts, ensure_ascii=False).replace("</", "<\\/"))
            .replace("__SILENT__", silent))
open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(html)
print(f"index.html written, build {stamp}, {os.path.getsize(os.path.join(ROOT, 'index.html'))/1e6:.1f} MB")
