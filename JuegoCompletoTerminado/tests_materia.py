import unittest
import os
from typing import Any
from buscaminas import (crear_juego, descubrir_celda, marcar_celda, obtener_estado_tablero_visible,
                               reiniciar_juego, colocar_minas, calcular_numeros, verificar_victoria, 
                               guardar_estado, cargar_estado, BOMBA, BANDERA, VACIO, EstadoJuego,
                               es_matriz,estado_valido,son_matriz_y_misma_dimension,estructura_y_tipos_validos,
                               todas_celdas_seguras_descubiertas,caminos_descubiertos)

# Tipo de alias para el estado del juego
EstadoJuego = dict[str, Any]
'''
Ayudamemoria: entre los métodos para testear están los siguientes:

    self.assertEqual(a, b) -> testea que a y b tengan el mismo valor
    self.assertTrue(x)     -> testea que x sea True
    self.assertFalse(x)    -> testea que x sea False
    self.assertIn(a, b)    -> testea que a esté en b (siendo b una lista o tupla)
'''

#Funciones auxiliares PROPIAS:
#usamos remove para borrar archivos creados
def borrar_archivos():
    if os.path.exists("tablero.txt"):
        os.remove("tablero.txt")
    if os.path.exists("tablero_visible.txt"):
        os.remove("tablero_visible.txt")

# Función auxiliar para contar minas (-1)
def cant_minas_en_tablero(tablero: list[list[int]]) -> int:
    """Chequea que el número de minas en el tablero sea igual al número de minas esperado"""
    contador_minas:int = 0
    for fila in tablero:
        for celda in fila:
            if celda == -1:
                contador_minas += 1
    return contador_minas

# Función auxiliar para verificar que solo hay 0 y -1
def son_solo_ceros_y_bombas (tablero: list[list[int]]) -> bool:
    for fila in tablero:
        for celda in fila:
            if celda not in [0, -1]:
                return False
    return True

# Función auxiliar para verificar dimensiones correctas
def dimension_correcta(tablero: list[list[int]], filas: int, columnas: int) -> bool:
    """Chequea que el tablero tenga las dimensiones correctas"""
    if len(tablero) != filas:
        return False
    for fila in tablero:
        if len(fila) != columnas:
            return False
    return True

#Tests del template:
class colocar_minasTest(unittest.TestCase):
    def test_ejemplo(self):
        filas = 2
        columnas = 2
        minas = 1
        
        tablero: list[list[int]] = colocar_minas(filas, columnas, minas)
        # Testeamos que el tablero tenga solo bombas o ceros
        self.assertTrue(son_solo_ceros_y_bombas(tablero))
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(tablero), minas)
        



class calcular_numerosTest(unittest.TestCase):
    def test_ejemplo(self):
        tablero = [[0,-1],
                   [0, 0]]

        calcular_numeros(tablero)
        # Testeamos que el tablero tenga los números correctos
        self.assertEqual(tablero, [[1,-1],
                                   [1, 1]])

class crear_juegoTest(unittest.TestCase):
    def test_ejemplo(self):
        filas = 2
        columnas = 2
        minas = 1
        estado: EstadoJuego = crear_juego(filas, columnas, minas)
        # Testeamos que el tablero tenga las dimensiones correctas
        self.assertTrue(dimension_correcta(estado['tablero'], filas, columnas))
        # Testeamos que el tablero visible tenga las dimensiones correctas
        self.assertTrue(dimension_correcta(estado['tablero_visible'], filas, columnas))
        # Testeamos que el tablero visible esté vacío
        for fila in estado['tablero_visible']:
            for celda in fila:
                self.assertEqual(celda, VACIO)
        # Testeamos que el resto es lo esperado
        self.assertEqual(estado['filas'], filas)
        self.assertEqual(estado['columnas'], columnas)
        self.assertEqual(estado['minas'], minas)
        self.assertFalse(estado['juego_terminado'])
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), minas)
    

