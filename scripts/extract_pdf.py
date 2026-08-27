import sys, re, os
from pypdf import PdfReader


def extract(path, out):
    try:
        r = PdfReader(path)
    except Exception as e:
        return f"ERR {e}"
    parts = []
    for i, pg in enumerate(r.pages):
        try:
            t = pg.extract_text() or ""
        except Exception as e:
            t = f"[page {i} err {e}]"
        parts.append(t)
    full = "\n".join(parts)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(full)
    return f"OK pages={len(r.pages)} chars={len(full)} -> {out}"


if __name__ == "__main__":
    path = sys.argv[1]
    outdir = (
        sys.argv[2]
        if len(sys.argv) > 2
        else os.path.join(os.environ.get("TEMP", "."), "opencode", "lore_pdf")
    )
    name = (
        os.path.splitext(os.path.basename(path))[0].replace(" ", "_").replace("'", "")
    )
    out = os.path.join(outdir, name + ".txt")
    print(extract(path, out))
