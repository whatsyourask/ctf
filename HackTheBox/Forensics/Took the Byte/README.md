# Took the byte

Completed: Yes
Date: July 2, 2021 → July 2, 2021
Platform: HackTheBox

Trying to read the file:

```bash
cat password      
����������(c��������������������������ы������$���j���
���
   ��U�3��6�3�U▒�������7���������������������(c���7���������������������[~������������ы������$���j�������������������������
```

Trying to find something in hex:

```bash
cat password| xxd 
00000000: afb4 fcfb ebff f7ff f7ff 2863 aab1 ffff  ..........(c....
00000010: ffff ffff ffff ffff ffff f3ff efff 8f9e  ................
00000020: 8c8c 8890 8d9b d18b 878b aaa7 f3ff 24bb  ..............$.
00000030: 90a3 6abb 90a3 0afe ebff 0cf7 8e55 c9cd  ..j..........U..
00000040: 8833 8d8c 36d1 33cb d308 551a fdff afb4  .3..6.3...U.....
00000050: f8f7 b237 01c1 ebff ffff edff ffff afb4  ...7............
00000060: fefd eafc ebff f7ff f7ff 2863 aab1 b237  ..........(c...7
00000070: 01c1 ebff ffff edff ffff f3ff f3ff ffff  ................
00000080: ffff ffff ffbf 5b7e ffff ffff 8f9e 8c8c  ......[~........
00000090: 8890 8d9b d18b 878b aaa7 f7ff 24bb 90a3  ............$...
000000a0: 6abb 90a3 afb4 faf9 ffff ffff feff feff  j...............
000000b0: b9ff ffff a1ff ffff ffff                 ..........
```

Nothing. The challenge says that someone stole the byte. Let's try to add or xor something with `CyberChef`: [https://0x1.gitlab.io/code/CyberChef/](https://0x1.gitlab.io/code/CyberChef/).

I used XOR Brute force and found this:

```bash
Key = ff: PK........×.UN................password.txtUX..ÛDo\.Do\õ...ó.qª62wÌrsÉ.Ì4,÷ªå..PK..MÈþ>........PK....
```

Then, just need to apply this key and xor the entire file. Save the file and see what the format it has:

```bash
file download.dat                                                                                                                                 
download.dat: Zip archive data, at least v2.0 to extract
```

Use `unzip` in linux or `unzip` in `CyberChef`.