import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
from compression.text_compression import TextCompressor
from compression.image_compression import ImageCompressor
from compression.audio_compression import AudioCompressor

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class CompressionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Compresión de Datos")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        self.main_output_dir = "comprimidos"
        os.makedirs(self.main_output_dir, exist_ok=True)
        
        self.text_compressor = TextCompressor(os.path.join(self.main_output_dir, "texto"))
        self.image_compressor = ImageCompressor(os.path.join(self.main_output_dir, "imagenes"))
        self.audio_compressor = AudioCompressor(os.path.join(self.main_output_dir, "audio"))
        
        self.setup_ui()
    
    def setup_ui(self):
        main_frame = ctk.CTkFrame(self.root, fg_color=("gray90", "gray13"))
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            main_frame,
            text="🔄 SISTEMA DE COMPRESIÓN DE DATOS",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=("#2B5B84", "#4CC9F0")
        )
        title_label.pack(pady=(40, 20))
        
        subtitle_label = ctk.CTkLabel(
            main_frame,
            text="Seleccione el tipo de archivo que desea comprimir",
            font=ctk.CTkFont(size=14),
            text_color=("gray40", "gray60")
        )
        subtitle_label.pack(pady=(0, 40))
        
        buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        buttons_frame.pack(pady=20, padx=100, fill="both", expand=True)
        
        text_btn = ctk.CTkButton(
            buttons_frame,
            text="📝 Comprimir Texto\n(Algoritmo Huffman)",
            command=self.open_text_compression,
            height=80,
            font=ctk.CTkFont(size=16, weight="bold"),
            border_width=2,
            border_color=("#3B8ED0", "#1F6AA5"),
            corner_radius=15,
            hover_color=("#2B7BBD", "#144870")
        )
        text_btn.pack(pady=15, fill="x")
        
        image_btn = ctk.CTkButton(
            buttons_frame,
            text="🖼️ Comprimir Imágenes\n(Algoritmo RLE)",
            command=self.open_image_compression,
            height=80,
            font=ctk.CTkFont(size=16, weight="bold"),
            border_width=2,
            border_color=("#2E8B57", "#1F5E3B"),
            corner_radius=15,
            hover_color=("#267A49", "#164A2A")
        )
        image_btn.pack(pady=15, fill="x")
        
        audio_btn = ctk.CTkButton(
            buttons_frame,
            text="🎵 Comprimir Audio\n(Codificación Diferencial + RLE)",
            command=self.open_audio_compression,
            height=80,
            font=ctk.CTkFont(size=16, weight="bold"),
            border_width=2,
            border_color=("#8B4513", "#5D2F0F"),
            corner_radius=15,
            hover_color=("#7A3C10", "#4A2509")
        )
        audio_btn.pack(pady=15, fill="x")
        
        open_folder_btn = ctk.CTkButton(
            main_frame,
            text="📁 Abrir Carpeta de Comprimidos",
            command=self.open_compressed_folder,
            height=50,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=("#8B4513", "#5D2F0F"),
            hover_color=("#7A3C10", "#4A2509")
        )
        open_folder_btn.pack(pady=20)
    
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
    def __init__(self, parent, compressor, title, icon):
        self.window = ctk.CTkToplevel(parent)
        self.window.title(title)
        self.window.geometry("700x650")
        self.window.resizable(True, True)
        
        self.window.transient(parent)
        self.window.grab_set()
        
        self.compressor = compressor
        self.file_path = None
        self.compressed_path = None
        self.setup_ui(title, icon)
    
    def setup_ui(self, title, icon):
        main_frame = ctk.CTkFrame(self.window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text=f"{icon} {title}",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=10)
        
        file_frame = ctk.CTkFrame(main_frame)
        file_frame.pack(fill="x", pady=10, padx=10)
        
        ctk.CTkLabel(
            file_frame,
            text="Selección de Archivo",
            font=ctk.CTkFont(weight="bold")
        ).pack(pady=10)
        
        self.load_btn = ctk.CTkButton(
            file_frame,
            text="📂 Cargar Archivo",
            command=self.load_file,
            width=200,
            height=40,
            corner_radius=10
        )
        self.load_btn.pack(pady=10)
        
        self.file_label = ctk.CTkLabel(
            file_frame,
            text="No se ha cargado ningún archivo",
            text_color=("gray50", "gray70"),
            wraplength=500
        )
        self.file_label.pack(pady=5)
        
        compress_frame = ctk.CTkFrame(main_frame)
        compress_frame.pack(fill="x", pady=10, padx=10)
        
        ctk.CTkLabel(
            compress_frame,
            text="Compresión",
            font=ctk.CTkFont(weight="bold")
        ).pack(pady=10)
        
        self.compress_btn = ctk.CTkButton(
            compress_frame,
            text="🗜️ Comprimir Archivo",
            command=self.compress_file,
            width=200,
            height=40,
            corner_radius=10,
            state="disabled"
        )
        self.compress_btn.pack(pady=10)
        
        stats_frame = ctk.CTkFrame(main_frame)
        stats_frame.pack(fill="x", pady=10, padx=10)
        
        ctk.CTkLabel(
            stats_frame,
            text="Estadísticas",
            font=ctk.CTkFont(weight="bold")
        ).pack(pady=10)
        
        self.size_label = ctk.CTkLabel(
            stats_frame,
            text="Esperando compresión...",
            text_color=("gray50", "gray70"),
            font=ctk.CTkFont(size=12)
        )
        self.size_label.pack(pady=5)
        
        self.progress_bar = ctk.CTkProgressBar(stats_frame, height=20, corner_radius=10)
        self.progress_bar.pack(fill="x", pady=10, padx=20)
        self.progress_bar.set(0)
        
        decompress_frame = ctk.CTkFrame(main_frame)
        decompress_frame.pack(fill="x", pady=10, padx=10)
        
        ctk.CTkLabel(
            decompress_frame,
            text="Descompresión",
            font=ctk.CTkFont(weight="bold")
        ).pack(pady=10)
        
        self.decompress_btn = ctk.CTkButton(
            decompress_frame,
            text="📤 Descomprimir Archivo",
            command=self.decompress_file,
            width=200,
            height=40,
            corner_radius=10,
            state="disabled"
        )
        self.decompress_btn.pack(pady=10)
        
        open_folder_btn = ctk.CTkButton(
            decompress_frame,
            text="📁 Abrir Carpeta",
            command=self.open_output_folder,
            width=200,
            height=35,
            corner_radius=10,
            fg_color=("#2E8B57", "#1F5E3B"),
            hover_color=("#267A49", "#164A2A")
        )
        open_folder_btn.pack(pady=5)
    
    def load_file(self):
        pass
    
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
        super().__init__(parent, compressor, "Compresión de Texto", "📝")
    
    def load_file(self):
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo de texto",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        if file_path:
            self.file_path = file_path
            file_size = self.get_file_size(file_path)
            self.file_label.configure(
                text=f"📄 Archivo: {os.path.basename(file_path)}\n"
                     f"📦 Tamaño: {self.format_size(file_size)}"
            )
            self.compress_btn.configure(state="normal")
    
    def compress_file(self):
        if not self.file_path:
            return
        try:
            self.update_progress(0.3)
            compressed_file = self.compressor.compress(self.file_path)
            self.compressed_path = compressed_file
            self.update_progress(0.8)
            original_size = self.get_file_size(self.file_path)
            compressed_size = self.get_file_size(compressed_file)
            compression_ratio = (1 - compressed_size / original_size) * 100
            self.size_label.configure(
                text=f"📊 Original: {self.format_size(original_size)}\n"
                     f"🗜️ Comprimido: {self.format_size(compressed_size)}\n"
                     f"📈 Ratio de compresión: {compression_ratio:.1f}%"
            )
            self.update_progress(1.0)
            self.decompress_btn.configure(state="normal")
            messagebox.showinfo("Éxito", "✅ Archivo comprimido correctamente")
        except Exception as e:
            self.update_progress(0)
            messagebox.showerror("Error", f"❌ Error al comprimir: {str(e)}")
    
    def decompress_file(self):
        if not self.compressed_path:
            return
        try:
            self.update_progress(0.3)
            decompressed_file = self.compressor.decompress(self.compressed_path)
            self.update_progress(0.8)
            compressed_size = self.get_file_size(self.compressed_path)
            decompressed_size = self.get_file_size(decompressed_file)
            self.update_progress(1.0)
            messagebox.showinfo("Éxito", 
                               f"✅ Archivo descomprimido correctamente\n\n"
                               f"🗜️ Tamaño comprimido: {self.format_size(compressed_size)}\n"
                               f"📄 Tamaño descomprimido: {self.format_size(decompressed_size)}")
        except Exception as e:
            self.update_progress(0)
            messagebox.showerror("Error", f"❌ Error al descomprimir: {str(e)}")

