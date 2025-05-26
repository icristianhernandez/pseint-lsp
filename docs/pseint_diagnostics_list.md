# PSeInt Diagnostics List

This document lists potential diagnostics (errors and warnings) for PSeInt code, based on common syntax and semantic rules.

## 1. Block Errors

These errors relate to the incorrect structure of PSeInt blocks (Proceso, Si, Mientras, etc.).

*   **Message**: "Bloque '<block_type>' no cerrado con '<expected_closing_keyword>'."
    *   **Severity**: Error
    *   **Example**:
        ```pseint
        Proceso Ejemplo
            Escribir "Hola";
        // FinProceso falta
        ```
    *   **Note**: Applies to `Proceso`, `Algoritmo`, `SubProceso`, `SubAlgoritmo`, `Funcion`, `Si`, `Mientras`, `Para`, `Segun`, `Repetir`.

*   **Message**: "'<closing_keyword>' inesperado sin un bloque '<expected_opening_keyword>' abierto."
    *   **Severity**: Error
    *   **Example**:
        ```pseint
        Escribir "Algo";
        FinProceso // No hay Proceso que cerrar
        ```
    *   **Note**: Applies to `FinProceso`, `FinAlgoritmo`, `FinSubProceso`, `FinSubAlgoritmo`, `FinFuncion`, `FinSi`, `FinMientras`, `FinPara`, `FinSegun`, `Hasta Que`.

*   **Message**: "Se esperaba '<expected_closing_keyword>' pero se encontró '<actual_closing_keyword>'."
    *   **Severity**: Error
    *   **Example**:
        ```pseint
        Proceso EjemploMalo
            Si a > 5 Entonces
                Escribir "Dentro del Si";
            FinProceso // Debería ser FinSi
        ```

*   **Message**: "'<keyword>' no puede estar en la misma línea que '<block_start_keyword> ... Entonces'."
    *   **Severity**: Error
    *   **Example**:
        ```pseint
        Proceso EjemploMalo
            Si a > 5 Entonces FinSi // FinSi en la misma línea
        FinProceso
        ```
    *   **Note**: Primarily for `FinSi` with `Si ... Entonces`.

*   **Message**: "Palabra clave '<keyword>' inesperada fuera de un bloque '<expected_parent_block>'."
    *   **Severity**: Error
    *   **Example (Sino fuera de Si)**:
        ```pseint
        Proceso Ejemplo
            Sino // Sino sin un Si...Entonces previo
                Escribir "Esto es un error";
            FinSi
        FinProceso
        ```
    *   **Example (Caso fuera de Segun)**:
        ```pseint
        Proceso Ejemplo
            Caso 1: // Caso sin un Segun previo
                Escribir "Error";
        FinProceso
        ```
    *   **Note**: Applies to `Sino`, `Caso`, `De Otro Modo`, `Hasta Que` (if not preceded by `Repetir`).

*   **Message**: "Bloque '<block_type>' vacío. Se esperaba contenido."
    *   **Severity**: Warning (Potentially Error depending on PSeInt strictness)
    *   **Example**:
        ```pseint
        Proceso BloqueVacio
            Si a > 10 Entonces
            FinSi
        FinProceso
        ```

## 2. Variable and Definition Errors

These errors relate to variable declarations, usage, and type definitions.

*   **Message**: "Variable '<variable_name>' no definida."
    *   **Severity**: Error
    *   **Example**:
        ```pseint
        Proceso Ejemplo
            x <- 5; // x no ha sido definida
            Escribir x;
        FinProceso
        ```

*   **Message**: "Variable '<variable_name>' definida pero no utilizada."
    *   **Severity**: Warning
    *   **Example**:
        ```pseint
        Proceso Ejemplo
            Definir x Como Entero;
            // x nunca se usa
        FinProceso
        ```

*   **Message**: "Redefinición de variable '<variable_name>'."
    *   **Severity**: Error
    *   **Example**:
        ```pseint
        Proceso Ejemplo
            Definir x Como Entero;
            Definir x Como Real; // x ya está definida
        FinProceso
        ```

*   **Message**: "Tipo de dato desconocido: '<type_name>'."
    *   **Severity**: Error
    *   **Example**:
        ```pseint
        Proceso Ejemplo
            Definir x Como Numerito; // 'Numerito' no es un tipo válido
        FinProceso
        ```
    *   **Note**: Valid types are `Entero`, `Real`, `Numero`, `Logico`, `Booleano`, `Caracter`, `Texto`, `Cadena`.

