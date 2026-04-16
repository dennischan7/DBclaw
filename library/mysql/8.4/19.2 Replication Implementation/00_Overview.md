---
source: MySQL 8.4 Reference
title: 00_Overview
---

Replication is based on the source server keeping track of all changes to its databases (updates, deletes, and so on) in its binary log. The binary log serves as a written record of all events that modify database structure or content (data) from the moment the server was started. Typically, SELECT statements are not recorded because they modify neither database structure nor content.

Each replica that connects to the source requests a copy of the binary log. That is, it pulls the data from the source, rather than the source pushing the data to the replica. The replica also executes the events from the binary log that it receives. This has the effect of repeating the original changes just as they were made on the source. Tables are created or their structure modified, and data is inserted, deleted, and updated according to the changes that were originally made on the source.

Because each replica is independent, the replaying of the changes from the source's binary log occurs independently on each replica that is connected to the source. In addition, because each replica receives a copy of the binary log only by requesting it from the source, the replica is able to read and update the copy of the database at its own pace and can start and stop the replication process at will without affecting the ability to update to the latest database status on either the source or replica side.

For more information on the specifics of the replication implementation, see [Section 19.2.3,](#page-121-0) ["Replication Threads".](#page-121-0)

Source servers and replicas report their status in respect of the replication process regularly so that you can monitor them. See Section 10.14, "Examining Server Thread (Process) Information", for descriptions of all replicated-related states.

The source's binary log is written to a local relay log on the replica before it is processed. The replica also records information about the current position with the source's binary log and the local relay log. See [Section 19.2.4, "Relay Log and Replication Metadata Repositories"](#page-124-1).

Database changes are filtered on the replica according to a set of rules that are applied according to the various configuration options and variables that control event evaluation. For details on how these rules are applied, see [Section 19.2.5, "How Servers Evaluate Replication Filtering Rules"](#page-131-0).

# <span id="page-110-0"></span>**19.2.1 Replication Formats**

Replication works because events written to the binary log are read from the source and then processed on the replica. The events are recorded within the binary log in different formats according to the type of event. The different replication formats used correspond to the binary logging format used when the events were recorded in the source's binary log. The correlation between binary logging formats and the terms used during replication are:

- When using statement-based binary logging, the source writes SQL statements to the binary log. Replication of the source to the replica works by executing the SQL statements on the replica. This is called statement-based replication (which can be abbreviated as SBR), which corresponds to the MySQL statement-based binary logging format.
- When using row-based logging, the source writes events to the binary log that indicate how individual table rows are changed. Replication of the source to the replica works by copying the events representing the changes to the table rows to the replica. This is called row-based replication (which can be abbreviated as RBR).

Row-based logging is the default method.

• You can also configure MySQL to use a mix of both statement-based and row-based logging, depending on which is most appropriate for the change to be logged. This is called mixed-format logging. When using mixed-format logging, a statement-based log is used by default. Depending on certain statements, and also the storage engine being used, the log is automatically switched to row-based in particular cases. Replication using the mixed format is referred to as mixed-based replication or mixed-format replication. For more information, see Section 7.4.4.3, "Mixed Binary Logging Format".

**NDB Cluster.** The default binary logging format in MySQL NDB Cluster 8.4 is ROW. NDB Cluster Replication uses row-based replication; that the NDB storage engine is incompatible with statementbased replication. See Section 25.7.2, "General Requirements for NDB Cluster Replication", for more information.

When using MIXED format, the binary logging format is determined in part by the storage engine being used and the statement being executed. For more information on mixed-format logging and the rules governing the support of different logging formats, see Section 7.4.4.3, "Mixed Binary Logging Format".

The logging format in a running MySQL server is controlled by setting the [binlog\\_format](#page-77-1) server system variable. This variable can be set with session or global scope. The rules governing when and how the new setting takes effect are the same as for other MySQL server system variables. Setting the variable for the current session lasts only until the end of that session, and the change is not visible to other sessions. Setting the variable globally takes effect for clients that connect after the change, but not for any current client sessions, including the session where the variable setting was changed. To make the global system variable setting permanent so that it applies across server restarts, you must set it in an option file. For more information, see Section 15.7.6.1, "SET Syntax for Variable Assignment".

There are conditions under which you cannot change the binary logging format at runtime or doing so causes replication to fail. See Section 7.4.4.2, "Setting The Binary Log Format".

Changing the global [binlog\\_format](#page-77-1) value requires privileges sufficient to set global system variables. Changing the session [binlog\\_format](#page-77-1) value requires privileges sufficient to set restricted session system variables. See Section 7.1.9.1, "System Variable Privileges".

![](_page_111_Picture_10.jpeg)

#### **Note**

Changing the binary logging format ([binlog\\_format](#page-77-1) system variable) was deprecated in MySQL 8.0; in a future version of MySQL, you can expect binlog\_format to be removed altogether, and the row-based format to become the only logging format used by MySQL.

The statement-based and row-based replication formats have different issues and limitations. For a comparison of their relative advantages and disadvantages, see [Section 19.2.1.1, "Advantages and](#page-112-0) [Disadvantages of Statement-Based and Row-Based Replication".](#page-112-0)

With statement-based replication, you may encounter issues with replicating stored routines or triggers. You can avoid these issues by using row-based replication instead. For more information, see Section 27.7, "Stored Program Binary Logging".

## <span id="page-112-0"></span>**19.2.1.1 Advantages and Disadvantages of Statement-Based and Row-Based Replication**

Each binary logging format has advantages and disadvantages. For most users, the mixed replication format should provide the best combination of data integrity and performance. If, however, you want to take advantage of the features specific to the statement-based or row-based replication format when performing certain tasks, you can use the information in this section, which provides a summary of their relative advantages and disadvantages, to determine which is best for your needs.

- [Advantages of statement-based replication](#page-112-1)
- [Disadvantages of statement-based replication](#page-112-2)
- [Advantages of row-based replication](#page-113-0)
- [Disadvantages of row-based replication](#page-114-0)

### <span id="page-112-1"></span>**Advantages of statement-based replication**

- Proven technology.
- Less data written to log files. When updates or deletes affect many rows, this results in much less storage space required for log files. This also means that taking and restoring from backups can be accomplished more quickly.
- Log files contain all statements that made any changes, so they can be used to audit the database.

#### <span id="page-112-2"></span>**Disadvantages of statement-based replication**

- **Statements that are unsafe for SBR.** 
  - Not all statements which modify data (such as INSERT DELETE, UPDATE, and REPLACE statements) can be replicated using statement-based replication. Any nondeterministic behavior is difficult to replicate when using statement-based replication. Examples of such Data Modification Language (DML) statements include the following:
  - A statement that depends on a loadable function or stored program that is nondeterministic, since the value returned by such a function or stored program depends on factors other than the parameters supplied to it. (Row-based replication, however, simply replicates the value returned by the function or stored program, so its effect on table rows and data is the same on both the source and replica.) See [Section 19.5.1.16, "Replication of Invoked Features"](#page-187-0), for more information.
  - DELETE and UPDATE statements that use a LIMIT clause without an ORDER BY are nondeterministic. See [Section 19.5.1.18, "Replication and LIMIT"](#page-188-0).
  - Locking read statements (SELECT ... FOR UPDATE and SELECT ... FOR SHARE) that use NOWAIT or SKIP LOCKED options. See Locking Read Concurrency with NOWAIT and SKIP LOCKED.
  - Deterministic loadable functions must be applied on the replicas.
  - Statements using any of the following functions cannot be replicated properly using statementbased replication:
    - LOAD\_FILE()
    - UUID(), UUID\_SHORT()
    - USER()
    - FOUND\_ROWS()
    - SYSDATE() (unless both the source and the replica are started with the --sysdate-is-now option)

- GET\_LOCK()
- IS\_FREE\_LOCK()
- IS\_USED\_LOCK()
- RAND()
- RELEASE\_LOCK()
- SOURCE\_POS\_WAIT()
- SLEEP()
- VERSION()

However, all other functions are replicated correctly using statement-based replication, including NOW() and so forth.

For more information, see [Section 19.5.1.14, "Replication and System Functions"](#page-185-0).

Statements that cannot be replicated correctly using statement-based replication are logged with a warning like the one shown here:

```
[Warning] Statement is not safe to log in statement format.
```

A similar warning is also issued to the client in such cases. The client can display it using SHOW WARNINGS.

- INSERT ... SELECT requires a greater number of row-level locks than with row-based replication.
- UPDATE statements that require a table scan (because no index is used in the WHERE clause) must lock a greater number of rows than with row-based replication.
- For InnoDB: An INSERT statement that uses AUTO\_INCREMENT blocks other nonconflicting INSERT statements.
- For complex statements, the statement must be evaluated and executed on the replica before the rows are updated or inserted. With row-based replication, the replica only has to modify the affected rows, not execute the full statement.
- If there is an error in evaluation on the replica, particularly when executing complex statements, statement-based replication may slowly increase the margin of error across the affected rows over time. See [Section 19.5.1.29, "Replica Errors During Replication".](#page-193-0)
- Stored functions execute with the same NOW() value as the calling statement. However, this is not true of stored procedures.
- Table definitions must be (nearly) identical on source and replica. See [Section 19.5.1.9, "Replication](#page-180-0) [with Differing Table Definitions on Source and Replica"](#page-180-0), for more information.
- DML operations that read data from MySQL grant tables (through a join list or subquery) but do not modify them are performed as non-locking reads on the MySQL grant tables and are therefore not safe for statement-based replication. For more information, see Grant Table Concurrency.

#### <span id="page-113-0"></span>**Advantages of row-based replication**

• All changes can be replicated. This is the safest form of replication.

![](_page_113_Picture_24.jpeg)

#### **Note**

Statements that update the information in the mysql system schema, such as GRANT, REVOKE and the manipulation of triggers, stored routines (including

stored procedures), and views, are all replicated to replicas using statementbased replication.

For statements such as CREATE TABLE ... SELECT, a CREATE statement is generated from the table definition and replicated using statement-based format, while the row insertions are replicated using row-based format.

- Fewer row locks are required on the source, which thus achieves higher concurrency, for the following types of statements:
  - INSERT ... SELECT
  - INSERT statements with AUTO\_INCREMENT
  - UPDATE or DELETE statements with WHERE clauses that do not use keys or do not change most of the examined rows.
- Fewer row locks are required on the replica for any INSERT, UPDATE, or DELETE statement.

#### <span id="page-114-0"></span>**Disadvantages of row-based replication**

- RBR can generate more data that must be logged. To replicate a DML statement (such as an UPDATE or DELETE statement), statement-based replication writes only the statement to the binary log. By contrast, row-based replication writes each changed row to the binary log. If the statement changes many rows, row-based replication may write significantly more data to the binary log; this is true even for statements that are rolled back. This also means that making and restoring a backup can require more time. In addition, the binary log is locked for a longer time to write the data, which may cause concurrency problems. Use [binlog\\_row\\_image=minimal](#page-83-0) to reduce the disadvantage considerably.
- Deterministic loadable functions that generate large BLOB values take longer to replicate with rowbased replication than with statement-based replication. This is because the BLOB column value is logged, rather than the statement generating the data.
- You cannot see on the replica what statements were received from the source and executed. However, you can see what data was changed using mysqlbinlog with the options --base64 output=DECODE-ROWS and --verbose.

Alternatively, use the [binlog\\_rows\\_query\\_log\\_events](#page-86-0) variable, which if enabled adds a Rows\_query event with the statement to mysqlbinlog output when the -vv option is used.

• For tables using the MyISAM storage engine, a stronger lock is required on the replica for INSERT statements when applying them as row-based events to the binary log than when applying them as statements. This means that concurrent inserts on MyISAM tables are not supported when using rowbased replication.