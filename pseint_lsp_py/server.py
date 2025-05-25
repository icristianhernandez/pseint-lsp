import logging
from typing import List, Optional

from pygls.server import LanguageServer
from pygls.lsp.types import (
    DidChangeTextDocumentParams,
    DidCloseTextDocumentParams,
    DidOpenTextDocumentParams,
    DidSaveTextDocumentParams,
    DocumentFormattingParams,
    InitializeParams,
    InitializeResult,
    MessageType,
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
    logging.info(f"Initializing PSeInt LSP Server. Client capabilities: {params.capabilities}")
    server.show_message_log("PSeInt LSP Server initializing...", MessageType.Info)
    return InitializeResult(
        server_info={
            "name": "pseint-lsp-py",
            "version": "0.1.0",
        },
        capabilities=ServerCapabilities(
            text_document_sync=TextDocumentSyncKind.FULL,
            document_formatting_provider=True,
        ),
    )

@server.feature("textDocument/didOpen")
async def did_open(ls: LanguageServer, params: DidOpenTextDocumentParams):
    ls.show_message_log(f"File Opened: {params.text_document.uri}", MessageType.Info)
    logging.info(f"File Opened: {params.text_document.uri}")

@server.feature("textDocument/didChange")
async def did_change(ls: LanguageServer, params: DidChangeTextDocumentParams):
    ls.show_message_log(f"File Changed: {params.text_document.uri}", MessageType.Info)
    logging.info(f"File Changed: {params.text_document.uri}")

@server.feature("textDocument/didSave")
async def did_save(ls: LanguageServer, params: DidSaveTextDocumentParams):
    ls.show_message_log(f"File Saved: {params.text_document.uri}", MessageType.Info)
    logging.info(f"File Saved: {params.text_document.uri}")

@server.feature("textDocument/didClose")
async def did_close(ls: LanguageServer, params: DidCloseTextDocumentParams):
    ls.show_message_log(f"File Closed: {params.text_document.uri}", MessageType.Info)
    logging.info(f"File Closed: {params.text_document.uri}")

@server.feature("textDocument/formatting")
def format_document(ls: LanguageServer, params: DocumentFormattingParams) -> Optional[List[TextEdit]]:
    document_uri = params.text_document.uri
    document = ls.workspace.get_document(document_uri)
    
    if not document:
        ls.show_message_log(f"Document not found for formatting: {document_uri}", MessageType.Error)
        logging.warning(f"Document not found for formatting: {document_uri}")
        return None

    source_code = document.source
    ls.show_message_log(f"Formatting document: {document_uri}", MessageType.Info)
    logging.info(f"Attempting to format: {document_uri}")

    try:
        formatted_code = format_pseint_code(source_code)
        
        if formatted_code == source_code:
            ls.show_message_log(f"No formatting changes needed for: {document_uri}", MessageType.Info)
            logging.info(f"No formatting changes for {document_uri}")
            return [] 

        lines = source_code.splitlines()
        range_end_line = len(lines)
        
        doc_range = Range(
            start=Position(line=0, character=0),
            end=Position(line=range_end_line, character=0)
        )

        logging.info(f"Applying format for {document_uri}. Original lines: {len(lines)}. Range end line: {range_end_line}")
        return [TextEdit(range=doc_range, new_text=formatted_code)]
        
    except Exception as e:
        ls.show_message_log(f"Error formatting {document_uri}: {str(e)}", MessageType.Error)
        logging.error(f"Error formatting {document_uri}: {e}", exc_info=True)
        return None

def run():
    logging.info("Starting PSeInt LSP Server (Python) via stdio")
    server.start_io()
    logging.info("PSeInt LSP Server (Python) stopped")

if __name__ == "__main__":
    run()
