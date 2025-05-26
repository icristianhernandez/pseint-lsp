import re
from typing import List, Tuple, Dict, Set, Optional, Union 

from lsprotocol.types import (
    Diagnostic,
    DiagnosticSeverity,
    Position,
    Range,
)

# --- PSeInt Keywords and Configuration ---
PSEINT_BLOCK_KEYWORDS: Dict[str, str] = {
    "proceso": "finproceso", "algoritmo": "finalgoritmo",
    "subproceso": "finsubproceso", "subalgoritmo": "finsubalgoritmo",
    "funcion": "finfuncion", "si": "finsi", "mientras": "finmientras",
    "para": "finpara", "segun": "finsegun", "repetir": "hastaque",
}
CONTEXTUAL_KEYWORDS: Dict[str, str] = {
    "sino": "si", "caso": "segun", "deotromodo": "segun", "hastaque": "repetir",
}
VALID_TYPES: Set[str] = {
    "entero", "real", "numero", "logico", "booleano", "caracter", "texto", "cadena"
}
NUMERIC_TYPES: Set[str] = {"entero", "real", "numero"}
STRING_TYPES: Set[str] = {"caracter", "texto", "cadena"}
LOGICAL_TYPES: Set[str] = {"logico", "booleano"}
ALL_OPERATORS: Set[str] = {
    "+", "-", "*", "/", "%", "mod", "^", "=", "<>", "<", ">", "<=", ">=",
    "&", "|", "y", "o", "no", "~", "<-"
}
ARITHMETIC_OPERATORS: Set[str] = {"+", "-", "*", "/", "%", "mod", "^"}
LOGICAL_OPERATORS: Set[str] = {"&", "|", "y", "o"} 
COMPARISON_OPERATORS: Set[str] = {"=", "<>", "<", ">", "<=", ">="}
KNOWN_KEYWORDS_FOR_LINE_START: Set[str] = set(PSEINT_BLOCK_KEYWORDS.keys()) | \
                                       set(PSEINT_BLOCK_KEYWORDS.values()) | \
                                       set(CONTEXTUAL_KEYWORDS.keys()) | \
                                       {"definir", "dimension", "leer", "escribir", "escribir sin saltar", "esperar", "borrar"} # Added "escribir sin saltar"

KEYWORD_ALIASES: Dict[str, str] = {
    "algoritmo": "Proceso", "subalgoritmo": "SubProceso", 
    "booleano": "Logico", 
    "texto": "Caracter", # Or Cadena, PSeInt is flexible
    "cadena": "Caracter"  # Or Texto
}


BUILTIN_FUNCTIONS_SIGNATURES: Dict[str, Dict[str, Any]] = {
    "longitud": {"min_args": 1, "max_args": 1, "param_spec": [(STRING_TYPES, "cadena")], "ret_type": "entero"},
    "mayusculas": {"min_args": 1, "max_args": 1, "param_spec": [(STRING_TYPES, "cadena")], "ret_type": "caracter"}, 
    "subcadena": {"min_args": 3, "max_args": 3, "param_spec": [(STRING_TYPES, "cadena"), (NUMERIC_TYPES, "entero"), (NUMERIC_TYPES, "entero")], "ret_type": "caracter"},
    "convertiranumero": {"min_args": 1, "max_args": 1, "param_spec": [(STRING_TYPES, "cadena")], "ret_type": "numero"}, 
    "convertiratexto": {"min_args": 1, "max_args": 1, "param_spec": [(VALID_TYPES, "cualquier")], "ret_type": "caracter"}, 
    "rc": {"min_args": 1, "max_args": 1, "param_spec": [(NUMERIC_TYPES, "numero")], "ret_type": "real"}, 
    "abs": {"min_args": 1, "max_args": 1, "param_spec": [(NUMERIC_TYPES, "numero")], "ret_type": "numero"}, 
    "ln": {"min_args": 1, "max_args": 1, "param_spec": [(NUMERIC_TYPES, "numero")], "ret_type": "real"}, 
    "exp": {"min_args": 1, "max_args": 1, "param_spec": [(NUMERIC_TYPES, "numero")], "ret_type": "real"}, 
    "sen": {"min_args": 1, "max_args": 1, "param_spec": [(NUMERIC_TYPES, "numero")], "ret_type": "real"}, 
    "cos": {"min_args": 1, "max_args": 1, "param_spec": [(NUMERIC_TYPES, "numero")], "ret_type": "real"}, 
    "tan": {"min_args": 1, "max_args": 1, "param_spec": [(NUMERIC_TYPES, "numero")], "ret_type": "real"}, 
    "trunc": {"min_args": 1, "max_args": 1, "param_spec": [(NUMERIC_TYPES, "numero")], "ret_type": "entero"},
    "redon": {"min_args": 1, "max_args": 1, "param_spec": [(NUMERIC_TYPES, "numero")], "ret_type": "entero"},
    "azar": {"min_args": 1, "max_args": 1, "param_spec": [(NUMERIC_TYPES, "entero")], "ret_type": "entero"}, 
    "aleatorio": {"min_args": 2, "max_args": 2, "param_spec": [(NUMERIC_TYPES, "entero"), (NUMERIC_TYPES, "entero")], "ret_type": "entero"},
}


