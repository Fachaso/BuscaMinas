import random
from typing import Any, TextIO
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
    tablero : list[list[int]] = crear_tablero_lleno_de_elem(filas, columnas, 0)
    minas_colocadas : int = 0
    while minas_colocadas < minas:
        fila : int = random.randint(0, filas -1)
        columna : int = random.randint(0, columnas-1)

        if tablero[fila][columna] == 0:      # en caso de que elija la misma posición, no suma a minas_colocadas hasta que elija una nueva posición
            tablero[fila][columna] = -1
            minas_colocadas += 1

    return tablero

def crear_tablero_lleno_de_elem(filas : int, columnas : int, elem : Any) -> list[list[int]]:
    """
    Crea un tablero de dimensión filas x columnas con elem en cada posicion
    """
    tablero_vacio : list[list[int]] = []  
    for _ in range(filas):
        fila : list[list[int]] = []
        for _ in range(columnas):
            fila.append(elem)
        tablero_vacio.append(fila)

    return tablero_vacio

def calcular_numeros(tablero: list[list[int]]) -> None:
    for i in range(len(tablero)):
        for j in range(len(tablero[0])):
            if tablero[i][j] != -1:
                tablero[i][j] = calcular_numero_por_posicion(tablero, i+1, j+1)     # como parámetro pasamos i+1 y j+1 porque la posicion (i,j) en el tablero original se corresponde con (i+1,j+1) en el tablero con borde

def calcular_numero_por_posicion(tablero : list[list[int]], fila : int, columna : int) -> int:
    """"
     A partir de un tablero no vacio, y una posicion (fila,columna) válida en el tablero,
    devuelve la cantidad de minas adyacentes a la posicion
    """
    tablero_con_borde : list[list[int]] = crear_tablero_con_borde(tablero)
    minas : int = 0
    if tablero_con_borde[fila + 1][columna] == -1:
        minas += 1
    if tablero_con_borde[fila - 1][columna] == -1:
        minas += 1
    if tablero_con_borde[fila][columna + 1] == -1:
        minas += 1
    if tablero_con_borde[fila][columna - 1] == -1:
        minas += 1
    if tablero_con_borde[fila + 1][columna + 1] == -1:
        minas += 1
    if tablero_con_borde[fila + 1][columna - 1] == -1:
        minas += 1
    if tablero_con_borde[fila - 1][columna + 1] == -1:
        minas += 1
    if tablero_con_borde[fila - 1][columna - 1] == -1:
        minas += 1
    return minas
 

def crear_tablero_con_borde(tablero_original : list[list[int]]) -> list[list[int]]:      
    """
    A partir de un tablero (con filas y columnas no nulas), devuelve el mismo tablero con "borde",
    es decir, agrega una fila al principio y al final y una columna al principio y al final,
    todas llenas con -2 (para evitar separar en casos cuando la posición esta en un extremo)
    """  
    filas : int = len(tablero_original) + 2
    columnas : int = len(tablero_original[0]) + 2
    tablero_con_borde : list[list[int]] = crear_tablero_lleno_de_elem(filas, columnas,0)
    for i in range(filas):
        for j in range(columnas):
            if i == 0 or j == 0 or i == filas -1 or j == columnas -1:
                tablero_con_borde[i][j] = -2
            else:
                tablero_con_borde[i][j] = tablero_original[i-1][j-1]    # es (i-1,j-1) porque la posicion (i,j) que no sea borde en el tablero con borde, representa la posicion (i-1,j-1) en el tablero original
    return tablero_con_borde


def crear_juego(filas:int, columnas:int, minas:int) -> EstadoJuego:
  tablero:list[list[int]] = colocar_minas(filas,columnas,minas)
  calcular_numeros(tablero)
  tablero_visible:list[list[str]]= crear_tablero_lleno_de_elem(filas, columnas, VACIO)
  estado: EstadoJuego = {'filas':filas,
                        'columnas': columnas,
                        'minas':minas,
                        'tablero':tablero,
                        'tablero_visible':tablero_visible,
                        'juego_terminado':False,}

  return estado

def todas_celdas_seguras_descubiertas(tablero:list[list[int]],tablero_visible:list[list[str]])->bool:
    for i in range(len(tablero)):
        for j in range (len(tablero[0])):
            res : bool = ((tablero[i][j]==-1)and(tablero_visible[i][j]==VACIO or tablero_visible[i][j]==BANDERA)) or ((tablero[i][j]!=-1)and (tablero_visible[i][j]==str(tablero[i][j])))
            if res == False:
                return res
    return True    


