// Usaremos este archivo para nuestro trabajo

Proceso BatallaNavalMain

    Definir nombre_jugador Como Caracter;
    Definir encontrado Como Logico;
    Definir dato Como Caracter;
    Definir datonumerico, i Como Entero;
    Definir opcionNumeros Como Cadena;
    opcionNumeros <- "1234";
    datonumerico <- 0;
    mensajeAmpliarPantalla();
    Borrar Pantalla;
    textoEstatico();
    Borrar Pantalla;
    Animacion();
    Borrar Pantalla;
    MensajeBienvenida(Nombre_Jugador);
    Borrar Pantalla;

    Repetir
        Escribir "Hola soldado ", nombre_jugador, ". Este es el Menu del juego.";
        Escribir "";
        Escribir "1- Jugar"; // aqui se redirige al subalgoritmo "batallaNavalLoop"
        Escribir "2- Reglas del juego"; // aqui se redirige al ReglasDelJuego
        Escribir "3- Creditos"; // aqui se redirige al subalgoritmo "creditos"
        Escribir "4- Salir"; // aqui se redirige al subalgoritmo "salir"
        Escribir Sin Saltar "Digite la opcion de menu:";
        Leer dato;
        encontrado <- Falso;
        datonumerico <- 0;
        i <- 0;

        // Busqueda secuencial
        Mientras (i < 4 Y encontrado = Falso) Hacer
            Si (SubCadena(opcionNumeros, i, i) == dato) Entonces
                encontrado <- Verdadero;
                datonumerico <- ConvertirANumero(dato);
                Escribir datonumerico;
            FinSi
            i <- i + 1;
        FinMientras
        // 		Escribir "Se equivoc� de opcion de menu.";
        // 		escribir "";
        Borrar Pantalla;

        Segun datonumerico Hacer
            1:
            batallaNavalLoop(nombre_jugador);
            2:
            ReglasDelJuego();
            3:
            Creditos();
            4:
            finDelJuego(nombre_jugador);
        De Otro Modo:
            Escribir "Se equivoc� de opcion de menu.";
        FinSegun
    Hasta Que datonumerico == 4
FinProceso

SubAlgoritmo mensajeAmpliarPantalla

    Definir tecla Como Caracter;
    Escribir "                    PARA UNA MEJOR EXPERIENCIA DE JUEGO";
    Escribir "                 ABRA A PANTALLA COMPLETA Y PRESIONE ENTER";
    Leer TECLA;
    Borrar Pantalla;
FinSubAlgoritmo

// En este SubProceso mostramos la portada de presentacion
SubAlgoritmo textoEstatico

    Definir tecla Como Caracter;
    // Esta seria la pantalla inicial a modo de caratula

    Escribir "";
    Escribir "";
    Escribir "";
    Escribir "                                                                            Universidad Tecnologica Nacional";
    Escribir "";
    Escribir "                                                                              Facultad Regional San Rafael";
    Escribir "";
    Escribir "";
    Escribir "                                                                                  Proyecto Integrador";
    Escribir "";
    Escribir "                                                                                  T.U.P COHORTE 2024";

    Escribir "";
    Escribir "";
    Escribir "";

    Escribir "                                                     ............................................................................. ";
    Escribir "                                                     ............................................................................. ";
    Escribir "                                                     ............................................................................. ";
    Escribir "                                                     ... GOLDEN       ****  ****  ****    **    ****  *    *  *****      *     ... ";
    Escribir "                                                     ...      BYTES   *  *  *  *  *      *   *  *     * *  *    *       * *    ... ";
    Escribir "                                                     ...              ****  ****  ***      \    ***   *  * *    *      *   *   ... ";
    Escribir "                                                     ...              *     * *   *     *   *   *     *    *    *     *******  ... ";
    Escribir "                                                     ...              *     *  *  ****    **    ****  *    *    *    *       * ... ";
    Escribir "                                                     ............................................................................. ";
    Escribir "                                                     ............................................................................. ";
    Escribir "                                                     ............................................................................. ";
    Escribir "";
    Escribir "";
    Escribir "                                                                       Presione Enter para continuar...";
    Leer tecla;
FinSubAlgoritmo

