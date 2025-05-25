import logging
from typing import List, Optional

from pygls.server import LanguageServer
from lsprotocol.types import (
    DidChangeTextDocumentParams,
    DidCloseTextDocumentParams,
    DidOpenTextDocumentParams,
    DidSaveTextDocumentParams,
    DocumentFormattingParams,
    InitializeParams,
    InitializeResult,
    InitializeResultServerInfoType,
    Position,
    Range,
    ServerCapabilities,
    TextDocumentSyncKind,
    TextEdit,
)

# Import the formatter function
from .formatter import format_pseint_code

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
        ),
    )


@server.feature("textDocument/didOpen")
async def did_open(ls: LanguageServer, params: DidOpenTextDocumentParams):
    logging.info(f"File Opened: {params.text_document.uri}")


@server.feature("textDocument/didChange")
async def did_change(ls: LanguageServer, params: DidChangeTextDocumentParams):
    logging.info(f"File Changed: {params.text_document.uri}")


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
        formatted_code = format_pseint_code(source_code)

        if formatted_code == source_code:
            logging.info(f"No formatting changes for {document_uri}")
            return []

        lines = source_code.splitlines()
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
