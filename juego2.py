from random import randint, shuffle, sample, choice
import tkinter as tk
import time


#Clase para usarla luego con el times
class TimerState:
    def __init__(self):
        self.tiempo_inicio= time.time()
        self.tiempo_pausado= 0
        self.activo= True
        self.id= None

#Clase para todo el juego
class LexiReto:
    def __init__(self):
        self.app= tk.Tk()
        self.widgets= {}
        self.timer_state= TimerState()
        self.tiempo_oculto= False

        combinacionesLetras=[
        ["u", "a", "e", "r", "d", "j", "q"],
        ["p", "o", "u", "g", "e", "i", "s"],
        ["j", "e", "o", "c", "r", "p", "a"],
        ["n", "u", "e", "r", "l", "b", "a"],
        ["p", "i", "e", "u", "l", "j", "o"],
        ["v", "n", "i", "c", "r", "a", "u"],
        ["f", "s", "p", "t", "r", "a", "e"],
        ["e", "m", "n", "g", "c", "i", "o"],
        ["s", "d", "c", "u", "l", "i", "o"],
        ["l", "u", "i", "q", "r", "e", "o"]
        ]

        #Verifica  si la palabra es mayor a 3 letras, si contiene la letra central y si contiene algunas de las otras letras
        def verificarPalabra(palabraIngresada, letrasDisponibles, letraCentral):
            palabraIngresada= palabraIngresada.upper()
            if len(palabraIngresada)<3:
                return False
            if letraCentral not in palabraIngresada:
                return False
            for letra in palabraIngresada:
                if letra not in letrasDisponibles:
                    return False
            return True
        
        #Calcula si la palabra es Heptacrack (Contiene 7 letras distintas)
        def esHeptacrack(palabraIngresada):
            letrasUnicas = listaAleatoriaCombinaciones[:]
            for letra in letrasUnicas:
                if letra not in palabraIngresada.upper():
                    return False
            return True

        #Calcula el puntaje
        def calcularPuntaje(palabraIngresada):
            if esHeptacrack(palabraIngresada):
                return 10
            if (len(palabraIngresada)>=7):
                return len(palabraIngresada)
            elif(len(palabraIngresada)==6):
                return 6
            elif(len(palabraIngresada)==5):
                return 5 
            elif(len(palabraIngresada)==4):
                return 2
            else:
                return 1

        listaAleatoriaCombinaciones= []
        for letra in choice(combinacionesLetras):
            listaAleatoriaCombinaciones.append(letra.upper())
        letraCentral = listaAleatoriaCombinaciones[0]
        letras_sin_repetir= listaAleatoriaCombinaciones[:]

        seleccionadas= []
        #Abre el archivo "palabras.txt", escoge una lista de palabras, y lee, verifica y guarda las palabras que vaya leyendo en seleccionadas
        with open("palabras_potente.txt", "r", encoding="utf-8") as archivo:
            for linea in archivo:
                palabra = linea.strip().upper()
                es_valida = verificarPalabra(palabra, listaAleatoriaCombinaciones, letraCentral)
                if es_valida:
                    seleccionadas.append(palabra)

        #Contador para los puntos totales
        ptsTotal = 0
        #Listas para almacenar las palabras que se vayan ingresando en el juego
        palabrasElegidas0= []
        palabrasElegidas1 = []
        palabrasElegidas2 = []
        palabrasElegidas3 = []
        palabrasElegidas4 = []
        palabrasElegidas5 = []
        palabrasElegidas6 = []
        palabrasElegidas7 = []

        #Variable que almacena el puntaje por cada palabra
        pts= 0

        """print(seleccionadas)
        print("                               ↑                               ")
        print("Lista de seleccionados (solo de guía para completar el juego)\n")"""

        #Verifica si la palabra ingresada al clickear los botones, está en la lista de palabrasElegidas, y si cumple las condiciones necesarias
        #Además de Imprimir los pts obtenidos, totales, y verificar si se encontraron todas las palabras para terminar el juego
        def iniciarReto(palIngresada, mensajeLabel1, mensajeLabel2):
            nonlocal ptsTotal

            Pal = palIngresada
            if Pal in seleccionadas and Pal not in palabrasElegidas0:
                if verificarPalabra(Pal.upper(), listaAleatoriaCombinaciones, letraCentral):
                    pts = calcularPuntaje(Pal)
                    ptsTotal= ptsTotal + pts
                    palabrasElegidas0.append(Pal)
                    letra_inicial= Pal[0]
                    if letra_inicial==listaAleatoriaCombinaciones[0]:
                        palabrasElegidas1.append(Pal)
                    elif letra_inicial==listaAleatoriaCombinaciones[1]:
                        palabrasElegidas2.append(Pal)
                    elif letra_inicial==listaAleatoriaCombinaciones[2]:
                        palabrasElegidas3.append(Pal)
                    elif letra_inicial==listaAleatoriaCombinaciones[3]:
                        palabrasElegidas4.append(Pal)
                    elif letra_inicial==listaAleatoriaCombinaciones[4]:
                        palabrasElegidas5.append(Pal)
                    elif letra_inicial==listaAleatoriaCombinaciones[5]:
                        palabrasElegidas6.append(Pal)
                    elif letra_inicial==listaAleatoriaCombinaciones[6]:
                        palabrasElegidas7.append(Pal)
                    palabrasElegidasSinEspacios1= ", ".join(palabrasElegidas1)
                    palabrasElegidasSinEspacios2= ", ".join(palabrasElegidas2)
                    palabrasElegidasSinEspacios3= ", ".join(palabrasElegidas3)
                    palabrasElegidasSinEspacios4= ", ".join(palabrasElegidas4)
                    palabrasElegidasSinEspacios5= ", ".join(palabrasElegidas5)
                    palabrasElegidasSinEspacios6= ", ".join(palabrasElegidas6)
                    palabrasElegidasSinEspacios7= ", ".join(palabrasElegidas7)
                    if esHeptacrack(Pal)==True:
                        mensaje1.config(text=f"ES HEPTACRACK!\nHaz obtenido {pts} punto/s\nTienes {ptsTotal} punto/s en total")
                    else:
                        mensaje1.config(text=f"Haz obtenido {pts} punto/s\nTienes {ptsTotal} punto/s en total")
                    mensajeLabel2.config(text=f"Palabras encontradas: {len(palabrasElegidas0)}/{len(seleccionadas)}")
                    todas_letras = listaAleatoriaCombinaciones
                    listasPalabrasSinEspacios = [palabrasElegidas1, palabrasElegidas2, palabrasElegidas3, palabrasElegidas4, palabrasElegidas5, palabrasElegidas6, palabrasElegidas7]
                    for i in range(len(todas_letras)):
                        if i<len(listasPalabrasSinEspacios):
                            texto= f"Palabras encontradas con {todas_letras[i]}: {', '.join(listasPalabrasSinEspacios[i])}"
                            if i==0:
                                mensajePalabrasElegidas1.config(text=texto)
                            elif i==1:
                                mensajePalabrasElegidas2.config(text=texto)
                            elif i==2:
                                mensajePalabrasElegidas3.config(text=texto)
                            elif i==3:
                                mensajePalabrasElegidas4.config(text=texto)
                            elif i==4:
                                mensajePalabrasElegidas5.config(text=texto)
                            elif i==5:
                                mensajePalabrasElegidas6.config(text=texto)
                            elif i==6:
                                mensajePalabrasElegidas7.config(text=texto)
                    if len(palabrasElegidas0)==len(seleccionadas):
                        mostrarFelicitacionFinal()
                else:
                    mensajeLabel1.config(text=f"La palabra no contiene la letra {letraCentral} o es demasiado corta.")
            elif Pal in palabrasElegidas0:
                mensajeLabel1.config(text="Ya ingresaste esa palabra")
            else:
                mensajeLabel1.config(text="Palabra inválida")

        #Elimino la letra central de mi lista de "letras_sin_repetir" para mandarsela a la lista "letras_botones", ya que esa lista no necesita la letraCentral
        letras_botones= []
        for letra in letras_sin_repetir:
            if letra!=letraCentral:
                letras_botones.append(letra)

        #Quito la letra central de la lista de sin repetidos
        if letraCentral in letras_sin_repetir:
            letras_sin_repetir.remove(letraCentral)

        #Cuando se de clic al botón de "Aplicar" (Línea 332), verificará la palabra y cambiara el 
        #espacio llamado "ingresoLetras" (Línea 346) para volver a escribir otra palabra
        def aplicarEntrada():
            palabraIngresada= letra.get()
            iniciarReto(palabraIngresada, mensaje1, mensaje2)
            letra.set("")

        #Al ir dando clic a los botones, imprime en un espacio llamado "iniciarReto" (Línea 346) la letra que contiene cada botón y va generando la palabra
        def actualizarLetra(letra_boton):
            letra_actual= letra.get()
            letra.set(letra_actual+letra_boton)

        #En el espacio llamado "iniciarReto" (Línea 346), simplemente elimina la última letra que se ingreso
        def borrarUltimaLetra():
            texto_actual= letra.get()
            if len(texto_actual)>0:
                letra.set(texto_actual[:-1])

        #Funciones para cambiar el color de los botones cada que el cursor pase sobre ellos
        def onEnterLetrasApli(event):
            event.widget.config(bg="#4A90E2", fg='white')
        def onLeaveLetrasApli(event):
            event.widget.config(bg='SystemButtonFace', fg='black')

        def onEnterPausaIns(event):
            event.widget.config(bg="#999999", fg='white')
        def onLeavePausaIns(event):
            event.widget.config(bg='#999999', fg='black')

        def onEnterContinuar(event):
            event.widget.config(bg="#61d061", fg='black')
        def onLeaveContinuar(event):
            event.widget.config(bg='#44cc44', fg='white')

        def onEnterCerrar(event):
            event.widget.config(bg="#db6060", fg='black')
        def onLeaveCerrar(event):
            event.widget.config(bg='#cc4444', fg='white')

        def onEnterCentral(event):
            event.widget.config(bg="#fed155", fg='white')
        def onLeaveCentral(event):
            event.widget.config(bg='#ffc733', fg='black')

        #Al encontrar la cantidad de palabras generadas por el juego, muestra en la ventana un mensajede felicitaciones
        def mostrarFelicitacionFinal():
            capa= tk.Frame(
                self.app, 
                bg='white'
            )
            capa.place(
                relx=0, 
                rely=0, 
                relwidth=1, 
                relheight=1
            )

            mensaje= tk.Label(
                capa,
                text=f"¡Felicidades por ganar!🎉\nMis Estadísticas\nNombre de usuario: Marcelo López\nPuntaje obtenido: {ptsTotal}\n",
                font=("Courier", 16, "bold"),
                fg="green",
                bg="white",
                justify="center"
            )
            mensaje.pack(expand=True)

            #Botón para cerrar el juego
            cerrar_btn= tk.Button(
                capa,
                text="Cerrar juego",
                font=("Courier", 14),
                bg="#ff4444",
                fg="white",
                command=self.app.destroy
            )
            cerrar_btn.pack(
                pady=20
            )

            cerrar_btn.bind("<Enter>", onEnterCerrar) 
            cerrar_btn.bind("<Leave>", onLeaveCerrar)

        #Función para cuando se de clic al botón de "actualizar" (Línea 476), genere una nueva letra de las elegidas para cada botón
        def mezclarLetras():
            letras_nuevas = letras_botones[:]
            shuffle(letras_nuevas)
            boton1.config(text=letras_nuevas[0], command=lambda: actualizarLetra(letras_nuevas[0]))
            boton2.config(text=letras_nuevas[1], command=lambda: actualizarLetra(letras_nuevas[1]))
            boton3.config(text=letras_nuevas[2], command=lambda: actualizarLetra(letras_nuevas[2]))
            boton5.config(text=letras_nuevas[3], command=lambda: actualizarLetra(letras_nuevas[3]))
            boton6.config(text=letras_nuevas[4], command=lambda: actualizarLetra(letras_nuevas[4]))
            boton7.config(text=letras_nuevas[5], command=lambda: actualizarLetra(letras_nuevas[5]))


        letra= tk.StringVar(self.app)
        letra.set("")

        #Desde aquí hasta la línea 238, son funciones que realizan justamente lo que dicen sus nombres. Funciones que luego se llaman al pausar o continuar el juego
        timer_state = TimerState()
        tiempo_label = tk.Label(
            self.app, 
            text="00:00", 
            font=("Arial", 24), 
            bg="#282c34", 
            fg="white", 
            width=5, 
            anchor="center"
        )
        tiempo_label.place(
            relx= 0,
            rely= 0,
            width= 100,
            height= 30
        )

        self.widgets['label_tiempo'] = tiempo_label

        def actualizar_timer():
            if self.timer_state.activo:
                tiempo_transcurrido = time.time() - self.timer_state.tiempo_inicio
                minutos = int(tiempo_transcurrido // 60)
                segundos = int(tiempo_transcurrido % 60)
                if 'label_tiempo' in self.widgets and not self.tiempo_oculto:
                    self.widgets['label_tiempo'].config(text=f"{minutos:02d}:{segundos:02d}")
                self.timer_state.id = self.app.after(1000, actualizar_timer)

        def pausar_timer():
            if timer_state.activo:
                timer_state.activo = False
                timer_state.tiempo_pausado = time.time() - timer_state.tiempo_inicio
                if timer_state.id:
                    self.app.after_cancel(timer_state.id)

        def reanudar_timer():
            if not timer_state.activo:
                timer_state.tiempo_inicio = time.time() - timer_state.tiempo_pausado
                timer_state.activo = True
                actualizar_timer()

        self.tiempo_oculto= False

        def ocultar_mostrar_tiempo():
            self.tiempo_oculto = not self.tiempo_oculto
            if self.tiempo_oculto:
                self.widgets['label_tiempo'].config(text="--:--")
                self.widgets['boton_ocultar'].config(text="Mostrar")# ← Cambia el texto del botón
            else:
                actualizar_timer()
                self.widgets['boton_ocultar'].config(text="Ocultar")# ← Vuelve a "Ocultar"


        #Pausa el juego...
        def pausarJuego():
            pausar_timer()
            pausa_capa = tk.Frame(self.app, bg="#222222")
            pausa_capa.place(relx=0, rely=0, relwidth=1, relheight=1)

            mensaje_pausa = tk.Label(
                pausa_capa,
                text="⏸ Juego en Pausa ⏸",
                font=("Courier", 18, "bold"),
                fg="white",
                bg="#222222"
            )
            mensaje_pausa.pack(pady=50)

            #Botón para continuar el juego y el timer
            boton_continuar_pausa = tk.Button(
                pausa_capa,
                text="Continuar",
                font=("Courier", 14),
                bg="#44cc44",
                fg="white",
                command=lambda: [pausa_capa.destroy(), reanudar_timer()]
            )
            boton_continuar_pausa.pack(
                pady=20
            )

            boton_continuar_pausa.bind("<Enter>", onEnterContinuar) 
            boton_continuar_pausa.bind("<Leave>", onLeaveContinuar)

            #Botón para salir de la aplicación
            boton_salir_pausa = tk.Button(
                pausa_capa,
                text="Salir del Juego",
                font=("Courier", 14),
                bg="#cc4444",
                fg="white",
                command=self.app.destroy
            )
            boton_salir_pausa.pack(
                pady=10
            )

            boton_salir_pausa.bind("<Enter>", onEnterCerrar) 
            boton_salir_pausa.bind("<Leave>", onLeaveCerrar)

        def Instrucciones():
            instruccionesCapa= tk.Frame(self.app, bg="#222222")
            instruccionesCapa.place(relx=0, rely=0, relwidth=1, relheight=1)

            mensajeInstrucciones = tk.Label(
                instruccionesCapa,
                text="Cómo se juega",
                font=("Courier", 19, "bold"),
                fg="white",
                bg="#222222"
            )
            mensajeInstrucciones.pack(
                pady= 40
            )

            mensajeInstrucciones = tk.Label(
                instruccionesCapa,
                text="Forma palabras de al menos 3 letras. Puedes repetir las letras, pero siempre incluyendo la letra central.\n No se admiten nombres propios, plurales y formas verbales conjugadas (solo infinitivos).\n Encuentra palabras que incluyan las 7 letras (¡Heptacrack!).\n Puntuación: las palabras de 3 letras dan 1 punto y las de 4 letras, 2 puntos. A partir de 5 letras, obtendrás tantos puntos como letras tenga la palabra. Los heptacracks valen 10 puntos.",
                font=("Courier", 15),
                fg="white",
                bg="#222222",
                justify="center",
                wraplength=600,
            )
            mensajeInstrucciones.pack(
                pady= 10
            )

            #Botón para continuar el juego
            boton_continuar_instrucciones = tk.Button(
                instruccionesCapa,
                text="Continuar",
                font=("Courier", 14),
                bg="#44cc44",
                fg="white",
                command=lambda: [instruccionesCapa.destroy()]
            )
            boton_continuar_instrucciones.pack(
                pady=25
            )

            boton_continuar_instrucciones.bind("<Enter>", onEnterContinuar) 
            boton_continuar_instrucciones.bind("<Leave>", onLeaveContinuar)

        #Hace que el timer empieze nada más abrir el juego
        actualizar_timer()

        #Da un tamaño a la aplicación
        self.app.geometry("1300x700")
        tk.Wm.wm_title(self.app, "LexiReto")

        #Botón que ejecuta la función "pausarJuego"
        boton_pausa = tk.Button(
            self.app,
            text="⏸ Pausa",
            font=("Courier", 10),
            bg="#999999",
            command=pausarJuego
        )
        boton_pausa.place(
            x= 1200,
            y= 0,
            width=100,
            height=30
        )

        boton_pausa.bind("<Enter>", onEnterPausaIns) 
        boton_pausa.bind("<Leave>", onLeavePausaIns)

        #Espacio en donde se mostrarán las letras que se vayan ingresando mediante los botones
        ingresoLetras= tk.Label(
            self.app,
            text="",
            textvariable=letra,
            font=("Courier", 10),
            fg="white",
            bg="#333333",
            relief="ridge",
            justify="center",
            wraplength=190,
            width=30,
            height=3,
        )
        ingresoLetras.place(
            x= 10,
            y= 60,
            width= 250,
            height= 50
        )

        #A partir de acá, hasta la línea 440, son los botones en donde apareceran las letras escogidas
        boton1 = tk.Button(
            self.app,
            text=letras_botones[0],
            font=("Courier", 15),
            fg="black",
            relief="ridge",
            command=lambda: actualizarLetra(letras_botones[0])
        )
        boton1.place(
            x= 75,
            y= 120,
            width= 60,
            height= 40
        )

        boton1.bind("<Enter>", onEnterLetrasApli) 
        boton1.bind("<Leave>", onLeaveLetrasApli)

        boton2 = tk.Button(
            self.app,
            text=letras_botones[1],
            font=("Courier", 15),
            fg="black",
            relief="ridge",
            command=lambda: actualizarLetra(letras_botones[1])
        )
        boton2.place(
            x= 140,
            y= 120,
            width= 60,
            height= 40
        )

        boton2.bind("<Enter>", onEnterLetrasApli) 
        boton2.bind("<Leave>", onLeaveLetrasApli)

        boton3 = tk.Button(
            self.app,
            text=letras_botones[2],
            font=("Courier", 15),
            fg="black",
            relief="ridge",
            command=lambda: actualizarLetra(letras_botones[2])
        )
        boton3.place(
            x= 40,
            y= 185,
            width= 60,
            height= 40
        )

        boton3.bind("<Enter>", onEnterLetrasApli) 
        boton3.bind("<Leave>", onLeaveLetrasApli)

        boton4 = tk.Button(
            self.app,
            text=letraCentral.upper(),
            font=("Courier", 15),
            fg="black",
            bg="#ffc733",
            relief="ridge",
            command=lambda: actualizarLetra(letraCentral.upper())
        )
        boton4.place(
            x= 105,
            y= 185,
            width= 60,
            height= 40
        )

        boton4.bind("<Enter>", onEnterCentral) 
        boton4.bind("<Leave>", onLeaveCentral)

        boton5 = tk.Button(
            self.app,
            text=letras_botones[3],
            font=("Courier", 15),
            fg="black",
            relief="ridge",
            command=lambda: actualizarLetra(letras_botones[3])
        )
        boton5.place(
            x= 170,
            y= 185,
            width= 60,
            height= 40
        )

        boton5.bind("<Enter>", onEnterLetrasApli) 
        boton5.bind("<Leave>", onLeaveLetrasApli)

        boton6 = tk.Button(
            self.app,
            text=letras_botones[4],
            font=("Courier", 15),
            fg="black",
            relief="ridge",
            command=lambda: actualizarLetra(letras_botones[4])
        )
        boton6.place(
            x= 75,
            y= 250,
            width= 60,
            height= 40
        )

        boton6.bind("<Enter>", onEnterLetrasApli) 
        boton6.bind("<Leave>", onLeaveLetrasApli)

        boton7 = tk.Button(
            self.app,
            text=letras_botones[5],
            font=("Courier", 15),
            fg="black",
            relief="ridge",
            command=lambda: actualizarLetra(letras_botones[5])
        )
        boton7.place(
            x= 140,
            y= 250,
            width= 60,
            height= 40
        )

        boton7.bind("<Enter>", onEnterLetrasApli) 
        boton7.bind("<Leave>", onLeaveLetrasApli)

        #Botón que manda a la función "iniciarReto" la palabra ingresada
        aplicar= tk.Button(
            self.app,
            text=("Aplicar"),
            font=("Courier", 14),
            fg=("black"),
            command=aplicarEntrada ,
            relief="ridge"
        )
        aplicar.place(
            x= 10,
            y= 380,
            width= 100,
            height= 40
        )

        aplicar.bind("<Enter>", onEnterLetrasApli) 
        aplicar.bind("<Leave>", onLeaveLetrasApli)

        #Botón para mezclar las letras generadas entre los botones
        actualizar= tk.Button(
            self.app,
            text=("⟲"),
            font=("Courier", 15),
            fg=("black"),
            command=mezclarLetras,
            relief="ridge"
        )
        actualizar.place(
            x= 115,
            y= 380,
            width= 50,
            height= 40
        )

        actualizar.bind("<Enter>", onEnterLetrasApli) 
        actualizar.bind("<Leave>", onLeaveLetrasApli)

        #Botón para borrar la última letra ingresada
        borrar= tk.Button(
            self.app,
            text=("BORRAR"),
            font=("Courier", 14),
            fg=("black"),
            command=borrarUltimaLetra,
            relief="ridge"
        )
        borrar.place(
            x= 170,
            y= 380,
            width= 90,
            height= 40
        )

        borrar.bind("<Enter>", onEnterLetrasApli) 
        borrar.bind("<Leave>", onLeaveLetrasApli)

        comoJugar= tk.Button(
            self.app,
            text=("Cómo se juega"),
            font=("Courier", 10),
            bg="#999999",
            fg=("black"),
            command=Instrucciones
        )
        comoJugar.place(
            x= 650,
            y= 0,
            width= 130,
            height= 30
        )

        comoJugar.bind("<Enter>", onEnterPausaIns) 
        comoJugar.bind("<Leave>", onLeavePausaIns)

        boton_ocultar= tk.Button(
            self.app,
            text="Ocultar",
            font=("Courier", 10),
            bg="#999999",
            fg="black",
            command=ocultar_mostrar_tiempo
        )
        boton_ocultar.place(
            x=110,
            y=0,
            width=100,
            height=30
        )

        self.widgets['boton_ocultar']= boton_ocultar

        boton_ocultar.bind("<Enter>", onEnterPausaIns) 
        boton_ocultar.bind("<Leave>", onLeavePausaIns)

        #Imprime en un espacio la cantidad de puntos que se ganó en caso de acertar una palabra, y cuantos puntos tiene en total.
        #Esta opción técnicamente no está en el juego original, pero se puede dejar como un extra
        mensaje1 = tk.Label(
            self.app,
            text="",
            font=("Courier", 10),
            fg="white",
            bg="#333333",
            relief="ridge",
            justify="center",
            wraplength=250,
            width=30,
            height=3,
        )
        mensaje1.place(
            x= 10,
            y= 440,
            width= 250,
            height= 60
        )

        #Imprime en un espacio la cantidad de palabras que lleva encontradas el usuario
        mensaje2 = tk.Label(
            self.app,
            text=f"Palabras encontradas: {len(palabrasElegidas0)}/{len(seleccionadas)}",
            font=("Courier", 10),
            fg="white",
            bg="#333333",
            relief="ridge",
            justify="center",
            wraplength=400,
            width=35,
            height=5
        )
        mensaje2.place(
            x= 10,
            y= 310,
            width= 250,
            height= 50
        )

        mensajePalabrasElegidas1 = tk.Label(
            self.app,
            text=f"Palabras encontradas con {listaAleatoriaCombinaciones[0]}:",
            font=("Courier", 10),
            fg="white",
            bg="#333333",
            relief="ridge",
            justify="center",
            wraplength=950,
            width=35,
            height=5
        )
        mensajePalabrasElegidas1.place(
            x= 300,
            y= 60,
            width= 990,
            height= 80
        )

        mensajePalabrasElegidas2 = tk.Label(
            self.app,
            text=f"Palabras encontradas con {listaAleatoriaCombinaciones[1]}:",
            font=("Courier", 10),
            fg="white",
            bg="#333333",
            relief="ridge",
            justify="center",
            wraplength=950,
            width=35,
            height=5
        )
        mensajePalabrasElegidas2.place(
            x= 300,
            y= 150,
            width= 990,
            height= 80
        )

        mensajePalabrasElegidas3 = tk.Label(
            self.app,
            text=f"Palabras encontradas con {listaAleatoriaCombinaciones[2]}:",
            font=("Courier", 10),
            fg="white",
            bg="#333333",
            relief="ridge",
            justify="center",
            wraplength=950,
            width=35,
            height=5
        )
        mensajePalabrasElegidas3.place(
            x= 300,
            y= 240,
            width= 990,
            height= 80
        )

        mensajePalabrasElegidas4 = tk.Label(
            self.app,
            text=f"Palabras encontradas con {listaAleatoriaCombinaciones[3]}:",
            font=("Courier", 10),
            fg="white",
            bg="#333333",
            relief="ridge",
            justify="center",
            wraplength=950,
            width=35,
            height=5
        )
        mensajePalabrasElegidas4.place(
            x= 300,
            y= 330,
            width= 990,
            height= 80
        )

        mensajePalabrasElegidas5 = tk.Label(
            self.app,
            text=f"Palabras encontradas con {listaAleatoriaCombinaciones[4]}:",
            font=("Courier", 10),
            fg="white",
            bg="#333333",
            relief="ridge",
            justify="center",
            wraplength=950,
            width=35,
            height=5
        )
        mensajePalabrasElegidas5.place(
            x= 300,
            y= 420,
            width= 990,
            height= 80
        )

        mensajePalabrasElegidas6 = tk.Label(
            self.app,
            text=f"Palabras encontradas con {listaAleatoriaCombinaciones[5]}:",
            font=("Courier", 10),
            fg="white",
            bg="#333333",
            relief="ridge",
            justify="center",
            wraplength=950,
            width=35,
            height=5
        )
        mensajePalabrasElegidas6.place(
            x= 300,
            y= 510,
            width= 990,
            height= 80
        )

        mensajePalabrasElegidas7 = tk.Label(
            self.app,
            text=f"Palabras encontradas con {listaAleatoriaCombinaciones[6]}:",
            font=("Courier", 10),
            fg="white",
            bg="#333333",
            relief="ridge",
            justify="center",
            wraplength=950,
            width=35,
            height=5
        )
        mensajePalabrasElegidas7.place(
            x= 300,
            y= 600,
            width= 990,
            height= 80
        )


def iniciarJuego2(user):
    juego = LexiReto(user)
    juego.root.mainloop()
