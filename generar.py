import random
import string
import re
import time

FILAS, COLUMNAS = 5, 6
DIRECCIONES = [(-1, 0), (1, 0), (0, -1), (0, 1)]

LONGITUDES_OBJETIVO = [9, 8, 7, 7, 6, 6, 6]

# --------------------- Utilidades ---------------------

def leer_y_borrar_matriz(archivo="matrices_validas.txt"):
    with open(archivo, "r", encoding="utf-8") as f:
        lineas = f.readlines()

    matriz = []
    palabras = None
    inicio = 0

    for i, linea in enumerate(lineas):
        if linea.startswith("["):
            palabras = eval(linea.strip())
            inicio = i
            matriz = [lineas[i + j + 1].strip().split() for j in range(5)]
            break

    if palabras is None:
        raise RuntimeError("No hay matrices disponibles")

    # Guardar el resto del archivo
    with open(archivo, "w", encoding="utf-8") as f:
        f.writelines(lineas[i + 6:])  # 1 línea palabras + 5 matriz

    dict = {}
    dict["tablero"] = matriz
    dict["palabras_colocadas"] = palabras
    return dict

def crear_matriz_vacia():
    return [['' for _ in range(COLUMNAS)] for _ in range(FILAS)]

def es_valido(f, c):
    return 0 <= f < FILAS and 0 <= c < COLUMNAS

def copiar_matriz(m):
    return [fila.copy() for fila in m]

def cargar_diccionario(path="diccionario_curado.txt"):
    por_longitud = {}
    with open(path, "r", encoding="utf-8") as f:
        for linea in f:
            palabra = linea.strip().upper()
            if palabra.isalpha():
                por_longitud.setdefault(len(palabra), []).append(palabra)
    return por_longitud

# ------------------ Búsqueda de caminos ------------------
def generar_camino(matriz, longitud):
    posiciones = [(f, c) for f in range(FILAS) for c in range(COLUMNAS)]
    random.shuffle(posiciones)

    for f, c in posiciones:
        camino = dfs_camino(matriz, f, c, longitud, set())
        if camino:
            return camino
    return None

def dfs_camino(matriz, f, c, restante, visitado):
    if not es_valido(f, c) or (f, c) in visitado:
        return None

    visitado.add((f, c))

    if restante == 1:
        return [(f, c)]

    random.shuffle(DIRECCIONES)
    for df, dc in DIRECCIONES:
        res = dfs_camino(matriz, f + df, c + dc, restante - 1, visitado.copy())
        if res:
            return [(f, c)] + res

    return None

# ------------------ Patron y búsqueda ------------------
def construir_patron(matriz, camino):
    return ''.join(matriz[f][c] if matriz[f][c] else '0' for f, c in camino)

def buscar_palabra_por_patron(patron, diccionario):
    regex = re.compile("^" + patron.replace('0', '.') + "$")
    posibles = diccionario.get(len(patron), [])
    random.shuffle(posibles)
    for palabra in posibles:
        if regex.fullmatch(palabra):
            return palabra
    return None
# ------------------ Guardado en archivo ------------------
def guardar_matriz_en_archivo(matriz, palabras, archivo="matrices_validas.txt"):
    with open(archivo, "a", encoding="utf-8") as f:
        f.write(str(palabras) + "\n")
        for fila in matriz:
            f.write(" ".join(fila) + "\n")
        f.write("\n")  # separador entre conjuntos

def contar_matrices_en_archivo(archivo="matrices_validas.txt"):
    with open(archivo, "r", encoding="utf-8") as f:
        return f.read().count("[")  # una línea con [ indica un conjunto de palabras

def generador_continuo_matrices(archivo="matrices_validas.txt", intervalo=1, max_matrices=15):
    while True:
        try:
            if contar_matrices_en_archivo(archivo) >= max_matrices:
                time.sleep(intervalo)
                continue

            matriz, palabras = generar_sopa_inteligente()
            guardar_matriz_en_archivo(matriz, palabras, archivo)
            print("✅ Matriz guardada con:", palabras)
        except Exception as e:
            print("⚠️ Error generando matriz:", e)
        time.sleep(intervalo)

# ------------------ Generador principal ------------------
def generar_sopa_inteligente(diccionario_path="diccionario_curado.txt", max_reintentos=100):
    diccionario = cargar_diccionario(diccionario_path)

    for _ in range(max_reintentos):
        matriz = crear_matriz_vacia()
        palabras_colocadas = []
        exito = True

        for longitud in LONGITUDES_OBJETIVO:
            for _ in range(200):  # intentos por palabra
                camino = generar_camino(matriz, longitud)
                if not camino:
                    break
                patron = construir_patron(matriz, camino)
                palabra = buscar_palabra_por_patron(patron, diccionario)
                if palabra and palabra not in palabras_colocadas:
                    for (f, c), letra in zip(camino, palabra):
                        matriz[f][c] = letra
                    palabras_colocadas.append(palabra)
                    break
            else:
                exito = False
                break

        if exito:
            for i in range(FILAS):
                for j in range(COLUMNAS):
                    if matriz[i][j] == '':
                        matriz[i][j] = random.choice(string.ascii_uppercase)
            return matriz, palabras_colocadas

    raise RuntimeError("No se pudo generar una sopa válida tras varios intentos")

# # ------------------ Ejemplo de uso ------------------
# if __name__ == "__main__":
#     generador_continuo_matrices()
