#include<stdlib.h>
#include<unistd.h>

int main(int argc, char* argv[]){
    printf("%s, %p\n", argv[1], getenv(argv[1]));
}
