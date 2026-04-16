---
source: MySQL 5.7 Reference
title: 00_Overview
---

[myisamchk](#page-156-6) supports the following options for table repair operations (operations performed when an option such as [--recover](#page-166-4) or [--safe-recover](#page-167-1) is given):

<span id="page-165-0"></span>• [--backup](#page-165-0), -B

| Command-Line Format | backup |
|---------------------|--------|
|---------------------|--------|

Make a backup of the .MYD file as file\_name-time.BAK

<span id="page-165-1"></span>• [--character-sets-dir=](#page-165-1)dir\_name

| Command-Line Format | character-sets-dir=path |
|---------------------|-------------------------|
| Type                | String                  |
| Default Value       | [none]                  |

The directory where character sets are installed. See Section 10.15, "Character Set Configuration".

<span id="page-165-2"></span>• [--correct-checksum](#page-165-2)

| Command-Line Format | correct-checksum |
|---------------------|------------------|
|---------------------|------------------|

Correct the checksum information for the table.

<span id="page-165-3"></span>• [--data-file-length=](#page-165-3)len, -D len

| Command-Line Format | data-file-length=len |
|---------------------|----------------------|
| Type                | Numeric              |

The maximum length of the data file (when re-creating data file when it is "full").

• [--extend-check](#page-164-1), -e

| 538 | Command-Line Format | extend-check |
|-----|---------------------|--------------|
|-----|---------------------|--------------|

Do a repair that tries to recover every possible row from the data file. Normally, this also finds a lot of

See also the description of this option under table checking options.

For a description of the output format, see [Section 4.6.3.5, "Obtaining Table Information with](#page-168-5) [myisamchk"](#page-168-5).

• [--force](#page-164-3), -f

| Command-Line Format | force |
|---------------------|-------|

Overwrite old intermediate files (files with names like tbl\_name.TMD) instead of aborting.

<span id="page-166-0"></span>• [--keys-used=](#page-166-0)val, -k val

| Command-Line Format | keys-used=val |
|---------------------|---------------|
| Type                | Numeric       |

For [myisamchk](#page-156-6), the option value is a bit value that indicates which indexes to update. Each binary bit of the option value corresponds to a table index, where the first index is bit 0. An option value of 0 disables updates to all indexes, which can be used to get faster inserts. Deactivated indexes can be reactivated by using [myisamchk -r](#page-156-6).

<span id="page-166-1"></span>• [--max-record-length=](#page-166-1)len

| Command-Line Format | max-record-length=len |
|---------------------|-----------------------|
| Type                | Numeric               |

Skip rows larger than the given length if [myisamchk](#page-156-6) cannot allocate memory to hold them.

<span id="page-166-2"></span>• [--parallel-recover](#page-166-2), -p

| Command-Line Format | parallel-recover |
|---------------------|------------------|
|---------------------|------------------|

![](_page_166_Picture_14.jpeg)

#### **Note**

This option is deprecated in MySQL 5.7.38 and removed in MySQL 5.7.39.

Use the same technique as -r and -n, but create all the keys in parallel, using different threads. This is beta-quality code. Use at your own risk!

<span id="page-166-3"></span>• [--quick](#page-166-3), -q

| Command-Line Format | quick |
|---------------------|-------|
|---------------------|-------|

Achieve a faster repair by modifying only the index file, not the data file. You can specify this option twice to force [myisamchk](#page-156-6) to modify the original data file in case of duplicate keys.

<span id="page-166-4"></span>• [--recover](#page-166-4), -r 539

| Command-Line Format | recover |
|---------------------|---------|
|---------------------|---------|

first. You should try [--safe-recover](#page-167-1) only if [myisamchk](#page-156-6) reports that the table cannot be recovered using [--recover](#page-166-4). (In the unlikely case that [--recover](#page-166-4) fails, the data file remains intact.)

If you have lots of memory, you should increase the value of myisam\_sort\_buffer\_size.

<span id="page-167-1"></span>• [--safe-recover](#page-167-1), -o

| Command-Line Format | safe-recover |
|---------------------|--------------|
|---------------------|--------------|

Do a repair using an old recovery method that reads through all rows in order and updates all index trees based on the rows found. This is an order of magnitude slower than [--recover](#page-166-4), but can handle a couple of very unlikely cases that [--recover](#page-166-4) cannot. This recovery method also uses much less disk space than [--recover](#page-166-4). Normally, you should repair first using [--recover](#page-166-4), and then with [--safe-recover](#page-167-1) only if [--recover](#page-166-4) fails.

If you have lots of memory, you should increase the value of key\_buffer\_size.

<span id="page-167-2"></span>• [--set-collation=](#page-167-2)name

| Command-Line Format | set-collation=name |
|---------------------|--------------------|
| Type                | String             |

Specify the collation to use for sorting table indexes. The character set name is implied by the first part of the collation name.

<span id="page-167-3"></span>• [--sort-recover](#page-167-3), -n

| Command-Line Format | sort-recover |
|---------------------|--------------|
|---------------------|--------------|

Force [myisamchk](#page-156-6) to use sorting to resolve the keys even if the temporary files would be very large.

<span id="page-167-4"></span>• [--tmpdir=](#page-167-4)dir\_name, -t dir\_name

| Command-Line Format | tmpdir=dir_name |
|---------------------|-----------------|
| Type                | Directory name  |

The path of the directory to be used for storing temporary files. If this is not set, [myisamchk](#page-156-6) uses the value of the TMPDIR environment variable. [--tmpdir](#page-167-4) can be set to a list of directory paths that are used successively in round-robin fashion for creating temporary files. The separator character between directory names is the colon (:) on Unix and the semicolon (;) on Windows.

<span id="page-167-5"></span>• [--unpack](#page-167-5), -u

| Command-Line Format | unpack |
|---------------------|--------|

Unpack a table that was packed with [myisampack](#page-176-0).

## <span id="page-167-0"></span>**4.6.3.4 Other myisamchk Options**

[myisamchk](#page-156-6) supports the following options for actions other than table checks and repairs:

• [--analyze](#page-167-0), -a

| Command-Line Format | analyze |
|---------------------|---------|
|---------------------|---------|

Analyze the distribution of key values. This improves join performance by enabling the join optimizer to better choose the order in which to join the tables and which indexes it should use. To obtain information about the key distribution, use a [myisamchk --description --verbose](#page-156-6) [tbl\\_name](#page-156-6) command or the SHOW INDEX FROM tbl\_name statement.

<span id="page-168-0"></span>• [--block-search=](#page-168-0)offset, -b offset

| Command-Line Format | block-search=offset |
|---------------------|---------------------|
| Type                | Numeric             |

Find the record that a block at the given offset belongs to.

<span id="page-168-1"></span>• [--description](#page-168-1), -d

| Command-Line Format | description |
|---------------------|-------------|
|---------------------|-------------|

Print some descriptive information about the table. Specifying the [--verbose](#page-162-0) option once or twice produces additional information. See [Section 4.6.3.5, "Obtaining Table Information with myisamchk".](#page-168-5)

<span id="page-168-2"></span>• [--set-auto-increment\[=](#page-168-2)value], -A[value]

Force AUTO\_INCREMENT numbering for new records to start at the given value (or higher, if there are existing records with AUTO\_INCREMENT values this large). If value is not specified, AUTO\_INCREMENT numbers for new records begin with the largest value currently in the table, plus one.

<span id="page-168-3"></span>• [--sort-index](#page-168-3), -S

| Command-Line Format | sort-index |
|---------------------|------------|
|---------------------|------------|

Sort the index tree blocks in high-low order. This optimizes seeks and makes table scans that use indexes faster.

<span id="page-168-4"></span>• [--sort-records=](#page-168-4)N, -R N

| Command-Line Format | sort-records=# |
|---------------------|----------------|
| Type                | Numeric        |

Sort records according to a particular index. This makes your data much more localized and may speed up range-based SELECT and ORDER BY operations that use this index. (The first time you use this option to sort a table, it may be very slow.) To determine a table's index numbers, use SHOW INDEX, which displays a table's indexes in the same order that [myisamchk](#page-156-6) sees them. Indexes are numbered beginning with 1.

If keys are not packed (PACK\_KEYS=0), they have the same length, so when [myisamchk](#page-156-6) sorts and moves records, it just overwrites record offsets in the index. If keys are packed (PACK\_KEYS=1), [myisamchk](#page-156-6) must unpack key blocks first, then re-create indexes and pack the key blocks again. (In this case, re-creating indexes is faster than updating offsets for each index.)

# <span id="page-168-5"></span>**4.6.3.5 Obtaining Table Information with myisamchk**

To obtain a description of a MyISAM table or statistics about it, use the commands shown here. The output from these commands is explained later in this section.

• [myisamchk -d](#page-156-6) tbl\_name

Runs [myisamchk](#page-156-6) in "describe mode" to produce a description of your table. If you start the MySQL server with external locking disabled, [myisamchk](#page-156-6) may report an error for a table that is updated while it runs. However, because [myisamchk](#page-156-6) does not change the table in describe mode, there is no risk of destroying data.

• [myisamchk -dv](#page-156-6) tbl\_name

Adding -v runs [myisamchk](#page-156-6) in verbose mode so that it produces more information about the table. Adding -v a second time produces even more information.

• [myisamchk -eis](#page-156-6) tbl\_name

Shows only the most important information from a table. This operation is slow because it must read the entire table.

• [myisamchk -eiv](#page-156-6) tbl\_name

This is like -eis, but tells you what is being done.

The tbl\_name argument can be either the name of a MyISAM table or the name of its index file, as described in [Section 4.6.3, "myisamchk — MyISAM Table-Maintenance Utility"](#page-156-6). Multiple tbl\_name arguments can be given.

Suppose that a table named person has the following structure. (The MAX\_ROWS table option is included so that in the example output from [myisamchk](#page-156-6) shown later, some values are smaller and fit the output format more easily.)

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

#### Example of [myisamchk -dvv](#page-156-6) output:

```
MyISAM file: person
Record format: Packed
Character set: latin1_swedish_ci (8)
File-version: 1
Creation time: 2009-08-19 16:47:41
Recover time: 2009-08-19 16:47:56
Status: checked,analyzed,optimized keys
Auto increment key: 1 Last value: 306688
Data records: 306688 Deleted blocks: 0
Datafile parts: 306688 Deleted data: 0
Datafile pointer (bytes): 4 Keyfile pointer (bytes): 3
Datafile length: 9347072 Keyfile length: 6066176
Max datafile length: 4294967294 Max keyfile length: 17179868159
Recordlength: 54
table description:
Key Start Len Index Type Rec/key Root Blocksize
1 2 4 unique long 1 99328 1024
2 6 20 multip. varchar prefix 512 3563520 1024
 27 20 varchar 512
3 48 3 multip. uint24 NULL 306688 6065152 1024
```

```
Field Start Length Nullpos Nullbit Type
1 1 1
2 2 4 no zeros
3 6 21 varchar
4 27 21 varchar
5 48 3 1 1 no zeros
6 51 3 1 2 no zeros
```

Explanations for the types of information [myisamchk](#page-156-6) produces are given here. "Keyfile" refers to the index file. "Record" and "row" are synonymous, as are "field" and "column."

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

How many deleted blocks still have reserved space. You can optimize your table to minimize this space. See Section 7.6.4, "MyISAM Table Optimization".

• Datafile parts

For dynamic-row format, this indicates how many data blocks there are. For an optimized table without fragmented rows, this is the same as Data records.

• Deleted data

How many bytes of unreclaimed deleted data there are. You can optimize your table to minimize this space. See Section 7.6.4, "MyISAM Table Optimization".

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

The table description part of the output includes a list of all keys in the table. For each key, [myisamchk](#page-156-6) displays some low-level information:

• Key

This key's number. This value is shown only for the first column of the key. If this value is missing, the line corresponds to the second or later column of a multiple-column key. For the table shown in the example, there are two table description lines for the second index. This indicates that it is a multiple-part index with two parts.

• Start

Where in the row this portion of the index starts.

• Len

How long this portion of the index is. For packed numbers, this should always be the full length of the column. For strings, it may be shorter than the full length of the indexed column, because you can index a prefix of a string column. The total length of a multiple-part key is the sum of the Len values for all key parts.

• Index

Whether a key value can exist multiple times in the index. Possible values are unique or multip. (multiple).

• Type

What data type this portion of the index has. This is a MyISAM data type with the possible values packed, stripped, or empty.

• Root

Address of the root index block.

• Blocksize

The size of each index block. By default this is 1024, but the value may be changed at compile time when MySQL is built from source.

• Rec/key

This is a statistical value used by the optimizer. It tells how many rows there are per value for this index. A unique index always has a value of 1. This may be updated after a table is loaded (or greatly changed) with [myisamchk -a](#page-156-6). If this is not updated at all, a default value of 30 is given.

The last part of the output provides information about each column:

• Field

The column number.

• Start

The byte position of the column within table rows.

• Length

The length of the column in bytes.

• Nullpos, Nullbit

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

The Huff tree and Bits fields are displayed if the table has been compressed with [myisampack](#page-176-0). See [Section 4.6.5, "myisampack — Generate Compressed, Read-Only MyISAM Tables"](#page-176-0), for an example of this information.

Example of [myisamchk -eiv](#page-156-6) output:

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

[myisamchk -eiv](#page-156-6) output includes the following information:

• Data records

The number of rows in the table.

• Deleted blocks

How many deleted blocks still have reserved space. You can optimize your table to minimize this space. See Section 7.6.4, "MyISAM Table Optimization".

• Key

The key number.

## • Keyblocks used

What percentage of the keyblocks are used. When a table has just been reorganized with [myisamchk](#page-156-6), the values are very high (very near theoretical maximum).

#### • Packed

MySQL tries to pack key values that have a common suffix. This can only be used for indexes on CHAR and VARCHAR columns. For long indexed strings that have similar leftmost parts, this can significantly reduce the space used. In the preceding example, the second key is 40 bytes long and a 97% reduction in space is achieved.

#### • Max levels

How deep the B-tree for this key is. Large tables with long key values get high values.

## • Records

How many rows are in the table.

#### • M.recordlength

The average row length. This is the exact row length for tables with fixed-length rows, because all rows have the same length.

#### • Packed

MySQL strips spaces from the end of strings. The Packed value indicates the percentage of savings achieved by doing this.

#### • Recordspace used

What percentage of the data file is used.

#### • Empty space

What percentage of the data file is unused.

## • Blocks/Record

Average number of blocks per row (that is, how many links a fragmented row is composed of). This is always 1.0 for fixed-format tables. This value should stay as close to 1.0 as possible. If it gets too large, you can reorganize the table. See Section 7.6.4, "MyISAM Table Optimization".

## • Recordblocks

How many blocks (links) are used. For fixed-format tables, this is the same as the number of rows.

#### • Deleteblocks

How many blocks (links) are deleted.

## • Recorddata

How many bytes in the data file are used.

#### • Deleted data

How many bytes in the data file are deleted (unused).

#### • Lost space

If a row is updated to a shorter length, some space is lost. This is the sum of all such losses, in bytes.

## • Linkdata

When the dynamic table format is used, row fragments are linked with pointers (4 to 7 bytes each). Linkdata is the sum of the amount of storage used by all such pointers.

## <span id="page-175-0"></span>**4.6.3.6 myisamchk Memory Usage**

Memory allocation is important when you run [myisamchk](#page-156-6). [myisamchk](#page-156-6) uses no more memory than its memory-related variables are set to. If you are going to use [myisamchk](#page-156-6) on very large tables, you should first decide how much memory you want it to use. The default is to use only about 3MB to perform repairs. By using larger values, you can get [myisamchk](#page-156-6) to operate faster. For example, if you have more than 512MB RAM available, you could use options such as these (in addition to any other options you might specify):

```
myisamchk --myisam_sort_buffer_size=256M \
 --key_buffer_size=512M \
 --read_buffer_size=64M \
 --write_buffer_size=64M ...
```

Using --myisam\_sort\_buffer\_size=16M is probably enough for most cases.

Be aware that [myisamchk](#page-156-6) uses temporary files in TMPDIR. If TMPDIR points to a memory file system, out of memory errors can easily occur. If this happens, run [myisamchk](#page-156-6) with the [--tmpdir=](#page-167-4)dir\_name option to specify a directory located on a file system that has more space.

When performing repair operations, [myisamchk](#page-156-6) also needs a lot of disk space:

- Twice the size of the data file (the original file and a copy). This space is not needed if you do a repair with [--quick](#page-166-3); in this case, only the index file is re-created. This space must be available on the same file system as the original data file, as the copy is created in the same directory as the original.
- Space for the new index file that replaces the old one. The old index file is truncated at the start of the repair operation, so you usually ignore this space. This space must be available on the same file system as the original data file.
- When using [--recover](#page-166-4) or [--sort-recover](#page-167-3) (but not when using [--safe-recover](#page-167-1)), you need space on disk for sorting. This space is allocated in the temporary directory (specified by TMPDIR or [--tmpdir=](#page-167-4)dir\_name). The following formula yields the amount of space required:

```
(largest_key + row_pointer_length) * number_of_rows * 2
```

You can check the length of the keys and the row\_pointer\_length with [myisamchk](#page-156-6)  dv [tbl\\_name](#page-156-6) (see [Section 4.6.3.5, "Obtaining Table Information with myisamchk"\)](#page-168-5). The row\_pointer\_length and number\_of\_rows values are the Datafile pointer and Data records values in the table description. To determine the largest\_key value, check the Key lines in the table description. The Len column indicates the number of bytes for each key part. For a multiple-column index, the key size is the sum of the Len values for all key parts.

If you have a problem with disk space during repair, you can try [--safe-recover](#page-167-1) instead of [-](#page-166-4) [recover](#page-166-4).

# <span id="page-175-1"></span>**4.6.4 myisamlog — Display MyISAM Log File Contents**

[myisamlog](#page-175-1) processes the contents of a MyISAM log file. To create such a file, start the server with a --log-isam=log\_file option.

Invoke [myisamlog](#page-175-1) like this:

```
myisamlog [options] [file_name [tbl_name] ...]
```

The default operation is update (-u). If a recovery is done (-r), all writes and possibly updates and deletes are done and errors are only counted. The default log file name is myisam.log if no log\_file argument is given. If tables are named on the command line, only those tables are updated. [myisamlog](#page-175-1) supports the following options:

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

# <span id="page-176-0"></span>**4.6.5 myisampack — Generate Compressed, Read-Only MyISAM Tables**

The [myisampack](#page-176-0) utility compresses MyISAM tables. [myisampack](#page-176-0) works by compressing each column in the table separately. Usually, [myisampack](#page-176-0) packs the data file 40% to 70%.

When the table is used later, the server reads into memory the information needed to decompress columns. This results in much better performance when accessing individual rows, because you only have to uncompress exactly one row.

MySQL uses mmap() when possible to perform memory mapping on compressed tables. If mmap() does not work, MySQL falls back to normal read/write file operations.

Please note the following:

- If the mysqld server was invoked with external locking disabled, it is not a good idea to invoke [myisampack](#page-176-0) if the table might be updated by the server during the packing process. It is safest to compress tables with the server stopped.
- After packing a table, it becomes read only. This is generally intended (such as when accessing packed tables on a CD).
- [myisampack](#page-176-0) does not support partitioned tables.

Invoke [myisampack](#page-176-0) like this:

```
myisampack [options] file_name ...
```

Each file name argument should be the name of an index (.MYI) file. If you are not in the database directory, you should specify the path name to the file. It is permissible to omit the .MYI extension.

After you compress a table with [myisampack](#page-176-0), use [myisamchk -rq](#page-156-6) to rebuild its indexes. [Section 4.6.3, "myisamchk — MyISAM Table-Maintenance Utility".](#page-156-6)

[myisampack](#page-176-0) supports the following options. It also reads option files and supports the options for processing them described at Section 4.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-177-0"></span>• [--help](#page-177-0), -?

| Command-Line Format | help |
|---------------------|------|
|---------------------|------|

Display a help message and exit.

<span id="page-177-1"></span>• [--backup](#page-177-1), -b

| Command-Line Format | backup |
|---------------------|--------|
|---------------------|--------|

Make a backup of each table's data file using the name tbl\_name.OLD.

<span id="page-177-2"></span>• [--character-sets-dir=](#page-177-2)dir\_name

| Command-Line Format | character-sets-dir=dir_name |
|---------------------|-----------------------------|
| Type                | Directory name              |

The directory where character sets are installed. See Section 10.15, "Character Set Configuration".

<span id="page-177-3"></span>• --debug[=[debug\\_options](#page-177-3)], -# [debug\_options]

| Command-Line Format | debug[=debug_options] |
|---------------------|-----------------------|
| Type                | String                |
| Default Value       | d:t:o                 |

Write a debugging log. A typical debug\_options string is d:t:o,file\_name. The default is d:t:o.

This option is available only if MySQL was built using WITH\_DEBUG. MySQL release binaries provided by Oracle are not built using this option.

<span id="page-178-0"></span>• [--force](#page-178-0), -f

| Command-Line Format | force |
|---------------------|-------|
|---------------------|-------|

Produce a packed table even if it becomes larger than the original or if the intermediate file from an earlier invocation of [myisampack](#page-176-0) exists. ([myisampack](#page-176-0) creates an intermediate file named tbl\_name.TMD in the database directory while it compresses the table. If you kill [myisampack](#page-176-0), the .TMD file might not be deleted.) Normally, [myisampack](#page-176-0) exits with an error if it finds that tbl\_name.TMD exists. With [--force](#page-178-0), [myisampack](#page-176-0) packs the table anyway.

<span id="page-178-1"></span>• --join=[big\\_tbl\\_name](#page-178-1), -j big\_tbl\_name

| Command-Line Format | join=big_tbl_name |
|---------------------|-------------------|
| Type                | String            |

Join all tables named on the command line into a single packed table big\_tbl\_name. All tables that are to be combined must have identical structure (same column names and types, same indexes, and so forth).

big\_tbl\_name must not exist prior to the join operation. All source tables named on the command line to be merged into big\_tbl\_name must exist. The source tables are read for the join operation but not modified.

<span id="page-178-2"></span>• [--silent](#page-178-2), -s

| Command-Line Format | silent |
|---------------------|--------|
|---------------------|--------|

Silent mode. Write output only when errors occur.

<span id="page-178-3"></span>• [--test](#page-178-3), -t

| Command-Line Format | test |
|---------------------|------|
|---------------------|------|

Do not actually pack the table, just test packing it.

<span id="page-178-4"></span>• [--tmpdir=](#page-178-4)dir\_name, -T dir\_name

| Command-Line Format | tmpdir=dir_name |
|---------------------|-----------------|
| Type                | Directory name  |

Use the named directory as the location where [myisampack](#page-176-0) creates temporary files.

<span id="page-178-5"></span>• [--verbose](#page-178-5), -v

| Command-Line Format | verbose |
|---------------------|---------|

Verbose mode. Write information about the progress of the packing operation and its result.

<span id="page-178-6"></span>• [--version](#page-178-6), -V

| Command-Line Format | version |
|---------------------|---------|

Display version information and exit.

<span id="page-179-0"></span>• [--wait](#page-179-0), -w

```
Command-Line Format --wait
```

Wait and retry if the table is in use. If the mysqld server was invoked with external locking disabled, it is not a good idea to invoke [myisampack](#page-176-0) if the table might be updated by the server during the packing process.

The following sequence of commands illustrates a typical table compression session:

```
$> ls -l station.*
-rw-rw-r-- 1 jones my 994128 Apr 17 19:00 station.MYD
-rw-rw-r-- 1 jones my 53248 Apr 17 19:00 station.MYI
-rw-rw-r-- 1 jones my 5767 Apr 17 19:00 station.frm
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
```

```
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
-rw-rw-r-- 1 jones my 5767 Apr 17 19:00 station.frm
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
```

```
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
41 417 4 always zero 2 9
42 421 4 no zeros 2 9
43 425 4 always zero 2 9
44 429 20 no empty 3 9
45 449 30 no empty 3 9
46 479 1 14 4
47 480 1 14 4
48 481 79 no endspace, no empty 15 9
49 560 79 no empty 2 9
50 639 79 no empty 2 9
51 718 79 no endspace 16 9
52 797 8 no empty 2 9
53 805 1 17 1
54 806 1 3 9
55 807 20 no empty 3 9
56 827 4 no zeros, zerofill(2) 2 9
57 831 4 no zeros, zerofill(1) 2 9
```

[myisampack](#page-176-0) displays the following kinds of information:

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

After a table has been compressed, the Field lines displayed by [myisamchk -dvv](#page-156-6) include additional information about each column:

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

After you run [myisampack](#page-176-0), use [myisamchk](#page-156-6) to re-create any indexes. At this time, you can also sort the index blocks and create statistics needed for the MySQL optimizer to work more efficiently:

```
myisamchk -rq --sort-index --analyze tbl_name.MYI
```

After you have installed the packed table into the MySQL database directory, you should execute [mysqladmin flush-tables](#page-30-0) to force mysqld to start using the new table.

To unpack a packed table, use the [--unpack](#page-167-5) option to [myisamchk](#page-156-6).

# <span id="page-183-0"></span>**4.6.6 mysql\_config\_editor — MySQL Configuration Utility**

The [mysql\\_config\\_editor](#page-183-0) utility enables you to store authentication credentials in an obfuscated login path file named .mylogin.cnf. The file location is the %APPDATA%\MySQL directory on Windows and the current user's home directory on non-Windows systems. The file can be read later by MySQL client programs to obtain authentication credentials for connecting to MySQL Server.

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

When you invoke a client program to connect to the server, the client uses .mylogin.cnf in conjunction with other option files. Its precedence is higher than other option files, but less than options specified explicitly on the client command line. For information about the order in which option files are used, see Section 4.2.2.2, "Using Option Files".

To specify an alternate login path file name, set the MYSQL\_TEST\_LOGIN\_FILE environment variable. This variable is recognized by [mysql\\_config\\_editor](#page-183-0), by standard MySQL clients (mysql, [mysqladmin](#page-30-0), and so forth), and by the mysql-test-run.pl testing utility.

Programs use groups in the login path file as follows:

- [mysql\\_config\\_editor](#page-183-0) operates on the client login path by default if you specify no --loginpath=name option to indicate explicitly which login path to use.
- Without a --login-path option, client programs read the same option groups from the login path file that they read from other option files. Consider this command:

mysql

By default, the mysql client reads the [client] and [mysql] groups from other option files, so it reads them from the login path file as well.

• With a --login-path option, client programs additionally read the named login path from the login path file. The option groups read from other option files remain the same. Consider this command:

```
mysql --login-path=mypath
```

The mysql client reads [client] and [mysql] from other option files, and [client], [mysql], and [mypath] from the login path file.

• Client programs read the login path file even when the --no-defaults option is used, unless [--no-login-paths](https://dev.mysql.com/doc/refman/8.4/en/option-file-options.md#option_general_no-login-paths) is set. This permits passwords to be specified in a safer way than on the command line even if --no-defaults is present.

[mysql\\_config\\_editor](#page-183-0) obfuscates the .mylogin.cnf file so it cannot be read as cleartext, and its contents when unobfuscated by client programs are used only in memory. In this way, passwords can be stored in a file in non-cleartext format and used later without ever needing to be exposed on the command line or in an environment variable. [mysql\\_config\\_editor](#page-183-0) provides a print command for displaying the login path file contents, but even in this case, password values are masked so as never to appear in a way that other users can see them.

The obfuscation used by [mysql\\_config\\_editor](#page-183-0) prevents passwords from appearing in .mylogin.cnf as cleartext and provides a measure of security by preventing inadvertent password exposure. For example, if you display a regular unobfuscated my.cnf option file on the screen, any passwords it contains are visible for anyone to see. With .mylogin.cnf, that is not true, but the obfuscation used is not likely to deter a determined attacker and you should not consider it unbreakable. A user who can gain system administration privileges on your machine to access your files could unobfuscate the .mylogin.cnf file with some effort.

The login path file must be readable and writable to the current user, and inaccessible to other users. Otherwise, [mysql\\_config\\_editor](#page-183-0) ignores it, and client programs do not use it, either.

Invoke [mysql\\_config\\_editor](#page-183-0) like this:

```
mysql_config_editor [program_options] command [command_options]
```

If the login path file does not exist, [mysql\\_config\\_editor](#page-183-0) creates it.

Command arguments are given as follows:

- program\_options consists of general [mysql\\_config\\_editor](#page-183-0) options.
- command indicates what action to perform on the .mylogin.cnf login path file. For example, set writes a login path to the file, remove removes a login path, and print displays login path contents.
- command\_options indicates any additional options specific to the command, such as the login path name and the values to use in the login path.

The position of the command name within the set of program arguments is significant. For example, these command lines have the same arguments, but produce different results:

```
mysql_config_editor --help set
mysql_config_editor set --help
```

The first command line displays a general [mysql\\_config\\_editor](#page-183-0) help message, and ignores the set command. The second command line displays a help message specific to the set command.

Suppose that you want to establish a client login path that defines your default connection parameters, and an additional login path named remote for connecting to the MySQL server the host remote.example.com. You want to log in as follows:

• By default, to the local server with a user name and password of localuser and localpass

• To the remote server with a user name and password of remoteuser and remotepass

To set up the login paths in the .mylogin.cnf file, use the following set commands. Enter each command on a single line, and enter the appropriate passwords when prompted:

```
$> mysql_config_editor set --login-path=client
 --host=localhost --user=localuser --password
Enter password: enter password "localpass" here
$> mysql_config_editor set --login-path=remote
 --host=remote.example.com --user=remoteuser --password
Enter password: enter password "remotepass" here
```

[mysql\\_config\\_editor](#page-183-0) uses the client login path by default, so the --login-path=client option can be omitted from the first command without changing its effect.

To see what [mysql\\_config\\_editor](#page-183-0) writes to the .mylogin.cnf file, use the print command:

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

As shown by the preceding example, the login path file can contain multiple login paths. In this way, [mysql\\_config\\_editor](#page-183-0) makes it easy to set up multiple "personalities" for connecting to different MySQL servers, or for connecting to a given server using different accounts. Any of these can be selected by name later using the --login-path option when you invoke a client program. For example, to connect to the remote server, use this command:

```
mysql --login-path=remote
```

Here, mysql reads the [client] and [mysql] option groups from other option files, and the [client], [mysql], and [remote] groups from the login path file.

To connect to the local server, use this command:

```
mysql --login-path=client
```

Because mysql reads the client and mysql login paths by default, the --login-path option does not add anything in this case. That command is equivalent to this one:

```
mysql
```

Options read from the login path file take precedence over options read from other option files. Options read from login path groups appearing later in the login path file take precedence over options read from groups appearing earlier in the file.

[mysql\\_config\\_editor](#page-183-0) adds login paths to the login path file in the order you create them, so you should create more general login paths first and more specific paths later. If you need to move a login path within the file, you can remove it, then recreate it to add it to the end. For example, a client login path is more general because it is read by all client programs, whereas a mysqldump login path is read only by [mysqldump](#page-57-0). Options specified later override options specified earlier, so putting the login paths in the order client, mysqldump enables [mysqldump](#page-57-0)-specific options to override client options.

When you use the set command with [mysql\\_config\\_editor](#page-183-0) to create a login path, you need not specify all possible option values (host name, user name, password, port, socket). Only those values given are written to the path. Any missing values required later can be specified when you invoke a client path to connect to the MySQL server, either in other option files or on the command line. Any options specified on the command line override those specified in the login path file or other option files. For example, if the credentials in the remote login path also apply for the host remote2.example.com, connect to the server on that host like this:

mysql --login-path=remote --host=remote2.example.com

## <span id="page-186-4"></span>**mysql\_config\_editor General Options**

[mysql\\_config\\_editor](#page-183-0) supports the following general options, which may be used preceding any command named on the command line. For descriptions of command-specific options, see [mysql\\_config\\_editor Commands and Command-Specific Options.](#page-187-0)

#### **Table 4.22 mysql\_config\_editor General Options**

| Option Name | Description                          |
|-------------|--------------------------------------|
| debug       | Write debugging log                  |
| help        | Display help message and exit        |
| verbose     | Verbose mode                         |
| version     | Display version information and exit |

<span id="page-186-1"></span>• [--help](#page-186-1), -?

| Command-Line Format | help |
|---------------------|------|
|---------------------|------|

Display a general help message and exit.

To see a command-specific help message, invoke [mysql\\_config\\_editor](#page-183-0) as follows, where command is a command other than help:

mysql\_config\_editor command --help

<span id="page-186-0"></span>• --debug[=[debug\\_options](#page-186-0)], -# debug\_options

| Command-Line Format | debug[=debug_options] |  |
|---------------------|-----------------------|--|
| Type                | String                |  |
| Default Value       | d:t:o                 |  |

Write a debugging log. A typical debug\_options string is d:t:o,file\_name. The default is d:t:o,/tmp/mysql\_config\_editor.trace.

This option is available only if MySQL was built using WITH\_DEBUG. MySQL release binaries provided by Oracle are not built using this option.

<span id="page-186-2"></span>• [--verbose](#page-186-2), -v

| Command-Line Format | verbose |
|---------------------|---------|
|---------------------|---------|

Verbose mode. Print more information about what the program does. This option may be helpful in diagnosing problems if an operation does not have the effect you expect.

<span id="page-186-3"></span>• [--version](#page-186-3), -V

| Command-Line Format | version |
|---------------------|---------|
|                     |         |

Display version information and exit.

## <span id="page-187-0"></span>**mysql\_config\_editor Commands and Command-Specific Options**

This section describes the permitted [mysql\\_config\\_editor](#page-183-0) commands, and, for each one, the command-specific options permitted following the command name on the command line.

In addition, [mysql\\_config\\_editor](#page-183-0) supports general options that can be used preceding any command. For descriptions of these options, see [mysql\\_config\\_editor General Options.](#page-186-4)

[mysql\\_config\\_editor](#page-183-0) supports these commands:

• help

Display a general help message and exit. This command takes no following options.

To see a command-specific help message, invoke [mysql\\_config\\_editor](#page-183-0) as follows, where command is a command other than help:

```
mysql_config_editor command --help
```

• print [options]

Print the contents of the login path file in unobfuscated form, with the exception that passwords are displayed as \*\*\*\*\*.

The default login path name is client if no login path is named. If both --all and --login-path are given, --all takes precedence.

The print command permits these options following the command name:

• --help, -?

Display a help message for the print command and exit.

To see a general help message, use [mysql\\_config\\_editor --help](#page-183-0).

• --all

Print the contents of all login paths in the login path file.

• --login-path=name, -G name

Print the contents of the named login path.

• remove [options]

Remove a login path from the login path file, or modify a login path by removing options from it.

This command removes from the login path only such options as are specified with the --host, - password, --port, --socket, and --user options. If none of those options are given, remove removes the entire login path. For example, this command removes only the user option from the mypath login path rather than the entire mypath login path:

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

To see a general help message, use [mysql\\_config\\_editor --help](#page-183-0).

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

To see a general help message, use [mysql\\_config\\_editor --help](#page-183-0).

• set [options]

Write a login path to the login path file.

This command writes to the login path only such options as are specified with the --host, --password, --port, --socket, and --user options. If none of those options are given, [mysql\\_config\\_editor](#page-183-0) writes the login path as an empty group.

The set command permits these options following the command name:

• --help, -?

Display a help message for the set command and exit.

To see a general help message, use [mysql\\_config\\_editor --help](#page-183-0).

• --host=host\_name, -h host\_name

The host name to write to the login path.

• --login-path=name, -G name

The login path to create. The default login path name is client if this option is not given.

• --password, -p

Prompt for a password to write to the login path. After [mysql\\_config\\_editor](#page-183-0) displays the prompt, type the password and press Enter. To prevent other users from seeing the password, [mysql\\_config\\_editor](#page-183-0) does not echo it.

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

# <span id="page-189-0"></span>**4.6.7 mysqlbinlog — Utility for Processing Binary Log Files**

The server's binary log consists of files containing "events" that describe modifications to database contents. The server writes these files in binary format. To display their contents in text format, use the [mysqlbinlog](#page-189-0) utility. You can also use [mysqlbinlog](#page-189-0) to display the contents of relay log files written by a replica server in a replication setup because relay logs have the same format as binary logs. The binary log and relay log are discussed further in Section 5.4.4, "The Binary Log", and Section 16.2.4, "Relay Log and Replication Metadata Repositories".

Invoke [mysqlbinlog](#page-189-0) like this:

```
mysqlbinlog [options] log_file ...
```

For example, to display the contents of the binary log file named binlog.000003, use this command:

```
mysqlbinlog binlog.000003
```

The output includes events contained in binlog.000003. For statement-based logging, event information includes the SQL statement, the ID of the server on which it was executed, the timestamp when the statement was executed, how much time it took, and so forth. For row-based logging, the event indicates a row change rather than an SQL statement. See Section 16.2.1, "Replication Formats", for information about logging modes.

Events are preceded by header comments that provide additional information. For example:

```
# at 141
#100309 9:28:36 server id 123 end_log_pos 245
 Query thread_id=3350 exec_time=11 error_code=0
```

In the first line, the number following at indicates the file offset, or starting position, of the event in the binary log file.

The second line starts with a date and time indicating when the statement started on the server where the event originated. For replication, this timestamp is propagated to replica servers. server id is the server\_id value of the server where the event originated. end\_log\_pos indicates where the next event starts (that is, it is the end position of the current event + 1). thread\_id indicates which thread executed the event. exec\_time is the time spent executing the event, on a replication source server. On a replica, it is the difference of the end execution time on the replica minus the beginning execution time on the source. The difference serves as an indicator of how much replication lags behind the source. error\_code indicates the result from executing the event. Zero means that no error occurred.

![](_page_190_Picture_5.jpeg)

#### **Note**

When using event groups, the file offsets of events may be grouped together and the comments of events may be grouped together. Do not mistake these grouped events for blank file offsets.

The output from [mysqlbinlog](#page-189-0) can be re-executed (for example, by using it as input to mysql) to redo the statements in the log. This is useful for recovery operations after an unexpected server exit. For other usage examples, see the discussion later in this section and in Section 7.5, "Point-in-Time (Incremental) Recovery".

You can use [mysqlbinlog](#page-189-0) to read binary log files directly and apply them to the local MySQL server. You can also read binary logs from a remote server by using the --read-from-remote-server option. To read remote binary logs, the connection parameter options can be given to indicate how to connect to the server. These options are [--host](#page-199-0), --password, --port, --protocol, --socket, and --user.

When running [mysqlbinlog](#page-189-0) against a large binary log, be careful that the filesystem has enough space for the resulting files. To configure the directory that [mysqlbinlog](#page-189-0) uses for temporary files, use the TMPDIR environment variable.

[mysqlbinlog](#page-189-0) sets the value of pseudo\_slave\_mode to true before executing any SQL statements. This system variable affects the handling of XA transactions.

[mysqlbinlog](#page-189-0) supports the following options, which can be specified on the command line or in the [mysqlbinlog] and [client] groups of an option file. For information about option files used by MySQL programs, see Section 4.2.2.2, "Using Option Files".

| Table 4.23 mysqlbinlog Options |  |
|--------------------------------|--|
|--------------------------------|--|

| Option Name               | Description                                                                                        | Deprecated |
|---------------------------|----------------------------------------------------------------------------------------------------|------------|
| base64-output             | Print binary log entries using<br>base-64 encoding                                                 |            |
| bind-address              | Use specified network interface<br>to connect to MySQL Server                                      |            |
| binlog-row-event-max-size | Binary log max event size                                                                          |            |
| character-sets-dir        | Directory where character sets<br>are installed                                                    |            |
| connection-server-id      | Used for testing and debugging.<br>See text for applicable default<br>values and other particulars |            |
| database                  | List entries for just this database                                                                |            |

| Option Name           | Description                                                                                                 | Deprecated |
|-----------------------|-------------------------------------------------------------------------------------------------------------|------------|
| debug                 | Write debugging log                                                                                         |            |
| debug-check           | Print debugging information<br>when program exits                                                           |            |
| debug-info            | Print debugging information,<br>memory, and CPU statistics<br>when program exits                            |            |
| default-auth          | Authentication plugin to use                                                                                |            |
| defaults-extra-file   | Read named option file in<br>addition to usual option files                                                 |            |
| defaults-file         | Read only named option file                                                                                 |            |
| defaults-group-suffix | Option group suffix value                                                                                   |            |
| disable-log-bin       | Disable binary logging                                                                                      |            |
| exclude-gtids         | Do not show any of the groups in<br>the GTID set provided                                                   |            |
| force-if-open         | Read binary log files even if open<br>or not closed properly                                                |            |
| force-read            | If mysqlbinlog reads a binary log<br>event that it does not recognize,<br>it prints a warning               |            |
| get-server-public-key | Request RSA public key from<br>server                                                                       |            |
| help                  | Display help message and exit                                                                               |            |
| hexdump               | Display a hex dump of the log in<br>comments                                                                |            |
| host                  | Host on which MySQL server is<br>located                                                                    |            |
| idempotent            | Cause the server to use<br>idempotent mode while<br>processing binary log updates<br>from this session only |            |
| include-gtids         | Show only the groups in the<br>GTID set provided                                                            |            |
| local-load            | Prepare local temporary files<br>for LOAD DATA in the specified<br>directory                                |            |
| login-path            | Read login path options<br>from .mylogin.cnf                                                                |            |
| no-defaults           | Read no option files                                                                                        |            |
| offset                | Skip the first N entries in the log                                                                         |            |
| open-files-limit      | Specify the number of open file<br>descriptors to reserve                                                   |            |
| password              | Password to use when<br>connecting to server                                                                |            |
| plugin-dir            | Directory where plugins are<br>installed                                                                    |            |
| port                  | TCP/IP port number for<br>connection                                                                        |            |

| Option Name             | Description                                                                                                                                                                                                                  | Deprecated |
|-------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------|
| print-defaults          | Print default options                                                                                                                                                                                                        |            |
| protocol                | Transport protocol to use                                                                                                                                                                                                    |            |
| raw                     | Write events in raw (binary)<br>format to output files                                                                                                                                                                       |            |
| read-from-remote-master | Read the binary log from a<br>MySQL replication source server<br>rather than reading a local log file                                                                                                                        |            |
| read-from-remote-server | Read binary log from MySQL<br>server rather than local log file                                                                                                                                                              |            |
| result-file             | Direct output to named file                                                                                                                                                                                                  |            |
| rewrite-db              | Create rewrite rules for<br>databases when playing back<br>from logs written in row-based<br>format. Can be used multiple<br>times                                                                                           |            |
| secure-auth             | Do not send passwords to server<br>in old (pre-4.1) format                                                                                                                                                                   | Yes        |
| server-id               | Extract only those events created<br>by the server having the given<br>server ID                                                                                                                                             |            |
| server-id-bits          | Tell mysqlbinlog how to interpret<br>server IDs in binary log when log<br>was written by a mysqld having<br>its server-id-bits set to less than<br>the maximum; supported only<br>by MySQL Cluster version of<br>mysqlbinlog |            |
| server-public-key-path  | Path name to file containing RSA<br>public key                                                                                                                                                                               |            |
| set-charset             | Add a SET NAMES<br>charset_name statement to the<br>output                                                                                                                                                                   |            |
| shared-memory-base-name | Shared-memory name for<br>shared-memory connections<br>(Windows only)                                                                                                                                                        |            |
| short-form              | Display only the statements<br>contained in the log                                                                                                                                                                          |            |
| skip-gtids              | Do not include the GTIDs from<br>the binary log files in the output<br>dump file                                                                                                                                             |            |
| socket                  | Unix socket file or Windows<br>named pipe to use                                                                                                                                                                             |            |
| ssl                     | Enable connection encryption                                                                                                                                                                                                 |            |
| ssl-ca                  | File that contains list of trusted<br>SSL Certificate Authorities                                                                                                                                                            |            |
| ssl-capath              | Directory that contains trusted<br>SSL Certificate Authority<br>certificate files                                                                                                                                            |            |

| Option Name                | Description                                                                                                                            | Deprecated |
|----------------------------|----------------------------------------------------------------------------------------------------------------------------------------|------------|
| ssl-cert                   | File that contains X.509<br>certificate                                                                                                |            |
| ssl-cipher                 | Permissible ciphers for<br>connection encryption                                                                                       |            |
| ssl-crl                    | File that contains certificate<br>revocation lists                                                                                     |            |
| ssl-crlpath                | Directory that contains certificate<br>revocation-list files                                                                           |            |
| ssl-key                    | File that contains X.509 key                                                                                                           |            |
| ssl-mode                   | Desired security state of<br>connection to server                                                                                      |            |
| ssl-verify-server-cert     | Verify host name against server<br>certificate Common Name<br>identity                                                                 |            |
| start-datetime             | Read binary log from first event<br>with timestamp equal to or later<br>than datetime argument                                         |            |
| start-position             | Decode binary log from first<br>event with position equal to or<br>greater than argument                                               |            |
| stop-datetime              | Stop reading binary log at first<br>event with timestamp equal to or<br>greater than datetime argument                                 |            |
| stop-never                 | Stay connected to server after<br>reading last binary log file                                                                         |            |
| stop-never-slave-server-id | Slave server ID to report when<br>connecting to server                                                                                 |            |
| stop-position              | Stop decoding binary log at first<br>event with position equal to or<br>greater than argument                                          |            |
| tls-version                | Permissible TLS protocols for<br>encrypted connections                                                                                 |            |
| to-last-log                | Do not stop at the end of<br>requested binary log from<br>a MySQL server, but rather<br>continue printing to end of last<br>binary log |            |
| user                       | MySQL user name to use when<br>connecting to server                                                                                    |            |
| verbose                    | Reconstruct row events as SQL<br>statements                                                                                            |            |
| verify-binlog-checksum     | Verify checksums in binary log                                                                                                         |            |
| version                    | Display version information and<br>exit                                                                                                |            |

<span id="page-194-3"></span>• [--help](#page-194-3), -?

| Command-Line Format | help |
|---------------------|------|
|---------------------|------|

Display a help message and exit.

<span id="page-194-0"></span>• [--base64-output=](#page-194-0)value

| Command-Line Format | base64-output=value |
|---------------------|---------------------|
| Type                | String              |
| Default Value       | AUTO                |
| Valid Values        | AUTO                |
|                     | NEVER               |
|                     | DECODE-ROWS         |

This option determines when events should be displayed encoded as base-64 strings using BINLOG statements. The option has these permissible values (not case-sensitive):

• AUTO ("automatic") or UNSPEC ("unspecified") displays BINLOG statements automatically when necessary (that is, for format description events and row events). If no [--base64-output](#page-194-0) option is given, the effect is the same as [--base64-output=AUTO](#page-194-0).

![](_page_194_Picture_8.jpeg)

## **Note**

Automatic BINLOG display is the only safe behavior if you intend to use the output of [mysqlbinlog](#page-189-0) to re-execute binary log file contents. The other option values are intended only for debugging or testing purposes because they may produce output that does not include all events in executable form.

- NEVER causes BINLOG statements not to be displayed. [mysqlbinlog](#page-189-0) exits with an error if a row event is found that must be displayed using BINLOG.
- DECODE-ROWS specifies to [mysqlbinlog](#page-189-0) that you intend for row events to be decoded and displayed as commented SQL statements by also specifying the --verbose option. Like NEVER, DECODE-ROWS suppresses display of BINLOG statements, but unlike NEVER, it does not exit with an error if a row event is found.

For examples that show the effect of [--base64-output](#page-194-0) and --verbose on row event output, see Section 4.6.7.2, "mysqlbinlog Row Event Display".

<span id="page-194-1"></span>• [--bind-address=](#page-194-1)ip\_address

| Command-Line Format | bind-address=ip_address |
|---------------------|-------------------------|

On a computer having multiple network interfaces, use this option to select which interface to use for connecting to the MySQL server.

<span id="page-194-2"></span>• [--binlog-row-event-max-size=](#page-194-2)N

| Command-Line Format | 567<br>binlog-row-event-max-size=# |
|---------------------|------------------------------------|
| Type                | Numeric                            |
| Default Value       | 4294967040                         |

#### mysqlbinlog — Utility for Processing Binary Log Files

| Minimum Value | 256                  |
|---------------|----------------------|
| Maximum Value | 18446744073709547520 |

Specify the maximum size of a row-based binary log event, in bytes. Rows are grouped into events smaller than this size if possible. The value should be a multiple of 256. The default is 4GB.

<span id="page-195-0"></span>• [--character-sets-dir=](#page-195-0)dir\_name

| Command-Line Format | character-sets-dir=dir_name |
|---------------------|-----------------------------|
| Type                | Directory name              |

The directory where character sets are installed. See Section 10.15, "Character Set Configuration".

<span id="page-195-1"></span>• [--connection-server-id=](#page-195-1)server\_id

| Command-Line Format | connection-server-id=#] |
|---------------------|-------------------------|
| Type                | Integer                 |
| Default Value       | 0 (1)                   |
| Minimum Value       | 0 (1)                   |
| Maximum Value       | 4294967295              |

This option is used to test a MySQL server for support of the BINLOG\_DUMP\_NON\_BLOCK connection flag. It is not required for normal operations.

The effective default and minimum values for this option depend on whether [mysqlbinlog](#page-189-0) is run in blocking mode or non-blocking mode. When [mysqlbinlog](#page-189-0) is run in blocking mode, the default (and minimum) value is 1; when run in non-blocking mode, the default (and minimum) value is 0.

<span id="page-195-2"></span>• [--database=](#page-195-2)db\_name, -d db\_name

| Command-Line Format | database=db_name |
|---------------------|------------------|

| Type | String |
|------|--------|
|------|--------|

This option causes [mysqlbinlog](#page-189-0) to output entries from the binary log (local log only) that occur while db\_name is been selected as the default database by USE.

The [--database](#page-195-2) option for [mysqlbinlog](#page-189-0) is similar to the --binlog-do-db option for mysqld, but can be used to specify only one database. If [--database](#page-195-2) is given multiple times, only the last instance is used.

The effects of this option depend on whether the statement-based or row-based logging format is in use, in the same way that the effects of --binlog-do-db depend on whether statement-based or row-based logging is in use.

**Statement-based logging.** The [--database](#page-195-2) option works as follows:

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

[mysqlbinlog --database=test](#page-189-0) does not output the first two INSERT statements because there is no default database. It outputs the three INSERT statements following USE test, but not the three INSERT statements following USE db2.

[mysqlbinlog --database=db2](#page-189-0) does not output the first two INSERT statements because there is no default database. It does not output the three INSERT statements following USE test, but does output the three INSERT statements following USE db2.

**Row-based logging.** [mysqlbinlog](#page-189-0) outputs only entries that change tables belonging to db\_name. The default database has no effect on this. Suppose that the binary log just described was created using row-based logging rather than statement-based logging. [mysqlbinlog -](#page-189-0) [database=test](#page-189-0) outputs only those entries that modify t1 in the test database, regardless of whether USE was issued or what the default database is.

If a server is running with binlog\_format set to MIXED and you want it to be possible to use [mysqlbinlog](#page-189-0) with the [--database](#page-195-2) option, you must ensure that tables that are modified are in the database selected by USE. (In particular, no cross-database updates should be used.)

When used together with the --rewrite-db option, the --rewrite-db option is applied first; then the --database option is applied, using the rewritten database name. The order in which the options are provided makes no difference in this regard.

## <span id="page-197-0"></span>• --debug[=[debug\\_options](#page-197-0)], -# [debug\_options]

| Command-Line Format | debug[=debug_options]        |
|---------------------|------------------------------|
| Type                | String                       |
| Default Value       | d:t:o,/tmp/mysqlbinlog.trace |

Write a debugging log. A typical debug\_options string is d:t:o,file\_name. The default is d:t:o,/tmp/mysqlbinlog.trace.

This option is available only if MySQL was built using WITH\_DEBUG. MySQL release binaries provided by Oracle are not built using this option.

## <span id="page-197-1"></span>• [--debug-check](#page-197-1)

| Command-Line Format | debug-check |
|---------------------|-------------|
| Type                | Boolean     |
| Default Value       | FALSE       |

Print some debugging information when the program exits.

This option is available only if MySQL was built using WITH\_DEBUG. MySQL release binaries provided by Oracle are not built using this option.

## <span id="page-197-2"></span>• [--debug-info](#page-197-2)

| Command-Line Format | debug-info |
|---------------------|------------|
| Type                | Boolean    |
| Default Value       | FALSE      |

Print debugging information and memory and CPU usage statistics when the program exits.

This option is available only if MySQL was built using WITH\_DEBUG. MySQL release binaries provided by Oracle are not built using this option.

#### <span id="page-197-3"></span>• [--default-auth=](#page-197-3)plugin

| Command-Line Format | default-auth=plugin |
|---------------------|---------------------|
| Type                | String              |

A hint about which client-side authentication plugin to use. See Section 6.2.13, "Pluggable Authentication".

<span id="page-197-4"></span>• [--defaults-extra-file=](#page-197-4)file\_name

| Command-Line Format | defaults-extra-file=file_name |
|---------------------|-------------------------------|
|---------------------|-------------------------------|

| Type<br>File name |
|-------------------|
|-------------------|

Read this option file after the global option file but (on Unix) before the user option file. If the file does not exist or is otherwise inaccessible, an error occurs. If file\_name is not an absolute path name, it is interpreted relative to the current directory.

For additional information about this and other option-file options, see Section 4.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-198-0"></span>• [--defaults-file=](#page-198-0)file\_name

| Command-Line Format | defaults-file=file_name |
|---------------------|-------------------------|
| Type                | File name               |

Use only the given option file. If the file does not exist or is otherwise inaccessible, an error occurs. If file\_name is not an absolute path name, it is interpreted relative to the current directory.

Exception: Even with --defaults-file, client programs read .mylogin.cnf.

For additional information about this and other option-file options, see Section 4.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-198-1"></span>• [--defaults-group-suffix=](#page-198-1)str

| Command-Line Format | defaults-group-suffix=str |
|---------------------|---------------------------|
| Type                | String                    |

Read not only the usual option groups, but also groups with the usual names and a suffix of str. For example, [mysqlbinlog](#page-189-0) normally reads the [client] and [mysqlbinlog] groups. If this option is given as [--defaults-group-suffix=\\_other](#page-198-1), [mysqlbinlog](#page-189-0) also reads the [client\_other] and [mysqlbinlog\_other] groups.

For additional information about this and other option-file options, see Section 4.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-198-2"></span>• [--disable-log-bin](#page-198-2), -D

| Command-Line Format | disable-log-bin |
|---------------------|-----------------|
|---------------------|-----------------|

Disable binary logging. This is useful for avoiding an endless loop if you use the --to-lastlog option and are sending the output to the same MySQL server. This option also is useful when restoring after an unexpected exit to avoid duplication of the statements you have logged.

This option causes [mysqlbinlog](#page-189-0) to include a SET sql\_log\_bin = 0 statement in its output to disable binary logging of the remaining output. Manipulating the session value of the sql\_log\_bin system variable is a restricted operation, so this option requires that you have privileges sufficient to set restricted session variables. See Section 5.1.8.1, "System Variable Privileges".

<span id="page-198-3"></span>• [--exclude-gtids=](#page-198-3)gtid\_set

|                     | 571                    |
|---------------------|------------------------|
| Command-Line Format | exclude-gtids=gtid_set |
| Type                | String                 |

| Default Value |  |
|---------------|--|
|---------------|--|

Do not display any of the groups listed in the gtid\_set.

<span id="page-199-1"></span>• [--force-if-open](#page-199-1), -F

| Command-Line Format | force-if-open |
|---------------------|---------------|
|---------------------|---------------|

Read binary log files even if they are open or were not closed properly.

<span id="page-199-2"></span>• [--force-read](#page-199-2), -f

| Command-Line Format | force-read |
|---------------------|------------|
|---------------------|------------|

With this option, if [mysqlbinlog](#page-189-0) reads a binary log event that it does not recognize, it prints a warning, ignores the event, and continues. Without this option, [mysqlbinlog](#page-189-0) stops if it reads such an event.

<span id="page-199-3"></span>• [--get-server-public-key](#page-199-3)

| Command-Line Format | get-server-public-key |
|---------------------|-----------------------|
| Type                | Boolean               |

Request from the server the public key required for RSA key pair-based password exchange. This option applies to clients that authenticate with the caching\_sha2\_password authentication plugin. For that plugin, the server does not send the public key unless requested. This option is ignored for accounts that do not authenticate with that plugin. It is also ignored if RSA-based password exchange is not used, as is the case when the client connects to the server using a secure connection.

If --server-public-key-path=file\_name is given and specifies a valid public key file, it takes precedence over [--get-server-public-key](#page-199-3).

For information about the caching\_sha2\_password plugin, see Section 6.4.1.4, "Caching SHA-2 Pluggable Authentication".

The [--get-server-public-key](#page-199-3) option was added in MySQL 5.7.23.

<span id="page-199-4"></span>• [--hexdump](#page-199-4), -H

| Command-Line Format | hexdump |
|---------------------|---------|
|                     |         |

Display a hex dump of the log in comments, as described in Section 4.6.7.1, "mysqlbinlog Hex Dump Format". The hex output can be helpful for replication debugging.

<span id="page-199-0"></span>• --host=[host\\_name](#page-199-0), -h host\_name

| Command-Line Format | host=host_name |
|---------------------|----------------|
| Type                | String         |
| Default Value       | localhost      |

Get the binary log from the MySQL server on the given host.

<span id="page-199-5"></span>• [--idempotent](#page-199-5)

| Command-Line Format | idempotent |
|---------------------|------------|
| Type                | Boolean    |
| Default Value       | true       |

Tell the MySQL Server to use idempotent mode while processing updates; this causes suppression of any duplicate-key or key-not-found errors that the server encounters in the current session while processing updates. This option may prove useful whenever it is desirable or necessary to replay one or more binary logs to a MySQL Server which may not contain all of the data to which the logs refer.

The scope of effect for this option includes the current mysqlbinlog client and session only.

<span id="page-0-0"></span>• [--include-gtids=](#page-0-0)gtid\_set

| Command-Line Format | include-gtids=gtid_set |
|---------------------|------------------------|
| Type                | String                 |
| Default Value       |                        |

Display only the groups listed in the gtid\_set.

<span id="page-0-1"></span>• [--local-load=](#page-0-1)dir\_name, -l dir\_name

| Command-Line Format | local-load=dir_name |
|---------------------|---------------------|
| Type                | Directory name      |

For data loading operations corresponding to LOAD DATA statements, mysqlbinlog extracts the files from the binary log events, writes them as temporary files to the local file system, and writes LOAD DATA LOCAL statements to cause the files to be loaded. By default, mysqlbinlog writes these temporary files to an operating system-specific directory. The [--local-load](#page-0-1) option can be used to explicitly specify the directory where mysqlbinlog should prepare local temporary files.

![](_page_0_Picture_10.jpeg)

#### **Important**

These temporary files are not automatically removed by mysqlbinlog or any other MySQL program.

<span id="page-0-2"></span>• [--login-path=](#page-0-2)name

| Command-Line Format | login-path=name |
|---------------------|-----------------|
| Type                | String          |

Read options from the named login path in the .mylogin.cnf login path file. A "login path" is an option group containing options that specify which MySQL server to connect to and which account to authenticate as. To create or modify a login path file, use the mysql\_config\_editor utility. See Section 4.6.6, "mysql\_config\_editor — MySQL Configuration Utility".

For additional information about this and other option-file options, see Section 4.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-0-3"></span>• [--no-defaults](#page-0-3)

| Command-Line Format | no-defaults |
|---------------------|-------------|
|---------------------|-------------|

Do not read any option files. If program startup fails due to reading unknown options from an option file, [--no-defaults](#page-0-3) can be used to prevent them from being read.

The exception is that the .mylogin.cnf file is read in all cases, if it exists. This permits passwords to be specified in a safer way than on the command line even when [--no-defaults](#page-0-3) is used. To create .mylogin.cnf, use the mysql\_config\_editor utility. See Section 4.6.6, "mysql\_config\_editor — MySQL Configuration Utility".

For additional information about this and other option-file options, see Section 4.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-1-0"></span>• [--offset=](#page-1-0)N, -o N

| Command-Line Format | offset=# |
|---------------------|----------|
| Type                | Numeric  |

Skip the first N entries in the log.

<span id="page-1-1"></span>• [--open-files-limit=](#page-1-1)N

| Command-Line Format | open-files-limit=#   |
|---------------------|----------------------|
| Type                | Numeric              |
| Default Value       | 8                    |
| Minimum Value       | 1                    |
| Maximum Value       | [platform dependent] |

Specify the number of open file descriptors to reserve.

<span id="page-1-2"></span>• [--password\[=](#page-1-2)password], -p[password]

| Command-Line Format | password[=password] |
|---------------------|---------------------|
| Type                | String              |

The password of the MySQL account used for connecting to the server. The password value is optional. If not given, mysqlbinlog prompts for one. If given, there must be no space between [-](#page-1-2) [password=](#page-1-2) or -p and the password following it. If no password option is specified, the default is to send no password.

Specifying a password on the command line should be considered insecure. To avoid giving the password on the command line, use an option file. See Section 6.1.2.1, "End-User Guidelines for Password Security".

To explicitly specify that there is no password and that mysqlbinlog should not prompt for one, use the [--skip-password](#page-1-2) option.

<span id="page-1-3"></span>• [--plugin-dir=](#page-1-3)dir\_name

| Command-Line Format | plugin-dir=dir_name |
|---------------------|---------------------|
| Type                | Directory name      |

The directory in which to look for plugins. Specify this option if the --default-auth option is used to specify an authentication plugin but mysqlbinlog does not find it. See Section 6.2.13, "Pluggable Authentication".

## <span id="page-2-0"></span>• --port=[port\\_num](#page-2-0), -P port\_num

| Command-Line Format | port=port_num |
|---------------------|---------------|
| Type                | Numeric       |
| Default Value       | 3306          |

The TCP/IP port number to use for connecting to a remote server.

## <span id="page-2-1"></span>• [--print-defaults](#page-2-1)

| Command-Line Format | print-defaults |
|---------------------|----------------|
|---------------------|----------------|

Print the program name and all options that it gets from option files.

For additional information about this and other option-file options, see Section 4.2.2.3, "Command-Line Options that Affect Option-File Handling".

#### <span id="page-2-2"></span>• [--protocol={TCP|SOCKET|PIPE|MEMORY}](#page-2-2)

| Command-Line Format | protocol=type |
|---------------------|---------------|
| Type                | String        |
| Default Value       | [see text]    |
| Valid Values        | TCP           |
|                     | SOCKET        |
|                     | PIPE          |
|                     | MEMORY        |

The transport protocol to use for connecting to the server. It is useful when the other connection parameters normally result in use of a protocol other than the one you want. For details on the permissible values, see Section 4.2.5, "Connection Transport Protocols".

## <span id="page-2-3"></span>• [--raw](#page-2-3)

| Command-Line Format | raw     |
|---------------------|---------|
| Type                | Boolean |
| Default Value       | FALSE   |

By default, mysqlbinlog reads binary log files and writes events in text format. The [--raw](#page-2-3) option tells mysqlbinlog to write them in their original binary format. Its use requires that [--read-from](#page-3-0)[remote-server](#page-3-0) also be used because the files are requested from a server. mysqlbinlog writes one output file for each file read from the server. The [--raw](#page-2-3) option can be used to make a backup of a server's binary log. With the [--stop-never](#page-7-0) option, the backup is "live" because mysqlbinlog stays connected to the server. By default, output files are written in the current directory with the same names as the original log files. Output file names can be modified using the [--result-file](#page-3-1) option. For more information, see [Section 4.6.7.3, "Using mysqlbinlog to Back Up Binary Log Files"](#page-14-0).

<span id="page-3-2"></span>• [--read-from-remote-master=](#page-3-2)type

| Command-Line Format | read-from-remote-master=type |
|---------------------|------------------------------|
|---------------------|------------------------------|

Read binary logs from a MySQL server with the COM\_BINLOG\_DUMP or COM\_BINLOG\_DUMP\_GTID commands by setting the option value to either BINLOG-DUMP-NON-GTIDS or BINLOG-DUMP-GTIDS, respectively. If [--read-from-remote-master=BINLOG-DUMP-GTIDS](#page-3-2) is combined with --exclude-gtids, transactions can be filtered out on the source, avoiding unnecessary network traffic.

The connection parameter options are used with this option or the [--read-from-remote-server](#page-3-0) option. These options are --host, [--password](#page-1-2), [--port](#page-2-0), [--protocol](#page-2-2), [--socket](#page-6-0), and [--user](#page-8-0). If neither of the remote options is specified, the connection parameter options are ignored.

The REPLICATION SLAVE privilege is required to use this option.

<span id="page-3-0"></span>• [--read-from-remote-server=](#page-3-0)file\_name, -R

| Command-Line Format | read-from-remote-server=file_name |
|---------------------|-----------------------------------|
|---------------------|-----------------------------------|

Read the binary log from a MySQL server rather than reading a local log file. This option requires that the remote server be running. It works only for binary log files on the remote server, not relay log files, and takes only the binary log file name (including the numeric suffix) as its argument, while ignoring any path.

The connection parameter options are used with this option or the [--read-from-remote-master](#page-3-2) option. These options are --host, [--password](#page-1-2), [--port](#page-2-0), [--protocol](#page-2-2), [--socket](#page-6-0), and [--user](#page-8-0). If neither of the remote options is specified, the connection parameter options are ignored.

The REPLICATION SLAVE privilege is required to use this option.

This option is like [--read-from-remote-master=BINLOG-DUMP-NON-GTIDS](#page-3-2).

<span id="page-3-1"></span>• [--result-file=](#page-3-1)name, -r name

| Command-Line Format<br>result-file=name |  |
|-----------------------------------------|--|
|-----------------------------------------|--|

Without the [--raw](#page-2-3) option, this option indicates the file to which mysqlbinlog writes text output. With [--raw](#page-2-3), mysqlbinlog writes one binary output file for each log file transferred from the server, writing them by default in the current directory using the same names as the original log file. In this case, the [--result-file](#page-3-1) option value is treated as a prefix that modifies output file names.

<span id="page-3-3"></span>• [--rewrite-db='](#page-3-3)from\_name->to\_name'

| Command-Line Format | rewrite-db='oldname->newname' |
|---------------------|-------------------------------|
| Type                | String                        |
| Default Value       | [none]                        |

When reading from a row-based or statement-based log, rewrite all occurrences of from\_name 576 to to\_name. Rewriting is done on the rows, for row-based logs, as well as on the USE clauses, for statement-based logs. In MySQL versions prior to 5.7.8, this option was only for use when restoring tables logged using the row-based format.

![](_page_4_Picture_2.jpeg)

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

<span id="page-4-0"></span>• [--secure-auth](#page-4-0)

| Command-Line Format | secure-auth |
|---------------------|-------------|
| Deprecated          | Yes         |

Do not send passwords to the server in old (pre-4.1) format. This prevents connections except for servers that use the newer password format.

As of MySQL 5.7.5, this option is deprecated; expect it to be removed in a future MySQL release. It is always enabled and attempting to disable it ([--skip-secure-auth](#page-4-0), [--secure-auth=0](#page-4-0)) produces an error. Before MySQL 5.7.5, this option is enabled by default but can be disabled.

![](_page_4_Picture_14.jpeg)

#### **Note**

Passwords that use the pre-4.1 hashing method are less secure than passwords that use the native password hashing method and should be avoided. Pre-4.1 passwords are deprecated and support for them was removed in MySQL 5.7.5. For account upgrade instructions, see Section 6.4.1.3, "Migrating Away from Pre-4.1 Password Hashing and the mysql\_old\_password Plugin".

<span id="page-4-1"></span>• [--server-id=](#page-4-1)id

| Command-Line Format | server-id=id |
|---------------------|--------------|
| Type                | Numeric      |

Display only those events created by the server having the given server ID.

<span id="page-4-2"></span>• [--server-id-bits=](#page-4-2)N

| Command-Line Format | server-id-bits=# |
|---------------------|------------------|

| Type          | Numeric |
|---------------|---------|
| Default Value | 32      |
| Minimum Value | 7       |
| Maximum Value | 32      |

Use only the first N bits of the server\_id to identify the server. If the binary log was written by a mysqld with server-id-bits set to less than 32 and user data stored in the most significant bit, running mysqlbinlog with --server-id-bits set to 32 enables this data to be seen.

This option is supported only by the version of mysqlbinlog supplied with the NDB Cluster distribution, or built with NDB Cluster support.

<span id="page-5-0"></span>• [--server-public-key-path=](#page-5-0)file\_name

| Command-Line Format | server-public-key-path=file_name |
|---------------------|----------------------------------|
| Type                | File name                        |

The path name to a file in PEM format containing a client-side copy of the public key required by the server for RSA key pair-based password exchange. This option applies to clients that authenticate with the sha256\_password or caching\_sha2\_password authentication plugin. This option is ignored for accounts that do not authenticate with one of those plugins. It is also ignored if RSAbased password exchange is not used, as is the case when the client connects to the server using a secure connection.

If [--server-public-key-path=](#page-5-0)file\_name is given and specifies a valid public key file, it takes precedence over --get-server-public-key.

For sha256\_password, this option applies only if MySQL was built using OpenSSL.

For information about the sha256\_password and caching\_sha2\_password plugins, see Section 6.4.1.5, "SHA-256 Pluggable Authentication", and Section 6.4.1.4, "Caching SHA-2 Pluggable Authentication".

The [--server-public-key-path](#page-5-0) option was added in MySQL 5.7.23.

<span id="page-5-1"></span>• [--set-charset=](#page-5-1)charset\_name

| Command-Line Format | set-charset=charset_name |
|---------------------|--------------------------|
| Type                | String                   |

Add a SET NAMES charset\_name statement to the output to specify the character set to be used for processing log files.

<span id="page-5-2"></span>• [--shared-memory-base-name=](#page-5-2)name

| Command-Line Format | shared-memory-base-name=name |
|---------------------|------------------------------|
| Platform Specific   | Windows                      |

On Windows, the shared-memory name to use for connections made using shared memory to a local server. The default value is MYSQL. The shared-memory name is case-sensitive.

This option applies only if the server was started with the shared\_memory system variable enabled to support shared-memory connections.

<span id="page-6-1"></span>• [--short-form](#page-6-1), -s

| Command-Line Format<br>short-form |
|-----------------------------------|
|-----------------------------------|

Display only the statements contained in the log, without any extra information or row-based events. This is for testing only, and should not be used in production systems.

<span id="page-6-2"></span>• [--skip-gtids\[=\(true|false\)\]](#page-6-2)

| Command-Line Format | skip-gtids[=true false] |
|---------------------|-------------------------|
| Type                | Boolean                 |
| Default Value       | false                   |

Do not include the GTIDs from the binary log files in the output dump file. For example:

```
mysqlbinlog --skip-gtids binlog.000001 > /tmp/dump.sql
mysql -u root -p -e "source /tmp/dump.sql"
```

You should not normally use this option in production or in recovery, except in the specific, and rare, scenarios where the GTIDs are actively unwanted. For example, an administrator might want to duplicate selected transactions (such as table definitions) from a deployment to another, unrelated, deployment that will not replicate to or from the original. In that scenario, [--skip-gtids](#page-6-2) can be used to enable the administrator to apply the transactions as if they were new, and ensure that the deployments remain unrelated. However, you should only use this option if the inclusion of the GTIDs causes a known issue for your use case.

<span id="page-6-0"></span>• [--socket=](#page-6-0)path, -S path

| Command-Line Format | socket={file_name pipe_name} |
|---------------------|------------------------------|
| Type                | String                       |

For connections to localhost, the Unix socket file to use, or, on Windows, the name of the named pipe to use.

On Windows, this option applies only if the server was started with the [named\\_pipe](#page-192-0) system variable enabled to support named-pipe connections. In addition, the user making the connection must be a member of the Windows group specified by the [named\\_pipe\\_full\\_access\\_group](#page-192-1) system variable.

• --ssl\*

Options that begin with --ssl specify whether to connect to the server using encryption and indicate where to find SSL keys and certificates. See Command Options for Encrypted Connections.

<span id="page-6-3"></span>• [--start-datetime=](#page-6-3)datetime

| Command-Line Format | start-datetime=datetime |
|---------------------|-------------------------|
| Type                | Datetime                |

Start reading the binary log at the first event having a timestamp equal to or later than the datetime argument. The datetime value is relative to the local time zone on the machine where you run 579 mysqlbinlog. The value should be in a format accepted for the DATETIME or TIMESTAMP data types. For example:

```
mysqlbinlog --start-datetime="2005-12-25 11:25:56" binlog.000003
```

This option is useful for point-in-time recovery. See Section 7.5, "Point-in-Time (Incremental) Recovery".

<span id="page-7-1"></span>• [--start-position=](#page-7-1)N, -j N

| Command-Line Format | start-position=# |
|---------------------|------------------|
| Type                | Numeric          |

Start reading the binary log at the first event having a position equal to or greater than N. This option applies to the first log file named on the command line.

This option is useful for point-in-time recovery. See Section 7.5, "Point-in-Time (Incremental) Recovery".

<span id="page-7-2"></span>• [--stop-datetime=](#page-7-2)datetime

| Command-Line Format | stop-datetime=datetime |
|---------------------|------------------------|
|---------------------|------------------------|

Stop reading the binary log at the first event having a timestamp equal to or later than the datetime argument. See the description of the [--start-datetime](#page-6-3) option for information about the datetime value.

This option is useful for point-in-time recovery. See Section 7.5, "Point-in-Time (Incremental) Recovery".

<span id="page-7-0"></span>• [--stop-never](#page-7-0)

| Command-Line Format | stop-never |
|---------------------|------------|
| Type                | Boolean    |
| Default Value       | FALSE      |

This option is used with [--read-from-remote-server](#page-3-0). It tells mysqlbinlog to remain connected to the server. Otherwise mysqlbinlog exits when the last log file has been transferred from the server. [--stop-never](#page-7-0) implies [--to-last-log](#page-8-1), so only the first log file to transfer need be named on the command line.

[--stop-never](#page-7-0) is commonly used with [--raw](#page-2-3) to make a live binary log backup, but also can be used without [--raw](#page-2-3) to maintain a continuous text display of log events as the server generates them.

<span id="page-7-3"></span>• [--stop-never-slave-server-id=](#page-7-3)id

| Command-Line Format | stop-never-slave-server-id=# |
|---------------------|------------------------------|
| Type                | Numeric                      |
| Default Value       | 65535                        |
| Minimum Value       | 1                            |

a conflict with the ID of a replica server or another mysqlbinlog process. See [Section 4.6.7.4,](#page-16-0) ["Specifying the mysqlbinlog Server ID"](#page-16-0).

<span id="page-8-2"></span>• [--stop-position=](#page-8-2)N

| Command-Line Format | stop-position=# |
|---------------------|-----------------|
| Type                | Numeric         |

Stop reading the binary log at the first event having a position equal to or greater than N. This option applies to the last log file named on the command line.

This option is useful for point-in-time recovery. See Section 7.5, "Point-in-Time (Incremental) Recovery".

<span id="page-8-3"></span>• [--tls-version=](#page-8-3)protocol\_list

| Command-Line Format | tls-version=protocol_list |
|---------------------|---------------------------|
| Type                | String                    |
| Default Value       | TLSv1,TLSv1.1,TLSv1.2     |

The permissible TLS protocols for encrypted connections. The value is a list of one or more commaseparated protocol names. The protocols that can be named for this option depend on the SSL library used to compile MySQL. For details, see Section 6.3.2, "Encrypted Connection TLS Protocols and Ciphers".

This option was added in MySQL 5.7.10.

<span id="page-8-1"></span>• [--to-last-log](#page-8-1), -t

| Command-Line Format | to-last-log |
|---------------------|-------------|

Do not stop at the end of the requested binary log from a MySQL server, but rather continue printing until the end of the last binary log. If you send the output to the same MySQL server, this may lead to an endless loop. This option requires [--read-from-remote-server](#page-3-0).

<span id="page-8-0"></span>• --user=[user\\_name](#page-8-0), -u user\_name

| Command-Line Format | user=user_name, |
|---------------------|-----------------|
| Type                | String          |

The user name of the MySQL account to use when connecting to a remote server.

<span id="page-8-4"></span>• [--verbose](#page-8-4), -v

| Command-Line Format | verbose |
|---------------------|---------|
|---------------------|---------|

Reconstruct row events and display them as commented SQL statements. If this option is given twice (by passing in either "-vv" or "--verbose --verbose"), the output includes comments to indicate column data types and some metadata, and row query log events if so configured.

For examples that show the effect of --base64-output and [--verbose](#page-8-4) on row event output, see [Section 4.6.7.2, "mysqlbinlog Row Event Display"](#page-10-0).

<span id="page-8-5"></span>• [--verify-binlog-checksum](#page-8-5), -c

| Command-Line Format | verify-binlog-checksum |
|---------------------|------------------------|

Verify checksums in binary log files.

<span id="page-9-0"></span>• [--version](#page-9-0), -V

```
Command-Line Format --version
```

Display version information and exit.

In MySQL 5.7, the version number shown by mysqlbinlog when using this option is 3.4.

You can pipe the output of mysqlbinlog into the mysql client to execute the events contained in the binary log. This technique is used to recover from an unexpected exit when you have an old backup (see Section 7.5, "Point-in-Time (Incremental) Recovery"). For example:

```
mysqlbinlog binlog.000001 | mysql -u root -p
Or:
```

```
mysqlbinlog binlog.[0-9]* | mysql -u root -p
```

If the statements produced by mysqlbinlog may contain BLOB values, these may cause problems when mysql processes them. In this case, invoke mysql with the --binary-mode option.

You can also redirect the output of mysqlbinlog to a text file instead, if you need to modify the statement log first (for example, to remove statements that you do not want to execute for some reason). After editing the file, execute the statements that it contains by using it as input to the mysql program:

```
mysqlbinlog binlog.000001 > tmpfile
... edit tmpfile ...
mysql -u root -p < tmpfile
```

When mysqlbinlog is invoked with the [--start-position](#page-7-1) option, it displays only those events with an offset in the binary log greater than or equal to a given position (the given position must match the start of one event). It also has options to stop and start when it sees an event with a given date and time. This enables you to perform point-in-time recovery using the [--stop-datetime](#page-7-2) option (to be able to say, for example, "roll forward my databases to how they were today at 10:30 a.m.").

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

mysqlbinlog can produce output that reproduces a LOAD DATA operation without the original data file. mysqlbinlog copies the data to a temporary file and writes a LOAD DATA LOCAL statement that refers to the file. The default location of the directory where these files are written is system-specific. To specify a directory explicitly, use the [--local-load](#page-0-1) option.

Because mysqlbinlog converts LOAD DATA statements to LOAD DATA LOCAL statements (that is, it adds LOCAL), both the client and the server that you use to process the statements must be configured with the LOCAL capability enabled. See Section 6.1.6, "Security Considerations for LOAD DATA LOCAL".

![](_page_10_Picture_3.jpeg)

#### **Warning**

The temporary files created for LOAD DATA LOCAL statements are not automatically deleted because they are needed until you actually execute those statements. You should delete the temporary files yourself after you no longer need the statement log. The files can be found in the temporary file directory and have names like original\_file\_name-#-#.