*   **Message**: "Se esperaba la palabra clave 'Como' en la definición de variable."
    *   **Severity**: Error
    *   **Example**:
        ```pseint
        Proceso Ejemplo
            Definir x Entero; // Falta 'Como'
        FinProceso
        ```

*   **Message**: "Variable '<variable_name>' utilizada antes de ser asignada."
    *   **Severity**: Warning (Potentially Error in some PSeInt configurations)
    *   **Example**:
        ```pseint
        Proceso Ejemplo
            Definir x Como Entero;
            Escribir x; // x no tiene un valor asignado
            x <- 10;
        FinProceso
        ```

## 3. Type Errors

These errors relate to mismatched types in assignments, operations, or function calls.

*   **Message**: "No se puede asignar un valor de tipo '<source_type>' a una variable de tipo '<target_type>'."
    *   **Severity**: Error
    *   **Example**:
        ```pseint
        Proceso Ejemplo
            Definir nombre Como Caracter;
            nombre <- 123; // Se asigna Entero a Caracter
        FinProceso
        ```

*   **Message**: "Operador '<operator>' no aplicable a operandos de tipo '<type1>' y '<type2>'."
    *   **Severity**: Error
    *   **Example**:
        ```pseint
        Proceso Ejemplo
            Definir texto Como Caracter;
            Definir num Como Entero;
            texto <- "Hola";
            num <- texto + 5; // No se puede sumar Caracter y Entero
        FinProceso
        ```

*   **Message**: "Condición en '<control_structure>' debe ser de tipo Logico."
    *   **Severity**: Error
    *   **Example**:
        ```pseint
        Proceso Ejemplo
            Definir x Como Entero;
            x <- 10;
            Si x Entonces // x es Entero, no Logico
                Escribir "Condición inválida";
            FinSi
        FinProceso
        ```
    *   **Note**: Applies to `Si`, `Mientras`, `Hasta Que`.

*   **Message**: "La variable de control en 'Para' debe ser de tipo numérico."
    *   **Severity**: Error
    *   **Example**:
        ```pseint
        Proceso Ejemplo
            Definir i Como Caracter;
            Para i <- "a" Hasta "z" Con Paso 1 Hacer // i debe ser numérico
                Escribir i;
            FinPara
        FinProceso
        ```
*   **Message**: "Los límites y el paso en 'Para' deben ser de tipo numérico."
    *   **Severity**: Error
    *   **Example**:
        ```pseint
        Proceso Ejemplo
            Definir i Como Entero;
            Para i <- 1 Hasta "diez" Hacer // "diez" no es numérico
                Escribir i;
            FinPara
        FinProceso
        ```

*   **Message**: "La variable en 'Segun' debe ser de tipo Entero o Caracter." (PSeInt often restricts to ordinal types)
    *   **Severity**: Error
    *   **Example**:
        ```pseint
        Proceso Ejemplo
            Definir x Como Real;
            x <- 5.5;
            Segun x Hacer // x es Real, usualmente no permitido
                Caso 5.5: Escribir "Medio";
            FinSegun
        FinProceso
        ```

*   **Message**: "Los valores en 'Caso' deben coincidir con el tipo de la variable en 'Segun'."
    *   **Severity**: Error
    *   **Example**:
        ```pseint
        Proceso Ejemplo
            Definir x Como Entero;
            x <- 1;
            Segun x Hacer
                Caso "uno": Escribir "Texto"; // x es Entero, "uno" es Caracter
            FinSegun
        FinProceso
        ```

## 4. Operator Errors

These errors relate to the misuse or malformation of operators.

*   **Message**: "Operador de asignación incorrecto. Use '<-' en lugar de '='."
    *   **Severity**: Error (Potentially Warning if PSeInt is lenient and auto-corrects)
    *   **Example**:
        ```pseint
        Proceso Ejemplo
            Definir x Como Entero;
            x = 5; // Debería ser x <- 5
        FinProceso
        ```

*   **Message**: "Operador de comparación incorrecto. Use '=' para comparación, no '<-'."
    *   **Severity**: Error
    *   **Example**:
        ```pseint
        Proceso Ejemplo
            Definir x Como Entero;
            x <- 5;
            Si x <- 5 Entonces // Debería ser x = 5
                Escribir "Iguales";
            FinSi
        FinProceso
        ```
    *   **Note**: PSeInt often uses `=` for comparison. If `==` is used from other languages, it might be an error or warning.

*   **Message**: "Faltan operandos para el operador '<operator>'."
    *   **Severity**: Error
    *   **Example**:
        ```pseint
        Proceso Ejemplo
            Definir x Como Entero;
            x <- 5 + ; // Operando faltante después de +
        FinProceso
        ```

