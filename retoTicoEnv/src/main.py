import pygame
import sys
import os
from SistemaRetoTico.menu import Menu
from configuracion.db_setup import Db_setup
from configuracion.db_insertarDatos import Db_insertarDatos

def get_absolute_path(file_name):
    """Función que devuelve la ruta absoluta a un archivo dado en el directorio 'music'."""
    base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, 'assets', 'music', file_name)

def play_background_music(music_file):
    """Función para cargar y reproducir música de fondo. Maneja errores si el archivo no existe."""
    music_path = get_absolute_path(music_file)
    if os.path.exists(music_path):
        try:
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play(-1)  # Reproducir en bucle infinito
            print(f"Reproduciendo música: {music_file}")
        except pygame.error as e:
            print(f"Error al cargar o reproducir la música: {e}")
    else:
        print(f"Archivo de música no encontrado: {music_path}")

def main():
    # Crear tablas si no existen
    Db_setup.create_tables()
    Db_insertarDatos.insertar_datos()

    pygame.init()
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Menú Principal")

    # Reproducir música de fondo
    play_background_music('nature-reserve.wav')

    menu = Menu(screen, screen_width, screen_height)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                menu.handle_click(event.pos)

        if running:
            menu.show()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
