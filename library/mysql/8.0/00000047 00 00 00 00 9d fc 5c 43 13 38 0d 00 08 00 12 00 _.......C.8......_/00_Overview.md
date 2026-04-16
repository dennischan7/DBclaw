---
source: MySQL 8.0 Reference
title: 00_Overview
---

# 00000057 04 04 04 04 12 00 00 4b 00 04 1a |.......K...|
# Start: binlog v 4, server v 5.0.15-debug-log created 051024 17:24:13
# at startup
ROLLBACK;
```

Hex dump output currently contains the elements in the following list. This format is subject to change. For more information about binary log format, see [MySQL Internals: The Binary Log](https://dev.mysql.com/doc/internals/en/binary-log.md).

- Position: The byte position within the log file.
- Timestamp: The event timestamp. In the example shown, '9d fc 5c 43' is the representation of '051024 17:24:13' in hexadecimal.
- Type: The event type code.
- Master ID: The server ID of the replication source server that created the event.
- Size: The size in bytes of the event.
- Master Pos: The position of the next event in the original source log file.
- Flags: Event flag values.

## <span id="page-138-0"></span>**6.6.9.2 mysqlbinlog Row Event Display**

The following examples illustrate how [mysqlbinlog](#page-113-1) displays row events that specify data modifications. These correspond to events with the WRITE\_ROWS\_EVENT, UPDATE\_ROWS\_EVENT, and DELETE\_ROWS\_EVENT type codes. The [--base64-output=DECODE-ROWS](#page-118-0) and [--verbose](#page-135-1) options may be used to affect row event output.

Suppose that the server is using row-based binary logging and that you execute the following sequence of statements:

```
CREATE TABLE t
(
 id INT NOT NULL,
 name VARCHAR(20) NOT NULL,
 date DATE NULL
) ENGINE = InnoDB;
START TRANSACTION;
INSERT INTO t VALUES(1, 'apple', NULL);
UPDATE t SET name = 'pear', date = '2009-01-01' WHERE id = 1;
DELETE FROM t WHERE id = 1;
COMMIT;
```

By default, [mysqlbinlog](#page-113-1) displays row events encoded as base-64 strings using BINLOG statements. Omitting extraneous lines, the output for the row events produced by the preceding statement sequence looks like this:

```
$> mysqlbinlog log_file
...
# at 218
#080828 15:03:08 server id 1 end_log_pos 258 Write_rows: table id 17 flags: STMT_END_F
BINLOG '
fAS3SBMBAAAALAAAANoAAAAAABEAAAAAAAAABHRlc3QAAXQAAwMPCgIUAAQ=
fAS3SBcBAAAAKAAAAAIBAAAQABEAAAAAAAEAA//8AQAAAAVhcHBsZQ==
'/*!*/;
...
# at 302
#080828 15:03:08 server id 1 end_log_pos 356 Update_rows: table id 17 flags: STMT_END_F
BINLOG '
fAS3SBMBAAAALAAAAC4BAAAAABEAAAAAAAAABHRlc3QAAXQAAwMPCgIUAAQ=
fAS3SBgBAAAANgAAAGQBAAAQABEAAAAAAAEAA////AEAAAAFYXBwbGX4AQAAAARwZWFyIbIP
'/*!*/;
...
# at 400
#080828 15:03:08 server id 1 end_log_pos 442 Delete_rows: table id 17 flags: STMT_END_F
BINLOG '
```

```
fAS3SBMBAAAALAAAAJABAAAAABEAAAAAAAAABHRlc3QAAXQAAwMPCgIUAAQ=
fAS3SBkBAAAAKgAAALoBAAAQABEAAAAAAAEAA//4AQAAAARwZWFyIbIP
'/*!*/;
```

To see the row events as comments in the form of "pseudo-SQL" statements, run [mysqlbinlog](#page-113-1) with the [--verbose](#page-135-1) or -v option. This output level also shows table partition information where applicable. The output contains lines beginning with ###:

```
$> mysqlbinlog -v log_file
...
# at 218
#080828 15:03:08 server id 1 end_log_pos 258 Write_rows: table id 17 flags: STMT_END_F
BINLOG '
fAS3SBMBAAAALAAAANoAAAAAABEAAAAAAAAABHRlc3QAAXQAAwMPCgIUAAQ=
fAS3SBcBAAAAKAAAAAIBAAAQABEAAAAAAAEAA//8AQAAAAVhcHBsZQ==
'/*!*/;
### INSERT INTO test.t
### SET
### @1=1
### @2='apple'
### @3=NULL
...
# at 302
#080828 15:03:08 server id 1 end_log_pos 356 Update_rows: table id 17 flags: STMT_END_F
BINLOG '
fAS3SBMBAAAALAAAAC4BAAAAABEAAAAAAAAABHRlc3QAAXQAAwMPCgIUAAQ=
fAS3SBgBAAAANgAAAGQBAAAQABEAAAAAAAEAA////AEAAAAFYXBwbGX4AQAAAARwZWFyIbIP
'/*!*/;
### UPDATE test.t
### WHERE
### @1=1
### @2='apple'
### @3=NULL
### SET
### @1=1
### @2='pear'
### @3='2009:01:01'
...
# at 400
#080828 15:03:08 server id 1 end_log_pos 442 Delete_rows: table id 17 flags: STMT_END_F
BINLOG '
fAS3SBMBAAAALAAAAJABAAAAABEAAAAAAAAABHRlc3QAAXQAAwMPCgIUAAQ=
fAS3SBkBAAAAKgAAALoBAAAQABEAAAAAAAEAA//4AQAAAARwZWFyIbIP
'/*!*/;
### DELETE FROM test.t
### WHERE
### @1=1
### @2='pear'
### @3='2009:01:01'
```

Specify [--verbose](#page-135-1) or -v twice to also display data types and some metadata for each column, and informational log events such as row query log events if the binlog\_rows\_query\_log\_events system variable is set to TRUE. The output contains an additional comment following each column change:

```
$> mysqlbinlog -vv log_file
...
# at 218
#080828 15:03:08 server id 1 end_log_pos 258 Write_rows: table id 17 flags: STMT_END_F
BINLOG '
fAS3SBMBAAAALAAAANoAAAAAABEAAAAAAAAABHRlc3QAAXQAAwMPCgIUAAQ=
fAS3SBcBAAAAKAAAAAIBAAAQABEAAAAAAAEAA//8AQAAAAVhcHBsZQ==
'/*!*/;
### INSERT INTO test.t
### SET
### @1=1 /* INT meta=0 nullable=0 is_null=0 */
### @2='apple' /* VARSTRING(20) meta=20 nullable=0 is_null=0 */
```

```
### @3=NULL /* VARSTRING(20) meta=0 nullable=1 is_null=1 */
...
# at 302
#080828 15:03:08 server id 1 end_log_pos 356 Update_rows: table id 17 flags: STMT_END_F
BINLOG '
fAS3SBMBAAAALAAAAC4BAAAAABEAAAAAAAAABHRlc3QAAXQAAwMPCgIUAAQ=
fAS3SBgBAAAANgAAAGQBAAAQABEAAAAAAAEAA////AEAAAAFYXBwbGX4AQAAAARwZWFyIbIP
'/*!*/;
### UPDATE test.t
### WHERE
### @1=1 /* INT meta=0 nullable=0 is_null=0 */
### @2='apple' /* VARSTRING(20) meta=20 nullable=0 is_null=0 */
### @3=NULL /* VARSTRING(20) meta=0 nullable=1 is_null=1 */
### SET
### @1=1 /* INT meta=0 nullable=0 is_null=0 */
### @2='pear' /* VARSTRING(20) meta=20 nullable=0 is_null=0 */
### @3='2009:01:01' /* DATE meta=0 nullable=1 is_null=0 */
...
# at 400
#080828 15:03:08 server id 1 end_log_pos 442 Delete_rows: table id 17 flags: STMT_END_F
BINLOG '
fAS3SBMBAAAALAAAAJABAAAAABEAAAAAAAAABHRlc3QAAXQAAwMPCgIUAAQ=
fAS3SBkBAAAAKgAAALoBAAAQABEAAAAAAAEAA//4AQAAAARwZWFyIbIP
'/*!*/;
### DELETE FROM test.t
### WHERE
### @1=1 /* INT meta=0 nullable=0 is_null=0 */
### @2='pear' /* VARSTRING(20) meta=20 nullable=0 is_null=0 */
### @3='2009:01:01' /* DATE meta=0 nullable=1 is_null=0 */
```

You can tell [mysqlbinlog](#page-113-1) to suppress the BINLOG statements for row events by using the [-](#page-118-0) [base64-output=DECODE-ROWS](#page-118-0) option. This is similar to [--base64-output=NEVER](#page-118-0) but does not exit with an error if a row event is found. The combination of [--base64-output=DECODE-ROWS](#page-118-0) and [--verbose](#page-135-1) provides a convenient way to see row events only as SQL statements:

```
$> mysqlbinlog -v --base64-output=DECODE-ROWS log_file
...
# at 218
#080828 15:03:08 server id 1 end_log_pos 258 Write_rows: table id 17 flags: STMT_END_F
### INSERT INTO test.t
### SET
### @1=1
### @2='apple'
### @3=NULL
...
# at 302
#080828 15:03:08 server id 1 end_log_pos 356 Update_rows: table id 17 flags: STMT_END_F
### UPDATE test.t
### WHERE
### @1=1
### @2='apple'
### @3=NULL
### SET
### @1=1
### @2='pear'
### @3='2009:01:01'
...
# at 400
#080828 15:03:08 server id 1 end_log_pos 442 Delete_rows: table id 17 flags: STMT_END_F
### DELETE FROM test.t
### WHERE
### @1=1
### @2='pear'
### @3='2009:01:01'
```

![](_page_140_Picture_4.jpeg)

#### **Note**

You should not suppress BINLOG statements if you intend to re-execute [mysqlbinlog](#page-113-1) output.

The SQL statements produced by [--verbose](#page-135-1) for row events are much more readable than the corresponding BINLOG statements. However, they do not correspond exactly to the original SQL statements that generated the events. The following limitations apply:

- The original column names are lost and replaced by @N, where N is a column number.
- Character set information is not available in the binary log, which affects string column display:
  - There is no distinction made between corresponding binary and nonbinary string types (BINARY and CHAR, VARBINARY and VARCHAR, BLOB and TEXT). The output uses a data type of STRING for fixed-length strings and VARSTRING for variable-length strings.
  - For multibyte character sets, the maximum number of bytes per character is not present in the binary log, so the length for string types is displayed in bytes rather than in characters. For example, STRING(4) is used as the data type for values from either of these column types:

```
CHAR(4) CHARACTER SET latin1
CHAR(2) CHARACTER SET ucs2
```

• Due to the storage format for events of type UPDATE\_ROWS\_EVENT, UPDATE statements are displayed with the WHERE clause preceding the SET clause.

Proper interpretation of row events requires the information from the format description event at the beginning of the binary log. Because [mysqlbinlog](#page-113-1) does not know in advance whether the rest of the log contains row events, by default it displays the format description event using a BINLOG statement in the initial part of the output.

If the binary log is known not to contain any events requiring a BINLOG statement (that is, no row events), the [--base64-output=NEVER](#page-118-0) option can be used to prevent this header from being written.

## <span id="page-141-0"></span>**6.6.9.3 Using mysqlbinlog to Back Up Binary Log Files**

By default, [mysqlbinlog](#page-113-1) reads binary log files and displays their contents in text format. This enables you to examine events within the files more easily and to re-execute them (for example, by using the output as input to mysql). [mysqlbinlog](#page-113-1) can read log files directly from the local file system, or, with the [--read-from-remote-server](#page-129-0) option, it can connect to a server and request binary log contents from that server. [mysqlbinlog](#page-113-1) writes text output to its standard output, or to the file named as the value of the [--result-file=](#page-129-2)file\_name option if that option is given.

- [mysqlbinlog Backup Capabilities](#page-141-1)
- [mysqlbinlog Backup Options](#page-142-0)
- [Static and Live Backups](#page-142-1)
- [Output File Naming](#page-143-0)
- [Example: mysqldump + mysqlbinlog for Backup and Restore](#page-143-1)
- [mysqlbinlog Backup Restrictions](#page-144-1)

## <span id="page-141-1"></span>**mysqlbinlog Backup Capabilities**

[mysqlbinlog](#page-113-1) can read binary log files and write new files containing the same content—that is, in binary format rather than text format. This capability enables you to easily back up a binary log in its original format. [mysqlbinlog](#page-113-1) can make a static backup, backing up a set of log files and stopping when the end of the last file is reached. It can also make a continuous ("live") backup, staying connected to the server when it reaches the end of the last log file and continuing to copy new events as they are generated. In continuous-backup operation, [mysqlbinlog](#page-113-1) runs until the connection ends (for example, when the server exits) or [mysqlbinlog](#page-113-1) is forcibly terminated. When the connection ends, [mysqlbinlog](#page-113-1) does not wait and retry the connection, unlike a replica server. To continue a live backup after the server has been restarted, you must also restart [mysqlbinlog](#page-113-1).

![](_page_142_Picture_1.jpeg)

## **Important**

[mysqlbinlog](#page-113-1) can back up both encrypted and unencrypted binary log files . However, copies of encrypted binary log files that are generated using [mysqlbinlog](#page-113-1) are stored in an unencrypted format.

## <span id="page-142-0"></span>**mysqlbinlog Backup Options**

Binary log backup requires that you invoke [mysqlbinlog](#page-113-1) with two options at minimum:

- The [--read-from-remote-server](#page-129-0) (or -R) option tells [mysqlbinlog](#page-113-1) to connect to a server and request its binary log. (This is similar to a replica server connecting to its replication source server.)
- The [--raw](#page-128-0) option tells [mysqlbinlog](#page-113-1) to write raw (binary) output, not text output.

Along with [--read-from-remote-server](#page-129-0), it is common to specify other options: [--host](#page-124-0) indicates where the server is running, and you may also need to specify connection options such as [--user](#page-135-0) and [--password](#page-126-0).

Several other options are useful in conjunction with [--raw](#page-128-0):

- [--stop-never](#page-133-3): Stay connected to the server after reaching the end of the last log file and continue to read new events.
- [--connection-server-id=](#page-120-0)id: The server ID that [mysqlbinlog](#page-113-1) reports when it connects to a server. When [--stop-never](#page-133-3) is used, the default reported server ID is 1. If this causes a conflict with the ID of a replica server or another [mysqlbinlog](#page-113-1) process, use [--connection-server-id](#page-120-0) to specify an alternative server ID. See [Section 6.6.9.4, "Specifying the mysqlbinlog Server ID".](#page-144-0)
- [--result-file](#page-129-2): A prefix for output file names, as described later.

## <span id="page-142-1"></span>**Static and Live Backups**

To back up a server's binary log files with [mysqlbinlog](#page-113-1), you must specify file names that actually exist on the server. If you do not know the names, connect to the server and use the SHOW BINARY LOGS statement to see the current names. Suppose that the statement produces this output:

```
mysql> SHOW BINARY LOGS;
+---------------+-----------+-----------+
| Log_name | File_size | Encrypted |
+---------------+-----------+-----------+
| binlog.000130 | 27459 | No |
| binlog.000131 | 13719 | No |
| binlog.000132 | 43268 | No |
+---------------+-----------+-----------+
```

With that information, you can use [mysqlbinlog](#page-113-1) to back up the binary log to the current directory as follows (enter each command on a single line):

• To make a static backup of binlog.000130 through binlog.000132, use either of these commands:

```
mysqlbinlog --read-from-remote-server --host=host_name --raw
 binlog.000130 binlog.000131 binlog.000132