// Este subproceso es una animacion que muestra el nombre de nuestro juego
SubProceso Animacion

    Definir logo Como Caracter;
    Definir i, j Como Entero;
    Definir tecla Como Caracter;

    Dimension logo[24]; // Definimos un arreglo que contenga los caracteres que formaran la animacion

    // cargamos manualmente el arreglo para lograr el efecto deseado

    logo[1] <- "      8 888888888o           .8.    8888888 8888888888    .8.          8 8888         8 8888                  .8.";
    logo[2] <- "      8 8888    `88.        .888.         8 8888         .888.         8 8888         8 8888                 .888.";
    logo[3] <- "      8 8888     `88       :88888.        8 8888        :88888.        8 8888         8 8888                :88888.";
    logo[4] <- "      8 8888     ,88      . `88888.       8 8888       . `88888.       8 8888         8 8888               . `88888.";
    logo[5] <- "      8 8888.   ,88?     .8. `88888.      8 8888      .8. `88888.      8 8888         8 8888              .8. `88888.";
    logo[6] <- "      8 8888888888      .8`8. `88888.     8 8888     .8`8. `88888.     8 8888         8 8888             .8`8. `88888.";
    logo[7] <- "      8 8888    `88.   .8? `8. `88888.    8 8888    .8? `8. `88888.    8 8888         8 8888            .8? `8. `88888.";
    logo[8] <- "      8 8888      88  .8?   `8. `88888.   8 8888   .8?   `8. `88888.   8 8888         8 8888           .8?   `8. `88888.";
    logo[9] <- "      8 8888    ,88? .888888888. `88888.  8 8888  .888888888. `88888.  8 8888         8 8888          .888888888. `88888.";
    logo[10] <- "      8 888888888P  .8?       `8. `88888. 8 8888. 8?       `8. `88888. 8 888888888888 8 888888888888 .8?       `8. `88888.";
    logo[11] <- "                                    ";
    logo[12] <- "                                    ";
    logo[13] <- "                                    ";
    logo[14] <- "                                                                    b.             8            .8.   `8.`888b           ,8?   .8.            8 8888";
    logo[15] <- "                                                                    888o.          8           .888.   `8.`888b         ,8?   .888.           8 8888";
    logo[16] <- "                                                                    Y88888o.       8          :88888.   `8.`888b       ,8?   :88888.          8 8888";
    logo[17] <- "                                                                    .`Y888888o.    8         . `88888.   `8.`888b     ,8?   . `88888.         8 8888";
    logo[18] <- "                                                                    8o. `Y888888o. 8        .8. `88888.   `8.`888b   ,8?   .8. `88888.        8 8888";
    logo[19] <- "                                                                    8`Y8o. `Y88888o8       .8`8. `88888.   `8.`888b ,8?   .8`8. `88888.       8 8888";
    logo[20] <- "                                                                    8   `Y8o. `Y8888      .8? `8. `88888.   `8.`888b8?   .8? `8. `88888.      8 8888";
    logo[21] <- "                                                                    8      `Y8o. `Y8     .8?   `8. `88888.   `8.`888?   .8?   `8. `88888.     8 8888";
    logo[22] <- "                                                                    8         `Y8o.`    .888888888. `88888.   `8.`8?   .888888888. `88888.    8 8888";
    logo[23] <- "                                                                    8            `Yo   .8?       `8. `88888.   `8.`   .8?       `8. `88888.   8 888888888888";

    // Para hacer aparecer el logo gradualmente recorremos el arreglo y le damos un tiempo de 150 milisegundos
    // de duracion
    Para i <- 1 Hasta 23 Hacer
        Escribir "";
        Borrar Pantalla;
        Para j <- 1 Hasta i Hacer
            Si j <= Longitud(logo[j]) Entonces
                Escribir logo[j];
            FinSi
        FinPara
        Esperar 150 Milisegundos;
    FinPara

    // Para hacer desaparecer el logo gradualmente recorremos el arreglo de manera inversa dandole el valor de -1 al paso
    Para i <- 23 Hasta 1 Con Paso -1 Hacer
        Borrar Pantalla;
        Escribir "";
        Para j <- 1 Hasta i Hacer
            Si j <= Longitud(logo[j]) Entonces
                Escribir logo[j];
            FinSi
        FinPara
        Esperar 200 Milisegundos;
    FinPara
    Para i <- 1 Hasta 23 Hacer
        Escribir logo[i];
    FinPara

    // escribimos un mensaje para mejorar la experiencia del jugador

    Escribir "";
    Escribir "";
    Escribir "";
    Escribir "";
    Escribir "                                                                                ***EL JUEGO COMIENZA***";

    Escribir "";
    Escribir "";
    Escribir "";
    Escribir "                                                                              Presiona Enter para continuar...";
    Leer tecla;
FinSubProceso

// Aqui Damos un Mensaje de Bienvenida al Jugador

SubProceso MensajeBienvenida (nombre_jugador Por Referencia)
    Definir confirmacion Como Caracter; // variable para Si o No
    Definir min_longitud Como Entero; // longitud minima del nombre
    min_longitud <- 3; // Longitud minima para el nombre
    Definir tecla Como Caracter;

    Escribir "";
    Escribir "";
    Escribir "";
    Escribir "";
    Escribir "";
    Escribir "                                                                              ��� Bienvenido Soldado !!!";
    Escribir "";
    Escribir "                                                                   Estas Listo y preparado para esta Gran Aventura";
    Escribir "";
    Escribir "                                                                                 Presentate Soldado ";
    Escribir "";
    Repetir

        Escribir "                                                                       Escribe Tu Nombre (m�nimo ", min_longitud, " caracteres):";
        Leer nombre_jugador;
        Si Longitud(nombre_jugador) < min_longitud Entonces
            Escribir "El nombre debe tener al menos ", min_longitud, " caracteres. Int�ntalo de nuevo.";
        Sino
            // Confirmar el nombre ingresado
            Escribir "�Es correcto el nombre ", nombre_jugador, "? (S/N):";
            Leer confirmacion;
            // Convertir la confirmaci�n a may�scula para simplificar la comparaci�n
            confirmacion <- Mayusculas(confirmacion);
        FinSi
    Hasta Que Longitud(nombre_jugador) >= min_longitud Y confirmacion = "S"
    Escribir "Nombre confirmado: ", nombre_jugador;
    Escribir "";
    Escribir "                                                             Perfecto soldado", " ", nombre_jugador, " ��� Que comience la Batalla !!!";

    Escribir "";
    Escribir "";

    Escribir "                                                                           Pesione Enter para continuar...";
    Leer tecla;
    Escribir "";
    Escribir "";
    Escribir "";
    Escribir "";
