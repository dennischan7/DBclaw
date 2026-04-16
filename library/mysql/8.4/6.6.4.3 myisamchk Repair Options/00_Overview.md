---
source: MySQL 8.4 Reference
title: 00_Overview
---

[myisamchk](#page-150-4) supports the following options for table repair operations (operations performed when an option such as [--recover](#page-160-2) or [--safe-recover](#page-160-3) is given):

<span id="page-159-0"></span>• [--backup](#page-159-0), -B

| Command-Line Format | backup |
|---------------------|--------|
|---------------------|--------|

Make a backup of the .MYD file as file\_name-time.BAK

<span id="page-159-1"></span>• [--character-sets-dir=](#page-159-1)dir\_name

| Command-Line Format | character-sets-dir=path |
|---------------------|-------------------------|
| Type                | String                  |
| Default Value       | [none]                  |

The directory where character sets are installed. See Section 12.15, "Character Set Configuration".

<span id="page-159-2"></span>• [--correct-checksum](#page-159-2)

| Command-Line Format | correct-checksum |
|---------------------|------------------|
|---------------------|------------------|

Correct the checksum information for the table.

<span id="page-159-3"></span>• [--data-file-length=](#page-159-3)len, -D len

| Command-Line Format | data-file-length=len |
|---------------------|----------------------|
| Type                | Numeric              |

The maximum length of the data file (when re-creating data file when it is "full").

• [--extend-check](#page-157-2), -e

| Command-Line Format | extend-check |
|---------------------|--------------|
|---------------------|--------------|

Do a repair that tries to recover every possible row from the data file. Normally, this also finds a lot of garbage rows. Do not use this option unless you are desperate.

See also the description of this option under table checking options.

For a description of the output format, see [Section 6.6.4.5, "Obtaining Table Information with](#page-162-2) [myisamchk"](#page-162-2).

• [--force](#page-158-1), -f

| Command-Line Format | force |
|---------------------|-------|
|                     |       |

Overwrite old intermediate files (files with names like tbl\_name.TMD) instead of aborting.

<span id="page-159-4"></span>• [--keys-used=](#page-159-4)val, -k val

| Command-Line Format | keys-used=val |
|---------------------|---------------|
| Type                | Numeric       |

For [myisamchk](#page-150-4), the option value is a bit value that indicates which indexes to update. Each binary bit of the option value corresponds to a table index, where the first index is bit 0. An option value of 0 disables updates to all indexes, which can be used to get faster inserts. Deactivated indexes can be reactivated by using [myisamchk -r](#page-150-4).

## <span id="page-160-0"></span>• [--max-record-length=](#page-160-0)len

| Command-Line Format | max-record-length=len |
|---------------------|-----------------------|
| Type                | Numeric               |

Skip rows larger than the given length if [myisamchk](#page-150-4) cannot allocate memory to hold them.

## <span id="page-160-1"></span>• [--quick](#page-160-1), -q

| Command-Line Format | quick |
|---------------------|-------|
|---------------------|-------|

Achieve a faster repair by modifying only the index file, not the data file. You can specify this option twice to force [myisamchk](#page-150-4) to modify the original data file in case of duplicate keys.

## <span id="page-160-2"></span>• [--recover](#page-160-2), -r

| Command-Line Format | recover |
|---------------------|---------|
|---------------------|---------|

Do a repair that can fix almost any problem except unique keys that are not unique (which is an extremely unlikely error with MyISAM tables). If you want to recover a table, this is the option to try first. You should try [--safe-recover](#page-160-3) only if [myisamchk](#page-150-4) reports that the table cannot be recovered using [--recover](#page-160-2). (In the unlikely case that [--recover](#page-160-2) fails, the data file remains intact.)

If you have lots of memory, you should increase the value of myisam\_sort\_buffer\_size.

## <span id="page-160-3"></span>• [--safe-recover](#page-160-3), -o

| Command-Line Format<br>safe-recover |
|-------------------------------------|
|-------------------------------------|

Do a repair using an old recovery method that reads through all rows in order and updates all index trees based on the rows found. This is an order of magnitude slower than [--recover](#page-160-2), but can handle a couple of very unlikely cases that [--recover](#page-160-2) cannot. This recovery method also uses much less disk space than [--recover](#page-160-2). Normally, you should repair first using [--recover](#page-160-2), and then with [--safe-recover](#page-160-3) only if [--recover](#page-160-2) fails.

If you have lots of memory, you should increase the value of key\_buffer\_size.

# <span id="page-160-4"></span>• [--set-collation=](#page-160-4)name

| Command-Line Format | set-collation=name |
|---------------------|--------------------|
| Type                | String             |

Specify the collation to use for sorting table indexes. The character set name is implied by the first part of the collation name.

<span id="page-161-4"></span>• [--sort-recover](#page-161-4), -n

| Command-Line Format | sort-recover |
|---------------------|--------------|

Force [myisamchk](#page-150-4) to use sorting to resolve the keys even if the temporary files would be very large.

<span id="page-161-5"></span>• [--tmpdir=](#page-161-5)dir\_name, -t dir\_name

| Command-Line Format | tmpdir=dir_name |
|---------------------|-----------------|
| Type                | Directory name  |

The path of the directory to be used for storing temporary files. If this is not set, [myisamchk](#page-150-4) uses the value of the TMPDIR environment variable. [--tmpdir](#page-161-5) can be set to a list of directory paths that are used successively in round-robin fashion for creating temporary files. The separator character between directory names is the colon (:) on Unix and the semicolon (;) on Windows.

<span id="page-161-6"></span>• [--unpack](#page-161-6), -u

| Command-Line Format | unpack |
|---------------------|--------|
|---------------------|--------|

Unpack a table that was packed with [myisampack](#page-170-0).

# <span id="page-161-0"></span>**6.6.4.4 Other myisamchk Options**

[myisamchk](#page-150-4) supports the following options for actions other than table checks and repairs:

• [--analyze](#page-161-0), -a

| Command-Line Format | analyze |
|---------------------|---------|
|---------------------|---------|

Analyze the distribution of key values. This improves join performance by enabling the join optimizer to better choose the order in which to join the tables and which indexes it should use. To obtain information about the key distribution, use a [myisamchk --description --verbose](#page-150-4) [tbl\\_name](#page-150-4) command or the SHOW INDEX FROM tbl\_name statement.

<span id="page-161-1"></span>• [--block-search=](#page-161-1)offset, -b offset

| Command-Line Format | block-search=offset |
|---------------------|---------------------|
| Type                | Numeric             |

Find the record that a block at the given offset belongs to.

<span id="page-161-2"></span>• [--description](#page-161-2), -d

<span id="page-161-3"></span>

| Command-Line Format | description |
|---------------------|-------------|
|---------------------|-------------|

AUTO\_INCREMENT numbers for new records begin with the largest value currently in the table, plus one.

<span id="page-162-0"></span>• [--sort-index](#page-162-0), -S

| Command-Line Format | sort-index |
|---------------------|------------|
|---------------------|------------|

Sort the index tree blocks in high-low order. This optimizes seeks and makes table scans that use indexes faster.

<span id="page-162-1"></span>• [--sort-records=](#page-162-1)N, -R N

| Command-Line Format | sort-records=# |
|---------------------|----------------|
| Type                | Numeric        |

Sort records according to a particular index. This makes your data much more localized and may speed up range-based SELECT and ORDER BY operations that use this index. (The first time you use this option to sort a table, it may be very slow.) To determine a table's index numbers, use SHOW INDEX, which displays a table's indexes in the same order that [myisamchk](#page-150-4) sees them. Indexes are numbered beginning with 1.

If keys are not packed (PACK\_KEYS=0), they have the same length, so when [myisamchk](#page-150-4) sorts and moves records, it just overwrites record offsets in the index. If keys are packed (PACK\_KEYS=1), [myisamchk](#page-150-4) must unpack key blocks first, then re-create indexes and pack the key blocks again. (In this case, re-creating indexes is faster than updating offsets for each index.)

# <span id="page-162-2"></span>**6.6.4.5 Obtaining Table Information with myisamchk**

To obtain a description of a MyISAM table or statistics about it, use the commands shown here. The output from these commands is explained later in this section.

• [myisamchk -d](#page-150-4) tbl\_name

Runs [myisamchk](#page-150-4) in "describe mode" to produce a description of your table. If you start the MySQL server with external locking disabled, [myisamchk](#page-150-4) may report an error for a table that is updated while it runs. However, because [myisamchk](#page-150-4) does not change the table in describe mode, there is no risk of destroying data.

• [myisamchk -dv](#page-150-4) tbl\_name

Adding -v runs [myisamchk](#page-150-4) in verbose mode so that it produces more information about the table. Adding -v a second time produces even more information.

• [myisamchk -eis](#page-150-4) tbl\_name

Shows only the most important information from a table. This operation is slow because it must read the entire table.

• [myisamchk -eiv](#page-150-4) tbl\_name

This is like -eis, but tells you what is being done.

The tbl\_name argument can be either the name of a MyISAM table or the name of its index file, as described in [Section 6.6.4, "myisamchk — MyISAM Table-Maintenance Utility"](#page-150-4). Multiple tbl\_name arguments can be given.

Suppose that a table named person has the following structure. (The MAX\_ROWS table option is included so that in the example output from [myisamchk](#page-150-4) shown later, some values are smaller and fit the output format more easily.)

```
CREATE TABLE person
(
 id INT NOT NULL AUTO_INCREMENT,
 last_name VARCHAR(20) NOT NULL,
 first_name VARCHAR(20) NOT NULL,
 birth DATE,
 death DATE,
 PRIMARY KEY (id),
 INDEX (last_name, first_name),
 INDEX (birth)
) MAX_ROWS = 1000000 ENGINE=MYISAM;
```

Suppose also that the table has these data and index file sizes:

```
-rw-rw---- 1 mysql mysql 9347072 Aug 19 11:47 person.MYD
-rw-rw---- 1 mysql mysql 6066176 Aug 19 11:47 person.MYI
```

## Example of [myisamchk -dvv](#page-150-4) output:

```
MyISAM file: person
Record format: Packed
Character set: utf8mb4_0900_ai_ci (255)
File-version: 1
Creation time: 2017-03-30 21:21:30
Status: checked,analyzed,optimized keys,sorted index pages
Auto increment key: 1 Last value: 306688
Data records: 306688 Deleted blocks: 0
Datafile parts: 306688 Deleted data: 0
Datafile pointer (bytes): 4 Keyfile pointer (bytes): 3
Datafile length: 9347072 Keyfile length: 6066176
Max datafile length: 4294967294 Max keyfile length: 17179868159
Recordlength: 54
table description:
Key Start Len Index Type Rec/key Root Blocksize
1 2 4 unique long 1 1024
2 6 80 multip. varchar prefix 0 1024
 87 80 varchar 0
3 168 3 multip. uint24 NULL 0 1024
Field Start Length Nullpos Nullbit Type
1 1 1
2 2 4 no zeros
3 6 81 varchar
4 87 81 varchar
5 168 3 1 1 no zeros
6 171 3 1 2 no zeros
```

Explanations for the types of information [myisamchk](#page-150-4) produces are given here. "Keyfile" refers to the index file. "Record" and "row" are synonymous, as are "field" and "column."

The initial part of the table description contains these values:

• MyISAM file

Name of the MyISAM (index) file.

• Record format

The format used to store table rows. The preceding examples use Fixed length. Other possible values are Compressed and Packed. (Packed corresponds to what SHOW TABLE STATUS reports as Dynamic.)

• Chararacter set

The table default character set.

• File-version

Version of MyISAM format. Always 1.

• Creation time

When the data file was created.

• Recover time

When the index/data file was last reconstructed.

• Status

Table status flags. Possible values are crashed, open, changed, analyzed, optimized keys, and sorted index pages.

• Auto increment key, Last value

The key number associated the table's AUTO\_INCREMENT column, and the most recently generated value for this column. These fields do not appear if there is no such column.

• Data records

The number of rows in the table.

• Deleted blocks

How many deleted blocks still have reserved space. You can optimize your table to minimize this space. See Section 9.6.4, "MyISAM Table Optimization".

• Datafile parts

For dynamic-row format, this indicates how many data blocks there are. For an optimized table without fragmented rows, this is the same as Data records.

• Deleted data

How many bytes of unreclaimed deleted data there are. You can optimize your table to minimize this space. See Section 9.6.4, "MyISAM Table Optimization".

• Datafile pointer

The size of the data file pointer, in bytes. It is usually 2, 3, 4, or 5 bytes. Most tables manage with 2 bytes, but this cannot be controlled from MySQL yet. For fixed tables, this is a row address. For dynamic tables, this is a byte address.

• Keyfile pointer

The size of the index file pointer, in bytes. It is usually 1, 2, or 3 bytes. Most tables manage with 2 bytes, but this is calculated automatically by MySQL. It is always a block address.

• Max datafile length

How long the table data file can become, in bytes.

• Max keyfile length

How long the table index file can become, in bytes.

• Recordlength

How much space each row takes, in bytes.

The table description part of the output includes a list of all keys in the table. For each key, [myisamchk](#page-150-4) displays some low-level information:

## • Key

This key's number. This value is shown only for the first column of the key. If this value is missing, the line corresponds to the second or later column of a multiple-column key. For the table shown in the example, there are two table description lines for the second index. This indicates that it is a multiple-part index with two parts.

## • Start

Where in the row this portion of the index starts.

## • Len

How long this portion of the index is. For packed numbers, this should always be the full length of the column. For strings, it may be shorter than the full length of the indexed column, because you can index a prefix of a string column. The total length of a multiple-part key is the sum of the Len values for all key parts.

## • Index

Whether a key value can exist multiple times in the index. Possible values are unique or multip. (multiple).

## • Type

What data type this portion of the index has. This is a MyISAM data type with the possible values packed, stripped, or empty.

## • Root

Address of the root index block.

## • Blocksize

The size of each index block. By default this is 1024, but the value may be changed at compile time when MySQL is built from source.

## • Rec/key

This is a statistical value used by the optimizer. It tells how many rows there are per value for this index. A unique index always has a value of 1. This may be updated after a table is loaded (or greatly changed) with [myisamchk -a](#page-150-4). If this is not updated at all, a default value of 30 is given.

The last part of the output provides information about each column:

## • Field

The column number.

## • Start

The byte position of the column within table rows.

## • Length

The length of the column in bytes.

## • Nullpos, Nullbit

For columns that can be NULL, MyISAM stores NULL values as a flag in a byte. Depending on how many nullable columns there are, there can be one or more bytes used for this purpose. The Nullpos and Nullbit values, if nonempty, indicate which byte and bit contains that flag indicating whether the column is NULL.

The position and number of bytes used to store NULL flags is shown in the line for field 1. This is why there are six Field lines for the person table even though it has only five columns.

• Type

The data type. The value may contain any of the following descriptors:

• constant

All rows have the same value.

• no endspace

Do not store endspace.

• no endspace, not\_always

Do not store endspace and do not do endspace compression for all values.

• no endspace, no empty

Do not store endspace. Do not store empty values.

• table-lookup

The column was converted to an ENUM.

• zerofill(N)

The most significant N bytes in the value are always 0 and are not stored.

• no zeros

Do not store zeros.

• always zero

Zero values are stored using one bit.

• Huff tree

The number of the Huffman tree associated with the column.

• Bits

The number of bits used in the Huffman tree.

The Huff tree and Bits fields are displayed if the table has been compressed with [myisampack](#page-170-0). See [Section 6.6.6, "myisampack — Generate Compressed, Read-Only MyISAM Tables"](#page-170-0), for an example of this information.

Example of [myisamchk -eiv](#page-150-4) output:

```
Checking MyISAM file: person
Data records: 306688 Deleted blocks: 0
- check file-size
- check record delete-chain
No recordlinks
- check key delete-chain
block_size 1024:
- check index reference
- check data record references index: 1
Key: 1: Keyblocks used: 98% Packed: 0% Max levels: 3
- check data record references index: 2
```

```
Key: 2: Keyblocks used: 99% Packed: 97% Max levels: 3
- check data record references index: 3
Key: 3: Keyblocks used: 98% Packed: -14% Max levels: 3
Total: Keyblocks used: 98% Packed: 89%
- check records and index references
*** LOTS OF ROW NUMBERS DELETED ***
Records: 306688 M.recordlength: 25 Packed: 83%
Recordspace used: 97% Empty space: 2% Blocks/Record: 1.00
Record blocks: 306688 Delete blocks: 0
Record data: 7934464 Deleted data: 0
Lost space: 256512 Linkdata: 1156096
User time 43.08, System time 1.68
Maximum resident set size 0, Integral resident set size 0
Non-physical pagefaults 0, Physical pagefaults 0, Swaps 0
Blocks in 0 out 7, Messages in 0 out 0, Signals 0
Voluntary context switches 0, Involuntary context switches 0
Maximum memory usage: 1046926 bytes (1023k)
```

[myisamchk -eiv](#page-150-4) output includes the following information:

• Data records

The number of rows in the table.

• Deleted blocks

How many deleted blocks still have reserved space. You can optimize your table to minimize this space. See Section 9.6.4, "MyISAM Table Optimization".

• Key

The key number.

• Keyblocks used

What percentage of the keyblocks are used. When a table has just been reorganized with [myisamchk](#page-150-4), the values are very high (very near theoretical maximum).

• Packed

MySQL tries to pack key values that have a common suffix. This can only be used for indexes on CHAR and VARCHAR columns. For long indexed strings that have similar leftmost parts, this can significantly reduce the space used. In the preceding example, the second key is 40 bytes long and a 97% reduction in space is achieved.

• Max levels

How deep the B-tree for this key is. Large tables with long key values get high values.

• Records

How many rows are in the table.

• M.recordlength

The average row length. This is the exact row length for tables with fixed-length rows, because all rows have the same length.

• Packed

MySQL strips spaces from the end of strings. The Packed value indicates the percentage of savings achieved by doing this.

• Recordspace used

What percentage of the data file is used.

• Empty space

What percentage of the data file is unused.

• Blocks/Record

Average number of blocks per row (that is, how many links a fragmented row is composed of). This is always 1.0 for fixed-format tables. This value should stay as close to 1.0 as possible. If it gets too large, you can reorganize the table. See Section 9.6.4, "MyISAM Table Optimization".

• Recordblocks

How many blocks (links) are used. For fixed-format tables, this is the same as the number of rows.

• Deleteblocks

How many blocks (links) are deleted.

• Recorddata

How many bytes in the data file are used.

• Deleted data

How many bytes in the data file are deleted (unused).

• Lost space

If a row is updated to a shorter length, some space is lost. This is the sum of all such losses, in bytes.

• Linkdata

When the dynamic table format is used, row fragments are linked with pointers (4 to 7 bytes each). Linkdata is the sum of the amount of storage used by all such pointers.

# <span id="page-168-0"></span>**6.6.4.6 myisamchk Memory Usage**

Memory allocation is important when you run [myisamchk](#page-150-4). [myisamchk](#page-150-4) uses no more memory than its memory-related variables are set to. If you are going to use [myisamchk](#page-150-4) on very large tables, you should first decide how much memory you want it to use. The default is to use only about 3MB to perform repairs. By using larger values, you can get [myisamchk](#page-150-4) to operate faster. For example, if you have more than 512MB RAM available, you could use options such as these (in addition to any other options you might specify):

```
myisamchk --myisam_sort_buffer_size=256M \
 --key_buffer_size=512M \
 --read_buffer_size=64M \
 --write_buffer_size=64M ...
```

Using --myisam\_sort\_buffer\_size=16M is probably enough for most cases.

Be aware that [myisamchk](#page-150-4) uses temporary files in TMPDIR. If TMPDIR points to a memory file system, out of memory errors can easily occur. If this happens, run [myisamchk](#page-150-4) with the [--tmpdir=](#page-161-5)dir\_name option to specify a directory located on a file system that has more space.

When performing repair operations, [myisamchk](#page-150-4) also needs a lot of disk space:

• Twice the size of the data file (the original file and a copy). This space is not needed if you do a repair with [--quick](#page-160-1); in this case, only the index file is re-created. This space must be available on the same file system as the original data file, as the copy is created in the same directory as the original.

- Space for the new index file that replaces the old one. The old index file is truncated at the start of the repair operation, so you usually ignore this space. This space must be available on the same file system as the original data file.
- When using [--recover](#page-160-2) or [--sort-recover](#page-161-4) (but not when using [--safe-recover](#page-160-3)), you need space on disk for sorting. This space is allocated in the temporary directory (specified by TMPDIR or [--tmpdir=](#page-161-5)dir\_name). The following formula yields the amount of space required:

```
(largest_key + row_pointer_length) * number_of_rows * 2
```

You can check the length of the keys and the row\_pointer\_length with [myisamchk](#page-150-4)  dv [tbl\\_name](#page-150-4) (see [Section 6.6.4.5, "Obtaining Table Information with myisamchk"\)](#page-162-2). The row\_pointer\_length and number\_of\_rows values are the Datafile pointer and Data records values in the table description. To determine the largest\_key value, check the Key lines in the table description. The Len column indicates the number of bytes for each key part. For a multiple-column index, the key size is the sum of the Len values for all key parts.

If you have a problem with disk space during repair, you can try [--safe-recover](#page-160-3) instead of [-](#page-160-2) [recover](#page-160-2).

# <span id="page-169-0"></span>**6.6.5 myisamlog — Display MyISAM Log File Contents**

[myisamlog](#page-169-0) processes the contents of a MyISAM log file. To create such a file, start the server with a --log-isam=log\_file option.

Invoke [myisamlog](#page-169-0) like this:

```
myisamlog [options] [file_name [tbl_name] ...]
```

The default operation is update (-u). If a recovery is done (-r), all writes and possibly updates and deletes are done and errors are only counted. The default log file name is myisam.log if no log\_file argument is given. If tables are named on the command line, only those tables are updated.

[myisamlog](#page-169-0) supports the following options:

• -?, -I

Display a help message and exit.

• -c N

Execute only N commands.

• -f N

Specify the maximum number of open files.

• -F filepath/

Specify the file path with a trailing slash.

• -i

Display extra information before exiting.

• -o offset

Specify the starting offset.

• -p N

Remove N components from path.

• -r

Perform a recovery operation.

• -R record\_pos\_file record\_pos

Specify record position file and record position.

• -u

Perform an update operation.

• -v

Verbose mode. Print more output about what the program does. This option can be given multiple times to produce more and more output.

• -w write\_file

Specify the write file.

• -V

Display version information.

# <span id="page-170-0"></span>**6.6.6 myisampack — Generate Compressed, Read-Only MyISAM Tables**

The [myisampack](#page-170-0) utility compresses MyISAM tables. [myisampack](#page-170-0) works by compressing each column in the table separately. Usually, [myisampack](#page-170-0) packs the data file 40% to 70%.

When the table is used later, the server reads into memory the information needed to decompress columns. This results in much better performance when accessing individual rows, because you only have to uncompress exactly one row.

MySQL uses mmap() when possible to perform memory mapping on compressed tables. If mmap() does not work, MySQL falls back to normal read/write file operations.

Please note the following:

- If the mysqld server was invoked with external locking disabled, it is not a good idea to invoke [myisampack](#page-170-0) if the table might be updated by the server during the packing process. It is safest to compress tables with the server stopped.
- After packing a table, it becomes read only. This is generally intended (such as when accessing packed tables on a CD).
- [myisampack](#page-170-0) does not support partitioned tables.

Invoke [myisampack](#page-170-0) like this:

```
myisampack [options] file_name ...
```

Each file name argument should be the name of an index (.MYI) file. If you are not in the database directory, you should specify the path name to the file. It is permissible to omit the .MYI extension.

After you compress a table with [myisampack](#page-170-0), use [myisamchk -rq](#page-150-4) to rebuild its indexes. [Section 6.6.4, "myisamchk — MyISAM Table-Maintenance Utility".](#page-150-4)

[myisampack](#page-170-0) supports the following options. It also reads option files and supports the options for processing them described at Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-170-1"></span>• [--help](#page-170-1), -?

| Command-Line Format | help |
|---------------------|------|

Display a help message and exit.

<span id="page-171-0"></span>• [--backup](#page-171-0), -b

| Command-Line Format | backup |
|---------------------|--------|
|                     |        |

Make a backup of each table's data file using the name tbl\_name.OLD.

<span id="page-171-1"></span>• [--character-sets-dir=](#page-171-1)dir\_name

| Command-Line Format | character-sets-dir=dir_name |
|---------------------|-----------------------------|
| Type                | Directory name              |

The directory where character sets are installed. See Section 12.15, "Character Set Configuration".

<span id="page-171-2"></span>• --debug[=[debug\\_options](#page-171-2)], -# [debug\_options]

| Command-Line Format<br>debug[=debug_options] |        |  |  |
|----------------------------------------------|--------|--|--|
| Type                                         | String |  |  |
| Default Value                                | d:t:o  |  |  |

Write a debugging log. A typical debug\_options string is d:t:o,file\_name. The default is d:t:o.

This option is available only if MySQL was built using WITH\_DEBUG. MySQL release binaries provided by Oracle are not built using this option.

<span id="page-171-3"></span>• [--force](#page-171-3), -f

| Command-Line Format<br>force |  |  |
|------------------------------|--|--|
|------------------------------|--|--|

Produce a packed table even if it becomes larger than the original or if the intermediate file from an earlier invocation of [myisampack](#page-170-0) exists. ([myisampack](#page-170-0) creates an intermediate file named tbl\_name.TMD in the database directory while it compresses the table. If you kill [myisampack](#page-170-0), the .TMD file might not be deleted.) Normally, [myisampack](#page-170-0) exits with an error if it finds that tbl\_name.TMD exists. With [--force](#page-171-3), [myisampack](#page-170-0) packs the table anyway.

<span id="page-171-4"></span>• --join=[big\\_tbl\\_name](#page-171-4), -j big\_tbl\_name

| Command-Line Format | join=big_tbl_name |  |  |
|---------------------|-------------------|--|--|
| Type                | String            |  |  |

Join all tables named on the command line into a single packed table big\_tbl\_name. All tables that are to be combined must have identical structure (same column names and types, same indexes, and so forth).

big\_tbl\_name must not exist prior to the join operation. All source tables named on the command line to be merged into big\_tbl\_name must exist. The source tables are read for the join operation but not modified.

<span id="page-171-5"></span>• [--silent](#page-171-5), -s

| Command-Line Format<br>silent |
|-------------------------------|
|-------------------------------|

Silent mode. Write output only when errors occur.

<span id="page-172-0"></span>• [--test](#page-172-0), -t

| Command-Line Format | test |
|---------------------|------|
|---------------------|------|

Do not actually pack the table, just test packing it.

<span id="page-172-1"></span>• [--tmpdir=](#page-172-1)dir\_name, -T dir\_name

| Command-Line Format | tmpdir=dir_name |  |
|---------------------|-----------------|--|
| Type                | Directory name  |  |

Use the named directory as the location where [myisampack](#page-170-0) creates temporary files.

<span id="page-172-2"></span>• [--verbose](#page-172-2), -v

| Command-Line Format | verbose |
|---------------------|---------|

Verbose mode. Write information about the progress of the packing operation and its result.

<span id="page-172-3"></span>• [--version](#page-172-3), -V

| Command-Line Format | version |
|---------------------|---------|
|---------------------|---------|

Display version information and exit.

<span id="page-172-4"></span>• [--wait](#page-172-4), -w

| Command-Line Format | wait |
|---------------------|------|
|---------------------|------|

Wait and retry if the table is in use. If the mysqld server was invoked with external locking disabled, it is not a good idea to invoke [myisampack](#page-170-0) if the table might be updated by the server during the packing process.

The following sequence of commands illustrates a typical table compression session:

```
$> ls -l station.*
-rw-rw-r-- 1 jones my 994128 Apr 17 19:00 station.MYD
-rw-rw-r-- 1 jones my 53248 Apr 17 19:00 station.MYI
$> myisamchk -dvv station
MyISAM file: station
Isam-version: 2
Creation time: 1996-03-13 10:08:58
Recover time: 1997-02-02 3:06:43
Data records: 1192 Deleted blocks: 0
Datafile parts: 1192 Deleted data: 0
Datafile pointer (bytes): 2 Keyfile pointer (bytes): 2
Max datafile length: 54657023 Max keyfile length: 33554431
Recordlength: 834
Record format: Fixed length
table description:
Key Start Len Index Type Root Blocksize Rec/key
1 2 4 unique unsigned long 1024 1024 1
```

```
2 32 30 multip. text 10240 1024 1
Field Start Length Type
1 1 1
2 2 4
3 6 4
4 10 1
5 11 20
6 31 1
7 32 30
8 62 35
9 97 35
10 132 35
11 167 4
12 171 16
13 187 35
14 222 4
15 226 16
16 242 20
17 262 20
18 282 20
19 302 30
20 332 4
21 336 4
22 340 1
23 341 8
24 349 8
25 357 8
26 365 2
27 367 2
28 369 4
29 373 4
30 377 1
31 378 2
32 380 8
33 388 4
34 392 4
35 396 4
36 400 4
37 404 1
38 405 4
39 409 4
40 413 4
41 417 4
42 421 4
43 425 4
44 429 20
45 449 30
46 479 1
47 480 1
48 481 79
49 560 79
50 639 79
51 718 79
52 797 8
53 805 1
54 806 1
55 807 20
56 827 4
57 831 4
$> myisampack station.MYI
Compressing station.MYI: (1192 records)
- Calculating statistics
normal: 20 empty-space: 16 empty-zero: 12 empty-fill: 11
pre-space: 0 end-space: 12 table-lookups: 5 zero: 7
Original trees: 57 After join: 17
- Compressing file
87.14%
Remember to run myisamchk -rq on compressed tables
```

```
$> myisamchk -rq station
- check record delete-chain
- recovering (with sort) MyISAM-table 'station'
Data records: 1192
- Fixing index 1
- Fixing index 2
$> mysqladmin -uroot flush-tables
$> ls -l station.*
-rw-rw-r-- 1 jones my 127874 Apr 17 19:00 station.MYD
-rw-rw-r-- 1 jones my 55296 Apr 17 19:04 station.MYI
$> myisamchk -dvv station
MyISAM file: station
Isam-version: 2
Creation time: 1996-03-13 10:08:58
Recover time: 1997-04-17 19:04:26
Data records: 1192 Deleted blocks: 0
Datafile parts: 1192 Deleted data: 0
Datafile pointer (bytes): 3 Keyfile pointer (bytes): 1
Max datafile length: 16777215 Max keyfile length: 131071
Recordlength: 834
Record format: Compressed
table description:
Key Start Len Index Type Root Blocksize Rec/key
1 2 4 unique unsigned long 10240 1024 1
2 32 30 multip. text 54272 1024 1
Field Start Length Type Huff tree Bits
1 1 1 constant 1 0
2 2 4 zerofill(1) 2 9
3 6 4 no zeros, zerofill(1) 2 9
4 10 1 3 9
5 11 20 table-lookup 4 0
6 31 1 3 9
7 32 30 no endspace, not_always 5 9
8 62 35 no endspace, not_always, no empty 6 9
9 97 35 no empty 7 9
10 132 35 no endspace, not_always, no empty 6 9
11 167 4 zerofill(1) 2 9
12 171 16 no endspace, not_always, no empty 5 9
13 187 35 no endspace, not_always, no empty 6 9
14 222 4 zerofill(1) 2 9
15 226 16 no endspace, not_always, no empty 5 9
16 242 20 no endspace, not_always 8 9
17 262 20 no endspace, no empty 8 9
18 282 20 no endspace, no empty 5 9
19 302 30 no endspace, no empty 6 9
20 332 4 always zero 2 9
21 336 4 always zero 2 9
22 340 1 3 9
23 341 8 table-lookup 9 0
24 349 8 table-lookup 10 0
25 357 8 always zero 2 9
26 365 2 2 9
27 367 2 no zeros, zerofill(1) 2 9
28 369 4 no zeros, zerofill(1) 2 9
29 373 4 table-lookup 11 0
30 377 1 3 9
31 378 2 no zeros, zerofill(1) 2 9
32 380 8 no zeros 2 9
33 388 4 always zero 2 9
34 392 4 table-lookup 12 0
35 396 4 no zeros, zerofill(1) 13 9
36 400 4 no zeros, zerofill(1) 2 9
37 404 1 2 9
38 405 4 no zeros 2 9
39 409 4 always zero 2 9
40 413 4 no zeros 2 9
```

| 41 | 417 | 4  | always zero           | 2  | 9 |
|----|-----|----|-----------------------|----|---|
| 42 | 421 | 4  | no zeros              | 2  | 9 |
| 43 | 425 | 4  | always zero           | 2  | 9 |
| 44 | 429 | 20 | no empty              | 3  | 9 |
| 45 | 449 | 30 | no empty              | 3  | 9 |
| 46 | 479 | 1  |                       | 14 | 4 |
| 47 | 480 | 1  |                       | 14 | 4 |
| 48 | 481 | 79 | no endspace, no empty | 15 | 9 |
| 49 | 560 | 79 | no empty              | 2  | 9 |
| 50 | 639 | 79 | no empty              | 2  | 9 |
| 51 | 718 | 79 | no endspace           | 16 | 9 |
| 52 | 797 | 8  | no empty              | 2  | 9 |
| 53 | 805 | 1  |                       | 17 | 1 |
| 54 | 806 | 1  |                       | 3  | 9 |
| 55 | 807 | 20 | no empty              | 3  | 9 |
| 56 | 827 | 4  | no zeros, zerofill(2) | 2  | 9 |
| 57 | 831 | 4  | no zeros, zerofill(1) | 2  | 9 |
|    |     |    |                       |    |   |

[myisampack](#page-170-0) displays the following kinds of information:

• normal

The number of columns for which no extra packing is used.

• empty-space

The number of columns containing values that are only spaces. These occupy one bit.

• empty-zero

The number of columns containing values that are only binary zeros. These occupy one bit.

• empty-fill

The number of integer columns that do not occupy the full byte range of their type. These are changed to a smaller type. For example, a BIGINT column (eight bytes) can be stored as a TINYINT column (one byte) if all its values are in the range from -128 to 127.

• pre-space

The number of decimal columns that are stored with leading spaces. In this case, each value contains a count for the number of leading spaces.

• end-space

The number of columns that have a lot of trailing spaces. In this case, each value contains a count for the number of trailing spaces.

• table-lookup

The column had only a small number of different values, which were converted to an ENUM before Huffman compression.

• zero

The number of columns for which all values are zero.

• Original trees

The initial number of Huffman trees.

• After join

The number of distinct Huffman trees left after joining trees to save some header space.

After a table has been compressed, the Field lines displayed by [myisamchk -dvv](#page-150-4) include additional information about each column:

• Type

The data type. The value may contain any of the following descriptors:

• constant

All rows have the same value.

• no endspace

Do not store endspace.

• no endspace, not\_always

Do not store endspace and do not do endspace compression for all values.

• no endspace, no empty

Do not store endspace. Do not store empty values.

• table-lookup

The column was converted to an ENUM.

• zerofill(N)

The most significant N bytes in the value are always 0 and are not stored.

• no zeros

Do not store zeros.

• always zero

Zero values are stored using one bit.

• Huff tree

The number of the Huffman tree associated with the column.

• Bits

The number of bits used in the Huffman tree.

After you run [myisampack](#page-170-0), use [myisamchk](#page-150-4) to re-create any indexes. At this time, you can also sort the index blocks and create statistics needed for the MySQL optimizer to work more efficiently:

```
myisamchk -rq --sort-index --analyze tbl_name.MYI
```

After you have installed the packed table into the MySQL database directory, you should execute [mysqladmin flush-tables](#page-28-0) to force mysqld to start using the new table.

To unpack a packed table, use the [--unpack](#page-161-6) option to [myisamchk](#page-150-4).

# <span id="page-176-0"></span>**6.6.7 mysql\_config\_editor — MySQL Configuration Utility**

The [mysql\\_config\\_editor](#page-176-0) utility enables you to store authentication credentials in an obfuscated login path file named .mylogin.cnf. The file location is the %APPDATA%\MySQL directory on Windows and the current user's home directory on non-Windows systems. The file can be read later by MySQL client programs to obtain authentication credentials for connecting to MySQL Server.

The unobfuscated format of the .mylogin.cnf login path file consists of option groups, similar to other option files. Each option group in .mylogin.cnf is called a "login path," which is a group that permits only certain options: host, user, password, port and socket. Think of a login path option group as a set of options that specify which MySQL server to connect to and which account to authenticate as. Here is an unobfuscated example:

```
[client]
user = mydefaultname
password = mydefaultpass
host = 127.0.0.1
[mypath]
user = myothername
password = myotherpass
host = localhost
```

When you invoke a client program to connect to the server, the client uses .mylogin.cnf in conjunction with other option files. Its precedence is higher than other option files, but less than options specified explicitly on the client command line. For information about the order in which option files are used, see Section 6.2.2.2, "Using Option Files".

To specify an alternate login path file name, set the MYSQL\_TEST\_LOGIN\_FILE environment variable. This variable is recognized by [mysql\\_config\\_editor](#page-176-0), by standard MySQL clients (mysql, [mysqladmin](#page-28-0), and so forth), and by the mysql-test-run.pl testing utility.

Programs use groups in the login path file as follows:

- [mysql\\_config\\_editor](#page-176-0) operates on the client login path by default if you specify no --loginpath=name option to indicate explicitly which login path to use.
- Without a --login-path option, client programs read the same option groups from the login path file that they read from other option files. Consider this command:

```
mysql
```

By default, the mysql client reads the [client] and [mysql] groups from other option files, so it reads them from the login path file as well.

• With a --login-path option, client programs additionally read the named login path from the login path file. The option groups read from other option files remain the same. Consider this command:

```
mysql --login-path=mypath
```

The mysql client reads [client] and [mysql] from other option files, and [client], [mysql], and [mypath] from the login path file.

• Client programs read the login path file even when the --no-defaults option is used, unless --no-login-paths is set. This permits passwords to be specified in a safer way than on the command line even if --no-defaults is present.

[mysql\\_config\\_editor](#page-176-0) obfuscates the .mylogin.cnf file so it cannot be read as cleartext, and its contents when unobfuscated by client programs are used only in memory. In this way, passwords can be stored in a file in non-cleartext format and used later without ever needing to be exposed on the command line or in an environment variable. [mysql\\_config\\_editor](#page-176-0) provides a print command for displaying the login path file contents, but even in this case, password values are masked so as never to appear in a way that other users can see them.

The obfuscation used by [mysql\\_config\\_editor](#page-176-0) prevents passwords from appearing in .mylogin.cnf as cleartext and provides a measure of security by preventing inadvertent password exposure. For example, if you display a regular unobfuscated my.cnf option file on the screen, any passwords it contains are visible for anyone to see. With .mylogin.cnf, that is not true, but the obfuscation used is not likely to deter a determined attacker and you should not consider it unbreakable. A user who can gain system administration privileges on your machine to access your files could unobfuscate the .mylogin.cnf file with some effort.

The login path file must be readable and writable to the current user, and inaccessible to other users. Otherwise, [mysql\\_config\\_editor](#page-176-0) ignores it, and client programs do not use it, either.

Invoke [mysql\\_config\\_editor](#page-176-0) like this:

```
mysql_config_editor [program_options] command [command_options]
```

If the login path file does not exist, [mysql\\_config\\_editor](#page-176-0) creates it.

Command arguments are given as follows:

- program\_options consists of general [mysql\\_config\\_editor](#page-176-0) options.
- command indicates what action to perform on the .mylogin.cnf login path file. For example, set writes a login path to the file, remove removes a login path, and print displays login path contents.
- command\_options indicates any additional options specific to the command, such as the login path name and the values to use in the login path.

The position of the command name within the set of program arguments is significant. For example, these command lines have the same arguments, but produce different results:

```
mysql_config_editor --help set
mysql_config_editor set --help
```

The first command line displays a general [mysql\\_config\\_editor](#page-176-0) help message, and ignores the set command. The second command line displays a help message specific to the set command.

Suppose that you want to establish a client login path that defines your default connection parameters, and an additional login path named remote for connecting to the MySQL server the host remote.example.com. You want to log in as follows:

- By default, to the local server with a user name and password of localuser and localpass
- To the remote server with a user name and password of remoteuser and remotepass

To set up the login paths in the .mylogin.cnf file, use the following set commands. Enter each command on a single line, and enter the appropriate passwords when prompted:

```
$> mysql_config_editor set --login-path=client
 --host=localhost --user=localuser --password
Enter password: enter password "localpass" here
$> mysql_config_editor set --login-path=remote
 --host=remote.example.com --user=remoteuser --password
Enter password: enter password "remotepass" here
```

[mysql\\_config\\_editor](#page-176-0) uses the client login path by default, so the --login-path=client option can be omitted from the first command without changing its effect.

To see what [mysql\\_config\\_editor](#page-176-0) writes to the .mylogin.cnf file, use the print command:

```
$> mysql_config_editor print --all
[client]
user = localuser
password = *****
host = localhost
[remote]
user = remoteuser
password = *****
host = remote.example.com
```

The print command displays each login path as a set of lines beginning with a group header indicating the login path name in square brackets, followed by the option values for the login path. Password values are masked and do not appear as cleartext.

If you do not specify --all to display all login paths or --login-path=name to display a named login path, the print command displays the client login path by default, if there is one.

As shown by the preceding example, the login path file can contain multiple login paths. In this way, [mysql\\_config\\_editor](#page-176-0) makes it easy to set up multiple "personalities" for connecting to different MySQL servers, or for connecting to a given server using different accounts. Any of these can be

selected by name later using the --login-path option when you invoke a client program. For example, to connect to the remote server, use this command:

mysql --login-path=remote

Here, mysql reads the [client] and [mysql] option groups from other option files, and the [client], [mysql], and [remote] groups from the login path file.

To connect to the local server, use this command:

mysql --login-path=client

Because mysql reads the client and mysql login paths by default, the --login-path option does not add anything in this case. That command is equivalent to this one:

mysql

Options read from the login path file take precedence over options read from other option files. Options read from login path groups appearing later in the login path file take precedence over options read from groups appearing earlier in the file.

[mysql\\_config\\_editor](#page-176-0) adds login paths to the login path file in the order you create them, so you should create more general login paths first and more specific paths later. If you need to move a login path within the file, you can remove it, then recreate it to add it to the end. For example, a client login path is more general because it is read by all client programs, whereas a mysqldump login path is read only by [mysqldump](#page-57-0). Options specified later override options specified earlier, so putting the login paths in the order client, mysqldump enables [mysqldump](#page-57-0)-specific options to override client options.

When you use the set command with [mysql\\_config\\_editor](#page-176-0) to create a login path, you need not specify all possible option values (host name, user name, password, port, socket). Only those values given are written to the path. Any missing values required later can be specified when you invoke a client path to connect to the MySQL server, either in other option files or on the command line. Any options specified on the command line override those specified in the login path file or other option files. For example, if the credentials in the remote login path also apply for the host remote2.example.com, connect to the server on that host like this:

mysql --login-path=remote --host=remote2.example.com

# <span id="page-179-1"></span>**mysql\_config\_editor General Options**

[mysql\\_config\\_editor](#page-176-0) supports the following general options, which may be used preceding any command named on the command line. For descriptions of command-specific options, see [mysql\\_config\\_editor Commands and Command-Specific Options.](#page-180-0)

**Table 6.18 mysql\_config\_editor General Options**

| Option Name | Description                          |
|-------------|--------------------------------------|
| debug       | Write debugging log                  |
| help        | Display help message and exit        |
| verbose     | Verbose mode                         |
| version     | Display version information and exit |

<span id="page-179-0"></span>• [--help](#page-179-0), -?

| Command-Line Format | help |
|---------------------|------|
|                     |      |

Display a general help message and exit.

To see a command-specific help message, invoke [mysql\\_config\\_editor](#page-176-0) as follows, where command is a command other than help:

mysql\_config\_editor command --help

<span id="page-180-1"></span>• --debug[=[debug\\_options](#page-180-1)], -# debug\_options

| Command-Line Format | debug[=debug_options] |  |
|---------------------|-----------------------|--|
| Type                | String                |  |
| Default Value       | d:t:o                 |  |

Write a debugging log. A typical debug\_options string is d:t:o,file\_name. The default is d:t:o,/tmp/mysql\_config\_editor.trace.

This option is available only if MySQL was built using WITH\_DEBUG. MySQL release binaries provided by Oracle are not built using this option.

<span id="page-180-2"></span>• [--verbose](#page-180-2), -v

| Command-Line Format | verbose |
|---------------------|---------|
|---------------------|---------|

Verbose mode. Print more information about what the program does. This option may be helpful in diagnosing problems if an operation does not have the effect you expect.

<span id="page-180-3"></span>• [--version](#page-180-3), -V

| Command-Line Format | version |
|---------------------|---------|
|---------------------|---------|

Display version information and exit.

# <span id="page-180-0"></span>**mysql\_config\_editor Commands and Command-Specific Options**

This section describes the permitted [mysql\\_config\\_editor](#page-176-0) commands, and, for each one, the command-specific options permitted following the command name on the command line.

In addition, [mysql\\_config\\_editor](#page-176-0) supports general options that can be used preceding any command. For descriptions of these options, see [mysql\\_config\\_editor General Options.](#page-179-1)

[mysql\\_config\\_editor](#page-176-0) supports these commands:

• help

Display a general help message and exit. This command takes no following options.

To see a command-specific help message, invoke [mysql\\_config\\_editor](#page-176-0) as follows, where command is a command other than help:

```
mysql_config_editor command --help
```

• print [options]

Print the contents of the login path file in unobfuscated form, with the exception that passwords are displayed as \*\*\*\*\*.

The default login path name is client if no login path is named. If both --all and --login-path are given, --all takes precedence.

The print command permits these options following the command name:

• --help, -?

Display a help message for the print command and exit.

To see a general help message, use [mysql\\_config\\_editor --help](#page-176-0).

• --all

Print the contents of all login paths in the login path file.

• --login-path=name, -G name

Print the contents of the named login path.

• remove [options]

Remove a login path from the login path file, or modify a login path by removing options from it.

This command removes from the login path only such options as are specified with the --host, - password, --port, --socket, and --user options. If none of those options are given, remove

removes the entire login path. For example, this command removes only the user option from the mypath login path rather than the entire mypath login path:

```
mysql_config_editor remove --login-path=mypath --user
```

This command removes the entire mypath login path:

```
mysql_config_editor remove --login-path=mypath
```

The remove command permits these options following the command name:

• --help, -?

Display a help message for the remove command and exit.

To see a general help message, use [mysql\\_config\\_editor --help](#page-176-0).

• --host, -h

Remove the host name from the login path.

• --login-path=name, -G name

The login path to remove or modify. The default login path name is client if this option is not given.

• --password, -p

Remove the password from the login path.

• --port, -P

Remove the TCP/IP port number from the login path.

• --socket, -S

Remove the Unix socket file name from the login path.

• --user, -u

Remove the user name from the login path.

• --warn, -w

Warn and prompt the user for confirmation if the command attempts to remove the default login path (client) and --login-path=client was not specified. This option is enabled by default; use --skip-warn to disable it.

• reset [options]

Empty the contents of the login path file.

The reset command permits these options following the command name:

• --help, -?

Display a help message for the reset command and exit.

To see a general help message, use [mysql\\_config\\_editor --help](#page-176-0).

• set [options]

Write a login path to the login path file.

This command writes to the login path only such options as are specified with the --host, --password, --port, --socket, and --user options. If none of those options are given, [mysql\\_config\\_editor](#page-176-0) writes the login path as an empty group.

The set command permits these options following the command name:

• --help, -?

Display a help message for the set command and exit.

To see a general help message, use [mysql\\_config\\_editor --help](#page-176-0).

• --host=host\_name, -h host\_name

The host name to write to the login path.

• --login-path=name, -G name

The login path to create. The default login path name is client if this option is not given.

• --password, -p

Prompt for a password to write to the login path. After [mysql\\_config\\_editor](#page-176-0) displays the prompt, type the password and press Enter. To prevent other users from seeing the password, [mysql\\_config\\_editor](#page-176-0) does not echo it.

To specify an empty password, press Enter at the password prompt. The resulting login path written to the login path file includes a line like this:

```
password =
```

• --port=port\_num, -P port\_num

The TCP/IP port number to write to the login path.

• --socket=file\_name, -S file\_name

The Unix socket file name to write to the login path.

• --user=user\_name, -u user\_name

The user name to write to the login path.

• --warn, -w

Warn and prompt the user for confirmation if the command attempts to overwrite an existing login path. This option is enabled by default; use --skip-warn to disable it.

# <span id="page-183-0"></span>**6.6.8 mysql\_migrate\_keyring — Keyring Key Migration Utility**

The [mysql\\_migrate\\_keyring](#page-183-0) utility migrates keys between one keyring component and another. It supports offline and online migrations.

Invoke [mysql\\_migrate\\_keyring](#page-183-0) like this (enter the command on a single line):

```
mysql_migrate_keyring
 --component-dir=dir_name
 --source-keyring=name
 --destination-keyring=name
```

[other options]

For information about key migrations and instructions describing how to perform them using [mysql\\_migrate\\_keyring](#page-183-0) and other methods, see Section 8.4.4.11, "Migrating Keys Between Keyring Keystores".

[mysql\\_migrate\\_keyring](#page-183-0) supports the following options, which can be specified on the command line or in the [mysql\_migrate\_keyring] group of an option file. For information about option files used by MySQL programs, see Section 6.2.2.2, "Using Option Files".

**Table 6.19 mysql\_migrate\_keyring Options**

| Option Name                           | Description                                                                    |
|---------------------------------------|--------------------------------------------------------------------------------|
| component-dir                         | Directory for keyring components                                               |
| defaults-extra-file                   | Read named option file in addition to usual option<br>files                    |
| defaults-file                         | Read only named option file                                                    |
| defaults-group-suffix                 | Option group suffix value                                                      |
| destination-keyring                   | Destination keyring component name                                             |
| destination-keyring-configuration-dir | Destination keyring component configuration<br>directory                       |
| get-server-public-key                 | Request RSA public key from server                                             |
| help                                  | Display help message and exit                                                  |
| host                                  | Host on which MySQL server is located                                          |
| login-path                            | Read login path options from .mylogin.cnf                                      |
| no-defaults                           | Read no option files                                                           |
| no-login-paths                        | Do not read login paths from the login path file                               |
| online-migration                      | Migration source is an active server                                           |
| password                              | Password to use when connecting to server                                      |
| port                                  | TCP/IP port number for connection                                              |
| print-defaults                        | Print default options                                                          |
| server-public-key-path                | Path name to file containing RSA public key                                    |
| socket                                | Unix socket file or Windows named pipe to use                                  |
| source-keyring                        | Source keyring component name                                                  |
| source-keyring-configuration-dir      | Source keyring component configuration directory                               |
| ssl-ca                                | File that contains list of trusted SSL Certificate<br>Authorities              |
| ssl-capath                            | Directory that contains trusted SSL Certificate<br>Authority certificate files |
| ssl-cert                              | File that contains X.509 certificate                                           |
| ssl-cipher                            | Permissible ciphers for connection encryption                                  |
| ssl-crl                               | File that contains certificate revocation lists                                |
| ssl-crlpath                           | Directory that contains certificate revocation-list<br>files                   |
| ssl-fips-mode                         | Whether to enable FIPS mode on client side                                     |
| ssl-key                               | File that contains X.509 key                                                   |
| ssl-mode                              | Desired security state of connection to server                                 |
|                                       |                                                                                |

| Option Name                               | Description                                                   |
|-------------------------------------------|---------------------------------------------------------------|
| ssl-session-data                          | File that contains SSL session data                           |
| ssl-session-data-continue-on-failed-reuse | Whether to establish connections if session reuse<br>fails    |
| tls-ciphersuites                          | Permissible TLSv1.3 ciphersuites for encrypted<br>connections |
| tls-sni-servername                        | Server name supplied by the client                            |
| tls-version                               | Permissible TLS protocols for encrypted<br>connections        |
| user                                      | MySQL user name to use when connecting to<br>server           |
| verbose                                   | Verbose mode                                                  |
| version                                   | Display version information and exit                          |

<span id="page-185-3"></span>• [--help](#page-185-3), -h

| Command-Line Format | help |
|---------------------|------|
|---------------------|------|

#### Display a help message and exit.

<span id="page-185-0"></span>• [--component-dir=](#page-185-0)dir\_name

| Command-Line Format | component-dir=dir_name |
|---------------------|------------------------|
| Type                | Directory name         |

The directory where keyring components are located. This is typically the value of the plugin\_dir system variable for the local MySQL server.

![](_page_185_Picture_8.jpeg)

# **Note**

[--component-dir](#page-185-0), [--source-keyring](#page-189-3), and [--destination](#page-186-1)[keyring](#page-186-1) are mandatory for all keyring migration operations performed by [mysql\\_migrate\\_keyring](#page-183-0). In addition, the source and destination components must differ, and both components must be properly configured so that [mysql\\_migrate\\_keyring](#page-183-0) can load and use them.

<span id="page-185-1"></span>• [--defaults-extra-file=](#page-185-1)file\_name

| Command-Line Format | defaults-extra-file=file_name |
|---------------------|-------------------------------|
| Type                | File name                     |

Read this option file after the global option file but (on Unix) before the user option file. If the file does not exist or is otherwise inaccessible, an error occurs. If file\_name is not an absolute path name, it is interpreted relative to the current directory.

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-185-2"></span>• [--defaults-file=](#page-185-2)file\_name

| Command-Line Format | defaults-file=file_name |
|---------------------|-------------------------|
| Type                | File name               |

Use only the given option file. If the file does not exist or is otherwise inaccessible, an error occurs. If file\_name is not an absolute path name, it is interpreted relative to the current directory.

Exception: Even with --defaults-file, client programs read .mylogin.cnf.

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-186-0"></span>• [--defaults-group-suffix=](#page-186-0)str

| Command-Line Format | defaults-group-suffix=str |
|---------------------|---------------------------|
| Type                | String                    |

Read not only the usual option groups, but also groups with the usual names and a suffix of str. For example, [mysql\\_migrate\\_keyring](#page-183-0) normally reads the [mysql\_migrate\_keyring] group. If this option is given as [--defaults-group-suffix=\\_other](#page-186-0), [mysql\\_migrate\\_keyring](#page-183-0) also reads the [mysql\_migrate\_keyring\_other] group.

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-186-1"></span>• [--destination-keyring=](#page-186-1)name

| Command-Line Format | destination-keyring=name |
|---------------------|--------------------------|
| Type                | String                   |

The destination keyring component for key migration. The format and interpretation of the option value is the same as described for the [--source-keyring](#page-189-3) option.

![](_page_186_Picture_11.jpeg)

#### **Note**

[--component-dir](#page-185-0), [--source-keyring](#page-189-3), and [--destination](#page-186-1)[keyring](#page-186-1) are mandatory for all keyring migration operations performed by [mysql\\_migrate\\_keyring](#page-183-0). In addition, the source and destination components must differ, and both components must be properly configured so that [mysql\\_migrate\\_keyring](#page-183-0) can load and use them.

<span id="page-186-2"></span>• [--destination-keyring-configuration-dir=](#page-186-2)dir\_name

| Command-Line Format | destination-keyring-configuration<br>dir=dir_name |
|---------------------|---------------------------------------------------|
| Type                | Directory name                                    |

This option applies only if the destination keyring component global configuration file contains "read\_local\_config": true, indicating that component configuration is contained in the local configuration file. The option value specifies the directory containing that local file.

<span id="page-186-3"></span>• [--get-server-public-key](#page-186-3)

| Command-Line Format | get-server-public-key |
|---------------------|-----------------------|
|                     |                       |
|                     |                       |

Request from the server the public key required for RSA key pair-based password exchange. This option applies to clients that authenticate with the caching\_sha2\_password authentication plugin. For that plugin, the server does not send the public key unless requested. This option is ignored for accounts that do not authenticate with that plugin. It is also ignored if RSA-based password exchange is not used, as is the case when the client connects to the server using a secure connection.

If [--server-public-key-path=](#page-189-1)file\_name is given and specifies a valid public key file, it takes precedence over [--get-server-public-key](#page-186-3).

For information about the caching\_sha2\_password plugin, see Section 8.4.1.2, "Caching SHA-2 Pluggable Authentication".

<span id="page-187-0"></span>• --host=[host\\_name](#page-187-0), -h host\_name

| Command-Line Format | host=host_name |
|---------------------|----------------|
| Type                | String         |
| Default Value       | localhost      |

The host location of the running server that is currently using one of the key migration keystores. Migration always occurs on the local host, so the option always specifies a value for connecting to a local server, such as localhost, 127.0.0.1, ::1, or the local host IP address or host name.

<span id="page-187-1"></span>• [--login-path=](#page-187-1)name

| Command-Line Format | login-path=name |
|---------------------|-----------------|
| Type                | String          |

Read options from the named login path in the .mylogin.cnf login path file. A "login path" is an option group containing options that specify which MySQL server to connect to and which account to authenticate as. To create or modify a login path file, use the [mysql\\_config\\_editor](#page-176-0) utility. See [Section 6.6.7, "mysql\\_config\\_editor — MySQL Configuration Utility".](#page-176-0)

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-187-2"></span>• [--no-login-paths](#page-187-2)

| Command-Line Format | no-login-paths |
|---------------------|----------------|
|---------------------|----------------|

Skips reading options from the login path file.

See [--login-path](#page-187-1) for related information.

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

## <span id="page-188-0"></span>• [--no-defaults](#page-188-0)

| Command-Line Format | no-defaults |
|---------------------|-------------|
|---------------------|-------------|

Do not read any option files. If program startup fails due to reading unknown options from an option file, [--no-defaults](#page-188-0) can be used to prevent them from being read.

The exception is that the .mylogin.cnf file is read in all cases, if it exists. This permits passwords to be specified in a safer way than on the command line even when [--no-defaults](#page-188-0) is used. To create .mylogin.cnf, use the [mysql\\_config\\_editor](#page-176-0) utility. See [Section 6.6.7,](#page-176-0) ["mysql\\_config\\_editor — MySQL Configuration Utility".](#page-176-0)

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

## <span id="page-188-1"></span>• [--online-migration](#page-188-1)

| Command-Line Format | online-migration |
|---------------------|------------------|
| Type                | Boolean          |
| Default Value       | FALSE            |

This option is mandatory when a running server is using the keyring. It tells [mysql\\_migrate\\_keyring](#page-183-0) to perform an online key migration. The option has these effects:

- [mysql\\_migrate\\_keyring](#page-183-0) connects to the server using any connection options specified; these options are otherwise ignored.
- After [mysql\\_migrate\\_keyring](#page-183-0) connects to the server, it tells the server to pause keyring operations. When key copying is complete, [mysql\\_migrate\\_keyring](#page-183-0) tells the server it can resume keyring operations before disconnecting.
- <span id="page-188-2"></span>• [--password\[=](#page-188-2)password], -p[password]

| Command-Line Format | password[=password] |
|---------------------|---------------------|
| Type                | String              |

The password of the MySQL account used for connecting to the running server that is currently using one of the key migration keystores. The password value is optional. If not given, [mysql\\_migrate\\_keyring](#page-183-0) prompts for one. If given, there must be no space between [-](#page-188-2) [password=](#page-188-2) or -p and the password following it. If no password option is specified, the default is to send no password.

Specifying a password on the command line should be considered insecure. To avoid giving the password on the command line, use an option file. See Section 8.1.2.1, "End-User Guidelines for Password Security".

To explicitly specify that there is no password and that [mysql\\_migrate\\_keyring](#page-183-0) should not prompt for one, use the [--skip-password](#page-188-2) option.

<span id="page-188-3"></span>• --port=[port\\_num](#page-188-3), -P port\_num

| Command-Line Format | 559<br>port=port_num |
|---------------------|----------------------|
| Type                | Numeric              |

| Default Value | 0 |
|---------------|---|
|---------------|---|

For TCP/IP connections, the port number for connecting to the running server that is currently using one of the key migration keystores.

<span id="page-189-0"></span>• [--print-defaults](#page-189-0)

| Command-Line Format | print-defaults |
|---------------------|----------------|
|---------------------|----------------|

Print the program name and all options that it gets from option files.

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-189-1"></span>• [--server-public-key-path=](#page-189-1)file\_name

| Command-Line Format | server-public-key-path=file_name |
|---------------------|----------------------------------|
| Type                | File name                        |

The path name to a file in PEM format containing a client-side copy of the public key required by the server for RSA key pair-based password exchange. This option applies to clients that authenticate with the sha256\_password (deprecated) or caching\_sha2\_password authentication plugin. This option is ignored for accounts that do not authenticate with one of those plugins. It is also ignored if RSA-based password exchange is not used, as is the case when the client connects to the server using a secure connection.

If [--server-public-key-path=](#page-189-1)file\_name is given and specifies a valid public key file, it takes precedence over [--get-server-public-key](#page-186-3).

For sha256\_password (deprecated), this option applies only if MySQL was built using OpenSSL.

For information about the sha256\_password and caching\_sha2\_password plugins, see Section 8.4.1.3, "SHA-256 Pluggable Authentication", and Section 8.4.1.2, "Caching SHA-2 Pluggable Authentication".

<span id="page-189-2"></span>• [--socket=](#page-189-2)path, -S path

| Command-Line Format | socket={file_name pipe_name} |
|---------------------|------------------------------|
| Type                | String                       |

For Unix socket file or Windows named pipe connections, the socket file or named pipe for connecting to the running server that is currently using one of the key migration keystores.

On Windows, this option applies only if the server was started with the named\_pipe system variable enabled to support named-pipe connections. In addition, the user making the connection must be a member of the Windows group specified by the named\_pipe\_full\_access\_group system variable.

<span id="page-189-3"></span>• [--source-keyring=](#page-189-3)name

| Command-Line Format | source-keyring=name |
|---------------------|---------------------|

| Type | String |
|------|--------|
|------|--------|

The source keyring component for key migration. This is the component library file name specified without any platform-specific extension such as .so or .dll. For example, to use the component for which the library file is component\_keyring\_file.so, specify the option as [--source](#page-189-3)[keyring=component\\_keyring\\_file](#page-189-3).

![](_page_190_Picture_3.jpeg)

#### **Note**

[--component-dir](#page-185-0), [--source-keyring](#page-189-3), and [--destination](#page-186-1)[keyring](#page-186-1) are mandatory for all keyring migration operations performed by [mysql\\_migrate\\_keyring](#page-183-0). In addition, the source and destination components must differ, and both components must be properly configured so that [mysql\\_migrate\\_keyring](#page-183-0) can load and use them.

<span id="page-190-0"></span>• [--source-keyring-configuration-dir=](#page-190-0)dir\_name

| Command-Line Format | source-keyring-configuration |
|---------------------|------------------------------|
|                     | dir=dir_name                 |
| Type                | Directory name               |

This option applies only if the source keyring component global configuration file contains "read\_local\_config": true, indicating that component configuration is contained in the local configuration file. The option value specifies the directory containing that local file.

<span id="page-190-1"></span>• --ssl\*

Options that begin with --ssl specify whether to connect to the server using encryption and indicate where to find SSL keys and certificates. See Command Options for Encrypted Connections.

<span id="page-190-2"></span>• [--ssl-fips-mode={OFF|ON|STRICT}](#page-190-2)

| Command-Line Format | ssl-fips-mode={OFF ON STRICT} |
|---------------------|-------------------------------|
| Deprecated          | Yes                           |
| Type                | Enumeration                   |
| Default Value       | OFF                           |
| Valid Values        | OFF                           |
|                     | ON                            |
|                     | STRICT                        |

Controls whether to enable FIPS mode on the client side. The [--ssl-fips-mode](#page-190-2) option differs from other --ssl-xxx options in that it is not used to establish encrypted connections, but rather to affect which cryptographic operations to permit. See Section 8.8, "FIPS Support".

These [--ssl-fips-mode](#page-190-2) values are permitted:

- OFF: Disable FIPS mode.
- ON: Enable FIPS mode.

• STRICT: Enable "strict" FIPS mode.

![](_page_191_Picture_2.jpeg)

#### **Note**

If the OpenSSL FIPS Object Module is not available, the only permitted value for [--ssl-fips-mode](#page-190-2) is OFF. In this case, setting [--ssl-fips-mode](#page-190-2) to ON or STRICT causes the client to produce a warning at startup and to operate in non-FIPS mode.

This option is deprecated. Expect it to be removed in a future version of MySQL.

<span id="page-191-0"></span>• [--tls-ciphersuites=](#page-191-0)ciphersuite\_list

| Command-Line Format | tls-ciphersuites=ciphersuite_list |
|---------------------|-----------------------------------|
| Type                | String                            |

The permissible ciphersuites for encrypted connections that use TLSv1.3. The value is a list of one or more colon-separated ciphersuite names. The ciphersuites that can be named for this option depend on the SSL library used to compile MySQL. For details, see Section 8.3.2, "Encrypted Connection TLS Protocols and Ciphers".

<span id="page-191-1"></span>• [--tls-sni-servername=](#page-191-1)server\_name

| Command-Line Format | tls-sni-servername=server_name |
|---------------------|--------------------------------|
| Type                | String                         |

When specified, the name is passed to the libmysqlclient C API library using the MYSQL\_OPT\_TLS\_SNI\_SERVERNAME option of [mysql\\_options\(\)](https://dev.mysql.com/doc/c-api/8.4/en/mysql-options.md). The server name is not casesensitive. To show which server name the client specified for the current session, if any, check the Tls\_sni\_server\_name status variable.

Server Name Indication (SNI) is an extension to the TLS protocol (OpenSSL must be compiled using TLS extensions for this option to function). The MySQL implementation of SNI represents the clientside only.

<span id="page-191-2"></span>• [--tls-version=](#page-191-2)protocol\_list

| Command-Line Format | tls-version=protocol_list                                  |
|---------------------|------------------------------------------------------------|
| Type                | String                                                     |
| Default Value       | TLSv1,TLSv1.1,TLSv1.2,TLSv1.3<br>(OpenSSL 1.1.1 or higher) |
|                     | TLSv1,TLSv1.1,TLSv1.2 (otherwise)                          |

The permissible TLS protocols for encrypted connections. The value is a list of one or more commaseparated protocol names. The protocols that can be named for this option depend on the SSL library used to compile MySQL. For details, see Section 8.3.2, "Encrypted Connection TLS Protocols and Ciphers".

<span id="page-191-3"></span>• --user=[user\\_name](#page-191-3), -u user\_name

The user name of the MySQL account used for connecting to the running server that is currently using one of the key migration keystores.

<span id="page-192-0"></span>• [--verbose](#page-192-0), -v

| Command-Line Format | verbose |
|---------------------|---------|
|---------------------|---------|

Verbose mode. Produce more output about what the program does.

<span id="page-192-1"></span>• [--version](#page-192-1), -V

| Command-Line Format | version |
|---------------------|---------|

Display version information and exit.

# <span id="page-192-2"></span>**6.6.9 mysqlbinlog — Utility for Processing Binary Log Files**

The server's binary log consists of files containing "events" that describe modifications to database contents. The server writes these files in binary format. To display their contents in text format, use the [mysqlbinlog](#page-192-2) utility. You can also use [mysqlbinlog](#page-192-2) to display the contents of relay log files written by a replica server in a replication setup because relay logs have the same format as binary logs. The binary log and relay log are discussed further in Section 7.4.4, "The Binary Log", and Section 19.2.4, "Relay Log and Replication Metadata Repositories".

Invoke [mysqlbinlog](#page-192-2) like this:

```
mysqlbinlog [options] log_file ...
```

For example, to display the contents of the binary log file named binlog.000003, use this command:

```
mysqlbinlog binlog.000003
```

The output includes events contained in binlog.000003. For statement-based logging, event information includes the SQL statement, the ID of the server on which it was executed, the timestamp when the statement was executed, how much time it took, and so forth. For row-based logging, the event indicates a row change rather than an SQL statement. See Section 19.2.1, "Replication Formats", for information about logging modes.

Events are preceded by header comments that provide additional information. For example:

```
# at 141
#100309 9:28:36 server id 123 end_log_pos 245
 Query thread_id=3350 exec_time=11 error_code=0
```

In the first line, the number following at indicates the file offset, or starting position, of the event in the binary log file.

The second line starts with a date and time indicating when the statement started on the server where the event originated. For replication, this timestamp is propagated to replica servers. server id is the server\_id value of the server where the event originated. end\_log\_pos indicates where the next event starts (that is, it is the end position of the current event + 1). thread\_id indicates which thread executed the event. exec\_time is the time spent executing the event, on a replication source server. On a replica, it is the difference of the end execution time on the replica minus the beginning execution time on the source. The difference serves as an indicator of how much replication lags behind the source. error\_code indicates the result from executing the event. Zero means that no error occurred. 563

![](_page_193_Picture_1.jpeg)

#### **Note**

When using event groups, the file offsets of events may be grouped together and the comments of events may be grouped together. Do not mistake these grouped events for blank file offsets.

The output from [mysqlbinlog](#page-192-2) can be re-executed (for example, by using it as input to mysql) to redo the statements in the log. This is useful for recovery operations after an unexpected server exit. For other usage examples, see the discussion later in this section and in Section 9.5, "Point-in-Time (Incremental) Recovery". To execute the internal-use BINLOG statements used by [mysqlbinlog](#page-192-2), the user requires the BINLOG\_ADMIN privilege (or the deprecated SUPER privilege), or the REPLICATION\_APPLIER privilege plus the appropriate privileges to execute each log event.

You can use [mysqlbinlog](#page-192-2) to read binary log files directly and apply them to the local MySQL server. You can also read binary logs from a remote server by using the --read-from-remote-server option. To read remote binary logs, the connection parameter options can be given to indicate how to connect to the server. These options are --host, --password, --port, --protocol, --socket, and --user.

When binary log files have been encrypted, [mysqlbinlog](#page-192-2) cannot read them directly, but can read them from the server using the --read-from-remote-server option. Binary log files are encrypted when the server's binlog\_encryption system variable is set to ON. The SHOW BINARY LOGS statement shows whether a particular binary log file is encrypted or unencrypted. Encrypted and unencrypted binary log files can also be distinguished using the magic number at the start of the file header for encrypted log files (0xFD62696E), which differs from that used for unencrypted log files (0xFE62696E). Note that [mysqlbinlog](#page-192-2) returns a suitable error if you attempt to read an encrypted binary log file directly, but older versions of [mysqlbinlog](#page-192-2) do not recognise the file as a binary log file at all. For more information on binary log encryption, see Section 19.3.2, "Encrypting Binary Log Files and Relay Log Files".

When binary log transaction payloads have been compressed, [mysqlbinlog](#page-192-2) automatically decompresses and decodes the transaction payloads, and prints them as it would uncompressed events. When binlog\_transaction\_compression is set to ON, transaction payloads are compressed and then written to the server's binary log file as a single event (a Transaction\_payload\_event). With the --verbose option, [mysqlbinlog](#page-192-2) adds comments stating the compression algorithm used, the compressed payload size that was originally received, and the resulting payload size after decompression.

![](_page_193_Picture_8.jpeg)

## **Note**

The end position (end\_log\_pos) that [mysqlbinlog](#page-192-2) states for an individual event that was part of a compressed transaction payload is the same as the end position of the original compressed payload. Multiple decompressed events can therefore have the same end position.

[mysqlbinlog](#page-192-2)'s own connection compression does less if transaction payloads are already compressed, but still operates on uncompressed transactions and headers.

For more information on binary log transaction compression, see Section 7.4.4.5, "Binary Log Transaction Compression".

When running [mysqlbinlog](#page-192-2) against a large binary log, be careful that the filesystem has enough space for the resulting files. To configure the directory that [mysqlbinlog](#page-192-2) uses for temporary files, use the TMPDIR environment variable.

[mysqlbinlog](#page-192-2) sets the value of pseudo\_replica\_mode to true before executing any SQL statements. This system variable affects the handling of XA transactions, the original\_commit\_timestamp replication delay timestamp and the original\_server\_version system variable, and unsupported SQL modes.

[mysqlbinlog](#page-192-2) supports the following options, which can be specified on the command line or in the [mysqlbinlog] and [client] groups of an option file. For information about option files used by MySQL programs, see Section 6.2.2.2, "Using Option Files".

#### **Table 6.20 mysqlbinlog Options**

| Option Name               | Description                                                                                              |
|---------------------------|----------------------------------------------------------------------------------------------------------|
| base64-output             | Print binary log entries using base-64 encoding                                                          |
| bind-address              | Use specified network interface to connect to<br>MySQL Server                                            |
| binlog-row-event-max-size | Binary log max event size                                                                                |
| character-sets-dir        | Directory where character sets are installed                                                             |
| compress                  | Compress all information sent between client and<br>server                                               |
| compression-algorithms    | Permitted compression algorithms for connections<br>to server                                            |
| connection-server-id      | Used for testing and debugging. See text for<br>applicable default values and other particulars          |
| database                  | List entries for just this database                                                                      |
| debug                     | Write debugging log                                                                                      |
| debug-check               | Print debugging information when program exits                                                           |
| debug-info                | Print debugging information, memory, and CPU<br>statistics when program exits                            |
| default-auth              | Authentication plugin to use                                                                             |
| defaults-extra-file       | Read named option file in addition to usual option<br>files                                              |
| defaults-file             | Read only named option file                                                                              |
| defaults-group-suffix     | Option group suffix value                                                                                |
| disable-log-bin           | Disable binary logging                                                                                   |
| exclude-gtids             | Do not show any of the groups in the GTID set<br>provided                                                |
| force-if-open             | Read binary log files even if open or not closed<br>properly                                             |
| force-read                | If mysqlbinlog reads a binary log event that it does<br>not recognize, it prints a warning               |
| get-server-public-key     | Request RSA public key from server                                                                       |
| help                      | Display help message and exit                                                                            |
| hexdump                   | Display a hex dump of the log in comments                                                                |
| host                      | Host on which MySQL server is located                                                                    |
| idempotent                | Cause the server to use idempotent mode while<br>processing binary log updates from this session<br>only |
| include-gtids             | Show only the groups in the GTID set provided                                                            |
| local-load                | Prepare local temporary files for LOAD DATA in<br>the specified directory                                |
| login-path                | Read login path options from .mylogin.cnf                                                                |
| no-defaults               | Read no option files                                                                                     |
| no-login-paths            | Do not read login paths from the login path file                                                         |
|                           |                                                                                                          |

| Option Name             | Description                                                                                                                                                                                                            |
|-------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| offset                  | Skip the first N entries in the log                                                                                                                                                                                    |
| password                | Password to use when connecting to server                                                                                                                                                                              |
| plugin-dir              | Directory where plugins are installed                                                                                                                                                                                  |
| port                    | TCP/IP port number for connection                                                                                                                                                                                      |
| print-defaults          | Print default options                                                                                                                                                                                                  |
| print-table-metadata    | Print table metadata                                                                                                                                                                                                   |
| protocol                | Transport protocol to use                                                                                                                                                                                              |
| raw                     | Write events in raw (binary) format to output files                                                                                                                                                                    |
| read-from-remote-master | Read the binary log from a MySQL replication<br>source server rather than reading a local log file                                                                                                                     |
| read-from-remote-server | Read binary log from MySQL server rather than<br>local log file                                                                                                                                                        |
| read-from-remote-source | Read the binary log from a MySQL replication<br>source server rather than reading a local log file                                                                                                                     |
| require-row-format      | Require row-based binary logging format                                                                                                                                                                                |
| result-file             | Direct output to named file                                                                                                                                                                                            |
| rewrite-db              | Create rewrite rules for databases when playing<br>back from logs written in row-based format. Can<br>be used multiple times                                                                                           |
| server-id               | Extract only those events created by the server<br>having the given server ID                                                                                                                                          |
| server-id-bits          | Tell mysqlbinlog how to interpret server IDs in<br>binary log when log was written by a mysqld<br>having its server-id-bits set to less than the<br>maximum; supported only by MySQL Cluster<br>version of mysqlbinlog |
| server-public-key-path  | Path name to file containing RSA public key                                                                                                                                                                            |
| set-charset             | Add a SET NAMES charset_name statement to<br>the output                                                                                                                                                                |
| shared-memory-base-name | Shared-memory name for shared-memory<br>connections (Windows only)                                                                                                                                                     |
| short-form              | Display only the statements contained in the log                                                                                                                                                                       |
| skip-gtids              | Do not include the GTIDs from the binary log files<br>in the output dump file                                                                                                                                          |
| socket                  | Unix socket file or Windows named pipe to use                                                                                                                                                                          |
| ssl-ca                  | File that contains list of trusted SSL Certificate<br>Authorities                                                                                                                                                      |
| ssl-capath              | Directory that contains trusted SSL Certificate<br>Authority certificate files                                                                                                                                         |
| ssl-cert                | File that contains X.509 certificate                                                                                                                                                                                   |
| ssl-cipher              | Permissible ciphers for connection encryption                                                                                                                                                                          |
| ssl-crl                 | File that contains certificate revocation lists                                                                                                                                                                        |
| ssl-crlpath             | Directory that contains certificate revocation-list<br>files                                                                                                                                                           |
| ssl-fips-mode           | Whether to enable FIPS mode on client side                                                                                                                                                                             |

| Option Name                               | Description                                                                                                                      |
|-------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------|
| ssl-key                                   | File that contains X.509 key                                                                                                     |
| ssl-mode                                  | Desired security state of connection to server                                                                                   |
| ssl-session-data                          | File that contains SSL session data                                                                                              |
| ssl-session-data-continue-on-failed-reuse | Whether to establish connections if session reuse<br>fails                                                                       |
| start-datetime                            | Read binary log from first event with timestamp<br>equal to or later than datetime argument                                      |
| start-position                            | Decode binary log from first event with position<br>equal to or greater than argument                                            |
| stop-datetime                             | Stop reading binary log at first event with<br>timestamp equal to or greater than datetime<br>argument                           |
| stop-never                                | Stay connected to server after reading last binary<br>log file                                                                   |
| stop-never-slave-server-id                | Slave server ID to report when connecting to<br>server                                                                           |
| stop-position                             | Stop decoding binary log at first event with<br>position equal to or greater than argument                                       |
| tls-ciphersuites                          | Permissible TLSv1.3 ciphersuites for encrypted<br>connections                                                                    |
| tls-sni-servername                        | Server name supplied by the client                                                                                               |
| tls-version                               | Permissible TLS protocols for encrypted<br>connections                                                                           |
| to-last-log                               | Do not stop at the end of requested binary log<br>from a MySQL server, but rather continue printing<br>to end of last binary log |
| user                                      | MySQL user name to use when connecting to<br>server                                                                              |
| verbose                                   | Reconstruct row events as SQL statements                                                                                         |
| verify-binlog-checksum                    | Verify checksums in binary log                                                                                                   |
| version                                   | Display version information and exit                                                                                             |
| zstd-compression-level                    | Compression level for connections to server that<br>use zstd compression                                                         |

## <span id="page-196-1"></span>• [--help](#page-196-1), -?

| Command-Line Format | help |
|---------------------|------|

## Display a help message and exit.

## <span id="page-196-0"></span>• [--base64-output=](#page-196-0)value

| Command-Line Format | base64-output=value |
|---------------------|---------------------|
| Type                | String              |
| Default Value       | AUTO                |
| Valid Values        | AUTO                |
|                     |                     |
|                     | NEVER<br>567        |

DECODE-ROWS

This option determines when events should be displayed encoded as base-64 strings using BINLOG statements. The option has these permissible values (not case-sensitive):

• AUTO ("automatic") or UNSPEC ("unspecified") displays BINLOG statements automatically when necessary (that is, for format description events and row events). If no [--base64-output](#page-196-0) option is given, the effect is the same as [--base64-output=AUTO](#page-196-0).

![](_page_197_Picture_4.jpeg)

#### **Note**

Automatic BINLOG display is the only safe behavior if you intend to use the output of [mysqlbinlog](#page-192-2) to re-execute binary log file contents. The other option values are intended only for debugging or testing purposes because they may produce output that does not include all events in executable form.

- NEVER causes BINLOG statements not to be displayed. [mysqlbinlog](#page-192-2) exits with an error if a row event is found that must be displayed using BINLOG.
- DECODE-ROWS specifies to [mysqlbinlog](#page-192-2) that you intend for row events to be decoded and displayed as commented SQL statements by also specifying the --verbose option. Like NEVER, DECODE-ROWS suppresses display of BINLOG statements, but unlike NEVER, it does not exit with an error if a row event is found.

For examples that show the effect of [--base64-output](#page-196-0) and --verbose on row event output, see Section 6.6.9.2, "mysqlbinlog Row Event Display".

<span id="page-197-0"></span>• [--bind-address=](#page-197-0)ip\_address

| Command-Line Format | bind-address=ip_address |
|---------------------|-------------------------|
|---------------------|-------------------------|

On a computer having multiple network interfaces, use this option to select which interface to use for connecting to the MySQL server.

<span id="page-197-1"></span>• [--binlog-row-event-max-size=](#page-197-1)N

| Command-Line Format | binlog-row-event-max-size=# |
|---------------------|-----------------------------|
| Type                | Numeric                     |
| Default Value       | 4294967040                  |
| Minimum Value       | 256                         |
| Maximum Value       | 18446744073709547520        |

Specify the maximum size of a row-based binary log event, in bytes. Rows are grouped into events smaller than this size if possible. The value should be a multiple of 256. The default is 4GB.

<span id="page-197-2"></span>• [--character-sets-dir=](#page-197-2)dir\_name

| Command-Line Format | character-sets-dir=dir_name |
|---------------------|-----------------------------|
| Type                | Directory name              |

The directory where character sets are installed. See Section 12.15, "Character Set Configuration".

<span id="page-197-3"></span>• [--compress](#page-197-3)

| Command-Line Format | compress[={OFF ON}] |
|---------------------|---------------------|
| Deprecated          | Yes                 |
| Type                | Boolean             |
| Default Value       | OFF                 |

Compress all information sent between the client and the server if possible. See Section 6.2.8, "Connection Compression Control".

This option is deprecated. Expect it to be removed in a future version of MySQL. See Configuring Legacy Connection Compression.

<span id="page-198-0"></span>• [--compression-algorithms=](#page-198-0)value

| Command-Line Format | compression-algorithms=value |
|---------------------|------------------------------|
| Type                | Set                          |
| Default Value       | uncompressed                 |
| Valid Values        | zlib                         |
|                     | zstd                         |
|                     | uncompressed                 |

The permitted compression algorithms for connections to the server. The available algorithms are the same as for the protocol\_compression\_algorithms system variable. The default value is uncompressed.

For more information, see Section 6.2.8, "Connection Compression Control".

<span id="page-198-1"></span>• [--connection-server-id=](#page-198-1)server\_id

| Command-Line Format | connection-server-id=#] |
|---------------------|-------------------------|
| Type                | Integer                 |
| Default Value       | 0 (1)                   |
| Minimum Value       | 0 (1)                   |
| Maximum Value       | 4294967295              |

[--connection-server-id](#page-198-1) specifies the server ID that [mysqlbinlog](#page-192-2) reports when it connects to the server. It can be used to avoid a conflict with the ID of a replica server or another [mysqlbinlog](#page-192-2) process.

If the --read-from-remote-server option is specified, [mysqlbinlog](#page-192-2) reports a server ID of 0, which tells the server to disconnect after sending the last log file (nonblocking behavior). If the - stop-never option is also specified to maintain the connection to the server, [mysqlbinlog](#page-192-2) reports a server ID of 1 by default instead of 0, and [--connection-server-id](#page-198-1) can be used to replace that server ID if required. See Section 6.6.9.4, "Specifying the mysqlbinlog Server ID".

<span id="page-198-2"></span>• [--database=](#page-198-2)db\_name, -d db\_name

| Command-Line Format | database=db_name |
|---------------------|------------------|
|                     |                  |

| Type | String |
|------|--------|
|      |        |

This option causes [mysqlbinlog](#page-192-2) to output entries from the binary log (local log only) that occur while db\_name is been selected as the default database by USE.

The [--database](#page-198-2) option for [mysqlbinlog](#page-192-2) is similar to the --binlog-do-db option for mysqld, but can be used to specify only one database. If [--database](#page-198-2) is given multiple times, only the last instance is used.

The effects of this option depend on whether the statement-based or row-based logging format is in use, in the same way that the effects of --binlog-do-db depend on whether statement-based or row-based logging is in use.

**Statement-based logging.** The [--database](#page-198-2) option works as follows:

- While db\_name is the default database, statements are output whether they modify tables in db\_name or a different database.
- Unless db\_name is selected as the default database, statements are not output, even if they modify tables in db\_name.
- There is an exception for CREATE DATABASE, ALTER DATABASE, and DROP DATABASE. The database being created, altered, or dropped is considered to be the default database when determining whether to output the statement.

Suppose that the binary log was created by executing these statements using statement-basedlogging:

```
INSERT INTO test.t1 (i) VALUES(100);
INSERT INTO db2.t2 (j) VALUES(200);
USE test;
INSERT INTO test.t1 (i) VALUES(101);
INSERT INTO t1 (i) VALUES(102);
INSERT INTO db2.t2 (j) VALUES(201);
USE db2;
INSERT INTO test.t1 (i) VALUES(103);
INSERT INTO db2.t2 (j) VALUES(202);
INSERT INTO t2 (j) VALUES(203);
```

[mysqlbinlog --database=test](#page-192-2) does not output the first two INSERT statements because there is no default database. It outputs the three INSERT statements following USE test, but not the three INSERT statements following USE db2.

[mysqlbinlog --database=db2](#page-192-2) does not output the first two INSERT statements because there is no default database. It does not output the three INSERT statements following USE test, but does output the three INSERT statements following USE db2.

**Row-based logging.** [mysqlbinlog](#page-192-2) outputs only entries that change tables belonging to db\_name. The default database has no effect on this. Suppose that the binary log just described was created using row-based logging rather than statement-based logging. [mysqlbinlog -](#page-192-2) [database=test](#page-192-2) outputs only those entries that modify t1 in the test database, regardless of whether USE was issued or what the default database is.

If a server is running with binlog\_format set to MIXED and you want it to be possible to use [mysqlbinlog](#page-192-2) with the [--database](#page-198-2) option, you must ensure that tables that are modified are in the database selected by USE. (In particular, no cross-database updates should be used.)

When used together with the --rewrite-db option, the --rewrite-db option is applied first; then the --database option is applied, using the rewritten database name. The order in which the options are provided makes no difference in this regard.

### <span id="page-0-0"></span>• --debug[=[debug\\_options](#page-0-0)], -# [debug\_options]

| Command-Line Format | debug[=debug_options]        |
|---------------------|------------------------------|
| Type                | String                       |
| Default Value       | d:t:o,/tmp/mysqlbinlog.trace |

Write a debugging log. A typical debug\_options string is d:t:o,file\_name. The default is d:t:o,/tmp/mysqlbinlog.trace.

This option is available only if MySQL was built using WITH\_DEBUG. MySQL release binaries provided by Oracle are not built using this option.

### <span id="page-0-1"></span>• [--debug-check](#page-0-1)

| Command-Line Format | debug-check |
|---------------------|-------------|
| Type                | Boolean     |
| Default Value       | FALSE       |

Print some debugging information when the program exits.

This option is available only if MySQL was built using WITH\_DEBUG. MySQL release binaries provided by Oracle are not built using this option.

### <span id="page-0-2"></span>• [--debug-info](#page-0-2)

| Command-Line Format | debug-info |
|---------------------|------------|
| Type                | Boolean    |
| Default Value       | FALSE      |

Print debugging information and memory and CPU usage statistics when the program exits.

This option is available only if MySQL was built using WITH\_DEBUG. MySQL release binaries provided by Oracle are not built using this option.

#### <span id="page-0-3"></span>• [--default-auth=](#page-0-3)plugin

| Command-Line Format | default-auth=plugin |
|---------------------|---------------------|
| Type                | String              |

A hint about which client-side authentication plugin to use. See Section 8.2.17, "Pluggable Authentication".

### <span id="page-0-4"></span>• [--defaults-extra-file=](#page-0-4)file\_name

| Command-Line Format | defaults-extra-file=file_name |
|---------------------|-------------------------------|
|---------------------|-------------------------------|

Read this option file after the global option file but (on Unix) before the user option file. If the file does not exist or is otherwise inaccessible, an error occurs. If file\_name is not an absolute path name, it is interpreted relative to the current directory.

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-1-0"></span>• [--defaults-file=](#page-1-0)file\_name

| Command-Line Format | defaults-file=file_name |
|---------------------|-------------------------|
| Type                | File name               |

Use only the given option file. If the file does not exist or is otherwise inaccessible, an error occurs. If file\_name is not an absolute path name, it is interpreted relative to the current directory.

Exception: Even with --defaults-file, client programs read .mylogin.cnf.

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-1-1"></span>• [--defaults-group-suffix=](#page-1-1)str

| Command-Line Format | defaults-group-suffix=str |
|---------------------|---------------------------|
| Type                | String                    |

Read not only the usual option groups, but also groups with the usual names and a suffix of str. For example, mysqlbinlog normally reads the [client] and [mysqlbinlog] groups. If this option is given as [--defaults-group-suffix=\\_other](#page-1-1), mysqlbinlog also reads the [client\_other] and [mysqlbinlog\_other] groups.

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-1-2"></span>• [--disable-log-bin](#page-1-2), -D

| Command-Line Format | disable-log-bin |
|---------------------|-----------------|
|---------------------|-----------------|

Disable binary logging. This is useful for avoiding an endless loop if you use the [--to-last](#page-13-0)[log](#page-13-0) option and are sending the output to the same MySQL server. This option also is useful when restoring after an unexpected exit to avoid duplication of the statements you have logged.

This option causes mysqlbinlog to include a SET sql\_log\_bin = 0 statement in its output to disable binary logging of the remaining output. Manipulating the session value of the sql\_log\_bin system variable is a restricted operation, so this option requires that you have privileges sufficient to set restricted session variables. See Section 7.1.9.1, "System Variable Privileges".

<span id="page-1-3"></span>• [--exclude-gtids=](#page-1-3)gtid\_set

| Command-Line Format | exclude-gtids=gtid_set |
|---------------------|------------------------|
| Type                | String                 |

| Default Value |  |
|---------------|--|
|---------------|--|

Do not display any of the groups listed in the gtid\_set.

<span id="page-2-0"></span>• [--force-if-open](#page-2-0), -F

| Command-Line Format | force-if-open |
|---------------------|---------------|
|---------------------|---------------|

Read binary log files even if they are open or were not closed properly (IN\_USE flag is set); do not fail if the file ends with a truncated event.

The IN\_USE flag is set only for the binary log that is currently written by the server; if the server has crashed, the flag remains set until the server is started up again and recovers the binary log. Without this option, mysqlbinlog refuses to process a file with this flag set. Since the server may be in the process of writing the file, truncation of the last event is considered normal.

<span id="page-2-1"></span>• [--force-read](#page-2-1), -f

With this option, if mysqlbinlog reads a binary log event that it does not recognize, it prints a warning, ignores the event, and continues. Without this option, mysqlbinlog stops if it reads such an event.

<span id="page-2-2"></span>• [--get-server-public-key](#page-2-2)

| Command-Line Format | get-server-public-key |
|---------------------|-----------------------|
| Type                | Boolean               |

Request from the server the public key required for RSA key pair-based password exchange. This option applies to clients that authenticate with the caching\_sha2\_password authentication plugin. For that plugin, the server does not send the public key unless requested. This option is ignored for accounts that do not authenticate with that plugin. It is also ignored if RSA-based password exchange is not used, as is the case when the client connects to the server using a secure connection.

If [--server-public-key-path=](#page-8-0)file\_name is given and specifies a valid public key file, it takes precedence over [--get-server-public-key](#page-2-2).

For information about the caching\_sha2\_password plugin, see Section 8.4.1.2, "Caching SHA-2 Pluggable Authentication".

<span id="page-2-3"></span>• [--hexdump](#page-2-3), -H

| Command-Line Format | hexdump |
|---------------------|---------|
|---------------------|---------|

Display a hex dump of the log in comments, as described in [Section 6.6.9.1, "mysqlbinlog Hex Dump](#page-15-0) [Format"](#page-15-0). The hex output can be helpful for replication debugging.

<span id="page-2-4"></span>• --host=[host\\_name](#page-2-4), -h host\_name

| Command-Line Format | host=host_name |
|---------------------|----------------|
| Type                | String         |
| Default Value       | localhost      |

Get the binary log from the MySQL server on the given host.

<span id="page-3-0"></span>• [--idempotent](#page-3-0)

| Command-Line Format | idempotent |
|---------------------|------------|
| Type                | Boolean    |
| Default Value       | true       |

Tell the MySQL Server to use idempotent mode while processing updates; this causes suppression of any duplicate-key or key-not-found errors that the server encounters in the current session while processing updates. This option may prove useful whenever it is desirable or necessary to replay one or more binary logs to a MySQL Server which may not contain all of the data to which the logs refer.

The scope of effect for this option includes the current mysqlbinlog client and session only.

<span id="page-3-1"></span>• [--include-gtids=](#page-3-1)gtid\_set

| Command-Line Format | include-gtids=gtid_set |
|---------------------|------------------------|
| Type                | String                 |
| Default Value       |                        |

Display only the groups listed in the gtid\_set.

<span id="page-3-2"></span>• [--local-load=](#page-3-2)dir\_name, -l dir\_name

| Command-Line Format | local-load=dir_name |
|---------------------|---------------------|
| Type                | Directory name      |

For data loading operations corresponding to LOAD DATA statements, mysqlbinlog extracts the files from the binary log events, writes them as temporary files to the local file system, and writes LOAD DATA LOCAL statements to cause the files to be loaded. By default, mysqlbinlog writes these temporary files to an operating system-specific directory. The [--local-load](#page-3-2) option can be used to explicitly specify the directory where mysqlbinlog should prepare local temporary files.

Because other processes can write files to the default system-specific directory, it is advisable to specify the [--local-load](#page-3-2) option to mysqlbinlog to designate a different directory for data files, and then designate that same directory by specifying the --load-data-local-dir option to mysql when processing the output from mysqlbinlog. For example:

```
mysqlbinlog --local-load=/my/local/data ...
 | mysql --load-data-local-dir=/my/local/data ...
```

![](_page_3_Picture_14.jpeg)

#### **Important**

These temporary files are not automatically removed by mysqlbinlog or any other MySQL program.

<span id="page-3-3"></span>• [--login-path=](#page-3-3)name

|  | Type | String |  |
|--|------|--------|--|
|--|------|--------|--|

Read options from the named login path in the .mylogin.cnf login path file. A "login path" is an option group containing options that specify which MySQL server to connect to and which account to authenticate as. To create or modify a login path file, use the mysql\_config\_editor utility. See Section 6.6.7, "mysql\_config\_editor — MySQL Configuration Utility".

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-4-0"></span>• [--no-login-paths](#page-4-0)

| Command-Line Format | no-login-paths |
|---------------------|----------------|
|---------------------|----------------|

Skips reading options from the login path file.

See [--login-path](#page-3-3) for related information.

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-4-1"></span>• [--no-defaults](#page-4-1)

| Command-Line Format | no-defaults |
|---------------------|-------------|
|---------------------|-------------|

Do not read any option files. If program startup fails due to reading unknown options from an option file, [--no-defaults](#page-4-1) can be used to prevent them from being read.

The exception is that the .mylogin.cnf file is read in all cases, if it exists. This permits passwords to be specified in a safer way than on the command line even when [--no-defaults](#page-4-1) is used. To create .mylogin.cnf, use the mysql\_config\_editor utility. See Section 6.6.7, "mysql\_config\_editor — MySQL Configuration Utility".

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-4-2"></span>• [--offset=](#page-4-2)N, -o N

| Command-Line Format | offset=# |
|---------------------|----------|
| Type                | Numeric  |

Skip the first N entries in the log.

<span id="page-4-3"></span>• [--open-files-limit=](#page-4-3)N

| Command-Line Format | open-files-limit=#   |
|---------------------|----------------------|
| Type                | Numeric              |
| Default Value       | 8                    |
| Minimum Value       | 1                    |
| Maximum Value       | [platform dependent] |

Specify the number of open file descriptors to reserve.

<span id="page-4-4"></span>• [--password\[=](#page-4-4)password], -p[password]

| Command-Line Format | password[=password] |
|---------------------|---------------------|
| Type                | String              |

The password of the MySQL account used for connecting to the server. The password value is optional. If not given, mysqlbinlog prompts for one. If given, there must be no space between [-](#page-4-4) [password=](#page-4-4) or -p and the password following it. If no password option is specified, the default is to send no password.

Specifying a password on the command line should be considered insecure. To avoid giving the password on the command line, use an option file. See Section 8.1.2.1, "End-User Guidelines for Password Security".

To explicitly specify that there is no password and that mysqlbinlog should not prompt for one, use the [--skip-password](#page-4-4) option.

<span id="page-5-0"></span>• [--plugin-dir=](#page-5-0)dir\_name

| Command-Line Format | plugin-dir=dir_name |
|---------------------|---------------------|
| Type                | Directory name      |

The directory in which to look for plugins. Specify this option if the [--default-auth](#page-0-3) option is used to specify an authentication plugin but mysqlbinlog does not find it. See Section 8.2.17, "Pluggable Authentication".

<span id="page-5-1"></span>• --port=[port\\_num](#page-5-1), -P port\_num

| Command-Line Format | port=port_num |
|---------------------|---------------|
| Type                | Numeric       |
| Default Value       | 3306          |

The TCP/IP port number to use for connecting to a remote server.

<span id="page-5-2"></span>• [--print-defaults](#page-5-2)

| Command-Line Format | print-defaults |
|---------------------|----------------|
|---------------------|----------------|

Print the program name and all options that it gets from option files.

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-5-3"></span>• [--print-table-metadata](#page-5-3)

| Command-Line Format | print-table-metadata |
|---------------------|----------------------|

<span id="page-5-4"></span>Print table related metadata from the binary log. Configure the amount of table related metadata binary logged using binlog-row-metadata.

| Default Value | [see text] |
|---------------|------------|
| Valid Values  | TCP        |
|               | SOCKET     |
|               | PIPE       |
|               | MEMORY     |

The transport protocol to use for connecting to the server. It is useful when the other connection parameters normally result in use of a protocol other than the one you want. For details on the permissible values, see Section 6.2.7, "Connection Transport Protocols".

#### <span id="page-6-0"></span>• [--raw](#page-6-0)

| Command-Line Format | raw     |
|---------------------|---------|
| Type                | Boolean |
| Default Value       | FALSE   |

By default, mysqlbinlog reads binary log files and writes events in text format. The [--raw](#page-6-0) option tells mysqlbinlog to write them in their original binary format. Its use requires that [--read-from](#page-6-1)[remote-server](#page-6-1) also be used because the files are requested from a server. mysqlbinlog writes one output file for each file read from the server. The [--raw](#page-6-0) option can be used to make a backup of a server's binary log. With the [--stop-never](#page-11-0) option, the backup is "live" because mysqlbinlog stays connected to the server. By default, output files are written in the current directory with the same names as the original log files. Output file names can be modified using the [--result-file](#page-7-0) option. For more information, see [Section 6.6.9.3, "Using mysqlbinlog to Back Up Binary Log Files"](#page-19-0).

#### <span id="page-6-2"></span>• [--read-from-remote-source=](#page-6-2)type

| Command-Line Format | read-from-remote-source=type |
|---------------------|------------------------------|
|---------------------|------------------------------|

This option reads binary logs from a MySQL server with the COM\_BINLOG\_DUMP or COM\_BINLOG\_DUMP\_GTID commands by setting the option value to either BINLOG-DUMP-NON-GTIDS or BINLOG-DUMP-GTIDS, respectively. If [--read-from-remote-source=BINLOG-](#page-6-2)[DUMP-GTIDS](#page-6-2) is combined with [--exclude-gtids](#page-1-3), transactions can be filtered out on the source, avoiding unnecessary network traffic.

The connection parameter options are used with these options or the [--read-from-remote](#page-6-1)[server](#page-6-1) option. These options are [--host](#page-2-4), [--password](#page-4-4), [--port](#page-5-1), [--protocol](#page-5-4), [--socket](#page-10-0), and [--user](#page-13-1). If none of the remote options is specified, the connection parameter options are ignored.

The REPLICATION SLAVE privilege is required to use these options.

#### <span id="page-6-3"></span>• [--read-from-remote-master=](#page-6-3)type

| Command-Line Format | read-from-remote-master=type |
|---------------------|------------------------------|
| Deprecated          | Yes                          |

Deprecated synonym for [--read-from-remote-source](#page-6-2).

#### <span id="page-6-1"></span>• [--read-from-remote-server=](#page-6-1)file\_name, -R

| Command-Line Format | read-from-remote-server=file_name |
|---------------------|-----------------------------------|
|                     |                                   |

Read the binary log from a MySQL server rather than reading a local log file. This option requires that the remote server be running. It works only for binary log files on the remote server and not relay log files. This accepts the binary log file name (including the numeric suffix) without the file path.

The connection parameter options are used with this option or the [--read-from-remote-source](#page-6-2) option. These options are [--host](#page-2-4), [--password](#page-4-4), [--port](#page-5-1), [--protocol](#page-5-4), [--socket](#page-10-0), and [--user](#page-13-1). If neither of the remote options is specified, the connection parameter options are ignored.

The REPLICATION SLAVE privilege is required to use this option.

This option is like [--read-from-remote-source=BINLOG-DUMP-NON-GTIDS](#page-6-2).

<span id="page-7-0"></span>• [--result-file=](#page-7-0)name, -r name

| Command-Line Format | result-file=name |
|---------------------|------------------|
|---------------------|------------------|

Without the [--raw](#page-6-0) option, this option indicates the file to which mysqlbinlog writes text output. With [--raw](#page-6-0), mysqlbinlog writes one binary output file for each log file transferred from the server, writing them by default in the current directory using the same names as the original log file. In this case, the [--result-file](#page-7-0) option value is treated as a prefix that modifies output file names.

<span id="page-7-1"></span>• [--require-row-format](#page-7-1)

| Command-Line Format | require-row-format |
|---------------------|--------------------|
| Type                | Boolean            |
| Default Value       | false              |

Require row-based binary logging format for events. This option enforces row-based replication events for mysqlbinlog output. The stream of events produced with this option would be accepted by a replication channel that is secured using the REQUIRE\_ROW\_FORMAT option of the CHANGE REPLICATION SOURCE TO statement. binlog\_format=ROW must be set on the server where the binary log was written. When you specify this option, mysqlbinlog stops with an error message if it encounters any events that are disallowed under the REQUIRE\_ROW\_FORMAT restrictions, including LOAD DATA INFILE instructions, creating or dropping temporary tables, INTVAR, RAND, or USER\_VAR events, and non-row-based events within a DML transaction. mysqlbinlog also prints a SET @@session.require\_row\_format statement at the start of its output to apply the restrictions when the output is executed, and does not print the SET @@session.pseudo\_thread\_id statement.

<span id="page-7-2"></span>• [--rewrite-db='](#page-7-2)from\_name->to\_name'

| Command-Line Format | rewrite-db='oldname->newname' |
|---------------------|-------------------------------|
| Type                | String                        |

| Default Value | [none] |
|---------------|--------|
|---------------|--------|

When reading from a row-based or statement-based log, rewrite all occurrences of from\_name to to\_name. Rewriting is done on the rows, for row-based logs, as well as on the USE clauses, for statement-based logs.

![](_page_8_Picture_3.jpeg)

#### **Warning**

Statements in which table names are qualified with database names are not rewritten to use the new name when using this option.

The rewrite rule employed as a value for this option is a string having the form 'from\_name- >to\_name', as shown previously, and for this reason must be enclosed by quotation marks.

To employ multiple rewrite rules, specify the option multiple times, as shown here:

```
mysqlbinlog --rewrite-db='dbcurrent->dbold' --rewrite-db='dbtest->dbcurrent' \
 binlog.00001 > /tmp/statements.sql
```

When used together with the --database option, the --rewrite-db option is applied first; then --database option is applied, using the rewritten database name. The order in which the options are provided makes no difference in this regard.

This means that, for example, if mysqlbinlog is started with --rewrite-db='mydb->yourdb' --database=yourdb, then all updates to any tables in databases mydb and yourdb are included in the output. On the other hand, if it is started with --rewrite-db='mydb->yourdb' - database=mydb, then mysqlbinlog outputs no statements at all: since all updates to mydb are first rewritten as updates to yourdb before applying the --database option, there remain no updates that match --database=mydb.

<span id="page-8-1"></span>• [--server-id=](#page-8-1)id

| Command-Line Format | server-id=id |
|---------------------|--------------|
| Type                | Numeric      |

Display only those events created by the server having the given server ID.

<span id="page-8-2"></span>• [--server-id-bits=](#page-8-2)N

| Command-Line Format | server-id-bits=# |
|---------------------|------------------|
| Type                | Numeric          |
| Default Value       | 32               |
| Minimum Value       | 7                |
| Maximum Value       | 32               |

Use only the first N bits of the server\_id to identify the server. If the binary log was written by a mysqld with server-id-bits set to less than 32 and user data stored in the most significant bit, running mysqlbinlog with --server-id-bits set to 32 enables this data to be seen.

This option is supported only by the version of mysqlbinlog supplied with the NDB Cluster distribution, or built with NDB Cluster support.

<span id="page-8-0"></span>• [--server-public-key-path=](#page-8-0)file\_name

The path name to a file in PEM format containing a client-side copy of the public key required by the server for RSA key pair-based password exchange. This option applies to clients that authenticate with the sha256\_password (deprecated) or caching\_sha2\_password authentication plugin. This option is ignored for accounts that do not authenticate with one of those plugins. It is also ignored if RSA-based password exchange is not used, as is the case when the client connects to the server using a secure connection.

If [--server-public-key-path=](#page-8-0)file\_name is given and specifies a valid public key file, it takes precedence over [--get-server-public-key](#page-2-2).

For sha256\_password (deprecated), this option applies only if MySQL was built using OpenSSL.

For information about the sha256\_password and caching\_sha2\_password plugins, see Section 8.4.1.3, "SHA-256 Pluggable Authentication", and Section 8.4.1.2, "Caching SHA-2 Pluggable Authentication".

<span id="page-9-0"></span>• [--set-charset=](#page-9-0)charset\_name

| Command-Line Format | set-charset=charset_name |
|---------------------|--------------------------|
| Type                | String                   |

Add a SET NAMES charset\_name statement to the output to specify the character set to be used for processing log files.

<span id="page-9-1"></span>• [--shared-memory-base-name=](#page-9-1)name

| Command-Line Format | shared-memory-base-name=name |
|---------------------|------------------------------|
| Platform Specific   | Windows                      |

On Windows, the shared-memory name to use for connections made using shared memory to a local server. The default value is MYSQL. The shared-memory name is case-sensitive.

This option applies only if the server was started with the shared\_memory system variable enabled to support shared-memory connections.

<span id="page-9-2"></span>• [--short-form](#page-9-2), -s

| Command-Line Format | short-form |
|---------------------|------------|
|---------------------|------------|

Display only the statements contained in the log, without any extra information or row-based events. This is for testing only, and should not be used in production systems. It is deprecated, and you should expect it to be removed in a future release.

<span id="page-9-3"></span>• [--skip-gtids\[=\(true|false\)\]](#page-9-3)

| Command-Line Format | skip-gtids[=true false] |
|---------------------|-------------------------|
| Type                | Boolean                 |
| Default Value       | false                   |

Do not include the GTIDs from the binary log files in the output dump file. For example:

mysqlbinlog --skip-gtids binlog.000001 > /tmp/dump.sql

```
mysql -u root -p -e "source /tmp/dump.sql"
```

You should not normally use this option in production or in recovery, except in the specific, and rare, scenarios where the GTIDs are actively unwanted. For example, an administrator might want to duplicate selected transactions (such as table definitions) from a deployment to another, unrelated, deployment that will not replicate to or from the original. In that scenario, [--skip-gtids](#page-9-3) can be used to enable the administrator to apply the transactions as if they were new, and ensure that the deployments remain unrelated. However, you should only use this option if the inclusion of the GTIDs causes a known issue for your use case.

<span id="page-10-0"></span>• [--socket=](#page-10-0)path, -S path

| Command-Line Format | socket={file_name pipe_name} |
|---------------------|------------------------------|
| Type                | String                       |

For connections to localhost, the Unix socket file to use, or, on Windows, the name of the named pipe to use.

On Windows, this option applies only if the server was started with the named\_pipe system variable enabled to support named-pipe connections. In addition, the user making the connection must be a member of the Windows group specified by the named\_pipe\_full\_access\_group system variable.

• --ssl\*

Options that begin with --ssl specify whether to connect to the server using encryption and indicate where to find SSL keys and certificates. See Command Options for Encrypted Connections.

<span id="page-10-1"></span>• [--ssl-fips-mode={OFF|ON|STRICT}](#page-10-1)

| Command-Line Format | ssl-fips-mode={OFF ON STRICT} |
|---------------------|-------------------------------|
| Deprecated          | Yes                           |
| Type                | Enumeration                   |
| Default Value       | OFF                           |
| Valid Values        | OFF                           |
|                     | ON                            |
|                     | STRICT                        |

Controls whether to enable FIPS mode on the client side. The [--ssl-fips-mode](#page-10-1) option differs from other --ssl-xxx options in that it is not used to establish encrypted connections, but rather to affect which cryptographic operations to permit. See Section 8.8, "FIPS Support".

These [--ssl-fips-mode](#page-10-1) values are permitted:

- OFF: Disable FIPS mode.
- ON: Enable FIPS mode.
- STRICT: Enable "strict" FIPS mode.

![](_page_10_Picture_16.jpeg)

#### **Note**

or STRICT causes the client to produce a warning at startup and to operate in non-FIPS mode.

This option is deprecated. Expect it to be removed in a future version of MySQL.

<span id="page-11-1"></span>• [--start-datetime=](#page-11-1)datetime

| Command-Line Format | start-datetime=datetime |
|---------------------|-------------------------|
| Type                | Datetime                |

Start reading the binary log at the first event having a timestamp equal to or later than the datetime argument. The datetime value is relative to the local time zone on the machine where you run mysqlbinlog. The value should be in a format accepted for the DATETIME or TIMESTAMP data types. For example:

```
mysqlbinlog --start-datetime="2005-12-25 11:25:56" binlog.000003
```

This option is useful for point-in-time recovery. See Section 9.5, "Point-in-Time (Incremental) Recovery".

<span id="page-11-2"></span>• [--start-position=](#page-11-2)N, -j N

| Command-Line Format | start-position=# |
|---------------------|------------------|
| Type                | Numeric          |

Start decoding the binary log at the log position N, including in the output any events that begin at position N or after. The position is a byte point in the log file, not an event counter; it needs to point to the starting position of an event to generate useful output. This option applies to the first log file named on the command line.

The maximum value supported for this option is 18446744073709551616 (264-1), unless [--read](#page-6-1)[from-remote-server](#page-6-1) or [--read-from-remote-source](#page-6-2) is also used, in which case the maximum is 4294967295.

This option is useful for point-in-time recovery. See Section 9.5, "Point-in-Time (Incremental) Recovery".

<span id="page-11-3"></span>• [--stop-datetime=](#page-11-3)datetime

| Command-Line Format | stop-datetime=datetime |
|---------------------|------------------------|
|---------------------|------------------------|

Stop reading the binary log at the first event having a timestamp equal to or later than the datetime argument. See the description of the [--start-datetime](#page-11-1) option for information about the datetime value.

This option is useful for point-in-time recovery. See Section 9.5, "Point-in-Time (Incremental) Recovery".

• [--stop-never](#page-11-0)

<span id="page-11-0"></span>

|     | Command-Line Format | stop-never |
|-----|---------------------|------------|
| 582 | Type                | Boolean    |

| Default Value | FALSE |  |
|---------------|-------|--|
|---------------|-------|--|

This option is used with [--read-from-remote-server](#page-6-1). It tells mysqlbinlog to remain connected to the server. Otherwise mysqlbinlog exits when the last log file has been transferred from the server. [--stop-never](#page-11-0) implies [--to-last-log](#page-13-0), so only the first log file to transfer need be named on the command line.

[--stop-never](#page-11-0) is commonly used with [--raw](#page-6-0) to make a live binary log backup, but also can be used without [--raw](#page-6-0) to maintain a continuous text display of log events as the server generates them.

With [--stop-never](#page-11-0), by default, mysqlbinlog reports a server ID of 1 when it connects to the server. Use --connection-server-id to explicitly specify an alternative ID to report. It can be used to avoid a conflict with the ID of a replica server or another mysqlbinlog process. See [Section 6.6.9.4, "Specifying the mysqlbinlog Server ID"](#page-22-0).

<span id="page-12-0"></span>• [--stop-never-slave-server-id=](#page-12-0)id

| Command-Line Format | stop-never-slave-server-id=# |
|---------------------|------------------------------|
| Type                | Numeric                      |
| Default Value       | 65535                        |
| Minimum Value       | 1                            |

This option is deprecated; expect it to be removed in a future release. Use the --connectionserver-id option instead to specify a server ID for mysqlbinlog to report.

<span id="page-12-1"></span>• [--stop-position=](#page-12-1)N

| Command-Line Format | stop-position=# |
|---------------------|-----------------|
| Type                | Numeric         |

Stop decoding the binary log at the log position N, excluding from the output any events that begin at position N or after. The position is a byte point in the log file, not an event counter; it needs to point to a spot after the starting position of the last event you want to include in the output. The event starting before position N and finishing at or after the position is the last event to be processed. This option applies to the last log file named on the command line.

This option is useful for point-in-time recovery. See Section 9.5, "Point-in-Time (Incremental) Recovery".

<span id="page-12-2"></span>• [--tls-ciphersuites=](#page-12-2)ciphersuite\_list

| Command-Line Format | tls-ciphersuites=ciphersuite_list |
|---------------------|-----------------------------------|
| Type                | String                            |

The permissible ciphersuites for encrypted connections that use TLSv1.3. The value is a list of one or more colon-separated ciphersuite names. The ciphersuites that can be named for this option depend on the SSL library used to compile MySQL. For details, see Section 8.3.2, "Encrypted Connection TLS Protocols and Ciphers".

<span id="page-12-3"></span>• [--tls-sni-servername=](#page-12-3)server\_name

|  |  | Type | String |
|--|--|------|--------|
|--|--|------|--------|

When specified, the name is passed to the libmysqlclient C API library using the MYSQL\_OPT\_TLS\_SNI\_SERVERNAME option of [mysql\\_options\(\)](https://dev.mysql.com/doc/c-api/8.4/en/mysql-options.md). The server name is not casesensitive. To show which server name the client specified for the current session, if any, check the Tls\_sni\_server\_name status variable.

Server Name Indication (SNI) is an extension to the TLS protocol (OpenSSL must be compiled using TLS extensions for this option to function). The MySQL implementation of SNI represents the clientside only.

<span id="page-13-2"></span>• [--tls-version=](#page-13-2)protocol\_list

| Command-Line Format | tls-version=protocol_list                                  |
|---------------------|------------------------------------------------------------|
| Type                | String                                                     |
| Default Value       | TLSv1,TLSv1.1,TLSv1.2,TLSv1.3<br>(OpenSSL 1.1.1 or higher) |
|                     | TLSv1,TLSv1.1,TLSv1.2 (otherwise)                          |

The permissible TLS protocols for encrypted connections. The value is a list of one or more commaseparated protocol names. The protocols that can be named for this option depend on the SSL library used to compile MySQL. For details, see Section 8.3.2, "Encrypted Connection TLS Protocols and Ciphers".

<span id="page-13-0"></span>• [--to-last-log](#page-13-0), -t

Do not stop at the end of the requested binary log from a MySQL server, but rather continue printing until the end of the last binary log. If you send the output to the same MySQL server, this may lead to an endless loop. This option requires [--read-from-remote-server](#page-6-1).

<span id="page-13-1"></span>• --user=[user\\_name](#page-13-1), -u user\_name

| Command-Line Format | user=user_name, |
|---------------------|-----------------|
| Type                | String          |

The user name of the MySQL account to use when connecting to a remote server.

If you are using the Rewriter plugin, you should grant this user the SKIP\_QUERY\_REWRITE privilege.

<span id="page-13-3"></span>• [--verbose](#page-13-3), -v

| Command-Line Format | verbose |
|---------------------|---------|
|---------------------|---------|

informational log events such as row query log events if the binlog\_rows\_query\_log\_events system variable is set to TRUE.

For examples that show the effect of --base64-output and --verbose on row event output, see Section 6.6.9.2, "mysqlbinlog Row Event Display".

<span id="page-14-0"></span>• --verify-binlog-checksum, -c

| Command-Line Format | verify-binlog-checksum |
|---------------------|------------------------|
|---------------------|------------------------|

Verify checksums in binary log files.

<span id="page-14-1"></span>• --version, -V

| Command-Line Format | version |
|---------------------|---------|

Display version information and exit.

<span id="page-14-2"></span>• --zstd-compression-level=*level* 

| Command-Line Format | zstd-compression-level=# |
|---------------------|--------------------------|
| Туре                | Integer                  |

The compression level to use for connections to the server that use the zstd compression algorithm. The permitted levels are from 1 to 22, with larger values indicating increasing levels of compression. The default zstd compression level is 3. The compression level setting has no effect on connections that do not use zstd compression.

For more information, see Section 6.2.8, "Connection Compression Control".

You can pipe the output of mysqlbinlog into the mysql client to execute the events contained in the binary log. This technique is used to recover from an unexpected exit when you have an old backup (see Section 9.5, "Point-in-Time (Incremental) Recovery"). For example:

```
mysqlbinlog binlog.000001 | mysql -u root -p
```

Or:

```
mysqlbinlog binlog.[0-9]* | mysql -u root -p
```

If the statements produced by <code>mysqlbinlog</code> may contain <code>BLOB</code> values, these may cause problems when <code>mysql</code> processes them. In this case, invoke <code>mysql</code> with the <code>--binary-mode</code> option.

You can also redirect the output of mysqlbinlog to a text file instead, if you need to modify the statement log first (for example, to remove statements that you do not want to execute for some reason). After editing the file, execute the statements that it contains by using it as input to the mysql program:

```
mysqlbinlog binlog.000001 > tmpfile
... edit tmpfile ...
mysql -u root -p < tmpfile</pre>
```

When mysqlbinlog is invoked with the --start-position option, it displays only those events with an offset in the binary log greater than or equal to a given position (the given position must mategrate the start of one event). It also has options to stop and start when it sees an event with a given date and time. This enables you to perform point-in-time recovery using the --stop-datetime option (to be able to say, for example, "roll forward my databases to how they were today at 10:30 a.m.").

**Processing multiple files.** If you have more than one binary log to execute on the MySQL server, the safe method is to process them all using a single connection to the server. Here is an example that demonstrates what may be unsafe:

```
mysqlbinlog binlog.000001 | mysql -u root -p # DANGER!!
mysqlbinlog binlog.000002 | mysql -u root -p # DANGER!!
```

Processing binary logs this way using multiple connections to the server causes problems if the first log file contains a CREATE TEMPORARY TABLE statement and the second log contains a statement that uses the temporary table. When the first mysql process terminates, the server drops the temporary table. When the second mysql process attempts to use the table, the server reports "unknown table."

To avoid problems like this, use a single mysql process to execute the contents of all binary logs that you want to process. Here is one way to do so:

```
mysqlbinlog binlog.000001 binlog.000002 | mysql -u root -p
```

Another approach is to write all the logs to a single file and then process the file:

```
mysqlbinlog binlog.000001 > /tmp/statements.sql
mysqlbinlog binlog.000002 >> /tmp/statements.sql
mysql -u root -p -e "source /tmp/statements.sql"
```

You can also supply multiple binary log files to mysqlbinlog as streamed input using a shell pipe. An archive of compressed binary log files can be decompressed and provided directly to mysqlbinlog. In this example, binlog-files\_1.gz contains multiple binary log files for processing. The pipeline extracts the contents of binlog-files\_1.gz, pipes the binary log files to mysqlbinlog as standard input, and pipes the output of mysqlbinlog into the mysql client for execution:

```
gzip -cd binlog-files_1.gz | ./mysqlbinlog - | ./mysql -uroot -p
```

You can specify more than one archive file, for example:

```
gzip -cd binlog-files_1.gz binlog-files_2.gz | ./mysqlbinlog - | ./mysql -uroot -p
```

For streamed input, do not use --stop-position, because mysqlbinlog cannot identify the last log file to apply this option.

**LOAD DATA operations.** mysqlbinlog can produce output that reproduces a LOAD DATA operation without the original data file. mysqlbinlog copies the data to a temporary file and writes a LOAD DATA LOCAL statement that refers to the file. The default location of the directory where these files are written is system-specific. To specify a directory explicitly, use the [--local-load](#page-3-2) option.

Because mysqlbinlog converts LOAD DATA statements to LOAD DATA LOCAL statements (that is, it adds LOCAL), both the client and the server that you use to process the statements must be configured with the LOCAL capability enabled. See Section 8.1.6, "Security Considerations for LOAD DATA LOCAL".

![](_page_15_Picture_15.jpeg)

#### **Warning**

The temporary files created for LOAD DATA LOCAL statements are not automatically deleted because they are needed until you actually execute those statements. You should delete the temporary files yourself after you no longer need the statement log. The files can be found in the temporary file directory and have names like original\_file\_name-#-#.

# <span id="page-15-0"></span>**6.6.9.1 mysqlbinlog Hex Dump Format**

The [--hexdump](#page-2-3) option causes mysqlbinlog to produce a hex dump of the binary log contents:

```
mysqlbinlog --hexdump source-bin.000001
```

The hex output consists of comment lines beginning with #, so the output might look like this for the preceding command:

```
/*!40019 SET @@SESSION.max_insert_delayed_threads=0*/;
/*!50003 SET @OLD_COMPLETION_TYPE=@@COMPLETION_TYPE,COMPLETION_TYPE=0*/;
# at 4
#051024 17:24:13 server id 1 end_log_pos 98
# Position Timestamp Type Master ID Size Master Pos Flags