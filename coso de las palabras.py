# Abrir y filtrar palabras de un archivo
def cargar_palabras(ruta_archivo, min_long=4, max_long=7):
    palabras_filtradas = []
    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            palabra = linea.strip()
            # palabra = linea.strip().split()[0].lower()
            if min_long <= len(palabra) <= max_long and palabra.isalpha():
                palabras_filtradas.append(f"{palabra}\n")

    return palabras_filtradas

# Ejemplo de uso
ruta = "es_50k.txt"
  # archivo descargado de la fuente
diccionario = cargar_palabras(ruta)

# Ver algunas palabras
with open("palabras_potente.txt", mode="w") as f:
    f.writelines(diccionario)