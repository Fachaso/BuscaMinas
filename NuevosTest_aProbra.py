#TestEstadoValido
def test_no_descubiertas_y_sin_bomba(self):
    # Testea si no hay BOMBA visible pero tampoco están todas las celdas descubiertas
    estado: EstadoJuego = {
        'filas': 2,
        'columnas': 2,
        'minas': 1,
        'tablero': [[-1, 1], [1, 1]],
        'tablero_visible': [[VACIO, VACIO], [VACIO, VACIO]],
        'juego_terminado': False
    }
    self.assertFalse(estado_valido(estado))

#TestEstructuraYTipos
def test_tipo_invalido_en_tablero(self):
    estado = crear_juego(2, 2, 1)
    estado['tablero'][0][0] = 99  # Valor fuera de rango permitido (-1 a 8)
    self.assertFalse(estructura_y_tipos_validos(estado))

def test_valor_invalido_en_tablero_visible(self):
    estado = crear_juego(2, 2, 1)
    estado['tablero_visible'][0][0] = 'Z'  # No es VACIO, BANDERA, BOMBA ni número
    self.assertFalse(estructura_y_tipos_validos(estado))

def test_tipo_incorrecto_en_filas(self):
    estado = crear_juego(2, 2, 1)
    estado['filas'] = 'dos'  # Tipo incorrecto
    self.assertFalse(estructura_y_tipos_validos(estado))

#marcar_celdaTest
def test_no_marcar_si_terminado(self):
    estado = crear_juego(2, 2, 1)
    estado['juego_terminado'] = True
    valor_original = estado['tablero_visible'][0][0]
    marcar_celda(estado, 0, 0)
    self.assertEqual(estado['tablero_visible'][0][0], valor_original)

def test_no_marcar_si_no_vacia(self):
    estado = crear_juego(2, 2, 1)
    estado['tablero_visible'][0][0] = '1'  # ya descubierta
    valor_original = estado['tablero_visible'][0][0]
    marcar_celda(estado, 0, 0)
    self.assertEqual(estado['tablero_visible'][0][0], valor_original)

#descubrir_celdaTest
def test_no_descubre_bandera(self):
    estado: EstadoJuego = {
        'filas': 2,
        'columnas': 2,
        'minas': 0,
        'tablero': [[0, 0], [0, 0]],
        'tablero_visible': [[VACIO, BANDERA], [VACIO, VACIO]],
        'juego_terminado': False
    }
    descubrir_celda(estado, 0, 0)
    self.assertEqual(estado['tablero_visible'][0][1], BANDERA)  # la bandera debe mantenerse

#cargar_estadoTest (archivos mal formados)
def test_cargar_estado_mal_valor(self):
    # Creamos un archivo incorrecto a mano usando funciones permitidas
    archivo_tablero = open(os.path.join(\"testdata\", \"tablero.txt\"), \"w\")  # usamos open y write
    archivo_tablero.write(\"X,1\\n1,1\\n\")  # X no es un valor válido
    archivo_tablero.close()

    archivo_visible = open(os.path.join(\"testdata\", \"tablero_visible.txt\"), \"w\")
    archivo_visible.write(\"?,1\\n?,1\\n\")
    archivo_visible.close()

    estado = {}
    self.assertFalse(cargar_estado(estado, \"testdata\"))
