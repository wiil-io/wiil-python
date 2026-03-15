#!/usr/bin/env python3
"""
Package tagging script for WIIL Python SDK.

This script automates version bumping, building, and tagging for Python package releases.
It follows semantic versioning and integrates with pyproject.toml.

Usage:
    python scripts/tag_script.py

The script will interactively prompt for:
    - Version bump type (patch/minor/major/custom)
    - Confirmation before proceeding
"""

import re
import subprocess
import sys
import tomllib
from datetime import datetime
from pathlib import Path
from typing import Literal


def run_command(cmd: list[str], cwd: Path | None = None) -> tuple[int, str, str]:
    """Execute a shell command and return exit code, stdout, stderr."""
    result = subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=True,
        text=True
    )
    return result.returncode, result.stdout, result.stderr


def load_pyproject_toml(project_root: Path) -> dict:
    """Load and parse pyproject.toml file."""
    pyproject_path = project_root / "pyproject.toml"
    if not pyproject_path.exists():
        raise FileNotFoundError(f"pyproject.toml not found at {pyproject_path}")

    with open(pyproject_path, "rb") as f:
        return tomllib.load(f)


def get_package_info(config: dict) -> tuple[str, str]:
    """Extract package name and current version from pyproject.toml."""
    try:
        name = config["project"]["name"]
        version = config["project"]["version"]
        return name, version
    except KeyError as e:
        raise ValueError(f"Missing required field in pyproject.toml: {e}")


def get_git_info() -> tuple[str, str]:
    """Get git repository information."""
    # Get remote URL
    returncode, repo_url, _ = run_command(["git", "remote", "get-url", "origin"])
    if returncode != 0:
        raise RuntimeError("Failed to get git remote URL")

    # Extract repository name from URL
    # Handles both HTTPS and SSH formats
    match = re.search(r"github\.com[:/](.+?)(?:\.git)?$", repo_url.strip())
    if not match:
        raise ValueError(f"Could not parse repository name from: {repo_url}")

    repo_name = match.group(1)
    return repo_url.strip(), repo_name


def bump_version(
    current: str,
    bump_type: Literal["patch", "minor", "major"]
) -> str:
    """Calculate new version based on bump type."""
    parts = list(map(int, current.split(".")))
    if len(parts) != 3:
        raise ValueError(f"Invalid version format: {current}")

    if bump_type == "patch":
        parts[2] += 1
    elif bump_type == "minor":
        parts[1] += 1
        parts[2] = 0
    elif bump_type == "major":
        parts[0] += 1
        parts[1] = 0
        parts[2] = 0

    return ".".join(map(str, parts))


def validate_version_format(version: str) -> bool:
    """Validate semantic version format (x.y.z)."""
    return bool(re.match(r"^\d+\.\d+\.\d+$", version))


