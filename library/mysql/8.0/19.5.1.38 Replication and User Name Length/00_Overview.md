---
source: MySQL 8.0 Reference
title: 00_Overview
---

The maximum length for user names in MySQL 8.0 is 32 characters. Replication of user names longer than 16 characters fails when the replica runs a version of MySQL previous to 5.7, because those versions support only shorter user names. This occurs only when replicating from a newer source to an older replica, which is not a recommended configuration.

# <span id="page-74-0"></span>**19.5.1.39 Replication and Variables**

System variables are not replicated correctly when using STATEMENT mode, except for the following variables when they are used with session scope:

- auto\_increment\_increment
- auto\_increment\_offset
- character\_set\_client
- character\_set\_connection
- character\_set\_database
- character\_set\_server
- collation\_connection
- collation\_database
- collation\_server
- foreign\_key\_checks
- identity
- last\_insert\_id
- lc\_time\_names
- pseudo\_thread\_id
- sql\_auto\_is\_null
- time\_zone
- timestamp
- unique\_checks

When MIXED mode is used, the variables in the preceding list, when used with session scope, cause a switch from statement-based to row-based logging. See Section 7.4.4.3, "Mixed Binary Logging Format".

sql\_mode is also replicated except for the NO\_DIR\_IN\_CREATE mode; the replica always preserves its own value for NO\_DIR\_IN\_CREATE, regardless of changes to it on the source. This is true for all replication formats.

However, when mysqlbinlog parses a SET @@sql\_mode = mode statement, the full mode value, including NO\_DIR\_IN\_CREATE, is passed to the receiving server. For this reason, replication of such a statement may not be safe when STATEMENT mode is in use.

The default\_storage\_engine system variable is not replicated, regardless of the logging mode; this is intended to facilitate replication between different storage engines.

The read\_only system variable is not replicated. In addition, the enabling this variable has different effects with regard to temporary tables, table locking, and the SET PASSWORD statement in different MySQL versions.

The max\_heap\_table\_size system variable is not replicated. Increasing the value of this variable on the source without doing so on the replica can lead eventually to Table is full errors on the replica when trying to execute INSERT statements on a MEMORY table on the source that is thus permitted to grow larger than its counterpart on the replica. For more information, see [Section 19.5.1.21,](#page-62-0) ["Replication and MEMORY Tables"](#page-62-0).

In statement-based replication, session variables are not replicated properly when used in statements that update tables. For example, the following sequence of statements does not insert the same data on the source and the replica:

```
SET max_join_size=1000;
INSERT INTO mytable VALUES(@@max_join_size);
```

This does not apply to the common sequence:

```
SET time_zone=...;
INSERT INTO mytable VALUES(CONVERT_TZ(..., ..., @@time_zone));
```

Replication of session variables is not a problem when row-based replication is being used, in which case, session variables are always replicated safely. See Section 19.2.1, "Replication Formats".

The following session variables are written to the binary log and honored by the replica when parsing the binary log, regardless of the logging format:

- sql\_mode
- foreign\_key\_checks
- unique\_checks
- character\_set\_client
- collation\_connection
- collation\_database
- collation\_server
- sql\_auto\_is\_null

![](_page_75_Picture_18.jpeg)

#### **Important**

Even though session variables relating to character sets and collations are written to the binary log, replication between different character sets is not supported.

To help reduce possible confusion, we recommend that you always use the same setting for the lower\_case\_table\_names system variable on both source and replica, especially when you are running MySQL on platforms with case-sensitive file systems. The lower\_case\_table\_names setting can only be configured when initializing the server.