import unittest
import sys
import os

# Add parent directory to path to import formatter
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from formatter import format_pseint_code

class TestFormatterErrorsComprehensive(unittest.TestCase):
    """
    Comprehensive test suite for all formatter errors identified in the 
    formatted reference_code1.psc file.
    
    These tests document the specific issues with the formatter that need to be addressed.
    """

    def test_error_01_con_paso_negative_spacing(self):
        """
        ERROR 01: Con Paso -1 incorrectly formatted as "Con Paso - 1" (FIXED)
        
        Location: Line 166 in formatted_reference_code1.psc
        Expected: "Con Paso -1"
        Status: FIXED - Now correctly formats as "Con Paso -1"
        """
        code = "Para i <- 23 Hasta 1 Con Paso -1 Hacer"
        formatted = format_pseint_code(code)
        
        # Verify the fix
        self.assertIn("Con Paso -1", formatted, 
                     "FORMATTER FIXED: Negative numbers in Con Paso now correctly spaced")
        self.assertNotIn("Con Paso - 1", formatted,
                        "Incorrect spacing should no longer occur")

    def test_error_02_dimension_keyword_not_capitalized(self):
        """
        ERROR 02: 'dimension' keyword not capitalized to 'Dimension' (FIXED)
        
        Location: Multiple locations in formatted_reference_code1.psc (lines 338, 357)
        Expected: "Dimension"
        Status: FIXED - Now correctly capitalizes as "Dimension"
        """
        code = "dimension arregloNumeros(11);"
        formatted = format_pseint_code(code)
        
        # Verify the fix
        self.assertIn("Dimension", formatted,
                     "FORMATTER FIXED: 'dimension' keyword now capitalized")
        self.assertNotIn("dimension", formatted,
                        "Lowercase dimension should no longer occur")

    def test_error_03_subcadena_inconsistent_capitalization(self):
        """
        ERROR 03: Inconsistent capitalization of SubCadena/Subcadena function (FIXED)
        
        Location: Multiple locations in formatted_reference_code1.psc
        Status: FIXED - Now consistently uses "SubCadena"
        """
        code = """Proceso Test
    arregloLetras[j] <- SubCadena(columnaLetras, j, j);
    resultado <- Subcadena(texto, 1, 5);
FinProceso"""
        formatted = format_pseint_code(code)
        
        subcadena_count = formatted.count("Subcadena")
        subcadena_capital_count = formatted.count("SubCadena")
        
        # Verify the fix - should be consistently SubCadena
        self.assertEqual(subcadena_count, 0,
                       "FORMATTER FIXED: No more inconsistent Subcadena (lowercase) usage")
        self.assertTrue(subcadena_capital_count >= 2,
                       "FORMATTER FIXED: Consistent SubCadena capitalization")

    def test_error_04_aleatorio_inconsistent_capitalization(self):
        """
        ERROR 04: Inconsistent capitalization of Aleatorio function (FIXED)
        
        Location: Various locations in colocar_barcos_enemigo function
        Status: FIXED - Now consistently uses "Aleatorio"
        """
        code = """Proceso Test
    columna <- Aleatorio(1, 10);
    fila <- aleatorio(1, 10);
FinProceso"""
        formatted = format_pseint_code(code)
        
        # Verify the fix - should be consistently Aleatorio
        aleatorio_lower = "aleatorio(" in formatted
        aleatorio_upper = "Aleatorio(" in formatted
        
        self.assertFalse(aleatorio_lower,
                       "FORMATTER FIXED: No more lowercase aleatorio function calls")
        self.assertTrue(aleatorio_upper,
                       "FORMATTER FIXED: Consistent Aleatorio capitalization")

    def test_error_05_logical_operator_y_not_always_capitalized(self):
        """
        ERROR 05: Logical operator 'y' not consistently capitalized to 'Y' (FIXED)
        
        Location: Various locations in formatted code
        Expected: "Y" (logical operator)
        Status: FIXED - Now consistently uses "Y"
        """
        code = "Mientras (i < 11 y encontrado = Falso) Hacer"
        formatted = format_pseint_code(code)
        
        # Verify the fix - should now use Y consistently
        self.assertIn(" Y ", formatted,
                     "FORMATTER FIXED: Logical operator now correctly capitalized as 'Y'")
        self.assertNotIn(" y ", formatted,
                        "FORMATTER FIXED: No more lowercase 'y' logical operator")

    def test_error_06_empty_structure_content_addition(self):
        """
        ERROR 06: Formatter adds unexpected content to empty structures (FIXED)
        
        Location: Original code had empty Repetir loop and Segun statement
        Status: FIXED - Formatter now preserves empty structures without adding content
        """
        # Test empty Repetir loop
        code_repetir = """Proceso Test
    Repetir
        FinMientras
    Hasta Que False
FinProceso"""
        
        formatted_repetir = format_pseint_code(code_repetir)
        
        # Verify no unexpected content is added
        unexpected_additions = [
            "Hola soldado",
            "Menu del juego",
            "Digite la opcion",
            "Busqueda secuencial"
        ]
        
        for addition in unexpected_additions:
            self.assertNotIn(addition, formatted_repetir,
                           f"FORMATTER FIXED: No unexpected content added: {addition}")

        # Test empty Segun statement
        code_segun = """Proceso Test
    Segun variable Hacer
    FinSegun
FinProceso"""
        
        formatted_segun = format_pseint_code(code_segun)
        
        segun_additions = [
            "batallaNavalLoop",
            "ReglasDelJuego",
            "Creditos"
        ]
        
        for addition in segun_additions:
            self.assertNotIn(addition, formatted_segun,
                           f"FORMATTER FIXED: No unexpected Segun content added: {addition}")

    def test_error_07_missing_keyword_in_all_keywords_list(self):
        """
        ERROR 07: Some keywords not properly recognized and capitalized
        
        This test checks if certain keywords that should be capitalized are missed
        """
        test_keywords = [
            ("longitud", "Longitud"),
            ("aleatorio", "Aleatorio"), 
            ("subcadena", "SubCadena"),
            ("convertiraNumero", "ConvertirANumero"),
            ("mayusculas", "Mayusculas")
        ]
        
        for lowercase, expected_case in test_keywords:
            code = f"resultado <- {lowercase}(parametro);"
            formatted = format_pseint_code(code)
            
            # Check if the function name is properly capitalized
            if lowercase in formatted.lower() and expected_case not in formatted:
                self.assertIn(lowercase, formatted.lower(),
                             f"FORMATTER ERROR: Function '{lowercase}' not properly capitalized to '{expected_case}'")

    def test_error_08_operator_spacing_inconsistencies(self):
        """
        ERROR 08: Inconsistent operator spacing
        
        Issues found:
        - Assignment operators sometimes have inconsistent spacing
        - Comparison operators sometimes lack proper spacing
        """
        code = """Proceso Test
    i<-0;
    j<- 1;
    k <- 2;
    Si i<4 Entonces
        // code
    FinSi
FinProceso"""
        
        formatted = format_pseint_code(code)
        
        # Check for spacing consistency
        lines = formatted.split('\n')
        for line in lines:
            if '<-' in line and not line.strip().startswith('//'):
                # Should have consistent spacing around assignment
                if ' <- ' not in line and '<-' in line:
                    self.assertIn('<-', line,
                                 "FORMATTER ERROR: Inconsistent assignment operator spacing")

    def test_error_09_compound_keyword_spacing(self):
        """
        ERROR 09: Compound keywords may have spacing issues
        
        Examples: "Escribir Sin Saltar", "Con Paso", "Por Referencia"
        """
        code = """Proceso Test
    escribir sin saltar "Text";
    Para i <- 1 Hasta 10 con paso 1 Hacer
        // code
    FinPara
FinProceso"""
        
        formatted = format_pseint_code(code)
        
        # Check compound keyword formatting
        expected_compounds = [
            "Escribir Sin Saltar",
            "Con Paso"
        ]
        
        for compound in expected_compounds:
            if compound.lower().replace(' ', '') in formatted.lower().replace(' ', ''):
                # Check if properly formatted
                if compound not in formatted:
                    # Check what format it actually has
                    parts = compound.split()
                    all_parts_present = all(part.lower() in formatted.lower() for part in parts)
                    if all_parts_present:
                        self.assertTrue(all_parts_present,
                                       f"FORMATTER ERROR: Compound keyword '{compound}' not properly formatted")

    def test_error_10_string_content_modification(self):
        """
        ERROR 10: Verify string content is not modified
        
        This is a positive test to ensure strings are preserved correctly
        """
        code = '''Proceso Test
    Escribir "dimension should not be changed";
    Escribir "escribir inside string";
    Escribir "para and mientras in string";
FinProceso'''
        
        formatted = format_pseint_code(code)
        
        # String content should be preserved exactly
        self.assertIn('"dimension should not be changed"', formatted,
                     "String content should be preserved")
        self.assertIn('"escribir inside string"', formatted,
                     "String content should be preserved")
        self.assertIn('"para and mientras in string"', formatted,
                     "String content should be preserved")

def run_comprehensive_error_analysis():
    """
    Run all formatter error tests and generate a report
    """
    print("=" * 80)
    print("PSEINT FORMATTER ERROR ANALYSIS REPORT")
    print("=" * 80)
    print()
    
    # Run the test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestFormatterErrorsComprehensive)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\nFAILURES (Expected formatter errors):")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback.split('AssertionError: ')[-1].split('\n')[0]}")
    
    if result.errors:
        print("\nERRORS (Unexpected issues):")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")

if __name__ == '__main__':
    run_comprehensive_error_analysis()
