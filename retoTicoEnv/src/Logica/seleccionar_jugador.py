import pygame
import sys
from Datos.seleccion import Seleccion
from Logica.registrar_jugador import RegistrarJugador
from Logica.juego_iniciado import JuegoIniciado  # Asegúrate de que la ruta de importación sea correcta

class SeleccionarJugador:
    def __init__(self, screen, screen_width, screen_height):
        pygame.display.set_caption("Seleccion de Jugador")
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font(None, 36)
        self.seleccion = Seleccion()
        self.jugadores = self.seleccion.obtener_jugadores()
        self.buttons = self.create_buttons()
        self.dificultad = "media"  # Ejemplo de dificultad; esto puede cambiarse según tu lógica
        self.categoria = 2

    def create_buttons(self):
        return {
            "Volver": pygame.Rect(self.screen_width // 2 - 150, self.screen_height - 100, 100, 50),
            "Registrar Nuevo": pygame.Rect(self.screen_width // 2 + 50, self.screen_height - 100, 150, 50)
        }

    def seleccion_jugador(self):
        if not self.jugadores:
            print("No hay jugadores registrados.")
            return "No hay jugadores"

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.buttons["Volver"].collidepoint(event.pos):
                        self.volver_a_inicio()
                        running = False
                    elif self.buttons["Registrar Nuevo"].collidepoint(event.pos):
                        self.registrar_nuevo_jugador()
                        running = False
                    for jugador in self.jugadores:
                        jugador_rect = pygame.Rect(200, 100 + self.jugadores.index(jugador) * 50, 400, 40)
                        if jugador_rect.collidepoint(event.pos):
                            self.iniciar_juego(jugador)  # Inicia el juego con el jugador seleccionado

            self.renderizar_jugadores()
            pygame.display.flip()

    def iniciar_juego(self, jugador):
        print(f"Jugador seleccionado: {jugador[1]} {jugador[2]}")
        juego = JuegoIniciado(jugador, self.dificultad, self.categoria, self.screen, self.screen_width, self.screen_height)  # Pasar las dimensiones
        juego.iniciar_juego()  # Inicia el juego

    def renderizar_jugadores(self):
        self.screen.fill((0, 0, 0))
        for jugador in self.jugadores:
            jugador_surface = self.font.render(f"{jugador[1]} {jugador[2]}", True, (255, 255, 255))
            jugador_rect = pygame.Rect(200, 100 + self.jugadores.index(jugador) * 50, 400, 40)
            self.screen.blit(jugador_surface, (jugador_rect.x, jugador_rect.y))
            pygame.draw.rect(self.screen, (255, 255, 255), jugador_rect, 2)

        for text, rect in self.buttons.items():
            pygame.draw.rect(self.screen, (255, 255, 255), rect, 2)
            btn_text = self.font.render(text, True, (255, 255, 255))
            self.screen.blit(btn_text, (rect.x + 10, rect.y + 10))

    def volver_a_inicio(self):
        # Implementa la lógica para regresar al menú principal aquí
        print("Volver al menú principal")
        from SistemaRetoTico.menu import Menu  # Import Menu here to avoid circular import issues
        menu = Menu(self.screen, self.screen_width, self.screen_height)
        menu.show()
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    menu.handle_click(event.pos)
                    
        pygame.quit()

    def registrar_nuevo_jugador(self):
        registrar_jugador = RegistrarJugador(self.screen, self.screen_width, self.screen_height)
        registrar_jugador.get_user_data()