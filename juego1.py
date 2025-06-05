import tkinter as tk
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
FUENTE_BOTON = ("Segoe UI", 14, "bold")


class JuegoLetras:
    # Clase para usarla luego con el times

    def __init__(self, user, root):     # Iniciarlizar variables "globales" para el juego
        self.user = user
        self.juego = tk.Toplevel(root)
        self.juego.title("L E T R A S  !!!")
        self.juego.attributes("-fullscreen", True)
        self.juego.configure(bg=COLOR_FONDO)  # Fondo azul marino
        self.timer_pausado = False
        self.timer_id = None
        self.timer_oculto = False
        self.pista = 0
        self.letras_seleccionadas = []
        self.partida = {}

        # Crear interfaz
        self.crear_interfaz()

    def generar_tablero_dinamico(self): # Genera tablero dinámicamente si no existe uno en partida
        self.partida = mp.cargar_partida(self.user, "juego1")   # Busca si hay una matriz del usuario
        if self.partida is None:
            self.partida = gen.leer_y_borrar_matriz()
            self.partida["palabras_encontradas"] = []   # Acá se arregla el bug con las estadísticas
            self.partida["puntaje"] = 0
        # Lanzar la generación de la próxima sopa en segundo plano
        threading.Thread(
            target=self.generar_y_guardar_en_segundo_plano, daemon=True
        ).start()
        print(self.partida.get("palabras_colocadas"))
        mp.guardar_partida(self.user, self.partida, "juego1")

    def generar_y_guardar_en_segundo_plano(self):   # Crea matrices próximos en segunod plano para acelerar la carga de matrices
        try:
            matriz, palabras = gen.generar_sopa_inteligente()
            if gen.guardar_matriz_en_archivo(matriz, palabras, "matrices_validas.txt"):
                print("✅ Matriz regenerada en segundo plano")
            else:
                print("Máximo matrices en archivos")
        except Exception as e:
            print("⚠️ Error generando matriz en segundo plano:", e)

    def crear_interfaz(self):   # Función que crea toda la interfaz del juego
        # Frame principal
        self.frame_principal = tk.Frame(self.juego, padx=20, pady=20, bg=COLOR_FONDO)
        self.frame_principal.pack(expand=True, fill=tk.BOTH)

        # Frame para el tablero y controles
        self.frame_juego = tk.Frame(self.frame_principal, bg=COLOR_FONDO)
        self.frame_juego.pack(expand=True, fill=tk.BOTH)

        # Frame de controles
        self.frame_controles = tk.Frame(self.frame_juego, bg=COLOR_FONDO)
        self.frame_controles.pack(side=tk.RIGHT, padx=20, pady=10, fill=tk.Y)

        # Label del puntaje
        puntos = self.partida.get("puntaje", 0)
        self.label_puntaje = tk.Label(
            self.frame_controles,
            text=f"🏅 Puntaje: {puntos}",
            font=FUENTE_BOTON,
            bg=COLOR_FONDO,
            width=15,
        )
        self.label_puntaje.pack(fill=tk.X, pady=5)

        # Cronómetro
        self.label_cronometro = tk.Button(
            self.frame_controles,
            text="⏱️ Tiempo: 00:00",
            font=FUENTE_BOTON,
            bg=COLOR_FONDO,
            command=self.toggle_cronometro_texto,
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
            width=15,
        )
        self.label_cronometro.pack(fill=tk.X, pady=5)

        # Botón de pausa
        self.boton_pausa = tk.Button(
            self.frame_controles,
            text="⏸ Pausa",
            font=FUENTE_BOTON,
            bg=COLOR_SECUNDARIO,
            width=15,
            command=self.toggle_cronometro,
        )
        self.boton_pausa.pack(fill=tk.X, pady=5)

        # Botón "Cómo se juega"
        tk.Button(
            self.frame_controles,
            text="Cómo se juega",
            font=FUENTE_BOTON,
            bg=COLOR_SECUNDARIO,
            fg=COLOR_TEXTO,
            width=25,
            command=self.Instrucciones,
        ).pack(fill=tk.X, pady=5)

        # Título
        tk.Label(
            self.frame_juego,
            text="JUEGO DE LETRAS",
            font=FUENTE_TITULO,
            bg=COLOR_FONDO,
            fg=COLOR_BOTON,
        ).pack(pady=10)

        # Tablero de letras
        self.frame_tablero = tk.Frame(self.frame_juego, bg=COLOR_FONDO)
        self.frame_tablero.pack(side=tk.LEFT, padx=20, pady=10)

        # Frame oculto para pausa
        self.overlay_pausa = tk.Frame(self.juego, bg=COLOR_TEXTO)
        self.overlay_pausa.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.overlay_pausa.place_forget()  # Oculto por defecto

        # Label "Juego en pausa"
        self.label_pausa = tk.Label(
            self.overlay_pausa,
            text="⏸ Juego en Pausa ⏸",
            font=FUENTE_BOTON,
            fg="white",
            bg=COLOR_TEXTO,
        )
        self.label_pausa.pack(fill=tk.BOTH, expand=True, side=tk.TOP, pady=20)

        # Botón seguir jugando
        self.boton_reanudar_overlay = tk.Button(
            self.overlay_pausa,
            text="Continuar",
            font=FUENTE_BOTON,
            bg=COLOR_BOTON,
            fg="white",
            command=self.reanudar_desde_overlay,
        )
        self.boton_reanudar_overlay.pack(pady=10)

        # Botón salir del juego
        self.boton_salir_menu = tk.Button(
            self.overlay_pausa,
            text="Salir del Juego",
            font=FUENTE_BOTON,
            bg="#cc4444",
            fg="white",
            command=self.cerrar_juego,
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
                    width=5,
                    height=2,
                    relief=tk.RAISED,
                    bg=COLOR_BOTON,
                    command=lambda i=i, j=j: self.seleccionar_letra(i, j),
                )
                btn.grid(row=i, column=j, padx=2, pady=2)
                fila_botones.append(btn)
            self.botones_letras.append(fila_botones)

        # Frame central a la derecha de la matriz
        self.frame_centro_derecha = tk.Frame(self.frame_juego, bg=COLOR_FONDO)
        self.frame_centro_derecha.pack(
            side=tk.LEFT, fill=tk.BOTH, expand=False, padx=10
        )

        # Contenedor debajo de la matriz
        self.frame_inferior = tk.Frame(self.frame_tablero, bg=COLOR_FONDO)
        self.frame_inferior.grid(
            row=len(self.partida["tablero"]),
            column=0,
            columnspan=len(self.partida["tablero"][0]),
            pady=(10, 0),
        )

        # Label Palabra actual
        self.label_palabra = tk.Label(
            self.frame_inferior,
            text="",
            font=FUENTE_ETIQUETA,
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO,
            anchor="center",
        )
        self.label_palabra.pack(fill=tk.X, pady=(0, 10))

        # Botones de acción funciones
        self.frame_botones_accion = tk.Frame(self.frame_inferior, bg=COLOR_FONDO)
        self.frame_botones_accion.pack()

        botones = [
            ("Borrar", self.borrar_seleccion),
            ("Aplicar", self.validar_palabra),
            ("Reiniciar", self.reiniciar_juego),
            ("Pista", self.mostrar_pista),
        ]

        # Estilo de botones de acción
        for i, (texto, comando) in enumerate(botones):
            btn = tk.Button(
                self.frame_botones_accion,
                text=texto,
                font=FUENTE_BOTON,
                bg=COLOR_BOTON if texto != "Pista" else COLOR_SECUNDARIO,
                command=comando,
                width=20,
                height=2,
            )
            btn.grid(row=i // 2, column=i % 2, padx=10, pady=10, sticky="nsew")

        # Expandir celdas uniformemente
        for i in range(2):
            self.frame_botones_accion.columnconfigure(i, weight=1)

        self.frame_palabras = tk.Frame(self.frame_centro_derecha, bg=COLOR_FONDO)
        self.frame_palabras.pack(pady=10, fill=tk.BOTH, expand=True)

        # Listas palabras encontradas - por encontrar
        self.lista_palabras = tk.Listbox(
            self.frame_palabras,
            height=15,
            bg=COLOR_FONDO,
            font=FUENTE_ETIQUETA,
            justify="left",
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
            width=35,
        )
        self.lista_palabras.pack(fill=tk.BOTH, expand=True)

        # Estadísticas debajo de la lista
        self.frame_stats = tk.Frame(self.frame_palabras, bg=COLOR_FONDO)
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
        self.label_stats.pack()

        if self.partida.get("palabras_encontradas") is not None:
            self.actualizar_estadisticas()
        self.label_stats.pack()

        self.mostrar_resumen_palabras()
        self.actualizar_cronometro()

        # Label mensaje al usuario
        self.label_mensaje = tk.Label(
            self.frame_controles,
            text="",
            font=FUENTE_ETIQUETA,
            fg=COLOR_TEXTO,
            bg=COLOR_FONDO,
            wraplength=250,
            justify="left",
        )
        self.label_mensaje.pack(fill=tk.X, pady=(10, 5))

    def mostrar_mensaje(self, texto, tipo="info"):  # Función mensaje al usuario
        colores = {"info": COLOR_TEXTO, "exito": "green", "error": "red"}
        self.label_mensaje.config(text=texto, fg=colores.get(tipo, COLOR_TEXTO))

    def cerrar_juego(self): # Función guardar partida y cerrar juego
        mp.guardar_partida(self.user, self.partida, "juego1")
        self.juego.destroy()

    def seleccionar_letra(self, fila, columna): # Función elegir letra de la matriz
        # Si ya fue seleccionada, no hacer nada
        if (fila, columna) in self.letras_seleccionadas:
            return

        # Si es la primera letra, permitir libremente
        if not self.letras_seleccionadas:
            valido = True
        else:   # Si no es la primera letra solo permitir contiguos no diagonales
            ult_fila, ult_col = self.letras_seleccionadas[-1]
            delta_fila = abs(fila - ult_fila)
            delta_col = abs(columna - ult_col)
            valido = (delta_fila == 1 and delta_col == 0) or (
                delta_fila == 0 and delta_col == 1
            )

        # Si es valido la letra entonces marcar
        if valido:
            boton = self.botones_letras[fila][columna]
            boton.config(relief=tk.SUNKEN, bg="lightgreen", state=tk.DISABLED)
            self.letras_seleccionadas.append((fila, columna))
            self.label_palabra.config(text=self.obtener_palabra_actual())

    def obtener_palabra_actual(self):   # Función escribir letra seleccionada
        return "".join(
            [
                self.partida["tablero"][fila][col]
                for fila, col in self.letras_seleccionadas
            ]
        )

    def borrar_seleccion(self): # Función borrar palabra formada
        for fila, col in self.letras_seleccionadas:
            boton = self.botones_letras[fila][col]
            boton.config(relief=tk.RAISED, bg=COLOR_BOTON, state=tk.NORMAL)
        self.letras_seleccionadas = []
        self.label_palabra.config(text="")

    def validar_palabra(self):  # Función para validar palabra con "palabras_colocadas"
        palabra = self.obtener_palabra_actual()

        if not palabra:
            self.mostrar_mensaje("✅ Palabra correcta.", tipo="exito")
            return

        if palabra in self.partida.get("palabras_colocadas") and palabra not in self.partida.get("palabras_encontradas", []):  # Agregar palabra encontrada
            if self.partida.get("palabras_encontradas") is None:
                self.partida["palabras_encontradas"] = palabra
            else:
                self.partida["palabras_encontradas"].append(palabra)

            self.lista_palabras.insert(tk.END, palabra)
            self.mostrar_mensaje("✅ Palabra correcta.", tipo="exito")
            # Calculo de puntaje por palabra
            segundos = self.partida.get("tiempo_transcurrido", 1)
            puntos_palabra = len(palabra) ** 5 // segundos  # formula para puntaje = (longitud de la palabra ^ 5) / segundos

            if self.pista:  # Si usó pista
                self.partida["puntaje"] += puntos_palabra // 3  # Si uso pista 1/3 Total puntaje
                self.pista = 0
            else:   # Si no usó pista
                self.partida["puntaje"] += puntos_palabra

            # Actualiza el texto de puntaje
            self.label_puntaje.config(text=f"🏅 Puntaje: {self.partida.get('puntaje', 0)}")
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
            self.mostrar_mensaje("❌ Incorrecto, La palabra no es válida", tipo="error")

        self.actualizar_estadisticas()
        self.mostrar_resumen_palabras()

    def mostrar_resumen_palabras(self): # Actualizar tabla de palabras a encontrar - encontradas
        palabras = self.partida.get("palabras_colocadas", [])
        encontradas = set(self.partida.get("palabras_encontradas", []))
        resumen = {}

        for palabra in palabras:
            longitud = len(palabra)
            if longitud not in resumen:
                resumen[longitud] = []

            if palabra in encontradas:
                resumen[longitud].append(palabra.upper())
            else:
                resumen[longitud].append(palabra[0].upper())

        # Construir texto ordenado por longitud descendente
        resumen_texto = ""
        for longitud in sorted(resumen.keys(), reverse=True):
            letras_ypalabras = resumen[longitud]
            resumen_texto += f"{longitud} letras:\n"
            for entrada in sorted(letras_ypalabras):
                resumen_texto += f"{entrada}\n"
            resumen_texto += "\n"

        # Mostrar en la lista
        self.lista_palabras.delete(0, tk.END)
        for linea in resumen_texto.strip().split("\n"):
            self.lista_palabras.insert(tk.END, linea)

    def reiniciar_juego(self):  # Función reiniciar juego
        mp.eliminar_partida(self.user, "juego1")    # Elimina partida guardada anteriormente
        self.generar_tablero_dinamico() # Genera tablero de nuevo

        for i in range(len(self.partida["tablero"])):
            for j in range(len(self.partida["tablero"][i])):
                letra = self.partida["tablero"][i][j]
                btn = self.botones_letras[i][j]
                btn.config(
                    text=letra, relief=tk.RAISED, bg=COLOR_BOTON, state=tk.NORMAL
                )

        # Poner todas las estadísticas vacías
        self.borrar_seleccion()
        self.partida["palabras_encontradas"] = []
        self.lista_palabras.delete(0, tk.END)
        self.actualizar_estadisticas()
        self.reiniciar_cronometro()
        self.partida["puntaje"] = 0
        self.label_puntaje.config(text=f"🏅 Puntaje: 0")
        mp.guardar_partida(self.user, self.partida, "juego1")
        self.mostrar_resumen_palabras()

    def actualizar_estadisticas(self):  # Actualizar estadísticas por porcentaje y palabras encontradas
        total_palabras = len(self.partida.get("palabras_colocadas", []))
        encontradas = len(self.partida.get("palabras_encontradas", []))
        porcentaje = (encontradas / total_palabras) * 100 if total_palabras > 0 else 0
        self.label_stats.config(
            text=f"Encontrados: {encontradas}\nCompletados: {porcentaje:.2f}%"
        )
        self.label_puntaje.config(text=f"🏅 Puntaje: {self.partida.get('puntaje', 0)}")

    def buscar_palabra_en_matriz(self, palabra):    # Buscar camino de la "palabra"
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

            for df, dc in DIRECCIONES:  # bucle recorre las direcciones contiguas
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

    def mostrar_pista(self):    # Función para mostrar pista
        self.pista = 1  # Bandera pista habilitado
        posibles = [
            p
            for p in self.partida.get("palabras_colocadas")
            if p not in self.partida.get("palabras_encontradas", [])
        ]
        if not posibles:
            self.mostrar_mensaje("Pista", "¡Ya encontraste todas las palabras!", tipo="info")
            return

        palabra = random.choice(posibles)
        camino = self.buscar_palabra_en_matriz(palabra)

        if not camino:
            self.mostrar_mensaje(f"No se pudo encontrar la palabra '{palabra}' en la matriz.",tipo="error",) # Posible error
            return

        for f, c in camino: # Pinta el camino de amarillo
            self.botones_letras[f][c].config(bg="gold")

        # Restaurar colores después de 2 segundos
        self.juego.after(2000, lambda: self.restaurar_colores(camino))

    def restaurar_colores(self, camino):    # Función para restaurar colores de pista
        for f, c in camino:
            # estado = self.botones_letras[f][c]["state"]
            color = "lightgreen" if (f, c) in self.letras_seleccionadas else COLOR_BOTON
            self.botones_letras[f][c].config(bg=color)

    def actualizar_cronometro(self):    # Función cronometro
        if not self.timer_pausado:
            if self.partida.get("tiempo_transcurrido") is None:
                self.partida["tiempo_transcurrido"] = 1
            else:
                self.partida["tiempo_transcurrido"] += 1

            minutos = self.partida["tiempo_transcurrido"] // 60
            segundos = self.partida["tiempo_transcurrido"] % 60
            if not self.timer_oculto:
                self.label_cronometro.config(text=f"⏱️ Tiempo: {minutos:02}:{segundos:02}")
            self.timer_id = self.juego.after(1000, self.actualizar_cronometro)

    def pausar_cronometro(self):    # Función pausar cronómetro
        self.timer_pausado = True
        if self.timer_id:
            self.juego.after_cancel(self.timer_id)
            self.timer_id = None

    def reanudar_cronometro(self):  # Función despausar cronómetro
        if self.timer_pausado:
            self.timer_pausado = False
            self.actualizar_cronometro()

    def reiniciar_cronometro(self): # Función reinicar cronómetro
        self.pausar_cronometro()
        self.partida["tiempo_transcurrido"] = 0
        self.label_cronometro.config(text="⏱️ Tiempo: 00:00")
        self.reanudar_cronometro()

    def toggle_cronometro(self):    # Función cambio de texto al botón pausa
        if self.timer_pausado:
            self.boton_pausa.config(text="Pausar")
            self.reanudar_cronometro()
            self.overlay_pausa.place_forget()
        else:
            self.boton_pausa.config(text="Reanudar") # En desuso
            self.pausar_cronometro()
            self.overlay_pausa.lift()
            self.overlay_pausa.place(relx=0, rely=0, relwidth=1, relheight=1)

    def toggle_cronometro_texto(self):  # Función Ocultar tiempo en cronómetro
        if not self.timer_oculto:
            self.label_cronometro.config(text="⏱️ Tiempo: --:--")
            self.timer_oculto = True
        else:
            minutos = self.partida["tiempo_transcurrido"] // 60
            segundos = self.partida["tiempo_transcurrido"] % 60
            self.label_cronometro.config(text=f"⏱️ Tiempo: {minutos:02}:{segundos:02}")
            self.timer_oculto = False

    def reanudar_desde_overlay(self):
        self.overlay_pausa.place_forget()
        self.toggle_cronometro()  # Esto cambia el estado a "reanudar"

    def Instrucciones(self):    # Función instruccinoes cómo se juega
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

    def finalizar_juego(self):  # Función ganar y reinciar
        self.pausar_cronometro()
        minutos = self.partida["tiempo_transcurrido"] // 60
        segundos = self.partida["tiempo_transcurrido"] % 60
        tiempo_str = f"{minutos:02}:{segundos:02}"

        self.mostrar_mensaje(
            f"¡Felicidades! \nEncontraste todas las palabras.\nTiempo: {tiempo_str}\nPuntaje: {self.partida['puntaje']}",
            "exito",
        )
        self.reiniciar_juego()
        mp.guardar_partida(self.user, self.partida, "juego1")


# ------------------ Ejemplo de uso ------------------
if __name__ == "__main__":
    prueba = tk.Tk()
    prueba.withdraw()  # Oculta ventana principal
    juego = JuegoLetras(
        "", prueba
    )  # si o si tiene que tener algo en el parametro user para que pueda crear el archivo correspondiente
    juego.juego.mainloop()
