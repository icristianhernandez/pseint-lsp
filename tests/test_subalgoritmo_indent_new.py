#!/usr/bin/env python3
"""
Test SubAlgoritmo indentation issue
"""

import unittest
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.formatter import format_pseint_code

class TestSubAlgoritmoIndent(unittest.TestCase):
    """Test SubAlgoritmo indentation functionality"""

    def test_subalgoritmo_indentation(self):
        """Test that SubAlgoritmo blocks are properly indented"""
        
        # Test code with SubAlgoritmo that should be indented
        test_code = """SubAlgoritmo calcular()
Escribir "Calculando..."
x <- 5 + 3
Escribir x
FinSubAlgoritmo"""
        
        formatted_code = format_pseint_code(test_code)
        lines = formatted_code.split('\n')
        
        # Check if the content inside SubAlgoritmo is indented
        subalgoritmo_found = False
        for i, line in enumerate(lines):
            if 'SubAlgoritmo' in line:
                subalgoritmo_found = True
                
                # Check the next lines until FinSubAlgoritmo
                for j in range(i+1, len(lines)):
                    if 'FinSubAlgoritmo' in lines[j]:
                        break
                    else:
                        # This should be indented with 4 spaces
                        leading_spaces = len(lines[j]) - len(lines[j].lstrip())
                        if lines[j].strip():  # Only check non-empty lines
                            self.assertEqual(leading_spaces, 4, 
                                           f"Line {j+1} should have 4 spaces but has {leading_spaces}")
                break
        
        self.assertTrue(subalgoritmo_found, "SubAlgoritmo not found in formatted code")

if __name__ == "__main__":
    unittest.main()
