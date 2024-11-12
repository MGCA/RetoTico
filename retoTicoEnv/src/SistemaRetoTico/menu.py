import pygame
import sys
import os
import subprocess
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
        # Cambiar el ícono de la ventana
        base_path = os.path.dirname(os.path.abspath(__file__))
        icons_folder = os.path.join(base_path, '..', 'assets', 'icons/icon64x64.ico')
        icon = pygame.image.load(icons_folder)
        pygame.display.set_icon(icon)  # Establece el ícono de la ventana
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.title_font = pygame.font.SysFont('Arial', 54)  # Cambiar a fuente predeterminada
        self.font = pygame.font.Font(None, 36)
        self.options = ["Iniciar", "Jugadores", "Acerca de", "Ajustes", "Políticas de Privacidad", "Salir"]
        self.colors = {"background": (0, 0, 0), "text": (255, 255, 255)}
        self.icons = self.load_icons()
        self.estudiantes = [("Michael Chavarria Alvarado", "5-0415-0045"), ("Estela Artavia Aguilar", "1-1251-0048")]
        self.music_on = True  # Variable para controlar el estado de la música
        self.play_background_music('music/nature-reserve.wav')
        
        
        # Inicializar BD solo una vez
        Db_setup.create_tables()
        Db_insertarDatos.insertar_datos()

    def get_icon_path(self, icon_name):
        base_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_path, '..', 'assets', 'icons', icon_name)

    def load_icons(self):
        icon_files = ["iniciar.png", "jugadores.png", "acerca_de.png", "ajustes.png", "politicas_privacidad.png", "salir.png"]
        icons = {}
        size = (40, 40)
        base_path = os.path.dirname(os.path.abspath(__file__))
        icons_folder = os.path.join(base_path, '..', 'assets', 'icons')

        for option, icon_name in zip(self.options, icon_files):
            icon_path = os.path.join(icons_folder, icon_name)
            if os.path.exists(icon_path):
                try:
                    icon = pygame.image.load(icon_path)
                    icon = pygame.transform.scale(icon, size)
                    icons[option] = icon
                except pygame.error as e:
                    print(f"Error al cargar el icono {icon_name}: {e}")
            else:
                print(f"Ícono no encontrado: {icon_path}")
        return icons

    def play_background_music(self, music_file):
        music_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../assets', music_file)
        if os.path.exists(music_path):
            try:
                pygame.mixer.music.load(music_path)
                if self.music_on:
                    pygame.mixer.music.play(-1)
                print(f"Reproduciendo música: {music_file}")
            except pygame.error as e:
                print(f"Error al cargar o reproducir la música: {e}")
        else:
            print(f"Archivo de música no encontrado: {music_path}")

    def show_music_switch(self):
        # Dibuja el ícono del switch de música en la esquina superior derecha
        switch_text = "Sonido ON" if self.music_on else "Sonido OFF"
        text_color = (0, 255, 0) if self.music_on else (255, 0, 0)
        switch_surface = self.font.render(switch_text, True, text_color)
        switch_rect = switch_surface.get_rect(topright=(self.screen_width - 20, 20))
        self.screen.blit(switch_surface, switch_rect)
        return switch_rect

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
            pygame.time.delay(50)

    def toggle_music(self):
        if self.music_on:
            pygame.mixer.music.stop()
        else:
            pygame.mixer.music.play(-1)
        self.music_on = not self.music_on
        self.show()  # Redibujar el menú inmediatamente después de alternar

    def handle_events(self, event):
        # Detectar si se hizo clic en el área del switch
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.show_music_switch().collidepoint(event.pos):
                self.toggle_music()

    def show(self):
        self.screen.fill(self.colors["background"])
        # Actualizar el switch de sonido
        self.show_music_switch()
        
        # Mostrar el logo y título
        icon = pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../assets', 'img', 'icon.png'))
        icon = pygame.transform.scale(icon, (100, 100))  
        logo_rect = icon.get_rect(center=(self.screen_width // 2, 50))  
        self.screen.blit(icon, logo_rect)

        try:
            titulo_texto = self.title_font.render("RetoTico", True, self.colors["text"])
            titulo_rect = titulo_texto.get_rect(center=(self.screen_width // 2, logo_rect.bottom + 10))
            self.screen.blit(titulo_texto, titulo_rect)
        except Exception as e:
            print(f"Error al renderizar el texto: {e}")

        espacio_entre_titulo_y_opciones = 100

        for i, opcion in enumerate(self.options):
            icon = self.icons.get(opcion)
            if icon:
                icon_rect = icon.get_rect(center=(self.screen_width // 2, logo_rect.bottom + espacio_entre_titulo_y_opciones + i * 80))
                self.screen.blit(icon, icon_rect.topleft)

            texto = self.font.render(opcion, True, self.colors["text"])
            text_rect = texto.get_rect(center=(self.screen_width // 2, logo_rect.bottom + espacio_entre_titulo_y_opciones + 30 + i * 80))
            self.screen.blit(texto, text_rect.topleft)

        pygame.display.flip()

    def handle_click(self, pos):
        for i, option in enumerate(self.options):
            y_start = 170 + i * 80 - 20
            y_end = 230 + i * 80
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
        if not pygame.display.get_init():  # Verifica si Pygame ha sido inicializado
            print("Pygame no está inicializado. No se puede mostrar las políticas.")
            return

        politicas = PoliticasDePrivacidad(self.screen, "RetoTico", self.estudiantes)
        politicas.mostrar_politicas()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    pygame.quit()  # Asegúrate de cerrar Pygame aquí
                    sys.exit()  # Salir del programa correctamente
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        waiting = False

        # Después de que se cierre el cuadro de políticas, vuelve al menú solo si Pygame sigue activo
        if pygame.display.get_init():
            self.show()  # Mostrar el menú principal nuevamente

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
        # Ruta del archivo README.md
        readme_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'doc', 'README.md')
        
        try:
            # Comprobamos que el archivo existe
            if os.path.exists(readme_path):
                # Para Windows, intentamos abrir con el Bloc de notas
                subprocess.Popen(['notepad', readme_path])
                print("Abriendo el archivo README.md en el Bloc de notas.")
            else:
                print("Archivo README.md no encontrado en:", readme_path)
            
        except Exception as e:
            print(f"Error al intentar abrir el archivo: {e}")

    def mostrar_ajustes(self):
        print("Mostrando ajustes...")
