Algoritmo TestErrores
    // Este archivo contiene varios tipos de errores para probar los diagnósticos
    
    // 1. Variables no declaradas
    Escribir x + y  // x e y no están declaradas
    
    // 2. Variables declaradas pero no utilizadas
    Definir variable_no_usada Como Entero
    Definir otra_variable_sin_uso Como Real
    
    // 3. Bloques mal cerrados
    Si verdadero Entonces
        Escribir "En bloque if"
        Para i <- 1 Hasta 5 Hacer
            Escribir i
        // Falta FinPara
    // Falta FinSi
    
    // 4. Tipos incompatibles
    Definir numero Como Entero
    Definir texto Como Caracter
    numero <- "esto es texto"  // Asignación de tipo incompatible
    texto <- 123  // Asignación de tipo incompatible
    
    // 5. Funciones/procedimientos no definidos
    resultado <- funcionInexistente(5, 10)
    procedimientoInexistente(numero)
    
    // 6. Problemas con arrays
    Definir arreglo Como Entero
    arreglo[1] <- 5  // Usar como array sin declarar dimensiones
    
    // 7. Parámetros incorrectos en funciones built-in
    Escribir RC(2, 3, 4)  // RC solo toma 1 parámetro
    Escribir Subcadena()  // Subcadena requiere parámetros
    
    // 8. Variables redefinidas
    Definir contador Como Entero
    Definir contador Como Real  // Redefinición de variable
    
    // 9. Uso de variables antes de inicialización
    Definir valor Como Entero
    Si valor > 0 Entonces  // Usando valor sin inicializar
        Escribir "Positivo"
    FinSi
    
    // 10. Problemas con estructuras de control
    Mientras condicion_inexistente Hacer  // Variable no definida
        Escribir "En bucle"
    FinMientras
    
    // 11. Casos de switch sin valor por defecto
    Segun numero Hacer
        1: Escribir "Uno"
        2: Escribir "Dos"
        // Falta caso por defecto
    FinSegun
    
    // 12. Variables de bucle para mal utilizadas
    Para j <- 1 Hasta 10 Hacer
        j <- j + 2  // Modificar variable de control del bucle
    FinPara
    
    // 13. Operaciones con tipos incorrectos
    Definir booleano Como Logico
    booleano <- verdadero
    resultado_incorrecto <- booleano + numero  // Suma entre lógico y entero
    
    // 14. Funciones que no retornan valor
    Funcion miFuncion(parametro)
        Escribir parametro
        // Falta sentencia de retorno
    FinFuncion
    
    // 15. Llamadas recursivas sin caso base
    Funcion factorial(n)
        retorno <- n * factorial(n-1)  // Sin caso base, recursión infinita
    FinFuncion
    
FinAlgoritmo
