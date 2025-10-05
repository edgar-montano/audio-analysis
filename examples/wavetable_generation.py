"""Example: Generate wavetables from audio for use in synthesizers."""

from audio_analysis import AudioAnalyzer, WavetableSynthesizer
import numpy as np

# Initialize analyzer with audio file
analyzer = AudioAnalyzer('path/to/your/audio.wav')

# Initialize synthesizer
synthesizer = WavetableSynthesizer(sr=analyzer.sr)

print(f"Analyzing audio: {analyzer.duration:.2f} seconds at {analyzer.sr} Hz")

# Extract wavetables from the audio
print("\nExtracting wavetables...")
wavetables = synthesizer.extract_wavetables_from_audio(
    analyzer.y,
    analyzer.sr,
    num_tables=64,      # Number of wavetables
    wavetable_size=2048  # Size of each wavetable (samples per cycle)
)

print(f"Generated {wavetables.shape[0]} wavetables of size {wavetables.shape[1]}")

# Save the wavetable stack
synthesizer.save_wavetable(wavetables, 'output_wavetables.wav')
print("Wavetables saved to: output_wavetables.wav")

# You can also create basic waveforms
print("\nGenerating basic waveforms...")
sine_table = synthesizer.generate_sine_wavetable(2048)
saw_table = synthesizer.generate_saw_wavetable(2048)
square_table = synthesizer.generate_square_wavetable(2048)

# Morph between two wavetables
print("Creating morphed wavetables...")
morphed = synthesizer.morph_wavetables(sine_table, saw_table, num_steps=16)
synthesizer.save_wavetable(morphed, 'morphed_wavetables.wav')
print("Morphed wavetables saved to: morphed_wavetables.wav")

# Create a custom wavetable from a spectrum
print("\nCreating custom wavetable from spectrum...")
# Get the average spectrum from the audio
import librosa
stft = librosa.stft(analyzer.y, n_fft=2048)
avg_spectrum = np.mean(np.abs(stft), axis=1)
custom_table = synthesizer.create_wavetable_from_spectrum(avg_spectrum[:1024], 2048)
synthesizer.save_wavetable(custom_table, 'custom_wavetable.wav')
print("Custom wavetable saved to: custom_wavetable.wav")

print("\nAll wavetables generated successfully!")
print("These can now be imported into wavetable synthesizers like:")
print("  - Serum")
print("  - Vital")
print("  - Massive")
print("  - Pigments")
