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

#Ejercicio 1:
#Verifica que t sea una matriz valida(no vacía y filas de igual longitud):
def es_matriz(t: list[list]) -> bool:
    """
    Verifica que t sea una matriz valida(no vacía y filas de igual longitud)

    Args:
        t (list[list]): Matriz bidimensional con minas 

    Returns:
        bool: Verdadero si es una matriz valida
              False si no es una matriz valida
    """
    #Verifica que no esta vacia
    if len(t) == 0 or len(t[0]) == 0:
        return False
    #Verifica que todas las filas tienen la misma cantidad de columnas
    cantidad_columnas: int = len(t[0])
    for fila in t:
        if len(fila) != cantidad_columnas:
            return False
    return True

def colocar_minas(filas:int, columnas: int, minas:int) -> list[list[int]]:
    """
    Genera una matriz de dimensiones filas x columnas con minas colocadas aleatoriamente
    Cada celda de la matriz es un entero (-1) que representa una mina y (0) que representa una celda vacia sin minas adyacentes
    La ubicacion de las minas se selecciona de forma aleatoria y uniforme usando random

    Args:
        filas(int): Cantidad de filas de la matriz debe ser mayor a 0
        columnas(int): Cantidad de columnas de la matriz debe ser mayor a 0
        minas(int): Cantidad total de minas a colocar debe ser mayor que 0 y menor que filas * columnas

    Returns:
        list[list[int]]: Matriz bidimensional con minas representadas como -1 y celdas vacias como 0
                         La matriz resultante cumple con las dimensiones validas
    """
#Crea una matriz llena de ceros 
    """  
    [[0,0,0],
    [0,0,0],
    [0,0,0]]
    """
    matriz_res: list[list[int]] = []

    for _ in range(filas):
        fila: list[int] = []
        for _ in range(columnas):
            fila.append(0)               #Agrego un 0 al final de la lista
        matriz_res.append(fila)          # Agrega la fila completa a la matriz

  
    if es_matriz(matriz_res): #Verifica que la matriz es valida
        #Generamos las posiciones poibles para la ubicacion de las minas
    
        posiciones: list[tuple[int, int]] = []
        for i in range(filas):
            for j in range(columnas):
                posiciones.append((i, j))

        #Elegimos las posiciones aleatorias para colocar las minas en la matriz
        posiciones_minas: list[tuple[int, int]] = random.sample(posiciones, minas)

        #colocar -1 en las posiciones seleccionadas para las minas
        for (i, j) in posiciones_minas:
            matriz_res[i][j] = -1

    return matriz_res

