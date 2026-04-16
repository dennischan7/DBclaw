---
source: MySQL 5.7 Reference
title: 00_Overview
---

For a table I/O event, there are usually two rows in [events\\_waits\\_current](#page-23-0), not one. For example, a row fetch might result in rows like this:

```
Row# EVENT_NAME TIMER_START TIMER_END
---- ---------- ----------- ---------
 1 wait/io/file/myisam/dfile 10001 10002
 2 wait/io/table/sql/handler 10000 NULL
```

The row fetch causes a file read. In the example, the table I/O fetch event started before the file I/O event but has not finished (its TIMER\_END value is NULL). The file I/O event is "nested" within the table I/O event.

This occurs because, unlike other "atomic" wait events such as for mutexes or file I/O, table I/O events are "molecular" and include (overlap with) other events. In [events\\_waits\\_current](#page-23-0), the table I/O event usually has two rows:

- One row for the most recent table I/O wait event
- One row for the most recent wait event of any kind

Usually, but not always, the "of any kind" wait event differs from the table I/O event. As each subsidiary event completes, it disappears from [events\\_waits\\_current](#page-23-0). At this point, and until the next subsidiary event begins, the table I/O wait is also the most recent wait of any kind.

# <span id="page-1-0"></span>**25.9 Performance Schema Tables for Current and Historical Events**

For wait, stage, statement, and transaction events, the Performance Schema can monitor and store current events. In addition, when events end, the Performance Schema can store them in history tables. For each event type, the Performance Schema uses three tables for storing current and historical events. The tables have names of the following forms, where xxx indicates the event type (waits, stages, statements, transactions):

- events\_xxx\_current: The "current events" table stores the current monitored event for each thread (one row per thread).
- events\_xxx\_history: The "recent history" table stores the most recent events that have ended per thread (up to a maximum number of rows per thread).
- events\_xxx\_history\_long: The "long history" table stores the most recent events that have ended globally (across all threads, up to a maximum number of rows per table).

The \_current table for each event type contains one row per thread, so there is no system variable for configuring its maximum size. The Performance Schema autosizes the history tables, or the sizes can be configured explicitly at server startup using table-specific system variables, as indicated in the sections that describe the individual history tables. Typical autosized values are 10 rows per thread for \_history tables, and 10,000 rows total for \_history\_long tables.

For each event type, the \_current, \_history, and \_history\_long tables have the same columns.

The \_current tables show what is currently happening within the server. When a current event ends, it is removed from its \_current table.

The \_history and \_history\_long tables show what has happened in the recent past. When the history tables become full, old events are discarded as new events are added. Rows expire from the \_history and \_history\_long tables in different ways because the tables serve different purposes:

- \_history is meant to investigate individual threads, independently of the global server load.
- \_history\_long is meant to investigate the server globally, not each thread.

The difference between the two types of history tables relates to the data retention policy. Both tables contains the same data when an event is first seen. However, data within each table expires differently over time, so that data might be preserved for a longer or shorter time in each table:

- For \_history, when the table contains the maximum number of rows for a given thread, the oldest thread row is discarded when a new row for that thread is added.
- For \_history\_long, when the table becomes full, the oldest row is discarded when a new row is added, regardless of which thread generated either row.

When a thread ends, all its rows are discarded from the \_history table but not from the \_history\_long table.

The following example illustrates the differences in how events are added to and discarded from the two types of history tables. The principles apply equally to all event types. The example is based on these assumptions:

- The Performance Schema is configured to retain 10 rows per thread in the \_history table and 10,000 rows total in the \_history\_long table.
- Thread A generates 1 event per second.

Thread B generates 100 events per second.

• No other threads are running.

After 5 seconds of execution:

- A and B have generated 5 and 500 events, respectively.
- \_history contains 5 rows for A and 10 rows for B. Because storage per thread is limited to 10 rows, no rows have been discarded for A, whereas 490 rows have been discarded for B.
- \_history\_long contains 5 rows for A and 500 rows for B. Because the table has a maximum size of 10,000 rows, no rows have been discarded for either thread.

After 5 minutes (300 seconds) of execution:

- A and B have generated 300 and 30,000 events, respectively.
- \_history contains 10 rows for A and 10 rows for B. Because storage per thread is limited to 10 rows, 290 rows have been discarded for A, whereas 29,990 rows have been discarded for B. Rows for A include data up to 10 seconds old, whereas rows for B include data up to only .1 seconds old.
- \_history\_long contains 10,000 rows. Because A and B together generate 101 events per second, the table contains data up to approximately 10,000/101 = 99 seconds old, with a mix of rows approximately 100 to 1 from B as opposed to A.

# <span id="page-2-0"></span>**25.10 Performance Schema Statement Digests**

The MySQL server is capable of maintaining statement digest information. The digesting process converts each SQL statement to normalized form (the statement digest) and computes an MD5 hash value (the digest hash value) from the normalized result. Normalization permits statements that are similar to be grouped and summarized to expose information about the types of statements the server is executing and how often they occur. This section describes how statement digesting occurs and how it can be useful.

Digesting occurs in the parser regardless of whether the Performance Schema is available, so that other server components such as MySQL Enterprise Firewall and query rewrite plugins have access to statement digests.

- [Statement Digest General Concepts](#page-3-0)
- [Statement Digests in the Performance Schema](#page-4-0)

• [Statement Digest Memory Use](#page-5-0)

# <span id="page-3-0"></span>**Statement Digest General Concepts**

When the parser receives an SQL statement, it computes a statement digest if that digest is needed, which is true if any of the following conditions are true:

- Performance Schema digest instrumentation is enabled
- MySQL Enterprise Firewall is enabled
- A query rewrite plugin is enabled

The max\_digest\_length system variable value determines the maximum number of bytes available per session for computation of normalized statement digests. Once that amount of space is used during digest computation, truncation occurs: no further tokens from a parsed statement are collected or figure into its digest value. Statements that differ only after that many bytes of parsed tokens produce the same normalized statement digest and are considered identical if compared or if aggregated for digest statistics.

![](_page_3_Picture_8.jpeg)

#### **Warning**

Setting the max\_digest\_length system variable to zero disables digest production, which also disables server functionality that requires digests.

After the normalized statement has been computed, an MD5 hash value is computed from it. In addition:

- If MySQL Enterprise Firewall is enabled, it is called and the digest as computed is available to it.
- If any query rewrite plugin is enabled, it is called and the statement digest and digest value are available to it.
- If the Performance Schema has digest instrumentation enabled, it makes a copy of the normalized statement digest, allocating a maximum of [performance\\_schema\\_max\\_digest\\_length](#page-114-0) bytes for it. Consequently, if [performance\\_schema\\_max\\_digest\\_length](#page-114-0) is less than max\_digest\_length, the copy is truncated relative to the original. The copy of the normalized statement digest is stored in the appropriate Performance Schema tables, along with the MD5 hash value computed from the original normalized statement. (If the Performance Schema truncates its copy of the normalized statement digest relative to the original, it does not recompute the MD5 hash value.)

Statement normalization transforms the statement text to a more standardized digest string representation that preserves the general statement structure while removing information not essential to the structure:

- Object identifiers such as database and table names are preserved.
- Literal values are converted to parameter markers. A normalized statement does not retain information such as names, passwords, dates, and so forth.
- Comments are removed and whitespace is adjusted.

Consider these statements:

```
SELECT * FROM orders WHERE customer_id=10 AND quantity>20
SELECT * FROM orders WHERE customer_id = 20 AND quantity > 100
```

To normalize these statements, the parser replaces data values by ? and adjusts whitespace. Both statements yield the same normalized form and thus are considered "the same":

```
SELECT * FROM orders WHERE customer_id = ? AND quantity > ?
```

The normalized statement contains less information but is still representative of the original statement. Other similar statements that have different data values have the same normalized form.

Now consider these statements:

```
SELECT * FROM customers WHERE customer_id = 1000
SELECT * FROM orders WHERE customer_id = 1000
```

In this case, the normalized statements differ because the object identifiers differ:

```
SELECT * FROM customers WHERE customer_id = ?
SELECT * FROM orders WHERE customer_id = ?
```

If normalization produces a statement that exceeds the space available in the digest buffer (as determined by max\_digest\_length), truncation occurs and the text ends with "...". Long normalized statements that differ only in the part that occurs following the "..." are considered the same. Consider these statements:

```
SELECT * FROM mytable WHERE cola = 10 AND colb = 20
SELECT * FROM mytable WHERE cola = 10 AND colc = 20
```

If the cutoff happens to be right after the AND, both statements have this normalized form:

```
SELECT * FROM mytable WHERE cola = ? AND ...
```

In this case, the difference in the second column name is lost and both statements are considered the same.

# <span id="page-4-0"></span>**Statement Digests in the Performance Schema**

In the Performance Schema, statement digesting involves these elements:

- A statements\_digest consumer in the [setup\\_consumers](#page-12-0) table controls whether the Performance Schema maintains digest information. See Statement Digest Consumer.
- The statement event tables ([events\\_statements\\_current](#page-36-0), [events\\_statements\\_history](#page-39-0), and [events\\_statements\\_history\\_long](#page-39-1)) have columns for storing normalized statement digests and the corresponding digest MD5 hash values:
  - DIGEST\_TEXT is the text of the normalized statement digest. This is a copy of the original normalized statement that was computed to a maximum of max\_digest\_length bytes, further truncated as necessary to [performance\\_schema\\_max\\_digest\\_length](#page-114-0) bytes.
  - DIGEST is the digest MD5 hash value computed from the original normalized statement.

See [Section 25.12.6, "Performance Schema Statement Event Tables"](#page-32-0).

• The [events\\_statements\\_summary\\_by\\_digest](#page-78-0) summary table provides aggregated statement digest information. This table aggregates information for statements per SCHEMA\_NAME and DIGEST combination. The Performance Schema uses MD5 hash values for aggregation because they are fast to compute and have a favorable statistical distribution that minimizes collisions. See [Section 25.12.15.3, "Statement Summary Tables".](#page-78-0)

The statement event tables also have an SQL\_TEXT column that contains the original SQL statement. The maximum space available for statement display is 1024 bytes by default. To change this value, set the [performance\\_schema\\_max\\_sql\\_text\\_length](#page-119-0) system variable at server startup.

The [performance\\_schema\\_max\\_digest\\_length](#page-114-0) system variable determines the maximum number of bytes available per statement for digest value storage in the Performance Schema.

However, the display length of statement digests may be longer than the available buffer size due to internal encoding of statement elements such as keywords and literal values. Consequently, values selected from the DIGEST\_TEXT column of statement event tables may appear to exceed the [performance\\_schema\\_max\\_digest\\_length](#page-114-0) value.

The [events\\_statements\\_summary\\_by\\_digest](#page-78-0) summary table provides a profile of the statements executed by the server. It shows what kinds of statements an application is executing and how often. An application developer can use this information together with other information in the table to assess the application's performance characteristics. For example, table columns that show wait times, lock times, or index use may highlight types of queries that are inefficient. This gives the developer insight into which parts of the application need attention.

The [events\\_statements\\_summary\\_by\\_digest](#page-78-0) summary table has a fixed size. By default the Performance Schema estimates the size to use at startup. To specify the table size explicitly, set the [performance\\_schema\\_digests\\_size](#page-110-0) system variable at server startup. If the table becomes full, the Performance Schema groups statements that have SCHEMA\_NAME and DIGEST values not matching existing values in the table in a special row with SCHEMA\_NAME and DIGEST set to NULL. This permits all statements to be counted. However, if the special row accounts for a significant percentage of the statements executed, it might be desirable to increase the summary table size by increasing [performance\\_schema\\_digests\\_size](#page-110-0).

# <span id="page-5-0"></span>**Statement Digest Memory Use**

For applications that generate very long statements that differ only at the end, increasing max\_digest\_length enables computation of digests that distinguish statements that would otherwise aggregate to the same digest. Conversely, decreasing max\_digest\_length causes the server to devote less memory to digest storage but increases the likelihood of longer statements aggregating to the same digest. Administrators should keep in mind that larger values result in correspondingly increased memory requirements, particularly for workloads that involve large numbers of simultaneous sessions (the server allocates max\_digest\_length bytes per session).

As described previously, normalized statement digests as computed by the parser are constrained to a maximum of max\_digest\_length bytes, whereas normalized statement digests stored in the Performance Schema use [performance\\_schema\\_max\\_digest\\_length](#page-114-0) bytes. The following memory-use considerations apply regarding the relative values of max\_digest\_length and [performance\\_schema\\_max\\_digest\\_length](#page-114-0):

- If max\_digest\_length is less than [performance\\_schema\\_max\\_digest\\_length](#page-114-0):
  - Server components other than the Performance Schema use normalized statement digests that take up to max\_digest\_length bytes.
  - The Performance Schema does not further truncate normalized statement digests that it stores, but allocates more memory than max\_digest\_length bytes per digest, which is unnecessary.
- If max\_digest\_length equals [performance\\_schema\\_max\\_digest\\_length](#page-114-0):
  - Server components other than the Performance Schema use normalized statement digests that take up to max\_digest\_length bytes.
  - The Performance Schema does not further truncate normalized statement digests that it stores, and allocates the same amount of memory as max\_digest\_length bytes per digest.
- If max\_digest\_length is greater than [performance\\_schema\\_max\\_digest\\_length](#page-114-0):
  - Server components other than the Performance Schema use normalized statement digests that take up to max\_digest\_length bytes.
  - The Performance Schema further truncates normalized statement digests that it stores, and allocates less memory than max\_digest\_length bytes per digest.

Because the Performance Schema statement event tables might store many digests, setting [performance\\_schema\\_max\\_digest\\_length](#page-114-0) smaller than max\_digest\_length enables administrators to balance these factors:

- The need to have long normalized statement digests available for server components outside the Performance Schema
- Many concurrent sessions, each of which allocates digest-computation memory
- The need to limit memory consumption by the Performance Schema statement event tables when storing many statement digests

The [performance\\_schema\\_max\\_digest\\_length](#page-114-0) setting is not per session, it is per statement, and a session can store multiple statements in the [events\\_statements\\_history](#page-39-0) table. A typical number of statements in this table is 10 per session, so each session consumes 10 times the memory indicated by the [performance\\_schema\\_max\\_digest\\_length](#page-114-0) value, for this table alone.

Also, there are many statements (and digests) collected globally, most notably in the [events\\_statements\\_history\\_long](#page-39-1) table. Here, too, N statements stored consume N times the memory indicated by the [performance\\_schema\\_max\\_digest\\_length](#page-114-0) value.

To assess the amount of memory used for SQL statement storage and digest computation, use the SHOW ENGINE PERFORMANCE\_SCHEMA STATUS statement, or monitor these instruments:

```
mysql> SELECT NAME
 FROM performance_schema.setup_instruments
 WHERE NAME LIKE '%.sqltext';
+------------------------------------------------------------------+
| NAME |
+------------------------------------------------------------------+
| memory/performance_schema/events_statements_history.sqltext |
| memory/performance_schema/events_statements_current.sqltext |
| memory/performance_schema/events_statements_history_long.sqltext |
+------------------------------------------------------------------+
mysql> SELECT NAME
 FROM performance_schema.setup_instruments
 WHERE NAME LIKE 'memory/performance_schema/%.tokens';
+----------------------------------------------------------------------+
| NAME |
+----------------------------------------------------------------------+
| memory/performance_schema/events_statements_history.tokens |
| memory/performance_schema/events_statements_current.tokens |
| memory/performance_schema/events_statements_summary_by_digest.tokens |
| memory/performance_schema/events_statements_history_long.tokens |
+----------------------------------------------------------------------+
```