from typing import List, Optional, Set
from lsprotocol.types import CompletionItem, CompletionItemKind, InsertTextFormat

# Attempt to import from local pseint_parser, fallback for different execution contexts
try:
    from .pseint_parser import analyze_document_context, Symbol, BlockContext
except ImportError:
    from pseint_parser import analyze_document_context, Symbol, BlockContext


PSEINT_KEYWORDS_DEFINITIONS = {
    # Main program structures
    "Proceso": {"kind": CompletionItemKind.Keyword, "doc": "Inicia un bloque de Proceso principal."},
    "FinProceso": {"kind": CompletionItemKind.Keyword, "doc": "Finaliza un bloque de Proceso."},
    "Algoritmo": {"kind": CompletionItemKind.Keyword, "doc": "Inicia un bloque de Algoritmo principal (sinónimo de Proceso)."},
    "FinAlgoritmo": {"kind": CompletionItemKind.Keyword, "doc": "Finaliza un bloque de Algoritmo."},

    # Subprogram structures
    "SubProceso": {"kind": CompletionItemKind.Keyword, "doc": "Define un subproceso (procedimiento)."},
    "FinSubProceso": {"kind": CompletionItemKind.Keyword, "doc": "Finaliza un subproceso."},
    "SubAlgoritmo": {"kind": CompletionItemKind.Keyword, "doc": "Define un subalgoritmo (sinónimo de SubProceso)."},
    "FinSubAlgoritmo": {"kind": CompletionItemKind.Keyword, "doc": "Finaliza un subalgoritmo."},
    "Funcion": {"kind": CompletionItemKind.Keyword, "doc": "Define una función que retorna un valor."},
    "FinFuncion": {"kind": CompletionItemKind.Keyword, "doc": "Finaliza una función."},

    # Declarations
    "Definir": {"kind": CompletionItemKind.Keyword, "doc": "Declara una o más variables."},
    "Como": {"kind": CompletionItemKind.Keyword, "doc": "Especifica el tipo de una variable en una declaración."},
    "Dimension": {"kind": CompletionItemKind.Keyword, "doc": "Declara un arreglo (vector o matriz)."},

    # Basic I/O
    "Leer": {"kind": CompletionItemKind.Keyword, "doc": "Lee datos de la entrada estándar."},
    "Escribir": {"kind": CompletionItemKind.Keyword, "doc": "Muestra datos en la salida estándar."},
    "Escribir Sin Saltar": {"kind": CompletionItemKind.Keyword, "doc": "Muestra datos sin avanzar a la siguiente línea."},

    # Conditional structure
    "Si": {"kind": CompletionItemKind.Keyword, "doc": "Inicia una estructura condicional."},
    "Entonces": {"kind": CompletionItemKind.Keyword, "doc": "Parte de la estructura Si-Entonces."},
    "Sino": {"kind": CompletionItemKind.Keyword, "doc": "Parte de la estructura Si-Entonces-Sino."},
    "FinSi": {"kind": CompletionItemKind.Keyword, "doc": "Finaliza una estructura Si."},

    # Loop structures
    "Mientras": {"kind": CompletionItemKind.Keyword, "doc": "Inicia un bucle Mientras-Hacer."},
    "Hacer": {"kind": CompletionItemKind.Keyword, "doc": "Parte de las estructuras Mientras y Segun."},
    "FinMientras": {"kind": CompletionItemKind.Keyword, "doc": "Finaliza un bucle Mientras."},
    "Para": {"kind": CompletionItemKind.Keyword, "doc": "Inicia un bucle Para."},
    "Hasta": {"kind": CompletionItemKind.Keyword, "doc": "Parte de la estructura Para."},
    "Con Paso": {"kind": CompletionItemKind.Keyword, "doc": "Parte de la estructura Para (opcional)."},
    "FinPara": {"kind": CompletionItemKind.Keyword, "doc": "Finaliza un bucle Para."},
    "Repetir": {"kind": CompletionItemKind.Keyword, "doc": "Inicia un bucle Repetir-Hasta Que."},
    "Hasta Que": {"kind": CompletionItemKind.Keyword, "doc": "Finaliza un bucle Repetir, especificando la condición."},

    # Switch structure
    "Segun": {"kind": CompletionItemKind.Keyword, "doc": "Inicia una estructura de selección múltiple."},
    "Caso": {"kind": CompletionItemKind.Keyword, "doc": "Define un caso dentro de una estructura Segun."},
    "De Otro Modo": {"kind": CompletionItemKind.Keyword, "doc": "Define el caso por defecto en Segun."},
    "FinSegun": {"kind": CompletionItemKind.Keyword, "doc": "Finaliza una estructura Segun."},

    # Operators and parameters (often used as keywords)
    "MOD": {"kind": CompletionItemKind.Operator, "doc": "Operador módulo."},
    "Por Referencia": {"kind": CompletionItemKind.Keyword, "doc": "Especifica paso de parámetros por referencia."},
    "Por Valor": {"kind": CompletionItemKind.Keyword, "doc": "Especifica paso de parámetros por valor (generalmente implícito)."},

    # Data types
    "Entero": {"kind": CompletionItemKind.TypeParameter, "doc": "Tipo de dato para números enteros."},
    "Real": {"kind": CompletionItemKind.TypeParameter, "doc": "Tipo de dato para números reales."},
    "Numero": {"kind": CompletionItemKind.TypeParameter, "doc": "Tipo de dato numérico (abarca Entero y Real)."},
    "Logico": {"kind": CompletionItemKind.TypeParameter, "doc": "Tipo de dato para valores booleanos (Verdadero/Falso)."},
    "Booleano": {"kind": CompletionItemKind.TypeParameter, "doc": "Sinónimo de Logico."},
    "Caracter": {"kind": CompletionItemKind.TypeParameter, "doc": "Tipo de dato para un solo carácter."},
    "Texto": {"kind": CompletionItemKind.TypeParameter, "doc": "Tipo de dato para cadenas de caracteres (sinónimo de Cadena)."},
    "Cadena": {"kind": CompletionItemKind.TypeParameter, "doc": "Tipo de dato para cadenas de caracteres."},

    # Built-in functions / commands (subset)
    "BorrarPantalla": {"kind": CompletionItemKind.Keyword, "doc": "Limpia la pantalla de salida."},
    "EsperarTecla": {"kind": CompletionItemKind.Keyword, "doc": "Pausa la ejecución hasta que se presione una tecla."},
    "Esperar": {"kind": CompletionItemKind.Function, "doc": "Pausa la ejecución por un tiempo específico."},
    "Milisegundos": {"kind": CompletionItemKind.Keyword, "doc": "Unidad de tiempo en milisegundos (usado con Esperar)."},
    "Segundos": {"kind": CompletionItemKind.Keyword, "doc": "Unidad de tiempo en segundos (usado con Esperar)."},
    "Mayusculas": {"kind": CompletionItemKind.Function, "doc": "Convierte una cadena a mayúsculas."},
    "Minusculas": {"kind": CompletionItemKind.Function, "doc": "Convierte una cadena a minúsculas."},
    "Longitud": {"kind": CompletionItemKind.Function, "doc": "Obtiene la longitud de una cadena."},
    "Subcadena": {"kind": CompletionItemKind.Function, "doc": "Extrae una parte de una cadena."},
    "SubCadena": {"kind": CompletionItemKind.Function, "doc": "Extrae una parte de una cadena (sinónimo de Subcadena)."},
    "ConvertirANumero": {"kind": CompletionItemKind.Function, "doc": "Convierte una cadena a número."},
    "Aleatorio": {"kind": CompletionItemKind.Function, "doc": "Genera un número aleatorio."},
    "trunc": {"kind": CompletionItemKind.Function, "doc": "Trunca la parte decimal de un número."}
}

