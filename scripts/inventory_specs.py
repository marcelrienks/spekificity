#!/usr/bin/env python3
"""Produce an inventory of markdown spec files under wiki/specs.

Outputs a simple markdown table: file, lines, words, SuccessCriteriaCount,
DependsOnCount,UsedByCount,CodeFenceCount,HasFrontmatter,FirstHeading
"""
from pathlib import Path
import re
import glob


def analyze(path):
    text = path.read_text(encoding='utf-8')
    lines = text.splitlines()
    words = len(text.split())
    sc = len(re.findall(r"^##+\s*Success Criteria", text, flags=re.IGNORECASE | re.MULTILINE))
    depends = len(re.findall(r"\bDepends On:\b|\bDepends on:\b", text, flags=re.IGNORECASE))
    usedby = len(re.findall(r"\bUsed By:\b|\bUsed by:\b|\bUsed by:?\b", text, flags=re.IGNORECASE))
    codefences = len(re.findall(r"^\s*(```|~~~)", text, flags=re.MULTILINE))
    has_front = text.startswith('---\n')
    # find first h1 or h2
    m = re.search(r"^#\s*(.+)$", text, flags=re.MULTILINE)
    first_h = m.group(1).strip() if m else ''
    return {
        'file': str(path),
        'lines': len(lines),
        'words': words,
        'success_criteria': sc,
        'depends_on': depends,
        'used_by': usedby,
        'code_fences': codefences,
        'frontmatter': has_front,
        'first_heading': first_h,
    }


def main():
    base = Path('wiki') / 'specs'
    files = sorted(glob.glob(str(base / '*.md')))
    rows = []
    for f in files:
        p = Path(f)
        rows.append(analyze(p))

    # print markdown table
    print('| File | Lines | Words | SuccessCriteria | DependsOn | UsedBy | CodeFences | Frontmatter | First Heading |')
    print('|---|---:|---:|---:|---:|---:|---:|---:|---|')
    for r in rows:
        print(f"| {r['file']} | {r['lines']} | {r['words']} | {r['success_criteria']} | {r['depends_on']} | {r['used_by']} | {r['code_fences']} | {int(r['frontmatter'])} | {r['first_heading'][:60]} |")


if __name__ == '__main__':
    main()
