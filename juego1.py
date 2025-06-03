import tkinter as tk
from tkinter import messagebox, font
import random
from generar import *
import threading

class JuegoLetras:
    #Clase para usarla luego con el times

    def __init__(self, root):
        self.root = root
        self.root.title("Juego de Letras")
        self.root.geometry("800x600")
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg='navy')  # Fondo azul marino
        self.tiempo_transcurrido = 0
        self.timer_pausado = False
        self.timer_id = None
        self.timer_oculto = False
        self.puntaje = 0
        self.pista = 0

        
        # Configuración de estilos
        self.fuente_letras = font.Font(family='Helvetica', size=16, weight='bold')
        self.fuente_botones = font.Font(family='Helvetica', size=12)
        self.fuente_titulo = font.Font(family='Helvetica', size=20, weight='bold')
        
        # Variables del juego
        self.palabras_encontradas = []
        self.letras_seleccionadas = []
        
        # Crear interfaz
        self.crear_interfaz()
        
    def generar_tablero_dinamico(self):
        self.matriz_letras, self.palabras_validas = leer_y_borrar_matriz()
        # Lanzar la generación de la próxima sopa en segundo plano
        threading.Thread(target=self.generar_y_guardar_en_segundo_plano, daemon=True).start()
        print(self.palabras_validas)

    def generar_y_guardar_en_segundo_plano(self):
        try:
            matriz, palabras = generar_sopa_inteligente()
            guardar_matriz_en_archivo(matriz, palabras, "matrices_validas.txt")
            print("✅ Matriz regenerada en segundo plano")
        except Exception as e:
            print("⚠️ Error generando matriz en segundo plano:", e)
        
    
    def crear_interfaz(self):
        # Frame principal
        self.frame_principal = tk.Frame(self.root, padx=20, pady=20, bg='navy')
        self.frame_principal.pack(expand=True, fill=tk.BOTH)

        # Frame para el tablero y controles
        self.frame_juego = tk.Frame(self.frame_principal, bg='navy')
        self.frame_juego.pack(expand=True, fill=tk.BOTH)

        # Frame de controles
        self.frame_controles = tk.Frame(self.frame_juego, bg='navy')
        self.frame_controles.pack(side=tk.RIGHT, padx=20, pady=10, fill=tk.Y)

        # Frame puntaje
        self.label_puntaje = tk.Label(
            self.frame_controles, text="🏅 Puntaje: 0", font=self.fuente_botones, bg="white"
        )
        self.label_puntaje.pack(fill=tk.X, pady=5)
        
        # Título
        tk.Label(self.frame_juego, text="JUEGO DE LETRAS", font=self.fuente_titulo, bg='navy', fg='white').pack(pady=10)

        

        # Frame para el cronometro
        self.label_cronometro = tk.Label(self.frame_controles, text="⏱️ Tiempo: 00:00", font=self.fuente_botones, bg="white")
        self.label_cronometro.pack(fill=tk.X, pady=5)
        self.label_cronometro.bind("<Button-1>", self.toggle_cronometro_texto)

        self.boton_pausa = tk.Button(
            self.frame_controles,
            text="Pausar",
            font=self.fuente_botones,
            bg="orange",
            command=self.toggle_cronometro
        )
        self.boton_pausa.pack(fill=tk.X, pady=5)
        
        # Tablero de letras (5x5 como ejemplo)
        self.frame_tablero = tk.Frame(self.frame_juego, bg='navy')
        self.frame_tablero.pack(side=tk.LEFT, padx=20, pady=10)

        # Frame oculto para pausa
        self.overlay_pausa = tk.Frame(self.frame_juego, bg="black", width=600, height=500)
        self.overlay_pausa.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.overlay_pausa.place_forget()  # Oculto por defecto

        self.label_pausa = tk.Label(
            self.overlay_pausa, text="⏸ El juego está pausado", font=("Arial", 20), fg="white", bg="black", 
        )
        self.label_pausa.pack(fill=tk.BOTH, expand=True, side=tk.TOP,pady=20)

        self.boton_reanudar_overlay = tk.Button(
            self.overlay_pausa, text="Reanudar", font=("Arial", 14), command=self.reanudar_desde_overlay
        )
        self.boton_reanudar_overlay.pack(pady=10)

        
        # Matriz de letras
        self.botones_letras = []
        self.generar_tablero_dinamico()
        
        for i in range(len(self.matriz_letras)):
            fila_botones = []
            for j in range(len(self.matriz_letras[i])):
                btn = tk.Button(
                    self.frame_tablero, 
                    text=self.matriz_letras[i][j], 
                    font=self.fuente_letras,
                    width=4, 
                    height=2,
                    relief=tk.RAISED,
                    bg='lightblue',
                    command=lambda i=i, j=j: self.seleccionar_letra(i, j)
                )
                btn.grid(row=i, column=j, padx=2, pady=2)
                fila_botones.append(btn)
            self.botones_letras.append(fila_botones)

        
        # Palabra actual
        self.label_palabra = tk.Label(self.frame_controles, text="", font=self.fuente_letras, bg='navy', fg='white')
        self.label_palabra.pack(pady=10)
        
        # Botones de acción
        tk.Button(
            self.frame_controles, 
            text="Borrar", 
            font=self.fuente_botones,
            bg='lightblue',
            command=self.borrar_seleccion
        ).pack(fill=tk.X, pady=5)
        
        tk.Button(
            self.frame_controles, 
            text="Aplicar", 
            font=self.fuente_botones,
            bg='lightblue',
            command=self.validar_palabra
        ).pack(fill=tk.X, pady=5)
        
        tk.Button(
            self.frame_controles, 
            text="Reiniciar", 
            font=self.fuente_botones,
            bg='lightblue',
            command=self.reiniciar_juego
        ).pack(fill=tk.X, pady=5)

        tk.Button(
            self.frame_controles, 
            text="Pista", 
            font=self.fuente_botones,
            bg='khaki1',
            command=self.mostrar_pista
        ).pack(fill=tk.X, pady=5)

        # Palabras encontradas
        self.frame_palabras = tk.Frame(self.frame_controles, bg='navy')
        self.frame_palabras.pack(pady=10)
        
        tk.Label(self.frame_palabras, text="Palabras encontradas:", font=self.fuente_botones, bg='navy', fg='white').pack()
        self.lista_palabras = tk.Listbox(self.frame_palabras, width=20, height=10, bg='lightblue')
        self.lista_palabras.pack()
        
        # Estadísticas
        self.frame_stats = tk.Frame(self.frame_controles, bg='navy')
        self.frame_stats.pack(pady=10)
        
        tk.Label(self.frame_stats, text="Estadísticas:", font=self.fuente_botones, bg='navy', fg='white').pack()
        self.label_stats = tk.Label(self.frame_stats, text="Jugados: 0\nCompletados: 0%", justify=tk.LEFT, bg='navy', fg='white')
        self.label_stats.pack()

        tk.Button(
            self.frame_controles, 
            text="Menú", 
            font=self.fuente_botones,
            bg='lightblue',
            command=root.destroy
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
            valido = (delta_fila == 1 and delta_col == 0) or (delta_fila == 0 and delta_col == 1)

        if valido:
            boton = self.botones_letras[fila][columna]
            boton.config(relief=tk.SUNKEN, bg='lightgreen', state=tk.DISABLED)
            self.letras_seleccionadas.append((fila, columna))
            self.label_palabra.config(text=self.obtener_palabra_actual())

    def obtener_palabra_actual(self):
        return ''.join([self.matriz_letras[fila][col] for fila, col in self.letras_seleccionadas])
    
    def borrar_seleccion(self):
        for fila, col in self.letras_seleccionadas:
            boton = self.botones_letras[fila][col]
            boton.config(relief=tk.RAISED, bg='lightblue', state=tk.NORMAL)
        self.letras_seleccionadas = []
        self.label_palabra.config(text="")
    
    def validar_palabra(self):
        palabra = self.obtener_palabra_actual()
        
        if not palabra:
            messagebox.showwarning("Atención", "No has seleccionado ninguna letra.")
            return
        
        if palabra in self.palabras_validas and palabra not in self.palabras_encontradas: # Agregar palabra encontrada
            self.palabras_encontradas.append(palabra)
            self.lista_palabras.insert(tk.END, palabra)
            messagebox.showinfo("¡Correcto!", f"¡Encontraste la palabra {palabra}!")
            # -------------------------------------------------------------------------------------- Calcular puntos
            segundos = self.tiempo_transcurrido or 1
            puntos_palabra = len(palabra)*len(palabra)*len(palabra)*len(palabra)*len(palabra) // segundos
            if (self.pista):
                self.puntaje += puntos_palabra // 3
                self.pista = 0
            else:
                self.puntaje += puntos_palabra
            self.label_puntaje.config(text=f"🏅 Puntaje: {self.puntaje}")
            # Verificar fin del juego
            if len(self.palabras_encontradas) == 7:
                self.finalizar_juego()
            self.borrar_seleccion()
        else:
            # Cambiar a rojo las letras seleccionadas
            for fila, col in self.letras_seleccionadas:
                self.botones_letras[fila][col].config(bg='firebrick1')
            
            # Volver al color original después de 1,5 seg
            self.root.after(1500, self.borrar_seleccion)
            messagebox.showwarning("Incorrecto", "La palabra no es válida o ya fue encontrada.")
        
        self.actualizar_estadisticas()
    
    def reiniciar_juego(self):
        self.generar_tablero_dinamico()

        for i in range(len(self.matriz_letras)):
            for j in range(len(self.matriz_letras[i])):
                letra = self.matriz_letras[i][j]
                btn = self.botones_letras[i][j]
                btn.config(text=letra, relief=tk.RAISED, bg='lightblue', state=tk.NORMAL)

        self.borrar_seleccion()
        self.palabras_encontradas = []
        self.lista_palabras.delete(0, tk.END)
        self.actualizar_estadisticas()
        self.reiniciar_cronometro()
        self.puntaje = 0
        self.label_puntaje.config(text="🏅 Puntaje: 0")
    
    def actualizar_estadisticas(self):
        total_palabras = len(self.palabras_validas)
        encontradas = len(self.palabras_encontradas)
        porcentaje = (encontradas / total_palabras) * 100 if total_palabras > 0 else 0
        self.label_stats.config(text=f"Jugados: {encontradas}\nCompletados: {porcentaje:.2f}%")

    def buscar_palabra_en_matriz(self, palabra):
        FILAS = len(self.matriz_letras)
        COLUMNAS = len(self.matriz_letras[0])
        DIRECCIONES = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        def dfs(f, c, indice, visitado):
            if not (0 <= f < FILAS and 0 <= c < COLUMNAS):
                return None
            if (f, c) in visitado:
                return None
            if self.matriz_letras[f][c] != palabra[indice]:
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
                if self.matriz_letras[i][j] == palabra[0]:
                    camino = dfs(i, j, 0, set())
                    if camino:
                        return camino
        return None

    def mostrar_pista(self):
        self.pista = 1
        posibles = [p for p in self.palabras_validas if p not in self.palabras_encontradas]
        if not posibles:
            messagebox.showinfo("Pista", "¡Ya encontraste todas las palabras!")
            return
    
        palabra = random.choice(posibles)
        camino = self.buscar_palabra_en_matriz(palabra)

        if not camino:
            messagebox.showwarning("Pista", f"No se pudo encontrar la palabra '{palabra}' en la matriz.")
            return

        for f, c in camino:
            self.botones_letras[f][c].config(bg='gold')
    
        # Restaurar colores después de 2 segundos
        self.root.after(2000, lambda: self.restaurar_colores(camino))

    def restaurar_colores(self, camino):
        for f, c in camino:
            estado = self.botones_letras[f][c]['state']
            color = 'lightgreen' if (f, c) in self.letras_seleccionadas else 'lightblue'
            self.botones_letras[f][c].config(bg=color)

    def actualizar_cronometro(self):
        if not self.timer_pausado:
            self.tiempo_transcurrido += 1
            minutos = self.tiempo_transcurrido // 60
            segundos = self.tiempo_transcurrido % 60
            if not self.timer_oculto:
                self.label_cronometro.config(text=f"⏱️ Tiempo: {minutos:02}:{segundos:02}")
            self.timer_id = self.root.after(1300, self.actualizar_cronometro)
    
    def pausar_cronometro(self):
        self.timer_pausado = True
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

    def reanudar_cronometro(self):
        if self.timer_pausado:
            self.timer_pausado = False
            self.actualizar_cronometro()

    def reiniciar_cronometro(self):
        self.pausar_cronometro()
        self.tiempo_transcurrido = 0
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

    def toggle_cronometro_texto(self,event):
        if not self.timer_oculto:
            self.timer_oculto = True
            self.label_cronometro.config(text="⏱️ Tiempo: --:--")
        else:
            self.timer_oculto = False
            self.actualizar_cronometro()
    
    def reanudar_desde_overlay(self):
        self.overlay_pausa.place_forget()
        self.toggle_cronometro()  # Esto cambia el estado a "reanudar"

    def finalizar_juego(self):
        self.pausar_cronometro()
        minutos = self.tiempo_transcurrido // 60
        segundos = self.tiempo_transcurrido % 60
        tiempo_str = f"{minutos:02}:{segundos:02}"

        messagebox.showinfo("¡Felicidades!",f"Encontraste todas las palabras.\nTiempo: {tiempo_str}\nPuntaje: {self.puntaje}")
        

if __name__ == "__main__":
    root = tk.Tk()
    juego = JuegoLetras(root)
    root.mainloop()
