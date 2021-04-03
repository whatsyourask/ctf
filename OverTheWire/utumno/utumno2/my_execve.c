#include <unistd.h>

void main(){
    char *envp[] = {};
    execve('/utumno/utumno2', NULL, envp);
}

