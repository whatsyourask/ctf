import sys
from base64 import b64decode
from Crypto.Util.number import bytes_to_long
#import pem


pem_filename = sys.argv[1]
pem = b'\n'.join(open(pem_filename, 'rb').read().split(b'\n')[1:-2])
print(pem)
pem = b64decode(pem)
print(pem)
print(bytes_to_long(pem))
#certs = pem.parse_file(pem_filename)
#print(certs)
#print(certs[0])
