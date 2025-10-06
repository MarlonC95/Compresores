import os
import pickle
import numpy as np
from scipy.io import wavfile
import simpleaudio as sa

class AudioCompressor:
    def __init__(self):
        pass
    
    def differential_encoding(self, data):
        """Codificación diferencial para audio"""
        encoded = [data[0]]
        for i in range(1, len(data)):
            encoded.append(data[i] - data[i-1])
        return encoded
    
    def differential_decoding(self, encoded_data):
        """Decodificación diferencial"""
        decoded = [encoded_data[0]]
        for i in range(1, len(encoded_data)):
            decoded.append(encoded_data[i] + decoded[i-1])
        return decoded
    
    def rle_compress_audio(self, data, threshold=10):
        """RLE adaptado para audio con umbral de diferencia"""
        if len(data) == 0:
            return []
        
        compressed = []
        count = 1
        current = data[0]
        
        for i in range(1, len(data)):
            if abs(data[i] - current) <= threshold and count < 255:
                count += 1
                current = (current * (count - 1) + data[i]) / count
            else:
                compressed.append((int(current), count))
                current = data[i]
                count = 1
        
        compressed.append((int(current), count))
        return compressed
    
    def rle_decompress_audio(self, compressed_data):
        """Descompresión RLE para audio"""
        decompressed = []
        for value, count in compressed_data:
            decompressed.extend([value] * count)
        return decompressed
    
    def compress(self, input_file):
        file_ext = os.path.splitext(input_file)[1].lower()
        
        if file_ext == '.wav':
            return self.compress_wav(input_file)
        else:
            raise Exception("Formato de audio no soportado. Use archivos WAV.")
    
    def compress_wav(self, input_file):
        try:
            sample_rate, audio_data = wavfile.read(input_file)
        except Exception as e:
            raise Exception(f"No se pudo cargar el archivo WAV: {str(e)}")
        if len(audio_data.shape) > 1:
            audio_data = np.mean(audio_data, axis=1)
        
        # Normalizar datos de audio
        audio_data = audio_data.astype(np.int16)
        diff_encoded = self.differential_encoding(audio_data.tolist())
        compressed_data = self.rle_compress_audio(diff_encoded)
        compressed_info = {
            'compressed_data': compressed_data,
            'sample_rate': sample_rate,
            'original_length': len(audio_data),
            'data_type': 'wav'
        }
        
        output_file = os.path.splitext(input_file)[0] + '_compressed.audiocomp'
        with open(output_file, 'wb') as file:
            pickle.dump(compressed_info, file)
        
        return output_file
    
    def decompress(self, input_file):
        with open(input_file, 'rb') as file:
            compressed_info = pickle.load(file)
        
        compressed_data = compressed_info['compressed_data']
        sample_rate = compressed_info['sample_rate']
        data_type = compressed_info['data_type']
        
        if data_type == 'wav':
            diff_decoded = self.rle_decompress_audio(compressed_data)
            audio_data = self.differential_decoding(diff_decoded)
            audio_array = np.array(audio_data, dtype=np.int16)
            output_file = os.path.splitext(input_file)[0] + '_decompressed.wav'
            wavfile.write(output_file, sample_rate, audio_array)
            
            return output_file
        else:
            raise Exception("Tipo de audio no soportado")
    
    def play_audio(self, audio_file):
        """Reproducir archivo de audio"""
        try:
            if audio_file.endswith('.wav'):
                wave_obj = sa.WaveObject.from_wave_file(audio_file)
                play_obj = wave_obj.play()
                play_obj.wait_done()
            else:
                raise Exception("Formato de audio no soportado para reproducción")
        except Exception as e:
            raise Exception(f"Error al reproducir audio: {str(e)}")