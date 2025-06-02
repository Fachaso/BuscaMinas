import unittest
import os
from buscaminas3 import (crear_juego, descubrir_celda, marcar_celda, obtener_estado_tablero_visible,
                               reiniciar_juego, colocar_minas, calcular_numeros, verificar_victoria, 
                               guardar_estado, cargar_estado, BOMBA, BANDERA, VACIO, EstadoJuego,
                               es_matriz,estado_valido,son_matriz_y_misma_dimension,estructura_y_tipos_validos)


'''
Ayudamemoria: entre los métodos para testear están los siguientes:

    self.assertEqual(a, b) -> testea que a y b tengan el mismo valor
    self.assertTrue(x)     -> testea que x sea True
    self.assertFalse(x)    -> testea que x sea False
    self.assertIn(a, b)    -> testea que a esté en b (siendo b una lista o tupla)
'''
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


# Test para colocar_minas
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
        

# Test para es_matriz
class TestEsMatriz(unittest.TestCase):
    def test_valido(self):
        self.assertTrue(es_matriz([[1, 2], [3, 4]]))

    def test_vacio(self):
        self.assertFalse(es_matriz([]))

    def test_filas_diferentes(self):
        self.assertFalse(es_matriz([[1, 2], [3]]))

# Test para calcular_numeros
class calcular_numerosTest(unittest.TestCase):
    def test_ejemplo(self):
        tablero = [[0,-1],
                   [0, 0]]

        calcular_numeros(tablero)
        # Testeamos que el tablero tenga los números correctos
        self.assertEqual(tablero, [[1,-1],
                                   [1, 1]])

# Test para crear_juego y validaciones
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

# Test para estado_valido
class TestEstadoValido(unittest.TestCase):
    def test_valido(self):
        estado: EstadoJuego = crear_juego(2, 2, 1)
        self.assertTrue(estado_valido(estado))

# Test para estructura_y_tipos_validos
class TestEstructuraYTipos(unittest.TestCase):
    def test_faltan_claves(self):
        estado_mal: EstadoJuego = {'filas': 2}
        self.assertFalse(estructura_y_tipos_validos(estado_mal))

# Test para son_matriz_y_misma_dimension
class TestMismaDimension(unittest.TestCase):
    def test_correcta(self):
        self.assertTrue(son_matriz_y_misma_dimension([[1,2]], [["a","b"]]))

    def test_distinta(self):
        self.assertFalse(son_matriz_y_misma_dimension([[1,2]], [["a"]]))

# Test para marcar_celda
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


# Test para descubrir_celda
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

    #mirar si hace falta implementarlo
    """def test_descubrir_bomba(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [[-1, 1], [1, 1]],
            'tablero_visible': [[VACIO, VACIO], [VACIO, VACIO]],
            'juego_terminado': False
        }
        descubrir_celda(estado, 0, 0)
        self.assertEqual(estado['tablero_visible'][0][0], BOMBA)
        self.assertTrue(estado['juego_terminado'])"""

# Test para verificar_victoria
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

# Test para reiniciar_juego
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

# Tarea: Pensar cómo testear  guardar_estado y cargar_estado

# Test para guardar_estado
class guardar_estadoTest(unittest.TestCase):
    def test_ejemplo (self):
        # Asegurarse de que la carpeta testdata exista manualmente
        self.assertTrue(os.path.exists("testdata"))  # <- no usamos os.mkdir()

        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [[-1, 1], [1, 1]],
            'tablero_visible': [[BANDERA, "1"], [VACIO, "1"]],
            'juego_terminado': False
        }

        # Guardamos el estado
        guardar_estado(estado, "testdata")

        # Verificamos que los archivos fueron creados
        self.assertTrue(os.path.exists(os.path.join("testdata", "tablero.txt")))
        self.assertTrue(os.path.exists(os.path.join("testdata", "tablero_visible.txt")))

        # Creamos nuevo estado vacío y lo cargamos desde el archivo
        nuevo_estado: EstadoJuego = {}
        resultado: bool = cargar_estado(nuevo_estado, "testdata")

        # Verificamos que todo esté correcto
        self.assertTrue(resultado)
        self.assertEqual(nuevo_estado['filas'], 2)
        self.assertEqual(nuevo_estado['columnas'], 2)
        self.assertEqual(nuevo_estado['minas'], 1)
        self.assertEqual(nuevo_estado['tablero'], estado['tablero'])
        self.assertEqual(nuevo_estado['tablero_visible'], estado['tablero_visible'])
        self.assertFalse(nuevo_estado['juego_terminado'])
        

# Test para cargar_estado
class cargar_estadoTest(unittest.TestCase):
    def test_ejemplo (self):
        
        # Aseguramos que los archivos existen antes de cargar
        self.assertTrue(os.path.exists(os.path.join("testdata", "tablero.txt")))
        self.assertTrue(os.path.exists(os.path.join("testdata", "tablero_visible.txt")))

        # Creamos un diccionario vacío para cargar el estado
        estado_cargado: EstadoJuego = {}

        # Ejecutamos la función y verificamos que devuelve True
        resultado: bool = cargar_estado(estado_cargado, "testdata")
        self.assertTrue(resultado)

        # Verificamos que los datos cargados sean correctos
        self.assertEqual(estado_cargado['filas'], 2)
        self.assertEqual(estado_cargado['columnas'], 2)
        self.assertEqual(estado_cargado['minas'], 1)
        self.assertEqual(estado_cargado['tablero'], [[-1, 1], [1, 1]])
        self.assertEqual(estado_cargado['tablero_visible'], [[BANDERA, "1"], [VACIO, "1"]])
        self.assertFalse(estado_cargado['juego_terminado'])


"""
- Agregar varios casos de prueba para cada función.
- Se debe cubrir al menos el 95% de las líneas de cada función.
- Se debe cubrir al menos el 95% de ramas de cada función.
"""

# Ejecutar todos los tests
if __name__ == '__main__':
    unittest.main(verbosity=2)

