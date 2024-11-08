import pygame
import sys
from Datos.seleccion import Seleccion
from Logica.registrar_jugador import RegistrarJugador
from Logica.juego import Juego  # Asegúrate de que la ruta de importación sea correcta

class SeleccionarJugador:
    def __init__(self, screen, screen_width, screen_height):
        pygame.init()
        pygame.display.set_caption("Selección de Jugador")
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font(None, 36)
        self.seleccion = Seleccion()
        self.jugadores = self.seleccion.obtener_jugadores()  # Obtener jugadores registrados
        self.buttons = self.create_buttons()
        self.dificultad = "media"  # Ejemplo de dificultad; esto puede cambiarse según tu lógica
        self.categoria = 2
        
        # Optimización: renderizamos el texto de los jugadores al inicializar
        self.jugador_surfaces = self.preparar_jugadores_surfaces()

    def preparar_jugadores_surfaces(self):
        """Pre-renderiza el texto de cada jugador y sus rectángulos una sola vez."""
        surfaces = []
        for idx, jugador in enumerate(self.jugadores):
            jugador_text = f"{jugador[1]} {jugador[2]}"
            jugador_surface = self.font.render(jugador_text, True, (255, 255, 255))
            jugador_rect = pygame.Rect(200, 100 + idx * 50, 400, 40)
            surfaces.append((jugador_surface, jugador_rect))
        return surfaces

    def create_buttons(self):
        return {
            "Volver": pygame.Rect(self.screen_width // 2 - 150, self.screen_height - 100, 100, 50),
            "Registrar Nuevo": pygame.Rect(self.screen_width // 2 + 50, self.screen_height - 100, 150, 50)
        }

    def renderizar_jugadores(self):
        """Dibuja la pantalla de selección de jugadores, incluyendo botones."""
        if not pygame.display.get_init():
            return

        self.screen.fill((0, 0, 0))  # Limpiar pantalla

        # Dibujar jugadores (usando superficies pre-renderizadas)
        for jugador_surface, jugador_rect in self.jugador_surfaces:
            self.screen.blit(jugador_surface, jugador_rect)
            pygame.draw.rect(self.screen, (255, 255, 255), jugador_rect, 2)

        # Dibujar botones
        self.renderizar_botones()

    def renderizar_botones(self):
        """Dibuja los botones de acción en la pantalla."""
        for text, rect in self.buttons.items():
            pygame.draw.rect(self.screen, (255, 255, 255), rect, 2)
            btn_text = self.font.render(text, True, (255, 255, 255))
            self.screen.blit(btn_text, (rect.x + 10, rect.y + 10))


    def obtener_lista_de_jugadores(self):
        # Aquí se devuelve la lista de jugadores, ya implementada en tu clase `Seleccion`
        return self.jugadores

    def iniciar_juego(self, jugador):
        """Inicia el juego con el jugador seleccionado."""
        print(f"Jugador seleccionado: {jugador[1]} {jugador[2]}")
        juego = Juego(jugador, self.dificultad, self.categoria, self.screen, self.screen_width, self.screen_height)
        
        # Ejecuta el juego y regresa al menú al terminar
        while True:
            juego_terminado = juego.ejecutar()  # Asegúrate de que `ejecutar` devuelve True si el juego termina o el jugador elige salir
            
            if juego_terminado:
                print("Juego terminado. Regresando al menú principal.")
                self.volver_a_inicio()  # Llamar al método para regresar al menú principal
                break

    def seleccion_jugador(self):
        """Selecciona un jugador y maneja la navegación al juego o menú."""
        if not self.obtener_lista_de_jugadores():
            print("No hay jugadores registrados.")
            self.registrar_nuevo_jugador()
            return "No hay jugadores"

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.volver_a_inicio()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.buttons["Volver"].collidepoint(event.pos):
                        running = False
                        self.volver_a_inicio()
                    elif self.buttons["Registrar Nuevo"].collidepoint(event.pos):
                        self.registrar_nuevo_jugador()
                    for jugador in self.jugadores:
                        jugador_rect = pygame.Rect(200, 100 + self.jugadores.index(jugador) * 50, 400, 40)
                        if jugador_rect.collidepoint(event.pos):
                            running = False
                            self.iniciar_juego(jugador)

            if running:
                self.renderizar_jugadores()
                pygame.display.flip()

    def volver_a_inicio(self):
        """Muestra el menú principal sin cerrar la aplicación."""
        print("Volver al menú principal")
        from SistemaRetoTico.menu import Menu  # Importa el menú aquí para evitar importaciones circulares
        menu = Menu(self.screen, self.screen_width, self.screen_height)
        menu.show()


    def registrar_nuevo_jugador(self):
        registrar_jugador = RegistrarJugador(self.screen, self.screen_width, self.screen_height)
        registrar_jugador.get_user_data()