mysqlbinlog --read-from-remote-server --host=host_name --raw
 --to-last-log binlog.000130
```

The first command specifies every file name explicitly. The second names only the first file and uses [--to-last-log](#page-135-3) to read through the last. A difference between these commands is that if the server happens to open binlog.000133 before [mysqlbinlog](#page-113-1) reaches the end of binlog.000132, the first command does not read it, but the second command does.

• To make a live backup in which [mysqlbinlog](#page-113-1) starts with binlog.000130 to copy existing log files, then stays connected to copy new events as the server generates them:

```
mysqlbinlog --read-from-remote-server --host=host_name --raw
 --stop-never binlog.000130
```

With [--stop-never](#page-133-3), it is not necessary to specify [--to-last-log](#page-135-3) to read to the last log file because that option is implied.

## <span id="page-143-0"></span>**Output File Naming**

Without [--raw](#page-128-0), [mysqlbinlog](#page-113-1) produces text output and the [--result-file](#page-129-2) option, if given, specifies the name of the single file to which all output is written. With [--raw](#page-128-0), [mysqlbinlog](#page-113-1) writes one binary output file for each log file transferred from the server. By default, [mysqlbinlog](#page-113-1) writes the files in the current directory with the same names as the original log files. To modify the output file names, use the [--result-file](#page-129-2) option. In conjunction with [--raw](#page-128-0), the [--result-file](#page-129-2) option value is treated as a prefix that modifies the output file names.

Suppose that a server currently has binary log files named binlog.000999 and up. If you use [mysqlbinlog --raw](#page-113-1) to back up the files, the [--result-file](#page-129-2) option produces output file names as shown in the following table. You can write the files to a specific directory by beginning the [--result](#page-129-2)[file](#page-129-2) value with the directory path. If the [--result-file](#page-129-2) value consists only of a directory name, the value must end with the pathname separator character. Output files are overwritten if they exist.

| result-file Option | Output File Names          |
|--------------------|----------------------------|
| result-file=x      | xbinlog.000999 and up      |
| result-file=/tmp/  | /tmp/binlog.000999 and up  |
| result-file=/tmp/x | /tmp/xbinlog.000999 and up |

## <span id="page-143-1"></span>**Example: mysqldump + mysqlbinlog for Backup and Restore**

The following example describes a simple scenario that shows how to use mysqldump and [mysqlbinlog](#page-113-1) together to back up a server's data and binary log, and how to use the backup to restore the server if data loss occurs. The example assumes that the server is running on host host\_name and its first binary log file is named binlog.000999. Enter each command on a single line.

Use [mysqlbinlog](#page-113-1) to make a continuous backup of the binary log:

```
mysqlbinlog --read-from-remote-server --host=host_name --raw
 --stop-never binlog.000999
