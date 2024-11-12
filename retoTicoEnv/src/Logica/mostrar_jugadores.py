import pygame
from Datos.seleccion import Seleccion

class MostrarJugadores:
    def __init__(self, screen, screen_width, screen_height):
        pygame.display.set_caption("Lista de Jugadores")
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font(None, 36)
        self.seleccion = Seleccion()  # Instancia para obtener jugadores

        # Variables para manejar la pantalla actual (lista o historial)
        self.estado = "lista"  # Estado inicial para mostrar la lista de jugadores
        self.jugadores = []
        self.historial = {}

        # Cargar los jugadores en el menú
        self.mostrar_lista_jugadores()

    def mostrar_lista_jugadores(self):
        """ Obtiene la lista de jugadores y prepara los botones para cada uno """
        self.jugadores = [list(jugador) for jugador in self.seleccion.obtener_jugadores()]

    def mostrar_historial(self, id_usuario):
        """ Muestra el historial del jugador seleccionado """
        self.historial[id_usuario] = self.seleccion.obtener_historial_juegos(id_usuario)
        self.estado = "historial"  # Cambia el estado a historial

    def dibujar_lista_jugadores(self):
        """ Dibuja la lista de jugadores con su botón de 'Volver al Menú' """
        self.screen.fill((0, 0, 0))

        # Mostrar el título
        title_text = self.font.render("Lista de Jugadores", True, (255, 255, 255))
        self.screen.blit(title_text, (self.screen_width // 2 - title_text.get_width() // 2, 20))

        # Dibujar los botones para cada jugador
        button_height = 50
        for idx, jugador in enumerate(self.jugadores):
            nombre = f"{jugador[1]} {jugador[2]}"
            button_text = self.font.render(nombre, True, (255, 255, 255))
            button_rect = pygame.Rect(self.screen_width // 2 - button_text.get_width() // 2 - 10, 100 + idx * (button_height + 10), button_text.get_width() + 20, button_height)
            pygame.draw.rect(self.screen, (0, 0, 255), button_rect)
            self.screen.blit(button_text, (button_rect.x + 10, button_rect.y + (button_height - button_text.get_height()) // 2))

            # Almacenar el botón en el jugador para manejar clics
            jugador.append(button_rect)

        # Botón "Volver al Menú"
        volver_menu_button = pygame.Rect(self.screen_width // 2 - 100, self.screen_height - 80, 200, 50)
        pygame.draw.rect(self.screen, (255, 0, 0), volver_menu_button)
        volver_menu_text = self.font.render("Volver al Menú", True, (255, 255, 255))
        # Centramos el texto en el botón
        text_rect = volver_menu_text.get_rect(center=volver_menu_button.center)
        self.screen.blit(volver_menu_text, text_rect.topleft)
        self.volver_menu_button = volver_menu_button  # Guardar el botón para gestionar clics

        pygame.display.flip()

    def dibujar_historial(self):
        """ Dibuja el historial de juegos del jugador seleccionado con su botón 'Volver a la Lista de Jugadores' """
        self.screen.fill((0, 0, 0))

        # Mostrar el título
        title_text = self.font.render("Historial de Juegos", True, (255, 255, 255))
        self.screen.blit(title_text, (self.screen_width // 2 - title_text.get_width() // 2, 20))

        # Mostrar el historial de juegos
        jugador_id = list(self.historial.keys())[0] if self.historial else None
        if jugador_id:
            historial = self.historial[jugador_id]
            for idx, juego in enumerate(historial):
                fecha, puntos = juego
                game_text = self.font.render(f"Fecha: {fecha}, Puntos: {puntos}", True, (255, 255, 255))
                self.screen.blit(game_text, (self.screen_width // 2 - game_text.get_width() // 2, 100 + idx * 40))

        # Botón "Volver a la Lista de Jugadores"
        volver_lista_button = pygame.Rect(self.screen_width // 2 - 100, self.screen_height - 80, 200, 50)
        pygame.draw.rect(self.screen, (255, 0, 0), volver_lista_button)
        volver_lista_text = self.font.render("Volver a la Lista", True, (255, 255, 255))
        text_rect = volver_lista_text.get_rect(center=volver_lista_button.center)
        self.screen.blit(volver_lista_text, text_rect.topleft)
        self.volver_lista_button = volver_lista_button  # Guardar el botón para gestionar clics

        pygame.display.flip()

    def handle_click(self, pos):
        """ Gestiona los clics en los botones de jugadores o en 'Volver' """
        if self.estado == "lista":
            if self.volver_menu_button.collidepoint(pos):
                print("Volviendo al menú principal...")
                from SistemaRetoTico.menu import Menu
                menu = Menu(self.screen, self.screen_width, self.screen_height)
                menu.show()
                running = True
                while running:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                            #sys.exit()
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            menu.handle_events(event)
                            menu.handle_click(event.pos)
            else:
                for jugador in self.jugadores:
                    button_rect = jugador[-1]
                    if button_rect.collidepoint(pos):
                        self.mostrar_historial(jugador[0])
        elif self.estado == "historial":
            if self.volver_lista_button.collidepoint(pos):
                self.estado = "lista"
                self.historial.clear()  # Limpiar el historial al volver a la lista de jugadores


    def show(self):
        """ Método para dibujar la pantalla en base al estado actual """
        if self.estado == "lista":
            self.dibujar_lista_jugadores()
        elif self.estado == "historial":
            self.dibujar_historial()