#Ejercicio 2:
#Esta función modifica un tablero de Buscaminas, calculando cuántas minas (-1) hay alrededor de cada celda vacía (0)
def calcular_numeros(tablero: list[list[int]]) -> None:
    """
    Se modifica las celdas vacias (0) asignandoles un valor y las minas (-1) no se modifican

    Args:
        tablero (list[list[int]]): Matriz del tablero con -1 como minas y 0 como celdas vacias

    Modify: 
        Se modifica el tablero en el lugar asignando en cada celda vacia (0) la cantidad de minas cercanas
    """
    """
    Primero debemos modificar directamente el tablero (inout), y no crear uno nuevo según la especificacion

El objetivo que vamos a hacer en cada celda que no es una mina (-1),es  reemplazar el 0 por la cantidad de minas adyacentes.

1) Vamos a medir la dimensión del tablero
	cantidad_filas y cantidad_columnas

2) Realizamos una copia del tablero original 
	Porque si lo modificamos mientras lo recorremos, vamos a pisar valores antes de analizarlos.
Esta copia solo la usamos para leer mientras escribimos en el original

3) Para cada celda tablero_original[fila][columna] que no sea mina, contar las minas que hay alrededor
Para eso hay que recorrer las 8 direcciones posibles. Lo mejor es usar una lista de desplazamientos 
	posiciones_vecinas

EJEMPLO:
supongamos que estamos en la celda (fila, columna) = (2,2)

arriba a la izquierda 
es la tupla (-1, -1) y corresponde a la celda (1,1)   
y usamos la formula: 

(fila + desplazamiento_fila , columna + desplazamiento_columna) = 2-1, 2-1

abajo derecha
es la tupla (1, 1) y corresponde a la celda (3, 3)
con la formula:

(fila + desplazamiento_fila , columna + desplazamiento_columna) = 2+1, 2+1

y asi con las demás posiciones.


4) Recorremos cada celda y contamos las minas vecinas
iteramos por cada índice de fila , desde 0 hasta cantidad_filas -1
y por cada fila recorremos todas las columnas, hasta recorrer todo el tablero

Luego con el primer if analizamos las celdas que no son minas (-1) no se deben tocar.

	
	-Recorremos todas las tuplas de las 8 direcciones posibles de 	posiciones_vecinas.

	-iniciamos el contador de Minas Adyacentes.	
	
	-calculamos la posición de la celda vecina con la formula:
	(fila + desplazamiento_fila, columna + desplazamiento_columna)
	
	- con el siguiente if verificamos que la celda esta dentro del tablero.
	
	-con el ultimo if , si la celda vecina es una mina, sumamos al contador.

Por ultimo reemplazamos el 0 de la celda por el numero de minas que tiene alrededor.
"""
    # Recorremos cada fila del tablero usando su índice i
    for i in range(len(tablero)):
        # Recorremos cada columna del tablero usando su índice j
        for j in range(len(tablero[0])):
            # Si encontramos una celda con valor 0 (sin mina)
            if tablero[i][j] == 0:
                # Inicializamos el contador de minas alrededor
                minas_cerca: int = 0
                # Recorremos las celdas vecinas (3x3 centrado en [i][j])
                for x in range(i - 1, i + 2):  # Filas vecinas
                    for y in range(j - 1, j + 2):  # Columnas vecinas
                        # Verificamos que las coordenadas estén dentro del tablero (evita errores en bordes)
                        if 0 <= x < len(tablero) and 0 <= y < len(tablero[0]):
                            # Si la celda vecina contiene una mina (-1), la contamos
                            if tablero[x][y] == -1:
                                minas_cerca += 1
                # Después de contar las minas vecinas, asignamos ese número a la celda original
                tablero[i][j] = minas_cerca

    # Las celdas con -1 (minas) no se modifican, ya que no entran al bloque que las cambia


#Empieza Ejercicio 3:
def crear_juego(filas:int, columnas:int, minas:int) -> EstadoJuego:
    """
    Crea un nuevo estado de juego con minas colocadas aleatoriamente por otras funciones como colocar_minas

    Args:
        filas(int): Numero de filas del tablero
        columnas(int): Numero de columnas del tablero
        minas(int): Cantidad de minas a colocar

    Returns:
        EstadoJuego(dict[str, Any]): Diccionario con el estado inicial del juego
    """
    """
    1) vamos a crear el tablero con colocar_minas
llamamos a la función colocar_minas,para tener el tablero con las minas colocadas.
     -1 en posiciones elegidas aleatoriamente cantidad_minas
       0 en el resto
Guardamos el tablero en la variable tablero_con_minas

 2) completar el tablero con números alrededor de las minas
con calcular_numeros(tablero_con_minas)
como calcular_numeros modifica la matriz directamente (inout), no hace falta reasignar nada.

Hasta ACA ya tenemos listo el tablero para incluirlo en el EstadoJuego.


3) crear tablero_visible
creamos tablero_visible,que es lo que ve el jugador al inicio, donde todo esta oculto, con casillas VACIAS.

Tenemos que crear una matriz del mismo tamaño que el tablero, donde cada celda tenga el valor VACIO = " "
	-creamos la matriz vacia que se va a llenar de espacios " "
	(Este es el tablero oculto el que se va mostrando de a poco durante el juego)
	- iteramos las filas y por cada fila agregamos columnas con celdas " "

Este tablero coincide en tamaño con el tablero_con_minas, lo cual va a ser fundamental para validaciones futuras (estado_valido, son_matriz_y_misma_dimension)

4) crear el diccionario estado con todas las claves
{CLAVE,VALOR ESPERADO}

{"tablero",la matriz con minas y numeros}
Es el tablero modificado por calcular_numeros, ya con minas (-1) y números.

{"tablero_visible", la matriz oculta llena de " "}
Es el tablero oculto que ve el jugador: todo " " (VACIO).

{"filas", Cantidad de filas}
{"columnas", Cantidad de columnas}
Cantidades exactas pasadas como parámetro a la función. las vamos a usar en muchas validaciones posteriores (estado_valido).

{"Minas", Cantidad total de minas}
Número total de minas puestas → debe coincidir con las minas colocadas realmente.

{"juego_terminado", Estado del juego inicial: False}
Al iniciar, siempre es False. Solo cambia si el jugador pierde o gana.


5) Devolver el estado
devolvemos el estado de todo lo que construimos
return estado
    """
    # Creamos el tablero con colocar_minas y lo guardamos en una variable
    tablero_con_minas: list[list[int]] = colocar_minas(filas, columnas, minas)
    
    #Completamos el tablero con numeros alrededor de las minas usando calcular_numeros()
    calcular_numeros(tablero_con_minas)

