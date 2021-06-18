from Crypto.PublicKey import RSA
import base64
import requests
import re
from Crypto.Cipher import PKCS1_OAEP
import gmpy
import binascii


def get_req(url, param, data):
    params = {}
    params[param] = data
    r = requests.get(url, params=params)
    return r.text


def find_factor(text):
    temp = re.findall(r'query" value="\d{1,}', text)[0]
    ind = temp.find('value="') + 7
    return int(temp[ind:])


def decrypt(flag, d, n):
    # Convert in int format
    int_flag = int.from_bytes(flag, byteorder="big")
    # Calculate c ^ d mod n
    decrypted_flag = pow(int_flag, d, n)
    # Calculate the length of the hex string
    bytes_len = len(hex(decrypted_flag)[2:]) // 2 + 1
    # Convert to byte string again
    byte_flag = decrypted_flag.to_bytes(bytes_len, byteorder="big")
    # Decode
    flag = byte_flag.decode('utf-8', errors='ignore')
    return flag


def main():
    key = ''.join(open('key.pub', 'r').read().split('\n')[1:-2]).encode()
    key = base64.b64decode(key)
    pub_key = RSA.importKey(key)
    print('n = ', pub_key.n)
    url = 'http://factordb.com/index.php'
    # Get links to factor of n
    text = get_req(url, 'query', str(pub_key.n))
    results = re.findall(r'href="index.php\?id=\d{1,19}', text)[1:]
    id_ind = results[0].find('?id=') + 4
    first_link = results[0][id_ind:]
    second_link = results[1][id_ind:]
    # Go to links and take p and q
    text2 = get_req(url, 'id', str(first_link))
    text3 = get_req(url, 'id', str(second_link))
    p = find_factor(text2)
    q = find_factor(text3)
    print('p = ', p)
    print('q = ', q)
    # Calculate euler function
    euler_func = (p - 1) * (q - 1)
    # Calculate private key d
    d = gmpy.invert(pub_key.e, euler_func)
    print('d = ', d, '\n')
    flag = open('flag.enc', 'rb').read()
    flag = decrypt(flag, int(d), int(pub_key.n))
    print(flag)


main()
