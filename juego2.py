from random import shuffle, choice
import tkinter as tk
import time

COLOR_FONDO = "#f0f4f8"
COLOR_BOTON = "#6fbf73"
COLOR_BOTON_HOVER = "lightgreen"
COLOR_SECUNDARIO = "#4a90e2"
COLOR_TEXTO = "#333333"
COLOR_ROJO = "#ff4444"
FUENTE_TITULO = ("Segoe UI", 32, "bold")
FUENTE_ETIQUETA = ("Segoe UI", 16)
FUENTE_ETIQUETAB = ("Segoe UI", 16, "bold")
FUENTE_ETIQUETA_2 = ("Segoe UI", 14)
FUENTE_BOTON = ("Segoe UI", 12, "bold")


# Clase para usarla luego con el times
class TimerState:
    def __init__(self):
        self.tiempo_inicio = time.time()
        self.tiempo_pausado = 0
        self.activo = True
        self.id = None


# Clase para todo el juego
class LexiReto:
    def __init__(self, user, root):
        self.juego = tk.Toplevel(root)
        self.juego.attributes("-fullscreen", True)
        self.widgets = {}
        self.timer_state = TimerState()
        self.tiempo_oculto = False

        self.combinacionesLetras = [
            ["u", "a", "e", "r", "d", "j", "q"],
            ["p", "o", "u", "g", "e", "i", "s"],
            ["j", "e", "o", "c", "r", "p", "a"],
            ["n", "u", "e", "r", "l", "b", "a"],
            ["p", "i", "e", "u", "l", "j", "o"],
            ["v", "n", "i", "c", "r", "a", "u"],
            ["f", "s", "p", "t", "r", "a", "e"],
            ["e", "m", "n", "g", "c", "i", "o"],
            ["s", "d", "c", "u", "l", "i", "o"],
            ["l", "u", "i", "q", "r", "e", "o"],
        ]

        self.tiempo_oculto = False
        self.listaAleatoriaCombinaciones = []
        for letra in choice(self.combinacionesLetras):
            self.listaAleatoriaCombinaciones.append(letra.upper())
        self.letraCentral = self.listaAleatoriaCombinaciones[0]
        self.letras_sin_repetir = self.listaAleatoriaCombinaciones[:]
        self.seleccionadas = []
        # Abre el archivo "palabras.txt", escoge una lista de palabras, y lee, verifica y guarda las palabras que vaya leyendo en self.seleccionadas
        with open("palabras_potente.txt", "r", encoding="utf-8") as archivo:
            for linea in archivo:
                palabra = linea.strip().upper()
                es_valida = self.verificarPalabra(
                    palabra, self.listaAleatoriaCombinaciones, self.letraCentral
                )
                if es_valida:
                    self.seleccionadas.append(palabra)

        # Contador para los puntos totales
        self.ptsTotal = 0
        # Listas para almacenar las palabras que se vayan ingresando en el juego
        self.palabrasElegidas0 = []
        self.palabrasElegidas1 = []
        self.palabrasElegidas2 = []
        self.palabrasElegidas3 = []
        self.palabrasElegidas4 = []
        self.palabrasElegidas5 = []
        self.palabrasElegidas6 = []
        self.palabrasElegidas7 = []

        letra = tk.StringVar(self.juego)
        letra.set("")

        # son funciones que realizan justamente lo que dicen sus nombres. Funciones que luego se llaman al pausar o continuar el juego
        self.timer_state = TimerState()
        tiempo_label = tk.Label(
            self.juego,
            text="00:00",
            font=FUENTE_ETIQUETAB,
            bg=COLOR_TEXTO,
            fg="white",
            width=5,
            anchor="center",
        )
        tiempo_label.place(relx=0, rely=0, width=100, height=30)

        self.widgets["label_tiempo"] = tiempo_label
        # Hace que el timer empieze nada más abrir el juego
        self.actualizar_timer()

        # Botón que ejecuta la función "pausarJuego"
        boton_pausa = tk.Button(
            self.juego,
            text="⏸ Pausa",
            font=FUENTE_BOTON,
            bg=COLOR_BOTON,
            command=self.pausarJuego,
        )
        boton_pausa.place(x=1200, y=0, width=100, height=30)

        boton_pausa.bind("<Enter>", self.onEnterPausaIns)
        boton_pausa.bind("<Leave>", self.onLeavePausaIns)

        # Espacio en donde se mostrarán las letras que se vayan ingresando mediante los botones
        ingresoLetras = tk.Label(
            self.juego,
            text="",
            textvariable=letra,
            font=FUENTE_ETIQUETA_2,
            fg="white",
            bg=COLOR_TEXTO,
            relief="ridge",
            justify="center",
            wraplength=190,
            width=30,
            height=3,
        )
        ingresoLetras.place(x=10, y=60, width=250, height=50)

        # Elimino la letra central de mi lista de "letras_sin_repetir" para mandarsela a la lista "letras_botones", ya que esa lista no necesita la letraCentral
        self.letras_botones = []
        for letra in self.letras_sin_repetir:
            if letra != self.letraCentral:
                self.letras_botones.append(letra)

        # Quito la letra central de la lista de sin repetidos
        if self.letraCentral in self.letras_sin_repetir:
            self.letras_sin_repetir.remove(self.letraCentral)

        # A partir de acá, hasta la línea 440, son los botones en donde apareceran las letras escogidas
        boton1 = tk.Button(
            self.juego,
            text=self.letras_botones[0],
            font=FUENTE_BOTON,
            fg=COLOR_TEXTO,
            relief="ridge",
            command=lambda: self.actualizarLetra(self.letras_botones[0]),
        )
        boton1.place(x=75, y=120, width=60, height=40)

        boton1.bind("<Enter>", self.onEnterLetrasApli)
        boton1.bind("<Leave>", self.onLeaveLetrasApli)

        boton2 = tk.Button(
            self.juego,
            text=self.letras_botones[1],
            font=FUENTE_BOTON,
            fg=COLOR_TEXTO,
            relief="ridge",
            command=lambda: self.actualizarLetra(self.letras_botones[1]),
        )
        boton2.place(x=140, y=120, width=60, height=40)

        boton2.bind("<Enter>", self.onEnterLetrasApli)
        boton2.bind("<Leave>", self.onLeaveLetrasApli)

        boton3 = tk.Button(
            self.juego,
            text=self.letras_botones[2],
            font=FUENTE_BOTON,
            fg=COLOR_TEXTO,
            relief="ridge",
            command=lambda: self.actualizarLetra(self.letras_botones[2]),
        )
        boton3.place(x=40, y=185, width=60, height=40)

        boton3.bind("<Enter>", self.onEnterLetrasApli)
        boton3.bind("<Leave>", self.onLeaveLetrasApli)

        boton4 = tk.Button(
            self.juego,
            text=self.letraCentral.upper(),
            font=FUENTE_BOTON,
            fg="black",
            bg="#ffc733",
            relief="ridge",
            command=lambda: self.actualizarLetra(self.letraCentral.upper()),
        )
        boton4.place(x=105, y=185, width=60, height=40)

        boton4.bind("<Enter>", self.onEnterCentral)
        boton4.bind("<Leave>", self.onLeaveCentral)

        boton5 = tk.Button(
            self.juego,
            text=self.letras_botones[3],
            font=FUENTE_BOTON,
            fg=COLOR_TEXTO,
            relief="ridge",
            command=lambda: self.actualizarLetra(self.letras_botones[3]),
        )
        boton5.place(x=170, y=185, width=60, height=40)

        boton5.bind("<Enter>", self.onEnterLetrasApli)
        boton5.bind("<Leave>", self.onLeaveLetrasApli)

        boton6 = tk.Button(
            self.juego,
            text=self.letras_botones[4],
            font=FUENTE_BOTON,
            fg=COLOR_TEXTO,
            relief="ridge",
            command=lambda: self.actualizarLetra(self.letras_botones[4]),
        )
        boton6.place(x=75, y=250, width=60, height=40)

        boton6.bind("<Enter>", self.onEnterLetrasApli)
        boton6.bind("<Leave>", self.onLeaveLetrasApli)

        boton7 = tk.Button(
            self.juego,
            text=self.letras_botones[5],
            font=FUENTE_BOTON,
            fg=COLOR_TEXTO,
            relief="ridge",
            command=lambda: self.actualizarLetra(self.letras_botones[5]),
        )
        boton7.place(x=140, y=250, width=60, height=40)

        boton7.bind("<Enter>", self.onEnterLetrasApli)
        boton7.bind("<Leave>", self.onLeaveLetrasApli)

        # Botón que manda a la función "iniciarReto" la palabra ingresada
        aplicar = tk.Button(
            self.juego,
            text=("Aplicar"),
            font=FUENTE_BOTON,
            fg=COLOR_TEXTO,
            command=self.aplicarEntrada,
            relief="ridge",
        )
        aplicar.place(x=10, y=380, width=100, height=40)

        aplicar.bind("<Enter>", self.onEnterLetrasApli)
        aplicar.bind("<Leave>", self.onLeaveLetrasApli)

        # Botón para mezclar las letras generadas entre los botones
        actualizar = tk.Button(
            self.juego,
            text=("⟲"),
            font=("Courier", 15),
            fg=COLOR_TEXTO,
            command=self.mezclarLetras,
            relief="ridge",
        )
        actualizar.place(x=115, y=380, width=50, height=40)

        actualizar.bind("<Enter>", self.onEnterLetrasApli)
        actualizar.bind("<Leave>", self.onLeaveLetrasApli)

        # Botón para borrar la última letra ingresada
        borrar = tk.Button(
            self.juego,
            text=("BORRAR"),
            font=FUENTE_BOTON,
            fg=COLOR_TEXTO,
            command=self.borrarUltimaLetra,
            relief="ridge",
        )
        borrar.place(x=170, y=380, width=90, height=40)

        borrar.bind("<Enter>", self.onEnterLetrasApli)
        borrar.bind("<Leave>", self.onLeaveLetrasApli)

        comoJugar = tk.Button(
            self.juego,
            text=("Cómo se juega"),
            font=FUENTE_BOTON,
            bg=COLOR_BOTON,
            fg=COLOR_TEXTO,
            command=self.instrucciones,
        )
        comoJugar.place(x=650, y=0, width=130, height=30)

        comoJugar.bind("<Enter>", self.onEnterPausaIns)
        comoJugar.bind("<Leave>", self.onLeavePausaIns)

        boton_ocultar = tk.Button(
            self.juego,
            text="Ocultar",
            font=FUENTE_BOTON,
            bg=COLOR_BOTON,
            fg=COLOR_TEXTO,
            command=self.ocultar_mostrar_tiempo,
        )
        boton_ocultar.place(x=110, y=0, width=100, height=30)

        self.widgets["boton_ocultar"] = boton_ocultar

        boton_ocultar.bind("<Enter>", self.onEnterPausaIns)
        boton_ocultar.bind("<Leave>", self.onLeavePausaIns)

        # Imprime en un espacio la cantidad de puntos que se ganó en caso de acertar una palabra, y cuantos puntos tiene en total.
        # Esta opción técnicamente no está en el juego original, pero se puede dejar como un extra
        self.mensaje1 = tk.Label(
            self.juego,
            text="",
            font=FUENTE_ETIQUETA_2,
            fg="white",
            bg=COLOR_TEXTO,
            relief="ridge",
            justify="center",
            wraplength=250,
            width=30,
            height=3,
        )
        self.mensaje1.place(x=10, y=440, width=250, height=60)

        # Imprime en un espacio la cantidad de palabras que lleva encontradas el usuario
        mensaje2 = tk.Label(
            self.juego,
            text=f"Palabras encontradas: {len(self.palabrasElegidas0)}/{len(self.seleccionadas)}",
            font=FUENTE_ETIQUETA_2,
            fg="white",
            bg=COLOR_TEXTO,
            relief="ridge",
            justify="center",
            wraplength=400,
            width=35,
            height=5,
        )
        mensaje2.place(x=10, y=310, width=250, height=50)

        mensajePalabrasElegidas1 = tk.Label(
            self.juego,
            text=f"Palabras encontradas con {self.listaAleatoriaCombinaciones[0]}:",
            font=FUENTE_ETIQUETA_2,
            fg="white",
            bg=COLOR_TEXTO,
            relief="ridge",
            justify="center",
            wraplength=950,
            width=35,
            height=5,
        )
        mensajePalabrasElegidas1.place(x=300, y=60, width=990, height=80)

        mensajePalabrasElegidas2 = tk.Label(
            self.juego,
            text=f"Palabras encontradas con {self.listaAleatoriaCombinaciones[1]}:",
            font=FUENTE_ETIQUETA_2,
            fg="white",
            bg=COLOR_TEXTO,
            relief="ridge",
            justify="center",
            wraplength=950,
            width=35,
            height=5,
        )
        mensajePalabrasElegidas2.place(x=300, y=150, width=990, height=80)

        mensajePalabrasElegidas3 = tk.Label(
            self.juego,
            text=f"Palabras encontradas con {self.listaAleatoriaCombinaciones[2]}:",
            font=FUENTE_ETIQUETA_2,
            fg="white",
            bg=COLOR_TEXTO,
            relief="ridge",
            justify="center",
            wraplength=950,
            width=35,
            height=5,
        )
        mensajePalabrasElegidas3.place(x=300, y=240, width=990, height=80)

        mensajePalabrasElegidas4 = tk.Label(
            self.juego,
            text=f"Palabras encontradas con {self.listaAleatoriaCombinaciones[3]}:",
            font=FUENTE_ETIQUETA_2,
            fg="white",
            bg=COLOR_TEXTO,
            relief="ridge",
            justify="center",
            wraplength=950,
            width=35,
            height=5,
        )
        mensajePalabrasElegidas4.place(x=300, y=330, width=990, height=80)

        mensajePalabrasElegidas5 = tk.Label(
            self.juego,
            text=f"Palabras encontradas con {self.listaAleatoriaCombinaciones[4]}:",
            font=FUENTE_ETIQUETA_2,
            fg="white",
            bg=COLOR_TEXTO,
            relief="ridge",
            justify="center",
            wraplength=950,
            width=35,
            height=5,
        )
        mensajePalabrasElegidas5.place(x=300, y=420, width=990, height=80)

        mensajePalabrasElegidas6 = tk.Label(
            self.juego,
            text=f"Palabras encontradas con {self.listaAleatoriaCombinaciones[5]}:",
            font=FUENTE_ETIQUETA_2,
            fg="white",
            bg=COLOR_TEXTO,
            relief="ridge",
            justify="center",
            wraplength=950,
            width=35,
            height=5,
        )
        mensajePalabrasElegidas6.place(x=300, y=510, width=990, height=80)

        mensajePalabrasElegidas7 = tk.Label(
            self.juego,
            text=f"Palabras encontradas con {self.listaAleatoriaCombinaciones[6]}:",
            font=FUENTE_ETIQUETA_2,
            fg="white",
            bg=COLOR_TEXTO,
            relief="ridge",
            justify="center",
            wraplength=950,
            width=35,
            height=5,
        )
        mensajePalabrasElegidas7.place(x=300, y=600, width=990, height=80)
    
    # Verifica si la palabra es mayor a 3 letras, si contiene la letra central y si contiene algunas de las otras letras
    def verificarPalabra(self, palabraIngresada, letrasDisponibles):
        if len(palabraIngresada) < 3:
            return False
        if self.letraCentral not in palabraIngresada:
            return False
        for letra in palabraIngresada:
            if letra not in letrasDisponibles:
                return False
        return True

    # Calcula si la palabra es Heptacrack (Contiene 7 letras distintas)
    def esHeptacrack(self, palabraIngresada):
        letrasUnicas = self.listaAleatoriaCombinaciones[:]
        for letra in letrasUnicas:
            if letra not in palabraIngresada.upper():
                return False
        return True


    # Calcula el puntaje
    def calcularPuntaje(self, palabraIngresada):
        if self.esHeptacrack(palabraIngresada):
            return 10
        if len(palabraIngresada) >= 7:
            return len(palabraIngresada)
        elif len(palabraIngresada) == 6:
            return 6
        elif len(palabraIngresada) == 5:
            return 5
        elif len(palabraIngresada) == 4:
            return 2
        else:
            return 1



    """print(self.seleccionadas)
    print("                               ↑                               ")
    print("Lista de seleccionados (solo de guía para completar el juego)\n")"""

    # Verifica si la palabra ingresada al clickear los botones, está en la lista de palabrasElegidas, y si cumple las condiciones necesarias
    # Además de Imprimir los pts obtenidos, totales, y verificar si se encontraron todas las palabras para terminar el juego
    def iniciarReto(self, palIngresada, mensajeLabel1, mensajeLabel2):
        Pal = palIngresada.upper()
        if not self.verificarPalabra(Pal, self.listaAleatoriaCombinaciones, self.letraCentral):
            mensajeLabel1.config(
                text=f"La palabra no contiene la letra {self.letraCentral} o es demasiado corta."
            )
            return
        if Pal not in self.seleccionadas:
            mensajeLabel1.config(text="Palabra inválida")
            return
        if Pal in self.palabrasElegidas0:
            mensajeLabel1.config(text="Ya ingresaste esa palabra")
            return

        pts = self.calcularPuntaje(Pal)
        self.ptsTotal += pts
        self.palabrasElegidas0.append(Pal)
        letra_inicial = Pal[0]
        if letra_inicial == self.listaAleatoriaCombinaciones[0]:
            self.palabrasElegidas1.append(Pal)
        elif letra_inicial == self.listaAleatoriaCombinaciones[1]:
            self.palabrasElegidas2.append(Pal)
        elif letra_inicial == self.listaAleatoriaCombinaciones[2]:
            self.palabrasElegidas3.append(Pal)
        elif letra_inicial == self.listaAleatoriaCombinaciones[3]:
            self.palabrasElegidas4.append(Pal)
        elif letra_inicial == self.listaAleatoriaCombinaciones[4]:
            self.palabrasElegidas5.append(Pal)
        elif letra_inicial == self.listaAleatoriaCombinaciones[5]:
            self.palabrasElegidas6.append(Pal)
        elif letra_inicial == self.listaAleatoriaCombinaciones[6]:
            self.palabrasElegidas7.append(Pal)

        if self.esHeptacrack(Pal):
            self.mensaje1.config(
                text=f"ES HEPTACRACK!\nHaz obtenido {pts} punto/s\nTienes {self.ptsTotal} punto/s en total"
            )
        else:
            self.mensaje1.config(
                text=f"Haz obtenido {pts} punto/s\nTienes {self.ptsTotal} punto/s en total"
            )

        mensajeLabel2.config(
            text=f"Palabras encontradas: {len(self.palabrasElegidas0)}/{len(self.seleccionadas)}"
        )
        todas_letras = self.listaAleatoriaCombinaciones
        listasPalabrasSinEspacios = [
            self.palabrasElegidas1,
            self.palabrasElegidas2,
            self.palabrasElegidas3,
            self.palabrasElegidas4,
            self.palabrasElegidas5,
            self.palabrasElegidas6,
            self.palabrasElegidas7,
        ]

        for i in range(len(todas_letras)):
            if i < len(listasPalabrasSinEspacios):
                texto = f"Palabras encontradas con {todas_letras[i]}: {', '.join(listasPalabrasSinEspacios[i])}"
                if i == 0:
                    self.mensajePalabrasElegidas1.config(text=texto)
                elif i == 1:
                    self.mensajePalabrasElegidas2.config(text=texto)
                elif i == 2:
                    self.mensajePalabrasElegidas3.config(text=texto)
                elif i == 3:
                    self.mensajePalabrasElegidas4.config(text=texto)
                elif i == 4:
                    self.mensajePalabrasElegidas5.config(text=texto)
                elif i == 5:
                    self.mensajePalabrasElegidas6.config(text=texto)
                elif i == 6:
                    self.mensajePalabrasElegidas7.config(text=texto)

        if len(self.palabrasElegidas0) == len(self.seleccionadas):
            self.mostrarFelicitacionFinal()


    # Cuando se de clic al botón de "Aplicar" (Línea 332), verificará la palabra y cambiara el
    # espacio llamado "ingresoLetras" (Línea 346) para volver a escribir otra palabra
    def aplicarEntrada(self):
        palabraIngresada = self.letra.get()
        self.iniciarReto(palabraIngresada, self.mensaje1, self.mensaje2)
        self.letra.set("")

    # Al ir dando clic a los botones, imprime en un espacio llamado "iniciarReto" (Línea 346) la letra que contiene cada botón y va generando la palabra
    def actualizarLetra(self, letra_boton):
        letra_actual = self.letra.get()
        self.letra.set(letra_actual + letra_boton)

    # En el espacio llamado "iniciarReto" (Línea 346), simplemente elimina la última letra que se ingreso
    def borrarUltimaLetra(self):
        texto_actual = self.letra.get()
        if len(texto_actual) > 0:
            self.letra.set(texto_actual[:-1])

    # Funciones para cambiar el color de los botones cada que el cursor pase sobre ellos
    def onEnterLetrasApli(self, event):
        event.widget.config(bg=COLOR_BOTON_HOVER, fg="white")

    def onLeaveLetrasApli(self, event):
        event.widget.config(bg="SystemButtonFace", fg="black")

    def onEnterPausaIns(self, event):
        event.widget.config(bg=COLOR_BOTON_HOVER, fg="white")

    def onLeavePausaIns(self, event):
        event.widget.config(bg=COLOR_BOTON, fg="black")

    def onEnterContinuar(self, event):
        event.widget.config(bg=COLOR_BOTON_HOVER, fg="black")

    def onLeaveContinuar(self, event):
        event.widget.config(bg=COLOR_BOTON, fg="white")

    def onEnterCerrar(self, event):
        event.widget.config(bg="#db6060", fg="black")

    def onLeaveCerrar(self, event):
        event.widget.config(bg="#cc4444", fg="white")

    def onEnterCentral(self, event):
        event.widget.config(bg="#fed155", fg="white")

    def onLeaveCentral(self,event):
        event.widget.config(bg="#ffc733", fg="black")

    # Al encontrar la cantidad de palabras generadas por el juego, muestra en la ventana un mensajede felicitaciones
    def mostrarFelicitacionFinal(self):
        capa = tk.Frame(self.juego, bg="white")
        capa.place(relx=0, rely=0, relwidth=1, relheight=1)

        mensaje = tk.Label(
            capa,
            text=f"¡Felicidades por ganar!🎉\nMis Estadísticas\nNombre de usuario: Marcelo López\nPuntaje obtenido: {self.ptsTotal}\n",
            font=FUENTE_ETIQUETAB,
            fg=COLOR_TEXTO,
            bg="white",
            justify="center",
        )
        mensaje.pack(expand=True)

        # Botón para cerrar el juego
        cerrar_btn = tk.Button(
            capa,
            text="Cerrar juego",
            font=("Courier", 14),
            bg=COLOR_ROJO,
            fg="white",
            command=self.juego.destroy,
        )
        cerrar_btn.pack(pady=20)

        cerrar_btn.bind("<Enter>", self.onEnterCerrar)
        cerrar_btn.bind("<Leave>", self.onLeaveCerrar)

    # Función para cuando se de clic al botón de "actualizar" (Línea 476), genere una nueva letra de las elegidas para cada botón
    def mezclarLetras(self):
        letras_nuevas = self.letras_botones[:]
        shuffle(letras_nuevas)
        self.boton1.config(
            text=letras_nuevas[0], command=lambda: self.actualizarLetra(letras_nuevas[0])
        )
        self.boton2.config(
            text=letras_nuevas[1], command=lambda: self.actualizarLetra(letras_nuevas[1])
        )
        self.boton3.config(
            text=letras_nuevas[2], command=lambda: self.actualizarLetra(letras_nuevas[2])
        )
        self.boton5.config(
            text=letras_nuevas[3], command=lambda: self.actualizarLetra(letras_nuevas[3])
        )
        self.boton6.config(
            text=letras_nuevas[4], command=lambda: self.actualizarLetra(letras_nuevas[4])
        )
        self.boton7.config(
            text=letras_nuevas[5], command=lambda: self.actualizarLetra(letras_nuevas[5])
        )


    def actualizar_timer(self):
        if self.timer_state.activo:
            tiempo_transcurrido = time.time() - self.timer_state.tiempo_inicio
            minutos = int(tiempo_transcurrido // 60)
            segundos = int(tiempo_transcurrido % 60)
            if "label_tiempo" in self.widgets and not self.tiempo_oculto:
                self.widgets["label_tiempo"].config(
                    text=f"{minutos:02d}:{segundos:02d}"
                )
            self.timer_state.id = self.juego.after(1000, self.actualizar_timer)

    def pausar_timer(self):
        if self.timer_state.activo:
            self.timer_state.activo = False
            self.timer_state.tiempo_pausado = time.time() - self.timer_state.tiempo_inicio
            if self.timer_state.id:
                self.juego.after_cancel(self.timer_state.id)

    def reanudar_timer(self):
        if not self.timer_state.activo:
            self.timer_state.tiempo_inicio = time.time() - self.timer_state.tiempo_pausado
            self.timer_state.activo = True
            self.actualizar_timer()


    def ocultar_mostrar_tiempo(self):
        self.tiempo_oculto = not self.tiempo_oculto
        if self.tiempo_oculto:
            self.widgets["label_tiempo"].config(text="--:--")
            self.widgets["boton_ocultar"].config(
                text="Mostrar"
            )  # ← Cambia el texto del botón
        else:
            self.actualizar_timer()
            self.widgets["boton_ocultar"].config(
                text="Ocultar"
            )  # ← Vuelve a "Ocultar"

    # Pausa el juego...
    def pausarJuego(self):
        self.pausar_timer()
        pausa_capa = tk.Frame(self.juego, bg=COLOR_TEXTO)
        pausa_capa.place(relx=0, rely=0, relwidth=1, relheight=1)

        mensaje_pausa = tk.Label(
            pausa_capa,
            text="⏸ Juego en Pausa ⏸",
            font=FUENTE_ETIQUETAB,
            fg="white",
            bg=COLOR_TEXTO,
        )
        mensaje_pausa.pack(pady=50)

        # Botón para continuar el juego y el timer
        boton_continuar_pausa = tk.Button(
            pausa_capa,
            text="Continuar",
            font=FUENTE_ETIQUETA_2,
            bg=COLOR_BOTON,
            fg="white",
            command=lambda: [pausa_capa.destroy(), self.reanudar_timer()],
        )
        boton_continuar_pausa.pack(pady=20)

        boton_continuar_pausa.bind("<Enter>", self.onEnterContinuar)
        boton_continuar_pausa.bind("<Leave>", self.onLeaveContinuar)

        # Botón para salir de la aplicación
        boton_salir_pausa = tk.Button(
            pausa_capa,
            text="Salir del Juego",
            font=FUENTE_ETIQUETA,
            bg=COLOR_ROJO,
            fg="white",
            command=self.juego.destroy,
        )
        boton_salir_pausa.pack(pady=10)

        boton_salir_pausa.bind("<Enter>", self.onEnterCerrar)
        boton_salir_pausa.bind("<Leave>", self.onLeaveCerrar)

    def instrucciones(self):
        instruccionesCapa = tk.Frame(self.juego, bg=COLOR_TEXTO)
        instruccionesCapa.place(relx=0, rely=0, relwidth=1, relheight=1)

        mensajeInstrucciones = tk.Label(
            instruccionesCapa,
            text="Cómo se juega",
            font=FUENTE_ETIQUETAB,
            fg="white",
            bg=COLOR_TEXTO,
        )
        mensajeInstrucciones.pack(pady=40)

        mensajeInstrucciones = tk.Label(
            instruccionesCapa,
            text="Forma palabras de al menos 3 letras. Puedes repetir las letras, pero siempre incluyendo la letra central.\n No se admiten nombres propios, plurales y formas verbales conjugadas (solo infinitivos).\n Encuentra palabras que incluyan las 7 letras (¡Heptacrack!).\n Puntuación: las palabras de 3 letras dan 1 punto y las de 4 letras, 2 puntos. A partir de 5 letras, obtendrás tantos puntos como letras tenga la palabra. Los heptacracks valen 10 puntos.",
            font=FUENTE_ETIQUETA,
            fg="white",
            bg=COLOR_TEXTO,
            justify="center",
            wraplength=600,
        )
        mensajeInstrucciones.pack(pady=10)

        # Botón para continuar el juego
        boton_continuar_instrucciones = tk.Button(
            instruccionesCapa,
            text="Continuar",
            font=FUENTE_ETIQUETA_2,
            bg=COLOR_BOTON,
            fg="white",
            command=lambda: [instruccionesCapa.destroy()],
        )
        boton_continuar_instrucciones.pack(pady=25)

        boton_continuar_instrucciones.bind("<Enter>", self.onEnterContinuar)
        boton_continuar_instrucciones.bind("<Leave>", self.onLeaveContinuar)


# No se si se hace de esta manera xd
if __name__ == "__main__":
    juego = LexiReto()
    juego.juego.mainloop()
