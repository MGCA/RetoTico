import pygame
import sys
from Logica.controlador_juego import ControladorJuego
from Logica.estado_juego import EstadoJuego

class Juego:
    def __init__(self, jugador, dificultad, categoria, pantalla, ancho_pantalla, alto_pantalla):
        pygame.init()  # Aseguramos que pygame esté inicializado
        pygame.display.set_caption("Juego Iniciado")
        
        self.pantalla = pantalla  # Pantalla para renderizar el juego
        self.controlador = ControladorJuego(jugador, dificultad, categoria, pantalla, ancho_pantalla, alto_pantalla)
        self.estado = EstadoJuego()  # Estado del juego
    
    def ejecutar(self):
        """Ejecuta el bucle principal del juego y regresa al menú al finalizar."""
        ejecutando = True
        
        while ejecutando:
            eventos = pygame.event.get()
            
            for evento in eventos:
                if evento.type == pygame.QUIT:
                    self.estado.juego_salir = True  # Marcamos que el jugador quiere salir
                    ejecutando = False  # Salimos del bucle
                    pygame.quit()  # Cerramos pygame de manera segura
                    sys.exit()  # Terminamos el programa

                # Manejar el evento de pausa
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_p:  # Pausar o reanudar con la tecla 'P'
                        self.estado.juego_pausado = not self.estado.juego_pausado

            if self.estado.juego_pausado:
                # Mostrar la pantalla de pausa
                self.controlador.mostrar_pantalla_pausa()
                # Manejar eventos de clic en los botones de la pantalla de pausa
                self.controlador.manejar_eventos_pausa(eventos)
            else:
                # Actualizar el estado del juego si no está en pausa
                if self.controlador.actualizar(eventos):
                    # Si el juego ha terminado, actualizar el estado y salir
                    self.estado.juego_terminado = True
                    ejecutando = False

            # Verificar si el juego ha terminado o si el jugador quiere salir
            if self.estado.juego_terminado or self.estado.juego_salir:
                ejecutando = False

            # Actualizar la pantalla principal, asegurándonos de que esté inicializada
            if pygame.display.get_init():
                pygame.display.flip()
            else:
                print("Error: el sistema de video de pygame no está inicializado.")
                return False  # Salimos del bucle si no está inicializado

        # Devolvemos True si el juego terminó normalmente
        return True if self.estado.juego_terminado else False