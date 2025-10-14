import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import pickle
import threading
from compression.text_compression import TextCompressor
from compression.image_compression import ImageCompressor
from compression.audio_compression import AudioCompressor
from PIL import Image, ImageTk

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class CompressionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Compresión de Datos")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Centrar la ventana
        self.center_window(800, 600)
        
        self.main_output_dir = "comprimidos"
        os.makedirs(self.main_output_dir, exist_ok=True)
        
        self.text_compressor = TextCompressor(os.path.join(self.main_output_dir, "texto"))
        self.image_compressor = ImageCompressor(os.path.join(self.main_output_dir, "imagenes"))
        self.audio_compressor = AudioCompressor(os.path.join(self.main_output_dir, "audio"))
        
        self.setup_ui()
    
    def center_window(self, width, height):
        """Centrar la ventana en la pantalla"""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def setup_ui(self):
        # Frame principal con gradiente
        main_frame = ctk.CTkFrame(
            self.root, 
            fg_color=("gray95", "gray10"),
            corner_radius=20,
            border_width=2,
            border_color=("#3B8ED0", "#1F6AA5")
        )
        main_frame.pack(fill="both", expand=True, padx=25, pady=25)
        
        # Título principal con icono
        title_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        title_frame.pack(pady=(40, 20))
        
        title_label = ctk.CTkLabel(
            title_frame,
            text="🔄 SISTEMA DE COMPRESIÓN DE DATOS",
            font=ctk.CTkFont(size=26, weight="bold", family="Arial"),
            text_color=("#2B5B84", "#4CC9F0")
        )
        title_label.pack(pady=10)
        
        subtitle_label = ctk.CTkLabel(
            title_frame,
            text="Seleccione el tipo de archivo que desea comprimir",
            font=ctk.CTkFont(size=15, family="Arial"),
            text_color=("gray50", "gray70")
        )
        subtitle_label.pack(pady=(0, 30))
        
        # Frame para botones principales
        buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        buttons_frame.pack(pady=20, padx=80, fill="both", expand=True)
        
        # Botón de compresión de texto
        text_btn = ctk.CTkButton(
            buttons_frame,
            text="📝 COMPRIMIR TEXTO\nAlgoritmo Huffman",
            command=self.open_text_compression,
            height=90,
            font=ctk.CTkFont(size=18, weight="bold", family="Arial"),
            border_width=3,
            border_color=("#3B8ED0", "#1F6AA5"),
            corner_radius=20,
            hover_color=("#2B7BBD", "#144870"),
            fg_color=("#4CAF50", "#2E7D32"),
            text_color="white"
        )
        text_btn.pack(pady=15, fill="x")
        
        # Botón de compresión de imágenes
        image_btn = ctk.CTkButton(
            buttons_frame,
            text="🖼️ COMPRIMIR IMÁGENES\nAlgoritmo RLE",
            command=self.open_image_compression,
            height=90,
            font=ctk.CTkFont(size=18, weight="bold", family="Arial"),
            border_width=3,
            border_color=("#FF9800", "#EF6C00"),
            corner_radius=20,
            hover_color=("#F57C00", "#E65100"),
            fg_color=("#FF5722", "#D84315"),
            text_color="white"
        )
        image_btn.pack(pady=15, fill="x")
        
        # Botón de compresión de audio
        audio_btn = ctk.CTkButton(
            buttons_frame,
            text="🎵 COMPRIMIR AUDIO\nCodificación Diferencial + RLE",
            command=self.open_audio_compression,
            height=90,
            font=ctk.CTkFont(size=18, weight="bold", family="Arial"),
            border_width=3,
            border_color=("#9C27B0", "#7B1FA2"),
            corner_radius=20,
            hover_color=("#8E24AA", "#6A1B9A"),
            fg_color=("#673AB7", "#512DA8"),
            text_color="white"
        )
        audio_btn.pack(pady=15, fill="x")
        
        # Botón para abrir carpeta
        open_folder_btn = ctk.CTkButton(
            main_frame,
            text="📁 ABRIR CARPETA DE COMPRIMIDOS",
            command=self.open_compressed_folder,
            height=55,
            font=ctk.CTkFont(size=16, weight="bold", family="Arial"),
            fg_color=("#607D8B", "#455A64"),
            hover_color=("#546E7A", "#37474F"),
            corner_radius=15,
            border_width=2,
            border_color=("#78909C", "#546E7A")
        )
        open_folder_btn.pack(pady=30)
    
    def open_text_compression(self):
        window = TextCompressionWindow(self.root, self.text_compressor)
        window.window.transient(self.root)
        window.window.grab_set()
    
    def open_image_compression(self):
        window = ImageCompressionWindow(self.root, self.image_compressor)
        window.window.transient(self.root)
        window.window.grab_set()
    
    def open_audio_compression(self):
        window = AudioCompressionWindow(self.root, self.audio_compressor)
        window.window.transient(self.root)
        window.window.grab_set()
    
    def open_compressed_folder(self):
        if os.path.exists(self.main_output_dir):
            os.startfile(self.main_output_dir)
        else:
            messagebox.showinfo("Información", "La carpeta de comprimidos no existe todavía.")

