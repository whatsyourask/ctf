# Read the file with challenge data
data = open('rsanoob (1).txt', 'r').read().split('\n')
# Get e, c, n for RSA
e = int(data[0][3:])
c = int(data[1][2:])
n = int(data[2][3:])
# Get the factorial of n from file in that i put the result from factordb
factordb = open('factordb_result.txt', 'r').read().split('\n')
# Get p and q
p = int(factordb[0][2:])
q = int(factordb[1][2:])
# Calculate euler's totient function
phi = (p - 1) * (q - 1)
# Find the invert or d = e^(-1) mod phi
d = gmpy.invert(e, phi)
# Decrypt the ciphertext
# plaintext = (ciphertext)^d mod n
plaintext = long_to_bytes(pow(c, d, n)).decode()
print(str(plaintext))
