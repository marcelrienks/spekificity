#!/usr/bin/env python3
"""Find and report broken local markdown links in wiki/specs/*.md

Checks:
- Markdown links of form [text](target). If target is a relative path, verify the file exists.
- For targets with fragments (file.md#anchor), verify the file exists (does not verify anchors).

Prints a list of broken links with file context and returns non-zero if any broken links found.
"""
from pathlib import Path
import re
import glob
import sys


LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def check_file(p: Path):
    text = p.read_text(encoding='utf-8')
    broken = []
    for m in LINK_RE.finditer(text):
        target = m.group(1).strip()
        if target.startswith('http://') or target.startswith('https://') or target.startswith('mailto:'):
            continue
        # strip title part after space
        if ' "' in target or " '" in target:
            target = target.split(' ')[0]
        # remove surrounding <> if present
        target = target.strip('<>')
        # handle anchors
        if target.startswith('#'):
            continue
        target_path = target.split('#')[0]
        # consider relative to the markdown file
        tp = (p.parent / target_path).resolve()
        if not tp.exists():
            broken.append((m.group(0), target, tp))
    return broken


def main():
    files = sorted(glob.glob('wiki/specs/*.md'))
    any_broken = False
    for f in files:
        p = Path(f)
        broken = check_file(p)
        if broken:
            any_broken = True
            print(f"Broken links in {p}:")
            for link_text, target, tp in broken:
                print(f" - {link_text} -> {target} (resolved {tp})")
    if any_broken:
        print('\nLink check completed: broken links found.')
        sys.exit(2)
    else:
        print('Link check completed: no broken local links found.')


if __name__ == '__main__':
    main()
