# db_setup.py

import sqlite3
import os
from configuracion.db_insertarDatos import Db_insertarDatos

class Db_setup:
    @staticmethod
    def create_tables():
        # Verificar si la base de datos existe
        db_exists = os.path.exists('retotico.db')

        # Crear la base de datos y las tablas si no existen
        conn = sqlite3.connect('retotico.db')
        c = conn.cursor()

        # Crear las tablas si no existen
        c.execute(''' 
            CREATE TABLE IF NOT EXISTS usuarios (
                id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT,
                apellido TEXT,
                edad INTEGER,
                provincia TEXT,
                canton TEXT,
                distrito TEXT,
                numero_whatsapp TEXT,
                correo TEXT
            )
        ''')

        c.execute(''' 
            CREATE TABLE IF NOT EXISTS categorias (
                id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre_categoria TEXT
            )
        ''')

        c.execute(''' 
            CREATE TABLE IF NOT EXISTS preguntas (
                id_pregunta INTEGER PRIMARY KEY AUTOINCREMENT,
                pregunta TEXT,
                id_categoria INTEGER,
                nivel_dificultad TEXT,
                FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria)
            )
        ''')

        c.execute(''' 
            CREATE TABLE IF NOT EXISTS respuestas (
                id_respuesta INTEGER PRIMARY KEY AUTOINCREMENT,
                respuesta TEXT,
                es_correcta BOOLEAN,
                id_pregunta INTEGER,
                valor_puntos INTEGER,
                FOREIGN KEY (id_pregunta) REFERENCES preguntas(id_pregunta)
            )
        ''')

        c.execute(''' 
            CREATE TABLE IF NOT EXISTS historial_juegos (
                id_historial INTEGER PRIMARY KEY AUTOINCREMENT,
                id_usuario INTEGER,
                fecha_juego TEXT,
                puntos_obtenidos INTEGER,
                FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
            )
        ''')

        c.execute(''' 
            CREATE TABLE IF NOT EXISTS detalles_historial (
                id_detalle INTEGER PRIMARY KEY AUTOINCREMENT,
                id_historial INTEGER,
                id_pregunta INTEGER,
                id_respuesta_usuario INTEGER,
                es_correcta INTEGER,
                FOREIGN KEY (id_historial) REFERENCES historial_juegos(id_historial),
                FOREIGN KEY (id_pregunta) REFERENCES preguntas(id_pregunta),
                FOREIGN KEY (id_respuesta_usuario) REFERENCES respuestas(id_respuesta)
            )
        ''')

        c.execute(''' 
            CREATE TABLE IF NOT EXISTS imagenes (
                id_imagen INTEGER PRIMARY KEY AUTOINCREMENT,
                id_pregunta INTEGER,
                ruta_imagen TEXT,
                FOREIGN KEY (id_pregunta) REFERENCES preguntas(id_pregunta)
            )
        ''')

        conn.commit()

        # Si la base de datos no existe, entonces insertar los datos
        if not db_exists:
            print("Base de Datos creada")
            Db_insertarDatos.insertar_datos()
            print("Datos cargados")

        conn.close()