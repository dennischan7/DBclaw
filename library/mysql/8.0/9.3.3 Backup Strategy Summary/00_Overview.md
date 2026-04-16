---
source: MySQL 8.0 Reference
title: 00_Overview
---

In case of an operating system crash or power failure, InnoDB itself does all the job of recovering data. But to make sure that you can sleep well, observe the following guidelines:

- Always tun the MySQL server with binary logging enabled (that is the default setting for MySQL 8.0). If you have such safe media, this technique can also be good for disk load balancing (which results in a performance improvement).
- Make periodic full backups, using the mysqldump command shown earlier in [Section 9.3.1,](#page-2-0) ["Establishing a Backup Policy"](#page-2-0), that makes an online, nonblocking backup.
- Make periodic incremental backups by flushing the logs with FLUSH LOGS or mysqladmin flushlogs.

# <span id="page-5-0"></span>**9.4 Using mysqldump for Backups**

![](_page_5_Picture_10.jpeg)

#### **Tip**

Consider using the [MySQL Shell dump utilities,](https://dev.mysql.com/doc/mysql-shell/8.0/en/mysql-shell-utilities-dump-instance-schema.md) which provide parallel dumping with multiple threads, file compression, and progress information display, as well as cloud features such as Oracle Cloud Infrastructure Object Storage streaming, and MySQL HeatWave compatibility checks and modifications. Dumps can be easily imported into a MySQL Server instance or a MySQL HeatWave DB System using the [MySQL Shell load dump utilities.](https://dev.mysql.com/doc/mysql-shell/8.0/en/mysql-shell-utilities-load-dump.md) Installation instructions for MySQL Shell can be found [here.](https://dev.mysql.com/doc/mysql-shell/8.0/en/mysql-shell-install.md)

This section describes how to use mysqldump to produce dump files, and how to reload dump files. A dump file can be used in several ways:

- As a backup to enable data recovery in case of data loss.
- As a source of data for setting up replicas.
- As a source of data for experimentation:
  - To make a copy of a database that you can use without changing the original data.
  - To test potential upgrade incompatibilities.

mysqldump produces two types of output, depending on whether the --tab option is given:

- Without --tab, mysqldump writes SQL statements to the standard output. This output consists of CREATE statements to create dumped objects (databases, tables, stored routines, and so forth), and INSERT statements to load data into tables. The output can be saved in a file and reloaded later using mysql to recreate the dumped objects. Options are available to modify the format of the SQL statements, and to control which objects are dumped.
- With --tab, mysqldump produces two output files for each dumped table. The server writes one file as tab-delimited text, one line per table row. This file is named tbl\_name.txt in the output directory. The server also sends a CREATE TABLE statement for the table to mysqldump, which writes it as a file named tbl\_name.sql in the output directory.