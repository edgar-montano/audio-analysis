# Quick Start Guide

Get started with audio-analysis in minutes!

## Installation

```bash
pip install audio-analysis
```

Or install from source:
```bash
git clone https://github.com/edgar-montano/audio-analysis.git
cd audio-analysis
uv sync
```

## 5-Minute Tutorial

### 1. Extract Features from Audio

```bash
# Analyze an audio file and save features to JSON
audio-analysis my_song.wav -o features.json

# Get summary statistics in CSV format
audio-analysis my_song.wav -s --format csv -o summary.csv

# Extract only spectral features
audio-analysis my_song.wav -f spectral -o spectral.json
```

### 2. Generate Wavetables

```bash
# Create wavetables for synthesizers
audio-analysis my_sound.wav -w -o wavetables.wav --num-tables 64

# Generate fewer, larger wavetables
audio-analysis my_sound.wav -w -o wavetables.wav --num-tables 32 --table-size 4096
```

### 3. Python API

```python
from audio_analysis import AudioAnalyzer, OutputFormatter

# Load and analyze audio
analyzer = AudioAnalyzer('audio.wav')

# Get summary statistics
summary = analyzer.get_summary_statistics()
print(f"Tempo: {summary['tempo']['value']} BPM")
print(f"Mean pitch: {summary['pitch']['mean']:.2f} Hz")

# Extract all features
features = analyzer.extract_all_features()

# Save results
OutputFormatter.save_features(features, 'output.json')
```

## Common Use Cases

### Music Analysis

```python
from audio_analysis import AudioAnalyzer

analyzer = AudioAnalyzer('song.mp3')

# Get tempo and beats
temporal = analyzer.extract_temporal_features()
print(f"Tempo: {temporal['tempo'][0]} BPM")

# Analyze harmony
spectral = analyzer.extract_spectral_features()
chroma = spectral['chroma_stft']  # Pitch class distribution
```

### Sound Design with Wavetables

```python
from audio_analysis import AudioAnalyzer, WavetableSynthesizer

# Analyze source audio
analyzer = AudioAnalyzer('vocal.wav')

# Create wavetables
synth = WavetableSynthesizer(sr=analyzer.sr)
wavetables = synth.extract_wavetables_from_audio(
    analyzer.y, 
    analyzer.sr,
    num_tables=64
)

# Save for use in Serum, Vital, etc.
synth.save_wavetable(wavetables, 'vocal_wavetables.wav')
```

### Batch Processing for ML

```python
from pathlib import Path
from audio_analysis import AudioAnalyzer, OutputFormatter

audio_dir = Path('dataset/audio')
output_dir = Path('dataset/features')
output_dir.mkdir(exist_ok=True)

for audio_file in audio_dir.glob('*.wav'):
    analyzer = AudioAnalyzer(str(audio_file))
    features = analyzer.get_summary_statistics()
    
    output_path = output_dir / f"{audio_file.stem}.json"
    OutputFormatter.save_features(features, str(output_path))
```

## Command-Line Reference

### Basic Commands

```bash
# Show help
audio-analysis --help

# Analyze with default settings (JSON output)
audio-analysis input.wav

# Specify output file
audio-analysis input.wav -o output.json

# Enable verbose output
audio-analysis input.wav -v
```

### Feature Types

```bash
# All features (default)
audio-analysis input.wav -f all

# Only spectral features
audio-analysis input.wav -f spectral

# Only temporal features  
audio-analysis input.wav -f temporal

# Only pitch features
audio-analysis input.wav -f pitch

# Harmonic/percussive separation
audio-analysis input.wav -f harmonic

# Onset detection
audio-analysis input.wav -f onsets
```

### Output Formats

```bash
# JSON (default, full data)
audio-analysis input.wav --format json

# CSV (tabular format)
audio-analysis input.wav --format csv

# NPZ (NumPy compressed)
audio-analysis input.wav --format npz

# TXT (human-readable)
audio-analysis input.wav --format txt
```

### Wavetable Options

```bash
# Generate wavetables
audio-analysis input.wav -w -o output.wav

# Set number of wavetables
audio-analysis input.wav -w --num-tables 32

# Set wavetable size (must be power of 2)
audio-analysis input.wav -w --table-size 4096

# Custom sample rate
audio-analysis input.wav -w --sr 48000
```

## Python API Reference

### AudioAnalyzer

```python
analyzer = AudioAnalyzer('audio.wav', sr=None)  # sr=None uses native rate

# Feature extraction methods
analyzer.extract_spectral_features()     # MFCCs, centroid, etc.
analyzer.extract_temporal_features()     # ZCR, RMS, tempo
analyzer.extract_pitch_features()        # F0 estimation
analyzer.extract_harmonic_percussive()   # HPSS
analyzer.detect_onsets()                 # Onset detection
analyzer.extract_all_features()          # Everything
analyzer.get_summary_statistics()        # Aggregated stats
```

### WavetableSynthesizer

```python
synth = WavetableSynthesizer(sr=44100)

# Extract from audio
wavetables = synth.extract_wavetables_from_audio(audio, sr, num_tables=64)

# Generate basic waveforms
sine = synth.generate_sine_wavetable(2048)
saw = synth.generate_saw_wavetable(2048)
square = synth.generate_square_wavetable(2048)

# Morph between wavetables
morphed = synth.morph_wavetables(sine, saw, num_steps=16)

# Save wavetables
synth.save_wavetable(wavetables, 'output.wav')
```

### OutputFormatter

```python
# Save in different formats
OutputFormatter.save_features(features, 'output', format='json')
OutputFormatter.save_features(features, 'output', format='csv')
OutputFormatter.save_features(features, 'output', format='npz')
OutputFormatter.save_features(features, 'output', format='txt')
```

## Next Steps

- Check out the [examples](examples/) directory for more detailed examples
- Read the [README](README.md) for comprehensive documentation
- See [CONTRIBUTING](CONTRIBUTING.md) to contribute to the project
- Visit the [GitHub repository](https://github.com/edgar-montano/audio-analysis) for latest updates

## Troubleshooting

### Import Error

```bash
pip install --upgrade audio-analysis
```

### Audio Loading Error

Make sure you have a supported audio file (WAV, MP3, FLAC, OGG, etc.)

### Memory Issues

For large files, consider:
- Using a lower sample rate: `--sr 22050`
- Processing in chunks
- Using summary statistics instead of full features: `-s`

### Permission Errors

Make sure you have write permissions for the output directory.

## Support

- GitHub Issues: https://github.com/edgar-montano/audio-analysis/issues
- Documentation: https://github.com/edgar-montano/audio-analysis
