# Console

Completed: Yes
Platform: HackTheBox

I opened the main page of URL in firefox and got the message to make sure that I have PHP console in order to be prompted for a password. I didn't understand it at the beginning, but after some time, I got it and found this tool: [https://github.com/barbushin/php-console](https://github.com/barbushin/php-console). It is a chrome extension. Install it, but only with `Load unpacked`. And you will be prompted for a password. Try to send some passwords and check the network panel. You will find this:

```bash
PHP-Console: {"protocol":5,"auth":{"publicKey":"6db23b5c4654088d9d2ebee9bceea4182649c1a635931d5b0934886d95b8f9bb","isSuccess":false},"docRoot":null,"sourcesBasePath":null,"getBackData":null,"isLocal":null,"isSslOnlyMode":false,"isEvalEnabled":null,"messages":[]}
```

Okay, we have a hash. And also, we have a source code, don't forget to view it. Particularly, check Auth.php, where you can find the algorithm of cashing. The algorithm is next:

1. We have salt.
2. This salt is concatenated with a password and it's calculated as sha256.
3. The resulting hash from the previous step is then concatenated with the IP address of the server and again calculated as sha256.

Well, we got the algorithm, we got the resulting hash, let's just brute force it.

```bash
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
```

The password is `poohbear`. Use it and get the flag.