FinSubProceso

SubAlgoritmo batallaNavalLoop(nombre_jugador Por Referencia)

    // ESTAS VARIABLES  O AL MENOS LAS MATRIZ JUGADOR Y ENEMIGO VAN A TENER QUE SER PASAR POR REFERENCIA a los otrso sub algoritomos
    Definir matrizJugador, contadorBarcosEnemigo, contadorBarcosJugador, i, j Como Entero;
    Dimension matrizJugador[11, 11];
    Definir matrizEnemigo Como Entero;
    Dimension matrizEnemigo[11, 11];
    Definir ganar, perder Como Logico;
    Dimension contadorBarcosEnemigo[5], contadorBarcosJugador[5];

    // contador enemigo
    contadorBarcosEnemigo[1] <- 4; // tama�o del portaviones
    contadorBarcosEnemigo[2] <- 4; // tama�o del crucero
    contadorBarcosEnemigo[3] <- 4; // tama�o del submarino
    contadorBarcosEnemigo[4] <- 2; // tama�o de la lancha
    // Contador jugador
    contadorBarcosJugador[1] <- 4; // tama�o del portaviones
    contadorBarcosJugador[2] <- 4; // tama�o del crucero
    contadorBarcosJugador[3] <- 4; // tama�o del submarino
    contadorBarcosJugador[4] <- 2; // tama�o de la lancha

    Para i <- 0 Hasta 10 Con Paso 1 Hacer
        Para j <- 0 Hasta 10 Con Paso 1 Hacer
            Escribir Sin Saltar "    "; // centrado de la matriz margen superior
            matrizJugador[i, j] <- 0;
        FinPara
    FinPara
    mostrarTableroJugador(matrizJugador);
    Borrar Pantalla;
    IngresarPosicionBarcoJugador(matrizJugador);
    colocar_barcos_enemigo(matrizEnemigo);
    Borrar Pantalla;

    Repetir
        mostrarTableroJugadorEnemigo(matrizJugador, matrizEnemigo);
        ataqueDelJugador(matrizEnemigo, contadorBarcosEnemigo);
        ataqueDelEnemigo(matrizJugador, contadorBarcosJugador); // atacar enemigo

        i <- 1;
        ganar <- Verdadero;

        Mientras i < 5 Y (ganar == Verdadero) Hacer
            ganar <- contadorBarcosEnemigo[i] == 0;
            i <- i + 1;
        FinMientras

        perder <- Verdadero;
        i <- 1;
        Mientras i < 5 Y (perder == Verdadero) Hacer
            perder <- contadorBarcosJugador[i] == 0;
            i <- i + 1;
        FinMientras
    Hasta Que ganar O perder

    Si ganar Entonces
        Borrar Pantalla;
        Escribir "";
        Escribir "Felicitaciones ha ganado!!!";
    Sino
        Borrar Pantalla;
        Escribir "";
        Escribir "Has sido derrotado. No te rindas, vuelve a jugar";
    FinSi

    // Mostrar mensaje de agradecimiento al final del juego
    finDelJuego(nombre_jugador);
    Creditos();
FinSubAlgoritmo

// En este subproceso le mostramos el tablero que utilizara el jugador

SubAlgoritmo mostrarTableroJugador(matrizJugador Por Referencia)
    Definir i, j, filaNumeros Como Entero;
    Definir columnaLetras Como Cadena;
    columnaLetras <- " ABCDEFGHIJ";
    Dimension filaNumeros[10];
    Definir tecla Como Caracter;
    Definir esJugador Como Logico;

    Para i <- 0 Hasta 9 Con Paso 1 Hacer
        filaNumeros[i] <- i + 1;
    FinPara

    Escribir "Este es tu tablero piensa en donde ubicar tus barcos";

    Para i <- 0 Hasta 10 Con Paso 1 Hacer
        Escribir "";
        esJugador <- Verdadero;
        mostrarValor(matrizJugador, columnaLetras, filaNumeros, i, esJugador); // llamo a la funcion para mostrar una matriz
        Escribir "";
    FinPara
    Escribir "";
    Escribir "                                                                           Presiona Enter para continuar...";
    Leer tecla;
FinSubAlgoritmo

// -------------------------------------------------------------------------------------------------------------------------------------------------------

// En este subproceso le indicamos al juagdor para que coloque sus barcos en el tablero