*   **Message**: "Operador '<operator>' desconocido o mal utilizado."
    *   **Severity**: Error
    *   **Example**:
        ```pseint
        Proceso Ejemplo
            Definir x Como Entero;
            x <- 5 ** 2; // ** no es el operador de potencia estándar en PSeInt (es ^)
        FinProceso
        ```

## 5. Control Structure Errors

These errors relate to the specific syntax requirements of control structures beyond block open/close.

*   **Message**: "Se esperaba 'Entonces' después de la condición en 'Si'."
    *   **Severity**: Error
    *   **Example**:
        ```pseint
        Proceso Ejemplo
            Si a > 5 // Falta 'Entonces'
                Escribir "Mayor";
            FinSi
        FinProceso
        ```

*   **Message**: "Se esperaba 'Hacer' después de la condición en 'Mientras'."
    *   **Severity**: Error
    *   **Example**:
        ```pseint
        Proceso Ejemplo
            Mientras x < 10 // Falta 'Hacer'
                x <- x + 1;
            FinMientras
        FinProceso
        ```

*   **Message**: "Se esperaba 'Hacer' en la estructura 'Para'."
    *   **Severity**: Error
    *   **Example**:
        ```pseint
        Proceso Ejemplo
            Definir i Como Entero;
            Para i <- 1 Hasta 10 // Falta 'Hacer'
                Escribir i;
            FinPara
        FinProceso
        ```

*   **Message**: "Se esperaba 'Hasta Que' después del bloque en 'Repetir'."
    *   **Severity**: Error
    *   **Example**:
        ```pseint
        Proceso Ejemplo
            Definir x Como Entero;
            x <- 0;
            Repetir
                x <- x + 1;
            // Falta 'Hasta Que <condicion>'
        FinProceso
        ```
*   **Message**: "Se esperaba 'Hacer' después de la variable en 'Segun'."
    *   **Severity**: Error
    *   **Example**:
        ```pseint
        Proceso Ejemplo
            Definir opcion Como Entero;
            opcion <- 1;
            Segun opcion // Falta 'Hacer'
                Caso 1: Escribir "Uno";
            FinSegun
        FinProceso
        ```
*   **Message**: "Cláusula 'Caso' requiere un valor o rango."
    *   **Severity**: Error
    *   **Example**:
        ```pseint
        Proceso Ejemplo
            Definir opcion Como Entero;
            opcion <- 1;
            Segun opcion Hacer
                Caso : Escribir "Vacio"; // Falta valor en Caso
            FinSegun
        FinProceso
        ```
*   **Message**: "Se esperaba ':' después del valor en 'Caso' o en 'De Otro Modo'." (More of a style warning if PSeInt is flexible)
    *   **Severity**: Warning
    *   **Example**:
        ```pseint
        Proceso Ejemplo
            Definir opcion Como Entero;
            opcion <- 1;
            Segun opcion Hacer
                Caso 1 Escribir "Uno"; // Falta ':'
                De Otro Modo Escribir "Otro"; // Falta ':'
            FinSegun
        FinProceso
        ```

## 6. Function/Subprocess Errors

These errors relate to the definition and usage of functions and subprocesses.

*   **Message**: "Nombre de <SubProceso|Funcion> '<name>' ya está en uso."
    *   **Severity**: Error
    *   **Example**:
        ```pseint
        SubProceso Saludar()
            Escribir "Hola";
        FinSubProceso

        SubProceso Saludar() // Nombre repetido
            Escribir "Adiós";
        FinSubProceso

        Proceso Principal
        FinProceso
        ```

*   **Message**: "Se esperaba '(' para la lista de parámetros en la definición de <SubProceso|Funcion>."
    *   **Severity**: Error
    *   **Example**:
        ```pseint
        SubProceso Sumar a Como Entero, b Como Entero // Faltan paréntesis
            Escribir a+b;
        FinSubProceso
        Proceso Principal
        FinProceso
        ```

*   **Message**: "Se esperaba ')' para finalizar la lista de parámetros en la definición de <SubProceso|Funcion>."
    *   **Severity**: Error
    *   **Example**:
        ```pseint
        SubProceso Sumar(a Como Entero, b Como Entero // Falta paréntesis de cierre
            Escribir a+b;
        FinSubProceso
        Proceso Principal
        FinProceso
        ```

*   **Message**: "Tipo de parámetro ausente para '<param_name>'. Se esperaba 'Como <Tipo>'."
    *   **Severity**: Error
    *   **Example**:
        ```pseint
        SubProceso Imprimir(valor) // Falta 'Como Tipo' para valor
            Escribir valor;
        FinSubProceso
        Proceso Principal
        FinProceso
        ```