PSEINT_SNIPPETS_DEFINITIONS = [
    {
        "label": "Proceso",
        "insert_text": "Proceso ${1:nombre_proceso}\n\t${2:acciones}\nFinProceso",
        "documentation": "Bloque de Proceso principal."
    },
    {
        "label": "Algoritmo",
        "insert_text": "Algoritmo ${1:nombre_algoritmo}\n\t${2:acciones}\nFinAlgoritmo",
        "documentation": "Bloque de Algoritmo principal (sinónimo de Proceso)."
    },
    {
        "label": "SubProceso",
        "insert_text": "SubProceso ${1:nombre_subproceso}(${2:argumentos})\n\t${3:acciones}\nFinSubProceso",
        "documentation": "Define un subproceso (procedimiento)."
    },
    {
        "label": "SubAlgoritmo",
        "insert_text": "SubAlgoritmo ${1:nombre_subalgoritmo}(${2:argumentos})\n\t${3:acciones}\nFinSubAlgoritmo",
        "documentation": "Define un subalgoritmo (sinónimo de SubProceso)."
    },
    {
        "label": "Funcion",
        "insert_text": "Funcion ${1:variable_retorno} <- ${2:nombre_funcion}(${3:argumentos})\n\t${4:acciones}\nFinFuncion",
        "documentation": "Define una función que retorna un valor."
    },
    {
        "label": "Si (simple)",
        "insert_text": "Si ${1:condicion} Entonces\n\t${2:acciones}\nFinSi",
        "documentation": "Estructura condicional Si-Entonces."
    },
    {
        "label": "Si-Entonces-Sino",
        "insert_text": "Si ${1:condicion} Entonces\n\t${2:acciones}\nSino\n\t${3:acciones_sino}\nFinSi",
        "documentation": "Estructura condicional Si-Entonces-Sino."
    },
    {
        "label": "Mientras",
        "insert_text": "Mientras ${1:condicion} Hacer\n\t${2:acciones}\nFinMientras",
        "documentation": "Bucle Mientras-Hacer."
    },
    {
        "label": "Para",
        "insert_text": "Para ${1:variable} <- ${2:valor_inicial} Hasta ${3:valor_final} Con Paso ${4:paso} Hacer\n\t${5:acciones}\nFinPara",
        "documentation": "Bucle Para-Hasta-Con Paso-Hacer."
    },
    {
        "label": "Repetir",
        "insert_text": "Repetir\n\t${1:acciones}\nHasta Que ${2:condicion};",
        "documentation": "Bucle Repetir-Hasta Que."
    },
    {
        "label": "Segun",
        "insert_text": "Segun ${1:variable} Hacer\n\tCaso ${2:valor1}:\n\t\t${3:acciones_caso1}\n\tCaso ${4:valor2}:\n\t\t${5:acciones_caso2}\n\tDe Otro Modo:\n\t\t${6:acciones_otro_modo}\nFinSegun",
        "documentation": "Estructura de selección múltiple Segun-Caso-De Otro Modo."
    },
    {
        "label": "Definir",
        "insert_text": "Definir ${1:variable} Como ${2:Tipo};",
        "documentation": "Declaración de variables."
    },
    {
        "label": "Escribir",
        "insert_text": "Escribir ${1:expresion};",
        "documentation": "Muestra datos en la salida estándar."
    },
    {
        "label": "Leer",
        "insert_text": "Leer ${1:variable};",
        "documentation": "Lee datos de la entrada estándar."
    },
    {
        "label": "Dimension (vector)",
        "insert_text": "Dimension ${1:nombre_vector}[${2:tamaño}];",
        "documentation": "Define un arreglo (vector) de una dimensión."
    },
    # Dimension (matriz) was not in the original list, so it's not included here for aliasing.
]

