Funcion resultado <- pagar(tasaBCV, monto)
    Definir resultado Como Real
    resultado <- monto
    Definir opcion Como Cadena
    Definir pago Como Real
    Definir entradaPago Como Caracter
    Definir salir, entradaValida Como Logico
    Definir contadorPuntos, contadorComas, i Como Entero
    
    salir <- Falso
    
    Repetir
        Limpiar Pantalla
        Escribir "TOTAL PENDIENTE: ", resultado, "$ (", resultado*tasaBCV, " BS)"
        Escribir "*----------------- METODOS DE PAGO ----------------------*"
        Escribir "| 1. TRANSFERENCIA                                       |"
        Escribir "| 2. PAGO MOVIL                                          |"
        Escribir "| 3. EFECTIVO                                            |"
        Escribir "| 4. SALIR                                               |"
        Escribir "*--------------------------------------------------------*"
        Escribir "OPCION: "
        Leer opcion
        
        // Validaci�n de opci�n del men�
        Si NO EsNumeroEntero(opcion) O ConvertirANumero(opcion) < 1 O ConvertirANumero(opcion) > 4 Entonces
            Escribir "ERROR: Opci�n no v�lida (1-4)"
            Esperar 1 Segundo
        Sino
            Segun ConvertirANumero(opcion) Hacer
                Caso 1:  // Transferencia
                    Escribir "-- DATOS PARA REALIZAR LA TRANSFERENCIA-- "
                    Escribir "BANCO: 0102 BANCO DE VENEZUELA"
                    Escribir "CUENTA A DEBITAR: 01020501810109389192"
                    Escribir "DOCUMENTO: J - 28303325"
                    
						Escribir "�Desea pagar el monto completo?"
						Repetir
							leer respuesta
							Segun respuesta Hacer
								"1" o "si" o "SI" o "Si" o "y" o "Y":
									respuesta_num<-1
								"2" o "no" o "NO" o "No" o "n" o "N":
									respuesta_num<-0
								De Otro Modo:
									Escribir "No he entendido la respuesta, por favor ingresela de nuevo"
									Borrar Pantalla
							Fin Segun
						Hasta Que respuesta_num=0 o respuesta_num=1
						si respuesta_num=1 Entonces
							Escribir  "PAGO REALIZADO: ", monto, " $. ",monto*tasaBCV," BS"
							Esperar Tecla
							resultado <- 0
						SiNo
							Escribir "MONTO DE LA TRANSFERENCIA EN BS: "
							Repetir
								Leer entradaPago
								
								// Validaci�n directa del n�mero real
								entradaValida <- Verdadero
								contadorPuntos <- 0
								contadorComas <- 0
								
								// Validar formato num�rico
								Si Longitud(entradaPago) = 0 Entonces
									entradaValida <- Falso
									Escribir "ERROR: No puede dejar el monto vac�o"
								Sino
									Para i <- 0 Hasta Longitud(entradaPago) - 1 Hacer
										Segun SubCadena(entradaPago, i, i)
											Caso "0":  // No hacer nada, es d�gito v�lido
											Caso "1":  
											Caso "2":  
											Caso "3":  
											Caso "4":  
											Caso "5":  
											Caso "6":  
											Caso "7":  
											Caso "8":  
											Caso "9":  
												// Todos estos casos son d�gitos v�lidos
											Caso ".":
												contadorPuntos <- contadorPuntos + 1
												Si contadorPuntos > 1 O contadorComas > 0 Entonces
													entradaValida <- Falso
												FinSi
											Caso ",":
												contadorComas <- contadorComas + 1
												Si contadorComas > 1 O contadorPuntos > 0 Entonces
													entradaValida <- Falso
												FinSi
											De Otro Modo:
												entradaValida <- Falso
										FinSegun
									FinPara
									
									// Validar posici�n de separadores
									Si entradaValida = Verdadero Entonces
										Si SubCadena(entradaPago, 0, 0) = "." O SubCadena(entradaPago, 0, 0) = "," O SubCadena(entradaPago, Longitud(entradaPago)-1, Longitud(entradaPago)-1) = "." O SubCadena(entradaPago, Longitud(entradaPago)-1, Longitud(entradaPago)-1) = "," Entonces
											entradaValida <- Falso
										FinSi
									FinSi
								FinSi
								
								Si entradaValida = Falso Entonces
									Escribir "Entrada inv�lida. Por favor ingrese un n�mero real:"
								FinSi
							Hasta Que entradaValida = Verdadero
							Si contadorComas > 0 Entonces
								// Reemplazar coma por punto para la conversi�n
								entradaPago <- Reemplazar(entradaPago)
							FinSi
							
							pago <- ConvertirANumero(entradaPago)
							
							Si pago >= resultado*tasaBCV Entonces
								resultado <- 0
								Escribir "FACTURA PAGADA COMPLETAMENTE"
								Escribir "PULSAR CUALQUIER TECLA PARA AVANZAR"
							Sino
								resultado <- resultado - (pago/tasaBCV)
								Escribir "PAGO PARCIAL REALIZADO: ", pago/tasaBCV, " $. ", pago, " BS"
								Escribir "SALDO PENDIENTE: ", resultado, "$ (", resultado*tasaBCV, " BS)"
								Escribir "PULSAR CUALQUIER TECLA PARA AVANZAR"
							FinSi
							Esperar Tecla      
						FinSi 
                Caso 2:  // Pago M�vil
                    Escribir "--DATOS PARA PAGO MOVIL-- "
                    Escribir "DOCUMENTO: J-28303325"
                    Escribir "NUMERO DE TELEFONO: 04141628880"
                    Escribir "BANCO DESTINO: 0102 BANCO DE VENEZUELA"
                    
                    Escribir "�Desea pagar el monto completo?"
					Repetir
						leer respuesta
						Segun respuesta Hacer
							"1" o "si" o "SI" o "Si" o "y" o "Y":
								respuesta_num<-1
							"2" o "no" o "NO" o "No" o "n" o "N":
								respuesta_num<-0
							De Otro Modo:
								Escribir "No he entendido la respuesta, por favor ingresela de nuevo"
								Borrar Pantalla
						Fin Segun
					Hasta Que respuesta_num=0 o respuesta_num=1
					si respuesta_num=1 Entonces
						Escribir  "PAGO REALIZADO: ", monto, " $. ",monto*tasaBCV," BS"
						Esperar Tecla
						resultado <- 0
					SiNo
						Escribir "MONTO DE LA TRANSFERENCIA EN BS: "
						Repetir
							Leer entradaPago
							
							// Validaci�n directa del n�mero real
							entradaValida <- Verdadero
							contadorPuntos <- 0
							contadorComas <- 0
							
							// Validar formato num�rico
							Si Longitud(entradaPago) = 0 Entonces
								entradaValida <- Falso
								Escribir "ERROR: No puede dejar el monto vac�o"
							Sino
								Para i <- 0 Hasta Longitud(entradaPago) - 1 Hacer
									Segun SubCadena(entradaPago, i, i)
										Caso "0":  // No hacer nada, es d�gito v�lido
										Caso "1":  
										Caso "2":  
										Caso "3":  
										Caso "4":  
										Caso "5":  
										Caso "6":  
										Caso "7":  
										Caso "8":  
										Caso "9":  
											// Todos estos casos son d�gitos v�lidos
										Caso ".":
											contadorPuntos <- contadorPuntos + 1
											Si contadorPuntos > 1 O contadorComas > 0 Entonces
												entradaValida <- Falso
											FinSi
										Caso ",":
											contadorComas <- contadorComas + 1
											Si contadorComas > 1 O contadorPuntos > 0 Entonces
												entradaValida <- Falso
											FinSi
										De Otro Modo:
											entradaValida <- Falso
									FinSegun
								FinPara
								
								// Validar posici�n de separadores
								Si entradaValida = Verdadero Entonces
									Si SubCadena(entradaPago, 0, 0) = "." O SubCadena(entradaPago, 0, 0) = "," O SubCadena(entradaPago, Longitud(entradaPago)-1, Longitud(entradaPago)-1) = "." O SubCadena(entradaPago, Longitud(entradaPago)-1, Longitud(entradaPago)-1) = "," Entonces
										entradaValida <- Falso
									FinSi
								FinSi
							FinSi
							
							Si entradaValida = Falso Entonces
								Escribir "Entrada inv�lida. Por favor ingrese un n�mero real:"
							FinSi
						Hasta Que entradaValida = Verdadero
						Si contadorComas > 0 Entonces
							// Reemplazar coma por punto para la conversi�n
							entradaPago <- Reemplazar(entradaPago)
						FinSi
						
						pago <- ConvertirANumero(entradaPago)
						
						Si pago >= resultado*tasaBCV Entonces
							resultado <- 0
							Escribir "FACTURA PAGADA COMPLETAMENTE"
							Escribir "PULSAR CUALQUIER TECLA PARA AVANZAR"
						Sino
							resultado <- resultado - (pago/tasaBCV)
							Escribir "PAGO PARCIAL REALIZADO: ", pago/tasaBCV, " $. ", pago, " BS"
							Escribir "SALDO PENDIENTE: ", resultado, "$ (", resultado*tasaBCV, " BS)"
							Escribir "PULSAR CUALQUIER TECLA PARA AVANZAR"
						FinSi
						Esperar Tecla      
						FinSi 
                    
                Caso 3:  // Efectivo
                    Escribir "PAGOS EN EFECTIVO DIRIGIRSE A LA TAQUILLA MAS CERCANA Y REALICE SU PAGO"
                    Escribir "IMPORTANTE: PARA PAGAR PARTE DEL MONTO USE TRANSFERENCIA O PAGO MOVIL"
                    Escribir "PULSAR CUALQUIER TECLA PARA VOLVER"
                    Esperar Tecla
                    
                Caso 4:  // Salir
                    Escribir "SALIENDO DE METODOS DE PAGOS"
                    salir <- Verdadero
                    Esperar 1 Segundo
            FinSegun
        FinSi
    Hasta Que resultado <= 0 O salir
FinFuncion

Funcion resultado <- Reemplazar(dato)
    Definir resultado Como Caracter
    Definir i Como Entero
    
    resultado <- ""
    
    Para i <- 0 Hasta Longitud(dato) - 1 Hacer
        Si SubCadena(dato, i, i) = "," Entonces
            resultado <- resultado + "."
        Sino
            resultado <- resultado + SubCadena(dato, i, i)
        FinSi
    FinPara
FinFuncion

Funcion disponibilidad<-funciones_check ( arreglo )
	Para J<-0 Hasta 9 Hacer
		Para I<-0 Hasta 8 Hacer
			Si arreglo[J,I]<>0 Entonces
				asientos_vendidos<-asientos_vendidos+1
			SiNo
				
			Fin Si
		FinPara
	FinPara
	Si asientos_vendidos>=90 Entonces
		disponibilidad<-1
	SiNo
		disponibilidad<-0
	FinSi
Fin Funcion

Funcion  compra_asiento (arreglo1,arreglo2,id_clase,tasaBCV)
	Definir montoPendiente Como Real
	iva <- 0.16
	Dimensionar boletos_comprados_back[87], boletos_comprados_colum[87], boletos_comprados_fil[87], boletos_comprados_tipo[87]
	salir<-0
	Repetir
		compra_correcta=1
		Escribir "Cu�ntos asientos desea comprar"
		Repetir
			Leer boletos
			Si EsNumeroEntero(boletos) Entonces
				Si ConvertirANumero(boletos)> 0 Y ConvertirANumero(boletos) <=87  Entonces
					entradaValida <- Verdadero
				Sino
					Escribir "Opci�n inv�lida. Por favor seleccione una opci�n v�lida."
					entradaValida <- Falso
				FinSi
			Sino
				Escribir "Funci�n inv�lida. Por favor ingrese un n�mero."
				entradaValida <- Falso
			FinSi
		Hasta Que entradaValida = Verdadero
		boletos_num=ConvertirANumero(boletos)
		Si ConvertirANumero(boletos)<=87 y ConvertirANumero(boletos)>0 Entonces
			c<-1
			Repetir
				Escribir "Ingrese la fila de la butaca n�mero ",c," que desea comprar (Eje. A)"
				Leer columna
				Escribir "Ingrese la columna"
				Leer fila
				EScribir "Ingrese que tipo de boleto, desea comprar (Eje. 1)"
				Leer tipo_boleto
				Segun columna Hacer
					"1" o "a" o "A":
						columna_num<-0
						columna<-"A"
					"2" o "b" o "B":
						columna_num<-1
						columna<-"B"
					"3" o "c" o "C":
						columna_num<-2
						columna<-"C"
					"4" o "d" o "D":
						columna_num<-3
						columna<-"D"
					"5" o "e" o "E":
						columna_num<-4
						columna<-"E"
					"6" o "f" o "F":
						columna_num<-5
						columna<-"F"
					"7" o "g" o "G":
						columna_num<-6
						columna<-"G"
					"8" o "h" o "H":
						columna_num<-7
						columna<-"H"
					"9" o "i" o "I":
						columna_num<-8
						columna<-"I"
					"10" o "j" o "J":
						columna_num<-9
						columna<-"J"
					De Otro Modo:
						Escribir "parece que uno de sus asientos no ha sido ingresado correctamente, la columna parece no existir, por favor vuelva a intentarlo"
						boleto_ni�o<-0
						boleto_adulto<-0
						boleto_adulto_mayor<-0
						boletos_num=0
						compra_correcta=0
						c=ConvertirANumero(boletos)
						Esperar Tecla
				Fin Segun
				Segun fila Hacer
					"1":
						fila_num<-0
					"2":
						fila_num<-1
					"3":
						fila_num<-2
					"4":
						fila_num<-3
					"5":
						fila_num<-4
					"6":
						fila_num<-5
					"7":
						fila_num<-6
					"8":
						fila_num<-7
					"9":
						fila_num<-8
					De Otro Modo:
						Escribir "parece que uno de sus asientos no ha sido ingresado correctamente, la fila parece no existir, por favor vuelva a intentarlo"
						boleto_ni�o<-0
						boleto_adulto<-0
						boleto_adulto_mayor<-0
						boletos_num=0
						compra_correcta=0
						c=ConvertirANumero(boletos)
						Esperar Tecla
				Fin Segun
				Segun tipo_boleto Hacer
					"1" o "adulto" o "Adulto" o "ADULTO":
						boleto_adulto<-boleto_adulto+1
						boletos_comprados_tipo[c]<-1
					"2" o "adulto mayor" o "Adulto mayor" o "Adulto Mayor" o "ADULTO MAYOR":
						boleto_adulto_mayor<-boleto_adulto_mayor+1
						boletos_comprados_tipo[c]<-2
					"3" o "Ni�o" o "ni�o" o "NI�O":
						boleto_ni�o<-boleto_ni�o+1
						boletos_comprados_tipo[c]<-3
					De Otro Modo:
						Escribir "Error al procesar el tipo de boleto"
						boleto_ni�o<-0
						boleto_adulto<-0
						boleto_adulto_mayor<-0
						compra_correcta=0
						c=ConvertirANumero(boletos)
						Esperar Tecla
				Fin Segun
				boletos_comprados_back[c]<-columna
				boletos_comprados_colum[c]<-columna_num
				boletos_comprados_fil[c]<-fila_num
				c<-c+1
				SI boleto_ni�o>0 y boleto_adulto<=0 y boleto_adulto_mayor<=0 Entonces
					Escribir "Los ni�os no pueden comprar boletos por su cuenta y deben siempre tener la supervici�n de un adulto"
					boleto_ni�o<-0
					boleto_adulto<-0
					boleto_adulto_mayor<-0
					compra_correcta=0
					c=ConvertirANumero(boletos)+1
					Esperar Tecla
				FinSi
				Si boleto_ni�o>0 y id_clase=3 Entonces
					Escribir "Los ni�os menores de 16 a�os no pueden asistir a funciones de clase C, por favor realic� la compra de otra pel�cula o abstengace de llevar a su hijo a esta funci�n"
					boleto_ni�o<-0
					boleto_adulto<-0
					boleto_adulto_mayor<-0
					compra_correcta=0
					c=ConvertirANumero(boletos)
					Esperar Tecla
				FinSi
				Si boleto_ni�o>0 y id_clase=2 Entonces
					Escribir "Le recordamos que la funci�n a la que asistir� es clase B, los ni�os pueden asistir acompa�ados de un adulto bajo su propia discreci�n"
					Esperar Tecla
				FinSi
			Hasta Que c=ConvertirANumero(boletos)+1
		SiNo
			Escribir "La cantidad de boletos que desea comprar no es posible, est� intentando comprar m�s boletos de los disponibles o ha ingresado una tecla erronea"
			Esperar Tecla
			boleto_ni�o<-0
			boleto_adulto<-0
			boleto_adulto_mayor<-0
			boletos_num=0
			compra_correcta=0
			c=ConvertirANumero(boletos)
			Borrar Pantalla
		Fin Si
		Si ConvertirANumero(boletos)>0 y ConvertirANumero(boletos)<=87 y compra_correcta=1 Entonces
			Para d<-1 Hasta ConvertirANumero(boletos) Hacer
				Si arreglo2[boletos_comprados_colum[d],boletos_comprados_fil[d]]=0 Entonces
					Escribir Sin Saltar "."
					Si d=ConvertirANumero(boletos) Entonces
						Repetir
							Escribir "FACTURA"
							Escribir "============================"
							Escribir "DETALLE DE COMPRA:"
							Escribir Sin Saltar"asientos comprados: "
							Para e<-1 Hasta ConvertirANumero(boletos) Hacer
								Escribir Sin Saltar boletos_comprados_back[e],boletos_comprados_fil[e]+1," "
							Fin Para
							Escribir " "
							Si boleto_adulto>0 Entonces
								Escribir boleto_adulto, " boletos para un adulto "
							SiNo
								
							Fin Si
							Si boleto_adulto_mayor>0 Entonces
								Escribir boleto_adulto_mayor, " boletos para un adulto mayor "
							SiNo
								
							Fin Si
							Si boleto_ni�o>0 Entonces
								Escribir boleto_ni�o, " boletos para un ni�o "
							SiNo
								
							Fin Si
							Escribir "============================"
							boleto_adulto_precio<- boleto_adulto*2
							boleto_adulto_mayor_precio<-boleto_adulto_mayor*1.5
							boleto_ni�o_precio<-boleto_ni�o*1
							valor_de_compra<-boleto_adulto_precio+boleto_adulto_mayor_precio+boleto_ni�o_precio
							Escribir "Subtotal: $", valor_de_compra, " (", valor_de_compra * tasaBCV, " Bs)"
							Escribir "IVA (", iva*100, "%): $", valor_de_compra * iva, " (", valor_de_compra * iva * tasaBCV, " Bs)"
							Escribir "TOTAL A PAGAR: $", valor_de_compra * (1 + iva), " (", valor_de_compra * (1 + iva) * tasaBCV, " Bs)"
							Escribir "============================"
							Escribir "Tasa del d�a a BCV: ", tasaBCV, " Bs"
							Escribir "============================"
							Escribir " �Es correcto?"
							Escribir "============================"
							leer respuesta
							Segun respuesta Hacer
								"1" o "si" o "SI" o "Si" o "y" o "Y":
									respuesta_num<-1
								"2" o "no" o "NO" o "No" o "n" o "N":
									respuesta_num<-0
								De Otro Modo:
									Escribir "No he entendido la respuesta, por favor ingresela de nuevo"
									Borrar Pantalla
							Fin Segun
						Hasta Que respuesta_num=1 o respuesta_num=0
						Si respuesta_num=1 Entonces
							para a<-1 Hasta 11
								n<-convertiratexto(Aleatorio(1,9))
								Numero_de_referencia<-Numero_de_referencia+n
							FinPara
							montoPendiente <- pagar(tasaBCV,valor_de_compra * (1 + iva))
							Escribir "Su n�mero de referencia es: ",Numero_de_referencia," Que disfrute su funci�n!"
							Para f<-1 Hasta ConvertirANumero(boletos) Hacer
								arreglo2[boletos_comprados_colum[f],boletos_comprados_fil[f]]=boletos_comprados_tipo[f]
							Fin Para
							salir<-1
							Esperar Tecla
							Borrar Pantalla
						SiNo
							Escribir "Entendido, volvamos a empezar"
							boleto_adulto<-0
							boleto_adulto_mayor<-0
							boleto_ni�o<-0
						Fin Si
					SiNo
						
					Fin Si
				SiNo
					Si ConvertirANumero(boleto)=1 Entonces
						Escribir "opps, parece que el asiento: ", boletos_comprados_back[d],boletos_comprados_fil[d]," est� ocupado, intente de nuevo"
						Esperar Tecla
						boleto_adulto<-0
						boleto_adulto_mayor<-0
						boleto_ni�o<-0
						Borrar Pantalla
					FinSi
					Si ConvertirANumero(boleto)<1 Entonces
						Escribir "opps, parece que el asiento: ", boletos_comprados_back[d],boletos_comprados_fil[d]," no se encuentra disponible, intente de nuevo"
						Esperar Tecla
						boleto_adulto<-0
						boleto_adulto_mayor<-0
						boleto_ni�o<-0
						Borrar Pantalla
					FinSi
				Fin Si
			Fin Para
		Fin Si
	Hasta Que salir=1
