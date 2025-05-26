#!/usr/bin/env python3
import logging
import sys
from pathlib import Path
from typing import List, Optional

from pygls.server import LanguageServer
from lsprotocol.types import (
    DidChangeTextDocumentParams,
    DidCloseTextDocumentParams,
    DidOpenTextDocumentParams,
    DidSaveTextDocumentParams,
    DocumentFormattingParams,
    DiagnosticOptions,  # Added
    InitializeParams,
    InitializeResult,
    InitializeResultServerInfoType,
    Position,
    Range,
    ServerCapabilities,
    TextDocumentSyncKind,
    TextEdit,
)

# Ensure we can import from the current directory
script_dir = Path(__file__).parent.absolute()
if str(script_dir) not in sys.path:
    sys.path.insert(0, str(script_dir))

# Import the formatter function and encoding utilities
try:
    from .formatter import format_pseint_code
    from .encoding_utils import ensure_clean_text
    from .diagnostics import get_diagnostics  # Added
except ImportError:
    from formatter import format_pseint_code
    from encoding_utils import ensure_clean_text
    from diagnostics import get_diagnostics  # Added

logging.basicConfig(level=logging.DEBUG, filename="/tmp/pseint_lsp.log")

server = LanguageServer("pseint-lsp-py", "0.1.0")


@server.feature("initialize")
def initialize(params: InitializeParams) -> InitializeResult:
    logging.info(
        f"Initializing PSeInt LSP Server. Client capabilities: {params.capabilities}"
    )
    return InitializeResult(
        server_info=InitializeResultServerInfoType(
            name="pseint-lsp-py",
            version="0.1.0",
        ),
        capabilities=ServerCapabilities(
            text_document_sync=TextDocumentSyncKind.Full,
            document_formatting_provider=True,
            diagnostic_provider=DiagnosticOptions(  # Added
                inter_file_dependencies=False,
                workspace_diagnostics=False,
            ),
        ),
    )


@server.feature("textDocument/didOpen")
async def did_open(ls: LanguageServer, params: DidOpenTextDocumentParams):
    logging.info(f"File Opened: {params.text_document.uri}")
    document_uri = params.text_document.uri
    document = ls.workspace.get_document(document_uri) # type: ignore
    if document:
        diagnostics = get_diagnostics(document.source)
        ls.publish_diagnostics(document_uri, diagnostics)
    else:
        logging.warning(f"Document not found for diagnostics on open: {document_uri}")


@server.feature("textDocument/didChange")
async def did_change(ls: LanguageServer, params: DidChangeTextDocumentParams):
    logging.info(f"File Changed: {params.text_document.uri}")
    document_uri = params.text_document.uri
    # For DidChangeTextDocumentParams, the content is in params.content_changes[0].text
    # assuming TextDocumentSyncKind.Full (which it is)
    # However, pygls updates the workspace document automatically.
    document = ls.workspace.get_document(document_uri) # type: ignore
    if document:
        diagnostics = get_diagnostics(document.source)
        ls.publish_diagnostics(document_uri, diagnostics)
    else:
        logging.warning(f"Document not found for diagnostics on change: {document_uri}")


@server.feature("textDocument/didSave")
async def did_save(ls: LanguageServer, params: DidSaveTextDocumentParams):
    logging.info(f"File Saved: {params.text_document.uri}")


@server.feature("textDocument/didClose")
async def did_close(ls: LanguageServer, params: DidCloseTextDocumentParams):
    logging.info(f"File Closed: {params.text_document.uri}")


@server.feature("textDocument/formatting")
def format_document(
    ls: LanguageServer, params: DocumentFormattingParams
) -> Optional[List[TextEdit]]:
    document_uri = params.text_document.uri
    # Type: ignore for pygls workspace document retrieval
    document = ls.workspace.get_document(document_uri)  # type: ignore

    if not document:
        logging.warning(f"Document not found for formatting: {document_uri}")
        return None

    source_code = document.source
    logging.info(f"Attempting to format: {document_uri}")

    try:
        # Apply editor-agnostic encoding correction
        clean_source_code = ensure_clean_text(source_code, document_uri)
        
        # Log if encoding issues were detected and fixed
        if clean_source_code != source_code:
            logging.info(f"Applied encoding corrections to {document_uri}")
        
        formatted_code = format_pseint_code(clean_source_code)

        if formatted_code == clean_source_code:
            logging.info(f"No formatting changes for {document_uri}")
            return []

        lines = clean_source_code.splitlines()
        range_end_line = len(lines)

        doc_range = Range(
            start=Position(line=0, character=0),
            end=Position(line=range_end_line, character=0),
        )

        logging.info(
            f"Applying format for {document_uri}. Original lines: {len(lines)}. Range end line: {range_end_line}"
        )
        return [TextEdit(range=doc_range, new_text=formatted_code)]

    except Exception as e:
        logging.error(f"Error formatting {document_uri}: {e}", exc_info=True)
        return None


def run():
    logging.info("Starting PSeInt LSP Server (Python) via stdio")
    server.start_io()
    logging.info("PSeInt LSP Server (Python) stopped")


if __name__ == "__main__":
    run()
