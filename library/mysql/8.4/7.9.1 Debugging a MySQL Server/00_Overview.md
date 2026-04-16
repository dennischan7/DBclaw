---
source: MySQL 8.4 Reference
title: 00_Overview
---

If you are using some functionality that is very new in MySQL, you can try to run mysqld with the - skip-new option (which disables all new, potentially unsafe functionality). See Section B.3.3.3, "What to Do If MySQL Keeps Crashing".

If mysqld does not want to start, verify that you have no my.cnf files that interfere with your setup! You can check your my.cnf arguments with mysqld --print-defaults and avoid using them by starting with mysqld --no-defaults ....

If mysqld starts to eat up CPU or memory or if it "hangs," you can use mysqladmin processlist status to find out if someone is executing a query that takes a long time. It may be a good idea to run mysqladmin -i10 processlist status in some window if you are experiencing performance problems or problems when new clients cannot connect.

The command mysqladmin debug dumps some information about locks in use, used memory and query usage to the MySQL log file. This may help solve some problems. This command also provides some useful information even if you have not compiled MySQL for debugging!

If the problem is that some tables are getting slower and slower you should try to optimize the table with OPTIMIZE TABLE or myisamchk. See Chapter 7, MySQL Server Administration. You should also check the slow queries with EXPLAIN.

You should also read the OS-specific section in this manual for problems that may be unique to your environment. See Section 2.1, "General Installation Guidance".

# <span id="page-139-1"></span>**7.9.1.1 Compiling MySQL for Debugging**

If you have some very specific problem, you can always try to debug MySQL. To do this you must configure MySQL with the -DWITH\_DEBUG=1 option. You can check whether MySQL was compiled with debugging by doing: mysqld --help. If the --debug flag is listed with the options then you have debugging enabled. mysqladmin ver also lists the mysqld version as mysql ... --debug in this case.

If mysqld stops crashing when you configure it with the -DWITH\_DEBUG=1 CMake option, you probably have found a compiler bug or a timing bug within MySQL. In this case, you can try to add -g using the CMAKE\_C\_FLAGS and CMAKE\_CXX\_FLAGS CMake options and not use -DWITH\_DEBUG=1. If mysqld dies, you can at least attach to it with gdb or use gdb on the core file to find out what happened.

When you configure MySQL for debugging you automatically enable a lot of extra safety check functions that monitor the health of mysqld. If they find something "unexpected," an entry is written to stderr, which mysqld\_safe directs to the error log! This also means that if you are having some unexpected problems with MySQL and are using a source distribution, the first thing you should do is to configure MySQL for debugging. If you believe that you have found a bug, please use the instructions at Section 1.6, "How to Report Bugs or Problems".

In the Windows MySQL distribution, mysqld.exe is by default compiled with support for trace files.

# <span id="page-140-0"></span>**7.9.1.2 Creating Trace Files**

If the mysqld server does not start or it crashes easily, you can try to create a trace file to find the problem.

To do this, you must have a mysqld that has been compiled with debugging support. You can check this by executing mysqld -V. If the version number ends with -debug, it is compiled with support for trace files. (On Windows, the debugging server is named mysqld-debug rather than mysqld.)

Start the mysqld server with a trace log in /tmp/mysqld.trace on Unix or \mysqld.trace on Windows:

```
$> mysqld --debug
```

On Windows, you should also use the --standalone flag to not start mysqld as a service. In a console window, use this command:

```
C:\> mysqld-debug --debug --standalone
```

After this, you can use the mysql.exe command-line tool in a second console window to reproduce the problem. You can stop the mysqld server with mysqladmin shutdown.

The trace file can become **very large**! To generate a smaller trace file, you can use debugging options something like this:

```
mysqld --debug=d,info,error,query,general,where:O,/tmp/mysqld.trace
```

This only prints information with the most interesting tags to the trace file.

If you file a bug, please add only those lines from the trace file to the bug report that indicate where something seems to go wrong. If you cannot locate the wrong place, open a bug report and upload the whole trace file to the report, so that a MySQL developer can take a look at it. For instructions, see Section 1.6, "How to Report Bugs or Problems".

The trace file is made with the DBUG package by Fred Fish. See [Section 7.9.4, "The DBUG Package".](#page-150-0)