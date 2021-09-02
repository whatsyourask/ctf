given_str = 'label'
result = ''
xor_value = 13
for char in given_str:
    result += chr(ord(char) ^ xor_value)
print(result)
