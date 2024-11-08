import pygame
import sys
from Logica.registrar_jugador import RegistrarJugador
from Logica.seleccionar_jugador import SeleccionarJugador

class Iniciar:
    def __init__(self, screen, screen_width, screen_height):
        pygame.display.set_caption("Iniciar: Selección / Registro")
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font(None, 36)
        self.buttons = self.create_buttons()

    def create_buttons(self):
        return {
            "Seleccionar Jugador": pygame.Rect(self.screen_width // 2 - 150, self.screen_height // 2 - 50, 300, 50),
            "Registrar Nuevo": pygame.Rect(self.screen_width // 2 - 150, self.screen_height // 2 + 20, 300, 50),
            "Volver": pygame.Rect(self.screen_width // 2 - 50, self.screen_height // 2 + 90, 100, 50)
        }

    def show(self):
        running = True
        while running:
            self.screen.fill((0, 0, 0))  # Rellenar la pantalla con negro
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)

            # Dibuja los botones
            for text, rect in self.buttons.items():
                pygame.draw.rect(self.screen, (255, 255, 255), rect, 2)
                btn_text = self.font.render(text, True, (255, 255, 255))
                self.screen.blit(btn_text, (rect.x + 10, rect.y + 10))

            pygame.display.flip()  # Actualizar la pantalla

    def handle_click(self, pos):
        if self.buttons["Seleccionar Jugador"].collidepoint(pos):
            self.seleccionar_jugador()
        elif self.buttons["Registrar Nuevo"].collidepoint(pos):
            self.registrar_jugador()
        elif self.buttons["Volver"].collidepoint(pos):
            self.regresar_menu_principal()

    def seleccionar_jugador(self):
        # Verificamos si hay jugadores registrados (esto puede depender de cómo estés guardando los jugadores)
        # Supondré que tienes una función o una lista de jugadores en tu aplicación
        # que te dice si hay jugadores disponibles o no.
        # Mostrar la pantalla de selección de jugador
        seleccionar_jugador = SeleccionarJugador(self.screen, self.screen_width, self.screen_height)
        
        jugadores_registrados = seleccionar_jugador.obtener_lista_de_jugadores()

        if jugadores_registrados:  # Si hay jugadores registrados
            
            jugador_seleccionado = seleccionar_jugador.seleccion_jugador()

            if jugador_seleccionado != "No hay jugadores":
                print(f"Jugador existente seleccionado: {jugador_seleccionado}")
            else:
                print("No se ha seleccionado un jugador válido.")
        else:
            # Si no hay jugadores registrados, mostramos un mensaje
            print("No hay jugadores registrados. Por favor, registre un jugador primero.")
            # Opcionalmente, puedes redirigir a la pantalla de registro de jugadores:
            self.registrar_jugador()  # Llamar al método de registrar jugador si no hay jugadores

    def registrar_jugador(self):
        registrar_jugador = RegistrarJugador(self.screen, self.screen_width, self.screen_height)
        user_data = registrar_jugador.get_user_data()
        registrar_jugador.guardar_usuario()
        print("Datos del usuario guardados:", user_data)

    def regresar_menu_principal(self):
        print("Volver al menú principal")
        from SistemaRetoTico.menu import Menu  # Import Menu here to avoid circular import issues
        menu = Menu(self.screen, self.screen_width, self.screen_height)
        menu.show()  # Llamamos al menú principal

        # Bucle para mostrar el menú hasta que se cierre
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    menu.handle_click(event.pos)

    def update_screen(self):
        """Método adicional para refrescar la pantalla, si es necesario."""
        self.show()  # Usa el método show() para redibujar la pantalla completa
