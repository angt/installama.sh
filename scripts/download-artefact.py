import json
import urllib.request
from pathlib import Path

with open("artefacts.json", "r", encoding="utf-8") as f:
    artefacts = json.load(f)

for item in artefacts:
    name = item["name"]
    url = item["url"]
    dest = Path(item["dest"])
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        urllib.request.urlretrieve(url, dest)
    except Exception as e:
        print(f"Failed to download {name}: {e}")
