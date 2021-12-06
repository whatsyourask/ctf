import sys
import requests
import re
import hashlib


def get_flag(ip, port):
    url = f'http://{ip}:{port}/'
    s = requests.Session()
    res = s.get(url)
    str_to_enc = re.search("<h3 align='center'>(\d|\w)+", res.text)[0]
    str_to_enc = str_to_enc[19:]
    print(str_to_enc)
    md5 = hashlib.md5()
    md5.update(str_to_enc.encode())
    encoded = md5.hexdigest()
    print(encoded)
    res = s.post(url, data={'hash': encoded})
    print(res.text)


def main():
    ip = sys.argv[1]
    port = sys.argv[2]
    get_flag(ip, port)


if __name__=='__main__':
    main()
