---
source: MySQL 5.7 Reference
title: 00_Overview
---

This section describes administrative programs and programs that perform miscellaneous utility operations.

# <span id="page-148-4"></span>**4.6.1 innochecksum — Offline InnoDB File Checksum Utility**

[innochecksum](#page-148-4) prints checksums for InnoDB files. This tool reads an InnoDB tablespace file, calculates the checksum for each page, compares the calculated checksum to the stored checksum, and reports mismatches, which indicate damaged pages. It was originally developed to speed up verifying the integrity of tablespace files after power outages but can also be used after file copies. Because checksum mismatches cause InnoDB to deliberately shut down a running server, it may be preferable to use this tool rather than waiting for an in-production server to encounter the damaged pages.

[innochecksum](#page-148-4) cannot be used on tablespace files that the server already has open. For such files, you should use CHECK TABLE to check tables within the tablespace. Attempting to run [innochecksum](#page-148-4) on a tablespace that the server already has open results in an Unable to lock file error.

If checksum mismatches are found, restore the tablespace from backup or start the server and attempt to use [mysqldump](#page-57-0) to make a backup of the tables within the tablespace.

Invoke [innochecksum](#page-148-4) like this:

innochecksum [options] file\_name

## **innochecksum Options**

[innochecksum](#page-148-4) supports the following options. For options that refer to page numbers, the numbers are zero-based.

<span id="page-149-0"></span>• [--help](#page-149-0), -?

| Command-Line Format | help    |
|---------------------|---------|
| Type                | Boolean |
| Default Value       | false   |

Displays command line help. Example usage:

innochecksum --help

<span id="page-149-1"></span>• [--info](#page-149-1), -I

| Command-Line Format | info    |
|---------------------|---------|
| Type                | Boolean |
| Default Value       | false   |

Synonym for [--help](#page-149-0). Displays command line help. Example usage:

innochecksum --info

<span id="page-149-2"></span>• [--version](#page-149-2), -V

| Command-Line Format | version |
|---------------------|---------|
| Type                | Boolean |
| Default Value       | false   |

Displays version information. Example usage:

innochecksum --version

<span id="page-149-3"></span>• [--verbose](#page-149-3), -v

| Command-Line Format | verbose |
|---------------------|---------|
| Type                | Boolean |
| Default Value       | false   |

Verbose mode; prints a progress indicator to the log file every five seconds. In order for the progress indicator to be printed, the log file must be specified using the --log option. To turn on verbose mode, run:

innochecksum --verbose

To turn off verbose mode, run:

innochecksum --verbose=FALSE

The --verbose option and --log option can be specified at the same time. For example:

```
innochecksum --verbose --log=/var/lib/mysql/test/logtest.txt
```

To locate the progress indicator information in the log file, you can perform the following search:

```
cat ./logtest.txt | grep -i "okay"
```

The progress indicator information in the log file appears similar to the following:

```
page 1663 okay: 2.863% done
page 8447 okay: 14.537% done
page 13695 okay: 23.568% done
page 18815 okay: 32.379% done
page 23039 okay: 39.648% done
page 28351 okay: 48.789% done
page 33023 okay: 56.828% done
page 37951 okay: 65.308% done
page 44095 okay: 75.881% done
page 49407 okay: 85.022% done
page 54463 okay: 93.722% done
...
```

<span id="page-150-0"></span>• [--count](#page-150-0), -c

| Command-Line Format | count     |
|---------------------|-----------|
| Type                | Base name |
| Default Value       | true      |

Print a count of the number of pages in the file and exit. Example usage:

```
innochecksum --count ../data/test/tab1.ibd
```

<span id="page-150-1"></span>• [--start-page=](#page-150-1)num, -s num

| Command-Line Format | start-page=# |
|---------------------|--------------|
| Type                | Numeric      |
| Default Value       | 0            |

#### Start at this page number. Example usage:

```
innochecksum --start-page=600 ../data/test/tab1.ibd
```

or:

```
innochecksum -s 600 ../data/test/tab1.ibd
```

<span id="page-150-2"></span>• [--end-page=](#page-150-2)num, -e num

| Command-Line Format | end-page=# |
|---------------------|------------|
| Type                | Numeric    |
| Default Value       | 0          |
| Minimum Value       | 0          |

| Maximum Value | 18446744073709551615 |
|---------------|----------------------|
|---------------|----------------------|

#### End at this page number. Example usage:

innochecksum --end-page=700 ../data/test/tab1.ibd

or:

innochecksum --p 700 ../data/test/tab1.ibd

<span id="page-151-0"></span>• [--page=](#page-151-0)num, -p num

| Command-Line Format | page=#  |
|---------------------|---------|
| Type                | Integer |
| Default Value       | 0       |

#### Check only this page number. Example usage:

innochecksum --page=701 ../data/test/tab1.ibd

<span id="page-151-1"></span>• [--strict-check](#page-151-1), -C

| Command-Line Format | strict-check=algorithm |
|---------------------|------------------------|
| Type                | Enumeration            |
| Default Value       | crc32                  |
| Valid Values        | innodb                 |
|                     | crc32                  |
|                     | none                   |

Specify a strict checksum algorithm. Options include innodb, crc32, and none.

In this example, the innodb checksum algorithm is specified:

```
innochecksum --strict-check=innodb ../data/test/tab1.ibd
```

In this example, the crc32 checksum algorithm is specified:

innochecksum -C crc32 ../data/test/tab1.ibd

The following conditions apply:

- If you do not specify the [--strict-check](#page-151-1) option, [innochecksum](#page-148-4) validates against innodb, crc32 and none.
- If you specify the none option, only checksums generated by none are allowed.
- If you specify the innodb option, only checksums generated by innodb are allowed.
- If you specify the crc32 option, only checksums generated by crc32 are allowed.
- <span id="page-151-2"></span>• [--no-check](#page-151-2), -n

| Command-Line Format | no-check |
|---------------------|----------|
| Type                | Boolean  |
| Default Value       | false    |

Ignore the checksum verification when rewriting a checksum. This option may only be used with the [innochecksum](#page-148-4) [--write](#page-152-0) option. If the [--write](#page-152-0) option is not specified, [innochecksum](#page-148-4) terminates.

In this example, an innodb checksum is rewritten to replace an invalid checksum:

innochecksum --no-check --write innodb ../data/test/tab1.ibd

<span id="page-152-1"></span>• [--allow-mismatches](#page-152-1), -a

| Command-Line Format | allow-mismatches=#   |
|---------------------|----------------------|
| Type                | Integer              |
| Default Value       | 0                    |
| Minimum Value       | 0                    |
| Maximum Value       | 18446744073709551615 |

The maximum number of checksum mismatches allowed before [innochecksum](#page-148-4) terminates. The default setting is 0. If --allow-mismatches=N, where N>=0, N mismatches are permitted and [innochecksum](#page-148-4) terminates at N+1. When --allow-mismatches is set to 0, [innochecksum](#page-148-4) terminates on the first checksum mismatch.

In this example, an existing innodb checksum is rewritten to set --allow-mismatches to 1.

```
innochecksum --allow-mismatches=1 --write innodb ../data/test/tab1.ibd
```

With --allow-mismatches set to 1, if there is a mismatch at page 600 and another at page 700 on a file with 1000 pages, the checksum is updated for pages 0-599 and 601-699. Because - allow-mismatches is set to 1, the checksum tolerates the first mismatch and terminates on the second mismatch, leaving page 600 and pages 700-999 unchanged.

<span id="page-152-0"></span>• [--write=](#page-152-0)name, -w num

| Command-Line Format | write=algorithm |
|---------------------|-----------------|
| Type                | Enumeration     |
| Default Value       | crc32           |
| Valid Values        | innodb          |
|                     | crc32           |
|                     | none            |

Rewrite a checksum. When rewriting an invalid checksum, the [--no-check](#page-151-2) option must be used together with the --write option. The [--no-check](#page-151-2) option tells [innochecksum](#page-148-4) to ignore verification of the invalid checksum. You do not have to specify the [--no-check](#page-151-2) option if the current checksum is valid.

An algorithm must be specified when using the [--write](#page-152-0) option. Possible values for the --write option are:

- innodb: A checksum calculated in software, using the original algorithm from InnoDB.
- crc32: A checksum calculated using the crc32 algorithm, possibly done with a hardware assist.

• none: A constant number.

The --write option rewrites entire pages to disk. If the new checksum is identical to the existing checksum, the new checksum is not written to disk in order to minimize I/O.

[innochecksum](#page-148-4) obtains an exclusive lock when the --write option is used.

In this example, a crc32 checksum is written for tab1.ibd:

```
innochecksum -w crc32 ../data/test/tab1.ibd
```

In this example, a crc32 checksum is rewritten to replace an invalid crc32 checksum:

```
innochecksum --no-check --write crc32 ../data/test/tab1.ibd
```

<span id="page-153-0"></span>• [--page-type-summary](#page-153-0), -S

| Command-Line Format | page-type-summary |
|---------------------|-------------------|
| Type                | Boolean           |
| Default Value       | false             |

Display a count of each page type in a tablespace. Example usage:

```
innochecksum --page-type-summary ../data/test/tab1.ibd
```

Sample output for --page-type-summary:

```
File::../data/test/tab1.ibd
================PAGE TYPE SUMMARY==============
#PAGE_COUNT PAGE_TYPE
===============================================
 2 Index page
 0 Undo log page
 1 Inode page
 0 Insert buffer free list page
 2 Freshly allocated page
 1 Insert buffer bitmap
 0 System page
 0 Transaction system page
 1 File Space Header
 0 Extent descriptor page
 0 BLOB page
 0 Compressed BLOB page
 0 Other type of page
===============================================
Additional information:
Undo page type: 0 insert, 0 update, 0 other
Undo page state: 0 active, 0 cached, 0 to_free, 0 to_purge, 0 prepared, 0 other
```

<span id="page-153-1"></span>• [--page-type-dump](#page-153-1), -D

| Command-Line Format | page-type-dump=name |
|---------------------|---------------------|
| Type                | String              |
| Default Value       | [none]              |

Dump the page type information for each page in a tablespace to stderr or stdout. Example usage:

#### <span id="page-154-0"></span>• [--log](#page-154-0), -l

| Command-Line Format | log=path  |
|---------------------|-----------|
| Type                | File name |
| Default Value       | [none]    |

Log output for the [innochecksum](#page-148-4) tool. A log file name must be provided. Log output contains checksum values for each tablespace page. For uncompressed tables, LSN values are also provided. The [--log](#page-154-0) replaces the --debug option, which was available in earlier releases. Example usage:

```
innochecksum --log=/tmp/log.txt ../data/test/tab1.ibd
```

or:

```
innochecksum -l /tmp/log.txt ../data/test/tab1.ibd
```

• - option.

Specify the - option to read from standard input. If the - option is missing when "read from standard in" is expected, [innochecksum](#page-148-4) prints [innochecksum](#page-148-4) usage information indicating that the "-" option was omitted. Example usages:

```
cat t1.ibd | innochecksum -
```

In this example, [innochecksum](#page-148-4) writes the crc32 checksum algorithm to a.ibd without changing the original t1.ibd file.

```
cat t1.ibd | innochecksum --write=crc32 - > a.ibd
```

## **Running innochecksum on Multiple User-defined Tablespace Files**

The following examples demonstrate how to run [innochecksum](#page-148-4) on multiple user-defined tablespace files (.ibd files).

Run [innochecksum](#page-148-4) for all tablespace (.ibd) files in the "test" database:

```
innochecksum ./data/test/*.ibd
```

Run [innochecksum](#page-148-4) for all tablespace files (.ibd files) that have a file name starting with "t":

```
innochecksum ./data/test/t*.ibd
```

Run [innochecksum](#page-148-4) for all tablespace files (.ibd files) in the data directory:

innochecksum ./data/\*/\*.ibd

![](_page_154_Picture_20.jpeg)

## **Note**

Running [innochecksum](#page-148-4) on multiple user-defined tablespace files is not supported on Windows operating systems, as Windows shells such as cmd.exe do not support glob pattern expansion. On Windows systems, [innochecksum](#page-148-4) must be run separately for each user-defined tablespace file. For example:

```
innochecksum.exe t1.ibd
innochecksum.exe t2.ibd
innochecksum.exe t3.ibd
```

## **Running innochecksum on Multiple System Tablespace Files**

By default, there is only one InnoDB system tablespace file (ibdata1) but multiple files for the system tablespace can be defined using the innodb\_data\_file\_path option. In the following example,

three files for the system tablespace are defined using the innodb\_data\_file\_path option: ibdata1, ibdata2, and ibdata3.

```
./bin/mysqld --no-defaults --innodb-data-file-path="ibdata1:10M;ibdata2:10M;ibdata3:10M:autoextend"
```

The three files (ibdata1, ibdata2, and ibdata3) form one logical system tablespace. To run [innochecksum](#page-148-4) on multiple files that form one logical system tablespace, [innochecksum](#page-148-4) requires the - option to read tablespace files in from standard input, which is equivalent to concatenating multiple files to create one single file. For the example provided above, the following [innochecksum](#page-148-4) command would be used:

```
cat ibdata* | innochecksum -
```

Refer to the [innochecksum](#page-148-4) options information for more information about the "-" option.

![](_page_155_Picture_6.jpeg)

#### **Note**

Running [innochecksum](#page-148-4) on multiple files in the same tablespace is not supported on Windows operating systems, as Windows shells such as cmd.exe do not support glob pattern expansion. On Windows systems, [innochecksum](#page-148-4) must be run separately for each system tablespace file. For example:

```
innochecksum.exe ibdata1
innochecksum.exe ibdata2
innochecksum.exe ibdata3
```

# <span id="page-155-0"></span>**4.6.2 myisam\_ftdump — Display Full-Text Index information**

[myisam\\_ftdump](#page-155-0) displays information about FULLTEXT indexes in MyISAM tables. It reads the MyISAM index file directly, so it must be run on the server host where the table is located. Before using [myisam\\_ftdump](#page-155-0), be sure to issue a FLUSH TABLES statement first if the server is running.

[myisam\\_ftdump](#page-155-0) scans and dumps the entire index, which is not particularly fast. On the other hand, the distribution of words changes infrequently, so it need not be run often.

Invoke [myisam\\_ftdump](#page-155-0) like this:

```
myisam_ftdump [options] tbl_name index_num
```

The tbl\_name argument should be the name of a MyISAM table. You can also specify a table by naming its index file (the file with the .MYI suffix). If you do not invoke [myisam\\_ftdump](#page-155-0) in the directory where the table files are located, the table or index file name must be preceded by the path name to the table's database directory. Index numbers begin with 0.

Example: Suppose that the test database contains a table named mytexttable that has the following definition:

```
CREATE TABLE mytexttable
(
 id INT NOT NULL,
 txt TEXT NOT NULL,
 PRIMARY KEY (id),
 FULLTEXT (txt)
) ENGINE=MyISAM;
```

The index on id is index 0 and the FULLTEXT index on txt is index 1. If your working directory is the test database directory, invoke [myisam\\_ftdump](#page-155-0) as follows:

```
myisam_ftdump mytexttable 1
```

If the path name to the test database directory is /usr/local/mysql/data/test, you can also specify the table name argument using that path name. This is useful if you do not invoke [myisam\\_ftdump](#page-155-0) in the database directory:

```
myisam_ftdump /usr/local/mysql/data/test/mytexttable 1
```

You can use [myisam\\_ftdump](#page-155-0) to generate a list of index entries in order of frequency of occurrence like this on Unix-like systems:

myisam\_ftdump -c mytexttable 1 | sort -r

On Windows, use:

myisam\_ftdump -c mytexttable 1 | sort /R

[myisam\\_ftdump](#page-155-0) supports the following options:

<span id="page-156-0"></span>• [--help](#page-156-0), -h -?

| Command-Line Format | help |
|---------------------|------|
|---------------------|------|

Display a help message and exit.

<span id="page-156-1"></span>• [--count](#page-156-1), -c

| Command-Line Format | count |
|---------------------|-------|
|---------------------|-------|

Calculate per-word statistics (counts and global weights).

<span id="page-156-2"></span>• [--dump](#page-156-2), -d

| Command-Line Format | dump |
|---------------------|------|
|---------------------|------|

Dump the index, including data offsets and word weights.

<span id="page-156-3"></span>• [--length](#page-156-3), -l

| Command-Line Format | length |
|---------------------|--------|

Report the length distribution.

<span id="page-156-4"></span>• [--stats](#page-156-4), -s

| Command-Line Format | stats |
|---------------------|-------|
|---------------------|-------|

Report global index statistics. This is the default operation if no other operation is specified.

<span id="page-156-5"></span>• [--verbose](#page-156-5), -v

| Command-Line Format | verbose |
|---------------------|---------|

Verbose mode. Print more output about what the program does.

# <span id="page-156-6"></span>**4.6.3 myisamchk — MyISAM Table-Maintenance Utility**

The [myisamchk](#page-156-6) utility gets information about your database tables or checks, repairs, or optimizes them. [myisamchk](#page-156-6) works with MyISAM tables (tables that have .MYD and .MYI files for storing data and indexes).

You can also use the CHECK TABLE and REPAIR TABLE statements to check and repair MyISAM tables. See Section 13.7.2.2, "CHECK TABLE Statement", and Section 13.7.2.5, "REPAIR TABLE Statement".

The use of [myisamchk](#page-156-6) with partitioned tables is not supported.

![](_page_157_Picture_2.jpeg)

#### **Caution**

It is best to make a backup of a table before performing a table repair operation; under some circumstances the operation might cause data loss. Possible causes include but are not limited to file system errors.

Invoke [myisamchk](#page-156-6) like this:

```
myisamchk [options] tbl_name ...
```

The options specify what you want [myisamchk](#page-156-6) to do. They are described in the following sections. You can also get a list of options by invoking [myisamchk --help](#page-156-6).

With no options, [myisamchk](#page-156-6) simply checks your table as the default operation. To get more information or to tell [myisamchk](#page-156-6) to take corrective action, specify options as described in the following discussion.

tbl\_name is the database table you want to check or repair. If you run [myisamchk](#page-156-6) somewhere other than in the database directory, you must specify the path to the database directory, because [myisamchk](#page-156-6) has no idea where the database is located. In fact, [myisamchk](#page-156-6) does not actually care whether the files you are working on are located in a database directory. You can copy the files that correspond to a database table into some other location and perform recovery operations on them there.

You can name several tables on the [myisamchk](#page-156-6) command line if you wish. You can also specify a table by naming its index file (the file with the .MYI suffix). This enables you to specify all tables in a directory by using the pattern \*.MYI. For example, if you are in a database directory, you can check all the MyISAM tables in that directory like this:

```
myisamchk *.MYI
```

If you are not in the database directory, you can check all the tables there by specifying the path to the directory:

```
myisamchk /path/to/database_dir/*.MYI
```

You can even check all tables in all databases by specifying a wildcard with the path to the MySQL data directory:

```
myisamchk /path/to/datadir/*/*.MYI
```

The recommended way to quickly check all MyISAM tables is:

```
myisamchk --silent --fast /path/to/datadir/*/*.MYI
```

If you want to check all MyISAM tables and repair any that are corrupted, you can use the following command:

```
myisamchk --silent --force --fast --update-state \
 --key_buffer_size=64M --myisam_sort_buffer_size=64M \
 --read_buffer_size=1M --write_buffer_size=1M \
 /path/to/datadir/*/*.MYI
```

This command assumes that you have more than 64MB free. For more information about memory allocation with [myisamchk](#page-156-6), see [Section 4.6.3.6, "myisamchk Memory Usage".](#page-175-0)

For additional information about using [myisamchk](#page-156-6), see Section 7.6, "MyISAM Table Maintenance and Crash Recovery".

![](_page_157_Picture_22.jpeg)

#### **Important**

You must ensure that no other program is using the tables while you are running [myisamchk](#page-156-6). The most effective means of doing so is to shut down the MySQL server while running [myisamchk](#page-156-6), or to lock all tables that [myisamchk](#page-156-6) is being used on.

Otherwise, when you run [myisamchk](#page-156-6), it may display the following error message:

warning: clients are using or haven't closed the table properly

This means that you are trying to check a table that has been updated by another program (such as the mysqld server) that hasn't yet closed the file or that has died without closing the file properly, which can sometimes lead to the corruption of one or more MyISAM tables.

If mysqld is running, you must force it to flush any table modifications that are still buffered in memory by using FLUSH TABLES. You should then ensure that no one is using the tables while you are running [myisamchk](#page-156-6)

However, the easiest way to avoid this problem is to use CHECK TABLE instead of [myisamchk](#page-156-6) to check tables. See Section 13.7.2.2, "CHECK TABLE Statement".

[myisamchk](#page-156-6) supports the following options, which can be specified on the command line or in the [myisamchk] group of an option file. For information about option files used by MySQL programs, see Section 4.2.2.2, "Using Option Files".

**Table 4.21 myisamchk Options**

| Option Name           | Description                                                                                           |
|-----------------------|-------------------------------------------------------------------------------------------------------|
| analyze               | Analyze the distribution of key values                                                                |
| backup                | Make a backup of the .MYD file as file_name<br>time.BAK                                               |
| block-search          | Find the record that a block at the given offset<br>belongs to                                        |
| character-sets-dir    | Directory where character sets can be found                                                           |
| check                 | Check the table for errors                                                                            |
| check-only-changed    | Check only tables that have changed since the<br>last check                                           |
| correct-checksum      | Correct the checksum information for the table                                                        |
| data-file-length      | Maximum length of the data file (when re-creating<br>data file when it is full)                       |
| debug                 | Write debugging log                                                                                   |
| decode_bits           | Decode_bits                                                                                           |
| defaults-extra-file   | Read named option file in addition to usual option<br>files                                           |
| defaults-file         | Read only named option file                                                                           |
| defaults-group-suffix | Option group suffix value                                                                             |
| description           | Print some descriptive information about the table                                                    |
| extend-check          | Do very thorough table check or repair that tries to<br>recover every possible row from the data file |
| fast                  | Check only tables that haven't been closed<br>properly                                                |
| force                 | Do a repair operation automatically if myisamchk<br>finds any errors in the table                     |

| Option Name             | Description                                                                                                                             |
|-------------------------|-----------------------------------------------------------------------------------------------------------------------------------------|
| force                   | Overwrite old temporary files. For use with the -r<br>or -o option                                                                      |
| ft_max_word_len         | Maximum word length for FULLTEXT indexes                                                                                                |
| ft_min_word_len         | Minimum word length for FULLTEXT indexes                                                                                                |
| ft_stopword_file        | Use stopwords from this file instead of built-in list                                                                                   |
| HELP                    | Display help message and exit                                                                                                           |
| help                    | Display help message and exit                                                                                                           |
| information             | Print informational statistics about the table that is<br>checked                                                                       |
| key_buffer_size         | Size of buffer used for index blocks for MyISAM<br>tables                                                                               |
| keys-used               | A bit-value that indicates which indexes to update                                                                                      |
| max-record-length       | Skip rows larger than the given length if<br>myisamchk cannot allocate memory to hold them                                              |
| medium-check            | Do a check that is faster than anextend-check<br>operation                                                                              |
| myisam_block_size       | Block size to be used for MyISAM index pages                                                                                            |
| myisam_sort_buffer_size | The buffer that is allocated when sorting the index<br>when doing a REPAIR or when creating indexes<br>with CREATE INDEX or ALTER TABLE |
| no-defaults             | Read no option files                                                                                                                    |
| parallel-recover        | Uses the same technique as -r and -n, but creates<br>all the keys in parallel, using different threads<br>(beta)                        |
| print-defaults          | Print default options                                                                                                                   |
| quick                   | Achieve a faster repair by not modifying the data<br>file                                                                               |
| read_buffer_size        | Each thread that does a sequential scan allocates<br>a buffer of this size for each table it scans                                      |
| read-only               | Do not mark the table as checked                                                                                                        |
| recover                 | Do a repair that can fix almost any problem except<br>unique keys that aren't unique                                                    |
| safe-recover            | Do a repair using an old recovery method that<br>reads through all rows in order and updates all<br>index trees based on the rows found |
| set-auto-increment      | Force AUTO_INCREMENT numbering for new<br>records to start at the given value                                                           |
| set-collation           | Specify the collation to use for sorting table<br>indexes                                                                               |
| silent                  | Silent mode                                                                                                                             |
| sort_buffer_size        | The buffer that is allocated when sorting the index<br>when doing a REPAIR or when creating indexes<br>with CREATE INDEX or ALTER TABLE |
| sort-index              | Sort the index tree blocks in high-low order                                                                                            |
| sort_key_blocks         | sort_key_blocks                                                                                                                         |
| sort-records            | Sort records according to a particular index                                                                                            |

| Option Name       | Description                                                                                                   |
|-------------------|---------------------------------------------------------------------------------------------------------------|
| sort-recover      | Force myisamchk to use sorting to resolve the<br>keys even if the temporary files would be very<br>large      |
| stats_method      | Specifies how MyISAM index statistics collection<br>code should treat NULLs                                   |
| tmpdir            | Directory to be used for storing temporary files                                                              |
| unpack            | Unpack a table that was packed with myisampack                                                                |
| update-state      | Store information in the .MYI file to indicate when<br>the table was checked and whether the table<br>crashed |
| verbose           | Verbose mode                                                                                                  |
| version           | Display version information and exit                                                                          |
| wait              | Wait for locked table to be unlocked, instead of<br>terminating                                               |
| write_buffer_size | Write buffer size                                                                                             |