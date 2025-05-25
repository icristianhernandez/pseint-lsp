#!/usr/bin/env python3
"""
Test suite runner for PSeInt LSP formatter.
Runs all tests in organized categories with detailed reporting.
"""


import unittest
import sys
import os
from pathlib import Path
import importlib.util

# Add the parent directory to sys.path for imports
script_dir = Path(__file__).parent.absolute()
parent_dir = script_dir.parent
sys.path.insert(0, str(parent_dir))

def run_test_suite():
    """Run the complete test suite with categorized reporting."""
    
    print("=" * 70)
    print("PSeInt LSP Formatter - Comprehensive Test Suite")
    print("=" * 70)
    
    # Test categories and their descriptions
    test_categories = {
        "Core Formatter Tests": [
            "test_formatter.py",
            "test_edge_cases.py"
        ],
        "SubAlgoritmo Debug Tests": [
            "test_subalgoritmo_debug.py",
            "test_subalgoritmo_verification.py",
            "test_subalgoritmo_indent.py"
        ],
        "String Formatting Tests": [
            "test_string_formatting.py"
        ],
        "Integration Tests": [
            "test_integration.py",
            "test_comprehensive_integration.py",
            "test_real_world_code.py"
        ],
        "Server Tests": [
            "test_server.py"
        ],
        "Encoding Compatibility": [
            "test_encoding_compatibility.py",
            "test_encoding_investigation.py"
        ]
    }
    
    total_tests = 0
    total_failures = 0
    total_errors = 0
    
    for category, test_files in test_categories.items():
        print(f"\n🔍 {category}")
        print("-" * 50)
        
        category_tests = 0
        category_failures = 0
        category_errors = 0
        
        for test_file in test_files:
            test_path = script_dir / test_file
            if test_path.exists():
                print(f"  Running {test_file}...")
                
                # Load and run the test
                loader = unittest.TestLoader()
                try:
                    module_name = test_file[:-3]  # Remove .py extension
                    spec = importlib.util.spec_from_file_location(module_name, test_path)
                    if spec is None or spec.loader is None:
                        raise ImportError(f"Could not load spec for {test_file}")
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    suite = loader.loadTestsFromModule(module)
                    runner = unittest.TextTestRunner(verbosity=0, stream=open(os.devnull, 'w'))
                    result = runner.run(suite)
                    category_tests += result.testsRun
                    category_failures += len(result.failures)
                    category_errors += len(result.errors)
                    if result.failures or result.errors:
                        status = "❌ FAILED"
                        if result.failures:
                            status += f" ({len(result.failures)} failures)"
                        if result.errors:
                            status += f" ({len(result.errors)} errors)"
                    else:
                        status = "✅ PASSED"
                    print(f"    {status} - {result.testsRun} tests")
                except Exception as e:
                    print(f"    ⚠️  ERROR loading {test_file}: {e}")
                    category_errors += 1
            else:
                print(f"    ⚠️  {test_file} not found")
        
        print(f"  Category summary: {category_tests} tests, {category_failures} failures, {category_errors} errors")
        
        total_tests += category_tests
        total_failures += category_failures
        total_errors += category_errors
    
    # Final summary
    print("\n" + "=" * 70)
    print("FINAL SUMMARY")
    print("=" * 70)
    print(f"Total tests run: {total_tests}")
    print(f"Failures: {total_failures}")
    print(f"Errors: {total_errors}")
    
    if total_failures == 0 and total_errors == 0:
        print("🎉 ALL TESTS PASSED!")
        return True
    else:
        print("❌ Some tests failed. Check individual test output for details.")
        return False

def run_specific_category(category_name: str):
    """Run tests from a specific category only."""
    # This could be extended to allow running specific test categories
    pass

if __name__ == "__main__":
    success = run_test_suite()
    sys.exit(0 if success else 1)
