"""Git integration: branch creation, commits, history, merges.

Manages feature branch workflow and commit tracking.
"""

import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional


class GitManager:
    """Git workflow management."""

    def __init__(self, project_path: str = "."):
        self.project_path = Path(project_path)

    def check_clean(self) -> Dict[str, Any]:
        """Check if working directory is clean.

        Returns:
            Dict with clean status and details
        """
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True,
                cwd=self.project_path,
                timeout=10
            )
            clean = result.returncode == 0 and not result.stdout.strip()
            changes = result.stdout if not clean else ""

            return {
                "clean": clean,
                "changes": changes,
                "message": "Working directory clean" if clean else f"Uncommitted: {len(changes.split(chr(10)))} files"
            }
        except Exception as e:
            return {"clean": False, "error": str(e)}

    def create_branch(self, feature_name: str, base: str = "main") -> Dict[str, Any]:
        """Create feature branch.

        Args:
            feature_name: Feature name
            base: Base branch (default: main)

        Returns:
            Dict with branch creation result
        """
        # Sanitize branch name
        branch_name = f"feature/{feature_name.lower().replace(' ', '-')}"

        try:
            # Fetch latest
            subprocess.run(
                ["git", "fetch", "origin", base],
                capture_output=True,
                cwd=self.project_path,
                timeout=30
            )

            # Create branch
            result = subprocess.run(
                ["git", "checkout", "-b", branch_name, f"origin/{base}"],
                capture_output=True,
                text=True,
                cwd=self.project_path,
                timeout=10
            )

            if result.returncode == 0:
                return {
                    "success": True,
                    "branch": branch_name,
                    "base": base,
                    "message": f"Created branch {branch_name}"
                }
            else:
                return {
                    "success": False,
                    "error": result.stderr or result.stdout
                }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def commit(self, message: str, scope: str = "feature") -> Dict[str, Any]:
        """Commit staged changes.

        Args:
            message: Commit message
            scope: Scope (feature, docs, test, etc.)

        Returns:
            Dict with commit result
        """
        full_message = f"{scope}: {message}\n\nCo-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>"

        try:
            # Stage all changes
            subprocess.run(
                ["git", "add", "-A"],
                capture_output=True,
                cwd=self.project_path,
                timeout=10
            )

            # Commit
            result = subprocess.run(
                ["git", "commit", "-m", full_message],
                capture_output=True,
                text=True,
                cwd=self.project_path,
                timeout=10
            )

            if result.returncode == 0:
                return {
                    "success": True,
                    "message": message,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "success": False,
                    "error": result.stderr or "No changes to commit"
                }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_history(self, feature_name: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get commit history for feature.

        Args:
            feature_name: Feature name or branch
            limit: Number of commits to show

        Returns:
            List of commit dicts
        """
        try:
            result = subprocess.run(
                ["git", "log", "--oneline", f"-{limit}", feature_name],
                capture_output=True,
                text=True,
                cwd=self.project_path,
                timeout=10
            )

            commits = []
            for line in result.stdout.strip().split("\n"):
                if not line:
                    continue
                parts = line.split(" ", 1)
                if len(parts) == 2:
                    commits.append({
                        "hash": parts[0],
                        "message": parts[1]
                    })

            return commits
        except Exception as e:
            return []

    def merge(self, feature_branch: str, target: str = "main", strategy: str = "squash") -> Dict[str, Any]:
        """Merge feature branch to target.

        Args:
            feature_branch: Feature branch name
            target: Target branch (default: main)
            strategy: Merge strategy (squash, merge, rebase)

        Returns:
            Dict with merge result
        """
        try:
            # Switch to target
            subprocess.run(
                ["git", "checkout", target],
                capture_output=True,
                cwd=self.project_path,
                timeout=10
            )

            # Pull latest
            subprocess.run(
                ["git", "pull"],
                capture_output=True,
                cwd=self.project_path,
                timeout=30
            )

            # Merge
            merge_args = ["git", "merge"]
            if strategy == "squash":
                merge_args.append("--squash")
            elif strategy == "rebase":
                merge_args.append("--rebase")

            merge_args.append(feature_branch)

            result = subprocess.run(
                merge_args,
                capture_output=True,
                text=True,
                cwd=self.project_path,
                timeout=30
            )

            if result.returncode == 0:
                return {
                    "success": True,
                    "feature_branch": feature_branch,
                    "target": target,
                    "strategy": strategy
                }
            else:
                return {
                    "success": False,
                    "error": result.stderr or "Merge failed",
                    "conflicts": "CONFLICT" in result.stdout
                }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_current_branch(self) -> str:
        """Get current branch name.

        Returns:
            Branch name or "unknown"
        """
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                capture_output=True,
                text=True,
                cwd=self.project_path,
                timeout=10
            )
            return result.stdout.strip() if result.returncode == 0 else "unknown"
        except Exception:
            return "unknown"
