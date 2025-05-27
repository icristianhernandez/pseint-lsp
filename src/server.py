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
    InitializeParams,
    InitializeResult,
    InitializeResultServerInfoType,
    Position,
    Range,
    ServerCapabilities,
    TextDocumentSyncKind,
    TextEdit,
    TEXT_DOCUMENT_COMPLETION,
    CompletionParams,
    CompletionList,
    CompletionItem,
    TEXT_DOCUMENT_HOVER, # Added
    HoverParams,         # Added
    Hover,               # Added
    MarkupContent,       # Added
    MarkupKind,          # Added
    TEXT_DOCUMENT_SIGNATURE_HELP, # Added
    SignatureHelpParams,          # Added
    SignatureHelp,                # Added
    SignatureInformation,         # Added
    ParameterInformation,         # Added
    SignatureHelpContext,         # Added
    SignatureHelpOptions,         # Added
)

# Ensure we can import from the current directory
script_dir = Path(__file__).parent.absolute()
if str(script_dir) not in sys.path:
    sys.path.insert(0, str(script_dir))

# Import the formatter function and encoding utilities
try:
    from .formatter import format_pseint_code
    from .encoding_utils import ensure_clean_text
    from .completions import get_contextual_completions
    from .pseint_parser import analyze_document_context, Symbol # Added
except ImportError:
    from formatter import format_pseint_code
    from encoding_utils import ensure_clean_text
    from completions import get_contextual_completions
    from pseint_parser import analyze_document_context, Symbol # Added

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
            completion_provider={"trigger_characters": []},
            hover_provider=True,
            signature_help_provider=SignatureHelpOptions(trigger_characters=['(', ',']), # Added
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


@server.feature(TEXT_DOCUMENT_COMPLETION)
async def completions(ls: LanguageServer, params: CompletionParams) -> CompletionList: # Added ls and type hint
    """Provides context-aware completion items."""
    document_uri = params.text_document.uri
    document = ls.workspace.get_document(document_uri) # Use ls.workspace

    if not document:
        logging.warning(f"Document not found for completion: {document_uri}")
        return CompletionList(items=[], is_incomplete=False)

    document_content = document.source
    cursor_line_num = params.position.line
    cursor_char_num = params.position.character

    logging.info(
        f"Contextual completion request for: {document_uri} at L{cursor_line_num}:C{cursor_char_num}"
    )

    try:
        contextual_items = get_contextual_completions(
            document_content, cursor_line_num, cursor_char_num
        )
        logging.debug(f"Found {len(contextual_items)} contextual items.")
        return CompletionList(items=contextual_items, is_incomplete=False)
    except Exception as e:
        logging.error(f"Error during contextual completion for {document_uri}: {e}", exc_info=True)
        return CompletionList(items=[], is_incomplete=False)

# Helper function to extract word at a position (simplified)
def get_word_at_position(line_content: str, char_position: int) -> Optional[str]:
    import re
    # This regex finds words, including those with underscores or PSeInt specific chars if needed
    # For simplicity, using \w+ which is [a-zA-Z0-9_]
    # We iterate through all words and check if the char_position falls within one.
    for match in re.finditer(r"[\w_]+", line_content):
        start, end = match.span()
        if start <= char_position < end:
            return match.group(0)
    return None

