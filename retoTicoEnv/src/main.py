import pygame
import sys
from SistemaRetoTico.menu import Menu
from configuracion.db_setup import Db_setup  # Asegúrate de que el nombre sea correcto

def main():
    pygame.init()

    # Definir el tamaño de la pantalla
    screen_width = 1024
    screen_height = 768
    screen = pygame.display.set_mode((screen_width, screen_height))
    
    # Inicializar la base de datos
    Db_setup.create_tables()  # Llamamos a la función para crear la base de datos e insertar datos

    # Crear el objeto Menu y mostrar la presentación
    menu = Menu(screen, screen_width, screen_height)
    menu.mostrar_presentacion()  # Mostrar la pantalla de carga o presentación
    menu.show()  # Mostrar el menú principal

    # Bucle principal del juego
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Aquí agregamos el manejo del clic
                menu.handle_click(event.pos)

        # Redibujar el menú cada ciclo
        menu.show()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