Fin Funcion

Funcion pelicula <- pelicula_a_comprar  ( arreglo1,arreglo12,arreglo22,arreglo32,eleccion )
	Repetir
		salir<-0
		Escribir "*-----------------------------------------------------------------*"
		Escribir "Funciones diponibles marcadas con :","[1m[34mAzul"
		Escribir "Funciones  no disponibles marcadas con : ", "[1m[31mRojo"
		Escribir "*-----------------------------------------------------------------*"
		Segun eleccion Hacer
			1:
				Escribir sin saltar "1- El d�a que la tierra explot� (ESP)"
				Para j<-0 Hasta 3 Hacer
					Si  arreglo12[j]=1 Entonces
						Si j<>3 Entonces
							Escribir Sin Saltar "[1m[31m"+arreglo1[j]
						SiNo
							Escribir "[1m[31m"+arreglo1[J]
						Fin Si
					SiNo
						Si j<>3 Entonces
							Escribir sin saltar "[1m[34m"+arreglo1[J]
						SiNo
							Escribir "[1m[34m"+arreglo1[J]
						Fin Si
					Fin Si
				FinPara
				Repetir
					Escribir "Para que funci�n desea comprar?"
					Leer opcion
					Si EsNumeroEntero(opcion) Entonces
						Si ConvertirANumero(opcion) >= 0 Y ConvertirANumero(opcion) <=5  Entonces
							entradaValida <- Verdadero
						Sino
							Escribir "Opci�n inv�lida. Por favor seleccione una opci�n v�lida."
							entradaValida <- Falso
						FinSi
					Sino
						Escribir "Funci�n inv�lida. Por favor ingrese un n�mero."
						entradaValida <- Falso
					FinSi 
				Hasta Que entradaValida
				respuesta<-ConvertirANumero(opcion)
				Si arreglo12[respuesta-1]=1 Entonces
					Escribir "Funci�n no disponible, intente de nuevo"
					Esperar Tecla
				SiNo
					pelicula<-respuesta
					salir<-1
				Fin Si
			2:
				Escribir sin saltar "2- Godzilla minus one (ESP)"
				Para j<-0 Hasta 3 Hacer
					Si  arreglo22[j]=1 Entonces
						Si j<>3 Entonces
							Escribir Sin Saltar "[1m[31m"+arreglo1[J]
						SiNo
							Escribir "[1m[31m"+arreglo1[J]
						Fin Si
					SiNo
						Si j<>3 Entonces
							Escribir sin saltar "[1m[34m"+arreglo1[J]
						SiNo
							Escribir "[1m[34m"+arreglo1[J]
						Fin Si
					Fin Si
				FinPara
				Repetir
					Escribir "Para que funci�n desea comprar?"
					Leer opcion
					Si EsNumeroEntero(opcion) Entonces
						Si ConvertirANumero(opcion) >= 0 Y ConvertirANumero(opcion) <=5  Entonces
							entradaValida <- Verdadero
						Sino
							Escribir "Opci�n inv�lida. Por favor seleccione una opci�n v�lida."
							entradaValida <- Falso
						FinSi
					Sino
						Escribir "Funci�n inv�lida. Por favor ingrese un n�mero."
						entradaValida <- Falso
					FinSi 
				Hasta Que entradaValida
				respuesta<-ConvertirANumero(opcion)
				Si arreglo22[respuesta-1]=1 Entonces
					Escribir "Funci�n no disponible, intente de nuevo"
					Esperar Tecla
				SiNo
					pelicula<-respuesta
					salir<-1
				Fin Si
			3:
				Escribir sin saltar "3- M�s extra�o que la ficci�n (ESP)"
				Para j<-0 Hasta 3 Hacer
					Si  arreglo32[j]=1 Entonces
						Si j<>3 Entonces
							Escribir Sin Saltar "[1m[31m"+arreglo1[J]
						SiNo
							Escribir "[1m[31m"+arreglo1[J]
						Fin Si
					SiNo
						Si j<>3 Entonces
							Escribir sin saltar "[1m[34m"+arreglo1[J]
						SiNo
							Escribir "[1m[34m"+arreglo1[J]
						Fin Si
					Fin Si
				FinPara
				Repetir
					Escribir "Para que funci�n desea comprar?"
					Leer opcion
					Si EsNumeroEntero(opcion) Entonces
						Si ConvertirANumero(opcion) >= 0 Y ConvertirANumero(opcion) <=5  Entonces
							entradaValida <- Verdadero
						Sino
							Escribir "Opci�n inv�lida. Por favor seleccione una opci�n v�lida."
							entradaValida <- Falso
						FinSi
					Sino
						Escribir "Funci�n inv�lida. Por favor ingrese un n�mero."
						entradaValida <- Falso
					FinSi 
				Hasta Que entradaValida
				respuesta<-ConvertirANumero(opcion)
				Si arreglo32[respuesta-1]=1 Entonces
					Escribir "Funci�n no disponible, intente de nuevo"
					Esperar Tecla
				SiNo
					pelicula<-respuesta
					salir<-1
				Fin Si
			De Otro Modo:
				Escribir "Error mostrando las funciones disponibles"
		Fin Segun
		Borrar Pantalla
	Hasta Que salir=1
Fin Funcion

Funcion pelicula <- pelicula_a_observar  ( arreglo1,arreglo12,arreglo22,arreglo32,eleccion )
	Repetir
		salir<-0
		Escribir "*-----------------------------------------------------------------*"
		Segun eleccion Hacer
			1:
				Escribir sin saltar "1- El d�a que la tierra explot� (ESP)"
				Para j<-0 Hasta 3 Hacer
					Si  arreglo12[j]=1 Entonces
						Si j<>3 Entonces
							Escribir Sin Saltar "[1m[31m"+arreglo1[j]
						SiNo
							Escribir "[1m[31m"+arreglo1[J]
						Fin Si
					SiNo
						Si j<>3 Entonces
							Escribir sin saltar "[1m[34m"+arreglo1[J]
						SiNo
							Escribir "[1m[34m"+arreglo1[J]
						Fin Si
					Fin Si
				FinPara
				Repetir
					Escribir "�Qu� funci�n desea examinar?"
					Leer opcion
					Si EsNumeroEntero(opcion) Entonces
						Si ConvertirANumero(opcion) > 0 Y ConvertirANumero(opcion) <5  Entonces
							entradaValida <- Verdadero
						Sino
							Escribir "Opci�n inv�lida. Por favor seleccione una opci�n v�lida."
							entradaValida <- Falso
						FinSi
					Sino
						Escribir "Funci�n inv�lida. Por favor ingrese un n�mero."
						entradaValida <- Falso
					FinSi 
				Hasta Que entradaValida
				respuesta<-ConvertirANumero(opcion)
				pelicula<-respuesta
				salir<-1
			2:
				Escribir sin saltar "2- Godzilla minus one (ESP)"
				Para j<-0 Hasta 3 Hacer
					Si  arreglo22[j]=1 Entonces
						Si j<>3 Entonces
							Escribir Sin Saltar "[1m[31m"+arreglo1[J]
						SiNo
							Escribir "[1m[31m"+arreglo1[J]
						Fin Si
					SiNo
						Si j<>3 Entonces
							Escribir sin saltar "[1m[34m"+arreglo1[J]
						SiNo
							Escribir "[1m[34m"+arreglo1[J]
						Fin Si
					Fin Si
				FinPara
				Repetir
					Escribir "�Qu� funci�n desea examinar?"
					Leer opcion
					Si EsNumeroEntero(opcion) Entonces
						Si ConvertirANumero(opcion) > 0 Y ConvertirANumero(opcion) <5  Entonces
							entradaValida <- Verdadero
						Sino
							Escribir "Opci�n inv�lida. Por favor seleccione una opci�n v�lida."
							entradaValida <- Falso
						FinSi
					Sino
						Escribir "Funci�n inv�lida. Por favor ingrese un n�mero."
						entradaValida <- Falso
					FinSi 
				Hasta Que entradaValida
				respuesta<-ConvertirANumero(opcion)
				pelicula<-respuesta
				salir<-1
			3:
				Escribir sin saltar "3- M�s extra�o que la ficci�n (ESP)"
				Para j<-0 Hasta 3 Hacer
					Si  arreglo32[j]=1 Entonces
						Si j<>3 Entonces
							Escribir Sin Saltar "[1m[31m"+arreglo1[J]
						SiNo
							Escribir "[1m[31m"+arreglo1[J]
						Fin Si
					SiNo
						Si j<>3 Entonces
							Escribir sin saltar "[1m[34m"+arreglo1[J]
						SiNo
							Escribir "[1m[34m"+arreglo1[J]
						Fin Si
					Fin Si
				FinPara
				Repetir
					Escribir "�Qu� funci�n desea examinar?"
					Leer opcion
					Si EsNumeroEntero(opcion) Entonces
						Si ConvertirANumero(opcion) > 0 Y ConvertirANumero(opcion) <5  Entonces
							entradaValida <- Verdadero
						Sino
							Escribir "Opci�n inv�lida. Por favor seleccione una opci�n v�lida."
							entradaValida <- Falso
						FinSi
					Sino
						Escribir "Funci�n inv�lida. Por favor ingrese un n�mero."
						entradaValida <- Falso
					FinSi 
				Hasta Que entradaValida
				respuesta<-ConvertirANumero(opcion)
				pelicula<-respuesta
				salir<-1
			De Otro Modo:
				Escribir "Error mostrando las funciones disponibles"
		Fin Segun
		Borrar Pantalla
	Hasta Que salir=1
Fin Funcion

Funcion pelicula_a_mostrar  ( arreglo1,arreglo12,arreglo22,arreglo32,eleccion )
	Escribir "*-----------------------------------------------------------------*"
	Escribir "Funciones diponibles marcadas con :","[1m[34mAzul"
	Escribir "Funciones  no disponibles marcadas con : ", "[1m[31mRojo"
	Escribir "*-----------------------------------------------------------------*"
	Segun eleccion Hacer
		1:
			Escribir sin saltar "1- El d�a que la tierra explot� (ESP)"
			Para j<-0 Hasta 3 Hacer
				Si  arreglo12[j]=1 Entonces
					Si j<>3 Entonces
						Escribir Sin Saltar "[1m[31m"+arreglo1[j]
					SiNo
						Escribir "[1m[31m"+arreglo1[J]
					Fin Si
				SiNo
					Si j<>3 Entonces
						Escribir sin saltar "[1m[34m"+arreglo1[J]
					SiNo
						Escribir "[1m[34m"+arreglo1[J]
					Fin Si
				Fin Si
			FinPara
		2:
			Escribir sin saltar "2- Godzilla minus one (ESP)"
			Para j<-0 Hasta 3 Hacer
				Si  arreglo22[j]=1 Entonces
					Si j<>3 Entonces
						Escribir Sin Saltar "[1m[31m"+arreglo1[J]
					SiNo
						Escribir "[1m[31m"+arreglo1[J]
					Fin Si
				SiNo
					Si j<>3 Entonces
						Escribir sin saltar "[1m[34m"+arreglo1[J]
					SiNo
						Escribir "[1m[34m"+arreglo1[J]
					Fin Si
				Fin Si
			FinPara
		3:
			Escribir sin saltar "3- M�s extra�o que la ficci�n (ESP)"
			Para j<-0 Hasta 3 Hacer
				Si  arreglo32[j]=1 Entonces
					Si j<>3 Entonces
						Escribir Sin Saltar "[1m[31m"+arreglo1[J]
					SiNo
						Escribir "[1m[31m"+arreglo1[J]
					Fin Si
				SiNo
					Si j<>3 Entonces
						Escribir sin saltar "[1m[34m"+arreglo1[J]
					SiNo
						Escribir "[1m[34m"+arreglo1[J]
					Fin Si
				Fin Si
			FinPara
		De Otro Modo:
			Escribir "Error mostrando las funciones disponibles"
	Fin Segun
Fin Funcion

Funcion crear_funciones (arreglo2)
	Para J<-0 Hasta 3 Hacer
		arreglo2[J]<-0
	FinPara
FinFuncion

Funcion crear_asientos (arreglo2)
	Para J<-0 Hasta 9 Hacer
		Para I<-0 Hasta 8 Hacer
			Si I=1 y J=1 o J=3 y I=6 o J=7 y I=3 Entonces
				arreglo2[J,I]<--0-1
			SiNo
				arreglo2[J,I]<-0
			Fin Si
		FinPara
	FinPara
Fin Funcion
Funcion imp_asientos (arreglo1,arreglo2)
	Escribir "Asientos diponibles marcados con :","[1m[36mAz�l Claro"
	Escribir "Asientos  no disponibles marcados con : ", "[1m[31mRojo"
	Escribir "Asientos da�ados marcados con: ", "[1m[34mAz�l"
	Para J<-0 Hasta 9 Hacer
		Para I<-0 Hasta 8 Hacer
			Si arreglo2[J,I]=0 Entonces
				Si I<>8 Entonces
					Escribir Sin Saltar "[1m[36m[","[1m[36m"+arreglo1[J,I],"[1m[36m] "
			    SiNo
					Escribir "[1m[36m[","[1m[36m"+arreglo1[J,I],"[1m[36m] "
				Fin Si
			SiNo
				Si arreglo2[J,I]=(-1) Entonces
					Si I<>8 Entonces
						Escribir Sin Saltar "[1m[34m[","[1m[34m"+arreglo1[J,I],"[1m[34m] "
					SiNo
						Escribir "[1m[34m[","[1m[34m"+arreglo1[J,I],"[1m[34m] "
					Fin Si
				SiNo
					Si I<>8 Entonces
						Escribir Sin Saltar "[1m[31m[","[1m[31m"+arreglo1[J,I],"[1m[31m] "
					SiNo
						Escribir "[1m[31m[","[1m[31m"+arreglo1[J,I],"[1m[31m] "
					Fin Si
				FinSi
			Fin si
		FinPara
	FinPara
Fin Funcion

Funcion Cartelera(arreglo1,arreglo12,arreglo22,arreglo32,tasaBCV)
    Limpiar Pantalla
    Escribir "CARTELERA"
    Escribir "============================"
	Escribir "Funciones diponibles marcadas con :","[1m[34mAzul"
	Escribir "Funciones  no disponibles marcadas con : ", "[1m[31mRojo"
	Para i<-1 Hasta 3 Hacer
		Segun i Hacer
			1:
				Escribir sin saltar "1- El d�a que la tierra explot� (ESP)"
				Para j<-0 Hasta 3 Hacer
					Si  arreglo12[j]=1 Entonces
						Si j<>3 Entonces
							Escribir Sin Saltar "[1m[31m"+arreglo1[j]
						SiNo
							Escribir "[1m[31m"+arreglo1[J]
						Fin Si
					SiNo
						Si j<>3 Entonces
							Escribir sin saltar "[1m[34m"+arreglo1[J]
						SiNo
							Escribir "[1m[34m"+arreglo1[J]
						Fin Si
					Fin Si
				FinPara
			2:
				Escribir sin saltar "2- Godzilla minus one (ESP)"
				Para j<-0 Hasta 3 Hacer
					Si  arreglo22[j]=1 Entonces
						Si j<>3 Entonces
							Escribir Sin Saltar "[1m[31m"+arreglo1[J]
						SiNo
							Escribir "[1m[31m"+arreglo1[J]
						Fin Si
					SiNo
						Si j<>3 Entonces
							Escribir sin saltar "[1m[34m"+arreglo1[J]
						SiNo
							Escribir "[1m[34m"+arreglo1[J]
						Fin Si
					Fin Si
				FinPara
			3:
				Escribir sin saltar "3- M�s extra�o que la ficci�n (ESP)"
				Para j<-0 Hasta 3 Hacer
					Si  arreglo32[j]=1 Entonces
						Si j<>3 Entonces
							Escribir Sin Saltar "[1m[31m"+arreglo1[J]
						SiNo
							Escribir "[1m[31m"+arreglo1[J]
						Fin Si
					SiNo
						Si j<>3 Entonces
							Escribir sin saltar "[1m[34m"+arreglo1[J]
						SiNo
							Escribir "[1m[34m"+arreglo1[J]
						Fin Si
					Fin Si
				FinPara
			De Otro Modo:
				Escribir "Error mostrando las funciones disponibles"
		Fin Segun
	Fin Para
	Escribir "============================"
    Escribir "Tasa del d�a a BCV: ", tasaBCV, " Bs"
    Escribir "============================"
FinFuncion

Funcion MostrarPeliculas(peliculas, clasificaciones, sinopsis, valoraciones, funciones_front,EL_dia_que_la_tierra_explot�_back,godzilla_minus_one_back,m�s_extra�o_que_la_ficci�n_back,opcionComprar_pelicula)
    Definir opcionMenu Como Entero
    Definir opcion Como Cadena
    Definir entradaValida Como Logico
    
    Repetir
        Limpiar Pantalla
        Escribir "============================"
        Escribir "        PEL�CULAS          "
        Escribir "============================"
        
        // Mostrar lista de pel�culas
        Para i <- 0 Hasta 2
            Escribir i+1, ". ", peliculas[i]
        FinPara
        Escribir "0. Volver al men� principal"
        Escribir "============================"
        Escribir "Seleccione una pel�cula (1-3) o 0 para volver: "
        
        // Validaci�n de entrada
        Repetir
            Leer opcion
            Si EsNumeroEntero(opcion) Entonces
                opcionMenu <- ConvertirANumero(opcion)
                Si opcionMenu >= 0 Y opcionMenu <= 3 Entonces
                    entradaValida <- Verdadero
                Sino
                    Escribir "Opci�n inv�lida. Debe ser entre 0 y 3."
                    entradaValida <- Falso
                FinSi
            Sino
                Escribir "Entrada inv�lida. Por favor ingrese un n�mero."
                entradaValida <- Falso
            FinSi
        Hasta Que entradaValida = Verdadero
        
        Si opcionMenu >= 1 Y opcionMenu <= 3 Entonces
            // Mostrar detalles de la pel�cula seleccionada
            Limpiar Pantalla
            Escribir "============================"
            Escribir "DETALLES DE LA PEL�CULA"
            Escribir "============================"
            Escribir "T�tulo: ", peliculas[opcionMenu-1]
            Escribir "Clasificaci�n: ", clasificaciones[opcionMenu-1]
            Escribir "Sinopsis: ", sinopsis[opcionMenu-1]
            Escribir "Valoraci�n: ", valoraciones[opcionMenu-1], "/5"
            Escribir ""
            Escribir "HORARIOS DISPONIBLES:"
            // Mostrar horarios disponibles 
            pelicula_a_mostrar(funciones_front,EL_dia_que_la_tierra_explot�_back,godzilla_minus_one_back,m�s_extra�o_que_la_ficci�n_back,opcionMenu)
            Escribir "============================"
			Escribir "Presione enter para volver"
			peli_funcion=opcionMenu+1
            Esperar Tecla
        FinSi
    Hasta Que opcionMenu = 0
FinFuncion

