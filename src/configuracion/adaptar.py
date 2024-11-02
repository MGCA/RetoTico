import sqlite3
import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
from tkinter import ttk
from PIL import Image, ImageTk
import random
import os

# Conexión a la base de datos SQLite
conn = sqlite3.connect('retoticoJunior.db')
cursor = conn.cursor()

# Crear tablas necesarias
cursor.execute('''
CREATE TABLE IF NOT EXISTS jugadores (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL UNIQUE,
    avatar BLOB,
    puntos INTEGER DEFAULT 0,
    nivel INTEGER DEFAULT 1,
    estrellas INTEGER DEFAULT 0
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS categorias (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    imagen BLOB
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS preguntas (
    id INTEGER PRIMARY KEY,
    categoria_id INTEGER,
    pregunta TEXT NOT NULL,
    respuesta_correcta TEXT NOT NULL,
    opcion1 TEXT NOT NULL,
    opcion2 TEXT NOT NULL,
    opcion3 TEXT NOT NULL,
    FOREIGN KEY (categoria_id) REFERENCES categorias(id)
)
''')
conn.commit()

# Agregar categorías predeterminadas si no existen
categorias_predeterminadas = [
    (1, 'Historia', None),
    (2, 'Geografía', None),
    (3, 'Fauna y Flora', None),
    (4, 'Cultura y Tradiciones', None)
]
cursor.executemany('INSERT OR IGNORE INTO categorias (id, nombre, imagen) VALUES (?, ?, ?)', categorias_predeterminadas)
conn.commit()

# Agregar preguntas predeterminadas si no existen
preguntas_predeterminadas = [
    # Categoria de Historia
    pregunta, respuesta_correcta, opcion1, opcion2, opcion3, categoria_id
    ("¿En qué año se abolió el ejército en Costa Rica?", "1949", "1821", "1972", "1994", 1),
    ("¿Quién fue el primer presidente de Costa Rica?", "José María Castro Madriz", "Juan Mora Fernández", "Alfredo González Flores", "Rafael Ángel Calderón Guardia", 1),
    ("¿Qué batalla famosa se libró en 1856?", "Batalla de Santa Rosa", "Batalla de Rivas", "Batalla de la Trinidad", "Batalla de Sardinal", 1),
    ("¿Qué tratado se firmó para definir las fronteras con Nicaragua?", "Tratado Cañas-Jerez", "Tratado Limón-Matagalpa", "Tratado de Managua", "Tratado de San José", 1),
    ("¿Cuál fue el propósito principal de la Campaña Nacional?", "Expulsar a los filibusteros", "Abolir el ejército", "Firmar la independencia", "Nacionalizar los bancos", 1),


    # Categoria de Geografía
    pregunta, respuesta_correcta, opcion1, opcion2, opcion3, categoria_id
    ("¿Cuál es el volcán más alto de Costa Rica?", "Cerro Chirripó", "Volcán Poás", "Volcán Arenal", "Volcán Turrialba", 2),
    ("¿Cuántas provincias tiene Costa Rica?", "7", "5", "9", "8", 2),
    ("¿Cuál es el río más largo de Costa Rica?", "Río San Juan", "Río Tempisque", "Río Grande de Térraba", "Río Reventazón", 2),
    ("¿Qué parque nacional es famoso por sus tortugas marinas?", "Parque Nacional Tortuguero", "Parque Nacional Corcovado", "Parque Nacional Manuel Antonio", "Parque Nacional Cahuita", 2),
    ("¿Cuál es el pico más alto de Costa Rica?", "Cerro Chirripó", "Cerro de la Muerte", "Cerro Kamuk", "Volcán Irazú", 2),

    # Categoria de Fauna y Flora
    pregunta, respuesta_correcta, opcion1, opcion2, opcion3, categoria_id
    ("¿Cuál es el ave nacional de Costa Rica?", "Yigüirro", "Tucán", "Quetzal", "Colibrí", 3),
    ("¿Qué rana es conocida por su color rojo y ojos verdes?", "Rana flecha roja", "Rana de árbol verde", "Rana toro", "Rana perezosa", 3),
    ("¿Qué mariposa es símbolo de transformación en Costa Rica?", "Mariposa morfo azul", "Mariposa monarca", "Mariposa cristal", "Mariposa nocturna", 3),
    ("¿Cuál es el animal que representa al perezoso en la fauna costarricense?", "Pereza de tres dedos", "Mono capuchino", "Oso perezoso", "Pereza de dos dedos", 3),
    ("¿Qué flor es la nacional?", "Orquídea Guaria Morada", "Rosa", "Margarita", "Girasol", 3),

    # Categoria de Cultura y Tradiciones
    pregunta, respuesta_correcta, opcion1, opcion2, opcion3, categoria_id
    ("¿Qué significa “Pura Vida”?", "Buenas vibras", "Vida sencilla", "Salud", "Felicidad", 4),
    ("¿Qué festividad se celebra el 15 de septiembre?", "Día de la Independencia", "Día del Trabajo", "Día de San José", "Día del Agricultor", 4),
    ("¿Qué bebida es popular durante las fiestas navideñas?", "Rompope", "Cerveza", "Ron", "Vino", 4),
    ("¿Qué día se celebra el Día del Agricultor?", "15 de mayo", "1 de abril", "10 de agosto", "25 de diciembre", 4)
]

