"""Example: Basic feature extraction from audio file."""

from audio_analysis import AudioAnalyzer, OutputFormatter

# Initialize analyzer with an audio file
analyzer = AudioAnalyzer('path/to/your/audio.wav')

# Print basic information
print(f"Audio duration: {analyzer.duration:.2f} seconds")
print(f"Sample rate: {analyzer.sr} Hz")
print(f"Total samples: {len(analyzer.y)}")

# Extract all features
print("\nExtracting all features...")
all_features = analyzer.extract_all_features()

# Access specific feature categories
spectral_features = all_features['spectral']
temporal_features = all_features['temporal']
pitch_features = all_features['pitch']

print(f"\nSpectral features extracted: {list(spectral_features.keys())}")
print(f"Temporal features extracted: {list(temporal_features.keys())}")
print(f"Pitch features extracted: {list(pitch_features.keys())}")

# Get summary statistics
summary = analyzer.get_summary_statistics()
print("\nSummary Statistics:")
for feature_name, stats in summary.items():
    print(f"\n{feature_name}:")
    for stat_name, value in stats.items():
        print(f"  {stat_name}: {value:.4f}")

# Save features in different formats
OutputFormatter.save_features(all_features, 'features_all.json', format='json')
OutputFormatter.save_features(summary, 'features_summary.csv', format='csv')
OutputFormatter.save_features(all_features, 'features_all.npz', format='npz')

print("\nFeatures saved to:")
print("  - features_all.json")
print("  - features_summary.csv")
print("  - features_all.npz")
