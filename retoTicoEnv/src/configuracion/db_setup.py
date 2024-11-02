import sqlite3
class Db_setup:
    def create_tables():
        conn = sqlite3.connect('retotico.db')
        c = conn.cursor()

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
        )''')

        c.execute('''
        CREATE TABLE IF NOT EXISTS categorias (
            id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_categoria TEXT
        )''')

        c.execute('''
        CREATE TABLE IF NOT EXISTS preguntas (
            id_pregunta INTEGER PRIMARY KEY AUTOINCREMENT,
            pregunta TEXT,
            id_categoria INTEGER,
            nivel_dificultad TEXT,
            FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria)
        )''')

        c.execute('''
        CREATE TABLE IF NOT EXISTS respuestas (
            id_respuesta INTEGER PRIMARY KEY AUTOINCREMENT,
            respuesta TEXT,
            es_correcta BOOLEAN,
            id_pregunta INTEGER,
            valor_puntos INTEGER,
            FOREIGN KEY (id_pregunta) REFERENCES preguntas(id_pregunta)
        )''')

        c.execute('''
        CREATE TABLE IF NOT EXISTS historial_juegos (
            id_historial INTEGER PRIMARY KEY AUTOINCREMENT,
            id_usuario INTEGER,
            id_pregunta INTEGER,
            fecha_juego TEXT,
            aciertos INTEGER,
            desaciertos INTEGER,
            puntos_obtenidos INTEGER,
            FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),
            FOREIGN KEY (id_pregunta) REFERENCES preguntas(id_pregunta)
        )''')

        c.execute('''
        CREATE TABLE IF NOT EXISTS imagenes (
            id_imagen INTEGER PRIMARY KEY AUTOINCREMENT,
            id_pregunta INTEGER,
            ruta_imagen TEXT,
            FOREIGN KEY (id_pregunta) REFERENCES preguntas(id_pregunta)
        )''')
        
        

        conn.commit()
        conn.close()

    if __name__ == "__main__":
        create_tables()
