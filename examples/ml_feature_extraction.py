"""Example: Advanced feature extraction for ML/AI training data preparation."""

import numpy as np
from audio_analysis import AudioAnalyzer, OutputFormatter

def extract_ml_features(audio_path, frame_length=2048, hop_length=512):
    """
    Extract features suitable for machine learning models.
    
    Returns a dictionary with features organized for ML pipelines.
    """
    analyzer = AudioAnalyzer(audio_path)
    
    # Extract all features
    spectral = analyzer.extract_spectral_features()
    temporal = analyzer.extract_temporal_features()
    pitch = analyzer.extract_pitch_features()
    
    # Organize features for ML
    ml_features = {}
    
    # Aggregate spectral features (mean and std over time)
    for feature_name, feature_data in spectral.items():
        ml_features[f'{feature_name}_mean'] = np.mean(feature_data, axis=-1)
        ml_features[f'{feature_name}_std'] = np.std(feature_data, axis=-1)
        ml_features[f'{feature_name}_max'] = np.max(feature_data, axis=-1)
        ml_features[f'{feature_name}_min'] = np.min(feature_data, axis=-1)
    
    # Aggregate temporal features
    for feature_name, feature_data in temporal.items():
        if feature_name == 'beat_frames':
            # Special handling for beat frames
            ml_features['num_beats'] = len(feature_data)
            continue
        if feature_name == 'tempo':
            ml_features['tempo'] = feature_data[0]
            continue
        ml_features[f'{feature_name}_mean'] = np.mean(feature_data)
        ml_features[f'{feature_name}_std'] = np.std(feature_data)
    
    # Aggregate pitch features
    pitch_track = pitch['pitch_track']
    non_zero_pitches = pitch_track[pitch_track > 0]
    if len(non_zero_pitches) > 0:
        ml_features['pitch_mean'] = np.mean(non_zero_pitches)
        ml_features['pitch_std'] = np.std(non_zero_pitches)
        ml_features['pitch_range'] = np.max(non_zero_pitches) - np.min(non_zero_pitches)
        ml_features['pitch_presence'] = len(non_zero_pitches) / len(pitch_track)
    
    return ml_features

def create_training_dataset(audio_files, output_file):
    """
    Create a training dataset from multiple audio files.
    
    Args:
        audio_files: List of audio file paths
        output_file: Output file path for the dataset
    """
    import pandas as pd
    
    all_features = []
    
    print(f"Processing {len(audio_files)} files for ML dataset...")
    
    for i, audio_file in enumerate(audio_files, 1):
        try:
            print(f"  [{i}/{len(audio_files)}] Processing: {audio_file}")
            
            features = extract_ml_features(audio_file)
            features['filename'] = audio_file
            all_features.append(features)
            
        except Exception as e:
            print(f"    Error: {e}")
            continue
    
    # Create DataFrame
    df = pd.DataFrame(all_features)
    
    # Save to CSV
    df.to_csv(output_file, index=False)
    print(f"\nDataset saved to: {output_file}")
    print(f"Shape: {df.shape}")
    print(f"\nFeatures extracted: {len(df.columns) - 1}")  # -1 for filename column
    
    return df

if __name__ == '__main__':
    # Example: Extract features from a single file
    print("Example 1: Single file feature extraction")
    features = extract_ml_features('path/to/audio.wav')
    print(f"Extracted {len(features)} features")
    print("\nSample features:")
    for key, value in list(features.items())[:5]:
        print(f"  {key}: {value}")
    
    # Example: Create training dataset
    print("\n" + "="*50)
    print("Example 2: Create training dataset")
    audio_files = [
        'path/to/audio1.wav',
        'path/to/audio2.wav',
        'path/to/audio3.wav',
    ]
    # Uncomment to run:
    # df = create_training_dataset(audio_files, 'training_dataset.csv')
