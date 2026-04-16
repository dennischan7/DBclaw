---
source: MySQL 5.7 Reference
title: 00_Overview
---

# <span id="page-23-4"></span>**4.8.1 lz4\_decompress — Decompress mysqlpump LZ4-Compressed Output**

The [lz4\\_decompress](#page-23-4) utility decompresses mysqlpump output that was created using LZ4 compression. [lz4\\_decompress](#page-23-4) was added in MySQL 5.7.10.

Invoke [lz4\\_decompress](#page-23-4) like this:

```
lz4_decompress input_file output_file
```

#### Example:

```
mysqlpump --compress-output=LZ4 > dump.lz4
lz4_decompress dump.lz4 dump.txt
```

To see a help message, invoke [lz4\\_decompress](#page-23-4) with no arguments.

To decompress mysqlpump ZLIB-compressed output, use [zlib\\_decompress](#page-25-0). See [Section 4.8.5,](#page-25-0) ["zlib\\_decompress — Decompress mysqlpump ZLIB-Compressed Output".](#page-25-0)

# <span id="page-23-5"></span>**4.8.2 perror — Display MySQL Error Message Information**

For most system errors, MySQL displays, in addition to an internal text message, the system error code in one of the following styles:

```
message ... (errno: #)
message ... (Errcode: #)
```

You can find out what the error code means by examining the documentation for your system or by using the [perror](#page-23-5) utility.

[perror](#page-23-5) prints a description for a system error code or for a storage engine (table handler) error code.

Invoke [perror](#page-23-5) like this:

```
perror [options] errorcode ...
```

Examples:

```
$> perror 1231
MySQL error code 1231 (ER_WRONG_VALUE_FOR_VAR): Variable '%-.64s' can't
be set to the value of '%-.200s'
$> perror 13 64
```

To obtain the error message for a MySQL Cluster error code, use the ndb\_perror utility.

The meaning of system error messages may be dependent on your operating system. A given error code may mean different things on different operating systems.

[perror](#page-23-5) supports the following options.

OS error code 13: Permission denied

OS error code 64: Machine is not on the network

<span id="page-24-0"></span>• [--help](#page-24-0), [--info](#page-24-0), -I, -?

Display a help message and exit.

<span id="page-24-1"></span>• [--ndb](#page-24-1)

Print the error message for an NDB Cluster error code.

This option is deprecated in NDB 7.6.4 and later, where [perror](#page-23-5) prints a warning if it is used, and is removed in NDB Cluster 8.0. Use the ndb\_perror utility instead.

<span id="page-24-2"></span>• [--silent](#page-24-2), -s

Silent mode. Print only the error message.

<span id="page-24-3"></span>• [--verbose](#page-24-3), -v

Verbose mode. Print error code and message. This is the default behavior.

• [--version](#page-24-4), -V

Display version information and exit.

# <span id="page-24-5"></span><span id="page-24-4"></span>**4.8.3 replace — A String-Replacement Utility**

The [replace](#page-24-5) utility program changes strings in place in files or on the standard input.

![](_page_24_Picture_18.jpeg)

#### **Note**

The [replace](#page-24-5) utility is deprecated as of MySQL 5.7.18 and is removed in MySQL 8.0.

Invoke [replace](#page-24-5) in one of the following ways:

```
replace from to [from to] ... -- file_name [file_name] ...
replace from to [from to] ... < file_name
```

from represents a string to look for and to represents its replacement. There can be one or more pairs of strings.

Use the -- option to indicate where the string-replacement list ends and the file names begin. In this case, any file named on the command line is modified in place, so you may want to make a copy of the original before converting it. replace prints a message indicating which of the input files it actually modifies.

If the -- option is not given, [replace](#page-24-5) reads the standard input and writes to the standard output.

[replace](#page-24-5) uses a finite state machine to match longer strings first. It can be used to swap strings. For example, the following command swaps a and b in the given files, file1 and file2:

replace a b b a -- file1 file2 ...

[replace](#page-24-5) supports the following options.

• -?, -I

Display a help message and exit.

• -#debug\_options

Enable debugging.

• -s

Silent mode. Print less information what the program does.

• -v

Verbose mode. Print more information about what the program does.

• -V

Display version information and exit.

# <span id="page-25-1"></span>**4.8.4 resolveip — Resolve Host name to IP Address or Vice Versa**

The [resolveip](#page-25-1) utility resolves host names to IP addresses and vice versa.

![](_page_25_Picture_15.jpeg)

#### **Note**

[resolveip](#page-25-1) is deprecated and is removed in MySQL 8.0. nslookup, host, or dig can be used instead.

Invoke [resolveip](#page-25-1) like this:

```
resolveip [options] {host_name|ip-addr} ...
```

[resolveip](#page-25-1) supports the following options.

<span id="page-25-2"></span>• [--help](#page-25-2), [--info](#page-25-2), -?, -I

Display a help message and exit.

<span id="page-25-3"></span>• [--silent](#page-25-3), -s

Silent mode. Produce less output.

• [--version](#page-25-4), -V

Display version information and exit.

# <span id="page-25-4"></span><span id="page-25-0"></span>**4.8.5 zlib\_decompress — Decompress mysqlpump ZLIB-Compressed Output**

The [zlib\\_decompress](#page-25-0) utility decompresses mysqlpump output that was created using ZLIB compression. [zlib\\_decompress](#page-25-0) was added in MySQL 5.7.10.

Invoke [zlib\\_decompress](#page-25-0) like this:

```
zlib_decompress input_file output_file
```

Example:

```
mysqlpump --compress-output=ZLIB > dump.zlib
zlib_decompress dump.zlib dump.txt
```

To see a help message, invoke [zlib\\_decompress](#page-25-0) with no arguments.

To decompress mysqlpump LZ4-compressed output, use [lz4\\_decompress](#page-23-4). See [Section 4.8.1,](#page-23-4) ["lz4\\_decompress — Decompress mysqlpump LZ4-Compressed Output".](#page-23-4)