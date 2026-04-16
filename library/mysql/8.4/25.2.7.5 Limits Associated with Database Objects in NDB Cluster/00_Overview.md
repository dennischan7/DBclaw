---
source: MySQL 8.4 Reference
title: 00_Overview
---

Some database objects such as tables and indexes have different limitations when using the [NDBCLUSTER](#page-50-0) storage engine:

- **Number of database objects.** The maximum number of all [NDB](#page-50-0) database objects in a single NDB Cluster—including databases, tables, and indexes—is limited to 20320.
- **Attributes per table.** The maximum number of attributes (that is, columns and indexes) that can belong to a given table is 512.
- **Attributes per key.** The maximum number of attributes per key is 32.
- **Row size.** The maximum permitted size of any one row is 30000 bytes.

Each BLOB or TEXT column contributes 256 + 8 = 264 bytes to this total; this includes JSON columns. See String Type Storage Requirements, as well as JSON Storage Requirements, for more information relating to these types.

In addition, the maximum offset for a fixed-width column of an NDB table is 8188 bytes; attempting to create a table that violates this limitation fails with NDB error 851 Maximum offset for fixed-size columns exceeded. For memory-based columns, you can work around this limitation by using a variable-width column type such as VARCHAR or defining the column as COLUMN\_FORMAT=DYNAMIC; this does not work with columns stored on disk. For disk-based columns, you may be able to do so by reordering one or more of the table's disk-based columns such that the combined width of all but the disk-based column defined last in the CREATE TABLE statement used to create the table does not exceed 8188 bytes, less any possible rounding performed for some data types such as CHAR or VARCHAR; otherwise it is necessary to use memorybased storage for one or more of the offending column or columns instead.

- **BIT column storage per table.** The maximum combined width for all BIT columns used in a given NDB table is 4096.
- **FIXED column storage.** NDB Cluster supports a maximum of 128 TB per fragment of data in FIXED columns.

# <span id="page-78-0"></span>**25.2.7.6 Unsupported or Missing Features in NDB Cluster**

A number of features supported by other storage engines are not supported for [NDB](#page-50-0) tables. Trying to use any of these features in NDB Cluster does not cause errors in or of itself; however, errors may occur in applications that expects the features to be supported or enforced. Statements referencing such features, even if effectively ignored by NDB, must be syntactically and otherwise valid.

• **Index prefixes.** Prefixes on indexes are not supported for NDB tables. If a prefix is used as part of an index specification in a statement such as CREATE TABLE, ALTER TABLE, or CREATE INDEX, the prefix is not created by NDB.

A statement containing an index prefix, and creating or modifying an NDB table, must still be syntactically valid. For example, the following statement always fails with Error 1089 Incorrect prefix key; the used key part is not a string, the used length is longer than the key part, or the storage engine doesn't support unique prefix keys, regardless of storage engine:

```
CREATE TABLE t1 (
 c1 INT NOT NULL,
 c2 VARCHAR(100),
 INDEX i1 (c2(500))
);
```

This happens on account of the SQL syntax rule that no index may have a prefix larger than itself.

- **Savepoints and rollbacks.** Savepoints and rollbacks to savepoints are ignored as in MyISAM.
- **Durability of commits.** There are no durable commits on disk. Commits are replicated, but there is no guarantee that logs are flushed to disk on commit.
- **Replication.** Statement-based replication is not supported. Use --binlog-format=ROW (or --binlog-format=MIXED) when setting up cluster replication. See Section 25.7, "NDB Cluster Replication", for more information.

Replication using global transaction identifiers (GTIDs) is not compatible with NDB Cluster, and is not supported in NDB Cluster 8.4. Do not enable GTIDs when using the NDB storage engine, as this is very likely to cause problems up to and including failure of NDB Cluster Replication.

Semisynchronous replication is not supported in NDB Cluster.

• **Generated columns.** The NDB storage engine does not support indexes on virtual generated columns.

As with other storage engines, you can create an index on a stored generated column, but you should bear in mind that NDB uses [DataMemory](#page-156-0) for storage of the generated column as well as [IndexMemory](#page-157-0) for the index. See JSON columns and indirect indexing in NDB Cluster, for an example.

NDB Cluster writes changes in stored generated columns to the binary log, but does log not those made to virtual columns. This should not effect NDB Cluster Replication or replication between NDB and other MySQL storage engines.

![](_page_78_Picture_17.jpeg)

#### **Note**

See [Section 25.2.7.3, "Limits Relating to Transaction Handling in NDB Cluster"](#page-74-0), for more information relating to limitations on transaction handling in [NDB](#page-50-0).