"""Core audio analysis module for feature extraction."""

import librosa
import numpy as np
from typing import Dict, Optional, Tuple, List
import warnings


class AudioAnalyzer:
    """Comprehensive audio analyzer with multiple feature extraction techniques."""

    def __init__(self, audio_path: str, sr: Optional[int] = None):
        """
        Initialize the analyzer with an audio file.

        Args:
            audio_path: Path to the audio file
            sr: Target sampling rate (None to use native rate)
        """
        self.audio_path = audio_path
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.y, self.sr = librosa.load(audio_path, sr=sr)
        self.duration = librosa.get_duration(y=self.y, sr=self.sr)

    def extract_spectral_features(self) -> Dict[str, np.ndarray]:
        """
        Extract spectral features from the audio.

        Returns:
            Dictionary containing spectral features
        """
        features = {}
        
        # MFCCs (Mel-frequency cepstral coefficients)
        features['mfcc'] = librosa.feature.mfcc(y=self.y, sr=self.sr, n_mfcc=13)
        features['mfcc_delta'] = librosa.feature.delta(features['mfcc'])
        features['mfcc_delta2'] = librosa.feature.delta(features['mfcc'], order=2)
        
        # Spectral centroid
        features['spectral_centroid'] = librosa.feature.spectral_centroid(y=self.y, sr=self.sr)
        
        # Spectral rolloff
        features['spectral_rolloff'] = librosa.feature.spectral_rolloff(y=self.y, sr=self.sr)
        
        # Spectral bandwidth
        features['spectral_bandwidth'] = librosa.feature.spectral_bandwidth(y=self.y, sr=self.sr)
        
        # Spectral contrast
        features['spectral_contrast'] = librosa.feature.spectral_contrast(y=self.y, sr=self.sr)
        
        # Chroma features
        features['chroma_stft'] = librosa.feature.chroma_stft(y=self.y, sr=self.sr)
        features['chroma_cqt'] = librosa.feature.chroma_cqt(y=self.y, sr=self.sr)
        features['chroma_cens'] = librosa.feature.chroma_cens(y=self.y, sr=self.sr)
        
        return features

    def extract_temporal_features(self) -> Dict[str, np.ndarray]:
        """
        Extract temporal features from the audio.

        Returns:
            Dictionary containing temporal features
        """
        features = {}
        
        # Zero-crossing rate
        features['zero_crossing_rate'] = librosa.feature.zero_crossing_rate(self.y)
        
        # RMS energy
        features['rms'] = librosa.feature.rms(y=self.y)
        
        # Tempo and beat tracking
        tempo, beats = librosa.beat.beat_track(y=self.y, sr=self.sr)
        features['tempo'] = np.array([tempo])
        features['beat_frames'] = beats
        
        return features

    def extract_harmonic_percussive(self) -> Dict[str, np.ndarray]:
        """
        Separate harmonic and percussive components.

        Returns:
            Dictionary containing harmonic and percussive signals
        """
        y_harmonic, y_percussive = librosa.effects.hpss(self.y)
        
        return {
            'harmonic': y_harmonic,
            'percussive': y_percussive
        }

    def detect_onsets(self) -> Dict[str, np.ndarray]:
        """
        Detect onset events in the audio.

        Returns:
            Dictionary containing onset information
        """
        onset_frames = librosa.onset.onset_detect(y=self.y, sr=self.sr)
        onset_times = librosa.frames_to_time(onset_frames, sr=self.sr)
        onset_strength = librosa.onset.onset_strength(y=self.y, sr=self.sr)
        
        return {
            'onset_frames': onset_frames,
            'onset_times': onset_times,
            'onset_strength': onset_strength
        }

    def extract_pitch_features(self) -> Dict[str, np.ndarray]:
        """
        Extract pitch-related features.

        Returns:
            Dictionary containing pitch features
        """
        # Pitch (F0) estimation using piptrack
        pitches, magnitudes = librosa.piptrack(y=self.y, sr=self.sr)
        
        # Get the most prominent pitch at each frame
        pitch_values = []
        for t in range(pitches.shape[1]):
            index = magnitudes[:, t].argmax()
            pitch = pitches[index, t]
            pitch_values.append(pitch)
        
        return {
            'pitch_track': np.array(pitch_values),
            'pitch_matrix': pitches,
            'magnitude_matrix': magnitudes
        }

    def extract_all_features(self) -> Dict[str, Dict[str, np.ndarray]]:
        """
        Extract all available features.

        Returns:
            Dictionary containing all feature categories
        """
        return {
            'spectral': self.extract_spectral_features(),
            'temporal': self.extract_temporal_features(),
            'harmonic_percussive': self.extract_harmonic_percussive(),
            'onsets': self.detect_onsets(),
            'pitch': self.extract_pitch_features(),
            'metadata': {
                'sr': np.array([self.sr]),
                'duration': np.array([self.duration]),
                'samples': np.array([len(self.y)])
            }
        }

    def get_summary_statistics(self) -> Dict[str, Dict[str, float]]:
        """
        Get summary statistics for key features.

        Returns:
            Dictionary containing summary statistics
        """
        spectral = self.extract_spectral_features()
        temporal = self.extract_temporal_features()
        pitch = self.extract_pitch_features()
        
        summary = {}
        
        # Spectral statistics
        summary['spectral_centroid'] = {
            'mean': float(np.mean(spectral['spectral_centroid'])),
            'std': float(np.std(spectral['spectral_centroid'])),
            'min': float(np.min(spectral['spectral_centroid'])),
            'max': float(np.max(spectral['spectral_centroid']))
        }
        
        # RMS energy statistics
        summary['rms'] = {
            'mean': float(np.mean(temporal['rms'])),
            'std': float(np.std(temporal['rms'])),
            'min': float(np.min(temporal['rms'])),
            'max': float(np.max(temporal['rms']))
        }
        
        # Tempo
        summary['tempo'] = {
            'value': float(temporal['tempo'][0])
        }
        
        # Pitch statistics (non-zero values)
        non_zero_pitches = pitch['pitch_track'][pitch['pitch_track'] > 0]
        if len(non_zero_pitches) > 0:
            summary['pitch'] = {
                'mean': float(np.mean(non_zero_pitches)),
                'std': float(np.std(non_zero_pitches)),
                'min': float(np.min(non_zero_pitches)),
                'max': float(np.max(non_zero_pitches))
            }
        
        return summary