Funcion Carameleria(tasaBCV, subtotal Por Referencia, productos, nombres, precios, cantidades, nombresCategorias)
	Definir opcionMenu, categoria Como Entero
    Definir opcion, letra, cantidadTexto Como Cadena
    Definir opcionNum, producto, i, cantidadEliminar, cantidadAgregar Como Entero
    Definir hayArticulos, entradaValida Como Logico
    
    Repetir
        Limpiar Pantalla
        Escribir "============================"
        Escribir "        CARAMELER�A         "
        Escribir "============================"
        Escribir "1. Combos"
        Escribir "2. Cotufas"
        Escribir "3. Bebidas individuales"
        Escribir "4. Snacks y golosinas"
        Escribir "0. Volver al men� principal"
        Escribir "============================"
        Escribir "Tasa del d�a a BCV: ", tasaBCV, " Bs"
        Escribir "============================"
        Escribir "Seleccione una categor�a (1-4) o 0 para volver: "
        
        // Validaci�n de entrada para categor�a
        Repetir
            Leer opcion
            Si EsNumeroEntero(opcion) Entonces
                opcionMenu <- ConvertirANumero(opcion)
                Si opcionMenu >= 0 Y opcionMenu <= 4 Entonces
                    entradaValida <- Verdadero
                    Si opcionMenu > 0 Entonces
                        categoria <- opcionMenu - 1
                    Sino
                        categoria <- -1
                    FinSi
                Sino
                    Escribir "Opci�n inv�lida. Debe ser entre 0 y 4."
                    entradaValida <- Falso
                FinSi
            Sino
                Escribir "Entrada inv�lida. Por favor ingrese un n�mero."
                entradaValida <- Falso
            FinSi
        Hasta Que entradaValida = Verdadero
        
        Si opcionMenu >= 1 Y opcionMenu <= 4 Entonces
            // Men� de productos
            Repetir
                Limpiar Pantalla
                Escribir "============================"
                Escribir "        CATEGOR�A: ", nombresCategorias[categoria]
                Escribir "============================"
                
                // Mostrar resumen actual
                Escribir "RESUMEN ACTUAL:"
                hayArticulos <- Falso
                Para i <- 0 Hasta productos[categoria]-1
                    Si cantidades[categoria,i] > 0 Entonces
                        Escribir i+1, ". ", nombres[categoria,i], ": ", cantidades[categoria,i], " x $", precios[categoria,i], " = $", cantidades[categoria,i] * precios[categoria,i], " (", cantidades[categoria,i] * precios[categoria,i] * tasaBCV, " Bs)"
                        hayArticulos <- Verdadero
                    FinSi
                FinPara
                
                Si hayArticulos = Falso Entonces
                    Escribir "No hay art�culos a�adidos a�n"
                FinSi
                
                Escribir "============================"
                
                // Mostrar productos
                Para i <- 0 Hasta productos[categoria]-1
                    Escribir i+1, ". ", nombres[categoria,i], " - $", precios[categoria,i], " (", precios[categoria,i]*tasaBCV, " Bs)"
                FinPara
                
                Escribir "E. Eliminar un art�culo"
                Escribir "0. Volver"
                Escribir "============================"
				Escribir "Tasa del d�a a BCV: ", tasaBCV, " Bs"
				Escribir "============================"
                Escribir "Seleccione una opci�n: "
                
                // Validaci�n para selecci�n de producto
                Repetir
                    Leer opcion
                    letra <- Mayusculas(opcion)
                    
                    Segun letra Hacer
                        Caso "E":
                            opcionNum <- -1 // C�digo especial para eliminar
                            entradaValida <- Verdadero
                        De Otro Modo:
                            Si EsNumeroEntero(opcion) Entonces
                                opcionNum <- ConvertirANumero(opcion)
                                Si opcionNum >= 0 Y opcionNum <= productos[categoria] Entonces
                                    entradaValida <- Verdadero
                                Sino
                                    Escribir "Opci�n inv�lida. Por favor seleccione una opci�n v�lida."
                                    entradaValida <- Falso
                                FinSi
                            Sino
                                Escribir "Entrada inv�lida. Por favor ingrese un n�mero o E para eliminar."
                                entradaValida <- Falso
                            FinSi
                    FinSegun
                Hasta Que entradaValida
                
                Segun opcionNum Hacer
                    Caso 0:
                        // Volver sin hacer nada
                    Caso -1: // Opci�n para eliminar
                        // Eliminar producto
                        Limpiar Pantalla
                        Escribir "ART�CULOS A�ADIDOS:"
                        hayArticulos <- Falso
                        
                        Para i <- 0 Hasta productos[categoria]-1
                            Si cantidades[categoria,i] > 0 Entonces
                                Escribir i+1, ". ", nombres[categoria,i], ": ", cantidades[categoria,i], " x $", precios[categoria,i]
                                hayArticulos <- Verdadero
                            FinSi
                        FinPara
                        
                        Si hayArticulos Entonces
                            Escribir "0. Cancelar"
                            Escribir "Seleccione el art�culo a eliminar: "
                            
                            // Validaci�n para eliminar
                            Repetir
                                Leer opcion
                                Si EsNumeroEntero(opcion) Entonces
                                    producto <- ConvertirANumero(opcion)
                                    Si producto >= 0 Y producto <= productos[categoria] Entonces
                                        entradaValida <- Verdadero
                                    Sino
                                        Escribir "Opci�n no v�lida"
                                        entradaValida <- Falso
                                    FinSi
                                Sino
                                    Escribir "Entrada inv�lida. Por favor ingrese un n�mero."
                                    entradaValida <- Falso
                                FinSi
                            Hasta Que entradaValida
                            
                            Si producto >= 1 Y producto <= productos[categoria] Entonces
                                Si cantidades[categoria, producto-1] > 0 Entonces
                                    Repetir
                                        Escribir "Tienes ", cantidades[categoria, producto-1], " ", nombres[categoria, producto-1], ". �Cu�ntos quieres eliminar?"
                                        Leer cantidadTexto
                                        Si EsNumeroEntero(cantidadTexto) Entonces
                                            cantidadEliminar <- ConvertirANumero(cantidadTexto)
                                            Si cantidadEliminar > 0 Y cantidadEliminar <= cantidades[categoria, producto-1] Entonces
                                                cantidades[categoria, producto-1] <- cantidades[categoria, producto-1] - cantidadEliminar
                                                subtotal <- subtotal - (precios[categoria, producto-1] * cantidadEliminar)
                                                Escribir "Se eliminaron ", cantidadEliminar, " ", nombres[categoria, producto-1]
                                                entradaValida <- Verdadero
                                            Sino
                                                Escribir "Cantidad inv�lida. Debe ser entre 1 y ", cantidades[categoria, producto-1]
                                                entradaValida <- Falso
                                            FinSi
                                        Sino
                                            Escribir "Entrada inv�lida. Por favor ingrese un n�mero."
                                            entradaValida <- Falso
                                        FinSi
                                    Hasta Que entradaValida
                                Sino
                                    Escribir "No hay art�culos de ", nombres[categoria, producto-1], " a�adidos al pedido."
                                FinSi
                            FinSi
                        Sino
                            Escribir "No hay art�culos para eliminar"
                        FinSi
                        Escribir "Presione Enter para continuar..."
                        Esperar Tecla
						
					De Otro Modo:
                        // Agregar producto
                        Si opcionNum >= 1 Y opcionNum <= productos[categoria] Entonces
                            Repetir
                                Escribir "�Cu�ntos ", nombres[categoria, opcionNum-1], " deseas a�adir?"
                                Leer cantidadTexto
                                Si EsNumeroEntero(cantidadTexto) Entonces
                                    cantidadAgregar <- ConvertirANumero(cantidadTexto)
                                    Si cantidadAgregar > 0 Entonces
                                        cantidades[categoria, opcionNum-1] <- cantidades[categoria, opcionNum-1] + cantidadAgregar
                                        subtotal <- subtotal + (precios[categoria, opcionNum-1] * cantidadAgregar)
                                        Escribir "Se han agregado ", cantidadAgregar, " ", nombres[categoria, opcionNum-1]
                                        entradaValida <- Verdadero
                                    Sino
                                        Escribir "La cantidad debe ser mayor que 0"
                                        entradaValida <- Falso
                                    FinSi
                                Sino
                                    Escribir "Entrada inv�lida. Por favor ingrese un n�mero."
                                    entradaValida <- Falso
                                FinSi
                            Hasta Que entradaValida
                            Esperar 1 Segundo
                        Sino
                            Escribir "N�mero de producto no v�lido"
                            Esperar Tecla
                        FinSi
                FinSegun
            Hasta Que opcionNum = 0
        FinSi
    Hasta Que opcionMenu = 0
FinFuncion

Funcion GenerarFactura(tasaBCV, subtotal Por Referencia, iva, productos, nombres, precios, cantidades Por Referencia)
    Definir opcionMenu Como Cadena
    Definir Numero_de_referencia Como Cadena
    Definir montoPendiente Como Real
    Definir salir Como Logico
    
    salir <- Falso
    
    Repetir
        Limpiar Pantalla
        Escribir "============================"
        Escribir "        FACTURACI�N         "
        Escribir "============================"
        
        // Mostrar detalle de compra
        Escribir "DETALLE DE COMPRA:"
        Para categoria <- 0 Hasta 3 Hacer
            Para i <- 0 Hasta productos[categoria]-1 Hacer
                Si cantidades[categoria,i] > 0 Entonces
                    Escribir nombres[categoria,i], ": ", cantidades[categoria,i], " x $", precios[categoria,i], " = $", cantidades[categoria,i]*precios[categoria,i], " (", cantidades[categoria,i] * precios[categoria,i] * tasaBCV, " Bs)"
                FinSi
            FinPara
        FinPara
        
        Escribir "============================"
        Escribir "Subtotal: $", subtotal, " (", subtotal * tasaBCV, " Bs)"
        Escribir "IVA (16%): $", subtotal*iva, " (", subtotal * iva * tasaBCV, " Bs)"
        Escribir "TOTAL: $", subtotal*(1+iva), " (", subtotal*(1+iva)*tasaBCV, " BS)"
        Escribir "============================"
		Escribir "Tasa del d�a a BCV: ", tasaBCV, " Bs"
		Escribir "============================"
        
        // Opciones din�micas
        Si subtotal > 0 Entonces
            Escribir "1. Realizar pago"
            Escribir "0. Volver al men� principal"
        Sino
            Escribir "1. Ver comprobante"
            Escribir "0. Volver al men� principal"
        FinSi
        
        Escribir "============================"
        Escribir "Seleccione opci�n: "
        Leer opcionMenu
        
        Si EsNumeroEntero(opcionMenu) Entonces
            Segun ConvertirANumero(opcionMenu) Hacer
                1:
                    Si subtotal > 0 Entonces
                        montoPendiente <- pagar(tasaBCV, subtotal*(1+iva))
                        
                        Si montoPendiente <= 0 Entonces
                            Numero_de_referencia <- GenerarNumeroReferencia(11, 0, 9) // Par�metros correctos
                            
                            LimpiarCarrito(cantidades, productos)
                            subtotal <- 0
                            
                            Escribir "�Pago completado!"
                            Escribir "N� de referencia: ", Numero_de_referencia
							Escribir "PULSAR CUALQUIER TECLA PARA AVANZAR"
                        Sino
                            subtotal <- montoPendiente/(1+iva)
                            Escribir "Queda pendiente: $", montoPendiente, " (", montoPendiente*tasaBCV, " BS)"
							Escribir "PULSAR CUALQUIER TECLA PARA AVANZAR"
                        FinSi
                    Sino
                        Escribir "Mostrando comprobante de pago..."
                    FinSi
                    Esperar Tecla
                0:
                    salir <- Verdadero
                De Otro Modo:
                    Escribir "Error: Opci�n debe ser 0 o 1"
                    Esperar 1 Segundo
            FinSegun
        Sino
            Escribir "Error: Debe ingresar un n�mero"
            Esperar 1 Segundo
        FinSi
    Hasta Que salir O subtotal <= 0
FinFuncion

// Funci�n auxiliar para generar n�mero de referencia (ahora con argumento)
Funcion resultado <- GenerarNumeroReferencia(longitu, minDigito, maxDigito)
    Definir resultado Como Cadena
    Definir i, digito Como Entero
    
    resultado <- ""
    Para i <- 1 Hasta longitu Hacer
        digito <- Aleatorio(minDigito, maxDigito)
        resultado <- resultado + ConvertirATexto(digito)
    FinPara
    
    resultado <- resultado // Devuelve el valor (en PSeInt no se usa "Devolver")
FinFuncion

// Funci�n auxiliar para limpiar el carrito
Funcion LimpiarCarrito(cantidades Por Referencia, productos)
    Definir categoria, i Como Entero
    
    Para categoria <- 0 Hasta 3 Hacer
        Para i <- 0 Hasta productos[categoria]-1 Hacer
            cantidades[categoria,i] <- 0
        FinPara
    FinPara
FinFuncion

Funcion resultado <- EsNumeroEntero(cadena)
    Definir resultado Como Logico
    Definir i Como Entero
    
    resultado <- Verdadero
    Si Longitud(cadena) = 0 Entonces
        resultado <- Falso
    Sino
        Para i <- 0 Hasta Longitud(cadena)-1
            Si SubCadena(cadena, i, i) < "0" O SubCadena(cadena, i, i) > "9" Entonces
                resultado <- Falso
            FinSi
        FinPara
    FinSi
FinFuncion

