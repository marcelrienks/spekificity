#!/usr/bin/env python3
"""Remove inline metadata fields from markdown files under wiki/specs/.

Targets: Status, Type, Version, Scope (both bolded '**Status:**' and plain 'Status:').
Idempotent: safe to run multiple times.
"""
import re
import glob
from pathlib import Path


def clean_text(text: str) -> (str, bool):
    orig = text
    # Remove any YAML frontmatter just in case (idempotent)
    if text.startswith("---\n"):
        parts = text.splitlines()
        for i in range(1, len(parts)):
            if parts[i].strip() == "---":
                text = "\n".join(parts[i+1:])
                break

    lines = text.splitlines(keepends=True)
    out_lines = []
    in_fence = False
    fence_re = re.compile(r"^\s*(```|~~~)\b")

    # patterns for inline bolded metadata
    bold_patterns = [
        re.compile(r"\*\*Status:\*\*\s*[^\n|]*\s*(\|\s*)?", re.IGNORECASE),
        re.compile(r"\*\*Type:\*\*\s*[^\n|]*\s*(\|\s*)?", re.IGNORECASE),
        re.compile(r"\*\*Version:\*\*\s*[^\n|]*\s*(\|\s*)?", re.IGNORECASE),
        re.compile(r"\*\*Scope:\*\*\s*[^\n|]*\s*(\|\s*)?", re.IGNORECASE),
    ]

    # line-start metadata patterns including optional bullet markers
    line_meta_re = re.compile(r"^[\s>\-*•]*\b(Status|Type|Version|Scope):\b.*$", re.IGNORECASE)

    for ln in lines:
        if fence_re.match(ln):
            in_fence = not in_fence
            out_lines.append(ln)
            continue

        if in_fence:
            out_lines.append(ln)
            continue

        s = ln
        # remove bolded inline metadata occurrences
        for pat in bold_patterns:
            s = pat.sub("", s)

        # if the (possibly stripped) line is a metadata-only line, skip it
        if line_meta_re.match(s.strip()):
            # drop the line entirely
            continue

        out_lines.append(s)

    new_text = "".join(out_lines)
    # Clean up repeated separators like ' |  | ' and leading/trailing '|' in title lines
    new_text = re.sub(r"\s*\|\s*\|\s*", " | ", new_text)
    new_text = re.sub(r"^\s*\|\s*", "", new_text, flags=re.MULTILINE)
    new_text = re.sub(r"\s*\|\s*$", "", new_text, flags=re.MULTILINE)

    changed = new_text != orig
    return new_text, changed


def main():
    base = Path(__file__).resolve().parents[1] / "wiki" / "specs"
    files = sorted(glob.glob(str(base / "*.md")))
    modified = []
    for f in files:
        p = Path(f)
        text = p.read_text(encoding="utf-8")
        new, did = clean_text(text)
        if did:
            p.write_text(new, encoding="utf-8")
            modified.append(p.relative_to(Path.cwd()))

    if modified:
        print("Removed inline metadata from files:")
        for m in modified:
            print(f" - {m}")
    else:
        print("No inline metadata fields found in wiki/specs/*.md files.")


if __name__ == "__main__":
    main()