```

Use mysqldump to create a dump file as a snapshot of the server's data. Use --all-databases, - events, and --routines to back up all data, and --master-data=2 to include the current binary log coordinates in the dump file.

```
mysqldump --host=host_name --all-databases --events --routines --master-data=2> dump_file
```

Execute the mysqldump command periodically to create newer snapshots as desired.

If data loss occurs (for example, if the server unexpectedly exits), use the most recent dump file to restore the data:

```
mysql --host=host_name -u root -p < dump_file
```

Then use the binary log backup to re-execute events that were written after the coordinates listed in the dump file. Suppose that the coordinates in the file look like this:

```
-- CHANGE MASTER TO MASTER_LOG_FILE='binlog.001002', MASTER_LOG_POS=27284;
```

If the most recent backed-up log file is named binlog.001004, re-execute the log events like this:

```
mysqlbinlog --start-position=27284 binlog.001002 binlog.001003 binlog.001004
 | mysql --host=host_name -u root -p
```

You might find it easier to copy the backup files (dump file and binary log files) to the server host to make it easier to perform the restore operation, or if MySQL does not allow remote root access.

## <span id="page-144-1"></span>**mysqlbinlog Backup Restrictions**

Binary log backups with [mysqlbinlog](#page-113-1) are subject to these restrictions:

- [mysqlbinlog](#page-113-1) does not automatically reconnect to the MySQL server if the connection is lost (for example, if a server restart occurs or there is a network outage).
- The delay for a backup is similar to the delay for a replica server.

## <span id="page-144-0"></span>**6.6.9.4 Specifying the mysqlbinlog Server ID**

When invoked with the --read-from-remote-server option, [mysqlbinlog](#page-113-1) connects to a MySQL server, specifies a server ID to identify itself, and requests binary log files from the server. You can use [mysqlbinlog](#page-113-1) to request log files from a server in several ways:

- Specify an explicitly named set of files: For each file, [mysqlbinlog](#page-113-1) connects and issues a Binlog dump command. The server sends the file and disconnects. There is one connection per file.
- Specify the beginning file and [--to-last-log](#page-135-3): [mysqlbinlog](#page-113-1) connects and issues a Binlog dump command for all files. The server sends all files and disconnects.
- Specify the beginning file and [--stop-never](#page-133-3) (which implies [--to-last-log](#page-135-3)): [mysqlbinlog](#page-113-1) connects and issues a Binlog dump command for all files. The server sends all files, but does not disconnect after sending the last one.

With [--read-from-remote-server](#page-129-0) only, [mysqlbinlog](#page-113-1) connects using a server ID of 0, which tells the server to disconnect after sending the last requested log file.

With [--read-from-remote-server](#page-129-0) and [--stop-never](#page-133-3), [mysqlbinlog](#page-113-1) connects using a nonzero server ID, so the server does not disconnect after sending the last log file. The server ID is 1 by default, but this can be changed with [--connection-server-id](#page-120-0).

Thus, for the first two ways of requesting files, the server disconnects because [mysqlbinlog](#page-113-1) specifies a server ID of 0. It does not disconnect if [--stop-never](#page-133-3) is given because [mysqlbinlog](#page-113-1) specifies a nonzero server ID.

## <span id="page-144-2"></span>**6.6.10 mysqldumpslow — Summarize Slow Query Log Files**

The MySQL slow query log contains information about queries that take a long time to execute (see Section 7.4.5, "The Slow Query Log"). [mysqldumpslow](#page-144-2) parses MySQL slow query log files and summarizes their contents.

Normally, [mysqldumpslow](#page-144-2) groups queries that are similar except for the particular values of number and string data values. It "abstracts" these values to N and 'S' when displaying summary output. To modify value abstracting behavior, use the -a and -n options.

Invoke [mysqldumpslow](#page-144-2) like this:

```
mysqldumpslow [options] [log_file ...]
```

#### Example output with no options given:

```
Reading mysql slow query log from /usr/local/mysql/data/mysqld80-slow.log
Count: 1 Time=4.32s (4s) Lock=0.00s (0s) Rows=0.0 (0), root[root]@localhost
 insert into t2 select * from t1
