import pygame
from Logica.controlador_juego import ControladorJuego

class Juego:
    def __init__(self, jugador, dificultad, categoria, pantalla, ancho_pantalla, alto_pantalla):
        pygame.display.set_caption("Juego Iniciado")
        self.controlador = ControladorJuego(jugador, dificultad, categoria, pantalla, ancho_pantalla, alto_pantalla)
        self.juego_pausado = False  # Variable para controlar si el juego está pausado
        
    def ejecutar(self):
        """Ejecuta el bucle principal del juego y regresa al menú al finalizar."""
        ejecutando = True
        
        while ejecutando:
            eventos = pygame.event.get()
            
            for evento in eventos:
                if evento.type == pygame.QUIT:
                    # Salimos del juego y regresamos al menú
                    return True  
                
                # Manejar el evento de pausa
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_p:  # Pausar o reanudar con la tecla 'P'
                        self.juego_pausado = not self.juego_pausado
            
            if self.juego_pausado:
                # Mostrar la pantalla de pausa
                self.controlador.mostrar_pantalla_pausa()
                # Manejar eventos de clic en los botones de la pantalla de pausa
                self.controlador.manejar_eventos_pausa(eventos)
            else:
                # Actualizar el estado del juego si no está en pausa
                if self.controlador.actualizar(eventos):
                    # El juego ha terminado, regresamos al menú
                    return True  
            
            pygame.display.flip()  # Actualizar la pantalla principal
        
        # Devolvemos True para indicar que el juego terminó normalmente
        return True  
