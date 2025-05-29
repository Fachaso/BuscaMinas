def crear_juego(filas:int, columnas:int, minas:int) -> EstadoJuego:
    # Crear el tablero con minas
    tablero: list[list[int]] = colocar_minas(filas, columnas, minas)

    # Calcular los números alrededor de las minas
    calcular_numeros(tablero)

    # Crear el tablero visible lleno de VACIO
    tablero_visible: list[list[int]] = [[VACIO for _ in range(columnas)] for _ in range(filas)]
    #Otra forma de hacer lo de arriba:
    """tablero_visible: list[list[int]] = []  # Lista vacía para el tablero visible

    for _ in range(filas):  # Por cada fila
        fila = []  # Creamos una lista vacía para la fila
        for _ in range(columnas):  # Por cada columna
            fila.append(VACIO)  # Añadimos el símbolo VACIO a la fila, VACIO es " "
        tablero_visible.append(fila)  # Añadimos la fila al tablero visible
    """

    # Estado del juego
    EstadoJuego = {
        "filas": filas,
        "columnas": columnas,
        "minas": minas,
        "tablero": tablero,
        "tablero_visible": tablero_visible,
        "juego_terminado": False
    }

    return EstadoJuego
#Ejemplo:
""" 
juego = crear_juego(6, 8, 10)

print("Tablero (con minas y números):")
for fila in juego["tablero"]:
    print(fila)

print("\nTablero visible (VACÍO):")
for fila in juego["tablero_visible"]:
    print(fila)"""
#Fin ejemplo

#Empieza Ejercicio 3:
def estructura_y_tipos_validos(estado: dict[str, object]) -> bool:
    filas: int = estado.get('filas')
    columnas: int = estado.get('columnas')
    minas: int = estado.get('minas')
    tablero: list[list[int]] = estado.get('tablero')
    tablero_visible: list[list[str]] = estado.get('tablero_visible')
    juego_terminado = estado.get('juego_terminado')

    # Validar filas, columnas y minas como enteros positivos y en rango
    if not (type(filas) is int and filas > 0):
        return False
    if not (type(columnas) is int and columnas > 0):
        return False
    if not (type(minas) is int and minas > 0 and minas < filas * columnas):
        return False

    # Validar juego_terminado como bool
    if juego_terminado is not True and juego_terminado is not False:
        return False

    # Validar tablero y tablero_visible son listas con la cantidad correcta de filas
    if not (type(tablero) is list and len(tablero) == filas):
        return False
    if not (type(tablero_visible) is list and len(tablero_visible) == filas):
        return False

    # Validar cada fila del tablero y tablero_visible
    for i in range(filas):
        if not (type(tablero[i]) is list and len(tablero[i]) == columnas):
            return False
        if not (type(tablero_visible[i]) is list and len(tablero_visible[i]) == columnas):
            return False

    # Validar valores en tablero entre -1 y 8
    for i in range(filas):
        for j in range(columnas):
            valor = tablero[i][j]
            if not (type(valor) is int and -1 <= valor <= 8):
                return False

    # Valores permitidos para tablero_visible
    valores_validos = [VACIO, BOMBA, BANDERA]

    # Validar valores en tablero_visible
    for i in range(filas):
        for j in range(columnas):
            valor_v = tablero_visible[i][j]
            if not (type(valor_v) is str):
                return False
            if valor_v in valores_validos:
                continue
            # Debe ser número entre '0' y '8' como string
            if len(valor_v) != 1:
                return False
            c = valor_v[0]
            if c < '0' or c > '8':
                return False

    return True


def estado_valido(estado: dict[str, object]) -> bool:
    if not estructura_y_tipos_validos(estado):
        return False

    filas: int = estado['filas']
    columnas: int = estado['columnas']
    minas: int = estado['minas']
    tablero: list[list[int]] = estado['tablero']
    tablero_visible: list[list[str]] = estado['tablero_visible']

    # Contar minas en tablero sin usar sum ni isinstance
    minas_contadas: int = 0
    for i in range(filas):
        for j in range(columnas):
            if tablero[i][j] == -1:
                minas_contadas += 1
    if minas_contadas != minas:
        return False

    # Crear tablero copia para calcular números
    tablero_copia: list[list[int]] = []
    for i in range(filas):
        fila_copia: list[int] = []
        for j in range(columnas):
            if tablero[i][j] == -1:
                fila_copia.append(-1)
            else:
                fila_copia.append(0)
        tablero_copia.append(fila_copia)

    calcular_numeros(tablero_copia)

    # Verificar que tablero coincide con el calculado
    for i in range(filas):
        for j in range(columnas):
            if tablero[i][j] != tablero_copia[i][j]:
                return False

    # Validar que tablero_visible concuerde con tablero
    for i in range(filas):
        for j in range(columnas):
            celda_v: str = tablero_visible[i][j]
            celda_r: int = tablero[i][j]

            if celda_v == BOMBA:
                if celda_r != -1:
                    return False
            elif celda_v != VACIO and celda_v != BANDERA:
                if celda_v != str(celda_r):
                    return False

    return True


