# Vault Sync Abstraction Specification

Date: 2026-05-21

Purpose
- Define the adapter interface and runtime selection rules for vault synchronization so the system works with Obsidian CLI when available and falls back to Git-only operations otherwise.

Design Overview
- Provide a single runtime factory `get_vault_sync(prefer: Optional[str])` returning an adapter implementing the `VaultSyncAdapter` protocol.
- Two adapters:
  - `ObsidianCLIAdapter`: uses the `obsidian` CLI to perform sync operations (publish, pull, list files).
  - `GitOnlyAdapter`: uses `GitPython` for basic file operations (pull, push, status) and direct file IO for read/write.

Adapter Interface (required methods)
- `list_files(path: str) -> List[str]` — list vault files under `path`.
- `read_file(path: str) -> str` — read file contents.
- `write_file(path: str, content: str) -> None` — write file contents (atomic write recommended).
- `sync_pull() -> None` — ensure local mirror matches remote (no-op for git-only local operations if not configured).
- `sync_push(commit_message: str) -> None` — push local changes; commit when necessary.

- `is_available() -> bool` — returns True if adapter runtime dependencies are available.

Selection Rules
- `prefer` argument controls selection: `obsidian_cli`, `git_only`, or None.
- If `prefer=None`: choose `ObsidianCLIAdapter` if `shutil.which('obsidian')` is truthy; otherwise `GitOnlyAdapter`.
- If `prefer='obsidian_cli'` and `obsidian` not found: raise `AdapterUnavailableError`.

Error Semantics
- `AdapterUnavailableError`: requested adapter binary missing.
- `SyncError`: transient sync failure; should be retried twice with exponential backoff by caller.
- `WriteConflictError`: when a target file changed on disk between read→write; adapter should provide merge hints (e.g., `.orig` file) and raise the error.

- Security & Safety
- File writes should be atomic (write to temp file + rename).
- Avoid executing arbitrary shell commands; use subprocess with argument arrays.

Testing & Validation
- Unit tests for adapter behavior using temporary directories and monkeypatching `shutil.which`.
- Integration test: simulate presence/absence of `obsidian` and verify fallback path exercised.

Acceptance Criteria
- `get_vault_sync()` factory implements selection rules and exposes adapter objects that pass an adapter conformance test suite.