Count: 3 Time=2.53s (7s) Lock=0.00s (0s) Rows=0.0 (0), root[root]@localhost
 insert into t2 select * from t1 limit N
Count: 3 Time=2.13s (6s) Lock=0.00s (0s) Rows=0.0 (0), root[root]@localhost
 insert into t1 select * from t1
```

[mysqldumpslow](#page-144-2) supports the following options.

## **Table 6.24 mysqldumpslow Options**

| Option Name | Description                                         |
|-------------|-----------------------------------------------------|
| -a          | Do not abstract all numbers to N and strings to 'S' |
| -n          | Abstract numbers with at least the specified digits |
| debug       | Write debugging information                         |
| -g          | Only consider statements that match the pattern     |
| help        | Display help message and exit                       |
| -h          | Host name of the server in the log file name        |
| -i          | Name of the server instance                         |
| -l          | Do not subtract lock time from total time           |
| -r          | Reverse the sort order                              |
| -s          | How to sort output                                  |
| -t          | Display only first num queries                      |
| verbose     | Verbose mode                                        |

### <span id="page-145-3"></span>• [--help](#page-145-3)

| Command-Line Format | help |
|---------------------|------|
|---------------------|------|

Display a help message and exit.

<span id="page-145-0"></span>• -a

Do not abstract all numbers to N and strings to 'S'.

<span id="page-145-1"></span>• [--debug](#page-145-1), -d

| Command-Line Format | debug |
|---------------------|-------|
|---------------------|-------|

Run in debug mode.

This option is available only if MySQL was built using WITH\_DEBUG. MySQL release binaries provided by Oracle are not built using this option.

<span id="page-145-2"></span>• -g pattern

| Type | String |
|------|--------|
|------|--------|

Consider only queries that match the (grep-style) pattern.

<span id="page-145-4"></span>• -h host\_name

| Type          | String |
|---------------|--------|
| Default Value | *      |

Host name of MySQL server for \*-slow.log file name. The value can contain a wildcard. The default is \* (match all).

<span id="page-145-5"></span>• -i name

| Type | String |
|------|--------|
|      |        |

Name of server instance (if using mysql.server startup script).

<span id="page-146-1"></span>• -l

Do not subtract lock time from total time.

<span id="page-146-0"></span>• -n N

| Type | Numeric |
|------|---------|

Abstract numbers with at least N digits within names.

<span id="page-146-2"></span>• -r

Reverse the sort order.

<span id="page-146-3"></span>• -s sort\_type

| Type          | String |
|---------------|--------|
| Default Value | at     |

How to sort the output. The value of sort\_type should be chosen from the following list:

- t, at: Sort by query time or average query time
- l, al: Sort by lock time or average lock time
- r, ar: Sort by rows sent or average rows sent
- c: Sort by count

By default, [mysqldumpslow](#page-144-2) sorts by average query time (equivalent to -s at).

<span id="page-146-4"></span>• -t N

| Type | Numeric |
|------|---------|
|------|---------|

Display only the first N queries in the output.

<span id="page-146-5"></span>• [--verbose](#page-146-5), -v

| Command-Line Format | verbose |
|---------------------|---------|

Verbose mode. Print more information about what the program does.