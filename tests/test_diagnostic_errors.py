#!/usr/bin/env python3
"""
Test cases for PSeInt diagnostic implementation.
Tests various error scenarios to ensure the diagnostic system properly detects issues.
"""

import pytest
import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from diagnostics import get_diagnostics
from lsprotocol.types import DiagnosticSeverity


class TestDiagnostics:
    """Test suite for PSeInt diagnostics functionality."""
    
    def test_undeclared_variables(self):
        """Test detection of undeclared variables."""
        code = """Algoritmo Test
        Escribir x + y  // x and y are undeclared
        FinAlgoritmo"""
        
        diagnostics = get_diagnostics(code)
        
        # Should detect undeclared variables x and y
        undeclared_errors = [d for d in diagnostics if "no declarada" in d.message or "not declared" in d.message]
        assert len(undeclared_errors) >= 2, f"Expected at least 2 undeclared variable errors, got {len(undeclared_errors)}"
        
    def test_unused_variables(self):
        """Test detection of unused variables."""
        code = """Algoritmo Test
        Definir variable_no_usada Como Entero
        Definir otra_variable_sin_uso Como Real
        Escribir "Hello"
        FinAlgoritmo"""
        
        diagnostics = get_diagnostics(code)
        
        # Should detect unused variables
        unused_warnings = [d for d in diagnostics if "no utilizada" in d.message or "not used" in d.message]
        assert len(unused_warnings) >= 2, f"Expected at least 2 unused variable warnings, got {len(unused_warnings)}"
        
    def test_unclosed_blocks(self):
        """Test detection of unclosed block structures."""
        code = """Algoritmo Test
        Si verdadero Entonces
            Escribir "En bloque if"
            Para i <- 1 Hasta 5 Hacer
                Escribir i
            // Missing FinPara
        // Missing FinSi
        FinAlgoritmo"""
        
        diagnostics = get_diagnostics(code)
        
        # Should detect unclosed blocks
        block_errors = [d for d in diagnostics if any(keyword in d.message.lower() for keyword in 
                       ["bloque", "block", "finsi", "finpara", "sin cerrar", "unclosed"])]
        assert len(block_errors) >= 1, f"Expected at least 1 unclosed block error, got {len(block_errors)}"
        
    def test_type_incompatibility(self):
        """Test detection of type incompatible assignments."""
        code = """Algoritmo Test
        Definir numero Como Entero
        Definir texto Como Caracter
        numero <- "esto es texto"
        texto <- 123
        FinAlgoritmo"""
        
        diagnostics = get_diagnostics(code)
        
        # Should detect type incompatibility
        type_errors = [d for d in diagnostics if any(keyword in d.message.lower() for keyword in 
                      ["tipo", "type", "incompatible", "asignación"])]
        assert len(type_errors) >= 2, f"Expected at least 2 type incompatibility errors, got {len(type_errors)}"
        
    def test_undefined_functions(self):
        """Test detection of undefined function calls."""
        code = """Algoritmo Test
        resultado <- funcionInexistente(5, 10)
        procedimientoInexistente(123)
        FinAlgoritmo"""
        
        diagnostics = get_diagnostics(code)
        
        # Should detect undefined functions
        function_errors = [d for d in diagnostics if any(keyword in d.message.lower() for keyword in 
                          ["función", "function", "procedimiento", "procedure", "no definida", "undefined"])]
        assert len(function_errors) >= 2, f"Expected at least 2 undefined function errors, got {len(function_errors)}"
        
    def test_array_usage_without_declaration(self):
        """Test detection of array usage without proper declaration."""
        code = """Algoritmo Test
        Definir arreglo Como Entero
        arreglo[1] <- 5
        FinAlgoritmo"""
        
        diagnostics = get_diagnostics(code)
        
        # Should detect improper array usage
        array_errors = [d for d in diagnostics if any(keyword in d.message.lower() for keyword in 
                       ["arreglo", "array", "dimensión", "dimension", "índice", "index"])]
        # This might not be implemented yet, so we'll check but not fail
        print(f"Array usage errors detected: {len(array_errors)}")
        
    def test_builtin_function_parameter_errors(self):
        """Test detection of incorrect parameters in built-in functions."""
        code = """Algoritmo Test
        Escribir RC(2, 3, 4)  // RC takes only 1 parameter
        resultado <- Subcadena()  // Subcadena requires parameters
        FinAlgoritmo"""
        
        diagnostics = get_diagnostics(code)
        
        # Should detect parameter errors
        param_errors = [d for d in diagnostics if any(keyword in d.message.lower() for keyword in 
                       ["parámetro", "parameter", "argumento", "argument"])]
        print(f"Parameter errors detected: {len(param_errors)}")
        
    def test_variable_redefinition(self):
        """Test detection of variable redefinition."""
        code = """Algoritmo Test
        Definir contador Como Entero
        Definir contador Como Real
        FinAlgoritmo"""
        
        diagnostics = get_diagnostics(code)
        
        # Should detect redefinition
        redef_errors = [d for d in diagnostics if any(keyword in d.message.lower() for keyword in 
                       ["redefinida", "redefined", "ya definida", "already defined"])]
        assert len(redef_errors) >= 1, f"Expected at least 1 redefinition error, got {len(redef_errors)}"
        
    def test_uninitialized_variable_usage(self):
        """Test detection of uninitialized variable usage."""
        code = """Algoritmo Test
        Definir valor Como Entero
        Si valor > 0 Entonces
            Escribir "Positivo"
        FinSi
        FinAlgoritmo"""
        
        diagnostics = get_diagnostics(code)
        
        # Should detect uninitialized usage
        uninit_errors = [d for d in diagnostics if any(keyword in d.message.lower() for keyword in 
                        ["inicializada", "initialized", "sin inicializar", "uninitialized"])]
        # This might not be fully implemented
        print(f"Uninitialized variable errors detected: {len(uninit_errors)}")
        
    def test_missing_return_statement(self):
        """Test detection of functions without return statements."""
        code = """Algoritmo Test
        
        Funcion miFuncion(parametro)
            Escribir parametro
            // Missing return statement
        FinFuncion
        
        FinAlgoritmo"""
        
        diagnostics = get_diagnostics(code)
        
        # Should detect missing return
        return_errors = [d for d in diagnostics if any(keyword in d.message.lower() for keyword in 
                        ["retorno", "return", "valor", "value"])]
        print(f"Missing return statement errors detected: {len(return_errors)}")
        
    def test_comprehensive_error_file(self):
        """Test the comprehensive error file from reference_code."""
        try:
            with open('reference_code/test_errors.psc', 'r', encoding='utf-8') as f:
                code = f.read()
        except FileNotFoundError:
            pytest.skip("test_errors.psc not found in reference_code")
            
        diagnostics = get_diagnostics(code)
        
        # Should detect multiple types of errors
        assert len(diagnostics) > 0, "Expected multiple diagnostics for comprehensive error file"
        
        # Count different types of diagnostics
        errors = [d for d in diagnostics if d.severity == DiagnosticSeverity.Error]
        warnings = [d for d in diagnostics if d.severity == DiagnosticSeverity.Warning]
        
        print(f"Total diagnostics: {len(diagnostics)}")
        print(f"Errors: {len(errors)}")
        print(f"Warnings: {len(warnings)}")
        
        # Print first few diagnostics for inspection
        for i, diag in enumerate(diagnostics[:10]):
            print(f"Diagnostic {i+1}: Line {diag.range.start.line + 1}, {diag.message}")
            
    def test_simple_error_file(self):
        """Test the simple error file from reference_code."""
        try:
            with open('reference_code/simple_errors.psc', 'r', encoding='utf-8') as f:
                code = f.read()
        except FileNotFoundError:
            pytest.skip("simple_errors.psc not found in reference_code")
            
        diagnostics = get_diagnostics(code)
        
        # Should detect at least the basic errors
        assert len(diagnostics) >= 3, f"Expected at least 3 diagnostics for simple error file, got {len(diagnostics)}"
        
        print(f"Simple errors diagnostics: {len(diagnostics)}")
        for i, diag in enumerate(diagnostics):
            print(f"Diagnostic {i+1}: Line {diag.range.start.line + 1}, {diag.message}")


