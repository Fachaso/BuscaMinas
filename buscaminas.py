import random
from typing import Any
import os

# Constantes para dibujar
BOMBA = chr(128163)  # simbolo de una mina
BANDERA = chr(127987)  # simbolo de bandera blanca
VACIO = " "  # simbolo vacio inicial

# Tipo de alias para el estado del juego
EstadoJuego = dict[str, Any]

def existe_archivo(ruta_directorio: str, nombre_archivo:str) -> bool:
    """Chequea si existe el archivo en la ruta dada"""
    return os.path.exists(os.path.join(ruta_directorio, nombre_archivo))

def colocar_minas(filas:int, columnas: int, minas:int) -> list[list[int]]:
#construccion de la matriz
    matrizres: list[list[int]] = []
    for _ in range(filas):
        fila: list[int] = []
        for _ in range(columnas):
            fila.append(0)
        matrizres.append(fila)
#Generamos las posiciones poibles para la ubicacion de las minas
    
    posiciones: list[tuple[int, int]] = []
    for i in range(filas):
        for j in range(columnas):
            posiciones.append((i, j))

#Elegimos las posiciones aleatorias para colocar las minas en la matriz
    posiciones_minas: list[tuple[int, int]] = random.sample(posiciones, minas)

#colocar -1 en las posiciones seleccionadas para las minas
    for (i, j) in posiciones_minas:
    matrizres[i][j] = -1

    return matrizres
    
def es_matriz(t: list[list]) -> bool:
    if len(t) == 0 or len(t[0]) == 0:
        return False
    cantidad_columnas: int = len(t[0])
    for fila in t:
        if len(fila) != cantidad_columnas:
            return False
    return True

def calcular_numeros(tablero: list[list[int]]) -> None:
    return


def crear_juego(filas:int, columnas:int, minas:int) -> EstadoJuego:
    return {}


def obtener_estado_tablero_visible(estado: EstadoJuego) -> list[list[str]]:
    return [[]]


def marcar_celda(estado: EstadoJuego, fila: int, columna: int) -> None:
    return


def descubrir_celda(estado: EstadoJuego, fila: int, columna: int) -> None:
    return


def verificar_victoria(estado: EstadoJuego) -> bool:
    return True


def reiniciar_juego(estado: EstadoJuego) -> None:
    return


def guardar_estado(estado: EstadoJuego, ruta_directorio: str) -> None:
    return


def cargar_estado(estado: EstadoJuego, ruta_directorio: str) -> bool:
    return False