#HASTA ACA ya tenemos listo el tablero para incluirlo en el EstadoJuego

# Creamos tablero_visible , que es lo que ve el jugador al inicio, donde todo esta oculto. 
    tablero_visible: list[list[str]] = []
    # Crear el tablero visible lleno de VACIO
    for _ in range(filas):      # Por cada fila
        fila_visible: list[str] = []    # Creamos una lista vacía para la fila
        for _ in range(columnas):       # Por cada columna
            fila_visible.append(VACIO)  # Añadimos el símbolo VACIO a la fila, VACIO es " "
        tablero_visible.append(fila_visible)    # Añadimos la fila al tablero visible

# crear el diccionario estado con todas las claves
# {CLAVE,VALOR ESPERADO}
# Estado del juego
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
    """
    Verifica que el estado del juego sea valido
    Comprueba estructura,cantidad correcta de minas, numeracion del tablero,
    igualdad entre tablero y tablero_visible, y validez del estado final.

    Args:
        estado (EstadoJuego): Estado actual del juego

    Returns:
        bool: True si el estado es valido
              False si el estado no es valido
    """
    """
    1) El primer if verifica que el estado:
	-tiene todas las claves necesarias y cada valor su tipo correcto
	-es_matriz es valida y con el tamaño correcto
SI FALLA devuelve False 

2) Contamos las minas reales
recorremos todas las celdas del tablero, y contamos los lugares que contienen (-1) y verificamos que esa cantidad coincida exactamente con lo que dice estado["minas"]

3) Validamos que el tablero esta bien numerado
	-creamos una copia del tablero para no modificar el original
	-aplicamos calcular_numeros para ver los valores que deben estar
	-comparamos la copia con el tablero original, si no son iguales
	significa que los números del tablero no están bien calculados

4) Validar juego_terminado
	-Verifica si el jugador piso una mina
	-llama a todas_las_celdas_seguras_descubiertas para ver si todas las      	celdas SIN mina están descubiertas
	-Para que el juego termine  debe cumplirse al menos una de esas 	condiciones.
	-Si el juego no esta terminado , no debe cumplirse ninguna

5) Verificar si todas las banderas están bien puestas
	-Recorremos todas las celdas visibles
	-si hay una bandera colocada, estará en el mismo lugar que una mina(-1)
	
6) Los números visibles deben coincidir con el tablero convertido a string
	-recorremos todas las celdas vacias
	-Si la celda no es VACIO, BANDERA, BOMBA entonces debe ser un numero 	entre 0 y 8
	-Lo comparamos con str(tablero[i][j] y DEBEN COINCIDIR
    """
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
    """
    Verifica que el estado tenga la estructura esperada y tipos correctos
    Incluye validaciones de claves, dimensiones, tipos y valores permitidos en el tablero y el tablero visible

    Args:
        estado(EstadoJuego): Estado del juego

    Returns:
        bool: True si la estructura y tipos son validos
              False si es lo contrario
    """
    """
    1) verificamos que existen todas las claves esperadas(las 6) de estado

2) verificamos que sean números enteros positivos y que minas < filas x columnas

3) Validamos juego terminado
	-verificamos que juego_terminado sea True o False

4) Verificamos es_matriz y que tengan la misma dimensión
	-usamos las funciones auxiliares es_matriz() y 	son_matriz_y_misma_dimension()

5) Validamos los valores del tablero
	-recorremos la matriz y nos aseguramos que los valores esten en el rango 	de [-1. 8]

6) Validamos los valores de tablero_visible
	-comprobamos que cada valor en el tablero visible sea valido uno a uno 	con un bucle.
    """
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

    if not es_matriz(tablero) or not es_matriz(tablero_visible) or not son_matriz_y_misma_dimension(tablero, tablero_visible):
        return False
    """if not es_matriz(tablero_visible):
        return False
    if not son_matriz_y_misma_dimension(tablero, tablero_visible):
        return False"""

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
    """
    Verifica si dos matrices tienen la misma dimension y son validas

    Args:
        t1 (list[list[Any]]): Primera matriz
        t2 (list[list[Any]]): Segunda matriz

    Returns:
        bool: True si ambas matrices tienen igual forma y son validas
              False si no lo son
    """
    # Verifica que t1 sea matriz válida o t2 sea matriz válida 
    # o que ambas tengan la misma cantidad de filas
    # o que las filas tengan la misma longitud
    if not es_matriz(t1) or not es_matriz(t2) or len(t1) != len(t2) or len(t1[0]) != len(t2[0]):
        return False
    
    """if len(t1) == 0:
        return True"""
    
    return True

