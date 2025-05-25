# PSeInt Syntax and Formatting Rules Analysis

## 1. Keywords

*   `Proceso`
*   `FinProceso`
*   `Algoritmo`
*   `FinAlgoritmo`
*   `SubProceso` (also seen as `SubAlgoritmo`)
*   `FinSubProceso` (also seen as `FinSubAlgoritmo`)
*   `Definir`
*   `Como`
*   `Leer`
*   `Escribir`
*   `Escribir Sin Saltar`
*   `Si`
*   `Entonces`
*   `Sino`
*   `FinSi`
*   `Mientras`
*   `Hacer`
*   `FinMientras`
*   `Para`
*   `Hasta`
*   `Con Paso`
*   `FinPara`
*   `Segun`
*   `Caso` (within `Segun`)
*   `De Otro Modo` (within `Segun`)
*   `FinSegun`
*   `Repetir`
*   `Hasta Que`
*   `Dimension`
*   `Funcion` (for function definitions that return a value)
*   `MOD` (Operator, but listed as a keyword in formatter)
*   `Por Referencia` (for parameter passing)
*   `Por Valor` (for parameter passing, though often implicit)

## 2. Data Types

*   `Entero`
*   `Real` (implied, though `Numero` is used in formatter)
*   `Numero` (used in formatter, likely encompasses `Entero` and `Real`)
*   `Logico`
*   `Booleano` (used in formatter, synonym for `Logico`)
*   `Caracter`
*   `Texto` (used in formatter, synonym for `Caracter` or `Cadena`)
*   `Cadena`

## 3. Control Structures

### 3.1. Conditional (Si)
*   `Si <condicion> Entonces`
*   `Sino`
*   `FinSi`

### 3.2. Loop (Mientras)
*   `Mientras <condicion> Hacer`
*   `FinMientras`

### 3.3. Loop (Para)
*   `Para <variable> <- <valor_inicial> Hasta <valor_final> Con Paso <paso> Hacer`
*   `FinPara`

### 3.4. Loop (Repetir)
*   `Repetir`
*   `Hasta Que <condicion>`

### 3.5. Switch/Case (Segun)
*   `Segun <variable> Hacer`
*   `Caso <valor1_o_rango>[, <valor2_o_rango>, ...]:` (colon seems optional in some contexts but good practice)
*   `De Otro Modo:` (colon seems optional but good practice)
*   `FinSegun`

## 4. Operators

*   Assignment: `<-`
*   Arithmetic: `+`, `-`, `*`, `/`, `%` (Modulo), `MOD` (Modulo keyword)
*   Logical: `Y`, `O`, `NO` (also `&`, `|`, `~` as per formatter)
*   Relational: `=`, `<`, `>`, `<=`, `>=`, `<>` (Note: `=` for comparison, `<-` for assignment). The formatter also includes `==`, `!=`.

## 5. Functions and Subprocesses

*   **SubProceso (Procedure):**
    *   `SubProceso nombre_subproceso (param1 Como Tipo, param2 Por Referencia Como Tipo, ...)`
    *   `SubAlgoritmo nombre_subalgoritmo (param1 Como Tipo, ...)` (synonymous with SubProceso)
    *   `FinSubProceso` or `FinSubAlgoritmo`
*   **Funcion (Function that returns a value):**
    *   `Funcion variable_retorno = nombre_funcion (param1 Como Tipo, ...)`
    *   `FinFuncion` (implied, not explicitly seen in examples but standard in PSeInt)
*   Parameter Passing:
    *   By Value (default): `param1 Como Tipo`
    *   By Reference: `param1 Por Referencia Como Tipo` or `param1 Por Referencia`

## 6. Arrays/Matrices

*   Declaration: `Dimension nombre_array[tam1, tam2, ...]` (e.g., `Dimension matrizJugador[11,11]`)
*   Access: `nombre_array[idx1, idx2, ...]` (e.g., `matrizJugador[i,j]`)
*   Indices are typically 0-based or 1-based depending on PSeInt configuration, but examples show both (e.g. loops from 0 to N-1, and direct access like `matriz[fila, columna+h]`). The reference code seems to use both 0-indexed and 1-indexed logic in different places.

