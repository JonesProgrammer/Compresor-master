from logicahuffman import HuffmanCoding
import time
import sys

txt_path = sys.argv[1]

hff = HuffmanCoding(txt_path)

start = time.time()
compressed_path = hff.compress()
end = time.time()

total = end - start 

print(total)