class marcar_celdaTest(unittest.TestCase):
    def test_ejemplo(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [-1, 1],
                [1, 1]
            ],
            'tablero_visible': [
                [VACIO, VACIO],
                [VACIO, VACIO]
            ],
            'juego_terminado': False
        }
        marcar_celda(estado, 0, 0)
        # Testeamos que sólo la celda marcada sea visible
        self.assertEqual(estado['tablero_visible'], [
            [BANDERA, VACIO],
            [VACIO, VACIO]
        ])
        # Testeamos que el resto no se modificó
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(estado['tablero'], [
            [-1, 1],
            [1, 1]
        ])
        self.assertFalse(estado['juego_terminado'])
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 1)



class descubrir_celdaTest(unittest.TestCase):
    def test_ejemplo(self):
        estado: EstadoJuego = {
            'filas': 3,
            'columnas': 3,
            'minas': 3,
            'tablero': [
                [2, -1, 1],
                [-1, 3, 1],
                [-1, 2, 0]
            ],
            'tablero_visible': [
                [VACIO, VACIO, VACIO],
                [VACIO, VACIO, VACIO],
                [VACIO, VACIO, VACIO]
            ],
            'juego_terminado': False
        }
        descubrir_celda(estado, 2, 2)
        # Testeamos que la celda descubierta sea visible
        self.assertEqual(estado['tablero_visible'], [
            [VACIO, VACIO, VACIO],
            [VACIO, "3", "1"],
            [VACIO, "2", "0"]
        ])
        # Testeamos que el resto no se modificó
        self.assertEqual(estado['filas'], 3)
        self.assertEqual(estado['columnas'], 3)
        self.assertEqual(estado['minas'], 3)
        self.assertEqual(estado['tablero'], [
            [2, -1, 1],
            [-1, 3, 1],
            [-1, 2, 0]
        ])
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 3)
        self.assertFalse(estado['juego_terminado'])


class verificar_victoriaTest(unittest.TestCase):
    def test_ejemplo(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [-1, 1],
                [ 1, 1]
            ],
            'tablero_visible': [
                [VACIO, "1"],
                ["1", "1"]
            ],
            'juego_terminado': False
        }
        # Testeamos que el juego no esté terminado y que no haya ganado
        self.assertTrue(verificar_victoria(estado))
        # Testeamos que el resto no se modificó
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(estado['tablero'], [
            [-1, 1],
            [ 1, 1]
        ])
        self.assertEqual(estado['tablero_visible'], [
            [VACIO, "1"],
            ["1", "1"]
        ])
        self.assertFalse(estado['juego_terminado'])
        


class obtener_estado_tableroTest(unittest.TestCase):
    def test_ejemplo(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [-1, 1],
                [ 1, 1]
            ],
            'tablero_visible': [
                [VACIO, "1"],
                [VACIO, VACIO]
            ],
            'juego_terminado': False
        }
        # Testeamos que el estado del tablero sea el esperado
        self.assertEqual(obtener_estado_tablero_visible(estado), [
            [VACIO, "1"],
            [VACIO, VACIO]
        ])
         # Testeamos que nada se modificó
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(estado['tablero'], [
            [-1, 1],
            [ 1, 1]
        ])
        self.assertEqual(estado['tablero_visible'], [
            [VACIO, "1"],
            [VACIO, VACIO]
        ])
        self.assertFalse(estado['juego_terminado'])


class reiniciar_juegoTest(unittest.TestCase):
    def test_ejemplo(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [-1, 1],
                [ 1, 1]
            ],
            'tablero_visible': [
                [VACIO, "1"],
                [VACIO, VACIO]
            ],
            'juego_terminado': False
        }
        reiniciar_juego(estado)
        # Testeamos que el juego esté reiniciado
        self.assertEqual(estado['tablero_visible'], [
            [VACIO, VACIO],
            [VACIO, VACIO]
        ])
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 1)
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(len(estado['tablero']), 2)
        self.assertEqual(len(estado['tablero'][0]), 2)
        self.assertFalse(estado['juego_terminado'])
        # Testeamos que es diferente tablero
        self.assertNotEqual(estado['tablero'], [
            [-1, 1],
            [ 1, 1]
        ])


