import json, os, re, sys, unicodedata
newdir, curdir = sys.argv[1], sys.argv[2]
def key(s): return re.sub(r"[^a-z0-9]", "", unicodedata.normalize("NFKD", s.split("(")[0]).encode("ascii","ignore").decode().lower())
cur = {f[:-5] for f in os.listdir(curdir)}
curnames = {key(json.load(open(f"{curdir}/{f}"))["name"]) for f in os.listdir(curdir)}
w, skipped = [], []
for f in sorted(os.listdir(newdir)):
    r = json.load(open(f"{newdir}/{f}")); k = key(r["name"])
    if f[:-5] in cur or k in curnames or any(len(k) > 6 and (k in c or c in k) for c in curnames if len(c) > 6):
        skipped.append(r["name"]); continue
    curnames.add(k)
    w.append({"op":"set","collection":"places","doc_id":f[:-5],"file_path":os.path.abspath(f"{newdir}/{f}")})
print("SKIPPED:", skipped, file=sys.stderr)
print(json.dumps(w))
