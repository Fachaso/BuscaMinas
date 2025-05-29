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
     #Vamos a medir las dimensiones del tablero
    cantidad_filas: int = len(tablero)
    cantidad_columnas: int = len(tablero[0])

# Creamos una copia del tablero original SOLO para leerlo mientras modiescribimos en el Original
    copia_tablero_original: list[list[int]] = []
    for fila_actual in tablero:
        copia_fila: list[int] = fila_actual.copy()
        copia_tablero_original.append(copia_fila)

# Lista de tuplas para recorrer las 8 direcciones posibles que rodean a una mina
    posiciones_vecinas: list[tuple[int, int]] = [
        (-1, -1), (-1, 0), (-1, 1),
        ( 0, -1),          ( 0, 1),
        ( 1, -1), ( 1, 0), ( 1, 1)
    ]

# Recorremos cada celda y contamos las minas vecinas

    for fila: int in range(cantidad_filas):
        for columna: int in range(cantidad_columnas):
            if copia_tablero_original[fila][columna] != -1:
                minas_adyacentes: int = 0
                for desplazamiento_fila, desplazamiento_columna in posiciones_vecinas:
                    fila_vecina: int = fila + desplazamiento_fila
                    columna_vecina: int = columna + desplazamiento_columna
                    if 0 <= fila_vecina < cantidad_filas and 0 <= columna_vecina < cantidad_columnas:
                        if copia_tablero_original[fila_vecina][columna_vecina] == -1:
                            minas_adyacentes += 1
                tablero[fila][columna] = minas_adyacentes


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