class ImageCompressionWindow(CompressionWindow):
    def __init__(self, parent, compressor):
        super().__init__(parent, compressor, "Compresión de Imágenes", "🖼️")
    
    def load_file(self):
        file_path = filedialog.askopenfilename(
            title="Seleccionar imagen",
            filetypes=[
                ("Imágenes", "*.png *.bmp *.jpg *.jpeg"),
                ("Todos los archivos", "*.*")
            ]
        )
        if file_path:
            self.file_path = file_path
            file_size = self.get_file_size(file_path)
            self.file_label.configure(
                text=f"🖼️ Archivo: {os.path.basename(file_path)}\n"
                     f"📦 Tamaño: {self.format_size(file_size)}"
            )
            self.compress_btn.configure(state="normal")
    
    def compress_file(self):
        if not self.file_path:
            return
        try:
            self.update_progress(0.2)
            compressed_file = self.compressor.compress(self.file_path)
            self.compressed_path = compressed_file
            self.update_progress(0.7)
            original_size = self.get_file_size(self.file_path)
            compressed_size = self.get_file_size(compressed_file)
            self.update_progress(0.9)
            compression_ratio = (1 - compressed_size / original_size) * 100
            self.size_label.configure(
                text=f"📊 Original: {self.format_size(original_size)}\n"
                     f"🗜️ Comprimido: {self.format_size(compressed_size)}\n"
                     f"📈 Ratio de compresión: {compression_ratio:.1f}%"
            )
            self.update_progress(1.0)
            self.decompress_btn.configure(state="normal")
            messagebox.showinfo("Éxito", "✅ Imagen comprimida correctamente")
        except Exception as e:
            self.update_progress(0)
            messagebox.showerror("Error", f"❌ Error al comprimir: {str(e)}")
    
    def decompress_file(self):
        if not self.compressed_path:
            return
        try:
            self.update_progress(0.2)
            decompressed_file = self.compressor.decompress(self.compressed_path)
            self.update_progress(0.7)
            compressed_size = self.get_file_size(self.compressed_path)
            decompressed_size = self.get_file_size(decompressed_file)
            self.update_progress(1.0)
            messagebox.showinfo("Éxito", 
                               f"✅ Imagen descomprimida correctamente\n\n"
                               f"🗜️ Tamaño comprimido: {self.format_size(compressed_size)}\n"
                               f"🖼️ Tamaño descomprimido: {self.format_size(decompressed_size)}")
        except Exception as e:
            self.update_progress(0)
            messagebox.showerror("Error", f"❌ Error al descomprimir: {str(e)}")