# --- English Aliases for Snippets ---

SPANISH_TO_ENGLISH_LABELS = {
    "Proceso": "Process",
    "Algoritmo": "Algorithm",
    "SubProceso": "SubProcess",
    "SubAlgoritmo": "SubAlgorithm",
    "Funcion": "FunctionDef", # "Function" is a keyword kind, so use "FunctionDef" for snippet label
    "Si (simple)": "If",
    "Si-Entonces-Sino": "IfElse",
    "Mientras": "While",
    "Para": "For",
    "Repetir": "Repeat",
    "Segun": "Select", # Or "Switch"
    "Definir": "DefineSnippet", # "Definir" is a keyword, "DefineSnippet" for the snippet
    "Escribir": "WriteSnippet", # "Escribir" is a keyword, "WriteSnippet" for the snippet
    "Leer": "ReadSnippet",       # "Leer" is a keyword, "ReadSnippet" for the snippet
    "Dimension (vector)": "DimensionArray1D",
    # "Dimension (matriz)" would be "DimensionArray2D" if it existed
}

english_snippet_definitions = []
for snippet_def in PSEINT_SNIPPETS_DEFINITIONS:
    spanish_label = snippet_def["label"]
    if spanish_label in SPANISH_TO_ENGLISH_LABELS:
        english_label = SPANISH_TO_ENGLISH_LABELS[spanish_label]
        
        new_english_snippet = snippet_def.copy()
        new_english_snippet["label"] = english_label
        
        original_doc = snippet_def.get('documentation', '')
        new_english_snippet["documentation"] = f"(Alias for '{spanish_label}') {original_doc}"
        
        english_snippet_definitions.append(new_english_snippet)

