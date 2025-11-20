#include <cstdio>
#include <hip/hip_runtime.h>

int
main(void)
{
    int count = 0;

    if (hipGetDeviceCount(&count) != hipSuccess || !count)
        return 1;

    for (int i = 0; i < count; i++) {
        hipDeviceProp_t prop;

        if (hipGetDeviceProperties(&prop, i) != hipSuccess)
            continue;

        const char *name = prop.gcnArchName;

        if (!name)
            continue;

        for (; *name && *name != ':'; name++)
            std::putchar(*name);

        std::putchar('\n');
        return 0;
    }
    return 2;
}
