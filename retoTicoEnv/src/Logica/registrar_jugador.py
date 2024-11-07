import pygame
import sys
from Datos.insercion import Insercion

class RegistrarJugador:
    def __init__(self, screen, screen_width, screen_height):
        pygame.display.set_caption("Registrar Jugador")
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font(None, 36)
        self.input_boxes = []
        self.active_input = None
        self.buttons = self.create_buttons()
        self.prompts = ["Nombre:", "Apellido:", "Edad:", "Provincia:", "Canton:", "Distrito:", "Número WhatsApp:", "Correo:"]
        self.user_data = {}
        self.data_guardada = False  # Flag para asegurar que los datos solo se guardan una vez
        for i, prompt in enumerate(self.prompts):
            self.input_boxes.append(pygame.Rect(150, 50 + i * 50, 400, 40))

    def create_buttons(self):
        return {
            "Guardar": pygame.Rect(self.screen_width // 2 - 110, self.screen_height - 100, 100, 50),
            "Volver": pygame.Rect(self.screen_width // 2 + 10, self.screen_height - 100, 100, 50)
        }

    def get_user_data(self):
        running = True
        input_texts = [""] * len(self.prompts)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.buttons["Guardar"].collidepoint(event.pos) and not self.data_guardada:
                        self.user_data = dict(zip(self.prompts, input_texts))
                        if all(self.user_data.values()):  # Ensure all fields are filled
                            self.guardar_usuario()
                            self.data_guardada = True  # Ensure data is saved only once
                            self.mostrar_mensaje_guardado()
                            self.volver_a_inicio()
                            running = False
                        else:
                            print("Por favor, complete todos los campos.")
                    elif self.buttons["Volver"].collidepoint(event.pos):
                        self.volver_a_inicio()
                        running = False
                        self.user_data = {}  # Clear user_data if returning to menu
                    for i, box in enumerate(self.input_boxes):
                        if box.collidepoint(event.pos):
                            self.active_input = i
                if event.type == pygame.KEYDOWN and self.active_input is not None:
                    if event.key == pygame.K_BACKSPACE:
                        input_texts[self.active_input] = input_texts[self.active_input][:-1]
                    else:
                        input_texts[self.active_input] += event.unicode
            self.screen.fill((0, 0, 0))
            for i, box in enumerate(self.input_boxes):
                txt_surface = self.font.render(input_texts[i], True, (255, 255, 255))
                self.screen.blit(txt_surface, (box.x + 5, box.y + 5))
                pygame.draw.rect(self.screen, (255, 255, 255), box, 2)
                prompt_surface = self.font.render(self.prompts[i], True, (255, 255, 255))
                self.screen.blit(prompt_surface, (50, 50 + i * 50))
            for text, rect in self.buttons.items():
                pygame.draw.rect(self.screen, (255, 255, 255), rect, 2)
                btn_text = self.font.render(text, True, (255, 255, 255))
                self.screen.blit(btn_text, (rect.x + 10, rect.y + 10))
            pygame.display.flip()
        return self.user_data

    def guardar_usuario(self):
        insercion = Insercion()
        insercion.insertar_usuario(self.user_data)

    def mostrar_mensaje_guardado(self):
        self.screen.fill((0, 0, 0))
        mensaje_surface = self.font.render("Jugador guardado", True, (0, 255, 0))
        self.screen.blit(mensaje_surface, (self.screen_width // 2 - mensaje_surface.get_width() // 2, self.screen_height // 2))
        pygame.display.flip()
        pygame.time.delay(2000)  # Delay for 2 seconds

    def volver_a_inicio(self):
        print("Volver al menú principal")
        from SistemaRetoTico.menu import Menu  # Import Menu here to avoid circular import issues
        menu = Menu(self.screen, self.screen_width, self.screen_height)
        menu.show()
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    menu.handle_click(event.pos)
                    
        pygame.quit()
