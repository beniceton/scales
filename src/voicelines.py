"""Shared between build.py and generate.py: which lines exist, and the id used for each clip."""
def all_lines(script):
    out = [c["text"] for c in script["breath"]] + [script["intro"], script["timed_release_lead"]] + list(script["release"])
    out += [script["end_breath"], script["end_scales"]]
    out += [p + "." for p in script.get("sensations", []) + script.get("places", []) + script.get("perceptions", [])]
    for e in script.get("exercises", {}).values(): out += list(e["lines"])
    return out

def line_id(text):
    h = 5381
    for ch in text:
        h = ((h * 33) ^ ord(ch)) & 0xFFFFFFFF
    return format(h, "08x")
