"""
Test the formatter with actual content from reference_code1.psc
to ensure it handles real-world complex strings correctly.
"""

import sys
import os

# Add the parent directory to the path to import the formatter
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.formatter import format_pseint_code


def test_real_reference_code():
    """Test formatter with actual complex code from reference_code1.psc"""
    
    # Test the ASCII art section
    ascii_art_code = '''SubAlgoritmo textoEstatico
    definir tecla Como Caracter;
    Escribir "";
    Escribir "";
    Escribir "";
    Escribir "                                                                            Universidad Tecnologica Nacional";
    Escribir "";
    Escribir "                                                                              Facultad Regional San Rafael";
    Escribir "";
    Escribir "";
    Escribir "                                                                                  Proyecto Integrador";
    Escribir "";
    Escribir "                                                                                  T.U.P COHORTE 2024"; 
    
    Escribir "";
    Escribir "";
    Escribir "";
    
    Escribir "                                                     ............................................................................. ";
    Escribir "                                                     ............................................................................. ";
    Escribir "                                                     ............................................................................. ";
    Escribir "                                                     ... GOLDEN       ****  ****  ****    **    ****  *    *  *****      *     ... ";
    Escribir "                                                     ...      BYTES   *  *  *  *  *      *   *  *     * *  *    *       * *    ... ";
    Escribir "                                                     ...              ****  ****  ***      \\    ***   *  * *    *      *   *   ... ";
    Escribir "                                                     ...              *     * *   *     *   *   *     *    *    *     *******  ... ";
    Escribir "                                                     ...              *     *  *  ****    **    ****  *    *    *    *       * ... ";
    Escribir "                                                     ............................................................................. ";
    Escribir "                                                     ............................................................................. ";
    Escribir "                                                     ............................................................................. ";
    Escribir "";
    Escribir "";
    Escribir "                                                                       Presione Enter para continuar...";
    Leer tecla;
FinSubAlgoritmo'''

    result = format_pseint_code(ascii_art_code)
    print("=== Formatted ASCII Art Code ===")
    print(result)
    print("=" * 50)
    
    # Check that strings are preserved exactly
    assert '"                                                                            Universidad Tecnologica Nacional"' in result
    assert '"                                                     ............................................................................. "' in result
    assert '"                                                     ... GOLDEN       ****  ****  ****    **    ****  *    *  *****      *     ... "' in result
    assert '"                                                     ...      BYTES   *  *  *  *  *      *   *  *     * *  *    *       * *    ... "' in result
    
    # Test the animation logo array assignments
    animation_code = '''SubProceso Animacion
    Definir logo Como caracter;
    Definir i,j Como Entero;
    Definir tecla Como Caracter;
    
    Dimension logo[24];
    
    logo[1] <- "      8 888888888o           .8.    8888888 8888888888    .8.          8 8888         8 8888                  .8.";          
    logo[2] <- "      8 8888    `88.        .888.         8 8888         .888.         8 8888         8 8888                 .888.";         
    logo[3] <- "      8 8888     `88       :88888.        8 8888        :88888.        8 8888         8 8888                :88888.";        
    logo[4] <- "      8 8888     ,88      . `88888.       8 8888       . `88888.       8 8888         8 8888               . `88888.";       
    logo[5] <- "      8 8888.   ,88?     .8. `88888.      8 8888      .8. `88888.      8 8888         8 8888              .8. `88888.";      
FinSubProceso'''

    result2 = format_pseint_code(animation_code)
    print("=== Formatted Animation Code ===")
    print(result2)
    print("=" * 50)
    
    # Check that logo array assignments preserve exact string content
    assert 'logo[1] <- "      8 888888888o           .8.    8888888 8888888888    .8.          8 8888         8 8888                  .8."' in result2
    assert 'logo[2] <- "      8 8888    `88.        .888.         8 8888         .888.         8 8888         8 8888                 .888."' in result2
    
    # Test complex message with variables
    message_code = '''SubProceso MensajeBienvenida (nombre_jugador Por Referencia)
    Escribir "                                                                              ¡¡¡ Bienvenido Soldado !!!";
    Escribir "";
    Escribir "                                                                   Estas Listo y preparado para esta Gran Aventura";
    Escribir "";
    Escribir "                                                                                 Presentate Soldado ";
    Escribir "";
    Escribir "Nombre confirmado: ",nombre_jugador;
    Escribir "";
    Escribir "                                                             Perfecto soldado"," ", nombre_jugador, " ¡¡¡ Que comience la Batalla !!!";
FinSubProceso'''

    result3 = format_pseint_code(message_code)
    print("=== Formatted Message Code ===")
    print(result3)
    print("=" * 50)
    
    # Check that message strings are preserved and commas are properly spaced outside strings
    assert '"                                                                              ¡¡¡ Bienvenido Soldado !!!"' in result3
    assert '"Nombre confirmado: "' in result3
    assert 'nombre_jugador' in result3
    assert '" ¡¡¡ Que comience la Batalla !!!"' in result3
    
    print("All tests passed! ✅")


if __name__ == "__main__":
    test_real_reference_code()
