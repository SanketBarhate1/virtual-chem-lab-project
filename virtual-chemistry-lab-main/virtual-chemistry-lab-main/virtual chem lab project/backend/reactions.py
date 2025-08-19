import json, os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHEMS_FILE = os.path.join(BASE_DIR, "chemicals.json")

# Load reactions from chemicals.json so you keep a single source of truth
with open(CHEMS_FILE, "r", encoding="utf-8") as f:
    _DATA = json.load(f)

_REACTIONS = _DATA.get("reactions", {})

def _lookup(a, b):
    return _REACTIONS.get(f"{a}+{b}") or _REACTIONS.get(f"{b}+{a}")

def find_reaction(a, b):
    r = _lookup(a, b)
    if r:
        return r
    # default fallback for unknown pairs (strong defaults)
    return {
        "reaction": "No visible reaction",
        "description": "No noticeable change observed.",
        "safety": "No special hazard noted for dilute mixture.",
        "color": "rgba(200,220,255,0.30)",
        "animation": "fizz-soft"
    }