def obtener_estado_tablero_visible(estado : EstadoJuego) -> list[list[str]]:  
    copia_tablero_visible : list[list[str]] = estado['tablero_visible'].copy()
    return copia_tablero_visible

def marcar_celda(estado: EstadoJuego, fila: int, columna: int) -> None:
    tablero_visible:list[list[str]]= estado['tablero_visible']
    if not estado["juego_terminado"]:
        if tablero_visible[fila][columna] == VACIO:
            tablero_visible[fila][columna] = BANDERA
        elif tablero_visible[fila][columna] == BANDERA:
            tablero_visible[fila][columna] = VACIO
        
def descubrir_celda(estado: EstadoJuego, fila: int, columna: int) -> None:
    filas:int= estado['filas']
    columnas:int= estado ['columnas']   
    tablero_visible:list[list[str]]= estado['tablero_visible']
    tablero:list[list[int]]= estado['tablero']
    if not estado["juego_terminado"]:
        if tablero[fila][columna] == -1:
            estado['juego_terminado']= True
            for i in range(filas):
                for j in range (columnas):
                    if tablero[i][j]== -1:
                        tablero_visible[i][j]=BOMBA
        else:
            for x, y in caminos_descubiertos(tablero,fila,columna,[]):
                if tablero_visible[x][y] != BANDERA:
                    tablero_visible[x][y]=str(tablero[x][y])

            if (todas_celdas_seguras_descubiertas(tablero, tablero_visible)):
                estado['juego_terminado']=True
          
def caminos_descubiertos (tablero:list[list[int]],f:int,c:int,s:list[(int,int)]) -> list[(int,int)]:
    s.append((f,c))   #crea una lista de cordenadas con las funciones a descubrir
    res:list[(int,int)]=[]
    if tablero[f][c] == 0:         
        for x , y in buscar_adyacente(tablero,f,c):      #si no hay ninguna bomba al rededor busca sus adyacentes
            if tablero[x][y] == 0 and (x,y) not in s:    #si encuentra algun elemnto adyacente que sea 0 y no este en la lista hace recursion sobre esa coordenada
                s = caminos_descubiertos(tablero,x,y,s) 
            else:
                s.append((x,y))                          #sino la agrega a la lista
    for i in s:
        if i not in res:
            res.append(i)            # elimina los repetidos de la lista
    
    return res       
    
def buscar_adyacente (tablero:list[list[int]],f:int,c:int) -> list[(int,int)]:
    tablero_con_borde: list[list[int]] = crear_tablero_con_borde(tablero)   #crea un tablero coon borde para buscar los adyacentes de los bordes del tablero original
    coordenadas = [(f-1, c-1), (f-1, c),(f-1, c+1),(f, c+1),(f+1, c+1),(f+1, c),(f+1, c-1),(f, c-1),]
    posiciones_vecinas = []
    for fila , columna in coordenadas:
        if tablero_con_borde[fila+1][columna+1] > -1:  #busca los numeros vecinos que no sean bomba ni el borde, se suma uno a la fila y uno a la columna ya que se le agrega el borde
            posiciones_vecinas.append((fila, columna))
    
    return posiciones_vecinas

def verificar_victoria(estado: EstadoJuego) -> bool:
    res : bool = False
    if todas_celdas_seguras_descubiertas(estado['tablero'], estado['tablero_visible']):
        res = True
    return res

def reiniciar_juego(estado: EstadoJuego) -> None:
    minas = estado ['minas']
    filas= estado ['filas']
    columnas= estado['columnas']
    tablero_viejo=estado['tablero']
    tablero_nuevo=colocar_minas (filas,columnas,minas)#crea de nuevo los tableros
    while tableros_iguales (tablero_viejo,tablero_nuevo):
        tablero_nuevo = colocar_minas (filas,columnas,minas)
    calcular_numeros (tablero_nuevo)
    tablero_nuevo_visible= crear_tablero_lleno_de_elem(filas, columnas, VACIO)
    estado['tablero']=tablero_nuevo#deberia actualizar el estado 
    estado['tablero_visible']=tablero_nuevo_visible
    estado['juego_terminado']=False
    

def tableros_iguales(t1:list[list[int]],t2:list[list[int]]) -> bool: #verifica si dos tableros son iguales
    igual=True
    for i in range (len(t1)):
        for k in range (len(t1[0])):
            if t1[i][k] != t2[i][k]:  #chequea que los elementos de ambos  tableros sean diferentes
                igual=False
    return igual

