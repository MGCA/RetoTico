import sqlite3
import time

class ControlPreguntas:
    @staticmethod
    def obtener_preguntas_aleatorias(dificultad, cantidad=2):
        conn = sqlite3.connect('retotico.db')
        c = conn.cursor()

        # Selecciona preguntas aleatorias de la base de datos según la dificultad
        try:
            c.execute("SELECT * FROM preguntas WHERE nivel_dificultad = ? ORDER BY RANDOM() LIMIT ?", (dificultad, cantidad))
            preguntas = c.fetchall()
            
            # Verificar si se obtuvieron preguntas
            if not preguntas:
                print(f"No se encontraron preguntas para la dificultad: {dificultad}")
                return []  # Retorna una lista vacía si no hay preguntas

            preguntas_y_respuestas = []
            
            for pregunta in preguntas:
                c.execute("SELECT * FROM respuestas WHERE id_pregunta = ?", (pregunta[0],))
                respuestas = c.fetchall()
                
                # Verifica si se encontraron respuestas para la pregunta
                if not respuestas:
                    print(f"No se encontraron respuestas para la pregunta: {pregunta[1]}")  # Asumiendo que pregunta[1] es el texto de la pregunta
                    continue  # Salta a la siguiente pregunta
                
                preguntas_y_respuestas.append((pregunta, respuestas))

            # Print de la lista de preguntas y respuestas
            print("Preguntas obtenidas:")
            for idx, (pregunta, respuestas) in enumerate(preguntas_y_respuestas):
                print(f"Pregunta {idx + 1}: {pregunta[1]}")  # Suponiendo que pregunta[1] es el texto de la pregunta
                print("Respuestas:")
                for respuesta in respuestas:
                    print(f"- {respuesta[1]} (Correcta: {'Sí' if respuesta[2] == 1 else 'No'})")  # Suponiendo que respuesta[2] indica si es correcta

            return preguntas_y_respuestas  # Retorna una lista de tuplas (pregunta, respuestas)

        except sqlite3.Error as e:
            print(f"Error al acceder a la base de datos: {e}")
            return []

        finally:
            conn.close()  # Asegúrate de cerrar la conexión

    @staticmethod
    def controlar_tiempo_y_respuesta(respuestas, dificultad):
        tiempos = {"baja": 200, "media": 150, "alta": 100}
        tiempo_max = tiempos.get(dificultad, 20)  # Valor por defecto en caso de que la dificultad no exista

        print(f"Tienes {tiempo_max} segundos para responder.")
        inicio = time.time()

        # Muestra las respuestas al usuario y le pide que seleccione
        for index, respuesta in enumerate(respuestas):
            print(f"{index + 1}: {respuesta[1]}")  # Suponiendo que la segunda columna es el texto de la respuesta

        try:
            respuesta_jugador = int(input("Tu respuesta: ")) - 1
            
            tiempo_transcurrido = time.time() - inicio
            if tiempo_transcurrido > tiempo_max:
                print("Tiempo agotado.")
                return False
            
            # Verifica si la respuesta es correcta
            return respuestas[respuesta_jugador][2] == 1  # Devuelve True si la respuesta es correcta

        except (ValueError, IndexError):
            print("Entrada inválida. Asegúrate de ingresar un número de respuesta válido.")
            return False
