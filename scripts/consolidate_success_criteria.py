#!/usr/bin/env python3
"""Consolidate multiple '## Success Criteria' sections into one per markdown spec.

Behavior:
- Finds all '## Success Criteria' headings (case-insensitive) and captures the
  following block until the next same-or-higher-level heading (# or ##) or EOF.
- Extracts list items and paragraph lines, preserves order, deduplicates while
  keeping first-seen order.
- Removes all original '## Success Criteria' sections and inserts a single
  consolidated '## Success Criteria' at the location of the first occurrence
  (or appends at EOF if none found).
"""
from pathlib import Path
import re
import glob


def extract_sections(text):
    # Find positions of headings '## Success Criteria' (case-insensitive)
    pattern = re.compile(r"^(##+)\s*Success Criteria\s*$", re.IGNORECASE | re.MULTILINE)
    matches = list(pattern.finditer(text))
    sections = []
    for m in matches:
        start = m.end()
        # find next heading (level 1 or 2) after start
        next_heading = re.search(r"^#{1,2}\b.*$", text[start:], re.MULTILINE)
        end = start + (next_heading.start() if next_heading else len(text[start:]))
        sections.append(text[start:end].strip())
    return matches, sections


def parse_items(section_text):
    items = []
    for line in section_text.splitlines():
        s = line.strip()
        # skip empty lines and horizontal rules
        if not s or s.startswith('---'):
            continue
        # list bullets
        m = re.match(r"^[-*+]\s+(.*)$", s)
        if m:
            items.append(m.group(1).strip())
            continue
        # numbered lists
        m = re.match(r"^\d+[.)]\s+(.*)$", s)
        if m:
            items.append(m.group(1).strip())
            continue
        # plain paragraph lines: take as items
        items.append(s)
    return items


def consolidate_items(all_items):
    seen = set()
    out = []
    for it in all_items:
        key = it.strip()
        if not key:
            continue
        if key in seen:
            continue
        seen.add(key)
        out.append(key)
    return out


def consolidate_file(path: Path) -> bool:
    text = path.read_text(encoding='utf-8')
    matches, sections = extract_sections(text)
    if not matches:
        return False

    all_items = []
    for sec in sections:
        all_items.extend(parse_items(sec))

    consolidated = consolidate_items(all_items)
    # Build consolidated section markdown
    if consolidated:
        block = "\n## Success Criteria\n\n"
        for it in consolidated:
            block += f"- {it}\n"
        block += "\n"
    else:
        block = "\n## Success Criteria\n\n- (no explicit items)\n\n"

    # Remove all original sections
    # We'll remove from end to start to keep positions stable
    new_text = text
    for m in reversed(matches):
        start_head = m.start()
        start = m.end()
        next_heading = re.search(r"^#{1,2}\b.*$", text[start:], re.MULTILINE)
        end = start + (next_heading.start() if next_heading else len(text[start:]))
        # remove from start_head to end
        new_text = new_text[:start_head] + new_text[end:]

    # Insert consolidated block at position of first match start
    insert_at = matches[0].start()
    new_text = new_text[:insert_at] + block + new_text[insert_at:]

    # Normalize double newlines
    new_text = re.sub(r"\n{3,}", "\n\n", new_text)

    if new_text != text:
        path.write_text(new_text, encoding='utf-8')
        return True
    return False


def main():
    base = Path('wiki') / 'specs'
    files = sorted(glob.glob(str(base / '*.md')))
    modified = []
    for f in files:
        p = Path(f)
        try:
            did = consolidate_file(p)
            if did:
                modified.append(p)
        except Exception as e:
            print(f"Error processing {p}: {e}")

    if modified:
        print('Consolidated Success Criteria in files:')
        for m in modified:
            print(' -', m)
    else:
        print('No files required consolidation.')


if __name__ == '__main__':
    main()