PSEINT_SNIPPETS_DEFINITIONS.extend(english_snippet_definitions)


# Pre-generate CompletionItem objects for all keywords and snippets
# These will be filtered by get_contextual_completions

ALL_KEYWORD_COMPLETION_ITEMS: List[CompletionItem] = [
    CompletionItem(
        label=keyword,
        kind=details["kind"],
        insert_text_format=InsertTextFormat.PlainText,
        insert_text=keyword,
        documentation=details["doc"],
        # Additional properties to prevent function-like behavior for keywords
        detail="PSeInt Keyword" if details["kind"] == CompletionItemKind.Keyword else None
    ) for keyword, details in PSEINT_KEYWORDS_DEFINITIONS.items()
]

ALL_SNIPPET_COMPLETION_ITEMS: List[CompletionItem] = [
    CompletionItem(
        label=snippet_def["label"],
        kind=CompletionItemKind.Snippet, # All snippets are of kind SNIPPET
        insert_text=snippet_def["insert_text"],
        insert_text_format=InsertTextFormat.Snippet,
        documentation=snippet_def.get("documentation")
    ) for snippet_def in PSEINT_SNIPPETS_DEFINITIONS
]


def _is_symbol_in_scope(symbol: Symbol, cursor_line_num: int) -> bool:
    """Checks if a symbol is in scope at the cursor's line."""
    if symbol.declaration_line > cursor_line_num: # Defined after cursor
        return False
    
    # Global scope (e.g. functions, or variables in main Proceso if scope_start_line is Proceso start)
    # or symbols whose block scope is still active or just ended on this line.
    if symbol.scope_end_line is None or cursor_line_num <= symbol.scope_end_line:
        # Symbol's scope has not ended OR cursor is on the line where scope ends
        # Additionally, ensure cursor is within or at the start of the symbol's defined scope
        return cursor_line_num >= symbol.scope_start_line
    return False


