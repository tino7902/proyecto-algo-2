from random import randint, shuffle, sample, choice
import tkinter as tk
import time

#Esta es simplemente otra manera de leer las palabras del archivo txt, en caso de que se genere de otra manera
#Ya que en mi programa lee el archivo de "palabras.txt" teniendo en cuenta que todás están una debajo de la otra
"""anagramas = []
with open("palabras.txt", "r", encoding="utf-8") as archivo:
    contenido = archivo.read()
    palabras = contenido.strip().split()
    for palabra in palabras:
        anagramas.append(palabra)
"""

combinacionesLetras=[
["u", "a", "e", "r", "d", "j", "q"],
["p", "o", "u", "g", "e", "i", "s"],
["j", "e", "o", "c", "r", "p", "a"],
["n", "u", "e", "r", "l", "b", "a"],
["p", "i", "e", "u", "l", "j", "o"]
]


#Clase para usarla luego con el times
class TimerState:
    def __init__(self):
        self.tiempo_inicio = time.time()
        self.tiempo_pausado = 0
        self.activo = True
        self.id = None

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


#Calcula el puntaje
def calcularPuntaje(palabraIngresada):
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
    
#Obtiene una lista con las letras únicas
def obtenerLetras(lista_palabras):
    palabra_mas_unica = ""
    max_letras_unicas = 0
    letras_resultado = []

    for palabra in lista_palabras:
        letras_unicas = []
        for letra in palabra:
            if letra not in letras_unicas:
                letras_unicas.append(letra)
        
        if len(letras_unicas) > max_letras_unicas:
            max_letras_unicas = len(letras_unicas)
            palabra_mas_unica = palabra
            letras_resultado = letras_unicas

    return letras_resultado

#Calcula si la palabra es Heptacrack (Contiene 7 letras distintas)
def esHeptacrack(palabraIngresada):
    letrasUnicas= obtenerLetras(seleccionadas)
    letrasDiferentes= 0
    if letra in palabraIngresada:
        if letra in letrasUnicas:
            letrasDiferentes= letrasDiferentes + 1
    if letrasDiferentes == len(letrasUnicas):
        return True
    return False

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
#Lista para almacenar las palabras que se vayan ingresando en el juego
palabrasElegidas = []

palabrasElegidasSinEspacios= []

print(seleccionadas)
print("                  ↑                  ")
print("Lista de seleccionados (solo de guía para completar el juego)\n")

#Verifica si la palabra ingresada al clickear los botones, está en la lista de palabrasElegidas, y si cumple las condiciones necesarias
#Además de Imprimir los pts obtenidos, totales, y verificar si se encontraron todas las palabras para terminar el juego
def iniciarReto(palIngresada, mensajeLabel1, mensajeLabel2):
    global ptsTotal

    Pal = palIngresada
    if Pal in seleccionadas and Pal not in palabrasElegidas:
        if verificarPalabra(Pal.upper(), listaAleatoriaCombinaciones, letraCentral):
            pts = calcularPuntaje(Pal)
            ptsTotal= ptsTotal + pts
            palabrasElegidas.append(Pal)
            palabrasElegidasSinEspacios= ", ".join(palabrasElegidas)
            if esHeptacrack==True:
                mensajeLabel1.config(text=f"ES HEPTACRACK!\nHaz obtenido {pts} punto/s || Tienes {ptsTotal} punto/s en total")
            else:
                mensajeLabel1.config(text=f"Haz obtenido {pts} punto/s || Tienes {ptsTotal} punto/s en total")
            mensajeLabel2.config(text=f"Palabras encontradas: {len(palabrasElegidas)}/{len(seleccionadas)}")
            mensajePalabrasElegidas.config(text=f"Palabras encontradas: {palabrasElegidasSinEspacios}")
            if len(palabrasElegidas) == len(seleccionadas):
                mostrarFelicitacionFinal()
        else:
            mensajeLabel1.config(text=f"La palabra no contiene la letra {letraCentral} o es demasiado corta.")
    elif Pal in palabrasElegidas:
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
    palabraIngresada = letra.get()
    iniciarReto(palabraIngresada, mensaje1, mensaje2)
    letra.set("")

#Al ir dando clic a los botones, imprime en un espacio llamado "iniciarReto" (Línea 346) la letra que contiene cada botón y va generando la palabra
def actualizarLetra(letra_boton):
    letra_actual = letra.get()
    letra.set(letra_actual + letra_boton)

#En el espacio llamado "iniciarReto" (Línea 346), simplemente elimina la última letra que se ingreso
def borrarUltimaLetra():
    texto_actual = letra.get()
    if len(texto_actual) > 0:
        letra.set(texto_actual[:-1])

