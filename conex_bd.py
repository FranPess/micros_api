"""
Módulo que permite generar una clase llamada ConexionBD la cual presenta los métodos necesarios para crear
la base de datos, conectarse a la base de datos y cerrar la base de datos, también contiene un nro limitado de reintentos de conexión
como las llamadas a las funciones que transfieren los errores de conexión a la base de datos al observador y también llama a las funciones
de enviar los log.txt por ssh al servidor.
se importa lo siguiente:
* Libreria sqlite3
* Libreria os.path
"""
import sqlite3
from os.path import abspath, dirname, join
from observador import ErrorBaseDeDatosObservador
from ssh_log import transferir_archivos_on_error


class ConexionBD:
    def __init__(self, db_ruta, max_intentos=3):
        self.db_ruta = db_ruta
        self.max_intentos = max_intentos
        self.intentos = 0
        self.con = None
        self.cursor = None
        self.observador_error = ErrorBaseDeDatosObservador()
        self.observadores = [self.observador_error]
        self.error_notificado = False

    def agregar_observador(self, observador):
        self.observadores.append(observador)

    def notificar_error(self, mensaje):
        if not self.error_notificado:
            for observador in self.observadores:
                if isinstance(observador, ErrorBaseDeDatosObservador):
                    observador.on_error(mensaje)
            self.error_notificado = True
            transferir_archivos_on_error(["log_bd.txt", "detalles_crud.txt"], ["C:/Users/Administrator/Desktop/TGM_Bot/log_bd.txt", "C:/Users/Administrator/Desktop/TGM_Bot/detalles_crud.txt"])
            
    def reiniciar_estado_error(self):
        self.error_notificado = False

    def intentar_conexion(self): #Intentos máximos de conexion a la bd
        self.intentos += 1
        if self.intentos <= self.max_intentos:
            self.conectar()
        else:
            self.notificar_error("Número máximo de intentos de conexión alcanzado.")
    
    def conectar(self):
        try:
            self.con = sqlite3.connect(self.db_ruta)
            self.cursor = self.con.cursor()
            self.intentos = 0  # Reiniciar contador de intentos al conectar
            self.reiniciar_estado_error()  # Reiniciar estado de error al conectar
        except sqlite3.Error as e:
            if not self.error_notificado:
                self.notificar_error(str(e))

    def crear_tabla(self):
        sql = 'CREATE TABLE IF NOT EXISTS salidas (id INTEGER PRIMARY KEY AUTOINCREMENT, interno INTEGER NOT NULL, numero INTEGER NOT NULL, chofer VARCHAR(25), recorrido VARCHAR(40), salida TEXT, fecha TEXT)'
        try:
            self.cursor.execute(sql)
            self.con.commit()
        except sqlite3.Error as e:
            self.notificar_error(f"Error al crear tabla: {e}")
            raise

    def cerrar_conexion(self):
        if self.con:
            self.con.close()

    def conex(self):
        script_dir = dirname(abspath(__file__))
        self.db_ruta = join(script_dir, "micros.bd")
        self.intentar_conexion()

        try:
            self.crear_tabla()
        except Exception as e:
            print("Error:", str(e))
