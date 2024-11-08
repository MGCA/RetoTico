# gestor_preguntas.py
class GestorPreguntas:
    def __init__(self, dificultad, categoria):
        self.dificultad = dificultad
        self.categoria = categoria
        self.preguntas = self.obtener_preguntas()
    
    def obtener_preguntas(self):
        from Datos.seleccion import Seleccion
        contenedor = Seleccion()
        preguntas = []
        
        info_preguntas = contenedor.obtener_preguntas(self.dificultad, self.categoria)
        
        if isinstance(info_preguntas, list) and info_preguntas:
            for p in info_preguntas:
                try:
                    indice_correcto = next(i for i, r in enumerate(p["respuestas"]) if r["es_correcta"])
                    preguntas.append({
                        "idPregunta": p["id_pregunta"],
                        "pregunta": p["pregunta"],
                        "opciones": [r["respuesta"] for r in p["respuestas"]],
                        "correcta": indice_correcto
                    })
                except StopIteration:
                    print(f"No se encontró respuesta correcta para pregunta {p['id_pregunta']}")
                    
        return preguntas

    def obtener_pregunta_actual(self, indice_actual):
        return self.preguntas[indice_actual] if indice_actual < len(self.preguntas) else None
