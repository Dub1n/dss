"""Link checker for DSS repo."""
import re, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
def main():
    missing=[]
    for md in ROOT.rglob("*.md"):
        txt = md.read_text(encoding="utf-8")
        for link in re.findall(r"\[[^\]]+\]\(([^)]+)\)", txt):
            t = (md.parent / link).resolve()
            if not t.exists():
                missing.append((md.relative_to(ROOT), link))
    if missing:
        print("Missing links:")
        for src,l in missing: print(f"{src} -> {l}")
        sys.exit(1)
    print("All links ok.")
if __name__=="__main__": main()
