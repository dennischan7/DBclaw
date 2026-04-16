---
source: MySQL 8.4 Reference
title: 00_Overview
---

The options described in this section can be used for any type of table maintenance operation performed by [myisamchk](#page-150-4). The sections following this one describe options that pertain only to specific operations, such as table checking or repairing.

<span id="page-154-4"></span>• [--help](#page-154-4), -?

| Command-Line Format | help |
|---------------------|------|
|---------------------|------|

Display a help message and exit. Options are grouped by type of operation.

<span id="page-154-3"></span>• [--HELP](#page-154-3), -H

| Command-Line Format | HELP |
|---------------------|------|
|---------------------|------|

Display a help message and exit. Options are presented in a single list.

<span id="page-154-0"></span>• --debug=[debug\\_options](#page-154-0), -# debug\_options

| Command-Line Format | debug[=debug_options]      |
|---------------------|----------------------------|
| Type                | String                     |
| Default Value       | d:t:o,/tmp/myisamchk.trace |

Write a debugging log. A typical debug\_options string is d:t:o,file\_name. The default is d:t:o,/tmp/myisamchk.trace.

This option is available only if MySQL was built using WITH\_DEBUG. MySQL release binaries provided by Oracle are not built using this option.

<span id="page-154-1"></span>• [--defaults-extra-file=](#page-154-1)file\_name

| Command-Line Format | defaults-extra-file=file_name |
|---------------------|-------------------------------|
| Type                | File name                     |

Read this option file after the global option file but (on Unix) before the user option file. If the file does not exist or is otherwise inaccessible, an error occurs. If file\_name is not an absolute path name, it is interpreted relative to the current directory.

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-154-2"></span>• [--defaults-file=](#page-154-2)file\_name

| Command-Line Format | defaults-file=file_name |
|---------------------|-------------------------|
| Type                | File name               |

Use only the given option file. If the file does not exist or is otherwise inaccessible, an error occurs. If file\_name is not an absolute path name, it is interpreted relative to the current directory.

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-155-0"></span>• [--defaults-group-suffix=](#page-155-0)str

| Command-Line Format | defaults-group-suffix=str |
|---------------------|---------------------------|
| Type                | String                    |

Read not only the usual option groups, but also groups with the usual names and a suffix of str. For example, [myisamchk](#page-150-4) normally reads the [myisamchk] group. If this option is given as [-](#page-155-0) [defaults-group-suffix=\\_other](#page-155-0), [myisamchk](#page-150-4) also reads the [myisamchk\_other] group.

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-155-1"></span>• [--no-defaults](#page-155-1)

| Command-Line Format | no-defaults |
|---------------------|-------------|
|---------------------|-------------|

Do not read any option files. If program startup fails due to reading unknown options from an option file, [--no-defaults](#page-155-1) can be used to prevent them from being read.

The exception is that the .mylogin.cnf file is read in all cases, if it exists. This permits passwords to be specified in a safer way than on the command line even when [--no-defaults](#page-155-1) is used. To create .mylogin.cnf, use the [mysql\\_config\\_editor](#page-176-0) utility. See [Section 6.6.7,](#page-176-0) ["mysql\\_config\\_editor — MySQL Configuration Utility".](#page-176-0)

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-155-2"></span>• [--print-defaults](#page-155-2)

| Command-Line Format | print-defaults |
|---------------------|----------------|
|---------------------|----------------|

Print the program name and all options that it gets from option files.

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-155-3"></span>• [--silent](#page-155-3), -s

| Command-Line Format | silent |
|---------------------|--------|

Silent mode. Write output only when errors occur. You can use -s twice (-ss) to make [myisamchk](#page-150-4) very silent.

<span id="page-155-4"></span>• [--verbose](#page-155-4), -v

| Command-Line Format | verbose |
|---------------------|---------|

Verbose mode. Print more information about what the program does. This can be used with -d and e. Use -v multiple times (-vv, -vvv) for even more output.

<span id="page-156-0"></span>• [--version](#page-156-0), -V

| Command-Line Format | version |
|---------------------|---------|
|---------------------|---------|

Display version information and exit.

<span id="page-156-1"></span>• [--wait](#page-156-1), -w

| Command-Line Format | wait    |
|---------------------|---------|
| Type                | Boolean |
| Default Value       | false   |

Instead of terminating with an error if the table is locked, wait until the table is unlocked before continuing. If you are running mysqld with external locking disabled, the table can be locked only by another [myisamchk](#page-150-4) command.

You can also set the following variables by using --var\_name=value syntax:

| Variable               | Default Value     |
|------------------------|-------------------|
| decode_bits            | 9                 |
| ft_max_word_len        | version-dependent |
| ft_min_word_len        | 4                 |
| ft_stopword_file       | built-in list     |
| key_buffer_size        | 523264            |
| myisam_block_size      | 1024              |
| myisam_sort_key_blocks | 16                |
| read_buffer_size       | 262136            |
| sort_buffer_size       | 2097144           |
| sort_key_blocks        | 16                |
| stats_method           | nulls_unequal     |
| write_buffer_size      | 262136            |

The possible [myisamchk](#page-150-4) variables and their default values can be examined with [myisamchk -](#page-150-4) [help](#page-150-4):

myisam\_sort\_buffer\_size is used when the keys are repaired by sorting keys, which is the normal case when you use [--recover](#page-160-2). sort\_buffer\_size is a deprecated synonym for myisam\_sort\_buffer\_size.

key\_buffer\_size is used when you are checking the table with [--extend-check](#page-157-2) or when the keys are repaired by inserting keys row by row into the table (like when doing normal inserts). Repairing through the key buffer is used in the following cases:

- You use [--safe-recover](#page-160-3).
- The temporary files needed to sort the keys would be more than twice as big as when creating the key file directly. This is often the case when you have large key values for CHAR, VARCHAR, or TEXT columns, because the sort operation needs to store the complete key values as it proceeds. If you have lots of temporary space and you can force [myisamchk](#page-150-4) to repair by sorting, you can use the [-](#page-161-4) [sort-recover](#page-161-4) option.

Repairing through the key buffer takes much less disk space than using sorting, but is also much slower.

If you want a faster repair, set the key\_buffer\_size and myisam\_sort\_buffer\_size variables to about 25% of your available memory. You can set both variables to large values, because only one of them is used at a time.

myisam\_block\_size is the size used for index blocks.

stats\_method influences how NULL values are treated for index statistics collection when the [--analyze](#page-161-0) option is given. It acts like the myisam\_stats\_method system variable. For more information, see the description of myisam\_stats\_method in Section 7.1.8, "Server System Variables", and Section 10.3.8, "InnoDB and MyISAM Index Statistics Collection".

ft\_min\_word\_len and ft\_max\_word\_len indicate the minimum and maximum word length for FULLTEXT indexes on MyISAM tables. ft\_stopword\_file names the stopword file. These need to be set under the following circumstances.

If you use [myisamchk](#page-150-4) to perform an operation that modifies table indexes (such as repair or analyze), the FULLTEXT indexes are rebuilt using the default full-text parameter values for minimum and maximum word length and the stopword file unless you specify otherwise. This can result in queries failing.

The problem occurs because these parameters are known only by the server. They are not stored in MyISAM index files. To avoid the problem if you have modified the minimum or maximum word length or the stopword file in the server, specify the same ft\_min\_word\_len, ft\_max\_word\_len, and ft\_stopword\_file values to [myisamchk](#page-150-4) that you use for mysqld. For example, if you have set the minimum word length to 3, you can repair a table with [myisamchk](#page-150-4) like this:

```
myisamchk --recover --ft_min_word_len=3 tbl_name.MYI
```

To ensure that [myisamchk](#page-150-4) and the server use the same values for full-text parameters, you can place each one in both the [mysqld] and [myisamchk] sections of an option file:

```
[mysqld]
ft_min_word_len=3
[myisamchk]
ft_min_word_len=3
```

An alternative to using [myisamchk](#page-150-4) is to use the REPAIR TABLE, ANALYZE TABLE, OPTIMIZE TABLE, or ALTER TABLE. These statements are performed by the server, which knows the proper fulltext parameter values to use.

# <span id="page-157-0"></span>**6.6.4.2 myisamchk Check Options**

[myisamchk](#page-150-4) supports the following options for table checking operations:

• [--check](#page-157-0), -c

| Command-Line Format | check |
|---------------------|-------|
|---------------------|-------|

Check the table for errors. This is the default operation if you specify no option that selects an operation type explicitly.

<span id="page-157-1"></span>• [--check-only-changed](#page-157-1), -C

| Command-Line Format | check-only-changed |
|---------------------|--------------------|
|---------------------|--------------------|

Check only tables that have changed since the last check.

<span id="page-157-2"></span>• [--extend-check](#page-157-2), -e

| Command-Line Format | extend-check |
|---------------------|--------------|

Check the table very thoroughly. This is quite slow if the table has many indexes. This option should only be used in extreme cases. Normally, [myisamchk](#page-150-4) or [myisamchk --medium-check](#page-150-4) should be able to determine whether there are any errors in the table.

If you are using [--extend-check](#page-157-2) and have plenty of memory, setting the key\_buffer\_size variable to a large value helps the repair operation run faster.

See also the description of this option under table repair options.

For a description of the output format, see [Section 6.6.4.5, "Obtaining Table Information with](#page-162-2) [myisamchk"](#page-162-2).

<span id="page-158-0"></span>• [--fast](#page-158-0), -F

| Command-Line Format | fast |
|---------------------|------|
|                     |      |

Check only tables that haven't been closed properly.

<span id="page-158-1"></span>• [--force](#page-158-1), -f

| Command-Line Format | force |
|---------------------|-------|
|---------------------|-------|

Do a repair operation automatically if [myisamchk](#page-150-4) finds any errors in the table. The repair type is the same as that specified with the [--recover](#page-160-2) or -r option.

<span id="page-158-2"></span>• [--information](#page-158-2), -i

| Command-Line Format | information |
|---------------------|-------------|
|---------------------|-------------|

Print informational statistics about the table that is checked.

<span id="page-158-3"></span>• [--medium-check](#page-158-3), -m

| Command-Line Format | medium-check |
|---------------------|--------------|
|---------------------|--------------|

Do a check that is faster than an [--extend-check](#page-157-2) operation. This finds only 99.99% of all errors, which should be good enough in most cases.

<span id="page-158-4"></span>• [--read-only](#page-158-4), -T

| Command-Line Format | read-only |
|---------------------|-----------|

Do not mark the table as checked. This is useful if you use [myisamchk](#page-150-4) to check a table that is in use by some other application that does not use locking, such as mysqld when run with external locking disabled.

<span id="page-158-5"></span>• [--update-state](#page-158-5), -U

| 529 |
|-----|
|-----|

| Command-Line Format<br>update-state |
|-------------------------------------|
|-------------------------------------|

shouldn't use this option if the mysqld server is using the table and you are running it with external locking disabled.