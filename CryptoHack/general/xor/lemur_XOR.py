import sys
from pwn import xor
from binascii import unhexlify

def get_file_content(filename):
    return open(filename, 'rb').read() 


lemur_img_filename = sys.argv[1]
flag_img_filename = sys.argv[2]
lemur_img = get_file_content(lemur_img_filename)
flag_img = get_file_content(flag_img_filename)
