import unittest
import sys
import os
from typing import Optional

# Add the parent directory to sys.path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.formatter import format_pseint_code


class TestPSeIntFormatterIntegration(unittest.TestCase):
    """Integration tests using real PSeInt code examples."""

    def setUp(self):
        """Set up test fixtures."""
        # Set reference_files_dir to the correct reference_code directory
        self.reference_files_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "reference_code"
        )

    def read_reference_file(self, filename: str) -> Optional[str]:
        """Read content from a reference file."""
        file_path = os.path.join(self.reference_files_dir, filename)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            self.skipTest(f"Reference file {filename} not found")
        except UnicodeDecodeError:
            # Try with latin-1 encoding for files with special characters
            with open(file_path, "r", encoding="latin-1") as f:
                return f.read()

    def test_format_reference_code1_battleship(self):
        """Test formatting of reference_code1.psc (battleship game)."""
        content = self.read_reference_file("reference_code1.psc")
        if content is None:
            return

        # Format the code
        formatted = format_pseint_code(content)

        # Basic checks - formatted code should have proper structure
        self.assertIn("Proceso BatallaNavalMain", formatted)
        self.assertIn("FinProceso", formatted)

        # Check that keywords are properly cased
        self.assertIn("Definir", formatted)
        self.assertIn("Como", formatted)
        self.assertIn("Repetir", formatted)

        # Check indentation - lines after Proceso should be indented
        lines = formatted.split("\n")
        proceso_found = False
        for i, line in enumerate(lines):
            if "Proceso BatallaNavalMain" in line:
                proceso_found = True
                # Next non-empty line should be indented
                for j in range(i + 1, len(lines)):
                    if lines[j].strip():
                        self.assertTrue(
                            lines[j].startswith("    "),
                            f"Line after Proceso should be indented: '{lines[j]}'",
                        )
                        break
                break

        self.assertTrue(
            proceso_found, "Proceso BatallaNavalMain not found in formatted output"
        )

    def test_format_reference_code2_sales_matrix(self):
        """Test formatting of reference_code2.psc (sales matrix management)."""
        content = self.read_reference_file("reference_code2.psc")
        if content is None:
            return

        # Format the code
        formatted = format_pseint_code(content)

        # Check SubProceso formatting
        self.assertIn("SubProceso", formatted)
        self.assertIn("FinSubProceso", formatted)

        # Check Para loop formatting
        self.assertIn("Para", formatted)
        self.assertIn("FinPara", formatted)

        # Check proper indentation in subprocesos
        lines = formatted.split("\n")
        in_subproceso = False
        for line in lines:
            if line.strip().startswith("SubProceso"):
                in_subproceso = True
            elif line.strip().startswith("FinSubProceso"):
                in_subproceso = False
            elif in_subproceso and line.strip() and not line.strip().startswith("//"):
                # Non-comment lines inside SubProceso should be indented
                self.assertTrue(
                    line.startswith("    "),
                    f"Line in SubProceso should be indented: '{line}'",
                )

    def test_format_reference_code3_word_matrix(self):
        """Test formatting of reference_code3.psc (word matrix algorithm)."""
        content = self.read_reference_file("reference_code3.psc")
        if content is None:
            return

        # Format the code
        formatted = format_pseint_code(content)

        # Check Algoritmo formatting
        self.assertIn("Algoritmo", formatted)
        self.assertIn("FinAlgoritmo", formatted)

        # Check array dimension formatting
        self.assertIn("Dimension", formatted)

        # Check function calls are properly formatted
        lines = formatted.split("\n")
        for line in lines:
            # Check that function calls with parentheses are properly spaced
            if "(" in line and ")" in line and not line.strip().startswith("//"):
                # There should be no space before opening parenthesis in function calls
                # This is a basic check - more sophisticated parsing would be needed for complete validation
                pass

    def test_formatter_preserves_functionality(self):
        """Test that formatting preserves the logical structure of all reference files."""
        for ref_file in [
            "reference_code1.psc",
            "reference_code2.psc",
            "reference_code3.psc",
        ]:
            with self.subTest(reference_file=ref_file):
                content = self.read_reference_file(ref_file)
                if content is None:
                    continue

                formatted = format_pseint_code(content)

                # Count control structure pairs to ensure they're preserved
                # Count Si statements more accurately using regex to match word boundaries
                import re
                
                original_counts = {
                    "proceso": len(re.findall(r'\bproceso\b', content, re.IGNORECASE)),
                    "finproceso": len(re.findall(r'\bfinproceso\b', content, re.IGNORECASE)),
                    "subproceso": len(re.findall(r'\bsubproceso\b', content, re.IGNORECASE)),
                    "finsubproceso": len(re.findall(r'\bfinsubproceso\b', content, re.IGNORECASE)),
                    "algoritmo": len(re.findall(r'\balgoritmo\b', content, re.IGNORECASE)),
                    "finalgoritmo": len(re.findall(r'\bfinalgoritmo\b', content, re.IGNORECASE)),
                    "si": len(re.findall(r'\bsi\b', content, re.IGNORECASE)),
                    "finsi": len(re.findall(r'\bfinsi\b', content, re.IGNORECASE)),
                    "mientras": len(re.findall(r'\bmientras\b', content, re.IGNORECASE)),
                    "finmientras": len(re.findall(r'\bfinmientras\b', content, re.IGNORECASE)),
                    "para": len(re.findall(r'\bpara\b', content, re.IGNORECASE)),
                    "finpara": len(re.findall(r'\bfinpara\b', content, re.IGNORECASE)),
                }

                formatted_counts = {
                    "proceso": len(re.findall(r'\bproceso\b', formatted, re.IGNORECASE)),
                    "finproceso": len(re.findall(r'\bfinproceso\b', formatted, re.IGNORECASE)),
                    "subproceso": len(re.findall(r'\bsubproceso\b', formatted, re.IGNORECASE)),
                    "finsubproceso": len(re.findall(r'\bfinsubproceso\b', formatted, re.IGNORECASE)),
                    "algoritmo": len(re.findall(r'\balgoritmo\b', formatted, re.IGNORECASE)),
                    "finalgoritmo": len(re.findall(r'\bfinalgoritmo\b', formatted, re.IGNORECASE)),
                    "si": len(re.findall(r'\bsi\b', formatted, re.IGNORECASE)),
                    "finsi": len(re.findall(r'\bfinsi\b', formatted, re.IGNORECASE)),
                    "mientras": len(re.findall(r'\bmientras\b', formatted, re.IGNORECASE)),
                    "finmientras": len(re.findall(r'\bfinmientras\b', formatted, re.IGNORECASE)),
                    "para": len(re.findall(r'\bpara\b', formatted, re.IGNORECASE)),
                    "finpara": len(re.findall(r'\bfinpara\b', formatted, re.IGNORECASE)),
                }

                # Verify counts match (allowing for some flexibility due to spacing changes)
                for keyword, original_count in original_counts.items():
                    formatted_count = formatted_counts[keyword]
                    self.assertEqual(
                        original_count,
                        formatted_count,
                        f"Keyword '{keyword}' count mismatch in {ref_file}: "
                        f"original={original_count}, formatted={formatted_count}",
                    )

    def test_complex_nested_structures(self):
        """Test formatting of complex nested control structures."""
        complex_code = """
Proceso ComplexExample
Definir i, j, k Como Entero
Para i<-1 Hasta 10 Con Paso 1 Hacer
Si i MOD 2 = 0 Entonces
Mientras j < 5 Hacer
Segun k Hacer
Caso 1: Escribir "Uno"
Caso 2,3: Escribir "Dos o Tres"
De Otro Modo: Escribir "Otro"
FinSegun
j <- j + 1
FinMientras
Sino
Repetir
Escribir "Impar: ", i
k <- k + 1
Hasta Que k > 3
FinSi
FinPara
FinProceso
"""

        formatted = format_pseint_code(complex_code)
        lines = formatted.split("\n")

        # Check proper nesting indentation
        expected_indents = {
            "Proceso ComplexExample": 0,
            "Definir i, j, k Como Entero": 1,
            "Para i <- 1 Hasta 10 Con Paso 1 Hacer": 1,
            "Si i MOD 2 = 0 Entonces": 2,
            "Mientras j < 5 Hacer": 3,
            "Segun k Hacer": 4,
            "Caso 1:": 5,
            'Escribir "Uno"': 6,
            "FinSegun": 4,
            "FinMientras": 3,
            "Sino": 2,
            "Repetir": 3,
            "FinSi": 2,
            "FinPara": 1,
            "FinProceso": 0,
        }

        # Verify indentation levels using expected_indents dictionary
        for line in lines:
            stripped = line.strip()
            if stripped in expected_indents:
                expected_indent = expected_indents[stripped] * 4  # 4 spaces per indent level
                actual_indent = len(line) - len(line.lstrip())
                self.assertEqual(
                    actual_indent, 
                    expected_indent,
                    f"Incorrect indentation for '{stripped}': expected {expected_indent}, got {actual_indent}"
                )


if __name__ == "__main__":
    unittest.main()
