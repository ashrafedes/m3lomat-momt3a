# Fetch Pexels images for article categories -> tools/pexels.json
# Usage: PEXELS_API_KEY=xxx python tools/fetch_pexels.py
import json, os, sys, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEY = os.environ.get("PEXELS_API_KEY")
if not KEY:
    sys.exit("set PEXELS_API_KEY")

QUERIES = {
    "space": ["space galaxy stars", "planet astronomy"],
    "science": ["science laboratory", "chemistry experiment"],
    "animals": ["wildlife animal", "animals nature"],
    "human": ["human anatomy", "medical health"],
    "history": ["ancient history ruins", "museum historical"],
    "tech": ["technology computer", "futuristic tech"],
    "nature": ["nature landscape", "forest nature"],
    "geo": ["earth map geography", "mountains landscape aerial"],
    "food": ["cooking food kitchen", "egyptian food"],
    "religion": ["quran mosque prayer", "ramadan islam"],
    "money": ["business money finance", "office work"],
}

out = {}
for cat, queries in QUERIES.items():
    photos = []
    seen = set()
    for q in queries:
        url = ("https://api.pexels.com/v1/search?query=%s&per_page=15&orientation=landscape"
               % urllib.parse.quote(q))
        req = urllib.request.Request(url, headers={
            "Authorization": KEY, "User-Agent": "Mozilla/5.0"})
        try:
            data = json.load(urllib.request.urlopen(req, timeout=20))
        except Exception as e:
            print(cat, q, "FAILED:", e)
            continue
        for p in data.get("photos", []):
            if p["id"] in seen:
                continue
            seen.add(p["id"])
            photos.append({
                "img": p["src"]["large"],
                "thumb": p["src"]["medium"],
                "credit": p["photographer"],
                "credit_url": p["photographer_url"],
            })
    out[cat] = photos
    print(cat, len(photos))

dst = os.path.join(ROOT, "tools", "pexels.json")
json.dump(out, open(dst, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote", dst)
