#!/usr/bin/env python3
"""Remove leading YAML frontmatter (--- ... ---) from markdown files under wiki/specs/.

Idempotent: files without frontmatter are left unchanged.
"""
import glob
from pathlib import Path


def strip_frontmatter(text: str) -> (str, bool):
    if not text.startswith("---\n"):
        return text, False
    # find the closing '---' on its own line
    parts = text.splitlines()
    for i in range(1, len(parts)):
        if parts[i].strip() == "---":
            # remove lines 0..i inclusive
            new = "\n".join(parts[i+1:])
            # strip a single leading blank line if present
            if new.startswith("\n"):
                new = new[1:]
            return new, True
    return text, False


def main():
    base = Path(__file__).resolve().parents[1] / "wiki" / "specs"
    files = sorted(glob.glob(str(base / "*.md")))
    changed = []
    for f in files:
        p = Path(f)
        text = p.read_text(encoding="utf-8")
        new, did = strip_frontmatter(text)
        if did:
            p.write_text(new, encoding="utf-8")
            changed.append(p.relative_to(Path.cwd()))
    if changed:
        print("Removed frontmatter from files:")
        for c in changed:
            print(f" - {c}")
    else:
        print("No frontmatter found in wiki/specs/*.md files.")


if __name__ == "__main__":
    main()
