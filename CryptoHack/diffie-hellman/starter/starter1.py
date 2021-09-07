g = 209
p = 991
for d in range(p):
    if (g * d) % p == 1:
        print(d)
