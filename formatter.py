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

    # --- Keyword Categorization for Indentation and Casing ---
    all_keywords_list: List[str] = [
        "Proceso",
        "FinProceso",
        "SubProceso",
        "FinSubProceso",
        "Algoritmo",
        "FinAlgoritmo",
        "Funcion",
        "FinFuncion",
        "Definir",
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
        "Por Referencia",
    ]
    all_keywords_lower_to_proper_case: Dict[str, str] = {
        kw.lower(): kw for kw in all_keywords_list
    }

    # Keywords that start a new indentation level for the lines *following* them
    indent_starters: Set[str] = {
        "proceso",
        "subproceso",
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
    indent_mid_transitions: Set[str] = {"sino", "de otro modo", "caso"}

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

        main_code = re.sub(
            r"\s*(<-|<=|>=|<>|==|!=|=|<|>|\+|-|\*|/|%|\bMOD\b|\bY\b|&|\bO\b|\||\bNO\b|~)\s*",
            r" \1 ",
            main_code,
        )
        # Handle comma spacing, but preserve no-space formatting in Caso statements
        # First, handle general comma spacing
        main_code = re.sub(r"\s*,\s*", r", ", main_code)
        # Then, fix Caso statements to remove space after commas
        main_code = re.sub(r"\bCaso\s+([^:]*),\s*([^:]*?):", r"Caso \1,\2:", main_code)
        main_code = re.sub(r"\(\s*", r"(", main_code)
        main_code = re.sub(r"\s*\)", r")", main_code)

        main_code = re.sub(r"\s+", " ", main_code).strip()
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

        if matched_ender:
            indentation_level = max(0, indentation_level - 1)
            current_indent_str = " " * indentation_level * indent_size

            if matched_ender == "hasta que":
                pass  # No special handling needed after removing the unused variable
            elif matched_mid_transition:
                indentation_level = max(0, indentation_level - 1)
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
