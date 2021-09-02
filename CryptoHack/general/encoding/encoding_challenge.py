from pwn import *
import json
import base64
import binascii
from Crypto.Util.number import long_to_bytes 
import codecs


def from_hex(hex_str):
    hex_str = hex_str
    return binascii.unhexlify(hex_str).decode()


def from_ascii(ascii_str):
    result = ''
    for i in ascii_str:
        result += chr(i)
    return result 


def from_rot13(rot13_str):
    return codecs.decode(rot13_str, 'rot-13')


def from_bigint(bigint_str):
    bigint_str = bigint_str[2:]
    bigint_str = binascii.unhexlify(bigint_str)
    return bigint_str.decode()


def from_base64(base64_str):
    return base64.b64decode(base64_str).decode()


def solve():
    con = remote('socket.cryptohack.org', 13377)
    encoding_funcs = {
        'base64': from_base64,
        'hex': from_hex,
        'rot13':from_rot13,
        'bigint':from_bigint,
        'utf-8':from_ascii
    }
    for i in range(100):
        message = con.recv()
        message = json.loads(message)
        encoding_type = message['type']
        encoded_message = message['encoded']
        decoded = encoding_funcs[encoding_type](encoded_message)
        result = {}
        result['decoded'] = decoded
        result = json.dumps(result)
        con.send(result.encode())
    print(con.recv())
    con.close()


if __name__=='__main__':
    solve()
