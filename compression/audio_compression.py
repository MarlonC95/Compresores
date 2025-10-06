import os
import pickle
import numpy as np
from scipy.io import wavfile
import simpleaudio as sa
from datetime import datetime
from pydub import AudioSegment
import tempfile

class AudioCompressor:
    def __init__(self, output_dir="comprimidos/audio"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def differential_encoding(self, data):
        encoded = [data[0]]
        for i in range(1, len(data)):
            encoded.append(data[i] - data[i-1])
        return encoded
    
    def differential_decoding(self, encoded_data):
        decoded = [encoded_data[0]]
        for i in range(1, len(encoded_data)):
            decoded.append(encoded_data[i] + decoded[i-1])
        return decoded
    
    def rle_compress_audio(self, data, threshold=10):
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
        decompressed = []
        for value, count in compressed_data:
            decompressed.extend([value] * count)
        return decompressed
    
    def convert_to_wav(self, input_file):
        file_ext = os.path.splitext(input_file)[1].lower()
        
        if file_ext == '.wav':
            return input_file
        
        elif file_ext == '.mp3':
            try:
                audio = AudioSegment.from_mp3(input_file)
                temp_wav = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
                audio.export(temp_wav.name, format='wav')
                return temp_wav.name
            except Exception as e:
                raise Exception(f"Error al convertir MP3 a WAV: {str(e)}")
        
        else:
            raise Exception(f"Formato de audio no soportado: {file_ext}")
    
    def compress(self, input_file):
        file_ext = os.path.splitext(input_file)[1].lower()
        
        if file_ext in ['.wav', '.mp3']:
            return self.compress_audio(input_file)
        else:
            raise Exception("Formato de audio no soportado. Use archivos WAV o MP3.")
    
    def compress_audio(self, input_file):
        temp_wav_file = None
        try:
            if input_file.lower().endswith('.mp3'):
                temp_wav_file = self.convert_to_wav(input_file)
                wav_file_path = temp_wav_file
            else:
                wav_file_path = input_file
            
            sample_rate, audio_data = wavfile.read(wav_file_path)
            
            if len(audio_data.shape) > 1:
                audio_data = np.mean(audio_data, axis=1)
            
            audio_data = audio_data.astype(np.int16)
            diff_encoded = self.differential_encoding(audio_data.tolist())
            compressed_data = self.rle_compress_audio(diff_encoded)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.splitext(os.path.basename(input_file))[0]
            output_file = os.path.join(self.output_dir, f"{filename}_compressed_{timestamp}.audiocomp")
            
            compressed_info = {
                'compressed_data': compressed_data,
                'sample_rate': sample_rate,
                'original_length': len(audio_data),
                'data_type': 'wav',
                'original_format': os.path.splitext(input_file)[1].lower()
            }
            
            with open(output_file, 'wb') as file:
                pickle.dump(compressed_info, file)
            
            return output_file
            
        except Exception as e:
            raise Exception(f"Error al comprimir audio: {str(e)}")
        
        finally:
            if temp_wav_file and os.path.exists(temp_wav_file):
                os.unlink(temp_wav_file)
    
    def decompress(self, input_file):
        with open(input_file, 'rb') as file:
            compressed_info = pickle.load(file)
        
        compressed_data = compressed_info['compressed_data']
        sample_rate = compressed_info['sample_rate']
        original_format = compressed_info.get('original_format', '.wav')
        
        diff_decoded = self.rle_decompress_audio(compressed_data)
        audio_data = self.differential_decoding(diff_decoded)
        audio_array = np.array(audio_data, dtype=np.int16)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.splitext(os.path.basename(input_file))[0]
        
        if original_format == '.mp3':
            output_file = os.path.join(self.output_dir, f"{filename}_decompressed_{timestamp}.mp3")
            
            temp_wav = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
            wavfile.write(temp_wav.name, sample_rate, audio_array)
            
            try:
                audio = AudioSegment.from_wav(temp_wav.name)
                audio.export(output_file, format='mp3')
            finally:
                if os.path.exists(temp_wav.name):
                    os.unlink(temp_wav.name)
                    
        else:
            output_file = os.path.join(self.output_dir, f"{filename}_decompressed_{timestamp}.wav")
            wavfile.write(output_file, sample_rate, audio_array)
        
        return output_file
    
    def play_audio(self, audio_file):
        try:
            file_ext = os.path.splitext(audio_file)[1].lower()
            
            if file_ext == '.wav':
                wave_obj = sa.WaveObject.from_wave_file(audio_file)
                play_obj = wave_obj.play()
                play_obj.wait_done()
                
            elif file_ext == '.mp3':
                temp_wav = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
                try:
                    audio = AudioSegment.from_mp3(audio_file)
                    audio.export(temp_wav.name, format='wav')
                    
                    wave_obj = sa.WaveObject.from_wave_file(temp_wav.name)
                    play_obj = wave_obj.play()
                    play_obj.wait_done()
                    
                finally:
                    if os.path.exists(temp_wav.name):
                        os.unlink(temp_wav.name)
                        
            else:
                raise Exception("Formato de audio no soportado para reproducción")
                
        except Exception as e:
            raise Exception(f"Error al reproducir audio: {str(e)}")