#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#ifdef _WIN32
#include <process.h>
#define execvp _execvp
#else
#include <unistd.h>
#endif

int
main(int argc, char **argv)
{
    char *cmd = strrchr(argv[0], '-');
    char **args = calloc(argc + 2, sizeof(char *));

    if (!args)
        return 1;

    args[0] = "zig";
    args[1] = cmd + 1;

    for (int i = 1; i < argc; i++)
        args[i + 1] = argv[i];

    execvp("zig", args);
    return 1;
}
