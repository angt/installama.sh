#define _POSIX_C_SOURCE 200809L

#include <errno.h>
#include <float.h>
#include <math.h>
#include <pthread.h>
#include <stdint.h>
#include <string.h>
#include <wchar.h>

void *
mempcpy(void *dst, const void *src, size_t n)
{
    return (char *)memcpy(dst, src, n) + n;
}

char *
strtok_r(char *str, const char *delim, char **save)
{
    if (!str)
        str = *save;

    if (!str)
        return NULL;

    str += strspn(str, delim);

    if (*str == '\0') {
        *save = NULL;
        return NULL;
    }
    char *tok = str;
    str = strpbrk(tok, delim);

    if (str)
        *str++ = '\0';

    *save = str;
    return tok;
}

int
pthread_spin_init(pthread_spinlock_t *l, int pshared)
{
    (void)pshared;
    *l = 0;
    return 0;
}

int
pthread_spin_destroy(pthread_spinlock_t *l)
{
    (void)l;
    return 0;
}

int
pthread_spin_lock(pthread_spinlock_t *l)
{
    while (__atomic_test_and_set(l, __ATOMIC_ACQUIRE)) {
        #if defined(__x86_64__) || defined(__i386__)
        __builtin_ia32_pause();
        #endif
    }
    return 0;
}

int
pthread_spin_trylock(pthread_spinlock_t *l)
{
    return __atomic_test_and_set(l, __ATOMIC_ACQUIRE) ? EBUSY : 0;
}

int
pthread_spin_unlock(pthread_spinlock_t *l)
{
    __atomic_clear(l, __ATOMIC_RELEASE);
    return 0;
}

wchar_t *
wmemchr(const wchar_t *s, wchar_t c, size_t n)
{
    for (size_t i = 0; i < n; i++) {
        if (s[i] == c)
            return (wchar_t *)&s[i];
    }
    return NULL;
}

int
wmemcmp(const wchar_t *s1, const wchar_t *s2, size_t n)
{
    for (size_t i = 0; i < n; i++) {
        if (s1[i] != s2[i])
            return s1[i] < s2[i] ? -1 : 1;
    }
    return 0;
}

wchar_t *
wmemcpy(wchar_t *dst, const wchar_t *src, size_t n)
{
    return memcpy(dst, src, n * sizeof(wchar_t));
}

wchar_t *
wmempcpy(wchar_t *dst, const wchar_t *src, size_t n)
{
    return wmemcpy(dst, src, n) + n;
}

wchar_t *
wmemmove(wchar_t *dst, const wchar_t *src, size_t n)
{
    return memmove(dst, src, n * sizeof(wchar_t));
}

wchar_t *
wmemset(wchar_t *s, wchar_t c, size_t n)
{
    for (size_t i = 0; i < n; i++) {
        s[i] = c;
    }
    return s;
}

#undef frexpf
#undef frexpl
#undef modfl
#undef hypotf
#undef hypotl
#undef atanl
#undef copysignl
#undef fdiml
#undef nanl
#undef rintl
#undef lrintl

float
frexpf(float x, int *exp)
{
    return (float)frexp((double)x, exp);
}

long double
frexpl(long double x, int *exp)
{
    return (long double)frexp((double)x, exp);
}

long double
modfl(long double x, long double *iptr)
{
    double di;
    long double f = (long double)modf((double)x, &di);
    *iptr = di;
    return f;
}

float
hypotf(float x, float y)
{
    return (float)hypot((double)x, (double)y);
}

long double
hypotl(long double x, long double y)
{
    return (long double)hypot((double)x, (double)y);
}

long double
atanl(long double x)
{
    return (long double)atan((double)x);
}

long double
copysignl(long double x, long double y)
{
    return (long double)copysign((double)x, (double)y);
}

long double
fdiml(long double x, long double y)
{
    return (long double)fdim((double)x, (double)y);
}

long double
nanl(const char *s)
{
    return (long double)nan(s);
}

long double
rintl(long double x)
{
    return (long double)rint((double)x);
}

long
lrintl(long double x)
{
    return lrint((double)x);
}

#undef isnan
#undef __isnan
#undef isnanf
#undef __isnanf
#undef isnanl
#undef __isnanl

int
isnan(double x)
{
    return __builtin_isnan(x);
}

int
__isnan(double x)
{
    return __builtin_isnan(x);
}

int
isnanf(float x)
{
    return __builtin_isnan(x);
}

int
__isnanf(float x)
{
    return __builtin_isnan(x);
}

int
isnanl(long double x)
{
    return __builtin_isnan(x);
}

int
__isnanl(long double x)
{
    return __builtin_isnan(x);
}

double __DENORM  = 0x1p-1074;
double __INF     = __builtin_inf();
double __QNAN    = __builtin_nan("");
double __SNAN    = __builtin_nans("");

float __DENORMF = 0x1p-149f;
float __INFF    = __builtin_inff();
float __QNANF   = __builtin_nanf("");
float __SNANF   = __builtin_nansf("");

long double __DENORML = 0x1p-1074L;
long double __INFL    = __builtin_infl();
long double __QNANL   = __builtin_nanl("");
long double __SNANL   = __builtin_nansl("");
