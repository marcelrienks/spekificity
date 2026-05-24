#!/usr/bin/env python3
"""Standardize top-level section ordering for spec files in wiki/specs.

Template order (non-destructive):
  - H1 (title)
  - short summary/introduction (anything before first H2)
  - Dependencies / Depends On / Used By
  - Overview / Purpose
  - Scope & Relationships
  - Examples
  - Success Criteria
  - References / See also
  - Any remaining sections (appended)

Idempotent: will not duplicate sections if order already matches.
"""
from pathlib import Path
import re
import glob


ORDER = [
    'dependencies',
    'overview',
    'purpose',
    'scope',
    'examples',
    'success criteria',
    'references',
]


def normalize_heading(h):
    return re.sub(r"[^a-z0-9 ]+", '', h.lower()).strip()


def split_sections(text):
    # Split into preamble (before first H2) and H2 sections
    lines = text.splitlines(keepends=True)
    sections = []
    current = {'heading': None, 'content': ''}
    i = 0
    while i < len(lines):
        ln = lines[i]
        m = re.match(r'^(#{2,})\s+(.*)', ln)
        if m:
            # start new section
            if current['heading'] is not None or current['content']:
                sections.append(current)
            current = {'heading': m.group(2).strip(), 'content': ''}
        else:
            current['content'] += ln
        i += 1
    sections.append(current)
    return sections


def build_ordered(text):
    # preserve H1 and anything before first H2 as preamble
    parts = re.split(r'(\n##\s+)', text, maxsplit=1)
    if len(parts) == 1:
        return text
    preamble = parts[0]
    rest = '## ' + parts[2] + parts[3] if len(parts) >= 4 else parts[0]
    sections = split_sections(text)
    # separate preamble (heading None) and actual sections
    pre = sections[0]
    others = sections[1:]
    mapped = {}
    remaining = []
    for s in others:
        key = normalize_heading(s['heading'])
        placed = False
        for name in ORDER:
            if name in key:
                mapped.setdefault(name, []).append(s)
                placed = True
                break
        if not placed:
            remaining.append(s)

    # assemble
    out = pre['content'] if pre['heading'] is None else ('## ' + pre['heading'] + '\n' + pre['content'])
    for name in ORDER:
        for s in mapped.get(name, []):
            out += f"\n## {s['heading']}\n" + s['content']
    for s in remaining:
        out += f"\n## {s['heading']}\n" + s['content']
    return out


def process_file(p: Path):
    text = p.read_text(encoding='utf-8')
    new = build_ordered(text)
    if new != text:
        p.write_text(new, encoding='utf-8')
        return True
    return False


def main():
    modified = []
    for f in sorted(glob.glob('wiki/specs/*.md')):
        if f.endswith('_boilerplate.md') or f.endswith('.md') and '/examples/' in f:
            pass
        p = Path(f)
        try:
            if process_file(p):
                modified.append(p)
        except Exception as e:
            print(f"Error {p}: {e}")
    if modified:
        print('Reordered sections in:')
        for m in modified:
            print(' -', m)
    else:
        print('No files required reordering.')


if __name__ == '__main__':
    main()
