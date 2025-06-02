import tkinter as tk
from tkinter import messagebox, font
import random
from collections import defaultdict
import string
from generar import generar_sopa_final

class JuegoLetras:
    def _init_(self, root):
        self.root = root
        self.root.title("Juego de Letras")
        self.root.geometry("800x600")
        self.root.configure(bg='navy')  # Fondo azul marino
        
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
        self.matriz_letras, self.palabras_validas = generar_sopa_final()
        print(self.palabras_validas)

        
    
    def crear_interfaz(self):
        # Frame principal
        self.frame_principal = tk.Frame(self.root, padx=20, pady=20, bg='navy')
        self.frame_principal.pack(expand=True, fill=tk.BOTH)
        
        # Título
        tk.Label(self.frame_principal, text="JUEGO DE LETRAS", font=self.fuente_titulo, bg='navy', fg='white').pack(pady=10)
        
        # Frame para el tablero y controles
        self.frame_juego = tk.Frame(self.frame_principal, bg='navy')
        self.frame_juego.pack(expand=True, fill=tk.BOTH)
        
        # Tablero de letras (5x5 como ejemplo)
        self.frame_tablero = tk.Frame(self.frame_juego, bg='navy')
        self.frame_tablero.pack(side=tk.LEFT, padx=20, pady=10)
        
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
        
        # Frame de controles
        self.frame_controles = tk.Frame(self.frame_juego, bg='navy')
        self.frame_controles.pack(side=tk.RIGHT, padx=20, pady=10, fill=tk.Y)
        
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
        
        if palabra in self.palabras_validas and palabra not in self.palabras_encontradas:
            self.palabras_encontradas.append(palabra)
            self.lista_palabras.insert(tk.END, palabra)
            messagebox.showinfo("¡Correcto!", f"¡Encontraste la palabra {palabra}!")
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

if __name__ == "_main_":
    root = tk.Tk()
    juego = JuegoLetras(root)
    root.mainloop()