---
source: MySQL 5.7 Reference
title: 00_Overview
---

This section describes some utilities that you may find useful when developing MySQL programs.

In shell scripts, you can use the [my\\_print\\_defaults](#page-21-0) program to parse option files and see what options would be used by a given program. The following example shows the output that [my\\_print\\_defaults](#page-21-0) might produce when asked to show the options found in the [client] and [mysql] groups:

```
$> my_print_defaults client mysql
--port=3306
--socket=/tmp/mysql.sock
--no-auto-rehash
```

Note for developers: Option file handling is implemented in the C client library simply by processing all options in the appropriate group or groups before any command-line arguments. This works well for programs that use the last instance of an option that is specified multiple times. If you have a C or C++ program that handles multiply specified options this way but that does not read option files, you need add only two lines to give it that capability. Check the source code of any of the standard MySQL clients to see how to do this.

Several other language interfaces to MySQL are based on the C client library, and some of them provide a way to access option file contents. These include Perl and Python. For details, see the documentation for your preferred interface.

# <span id="page-19-3"></span>**4.7.1 mysql\_config — Display Options for Compiling Clients**

[mysql\\_config](#page-19-3) provides you with useful information for compiling your MySQL client and connecting it to MySQL. It is a shell script, so it is available only on Unix and Unix-like systems.

![](_page_20_Picture_1.jpeg)

#### **Note**

As of MySQL 5.7.9, pkg-config can be used as an alternative to [mysql\\_config](#page-19-3) for obtaining information such as compiler flags or link libraries required to compile MySQL applications. For more information, see [Building C](https://dev.mysql.com/doc/c-api/5.7/en/c-api-building-clients-pkg-config.md) [API Client Programs Using pkg-config](https://dev.mysql.com/doc/c-api/5.7/en/c-api-building-clients-pkg-config.md).

![](_page_20_Picture_4.jpeg)

#### **Note**

As of MySQL 5.7.4, for binary distributions for Solaris, [mysql\\_config](#page-19-3) does not provide arguments for linking with the embedded library. To get linking arguments for the embedded library, use the mysql\_server\_config script instead.

[mysql\\_config](#page-19-3) supports the following options.

<span id="page-20-0"></span>• [--cflags](#page-20-0)

C Compiler flags to find include files and critical compiler flags and defines used when compiling the libmysqlclient library. The options returned are tied to the specific compiler that was used when the library was created and might clash with the settings for your own compiler. Use [--include](#page-20-1) for more portable options that contain only include paths.

<span id="page-20-2"></span>• [--cxxflags](#page-20-2)

Like [--cflags](#page-20-0), but for C++ compiler flags.

<span id="page-20-1"></span>• [--include](#page-20-1)

Compiler options to find MySQL include files.

<span id="page-20-3"></span>• [--libmysqld-libs](#page-20-3), [--embedded-libs](#page-20-3), [--embedded](#page-20-3)

Libraries and options required to link with libmysqld, the MySQL embedded server.

![](_page_20_Picture_16.jpeg)

# **Note**

The libmysqld embedded server library is deprecated as of MySQL 5.7.19 and has been removed in MySQL 8.0.

<span id="page-20-4"></span>• [--libs](#page-20-4)

Libraries and options required to link with the MySQL client library.

<span id="page-20-5"></span>• [--libs\\_r](#page-20-5)

Libraries and options required to link with the thread-safe MySQL client library. In MySQL 5.7, all client libraries are thread-safe, so this option need not be used. The [--libs](#page-20-4) option can be used in all cases.

<span id="page-20-6"></span>• [--plugindir](#page-20-6)

The default plugin directory path name, defined when configuring MySQL.

<span id="page-20-7"></span>• [--port](#page-20-7)

The default TCP/IP port number, defined when configuring MySQL.

<span id="page-20-8"></span>• [--socket](#page-20-8)

The default Unix socket file, defined when configuring MySQL.

<span id="page-20-9"></span>• [--variable=](#page-20-9)var\_name

Display the value of the named configuration variable. Permitted var\_name values are pkgincludedir (the header file directory), pkglibdir (the library directory), and plugindir (the plugin directory).

<span id="page-21-1"></span>• [--version](#page-21-1)

Version number for the MySQL distribution.

If you invoke [mysql\\_config](#page-19-3) with no options, it displays a list of all options that it supports, and their values:

```
$> mysql_config
Usage: /usr/local/mysql/bin/mysql_config [options]
Options:
 --cflags [-I/usr/local/mysql/include/mysql -mcpu=pentiumpro]
 --cxxflags [-I/usr/local/mysql/include/mysql -mcpu=pentiumpro]
 --include [-I/usr/local/mysql/include/mysql]
 --libs [-L/usr/local/mysql/lib/mysql -lmysqlclient
 -lpthread -lm -lrt -lssl -lcrypto -ldl]
 --libs_r [-L/usr/local/mysql/lib/mysql -lmysqlclient_r
 -lpthread -lm -lrt -lssl -lcrypto -ldl]
 --plugindir [/usr/local/mysql/lib/plugin]
 --socket [/tmp/mysql.sock]
 --port [3306]
 --version [5.7.9]
 --libmysqld-libs [-L/usr/local/mysql/lib/mysql -lmysqld
 -lpthread -lm -lrt -lssl -lcrypto -ldl -lcrypt]
 --variable=VAR VAR is one of:
 pkgincludedir [/usr/local/mysql/include]
 pkglibdir [/usr/local/mysql/lib]
 plugindir [/usr/local/mysql/lib/plugin]
```

You can use [mysql\\_config](#page-19-3) within a command line using backticks to include the output that it produces for particular options. For example, to compile and link a MySQL client program, use [mysql\\_config](#page-19-3) as follows:

```
gcc -c `mysql_config --cflags` progname.c
gcc -o progname progname.o `mysql_config --libs`
```

# <span id="page-21-0"></span>**4.7.2 my\_print\_defaults — Display Options from Option Files**

[my\\_print\\_defaults](#page-21-0) displays the options that are present in option groups of option files. The output indicates what options are used by programs that read the specified option groups. For example, the mysqlcheck program reads the [mysqlcheck] and [client] option groups. To see what options are present in those groups in the standard option files, invoke [my\\_print\\_defaults](#page-21-0) like this:

```
$> my_print_defaults mysqlcheck client
--user=myusername
--password=password
--host=localhost
```

The output consists of options, one per line, in the form that they would be specified on the command line.

[my\\_print\\_defaults](#page-21-0) supports the following options.

<span id="page-21-2"></span>• [--help](#page-21-2), -?

Display a help message and exit.

<span id="page-21-3"></span>• [--config-file=](#page-21-3)file\_name, [--defaults-file=](#page-21-3)file\_name, -c file\_name

Read only the given option file.

<span id="page-21-4"></span>• --debug=[debug\\_options](#page-21-4), -# debug\_options

Write a debugging log. A typical debug\_options string is d:t:o,file\_name. The default is d:t:o,/tmp/my\_print\_defaults.trace.

<span id="page-22-0"></span>• [--defaults-extra-file=](#page-22-0)file\_name, [--extra-file=](#page-22-0)file\_name, -e file\_name

Read this option file after the global option file but (on Unix) before the user option file.

For additional information about this and other option-file options, see Section 4.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-22-1"></span>• [--defaults-group-suffix=](#page-22-1)suffix, -g suffix

In addition to the groups named on the command line, read groups that have the given suffix.

For additional information about this and other option-file options, see Section 4.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-22-2"></span>• [--login-path=](#page-22-2)name, -l name

Read options from the named login path in the .mylogin.cnf login path file. A "login path" is an option group containing options that specify which MySQL server to connect to and which account to authenticate as. To create or modify a login path file, use the mysql\_config\_editor utility. See Section 4.6.6, "mysql\_config\_editor — MySQL Configuration Utility".

For additional information about this and other option-file options, see Section 4.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-22-3"></span>• [--no-defaults](#page-22-3), -n

Return an empty string.

For additional information about this and other option-file options, see Section 4.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-22-4"></span>• [--show](#page-22-4), -s

As of MySQL 5.7.8, [my\\_print\\_defaults](#page-21-0) masks passwords by default. Use this option to display passwords in cleartext.

<span id="page-22-5"></span>• [--verbose](#page-22-5), -v

Verbose mode. Print more information about what the program does.

• [--version](#page-22-6), -V

Display version information and exit.

# <span id="page-22-7"></span><span id="page-22-6"></span>**4.7.3 resolve\_stack\_dump — Resolve Numeric Stack Trace Dump to Symbols**

[resolve\\_stack\\_dump](#page-22-7) resolves a numeric stack dump to symbols.

![](_page_22_Picture_22.jpeg)

# **Note**

[resolve\\_stack\\_dump](#page-22-7) is deprecated and is removed in MySQL 8.0. Stack traces from official MySQL builds are always symbolized, so there is no need to use [resolve\\_stack\\_dump](#page-22-7).

Invoke [resolve\\_stack\\_dump](#page-22-7) like this:

resolve\_stack\_dump [options] symbols\_file [numeric\_dump\_file]

The symbols file should include the output from the nm --numeric-sort mysqld command. The numeric dump file should contain a numeric stack track from mysqld. If no numeric dump file is named on the command line, the stack trace is read from the standard input.

[resolve\\_stack\\_dump](#page-22-7) supports the following options.

<span id="page-23-0"></span>• [--help](#page-23-0), -h

Display a help message and exit.

<span id="page-23-1"></span>• [--numeric-dump-file=](#page-23-1)file\_name, -n file\_name

Read the stack trace from the given file.

<span id="page-23-2"></span>• [--symbols-file=](#page-23-2)file\_name, -s file\_name

Use the given symbols file.

<span id="page-23-3"></span>• [--version](#page-23-3), -V

Display version information and exit.

For more information, see Section 5.8.1.5, "Using a Stack Trace".