SubAlgoritmo IngresarPosicionBarcoJugador(matriz Por Referencia)
    Definir posicion, columna, fila, i, j, size, tipo, h, formato Como Entero;
    Definir arregloLetras, dato, arregloNumeros Como Caracter;
    Definir columnaLetras, columnaNumeros Como Cadena;
    Definir esValido, encontrado, posicionOcupada Como Logico;
    esValido <- Verdadero;
    Dimension arregloLetras(11);
    Dimension arregloNumeros(11);
    columnaLetras <- " ABCDEFGHIJ";
    columnaNumeros <- " 1234567890";
    columna <- 12;
    fila <- 12;

    Para i <- 0 Hasta 10 Con Paso 1 Hacer
        arregloNumeros[i] <- SubCadena(columnaNumeros, i, i);
    FinPara

    Para j <- 0 Hasta 10 Con Paso 1 Hacer
        arregloLetras[j] <- SubCadena(columnaLetras, j, j);
    FinPara

    // Arreglo para almacenar los tama�os y formatos de los barcos enemigos
    Definir barco Como Entero;
    Definir formatos Como Entero;
    Definir nombreDeBarco Como Caracter;
    Dimension nombreDeBarco[5];
    Dimension barco[5];
    Dimension formatos[5];
    Definir tecla Como Caracter;

    // Nombres e barco
    nombreDeBarco[1] <- "portaviones"; // tama�o del portaviones
    nombreDeBarco[2] <- "crucero"; // tama�o del crucero
    nombreDeBarco[3] <- "submarino"; // tama�o del submarino
    nombreDeBarco[4] <- "lancha"; // tama�o de la lancha

    // Definir tama�os y formatos para cada tipo de barco
    barco[1] <- 4; // tama�o del portaviones
    barco[2] <- 4; // tama�o del crucero
    barco[3] <- 4; // tama�o del submarino
    barco[4] <- 2; // tama�o de la lancha

    formatos[1] <- 9; // formato del portaviones
    formatos[2] <- 8; // formato del crucero
    formatos[3] <- 7; // formato del submarino
    formatos[4] <- 6; // formato de la lancha

    // Colocar cada barco autom�ticamente
    Para tipo <- 1 Hasta 4 Hacer
        Repetir
            Escribir Sin Saltar "Coloque el ", nombreDeBarco[tipo], " en el tablero, ", "con tama�o ", barco[tipo], " .";

            h <- 0;
            // Solicitar columna al usuario
            Mientras h = 0 Hacer
                h <- 1;
                mostrarTableroJugador(matriz);

                Escribir "elija en que columna quiere colocar su barco (1-2-3-4-5-6-7-8-9-10) ";
                Leer dato;

                encontrado <- Falso;
                i <- 0;
                // Busqueda secuencial
                Mientras (i < 11 Y encontrado = Falso) Hacer
                    Si (arregloNumeros[i] = dato) Entonces
                        encontrado <- Verdadero;
                        columna <- i;
                    FinSi
                    i <- i + 1;
                FinMientras
                Si dato = "10" Entonces
                    columna <- 10;
                FinSi
                Si columna < 1 O columna > 11 Entonces
                    Escribir "el valor dado esta fuera del rango";
                    h <- 0;
                FinSi
            FinMientras

            // solicitar fila
            h <- 0;
            Mientras h = 0 Hacer
                h <- 1;
                Escribir "elija en que fila quiere colocar su barco (A-B-C-D-E-F-G-H-I-J) ";
                Leer dato;
                dato <- Mayusculas(dato);
                encontrado <- Falso;
                j <- 0;
                // Busqueda secuencial
                Mientras (j < 11 Y encontrado = Falso) Hacer
                    Si (arregloLetras[j] = dato) Entonces
                        encontrado <- Verdadero;
                        fila <- j;
                    FinSi
                    j <- j + 1;
                FinMientras

                Si fila < 1 O fila > 11 Entonces
                    Escribir "el valor dado esta fuera del rango";
                    h <- 0;
                FinSi
            FinMientras

            Si (columna + barco[tipo]) > 11 Entonces

                Escribir "El ", nombreDeBarco[tipo], " se ubicaria fuera del tablero, elija otra ubicacion ";
                Escribir "";
            Sino
                posicionOcupada <- Falso;
                i <- 0;
                Mientras i < barco[tipo] Y posicionOcupada == Falso Hacer
                    Si matriz[fila, columna + i] <> 0 Entonces
                        posicionOcupada <- Verdadero;
                    FinSi
                    i <- i + 1;
                FinMientras
                Si (posicionOcupada) Entonces
                    Escribir "Ya hay un barco en esta posicion, elija otra.";
                    Escribir "";
                FinSi
            FinSi
        Hasta Que ((columna + barco[tipo]-1) < 11) Y (posicionOcupada == Falso)

        // Colocar el barco en la matriz
        h <- 0;
        Para i <- 0 Hasta barco[tipo]-1 Hacer
            matriz[fila, columna + h] <- formatos[tipo];
            h <- h + 1;
        FinPara

        Escribir Sin Saltar "El barco a sido colocado en la siguiente ubicacion del tablero (", columna, ",", arregloLetras[fila], "):";
        Escribir "";
        mostrarTableroJugador(matriz);
        Borrar Pantalla;
    FinPara
FinSubAlgoritmo

SubAlgoritmo mostrarTableroJugadorEnemigo(matrizJugador Por Referencia, matrizEnemigo Por Referencia)
    Definir i, j, filaNumeros Como Entero;
    Definir columnaLetras Como Cadena;
    columnaLetras <- " ABCDEFGHIJ";
    Dimension filaNumeros[10];
    Definir esJugador Como Logico;
    Definir tecla Como Caracter;

    Para i <- 0 Hasta 9 Con Paso 1 Hacer
        filaNumeros[i] <- i + 1;
    FinPara

    Escribir "                                Este es tu tablero                                                             Este es el tablero del enemigo";

    Para i <- 0 Hasta 10 Con Paso 1 Hacer
        Escribir "";
        esJugador <- Verdadero;
        mostrarValor(matrizJugador, columnaLetras, filaNumeros, i, esJugador); // llamo a la funcion para mostrar una matriz
        esJugador <- Falso;
        mostrarValor(matrizEnemigo, columnaLetras, filaNumeros, i, esJugador);
        Escribir "";
    FinPara

    Escribir "";
    Escribir "                                                                           Presiona Enter para continuar...";
    Leer tecla;