def get_contextual_completions(document_content: str, cursor_line_num: int, cursor_char_num: int) -> List[CompletionItem]:
    context_analysis = analyze_document_context(document_content, cursor_line_num)
    open_blocks: List[BlockContext] = context_analysis.get('open_blocks', [])
    symbols: List[Symbol] = context_analysis.get('symbols', [])
    
    contextual_keywords: List[CompletionItem] = []
    symbol_completions: List[CompletionItem] = []
    contextual_snippets: List[CompletionItem] = []

    # --- Filter Keywords ---
    allowed_keyword_labels: Set[str] = set()
    current_block_keyword = open_blocks[-1].keyword if open_blocks else None
    
    base_keywords = {"Definir", "Leer", "Escribir", "Escribir Sin Saltar", "Dimension", 
                     "Si", "Mientras", "Para", "Segun", "Repetir"}
    program_level_keywords = {"Proceso", "Algoritmo", "Funcion", "SubProceso", "SubAlgoritmo"}

    if not open_blocks: # Top level, outside any main block
        allowed_keyword_labels.update(program_level_keywords)
    else:
        # Inside some block
        allowed_keyword_labels.update(base_keywords)
        # Keywords for specific data types or common commands
        allowed_keyword_labels.update({"Entero", "Real", "Numero", "Logico", "Booleano", "Caracter", "Texto", "Cadena", "Como"})
        allowed_keyword_labels.update({"BorrarPantalla", "EsperarTecla", "Esperar", "Milisegundos", "Segundos", "Mayusculas", "Minusculas", "Longitud", "Subcadena", "SubCadena", "ConvertirANumero", "Aleatorio", "trunc"})


        if current_block_keyword in {"proceso", "algoritmo"}:
            allowed_keyword_labels.update(program_level_keywords) # Can define functions within
            allowed_keyword_labels.add(f"Fin{current_block_keyword.capitalize()}")
        elif current_block_keyword == "si":
            allowed_keyword_labels.add("Sino")
            allowed_keyword_labels.add("FinSi")
            allowed_keyword_labels.add("Entonces") # Often re-typed
        elif current_block_keyword == "mientras":
            allowed_keyword_labels.add("FinMientras")
            allowed_keyword_labels.add("Hacer") # Often re-typed
        elif current_block_keyword == "para":
            allowed_keyword_labels.add("FinPara")
            allowed_keyword_labels.add("Hasta")
            allowed_keyword_labels.add("Con Paso")
            allowed_keyword_labels.add("Hacer")
        elif current_block_keyword == "segun":
            allowed_keyword_labels.add("Caso")
            allowed_keyword_labels.add("De Otro Modo")
            allowed_keyword_labels.add("FinSegun")
            allowed_keyword_labels.add("Hacer")
        elif current_block_keyword == "repetir":
            allowed_keyword_labels.add("Hasta Que")
        elif current_block_keyword == "funcion":
            allowed_keyword_labels.add("FinFuncion")
        elif current_block_keyword in {"subproceso", "subalgoritmo"}:
            allowed_keyword_labels.add(f"Fin{current_block_keyword.capitalize()}")

    # Filter from all predefined keyword items
    for item in ALL_KEYWORD_COMPLETION_ITEMS:
        if item.label in allowed_keyword_labels:
            contextual_keywords.append(item)

    # --- Suggest User-Defined Symbols ---
    for sym in symbols:
        if _is_symbol_in_scope(sym, cursor_line_num):
            kind = CompletionItemKind.Variable
            detail = f"Tipo: {sym.details.get('var_type', 'Desconocido')}"
            if sym.symbol_type == "array":
                dims = sym.details.get('dimensions', [])
                detail = f"Arreglo: {sym.details.get('var_type', '')}[{', '.join(dims)}]"
            elif sym.symbol_type == "function" or sym.symbol_type == "subproceso":
                kind = CompletionItemKind.Function
                params_list = sym.details.get('params', [])
                param_names = [p.get('name', 'arg') for p in params_list]
                param_str = ", ".join(param_names)
                detail = f"{sym.symbol_type.capitalize()} ({param_str})"
                if sym.details.get('return_var') and sym.symbol_type == "function":
                    detail += f" -> {sym.details['return_var']}"


            symbol_completions.append(CompletionItem(
                label=sym.name,
                kind=kind,
                insert_text=sym.name,
                insert_text_format=InsertTextFormat.PlainText,
                detail=detail,
                documentation=f"Declarado en línea: {sym.declaration_line}"
            ))
            
    # --- Filter Snippets (Refined) ---
    filtered_snippets: List[CompletionItem] = []
    has_main_block = any(b.keyword in {"proceso", "algoritmo"} for b in open_blocks)

    # Labels of snippets that define a new block of a certain type.
    # Used to prevent suggesting the same block type snippet when already inside one.
    block_defining_snippet_labels_map = {
        "si": ["Si (simple)", "Si-Entonces-Sino"],
        "mientras": ["Mientras"],
        "para": ["Para"],
        "segun": ["Segun"],
        "repetir": ["Repetir"],
        "funcion": ["Funcion"],
        "subproceso": ["SubProceso"],
        "subalgoritmo": ["SubAlgoritmo"],
        # Proceso/Algoritmo are handled by has_main_block check primarily
    }
    
    # Snippets that are general statements/declarations, usually not for top-level outside Proceso/Algoritmo
    general_statement_snippet_labels = {
        "Definir", "Escribir", "Leer", 
        "Dimension (vector)", "Dimension (matriz)" # Specific Dimension snippets
    }

    for snippet_item in ALL_SNIPPET_COMPLETION_ITEMS:
        allow_snippet = True

        # Rule 1: Exclude Proceso/Algoritmo snippets if a main block (Proceso/Algoritmo) is already open.
        if has_main_block and snippet_item.label in {"Proceso", "Algoritmo"}:
            allow_snippet = False
        
        # Rule 2: Exclude snippet for the current block type if we are already inside such a block.
        # This prevents suggesting, e.g., a "Si (simple)" snippet when the cursor is already inside a Si block.
        if current_block_keyword and current_block_keyword in block_defining_snippet_labels_map:
            if snippet_item.label in block_defining_snippet_labels_map[current_block_keyword]:
                allow_snippet = False
        
        # Rule 3: Exclude general statement snippets if at the very top level (no Proceso/Algoritmo defined yet).
        # These snippets are for writing code inside a main block or sub-blocks.
        if not open_blocks and snippet_item.label in general_statement_snippet_labels:
            allow_snippet = False
            
        # Rule 4: Contextual offering for specific parts of structures (currently illustrative as
        # our snippets are mostly encompassing, and keywords handle parts like 'Sino', 'Caso').
        # Example: If we had a standalone "Sino" snippet:
        # if snippet_item.label == "Sino" and current_block_keyword != "si":
        #     allow_snippet = False
        # Example: If we had a standalone "Caso" snippet:
        # if snippet_item.label == "Caso" and current_block_keyword != "segun":
        #     allow_snippet = False

        if allow_snippet:
            filtered_snippets.append(snippet_item)

    # --- Add Parameters of Current Function/SubProceso ---
    parameter_completions: List[CompletionItem] = []
    if open_blocks:
        current_block_ctx = open_blocks[-1]
        if current_block_ctx.keyword in {"funcion", "subproceso", "subalgoritmo"}:
            # Find the Symbol object for this function/subproceso to get its full parameter details
            function_symbol: Optional[Symbol] = None
            for sym in symbols:
                if sym.name == current_block_ctx.name and \
                   sym.declaration_line == current_block_ctx.start_line and \
                   sym.symbol_type in {"function", "subproceso", "subalgoritmo"}: # ensure it's the correct symbol type
                    function_symbol = sym
                    break
            
            if function_symbol and function_symbol.details:
                params_from_symbol_details = function_symbol.details.get('params', [])
                for param_detail in params_from_symbol_details:
                    param_name = param_detail.get('name')
                    if not param_name:
                        continue

                    param_type = param_detail.get('type', 'Desconocido')
                    param_mode = param_detail.get('mode', 'Por Valor')
                    
                    detail_str = f"Parámetro ({param_type}"
                    if param_mode != "Por Valor":
                        detail_str += f", {param_mode}"
                    detail_str += ")"
                    
                    parameter_completions.append(CompletionItem(
                        label=param_name,
                        kind=CompletionItemKind.Variable, # Parameters are used like variables
                        insert_text=param_name,
                        insert_text_format=InsertTextFormat.PlainText,
                        detail=detail_str,
                        documentation=f"Parámetro de {function_symbol.name}"
                    ))

    return contextual_keywords + symbol_completions + parameter_completions + filtered_snippets