def todas_celdas_seguras_descubiertas(tablero: list[list[int]], tablero_visible: list[list[str]]) -> bool:
    """
    Verifica si todas las celdas sin minas han sido descubiertas correctamente

    Args:
        tablero (list[list[int]]): Matriz con minas y numeros
        tablero_visible (list[list[str]]): Matriz con lo que ve el jugador

    Returns:
        bool: True si todas las celdas seguras estan descubiertas
              False en caso de que sea lo contrario
    """
    """
    agrego todas_celdas_seguras_descubiertas

para cada posición de fila y columna (i, j) es True si alguna de estas opciones se cumple:
	-Hay una mina, no hace falta descubrirla
	-Esta oculta (" ") o marcada con una bandera (sirve pero no seria victoria)
	-cada posición esta descubierta y el numero coincide con el del tablero

En resumen la celda esata segura si es una mina o si esta descubierta con su valor correcto.

Creamos una función que recibe:
	- tablero : es la matriz real de numero y minas (-1, 0 a 8)
	- tablero_visible: la matriz que el jugador ve con (VACIO,"1",BANDERAS)
devuelve True si todas las celdas no tienen mina están descubiertas correctamente
False si hay alguna celda segura sin descubrir
    """
   
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
    # Si es mina (-1), en visible debe ser VACIO o BANDERA
            if valor_tablero == -1:
                if not (valor_visible == VACIO or valor_visible == BANDERA):
                    return False
            else:
                # Si no es mina, debe estar descubierto con su número en string
                if valor_visible != str(valor_tablero):
                    return False
                
    return True

#Ejercicio 4:
def obtener_estado_tablero_visible(estado: EstadoJuego) -> list[list[str]]:
    """
    Retorna una copia del tablero visible del estado de juego

    Returns:
        list[list[str]]: Copia del tablero visible actual
    """
    """
    Creamos una copia de tablero_visible, una nueva matriz con los mismos valores.

1) accedemos a la matriz que queremos copiar 
2) Creamos una nueva lista vacia
	-por cada fila en el tablero visible usamos .copy() para copiar la fila
	y la agregamos a la copia.


Solo se ejecuta si "estado" ya es valido, devuelve una copia de estado["tablero_visible"]

Porque creamos una copia y devolvemos directo estado["tablero_visible"]???
Porque si devolvemos el mismo objeto, alguien desde afuera podría modificarlo, y eso rompería el estado interno del juego.
    """
    tablero_visible: list[list[str]] = estado["tablero_visible"]
    copia: list[list[str]] = []

    for fila in tablero_visible:
        fila_copia: list[str] = fila.copy()
        copia.append(fila_copia)

    return copia

