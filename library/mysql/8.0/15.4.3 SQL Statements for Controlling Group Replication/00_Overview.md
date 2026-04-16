---
source: MySQL 8.0 Reference
title: 00_Overview
---

This section provides information about the statements used for controlling group replication.

## <span id="page-170-0"></span>**15.4.3.1 START GROUP\_REPLICATION Statement**

```
 START GROUP_REPLICATION
 [USER='user_name']
 [, PASSWORD='user_pass']
 [, DEFAULT_AUTH='plugin_name']
```

Starts group replication. This statement requires the GROUP\_REPLICATION\_ADMIN privilege (or the deprecated SUPER privilege). If super\_read\_only=ON is set and the member should join as a primary, super\_read\_only is set to OFF once Group Replication successfully starts.

A server that participates in a group in single-primary mode should use skip\_replica\_start=ON. Otherwise, the server is not allowed to join a group as a secondary.

In MySQL 8.0.21 and later, you can specify user credentials for distributed recovery on the START GROUP\_REPLICATION statement using the USER, PASSWORD, and DEFAULT\_AUTH options, as follows:

- USER: The replication user for distributed recovery. For instructions to set up this account, see Section 20.2.1.3, "User Credentials For Distributed Recovery". You cannot specify an empty or null string, or omit the USER option if PASSWORD is specified.
- PASSWORD: The password for the replication user account. The password cannot be encrypted, but it is masked in the query log.
- DEFAULT\_AUTH: The name of the authentication plugin used for the replication user account. If you do not specify this option, MySQL native authentication (the mysql\_native\_password plugin) is assumed. This option acts as a hint to the server, and the donor for distributed recovery overrides it if a different plugin is associated with the user account on that server. The authentication plugin used by default when you create user accounts in MySQL 8 is the caching SHA-2 authentication plugin (caching\_sha2\_password). See Section 8.2.17, "Pluggable Authentication" for more information on authentication plugins.

These credentials are used for distributed recovery on the group\_replication\_recovery channel. When you specify user credentials on START GROUP\_REPLICATION, the credentials are saved in memory only, and are removed by a STOP GROUP\_REPLICATION statement or server shutdown. You must issue a START GROUP\_REPLICATION statement to provide the credentials again. This method is therefore not compatible with starting Group Replication automatically on server start, as specified by the group\_replication\_start\_on\_boot system variable.

