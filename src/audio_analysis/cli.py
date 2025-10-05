"""Command-line interface for audio analysis."""

import argparse
import sys
from pathlib import Path
from typing import Optional

from .analyzer import AudioAnalyzer
from .wavetable import WavetableSynthesizer
from .formatter import OutputFormatter


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Audio Analysis Tool - Extract features and generate wavetables from audio files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze audio and save all features to JSON
  audio-analysis input.wav -o output.json
  
  # Extract only spectral features
  audio-analysis input.wav -f spectral -o features.json
  
  # Generate wavetables from audio
  audio-analysis input.wav -w -o wavetables.wav --num-tables 64
  
  # Get summary statistics in CSV format
  audio-analysis input.wav -s --format csv -o summary.csv
  
  # Extract all features and save in NPZ format
  audio-analysis input.wav --format npz -o features.npz
        """
    )
    
    # Input/Output arguments
    parser.add_argument(
        'input',
        type=str,
        help='Input audio file path'
    )
    parser.add_argument(
        '-o', '--output',
        type=str,
        default=None,
        help='Output file path (extension will be added based on format)'
    )
    
    # Feature extraction options
    parser.add_argument(
        '-f', '--features',
        type=str,
        choices=['all', 'spectral', 'temporal', 'harmonic', 'onsets', 'pitch'],
        default='all',
        help='Feature extraction type (default: all)'
    )
    parser.add_argument(
        '-s', '--summary',
        action='store_true',
        help='Extract only summary statistics instead of full features'
    )
    
    # Output format options
    parser.add_argument(
        '--format',
        type=str,
        choices=['json', 'csv', 'npz', 'txt'],
        default='json',
        help='Output format (default: json)'
    )
    
    # Wavetable options
    parser.add_argument(
        '-w', '--wavetable',
        action='store_true',
        help='Generate wavetables instead of extracting features'
    )
    parser.add_argument(
        '--num-tables',
        type=int,
        default=64,
        help='Number of wavetables to generate (default: 64)'
    )
    parser.add_argument(
        '--table-size',
        type=int,
        default=2048,
        help='Size of each wavetable (default: 2048)'
    )
    
    # Audio processing options
    parser.add_argument(
        '--sr',
        type=int,
        default=None,
        help='Target sample rate (default: native)'
    )
    
    # Verbosity
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    # Validate input file
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file '{args.input}' does not exist", file=sys.stderr)
        return 1
    
    # Set default output path if not specified
    if args.output is None:
        if args.wavetable:
            args.output = input_path.stem + '_wavetables.wav'
        else:
            args.output = input_path.stem + '_features'
    
    try:
        if args.wavetable:
            # Wavetable generation mode
            if args.verbose:
                print(f"Loading audio from: {args.input}")
            
            analyzer = AudioAnalyzer(args.input, sr=args.sr)
            synthesizer = WavetableSynthesizer(sr=analyzer.sr)
            
            if args.verbose:
                print(f"Generating {args.num_tables} wavetables of size {args.table_size}")
            
            wavetables = synthesizer.extract_wavetables_from_audio(
                analyzer.y,
                analyzer.sr,
                num_tables=args.num_tables,
                wavetable_size=args.table_size
            )
            
            output_path = args.output
            if not output_path.endswith('.wav'):
                output_path += '.wav'
            
            synthesizer.save_wavetable(wavetables, output_path)
            
            if args.verbose:
                print(f"Wavetables saved to: {output_path}")
                print(f"Total samples: {wavetables.size}")
        
        else:
            # Feature extraction mode
            if args.verbose:
                print(f"Loading audio from: {args.input}")
                print(f"Sample rate: {args.sr if args.sr else 'native'}")
            
            analyzer = AudioAnalyzer(args.input, sr=args.sr)
            
            if args.verbose:
                print(f"Audio duration: {analyzer.duration:.2f} seconds")
                print(f"Sample rate: {analyzer.sr} Hz")
            
            # Extract features based on type
            if args.summary:
                if args.verbose:
                    print("Extracting summary statistics...")
                features = analyzer.get_summary_statistics()
            elif args.features == 'all':
                if args.verbose:
                    print("Extracting all features...")
                features = analyzer.extract_all_features()
            elif args.features == 'spectral':
                if args.verbose:
                    print("Extracting spectral features...")
                features = analyzer.extract_spectral_features()
            elif args.features == 'temporal':
                if args.verbose:
                    print("Extracting temporal features...")
                features = analyzer.extract_temporal_features()
            elif args.features == 'harmonic':
                if args.verbose:
                    print("Extracting harmonic/percussive components...")
                features = analyzer.extract_harmonic_percussive()
            elif args.features == 'onsets':
                if args.verbose:
                    print("Detecting onsets...")
                features = analyzer.detect_onsets()
            elif args.features == 'pitch':
                if args.verbose:
                    print("Extracting pitch features...")
                features = analyzer.extract_pitch_features()
            
            # Save features
            output_path = OutputFormatter.save_features(
                features,
                args.output,
                format=args.format
            )
            
            if args.verbose:
                print(f"Features saved to: {output_path}")
        
        return 0
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