*   **Message**: "Número incorrecto de argumentos al llamar a <SubProceso|Funcion> '<name>'. Se esperaban <expected_count> pero se pasaron <actual_count>."
    *   **Severity**: Error
    *   **Example**:
        ```pseint
        SubProceso Mostrar(msg Como Caracter)
            Escribir msg;
        FinSubProceso

        Proceso Principal
            Mostrar("Hola", "Mundo"); // Demasiados argumentos
        FinProceso
        ```

*   **Message**: "Tipo de argumento incorrecto para el parámetro '<param_name>' en <SubProceso|Funcion> '<name>'. Se esperaba '<expected_type>' pero se pasó '<actual_type>'."
    *   **Severity**: Error
    *   **Example**:
        ```pseint
        SubProceso ImprimirNumero(num Como Entero)
            Escribir num;
        FinSubProceso

        Proceso Principal
            ImprimirNumero("hola"); // Se pasó Caracter en lugar de Entero
        FinProceso
        ```

*   **Message**: "Variable de retorno '<var_name>' en Funcion '<func_name>' no asignada."
    *   **Severity**: Error (PSeInt functions must assign to their return variable)
    *   **Example**:
        ```pseint
        Funcion resultado = Sumar(a Como Entero, b Como Entero)
            // resultado <- a + b;  (Línea faltante)
        FinFuncion

        Proceso Principal
            Definir r Como Entero;
            r <- Sumar(5,3);
        FinProceso
        ```

*   **Message**: "Una Funcion debe tener una variable de retorno definida (ej: `Funcion var_retorno = ...`)."
    *   **Severity**: Error
    *   **Example**:
        ```pseint
        Funcion Sumar(a Como Entero, b Como Entero) // Falta "var_retorno ="
            Definir res Como Entero;
            res <- a + b;
        FinFuncion
        Proceso Principal
        FinProceso
        ```

*   **Message**: "No se puede llamar a una Funcion como si fuera un SubProceso (sin asignación)."
    *   **Severity**: Warning (or Error depending on PSeInt strictness)
    *   **Example**:
        ```pseint
        Funcion res = Calcular()
            res <- 10;
        FinFuncion
        Proceso Principal
            Calcular(); // Llamada incorrecta, el resultado no se usa
        FinProceso
        ```

*   **Message**: "No se puede asignar el resultado de un SubProceso a una variable."
    *   **Severity**: Error
    *   **Example**:
        ```pseint
        SubProceso HacerAlgo()
            Escribir "hecho";
        FinSubProceso
        Proceso Principal
            Definir x Como Entero;
            x <- HacerAlgo(); // Incorrecto, SubProceso no retorna valor
        FinProceso
        ```
*   **Message**: "Parámetro '<param_name>' pasado 'Por Referencia' a una constante o expresión."
    *   **Severity**: Error
    *   **Example**:
        ```pseint
        SubProceso Modificar(num Por Referencia Como Entero)
            num <- num + 1;
        FinSubProceso
        Proceso Principal
            Modificar(5); // 5 es una constante, no puede ser Por Referencia
        FinProceso
        ```

## 7. Array Errors

These errors relate to the declaration and usage of arrays (Dimension).

*   **Message**: "Nombre de array '<array_name>' ya está en uso."
    *   **Severity**: Error
    *   **Example**:
        ```pseint
        Proceso Ejemplo
            Definir miArray Como Entero;
            Dimension miArray[5]; // miArray ya definido como variable simple
        FinProceso
        ```

*   **Message**: "Dimensiones de array deben ser numéricas y positivas."
    *   **Severity**: Error
    *   **Example**:
        ```pseint
        Proceso Ejemplo
            Definir tam Como Caracter;
            tam <- "grande";
            Dimension miArray[tam]; // tam debe ser numérico
            Dimension otroArray[-5]; // Tamaño debe ser positivo
        FinProceso
        ```

*   **Message**: "Número incorrecto de índices para el array '<array_name>'. Se esperaban <expected_count> pero se usaron <actual_count>."
    *   **Severity**: Error
    *   **Example**:
        ```pseint
        Proceso Ejemplo
            Dimension vector[5];
            vector[2,3] <- 10; // vector es de 1 dimensión, se usan 2 índices
        FinProceso
        ```

*   **Message**: "Índice '<index_value>' fuera de rango para el array '<array_name>' (Dimensión: <size>)."
    *   **Severity**: Error (Runtime error in PSeInt, but can be caught statically if index is constant)
    *   **Example**:
        ```pseint
        Proceso Ejemplo
            Dimension miArray[5]; // Índices 0-4 o 1-5 según config
            miArray[10] <- 7; // Índice 10 está fuera de rango
        FinProceso
        ```