"""def es_matriz(t: List[List[int]]) -> bool:
    # Verifica que t no esté vacía y todas las filas tengan la misma longitud
    if t == []:
        return False
    largo_fila = len(t[0])
    for fila in t:
        if len(fila) != largo_fila:
            return False
    return True
"""
def son_matriz_y_misma_dimension(t1: list[list[int]], t2: list[list[str]]) -> bool:
    # Verifica que t1 sea matriz válida
    if not es_matriz(t1):
        return False
    # Verifica que t2 sea matriz válida
    if not es_matriz(t2):
        return False
    # Verifica que ambas tengan la misma cantidad de filas
    if len(t1) != len(t2):
        return False
    # Verifica que las filas correspondientes tengan la misma longitud
    for i in range(len(t1)):
        if len(t1[i]) != len(t2[i]):
            return False
    return True

def todas_celdas_seguras_descubiertas(tablero: list[list[int]], tablero_visible: list[list[str]]) -> bool:
    # Primero verificamos que son matrices de la misma dimensión
    if not son_matriz_y_misma_dimension(tablero, tablero_visible):
        return False

    filas = len(tablero)
    columnas = len(tablero[0])

    for i in range(filas):
        for j in range(columnas):
            valor_tablero = tablero[i][j]
            valor_visible = tablero_visible[i][j]

            # Si es mina (-1), en visible debe ser VACIO o BANDERA
            if valor_tablero == -1:
                if not (valor_visible == VACIO or valor_visible == BANDERA):
                    return False
            else:
                # Si no es mina, debe estar descubierto con su número en string
                if valor_visible != str(valor_tablero):
                    return False
    return True
#Ejemplos
"""
# Ejemplo matrices válidas y no válidas
tablero_valido = [
    [-1, 1, 0],
    [1, 1, 0],
    [0, 0, 0]
]

tablero_visible_valido = [
    [VACIO, VACIO, VACIO],
    [VACIO, VACIO, VACIO],
    [VACIO, VACIO, VACIO]
]

tablero_visible_descubierto = [
    [VACIO, VACIO, VACIO],
    [VACIO, VACIO, VACIO],
    ["0", "0", "0"]
]

tablero_visible_invalido = [
    [VACIO, VACIO, VACIO],
    [VACIO, "X", VACIO],  # "X" no es válido
    [VACIO, VACIO, VACIO]
]

tablero_no_matriz = [
    [-1, 1],
    [1, 1, 0]  # fila con distinta longitud
]

tablero_visible_diferente_dim = [
    [VACIO, VACIO],
    [VACIO, VACIO]
]

print("son_matriz_y_misma_dimension(tablero_valido, tablero_visible_valido):", 
      son_matriz_y_misma_dimension(tablero_valido, tablero_visible_valido))  # Esperado: True

print("son_matriz_y_misma_dimension(tablero_no_matriz, tablero_visible_valido):", 
      son_matriz_y_misma_dimension(tablero_no_matriz, tablero_visible_valido))  # Esperado: False

print("son_matriz_y_misma_dimension(tablero_valido, tablero_visible_diferente_dim):", 
      son_matriz_y_misma_dimension(tablero_valido, tablero_visible_diferente_dim))  # Esperado: False

print("todas_celdas_seguras_descubiertas(tablero_valido, tablero_visible_valido):", 
      todas_celdas_seguras_descubiertas(tablero_valido, tablero_visible_valido))  # Esperado: True

print("todas_celdas_seguras_descubiertas(tablero_valido, tablero_visible_descubierto):", 
      todas_celdas_seguras_descubiertas(tablero_valido, tablero_visible_descubierto))  # Esperado: False (hay minas no descubiertas)

print("todas_celdas_seguras_descubiertas(tablero_valido, tablero_visible_invalido):", 
      todas_celdas_seguras_descubiertas(tablero_valido, tablero_visible_invalido))  # Esperado: False (valor inválido)
"""
#Fin Ejemplos
#Fin Ejercicio 3
