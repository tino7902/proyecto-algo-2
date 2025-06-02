import random
import string
import re
from collections import defaultdict

FILAS = 5
COLUMNAS = 6
DIRECCIONES = [(-1, 0), (1, 0), (0, -1), (0, 1)]

LONGITUDES_OBJETIVO = [9, 8, 8, 7, 7, 6, 6]
PALABRAS_INICIALES = LONGITUDES_OBJETIVO[:3]
PALABRAS_RESTO = LONGITUDES_OBJETIVO[3:]

def crear_matriz_vacia():
    return [['' for _ in range(COLUMNAS)] for _ in range(FILAS)]

def es_valido(f, c):
    return 0 <= f < FILAS and 0 <= c < COLUMNAS

def seleccionar_palabras(diccionario_path, longitudes):
    palabras_por_longitud = defaultdict(list)
    with open(diccionario_path, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            palabra = linea.strip().upper()
            if palabra.isalpha() and len(palabra) in longitudes:
                palabras_por_longitud[len(palabra)].append(palabra)

    seleccionadas = []
    for l in longitudes:
        if not palabras_por_longitud[l]:
            raise ValueError(f"No hay palabras de longitud {l}")
        p = random.choice(palabras_por_longitud[l])
        seleccionadas.append(p)
        palabras_por_longitud[l].remove(p)
    return seleccionadas

def buscar_camino(matriz, palabra, f, c, idx, visitado):
    if not es_valido(f, c) or (f, c) in visitado:
        return None
    letra_actual = palabra[idx]
    celda = matriz[f][c]
    if celda != '' and celda != letra_actual:
        return None

    visitado.add((f, c))
    if idx == len(palabra) - 1:
        return [(f, c)]

    random.shuffle(DIRECCIONES)
    for df, dc in DIRECCIONES:
        camino = buscar_camino(matriz, palabra, f + df, c + dc, idx + 1, visitado.copy())
        if camino:
            return [(f, c)] + camino
    return None

def insertar_palabra(matriz, palabra):
    posiciones = [(i, j) for i in range(FILAS) for j in range(COLUMNAS)]
    random.shuffle(posiciones)
    for f, c in posiciones:
        camino = buscar_camino(matriz, palabra, f, c, 0, set())
        if camino:
            for (x, y), letra in zip(camino, palabra):
                matriz[x][y] = letra
            return True
    return False

def buscar_palabra_por_patron(patron, diccionario_path="diccionario_curado.txt"):
    regex = re.compile("^" + ''.join("." if c == "0" else c for c in patron) + "$")
    with open(diccionario_path, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            palabra = linea.strip().upper()
            if regex.fullmatch(palabra):
                return palabra
    return None

def generar_caminos_desde_letras(matriz, longitud):
    caminos = []

    def dfs(camino, visitado):
        if len(camino) == longitud:
            caminos.append(camino)
            return
        ult = camino[-1]
        for df, dc in DIRECCIONES:
            nf, nc = ult[0] + df, ult[1] + dc
            if es_valido(nf, nc) and (nf, nc) not in visitado:
                camino_nuevo = camino + [(nf, nc)]
                dfs(camino_nuevo, visitado | {(nf, nc)})

    letras_usadas = [(i, j) for i in range(FILAS) for j in range(COLUMNAS) if matriz[i][j] != '']
    random.shuffle(letras_usadas)
    for f, c in letras_usadas:
        dfs([(f, c)], {(f, c)})
        if len(caminos) > 20:
            break
    return caminos

def obtener_patron(matriz, camino):
    return ''.join(matriz[f][c] if matriz[f][c] != '' else '0' for f, c in camino)

def insertar_palabra_por_patron(matriz, palabra, camino):
    for (f, c), letra in zip(camino, palabra):
        matriz[f][c] = letra

def generar_sopa_final(diccionario_path="diccionario_curado.txt", max_reintentos=50):
    for _ in range(max_reintentos):
        matriz = crear_matriz_vacia()
        palabras_colocadas = []

        try:
            palabras_iniciales = seleccionar_palabras(diccionario_path, PALABRAS_INICIALES)
        except ValueError:
            continue

        exito = True
        for palabra in palabras_iniciales:
            if not insertar_palabra(matriz, palabra):
                exito = False
                break
            palabras_colocadas.append(palabra)
        if not exito:
            continue

        try:
            palabras_restantes = seleccionar_palabras(diccionario_path, PALABRAS_RESTO)
        except ValueError:
            continue

        for longitud in PALABRAS_RESTO:
            caminos = generar_caminos_desde_letras(matriz, longitud)
            random.shuffle(caminos)
            palabra_insertada = False
            for camino in caminos:
                patron = obtener_patron(matriz, camino)
                palabra = buscar_palabra_por_patron(patron, diccionario_path)
                if palabra and palabra not in palabras_colocadas:
                    insertar_palabra_por_patron(matriz, palabra, camino)
                    palabras_colocadas.append(palabra)
                    palabra_insertada = True
                    break
            if not palabra_insertada:
                exito = False
                break

        if exito and len(palabras_colocadas) == 7:
            for i in range(FILAS):
                for j in range(COLUMNAS):
                    if matriz[i][j] == '':
                        matriz[i][j] = random.choice(string.ascii_uppercase)
            return matriz, palabras_colocadas

    raise RuntimeError("No se pudo generar una sopa válida tras múltiples intentos.")

if _name_ == "_main_":
    matriz, palabras = generar_sopa_final("diccionario_curado.txt")
    for fila in matriz:
        print(' '.join(fila))
    print("\nPalabras insertadas:", palabras)