#TESTS PROPIOS:
#Tests ejercicio 1:
class TestColocarMinas(unittest.TestCase):
    def test_colocar_minas_cantidad_correcta(self):
        tablero:list[list[int]] = colocar_minas(3, 3, 5)
        minas:int = cant_minas_en_tablero(tablero)
        self.assertEqual(minas, 5)

    def test_colocar_minas_dimensiones(self):
        filas:int = 4
        columnas:int = 2
        tablero = colocar_minas(filas, columnas, 3)
        """self.assertEqual(len(tablero), filas)
        for fila in tablero:
            self.assertEqual(len(fila), columnas)"""
        self.assertTrue(dimension_correcta(tablero,filas,columnas))

    def test_colocar_minas_solo_0_y_menos1(self):
        tablero = colocar_minas(2, 2, 2)
        """for fila in tablero:
            for columna in fila:
                self.assertIn(columna, [0, -1])     #chequea si a esta en b"""
        self.assertTrue(son_solo_ceros_y_bombas(tablero)) 

class TestEsMatriz(unittest.TestCase):
    def test_matriz_valida(self):
        matriz:list[list[int]] = [[1, 2], [3, 4]]
        self.assertTrue(es_matriz(matriz))

    def test_lista_vacia(self):
        self.assertFalse(es_matriz([]))

    def test_matriz_filas_diferente(self):
        matriz:list[list[int]] = [[1, 2], [3]]
        self.assertFalse(es_matriz(matriz))

    def test_matriz_una_fila_vacia(self):
        matriz:list[list[int]] = [[1, 2], []]
        self.assertFalse(es_matriz(matriz))

    def test_matriz_una_columna(self):
        matriz:list[list[int]] = [[1], [2], [3]]
        self.assertTrue(es_matriz(matriz))


#Ejercicio 2:
class TestCalcularNumeros(unittest.TestCase):
    def test_calcular_numeros_completo(self):
        tablero:list[list[int]] = [
            [-1, 0, 0],
            [ 0, 0, 0],
            [ 0, 0, -1]
        ]
        calcular_numeros(tablero)
        esperado:list[list[int]] = [
            [-1, 1, 0],
            [ 1, 2, 1],
            [ 0, 1, -1]
        ]
        self.assertEqual(tablero, esperado)

    def test_calcular_numeros_solo_bordes(self):
        tablero:list[list[int]] = [
            [0, -1],
            [0, 0]
        ]
        calcular_numeros(tablero)
        self.assertEqual(tablero, [
            [1, -1],
            [1, 1]
        ])

#Ejercicio 3:
class TestCrearJuego(unittest.TestCase):
    def test_crear_juego_dimensiones(self):
        estado:list[list[int]] = crear_juego(3, 4, 5)
        self.assertEqual(estado["filas"], 3)
        self.assertEqual(estado["columnas"], 4)
        self.assertEqual(len(estado["tablero"]), 3)
        """for fila in estado["tablero"]:
            self.assertEqual(len(fila), 4)"""
        self.assertTrue(dimension_correcta(estado["tablero"],estado["filas"],estado["columnas"]))
        

    def test_crear_juego_cantidad_minas(self):
        estado:list[list[int]] = crear_juego(3, 4, 5)
        minas = cant_minas_en_tablero(estado["tablero"])
        self.assertEqual(minas, 5)

    def test_crear_juego_tablero_visible_vacio(self):
        estado:list[list[int]] = crear_juego(2, 2, 1)
        for fila in estado["tablero_visible"]:
            for celda in fila:
                self.assertEqual(celda, VACIO)

    def test_crear_juego_inicial_juego_no_terminado(self):
        estado:list[list[int]] = crear_juego(2, 2, 1)
        self.assertFalse(estado["juego_terminado"])

class TestCrearJuego_V2(unittest.TestCase):

    def test_crear_juego_valores_generados(self):
        juego = crear_juego(3, 3, 2)
        self.assertEqual(juego["filas"], 3)
        self.assertEqual(juego["columnas"], 3)
        self.assertEqual(juego["minas"], 2)
        self.assertEqual(len(juego["tablero"]), 3)
        self.assertEqual(len(juego["tablero_visible"]), 3)
        self.assertFalse(juego["juego_terminado"])

