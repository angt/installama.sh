import json
import shutil
import urllib.request
from pathlib import Path

with open("artefacts.json", "r", encoding="utf-8") as f:
    artefacts = json.load(f)

for item in artefacts:
    src = item["src"]
    dst = Path(item["dst"])
    dst.parent.mkdir(parents=True, exist_ok=True)
    try:
        if src.startswith("https://"):
            urllib.request.urlretrieve(src, dst)
        else:
            shutil.copy2(src, dst)
    except Exception as e:
        print(f"Failed to process {dst}: {e}")
