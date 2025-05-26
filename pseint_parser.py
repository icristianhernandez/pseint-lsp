import re
from typing import List, Dict, Any, Optional, Set, Tuple

# --- Keyword Definitions ---

BLOCK_START_KEYWORDS: Set[str] = {
    "proceso", "algoritmo", "subproceso", "subalgoritmo", "funcion",
    "si", "mientras", "para", "segun", "repetir"
}

BLOCK_END_KEYWORDS: Set[str] = {
    "finproceso", "finalgoritmo", "finsubproceso", "finsubalgoritmo", "finfuncion",
    "finsi", "finmientras", "finpara", "finsegun"
    # "hasta que" is handled specially as it's part of a line that ends a Repetir block
}

DECLARATION_KEYWORDS: Set[str] = {"definir", "dimension"}

# Keywords that might appear in the middle of a line or signify structure but aren't strictly start/end
# These are useful for detailed line parsing.
STRUCTURAL_KEYWORDS: Set[str] = {
    "entonces", "sino", "hacer", "con paso", "hasta", "caso", "de otro modo", "como",
    "por referencia", "por valor"
}

ALL_KEYWORDS = BLOCK_START_KEYWORDS | BLOCK_END_KEYWORDS | DECLARATION_KEYWORDS | STRUCTURAL_KEYWORDS

# --- Data Structures ---

class Symbol:
    def __init__(self, name: str, symbol_type: str, declaration_line: int,
                 scope_start_line: int, 
                 name_start_char: Optional[int] = None, # Position relative to stripped line
                 name_end_char: Optional[int] = None,   # Position relative to stripped line
                 details: Optional[Dict[str, Any]] = None):
        self.name: str = name
        self.symbol_type: str = symbol_type  # e.g., "variable", "array", "function", "subproceso"
        self.declaration_line: int = declaration_line
        self.scope_start_line: int = scope_start_line # Line where the scope (e.g. Proceso, Funcion) begins
        self.scope_end_line: Optional[int] = None
        self.name_start_char: Optional[int] = name_start_char
        self.name_end_char: Optional[int] = name_end_char
        self.details: Dict[str, Any] = details if details else {} # e.g., var_type, params, return_var

    def __repr__(self) -> str:
        return (f"Symbol(name='{self.name}', type='{self.symbol_type}', decl_line={self.declaration_line}, "
                f"name_pos=({self.name_start_char}-{self.name_end_char}), "
                f"scope=({self.scope_start_line}-{self.scope_end_line}), details={self.details})")

class BlockContext:
    def __init__(self, keyword: str, start_line: int, name: Optional[str] = None,
                 details: Optional[Dict[str, Any]] = None):
        self.keyword: str = keyword.lower()
        self.name: Optional[str] = name
        self.start_line: int = start_line
        self.details: Dict[str, Any] = details if details else {}

    def __repr__(self) -> str:
        return f"BlockContext(keyword='{self.keyword}', name='{self.name}', start_line={self.start_line})"

# --- Parsing Functions ---

def _extract_tokens(line_content: str) -> List[str]:
    """Helper to split line by spaces but keep quoted strings together."""
    return re.findall(r'"[^"]*"|\S+', line_content)