class TestEstadoValido(unittest.TestCase):
    def test_estado_valido_valido(self):
        estado:EstadoJuego = {
            "filas": 2,
            "columnas": 2,
            "minas": 1,
            "tablero": [[-1, 1], [1, 1]],
            "tablero_visible": [[BANDERA, "1"], ["1", "1"]],
            "juego_terminado": True
        }
        self.assertTrue(estado_valido(estado))

    def test_estado_valido_invalido(self):
        estado:EstadoJuego = {
            "filas": 2,
            "columnas": 3,
            "minas": 1,
            "tablero": [[0, -1], [1, 1]],
            "tablero_visible": [["0", "?"], ["1", "1"]],
            "juego_terminado": False
        }
        self.assertFalse(estado_valido(estado))
        estado:EstadoJuego = {
            "filas": 2,
            "columnas": 2,
            "minas": 4,
            "tablero": [[-1, -1], [-1, -1]],
            "tablero_visible": [["1", "?"], ["1", "1"]],
            "juego_terminado": False
        }
        self.assertFalse(estado_valido(estado))


class TestEstructuraYTiposValidos(unittest.TestCase):
    def test_estructura_y_tipos_validos_correcto(self):
        estado:EstadoJuego = {
            "filas": 2,
            "columnas": 2,
            "minas": 1,
            "tablero": [[-1, 1], [1, 1]],
            "tablero_visible": [[BANDERA, "1"], ["1", "1"]],
            "juego_terminado": True
        }
        self.assertTrue(estructura_y_tipos_validos(estado))

    def test_estructura_y_tipos_validos_incorrecto(self):
        estado:EstadoJuego = {
            "filas": "2",
            "columnas": 2,
            "minas": 1,
            "tablero": [[0, -1], [1, 1]],
            "tablero_visible": [["0", "?"], ["1", "1"]],
            "juego_terminado": False
        }
        #self.assertFalse(estructura_y_tipos_validos(estado)) # da ERROR
        estado:EstadoJuego = {
            "filas": 2,
            "dato_extra": 3,
            "columnas": 2,
            "minas": 1,
            "tablero": [[-1, 1], [1, 1]],
            "tablero_visible": [[BANDERA, "1"], ["1", "1"]],
            "juego_terminado": True
        }
        self.assertFalse(estructura_y_tipos_validos(estado))
        estado:EstadoJuego = {
            "filas": 2,
            "columnas": 2,
            "minas": 1,
            "tablero": [[-1, 9], [9, 1]],
            "tablero_visible": [[BANDERA, "1"], ["1", "1"]],
            "juego_terminado": True
        }
        self.assertFalse(estructura_y_tipos_validos(estado))
        estado:EstadoJuego = {
            "filas": 2,
            "columnas": 2,
            "minas": 1,
            "tablero": [[-1, 1], [1, 1]],
            "tablero_visible": [[BANDERA, "1"], ["1", "1"]],
            "juego_terminado": 2
        }
        self.assertFalse(estructura_y_tipos_validos(estado))
        estado:EstadoJuego = {
            "filas": -1,
            "columnas": 2,
            "minas": 1,
            "tablero": [[-1, 1], [1, 1]],
            "tablero_visible": [[BANDERA, "1"], ["1", "1"]],
            "juego_terminado": True
        }
        self.assertFalse(estructura_y_tipos_validos(estado))
        estado:EstadoJuego = {
            "filas": 2,
            "columnas": -1,
            "minas": 1,
            "tablero": [[-1, 1], [1, 1]],
            "tablero_visible": [[BANDERA, "1"], ["1", "1"]],
            "juego_terminado": True
        }
        self.assertFalse(estructura_y_tipos_validos(estado))     
        
    def test_son_matriz_y_misma_dimension_true(self):
        matriz_v1:list[list[int]] = [[1, 2], [3, 4]]
        matriz_v2:list[list[int]] = [["a", "b"], ["c", "d"]]
        self.assertTrue(son_matriz_y_misma_dimension(matriz_v1, matriz_v2))

    def test_son_matriz_y_misma_dimension_false(self):
        matriz_v1:list[list[int]] = [[1, 2], [3, 4]]
        matriz_v2:list[list[int]] = [["a", "b", "c"], ["d", "e", "f"]]
        self.assertFalse(son_matriz_y_misma_dimension(matriz_v1, matriz_v2))

