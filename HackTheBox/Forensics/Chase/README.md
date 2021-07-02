# Chase

Completed: Yes
Date: July 2, 2021 → July 2, 2021
Platform: HackTheBox

Open pcap file in Wireshark. If you will trace the HTTP protocol, you will see that the attacker went to `/upload.aspx`. Then he uploaded `cmd.exe`. After that, he uploaded netcat.exe with certutil. He used Netcat to get a reverse shell. Then, he requested file which filename is a flag.

![expert_info.png](expert_info.png)

This is the flag in base32.
