from logicahuffman import HuffmanCoding
import time
import sys


compressed_path = sys.argv[1]


hff = HuffmanCoding(compressed_path)

start = time.time()
decompressed_path = hff.decompress(compressed_path)
end = time.time()

total = end - start 

print(total)