Algoritmo CineMoya
	Dimensionar funciones_front[4]
	Para J<-0 Hasta 3 Hacer
		Segun J Hacer
			0:
				funciones_front[J]<-" [10:00 am]"
			1:
				funciones_front[J]<-" [12:00 pm]"
			2:
				funciones_front[J]<-" [2:00 pm]"
			3:
				funciones_front[J]<-" [4:00 pm]"
			De Otro Modo:
				Escribir "Error al crear las funciones"
		Fin Segun
	FinPara
	Dimensionar Asientos_front[10,9]
	Para J<-0 Hasta 9 Hacer
		Para I<-0 Hasta 8 Hacer
			Segun J Hacer
				0:
					Asientos_front[J,I]<-"A"
				1:
					Asientos_front[J,I]<-"B"
				2:
					Asientos_front[J,I]<-"C"
				3:
					Asientos_front[J,I]<-"D"
				4:
					Asientos_front[J,I]<-"E"
				5:
					Asientos_front[J,I]<-"F"
				6:
					Asientos_front[J,I]<-"G"
				7:
					Asientos_front[J,I]<-"H"
				8:
					Asientos_front[J,I]<-"I"
				9:
					Asientos_front[J,I]<-"J"
				De Otro Modo:
					Escribir "Error creando las butacas"
			Fin Segun
			Segun I Hacer
				0:
					Asientos_front[J,I]<-Asientos_front[J,I]+"1"
				1:
					Asientos_front[J,I]<-Asientos_front[J,I]+"2"
				2:
					Asientos_front[J,I]<-Asientos_front[J,I]+"3"
				3:
					Asientos_front[J,I]<-Asientos_front[J,I]+"4"
				4:
					Asientos_front[J,I]<-Asientos_front[J,I]+"5"
				5:
					Asientos_front[J,I]<-Asientos_front[J,I]+"6"
				6:
					Asientos_front[J,I]<-Asientos_front[J,I]+"7"
				7:
					Asientos_front[J,I]<-Asientos_front[J,I]+"8"
				8:
					Asientos_front[J,I]<-Asientos_front[J,I]+"9"
				De Otro Modo:
					Escribir "Error creando las butacas"
			Fin Segun
		FinPara
	FinPara
	Dimensionar EL_dia_que_la_tierra_explot�_back[4],godzilla_minus_one_back[4], m�s_extra�o_que_la_ficci�n_back[4]
	crear_funciones(El_dia_que_la_tierra_explot�_back)
	crear_funciones(godzilla_minus_one_back)
	crear_funciones(m�s_extra�o_que_la_ficci�n_back)
	//asientos
	Dimensionar EL_dia_que_la_tierra_explot�_back_asientos[10,9]
	Dimensionar godzilla_minus_one_back_asientos[10,9]
	Dimensionar m�s_extra�o_que_la_ficci�n_back_asientos[10,9]
	Dimensionar EL_dia_que_la_tierra_explot�_back_asientos2[10,9]
	Dimensionar godzilla_minus_one_back_asientos2[10,9]
	Dimensionar m�s_extra�o_que_la_ficci�n_back_asientos2[10,9]
	Dimensionar EL_dia_que_la_tierra_explot�_back_asientos3[10,9]
	Dimensionar godzilla_minus_one_back_asientos3[10,9]
	Dimensionar m�s_extra�o_que_la_ficci�n_back_asientos3[10,9]
	Dimensionar EL_dia_que_la_tierra_explot�_back_asientos4[10,9]
	Dimensionar godzilla_minus_one_back_asientos4[10,9]
	Dimensionar m�s_extra�o_que_la_ficci�n_back_asientos4[10,9]
	crear_asientos(EL_dia_que_la_tierra_explot�_back_asientos)
	crear_asientos(godzilla_minus_one_back_asientos)
	crear_asientos(m�s_extra�o_que_la_ficci�n_back_asientos)
	crear_asientos(EL_dia_que_la_tierra_explot�_back_asientos2)
	crear_asientos(godzilla_minus_one_back_asientos2)
	crear_asientos(m�s_extra�o_que_la_ficci�n_back_asientos2)
	crear_asientos(EL_dia_que_la_tierra_explot�_back_asientos3)
	crear_asientos(godzilla_minus_one_back_asientos3)
	crear_asientos(m�s_extra�o_que_la_ficci�n_back_asientos3)
	crear_asientos(EL_dia_que_la_tierra_explot�_back_asientos4)
	crear_asientos(godzilla_minus_one_back_asientos4)
	crear_asientos(m�s_extra�o_que_la_ficci�n_back_asientos4)
	Para J<-0 Hasta 9 Hacer
		Para I<-0 Hasta 8 Hacer
			Si I=1 y J=1 o J=3 y I=6 o J=7 y I=3 Entonces
				m�s_extra�o_que_la_ficci�n_back_asientos4[J,I]<-0-1
			SiNo
				m�s_extra�o_que_la_ficci�n_back_asientos4[J,I]<-1
			Fin Si
		FinPara
	FinPara
	m�s_extra�o_que_la_ficci�n_back_asientos4[9,8]<-0
	
    //Definir constantes para las categor�as 
    Definir COMBOS, COTUFAS, BEBIDAS, SNACKS Como Entero
	
	COMBOS <- 0
    COTUFAS <- 1
    BEBIDAS <- 2
    SNACKS <- 3
	
	// Arreglo con nombres de categor�as (base 0)
    Dimension nombresCategorias[4]
    nombresCategorias[COMBOS] <- "COMBOS"
    nombresCategorias[COTUFAS] <- "COTUFAS"
    nombresCategorias[BEBIDAS] <- "BEBIDAS"
    nombresCategorias[SNACKS] <- "SNACKS"
    
	// ================= INICIALIZACI�N DE ARREGLOS =================
    // Primero dimensionamos los arreglos 
    Dimension cantidadProductos[4]  // �ndices del 0 al 3
    
    // Luego asignamos los valores
    cantidadProductos[COMBOS] <- 6    // 6 combos disponibles
    cantidadProductos[COTUFAS] <- 3    // 3 tipos de cotufas
    cantidadProductos[BEBIDAS] <- 6    // 6 bebidas
    cantidadProductos[SNACKS] <- 11    // 11 snacks
    
    // Dimensionamos los dem�s arreglos 
    Dimension nombres[4, 11]  // [Categor�a][Producto] - 11 es el m�ximo necesario (para snacks)
    Dimension precios[4, 11]
    Dimension cantidades[4, 11]
	
	// ================= INICIALIZACI�N DE DATOS =================
    // --- Combos --- 
    nombres[COMBOS, 0] <- "COMBO YUKY PAK"
    precios[COMBOS, 0] <- 5.20
    nombres[COMBOS, 1] <- "COMBO TEQUE�OS"
    precios[COMBOS, 1] <- 7.80
    nombres[COMBOS, 2] <- "COMBO NUGGETS"
    precios[COMBOS, 2] <- 6.80
    nombres[COMBOS, 3] <- "COMBO PEQUE�O"
    precios[COMBOS, 3] <- 5.00
    nombres[COMBOS, 4] <- "COMBO MEDIANO"
    precios[COMBOS, 4] <- 6.00
    nombres[COMBOS, 5] <- "COMBO PARA DOS"
    precios[COMBOS, 5] <- 10.50
	
    // --- Cotufas --- 
    nombres[COTUFAS, 0] <- "COTUFA PEQUE�A"
    precios[COTUFAS, 0] <- 4.20
    nombres[COTUFAS, 1] <- "COTUFA MEDIANA"
    precios[COTUFAS, 1] <- 5.20
    nombres[COTUFAS, 2] <- "COTUFA GRANDE"
    precios[COTUFAS, 2] <- 6.00
	
    // --- Bebidas --- 
    nombres[BEBIDAS, 0] <- "MINALBA PET 600ML"
    precios[BEBIDAS, 0] <- 1.80
    nombres[BEBIDAS, 1] <- "REFRESCO GRANDE"
    precios[BEBIDAS, 1] <- 2.50
    nombres[BEBIDAS, 2] <- "REFRESCO MEDIANO"
    precios[BEBIDAS, 2] <- 2.20 
    nombres[BEBIDAS, 3] <- "YUKY-PAK 250ML"
    precios[BEBIDAS, 3] <- 1.30
    nombres[BEBIDAS, 4] <- "MALTA EN LATA 355ML"
    precios[BEBIDAS, 4] <- 1.60
    nombres[BEBIDAS, 5] <- "REFRESCO PEQUE�O"
    precios[BEBIDAS, 5] <- 2.00
	
    // --- Snacks --- 
    nombres[SNACKS, 0] <- "COCOSETTE MAXI"
    precios[SNACKS, 0] <- 1.20
    nombres[SNACKS, 1] <- "SUSY CHOCOLATE MAXI"
    precios[SNACKS, 1] <- 1.20
    nombres[SNACKS, 2] <- "CHOCOLATE DE LECHE SAVOY 30GR"
    precios[SNACKS, 2] <- 1.50
    nombres[SNACKS, 3] <- "CIR CRI 27GR"
    precios[SNACKS, 3] <- 1.50
    nombres[SNACKS, 4] <- "SAMBA 32GR"
    precios[SNACKS, 4] <- 1.00
    nombres[SNACKS, 5] <- "NATUCHIPS PLATANITOS NAT 150 GR"
    precios[SNACKS, 5] <- 4.00
    nombres[SNACKS, 6] <- "RUFFLES QUESO 125 GRS"
    precios[SNACKS, 6] <- 4.10
    nombres[SNACKS, 7] <- "CHEESE TRIS 150 GRS"
    precios[SNACKS, 7] <- 2.30
    nombres[SNACKS, 8] <- "PEPITO 80GR"
    precios[SNACKS, 8] <- 1.50
    nombres[SNACKS, 9] <- "DORITOS MEGA QUESO 150 GR"
    precios[SNACKS, 9] <- 3.50
    nombres[SNACKS, 10] <- "CHEETOS FLAMIN HOT 120 GR"
    precios[SNACKS, 10] <- 2.50
    
    // ================= DATOS DE PEL�CULAS =================
    Dimension peliculas[3]
    Dimension clasificaciones[3]
    Dimension sinopsis[3]
    Dimension valoraciones[3]
    
    // Inicializar datos de pel�culas
    peliculas[0] <- "El d�a que la tierra explot� (ESP)"
    clasificaciones[0] <- "A"
    sinopsis[0] <- "Porky y Lucas salvar�n el d�a, cuando descubran un plan alien�gena secreto para controlar las mentes"
    valoraciones[0] <- "4.2"
    
    peliculas[1] <- "Godzilla minus one (ESP)"
    clasificaciones[1] <- "C"
    sinopsis[1] <- "Un monstruo gigante emerge de las profundidades del oc�ano y se dispone a atacar Jap�n justo cuando la naci�n trata de recuperarse tras la destrucci�n ocasionada por la Segunda Guerra Mundial"
    valoraciones[1] <- "4.7"
    
    peliculas[2] <- "M�s extra�o que la ficci�n (ESP)"
    clasificaciones[2] <- "B"
    sinopsis[2] <- "Una comedia dram�tica sobre un hombre que descubre que es personaje de una novela."
    valoraciones[2] <- "4.5"
	
    // ================= VARIABLES GLOBALES =================
    Definir subtotal, iva, tasaBCV Como Real
    subtotal <- 0
    iva <- 0.16
    tasaBCV <- 94.80
	
    // Variables principales 
    Definir opcionMenuPrincipal Como Entero
    Definir entradaMenu Como Cadena
    Definir valido Como Logico
	Definir entradaMenu2 Como Caracter
	Definir menu Como Entero
	columna<-10
	fila<-9
	
	butaca_deteriorada <- -1
	butaca_vacia <- 0
	butaca_adulto <- 1
	butaca_adulto_mayor <- 2
	butaca_joven <- 3
    // Men� principal 
    Repetir
		EL_dia_que_la_tierra_explot�_back[0]<-funciones_check(EL_dia_que_la_tierra_explot�_back_asientos)
		EL_dia_que_la_tierra_explot�_back[1]<-funciones_check(EL_dia_que_la_tierra_explot�_back_asientos2)
		EL_dia_que_la_tierra_explot�_back[2]<-funciones_check(EL_dia_que_la_tierra_explot�_back_asientos3)
		EL_dia_que_la_tierra_explot�_back[3]<-funciones_check(EL_dia_que_la_tierra_explot�_back_asientos4)
		godzilla_minus_one_back[0]<-funciones_check(godzilla_minus_one_back_asientos)
		godzilla_minus_one_back[1]<-funciones_check(godzilla_minus_one_back_asientos2)
		godzilla_minus_one_back[2]<-funciones_check(godzilla_minus_one_back_asientos3)
		godzilla_minus_one_back[3]<-funciones_check(godzilla_minus_one_back_asientos4)
		m�s_extra�o_que_la_ficci�n_back[0]<-funciones_check(m�s_extra�o_que_la_ficci�n_back_asientos)
		m�s_extra�o_que_la_ficci�n_back[1]<-funciones_check(m�s_extra�o_que_la_ficci�n_back_asientos2)
		m�s_extra�o_que_la_ficci�n_back[2]<-funciones_check(m�s_extra�o_que_la_ficci�n_back_asientos3)
		m�s_extra�o_que_la_ficci�n_back[3]<-funciones_check(m�s_extra�o_que_la_ficci�n_back_asientos4)
		EL_dia_que_la_tierra_explot�_back[0]<-1
		godzilla_minus_one_back[0]<-1
		m�s_extra�o_que_la_ficci�n_back[0]<-1
		
		// Men� principal 
		Limpiar Pantalla
        Escribir "============================"
        Escribir "       CINE MOYA        "
        Escribir "============================"
        Escribir "1. Cartelera"
        Escribir "2. Pel�culas"
		Escribir "3. Ver asientos disponibles"
		Escribir "4. Comprar boletos"
        Escribir "5. Carameler�a"
        Escribir "6. Factura de Carameler�a"
		Escribir "7. Curiosidades del prof. Alexander Moya"
        Escribir "8. Salir"
        Escribir "============================"
		Escribir "Tasa del d�a a BCV: ", tasaBCV, " Bs"
		Escribir "============================"
        Escribir "Seleccione una opci�n (1-8): "
        
        Repetir
            Leer entradaMenu
            valido <- Verdadero
            
            Si No EsNumeroEntero(entradaMenu) Entonces
                Escribir "Error: Debe ingresar un n�mero"
                valido <- Falso
            Sino
                opcionMenuPrincipal <- ConvertirANumero(entradaMenu)
                Si opcionMenuPrincipal < 1 O opcionMenuPrincipal > 8 Entonces
                    Escribir "Error: Opci�n debe ser entre 1-8"
                    valido <- Falso
                FinSi
            FinSi
        Hasta Que valido
		Segun opcionMenuPrincipal Hacer
			1: 
                Cartelera(funciones_front,EL_dia_que_la_tierra_explot�_back,godzilla_minus_one_back,m�s_extra�o_que_la_ficci�n_back,tasaBCV)
				Escribir "Presione enter para volver"
				Esperar Tecla
            2:
                MostrarPeliculas(peliculas, clasificaciones, sinopsis, valoraciones, funciones_front,EL_dia_que_la_tierra_explot�_back,godzilla_minus_one_back,m�s_extra�o_que_la_ficci�n_back,opcionComprar_pelicula)
			3:
				Cartelera(funciones_front,EL_dia_que_la_tierra_explot�_back,godzilla_minus_one_back,m�s_extra�o_que_la_ficci�n_back,tasaBCV)
				Escribir "�Cu�l pel�cula desea ver?"
				Repetir
					Leer pregunta
					Si EsNumeroEntero(pregunta) Entonces
						Si ConvertirANumero(pregunta)>= 1 Y ConvertirANumero(pregunta) <=3  Entonces
							entradaValida <- Verdadero
							pregunta_num<-ConvertirANumero(pregunta)
						Sino
							Escribir "Opci�n inv�lida. Por favor seleccione una opci�n v�lida."
							entradaValida <- Falso
						FinSi
					Sino
						Escribir "Funci�n inv�lida. Por favor ingrese un n�mero."
						entradaValida <- Falso
					FinSi
				Hasta Que entradaValida
				pelicula_a_mostrar(funciones_front,EL_dia_que_la_tierra_explot�_back,godzilla_minus_one_back,m�s_extra�o_que_la_ficci�n_back,pregunta_num)
				Escribir "�D� que funci�n desea ver los asientos?"
				Repetir
					Leer pregunta2
					Si EsNumeroEntero(pregunta2) Entonces
						Si ConvertirANumero(pregunta2)> 1 Y ConvertirANumero(pregunta2) <=4  Entonces
							entradaValida <- Verdadero
							pregunta2_num<-ConvertirANumero(pregunta2)
						Sino
							Escribir "Opci�n inv�lida. Por favor seleccione una opci�n v�lida."
							entradaValida <- Falso
						FinSi
					Sino
						Escribir "Funci�n inv�lida. Por favor ingrese un n�mero."
						entradaValida <- Falso
					FinSi
				Hasta Que entradaValida
				Segun pregunta_num Hacer
					1:
						Segun pregunta2_num Hacer
							1:
								imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos)
								Escribir "Asientos disponible en pantalla"
								Esperar Tecla
							2:
								imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos2)
								Escribir "Asientos disponible en pantalla"
								Esperar Tecla
							3:
								imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos3)
								Escribir "Asientos disponible en pantalla"
								Esperar Tecla
							4:
								imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos4)
								Escribir "Asientos disponible en pantalla"
								Esperar Tecla
							De Otro Modo:
								Escribir "Error al mostrar asientos"
						Fin Segun
					2:
						Segun pregunta2_num Hacer
							1:
								imp_asientos(Asientos_front,godzilla_minus_one_back_asientos)
								Escribir "Asientos disponible en pantalla"
								Esperar Tecla
							2:
								imp_asientos(Asientos_front,godzilla_minus_one_back_asientos2)
								Escribir "Asientos disponible en pantalla"
								Esperar Tecla
							3:
								imp_asientos(Asientos_front,godzilla_minus_one_back_asientos3)
								Escribir "Asientos disponible en pantalla"
								Esperar Tecla
							4:
								imp_asientos(Asientos_front,godzilla_minus_one_back_asientos4)
								Escribir "Asientos disponible en pantalla"
								Esperar Tecla
							De Otro Modo:
								Escribir "Error al mostrar asientos"
						Fin Segun
					3:
						Segun pregunta2_num Hacer
							1:
								imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos)
								Escribir "Asientos disponible en pantalla"
								Esperar Tecla
							2:
								imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos2)
								Escribir "Asientos disponible en pantalla"
								Esperar Tecla
							3:
								imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos3)
								Escribir "Asientos disponible en pantalla"
								Esperar Tecla
							4:
								imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos4)
								Escribir "Asientos disponible en pantalla"
								Esperar Tecla
							De Otro Modo:
								Escribir "Error al mostrar asientos"
						Fin Segun
				FinSegun
				
			4:
				Escribir "*-------------------------------- Pel�culas----------*"
				Escribir "1.El d�a que la tierra explot� (ESP) - Clase A"
				Escribir "2. Godzilla minus one (ESP) - Clase C"
				Escribir "3. M�s extra�o que la ficci�n (ESP) - Clase B"
				Escribir "�Para que pel�cula desea comprar sus boletos?"
				Escribir "*----------------------------------------------------*"
				Repetir
					Leer comprar_pelicula
					valido <- Verdadero
					Si No EsNumeroEntero(comprar_pelicula) Entonces
						Escribir "Error: Debe ingresar un n�mero"
						valido <- Falso
					Sino
						opcionComprar_pelicula <- ConvertirANumero(comprar_pelicula)
						Si opcionComprar_pelicula < 1 O opcionComprar_pelicula > 3 Entonces
							Escribir "Error: Opci�n debe ser entre 1-3"
							valido <- Falso
						FinSi
					FinSi
				Hasta Que valido
				Borrar Pantalla
				funcion_comprada<-pelicula_a_comprar(funciones_front,EL_dia_que_la_tierra_explot�_back,godzilla_minus_one_back,m�s_extra�o_que_la_ficci�n_back,opcionComprar_pelicula)
				Segun opcionComprar_pelicula Hacer
					1:
						Segun funcion_comprada Hacer
							1:
								imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos)
								compra_asiento(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos,1,tasaBCV)
								imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos)
								Borrar Pantalla
								Escribir "Asiento comprado en pantalla"
								Esperar Tecla
							2:
								imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos2)
								compra_asiento(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos2,1,tasaBCV)
								imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos2)
								Escribir "Asiento comprado en pantalla"
								Esperar Tecla
							3:
								imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos3)
								compra_asiento(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos3,1,tasaBCV)
								imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos3)
								Escribir "Asiento comprado en pantalla"
								Esperar Tecla
							4:
								imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos4)
								compra_asiento(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos4,1,tasaBCV)
								imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos4)
								Escribir "Asiento comprado en pantalla"
								Esperar Tecla
							De Otro Modo:
								Escribir "Error al comprar la pel�cula"
						Fin Segun
					2:
						Segun funcion_comprada Hacer
							1:
								imp_asientos(Asientos_front,godzilla_minus_one_back_asientos)
								compra_asiento(Asientos_front,godzilla_minus_one_back_asientos,3,tasaBCV)
								imp_asientos(Asientos_front,godzilla_minus_one_back_asientos)
								Escribir "Asiento comprado en pantalla"
								Esperar Tecla
							2:
								imp_asientos(Asientos_front,godzilla_minus_one_back_asientos2)
								compra_asiento(Asientos_front,godzilla_minus_one_back_asientos2,3,tasaBCV)
								imp_asientos(Asientos_front,godzilla_minus_one_back_asientos2)
								Escribir "Asiento comprado en pantalla"
								Esperar Tecla
							3:
								imp_asientos(Asientos_front,godzilla_minus_one_back_asientos3)
								compra_asiento(Asientos_front,godzilla_minus_one_back_asientos3,3,tasaBCV)
								imp_asientos(Asientos_front,godzilla_minus_one_back_asientos3)
								Escribir "Asiento comprado en pantalla"
								Esperar Tecla
							4:
								imp_asientos(Asientos_front,godzilla_minus_one_back_asientos4)
								compra_asiento(Asientos_front,godzilla_minus_one_back_asientos4,3,tasaBCV)
								imp_asientos(Asientos_front,godzilla_minus_one_back_asientos4)
								Escribir "Asiento comprado en pantalla"
								Esperar Tecla
							De Otro Modo:
								Escribir "Error al comprar la pel�cula"
						Fin Segun
					3:
						Segun funcion_comprada Hacer
							1:
								imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos)
								compra_asiento(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos,2,tasaBCV)
								imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos)
								Escribir "Asiento comprado en pantalla"
								Esperar Tecla
							2:
								imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos2)
								compra_asiento(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos2,2,tasaBCV)
								imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos2)
								Escribir "Asiento comprado en pantalla"
								Esperar Tecla
							3:
								imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos3)
								compra_asiento(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos3,2,tasaBCV)
								imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos3)
								Escribir "Asiento comprado en pantalla"
								Esperar Tecla
							4:
								imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos4)
								compra_asiento(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos4,2,tasaBCV)
								imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos4)
								Escribir "Asiento comprado en pantalla"
								Esperar Tecla
							De Otro Modo:
								Escribir "Error al comprar la pel�cula"
				        Fin Segun
				FinSegun
				
			5:
				Carameleria(tasaBCV, subtotal, cantidadProductos, nombres, precios, cantidades, nombresCategorias)
			6:
				Si subtotal > 0 Entonces
					GenerarFactura(tasaBCV, subtotal, iva, cantidadProductos, nombres, precios, cantidades)
				Sino
					Escribir "No hay productos para facturar"
					Esperar 1 Segundos
				FinSi
			7:
				
				Repetir
					Escribir "*-------------------------------- MEN� PRINCIPAL ---------------------------------*"
					Escribir "| 1. BUSCAR FILA MAS VENDIDA                                                      |"
					Escribir "| 2. BUSCAR COLUMNA MAS VENDIDA                                                   |"
					Escribir "| 3. BUTACAS VENDIDAS EN LA DIAGONAL PRINCIPAL                                    |"
					Escribir "| 4. BUTACAS VENDIDAS EN LA DIAGONAL SECUNDARIA                                   |"
					Escribir "| 5. BUTACAS VENDIDAS QUE EL VALOR DE LA COLUMNA PERTENEZCA A LA SERIE FIBONACCI  |" 
					Escribir "| 6. BUTACAS VENDIDAS QUE EL VALOR DE LA FILA PERTENEZCA A LA SERIE FIBONACCI     |"
					Escribir "| 7. TOTAL DE BUTACAS VENDIDAS EN FILAS                                           |"
					Escribir "| 8. TOTAL DE BUTACAS VENDIDAS EN COLUMNAS                                        |"
					Escribir "| 9. CANTIDAD DE BUTACAS VENDIDAS EN ADULTO MAYORES                               |"
					Escribir "| 10. CANTIDAD DE BUTACAS VENDIDAS EN ADULTO                                      |"
					Escribir "| 11. CANTIDAD DE BUTACAS VENDIDAS EN JOVENES                                     |"
					Escribir "| 12. BUTACAS VENDIDAS QUE EL VALOR DE LA FILA SEA UN NUMERO PRIMO                |"
					Escribir "| 13. BUTACAS VENDIDAS QUE EL VALOR DE LA COLUMNA SEA UN NUMERO PRIMO             |"
					Escribir "| 14. BUTACAS VENDIDAS QUE EL VALOR DE LA FILA SEA UN NUMERO PAR                  |"
					Escribir "| 15. BUTACAS VENDIDAS QUE EL VALOR DE LA COLUMNA SEA UN NUMERO PAR               |"
					Escribir "| 16. BUTACAS VENDIDAS QUE EL VALOR DE LA FILA SEA UN NUMERO IMPAR                |"
					Escribir "| 17. BUTACAS VENDIDAS QUE EL VALOR DE LA COLUMNA SEA UN NUMERO IMPAR             |"
					Escribir "| 18. MOSTRAR LA SALA TRANSPUESTA                                                 |"
					Escribir "| 19. SALIR                                                                       |"
					Escribir "*---------------------------------------------------------------------------------*"
					Escribir "OPCION: "
					Repetir
						Leer entradaMenu2
						valido <- Verdadero
						
						Si No EsNumeroEntero(entradaMenu2) Entonces
							Escribir "Error: SISTEMA ESPERA UN NUMERO ENTERO"
							valido <- Falso
						Sino
							menu <- ConvertirANumero(entradaMenu2)
						FinSi
					Hasta Que valido
					// Procesar opci�n
					Segun menu Hacer
						1:
							Escribir "*-------------------------------- Pel�culas----------*"
							Escribir "1.El d�a que la tierra explot� (ESP) - Clase A"
							Escribir "2. Godzilla minus one (ESP) - Clase C"
							Escribir "3. M�s extra�o que la ficci�n (ESP) - Clase B"
							Escribir "�Para que pel�cula desea hacer esta pregunta?"
							Escribir "*----------------------------------------------------*"
							Repetir
								Leer comprar_pelicula
								valido <- Verdadero
								Si No EsNumeroEntero(comprar_pelicula) Entonces
									Escribir "Error: Debe ingresar un n�mero"
									valido <- Falso
								Sino
									opcionComprar_pelicula <- ConvertirANumero(comprar_pelicula)
									Si opcionComprar_pelicula < 1 O opcionComprar_pelicula > 3 Entonces
										Escribir "Error: Opci�n debe ser entre 1-3"
										valido <- Falso
									FinSi
								FinSi
							Hasta Que valido
							Borrar Pantalla
							funcion_comprada<-pelicula_a_observar(funciones_front,EL_dia_que_la_tierra_explot�_back,godzilla_minus_one_back,m�s_extra�o_que_la_ficci�n_back,opcionComprar_pelicula)
							Segun opcionComprar_pelicula Hacer
								1:
									
									Segun funcion_comprada Hacer
										1:
											imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos)
											fila_butacas_mas_vendidas( EL_dia_que_la_tierra_explot�_back_asientos , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										2:
											imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos2)
											fila_butacas_mas_vendidas( EL_dia_que_la_tierra_explot�_back_asientos2 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										3:
											imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos3)
											fila_butacas_mas_vendidas( EL_dia_que_la_tierra_explot�_back_asientos3 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										4:
											imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos4)
											fila_butacas_mas_vendidas( EL_dia_que_la_tierra_explot�_back_asientos4 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										De Otro Modo:
											Escribir "Error al obtener la matriz"
									Fin Segun
								2:
									Segun funcion_comprada Hacer
										1:
											imp_asientos(Asientos_front,godzilla_minus_one_back_asientos)
											fila_butacas_mas_vendidas( godzilla_minus_one_back_asientos , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										2:
											imp_asientos(Asientos_front,godzilla_minus_one_back_asientos2)
											fila_butacas_mas_vendidas( godzilla_minus_one_back_asientos2 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										3:
											imp_asientos(Asientos_front,godzilla_minus_one_back_asientos3)
											fila_butacas_mas_vendidas( godzilla_minus_one_back_asientos3 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										4:
											imp_asientos(Asientos_front,godzilla_minus_one_back_asientos4)
											fila_butacas_mas_vendidas( godzilla_minus_one_back_asientos4 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										De Otro Modo:
											Escribir "Error al obtener la matriz"
									Fin Segun
								3:
									Segun funcion_comprada Hacer
										1:
											imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos)
											fila_butacas_mas_vendidas( m�s_extra�o_que_la_ficci�n_back_asientos , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										2:
											imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos2)
											fila_butacas_mas_vendidas( m�s_extra�o_que_la_ficci�n_back_asientos2 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										3:
											imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos3)
											fila_butacas_mas_vendidas( m�s_extra�o_que_la_ficci�n_back_asientos3 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										4:
											imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos4)
											fila_butacas_mas_vendidas( m�s_extra�o_que_la_ficci�n_back_asientos4 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										De Otro Modo:
											Escribir "Error al obtener la matriz"
									Fin Segun
								De Otro Modo:
									
							FinSegun
						2:
							Escribir "*-------------------------------- Pel�culas----------*"
							Escribir "1.El d�a que la tierra explot� (ESP) - Clase A"
							Escribir "2. Godzilla minus one (ESP) - Clase C"
							Escribir "3. M�s extra�o que la ficci�n (ESP) - Clase B"
							Escribir "�Para que pel�cula desea hacer esta pregunta?"
							Escribir "*----------------------------------------------------*"
							Repetir
								Leer comprar_pelicula
								valido <- Verdadero
								Si No EsNumeroEntero(comprar_pelicula) Entonces
									Escribir "Error: Debe ingresar un n�mero"
									valido <- Falso
								Sino
									opcionComprar_pelicula <- ConvertirANumero(comprar_pelicula)
									Si opcionComprar_pelicula < 1 O opcionComprar_pelicula > 3 Entonces
										Escribir "Error: Opci�n debe ser entre 1-3"
										valido <- Falso
									FinSi
								FinSi
							Hasta Que valido
							Borrar Pantalla
							funcion_comprada<-pelicula_a_observar(funciones_front,EL_dia_que_la_tierra_explot�_back,godzilla_minus_one_back,m�s_extra�o_que_la_ficci�n_back,opcionComprar_pelicula)
							Segun opcionComprar_pelicula Hacer
								1:
									
									Segun funcion_comprada Hacer
										1:
											imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos)
											columna_butacas_mas_vendidas( EL_dia_que_la_tierra_explot�_back_asientos , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										2:
											imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos2)
											columna_butacas_mas_vendidas( EL_dia_que_la_tierra_explot�_back_asientos2 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										3:
											imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos3)
											columna_butacas_mas_vendidas( EL_dia_que_la_tierra_explot�_back_asientos3 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										4:
											imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos4)
											columna_butacas_mas_vendidas( EL_dia_que_la_tierra_explot�_back_asientos4 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										De Otro Modo:
											Escribir "Error al obtener la matriz"
									Fin Segun
								2:
									Segun funcion_comprada Hacer
										1:
											imp_asientos(Asientos_front,godzilla_minus_one_back_asientos)
											columna_butacas_mas_vendidas( godzilla_minus_one_back_asientos , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										2:
											imp_asientos(Asientos_front,godzilla_minus_one_back_asientos2)
											columna_butacas_mas_vendidas( godzilla_minus_one_back_asientos2 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										3:
											imp_asientos(Asientos_front,godzilla_minus_one_back_asientos3)
											columna_butacas_mas_vendidas( godzilla_minus_one_back_asientos3 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										4:
											imp_asientos(Asientos_front,godzilla_minus_one_back_asientos4)
											columna_butacas_mas_vendidas( godzilla_minus_one_back_asientos4 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										De Otro Modo:
											Escribir "Error al obtener la matriz"
									Fin Segun
								3:
									Segun funcion_comprada Hacer
										1:
											imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos)
											columna_butacas_mas_vendidas( m�s_extra�o_que_la_ficci�n_back_asientos , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										2:
											imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos2)
											columna_butacas_mas_vendidas( m�s_extra�o_que_la_ficci�n_back_asientos2 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										3:
											imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos3)
											columna_butacas_mas_vendidas( m�s_extra�o_que_la_ficci�n_back_asientos3 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										4:
											imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos4)
											columna_butacas_mas_vendidas( m�s_extra�o_que_la_ficci�n_back_asientos4 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										De Otro Modo:
											Escribir "Error al obtener la matriz"
									Fin Segun
								De Otro Modo:
									
						    FinSegun
						3:
							Escribir "*-------------------------------- Pel�culas----------*"
							Escribir "1.El d�a que la tierra explot� (ESP) - Clase A"
							Escribir "2. Godzilla minus one (ESP) - Clase C"
							Escribir "3. M�s extra�o que la ficci�n (ESP) - Clase B"
							Escribir "�Para que pel�cula desea hacer esta pregunta?"
							Escribir "*----------------------------------------------------*"
							Repetir
								Leer comprar_pelicula
								valido <- Verdadero
								Si No EsNumeroEntero(comprar_pelicula) Entonces
									Escribir "Error: Debe ingresar un n�mero"
									valido <- Falso
								Sino
									opcionComprar_pelicula <- ConvertirANumero(comprar_pelicula)
									Si opcionComprar_pelicula < 1 O opcionComprar_pelicula > 3 Entonces
										Escribir "Error: Opci�n debe ser entre 1-3"
										valido <- Falso
									FinSi
								FinSi
							Hasta Que valido
							Borrar Pantalla
							funcion_comprada<-pelicula_a_observar(funciones_front,EL_dia_que_la_tierra_explot�_back,godzilla_minus_one_back,m�s_extra�o_que_la_ficci�n_back,opcionComprar_pelicula)
							Segun opcionComprar_pelicula Hacer
								1:
									
									Segun funcion_comprada Hacer
										1:
											imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos)
											diagonal_principal_butacas_vendidas( EL_dia_que_la_tierra_explot�_back_asientos , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										2:
											imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos2)
											diagonal_principal_butacas_vendidas( EL_dia_que_la_tierra_explot�_back_asientos2 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										3:
											imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos3)
											diagonal_principal_butacas_vendidas( EL_dia_que_la_tierra_explot�_back_asientos3 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										4:
											imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos4)
											diagonal_principal_butacas_vendidas( EL_dia_que_la_tierra_explot�_back_asientos4 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										De Otro Modo:
											Escribir "Error al obtener la matriz"
									Fin Segun
								2:
									Segun funcion_comprada Hacer
										1:
											imp_asientos(Asientos_front,godzilla_minus_one_back_asientos)
											diagonal_principal_butacas_vendidas( godzilla_minus_one_back_asientos , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										2:
											imp_asientos(Asientos_front,godzilla_minus_one_back_asientos2)
											diagonal_principal_butacas_vendidas( godzilla_minus_one_back_asientos2 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										3:
											imp_asientos(Asientos_front,godzilla_minus_one_back_asientos3)
											diagonal_principal_butacas_vendidas( godzilla_minus_one_back_asientos3 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										4:
											imp_asientos(Asientos_front,godzilla_minus_one_back_asientos4)
											diagonal_principal_butacas_vendidas( godzilla_minus_one_back_asientos4 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										De Otro Modo:
											Escribir "Error al obtener la matriz"
									Fin Segun
								3:
									Segun funcion_comprada Hacer
										1:
											imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos)
											diagonal_principal_butacas_vendidas( m�s_extra�o_que_la_ficci�n_back_asientos , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										2:
											imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos2)
											diagonal_principal_butacas_vendidas( m�s_extra�o_que_la_ficci�n_back_asientos2 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										3:
											imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos3)
											diagonal_principal_butacas_vendidas( m�s_extra�o_que_la_ficci�n_back_asientos3 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										4:
											imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos4)
											diagonal_principal_butacas_vendidas( m�s_extra�o_que_la_ficci�n_back_asientos4 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										De Otro Modo:
											Escribir "Error al obtener la matriz"
									Fin Segun
								De Otro Modo:
									
						    FinSegun
						4:
							Escribir "*-------------------------------- Pel�culas----------*"
							Escribir "1.El d�a que la tierra explot� (ESP) - Clase A"
							Escribir "2. Godzilla minus one (ESP) - Clase C"
							Escribir "3. M�s extra�o que la ficci�n (ESP) - Clase B"
							Escribir "�Para que pel�cula desea hacer esta pregunta?"
							Escribir "*----------------------------------------------------*"
							Repetir
								Leer comprar_pelicula
								valido <- Verdadero
								Si No EsNumeroEntero(comprar_pelicula) Entonces
									Escribir "Error: Debe ingresar un n�mero"
									valido <- Falso
								Sino
									opcionComprar_pelicula <- ConvertirANumero(comprar_pelicula)
									Si opcionComprar_pelicula < 1 O opcionComprar_pelicula > 3 Entonces
										Escribir "Error: Opci�n debe ser entre 1-3"
										valido <- Falso
									FinSi
								FinSi
							Hasta Que valido
							Borrar Pantalla
							funcion_comprada<-pelicula_a_observar(funciones_front,EL_dia_que_la_tierra_explot�_back,godzilla_minus_one_back,m�s_extra�o_que_la_ficci�n_back,opcionComprar_pelicula)
							Segun opcionComprar_pelicula Hacer
								1:
									
									Segun funcion_comprada Hacer
										1:
											imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos)
											diagonal_secundaria_butacas_vendidas( EL_dia_que_la_tierra_explot�_back_asientos , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										2:
											imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos2)
											diagonal_secundaria_butacas_vendidas( EL_dia_que_la_tierra_explot�_back_asientos2 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										3:
											imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos3)
											diagonal_secundaria_butacas_vendidas( EL_dia_que_la_tierra_explot�_back_asientos3 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										4:
											imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos4)
											diagonal_secundaria_butacas_vendidas( EL_dia_que_la_tierra_explot�_back_asientos4 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										De Otro Modo:
											Escribir "Error al obtener la matriz"
									Fin Segun
								2:
									Segun funcion_comprada Hacer
										1:
											imp_asientos(Asientos_front,godzilla_minus_one_back_asientos)
											diagonal_secundaria_butacas_vendidas( godzilla_minus_one_back_asientos , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										2:
											imp_asientos(Asientos_front,godzilla_minus_one_back_asientos2)
											diagonal_secundaria_butacas_vendidas( godzilla_minus_one_back_asientos2 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										3:
											imp_asientos(Asientos_front,godzilla_minus_one_back_asientos3)
											diagonal_secundaria_butacas_vendidas( godzilla_minus_one_back_asientos3 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										4:
											imp_asientos(Asientos_front,godzilla_minus_one_back_asientos4)
											diagonal_secundaria_butacas_vendidas( godzilla_minus_one_back_asientos4 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										De Otro Modo:
											Escribir "Error al obtener la matriz"
									Fin Segun
								3:
									Segun funcion_comprada Hacer
										1:
											imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos)
											diagonal_secundaria_butacas_vendidas( m�s_extra�o_que_la_ficci�n_back_asientos , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										2:
											imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos2)
											diagonal_secundaria_butacas_vendidas( m�s_extra�o_que_la_ficci�n_back_asientos2 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										3:
											imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos3)
											diagonal_secundaria_butacas_vendidas( m�s_extra�o_que_la_ficci�n_back_asientos3 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										4:
											imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos4)
											diagonal_secundaria_butacas_vendidas( m�s_extra�o_que_la_ficci�n_back_asientos4 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										De Otro Modo:
											Escribir "Error al obtener la matriz"
									Fin Segun
								De Otro Modo:
									
						    FinSegun
						5:
							Escribir "*-------------------------------- Pel�culas----------*"
							Escribir "1.El d�a que la tierra explot� (ESP) - Clase A"
							Escribir "2. Godzilla minus one (ESP) - Clase C"
							Escribir "3. M�s extra�o que la ficci�n (ESP) - Clase B"
							Escribir "�Para que pel�cula desea hacer esta pregunta?"
							Escribir "*----------------------------------------------------*"
							Repetir
								Leer comprar_pelicula
								valido <- Verdadero
								Si No EsNumeroEntero(comprar_pelicula) Entonces
									Escribir "Error: Debe ingresar un n�mero"
									valido <- Falso
								Sino
									opcionComprar_pelicula <- ConvertirANumero(comprar_pelicula)
									Si opcionComprar_pelicula < 1 O opcionComprar_pelicula > 3 Entonces
										Escribir "Error: Opci�n debe ser entre 1-3"
										valido <- Falso
									FinSi
								FinSi
							Hasta Que valido
							Borrar Pantalla
							funcion_comprada<-pelicula_a_observar(funciones_front,EL_dia_que_la_tierra_explot�_back,godzilla_minus_one_back,m�s_extra�o_que_la_ficci�n_back,opcionComprar_pelicula)
							Segun opcionComprar_pelicula Hacer
								1:
									
									Segun funcion_comprada Hacer
										1:
											imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos)
											columna_indice_fibonacci_butacas_vendidas( EL_dia_que_la_tierra_explot�_back_asientos , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										2:
											imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos2)
											columna_indice_fibonacci_butacas_vendidas( EL_dia_que_la_tierra_explot�_back_asientos2 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										3:
											imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos3)
											columna_indice_fibonacci_butacas_vendidas( EL_dia_que_la_tierra_explot�_back_asientos3 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										4:
											imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos4)
											columna_indice_fibonacci_butacas_vendidas( EL_dia_que_la_tierra_explot�_back_asientos4 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										De Otro Modo:
											Escribir "Error al obtener la matriz"
									Fin Segun
								2:
									Segun funcion_comprada Hacer
										1:
											imp_asientos(Asientos_front,godzilla_minus_one_back_asientos)
											columna_indice_fibonacci_butacas_vendidas( godzilla_minus_one_back_asientos , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										2:
											imp_asientos(Asientos_front,godzilla_minus_one_back_asientos2)
											columna_indice_fibonacci_butacas_vendidas( godzilla_minus_one_back_asientos2 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										3:
											imp_asientos(Asientos_front,godzilla_minus_one_back_asientos3)
											columna_indice_fibonacci_butacas_vendidas( godzilla_minus_one_back_asientos3 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										4:
											imp_asientos(Asientos_front,godzilla_minus_one_back_asientos4)
											columna_indice_fibonacci_butacas_vendidas( godzilla_minus_one_back_asientos4 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										De Otro Modo:
											Escribir "Error al obtener la matriz"
									Fin Segun
								3:
									Segun funcion_comprada Hacer
										1:
											imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos)
											columna_indice_fibonacci_butacas_vendidas( m�s_extra�o_que_la_ficci�n_back_asientos , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										2:
											imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos2)
											columna_indice_fibonacci_butacas_vendidas( m�s_extra�o_que_la_ficci�n_back_asientos2 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										3:
											imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos3)
											columna_indice_fibonacci_butacas_vendidas( m�s_extra�o_que_la_ficci�n_back_asientos3 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										4:
											imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos4)
											columna_indice_fibonacci_butacas_vendidas( m�s_extra�o_que_la_ficci�n_back_asientos4 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										De Otro Modo:
											Escribir "Error al obtener la matriz"
									Fin Segun
								De Otro Modo:
									
						    FinSegun
						6:
							Escribir "*-------------------------------- Pel�culas----------*"
							Escribir "1.El d�a que la tierra explot� (ESP) - Clase A"
							Escribir "2. Godzilla minus one (ESP) - Clase C"
							Escribir "3. M�s extra�o que la ficci�n (ESP) - Clase B"
							Escribir "�Para que pel�cula desea hacer esta pregunta?"
							Escribir "*----------------------------------------------------*"
							Repetir
								Leer comprar_pelicula
								valido <- Verdadero
								Si No EsNumeroEntero(comprar_pelicula) Entonces
									Escribir "Error: Debe ingresar un n�mero"
									valido <- Falso
								Sino
									opcionComprar_pelicula <- ConvertirANumero(comprar_pelicula)
									Si opcionComprar_pelicula < 1 O opcionComprar_pelicula > 3 Entonces
										Escribir "Error: Opci�n debe ser entre 1-3"
										valido <- Falso
									FinSi
								FinSi
							Hasta Que valido
							Borrar Pantalla
							funcion_comprada<-pelicula_a_observar(funciones_front,EL_dia_que_la_tierra_explot�_back,godzilla_minus_one_back,m�s_extra�o_que_la_ficci�n_back,opcionComprar_pelicula)
							Segun opcionComprar_pelicula Hacer
								1:
									
									Segun funcion_comprada Hacer
										1:
											imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos)
											fila_indice_fibonacci_butacas_vendidas( EL_dia_que_la_tierra_explot�_back_asientos , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										2:
											imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos2)
											fila_indice_fibonacci_butacas_vendidas( EL_dia_que_la_tierra_explot�_back_asientos2 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										3:
											imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos3)
											fila_indice_fibonacci_butacas_vendidas( EL_dia_que_la_tierra_explot�_back_asientos3 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										4:
											imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos4)
											fila_indice_fibonacci_butacas_vendidas( EL_dia_que_la_tierra_explot�_back_asientos4 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										De Otro Modo:
											Escribir "Error al obtener la matriz"
									Fin Segun
								2:
									Segun funcion_comprada Hacer
										1:
											imp_asientos(Asientos_front,godzilla_minus_one_back_asientos)
											fila_indice_fibonacci_butacas_vendidas( godzilla_minus_one_back_asientos , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										2:
											imp_asientos(Asientos_front,godzilla_minus_one_back_asientos2)
											fila_indice_fibonacci_butacas_vendidas( godzilla_minus_one_back_asientos2 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										3:
											imp_asientos(Asientos_front,godzilla_minus_one_back_asientos3)
											fila_indice_fibonacci_butacas_vendidas( godzilla_minus_one_back_asientos3 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										4:
											imp_asientos(Asientos_front,godzilla_minus_one_back_asientos4)
											fila_indice_fibonacci_butacas_vendidas( godzilla_minus_one_back_asientos4 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										De Otro Modo:
											Escribir "Error al obtener la matriz"
									Fin Segun
								3:
									Segun funcion_comprada Hacer
										1:
											imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos)
											fila_indice_fibonacci_butacas_vendidas( m�s_extra�o_que_la_ficci�n_back_asientos , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										2:
											imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos2)
											fila_indice_fibonacci_butacas_vendidas( m�s_extra�o_que_la_ficci�n_back_asientos2 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										3:
											imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos3)
											fila_indice_fibonacci_butacas_vendidas( m�s_extra�o_que_la_ficci�n_back_asientos3 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										4:
											imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos4)
											fila_indice_fibonacci_butacas_vendidas( m�s_extra�o_que_la_ficci�n_back_asientos4 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										De Otro Modo:
											Escribir "Error al obtener la matriz"
									Fin Segun
								De Otro Modo:
									
						    FinSegun
						7:
							Escribir "*-------------------------------- Pel�culas----------*"
							Escribir "1.El d�a que la tierra explot� (ESP) - Clase A"
							Escribir "2. Godzilla minus one (ESP) - Clase C"
							Escribir "3. M�s extra�o que la ficci�n (ESP) - Clase B"
							Escribir "�Para que pel�cula desea hacer esta pregunta?"
							Escribir "*----------------------------------------------------*"
							Repetir
								Leer comprar_pelicula
								valido <- Verdadero
								Si No EsNumeroEntero(comprar_pelicula) Entonces
									Escribir "Error: Debe ingresar un n�mero"
									valido <- Falso
								Sino
									opcionComprar_pelicula <- ConvertirANumero(comprar_pelicula)
									Si opcionComprar_pelicula < 1 O opcionComprar_pelicula > 3 Entonces
										Escribir "Error: Opci�n debe ser entre 1-3"
										valido <- Falso
									FinSi
								FinSi
							Hasta Que valido
							Borrar Pantalla
							funcion_comprada<-pelicula_a_observar(funciones_front,EL_dia_que_la_tierra_explot�_back,godzilla_minus_one_back,m�s_extra�o_que_la_ficci�n_back,opcionComprar_pelicula)
							Segun opcionComprar_pelicula Hacer
								1:
									
									Segun funcion_comprada Hacer
										1:
											imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos)
											total_butacas_vendidas_filas( EL_dia_que_la_tierra_explot�_back_asientos , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										2:
											imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos2)
											total_butacas_vendidas_filas( EL_dia_que_la_tierra_explot�_back_asientos2 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										3:
											imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos3)
											total_butacas_vendidas_filas( EL_dia_que_la_tierra_explot�_back_asientos3 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										4:
											imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos4)
											total_butacas_vendidas_filas( EL_dia_que_la_tierra_explot�_back_asientos4 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										De Otro Modo:
											Escribir "Error al obtener la matriz"
									Fin Segun
								2:
									Segun funcion_comprada Hacer
										1:
											imp_asientos(Asientos_front,godzilla_minus_one_back_asientos)
											total_butacas_vendidas_filas( godzilla_minus_one_back_asientos , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										2:
											imp_asientos(Asientos_front,godzilla_minus_one_back_asientos2)
											total_butacas_vendidas_filas( godzilla_minus_one_back_asientos2 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										3:
											imp_asientos(Asientos_front,godzilla_minus_one_back_asientos3)
											total_butacas_vendidas_filas( godzilla_minus_one_back_asientos3 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										4:
											imp_asientos(Asientos_front,godzilla_minus_one_back_asientos4)
											total_butacas_vendidas_filas( godzilla_minus_one_back_asientos4 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										De Otro Modo:
											Escribir "Error al obtener la matriz"
									Fin Segun
								3:
									Segun funcion_comprada Hacer
										1:
											imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos)
											total_butacas_vendidas_filas( m�s_extra�o_que_la_ficci�n_back_asientos , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										2:
											imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos2)
											total_butacas_vendidas_filas( m�s_extra�o_que_la_ficci�n_back_asientos2 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										3:
											imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos3)
											total_butacas_vendidas_filas( m�s_extra�o_que_la_ficci�n_back_asientos3 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										4:
											imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos4)
											total_butacas_vendidas_filas( m�s_extra�o_que_la_ficci�n_back_asientos4 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										De Otro Modo:
											Escribir "Error al obtener la matriz"
									Fin Segun
								De Otro Modo:
									
						    FinSegun
						8:
							Escribir "*-------------------------------- Pel�culas----------*"
							Escribir "1.El d�a que la tierra explot� (ESP) - Clase A"
							Escribir "2. Godzilla minus one (ESP) - Clase C"
							Escribir "3. M�s extra�o que la ficci�n (ESP) - Clase B"
							Escribir "�Para que pel�cula desea hacer esta pregunta?"
							Escribir "*----------------------------------------------------*"
							Repetir
								Leer comprar_pelicula
								valido <- Verdadero
								Si No EsNumeroEntero(comprar_pelicula) Entonces
									Escribir "Error: Debe ingresar un n�mero"
									valido <- Falso
								Sino
									opcionComprar_pelicula <- ConvertirANumero(comprar_pelicula)
									Si opcionComprar_pelicula < 1 O opcionComprar_pelicula > 3 Entonces
										Escribir "Error: Opci�n debe ser entre 1-3"
										valido <- Falso
									FinSi
								FinSi
							Hasta Que valido
							Borrar Pantalla
							funcion_comprada<-pelicula_a_observar(funciones_front,EL_dia_que_la_tierra_explot�_back,godzilla_minus_one_back,m�s_extra�o_que_la_ficci�n_back,opcionComprar_pelicula)
							Segun opcionComprar_pelicula Hacer
								1:
									
									Segun funcion_comprada Hacer
										1:
											imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos)
											total_butacas_vendidas_columnas( EL_dia_que_la_tierra_explot�_back_asientos , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										2:
											imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos2)
											total_butacas_vendidas_columnas( EL_dia_que_la_tierra_explot�_back_asientos2 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										3:
											imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos3)
											total_butacas_vendidas_columnas( EL_dia_que_la_tierra_explot�_back_asientos3 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										4:
											imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos4)
											total_butacas_vendidas_columnas( EL_dia_que_la_tierra_explot�_back_asientos4 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										De Otro Modo:
											Escribir "Error al obtener la matriz"
									Fin Segun
								2:
									Segun funcion_comprada Hacer
										1:
											imp_asientos(Asientos_front,godzilla_minus_one_back_asientos)
											total_butacas_vendidas_columnas( godzilla_minus_one_back_asientos , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										2:
											imp_asientos(Asientos_front,godzilla_minus_one_back_asientos2)
											total_butacas_vendidas_columnas( godzilla_minus_one_back_asientos2 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										3:
											imp_asientos(Asientos_front,godzilla_minus_one_back_asientos3)
											total_butacas_vendidas_columnas( godzilla_minus_one_back_asientos3 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										4:
											imp_asientos(Asientos_front,godzilla_minus_one_back_asientos4)
											total_butacas_vendidas_columnas( godzilla_minus_one_back_asientos4 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										De Otro Modo:
											Escribir "Error al obtener la matriz"
									Fin Segun
								3:
									Segun funcion_comprada Hacer
										1:
											imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos)
											total_butacas_vendidas_columnas( m�s_extra�o_que_la_ficci�n_back_asientos , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										2:
											imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos2)
											total_butacas_vendidas_columnas( m�s_extra�o_que_la_ficci�n_back_asientos2 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										3:
											imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos3)
											total_butacas_vendidas_columnas( m�s_extra�o_que_la_ficci�n_back_asientos3 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										4:
											imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos4)
											total_butacas_vendidas_columnas( m�s_extra�o_que_la_ficci�n_back_asientos4 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										De Otro Modo:
											Escribir "Error al obtener la matriz"
									Fin Segun
								De Otro Modo:
									
						    FinSegun
						9:
							Escribir "*-------------------------------- Pel�culas----------*"
							Escribir "1.El d�a que la tierra explot� (ESP) - Clase A"
							Escribir "2. Godzilla minus one (ESP) - Clase C"
							Escribir "3. M�s extra�o que la ficci�n (ESP) - Clase B"
							Escribir "�Para que pel�cula desea hacer esta pregunta?"
							Escribir "*----------------------------------------------------*"
							Repetir
								Leer comprar_pelicula
								valido <- Verdadero
								Si No EsNumeroEntero(comprar_pelicula) Entonces
									Escribir "Error: Debe ingresar un n�mero"
									valido <- Falso
								Sino
									opcionComprar_pelicula <- ConvertirANumero(comprar_pelicula)
									Si opcionComprar_pelicula < 1 O opcionComprar_pelicula > 3 Entonces
										Escribir "Error: Opci�n debe ser entre 1-3"
										valido <- Falso
									FinSi
								FinSi
							Hasta Que valido
							Borrar Pantalla
							funcion_comprada<-pelicula_a_observar(funciones_front,EL_dia_que_la_tierra_explot�_back,godzilla_minus_one_back,m�s_extra�o_que_la_ficci�n_back,opcionComprar_pelicula)
							Segun opcionComprar_pelicula Hacer
								1:
									
									Segun funcion_comprada Hacer
										1:
											imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos)
											total_adultos_mayores( EL_dia_que_la_tierra_explot�_back_asientos , columna , fila, butaca_adulto_mayor)
											Esperar Tecla
											Borrar Pantalla
										2:
											imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos2)
											total_adultos_mayores( EL_dia_que_la_tierra_explot�_back_asientos2 , columna , fila, butaca_adulto_mayor)
											Esperar Tecla
											Borrar Pantalla
										3:
											imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos3)
											total_adultos_mayores( EL_dia_que_la_tierra_explot�_back_asientos3 , columna , fila, butaca_adulto_mayor)
											Esperar Tecla
											Borrar Pantalla
										4:
											imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos4)
											total_adultos_mayores( EL_dia_que_la_tierra_explot�_back_asientos4 , columna , fila, butaca_adulto_mayor)
											Esperar Tecla
											Borrar Pantalla
										De Otro Modo:
											Escribir "Error al obtener la matriz"
									Fin Segun
								2:
									Segun funcion_comprada Hacer
										1:
											imp_asientos(Asientos_front,godzilla_minus_one_back_asientos)
											total_adultos_mayores( godzilla_minus_one_back_asientos , columna , fila, butaca_adulto_mayor)
											Esperar Tecla
											Borrar Pantalla
										2:
											imp_asientos(Asientos_front,godzilla_minus_one_back_asientos2)
											total_adultos_mayores( godzilla_minus_one_back_asientos2 , columna , fila,butaca_adulto_mayor)
											Esperar Tecla
											Borrar Pantalla
										3:
											imp_asientos(Asientos_front,godzilla_minus_one_back_asientos3)
											total_adultos_mayores( godzilla_minus_one_back_asientos3 , columna , fila, butaca_adulto_mayor)
											Esperar Tecla
											Borrar Pantalla
										4:
											imp_asientos(Asientos_front,godzilla_minus_one_back_asientos4)
											total_adultos_mayores( godzilla_minus_one_back_asientos4 , columna , fila,butaca_adulto_mayor)
											Esperar Tecla
											Borrar Pantalla
										De Otro Modo:
											Escribir "Error al obtener la matriz"
									Fin Segun
								3:
									Segun funcion_comprada Hacer
										1:
											imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos)
											total_adultos_mayores( m�s_extra�o_que_la_ficci�n_back_asientos , columna , fila, butaca_adulto_mayor)
											Esperar Tecla
											Borrar Pantalla
										2:
											imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos2)
											total_adultos_mayores( m�s_extra�o_que_la_ficci�n_back_asientos2 , columna , fila,butaca_adulto_mayor)
											Esperar Tecla
											Borrar Pantalla
										3:
											imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos3)
											total_adultos_mayores( m�s_extra�o_que_la_ficci�n_back_asientos3 , columna , fila, butaca_adulto_mayor)
											Esperar Tecla
											Borrar Pantalla
										4:
											imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos4)
											total_adultos_mayores( m�s_extra�o_que_la_ficci�n_back_asientos4 , columna , fila,butaca_adulto_mayor)
											Esperar Tecla
											Borrar Pantalla
										De Otro Modo:
											Escribir "Error al obtener la matriz"
									Fin Segun
								De Otro Modo:
									
						    FinSegun
						10:
							Escribir "*-------------------------------- Pel�culas----------*"
							Escribir "1.El d�a que la tierra explot� (ESP) - Clase A"
							Escribir "2. Godzilla minus one (ESP) - Clase C"
							Escribir "3. M�s extra�o que la ficci�n (ESP) - Clase B"
							Escribir "�Para que pel�cula desea hacer esta pregunta?"
							Escribir "*----------------------------------------------------*"
							Repetir
								Leer comprar_pelicula
								valido <- Verdadero
								Si No EsNumeroEntero(comprar_pelicula) Entonces
									Escribir "Error: Debe ingresar un n�mero"
									valido <- Falso
								Sino
									opcionComprar_pelicula <- ConvertirANumero(comprar_pelicula)
									Si opcionComprar_pelicula < 1 O opcionComprar_pelicula > 3 Entonces
										Escribir "Error: Opci�n debe ser entre 1-3"
										valido <- Falso
									FinSi
								FinSi
							Hasta Que valido
							Borrar Pantalla
							funcion_comprada<-pelicula_a_observar(funciones_front,EL_dia_que_la_tierra_explot�_back,godzilla_minus_one_back,m�s_extra�o_que_la_ficci�n_back,opcionComprar_pelicula)
							Segun opcionComprar_pelicula Hacer
								1:
									
									Segun funcion_comprada Hacer
										1:
											imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos)
											total_adultos( EL_dia_que_la_tierra_explot�_back_asientos , columna , fila,butaca_adulto)
											Esperar Tecla
											Borrar Pantalla
										2:
											imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos2)
											total_adultos( EL_dia_que_la_tierra_explot�_back_asientos2 , columna , fila, butaca_adulto)
											Esperar Tecla
											Borrar Pantalla
										3:
											imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos3)
											total_adultos( EL_dia_que_la_tierra_explot�_back_asientos3 , columna , fila,butaca_adulto)
											Esperar Tecla
											Borrar Pantalla
										4:
											imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos4)
											total_adultos( EL_dia_que_la_tierra_explot�_back_asientos4 , columna , fila,butaca_adulto)
											Esperar Tecla
											Borrar Pantalla
										De Otro Modo:
											Escribir "Error al obtener la matriz"
									Fin Segun
								2:
									Segun funcion_comprada Hacer
										1:
											imp_asientos(Asientos_front,godzilla_minus_one_back_asientos)
											total_adultos( godzilla_minus_one_back_asientos , columna , fila,butaca_adulto)
											Esperar Tecla
											Borrar Pantalla
										2:
											imp_asientos(Asientos_front,godzilla_minus_one_back_asientos2)
											total_adultos( godzilla_minus_one_back_asientos2 , columna , fila,butaca_adulto)
											Esperar Tecla
											Borrar Pantalla
										3:
											imp_asientos(Asientos_front,godzilla_minus_one_back_asientos3)
											total_adultos( godzilla_minus_one_back_asientos3 , columna , fila,butaca_adulto)
											Esperar Tecla
											Borrar Pantalla
										4:
											imp_asientos(Asientos_front,godzilla_minus_one_back_asientos4)
											total_adultos( godzilla_minus_one_back_asientos4 , columna , fila, butaca_adulto)
											Esperar Tecla
											Borrar Pantalla
										De Otro Modo:
											Escribir "Error al obtener la matriz"
									Fin Segun
								3:
									Segun funcion_comprada Hacer
										1:
											imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos)
											total_adultos( m�s_extra�o_que_la_ficci�n_back_asientos , columna , fila,butaca_adulto)
											Esperar Tecla
											Borrar Pantalla
										2:
											imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos2)
											total_adultos( m�s_extra�o_que_la_ficci�n_back_asientos2 , columna , fila,butaca_adulto)
											Esperar Tecla
											Borrar Pantalla
										3:
											imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos3)
											total_adultos( m�s_extra�o_que_la_ficci�n_back_asientos3 , columna , fila,butaca_adulto)
											Esperar Tecla
											Borrar Pantalla
										4:
											imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos4)
											total_adultos( m�s_extra�o_que_la_ficci�n_back_asientos4 , columna , fila,butaca_adulto)
											Esperar Tecla
											Borrar Pantalla
										De Otro Modo:
											Escribir "Error al obtener la matriz"
									Fin Segun
								De Otro Modo:
									
						    FinSegun
						11:
							Escribir "*-------------------------------- Pel�culas----------*"
							Escribir "1.El d�a que la tierra explot� (ESP) - Clase A"
							Escribir "2. Godzilla minus one (ESP) - Clase C"
							Escribir "3. M�s extra�o que la ficci�n (ESP) - Clase B"
							Escribir "�Para que pel�cula desea hacer esta pregunta?"
							Escribir "*----------------------------------------------------*"
							Repetir
								Leer comprar_pelicula
								valido <- Verdadero
								Si No EsNumeroEntero(comprar_pelicula) Entonces
									Escribir "Error: Debe ingresar un n�mero"
									valido <- Falso
								Sino
									opcionComprar_pelicula <- ConvertirANumero(comprar_pelicula)
									Si opcionComprar_pelicula < 1 O opcionComprar_pelicula > 3 Entonces
										Escribir "Error: Opci�n debe ser entre 1-3"
										valido <- Falso
									FinSi
								FinSi
							Hasta Que valido
							Borrar Pantalla
							funcion_comprada<-pelicula_a_observar(funciones_front,EL_dia_que_la_tierra_explot�_back,godzilla_minus_one_back,m�s_extra�o_que_la_ficci�n_back,opcionComprar_pelicula)
							Segun opcionComprar_pelicula Hacer
								1:
									
									Segun funcion_comprada Hacer
										1:
											imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos)
											total_jovenes( EL_dia_que_la_tierra_explot�_back_asientos , columna , fila,butaca_joven)
											Esperar Tecla
											Borrar Pantalla
										2:
											imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos2)
											total_jovenes( EL_dia_que_la_tierra_explot�_back_asientos2 , columna , fila,butaca_joven)
											Esperar Tecla
											Borrar Pantalla
										3:
											imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos3)
											total_jovenes( EL_dia_que_la_tierra_explot�_back_asientos3 , columna , fila,butaca_joven)
											Esperar Tecla
											Borrar Pantalla
										4:
											imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos4)
											total_jovenes( EL_dia_que_la_tierra_explot�_back_asientos4 , columna , fila,butaca_joven)
											Esperar Tecla
											Borrar Pantalla
										De Otro Modo:
											Escribir "Error al obtener la matriz"
									Fin Segun
								2:
									Segun funcion_comprada Hacer
										1:
											imp_asientos(Asientos_front,godzilla_minus_one_back_asientos)
											total_jovenes( godzilla_minus_one_back_asientos , columna , fila,butaca_joven)
											Esperar Tecla
											Borrar Pantalla
										2:
											imp_asientos(Asientos_front,godzilla_minus_one_back_asientos2)
											total_jovenes( godzilla_minus_one_back_asientos2 , columna , fila,butaca_joven)
											Esperar Tecla
											Borrar Pantalla
										3:
											imp_asientos(Asientos_front,godzilla_minus_one_back_asientos3)
											total_jovenes( godzilla_minus_one_back_asientos3 , columna , fila,butaca_joven)
											Esperar Tecla
											Borrar Pantalla
										4:
											imp_asientos(Asientos_front,godzilla_minus_one_back_asientos4)
											total_jovenes( godzilla_minus_one_back_asientos4 , columna , fila,butaca_joven)
											Esperar Tecla
											Borrar Pantalla
										De Otro Modo:
											Escribir "Error al obtener la matriz"
									Fin Segun
								3:
									Segun funcion_comprada Hacer
										1:
											imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos)
											total_jovenes( m�s_extra�o_que_la_ficci�n_back_asientos , columna , fila,butaca_joven)
											Esperar Tecla
											Borrar Pantalla
										2:
											imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos2)
											total_jovenes( m�s_extra�o_que_la_ficci�n_back_asientos2 , columna , fila,butaca_joven)
											Esperar Tecla
											Borrar Pantalla
										3:
											imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos3)
											total_jovenes( m�s_extra�o_que_la_ficci�n_back_asientos3 , columna , fila,butaca_joven)
											Esperar Tecla
											Borrar Pantalla
										4:
											imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos4)
											total_jovenes( m�s_extra�o_que_la_ficci�n_back_asientos4 , columna , fila,butaca_joven)
											Esperar Tecla
											Borrar Pantalla
										De Otro Modo:
											Escribir "Error al obtener la matriz"
									Fin Segun
								De Otro Modo:
									
						    FinSegun
						12:
							Escribir "*-------------------------------- Pel�culas----------*"
							Escribir "1.El d�a que la tierra explot� (ESP) - Clase A"
							Escribir "2. Godzilla minus one (ESP) - Clase C"
							Escribir "3. M�s extra�o que la ficci�n (ESP) - Clase B"
							Escribir "�Para que pel�cula desea hacer esta pregunta?"
							Escribir "*----------------------------------------------------*"
							Repetir
								Leer comprar_pelicula
								valido <- Verdadero
								Si No EsNumeroEntero(comprar_pelicula) Entonces
									Escribir "Error: Debe ingresar un n�mero"
									valido <- Falso
								Sino
									opcionComprar_pelicula <- ConvertirANumero(comprar_pelicula)
									Si opcionComprar_pelicula < 1 O opcionComprar_pelicula > 3 Entonces
										Escribir "Error: Opci�n debe ser entre 1-3"
										valido <- Falso
									FinSi
								FinSi
							Hasta Que valido
							Borrar Pantalla
							funcion_comprada<-pelicula_a_observar(funciones_front,EL_dia_que_la_tierra_explot�_back,godzilla_minus_one_back,m�s_extra�o_que_la_ficci�n_back,opcionComprar_pelicula)
							Segun opcionComprar_pelicula Hacer
								1:
									
									Segun funcion_comprada Hacer
										1:
											imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos)
											butaca_vendida_fila_prima( EL_dia_que_la_tierra_explot�_back_asientos , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										2:
											imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos2)
											butaca_vendida_fila_prima( EL_dia_que_la_tierra_explot�_back_asientos2 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										3:
											imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos3)
											butaca_vendida_fila_prima( EL_dia_que_la_tierra_explot�_back_asientos3 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										4:
											imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos4)
											butaca_vendida_fila_prima( EL_dia_que_la_tierra_explot�_back_asientos4 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										De Otro Modo:
											Escribir "Error al obtener la matriz"
									Fin Segun
								2:
									Segun funcion_comprada Hacer
										1:
											imp_asientos(Asientos_front,godzilla_minus_one_back_asientos)
											butaca_vendida_fila_prima( godzilla_minus_one_back_asientos , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										2:
											imp_asientos(Asientos_front,godzilla_minus_one_back_asientos2)
											butaca_vendida_fila_prima( godzilla_minus_one_back_asientos2 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										3:
											imp_asientos(Asientos_front,godzilla_minus_one_back_asientos3)
											butaca_vendida_fila_prima( godzilla_minus_one_back_asientos3 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										4:
											imp_asientos(Asientos_front,godzilla_minus_one_back_asientos4)
											butaca_vendida_fila_prima( godzilla_minus_one_back_asientos4 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										De Otro Modo:
											Escribir "Error al obtener la matriz"
									Fin Segun
								3:
									Segun funcion_comprada Hacer
										1:
											imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos)
											butaca_vendida_fila_prima( m�s_extra�o_que_la_ficci�n_back_asientos , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										2:
											imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos2)
											butaca_vendida_fila_prima( m�s_extra�o_que_la_ficci�n_back_asientos2 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										3:
											imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos3)
											butaca_vendida_fila_prima( m�s_extra�o_que_la_ficci�n_back_asientos3 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										4:
											imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos4)
											butaca_vendida_fila_prima( m�s_extra�o_que_la_ficci�n_back_asientos4 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										De Otro Modo:
											Escribir "Error al obtener la matriz"
									Fin Segun
								De Otro Modo:
									
						    FinSegun
						13:
							Escribir "*-------------------------------- Pel�culas----------*"
							Escribir "1.El d�a que la tierra explot� (ESP) - Clase A"
							Escribir "2. Godzilla minus one (ESP) - Clase C"
							Escribir "3. M�s extra�o que la ficci�n (ESP) - Clase B"
							Escribir "�Para que pel�cula desea hacer esta pregunta?"
							Escribir "*----------------------------------------------------*"
							Repetir
								Leer comprar_pelicula
								valido <- Verdadero
								Si No EsNumeroEntero(comprar_pelicula) Entonces
									Escribir "Error: Debe ingresar un n�mero"
									valido <- Falso
								Sino
									opcionComprar_pelicula <- ConvertirANumero(comprar_pelicula)
									Si opcionComprar_pelicula < 1 O opcionComprar_pelicula > 3 Entonces
										Escribir "Error: Opci�n debe ser entre 1-3"
										valido <- Falso
									FinSi
								FinSi
							Hasta Que valido
							Borrar Pantalla
							funcion_comprada<-pelicula_a_observar(funciones_front,EL_dia_que_la_tierra_explot�_back,godzilla_minus_one_back,m�s_extra�o_que_la_ficci�n_back,opcionComprar_pelicula)
							Segun opcionComprar_pelicula Hacer
								1:
									
									Segun funcion_comprada Hacer
										1:
											imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos)
											butaca_vendida_columna_prima( EL_dia_que_la_tierra_explot�_back_asientos , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										2:
											imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos2)
											butaca_vendida_columna_prima( EL_dia_que_la_tierra_explot�_back_asientos2 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										3:
											imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos3)
											butaca_vendida_columna_prima( EL_dia_que_la_tierra_explot�_back_asientos3 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										4:
											imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos4)
											butaca_vendida_columna_prima( EL_dia_que_la_tierra_explot�_back_asientos4 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										De Otro Modo:
											Escribir "Error al obtener la matriz"
									Fin Segun
								2:
									Segun funcion_comprada Hacer
										1:
											imp_asientos(Asientos_front,godzilla_minus_one_back_asientos)
											butaca_vendida_columna_prima( godzilla_minus_one_back_asientos , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										2:
											imp_asientos(Asientos_front,godzilla_minus_one_back_asientos2)
											butaca_vendida_columna_prima( godzilla_minus_one_back_asientos2 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										3:
											imp_asientos(Asientos_front,godzilla_minus_one_back_asientos3)
											butaca_vendida_columna_prima( godzilla_minus_one_back_asientos3 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										4:
											imp_asientos(Asientos_front,godzilla_minus_one_back_asientos4)
											butaca_vendida_columna_prima( godzilla_minus_one_back_asientos4 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										De Otro Modo:
											Escribir "Error al obtener la matriz"
									Fin Segun
								3:
									Segun funcion_comprada Hacer
										1:
											imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos)
											butaca_vendida_columna_prima( m�s_extra�o_que_la_ficci�n_back_asientos , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										2:
											imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos2)
											butaca_vendida_columna_prima( m�s_extra�o_que_la_ficci�n_back_asientos2 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										3:
											imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos3)
											butaca_vendida_columna_prima( m�s_extra�o_que_la_ficci�n_back_asientos3 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										4:
											imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos4)
											butaca_vendida_columna_prima( m�s_extra�o_que_la_ficci�n_back_asientos4 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										De Otro Modo:
											Escribir "Error al obtener la matriz"
									Fin Segun
								De Otro Modo:
									
						    FinSegun
						14:
							Escribir "*-------------------------------- Pel�culas----------*"
							Escribir "1.El d�a que la tierra explot� (ESP) - Clase A"
							Escribir "2. Godzilla minus one (ESP) - Clase C"
							Escribir "3. M�s extra�o que la ficci�n (ESP) - Clase B"
							Escribir "�Para que pel�cula desea hacer esta pregunta?"
							Escribir "*----------------------------------------------------*"
							Repetir
								Leer comprar_pelicula
								valido <- Verdadero
								Si No EsNumeroEntero(comprar_pelicula) Entonces
									Escribir "Error: Debe ingresar un n�mero"
									valido <- Falso
								Sino
									opcionComprar_pelicula <- ConvertirANumero(comprar_pelicula)
									Si opcionComprar_pelicula < 1 O opcionComprar_pelicula > 3 Entonces
										Escribir "Error: Opci�n debe ser entre 1-3"
										valido <- Falso
									FinSi
								FinSi
							Hasta Que valido
							Borrar Pantalla
							funcion_comprada<-pelicula_a_observar(funciones_front,EL_dia_que_la_tierra_explot�_back,godzilla_minus_one_back,m�s_extra�o_que_la_ficci�n_back,opcionComprar_pelicula)
							Segun opcionComprar_pelicula Hacer
								1:
									
									Segun funcion_comprada Hacer
										1:
											imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos)
											fila_indice_par_butacas_vendidas( EL_dia_que_la_tierra_explot�_back_asientos , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										2:
											imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos2)
											fila_indice_par_butacas_vendidas( EL_dia_que_la_tierra_explot�_back_asientos2 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										3:
											imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos3)
											fila_indice_par_butacas_vendidas( EL_dia_que_la_tierra_explot�_back_asientos3 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										4:
											imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos4)
											fila_indice_par_butacas_vendidas( EL_dia_que_la_tierra_explot�_back_asientos4 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										De Otro Modo:
											Escribir "Error al obtener la matriz"
									Fin Segun
								2:
									Segun funcion_comprada Hacer
										1:
											imp_asientos(Asientos_front,godzilla_minus_one_back_asientos)
											fila_indice_par_butacas_vendidas( godzilla_minus_one_back_asientos , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										2:
											imp_asientos(Asientos_front,godzilla_minus_one_back_asientos2)
											fila_indice_par_butacas_vendidas( godzilla_minus_one_back_asientos2 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										3:
											imp_asientos(Asientos_front,godzilla_minus_one_back_asientos3)
											fila_indice_par_butacas_vendidas( godzilla_minus_one_back_asientos3 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										4:
											imp_asientos(Asientos_front,godzilla_minus_one_back_asientos4)
											fila_indice_par_butacas_vendidas( godzilla_minus_one_back_asientos4 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										De Otro Modo:
											Escribir "Error al obtener la matriz"
									Fin Segun
								3:
									Segun funcion_comprada Hacer
										1:
											imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos)
											fila_indice_par_butacas_vendidas( m�s_extra�o_que_la_ficci�n_back_asientos , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										2:
											imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos2)
											fila_indice_par_butacas_vendidas( m�s_extra�o_que_la_ficci�n_back_asientos2 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										3:
											imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos3)
											fila_indice_par_butacas_vendidas( m�s_extra�o_que_la_ficci�n_back_asientos3 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										4:
											imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos4)
											fila_indice_par_butacas_vendidas( m�s_extra�o_que_la_ficci�n_back_asientos4 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										De Otro Modo:
											Escribir "Error al obtener la matriz"
									Fin Segun
								De Otro Modo:
									
						    FinSegun
						15:
							Escribir "*-------------------------------- Pel�culas----------*"
							Escribir "1.El d�a que la tierra explot� (ESP) - Clase A"
							Escribir "2. Godzilla minus one (ESP) - Clase C"
							Escribir "3. M�s extra�o que la ficci�n (ESP) - Clase B"
							Escribir "�Para que pel�cula desea hacer esta pregunta?"
							Escribir "*----------------------------------------------------*"
							Repetir
								Leer comprar_pelicula
								valido <- Verdadero
								Si No EsNumeroEntero(comprar_pelicula) Entonces
									Escribir "Error: Debe ingresar un n�mero"
									valido <- Falso
								Sino
									opcionComprar_pelicula <- ConvertirANumero(comprar_pelicula)
									Si opcionComprar_pelicula < 1 O opcionComprar_pelicula > 3 Entonces
										Escribir "Error: Opci�n debe ser entre 1-3"
										valido <- Falso
									FinSi
								FinSi
							Hasta Que valido
							Borrar Pantalla
							funcion_comprada<-pelicula_a_observar(funciones_front,EL_dia_que_la_tierra_explot�_back,godzilla_minus_one_back,m�s_extra�o_que_la_ficci�n_back,opcionComprar_pelicula)
							Segun opcionComprar_pelicula Hacer
								1:
									
									Segun funcion_comprada Hacer
										1:
											imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos)
											columna_indice_par_butacas_vendidas( EL_dia_que_la_tierra_explot�_back_asientos , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										2:
											imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos2)
											columna_indice_par_butacas_vendidas( EL_dia_que_la_tierra_explot�_back_asientos2 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										3:
											imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos3)
											columna_indice_par_butacas_vendidas( EL_dia_que_la_tierra_explot�_back_asientos3 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										4:
											imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos4)
											columna_indice_par_butacas_vendidas( EL_dia_que_la_tierra_explot�_back_asientos4 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										De Otro Modo:
											Escribir "Error al obtener la matriz"
									Fin Segun
								2:
									Segun funcion_comprada Hacer
										1:
											imp_asientos(Asientos_front,godzilla_minus_one_back_asientos)
											columna_indice_par_butacas_vendidas( godzilla_minus_one_back_asientos , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										2:
											imp_asientos(Asientos_front,godzilla_minus_one_back_asientos2)
											columna_indice_par_butacas_vendidas( godzilla_minus_one_back_asientos2 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										3:
											imp_asientos(Asientos_front,godzilla_minus_one_back_asientos3)
											columna_indice_par_butacas_vendidas( godzilla_minus_one_back_asientos3 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										4:
											imp_asientos(Asientos_front,godzilla_minus_one_back_asientos4)
											columna_indice_par_butacas_vendidas( godzilla_minus_one_back_asientos4 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										De Otro Modo:
											Escribir "Error al obtener la matriz"
									Fin Segun
								3:
									Segun funcion_comprada Hacer
										1:
											imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos)
											columna_indice_par_butacas_vendidas( m�s_extra�o_que_la_ficci�n_back_asientos , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										2:
											imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos2)
											columna_indice_par_butacas_vendidas( m�s_extra�o_que_la_ficci�n_back_asientos2 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										3:
											imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos3)
											columna_indice_par_butacas_vendidas( m�s_extra�o_que_la_ficci�n_back_asientos3 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										4:
											imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos4)
											columna_indice_par_butacas_vendidas( m�s_extra�o_que_la_ficci�n_back_asientos4 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										De Otro Modo:
											Escribir "Error al obtener la matriz"
									Fin Segun
								De Otro Modo:
									
						    FinSegun
						16:
							Escribir "*-------------------------------- Pel�culas----------*"
							Escribir "1.El d�a que la tierra explot� (ESP) - Clase A"
							Escribir "2. Godzilla minus one (ESP) - Clase C"
							Escribir "3. M�s extra�o que la ficci�n (ESP) - Clase B"
							Escribir "�Para que pel�cula desea hacer esta pregunta?"
							Escribir "*----------------------------------------------------*"
							Repetir
								Leer comprar_pelicula
								valido <- Verdadero
								Si No EsNumeroEntero(comprar_pelicula) Entonces
									Escribir "Error: Debe ingresar un n�mero"
									valido <- Falso
								Sino
									opcionComprar_pelicula <- ConvertirANumero(comprar_pelicula)
									Si opcionComprar_pelicula < 1 O opcionComprar_pelicula > 3 Entonces
										Escribir "Error: Opci�n debe ser entre 1-3"
										valido <- Falso
									FinSi
								FinSi
							Hasta Que valido
							Borrar Pantalla
							funcion_comprada<-pelicula_a_observar(funciones_front,EL_dia_que_la_tierra_explot�_back,godzilla_minus_one_back,m�s_extra�o_que_la_ficci�n_back,opcionComprar_pelicula)
							Segun opcionComprar_pelicula Hacer
								1:
									
									Segun funcion_comprada Hacer
										1:
											imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos)
											fila_indice_impar_butacas_vendidas( EL_dia_que_la_tierra_explot�_back_asientos , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										2:
											imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos2)
											fila_indice_impar_butacas_vendidas( EL_dia_que_la_tierra_explot�_back_asientos2 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										3:
											imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos3)
											fila_indice_impar_butacas_vendidas( EL_dia_que_la_tierra_explot�_back_asientos3 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										4:
											imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos4)
											fila_indice_impar_butacas_vendidas( EL_dia_que_la_tierra_explot�_back_asientos4 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										De Otro Modo:
											Escribir "Error al obtener la matriz"
									Fin Segun
								2:
									Segun funcion_comprada Hacer
										1:
											imp_asientos(Asientos_front,godzilla_minus_one_back_asientos)
											fila_indice_impar_butacas_vendidas( godzilla_minus_one_back_asientos , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										2:
											imp_asientos(Asientos_front,godzilla_minus_one_back_asientos2)
											fila_indice_impar_butacas_vendidas( godzilla_minus_one_back_asientos2 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										3:
											imp_asientos(Asientos_front,godzilla_minus_one_back_asientos3)
											fila_indice_impar_butacas_vendidas( godzilla_minus_one_back_asientos3 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										4:
											imp_asientos(Asientos_front,godzilla_minus_one_back_asientos4)
											fila_indice_impar_butacas_vendidas( godzilla_minus_one_back_asientos4 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										De Otro Modo:
											Escribir "Error al obtener la matriz"
									Fin Segun
								3:
									Segun funcion_comprada Hacer
										1:
											imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos)
											fila_indice_impar_butacas_vendidas( m�s_extra�o_que_la_ficci�n_back_asientos , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										2:
											imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos2)
											fila_indice_impar_butacas_vendidas( m�s_extra�o_que_la_ficci�n_back_asientos2 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										3:
											imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos3)
											fila_indice_impar_butacas_vendidas( m�s_extra�o_que_la_ficci�n_back_asientos3 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										4:
											imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos4)
											fila_indice_impar_butacas_vendidas( m�s_extra�o_que_la_ficci�n_back_asientos4 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										De Otro Modo:
											Escribir "Error al obtener la matriz"
									Fin Segun
								De Otro Modo:
									
						    FinSegun
						17:
							Escribir "*-------------------------------- Pel�culas----------*"
							Escribir "1.El d�a que la tierra explot� (ESP) - Clase A"
							Escribir "2. Godzilla minus one (ESP) - Clase C"
							Escribir "3. M�s extra�o que la ficci�n (ESP) - Clase B"
							Escribir "�Para que pel�cula desea hacer esta pregunta?"
							Escribir "*----------------------------------------------------*"
							Repetir
								Leer comprar_pelicula
								valido <- Verdadero
								Si No EsNumeroEntero(comprar_pelicula) Entonces
									Escribir "Error: Debe ingresar un n�mero"
									valido <- Falso
								Sino
									opcionComprar_pelicula <- ConvertirANumero(comprar_pelicula)
									Si opcionComprar_pelicula < 1 O opcionComprar_pelicula > 3 Entonces
										Escribir "Error: Opci�n debe ser entre 1-3"
										valido <- Falso
									FinSi
								FinSi
							Hasta Que valido
							Borrar Pantalla
							funcion_comprada<-pelicula_a_observar(funciones_front,EL_dia_que_la_tierra_explot�_back,godzilla_minus_one_back,m�s_extra�o_que_la_ficci�n_back,opcionComprar_pelicula)
							Segun opcionComprar_pelicula Hacer
								1:
									
									Segun funcion_comprada Hacer
										1:
											imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos)
											columna_indice_impar_butacas_vendidas( EL_dia_que_la_tierra_explot�_back_asientos , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										2:
											imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos2)
											columna_indice_impar_butacas_vendidas( EL_dia_que_la_tierra_explot�_back_asientos2 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										3:
											imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos3)
											columna_indice_impar_butacas_vendidas( EL_dia_que_la_tierra_explot�_back_asientos3 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										4:
											imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos4)
											columna_indice_impar_butacas_vendidas( EL_dia_que_la_tierra_explot�_back_asientos4 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										De Otro Modo:
											Escribir "Error al obtener la matriz"
									Fin Segun
								2:
									Segun funcion_comprada Hacer
										1:
											imp_asientos(Asientos_front,godzilla_minus_one_back_asientos)
											columna_indice_impar_butacas_vendidas( godzilla_minus_one_back_asientos , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										2:
											imp_asientos(Asientos_front,godzilla_minus_one_back_asientos2)
											columna_indice_impar_butacas_vendidas( godzilla_minus_one_back_asientos2 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										3:
											imp_asientos(Asientos_front,godzilla_minus_one_back_asientos3)
											columna_indice_impar_butacas_vendidas( godzilla_minus_one_back_asientos3 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										4:
											imp_asientos(Asientos_front,godzilla_minus_one_back_asientos4)
											columna_indice_impar_butacas_vendidas( godzilla_minus_one_back_asientos4 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										De Otro Modo:
											Escribir "Error al obtener la matriz"
									Fin Segun
								3:
									Segun funcion_comprada Hacer
										1:
											imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos)
											columna_indice_impar_butacas_vendidas( m�s_extra�o_que_la_ficci�n_back_asientos , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										2:
											imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos2)
											columna_indice_impar_butacas_vendidas( m�s_extra�o_que_la_ficci�n_back_asientos2 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										3:
											imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos3)
											columna_indice_impar_butacas_vendidas( m�s_extra�o_que_la_ficci�n_back_asientos3 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										4:
											imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos4)
											columna_indice_impar_butacas_vendidas( m�s_extra�o_que_la_ficci�n_back_asientos4 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										De Otro Modo:
											Escribir "Error al obtener la matriz"
									Fin Segun
								De Otro Modo:
									
						    FinSegun
						18:
							Escribir "*-------------------------------- Pel�culas----------*"
							Escribir "1.El d�a que la tierra explot� (ESP) - Clase A"
							Escribir "2. Godzilla minus one (ESP) - Clase C"
							Escribir "3. M�s extra�o que la ficci�n (ESP) - Clase B"
							Escribir "�Para que pel�cula desea hacer esta pregunta?"
							Escribir "*----------------------------------------------------*"
							Repetir
								Leer comprar_pelicula
								valido <- Verdadero
								Si No EsNumeroEntero(comprar_pelicula) Entonces
									Escribir "Error: Debe ingresar un n�mero"
									valido <- Falso
								Sino
									opcionComprar_pelicula <- ConvertirANumero(comprar_pelicula)
									Si opcionComprar_pelicula < 1 O opcionComprar_pelicula > 3 Entonces
										Escribir "Error: Opci�n debe ser entre 1-3"
										valido <- Falso
									FinSi
								FinSi
							Hasta Que valido
							Borrar Pantalla
							funcion_comprada<-pelicula_a_observar(funciones_front,EL_dia_que_la_tierra_explot�_back,godzilla_minus_one_back,m�s_extra�o_que_la_ficci�n_back,opcionComprar_pelicula)
							Segun opcionComprar_pelicula Hacer
								1:
									
									Segun funcion_comprada Hacer
										1:
											imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos)
											transpuesta( EL_dia_que_la_tierra_explot�_back_asientos , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										2:
											imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos2)
											transpuesta( EL_dia_que_la_tierra_explot�_back_asientos2 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										3:
											imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos3)
											transpuesta( EL_dia_que_la_tierra_explot�_back_asientos3 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										4:
											imp_asientos(Asientos_front,EL_dia_que_la_tierra_explot�_back_asientos4)
											transpuesta( EL_dia_que_la_tierra_explot�_back_asientos4 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										De Otro Modo:
											Escribir "Error al obtener la matriz"
									Fin Segun
								2:
									Segun funcion_comprada Hacer
										1:
											imp_asientos(Asientos_front,godzilla_minus_one_back_asientos)
											transpuesta( godzilla_minus_one_back_asientos , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										2:
											imp_asientos(Asientos_front,godzilla_minus_one_back_asientos2)
											transpuesta( godzilla_minus_one_back_asientos2 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										3:
											imp_asientos(Asientos_front,godzilla_minus_one_back_asientos3)
											transpuesta( godzilla_minus_one_back_asientos3 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										4:
											imp_asientos(Asientos_front,godzilla_minus_one_back_asientos4)
											transpuesta( godzilla_minus_one_back_asientos4 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										De Otro Modo:
											Escribir "Error al obtener la matriz"
									Fin Segun
								3:
									Segun funcion_comprada Hacer
										1:
											imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos)
											transpuesta( m�s_extra�o_que_la_ficci�n_back_asientos , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										2:
											imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos2)
											transpuesta( m�s_extra�o_que_la_ficci�n_back_asientos2 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										3:
											imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos3)
											transpuesta( m�s_extra�o_que_la_ficci�n_back_asientos3 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										4:
											imp_asientos(Asientos_front,m�s_extra�o_que_la_ficci�n_back_asientos4)
											transpuesta( m�s_extra�o_que_la_ficci�n_back_asientos4 , columna , fila, butaca_vacia , butaca_deteriorada)
											Esperar Tecla
											Borrar Pantalla
										De Otro Modo:
											Escribir "Error al obtener la matriz"
									Fin Segun
								De Otro Modo:
									
						    FinSegun
						19:
							Escribir  "SALIENDO DE MENU"
						De Otro Modo:
							Escribir "OPCION NO VALIDA";
					FinSegun
				Hasta Que menu = 19
			8:
				Escribir "Gracias por su visita!"
			De Otro Modo:
				Escribir "Opci�n no valida"
		FinSegun
	Hasta Que opcionMenuPrincipal = 8
FinAlgoritmo
Funcion  letra <- obtener_indice_columna ( indice )
	letra<-"A"
	Segun indice Hacer
		0:
			letra<-"A"
		1:
			letra<-"B"
		2:
			letra<-"C"
		3:
			letra<-"D"
		4:
			letra<-"E"
		5:
			letra<-"F"
		6:
			letra<-"G"
		7:
			letra<-"H"
		8:
			letra<-"I"
		9:
			letra<-"J"
		10:
			letra<-"K"
		De Otro Modo:
			Escribir "ERROR DE INDICE DE COLUMNA"
	Fin Segun
Fin Funcion
Funcion resultado <- es_fibonacci(num)
    Definir resultado Como Logico
    Definir a, b, c Como Entero
    resultado <- Falso
    Si num = 0 O num = 1 Entonces
        resultado <- Verdadero
	SiNo
		a <- 0
		b <- 1
		c <- a + b
		Mientras c <= num Hacer
			Si c = num Entonces
				resultado <- Verdadero
			FinSi
			a <- b
			b <- c
			c <- a + b
		FinMientras
    FinSi
FinFuncion
Funcion total_contador(contador)
	Si contador=0 Entonces
		Escribir  "NO HAY BUTACAS VENDIDAS"
	SiNo
		Escribir  "TOTAL DE BUTACAS VENDIDAS: " contador
	FinSi
FinFuncion
Funcion resultado <- es_primo(n)
	Definir resultado Como Logico
	Definir i Como Entero
	Si n <= 1 Entonces
        resultado <- Falso
    Sino Si n = 2 Entonces
			resultado <- Verdadero
		Sino Si n % 2 = 0 Entonces
				resultado <- Falso
			Sino
				resultado <- Verdadero
				i <- 2
				Mientras i <= (n/2) Hacer
					Si n % i = 0 Entonces
						resultado <- Falso
					FinSi
					i <- i + 1
				FinMientras
			FinSi
		FinSi
	FinSi
FinFuncion
Funcion fila_butacas_mas_vendidas(sala, columna, fila, butaca_vacia , butaca_deteriorada)
    Definir contador, i, j Como Entero
    Definir max_vendidas Como Entero
    Definir fila_maximo_valor Como Cadena
    
	max_vendidas <- 0
    fila_maximo_valor<-""
	Escribir  "FILA CON MAS BUTACAS VENDIDAS"
	
    Para i <- 0 Hasta columna-1 Hacer
        contador <- 0
        Para j <- 0 Hasta fila-1 Hacer
            Si sala[i,j] <> butaca_vacia y sala[i,j] <>butaca_deteriorada Entonces
                contador <- contador + 1
            FinSi
        FinPara
        Si contador > max_vendidas Entonces
            max_vendidas <- contador
            fila_maximo_valor<- ConvertirATexto(i+1)
		SiNo Si contador=max_vendidas Entonces
				fila_maximo_valor<- fila_maximo_valor + ", " + ConvertirATexto(i+1)
			FinSi
        FinSi
    FinPara
	Si max_vendidas = 0 Entonces
        Escribir "NO HAY BUTACAS VENDIDAS"
    Sino Si Longitud(fila_maximo_valor) >1 Entonces
			Escribir "FILAS CON MAS BUTACAS VENDIDAS: ", fila_maximo_valor, " CON ", max_vendidas, " VENTAS"			
		SiNo
			Escribir "FILA " fila_maximo_valor " CON MAS BUTACAS VENDIDAS ", " CON ", max_vendidas, " VENTAS"	
		FinSi
    FinSi
FinFuncion
Funcion columna_butacas_mas_vendidas(sala, columna, fila, butaca_vacia , butaca_deteriorada)
    Definir contador, i, j Como Entero
    Definir max_vendidas Como Entero
    Definir  columna_maximo_valor como Cadena 
	
	Escribir  "COLUMNA CON MAS BUTACAS VENDIDAS"
    
    max_vendidas <- 0
    Para j <- 0 Hasta fila-1 Hacer
        contador <- 0
        Para i <- 0 Hasta columna-1 Hacer
            Si sala[i,j] <> butaca_vacia y sala[i,j] <> butaca_deteriorada Entonces
                contador <- contador + 1
            FinSi
        FinPara
        Si contador > max_vendidas Entonces
            max_vendidas <- contador
            columna_maximo_valor<-ConvertirATexto(j + 1)
		SiNo Si contador=max_vendidas Entonces
				columna_maximo_valor<- columna_maximo_valor + ", " + ConvertirATexto(j+1)
			FinSi
        FinSi
    FinPara
    
    Si max_vendidas = 0 Entonces
        Escribir "NO HAY BUTACAS VENDIDAS EN NINGUNA COLUMNA"
    Sino Si Longitud(columna_maximo_valor) > 1 Entonces
			Escribir "COLUMNAS CON MAS BUTACAS VENDIDAS: ", columna_maximo_valor, " CON ", max_vendidas, " VENTAS"
		SiNo
			Escribir "COLUMNA " columna_maximo_valor " CON MAS BUTACAS VENDIDAS ", " CON ", max_vendidas, " VENTAS"	
		FinSi
		
    FinSi
FinFuncion

Funcion  diagonal_principal_butacas_vendidas ( sala, columna, fila, butaca_vacia , butaca_deteriorada )
	
	Escribir "BUTACAS VENDIDAS EN LA DIAGONAL PRINCIPAL"
	contador<- 0
	Para i<-0 Hasta columna-1 Hacer
		Para j<-0 Hasta fila-1 Hacer
			Si i=j y sala[i,j]<>butaca_vacia  y sala[i,j] <> butaca_deteriorada Entonces
				Escribir "BUTACAS [" obtener_indice_columna(i)  j+1 "]: " sala[i,j]
				contador<- contador + 1
			Fin Si
		Fin Para
	Fin Para
	total_contador(contador)
Fin Funcion
Funcion diagonal_secundaria_butacas_vendidas(sala, columna, fila, butaca_vacia , butaca_deteriorada)
	Definir i, j, contador Como Entero
	butaca_vacia<-0
	contador <- 0
	Escribir "BUTACAS VENDIDAS EN LA DIAGONAL SECUNDARIA"
	j<- fila-1
	Para i<-0 Hasta columna-1 Con Paso 1 Hacer
		Si j>=0 Entonces
			Si sala[i,j] <> butaca_vacia y sala[i,j] <> butaca_deteriorada Entonces
				Escribir "BUTACA:" "[1m[31m["  obtener_indice_columna(i) j+1 "[1m[31m]"
				contador <- contador + 1
			FinSi
		FinSi
		j <- j-1
	Fin Para	
	
	total_contador(contador)
	
FinFuncion
Funcion  columna_indice_fibonacci_butacas_vendidas( sala,columna, fila, butaca_vacia , butaca_deteriorada )
	Escribir  "BUTACAS VENDIDAS VALOR DE LA COLUMNA PERTENEZCA AL NUMERO FIBONACCI"
	Definir contador Como Entero
	contador <- 0
	Para j<-0 Hasta fila - 1 Hacer
		Si es_fibonacci(j+1) Entonces
			Para i<-0 Hasta columna - 1 Hacer
				Si sala[i,j]<>butaca_vacia y sala[i,j] <> butaca_deteriorada Entonces
					Escribir "BUTACAS [" obtener_indice_columna(i)  j+1 "]" 
					contador<- contador + 1
				Fin Si
			Fin Para
		Fin Si
	Fin Para
	total_contador(contador)
Fin Funcion

Funcion fila_indice_fibonacci_butacas_vendidas( sala, columna, fila, butaca_vacia , butaca_deteriorada )
	Escribir  "BUTACAS VENDIDAS VALOR DE LA FILA PERTENEZCA AL NUMERO FIBONACCI"
	Definir contador Como Entero
	contador <- 0
	Para i<-0 Hasta columna - 1 Hacer
		Si es_fibonacci(i+1) Entonces
			Para j<-0 Hasta fila - 1 Hacer
				Si sala[i,j]<>butaca_vacia y sala[i,j] <> butaca_deteriorada Entonces
					Escribir "BUTACAS [" obtener_indice_columna(i) j +1  "]"
					contador<- contador + 1
				Fin Si
			Fin Para
		Fin Si
	Fin Para
	total_contador(contador)
FinFuncion
Funcion total_butacas_vendidas_filas(sala, filas, columnas, butaca_vacia , butaca_deteriorada)
	Definir i, j, contador, total Como Entero
	
	total<-0
	
	Escribir  "TOTAL DE BUTACAS VENDIDAS EN CADA FILAS"
	Para i <- 0 Hasta filas-1 Hacer
		contador <- 0
		Para j <- 0 Hasta columnas-1 Hacer
			Si sala[i,j] <> butaca_vacia y sala[i,j] <> butaca_deteriorada Entonces
				contador <- contador + 1
				total<- total + 1
			FinSi
		FinPara
		Escribir "FILA ", i+1, ": ", contador, " BUTACAS VENDIDA"
	FinPara
	total_contador(total)
FinFuncion
Funcion total_butacas_vendidas_columnas(sala, fila, columna, butaca_vacia , butaca_deteriorada)
    Definir i, j, contador, total Como Entero
    total <- 0
	Escribir  "TOTAL DE BUTACAS VENDIDAS EN CADA COLUMNAS"
    Para j <- 0 Hasta columna-1 Hacer
        contador <- 0
        Para i <- 0 Hasta fila-1 Hacer
            Si sala[i,j] <> butaca_vacia y sala[i,j] <> butaca_deteriorada Entonces
                contador <- contador + 1
				total <- total + 1
            FinSi
        FinPara
        Escribir "COLUMNA ", j+1, ": ", contador, " BUTACAS VENDIDAS"
    FinPara
	total_contador(total)
FinFuncion
Funcion  total_adultos_mayores( sala,columna, fila, butaca_adulto_mayor )
	contador <-0
	Escribir "ADULTOS MAYORES"
	Para i<-0 Hasta columna-1 Hacer
		Para j<-0 Hasta fila-1 Hacer
			Si sala[i,j]=butaca_adulto_mayor Entonces
				contador<- contador + 1
			Fin Si
		Fin Para
	Fin Para
	Si contador<>0 Entonces
		Escribir  "TOTAL ADULTOS MAYORES : " contador
	SiNo
		Escribir "NO HAY ADULTOS MAYORES"
	Fin Si
	
Fin Funcion
Funcion  total_adultos( sala,columna, fila , butaca_adulto)
	contador <-0
	Escribir  "ADULTOS"
	Para i<-0 Hasta columna-1 Hacer
		Para j<-0 Hasta fila-1 Hacer
			Si sala[i,j]=butaca_adulto Entonces
				contador<- contador + 1
			Fin Si
		Fin Para
	Fin Para
	Si contador<>0 Entonces
		Escribir  "TOTAL ADULTOS : " contador
	SiNo
		Escribir "NO HAY ADULTOS"
	Fin Si
	
Fin Funcion

Funcion  total_jovenes( sala,columna, fila, butaca_joven)
	contador <-0
	Escribir  "JOVENES"
	Para i<-0 Hasta columna-1 Hacer
		Para j<-0 Hasta fila-1 Hacer
			Si sala[i,j]=butaca_joven Entonces
				contador<- contador + 1
			Fin Si
		Fin Para
	Fin Para
	Si contador<>0 Entonces
		Escribir  "TOTAL JOVENES: " contador
	SiNo
		Escribir "NO HAY JOVENES"
	Fin Si
	
Fin Funcion
Funcion  butaca_vendida_fila_prima( sala,columna, fila, butaca_vacia , butaca_deteriorada )
	Definir  contador como Entero
	contador <-0
	Escribir "BUTACAS VENDIDAS EN FILA CON INDICE QUE SEA NUMERO PRIMO"
	Para i<-0 Hasta columna - 1 Hacer
		Si es_primo(i+1) Entonces
			Para j<-0 Hasta fila - 1 Hacer
				Si sala[i,j]<>butaca_vacia y sala[i,j] <> butaca_deteriorada Entonces
					Escribir "BUTACAS [" obtener_indice_columna(i) j +1  "]: " sala[i,j]
					contador<- contador + 1
				Fin Si
			Fin Para
		Fin Si
	Fin Para
	total_contador(contador)
FinFuncion
Funcion  butaca_vendida_columna_prima( sala,columna, fila, butaca_vacia , butaca_deteriorada )
	Definir  contador como Entero
	contador <-0
	Escribir "BUTACAS VENDIDAS EN COLUMNA CON INDICE QUE SEA NUMERO PRIMO"
	Para j<-0 Hasta fila - 1 Hacer
		Si es_primo(j+1) Entonces
			Para i<-0 Hasta columna - 1 Hacer
				Si sala[i,j]<>butaca_vacia y sala[i,j] <> butaca_deteriorada Entonces
					Escribir "BUTACAS [" obtener_indice_columna(i) j +1  "]: " sala[i,j]
					contador<- contador + 1
				Fin Si
			Fin Para
		Fin Si
	Fin Para
	total_contador(contador)
FinFuncion
Funcion fila_indice_par_butacas_vendidas( sala, columna, fila, butaca_vacia , butaca_deteriorada )
	Escribir  "BUTACAS VENDIDAS VALOR DE LA FILA SEA UN NUMERO PAR"
	Definir contador Como Entero
	contador <- 0
	Para i<-0 Hasta columna - 1 Hacer
		Si (i+1)%2=0 Entonces
			Para j<-0 Hasta fila - 1 Hacer
				Si sala[i,j]<>butaca_vacia y sala[i,j] <> butaca_deteriorada Entonces
					Escribir "BUTACAS [" obtener_indice_columna(i) j +1  "]"
					contador<- contador + 1
				Fin Si
			Fin Para
		Fin Si
	Fin Para
	total_contador(contador)
FinFuncion

Funcion  columna_indice_par_butacas_vendidas( sala,columna, fila, butaca_vacia , butaca_deteriorada )
	Escribir  "BUTACAS VENDIDAS VALOR DE LA COLUMNA SEA UN NUMERO PAR"
	Definir contador Como Entero
	contador <- 0
	Para j<-0 Hasta fila - 1 Hacer
		Si (j+1)%2=0 Entonces
			Para i<-0 Hasta columna - 1 Hacer
				Si sala[i,j]<>butaca_vacia y sala[i,j] <> butaca_deteriorada Entonces
					Escribir "BUTACAS [" obtener_indice_columna(i)  j+1 "]" 
					contador<- contador + 1
				Fin Si
			Fin Para
		Fin Si
	Fin Para
	total_contador(contador)
Fin Funcion
Funcion fila_indice_impar_butacas_vendidas( sala, columna, fila, butaca_vacia , butaca_deteriorada )
	Escribir  "BUTACAS VENDIDAS VALOR DE LA FILA SEA UN NUMERO IMPAR"
	Definir contador Como Entero
	contador <- 0
	Para i<-0 Hasta columna - 1 Hacer
		Si (i+1)%2<>0 Entonces
			Para j<-0 Hasta fila - 1 Hacer
				Si sala[i,j]<>butaca_vacia y sala[i,j] <> butaca_deteriorada Entonces
					Escribir "BUTACAS [" obtener_indice_columna(i) j +1  "]"
					contador<- contador + 1
				Fin Si
			Fin Para
		Fin Si
	Fin Para
	total_contador(contador)
FinFuncion

Funcion  columna_indice_impar_butacas_vendidas( sala,columna, fila, butaca_vacia , butaca_deteriorada )
	Escribir  "BUTACAS VENDIDAS VALOR DE LA COLUMNA SEA UN NUMERO IMPAR"
	Definir contador Como Entero
	contador <- 0
	Para j<-0 Hasta fila - 1 Hacer
		Si (j+1)%2<>0 Entonces
			Para i<-0 Hasta columna - 1 Hacer
				Si sala[i,j]<>butaca_vacia y sala[i,j] <> butaca_deteriorada Entonces
					Escribir "BUTACAS [" obtener_indice_columna(i)  j+1 "]" 
					contador<- contador + 1
				Fin Si
			Fin Para
		Fin Si
	Fin Para
	total_contador(contador)
Fin Funcion
Funcion transpuesta(sala, columna, fila, butaca_vacia, butaca_deteriorada)
    Definir i, j Como Entero
	Escribir "SALA DE CINE TRANSPUESTA"
    Para i <- 0 Hasta fila - 1 Hacer
        Para j <- 0 Hasta columna - 1 Hacer
            Si sala[j,i]=butaca_vacia Entonces
				Escribir "[1m[36m[" + obtener_indice_columna(j) + ConvertirATexto(i+1) + "[1m[36m]" " "  Sin Saltar
			SiNo Si sala[j,i]=butaca_deteriorada Entonces
					Escribir  "[1m[34m[" + obtener_indice_columna(j) + ConvertirATexto(i+1) + "[1m[34m]" " " Sin Saltar
				SiNo
					Escribir "[1m[31m[" + obtener_indice_columna(j) + ConvertirATexto(i+1) + "[1m[31m]"  " " Sin Saltar
				FinSi
			FinSi
		FinPara
		Escribir "";
    FinPara
FinFuncion