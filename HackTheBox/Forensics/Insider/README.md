# Insider

Completed: Yes
Date: July 2, 2021 → July 2, 2021
Platform: HackTheBox

In the beginning, I just searched some token or something in files. Also, I opened SQLite files in DB viewer, but it gives me nothing. I tried to decode some cookies and so on from classic base64 because it was similar to it.

Then, I googled how to do forensics for Mozilla firefox and found this tool which will decode all stuff from the profile folder - [https://github.com/Unode/firefox_decrypt](https://github.com/Unode/firefox_decrypt). To use it, you need to specify the path to one of the profiles.

```bash
~/tools/firefox_decrypt/firefox_decrypt.py ~/Downloads/Mozilla/Firefox/Profiles/2542z9mo.default-release 
2021-07-02 11:29:38,712 - WARNING - profile.ini not found in /home/kali/Downloads/Mozilla/Firefox/Profiles/2542z9mo.default-release
2021-07-02 11:29:38,712 - WARNING - Continuing and assuming '/home/kali/Downloads/Mozilla/Firefox/Profiles/2542z9mo.default-release' is a profile location

Website:   http://acc01:8080
Username: 'admin'
Password: 'HTB{****}'
```