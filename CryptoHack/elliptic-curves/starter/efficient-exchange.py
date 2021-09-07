from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib
from scalar_multiplication import PointWithMultOp


def is_pkcs7_padded(message):
    padding = message[-message[-1]:]
    return all(padding[i] == len(padding) for i in range(0, len(padding)))


def decrypt_flag(shared_secret: int, iv: str, ciphertext: str):
    # Derive AES key from shared secret
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode('ascii'))
    key = sha1.digest()[:16]
    # Decrypt flag
    ciphertext = bytes.fromhex(ciphertext)
    iv = bytes.fromhex(iv)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)

    if is_pkcs7_padded(plaintext):
        return unpad(plaintext, 16).decode('ascii')
    else:
        return plaintext.decode('ascii')


def calculate_y(a, b, modulus, x):
    sq_y = (x ** 3 + a * x + b) % modulus
    # https://www.rieselprime.de/ziki/Modular_square_root
    # from here we need to use formula for p = 3 mod 4
    y = pow(sq_y, (modulus + 1) // 4, modulus)
    return y


a = 497
b = 1768
modulus = 9739
n = 6534
q_x = 4726
y = calculate_y(a, b, modulus, q_x)
print(y)
q_a = PointWithMultOp(4726, y, modulus)
print(q_a.x, q_a.y)
s = q_a.mul(n)
print(s.x, s.y)
shared_secret = s.x
iv = 'cd9da9f1c60925922377ea952afc212c'
ciphertext = 'febcbe3a3414a730b125931dccf912d2239f3e969c4334d95ed0ec86f6449ad8'

print(decrypt_flag(shared_secret, iv, ciphertext))