User credentials specified on START GROUP\_REPLICATION take precedence over any user credentials set for the group\_replication\_recovery channel using a [CHANGE REPLICATION](#page-147-0) [SOURCE TO](#page-147-0) statement (from MySQL 8.0.23) or [CHANGE MASTER TO](#page-129-0) statement (before MySQL 8.0.23). Note that user credentials set using these statements are stored in the replication metadata repositories, and are used when START GROUP\_REPLICATION is specified without user credentials, including automatic starts if the group\_replication\_start\_on\_boot system variable is set to ON. To gain the security benefits of specifying user credentials on START GROUP\_REPLICATION, ensure that group\_replication\_start\_on\_boot is set to OFF (the default is ON), and clear any user credentials previously set for the group\_replication\_recovery channel, following the instructions in Section 20.6.3, "Securing Distributed Recovery Connections".

While a member is rejoining a replication group, its status can be displayed as OFFLINE or ERROR before the group completes the compatibility checks and accepts it as a member. When the member is catching up with the group's transactions, its status is RECOVERING.

## <span id="page-171-0"></span>**15.4.3.2 STOP GROUP\_REPLICATION Statement**

STOP GROUP\_REPLICATION

Stops Group Replication. This statement requires the GROUP\_REPLICATION\_ADMIN privilege (or the deprecated SUPER privilege). As soon as you issue [STOP GROUP\\_REPLICATION](#page-171-0) the member is set to super\_read\_only=ON, which ensures that no writes can be made to the member while Group Replication stops. Any other asynchronous replication channels running on the member are also stopped. Any user credentials that you specified in the [START GROUP\\_REPLICATION](#page-170-0) statement when starting Group Replication on this member are removed from memory, and must be supplied when you start Group Replication again.

![](_page_171_Picture_7.jpeg)

#### **Warning**

Use this statement with extreme caution because it removes the server instance from the group, meaning it is no longer protected by Group Replication's consistency guarantee mechanisms. To be completely safe, ensure that your applications can no longer connect to the instance before issuing this statement to avoid any chance of stale reads.

The [STOP GROUP\\_REPLICATION](#page-171-0) statement stops asynchronous replication channels on the group member, but it does not implicitly commit transactions that are in progress on them like [STOP](#page-168-0) [REPLICA](#page-168-0) does. This is because on a Group Replication group member, an additional transaction committed during the shutdown operation would leave the member inconsistent with the group and cause an issue with rejoining. To avoid failed commits for transactions that are in progress while stopping Group Replication, from MySQL 8.0.28, the [STOP GROUP\\_REPLICATION](#page-171-0) statement cannot be issued while a GTID is assigned as the value of the gtid\_next system variable.

The group\_replication\_components\_stop\_timeout system variable specifies the time for which Group Replication waits for each of its modules to complete ongoing processes after this statement is issued. The timeout is used to resolve situations in which Group Replication components cannot be stopped normally, which can happen if the member is expelled from the group while it is in an error state, or while a process such as MySQL Enterprise Backup is holding a global lock on tables on the member. In such situations, the member cannot stop the applier thread or complete the distributed recovery process to rejoin. STOP GROUP\_REPLICATION does not complete until either the situation is resolved (for example, by the lock being released), or the component timeout expires and the modules are shut down regardless of their status. Prior to MySQL 8.0.27, the default component timeout is 31536000 seconds, or 365 days. With this setting, the component timeout does not help in situations such as those just described, so a lower setting is recommended in those versions of MySQL 8.0. Beginning with MySQL 8.0.27, the default value is 300 seconds; this means that Group Replication components are stopped after 5 minutes if the situation is not resolved before that time, allowing the member to be restarted and rejoin.

# <span id="page-172-3"></span>**15.5 Prepared Statements**

MySQL 8.0 provides support for server-side prepared statements. This support takes advantage of the efficient client/server binary protocol. Using prepared statements with placeholders for parameter values has the following benefits:

- Less overhead for parsing the statement each time it is executed. Typically, database applications process large volumes of almost-identical statements, with only changes to literal or variable values in clauses such as WHERE for queries and deletes, SET for updates, and VALUES for inserts.
- Protection against SQL injection attacks. The parameter values can contain unescaped SQL quote and delimiter characters.

The following sections provide an overview of the characteristics of prepared statements:

- [Prepared Statements in Application Programs](#page-172-0)
- [Prepared Statements in SQL Scripts](#page-172-1)
- [PREPARE, EXECUTE, and DEALLOCATE PREPARE Statements](#page-172-2)
- [SQL Syntax Permitted in Prepared Statements](#page-174-0)

# <span id="page-172-0"></span>**Prepared Statements in Application Programs**

You can use server-side prepared statements through client programming interfaces, including the [MySQL C API client library](https://dev.mysql.com/doc/c-api/8.0/en/) for C programs, [MySQL Connector/J](https://dev.mysql.com/doc/connector-j/en/) for Java programs, and [MySQL](https://dev.mysql.com/doc/connector-net/en/) [Connector/NET](https://dev.mysql.com/doc/connector-net/en/) for programs using .NET technologies. For example, the C API provides a set of function calls that make up its prepared statement API. See [C API Prepared Statement Interface.](https://dev.mysql.com/doc/c-api/8.0/en/c-api-prepared-statement-interface.md) Other language interfaces can provide support for prepared statements that use the binary protocol by linking in the C client library, one example being the mysqli [extension,](http://php.net/mysqli) available in PHP 5.0 and higher.

# <span id="page-172-1"></span>**Prepared Statements in SQL Scripts**

An alternative SQL interface to prepared statements is available. This interface is not as efficient as using the binary protocol through a prepared statement API, but requires no programming because it is available directly at the SQL level:

- You can use it when no programming interface is available to you.
- You can use it from any program that can send SQL statements to the server to be executed, such as the mysql client program.
- You can use it even if the client is using an old version of the client library.

SQL syntax for prepared statements is intended to be used for situations such as these:

- To test how prepared statements work in your application before coding it.
- To use prepared statements when you do not have access to a programming API that supports them.
- To interactively troubleshoot application issues with prepared statements.
- To create a test case that reproduces a problem with prepared statements, so that you can file a bug report.

# <span id="page-172-2"></span>**PREPARE, EXECUTE, and DEALLOCATE PREPARE Statements**

SQL syntax for prepared statements is based on three SQL statements:

• [PREPARE](#page-175-0) prepares a statement for execution (see [Section 15.5.1, "PREPARE Statement"\)](#page-175-0).

- [EXECUTE](#page-177-0) executes a prepared statement (see [Section 15.5.2, "EXECUTE Statement"](#page-177-0)).
- [DEALLOCATE PREPARE](#page-177-1) releases a prepared statement (see [Section 15.5.3, "DEALLOCATE](#page-177-1) [PREPARE Statement"](#page-177-1)).

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

# <span id="page-174-0"></span>**SQL Syntax Permitted in Prepared Statements**

The following SQL statements can be used as prepared statements:

```
ALTER TABLE
ALTER USER {DEFAULT ROLE}
ANALYZE TABLE
CACHE INDEX
CALL
CHANGE {MASTER | REPLICATION FILTER}
CHECKSUM
COMMIT
{CREATE | DROP} INDEX
{CREATE | RENAME | DROP} DATABASE
{CREATE | DROP} TABLE
{CREATE | RENAME | DROP} USER
{CREATE | DROP} VIEW
DELETE
DO
FLUSH
GRANT {ROLE}
INSERT
INSERT ... SELECT
INSTALL PLUGIN
KILL
LOAD INDEX INTO CACHE
OPTIMIZE TABLE
RENAME TABLE
REPAIR TABLE
REPLACE
RESET {MASTER | REPLICA}
REVOKE {ALL | ROLE}
SELECT
SET {PASSWORD | RESOURCE GROUP | ROLE | VARIABLE}
SHOW {BINLOG EVENTS | BINARY LOGS | CHARACTER SETS | COLLATIONS | DATABASES | ENGINE |
 ERRORS | EVENTS | FIELDS | FUNCTION CODE | FUNCTION STATUS | GRANTS | KEYS | OPEN TABLES |
 PLUGINS | PRIVILEGES | PROCEDURE CODE | PROCEDURE STATUS | PROCESSLIST | PROFILE | PROFILES | 
 RELAYLOG EVENTS | REPLICAS | REPLICA STATUS | STATUS | PROCEDURE STATUS | TABLE STATUS | TABLES | 
 TRIGGERS | VARIABLES | WARNINGS}
SHOW CREATE { DATABASE | EVENT | FUNCTION | PROCEDURE | TABLE | TRIGGER | USER | VIEW}
REPLICA {START | STOP}
TRUNCATE
UNINSTALL PLUGIN
UPDATE
```

Other statements are not supported.

For compliance with the SQL standard, which states that diagnostics statements are not preparable, MySQL does not support the following as prepared statements:

- SHOW WARNINGS, SHOW COUNT(\*) WARNINGS
- SHOW ERRORS, SHOW COUNT(\*) ERRORS
- Statements containing any reference to the warning\_count or error\_count system variable.

Generally, statements not permitted in SQL prepared statements are also not permitted in stored programs. Exceptions are noted in Section 27.8, "Restrictions on Stored Programs".

Metadata changes to tables or views referred to by prepared statements are detected and cause automatic repreparation of the statement when it is next executed. For more information, see Section 10.10.3, "Caching of Prepared Statements and Stored Programs".

Placeholders can be used for the arguments of the LIMIT clause when using prepared statements. See [Section 15.2.13, "SELECT Statement".](#page-49-0)

In prepared [CALL](#page-3-0) statements used with [PREPARE](#page-175-0) and [EXECUTE](#page-177-0), placeholder support for OUT and INOUT parameters is available beginning with MySQL 8.0. See [Section 15.2.1, "CALL Statement",](#page-3-0) for an example and a workaround for earlier versions. Placeholders can be used for IN parameters regardless of version.

SQL syntax for prepared statements cannot be used in nested fashion. That is, a statement passed to [PREPARE](#page-175-0) cannot itself be a [PREPARE](#page-175-0), [EXECUTE](#page-177-0), or [DEALLOCATE PREPARE](#page-177-1) statement.

SQL syntax for prepared statements is distinct from using prepared statement API calls. For example, you cannot use the [mysql\\_stmt\\_prepare\(\)](https://dev.mysql.com/doc/c-api/8.0/en/mysql-stmt-prepare.md) C API function to prepare a [PREPARE](#page-175-0), [EXECUTE](#page-177-0), or [DEALLOCATE PREPARE](#page-177-1) statement.

SQL syntax for prepared statements can be used within stored procedures, but not in stored functions or triggers. However, a cursor cannot be used for a dynamic statement that is prepared and executed with [PREPARE](#page-175-0) and [EXECUTE](#page-177-0). The statement for a cursor is checked at cursor creation time, so the statement cannot be dynamic.

SQL syntax for prepared statements does not support multi-statements (that is, multiple statements within a single string separated by ; characters).

To write C programs that use the [CALL](#page-3-0) SQL statement to execute stored procedures that contain prepared statements, the CLIENT\_MULTI\_RESULTS flag must be enabled. This is because each [CALL](#page-3-0) returns a result to indicate the call status, in addition to any result sets that might be returned by statements executed within the procedure.

CLIENT\_MULTI\_RESULTS can be enabled when you call [mysql\\_real\\_connect\(\)](https://dev.mysql.com/doc/c-api/8.0/en/mysql-real-connect.md), either explicitly by passing the CLIENT\_MULTI\_RESULTS flag itself, or implicitly by passing CLIENT\_MULTI\_STATEMENTS (which also enables CLIENT\_MULTI\_RESULTS). For additional information, see [Section 15.2.1, "CALL Statement"](#page-3-0).

# <span id="page-175-0"></span>**15.5.1 PREPARE Statement**

PREPARE stmt\_name FROM preparable\_stmt

The [PREPARE](#page-175-0) statement prepares a SQL statement and assigns it a name, stmt\_name, by which to refer to the statement later. The prepared statement is executed with [EXECUTE](#page-177-0) and released with [DEALLOCATE PREPARE](#page-177-1). For examples, see [Section 15.5, "Prepared Statements".](#page-172-3)

Statement names are not case-sensitive. preparable\_stmt is either a string literal or a user variable that contains the text of the SQL statement. The text must represent a single statement, not multiple statements. Within the statement, ? characters can be used as parameter markers to indicate where data values are to be bound to the query later when you execute it. The ? characters should not be enclosed within quotation marks, even if you intend to bind them to string values. Parameter markers can be used only where data values should appear, not for SQL keywords, identifiers, and so forth.

If a prepared statement with the given name already exists, it is deallocated implicitly before the new statement is prepared. This means that if the new statement contains an error and cannot be prepared, an error is returned and no statement with the given name exists.

The scope of a prepared statement is the session within which it is created, which as several implications:

- A prepared statement created in one session is not available to other sessions.
- When a session ends, whether normally or abnormally, its prepared statements no longer exist. If auto-reconnect is enabled, the client is not notified that the connection was lost. For this reason, clients may wish to disable auto-reconnect. See [Automatic Reconnection Control](https://dev.mysql.com/doc/c-api/8.0/en/c-api-auto-reconnect.md).
- A prepared statement created within a stored program continues to exist after the program finishes executing and can be executed outside the program later.
- A statement prepared in stored program context cannot refer to stored procedure or function parameters or local variables because they go out of scope when the program ends and would be

unavailable were the statement to be executed later outside the program. As a workaround, refer instead to user-defined variables, which also have session scope; see Section 11.4, "User-Defined Variables".

Beginning with MySQL 8.0.22, a parameter used in a prepared statement has its type determined when the statement is first prepared, and retains this type whenever [EXECUTE](#page-177-0) is invoked for this prepared statement (unless the statement is reprepared, as explained later in this section). Rules for determining a parameter's type are listed here:

- A parameter which is an operand of a binary arithmetic operator has the same data type as the other operand.
- If both operands of a binary arithmetic operator are parameters, the type of the parameters is decided by the context of the operator.
- If a parameter is the operand of a unary arithmetic operator, the parameter's type is decided by the context of the operator.
- If an arithmetic operator has no type-determining context, the derived type for any parameters involved is DOUBLE PRECISION. This can happen, for example, when the parameter is a top-level node in a [SELECT](#page-49-0) list, or when it is part of a comparison operator.
- A parameter which is an operand of a character string operator has the same derived type as the aggregated type of the other operands. If all operands of the operator are parameters, the derived type is VARCHAR; its collation is determined by the value of collation\_connection.
- A parameter which is an operand of a temporal operator has type DATETIME if the operator returns a DATETIME, TIME if the operator returns a TIME, and DATE if the operator returns a DATE.
- A parameter which is an operand of a binary comparison operator has the same derived type as the other operand of the comparison.
- A parameter that is an operand of a ternary comparison operator such as BETWEEN has the same derived type as the aggregated type of the other operands.
- If all operands of a comparison operator are parameters, the derived type for each of them is VARCHAR, with collation determined by the value of collation\_connection.
- A parameter that is an output operand of any of CASE, COALESCE, IF, IFNULL, or NULLIF has the same derived type as the aggregated type of the operator's other output operands.
- If all output operands of any of CASE, COALESCE, IF, IFNULL, or NULLIF are parameters, or they are all NULL, the type of the parameter is decided by the context of the operator.
- If the parameter is an operand of any of CASE, COALESCE(), IF, or IFNULL, and has no typedetermining context, the derived type for each of the parameters involved is VARCHAR, and its collation is determined by the value of collation\_connection.
- A parameter which is the operand of a CAST() has the same type as specified by the CAST().
- If a parameter is an immediate member of a [SELECT](#page-49-0) list that is not part of an [INSERT](#page-15-0) statement, the derived type of the parameter is VARCHAR, and its collation is determined by the value of collation\_connection.
- If a parameter is an immediate member of a SELECT list that is part of an [INSERT](#page-15-0) statement, the derived type of the parameter is the type of the corresponding column into which the parameter is inserted.
- If a parameter is used as source for an assignment in a SET clause of an [UPDATE](#page-88-0) statement or in the ON DUPLICATE KEY UPDATE clause of an [INSERT](#page-15-0) statement, the derived type of the parameter is the type of the corresponding column which is updated by the SET or ON DUPLICATE KEY UPDATE clause.

• If a parameter is an argument of a function, the derived type depends on the function's return type.

For some combinations of actual type and derived type, an automatic repreparation of the statement is triggered, to ensure closer compatibility with previous versions of MySQL. Repreparation does not occur if any of the following conditions are true:

- NULL is used as the actual parameter value.
- A parameter is an operand of a CAST(). (Instead, a cast to the derived type is attempted, and an exception raised if the cast fails.)
- A parameter is a string. (In this case, an implicit CAST(? AS derived\_type) is performed.)
- The derived type and actual type of the parameter are both INTEGER and have the same sign.
- The parameter's derived type is DECIMAL and its actual type is either DECIMAL or INTEGER.
- The derived type is DOUBLE and the actual type is any numeric type.
- Both the derived type and the actual type are string types.
- If the derived type is temporal and the actual type is temporal. Exceptions: The derived type is TIME and the actual type is not TIME; the derived type is DATE and the actual type is not DATE.
- The derived type is temporal and the actual type is numeric.

For cases other than those just listed, the statement is reprepared and the actual parameter types are used instead of the derived parameter types.

These rules also apply to a user variable referenced in a prepared statement.

Using a different data type for a given parameter or user variable within a prepared statement for executions of the statement subsequent to the first execution causes the statement to be reprepared. This is less efficient; it may also lead to the parameter's (or variable's) actual type to vary, and thus for results to be inconsistent, with subsequent executions of the prepared statement. For these reasons, it is advisable to use the same data type for a given parameter when re-executing a prepared statement.

# <span id="page-177-0"></span>**15.5.2 EXECUTE Statement**

```
EXECUTE stmt_name
 [USING @var_name [, @var_name] ...]
```

After preparing a statement with [PREPARE](#page-175-0), you execute it with an [EXECUTE](#page-177-0) statement that refers to the prepared statement name. If the prepared statement contains any parameter markers, you must supply a USING clause that lists user variables containing the values to be bound to the parameters. Parameter values can be supplied only by user variables, and the USING clause must name exactly as many variables as the number of parameter markers in the statement.

You can execute a given prepared statement multiple times, passing different variables to it or setting the variables to different values before each execution.

For examples, see [Section 15.5, "Prepared Statements"](#page-172-3).

# <span id="page-177-1"></span>**15.5.3 DEALLOCATE PREPARE Statement**

```
{DEALLOCATE | DROP} PREPARE stmt_name
```

To deallocate a prepared statement produced with [PREPARE](#page-175-0), use a [DEALLOCATE PREPARE](#page-177-1) statement that refers to the prepared statement name. Attempting to execute a prepared statement after deallocating it results in an error. If too many prepared statements are created and not deallocated by

either the DEALLOCATE PREPARE statement or the end of the session, you might encounter the upper limit enforced by the max\_prepared\_stmt\_count system variable.

For examples, see [Section 15.5, "Prepared Statements"](#page-172-3).