#!/usr/bin/env python3

filename = 'TheMessage.txt'
data = open(filename, 'r').read()
decoded = ''
for char in data:
    decoded += '0' if char == ' ' else '1'
print(decoded)
