import os
import json

""" Formato de json
{
  "tablero": [
    ["A", "B", "C"],
    ["D", "E", "F"]
  ],
  "palabras_colocadas": ["PEZ", "GATO", "SOL"],
  "palabras_encontradas": ["PEZ"],
  "palabras_pendientes": ["GATO", "SOL"],
  "tiempo_transcurrido": 120,
  "terminada": False
}
"""

def guardar_partida(user, estado_juego, juego):
    dir_partidas = f"partidas/{juego}"
    os.makedirs(dir_partidas, exist_ok=True)
    dir_archivo = os.path.join(dir_partidas, f"{user}.json")
    try:
        with open(dir_archivo, 'w') as f:
            json.dump(estado_juego, f, indent=2)
        print(f"partida de {user} guardada en {dir_archivo}")
    except IOError as e:
        print(f"error al guardar la partido: {e}")

def cargar_partida(user, juego):
    dir_partidas = f"partidas/{juego}"
    dir_archivo = os.path.join(dir_partidas, f"{user}.json")
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