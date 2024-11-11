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
        self.jugadores = self.seleccion.obtener_jugadores()
        self.dificultades = self.seleccion.obtener_dificultades()
        self.categorias = None
        self.buttons = self.create_buttons()
        self.jugador_seleccionado = None
        self.dificultad_seleccionada = None
        self.categorias_seleccionadas = []
        self.jugador_surfaces = self.preparar_jugadores_surfaces()
        
    def obtener_lista_de_jugadores(self):
        # Aquí se devuelve la lista de jugadores, ya implementada en tu clase `Seleccion`
        return self.jugadores

    def preparar_jugadores_surfaces(self):
        surfaces = []
        for idx, jugador in enumerate(self.jugadores):
            jugador_text = f"{jugador[1]} {jugador[2]}"
            jugador_surface = self.font.render(jugador_text, True, (255, 255, 255))
            jugador_rect = pygame.Rect(200, 100 + idx * 50, 400, 40)
            surfaces.append((jugador_surface, jugador_rect))
        return surfaces

    def create_buttons(self):
        buttons = {}
        button_texts = ["Volver", "Registrar Nuevo", "Iniciar Juego"]
        
        # Espacio entre los botones
        vertical_margin = 10
        # Establece el espacio de los botones desde la parte inferior de la pantalla
        initial_y = self.screen_height - 100

        for text in button_texts:
            # Calcula el ancho y alto del botón basado en el tamaño del texto
            text_surface = self.font.render(text, True, (255, 255, 255))
            button_width = text_surface.get_width() + 20  # Añadir margen
            button_height = text_surface.get_height() + 20  # Añadir margen

            # Centra los botones horizontalmente en la pantalla
            button_rect = pygame.Rect(self.screen_width // 2 - button_width // 2, 
                                    initial_y - (button_height + vertical_margin), 
                                    button_width, 
                                    button_height)
            
            # Guardar el botón en el diccionario de botones
            buttons[text] = button_rect

            # Actualizar la posición inicial_y para el siguiente botón
            initial_y = button_rect.top - vertical_margin

        return buttons

    def renderizar_jugadores(self):
        self.screen.fill((0, 0, 0))
        for jugador_surface, jugador_rect in self.jugador_surfaces:
            self.screen.blit(jugador_surface, jugador_rect)
            pygame.draw.rect(self.screen, (255, 255, 255), jugador_rect, 2)
        self.renderizar_botones(["Volver", "Registrar Nuevo"])

    def renderizar_botones(self, botones):
        y_offset = 0  # Para mantener los botones ordenados verticalmente
        for boton in botones:
            rect = self.buttons[boton]
            # Reajustar la posición vertical si es necesario
            rect.y = self.screen_height - 100 - y_offset
            pygame.draw.rect(self.screen, (255, 255, 255), rect, 2)
            btn_text = self.font.render(boton, True, (255, 255, 255))
            self.screen.blit(btn_text, (rect.x + 10, rect.y + 10))
            y_offset += rect.height + 10  # Ajusta la distancia entre botones

    def seleccion_jugador(self):
        if not self.jugadores:
            print("No hay jugadores registrados.")
            self.registrar_nuevo_jugador()
            return "No hay jugadores"
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.volver_a_inicio()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.buttons["Volver"].collidepoint(event.pos):
                        running = False
                        self.volver_a_inicio()
                    elif self.buttons["Registrar Nuevo"].collidepoint(event.pos):
                        self.registrar_nuevo_jugador()
                    for idx, jugador in enumerate(self.jugadores):
                        jugador_rect = pygame.Rect(200, 100 + idx * 50, 400, 40)
                        if jugador_rect.collidepoint(event.pos):
                            running = False
                            self.jugador_seleccionado = jugador
                            self.seleccion_dificultad()  # Selección de dificultad aquí
            if running:
                self.renderizar_jugadores()
                pygame.display.flip()

    def renderizar_opciones(self, opciones, seleccionadas=None, es_categoria=False):
        """Renderiza opciones en pantalla, destacando las seleccionadas si corresponde.
        
        :param opciones: Lista de opciones a renderizar (pueden ser solo nombres o diccionarios con 'id' y 'nombre').
        :param seleccionadas: Lista de opciones seleccionadas, se usa para cambiar el color de las seleccionadas.
        :param es_categoria: Indica si las opciones son categorías (por lo que se manejarán id y nombre).
        """
        self.screen.fill((0, 0, 0))  # Limpiar pantalla

        for i, opcion in enumerate(opciones):
            if es_categoria:
                # Si 'opcion' es un diccionario con las claves 'id' y 'nombre'
                if isinstance(opcion, dict) and 'id_categoria' in opcion and 'nombre_categoria' in opcion:
                    opcion_str = opcion['nombre_categoria']  # Usamos el nombre de la categoría
                    opcion_id = opcion['id_categoria']      # Guardamos el id de la categoría
                else:
                    # Si 'opcion' no es un diccionario o no tiene las claves esperadas
                    print(f"Advertencia: la opción '{opcion}' no tiene el formato esperado (id, nombre).")
                    continue
            else:
                # Si es dificultad, 'opcion' es simplemente el nombre
                opcion_str = opcion
                opcion_id = opcion  # El id es el mismo que el nombre de la dificultad

            # Verificar si la opción está seleccionada
            color = (0, 255, 0) if seleccionadas and opcion_id in seleccionadas else (255, 255, 255)
            
            # Renderizar el texto de la opción
            opcion_text = self.font.render(opcion_str, True, color)
            opcion_rect = pygame.Rect(200, 100 + i * 50, 400, 40)
            
            # Dibujar rectángulo y texto
            pygame.draw.rect(self.screen, color, opcion_rect, 2)
            self.screen.blit(opcion_text, (opcion_rect.x + 10, opcion_rect.y + 10))

        # Dibujar botón de iniciar juego
        iniciar_juego_rect = pygame.Rect(self.screen_width // 2 - 75, self.screen_height - 100, 150, 50)
        pygame.draw.rect(self.screen, (255, 255, 255), iniciar_juego_rect, 2)
        iniciar_text = self.font.render("Iniciar Juego", True, (255, 255, 255))
        self.screen.blit(iniciar_text, (iniciar_juego_rect.x + 10, iniciar_juego_rect.y + 10))
        
        # Guardar rectángulo del botón para manejo de clics en el otro método
        self.buttons = {"Iniciar Juego": iniciar_juego_rect}


    def renderizar_dificultades(self):
        """Renderiza las opciones de dificultad en pantalla."""
        self.renderizar_opciones(self.dificultades, es_categoria=False)

    def renderizar_categorias(self, seleccionadas):
        """Renderiza las opciones de categorías en pantalla, destacando las seleccionadas."""
        # Aquí se pasa la lista de categorías con los id_categoria y nombre
        self.renderizar_opciones(self.categorias, seleccionadas=seleccionadas, es_categoria=True)

    def seleccion_dificultad(self):
        """Permite al usuario seleccionar una dificultad mediante clics en la pantalla."""
        if not self.dificultades:
            print("No hay dificultades disponibles.")
            self.volver_a_inicio()
            return

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.volver_a_inicio()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for i, dificultad in enumerate(self.dificultades):
                        dificultad_rect = pygame.Rect(200, 100 + i * 50, 400, 40)
                        if dificultad_rect.collidepoint(event.pos):
                            self.dificultad_seleccionada = dificultad
                            running = False
                            self.seleccion_categorias(self.dificultad_seleccionada)  # Avanza a la selección de categorías
            if running:
                self.renderizar_dificultades()
                pygame.display.flip()

    def seleccion_categorias(self,dificultad):
        """Permite al usuario seleccionar múltiples categorías mediante clics en la pantalla."""
        self.categorias = self.seleccion.obtener_categorias(dificultad)
        if not self.categorias:
            print("No hay categorías disponibles.")
            self.volver_a_inicio()
            return

        seleccionadas = set()  # Para almacenar los id_categoria seleccionados
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.volver_a_inicio()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for i, categoria in enumerate(self.categorias):
                        categoria_rect = pygame.Rect(200, 100 + i * 50, 400, 40)
                        if categoria_rect.collidepoint(event.pos):
                            # Almacenar el id_categoria de la categoría seleccionada, no el nombre
                            if categoria['id_categoria'] in seleccionadas:
                                seleccionadas.remove(categoria['id_categoria'])  # Desmarcar
                            else:
                                seleccionadas.add(categoria['id_categoria'])  # Marcar

                    # Comprueba si el botón de iniciar juego ha sido presionado
                    if self.buttons["Iniciar Juego"].collidepoint(event.pos):
                        if seleccionadas:
                            # Almacenar los id_categoria seleccionados
                            self.categorias_seleccionadas = list(seleccionadas)
                            running = False
                            self.iniciar_juego(self.jugador_seleccionado)  # Inicia el juego
            if running:
                self.renderizar_categorias(seleccionadas)
                pygame.display.flip()
    
    def iniciar_juego(self, jugador):
        """Inicia el juego con el jugador seleccionado."""
        print(f"Jugador seleccionado: {jugador[1]} {jugador[2]}")
        juego = Juego(jugador, self.dificultad_seleccionada, self.categorias_seleccionadas, self.screen, self.screen_width, self.screen_height)
        
        # Ejecuta el juego y regresa al menú al terminar
        while True:
            juego_terminado = juego.ejecutar()  # Asegúrate de que `ejecutar` devuelve True si el juego termina o el jugador elige salir
            
            if juego_terminado:
                print("Juego terminado. Regresando al menú principal.")
                self.volver_a_inicio()  # Llamar al método para regresar al menú principal
                break

    def volver_a_inicio(self):
        """Muestra el menú principal sin cerrar la aplicación."""
        print("Volver al menú principal")
        from SistemaRetoTico.menu import Menu  # Importa el menú aquí para evitar importaciones circulares
        menu = Menu(self.screen, self.screen_width, self.screen_height)
        menu.show()


    def registrar_nuevo_jugador(self):
        registrar_jugador = RegistrarJugador(self.screen, self.screen_width, self.screen_height)
        registrar_jugador.get_user_data()
