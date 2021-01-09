# Warzone: 1

[Machine](https://www.vulnhub.com/entry/warzone-1,589/ "https://www.vulnhub.com/entry/warzone-1,589/")

## Reconnaissance

### nmap

#### Ports scanning:
```
nmap -sS -T4 -p- 192.168.88.226 -oA ports
```
#### Services scanning:
```
nmap -sV -O -T4 -p21,22,5000 192.168.88.226 -oA services
```
### ftp

On ftp we have an anonymous login. Also we can download all files in pub directory.
There are one note.txt and one jar file. Note says that jar file is used to encrypt password.
```
jar xf warzone-encrypt.jar
```
After extraction:

crypto/
	AES.class
encrypt/
	Main.class
Other/
	Obfuscated.class 

I used java decompiler to get source code.

In Main it just encrypts the password with AES from AES source. But AES has interesting methods...

![aes](screenshots/aes.png)

Obfuscated:

![obfuscated](screenshots/obfuscated.png)

Thus, secrets are not secrets anymore :)

We can easy decrypt the passwords, but need some java coding, just a little.

By the way, what passwords need to be decrypted???

## Thread modelling

## Vulnerability analysis

## Exploitation

## Post exploitation
