import pygame
import sys
from Datos.insercion import Insercion
from Datos.seleccion import Seleccion

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
        self.dropdown_open = None  # Indica si un dropdown está abierto
        self.dropdown_items = []  # Los items a mostrar en el dropdown
        self.selected_dropdown_item = None  # Elemento seleccionado en el dropdown

        # Definir los rectángulos para las cajas de entrada
        for i, prompt in enumerate(self.prompts):
            self.input_boxes.append(pygame.Rect(150, 50 + i * 80, 400, 40))

        self.seleccion_datos = Seleccion()

        # Obtener las provincias, cantones y distritos
        self.provincias = self.seleccion_datos.obtener_provincias()
        self.cantones = []
        self.distritos = []

    def create_buttons(self):
        # Crear botones con tamaño dinámico dependiendo del texto
        guardar_text = self.font.render("Guardar", True, (0, 0, 0))
        volver_text = self.font.render("Volver", True, (0, 0, 0))
        
        # Ajustar el tamaño de los botones basado en el ancho del texto
        guardar_width = guardar_text.get_width() + 20  # Agregar margen alrededor del texto
        volver_width = volver_text.get_width() + 20

        return {
            "Guardar": pygame.Rect(self.screen_width // 2 - (guardar_width + volver_width) // 2, self.screen_height - 100, guardar_width, 50),
            "Volver": pygame.Rect(self.screen_width // 2 + (guardar_width + volver_width) // 2, self.screen_height - 100, volver_width, 50)
        }

    def draw_buttons(self):
        # Botones "Guardar" y "Volver"
        pygame.draw.rect(self.screen, (0, 255, 0), self.buttons["Guardar"])  # Botón Guardar en verde
        pygame.draw.rect(self.screen, (255, 0, 0), self.buttons["Volver"])  # Botón Volver en rojo

        # Mostrar el texto en los botones
        guardar_surface = self.font.render("Guardar", True, (0, 0, 0))
        volver_surface = self.font.render("Volver", True, (0, 0, 0))
        self.screen.blit(guardar_surface, (self.buttons["Guardar"].x + 10, self.buttons["Guardar"].y + 10))
        self.screen.blit(volver_surface, (self.buttons["Volver"].x + 10, self.buttons["Volver"].y + 10))


    def draw_dropdown(self, rect, items, selected_item=None):
        """Dibuja el dropdown con las opciones disponibles."""
        pygame.draw.rect(self.screen, (255, 255, 255), rect, 2)
        if selected_item:
            text_surface = self.font.render(selected_item, True, (255, 255, 255))
        else:
            text_surface = self.font.render("Seleccionar", True, (255, 255, 255))
        self.screen.blit(text_surface, (rect.x + 5, rect.y + 5))
        
        if self.dropdown_open:
            for idx, item in enumerate(items):
                item_rect = pygame.Rect(rect.x, rect.y + (idx + 1) * 40, rect.width, 40)
                pygame.draw.rect(self.screen, (255, 255, 255), item_rect)
                item_text = self.font.render(item, True, (0, 0, 0))  # Negro para el texto
                self.screen.blit(item_text, (item_rect.x + 5, item_rect.y + 5))

    def get_user_data(self):
        try:
            self.screen.fill((0, 0, 0))
            running = True
            input_texts = [""] * len(self.prompts)
            scroll_offset = 0  # Desplazamiento para el scroll
            scroll_speed = 30  # Cuánto se mueve el scroll por evento

            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.buttons["Guardar"].collidepoint(event.pos) and not self.data_guardada:
                            self.user_data = dict(zip(self.prompts, input_texts))
                            if all(self.user_data.values()):  # Asegura que todos los campos estén completos
                                self.guardar_usuario()
                                self.data_guardada = True  # Asegura que los datos solo se guarden una vez
                                self.mostrar_mensaje_guardado()
                                self.volver_a_inicio()
                                running = False
                            else:
                                print("Por favor, complete todos los campos.")
                        elif self.buttons["Volver"].collidepoint(event.pos):
                            self.volver_a_inicio()
                            running = False
                            self.user_data = {}  # Limpiar los datos del usuario al regresar

                        # Verifica si el clic está fuera de los dropdowns
                        if self.dropdown_open:
                            for idx, item in enumerate(self.dropdown_items):
                                dropdown_rect = pygame.Rect(self.input_boxes[self.active_input].x, self.input_boxes[self.active_input].y + (idx + 1) * 40 - scroll_offset, 400, 40)
                                if dropdown_rect.collidepoint(event.pos):
                                    # Al seleccionar un item, guardar el ID (campo 0)
                                    self.selected_dropdown_item = item
                                    self.dropdown_open = False
                                    input_texts[self.active_input] = item[1]  # Mostrar solo el nombre (campo 1) en el campo de texto

                                    # Aquí almacenamos el ID (campo 0) para usarlo en la consulta
                                    if self.active_input == 3:  # Provincia seleccionada
                                        provincia_id = item[0]  # Guardamos el ID de la provincia
                                        self.cantones = self.seleccion_datos.obtener_cantones(provincia_id)
                                        self.distritos = []  # Limpiar distritos cuando se selecciona una provincia
                                    elif self.active_input == 4:  # Cantón seleccionado
                                        canton_id = item[0]  # Guardamos el ID del cantón
                                        self.distritos = self.seleccion_datos.obtener_distritos(canton_id)
                                    break  # Salir del bucle una vez que se selecciona un item
                            else:
                                self.dropdown_open = False  # Cerrar si no se selecciona nada

                        # Si se hace clic en alguna caja de texto
                        for i, box in enumerate(self.input_boxes):
                            if box.collidepoint(event.pos):
                                self.active_input = i
                                if i == 3:  # Cuando seleccionan Provincia
                                    self.dropdown_open = True
                                    self.dropdown_items = [(provincia[0], provincia[1]) for provincia in self.provincias]  # Tuplas (ID, Nombre)
                                elif i == 4:  # Cuando seleccionan Cantón
                                    if self.cantones:
                                        self.dropdown_open = True
                                        self.dropdown_items = [(canton[0], canton[1]) for canton in self.cantones]  # Tuplas (ID, Nombre)
                                    else:
                                        self.dropdown_open = False  # No mostrar dropdown si no hay cantones disponibles
                                elif i == 5:  # Cuando seleccionan Distrito
                                    if self.distritos:
                                        self.dropdown_open = True
                                        self.dropdown_items = [(distrito[0], distrito[1]) for distrito in self.distritos]  # Tuplas (ID, Nombre)
                                    else:
                                        self.dropdown_open = False  # No mostrar dropdown si no hay distritos disponibles
                                else:
                                    self.dropdown_open = False  # Si no es Provincia, Canton o Distrito

                    # Manejo de teclas
                    if event.type == pygame.KEYDOWN and self.active_input is not None:
                        # Si el dropdown está abierto, no permitir que el usuario escriba
                        if self.dropdown_open:
                            continue  # Salir de este ciclo y no permitir la escritura

                        if event.key == pygame.K_BACKSPACE:
                            # Eliminar el último carácter
                            input_texts[self.active_input] = input_texts[self.active_input][:-1]
                        elif event.key == pygame.K_TAB:
                            # Cambiar al siguiente campo de entrada
                            self.active_input = (self.active_input + 1) % len(self.input_boxes)
                        elif event.key == pygame.K_RETURN:
                            # Guardar cuando se presiona Enter
                            if not self.data_guardada:
                                self.user_data = dict(zip(self.prompts, input_texts))
                                if all(self.user_data.values()):  # Asegura que todos los campos estén completos
                                    self.guardar_usuario()
                                    self.data_guardada = True  # Asegura que los datos solo se guarden una vez
                                    self.mostrar_mensaje_guardado()
                                    self.volver_a_inicio()
                                    running = False
                                else:
                                    print("Por favor, complete todos los campos.")
                        elif event.key == pygame.K_ESCAPE:
                            # Volver al inicio si se presiona la tecla Escape
                            self.volver_a_inicio()
                            running = False
                        else:
                            # Validación para el cuadro de texto de Edad (solo números, máximo 2 dígitos)
                            if self.active_input == 2:  # Suponiendo que el cuadro de Edad es el índice 6
                                if event.unicode.isdigit() and len(input_texts[self.active_input]) < 2:
                                    input_texts[self.active_input] += event.unicode
                            # Validación para el cuadro de texto de Número WhatsApp (solo números, máximo 8 dígitos)
                            elif self.active_input == 6:  # Suponiendo que el cuadro de WhatsApp es el índice 7
                                if event.unicode.isdigit() and len(input_texts[self.active_input]) < 8:
                                    input_texts[self.active_input] += event.unicode
                            # Validación para los campos Nombre y Apellido (solo letras)
                            elif self.active_input == 0 or self.active_input == 1:
                                if event.unicode.isalpha() or event.key == pygame.K_SPACE:  # Permitir letras y espacio
                                    input_texts[self.active_input] += event.unicode
                            # Si es cualquier otro cuadro de texto, agregar el carácter
                            else:
                                input_texts[self.active_input] += event.unicode

                    # Detectar el desplazamiento con la rueda del mouse
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.dropdown_open and event.button == 4:  # Rueda del mouse hacia arriba
                            scroll_offset = max(scroll_offset - scroll_speed, 0)  # Limitar el scroll hacia arriba
                        elif self.dropdown_open and event.button == 5:  # Rueda del mouse hacia abajo
                            max_scroll = len(self.dropdown_items) * 40 - 400  # 400 es la altura visible del dropdown
                            scroll_offset = min(scroll_offset + scroll_speed, max_scroll)  # Limitar el scroll hacia abajo

                # Dibujar la pantalla
                self.screen.fill((0, 0, 0))

                for i, box in enumerate(self.input_boxes):
                    # Mostrar el cursor (rayita de espera) en el cuadro activo
                    if self.active_input == i:
                        txt_surface = self.font.render(input_texts[i] + "|", True, (255, 255, 255))  # Cursor al final del texto
                    else:
                        txt_surface = self.font.render(input_texts[i], True, (255, 255, 255))
                    
                    self.screen.blit(txt_surface, (box.x + 5, box.y + 5))
                    
                    # Cambiar el color del borde para indicar el cuadro activo
                    border_color = (0, 255, 0) if self.active_input == i else (255, 255, 255)
                    pygame.draw.rect(self.screen, border_color, box, 2)

                    # Dibujar el texto del prompt debajo del cuadro de texto para evitar superposiciones
                    prompt_surface = self.font.render(self.prompts[i], True, (255, 255, 255))
                    self.screen.blit(prompt_surface, (box.x, box.y - 35))  # Ajustar la posición vertical

                # Dibujar los botones con colores específicos
                pygame.draw.rect(self.screen, (0, 255, 0), self.buttons["Guardar"])  # Botón Guardar en verde
                pygame.draw.rect(self.screen, (255, 0, 0), self.buttons["Volver"])  # Botón Volver en rojo

                # Mostrar el texto en los botones
                guardar_surface = self.font.render("Guardar", True, (0, 0, 0))
                volver_surface = self.font.render("Volver", True, (0, 0, 0))
                self.screen.blit(guardar_surface, (self.buttons["Guardar"].x + 10, self.buttons["Guardar"].y + 10))
                self.screen.blit(volver_surface, (self.buttons["Volver"].x + 10, self.buttons["Volver"].y + 10))

                if self.dropdown_open:
                    for idx, item in enumerate(self.dropdown_items):
                        dropdown_rect = pygame.Rect(self.input_boxes[self.active_input].x, self.input_boxes[self.active_input].y + (idx + 1) * 40 - scroll_offset, 400, 40)
                        pygame.draw.rect(self.screen, (255, 255, 255), dropdown_rect)
                        dropdown_surface = self.font.render(item[1], True, (0, 0, 0))  # Mostrar solo el nombre
                        self.screen.blit(dropdown_surface, (dropdown_rect.x + 5, dropdown_rect.y + 5))

                pygame.display.flip()  # Actualizar la pantalla
        except pygame.error:
            # Aquí puedes manejar el error o terminar el ciclo si el display ha sido cerrado.
            running = False



    def guardar_usuario(self):
        # Guardar datos en la base de datos
        insercion = Insercion()
        insercion.insertar_usuario(self.user_data)

    def mostrar_mensaje_guardado(self):
        mensaje_surface = self.font.render("Datos guardados correctamente.", True, (0, 255, 0))
        self.screen.blit(mensaje_surface, (self.screen_width // 2 - 100, self.screen_height // 2))
        pygame.display.flip()
        pygame.time.wait(2000)


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
                    menu.handle_events(event)
                    menu.handle_click(event.pos)

        pygame.quit()
