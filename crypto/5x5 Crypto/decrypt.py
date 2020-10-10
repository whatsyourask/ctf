#!/usr/bin/env python3
import sys


def get_tap_code():
    # Generate the tap code table
    tap_code = []
    temp     = chr(ord('A') - 1)
    for i in range(5):
        tap_code.append([])
        for j in range(5):
            temp = chr(ord(temp) + 1)
            if temp == 'K':
                # Just switch on next letter
                temp = chr(ord(temp) + 1)
            tap_code[i].append(temp)
    return tap_code


def decode(ciphertext, tap_code):
    plaintext = ''
    for cipher in ciphertext:
        if cipher != '{' and cipher != '}' and cipher != '_':
            row        = int(cipher[0]) - 1
            column     = int(cipher[2]) - 1
            plaintext += tap_code[row][column]
        else:
            plaintext += cipher
    return plaintext


tap_code   = get_tap_code()
ciphertext = sys.argv[1].split(',')
print(ciphertext)
print(decode(ciphertext, tap_code))
