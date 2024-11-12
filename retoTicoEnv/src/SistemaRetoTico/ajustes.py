import pygame
import sys

class Ajustes:
    def __init__(self, screen, screen_width, screen_height):
        pygame.display.set_caption("Ajustes")
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font(None, 36)
        self.estado = "menu"  # Estado inicial
        self.setup_ui()

    def setup_ui(self):
        """ Configura la interfaz del menú de ajustes """
        self.boton_agregar_pregunta = pygame.Rect(self.screen_width // 2 - 100, 100, 200, 50)
        self.boton_editar_pregunta = pygame.Rect(self.screen_width // 2 - 100, 200, 200, 50)
        self.boton_agregar_categoria = pygame.Rect(self.screen_width // 2 - 100, 300, 200, 50)
        self.boton_editar_categoria = pygame.Rect(self.screen_width // 2 - 100, 400, 200, 50)
        self.boton_editar_usuario = pygame.Rect(self.screen_width // 2 - 100, 500, 200, 50)
        
        # Botón de volver al menú
        self.boton_volver_menu = pygame.Rect(self.screen_width // 2 - 100, 600, 200, 50)

    def dibujar_menu(self):
        """ Dibuja el menú de ajustes """
        self.screen.fill((0, 0, 0))

        title_text = self.font.render("Ajustes", True, (255, 255, 255))
        self.screen.blit(title_text, (self.screen_width // 2 - title_text.get_width() // 2, 20))

        pygame.draw.rect(self.screen, (0, 0, 255), self.boton_agregar_pregunta)
        self.screen.blit(self.font.render("Agregar Pregunta", True, (255, 255, 255)), (self.screen_width // 2 - 90, 115))

        pygame.draw.rect(self.screen, (0, 0, 255), self.boton_editar_pregunta)
        self.screen.blit(self.font.render("Editar Pregunta", True, (255, 255, 255)), (self.screen_width // 2 - 90, 215))

        pygame.draw.rect(self.screen, (0, 0, 255), self.boton_agregar_categoria)
        self.screen.blit(self.font.render("Agregar Categoria", True, (255, 255, 255)), (self.screen_width // 2 - 90, 315))

        pygame.draw.rect(self.screen, (0, 0, 255), self.boton_editar_categoria)
        self.screen.blit(self.font.render("Editar Categoria", True, (255, 255, 255)), (self.screen_width // 2 - 90, 415))

        pygame.draw.rect(self.screen, (0, 0, 255), self.boton_editar_usuario)
        self.screen.blit(self.font.render("Editar Usuario", True, (255, 255, 255)), (self.screen_width // 2 - 90, 515))

        # Dibuja el botón de "Volver al Menú"
        pygame.draw.rect(self.screen, (255, 0, 0), self.boton_volver_menu)
        self.screen.blit(self.font.render("Volver al Menú", True, (255, 255, 255)), 
                         (self.screen_width // 2 - 90, 615))
        
        pygame.display.flip()

    def handle_click(self, pos):
        """ Gestiona los clics en los botones de ajustes """
        if self.boton_agregar_pregunta.collidepoint(pos):
            self.agregar_pregunta()
        elif self.boton_editar_pregunta.collidepoint(pos):
            self.editar_pregunta()
        elif self.boton_agregar_categoria.collidepoint(pos):
            self.agregar_categoria()
        elif self.boton_editar_categoria.collidepoint(pos):
            self.editar_categoria()
        elif self.boton_editar_usuario.collidepoint(pos):
            self.editar_usuario()
        elif self.boton_volver_menu.collidepoint(pos):
            self.volver_al_menu()

    def agregar_pregunta(self):
        print("# Implementa la lógica para agregar una nueva pregunta")
        pass

    def editar_pregunta(self):
        print("# Implementa la lógica para editar una pregunta")
        pass

    def agregar_categoria(self):
        print("# Implementa la lógica para agregar una nueva categoría")
        pass

    def editar_categoria(self):
        print("# Implementa la lógica para editar una categoría")
        pass

    def editar_usuario(self):
        print("# Implementa la lógica para editar un usuario")
        pass
    def volver_al_menu(self):
        print("Volviendo al menú principal...")
        from SistemaRetoTico.menu import Menu
        menu = Menu(self.screen, self.screen_width, self.screen_height)
        menu.show()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    menu.handle_events(event)
                    menu.handle_click(event.pos)
            
        
