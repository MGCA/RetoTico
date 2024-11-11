import sqlite3
import sys
import os

class InsertarJuegos:
    def __init__(self, db_name='retotico.db'):
        # Definir la ruta completa de la base de datos en el directorio del usuario
        user_dir = os.path.expanduser("~")
        self.db_path = os.path.join(user_dir, db_name)
        
        self.conn = None
        self.cursor = None

    def abrir_conexion(self):
        """ Abre la conexión a la base de datos """
        if self.conn is None:
            try:
                self.conn = sqlite3.connect(self.db_path)
                self.cursor = self.conn.cursor()
            except sqlite3.Error as e:
                print(f"Error al abrir la base de datos: {e}")
                raise

    def cerrar_conexion(self):
        """ Cierra la conexión con la base de datos """
        if self.conn:
            try:
                self.conn.commit()  # Asegurarse de que todos los cambios estén guardados
                self.conn.close()
            except sqlite3.Error as e:
                print(f"Error al cerrar la conexión a la base de datos: {e}")
            finally:
                self.conn = None
                self.cursor = None

    def insertar_historial_juego(self, id_usuario, fecha_juego, puntos_obtenidos):
        """
        Inserta un registro en historial_juegos.
        :param id_usuario: ID del usuario que jugó.
        :param fecha_juego: Fecha en la que se jugó.
        :param puntos_obtenidos: Puntos obtenidos en el juego.
        :return: ID del historial insertado.
        """
        self.abrir_conexion()
        try:
            # Insertar el historial del juego
            self.cursor.execute('''
                INSERT INTO historial_juegos (id_usuario, fecha_juego, puntos_obtenidos)
                VALUES (?, ?, ?)
            ''', (id_usuario, fecha_juego, puntos_obtenidos))

            # Obtener el ID del historial recién insertado
            id_historial = self.cursor.lastrowid
            self.conn.commit()
            return id_historial
        except sqlite3.Error as e:
            print(f"Error al insertar el historial del juego: {e}")
            self.conn.rollback()
            raise
        finally:
            self.cerrar_conexion()

    def insertar_detalle_historial(self, id_historial, id_pregunta, id_respuesta_usuario, es_correcta):
        """
        Inserta un detalle de historial para registrar una respuesta del usuario.
        :param id_historial: ID del historial del juego.
        :param id_pregunta: ID de la pregunta respondida.
        :param id_respuesta_usuario: ID de la respuesta seleccionada por el usuario.
        :param es_correcta: Indica si la respuesta fue correcta (1 para correcta, 0 para incorrecta).
        """
        self.abrir_conexion()
        try:
            # Insertar el detalle del historial
            self.cursor.execute('''
                INSERT INTO detalles_historial (id_historial, id_pregunta, id_respuesta_usuario, es_correcta)
                VALUES (?, ?, ?, ?)
            ''', (id_historial, id_pregunta, id_respuesta_usuario, es_correcta))

            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error al insertar el detalle del historial: {e}")
            self.conn.rollback()
            raise
        finally:
            self.cerrar_conexion()
