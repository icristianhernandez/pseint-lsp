#!/usr/bin/env python3
"""
Test script to investigate encoding issues with PSeInt files
"""
import sys
import os

# Add the current directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.formatter import format_pseint_code

def test_encoding_compatibility():
    """Test how the formatter handles different encodings"""
    print("=== PSeInt Encoding Compatibility Test ===\n")
    
    # Test with reference_code3.psc (ISO-8859-1)
    file_path = 'reference_code/reference_code3.psc'
    
    print("1. Testing UTF-8 reading:")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content_utf8 = f.read()
        print("   ✓ UTF-8 read successful")
        print(f"   Content length: {len(content_utf8)} chars")
    except UnicodeDecodeError as e:
        print(f"   ✗ UTF-8 failed: {e}")
        content_utf8 = None
    
    print("\n2. Testing ISO-8859-1 reading:")
    try:
        with open(file_path, 'r', encoding='iso-8859-1') as f:
            content_latin1 = f.read()
        print("   ✓ ISO-8859-1 read successful")
        print(f"   Content length: {len(content_latin1)} chars")
        
        # Find lines with special characters
        special_lines: list[tuple[int, str]] = []
        for i, line in enumerate(content_latin1.split('\n')):
            if any(char in line for char in ['ó', 'é', 'ñ', 'á', 'í', 'ú', 'ü']):
                special_lines.append((i+1, line.strip()))
        
        print(f"   Found {len(special_lines)} lines with special characters:")
        for line_num, line in special_lines[:5]:  # Show first 5
            print(f"     Line {line_num}: {line}")
            
    except Exception as e:
        print(f"   ✗ ISO-8859-1 failed: {e}")
        content_latin1 = None
    
    print("\n3. Testing formatter with both encodings:")
    
    if content_utf8:
        try:
            formatted_utf8 = format_pseint_code(content_utf8)
            print("   ✓ Formatter works with UTF-8 content")
            print(f"   UTF-8 formatted length: {len(formatted_utf8)} chars")
        except Exception as e:
            print(f"   ✗ Formatter failed with UTF-8: {e}")
    
    if content_latin1:
        try:
            formatted_latin1 = format_pseint_code(content_latin1)
            print("   ✓ Formatter works with ISO-8859-1 content")
            
            # Check if special characters are preserved
            original_specials = [line for line in content_latin1.split('\n') 
                               if any(char in line for char in ['ó', 'é', 'ñ', 'á', 'í', 'ú', 'ü'])]
            formatted_specials = [line for line in formatted_latin1.split('\n') 
                                if any(char in line for char in ['ó', 'é', 'ñ', 'á', 'í', 'ú', 'ü'])]
            
            print(f"   Original lines with special chars: {len(original_specials)}")
            print(f"   Formatted lines with special chars: {len(formatted_specials)}")
            
            if len(original_specials) == len(formatted_specials):
                print("   ✓ Special characters preserved")
            else:
                print("   ⚠ Special character count changed")
                
        except Exception as e:
            print(f"   ✗ Formatter failed with ISO-8859-1: {e}")
    
    print("\n4. Testing encoding conversion:")
    if content_latin1:
        # Test converting to UTF-8 and back
        try:
            # Convert Latin-1 to UTF-8
            utf8_bytes = content_latin1.encode('utf-8')
            utf8_content = utf8_bytes.decode('utf-8')
            
            # Convert back to Latin-1
            latin1_bytes = utf8_content.encode('iso-8859-1')
            recovered_content = latin1_bytes.decode('iso-8859-1')
            
            if content_latin1 == recovered_content:
                print("   ✓ Round-trip conversion successful")
            else:
                print("   ✗ Round-trip conversion failed")
                
        except UnicodeEncodeError as e:
            print(f"   ⚠ Some characters cannot be encoded in ISO-8859-1: {e}")
        except Exception as e:
            print(f"   ✗ Conversion test failed: {e}")

if __name__ == "__main__":
    test_encoding_compatibility()