#Ejercicio 5:
def marcar_celda(estado: EstadoJuego, fila: int, columna: int) -> None:
    """
    Alterna entre marcar o desmarcar una celda con una bandera
    No hace nada si el juego termino o la celda ya fue descubierta

    Args:
        estado (EstadoJuego): Estado actual del juego
        fila (int): Fila
        columna (int): Columna 
    Modify:
        Modifica celdas visibles con BANDERA o VACIO
    """
    # No hacemos nada si el juego terminó o la celda ya está descubierta
    #Si el juego ya termino o la celda ya esta descubierta(no es ni VACIO ni BANDERA) entonces no se modifica el tablero visible.
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

#Ejercicio 6:
def descubrir_celda(estado: EstadoJuego, fila: int, columna: int) -> None:
    """
    Descubre una celda y si es segura se expande automaticamente las celdas vecina
    Si se descubre una mina el juego termina

    Args:
        estado (EstadoJuego): Estado actual del juego
        fila(int): Fila 
        columna(int): Columna 
    Modify:
        Modifica el estado del tablero visible y el estado del juego terminado
    """
    """
1) si el juego esta terminado , no se puede descubrir mas nada



2) mostramos la BOMBA y marcamos el juego como terminado


3) Si el jugador no piso una mina , o sea la celda era segura, se deben descubrir todas las celdas seguras.

4) Todas las celdas seguras conectadas deben descubrirse, o sea Se deben descubrir todos los caminos seguros a partir de esa celda.


5) las demás celdas no deben cambiar, no tocamos nada que este fuera de los caminos seguros conectados. Las celdas fuera de los caminos deben mantenerse igual.

6) El resto del estado no cambia , no modificamos nada mas.
    """
    # Si el juego termino, no se hace nada
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
                numero:int = estado["tablero"][fila_camino][columna_camino]
                estado["tablero_visible"][fila_camino][columna_camino] =str(numero)
    
    # Verificamos si todas las celdas seguras fueron descubiertas (¡victoria!)
    if todas_celdas_seguras_descubiertas(estado["tablero"], estado["tablero_visible"]):
        estado["juego_terminado"] = True



def caminos_descubiertos(tablero: list[list[int]], tablero_visible: list[list[str]], f: int, c: int) -> list[list[tuple[int, int]]]:
    """
    Devuelve los caminos de celdas que deben revelarse al descubrir una celda segura

    Args:
        tablero(list[list[int]]): Tablero del juego
        tablero_visible(list[list[str]]): Tablero visible para el jugador
        f(int): Fila 
        c(int): Columna 

    Returns:
        list[list[tuple[int, int]]]: Lista de caminos de celdas a descubrir
    """
    """
    Esta función va a permitir que descubrir celda funcione correctamente, 
    ya que determina que celdas deben ser reveladas automáticamente cuando el usuario descubre una celda con valor 0
f, c: Z son las coordenadas donde comienza la expansión .
: seq(seq(ZxZ)) devuelve una lista de caminos , cada camino son tuplas(i,j) que deben revelarse.
    """
    
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
#Ejercicio 7:
def verificar_victoria(estado: EstadoJuego) -> bool:
    """
    Verifica si el jugador gano osea que todas las celdas seguras estan descubiertas

    Args:
        estado (EstadoJuego): Estado del juego

    Returns:
        bool: True si se gano
              False si no gano
    """
    """
    El resultado de la función es True si y solo si TODAS las celdas sin minas han #sido descubiertas correctamente.
    """
    return todas_celdas_seguras_descubiertas(estado["tablero"], estado["tablero_visible"])