FinSubAlgoritmo

SubAlgoritmo mostrarValor(matriz Por Referencia, columnaLetras Por Referencia, filaNumeros Por Referencia, i Por Valor, esjugador Por Valor)
    Definir j Como Entero;

    Escribir Sin Saltar "             "; // aqui centramos la matriz margen de izquierda a derecha
    Escribir Sin Saltar SubCadena(columnaLetras, i, i);
    Escribir Sin Saltar "     "; // separacion de la matriz de la primera columna

    Para j <- 0 Hasta 9 Con Paso 1 Hacer
        Si i == 0 Entonces // si true muestro los numeros
            Escribir Sin Saltar filaNumeros[j];
            Escribir Sin Saltar "     "; // separacion entre los numeros
        Sino
            // Aqui imprimimos matriz (MODO DEBUG) DESCOMITEAR ESTAS 2 LINEAS Y COMMITEAR LAS OTRAS

            Si esJugador Entonces
                // 				Escribir Sin Saltar matriz[i,j+1]; // MODO DEBUG
                // 				Escribir Sin Saltar "     "; // MODO DEBUG

                Si matriz[i, j + 1] == -1 Entonces
                    Escribir Sin Saltar "A"; // 
                    Escribir Sin Saltar "     ";
                FinSi
                Si matriz[i, j + 1] == 0 Entonces
                    Escribir Sin Saltar "~"; // 
                    Escribir Sin Saltar "     "; // separacion del simbolo agua
                FinSi
                Si matriz[i, j + 1] < -1 Entonces
                    Escribir Sin Saltar "*"; // 
                    Escribir Sin Saltar "     ";
                FinSi
                Si matriz[i, j + 1] == 6 Entonces
                    Escribir Sin Saltar "L"; // 
                    Escribir Sin Saltar "     ";
                FinSi
                Si matriz[i, j + 1] == 7 Entonces
                    Escribir Sin Saltar "S"; // 
                    Escribir Sin Saltar "     ";
                FinSi
                Si matriz[i, j + 1] == 8 Entonces
                    Escribir Sin Saltar "C"; // 
                    Escribir Sin Saltar "     ";
                FinSi
                Si matriz[i, j + 1] == 9 Entonces
                    Escribir Sin Saltar "P"; // 
                    Escribir Sin Saltar "     ";
                FinSi
            Sino
                // 				Escribir Sin Saltar matriz[i,j+1]; // MODO DEBUG
                // 				Escribir Sin Saltar "     "; // MODO DEBUG
                Si matriz[i, j + 1] == -1 Entonces
                    Escribir Sin Saltar "A"; // 
                    Escribir Sin Saltar "     ";
                FinSi
                Si matriz[i, j + 1] >= 0 Entonces
                    Escribir Sin Saltar "~"; // 
                    Escribir Sin Saltar "     "; // separacion del simbolo agua
                FinSi
                Si matriz[i, j + 1] == -6 Entonces
                    Escribir Sin Saltar "L"; // 
                    Escribir Sin Saltar "     ";
                FinSi
                Si matriz[i, j + 1] == -7 Entonces
                    Escribir Sin Saltar "S"; // 
                    Escribir Sin Saltar "     ";
                FinSi
                Si matriz[i, j + 1] == -8 Entonces
                    Escribir Sin Saltar "C"; // 
                    Escribir Sin Saltar "     ";
                FinSi
                Si matriz[i, j + 1] == -9 Entonces
                    Escribir Sin Saltar "P"; // 
                    Escribir Sin Saltar "     ";
                FinSi
            FinSi
        FinSi
    FinPara
FinSubAlgoritmo

