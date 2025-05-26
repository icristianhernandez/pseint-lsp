import unittest
import sys
import os
from unittest.mock import Mock, patch
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
    CompletionParams,
    Position,
    CompletionList,
    CompletionItemKind,
    InsertTextFormat,
    Hover, HoverParams, MarkupContent, MarkupKind, # For Hover
    SignatureHelp, SignatureHelpParams, SignatureInformation, ParameterInformation, # For SignatureHelp
    SignatureHelpContext, SignatureHelpTriggerKind # For SignatureHelp context
)

# Import server module
import server
from server import completions as server_completions
from server import hover_handler as server_hover_handler # Import the hover handler
from server import signature_help_handler as server_signature_help_handler # Import the signature help handler


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

        # Create mock language server
        mock_ls = Mock()

        # Call the did_open function
        await server.did_open(mock_ls, params)

        # Verify logging was called
        mock_logging.info.assert_called_once()

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

        # Create mock language server
        mock_ls = Mock()

        # Call the did_change function
        await server.did_change(mock_ls, params)

        # Verify logging was called
        mock_logging.info.assert_called_once()

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

    async def _get_completions(self, content: str, line: int, char: int, uri: str = "file:///test_doc.psc") -> CompletionList:
        """Helper method to simulate completion requests."""
        mock_ls = Mock(spec=server.LanguageServer)
        mock_workspace = Mock()
        mock_document = Mock()

        mock_document.source = content
        mock_document.uri = uri
        
        mock_workspace.get_document.return_value = mock_document
        mock_ls.workspace = mock_workspace

        params = CompletionParams(
            text_document=TextDocumentIdentifier(uri=uri),
            position=Position(line=line, character=char)
        )
        
        # Call the server's completion handler
        return await server_completions(mock_ls, params)

    async def test_completions_toplevel_empty_file(self):
        """Test completions in an empty file (top-level)."""
        content = ""
        completions_result = await self._get_completions(content, 0, 0)
        labels = [item.label for item in completions_result.items]

        self.assertIn("Proceso", labels)
        self.assertIn("Algoritmo", labels)
        self.assertIn("Funcion", labels) # Snippet and Keyword
        self.assertIn("SubProceso", labels) # Snippet and Keyword
        
        # Check for absence of block-closing keywords
        self.assertNotIn("FinProceso", labels)
        self.assertNotIn("FinSi", labels)
        self.assertNotIn("Sino", labels)
        self.assertNotIn("Definir", labels) # Should not be suggested in completely empty file before Proceso/Algoritmo

    async def test_completions_inside_proceso_block_general(self):
        """Test general keyword completions inside a Proceso block."""
        content = """
Proceso Test
    |
FinProceso
"""
        # Cursor at line 2, char 4 (represented by |)
        completions_result = await self._get_completions(content, 2, 4)
        labels = [item.label for item in completions_result.items]

        expected_keywords = ["Definir", "Leer", "Escribir", "Si", "Mientras", "Para", "Segun", "Repetir", "Dimension"]
        for kw in expected_keywords:
            self.assertIn(kw, labels)
        
        self.assertIn("FinProceso", labels) # FinProceso should be available
        self.assertNotIn("Proceso", labels) # Should not suggest starting a new Proceso
        self.assertNotIn("Algoritmo", labels) # Snippet for Algorithm should be filtered out
        self.assertNotIn("FinSi", labels) # No Si block open

    async def test_completions_inside_proceso_suggests_finproceso_at_end(self):
        """Test FinProceso is suggested appropriately."""
        content = """
Proceso Test
    Definir x Como Entero;
    |
"""
        # Cursor at line 3, char 4
        completions_result = await self._get_completions(content, 3, 4)
        labels = [item.label for item in completions_result.items]
        self.assertIn("FinProceso", labels)

    async def test_completions_inside_si_block(self):
        """Test completions inside an If (Si) block."""
        content = """
Proceso Test
    Definir x Como Entero;
    Si x > 0 Entonces
        | // Cursor here
    FinSi
FinProceso
"""
        # Cursor at line 4, char 8
        completions_result = await self._get_completions(content, 4, 8)
        labels = [item.label for item in completions_result.items]

        self.assertIn("Escribir", labels)
        self.assertIn("Leer", labels)
        self.assertIn("Definir", labels) # Can define local to Si
        self.assertIn("Sino", labels)
        self.assertIn("FinSi", labels)
        self.assertNotIn("FinProceso", labels) # Not the immediate next suggestion, but should be available if typed

    async def test_completions_inside_si_block_after_sino(self):
        """Test completions inside an If-Else (Si-Sino) block, after Sino."""
        content = """
Proceso Test
    Definir x Como Entero;
    Si x > 0 Entonces
        Escribir "Mayor";
    Sino
        | // Cursor here
    FinSi
FinProceso
"""
        # Cursor at line 6, char 8
        completions_result = await self._get_completions(content, 6, 8)
        labels = [item.label for item in completions_result.items]

        self.assertIn("Escribir", labels)
        self.assertIn("Leer", labels)
        self.assertIn("FinSi", labels)
        self.assertNotIn("Sino", labels) # Sino already used for this Si

    async def test_completions_no_closing_keywords_outside_blocks(self):
        """Test that block-closing keywords are not suggested when no block is open."""
        content = """
Proceso Test
    Definir x Como Entero;
    x <- 10;
    | // Cursor here, outside any specific sub-block like Si or Mientras
FinProceso
"""
        # Cursor at line 4, char 4
        completions_result = await self._get_completions(content, 4, 4)
        labels = [item.label for item in completions_result.items]

        self.assertNotIn("FinSi", labels)
        self.assertNotIn("Sino", labels)
        self.assertNotIn("FinMientras", labels)
        self.assertNotIn("Hasta Que", labels)
        self.assertIn("FinProceso", labels) # This is valid here

    async def test_completions_variable_suggestion_in_scope(self):
        """Test that user-defined variables are suggested within their scope."""
        content = """
Proceso TestScope
    Definir miNumero Como Entero;
    Definir otroValor Como Real;
    miN| // Cursor here, typing miNumero
FinProceso
"""
        # Cursor at line 4, char 7
        completions_result = await self._get_completions(content, 4, 7) # Line 4, after "miN"
        labels = [item.label for item in completions_result.items]
        item_details = {item.label: item for item in completions_result.items}


        self.assertIn("miNumero", labels)
        self.assertIn("otroValor", labels) # Should also be suggested as it's in scope

        if "miNumero" in item_details:
            self.assertEqual(item_details["miNumero"].kind, CompletionItemKind.VARIABLE)
            self.assertIn("Entero", item_details["miNumero"].detail if item_details["miNumero"].detail else "")
            
    async def test_completions_variable_suggestion_out_of_scope(self):
        """Test that variables are not suggested outside their defined scope."""
        content = """
Proceso TestOuter
    Definir varGlobal Como Texto;
FinProceso

SubProceso OtroSub()
    // varGlobal should not be suggested here by default PSeInt scoping rules
    | // Cursor here
FinSubProceso
"""
        # Cursor at line 7, char 4
        completions_result = await self._get_completions(content, 7, 4)
        labels = [item.label for item in completions_result.items]
        self.assertNotIn("varGlobal", labels)

    async def test_completions_function_param_suggestion_in_scope(self):
        """Test that function parameters are suggested inside the function."""
        content = """
Funcion resultado = MiFuncion(param1 Como Entero, paramOtro Como Caracter)
    Definir suma Como Entero;
    suma <- param| // Cursor here, typing param1 or paramOtro
FinFuncion
"""
        # Cursor at line 3, char 18
        completions_result = await self._get_completions(content, 3, 18)
        labels = [item.label for item in completions_result.items]
        item_details = {item.label: item for item in completions_result.items}

        self.assertIn("param1", labels)
        self.assertIn("paramOtro", labels)
        self.assertIn("suma", labels) # Local var
        self.assertIn("resultado", labels) # Return var also in scope

        if "param1" in item_details:
            self.assertEqual(item_details["param1"].kind, CompletionItemKind.VARIABLE) # Params treated as vars
            self.assertIn("Entero", item_details["param1"].detail if item_details["param1"].detail else "")
        if "resultado" in item_details: # The return variable
             self.assertEqual(item_details["resultado"].kind, CompletionItemKind.VARIABLE)


    async def test_completions_function_definition_suggestion(self):
        """Test that defined functions are suggested after their definition."""
        content = """
Proceso Principal
    Definir x Como Entero;
    x <- MiF| // Cursor here, typing MiFuncion
FinProceso

Funcion res = MiFuncion(n Como Entero)
    res <- n * 2;
FinFuncion
"""
        # Cursor at line 3, char 11
        completions_result = await self._get_completions(content, 3, 11)
        labels = [item.label for item in completions_result.items]
        item_details = {item.label: item for item in completions_result.items}

        self.assertIn("MiFuncion", labels)
        if "MiFuncion" in item_details:
            self.assertEqual(item_details["MiFuncion"].kind, CompletionItemKind.FUNCTION)
            self.assertIn("(n)", item_details["MiFuncion"].detail if item_details["MiFuncion"].detail else "")
            
    async def test_completions_array_suggestion_in_scope(self):
        """Test that defined arrays are suggested."""
        content = """
Proceso TestArray
    Dimension miVector[5];
    Dimension miMatriz[3,4];
    miV| // Cursor here
FinProceso
"""
        # Cursor at line 4, char 7
        completions_result = await self._get_completions(content, 4, 7)
        labels = [item.label for item in completions_result.items]
        item_details = {item.label: item for item in completions_result.items}

        self.assertIn("miVector", labels)
        self.assertIn("miMatriz", labels)
        if "miVector" in item_details:
            self.assertEqual(item_details["miVector"].kind, CompletionItemKind.VARIABLE) # Arrays are Variable kind
            self.assertIn("Arreglo", item_details["miVector"].detail if item_details["miVector"].detail else "")
            self.assertIn("[5]", item_details["miVector"].detail if item_details["miVector"].detail else "")


    async def test_completions_inside_mientras_block(self):
        content = "Proceso Loop\n  Mientras x < 10 Hacer\n    |\n  FinMientras\nFinProceso"
        # Cursor at line 2, char 4 (0-indexed)
        completions = await self._get_completions(content, 2, 4)
        labels = [item.label for item in completions.items]
        self.assertIn("Escribir", labels)
        self.assertIn("FinMientras", labels)
        self.assertNotIn("Sino", labels)

    async def test_completions_inside_para_block(self):
        content = "Proceso Loop\n  Para i<-0 Hasta 9 Con Paso 1 Hacer\n    |\n  FinPara\nFinProceso"
        # Cursor at line 2, char 4
        completions = await self._get_completions(content, 2, 4)
        labels = [item.label for item in completions.items]
        self.assertIn("Escribir", labels)
        self.assertIn("FinPara", labels)

    async def test_completions_inside_segun_block(self):
        content = "Proceso Select\n  Definir opc Como Entero;\n  Segun opc Hacer\n    Caso 1:\n      |\n    De Otro Modo:\n  FinSegun\nFinProceso"
        # Cursor at line 4, char 6 (inside Caso 1)
        completions = await self._get_completions(content, 4, 6)
        labels = [item.label for item in completions.items]
        self.assertIn("Escribir", labels)
        self.assertIn("Caso", labels) # Can have more cases
        self.assertIn("De Otro Modo", labels)
        self.assertIn("FinSegun", labels)

        # Test completion for "Caso" itself or "De Otro Modo"
        content_for_caso = "Proceso Select\n  Definir opc Como Entero;\n  Segun opc Hacer\n    |\n  FinSegun\nFinProceso"
        # Cursor at line 3, char 4 (inside Segun, before any Caso)
        completions_for_caso = await self._get_completions(content_for_caso, 3, 4)
        labels_for_caso = [item.label for item in completions_for_caso.items]
        self.assertIn("Caso", labels_for_caso)
        self.assertIn("De Otro Modo", labels_for_caso)


    async def test_completions_inside_repetir_block(self):
        content = "Proceso Loop\n  Repetir\n    |\n  Hasta Que x > 10\nFinProceso"
        # Cursor at line 2, char 4
        completions = await self._get_completions(content, 2, 4)
        labels = [item.label for item in completions.items]
        self.assertIn("Escribir", labels)
        self.assertIn("Hasta Que", labels)

    # --- Helper methods for Hover and Signature Help ---

    async def _get_hover_info(self, content: str, line: int, char: int, uri: str = "file:///test_hover.psc") -> Optional[Hover]:
        """Helper method to simulate hover requests."""
        mock_ls = Mock(spec=server.LanguageServer)
        mock_workspace = Mock()
        mock_document = Mock()

        mock_document.source = content
        mock_document.uri = uri
        
        mock_workspace.get_document.return_value = mock_document
        mock_ls.workspace = mock_workspace

        params = HoverParams(
            text_document=TextDocumentIdentifier(uri=uri),
            position=Position(line=line, character=char)
        )
        return await server_hover_handler(mock_ls, params)

    async def _get_signature_help_info(self, content: str, line: int, char: int, 
                                     trigger_char: Optional[str] = '(', 
                                     uri: str = "file:///test_sighelp.psc") -> Optional[SignatureHelp]:
        """Helper method to simulate signature help requests."""
        mock_ls = Mock(spec=server.LanguageServer)
        mock_workspace = Mock()
        mock_document = Mock()

        mock_document.source = content
        mock_document.uri = uri
        
        mock_workspace.get_document.return_value = mock_document
        mock_ls.workspace = mock_workspace

        context = SignatureHelpContext(
            trigger_kind=SignatureHelpTriggerKind.TriggerCharacter if trigger_char else SignatureHelpTriggerKind.Invoked,
            trigger_character=trigger_char,
            is_retrigger=False,
            active_signature_help=None 
        )

        params = SignatureHelpParams(
            text_document=TextDocumentIdentifier(uri=uri),
            position=Position(line=line, character=char),
            context=context
        )
        return await server_signature_help_handler(mock_ls, params)

    # --- Hover Tests ---

    async def test_hover_on_variable_definition(self):
        content = "Proceso Test\n  Definir miVar Como Entero;\nFinProceso"
        # Hover on 'miVar' in "Definir miVar Como Entero;" (line 1, char 10-15)
        # Parser stores name_start_char relative to stripped line "Definir miVar Como Entero;" -> "miVar" is at 8
        # "  Definir miVar Como Entero;" -> lstrip() -> "Definir miVar Como Entero;"
        # leading whitespace is 2.  8 + 2 = 10
        hover_info = await self._get_hover_info(content, 1, 12) 
        self.assertIsNotNone(hover_info)
        if hover_info and isinstance(hover_info.contents, MarkupContent):
            self.assertIn("**miVar** `(variable)`", hover_info.contents.value)
            self.assertIn("**Tipo**: `Entero`", hover_info.contents.value)
            self.assertIn("*Definido en línea: 2*", hover_info.contents.value) # Parser uses 1-based lines

    async def test_hover_on_function_definition(self):
        content = "Proceso Test\n  Funcion res = MiFunc(p1 Como Real)\n    res = p1 * 2\n  FinFuncion\nFinProceso"
        # Hover on 'MiFunc' in "Funcion res = MiFunc(p1 Como Real)"
        # "  Funcion res = MiFunc(p1 Como Real)" -> lstrip -> "Funcion res = MiFunc(p1 Como Real)"
        # "MiFunc" is at char 16 of stripped. Leading whitespace 2. 16+2=18
        hover_info = await self._get_hover_info(content, 1, 20) 
        self.assertIsNotNone(hover_info)
        if hover_info and isinstance(hover_info.contents, MarkupContent):
            self.assertIn("**MiFunc** `(function)`", hover_info.contents.value)
            self.assertIn("**Parámetros**: `p1` Como `Real`", hover_info.contents.value)
            self.assertIn("**Retorna**: `res`", hover_info.contents.value) # Parser implies func name if not specified
            self.assertIn("*Definido en línea: 2*", hover_info.contents.value)

    async def test_hover_on_subproceso_definition(self):
        content = "Proceso Test\n  SubProceso MiSub(p1 Por Referencia Como Logico)\n    Escribir p1;\n  FinSubProceso\nFinProceso"
        # Hover on 'MiSub' in "SubProceso MiSub(p1 Por Referencia Como Logico)"
        # "  SubProceso MiSub(..." -> lstrip -> "SubProceso MiSub(..."
        # "MiSub" is at char 11 of stripped. Leading whitespace 2. 11+2=13
        hover_info = await self._get_hover_info(content, 1, 15)
        self.assertIsNotNone(hover_info)
        if hover_info and isinstance(hover_info.contents, MarkupContent):
            self.assertIn("**MiSub** `(subproceso)`", hover_info.contents.value)
            self.assertIn("`p1` Como `Logico` (Por Referencia)", hover_info.contents.value)
            self.assertIn("*Definido en línea: 2*", hover_info.contents.value)

    async def test_hover_on_variable_usage(self):
        content = "Proceso Test\n  Definir count Como Entero;\n  count = count + 1;\nFinProceso"
        # Hover on the second 'count' (usage) (line 2, char 2-7)
        hover_info = await self._get_hover_info(content, 2, 4)
        self.assertIsNotNone(hover_info)
        if hover_info and isinstance(hover_info.contents, MarkupContent):
            self.assertIn("**count** `(variable)`", hover_info.contents.value)
            self.assertIn("**Tipo**: `Entero`", hover_info.contents.value)
            self.assertIn("*Definido en línea: 2*", hover_info.contents.value)

    async def test_hover_on_function_parameter_definition(self):
        content = "Proceso Test\n  Funcion res = MiFunc(paramA Como Entero)\n    res = paramA * 10;\n  FinFuncion\nFinProceso"
        # Hover on 'paramA' in "Funcion res = MiFunc(paramA Como Entero)"
        # Current parser limitation: No precise char location for 'paramA' in definition.
        # Hovering over 'paramA' (e.g. line 1, char 25) will likely resolve to 'MiFunc' or nothing.
        # If it resolves to MiFunc because get_word_at_position picks up "MiFunc" if cursor is near it,
        # or if "paramA" is picked up by get_word_at_position but not found as a standalone symbol.
        hover_info_on_param_name = await self._get_hover_info(content, 1, 25) # On "paramA"
        
        # Based on current parser, this will NOT find 'paramA' as a symbol with its own definition.
        # It will find "paramA" as a word using get_word_at_position.
        # Then, it will search for a symbol named "paramA".
        # The `analyze_document_context` populates function parameters as Symbols, but their name_start/end_char are None.
        # However, the *usage* of 'paramA' on line 2 would be hoverable if parameters were added to symbol list by parser.
        # For now, let's check if it *doesn't* find 'paramA' as a distinct variable symbol, or finds MiFunc.
        
        # Test Case 1: Hovering over "paramA" on line 1 (definition)
        # The parser _does_ create symbols for parameters. Let's check if it's found.
        # The parameters are added to the symbol list by `_parse_parameters` but without char locations.
        # The hover logic's fallback (word-based search) should find it if the parser adds params as symbols.
        # The current `_parse_parameters` in `pseint_parser.py` does NOT create symbols for parameters.
        # It only extracts them into the `details` of the function symbol.
        # Therefore, hovering on 'paramA' in the definition line will likely find no symbol or the function 'MiFunc'.
        
        if hover_info_on_param_name and isinstance(hover_info_on_param_name.contents, MarkupContent):
            # If it resolved to MiFunc (because 'paramA' is not a symbol in its own right at definition)
            self.assertNotIn("**paramA**", hover_info_on_param_name.contents.value, "Should not find paramA as a top-level symbol via definition hover")
            # It might find MiFunc if cursor is near it, or find nothing.
            # If `get_word_at_position` picks "paramA", it won't be in global symbols.
            # If it picks "MiFunc", it will show MiFunc.
            # For line 1, char 25 ("paramA"), `get_word_at_position` should return "paramA".
            # Since "paramA" is not a symbol defined independently, hover should be None.
            self.assertIsNone(hover_info_on_param_name, "Hovering on param name in definition should ideally be None or for the param if parser supported it.")
        else:
            self.assertIsNone(hover_info_on_param_name, "Expected no specific hover for param name in definition with current parser.")

        # Test Case 2: Hovering over "paramA" on line 2 (usage)
        # This depends on whether parameters are added to the symbol list by the parser and scoped correctly.
        # Current `analyze_document_context` does not add parameters from `_parse_parameters` to the main symbol list.
        hover_info_on_param_usage = await self._get_hover_info(content, 2, 10) # On "paramA" usage
        # With current parser, parameters are not added as distinct symbols to the main symbol list
        # in analyze_document_context, so they won't be found by the hover's fallback word search.
        # The parameter completion logic directly uses BlockContext.details.params.
        # This test correctly expects None if parameters are not globally queryable symbols.
        self.assertIsNone(hover_info_on_param_usage, "Expected no hover for param usage if params are not added to main symbol list by parser for general lookup.")

    async def test_hover_on_function_parameter_in_definition(self):
        """Test hover on parameter names within a Funcion definition line."""
        content = """Proceso TestHoverParam
    Funcion resultado = MiFuncionConParams(param1 Como Entero, valRef Por Referencia Como Real)
        resultado = param1 + valRef
    FinFuncion
FinProceso"""
        # Test Case 1.1: Hover on `param1`
        # "  Funcion resultado = MiFuncionConParams(param1 Como Entero, valRef Por Referencia Como Real)"
        # `param1` is approx char 39-45. `MiFuncionConParams` ends around 37. `(` is at 38. param_string starts at 39.
        # `param1` is at index 0 in param_string "param1 Como Entero, valRef Por Referencia Como Real"
        hover_info_param1 = await self._get_hover_info(content, 1, 42)  # Cursor on "param1"
        self.assertIsNotNone(hover_info_param1, "Hover on 'param1' should provide info.")
        if hover_info_param1 and isinstance(hover_info_param1.contents, MarkupContent):
            self.assertIn("**param1** `(parámetro)`", hover_info_param1.contents.value)
            self.assertIn("**Tipo**: `Entero`", hover_info_param1.contents.value)
            self.assertNotIn("Por Referencia", hover_info_param1.contents.value) # param1 is ByVal
            self.assertIn("*Parámetro de: MiFuncionConParams*", hover_info_param1.contents.value)
            self.assertIn("*Definido en línea: 2*", hover_info_param1.contents.value) # Line of the function

        # Test Case 1.2: Hover on `valRef`
        # `valRef` is approx char 59-65 in the same line.
        hover_info_valref = await self._get_hover_info(content, 1, 62)  # Cursor on "valRef"
        self.assertIsNotNone(hover_info_valref, "Hover on 'valRef' should provide info.")
        if hover_info_valref and isinstance(hover_info_valref.contents, MarkupContent):
            self.assertIn("**valRef** `(parámetro)`", hover_info_valref.contents.value)
            self.assertIn("**Tipo**: `Real`", hover_info_valref.contents.value)
            self.assertIn("**Modo**: `Por Referencia`", hover_info_valref.contents.value)
            self.assertIn("*Parámetro de: MiFuncionConParams*", hover_info_valref.contents.value)
            self.assertIn("*Definido en línea: 2*", hover_info_valref.contents.value)

    async def test_hover_on_subproceso_parameter_in_definition(self):
        """Test hover on parameter names within a SubProceso definition line."""
        content = """Proceso TestHoverSubParam
    SubProceso MiSubProcesoConParams(argA Como Logico)
        Escribir argA;
    FinSubProceso
FinProceso"""
        # Hover on `argA` in "SubProceso MiSubProcesoConParams(argA Como Logico)"
        # `argA` is approx char 35-39.
        hover_info_arga = await self._get_hover_info(content, 1, 37)  # Cursor on "argA"
        self.assertIsNotNone(hover_info_arga, "Hover on 'argA' should provide info.")
        if hover_info_arga and isinstance(hover_info_arga.contents, MarkupContent):
            self.assertIn("**argA** `(parámetro)`", hover_info_arga.contents.value)
            self.assertIn("**Tipo**: `Logico`", hover_info_arga.contents.value)
            self.assertNotIn("Por Referencia", hover_info_arga.contents.value) # argA is ByVal
            self.assertIn("*Parámetro de: MiSubProcesoConParams*", hover_info_arga.contents.value)
            self.assertIn("*Definido en línea: 2*", hover_info_arga.contents.value) # Line of the subproceso

    async def test_hover_on_no_symbol(self):
        content = "Proceso Test\n  Escribir \"Hola\";\nFinProceso"
        # Hover on 'Escribir' (a keyword, not a user-defined symbol)
        hover_info_keyword = await self._get_hover_info(content, 1, 4)
        self.assertIsNone(hover_info_keyword)

        # Hover on "Hola" (a string literal)
        hover_info_literal = await self._get_hover_info(content, 1, 12)
        self.assertIsNone(hover_info_literal)

        # Hover on empty space
        hover_info_empty = await self._get_hover_info(content, 1, 0)
        self.assertIsNone(hover_info_empty)

    # --- Signature Help Tests ---

    async def test_signature_help_simple_function_no_params(self):
        content = "Proceso Test\n  Funcion x = MiFunc()\n    x = 1\n  FinFuncion\n  Definir y Como Entero;\n  y = MiFunc(\nFinProceso"
        # Cursor at line 5, char 13 (inside MiFunc() call, after '(')
        sig_help = await self._get_signature_help_info(content, 5, 13, trigger_char='(')
        self.assertIsNotNone(sig_help)
        if sig_help:
            self.assertEqual(len(sig_help.signatures), 1)
            self.assertEqual(sig_help.signatures[0].label, "MiFunc()")
            self.assertEqual(len(sig_help.signatures[0].parameters), 0)
            self.assertEqual(sig_help.active_parameter, 0)

    async def test_signature_help_function_with_params_first_param(self):
        content = "Proceso Test\n  Funcion z = Suma(a Como Entero, b Como Entero)\n    z = a + b\n  FinFuncion\n  Definir r Como Entero;\n  r = Suma(\nFinProceso"
        # Cursor at line 5, char 11 (inside Suma() call, after '(')
        sig_help = await self._get_signature_help_info(content, 5, 11, trigger_char='(')
        self.assertIsNotNone(sig_help)
        if sig_help:
            self.assertEqual(len(sig_help.signatures), 1)
            self.assertEqual(sig_help.signatures[0].label, "Suma(a Como Entero, b Como Entero) -> z")
            self.assertEqual(len(sig_help.signatures[0].parameters), 2)
            if sig_help.signatures[0].parameters:
                 self.assertEqual(sig_help.signatures[0].parameters[0].label, "a Como Entero")
                 self.assertEqual(sig_help.signatures[0].parameters[1].label, "b Como Entero")
            self.assertEqual(sig_help.active_parameter, 0)

    async def test_signature_help_function_with_params_second_param(self):
        content = "Proceso Test\n  Funcion z = Suma(a Como Entero, b Como Entero)\n    z = a + b\n  FinFuncion\n  Definir r Como Entero;\n  r = Suma(10, \nFinProceso"
        # Cursor at line 5, char 15 (inside Suma() call, after ', ')
        sig_help = await self._get_signature_help_info(content, 5, 15, trigger_char=',')
        self.assertIsNotNone(sig_help)
        if sig_help:
            self.assertEqual(len(sig_help.signatures), 1)
            self.assertEqual(sig_help.signatures[0].label, "Suma(a Como Entero, b Como Entero) -> z")
            self.assertEqual(sig_help.active_parameter, 1)

    async def test_signature_help_subproceso_referencia(self):
        content = "Proceso Test\n  SubProceso Modificar(v Por Referencia Como Real)\n    v = v * 1.5\n  FinSubProceso\n  Definir miVal Como Real;\n  Modificar(\nFinProceso"
        # Cursor at line 5, char 12 (inside Modificar() call, after '(')
        sig_help = await self._get_signature_help_info(content, 5, 12, trigger_char='(')
        self.assertIsNotNone(sig_help)
        if sig_help:
            self.assertEqual(len(sig_help.signatures), 1)
            self.assertEqual(sig_help.signatures[0].label, "Modificar(v Por Referencia Como Real)")
            self.assertEqual(len(sig_help.signatures[0].parameters), 1)
            if sig_help.signatures[0].parameters:
                self.assertEqual(sig_help.signatures[0].parameters[0].label, "v Por Referencia Como Real")
            self.assertEqual(sig_help.active_parameter, 0)

    async def test_signature_help_not_in_call_context(self):
        content = "Proceso Test\n  Definir a Como Entero;\n  a = \nFinProceso"
        # Cursor at line 2, char 6 (after 'a = ')
        sig_help = await self._get_signature_help_info(content, 2, 6, trigger_char=None) # No specific trigger char here
        self.assertIsNone(sig_help)

    # --- Parameter Completion Tests ---
    async def test_completion_of_parameters_in_function_body(self):
        content = """Proceso TestParamCompletions
    Funcion resultado = Suma(num1 Como Entero, num2 Como Entero)
        Definir temp Como Entero;
        temp = | // Cursor here, line 3 (0-indexed)
    FinFuncion
FinProceso"""
        completions_result = await self._get_completions(content, 3, 15) # Cursor after "temp = "
        
        labels = {item.label: item for item in completions_result.items}
        
        self.assertIn("num1", labels)
        if "num1" in labels:
            self.assertEqual(labels["num1"].kind, CompletionItemKind.VARIABLE)
            self.assertIn("Parámetro (Entero)", labels["num1"].detail if labels["num1"].detail else "")

        self.assertIn("num2", labels)
        if "num2" in labels:
            self.assertEqual(labels["num2"].kind, CompletionItemKind.VARIABLE)
            self.assertIn("Parámetro (Entero)", labels["num2"].detail if labels["num2"].detail else "")

        self.assertIn("temp", labels) # Local variable
        if "temp" in labels:
            self.assertEqual(labels["temp"].kind, CompletionItemKind.VARIABLE)
            self.assertIn("Tipo: Entero", labels["temp"].detail if labels["temp"].detail else "")
        
        self.assertIn("resultado", labels) # Function's return variable also in scope
        if "resultado" in labels:
             self.assertEqual(labels["resultado"].kind, CompletionItemKind.VARIABLE) # Treated as a var in this context
             self.assertIn("Tipo: Desconocido", labels["resultado"].detail if labels["resultado"].detail else "") # Type of return var not explicitly stored by current parser for this symbol


    async def test_completion_of_parameters_in_subproceso_body_with_referencia(self):
        content = """Proceso TestParamCompletionsSub
    SubProceso ModificarLista(listaNumeros Por Referencia Como Real, indice Como Entero)
        listaNumeros[indice] = listaNumeros[indice] * 2;
        | // Cursor here, line 3
    FinSubProceso
FinProceso"""
        completions_result = await self._get_completions(content, 3, 8) # Cursor at start of empty line
        labels = {item.label: item for item in completions_result.items}

        self.assertIn("listaNumeros", labels)
        if "listaNumeros" in labels:
            self.assertEqual(labels["listaNumeros"].kind, CompletionItemKind.VARIABLE)
            self.assertIn("Parámetro (Real, Por Referencia)", labels["listaNumeros"].detail if labels["listaNumeros"].detail else "")

        self.assertIn("indice", labels)
        if "indice" in labels:
            self.assertEqual(labels["indice"].kind, CompletionItemKind.VARIABLE)
            self.assertIn("Parámetro (Entero)", labels["indice"].detail if labels["indice"].detail else "")
        
        self.assertIn("Escribir", labels) # General keywords should also be available

    async def test_completion_parameters_not_suggested_outside_function(self):
        content = """Proceso TestNoParamCompletions
    Funcion resultado = MiFunc(p1 Como Entero)
        resultado = p1;
    FinFuncion
    
    Definir x Como Entero;
    x = | // Cursor here, line 6
FinProceso"""
        completions_result = await self._get_completions(content, 6, 8) # Cursor after "x = "
        labels = {item.label: item for item in completions_result.items}

        self.assertNotIn("p1", labels)
        self.assertNotIn("resultado", labels) # 'resultado' is local to MiFunc
        self.assertIn("x", labels)
        if "x" in labels:
            self.assertEqual(labels["x"].kind, CompletionItemKind.VARIABLE)
            self.assertIn("Tipo: Entero", labels["x"].detail if labels["x"].detail else "")


if __name__ == "__main__":
    unittest.main()