def _parse_parameters(param_string: str) -> List[Dict[str, Any]]:
    params = []
    if not param_string:
        return params
    params_list: List[Dict[str, Any]] = []
    if not param_string:
        return params_list

    current_offset = 0
    # Split by comma, then process each segment.
    # This assumes commas are the primary separators and don't appear inside type names (usually true for PSeInt).
    for segment in param_string.split(','):
        segment_stripped = segment.strip()
        if not segment_stripped:
            current_offset += len(segment) + 1 # Advance offset by original segment length + comma
            continue

        # Regex to capture name and the rest of the segment
        # It tries to find the first word as the name.
        # Then it checks "Por Referencia" and "Como <Tipo>" in the remainder.
        
        p_name = ""
        p_type = None
        p_mode = "Por Valor" # Default
        name_start_char_in_segment = -1
        name_end_char_in_segment = -1

        # Try to find name first
        name_match = re.match(r"^\s*([\w_]+)", segment_stripped)
        if name_match:
            p_name = name_match.group(1)
            name_start_char_in_segment = name_match.start(1)
            name_end_char_in_segment = name_match.end(1)
            
            remainder_after_name = segment_stripped[name_end_char_in_segment:].lower()

            # Check for "Por Referencia"
            ref_match = re.search(r"\bpor\s+referencia\b", remainder_after_name)
            if ref_match:
                p_mode = "Por Referencia"
                # Remove "por referencia" from remainder to avoid confusion with type parsing
                remainder_after_name = remainder_after_name.replace(ref_match.group(0), "", 1).strip()

            # Check for "Como <Tipo>"
            type_match = re.search(r"\bcomo\s+([\w_]+)\b", remainder_after_name)
            if type_match:
                p_type = type_match.group(1).strip()
            elif re.search(r"\bcomo\b", remainder_after_name): # "Como" is present but type is missing/malformed
                p_type = "Desconocido"


        # Calculate absolute start/end for the name within the original param_string
        # Offset of the current segment in the original param_string
        segment_original_start_offset = param_string.find(segment, current_offset)
        # Offset of the stripped segment start within the original segment
        strip_offset_in_segment = segment.find(segment_stripped)

        abs_name_start = -1
        abs_name_end = -1

        if name_start_char_in_segment != -1:
            abs_name_start = segment_original_start_offset + strip_offset_in_segment + name_start_char_in_segment
            abs_name_end = segment_original_start_offset + strip_offset_in_segment + name_end_char_in_segment
        
        if p_name: # Only add if a name was found
            params_list.append({
                "name": p_name,
                "mode": p_mode,
                "type": p_type if p_type else "Desconocido",
                "name_start_char": abs_name_start if abs_name_start !=-1 else None,
                "name_end_char": abs_name_end if abs_name_end != -1 else None
            })
        
        current_offset = segment_original_start_offset + len(segment) + 1 # Move past this segment and the comma

    return params_list


