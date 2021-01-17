# Warzone: 3

[Machine](https://www.vulnhub.com/entry/warzone-3-exogen,606/ "https://www.vulnhub.com/entry/warzone-3-exogen,606/")

## Reconnaissance

### nmap

* 21 - ftp
* 22 - ssh
* 4444 - kerberos...?

### ftp

Anonymous access is allowed.

* note.txt
* alienclient.jar

#### Credentials

from note.txt we got:

username:	alienum@exogenesis
password:	sha256(username)

To get a password execute next in python3 interpreter:
```
import hashlib

hashlib.sha256(b'alienum@exogenesis').hexdigest()
```

Also, we have a client app:

![app](screenshots/app.png)

### kerberos

I don't know what to gather from it. Moreover, i don't want to use metasploit.

## Threat modeling

Definitly, here the attack vector is `alienclient.jar` file which we can decompile and use it with the right credential.

## Vulnerability analysis

Again, here is information leakage through misconfiguration of ftp.
