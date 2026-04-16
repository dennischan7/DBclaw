---
source: MySQL 8.0 Reference
title: 00_Overview
---

This table provides about blob values stored in NDB. The blobs table has the columns listed here:

• table\_id

Unique ID of the table containing the column

• database\_name

Name of the database in which this table resides

• table\_name

Name of the table

• column\_id

The column's unique ID within the table

• column\_name

Name of the column

• inline\_size

Inline size of the column

• part\_size

Part size of the column

• stripe\_size

Stripe size of the column

• blob\_table\_name

Name of the blob table containing this column's blob data, if any

Rows exist in this table for those NDB table columns that store BLOB, TEXT values taking up more than 255 bytes and thus require the use of a blob table. Parts of JSON values exceeding 4000 bytes in size are also stored in this table. For more information about how NDB Cluster stores columns of such types, see String Type Storage Requirements.

The part and (NDB 8.0.30 and later) inline sizes of NDB blob columns can be set using CREATE TABLE and ALTER TABLE statements containing NDB table column comments (see NDB\_COLUMN Options); this can also be done in NDB API applications (see [Column::setPartSize\(\)](https://dev.mysql.com/doc/ndbapi/en/ndb-column.md#ndb-column-setpartsize) and [setInlineSize\(\)](https://dev.mysql.com/doc/ndbapi/en/ndb-column.md#ndb-column-setinlinesize)).

The blobs table was added in NDB 8.0.29.

# <span id="page-134-0"></span>**25.6.16.5 The ndbinfo blocks Table**

The blocks table is a static table which simply contains the names and internal IDs of all NDB kernel blocks (see [NDB Kernel Blocks](https://dev.mysql.com/doc/ndb-internals/en/ndb-internals-kernel-blocks.md)). It is for use by the other [ndbinfo](#page-126-0) tables (most of which are actually views) in mapping block numbers to block names for producing human-readable output.

The blocks table contains the following columns:

• block\_number

Block number

• block\_name

Block name

### **Notes**

To obtain a list of all block names, simply execute SELECT block\_name FROM ndbinfo.blocks. Although this is a static table, its content can vary between different NDB Cluster releases.