class AudioCompressionWindow(CompressionWindow):
    def __init__(self, parent, compressor):
        super().__init__(parent, compressor, "Compresión de Audio", "🎵")
        self.play_btn = None
        self.create_play_button()
    
    def create_play_button(self):
        main_frame = self.window.winfo_children()[0]
        for widget in main_frame.winfo_children():
            if isinstance(widget, ctk.CTkFrame) and "Descompresión" in str(widget.winfo_children()[0].cget("text")):
                self.play_btn = ctk.CTkButton(
                    widget,
                    text="▶️ Reproducir Audio",
                    command=self.play_audio,
                    width=200,
                    height=40,
                    corner_radius=10,
                    state="disabled",
                    fg_color=("#2E8B57", "#1F5E3B"),
                    hover_color=("#267A49", "#164A2A")
                )
                self.play_btn.pack(pady=5)
                break
    
    def load_file(self):
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo de audio",
            filetypes=[
                ("Archivos WAV", "*.wav"),
                ("Archivos MP3", "*.mp3"),
                ("Todos los archivos", "*.*")
            ]
        )
        if file_path:
            self.file_path = file_path
            file_size = self.get_file_size(file_path)
            self.file_label.configure(
                text=f"🎵 Archivo: {os.path.basename(file_path)}\n"
                     f"📦 Tamaño: {self.format_size(file_size)}"
            )
            self.compress_btn.configure(state="normal")
    
    def compress_file(self):
        if not self.file_path:
            return
        try:
            self.update_progress(0.2)
            compressed_file = self.compressor.compress(self.file_path)
            self.compressed_path = compressed_file
            self.update_progress(0.7)
            original_size = self.get_file_size(self.file_path)
            compressed_size = self.get_file_size(compressed_file)
            self.update_progress(0.9)
            compression_ratio = (1 - compressed_size / original_size) * 100
            self.size_label.configure(
                text=f"📊 Original: {self.format_size(original_size)}\n"
                     f"🗜️ Comprimido: {self.format_size(compressed_size)}\n"
                     f"📈 Ratio de compresión: {compression_ratio:.1f}%"
            )
            self.update_progress(1.0)
            self.decompress_btn.configure(state="normal")
            if self.play_btn:
                self.play_btn.configure(state="normal")
            messagebox.showinfo("Éxito", "✅ Audio comprimido correctamente")
        except Exception as e:
            self.update_progress(0)
            messagebox.showerror("Error", f"❌ Error al comprimir: {str(e)}")
    
    def decompress_file(self):
        if not self.compressed_path:
            return
        try:
            self.update_progress(0.2)
            decompressed_file = self.compressor.decompress(self.compressed_path)
            self.update_progress(0.7)
            compressed_size = self.get_file_size(self.compressed_path)
            decompressed_size = self.get_file_size(decompressed_file)
            self.update_progress(1.0)
            messagebox.showinfo("Éxito", 
                               f"✅ Audio descomprimido correctamente\n\n"
                               f"🗜️ Tamaño comprimido: {self.format_size(compressed_size)}\n"
                               f"🎵 Tamaño descomprimido: {self.format_size(decompressed_size)}")
        except Exception as e:
            self.update_progress(0)
            messagebox.showerror("Error", f"❌ Error al descomprimir: {str(e)}")
    
    def play_audio(self):
        if not self.compressed_path:
            return
        try:
            base_name = self.compressed_path.replace('_compressed.audiocomp', '_decompressed')
            
            for ext in ['.wav', '.mp3']:
                audio_file = base_name + ext
                if os.path.exists(audio_file):
                    self.compressor.play_audio(audio_file)
                    return
            
            messagebox.showwarning("Advertencia", "Primero debe descomprimir el archivo para reproducirlo")
        except Exception as e:
            messagebox.showerror("Error", f"❌ Error al reproducir audio: {str(e)}")

if __name__ == "__main__":
    root = ctk.CTk()
    app = CompressionApp(root)
    root.mainloop()