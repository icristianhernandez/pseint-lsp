import unittest
import sys
import os
from src.formatter import format_pseint_code

class TestFormatterErrorsFromReferenceCode(unittest.TestCase):
    """Test cases for specific formatter errors found in the formatted reference_code1.psc."""

    def test_con_paso_negative_number_spacing(self):
        """Test the Con Paso -1 spacing error found in the formatted code."""
        code = """SubProceso Animacion
    Para i <- 23 Hasta 1 Con Paso -1 Hacer
        Borrar Pantalla;
    FinPara
FinSubProceso"""
        
        formatted = format_pseint_code(code)
        
        # ERROR 01 FIX: The formatter should now correctly format "Con Paso -1" 
        self.assertIn("Con Paso -1", formatted, "Formatter should correctly format negative numbers")
        self.assertNotIn("Con Paso - 1", formatted, "Formatter should not incorrectly space negative numbers")

    def test_dimension_keyword_not_capitalized(self):
        """Test the dimension keyword capitalization error."""
        code = """SubAlgoritmo Test
    Definir arreglo Como Entero;
    dimension arregloNumeros(11);
FinSubAlgoritmo"""
        
        formatted = format_pseint_code(code)
        
        # ERROR 02 FIX: The formatter should now capitalize 'dimension' to 'Dimension'
        self.assertIn("Dimension arregloNumeros(11);", formatted, "Formatter should capitalize 'dimension'")
        self.assertNotIn("dimension arregloNumeros(11);", formatted, "Lowercase 'dimension' should be fixed")

    def test_logical_operator_y_not_capitalized(self):
        """Test that logical operator 'y' is not properly capitalized to 'Y'."""
        code = """Proceso Test
    Mientras (i < 11 y encontrado = Falso) Hacer
        i <- i + 1;
    FinMientras
FinProceso"""
        
        formatted = format_pseint_code(code)
        
        # ERROR 05 FIX: The formatter should now capitalize 'y' to 'Y' consistently
        self.assertIn("Y encontrado", formatted, "Formatter should capitalize 'y' to 'Y'")
        self.assertNotIn("y encontrado", formatted, "Lowercase 'y' should be fixed")

    def test_subcadena_function_capitalization(self):
        """Test Subcadena function name capitalization inconsistency."""
        code = """Proceso Test
    arregloLetras[j] <- SubCadena(columnaLetras, j, j);
    resultado <- Subcadena(texto, 1, 5);
FinProceso"""
        
        formatted = format_pseint_code(code)
        
        # ERROR 03 FIX: Should now have consistent capitalization (SubCadena)
        self.assertIn("SubCadena(columnaLetras, j, j)", formatted, "Function should be SubCadena")
        self.assertIn("SubCadena(Texto, 1, 5)", formatted, "Function should be consistently SubCadena")
        self.assertNotIn("Subcadena(", formatted, "Inconsistent casing should be fixed")

    def test_mayusculas_function_usage(self):
        """Test that Mayusculas function is properly formatted."""
        code = """Proceso Test
    dato <- Mayusculas(dato);
    confirmacion <- Mayusculas(confirmacion);
FinProceso"""
        
        formatted = format_pseint_code(code)
        
        # Should maintain proper function name capitalization
        self.assertIn("Mayusculas(dato)", formatted)
        self.assertIn("Mayusculas(confirmacion)", formatted)

    def test_escribir_sin_saltar_spacing(self):
        """Test 'Escribir Sin Saltar' compound keyword spacing."""
        code = """Proceso Test
    Escribir sin saltar "Digite la opcion de menu:";
    escribir Sin Saltar "Texto: ";
FinProceso"""
        
        formatted = format_pseint_code(code)
        
        # Should properly format compound keywords
        self.assertIn("Escribir Sin Saltar", formatted)
        # Should not have inconsistent casing
        self.assertNotIn("escribir Sin Saltar", formatted)

    def test_longitud_vs_length_function(self):
        """Test function name consistency for length operations."""
        code = """Proceso Test
    Si longitud(nombre_jugador) >= min_longitud Entonces
        // code
    FinSi
    Si Longitud(logo[j]) > 0 Entonces
        // code
    FinSi
FinProceso"""
        
        formatted = format_pseint_code(code)
        
        # ERROR 07 FIX: Check for consistent function name capitalization
        self.assertIn("Longitud(nombre_jugador)", formatted, "Function should be consistently Longitud")
        self.assertIn("Longitud(logo[j])", formatted, "Function should be consistently Longitud")
        longitud_count = formatted.count("longitud(")
        self.assertEqual(longitud_count, 0, "Should not have lowercase longitud function calls")

    def test_aleatorio_function_formatting(self):
        """Test Aleatorio function formatting."""
        code = """Proceso Test
    columna <- Aleatorio(1, 10);
    fila <- aleatorio(1, 10);
FinProceso"""
        
        formatted = format_pseint_code(code)
        
        # ERROR 04 FIX: Should consistently capitalize function names
        self.assertIn("Aleatorio(1, 10)", formatted, "Function should be consistently Aleatorio")
        aleatorio_count = formatted.count("aleatorio(")
        self.assertEqual(aleatorio_count, 0, "Should not have lowercase aleatorio function calls")

    def test_convertir_a_numero_function(self):
        """Test ConvertirANumero function formatting."""
        code = """Proceso Test
    datonumerico <- ConvertirANumero(dato);
FinProceso"""
        
        formatted = format_pseint_code(code)
        
        # Should maintain proper function name
        self.assertIn("ConvertirANumero(dato)", formatted)

    def test_empty_repetir_content_addition(self):
        """Test that formatter doesn't add unexpected content to empty structures."""
        # This is based on the original code having empty Repetir/FinMientras
        code = """Proceso BatallaNavalMain
    Repetir
        FinMientras
    Hasta Que datonumerico == 4
FinProceso"""
        
        formatted = format_pseint_code(code)
        
        # ERROR 06 FIX: The formatter should now preserve empty structures without adding content
        self.assertNotIn("Hola soldado", formatted, "Formatter should not add unexpected menu content")
        self.assertIn("Repetir", formatted, "Repetir keyword should be preserved")
        self.assertIn("FinMientras", formatted, "FinMientras should be preserved")
        self.assertIn("Hasta Que", formatted, "Hasta Que should be preserved")

    def test_segun_empty_cases_handling(self):
        """Test handling of Segun statements with missing case content."""
        code = """Proceso Test
    Segun datonumerico Hacer
    FinSegun
FinProceso"""
        
        formatted = format_pseint_code(code)
        
        # ERROR 06 FIX: Check how formatter handles empty Segun blocks (should preserve them)
        self.assertIn("Segun datonumerico Hacer", formatted, "Segun statement should be preserved")
        self.assertIn("FinSegun", formatted, "FinSegun should be preserved")
        
        # Should not add unexpected content
        self.assertNotIn("batallaNavalLoop", formatted, "Formatter should not add unexpected case content")

if __name__ == '__main__':
    # Run tests and capture results
    unittest.main(verbosity=2)
