"""Auto-tagging and wikilink insertion for vault lesson files."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from difflib import SequenceMatcher
from pathlib import Path

from spekificity.utils import print_status


_STOPWORDS = frozenset({
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "as", "is", "was", "are", "were", "be",
    "been", "being", "have", "has", "had", "do", "does", "did", "will",
    "would", "could", "should", "may", "might", "shall", "can", "it",
    "its", "this", "that", "these", "those", "we", "i", "you", "he",
    "she", "they", "my", "your", "our", "their", "not", "no", "if",
    "then", "when", "so", "there", "here",
})


@dataclass
class AutolinkResult:
    links_inserted: int = 0
    tags_added: list[str] = field(default_factory=list)
    skipped: bool = False


def _build_vault_index(vault_path: Path) -> dict[str, Path]:
    """Scan vault_path recursively for .md files. Key = normalized stem."""
    index: dict[str, Path] = {}
    for path in vault_path.rglob("*.md"):
        key = path.stem.lower().replace("-", " ").replace("_", " ")
        index[key] = path
    return index


def _strip_markdown(text: str) -> str:
    """Remove markdown syntax to expose plain text for keyword extraction."""
    text = re.sub(r"```[\s\S]*?```", " ", text)
    text = re.sub(r"`[^`]+`", " ", text)
    text = re.sub(r"^#+\s+", " ", text, flags=re.MULTILINE)
    text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)
    text = re.sub(r"\[\[([^\]]+)\]\]", r"\1", text)
    text = re.sub(r"^[-*+]\s+", " ", text, flags=re.MULTILINE)
    text = re.sub(r"^\d+\.\s+", " ", text, flags=re.MULTILINE)
    return text


def _extract_keywords(text: str) -> list[str]:
    """Extract candidate keywords from lesson text (stdlib only)."""
    clean = _strip_markdown(text)
    words = re.findall(r"[a-zA-Z][\w-]*", clean)
    seen: set[str] = set()
    keywords: list[str] = []
    for word in words:
        norm = word.lower()
        if norm not in _STOPWORDS and len(norm) > 2 and norm not in seen:
            keywords.append(norm)
            seen.add(norm)
    return keywords


def _match_keywords(
    keywords: list[str],
    vault_index: dict[str, Path],
    threshold: float,
) -> list[tuple[str, Path]]:
    """Return (keyword, vault_path) pairs where similarity >= threshold."""
    matches: list[tuple[str, Path]] = []
    for keyword in keywords:
        for vault_key, vault_path in vault_index.items():
            if SequenceMatcher(None, keyword, vault_key).ratio() >= threshold:
                matches.append((keyword, vault_path))
                break
    return matches


def _insert_wikilinks(text: str, matches: list[tuple[str, Path]]) -> tuple[str, int]:
    """Replace bare keyword with [[keyword]]. Skips already-linked occurrences."""
    count = 0
    for keyword, _ in matches:
        pattern = re.compile(
            r"(?<!\[\[)\b" + re.escape(keyword) + r"\b(?!\]\])",
            re.IGNORECASE,
        )
        text, n = pattern.subn(f"[[{keyword}]]", text)
        count += n
    return text, count


def _add_frontmatter_tags(text: str, tags: list[str]) -> str:
    """Merge tags into YAML frontmatter. Creates block if absent."""
    if not tags:
        return text
    fm_pattern = re.compile(r"^---\n([\s\S]*?)\n---\n", re.MULTILINE)
    match = fm_pattern.match(text)
    if match:
        fm_body = match.group(1)
        tags_line = re.search(r"^tags:\s*\[([^\]]*)\]", fm_body, re.MULTILINE)
        if tags_line:
            existing = [t.strip() for t in tags_line.group(1).split(",") if t.strip()]
            merged = existing + [t for t in tags if t not in existing]
            new_fm = (
                fm_body[: tags_line.start()]
                + f"tags: [{', '.join(merged)}]"
                + fm_body[tags_line.end() :]
            )
            return f"---\n{new_fm}\n---\n" + text[match.end() :]
        new_fm = fm_body + f"\ntags: [{', '.join(tags)}]"
        return f"---\n{new_fm}\n---\n" + text[match.end() :]
    return f"---\ntags: [{', '.join(tags)}]\n---\n" + text


def process_lesson(
    lesson_path: Path,
    vault_path: Path,
    config: dict,
) -> AutolinkResult:
    """Enrich lesson file with wikilinks and frontmatter tags. Idempotent."""
    autolink_cfg = config.get("autolink", {})
    if not autolink_cfg.get("enabled", True):
        print_status("SKIP", "autolink disabled in config")
        return AutolinkResult(skipped=True)

    threshold = float(autolink_cfg.get("threshold", 0.8))
    keyword_tags: dict[str, list[str]] = autolink_cfg.get("keyword_tags", {})

    text = lesson_path.read_text()
    vault_index = _build_vault_index(vault_path)
    keywords = _extract_keywords(text)
    matches = _match_keywords(keywords, vault_index, threshold)

    text, links_inserted = _insert_wikilinks(text, matches)

    matched_keywords = {kw for kw, _ in matches}
    tags: list[str] = []
    for kw, tag_list in keyword_tags.items():
        if kw.lower() in matched_keywords:
            tags.extend(tag_list)

    text = _add_frontmatter_tags(text, tags)
    lesson_path.write_text(text)

    print_status("OK", f"autolink: {links_inserted} wikilink(s) inserted, {len(tags)} tag(s) added")
    return AutolinkResult(links_inserted=links_inserted, tags_added=tags)
