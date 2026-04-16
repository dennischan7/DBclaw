# Oracle 19c - Types-of-SQL-Statements
Source: https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/Types-of-SQL-Statements.html

Data definition language (DDL) statements let you to perform these tasks:

* Create, alter, and drop schema objects
* Grant and revoke privileges and roles
* Analyze information on a table, index, or cluster
* Establish auditing options
* Add comments to the data dictionary

The `CREATE`, `ALTER`, and `DROP` commands require exclusive access to the specified object. For example, an `ALTER` `TABLE` statement fails if another user has an open transaction on the specified table.

The `GRANT`, `REVOKE`, `ANALYZE`, `AUDIT`, and `COMMENT` commands do not require exclusive access to the specified object. For example, you can analyze a table while other users are updating the table.

Oracle Database implicitly commits the current transaction before and after every DDL statement.

A DDL statement is either blocking or nonblocking, and both types of DDL statements require exclusive locks on internal structures.

Many DDL statements may cause Oracle Database to recompile or reauthorize schema objects. For information on how Oracle Database recompiles and reauthorizes schema objects and the circumstances under which a DDL statement would cause this, see [Oracle Database Concepts](/pls/topic/lookup?ctx=en/database/oracle/oracle-database/19/sqlrf&id=CNCPT216).

DDL statements are supported by PL/SQL with the use of the `DBMS_SQL` package.

The DDL statements are:

* `ALTER` ... (All statements beginning with `ALTER`, except `ALTER` `SESSION` and `ALTER` `SYSTEM`âsee "[Session Control Statements](Types-of-SQL-Statements.md#GUID-B8AEC1B3-D1E8-4567-9EFB-8F3410CA70A4)" and "[System Control Statement](Types-of-SQL-Statements.md#GUID-83CC2729-F33B-45D8-A6C5-0D3C654FBFC4)")
* `ANALYZE`
* `ASSOCIATE` `STATISTICS`
* `AUDIT`
* `COMMENT`
* `CREATE` ... (All statements beginning with `CREATE)`
* `DISASSOCIATE` `STATISTICS`
* `DROP` ... (All statements beginning with `DROP)`
* `FLASHBACK` ... (All statements beginning with `FLASHBACK`)
* `GRANT`
* `NOAUDIT`
* `PURGE`
* `RENAME`
* `REVOKE`
* `TRUNCATE`