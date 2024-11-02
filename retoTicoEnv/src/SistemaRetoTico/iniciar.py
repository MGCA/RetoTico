import pygame
import sys
from Logica.registrar_jugador import RegistrarJugador
from Logica.seleccionar_jugador import SeleccionarJugador

class Iniciar:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font(None, 36)
        self.buttons = self.create_buttons()

    def create_buttons(self):
        return {
            "Seleccionar Jugador": pygame.Rect(self.screen_width // 2 - 150, self.screen_height // 2 - 50, 300, 50),
            "Registrar Nuevo": pygame.Rect(self.screen_width // 2 - 150, self.screen_height // 2 + 20, 300, 50),
            "Volver": pygame.Rect(self.screen_width // 2 - 50, self.screen_height // 2 + 90, 100, 50)
        }

    def show(self):
        self.screen.fill((0, 0, 0))
        for text, rect in self.buttons.items():
            pygame.draw.rect(self.screen, (255, 255, 255), rect, 2)
            btn_text = self.font.render(text, True, (255, 255, 255))
            self.screen.blit(btn_text, (rect.x + 10, rect.y + 10))
        pygame.display.flip()

    def handle_click(self, pos):
        if self.buttons["Seleccionar Jugador"].collidepoint(pos):
            self.seleccionar_jugador()
        elif self.buttons["Registrar Nuevo"].collidepoint(pos):
            self.registrar_jugador()
        elif self.buttons["Volver"].collidepoint(pos):
            self.regresar_menu_principal()

    def seleccionar_jugador(self):
        seleccionar_jugador = SeleccionarJugador(self.screen, self.screen_width, self.screen_height)
        jugador_seleccionado = seleccionar_jugador.seleccion_jugador()
        if jugador_seleccionado:
            print(f"Jugador existente seleccionado: {jugador_seleccionado}")
        else:
            print("No hay jugadores registrados.")

    def registrar_jugador(self):
        registrar_jugador = RegistrarJugador(self.screen, self.screen_width, self.screen_height)
        user_data = registrar_jugador.get_user_data()
        registrar_jugador.guardar_usuario()
        print("Datos del usuario guardados:", user_data)

    def regresar_menu_principal(self):
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