@server.feature(TEXT_DOCUMENT_HOVER)
async def hover_handler(ls: LanguageServer, params: HoverParams) -> Optional[Hover]:
    document_uri = params.text_document.uri
    position = params.position
    document = ls.workspace.get_document(document_uri)

    if not document:
        logging.warning(f"Document not found for hover: {document_uri}")
        return None

    logging.info(f"Hover request for {document_uri} at L{position.line}:C{position.character}")

    try:
        current_line_text = document.source.splitlines()[position.line]
        word = get_word_at_position(current_line_text, position.character)

        if not word:
            logging.debug(f"No word found at cursor for hover in {document_uri}")
            return None
        
        logging.debug(f"Word under cursor: '{word}'") 

        parsed_context = analyze_document_context(document.source, position.line)
        symbols: List[Symbol] = parsed_context.get('symbols', [])
        
        # Holder for the actual symbol or parameter detail that is hovered.
        hover_target_info: Optional[Dict[str, Any]] = None 
        # Flag to indicate if the target is a parameter
        is_parameter_hover = False

        # 1. Try to find symbol by precise hover on its definition name (main symbol name)
        for sym in symbols:
            if sym.declaration_line - 1 == position.line:
                line_text_for_symbol_def = document.source.splitlines()[sym.declaration_line - 1]
                leading_whitespace = len(line_text_for_symbol_def) - len(line_text_for_symbol_def.lstrip())
                
                if sym.name_start_char is not None and sym.name_end_char is not None:
                    name_start_abs = sym.name_start_char + leading_whitespace
                    name_end_abs = sym.name_end_char + leading_whitespace
                    if name_start_abs <= position.character < name_end_abs:
                        hover_target_info = {
                            "name": sym.name, "type": sym.symbol_type, "details": sym.details,
                            "declaration_line": sym.declaration_line, "is_param": False, "parent_func_name": None
                        }
                        logging.debug(f"Hover: Matched symbol definition directly: {sym.name}")
                        break 
        
        # 2. If not found, try to find if hovering over a parameter in a function/subproceso definition
        if not hover_target_info:
            for sym in symbols:
                if sym.symbol_type in {"function", "subproceso", "subalgoritmo"} and \
                   sym.declaration_line - 1 == position.line:
                    
                    line_text_for_symbol_def = document.source.splitlines()[sym.declaration_line - 1]
                    
                    # Find start of parameter string (after '(' of function name)
                    # sym.name_end_char is relative to stripped line, so adjust with leading_whitespace
                    func_name_abs_end_char = (sym.name_end_char + 
                                             (len(line_text_for_symbol_def) - len(line_text_for_symbol_def.lstrip()))
                                            ) if sym.name_end_char is not None else 0

                    open_paren_index_on_line = -1
                    # Search for '(' starting from the character after the function name's end on the original line.
                    # This assumes function name parsing is accurate.
                    search_start_for_paren = func_name_abs_end_char
                    
                    # A more direct way if sym.details['params_str_raw_offset_in_line'] existed from parser
                    # For now, find first '(' after the function name.
                    # The parser stores sym.details['name_start_char'] relative to stripped line.
                    # And sym.details['params'] has param name_start_char relative to params_str.
                    
                    # Let's find the first '(' after the function name on the line
                    # The function name itself is at sym.name_start_char (relative to stripped)
                    # Find '(' in stripped_line, after function name
                    stripped_line_text = line_text_for_symbol_def.lstrip()
                    func_name_in_stripped = stripped_line_text[sym.name_start_char : sym.name_end_char] \
                                            if sym.name_start_char is not None and sym.name_end_char is not None else ""

                    if func_name_in_stripped == sym.name : # sanity check
                        open_paren_rel_to_stripped = stripped_line_text.find('(', sym.name_end_char if sym.name_end_char is not None else 0)
                        if open_paren_rel_to_stripped != -1:
                            leading_whitespace_offset = len(line_text_for_symbol_def) - len(stripped_line_text)
                            # This is the char index of '(' on the original, unstripped line.
                            open_paren_index_on_line = leading_whitespace_offset + open_paren_rel_to_stripped
                            
                            parameter_string_offset_on_line = open_paren_index_on_line + 1

                            for param_detail in sym.details.get('params', []):
                                if param_detail.get('name_start_char') is not None and \
                                   param_detail.get('name_end_char') is not None:
                                    
                                    abs_param_name_start = parameter_string_offset_on_line + param_detail['name_start_char']
                                    abs_param_name_end = parameter_string_offset_on_line + param_detail['name_end_char']

                                    if abs_param_name_start <= position.character < abs_param_name_end:
                                        hover_target_info = {
                                            "name": param_detail['name'], "type": param_detail.get('type', 'Desconocido'),
                                            "mode": param_detail.get('mode', "Por Valor"), "is_param": True,
                                            "parent_func_name": sym.name, "declaration_line": sym.declaration_line,
                                            "details": param_detail # Store the whole param_detail for flexibility
                                        }
                                        logging.debug(f"Hover: Matched parameter definition: {param_detail['name']} in {sym.name}")
                                        is_parameter_hover = True
                                        break # Found hovered parameter
                    if is_parameter_hover:
                        break # Found parameter in this function, stop searching other functions

        # 3. If still not found, and a 'word' was extracted by get_word_at_position,
        #    fall back to finding symbol by name (hovering on usage).
        if not hover_target_info and word:
            logging.debug(f"Hover: No direct definition or param match, trying word-based search for '{word}'")
            for sym_usage in symbols: # Renamed to sym_usage to avoid conflict
                if sym_usage.name == word:
                    if sym_usage.declaration_line -1 <= position.line and \
                       (sym_usage.scope_end_line is None or position.line <= sym_usage.scope_end_line -1) and \
                       position.line >= sym_usage.scope_start_line -1 :
                        hover_target_info = {
                            "name": sym_usage.name, "type": sym_usage.symbol_type, "details": sym_usage.details,
                            "declaration_line": sym_usage.declaration_line, "is_param": False, "parent_func_name": None
                        }
                        logging.debug(f"Hover: Matched symbol by word usage: {sym_usage.name}")
                        break
        
        # Handle case where no word was under cursor and no direct definition/param hover.
        if not hover_target_info and not word:
             logging.debug(f"No word found at cursor for hover in {document_uri} and no direct definition/param hover.")
             return None

        # --- Format Hover Content ---
        if hover_target_info:
            hover_lines = []
            s_type = found_symbol.symbol_type
            s_name = found_symbol.name
            s_details = found_symbol.details

            hover_lines.append(f"**{s_name}** `({s_type})`")

            if s_type == "variable":
                var_type = s_details.get('var_type', 'Desconocido')
                hover_lines.append(f"**Tipo**: `{var_type}`")
            elif s_type == "array":
                arr_type = s_details.get('var_type', 'Desconocido') # Assuming var_type might be stored
                dims = s_details.get('dimensions', [])
                dim_str = ", ".join(dims)
                hover_lines.append(f"**Tipo**: Arreglo de `{arr_type if arr_type else 'elementos'}`")
                hover_lines.append(f"**Dimensiones**: `[{dim_str}]`")
            elif s_type in {"function", "subproceso", "subalgoritmo"}:
                params_list = s_details.get('params', [])
                param_details_str_list = []
                for p in params_list:
                    p_name = p.get('name', 'arg')
                    p_type = p.get('type', 'Desconocido')
                    p_mode = f" ({p.get('mode')})" if p.get('mode') != "Por Valor" else ""
                    param_details_str_list.append(f"`{p_name}` Como `{p_type}`{p_mode}")
                
                param_str = ", ".join(param_details_str_list) if param_details_str_list else "ninguno"
                hover_lines.append(f"**Parámetros**: {param_str}")

                if s_type == "function" and s_details.get('return_var'):
                    # The parser stores the entire original line for 'Funcion', from which name and return_var are derived.
                    # The 'return_var' in details might be the name of the variable assigned or the function name itself.
                    hover_lines.append(f"**Retorna**: `{s_details.get('return_var')}`")
            
            hover_lines.append(f"\n*Definido en línea: {found_symbol.declaration_line + 1}*") # +1 for 1-based display

            markdown_text = "\n\n".join(hover_lines) # Use double newline for better markdown spacing
            logging.debug(f"Hover content for '{word}': {markdown_text}")
            return Hover(contents=MarkupContent(kind=MarkupKind.Markdown, value=markdown_text))
        else:
            logging.debug(f"No symbol definition found for word '{word}' in context.")
            return None

    except Exception as e:
        logging.error(f"Error during hover processing for {document_uri}: {e}", exc_info=True)
        return None

