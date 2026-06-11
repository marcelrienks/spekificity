"""Unit tests for spekificity.vault.autolink."""

from __future__ import annotations
from pathlib import Path
import pytest
from spekificity.vault.autolink import (
    _add_frontmatter_tags,
    _build_vault_index,
    _extract_keywords,
    _insert_wikilinks,
    _match_keywords,
    process_lesson,
)


class TestBuildVaultIndex:
    def test_normalized_stem_keys(self, tmp_path):
        (tmp_path / "decisions.md").touch()
        (tmp_path / "my-patterns.md").touch()
        index = _build_vault_index(tmp_path)
        assert "decisions" in index
        assert "my patterns" in index

    def test_scans_recursively(self, tmp_path):
        sub = tmp_path / "sub"
        sub.mkdir()
        (sub / "nested.md").touch()
        index = _build_vault_index(tmp_path)
        assert "nested" in index

    def test_empty_vault(self, tmp_path):
        assert _build_vault_index(tmp_path) == {}

    def test_underscores_normalized(self, tmp_path):
        (tmp_path / "auth_service.md").touch()
        index = _build_vault_index(tmp_path)
        assert "auth service" in index


class TestExtractKeywords:
    def test_removes_stopwords(self):
        kws = _extract_keywords("the cat and the dog")
        assert "the" not in kws
        assert "and" not in kws

    def test_strips_markdown_headers(self):
        kws = _extract_keywords("# Heading\nsome authentication content")
        assert "authentication" in kws

    def test_strips_code_blocks(self):
        kws = _extract_keywords("```python\nimport os\n```\nauthentication")
        assert "authentication" in kws

    def test_deduplicates(self):
        kws = _extract_keywords("auth auth auth")
        assert kws.count("auth") == 1

    def test_filters_short_words(self):
        kws = _extract_keywords("ok hi authentication")
        assert "ok" not in kws
        assert "hi" not in kws
        assert "authentication" in kws

    def test_strips_wikilinks(self):
        kws = _extract_keywords("[[decisions]] are important for authentication")
        assert "decisions" in kws
        assert "authentication" in kws


class TestMatchKeywords:
    def test_exact_match_above_threshold(self):
        index = {"decisions": Path("decisions.md")}
        matches = _match_keywords(["decisions"], index, 0.8)
        assert len(matches) == 1
        assert matches[0][0] == "decisions"

    def test_skips_below_threshold(self):
        index = {"decisions": Path("decisions.md")}
        matches = _match_keywords(["xyz"], index, 0.8)
        assert matches == []

    def test_one_match_per_keyword(self):
        index = {
            "auth": Path("auth.md"),
            "authentication": Path("authentication.md"),
        }
        matches = _match_keywords(["auth"], index, 0.8)
        assert len(matches) == 1

    def test_empty_index(self):
        assert _match_keywords(["auth"], {}, 0.8) == []


class TestInsertWikilinks:
    def test_wraps_bare_keyword(self):
        text = "We use decisions in this project."
        matches = [("decisions", Path("decisions.md"))]
        result, count = _insert_wikilinks(text, matches)
        assert "[[decisions]]" in result
        assert count == 1

    def test_does_not_double_wrap_existing(self):
        text = "We use [[decisions]] already."
        matches = [("decisions", Path("decisions.md"))]
        result, count = _insert_wikilinks(text, matches)
        assert result.count("[[decisions]]") == 1
        assert count == 0

    def test_count_reflects_insertions(self):
        text = "auth auth auth"
        matches = [("auth", Path("auth.md"))]
        _, count = _insert_wikilinks(text, matches)
        assert count == 3

    def test_no_matches_unchanged(self):
        text = "nothing to link here"
        result, count = _insert_wikilinks(text, [])
        assert result == text
        assert count == 0


class TestAddFrontmatterTags:
    def test_creates_block_when_absent(self):
        text = "# Lesson\ncontent"
        result = _add_frontmatter_tags(text, ["auth", "security"])
        assert result.startswith("---\n")
        assert "tags: [auth, security]" in result
        assert "# Lesson" in result

    def test_merges_into_existing_block(self):
        text = "---\ntitle: foo\ntags: [existing]\n---\ncontent"
        result = _add_frontmatter_tags(text, ["new"])
        assert "existing" in result
        assert "new" in result

    def test_no_duplicate_tags(self):
        text = "---\ntags: [auth]\n---\ncontent"
        result = _add_frontmatter_tags(text, ["auth"])
        assert result.count("auth") == 1

    def test_noop_when_tags_empty(self):
        text = "# content"
        assert _add_frontmatter_tags(text, []) == text

    def test_adds_tags_to_block_without_existing_tags(self):
        text = "---\ntitle: foo\n---\ncontent"
        result = _add_frontmatter_tags(text, ["security"])
        assert "tags: [security]" in result


class TestProcessLesson:
    def test_skipped_when_disabled(self, tmp_path):
        lesson = tmp_path / "lesson.md"
        lesson.write_text("auth content")
        result = process_lesson(lesson, tmp_path, {"autolink": {"enabled": False}})
        assert result.skipped is True
        assert lesson.read_text() == "auth content"

    def test_inserts_wikilinks_for_vault_match(self, tmp_path):
        vault = tmp_path / "vault"
        vault.mkdir()
        (vault / "decisions.md").touch()
        lesson = tmp_path / "lesson.md"
        lesson.write_text("We use decisions here.")
        result = process_lesson(lesson, vault, {})
        assert "[[decisions]]" in lesson.read_text()
        assert result.links_inserted >= 1

    def test_idempotent(self, tmp_path):
        vault = tmp_path / "vault"
        vault.mkdir()
        (vault / "decisions.md").touch()
        lesson = tmp_path / "lesson.md"
        lesson.write_text("We use decisions here.")
        process_lesson(lesson, vault, {})
        first_text = lesson.read_text()
        result2 = process_lesson(lesson, vault, {})
        assert lesson.read_text() == first_text
        assert result2.links_inserted == 0

    def test_adds_tags_from_keyword_tags_config(self, tmp_path):
        vault = tmp_path / "vault"
        vault.mkdir()
        (vault / "auth.md").touch()
        lesson = tmp_path / "lesson.md"
        lesson.write_text("auth implementation details")
        config = {"autolink": {"keyword_tags": {"auth": ["security", "authentication"]}}}
        result = process_lesson(lesson, vault, config)
        content = lesson.read_text()
        assert "security" in content
        assert "authentication" in content
        assert result.tags_added == ["security", "authentication"]

    def test_no_vault_files_no_links(self, tmp_path):
        vault = tmp_path / "vault"
        vault.mkdir()
        lesson = tmp_path / "lesson.md"
        lesson.write_text("some content with no vault matches")
        result = process_lesson(lesson, vault, {})
        assert result.links_inserted == 0
        assert result.skipped is False