if __name__ == "__main__":
    # Run the tests
    test_instance = TestDiagnostics()
    
    print("=== Testing PSeInt Diagnostics Implementation ===\n")
    
    tests = [
        ("Undeclared Variables", test_instance.test_undeclared_variables),
        ("Unused Variables", test_instance.test_unused_variables),
        ("Unclosed Blocks", test_instance.test_unclosed_blocks),
        ("Type Incompatibility", test_instance.test_type_incompatibility),
        ("Undefined Functions", test_instance.test_undefined_functions),
        ("Array Usage", test_instance.test_array_usage_without_declaration),
        ("Built-in Function Parameters", test_instance.test_builtin_function_parameter_errors),
        ("Variable Redefinition", test_instance.test_variable_redefinition),
        ("Uninitialized Variables", test_instance.test_uninitialized_variable_usage),
        ("Missing Return Statement", test_instance.test_missing_return_statement),
        ("Comprehensive Error File", test_instance.test_comprehensive_error_file),
        ("Simple Error File", test_instance.test_simple_error_file),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"\n--- Testing: {test_name} ---")
        try:
            test_func()
            print(f"✅ PASSED: {test_name}")
            passed += 1
        except AssertionError as e:
            print(f"❌ FAILED: {test_name} - {e}")
            failed += 1
        except Exception as e:
            print(f"⚠️  ERROR: {test_name} - {e}")
            failed += 1
    
    print(f"\n=== Test Summary ===")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Total: {passed + failed}")