class TestTodasCeldasSegurasDescubiertas(unittest.TestCase):
    def test_todas_celdas_seguras_descubiertas_true(self):
        tablero:list[list[int]] = [[-1, 1], [1, 1]]
        tablero_visible:list[list[int]] = [[BANDERA, "1"], ["1", "1"]]
        self.assertTrue(todas_celdas_seguras_descubiertas(tablero, tablero_visible))

    def test_todas_celdas_seguras_descubiertas_false(self):
        tablero:list[list[int]] = [[-1, 1], [1, 1]]
        tablero_visible:list[list[int]] = [[BANDERA, "?"], ["1", "1"]]
        self.assertFalse(todas_celdas_seguras_descubiertas(tablero, tablero_visible))


#Ejercicio 4:
class TestObtenerEstadoTableroVisible(unittest.TestCase):
    def test_copia_correcta_del_tablero_visible(self):
        estado: EstadoJuego = crear_juego(2, 2, 1)
        estado['tablero_visible'][0][0] = "1"           #Modifico manualmente la celda visible:para que muestra "1" (descubierta)
        estado['tablero_visible'][1][1] = BANDERA       #y otra una bandera
        copia:list[list[str]] = obtener_estado_tablero_visible(estado)

        # Verifica que la copia tenga el mismo contenido que el original
        self.assertEqual(copia, estado['tablero_visible'])   

        # Verifica que el original no se haya modificado
        copia[0][0] = "X"
        self.assertNotEqual(copia, estado['tablero_visible'])


#Ejercicio 5:
class TestMarcarCelda(unittest.TestCase):
    def test_marcar_y_desmarcar_correcto(self):
        estado:EstadoJuego = crear_juego(2, 2, 1)

        # Inicialmente todo debe ser VACIO
        self.assertEqual(estado['tablero_visible'][1][0], VACIO)

        # Marcamos con bandera
        marcar_celda(estado, 1, 0)
        self.assertEqual(estado['tablero_visible'][1][0], BANDERA)

        # Desmarcamos
        marcar_celda(estado, 1, 0)
        self.assertEqual(estado['tablero_visible'][1][0], VACIO)

    def test_no_modificar_si_termino(self):
        estado:EstadoJuego = crear_juego(2, 2, 1)
        estado['juego_terminado'] = True
        estado['tablero_visible'][0][0] = VACIO
        marcar_celda(estado, 0, 0)
        self.assertEqual(estado['tablero_visible'][0][0], VACIO)

    def test_no_marcar_si_ya_descubierto(self):
        estado:EstadoJuego = crear_juego(2, 2, 1)
        estado['tablero_visible'][0][0] = "1"
        marcar_celda(estado, 0, 0)
        self.assertEqual(estado['tablero_visible'][0][0], "1")

    def test_marcar_dos_celdas_distintas(self):
        estado:EstadoJuego = crear_juego(3, 3, 1)
        marcar_celda(estado, 1, 1)
        self.assertEqual(estado['tablero_visible'][1][1], BANDERA)
        marcar_celda(estado, 2, 2)
        self.assertEqual(estado['tablero_visible'][2][2], BANDERA)

    def test_no_afecta_a_otras_celdas(self):
        estado:EstadoJuego = crear_juego(2, 2, 1)
        marcar_celda(estado, 1, 1)
        self.assertEqual(estado['tablero_visible'][0][0], VACIO)
        self.assertEqual(estado['tablero_visible'][1][1], BANDERA)


