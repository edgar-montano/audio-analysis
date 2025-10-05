"""Output formatters for various export formats."""

import json
import csv
import numpy as np
from pathlib import Path
from typing import Dict, Any, Union
import warnings


class OutputFormatter:
    """Format and export audio analysis results in various formats."""

    @staticmethod
    def _convert_numpy_types(obj: Any) -> Any:
        """Convert numpy types to native Python types for JSON serialization."""
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, dict):
            return {key: OutputFormatter._convert_numpy_types(value) for key, value in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [OutputFormatter._convert_numpy_types(item) for item in obj]
        return obj

    @staticmethod
    def to_json(data: Dict[str, Any], output_path: str, indent: int = 2):
        """
        Export data to JSON format.

        Args:
            data: Dictionary of analysis results
            output_path: Output file path
            indent: JSON indentation level
        """
        converted_data = OutputFormatter._convert_numpy_types(data)
        
        with open(output_path, 'w') as f:
            json.dump(converted_data, f, indent=indent)

    @staticmethod
    def to_csv(data: Dict[str, Any], output_path: str, flatten: bool = True):
        """
        Export data to CSV format.

        Args:
            data: Dictionary of analysis results
            output_path: Output file path
            flatten: Whether to flatten nested structures
        """
        # Flatten the data for CSV export
        flattened = {}
        
        def flatten_dict(d: Dict, parent_key: str = ''):
            for k, v in d.items():
                new_key = f"{parent_key}.{k}" if parent_key else k
                
                if isinstance(v, dict):
                    flatten_dict(v, new_key)
                elif isinstance(v, np.ndarray):
                    if v.ndim == 1 and len(v) < 100:
                        # Store small 1D arrays as comma-separated values
                        flattened[new_key] = ','.join(map(str, v.tolist()))
                    else:
                        # Store shape info for large/multi-dimensional arrays
                        flattened[f"{new_key}.shape"] = str(v.shape)
                        flattened[f"{new_key}.mean"] = float(np.mean(v))
                        flattened[f"{new_key}.std"] = float(np.std(v))
                else:
                    flattened[new_key] = v
        
        if flatten:
            flatten_dict(data)
        else:
            flattened = OutputFormatter._convert_numpy_types(data)
        
        # Write to CSV
        with open(output_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Feature', 'Value'])
            for key, value in flattened.items():
                writer.writerow([key, value])

    @staticmethod
    def to_npz(data: Dict[str, Any], output_path: str):
        """
        Export data to NumPy compressed format.

        Args:
            data: Dictionary of analysis results
            output_path: Output file path
        """
        # Flatten nested dictionaries and convert to numpy arrays
        arrays = {}
        
        def process_dict(d: Dict, prefix: str = ''):
            for key, value in d.items():
                full_key = f"{prefix}_{key}" if prefix else key
                
                if isinstance(value, dict):
                    process_dict(value, full_key)
                elif isinstance(value, np.ndarray):
                    arrays[full_key] = value
                elif isinstance(value, (list, tuple)):
                    arrays[full_key] = np.array(value)
                elif isinstance(value, (int, float)):
                    arrays[full_key] = np.array([value])
        
        process_dict(data)
        
        # Save to compressed npz file
        np.savez_compressed(output_path, **arrays)

    @staticmethod
    def to_txt(data: Dict[str, Any], output_path: str):
        """
        Export data to human-readable text format.

        Args:
            data: Dictionary of analysis results
            output_path: Output file path
        """
        def format_value(v: Any, indent: int = 0) -> str:
            indent_str = "  " * indent
            
            if isinstance(v, dict):
                lines = []
                for key, value in v.items():
                    lines.append(f"{indent_str}{key}:")
                    lines.append(format_value(value, indent + 1))
                return "\n".join(lines)
            elif isinstance(v, np.ndarray):
                if v.ndim == 1 and len(v) <= 10:
                    return f"{indent_str}  {v.tolist()}"
                else:
                    return (f"{indent_str}  shape: {v.shape}, "
                           f"mean: {np.mean(v):.4f}, "
                           f"std: {np.std(v):.4f}")
            elif isinstance(v, (list, tuple)) and len(v) <= 10:
                return f"{indent_str}  {v}"
            else:
                return f"{indent_str}  {v}"
        
        with open(output_path, 'w') as f:
            f.write(format_value(data))

    @staticmethod
    def save_features(
        features: Dict[str, Any],
        output_path: str,
        format: str = 'json'
    ):
        """
        Save features in the specified format.

        Args:
            features: Feature dictionary
            output_path: Output file path (extension may be added automatically)
            format: Output format ('json', 'csv', 'npz', 'txt')
        """
        # Ensure output path has correct extension
        output_path = str(Path(output_path))
        if not output_path.endswith(f'.{format}'):
            output_path = f"{output_path}.{format}"
        
        if format == 'json':
            OutputFormatter.to_json(features, output_path)
        elif format == 'csv':
            OutputFormatter.to_csv(features, output_path)
        elif format == 'npz':
            OutputFormatter.to_npz(features, output_path)
        elif format == 'txt':
            OutputFormatter.to_txt(features, output_path)
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        return output_path
