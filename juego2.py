from random import shuffle, sample
import tkinter as tk
import time
import manejo_partida as mp

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
FUENTE_BOTON = ("Segoe UI", 15, "bold")

# Función generar palabras validas
def generar_letras():
    vocales = list("AEIOU")
    consonantes = list("BCDFGHJKLMNPQRSTV")

    # Seleccionamos sin repetir
    seleccion_vocales = sample(vocales, 3)
    seleccion_consonantes = sample(consonantes, 4)

    letras = seleccion_vocales + seleccion_consonantes
    shuffle(letras)  # Para mezclar el orden
    return letras


# Clase para todo el juego
class LexiReto:
    def __init__(self, user, root):
        self.user = user
        self.juego = tk.Toplevel(root)
        self.juego.attributes("-fullscreen", True)
        self.widgets = {}
        self.timer_pausado = False
        self.timer_id = None
        self.timer_oculto = False

        self.iniciar_juego()

        self.letra = tk.StringVar(self.juego)
        self.letra.set("")

        # Botón que ejecuta la función "pausarJuego"
        boton_pausa = tk.Button(
            self.juego,
            text="⏸ Pausa",
            font=FUENTE_BOTON,
            bg=COLOR_BOTON,
            command=self.pausarJuego,
        )
        boton_pausa.place(relx=1.0, y=0, anchor="ne", width=130, height=40)
        # Efectos visuales
        boton_pausa.bind("<Enter>", self.onEnterPausaIns)
        boton_pausa.bind("<Leave>", self.onLeavePausaIns)

        # Espacio en donde se mostrarán las letras que se vayan ingresando mediante los botones
        ingresoLetras = tk.Label(
            self.juego,
            text="",
            textvariable=self.letra,
            font=FUENTE_ETIQUETA_2,
            fg="white",
            bg=COLOR_TEXTO,
            relief="ridge",
            justify="center",
            wraplength=190,
            width=30,
            height=3,
        )
        ingresoLetras.place(x=50, y=60, width=650, height=50)

        # Elimino la letra central de mi lista de "letras_sin_repetir" para mandarsela a la lista "letras_botones", ya que esa lista no necesita la letraCentral
        self.boton1 = tk.Button(
            self.juego,
            text=self.partida["letras_botones"][0],
            font=FUENTE_BOTON,
            fg=COLOR_TEXTO,
            relief="ridge",
            command=lambda: self.actualizarLetra(self.partida["letras_botones"][0]),
        )
        self.boton1.place(x=250, y=120, width=100, height=80)

        self.boton1.bind("<Enter>", self.onEnterLetrasApli)
        self.boton1.bind("<Leave>", self.onLeaveLetrasApli)

        self.boton2 = tk.Button(
            self.juego,
            text=self.partida["letras_botones"][1],
            font=FUENTE_BOTON,
            fg=COLOR_TEXTO,
            relief="ridge",
            command=lambda: self.actualizarLetra(self.partida["letras_botones"][1]),
        )
        self.boton2.place(x=380, y=120, width=100, height=80)

        self.boton2.bind("<Enter>", self.onEnterLetrasApli)
        self.boton2.bind("<Leave>", self.onLeaveLetrasApli)

        self.boton3 = tk.Button(
            self.juego,
            text=self.partida["letras_botones"][2],
            font=FUENTE_BOTON,
            fg=COLOR_TEXTO,
            relief="ridge",
            command=lambda: self.actualizarLetra(self.partida["letras_botones"][2]),
        )
        self.boton3.place(x=180, y=215, width=100, height=80)

        self.boton3.bind("<Enter>", self.onEnterLetrasApli)
        self.boton3.bind("<Leave>", self.onLeaveLetrasApli)

        self.boton4 = tk.Button(
            self.juego,
            text=self.partida["letraCentral"].upper(),
            font=FUENTE_BOTON,
            fg="black",
            bg="#ffc733",
            relief="ridge",
            command=lambda: self.actualizarLetra(self.partida["letraCentral"].upper()),
        )
        self.boton4.place(x=315, y=215, width=100, height=80)

        self.boton4.bind("<Enter>", self.onEnterCentral)
        self.boton4.bind("<Leave>", self.onLeaveCentral)

        self.boton5 = tk.Button(
            self.juego,
            text=self.partida["letras_botones"][3],
            font=FUENTE_BOTON,
            fg=COLOR_TEXTO,
            relief="ridge",
            command=lambda: self.actualizarLetra(self.partida["letras_botones"][3]),
        )
        self.boton5.place(x=450, y=215, width=100, height=80)

        self.boton5.bind("<Enter>", self.onEnterLetrasApli)
        self.boton5.bind("<Leave>", self.onLeaveLetrasApli)

        self.boton6 = tk.Button(
            self.juego,
            text=self.partida["letras_botones"][4],
            font=FUENTE_BOTON,
            fg=COLOR_TEXTO,
            relief="ridge",
            command=lambda: self.actualizarLetra(self.partida["letras_botones"][4]),
        )
        self.boton6.place(x=250, y=310, width=100, height=80)

        self.boton6.bind("<Enter>", self.onEnterLetrasApli)
        self.boton6.bind("<Leave>", self.onLeaveLetrasApli)

        self.boton7 = tk.Button(
            self.juego,
            text=self.partida["letras_botones"][5],
            font=FUENTE_BOTON,
            fg=COLOR_TEXTO,
            relief="ridge",
            command=lambda: self.actualizarLetra(self.partida["letras_botones"][5]),
        )
        self.boton7.place(x=380, y=310, width=100, height=80)

        self.boton7.bind("<Enter>", self.onEnterLetrasApli)
        self.boton7.bind("<Leave>", self.onLeaveLetrasApli)

        # Botón que manda a la función "aplicarEntrada" la palabra ingresada
        self.aplicar = tk.Button(
            self.juego,
            text=("Aplicar"),
            font=FUENTE_BOTON,
            fg=COLOR_TEXTO,
            command=self.aplicarEntrada,
            relief="ridge",
        )
        self.aplicar.place(x=150, y=475, width=130, height=60)

        self.aplicar.bind("<Enter>", self.onEnterLetrasApli)
        self.aplicar.bind("<Leave>", self.onLeaveLetrasApli)

        # Botón para mezclar las letras generadas entre los botones
        self.actualizar = tk.Button(
            self.juego,
            text=("⟲"),
            font=("Courier", 15),
            fg=COLOR_TEXTO,
            command=self.mezclarLetras,
            relief="ridge",
        )
        self.actualizar.place(x=340, y=475, width=70, height=60)

        self.actualizar.bind("<Enter>", self.onEnterLetrasApli)
        self.actualizar.bind("<Leave>", self.onLeaveLetrasApli)

        # Botón para borrar la última letra ingresada
        self.borrar = tk.Button(
            self.juego,
            text=("Borrar"),
            font=FUENTE_BOTON,
            fg=COLOR_TEXTO,
            command=self.borrarUltimaLetra,
            relief="ridge",
        )
        self.borrar.place(x=460, y=475, width=130, height=60)

        self.borrar.bind("<Enter>", self.onEnterLetrasApli)
        self.borrar.bind("<Leave>", self.onLeaveLetrasApli)

        # Botón para ver las instrucciones del juego
        self.comoJugar = tk.Button(
            self.juego,
            text=("Cómo se juega"),
            font=FUENTE_BOTON,
            bg=COLOR_BOTON,
            fg=COLOR_TEXTO,
            command=self.instrucciones,
        )
        self.comoJugar.place(relx=0.5, y=0, anchor="n", width=160, height=40)

        self.comoJugar.bind("<Enter>", self.onEnterPausaIns)
        self.comoJugar.bind("<Leave>", self.onLeavePausaIns)

        #Botón para ocultar el timer
        self.boton_ocultar = tk.Button(
            self.juego,
            text="Ocultar",
            font=FUENTE_BOTON,
            bg=COLOR_BOTON,
            fg=COLOR_TEXTO,
            command=self.ocultar_mostrar_tiempo,
        )
        self.boton_ocultar.place(x=110, y=0, width=100, height=40)

        self.widgets["boton_ocultar"] = self.boton_ocultar

        self.boton_ocultar.bind("<Enter>", self.onEnterPausaIns)
        self.boton_ocultar.bind("<Leave>", self.onLeavePausaIns)

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
            wraplength=550,
            width=30,
            height=3,
        )
        self.mensaje1.place(x=50, y=560, width=650, height=50)

        # Imprime en un espacio la cantidad de palabras que lleva encontradas el usuario
        self.mensaje2 = tk.Label(
            self.juego,
            text=f"Palabras encontradas: {len(self.partida.get('palabrasElegidas0', []))}/{len(self.partida.get('seleccionadas', []))}",
            font=FUENTE_ETIQUETA_2,
            fg="white",
            bg=COLOR_TEXTO,
            relief="ridge",
            justify="center",
            wraplength=400,
            width=35,
            height=5,
        )
        self.mensaje2.place(x=50, y=400, width=650, height=50)

        #Imprime cuántas palabras se encontraron de acuerdo a la primera letra
        self.mensajePalabrasElegidas1 = tk.Label(
            self.juego,
            text=f"Palabras encontradas con {self.partida.get('listaAleatoriaCombinaciones')[0]}: {', '.join(self.partida.get('palabrasElegidas1'))}",
            font=FUENTE_ETIQUETA_2,
            fg="white",
            bg=COLOR_TEXTO,
            relief="ridge",
            justify="center",
            wraplength=950,
            width=35,
            height=5,
        )
        self.mensajePalabrasElegidas1.place(x=740, y=60, width=790, height=100)

        self.mensajePalabrasElegidas2 = tk.Label(
            self.juego,
            text=f"Palabras encontradas con {self.partida.get('listaAleatoriaCombinaciones')[1]}: {', '.join(self.partida.get('palabrasElegidas2'))}",
            font=FUENTE_ETIQUETA_2,
            fg="white",
            bg=COLOR_TEXTO,
            relief="ridge",
            justify="center",
            wraplength=950,
            width=35,
            height=5,
        )
        self.mensajePalabrasElegidas2.place(x=740, y=170, width=790, height=100)

        self.mensajePalabrasElegidas3 = tk.Label(
            self.juego,
            text=f"Palabras encontradas con {self.partida.get('listaAleatoriaCombinaciones')[2]}: {', '.join(self.partida.get('palabrasElegidas3'))}",
            font=FUENTE_ETIQUETA_2,
            fg="white",
            bg=COLOR_TEXTO,
            relief="ridge",
            justify="center",
            wraplength=950,
            width=35,
            height=5,
        )
        self.mensajePalabrasElegidas3.place(x=740, y=280, width=790, height=100)

        self.mensajePalabrasElegidas4 = tk.Label(
            self.juego,
            text=f"Palabras encontradas con {self.partida.get('listaAleatoriaCombinaciones')[3]}: {', '.join(self.partida.get('palabrasElegidas4'))}",
            font=FUENTE_ETIQUETA_2,
            fg="white",
            bg=COLOR_TEXTO,
            relief="ridge",
            justify="center",
            wraplength=950,
            width=35,
            height=5,
        )
        self.mensajePalabrasElegidas4.place(x=740, y=390, width=790, height=100)

        self.mensajePalabrasElegidas5 = tk.Label(
            self.juego,
            text=f"Palabras encontradas con {self.partida.get('listaAleatoriaCombinaciones')[4]}: {', '.join(self.partida.get('palabrasElegidas5'))}",
            font=FUENTE_ETIQUETA_2,
            fg="white",
            bg=COLOR_TEXTO,
            relief="ridge",
            justify="center",
            wraplength=950,
            width=35,
            height=5,
        )
        self.mensajePalabrasElegidas5.place(x=740, y=500, width=790, height=100)

        self.mensajePalabrasElegidas6 = tk.Label(
            self.juego,
            text=f"Palabras encontradas con {self.partida.get('listaAleatoriaCombinaciones')[5]}: {', '.join(self.partida.get('palabrasElegidas6'))}",
            font=FUENTE_ETIQUETA_2,
            fg="white",
            bg=COLOR_TEXTO,
            relief="ridge",
            justify="center",
            wraplength=950,
            width=35,
            height=5,
        )
        self.mensajePalabrasElegidas6.place(x=740, y=610, width=790, height=100)

        self.mensajePalabrasElegidas7 = tk.Label(
            self.juego,
            text=f"Palabras encontradas con {self.partida.get('listaAleatoriaCombinaciones')[6]}: {', '.join(self.partida.get('palabrasElegidas7'))}",
            font=FUENTE_ETIQUETA_2,
            fg="white",
            bg=COLOR_TEXTO,
            relief="ridge",
            justify="center",
            wraplength=950,
            width=35,
            height=5,
        )
        self.mensajePalabrasElegidas7.place(x=740, y=720, width=790, height=100)

        # Botón para simular que se encontraron todas las palabras y se ganó la partida (Crea una nueva partida)
        boton_test = tk.Button(
            self.juego,
            text="💊 Simular Victoria",
            font=FUENTE_BOTON,
            bg=COLOR_BOTON,
            fg=COLOR_TEXTO,
            command=self.simularVictoria
        )
        boton_test.place(x=1050, y=0, width=200, height=40)

        boton_test.bind("<Enter>", self.onEnterPausaIns)
        boton_test.bind("<Leave>", self.onLeavePausaIns)


    # Verifica si la palabra es mayor a 3 letras, si contiene la letra central y si contiene algunas de las otras letras
    def verificarPalabra(self, palabraIngresada):
        if len(palabraIngresada) < 3:
            return False
        if self.partida["letraCentral"] not in palabraIngresada:
            return False
        for letra in palabraIngresada:
            if letra not in self.partida["listaAleatoriaCombinaciones"]:
                return False
        return True

    # Calcula si la palabra es Heptacrack (Contiene 7 letras distintas)
    def esHeptacrack(self, palabraIngresada):
        letrasUnicas = self.partida["listaAleatoriaCombinaciones"][:]
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

    # Verifica si la palabra ingresada al clickear los botones, está en la lista de palabrasElegidas, y si cumple las condiciones necesarias
    # Además de Imprimir los pts obtenidos, totales, y verificar si se encontraron todas las palabras para terminar el juego
    def iniciarReto(self):
        pal = self.letra.get().upper()
        if not self.verificarPalabra(pal):
            self.mensaje1.config(
                text=f"La palabra no contiene la letra {self.partida['letraCentral']} o es demasiado corta."
            )
            return
        if pal not in self.partida["seleccionadas"]:
            self.mensaje1.config(text="Palabra inválida")
            return
        if pal in self.partida["palabrasElegidas0"]:
            self.mensaje1.config(text="Ya ingresaste esa palabra")
            return

        pts = self.calcularPuntaje(pal)
        self.partida["ptsTotal"] += pts
        self.partida["palabrasElegidas0"].append(pal)
        letra_inicial = pal[0]

        i = 0
        while letra_inicial != self.partida["listaAleatoriaCombinaciones"][i]:
            i += 1
        if self.partida.get(f"palabrasElegidas{i + 1}") is None:
            self.partida[f"palabrasElegidas{i + 1}"] = pal
        else:
            self.partida[f"palabrasElegidas{i + 1}"].append(pal)

        if self.esHeptacrack(pal):
            self.mensaje1.config(
                text=f"ES HEPTACRACK!\nHaz obtenido {pts} punto/s\nTienes {self.partida['ptsTotal']} punto/s en total"
            )
        else:
            self.mensaje1.config(
                text=f"Haz obtenido {pts} punto/s\nTienes {self.partida['ptsTotal']} punto/s en total"
            )

        self.mensaje2.config(
            text=f"Palabras encontradas: {len(self.partida['palabrasElegidas0'])}/{len(self.partida['seleccionadas'])}"
        )
        self.actualizar_tabla()

        if len(self.partida["palabrasElegidas0"]) == len(self.partida["seleccionadas"]):
            self.mostrarFelicitacionFinal()
        

        
    # Función para actualizar la impresión de palabras encontradas
    def actualizar_tabla(self):
        self.partida["listaAleatoriaCombinaciones"]
        listasPalabrasSinEspacios = [
            self.partida.get("palabrasElegidas1", []),
            self.partida.get("palabrasElegidas2", []),
            self.partida.get("palabrasElegidas3", []),
            self.partida.get("palabrasElegidas4", []),
            self.partida.get("palabrasElegidas5", []),
            self.partida.get("palabrasElegidas6", []),
            self.partida.get("palabrasElegidas7", []),
        ]

        mp.guardar_partida(self.user, self.partida, "juego2")

        for i in range(len(self.partida["listaAleatoriaCombinaciones"])):
            if i < len(listasPalabrasSinEspacios):
                texto = f"Palabras encontradas con {self.partida['listaAleatoriaCombinaciones'][i]}: {', '.join(listasPalabrasSinEspacios[i])}"
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

    # Cuando se de clic al botón de "Aplicar", verificará la palabra y lo volverá a su estado normal
    def aplicarEntrada(self):
        self.iniciarReto()
        self.letra.set("")

    # Al ir dando clic a los botones, imprime en un espacio llamado "iniciarReto" la letra que contiene cada botón y va generando la palabra
    def actualizarLetra(self, letra_boton):
        letra_actual = self.letra.get()
        self.letra.set(letra_actual + letra_boton)

    # En el espacio llamado "iniciarReto", simplemente elimina la última letra que se ingreso
    def borrarUltimaLetra(self):
        texto_actual = self.letra.get()
        if len(texto_actual) > 0:
            self.letra.set(texto_actual[:-1])

    # Funciones para cambiar el color de los botones cada que el cursor pase sobre ellos
    def onEnterLetrasApli(self, event):
        event.widget.config(bg=COLOR_BOTON_HOVER, fg="white")

    def onLeaveLetrasApli(self, event):
        event.widget.config(bg=COLOR_FONDO, fg="black")

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

    def onLeaveCentral(self, event):
        event.widget.config(bg="#ffc733", fg="black")

    # Al encontrar la cantidad de palabras generadas por el juego, muestra en la ventana un mensajede felicitaciones
    def mostrarFelicitacionFinal(self):
        capa = tk.Frame(self.juego, bg="white")
        capa.place(relx=0, rely=0, relwidth=1, relheight=1)

        mensaje = tk.Label(
            capa,
            text=f"¡Felicidades por ganar!🎉\nMis Estadísticas\nNombre de usuario: {self.user}\nPuntaje obtenido: {self.partida['ptsTotal']}\n",
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
            command=self.fin_juego,
        )
        cerrar_btn.pack(pady=20)

        cerrar_btn.bind("<Enter>", self.onEnterCerrar)
        cerrar_btn.bind("<Leave>", self.onLeaveCerrar)

    """def fin_juego(self):
        mp.eliminar_partida(self.user, "juego2")
        self.juego.destroy()"""

    def fin_juego(self):
        self.pausar_timer()
        mp.guardar_partida(self.user, self.partida, "juego2")
        mp.eliminar_partida(self.user, "juego2")
        self.juego.destroy()

    # Función para cuando se de clic al botón de "actualizar", genere una nueva letra de las elegidas para cada botón
    def mezclarLetras(self):
        letras_nuevas = self.partida["letras_botones"][:]
        shuffle(letras_nuevas)
        self.boton1.config(
            text=letras_nuevas[0],
            command=lambda: self.actualizarLetra(letras_nuevas[0]),
        )
        self.boton2.config(
            text=letras_nuevas[1],
            command=lambda: self.actualizarLetra(letras_nuevas[1]),
        )
        self.boton3.config(
            text=letras_nuevas[2],
            command=lambda: self.actualizarLetra(letras_nuevas[2]),
        )
        self.boton5.config(
            text=letras_nuevas[3],
            command=lambda: self.actualizarLetra(letras_nuevas[3]),
        )
        self.boton6.config(
            text=letras_nuevas[4],
            command=lambda: self.actualizarLetra(letras_nuevas[4]),
        )
        self.boton7.config(
            text=letras_nuevas[5],
            command=lambda: self.actualizarLetra(letras_nuevas[5]),
        )

    # Función principal para el timer
    def actualizar_timer(self):
        if not self.timer_pausado:
            if self.partida.get("tiempo_transcurrido") is None:
                self.partida["tiempo_transcurrido"] = 1
            else:
                self.partida["tiempo_transcurrido"] += 1

            minutos = self.partida["tiempo_transcurrido"] // 60
            segundos = self.partida["tiempo_transcurrido"] % 60
            if not self.timer_oculto:
                self.tiempo_label.config(text=f"{minutos:02}:{segundos:02}")
            self.timer_id = self.juego.after(1000, self.actualizar_timer)

    # Ocultar tiempo del timer
    def mostrar_timer_texto(self):
        if not self.timer_pausado:
            if self.partida.get("tiempo_transcurrido") is None:
                self.partida["tiempo_transcurrido"] = 1
            else:
                self.partida["tiempo_transcurrido"] += 1

            minutos = self.partida["tiempo_transcurrido"] // 60
            segundos = self.partida["tiempo_transcurrido"] % 60
            if not self.timer_oculto:
                self.tiempo_label.config(text=f"{minutos:02}:{segundos:02}")

        
    def pausar_timer(self):  # Función pausa
        self.timer_pausado = True
        if self.timer_id:
            self.juego.after_cancel(self.timer_id)
            self.timer_id = None

    def reanudar_timer(self):   # Función reanudar
        if self.timer_pausado:
            self.timer_pausado = False
            self.actualizar_timer()

    def ocultar_mostrar_tiempo(self):
        if not self.timer_oculto:
            self.tiempo_label.config(text="--:--")
            self.widgets["boton_ocultar"].config(
                text="Mostrar"
            )
            self.timer_oculto = True
        else:
            self.timer_oculto = False
            self.mostrar_timer_texto()
            self.widgets["boton_ocultar"].config(text="Ocultar")

    def pausarJuego(self): 
        self.pausar_timer()
        self.pausa_capa = tk.Frame(self.juego, bg=COLOR_TEXTO)
        self.pausa_capa.place(relx=0, rely=0, relwidth=1, relheight=1) # Label de pausa
        # self.overlay_pausa.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.mensaje_pausa = tk.Label(
            self.pausa_capa,
            text="⏸ Juego en Pausa ⏸",
            font=FUENTE_ETIQUETAB,
            fg="white",
            bg=COLOR_TEXTO,
        )
        # mensaje_pausa.pack(pady=50)
        self.mensaje_pausa.pack(fill=tk.BOTH, expand=True, side=tk.TOP, pady=20)

        # Botón para continuar el juego y el timer
        boton_continuar_pausa = tk.Button(
            self.pausa_capa,
            text="Continuar",
            font=FUENTE_ETIQUETA_2,
            bg=COLOR_BOTON,
            fg="white",
            command=lambda: [self.pausa_capa.destroy(), self.reanudar_timer()],
        )
        boton_continuar_pausa.pack(pady=20)

        boton_continuar_pausa.bind("<Enter>", self.onEnterContinuar)
        boton_continuar_pausa.bind("<Leave>", self.onLeaveContinuar)

        # Botón para salir de la aplicación
        boton_salir_pausa = tk.Button(
            self.pausa_capa,
            text="Salir del Juego",
            font=FUENTE_ETIQUETA,
            bg=COLOR_ROJO,
            fg="white",
            command=self.salir,
        )
        boton_salir_pausa.pack(pady=10)

        boton_salir_pausa.bind("<Enter>", self.onEnterCerrar)
        boton_salir_pausa.bind("<Leave>", self.onLeaveCerrar)

    def salir(self):    # Función guardar y salir del juego
        self.pausar_timer()
        mp.guardar_partida(self.user, self.partida, "juego2")
        self.juego.destroy()

    def instrucciones(self):    # Función instrucciones
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

    def iniciar_juego(self):
        self.partida = mp.cargar_partida(self.user, "juego2")
        self.tiempo_label = tk.Label(
            self.juego,
            font=FUENTE_ETIQUETAB,
            bg=COLOR_TEXTO,
            fg="white",
            width=5,
            anchor="center",
        )
        self.tiempo_label.place(relx=0, rely=0, width=100, height=40)
        
        if self.partida is None:
            # Cosas del DICT
            self.tiempo_oculto = False
            self.partida = {}
            while len(self.partida.get("seleccionadas", [])) < 3:
                self.partida["listaAleatoriaCombinaciones"] = generar_letras()
                self.letras_sin_repetir = self.partida["listaAleatoriaCombinaciones"][:]
                self.partida["letraCentral"] = self.partida.get(
                    "listaAleatoriaCombinaciones"
                )[0]
                self.partida["seleccionadas"] = []  # Palabras válidas
                with open("palabras_potente.txt", "r", encoding="utf-8") as archivo:
                    for linea in archivo:
                        palabra = linea.strip().upper()
                        es_valida = self.verificarPalabra(palabra)
                        if es_valida:
                            self.partida["seleccionadas"].append(palabra)
            print(self.partida.get("seleccionadas"))

            # Contador para los puntos totales
            self.partida["ptsTotal"] = 0
            # Listas para almacenar las palabras que se vayan ingresando en el juego
            self.partida["palabrasElegidas0"] = []
            self.partida["palabrasElegidas1"] = []
            self.partida["palabrasElegidas2"] = []
            self.partida["palabrasElegidas3"] = []
            self.partida["palabrasElegidas4"] = []
            self.partida["palabrasElegidas5"] = []
            self.partida["palabrasElegidas6"] = []
            self.partida["palabrasElegidas7"] = []

            self.partida["letras_botones"] = []
            for letra in self.letras_sin_repetir:
                if letra != self.partida["letraCentral"]:
                    self.partida["letras_botones"].append(letra)

            # Quito la letra central de la lista de sin repetidos
            if self.partida["letraCentral"] in self.letras_sin_repetir:
                self.letras_sin_repetir.remove(self.partida["letraCentral"])

            self.partida["tiempo_transcurrido"] = 0

            mp.guardar_partida(self.user, self.partida, "juego2")

        self.actualizar_timer()

    def simularVictoria(self):  # Botón para simular victoria
        self.partida["palabrasElegidas0"] = self.partida["seleccionadas"][:]
        # Vacía las listas específicas por letra
        for i in range(1, 8):
            self.partida[f"palabrasElegidas{i}"] = []

        for palabra in self.partida["seleccionadas"]:
            letra = palabra[0]
            for i, letra_ref in enumerate(self.partida["listaAleatoriaCombinaciones"]):
                if letra == letra_ref:
                    self.partida[f"palabrasElegidas{i+1}"].append(palabra)
                    break
        self.partida["ptsTotal"] = self.puntaje_maximo()
        self.actualizar_tabla()
        self.mensaje2.config(text=f"Palabras encontradas: {len(self.partida.get('palabrasElegidas0', []))}/{len(self.partida.get('seleccionadas', []))}",)
        self.juego.after(1500, self.mostrarFelicitacionFinal)

    def puntaje_maximo(self):   # Calcul del máximo puntaje por partida
        for i in range(len(self.partida["palabrasElegidas0"])):
            pts = self.calcularPuntaje(self.partida["palabrasElegidas0"][i])
            self.partida["ptsTotal"] += pts
        return self.partida["ptsTotal"]
            
if __name__ == "__main__":  # probar el juego sin el main.py
    prueba = tk.Tk()
    prueba.withdraw()  # Oculta ventana principal
    juego = LexiReto("prueba", prueba)
    prueba.mainloop()