def guardar_estado(estado: EstadoJuego, ruta_directorio: str) -> None:
    archivo_tablero : TextIO = open(os.path.join(ruta_directorio,"tablero.txt"), "w")
    archivo_tablero_visible : TextIO = open(os.path.join(ruta_directorio,"tablero_visible.txt"), "w")
    guardar_tablero(estado, archivo_tablero)
    guardar_tablero_visible(estado, archivo_tablero_visible)

def guardar_tablero(estado: EstadoJuego, archivo_tablero : str) -> None:
    """" Guarda un archivo con el estado del tablero"""
    tablero : list[list[int]] = estado["tablero"]
    for i in range(len(tablero)):
        for j in range(len(tablero[0])):
            archivo_tablero.write(str(tablero[i][j]))
            if not (j == len(tablero[0]) -1):               # En caso de que sea la ultima posicion no agrega coma
                archivo_tablero.write(",")
        archivo_tablero.write("\n")
    archivo_tablero.close()

def guardar_tablero_visible(estado: EstadoJuego, archivo_tablero : str) -> None:
    """" Guarda un archivo con el estado del tablero visible"""
    tablero : list[list[int]] = estado["tablero_visible"]
    for i in range(len(tablero)):
        for j in range(len(tablero[0])):

            if tablero[i][j] == VACIO:
                archivo_tablero.write("?")
            elif tablero[i][j] == BANDERA:
                archivo_tablero.write("*")
            else:
                archivo_tablero.write(str(tablero[i][j]))

            if not (j == len(tablero[0]) -1):               # En caso de que sea la ultima posicion no agrega coma
                archivo_tablero.write(",")
        archivo_tablero.write("\n")
    archivo_tablero.close()


def cargar_estado(estado: EstadoJuego, ruta_directorio: str) -> bool:
  if not  existe_archivo(ruta_directorio,'tablero.txt') or not existe_archivo(ruta_directorio, 'tablero_visible.txt'):
     return False
  else:
   archivo_tablero:TextIO=open(os.path.join(ruta_directorio,'tablero.txt'),'r')
   archivo_tablero_visible:TextIO= open(os.path.join(ruta_directorio,'tablero_visible.txt'),'r')

   lineas_tablero:list[str]= archivo_tablero.readlines()
   archivo_tablero.close()
   lineas_tablero_visible:list[str]= archivo_tablero_visible.readlines()
   archivo_tablero_visible.close()

  
   tablero:list[list[int]]= tablero_a_matriz(lineas_tablero)
   tablero_visible:list[list[str]]= tablero_visible_a_matriz(lineas_tablero_visible)
   minas:int= contar_minas(lineas_tablero)

   
   estado['filas']=  len(tablero)
   estado['columnas']= len(tablero[0])
   estado['minas']= minas
   estado['tablero']= tablero
   estado['tablero_visible']= tablero_visible
   estado['juego_terminado']= False
  
   return True

def tablero_a_matriz(lineas_tablero: list[str])->list[list[int]]: #Transforma el txt del tablero en una matriz en caso que la matriz del archivo sea valida
   tablero:list[list[int]]= []
   for i in range (len(lineas_tablero)):
       if len(lineas_tablero[i])>1:
          fila: list[int]=[]
          j= 0
          while j< len (lineas_tablero[i]):
              l: str= lineas_tablero [i][j]
              if l != "," and l !="\n":
                  if l == "-" and j+1 < len(lineas_tablero[i]) and lineas_tablero[i][j+1]=="1":
                      fila.append(-1)
                      j+=2 #es +2 porque si se suma 1 se suma el 1 que unimos al - recien
                  else: 
                      fila.append(int(l))
                      j +=1             
              else:
                  j += 1       
          tablero.append(fila)
   return tablero


def tablero_visible_a_matriz(lineas_tablero_visible:list[str])->list[list[str]]: #Transforma el txt del tablero visible en una matriz en caso que la matriz del archivo sea valida
   tablero_visible:list[list[str]]= []
   for i in range (len(lineas_tablero_visible)):
       if len(lineas_tablero_visible[i]) >1:
          fila:list[str]= []
          for j in range (len(lineas_tablero_visible[i])):
           l: str= lineas_tablero_visible [i][j]
           if l!= "," and l!= "\n":
              if l == "?":
                fila.append(VACIO)
              elif l== "*":
                fila.append(BANDERA)
              else:
                fila.append(l)
          tablero_visible.append(fila) 
   return tablero_visible

