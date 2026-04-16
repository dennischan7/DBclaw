---
source: MySQL 5.7 Reference
title: 00_Overview
---

The more complex your privilege setup, the more overhead applies to all SQL statements. Simplifying the privileges established by GRANT statements enables MySQL to reduce permission-checking overhead when clients execute statements. For example, if you do not grant any table-level or columnlevel privileges, the server need not ever check the contents of the tables\_priv and columns\_priv tables. Similarly, if you place no resource limits on any accounts, the server does not have to perform resource counting. If you have a very high statement-processing load, consider using a simplified grant structure to reduce permission-checking overhead.