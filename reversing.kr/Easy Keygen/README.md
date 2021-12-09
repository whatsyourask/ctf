# Easy Keygen

Platform: Reversing.Kr

The code from decompiler:

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  signed int j; // ebp
  int i; // esi
  char xor_values[4]; // [esp+Ch] [ebp-130h]
  char input[100]; // [esp+10h] [ebp-12Ch] BYREF
  char Buffer; // [esp+74h] [ebp-C8h] BYREF
  char v9[196]; // [esp+75h] [ebp-C7h] BYREF
  __int16 v10; // [esp+139h] [ebp-3h]
  char v11; // [esp+13Bh] [ebp-1h]

  input[0] = 0;
  Buffer = 0;
  memset(&input[1], 0, 0x60u);
  *(_WORD *)&input[97] = 0;
  input[99] = 0;
  memset(v9, 0, sizeof(v9));
  v10 = 0;
  v11 = 0;
  xor_values[0] = 16;
  xor_values[1] = 32;
  xor_values[2] = 48;
  printf((int)aInputName);
  scanf("%s", input);
  j = 0;
  for ( i = 0; j < (int)strlen(input); ++i )
  {
    if ( i >= 3 )
      i = 0;
    sprintf(&Buffer, "%s%02X", &Buffer, input[j++] ^ xor_values[i]);
  }
  memset(input, 0, sizeof(input));
  printf((int)aInputSerial);
  scanf("%s", input);
  if ( !strcmp(input, &Buffer) )
    printf((int)"Correct!\n");
  else
    printf((int)"Wrong\n");
  return 0;
}
```

You can clearly see that the keygen is simple. It just xor each character with 3 values 16, 32, 48 and put it in `Buffer` as hex values. Python script to get the valid name:

```python
serial_number = [0x5B, 0x13, 0x49, 0x77, 0x13, 0x5E, 0x7D, 0x13]
i = 0
xor_values = [16, 32, 48]
name = ''
for char in serial_number:
    if i > 2:
        i = 0
    name += chr(char ^ xor_values[i])
    i += 1
print(name)
```

```bash
$ python3 get_name_to_solve.py 
K3yg3nm3
```

```bash
C:\Users\shogun\Downloads\Easy_KeygenMe>".\Easy Keygen.exe"
Input Name: K3yg3nm3
Input Serial: 5B134977135E7D13
Correct!

C:\Users\shogun\Downloads\Easy_KeygenMe>
```