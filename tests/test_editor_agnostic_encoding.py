import unittest
import tempfile
import os
import sys


# Add the parent directory to sys.path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.encoding_utils import (
    detect_encoding_corruption, 
    fix_encoding_corruption, 
    ensure_clean_text,
    detect_file_encoding,
    validate_pseint_encoding_support
)
from src.formatter import format_pseint_code


class TestEditorAgnosticEncoding(unittest.TestCase):
    """Test that the formatter works correctly regardless of editor behavior."""

    def test_encoding_corruption_detection(self):
        """Test detection of common encoding corruption patterns."""
        
        # Test cases with corruption patterns
        test_cases = [
            ("Esta versiÃ³n", True, "Ã³"),
            ("El niÃ±o pequeÃ±o", True, "Ã±"), 
            ("AÃ±o nuevo", True, "Ã±"),
            ("¿CÃ³mo estÃ¡s?", True, "Ã³"),
            ("Esta versión", False, ""),
            ("El niño pequeño", False, ""),
            ("¿Cómo estás?", False, ""),
            ("Normal text without special chars", False, ""),
        ]
        
        for text, should_be_corrupted, expected_pattern in test_cases:
            with self.subTest(text=text):
                is_corrupted, reason = detect_encoding_corruption(text)
                self.assertEqual(is_corrupted, should_be_corrupted)
                if should_be_corrupted:
                    self.assertIn(expected_pattern, reason)

    def test_encoding_corruption_fixing(self):
        """Test automatic correction of encoding corruption."""
        
        test_cases = [
            ("Esta versiÃ³n", "Esta versión"),
            ("El niÃ±o", "El niño"),
            ("AÃ±o 2025", "Año 2025"), 
            ("Â¿CÃ³mo estÃ¡s?", "¿Cómo estás?"),
            ("Normal text", "Normal text"),  # No change expected
        ]
        
        for corrupted, expected in test_cases:
            with self.subTest(corrupted=corrupted):
                fixed = fix_encoding_corruption(corrupted)
                self.assertEqual(fixed, expected)

    def test_editor_agnostic_text_cleaning(self):
        """Test the main ensure_clean_text function."""
        
        # Simulate different editor scenarios
        
        # Scenario 1: VS Code with proper encoding detection
        clean_text = "Algoritmo Año2025\n    // Versión con niño"
        result = ensure_clean_text(clean_text, "test.psc")
        self.assertEqual(result, clean_text)
        
        # Scenario 2: Editor that sends corrupted text  
        corrupted_text = "Algoritmo AÃ±o2025\n    // VersiÃ³n con niÃ±o"
        result = ensure_clean_text(corrupted_text, "test.psc")
        expected = "Algoritmo Año2025\n    // Versión con niño"
        self.assertEqual(result, expected)

    def test_file_encoding_detection(self):
        """Test automatic file encoding detection."""
        
        # Create test files with different encodings
        test_content = "Algoritmo TestAño\n    // Versión con niño\nFinAlgoritmo"
        
        with tempfile.TemporaryDirectory() as tmpdir:
            # UTF-8 file
            utf8_file = os.path.join(tmpdir, "test_utf8.psc")
            with open(utf8_file, 'w', encoding='utf-8') as f:
                f.write(test_content)
            
            content, encoding = detect_file_encoding(utf8_file)
            self.assertEqual(encoding, 'utf-8')
            self.assertIn("Año", content)
            self.assertIn("niño", content)
            
            # ISO-8859-1 file
            iso_file = os.path.join(tmpdir, "test_iso.psc")
            with open(iso_file, 'w', encoding='iso-8859-1') as f:
                f.write(test_content)
                
            content, encoding = detect_file_encoding(iso_file)
            self.assertEqual(encoding, 'iso-8859-1')
            self.assertIn("Año", content)
            self.assertIn("niño", content)

    def test_complete_editor_agnostic_formatting(self):
        """Test complete formatting workflow with encoding issues."""
        
        # Simulate the complete workflow:
        # 1. Editor sends corrupted text to LSP
        # 2. LSP detects and fixes corruption
        # 3. LSP formats the clean text
        # 4. LSP returns formatted text
        
        # Original PSeInt code with corruption (as received from problematic editor)
        corrupted_input = """Algoritmo TestAÃ±o
    // Esta versiÃ³n tiene caracteres especiales
    Definir nombre Como Cadena
    Escribir "Â¿CÃ³mo estÃ¡ usted?"
    Escribir "NiÃ±o pequeÃ±o"
FinAlgoritmo"""

        # Expected clean result after encoding fix + formatting


        # Apply the complete editor-agnostic workflow
        clean_input = ensure_clean_text(corrupted_input)
        formatted_output = format_pseint_code(clean_input)
        
        # Verify the result
        self.assertIn("Año", formatted_output)
        self.assertIn("versión", formatted_output) 
        self.assertIn("¿Cómo", formatted_output)
        self.assertIn("Niño", formatted_output)
        
        # Should not contain corruption patterns
        self.assertNotIn("Ã±", formatted_output)
        self.assertNotIn("Ã³", formatted_output)
        self.assertNotIn("Â¿", formatted_output)

    def test_environment_encoding_support(self):
        """Test that the environment properly supports PSeInt encoding."""
        self.assertTrue(validate_pseint_encoding_support())

    def test_round_trip_encoding_compatibility(self):
        """Test that formatted content can be saved in original encoding."""
        
        test_content = "Algoritmo Año\n    // Versión con ñ\nFinAlgoritmo"
        
        # Test UTF-8 round trip
        formatted = format_pseint_code(test_content)
        try:
            utf8_bytes = formatted.encode('utf-8')
            utf8_decoded = utf8_bytes.decode('utf-8')
            self.assertEqual(utf8_decoded, formatted)
        except UnicodeError:
            self.fail("UTF-8 round trip failed")
            
        # Test ISO-8859-1 round trip  
        try:
            iso_bytes = formatted.encode('iso-8859-1')
            iso_decoded = iso_bytes.decode('iso-8859-1')
            self.assertEqual(iso_decoded, formatted)
        except UnicodeError:
            self.fail("ISO-8859-1 round trip failed")


class TestCLIFormatterIntegration(unittest.TestCase):
    """Test the CLI formatter with real files."""
    
    def test_cli_with_iso_file(self):
        """Test CLI formatter with actual ISO-8859-1 file."""
        
        # Use the reference file that we know is ISO-8859-1
        reference_file = "reference_code/reference_code3.psc"
        
        if os.path.exists(reference_file):
            # Test that we can detect the encoding
            content, encoding = detect_file_encoding(reference_file)
            self.assertEqual(encoding, 'iso-8859-1')
            
            # Test that the content contains expected Spanish characters
            self.assertIn("versión", content)
            self.assertIn("compañeros", content)
            
            # Test that we can format it
            formatted = format_pseint_code(content)
            self.assertIsInstance(formatted, str)
            
            # Test that formatted content can be encoded back to ISO-8859-1
            try:
                formatted.encode('iso-8859-1')
            except UnicodeEncodeError:
                self.fail("Formatted content cannot be encoded back to ISO-8859-1")


if __name__ == '__main__':
    unittest.main()
