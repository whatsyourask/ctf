#include <stdio.h>


// gcc -fPIC -m32 -ldl -shared preload_puts.c -o preload_puts.so
int puts(const char *s){
    printf("%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n"); 
    return 0;
}

