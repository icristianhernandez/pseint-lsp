import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from formatter import format_pseint_code

class TestFormatterErrors(unittest.TestCase):
    """Test cases for identified formatter errors in the formatted reference code."""

    def test_empty_repetir_loop_handling(self):
        """Test that empty Repetir loops are handled correctly."""
        code = """Proceso Test
    Repetir
        FinMientras
    Hasta Que False
FinProceso"""
        
        formatted = format_pseint_code(code)
        # The formatter should not add unexpected content to empty structures
        self.assertIn("Repetir", formatted)
        self.assertIn("Hasta Que", formatted)
        # Should not contain unexpected additions like menu code
        self.assertNotIn("Hola soldado", formatted)

    def test_empty_segun_statement_handling(self):
        """Test that empty Segun statements are handled correctly."""
        code = """Proceso Test
    Segun variable Hacer
    FinSegun
FinProceso"""
        
        formatted = format_pseint_code(code)
        # Should preserve the empty Segun structure
        self.assertIn("Segun variable Hacer", formatted)
        self.assertIn("FinSegun", formatted)
        # Should not add unexpected case statements
        self.assertNotIn("batallaNavalLoop", formatted)

    def test_operator_spacing_with_negative_numbers(self):
        """Test spacing around Con Paso with negative numbers."""
        code = """Proceso Test
    Para i <- 23 Hasta 1 Con Paso -1 Hacer
        Escribir i;
    FinPara
FinProceso"""
        
        formatted = format_pseint_code(code)
        # Should maintain proper spacing around "Con Paso -1"
        # The formatter incorrectly formats this as "Con Paso - 1"
        self.assertIn("Con Paso -1", formatted)
        self.assertNotIn("Con Paso - 1", formatted)

    def test_keyword_case_consistency_dimension(self):
        """Test that 'dimension' keyword is properly capitalized."""
        code = """Proceso Test
    Definir arreglo Como Entero;
    dimension arreglo[10];
FinProceso"""
        
        formatted = format_pseint_code(code)
        # Should capitalize 'dimension' to 'Dimension'
        self.assertIn("Dimension arreglo[10];", formatted)
        self.assertNotIn("dimension arreglo[10];", formatted)

    def test_escribir_case_consistency(self):
        """Test that 'escribir' keyword is properly capitalized."""
        code = """Proceso Test
    escribir "Hello";
FinProceso"""
        
        formatted = format_pseint_code(code)
        # Should capitalize 'escribir' to 'Escribir'
        self.assertIn("Escribir \"Hello\";", formatted)
        self.assertNotIn("escribir \"Hello\";", formatted)

    def test_operator_spacing_assignment(self):
        """Test spacing around assignment operators."""
        code = """Proceso Test
    i<-0;
    j <- i +1;
FinProceso"""
        
        formatted = format_pseint_code(code)
        # Should have consistent spacing around assignment operators
        self.assertIn("i <- 0;", formatted)
        self.assertIn("j <- i + 1;", formatted)

    def test_logical_operator_spacing(self):
        """Test spacing around logical operators."""
        code = """Proceso Test
    mientras (i<4 y encontrado = Falso ) Hacer
        // code
    FinMientras
FinProceso"""
        
        formatted = format_pseint_code(code)
        # Should have proper spacing around operators
        self.assertIn("Mientras (i < 4 Y encontrado = Falso) Hacer", formatted)

    def test_function_call_spacing(self):
        """Test spacing in function calls."""
        code = """Proceso Test
    Si (Subcadena(opcionNumeros,i,i) == dato) Entonces
        // code
    FinSi
FinProceso"""
        
        formatted = format_pseint_code(code)
        # Should have proper spacing in function parameters and correct capitalization
        self.assertIn("SubCadena(opcionNumeros, i, i)", formatted)

    def test_comment_spacing_consistency(self):
        """Test that comment spacing is consistent."""
        code = """Proceso Test
    Escribir "3- Creditos";// comment without space
    Escribir "4- Salir"; // comment with space
FinProceso"""
        
        formatted = format_pseint_code(code)
        # Comments should have consistent spacing
        lines = formatted.split('\n')
        comment_lines = [line for line in lines if '//' in line and 'Escribir' in line]
        for line in comment_lines:
            # All comments should have a space after //
            comment_part = line.split('//')[1]
            self.assertTrue(comment_part.startswith(' '), f"Comment should start with space: {line}")

    def test_string_literal_preservation(self):
        """Test that content within string literals is preserved."""
        code = '''Proceso Test
    Escribir "escribir should not be capitalized here";
    Escribir "dimension should stay lowercase";
FinProceso'''
        
        formatted = format_pseint_code(code)
        # Keywords inside strings should not be modified
        self.assertIn('"escribir should not be capitalized here"', formatted)
        self.assertIn('"dimension should stay lowercase"', formatted)

    def test_segun_case_structure_preservation(self):
        """Test that Segun/Caso structures maintain proper format."""
        code = """Proceso Test
    Segun variable Hacer
        1:
        Escribir "One";
        2:
        Escribir "Two";
    De Otro Modo:
        Escribir "Default";
    FinSegun
FinProceso"""
        
        formatted = format_pseint_code(code)
        # Should preserve case structure properly
        self.assertIn("Segun variable Hacer", formatted)
        self.assertIn("1:", formatted)
        self.assertIn("2:", formatted)
        self.assertIn("De Otro Modo:", formatted)
        self.assertIn("FinSegun", formatted)

    def test_incomplete_structure_handling(self):
        """Test handling of incomplete structures that appear in original code."""
        code = """Proceso Test
    Repetir
        FinMientras
    Hasta Que False
FinProceso"""
        
        formatted = format_pseint_code(code)
        # Should not add unrelated content to fix incomplete structures
        # The formatter incorrectly added menu-related code
        self.assertNotIn("Digite la opcion de menu", formatted)
        self.assertNotIn("Busqueda secuencial", formatted)

if __name__ == '__main__':
    unittest.main()
