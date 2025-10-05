# Contributing to audio-analysis

Thank you for your interest in contributing to audio-analysis! This document provides guidelines and instructions for contributing.

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/edgar-montano/audio-analysis.git
cd audio-analysis
```

2. Install uv (if not already installed):
```bash
pip install uv
```

3. Create a virtual environment and install dependencies:
```bash
uv sync
```

4. Activate the virtual environment:
```bash
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate  # On Windows
```

## Development Workflow

### Running Tests

Currently, the project doesn't have a test suite. If you'd like to contribute tests:

```bash
# Install pytest
uv add pytest --dev

# Run tests
pytest
```

### Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Write clear docstrings for all public functions and classes
- Keep functions focused and modular

### Making Changes

1. Create a new branch for your feature or bugfix:
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes and test them:
```bash
# Test CLI functionality
audio-analysis test_audio.wav -v

# Test Python API
python -c "from audio_analysis import AudioAnalyzer; print(AudioAnalyzer.__doc__)"
```

3. Commit your changes with clear commit messages:
```bash
git add .
git commit -m "Add feature: description of your changes"
```

4. Push your branch and create a pull request:
```bash
git push origin feature/your-feature-name
```

## Areas for Contribution

### High Priority
- Unit tests for all modules
- Integration tests for CLI
- Performance optimizations
- Additional audio features
- Support for more audio formats

### Documentation
- More example scripts
- Tutorial notebooks
- API reference documentation
- Video tutorials

### Features
- Real-time audio processing
- GPU acceleration for feature extraction
- Additional wavetable synthesis methods
- Support for streaming audio
- Audio augmentation techniques

### Bug Fixes
- Report bugs via GitHub Issues
- Include minimal reproduction steps
- Specify your environment (OS, Python version, etc.)

## Pull Request Process

1. Ensure your code follows the project's style guidelines
2. Update documentation if you're adding new features
3. Add your changes to the appropriate section in README.md
4. Ensure all tests pass (when test suite exists)
5. Request review from maintainers

## Code Review

All submissions require review. We use GitHub pull requests for this purpose. Reviewers will look for:

- Code quality and style
- Test coverage
- Documentation completeness
- Performance considerations
- Backward compatibility

## Questions?

Feel free to open an issue on GitHub if you have questions or need clarification on anything.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