# --- Symbol Table Structures ---
class ParamSymbol:
    def __init__(self, name: str, type: str, by_ref: bool = False):
        self.name = name; self.type = type; self.by_ref = by_ref

class Symbol:
    def __init__(self, name: str, type: str, line_defined: int, 
                 is_callable: bool = False, is_array: bool = False, 
                 is_proceso_algoritmo: bool = False, 
                 params: Optional[List[ParamSymbol]] = None, 
                 array_dims_str: Optional[List[str]] = None,
                 assigned_in_scope: bool = False, 
                 is_function_return_var: bool = False,
                 is_used: bool = False): # New field for P2
        self.name = name; self.type = type; self.line_defined = line_defined
        self.is_callable = is_callable; self.is_array = is_array
        self.is_proceso_algoritmo = is_proceso_algoritmo
        self.params = params or []; self.array_dims_str = array_dims_str or []
        self.assigned_in_scope = assigned_in_scope
        self.is_function_return_var = is_function_return_var
        self.is_used = is_used # For P2 "unused variable"


# --- Helper Functions ---
def _create_diagnostic(line_num: int, start_char: int, end_char: int, message: str, severity: DiagnosticSeverity = DiagnosticSeverity.Error) -> Diagnostic:
    start_char = max(0, start_char); end_char = max(start_char, end_char)
    return Diagnostic(range=Range(start=Position(line=line_num, character=start_char), end=Position(line=line_num, character=end_char)), message=message, severity=severity)

IDENTIFIER_REGEX_STR = r"[a-zA-Z_][a-zA-Z0-9_]*"
IDENTIFIER_REGEX = re.compile(fr"\b{IDENTIFIER_REGEX_STR}\b")

# --- Type Inference and Compatibility ---
# ... (All _infer_*, _is_*, _get_broader_*, _are_types_compatible_* functions remain unchanged from Turn 33) ...
def _infer_literal_type(literal_str: str) -> Optional[str]:
    literal_str = literal_str.lower()
    if literal_str in ("verdadero", "falso"): return "logico"
    if re.fullmatch(r"[0-9]+", literal_str): return "entero"
    if re.fullmatch(r"[0-9]+\.[0-9]+", literal_str): return "real"
    if (literal_str.startswith('"') and literal_str.endswith('"')) or \
       (literal_str.startswith("'") and literal_str.endswith("'")): return "caracter"
    return None
def _is_numeric_type(type_str: Optional[str]) -> bool: return type_str is not None and type_str.lower() in NUMERIC_TYPES
def _is_logical_type(type_str: Optional[str]) -> bool: return type_str is not None and type_str.lower() in LOGICAL_TYPES
def _is_string_type(type_str: Optional[str]) -> bool: return type_str is not None and type_str.lower() in STRING_TYPES
def _get_broader_numeric_type(type1: Optional[str], type2: Optional[str]) -> Optional[str]:
    if not _is_numeric_type(type1) or not _is_numeric_type(type2): return None
    if "real" in (type1, type2): return "real"; 
    if "numero" in (type1, type2): return "numero"; 
    return "entero"
