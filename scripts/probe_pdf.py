import sys
from pypdf import PdfReader

for f in sys.argv[1:]:
    try:
        r = PdfReader(f)
        for mode in ("layout", "plain"):
            try:
                t = r.pages[0].extract_text(extraction_mode=mode) or ""
                print(f"{f.split(chr(92))[-1]} mode={mode} page0_len={len(t)}")
                if t.strip():
                    print("   sample:", repr(t[:160]))
                    break
            except Exception as e:
                print("   mode err", mode, e)
    except Exception as e:
        print("ERR", f, e)
