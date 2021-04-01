#include <stdio.h>


// gcc -fPIC -m32 -ldl -shared preload_puts.c -o preload_puts.so
// LD_PRELOAD="./preload_puts.c" ./utumno0
int puts(const char *s){
    printf("I read you!");
    return 0;
}

