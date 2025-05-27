import unittest
import sys
import os

# Add the parent directory to sys.path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.formatter import format_pseint_code


class TestPSeIntFormatterEdgeCases(unittest.TestCase):
    """Edge case tests for the PSeInt formatter."""

    def test_empty_input(self):
        """Test formatting empty input."""
        result = format_pseint_code("")
        self.assertEqual(result, "")

    def test_whitespace_only_input(self):
        """Test formatting whitespace-only input."""
        result = format_pseint_code("   \n  \t  \n   ")
        self.assertEqual(result, "")

    def test_comments_only(self):
        """Test formatting file with only comments."""
        input_code = """
// This is a comment
// Another comment
// Yet another comment
"""
        result = format_pseint_code(input_code)
        lines = result.split("\n")
        for line in lines:
            if line.strip():
                self.assertTrue(line.strip().startswith("//"))

    def test_mixed_quotes_in_strings(self):
        """Test handling of mixed quote types in strings."""
        input_code = "Escribir \"String with 'single quotes' inside\""
        result = format_pseint_code(input_code)
        self.assertIn("String with 'single quotes' inside", result)

    def test_nested_quotes(self):
        """Test handling of nested quotes."""
        input_code = """
Proceso Test
    Escribir "He said: \\"Hello world\\""
    Escribir 'She replied: "How are you?"'
FinProceso
"""
        result = format_pseint_code(input_code)
        self.assertIn('He said: \\"Hello world\\"', result)
        self.assertIn('She replied: "How are you?"', result)

    def test_very_long_lines(self):
        """Test formatting of very long lines."""
        long_variable_name = "very_long_variable_name_that_exceeds_normal_length"
        input_code = f"""
Proceso Test
    Definir {long_variable_name} Como Entero
    {long_variable_name} <- 12345 + 67890 + 11111 + 22222 + 33333 + 44444 + 55555
    Escribir "This is a very long string that contains many words and should test how the formatter handles very long lines of code"
FinProceso
"""
        result = format_pseint_code(input_code)
        # Should not break or modify the structure
        self.assertIn("Proceso Test", result)
        self.assertIn("FinProceso", result)
        self.assertIn(long_variable_name, result)

    def test_special_characters_in_strings(self):
        """Test handling of special characters in strings."""
        input_code = """
Proceso Test
    Escribir "Special chars: áéíóú ñ ¡¿ @#$%^&*()+={}[]|\\:;'<>,.?/"
    Escribir "Unicode: 🙂 ⭐ 🚀 💯"
FinProceso
"""
        result = format_pseint_code(input_code)
        self.assertIn("Special chars: áéíóú ñ ¡¿ @#$%^&*()+={}[]|\\:;'<>,.?/", result)
        self.assertIn("Unicode: 🙂 ⭐ 🚀 💯", result)

    def test_malformed_control_structures(self):
        """Test handling of malformed control structures."""
        input_code = """
Proceso Test
    Si x > 0 Entonces
        Escribir "Positive"
    // Missing FinSi
    Para i <- 1 Hasta 10 Hacer
        Escribir i
    // Missing FinPara
FinProceso
"""
        # Should not crash
        result = format_pseint_code(input_code)
        self.assertIn("Proceso Test", result)
        self.assertIn("FinProceso", result)

    def test_multiple_blank_lines(self):
        """Test handling of multiple consecutive blank lines."""
        input_code = """
Proceso Test



    Escribir "Hello"



    Escribir "World"




FinProceso
"""
        result = format_pseint_code(input_code)
        lines = result.split("\n")

        # Should reduce multiple blank lines
        consecutive_blank_count = 0
        max_consecutive_blank = 0
        for line in lines:
            if line.strip() == "":
                consecutive_blank_count += 1
                max_consecutive_blank = max(
                    max_consecutive_blank, consecutive_blank_count
                )
            else:
                consecutive_blank_count = 0

        # Should not have more than 1 consecutive blank line
        self.assertLessEqual(max_consecutive_blank, 1)

    def test_keywords_in_different_cases(self):
        """Test keyword recognition in different cases."""
        input_code = """
PROCESO Test
    DEFINIR x COMO ENTERO
    si x > 0 entonces
        escribir "positive"
    finsi
finproceso
"""
        result = format_pseint_code(input_code)

        # Should normalize to proper case
        self.assertIn("Proceso Test", result)
        self.assertIn("Definir x Como Entero", result)
        self.assertIn("Si x > 0 Entonces", result)
        self.assertIn('Escribir "positive"', result)
        self.assertIn("FinSi", result)
        self.assertIn("FinProceso", result)

    def test_operators_spacing(self):
        """Test spacing around various operators."""
        input_code = """
Proceso Test
    x<-5+3*2-1/4
    y<=(x>=10)Y(x<=20)
    z<>x&y|NO(x<>5)
    result<-x MOD y
FinProceso
"""
        result = format_pseint_code(input_code)

        # Check that operators have proper spacing
        self.assertIn("x <- 5 + 3 * 2 - 1 / 4", result)
        self.assertIn("y <= (x >= 10) Y (x <= 20)", result)
        self.assertIn("z <> x & y | NO (x <> 5)", result)
        self.assertIn("result <- x MOD y", result)

    def test_function_calls_and_parameters(self):
        """Test formatting of function calls with parameters."""
        input_code = """
SubProceso Saludo(nombre,apellido,edad)
    Escribir"Hola",nombre,apellido,"tienes",edad,"años"
FinSubProceso

Proceso Test
    Saludo("Juan","Pérez",25)
FinProceso
"""
        result = format_pseint_code(input_code)

        # Check proper spacing in function calls and parameters
        self.assertIn("SubProceso Saludo(nombre, apellido, edad)", result)
        self.assertIn(
            'Escribir "Hola", nombre, apellido, "tienes", edad, "años"', result
        )
        self.assertIn('Saludo("Juan", "Pérez", 25)', result)

    def test_array_operations(self):
        """Test formatting of array operations."""
        input_code = """
Proceso Test
    Dimension matriz[10,20]
    matriz[1,2]<-5
    valor<-matriz[i+1,j*2]
    Para i<-0 Hasta 9 Hacer
        matriz[i,0]<-i*2
    FinPara
FinProceso
"""
        result = format_pseint_code(input_code)

        # Check array formatting
        self.assertIn("Dimension matriz[10, 20]", result)
        self.assertIn("matriz[1, 2] <- 5", result)
        self.assertIn("valor <- matriz[i + 1, j * 2]", result)
        self.assertIn("matriz[i, 0] <- i * 2", result)

    def test_inline_comments(self):
        """Test handling of inline comments."""
        input_code = """
Proceso Test
    x <- 5 // This is a comment
    Escribir x//Another comment
    y<-10//Comment without space
FinProceso
"""
        result = format_pseint_code(input_code)

        # Check that inline comments are properly spaced
        self.assertIn("x <- 5 // This is a comment", result)
        self.assertIn("Escribir x // Another comment", result)
        self.assertIn("y <- 10 // Comment without space", result)

    def test_case_statements_with_ranges(self):
        """Test Caso statements with value ranges."""
        input_code = """
Proceso Test
    Segun x Hacer
        Caso 1,2,3:Escribir"Bajo"
        Caso 4,5,6:
            Escribir"Medio"
        Caso 7,8,9:Escribir"Alto"
        De Otro Modo:Escribir"Fuera de rango"
    FinSegun
FinProceso
"""
        result = format_pseint_code(input_code)

        # Check proper formatting of Caso statements
        self.assertIn("Caso 1,2,3:", result)
        self.assertIn('Escribir "Bajo"', result)
        self.assertIn("Caso 4,5,6:", result)
        self.assertIn('Escribir "Medio"', result)
        self.assertIn("De Otro Modo:", result)
        self.assertIn('Escribir "Fuera de rango"', result)

    def test_repetir_hasta_que_structure(self):
        """Test Repetir...Hasta Que structure formatting."""
        input_code = """
Proceso Test
    Repetir
        Escribir"Introduce un número:"
        Leer num
        Si num<0 Entonces
            Escribir"Número negativo"
        FinSi
    Hasta Que num>=0
FinProceso
"""
        result = format_pseint_code(input_code)

        # Check proper indentation and formatting
        lines = result.split("\n")
        in_repetir = False
        for line in lines:
            stripped = line.strip()
            if stripped == "Repetir":
                in_repetir = True
            elif stripped.startswith("Hasta Que"):
                in_repetir = False
            elif in_repetir and stripped and not stripped.startswith("//"):
                # Lines inside Repetir should be indented
                self.assertTrue(
                    line.startswith("        "),
                    f"Line in Repetir should be indented: '{line}'",
                )


if __name__ == "__main__":
    unittest.main()
