#!/usr/bin/env python3
"""Fix local markdown links in wiki/specs by mapping short basenames to prefixed filenames.

Behavior:
- Build mapping: for each file `NNN-name.md` map `name.md` -> `NNN-name.md`.
- For each markdown file, find relative links whose target file doesn't exist but matches a mapped key; replace target with mapped filename.

Idempotent: won't change already-correct links.
"""
from pathlib import Path
import re
import glob


LINK_RE = re.compile(r"(\[[^\]]+\]\()([^ )]+)(\))")


def build_map():
    m = {}
    for p in sorted(Path('wiki/specs').glob('*.md')):
        name = p.name
        # skip examples and _boilerplate
        if name.startswith('_') or (Path('wiki/specs/examples') in p.parents):
            continue
        # remove leading number+dash
        short = re.sub(r'^[0-9]+-', '', name)
        m[short] = name
    return m


def fix_file(p: Path, mapping):
    text = p.read_text(encoding='utf-8')
    changed = False
    def repl(m):
        full = m.group(0)
        target = m.group(2)
        if target.startswith('http') or target.startswith('#') or target.startswith('/'):
            return full
        target_path = target.split('#')[0]
        resolved = (p.parent / target_path).resolve()
        if resolved.exists():
            return full
        # try mapping
        if target_path in mapping:
            new_target = mapping[target_path]
            changed_local = True
            return m.group(1) + new_target + (('#' + target.split('#',1)[1]) if '#' in target else '') + m.group(3)
        return full
    new_text = LINK_RE.sub(repl, text)
    if new_text != text:
        p.write_text(new_text, encoding='utf-8')
        return True
    return False


def main():
    mapping = build_map()
    modified = []
    for f in sorted(glob.glob('wiki/specs/*.md')):
        p = Path(f)
        if p.name == '_boilerplate.md':
            continue
        try:
            if fix_file(p, mapping):
                modified.append(p)
        except Exception as e:
            print(f"Error fixing {p}: {e}")
    if modified:
        print('Updated links in:')
        for m in modified:
            print(' -', m)
    else:
        print('No link updates necessary.')


if __name__ == '__main__':
    main()