// Esta funcion permite atacar al enemigo
SubAlgoritmo ataqueDelJugador(matrizEnemigo Por Referencia, contadorBarcosEnemigo Por Referencia)
    Escribir "Ingresa la coordenada para atacar al enemigo";
    Definir posicion, columna, fila, i, j, h Como Entero;
    Definir arregloLetras, dato, arregloNumeros Como Caracter;
    Definir columnaLetras, columnaNumeros Como Cadena;
    Definir encontrado Como Logico;
    Dimension arregloLetras(11);
    Dimension arregloNumeros(11);
    columnaLetras <- " ABCDEFGHIJ";
    columnaNumeros <- " 1234567890";
    columna <- 12;
    fila <- 12;

    Para i <- 0 Hasta 10 Con Paso 1 Hacer
        arregloNumeros[i] <- SubCadena(columnaNumeros, i, i);
    FinPara

    Para j <- 0 Hasta 10 Con Paso 1 Hacer
        arregloLetras[j] <- SubCadena(columnaLetras, j, j);
    FinPara

    h <- 0;
    // Solicitar columna al usuario
    Mientras h = 0 Hacer
        h <- 1;

        Escribir "elija en que columna quiere disparar al barco Enemigo (1-2-3-4-5-6-7-8-9-10) ";
        Leer dato;

        encontrado <- Falso;
        i <- 0;
        // Busqueda secuencial
        Mientras (i < 11 Y encontrado = Falso) Hacer
            Si (arregloNumeros[i] = dato) Entonces
                encontrado <- Verdadero;
                columna <- i;
            FinSi
            i <- i + 1;
        FinMientras
        Si dato = "10" Entonces
            columna <- 10;
        FinSi
        Si columna < 1 O columna > 11 Entonces
            Escribir "el valor dado esta fuera del rango";
            h <- 0;
        FinSi
    FinMientras

    // solicitar fila
    h <- 0;
    Mientras h = 0 Hacer
        h <- 1;
        Escribir "elija en que fila quiere disparar al barco enemigo (A-B-C-D-E-F-G-H-I-J) ";
        Leer dato;
        dato <- Mayusculas(dato);
        encontrado <- Falso;
        j <- 0;
        // Busqueda secuencial
        Mientras (j < 11 Y encontrado = Falso) Hacer
            Si (arregloLetras[j] = dato) Entonces
                encontrado <- Verdadero;
                fila <- j;
            FinSi
            j <- j + 1;
        FinMientras

        Si fila < 1 O fila > 11 Entonces
            Escribir "el valor dado esta fuera del rango";
            h <- 0;
        FinSi
    FinMientras

    Borrar Pantalla;
    Escribir "Desplegando ataque en las coordenadas ", columna, " : ", dato;
    Escribir "";

    // Verficar coordenadas
    Segun matrizEnemigo[fila, columna] Hacer
        0:
        Escribir "Le has dado al Agua";
        Escribir "";
        matrizEnemigo[fila, columna] <- -1; // -1 representa agua
        6: // formato de la lancha
        matrizEnemigo[fila, columna] <- -6; // representa lancha da�ado
        Si contadorBarcosEnemigo[4] == 1 Entonces
            Escribir "Excelente soldado ha destruido la lancha del enemigo!";
            Escribir "";
            contadorBarcosEnemigo[4] <- contadorBarcosEnemigo[4] - 1;
        Sino
            Escribir "Genial soldado, le diste a la lancha del enemigo";
            Escribir "";
            contadorBarcosEnemigo[4] <- contadorBarcosEnemigo[4] - 1;
        FinSi
        7: // formato del submarino
        matrizEnemigo[fila, columna] <- -7; // representa submarino da�ado
        Si contadorBarcosEnemigo[3] == 1 Entonces
            Escribir "Excelente soldado ha destruido el submarino del enemigo!";
            Escribir "";
            contadorBarcosEnemigo[3] <- contadorBarcosEnemigo[3] - 1;
        Sino
            Escribir "Genial soldado, le diste al submarino del enemigo";
            Escribir "";
            contadorBarcosEnemigo[3] <- contadorBarcosEnemigo[3] - 1;
        FinSi
        8: // formato del crucero
        matrizEnemigo[fila, columna] <- -8; // representa crucero da�ado
        Si contadorBarcosEnemigo[2] == 1 Entonces
            Escribir "Excelente soldado ha destruido el crucero del enemigo!";
            Escribir "";
            contadorBarcosEnemigo[2] <- contadorBarcosEnemigo[2] - 1;
        Sino
            Escribir "Genial soldado, le diste al crucero del enemigo";
            Escribir "";
            contadorBarcosEnemigo[2] <- contadorBarcosEnemigo[2] - 1;
        FinSi
        9: // formato del portaviones
        matrizEnemigo[fila, columna] <- -9; // representa portaviones da�ado
        Si contadorBarcosEnemigo[1] == 1 Entonces
            Escribir "Excelente soldado ha destruido el portaviones del enemigo!";
            Escribir "";
            contadorBarcosEnemigo[1] <- contadorBarcosEnemigo[1] - 1;
        Sino
            Escribir "Genial soldado, le diste al portaviones del enemigo.";
            Escribir "";
            contadorBarcosEnemigo[1] <- contadorBarcosEnemigo[1] - 1;
        FinSi

    De Otro Modo:
        Escribir "Ya has atacado aqui, turno del enemigo";
        Escribir "";
    FinSegun
FinSubAlgoritmo

// ---------------------------------------------------------------------------------------------------------------------------------------------------