class CompressionWindow:
    def __init__(self, parent, compressor, title, icon, accent_color):
        self.window = ctk.CTkToplevel(parent)
        self.window.title(title)
        self.window.geometry("750x700")
        self.window.resizable(True, True)
        self.is_maximized = False
        
        # Centrar ventana
        self.center_window(750, 700)
        
        self.window.transient(parent)
        self.window.grab_set()
        
        self.compressor = compressor
        self.file_path = None
        self.compressed_path = None
        self.accent_color = accent_color
        
        # Frame principal con scroll
        self.scrollable_frame = ctk.CTkScrollableFrame(
            self.window, 
            fg_color=("gray95", "gray10"),
            corner_radius=15
        )
        self.scrollable_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.setup_ui(title, icon)
    
    def center_window(self, width, height):
        """Centrar la ventana en la pantalla"""
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.window.geometry(f"{width}x{height}+{x}+{y}")
    
    def setup_ui(self, title, icon):
        main_frame = self.scrollable_frame
        
        # Header con gradiente
        header_frame = ctk.CTkFrame(
            main_frame, 
            fg_color="transparent",
            height=80
        )
        header_frame.pack(fill="x", pady=(0, 25))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text=f"{icon}  {title}",
            font=ctk.CTkFont(size=22, weight="bold", family="Arial"),
            text_color=self.accent_color[0]
        )
        title_label.pack(side="left", pady=15, padx=15)
        
        # Botón para maximizar/restaurar ventana
        maximize_btn = ctk.CTkButton(
            header_frame,
            text="⛶",
            command=self.toggle_window_size,
            width=45,
            height=45,
            corner_radius=12,
            fg_color=self.accent_color[0],
            hover_color=self.accent_color[1],
            font=ctk.CTkFont(size=16)
        )
        maximize_btn.pack(side="right", padx=15)
        
        # CUADRITO 1: Selección de Archivo
        file_frame = ctk.CTkFrame(
            main_frame,
            corner_radius=15,
            border_width=2,
            border_color=("gray70", "gray30")
        )
        file_frame.pack(fill="x", pady=12, padx=10)
        
        ctk.CTkLabel(
            file_frame,
            text="📁 SELECCIÓN DE ARCHIVO",
            font=ctk.CTkFont(size=16, weight="bold", family="Arial")
        ).pack(pady=15)
        
        self.load_btn = ctk.CTkButton(
            file_frame,
            text="📂 CARGAR ARCHIVO",
            command=self.load_file,
            width=220,
            height=45,
            corner_radius=12,
            fg_color=self.accent_color[0],
            hover_color=self.accent_color[1],
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.load_btn.pack(pady=12)
        
        self.file_label = ctk.CTkLabel(
            file_frame,
            text="No se ha cargado ningún archivo",
            text_color=("gray50", "gray70"),
            wraplength=600,
            font=ctk.CTkFont(size=13)
        )
        self.file_label.pack(pady=8)
        
        # CUADRITO 2: Compresión
        compress_frame = ctk.CTkFrame(
            main_frame,
            corner_radius=15,
            border_width=2,
            border_color=("gray70", "gray30")
        )
        compress_frame.pack(fill="x", pady=12, padx=10)
        
        ctk.CTkLabel(
            compress_frame,
            text="🗜️ COMPRESIÓN",
            font=ctk.CTkFont(size=16, weight="bold", family="Arial")
        ).pack(pady=15)
        
        self.compress_btn = ctk.CTkButton(
            compress_frame,
            text="COMPRIMIR ARCHIVO",
            command=self.compress_file,
            width=220,
            height=45,
            corner_radius=12,
            fg_color=("#4CAF50", "#2E7D32"),
            hover_color=("#45a049", "#1B5E20"),
            font=ctk.CTkFont(size=14, weight="bold"),
            state="disabled"
        )
        self.compress_btn.pack(pady=12)
        
        # CUADRITO 3: Estadísticas
        stats_frame = ctk.CTkFrame(
            main_frame,
            corner_radius=15,
            border_width=2,
            border_color=("gray70", "gray30")
        )
        stats_frame.pack(fill="x", pady=12, padx=10)
        
        ctk.CTkLabel(
            stats_frame,
            text="📊 ESTADÍSTICAS",
            font=ctk.CTkFont(size=16, weight="bold", family="Arial")
        ).pack(pady=15)
        
        self.size_label = ctk.CTkLabel(
            stats_frame,
            text="Esperando compresión...",
            text_color=("gray50", "gray70"),
            font=ctk.CTkFont(size=13),
            wraplength=600
        )
        self.size_label.pack(pady=8)
        
        self.progress_bar = ctk.CTkProgressBar(
            stats_frame, 
            height=22, 
            corner_radius=10,
            progress_color=self.accent_color[0]
        )
        self.progress_bar.pack(fill="x", pady=15, padx=25)
        self.progress_bar.set(0)
        
        # CUADRITO 4: Descompresión
        decompress_frame = ctk.CTkFrame(
            main_frame,
            corner_radius=15,
            border_width=2,
            border_color=("gray70", "gray30")
        )
        decompress_frame.pack(fill="x", pady=12, padx=10)
        
        ctk.CTkLabel(
            decompress_frame,
            text="📤 DESCOMPRESIÓN",
            font=ctk.CTkFont(size=16, weight="bold", family="Arial")
        ).pack(pady=15)
        
        self.decompress_btn = ctk.CTkButton(
            decompress_frame,
            text="DESCOMPRIMIR ARCHIVO",
            command=self.decompress_file,
            width=220,
            height=45,
            corner_radius=12,
            fg_color=("#FF9800", "#EF6C00"),
            hover_color=("#F57C00", "#E65100"),
            font=ctk.CTkFont(size=14, weight="bold"),
            state="disabled"
        )
        self.decompress_btn.pack(pady=8)
        
        open_folder_btn = ctk.CTkButton(
            decompress_frame,
            text="📁 ABRIR CARPETA DE SALIDA",
            command=self.open_output_folder,
            width=220,
            height=40,
            corner_radius=10,
            fg_color=("#607D8B", "#455A64"),
            hover_color=("#546E7A", "#37474F"),
            font=ctk.CTkFont(size=13, weight="bold")
        )
        open_folder_btn.pack(pady=8)
        
        # Forzar actualización de la UI
        self.window.update_idletasks()
    
    def toggle_window_size(self):
        if not self.is_maximized:
            self.window.state('zoomed')
            self.is_maximized = True
        else:
            self.window.state('normal')
            self.window.geometry("750x700")
            self.center_window(750, 700)
            self.is_maximized = False
    
    def load_file(self):
        """Método base para cargar archivos, será sobrescrito por las subclases"""
        file_types = [("Todos los archivos", "*.*")]
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo",
            filetypes=file_types
        )
        if file_path:
            self.file_path = file_path
            file_size = self.get_file_size(file_path)
            self.file_label.configure(
                text=f"📄 Archivo: {os.path.basename(file_path)}\n"
                     f"📦 Tamaño: {self.format_size(file_size)}"
            )
            self.compress_btn.configure(state="normal")
            self.decompress_btn.configure(state="disabled")
    
    def compress_file(self):
        pass
    
    def decompress_file(self):
        pass
    
    def open_output_folder(self):
        output_dir = getattr(self.compressor, 'output_dir', 'comprimidos')
        if os.path.exists(output_dir):
            os.startfile(output_dir)
        else:
            messagebox.showinfo("Información", "La carpeta no existe todavía.")
    
    def get_file_size(self, file_path):
        try:
            return os.path.getsize(file_path)
        except:
            return 0
    
    def format_size(self, size_bytes):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} TB"
    
    def update_progress(self, value):
        self.progress_bar.set(value)
        self.window.update_idletasks()

