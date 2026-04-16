---
source: MySQL 5.7 Reference
title: 00_Overview
---

The following items apply to Disk Data storage requirements:

• Variable-length columns of Disk Data tables take up a fixed amount of space. For each row, this is equal to the space required to store the largest possible value for that column.

For general information about calculating these values, see Section 11.7, "Data Type Storage Requirements".

You can obtain an estimate the amount of space available in data files and undo log files by querying the Information Schema FILES table. For more information and examples, see Section 24.3.9, "The INFORMATION\_SCHEMA FILES Table".

![](_page_3_Picture_15.jpeg)

### **Note**

The OPTIMIZE TABLE statement does not have any effect on Disk Data tables.

- In a Disk Data table, the first 256 bytes of a TEXT or BLOB column are stored in memory; only the remainder is stored on disk.
- Each row in a Disk Data table uses 8 bytes in memory to point to the data stored on disk. This means that, in some cases, converting an in-memory column to the disk-based format can actually result in greater memory usage. For example, converting a CHAR(4) column from memory-based to disk-based format increases the amount of DataMemory used per row from 4 to 8 bytes.

![](_page_4_Picture_3.jpeg)

### **Important**

Starting the cluster with the --initial option does not remove Disk Data files. You must remove these manually prior to performing an initial restart of the cluster.

Performance of Disk Data tables can be improved by minimizing the number of disk seeks by making sure that DiskPageBufferMemory is of sufficient size. You can query the [diskpagebuffer](#page-44-0) table to help determine whether the value for this parameter needs to be increased.