---
source: MySQL 8.0 Reference
title: 00_Overview
---

Some statements cannot be rolled back. In general, these include data definition language (DDL) statements, such as those that create or drop databases, those that create, drop, or alter tables or stored routines.

You should design your transactions not to include such statements. If you issue a statement early in a transaction that cannot be rolled back, and then another statement later fails, the full effect of the transaction cannot be rolled back in such cases by issuing a [ROLLBACK](#page-106-0) statement.

# <span id="page-109-0"></span>**15.3.3 Statements That Cause an Implicit Commit**

The statements listed in this section (and any synonyms for them) implicitly end any transaction active in the current session, as if you had done a [COMMIT](#page-106-0) before executing the statement.

Most of these statements also cause an implicit commit after executing. The intent is to handle each such statement in its own special transaction. Transaction-control and locking statements are exceptions: If an implicit commit occurs before execution, another does not occur after.

• **Data definition language (DDL) statements that define or modify database objects.** ALTER EVENT, ALTER FUNCTION, ALTER PROCEDURE, ALTER SERVER, ALTER TABLE, ALTER TABLESPACE, ALTER VIEW, CREATE DATABASE, CREATE EVENT, CREATE FUNCTION, CREATE INDEX, CREATE PROCEDURE, CREATE ROLE, CREATE SERVER, CREATE SPATIAL REFERENCE SYSTEM, CREATE TABLE, CREATE TABLESPACE, CREATE TRIGGER, CREATE VIEW, DROP DATABASE, DROP EVENT, DROP FUNCTION, DROP INDEX, DROP PROCEDURE, DROP ROLE, DROP SERVER, DROP SPATIAL REFERENCE SYSTEM, DROP TABLE, DROP TABLESPACE, [DROP](#page-0-0) [TRIGGER](#page-0-0), [DROP VIEW](#page-0-1), INSTALL PLUGIN, [RENAME TABLE](#page-0-2), [TRUNCATE TABLE](#page-2-0), UNINSTALL PLUGIN.

CREATE TABLE and DROP TABLE statements do not commit a transaction if the TEMPORARY keyword is used. (This does not apply to other operations on temporary tables such as ALTER TABLE and CREATE INDEX, which do cause a commit.) However, although no implicit commit occurs, neither can the statement be rolled back, which means that the use of such statements causes transactional atomicity to be violated. For example, if you use CREATE TEMPORARY TABLE and then roll back the transaction, the table remains in existence.

The CREATE TABLE statement in InnoDB is processed as a single transaction. This means that a [ROLLBACK](#page-106-0) from the user does not undo CREATE TABLE statements the user made during that transaction.

CREATE TABLE ... SELECT causes an implicit commit before and after the statement is executed when you are creating nontemporary tables. (No commit occurs for CREATE TEMPORARY TABLE ... SELECT.)

- **Statements that implicitly use or modify tables in the mysql database.** ALTER USER, CREATE USER, DROP USER, GRANT, RENAME USER, REVOKE, SET PASSWORD.
- **Transaction-control and locking statements.** [BEGIN](#page-106-0), [LOCK TABLES](#page-111-0), SET autocommit = 1 (if the value is not already 1), [START TRANSACTION](#page-106-0), [UNLOCK TABLES](#page-111-0).

[UNLOCK TABLES](#page-111-0) commits a transaction only if any tables currently have been locked with [LOCK](#page-111-0) [TABLES](#page-111-0) to acquire nontransactional table locks. A commit does not occur for [UNLOCK TABLES](#page-111-0) following FLUSH TABLES WITH READ LOCK because the latter statement does not acquire tablelevel locks.

Transactions cannot be nested. This is a consequence of the implicit commit performed for any current transaction when you issue a [START TRANSACTION](#page-106-0) statement or one of its synonyms.

Statements that cause an implicit commit cannot be used in an XA transaction while the transaction is in an ACTIVE state.

The [BEGIN](#page-106-0) statement differs from the use of the BEGIN keyword that starts a [BEGIN ... END](#page-178-0) compound statement. The latter does not cause an implicit commit. See [Section 15.6.1, "BEGIN ...](#page-178-0) [END Compound Statement"](#page-178-0).

- **Data loading statements.** [LOAD DATA](#page-26-0). [LOAD DATA](#page-26-0) causes an implicit commit only for tables using the NDB storage engine.
- **Administrative statements.** ANALYZE TABLE, CACHE INDEX, CHECK TABLE, FLUSH, LOAD INDEX INTO CACHE, OPTIMIZE TABLE, REPAIR TABLE, RESET (but not RESET PERSIST).
- **Replication control statements**. [START REPLICA](#page-163-0), [STOP REPLICA](#page-168-0), [RESET REPLICA](#page-161-0), [CHANGE](#page-147-0) [REPLICATION SOURCE TO](#page-147-0), [CHANGE MASTER TO](#page-129-0). The SLAVE keyword was replaced with REPLICA in MySQL 8.0.22.

# <span id="page-110-0"></span>**15.3.4 SAVEPOINT, ROLLBACK TO SAVEPOINT, and RELEASE SAVEPOINT Statements**

```
SAVEPOINT identifier
ROLLBACK [WORK] TO [SAVEPOINT] identifier
RELEASE SAVEPOINT identifier
```

InnoDB supports the SQL statements [SAVEPOINT](#page-110-0), [ROLLBACK TO SAVEPOINT](#page-110-0), [RELEASE](#page-110-0) [SAVEPOINT](#page-110-0) and the optional WORK keyword for [ROLLBACK](#page-106-0).

The [SAVEPOINT](#page-110-0) statement sets a named transaction savepoint with a name of identifier. If the current transaction has a savepoint with the same name, the old savepoint is deleted and a new one is set.

The [ROLLBACK TO SAVEPOINT](#page-110-0) statement rolls back a transaction to the named savepoint without terminating the transaction. Modifications that the current transaction made to rows after the savepoint was set are undone in the rollback, but InnoDB does not release the row locks that were stored in memory after the savepoint. (For a new inserted row, the lock information is carried by the transaction ID stored in the row; the lock is not separately stored in memory. In this case, the row lock is released in the undo.) Savepoints that were set at a later time than the named savepoint are deleted.

If the [ROLLBACK TO SAVEPOINT](#page-110-0) statement returns the following error, it means that no savepoint with the specified name exists:

```
ERROR 1305 (42000): SAVEPOINT identifier does not exist
```

The [RELEASE SAVEPOINT](#page-110-0) statement removes the named savepoint from the set of savepoints of the current transaction. No commit or rollback occurs. It is an error if the savepoint does not exist.

All savepoints of the current transaction are deleted if you execute a [COMMIT](#page-106-0), or a [ROLLBACK](#page-106-0) that does not name a savepoint.

A new savepoint level is created when a stored function is invoked or a trigger is activated. The savepoints on previous levels become unavailable and thus do not conflict with savepoints on the new level. When the function or trigger terminates, any savepoints it created are released and the previous savepoint level is restored.

# <span id="page-111-1"></span>**15.3.5 LOCK INSTANCE FOR BACKUP and UNLOCK INSTANCE Statements**

```
LOCK INSTANCE FOR BACKUP
UNLOCK INSTANCE
```

LOCK INSTANCE FOR BACKUP acquires an instance-level backup lock that permits DML during an online backup while preventing operations that could result in an inconsistent snapshot.

Executing the LOCK INSTANCE FOR BACKUP statement requires the BACKUP\_ADMIN privilege. The BACKUP\_ADMIN privilege is automatically granted to users with the RELOAD privilege when performing an in-place upgrade to MySQL 8.0 from an earlier version.

Multiple sessions can hold a backup lock simultaneously.

UNLOCK INSTANCE releases a backup lock held by the current session. A backup lock held by a session is also released if the session is terminated.

LOCK INSTANCE FOR BACKUP prevents files from being created, renamed, or removed. REPAIR TABLE [TRUNCATE TABLE](#page-2-0), OPTIMIZE TABLE, and account management statements are blocked. See Section 15.7.1, "Account Management Statements". Operations that modify InnoDB files that are not recorded in the InnoDB redo log are also blocked.

LOCK INSTANCE FOR BACKUP permits DDL operations that only affect user-created temporary tables. In effect, files that belong to user-created temporary tables can be created, renamed, or removed while a backup lock is held. Creation of binary log files is also permitted.

[PURGE BINARY LOGS](#page-126-0) should not be issued while a [LOCK INSTANCE FOR BACKUP](#page-111-1) statement is in effect for the instance, because it contravenes the rules of the backup lock by removing files from the server. From MySQL 8.0.28, this is disallowed.

A backup lock acquired by LOCK INSTANCE FOR BACKUP is independent of transactional locks and locks taken by FLUSH TABLES tbl\_name [, tbl\_name] ... WITH READ LOCK, and the following sequences of statements are permitted:

```
LOCK INSTANCE FOR BACKUP;
FLUSH TABLES tbl_name [, tbl_name] ... WITH READ LOCK;
UNLOCK TABLES;
UNLOCK INSTANCE;
FLUSH TABLES tbl_name [, tbl_name] ... WITH READ LOCK;
LOCK INSTANCE FOR BACKUP;
UNLOCK INSTANCE;
UNLOCK TABLES;
```

The lock\_wait\_timeout setting defines the amount of time that a LOCK INSTANCE FOR BACKUP statement waits to acquire a lock before giving up.

# <span id="page-111-0"></span>**15.3.6 LOCK TABLES and UNLOCK TABLES Statements**

```
LOCK {TABLE | TABLES}
 tbl_name [[AS] alias] lock_type
```

```
 [, tbl_name [[AS] alias] lock_type] ...
lock_type: {
 READ [LOCAL]
 | [LOW_PRIORITY] WRITE
}
UNLOCK {TABLE | TABLES}
```

MySQL enables client sessions to acquire table locks explicitly for the purpose of cooperating with other sessions for access to tables, or to prevent other sessions from modifying tables during periods when a session requires exclusive access to them. A session can acquire or release locks only for itself. One session cannot acquire locks for another session or release locks held by another session.

Locks may be used to emulate transactions or to get more speed when updating tables. This is explained in more detail in [Table-Locking Restrictions and Conditions](#page-116-0).

[LOCK TABLES](#page-111-0) explicitly acquires table locks for the current client session. Table locks can be acquired for base tables or views. You must have the LOCK TABLES privilege, and the SELECT privilege for each object to be locked.

For view locking, [LOCK TABLES](#page-111-0) adds all base tables used in the view to the set of tables to be locked and locks them automatically. For tables underlying any view being locked, [LOCK TABLES](#page-111-0) checks that the view definer (for SQL SECURITY DEFINER views) or invoker (for all views) has the proper privileges on the tables.

If you lock a table explicitly with [LOCK TABLES](#page-111-0), any tables used in triggers are also locked implicitly, as described in [LOCK TABLES and Triggers.](#page-115-0)

If you lock a table explicitly with [LOCK TABLES](#page-111-0), any tables related by a foreign key constraint are opened and locked implicitly. For foreign key checks, a shared read-only lock ([LOCK TABLES READ](#page-111-0)) is taken on related tables. For cascading updates, a shared-nothing write lock ([LOCK TABLES WRITE](#page-111-0)) is taken on related tables that are involved in the operation.

[UNLOCK TABLES](#page-111-0) explicitly releases any table locks held by the current session. [LOCK TABLES](#page-111-0) implicitly releases any table locks held by the current session before acquiring new locks.

Another use for [UNLOCK TABLES](#page-111-0) is to release the global read lock acquired with the FLUSH TABLES WITH READ LOCK statement, which enables you to lock all tables in all databases. See Section 15.7.8.3, "FLUSH Statement". (This is a very convenient way to get backups if you have a file system such as Veritas that can take snapshots in time.)

LOCK TABLE is a synonym for LOCK TABLES; UNLOCK TABLE is a synonym for UNLOCK TABLES.

A table lock protects only against inappropriate reads or writes by other sessions. A session holding a WRITE lock can perform table-level operations such as DROP TABLE or [TRUNCATE TABLE](#page-2-0). For sessions holding a READ lock, DROP TABLE and [TRUNCATE TABLE](#page-2-0) operations are not permitted.

The following discussion applies only to non-TEMPORARY tables. [LOCK TABLES](#page-111-0) is permitted (but ignored) for a TEMPORARY table. The table can be accessed freely by the session within which it was created, regardless of what other locking may be in effect. No lock is necessary because no other session can see the table.

- [Table Lock Acquisition](#page-113-0)
- [Table Lock Release](#page-114-0)
- [Interaction of Table Locking and Transactions](#page-114-1)
- [LOCK TABLES and Triggers](#page-115-0)
- [Table-Locking Restrictions and Conditions](#page-116-0)

## <span id="page-113-0"></span>**Table Lock Acquisition**

To acquire table locks within the current session, use the [LOCK TABLES](#page-111-0) statement, which acquires metadata locks (see Section 10.11.4, "Metadata Locking").

The following lock types are available:

```
READ [LOCAL] lock:
```

- The session that holds the lock can read the table (but not write it).
- Multiple sessions can acquire a READ lock for the table at the same time.
- Other sessions can read the table without explicitly acquiring a READ lock.
- The LOCAL modifier enables nonconflicting [INSERT](#page-15-0) statements (concurrent inserts) by other sessions to execute while the lock is held. (See Section 10.11.3, "Concurrent Inserts".) However, READ LOCAL cannot be used if you are going to manipulate the database using processes external to the server while you hold the lock. For InnoDB tables, READ LOCAL is the same as READ.

```
[LOW_PRIORITY] WRITE lock:
```

- The session that holds the lock can read and write the table.
- Only the session that holds the lock can access the table. No other session can access it until the lock is released.
- Lock requests for the table by other sessions block while the WRITE lock is held.
- The LOW\_PRIORITY modifier has no effect. In previous versions of MySQL, it affected locking behavior, but this is no longer true. It is now deprecated and its use produces a warning. Use WRITE without LOW\_PRIORITY instead.

WRITE locks normally have higher priority than READ locks to ensure that updates are processed as soon as possible. This means that if one session obtains a READ lock and then another session requests a WRITE lock, subsequent READ lock requests wait until the session that requested the WRITE lock has obtained the lock and released it. (An exception to this policy can occur for small values of the max\_write\_lock\_count system variable; see Section 10.11.4, "Metadata Locking".)

If the [LOCK TABLES](#page-111-0) statement must wait due to locks held by other sessions on any of the tables, it blocks until all locks can be acquired.

A session that requires locks must acquire all the locks that it needs in a single [LOCK TABLES](#page-111-0) statement. While the locks thus obtained are held, the session can access only the locked tables. For example, in the following sequence of statements, an error occurs for the attempt to access t2 because it was not locked in the [LOCK TABLES](#page-111-0) statement:

```
mysql> LOCK TABLES t1 READ;
mysql> SELECT COUNT(*) FROM t1;
+----------+
| COUNT(*) |
+----------+
| 3 |
+----------+
mysql> SELECT COUNT(*) FROM t2;
ERROR 1100 (HY000): Table 't2' was not locked with LOCK TABLES
```

Tables in the INFORMATION\_SCHEMA database are an exception. They can be accessed without being locked explicitly even while a session holds table locks obtained with [LOCK TABLES](#page-111-0).

You cannot refer to a locked table multiple times in a single query using the same name. Use aliases instead, and obtain a separate lock for the table and each alias:

```
mysql> LOCK TABLE t WRITE, t AS t1 READ;
mysql> INSERT INTO t SELECT * FROM t;
ERROR 1100: Table 't' was not locked with LOCK TABLES
mysql> INSERT INTO t SELECT * FROM t AS t1;
```

The error occurs for the first [INSERT](#page-15-0) because there are two references to the same name for a locked table. The second [INSERT](#page-15-0) succeeds because the references to the table use different names.

If your statements refer to a table by means of an alias, you must lock the table using that same alias. It does not work to lock the table without specifying the alias:

```
mysql> LOCK TABLE t READ;
mysql> SELECT * FROM t AS myalias;
ERROR 1100: Table 'myalias' was not locked with LOCK TABLES
```

Conversely, if you lock a table using an alias, you must refer to it in your statements using that alias:

```
mysql> LOCK TABLE t AS myalias READ;
mysql> SELECT * FROM t;
ERROR 1100: Table 't' was not locked with LOCK TABLES
mysql> SELECT * FROM t AS myalias;
```

## <span id="page-114-0"></span>**Table Lock Release**

When the table locks held by a session are released, they are all released at the same time. A session can release its locks explicitly, or locks may be released implicitly under certain conditions.

- A session can release its locks explicitly with [UNLOCK TABLES](#page-111-0).
- If a session issues a [LOCK TABLES](#page-111-0) statement to acquire a lock while already holding locks, its existing locks are released implicitly before the new locks are granted.
- If a session begins a transaction (for example, with [START TRANSACTION](#page-106-0)), an implicit [UNLOCK](#page-111-0) [TABLES](#page-111-0) is performed, which causes existing locks to be released. (For additional information about the interaction between table locking and transactions, see [Interaction of Table Locking and](#page-114-1) [Transactions](#page-114-1).)

If the connection for a client session terminates, whether normally or abnormally, the server implicitly releases all table locks held by the session (transactional and nontransactional). If the client reconnects, the locks are no longer in effect. In addition, if the client had an active transaction, the server rolls back the transaction upon disconnect, and if reconnect occurs, the new session begins with autocommit enabled. For this reason, clients may wish to disable auto-reconnect. With auto-reconnect in effect, the client is not notified if reconnect occurs but any table locks or current transaction are lost. With auto-reconnect disabled, if the connection drops, an error occurs for the next statement issued. The client can detect the error and take appropriate action such as reacquiring the locks or redoing the transaction. See [Automatic Reconnection Control](https://dev.mysql.com/doc/c-api/8.0/en/c-api-auto-reconnect.md).

![](_page_114_Picture_13.jpeg)

#### **Note**

If you use ALTER TABLE on a locked table, it may become unlocked. For example, if you attempt a second ALTER TABLE operation, the result may be an error Table 'tbl\_name' was not locked with LOCK TABLES. To handle this, lock the table again prior to the second alteration. See also Section B.3.6.1, "Problems with ALTER TABLE".

## <span id="page-114-1"></span>**Interaction of Table Locking and Transactions**

[LOCK TABLES](#page-111-0) and [UNLOCK TABLES](#page-111-0) interact with the use of transactions as follows:

• [LOCK TABLES](#page-111-0) is not transaction-safe and implicitly commits any active transaction before attempting to lock the tables.

• [UNLOCK TABLES](#page-111-0) implicitly commits any active transaction, but only if [LOCK TABLES](#page-111-0) has been used to acquire table locks. For example, in the following set of statements, [UNLOCK TABLES](#page-111-0) releases the global read lock but does not commit the transaction because no table locks are in effect:

```
FLUSH TABLES WITH READ LOCK;
START TRANSACTION;
SELECT ... ;
UNLOCK TABLES;
```

- Beginning a transaction (for example, with [START TRANSACTION](#page-106-0)) implicitly commits any current transaction and releases existing table locks.
- FLUSH TABLES WITH READ LOCK acquires a global read lock and not table locks, so it is not subject to the same behavior as [LOCK TABLES](#page-111-0) and [UNLOCK TABLES](#page-111-0) with respect to table locking and implicit commits. For example, [START TRANSACTION](#page-106-0) does not release the global read lock. See Section 15.7.8.3, "FLUSH Statement".
- Other statements that implicitly cause transactions to be committed do not release existing table locks. For a list of such statements, see [Section 15.3.3, "Statements That Cause an Implicit Commit"](#page-109-0).
- The correct way to use [LOCK TABLES](#page-111-0) and [UNLOCK TABLES](#page-111-0) with transactional tables, such as InnoDB tables, is to begin a transaction with SET autocommit = 0 (not [START TRANSACTION](#page-106-0)) followed by [LOCK TABLES](#page-111-0), and to not call [UNLOCK TABLES](#page-111-0) until you commit the transaction explicitly. For example, if you need to write to table t1 and read from table t2, you can do this:

```
SET autocommit=0;
LOCK TABLES t1 WRITE, t2 READ, ...;
... do something with tables t1 and t2 here ...
COMMIT;
UNLOCK TABLES;
```

When you call [LOCK TABLES](#page-111-0), InnoDB internally takes its own table lock, and MySQL takes its own table lock. InnoDB releases its internal table lock at the next commit, but for MySQL to release its table lock, you have to call [UNLOCK TABLES](#page-111-0). You should not have autocommit = 1, because then InnoDB releases its internal table lock immediately after the call of [LOCK TABLES](#page-111-0), and deadlocks can very easily happen. InnoDB does not acquire the internal table lock at all if autocommit = 1, to help old applications avoid unnecessary deadlocks.

• [ROLLBACK](#page-106-0) does not release table locks.

## <span id="page-115-0"></span>**LOCK TABLES and Triggers**

If you lock a table explicitly with [LOCK TABLES](#page-111-0), any tables used in triggers are also locked implicitly:

- The locks are taken as the same time as those acquired explicitly with the [LOCK TABLES](#page-111-0) statement.
- The lock on a table used in a trigger depends on whether the table is used only for reading. If so, a read lock suffices. Otherwise, a write lock is used.
- If a table is locked explicitly for reading with [LOCK TABLES](#page-111-0), but needs to be locked for writing because it might be modified within a trigger, a write lock is taken rather than a read lock. (That is, an implicit write lock needed due to the table's appearance within a trigger causes an explicit read lock request for the table to be converted to a write lock request.)

Suppose that you lock two tables, t1 and t2, using this statement:

```
LOCK TABLES t1 WRITE, t2 READ;
```

If t1 or t2 have any triggers, tables used within the triggers are also locked. Suppose that t1 has a trigger defined like this:

```
CREATE TRIGGER t1_a_ins AFTER INSERT ON t1 FOR EACH ROW
BEGIN
```

```
 UPDATE t4 SET count = count+1
 WHERE id = NEW.id AND EXISTS (SELECT a FROM t3);
 INSERT INTO t2 VALUES(1, 2);
END;
```

The result of the [LOCK TABLES](#page-111-0) statement is that t1 and t2 are locked because they appear in the statement, and t3 and t4 are locked because they are used within the trigger:

- t1 is locked for writing per the WRITE lock request.
- t2 is locked for writing, even though the request is for a READ lock. This occurs because t2 is inserted into within the trigger, so the READ request is converted to a WRITE request.
- t3 is locked for reading because it is only read from within the trigger.
- t4 is locked for writing because it might be updated within the trigger.

## <span id="page-116-0"></span>**Table-Locking Restrictions and Conditions**

You can safely use KILL to terminate a session that is waiting for a table lock. See Section 15.7.8.4, "KILL Statement".

[LOCK TABLES](#page-111-0) and [UNLOCK TABLES](#page-111-0) cannot be used within stored programs.

Tables in the performance\_schema database cannot be locked with [LOCK TABLES](#page-111-0), except the setup\_xxx tables.

The scope of a lock generated by LOCK TABLES is a single MySQL server. It is not compatible with NDB Cluster, which has no way of enforcing an SQL-level lock across multiple instances of mysqld. You can enforce locking in an API application instead. See Section 25.2.7.10, "Limitations Relating to Multiple NDB Cluster Nodes", for more information.

The following statements are prohibited while a [LOCK TABLES](#page-111-0) statement is in effect: CREATE TABLE, CREATE TABLE ... LIKE, CREATE VIEW, [DROP VIEW](#page-0-1), and DDL statements on stored functions and procedures and events.

For some operations, system tables in the mysql database must be accessed. For example, the HELP statement requires the contents of the server-side help tables, and CONVERT\_TZ() might need to read the time zone tables. The server implicitly locks the system tables for reading as necessary so that you need not lock them explicitly. These tables are treated as just described:

```
mysql.help_category
mysql.help_keyword
mysql.help_relation
mysql.help_topic
mysql.time_zone
mysql.time_zone_leap_second
mysql.time_zone_name
mysql.time_zone_transition
mysql.time_zone_transition_type
```

If you want to explicitly place a WRITE lock on any of those tables with a [LOCK TABLES](#page-111-0) statement, the table must be the only one locked; no other table can be locked with the same statement.

Normally, you do not need to lock tables, because all single [UPDATE](#page-88-0) statements are atomic; no other session can interfere with any other currently executing SQL statement. However, there are a few cases when locking tables may provide an advantage:

• If you are going to run many operations on a set of MyISAM tables, it is much faster to lock the tables you are going to use. Locking MyISAM tables speeds up inserting, updating, or deleting on them because MySQL does not flush the key cache for the locked tables until [UNLOCK TABLES](#page-111-0) is called. Normally, the key cache is flushed after each SQL statement.

The downside to locking the tables is that no session can update a READ-locked table (including the one holding the lock) and no session can access a WRITE-locked table other than the one holding the lock.

• If you are using tables for a nontransactional storage engine, you must use [LOCK TABLES](#page-111-0) if you want to ensure that no other session modifies the tables between a [SELECT](#page-49-0) and an [UPDATE](#page-88-0). The example shown here requires [LOCK TABLES](#page-111-0) to execute safely:

```
LOCK TABLES trans READ, customer WRITE;
SELECT SUM(value) FROM trans WHERE customer_id=some_id;
UPDATE customer
 SET total_value=sum_from_previous_statement
 WHERE customer_id=some_id;
UNLOCK TABLES;
```

Without [LOCK TABLES](#page-111-0), it is possible that another session might insert a new row in the trans table between execution of the [SELECT](#page-49-0) and [UPDATE](#page-88-0) statements.

You can avoid using [LOCK TABLES](#page-111-0) in many cases by using relative updates (UPDATE customer SET value=value+new\_value) or the LAST\_INSERT\_ID() function.

You can also avoid locking tables in some cases by using the user-level advisory lock functions GET\_LOCK() and RELEASE\_LOCK(). These locks are saved in a hash table in the server and implemented with pthread\_mutex\_lock() and pthread\_mutex\_unlock() for high speed. See Section 14.14, "Locking Functions".

See Section 10.11.1, "Internal Locking Methods", for more information on locking policy.

# <span id="page-117-0"></span>**15.3.7 SET TRANSACTION Statement**

```
SET [GLOBAL | SESSION] TRANSACTION
 transaction_characteristic [, transaction_characteristic] ...
transaction_characteristic: {
 ISOLATION LEVEL level
 | access_mode
}
level: {
 REPEATABLE READ
 | READ COMMITTED
 | READ UNCOMMITTED
 | SERIALIZABLE
}
access_mode: {
 READ WRITE
 | READ ONLY
}
```

This statement specifies transaction characteristics. It takes a list of one or more characteristic values separated by commas. Each characteristic value sets the transaction isolation level or access mode. The isolation level is used for operations on InnoDB tables. The access mode specifies whether transactions operate in read/write or read-only mode.

In addition, [SET TRANSACTION](#page-117-0) can include an optional GLOBAL or SESSION keyword to indicate the scope of the statement.

- [Transaction Isolation Levels](#page-118-0)
- [Transaction Access Mode](#page-118-1)
- [Transaction Characteristic Scope](#page-118-2)

## <span id="page-118-0"></span>**Transaction Isolation Levels**

To set the transaction isolation level, use an ISOLATION LEVEL level clause. It is not permitted to specify multiple ISOLATION LEVEL clauses in the same [SET TRANSACTION](#page-117-0) statement.

The default isolation level is REPEATABLE READ. Other permitted values are READ COMMITTED, READ UNCOMMITTED, and SERIALIZABLE. For information about these isolation levels, see Section 17.7.2.1, "Transaction Isolation Levels".

## <span id="page-118-1"></span>**Transaction Access Mode**

To set the transaction access mode, use a READ WRITE or READ ONLY clause. It is not permitted to specify multiple access-mode clauses in the same [SET TRANSACTION](#page-117-0) statement.

By default, a transaction takes place in read/write mode, with both reads and writes permitted to tables used in the transaction. This mode may be specified explicitly using [SET TRANSACTION](#page-117-0) with an access mode of READ WRITE.

If the transaction access mode is set to READ ONLY, changes to tables are prohibited. This may enable storage engines to make performance improvements that are possible when writes are not permitted.

In read-only mode, it remains possible to change tables created with the TEMPORARY keyword using DML statements. Changes made with DDL statements are not permitted, just as with permanent tables.

The READ WRITE and READ ONLY access modes also may be specified for an individual transaction using the [START TRANSACTION](#page-106-0) statement.

# <span id="page-118-2"></span>**Transaction Characteristic Scope**

You can set transaction characteristics globally, for the current session, or for the next transaction only:

- With the GLOBAL keyword:
  - The statement applies globally for all subsequent sessions.
  - Existing sessions are unaffected.
- With the SESSION keyword:
  - The statement applies to all subsequent transactions performed within the current session.
  - The statement is permitted within transactions, but does not affect the current ongoing transaction.
  - If executed between transactions, the statement overrides any preceding statement that sets the next-transaction value of the named characteristics.
- Without any SESSION or GLOBAL keyword:
  - The statement applies only to the next single transaction performed within the session.
  - Subsequent transactions revert to using the session value of the named characteristics.
  - The statement is not permitted within transactions:

```
mysql> START TRANSACTION;
Query OK, 0 rows affected (0.02 sec)
mysql> SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
ERROR 1568 (25001): Transaction characteristics can't be changed
while a transaction is in progress
```

A change to global transaction characteristics requires the CONNECTION\_ADMIN privilege (or the deprecated SUPER privilege). Any session is free to change its session characteristics (even in the middle of a transaction), or the characteristics for its next transaction (prior to the start of that transaction).

To set the global isolation level at server startup, use the --transaction-isolation=level option on the command line or in an option file. Values of level for this option use dashes rather than spaces, so the permissible values are READ-UNCOMMITTED, READ-COMMITTED, REPEATABLE-READ, or SERIALIZABLE.

Similarly, to set the global transaction access mode at server startup, use the --transactionread-only option. The default is OFF (read/write mode) but the value can be set to ON for a mode of read only.

For example, to set the isolation level to REPEATABLE READ and the access mode to READ WRITE, use these lines in the [mysqld] section of an option file:

```
[mysqld]
transaction-isolation = REPEATABLE-READ
transaction-read-only = OFF
```

At runtime, characteristics at the global, session, and next-transaction scope levels can be set indirectly using the [SET TRANSACTION](#page-117-0) statement, as described previously. They can also be set directly using the SET statement to assign values to the transaction\_isolation and transaction\_read\_only system variables:

- [SET TRANSACTION](#page-117-0) permits optional GLOBAL and SESSION keywords for setting transaction characteristics at different scope levels.
- The SET statement for assigning values to the transaction\_isolation and transaction\_read\_only system variables has syntaxes for setting these variables at different scope levels.

The following tables show the characteristic scope level set by each [SET TRANSACTION](#page-117-0) and variableassignment syntax.

| Table 15.9 SET TRANSACTION Syntax for Transaction Characteristics |  |  |
|-------------------------------------------------------------------|--|--|
|-------------------------------------------------------------------|--|--|

| Syntax                                                | Affected Characteristic Scope |
|-------------------------------------------------------|-------------------------------|
| SET GLOBAL TRANSACTION<br>transaction_characteristic  | Global                        |
| SET SESSION TRANSACTION<br>transaction_characteristic | Session                       |
| SET TRANSACTION<br>transaction_characteristic         | Next transaction only         |

**Table 15.10 SET Syntax for Transaction Characteristics**

| Syntax                              | Affected Characteristic Scope |
|-------------------------------------|-------------------------------|
| SET GLOBAL var_name = value         | Global                        |
| SET @@GLOBAL.var_name = value       | Global                        |
| SET PERSIST var_name = value        | Global                        |
| SET @@PERSIST.var_name = value      | Global                        |
| SET PERSIST_ONLY var_name = value   | No runtime effect             |
| SET @@PERSIST_ONLY.var_name = value | No runtime effect             |
| SET SESSION var_name = value        | Session                       |

| Syntax                         | Affected Characteristic Scope |
|--------------------------------|-------------------------------|
| SET @@SESSION.var_name = value | Session                       |
| SET var_name = value           | Session                       |
| SET @@var_name = value         | Next transaction only         |

It is possible to check the global and session values of transaction characteristics at runtime:

```
SELECT @@GLOBAL.transaction_isolation, @@GLOBAL.transaction_read_only;
SELECT @@SESSION.transaction_isolation, @@SESSION.transaction_read_only;
```

# <span id="page-120-0"></span>**15.3.8 XA Transactions**

Support for XA transactions is available for the InnoDB storage engine. The MySQL XA implementation is based on the X/Open CAE document Distributed Transaction Processing: The XA Specification. This document is published by The Open Group and available at [http://](http://www.opengroup.org/public/pubs/catalog/c193.md) [www.opengroup.org/public/pubs/catalog/c193.htm.](http://www.opengroup.org/public/pubs/catalog/c193.md) Limitations of the current XA implementation are described in [Section 15.3.8.3, "Restrictions on XA Transactions"](#page-124-0).

On the client side, there are no special requirements. The XA interface to a MySQL server consists of SQL statements that begin with the XA keyword. MySQL client programs must be able to send SQL statements and to understand the semantics of the XA statement interface. They do not need be linked against a recent client library. Older client libraries also work.

Among the MySQL Connectors, MySQL Connector/J 5.0.0 and higher supports XA directly, by means of a class interface that handles the XA SQL statement interface for you.

XA supports distributed transactions, that is, the ability to permit multiple separate transactional resources to participate in a global transaction. Transactional resources often are RDBMSs but may be other kinds of resources.

A global transaction involves several actions that are transactional in themselves, but that all must either complete successfully as a group, or all be rolled back as a group. In essence, this extends ACID properties "up a level" so that multiple ACID transactions can be executed in concert as components of a global operation that also has ACID properties. (As with nondistributed transactions, SERIALIZABLE may be preferred if your applications are sensitive to read phenomena. REPEATABLE READ may not be sufficient for distributed transactions.)

Some examples of distributed transactions:

- An application may act as an integration tool that combines a messaging service with an RDBMS. The application makes sure that transactions dealing with message sending, retrieval, and processing that also involve a transactional database all happen in a global transaction. You can think of this as "transactional email."
- An application performs actions that involve different database servers, such as a MySQL server and an Oracle server (or multiple MySQL servers), where actions that involve multiple servers must happen as part of a global transaction, rather than as separate transactions local to each server.
- A bank keeps account information in an RDBMS and distributes and receives money through automated teller machines (ATMs). It is necessary to ensure that ATM actions are correctly reflected in the accounts, but this cannot be done with the RDBMS alone. A global transaction manager integrates the ATM and database resources to ensure overall consistency of financial transactions.

Applications that use global transactions involve one or more Resource Managers and a Transaction Manager:

• A Resource Manager (RM) provides access to transactional resources. A database server is one kind of resource manager. It must be possible to either commit or roll back transactions managed by the RM.

• A Transaction Manager (TM) coordinates the transactions that are part of a global transaction. It communicates with the RMs that handle each of these transactions. The individual transactions within a global transaction are "branches" of the global transaction. Global transactions and their branches are identified by a naming scheme described later.

The MySQL implementation of XA enables a MySQL server to act as a Resource Manager that handles XA transactions within a global transaction. A client program that connects to the MySQL server acts as the Transaction Manager.

To carry out a global transaction, it is necessary to know which components are involved, and bring each component to a point when it can be committed or rolled back. Depending on what each component reports about its ability to succeed, they must all commit or roll back as an atomic group. That is, either all components must commit, or all components must roll back. To manage a global transaction, it is necessary to take into account that any component or the connecting network might fail.

The process for executing a global transaction uses two-phase commit (2PC). This takes place after the actions performed by the branches of the global transaction have been executed.

- 1. In the first phase, all branches are prepared. That is, they are told by the TM to get ready to commit. Typically, this means each RM that manages a branch records the actions for the branch in stable storage. The branches indicate whether they are able to do this, and these results are used for the second phase.
- 2. In the second phase, the TM tells the RMs whether to commit or roll back. If all branches indicated when they were prepared that they were able to commit, all branches are told to commit. If any branch indicated when it was prepared that it was not able to commit, all branches are told to roll back.

In some cases, a global transaction might use one-phase commit (1PC). For example, when a Transaction Manager finds that a global transaction consists of only one transactional resource (that is, a single branch), that resource can be told to prepare and commit at the same time.

## <span id="page-121-0"></span>**15.3.8.1 XA Transaction SQL Statements**

To perform XA transactions in MySQL, use the following statements:

```
XA {START|BEGIN} xid [JOIN|RESUME]
XA END xid [SUSPEND [FOR MIGRATE]]
XA PREPARE xid
XA COMMIT xid [ONE PHASE]
XA ROLLBACK xid
XA RECOVER [CONVERT XID]
```

For [XA START](#page-121-0), the JOIN and RESUME clauses are recognized but have no effect.

For [XA END](#page-121-0) the SUSPEND [FOR MIGRATE] clause is recognized but has no effect.

Each XA statement begins with the XA keyword, and most of them require an xid value. An xid is an XA transaction identifier. It indicates which transaction the statement applies to. xid values are supplied by the client, or generated by the MySQL server. An xid value has from one to three parts:

```
xid: gtrid [, bqual [, formatID ]]
```

gtrid is a global transaction identifier, bqual is a branch qualifier, and formatID is a number that identifies the format used by the gtrid and bqual values. As indicated by the syntax, bqual and formatID are optional. The default bqual value is '' if not given. The default formatID value is 1 if not given.

gtrid and bqual must be string literals, each up to 64 bytes (not characters) long. gtrid and bqual can be specified in several ways. You can use a quoted string ('ab'), hex string (X'6162', 0x6162), or bit value (b'nnnn').

formatID is an unsigned integer.

The gtrid and bqual values are interpreted in bytes by the MySQL server's underlying XA support routines. However, while an SQL statement containing an XA statement is being parsed, the server works with some specific character set. To be safe, write gtrid and bqual as hex strings.

xid values typically are generated by the Transaction Manager. Values generated by one TM must be different from values generated by other TMs. A given TM must be able to recognize its own xid values in a list of values returned by the [XA RECOVER](#page-121-0) statement.

[XA START](#page-121-0) xid starts an XA transaction with the given xid value. Each XA transaction must have a unique xid value, so the value must not currently be used by another XA transaction. Uniqueness is assessed using the gtrid and bqual values. All following XA statements for the XA transaction must be specified using the same xid value as that given in the [XA START](#page-121-0) statement. If you use any of those statements but specify an xid value that does not correspond to some existing XA transaction, an error occurs.

Beginning with MySQL 8.0.31, XA START, XA BEGIN, XA END, XA COMMIT, and XA ROLLBACK statements are not filtered by the default database when the server is running with --replicate-dodb or --replicate-ignore-db.

One or more XA transactions can be part of the same global transaction. All XA transactions within a given global transaction must use the same gtrid value in the xid value. For this reason, gtrid values must be globally unique so that there is no ambiguity about which global transaction a given XA transaction is part of. The bqual part of the xid value must be different for each XA transaction within a global transaction. (The requirement that bqual values be different is a limitation of the current MySQL XA implementation. It is not part of the XA specification.)

The [XA RECOVER](#page-121-0) statement returns information for those XA transactions on the MySQL server that are in the PREPARED state. (See [Section 15.3.8.2, "XA Transaction States"](#page-123-0).) The output includes a row for each such XA transaction on the server, regardless of which client started it.

[XA RECOVER](#page-121-0) requires the XA\_RECOVER\_ADMIN privilege. This privilege requirement prevents users from discovering the XID values for outstanding prepared XA transactions other than their own. It does not affect normal commit or rollback of an XA transaction because the user who started it knows its XID.

[XA RECOVER](#page-121-0) output rows look like this (for an example xid value consisting of the parts 'abc', 'def', and 7):

```
mysql> XA RECOVER;
+----------+--------------+--------------+--------+
| formatID | gtrid_length | bqual_length | data |
+----------+--------------+--------------+--------+
| 7 | 3 | 3 | abcdef |
+----------+--------------+--------------+--------+
```

The output columns have the following meanings:

- formatID is the formatID part of the transaction xid
- gtrid\_length is the length in bytes of the gtrid part of the xid
- bqual\_length is the length in bytes of the bqual part of the xid
- data is the concatenation of the gtrid and bqual parts of the xid

XID values may contain nonprintable characters. [XA RECOVER](#page-121-0) permits an optional CONVERT XID clause so that clients can request XID values in hexadecimal.

## <span id="page-123-0"></span>**15.3.8.2 XA Transaction States**

An XA transaction progresses through the following states:

- 1. Use [XA START](#page-121-0) to start an XA transaction and put it in the ACTIVE state.
- 2. For an ACTIVE XA transaction, issue the SQL statements that make up the transaction, and then issue an [XA END](#page-121-0) statement. [XA END](#page-121-0) puts the transaction in the IDLE state.
- 3. For an IDLE XA transaction, you can issue either an [XA PREPARE](#page-121-0) statement or an XA COMMIT ... ONE PHASE statement:
  - [XA PREPARE](#page-121-0) puts the transaction in the PREPARED state. An [XA RECOVER](#page-121-0) statement at this point includes the transaction's xid value in its output, because [XA RECOVER](#page-121-0) lists all XA transactions that are in the PREPARED state.
  - XA COMMIT ... ONE PHASE prepares and commits the transaction. The xid value is not listed by [XA RECOVER](#page-121-0) because the transaction terminates.
- 4. For a PREPARED XA transaction, you can issue an [XA COMMIT](#page-121-0) statement to commit and terminate the transaction, or [XA ROLLBACK](#page-121-0) to roll back and terminate the transaction.

Here is a simple XA transaction that inserts a row into a table as part of a global transaction:

```
mysql> XA START 'xatest';
Query OK, 0 rows affected (0.00 sec)
mysql> INSERT INTO mytable (i) VALUES(10);
Query OK, 1 row affected (0.04 sec)
mysql> XA END 'xatest';
Query OK, 0 rows affected (0.00 sec)
mysql> XA PREPARE 'xatest';
Query OK, 0 rows affected (0.00 sec)
mysql> XA COMMIT 'xatest';
Query OK, 0 rows affected (0.00 sec)
```

In MySQL 8.0.28 and earlier, within the context of a given client connection, XA transactions and local (non-XA) transactions are mutually exclusive. For example, if [XA START](#page-121-0) has been issued to begin an XA transaction, a local transaction cannot be started until the XA transaction has been committed or rolled back. Conversely, if a local transaction has been started with [START TRANSACTION](#page-106-0), no XA statements can be used until the transaction has been committed or rolled back.

MySQL 8.0.29 and later supports detached XA transactions, enabled by the xa\_detach\_on\_prepare system variable (ON by default). Detached transactions are disconnected from the current session following execution of [XA PREPARE](#page-121-0) (and can be committed or rolled back by another connection). This means that the current session is free to start a new local transaction or XA transaction without having to wait for the prepared XA transaction to be committed or rolled back.

When XA transactions are detached, a connection has no special knowledge of any XA transaction that it has prepared. If the current session tries to commit or roll back a given XA transaction (even one which it prepared) after another connection has already done so, the attempt is rejected with an invalid XID error ([ER\\_XAER\\_NOTA](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_xaer_nota)) since the requested xid no longer exists.

![](_page_123_Picture_14.jpeg)

#### **Note**

Detached XA transactions cannot use temporary tables.

When detached XA transactions are disabled (xa\_detach\_on\_prepare set to OFF), an XA transaction remains connected until it is committed or rolled back by the originating connection, as described previously for MySQL 8.0.28 and earlier. Disabling detached XA transactions is not recommended for a MySQL server instance used in group replication; see Server Instance Configuration, for more information.

If an XA transaction is in the ACTIVE state, you cannot issue any statements that cause an implicit commit. That would violate the XA contract because you could not roll back the XA transaction. Trying to execute such a statement raises the following error:

```
ERROR 1399 (XAE07): XAER_RMFAIL: The command cannot be executed
when global transaction is in the ACTIVE state
```

Statements to which the preceding remark applies are listed at [Section 15.3.3, "Statements That Cause](#page-109-0) [an Implicit Commit".](#page-109-0)

## <span id="page-124-0"></span>**15.3.8.3 Restrictions on XA Transactions**

XA transaction support is limited to the InnoDB storage engine.

For "external XA," a MySQL server acts as a Resource Manager and client programs act as Transaction Managers. For "Internal XA", storage engines within a MySQL server act as RMs, and the server itself acts as a TM. Internal XA support is limited by the capabilities of individual storage engines. Internal XA is required for handling XA transactions that involve more than one storage engine. The implementation of internal XA requires that a storage engine support two-phase commit at the table handler level, and currently this is true only for InnoDB.

For [XA START](#page-121-0), the JOIN and RESUME clauses are recognized but have no effect.

For [XA END](#page-121-0) the SUSPEND [FOR MIGRATE] clause is recognized but has no effect.

The requirement that the bqual part of the xid value be different for each XA transaction within a global transaction is a limitation of the current MySQL XA implementation. It is not part of the XA specification.

An XA transaction is written to the binary log in two parts. When XA PREPARE is issued, the first part of the transaction up to XA PREPARE is written using an initial GTID. A XA\_prepare\_log\_event is used to identify such transactions in the binary log. When XA COMMIT or XA ROLLBACK is issued, a second part of the transaction containing only the XA COMMIT or XA ROLLBACK statement is written using a second GTID. Note that the initial part of the transaction, identified by XA\_prepare\_log\_event, is not necessarily followed by its XA COMMIT or XA ROLLBACK, which can cause interleaved binary logging of any two XA transactions. The two parts of the XA transaction can even appear in different binary log files. This means that an XA transaction in PREPARED state is now persistent until an explicit XA COMMIT or XA ROLLBACK statement is issued, ensuring that XA transactions are compatible with replication.

On a replica, immediately after the XA transaction is prepared, it is detached from the replication applier thread, and can be committed or rolled back by any thread on the replica. This means that the same XA transaction can appear in the events\_transactions\_current table with different states on different threads. The events\_transactions\_current table displays the current status of the most recent monitored transaction event on the thread, and does not update this status when the thread is idle. So the XA transaction can still be displayed in the PREPARED state for the original applier thread, after it has been processed by another thread. To positively identify XA transactions that are still in the PREPARED state and need to be recovered, use the [XA RECOVER](#page-121-0) statement rather than the Performance Schema transaction tables.

The following restrictions exist for using XA transactions:

• Prior to MySQL 8.0.30, XA transactions are not fully resilient to an unexpected halt with respect to the binary log. If there is an unexpected halt while the server is in the middle of executing an XA PREPARE, XA COMMIT, XA ROLLBACK, or XA COMMIT ... ONE PHASE statement, the server might not be able to recover to a correct state, leaving the server and the binary log in an inconsistent state. In this situation, the binary log might either contain extra XA transactions that are not applied, or miss XA transactions that are applied. Also, if GTIDs are enabled, after recovery @@GLOBAL.GTID\_EXECUTED might not correctly describe the transactions that have been applied. Note that if an unexpected halt occurs before XA PREPARE, between XA PREPARE and XA COMMIT (or XA ROLLBACK), or after XA COMMIT (or XA ROLLBACK), the server and binary log are correctly recovered and taken to a consistent state.

Beginning with MySQL 8.0.30, this is no longer an issue; the server implements XA PREPARE as a two-phase operation, which maintains the state of the prepare operation between the storage engine and the server, and imposes order of execution between the storage engine and the binary log, so that state is not broadcast before it is consistent and persistent on the server node.

You should be aware that, when the same transaction XID is used to execute XA transactions sequentially and a break occurs during the processing of [XA COMMIT ... ONE PHASE](#page-121-0), it may no longer be possible to synchronize the state between the binary log and the storage engine. This can occur if the series of events just described takes place after this transaction has been prepared in the storage engine, while the XA COMMIT statement is still executing. This is a known issue.

• The use of replication filters or binary log filters in combination with XA transactions is not supported. Filtering of tables could cause an XA transaction to be empty on a replica, and empty XA transactions are not supported. Also, with the replica's connection metadata repository and applier metadata repository stored in InnoDB tables, which became the default in MySQL 8.0, the internal state of the data engine transaction is changed following a filtered XA transaction, and can become inconsistent with the replication transaction context state.

The error [ER\\_XA\\_REPLICATION\\_FILTERS](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_xa_replication_filters) is logged whenever an XA transaction is impacted by a replication filter, whether or not the transaction was empty as a result. If the transaction is not empty, the replica is able to continue running, but you should take steps to discontinue the use of replication filters with XA transactions in order to avoid potential issues. If the transaction is empty, the replica stops. In that event, the replica might be in an undetermined state in which the consistency of the replication process might be compromised. In particular, the gtid\_executed set on a replica of the replica might be inconsistent with that on the source. To resolve this situation, isolate the source and stop all replication, then check GTID consistency across the replication topology. Undo the XA transaction that generated the error message, then restart replication.

• XA transactions are considered unsafe for statement-based replication. If two XA transactions committed in parallel on the source are being prepared on the replica in the inverse order, locking dependencies can occur that cannot be safely resolved, and it is possible for replication to fail with deadlock on the replica. This situation can occur for a single-threaded or multithreaded replica. When binlog\_format=STATEMENT is set, a warning is issued for DML statements inside XA transactions. When binlog\_format=MIXED or binlog\_format=ROW is set, DML statements inside XA transactions are logged using row-based replication, and the potential issue is not present.