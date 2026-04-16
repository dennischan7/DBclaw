---
source: MySQL 8.4 Reference
title: 00_Overview
---

Online DDL operations that create or rebuild secondary indexes allocate temporary buffers during different phases of index creation. The innodb\_ddl\_buffer\_size variable defines the maximum buffer size for online DDL operations. The default setting is 1048576 bytes (1 MB). The setting applies to buffers created by threads executing online DDL operations. Defining an appropriate buffer size limit avoids potential out of memory errors for online DDL operations that create or rebuild secondary indexes. The maximum buffer size per DDL thread is the maximum buffer size divided by the number of DDL threads (innodb\_ddl\_buffer\_size/innodb\_ddl\_threads).