---
source: MySQL 5.7 Reference
title: 00_Overview
---

START GROUP\_REPLICATION

Starts Group Replication on this server instance. This statement requires the SUPER privilege. If super\_read\_only=ON and the member should join as a primary, super\_read\_only is set to OFF once Group Replication successfully starts.

A server that participates in a group in single-primary mode should use [skip\\_replica\\_start=ON](https://dev.mysql.com/doc/refman/8.0/en/replication-options-replica.md#sysvar_skip_replica_start). Otherwise, the server is not allowed to join a group as a secondary.

## <span id="page-47-0"></span>**13.4.3.2 STOP GROUP\_REPLICATION Statement**

STOP GROUP\_REPLICATION

Stops Group Replication. This statement requires the [GROUP\\_REPLICATION\\_ADMIN](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.md#priv_group-replication-admin) or SUPER privilege. As soon as you issue [STOP GROUP\\_REPLICATION](#page-47-0) the member is set to super\_read\_only=ON, which ensures that no writes can be made to the member while Group Replication stops. Any other replication channels running on the member are also stopped.

![](_page_47_Picture_13.jpeg)

### **Warning**

Use this statement with extreme caution because it removes the server instance from the group, meaning it is no longer protected by Group Replication's consistency guarantee mechanisms. To be completely safe, ensure that your applications can no longer connect to the instance before issuing this statement to avoid any chance of stale reads.

# <span id="page-47-1"></span>**13.5 Prepared Statements**

MySQL 5.7 provides support for server-side prepared statements. This support takes advantage of the efficient client/server binary protocol. Using prepared statements with placeholders for parameter values has the following benefits:

- Less overhead for parsing the statement each time it is executed. Typically, database applications process large volumes of almost-identical statements, with only changes to literal or variable values in clauses such as WHERE for queries and deletes, SET for updates, and VALUES for inserts.
- Protection against SQL injection attacks. The parameter values can contain unescaped SQL quote and delimiter characters.

The following sections provide an overview of the characteristics of prepared statements:

- [Prepared Statements in Application Programs](#page-48-0)
- [Prepared Statements in SQL Scripts](#page-48-1)
- [PREPARE, EXECUTE, and DEALLOCATE PREPARE Statements](#page-48-2)
- [SQL Syntax Permitted in Prepared Statements](#page-49-0)

# <span id="page-48-0"></span>**Prepared Statements in Application Programs**

You can use server-side prepared statements through client programming interfaces, including the [MySQL C API client library](https://dev.mysql.com/doc/c-api/5.7/en/) for C programs, [MySQL Connector/J](https://dev.mysql.com/doc/connector-j/en/) for Java programs, and [MySQL](https://dev.mysql.com/doc/connector-net/en/) [Connector/NET](https://dev.mysql.com/doc/connector-net/en/) for programs using .NET technologies. For example, the C API provides a set of function calls that make up its prepared statement API. See [C API Prepared Statement Interface.](https://dev.mysql.com/doc/c-api/5.7/en/c-api-prepared-statement-interface.md) Other language interfaces can provide support for prepared statements that use the binary protocol by linking in the C client library, one example being the mysqli [extension,](http://php.net/mysqli) available in PHP 5.0 and higher.

# <span id="page-48-1"></span>**Prepared Statements in SQL Scripts**

An alternative SQL interface to prepared statements is available. This interface is not as efficient as using the binary protocol through a prepared statement API, but requires no programming because it is available directly at the SQL level:

- You can use it when no programming interface is available to you.
- You can use it from any program that can send SQL statements to the server to be executed, such as the mysql client program.
- You can use it even if the client is using an old version of the client library.

SQL syntax for prepared statements is intended to be used for situations such as these:

- To test how prepared statements work in your application before coding it.
- To use prepared statements when you do not have access to a programming API that supports them.
- To interactively troubleshoot application issues with prepared statements.
- To create a test case that reproduces a problem with prepared statements, so that you can file a bug report.

# <span id="page-48-2"></span>**PREPARE, EXECUTE, and DEALLOCATE PREPARE Statements**

SQL syntax for prepared statements is based on three SQL statements:

- [PREPARE](#page-51-0) prepares a statement for execution (see [Section 13.5.1, "PREPARE Statement"\)](#page-51-0).
- [EXECUTE](#page-51-1) executes a prepared statement (see [Section 13.5.2, "EXECUTE Statement"](#page-51-1)).
- [DEALLOCATE PREPARE](#page-52-1) releases a prepared statement (see [Section 13.5.3, "DEALLOCATE](#page-52-1) [PREPARE Statement"](#page-52-1)).

The following examples show two equivalent ways of preparing a statement that computes the hypotenuse of a triangle given the lengths of the two sides.

The first example shows how to create a prepared statement by using a string literal to supply the text of the statement:

```
mysql> PREPARE stmt1 FROM 'SELECT SQRT(POW(?,2) + POW(?,2)) AS hypotenuse';
mysql> SET @a = 3;
mysql> SET @b = 4;
mysql> EXECUTE stmt1 USING @a, @b;
+------------+
| hypotenuse |
+------------+
| 5 |
+------------+
mysql> DEALLOCATE PREPARE stmt1;
```

The second example is similar, but supplies the text of the statement as a user variable:

```
mysql> SET @s = 'SELECT SQRT(POW(?,2) + POW(?,2)) AS hypotenuse';
mysql> PREPARE stmt2 FROM @s;
mysql> SET @a = 6;
mysql> SET @b = 8;
mysql> EXECUTE stmt2 USING @a, @b;
+------------+
| hypotenuse |
+------------+
| 10 |
+------------+
mysql> DEALLOCATE PREPARE stmt2;
```

Here is an additional example that demonstrates how to choose the table on which to perform a query at runtime, by storing the name of the table as a user variable:

```
mysql> USE test;
mysql> CREATE TABLE t1 (a INT NOT NULL);
mysql> INSERT INTO t1 VALUES (4), (8), (11), (32), (80);
mysql> SET @table = 't1';
mysql> SET @s = CONCAT('SELECT * FROM ', @table);
mysql> PREPARE stmt3 FROM @s;
mysql> EXECUTE stmt3;
+----+
| a |
+----+
| 4 |
| 8 |
| 11 |
| 32 |
| 80 |
+----+
mysql> DEALLOCATE PREPARE stmt3;
```

A prepared statement is specific to the session in which it was created. If you terminate a session without deallocating a previously prepared statement, the server deallocates it automatically.

A prepared statement is also global to the session. If you create a prepared statement within a stored routine, it is not deallocated when the stored routine ends.

To guard against too many prepared statements being created simultaneously, set the max\_prepared\_stmt\_count system variable. To prevent the use of prepared statements, set the value to 0.

# <span id="page-49-0"></span>**SQL Syntax Permitted in Prepared Statements**

The following SQL statements can be used as prepared statements:

```
ALTER TABLE
ALTER USER
ANALYZE TABLE
CACHE INDEX
CALL
```

```
CHANGE MASTER
CHECKSUM {TABLE | TABLES}
COMMIT
{CREATE | DROP} INDEX
{CREATE | RENAME | DROP} DATABASE
{CREATE | DROP} TABLE
{CREATE | RENAME | DROP} USER
{CREATE | DROP} VIEW
DELETE
DO
FLUSH {TABLE | TABLES | TABLES WITH READ LOCK | HOSTS | PRIVILEGES
 | LOGS | STATUS | MASTER | SLAVE | DES_KEY_FILE | USER_RESOURCES}
GRANT
INSERT
INSTALL PLUGIN
KILL
LOAD INDEX INTO CACHE
OPTIMIZE TABLE
RENAME TABLE
REPAIR TABLE
REPLACE
RESET {MASTER | SLAVE | QUERY CACHE}
REVOKE
SELECT
SET
SHOW BINLOG EVENTS
SHOW CREATE {PROCEDURE | FUNCTION | EVENT | TABLE | VIEW}
SHOW {MASTER | BINARY} LOGS
SHOW {MASTER | SLAVE} STATUS
SLAVE {START | STOP}
TRUNCATE TABLE
UNINSTALL PLUGIN
UPDATE
```

Other statements are not supported.

For compliance with the SQL standard, which states that diagnostics statements are not preparable, MySQL does not support the following as prepared statements:

- SHOW WARNINGS, SHOW COUNT(\*) WARNINGS
- SHOW ERRORS, SHOW COUNT(\*) ERRORS
- Statements containing any reference to the warning\_count or error\_count system variable.

Generally, statements not permitted in SQL prepared statements are also not permitted in stored programs. Exceptions are noted in Section 23.8, "Restrictions on Stored Programs".

Metadata changes to tables or views referred to by prepared statements are detected and cause automatic repreparation of the statement when it is next executed. For more information, see Section 8.10.4, "Caching of Prepared Statements and Stored Programs".

Placeholders can be used for the arguments of the LIMIT clause when using prepared statements. See Section 13.2.9, "SELECT Statement".

In prepared CALL statements used with [PREPARE](#page-51-0) and [EXECUTE](#page-51-1), placeholder support for OUT and INOUT parameters is available beginning with MySQL 5.7. See Section 13.2.1, "CALL Statement", for an example and a workaround for earlier versions. Placeholders can be used for IN parameters regardless of version.

SQL syntax for prepared statements cannot be used in nested fashion. That is, a statement passed to [PREPARE](#page-51-0) cannot itself be a [PREPARE](#page-51-0), [EXECUTE](#page-51-1), or [DEALLOCATE PREPARE](#page-52-1) statement.

SQL syntax for prepared statements is distinct from using prepared statement API calls. For example, you cannot use the [mysql\\_stmt\\_prepare\(\)](https://dev.mysql.com/doc/c-api/5.7/en/mysql-stmt-prepare.md) C API function to prepare a [PREPARE](#page-51-0), [EXECUTE](#page-51-1), or [DEALLOCATE PREPARE](#page-52-1) statement.

SQL syntax for prepared statements can be used within stored procedures, but not in stored functions or triggers. However, a cursor cannot be used for a dynamic statement that is prepared and executed with [PREPARE](#page-51-0) and [EXECUTE](#page-51-1). The statement for a cursor is checked at cursor creation time, so the statement cannot be dynamic.

SQL syntax for prepared statements does not support multi-statements (that is, multiple statements within a single string separated by ; characters).

Prepared statements use the query cache under the conditions described in Section 8.10.3.1, "How the Query Cache Operates".

To write C programs that use the CALL SQL statement to execute stored procedures that contain prepared statements, the CLIENT\_MULTI\_RESULTS flag must be enabled. This is because each CALL returns a result to indicate the call status, in addition to any result sets that might be returned by statements executed within the procedure.

CLIENT\_MULTI\_RESULTS can be enabled when you call [mysql\\_real\\_connect\(\)](https://dev.mysql.com/doc/c-api/5.7/en/mysql-real-connect.md), either explicitly by passing the CLIENT\_MULTI\_RESULTS flag itself, or implicitly by passing CLIENT\_MULTI\_STATEMENTS (which also enables CLIENT\_MULTI\_RESULTS). For additional information, see Section 13.2.1, "CALL Statement".

# <span id="page-51-0"></span>**13.5.1 PREPARE Statement**

PREPARE stmt\_name FROM preparable\_stmt

The [PREPARE](#page-51-0) statement prepares a SQL statement and assigns it a name, stmt\_name, by which to refer to the statement later. The prepared statement is executed with [EXECUTE](#page-51-1) and released with [DEALLOCATE PREPARE](#page-52-1). For examples, see [Section 13.5, "Prepared Statements".](#page-47-1)

Statement names are not case-sensitive. preparable\_stmt is either a string literal or a user variable that contains the text of the SQL statement. The text must represent a single statement, not multiple statements. Within the statement, ? characters can be used as parameter markers to indicate where data values are to be bound to the query later when you execute it. The ? characters should not be enclosed within quotation marks, even if you intend to bind them to string values. Parameter markers can be used only where data values should appear, not for SQL keywords, identifiers, and so forth.

If a prepared statement with the given name already exists, it is deallocated implicitly before the new statement is prepared. This means that if the new statement contains an error and cannot be prepared, an error is returned and no statement with the given name exists.

The scope of a prepared statement is the session within which it is created, which as several implications:

- A prepared statement created in one session is not available to other sessions.
- When a session ends, whether normally or abnormally, its prepared statements no longer exist. If auto-reconnect is enabled, the client is not notified that the connection was lost. For this reason, clients may wish to disable auto-reconnect. See [Automatic Reconnection Control](https://dev.mysql.com/doc/c-api/5.7/en/c-api-auto-reconnect.md).
- A prepared statement created within a stored program continues to exist after the program finishes executing and can be executed outside the program later.
- A statement prepared in stored program context cannot refer to stored procedure or function parameters or local variables because they go out of scope when the program ends and would be unavailable were the statement to be executed later outside the program. As a workaround, refer instead to user-defined variables, which also have session scope; see Section 9.4, "User-Defined Variables".

# <span id="page-51-1"></span>**13.5.2 EXECUTE Statement**

EXECUTE stmt\_name

```
 [USING @var_name [, @var_name] ...]
```

After preparing a statement with [PREPARE](#page-51-0), you execute it with an [EXECUTE](#page-51-1) statement that refers to the prepared statement name. If the prepared statement contains any parameter markers, you must supply a USING clause that lists user variables containing the values to be bound to the parameters. Parameter values can be supplied only by user variables, and the USING clause must name exactly as many variables as the number of parameter markers in the statement.

You can execute a given prepared statement multiple times, passing different variables to it or setting the variables to different values before each execution.

For examples, see [Section 13.5, "Prepared Statements"](#page-47-1).

# <span id="page-52-1"></span>**13.5.3 DEALLOCATE PREPARE Statement**

```
{DEALLOCATE | DROP} PREPARE stmt_name
```

To deallocate a prepared statement produced with [PREPARE](#page-51-0), use a [DEALLOCATE PREPARE](#page-52-1) statement that refers to the prepared statement name. Attempting to execute a prepared statement after deallocating it results in an error. If too many prepared statements are created and not deallocated by either the DEALLOCATE PREPARE statement or the end of the session, you might encounter the upper limit enforced by the max\_prepared\_stmt\_count system variable.

For examples, see [Section 13.5, "Prepared Statements"](#page-47-1).