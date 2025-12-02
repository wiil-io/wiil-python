#!/usr/bin/env python3
"""
Simple commit and push script for WIIL Python SDK.

This script automates the process of building, committing, and pushing changes
to a specified branch with timestamp-based commit messages.

Usage:
    python scripts/commit_script.py <branch-name>

Example:
    python scripts/commit_script.py main
"""

import subprocess
import sys
from datetime import datetime
from pathlib import Path


def run_command(cmd: list[str], cwd: Path | None = None) -> tuple[int, str, str]:
    """Execute a shell command and return exit code, stdout, stderr."""
    result = subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=True,
        text=True
    )
    return result.returncode, result.stdout, result.stderr


def check_git_changes() -> bool:
    """Check if there are uncommitted changes in the repository."""
    returncode, stdout, _ = run_command(["git", "diff-index", "--quiet", "HEAD", "--"])
    return returncode != 0


def show_changes() -> str:
    """Get porcelain status of git changes."""
    _, stdout, _ = run_command(["git", "status", "--porcelain"])
    return stdout


def confirm_action(prompt: str) -> bool:
    """Prompt user for confirmation."""
    while True:
        response = input(f"{prompt} (y/N): ").strip().lower()
        if response in ["y", "yes"]:
            return True
        elif response in ["n", "no", ""]:
            return False
        print("Please answer 'y' or 'n'")


def build_project(project_root: Path) -> bool:
    """Build the Python project using build tool."""
    print("🔨 Building project...")
    returncode, stdout, stderr = run_command(
        ["python", "-m", "build"],
        cwd=project_root
    )

    if returncode != 0:
        print(f"❌ Build failed:\n{stderr}")
        return False

    print("✅ Build completed successfully")
    return True


def main() -> int:
    """Main script execution."""
    # Check if branch argument is provided
    if len(sys.argv) < 2:
        print("❌ Error: Branch name is required")
        print(f"Usage: {sys.argv[0]} <branch-name>")
        print(f"Example: {sys.argv[0]} main")
        return 1

    branch = sys.argv[1]
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    project_root = Path(__file__).parent.parent

    print(f"📝 Committing and pushing to branch: {branch}")
    print(f"🕒 Timestamp: {current_date}")
    print()

    # Check if there are any changes to commit
    if not check_git_changes():
        print("⚠️  No changes to commit")
        return 0

    # Show what will be committed
    print("📋 Changes to be committed:")
    changes = show_changes()
    print(changes)
    print()

    # Confirm before proceeding
    if not confirm_action("Proceed with commit and push?"):
        print("❌ Cancelled")
        return 1

    # Build the project first
    if not build_project(project_root):
        print("❌ Cannot proceed without successful build")
        return 1

    # Add all changes
    print("📦 Adding all changes...")
    returncode, _, stderr = run_command(["git", "add", "."])
    if returncode != 0:
        print(f"❌ Failed to add changes:\n{stderr}")
        return 1

    # Commit with timestamp
    print("💾 Committing changes...")
    commit_message = f"{current_date} - pre-release updates"
    returncode, _, stderr = run_command(["git", "commit", "-m", commit_message])
    if returncode != 0:
        print(f"❌ Failed to commit:\n{stderr}")
        return 1

    # Push to specified branch
    print(f"🚀 Pushing to origin/{branch}...")
    returncode, _, stderr = run_command(["git", "push", "origin", branch])
    if returncode != 0:
        print(f"❌ Failed to push:\n{stderr}")
        return 1

    print()
    print(f"✅ Successfully committed and pushed to {branch}")
    print(f"🔗 Commit message: '{commit_message}'")

    return 0


if __name__ == "__main__":
    sys.exit(main())
