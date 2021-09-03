def extended_gcd(p, q):
    # https://www.geeksforgeeks.org/python-program-for-basic-and-extended-euclidean-algorithms-2/
    if p == 0:
        return q, 0, 1
    gcd, x_i, y_i = extended_gcd(q % p, p)
    x = y_i - (q // p) * x_i
    y = x_i
    return gcd, x, y

result = extended_gcd(26513, 32321)
print(result)
