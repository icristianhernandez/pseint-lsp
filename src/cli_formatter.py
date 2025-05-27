#!/usr/bin/env python3
"""
Command-line formatter for PSeInt files with encoding detection.

This provides a standalone CLI that can handle PSeInt files regardless of their encoding,
making the formatter truly editor-agnostic.

Usage:
    python cli_formatter.py input.psc output.psc
    python cli_formatter.py input.psc  # overwrites input file
"""

import sys
import argparse
from pathlib import Path
from typing import Optional


from src.formatter import format_pseint_code
from src.encoding_utils import detect_file_encoding, ensure_clean_text

# Ensure we can import from the current directory
script_dir = Path(__file__).parent.absolute()
if str(script_dir) not in sys.path:
    sys.path.insert(0, str(script_dir))


def format_file(input_path: str, output_path: Optional[str] = None) -> bool:
    """
    Format a PSeInt file with automatic encoding detection.
    
    Args:
        input_path: Path to the input file
        output_path: Path to the output file (defaults to input_path)
        
    Returns:
        True if formatting was successful
    """
    try:
        # Detect and read the file with proper encoding
        content, detected_encoding = detect_file_encoding(input_path)
        print(f"Detected encoding: {detected_encoding}")
        
        # Ensure the content is clean (in case editor sent corrupted text)
        clean_content = ensure_clean_text(content, input_path)
        
        if clean_content != content:
            print("Applied encoding corrections to input text")
        
        # Format the code
        formatted_content = format_pseint_code(clean_content)
        
        # Determine output path
        if output_path is None:
            output_path = input_path
            
        # Write the formatted content back using the original encoding
        with open(output_path, 'w', encoding=detected_encoding) as f:
            f.write(formatted_content)
            
        print(f"Successfully formatted {input_path} -> {output_path}")
        
        if formatted_content == clean_content:
            print("No formatting changes were needed")
        else:
            lines_before = len(clean_content.splitlines())
            lines_after = len(formatted_content.splitlines())
            print(f"Formatting applied: {lines_before} -> {lines_after} lines")
            
        return True
        
    except Exception as e:
        print(f"Error formatting file: {e}", file=sys.stderr)
        return False


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Format PSeInt files with automatic encoding detection",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s code.psc                    # Format in-place
  %(prog)s code.psc formatted.psc     # Format to new file
  %(prog)s *.psc                      # Format multiple files in-place
        """
    )
    
    parser.add_argument(
        'input_files',
        nargs='+',
        help='PSeInt files to format (.psc files)'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Output file (only valid with single input file)'
    )
    
    parser.add_argument(
        '--check',
        action='store_true',
        help='Check if files need formatting without modifying them'
    )
    
    parser.add_argument(
        '--encoding',
        choices=['auto', 'utf-8', 'iso-8859-1', 'cp1252'],
        default='auto',
        help='Force specific encoding (default: auto-detect)'
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.output and len(args.input_files) > 1:
        print("Error: --output can only be used with a single input file", file=sys.stderr)
        return 1
        
    if args.check and args.output:
        print("Error: --check and --output cannot be used together", file=sys.stderr)
        return 1
    
    success_count = 0
    total_count = len(args.input_files)
    
    for input_file in args.input_files:
        if not Path(input_file).exists():
            print(f"Error: File not found: {input_file}", file=sys.stderr)
            continue
            
        print(f"\nProcessing: {input_file}")
        
        if args.check:
            # Check mode: detect if formatting is needed
            try:
                content, _ = detect_file_encoding(input_file)
                clean_content = ensure_clean_text(content, input_file)
                formatted_content = format_pseint_code(clean_content)
                
                if formatted_content == clean_content:
                    print(f"✓ {input_file} is already formatted correctly")
                else:
                    print(f"✗ {input_file} needs formatting")
                    
                success_count += 1
                
            except Exception as e:
                print(f"Error checking {input_file}: {e}", file=sys.stderr)
        else:
            # Format mode
            output_file = args.output if args.output else None
            if format_file(input_file, output_file):
                success_count += 1
    
    print(f"\nCompleted: {success_count}/{total_count} files processed successfully")
    
    if args.check:
        # Return non-zero exit code if any files need formatting
        files_needing_format = total_count - success_count
        return 1 if files_needing_format > 0 else 0
    else:
        # Return non-zero exit code if any files failed to format
        return 0 if success_count == total_count else 1


if __name__ == "__main__":
    sys.exit(main())
