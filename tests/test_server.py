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


if __name__ == "__main__":
    unittest.main()
