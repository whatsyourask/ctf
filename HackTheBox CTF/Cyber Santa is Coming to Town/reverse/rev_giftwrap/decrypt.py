check = [0xbb, 0xa7, 0xb1, 0x88, 0x86, 0x83, 0x8b, 0xac, 0xc7, 0xc2, 0x9d, 0x87,
         0xac, 0xc6, 0xc3, 0xac, 0x9b, 0xc7, 0x81, 0x97, 0xd2, 0xd2, 0x8e]
flag = ''
for byte in check:
    flag += chr(byte ^ 243)
print(flag)
