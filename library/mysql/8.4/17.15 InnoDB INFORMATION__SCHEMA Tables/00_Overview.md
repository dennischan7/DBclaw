---
source: MySQL 8.4 Reference
title: 00_Overview
---

This section provides information and usage examples for InnoDB INFORMATION\_SCHEMA tables.

InnoDB INFORMATION\_SCHEMA tables provide metadata, status information, and statistics about various aspects of the InnoDB storage engine. You can view a list of InnoDB INFORMATION\_SCHEMA tables by issuing a SHOW TABLES statement on the INFORMATION\_SCHEMA database:

mysql> **SHOW TABLES FROM INFORMATION\_SCHEMA LIKE 'INNODB%';**

For table definitions, see Section 28.4, "INFORMATION\_SCHEMA InnoDB Tables". For general information regarding the MySQL INFORMATION\_SCHEMA database, see Chapter 28, INFORMATION\_SCHEMA Tables.