#Ejercicio 8:
def reiniciar_juego(estado: EstadoJuego) -> None:
    """
    Reinicia el juego manteniendo dimensiones y cantidad de minas ,pero con un nuevo tablero

    Args:
        estado (EstadoJuego): Estado del juego

    Modify:
        Modifica el estado (Estado del juego)
    """
    """
    Con esta función vamos a reiniciar el juego manteniendo las dimensiones(filas, columnas) , 
    la cantidad de minas, pero vamos a cambiar el tablero y reiniciamos tablero_visible y juego_terminado
    """
    
    # Vamos a recuperar los datos del estado manteniendo las dimensiones y cantidad de minas originales
    filas: int = estado["filas"]
    columnas: int = estado["columnas"]
    minas: int = estado["minas"]
    tablero_viejo: list[list[str]] = estado["tablero"]


    #Generamos un nuevo tablero con minas , agregando -1 donde hay minas y numeros del 0-8 en el resto.
    nuevo_tablero: list[list[int]] = colocar_minas(filas, columnas, minas)
    while(tablero_viejo == nuevo_tablero):
        nuevo_tablero = colocar_minas(filas, columnas, minas)
        calcular_numeros(nuevo_tablero)
    calcular_numeros(nuevo_tablero)

    # Generamos un tablero_visible VACIO, o sea lo llenamos con " " para que el jugador no vea nada aun 
    nuevo_tablero_visible: list[list[str]] = []
    for _ in range(filas):
        fila_visible: list[str] = []
        for _ in range(columnas):
            fila_visible.append(VACIO)
        nuevo_tablero_visible.append(fila_visible)

    #Asignamos nuevo estado, donde se actualiza todo el estado , menos las dimensiones y las minas

    estado["tablero"] = nuevo_tablero
    estado["tablero_visible"] = nuevo_tablero_visible
    estado["juego_terminado"] = False

#Ejercicio 9:
def guardar_estado(estado: EstadoJuego, ruta_directorio: str) -> None:
    """
    Guarda el estado actual del juego en archivos de texto 

    Args:
        estado (EstadoJuego): Estado del juego
        ruta_directorio(str): Directorio donde se guardan los archivos

    Modify:
        Crea o sobrescribe archivos
    """
    """
    Esta función guarda el estado actual del juego en dos archivos separados dentro del directorio xxxx para poder cargarlo mas tarde
	-tablero.txt : guarda el estado["tablero"] 
	separado por ; , cada fila es una linea
    """
    if estado["juego_terminado"]:
        return

    if not estado_valido(estado):
        return

    ruta_tablero: str = os.path.join(ruta_directorio, "tablero.txt")
    ruta_tablero_visible: str = os.path.join(ruta_directorio, "tablero_visible.txt")

# Generamos el contenido de tablero.txt
    contenido_tablero: list[str] = []

    for fila in estado["tablero"]:
        fila_str: str = ""
        for i in range(len(fila)):
            #Convertimos el entero en string y lo agregamos.
            fila_str += str(fila[i])
           #Agregamos un ; solo entre elementos, no al final de la fila.
            if i != len(fila) - 1:
                fila_str += ","
        #Agregamos la fila terminada a la lista.
        contenido_tablero.append(fila_str)

# Construimos una lista de strings donde cada uno es una linea del archivo tablero_visible.txt
    contenido_visible: list[str] = []

# Recorremos cada fila del tablero que es una matriz de strings
# Transformamos la BANDERA en * el espacio VACIO en ? y si es un numero queda igual
# Agregamos ; solo entre valores, no al final.
    for fila in estado["tablero_visible"]:
        fila_str: str = ""
        for i in range(len(fila)):
            celda: str = fila[i]
            if celda == BANDERA:
                fila_str += "*"
            elif celda == VACIO:
                fila_str += "?"
            else:
                fila_str += celda
            if i != len(fila) - 1:
                fila_str += ","
        contenido_visible.append(fila_str)

#Une correctamente la ruta del directorio con el nombre del archivo tablero.txt.
#Por ejemplo: si ruta_directorio = "./tppython", esto da ./tppython/tablero.txt.

    archivo_tablero: str = os.path.join(ruta_directorio, "tablero.txt")
    archivo_visible: str = os.path.join(ruta_directorio, "tablero_visible.txt")

# Abrimos el archivo para escritura y si no existe lo crea, agregamos salto de linea \n y cerramos los archivos 
    archivo1 = open(archivo_tablero, "w")
    for linea in contenido_tablero:
        archivo1.write(linea + "\n")
    archivo1.close()