def parse_line(line: str) -> Dict[str, Any]:
    stripped_line = line.strip()
    
    # 1. Handle comments
    if stripped_line.startswith("//"):
        return {"type": "comment", "content": stripped_line[2:].strip()}

    # 2. Handle empty lines
    if not stripped_line:
        return {"type": "empty"}

    line_lower = stripped_line.lower()
    tokens = _extract_tokens(stripped_line)
    first_token_lower = tokens[0].lower() if tokens else ""

    # 3. Block End Keywords (simple cases)
    if first_token_lower in BLOCK_END_KEYWORDS:
        return {"type": "block_end", "keyword": first_token_lower}

    # 4. Special case: "hasta que" for Repetir
    if line_lower.startswith("hasta que "):
        condition = stripped_line[len("hasta que "):].strip().rstrip(';')
        return {"type": "block_end", "keyword": "hasta que", "condition": condition}
    
    # 5. Block Start and Declaration Keywords
    if first_token_lower in BLOCK_START_KEYWORDS or first_token_lower in DECLARATION_KEYWORDS:
        keyword = first_token_lower
        remaining_line = stripped_line[len(tokens[0]):].strip()

        if keyword == "proceso" or keyword == "algoritmo":
            # Proceso MiProceso
            # Algoritmo MiAlgoritmo
            name_match = re.match(r"([\w_]+)", remaining_line)
            if name_match:
                name = name_match.group(1)
                name_start = name_match.start(1) + (len(stripped_line) - len(remaining_line)) # Adjust to full stripped_line
                name_end = name_match.end(1) + (len(stripped_line) - len(remaining_line))
                return {"type": "block_start", "keyword": keyword, "name": name, 
                        "name_start_char": name_start, "name_end_char": name_end}
            return {"type": "block_start", "keyword": keyword, "name": "SinNombre"}

        if keyword == "subproceso" or keyword == "subalgoritmo":
            # SubProceso [retorno <-] NombreSubAlgoritmo ( [argumentos] )
            name_pattern = r"(?:[\w_]+\s*<-\s*)?([\w_]+)\s*\("
            match_name_part = re.search(name_pattern, stripped_line, re.IGNORECASE) # Search in full line to get offsets
            
            if match_name_part:
                name = match_name_part.group(1) # The actual name
                name_start_char = match_name_part.start(1)
                name_end_char = match_name_part.end(1)

                # Full match for params string
                full_match = re.match(r"([\w\s,]*?<-)?\s*[\w_]+\s*\((.*?)\)", remaining_line, re.IGNORECASE)
                if full_match:
                    return_part, params_str = full_match.groups() if len(full_match.groups()) == 2 else (None, full_match.group(1) if full_match.group(1) else "") # Adjust based on groups
                    if '<-' not in stripped_line : # fix for when return_part is actually the params_str due to optional group
                         params_str = return_part if return_part and '(' not in return_part else params_str
                         return_part = None
                    
                    return_var = None
                    if return_part:
                        return_var = return_part.replace("<-", "").strip()
                    
                    params = _parse_parameters(params_str)
                    return {"type": "block_start", "keyword": keyword, "name": name, 
                            "name_start_char": name_start_char, "name_end_char": name_end_char,
                            "params": params, "return_var": return_var}

            # Fallback if complex regex fails (e.g. "SubProceso nombre_sub" without parenthesis)
            simple_name_match = re.match(r"([\w_]+)", remaining_line)
            name = simple_name_match.group(1) if simple_name_match else "SinNombre"
            name_start = simple_name_match.start(1) + (len(stripped_line) - len(remaining_line)) if simple_name_match else None
            name_end = simple_name_match.end(1) + (len(stripped_line) - len(remaining_line)) if simple_name_match else None
            return {"type": "block_start", "keyword": keyword, "name": name, 
                    "name_start_char": name_start, "name_end_char": name_end, "params": []}


        if keyword == "funcion":
            # Funcion [var_retorno <-] NombreFuncion ( [argumentos] )
            name_pattern = r"(?:[\w_]+\s*<-\s*)?([\w_]+)\s*\("
            match_name_part = re.search(name_pattern, stripped_line, re.IGNORECASE)

            if match_name_part:
                name = match_name_part.group(1)
                name_start_char = match_name_part.start(1)
                name_end_char = match_name_part.end(1)

                full_match = re.match(r"(([\w_]+)\s*<-)?\s*[\w_]+\s*\((.*?)\)", remaining_line, re.IGNORECASE)
                if full_match:
                    _, return_var, params_str = full_match.groups() # name is already from match_name_part
                    params = _parse_parameters(params_str)
                    actual_return_var = return_var if return_var else name # If "var <-" is not used, func name is implicit return
                    return {"type": "block_start", "keyword": keyword, "name": name,
                            "name_start_char": name_start_char, "name_end_char": name_end_char,
                            "return_var": actual_return_var, "params": params}
            
            simple_name_match = re.match(r"([\w_]+)", remaining_line) # Fallback for "Funcion MiFunc"
            name = simple_name_match.group(1) if simple_name_match else "SinNombre"
            name_start = simple_name_match.start(1) + (len(stripped_line) - len(remaining_line)) if simple_name_match else None
            name_end = simple_name_match.end(1) + (len(stripped_line) - len(remaining_line)) if simple_name_match else None
            return {"type": "block_start", "keyword": keyword, "name": name, 
                    "name_start_char": name_start, "name_end_char": name_end,
                    "return_var": name, "params": []}


        if keyword == "si":
            # Si condicion Entonces
            match = re.match(r"(.*?)entonces", remaining_line, re.IGNORECASE)
            condition = match.group(1).strip() if match else remaining_line
            return {"type": "block_start", "keyword": keyword, "condition": condition}

        if keyword == "mientras":
            # Mientras condicion Hacer
            match = re.match(r"(.*?)hacer", remaining_line, re.IGNORECASE)
            condition = match.group(1).strip() if match else remaining_line
            return {"type": "block_start", "keyword": keyword, "condition": condition}

        if keyword == "para":
            # Para var <- inicial Hasta final Con Paso paso Hacer
            match = re.match(r"([\w_]+)\s*<-\s*(.*?)\s+hasta\s+(.*?)(?:\s+con\s+paso\s+(.*?))?\s+hacer", remaining_line, re.IGNORECASE)
            if match:
                var, inicial, final, paso = match.groups()
                return {"type": "block_start", "keyword": keyword, "variable": var, 
                        "initial": inicial, "final": final, "step": paso if paso else "1"}
            return {"type": "block_start", "keyword": keyword, "details": remaining_line} # Fallback

        if keyword == "segun":
            # Segun variable Hacer
            match = re.match(r"(.*?)hacer", remaining_line, re.IGNORECASE)
            variable = match.group(1).strip() if match else remaining_line
            return {"type": "block_start", "keyword": keyword, "variable": variable}

        if keyword == "repetir":
            return {"type": "block_start", "keyword": keyword}

        if keyword == "definir":
            # Definir var1, var2 Como Tipo
            # For simplicity, this focuses on the first variable if multiple are on one line for position.
            # A more robust solution would parse each var name and its position.
            match_def = re.match(r"([\w_,\s]+?)como\s+(.+)", remaining_line, re.IGNORECASE)
            if match_def:
                vars_str, var_type = match_def.groups()
                variables = [v.strip() for v in vars_str.split(',')]
                
                # Try to get pos for the first variable
                first_var_name = variables[0] if variables else ""
                name_start, name_end = None, None
                
                # Search for the first variable name within the vars_str part of remaining_line
                # This needs to be relative to `stripped_line`
                # `len(stripped_line) - len(remaining_line)` is the offset of `remaining_line` in `stripped_line`
                # `match_def.start(1)` is the start of `vars_str` within `remaining_line`.
                vars_str_abs_start = (len(stripped_line) - len(remaining_line)) + match_def.start(1)

                var_name_match_in_vars_str = re.search(r"([\w_]+)", vars_str) # find first word
                if var_name_match_in_vars_str and var_name_match_in_vars_str.group(1) == first_var_name :
                    name_start = vars_str_abs_start + var_name_match_in_vars_str.start(1)
                    name_end = vars_str_abs_start + var_name_match_in_vars_str.end(1)

                return {"type": "declaration", "keyword": keyword, 
                        "variables": variables, "var_type": var_type.strip().rstrip(';'),
                        "name_start_char": name_start, "name_end_char": name_end, # For the first variable
                        "first_var_name": first_var_name
                       }
            return {"type": "declaration", "keyword": keyword, "details": remaining_line}

        if keyword == "dimension":
            # Dimension nombre_array[tam1, tam2, ...]
            match_dim = re.match(r"([\w_]+)\s*\[(.*?)\]", remaining_line)
            if match_dim:
                name, dims_str = match_dim.groups()
                name_start = (len(stripped_line) - len(remaining_line)) + match_dim.start(1)
                name_end = (len(stripped_line) - len(remaining_line)) + match_dim.end(1)
                dimensions = [d.strip() for d in dims_str.split(',')]
                return {"type": "declaration", "keyword": keyword, "name": name, 
                        "name_start_char": name_start, "name_end_char": name_end,
                        "dimensions": dimensions}
            return {"type": "declaration", "keyword": keyword, "details": remaining_line}

    # Handle mid-block structural keywords if not caught above (e.g. "Caso X:", "Sino")
    if first_token_lower in STRUCTURAL_KEYWORDS:
         # Basic identification, could be refined
        details = {"keyword": first_token_lower}
        if len(tokens) > 1:
             # Captures "X" in "Caso X:" or "X > Y" in "Caso X > Y:"
            value = stripped_line[len(tokens[0]):].strip().rstrip(':')
            details["value"] = value
        return {"type": "structural", **details}


    # 6. Default to simple code
    return {"type": "code", "content": stripped_line}


