# audio-analysis

A comprehensive Python tool for audio analysis and feature extraction, designed for ML/AI audio processing workflows. Built with `librosa` and supporting multiple output formats, this tool provides advanced feature extraction techniques and wavetable synthesis capabilities.

## Features

- **Multiple Feature Extraction Techniques:**
  - Spectral features (MFCCs, spectral centroid, rolloff, bandwidth, contrast)
  - Chroma features (STFT, CQT, CENS)
  - Temporal features (zero-crossing rate, RMS energy)
  - Harmonic/percussive separation
  - Onset detection
  - Pitch and tempo analysis

- **Wavetable Synthesis:**
  - Extract wavetables from audio for use in synthesizers
  - Support for multiple wavetable stacks
  - Morphing between wavetables
  - Compatible with standard wavetable synthesizers

- **Multiple Output Formats:**
  - JSON (human-readable, full data)
  - CSV (tabular format, summary statistics)
  - NPZ (NumPy compressed, efficient storage)
  - TXT (plain text, readable reports)

- **Command-Line Interface:**
  - Easy-to-use CLI with multiple options
  - Batch processing capabilities
  - Flexible configuration

## Installation

### From PyPI (once published)

```bash
pip install audio-analysis
```

### From Source

```bash
# Clone the repository
git clone https://github.com/edgar-montano/audio-analysis.git
cd audio-analysis

# Install with uv
uv sync

# Or install with pip
pip install -e .
```

## Usage

### Command Line

#### Basic feature extraction:
```bash
# Extract all features to JSON
audio-analysis input.wav -o output.json

# Extract only spectral features
audio-analysis input.wav -f spectral -o features.json

# Get summary statistics in CSV format
audio-analysis input.wav -s --format csv -o summary.csv
```

#### Wavetable generation:
```bash
# Generate 64 wavetables from audio
audio-analysis input.wav -w -o wavetables.wav --num-tables 64

# Generate with custom wavetable size
audio-analysis input.wav -w -o wavetables.wav --table-size 4096
```

#### Advanced options:
```bash
# Extract features with custom sample rate
audio-analysis input.wav --sr 22050 -o features.json

# Extract only temporal features in NPZ format
audio-analysis input.wav -f temporal --format npz -o temporal.npz

# Verbose output
audio-analysis input.wav -v -o output.json
```

### Python API

```python
from audio_analysis import AudioAnalyzer, WavetableSynthesizer, OutputFormatter

# Basic feature extraction
analyzer = AudioAnalyzer('audio.wav')

# Extract specific features
spectral = analyzer.extract_spectral_features()
temporal = analyzer.extract_temporal_features()
pitch = analyzer.extract_pitch_features()

# Get all features at once
all_features = analyzer.extract_all_features()

# Get summary statistics
summary = analyzer.get_summary_statistics()

# Save in different formats
OutputFormatter.save_features(all_features, 'output.json', format='json')
OutputFormatter.save_features(summary, 'summary.csv', format='csv')

# Wavetable synthesis
synthesizer = WavetableSynthesizer(sr=44100)
wavetables = synthesizer.extract_wavetables_from_audio(
    analyzer.y, 
    analyzer.sr,
    num_tables=64,
    wavetable_size=2048
)
synthesizer.save_wavetable(wavetables, 'wavetables.wav')
```

## Feature Descriptions

### Spectral Features
- **MFCCs**: Mel-frequency cepstral coefficients (13 coefficients + deltas)
- **Spectral Centroid**: Center of mass of the spectrum
- **Spectral Rolloff**: Frequency below which 85% of energy is contained
- **Spectral Bandwidth**: Width of the spectrum
- **Spectral Contrast**: Difference between peaks and valleys in spectrum
- **Chroma Features**: Pitch class profiles (STFT, CQT, CENS variants)

### Temporal Features
- **Zero-Crossing Rate**: Rate of signal sign changes
- **RMS Energy**: Root mean square energy
- **Tempo**: Estimated beats per minute
- **Beat Frames**: Detected beat locations

### Other Features
- **Harmonic/Percussive**: Separated components
- **Onsets**: Detected onset events and strength
- **Pitch**: Fundamental frequency tracking

## Use Cases

### ML/AI Audio Processing
- Feature extraction for audio classification models
- Training data preparation for music information retrieval
- Audio embeddings for similarity search
- Preprocessing for generative audio models

### Wavetable Synthesis
- Create custom wavetables from real instruments
- Extract timbral characteristics for synthesis
- Morph between different sounds
- Build wavetable banks for hardware/software synthesizers

### Audio Analysis
- Analyze audio characteristics programmatically
- Batch process large audio datasets
- Generate reports for audio quality assessment
- Educational tool for understanding audio features

## Development

### Setup Development Environment

```bash
# Install development dependencies
uv sync --all-extras

# Run tests (if available)
pytest

# Build package
python -m build
```

### Publishing to PyPI

```bash
# Build distribution
python -m build

# Upload to PyPI (requires credentials)
twine upload dist/*
```

## Requirements

- Python >= 3.9
- librosa >= 0.10.0
- numpy >= 1.24.0
- scipy >= 1.10.0
- soundfile >= 0.12.0

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

Edgar Montano

## Acknowledgments

- Built with [librosa](https://librosa.org/) for audio analysis
- Powered by [uv](https://github.com/astral-sh/uv) for package management
