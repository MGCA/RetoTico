import pygame
# renderizador_juego.py
class RenderizadorJuego:
    def __init__(self, pantalla, ancho_pantalla, alto_pantalla):
        self.pantalla = pantalla
        self.ancho_pantalla = ancho_pantalla
        self.alto_pantalla = alto_pantalla
        self.fuente = pygame.font.Font(None, 36)
        self.juego_terminado = False  # Estado para saber si el juego ha terminado

    def dibujar_info_jugador(self, jugador, dificultad, estado):
        if not self.juego_terminado:
            info = [
                (f"Jugador: {jugador}", (20, 20)),
                (f"Dificultad: {dificultad}", (20, 60)),
                (f"Puntaje: {estado.puntaje}", (self.ancho_pantalla - 200, 20)),
                (f"Aciertos: {estado.respuestas_correctas}", (self.ancho_pantalla - 200, 60)),
                (f"Desaciertos: {estado.respuestas_incorrectas}", (self.ancho_pantalla - 200, 100)),
                (f"Total de Preguntas: {estado.preguntas_totales}", (20, 100)),
                (f"Preguntas Restantes: {estado.preguntas_restantes}", (20, 140)),
            ]
            for texto, pos in info:
                superficie = self.fuente.render(texto, True, (0, 0, 0))
                self.pantalla.blit(superficie, pos)

    def dibujar_pregunta(self, pregunta, respuesta_seleccionada):
        if not pregunta:
            return None, None  # Asegúrate de devolver exactamente dos valores cuando no haya pregunta.

        # Dibuja el texto de la pregunta
        superficie_pregunta = self.fuente.render(pregunta["pregunta"], True, (0, 0, 0))
        pos_x = (self.ancho_pantalla - superficie_pregunta.get_width()) // 2
        pos_y = (self.alto_pantalla - superficie_pregunta.get_height()) // 2
        self.pantalla.blit(superficie_pregunta, (pos_x, pos_y))
        
        # Dibuja las opciones
        rectangulos_opciones = []
        for idx, opcion in enumerate(pregunta["opciones"]):
            color = (0, 128, 0) if respuesta_seleccionada == idx else (0, 0, 0)
            rect_checkbox = pygame.Rect(self.ancho_pantalla // 2 - 100, 
                                    pos_y + 70 + (idx * 40), 20, 20)
            pygame.draw.rect(self.pantalla, color, rect_checkbox, 2)
            
            if respuesta_seleccionada == idx:
                pygame.draw.line(self.pantalla, color, 
                            (rect_checkbox.x + 5, rect_checkbox.y + 5),
                            (rect_checkbox.x + 15, rect_checkbox.y + 15), 2)
                pygame.draw.line(self.pantalla, color,
                            (rect_checkbox.x + 15, rect_checkbox.y + 5),
                            (rect_checkbox.x + 5, rect_checkbox.y + 15), 2)
            
            superficie_opcion = self.fuente.render(opcion, True, (0, 0, 0))
            self.pantalla.blit(superficie_opcion, (self.ancho_pantalla // 2 - 50, 
                                            pos_y + 70 + (idx * 40)))
            rectangulos_opciones.append(rect_checkbox)
        
        # Dibujar botón verificar
        ultima_opcion_y = pos_y + 70 + (len(pregunta["opciones"]) * 40)
        self.boton_verificar = self.dibujar_boton_verificar(ultima_opcion_y + 20)
            
        return rectangulos_opciones, self.boton_verificar

    def mostrar_mensaje(self, mensaje, posicion=None, tamaño=25, color=(0, 0, 0)):
        superficie = self.fuente.render(mensaje, True, color)
        if posicion is None:
            posicion = ((self.ancho_pantalla - superficie.get_width()) // 2,
                       self.alto_pantalla - superficie.get_height() - 20)
        self.pantalla.blit(superficie, posicion)

    def dibujar_boton_verificar(self, y):
            # Configuración del botón
            texto_boton = "Verificar"
            superficie_boton = self.fuente.render(texto_boton, True, (255, 255, 255))
            
            ancho_boton = superficie_boton.get_width() + 20
            alto_boton = superficie_boton.get_height() + 10
            x = (self.ancho_pantalla - ancho_boton) // 2

            # Crear el rectángulo del botón
            rect_boton = pygame.Rect(x, y, ancho_boton, alto_boton)

            # Dibujar el botón en la pantalla
            pygame.draw.rect(self.pantalla, (0, 128, 255), rect_boton)
            self.pantalla.blit(superficie_boton, (x + 10, y + 5))

            return rect_boton

    def dibujar_menu_terminado(self):
        # Mostrar mensaje de "Juego Terminado"
        self.mostrar_mensaje("¡Juego Terminado!", tamaño=50, color=(255, 0, 0))
        
        # Mostrar botones de opciones
        opciones = ["Volver a Jugar", "Cambiar Dificultad", "Cambiar Jugador", "Menú Principal", "Salir"]
        for idx, opcion in enumerate(opciones):
            y = self.alto_pantalla // 2 + 60 + (idx * 50)
            rect_boton = self.dibujar_boton_opcion(opcion, y)

    def dibujar_boton_opcion(self, texto, y):
        # Configuración del botón de opciones
        superficie_boton = self.fuente.render(texto, True, (255, 255, 255))
        
        ancho_boton = superficie_boton.get_width() + 20
        alto_boton = superficie_boton.get_height() + 10
        x = (self.ancho_pantalla - ancho_boton) // 2

        # Crear el rectángulo del botón
        rect_boton = pygame.Rect(x, y, ancho_boton, alto_boton)

        # Dibujar el botón en la pantalla
        pygame.draw.rect(self.pantalla, (0, 128, 0), rect_boton)
        self.pantalla.blit(superficie_boton, (x + 10, y + 5))

        return rect_boton

    def fin_juego(self):
        # Cambiar el estado del juego a "terminado"
        self.juego_terminado = True
        # Llamar a la función de mostrar el menú de fin de juego
        self.dibujar_menu_terminado()
        
        
    def dibujar_menu_pausa(self):
        # Configuración del botón de pausa
        texto_pausa = "Pausa"
        superficie_pausa = self.fuente.render(texto_pausa, True, (255, 255, 255))
        
        ancho_boton = superficie_pausa.get_width() + 20
        alto_boton = superficie_pausa.get_height() + 10
        x = self.ancho_pantalla - ancho_boton - 20  # Posición en la esquina inferior derecha
        y = self.alto_pantalla - alto_boton - 20

        # Crear el rectángulo del botón de pausa
        rect_boton_pausa = pygame.Rect(x, y, ancho_boton, alto_boton)

        # Dibujar el botón de pausa en la pantalla
        pygame.draw.rect(self.pantalla, (200, 0, 0), rect_boton_pausa)
        self.pantalla.blit(superficie_pausa, (x + 10, y + 5))

        return rect_boton_pausa
    