# Insertar preguntas predeterminadas
for pregunta in preguntas_predeterminadas:
    cursor.execute('''
    INSERT OR IGNORE INTO preguntas (pregunta, respuesta_correcta, opcion1, opcion2, opcion3, categoria_id)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (pregunta[0], pregunta[1], pregunta[2], pregunta[3], pregunta[4], pregunta[5]))
conn.commit()

# Variables globales
jugador_id = None
puntaje_actual = 0
estrellas_actuales = 0
avatar_blob_global = None
avatar_imagen = None

# Nueva Paleta de colores inspirada en Costa Rica
colores = {
    'fondo_principal': '#0B4F6C',        # Azul profundo
    'texto_principal': '#FFFFFF',        # Blanco
    'boton_fondo': '#D62828',            # Rojo vibrante
    'boton_texto': '#FFFFFF',            # Blanco
    'entrada_fondo': '#FFFFFF',          # Blanco
    'entrada_texto': '#0B4F6C',          # Azul oscuro
    'opcion_fondo': ['#0B4F6C', '#D62828', '#F77F00', '#FCBF49'],  # Azul profundo, Rojo vibrante, Naranja brillante, Amarillo dorado
    'opcion_texto': '#FFFFFF',           # Blanco
    'fondo_secundario': '#0B4F6C',        # Mismo color que el fondo principal (Azul profundo)
    'lista_fondo': '#FFFFFF',            # Blanco
    'lista_texto': '#0B4F6C',            # Azul oscuro
    'seleccion_fondo': '#F77F00',        # Naranja brillante
    'boton_iniciar': '#F77F00',          # Naranja brillante
    'estrellas_color': '#FCBF49',        # Amarillo dorado
    'estrellas_texto': '#FCBF49',        # Amarillo dorado
    'boton_avatar_nina': '#3A86FF',      # Azul vibrante
    'boton_cargar_avatar': '#8ECAE6',    # Azul claro
}

# Fuentes personalizadas
# Asegúrate de tener instalada la fuente "Press Start 2P" o cambia el nombre de la fuente a una que tengas instalada.
fuente_titulo = ("Press Start 2P", 14, "bold")
fuente_texto = ("Press Start 2P", 10)
fuente_boton = ("Press Start 2P", 10, "bold")
fuente_boton_grande = ("Press Start 2P", 12, "bold")
fuente_listbox = ("Press Start 2P", 10)

# Función para centrar una ventana en la pantalla
def centrar_ventana(ventana):
    ventana.update_idletasks()
    ancho = ventana.winfo_width()
    alto = ventana.winfo_height()
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    x = (pantalla_ancho // 2) - (ancho // 2)
    y = (pantalla_alto // 2) - (alto // 2)
    ventana.geometry(f'{ancho}x{alto}+{x}+{y}')
    ventana.resizable(False, False)

# Función para cargar y mostrar un avatar personalizado
def cargar_avatar_personalizado():
    global avatar_blob_global
    avatar_path = filedialog.askopenfilename(title="Seleccione un Avatar", filetypes=[("Archivos de imagen", "*.png;*.jpg;*.jpeg")])
    if avatar_path:
        try:
            with open(avatar_path, 'rb') as file:
                avatar_blob_global = file.read()
            mostrar_avatar(avatar_blob_global)
            actualizar_avatar_en_bd()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el avatar: {e}")

# Función para cargar y mostrar un avatar predeterminado
def cargar_avatar_predeterminado(ruta):
    global avatar_blob_global
    ruta_completa = os.path.join(os.path.dirname(__file__), ruta)
    if os.path.exists(ruta_completa):
        try:
            with open(ruta_completa, 'rb') as file:
                avatar_blob_global = file.read()
            mostrar_avatar(avatar_blob_global)
            actualizar_avatar_en_bd()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el avatar: {e}")
    else:
        messagebox.showerror("Error", f"No se encontró el archivo: {ruta_completa}")

# Función para mostrar el avatar en la interfaz
def mostrar_avatar(avatar_blob):
    global avatar_imagen
    if avatar_blob:
        try:
            with open("temp_avatar.png", "wb") as file:
                file.write(avatar_blob)
            imagen = Image.open("temp_avatar.png").resize((150, 150), Image.LANCZOS)
            avatar_imagen = ImageTk.PhotoImage(imagen)
            avatar_label.config(image=avatar_imagen)
            avatar_label.image = avatar_imagen
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo mostrar el avatar: {e}")
        finally:
            if os.path.exists("temp_avatar.png"):
                os.remove("temp_avatar.png")

# Función para actualizar el avatar en la base de datos
def actualizar_avatar_en_bd():
    if jugador_id is not None:
        try:
            cursor.execute("UPDATE jugadores SET avatar = ? WHERE id = ?", (avatar_blob_global, jugador_id))
            conn.commit()
        except sqlite3.Error as e:
            messagebox.showerror("Error de Base de Datos", f"No se pudo actualizar el avatar: {e}")

# Función para registrar o cargar un jugador
def registrar_jugador():
    global avatar_blob_global, jugador_id, puntaje_actual, estrellas_actuales
    nombre = nombre_entry.get().strip()
    if not nombre:
        messagebox.showwarning("Advertencia", "Ingrese un nombre válido.")
        return
    if not avatar_blob_global:
        messagebox.showwarning("Advertencia", "Seleccione un avatar.")
        return
    try:
        cursor.execute("SELECT id, puntos, estrellas FROM jugadores WHERE nombre = ?", (nombre,))
        jugador = cursor.fetchone()
        if jugador:
            respuesta = messagebox.askyesno("Jugador Existente", f"El jugador '{nombre}' ya existe. ¿Desea cargar el perfil?")
            if respuesta:
                jugador_id, puntaje_actual, estrellas_actuales = jugador
                puntaje_label.config(text=f"Puntaje: {puntaje_actual}")
                actualizar_estrellas_visual()
                messagebox.showinfo("Perfil Cargado", f"Perfil de '{nombre}' cargado con éxito.")
                registrar_button.config(state=tk.DISABLED)
            else:
                messagebox.showinfo("Nombre en Uso", "El nombre ingresado ya está en uso. Por favor, ingrese un nombre diferente.")
                return
        else:
            cursor.execute("INSERT INTO jugadores (nombre, avatar) VALUES (?, ?)", (nombre, avatar_blob_global))
            conn.commit()
            cursor.execute("SELECT id, puntos, estrellas FROM jugadores WHERE nombre = ?", (nombre,))
            jugador = cursor.fetchone()
            jugador_id, puntaje_actual, estrellas_actuales = jugador
            puntaje_label.config(text=f"Puntaje: {puntaje_actual}")
            actualizar_estrellas_visual()
            messagebox.showinfo("Registro Exitoso", f"Jugador '{nombre}' registrado con éxito.")
            registrar_button.config(state=tk.DISABLED)
    except sqlite3.Error as e:
        messagebox.showerror("Error de Base de Datos", f"No se pudo registrar o cargar el jugador: {e}")

# Función para buscar un jugador existente
def buscar_jugador():
    global jugador_id, puntaje_actual, avatar_blob_global, estrellas_actuales
    nombre = nombre_entry.get().strip()
    if not nombre:
        messagebox.showwarning("Advertencia", "Ingrese un nombre válido.")
        return
    try:
        cursor.execute("SELECT id, puntos, avatar, estrellas FROM jugadores WHERE nombre = ?", (nombre,))
        jugador = cursor.fetchone()
        if jugador:
            jugador_id, puntaje_actual, avatar_blob, estrellas_actuales = jugador
            puntaje_label.config(text=f"Puntaje: {puntaje_actual}")
            avatar_blob_global = avatar_blob
            mostrar_avatar(avatar_blob_global)
            actualizar_estrellas_visual()
            messagebox.showinfo("Perfil Cargado", f"Perfil de '{nombre}' cargado con éxito.")
            registrar_button.config(state=tk.DISABLED)
        else:
            messagebox.showinfo("Jugador No Encontrado", f"No se encontró ningún jugador con el nombre '{nombre}'.")
            registrar_button.config(state=tk.NORMAL)
    except sqlite3.Error as e:
        messagebox.showerror("Error de Base de Datos", f"No se pudo buscar el jugador: {e}")

# Función para actualizar la visualización de las estrellas
def actualizar_estrellas_visual():
    global estrellas_label, estrellas_actuales
    estrellas_actuales = min(puntaje_actual // 100, 10)
    estrellas = '★' * estrellas_actuales
    estrellas_label.config(text=f"Estrellas: {estrellas}", fg=colores['estrellas_texto'])

# Función para abrir el mantenimiento de categorías y preguntas
def abrir_mantenimiento():
    mantenimiento_window = tk.Toplevel(root)
    mantenimiento_window.title("Mantenimiento de Categorías y Preguntas")
    mantenimiento_window.configure(bg=colores['fondo_principal'])  # Cambiado a fondo_principal

    # Crear un Notebook (pestañas) para separar categorías y preguntas
    notebook = ttk.Notebook(mantenimiento_window)
    notebook.pack(fill='both', expand=True)

    # Estilos para las pestañas
    style = ttk.Style()
    style.configure('TNotebook.Tab', font=fuente_boton)

    # Pestaña de Categorías
    tab_categorias = tk.Frame(notebook, bg=colores['fondo_principal'])  # Cambiado a fondo_principal
    notebook.add(tab_categorias, text='Categorías')

    # Pestaña de Preguntas
    tab_preguntas = tk.Frame(notebook, bg=colores['fondo_principal'])  # Cambiado a fondo_principal
    notebook.add(tab_preguntas, text='Preguntas')

    # ===================== SECCIÓN DE CATEGORÍAS =====================
    categorias_frame = tk.Frame(tab_categorias, bg=colores['fondo_principal'])  # Cambiado a fondo_principal
    categorias_frame.pack(fill='both', expand=True, padx=10, pady=10)

    # Lista de categorías con scrollbar
    lista_categorias_frame = tk.Frame(categorias_frame, bg=colores['fondo_principal'])  # Cambiado a fondo_principal
    lista_categorias_frame.pack(fill='both', expand=True)

    scrollbar_categorias = tk.Scrollbar(lista_categorias_frame)
    scrollbar_categorias.pack(side=tk.RIGHT, fill=tk.Y)

    lista_categorias = tk.Listbox(lista_categorias_frame, width=40, height=20, font=fuente_listbox,
                                  bg=colores['lista_fondo'], fg=colores['lista_texto'],
                                  selectbackground=colores['seleccion_fondo'],
                                  yscrollcommand=scrollbar_categorias.set)
    lista_categorias.pack(side=tk.LEFT, fill='both', expand=True)
    scrollbar_categorias.config(command=lista_categorias.yview)

    def actualizar_lista_categorias():
        lista_categorias.delete(0, tk.END)
        try:
            cursor.execute("SELECT * FROM categorias")
            for categoria in cursor.fetchall():
                lista_categorias.insert(tk.END, f"{categoria[0]} - {categoria[1]}")
        except sqlite3.Error as e:
            messagebox.showerror("Error de Base de Datos", f"No se pudieron cargar las categorías: {e}")

    actualizar_lista_categorias()

    # Botones para Categorías
    botones_categorias_frame = tk.Frame(categorias_frame, bg=colores['fondo_principal'])  # Cambiado a fondo_principal
    botones_categorias_frame.pack(pady=10)

    # Cargar imágenes para los botones
    try:
        agregar_icon = ImageTk.PhotoImage(Image.open("agregar.png").resize((30, 30), Image.LANCZOS))
        modificar_icon = ImageTk.PhotoImage(Image.open("modificar.png").resize((30, 30), Image.LANCZOS))
        borrar_icon = ImageTk.PhotoImage(Image.open("borrar.png").resize((30, 30), Image.LANCZOS))
    except Exception as e:
        messagebox.showerror("Error de Imagen", f"No se pudieron cargar las imágenes de los botones: {e}")
        mantenimiento_window.destroy()
        return

    def agregar_categoria():
        nombre_categoria = simpledialog.askstring("Agregar Categoría", "Ingrese el nombre de la nueva categoría:")
        if nombre_categoria:
            try:
                cursor.execute("INSERT INTO categorias (nombre) VALUES (?)", (nombre_categoria,))
                conn.commit()
                actualizar_lista_categorias()
            except sqlite3.Error as e:
                messagebox.showerror("Error de Base de Datos", f"No se pudo agregar la categoría: {e}")

    def editar_categoria():
        seleccion = lista_categorias.curselection()
        if seleccion:
            categoria_info = lista_categorias.get(seleccion[0])
            categoria_id = int(categoria_info.split(" - ")[0])
            nombre_actual = categoria_info.split(" - ")[1]
            nuevo_nombre = simpledialog.askstring("Modificar Categoría", "Ingrese el nuevo nombre de la categoría:", initialvalue=nombre_actual)
            if nuevo_nombre:
                try:
                    cursor.execute("UPDATE categorias SET nombre = ? WHERE id = ?", (nuevo_nombre, categoria_id))
                    conn.commit()
                    actualizar_lista_categorias()
                except sqlite3.Error as e:
                    messagebox.showerror("Error de Base de Datos", f"No se pudo modificar la categoría: {e}")
        else:
            messagebox.showwarning("Selección Vacía", "Seleccione una categoría para modificar.")

    def eliminar_categoria():
        seleccion = lista_categorias.curselection()
        if seleccion:
            categoria_info = lista_categorias.get(seleccion[0])
            categoria_id = int(categoria_info.split(" - ")[0])
            respuesta = messagebox.askyesno("Borrar Categoría", "¿Está seguro de que desea borrar esta categoría y todas sus preguntas asociadas?")
            if respuesta:
                try:
                    cursor.execute("DELETE FROM preguntas WHERE categoria_id = ?", (categoria_id,))
                    cursor.execute("DELETE FROM categorias WHERE id = ?", (categoria_id,))
                    conn.commit()
                    actualizar_lista_categorias()
                    actualizar_lista_preguntas()
                except sqlite3.Error as e:
                    messagebox.showerror("Error de Base de Datos", f"No se pudo borrar la categoría: {e}")
        else:
            messagebox.showwarning("Selección Vacía", "Seleccione una categoría para borrar.")

    # ======= Modificación Solicitada: Botón "Agregar Categoría" con texto "Agregar" y su icono =======
    boton_agregar = tk.Button(
        botones_categorias_frame,
        image=agregar_icon,
        text="Agregar",  # Añadir texto
        compound='left',  # Mostrar la imagen a la izquierda del texto
        command=agregar_categoria,
        bg=colores['boton_fondo'],        # Rojo vibrante
        fg=colores['boton_texto'],        # Blanco
        font=fuente_boton,
        activebackground='#B22222',        # Rojo más oscuro al presionar
        activeforeground='#FFFFFF',        # Blanco al presionar
        bd=0,                              # Sin borde para un aspecto más moderno
        highlightthickness=0,              # Sin contorno
        cursor='hand2'                     # Cambiar el cursor al pasar sobre el botón
    )
    boton_agregar.image = agregar_icon
    boton_agregar.pack(side=tk.LEFT, padx=5)
    # ================================================================================

    boton_modificar = tk.Button(
        botones_categorias_frame,
        text="Modificar",
        image=modificar_icon,
        compound='left',
        command=editar_categoria,
        bg='#D62828',                      # Rojo vibrante
        fg=colores['boton_texto'],        # Blanco
        font=fuente_boton,
        activebackground='#B22222',        # Rojo más oscuro al presionar
        activeforeground='#FFFFFF',        # Blanco al presionar
        bd=0,                              # Sin borde
        highlightthickness=0,
        cursor='hand2'
    )
    boton_modificar.image = modificar_icon
    boton_modificar.pack(side=tk.LEFT, padx=5)

    boton_borrar = tk.Button(
        botones_categorias_frame,
        text="Borrar",
        image=borrar_icon,
        compound='left',
        command=eliminar_categoria,
        bg='#F77F00',                      # Naranja brillante
        fg=colores['boton_texto'],        # Blanco
        font=fuente_boton,
        activebackground='#D2691E',        # Marrón más oscuro al presionar
        activeforeground='#FFFFFF',        # Blanco al presionar
        bd=0,                              # Sin borde
        highlightthickness=0,
        cursor='hand2'
    )
    boton_borrar.image = borrar_icon
    boton_borrar.pack(side=tk.LEFT, padx=5)
    # ================================================================================

    # ===================== SECCIÓN DE PREGUNTAS =====================
    preguntas_frame = tk.Frame(tab_preguntas, bg=colores['fondo_principal'])  # Cambiado a fondo_principal
    preguntas_frame.pack(fill='both', expand=True, padx=10, pady=10)

    # Lista de preguntas con scrollbar
    lista_preguntas_frame = tk.Frame(preguntas_frame, bg=colores['fondo_principal'])  # Cambiado a fondo_principal
    lista_preguntas_frame.pack(fill='both', expand=True)

    scrollbar_preguntas = tk.Scrollbar(lista_preguntas_frame)
    scrollbar_preguntas.pack(side=tk.RIGHT, fill=tk.Y)

    lista_preguntas = tk.Listbox(lista_preguntas_frame, width=80, height=20, font=fuente_listbox,
                                 bg=colores['lista_fondo'], fg=colores['lista_texto'],
                                 selectbackground=colores['seleccion_fondo'],
                                 yscrollcommand=scrollbar_preguntas.set)
    lista_preguntas.pack(side=tk.LEFT, fill='both', expand=True)
    scrollbar_preguntas.config(command=lista_preguntas.yview)

    def actualizar_lista_preguntas():
        lista_preguntas.delete(0, tk.END)
        try:
            cursor.execute("SELECT preguntas.id, categorias.nombre, preguntas.pregunta FROM preguntas JOIN categorias ON preguntas.categoria_id = categorias.id")
            for pregunta in cursor.fetchall():
                lista_preguntas.insert(tk.END, f"{pregunta[0]} - {pregunta[1]}: {pregunta[2]}")
        except sqlite3.Error as e:
            messagebox.showerror("Error de Base de Datos", f"No se pudieron cargar las preguntas: {e}")

    actualizar_lista_preguntas()

    # Botones para Preguntas
    botones_preguntas_frame = tk.Frame(preguntas_frame, bg=colores['fondo_principal'])  # Cambiado a fondo_principal
    botones_preguntas_frame.pack(pady=10)

    # Cargar imágenes para los botones de preguntas
    try:
        agregar_pregunta_icon = ImageTk.PhotoImage(Image.open("agregar.png").resize((30, 30), Image.LANCZOS))
        modificar_pregunta_icon = ImageTk.PhotoImage(Image.open("modificar.png").resize((30, 30), Image.LANCZOS))
        borrar_pregunta_icon = ImageTk.PhotoImage(Image.open("borrar.png").resize((30, 30), Image.LANCZOS))
    except Exception as e:
        messagebox.showerror("Error de Imagen", f"No se pudieron cargar las imágenes de los botones de preguntas: {e}")
        mantenimiento_window.destroy()
        return

    def agregar_pregunta():
        agregar_pregunta_window = tk.Toplevel(mantenimiento_window)
        agregar_pregunta_window.title("Agregar Pregunta")
        agregar_pregunta_window.configure(bg=colores['fondo_principal'])  # Cambiado a fondo_principal

        # Crear el contenido de la ventana
        tk.Label(agregar_pregunta_window, text="Categoría:", bg=colores['fondo_principal'],
                 fg=colores['texto_principal'], font=fuente_texto).pack(pady=5)
        categorias_disponibles = cursor.execute("SELECT id, nombre FROM categorias").fetchall()
        if not categorias_disponibles:
            messagebox.showwarning("Sin Categorías", "Debe crear al menos una categoría antes de agregar preguntas.")
            agregar_pregunta_window.destroy()
            return

        categoria_var = tk.StringVar(agregar_pregunta_window)
        categoria_var.set(categorias_disponibles[0][1])

        categoria_menu = tk.OptionMenu(agregar_pregunta_window, categoria_var, *[c[1] for c in categorias_disponibles])
        categoria_menu.config(font=fuente_texto)
        categoria_menu.pack(pady=5)

        tk.Label(agregar_pregunta_window, text="Pregunta:", bg=colores['fondo_principal'],
                 fg=colores['texto_principal'], font=fuente_texto).pack(pady=5)
        pregunta_entry = tk.Entry(agregar_pregunta_window, width=60, font=fuente_texto)
        pregunta_entry.pack(pady=5)

        tk.Label(agregar_pregunta_window, text="Respuesta Correcta:", bg=colores['fondo_principal'],
                 fg=colores['texto_principal'], font=fuente_texto).pack(pady=5)
        respuesta_correcta_entry = tk.Entry(agregar_pregunta_window, width=60, font=fuente_texto)
        respuesta_correcta_entry.pack(pady=5)

        tk.Label(agregar_pregunta_window, text="Opción 1:", bg=colores['fondo_principal'],
                 fg=colores['texto_principal'], font=fuente_texto).pack(pady=5)
        opcion1_entry = tk.Entry(agregar_pregunta_window, width=60, font=fuente_texto)
        opcion1_entry.pack(pady=5)

        tk.Label(agregar_pregunta_window, text="Opción 2:", bg=colores['fondo_principal'],
                 fg=colores['texto_principal'], font=fuente_texto).pack(pady=5)
        opcion2_entry = tk.Entry(agregar_pregunta_window, width=60, font=fuente_texto)
        opcion2_entry.pack(pady=5)

        tk.Label(agregar_pregunta_window, text="Opción 3:", bg=colores['fondo_principal'],
                 fg=colores['texto_principal'], font=fuente_texto).pack(pady=5)
        opcion3_entry = tk.Entry(agregar_pregunta_window, width=60, font=fuente_texto)
        opcion3_entry.pack(pady=5)

        def guardar_pregunta():
            categoria_id = next(c[0] for c in categorias_disponibles if c[1] == categoria_var.get())
            pregunta = pregunta_entry.get().strip()
            respuesta_correcta = respuesta_correcta_entry.get().strip()
            opcion1 = opcion1_entry.get().strip()
            opcion2 = opcion2_entry.get().strip()
            opcion3 = opcion3_entry.get().strip()

            if not all([pregunta, respuesta_correcta, opcion1, opcion2, opcion3]):
                messagebox.showwarning("Campos Vacíos", "Todos los campos deben ser completados.")
                return

            try:
                cursor.execute('''
                INSERT INTO preguntas (categoria_id, pregunta, respuesta_correcta, opcion1, opcion2, opcion3)
                VALUES (?, ?, ?, ?, ?, ?)
                ''', (categoria_id, pregunta, respuesta_correcta, opcion1, opcion2, opcion3))
                conn.commit()
                actualizar_lista_preguntas()
                agregar_pregunta_window.destroy()
            except sqlite3.Error as e:
                messagebox.showerror("Error de Base de Datos", f"No se pudo agregar la pregunta: {e}")

        # ======= Modificación Solicitada: Botón "Agregar" con icono =======
        boton_guardar = tk.Button(
            agregar_pregunta_window,
            text="Agregar",
            image=agregar_pregunta_icon,
            compound='left',  # Imagen a la izquierda del texto
            command=guardar_pregunta,
            bg=colores['boton_fondo'],
            fg=colores['boton_texto'],
            font=fuente_boton,
            activebackground='#B22222',  # Rojo más oscuro
            activeforeground='#FFFFFF',
            bd=0,
            highlightthickness=0,
            cursor='hand2'
        )
        boton_guardar.image = agregar_pregunta_icon
        boton_guardar.pack(pady=10)
        # ===============================================================

        agregar_pregunta_window.update()
        centrar_ventana(agregar_pregunta_window)

    def editar_pregunta():
        seleccion = lista_preguntas.curselection()
        if seleccion:
            pregunta_info = lista_preguntas.get(seleccion[0])
            pregunta_id = int(pregunta_info.split(" - ")[0])

            try:
                cursor.execute("SELECT * FROM preguntas WHERE id = ?", (pregunta_id,))
                pregunta = cursor.fetchone()
            except sqlite3.Error as e:
                messagebox.showerror("Error de Base de Datos", f"No se pudo obtener la pregunta: {e}")
                return

            editar_pregunta_window = tk.Toplevel(mantenimiento_window)
            editar_pregunta_window.title("Editar Pregunta")
            editar_pregunta_window.configure(bg=colores['fondo_principal'])  # Cambiado a fondo_principal

            tk.Label(editar_pregunta_window, text="Categoría:", bg=colores['fondo_principal'],
                     fg=colores['texto_principal'], font=fuente_texto).pack(pady=5)
            categorias_disponibles = cursor.execute("SELECT id, nombre FROM categorias").fetchall()
            categoria_var = tk.StringVar(editar_pregunta_window)
            categoria_actual = next(c[1] for c in categorias_disponibles if c[0] == pregunta[1])
            categoria_var.set(categoria_actual)

            categoria_menu = tk.OptionMenu(editar_pregunta_window, categoria_var, *[c[1] for c in categorias_disponibles])
            categoria_menu.config(font=fuente_texto)
            categoria_menu.pack(pady=5)

            tk.Label(editar_pregunta_window, text="Pregunta:", bg=colores['fondo_principal'],
                     fg=colores['texto_principal'], font=fuente_texto).pack(pady=5)
            pregunta_entry = tk.Entry(editar_pregunta_window, width=60, font=fuente_texto)
            pregunta_entry.insert(0, pregunta[2])
            pregunta_entry.pack(pady=5)

            tk.Label(editar_pregunta_window, text="Respuesta Correcta:", bg=colores['fondo_principal'],
                     fg=colores['texto_principal'], font=fuente_texto).pack(pady=5)
            respuesta_correcta_entry = tk.Entry(editar_pregunta_window, width=60, font=fuente_texto)
            respuesta_correcta_entry.insert(0, pregunta[3])
            respuesta_correcta_entry.pack(pady=5)

            tk.Label(editar_pregunta_window, text="Opción 1:", bg=colores['fondo_principal'],
                     fg=colores['texto_principal'], font=fuente_texto).pack(pady=5)
            opcion1_entry = tk.Entry(editar_pregunta_window, width=60, font=fuente_texto)
            opcion1_entry.insert(0, pregunta[4])
            opcion1_entry.pack(pady=5)

            tk.Label(editar_pregunta_window, text="Opción 2:", bg=colores['fondo_principal'],
                     fg=colores['texto_principal'], font=fuente_texto).pack(pady=5)
            opcion2_entry = tk.Entry(editar_pregunta_window, width=60, font=fuente_texto)
            opcion2_entry.insert(0, pregunta[5])
            opcion2_entry.pack(pady=5)

            tk.Label(editar_pregunta_window, text="Opción 3:", bg=colores['fondo_principal'],
                     fg=colores['texto_principal'], font=fuente_texto).pack(pady=5)
            opcion3_entry = tk.Entry(editar_pregunta_window, width=60, font=fuente_texto)
            opcion3_entry.insert(0, pregunta[6])
            opcion3_entry.pack(pady=5)

            def actualizar_pregunta():
                categoria_id = next(c[0] for c in categorias_disponibles if c[1] == categoria_var.get())
                pregunta_texto = pregunta_entry.get().strip()
                respuesta_correcta = respuesta_correcta_entry.get().strip()
                opcion1 = opcion1_entry.get().strip()
                opcion2 = opcion2_entry.get().strip()
                opcion3 = opcion3_entry.get().strip()

                if not all([pregunta_texto, respuesta_correcta, opcion1, opcion2, opcion3]):
                    messagebox.showwarning("Campos Vacíos", "Todos los campos deben ser completados.")
                    return

                try:
                    cursor.execute('''
                    UPDATE preguntas
                    SET categoria_id = ?, pregunta = ?, respuesta_correcta = ?, opcion1 = ?, opcion2 = ?, opcion3 = ?
                    WHERE id = ?
                    ''', (categoria_id, pregunta_texto, respuesta_correcta, opcion1, opcion2, opcion3, pregunta_id))
                    conn.commit()
                    actualizar_lista_preguntas()
                    editar_pregunta_window.destroy()
                except sqlite3.Error as e:
                    messagebox.showerror("Error de Base de Datos", f"No se pudo actualizar la pregunta: {e}")

            # ======= Modificación Solicitada: Botón "Actualizar" con icono =======
            boton_actualizar = tk.Button(
                editar_pregunta_window,
                text="Actualizar",
                image=modificar_pregunta_icon,
                compound='left',  # Imagen a la izquierda del texto
                command=actualizar_pregunta,
                bg=colores['boton_fondo'],
                fg=colores['boton_texto'],
                font=fuente_boton,
                activebackground='#B22222',  # Rojo más oscuro
                activeforeground='#FFFFFF',
                bd=0,
                highlightthickness=0,
                cursor='hand2'
            )
            boton_actualizar.image = modificar_pregunta_icon
            boton_actualizar.pack(pady=10)
            # =============================================================

            editar_pregunta_window.update()
            centrar_ventana(editar_pregunta_window)
        else:
            messagebox.showwarning("Selección Vacía", "Seleccione una pregunta para modificar.")

    def eliminar_pregunta():
        seleccion = lista_preguntas.curselection()
        if seleccion:
            pregunta_info = lista_preguntas.get(seleccion[0])
            pregunta_id = int(pregunta_info.split(" - ")[0])
            respuesta = messagebox.askyesno("Eliminar Pregunta", "¿Está seguro de que desea eliminar esta pregunta?")
            if respuesta:
                try:
                    cursor.execute("DELETE FROM preguntas WHERE id = ?", (pregunta_id,))
                    conn.commit()
                    actualizar_lista_preguntas()
                except sqlite3.Error as e:
                    messagebox.showerror("Error de Base de Datos", f"No se pudo eliminar la pregunta: {e}")
        else:
            messagebox.showwarning("Selección Vacía", "Seleccione una pregunta para eliminar.")

    # ======= Modificación Solicitada: Textos e iconos de los botones de preguntas =======
    boton_agregar_pregunta = tk.Button(
        botones_preguntas_frame,
        text="Agregar",
        image=agregar_pregunta_icon,
        compound='left',  # Imagen a la izquierda del texto
        command=agregar_pregunta,
        bg=colores['opcion_fondo'][2],  # Naranja brillante
        fg=colores['boton_texto'],
        font=fuente_boton,
        activebackground='#E07A5F',  # Naranja más oscuro al presionar
        activeforeground='#FFFFFF',
        bd=0,
        highlightthickness=0,
        cursor='hand2'
    )
    boton_agregar_pregunta.image = agregar_pregunta_icon
    boton_agregar_pregunta.pack(side=tk.LEFT, padx=5)

    boton_editar_pregunta = tk.Button(
        botones_preguntas_frame,
        text="Modificar",  # Texto cambiado de "Editar" a "Modificar"
        image=modificar_pregunta_icon,
        compound='left',  # Imagen a la izquierda del texto
        command=editar_pregunta,
        bg=colores['opcion_fondo'][1],  # Rojo vibrante
        fg=colores['boton_texto'],
        font=fuente_boton,
        activebackground='#B22222',  # Rojo más oscuro al presionar
        activeforeground='#FFFFFF',
        bd=0,
        highlightthickness=0,
        cursor='hand2'
    )
    boton_editar_pregunta.image = modificar_pregunta_icon
    boton_editar_pregunta.pack(side=tk.LEFT, padx=5)

    boton_borrar_pregunta = tk.Button(
        botones_preguntas_frame,
        text="Borrar",
        image=borrar_pregunta_icon,
        compound='left',
        command=eliminar_pregunta,
        bg=colores['opcion_fondo'][0],  # Azul profundo
        fg=colores['boton_texto'],
        font=fuente_boton,
        activebackground='#0B4F6C',  # Azul más oscuro al presionar
        activeforeground='#FFFFFF',
        bd=0,
        highlightthickness=0,
        cursor='hand2'
    )
    boton_borrar_pregunta.image = borrar_pregunta_icon
    boton_borrar_pregunta.pack(side=tk.LEFT, padx=5)
    # ========================================================================

    # Botón Salir para cerrar la ventana de mantenimiento
    def cerrar_mantenimiento():
        mantenimiento_window.destroy()

    salir_button = tk.Button(mantenimiento_window, text="Salir", command=cerrar_mantenimiento,
                             bg=colores['boton_cargar_avatar'], fg=colores['boton_texto'], font=fuente_boton,
                             cursor='hand2')
    salir_button.pack(pady=10)

    mantenimiento_window.update()
    centrar_ventana(mantenimiento_window)

# Función para mostrar preguntas y opciones de respuesta
def mostrar_preguntas(categoria_id):
    global puntaje_actual
    try:
        cursor.execute("SELECT * FROM preguntas WHERE categoria_id = ?", (categoria_id,))
        preguntas = cursor.fetchall()
    except sqlite3.Error as e:
        messagebox.showerror("Error de Base de Datos", f"No se pudieron cargar las preguntas: {e}")
        return

    if not preguntas:
        messagebox.showwarning("Sin preguntas", "No hay preguntas disponibles para esta categoría.")
        return

    random.shuffle(preguntas)  # Mezclar las preguntas

    pregunta_index = 0  # Índice de la pregunta actual

    def mostrar_pregunta_actual():
        nonlocal pregunta_index
        if pregunta_index >= len(preguntas):
            messagebox.showinfo("Fin de la Categoría", "Has completado todas las preguntas de esta categoría.")
            return

        pregunta = preguntas[pregunta_index]
        pregunta_window = tk.Toplevel(root)
        pregunta_window.title("Pregunta")
        pregunta_window.configure(bg=colores['fondo_principal'])  # Cambiado a fondo_principal

        def verificar_respuesta(seleccion):
            nonlocal pregunta_window
            if seleccion == pregunta[3]:  # Índice 3 es la respuesta correcta
                messagebox.showinfo("Correcto", "¡Respuesta correcta!")
                actualizar_puntaje(10)
            else:
                messagebox.showerror("Incorrecto", f"Respuesta incorrecta. La respuesta correcta es: {pregunta[3]}")
            pregunta_window.destroy()
            siguiente_pregunta()

        def cerrar_pregunta():
            pregunta_window.destroy()

        tk.Label(pregunta_window, text=pregunta[2], font=fuente_titulo, wraplength=400,
                 bg=colores['fondo_principal'], fg=colores['texto_principal']).pack(pady=10)
        opciones = [pregunta[3], pregunta[4], pregunta[5], pregunta[6]]  # Respuesta correcta y opciones 1-3
        random.shuffle(opciones)

        for i, opcion in enumerate(opciones):
            color_fondo_opcion = colores['opcion_fondo'][i % len(colores['opcion_fondo'])]
            tk.Button(pregunta_window, text=opcion, command=lambda o=opcion: verificar_respuesta(o),
                      font=fuente_boton, bg=color_fondo_opcion, fg=colores['opcion_texto'],
                      activebackground=color_fondo_opcion, activeforeground=colores['opcion_texto'],
                      cursor='hand2').pack(fill="x", pady=5)

        # Botón para salir de la pregunta
        tk.Button(pregunta_window, text="Salir", command=cerrar_pregunta,
                  font=fuente_boton, bg=colores['boton_fondo'], fg=colores['boton_texto'],
                  activebackground=colores['boton_fondo'], activeforeground=colores['boton_texto'],
                  cursor='hand2').pack(pady=10)

        pregunta_window.protocol("WM_DELETE_WINDOW", cerrar_pregunta)

        # Ajustar el tamaño y centrar la ventana
        pregunta_window.update()
        centrar_ventana(pregunta_window)
        pregunta_window.wait_window()

    def siguiente_pregunta():
        nonlocal pregunta_index
        pregunta_index += 1
        mostrar_pregunta_actual()

    def actualizar_puntaje(puntos):
        global puntaje_actual, estrellas_actuales
        puntaje_actual += puntos
        estrellas_nuevas = min(puntaje_actual // 100, 10)
        try:
            cursor.execute("UPDATE jugadores SET puntos = ?, estrellas = ? WHERE id = ?", (puntaje_actual, estrellas_nuevas, jugador_id))
            conn.commit()
            puntaje_label.config(text=f"Puntaje: {puntaje_actual}")
            estrellas_actuales = estrellas_nuevas
            actualizar_estrellas_visual()
        except sqlite3.Error as e:
            messagebox.showerror("Error de Base de Datos", f"No se pudo actualizar el puntaje: {e}")

    mostrar_pregunta_actual()

# Función para iniciar el juego con la selección de categoría
def iniciar_juego():
    if jugador_id is None:
        messagebox.showwarning("Jugador no registrado", "Primero debe registrar o buscar un jugador.")
        return
    # Crear una ventana de selección de categoría
    cat_window = tk.Toplevel(root)
    cat_window.title("Selecciona una Categoría")
    cat_window.configure(bg=colores['fondo_principal'])  # Cambiado a fondo_principal

    tk.Label(cat_window, text="Seleccione una categoría:", font=fuente_titulo,
             bg=colores['fondo_principal'], fg=colores['texto_principal']).pack(pady=10)

    try:
        cursor.execute("SELECT id, nombre, imagen FROM categorias")
        categorias = cursor.fetchall()
        if not categorias:
            messagebox.showwarning("Sin Categorías", "No hay categorías disponibles. Por favor, agregue una categoría primero.")
            cat_window.destroy()
            return

        # Crear un frame para contener las imágenes
        categorias_frame = tk.Frame(cat_window, bg=colores['fondo_principal'])  # Cambiado a fondo_principal
        categorias_frame.pack()

        for i, categoria in enumerate(categorias):
            categoria_id = categoria[0]
            nombre = categoria[1]
            imagen_blob = categoria[2]

            if imagen_blob:
                with open(f"temp_cat_{categoria_id}.png", "wb") as file:
                    file.write(imagen_blob)
                try:
                    imagen = Image.open(f"temp_cat_{categoria_id}.png").resize((100, 100), Image.LANCZOS)
                    imagen_tk = ImageTk.PhotoImage(imagen)
                except Exception as e:
                    messagebox.showerror("Error de Imagen", f"No se pudo procesar la imagen de la categoría '{nombre}': {e}")
                    categorias_frame.destroy()
                    cat_window.destroy()
                    return
                os.remove(f"temp_cat_{categoria_id}.png")
            else:
                # Si no hay imagen, usar un color sólido distinto para cada categoría
                colores_categoria = ['#0B4F6C', '#D62828', '#F77F00', '#FCBF49']  # Azul profundo, Rojo vibrante, Naranja brillante, Amarillo dorado
                imagen_tk = ImageTk.PhotoImage(Image.new('RGB', (100, 100), color=colores_categoria[i % len(colores_categoria)]))

            def abrir_preguntas(categoria_id=categoria_id):
                cat_window.destroy()
                mostrar_preguntas(categoria_id)

            boton_categoria = tk.Button(categorias_frame, image=imagen_tk, command=abrir_preguntas,
                                        bg=colores['fondo_principal'], bd=0, cursor='hand2')  # Cambiado a fondo_principal
            boton_categoria.image = imagen_tk  # Prevenir que la imagen sea recolectada por el garbage collector
            boton_categoria.grid(row=i // 4 * 2, column=i % 4, padx=10, pady=10)

            tk.Label(categorias_frame, text=nombre, bg=colores['fondo_principal'],
                     fg=colores['texto_principal'], font=fuente_texto).grid(row=(i // 4) * 2 + 1, column=i % 4)

        # Ajustar y centrar la ventana
        cat_window.update()
        centrar_ventana(cat_window)

    except sqlite3.Error as e:
        messagebox.showerror("Error de Base de Datos", f"No se pudieron cargar las categorías: {e}")
        cat_window.destroy()

# Función para cerrar la aplicación y limpiar recursos
def cerrar_aplicacion():
    conn.close()
    root.destroy()

# Configuración de la ventana principal de registro
root = tk.Tk()
root.title("RetoTico Junior")
root.configure(bg=colores['fondo_principal'])

# Dejar que la ventana principal se adapte al contenido
root.update()
root.minsize(root.winfo_width(), root.winfo_height())

# Menú de la aplicación
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

opciones_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Opciones", menu=opciones_menu)
opciones_menu.add_command(label="Acerca de", command=lambda: messagebox.showinfo("Acerca de", "RetoTico Junior\nVersión 1.0\nDesarrollado para educación infantil y adolescentes."))
opciones_menu.add_command(label="Descargo de responsabilidad", command=lambda: messagebox.showinfo("Descargo", "Este juego está diseñado solo con fines educativos."))
opciones_menu.add_separator()
opciones_menu.add_command(label="Mantenimiento", command=abrir_mantenimiento)

main_frame = tk.Frame(root, padx=20, pady=20, bg=colores['fondo_principal'])
main_frame.pack(fill="both", expand=True)

# Encabezado principal
header_label = tk.Label(main_frame, text="RetoTico Junior", font=fuente_titulo,
                        bg=colores['fondo_principal'], fg=colores['texto_principal'])
header_label.pack(pady=10)

# Separador de colores
separador = tk.Frame(main_frame, bg=colores['boton_iniciar'], height=5)  # Naranja brillante para el separador
separador.pack(fill='x', pady=10)

nombre_frame = tk.Frame(main_frame, bg=colores['fondo_principal'])
nombre_frame.pack(pady=10)
nombre_label = tk.Label(nombre_frame, text="Nombre del Jugador:", font=fuente_texto,
                        bg=colores['fondo_principal'], fg=colores['texto_principal'])
nombre_label.pack(side=tk.LEFT)
nombre_entry = tk.Entry(nombre_frame, font=fuente_texto, bg=colores['entrada_fondo'], fg=colores['entrada_texto'])
nombre_entry.pack(side=tk.LEFT, padx=5)

# Botón de búsqueda (icono de lupa)
try:
    buscar_icon = ImageTk.PhotoImage(Image.open("buscar.png").resize((20, 20), Image.LANCZOS))
except Exception as e:
    messagebox.showerror("Error de Imagen", f"No se pudo cargar la imagen 'buscar.png': {e}")
    root.destroy()
    exit()

buscar_button = tk.Button(nombre_frame, image=buscar_icon, command=buscar_jugador,
                          bg=colores['boton_fondo'], fg=colores['boton_texto'],
                          activebackground=colores['boton_fondo'], activeforeground=colores['boton_texto'],
                          bd=0, highlightthickness=0, cursor='hand2')
buscar_button.pack(side=tk.LEFT, padx=5)

# Área para mostrar el avatar seleccionado
avatar_frame = tk.Frame(main_frame, bg=colores['fondo_principal'])
avatar_frame.pack(pady=10)
avatar_label = tk.Label(avatar_frame, bg=colores['fondo_principal'])
avatar_label.pack()

# Botones para seleccionar el avatar predeterminado y personalizado
avatar_buttons_frame = tk.Frame(main_frame, bg=colores['fondo_principal'])
avatar_buttons_frame.pack(pady=10)

boton_boyero = tk.Button(avatar_buttons_frame, text="Avatar Boyero",
                         command=lambda: cargar_avatar_predeterminado('boyero.png'),
                         bg=colores['boton_fondo'], fg=colores['boton_texto'], font=fuente_boton,
                         activebackground=colores['boton_fondo'], activeforeground=colores['boton_texto'],
                         bd=0, highlightthickness=0, cursor='hand2')
boton_boyero.pack(side=tk.LEFT, padx=10)

boton_nina = tk.Button(avatar_buttons_frame, text="Avatar Niña",
                       command=lambda: cargar_avatar_predeterminado('nina.png'),
                       bg=colores['boton_avatar_nina'], fg=colores['boton_texto'], font=fuente_boton,
                       activebackground=colores['boton_avatar_nina'], activeforeground=colores['boton_texto'],
                       bd=0, highlightthickness=0, cursor='hand2')
boton_nina.pack(side=tk.LEFT, padx=10)

# ======= Modificación Solicitada: Botón "Cargar Avatar" a Color Azul Claro =======
boton_avatar_personalizado = tk.Button(avatar_buttons_frame, text="Cargar Avatar",
                                       command=cargar_avatar_personalizado,
                                       bg=colores['boton_cargar_avatar'], fg=colores['boton_texto'], font=fuente_boton,
                                       activebackground='#6AA5C7', activeforeground=colores['boton_texto'],
                                       bd=0, highlightthickness=0, cursor='hand2')  # Azul claro
boton_avatar_personalizado.pack(side=tk.LEFT, padx=10)
# ========================================================================

# Botón para registrar al jugador
registrar_button = tk.Button(main_frame, text="Registrar Jugador", command=registrar_jugador,
                             bg=colores['boton_fondo'], fg=colores['boton_texto'], font=fuente_boton,
                             activebackground=colores['boton_fondo'], activeforeground=colores['boton_texto'],
                             cursor='hand2')
registrar_button.pack(pady=10)

# Área para mostrar el puntaje
puntaje_label = tk.Label(main_frame, text="Puntaje: 0", font=("Press Start 2P", 14, "bold"),
                         bg=colores['fondo_principal'], fg=colores['estrellas_color'])  # Amarillo dorado
puntaje_label.pack(pady=5)

# Área para mostrar las estrellas
estrellas_label = tk.Label(main_frame, text="Estrellas: ", font=("Press Start 2P", 14, "bold"),
                           bg=colores['fondo_principal'], fg=colores['estrellas_texto'])  # Amarillo dorado
estrellas_label.pack(pady=5)

# Botón para iniciar el juego
try:
    play_icon = ImageTk.PhotoImage(Image.open("play.png").resize((20, 20), Image.LANCZOS))
except Exception as e:
    messagebox.showerror("Error de Imagen", f"No se pudo cargar la imagen 'play.png': {e}")
    root.destroy()
    exit()

iniciar_button = tk.Button(main_frame, text=" Iniciar Juego", command=iniciar_juego,
                           bg=colores['boton_iniciar'], fg=colores['boton_texto'],
                           font=fuente_boton_grande, image=play_icon, compound="left",
                           activebackground=colores['boton_iniciar'], activeforeground=colores['boton_texto'],
                           cursor='hand2', bd=0, highlightthickness=0)
iniciar_button.pack(pady=20)

# Configurar el cierre de la aplicación
root.protocol("WM_DELETE_WINDOW", cerrar_aplicacion)

# Iniciar el bucle principal de la aplicación
root.mainloop()
