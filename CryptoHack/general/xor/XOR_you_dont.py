from binascii import unhexlify
from pwn import xor

hex_str = '0e0b213f26041e480b26217f27342e175d0e070a3c5b103e2526217f27342e175d0e077e263451150104'
byte_str = unhexlify(hex_str)
print(byte_str)
key = xor(byte_str, 'crypto{'.encode())[:7] + b'y'
print(key)
print(xor(byte_str, key))