# Helper function for signatureHelp: _parse_function_call_context
def _parse_function_call_context(line_str_up_to_cursor: str) -> Optional[dict]:
    import re
    # Regex to find a potential function call at the end of the string
    # It looks for Word(possibly_some_args_or_empty
    # We are interested in the state *just before* the cursor, which is the end of line_str_up_to_cursor
    
    # Find the last open parenthesis
    open_paren_pos = line_str_up_to_cursor.rfind('(')
    if open_paren_pos == -1:
        return None

    # Extract potential function name (word before the open_paren_pos)
    # Regex to find last word before '('
    match_func_name = re.search(r"([\w_]+)\s*$", line_str_up_to_cursor[:open_paren_pos])
    if not match_func_name:
        return None
    
    function_name = match_func_name.group(1)
    
    # Content within parentheses up to cursor
    content_after_paren = line_str_up_to_cursor[open_paren_pos + 1:]
    
    # Count commas to determine active parameter.
    # This simple count assumes no nested calls or complex structures within arguments for now.
    # It also assumes cursor is not inside a string literal or comment.
    active_parameter = content_after_paren.count(',')
    
    return {
        'function_name': function_name,
        'active_parameter': active_parameter,
        'open_paren_pos': open_paren_pos # Not strictly needed by LSP spec but useful for context
    }


