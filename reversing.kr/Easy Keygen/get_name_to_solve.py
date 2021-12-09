serial_number = [0x5B, 0x13, 0x49, 0x77, 0x13, 0x5E, 0x7D, 0x13]
i = 0
xor_values = [16, 32, 48]
name = ''
for char in serial_number:
    if i > 2:
        i = 0
    name += chr(char ^ xor_values[i])
    i += 1
print(name)