#Al encontrar la cantidad de palabras generadas por el juego, muestra en la ventana un mensajede felicitaciones
def mostrarFelicitacionFinal():
    capa = tk.Frame(
        app, 
        bg='white'
    )
    capa.place(
        relx=0, 
        rely=0, 
        relwidth=1, 
        relheight=1
    )

    mensaje = tk.Label(
        capa,
        text=f"¡Felicidades por ganar!🎉\nMis Estadísticas\nNombre de usuario: Marcelo López\nPuntaje obtenido: {ptsTotal}\n",
        font=("Courier", 16, "bold"),
        fg="green",
        bg="white",
        justify="center"
    )
    mensaje.pack(expand=True)

    #Botón para cerrar el juego
    cerrar_btn = tk.Button(
        capa,
        text="Cerrar juego",
        font=("Courier", 14),
        bg="#ff4444",
        fg="white",
        command=app.destroy
    )
    cerrar_btn.pack(pady=20)

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


#Inicio de la aplicación o ventana o widget o como se quiera llamar
app= tk.Tk()
letra= tk.StringVar(app)
letra.set("")
entrada= tk.StringVar(app)

#Desde aquí hasta la línea 238, son funciones que realizan justamente lo que dicen sus nombres. Funciones que luego se llaman al pausar o continuar el juego
timer_state = TimerState()
tiempo_label = tk.Label(
    app, 
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

def actualizar_timer():
    if timer_state.activo:
        tiempo_transcurrido = time.time() - timer_state.tiempo_inicio
        minutos = int(tiempo_transcurrido // 60)
        segundos = int(tiempo_transcurrido % 60)
        tiempo_label.config(text=f"{minutos:02d}:{segundos:02d}")
        timer_state.id = app.after(1000, actualizar_timer)

def pausar_timer():
    if timer_state.activo:
        timer_state.activo = False
        timer_state.tiempo_pausado = time.time() - timer_state.tiempo_inicio
        if timer_state.id:
            app.after_cancel(timer_state.id)

def reanudar_timer():
    if not timer_state.activo:
        timer_state.tiempo_inicio = time.time() - timer_state.tiempo_pausado
        timer_state.activo = True
        actualizar_timer()

#Pausa el juego...
def pausarJuego():
    pausar_timer()
    pausa_capa = tk.Frame(app, bg="#222222")
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
    boton_continuar = tk.Button(
        pausa_capa,
        text="Continuar",
        font=("Courier", 14),
        bg="#44cc44",
        fg="white",
        command=lambda: [pausa_capa.destroy(), reanudar_timer()]
    )
    boton_continuar.pack(pady=20)

    #Botón para salir de la aplicación
    boton_salir = tk.Button(
        pausa_capa,
        text="Salir del Juego",
        font=("Courier", 14),
        bg="#cc4444",
        fg="white",
        command=app.destroy
    )
    boton_salir.pack(pady=10)

#Hace que el timer empieze nada más abrir el juego
actualizar_timer()

#Da un tamaño a la aplicación
app.geometry("880x600")
tk.Wm.wm_title(app, "Lexi Reto")

#Botón que ejecuta la función "pausarJuego"
boton_pausa = tk.Button(
    app,
    text="⏸ Pausa",
    font=("Courier", 10),
    bg="#999999",
    command=pausarJuego
)
boton_pausa.place(
    x= 780,
    y= 0,
    width=100,
    height=30
)

#Botón que manda a la función "iniciarReto" la palabra ingresada
aplicar= tk.Button(
    app,
    text=("Aplicar"),
    font=("Courier", 14),
    fg=("black"),
    command=aplicarEntrada ,
    relief="ridge"
).place(
    x= 300,
    y= 130,
    width= 100,
    height= 40
)

#Espacio en donde se mostrarán las letras que se vayan ingresando mediante los botones
ingresoLetras= tk.Label(
    app,
    text="",
    textvariable=letra,
    font=("Courier", 10),
    fg="white",
    bg="#333333",
    relief="ridge",
    justify="center",
    wraplength=190,
    width=10,
    height=5,
)
ingresoLetras.place(
    x= 10,
    y= 60,
    width= 190,
    height= 50
)

#A partir de acá, hasta la línea 440, son los botones en donde apareceran las letras escogidas
boton1 = tk.Button(
    app,
    text=letras_botones[0],
    font=("Courier", 15),
    fg="black",
    relief="ridge",
    command=lambda: actualizarLetra(letras_botones[0])
)
boton1.place(
    x= 45,
    y= 120,
    width= 60,
    height= 40
)

boton2 = tk.Button(
    app,
    text=letras_botones[1],
    font=("Courier", 15),
    fg="black",
    relief="ridge",
    command=lambda: actualizarLetra(letras_botones[1])
)
boton2.place(
    x= 110,
    y= 120,
    width= 60,
    height= 40
)

boton3 = tk.Button(
    app,
    text=letras_botones[2],
    font=("Courier", 15),
    fg="black",
    relief="ridge",
    command=lambda: actualizarLetra(letras_botones[2])
)
boton3.place(
    x= 10,
    y= 185,
    width= 60,
    height= 40
)

boton4 = tk.Button(
    app,
    text=letraCentral.upper(),
    font=("Courier", 15),
    fg="black",
    bg="#ffc733",
    relief="ridge",
    command=lambda: actualizarLetra(letraCentral.upper())
)
boton4.place(
    x= 75,
    y= 185,
    width= 60,
    height= 40
)

boton5 = tk.Button(
    app,
    text=letras_botones[3],
    font=("Courier", 15),
    fg="black",
    relief="ridge",
    command=lambda: actualizarLetra(letras_botones[3])
)
boton5.place(
    x= 140,
    y= 185,
    width= 60,
    height= 40
)

boton6 = tk.Button(
    app,
    text=letras_botones[4],
    font=("Courier", 15),
    fg="black",
    relief="ridge",
    command=lambda: actualizarLetra(letras_botones[4])
)
boton6.place(
    x= 45,
    y= 250,
    width= 60,
    height= 40
)

boton7 = tk.Button(
    app,
    text=letras_botones[5],
    font=("Courier", 15),
    fg="black",
    relief="ridge",
    command=lambda: actualizarLetra(letras_botones[5])
)
boton7.place(
    x= 110,
    y= 250,
    width= 60,
    height= 40
)

#Botón para mezclar las letras generadas entre los botones
actualizar= tk.Button(
    app,
    text=("⟲"),
    font=("Courier", 15),
    fg=("black"),
    command=mezclarLetras,
    relief="ridge"
).place(
    x= 405,
    y= 130,
    width= 50,
    height= 40
)

#Botón para borrar la última letra ingresada
borrar= tk.Button(
    app,
    text=("BORRAR"),
    font=("Courier", 14),
    fg=("black"),
    command=borrarUltimaLetra,
    relief="ridge"
).place(
    x= 460,
    y= 130,
    width= 90,
    height= 40
)

#Imprime en un espacio la cantidad de puntos que se ganó en caso de acertar una palabra, y cuantos puntos tiene en total.
#Esta opción técnicamente no está en el juego original, pero se puede dejar como un extra
mensaje1 = tk.Label(
    app,
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
    x= 300,
    y= 200,
    width= 250,
    height= 50
)

#Imprime en un espacio la cantidad de palabras que lleva encontradas el usuario
mensaje2 = tk.Label(
    app,
    text=f"Palabras encontradas: {len(palabrasElegidas)}/{len(seleccionadas)}",
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
    x= 300,
    y= 60,
    width= 250,
    height= 50
)

mensajePalabrasElegidas = tk.Label(
    app,
    text="",
    font=("Courier", 10),
    fg="white",
    bg="#333333",
    relief="ridge",
    justify="center",
    wraplength=245,
    width=35,
    height=5
)
mensajePalabrasElegidas.place(
    x= 620,
    y= 60,
    width= 250,
    height= 520
)

mensajeInstrucciones = tk.Label(
    app,
    text="Cómo se juega:\nForma palabras de al menos 3 letras. Puedes repetir las letras, pero siempre incluyendo la letra central.\n No se admiten nombres propios, plurales y formas verbales conjugadas (solo infinitivos).\n Encuentra palabras que incluyan las 7 letras (¡Heptacrack!).\n Puntuación: las palabras de 3 letras dan 1 punto y las de 4 letras, 2 puntos. A partir de 5 letras, obtendrás tantos puntos como letras tenga la palabra. Los heptacracks valen 10 puntos.\n ATENCIÓN. Solo podrás resolver los lexi retos durante el día en que se publican. A las 12 de la noche quedan inactivos y solo se pueden consultar.",
    font=("Courier", 10),
    fg="white",
    bg="#333333",
    relief="ridge",
    justify="center",
    wraplength=500,
    width=35,
    height=5
)
mensajeInstrucciones.place(
    x= 10,
    y= 320,
    width= 540,
    height= 220
)

app.mainloop()