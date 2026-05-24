#!/usr/bin/env python3
"""Extract large fenced code blocks and large tables from specs into examples/.

Rules:
- Fenced code blocks with >=30 lines are moved to `wiki/specs/examples/<spec>-example-<n>.md`.
- Tables (consecutive lines containing '|' with a header separator) with >=12 lines moved similarly.
- Replacement text: short note linking to the extracted example file.

Idempotent: won't re-extract if link already present.
"""
from pathlib import Path
import re
import glob


EXAMPLES_DIR = Path('wiki') / 'specs' / 'examples'
EXAMPLES_DIR.mkdir(parents=True, exist_ok=True)


def extract_code_blocks(text):
    # find fenced blocks
    pattern = re.compile(r"(^```.*?$\n)(.*?)(\n^```\s*$)", re.MULTILINE | re.DOTALL)
    out = []
    for m in pattern.finditer(text):
        fence_open = m.group(1)
        body = m.group(2)
        fence_close = m.group(3)
        lines = body.count('\n') + 1
        start, end = m.span()
        out.append({'start': start, 'end': end, 'open': fence_open, 'body': body, 'close': fence_close, 'lines': lines})
    return out


def extract_tables(text):
    # crude detection: consecutive lines with '|' and a header separator line containing ---
    lines = text.splitlines()
    matches = []
    i = 0
    while i < len(lines):
        if '|' in lines[i]:
            j = i
            while j < len(lines) and '|' in lines[j]:
                j += 1
            block = lines[i:j]
            # require at least one separator line like | --- | or ---|
            if any(re.search(r"^-{3,}|\|\s*-{3,}", ln) for ln in block):
                matches.append({'start_line': i, 'end_line': j, 'lines': len(block), 'block': '\n'.join(block)})
            i = j
        else:
            i += 1
    return matches


def process_file(path: Path):
    text = path.read_text(encoding='utf-8')
    if 'examples/' in text:
        return False
    changed = False
    # code blocks
    code_blocks = extract_code_blocks(text)
    # iterate in reverse to preserve offsets
    ex_count = 0
    for cb in reversed(code_blocks):
        if cb['lines'] >= 30:
            ex_count += 1
            name = f"{path.stem}-code-{ex_count}.md"
            outpath = EXAMPLES_DIR / name
            outpath.write_text(cb['open'] + cb['body'] + cb['close'], encoding='utf-8')
            link = f"[Example: {name}](./examples/{name})"
            text = text[:cb['start']] + f"\n> Example moved to {link}\n\n" + text[cb['end']:]
            changed = True

    # tables
    tables = extract_tables(text)
    tcount = 0
    for tb in reversed(tables):
        if tb['lines'] >= 12:
            tcount += 1
            name = f"{path.stem}-table-{tcount}.md"
            outpath = EXAMPLES_DIR / name
            outpath.write_text(tb['block'], encoding='utf-8')
            # compute character offsets for line ranges
            all_lines = text.splitlines(keepends=True)
            start = sum(len(ln) for ln in all_lines[:tb['start_line']])
            end = sum(len(ln) for ln in all_lines[:tb['end_line']])
            link = f"[Table example: {name}](./examples/{name})"
            text = text[:start] + f"\n> Table moved to {link}\n\n" + text[end:]
            changed = True

    if changed:
        path.write_text(text, encoding='utf-8')
        return True
    return False


def main():
    files = sorted(glob.glob('wiki/specs/*.md'))
    modified = []
    for f in files:
        p = Path(f)
        try:
            if process_file(p):
                modified.append(p)
        except Exception as e:
            print(f"Error processing {p}: {e}")
    if modified:
        print('Extracted examples/tables from:')
        for m in modified:
            print(' -', m)
    else:
        print('No large examples or tables found to extract.')


if __name__ == '__main__':
    main()
