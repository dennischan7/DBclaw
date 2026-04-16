---
source: MySQL 8.0 Reference
title: 00_Overview
---

Many MySQL programs have internal variables that can be set at runtime using the SET statement. See Section 15.7.6.1, "SET Syntax for Variable Assignment", and Section 7.1.9, "Using System Variables".

Most of these program variables also can be set at server startup by using the same syntax that applies to specifying program options. For example, <code>mysql</code> has a <code>max\_allowed\_packet</code> variable that controls the maximum size of its communication buffer. To set the <code>max\_allowed\_packet</code> variable for <code>mysql</code> to a value of 16MB, use either of the following commands:

```
mysql --max_allowed_packet=16777216
mysql --max_allowed_packet=16M
```

The first command specifies the value in bytes. The second specifies the value in megabytes. For variables that take a numeric value, the value can be given with a suffix of K, M, or G to indicate a multiplier of 1024, 1024 $^2$  or 1024 $^3$ . (For example, when used to set  $max_allowed_packet$ , the suffixes indicate units of kilobytes, megabytes, or gigabytes.) As of MySQL 8.0.14, a suffix can also be T, P, and E to indicate a multiplier of 1024 $^4$ , 1024 $^5$  or 1024 $^6$ . Suffix letters can be uppercase or lowercase.

In an option file, variable settings are given without the leading dashes:

```
[mysq1]
max_allowed_packet=16777216
```

#### Or:

```
[mysql]
max_allowed_packet=16M
```

If you like, underscores in an option name can be specified as dashes. The following option groups are equivalent. Both set the size of the server's key buffer to 512MB:

```
[mysqld]
key_buffer_size=512M

[mysqld]
key-buffer-size=512M
```

Suffixes for specifying a value multiplier can be used when setting a variable at program invocation time, but not to set the value with SET at runtime. On the other hand, with SET, you can assign a variable's value using an expression, which is not true when you set a variable at server startup. For example, the first of the following lines is legal at program invocation time, but the second is not:

```
$> mysql --max_allowed_packet=16M
$> mysql --max_allowed_packet=16*1024*1024
```

Conversely, the second of the following lines is legal at runtime, but the first is not:

```
mysql> SET GLOBAL max_allowed_packet=16M;
mysql> SET GLOBAL max_allowed_packet=16*1024*1024;
```