from scalar_multiplication import PointWithMultOp
import hashlib


modulus = 9739
g = PointWithMultOp(1804, 5368, modulus)
q_a = PointWithMultOp(815, 3190, modulus)
secret = 1829
key = q_a.mul(secret)
print(key.x)
flag = 'crypto{' + hashlib.sha1(str(key.x).encode()).hexdigest() + '}'
print(flag)