def contar_minas(lineas_tablero:list[str])->int: #Cuenta cantidad de minas en el txt en que caso de que la matriz del archivo sea valida
    minas:int= 0
    for i in range (len(lineas_tablero)):
        if len(lineas_tablero[i])>1:
            j=0
            while j<len(lineas_tablero[i]):
                l: str= lineas_tablero [i][j]
                if l != "," and l !="\n":
                  if l == "-" and j+1 < len(lineas_tablero[i]) and lineas_tablero[i][j+1]=="1":
                      minas +=1
                      j+=2 #es +2 porque si se suma 1 se suma el 1 que unimos al - recien
                  else: 
                      j +=1             
                else:
                  j += 1       
    return minas    

def tableros_compatibles(nombre_archivo_tablero_visible : str, nombre_archivo_tablero : str) -> bool:
    """Dado el archivo de tablero visible y de tablero, define si ambas matrices son válidas y si los tableros definidos
    por las matrices son válidos con respecto al otro"""
    archivo_tablero_visible : TextIO = open(nombre_archivo_tablero_visible, "r")
    archivo_tablero : TextIO = open(nombre_archivo_tablero, "r")
    lineas_tablero_visible : list[str] = quitar_saltos_de_lineas_al_final(archivo_tablero_visible.readlines())
    lineas_tablero : list[str] = quitar_menos_de_tablero(quitar_saltos_de_lineas_al_final(archivo_tablero.readlines()))

    if not es_matriz_valida(lineas_tablero_visible) or  not es_matriz_valida(lineas_tablero):
        return False
    
    if not es_valido_tablero(nombre_archivo_tablero):
        return False
    
    if not es_valido_tablero_visible(nombre_archivo_tablero_visible,nombre_archivo_tablero):
        return False

    archivo_tablero_visible.close()
    archivo_tablero.close()
    return True

def es_valido_tablero_visible(nombre_archivo_tablero_visible : str, nombre_archivo_tablero : str) -> bool:
    """Dado el archivo de tablero visible y el tablero, define si el tablero visible es válido con respecto al tablero,
      y si solo tiene caracteres válidos. Es decir, verifica que tengan las mismas dimensiones y se correspondan  """
    archivo_tablero_visible : TextIO = open(nombre_archivo_tablero_visible, "r")
    lineas_tablero_visible : list[str] = quitar_saltos_de_lineas_al_final(archivo_tablero_visible.readlines())
    archivo_tablero : TextIO = open(nombre_archivo_tablero, "r")
    lineas_tablero : list[str] = quitar_saltos_de_lineas_al_final(archivo_tablero.readlines())
    caracteres_validos : list[str] = ["0","1","2","3","4","5","6","7","8","*","?"]

    if not mismas_dimensiones(tablero_visible_a_matriz(lineas_tablero_visible), tablero_a_matriz(lineas_tablero)):
        return False

    for i in range(len(lineas_tablero_visible)):
        for j in range(len(lineas_tablero_visible[0])):
            if lineas_tablero_visible[i][j] != "," and not (lineas_tablero_visible[i][j] in caracteres_validos):
                return False
    
    if not tablero_visible_se_corresponde_con_tablero(tablero_visible_a_matriz(lineas_tablero_visible),tablero_a_matriz(lineas_tablero)):
        return False
    
    archivo_tablero.close()
    archivo_tablero_visible.close()
    return True

def mismas_dimensiones(tablero_visible : list[list[str]], tablero : list[list[int]]) -> bool:
    """Requiere que ambas tableros sean matrices válidas. Verifica que tiene las mismas columnas y filas"""
    if len(tablero_visible) != len(tablero) or len(tablero_visible[0]) != len(tablero[0]):
        return False
    return True

def tablero_visible_se_corresponde_con_tablero(tablero_visible : list[list[str]], tablero : list[list[int]]) -> bool:
    """Dado un tablero visible y un tablero, verifica que las posiciones en tablero visible que no sean vacio o bandera, 
    sean iguales a la posiciones en tablero"""
    
    for i in range(len(tablero_visible)):
        for j in range(len(tablero_visible[0])):
            if (tablero_visible[i][j])!= VACIO and (tablero_visible[i][j])!= BANDERA:
                if (tablero_visible[i][j]) !=str(tablero[i][j]):
                    return False
    return True

