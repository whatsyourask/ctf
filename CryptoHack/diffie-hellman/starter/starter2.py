def check(g, p):
    for i in range(2, p):
        if pow(g, i, p) == g:
            return i
    return p


# Simple brute force from 2 to p and checking if there are elements in Fp such as g^i mod p for current g.
p = 28151
for g in range(2, p):
    if check(g, p) == p:
        print(g)
        exit()