def _are_types_compatible_for_assignment(target_type: str, source_type: Optional[str]) -> bool:
    if source_type is None: return False
    target_type_lower = target_type.lower(); source_type_lower = source_type.lower()
    if target_type_lower == source_type_lower: return True
    if target_type_lower == "numero": return _is_numeric_type(source_type_lower)
    if target_type_lower == "real": return source_type_lower == "entero"
    if target_type_lower in ("texto", "cadena") and source_type_lower == "caracter": return True
    if target_type_lower == "caracter" and source_type_lower in ("texto", "cadena"): return True
    if target_type_lower == "booleano" and source_type_lower == "logico": return True
    if target_type_lower == "logico" and source_type_lower == "booleano": return True
    return False
def _are_types_compatible_for_comparison(type1: Optional[str], type2: Optional[str]) -> bool:
    if type1 is None or type2 is None: return False
    type1_lower = type1.lower(); type2_lower = type2.lower()
    if _is_numeric_type(type1_lower) and _is_numeric_type(type2_lower): return True
    if _is_string_type(type1_lower) and _is_string_type(type2_lower): return True
    if _is_logical_type(type1_lower) and _is_logical_type(type2_lower): return True
    return type1_lower == type2_lower
def _extract_expression_parts(expr_str: str) -> List[str]:
    tokens = re.split(r'(\b(?:mod|y|o|no)\b|\s+|<-|=|<>|<|>|<=|>=|\+|-|\*|/|%|\^|&|\||~|\(|\)|,|\[|\])', expr_str, flags=re.IGNORECASE)
    return [t.strip() for t in tokens if t and t.strip()]
def _parse_arg_list_str(arg_list_str: str) -> List[str]:
    args = []; balance = 0; current_arg = ""
    for char in arg_list_str:
        if char == ',' and balance == 0: args.append(current_arg.strip()); current_arg = ""
        else:
            if char == '(': balance += 1
            elif char == ')': balance -= 1
            current_arg += char
    if current_arg: args.append(current_arg.strip())
    return [a for a in args if a]

def _mark_variable_used(var_name: str, symbol_table: Dict[str, Symbol]):
    var_name_lower = var_name.lower()
    if var_name_lower in symbol_table:
        sym = symbol_table[var_name_lower]
        if not sym.is_callable and not sym.is_array and not sym.is_proceso_algoritmo:
            # Update is_used flag. Since Symbol is a class, we can mutate it.
            sym.is_used = True


