import sqlite3
import pygame
import time
from Logica.control_preguntas import ControlPreguntas

class JuegoIniciado:
    def __init__(self, jugador, dificultad, screen):
        self.jugador = jugador
        self.dificultad = dificultad
        self.screen = screen
        self.puntaje = 0  # Inicializar el puntaje del jugador
        self.aciertos = 0
        self.desaciertos = 0
        self.font = pygame.font.Font(None, 36)  # Fuente para el texto

    def iniciar_juego(self):
        self.temporizador(60)  # Comienza un temporizador de 60 segundos

    def temporizador(self, tiempo_max):
        start_time = time.time()
        while True:
            tiempo_transcurrido = time.time() - start_time
            tiempo_restante = max(tiempo_max - tiempo_transcurrido, 0)

            self.screen.fill((255, 255, 255))  # Limpiar la pantalla
            self.mostrar_informacion_jugador()  # Mostrar información del jugador
            
            # Mover el contador de tiempo restante a la parte inferior izquierda
            self.mostrar_mensaje(f"Tiempo restante: {int(tiempo_restante)} segundos", (20, self.screen.get_height() - 40))

            # Dibujar el botón de pausa
            self.dibujar_boton_pausa()

            pygame.display.flip()  # Actualizar la pantalla

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # Presiona ESC para pausar
                        self.pausa_menu()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if self.boton_pausa_rect.collidepoint(pos):  # Verifica clic en el botón de pausa
                        self.pausa_menu()

            if tiempo_restante <= 0:
                self.mostrar_mensaje("Tiempo agotado!")
                break

    def mostrar_informacion_jugador(self):
        # Información a mostrar
        info_jugador = f"Jugador: {self.jugador}"
        info_dificultad = f"Dificultad: {self.dificultad}"
        info_puntaje = f"Puntaje: {self.puntaje}"
        info_aciertos = f"Aciertos: {self.aciertos}"
        info_desaciertos = f"Desaciertos: {self.desaciertos}"

        # Renderizar el texto
        jugador_surface = self.font.render(info_jugador, True, (0, 0, 0))
        dificultad_surface = self.font.render(info_dificultad, True, (0, 0, 0))
        puntaje_surface = self.font.render(info_puntaje, True, (0, 0, 0))
        aciertos_surface = self.font.render(info_aciertos, True, (0, 0, 0))
        desaciertos_surface = self.font.render(info_desaciertos, True, (0, 0, 0))

        # Posiciones
        left_x = 20
        right_x = self.screen.get_width() - 200  # Ajusta este valor según el ancho que desees para la columna derecha
        top_y = 20

        # Dibujar en la parte izquierda
        self.screen.blit(jugador_surface, (left_x, top_y))
        self.screen.blit(dificultad_surface, (left_x, top_y + 40))  # Espacio de 40px entre líneas

        # Dibujar en la parte derecha
        self.screen.blit(puntaje_surface, (right_x, top_y))
        self.screen.blit(aciertos_surface, (right_x, top_y + 40))
        self.screen.blit(desaciertos_surface, (right_x, top_y + 80))

    def dibujar_boton_pausa(self):
        boton_pausa_ancho, boton_pausa_alto = 80, 30
        # Cambiar la posición a la parte inferior derecha
        self.boton_pausa_rect = pygame.Rect(self.screen.get_width() - boton_pausa_ancho - 20, self.screen.get_height() - boton_pausa_alto - 20, boton_pausa_ancho, boton_pausa_alto)
        pygame.draw.rect(self.screen, (255, 0, 0), self.boton_pausa_rect)  # Color del botón de pausa
        boton_texto = self.font.render("Pausa", True, (255, 255, 255))  # Texto del botón
        self.screen.blit(boton_texto, (self.boton_pausa_rect.x + 5, self.boton_pausa_rect.y + 5))  # Posición del texto

    def pausa_menu(self):
        opciones = [
            "Reanudar",
            "Cambiar dificultad",
            "Cambiar jugador",
            "Volver al menú",
            "Salir"
        ]
        botones_rect = []  # Lista para almacenar los rectángulos de los botones

        # Crear un fondo semitransparente para el menú de pausa
        fondo_menu = pygame.Surface(self.screen.get_size())
        fondo_menu.fill((0, 0, 0))
        fondo_menu.set_alpha(128)  # Ajustar la transparencia (0-255)
        
        while True:
            self.screen.fill((255, 255, 255))  # Limpiar la pantalla
            self.mostrar_informacion_jugador()  # Mostrar info del jugador

            # Mostrar el menú de pausa con fondo
            self.screen.blit(fondo_menu, (0, 0))  # Dibujar el fondo semitransparente
            self.mostrar_mensaje("Juego Pausado. Escoge una opción:")
            for i, opcion in enumerate(opciones):
                # Definir el área del botón
                boton_rect = pygame.Rect(self.screen.get_width() // 2 - 100, self.screen.get_height() // 2 - 50 + i * 40, 200, 30)
                botones_rect.append(boton_rect)

                # Dibujar el botón
                pygame.draw.rect(self.screen, (0, 128, 255), boton_rect)  # Color del botón
                opcion_surface = self.font.render(opcion, True, (255, 255, 255))  # Texto del botón
                self.screen.blit(opcion_surface, (boton_rect.x + 10, boton_rect.y + 5))  # Posición del texto

            pygame.display.flip()  # Actualizar la pantalla

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:  # Reanudar
                        return
                    elif event.key == pygame.K_2:  # Cambiar dificultad
                        self.cambiar_dificultad()
                    elif event.key == pygame.K_3:  # Cambiar jugador
                        self.cambiar_jugador()
                    elif event.key == pygame.K_4:  # Volver al menú
                        # Lógica para volver al menú principal
                        print("Volviendo al menú principal...")
                        return
                    elif event.key == pygame.K_5:  # Salir
                        pygame.quit()
                        exit()
                if event.type == pygame.MOUSEBUTTONDOWN:  # Detectar clic del ratón
                    pos = pygame.mouse.get_pos()
                    for i, boton_rect in enumerate(botones_rect):
                        if boton_rect.collidepoint(pos):  # Comprobar si el clic está dentro del botón
                            if i == 0:  # Reanudar
                                return
                            elif i == 1:  # Cambiar dificultad
                                self.cambiar_dificultad()
                            elif i == 2:  # Cambiar jugador
                                self.cambiar_jugador()
                            elif i == 3:  # Volver al menú
                                print("Volviendo al menú principal...")
                                return
                            elif i == 4:  # Salir
                                pygame.quit()
                                exit()

    def cambiar_dificultad(self):
        nueva_dificultad = input("Introduce la nueva dificultad (baja, media, alta): ")
        self.dificultad = nueva_dificultad
        print(f"Dificultad cambiada a: {self.dificultad}")

    def cambiar_jugador(self):
        nuevo_nombre = input("Introduce el nombre del nuevo jugador: ")
        self.jugador = nuevo_nombre
        print(f"Jugador cambiado a: {self.jugador}")

    def mostrar_mensaje(self, mensaje, posicion=(20, 60)):
        mensaje_text = self.font.render(mensaje, True, (0, 0, 0))  # Renderizar el mensaje
        self.screen.blit(mensaje_text, posicion)  # Dibujar el mensaje
    
