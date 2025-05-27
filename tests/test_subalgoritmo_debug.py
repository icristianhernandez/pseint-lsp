#!/usr/bin/env python3
"""
Comprehensive test for SubAlgoritmo indentation using the specific example provided by the user
"""

import unittest
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.formatter import format_pseint_code

class TestSubAlgoritmoDebug(unittest.TestCase):
    """Comprehensive SubAlgoritmo indentation tests"""
    
    def test_subalgoritmo_user_example(self):
        """Test the specific SubAlgoritmo example provided by the user"""
        
        # The exact code from the user's request
        test_code = """SubAlgoritmo mostrarTableroJugador(matrizJugador Por Referencia)
Definir i, j, filaNumeros Como Entero;
Definir columnaLetras Como Cadena;
columnaLetras <- " ABCDEFGHIJ";
Dimension filaNumeros[10];
Definir tecla Como Caracter;
Definir esJugador Como Logico;

Para i <- 0 Hasta 9 Con Paso 1 Hacer
    filaNumeros[i] <- i + 1;
FinPara

Escribir "Este es tu tablero piensa en donde ubicar tus barcos";

Para i <- 0 Hasta 10 Con Paso 1 Hacer
    Escribir "";
    esJugador <- Verdadero;
    mostrarValor(matrizJugador, columnaLetras, filaNumeros, i, esJugador); // llamo a la funcion para mostrar una matriz
    Escribir "";
FinPara
Escribir "";
Escribir "                                                                           Presiona Enter para continuar...";
Leer tecla;
FinSubAlgoritmo"""
        
        formatted_code = format_pseint_code(test_code)
        lines = formatted_code.split('\n')
        
        # Test specific indentation expectations
        for i, line in enumerate(lines):
            leading_spaces = len(line) - len(line.lstrip())
            
            if 'SubAlgoritmo' in line and 'FinSubAlgoritmo' not in line:
                self.assertEqual(leading_spaces, 0, f"SubAlgoritmo declaration should have 0 spaces at line {i+1}")
                
            elif 'FinSubAlgoritmo' in line:
                self.assertEqual(leading_spaces, 0, f"FinSubAlgoritmo should have 0 spaces at line {i+1}")
                
            elif line.strip() and 'Para' in line and 'FinPara' not in line:
                self.assertEqual(leading_spaces, 4, f"Para statement should have 4 spaces at line {i+1}")
                
            elif 'FinPara' in line:
                self.assertEqual(leading_spaces, 4, f"FinPara should have 4 spaces at line {i+1}")
                
            elif line.strip() and 'Definir' in line:
                self.assertEqual(leading_spaces, 4, f"Definir statement should have 4 spaces at line {i+1}")

if __name__ == "__main__":
    unittest.main()
