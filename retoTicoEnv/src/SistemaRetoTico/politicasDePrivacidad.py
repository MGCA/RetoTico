import pygame

class PoliticasDePrivacidad:
    def __init__(self, screen, nombre_del_sistema, estudiantes):
        pygame.init()
        pygame.display.set_caption("Politicas")
        self.screen = screen
        self.nombre_del_sistema = nombre_del_sistema
        self.estudiantes = estudiantes
        
        # Obtener dimensiones de la pantalla
        self.screen_width, self.screen_height = self.screen.get_size()
        
        # Definir tamaño de fuente relativo a la altura de la pantalla
        self.font_size = int(self.screen_height * 0.025)  # Por ejemplo, 2.5% de la altura de la pantalla
        self.font_normal = pygame.font.Font(None, self.font_size)
        self.font_bold = pygame.font.Font(None, self.font_size + 10)  # Fuente más grande para títulos

        # Definir dimensiones del botón
        self.button_width = 200
        self.button_height = 50
        self.button_color = (0, 128, 255)  # Color del botón
        self.button_hover_color = (0, 100, 200)  # Color cuando el mouse pasa sobre el botón
        self.button_text_color = (255, 255, 255)  # Color del texto del botón

    def mostrar_politicas(self):
        # Limpia la pantalla para mostrar solo las políticas
        self.screen.fill((0, 0, 0))  # Fondo negro

        # Título
        titulo_texto = f"Políticas de Privacidad de {self.nombre_del_sistema}"
        titulo = self.font_bold.render(titulo_texto, True, (255, 255, 255))  # Color blanco
        self.screen.blit(titulo, (20, 20))  # Dibuja el título en la pantalla

        # Espaciado inicial
        y_offset = 60  # Espacio después del título
        line_height = self.font_size * 1.5  # Altura de línea

        # Texto de políticas
        politicas_texto = (
            "Los desarrolladores de este proyecto educativo ceden este software como código\n"
            "abierto bajo la licencia MIT.\n"
            "Esto significa que cualquier persona es libre de usar, modificar y distribuir el\n"
            "software, siempre y cuando se cumplan las condiciones de la licencia.\n\n"
            "Los desarrolladores otorgan permiso a los profesores de la Escuela de Informática\n"
            "de la Universidad Nacional (UNA) para desarrollar un artículo académico basado en este proyecto,\n"
            "reconociendo y mencionando a los desarrolladores como autores del software. Esta cesión fomenta \n"
            "la investigación y la mejora continua en el ámbito de la educación tecnológica.\n\n"
            "Licencia MIT: \"El software se proporciona 'tal cual', sin garantía de ningún \n"
            "tipo, expresa o implícita, incluyendo pero no limitado a garantías de comercia-\n"
            "bilidad o adecuación para un propósito particular.\"\n\n"
            "NOMBRE Y CEDULA DE CADA ESTUDIANTE:\n"
            f"{self.formatear_estudiantes()}\n"
            "Firmas escaneadas que se ven en la presentación (y quedarán grabadas en el video)."
        )

        # Divide el texto en líneas y dibuja cada línea en la pantalla
        for line in politicas_texto.splitlines():
            texto = self.font_normal.render(line, True, (255, 255, 255))  # Color blanco
            
            # Ajusta la posición y dibuja el texto
            self.screen.blit(texto, (20, y_offset))
            y_offset += line_height  # Incrementa el offset para la siguiente línea

            # Verifica si el texto excede la altura de la pantalla
            if y_offset > self.screen_height - 100:  # Mantiene espacio para el botón
                break  # Detiene el dibujo si excede la pantalla

        # Dibuja el botón
        button_x = (self.screen_width - self.button_width) // 2  # Centrado horizontalmente
        button_y = self.screen_height - self.button_height - 20  # 20 píxeles de margen desde la parte inferior
        self.dibujar_boton(button_x, button_y, self.button_width, self.button_height, "Volver al Menú")

        pygame.display.flip()  # Actualiza la pantalla

        # Manejo de eventos para volver al menú
        self.esperar_volver(button_x, button_y, self.button_width, self.button_height)

    def dibujar_boton(self, x, y, width, height, texto):
        # Dibuja el botón
        pygame.draw.rect(self.screen, self.button_color, (x, y, width, height))  # Dibuja el rectángulo del botón
        texto_boton = self.font_normal.render(texto, True, self.button_text_color)
        texto_rect = texto_boton.get_rect(center=(x + width // 2, y + height // 2))
        self.screen.blit(texto_boton, texto_rect)  # Dibuja el texto del botón

    def esperar_volver(self, button_x, button_y, button_width, button_height):
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Escuchar cuando se cierra la ventana
                    pygame.quit()  # Finaliza Pygame
                    exit()  # Termina el programa
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # Presiona ESC para volver
                        waiting = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()  # Obtener la posición del mouse
                    if (button_x <= mouse_pos[0] <= button_x + button_width and
                            button_y <= mouse_pos[1] <= button_y + button_height):
                        waiting = False  # Cerrar si se hace clic en el botón

        # Aquí podrías añadir el código necesario para volver al menú principal
        self.volver_al_menu()

    def volver_al_menu(self):
        # Implementa la lógica para regresar al menú principal aquí
        print("Volver al menú principal")
        from SistemaRetoTico.menu import Menu  # Import Menu here to avoid circular import issues
        menu = Menu(self.screen, self.screen_width, self.screen_height)
        menu.show()

        # Mantén el ciclo de eventos abierto mientras el usuario está en el menú
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    menu.handle_events(event)
                    menu.handle_click(event.pos)

    def formatear_estudiantes(self):
        return "\n".join([f"{nombre} - Cédula: {cedula}" for nombre, cedula in self.estudiantes])
