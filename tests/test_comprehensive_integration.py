#!/usr/bin/env python3
"""
Comprehensive test of the formatter with actual reference code.    # Save the formatted result for manual inspection
    with open('../formatted_reference_code1.psc', 'w', encoding='utf-8') as f:
        f.write(formatted_code)
    print("\n📝 Formatted code saved to '../formatted_reference_code1.psc'")s tests the string formatting improvements to ensure they work correctly
with the complex strings found in the reference PSeInt code.
"""

import sys
import os

# Add the parent directory to the path to import the formatter
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from formatter import format_pseint_code


def test_full_reference_code():
    """Test the formatter with the complete reference_code1.psc file."""
    
    # Read the reference code
    with open('../reference_code/reference_code1.psc', 'r', encoding='utf-8') as f:
        original_code = f.read()
    
    print("Testing formatter with complete reference_code1.psc...")
    
    # Format the code
    try:
        formatted_code = format_pseint_code(original_code)
        print("✅ Formatting completed successfully!")
    except Exception as e:
        print(f"❌ Formatting failed: {e}")
        return False
    
    # Key strings that should be preserved exactly
    critical_strings = [
        '"                    PARA UNA MEJOR EXPERIENCIA DE JUEGO"',
        '"                 ABRA A PANTALLA COMPLETA Y PRESIONE ENTER"',
        '"                                                                            Universidad Tecnologica Nacional"',
        '"                                                     ............................................................................. "',
        '"                                                     ... GOLDEN       ****  ****  ****    **    ****  *    *  *****      *     ... "',
        '"                                                     ...      BYTES   *  *  *  *  *      *   *  *     * *  *    *       * *    ... "',
        '"      8 888888888o           .8.    8888888 8888888888    .8.          8 8888         8 8888                  .8."',
        '"      8 8888    `88.        .888.         8 8888         .888.         8 8888         8 8888                 .888."',
        '"                                                                              ��� Bienvenido Soldado !!!"'
    ]
    
    # Check that all critical strings are preserved
    preserved_count = 0
    for critical_string in critical_strings:
        if critical_string in formatted_code:
            print(f"✅ Preserved: {critical_string[:50]}...")
            preserved_count += 1
        else:
            print(f"❌ Missing: {critical_string[:50]}...")
    
    print(f"\nPreserved {preserved_count}/{len(critical_strings)} critical strings")
    
    # Check that keywords outside strings are properly formatted
    keyword_checks = [
        'SubAlgoritmo',  # Should be proper cased
        'FinSubAlgoritmo',  # Should be proper cased
        'Proceso',  # Should be proper cased
        'FinProceso',  # Should be proper cased
        'Definir',  # Should be proper cased
        'Como',  # Should be proper cased
    ]
    
    keyword_found = 0
    for keyword in keyword_checks:
        if keyword in formatted_code:
            keyword_found += 1
            print(f"✅ Found proper keyword: {keyword}")
        else:
            print(f"❌ Missing proper keyword: {keyword}")
    
    print(f"\nFound {keyword_found}/{len(keyword_checks)} properly formatted keywords")
    
    # Check that operators have proper spacing (outside of strings)
    operator_checks = [
        ' <- ',  # Assignment
        ' = ',   # Equality
    ]
    
    operator_found = 0
    for op in operator_checks:
        if op in formatted_code:
            operator_found += 1
            print(f"✅ Found properly spaced operator: {repr(op)}")
    
    print(f"\nFound {operator_found}/{len(operator_checks)} properly spaced operators")
    
    # Save the formatted code for manual inspection
    with open('formatted_reference_code1.psc', 'w', encoding='utf-8') as f:
        f.write(formatted_code)
    print("\n📝 Formatted code saved to 'formatted_reference_code1.psc'")
    
    # Summary
    total_checks = len(critical_strings) + len(keyword_checks) + len(operator_checks)
    passed_checks = preserved_count + keyword_found + operator_found
    
    print(f"\n📊 Summary: {passed_checks}/{total_checks} checks passed")
    
    if passed_checks == total_checks:
        print("🎉 All tests passed! The formatter correctly handles complex strings.")
        return True
    else:
        print("⚠️  Some checks failed. Review the output above.")
        return False


if __name__ == "__main__":
    success = test_full_reference_code()
    sys.exit(0 if success else 1)
