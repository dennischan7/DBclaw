---
source: PostgreSQL 15 Reference
title: 00_Overview
---

PostgreSQL can sometimes exhaust various operating system resource limits, especially when multiple copies of the server are running on the same system, or in very large installations. This section explains the kernel resources used by PostgreSQL and the steps you can take to resolve problems related to kernel resource consumption.

## <span id="page-2-0"></span>**19.4.1. Shared Memory and Semaphores**

PostgreSQL requires the operating system to provide inter-process communication (IPC) features, specifically shared memory and semaphores. Unix-derived systems typically provide "System V" IPC, "POSIX" IPC, or both. Windows has its own implementation of these features and is not discussed here.

By default, PostgreSQL allocates a very small amount of System V shared memory, as well as a much larger amount of anonymous mmap shared memory. Alternatively, a single large System V shared memory region can be used (see [shared\\_memory\\_type\)](#page-37-0). In addition a significant number of semaphores, which can be either System V or POSIX style, are created at server startup. Currently, POSIX semaphores are used on Linux and FreeBSD systems while other platforms use System V semaphores.

System V IPC features are typically constrained by system-wide allocation limits. When PostgreSQL exceeds one of these limits, the server will refuse to start and should leave an instructive error message describing the problem and what to do about it. (See also [Section 19.3.1.](#page-0-0)) The relevant kernel parameters are named consistently across different systems; [Table 19.1](#page-2-1) gives an overview. The methods to set them, however, vary. Suggestions for some platforms are given below.

<span id="page-2-1"></span>**Table 19.1. System V IPC Parameters**

| Name   | Description                                       | Values needed to run one PostgreSQL<br>instance         |
|--------|---------------------------------------------------|---------------------------------------------------------|
| SHMMAX | Maximum size of shared memory seg<br>ment (bytes) | at least 1kB, but the default is usually<br>much higher |

| Name   | Description                                                 | Values needed to run one PostgreSQL<br>instance                                                                                                           |
|--------|-------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------|
| SHMMIN | Minimum size of shared memory seg<br>ment (bytes)           | 1                                                                                                                                                         |
| SHMALL | Total amount of shared memory available<br>(bytes or pages) | same as SHMMAX if bytes, or ceil(SH<br>MMAX/PAGE_SIZE) if pages, plus<br>room for other applications                                                      |
| SHMSEG | Maximum number of shared memory<br>segments per process     | only 1 segment is needed, but the default<br>is much higher                                                                                               |
| SHMMNI | Maximum number of shared memory<br>segments system-wide     | like SHMSEG plus room for other applica<br>tions                                                                                                          |
| SEMMNI | Maximum number of semaphore identi<br>fiers (i.e., sets)    | at least ceil((max_connections<br>+ autovacuum_max_workers +<br>max_wal_senders + max_work<br>er_processes + 6) / 16) plus<br>room for other applications |
| SEMMNS | Maximum number of semaphores sys<br>tem-wide                | ceil((max_connections +<br>autovacuum_max_workers +<br>max_wal_senders + max_work<br>er_processes + 6) / 16) * 17<br>plus room for other applications     |
| SEMMSL | Maximum number of semaphores per set                        | at least 17                                                                                                                                               |
| SEMMAP | Number of entries in semaphore map                          | see text                                                                                                                                                  |
| SEMVMX | Maximum value of semaphore                                  | at least 1000 (The default is often 32767;<br>do not change unless necessary)                                                                             |

PostgreSQL requires a few bytes of System V shared memory (typically 48 bytes, on 64-bit platforms) for each copy of the server. On most modern operating systems, this amount can easily be allocated. However, if you are running many copies of the server or you explicitly configure the server to use large amounts of System V shared memory (see [shared\\_memory\\_type](#page-37-0) and [dynamic\\_shared\\_memo](#page-37-1)[ry\\_type\)](#page-37-1), it may be necessary to increase SHMALL, which is the total amount of System V shared memory system-wide. Note that SHMALL is measured in pages rather than bytes on many systems.

Less likely to cause problems is the minimum size for shared memory segments (SHMMIN), which should be at most approximately 32 bytes for PostgreSQL (it is usually just 1). The maximum number of segments system-wide (SHMMNI) or per-process (SHMSEG) are unlikely to cause a problem unless your system has them set to zero.

When using System V semaphores, PostgreSQL uses one semaphore per allowed connection [\(max\\_connections](#page-27-0)), allowed autovacuum worker process ([autovacuum\\_max\\_workers](#page-81-0)), allowed WAL sender process [\(max\\_wal\\_senders\)](#page-53-0), and allowed background process ([max\\_worker\\_processes\)](#page-41-0), in sets of 16. Each such set will also contain a 17th semaphore which contains a "magic number", to detect collision with semaphore sets used by other applications. The maximum number of semaphores in the system is set by SEMMNS, which consequently must be at least as high as max\_connections plus autovacuum\_max\_workers plus max\_wal\_senders, plus max\_worker\_processes, plus one extra for each 16 allowed connections plus workers (see the formula in [Table 19.1](#page-2-1)). The parameter SEMMNI determines the limit on the number of semaphore sets that can exist on the system at one time. Hence this parameter must be at least ceil((max\_connections + autovacuum\_max\_workers + max\_wal\_senders + max\_worker\_processes + 6) / 16). Lowering the number of allowed connections is a temporary workaround for failures, which are usually confusingly worded "No space left on device", from the function semget.

In some cases it might also be necessary to increase SEMMAP to be at least on the order of SEMMNS. If the system has this parameter (many do not), it defines the size of the semaphore resource map, in which each contiguous block of available semaphores needs an entry. When a semaphore set is freed it is either added to an existing entry that is adjacent to the freed block or it is registered under a new map entry. If the map is full, the freed semaphores get lost (until reboot). Fragmentation of the semaphore space could over time lead to fewer available semaphores than there should be.

Various other settings related to "semaphore undo", such as SEMMNU and SEMUME, do not affect PostgreSQL.

When using POSIX semaphores, the number of semaphores needed is the same as for System V, that is one semaphore per allowed connection ([max\\_connections\)](#page-27-0), allowed autovacuum worker process [\(autovacuum\\_max\\_workers\)](#page-81-0), allowed WAL sender process ([max\\_wal\\_senders](#page-53-0)), and allowed background process ([max\\_worker\\_processes](#page-41-0)). On the platforms where this option is preferred, there is no specific kernel limit on the number of POSIX semaphores.

#### AIX

It should not be necessary to do any special configuration for such parameters as SHMMAX, as it appears this is configured to allow all memory to be used as shared memory. That is the sort of configuration commonly used for other databases such as DB/2.

It might, however, be necessary to modify the global ulimit information in /etc/security/limits, as the default hard limits for file sizes (fsize) and numbers of files (nofiles) might be too low.

#### FreeBSD

The default shared memory settings are usually good enough, unless you have set shared\_memory\_type to sysv. System V semaphores are not used on this platform.

The default IPC settings can be changed using the sysctl or loader interfaces. The following parameters can be set using sysctl:

```
# sysctl kern.ipc.shmall=32768
# sysctl kern.ipc.shmmax=134217728
```

To make these settings persist over reboots, modify /etc/sysctl.conf.

If you have set shared\_memory\_type to sysv, you might also want to configure your kernel to lock System V shared memory into RAM and prevent it from being paged out to swap. This can be accomplished using the sysctl setting kern.ipc.shm\_use\_phys.

If running in a FreeBSD jail, you should set its sysvshm parameter to new, so that it has its own separate System V shared memory namespace. (Before FreeBSD 11.0, it was necessary to enable shared access to the host's IPC namespace from jails, and take measures to avoid collisions.)

#### NetBSD

The default shared memory settings are usually good enough, unless you have set shared\_memory\_type to sysv. You will usually want to increase kern.ipc.semmni and kern.ipc.semmns, as NetBSD's default settings for these are uncomfortably small.

IPC parameters can be adjusted using sysctl, for example:

```
# sysctl -w kern.ipc.semmni=100
```

To make these settings persist over reboots, modify /etc/sysctl.conf.

If you have set shared\_memory\_type to sysv, you might also want to configure your kernel to lock System V shared memory into RAM and prevent it from being paged out to swap. This can be accomplished using the sysctl setting kern.ipc.shm\_use\_phys.

#### OpenBSD

The default shared memory settings are usually good enough, unless you have set shared\_memory\_type to sysv. You will usually want to increase kern.seminfo.semmni and kern.seminfo.semmns, as OpenBSD's default settings for these are uncomfortably small.

IPC parameters can be adjusted using sysctl, for example:

```
# sysctl kern.seminfo.semmni=100
```

To make these settings persist over reboots, modify /etc/sysctl.conf.

#### HP-UX

The default settings tend to suffice for normal installations.

IPC parameters can be set in the System Administration Manager (SAM) under Kernel Configuration → Configurable Parameters. Choose Create A New Kernel when you're done.

#### Linux

The default shared memory settings are usually good enough, unless you have set shared\_memory\_type to sysv, and even then only on older kernel versions that shipped with low defaults. System V semaphores are not used on this platform.

The shared memory size settings can be changed via the sysctl interface. For example, to allow 16 GB:

```
$ sysctl -w kernel.shmmax=17179869184
$ sysctl -w kernel.shmall=4194304
```

To make these settings persist over reboots, see /etc/sysctl.conf.

#### macOS

The default shared memory and semaphore settings are usually good enough, unless you have set shared\_memory\_type to sysv.

The recommended method for configuring shared memory in macOS is to create a file named / etc/sysctl.conf, containing variable assignments such as:

```
kern.sysv.shmmax=4194304
kern.sysv.shmmin=1
kern.sysv.shmmni=32
kern.sysv.shmseg=8
kern.sysv.shmall=1024
```

Note that in some macOS versions, *all five* shared-memory parameters must be set in /etc/ sysctl.conf, else the values will be ignored.

SHMMAX can only be set to a multiple of 4096.

SHMALL is measured in 4 kB pages on this platform.

It is possible to change all but SHMMNI on the fly, using sysctl. But it's still best to set up your preferred values via /etc/sysctl.conf, so that the values will be kept across reboots.

Solaris illumos

> The default shared memory and semaphore settings are usually good enough for most PostgreSQL applications. Solaris defaults to a SHMMAX of one-quarter of system RAM. To further adjust this setting, use a project setting associated with the postgres user. For example, run the following as root:

```
projadd -c "PostgreSQL DB User" -K "project.max-shm-
memory=(privileged,8GB,deny)" -U postgres -G postgres
 user.postgres
```

This command adds the user.postgres project and sets the shared memory maximum for the postgres user to 8GB, and takes effect the next time that user logs in, or when you restart PostgreSQL (not reload). The above assumes that PostgreSQL is run by the postgres user in the postgres group. No server reboot is required.

Other recommended kernel setting changes for database servers which will have a large number of connections are:

```
project.max-shm-ids=(priv,32768,deny)
project.max-sem-ids=(priv,4096,deny)
project.max-msg-ids=(priv,4096,deny)
```

Additionally, if you are running PostgreSQL inside a zone, you may need to raise the zone resource usage limits as well. See "Chapter2: Projects and Tasks" in the *System Administrator's Guide* for more information on projects and prctl.