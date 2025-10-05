"""Example: Batch processing multiple audio files."""

import os
from pathlib import Path
from audio_analysis import AudioAnalyzer, OutputFormatter

def analyze_audio_file(input_path, output_dir):
    """Analyze a single audio file and save results."""
    try:
        print(f"Analyzing: {input_path}")
        
        # Create analyzer
        analyzer = AudioAnalyzer(str(input_path))
        
        # Get summary statistics
        summary = analyzer.get_summary_statistics()
        
        # Create output filename
        output_name = input_path.stem + '_analysis'
        output_path = output_dir / output_name
        
        # Save as JSON
        OutputFormatter.save_features(summary, str(output_path), format='json')
        
        print(f"  ✓ Saved to: {output_path}.json")
        return True
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def batch_analyze(input_directory, output_directory, extensions=None):
    """
    Batch analyze all audio files in a directory.
    
    Args:
        input_directory: Directory containing audio files
        output_directory: Directory to save analysis results
        extensions: List of file extensions to process (default: common audio formats)
    """
    if extensions is None:
        extensions = ['.wav', '.mp3', '.flac', '.ogg', '.m4a', '.aac']
    
    input_path = Path(input_directory)
    output_path = Path(output_directory)
    
    # Create output directory if it doesn't exist
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Find all audio files
    audio_files = []
    for ext in extensions:
        audio_files.extend(input_path.glob(f'*{ext}'))
        audio_files.extend(input_path.glob(f'*{ext.upper()}'))
    
    print(f"Found {len(audio_files)} audio files to process")
    print(f"Output directory: {output_path}\n")
    
    # Process each file
    success_count = 0
    for audio_file in audio_files:
        if analyze_audio_file(audio_file, output_path):
            success_count += 1
    
    print(f"\nProcessing complete!")
    print(f"Successfully analyzed: {success_count}/{len(audio_files)} files")

if __name__ == '__main__':
    # Example usage
    input_dir = 'path/to/audio/files'
    output_dir = 'path/to/output/analysis'
    
    batch_analyze(input_dir, output_dir)
    
    # Or specify custom extensions
    # batch_analyze(input_dir, output_dir, extensions=['.wav', '.mp3'])
