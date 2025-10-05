# Examples

This directory contains example scripts demonstrating various uses of the audio-analysis package.

## Files

### 1. `basic_feature_extraction.py`
Demonstrates basic audio feature extraction and output formatting.

**Features shown:**
- Loading audio files
- Extracting all feature types
- Getting summary statistics
- Saving in multiple formats (JSON, CSV, NPZ)

**Usage:**
```bash
python basic_feature_extraction.py
```

### 2. `wavetable_generation.py`
Shows how to generate wavetables from audio for use in synthesizers.

**Features shown:**
- Extracting wavetables from audio
- Creating basic waveforms (sine, saw, square)
- Morphing between wavetables
- Creating custom wavetables from spectra

**Usage:**
```bash
python wavetable_generation.py
```

### 3. `batch_processing.py`
Demonstrates batch processing of multiple audio files.

**Features shown:**
- Processing entire directories of audio files
- Error handling for batch operations
- Organizing output results

**Usage:**
```bash
python batch_processing.py
```

Edit the script to set your input/output directories:
```python
input_dir = 'path/to/audio/files'
output_dir = 'path/to/output/analysis'
batch_analyze(input_dir, output_dir)
```

### 4. `ml_feature_extraction.py`
Advanced example for ML/AI training data preparation.

**Features shown:**
- Aggregating features for machine learning
- Creating training datasets from multiple files
- Organizing features in ML-friendly format
- Exporting to CSV for use with pandas/scikit-learn

**Usage:**
```bash
python ml_feature_extraction.py
```

## Quick Start

To use these examples, you'll need to:

1. Install the package:
```bash
pip install audio-analysis
```

2. Modify the file paths in the examples to point to your audio files

3. Run the examples:
```bash
python examples/basic_feature_extraction.py
```

## Common Use Cases

### Music Classification
Use `ml_feature_extraction.py` to extract features for genre, mood, or instrument classification.

### Audio Search/Similarity
Extract features and use them to compute similarity between audio files for recommendation systems.

### Synthesizer Design
Use `wavetable_generation.py` to create custom wavetables from real instruments or sounds.

### Quality Assessment
Use `basic_feature_extraction.py` to analyze audio quality metrics like RMS energy, spectral centroid, etc.

### Dataset Preparation
Use `batch_processing.py` to process large collections of audio files for research or production.

## Notes

- All examples assume you have audio files to process. You can use any common audio format (WAV, MP3, FLAC, etc.)
- The examples include error handling, but you may want to customize them for your specific needs
- For large-scale processing, consider adding parallel processing or GPU acceleration for feature extraction
