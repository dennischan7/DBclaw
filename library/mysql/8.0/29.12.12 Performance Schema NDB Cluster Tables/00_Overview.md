---
source: MySQL 8.0 Reference
title: 00_Overview
---

The following table shows all Performance Schema tables relating to the NDBCLUSTER storage engine.

**Table 29.3 Performance Schema NDB Tables**

| Table Name                | Description                              |
|---------------------------|------------------------------------------|
| ndb_sync_excluded_objects | NDB objects which cannot be synchronized |
| ndb_sync_pending_objects  | NDB objects waiting for synchronization  |

Beginning with NDB 8.0.16, automatic synchronization in NDB attempts to detect and synchronize automatically all mismatches in metadata between the NDB Cluster's internal dictionary and the MySQL Server's datadictionary. This is done by default in the background at regular intervals as determined by the ndb\_metadata\_check\_interval system variable, unless disabled using ndb\_metadata\_check or overridden by setting ndb\_metadata\_sync. Prior to NDB 8.0.21, the only information readily accessible to users about this process was in the form of logging messages and object counts available (beginning with NDB 8.0.18) as the status variables Ndb\_metadata\_detected\_count, Ndb\_metadata\_synced\_count, and Ndb\_metadata\_excluded\_count (prior to NDB 8.0.22, this variable was named

Ndb\_metadata\_blacklist\_size). Beginning with NDB 8.0.21, more detailed information about the current state of automatic synchronization is exposed by a MySQL server acting as an SQL node in an NDB Cluster in these two Performance Schema tables:

- [ndb\\_sync\\_pending\\_objects](#page-31-1): Displays information about NDB database objects for which mismatches have been detected between the NDB dictionary and the MySQL data dictionary. When attempting to synchronize such objects, NDB removes the object from the queue awaiting synchronization, and from this table, and tries to reconcile the mismatch. If synchronization of the object fails due to a temporary error, it is picked up and added back to the queue (and to this table) the next time NDB performs mismatch detection; if the attempts fails due a permanent error, the object is added to the [ndb\\_sync\\_excluded\\_objects](#page-31-0) table.
- [ndb\\_sync\\_excluded\\_objects](#page-31-0): Shows information about NDB database objects for which automatic synchronization has failed due to permanent errors resulting from mismatches which cannot be reconciled without manual intervention; these objects are blocklisted and not considered again for mismatch detection until this has been done.

The [ndb\\_sync\\_pending\\_objects](#page-31-1) and [ndb\\_sync\\_excluded\\_objects](#page-31-0) tables are present only if MySQL has support enabled for the NDBCLUSTER storage engine.

These tables are described in more detail in the following two sections.

## <span id="page-31-1"></span>**29.12.12.1 The ndb\_sync\_pending\_objects Table**

This table provides information about NDB database objects for which mismatches have been detected and which are waiting to be synchronized between the NDB dictionary and the MySQL data dictionary.

Example information about NDB database objects awaiting synchronization:

```
mysql> SELECT * FROM performance_schema.ndb_sync_pending_objects;
+-------------+------+----------------+
| SCHEMA_NAME | NAME | TYPE |
+-------------+------+----------------+
| NULL | lg1 | LOGFILE GROUP |
| NULL | ts1 | TABLESPACE |
| db1 | NULL | SCHEMA |
| test | t1 | TABLE |
| test | t2 | TABLE |
| test | t3 | TABLE |
+-------------+------+----------------+
```

The [ndb\\_sync\\_pending\\_objects](#page-31-1) table has these columns:

- SCHEMA\_NAME: The name of the schema (database) in which the object awaiting synchronization resides; this is NULL for tablespaces and log file groups
- NAME: The name of the object awaiting synchronization; this is NULL if the object is a schema
- TYPE: The type of the object awaiting synchronization; this is one of LOGFILE GROUP, TABLESPACE, SCHEMA, or TABLE

The [ndb\\_sync\\_pending\\_objects](#page-31-1) table was added in NDB 8.0.21.

## <span id="page-31-0"></span>**29.12.12.2 The ndb\_sync\_excluded\_objects Table**

This table provides information about NDB database objects which cannot be automatically synchronized between NDB Cluster's dictionary and the MySQL data dictionary.

Example information about NDB database objects which cannot be synchronized with the MySQL data dictionary:

```
mysql> SELECT * FROM performance_schema.ndb_sync_excluded_objects\G
```

```
**************************************
SCHEMA NAME: NULL
     NAME: lg1
   TYPE: LOGFILE GROUP
   REASON: Injected failure
              ******** 2. row **************
SCHEMA NAME: NULL
     NAME: ts1
     TYPE: TABLESPACE
    REASON: Injected failure
                ****** 3. row *************
SCHEMA NAME: db1
    NAME: NULL
     TYPE · SCHEMA
   REASON: Injected failure
                 ***** 4. row **************
SCHEMA NAME: test
     NAME: +1
     TYPE: TABLE
   REASON: Injected failure
                ****** 5. row **************
SCHEMA NAME: test
     NAME: t2
     TYPE: TABLE
   REASON: Injected failure
                ****** 6. row ***************
SCHEMA NAME: test
     NAME: t3
     TYPE: TABLE
    REASON: Injected failure
```

The ndb sync excluded objects table has these columns:

- SCHEMA\_NAME: The name of the schema (database) in which the object which has failed to synchronize resides; this is NULL for tablespaces and log file groups
- NAME: The name of the object which has failed to synchronize; this is NULL if the object is a schema
- TYPE: The type of the object has failed to synchronize; this is one of LOGFILE GROUP, TABLESPACE, SCHEMA, or TABLE
- REASON: The reason for exclusion (blocklisting) of the object; that is, the reason for the failure to synchronize this object

Possible reasons include the following:

- Injected failure
- Failed to determine if object existed in NDB
- Failed to determine if object existed in DD
- Failed to drop object in DD
- Failed to get undofiles assigned to logfile group
- Failed to get object id and version
- Failed to install object in DD
- Failed to get datafiles assigned to tablespace
- Failed to create schema
- Failed to determine if object was a local table
- Failed to invalidate table references

- Failed to set database name of NDB object
- Failed to get extra metadata of table
- Failed to migrate table with extra metadata version 1
- Failed to get object from DD
- Definition of table has changed in NDB Dictionary
- Failed to setup binlogging for table

This list is not necessarily exhaustive, and is subject to change in future NDB releases.

The [ndb\\_sync\\_excluded\\_objects](#page-31-0) table was added in NDB 8.0.21.