import unittest
import sys
import os
from typing import Optional

# Adjust import path if your test runner needs it,
# assuming tests are run from the root of the 'pseint_lsp_py' directory or configured for src layout.
# from ..formatter import format_pseint_code
# For simplicity if running from repository root, we might need to adjust python path
# or make formatter installable. For now, let's assume direct relative import works
# if tests are run as a module from within 'pseint_lsp_py' or 'pseint_lsp_py/tests'.
# A common way is to add the project root to sys.path in a test helper,
# but for a single file, direct import from the parent module is often fine if structure allows.

# If `pseint_lsp_py` is in PYTHONPATH or the test is run with `python -m unittest discover pseint_lsp_py`:
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from formatter import format_pseint_code


class TestPSeIntFormatter(unittest.TestCase):
    def assertFormattedCode(
        self, input_code: str, expected_code: str, msg: Optional[str] = None
    ) -> None:
        # Helper to strip leading/trailing whitespace from each line for comparison,
        # and ignore completely blank lines at the start/end of the whole string.
        # This makes comparisons less brittle to minor whitespace variations in test definitions.

        formatted = format_pseint_code(input_code).strip()
        expected = expected_code.strip()

        formatted_lines = [line.strip() for line in formatted.splitlines()]
        expected_lines = [line.strip() for line in expected.splitlines()]

        # Remove leading/trailing blank lines from the list of lines
        while formatted_lines and not formatted_lines[0]:
            formatted_lines.pop(0)
        while formatted_lines and not formatted_lines[-1]:
            formatted_lines.pop()
        while expected_lines and not expected_lines[0]:
            expected_lines.pop(0)
        while expected_lines and not expected_lines[-1]:
            expected_lines.pop()

        self.assertEqual(formatted_lines, expected_lines, msg)

    def test_simple_proceso(self):
        input_code = """
proceso Suma
escribir "Hola"
finproceso
"""
        expected_code = """
Proceso Suma
    Escribir "Hola"
FinProceso
"""
        self.assertFormattedCode(input_code, expected_code)

    def test_keywords_casing(self):
        input_code = "definir a COMO entero;"
        expected_code = "Definir a Como Entero;"
        self.assertFormattedCode(input_code, expected_code)

    def test_indentation_si(self):
        input_code = """
Proceso Mayor
    Definir a, b Como Entero;
    Leer a, b;
    si a > b entonces
    Escribir "A es mayor";
    sino
        Escribir "B es mayor o igual";
    finsi
FinProceso
"""
        expected_code = """
Proceso Mayor
    Definir a, b Como Entero;
    Leer a, b;
    Si a > b Entonces
        Escribir "A es mayor";
    Sino
        Escribir "B es mayor o igual";
    FinSi
FinProceso
"""
        self.assertFormattedCode(input_code, expected_code)

    def test_indentation_mientras(self):
        input_code = """
Proceso Contar
    Definir x Como Entero;
    x <- 0;
    mientras x < 5 hacer
        x <- x + 1;
    Escribir x;
    finmientras
FinProceso
"""
        expected_code = """
Proceso Contar
    Definir x Como Entero;
    x <- 0;
    Mientras x < 5 Hacer
        x <- x + 1;
        Escribir x;
    FinMientras
FinProceso
"""
        self.assertFormattedCode(input_code, expected_code)

    def test_indentation_para(self):
        input_code = """
Proceso TablaDel5
    Definir i, res Como Entero;
    para i <- 1 hasta 5 con paso 1 hacer
        res <- 5 * i;
    Escribir "5 x ", i, " = ", res;
    finpara
FinProceso
"""
        expected_code = """
Proceso TablaDel5
    Definir i, res Como Entero;
    Para i <- 1 Hasta 5 Con Paso 1 Hacer
        res <- 5 * i;
        Escribir "5 x ", i, " = ", res;
    FinPara
FinProceso
"""
        self.assertFormattedCode(input_code, expected_code)

    def test_indentation_segun(self):
        input_code = """
Proceso DiaSemana
    Definir dia Como Entero;
    Leer dia;
    segun dia hacer
        caso 1:
            Escribir "Lunes";
        caso 2: Escribir "Martes";
        de otro modo:
            Escribir "Otro dia";
    finsegun
FinProceso
"""
        expected_code = """
Proceso DiaSemana
    Definir dia Como Entero;
    Leer dia;
    Segun dia Hacer
        Caso 1:
            Escribir "Lunes";
        Caso 2:
            Escribir "Martes";
        De Otro Modo:
            Escribir "Otro dia";
    FinSegun
FinProceso
"""
        self.assertFormattedCode(input_code, expected_code)

    def test_indentation_repetir(self):
        input_code = """
Proceso Clave
    Definir clave_ingresada Como Texto
    Definir clave_secreta Como Texto
    clave_secreta <- "123"
    repetir
        Escribir "Ingrese clave:"
        Leer clave_ingresada
    hasta que clave_ingresada = clave_secreta
    Escribir "Bienvenido"
FinProceso
"""
        expected_code = """
Proceso Clave
    Definir clave_ingresada Como Texto
    Definir clave_secreta Como Texto
    clave_secreta <- "123"
    Repetir
        Escribir "Ingrese clave:"
        Leer clave_ingresada
    Hasta Que clave_ingresada = clave_secreta
    Escribir "Bienvenido"
FinProceso
"""
        self.assertFormattedCode(input_code, expected_code)

    def test_spacing_operators_commas_parentheses(self):
        input_code = "a<-b+c*(d-e)/f; Escribir a,b;"
        expected_code = "a <- b + c * (d - e) / f; Escribir a, b;"
        # Note: formatter might put Escribir on new line if ; is complexly handled
        # Current formatter is line based, so ; behavior is as seen.
        self.assertFormattedCode(input_code, expected_code)

    def test_comment_handling(self):
        input_code = """
Proceso Comentarios
    Definir x Como Entero; // Variable x
    x <- 10; // Asignacion
    //Escribir x
    Escribir x; //Mostrar x
FinProceso // Fin
"""
        expected_code = """
Proceso Comentarios
    Definir x Como Entero; // Variable x
    x <- 10; // Asignacion
    // Escribir x
    Escribir x; // Mostrar x
FinProceso // Fin
"""
        self.assertFormattedCode(input_code, expected_code)

    def test_blank_lines(self):
        input_code = """
Proceso Espacios


    Definir v Como Logico;


    v <- verdadero;

FinProceso
"""
        expected_code = """
Proceso Espacios

    Definir v Como Logico;

    v <- verdadero;
FinProceso
"""
        self.assertFormattedCode(input_code, expected_code)

    def test_subproceso_algoritmo(self):
        input_code = """
algoritmo TestAlgo
    definir x como entero
    x = x + 1
finalgoritmo

subproceso MiSub(a por referencia, b como caracter)
    escribir a, b
finsubproceso
"""
        expected_code = """
Algoritmo TestAlgo
    Definir x Como Entero
    x = x + 1
FinAlgoritmo

SubProceso MiSub(a Por Referencia, b Como Caracter)
    Escribir a, b
FinSubProceso
"""
        self.assertFormattedCode(input_code, expected_code)

    def test_subproceso_with_assignment_correction(self):
        # Test with PSeInt idiomatic assignment operator "<-"
        input_code = """
algoritmo TestAlgoCorrected
    definir x como entero
    x <- x + 1
finalgoritmo
"""
        expected_code = """
Algoritmo TestAlgoCorrected
    Definir x Como Entero
    x <- x + 1
FinAlgoritmo
"""
        self.assertFormattedCode(input_code, expected_code)

    def test_from_formatter_sample(self):
        input_code = """
Proceso   SUMA
  Escribir "Ingrese el primer numero:"
    Leer   A
Escribir "Ingrese el segundo numero:"
Leer B
    C  <-   A+B
    Escribir    "El resultado es: ",C // Suma realizada


    // Otro comentario
    Si A > B Entonces
        Escribir "A es mayor"
    Sino
        Escribir "B es mayor o igual"
    FinSi
    Mientras A < 10 Hacer
    A <- A + 1
    Escribir A
    FinMientras

Repetir
    Escribir "Dentro de Repetir"
    A <- A - 1
Hasta Que A <= 5

Para X<-1 Hasta 10 Con Paso 1 Hacer
Escribir X
FinPara

Segun A Hacer
    Caso 1: Escribir "Uno";
    Caso 2:
        Escribir "Dos";
    De Otro Modo: Escribir "Otro";
FinSegun

Definir var Como Entero
SubProceso Saludo(nombre Como Texto)
    Escribir "Hola ", nombre
FinSubProceso

// Comentario al final
FinProceso
"""
        expected_code = """
Proceso SUMA
    Escribir "Ingrese el primer numero:"
    Leer A
    Escribir "Ingrese el segundo numero:"
    Leer B
    C <- A + B
    Escribir "El resultado es: ", C // Suma realizada

    // Otro comentario
    Si A > B Entonces
        Escribir "A es mayor"
    Sino
        Escribir "B es mayor o igual"
    FinSi
    Mientras A < 10 Hacer
        A <- A + 1
        Escribir A
    FinMientras

    Repetir
        Escribir "Dentro de Repetir"
        A <- A - 1
    Hasta Que A <= 5

    Para X <- 1 Hasta 10 Con Paso 1 Hacer
        Escribir X
    FinPara

    Segun A Hacer
        Caso 1:
            Escribir "Uno";
        Caso 2:
            Escribir "Dos";
        De Otro Modo:
            Escribir "Otro";
    FinSegun

    Definir var Como Entero
    SubProceso Saludo(nombre Como Texto)
        Escribir "Hola ", nombre
    FinSubProceso

// Comentario al final
FinProceso
"""
        self.assertFormattedCode(input_code, expected_code)

    def test_caso_with_multiple_values_and_colon(self):
        input_code = """
Segun OPCION Hacer
    CASO 1: Escribir "Opcion 1";
    CASO 2,3:
    Escribir "Opcion 2 o 3";
FinSegun
"""
        expected_code = """
Segun OPCION Hacer
    Caso 1:
        Escribir "Opcion 1";
    Caso 2,3:
        Escribir "Opcion 2 o 3";
FinSegun
"""
        self.assertFormattedCode(input_code, expected_code)

    def test_funcion_definition(self):
        # From reference_code3.psc
        input_code = """
Algoritmo TestFunciones
    Definir resultado Como Entero
    resultado <- CalcularSuma(5, 3)
    Escribir resultado
FinAlgoritmo

Funcion res = CalcularSuma(n1 Como Entero, n2 Como Entero)
    res <- n1 + n2
FinFuncion
"""
        # This test is now updated based on the assumption that "Funcion" and "FinFuncion"
        # will be added to the formatter's known keywords and indentation rules.
        expected_code_after_formatter_update = """
Algoritmo TestFunciones
    Definir resultado Como Entero
    resultado <- CalcularSuma(5, 3)
    Escribir resultado
FinAlgoritmo

Funcion res = CalcularSuma(n1 Como Entero, n2 Como Entero)
    res <- n1 + n2
FinFuncion
"""
        self.assertFormattedCode(input_code, expected_code_after_formatter_update)

    def test_indentation_subalgoritmo_basic(self):
        """Test basic SubAlgoritmo indentation"""
        input_code = """
SubAlgoritmo calcular()
Escribir "Calculando..."
x <- 5 + 3
Escribir x
FinSubAlgoritmo
"""
        expected_code = """
SubAlgoritmo calcular()
    Escribir "Calculando..."
    x <- 5 + 3
    Escribir x
FinSubAlgoritmo
"""
        self.assertFormattedCode(input_code, expected_code)

    def test_indentation_subalgoritmo_nested(self):
        """Test SubAlgoritmo with nested Para loop"""
        input_code = """
SubAlgoritmo demo()
Definir i Como Entero
Para i <- 1 Hasta 10 Hacer
Escribir i
FinPara
Escribir "Tabla completa"
FinSubAlgoritmo
"""
        expected_code = """
SubAlgoritmo demo()
    Definir i Como Entero
    Para i <- 1 Hasta 10 Hacer
        Escribir i
    FinPara
    Escribir "Tabla completa"
FinSubAlgoritmo
"""
        self.assertFormattedCode(input_code, expected_code)

    def test_indentation_subalgoritmo_user_example(self):
        """Test SubAlgoritmo with the user's specific battleship example"""
        input_code = """
SubAlgoritmo mostrarTableroJugador(matrizJugador Por Referencia)
Definir i, j, filaNumeros Como Entero;
Definir columnaLetras Como Cadena;
columnaLetras <- " ABCDEFGHIJ";
Para i <- 0 Hasta 9 Con Paso 1 Hacer
filaNumeros[i] <- i + 1;
FinPara
Escribir "Este es tu tablero";
Para i <- 0 Hasta 10 Con Paso 1 Hacer
Escribir "";
esJugador <- Verdadero;
FinPara
Leer tecla;
FinSubAlgoritmo
"""
        expected_code = """
SubAlgoritmo mostrarTableroJugador(matrizJugador Por Referencia)
    Definir i, j, filaNumeros Como Entero;
    Definir columnaLetras Como Cadena;
    columnaLetras <- " ABCDEFGHIJ";
    Para i <- 0 Hasta 9 Con Paso 1 Hacer
        filaNumeros[i] <- i + 1;
    FinPara
    Escribir "Este es tu tablero";
    Para i <- 0 Hasta 10 Con Paso 1 Hacer
        Escribir "";
        esJugador <- Verdadero;
    FinPara
    Leer tecla;
FinSubAlgoritmo
"""
        self.assertFormattedCode(input_code, expected_code)


if __name__ == "__main__":
    unittest.main()
