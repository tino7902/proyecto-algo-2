import tkinter as tk
from tkinter import messagebox, font
import os
import json

DIR_PARTIDAS = "partidas/juego1"

def guardar_partida(user, estado_juego):
    os.makedirs(DIR_PARTIDAS, exist_ok=True)
    dir_archivo = os.path.join(DIR_PARTIDAS, f"{user}.json")
    try:
        with open(dir_archivo, 'w') as f:
            json.dump(estado_juego, f, indent=2)
        print(f"partida de {user} guardada en {dir_archivo}")
    except IOError as e:
        print(f"error al guardar la partido: {e}")

def cargar_partida(user):
    dir_archivo = os.path.join(DIR_PARTIDAS, f"{user}.json")
    if not os.path.exists(dir_archivo):
        print("no hay partida guardada de {user}")
        return None
    
    try:
        with open(dir_archivo, 'r') as f:
            estado_juego = json.load(f)
        print(f"partida de {user} cargada")
        return estado_juego
    except json.JSONDecodeError as e:
        print(f"error al leer el json: {e}")
        return None
    except IOError as e:
        print(f"error al cargar la partida: {e}")
        return None

class JuegoLetras:
    def __init__(self):
        self.app = tk.Tk()
        self.app.title("Juego de Letras")
        self.app.geometry("800x600")
        self.app.configure(bg='navy')  # Fondo azul marino
        
        # Configuración de estilos
        self.fuente_letras = font.Font(family='Helvetica', size=16, weight='bold')
        self.fuente_botones = font.Font(family='Helvetica', size=12)
        self.fuente_titulo = font.Font(family='Helvetica', size=20, weight='bold')
        
        # Variables del juego
        self.palabras_encontradas = []
        self.letras_seleccionadas = []
        self.palabras_validas = ["PIEDRA", "TOXICA", "LETRAS", "LEBE"]  # Ejemplo
        
        # Crear interfaz
        self.crear_interfaz()
    
    def crear_interfaz(self):
        # Frame principal
        self.frame_principal = tk.Frame(self.app, padx=20, pady=20, bg='navy')
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
        self.matriz_letras = [
            ['G', 'A', 'A', 'J', 'E', 'C'],
            ['R', 'S', 'L', 'I', 'P', 'N'],
            ['A', 'P', 'A', 'D', 'C', 'O'],
            ['D', 'I', 'T', 'O', 'X', 'I'],
            ['O', 'E', 'D', 'R', 'A', 'C']
        ]
        
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
        self.botones_letras[fila][columna].config(relief=tk.SUNKEN, bg='lightgreen')
        self.letras_seleccionadas.append((fila, columna))
        self.label_palabra.config(text=self.obtener_palabra_actual())
    
    def obtener_palabra_actual(self):
        return ''.join([self.matriz_letras[fila][col] for fila, col in self.letras_seleccionadas])
    
    def borrar_seleccion(self):
        for fila, col in self.letras_seleccionadas:
            self.botones_letras[fila][col].config(relief=tk.RAISED, bg='lightblue')
        self.letras_seleccionadas = []
        self.label_palabra.config(text="")
    
    def validar_palabra(self):
        palabra = self.obtener_palabra_actual()
        
        if not palabra:
            messagebox.showwarning("Atención", "No has seleccionado ninguna letra.", parent=self.app)
            return
        
        if palabra in self.palabras_validas and palabra not in self.palabras_encontradas:
            self.palabras_encontradas.append(palabra)
            self.lista_palabras.insert(tk.END, palabra)
            messagebox.showinfo("¡Correcto!", f"¡Encontraste la palabra {palabra}!", parent=self.app)
            self.borrar_seleccion()
        else:
            # Cambiar a rojo las letras seleccionadas
            for fila, col in self.letras_seleccionadas:
                self.botones_letras[fila][col].config(bg='firebrick1')
            
            # Volver al color original después de 1,5 seg
            self.app.after(1500, self.borrar_seleccion)
            messagebox.showwarning("Incorrecto", "La palabra no es válida o ya fue encontrada.", parent=self.app)
        
        self.actualizar_estadisticas()
    
    def reiniciar_juego(self):
        self.borrar_seleccion()
        self.palabras_encontradas = []
        self.lista_palabras.delete(0, tk.END)
        self.actualizar_estadisticas()
    
    def actualizar_estadisticas(self):
        total_palabras = len(self.palabras_validas)
        encontradas = len(self.palabras_encontradas)
        porcentaje = (encontradas / total_palabras) * 100 if total_palabras > 0 else 0
        self.label_stats.config(text=f"Jugados: {encontradas}\nCompletados: {porcentaje:.2f}%")

def iniciarJuego1(user):
    juego = JuegoLetras()
    juego.app.mainloop()
