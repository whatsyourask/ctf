# Easy ELF

Platform: Reversing.Kr

Decompile of main function:

```c
int __cdecl main()
{
  write(1, "Reversing.Kr Easy ELF\n\n", 23u);
  get_input();
  if ( check_something() )
    write_correct();
  else
    write(1, "Wrong\n", 6u);
  return 0;
}
```

get_input() is just a function to do a scanf and get the input from a user. 

check_something():

```c
_BOOL4 check_something()
{
  if ( second != 49 )
    return 0;
  input ^= 52u;
  third ^= 50u;
  fourth ^= 136u;
  if ( fifth_0 != 88 )
    return 0;
  if ( sixth )
    return 0;
  if ( third != 124 )
    return 0;
  if ( input == 120 )
    return fourth == (char)0xFFFFFFDD;
  return 0;
}
```

So, the function is simple:

- The second char must be equal to 49.
- input which is the first char must be equal to 120, but after it will be XORed with 52.
- The third one must be equal to 124, after XOR with 50.
- The fourth must be equal to 0xffffffdd after XOR with 136.
- The fifth must be equal to 88.
- The sixth must not exist.

Thus, we can determine that it is a word `L1NUX`.