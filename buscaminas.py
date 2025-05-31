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
    tablero_visible: list[list[str]] = estado["tablero_visible"]
    copia: list[list[str]] = []

    for fila in tablero_visible:
        fila_copia: list[str] = fila.copy()
        copia.append(fila_copia)

    return copia


def marcar_celda(estado: EstadoJuego, fila: int, columna: int) -> None:
    # No hacemos nada si el juego terminó o la celda ya está descubierta
    #Si el juergo ya termino o la celda ya esta descubierta(no es ni VACIO ni BANDERA) entonces no se modifica el tablero visible.
	        #-Si el juego termino no se puede modificar mas el tablero
	        #-Si la celda ya fue descubierta no la podemos marcar***
    
    if estado["juego_terminado"]:
        return

    celda_visible: str = estado["tablero_visible"][fila][columna]

    if celda_visible != VACIO and celda_visible != BANDERA:
        return

    # Si está VACIO, colocamos una bandera
    if celda_visible == VACIO:
        estado["tablero_visible"][fila][columna] = BANDERA
    else:
        # Si tenia BANDERA, la desmarcamos (volvemos a VACIO)
        estado["tablero_visible"][fila][columna] = VACIO


def descubrir_celda(estado: EstadoJuego, fila: int, columna: int) -> None:
    # Si el juego terminó, no se hace nada
    if estado["juego_terminado"]:
        return

    # Si hay una mina, se muestra la bomba y se termina el juego
    if estado["tablero"][fila][columna] == -1:
        estado["tablero_visible"][fila][columna] = BOMBA
        estado["juego_terminado"] = True
        return

    # Si no hay una mina, se deben descubrir los caminos seguros
    caminos: list[list[tuple[int, int]]] = caminos_descubiertos(
        estado["tablero"], estado["tablero_visible"], fila, columna
    )

    for camino in caminos:
        for fila_camino, columna_camino in camino:
            if estado["tablero_visible"][fila_camino][columna_camino] != BANDERA:
                numero: int = estado["tablero"][fila_camino][columna_camino]
                estado["tablero_visible"][fila_camino][columna_camino] = str(numero)


def caminos_descubiertos(tablero: list[list[int]], tablero_visible: list[list[str]], f: int, c: int) -> list[list[tuple[int, int]]]:
    
    #Creamos la lista de caminos y guardamos las dimensiones
    caminos: list[list[tuple[int, int]]] = []

    cantidad_filas: int = len(tablero)
    cantidad_columnas: int = len(tablero[0])

    #Si se hace clic en una celda que no es 0, se devuelve solo esa celda como unico camino.
    #Ejemplo si el jugador hace click en una celda que tiene un numero mayor a 0, por ejemplo 2, NO hay expansion
        #en ese caso solo se muestra esa celda, no hay celdas vecinas para descubrir automaticamente
    if tablero[f][c] > 0:
        return [[(f, c)]] #por eso delvovemos una lista que contiene un solo camino con una unica posicion

    #Creamos variables auxiliares para no repetir celdas, y con frontera  hcemos una lista  de celdas a procesar
    #frontera son celdas que estan al borde de ser exploradas.
     
    posiciones_visitadas: list[tuple[int, int]] = []
    frontera: list[tuple[int, int]] = [(f, c)] # Comenzamos la expansion desde esta celda

    #Las 8 direcciones posibles alrededor de cada celda
    #Sirve para poder recorrer alrededor de una celda y chequear cada vecino que se puede descubrir
    posiciones_vecinas: list[tuple[int, int]] = [
        (-1, -1), (-1, 0), (-1, 1),
        ( 0, -1),          ( 0, 1),
        ( 1, -1), ( 1, 0), ( 1, 1)
    ]

    # Mientras haya posisciones por explorar, seguimos descubriendo/expandiendo
    #Vamos a explorar en cada vuelta a los vecinos, y luego a los vecinos de los vecinos y asi sucesivamente ...
    while len(frontera) > 0:
        actual: tuple[int, int] = frontera.pop()
        fila_actual: int = actual[0]
        columna_actual: int = actual[1]

    # No repetimos ni pisamos banderas, continuamos al siguiente ciclo del while si se cumple:
    # pasamos directamente a la siguiente en frontera
        if actual in posiciones_visitadas:
            continue

        if tablero_visible[fila_actual][columna_actual] == BANDERA:
            continue

        # Agregar la celda actual  al camino
        camino_actual: list[tuple[int, int]] = [(fila_actual, columna_actual)]
        posiciones_visitadas.append(actual)

        #Si tiene valor 0 la celda descubierta, agregamos sus vecinos seguros a la frontera para seguir expandiendo

        if tablero[fila_actual][columna_actual] == 0:
            for desplazamiento_fila, desplazamiento_columna in posiciones_vecinas:
                fila_vecina: int = fila_actual + desplazamiento_fila
                columna_vecina: int = columna_actual + desplazamiento_columna

                if 0 <= fila_vecina < cantidad_filas and 0 <= columna_vecina < cantidad_columnas:
                    if (fila_vecina, columna_vecina) not in posiciones_visitadas and (fila_vecina, columna_vecina) not in frontera:
                        if tablero[fila_vecina][columna_vecina] != -1:
                            frontera.append((fila_vecina, columna_vecina))

        #Agregamos camino a la lista de caminos, o sea que cada celda que recorrimos forma parte de su propio camino
        # que va a ser procesado por descubrir_celda
        caminos.append(camino_actual)

    return caminos

#El resultado de la función es True si y solo si TODAS las celdas sin minas han #sido descubiertas correctamente.

#O sea ganamos si todas las celdas que no tienen minas están visibles con su #numero correcto . 
	#-Verificamos para cada celda(i, j) si en el tablero hay un numero (0a8)
	#-no puede haber VACIO, BANDERA, ni errores en celdas seguras.
    #Ejemplo con Victoria
#    tablero = [
#  [-1, 1],
#  [ 1, 1]
#]

#tablero_visible = [
#  [" ", "1"],
#  ["1", "1"]
#]
def verificar_victoria(estado: EstadoJuego) -> bool:
    return todas_celdas_seguras_descubiertas(estado["tablero"], estado["tablero_visible"])


def reiniciar_juego(estado: EstadoJuego) -> None:
    return


def guardar_estado(estado: EstadoJuego, ruta_directorio: str) -> None:
    return


def cargar_estado(estado: EstadoJuego, ruta_directorio: str) -> bool:
    return False
