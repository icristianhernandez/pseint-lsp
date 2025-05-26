Algoritmo TestErrores
    // Error 1: Variable no declarada
    resultado <- variable_no_declarada + 5
    
    // Error 2: Tipos incompatibles
    Definir numero Como Entero
    numero <- "texto"
    
    // Error 3: Función no definida
    valor <- funcionInexistente(10)
    
    // Error 4: Bloque no cerrado
    Si numero > 0 Entonces
        Escribir "Positivo"
    // Falta FinSi
    
FinAlgoritmo
