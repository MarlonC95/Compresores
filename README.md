# 🗜️ Sistema de Compresión de Datos

## ✨ Características

 📝 Compresión de Texto
**Algoritmo**: Huffman Coding
**Formatos**: `.txt`, `.bin` (comprimidos)
Vista previa del texto original y comprimido

🖼️ Compresión de Imágenes  
**Algoritmo**: Run-Length Encoding (RLE)
**Formatos**: `.png`, `.jpg`, `.jpeg`, `.bmp`, `.rle`
Visualización lado a lado

🎵 Compresión de Audio
**Algoritmo**: Codificación Diferencial + RLE
**Formatos**: `.wav`, `.mp3`, `.audiocomp`
Reproducción integrada de audio

🚀 Instalación

```bash
# Instalar dependencias
pip install customtkinter==5.2.2 Pillow==10.2.0 numpy==1.26.4 scipy==1.13.0 pygame==2.5.2 pydub==0.25.1 ffmpeg-python==0.2.0

```🏗️ Estructura
compression_app/
├── main.py
├── requirements.txt
├── compression/
│   ├── text_compression.py
│   ├── image_compression.py
│   └── audio_compression.py
└── comprimidos/
    ├── texto/
    ├── imagenes/
    └── audio/

🎯 Uso
Seleccionar tipo de archivo en pantalla principal

Cargar archivo a comprimir/descomprimir

Comprimir o descomprimir según el caso

Ver estadísticas y vista previa

Abrir carpeta de archivos procesados

🔧 Algoritmos
Texto: Codificación Huffman - compresión sin pérdida

Imágenes: RLE - compresión de secuencias de píxeles

Audio: Codificación diferencial + RLE - mantiene calidad
