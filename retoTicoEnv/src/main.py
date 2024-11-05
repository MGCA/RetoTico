import pygame
import sys
import os
from SistemaRetoTico.menu import Menu
from configuracion.db_setup import Db_setup
from configuracion.db_insertarDatos import Db_insertarDatos


def get_absolute_path(file_name):
    """Función que devuelve la ruta absoluta a un archivo dado en el directorio 'assets'."""
    base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, 'assets', file_name)

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

def mostrar_presentacion(screen):
    """Muestra una pantalla de presentación con un logo y una barra de carga."""
    logo = pygame.image.load(get_absolute_path('img/logo.png'))  # Cargar tu logo aquí
    logo = pygame.transform.scale(logo, (screen.get_width(), screen.get_height()))  # Ajustar el tamaño del logo a la ventana
    loading_rect = pygame.Rect(100, screen.get_height() - 100, screen.get_width() - 200, 30)

    # Simulación de carga (puedes reemplazarlo con lógica de carga real)
    for i in range(101):  # 0 a 100
        screen.fill((255, 255, 255))  # Limpiar la pantalla
        screen.blit(logo, (0, 0))  # Dibujar el logo ajustado

        # Dibujar la barra de carga
        pygame.draw.rect(screen, (200, 200, 200), loading_rect)  # Fondo de la barra
        pygame.draw.rect(screen, (0, 255, 0), (loading_rect.x, loading_rect.y, loading_rect.width * i / 100, loading_rect.height))  # Progreso de la barra

        pygame.display.flip()  # Actualizar la pantalla
        pygame.time.delay(50)  # Esperar un poco para simular el tiempo de carga


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
    play_background_music('music/nature-reserve.wav')

    # Mostrar presentación
    mostrar_presentacion(screen)

    # Iniciar el menú
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
