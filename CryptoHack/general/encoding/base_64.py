import base64
import binascii


hex_str = '72bca9b68fc16ac7beeb8f849dca1d8a783e8acf9679bf9269f7bf'
byte_str = binascii.unhexlify(hex_str)
flag = base64.b64encode(byte_str)
print(flag)
