# Descargador de YouTube

Esta aplicación permite descargar y recortar cualquier vídeo de YouTube en formatos `.mp3` o `.mp4`.

## Características

- Descarga vídeos de YouTube.
- Conversión a formatos `.mp3` y `.mp4`.
- Posibilidad de recortar el vídeo descargado.

## Requisitos

- Python 3.x instalado en el sistema.
- Las siguientes bibliotecas de Python:
  - `pytube`
  - `moviepy`

## Instalación

1. Clona el repositorio:

   ```bash
   git clone https://github.com/Rodriwwi/DescargadorYoutube.git
   ```

2. Abre el directorio del proyecto:

   ```bash
   cd DescargadorYoutube
   ```

3. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

## Uso

1. Ejecuta el script principal:

   ```bash
   python descargadorYT.py
   ```

2. Sigue las instrucciones en pantalla para ingresar la URL del vídeo de YouTube que quieres descargar.

3. Selecciona el formato de salida (`.mp3` o `.mp4`).

4. Si quieres recortar el vídeo, especifica los tiempos de inicio y fin cuando se te solicite.

## Notas

- Es necesario tener conexión a internet para poder usar la herramienta.

