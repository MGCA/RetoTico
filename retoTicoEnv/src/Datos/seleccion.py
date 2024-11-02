import sqlite3

class Seleccion:
    def __init__(self, db_name='retotico.db'):
        self.db_name = db_name

    def hay_jugadores(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('SELECT COUNT(*) FROM usuarios')
        count = c.fetchone()[0]
        conn.close()
        return count > 0

    def obtener_jugadores(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('SELECT id_usuario, nombre, apellido FROM usuarios')
        jugadores = c.fetchall()
        conn.close()
        return jugadores
