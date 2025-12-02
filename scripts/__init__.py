"""
WIIL Python SDK - Release Scripts

This package contains automation scripts for building, versioning, and releasing
the WIIL Python SDK.

Available Scripts:
    - commit_script.py: Automated commit and push with build verification
    - tag_script.py: Version bumping, tagging, and release management

Usage:
    python scripts/commit_script.py <branch>
    python scripts/tag_script.py

Requirements:
    - Python 3.8+
    - Git configured with remote origin
    - python-build package installed (pip install build)
"""

__version__ = "1.0.0"
__all__ = []
