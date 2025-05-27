import unittest
import os
import sys

# Add the parent directory to sys.path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.formatter import format_pseint_code


class TestEncodingCompatibility(unittest.TestCase):
    """Test encoding compatibility with PSeInt's ISO-8859-1 format."""

    def test_utf8_vs_iso88591_content(self):
        """Test that formatter preserves special characters correctly."""
        
        # Sample PSeInt code with Spanish special characters
        # This represents what the content should look like when properly decoded
        utf8_content = '''Algoritmo TestEspeciales
    // Esta versión tiene caracteres especiales: ñ, á, é, í, ó, ú
    Definir nombre Como Cadena
    Escribir "¿Cómo está usted?"
    Escribir "Año: 2025"
    Escribir "Niño pequeño"
FinAlgoritmo'''

        # This represents corrupted content when ISO-8859-1 is read as UTF-8
        corrupted_content = '''Algoritmo TestEspeciales
    // Esta versi�n tiene caracteres especiales: �, �, �, �, �, �
    Definir nombre Como Cadena
    Escribir "�C�mo est� usted?"
    Escribir "A�o: 2025"
    Escribir "Ni�o peque�o"
FinAlgoritmo'''

        # Test formatting with proper UTF-8 content
        formatted_utf8 = format_pseint_code(utf8_content)
        
        # Test formatting with corrupted content
        formatted_corrupted = format_pseint_code(corrupted_content)
        
        # The formatter should preserve the characters as-is
        # Check that special characters are maintained in both cases
        self.assertIn("versión", formatted_utf8)
        self.assertIn("¿Cómo", formatted_utf8)
        self.assertIn("Año:", formatted_utf8)
        self.assertIn("Niño", formatted_utf8)
        
        # Corrupted content should maintain corruption (for now)
        self.assertIn("versi�n", formatted_corrupted)
        self.assertIn("�C�mo", formatted_corrupted)
        self.assertIn("A�o:", formatted_corrupted)
        self.assertIn("Ni�o", formatted_corrupted)

    def test_iso88591_string_literals_preservation(self):
        """Test that string literals with special characters are preserved exactly."""
        
        code_with_strings = '''Algoritmo TestStrings
    Definir mensaje Como Cadena
    mensaje <- "Bienvenido al año 2025"
    Escribir "El niño está feliz"
    Escribir "¡Qué día tan hermoso!"
FinAlgoritmo'''

        formatted = format_pseint_code(code_with_strings)
        
        # String content should be preserved exactly
        self.assertIn('"Bienvenido al año 2025"', formatted)
        self.assertIn('"El niño está feliz"', formatted)
        self.assertIn('"¡Qué día tan hermoso!"', formatted)

    def test_encoding_round_trip_simulation(self):
        """Simulate what happens with encoding round trips."""
        
        # Original ISO-8859-1 content
        original_latin1_bytes = b'Escribir "A\xf1o 2025"'  # "Año 2025" in Latin-1
        
        # Simulate proper decoding
        proper_content = original_latin1_bytes.decode('iso-8859-1')
        self.assertEqual(proper_content, 'Escribir "Año 2025"')
        
        # Format the properly decoded content
        formatted = format_pseint_code(proper_content)
        
        # Should preserve the special character
        self.assertIn("Año", formatted)
        
        # Test that we can encode back to ISO-8859-1
        try:
            encoded_back = formatted.encode('iso-8859-1')
            self.assertIsInstance(encoded_back, bytes)
        except UnicodeEncodeError:
            self.fail("Formatted content cannot be encoded back to ISO-8859-1")


if __name__ == '__main__':
    unittest.main()
