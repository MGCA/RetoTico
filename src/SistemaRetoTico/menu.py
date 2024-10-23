import pygame
import sys
from Logica.registrar_jugador import RegistrarJugador
from Logica.seleccionar_jugador import SeleccionarJugador
from Datos.seleccion import Seleccion
from SistemaRetoTico.iniciar import Iniciar

class Menu:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font(None, 36)
        self.options = ["Iniciar", "Jugadores", "Acerca de", "Ajustes", "Políticas de Privacidad", "Salir"]
        self.colors = {"background": (0, 0, 0), "text": (255, 255, 255)}
        self.icons = self.load_icons()

    def load_icons(self):
        """Carga los iconos, redimensiona y almacena en un diccionario."""
        icon_files = ["src/assets/icons/iniciar.png", "src/assets/icons/jugadores.png", "src/assets/icons/acerca_de.png", "src/assets/icons/ajustes.png", "src/assets/icons/politicas_privacidad.png", "src/assets/icons/salir.png"]
        icons = {}
        size = (40, 40)  # Ajusta el tamaño según sea necesario
        for option, icon_file in zip(self.options, icon_files):
            icon = pygame.image.load(icon_file)
            icon = pygame.transform.scale(icon, size)
            icons[option] = icon
        return icons

    def show(self):
        self.screen.fill(self.colors["background"])
        for i, opcion in enumerate(self.options):
            icon = self.icons[opcion]
            icon_rect = icon.get_rect(center=(self.screen_width // 2, 70 + i * 80))
            self.screen.blit(icon, icon_rect.topleft)

            texto = self.font.render(opcion, True, self.colors["text"])
            text_rect = texto.get_rect(center=(self.screen_width // 2, 100 + i * 80))
            self.screen.blit(texto, text_rect.topleft)

        pygame.display.flip()

    def handle_click(self, pos):
        for i, option in enumerate(self.options):
            y_start = 70 + i * 80 - 20
            y_end = 130 + i * 80
            if y_start <= pos[1] <= y_end:
                if option == "Salir":
                    pygame.quit()
                    sys.exit()  # Asegúrate de salir correctamente
                elif option == "Iniciar":
                    print("Iniciar seleccionado")
                    iniciar = Iniciar(self.screen, self.screen_width, self.screen_height)
                    iniciar.show()
                    running = True
                    while running:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                running = False
                            elif event.type == pygame.MOUSEBUTTONDOWN:
                                iniciar.handle_click(event.pos)
                    pygame.quit()
                elif option == "Jugadores":
                    print("Jugadores seleccionado")
                elif option == "Acerca de":
                    print("Acerca de seleccionado")
                elif option == "Ajustes":
                    print("Ajustes seleccionado")
                elif option == "Políticas de Privacidad":
                    print("Políticas de Privacidad seleccionado")
                else:
                    print(f"{option} seleccionado")
