import os
import pickle
from PIL import Image
import numpy as np

class ImageCompressor:
    def __init__(self):
        pass
    
    def rle_compress(self, data):
        """Compresión Run-Length Encoding"""
        if len(data) == 0:
            return []
        
        compressed = []
        count = 1
        current = data[0]
        
        for i in range(1, len(data)):
            if data[i] == current and count < 255:
                count += 1
            else:
                compressed.append((current, count))
                current = data[i]
                count = 1
        
        compressed.append((current, count))
        return compressed
    
    def rle_decompress(self, compressed_data):
        """Descompresión Run-Length Encoding"""
        decompressed = []
        for value, count in compressed_data:
            decompressed.extend([value] * count)
        return decompressed
    
    def compress(self, input_file):
        try:
            img = Image.open(input_file)
        except Exception as e:
            raise Exception(f"No se pudo cargar la imagen: {str(e)}")
        img_array = np.array(img)
        compressed_channels = []
        original_shape = img_array.shape
        
        if len(original_shape) == 2:
            compressed_data = self.rle_compress(img_array.flatten().tolist())
            compressed_channels.append(compressed_data)
        else:
            for channel in range(original_shape[2]):
                channel_data = img_array[:, :, channel].flatten().tolist()
                compressed_data = self.rle_compress(channel_data)
                compressed_channels.append(compressed_data)
        compressed_data = {
            'compressed_channels': compressed_channels,
            'original_shape': original_shape,
            'mode': img.mode
        }
        
        output_file = os.path.splitext(input_file)[0] + '_compressed.rle'
        with open(output_file, 'wb') as file:
            pickle.dump(compressed_data, file)
        
        return output_file
    
    def decompress(self, input_file):
        with open(input_file, 'rb') as file:
            compressed_data = pickle.load(file)
        
        compressed_channels = compressed_data['compressed_channels']
        original_shape = compressed_data['original_shape']
        mode = compressed_data['mode']
        decompressed_channels = []
        for compressed_channel in compressed_channels:
            decompressed_data = self.rle_decompress(compressed_channel)
            decompressed_channels.append(decompressed_data)
        
        if len(original_shape) == 2:
            img_array = np.array(decompressed_channels[0]).reshape(original_shape)
            img = Image.fromarray(img_array.astype('uint8'), mode)
        else:
            pixels = []
            for i in range(len(decompressed_channels[0])):
                pixel = []
                for channel in decompressed_channels:
                    pixel.append(channel[i])
                pixels.append(pixel)
            
            img_array = np.array(pixels).reshape(original_shape)
            img = Image.fromarray(img_array.astype('uint8'), mode)
    
        output_file = os.path.splitext(input_file)[0] + '_decompressed.png'
        img.save(output_file)
        
        return output_file