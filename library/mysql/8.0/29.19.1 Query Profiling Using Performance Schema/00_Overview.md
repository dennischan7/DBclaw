---
source: MySQL 8.0 Reference
title: 00_Overview
---

The following example demonstrates how to use Performance Schema statement events and stage events to retrieve data comparable to profiling information provided by SHOW PROFILES and SHOW PROFILE statements.

The setup\_actors table can be used to limit the collection of historical events by host, user, or account to reduce runtime overhead and the amount of data collected in history tables. The first step of the example shows how to limit collection of historical events to a specific user.

Performance Schema displays event timer information in picoseconds (trillionths of a second) to normalize timing data to a standard unit. In the following example, TIMER\_WAIT values are divided by 1000000000000 to show data in units of seconds. Values are also truncated to 6 decimal places to display data in the same format as SHOW PROFILES and SHOW PROFILE statements.

1. Limit the collection of historical events to the user that runs the query. By default, setup\_actors is configured to allow monitoring and historical event collection for all foreground threads:

```
mysql> SELECT * FROM performance_schema.setup_actors;
+------+------+------+---------+---------+
| HOST | USER | ROLE | ENABLED | HISTORY |
+------+------+------+---------+---------+
| % | % | % | YES | YES |
+------+------+------+---------+---------+
```

Update the default row in the setup\_actors table to disable historical event collection and monitoring for all foreground threads, and insert a new row that enables monitoring and historical event collection for the user that runs the query:

```
mysql> UPDATE performance_schema.setup_actors
 SET ENABLED = 'NO', HISTORY = 'NO'
 WHERE HOST = '%' AND USER = '%';
mysql> INSERT INTO performance_schema.setup_actors
 (HOST,USER,ROLE,ENABLED,HISTORY)
 VALUES('localhost','test_user','%','YES','YES');
```

Data in the setup\_actors table should now appear similar to the following:

```
mysql> SELECT * FROM performance_schema.setup_actors;
+-----------+-----------+------+---------+---------+
| HOST | USER | ROLE | ENABLED | HISTORY |
+-----------+-----------+------+---------+---------+
| % | % | % | NO | NO |
| localhost | test_user | % | YES | YES |
+-----------+-----------+------+---------+---------+
```

2. Ensure that statement and stage instrumentation is enabled by updating the setup\_instruments table. Some instruments may already be enabled by default.

```
mysql> UPDATE performance_schema.setup_instruments
 SET ENABLED = 'YES', TIMED = 'YES'
 WHERE NAME LIKE '%statement/%';
mysql> UPDATE performance_schema.setup_instruments
 SET ENABLED = 'YES', TIMED = 'YES'
 WHERE NAME LIKE '%stage/%';
```

3. Ensure that events\_statements\_\* and events\_stages\_\* consumers are enabled. Some consumers may already be enabled by default.

```
mysql> UPDATE performance_schema.setup_consumers
 SET ENABLED = 'YES'
 WHERE NAME LIKE '%events_statements_%';
mysql> UPDATE performance_schema.setup_consumers
 SET ENABLED = 'YES'
 WHERE NAME LIKE '%events_stages_%';
```

4. Under the user account you are monitoring, run the statement that you want to profile. For example:

```
mysql> SELECT * FROM employees.employees WHERE emp_no = 10001;
+--------+------------+------------+-----------+--------+------------+
| emp_no | birth_date | first_name | last_name | gender | hire_date |
+--------+------------+------------+-----------+--------+------------+
| 10001 | 1953-09-02 | Georgi | Facello | M | 1986-06-26 |
+--------+------------+------------+-----------+--------+------------+
```

5. Identify the EVENT\_ID of the statement by querying the events\_statements\_history\_long table. This step is similar to running SHOW PROFILES to identify the Query\_ID. The following query produces output similar to SHOW PROFILES:

```
mysql> SELECT EVENT_ID, TRUNCATE(TIMER_WAIT/1000000000000,6) as Duration, SQL_TEXT
 FROM performance_schema.events_statements_history_long WHERE SQL_TEXT like '%10001%';
+----------+----------+--------------------------------------------------------+
| event_id | duration | sql_text |
+----------+----------+--------------------------------------------------------+
```

```
| 31 | 0.028310 | SELECT * FROM employees.employees WHERE emp_no = 10001 |
+----------+----------+--------------------------------------------------------+
```

6. Query the events\_stages\_history\_long table to retrieve the statement's stage events. Stages are linked to statements using event nesting. Each stage event record has a NESTING\_EVENT\_ID column that contains the EVENT\_ID of the parent statement.

