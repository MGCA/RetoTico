import csv
import sqlite3
import os

class Db_insertarPcd:
    @staticmethod
    def insertar_datos():
        # Obtener el directorio base
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Construir la ruta del directorio assets/csv
        assets_dir = os.path.join(base_dir, '..', 'assets', 'csv')
        
        # Definir la ruta de la base de datos en el directorio de usuario
        user_dir = os.path.expanduser("~")
        db_path = os.path.join(user_dir, 'retotico.db')
        
        # Conectar a la base de datos
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Insertar datos
        Db_insertarPcd._insertar_provincias(cursor, assets_dir)
        Db_insertarPcd._insertar_cantones(cursor, assets_dir)
        Db_insertarPcd._insertar_distritos(cursor, assets_dir)

        # Guardar los cambios y cerrar la conexión
        conn.commit()
        conn.close()

    @staticmethod
    def _insertar_provincias(cursor, assets_dir):
        ruta_csv = os.path.join(assets_dir, "provincias.csv")
        with open(ruta_csv, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Saltar la cabecera del CSV
            for row in reader:
                cursor.execute("INSERT INTO provincias (CodigoProvincia, Provincia) VALUES (?, ?)", (row[0], row[1]))

    @staticmethod
    def _insertar_cantones(cursor, assets_dir):
        ruta_csv = os.path.join(assets_dir, "cantones.csv")
        with open(ruta_csv, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Saltar la cabecera del CSV
            for row in reader:
                cursor.execute("INSERT INTO cantones (CodigoProvincia, CodigoCanton, Provincia, Canton) VALUES (?, ?, ?, ?)", 
                               (row[0], row[1], row[2], row[3]))

    @staticmethod
    def _insertar_distritos(cursor, assets_dir):
        ruta_csv = os.path.join(assets_dir, "distritos.csv")
        with open(ruta_csv, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Saltar la cabecera del CSV
            for row in reader:
                cursor.execute("""
                    INSERT OR REPLACE INTO distritos (CodigoProvincia, CodigoCanton, CodigoDistrito, Provincia, Canton, Distrito, RegionINEC) 
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
