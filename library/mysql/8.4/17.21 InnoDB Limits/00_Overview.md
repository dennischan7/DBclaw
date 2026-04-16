---
source: MySQL 8.4 Reference
title: 00_Overview
---

This section describes limits for InnoDB tables, indexes, tablespaces, and other aspects of the InnoDB storage engine.

- A table can contain a maximum of 1017 columns. Virtual generated columns are included in this limit.
- A table can contain a maximum of 64 secondary indexes.
- The index key prefix length limit is 3072 bytes for InnoDB tables that use DYNAMIC or COMPRESSED row format.

The index key prefix length limit is 767 bytes for InnoDB tables that use the REDUNDANT or COMPACT row format. For example, you might hit this limit with a column prefix index of more than 191

characters on a TEXT or VARCHAR column, assuming a utf8mb4 character set and the maximum of 4 bytes for each character.

Attempting to use an index key prefix length that exceeds the limit returns an error.

If you reduce the InnoDB page size to 8KB or 4KB by specifying the [innodb\\_page\\_size](#page-41-0) option when creating the MySQL instance, the maximum length of the index key is lowered proportionally, based on the limit of 3072 bytes for a 16KB page size. That is, the maximum index key length is 1536 bytes when the page size is 8KB, and 768 bytes when the page size is 4KB.

The limits that apply to index key prefixes also apply to full-column index keys.

• A maximum of 16 columns is permitted for multicolumn indexes. Exceeding the limit returns an error.

```
ERROR 1070 (42000): Too many key parts specified; max 16 parts allowed
```

• The maximum row size, excluding any variable-length columns that are stored off-page, is slightly less than half of a page for 4KB, 8KB, 16KB, and 32KB page sizes. For example, the maximum row size for the default [innodb\\_page\\_size](#page-41-0) of 16KB is about 8000 bytes. However, for an InnoDB page size of 64KB, the maximum row size is approximately 16000 bytes. LONGBLOB and LONGTEXT columns must be less than 4GB, and the total row size, including BLOB and TEXT columns, must be less than 4GB.

If a row is less than half a page long, all of it is stored locally within the page. If it exceeds half a page, variable-length columns are chosen for external off-page storage until the row fits within half a page, as described in Section 17.11.2, "File Space Management".

- Although InnoDB supports row sizes larger than 65,535 bytes internally, MySQL itself imposes a row-size limit of 65,535 for the combined size of all columns. See Section 10.4.7, "Limits on Table Column Count and Row Size".
- The maximum table or tablespace size is impacted by the server's file system, which can impose a maximum file size that is smaller than the internal 64 TiB size limit defined by InnoDB. For example, the ext4 file system on Linux has a maximum file size of 16 TiB, so the maximum table or tablespace size becomes 16 TiB instead of 64 TiB. Another example is the FAT32 file system, which has a maximum file size of 4 GB.

If you require a larger system tablespace, configure it using several smaller data files rather than one large data file, or distribute table data across file-per-table and general tablespace data files.

- The combined maximum size for InnoDB log files is 512GB.
- The minimum tablespace size is slightly larger than 10MB. The maximum tablespace size depends on the InnoDB page size.

**Table 17.26 InnoDB Maximum Tablespace Size**

| InnoDB Page Size | Maximum Tablespace Size |
|------------------|-------------------------|
| 4KB              | 16TB                    |
| 8KB              | 32TB                    |
| 16KB             | 64TB                    |
| 32KB             | 128TB                   |
| 64KB             | 256TB                   |

The maximum tablespace size is also the maximum size for a table.

- An InnoDB instance supports up to 2^32 (4294967296) tablespaces, with a small number of those tablespaces reserved for undo and temporary tables.
- Shared tablespaces support up to 2^32 (4294967296) tables.

- The path of a tablespace file, including the file name, cannot exceed the MAX\_PATH limit on Windows. Prior to Windows 10, the MAX\_PATH limit is 260 characters. As of Windows 10, version 1607, MAX\_PATH limitations are removed from common Win32 file and directory functions, but you must enable the new behavior.
- For limits associated with concurrent read-write transactions, see Section 17.6.6, "Undo Logs".