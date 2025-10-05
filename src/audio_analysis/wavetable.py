"""Wavetable synthesis module for recreating sounds from analysis."""

import numpy as np
import soundfile as sf
from typing import Optional, List


class WavetableSynthesizer:
    """Generate wavetable data from audio analysis for use in synthesizers."""

    def __init__(self, sr: int = 44100):
        """
        Initialize the synthesizer.

        Args:
            sr: Sample rate for synthesis
        """
        self.sr = sr

    def create_wavetable_from_spectrum(
        self, 
        spectrum: np.ndarray, 
        wavetable_size: int = 2048
    ) -> np.ndarray:
        """
        Create a single-cycle wavetable from a spectrum.

        Args:
            spectrum: Magnitude spectrum
            wavetable_size: Size of the wavetable (power of 2 recommended)

        Returns:
            Single-cycle waveform
        """
        # Use inverse FFT to convert spectrum to time domain
        # Ensure the spectrum is the right size
        if len(spectrum) > wavetable_size // 2:
            spectrum = spectrum[:wavetable_size // 2]
        
        # Create complex spectrum (assuming zero phase)
        complex_spectrum = np.zeros(wavetable_size, dtype=complex)
        complex_spectrum[:len(spectrum)] = spectrum
        
        # Mirror for real signal
        if wavetable_size > 1:
            complex_spectrum[wavetable_size//2+1:] = np.conj(complex_spectrum[1:wavetable_size//2][::-1])
        
        # Inverse FFT
        wavetable = np.fft.ifft(complex_spectrum).real
        
        # Normalize
        if np.max(np.abs(wavetable)) > 0:
            wavetable = wavetable / np.max(np.abs(wavetable))
        
        return wavetable

    def create_wavetable_stack(
        self, 
        stft_matrix: np.ndarray, 
        num_tables: int = 64,
        wavetable_size: int = 2048
    ) -> np.ndarray:
        """
        Create a stack of wavetables from an STFT matrix.

        Args:
            stft_matrix: STFT magnitude matrix
            num_tables: Number of wavetables to create
            wavetable_size: Size of each wavetable

        Returns:
            Array of shape (num_tables, wavetable_size)
        """
        # Select evenly spaced frames from the STFT
        num_frames = stft_matrix.shape[1]
        frame_indices = np.linspace(0, num_frames - 1, num_tables, dtype=int)
        
        wavetables = np.zeros((num_tables, wavetable_size))
        
        for i, frame_idx in enumerate(frame_indices):
            spectrum = stft_matrix[:, frame_idx]
            wavetables[i] = self.create_wavetable_from_spectrum(spectrum, wavetable_size)
        
        return wavetables

    def extract_wavetables_from_audio(
        self, 
        y: np.ndarray, 
        sr: int,
        num_tables: int = 64,
        wavetable_size: int = 2048,
        n_fft: int = 2048
    ) -> np.ndarray:
        """
        Extract wavetables directly from audio signal.

        Args:
            y: Audio signal
            sr: Sample rate
            num_tables: Number of wavetables to extract
            wavetable_size: Size of each wavetable
            n_fft: FFT size for STFT

        Returns:
            Array of wavetables
        """
        import librosa
        
        # Compute STFT
        stft = librosa.stft(y, n_fft=n_fft, hop_length=n_fft//4)
        magnitude = np.abs(stft)
        
        # Create wavetable stack
        return self.create_wavetable_stack(magnitude, num_tables, wavetable_size)

    def save_wavetable(
        self, 
        wavetable: np.ndarray, 
        output_path: str,
        format: str = 'wav'
    ):
        """
        Save wavetable to audio file.

        Args:
            wavetable: Wavetable data (1D or 2D array)
            output_path: Output file path
            format: Audio format ('wav', 'flac', etc.)
        """
        # Ensure 2D shape for multi-table
        if wavetable.ndim == 1:
            wavetable = wavetable.reshape(1, -1)
        
        # Flatten to single audio stream
        flattened = wavetable.flatten()
        
        # Normalize
        if np.max(np.abs(flattened)) > 0:
            flattened = flattened / np.max(np.abs(flattened)) * 0.9
        
        # Save
        sf.write(output_path, flattened, self.sr, format=format)

    def generate_sine_wavetable(self, wavetable_size: int = 2048) -> np.ndarray:
        """
        Generate a basic sine wave wavetable.

        Args:
            wavetable_size: Size of the wavetable

        Returns:
            Sine wave wavetable
        """
        return np.sin(2 * np.pi * np.arange(wavetable_size) / wavetable_size)

    def generate_saw_wavetable(self, wavetable_size: int = 2048) -> np.ndarray:
        """
        Generate a sawtooth wave wavetable.

        Args:
            wavetable_size: Size of the wavetable

        Returns:
            Sawtooth wave wavetable
        """
        return 2 * (np.arange(wavetable_size) / wavetable_size) - 1

    def generate_square_wavetable(self, wavetable_size: int = 2048) -> np.ndarray:
        """
        Generate a square wave wavetable.

        Args:
            wavetable_size: Size of the wavetable

        Returns:
            Square wave wavetable
        """
        return np.where(np.arange(wavetable_size) < wavetable_size // 2, 1.0, -1.0)

    def morph_wavetables(
        self, 
        wavetable1: np.ndarray, 
        wavetable2: np.ndarray, 
        num_steps: int = 16
    ) -> np.ndarray:
        """
        Create morphed wavetables between two wavetables.

        Args:
            wavetable1: First wavetable
            wavetable2: Second wavetable
            num_steps: Number of interpolation steps

        Returns:
            Array of morphed wavetables
        """
        morphed = np.zeros((num_steps, len(wavetable1)))
        
        for i in range(num_steps):
            alpha = i / (num_steps - 1)
            morphed[i] = (1 - alpha) * wavetable1 + alpha * wavetable2
        
        return morphed
