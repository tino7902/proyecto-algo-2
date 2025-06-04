import tkinter as tk
from tkinter import messagebox
import random
import generar as gen
import threading
import manejo_partida as mp

COLOR_FONDO = "#f0f4f8"
COLOR_BOTON = "#6fbf73"
COLOR_SECUNDARIO = "#4a90e2"
COLOR_TEXTO = "#333333"
FUENTE_TITULO = ("Segoe UI", 32, "bold")
FUENTE_ETIQUETA = ("Segoe UI", 16)
FUENTE_BOTON = ("Segoe UI", 12, "bold")


class JuegoLetras:
    # Clase para usarla luego con el times

    def __init__(self, user):
        self.user = user
        self.juego = tk.Toplevel()
        self.juego.title("L E T R A S  !!!")
        self.juego.attributes("-fullscreen", True)
        self.juego.configure(bg=COLOR_FONDO)  # Fondo azul marino
        self.timer_pausado = False
        self.timer_id = None
        self.timer_oculto = False
        self.pista = 0

        # Variables del juego
        # self.partida = {}
        # self.partida["puntaje"] = 0
        # self.partida["tiempo_transcurrido"] = 0
        # self.partida["palabras_encontradas"] = []
        self.letras_seleccionadas = []

        # Crear interfaz
        self.crear_interfaz()

    def generar_tablero_dinamico(self):
        self.partida = mp.cargar_partida(self.user, "juego1")
        if self.partida is None:
            self.partida = gen.leer_y_borrar_matriz()
        # Lanzar la generación de la próxima sopa en segundo plano
        threading.Thread(
            target=self.generar_y_guardar_en_segundo_plano, daemon=True
        ).start()
        print(self.partida.get("palabras_colocadas"))
        mp.guardar_partida(self.user, self.partida, "juego1")

    def generar_y_guardar_en_segundo_plano(self):
        try:
            matriz, palabras = gen.generar_sopa_inteligente()
            gen.guardar_matriz_en_archivo(matriz, palabras, "matrices_validas.txt")
            print("✅ Matriz regenerada en segundo plano")
        except Exception as e:
            print("⚠️ Error generando matriz en segundo plano:", e)

    def crear_interfaz(self):
        # Frame principal
        self.frame_principal = tk.Frame(self.juego, padx=20, pady=20, bg=COLOR_FONDO)
        self.frame_principal.pack(expand=True, fill=tk.BOTH)

        # Frame para el tablero y controles
        self.frame_juego = tk.Frame(self.frame_principal, bg=COLOR_FONDO)
        self.frame_juego.pack(expand=True, fill=tk.BOTH)

        # Frame de controles
        self.frame_controles = tk.Frame(self.frame_juego, bg=COLOR_FONDO)
        self.frame_controles.pack(side=tk.RIGHT, padx=20, pady=10, fill=tk.Y)

        # Frame puntaje
        self.label_puntaje = tk.Label(
            self.frame_controles,
            text="🏅 Puntaje: 0",
            font=FUENTE_BOTON,
            bg=COLOR_FONDO,
        )
        self.label_puntaje.pack(fill=tk.X, pady=5)

        # Título
        tk.Label(
            self.frame_juego,
            text="JUEGO DE LETRAS",
            font=FUENTE_TITULO,
            bg=COLOR_FONDO,
            fg=COLOR_BOTON,
        ).pack(pady=10)

        # Frame para el cronometro
        self.label_cronometro = tk.Label(
            self.frame_controles,
            text="⏱️ Tiempo: 00:00",
            font=FUENTE_BOTON,
            bg=COLOR_FONDO,
        )
        self.label_cronometro.pack(fill=tk.X, pady=5)
        # no anda
        # self.label_cronometro.bind("<Button-1>", self.toggle_cronometro_texto)

        self.boton_pausa = tk.Button(
            self.frame_controles,
            text="⏸ Pausa",
            font=FUENTE_BOTON,
            bg=COLOR_SECUNDARIO,
            command=self.toggle_cronometro,
        )
        self.boton_pausa.pack(fill=tk.X, pady=5)

        # Tablero de letras (5x5 como ejemplo)
        self.frame_tablero = tk.Frame(self.frame_juego, bg=COLOR_FONDO)
        self.frame_tablero.pack(side=tk.LEFT, padx=20, pady=10)

        # Frame oculto para pausa
        self.overlay_pausa = tk.Frame(self.juego, bg=COLOR_TEXTO)
        self.overlay_pausa.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.overlay_pausa.place_forget()  # Oculto por defecto

        self.label_pausa = tk.Label(
            self.overlay_pausa,
            text="⏸ Juego en Pausa ⏸",
            font=FUENTE_BOTON,
            fg="white",
            bg=COLOR_TEXTO,
        )
        self.label_pausa.pack(fill=tk.BOTH, expand=True, side=tk.TOP, pady=20)

        self.boton_reanudar_overlay = tk.Button(
            self.overlay_pausa,
            text="Continuar",
            font=FUENTE_BOTON,
            bg=COLOR_BOTON,
            fg="white",
            command=self.reanudar_desde_overlay,
        )
        self.boton_reanudar_overlay.pack(pady=10)

        self.boton_salir_menu = tk.Button(
            self.overlay_pausa,
            text="Salir del Juego",
            font=FUENTE_BOTON,
            bg="#cc4444",
            fg="white",
            command=self.juego.destroy,
        )
        self.boton_salir_menu.pack(pady=10)

        # Matriz de letras
        self.botones_letras = []
        self.generar_tablero_dinamico()

        for i in range(len(self.partida["tablero"])):
            fila_botones = []
            for j in range(len(self.partida["tablero"][i])):
                btn = tk.Button(
                    self.frame_tablero,
                    text=self.partida["tablero"][i][j],
                    font=FUENTE_ETIQUETA,
                    width=4,
                    height=2,
                    relief=tk.RAISED,
                    bg=COLOR_BOTON,
                    command=lambda i=i, j=j: self.seleccionar_letra(i, j),
                )
                btn.grid(row=i, column=j, padx=2, pady=2)
                fila_botones.append(btn)
            self.botones_letras.append(fila_botones)

        # Palabra actual
        self.label_palabra = tk.Label(
            self.frame_controles,
            text="",
            font=FUENTE_ETIQUETA,
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO,
        )
        self.label_palabra.pack(pady=10)

        # Botones de acción
        tk.Button(
            self.frame_controles,
            text="Borrar",
            font=FUENTE_BOTON,
            bg=COLOR_BOTON,
            command=self.borrar_seleccion,
        ).pack(fill=tk.X, pady=5)

        tk.Button(
            self.frame_controles,
            text="Aplicar",
            font=FUENTE_BOTON,
            bg=COLOR_BOTON,
            command=self.validar_palabra,
        ).pack(fill=tk.X, pady=5)

        tk.Button(
            self.frame_controles,
            text="Reiniciar",
            font=FUENTE_BOTON,
            bg=COLOR_BOTON,
            command=self.reiniciar_juego,
        ).pack(fill=tk.X, pady=5)

        tk.Button(
            self.frame_controles,
            text="Pista",
            font=FUENTE_BOTON,
            bg=COLOR_SECUNDARIO,
            command=self.mostrar_pista,
        ).pack(fill=tk.X, pady=5)

        # Palabras encontradas
        self.frame_palabras = tk.Frame(self.frame_controles, bg=COLOR_FONDO)
        self.frame_palabras.pack(pady=10)

        tk.Label(
            self.frame_palabras,
            text="Palabras encontradas:",
            font=FUENTE_ETIQUETA,
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO,
        ).pack()
        self.lista_palabras = tk.Listbox(
            self.frame_palabras, width=20, height=10, bg=COLOR_BOTON
        )
        if self.partida.get("palabras_encontradas") is not None:
            for palabra in self.partida.get("palabras_encontradas"):
                self.lista_palabras.insert(tk.END, palabra)
        self.lista_palabras.pack()

        # Estadísticas
        self.frame_stats = tk.Frame(self.frame_controles, bg=COLOR_FONDO)
        self.frame_stats.pack(pady=10)

        tk.Label(
            self.frame_stats,
            text="Estadísticas:",
            font=FUENTE_BOTON,
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO,
        ).pack()
        self.label_stats = tk.Label(
            self.frame_stats,
            text="Encontrados: 0\nCompletados: 0%",
            justify=tk.LEFT,
            font=FUENTE_BOTON,
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO,
        )

        if self.partida.get("palabras_encontradas") is not None:
            self.actualizar_estadisticas()
        self.label_stats.pack()

        tk.Button(
            self.frame_controles,
            text=("Cómo se juega"),
            font=FUENTE_BOTON,
            bg=COLOR_SECUNDARIO,
            fg=COLOR_TEXTO,
            command=self.Instrucciones,
        ).pack(fill=tk.X, pady=5)

        self.actualizar_cronometro()

    def seleccionar_letra(self, fila, columna):
        # Si ya fue seleccionada, no hacer nada
        if (fila, columna) in self.letras_seleccionadas:
            return

        # Si es la primera letra, permitir libremente
        if not self.letras_seleccionadas:
            valido = True
        else:
            ult_fila, ult_col = self.letras_seleccionadas[-1]
            delta_fila = abs(fila - ult_fila)
            delta_col = abs(columna - ult_col)
            valido = (delta_fila == 1 and delta_col == 0) or (
                delta_fila == 0 and delta_col == 1
            )

        if valido:
            boton = self.botones_letras[fila][columna]
            boton.config(relief=tk.SUNKEN, bg="lightgreen", state=tk.DISABLED)
            self.letras_seleccionadas.append((fila, columna))
            self.label_palabra.config(text=self.obtener_palabra_actual())

    def obtener_palabra_actual(self):
        return "".join(
            [
                self.partida["tablero"][fila][col]
                for fila, col in self.letras_seleccionadas
            ]
        )

    def borrar_seleccion(self):
        for fila, col in self.letras_seleccionadas:
            boton = self.botones_letras[fila][col]
            boton.config(relief=tk.RAISED, bg=COLOR_BOTON, state=tk.NORMAL)
        self.letras_seleccionadas = []
        self.label_palabra.config(text="")

    def validar_palabra(self):
        palabra = self.obtener_palabra_actual()

        if not palabra:
            messagebox.showwarning("Atención", "No has seleccionado ninguna letra.")
            return

        if palabra in self.partida.get(
            "palabras_colocadas"
        ) and palabra not in self.partida.get(
            "palabras_encontradas", []
        ):  # Agregar palabra encontrada
            if self.partida.get("palabras_encontradas") is None:
                self.partida["palabras_encontradas"] = palabra
            else:
                self.partida["palabras_encontradas"].append(palabra)

            self.lista_palabras.insert(tk.END, palabra)
            messagebox.showinfo("¡Correcto!", f"¡Encontraste la palabra {palabra}!")
            # -------------------------------------------------------------------------------------- Calcular puntos
            segundos = self.partida.get("tiempo_transcurrido", 1)
            puntos_palabra = len(palabra) ** 5 // segundos
            if self.pista:
                if self.partida.get("puntaje") is None:
                    self.partida["puntaje"] = puntos_palabra // 3
                else:
                    self.partida["puntaje"] += puntos_palabra // 3
                self.pista = 0
            else:
                if self.partida.get("puntaje") is None:
                    self.partida["puntaje"] = puntos_palabra
                else:
                    self.partida["puntaje"] += puntos_palabra
            self.label_puntaje.config(
                text=f"🏅 Puntaje: {self.partida.get('puntaje', 0)}"
            )
            mp.guardar_partida(self.user, self.partida, "juego1")
            # Verificar fin del juego
            if len(self.partida.get("palabras_encontradas", [])) == 7:
                self.finalizar_juego()
            self.borrar_seleccion()
        else:
            # Cambiar a rojo las letras seleccionadas
            for fila, col in self.letras_seleccionadas:
                self.botones_letras[fila][col].config(bg="firebrick1")

            # Volver al color original después de 1,5 seg
            self.juego.after(1500, self.borrar_seleccion)
            messagebox.showwarning(
                "Incorrecto", "La palabra no es válida o ya fue encontrada."
            )

        self.actualizar_estadisticas()

    def reiniciar_juego(self):
        mp.eliminar_partida(self.user, "juego1")
        self.generar_tablero_dinamico()

        for i in range(len(self.partida["tablero"])):
            for j in range(len(self.partida["tablero"][i])):
                letra = self.partida["tablero"][i][j]
                btn = self.botones_letras[i][j]
                btn.config(
                    text=letra, relief=tk.RAISED, bg=COLOR_BOTON, state=tk.NORMAL
                )

        self.borrar_seleccion()
        self.partida["palabras_encontradas"] = []
        self.lista_palabras.delete(0, tk.END)
        self.actualizar_estadisticas()
        self.reiniciar_cronometro()
        self.partida["puntaje"] = 0
        self.label_puntaje.config(text="🏅 Puntaje: 0")

    def actualizar_estadisticas(self):
        total_palabras = len(self.partida.get("palabras_colocadas"))
        encontradas = len(self.partida["palabras_encontradas"])
        porcentaje = (encontradas / total_palabras) * 100 if total_palabras > 0 else 0
        self.label_stats.config(
            text=f"Encontrados: {encontradas}\nCompletados: {porcentaje:.2f}%"
        )

    def buscar_palabra_en_matriz(self, palabra):
        FILAS = len(self.partida["tablero"])
        COLUMNAS = len(self.partida["tablero"][0])
        DIRECCIONES = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        def dfs(f, c, indice, visitado):
            if not (0 <= f < FILAS and 0 <= c < COLUMNAS):
                return None
            if (f, c) in visitado:
                return None
            if self.partida["tablero"][f][c] != palabra[indice]:
                return None

            visitado.add((f, c))

            if indice == len(palabra) - 1:
                return [(f, c)]

            for df, dc in DIRECCIONES:
                nf, nc = f + df, c + dc
                subcamino = dfs(nf, nc, indice + 1, visitado.copy())
                if subcamino:
                    return [(f, c)] + subcamino

            return None

        for i in range(FILAS):
            for j in range(COLUMNAS):
                if self.partida["tablero"][i][j] == palabra[0]:
                    camino = dfs(i, j, 0, set())
                    if camino:
                        return camino
        return None

    def mostrar_pista(self):
        self.pista = 1
        posibles = [
            p
            for p in self.partida.get("palabras_colocadas")
            if p not in self.partida.get("palabras_encontradas", [])
        ]
        if not posibles:
            messagebox.showinfo("Pista", "¡Ya encontraste todas las palabras!")
            return

        palabra = random.choice(posibles)
        camino = self.buscar_palabra_en_matriz(palabra)

        if not camino:
            messagebox.showwarning(
                "Pista", f"No se pudo encontrar la palabra '{palabra}' en la matriz."
            )
            return

        for f, c in camino:
            self.botones_letras[f][c].config(bg="gold")

        # Restaurar colores después de 2 segundos
        self.juego.after(2000, lambda: self.restaurar_colores(camino))

    def restaurar_colores(self, camino):
        for f, c in camino:
            # estado = self.botones_letras[f][c]["state"]
            color = "lightgreen" if (f, c) in self.letras_seleccionadas else COLOR_BOTON
            self.botones_letras[f][c].config(bg=color)

    def actualizar_cronometro(self):
        if not self.timer_pausado:
            if self.partida.get("tiempo_transcurrido") is None:
                self.partida["tiempo_transcurrido"] = 1
            else:
                self.partida["tiempo_transcurrido"] += 1

            minutos = self.partida["tiempo_transcurrido"] // 60
            segundos = self.partida["tiempo_transcurrido"] % 60
            if not self.timer_oculto:
                self.label_cronometro.config(
                    text=f"⏱️ Tiempo: {minutos:02}:{segundos:02}"
                )
            self.timer_id = self.juego.after(1000, self.actualizar_cronometro)

    """
    def actualizar_timer():  # Usar este contador más adelante cuando se arregle el bug
        if self.timer_state.activo:
            tiempo_transcurrido = time.time() - self.timer_state.tiempo_inicio
            minutos = int(tiempo_transcurrido // 60)
            segundos = int(tiempo_transcurrido % 60)
            if 'label_tiempo' in self.widgets and not self.tiempo_oculto:
                self.widgets['label_tiempo'].config(text=f"{minutos:02d}:{segundos:02d}")
            self.timer_state.id = self.app.after(1000, actualizar_timer)
    """

    def pausar_cronometro(self):
        self.timer_pausado = True
        if self.timer_id:
            self.juego.after_cancel(self.timer_id)
            self.timer_id = None

    def reanudar_cronometro(self):
        if self.timer_pausado:
            self.timer_pausado = False
            self.actualizar_cronometro()

    def reiniciar_cronometro(self):
        self.pausar_cronometro()
        self.partida["tiempo_transcurrido"] = 0
        self.label_cronometro.config(text="⏱️ Tiempo: 00:00")
        self.reanudar_cronometro()

    def toggle_cronometro(self):
        if self.timer_pausado:
            self.boton_pausa.config(text="Pausar")
            self.reanudar_cronometro()
            self.overlay_pausa.place_forget()
        else:
            self.boton_pausa.config(text="Reanudar")
            self.pausar_cronometro()
            self.overlay_pausa.lift()
            self.overlay_pausa.place(relx=0, rely=0, relwidth=1, relheight=1)

    def toggle_cronometro_texto(self):
        if not self.timer_oculto:
            self.timer_oculto = True
            self.label_cronometro.config(text="⏱️ Tiempo: --:--")
        else:
            self.timer_oculto = False
            self.actualizar_cronometro()

    """
    def ocultar_mostrar_tiempo():   # Usar este código cuando se arregle el bug
        self.tiempo_oculto = not self.tiempo_oculto
        if self.tiempo_oculto:
            self.widgets['label_tiempo'].config(text="--:--")
            self.widgets['boton_ocultar'].config(text="Mostrar")# ← Cambia el texto del botón
        else:
            actualizar_timer()
            self.widgets['boton_ocultar'].config(text="Ocultar")# ← Vuelve a "Ocultar"
    """

    def reanudar_desde_overlay(self):
        self.overlay_pausa.place_forget()
        self.toggle_cronometro()  # Esto cambia el estado a "reanudar"

    def Instrucciones(self):
        instruccionesCapa = tk.Frame(self.juego, bg=COLOR_TEXTO)
        instruccionesCapa.place(relx=0, rely=0, relwidth=1, relheight=1)

        mensajeInstrucciones = tk.Label(
            instruccionesCapa,
            text="Cómo se juega",
            font=FUENTE_ETIQUETA,
            fg="white",
            bg=COLOR_TEXTO,
        )
        mensajeInstrucciones.pack(pady=40)

        mensajeInstrucciones = tk.Label(
            instruccionesCapa,
            text="Encuentra las siete palabras que hemos ocultado seleccionando casillas contiguas en todas las direcciones, salvo en diagonal. Puedes utilizar cada letra tantas veces como quieras, pero no en una misma palabra.\n¡ATENCIÓN! NO TODAS LAS PALABRAS QUE PUEDAS FORMAR SERÁN VÁLIDAS. SÓLO LAS QUE PROPONEMOS.",
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
            font=FUENTE_ETIQUETA,
            bg=COLOR_BOTON,
            fg="white",
            command=lambda: [instruccionesCapa.destroy()],
        )
        boton_continuar_instrucciones.pack(pady=25)

    def finalizar_juego(self):
        self.pausar_cronometro()
        minutos = self.partida["tiempo_transcurrido"] // 60
        segundos = self.partida["tiempo_transcurrido"] % 60
        tiempo_str = f"{minutos:02}:{segundos:02}"

        messagebox.showinfo(
            "¡Felicidades!",
            f"Encontraste todas las palabras.\nTiempo: {tiempo_str}\nPuntaje: {self.partida['puntaje']}",
        )

        self.reiniciar_juego()


# def iniciarJuego1(user):
#     juego = JuegoLetras(user)
#     juego.juego.mainloop()

# ------------------ Ejemplo de uso ------------------
if __name__ == "__main__":
    juego = JuegoLetras(
        "prueba"
    )  # si o si tiene que tener algo en el parametro user para que pueda crear el archivo correspondiente
    juego.juego.mainloop()
