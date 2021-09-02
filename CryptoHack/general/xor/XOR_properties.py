from pwn import xor
from binascii import unhexlify, hexlify


key1 = 'a6c8b6733c9b22de7bc0253266a3867df55acde8635e19c73313'
first_op = '37dcb292030faa90d07eec17e3b1c6d8daf94c35d4c9191a5e1e'
second_op = 'c1545756687e7573db23aa1c3452a098b71a7fbf0fddddde5fc1'
third_op = '04ee9855208a2cd59091d04767ae47963170d1660df7f56f5faf'

key1 = unhexlify(key1)
first_op = unhexlify(first_op)
second_op = unhexlify(second_op)
third_op = unhexlify(third_op)
temp1 = xor(third_op, second_op)
flag = xor(temp1, key1)
print(flag, '\n')