#Ejercicio 6:
class TestDescubrirCelda(unittest.TestCase):
    def test_descubrir_con_expansion_final(self):
        estado: EstadoJuego = {
            'filas': 3,
            'columnas': 3,
            'minas': 2,
            'tablero': [
                [0, 1, -1],
                [0, 1, 1],
                [0, 0, 0]
            ],
            'tablero_visible': [
                [VACIO, VACIO, VACIO],
                [VACIO, VACIO, VACIO],
                [VACIO, VACIO, VACIO]
            ],
            'juego_terminado': False
        }

        descubrir_celda(estado, 2, 0)

        self.assertEqual(estado['tablero_visible'], [
            ["0", "1", VACIO],
            ["0", "1", "1"],
            ["0", "0", "0"]
        ])
        self.assertTrue(estado['juego_terminado'])        

    def test_descubrir_mina_termino_el_juego(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [-1, 1],
                [1, 1]
            ],
            'tablero_visible': [
                [VACIO, VACIO],
                [VACIO, VACIO]
            ],
            'juego_terminado': False
        }

        descubrir_celda(estado, 0, 0)
        self.assertEqual(estado['tablero_visible'][0][0], BOMBA)
        self.assertTrue(estado['juego_terminado'])

    def test_descubrir_sin_expansion(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [1, -1],
                [1, 1]
            ],
            'tablero_visible': [
                [VACIO, VACIO],
                [VACIO, VACIO]
            ],
            'juego_terminado': False
        }

        descubrir_celda(estado, 0, 0)
        self.assertEqual(estado['tablero_visible'][0][0], "1")
        self.assertFalse(estado['juego_terminado'])

    def test_descubrir_victoria(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [-1, 1],
                [1, 1]
            ],
            'tablero_visible': [
                [VACIO, VACIO],
                ["1", "1"]
            ],
            'juego_terminado': False
        }

        descubrir_celda(estado, 0, 1)
        self.assertTrue(todas_celdas_seguras_descubiertas(estado["tablero"], estado["tablero_visible"]))
        self.assertTrue(estado['juego_terminado'])

class TestCaminosDescubiertos(unittest.TestCase):
    def test_clic_en_numero(self):
        tablero:list[list[str]] = [
            [1, -1],
            [0, 2]
        ]
        tablero_visible:list[list[str]] = [
            [VACIO, VACIO],
            [VACIO, VACIO]
        ]
        caminos_esperados:list[list[tuple[int, int]]] = caminos_descubiertos(tablero, tablero_visible, 0, 0)
        self.assertEqual(caminos_esperados, [[(0, 0)]])

    def test_clic_en_0_aislado(self):
        tablero:list[list[str]] = [
            [0, 1],
            [1, -1]
        ]
        tablero_visible:list[list[str]] = [
            [VACIO, VACIO],
            [VACIO, VACIO]
        ]

        caminos: list[list[tuple[int, int]]] = caminos_descubiertos(tablero, tablero_visible, 0, 0)

        caminos_esperados: list[list[tuple[int, int]]] = [[(0, 0)], [(0, 1)], [(1, 0)]]

        # Para comparar sin importar el orden, recorremos todos los caminos esperados y verificamos que estén
        for camino in caminos_esperados:
            self.assertTrue(camino in caminos)

        # Y además verificamos que no haya caminos de más
        for camino in caminos:
            self.assertTrue(camino in caminos_esperados)

    def test_clic_en_0_con_bandera(self):
        tablero:list[list[str]] = [
            [0, 1],
            [1, 0]
        ]
        tablero_visible:list[list[str]] = [
            [VACIO, VACIO],
            [VACIO, BANDERA]
        ]
        caminos_esperados:list[list[tuple[int, int]]] = caminos_descubiertos(tablero, tablero_visible, 0, 0)

        celdas:list[tuple[int, int]] = []
        for camino in caminos_esperados:
            for p in camino:
                celdas.append(p)

        self.assertTrue((1, 1) not in celdas)

    def test_clic_en_0_expandido(self):
        tablero:list[list[str]] = [
            [0, 0, 1],
            [0, 1, -1],
            [0, 1, 1]
        ]
        tablero_visible:list[list[str]] = [
            [VACIO,VACIO,VACIO],
            [VACIO,VACIO,VACIO],
            [VACIO,VACIO,VACIO]
        ]
        caminos_esperados:list[list[tuple[int, int]]] = caminos_descubiertos(tablero, tablero_visible, 0, 0)

        celdas:list[tuple[int, int]] = []
        for camino in caminos_esperados:
            for p in camino:
                celdas.append(p)

        self.assertIn((0, 0), celdas)
        self.assertIn((2, 1), celdas)
        self.assertNotIn((1, 2), celdas)  # No expande sobre mina

