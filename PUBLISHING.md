# Publishing to PyPI

This guide explains how to build and publish the audio-analysis package to PyPI.

## Prerequisites

1. Create accounts:
   - [PyPI](https://pypi.org/account/register/) - for production releases
   - [TestPyPI](https://test.pypi.org/account/register/) - for testing

2. Install required tools:
```bash
pip install --upgrade build twine
```

## Building the Package

1. Ensure version is updated in `pyproject.toml`:
```toml
[project]
name = "audio-analysis"
version = "0.1.0"  # Update this for each release
```

2. Build the distribution packages:
```bash
python -m build
```

This creates two files in the `dist/` directory:
- A source distribution (`audio-analysis-0.1.0.tar.gz`)
- A wheel (`audio_analysis-0.1.0-py3-none-any.whl`)

## Testing the Package (Recommended)

### Option 1: Test Installation Locally

```bash
# Install in editable mode
pip install -e .

# Test the CLI
audio-analysis --help

# Test the Python API
python -c "from audio_analysis import AudioAnalyzer; print('OK')"
```

### Option 2: Upload to TestPyPI

```bash
# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ audio-analysis

# Test it
audio-analysis --help
```

## Publishing to PyPI

### Using Twine (Recommended)

1. Upload the package:
```bash
twine upload dist/*
```

2. Enter your PyPI credentials when prompted

3. Verify the upload at https://pypi.org/project/audio-analysis/

### Using GitHub Actions (Automated)

Create `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.x'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    
    - name: Build package
      run: python -m build
    
    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: twine upload dist/*
```

Then create a GitHub release and the package will be automatically published.

## API Token Authentication (Recommended)

Instead of using username/password, use API tokens:

1. Go to PyPI Account Settings → API Tokens
2. Create a new token with appropriate scope
3. Use the token for authentication:

```bash
twine upload --username __token__ --password pypi-YOUR-API-TOKEN dist/*
```

Or set environment variables:
```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-YOUR-API-TOKEN
twine upload dist/*
```

## Version Management

Follow semantic versioning (MAJOR.MINOR.PATCH):

- **MAJOR**: Incompatible API changes
- **MINOR**: New functionality (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

Example:
- `0.1.0` - Initial release
- `0.1.1` - Bug fix
- `0.2.0` - New feature added
- `1.0.0` - Stable API

## Release Checklist

Before each release:

- [ ] Update version number in `pyproject.toml`
- [ ] Update CHANGELOG.md (if exists)
- [ ] Run tests
- [ ] Build the package (`python -m build`)
- [ ] Test installation locally
- [ ] (Optional) Upload to TestPyPI and test
- [ ] Create a git tag: `git tag v0.1.0`
- [ ] Push tag: `git push origin v0.1.0`
- [ ] Upload to PyPI: `twine upload dist/*`
- [ ] Create GitHub release

## Troubleshooting

### "File already exists" error

PyPI doesn't allow overwriting existing versions. You must:
1. Increment the version number
2. Rebuild the package
3. Upload the new version

### Import errors after installation

Ensure the package structure is correct:
```
src/
  audio_analysis/
    __init__.py
    analyzer.py
    ...
```

### Missing dependencies

All dependencies should be listed in `pyproject.toml` under `dependencies`.

## Resources

- [Python Packaging Guide](https://packaging.python.org/)
- [Twine Documentation](https://twine.readthedocs.io/)
- [PyPI Help](https://pypi.org/help/)
- [TestPyPI](https://test.pypi.org/)
