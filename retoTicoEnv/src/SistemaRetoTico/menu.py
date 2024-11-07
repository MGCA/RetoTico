import pygame
import sys
import os
from Logica.registrar_jugador import RegistrarJugador
from Logica.seleccionar_jugador import SeleccionarJugador
from Datos.seleccion import Seleccion
from SistemaRetoTico.iniciar import Iniciar
from SistemaRetoTico.politicasDePrivacidad import PoliticasDePrivacidad  # Asegúrate de importar tu clase

class Menu:
    def __init__(self, screen, screen_width, screen_height):
        pygame.display.set_caption("Menu Principal")
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font(None, 36)
        self.options = ["Iniciar", "Jugadores", "Acerca de", "Ajustes", "Políticas de Privacidad", "Salir"]
        self.colors = {"background": (0, 0, 0), "text": (255, 255, 255)}
        self.icons = self.load_icons()
        self.estudiantes = [("Michael Chavarria Alvarado", "5-0415-0045"), ("Estela Artavia Aguilar", "0-0000-0000")]  # Agrega tus estudiantes aquí

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
                    self.iniciar_juego()  # Llama al método separado
                elif option == "Jugadores":
                    print("Jugadores seleccionado")
                elif option == "Acerca de":
                    print("Acerca de seleccionado")
                elif option == "Ajustes":
                    print("Ajustes seleccionado")
                elif option == "Políticas de Privacidad":
                    print("Políticas de Privacidad seleccionado")
                    self.mostrar_politicas_privacidad()
                else:
                    print(f"{option} seleccionado")

    def iniciar_juego(self):
        """Inicia el juego creando una instancia de Iniciar y manejando su bucle de eventos."""
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

    def mostrar_politicas_privacidad(self):
        # Aquí se corrige el número de argumentos pasados al constructor
        politicas = PoliticasDePrivacidad(self.screen, "RetoTico", self.estudiantes)
        politicas.mostrar_politicas()

        # Pausar para ver las políticas
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Presiona Enter para continuar
                        waiting = False

        # Regresar al menú después de ver las políticas
        self.show()