# Abrimos el archivo, escribimos cada linea del archivo ya trasnformado y cerramos el archivo
    archivo2 = open(archivo_visible, "w")
    for linea in contenido_visible:
        archivo2.write(linea + "\n")
    archivo2.close()

#Ejercicio 10:
def cargar_estado(estado: EstadoJuego, ruta_directorio: str) -> bool:
        """
    Carga el estado del juego desde archivos del directorio dado

    Args:
        estado (EstadoJuego): Estado del juego 
        ruta_directorio(str): Directorio donde se guardan los archivos

    Returns:
        bool: True si se cargo correctamente
              False en caso de que se produzca un error
    """
    #Verificamos la existencia de los archivos tablero.txt y tablero_visible.txt
    
        if not existe_archivo(ruta_directorio, "tablero.txt"):
            return False
        if not existe_archivo(ruta_directorio, "tablero_visible.txt"):
            return False
#Leemos archivo tablero.txt y preparamos las variables
#para construir la ruta completa al archivo tablero.txt
#   -Abrimos el archivo , leemos todas sus lineas y las guardamos en lineas_tablero.
#   - Luego inicializamos todas las variables
        ruta_tablero = os.path.join(ruta_directorio, "tablero.txt")
        ruta_visible = os.path.join(ruta_directorio, "tablero_visible.txt")

        archivo_tablero = open(ruta_tablero, "r")
        lineas_tablero = archivo_tablero.readlines()
        archivo_tablero.close()

        tablero: list = []
        cantidad_minas: int = 0
        cantidad_filas: int = 0
        cantidad_columnas: int = -1

#    Procesamos cada linea del archivo tablero.txt
#    recorremos cada linea del archivo, si la linea tiene 1 o menos caracteres(por ejemplo, solo un \n) la salta, en resumen evitamos contar lineas vacias como filas del tablero.
        
        for linea_tablero in lineas_tablero:
            if len(linea_tablero) <= 1:
                continue

#convertimos la linea en numeros 
#recorremos la linea caracter por caracter, y armamos cada numero en numero_actual  y cada vez que aparece una (,) lo convertimos a entero y lo agregamos a la lista fila_numeros.
#           -Tambien contamos cuantas comas hay en esa linea
#           - y agregamos el ultimo numero que estaba en construccion
            fila_numeros: list = []
            numero_actual: str = ""
            cantidad_comas_en_fila: int = 0
            posicion = 0
            while posicion < len(linea_tablero):
                caracter = linea_tablero[posicion]
                if caracter == ",":
                    #if numero_actual == "":
                        #return False
                    fila_numeros.append(int(numero_actual))
                    numero_actual = ""
                    cantidad_comas_en_fila += 1
                elif caracter != "\n":
                    numero_actual += caracter
                posicion += 1
            if numero_actual != "":
                fila_numeros.append(int(numero_actual))

#Validamos las columnas y los valores numericos
#   Vamos a validar que estamos leyendo, como todavia no sabemos cuantas columnas tiene el tablero, por eso si la cantidad_columnas == -1, la calculamos como cantidad_columnas = cantidad_comas_en_fila + 1
#           con esto determinamos cuantas columnas va a tener todo el tablero.
#           Despues en todas las siguientes lineas , verificamos que tengan exactamente esa cantidad de columnas.
            
            if cantidad_columnas == -1:
                cantidad_columnas = cantidad_comas_en_fila + 1
            if cantidad_comas_en_fila != cantidad_columnas - 1:
                return False
            
            

#Validamos que todos los numeros esten entre -1 y 8 y contamos las minas
#Aca recorremos todos los valores numericos de esa fila (fila_numeros).
#Verificamos que cada valor este dentro del rango permitido:
#-PERMITIDO: -1 (mina), 0a8(cantidad de minas vecinas)
#-Sino devolvemos false
#-Si encuentra un -1 , suma 1 a la cantidad total de minas.

            indice = 0
            while indice < len(fila_numeros):
                valor_celda = fila_numeros[indice]
                if valor_celda < -1 or valor_celda > 8:
                    return False
                if valor_celda == -1:
                    cantidad_minas += 1
                indice += 1

