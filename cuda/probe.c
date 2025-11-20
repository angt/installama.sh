#include <stdio.h>
#include <cuda_runtime.h>

#ifndef PROBE_ARCH
#error "Please define PROBE_ARCH"
#endif

int
main(void)
{
    int arch[] = { PROBE_ARCH };
    int n_arch = sizeof(arch) / sizeof(arch[0]);

    struct {
        int runtime;
        int driver;
    } version;

    if (cudaRuntimeGetVersion(&version.runtime) != cudaSuccess)
        return 1;

    if (cudaDriverGetVersion(&version.driver) != cudaSuccess)
        return 2;

    if (version.driver < version.runtime)
        return 3;

    int count = 0;

    if (cudaGetDeviceCount(&count) != cudaSuccess || !count)
        return 4;

    int best_arch = 0;

    for (int i = 0; i < count; i++) {
        struct cudaDeviceProp prop;

        if (cudaGetDeviceProperties(&prop, i) != cudaSuccess)
            continue;

        int device_arch = prop.major * 10 + prop.minor;

        for (int j = 0; j < n_arch; j++) {
            if (arch[j] <= device_arch && arch[j] > best_arch)
                best_arch = arch[j];
        }
    }
    if (!best_arch)
        return 5;

    printf("%d\n", best_arch);
    return 0;
}
