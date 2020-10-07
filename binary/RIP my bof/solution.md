Put some input to the program:

![begin](screenshots/begin.png)

We can see that now we need to overflow the buffer and overwrite the ret address on the stack.
Source code:

![source](screenshots/source.png)

Find the address of `win` with `objdump -d server`:

![address](screenshots/address.png)

Now just overflow the buffer and rewrite the ret address to that address:

![rewrite](screenshots/rewrite.png)