def es_valido_tablero(nombre_archivo : str) -> bool:
    """A partir de un nombre de archivo, donde hay una matriz válida (esto se asume), define si el tablero es válido, esto es, 
    si hay al menos un -1, si los caracteres son válidos, y los números están bien calculados"""
    archivo : TextIO = open(nombre_archivo, "r")
    lineas_con_menos : list[str] =  quitar_saltos_de_lineas_al_final(archivo.readlines())
    lineas_sin_menos : list[str] =  quitar_menos_de_tablero(lineas_con_menos)
    caracteres_validos : list[str] = ["0","1","2","3","4","5","6","7","8"]

    for i in range(len(lineas_sin_menos)):
        for j in range(len(lineas_sin_menos[0])):
            if lineas_sin_menos[i][j] != "," and not (lineas_sin_menos[i][j] in caracteres_validos):
                return False

    if contar_minas(lineas_con_menos) == 0:
        return False
    
    if not numeros_correctos(tablero_a_matriz(lineas_con_menos)):
        return False
    
    return True

def numeros_correctos(tablero : list[list[int]]) -> bool:
    """Dado un tablero, verifica si los cantidad de minas adyacentes a cada posición correponde con el numero
    que tiene la posición"""

    copia_tablero : list[list[int]] = crear_tablero_lleno_de_elem(len(tablero), len(tablero[0]), 0)                  
    
    for fila in range(len(tablero)):
        for columna in range(len(tablero[0])):
            copia_tablero[fila][columna] = tablero[fila][columna]

    calcular_numeros(tablero)    
    if tablero != copia_tablero:    
        return False
    
    return True

def es_matriz_valida(lineas : list[str]) -> bool:
    """Devuelve True si y solo si el archivo (identificado por una lista de sus lineas) representa una matriz válida, esto es, 
    si sus dimensiones son validas y las comas están bien posicionadas"""

    if not dimensiones_validas(lineas):
        return False
    
    for linea in lineas:
        if not comas_en_posicion_correcta(linea):     
            return False    
       
    return True

def comas_en_posicion_correcta(linea : str) -> bool:
    """Chequea que las comas en una linea del archivo de tablero visible estén en posiciones válidas"""
    if linea[len(linea) -1] == ",":
        return False
    
    for i in range(1, len(linea), 2):
        if linea[i] != ",":
            return False
    
    for i in range(0, len(linea), 2):
        if linea[i] == ",":
            return False
        
    return True

def dimensiones_validas(lineas : list[str]) -> bool:
    """Verificamos que las dimensiones de la matriz del archivo tablero_visible sean validas, es decir, que 
    las filas y columnas sean como mínimo 2, y que las columnas sean de igual longitud"""
    if len(lineas) < 2:
        return False
    
    if len(lineas[0]) < 2:
        return False
    
    for i in range(len(lineas)):
        if len(lineas[0]) != len(lineas[i]):
            return False
    return True

def quitar_saltos_de_lineas_al_final(lineas : list[str]) -> list[str]:
    """Recibe una lista con las lineas de cualquiera de los dos archivos y devuelve la misma lista sin los -\n- en cada linea"""
    lineas_sin_salto : list[str] = []
    for linea in lineas:
        lineas_sin_salto.append(quitar_saltos_de_una_linea_al_final(linea))

    return lineas_sin_salto

def quitar_saltos_de_una_linea_al_final(linea: str) -> str:
    """Recibe una linea de cualquiera de los dos archivos y devuelve la misma linea sin los -\n- """
    linea_sin_salto : str = ""
    for i in range(len(linea)):
        if not(i == len(linea) -1 and linea[i] == "\n"):
            linea_sin_salto += linea[i]

    return linea_sin_salto

def quitar_menos_de_tablero(lineas : list[str]) -> list[str]:
    """Recibe una lista con las lineas del archivo tablero.txt y devuelve la misma lista sin los "-" de los -1 en cada linea"""
    lineas_sin_menos : list[str] = []
    for linea in lineas:
        lineas_sin_menos.append(quitar_menos_de_linea(linea))

    return lineas_sin_menos

def quitar_menos_de_linea(linea: str) -> str:
    """Recibe una linea del archivo tablero.txt y devuelve la misma linea sin los "-" de los -1"""
    linea_sin_menos : str = ""
    for i in range(len(linea)):
        if not (linea[i] == "-"):
            linea_sin_menos += linea[i]

    return linea_sin_menos

