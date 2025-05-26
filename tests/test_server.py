import unittest
import sys
import os
from unittest.mock import Mock, patch, AsyncMock # Added AsyncMock
from typing import cast, List

# Add the parent directory to sys.path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lsprotocol.types import (
    DidChangeTextDocumentParams,
    DidOpenTextDocumentParams,
    DidSaveTextDocumentParams,
    DocumentFormattingParams,
    InitializeParams,
    InitializeResult,
    TextDocumentIdentifier,
    TextDocumentItem,
    VersionedTextDocumentIdentifier,
    TextDocumentContentChangeEvent_Type2,
    TextDocumentContentChangeEvent,
    ClientCapabilities,
    FormattingOptions,
    Diagnostic,  # Added
    Range,       # Added
    Position,    # Added
    DiagnosticSeverity, # Added
)

# Import server module
import server


class TestPSeIntLSPServer(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.server = server.server

    def test_initialize(self):
        """Test the initialize LSP method."""
        # Create mock initialize params
        params = InitializeParams(
            process_id=12345,
            root_uri="file:///test/workspace",
            capabilities=ClientCapabilities(),
        )

        # Call the initialize function
        result = server.initialize(params)

        # Verify the result
        self.assertIsInstance(result, InitializeResult)
        self.assertIsNotNone(result.server_info)
        if result.server_info:
            self.assertEqual(result.server_info.name, "pseint-lsp-py")
            self.assertEqual(result.server_info.version, "0.1.0")
        self.assertTrue(result.capabilities.document_formatting_provider)

    @patch("server.logging")
    async def test_did_open(self, mock_logging: Mock):
        """Test the didOpen document handler."""
        # Create mock document open params
        text_doc = TextDocumentItem(
            uri="file:///test.psc",
            language_id="pseint",
            version=1,
            text="Proceso Test\nFinProceso",
        )
        params = DidOpenTextDocumentParams(text_document=text_doc)

        # Create mock language server and document
        mock_ls = AsyncMock(spec=server.LanguageServer)
        mock_document = Mock()
        mock_document.source = text_doc.text
        mock_document.uri = text_doc.uri
        mock_ls.workspace.get_document.return_value = mock_document

        # Call the did_open function
        await server.did_open(mock_ls, params)

        # Verify logging was called
        mock_logging.info.assert_called_with(f"File Opened: {text_doc.uri}")
        # Verify publish_diagnostics was called (even if with empty list)
        mock_ls.publish_diagnostics.assert_called_once()

    @patch("server.logging")
    async def test_did_change(self, mock_logging: Mock):
        """Test the didChange document handler."""
        # Create mock document change params
        text_doc = VersionedTextDocumentIdentifier(uri="file:///test.psc", version=2)
        content_changes = cast(List[TextDocumentContentChangeEvent], [
            TextDocumentContentChangeEvent_Type2(
                text="Proceso Test\n    Escribir 'Hello'\nFinProceso"
            )
        ])
        params = DidChangeTextDocumentParams(
            text_document=text_doc, content_changes=content_changes
        )

        # Create mock language server and document
        mock_ls = AsyncMock(spec=server.LanguageServer)
        mock_document = Mock()
        mock_document.source = content_changes[0].text # pygls updates document source internally
        mock_document.uri = text_doc.uri
        mock_ls.workspace.get_document.return_value = mock_document
        
        # Call the did_change function
        await server.did_change(mock_ls, params)

        # Verify logging was called
        mock_logging.info.assert_called_with(f"File Changed: {text_doc.uri}")
        # Verify publish_diagnostics was called
        mock_ls.publish_diagnostics.assert_called_once()

    @patch("server.logging")
    async def test_did_save(self, mock_logging: Mock):
        """Test the didSave document handler."""
        # Create mock document save params
        text_doc = TextDocumentIdentifier(uri="file:///test.psc")
        params = DidSaveTextDocumentParams(text_document=text_doc)

        # Create mock language server
        mock_ls = Mock()

        # Call the did_save function
        await server.did_save(mock_ls, params)

        # Verify logging was called
        mock_logging.info.assert_called_once()

    def test_format_document(self):
        """Test the document formatting functionality."""
        # Create mock formatting params
        text_doc = TextDocumentIdentifier(uri="file:///test.psc")
        options = FormattingOptions(tab_size=4, insert_spaces=True)
        params = DocumentFormattingParams(text_document=text_doc, options=options)

        # Create mock language server with document content
        mock_ls = Mock()
        mock_document = Mock()
        mock_document.source = "proceso test\nescribir 'hello'\nfinproceso"
        mock_ls.workspace.get_document.return_value = mock_document

        # Call the format_document function
        result = server.format_document(mock_ls, params)

        # Verify the result
        self.assertIsInstance(result, list)
        if result:
            self.assertTrue(len(result) > 0)

            # Check that the result contains TextEdit objects
            for edit in result:
                self.assertTrue(hasattr(edit, "range"))
                self.assertTrue(hasattr(edit, "new_text"))

    def test_format_document_with_empty_content(self):
        """Test formatting with empty document content."""
        # Create mock language server with empty document
        mock_ls = Mock()
        mock_document = Mock()
        mock_document.source = ""
        mock_ls.workspace.get_document.return_value = mock_document

        # Create mock formatting params
        text_doc = TextDocumentIdentifier(uri="file:///test.psc")
        options = FormattingOptions(tab_size=4, insert_spaces=True)
        params = DocumentFormattingParams(text_document=text_doc, options=options)

        # Call the format_document function
        result = server.format_document(mock_ls, params)
        
        # Empty content should return empty list or None
        self.assertIsInstance(result, (list, type(None)))

    # --- Tests for Diagnostics ---

    async def test_diagnostics_on_open_no_errors_async(self):
        """Test diagnostics on didOpen with no errors."""
        uri = "file:///test_no_errors.psc"
        content = "Proceso SinErrores\n    Escribir 'Hola';\nFinProceso"
        
        text_doc = TextDocumentItem(uri=uri, language_id="pseint", version=1, text=content)
        params = DidOpenTextDocumentParams(text_document=text_doc)
        
        mock_ls = AsyncMock(spec=server.LanguageServer)
        mock_document = Mock()
        mock_document.source = content
        mock_document.uri = uri
        mock_ls.workspace.get_document.return_value = mock_document

        await server.did_open(mock_ls, params)

        mock_ls.publish_diagnostics.assert_called_once_with(uri, [])

    async def test_diagnostics_on_open_missing_finproceso_async(self):
        """Test diagnostics on didOpen for missing FinProceso."""
        uri = "file:///test_missing_finproceso.psc"
        content = "Proceso Olvidado" # Missing FinProceso
        #           01234567890123
        
        text_doc = TextDocumentItem(uri=uri, language_id="pseint", version=1, text=content)
        params = DidOpenTextDocumentParams(text_document=text_doc)

        mock_ls = AsyncMock(spec=server.LanguageServer)
        mock_document = Mock()
        mock_document.source = content
        mock_document.uri = uri
        mock_ls.workspace.get_document.return_value = mock_document

        await server.did_open(mock_ls, params)

        expected_diagnostic = Diagnostic(
            range=Range(start=Position(line=0, character=0), end=Position(line=0, character=7)), # "Proceso"
            message="Bloque 'proceso' no cerrado con 'finproceso'.",
            severity=DiagnosticSeverity.Error,
        )
        mock_ls.publish_diagnostics.assert_called_once_with(uri, [expected_diagnostic])

    async def test_diagnostics_on_change_unexpected_finsi_async(self):
        """Test diagnostics on didChange for unexpected FinSi."""
        uri = "file:///test_unexpected_finsi.psc"
        initial_content = "Proceso Correcto\nFinProceso"
        changed_content = "Proceso Correcto\nFinSi\nFinProceso" 
        #                    012345
        
        # Setup for did_change
        # 1. Simulate did_open first so the document is in workspace
        open_text_doc = TextDocumentItem(uri=uri, language_id="pseint", version=1, text=initial_content)
        open_params = DidOpenTextDocumentParams(text_document=open_text_doc)
        
        mock_ls = AsyncMock(spec=server.LanguageServer)
        mock_document = Mock()
        mock_document.source = initial_content # Initial state
        mock_document.uri = uri
        mock_ls.workspace.get_document.return_value = mock_document
        
        await server.did_open(mock_ls, open_params) # Open the doc
        mock_ls.publish_diagnostics.assert_called_once_with(uri, []) # No errors initially

        # 2. Now simulate did_change
        mock_ls.publish_diagnostics.reset_mock() # Reset mock for the next call
        mock_document.source = changed_content # Update source for get_document

        change_event = TextDocumentContentChangeEvent_Type2(text=changed_content)
        params_change = DidChangeTextDocumentParams(
            text_document=VersionedTextDocumentIdentifier(uri=uri, version=2),
            content_changes=[cast(TextDocumentContentChangeEvent, change_event)]
        )
        
        await server.did_change(mock_ls, params_change)

        expected_diagnostic = Diagnostic(
            range=Range(start=Position(line=1, character=0), end=Position(line=1, character=5)), # "FinSi"
            message="'finsi' inesperado sin un bloque 'si' abierto.", # Based on current diagnostics.py
            severity=DiagnosticSeverity.Error,
        )
        mock_ls.publish_diagnostics.assert_called_once_with(uri, [expected_diagnostic])

    async def test_diagnostics_on_change_mismatched_keywords_async(self):
        """Test diagnostics on didChange for mismatched Proceso/FinSi."""
        uri = "file:///test_mismatched.psc"
        initial_content = "Proceso Algo\nFinProceso"
        changed_content = "Proceso Algo\nFinSi" # Mismatched closing
        #                   01234567890
        #                   01234

        open_text_doc = TextDocumentItem(uri=uri, language_id="pseint", version=1, text=initial_content)
        open_params = DidOpenTextDocumentParams(text_document=open_text_doc)
        
        mock_ls = AsyncMock(spec=server.LanguageServer)
        mock_document = Mock()
        mock_document.source = initial_content
        mock_document.uri = uri
        mock_ls.workspace.get_document.return_value = mock_document

        await server.did_open(mock_ls, open_params)
        mock_ls.publish_diagnostics.assert_called_once_with(uri, [])

        mock_ls.publish_diagnostics.reset_mock()
        mock_document.source = changed_content

        change_event = TextDocumentContentChangeEvent_Type2(text=changed_content)
        params_change = DidChangeTextDocumentParams(
            text_document=VersionedTextDocumentIdentifier(uri=uri, version=2),
            content_changes=[cast(TextDocumentContentChangeEvent, change_event)]
        )

        await server.did_change(mock_ls, params_change)
        
        # The stack will have 'proceso'. 'FinSi' is encountered.
        # The diagnostics.py logic will report: "Se esperaba 'finproceso' pero se encontró 'finsi'."
        # And then it will also report the unclosed 'proceso'.
        
        expected_diagnostic1 = Diagnostic(
            range=Range(start=Position(line=1, character=0), end=Position(line=1, character=5)), # "FinSi"
            message="Se esperaba 'finproceso' pero se encontró 'finsi'.",
            severity=DiagnosticSeverity.Error,
        )
        expected_diagnostic2 = Diagnostic(
            range=Range(start=Position(line=0, character=0), end=Position(line=0, character=7)), # "Proceso"
            message="Bloque 'proceso' no cerrado con 'finproceso'.",
            severity=DiagnosticSeverity.Error,
        )
        
        # Order of diagnostics might vary, so check for contents
        mock_ls.publish_diagnostics.assert_called_once()
        args, _ = mock_ls.publish_diagnostics.call_args
        self.assertEqual(args[0], uri)
        self.assertIn(expected_diagnostic1, args[1])
        self.assertIn(expected_diagnostic2, args[1])
        self.assertEqual(len(args[1]), 2)

    # --- New P0 Diagnostics Integration Tests ---

    async def helper_test_diagnostics_on_open(self, test_name: str, content: str, expected_diagnostics: List[Diagnostic]):
        """Helper function to test diagnostics on didOpen."""
        uri = f"file:///{test_name}.psc"
        
        text_doc = TextDocumentItem(uri=uri, language_id="pseint", version=1, text=content)
        params = DidOpenTextDocumentParams(text_document=text_doc)
        
        mock_ls = AsyncMock(spec=server.LanguageServer)
        mock_document = Mock()
        mock_document.source = content
        mock_document.uri = uri
        mock_ls.workspace.get_document.return_value = mock_document

        await server.did_open(mock_ls, params)

        # Sort diagnostics by line, character, and message for stable comparison
        # Actual diagnostics are in mock_ls.publish_diagnostics.call_args.args[1]
        # Expected diagnostics are already sorted in the calling test if necessary.
        
        # Check if publish_diagnostics was called
        try:
            mock_ls.publish_diagnostics.assert_called_once()
        except AssertionError as e:
            raise AssertionError(f"publish_diagnostics not called for {test_name}.\n{e}")

        # Get actual diagnostics
        actual_diagnostics_tuple = mock_ls.publish_diagnostics.call_args
        if actual_diagnostics_tuple is None:
            raise AssertionError(f"publish_diagnostics call_args is None for {test_name}")
            
        actual_uri, actual_diags_list = actual_diagnostics_tuple.args
        
        self.assertEqual(actual_uri, uri, f"[{test_name}] URI mismatch.")

        actual_diags_list.sort(key=lambda d: (d.range.start.line, d.range.start.character, d.message))
        expected_diagnostics.sort(key=lambda d: (d.range.start.line, d.range.start.character, d.message))

        self.assertEqual(len(actual_diags_list), len(expected_diagnostics),
                         f"[{test_name}] Number of diagnostics mismatch. Expected {len(expected_diagnostics)}, got {len(actual_diags_list)}.\nActual: {actual_diags_list}\nExpected: {expected_diagnostics}\nCode:\n{content}")

        for i, (actual, expected) in enumerate(zip(actual_diags_list, expected_diagnostics)):
            self.assertEqual(actual.message, expected.message, f"[{test_name}] Diag {i} message mismatch.")
            self.assertEqual(actual.range, expected.range, f"[{test_name}] Diag {i} range mismatch.")
            self.assertEqual(actual.severity, expected.severity, f"[{test_name}] Diag {i} severity mismatch.")

    async def test_p0_diag_unclosed_algoritmo(self):
        content = "Algoritmo Incompleto\n Escribir 'hola';"
        #           0123456789
        expected = [
            Diagnostic(
                range=Range(start=Position(line=0, character=0), end=Position(line=0, character=9)), # Algoritmo
                message="Bloque 'algoritmo' no cerrado con 'finalgoritmo'.",
                severity=DiagnosticSeverity.Error,
            )
        ]
        await self.helper_test_diagnostics_on_open("unclosed_algoritmo", content, expected)

    async def test_p0_diag_sino_without_si(self):
        content = "Proceso TestSino\n Sino\n Escribir 'error';\nFinProceso"
        #           0123
        expected = [
            Diagnostic(
                range=Range(start=Position(line=1, character=1), end=Position(line=1, character=5)), # Sino
                message="Palabra clave 'Sino' inesperada fuera de un bloque 'si'.",
                severity=DiagnosticSeverity.Error,
            )
        ]
        await self.helper_test_diagnostics_on_open("sino_without_si", content, expected)

    async def test_p0_diag_caso_without_segun(self):
        content = "Proceso TestCaso\n Caso 1:\n Escribir 'error';\nFinProceso"
        #           0123
        expected = [
            Diagnostic(
                range=Range(start=Position(line=1, character=1), end=Position(line=1, character=5)), # Caso
                message="Palabra clave 'Caso' inesperada fuera de un bloque 'segun'.",
                severity=DiagnosticSeverity.Error,
            )
        ]
        await self.helper_test_diagnostics_on_open("caso_without_segun", content, expected)

    async def test_p0_diag_missing_entonces(self):
        content = "Proceso TestSi\n Definir a Como Entero; Si a > 0\n FinSi\nFinProceso"
        #                                      01
        expected = [
            Diagnostic(
                range=Range(start=Position(line=1, character=22), end=Position(line=1, character=24)), # Si
                message="Se esperaba 'Entonces' después de la condición en 'Si'.",
                severity=DiagnosticSeverity.Error,
            )
        ]
        await self.helper_test_diagnostics_on_open("missing_entonces", content, expected)
    
    async def test_p0_diag_unknown_type(self):
        content = "Proceso TestTipo\n Definir x Como Patata;\nFinProceso"
        #                        012345
        expected = [
            Diagnostic(
                range=Range(start=Position(line=1, character=18), end=Position(line=1, character=24)), # Patata
                message="Tipo de dato desconocido: 'Patata'.",
                severity=DiagnosticSeverity.Error,
            )
        ]
        await self.helper_test_diagnostics_on_open("unknown_type", content, expected)

    async def test_p0_diag_missing_como(self):
        content = "Proceso TestComo\n Definir x Entero;\nFinProceso"
        #                  0
        expected = [
            Diagnostic(
                range=Range(start=Position(line=1, character=10), end=Position(line=1, character=11)), # x
                message="Se esperaba la palabra clave 'Como' en la definición de variable.",
                severity=DiagnosticSeverity.Error,
            )
        ]
        await self.helper_test_diagnostics_on_open("missing_como", content, expected)

    async def test_p0_diag_variable_redefinition(self):
        content = "Proceso TestRedef\n Definir x Como Entero;\n Definir x Como Texto;\nFinProceso"
        #                  0
        expected = [
            Diagnostic(
                range=Range(start=Position(line=2, character=10), end=Position(line=2, character=11)), # x
                message="Redefinición de variable 'x'. Ya definida en línea 2.",
                severity=DiagnosticSeverity.Error,
            )
        ]
        await self.helper_test_diagnostics_on_open("variable_redefinition", content, expected)

    async def test_p0_diag_undefined_variable_escribir(self):
        content = "Proceso TestUndef\n Escribir variable_fantasma;\nFinProceso"
        #          0123456789012345678
        expected = [
            Diagnostic(
                range=Range(start=Position(line=1, character=10), end=Position(line=1, character=28)), # variable_fantasma
                message="Variable 'variable_fantasma' no definida.",
                severity=DiagnosticSeverity.Error,
            )
        ]
        await self.helper_test_diagnostics_on_open("undefined_var_escribir", content, expected)

    async def test_p0_diag_undefined_variable_assign_rhs(self):
        content = "Proceso TestUndefAsign\n Definir x Como Entero;\n x <- var_fantasma_rhs;\nFinProceso"
        #             0123456789012345
        expected = [
            Diagnostic(
                range=Range(start=Position(line=2, character=7), end=Position(line=2, character=23)), # var_fantasma_rhs
                message="Variable 'var_fantasma_rhs' (en asignación derecha) no definida.",
                severity=DiagnosticSeverity.Error,
            )
        ]
        await self.helper_test_diagnostics_on_open("undefined_var_assign_rhs", content, expected)

    async def test_p0_diag_undefined_variable_assign_lhs(self):
        content = "Proceso TestUndefAsignLHS\n var_fantasma_lhs <- 10;\nFinProceso"
        #          0123456789012345
        expected = [
            Diagnostic(
                range=Range(start=Position(line=1, character=1), end=Position(line=1, character=17)), # var_fantasma_lhs
                message="Variable 'var_fantasma_lhs' (en asignación izquierda) no definida.",
                severity=DiagnosticSeverity.Error,
            )
        ]
        await self.helper_test_diagnostics_on_open("undefined_var_assign_lhs", content, expected)

    # --- P0 Type Error and Operator Error Integration Tests ---

    async def test_p0_type_error_assign_string_to_int(self):
        content = "Proceso T1\nDefinir x Como Entero;\nx <- \"text\";\nFinProceso"
        #                        012345
        expected = [
            Diagnostic(
                range=Range(start=Position(line=2, character=7), end=Position(line=2, character=13)), # "text"
                message="No se puede asignar un valor de tipo 'caracter' a una variable de tipo 'entero' ('x').",
                severity=DiagnosticSeverity.Error,
            )
        ]
        await self.helper_test_diagnostics_on_open("type_assign_str_to_int", content, expected)

    async def test_p0_type_error_op_non_numeric(self):
        content = "Proceso T2\nDefinir s Como Caracter; s <- \"a\" * 2;\nFinProceso"
        #                                 0
        expected = [
            Diagnostic(
                range=Range(start=Position(line=1, character=30), end=Position(line=1, character=31)), # *
                message="Operador '*' no aplicable a operandos de tipo 'caracter' y 'entero'.",
                severity=DiagnosticSeverity.Error,
            )
        ]
        await self.helper_test_diagnostics_on_open("type_op_non_numeric", content, expected)

    async def test_p0_type_error_si_condition_non_logical(self):
        content = "Proceso T3\nDefinir n Como Entero; n <- 0;\nSi n Entonces Escribir \"a\"; FinSi\nFinProceso"
        #          0
        expected = [
            Diagnostic(
                range=Range(start=Position(line=2, character=3), end=Position(line=2, character=4)), # n in "Si n"
                message="Condición en 'Si' debe ser de tipo Logico, pero es 'entero'.",
                severity=DiagnosticSeverity.Error,
            )
        ]
        await self.helper_test_diagnostics_on_open("type_si_cond_non_logical", content, expected)

    async def test_p0_type_error_para_start_val_non_numeric(self):
        content = "Proceso T4\nDefinir i Como Entero;\nPara i <- \"0\" Hasta 5 Hacer Escribir i; FinPara\nFinProceso"
        #                 012
        expected = [
            Diagnostic(
                range=Range(start=Position(line=2, character=11), end=Position(line=2, character=14)), # "0"
                message="El valor inicial en 'Para' debe ser de tipo numérico, pero se encontró '\"0\"' (tipo 'caracter').",
                severity=DiagnosticSeverity.Error,
            )
        ]
        await self.helper_test_diagnostics_on_open("type_para_start_non_numeric", content, expected)

    async def test_p0_type_error_segun_caso_mismatch(self):
        content = "Proceso T5\nDefinir x Como Entero; x <- 1;\nSegun x Hacer\n  Caso \"A\": Escribir \"letra\";\nFinSegun\nFinProceso"
        #              012
        expected = [
            Diagnostic(
                range=Range(start=Position(line=3, character=8), end=Position(line=3, character=11)), # "A"
                message="El tipo de valor en 'Caso' (caracter) no coincide con el tipo de la variable de 'Segun' (entero).",
                severity=DiagnosticSeverity.Error,
            )
        ]
        await self.helper_test_diagnostics_on_open("type_segun_caso_mismatch", content, expected)

    async def test_p0_operator_error_equals_for_assignment(self):
        content = "Proceso O1\nDefinir x Como Entero;\nx = 10;\nFinProceso"
        #         0
        expected = [
            Diagnostic(
                range=Range(start=Position(line=2, character=2), end=Position(line=2, character=3)), # =
                message="Operador de asignación incorrecto. Use '<-' en lugar de '='.",
                severity=DiagnosticSeverity.Error,
            )
        ]
        await self.helper_test_diagnostics_on_open("op_equals_for_assign", content, expected)

    async def test_p0_operator_error_assign_in_si_condition(self):
        content = "Proceso O2\nDefinir x Como Entero; x <- 5;\nSi x <- 5 Entonces Escribir \"a\"; FinSi\nFinProceso"
        #           01
        expected = [
            Diagnostic(
                range=Range(start=Position(line=2, character=6), end=Position(line=2, character=8)), # <-
                message="Operador de comparación incorrecto. Use '=' para comparación, no '<-' en una condición.",
                severity=DiagnosticSeverity.Error,
            )
        ]
        await self.helper_test_diagnostics_on_open("op_assign_in_si", content, expected)
    
    async def test_p0_operator_error_missing_operand_binary(self):
        content = "Proceso O3\nDefinir x Como Entero;\nx <- 5 + ;\nFinProceso"
        #               0
        expected = [
            Diagnostic(
                range=Range(start=Position(line=2, character=9), end=Position(line=2, character=10)), # +
                message="Faltan operandos para el operador '+'.",
                severity=DiagnosticSeverity.Error,
            )
        ]
        await self.helper_test_diagnostics_on_open("op_missing_operand_binary", content, expected)

    async def test_p0_operator_error_unknown_operator_power(self):
        content = "Proceso O4\nDefinir x Como Entero;\nx <- 2 ** 3;\nFinProceso"
        #              01
        expected = [
            Diagnostic(
                range=Range(start=Position(line=2, character=9), end=Position(line=2, character=11)), # **
                message="Operador '**' desconocido o mal utilizado en PSeInt.",
                severity=DiagnosticSeverity.Error,
            )
        ]
        await self.helper_test_diagnostics_on_open("op_unknown_power", content, expected)

    # --- P0 Function/Subprocess and Array Error Integration Tests ---

    async def test_p0_func_error_name_collision_subproceso_proceso(self):
        content = "Proceso X\nFinProceso\nSubProceso X()\nFinSubProceso"
        #                  0
        expected = [
            Diagnostic(
                range=Range(start=Position(line=2, character=11), end=Position(line=2, character=12)), # X in SubProceso
                message="Nombre de SubProceso 'X' ya está en uso. Definido en línea 1.",
                severity=DiagnosticSeverity.Error,
            )
        ]
        await self.helper_test_diagnostics_on_open("func_name_collision_sub_proc", content, expected)

    async def test_p0_func_error_missing_open_paren(self):
        content = "Proceso Main\nFinProceso\nSubProceso MiSub param Como Entero)\nFinSubProceso"
        #                      01234
        expected = [
            Diagnostic(
                range=Range(start=Position(line=2, character=17), end=Position(line=2, character=22)), # "param"
                message="Se esperaba '(' para la lista de parámetros en la definición de SubProceso.",
                severity=DiagnosticSeverity.Error,
            )
        ]
        await self.helper_test_diagnostics_on_open("func_missing_open_paren", content, expected)

    async def test_p0_func_error_missing_close_paren(self):
        content = "Proceso Main\nFinProceso\nSubProceso MiSub (param Como Entero\nFinSubProceso"
        #                                 012345678901234 (param Como Entero)
        expected = [
            Diagnostic(
                range=Range(start=Position(line=2, character=34), end=Position(line=2, character=34)), 
                message="Se esperaba ')' para finalizar la lista de parámetros.",
                severity=DiagnosticSeverity.Error,
            )
        ]
        await self.helper_test_diagnostics_on_open("func_missing_close_paren", content, expected)

    async def test_p0_func_error_param_type_missing(self):
        content = "Proceso Main\nFinProceso\nSubProceso MiSub(p1)\nFinSubProceso"
        #                     01
        expected = [
            Diagnostic(
                range=Range(start=Position(line=2, character=17), end=Position(line=2, character=19)), # p1
                message="Tipo de parámetro ausente para 'p1'. Se esperaba 'Como <Tipo>'.",
                severity=DiagnosticSeverity.Error,
            )
        ]
        await self.helper_test_diagnostics_on_open("func_param_type_missing", content, expected)

    async def test_p0_func_error_funcion_missing_ret_var(self):
        content = "Proceso Main\nFinProceso\nFuncion MiFunc()\nFinFuncion"
        #       01234567890
        expected = [
            Diagnostic(
                range=Range(start=Position(line=2, character=0), end=Position(line=2, character=16)), # Funcion MiFunc()
                message="Una Funcion debe tener una variable de retorno definida (ej: `Funcion var_retorno = ...`).",
                severity=DiagnosticSeverity.Error,
            )
        ]
        await self.helper_test_diagnostics_on_open("func_missing_ret_var", content, expected)

    async def test_p0_array_error_name_collision_var_dim(self):
        content = "Proceso TestArr\nDefinir arr Como Entero;\nDimension arr[5];\nFinProceso"
        #                 012
        expected = [
            Diagnostic(
                range=Range(start=Position(line=2, character=12), end=Position(line=2, character=15)), # arr in Dimension
                message="Nombre de array 'arr' ya está en uso. Definido en línea 2.",
                severity=DiagnosticSeverity.Error,
            )
        ]
        await self.helper_test_diagnostics_on_open("arr_name_collision_var_dim", content, expected)

    async def test_p0_array_error_non_positive_dimension(self):
        content = "Proceso TestArrDim\nDimension arr[0];\nFinProceso"
        #                       0
        expected = [
            Diagnostic(
                range=Range(start=Position(line=1, character=16), end=Position(line=1, character=17)), # 0
                message="Dimensión de array '0' debe ser un entero positivo.",
                severity=DiagnosticSeverity.Error,
            )
        ]
        await self.helper_test_diagnostics_on_open("arr_non_positive_dim", content, expected)

    async def test_p0_array_error_non_numeric_dimension_string(self):
        content = "Proceso TestArrDimStr\nDimension arr[\"size\"];\nFinProceso"
        #                       012345
        expected = [
            Diagnostic(
                range=Range(start=Position(line=1, character=16), end=Position(line=1, character=22)), # "size"
                message="Dimensiones de array deben ser numéricas y positivas. Se encontró '\"size\"' (tipo caracter).",
                severity=DiagnosticSeverity.Error,
            )
        ]
        await self.helper_test_diagnostics_on_open("arr_non_numeric_dim_str", content, expected)

    async def test_p0_array_error_non_integer_index(self):
        content = "Proceso TestArrIdx\nDimension arr[5];\narr[\"idx\"] <- 10;\nFinProceso"
        #           012
        expected = [
            Diagnostic(
                range=Range(start=Position(line=2, character=4), end=Position(line=2, character=9)), # "idx"
                message="Índice '\"idx\"' del array 'arr' debe ser de tipo Entero (se encontró caracter).",
                severity=DiagnosticSeverity.Error,
            )
        ]
        await self.helper_test_diagnostics_on_open("arr_non_integer_index", content, expected)

    async def test_p0_array_error_wrong_brackets_for_dimension(self):
        content = "Proceso TestArrBrackets\nDimension arr(5);\nFinProceso"
        #                        01234567
        expected = [
            Diagnostic(
                range=Range(start=Position(line=1, character=14), end=Position(line=1, character=18)), # arr(5) -> range of (5)
                message="Declaración de 'Dimension' debe usar corchetes `[]` para los tamaños, no paréntesis `()`.",
                severity=DiagnosticSeverity.Error,
            )
        ]
        await self.helper_test_diagnostics_on_open("arr_wrong_brackets", content, expected)

    # --- P1 Batch 1, Part A: Integration Tests ---

    async def test_p1_var_used_before_assigned_warning(self):
        content = "Proceso TestVarUnassigned\nDefinir x Como Entero;\nEscribir x;\nFinProceso"
        #                  0
        expected = [
            Diagnostic(
                range=Range(start=Position(line=2, character=10), end=Position(line=2, character=11)), # x in Escribir
                message="Variable 'x' utilizada antes de ser asignada.",
                severity=DiagnosticSeverity.Warning, # P1 specifies Warning
            )
        ]
        await self.helper_test_diagnostics_on_open("p1_var_unassigned", content, expected)

    async def test_p1_type_error_segun_var_logico(self):
        content = "Proceso TestSegunVarType\nDefinir opcion Como Logico;\nopcion <- VERDADERO;\nSegun opcion Hacer\n  Caso VERDADERO: Escribir \"Si\";\nFinSegun\nFinProceso"
        #             012345
        expected = [
            Diagnostic(
                range=Range(start=Position(line=3, character=7), end=Position(line=3, character=13)), # opcion in Segun
                message="La variable en 'Segun' ('opcion') debe ser de tipo Entero o Caracter, pero es 'logico'.",
                severity=DiagnosticSeverity.Error,
            )
        ]
        await self.helper_test_diagnostics_on_open("p1_segun_var_logico", content, expected)

    async def test_p1_func_call_too_few_args(self):
        content = "SubProceso Saludar(nombre Como Caracter, edad Como Entero)\n  Escribir \"Hola \", nombre, \" tienes \", edad, \" anios\";\nFinSubProceso\nProceso TestLlamada\n  Saludar(\"Ana\");\nFinProceso"
        #          0123456789
        expected = [
            Diagnostic(
                range=Range(start=Position(line=4, character=2), end=Position(line=4, character=16)), # Saludar("Ana")
                message="Número incorrecto de argumentos al llamar a 'Saludar'. Se esperaban 2 pero se pasaron 1.",
                severity=DiagnosticSeverity.Error,
            )
        ]
        await self.helper_test_diagnostics_on_open("p1_func_too_few_args", content, expected)

    async def test_p1_func_call_arg_type_mismatch(self):
        content = "SubProceso ImprimirNumero(num Como Entero)\n  Escribir num;\nFinSubProceso\nProceso TestLlamadaTipo\n  ImprimirNumero(\"cien\");\nFinProceso"
        #                    012345
        expected = [
            Diagnostic(
                range=Range(start=Position(line=4, character=17), end=Position(line=4, character=23)), # "cien"
                message="Tipo de argumento incorrecto para el parámetro 'num' en 'ImprimirNumero'. Se esperaba 'entero' pero se pasó 'caracter'.",
                severity=DiagnosticSeverity.Error,
            )
        ]
        await self.helper_test_diagnostics_on_open("p1_func_arg_type_mismatch", content, expected)

    async def test_p1_func_call_by_ref_with_literal(self):
        content = "SubProceso Incrementar(valor Por Referencia Como Entero)\n  valor <- valor + 1;\nFinSubProceso\nProceso TestLlamadaRef\n  Incrementar(5);\nFinProceso"
        #                    0
        expected = [
            Diagnostic(
                range=Range(start=Position(line=4, character=14), end=Position(line=4, character=15)), # 5
                message="Parámetro 'valor' (pasado Por Referencia a 'Incrementar') debe ser una variable, no una constante o expresión.",
                severity=DiagnosticSeverity.Error,
            )
        ]
        await self.helper_test_diagnostics_on_open("p1_func_byref_literal", content, expected)

    # --- P1 Batch 1, Part B: Integration Tests ---

    async def test_p1_func_return_not_assigned(self):
        content = "Proceso Principal\nFinProceso\nFuncion resultado = Test()\n  Definir x Como Entero;\n  x <- 5;\nFinFuncion"
        #        012345678
        expected = [
            Diagnostic(
                range=Range(start=Position(line=2, character=8), end=Position(line=2, character=17)), # "resultado"
                message="Variable de retorno 'resultado' en Funcion 'Test' no asignada.",
                severity=DiagnosticSeverity.Error,
            )
        ]
        await self.helper_test_diagnostics_on_open("p1_func_ret_not_assigned", content, expected)

    async def test_p1_func_called_as_subproceso(self):
        content = "Proceso Principal\n  Definir y Como Entero;\n  y <- MiFunc(1);\n  MiFunc(2); \nFinProceso\nFuncion res = MiFunc(a Como Entero)\n  res <- a * 2;\nFinFuncion"
        #          01234567
        expected = [
            Diagnostic(
                range=Range(start=Position(line=3, character=2), end=Position(line=3, character=11)), # MiFunc(2)
                message="No se puede llamar a la Funcion 'MiFunc' como si fuera un SubProceso (su resultado no se está utilizando).",
                severity=DiagnosticSeverity.Warning,
            )
        ]
        await self.helper_test_diagnostics_on_open("p1_func_called_as_sub", content, expected)

    async def test_p1_subproceso_result_assigned(self):
        content = "Proceso Principal\n  Definir x Como Entero;\n  x <- MiSubProceso();\nFinProceso\nSubProceso MiSubProceso()\n  Escribir \"hola\";\nFinSubProceso"
        #          01234567890123
        expected = [
            Diagnostic(
                range=Range(start=Position(line=2, character=2), end=Position(line=2, character=20)), # x <- MiSubProceso()
                message="No se puede asignar el resultado de un SubProceso ('MiSubProceso') a una variable.",
                severity=DiagnosticSeverity.Error,
            )
        ]
        await self.helper_test_diagnostics_on_open("p1_subproc_res_assigned", content, expected)

    async def test_p1_array_incorrect_index_count_too_few(self):
        content = "Proceso TestArrIdxCount\n  Dimension miMatriz[3,4];\n  miMatriz[1] <- 10;\nFinProceso"
        #          0123456789
        expected = [
            Diagnostic(
                range=Range(start=Position(line=2, character=2), end=Position(line=2, character=14)), # miMatriz[1]
                message="Número incorrecto de índices para el array 'miMatriz'. Se esperaban 2 pero se usaron 1.",
                severity=DiagnosticSeverity.Error,
            )
        ]
        await self.helper_test_diagnostics_on_open("p1_arr_idx_too_few", content, expected)

    async def test_p1_array_index_out_of_range_literal(self):
        content = "Proceso TestArrIdxRange\n  Dimension miVector[5];\n  miVector[6] <- 20;\nFinProceso"
        #             0
        expected = [
            Diagnostic(
                range=Range(start=Position(line=2, character=11), end=Position(line=2, character=12)), # 6
                message="Índice '6' fuera de rango para el array 'miVector' (Dimensión 1: 1..5).",
                severity=DiagnosticSeverity.Error,
            )
        ]
        await self.helper_test_diagnostics_on_open("p1_arr_idx_out_of_range", content, expected)

    async def test_p1_builtin_longitud_wrong_arg_type(self):
        content = "Proceso TestBuiltinLongitud\n  Definir x Como Entero;\n  x <- Longitud(123);\nFinProceso"
        #                        012
        expected = [
            Diagnostic(
                range=Range(start=Position(line=2, character=16), end=Position(line=2, character=19)), # 123
                message="Argumento 1 para 'longitud' de tipo incorrecto. Se esperaba 'cadena' pero se pasó 'entero'.",
                severity=DiagnosticSeverity.Error,
            )
        ]
        await self.helper_test_diagnostics_on_open("p1_builtin_long_wrong_type", content, expected)

    async def test_p1_builtin_subcadena_wrong_arg_count(self):
        content = "Proceso TestBuiltinSubcadena\n  Definir s Como Caracter;\n  s <- Subcadena(\"hola\", 1);\nFinProceso"
        #          012345678901234567
        expected = [
            Diagnostic(
                range=Range(start=Position(line=2, character=7), end=Position(line=2, character=27)), # Subcadena("hola", 1)
                message="Número incorrecto de argumentos para 'subcadena'. Se esperaban entre 3 y 3, pero se pasaron 2.",
                severity=DiagnosticSeverity.Error,
            )
        ]
        await self.helper_test_diagnostics_on_open("p1_builtin_subcad_wrong_count", content, expected)

    # --- P2-Low Priority Diagnostics: Integration Tests ---

    async def test_p2_empty_block_warning(self):
        content = "Proceso TestEmptyBlock\n  Definir cond Como Logico; cond <- VERDADERO;\n  Si cond Entonces\n  FinSi\nFinProceso"
        #          01
        expected = [
            Diagnostic(
                range=Range(start=Position(line=2, character=28), end=Position(line=2, character=30)), # "Si"
                message="Bloque 'si' vacío. Se esperaba contenido.",
                severity=DiagnosticSeverity.Warning,
            )
        ]
        await self.helper_test_diagnostics_on_open("p2_empty_block", content, expected)

    async def test_p2_unused_variable_warning(self):
        content = "Proceso TestUnusedVar\n  Definir x Como Entero;\n  Definir y Como Caracter;\n  y <- \"hola\";\n  Escribir y;\nFinProceso"
        #        0 (for variable x)
        expected = [
            Diagnostic(
                range=Range(start=Position(line=1, character=0), end=Position(line=1, character=1)), # "x" (approx range)
                message="Variable 'x' definida pero no utilizada.",
                severity=DiagnosticSeverity.Warning,
            )
        ]
        await self.helper_test_diagnostics_on_open("p2_unused_var", content, expected)

    async def test_p2_missing_colon_caso_warning(self):
        content = "Proceso TestMissingColon\n  Definir opc Como Entero;\n  opc <- 1;\n  Segun opc Hacer\n    Caso 1 Escribir \"Uno\";\n  FinSegun\nFinProceso"
        #                 01234567890123
        expected = [
            Diagnostic(
                range=Range(start=Position(line=4, character=11), end=Position(line=4, character=12)), # After "Caso 1"
                message="Se esperaba ':' después del valor en 'Caso'.",
                severity=DiagnosticSeverity.Warning,
            )
        ]
        await self.helper_test_diagnostics_on_open("p2_missing_colon_caso", content, expected)

    async def test_p2_empty_escribir_warning(self):
        content = "Proceso TestEmptyEscribir\n  Escribir;\nFinProceso"
        #          01234567
        expected = [
            Diagnostic(
                range=Range(start=Position(line=1, character=2), end=Position(line=1, character=10)), # "Escribir"
                message="Comando 'Escribir' requiere una o más expresiones.",
                severity=DiagnosticSeverity.Warning,
            )
        ]
        await self.helper_test_diagnostics_on_open("p2_empty_escribir", content, expected)

    async def test_p2_keyword_alias_algoritmo_warning(self):
        content = "Algoritmo TestAlias\nFinAlgoritmo"
        #          012345678
        expected = [
            Diagnostic(
                range=Range(start=Position(line=0, character=0), end=Position(line=0, character=9)), # "Algoritmo"
                message="Se recomienda usar 'Proceso' en lugar de 'Algoritmo' para consistencia.",
                severity=DiagnosticSeverity.Warning,
            )
        ]
        await self.helper_test_diagnostics_on_open("p2_alias_algoritmo", content, expected)
        
    async def test_p2_empty_comment_warning(self):
        content = "Proceso TestEmptyComment\n  //    \nFinProceso"
        #          01234567
        expected = [
            Diagnostic(
                range=Range(start=Position(line=1, character=2), end=Position(line=1, character=9)), # The whole comment line
                message="Comentario vacío.",
                severity=DiagnosticSeverity.Warning,
            )
        ]
        await self.helper_test_diagnostics_on_open("p2_empty_comment", content, expected)


if __name__ == "__main__":
    unittest.main()