class TextCompressionWindow(CompressionWindow):
    def __init__(self, parent, compressor):
        super().__init__(parent, compressor, "Compresión de Texto", "📝", ("#4CAF50", "#2E7D32"))
        self.is_compressed_file = False
        self.original_content = ""
        self.compressed_content = ""
        self.create_content_display()
    
    def create_content_display(self):
        main_frame = self.scrollable_frame
        
        # CUADRITO 5: Vista Previa del Contenido
        content_frame = ctk.CTkFrame(
            main_frame,
            corner_radius=15,
            border_width=2,
            border_color=("gray70", "gray30")
        )
        content_frame.pack(fill="both", expand=True, pady=12, padx=10)
        
        ctk.CTkLabel(
            content_frame,
            text="👁️ VISTA PREVIA DEL CONTENIDO",
            font=ctk.CTkFont(size=16, weight="bold", family="Arial")
        ).pack(pady=15)
        
        # Frame para los textboxes
        textboxes_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        textboxes_frame.pack(fill="both", expand=True, pady=15, padx=15)
        
        # Textbox para contenido original
        original_frame = ctk.CTkFrame(textboxes_frame, fg_color="transparent")
        original_frame.grid(row=0, column=0, padx=8, pady=8, sticky="nsew")
        
        ctk.CTkLabel(
            original_frame, 
            text="📄 TEXTO ORIGINAL:",
            font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w", pady=(0, 5))
        
        self.original_textbox = ctk.CTkTextbox(
            original_frame, 
            height=150, 
            wrap="word",
            corner_radius=10,
            border_width=2,
            border_color=("gray70", "gray30")
        )
        self.original_textbox.pack(fill="both", expand=True)
        self.original_textbox.configure(state="disabled")
        
        # Textbox para contenido comprimido
        compressed_frame = ctk.CTkFrame(textboxes_frame, fg_color="transparent")
        compressed_frame.grid(row=0, column=1, padx=8, pady=8, sticky="nsew")
        
        ctk.CTkLabel(
            compressed_frame, 
            text="🔐 TEXTO COMPRIMIDO:",
            font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w", pady=(0, 5))
        
        self.compressed_textbox = ctk.CTkTextbox(
            compressed_frame, 
            height=150, 
            wrap="word",
            corner_radius=10,
            border_width=2,
            border_color=("gray70", "gray30")
        )
        self.compressed_textbox.pack(fill="both", expand=True)
        self.compressed_textbox.configure(state="disabled")
        
        # Configurar grid weights
        textboxes_frame.grid_columnconfigure(0, weight=1)
        textboxes_frame.grid_columnconfigure(1, weight=1)
        textboxes_frame.grid_rowconfigure(0, weight=1)
    
    def load_file(self):
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo de texto",
            filetypes=[
                ("Archivos de texto", "*.txt"),
                ("Archivos comprimidos", "*.textcomp"),
                ("Todos los archivos", "*.*")
            ]
        )
        if file_path:
            self.file_path = file_path
            file_size = self.get_file_size(file_path)
            
            # Verificar si es un archivo comprimido
            self.is_compressed_file = file_path.endswith('.textcomp')
            
            if self.is_compressed_file:
                self.file_label.configure(
                    text=f"🗜️ Archivo comprimido: {os.path.basename(file_path)}\n"
                         f"📦 Tamaño: {self.format_size(file_size)}"
                )
                self.compress_btn.configure(state="disabled")
                self.decompress_btn.configure(state="normal")
                self.original_textbox.configure(state="normal")
                self.original_textbox.delete("1.0", "end")
                self.original_textbox.configure(state="disabled")
            else:
                self.file_label.configure(
                    text=f"📝 Archivo: {os.path.basename(file_path)}\n"
                         f"📦 Tamaño: {self.format_size(file_size)}"
                )
                self.compress_btn.configure(state="normal")
                self.decompress_btn.configure(state="disabled")
                
                # Mostrar contenido del archivo de texto en el textbox
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        self.original_content = file.read()
                        self.original_textbox.configure(state="normal")
                        self.original_textbox.delete("1.0", "end")
                        self.original_textbox.insert("1.0", self.original_content)
                        self.original_textbox.configure(state="disabled")
                except Exception as e:
                    messagebox.showerror("Error", f"❌ Error al leer el archivo: {str(e)}")
    
    def compress_file(self):
        if not self.file_path or self.is_compressed_file:
            return
        try:
            self.update_progress(0.2)
            compressed_file = self.compressor.compress(self.file_path)
            self.compressed_path = compressed_file
            self.update_progress(0.7)
            original_size = self.get_file_size(self.file_path)
            compressed_size = self.get_file_size(compressed_file)
            self.update_progress(0.9)
            compression_ratio = max(0, (1 - compressed_size / original_size) * 100) if original_size > 0 else 0
            self.size_label.configure(
                text=f"📊 Original: {self.format_size(original_size)}\n"
                     f"🗜️ Comprimido: {self.format_size(compressed_size)}\n"
                     f"📈 Ratio de compresión: {compression_ratio:.1f}%"
            )
            # Mostrar contenido comprimido en el textbox (representación legible)
            try:
                with open(compressed_file, 'rb') as file:
                    self.compressed_content = str(file.read())  # Convertir a string para mostrar
                    self.compressed_textbox.configure(state="normal")
                    self.compressed_textbox.delete("1.0", "end")
                    self.compressed_textbox.insert("1.0", self.compressed_content)
                    self.compressed_textbox.configure(state="disabled")
            except Exception as e:
                print(f"Error al mostrar contenido comprimido: {str(e)}")
            self.update_progress(1.0)
            self.decompress_btn.configure(state="normal")
            messagebox.showinfo("Éxito", "✅ Texto comprimido correctamente")
        except Exception as e:
            self.update_progress(0)
            messagebox.showerror("Error", f"❌ Error al comprimir: {str(e)}")
    
    def decompress_file(self):
        if not self.file_path:
            return
        try:
            self.update_progress(0.2)
            import time
            time.sleep(0.5)
            if self.is_compressed_file:
                decompressed_file = self.compressor.decompress(self.file_path)
            else:
                decompressed_file = self.compressor.decompress(self.compressed_path)
            self.update_progress(0.7)
            time.sleep(0.3)
            if self.is_compressed_file:
                compressed_size = self.get_file_size(self.file_path)
            else:
                compressed_size = self.get_file_size(self.compressed_path)
            decompressed_size = self.get_file_size(decompressed_file)
            self.update_progress(1.0)
            decompressed_filename = os.path.basename(decompressed_file)
            messagebox.showinfo("Éxito",
                               f"✅ Texto descomprimido correctamente\n\n"
                               f"🗜️ Tamaño comprimido: {self.format_size(compressed_size)}\n"
                               f"📝 Tamaño descomprimido: {self.format_size(decompressed_size)}\n"
                               f"📁 Archivo: {decompressed_filename}")
            # Mostrar contenido descomprimido
            try:
                with open(decompressed_file, 'r', encoding='utf-8') as file:
                    self.original_content = file.read()
                    self.original_textbox.configure(state="normal")
                    self.original_textbox.delete("1.0", "end")
                    self.original_textbox.insert("1.0", self.original_content)
                    self.original_textbox.configure(state="disabled")
            except Exception as e:
                print(f"Error al mostrar contenido descomprimido: {str(e)}")
        except Exception as e:
            self.update_progress(0)
            messagebox.showerror("Error", f"❌ Error al descomprimir: {str(e)}")

class ImageCompressionWindow(CompressionWindow):
    def __init__(self, parent, compressor):
        super().__init__(parent, compressor, "Compresión de Imágenes", "🖼️", ("#FF5722", "#D84315"))
        self.is_compressed_file = False
        self.original_image = None
        self.compressed_image = None
        self.original_photo = None
        self.compressed_photo = None
        self.create_image_display()
    
    def create_image_display(self):
        main_frame = self.scrollable_frame
        
        # CUADRITO 5: Vista Previa de Imágenes
        image_frame = ctk.CTkFrame(
            main_frame,
            corner_radius=15,
            border_width=2,
            border_color=("gray70", "gray30")
        )
        image_frame.pack(fill="both", expand=True, pady=12, padx=10)
        
        ctk.CTkLabel(
            image_frame,
            text="🖼️ VISTA PREVIA DE IMÁGENES",
            font=ctk.CTkFont(size=16, weight="bold", family="Arial")
        ).pack(pady=15)
        
        # Frame para las imágenes
        images_display_frame = ctk.CTkFrame(image_frame, fg_color="transparent")
        images_display_frame.pack(fill="both", expand=True, pady=15, padx=15)
        
        # Label para imagen original
        original_img_frame = ctk.CTkFrame(images_display_frame, fg_color="transparent")
        original_img_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        ctk.CTkLabel(
            original_img_frame, 
            text="🖼️ IMAGEN ORIGINAL:",
            font=ctk.CTkFont(weight="bold")
        ).pack(pady=(0, 8))
        
        self.original_image_label = ctk.CTkLabel(
            original_img_frame, 
            text="No hay imagen cargada", 
            width=250, 
            height=180,
            fg_color=("gray85", "gray25"),
            corner_radius=12,
            font=ctk.CTkFont(size=12)
        )
        self.original_image_label.pack(pady=5)
        
        # Label para imagen comprimida
        compressed_img_frame = ctk.CTkFrame(images_display_frame, fg_color="transparent")
        compressed_img_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        ctk.CTkLabel(
            compressed_img_frame, 
            text="🗜️ IMAGEN COMPRIMIDA:",
            font=ctk.CTkFont(weight="bold")
        ).pack(pady=(0, 8))
        
        self.compressed_image_label = ctk.CTkLabel(
            compressed_img_frame, 
            text="La imagen comprimida\naparecerá aquí", 
            width=250, 
            height=180,
            fg_color=("gray85", "gray25"),
            corner_radius=12,
            font=ctk.CTkFont(size=12)
        )
        self.compressed_image_label.pack(pady=5)
        
        # Configurar grid weights
        images_display_frame.grid_columnconfigure(0, weight=1)
        images_display_frame.grid_columnconfigure(1, weight=1)
    
    def load_file(self):
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo de imagen",
            filetypes=[
                ("Archivos de imagen", "*.png *.jpg *.jpeg *.bmp"),
                ("Archivos comprimidos", "*.imgcomp"),
                ("Todos los archivos", "*.*")
            ]
        )
        if file_path:
            self.file_path = file_path
            file_size = self.get_file_size(file_path)
            
            # Verificar si es un archivo comprimido
            self.is_compressed_file = file_path.endswith('.imgcomp')
            
            if self.is_compressed_file:
                self.file_label.configure(
                    text=f"🗜️ Archivo comprimido: {os.path.basename(file_path)}\n"
                         f"📦 Tamaño: {self.format_size(file_size)}"
                )
                self.compress_btn.configure(state="disabled")
                self.decompress_btn.configure(state="normal")
                self.original_image_label.configure(text="No hay imagen cargada", image=None)
            else:
                self.file_label.configure(
                    text=f"🖼️ Archivo: {os.path.basename(file_path)}\n"
                         f"📦 Tamaño: {self.format_size(file_size)}"
                )
                self.compress_btn.configure(state="normal")
                self.decompress_btn.configure(state="disabled")
                
                # Mostrar imagen original
                try:
                    self.original_image = Image.open(file_path)
                    # Redimensionar imagen para la vista previa
                    self.original_image.thumbnail((250, 180))
                    self.original_photo = ImageTk.PhotoImage(self.original_image)
                    self.original_image_label.configure(image=self.original_photo, text="")
                except Exception as e:
                    messagebox.showerror("Error", f"❌ Error al cargar la imagen: {str(e)}")
                    self.original_image_label.configure(text="No hay imagen cargada", image=None)
    
    def compress_file(self):
        if not self.file_path or self.is_compressed_file:
            return
        try:
            self.update_progress(0.2)
            compressed_file = self.compressor.compress(self.file_path)
            self.compressed_path = compressed_file
            self.update_progress(0.7)
            original_size = self.get_file_size(self.file_path)
            compressed_size = self.get_file_size(compressed_file)
            self.update_progress(0.9)
            compression_ratio = max(0, (1 - compressed_size / original_size) * 100) if original_size > 0 else 0
            self.size_label.configure(
                text=f"📊 Original: {self.format_size(original_size)}\n"
                     f"🗜️ Comprimido: {self.format_size(compressed_size)}\n"
                     f"📈 Ratio de compresión: {compression_ratio:.1f}%"
            )
            # Mostrar imagen comprimida
            try:
                self.compressed_image = Image.open(compressed_file)
                self.compressed_image.thumbnail((250, 180))
                self.compressed_photo = ImageTk.PhotoImage(self.compressed_image)
                self.compressed_image_label.configure(image=self.compressed_photo, text="")
            except Exception as e:
                print(f"Error al mostrar imagen comprimida: {str(e)}")
                self.compressed_image_label.configure(text="No hay imagen comprimida", image=None)
            self.update_progress(1.0)
            self.decompress_btn.configure(state="normal")
            messagebox.showinfo("Éxito", "✅ Imagen comprimida correctamente")
        except Exception as e:
            self.update_progress(0)
            messagebox.showerror("Error", f"❌ Error al comprimir: {str(e)}")
    
    def decompress_file(self):
        if not self.file_path:
            return
        try:
            self.update_progress(0.2)
            import time
            time.sleep(0.5)
            if self.is_compressed_file:
                decompressed_file = self.compressor.decompress(self.file_path)
            else:
                decompressed_file = self.compressor.decompress(self.compressed_path)
            self.update_progress(0.7)
            time.sleep(0.3)
            if self.is_compressed_file:
                compressed_size = self.get_file_size(self.file_path)
            else:
                compressed_size = self.get_file_size(self.compressed_path)
            decompressed_size = self.get_file_size(decompressed_file)
            self.update_progress(1.0)
            decompressed_filename = os.path.basename(decompressed_file)
            messagebox.showinfo("Éxito",
                               f"✅ Imagen descomprimida correctamente\n\n"
                               f"🗜️ Tamaño comprimido: {self.format_size(compressed_size)}\n"
                               f"🖼️ Tamaño descomprimido: {self.format_size(decompressed_size)}\n"
                               f"📁 Archivo: {decompressed_filename}")
            # Mostrar imagen descomprimida
            try:
                self.original_image = Image.open(decompressed_file)
                self.original_image.thumbnail((250, 180))
                self.original_photo = ImageTk.PhotoImage(self.original_image)
                self.original_image_label.configure(image=self.original_photo, text="")
            except Exception as e:
                print(f"Error al mostrar imagen descomprimida: {str(e)}")
                self.original_image_label.configure(text="No hay imagen cargada", image=None)
        except Exception as e:
            self.update_progress(0)
            messagebox.showerror("Error", f"❌ Error al descomprimir: {str(e)}")

