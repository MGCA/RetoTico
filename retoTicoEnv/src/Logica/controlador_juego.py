import pygame  # Asegúrate de importar pygame
from Logica.estado_juego import EstadoJuego
from Logica.gestor_preguntas import GestorPreguntas
from Logica.renderizador_juego import RenderizadorJuego
from Datos.insertar_juego import InsertarJuegos
from datetime import datetime


class ControladorJuego:
    def __init__(self, jugador, dificultad, categoria, pantalla, ancho_pantalla, alto_pantalla):
        self.jugador = jugador
        # Asignamos los valores de ancho y alto a los atributos de la clase
        self.ancho_pantalla = ancho_pantalla
        self.alto_pantalla = alto_pantalla
        self.dificultad = dificultad
        self.estado = EstadoJuego()
        self.gestor_preguntas = GestorPreguntas(dificultad, categoria)
        self.renderizador = RenderizadorJuego(pantalla, ancho_pantalla, alto_pantalla)
        self.pantalla = pantalla
        self.resultados_respuestas = []  # Lista para guardar los resultados de cada respuesta
        self.insertar_juegos = InsertarJuegos()
        # Configuración de botones de pausa
        self.botones_pausa = [
            {"texto": "Reanudar", "accion": self.reanudar, "rect": pygame.Rect(0, 0, 200, 50)},
            {"texto": "Cambiar Jugador", "accion": self.cambiar_jugador, "rect": pygame.Rect(0, 0, 200, 50)},
            {"texto": "Volver al Menú", "accion": self.volver_menu, "rect": pygame.Rect(0, 0, 200, 50)},
            {"texto": "Salir", "accion": self.salir, "rect": pygame.Rect(0, 0, 200, 50)},
        ]
        # Inicializar el total y las preguntas restantes en el estado
        self.estado.preguntas_totales = len(self.gestor_preguntas.preguntas)
        self.estado.preguntas_restantes = self.estado.preguntas_totales

    def actualizar(self, eventos):
        self.pantalla.fill((255, 255, 255))

        if self.estado.juego_pausado:
            self.mostrar_pantalla_pausa()
            self.manejar_eventos_pausa(eventos)
            pygame.display.flip()
            return self.estado.juego_terminado

        if self.estado.juego_terminado:
            return self.estado.juego_terminado

        pregunta_actual = self.gestor_preguntas.obtener_pregunta_actual(self.estado.pregunta_actual)
        self.renderizador.dibujar_info_jugador(self.jugador, self.dificultad, self.estado)
        rectangulos_opciones, boton_verificar = self.renderizador.dibujar_pregunta(pregunta_actual, self.estado.respuesta_seleccionada)
        boton_pausa = self.renderizador.dibujar_menu_pausa()

        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                pos = evento.pos
                if boton_pausa.collidepoint(pos):
                    self.juego_pausado()
                if rectangulos_opciones:
                    self.manejar_seleccion_opcion(pos, rectangulos_opciones)
                if boton_verificar and boton_verificar.collidepoint(pos):
                    self.verificar_respuesta()

        pygame.display.flip()
        return self.estado.juego_terminado

    def manejar_seleccion_opcion(self, pos, rectangulos_opciones):
        for idx, rect in enumerate(rectangulos_opciones):
            if rect.collidepoint(pos):
                self.estado.respuesta_seleccionada = idx
                break

    def verificar_respuesta(self):
        if self.estado.respuesta_seleccionada is not None:
            pregunta_actual = self.gestor_preguntas.obtener_pregunta_actual(self.estado.pregunta_actual)
            correcta = pregunta_actual["correcta"] == self.estado.respuesta_seleccionada

            resultado = {
                "idPregunta": pregunta_actual["idPregunta"],
                "pregunta": pregunta_actual["pregunta"],
                "respuesta_seleccionada": self.estado.respuesta_seleccionada,
                "es_correcta": correcta,
                "puntaje_obtenido": 10 if correcta else 0
            }
            self.resultados_respuestas.append(resultado)

            if correcta:
                self.estado.respuestas_correctas += 1
                self.estado.puntaje += 10
                self.renderizador.mostrar_mensaje("¡Respuesta Correcta!", color=(0, 128, 0))
            else:
                self.estado.respuestas_incorrectas += 1
                self.renderizador.mostrar_mensaje("Respuesta Incorrecta", color=(255, 0, 0))

            pygame.display.flip()
            pygame.time.wait(1000)

            # Actualizar pregunta actual y preguntas restantes
            self.estado.pregunta_actual += 1
            self.estado.preguntas_restantes -= 1  # Disminuir las preguntas restantes
            self.estado.respuesta_seleccionada = None

            if self.estado.pregunta_actual >= self.estado.preguntas_totales:
                self.estado.juego_terminado = True
                self.mostrar_resultados_finales()
        else:
            self.renderizador.mostrar_mensaje("Seleccione una opción antes de verificar.", color=(255, 0, 0))


    def mostrar_resultados_finales(self):
        self.finalizar_juego(self.jugador[0],self.resultados_respuestas,self.estado.puntaje)
        self.renderizador.mostrar_mensaje(f"¡Juego terminado! Puntaje final: {self.estado.puntaje}",color=(0, 0, 255))
        
        
        
        print("Resultados de cada pregunta:")
        for resultado in self.resultados_respuestas:
            print(resultado)  # O puedes guardarlo en un archivo para consultas posteriores
    
    def finalizar_juego(self, id_usuario, respuestas, puntos_totales):
        """
        Registra el fin de un juego y guarda los resultados en la base de datos.
        :param id_usuario: ID del usuario que jugó el juego.
        :param respuestas: Lista de diccionarios con las respuestas del usuario. Cada diccionario debe tener:
                           - id_pregunta: ID de la pregunta.
                           - id_respuesta_usuario: ID de la respuesta seleccionada por el usuario.
                           - es_correcta: 1 si es correcta, 0 si es incorrecta.
        :param puntos_totales: Puntos totales obtenidos por el usuario.
        """
        # Obtener la fecha actual
        fecha_juego = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Insertar en historial_juegos y obtener el id_historial
        try:
            id_historial = self.insertar_juegos.insertar_historial_juego(id_usuario, fecha_juego, puntos_totales)
            print(f"Historial de juego registrado con ID: {id_historial}")

            # Insertar cada respuesta en detalles_historial
            for respuesta in respuestas:
                id_pregunta = respuesta['idPregunta']
                id_respuesta_usuario = respuesta['respuesta_seleccionada']
                es_correcta = respuesta['es_correcta']
                
                self.insertar_juegos.insertar_detalle_historial(id_historial, id_pregunta, id_respuesta_usuario, es_correcta)
                print(f"Detalle insertado para pregunta ID: {id_pregunta}")

            print("Juego finalizado y registrado con éxito.")
        except Exception as e:
            print(f"Error al finalizar el juego: {e}")

    
    def juego_pausado(self):
        """Alterna el estado de pausa del juego"""
        self.estado.juego_pausado = not self.estado.juego_pausado
    

    def mostrar_pantalla_pausa(self):
        """Muestra la pantalla de pausa con una lista de botones"""
        # Mostrar el mensaje "¡Juego Pausado!" en la parte superior y centrado
        mensaje_pausa = "¡Juego Pausado!"
        superficie_pausa = self.renderizador.fuente.render(mensaje_pausa, True, (255, 0, 0))

        # Calculamos las coordenadas para centrar el mensaje horizontalmente
        x_pausa = (self.ancho_pantalla - superficie_pausa.get_width()) // 2
        y_pausa = 50  # Puedes ajustar este valor si quieres que esté más cerca de la parte superior

        # Mostrar el mensaje "¡Juego Pausado!"
        self.pantalla.blit(superficie_pausa, (x_pausa, y_pausa))

        # Crear y dibujar los botones
        self.dibujar_botones_pausa()


    def dibujar_botones_pausa(self):
        """Dibuja los botones de la pantalla de pausa"""
        espacio_vertical = 80  # Espacio entre botones
        y_inicio = (self.alto_pantalla - (len(self.botones_pausa) * espacio_vertical)) // 2  # Centrado vertical

        # Distribuir los botones en la pantalla
        for i, boton in enumerate(self.botones_pausa):
            # Posición de cada botón
            boton["rect"].x = (self.ancho_pantalla - boton["rect"].width) // 2  # Centrado horizontal
            boton["rect"].y = y_inicio + i * espacio_vertical  # Espaciado vertical

            # Dibuja cada botón en la pantalla
            pygame.draw.rect(self.pantalla, (0, 0, 0), boton["rect"])  # Fondo del botón
            texto_boton = self.renderizador.fuente.render(boton["texto"], True, (255, 255, 255))
            self.pantalla.blit(texto_boton, boton["rect"].move(20, 10))  # Centrar texto dentro del botón


    def manejar_eventos_pausa(self, eventos):
        """Maneja los eventos de la pantalla de pausa"""
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                pos = evento.pos
                for boton in self.botones_pausa:
                    if boton["rect"].collidepoint(pos):  # Si el clic es sobre el botón
                        boton["accion"]()  # Ejecuta la acción asociada

    # Acciones de los botones
    def reanudar(self):
        """Reanuda el juego"""
        self.estado.juego_pausado = False

    def cambiar_jugador(self):
        """Cambiar jugador"""
        from Logica.seleccionar_jugador import SeleccionarJugador
        seleccionar_jugador = SeleccionarJugador(self.pantalla, self.ancho_pantalla, self.alto_pantalla)
        
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

    def volver_menu(self):
        """Volver al menú principal"""
        print("Volver al menú principal")
        from SistemaRetoTico.menu import Menu  # Import Menu here to avoid circular import issues
        menu = Menu(self.pantalla, self.ancho_pantalla, self.alto_pantalla)
        menu.show()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    menu.handle_click(event.pos)

        pygame.quit()

    def salir(self):
        """Salir del juego"""
        pygame.quit()
        exit()
