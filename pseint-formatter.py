# example of use:
# python pseint-formatter.py cine.psc cine_formatted.psc
# python pseint-formatter.py <file_to_format> <file_to_save>

import re


def format_pseint_code(code_string):
    # ... (Your existing format_pseint_code function code) ...
    lines = code_string.split("\n")
    formatted_lines = []
    indentation_level = 0
    indent_size = 4

    # --- Keyword Categorization for Indentation and Casing ---
    all_keywords_list = [
        "Proceso",
        "FinProceso",
        "SubProceso",
        "FinSubProceso",
        "Algoritmo",
        "FinAlgoritmo",
        "Definir",
        "Como",
        "Leer",
        "Escribir",
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
        "FinPara",  # Removed "Hacer" from here as it's part of Para/Mientras line
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
    ]
    all_keywords_lower_to_proper_case = {kw.lower(): kw for kw in all_keywords_list}

    # Keywords that start a new indentation level for the lines *following* them
    indent_starters = {
        "proceso",
        "subproceso",
        "algoritmo",  # Added algoritmo
        "si",
        "mientras",
        "para",
        "segun",
        "repetir",
        "sino",
        "de otro modo",
        # "caso" is handled by mid_transitions causing next indent
    }
    # Keywords that end an indentation level (i.e., they themselves are placed at the outer level)
    indent_enders = {
        "finproceso",
        "finsubproceso",
        "finalgoritmo",  # Added finalgoritmo
        "finsi",
        "finmientras",
        "finpara",
        "finsegun",
        "hasta que",
    }
    # Keywords that are like an "else if" or "case" - they terminate a previous block segment at the same level
    # and start a new one. They are placed at the outer level, and then indent their body.
    indent_mid_transitions = {"sino", "de otro modo", "caso"}

    # --- Helper for Indentation Keyword Matching ---
    def get_keyword_starting_line(line_content_lower, keywords_set):
        for kw_lower in keywords_set:
            if line_content_lower.startswith(kw_lower):
                # Ensure it's a whole word match for keywords like "Si" vs "Siguiente" (if "Siguiente" was a kw)
                # For PSeInt, keywords are distinct enough that simple startswith is usually fine.
                # e.g. "Caso" vs "CasosEspeciales" - "Caso" would match.
                # Check if the character after the keyword is not an alphabet (if kw itself is all alpha)
                # This is more important if identifiers could start with keywords.
                # For now, direct startswith is used as per PSeInt keyword nature.
                if kw_lower == "caso" and not line_content_lower.startswith(
                    "caso "
                ):  # avoid matching "casos" if it were a variable
                    if (
                        ":" not in line_content_lower
                    ):  # "Caso" needs a value and often ":"
                        continue  # Not a structural "Caso" for indentation
                return kw_lower
        return None

    in_repetir_block_awaiting_hasta_que = (
        False  # Specific for Repetir/Hasta Que structure
    )

    for line_number, line in enumerate(lines):
        stripped_line = line.strip()

        if not stripped_line:
            formatted_lines.append("")
            continue

        # 6. Remove trailing whitespace (achieved by .strip() and careful reassembly)

        # 5. Comments
        comment_text = ""
        if "//" in stripped_line:
            parts = stripped_line.split("//", 1)
            main_code_part = parts[0].strip()
            comment_part = parts[1]
            if not comment_part.startswith(" "):
                comment_part = " " + comment_part
            comment_text = "//" + comment_part
        else:
            main_code_part = stripped_line

        # Tokenize for keyword casing and spacing (Rule 3 and 2.d)
        # Regex splits by spaces, operators, parentheses, commas, and comment starts, keeping delimiters.
        # Added // to delimiters to separate it from code for casing.
        raw_tokens = re.split(
            r"(\s+|<-|<=|>=|<>|==|!=|=|<|>|\+|-|\*|/|%|\bMOD\b|Y|&|O|\||NO|~|\(|\)|,|//)",
            main_code_part,
        )

        cased_and_spaced_tokens = []
        is_after_comment_delimiter = False
        for token_idx, token in enumerate(raw_tokens):
            if token is None or not token:
                continue

            if is_after_comment_delimiter:  # Text after // is part of the comment
                cased_and_spaced_tokens.append(token)
                continue

            if token == "//":
                cased_and_spaced_tokens.append(token)
                is_after_comment_delimiter = True
                continue

            if (
                token.isspace()
            ):  # Preserve original significant spaces for now, will normalize later
                cased_and_spaced_tokens.append(token)
                continue

            lower_token = token.lower()
            # Rule 3: Keyword Casing
            if lower_token in all_keywords_lower_to_proper_case:
                cased_token = all_keywords_lower_to_proper_case[lower_token]
                cased_and_spaced_tokens.append(cased_token)

                # Rule 2.d: Space after keywords (if not followed by specific chars or end of line)
                # Look ahead in raw_tokens to see what follows this keyword
                # This logic needs to be careful not to add space before a comment delimiter if no code follows

                # Simple rule: if a keyword is cased, and it's not an operator (MOD),
                # and it's not a line-ending keyword (Fin*), ensure a space if something follows.
                # This is complex to get right at token level for all cases.
                # The regex method later is more general.
                # For now, we ensure that the token reconstruction and later regex passes handle this.
            else:
                cased_and_spaced_tokens.append(token)  # Not a keyword, add as is

        main_code = "".join(cased_and_spaced_tokens)
        is_after_comment_delimiter = False  # Reset for next line processing

        # Rule 2.a (Operators), 2.b (Commas), 2.c (Parentheses), and general keyword spacing (2.d)
        # Apply specific keyword spacing first for those that need it definitely.
        # e.g. "Definir x Como Entero"
        for kw_lower, kw_proper in all_keywords_lower_to_proper_case.items():
            # Ensure space after keywords if followed by a non-whitespace, non-parenthesis, non-comma.
            # Except for operators like MOD which are handled by operator spacing.
            if kw_proper not in ["MOD"]:  # MOD is handled by operator spacing
                main_code = re.sub(
                    r"\b(" + re.escape(kw_proper) + r")\b(?!\s|[\(\,])(?=\S)",
                    r"\1 ",
                    main_code,
                )

        main_code = re.sub(
            r"\s*(<-|<=|>=|<>|==|!=|=|<|>|\+|-|\*|/|%|\bMOD\b|Y|&|O|\||NO|~)\s*",
            r" \1 ",
            main_code,
        )
        main_code = re.sub(r"\s*,\s*", r", ", main_code)
        main_code = re.sub(r"\(\s*", r"(", main_code)
        main_code = re.sub(r"\s*\)", r")", main_code)

        # Collapse multiple spaces into one, and strip leading/trailing spaces from the code part
        main_code = re.sub(r"\s+", " ", main_code).strip()

        # Specific keyword adjustments: e.g. "Fin Si" -> "FinSi"
        # This should be handled by all_keywords_lower having the correct target casing.
        # The tokenizer splits "Fin Si" if it was written like that.
        # If it was "FinSi", it's one token and cased correctly.
        # If it was "Fin    Si", the spaces are removed, then "Fin" and "Si" are cased.
        # This means the `all_keywords` list must contain "FinSi", not "Fin Si". It does.

        # Re-attach comment (Rule 5 comment spacing already handled)
        if comment_text:
            if main_code:
                formatted_line_content = main_code + " " + comment_text
            else:  # Line is only a comment
                formatted_line_content = comment_text
        else:
            formatted_line_content = main_code

        # 1. Indentation
        current_indent_level = indentation_level

        # Determine indentation changes based on keywords starting the line.
        # Use main_code_part (original content before comment) for this check.
        effective_code_lower = main_code_part.lower()
        current_indent_str = (
            " " * indentation_level * indent_size
        )  # Default for current line

        # Check for keywords that end a block first
        matched_ender = get_keyword_starting_line(effective_code_lower, indent_enders)
        matched_mid_transition = get_keyword_starting_line(
            effective_code_lower, indent_mid_transitions
        )

        if matched_ender:
            indentation_level = max(0, indentation_level - 1)
            current_indent_str = " " * indentation_level * indent_size
            if matched_ender == "hasta que":
                in_repetir_block_awaiting_hasta_que = False
        elif matched_mid_transition:
            # For "Sino", "De Otro Modo", "Caso", they align with the previous block starter.
            # So, dedent first to that level for the current line.
            indentation_level = max(0, indentation_level - 1)
            current_indent_str = " " * indentation_level * indent_size
            # The indent for their body will be handled after placing this line.

        # Apply current indentation
        if not main_code_part and comment_text:  # Line was originally only a comment
            final_line_to_add = (
                current_indent_str + comment_text.lstrip()
            )  # lstrip if comment already has spaces
        else:
            final_line_to_add = current_indent_str + formatted_line_content

        formatted_lines.append(final_line_to_add)

        # Now, check for keywords that start a new block (for the *next* line's indentation)
        # This includes mid-transition keywords as they also start a new indented body.
        # If a mid-transition keyword was matched, it takes precedence for starting the next indent.
        keyword_causing_next_indent = None
        if matched_mid_transition:
            keyword_causing_next_indent = matched_mid_transition
        else:
            # Only check indent_starters if not a mid_transition (to avoid double indent logic)
            # and also not an ender (enders don't start new indents)
            if not matched_ender:
                keyword_causing_next_indent = get_keyword_starting_line(
                    effective_code_lower, indent_starters
                )

        if keyword_causing_next_indent:
            indentation_level += 1
            if keyword_causing_next_indent == "repetir":
                in_repetir_block_awaiting_hasta_que = True
            # Special handling for "Caso" - it's a mid-transition that also indents its own body
            # The current logic: "Caso" in indent_mid_transitions means it dedents itself.
            # Then, `keyword_causing_next_indent` will be "caso", leading to `indentation_level += 1`. This is correct.

    # Rule 4: Blank Lines (remove multiple consecutive, ensure at most one)
    final_output_lines = []
    last_line_was_blank = False
    for i, l in enumerate(formatted_lines):
        is_current_blank = not l.strip()
        if is_current_blank:
            if not last_line_was_blank:
                final_output_lines.append("")  # Add one blank line
            last_line_was_blank = True
        else:
            final_output_lines.append(l)
            last_line_was_blank = False

    # Remove leading blank lines if any resulted
    while final_output_lines and not final_output_lines[0].strip():
        final_output_lines.pop(0)

    # Remove trailing blank lines if any resulted
    while final_output_lines and not final_output_lines[-1].strip():
        final_output_lines.pop()

    return "\n".join(final_output_lines)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python pseint_formatter.py <input_file.psc> [output_file.psc]")
        print(
            "If no output file is specified, the formatted code will be printed to the console."
        )
        # Fallback to sample code for demonstration if no arguments provided
        print("\n--- Running with sample code (no arguments provided) ---")
        sample_code = """
Proceso    SUMA
  Escribir "Ingrese el primer numero:"
    Leer   A
Escribir "Ingrese el segundo numero:"
Leer B
    C  <-   A+B
    Escribir    "El resultado es: ",C // Suma realizada
    
    
    // Otro comentario
    Si A > B Entonces
        Escribir "A es mayor"
    Sino
        Escribir "B es mayor o igual"
    FinSi
    Mientras A < 10 Hacer
    A <- A + 1
    Escribir A
    FinMientras
    
Repetir
    Escribir "Dentro de Repetir"
    A <- A - 1
Hasta Que A <= 5
    
Para X<-1 Hasta 10 Con Paso 1 Hacer
Escribir X
FinPara
    
Segun A Hacer
    Caso 1: Escribir "Uno";
    Caso 2:
        Escribir "Dos";
    De Otro Modo: Escribir "Otro";
FinSegun
    
Definir var Como Entero
SubProceso Saludo(nombre Como Texto)
    Escribir "Hola ", nombre
FinSubProceso

// Comentario al final
FinProceso
"""
        formatted_code = format_pseint_code(sample_code)
        print("\n==== Formatted PSeInt Code ====")
        print(formatted_code)

    else:
        input_file_path = sys.argv[1]
        output_file_path = None
        if len(sys.argv) > 2:
            output_file_path = sys.argv[2]

        try:
            with open(input_file_path, "r", encoding="utf-8") as f:
                pseint_code = f.read()

            formatted_code = format_pseint_code(pseint_code)

            if output_file_path:
                with open(output_file_path, "w", encoding="utf-8") as f:
                    f.write(formatted_code)
                print(
                    f"Successfully formatted '{input_file_path}' and saved to '{output_file_path}'"
                )
            else:
                print(formatted_code)

        except FileNotFoundError:
            print(f"Error: The file '{input_file_path}' was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