@server.feature(TEXT_DOCUMENT_SIGNATURE_HELP, SignatureHelpOptions(trigger_characters=['(', ',']))
async def signature_help_handler(ls: LanguageServer, params: SignatureHelpParams) -> Optional[SignatureHelp]:
    document_uri = params.text_document.uri
    position = params.position
    context = params.context

    # Ignore signature help requests if manually triggered and not an explicit trigger character
    if context and context.trigger_kind == 2 and context.trigger_character not in ['(', ',']: # 2 is SignatureHelpTriggerKind.ContentChange
         logging.debug(f"SignatureHelp: Ignoring manual trigger not by '(' or ','. Context: {context}")
         # Allowing it to proceed for now, as some clients might trigger it differently or after typing a char.
         # A more strict check might return None here.

    document = ls.workspace.get_document(document_uri)
    if not document:
        logging.warning(f"SignatureHelp: Document not found: {document_uri}")
        return None

    logging.info(f"SignatureHelp request for {document_uri} at L{position.line}:C{position.character} Trigger: {context.trigger_character if context else 'N/A'}")

    try:
        # Get the content of the line up to the cursor
        line_content = document.source.splitlines()[position.line]
        content_up_to_cursor = line_content[:position.character]
        
        call_context = _parse_function_call_context(content_up_to_cursor)

        if not call_context:
            logging.debug("SignatureHelp: Not in a function call context.")
            return None

        function_name = call_context['function_name']
        active_parameter_index = call_context['active_parameter']
        logging.debug(f"SignatureHelp: Parsed call context: func_name='{function_name}', active_param_idx={active_parameter_index}")

        # Analyze the whole document to find symbol definitions
        # Passing position.line for context, though for definitions this might not be strictly necessary
        # if symbols are globally available or parser handles this.
        parsed_doc_context = analyze_document_context(document.source, position.line)
        symbols: List[Symbol] = parsed_doc_context.get('symbols', [])
        
        found_symbol: Optional[Symbol] = None
        for sym in symbols:
            if sym.name == function_name and sym.symbol_type in {"function", "subproceso", "subalgoritmo"}:
                # Basic scope check (declaration before current line, and current line within scope if defined)
                if sym.declaration_line <= position.line and \
                   (sym.scope_end_line is None or position.line <= sym.scope_end_line) and \
                   position.line >= sym.scope_start_line:
                    found_symbol = sym
                    break
        
        if not found_symbol:
            logging.debug(f"SignatureHelp: Function/SubProceso '{function_name}' not found or not in scope.")
            return None

        s_details = found_symbol.details
        params_list_from_symbol = s_details.get('params', []) # From pseint_parser Symbol.details
        
        parameter_infos: List[ParameterInformation] = []
        param_labels_for_sig: List[str] = []

        for p_detail in params_list_from_symbol:
            p_name = p_detail.get('name', 'arg')
            p_type = p_detail.get('type', 'Desconocido')
            # Format for display in signature label and as parameter label
            param_label = f"{p_name} Como {p_type}" 
            if p_detail.get('mode') and p_detail.get('mode') != "Por Valor":
                param_label += f" ({p_detail.get('mode')})"
            
            parameter_infos.append(ParameterInformation(label=param_label))
            param_labels_for_sig.append(param_label) # Used for building the main signature string

        # Construct the main signature label
        sig_label_params = ", ".join(param_labels_for_sig)
        signature_str = f"{found_symbol.name}({sig_label_params})"
        if found_symbol.symbol_type == "function" and s_details.get('return_var'):
            signature_str += f" -> {s_details.get('return_var')}" # Or actual return type if available

        sig_info = SignatureInformation(
            label=signature_str,
            parameters=parameter_infos,
            documentation=MarkupContent(
                kind=MarkupKind.Markdown, 
                value=f"Define un {found_symbol.symbol_type} llamado '{found_symbol.name}'.\n\n*Definido en línea {found_symbol.declaration_line + 1}*."
            )
        )
        
        # Ensure active_parameter_index is within bounds
        if active_parameter_index >= len(parameter_infos) and parameter_infos:
             active_parameter_index = len(parameter_infos) -1 # Highlight last param if typing too many commas
        elif not parameter_infos and active_parameter_index > 0 :
             active_parameter_index = 0


        logging.debug(f"SignatureHelp: Providing signature for '{found_symbol.name}' with {len(parameter_infos)} params. Active index: {active_parameter_index}")
        return SignatureHelp(
            signatures=[sig_info],
            active_signature=0, # Only one signature per function in PSeInt typically
            active_parameter=active_parameter_index
        )

    except Exception as e:
        logging.error(f"Error during signature help processing for {document_uri}: {e}", exc_info=True)
        return None


def run():
    logging.info("Starting PSeInt LSP Server (Python) via stdio")
    server.start_io()
    logging.info("PSeInt LSP Server (Python) stopped")


if __name__ == "__main__":
    run()
