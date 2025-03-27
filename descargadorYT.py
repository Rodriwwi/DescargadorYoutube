import os
import sys
import subprocess
from pytubefix import YouTube
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import traceback
from PIL import Image, ImageTk


class YouTubeDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("Descargador de Youtube")
        self.root.geometry("650x550")
        self.root.resizable(False, False)

        # Configurar estilo
        self.setup_icon("C:\\CODE2\\favicon.ico")
        self.style = ttk.Style()
        self.style.configure('Titulo.TLabel', font=('Helvetica', 18, 'bold'))
        self.style.configure('Subtitulo.TLabel', font=('Helvetica', 10))
        self.style.configure('Progress.Horizontal.TProgressbar', thickness=20)

        # Variables
        self.url_var = tk.StringVar()
        self.format_var = tk.StringVar(value="mp4")
        self.start_time_var = tk.StringVar(value="00:00:00")
        self.end_time_var = tk.StringVar(value="00:00:00")
        self.output_path_var = tk.StringVar(value=os.path.expanduser("~/Downloads"))
        self.filename_var = tk.StringVar(value="")
        self.status_var = tk.StringVar(value="Listo para descargar")
        self.progress_var = tk.DoubleVar(value=0)

        # UI Elements
        self.create_widgets()

    def setup_icon(self, icon_path):
        """Configura el icono para la aplicación con múltiples métodos de respaldo"""
        try:
            # Método 1: Intenta cargar directamente el icono
            self.root.iconbitmap(icon_path)
            return
        except Exception as e:
            print(f"No se pudo cargar el icono directamente: {e}")

        try:
            # Método 2: Para PyInstaller (cuando se ejecuta desde el .exe)
            base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
            temp_icon_path = os.path.join(base_path, os.path.basename(icon_path))

            # Si estamos en modo empaquetado, copiamos el icono a un archivo temporal
            if hasattr(sys, '_MEIPASS'):
                import shutil
                shutil.copyfile(icon_path, temp_icon_path)

            self.root.iconbitmap(temp_icon_path)
        except Exception as e:
            print(f"No se pudo cargar el icono en modo empaquetado: {e}")

            # Método 3: Usar PIL como último recurso (para sistemas problemáticos)
            try:
                img = Image.open(icon_path)
                photo = ImageTk.PhotoImage(img)
                self.root.tk.call('wm', 'iconphoto', self.root._w, photo)
            except Exception as e:
                print(f"No se pudo cargar el icono con PIL: {e}")

    def create_widgets(self):
        # Marco principal para mejor organización
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Título principal
        ttk.Label(
            main_frame,
            text="Descargador de videos de Youtube",
            style='Titulo.TLabel'
        ).pack(pady=(0, 5))

        # Subtítulo
        ttk.Label(
            main_frame,
            text="© Rodriwwi 2025 | Todos los derechos reservados",
            style='Subtitulo.TLabel'
        ).pack(pady=(0, 20))

        # Separador
        ttk.Separator(main_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)

        # Contenido principal
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # URL Entry
        ttk.Label(content_frame, text="URL de YouTube:").pack(pady=(5, 0))
        url_entry = ttk.Entry(content_frame, textvariable=self.url_var, width=70)
        url_entry.pack(pady=(0, 10))

        # Format Selection
        ttk.Label(content_frame, text="Formato:").pack()
        format_frame = ttk.Frame(content_frame)
        format_frame.pack()
        ttk.Radiobutton(format_frame, text="MP4 (Video)", variable=self.format_var, value="mp4").pack(side=tk.LEFT,
                                                                                                      padx=5)
        ttk.Radiobutton(format_frame, text="MP3 (Audio)", variable=self.format_var, value="mp3").pack(side=tk.LEFT,
                                                                                                      padx=5)

        # Trim Options
        ttk.Label(content_frame, text="Recortar Video (opcional):").pack(pady=(10, 0))
        trim_frame = ttk.Frame(content_frame)
        trim_frame.pack()

        ttk.Label(trim_frame, text="Inicio (HH:MM:SS):").pack(side=tk.LEFT)
        start_entry = ttk.Entry(trim_frame, textvariable=self.start_time_var, width=10)
        start_entry.pack(side=tk.LEFT, padx=5)

        ttk.Label(trim_frame, text="Fin (HH:MM:SS):").pack(side=tk.LEFT, padx=(10, 0))
        end_entry = ttk.Entry(trim_frame, textvariable=self.end_time_var, width=10)
        end_entry.pack(side=tk.LEFT, padx=5)

        # Output Path
        ttk.Label(content_frame, text="Carpeta de destino:").pack(pady=(10, 0))
        path_frame = ttk.Frame(content_frame)
        path_frame.pack()

        path_entry = ttk.Entry(path_frame, textvariable=self.output_path_var, width=50)
        path_entry.pack(side=tk.LEFT, padx=(0, 5))

        browse_btn = ttk.Button(path_frame, text="Examinar", command=self.browse_folder)
        browse_btn.pack(side=tk.LEFT)

        # Filename Entry
        ttk.Label(content_frame, text="Nombre del archivo (opcional):").pack(pady=(10, 0))
        filename_entry = ttk.Entry(content_frame, textvariable=self.filename_var, width=70)
        filename_entry.pack(pady=(0, 10))

        # Download Button
        download_btn = ttk.Button(
            content_frame,
            text="Descargar",
            command=self.download,
            style='Accent.TButton'
        )
        download_btn.pack(pady=20)

        # Barra de progreso
        self.progress_bar = ttk.Progressbar(
            main_frame,
            orient=tk.HORIZONTAL,
            length=500,
            mode='determinate',
            variable=self.progress_var,
            style='Progress.Horizontal.TProgressbar'
        )
        self.progress_bar.pack(pady=(10, 5))

        # Status Bar
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=(5, 0))

        ttk.Label(status_frame, text="Estado:").pack(side=tk.LEFT)
        self.status_label = ttk.Label(status_frame, textvariable=self.status_var)
        self.status_label.pack(side=tk.LEFT, padx=5)

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_path_var.set(folder)

    def parse_time(self, time_str):
        try:
            h, m, s = map(int, time_str.split(':'))
            return h * 3600 + m * 60 + s
        except:
            return 0

    def sanitize_filename(self, filename):
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        return filename

    def update_progress(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        progress = (bytes_downloaded / total_size) * 100
        self.progress_var.set(progress)
        self.status_var.set(f"Descargando... {int(progress)}%")
        self.root.update_idletasks()

    def recortar_con_ffmpeg(self, input_path, output_path, start_time, end_time, is_audio=False):
        try:
            self.status_var.set("Recortando...")
            self.progress_var.set(50)
            self.root.update()

            cmd = [
                'ffmpeg',
                '-y',
                '-i', input_path,
                '-ss', str(start_time),
                '-to', str(end_time),
            ]

            if is_audio:
                cmd.extend([
                    '-acodec', 'libmp3lame',
                    '-q:a', '2',
                    output_path
                ])
            else:
                cmd.extend([
                    '-c:v', 'libx264',
                    '-crf', '23',
                    '-preset', 'fast',
                    '-c:a', 'aac',
                    '-movflags', '+faststart',
                    output_path
                ])

            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            self.progress_var.set(100)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error FFmpeg: {e.stderr}")
            return False

    def download(self):
        url = self.url_var.get()
        if not url:
            messagebox.showerror("Error", "Por favor ingresa una URL de YouTube")
            return

        try:
            self.progress_var.set(0)
            self.status_var.set("Conectando a YouTube...")
            self.root.update()

            yt = YouTube(
                url,
                on_progress_callback=self.update_progress,
                on_complete_callback=lambda stream, file_path: None
            )

            output_path = self.output_path_var.get()
            custom_filename = self.filename_var.get().strip()
            safe_title = self.sanitize_filename(custom_filename) if custom_filename else self.sanitize_filename(
                yt.title)
            is_audio = self.format_var.get() == "mp3"

            # Descargar el video completo
            self.status_var.set("Preparando descarga...")
            self.root.update()

            if is_audio:
                stream = yt.streams.filter(only_audio=True).first()
                final_extension = ".mp3"
            else:
                stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
                final_extension = ".mp4"

            temp_file = stream.download(
                output_path=output_path,
                filename_prefix="temp_",
                skip_existing=False
            )

            final_filename = os.path.join(output_path, f"{safe_title}{final_extension}")

            # Procesar recorte si es necesario
            start_time = self.start_time_var.get()
            end_time = self.end_time_var.get()

            if start_time != "00:00:00" or end_time != "00:00:00":
                start_sec = self.parse_time(start_time)
                end_sec = self.parse_time(end_time)

                if end_sec <= start_sec:
                    raise ValueError("El tiempo de fin debe ser mayor que el tiempo de inicio")

                if not self.recortar_con_ffmpeg(temp_file, final_filename, start_sec, end_sec, is_audio):
                    raise RuntimeError("Error al recortar con FFmpeg")

                os.remove(temp_file)
            else:
                os.rename(temp_file, final_filename)

            self.status_var.set(f"Descarga completada: {os.path.basename(final_filename)}")
            messagebox.showinfo("Éxito", "Descarga completada con éxito")

        except Exception as e:
            self.status_var.set("Error")
            error_msg = f"Ocurrió un error: {str(e)}"
            if "FFmpeg" in str(e):
                error_msg += "\n\nAsegúrate de tener FFmpeg instalado y en el PATH"
            messagebox.showerror("Error", error_msg)
            print(traceback.format_exc())
        finally:
            self.root.update()


if __name__ == "__main__":
    root = tk.Tk()

    # Estilo para Windows 10/11
    if 'win' in root.tk.call('tk', 'windowingsystem'):
        from ctypes import windll

        windll.shcore.SetProcessDpiAwareness(1)

    app = YouTubeDownloader(root)
    root.mainloop()