// Esta funcion permite que el enemigo ataque
SubAlgoritmo ataqueDelEnemigo(matrizJugador Por Referencia, contadorBarcosJugador Por Referencia)

    Definir posicion, columna, fila, i, j Como Entero;
    Definir arregloLetras, dato, aux Como Caracter;
    Definir columnaLetras Como Cadena;
    Definir encontrado Como Logico;
    Definir letra Como Caracter;
    Dimension arregloLetras(11);

    columnaLetras <- " ABCDEFGHIJ";

    Para i <- 0 Hasta 10 Con Paso 1 Hacer
        arregloLetras[i] <- SubCadena(columnaLetras, i, i);
    FinPara

    Repetir
        // Tomar valores al azar de filas y columnas para atacar
        columna <- Aleatorio(1, 10);
        dato <- SubCadena(columnaLetras, i, i);

        dato <- Mayusculas(dato);
        encontrado <- Falso;
        fila <- Aleatorio(1, 10);
    Hasta Que matrizJugador[fila, columna] >= 0

    i <- 1; //  Empezamos desde el 1 para no contar al espacio como encontrado
    // Busqueda secuencial
    Mientras (i < 11 Y encontrado = Falso) Hacer
        Si (arregloLetras[i] = dato) Entonces
            encontrado <- Verdadero;
            fila <- i;
        FinSi
        i <- i + 1;
    FinMientras

    // Verficar coordenadas
    Segun matrizJugador[fila, columna] Hacer
        0:
        Escribir "El enemigo le ha dado al Agua";
        Escribir "";
        matrizJugador[fila, columna] <- -1; // -1 representa agua
        6: // formato de la lancha
        matrizJugador[fila, columna] <- -6; // representa lancha da�ado
        Si contadorBarcosJugador[4] == 1 Entonces
            Escribir "El enemigo a destruido tu Lancha";
            Escribir "";
            contadorBarcosJugador[4] <- contadorBarcosJugador[4] - 1;
        Sino
            Escribir "El enemigo ha da�ado tu Lancha";
            Escribir "";
            contadorBarcosJugador[4] <- contadorBarcosJugador[4] - 1;
        FinSi
        7: // formato del submarino
        matrizJugador[fila, columna] <- -7; // representa submarino da�ado
        Si contadorBarcosJugador[3] == 1 Entonces
            Escribir "El enemigo ha destruido tu Submarino";
            Escribir "";
            contadorBarcosJugador[3] <- contadorBarcosJugador[3] - 1;
        Sino
            Escribir "El enemigo ha da�ado tu Submarino";
            Escribir "";
            contadorBarcosJugador[3] <- contadorBarcosJugador[3] - 1;
        FinSi
        8: // formato del crucero
        matrizJugador[fila, columna] <- -8; // representa crucero da�ado
        Si contadorBarcosJugador[2] == 1 Entonces
            Escribir "El enemigo ha destruido tu Crucero";
            Escribir "";
            contadorBarcosJugador[2] <- contadorBarcosJugador[2] - 1;
        Sino
            Escribir "El enemigo a da�ado tu Crucero";
            Escribir "";
            contadorBarcosJugador[2] <- contadorBarcosJugador[2] - 1;
        FinSi
        9: // formato del portaviones
        matrizJugador[fila, columna] <- -9; // representa portaviones da�ado
        Si contadorBarcosJugador[1] == 1 Entonces
            Escribir "El enemigo ha destruido tu Portaviones";
            Escribir "";
            contadorBarcosJugador[1] <- contadorBarcosJugador[1] - 1;
        Sino
            Escribir "El enemigo ha da�ado tu Portaviones";
            Escribir "";
            contadorBarcosJugador[1] <- contadorBarcosJugador[1] - 1;
        FinSi

    De Otro Modo:
    FinSegun
FinSubAlgoritmo

SubAlgoritmo colocar_barcos_enemigo(matrizEnemigo Por Referencia)
    Definir columna, fila, i, j, tipo, h Como Entero;

    // Inicializar la matriz con agua (0 representa agua)
    Para i <- 1 Hasta 10 Hacer
        Para j <- 1 Hasta 10 Hacer
            matrizEnemigo[i, j] <- 0;
        FinPara
    FinPara

    // Arreglo para almacenar los tama�os y formatos de los barcos enemigos
    Definir barco Como Entero;
    Definir formatos Como Entero;
    Dimension barco[5];
    Dimension formatos[5];
    Definir posicionOcupada Como Logico;
    Definir tecla Como Caracter;

    // Definir tama�os y formatos para cada tipo de barco
    barco[1] <- 4; // tama�o del portaviones
    barco[2] <- 4; // tama�o del crucero
    barco[3] <- 4; // tama�o del submarino
    barco[4] <- 2; // tama�o de la lancha

    formatos[1] <- 9; // formato del portaviones
    formatos[2] <- 8; // formato del crucero
    formatos[3] <- 7; // formato del submarino
    formatos[4] <- 6; // formato de la lancha

    // Colocar cada barco autom�ticamente
    Para tipo <- 1 Hasta 4 Hacer
        // Establece ubicaci�n aleatoria dentro de los l�mites del tablero
        // SERIA UN CHECK DE LA VARIABLE COLUMNA DE ARRIBA MAS LAS QUE TIENE QUE SER COLOCADAS
        // si el lugar es en columna i y lugar en columna i +1 +2+ +4 0 hago algo
        Repetir
            columna <- Aleatorio(1, 10 - barco[tipo] + 1);
            fila <- Aleatorio(1, 10);
            posicionOcupada <- Falso;
            Si (columna + barco[tipo]) > 11 Entonces
                posicionOcupada <- Verdadero;
            Sino
                i <- 0;
                Mientras i < barco[tipo] Y posicionOcupada == Falso Hacer
                    Si matrizEnemigo[fila, columna + i] <> 0 Entonces
                        posicionOcupada <- Verdadero;
                    FinSi
                    i <- i + 1;
                FinMientras
            FinSi
        Hasta Que posicionOcupada == Falso
        // Colocar el barco en la matriz
        h <- 0;

        Para i <- 0 Hasta barco[tipo]-1 Hacer
            matrizEnemigo[fila, columna + h] <- formatos[tipo];
            h <- h + 1;
        FinPara
    FinPara

    // Se le indica al jugador que presinando enter se colocaran
    // los barcos del enemigo en el tablero

    Escribir " El enemigo colocara sus barcos en el tablero";
    Escribir " Presione ENTER para continuar";
    Leer tecla;

    // Mostrar la matriz con los barcos colocados autom�ticamente
    Escribir "Los barcos han sido colocados correctamente:";
    Escribir "";

    Escribir "";
    Escribir " Presione ENTER para continuar";
    Leer tecla;
    Escribir "";