def _infer_expression_type(expr_str: str, symbol_table: Dict[str, Symbol], current_line_num: int, diagnostics: List[Diagnostic], original_line_text: str) -> Optional[str]:
    expr_str = expr_str.strip()
    literal_type = _infer_literal_type(expr_str)
    if literal_type: return literal_type
    
    if IDENTIFIER_REGEX.fullmatch(expr_str):
        sym = symbol_table.get(expr_str.lower())
        if sym:
            if not sym.is_callable and not sym.is_array and not sym.is_proceso_algoritmo:
                _mark_variable_used(sym.name, symbol_table) # Mark as used
                if not sym.assigned_in_scope and not sym.is_function_return_var:
                    var_start_char = original_line_text.lower().find(expr_str.lower())
                    diagnostics.append(_create_diagnostic(current_line_num, var_start_char, var_start_char + len(expr_str), f"Variable '{sym.name}' utilizada antes de ser asignada.", DiagnosticSeverity.Warning))
            return sym.type if not sym.is_callable and not sym.is_array else None
        return None

    call_match = re.match(fr"({IDENTIFIER_REGEX_STR})\s*\((.*?)\)", expr_str, re.IGNORECASE)
    if call_match:
        func_name_raw = call_match.group(1); func_name_lower = func_name_raw.lower(); args_str = call_match.group(2)
        _mark_variable_used(func_name_raw, symbol_table) # Mark function name as used
        if func_name_lower in BUILTIN_FUNCTIONS_SIGNATURES: sig = BUILTIN_FUNCTIONS_SIGNATURES[func_name_lower]; return sig["ret_type"]
        if func_name_lower in symbol_table and symbol_table[func_name_lower].is_callable: return symbol_table[func_name_lower].type
        return None 

    parts = _extract_expression_parts(expr_str)
    if len(parts) == 3: 
        op1_str, operator, op2_str = parts[0], parts[1], parts[2]; operator = operator.lower()
        type1 = _infer_expression_type(op1_str, symbol_table, current_line_num, diagnostics, original_line_text)
        type2 = _infer_expression_type(op2_str, symbol_table, current_line_num, diagnostics, original_line_text)
        if operator in ARITHMETIC_OPERATORS: return "caracter" if operator == "+" and (_is_string_type(type1) and _is_string_type(type2)) else _get_broader_numeric_type(type1, type2)
        if operator in LOGICAL_OPERATORS: return "logico" if _is_logical_type(type1) and _is_logical_type(type2) else None
        if operator in COMPARISON_OPERATORS: return "logico" 
    if len(parts) == 2 and parts[0].lower() in ("no", "~"):
        op_str = parts[1]; op_type = _infer_expression_type(op_str, symbol_table, current_line_num, diagnostics, original_line_text)
        return "logico" if _is_logical_type(op_type) else None
    return None


# --- Main Diagnostic Function ---
class FunctionScopeInfo(NamedTuple): # Keep as NamedTuple for immutability on stack
    name: str
    return_var_name: Optional[str]
    return_var_assigned: bool
    line_defined: int
    # For P2 Empty Block: Store start line of actual content for this function
    content_start_line: int = -1 

