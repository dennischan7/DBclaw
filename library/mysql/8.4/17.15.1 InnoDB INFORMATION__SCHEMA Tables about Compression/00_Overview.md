---
source: MySQL 8.4 Reference
title: 00_Overview
---

There are two pairs of InnoDB INFORMATION\_SCHEMA tables about compression that can provide insight into how well compression is working overall:

• INNODB\_CMP and INNODB\_CMP\_RESET provide information about the number of compression operations and the amount of time spent performing compression.

• INNODB\_CMPMEM and INNODB\_CMPMEM\_RESET provide information about the way memory is allocated for compression.