import heapq
import pickle
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

class HuffmanCoding:
    class HeapNode:
        def __init__(self, char, freq):
            self.char = char
            self.freq = freq
            self.left = None
            self.right = None

        def __lt__(self, other):
            return self.freq < other.freq

        def __eq__(self, other):
            return self.freq == other.freq if isinstance(other, self.__class__) else False

    def __init__(self, path):
        self.path = path
        self.heap = []
        self.codes = {}
        self.reverse_mapping = {}

    def make_frequency_dict(self, text):
        frequency = {}
        for character in text:
            frequency[character] = frequency.get(character, 0) + 1
        return frequency

    def make_heap(self, frequency):
        self.heap = [self.HeapNode(char, freq) for char, freq in frequency.items()]
        heapq.heapify(self.heap)

    def merge_nodes(self):
        while len(self.heap) > 1:
            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)
            merged = self.HeapNode(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2
            heapq.heappush(self.heap, merged)

    def make_codes_helper(self, root, current_code):
        if root is None:
            return
        if root.char is not None:
            self.codes[root.char] = current_code
            self.reverse_mapping[current_code] = root.char
            return
        self.make_codes_helper(root.left, current_code + "0")
        self.make_codes_helper(root.right, current_code + "1")

    def make_codes(self):
        root = heapq.heappop(self.heap)
        self.make_codes_helper(root, "")

    def get_encoded_text(self, text):
        encoded_text = ""
        for character in text:
            encoded_text += self.codes[character]
        return encoded_text

    def pad_encoded_text(self, encoded_text):
        extra_padding = 8 - len(encoded_text) % 8
        padded_encoded_text = encoded_text + "0" * extra_padding
        padded_info = "{0:08b}".format(extra_padding)
        return padded_info + padded_encoded_text

    def get_byte_array(self, padded_encoded_text):
        return bytearray(int(padded_encoded_text[i:i + 8], 2) for i in range(0, len(padded_encoded_text), 8))

    def compress(self, n):
        output_path = "comprimidop.elmejorprofesor"

        with open(self.path, 'rb') as file, open(output_path, 'wb') as output:
            text = file.read()
            frequency = self.make_frequency_dict(text)
            self.make_heap(frequency)
            self.merge_nodes()
            self.make_codes()
            with open('dictionary.bin', 'wb') as dictionary:
                    pickle.dump(self.reverse_mapping, dictionary)
            if rank == 0:
                #contenido padre
                dtext = ''
                for i in range (1,n):
                    dtext += comm.recv(source = i)
                padded_encoded_text = self.pad_encoded_text(dtext)
                byte_array = self.get_byte_array(padded_encoded_text)
                output.write(bytes(byte_array))
                return output_path
            
            else:
                #contenido hijos
                division = len(text)//(n-1)
                if rank == n-1:
                    encoded_text = self.get_encoded_text(text[division*(rank-1):len(text)])
                else:
                    encoded_text = self.get_encoded_text(text[division*(rank-1):(division*rank)+1])
                comm.send(encoded_text, dest = 0)

    def remove_padding(self, padded_encoded_text):
        padded_info = padded_encoded_text[:8]
        extra_padding = int(padded_info, 2)
        return padded_encoded_text[8:-extra_padding]

    def decode_text(self, encoded_text):
        current_code = ""
        decoded_text = b""
        for bit in encoded_text:
            current_code += bit
            if current_code in self.reverse_mapping:
                character = self.reverse_mapping[current_code]
                decoded_text += character
                current_code = ""
        return decoded_text

    def clean_dict(self):
        self.reverse_mapping = {key: value.to_bytes(1, 'big') for key, value in self.reverse_mapping.items()}

    def decompress(self, input_path, n):
        output_path = "descomprimidop-elmejorprofesor.txt"

        with open('dictionary.bin', 'rb') as dictionary:
            self.reverse_mapping = pickle.load(dictionary)

        self.clean_dict()

        with open(input_path, 'rb') as file, open(output_path, 'wb') as output:
            bit_string = "".join(f"{byte:08b}" for byte in file.read())
            encoded_text = self.remove_padding(bit_string)
            if rank != 0:
                #contenido hijo
                division = len(bit_string)//(n-1)
                if rank == n-1:
                    decompressed_text = self.decode_text(encoded_text[division*(rank-1):len(encoded_text)])
                else:
                    decompressed_text = self.decode_text(encoded_text[division*(rank-1):(division*rank)+1])
                comm.send(decompressed_text, dest = 0)
            else:
                #contenido padre
                etext = b""
                for i in range (1,n):
                    etext += comm.recv(source = i)
                output.write(bytes(etext))
                return output_path
