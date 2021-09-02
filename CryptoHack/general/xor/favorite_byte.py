from binascii import unhexlify
from pwn import xor

hex_str = '73626960647f6b206821204f21254f7d694f7624662065622127234f726927756d'
byte_str = unhexlify(hex_str)
for i in range(256):
    result = xor(byte_str, i).decode()
    if result.find('crypto{') == 0:
        print(result)
