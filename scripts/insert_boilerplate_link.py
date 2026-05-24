#!/usr/bin/env python3
"""Insert a short reference to _boilerplate.md after the first H1 in each spec file.

Idempotent: if the reference line already exists, it will not be added again.
"""
from pathlib import Path
import glob
import re


LINK_LINE = "See [Spec Boilerplate](./_boilerplate.md) for shared templates and conventions.\n"


def process(path: Path) -> bool:
    text = path.read_text(encoding='utf-8')
    # If link already present, skip
    if '_boilerplate.md' in text:
        return False

    # Find first H1
    m = re.search(r"^#\s+.*$", text, flags=re.MULTILINE)
    if not m:
        # prepend link
        new = LINK_LINE + "\n" + text
        path.write_text(new, encoding='utf-8')
        return True
    insert_at = m.end()
    # insert after heading and a following blank line if present
    # find position to insert (after first blank line following H1)
    rest = text[insert_at:]
    if rest.startswith("\n\n"):
        pos = insert_at + 2
    elif rest.startswith("\n"):
        pos = insert_at + 1
    else:
        pos = insert_at

    new = text[:pos] + "\n" + LINK_LINE + text[pos:]
    path.write_text(new, encoding='utf-8')
    return True


def main():
    base = Path('wiki') / 'specs'
    files = sorted(glob.glob(str(base / '*.md')))
    changed = []
    for f in files:
        p = Path(f)
        try:
            if process(p):
                changed.append(p)
        except Exception as e:
            print(f"Error processing {p}: {e}")

    if changed:
        print('Inserted boilerplate link into files:')
        for c in changed:
            print(' -', c)
    else:
        print('No files updated (links already present).')


if __name__ == '__main__':
    main()
