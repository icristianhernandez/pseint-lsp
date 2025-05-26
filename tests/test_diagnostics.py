import unittest
import sys
import os

# Add the parent directory to sys.path for local imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from diagnostics import get_diagnostics
from lsprotocol.types import (
    Diagnostic,
    DiagnosticSeverity,
    Position,
    Range,
)

class TestPSeIntDiagnostics(unittest.TestCase):

    def assertDiagnostics(self, code: str, expected_diagnostics: list[Diagnostic], msg_prefix: str = ""):
        diagnostics = get_diagnostics(code)
        prefix = f"{msg_prefix}: " if msg_prefix else ""
        diagnostics.sort(key=lambda d: (d.range.start.line, d.range.start.character, d.message))
        expected_diagnostics.sort(key=lambda d: (d.range.start.line, d.range.start.character, d.message))
        
        self.assertEqual(len(diagnostics), len(expected_diagnostics), 
                         f"{prefix}Expected {len(expected_diagnostics)} diagnostics, got {len(diagnostics)} for code:\n{code}\nDiagnostics:\n{diagnostics}")

        for i, (diag, expected_diag) in enumerate(zip(diagnostics, expected_diagnostics)):
            self.assertEqual(diag.message, expected_diag.message, f"{prefix}Diag {i} message mismatch for code:\n{code}\nActual: {diag.message}\nExpected: {expected_diag.message}")
            self.assertEqual(diag.range, expected_diag.range, f"{prefix}Diag {i} range mismatch for code:\n{code}\nActual: {diag.range}\nExpected: {expected_diag.range}")
            self.assertEqual(diag.severity, expected_diag.severity, f"{prefix}Diag {i} severity mismatch for code:\n{code}")

    # --- Existing tests (abbreviated for brevity) ---
    def test_no_errors_simple(self):
        code = "Proceso Test\n    Definir x Como Entero;\n    x <- 5;\n    Escribir x;\nFinProceso"
        self.assertDiagnostics(code, [])

    def test_p1_func_return_var_not_assigned(self): # Example of existing P1-B test
        code = "Proceso P\nFinProceso\nFuncion resultado = MiFuncion()\n Escribir 'nada';\nFinFuncion"
        expected = [Diagnostic(range=Range(start=Position(line=2, character=8), end=Position(line=2, character=17)), message="Variable de retorno 'resultado' en Funcion 'MiFuncion' no asignada.", severity=DiagnosticSeverity.Error)]
        self.assertDiagnostics(code, expected, "P1 Func return var not assigned")

    # --- P2-Low Priority Diagnostics Tests ---

    # 1. Empty Block Warning
    def test_p2_empty_block_si_consecutive(self):
        code = "Proceso Test\n Definir x Como Logico; x <- verdadero;\n Si x Entonces\n FinSi\nFinProceso"
        #       01
        expected = [
            Diagnostic(range=Range(start=Position(line=2, character=26), end=Position(line=2, character=28)), # Si
                       message="Bloque 'si' vacío. Se esperaba contenido.",
                       severity=DiagnosticSeverity.Warning)
        ]
        self.assertDiagnostics(code, expected, "P2 Empty Si block (consecutive)")

    def test_p2_empty_block_mientras_with_comment(self):
        code = "Proceso Test\n Definir x Como Logico; x <- verdadero;\n Mientras x Hacer\n  // Un comentario aqui\n FinMientras\nFinProceso"
        #       01234567
        expected = [
            Diagnostic(range=Range(start=Position(line=2, character=26), end=Position(line=2, character=34)), # Mientras
                       message="Bloque 'mientras' vacío. Se esperaba contenido.",
                       severity=DiagnosticSeverity.Warning)
        ]
        self.assertDiagnostics(code, expected, "P2 Empty Mientras block (comment)")
    
    def test_p2_empty_block_para_with_empty_line(self):
        code = "Proceso Test\n Definir i Como Entero;\n Para i<-1 Hasta 2 Hacer\n    \n FinPara\nFinProceso"
        #       0123
        expected = [
            Diagnostic(range=Range(start=Position(line=2, character=20), end=Position(line=2, character=24)), # Para
                       message="Bloque 'para' vacío. Se esperaba contenido.",
                       severity=DiagnosticSeverity.Warning)
        ]
        self.assertDiagnostics(code, expected, "P2 Empty Para block (empty line)")

    def test_p2_non_empty_block_ok(self):
        code = "Proceso Test\n Definir x Como Logico; x <- verdadero;\n Si x Entonces\n  Escribir 'algo';\n FinSi\nFinProceso"
        self.assertDiagnostics(code, [], "P2 Non-empty block OK")

    # 2. Unused Variable Warning
    def test_p2_unused_variable_simple(self):
        code = "Proceso Test\n Definir x Como Entero;\nFinProceso"
        #        0
        expected = [
            Diagnostic(range=Range(start=Position(line=1, character=0), end=Position(line=1, character=1)), # x (approx range)
                       message="Variable 'x' definida pero no utilizada.",
                       severity=DiagnosticSeverity.Warning)
        ]
        self.assertDiagnostics(code, expected, "P2 Unused variable simple")

    def test_p2_unused_variable_one_used_one_not(self):
        code = "Proceso Test\n Definir x Como Entero;\n Definir y Como Real;\n x <- 5;\n Escribir x;\nFinProceso"
        #        0
        expected = [
            Diagnostic(range=Range(start=Position(line=2, character=0), end=Position(line=2, character=1)), # y (approx range)
                       message="Variable 'y' definida pero no utilizada.",
                       severity=DiagnosticSeverity.Warning)
        ]
        self.assertDiagnostics(code, expected, "P2 One used, one unused")

    def test_p2_unused_variable_parameter_is_used(self):
        code = "SubProceso Test(p Como Entero)\nFinSubProceso\nProceso Main\n Test(5);\nFinProceso"
        self.assertDiagnostics(code, [], "P2 Parameter is considered used")
        
    def test_p2_unused_variable_loop_var_is_used(self):
        code = "Proceso Test\n Para i<-0 Hasta 1 Hacer\n FinPara\nFinProceso" # i is implicitly used by loop construct
        self.assertDiagnostics(code, [], "P2 Para loop var is considered used")


    # 3. Missing Colon in Caso/De Otro Modo
    def test_p2_missing_colon_caso(self):
        code = "Proceso Test\n Definir x Como Entero; Segun x Hacer\n  Caso 1 Escribir \"Uno\";\n FinSegun\nFinProceso"
        #                01234567890123
        expected = [
            Diagnostic(range=Range(start=Position(line=2, character=9), end=Position(line=2, character=10)), # After "Caso 1"
                       message="Se esperaba ':' después del valor en 'Caso'.",
                       severity=DiagnosticSeverity.Warning)
        ]
        self.assertDiagnostics(code, expected, "P2 Missing colon Caso")

    def test_p2_missing_colon_deotromodo(self):
        code = "Proceso Test\n Definir x Como Entero; Segun x Hacer\n  De Otro Modo Escribir \"Otro\";\n FinSegun\nFinProceso"
        #                     012345678901
        expected = [
            Diagnostic(range=Range(start=Position(line=2, character=15), end=Position(line=2, character=16)), # After "De Otro Modo"
                       message="Se esperaba ':' después de 'De Otro Modo'.",
                       severity=DiagnosticSeverity.Warning)
        ]
        self.assertDiagnostics(code, expected, "P2 Missing colon DeOtroModo")

    # 4. Empty Escribir/Escribir Sin Saltar
    def test_p2_empty_escribir(self):
        code = "Proceso Test\n Escribir;\nFinProceso"
        #       01234567
        expected = [
            Diagnostic(range=Range(start=Position(line=1, character=1), end=Position(line=1, character=9)), # Escribir
                       message="Comando 'Escribir' requiere una o más expresiones.",
                       severity=DiagnosticSeverity.Warning)
        ]
        self.assertDiagnostics(code, expected, "P2 Empty Escribir")

    def test_p2_empty_escribir_sin_saltar(self):
        code = "Proceso Test\n Escribir Sin Saltar;\nFinProceso"
        #       01234567890123456
        expected = [
            Diagnostic(range=Range(start=Position(line=1, character=1), end=Position(line=1, character=19)), # Escribir Sin Saltar
                       message="Comando 'Escribir Sin Saltar' requiere una o más expresiones.",
                       severity=DiagnosticSeverity.Warning)
        ]
        self.assertDiagnostics(code, expected, "P2 Empty Escribir Sin Saltar")

    # 5. Keyword Alias Warning
    def test_p2_alias_algoritmo(self):
        code = "Algoritmo Test\nFinAlgoritmo"
        #       012345678
        expected = [
            Diagnostic(range=Range(start=Position(line=0, character=0), end=Position(line=0, character=9)), # Algoritmo
                       message="Se recomienda usar 'Proceso' en lugar de 'Algoritmo' para consistencia.",
                       severity=DiagnosticSeverity.Warning)
        ]
        self.assertDiagnostics(code, expected, "P2 Alias Algoritmo")

    def test_p2_alias_booleano(self):
        code = "Proceso Test\n Definir x Como Booleano;\nFinProceso"
        #                             01234567
        expected = [
            Diagnostic(range=Range(start=Position(line=1, character=18), end=Position(line=1, character=26)), # Booleano
                       message="Se recomienda usar 'Logico' en lugar de 'Booleano' para consistencia.",
                       severity=DiagnosticSeverity.Warning)
        ]
        self.assertDiagnostics(code, expected, "P2 Alias Booleano")

    # 6. Malformed Comment Warning (Empty Comment)
    def test_p2_empty_comment(self):
        code = "Proceso Test\n //\nFinProceso"
        expected = [
            Diagnostic(range=Range(start=Position(line=1, character=1), end=Position(line=1, character=3)), # //
                       message="Comentario vacío.",
                       severity=DiagnosticSeverity.Warning)
        ]
        self.assertDiagnostics(code, expected, "P2 Empty comment")
        
    def test_p2_empty_comment_with_whitespace(self):
        code = "Proceso Test\n //    \nFinProceso"
        expected = [
            Diagnostic(range=Range(start=Position(line=1, character=1), end=Position(line=1, character=8)), # //
                       message="Comentario vacío.",
                       severity=DiagnosticSeverity.Warning)
        ]
        self.assertDiagnostics(code, expected, "P2 Empty comment with whitespace")


if __name__ == "__main__":
    unittest.main()
```
