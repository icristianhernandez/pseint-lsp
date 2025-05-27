#!/usr/bin/env python3
"""
Final verification that the SubAlgoritmo indentation bug has been fixed
"""

import unittest
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.formatter import format_pseint_code

class TestSubAlgoritmoVerification(unittest.TestCase):
    """Final verification tests for SubAlgoritmo indentation"""

    def test_basic_subalgoritmo(self):
        """Test basic SubAlgoritmo indentation"""
        test_code = """SubAlgoritmo test()
Escribir "Hello"
FinSubAlgoritmo"""
        
        formatted = format_pseint_code(test_code)
        lines = formatted.split('\n')
        
        self.assertEqual(len(lines[0]) - len(lines[0].lstrip()), 0)  # SubAlgoritmo at level 0
        self.assertEqual(len(lines[1]) - len(lines[1].lstrip()), 4)  # Content at level 1 
        self.assertEqual(len(lines[2]) - len(lines[2].lstrip()), 0)  # FinSubAlgoritmo at level 0

    def test_nested_subalgoritmo(self):
        """Test SubAlgoritmo with nested Para loop"""
        test_code = """SubAlgoritmo demo()
Para i <- 1 Hasta 10 Hacer
Escribir i
FinPara
FinSubAlgoritmo"""
        
        formatted = format_pseint_code(test_code)
        lines = formatted.split('\n')
        
        expected_indents = [0, 4, 8, 4, 0]  # SubAlgoritmo, Para, Escribir, FinPara, FinSubAlgoritmo
        
        for i, expected_indent in enumerate(expected_indents):
            actual_indent = len(lines[i]) - len(lines[i].lstrip())
            self.assertEqual(actual_indent, expected_indent, 
                           f"Line {i+1} should have {expected_indent} spaces, got {actual_indent}")

if __name__ == "__main__":
    unittest.main()
