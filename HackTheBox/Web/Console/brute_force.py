import hashlib


def get_content(filename):
    return open(filename, 'rb').read().split(b'\n')[0]

my_hash = get_content('hash')
salt = get_content('salt')
my_ip = get_content('host_ip')
wordlist = open('/usr/share/wordlists/rockyou.txt', 'rb').read().split(b'\n')
for word in wordlist:
    new_hash = word + salt
    first_hash = hashlib.sha256(new_hash).hexdigest().encode()
    second_hash = my_ip + first_hash
    third_hash = hashlib.sha256(second_hash).hexdigest().encode()
    #print(third_hash, my_hash)
    if third_hash == my_hash:
        print('Password: ', word.decode())
        break
