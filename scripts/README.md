# WIIL Python SDK - Release Scripts

This directory contains automation scripts for managing releases, versioning, and deployments of the WIIL Python SDK.

## Scripts Overview

### 1. `commit_script.py` - Automated Commit & Push

Automates the process of building, committing, and pushing changes with timestamp-based commit messages.

**Features:**
- ✅ Validates uncommitted changes exist
- ✅ Shows preview of changes to be committed
- ✅ Builds project before committing (using `python -m build`)
- ✅ User confirmation before proceeding
- ✅ Automatic timestamp in commit messages
- ✅ Pushes to specified branch

**Usage:**
```bash
python scripts/commit_script.py <branch-name>
```

**Example:**
```bash
python scripts/commit_script.py main
```

**Workflow:**
1. Check for uncommitted changes
2. Display changes for review
3. Request user confirmation
4. Build the project
5. Add all changes
6. Commit with timestamp: `"YYYY-MM-DD HH:MM:SS - pre-release updates"`
7. Push to specified branch

---

### 2. `tag_script.py` - Version Management & Tagging

Automates semantic versioning, tagging, and release preparation following Python packaging standards.

**Features:**
- ✅ Reads version from `pyproject.toml`
- ✅ Interactive version bump selection (patch/minor/major/custom)
- ✅ Semantic versioning validation
- ✅ Documentation generation (if configured)
- ✅ Automated building and testing
- ✅ Git tag creation and pushing
- ✅ Version update in `pyproject.toml`

**Usage:**
```bash
python scripts/tag_script.py
```

**Interactive Prompts:**
```
Select version bump type:
1) Patch (0.0.0 -> 0.0.1) - Bug fixes, small changes
2) Minor (0.0.0 -> 0.1.0) - New features, backwards compatible
3) Major (0.0.0 -> 1.0.0) - Breaking changes
4) Custom version

Choose (1-4):
```

**Workflow:**
1. Load current version from `pyproject.toml`
2. Display repository information
3. Prompt for version bump type
4. Calculate new version
5. Request user confirmation
6. Generate documentation (if configured)
7. Build the project
8. Commit any pending changes
9. Update version in `pyproject.toml`
10. Commit version bump: `"chore: bump <package> to v<version>"`
11. Create git tag `v<version>`
12. Push changes and tag to `main` branch

---

## Prerequisites

### System Requirements

- **Python 3.8+**
- **Git** configured with remote origin
- **Build tools** installed:
  ```bash
  pip install build
  ```

### Optional Dependencies

For documentation generation:
```bash
pip install sphinx  # or pdoc3
```

---

## Installation

The scripts are standalone and don't require installation. However, ensure you have the build tool:

```bash
# Install build tool
pip install build

# Or install all dev dependencies
pip install -e ".[dev]"
```

---

## Configuration

### `pyproject.toml` Requirements

The scripts expect a properly configured `pyproject.toml` file with:

```toml
[project]
name = "wiil"
version = "0.0.0"  # This will be updated by tag_script.py
```

### Git Configuration

Ensure your repository has:
- A configured `origin` remote
- Proper authentication for pushing
- A `main` branch (or adjust scripts for your default branch)

---

## Comparison with TypeScript Scripts

| Feature | TypeScript (Bash) | Python |
|---------|-------------------|--------|
| **Language** | Bash + Node.js | Pure Python |
| **Config File** | `package.json` | `pyproject.toml` |
| **Build Command** | `npm run build` | `python -m build` |
| **Version Tool** | `npm version` | Manual `pyproject.toml` update |
| **Docs Command** | `npm run docs` | `make html` (Sphinx) or skip |
| **Dependencies** | Node.js, npm, semver | Python 3.8+, build |

---

## Error Handling

Both scripts include comprehensive error handling:

### Common Errors

**1. No Changes to Commit**
```
⚠️  No changes to commit
```
*Solution:* Make changes before running commit script.

**2. Build Failure**
```
❌ Build failed:
[error details]
```
*Solution:* Fix build errors before proceeding.

**3. Git Push Failure**
```
❌ Failed to push:
[error details]
```
*Solution:* Check git authentication and network connection.

**4. Invalid Version Format**
```
❌ Invalid version format. Use semantic versioning (x.y.z)
```
*Solution:* Enter version in format: `1.2.3`

---

## Best Practices

### Before Running Scripts

1. **Test your changes:**
   ```bash
   pytest
   ```

2. **Check code quality:**
   ```bash
   ruff check .
   black --check .
   mypy wiil
   ```

3. **Review changes:**
   ```bash
   git status
   git diff
   ```

### Version Bumping Strategy

- **Patch (0.0.X):** Bug fixes, documentation updates, minor improvements
- **Minor (0.X.0):** New features, non-breaking changes, new APIs
- **Major (X.0.0):** Breaking changes, major refactors, incompatible API changes

---

## Examples

### Example 1: Quick Commit and Push

```bash
# Make changes to code
# ...

# Commit and push
python scripts/commit_script.py main
```

**Output:**
```
📝 Committing and pushing to branch: main
🕒 Timestamp: 2025-12-02 14:30:00

📋 Changes to be committed:
 M wiil/client/http_client.py
 M wiil/models/service_mgt/agent_config.py

Proceed with commit and push? (y/N): y
🔨 Building project...
✅ Build completed successfully
📦 Adding all changes...
💾 Committing changes...
🚀 Pushing to origin/main...

✅ Successfully committed and pushed to main
🔗 Commit message: '2025-12-02 14:30:00 - pre-release updates'
```

### Example 2: Minor Version Bump

```bash
python scripts/tag_script.py
```

**Output:**
```
📦 Package: wiil
📦 Current version: 0.1.0
🔗 Repository: wiil-io/wiil-python

Select version bump type:
1) Patch (0.1.0 -> 0.1.1) - Bug fixes, small changes
2) Minor (0.1.0 -> 0.2.0) - New features, backwards compatible
3) Major (0.1.0 -> 1.0.0) - Breaking changes
4) Custom version

Choose (1-4): 2
🆕 New version will be: 0.2.0

Build, commit, and push tag v0.2.0? (y/N): y
📚 Generating documentation...
✅ Documentation generated successfully
🔨 Building project...
✅ Build completed successfully
📦 Adding all changes...
📝 Updating pyproject.toml to v0.2.0...
🏷️  Creating tag v0.2.0...
🚀 Pushing changes and tag...

✅ Successfully tagged and pushed v0.2.0
```

---

## Troubleshooting

### Script Not Executable

If you get a permission error:
```bash
chmod +x scripts/commit_script.py
chmod +x scripts/tag_script.py
```

Or always use:
```bash
python scripts/commit_script.py <args>
```

### Build Module Not Found

```bash
pip install build
```

### Git Authentication Issues

Ensure your SSH keys or HTTPS credentials are configured:
```bash
git config --list
```

---

## Contributing

When modifying these scripts:

1. Maintain Python 3.8+ compatibility
2. Follow PEP 8 style guidelines
3. Add comprehensive error handling
4. Update this README with new features
5. Test on multiple platforms (Linux, macOS, Windows)

---

## License

MIT License - Same as WIIL Python SDK

---

## Support

For issues or questions:
- GitHub Issues: https://github.com/wiil-io/wiil-python/issues
- Documentation: https://docs.wiil.io
