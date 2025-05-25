#!/usr/bin/env python3

import sys
from formatter import format_pseint_code

def main():
    if len(sys.argv) != 3:
        print("Usage: python run_formatter.py <input_file> <output_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    try:
        # Read the input file
        with open(input_file, 'r', encoding='utf-8') as f:
            code = f.read()
        
        # Format the code
        formatted_code = format_pseint_code(code)
        
        # Write the formatted code to output file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(formatted_code)
        
        print(f"Successfully formatted {input_file} and saved to {output_file}")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
