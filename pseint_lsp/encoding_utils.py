#!/usr/bin/env python3
"""
Encoding utilities for PSeInt LSP server.

Provides editor-agnostic encoding detection and correction to handle
the mismatch between PSeInt's ISO-8859-1 default encoding and LSP's UTF-8 requirement.
"""

from typing import Tuple, Optional

def detect_encoding_corruption(text: str) -> Tuple[bool, str]:
    """
    Detect if text contains encoding corruption artifacts.
    
    This happens when ISO-8859-1 encoded text is incorrectly decoded as UTF-8,
    resulting in specific corruption patterns for Spanish special characters.
    
    Args:
        text: The text to check for encoding corruption
        
    Returns:
        Tuple of (is_corrupted: bool, reason: str)
    """
    # Common corruption patterns when ISO-8859-1 is read as UTF-8
    corruption_patterns = {
        'Ã±': 'ñ',  # ñ corrupted
        'Ã¡': 'á',  # á corrupted  
        'Ã©': 'é',  # é corrupted
        'Ã­': 'í',  # í corrupted
        'Ã³': 'ó',  # ó corrupted
        'Ãº': 'ú',  # ú corrupted
        'Ã': 'Ñ',   # Ñ corrupted
        'Ã¿': 'ÿ',  # ÿ corrupted
        'Â¿': '¿',  # ¿ corrupted
        'Â¡': '¡',  # ¡ corrupted
        '�': 'replacement character',  # Generic replacement character
    }
    
    found_patterns: list[str] = []
    for corrupted, original in corruption_patterns.items():
        if corrupted in text:
            found_patterns.append(f"'{corrupted}' (should be '{original}')")
    
    if found_patterns:
        return True, f"Found corruption patterns: {', '.join(found_patterns)}"
    
    return False, "No obvious corruption detected"


def fix_encoding_corruption(text: str) -> str:
    """
    Attempt to fix encoding corruption by converting common patterns.
    
    This function tries to reverse the damage caused when ISO-8859-1 text
    is incorrectly decoded as UTF-8.
    
    Args:
        text: The corrupted text
        
    Returns:
        Text with corruption patterns replaced with correct characters
    """
    # Mapping of common corruption patterns to correct characters
    fixes = {
        'Ã±': 'ñ',
        'Ã¡': 'á',
        'Ã©': 'é', 
        'Ã­': 'í',
        'Ã³': 'ó',
        'Ãº': 'ú',
        'Ã': 'Ñ',
        'Ã¿': 'ÿ',
        'Â¿': '¿',
        'Â¡': '¡',
        'Ã¼': 'ü',
        'Ã€': 'À',
        'Ã‰': 'É',
        'Ãš': 'Ú',
    }
    
    fixed_text = text
    for corrupted, correct in fixes.items():
        fixed_text = fixed_text.replace(corrupted, correct)
    return fixed_text


def detect_file_encoding(file_path: str) -> Tuple[str, str]:
    """
    Detect the encoding of a file by trying common encodings.
    
    Args:
        file_path: Path to the file to analyze
        
    Returns:
        Tuple of (content: str, encoding: str)
        
    Raises:
        UnicodeDecodeError: If file cannot be decoded with any supported encoding
    """
    # Try encodings in order of preference for PSeInt files
    encodings = ['utf-8', 'iso-8859-1', 'cp1252', 'latin-1']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
            return content, encoding
        except (UnicodeDecodeError, FileNotFoundError):
            continue
    
    raise ValueError(
        f"Could not decode file {file_path} with any of the supported encodings: {encodings}"
    )


def ensure_clean_text(text: str, file_uri: Optional[str] = None) -> str:
    """
    Ensure text is free from encoding corruption.
    
    This is the main function to call from the LSP server to handle
    encoding issues in a editor-agnostic way.
    
    Args:
        text: The text received from the LSP client
        file_uri: Optional file URI for logging purposes
        
    Returns:
        Clean text with any encoding corruption fixed
    """
    is_corrupted, reason = detect_encoding_corruption(text)
    
    if is_corrupted:
        # Log the detection for debugging
        import logging
        logging.warning(f"Encoding corruption detected in {file_uri or 'text'}: {reason}")
        
        # Attempt to fix the corruption
        fixed_text = fix_encoding_corruption(text)
        
        # Verify the fix worked
        is_still_corrupted, _reason2 = detect_encoding_corruption(fixed_text)
        if not is_still_corrupted:
            logging.info(f"Successfully fixed encoding corruption in {file_uri or 'text'}")
            return fixed_text
        else:
            logging.warning(f"Could not fully fix encoding corruption in {file_uri or 'text'}")
            return fixed_text  # Return partially fixed text anyway
    
    return text


def validate_pseint_encoding_support() -> bool:
    """
    Test if the current environment properly supports PSeInt character encoding.
    
    Returns:
        True if encoding support is working correctly
    """
    try:
        # Test string with common PSeInt Spanish characters
        test_string = "Año niño versión función código"
        
        # Test UTF-8 encoding/decoding
        utf8_encoded = test_string.encode('utf-8')
        utf8_decoded = utf8_encoded.decode('utf-8')
        
        # Test ISO-8859-1 encoding/decoding  
        iso_encoded = test_string.encode('iso-8859-1')
        iso_decoded = iso_encoded.decode('iso-8859-1')
        
        # Verify round-trip integrity
        return (utf8_decoded == test_string and 
                iso_decoded == test_string)
                
    except (UnicodeEncodeError, UnicodeDecodeError):
        return False


if __name__ == "__main__":
    # Test the encoding utilities
    print("=== Testing Encoding Utilities ===")
    
    # Test corruption detection
    corrupted_text = "Esta versiÃ³n fue realizada por el niÃ±o"
    clean_text = "Esta versión fue realizada por el niño"
    
    print(f"Corrupted text: {detect_encoding_corruption(corrupted_text)}")
    print(f"Clean text: {detect_encoding_corruption(clean_text)}")
    
    # Test corruption fixing
    fixed_text = fix_encoding_corruption(corrupted_text)
    print(f"Original: {corrupted_text}")
    print(f"Fixed: {fixed_text}")
    print(f"Expected: {clean_text}")
    print(f"Fix successful: {fixed_text == clean_text}")
    
    # Test environment support
    print(f"Environment supports PSeInt encoding: {validate_pseint_encoding_support()}")
