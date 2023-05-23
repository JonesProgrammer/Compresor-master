from parallelizedHuffman import HuffmanCoding
import time
from mpi4py import MPI
import sys

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

txt_path = sys.argv[1]


hff = HuffmanCoding(txt_path)

start = time.time()
compressed_path = hff.compress(size)
end = time.time()

total = end - start 

print(total, rank)