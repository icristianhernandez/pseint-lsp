Algoritmo ErroresBasicos
    // Archivo simple con errores básicos
    
    // Error 1: Variable no declarada
    Escribir variable_inexistente
    
    // Error 2: Variable declarada pero no usada
    Definir sin_uso Como Entero
    
    // Error 3: Bloque mal cerrado
    Si verdadero Entonces
        Escribir "Hola"
    // Falta FinSi
    
    // Error 4: Tipo incompatible
    Definir num Como Entero
    num <- "texto"
    
    // Error 5: Función no definida
    resultado <- funcionNoExiste(5)
    
FinAlgoritmo