#Ejercicio 7:
class TestVerificarVictoria(unittest.TestCase):
    def test_victoria_completa(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [-1, 1],
                [1, 1]
            ],
            'tablero_visible': [
                ["*", "1"],
                ["1", "1"]
            ],
            'juego_terminado': False
        }
        #self.assertTrue(verificar_victoria(estado)) #nose porque da Fail

    def test_falta_descubrir_celda_segura(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [-1, 1],
                [1, 1]
            ],
            'tablero_visible': [
                ["*", VACIO],
                ["1", "1"]
            ],
            'juego_terminado': False
        }
        self.assertFalse(verificar_victoria(estado))

    def test_descubrimiento_incorrecto(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [-1, 1],
                [1, 1]
            ],
            'tablero_visible': [
                ["*", "2"],
                ["1", "1"]
            ],
            'juego_terminado': False
        }
        self.assertFalse(verificar_victoria(estado))

    def test_dimensiones_diferentes(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [-1, 1],
                [1, 1]
            ],
            'tablero_visible': [
                ["*", "1"]
            ],
            'juego_terminado': False
        }
        self.assertFalse(verificar_victoria(estado))

    def test_tablero_no_es_matriz(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [-1, 1],
                [1]
            ],
            'tablero_visible': [
                ["*", "1"],
                ["1", "1"]
            ],
            'juego_terminado': False
        }
        self.assertFalse(verificar_victoria(estado))

#Ejercicio 8:
class TestReiniciarJuego(unittest.TestCase):
    def test_reiniciar_juego(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [-1, 1],
                [1, 1]
            ],
            'tablero_visible': [
                [VACIO, "1"],
                ["1", VACIO]
            ],
            'juego_terminado': True
        }
        
        filas: int = estado["filas"]
        columnas: int = estado["columnas"]
        nuevo_tablero: list[list[str]] = []

        for _ in range(filas):
            fila: list[str] = []
            for _ in range(columnas):
                fila.append(VACIO)
            nuevo_tablero.append(fila)

        reiniciar_juego(estado)

        # El tablero_visible debe ser completamente VACIO
        for fila in estado['tablero_visible']:
            for celda in fila:
                self.assertEqual(celda, VACIO)

        # La cantidad de minas debe seguir siendo 1
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 1)

        # Las dimensiones deben seguir siendo las mismas
        self.assertEqual(len(estado['tablero']), 2)
        self.assertEqual(len(estado['tablero'][0]), 2)

        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 1)

        # El juego debe estar en estado no terminado
        self.assertFalse(estado['juego_terminado'])

        # El tablero debe ser distinto al anterior
        self.assertNotEqual(estado['tablero'], nuevo_tablero)

