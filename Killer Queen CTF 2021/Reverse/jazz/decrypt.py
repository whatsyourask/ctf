#!/usr/bin/env python3


build = '''9xLmMiI2znmPam'D_A_1:RQ;Il\*7:%i".R<'''
print(build)
build = list(map(ord, build))
build1 = [build[i] for i in range(len(build)) if i % 2]
build2 = [build[i] for i in range(len(build)) if not i % 2]
#print(build1)
#print(len(build1))
#print(build2)
#print(len(build2))
flag = []
print(build)
for i,j in zip(build1, build2):
    for one in range(-157, 158):
        for two in range(-157, 158):
            temp1 = (2 * two - one + 153) % 93 + 33
            temp2 = (one - two + 93) % 93 + 33
            if temp1 == j and temp2 == i:
                one1 = 158 - one
                two2 = 158 - two
                print(chr(temp1), chr(temp2), '|', chr(two2), chr(one1))
                flag.append(two2)
                flag.append(one1)
print(''.join(map(chr, flag)))
flag = [''.join(map(chr, flag[i])) for i in range(len(flag)) if i % 2]
print(flag)

