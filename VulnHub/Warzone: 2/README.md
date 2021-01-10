# Warzone: 2

[Machine](https://www.vulnhub.com/entry/warzone-2,598/ "https://www.vulnhub.com/entry/warzone-2,598/")

## Reconnaissance

### nmap

#### Ports scanning:
```
nmap -sS -T4 -p- 192.168.88.224 -oA ports
```
#### Services scanning:
```
nmap -sV -O -p21,22,1337 192.168.88.224 -oA services
```
### ftp

Anonymous login is allowed.

![ftp](screenshots/ftp.png)

From there we have a three pictures.

username:

![username](ftp/username.PNG)

password:

![password](ftp/password.PNG)

token:

![token](ftp/token.PNG)

I searched for cipher on the username and password pictures. And i got [flag semaphore](https://en.wikipedia.org/wiki/Flag_semaphore "https://en.wikipedia.org/wiki/Flag_semaphore").

Decode the symbols from pictures and get a username and a password in `creds/`. I wrote it in upper case as wiki says.

### port 1337

1337 port seems to be a custom application.

I tried to take a banner:

![1337 conn](screenshots/1337_banner.png)

## Threat modelling

I think that it is enough to gather. Now we have the creds and have the 1337 port with login. I believe we easily will get remote access and that's all. 

By the way, need to write a script to create the token!

## Vulnerability analysis

### vsftpd

Not vulnerable.

### ssh

Not vulnerable.

### Misconfiguration of ftp

The main vulnerability is this. But i don't know about backend of 1337 port. Maybe here we can also have binary vulnerabilities.

## Exploitation

## Post exploitation

## Sources

### Flag semaphore

[wiki](https://en.wikipedia.org/wiki/Flag_semaphore "https://en.wikipedia.org/wiki/Flag_semaphore")
