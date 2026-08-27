import sys, re, os

src = sys.argv[1]
out = sys.argv[2]
files = [
    os.path.join(src, f) for f in os.listdir(src) if f.endswith(".txt") and len(f) > 5
]
report = []
MAX_BLOCK = 900
MAX_BLOCKS = 14
for fp in sorted(files):
    try:
        txt = open(fp, encoding="utf-8", errors="ignore").read()
    except Exception as e:
        continue
    name = os.path.splitext(os.path.basename(fp))[0]
    # find read-aloud markers
    blocks = []
    for m in re.finditer(
        r"(read[-\s]?aloud|read to the players|players read|boxed text|read aloud text)",
        txt,
        re.I,
    ):
        s = max(0, m.start() - 120)
        e = min(len(txt), m.end() + 700)
        chunk = txt[s:e]
        chunk = re.sub(r"\n{2,}", "\n", chunk)
        if len(chunk) > 40:
            blocks.append(chunk.strip())
        if len(blocks) >= MAX_BLOCKS:
            break
    if not blocks:
        # fallback: grab first few descriptive lines / intro
        sample = txt[:1200].strip()
        blocks = [sample]
    report.append(f"\n{'=' * 80}\n### {name}\n{'=' * 80}")
    for i, b in enumerate(blocks[:MAX_BLOCKS]):
        report.append(f"\n--- block {i + 1} ---\n" + b[:MAX_BLOCK])
open(out, "w", encoding="utf-8").write("\n".join(report))
print("wrote", out, "modules:", len(files))