def update_pyproject_version(project_root: Path, new_version: str) -> None:
    """Update version in pyproject.toml file."""
    pyproject_path = project_root / "pyproject.toml"

    with open(pyproject_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace version line in [project] section
    pattern = r'(version\s*=\s*)"[^"]*"'
    replacement = rf'\1"{new_version}"'
    new_content = re.sub(pattern, replacement, content)

    with open(pyproject_path, "w", encoding="utf-8") as f:
        f.write(new_content)


def check_pending_changes() -> bool:
    """Check if there are staged but uncommitted changes."""
    returncode, _, _ = run_command(["git", "diff-index", "--quiet", "--cached", "HEAD", "--"])
    return returncode != 0


def build_project(project_root: Path) -> bool:
    """Build the Python project."""
    print("🔨 Building project...")
    # Prefer uv build in this repository workflow.
    returncode, stdout, stderr = run_command(["uv", "build"], cwd=project_root)

    # Fallback for environments without uv.
    if returncode != 0:
        fallback_code, fallback_stdout, fallback_stderr = run_command(
            ["python", "-m", "build"],
            cwd=project_root
        )
        if fallback_code != 0:
            print(f"❌ Build failed with uv build:\n{stderr}")
            print(f"❌ Build failed with python -m build:\n{fallback_stderr}")
            return False

        stdout = fallback_stdout

    print("✅ Build completed successfully")
    return True


def confirm_action(prompt: str) -> bool:
    """Prompt user for confirmation."""
    while True:
        response = input(f"{prompt} (y/N): ").strip().lower()
        if response in ["y", "yes"]:
            return True
        elif response in ["n", "no", ""]:
            return False
        print("Please answer 'y' or 'n'")


def main() -> int:
    """Main script execution."""
    try:
        project_root = Path(__file__).parent.parent

        # Load package configuration
        print("📦 Loading package configuration...")
        config = load_pyproject_toml(project_root)
        package_name, current_version = get_package_info(config)
        repo_url, repo_name = get_git_info()

        print(f"📦 Package: {package_name}")
        print(f"📦 Current version: {current_version}")
        print(f"🔗 Repository: {repo_name}")
        print()

        # Choose version bump type
        print("Select version bump type:")
        print(f"1) Patch ({current_version} -> patch) - Bug fixes, small changes")
        print(f"2) Minor ({current_version} -> minor) - New features, backwards compatible")
        print(f"3) Major ({current_version} -> major) - Breaking changes")
        print("4) Custom version")
        print()

        choice = input("Choose (1-4): ").strip()

        if choice == "1":
            new_version = bump_version(current_version, "patch")
        elif choice == "2":
            new_version = bump_version(current_version, "minor")
        elif choice == "3":
            new_version = bump_version(current_version, "major")
        elif choice == "4":
            custom_version = input("Enter custom version (e.g., 2.1.0): ").strip()
            if not validate_version_format(custom_version):
                print("❌ Invalid version format. Use semantic versioning (x.y.z)")
                return 1
            new_version = custom_version
        else:
            print("❌ Invalid choice")
            return 1

        print(f"🆕 New version will be: {new_version}")
        print()

        # Confirm
        if not confirm_action(f"Build, commit, and push tag v{new_version}?"):
            print("❌ Cancelled")
            return 1

        # Build the project
        if not build_project(project_root):
            print("❌ Cannot proceed without successful build")
            return 1

        # Add all changes (including any uncommitted changes)
        print("📦 Adding all changes...")
        returncode, _, stderr = run_command(["git", "add", "."])
        if returncode != 0:
            print(f"❌ Failed to add changes:\n{stderr}")
            return 1

        # Commit pending changes if they exist
        if check_pending_changes():
            current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print("💾 Committing pending changes...")
            commit_msg = f"{current_date} - release updates"
            returncode, _, stderr = run_command(["git", "commit", "-m", commit_msg])
            if returncode != 0:
                print(f"❌ Failed to commit:\n{stderr}")
                return 1

        # Update pyproject.toml version
        print(f"📝 Updating pyproject.toml to v{new_version}...")
        update_pyproject_version(project_root, new_version)

        # Commit version bump
        returncode, _, stderr = run_command(["git", "add", "pyproject.toml"])
        if returncode != 0:
            print(f"❌ Failed to add pyproject.toml:\n{stderr}")
            return 1

        version_commit_msg = f"chore: bump {package_name} to v{new_version}"
        returncode, _, stderr = run_command(["git", "commit", "-m", version_commit_msg])
        if returncode != 0:
            print(f"❌ Failed to commit version bump:\n{stderr}")
            return 1

        # Create and push tag
        print(f"🏷️  Creating tag v{new_version}...")
        returncode, _, stderr = run_command(["git", "tag", f"v{new_version}"])
        if returncode != 0:
            print(f"❌ Failed to create tag:\n{stderr}")
            return 1

        print("🚀 Pushing changes and tag...")
        returncode, _, stderr = run_command(["git", "push", "origin", "main"])
        if returncode != 0:
            print(f"❌ Failed to push changes:\n{stderr}")
            return 1

        returncode, _, stderr = run_command(["git", "push", "origin", f"v{new_version}"])
        if returncode != 0:
            print(f"❌ Failed to push tag:\n{stderr}")
            return 1

        print()
        print(f"✅ Successfully tagged and pushed v{new_version}")

        return 0

    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
