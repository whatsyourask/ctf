#include <unistd.h>

// It's just an example
int main(){
        char *args[2];
        // Execve definition:
        // #include <unistd.h>
        //
        // int execve(const char *pathname, char *const argv[],
        //              char *const envp[];
        args[0] = "/bin/sh";
        args[1] = NULL;
        execve(args[0], args, NULL);
}
