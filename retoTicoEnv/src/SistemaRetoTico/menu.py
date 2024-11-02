import pygame
import sys
import os
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

    def get_icon_path(self, icon_name):
        """Devuelve la ruta completa del archivo de ícono."""
        base_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_path, '..', 'assets', 'icons', icon_name)

    def load_icons(self):
        """Carga los íconos necesarios para el menú."""
        icon_files = ["iniciar.png", "jugadores.png", "acerca_de.png", "ajustes.png", "politicas_privacidad.png", "salir.png"]
        icons = {}
        size = (40, 40)  # Ajusta el tamaño de los íconos según sea necesario
        for option, icon_name in zip(self.options, icon_files):
            icon_path = self.get_icon_path(icon_name)
            if os.path.exists(icon_path):
                icon = pygame.image.load(icon_path)
                icon = pygame.transform.scale(icon, size)
                icons[option] = icon
            else:
                print(f"Ícono no encontrado: {icon_path}")
        return icons

    def show(self):
        self.screen.fill(self.colors["background"])
        for i, opcion in enumerate(self.options):
            icon = self.icons.get(opcion)
            if icon:
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
                    sys.exit()
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
