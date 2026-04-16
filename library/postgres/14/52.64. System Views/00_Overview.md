---
source: PostgreSQL 14 Reference
title: 00_Overview
---

In addition to the system catalogs, PostgreSQL provides a number of built-in views. Some system views provide convenient access to some commonly used queries on the system catalogs. Other views provide access to internal server state.

The information schema (Chapter 37) provides an alternative set of views which overlap the functionality of the system views. Since the information schema is SQL-standard whereas the views described here are PostgreSQL-specific, it's usually better to use the information schema if it provides all the information you need.

[Table 52.65](#page-49-0) lists the system views described here. More detailed documentation of each view follows below. There are some additional views that provide access to the results of the statistics collector; they are described in Table 28.2.

Except where noted, all the views described here are read-only.

<span id="page-49-0"></span>**Table 52.65. System Views**

| View Name                       | Purpose                               |
|---------------------------------|---------------------------------------|
| pg_available_extensions         | available extensions                  |
| pg_available_extension_versions | available versions of extensions      |
| pg_backend_memory_contexts      | backend memory contexts               |
| pg_config                       | compile-time configuration parameters |
| pg_cursors                      | open cursors                          |

| View Name                    | Purpose                                                                  |  |
|------------------------------|--------------------------------------------------------------------------|--|
| pg_file_settings             | summary of configuration file contents                                   |  |
| pg_group                     | groups of database users                                                 |  |
| pg_hba_file_rules            | summary of client authentication configuration<br>file contents          |  |
| pg_indexes                   | indexes                                                                  |  |
| pg_locks                     | locks currently held or awaited                                          |  |
| pg_matviews                  | materialized views                                                       |  |
| pg_policies                  | policies                                                                 |  |
| pg_prepared_statements       | prepared statements                                                      |  |
| pg_prepared_xacts            | prepared transactions                                                    |  |
| pg_publication_tables        | publications and their associated tables                                 |  |
| pg_replication_origin_status | information about replication origins, including<br>replication progress |  |
| pg_replication_slots         | replication slot information                                             |  |
| pg_roles                     | database roles                                                           |  |
| pg_rules                     | rules                                                                    |  |
| pg_seclabels                 | security labels                                                          |  |
| pg_sequences                 | sequences                                                                |  |
| pg_settings                  | parameter settings                                                       |  |
| pg_shadow                    | database users                                                           |  |
| pg_shmem_allocations         | shared memory allocations                                                |  |
| pg_stats                     | planner statistics                                                       |  |
| pg_stats_ext                 | extended planner statistics                                              |  |
| pg_stats_ext_exprs           | extended planner statistics for expressions                              |  |
| pg_tables                    | tables                                                                   |  |
| pg_timezone_abbrevs          | time zone abbreviations                                                  |  |
| pg_timezone_names            | time zone names                                                          |  |
| pg_user                      | database users                                                           |  |
| pg_user_mappings             | user mappings                                                            |  |
| pg_views                     | views                                                                    |  |

# <span id="page-50-0"></span>**52.65. pg\_available\_extensions**

The pg\_available\_extensions view lists the extensions that are available for installation. See also the [pg\\_extension](#page-19-0) catalog, which shows the extensions currently installed.

**Table 52.66. pg\_available\_extensions Columns**

| Column Type<br>Description                                                    |
|-------------------------------------------------------------------------------|
| name name<br>Extension name                                                   |
| default_version text<br>Name of default version, or NULL if none is specified |
| installed_version text                                                        |

#### **Description**

Currently installed version of the extension, or NULL if not installed

comment text

Comment string from the extension's control file

The pg\_available\_extensions view is read-only.

# <span id="page-51-0"></span>**52.66. pg\_available\_extension\_versions**

The pg\_available\_extension\_versions view lists the specific extension versions that are available for installation. See also the [pg\\_extension](#page-19-0) catalog, which shows the extensions currently installed.

### **Table 52.67. pg\_available\_extension\_versions Columns**

#### **Column Type Description**

name name

Extension name

version text

Version name

installed bool

True if this version of this extension is currently installed

superuser bool

True if only superusers are allowed to install this extension (but see trusted)

trusted bool

True if the extension can be installed by non-superusers with appropriate privileges

relocatable bool

True if extension can be relocated to another schema

schema name

Name of the schema that the extension must be installed into, or NULL if partially or fully relocatable

requires name[]

Names of prerequisite extensions, or NULL if none

comment text

Comment string from the extension's control file

The pg\_available\_extension\_versions view is read-only.

# <span id="page-51-1"></span>**52.67. pg\_backend\_memory\_contexts**

The view pg\_backend\_memory\_contexts displays all the memory contexts of the server process attached to the current session.

pg\_backend\_memory\_contexts contains one row for each memory context.

### **Table 52.68. pg\_backend\_memory\_contexts Columns**

#### **Column Type Description**

name text

| Column Type<br>Description                                                                            |
|-------------------------------------------------------------------------------------------------------|
| Name of the memory context                                                                            |
| ident text<br>Identification information of the memory context. This field is truncated at 1024 bytes |
| parent text<br>Name of the parent of this memory context                                              |
| level int4<br>Distance from TopMemoryContext in context tree                                          |
| total_bytes int8<br>Total bytes allocated for this memory context                                     |
| total_nblocks int8<br>Total number of blocks allocated for this memory context                        |
| free_bytes int8<br>Free space in bytes                                                                |
| free_chunks int8<br>Total number of free chunks                                                       |
| used_bytes int8<br>Used space in bytes                                                                |

By default, the pg\_backend\_memory\_contexts view can be read only by superusers.

# <span id="page-52-0"></span>**52.68. pg\_config**

The view pg\_config describes the compile-time configuration parameters of the currently installed version of PostgreSQL. It is intended, for example, to be used by software packages that want to interface to PostgreSQL to facilitate finding the required header files and libraries. It provides the same basic information as the pg\_config PostgreSQL client application.

By default, the pg\_config view can be read only by superusers.

### **Table 52.69. pg\_config Columns**

## **Column Type Description** name text The parameter name setting text The parameter value

# <span id="page-52-1"></span>**52.69. pg\_cursors**

The pg\_cursors view lists the cursors that are currently available. Cursors can be defined in several ways:

- via the DECLARE statement in SQL
- via the Bind message in the frontend/backend protocol, as described in [Section 53.2.3](#page-83-0)
- via the Server Programming Interface (SPI), as described in Section 47.1

The pg\_cursors view displays cursors created by any of these means. Cursors only exist for the duration of the transaction that defines them, unless they have been declared WITH HOLD. Therefore non-holdable cursors are only present in the view until the end of their creating transaction.

## **Note**

Cursors are used internally to implement some of the components of PostgreSQL, such as procedural languages. Therefore, the pg\_cursors view might include cursors that have not been explicitly created by the user.

### **Table 52.70. pg\_cursors Columns**

### **Column Type Description** name text The name of the cursor statement text The verbatim query string submitted to declare this cursor is\_holdable bool true if the cursor is holdable (that is, it can be accessed after the transaction that declared the cursor has committed); false otherwise is\_binary bool true if the cursor was declared BINARY; false otherwise is\_scrollable bool true if the cursor is scrollable (that is, it allows rows to be retrieved in a nonsequential manner); false otherwise creation\_time timestamptz The time at which the cursor was declared

The pg\_cursors view is read-only.

# <span id="page-53-0"></span>**52.70. pg\_file\_settings**

The view pg\_file\_settings provides a summary of the contents of the server's configuration file(s). A row appears in this view for each "name = value" entry appearing in the files, with annotations indicating whether the value could be applied successfully. Additional row(s) may appear for problems not linked to a "name = value" entry, such as syntax errors in the files.

This view is helpful for checking whether planned changes in the configuration files will work, or for diagnosing a previous failure. Note that this view reports on the *current* contents of the files, not on what was last applied by the server. (The [pg\\_settings](#page-65-0) view is usually sufficient to determine that.)

By default, the pg\_file\_settings view can be read only by superusers.

### **Table 52.71. pg\_file\_settings Columns**

### **Column Type Description** sourcefile text Full path name of the configuration file sourceline int4 Line number within the configuration file where the entry appears seqno int4 Order in which the entries are processed (1..n) name text Configuration parameter name

setting text

Value to be assigned to the parameter

applied bool

True if the value can be applied successfully

error text

If not null, an error message indicating why this entry could not be applied

If the configuration file contains syntax errors or invalid parameter names, the server will not attempt to apply any settings from it, and therefore all the applied fields will read as false. In such a case there will be one or more rows with non-null error fields indicating the problem(s). Otherwise, individual settings will be applied if possible. If an individual setting cannot be applied (e.g., invalid value, or the setting cannot be changed after server start) it will have an appropriate message in the error field. Another way that an entry might have applied = false is that it is overridden by a later entry for the same parameter name; this case is not considered an error so nothing appears in the error field.

See Section 20.1 for more information about the various ways to change run-time parameters.

# <span id="page-54-0"></span>**52.71. pg\_group**

The view pg\_group exists for backwards compatibility: it emulates a catalog that existed in PostgreSQL before version 8.1. It shows the names and members of all roles that are marked as not rolcanlogin, which is an approximation to the set of roles that are being used as groups.

### **Table 52.72. pg\_group Columns**

#### **Column Type Description**

groname name (references [pg\\_authid](#page-5-0).rolname)

Name of the group

grosysid oid (references [pg\\_authid](#page-5-0).oid)

ID of this group

grolist oid[] (references [pg\\_authid](#page-5-0).oid)

An array containing the IDs of the roles in this group

# <span id="page-54-1"></span>**52.72. pg\_hba\_file\_rules**

The view pg\_hba\_file\_rules provides a summary of the contents of the client authentication configuration file, pg\_hba.conf. A row appears in this view for each non-empty, non-comment line in the file, with annotations indicating whether the rule could be applied successfully.

This view can be helpful for checking whether planned changes in the authentication configuration file will work, or for diagnosing a previous failure. Note that this view reports on the *current* contents of the file, not on what was last loaded by the server.

By default, the pg\_hba\_file\_rules view can be read only by superusers.

### **Table 52.73. pg\_hba\_file\_rules Columns**

#### **Column Type Description**

line\_number int4

Line number of this rule in pg\_hba.conf

type text

Type of connection

database text[]

List of database name(s) to which this rule applies

user\_name text[]

List of user and group name(s) to which this rule applies

address text

Host name or IP address, or one of all, samehost, or samenet, or null for local connections

netmask text

IP address mask, or null if not applicable

auth\_method text

Authentication method

options text[]

Options specified for authentication method, if any

error text

If not null, an error message indicating why this line could not be processed

Usually, a row reflecting an incorrect entry will have values for only the line\_number and error fields.

See Chapter 21 for more information about client authentication configuration.

# <span id="page-55-0"></span>**52.73. pg\_indexes**

The view pg\_indexes provides access to useful information about each index in the database.

### **Table 52.74. pg\_indexes Columns**

### **Column Type Description**

schemaname name (references [pg\\_namespace](#page-25-0).nspname)

Name of schema containing table and index

tablename name (references [pg\\_class](#page-8-0).relname)

Name of table the index is for

indexname name (references [pg\\_class](#page-8-0).relname)

Name of index

tablespace name (references [pg\\_tablespace](#page-41-0).spcname)

Name of tablespace containing index (null if default for database)

indexdef text

Index definition (a reconstructed CREATE INDEX command)

# <span id="page-55-1"></span>**52.74. pg\_locks**

The view pg\_locks provides access to information about the locks held by active processes within the database server. See Chapter 13 for more discussion of locking.

pg\_locks contains one row per active lockable object, requested lock mode, and relevant process. Thus, the same lockable object might appear many times, if multiple processes are holding or waiting for locks on it. However, an object that currently has no locks on it will not appear at all.

There are several distinct types of lockable objects: whole relations (e.g., tables), individual pages of relations, individual tuples of relations, transaction IDs (both virtual and permanent IDs), and general database objects (identified by class OID and object OID, in the same way as in [pg\\_description](#page-17-0) or [pg\\_depend](#page-15-0)). Also, the right to extend a relation is represented as a separate lockable object, as is the right to update pg\_database.datfrozenxid. Also, "advisory" locks can be taken on numbers that have user-defined meanings.

### **Table 52.75. pg\_locks Columns**

#### **Column Type Description**

locktype text

Type of the lockable object: relation, extend, frozenid, page, tuple, transactionid, virtualxid, spectoken, object, userlock, or advisory. (See also Table 28.11.)

database oid (references [pg\\_database](#page-13-0).oid)

OID of the database in which the lock target exists, or zero if the target is a shared object, or null if the target is a transaction ID

relation oid (references [pg\\_class](#page-8-0).oid)

OID of the relation targeted by the lock, or null if the target is not a relation or part of a relation

page int4

Page number targeted by the lock within the relation, or null if the target is not a relation page or tuple

tuple int2

Tuple number targeted by the lock within the page, or null if the target is not a tuple

virtualxid text

Virtual ID of the transaction targeted by the lock, or null if the target is not a virtual transaction ID

transactionid xid

ID of the transaction targeted by the lock, or null if the target is not a transaction ID

classid oid (references [pg\\_class](#page-8-0).oid)

OID of the system catalog containing the lock target, or null if the target is not a general database object

objid oid (references any OID column)

OID of the lock target within its system catalog, or null if the target is not a general database object

objsubid int2

Column number targeted by the lock (the classid and objid refer to the table itself), or zero if the target is some other general database object, or null if the target is not a general database object

virtualtransaction text

Virtual ID of the transaction that is holding or awaiting this lock

pid int4

Process ID of the server process holding or awaiting this lock, or null if the lock is held by a prepared transaction

mode text

Name of the lock mode held or desired by this process (see Section 13.3.1 and Section 13.2.3)

granted bool

True if lock is held, false if lock is awaited

fastpath bool

True if lock was taken via fast path, false if taken via main lock table

waitstart timestamptz

Time when the server process started waiting for this lock, or null if the lock is held. Note that this can be null for a very short period of time after the wait started even though granted is false.

granted is true in a row representing a lock held by the indicated process. False indicates that this process is currently waiting to acquire this lock, which implies that at least one other process is holding or waiting for a conflicting lock mode on the same lockable object. The waiting process will sleep until the other lock is released (or a deadlock situation is detected). A single process can be waiting to acquire at most one lock at a time.

Throughout running a transaction, a server process holds an exclusive lock on the transaction's virtual transaction ID. If a permanent ID is assigned to the transaction (which normally happens only if the transaction changes the state of the database), it also holds an exclusive lock on the transaction's permanent transaction ID until it ends. When a process finds it necessary to wait specifically for another transaction to end, it does so by attempting to acquire share lock on the other transaction's ID (either virtual or permanent ID depending on the situation). That will succeed only when the other transaction terminates and releases its locks.

Although tuples are a lockable type of object, information about row-level locks is stored on disk, not in memory, and therefore row-level locks normally do not appear in this view. If a process is waiting for a row-level lock, it will usually appear in the view as waiting for the permanent transaction ID of the current holder of that row lock.

Advisory locks can be acquired on keys consisting of either a single bigint value or two integer values. A bigint key is displayed with its high-order half in the classid column, its low-order half in the objid column, and objsubid equal to 1. The original bigint value can be reassembled with the expression (classid::bigint << 32) | objid::bigint. Integer keys are displayed with the first key in the classid column, the second key in the objid column, and objsubid equal to 2. The actual meaning of the keys is up to the user. Advisory locks are local to each database, so the database column is meaningful for an advisory lock.

pg\_locks provides a global view of all locks in the database cluster, not only those relevant to the current database. Although its relation column can be joined against [pg\\_class](#page-8-0).oid to identify locked relations, this will only work correctly for relations in the current database (those for which the database column is either the current database's OID or zero).

The pid column can be joined to the pid column of the pg\_stat\_activity view to get more information on the session holding or awaiting each lock, for example

```
SELECT * FROM pg_locks pl LEFT JOIN pg_stat_activity psa
 ON pl.pid = psa.pid;
```

Also, if you are using prepared transactions, the virtualtransaction column can be joined to the transaction column of the [pg\\_prepared\\_xacts](#page-60-1) view to get more information on prepared transactions that hold locks. (A prepared transaction can never be waiting for a lock, but it continues to hold the locks it acquired while running.) For example:

```
SELECT * FROM pg_locks pl LEFT JOIN pg_prepared_xacts ppx
 ON pl.virtualtransaction = '-1/' || ppx.transaction;
```

While it is possible to obtain information about which processes block which other processes by joining pg\_locks against itself, this is very difficult to get right in detail. Such a query would have to encode knowledge about which lock modes conflict with which others. Worse, the pg\_locks view does not expose information about which processes are ahead of which others in lock wait queues, nor information about which processes are parallel workers running on behalf of which other client sessions. It is better to use the pg\_blocking\_pids() function (see Table 9.65) to identify which process(es) a waiting process is blocked behind.

The pg\_locks view displays data from both the regular lock manager and the predicate lock manager, which are separate systems; in addition, the regular lock manager subdivides its locks into regular and *fast-path* locks. This data is not guaranteed to be entirely consistent. When the view is queried, data on fast-path locks (with fastpath = true) is gathered from each backend one at a time, without freezing the state of the entire lock manager, so it is possible for locks to be taken or released while information is gathered. Note, however, that these locks are known not to conflict with any other lock currently in place. After all backends have been queried for fast-path locks, the remainder of the regular lock manager is locked as a unit, and a consistent snapshot of all remaining locks is collected as an atomic action. After unlocking the regular lock manager, the predicate lock manager is similarly locked and all predicate locks are collected as an atomic action. Thus, with the exception of fast-path locks, each lock manager will deliver a consistent set of results, but as we do not lock both lock managers simultaneously, it is possible for locks to be taken or released after we interrogate the regular lock manager and before we interrogate the predicate lock manager.

Locking the regular and/or predicate lock manager could have some impact on database performance if this view is very frequently accessed. The locks are held only for the minimum amount of time necessary to obtain data from the lock managers, but this does not completely eliminate the possibility of a performance impact.

# <span id="page-58-0"></span>**52.75. pg\_matviews**

The view pg\_matviews provides access to useful information about each materialized view in the database.

### **Table 52.76. pg\_matviews Columns**

## **Column Type Description**

schemaname name (references [pg\\_namespace](#page-25-0).nspname)

Name of schema containing materialized view

matviewname name (references [pg\\_class](#page-8-0).relname)

Name of materialized view

matviewowner name (references [pg\\_authid](#page-5-0).rolname)

Name of materialized view's owner

tablespace name (references [pg\\_tablespace](#page-41-0).spcname)

Name of tablespace containing materialized view (null if default for database)

hasindexes bool

True if materialized view has (or recently had) any indexes

ispopulated bool

True if materialized view is currently populated

definition text

Materialized view definition (a reconstructed SELECT query)

# <span id="page-58-1"></span>**52.76. pg\_policies**

The view pg\_policies provides access to useful information about each row-level security policy in the database.

### **Table 52.77. pg\_policies Columns**

#### **Column Type**

#### **Description**

schemaname name (references [pg\\_namespace](#page-25-0).nspname)

Name of schema containing table policy is on

tablename name (references [pg\\_class](#page-8-0).relname)

Name of table policy is on

policyname name (references [pg\\_policy](#page-28-0).polname)

Name of policy

permissive text

Is the policy permissive or restrictive?

roles name[]

The roles to which this policy applies

cmd text

The command type to which the policy is applied

qual text

The expression added to the security barrier qualifications for queries that this policy applies to

with\_check text

The expression added to the WITH CHECK qualifications for queries that attempt to add rows to this table

# <span id="page-59-0"></span>**52.77. pg\_prepared\_statements**

The pg\_prepared\_statements view displays all the prepared statements that are available in the current session. See PREPARE for more information about prepared statements.

pg\_prepared\_statements contains one row for each prepared statement. Rows are added to the view when a new prepared statement is created and removed when a prepared statement is released (for example, via the DEALLOCATE command).

### **Table 52.78. pg\_prepared\_statements Columns**

#### **Column Type**

#### **Description**

name text

The identifier of the prepared statement

statement text

The query string submitted by the client to create this prepared statement. For prepared statements created via SQL, this is the PREPARE statement submitted by the client. For prepared statements created via the frontend/backend protocol, this is the text of the prepared statement itself.

prepare\_time timestamptz

The time at which the prepared statement was created

parameter\_types regtype[]

The expected parameter types for the prepared statement in the form of an array of regtype. The OID corresponding to an element of this array can be obtained by casting the regtype value to oid.

from\_sql bool

true if the prepared statement was created via the PREPARE SQL command; false if the statement was prepared via the frontend/backend protocol

generic\_plans int8

Number of times generic plan was chosen

custom\_plans int8

Number of times custom plan was chosen

The pg\_prepared\_statements view is read-only.

# <span id="page-60-1"></span>**52.78. pg\_prepared\_xacts**

The view pg\_prepared\_xacts displays information about transactions that are currently prepared for two-phase commit (see PREPARE TRANSACTION for details).

pg\_prepared\_xacts contains one row per prepared transaction. An entry is removed when the transaction is committed or rolled back.

### **Table 52.79. pg\_prepared\_xacts Columns**

#### **Column Type Description**

transaction xid

Numeric transaction identifier of the prepared transaction

gid text

Global transaction identifier that was assigned to the transaction

prepared timestamptz

Time at which the transaction was prepared for commit

owner name (references [pg\\_authid](#page-5-0).rolname)

Name of the user that executed the transaction

database name (references [pg\\_database](#page-13-0).datname)

Name of the database in which the transaction was executed

When the pg\_prepared\_xacts view is accessed, the internal transaction manager data structures are momentarily locked, and a copy is made for the view to display. This ensures that the view produces a consistent set of results, while not blocking normal operations longer than necessary. Nonetheless there could be some impact on database performance if this view is frequently accessed.

# <span id="page-60-0"></span>**52.79. pg\_publication\_tables**

The view pg\_publication\_tables provides information about the mapping between publications and the tables they contain. Unlike the underlying catalog [pg\\_publication\\_rel](#page-32-0), this view expands publications defined as FOR ALL TABLES, so for such publications there will be a row for each eligible table.

### **Table 52.80. pg\_publication\_tables Columns**

### **Column Type Description**

pubname name (references [pg\\_publication](#page-31-0).pubname)

Name of publication

schemaname name (references [pg\\_namespace](#page-25-0).nspname)

Name of schema containing table

tablename name (references [pg\\_class](#page-8-0).relname)

Name of table

# <span id="page-61-0"></span>**52.80. pg\_replication\_origin\_status**

The pg\_replication\_origin\_status view contains information about how far replay for a certain origin has progressed. For more on replication origins see Chapter 50.

### **Table 52.81. pg\_replication\_origin\_status Columns**

## **Column Type**

#### **Description**

local\_id oid (references [pg\\_replication\\_origin](#page-33-1).roident) internal node identifier

external\_id text (references [pg\\_replication\\_origin](#page-33-1).roname) external node identifier

remote\_lsn pg\_lsn

The origin node's LSN up to which data has been replicated.

local\_lsn pg\_lsn

This node's LSN at which remote\_lsn has been replicated. Used to flush commit records before persisting data to disk when using asynchronous commits.

# <span id="page-61-1"></span>**52.81. pg\_replication\_slots**

The pg\_replication\_slots view provides a listing of all replication slots that currently exist on the database cluster, along with their current state.

For more on replication slots, see Section 27.2.6 and Chapter 49.

### **Table 52.82. pg\_replication\_slots Columns**

#### **Column Type**

#### **Description**

slot\_name name

A unique, cluster-wide identifier for the replication slot

plugin name

The base name of the shared object containing the output plugin this logical slot is using, or null for physical slots.

slot\_type text

The slot type: physical or logical

datoid oid (references [pg\\_database](#page-13-0).oid)

The OID of the database this slot is associated with, or null. Only logical slots have an associated database.

database name (references [pg\\_database](#page-13-0).datname)

The name of the database this slot is associated with, or null. Only logical slots have an associated database.

temporary bool

True if this is a temporary replication slot. Temporary slots are not saved to disk and are automatically dropped on error or when the session has finished.

active bool

True if this slot is currently actively being used

active\_pid int4

The process ID of the session using this slot if the slot is currently actively being used. NULL if inactive.

#### xmin xid

The oldest transaction that this slot needs the database to retain. VACUUM cannot remove tuples deleted by any later transaction.

#### catalog\_xmin xid

The oldest transaction affecting the system catalogs that this slot needs the database to retain. VACUUM cannot remove catalog tuples deleted by any later transaction.

#### restart\_lsn pg\_lsn

The address (LSN) of oldest WAL which still might be required by the consumer of this slot and thus won't be automatically removed during checkpoints unless this LSN gets behind more than max\_slot\_wal\_keep\_size from the current LSN. NULL if the LSN of this slot has never been reserved.

#### confirmed\_flush\_lsn pg\_lsn

The address (LSN) up to which the logical slot's consumer has confirmed receiving data. Data older than this is not available anymore. NULL for physical slots.

#### wal\_status text

Availability of WAL files claimed by this slot. Possible values are:

- reserved means that the claimed files are within max\_wal\_size.
- extended means that max\_wal\_size is exceeded but the files are still retained, either by the replication slot or by wal\_keep\_size.
- unreserved means that the slot no longer retains the required WAL files and some of them are to be removed at the next checkpoint. This state can return to reserved or extended.
- lost means that some required WAL files have been removed and this slot is no longer usable.

The last two states are seen only when max\_slot\_wal\_keep\_size is non-negative.

#### safe\_wal\_size int8

The number of bytes that can be written to WAL such that this slot is not in danger of getting in state "lost". It is NULL for lost slots, as well as if max\_slot\_wal\_keep\_size is -1.

#### two\_phase bool

True if the slot is enabled for decoding prepared transactions. Always false for physical slots.

# <span id="page-62-0"></span>**52.82. pg\_roles**

The view pg\_roles provides access to information about database roles. This is simply a publicly readable view of [pg\\_authid](#page-5-0) that blanks out the password field.

### **Table 52.83. pg\_roles Columns**

### **Column Type Description**

rolname name

Role name

rolsuper bool

Role has superuser privileges

rolinherit bool

#### **Description**

Role automatically inherits privileges of roles it is a member of

rolcreaterole bool

Role can create more roles

rolcreatedb bool

Role can create databases

rolcanlogin bool

Role can log in. That is, this role can be given as the initial session authorization identifier

rolreplication bool

Role is a replication role. A replication role can initiate replication connections and create and drop replication slots.

rolconnlimit int4

For roles that can log in, this sets maximum number of concurrent connections this role can make. -1 means no limit.

rolpassword text

Not the password (always reads as \*\*\*\*\*\*\*\*)

rolvaliduntil timestamptz

Password expiry time (only used for password authentication); null if no expiration

rolbypassrls bool

Role bypasses every row-level security policy, see Section 5.8 for more information.

rolconfig text[]

Role-specific defaults for run-time configuration variables

oid oid (references [pg\\_authid](#page-5-0).oid)

ID of role

# <span id="page-63-1"></span>**52.83. pg\_rules**

The view pg\_rules provides access to useful information about query rewrite rules.

### **Table 52.84. pg\_rules Columns**

#### **Column Type**

#### **Description**

schemaname name (references [pg\\_namespace](#page-25-0).nspname)

Name of schema containing table

tablename name (references [pg\\_class](#page-8-0).relname)

Name of table the rule is for

rulename name (references [pg\\_rewrite](#page-33-0).rulename)

Name of rule

definition text

Rule definition (a reconstructed creation command)

The pg\_rules view excludes the ON SELECT rules of views and materialized views; those can be seen in [pg\\_views](#page-74-1) and [pg\\_matviews](#page-58-0).

# <span id="page-63-0"></span>**52.84. pg\_seclabels**

The view pg\_seclabels provides information about security labels. It as an easier-to-query version of the [pg\\_seclabel](#page-34-1) catalog.

### **Table 52.85. pg\_seclabels Columns**

### **Column Type Description** objoid oid (references any OID column) The OID of the object this security label pertains to classoid oid (references [pg\\_class](#page-8-0).oid) The OID of the system catalog this object appears in objsubid int4 For a security label on a table column, this is the column number (the objoid and classoid refer to the table itself). For all other object types, this column is zero. objtype text The type of object to which this label applies, as text. objnamespace oid (references [pg\\_namespace](#page-25-0).oid) The OID of the namespace for this object, if applicable; otherwise NULL. objname text

The name of the object to which this label applies, as text.

provider text (references [pg\\_seclabel](#page-34-1).provider)

The label provider associated with this label.

label text (references [pg\\_seclabel](#page-34-1).label)

The security label applied to this object.

# <span id="page-64-0"></span>**52.85. pg\_sequences**

The view pg\_sequences provides access to useful information about each sequence in the database.

### **Table 52.86. pg\_sequences Columns**

## **Column Type Description** schemaname name (references [pg\\_namespace](#page-25-0).nspname) Name of schema containing sequence sequencename name (references [pg\\_class](#page-8-0).relname) Name of sequence sequenceowner name (references [pg\\_authid](#page-5-0).rolname) Name of sequence's owner data\_type regtype (references [pg\\_type](#page-45-0).oid) Data type of the sequence start\_value int8 Start value of the sequence min\_value int8 Minimum value of the sequence max\_value int8 Maximum value of the sequence increment\_by int8 Increment value of the sequence cycle bool Whether the sequence cycles cache\_size int8 Cache size of the sequence last\_value int8

#### **Description**

The last sequence value written to disk. If caching is used, this value can be greater than the last value handed out from the sequence. Null if the sequence has not been read from yet. Also, if the current user does not have USAGE or SELECT privilege on the sequence, the value is null.

# <span id="page-65-0"></span>**52.86. pg\_settings**

The view pg\_settings provides access to run-time parameters of the server. It is essentially an alternative interface to the SHOW and SET commands. It also provides access to some facts about each parameter that are not directly available from SHOW, such as minimum and maximum values.

### **Table 52.87. pg\_settings Columns**

### **Column Type Description**

name text

Run-time configuration parameter name

setting text

Current value of the parameter

unit text

Implicit unit of the parameter

category text

Logical group of the parameter

short\_desc text

A brief description of the parameter

extra\_desc text

Additional, more detailed, description of the parameter

context text

Context required to set the parameter's value (see below)

vartype text

Parameter type (bool, enum, integer, real, or string)

source text

Source of the current parameter value

min\_val text

Minimum allowed value of the parameter (null for non-numeric values)

max\_val text

Maximum allowed value of the parameter (null for non-numeric values)

enumvals text[]

Allowed values of an enum parameter (null for non-enum values)

boot\_val text

Parameter value assumed at server startup if the parameter is not otherwise set

reset\_val text

Value that RESET would reset the parameter to in the current session

sourcefile text

Configuration file the current value was set in (null for values set from sources other than configuration files, or when examined by a user who is neither a superuser or a member of pg\_read\_all\_settings); helpful when using include directives in configuration files

sourceline int4

Line number within the configuration file the current value was set at (null for values set from sources other than configuration files, or when examined by a user who is neither a superuser or a member of pg\_read\_all\_settings).

pending\_restart bool

true if the value has been changed in the configuration file but needs a restart; or false otherwise.

There are several possible values of context. In order of decreasing difficulty of changing the setting, they are:

internal

These settings cannot be changed directly; they reflect internally determined values. Some of them may be adjustable by rebuilding the server with different configuration options, or by changing options supplied to initdb.

postmaster

These settings can only be applied when the server starts, so any change requires restarting the server. Values for these settings are typically stored in the postgresql.conf file, or passed on the command line when starting the server. Of course, settings with any of the lower context types can also be set at server start time.

sighup

Changes to these settings can be made in postgresql.conf without restarting the server. Send a SIGHUP signal to the postmaster to cause it to re-read postgresql.conf and apply the changes. The postmaster will also forward the SIGHUP signal to its child processes so that they all pick up the new value.

superuser-backend

Changes to these settings can be made in postgresql.conf without restarting the server. They can also be set for a particular session in the connection request packet (for example, via libpq's PGOPTIONS environment variable), but only if the connecting user is a superuser. However, these settings never change in a session after it is started. If you change them in postgresql.conf, send a SIGHUP signal to the postmaster to cause it to re-read postgresql.conf. The new values will only affect subsequently-launched sessions.

backend

Changes to these settings can be made in postgresql.conf without restarting the server. They can also be set for a particular session in the connection request packet (for example, via libpq's PGOPTIONS environment variable); any user can make such a change for their session. However, these settings never change in a session after it is started. If you change them in postgresql.conf, send a SIGHUP signal to the postmaster to cause it to re-read postgresql.conf. The new values will only affect subsequently-launched sessions.

superuser

These settings can be set from postgresql.conf, or within a session via the SET command; but only superusers can change them via SET. Changes in postgresql.conf will affect existing sessions only if no session-local value has been established with SET.

user

These settings can be set from postgresql.conf, or within a session via the SET command. Any user is allowed to change their session-local value. Changes in postgresql.conf will affect existing sessions only if no session-local value has been established with SET.

See Section 20.1 for more information about the various ways to change these parameters.

This view does not display customized options until the extension module that defines them has been loaded.

This view cannot be inserted into or deleted from, but it can be updated. An UPDATE applied to a row of pg\_settings is equivalent to executing the SET command on that named parameter. The change only affects the value used by the current session. If an UPDATE is issued within a transaction that is later aborted, the effects of the UPDATE command disappear when the transaction is rolled back. Once the surrounding transaction is committed, the effects will persist until the end of the session, unless overridden by another UPDATE or SET.

# <span id="page-67-0"></span>**52.87. pg\_shadow**

The view pg\_shadow exists for backwards compatibility: it emulates a catalog that existed in PostgreSQL before version 8.1. It shows properties of all roles that are marked as rolcanlogin in [pg\\_authid](#page-5-0).

The name stems from the fact that this table should not be readable by the public since it contains passwords. [pg\\_user](#page-73-1) is a publicly readable view on pg\_shadow that blanks out the password field.

### **Table 52.88. pg\_shadow Columns**

#### **Column Type Description**

usename name (references [pg\\_authid](#page-5-0).rolname)

User name

usesysid oid (references [pg\\_authid](#page-5-0).oid)

ID of this user

usecreatedb bool

User can create databases

usesuper bool

User is a superuser

userepl bool

User can initiate streaming replication and put the system in and out of backup mode.

usebypassrls bool

User bypasses every row-level security policy, see Section 5.8 for more information.

passwd text

Encrypted password; null if none. See [pg\\_authid](#page-5-0) for details of how encrypted passwords are stored.

valuntil timestamptz

Password expiry time (only used for password authentication)

useconfig text[]

Session defaults for run-time configuration variables

# <span id="page-67-1"></span>**52.88. pg\_shmem\_allocations**

The pg\_shmem\_allocations view shows allocations made from the server's main shared memory segment. This includes both memory allocated by postgres itself and memory allocated by extensions using the mechanisms detailed in Section 38.10.10.

Note that this view does not include memory allocated using the dynamic shared memory infrastructure.

### **Table 52.89. pg\_shmem\_allocations Columns**

#### **Column Type**

#### **Description**

name text

The name of the shared memory allocation. NULL for unused memory and <anonymous> for anonymous allocations.

off int8

The offset at which the allocation starts. NULL for anonymous allocations, since details related to them are not known.

size int8

Size of the allocation

allocated\_size int8

Size of the allocation including padding. For anonymous allocations, no information about padding is available, so the size and allocated\_size columns will always be equal. Padding is not meaningful for free memory, so the columns will be equal in that case also.

Anonymous allocations are allocations that have been made with ShmemAlloc() directly, rather than via ShmemInitStruct() or ShmemInitHash().

By default, the pg\_shmem\_allocations view can be read only by superusers.

# <span id="page-68-0"></span>**52.89. pg\_stats**

The view pg\_stats provides access to the information stored in the [pg\\_statistic](#page-37-0) catalog. This view allows access only to rows of [pg\\_statistic](#page-37-0) that correspond to tables the user has permission to read, and therefore it is safe to allow public read access to this view.

pg\_stats is also designed to present the information in a more readable format than the underlying catalog — at the cost that its schema must be extended whenever new slot types are defined for [pg\\_statistic](#page-37-0).

### **Table 52.90. pg\_stats Columns**

#### **Column Type**

#### **Description**

schemaname name (references [pg\\_namespace](#page-25-0).nspname)

Name of schema containing table

tablename name (references [pg\\_class](#page-8-0).relname)

Name of table

attname name (references [pg\\_attribute](#page-3-0).attname)

Name of column described by this row

inherited bool

If true, this row includes inheritance child columns, not just the values in the specified table

null\_frac float4

Fraction of column entries that are null

avg\_width int4

Average width in bytes of column's entries

n\_distinct float4

If greater than zero, the estimated number of distinct values in the column. If less than zero, the negative of the number of distinct values divided by the number of rows. (The

negated form is used when ANALYZE believes that the number of distinct values is likely to increase as the table grows; the positive form is used when the column seems to have a fixed number of possible values.) For example, -1 indicates a unique column in which the number of distinct values is the same as the number of rows.

most\_common\_vals anyarray

A list of the most common values in the column. (Null if no values seem to be more common than any others.)

most\_common\_freqs float4[]

A list of the frequencies of the most common values, i.e., number of occurrences of each divided by total number of rows. (Null when most\_common\_vals is.)

histogram\_bounds anyarray

A list of values that divide the column's values into groups of approximately equal population. The values in most\_common\_vals, if present, are omitted from this histogram calculation. (This column is null if the column data type does not have a < operator or if the most\_common\_vals list accounts for the entire population.)

correlation float4

Statistical correlation between physical row ordering and logical ordering of the column values. This ranges from -1 to +1. When the value is near -1 or +1, an index scan on the column will be estimated to be cheaper than when it is near zero, due to reduction of random access to the disk. (This column is null if the column data type does not have a < operator.)

most\_common\_elems anyarray

A list of non-null element values most often appearing within values of the column. (Null for scalar types.)

most\_common\_elem\_freqs float4[]

A list of the frequencies of the most common element values, i.e., the fraction of rows containing at least one instance of the given value. Two or three additional values follow the per-element frequencies; these are the minimum and maximum of the preceding per-element frequencies, and optionally the frequency of null elements. (Null when most\_common\_elems is.)

elem\_count\_histogram float4[]

A histogram of the counts of distinct non-null element values within the values of the column, followed by the average number of distinct non-null elements. (Null for scalar types.)

The maximum number of entries in the array fields can be controlled on a column-by-column basis using the ALTER TABLE SET STATISTICS command, or globally by setting the default\_statistics\_target run-time parameter.

# <span id="page-69-0"></span>**52.90. pg\_stats\_ext**

The view pg\_stats\_ext provides access to information about each extended statistics object in the database, combining information stored in the [pg\\_statistic\\_ext](#page-38-0) and [pg\\_statistic\\_ex](#page-39-0)[t\\_data](#page-39-0) catalogs. This view allows access only to rows of [pg\\_statistic\\_ext](#page-38-0) and [pg\\_sta](#page-39-0)[tistic\\_ext\\_data](#page-39-0) that correspond to tables the user owns, and therefore it is safe to allow public read access to this view.

pg\_stats\_ext is also designed to present the information in a more readable format than the underlying catalogs — at the cost that its schema must be extended whenever new types of extended statistics are added to [pg\\_statistic\\_ext](#page-38-0).

### **Table 52.91. pg\_stats\_ext Columns**

#### **Column Type Description**

schemaname name (references [pg\\_namespace](#page-25-0).nspname)

Name of schema containing table

tablename name (references [pg\\_class](#page-8-0).relname)

Name of table

statistics\_schemaname name (references [pg\\_namespace](#page-25-0).nspname)

Name of schema containing extended statistics object

statistics\_name name (references [pg\\_statistic\\_ext](#page-38-0).stxname)

Name of extended statistics object

statistics\_owner name (references [pg\\_authid](#page-5-0).rolname)

Owner of the extended statistics object

attnames name[] (references [pg\\_attribute](#page-3-0).attname)

Names of the columns included in the extended statistics object

exprs text[]

Expressions included in the extended statistics object

kinds char[]

Types of extended statistics object enabled for this record

n\_distinct pg\_ndistinct

N-distinct counts for combinations of column values. If greater than zero, the estimated number of distinct values in the combination. If less than zero, the negative of the number of distinct values divided by the number of rows. (The negated form is used when ANALYZE believes that the number of distinct values is likely to increase as the table grows; the positive form is used when the column seems to have a fixed number of possible values.) For example, -1 indicates a unique combination of columns in which the number of distinct combinations is the same as the number of rows.

dependencies pg\_dependencies

Functional dependency statistics

most\_common\_vals text[]

A list of the most common combinations of values in the columns. (Null if no combinations seem to be more common than any others.)

most\_common\_val\_nulls bool[]

A list of NULL flags for the most common combinations of values. (Null when most\_common\_vals is.)

most\_common\_freqs float8[]

A list of the frequencies of the most common combinations, i.e., number of occurrences of each divided by total number of rows. (Null when most\_common\_vals is.)

most\_common\_base\_freqs float8[]

A list of the base frequencies of the most common combinations, i.e., product of per-value frequencies. (Null when most\_common\_vals is.)

The maximum number of entries in the array fields can be controlled on a column-by-column basis using the ALTER TABLE SET STATISTICS command, or globally by setting the default\_statistics\_target run-time parameter.

# <span id="page-70-0"></span>**52.91. pg\_stats\_ext\_exprs**

The view pg\_stats\_ext\_exprs provides access to information about all expressions included in extended statistics objects, combining information stored in the [pg\\_statistic\\_ext](#page-38-0) and [pg\\_s](#page-39-0)[tatistic\\_ext\\_data](#page-39-0) catalogs. This view allows access only to rows of [pg\\_statistic\\_ext](#page-38-0) and [pg\\_statistic\\_ext\\_data](#page-39-0) that correspond to tables the user owns, and therefore it is safe to allow public read access to this view.

pg\_stats\_ext\_exprs is also designed to present the information in a more readable format than the underlying catalogs — at the cost that its schema must be extended whenever the structure of statistics in pg\_statistic\_ext changes.

### **Table 52.92. pg\_stats\_ext\_exprs Columns**

### **Column Type**

**Description**

schemaname name (references [pg\\_namespace](#page-25-0).nspname)

Name of schema containing table

tablename name (references [pg\\_class](#page-8-0).relname)

Name of table the statistics object is defined on

statistics\_schemaname name (references [pg\\_namespace](#page-25-0).nspname)

Name of schema containing extended statistics object

statistics\_name name (references [pg\\_statistic\\_ext](#page-38-0).stxname)

Name of extended statistics object

statistics\_owner name (references [pg\\_authid](#page-5-0).rolname)

Owner of the extended statistics object

expr text

Expression included in the extended statistics object

null\_frac float4

Fraction of expression entries that are null

avg\_width int4

Average width in bytes of expression's entries

n\_distinct float4

If greater than zero, the estimated number of distinct values in the expression. If less than zero, the negative of the number of distinct values divided by the number of rows. (The negated form is used when ANALYZE believes that the number of distinct values is likely to increase as the table grows; the positive form is used when the expression seems to have a fixed number of possible values.) For example, -1 indicates a unique expression in which the number of distinct values is the same as the number of rows.

most\_common\_vals anyarray

A list of the most common values in the expression. (Null if no values seem to be more common than any others.)

most\_common\_freqs float4[]

A list of the frequencies of the most common values, i.e., number of occurrences of each divided by total number of rows. (Null when most\_common\_vals is.)

histogram\_bounds anyarray

A list of values that divide the expression's values into groups of approximately equal population. The values in most\_common\_vals, if present, are omitted from this histogram calculation. (This expression is null if the expression data type does not have a < operator or if the most\_common\_vals list accounts for the entire population.)

correlation float4

Statistical correlation between physical row ordering and logical ordering of the expression values. This ranges from -1 to +1. When the value is near -1 or +1, an index scan on the expression will be estimated to be cheaper than when it is near zero, due to reduction of random access to the disk. (This expression is null if the expression's data type does not have a < operator.)

most\_common\_elems anyarray

A list of non-null element values most often appearing within values of the expression. (Null for scalar types.)

most\_common\_elem\_freqs float4[]

A list of the frequencies of the most common element values, i.e., the fraction of rows containing at least one instance of the given value. Two or three additional values follow the per-element frequencies; these are the minimum and maximum of the preceding per-element frequencies, and optionally the frequency of null elements. (Null when most\_common\_elems is.)

elem\_count\_histogram float4[]

A histogram of the counts of distinct non-null element values within the values of the expression, followed by the average number of distinct non-null elements. (Null for scalar types.)

The maximum number of entries in the array fields can be controlled on a column-by-column basis using the ALTER TABLE SET STATISTICS command, or globally by setting the default\_statistics\_target run-time parameter.

# <span id="page-72-0"></span>**52.92. pg\_tables**

The view pg\_tables provides access to useful information about each table in the database.

### **Table 52.93. pg\_tables Columns**

## **Column Type Description** schemaname name (references [pg\\_namespace](#page-25-0).nspname) Name of schema containing table tablename name (references [pg\\_class](#page-8-0).relname) Name of table tableowner name (references [pg\\_authid](#page-5-0).rolname) Name of table's owner tablespace name (references [pg\\_tablespace](#page-41-0).spcname) Name of tablespace containing table (null if default for database) hasindexes bool (references [pg\\_class](#page-8-0).relhasindex) True if table has (or recently had) any indexes hasrules bool (references [pg\\_class](#page-8-0).relhasrules) True if table has (or once had) rules hastriggers bool (references [pg\\_class](#page-8-0).relhastriggers) True if table has (or once had) triggers rowsecurity bool (references [pg\\_class](#page-8-0).relrowsecurity) True if row security is enabled on the table

# <span id="page-72-1"></span>**52.93. pg\_timezone\_abbrevs**

The view pg\_timezone\_abbrevs provides a list of time zone abbreviations that are currently recognized by the datetime input routines. The contents of this view change when the timezone\_abbreviations run-time parameter is modified.

### **Table 52.94. pg\_timezone\_abbrevs Columns**

## **Column Type Description** abbrev text Time zone abbreviation utc\_offset interval Offset from UTC (positive means east of Greenwich) is\_dst bool True if this is a daylight-savings abbreviation

While most timezone abbreviations represent fixed offsets from UTC, there are some that have historically varied in value (see Section B.4 for more information). In such cases this view presents their current meaning.

# <span id="page-73-0"></span>**52.94. pg\_timezone\_names**

The view pg\_timezone\_names provides a list of time zone names that are recognized by SET TIMEZONE, along with their associated abbreviations, UTC offsets, and daylight-savings status. (Technically, PostgreSQL does not use UTC because leap seconds are not handled.) Unlike the abbreviations shown in [pg\\_timezone\\_abbrevs](#page-72-1), many of these names imply a set of daylight-savings transition date rules. Therefore, the associated information changes across local DST boundaries. The displayed information is computed based on the current value of CURRENT\_TIMESTAMP.

### **Table 52.95. pg\_timezone\_names Columns**

| Column Type<br>Description                                                |
|---------------------------------------------------------------------------|
| name text<br>Time zone name                                               |
| abbrev text<br>Time zone abbreviation                                     |
| utc_offset interval<br>Offset from UTC (positive means east of Greenwich) |
| is_dst bool<br>True if currently observing daylight savings               |

# <span id="page-73-1"></span>**52.95. pg\_user**

The view pg\_user provides access to information about database users. This is simply a publicly readable view of [pg\\_shadow](#page-67-0) that blanks out the password field.

### **Table 52.96. pg\_user Columns**

| Column Type<br>Description      |  |
|---------------------------------|--|
| usename name<br>User name       |  |
| usesysid oid<br>ID of this user |  |
| usecreatedb bool                |  |

User can create databases

usesuper bool

User is a superuser

userepl bool

User can initiate streaming replication and put the system in and out of backup mode.

usebypassrls bool

User bypasses every row-level security policy, see Section 5.8 for more information.

passwd text

Not the password (always reads as \*\*\*\*\*\*\*\*)

valuntil timestamptz

Password expiry time (only used for password authentication)

useconfig text[]

Session defaults for run-time configuration variables

# <span id="page-74-0"></span>**52.96. pg\_user\_mappings**

The view pg\_user\_mappings provides access to information about user mappings. This is essentially a publicly readable view of [pg\\_user\\_mapping](#page-49-1) that leaves out the options field if the user has no rights to use it.

### **Table 52.97. pg\_user\_mappings Columns**

### **Column Type Description** umid oid (references [pg\\_user\\_mapping](#page-49-1).oid) OID of the user mapping srvid oid (references [pg\\_foreign\\_server](#page-20-0).oid) The OID of the foreign server that contains this mapping srvname name (references [pg\\_foreign\\_server](#page-20-0).srvname) Name of the foreign server umuser oid (references [pg\\_authid](#page-5-0).oid) OID of the local role being mapped, or zero if the user mapping is public usename name Name of the local user to be mapped umoptions text[] User mapping specific options, as "keyword=value" strings

To protect password information stored as a user mapping option, the umoptions column will read as null unless one of the following applies:

- current user is the user being mapped, and owns the server or holds USAGE privilege on it
- current user is the server owner and mapping is for PUBLIC
- current user is a superuser

# <span id="page-74-1"></span>**52.97. pg\_views**

The view pg\_views provides access to useful information about each view in the database.

### **Table 52.98. pg\_views Columns**

### **Column Type Description**

schemaname name (references [pg\\_namespace](#page-25-0).nspname)

Name of schema containing view

viewname name (references [pg\\_class](#page-8-0).relname)

Name of view

viewowner name (references [pg\\_authid](#page-5-0).rolname)

Name of view's owner

definition text

View definition (a reconstructed SELECT query)