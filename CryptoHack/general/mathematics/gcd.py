
def gcd(a, b):
    while b != 0:
        b, a = a % b, b
    return a

result = gcd(66528, 52920)
print(result)
