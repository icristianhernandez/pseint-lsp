"""
Tests for string formatting issues in the PSeInt formatter.
This test file focuses on preserving content inside string literals while still
applying proper formatting to the code outside of strings.
"""

import pytest
import sys
import os

# Add the parent directory to the path to import the formatter
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from formatter import format_pseint_code


class TestStringFormatting:
    """Test cases for string literal preservation during formatting."""

    def test_simple_strings_preserved(self):
        """Test that simple strings are preserved without modification."""
        code = '''Proceso Test
    Escribir "Hello World";
    Escribir "This is a test";
FinProceso'''
        
        result = format_pseint_code(code)
        assert '"Hello World"' in result
        assert '"This is a test"' in result

    def test_strings_with_keywords_preserved(self):
        """Test that strings containing PSeInt keywords are not modified."""
        code = '''Proceso Test
    Escribir "proceso inside string";
    Escribir "si entonces sino";
    Escribir "para hasta con paso";
FinProceso'''
        
        result = format_pseint_code(code)
        # Keywords inside strings should remain lowercase
        assert '"proceso inside string"' in result
        assert '"si entonces sino"' in result
        assert '"para hasta con paso"' in result

    def test_ascii_art_strings(self):
        """Test that ASCII art in strings is preserved exactly."""
        code = '''Proceso Test
    Escribir "... GOLDEN       ****  ****  ****    **    ****  *    *  *****      *     ...";
    Escribir "...      BYTES   *  *  *  *  *      *   *  *     * *  *    *       * *    ...";
FinProceso'''
        
        result = format_pseint_code(code)
        # ASCII art should be preserved exactly
        assert '"... GOLDEN       ****  ****  ****    **    ****  *    *  *****      *     ..."' in result
        assert '"...      BYTES   *  *  *  *  *      *   *  *     * *  *    *       * *    ..."' in result

    def test_strings_with_special_characters(self):
        """Test strings with special characters and symbols."""
        code = '''Proceso Test
    Escribir "8 888888888o           .8.    8888888 8888888888    .8.";
    Escribir ".8? `8. `88888.   8 8888   .8?   `8. `88888.";
    Escribir "Universidad Tecnológica Nacional";
FinProceso'''
        
        result = format_pseint_code(code)
        assert '"8 888888888o           .8.    8888888 8888888888    .8."' in result
        assert '".8? `8. `88888.   8 8888   .8?   `8. `88888."' in result
        assert '"Universidad Tecnológica Nacional"' in result

    def test_mixed_quotes_in_strings(self):
        """Test strings with mixed single and double quotes."""
        code = '''Proceso Test
    Escribir "This has 'single quotes' inside";
    Escribir 'This has "double quotes" inside';
FinProceso'''
        
        result = format_pseint_code(code)
        assert '"This has \'single quotes\' inside"' in result
        assert '\'This has "double quotes" inside\'' in result

    def test_strings_with_operators(self):
        """Test that operators inside strings are not modified."""
        code = '''Proceso Test
    Escribir "x <- y + z * 2";
    Escribir "if a = b then c >= d";
FinProceso'''
        
        result = format_pseint_code(code)
        # Operators inside strings should not get spaces added
        assert '"x <- y + z * 2"' in result
        assert '"if a = b then c >= d"' in result

    def test_strings_with_commas_and_semicolons(self):
        """Test that punctuation inside strings is preserved."""
        code = '''Proceso Test
    Escribir "Hello, World; This is a test.";
    Escribir "One,Two,Three;Four";
FinProceso'''
        
        result = format_pseint_code(code)
        assert '"Hello, World; This is a test."' in result
        assert '"One,Two,Three;Four"' in result

    def test_multiline_string_assignment(self):
        """Test string assignments to array elements."""
        code = '''Proceso Test
    logo[1] <- "      8 888888888o           .8.    8888888 8888888888    .8.";
    logo[2] <- "      8 8888    `88.        .888.         8 8888         .888.";
FinProceso'''
        
        result = format_pseint_code(code)
        # The assignment operator should get proper spacing, but string content preserved
        assert 'logo[1] <- "      8 888888888o           .8.    8888888 8888888888    .8."' in result
        assert 'logo[2] <- "      8 8888    `88.        .888.         8 8888         .888."' in result

    def test_code_with_keywords_outside_strings_formatted(self):
        """Test that keywords outside strings are properly formatted."""
        code = '''proceso test
    definir x como entero;
    escribir "string content";
    si x = 5 entonces
        escribir "inside if";
    finsi
finproceso'''
        
        result = format_pseint_code(code)
        # Keywords outside strings should be properly cased
        assert 'Proceso Test' in result or 'Proceso test' in result
        assert 'Definir x Como Entero' in result
        assert 'Si x = 5 Entonces' in result
        # String content should remain unchanged
        assert '"string content"' in result
        assert '"inside if"' in result

    def test_complex_line_with_strings_and_operators(self):
        """Test a complex line mixing strings with operators and keywords."""
        code = '''Proceso Test
    Escribir "Hola soldado ", nombre_jugador, ". Este es el Menu del juego.";
    Escribir "El total de las ventas es de ", sumaVentas;
FinProceso'''
        
        result = format_pseint_code(code)
        # String literals should be preserved, commas should have proper spacing
        assert '"Hola soldado "' in result
        assert 'nombre_jugador' in result
        assert '". Este es el Menu del juego."' in result
        assert '"El total de las ventas es de "' in result
        assert 'sumaVentas' in result

    def test_string_with_escaped_quotes(self):
        """Test strings containing escaped quotes."""
        code = '''Proceso Test
    Escribir "He said \\"Hello World\\"";
    Escribir 'She replied \\'Good morning\\'';
FinProceso'''
        
        result = format_pseint_code(code)
        # Escaped quotes should be preserved
        assert '"He said \\"Hello World\\""' in result
        assert '\'She replied \\\'Good morning\\\'\'' in result

    def test_empty_strings(self):
        """Test empty strings are handled correctly."""
        code = '''Proceso Test
    Escribir "";
    Escribir '';
    x <- "";
FinProceso'''
        
        result = format_pseint_code(code)
        assert 'Escribir "";' in result
        assert "Escribir '';" in result
        assert 'x <- "";' in result

    def test_long_strings_with_whitespace(self):
        """Test long strings with internal whitespace patterns."""
        code = '''Proceso Test
    Escribir "                    PARA UNA MEJOR EXPERIENCIA DE JUEGO";
    Escribir "                 ABRA A PANTALLA COMPLETA Y PRESIONE ENTER";
FinProceso'''
        
        result = format_pseint_code(code)
        # Internal whitespace in strings should be preserved exactly
        assert '"                    PARA UNA MEJOR EXPERIENCIA DE JUEGO"' in result
        assert '"                 ABRA A PANTALLA COMPLETA Y PRESIONE ENTER"' in result

    def test_strings_in_conditions_and_loops(self):
        """Test strings within control structures."""
        code = '''Proceso Test
    Si nombre = "admin" Entonces
        Escribir "Welcome administrator";
    FinSi
    Para i <- 1 Hasta 5 Hacer
        Escribir "Iteration ", i;
    FinPara
FinProceso'''
        
        result = format_pseint_code(code)
        assert '"admin"' in result
        assert '"Welcome administrator"' in result
        assert '"Iteration "' in result

    def test_real_world_example_from_reference(self):
        """Test a real example from the reference code."""
        code = '''SubAlgoritmo textoEstatico
    Escribir "                                                     ............................................................................. ";
    Escribir "                                                     ... GOLDEN       ****  ****  ****    **    ****  *    *  *****      *     ... ";
    Escribir "                                                     ...      BYTES   *  *  *  *  *      *   *  *     * *  *    *       * *    ... ";
    Escribir "                                                     ...              ****  ****  ***      \\    ***   *  * *    *      *   *   ... ";
FinSubAlgoritmo'''
        
        result = format_pseint_code(code)
        # All the ASCII art should be preserved exactly
        assert '"                                                     ............................................................................. "' in result
        assert '"                                                     ... GOLDEN       ****  ****  ****    **    ****  *    *  *****      *     ... "' in result
        assert '"                                                     ...      BYTES   *  *  *  *  *      *   *  *     * *  *    *       * *    ... "' in result
        assert '"                                                     ...              ****  ****  ***      \\    ***   *  * *    *      *   *   ... "' in result

    def test_caso_statements_with_inline_code(self):
        """Test that Caso statements with inline code are properly formatted."""
        code = '''Proceso Test
    Segun x Hacer
        Caso 1,2,3:Escribir "Bajo";
        Caso 4,5,6:
            Escribir "Medio";
        De Otro Modo:Escribir "Fuera de rango";
    FinSegun
FinProceso'''
        
        result = format_pseint_code(code)
        # The formatter should split inline statements after Caso into separate lines
        assert 'Caso 1,2,3:' in result
        assert 'Escribir "Bajo"' in result
        assert 'Caso 4,5,6:' in result  
        assert 'Escribir "Medio"' in result
        assert 'De Otro Modo:' in result
        assert 'Escribir "Fuera de rango"' in result
        # Check that commas in Caso statements don't have spaces
        assert '1,2,3' in result  # Not '1, 2, 3'

if __name__ == "__main__":
    pytest.main([__file__])
