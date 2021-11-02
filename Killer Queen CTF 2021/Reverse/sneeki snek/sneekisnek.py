#!/usr/bin/env python3

# 4
f = ''

# 5
a = 'rwhxi}eomr\\^`Y'

# 6
z = 'f]XdThbQd^TYL&\x13g'

# 7
a += z

# 8
for i, b in enumerate(a):
    # 9
    c = ord(b)

    # 10
    c -= 7

    # 11
    c += i

    # 12
    c = chr(c)

    # 13
    f += c

# 14
print(f)