```
mysql> SELECT event_name AS Stage, TRUNCATE(TIMER_WAIT/1000000000000,6) AS Duration
 FROM performance_schema.events_stages_history_long WHERE NESTING_EVENT_ID=31;
+--------------------------------+----------+
| Stage | Duration |
+--------------------------------+----------+
| stage/sql/starting | 0.000080 |
| stage/sql/checking permissions | 0.000005 |
| stage/sql/Opening tables | 0.027759 |
| stage/sql/init | 0.000052 |
| stage/sql/System lock | 0.000009 |
| stage/sql/optimizing | 0.000006 |
| stage/sql/statistics | 0.000082 |
| stage/sql/preparing | 0.000008 |
| stage/sql/executing | 0.000000 |
| stage/sql/Sending data | 0.000017 |
| stage/sql/end | 0.000001 |
| stage/sql/query end | 0.000004 |
| stage/sql/closing tables | 0.000006 |
| stage/sql/freeing items | 0.000272 |
| stage/sql/cleaning up | 0.000001 |
+--------------------------------+----------+
```

# <span id="page-137-0"></span>**29.19.2 Obtaining Parent Event Information**

The [data\\_locks](#page-33-0) table shows data locks held and requested. Rows of this table have a THREAD\_ID column indicating the thread ID of the session that owns the lock, and an EVENT\_ID column indicating the Performance Schema event that caused the lock. Tuples of (THREAD\_ID, EVENT\_ID) values implicitly identify a parent event in other Performance Schema tables:

- The parent wait event in the events\_waits\_xxx tables
- The parent stage event in the events\_stages\_xxx tables
- The parent statement event in the events\_statements\_xxx tables
- The parent transaction event in the events\_transactions\_current table

To obtain details about the parent event, join the THREAD\_ID and EVENT\_ID columns with the columns of like name in the appropriate parent event table. The relation is based on a nested set data model, so the join has several clauses. Given parent and child tables represented by parent and child, respectively, the join looks like this:

```
WHERE
 parent.THREAD_ID = child.THREAD_ID /* 1 */
 AND parent.EVENT_ID < child.EVENT_ID /* 2 */
 AND (
 child.EVENT_ID <= parent.END_EVENT_ID /* 3a */
 OR parent.END_EVENT_ID IS NULL /* 3b */
 )
```

The conditions for the join are:

- 1. The parent and child events are in the same thread.
- 2. The child event begins after the parent event, so its EVENT\_ID value is greater than that of the parent.
- 3. The parent event has either completed or is still running.

To find lock information, [data\\_locks](#page-33-0) is the table containing child events.

The [data\\_locks](#page-33-0) table shows only existing locks, so these considerations apply regarding which table contains the parent event:

- For transactions, the only choice is events\_transactions\_current. If a transaction is completed, it may be in the transaction history tables, but the locks are gone already.
- For statements, it all depends on whether the statement that took a lock is a statement in a transaction that has already completed (use events\_statements\_history) or the statement is still running (use events\_statements\_current).
- For stages, the logic is similar to that for statements; use events\_stages\_history or events\_stages\_current.
- For waits, the logic is similar to that for statements; use events\_waits\_history or events\_waits\_current. However, so many waits are recorded that the wait that caused a lock is most likely gone from the history tables already.

Wait, stage, and statement events disappear quickly from the history. If a statement that executed a long time ago took a lock but is in a still-open transaction, it might not be possible to find the statement, but it is possible to find the transaction.

This is why the nested set data model works better for locating parent events. Following links in a parent/child relationship (data lock -> parent wait -> parent stage -> parent transaction) does not work well when intermediate nodes are already gone from the history tables.

The following scenario illustrates how to find the parent transaction of a statement in which a lock was taken:

### Session A:

```
[1] START TRANSACTION;
[2] SELECT * FROM t1 WHERE pk = 1;
[3] SELECT 'Hello, world';
```

#### Session B:

```
SELECT ...
FROM performance_schema.events_transactions_current AS parent
 INNER JOIN performance_schema.data_locks AS child
WHERE
 parent.THREAD_ID = child.THREAD_ID
 AND parent.EVENT_ID < child.EVENT_ID
 AND (
 child.EVENT_ID <= parent.END_EVENT_ID
 OR parent.END_EVENT_ID IS NULL
 );
```

The query for session B should show statement [2] as owning a data lock on the record with pk=1.

If session A executes more statements, [2] fades out of the history table.

The query should show the transaction that started in [1], regardless of how many statements, stages, or waits were executed.

To see more data, you can also use the events\_xxx\_history\_long tables, except for transactions, assuming no other query runs in the server (so that history is preserved).