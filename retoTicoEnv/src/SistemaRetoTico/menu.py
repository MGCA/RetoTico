import pygame
import sys
import os
from Logica.registrar_jugador import RegistrarJugador
from Logica.seleccionar_jugador import SeleccionarJugador
from Datos.seleccion import Seleccion
from SistemaRetoTico.iniciar import Iniciar
from SistemaRetoTico.politicasDePrivacidad import PoliticasDePrivacidad
from configuracion.db_setup import Db_setup
from configuracion.db_insertarDatos import Db_insertarDatos
from Logica.mostrar_jugadores import MostrarJugadores

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
        self.estudiantes = [("Michael Chavarria Alvarado", "5-0415-0045"), ("Estela Artavia Aguilar", "1-1251-0048")]

        Db_setup.create_tables()
        Db_insertarDatos.insertar_datos()

        self.play_background_music('music/nature-reserve.wav')

    def get_icon_path(self, icon_name):
        base_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_path, '..', 'assets', 'icons', icon_name)

    def load_icons(self):
        icon_files = ["iniciar.png", "jugadores.png", "acerca_de.png", "ajustes.png", "politicas_privacidad.png", "salir.png"]
        icons = {}
        size = (40, 40)
        for option, icon_name in zip(self.options, icon_files):
            icon_path = self.get_icon_path(icon_name)
            if os.path.exists(icon_path):
                icon = pygame.image.load(icon_path)
                icon = pygame.transform.scale(icon, size)
                icons[option] = icon
            else:
                print(f"Ícono no encontrado: {icon_path}")
        return icons

    def play_background_music(self, music_file):
        music_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../assets', music_file)
        if os.path.exists(music_path):
            try:
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.play(-1)
                print(f"Reproduciendo música: {music_file}")
            except pygame.error as e:
                print(f"Error al cargar o reproducir la música: {e}")
        else:
            print(f"Archivo de música no encontrado: {music_path}")

    def mostrar_presentacion(self):
        screen_width, screen_height = self.screen.get_size()
        logo = pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../assets', 'img', 'logo.png'))
        logo = pygame.transform.scale(logo, (screen_width, screen_height))
        loading_rect = pygame.Rect(100, screen_height - 100, screen_width - 200, 30)

        for i in range(101):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill(self.colors["background"])
            self.screen.blit(logo, (0, 0))
            pygame.draw.rect(self.screen, (200, 200, 200), loading_rect)
            pygame.draw.rect(self.screen, (0, 255, 0), (loading_rect.x, loading_rect.y, loading_rect.width * i / 100, loading_rect.height))
            pygame.display.flip()
            pygame.time.delay(10)

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
                    self.iniciar_juego()
                elif option == "Jugadores":
                    self.mostrar_jugadores()
                elif option == "Acerca de":
                    self.mostrar_acerca_de()
                elif option == "Ajustes":
                    self.mostrar_ajustes()
                elif option == "Políticas de Privacidad":
                    self.mostrar_politicas_privacidad()

    def iniciar_juego(self):
        iniciar = Iniciar(self.screen, self.screen_width, self.screen_height)
        iniciar.show()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    iniciar.handle_click(event.pos)
            if not running:
                return

    def mostrar_politicas_privacidad(self):
        politicas = PoliticasDePrivacidad(self.screen, "RetoTico", self.estudiantes)
        politicas.mostrar_politicas()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        waiting = False
        self.show()

    def mostrar_jugadores(self):
        mostrar_jugadores = MostrarJugadores(self.screen, self.screen_width, self.screen_height)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mostrar_jugadores.handle_click(event.pos)
            mostrar_jugadores.show()

    def mostrar_acerca_de(self):
        print("Acerca de: Esta es la aplicación RetoTico...")

    def mostrar_ajustes(self):
        print("Mostrando ajustes...")
