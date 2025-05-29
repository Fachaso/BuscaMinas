# Ejercicio 2:
# Esta función modifica un tablero de Buscaminas, calculando cuántas minas (-1) hay alrededor de cada celda vacía (0).

def calcular_numeros(tablero: list[list[int]]) -> None:
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

# Ejemplo de uso:
"""
tablero = [
    [-1, -1, -1,0,0],
    [0,  0,0,-1, 0],
    [-1, 0,0,0, 0],
    [0,0,0,0,-1]
]

# Llamamos a la función para calcular los números en el tablero
calcular_numeros(tablero)

# Mostramos el tablero resultante
for fila in tablero:
    print(fila)
"""
#fin del ejemplo