## 7. Comments

*   `// comentario` (single line, extending to the end of the line)

## 8. Other Notable Syntax and Built-in Functions

*   Screen Output/Control:
    *   `Borrar Pantalla`
    *   `Esperar <tiempo> Milisegundos` (or `Segundos`)
*   String Manipulation:
    *   `Mayusculas(cadena)`
    *   `Longitud(cadena)`
    *   `Subcadena(cadena, desde_idx, hasta_idx)` (indices might be 0-based or 1-based depending on context/PSeInt version)
*   Type Conversion:
    *   `ConvertirANumero(cadena)`
*   Mathematical:
    *   `Aleatorio(min_valor, max_valor)`
    *   `trunc(numero)` (truncates decimal part)
*   Keywords/Commands:
    *   `Dimension` (for array/matrix declaration)

## 9. Formatting Rules from pseint-formatter.py

*   **Indentation:**
    *   Keywords starting indentation for the *following* lines: `Proceso`, `SubProceso`, `Algoritmo`, `Si`, `Mientras`, `Para`, `Segun`, `Repetir`.
    *   Keywords also starting indentation for their block (after being placed at the outer level of their parent): `Sino`, `De Otro Modo`, `Caso`.
    *   Keywords ending indentation (they themselves are placed at the outer level): `FinProceso`, `FinSubProceso`, `FinAlgoritmo`, `FinSi`, `FinMientras`, `FinPara`, `FinSegun`, `Hasta Que`.
    *   Indent size: 4 spaces.
*   **Keyword Casing:**
    *   All recognized keywords are converted to Proper Case (e.g., `proceso` -> `Proceso`). The script maintains a comprehensive list: `Proceso`, `FinProceso`, `SubProceso`, `FinSubProceso`, `Algoritmo`, `FinAlgoritmo`, `Definir`, `Como`, `Leer`, `Escribir`, `Si`, `Entonces`, `Sino`, `FinSi`, `Mientras`, `Hacer`, `FinMientras`, `Para`, `Hasta`, `Con Paso`, `FinPara`, `Segun`, `Caso`, `De Otro Modo`, `FinSegun`, `Repetir`, `Hasta Que`, `Entero`, `Real`, `Numero`, `Logico`, `Booleano`, `Caracter`, `Texto`, `Cadena`, `MOD`.
*   **Spacing:**
    *   **Operators:** Surrounded by single spaces. This includes: `<-`, `<=`, `>=`, `<>`, `==`, `!=`, `=`, `<`, `>`, `+`, `-`, `*`, `/`, `%`, `MOD`, `Y`, `&`, `O`, `|`, `NO`, `~`.
    *   **Commas:** Followed by a space, no space before (e.g., `, `).
    *   **Parentheses:** No space immediately after `(` and no space immediately before `)`.
    *   **Keywords:** Space after keywords if they are not followed by `(`, `,`, or another space, and are followed by a non-whitespace character. This is to ensure `Escribir "Hola"` instead of `Escribir"Hola"`. `MOD` is treated as an operator for spacing.
*   **Blank Lines:**
    *   Multiple consecutive blank lines are collapsed into a single blank line.
    *   Leading blank lines at the beginning of the file are removed.
    *   Trailing blank lines at the end of the file are removed.
*   **Comments:**
    *   A space is ensured after the `//` delimiter if not already present (e.g., `//comment` becomes `// comment`).
    *   Comments are indented to the same level as the code line they are associated with or precede. If a line is only a comment, it gets the current indentation level.
*   **Line Endings:**
    *   Trailing whitespace on lines is removed.
*   **Tokenization and Structure:**
    *   The formatter tokenizes lines based on spaces, operators, parentheses, commas, and comment delimiters to apply casing and spacing rules correctly.
    *   It has specific logic for `Repetir...Hasta Que` blocks to manage indentation correctly.
    *   `Caso` statements are handled as mid-transitions that dedent to the level of `Segun` and then indent their own content.
```
