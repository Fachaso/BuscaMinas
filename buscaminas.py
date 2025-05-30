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
    # Creamos el tablero con colocar_minas y lo guardamos en una variable
    tablero_con_minas: list[list[int]] = colocar_minas(filas, columnas, minas)
    
    #Completamos el tablero con numeros alrededor de las minas usando calcular_numeros()
    calcular_numeros(tablero_con_minas)

#HASTA ACA ya tenemos listo el tablero para incluirlo en el EstadoJuego

# Creamos tablero_visible , que es lo que ve el jugador al inicio, donde todo esta oculto. 
    tablero_visible: list[list[str]] = []
    for _ in range(filas):
        fila_visible: list[str] = []
        for _ in range(columnas):
            fila_visible.append(VACIO)
        tablero_visible.append(fila_visible)

# crear el diccionario estado con todas las claves
# {CLAVE,VALOR ESPERADO}

    estado: EstadoJuego = {
        "tablero": tablero_con_minas,
        "tablero_visible": tablero_visible,
        "filas": filas,
        "columnas": columnas,
        "minas": minas,
        "juego_terminado": False
    }

    return estado


def estado_valido(estado: EstadoJuego) -> bool:
    if not estructura_y_tipos_validos(estado):
        return False
# Estrucutura y y tipos
    tablero: list[list[int]] = estado["tablero"]
    tablero_visible: list[list[str]] = estado["tablero_visible"]
    filas: int = estado["filas"]
    columnas: int = estado["columnas"]
    minas: int = estado["minas"]
    juego_terminado: bool = estado["juego_terminado"]

    # verificar cantidad de minas
    cantidad: int = 0
    for fila in tablero:
        for celda in fila:
            if celda == -1:
                cantidad += 1
    if cantidad != minas:
        return False

    # verificar si tablero está bien numerado
    copia_tablero: list[list[int]] = []
    for fila in tablero:
        copia_tablero.append(fila.copy())
    calcular_numeros(copia_tablero)
    if copia_tablero != tablero:
        return False

    # juego terminado válido
    hay_bomba_visible: bool = False
    for i in range(filas):
        for j in range(columnas):
            if tablero_visible[i][j] == BOMBA:
                hay_bomba_visible = True
    todas_seguras_descubiertas: bool = todas_celdas_seguras_descubiertas(tablero, tablero_visible)
    if juego_terminado != (todas_seguras_descubiertas or hay_bomba_visible):
        return False

    # banderas solo sobre minas
    for i in range(filas):
        for j in range(columnas):
            if tablero_visible[i][j] == BANDERA and tablero[i][j] != -1:
                return False

    # los números visibles deben coincidir con el tablero
    for i in range(filas):
        for j in range(columnas):
            visible: str = tablero_visible[i][j]
            if visible != VACIO and visible != BANDERA and visible != BOMBA:
                if visible != str(tablero[i][j]):
                    return False

    return True

def estructura_y_tipos_validos(estado: EstadoJuego) -> bool:
    # Verificar que existan exactamente las 6 claves esperadas
    claves_esperadas: list[str] = ["tablero", "tablero_visible", "filas", "columnas", "minas", "juego_terminado"]
    for clave in claves_esperadas:
        if clave not in estado:
            return False
    if len(estado) != 6:
        return False

    # Verificar que filas, columnas y minas son enteros positivos y coherentes
    filas: int = estado["filas"]
    columnas: int = estado["columnas"]
    minas: int = estado["minas"]

    if filas <= 0 or filas // 1 != filas:
        return False
    if columnas <= 0 or columnas // 1 != columnas:
        return False
    if minas <= 0 or minas >= filas * columnas or minas // 1 != minas:
        return False

    # Verificar que juego_terminado sea un booleano (se rompe si usamos True==1 o False == 0)
    juego_terminado: Any = estado["juego_terminado"]
    if not (juego_terminado == True or juego_terminado == False):
        return False

    # Validar que tablero y tablero_visible son matrices válidas y con misma dimensión
    tablero: list[list[int]] = estado["tablero"]
    tablero_visible: list[list[str]] = estado["tablero_visible"]

    if not es_matriz(tablero):
        return False
    if not es_matriz(tablero_visible):
        return False
    if not son_matriz_y_misma_dimension(tablero, tablero_visible):
        return False

    # Validar que los valores del tablero estén entre -1 y 8
    for fila in tablero:
        for valor in fila:
            if valor < -1 or valor > 8:
                return False

    # Validar los valores del tablero_visible
    valores_validos: list[str] = [VACIO, BANDERA, BOMBA, "0", "1", "2", "3", "4", "5", "6", "7", "8"]
    for fila_visible in tablero_visible:
        for valor_visible in fila_visible:
            esta: bool = False
            for permitido in valores_validos:
                if valor_visible == permitido:
                    esta = True
            if not esta:
                return False

    return True

#Creamos la funcion son_matriz_y_misma_dimension
# Chequeamos que 2 matrices t1 y t2 tengan , la misma forma, misma cantidad de filas y la misma cantidad de columnas en todas sus dilas
# Utilizamos es_matriz del ejercicio 1
def son_matriz_y_misma_dimension(t1: list[list[Any]], t2: list[list[Any]]) -> bool:
    if not es_matriz(t1):
        return False
    if not es_matriz(t2):
        return False
    if len(t1) != len(t2):
        return False
    if len(t1) == 0:
        return True
    if len(t1[0]) != len(t2[0]):
        return False
    return True

def todas_celdas_seguras_descubiertas(tablero: list[list[int]], tablero_visible: list[list[str]]) -> bool:
   
   #Confirmamos que ambas matrices tienen la misma forma
    if not son_matriz_y_misma_dimension(tablero, tablero_visible):
        return False

    # Obtenemos la cantidad de filas y columnas , para calcular el tamaño de la matriz
    filas: int = len(tablero)
    columnas: int = len(tablero[0])

    # Recorremos todas las posiciones validas del tablero
    # Analizamos cada celda, si la celda del tablero no es una mina entonces:
    # tiene que estar descubierta en el tablero_visible con el numero correcto

    for i in range(filas):
        for j in range(columnas):
            valor_tablero: int = tablero[i][j]
            valor_visible: str = tablero_visible[i][j]

            if valor_tablero != -1:
                if not (valor_visible == str(valor_tablero)): #Tiene que coincidir para que este descubierta correctamente sino retorna False
                    return False

    return True


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
