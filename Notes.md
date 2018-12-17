# cx_Freeze trim unused libs

```bash
$ LD_LIBRARY_PATH=./lib strace ./run 2> trace
$ grep 'openat(AT_FDCWD, "/home/yelkhadiri/DEVEL/ldjam-43/build/Ulis43-linux/lib/' trace_openat | cut -f9 -d/ | cut -f1 -d\" > trace_openat_lib
$ sort -u trace_openat_lib > used_libs
$ comm -23 <(ls lib) used_libs
```
