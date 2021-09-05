from Crypto.PublicKey import RSA
import sys


pem = open(sys.argv[1], 'r').read()
key = RSA.importKey(pem)
print(key.n)