class AudioCompressionWindow(CompressionWindow):
    def __init__(self, parent, compressor):
        super().__init__(parent, compressor, "Compresión de Audio", "🎵", ("#673AB7", "#512DA8"))
        self.is_compressed_file = False
        self.play_btn = None
        self.is_playing = False
        self.create_play_button()
    
    def create_play_button(self):
        main_frame = self.scrollable_frame
        for widget in main_frame.winfo_children():
            if isinstance(widget, ctk.CTkFrame) and "DESCOMPRESIÓN" in str(widget.winfo_children()[0].cget("text")):
                self.play_btn = ctk.CTkButton(
                    widget,
                    text="▶️ REPRODUCIR AUDIO ORIGINAL",
                    command=self.play_audio,
                    width=220,
                    height=45,
                    corner_radius=12,
                    state="disabled",
                    fg_color=("#2196F3", "#1976D2"),
                    hover_color=("#1E88E5", "#1565C0"),
                    font=ctk.CTkFont(size=13, weight="bold")
                )
                self.play_btn.pack(pady=8)
                break
    
    def play_audio_in_thread(self, audio_file):
        """Reproducir audio en un hilo separado para no bloquear la interfaz"""
        def play():
            try:
                self.compressor.play_audio(audio_file)
                self.is_playing = False
                # Actualizar estado de los botones en el hilo principal
                self.window.after(0, self.update_play_button)
            except Exception as e:
                self.is_playing = False
                # Actualizar estado de los botones en el hilo principal
                self.window.after(0, self.update_play_button)
                print(f"Error al reproducir el audio: {e}")
        
        if not self.is_playing:
            self.is_playing = True
            self.update_play_button()
            thread = threading.Thread(target=play, daemon=True)
            thread.start()
    
    def update_play_button(self):
        """Actualizar estado del botón de reproducción"""
        if self.is_playing:
            self.play_btn.configure(state="disabled", text="⏸️ REPRODUCIENDO...")
        else:
            if self.file_path and not self.is_compressed_file:
                self.play_btn.configure(state="normal", text="▶️ REPRODUCIR AUDIO ORIGINAL")
            else:
                self.play_btn.configure(state="disabled", text="▶️ REPRODUCIR AUDIO ORIGINAL")
    
    def load_file(self):
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo de audio",
            filetypes=[
                ("Archivos WAV", "*.wav"),
                ("Archivos MP3", "*.mp3"),
                ("Archivos comprimidos", "*.audiocomp"),
                ("Todos los archivos", "*.*")
            ]
        )
        if file_path:
            self.file_path = file_path
            file_size = self.get_file_size(file_path)
            
            # Verificar si es un archivo comprimido
            self.is_compressed_file = file_path.endswith('.audiocomp')
            
            if self.is_compressed_file:
                self.file_label.configure(
                    text=f"🗜️ Archivo comprimido: {os.path.basename(file_path)}\n"
                         f"📦 Tamaño: {self.format_size(file_size)}"
                )
                self.compress_btn.configure(state="disabled")
                self.decompress_btn.configure(state="normal")
                self.play_btn.configure(state="disabled")
            else:
                self.file_label.configure(
                    text=f"🎵 Archivo: {os.path.basename(file_path)}\n"
                         f"📦 Tamaño: {self.format_size(file_size)}"
                )
                self.compress_btn.configure(state="normal")
                self.decompress_btn.configure(state="disabled")
                self.play_btn.configure(state="normal")
            
            self.update_play_button()
    
    def compress_file(self):
        if not self.file_path or self.is_compressed_file:
            return
        try:
            self.update_progress(0.2)
            compressed_file = self.compressor.compress(self.file_path)
            self.compressed_path = compressed_file
            self.update_progress(0.7)
            original_size = self.get_file_size(self.file_path)
            compressed_size = self.get_file_size(compressed_file)
            self.update_progress(0.9)
            compression_ratio = max(0, (1 - compressed_size / original_size) * 100) if original_size > 0 else 0
            self.size_label.configure(
                text=f"📊 Original: {self.format_size(original_size)}\n"
                     f"🗜️ Comprimido: {self.format_size(compressed_size)}\n"
                     f"📈 Ratio de compresión: {compression_ratio:.1f}%"
            )
            self.update_progress(1.0)
            self.decompress_btn.configure(state="normal")
            self.update_play_button()
            messagebox.showinfo("Éxito", "✅ Audio comprimido correctamente")
        except Exception as e:
            self.update_progress(0)
            messagebox.showerror("Error", f"❌ Error al comprimir: {str(e)}")
    
    def decompress_file(self):
        if not self.file_path:
            return
        try:
            self.update_progress(0.2)
            
            # Añadir retraso para evitar conflictos de archivos
            import time
            time.sleep(0.5)
            
            if self.is_compressed_file:
                # Descomprimir archivo cargado directamente
                decompressed_file = self.compressor.decompress(self.file_path)
            else:
                # Descomprimir archivo comprimido en esta sesión
                decompressed_file = self.compressor.decompress(self.compressed_path)
            
            self.update_progress(0.7)
            
            # Añadir otro retraso
            time.sleep(0.3)
            
            if self.is_compressed_file:
                compressed_size = self.get_file_size(self.file_path)
            else:
                compressed_size = self.get_file_size(self.compressed_path)
            
            decompressed_size = self.get_file_size(decompressed_file)
            self.update_progress(1.0)
            
            # Mostrar información más detallada
            decompressed_filename = os.path.basename(decompressed_file)
            messagebox.showinfo("Éxito", 
                               f"✅ Audio descomprimido correctamente\n\n"
                               f"🗜️ Tamaño comprimido: {self.format_size(compressed_size)}\n"
                               f"🎵 Tamaño descomprimido: {self.format_size(decompressed_size)}\n"
                               f"📁 Archivo: {decompressed_filename}")
            
            # Actualizar estado del botón de reproducción
            self.update_play_button()
            
        except Exception as e:
            self.update_progress(0)
            messagebox.showerror("Error", f"❌ Error al descomprimir: {str(e)}")
    
    def play_audio(self):
        if not self.file_path or self.is_playing:
            return
        try:
            if self.is_compressed_file:
                # Para archivos comprimidos, buscar el archivo descomprimido
                compressed_filename = os.path.splitext(os.path.basename(self.file_path))[0]
                output_dir = self.compressor.output_dir
                
                decompressed_files = []
                for file in os.listdir(output_dir):
                    if compressed_filename.replace('_compressed', '') in file and (
                        file.endswith('.wav') or file.endswith('.mp3')) and 'decompressed' in file:
                        decompressed_files.append(file)
                
                if decompressed_files:
                    decompressed_files.sort(reverse=True)
                    most_recent_file = decompressed_files[0]
                    audio_file = os.path.join(output_dir, most_recent_file)
                    self.play_audio_in_thread(audio_file)
                else:
                    messagebox.showinfo("Información", 
                                      "El archivo comprimido necesita ser descomprimido primero.")
            else:
                # Para archivos originales, reproducir directamente
                self.play_audio_in_thread(self.file_path)
        except Exception as e:
            messagebox.showerror("Error", f"❌ Error al reproducir audio: {str(e)}")

if __name__ == "__main__":
    root = ctk.CTk()
    app = CompressionApp(root)
    root.mainloop()