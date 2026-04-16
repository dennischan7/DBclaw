---
source: MySQL 8.4 Reference
title: 00_Overview
---

Normally, errors occur for data-change statements (such as INSERT or UPDATE) that would violate primary-key, unique-key, or foreign-key constraints. If you are using a transactional storage engine such as InnoDB, MySQL automatically rolls back the statement. If you are using a nontransactional storage engine, MySQL stops processing the statement at the row for which the error occurred and leaves any remaining rows unprocessed.

MySQL supports an IGNORE keyword for INSERT, UPDATE, and so forth. If you use it, MySQL ignores primary-key or unique-key violations and continues processing with the next row. See the section for the statement that you are using (Section 15.2.7, "INSERT Statement", Section 15.2.17, "UPDATE Statement", and so forth).

You can get information about the number of rows actually inserted or updated with the [mysql\\_info\(\)](https://dev.mysql.com/doc/c-api/8.4/en/mysql-info.md) C API function. You can also use the SHOW WARNINGS statement. See [mysql\\_info\(\),](https://dev.mysql.com/doc/c-api/8.4/en/mysql-info.md) and Section 15.7.7.42, "SHOW WARNINGS Statement".

InnoDB and NDB tables support foreign keys. See [Section 1.7.3.2, "FOREIGN KEY Constraints"](#page-82-0).

# <span id="page-82-0"></span>**1.7.3.2 FOREIGN KEY Constraints**

Foreign keys let you cross-reference related data across tables, and foreign key constraints help keep this spread-out data consistent.

MySQL supports ON UPDATE and ON DELETE foreign key references in CREATE TABLE and ALTER TABLE statements. The available referential actions are RESTRICT, CASCADE, SET NULL, and NO ACTION (the default).

SET DEFAULT is also supported by the MySQL Server but is currently rejected as invalid by InnoDB. Since MySQL does not support deferred constraint checking, NO ACTION is treated as RESTRICT. For the exact syntax supported by MySQL for foreign keys, see Section 15.1.20.5, "FOREIGN KEY Constraints".

MATCH FULL, MATCH PARTIAL, and MATCH SIMPLE are allowed, but their use should be avoided, as they cause the MySQL Server to ignore any ON DELETE or ON UPDATE clause used in the same statement. MATCH options do not have any other effect in MySQL, which in effect enforces MATCH SIMPLE semantics full-time.

MySQL requires that foreign key columns be indexed; if you create a table with a foreign key constraint but no index on a given column, an index is created.

You can obtain information about foreign keys from the Information Schema KEY\_COLUMN\_USAGE table. An example of a query against this table is shown here:

```
mysql> SELECT TABLE_SCHEMA, TABLE_NAME, COLUMN_NAME, CONSTRAINT_NAME
 > FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
 > WHERE REFERENCED_TABLE_SCHEMA IS NOT NULL;
+--------------+---------------+-------------+-----------------+
| TABLE_SCHEMA | TABLE_NAME | COLUMN_NAME | CONSTRAINT_NAME |
+--------------+---------------+-------------+-----------------+
| fk1 | myuser | myuser_id | f |
| fk1 | product_order | customer_id | f2 |
| fk1 | product_order | product_id | f1 |
+--------------+---------------+-------------+-----------------+
3 rows in set (0.01 sec)
```

Information about foreign keys on InnoDB tables can also be found in the INNODB\_FOREIGN and INNODB\_FOREIGN\_COLS tables, in the INFORMATION\_SCHEMA database.

InnoDB and NDB tables support foreign keys.