import sqlite3
import pygame
import time

class JuegoIniciado:
    def __init__(self, jugador, dificultad, categoria, screen, screen_width, screen_height):
        pygame.display.set_caption("Juego Iniciado")
        self.jugador = jugador
        self.categoria = categoria
        self.dificultad = dificultad
        self.screen = screen
        self.puntaje = 0
        self.aciertos = 0
        self.desaciertos = 0
        self.font = pygame.font.Font(None, 36)
        self.screen_width = screen_width  # Añadir este atributo
        self.screen_height = screen_height  # Añadir este atributo
        self.current_question = 0  # Índice de la pregunta actual
        self.selected_answer = None  # Respuesta seleccionada

        # Obtener las preguntas de la base de datos
        self.questions = self.obtener_preguntas()

    def obtener_preguntas(self):
        from Datos.seleccion import Seleccion
        contenedorPreguntas = Seleccion()
        preguntas = []
        
        for _ in range(5):  # Puedes cambiar el número de preguntas
            pregunta_info = contenedorPreguntas.obtener_preguntas(self.dificultad, self.categoria)
            
            # Verifica si es una lista y toma el primer elemento
            if isinstance(pregunta_info, list) and pregunta_info:
                pregunta_info = pregunta_info[0]

            if pregunta_info:
                try:
                    correct_index = next(i for i, r in enumerate(pregunta_info["respuestas"]) if r["es_correcta"])
                except StopIteration:
                    print(f"No se encontró una respuesta correcta para la pregunta con id {pregunta_info['id_pregunta']}")
                    correct_index = None  # O cualquier otro valor predeterminado si no hay una respuesta correcta
                
                preguntas.append({
                    "idPregunta": pregunta_info["id_pregunta"],
                    "question": pregunta_info["pregunta"],
                    "options": [r["respuesta"] for r in pregunta_info["respuestas"]],
                    "correct": correct_index
                })
        
        return preguntas

    def iniciar_juego(self):
        self.temporizador(60)

    def temporizador(self, tiempo_max):
        start_time = time.time()
        while True:
            tiempo_transcurrido = time.time() - start_time
            tiempo_restante = max(tiempo_max - tiempo_transcurrido, 0)

            self.screen.fill((255, 255, 255))
            self.mostrar_informacion_jugador()
            self.mostrar_pregunta()
            self.mostrar_mensaje(f"Tiempo restante: {int(tiempo_restante)} segundos", (20, self.screen.get_height() - 40))
            self.dibujar_boton_pausa()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.pausa_menu()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if self.boton_pausa_rect.collidepoint(pos):
                        self.pausa_menu()
                    elif self.verificar_boton_rect.collidepoint(pos):
                        self.verificar_respuesta()
                    else:
                        self.detectar_opcion_seleccionada(pos)

            if tiempo_restante <= 0:
                self.mostrar_mensaje("Tiempo agotado!")
                break

    def mostrar_pregunta(self):
        # Mostrar la pregunta y opciones en el centro de la pantalla sin recuadro
        if self.current_question < len(self.questions):
            pregunta = self.questions[self.current_question]
            texto_pregunta = pregunta["question"]
            opciones = pregunta["options"]

            # Definir colores
            color_texto = (0, 0, 0)  # Texto negro
            color_respuesta = (0, 128, 0)  # Color para la opción seleccionada

            # Renderizar y mostrar la pregunta centrada
            pregunta_surface = self.font.render(texto_pregunta, True, color_texto)
            pregunta_x = (self.screen_width - pregunta_surface.get_width()) // 2
            pregunta_y = (self.screen_height - pregunta_surface.get_height()) // 2
            self.screen.blit(pregunta_surface, (pregunta_x, pregunta_y))

            # Mostrar las opciones centradas debajo de la pregunta
            for idx, opcion in enumerate(opciones):
                # Definir el color de selección para el checkbox
                color_checkbox = color_respuesta if self.selected_answer == idx else color_texto
                checkbox_rect = pygame.Rect(self.screen_width // 2 - 100, pregunta_y + 70 + (idx * 40), 20, 20)
                pygame.draw.rect(self.screen, color_checkbox, checkbox_rect, 2)  # Borde del checkbox
                if self.selected_answer == idx:
                    # Si está seleccionado, dibujamos una marca de verificación dentro del checkbox
                    pygame.draw.line(self.screen, color_respuesta, (checkbox_rect.x + 5, checkbox_rect.y + 5),
                                    (checkbox_rect.x + 15, checkbox_rect.y + 15), 2)
                    pygame.draw.line(self.screen, color_respuesta, (checkbox_rect.x + 15, checkbox_rect.y + 5),
                                    (checkbox_rect.x + 5, checkbox_rect.y + 15), 2)

                # Mostrar la opción junto al checkbox
                opcion_surface = self.font.render(f"{opcion}", True, color_texto)
                opcion_x = self.screen_width // 2 - 50  # Ajuste para espacio después del checkbox
                opcion_y = pregunta_y + 70 + (idx * 40)  # Espacio entre las opciones
                self.screen.blit(opcion_surface, (opcion_x, opcion_y))

            # Dibujar el botón de verificación
            self.verificar_boton_rect = pygame.Rect(self.screen_width // 2 + 20, pregunta_y + 220, 100, 30)
            pygame.draw.rect(self.screen, (0, 128, 0), self.verificar_boton_rect)
            verificar_surface = self.font.render("Verificar", True, (255, 255, 255))
            self.screen.blit(verificar_surface, (self.verificar_boton_rect.x + 10, self.verificar_boton_rect.y + 5))


    def detectar_opcion_seleccionada(self, pos):
        # Detecta cuál opción fue seleccionada (ahora como un checkbox)
        for i in range(len(self.questions[self.current_question]["options"])):
            # Ajusta las posiciones de los checkboxes según las coordenadas correctas
            checkbox_rect = pygame.Rect(self.screen_width // 2 - 100, self.screen_height // 2 + 70 + i * 40, 20, 20)
            if checkbox_rect.collidepoint(pos):
                if self.selected_answer == i:
                    # Si la opción ya está seleccionada, desmarcarla
                    self.selected_answer = None
                else:
                    # Marcar la opción seleccionada
                    self.selected_answer = i

    def verificar_respuesta(self):
        # Verificar si la respuesta seleccionada es la correcta
        if self.selected_answer is not None:  # Verificar que se haya seleccionado una opción
            pregunta = self.questions[self.current_question]
            if self.selected_answer == pregunta["correct"]:
                self.aciertos += 1
                self.puntaje += 10  # Ajustar la puntuación según se desee
            else:
                self.desaciertos += 1
            self.current_question += 1
            self.selected_answer = None  # Reiniciar la selección de respuesta para la próxima pregunta


    def mostrar_informacion_jugador(self):
        info_jugador = f"Jugador: {self.jugador}"
        info_dificultad = f"Dificultad: {self.dificultad}"
        info_puntaje = f"Puntaje: {self.puntaje}"
        info_aciertos = f"Aciertos: {self.aciertos}"
        info_desaciertos = f"Desaciertos: {self.desaciertos}"

        jugador_surface = self.font.render(info_jugador, True, (0, 0, 0))
        dificultad_surface = self.font.render(info_dificultad, True, (0, 0, 0))
        puntaje_surface = self.font.render(info_puntaje, True, (0, 0, 0))
        aciertos_surface = self.font.render(info_aciertos, True, (0, 0, 0))
        desaciertos_surface = self.font.render(info_desaciertos, True, (0, 0, 0))

        left_x = 20
        right_x = self.screen.get_width() - 200
        top_y = 20

        self.screen.blit(jugador_surface, (left_x, top_y))
        self.screen.blit(dificultad_surface, (left_x, top_y + 40))
        self.screen.blit(puntaje_surface, (right_x, top_y))
        self.screen.blit(aciertos_surface, (right_x, top_y + 40))
        self.screen.blit(desaciertos_surface, (right_x, top_y + 80))

    def dibujar_boton_pausa(self):
        boton_pausa_ancho, boton_pausa_alto = 80, 30
        self.boton_pausa_rect = pygame.Rect(
            self.screen.get_width() - boton_pausa_ancho - 20,
            self.screen.get_height() - boton_pausa_alto - 20,
            boton_pausa_ancho,
            boton_pausa_alto
        )
        pygame.draw.rect(self.screen, (255, 0, 0), self.boton_pausa_rect)
        boton_texto = self.font.render("Pausa", True, (255, 255, 255))
        self.screen.blit(boton_texto, (self.boton_pausa_rect.x + 5, self.boton_pausa_rect.y + 5))

    def pausa_menu(self):
        opciones = ["Reanudar", "Cambiar dificultad", "Cambiar jugador", "Volver al menú", "Salir"]
        botones_rect = []

        fondo_menu = pygame.Surface(self.screen.get_size())
        fondo_menu.fill((0, 0, 0))
        fondo_menu.set_alpha(128)

        while True:
            self.screen.fill((255, 255, 255))
            self.mostrar_informacion_jugador()
            self.screen.blit(fondo_menu, (0, 0))
            self.mostrar_mensaje("Juego Pausado. Escoge una opción:")
            for i, opcion in enumerate(opciones):
                boton_rect = pygame.Rect(self.screen.get_width() // 2 - 100, self.screen.get_height() // 2 - 50 + i * 40, 200, 30)
                botones_rect.append(boton_rect)
                pygame.draw.rect(self.screen, (0, 128, 255), boton_rect)
                opcion_surface = self.font.render(opcion, True, (255, 255, 255))
                self.screen.blit(opcion_surface, (boton_rect.x + 10, boton_rect.y + 5))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        return
                    elif event.key == pygame.K_2:
                        self.cambiar_dificultad()
                    elif event.key == pygame.K_3:
                        self.cambiar_jugador()
                    elif event.key == pygame.K_4:
                        self.regresar_menu_principal()
                    elif event.key == pygame.K_5:
                        pygame.quit()
                        exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for i, boton_rect in enumerate(botones_rect):
                        if boton_rect.collidepoint(pos):
                            if i == 0:
                                return
                            elif i == 1:
                                self.cambiar_dificultad()
                            elif i == 2:
                                self.cambiar_jugador()
                            elif i == 3:
                                self.regresar_menu_principal()
                            elif i == 4:
                                pygame.quit()
                                exit()

    def regresar_menu_principal(self):
        print("Volver al menú principal")
        from SistemaRetoTico.menu import Menu  # Import Menu aquí para evitar problemas de importación circular
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

    def cambiar_dificultad(self):
        nueva_dificultad = input("Introduce la nueva dificultad (baja, media, alta): ")
        self.dificultad = nueva_dificultad
        print(f"Dificultad cambiada a: {self.dificultad}")

    def mostrar_mensaje(self, mensaje, posicion=(20, 60)):
        mensaje_text = self.font.render(mensaje, True, (0, 0, 0))
        self.screen.blit(mensaje_text, posicion)
    
    def cambiar_jugador(self):
        print("Seleccionar Jugador")
        from Logica.seleccionar_jugador import SeleccionarJugador
        seleccionar_jugador = SeleccionarJugador(self.screen, self.screen_width, self.screen_height)
        jugador_seleccionado = seleccionar_jugador.seleccion_jugador()
        if jugador_seleccionado:
            print(f"Jugador existente seleccionado: {jugador_seleccionado}")
        else:
            print("No hay jugadores registrados.")