#Agregamos la fila al tablero y aumentamos el contador de filas
#-agregamos la fila completa como una lista a la matriz tablero y aumentamos 1 el numero total de filas leidas.
            tablero.append(fila_numeros)
            cantidad_filas += 1

#Validacion general
#Sino se encontro ninguna fila valida o nunca se pudo contar/determinar la cantidad de columnas, el archivo no sirve y devuelve False.

        if cantidad_filas == 0 or cantidad_columnas == -1:
            return False
        
        #Valida de que hay al menos una mina
        if cantidad_minas == 0:
            return False

#Procesamos Tablero_visible.txt
#-Leemos todas las lineas del archivo y validamos la cantidad de filas y que tenga la misma cantidad de filas que tablero.txt

        archivo_visible = open(ruta_visible, "r")
        lineas_visible = archivo_visible.readlines()
        archivo_visible.close()

        if len(lineas_visible) != cantidad_filas:
            return False


#procesamos cada linea del archivo tablero_visible.txt
#-Recorremos caracter por caracter  y armamos cada simbolo (como "?", "1", "*") y lo guardamos en la fila visible.
#-Contamos las comas (,) para verificar la cantidad de columnas.
#y agregamos el ultimo valor que estaba en construccion.

        tablero_visible: list = []
        fila_index = 0
        while fila_index < cantidad_filas:
            linea_visible = lineas_visible[fila_index]
            fila_visible: list = []
            caracter_actual: str = ""
            cantidad_comas_en_visible = 0
            col_index = 0
            while col_index < len(linea_visible):
                caracter = linea_visible[col_index]
                if caracter == ",":
                    fila_visible.append(caracter_actual)
                    caracter_actual = ""
                    cantidad_comas_en_visible += 1
                elif caracter != "\n":
                    caracter_actual += caracter
                col_index += 1
            if caracter_actual != "":
                fila_visible.append(caracter_actual)


#Validamos la cantidad de columnas
#Nos aseguramos que cada fila en tablero_visible.txt tenga la misma cantidad de columnas que tablero.txt

            
            if len(fila_visible) != cantidad_columnas:
                return False

#VAlidamos caracteres y lo traducimos a valores internos.
#            -recorremos cada celda y validamos que contenga un simbolo permitido: (0a8, ? ,*...etc ) si hay otra cosa devuleve False.
#            -reemplaza * por BANDERA
#           -Reemplaza ? por VACIO
#           -Los numeros se dejan como estan en string

            
            indice_celda = 0
            while indice_celda < cantidad_columnas:
                simbolo = fila_visible[indice_celda]
                if simbolo not in ['*', '?', '.', '0', '1', '2', '3', '4', '5', '6', '7', '8']:
                    return False
                if simbolo == '*':
                    fila_visible[indice_celda] = BANDERA
                elif simbolo == '?':
                    fila_visible[indice_celda] = VACIO
                indice_celda += 1


#Agregamos la fila al tablero_visible
#La fila que ya esta procesada y traducida a la matriz tablero_visible

            tablero_visible.append(fila_visible)
            fila_index += 1

#Actualizamos el estado y devolvemos True
#Aca actualizamos el diccionario estado con todos los datos que se obtuvieron:
#-filas : es la cantidad de filas validas en tablero.txt
#-columnas: es la cantidad de columnas de la primera linea
#-minas: Total de -1 encontradas en tablero.txt
#-tablero: la matriz de enteros (con minas y numeros)
#-tablero_visible: las matriz de strings(visibles para el jugador)
#-Juego terminado: empieza con False poruqe al cargar un estado el juego no esta finalizado todavia.


        estado['filas'] = cantidad_filas
        estado['columnas'] = cantidad_columnas
        estado['minas'] = cantidad_minas
        estado['tablero'] = tablero
        estado['tablero_visible'] = tablero_visible
        estado['juego_terminado'] = False
#Si todo se proceso correctamente
        if not estado_valido(estado):
            return False
        
        return True