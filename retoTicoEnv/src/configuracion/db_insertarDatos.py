import sqlite3
import sys
import os


class Db_insertarDatos:
    @staticmethod
    def insertar_datos():
        # Definir la ruta de la base de datos en el directorio de usuario
        user_dir = os.path.expanduser("~")
        db_path = os.path.join(user_dir, 'retotico.db')  # Cambia "mi_juego.db" por el nombre de tu BD
        
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        # Verificamos si ya existen categorías para no insertarlas nuevamente
        c.execute("SELECT COUNT(*) FROM categorias")
        if c.fetchone()[0] == 0:  # Si no existen categorías, insertamos
            # Inserción de categorías
            categorias = [
                ('Historia',),
                ('Geografía',),
                ('Fauna y Flora',),
                ('Cultura y Tradiciones',),
                ('Economía',)
            ]
            c.executemany('INSERT INTO categorias (nombre_categoria) VALUES (?)', categorias)

            # Inserción de preguntas para cada categoría
            preguntas = [
                # Historia
                ('¿En qué año se abolió el ejército en Costa Rica?', 1, 'media'),
                ('¿Quién fue el primer presidente de Costa Rica?', 1, 'media'),
                ('¿Qué batalla famosa se libró en 1856?', 1, 'media'),
                ('¿Qué tratado se firmó para definir las fronteras con Nicaragua?', 1, 'media'),
                ('¿Cuál fue el propósito principal de la Campaña Nacional?', 1, 'media'),
                # Geografía
                ('¿Cuál es el volcán más alto de Costa Rica?', 2, 'media'),
                ('¿Cuántas provincias tiene Costa Rica?', 2, 'media'),
                ('¿Cuál es el río más largo de Costa Rica?', 2, 'media'),
                ('¿Qué parque nacional es famoso por sus tortugas marinas?', 2, 'media'),
                ('¿Cuál es el pico más alto de Costa Rica?', 2, 'media'),
                # Fauna y Flora
                ('¿Cuál es el ave nacional de Costa Rica?', 3, 'media'),
                ('¿Qué rana es conocida por su color rojo y ojos verdes?', 3, 'media'),
                ('¿Qué mariposa es símbolo de transformación en Costa Rica?', 3, 'media'),
                ('¿Cuál es el animal que representa al perezoso en la fauna costarricense?', 3, 'media'),
                ('¿Qué flor es la nacional?', 3, 'media'),
                # Cultura y Tradiciones
                ('¿Qué significa “Pura Vida”?', 4, 'media'),
                ('¿Qué festividad se celebra el 15 de septiembre?', 4, 'media'),
                ('¿Qué bebida es popular durante las fiestas navideñas?', 4, 'media'),
                ('¿Qué día se celebra el Día del Agricultor?', 4, 'media'),
                # Economía
                ('¿Cuál es el principal producto de exportación de Costa Rica?', 5, 'alta'),
                ('¿Qué recurso natural es utilizado principalmente para la producción de energía en Costa Rica?', 5, 'alta'),
                ('¿En qué año Costa Rica se convirtió en el primer país de América Latina en eliminar los impuestos sobre las exportaciones?', 5, 'alta'),
                
            ]
            c.executemany('INSERT INTO preguntas (pregunta, id_categoria, nivel_dificultad) VALUES (?, ?, ?)', preguntas)

            # Inserción de respuestas
            respuestas = [
                # Respuestas para cada pregunta
                ('1949', 1, 1, 10), ('1821', 0, 1, 0), ('1972', 0, 1, 0), ('1994', 0, 1, 0),
                ('José María Castro Madriz', 1, 2, 10), ('Juan Mora Fernández', 0, 2, 0), ('Alfredo González Flores', 0, 2, 0), ('Rafael Ángel Calderón Guardia', 0, 2, 0),
                ('Batalla de Santa Rosa', 1, 3, 10), ('Batalla de Rivas', 0, 3, 0), ('Batalla de la Trinidad', 0, 3, 0), ('Batalla de Sardinal', 0, 3, 0),
                ('Tratado Cañas-Jerez', 1, 4, 10), ('Tratado Limón-Matagalpa', 0, 4, 0), ('Tratado de Managua', 0, 4, 0), ('Tratado de San José', 0, 4, 0),
                ('Expulsar a los filibusteros', 1, 5, 10), ('Abolir el ejército', 0, 5, 0), ('Firmar la independencia', 0, 5, 0), ('Nacionalizar los bancos', 0, 5, 0),
                # Geografía
                ('Cerro Chirripó', 1, 6, 10), ('Volcán Poás', 0, 6, 0), ('Volcán Arenal', 0, 6, 0), ('Volcán Turrialba', 0, 6, 0),
                ('7', 1, 7, 10), ('5', 0, 7, 0), ('9', 0, 7, 0), ('8', 0, 7, 0),
                ('Río San Juan', 1, 8, 10), ('Río Tempisque', 0, 8, 0), ('Río Grande de Térraba', 0, 8, 0), ('Río Reventazón', 0, 8, 0),
                ('Parque Nacional Tortuguero', 1, 9, 10), ('Parque Nacional Corcovado', 0, 9, 0), ('Parque Nacional Manuel Antonio', 0, 9, 0), ('Parque Nacional Cahuita', 0, 9, 0),
                ('Cerro Chirripó', 1, 10, 10), ('Cerro de la Muerte', 0, 10, 0), ('Cerro Kamuk', 0, 10, 0), ('Cerro de los Ángeles', 0, 10, 0),
                # Categoria de Fauna y Flora
                ("Yigüirro",1,11,10), ("Tucán",0,11,0), ("Quetzal",0,11,0), ("Colibrí",0,11,0),
                ("Rana flecha roja",1,12,10), ("Rana de árbol verde",0,12,0), ("Rana toro",0,12,0), ("Rana perezosa",0,12,0),
                ("Mariposa morfo azul",1,13,10), ("Mariposa monarca",0,13,0), ("Mariposa cristal",0,13,0), ("Mariposa nocturna",0,13,0),
                ("Pereza de tres dedos",1,14,10), ("Mono capuchino",0,14,0), ("Oso perezoso",0,14,0), ("Pereza de dos dedos",0,14,0),
                ("Orquídea Guaria Morada",1,15,10), ("Rosa",0,15,0), ("Margarita",0,15,0), ("Girasol",0,15,0),
                # Categoria de Cultura y Tradiciones
                ("Buenas vibras",1,16,10), ("Vida sencilla",0,16,0), ("Salud",0,16,0), ("Felicidad",0,16,0),
                ("Día de la Independencia",1,17,10), ("Día del Trabajo",0,17,0), ("Día de San José",0,17,0), ("Día del Agricultor",0,17,0),
                ("Rompope",1,18,10), ("Cerveza",0,18,0), ("Ron",0,18,0), ("Vino",0,18,0),
                ("15 de mayo",1,19,10), ("1 de abril",0,19,0), ("10 de agosto",0,19,0), ("25 de diciembre",0,19,0),
                # Respuestas para la categoría Economía
                ('Piña', 1, 20, 10), ('Café', 0, 20, 0), ('Plátano', 0, 20, 0), ('Azúcar', 0, 20, 0),
                ('Energía geotérmica', 1, 21, 10), ('Petróleo', 0, 21, 0), ('Energía nuclear', 0, 21, 0), ('Energía solar', 0, 21, 0),
                ('1991', 1, 22, 10), ('1951', 0, 22, 0), ('1985', 0, 22, 0), ('2000', 0, 22, 0), 
            ]
            c.executemany('INSERT INTO respuestas (respuesta, es_correcta, id_pregunta, valor_puntos) VALUES (?, ?, ?, ?)', respuestas)

        conn.commit()
        conn.close()