def analyze_document_context(document_content: str, cursor_line_num: int) -> Dict[str, Any]:
    """
    Analyzes the PSeInt document content up to a specific line to determine
    the current block context and declared symbols.
    """
    open_blocks: List[BlockContext] = []
    symbols: List[Symbol] = []
    lines = document_content.splitlines()

    current_proceso_or_function_scope_start_line = 0

    for i, line_text in enumerate(lines):
        if i > cursor_line_num: # Only process up to the cursor line
            break 
        
        line_num = i + 1 # 1-indexed line numbers
        parsed_line = parse_line(line_text)
        line_type = parsed_line.get("type")
        keyword = parsed_line.get("keyword", "").lower()

        if line_type == "block_start":
            block_name = parsed_line.get("name")
            block_details = parsed_line # Store all parsed details
            
            # For scoping symbols, track the start of Proceso/Funcion/SubProceso
            if keyword in {"proceso", "algoritmo", "funcion", "subproceso", "subalgoritmo"}:
                current_proceso_or_function_scope_start_line = line_num
                # Add functions/subprocesos/proceso/algoritmo as symbols
                symbol_type = "function" if keyword == "funcion" else \
                              "subproceso" if keyword in {"subproceso", "subalgoritmo"} else \
                              "proceso" # for Proceso/Algoritmo
                
                name_s = parsed_line.get("name_start_char")
                name_e = parsed_line.get("name_end_char")

                symbols.append(Symbol(name=block_name if block_name else "Anon" + str(line_num),
                                      symbol_type=symbol_type,
                                      declaration_line=line_num,
                                      scope_start_line=line_num, 
                                      name_start_char=name_s,
                                      name_end_char=name_e,
                                      details=block_details))
            
            open_blocks.append(BlockContext(keyword, line_num, block_name, block_details))

        elif line_type == "block_end":
            if open_blocks:
                closed_block = open_blocks.pop()
                # Update scope_end_line for corresponding function/subproceso symbol
                if closed_block.keyword in {"proceso", "algoritmo", "funcion", "subproceso", "subalgoritmo"}:
                    for sym in reversed(symbols):
                        if sym.name == closed_block.name and sym.declaration_line == closed_block.start_line:
                            sym.scope_end_line = line_num
                            break
                if closed_block.keyword == "repetir" and keyword != "hasta que":
                    # Repetir doesn't match "hasta que" directly, put it back if not "hasta que"
                    # This can happen if a FinMientras or other Fin ends the loop prematurely
                    open_blocks.append(closed_block) 
                
            # Special handling for "hasta que" which is the true end for "repetir"
            if keyword == "hasta que" and open_blocks and open_blocks[-1].keyword == "repetir":
                 closed_block = open_blocks.pop()
                 # No specific symbol for Repetir block itself, but inner symbols would be scoped.


        elif line_type == "declaration":
            var_names = parsed_line.get("variables", [])
            var_type = parsed_line.get("var_type")
            array_name = parsed_line.get("name") # For Dimension

            scope_start = current_proceso_or_function_scope_start_line if current_proceso_or_function_scope_start_line > 0 else 1
            if open_blocks: # Prefer inner-most block start if available
                scope_start = open_blocks[-1].start_line


            if keyword == "definir" and var_names: # This handles multiple variables defined with one Definir
                # The name_start_char and name_end_char from parsed_line are for the *first* variable.
                # For subsequent variables on the same line, these positions would be incorrect.
                # This is a known limitation for multi-variable Definir lines.
                first_var_name_in_def = parsed_line.get("first_var_name")
                
                for var_name in var_names:
                    s_name_start, s_name_end = None, None
                    if var_name == first_var_name_in_def: # Only use stored pos for the first variable
                        s_name_start = parsed_line.get("name_start_char")
                        s_name_end = parsed_line.get("name_end_char")
                    # Else, s_name_start/end remain None for other variables on the same line.

                    symbols.append(Symbol(name=var_name, symbol_type="variable",
                                          declaration_line=line_num,
                                          scope_start_line=scope_start,
                                          name_start_char=s_name_start,
                                          name_end_char=s_name_end,
                                          details={"var_type": var_type}))
            elif keyword == "dimension" and array_name:
                s_name_start = parsed_line.get("name_start_char")
                s_name_end = parsed_line.get("name_end_char")
                symbols.append(Symbol(name=array_name, symbol_type="array",
                                      declaration_line=line_num,
                                      scope_start_line=scope_start,
                                      name_start_char=s_name_start,
                                      name_end_char=s_name_end,
                                      details={"dimensions": parsed_line.get("dimensions")}))
    
    # Set scope_end_line for symbols still open at cursor_line to None or cursor_line_num for context
    for sym in symbols:
        if sym.scope_end_line is None and sym.declaration_line <= cursor_line_num:
            # If the symbol's block is still in open_blocks, its scope is ongoing
            # Otherwise, if its block is closed but symbol wasn't updated, it's an issue.
            # For simplicity here, if scope_end_line is None, it implies scope extends to end of file or current analysis point.
            pass


    return {
        "open_blocks": open_blocks,
        "symbols": symbols,
        "current_block": open_blocks[-1] if open_blocks else None,
        "cursor_line_parsed": parse_line(lines[cursor_line_num]) if cursor_line_num < len(lines) else {"type":"eof"}
    }

