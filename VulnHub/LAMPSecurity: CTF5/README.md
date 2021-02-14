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
* ??? pop3
* [ ] rpcbind
* [ ] netbios
* ??? imap
* ??? 901
* [x] mysql
* ??? 40050

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
