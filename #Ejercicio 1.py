#Ejercicio 1:
#Verifica que t sea una matriz valida(no vacía y filas de igual longitud):
def es_matriz(t:list[list[int]])->bool:
    
    #Verifica que no esta vacia
    if t == []:
        return False

    #Verifica que todas las filas tienen la misma cantidad de columnas
    largo_fila = len(t[0])

    for fila in t:
        if len(fila) != largo_fila:
            return False

    return True

def colocar_minas(filas:int, columnas: int, minas:int) -> list[list[int]]:
    #Crea una matriz llena de ceros 
    """  
    [[0,0,0],
    [0,0,0],
    [0,0,0]]
    """
    matriz: list[list[int]] = []

    for _ in range(filas):
        fila: list[int] = []
        for _ in range(columnas):
            fila.append(0)                  #Agrego un 0 al final de la lista
        matriz.append(fila)                 # Agrega la fila completa a la matriz

    if es_matriz(matriz): #Verifica que la matriz es valida
        #Eligo posiciones aleatorias para las minas
        cantidad_celdas = filas * columnas
        secuencia:list[int]= range(cantidad_celdas)#Rango entre [0,cant_celdas]
        posiciones_minas:list[int] = random.sample(secuencia, minas)#Devuelve una lista con la cantidad de minas al azar 
        
        #Colocamos -1 en las posiciones de las minas
        """Ejemplo de posiciones:
        [ [ 0, 1, 2, 3 ],
        [ 4, 5, 6, 7 ],
        [ 8, 9,10,11 ] ]
        """
        for pos in posiciones_minas:
            i = pos // columnas  # Fila
            j = pos % columnas   # Columna
            matriz[i][j] = -1    # Coloca la mina

        return matriz
#print(colocar_minas(3,4,3))
