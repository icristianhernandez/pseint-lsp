# example of use:
# python pseint-formatter.py cine.psc cine_formatted.psc
# python pseint-formatter.py <file_to_format> <file_to_save>

import re
from typing import List, Dict, Set, Optional  # Add List, Dict, Set, Optional


def format_pseint_code(code_string: str) -> str:
    """
    Formats a given string containing PSeInt code.

    Applies rules for indentation, keyword casing, spacing around operators
    and keywords, and normalization of blank lines and comments.

    Args:
        code_string: A string containing the PSeInt code to be formatted.

    Returns:
        A string containing the formatted PSeInt code.
    """
    lines = code_string.split("\n")
    formatted_lines: List[str] = []
    indentation_level: int = 0
    indent_size: int = 4
    
    # Special state tracking for Segun/Caso structures
    segun_level_stack: List[int] = []  # Track indentation levels where Segun starts

    # --- Keyword Categorization for Indentation and Casing ---
    all_keywords_list: List[str] = [
        "Proceso",
        "FinProceso",
        "SubProceso",
        "FinSubProceso",
        "SubAlgoritmo",
        "FinSubAlgoritmo",
        "Algoritmo",
        "FinAlgoritmo",
        "Funcion",
        "FinFuncion",
        "Definir",
        "Dimension",  # Fix ERROR 02: Add Dimension keyword
        "Como",
        "Leer",
        "Escribir",
        "Escribir Sin Saltar",
        "Si",
        "Entonces",
        "Sino",
        "FinSi",
        "Mientras",
        "Hacer",
        "FinMientras",
        "Para",
        "Hasta",
        "Con Paso",
        "FinPara",
        "Segun",
        "Caso",
        "De Otro Modo",
        "FinSegun",
        "Repetir",
        "Hasta Que",
        "Entero",
        "Real",
        "Numero",
        "Logico",
        "Booleano",
        "Caracter",
        "Texto",
        "Cadena",
        "MOD",
        "Y",  # Fix ERROR 05: Add logical operator Y
        "O",  # Add logical operator O
        "NO", # Add logical operator NO
        "Verdadero",
        "Falso",
        "Por Referencia",
        # Fix ERROR 07: Add common function names
        "SubCadena",
        "Longitud", 
        "Aleatorio",
        "ConvertirANumero",
        "Mayusculas",
        "Minusculas",
        "Borrar Pantalla",
        "Esperar",
        "Milisegundos",
    ]
    all_keywords_lower_to_proper_case: Dict[str, str] = {
        kw.lower(): kw for kw in all_keywords_list
    }

    # Keywords that start a new indentation level for the lines *following* them
    indent_starters: Set[str] = {
        "proceso",
        "subproceso",
        "subalgoritmo",
        "algoritmo",
        "funcion",
        "si",
        "mientras",
        "para",
        "segun",
        "repetir",
        "sino",
        "de otro modo",  # "caso" is effectively handled by mid_transitions then this for body
    }
    # Keywords that end an indentation level (i.e., they themselves are placed at the outer level)
    indent_enders: Set[str] = {
        "finproceso",
        "finsubproceso",
        "finsubalgoritmo",
        "finalgoritmo",
        "finfuncion",
        "finsi",
        "finmientras",
        "finpara",
        "finsegun",
        "hasta que",
    }
    # Keywords that are like an "else if" or "case" - they terminate a previous block segment at the same level
    # and start a new one. They are placed at the outer level, and then indent their body.
    indent_mid_transitions: Set[str] = {"sino", "de otro modo"}
    
    # Caso statements are handled specially - they're inside Segun blocks and should indent from Segun level
    segun_case_keywords: Set[str] = {"caso"}

    # --- Helper for Indentation Keyword Matching ---
    def get_keyword_starting_line(
        line_content_lower: str, keywords_set: Set[str]
    ) -> Optional[str]:
        """
        Checks if a line starts with any of the keywords in the provided set.

        Args:
            line_content_lower: The lowercased content of the line to check.
            keywords_set: A set of lowercased keywords to check against.

        Returns:
            The matched keyword if found, otherwise None.
        """
        for kw_lower in keywords_set:
            if line_content_lower.startswith(kw_lower):
                # Specific check for "caso" to ensure it's followed by a value or colon,
                # differentiating from a variable name like "caso_especial".
                if kw_lower == "caso":
                    if (
                        not line_content_lower.startswith("caso ")
                        and ":" not in line_content_lower
                    ):
                        pass
                return kw_lower
        return None

    # Removed unused variable: in_repetir_block_awaiting_hasta_que

    for _, line in enumerate(lines):
        stripped_line: str = line.strip()

        if not stripped_line:
            formatted_lines.append("")
            continue

        comment_text: str = ""
        main_code_part: str
        if "//" in stripped_line:
            parts: List[str] = stripped_line.split("//", 1)
            main_code_part = parts[0].strip()
            comment_part_text: str = parts[1]
            if not comment_part_text.startswith(" "):
                comment_part_text = " " + comment_part_text
            comment_text = "//" + comment_part_text
        else:
            main_code_part = stripped_line

        original_main_code_part_for_indent_logic: str = main_code_part

        main_code_part_cased: str = main_code_part

        sorted_keywords_for_casing: List[tuple[str, str]] = sorted(
            all_keywords_lower_to_proper_case.items(),
            key=lambda x: len(x[0]),
            reverse=True,
        )

        # Apply keyword casing, but preserve content inside string literals
        def apply_keyword_casing_outside_strings(text: str) -> str:
            """Apply keyword casing only to text outside of string literals."""
            result: List[str] = []
            i = 0

            while i < len(text):
                char = text[i]

                if char in ['"', "'"]:
                    # Find the complete string literal
                    quote_char = char
                    string_start = i
                    i += 1  # Move past opening quote

                    # Find closing quote
                    while i < len(text) and text[i] != quote_char:
                        i += 1

                    if i < len(text):
                        i += 1  # Include closing quote

                    # Add the entire string literal as-is
                    string_literal = text[string_start:i]
                    result.append(string_literal)
                else:
                    # Outside string literal, collect until next string or end
                    segment_start = i
                    while i < len(text) and text[i] not in ['"', "'"]:
                        i += 1

                    segment = text[segment_start:i]

                    # Apply keyword casing to this segment
                    for kw_lower, kw_proper in sorted_keywords_for_casing:
                        # Special handling for single-letter logical operators
                        # Only replace them when they are clearly used as operators, not variables or parts of words
                        if kw_lower in ['y', 'o'] and len(kw_lower) <= 2:
                            # For logical operators, only replace when they are standalone and between expressions
                            if kw_lower == 'y':
                                # Replace Y when it's between expressions (not at start of line as variable)
                                # More specific patterns to avoid false matches
                                segment = re.sub(
                                    r'(?<=\))\s*' + re.escape(kw_lower) + r'\s*(?=\()',
                                    f' {kw_proper} ',
                                    segment,
                                    flags=re.IGNORECASE
                                )
                                # Pattern for word Y word, but only when Y is surrounded by spaces or punctuation
                                segment = re.sub(
                                    r'(?<=[\w\)])\s+' + re.escape(kw_lower) + r'\s+(?=[\w\(])',
                                    f' {kw_proper} ',
                                    segment,
                                    flags=re.IGNORECASE
                                )
                            elif kw_lower == 'o':
                                # For O, be even more careful - only replace when clearly an operator
                                # Look for patterns like ") O (" or "word O word" but not inside words
                                segment = re.sub(
                                    r'(?<=\))\s*' + re.escape(kw_lower) + r'\s*(?=\()',
                                    f' {kw_proper} ',
                                    segment,
                                    flags=re.IGNORECASE
                                )
                                # Only replace O when it's a standalone word with spaces around it
                                segment = re.sub(
                                    r'(?<=\s)' + re.escape(kw_lower) + r'(?=\s)',
                                    kw_proper,
                                    segment,
                                    flags=re.IGNORECASE
                                )
                        elif kw_lower == 'no':
                            # NO is often used as a prefix operator
                            # Only replace when it's clearly the NO logical operator
                            segment = re.sub(
                                r'\b' + re.escape(kw_lower) + r'\s*(?=\()',
                                f'{kw_proper} ',
                                segment,
                                flags=re.IGNORECASE
                            )
                            # Also handle "NO variable" patterns
                            segment = re.sub(
                                r'\b' + re.escape(kw_lower) + r'\s+(?=\w)',
                                f'{kw_proper} ',
                                segment,
                                flags=re.IGNORECASE
                            )
                        # Skip boolean literals - let them be handled by general keyword replacement or not at all
                        elif kw_lower in ['verdadero', 'falso']:
                            # Skip these to preserve original case
                            continue
                        else:
                            # Standard keyword replacement for other keywords
                            if " " in kw_lower:
                                pattern_parts: List[str] = [
                                    re.escape(part) for part in kw_lower.split(" ")
                                ]
                                regex_pattern: str = (
                                    r"\b" + r"\s+".join(pattern_parts) + r"\b"
                                )
                            else:
                                regex_pattern: str = r"\b" + re.escape(kw_lower) + r"\b"

                            try:
                                segment = re.sub(
                                    regex_pattern, kw_proper, segment, flags=re.IGNORECASE
                                )
                            except re.error:
                                pass

                    result.append(segment)

            return "".join(result)

        main_code_part_cased = apply_keyword_casing_outside_strings(main_code_part)

        raw_tokens: List[str] = re.split(
            r"(\s+|<-|<=|>=|<>|==|!=|=|<|>|\+|-|\*|/|%|\bMOD\b|\bY\b|&|\bO\b|\||\bNO\b|~|\(|\)|,|//)",
            main_code_part_cased,
        )

        processed_tokens: List[str] = []
        for token in raw_tokens:
            processed_tokens.append(token)

        main_code: str = "".join(processed_tokens)

        # Apply keyword spacing, but preserve content inside string literals
        def apply_keyword_spacing_outside_strings(text: str) -> str:
            """Apply keyword spacing only to text outside of string literals."""
            result: List[str] = []
            i = 0

            while i < len(text):
                char = text[i]

                if char in ['"', "'"]:
                    # Find the complete string literal
                    quote_char = char
                    string_start = i
                    i += 1  # Move past opening quote

                    # Find closing quote
                    while i < len(text) and text[i] != quote_char:
                        i += 1

                    if i < len(text):
                        i += 1  # Include closing quote

                    # Add the entire string literal as-is
                    string_literal = text[string_start:i]
                    result.append(string_literal)
                else:
                    # Outside string literal, collect until next string or end
                    segment_start = i
                    while i < len(text) and text[i] not in ['"', "'"]:
                        i += 1

                    segment = text[segment_start:i]

                    # Apply keyword spacing to this segment
                    for kw_proper in all_keywords_lower_to_proper_case.values():
                        if kw_proper not in ["MOD"]:
                            # Check if segment ends with keyword and next char is a quote
                            if (i < len(text) and text[i] in ['"', "'"] and 
                                segment.endswith(kw_proper) and 
                                (len(segment) == len(kw_proper) or not segment[-len(kw_proper)-1].isalnum())):
                                # Add space before the upcoming quote
                                segment = segment[:-len(kw_proper)] + kw_proper + " "
                            else:
                                # Normal regex processing for other cases
                                segment = re.sub(
                                    r"\b("
                                    + re.escape(kw_proper)
                                    + r")\b(?!\s|[\(\,\:])(?=\S)",
                                    r"\1 ",
                                    segment,
                                )

                    result.append(segment)

            return "".join(result)

        main_code = apply_keyword_spacing_outside_strings(main_code)

        # Apply operator spacing, but preserve content inside string literals
        def apply_operator_spacing_outside_strings(text: str) -> str:
            """Apply operator spacing only to text outside of string literals."""
            result: List[str] = []
            i = 0

            while i < len(text):
                char = text[i]

                if char in ['"', "'"]:
                    # Find the complete string literal
                    quote_char = char
                    string_start = i
                    i += 1  # Move past opening quote

                    # Find closing quote
                    while i < len(text) and text[i] != quote_char:
                        i += 1

                    if i < len(text):
                        i += 1  # Include closing quote

                    # Add the entire string literal as-is
                    string_literal = text[string_start:i]
                    result.append(string_literal)
                else:
                    # Outside string literal, collect until next string or end
                    segment_start = i
                    while i < len(text) and text[i] not in ['"', "'"]:
                        i += 1

                    segment = text[segment_start:i]

                    # Apply operator spacing to this segment
                    # Fix ERROR 01: Handle "Con Paso -number" specially to preserve negative numbers
                    
                    # Apply general operator spacing (excluding minus which is handled below)
                    segment = re.sub(
                        r"\s*(<-|<=|>=|<>|==|!=|=|<|>|\+|\*|/|%|\bMOD\b|\bY\b|&|\bO\b|\||\bNO\b|~)\s*",
                        r" \1 ",
                        segment,
                        flags=re.IGNORECASE
                    )
                    
                    # Handle minus operator spacing more carefully
                    # Only add spaces around minus when it's clearly a binary operator
                    # Avoid spacing negative numbers (those following specific patterns)
                    segment = re.sub(
                        r"(\w)\s*-\s*(\w)",  # between two words/numbers: a-b -> a - b
                        r"\1 - \2",
                        segment
                    )
                    segment = re.sub(
                        r"(\))\s*-\s*(\w)",  # after closing parenthesis: )-a -> ) - a
                        r"\1 - \2", 
                        segment
                    )
                    
                    # Fix "Con Paso -number" after general processing (as final pass)
                    segment = re.sub(
                        r"(Con\s+Paso)\s+-\s+(\d+)",
                        r"\1 -\2",
                        segment,
                        flags=re.IGNORECASE
                    )
                    result.append(segment)

            return "".join(result)

        # Apply punctuation spacing, but preserve content inside string literals
        def apply_punctuation_spacing_outside_strings(text: str) -> str:
            """Apply punctuation spacing only to text outside of string literals."""
            result: List[str] = []
            i = 0

            while i < len(text):
                char = text[i]

                if char in ['"', "'"]:
                    # Find the complete string literal
                    quote_char = char
                    string_start = i
                    i += 1  # Move past opening quote

                    # Find closing quote
                    while i < len(text) and text[i] != quote_char:
                        i += 1

                    if i < len(text):
                        i += 1  # Include closing quote

                    # Add the entire string literal as-is
                    string_literal = text[string_start:i]
                    result.append(string_literal)
                else:
                    # Outside string literal, collect until next string or end
                    segment_start = i
                    while i < len(text) and text[i] not in ['"', "'"]:
                        i += 1

                    segment = text[segment_start:i]

                    # Apply punctuation spacing to this segment
                    # Handle comma spacing, but preserve no-space formatting in Caso statements
                    segment = re.sub(r"\s*,\s*", r", ", segment)
                    # Handle parentheses spacing
                    segment = re.sub(r"\(\s*", r"(", segment)
                    segment = re.sub(r"\s*\)", r")", segment)
                    
                    result.append(segment)

            return "".join(result)

        # Apply whitespace normalization, but preserve content inside string literals
        def normalize_whitespace_outside_strings(text: str) -> str:
            """Normalize whitespace only outside of string literals."""
            result: List[str] = []
            i = 0

            while i < len(text):
                char = text[i]

                if char in ['"', "'"]:
                    # Find the complete string literal
                    quote_char = char
                    string_start = i
                    i += 1  # Move past opening quote

                    # Find closing quote
                    while i < len(text) and text[i] != quote_char:
                        i += 1

                    if i < len(text):
                        i += 1  # Include closing quote

                    # Add the entire string literal as-is
                    string_literal = text[string_start:i]
                    result.append(string_literal)
                else:
                    # Outside string literal, collect until next string or end
                    segment_start = i
                    while i < len(text) and text[i] not in ['"', "'"]:
                        i += 1

                    segment = text[segment_start:i]

                    # Normalize whitespace in this segment
                    segment = re.sub(r"\s+", " ", segment)
                    result.append(segment)

            return "".join(result).strip()

        main_code = apply_operator_spacing_outside_strings(main_code)
        main_code = apply_punctuation_spacing_outside_strings(main_code)
        main_code = normalize_whitespace_outside_strings(main_code)
        
        # Then, fix Caso statements to remove space after commas (outside strings only)
        def fix_caso_statements_outside_strings(text: str) -> str:
            """Fix Caso statement formatting only outside of string literals."""
            result: List[str] = []
            i = 0

            while i < len(text):
                char = text[i]

                if char in ['"', "'"]:
                    # Find the complete string literal
                    quote_char = char
                    string_start = i
                    i += 1  # Move past opening quote

                    # Find closing quote
                    while i < len(text) and text[i] != quote_char:
                        i += 1

                    if i < len(text):
                        i += 1  # Include closing quote

                    # Add the entire string literal as-is
                    string_literal = text[string_start:i]
                    result.append(string_literal)
                else:
                    # Outside string literal, collect until next string or end
                    segment_start = i
                    while i < len(text) and text[i] not in ['"', "'"]:
                        i += 1

                    segment = text[segment_start:i]

                    # Fix Caso statements in this segment
                    # Handle multiple comma-separated values in Caso statements
                    if "Caso " in segment:
                        # Match Caso statements and remove spaces after commas in the value list
                        segment = re.sub(r"\bCaso\s+([^:]+):", lambda m: f"Caso {re.sub(r',\s*', ',', m.group(1))}:", segment)
                    result.append(segment)

            return "".join(result)

        main_code = fix_caso_statements_outside_strings(main_code)
        main_code = re.sub(r"\s+;", ";", main_code)
        # main_code = re.sub(r"\s+:", ":", main_code)

        processed_main_code_for_split = main_code
        original_main_code_part_lower_for_split = (
            original_main_code_part_for_indent_logic.lower()
        )

        potential_split_statement = None

        if original_main_code_part_lower_for_split.startswith("caso"):
            match = re.match(r"^(Caso\s+[^:]+:)(.*)", processed_main_code_for_split)
            if match:
                keyword_section = match.group(1).strip()
                trailing_statement = match.group(2).strip()
                if trailing_statement:
                    processed_main_code_for_split = keyword_section
                    potential_split_statement = trailing_statement

        elif original_main_code_part_lower_for_split.startswith("de otro modo"):
            match = re.match(
                r"^De Otro Modo\s*:?\s*(.*)", processed_main_code_for_split
            )
            if match:
                keyword_section = "De Otro Modo:"  # Always use consistent format
                trailing_statement = match.group(1).strip()
                if trailing_statement:
                    processed_main_code_for_split = keyword_section
                    potential_split_statement = trailing_statement

        main_code = processed_main_code_for_split

        formatted_line_content: str
        if comment_text:
            if main_code:
                formatted_line_content = main_code + " " + comment_text
            else:
                formatted_line_content = comment_text
        else:
            formatted_line_content = main_code

        effective_code_lower: str = original_main_code_part_for_indent_logic.lower()
        current_indent_str: str = " " * indentation_level * indent_size

        matched_ender: Optional[str] = get_keyword_starting_line(
            effective_code_lower, indent_enders
        )
        matched_mid_transition: Optional[str] = get_keyword_starting_line(
            effective_code_lower, indent_mid_transitions
        )
        matched_caso: Optional[str] = get_keyword_starting_line(
            effective_code_lower, segun_case_keywords
        )
        matched_segun: Optional[str] = get_keyword_starting_line(
            effective_code_lower, {"segun"}
        )
        matched_finsegun: Optional[str] = get_keyword_starting_line(
            effective_code_lower, {"finsegun"}
        )

        # Handle Segun block tracking
        if matched_segun:
            # Starting a new Segun block - track the current level
            segun_level_stack.append(indentation_level)
        elif matched_finsegun and segun_level_stack:
            # Ending a Segun block - restore indentation level to Segun level
            segun_start_level = segun_level_stack.pop()
            indentation_level = segun_start_level

        if matched_finsegun:
            # FinSegun should be at the same level as Segun - already handled above
            current_indent_str = " " * indentation_level * indent_size
        elif matched_ender:
            indentation_level = max(0, indentation_level - 1)
            current_indent_str = " " * indentation_level * indent_size
        elif matched_mid_transition:
            indentation_level = max(0, indentation_level - 1)
            current_indent_str = " " * indentation_level * indent_size
        elif matched_caso and segun_level_stack:
            # Caso statements should be at Segun level + 1, not current level
            caso_level = segun_level_stack[-1] + 1
            current_indent_str = " " * caso_level * indent_size
            # Reset indentation level to maintain consistency for subsequent statements
            indentation_level = caso_level
        else:
            current_indent_str = " " * indentation_level * indent_size

        final_line_to_add: str
        if not original_main_code_part_for_indent_logic and comment_text:
            final_line_to_add = current_indent_str + comment_text.lstrip()
        else:
            final_line_to_add = current_indent_str + formatted_line_content

        formatted_lines.append(final_line_to_add)

        keyword_causing_next_indent: Optional[str] = None
        if matched_mid_transition:
            keyword_causing_next_indent = matched_mid_transition
        elif matched_caso:
            keyword_causing_next_indent = matched_caso
        else:
            if not matched_ender:
                keyword_causing_next_indent = get_keyword_starting_line(
                    effective_code_lower, indent_starters
                )

        if keyword_causing_next_indent:
            indentation_level += 1

        if potential_split_statement:
            current_split_line_indent_str = " " * indentation_level * indent_size
            formatted_lines.append(
                current_split_line_indent_str + potential_split_statement
            )

    # Rule 4: Blank Lines
    final_output_lines: List[str] = []
    last_line_was_blank = False

    # indent_enders and get_keyword_starting_line must be accessible here.
    # They are defined within format_pseint_code, so they are in scope.

    for i, current_line_content in enumerate(formatted_lines):
        is_current_line_empty_after_strip = not current_line_content.strip()

        if is_current_line_empty_after_strip:
            # Current line is blank. Check if we should add it.
            # Don't add if previous was already a blank (last_line_was_blank is true).
            # Also, don't add if the next non-blank line is an indent_ender.
            if last_line_was_blank:
                continue  # Already added a blank, or multiple blanks collapsed

            # Look ahead for next non-blank line
            is_next_non_blank_line_an_ender = False
            for j in range(i + 1, len(formatted_lines)):
                next_line_to_check_stripped = formatted_lines[j].strip()
                if next_line_to_check_stripped:  # Found next non-blank line
                    # Check if this line starts with any indent_ender keyword
                    # get_keyword_starting_line expects lowercase line content and lowercase keyword set
                    if get_keyword_starting_line(
                        next_line_to_check_stripped.lower(), indent_enders
                    ):
                        is_next_non_blank_line_an_ender = True
                    break  # Stop lookahead once next non-blank is found

            if not is_next_non_blank_line_an_ender:
                final_output_lines.append("")  # Add the blank line

            last_line_was_blank = (
                True  # Mark that we've processed (and possibly added) a blank
            )
        else:
            # Current line is not blank
            final_output_lines.append(current_line_content)
            last_line_was_blank = False

    # Remove leading blank lines if any resulted (from the original lines processing)
    # This should be applied to final_output_lines
    while final_output_lines and not final_output_lines[0].strip():
        final_output_lines.pop(0)

    # Remove trailing blank lines if any resulted (from the original lines processing)
    while final_output_lines and not final_output_lines[-1].strip():
        final_output_lines.pop()

    return "\n".join(final_output_lines)


# Removed the if __name__ == "__main__": block that handled command-line arguments and file I/O.
# The function format_pseint_code(code_string) is now intended to be imported and used directly.
