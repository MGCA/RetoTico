import pygame

class Menu:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font(None, 36)
        self.options = ["Iniciar", "Jugadores", "Acerca de", "Ajustes", "Políticas de Privacidad", "Salir"]
        self.colors = {"background": (0, 0, 0), "text": (255, 255, 255)}

    def show(self):
        self.screen.fill(self.colors["background"])
        for i, opcion in enumerate(self.options):
            texto = self.font.render(opcion, True, self.colors["text"])
            self.screen.blit(texto, (self.screen_width // 2 - texto.get_width() // 2, 100 + i * 50))
        pygame.display.flip()

    def handle_click(self, pos):
        for i, option in enumerate(self.options):
            y_start = 100 + i * 50
            y_end = y_start + 50
            if y_start <= pos[1] <= y_end:
                print(f"{option} seleccionado")
                if option == "Salir":
                    pygame.quit()
                    sys.exit()

