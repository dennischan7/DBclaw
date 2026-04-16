---
source: MySQL 8.0 Reference
title: 00_Overview
---

This section describes how to check for and deal with data corruption in MySQL databases. If your tables become corrupted frequently, you should try to find the reason why. See Section B.3.3.3, "What to Do If MySQL Keeps Crashing".

For an explanation of how MyISAM tables can become corrupted, see Section 18.2.4, "MyISAM Table Problems".

If you run mysqld with external locking disabled (which is the default), you cannot reliably use myisamchk to check a table when mysqld is using the same table. If you can be certain that no one can access the tables using mysqld while you run myisamchk, you only have to execute mysqladmin flush-tables before you start checking the tables. If you cannot guarantee this, you must stop mysqld while you check the tables. If you run myisamchk to check tables that mysqld is updating at the same time, you may get a warning that a table is corrupt even when it is not.

If the server is run with external locking enabled, you can use myisamchk to check tables at any time. In this case, if the server tries to update a table that myisamchk is using, the server waits for myisamchk to finish before it continues.

If you use myisamchk to repair or optimize tables, you must always ensure that the mysqld server is not using the table (this also applies if external locking is disabled). If you do not stop mysqld, you should at least do a mysqladmin flush-tables before you run myisamchk. Your tables may become corrupted if the server and myisamchk access the tables simultaneously.

When performing crash recovery, it is important to understand that each MyISAM table tbl\_name in a database corresponds to the three files in the database directory shown in the following table.

| File         | Purpose    |
|--------------|------------|
| tbl_name.MYD | Data file  |
| tbl_name.MYI | Index file |

Each of these three file types is subject to corruption in various ways, but problems occur most often in data files and index files.

myisamchk works by creating a copy of the .MYD data file row by row. It ends the repair stage by removing the old .MYD file and renaming the new file to the original file name. If you use --quick, myisamchk does not create a temporary .MYD file, but instead assumes that the .MYD file is correct and generates only a new index file without touching the .MYD file. This is safe, because myisamchk automatically detects whether the .MYD file is corrupt and aborts the repair if it is. You can also specify the --quick option twice to myisamchk. In this case, myisamchk does not abort on some errors (such as duplicate-key errors) but instead tries to resolve them by modifying the .MYD file. Normally the use of two --quick options is useful only if you have too little free disk space to perform a normal repair. In this case, you should at least make a backup of the table before running myisamchk.

# <span id="page-15-0"></span>**9.6.2 How to Check MyISAM Tables for Errors**

To check a MyISAM table, use the following commands:

• myisamchk tbl\_name

This finds 99.99% of all errors. What it cannot find is corruption that involves only the data file (which is very unusual). If you want to check a table, you should normally run myisamchk without options or with the -s (silent) option.

• myisamchk -m tbl\_name

This finds 99.999% of all errors. It first checks all index entries for errors and then reads through all rows. It calculates a checksum for all key values in the rows and verifies that the checksum matches the checksum for the keys in the index tree.

• myisamchk -e tbl\_name

This does a complete and thorough check of all data (-e means "extended check"). It does a checkread of every key for each row to verify that they indeed point to the correct row. This may take a

long time for a large table that has many indexes. Normally, myisamchk stops after the first error it finds. If you want to obtain more information, you can add the -v (verbose) option. This causes myisamchk to keep going, up through a maximum of 20 errors.

• myisamchk -e -i tbl\_name

This is like the previous command, but the -i option tells myisamchk to print additional statistical information.

In most cases, a simple myisamchk command with no arguments other than the table name is sufficient to check a table.