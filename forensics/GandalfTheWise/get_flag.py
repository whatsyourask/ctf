#!/usr/bin/env python3
import sys
import os
import base64


def get_data():
    # Get the strings from file
    filename = sys.argv[1]
    out      = 'result.txt'
    # I dunno how to extract that lines without strings and in python
    os.system(f"strings -n 16 {filename} > {out}")
    # I remove all rubbish from the end here
    strings  = open(out, 'r').read().split('\n')[1:-2]
    new = []
    for string in strings:
        # Remove '+' from start
        new.append(string[1:])
    return new


def base64_decode(strings):
    # Decode them
    decoded = []
    for elem in strings:
        out = base64.b64decode(elem.encode())
        decoded.append(out)
    return decoded


def xor(decoded):
    result = ''
    for i in range(len(decoded[0])):
        # Output of decoding is integer
        # So we don't need use ord()
        result += chr(decoded[0][i] ^ decoded[1][i])
    return result


strings = get_data()
decoded = base64_decode(strings)
result  = xor(decoded)
print(result)
