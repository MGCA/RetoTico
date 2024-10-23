import sqlite3

class Insercion:
    def __init__(self, db_name='retotico.db'):
        self.db_name = db_name

    def insertar_usuario(self, user_data):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()

        c.execute('''
        INSERT INTO usuarios (nombre, apellido, edad, provincia, canton, distrito, numero_whatsapp, correo)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (
            user_data["Nombre:"], user_data["Apellido:"], user_data["Edad:"], 
            user_data["Provincia:"], user_data["Canton:"], user_data["Distrito:"], 
            user_data["Número WhatsApp:"], user_data["Correo:"]
        ))

        conn.commit()
        conn.close()