FinSubAlgoritmo

SubAlgoritmo finDelJuego(nombre_jugador Por Referencia)
    Definir tecla Como Caracter;
    // Mostrar mensaje de agradecimiento al usuario
    Escribir "";
    Escribir "�Gracias por jugar, ", nombre_jugador, "! Esperamos que hayas disfrutado del juego.";
    Escribir "Recuerda: Si lo puedes imaginar, lo puedes programar.";
    Escribir "Ariel Bentancud";
    Escribir "";
    Escribir "                                                                           Presiona enter para continuar...";
    Leer tecla;
    Borrar Pantalla;
FinSubAlgoritmo

SubAlgoritmo ReglasDelJuego

    Escribir "===========================================================================================================================================================================================";
    Escribir "                                                                                    Reglas del juego";
    Escribir "===========================================================================================================================================================================================";
    Escribir "";
    Escribir " Las reglas de la batalla naval son";
    Escribir "";
    Escribir " CONDICIONES INICIALES:";
    Escribir " Cantidad de jugadores: 2 jugadores";
    Escribir " Para iniciar el juego cada jugador debe tener: ";
    Escribir " 1 Portaaviones , 1 crucero , 1 submarino";

    Escribir "";
    Escribir " COMIENZO DEL JUEGO";
    Escribir " 1 - Los jugadores eligen quien inicia el ataque";
    Escribir " 2 - Cada jugador coloca sus barcos horizontal o verticalmente (no en diagonal) ";
    Escribir " 3 - Cuando hayan sido colocados todos los barcos anuncian LISTO, a partir de ese momento no se pueden cambiar los barcos de posici�n.";
    Escribir "";
    Escribir " COMIENZA EL COMBATE";
    Escribir " 1 - El jugador que primero dijo LISTO, abre el fuego ingresando las coordenadas (compuesta por una letra y un numero) tratando de alcanzar un barco enemigo, luego lo har� su ";
    Escribir "      contrincante y as� sucesivamente.";
    Escribir " 2 - El disparo es anunciado con una Letra y un N�mero que corresponden a una coordenada del tablero enemigo localizado por la convergencia entre la Letra y el N�mero de su base.";
    Escribir " 3 - El atacado deber� informar su situaci�n: TOCADO, si el disparo fue certero � AGUA, si el disparo fue errado y el tipo de barco alcanzado (Portaaviones, Submarinos, etc).";
    Escribir "";
    Escribir " MARCACI�N";
    Escribir " 1 - Despu�s que el jugador haya efectuado el disparo y sepa si ha acertado o no, podr� ir visualizando los aciertos, �sto le servir� de referencia y evitar� repetir los disparos";
    Escribir "     a los mismos puntos.";
    Escribir " 2 - No se marcan los tiros fallidos del adversario pero s� los impactos.";
    Escribir "";
    Escribir " HUNDIR LOS BARCOS";
    Escribir " 1 - Cuando un barco haya recibido tantos impactos como agujeros tiene, se considera HUNDIDO y deber� ser retirado de la base debiendo ser anunciado al oponente.";
    Escribir " 2 - Los jugadores deben ser honestos anunciando los impactos recibidos, en caso de duda o posible equivocaci�n se solicita tregua y se revisan los disparos realizados hasta el momento.";

    Escribir "     Ser� ganador el primer jugador que hunda los cuatro barcos de su oponente.";
    Escribir "";
    Escribir "                                                                                       �A JUGAR!";

    Escribir "";
FinSubAlgoritmo

SubAlgoritmo Creditos

    Definir tecla Como Caracter;

    Escribir "                                                    ===================================================";
    Escribir "                                                                        Cr�ditos     ";
    Escribir "                                                    ===================================================";
    Escribir "                                                             Desarrollado por:**GOLDEN BYTES** ";
    Escribir "                                                              - Maxi Montenegro";
    Escribir "                                                              - Irene Machuca";
    Escribir "                                                              - Valentin Felipe";
    Escribir "                                                              - Felipe Landi";
    Escribir "                                                              - Leonardo Gomez ";
    Escribir "                                                              - Ezequiel Quiroz";
    Escribir "                                                              - Franco Poblete";
    Escribir "";
    Escribir "                                                             Agradecimientos especiales a:";
    Escribir "                                                              - Profesor Ariel Betancud";
    Escribir "                                                              - Profesora Natalia Lucero";
    Escribir "                                                              - Profesor Osvaldo Giordanini";
    Escribir "                                                    ===================================================";
    Escribir "                                                                 � 2024 Golden Bytes";
    Escribir "                                                             Todos los derechos reservados.";
    Escribir "                                                      Este juego y su contenido no pueden ser copiados,";
    Escribir "                                                      distribuidos o utilizados sin autorizaci�n previa.";
    Escribir "                                                    ===================================================";
    Escribir "                                                       PRESIONE ENTER PARA VOLVER AL MENU PRINCIPAL";
    Leer tecla;
    Borrar Pantalla;
FinSubAlgoritmo