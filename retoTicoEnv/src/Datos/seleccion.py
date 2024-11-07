import sqlite3
import random


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
    

    def obtener_preguntas(self, dificultad, categoria):
        """Obtiene preguntas con cuatro respuestas (incluyendo siempre la correcta) en función de la categoría y dificultad, con la imagen si existe."""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()

        try:
            # Seleccionar todas las preguntas con sus posibles respuestas y otros datos necesarios
            query = '''SELECT p.id_pregunta, p.pregunta, i.ruta_imagen,
                            r.id_respuesta, r.respuesta, r.es_correcta
                        FROM preguntas p
                        LEFT JOIN imagenes i ON p.id_pregunta = i.id_pregunta
                        JOIN respuestas r ON p.id_pregunta = r.id_pregunta
                        WHERE 1=1'''
            
            params = []
            if dificultad:
                query += " AND p.nivel_dificultad = ?"
                params.append(dificultad)
            if categoria:
                query += " AND p.id_categoria = ?"
                params.append(categoria)

            c.execute(query, params)
            datos = c.fetchall()

            # Si no hay preguntas encontradas, retornar una lista vacía
            if not datos:
                print("No se encontraron preguntas para los filtros dados.")
                return []

            preguntas_info = {}

            # Agrupar respuestas por id_pregunta
            for row in datos:
                id_pregunta, texto_pregunta, ruta_imagen, id_respuesta, texto_respuesta, es_correcta = row

                # Crear entrada de la pregunta si no existe en el diccionario
                if id_pregunta not in preguntas_info:
                    preguntas_info[id_pregunta] = {
                        "id_pregunta": id_pregunta,
                        "pregunta": texto_pregunta,
                        "respuestas": [],
                        "ruta_imagen": ruta_imagen if ruta_imagen else None
                    }

                # Añadir respuesta a la lista de respuestas de la pregunta
                preguntas_info[id_pregunta]["respuestas"].append({
                    "id_respuesta": id_respuesta,
                    "respuesta": texto_respuesta,
                    "es_correcta": bool(es_correcta)
                })

            preguntas_final = []

            # Procesar cada pregunta para incluir exactamente 4 respuestas
            for pregunta in preguntas_info.values():
                # Obtener la respuesta correcta y respuestas incorrectas
                respuestas_correctas = [r for r in pregunta["respuestas"] if r["es_correcta"]]
                respuestas_incorrectas = [r for r in pregunta["respuestas"] if not r["es_correcta"]]

                if respuestas_correctas:
                    respuesta_correcta = respuestas_correctas[0]  # Tomar la única respuesta correcta
                    # Seleccionar aleatoriamente tres respuestas incorrectas
                    if len(respuestas_incorrectas) >= 3:
                        respuestas_seleccionadas = random.sample(respuestas_incorrectas, 3)
                    else:
                        respuestas_seleccionadas = respuestas_incorrectas  # Si hay menos de 3, usar las disponibles
                    
                    # Añadir la respuesta correcta a la lista de respuestas seleccionadas
                    respuestas_seleccionadas.append(respuesta_correcta)
                    # Mezclar las respuestas para que la correcta no esté siempre en la misma posición
                    random.shuffle(respuestas_seleccionadas)

                    # Actualizar las respuestas de la pregunta con las seleccionadas
                    pregunta["respuestas"] = respuestas_seleccionadas
                    preguntas_final.append(pregunta)

            return preguntas_final

        finally:
            # Asegurarse de cerrar la conexión en cualquier caso
            conn.close()


