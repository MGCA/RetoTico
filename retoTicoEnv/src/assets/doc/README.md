# RetoTico

**Descripción**: Breve descripción de lo que hace tu proyecto.

Reto Tico es una aplicación educativa e interactiva diseñada para promover el conocimiento sobre la biodiversidad y cultura de Costa Rica. 
Dirigida especialmente a jóvenes y estudiantes, esta herramienta utiliza actividades lúdicas y retos para hacer el aprendizaje divertido y accesible. 
A través de una plataforma amigable y envolvente, los usuarios exploran la flora, fauna, y áreas protegidas del país, 
incentivando la conciencia ambiental. Con una interfaz atractiva, un sistema de logros, y contenido musical, Reto Tico 
busca transformar la educación ambiental en una experiencia dinámica que inspire respeto y protección hacia la riqueza natural de Costa Rica.

## Instalación
Para abrir el archivo .exe de la aplicación Reto Tico y evitar problemas con posibles detecciones de antivirus, sigue estos pasos:

1. Ubica el archivo .exe
Navega hasta la carpeta donde has guardado el archivo .exe de Reto Tico.

********ACTUALIZACIONES***********************
Si ya has usado el juego y descargo una nueva version del juego dirigirse al disco "C:" buscar la carpeta "users" o usuarios, y buscar el archivo "retotico.bd" 
y borrarla, esto borrara todos los usuarios, preguntas, respuestas, imagenes e historial de juegos.

2. Ejecuta el archivo como administrador
Haz clic derecho sobre el archivo .exe.
Selecciona "Ejecutar como administrador" para darle los permisos necesarios al programa.

3. Configura el antivirus si es necesario
Algunos antivirus pueden detectar el archivo .exe como una posible amenaza debido a las políticas de seguridad, especialmente si el archivo no está firmado digitalmente.
Añade el archivo a la lista de excepciones o exclusiones del antivirus. Esto le indica al software de seguridad que el archivo es seguro y puede ejecutarse sin restricciones.
Pasos para añadir una exclusión:
Abre la configuración de tu antivirus.
Busca una sección llamada "Exclusiones" o "Excepciones" (esto puede variar dependiendo del antivirus).
Añade la ruta o el archivo .exe de Reto Tico a esta lista.

4. Ejecuta el programa
Intenta abrir de nuevo el archivo .exe y verifica que el antivirus no lo bloquee.
Recomendación adicional:
Si el archivo sigue siendo detectado como una posible amenaza, verifica que el archivo provenga de una fuente confiable y asegúrate de que no haya sido modificado o dañado.

## Mejora u obtencion del codigo fuente
1. Clona este repositorio:
   ```bash
   git clone https://github.com/MGCA/retoTico.git
Instala las dependencias necesarias:
bash
Copiar código
pip install -r requirements.txt
Uso
Para ejecutar la aplicación, simplemente corre el siguiente comando:

bash
Copiar código
python retoTico.py
Estructura del proyecto
bash
Copiar código
RETOTICO/
├── retoTicoEnv/ 
   ├── src/ 
      ├── assets/            # carpetas como imágenes, iconos, csv, etc.
      ├── configuracion/     # archivos de insert, create db
      ├── Datos/            # Código de manejo de select,insert,delete a bd.
      ├── Logica/            # Código de la lógica del proyecto
      ├── SistemaRetoTico/   # Funciones y clases principales
      ├── icono.ico          # icono del .exe
      ├── main.py            # Script principal
      └── requirements.txt   # Dependencias del proyecto
Contribuciones
Si deseas contribuir, por favor sigue estos pasos:

Haz un fork de este repositorio.
Crea una rama con tu nueva característica (git checkout -b feature/nueva-caracteristica).
Haz commit de tus cambios (git commit -am 'Agrega nueva característica').
Empuja tus cambios a tu repositorio (git push origin feature/nueva-caracteristica).
Crea un pull request.

## Licencia
Este proyecto está bajo la [Licencia MIT](./LICENSE) - consulta el archivo LICENSE para más detalles.
