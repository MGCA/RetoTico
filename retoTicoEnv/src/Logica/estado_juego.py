# estado_juego.py
class EstadoJuego:
    def __init__(self):
        self.puntaje = 0
        self.respuestas_correctas = 0
        self.respuestas_incorrectas = 0
        self.pregunta_actual = 0
        self.respuesta_seleccionada = None
        self.juego_terminado = False
        self.juego_pausado = False
        self.preguntas_totales = 0
        self.preguntas_restantes = 0