if __name__ == '__main__':
    # --- Test cases for parse_line ---
    test_lines = [
        "Proceso MiAlgoritmo",
        "  Si x > 5 Entonces",
        "  FinSi",
        "Definir contador Como Entero;",
        "Definir a, b, c Como Real",
        "Dimension matriz[10, 20]",
        "Funcion res = Suma(a, b)",
        "SubProceso Saludar(nombre Por Referencia Como Caracter)",
        "SubProceso res <- Calcular(n1 Como Entero, n2 Por Referencia)",
        "// Esto es un comentario",
        "    ",
        "Escribir 'Hola Mundo'",
        "Leer numero",
        "Mientras x < 10 Hacer",
        "FinMientras",
        "Para i <- 1 Hasta 10 Con Paso 1 Hacer",
        "FinPara",
        "Segun opcion Hacer",
        "  Caso 1:",
        "    Escribir 'Uno'",
        "  De Otro Modo:",
        "    Escribir 'Otro'",
        "FinSegun",
        "Repetir",
        "  Escribir 'Repitiendo'",
        "Hasta Que x > 100",
        "finalgoritmo", # Deliberately lowercase to test case insensitivity
        "Proceso ", # Test Proceso without name
        "SubProceso Saludo()", # Test SubProceso with empty params
        "Funcion MiFunc()", # Test Funcion with empty params
        "Definir mi_variable Como Logico",
        "Dimension mi_vector[5]"
    ]

    print("--- parse_line tests ---")
    for tl in test_lines:
        print(f"Input: \"{tl}\" -> Output: {parse_line(tl)}")
    print("-" * 30)

    # --- Test cases for analyze_document_context ---
    sample_code_1 = """
Proceso Principal
  Definir a Como Entero;
  a <- 10;
  Si a > 5 Entonces
    Definir b Como Caracter;
    b <- "Hola";
    Escribir b;
  FinSi
  
  Funcion resultado = CalcularSuma(n1 Como Entero, n2 Como Entero)
    Definir suma_interna Como Entero;
    suma_interna <- n1 + n2;
    resultado <- suma_interna;
  FinFuncion
  
  Escribir CalcularSuma(a, 5);
FinProceso
"""
    print("\n--- analyze_document_context test 1 (full) ---")
    analysis_1 = analyze_document_context(sample_code_1, len(sample_code_1.splitlines()) -1)
    print(f"Open Blocks: {analysis_1['open_blocks']}")
    print(f"Current Block: {analysis_1['current_block']}")
    print("Symbols:")
    for s in analysis_1['symbols']: print(f"  {s}")
    print("-" * 30)

    print("\n--- analyze_document_context test 2 (cursor inside Si) ---")
    analysis_2 = analyze_document_context(sample_code_1, 6) # Cursor after Escribir b;
    print(f"Open Blocks: {analysis_2['open_blocks']}")
    print(f"Current Block: {analysis_2['current_block']}")
    print(f"Cursor Line Parsed: {analysis_2['cursor_line_parsed']}")
    print("Symbols:")
    for s in analysis_2['symbols']: print(f"  {s}")
    print("-" * 30)
    
    print("\n--- analyze_document_context test 3 (cursor inside Funcion) ---")
    analysis_3 = analyze_document_context(sample_code_1, 12) # Cursor after resultado <- suma_interna;
    print(f"Open Blocks: {analysis_3['open_blocks']}")
    print(f"Current Block: {analysis_3['current_block']}")
    print(f"Cursor Line Parsed: {analysis_3['cursor_line_parsed']}")
    print("Symbols:")
    for s in analysis_3['symbols']: print(f"  {s}")
    print("-" * 30)

    sample_code_2 = """
Algoritmo TestRepetir
    Definir x Como Entero;
    x <- 0;
    Repetir
        Escribir "x=", x;
        x <- x + 1;
    Hasta Que x >= 5;
    
    Definir y Como Real; // Global after Repetir
FinAlgoritmo
"""
    print("\n--- analyze_document_context test 4 (Repetir-Hasta Que) ---")
    analysis_4 = analyze_document_context(sample_code_2, len(sample_code_2.splitlines()) -1)
    print(f"Open Blocks: {analysis_4['open_blocks']}")
    print("Symbols:")
    for s in analysis_4['symbols']: print(f"  {s}")
    print("-" * 30)

    print("\n--- analyze_document_context test 5 (cursor within Repetir) ---")
    analysis_5 = analyze_document_context(sample_code_2, 5) # Cursor after Escribir "x=", x;
    print(f"Open Blocks: {analysis_5['open_blocks']}")
    print(f"Current Block: {analysis_5['current_block']}")
    print("Symbols:")
    for s in analysis_5['symbols']: print(f"  {s}")
    print("-" * 30)

```
