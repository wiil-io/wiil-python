"""Setup script for WIIL Python SDK."""
from setuptools import find_packages, setup

# Keep metadata in pyproject.toml while forcing reliable package discovery.
setup(
	packages=find_packages(include=["wiil", "wiil.*"]),
	package_data={"wiil": ["py.typed"]},
)