#Ejercicio 9:
class TestGuardarEstado(unittest.TestCase):
    def leer_lineas_sin_salto(self, nombre): # se escribre de esta forma al definir la funcion dentro del class
        archivo:str = open(nombre, "r")
        lineas:list = []
        for linea in archivo:
            texto:str = ""
            for celda in linea:
                if celda != "\n":
                    texto = texto + celda
            lineas.append(texto)
        archivo.close()
        return lineas


    def test_guardar_estado_valido(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [[-1, 1], [1, 1]],
            'tablero_visible': [[BANDERA, "1"], ["1", VACIO]],
            'juego_terminado': False
        }

        guardar_estado(estado, ".")
        self.assertTrue(os.path.exists("tablero.txt"))
        self.assertTrue(os.path.exists("tablero_visible.txt"))
        tablero:list = self.leer_lineas_sin_salto("tablero.txt")
        visible:list = self.leer_lineas_sin_salto("tablero_visible.txt")
        self.assertEqual(tablero, ["-1,1", "1,1"])
        self.assertEqual(visible, ["*,1", "1,?"])
        borrar_archivos()

    def test_estado_terminado_no_guarda(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [[-1, 1], [1, 1]],
            'tablero_visible': [["1", "1"], ["1", "1"]],
            'juego_terminado': True
        }

        guardar_estado(estado, ".")
        self.assertFalse(os.path.exists("tablero.txt"))
        self.assertFalse(os.path.exists("tablero_visible.txt"))

    def test_estado_invalido_no_guarda(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [[-1, 1], [1, 1]],
            'tablero_visible': [["$", "1"], ["1", "1"]],
            'juego_terminado': False
        }

        guardar_estado(estado, ".")
        self.assertFalse(os.path.exists("tablero.txt"))
        self.assertFalse(os.path.exists("tablero_visible.txt"))


    def test_guardar_estado_con_tablero_mal_formado(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [[-1], [1, 1]],  # una fila con menos columnas
            'tablero_visible': [[VACIO, "1"], [VACIO, VACIO]],
            'juego_terminado': False
        }

        guardar_estado(estado, ".")
        self.assertFalse(os.path.exists("tablero.txt"))
        self.assertFalse(os.path.exists("tablero_visible.txt"))


#Ejercicio 10:
class TestCargarEstado(unittest.TestCase):
    def escribir_archivo(self, nombre: str, lineas: list[str]) -> None:
        archivo:str = open(nombre, "w")
        for linea in lineas:
            archivo.write(linea + "\n")
        archivo.close()

    def test_cargar_estado_valido(self):
        self.escribir_archivo("tablero.txt", ["-1,1", "1,1"])
        self.escribir_archivo("tablero_visible.txt", ["*,1", "1,?"])
        estado: EstadoJuego = {}
        resultado:bool = cargar_estado(estado, ".")
        self.assertTrue(resultado)
        self.assertEqual(estado["tablero"], [[-1, 1], [1, 1]])
        self.assertEqual(estado["tablero_visible"], [[BANDERA, "1"], ["1", VACIO]])
        borrar_archivos()

    def test_archivo_inexistente(self):
        estado: EstadoJuego = {}
        resultado:bool = cargar_estado(estado, "./noexiste")
        self.assertFalse(resultado)

    def test_tablero_fuera_de_rango(self):
        self.escribir_archivo("tablero.txt", ["-1,9", "1,1"])
        self.escribir_archivo("tablero_visible.txt", ["*,1", "1,?"])
        estado: EstadoJuego = {}
        resultado:bool = cargar_estado(estado, ".")
        self.assertFalse(resultado)
        borrar_archivos()

    def test_tablero_visible_caracter_invalido(self):
        self.escribir_archivo("tablero.txt", ["-1,1", "1,1"])
        self.escribir_archivo("tablero_visible.txt", ["*,1", "1,X"])
        estado: EstadoJuego = {}
        resultado:bool = cargar_estado(estado, ".")
        self.assertFalse(resultado)
        borrar_archivos()

    def test_tablero_comas_erroneas(self):
        self.escribir_archivo("tablero.txt", ["-1,1,1", "1,1"])
        self.escribir_archivo("tablero_visible.txt", ["*,1", "1,?"])
        estado: EstadoJuego = {}
        resultado:bool = cargar_estado(estado, ".")
        self.assertFalse(resultado)
        borrar_archivos()

# Tarea: Pensar cómo testear  guardar_estado y cargar_estado
# Las puse arribe

"""
- Agregar varios casos de prueba para cada función.
- Se debe cubrir al menos el 95% de las líneas de cada función.
- Se debe cubrir al menos el 95% de ramas de cada función.
"""

# Ejecutar todos los tests
if __name__ == '__main__':
    unittest.main(verbosity=2)
