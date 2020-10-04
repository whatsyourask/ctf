#!/usr/bin/env python3

filename = 'TheMessage.txt'
data = open(filename, 'r').read()
decoded = ''
for char in data:
    decoded += '1' if char == ' ' else '0'
print(decoded)