def get_diagnostics(code: str) -> List[Diagnostic]:
    diagnostics: List[Diagnostic] = []
    lines = code.splitlines()
    block_stack: List[Tuple[str, int, int, str]] = [] # (keyword, line_num, start_char, original_line_text)
    symbol_table: Dict[str, Symbol] = {}
    current_segun_var_info: Optional[Tuple[str, int, str]] = None
    main_proceso_algoritmo_name: Optional[str] = None
    function_scope_stack: List[FunctionScopeInfo] = []


    for i, line_text in enumerate(lines):
        line_lower_stripped = line_text.strip().lower()
        line_stripped = line_text.strip()
        original_line_for_char_find = line_text 

        # P2: Malformed/Empty Comment Warning
        if line_stripped.startswith("//") and line_stripped[2:].strip() == "":
            diagnostics.append(_create_diagnostic(i, 0, len(line_stripped), "Comentario vacío.", DiagnosticSeverity.Warning))

        # ... (Invalid Character Check from Turn 25) ...

        is_definition_line = False 
        
        # --- Definitions: Proceso/Algoritmo, Funcion/SubProceso, Dimension, Definir ---
        # (Adapted logic from Turn 25/29/33)
        # ...
        subproceso_match = re.match(r"(subproceso|subalgoritmo)\s+(" + IDENTIFIER_REGEX_STR + r")\s*(\()?\s*(.*?)\s*(\))?", line_lower_stripped, re.IGNORECASE)
        funcion_match = re.match(r"funcion\s+(" + IDENTIFIER_REGEX_STR + r")\s*=\s*(" + IDENTIFIER_REGEX_STR + r")\s*(\()?\s*(.*?)\s*(\))?", line_lower_stripped, re.IGNORECASE)
        
        if funcion_match: 
            is_definition_line = True
            ret_var_name_raw = funcion_match.group(1); func_name_raw = funcion_match.group(2); func_name_lower = func_name_raw.lower()
            # ... (Full parsing logic for Funcion from Turn 25, creating Symbol, adding to symbol_table) ...
            # Mark params as used & assigned
            # Add return_var to symbol_table for this scope, is_function_return_var=True, assigned_in_scope=False, is_used=False
            # ...
            # Push to function_scope_stack
            # function_scope_stack.append(FunctionScopeInfo(name=func_name_lower, return_var_name=ret_var_name_raw.lower(), return_var_assigned=False, line_defined=i, content_start_line=i+1))
            # ... (Alias check for 'funcion' if any)
            pass # Placeholder for brevity, assume previous logic is integrated
        elif subproceso_match: # Handle SubProceso
            is_definition_line = True
            # ... (Full parsing logic for SubProceso from Turn 25, creating Symbol, adding to symbol_table) ...
            # Mark params as used & assigned
            # ...
            # Push to function_scope_stack (with return_var_name=None)
            # function_scope_stack.append(FunctionScopeInfo(name=func_name_lower, return_var_name=None, return_var_assigned=False, line_defined=i, content_start_line=i+1))
            # ... (Alias check for 'subproceso'/'subalgoritmo')
            pass # Placeholder for brevity

        # ... (Dimension and Definir parsing from Turn 33, including alias checks for types in Definir) ...
        # For Definir: mark symbol with is_used=False initially.
        # For Dimension: mark symbol with is_used=False initially (unless PSeInt considers dimensioning as usage).
        # For Parameters in Func/SubProc: mark is_used=True.
        # For Para loop var: mark is_used=True.


        # --- Block Error Checks & Segun Variable Type & P2 Empty Block & P2 Missing Colon ---
        found_block_keyword_for_stack = False
        for open_keyword, close_keyword_val in PSEINT_BLOCK_KEYWORDS.items():
            if line_lower_stripped.startswith(open_keyword):
                found_block_keyword_for_stack = True; start_char_on_line = original_line_for_char_find.lower().find(open_keyword)
                # P2: Keyword Alias Warning
                if open_keyword in KEYWORD_ALIASES:
                    diagnostics.append(_create_diagnostic(i, start_char_on_line, start_char_on_line + len(open_keyword), f"Se recomienda usar '{KEYWORD_ALIASES[open_keyword]}' en lugar de '{open_keyword.capitalize()}' para consistencia.", DiagnosticSeverity.Warning))
                
                # ... (Proceso/Algoritmo name collision logic from Turn 25) ...
                block_stack.append((open_keyword, i, start_char_on_line, original_line_for_char_find)) # Store original line for empty block check
                # ... (Segun variable type check & missing intermediate keywords from Turn 29/33) ...
                break
        if found_block_keyword_for_stack: continue
        
        for open_keyword_for_closer, close_keyword_val in PSEINT_BLOCK_KEYWORDS.items():
            is_hasta_que_line = open_keyword_for_closer == "repetir" and line_lower_stripped.startswith(close_keyword_val) # 'hastaque' is part of the line
            actual_close_keyword_on_line = close_keyword_val if not is_hasta_que_line else line_lower_stripped.split()[0] # Use the actual keyword like "hastaque"

            if line_lower_stripped.startswith(actual_close_keyword_on_line) or \
               (open_keyword_for_closer == "repetir" and close_keyword_val in line_lower_stripped and line_lower_stripped.startswith("hasta")): # for "Hasta Que"
                found_block_keyword_for_stack = True; start_char_on_line = original_line_for_char_find.lower().find(actual_close_keyword_on_line)
                
                if block_stack: # Check for empty block before popping
                    block_type, open_line_num, _, open_line_text = block_stack[-1]
                    if block_type == open_keyword_for_closer : # Matched block
                        is_empty = True
                        if i > open_line_num + 1: # More than one line apart
                            for k_line_idx in range(open_line_num + 1, i):
                                if lines[k_line_idx].strip() != "" and not lines[k_line_idx].strip().startswith("//"):
                                    is_empty = False; break
                        elif i == open_line_num + 1: # Consecutive lines
                            is_empty = True 
                        else: # Same line, or error - should not happen if block open/close are on different lines
                            is_empty = False 

                        if is_empty:
                             open_kw_start_char = open_line_text.lower().find(block_type)
                             diagnostics.append(_create_diagnostic(open_line_num, open_kw_start_char, open_kw_start_char + len(block_type), f"Bloque '{block_type.capitalize()}' vacío. Se esperaba contenido.", DiagnosticSeverity.Warning))
                # ... (Rest of closing keyword logic from Turn 25, including FinFuncion return value check) ...
                break
        if found_block_keyword_for_stack: continue

        for contextual_keyword, required_parent in CONTEXTUAL_KEYWORDS.items():
            if line_lower_stripped.startswith(contextual_keyword):
                # ... (Contextual keyword logic from Turn 25) ...
                # P2: Missing Colon for Caso/DeOtroModo
                if contextual_keyword == "caso":
                    match_caso_colon = re.match(r"caso\s+.+?(\s*:)?", line_lower_stripped, re.IGNORECASE)
                    if match_caso_colon and not match_caso_colon.group(1): # No colon found
                        kw_len = len("caso")
                        val_part_match = re.match(r"caso\s+(.+)", line_lower_stripped, re.IGNORECASE)
                        val_len = len(val_part_match.group(1).rstrip()) if val_part_match else 0
                        diag_end_char = original_line_for_char_find.lower().find("caso") + kw_len + val_len
                        diagnostics.append(_create_diagnostic(i, diag_end_char -1 , diag_end_char, "Se esperaba ':' después del valor en 'Caso'.", DiagnosticSeverity.Warning))
                elif contextual_keyword == "deotromodo":
                    if not line_lower_stripped.endswith(":"):
                        kw_len = len("deotromodo")
                        diag_end_char = original_line_for_char_find.lower().find("deotromodo") + kw_len
                        diagnostics.append(_create_diagnostic(i, diag_end_char -1, diag_end_char, "Se esperaba ':' después de 'De Otro Modo'.", DiagnosticSeverity.Warning))
                break
        
        # --- P2: Empty Escribir / Escribir Sin Saltar ---
        if line_lower_stripped.startswith("escribir"):
            command = "escribir sin saltar" if line_lower_stripped.startswith("escribir sin saltar") else "escribir"
            args_part = line_stripped[len(command):].strip()
            if not args_part or args_part == ";":
                cmd_start_char = original_line_for_char_find.lower().find(command)
                diagnostics.append(_create_diagnostic(i, cmd_start_char, cmd_start_char + len(command), f"Comando '{command.capitalize()}' requiere una o más expresiones.", DiagnosticSeverity.Warning))


        # --- Assignment, Expression, Call Checks (from Turn 33, including P1s) ---
        # ... (Full logic, ensure _infer_expression_type calls _mark_variable_used) ...
        if not (is_definition_line or found_block_keyword_for_stack or any(line_lower_stripped.startswith(kw) for kw in KNOWN_KEYWORDS_FOR_LINE_START)):
            # ... (Assignment, Operator, Type, Call, Array Index checks)
            pass # Placeholder for brevity

    # --- Final Checks (after all lines processed) ---
    # P2: Unused Variable Warning
    for sym_name, sym_obj in symbol_table.items():
        if not sym_obj.is_used and \
           not sym_obj.is_callable and \
           not sym_obj.is_array and \
           not sym_obj.is_proceso_algoritmo and \
           not sym_obj.is_function_return_var and \
           not any(p.name.lower() == sym_name for func_s in symbol_table.values() if func_s.params for p in func_s.params) and \
           not any(block_kw == "para" and sym_name == block_line.split()[1].lower() for block_kw, _, _, block_line in block_stack): # crude check for active para loops, better to mark para vars used
            diagnostics.append(_create_diagnostic(sym_obj.line_defined, 
                                                  0, len(sym_obj.name), # Approximate range on definition line
                                                  f"Variable '{sym_obj.name}' definida pero no utilizada.", 
                                                  DiagnosticSeverity.Warning))

    # ... (Final Block Checks from Turn 25) ...
    
    return diagnostics
```
