With DB browser on kali i easy got the count of entries. 376.

Also easy to got the count of bcrypt passwords. 21.

But with second task i had a problem cause i'm bad in sql. So i just typed the simple query that take all passwords and export them to the CSV file.

Next i wrote a python script.

`#!/usr/bin/env python3
import sys


passwords = open(sys.argv[1], 'r').read().split('\n')
for password in passwords:
    if passwords.count(password) > 1:
        print(f' [!] REPEATED PASSWORD WAS FOUND: {password}')
        break`

`root@kali:~/Downloads# ./count.py entries
 [!] REPEATED PASSWORD WAS FOUND: mah6geiVoo`

So the answer was 376_mah6geiVoo_21.
