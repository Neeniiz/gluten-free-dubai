import json, re, sys, os, unicodedata
src, outdir, prefix = sys.argv[1], sys.argv[2], sys.argv[3]
texts = []
def walk(o):
    if isinstance(o, dict):
        for v in o.values():
            if isinstance(v, str): texts.append(v)
            else: walk(v)
    elif isinstance(o, list):
        for v in o: walk(v)
for line in open(src):
    try: walk(json.loads(line))
    except Exception: pass
rows = None
dec = json.JSONDecoder()
for t in reversed(texts):
    i = t.find('[')
    while i != -1:
        try:
            v, _ = dec.raw_decode(t[i:])
            if isinstance(v, list) and v and isinstance(v[0], dict) and "name" in v[0] and "evidence_level" in v[0]:
                rows = v; break
        except Exception: pass
        i = t.find('[', i + 1)
    if rows: break
os.makedirs(outdir, exist_ok=True)
def norm_tamari(v):
    v = str(v or "").strip().lower()
    for k in ("yes", "no", "unknown", "n/a"):
        if v == k or v.startswith(k + " ") or v.startswith(k + ","): return k
    return "ask" if v else "unknown"
for r in rows:
    slug = re.sub(r"[^a-z0-9]+", "-", unicodedata.normalize("NFKD", r["name"].split("(")[0]).encode("ascii","ignore").decode().lower()).strip("-")[:60]
    r["tamari"] = norm_tamari(r.get("tamari"))
    r["delivery"] = [d for d in r.get("delivery", []) if not re.match(r"(unknown|n/a)", str(d).lower())]
    w = r.get("website") or ""
    r["website"] = w if w.startswith("http") else ""
    r.update({"status": None, "notes": "", "researched": "2026-10-18", "batch": prefix, "updated": 0})
    r.setdefault("ask_dishes", [])
    for k in [k for k in r if k != k.strip()]: r.pop(k)
    json.dump(r, open(f"{outdir}/{slug}.json", "w"), ensure_ascii=False)
    print(slug, "|", r["cuisine"], "|", r["evidence_level"], "|", r["tamari"])
