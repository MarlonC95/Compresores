import heapq
import os
import pickle
from collections import Counter

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
    
    def __lt__(self, other):
        return self.freq < other.freq

class TextCompressor:
    def __init__(self):
        pass
    
    def build_huffman_tree(self, text):
        frequency = Counter(text)
        
        heap = [HuffmanNode(char, freq) for char, freq in frequency.items()]
        heapq.heapify(heap)
        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)
            merged = HuffmanNode(None, left.freq + right.freq)
            merged.left = left
            merged.right = right
            heapq.heappush(heap, merged)
        
        return heap[0] if heap else None
    
    def build_codes(self, root):
        codes = {}
        
        def traverse(node, code):
            if node:
                if node.char is not None:
                    codes[node.char] = code
                traverse(node.left, code + '0')
                traverse(node.right, code + '1')
        
        traverse(root, '')
        return codes
    
    def compress_text(self, text):
        if not text:
            return "", {}
        
        root = self.build_huffman_tree(text)
        codes = self.build_codes(root)
        
        # Codificar texto
        encoded_text = ''.join(codes[char] for char in text)
        
        return encoded_text, codes
    
    def decompress_text(self, encoded_text, codes):
        reverse_codes = {v: k for k, v in codes.items()}
        current_code = ""
        decoded_text = ""
        
        for bit in encoded_text:
            current_code += bit
            if current_code in reverse_codes:
                decoded_text += reverse_codes[current_code]
                current_code = ""
        
        return decoded_text
    
    def compress(self, input_file):
        with open(input_file, 'r', encoding='utf-8') as file:
            text = file.read()
        encoded_text, codes = self.compress_text(text)
        compressed_data = {
            'encoded_text': encoded_text,
            'codes': codes,
            'original_size': len(text)
        }
        output_file = os.path.splitext(input_file)[0] + '_compressed.bin'
        with open(output_file, 'wb') as file:
            pickle.dump(compressed_data, file)
        
        return output_file
    
    def decompress(self, input_file):
        with open(input_file, 'rb') as file:
            compressed_data = pickle.load(file)
        encoded_text = compressed_data['encoded_text']
        codes = compressed_data['codes']
        decoded_text = self.decompress_text(encoded_text, codes)
        output_file = os.path.splitext(input_file)[0] + '_decompressed.txt'
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(decoded_text)
        
        return output_file