"""Unit tests for spekificity.caveman.install."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from spekificity.caveman.install import (
    CavemanInstallResult,
    _add_hook,
    _copy_skill,
    _fetch_skill_content,
    _has_hook,
    _strip_jsonc,
    _write_project_hooks,
    install_caveman,
)

DUMMY_SKILL = b"# Caveman\nBe terse."


# ---------------------------------------------------------------------------
# _strip_jsonc
# ---------------------------------------------------------------------------

class TestStripJsonc:
    def test_removes_line_comments(self):
        src = '{"a": 1 // comment\n}'
        assert json.loads(_strip_jsonc(src)) == {"a": 1}

    def test_removes_block_comments(self):
        src = '{"a": /* comment */ 1}'
        assert json.loads(_strip_jsonc(src)) == {"a": 1}

    def test_preserves_comment_like_content_in_strings(self):
        src = '{"url": "http://example.com"}'
        assert json.loads(_strip_jsonc(src)) == {"url": "http://example.com"}

    def test_removes_trailing_commas_in_object(self):
        src = '{"a": 1,}'
        assert json.loads(_strip_jsonc(src)) == {"a": 1}

    def test_removes_trailing_commas_in_array(self):
        src = '[1, 2, 3,]'
        assert json.loads(_strip_jsonc(src)) == [1, 2, 3]

    def test_plain_json_unchanged(self):
        src = '{"a": 1, "b": [2, 3]}'
        assert json.loads(_strip_jsonc(src)) == {"a": 1, "b": [2, 3]}


# ---------------------------------------------------------------------------
# _fetch_skill_content — T007
# ---------------------------------------------------------------------------

class TestFetchSkillContent:
    def test_fetch_from_global_skills(self, tmp_path):
        global_skill = tmp_path / ".claude" / "skills" / "caveman" / "SKILL.md"
        global_skill.parent.mkdir(parents=True)
        global_skill.write_bytes(DUMMY_SKILL)
        with patch("spekificity.caveman.install.Path.home", return_value=tmp_path):
            result = _fetch_skill_content()
        assert result == DUMMY_SKILL

    def test_fetch_falls_back_to_plugin_cache(self, tmp_path):
        # Global skills absent; plugin cache present
        sha_dir = tmp_path / ".claude" / "plugins" / "cache" / "caveman" / "caveman" / "abc123"
        candidate = sha_dir / "plugins" / "caveman" / "skills" / "caveman" / "SKILL.md"
        candidate.parent.mkdir(parents=True)
        candidate.write_bytes(DUMMY_SKILL)
        with patch("spekificity.caveman.install.Path.home", return_value=tmp_path):
            result = _fetch_skill_content()
        assert result == DUMMY_SKILL

    def test_fetch_falls_back_to_github(self, tmp_path):
        mock_resp = MagicMock()
        mock_resp.__enter__ = lambda s: s
        mock_resp.__exit__ = MagicMock(return_value=False)
        mock_resp.read.return_value = DUMMY_SKILL
        with patch("spekificity.caveman.install.Path.home", return_value=tmp_path):
            with patch("urllib.request.urlopen", return_value=mock_resp):
                result = _fetch_skill_content()
        assert result == DUMMY_SKILL

    def test_all_fail_returns_none(self, tmp_path):
        import urllib.error
        with patch("spekificity.caveman.install.Path.home", return_value=tmp_path):
            with patch("urllib.request.urlopen", side_effect=urllib.error.URLError("offline")):
                result = _fetch_skill_content()
        assert result is None


# ---------------------------------------------------------------------------
# _copy_skill — T008
# ---------------------------------------------------------------------------

class TestCopySkill:
    def test_flat_integration_writes_caveman_md(self, tmp_path):
        status = _copy_skill(tmp_path, "claude", DUMMY_SKILL)
        dest = tmp_path / ".claude" / "commands" / "caveman.md"
        assert status == "installed"
        assert dest.exists()
        assert dest.read_bytes() == DUMMY_SKILL

    def test_subfolder_integration_writes_skill_md(self, tmp_path):
        status = _copy_skill(tmp_path, "cursor-agent", DUMMY_SKILL)
        dest = tmp_path / ".cursor" / "skills" / "caveman" / "SKILL.md"
        assert status == "installed"
        assert dest.exists()

    def test_generic_integration_flat_path(self, tmp_path):
        status = _copy_skill(tmp_path, "generic", DUMMY_SKILL)
        dest = tmp_path / ".agents" / "skills" / "caveman.md"
        assert status == "installed"
        assert dest.exists()

    def test_idempotent_returns_skipped(self, tmp_path):
        _copy_skill(tmp_path, "claude", DUMMY_SKILL)
        status = _copy_skill(tmp_path, "claude", DUMMY_SKILL)
        assert status == "skipped"

    def test_idempotent_does_not_overwrite(self, tmp_path):
        dest = tmp_path / ".claude" / "commands" / "caveman.md"
        dest.parent.mkdir(parents=True)
        dest.write_bytes(b"original")
        _copy_skill(tmp_path, "claude", DUMMY_SKILL)
        assert dest.read_bytes() == b"original"

    def test_none_content_returns_failed(self, tmp_path):
        status = _copy_skill(tmp_path, "claude", None)
        assert status == "failed"
        assert not (tmp_path / ".claude" / "commands" / "caveman.md").exists()


# ---------------------------------------------------------------------------
# _has_hook / _add_hook
# ---------------------------------------------------------------------------

class TestHookHelpers:
    def test_has_hook_detects_marker(self):
        settings = {
            "hooks": {
                "SessionStart": [{"hooks": [{"type": "command", "command": 'node "caveman-activate.js"'}]}]
            }
        }
        assert _has_hook(settings, "SessionStart", "caveman-activate") is True

    def test_has_hook_absent(self):
        settings: dict = {}
        assert _has_hook(settings, "SessionStart", "caveman-activate") is False

    def test_add_hook_appends_entry(self):
        settings: dict = {}
        _add_hook(settings, "SessionStart", 'node "script.js"', "Loading...")
        entries = settings["hooks"]["SessionStart"]
        assert len(entries) == 1
        assert entries[0]["hooks"][0]["command"] == 'node "script.js"'
        assert entries[0]["hooks"][0]["timeout"] == 5

    def test_add_hook_preserves_existing(self):
        settings = {"hooks": {"SessionStart": [{"hooks": [{"type": "command", "command": "other"}]}]}}
        _add_hook(settings, "SessionStart", 'node "caveman-activate.js"', "Loading...")
        assert len(settings["hooks"]["SessionStart"]) == 2


# ---------------------------------------------------------------------------
# _write_project_hooks — T013
# ---------------------------------------------------------------------------

class TestWriteProjectHooks:
    def _make_node(self, tmp_path: Path) -> str:
        """Create a fake node script for shutil.which to find."""
        fake_node = tmp_path / "fake_node"
        fake_node.write_text("#!/bin/sh\nexit 0\n")
        fake_node.chmod(0o755)
        return str(fake_node)

    def test_creates_settings_json_with_both_hooks(self, tmp_path):
        project = tmp_path / "project"
        project.mkdir()
        # Simulate global hooks present
        hooks_dir = tmp_path / "home" / ".claude" / "hooks"
        hooks_dir.mkdir(parents=True)
        (hooks_dir / "caveman-activate.js").write_text("// stub")
        (hooks_dir / "caveman-mode-tracker.js").write_text("// stub")

        with patch("spekificity.caveman.install.Path.home", return_value=tmp_path / "home"):
            with patch("shutil.which", return_value="/usr/bin/node"):
                with patch("spekificity.caveman.install._ensure_global_hooks", return_value=True):
                    status = _write_project_hooks(project)

        assert status == "installed"
        settings_path = project / ".claude" / "settings.json"
        assert settings_path.exists()
        settings = json.loads(settings_path.read_text())
        assert _has_hook(settings, "SessionStart", "caveman-activate")
        assert _has_hook(settings, "UserPromptSubmit", "caveman-mode-tracker")

    def test_merges_with_existing_settings(self, tmp_path):
        project = tmp_path / "project"
        (project / ".claude").mkdir(parents=True)
        existing = {"permissions": {"allow": ["Bash(git status)"]}}
        (project / ".claude" / "settings.json").write_text(json.dumps(existing))

        hooks_dir = tmp_path / "home" / ".claude" / "hooks"
        hooks_dir.mkdir(parents=True)
        (hooks_dir / "caveman-activate.js").write_text("// stub")

        with patch("spekificity.caveman.install.Path.home", return_value=tmp_path / "home"):
            with patch("shutil.which", return_value="/usr/bin/node"):
                with patch("spekificity.caveman.install._ensure_global_hooks", return_value=True):
                    _write_project_hooks(project)

        settings = json.loads((project / ".claude" / "settings.json").read_text())
        # Existing entry preserved
        assert settings["permissions"]["allow"] == ["Bash(git status)"]
        # Caveman hooks added
        assert _has_hook(settings, "SessionStart", "caveman-activate")

    def test_idempotent_returns_skipped(self, tmp_path):
        project = tmp_path / "project"
        hooks_dir = tmp_path / "home" / ".claude" / "hooks"
        hooks_dir.mkdir(parents=True)
        (hooks_dir / "caveman-activate.js").write_text("// stub")

        with patch("spekificity.caveman.install.Path.home", return_value=tmp_path / "home"):
            with patch("shutil.which", return_value="/usr/bin/node"):
                with patch("spekificity.caveman.install._ensure_global_hooks", return_value=True):
                    _write_project_hooks(project)
                    status = _write_project_hooks(project)

        assert status == "skipped"

    def test_idempotent_no_duplicate_entries(self, tmp_path):
        project = tmp_path / "project"
        hooks_dir = tmp_path / "home" / ".claude" / "hooks"
        hooks_dir.mkdir(parents=True)
        (hooks_dir / "caveman-activate.js").write_text("// stub")

        with patch("spekificity.caveman.install.Path.home", return_value=tmp_path / "home"):
            with patch("shutil.which", return_value="/usr/bin/node"):
                with patch("spekificity.caveman.install._ensure_global_hooks", return_value=True):
                    _write_project_hooks(project)
                    _write_project_hooks(project)

        settings = json.loads((project / ".claude" / "settings.json").read_text())
        ss_entries = settings.get("hooks", {}).get("SessionStart", [])
        activate_count = sum(
            1 for e in ss_entries
            for h in e.get("hooks", [])
            if "caveman-activate" in h.get("command", "")
        )
        assert activate_count == 1

    def test_node_not_found_returns_failed(self, tmp_path):
        project = tmp_path / "project"
        project.mkdir()
        with patch("shutil.which", return_value=None):
            status = _write_project_hooks(project)
        assert status == "failed"
        assert not (project / ".claude" / "settings.json").exists()

    def test_handles_jsonc_settings_file(self, tmp_path):
        project = tmp_path / "project"
        (project / ".claude").mkdir(parents=True)
        jsonc_content = '{\n  // A comment\n  "theme": "dark", /* trailing */\n}'
        (project / ".claude" / "settings.json").write_text(jsonc_content)

        hooks_dir = tmp_path / "home" / ".claude" / "hooks"
        hooks_dir.mkdir(parents=True)
        (hooks_dir / "caveman-activate.js").write_text("// stub")

        with patch("spekificity.caveman.install.Path.home", return_value=tmp_path / "home"):
            with patch("shutil.which", return_value="/usr/bin/node"):
                with patch("spekificity.caveman.install._ensure_global_hooks", return_value=True):
                    status = _write_project_hooks(project)

        assert status == "installed"
        settings = json.loads((project / ".claude" / "settings.json").read_text())
        assert settings["theme"] == "dark"


# ---------------------------------------------------------------------------
# install_caveman — T009, T014, T015
# ---------------------------------------------------------------------------

class TestInstallCaveman:
    def test_failure_non_fatal_no_exception(self, tmp_path):
        import urllib.error
        with patch("spekificity.caveman.install.Path.home", return_value=tmp_path):
            with patch("urllib.request.urlopen", side_effect=urllib.error.URLError("offline")):
                result = install_caveman(tmp_path, "copilot")
        assert isinstance(result, CavemanInstallResult)
        assert result.status == "failed"
        assert result.skill_status == "failed"

    def test_non_claude_no_hooks_written(self, tmp_path):
        with patch("spekificity.caveman.install._fetch_skill_content", return_value=DUMMY_SKILL):
            result = install_caveman(tmp_path, "gemini")
        assert result.hook_status == "n/a"
        assert not (tmp_path / ".claude" / "settings.json").exists()

    def test_non_claude_skill_installed(self, tmp_path):
        with patch("spekificity.caveman.install._fetch_skill_content", return_value=DUMMY_SKILL):
            result = install_caveman(tmp_path, "gemini")
        assert result.skill_status == "installed"
        dest = tmp_path / ".gemini" / "skills" / "caveman" / "SKILL.md"
        assert dest.exists()

    def test_claude_writes_hooks(self, tmp_path):
        hooks_dir = tmp_path / ".claude" / "hooks"
        hooks_dir.mkdir(parents=True)
        (hooks_dir / "caveman-activate.js").write_text("// stub")

        with patch("spekificity.caveman.install._fetch_skill_content", return_value=DUMMY_SKILL):
            with patch("spekificity.caveman.install.Path.home", return_value=tmp_path):
                with patch("shutil.which", return_value="/usr/bin/node"):
                    with patch("spekificity.caveman.install._ensure_global_hooks", return_value=True):
                        result = install_caveman(tmp_path, "claude")

        assert result.hook_status == "installed"
        settings = json.loads((tmp_path / ".claude" / "settings.json").read_text())
        assert _has_hook(settings, "SessionStart", "caveman-activate")

    def test_status_installed_when_skill_installs(self, tmp_path):
        with patch("spekificity.caveman.install._fetch_skill_content", return_value=DUMMY_SKILL):
            result = install_caveman(tmp_path, "copilot")
        assert result.status == "installed"

    def test_status_skipped_when_both_already_present(self, tmp_path):
        # Pre-install
        with patch("spekificity.caveman.install._fetch_skill_content", return_value=DUMMY_SKILL):
            install_caveman(tmp_path, "copilot")
        # Re-install
        with patch("spekificity.caveman.install._fetch_skill_content", return_value=DUMMY_SKILL):
            result = install_caveman(tmp_path, "copilot")
        assert result.status == "skipped"
        assert result.skill_status == "skipped"
