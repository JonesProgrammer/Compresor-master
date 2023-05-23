from parallelizedHuffman import HuffmanCoding
import time
from mpi4py import MPI
import sys

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()


compressed_path = sys.argv[1]


plf = HuffmanCoding(compressed_path)

start = time.time()
decompressed_path = plf.decompress(compressed_path, size)
end = time.time()

total = end - start 

print(total, rank)