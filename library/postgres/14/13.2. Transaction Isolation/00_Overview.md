---
source: PostgreSQL 14 Reference
title: 00_Overview
---

The SQL standard defines four levels of transaction isolation. The most strict is Serializable, which is defined by the standard in a paragraph which says that any concurrent execution of a set of Serializable transactions is guaranteed to produce the same effect as running them one at a time in some order. The other three levels are defined in terms of phenomena, resulting from interaction between concurrent transactions, which must not occur at each level. The standard notes that due to the definition of Serializable, none of these phenomena are possible at that level. (This is hardly surprising -- if the effect of the transactions must be consistent with having been run one at a time, how could you see any phenomena caused by interactions?)

The phenomena which are prohibited at various levels are:

dirty read

A transaction reads data written by a concurrent uncommitted transaction.

nonrepeatable read

A transaction re-reads data it has previously read and finds that data has been modified by another transaction (that committed since the initial read).

phantom read

A transaction re-executes a query returning a set of rows that satisfy a search condition and finds that the set of rows satisfying the condition has changed due to another recently-committed transaction.

serialization anomaly

The result of successfully committing a group of transactions is inconsistent with all possible orderings of running those transactions one at a time.

 The SQL standard and PostgreSQL-implemented transaction isolation levels are described in [Ta](#page-112-0)[ble 13.1](#page-112-0).

<span id="page-112-0"></span>**Table 13.1. Transaction Isolation Levels**

| Isolation Level                   | Dirty Read   | Nonrepeatable<br>Read | Phantom Read              | Serialization<br>Anomaly |
|-----------------------------------|--------------|-----------------------|---------------------------|--------------------------|
| Read uncommitted Allowed, but not | in PG        | Possible              | Possible                  | Possible                 |
| Read committed                    | Not possible | Possible              | Possible                  | Possible                 |
| Repeatable read                   | Not possible | Not possible          | Allowed, but not<br>in PG | Possible                 |
| Serializable                      | Not possible | Not possible          | Not possible              | Not possible             |

In PostgreSQL, you can request any of the four standard transaction isolation levels, but internally only three distinct isolation levels are implemented, i.e., PostgreSQL's Read Uncommitted mode behaves like Read Committed. This is because it is the only sensible way to map the standard isolation levels to PostgreSQL's multiversion concurrency control architecture.

The table also shows that PostgreSQL's Repeatable Read implementation does not allow phantom reads. This is acceptable under the SQL standard because the standard specifies which anomalies must *not* occur at certain isolation levels; higher guarantees are acceptable. The behavior of the available isolation levels is detailed in the following subsections.

To set the transaction isolation level of a transaction, use the command SET TRANSACTION.

### **Important**

Some PostgreSQL data types and functions have special rules regarding transactional behavior. In particular, changes made to a sequence (and therefore the counter of a column declared using serial) are immediately visible to all other transactions and are not rolled back if the transaction that made the changes aborts. See Section 9.17 and Section 8.1.4.