*   **Message**: "Índices de array deben ser de tipo Entero."
    *   **Severity**: Error
    *   **Example**:
        ```pseint
        Proceso Ejemplo
            Dimension miArray[5];
            Definir idx Como Caracter;
            idx <- "a";
            miArray[idx] <- 7; // idx debe ser Entero
        FinProceso
        ```
*   **Message**: "Declaración de 'Dimension' debe usar corchetes `[]` para los tamaños."
    *   **Severity**: Error
    *   **Example**:
        ```pseint
        Proceso Ejemplo
            Dimension miArray(5); // Debe ser miArray[5]
        FinProceso
        ```

## 8. Command/Keyword Specific Errors

*   **Message**: "Comando 'Leer' requiere una o más variables."
    *   **Severity**: Error
    *   **Example**:
        ```pseint
        Proceso Ejemplo
            Leer; // Falta la variable donde guardar la entrada
        FinProceso
        ```
*   **Message**: "Variable para 'Leer' (<variable_name>) no está definida."
    *   **Severity**: Error
    *   **Example**:
        ```pseint
        Proceso Ejemplo
            Leer x; // x no está definida
        FinProceso
        ```

*   **Message**: "Comando 'Escribir' requiere una o más expresiones."
    *   **Severity**: Warning (PSeInt might allow `Escribir;` for a newline, but typically expects arguments)
    *   **Example**:
        ```pseint
        Proceso Ejemplo
            Escribir; // Podría ser una advertencia si se espera una expresión
        FinProceso
        ```
*   **Message**: "Uso incorrecto de 'Escribir Sin Saltar'. Se espera una expresión."
    *   **Severity**: Warning (Similar to Escribir)
    *   **Example**:
        ```pseint
        Proceso Ejemplo
            Escribir Sin Saltar;
        FinProceso
        ```
*   **Message**: "Argumento para '<BuiltinFunction>' de tipo incorrecto. Se esperaba '<ExpectedType>'."
    *   **Severity**: Error
    *   **Example**:
        ```pseint
        Proceso Ejemplo
            Definir x Como Entero;
            x <- Longitud(123); // Longitud espera Caracter/Texto
        FinProceso
        ```
    *   **Note**: Applies to `Mayusculas`, `Longitud`, `Subcadena`, `ConvertirANumero`, `trunc`, `Aleatorio`.

*   **Message**: "Número incorrecto de argumentos para '<BuiltinFunction>'. Se esperaban <count>."
    *   **Severity**: Error
    *   **Example**:
        ```pseint
        Proceso Ejemplo
            Definir cad Como Caracter;
            cad <- "hola";
            cad <- Subcadena(cad, 1); // Faltan argumentos para Subcadena
        FinProceso
        ```

## 9. Miscellaneous Errors/Warnings

*   **Message**: "Caracteres inválidos o inesperados: '<character>'."
    *   **Severity**: Error
    *   **Example**:
        ```pseint
        Proceso Ejemplo
            Definir x Como Entero;
            x <- 5 @ 2; // @ es un caracter inválido aquí
        FinProceso
        ```

*   **Message**: "Comentario no cerrado o mal formado." (Less likely with `//` but for other potential comment styles)
    *   **Severity**: Error
    *   **Example**: (Hypothetical if `/* */` were supported and misused)
        ```pseint
        /* Este es un comentario
        Proceso Ejemplo
        FinProceso
        // Fin de comentario faltante */
        ```

*   **Message**: "Se recomienda usar '<CorrectKeyword>' en lugar de '<AliasKeyword>' para consistencia."
    *   **Severity**: Warning (Style suggestion)
    *   **Example**:
        ```pseint
        Algoritmo MiPrograma // Se podría sugerir 'Proceso'
            Escribir "Hola";
        FinAlgoritmo
        ```
    *   **Note**: Applies to `Algoritmo` vs `Proceso`, `SubAlgoritmo` vs `SubProceso`, `Numero`/`Real` vs `Entero` if context allows, `Booleano` vs `Logico`, `Texto`/`Cadena` vs `Caracter`.

*   **Message**: "El nombre del <Proceso|Algoritmo> principal no puede ser igual al de un <SubProceso|SubAlgoritmo|Funcion>."
    *   **Severity**: Error
    *   **Example**:
        ```pseint
        Proceso MiRutina
        FinProceso
        SubProceso MiRutina()
             Escribir "Hola";
        FinSubProceso
        ```
```
