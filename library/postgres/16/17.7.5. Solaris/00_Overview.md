---
source: PostgreSQL 16 Reference
title: 00_Overview
---

PostgreSQL is well-supported on Solaris. The more up to date your operating system, the fewer issues you will experience.

### **17.7.5.1. Required Tools**

You can build with either GCC or Sun's compiler suite. For better code optimization, Sun's compiler is strongly recommended on the SPARC architecture. If you are using Sun's compiler, be careful not to select /usr/ucb/cc; use /opt/SUNWspro/bin/cc.

You can download Sun Studio from [https://www.oracle.com/technetwork/server-storage/solarisstu](https://www.oracle.com/technetwork/server-storage/solarisstudio/downloads/)[dio/downloads/.](https://www.oracle.com/technetwork/server-storage/solarisstudio/downloads/) Many GNU tools are integrated into Solaris 10, or they are present on the Solaris companion CD. If you need packages for older versions of Solaris, you can find these tools at [http://](http://www.sunfreeware.com) [www.sunfreeware.com.](http://www.sunfreeware.com) If you prefer sources, look at [https://www.gnu.org/prep/ftp.](https://www.gnu.org/prep/ftp)

### **17.7.5.2. configure Complains About a Failed Test Program**

If configure complains about a failed test program, this is probably a case of the run-time linker being unable to find some library, probably libz, libreadline or some other non-standard library such as libssl. To point it to the right location, set the LDFLAGS environment variable on the configure command line, e.g.,

```
configure ... LDFLAGS="-R /usr/sfw/lib:/opt/sfw/lib:/usr/local/lib"
```

See the ld man page for more information.

### **17.7.5.3. Compiling for Optimal Performance**

On the SPARC architecture, Sun Studio is strongly recommended for compilation. Try using the -xO5 optimization flag to generate significantly faster binaries. Do not use any flags that modify behavior of floating-point operations and errno processing (e.g., -fast).

If you do not have a reason to use 64-bit binaries on SPARC, prefer the 32-bit version. The 64-bit operations are slower and 64-bit binaries are slower than the 32-bit variants. On the other hand, 32 bit code on the AMD64 CPU family is not native, so 32-bit code is significantly slower on that CPU family.

### **17.7.5.4. Using DTrace for Tracing PostgreSQL**

Yes, using DTrace is possible. See Section 28.5 for further information.

If you see the linking of the postgres executable abort with an error message like:

```
Undefined first referenced
 symbol in file
AbortTransaction utils/probes.o
CommitTransaction utils/probes.o
ld: fatal: Symbol referencing errors. No output written to postgres
collect2: ld returned 1 exit status
make: *** [postgres] Error 1
```

your DTrace installation is too old to handle probes in static functions. You need Solaris 10u4 or newer to use DTrace.

# <span id="page-7-0"></span>**Chapter 18. Installation from Source Code on Windows**

It is recommended that most users download the binary distribution for Windows, available as a graphical installer package from the PostgreSQL website at [https://www.postgresql.org/download/.](https://www.postgresql.org/download/) Building from source is only intended for people developing PostgreSQL or extensions.

There are several different ways of building PostgreSQL on Windows. The simplest way to build with Microsoft tools is to install Visual Studio 2022 and use the included compiler. It is also possible to build with the full Microsoft Visual C++ 2015 to 2022. In some cases that requires the installation of the Windows SDK in addition to the compiler.

It is also possible to build PostgreSQL using the GNU compiler tools provided by MinGW, or using Cygwin for older versions of Windows.

Building using MinGW or Cygwin uses the normal build system, see Chapter 17 and the specific notes in [Section 17.7.4](#page-5-0) and [Section 17.7.2](#page-3-0). To produce native 64 bit binaries in these environments, use the tools from MinGW-w64. These tools can also be used to cross-compile for 32 bit and 64 bit Windows targets on other hosts, such as Linux and macOS. Cygwin is not recommended for running a production server, and it should only be used for running on older versions of Windows where the native build does not work. The official binaries are built using Visual Studio.

Native builds of psql don't support command line editing. The Cygwin build does support command line editing, so it should be used where psql is needed for interactive use on Windows.