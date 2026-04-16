---
source: PostgreSQL 15 Reference
title: 00_Overview
---

PostgreSQL has the ability to report the progress of certain commands during command execution. Currently, the only commands which support progress reporting are ANALYZE, CLUSTER, CREATE INDEX, VACUUM, COPY, and BASE\_BACKUP (i.e., replication command that pg\_basebackup issues to take a base backup). This may be expanded in the future.

# <span id="page-44-0"></span>**28.4.1. ANALYZE Progress Reporting**

Whenever ANALYZE is running, the pg\_stat\_progress\_analyze view will contain a row for each backend that is currently running that command. The tables below describe the information that will be reported and provide information about how to interpret it.

### **Table 28.36. pg\_stat\_progress\_analyze View**

| Column Type<br>Description                                                                                                                          |
|-----------------------------------------------------------------------------------------------------------------------------------------------------|
| pid integer<br>Process ID of backend.                                                                                                               |
| datid oid<br>OID of the database to which this backend is connected.                                                                                |
| datname name<br>Name of the database to which this backend is connected.                                                                            |
| relid oid<br>OID of the table being analyzed.                                                                                                       |
| phase text<br>Current processing phase. See Table 28.37.                                                                                            |
| sample_blks_total bigint<br>Total number of heap blocks that will be sampled.                                                                       |
| sample_blks_scanned bigint<br>Number of heap blocks scanned.                                                                                        |
| ext_stats_total bigint<br>Number of extended statistics.                                                                                            |
| ext_stats_computed bigint<br>Number of extended statistics computed. This counter only advances when the phase is<br>computing extended statistics. |
| child_tables_total bigint<br>Number of child tables.                                                                                                |
| child_tables_done bigint<br>Number of child tables scanned. This counter only advances when the phase is ac<br>quiring inherited sample rows.       |
| current_child_table_relid oid                                                                                                                       |

### **Column Type Description**

OID of the child table currently being scanned. This field is only valid when the phase is acquiring inherited sample rows.

<span id="page-45-1"></span>**Table 28.37. ANALYZE Phases**

| Phase                              | Description                                                                                                                                                                                                    |
|------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| initializing                       | The command is preparing to begin scanning the heap. This<br>phase is expected to be very brief.                                                                                                               |
| acquiring sample rows              | The command is currently scanning the table given by relid to<br>obtain sample rows.                                                                                                                           |
| acquiring inherited<br>sample rows | The command is currently scanning child tables to obtain sam<br>ple rows. Columns child_tables_total, child_ta<br>bles_done, and current_child_table_relid contain<br>the progress information for this phase. |
| computing statistics               | The command is computing statistics from the sample rows ob<br>tained during the table scan.                                                                                                                   |
| computing extended<br>statistics   | The command is computing extended statistics from the sample<br>rows obtained during the table scan.                                                                                                           |
| finalizing analyze                 | The command is updating pg_class. When this phase is com<br>pleted, ANALYZE will end.                                                                                                                          |

## **Note**

Note that when ANALYZE is run on a partitioned table, all of its partitions are also recursively analyzed. In that case, ANALYZE progress is reported first for the parent table, whereby its inheritance statistics are collected, followed by that for each partition.

# <span id="page-45-0"></span>**28.4.2. CREATE INDEX Progress Reporting**

Whenever CREATE INDEX or REINDEX is running, the pg\_stat\_progress\_create\_index view will contain one row for each backend that is currently creating indexes. The tables below describe the information that will be reported and provide information about how to interpret it.

**Table 28.38. pg\_stat\_progress\_create\_index View**

| Column Type<br>Description                                                                                          |
|---------------------------------------------------------------------------------------------------------------------|
| pid integer<br>Process ID of backend.                                                                               |
| datid oid<br>OID of the database to which this backend is connected.                                                |
| datname name<br>Name of the database to which this backend is connected.                                            |
| relid oid<br>OID of the table on which the index is being created.                                                  |
| index_relid oid<br>OID of the index being created or reindexed. During a non-concurrent CREATE INDEX,<br>this is 0. |
| command text                                                                                                        |

#### **Description**

The command that is running: CREATE INDEX, CREATE INDEX CONCURRENTLY, REINDEX, or REINDEX CONCURRENTLY.

phase text

Current processing phase of index creation. See [Table 28.39](#page-46-0).

lockers\_total bigint

Total number of lockers to wait for, when applicable.

lockers\_done bigint

Number of lockers already waited for.

current\_locker\_pid bigint

Process ID of the locker currently being waited for.

blocks\_total bigint

Total number of blocks to be processed in the current phase.

blocks\_done bigint

Number of blocks already processed in the current phase.

tuples\_total bigint

Total number of tuples to be processed in the current phase.

tuples\_done bigint

Number of tuples already processed in the current phase.

partitions\_total bigint

When creating an index on a partitioned table, this column is set to the total number of partitions on which the index is to be created. This field is 0 during a REINDEX.

partitions\_done bigint

When creating an index on a partitioned table, this column is set to the number of partitions on which the index has been created. This field is 0 during a REINDEX.

### <span id="page-46-0"></span>**Table 28.39. CREATE INDEX Phases**

| Phase                                    | Description                                                                                                                                                                                                                                                                                                                                         |
|------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| initializing                             | CREATE INDEX or REINDEX is preparing to create the index.<br>This phase is expected to be very brief.                                                                                                                                                                                                                                               |
| waiting for writers<br>before build      | CREATE INDEX CONCURRENTLY or REINDEX CONCUR<br>RENTLY is waiting for transactions with write locks that can po<br>tentially see the table to finish. This phase is skipped when not<br>in concurrent mode. Columns lockers_total, locker<br>s_done and current_locker_pid contain the progress in<br>formation for this phase.                      |
| building index                           | The index is being built by the access method-specific code. In<br>this phase, access methods that support progress reporting fill in<br>their own progress data, and the subphase is indicated in this col<br>umn. Typically, blocks_total and blocks_done will con<br>tain progress data, as well as potentially tuples_total and<br>tuples_done. |
| waiting for writers<br>before validation | CREATE INDEX CONCURRENTLY or REINDEX CONCUR<br>RENTLY is waiting for transactions with write locks that can po<br>tentially write into the table to finish. This phase is skipped when<br>not in concurrent mode. Columns lockers_total, locker<br>s_done and current_locker_pid contain the progress in<br>formation for this phase.               |
| index validation:<br>scanning index      | CREATE INDEX CONCURRENTLY is scanning the index<br>searching for tuples that need to be validated. This phase is                                                                                                                                                                                                                                    |

| Phase                                      | Description                                                                                                                                                                                                                                                                                                                   |
|--------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|                                            | skipped when not in concurrent mode. Columns blocks_to<br>tal (set to the total size of the index) and blocks_done con<br>tain the progress information for this phase.                                                                                                                                                       |
| index validation:<br>sorting tuples        | CREATE INDEX CONCURRENTLY is sorting the output of the<br>index scanning phase.                                                                                                                                                                                                                                               |
| index validation:<br>scanning table        | CREATE INDEX CONCURRENTLY is scanning the table to<br>validate the index tuples collected in the previous two phases.<br>This phase is skipped when not in concurrent mode. Columns<br>blocks_total (set to the total size of the table) and block<br>s_done contain the progress information for this phase.                 |
| waiting for old snap<br>shots              | CREATE INDEX CONCURRENTLY or REINDEX CONCUR<br>RENTLY is waiting for transactions that can potentially see the<br>table to release their snapshots. This phase is skipped when not<br>in concurrent mode. Columns lockers_total, locker<br>s_done and current_locker_pid contain the progress in<br>formation for this phase. |
| waiting for readers<br>before marking dead | REINDEX CONCURRENTLY is waiting for transactions with<br>read locks on the table to finish, before marking the old in<br>dex dead. This phase is skipped when not in concurrent mode.<br>Columns lockers_total, lockers_done and curren<br>t_locker_pid contain the progress information for this phase.                      |
| waiting for readers<br>before dropping     | REINDEX CONCURRENTLY is waiting for transactions with<br>read locks on the table to finish, before dropping the old index.<br>This phase is skipped when not in concurrent mode. Columns<br>lockers_total, lockers_done and current_lock<br>er_pid contain the progress information for this phase.                           |

## <span id="page-47-0"></span>**28.4.3. VACUUM Progress Reporting**

Whenever VACUUM is running, the pg\_stat\_progress\_vacuum view will contain one row for each backend (including autovacuum worker processes) that is currently vacuuming. The tables below describe the information that will be reported and provide information about how to interpret it. Progress for VACUUM FULL commands is reported via pg\_stat\_progress\_cluster because both VACUUM FULL and CLUSTER rewrite the table, while regular VACUUM only modifies it in place. See [Section 28.4.4.](#page-49-0)

**Table 28.40. pg\_stat\_progress\_vacuum View**

| Column Type<br>Description                                               |
|--------------------------------------------------------------------------|
| pid integer<br>Process ID of backend.                                    |
| datid oid<br>OID of the database to which this backend is connected.     |
| datname name<br>Name of the database to which this backend is connected. |
| relid oid<br>OID of the table being vacuumed.                            |
| phase text<br>Current processing phase of vacuum. See Table 28.41.       |
| heap_blks_total bigint                                                   |

### **Column Type Description**

Total number of heap blocks in the table. This number is reported as of the beginning of the scan; blocks added later will not be (and need not be) visited by this VACUUM.

#### heap\_blks\_scanned bigint

Number of heap blocks scanned. Because the visibility map is used to optimize scans, some blocks will be skipped without inspection; skipped blocks are included in this total, so that this number will eventually become equal to heap\_blks\_total when the vacuum is complete. This counter only advances when the phase is scanning heap.

#### heap\_blks\_vacuumed bigint

Number of heap blocks vacuumed. Unless the table has no indexes, this counter only advances when the phase is vacuuming heap. Blocks that contain no dead tuples are skipped, so the counter may sometimes skip forward in large increments.

index\_vacuum\_count bigint

Number of completed index vacuum cycles.

max\_dead\_tuples bigint

Number of dead tuples that we can store before needing to perform an index vacuum cycle, based on maintenance\_work\_mem.

num\_dead\_tuples bigint

Number of dead tuples collected since the last index vacuum cycle.

### <span id="page-48-0"></span>**Table 28.41. VACUUM Phases**

| Phase                       | Description                                                                                                                                                                                                                                                                                                                                                                   |
|-----------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| initializing                | VACUUM is preparing to begin scanning the heap. This phase is<br>expected to be very brief.                                                                                                                                                                                                                                                                                   |
| scanning heap               | VACUUM is currently scanning the heap. It will prune and defrag<br>ment each page if required, and possibly perform freezing activi<br>ty. The heap_blks_scanned column can be used to monitor<br>the progress of the scan.                                                                                                                                                   |
| vacuuming indexes           | VACUUM is currently vacuuming the indexes. If a table has any<br>indexes, this will happen at least once per vacuum, after the heap<br>has been completely scanned. It may happen multiple times per<br>vacuum if maintenance_work_mem (or, in the case of autovac<br>uum, autovacuum_work_mem if set) is insufficient to store the<br>number of dead tuples found.           |
| vacuuming heap              | VACUUM is currently vacuuming the heap. Vacuuming the heap<br>is distinct from scanning the heap, and occurs after each instance<br>of vacuuming indexes. If heap_blks_scanned is less than<br>heap_blks_total, the system will return to scanning the<br>heap after this phase is completed; otherwise, it will begin clean<br>ing up indexes after this phase is completed. |
| cleaning up indexes         | VACUUM is currently cleaning up indexes. This occurs after the<br>heap has been completely scanned and all vacuuming of the in<br>dexes and the heap has been completed.                                                                                                                                                                                                      |
| truncating heap             | VACUUM is currently truncating the heap so as to return empty<br>pages at the end of the relation to the operating system. This oc<br>curs after cleaning up indexes.                                                                                                                                                                                                         |
| performing final<br>cleanup | VACUUM is performing final cleanup. During this phase, VACUUM<br>will vacuum the free space map, update statistics in pg_class,<br>and report statistics to the cumulative statistics system. When this<br>phase is completed, VACUUM will end.                                                                                                                               |

## <span id="page-49-0"></span>**28.4.4. CLUSTER Progress Reporting**

Whenever CLUSTER or VACUUM FULL is running, the pg\_stat\_progress\_cluster view will contain a row for each backend that is currently running either command. The tables below describe the information that will be reported and provide information about how to interpret it.

**Table 28.42. pg\_stat\_progress\_cluster View**

### **Column Type Description**

pid integer

Process ID of backend.

datid oid

OID of the database to which this backend is connected.

datname name

Name of the database to which this backend is connected.

relid oid

OID of the table being clustered.

command text

The command that is running. Either CLUSTER or VACUUM FULL.

phase text

Current processing phase. See [Table 28.43](#page-49-1).

cluster\_index\_relid oid

If the table is being scanned using an index, this is the OID of the index being used; otherwise, it is zero.

heap\_tuples\_scanned bigint

Number of heap tuples scanned. This counter only advances when the phase is seq scanning heap, index scanning heap or writing new heap.

heap\_tuples\_written bigint

Number of heap tuples written. This counter only advances when the phase is seq scanning heap, index scanning heap or writing new heap.

heap\_blks\_total bigint

Total number of heap blocks in the table. This number is reported as of the beginning of seq scanning heap.

heap\_blks\_scanned bigint

Number of heap blocks scanned. This counter only advances when the phase is seq scanning heap.

index\_rebuild\_count bigint

Number of indexes rebuilt. This counter only advances when the phase is rebuilding index.

<span id="page-49-1"></span>**Table 28.43. CLUSTER and VACUUM FULL Phases**

| Phase               | Description                                                                                      |
|---------------------|--------------------------------------------------------------------------------------------------|
| initializing        | The command is preparing to begin scanning the heap. This<br>phase is expected to be very brief. |
| seq scanning heap   | The command is currently scanning the table using a sequential<br>scan.                          |
| index scanning heap | CLUSTER is currently scanning the table using an index scan.                                     |
| sorting tuples      | CLUSTER is currently sorting tuples.                                                             |
| writing new heap    | CLUSTER is currently writing the new heap.                                                       |

| Phase                       | Description                                                                                                |
|-----------------------------|------------------------------------------------------------------------------------------------------------|
| swapping relation<br>files  | The command is currently swapping newly-built files into place.                                            |
| rebuilding index            | The command is currently rebuilding an index.                                                              |
| performing final<br>cleanup | The command is performing final cleanup. When this phase is<br>completed, CLUSTER or VACUUM FULL will end. |

# <span id="page-50-0"></span>**28.4.5. Base Backup Progress Reporting**

Whenever an application like pg\_basebackup is taking a base backup, the pg\_stat\_progress\_basebackup view will contain a row for each WAL sender process that is currently running the BASE\_BACKUP replication command and streaming the backup. The tables below describe the information that will be reported and provide information about how to interpret it.

**Table 28.44. pg\_stat\_progress\_basebackup View**

| Column Type<br>Description                               |  |
|----------------------------------------------------------|--|
| pid integer<br>Process ID of a WAL sender process.       |  |
| phase text<br>Current processing phase. See Table 28.45. |  |
|                                                          |  |

backup\_total bigint

Total amount of data that will be streamed. This is estimated and reported as of the beginning of streaming database files phase. Note that this is only an approximation since the database may change during streaming database files phase and WAL log may be included in the backup later. This is always the same value as backup\_streamed once the amount of data streamed exceeds the estimated total size. If the estimation is disabled in pg\_basebackup (i.e., --no-estimate-size option is specified), this is NULL.

backup\_streamed bigint

Amount of data streamed. This counter only advances when the phase is streaming database files or transferring wal files.

tablespaces\_total bigint

Total number of tablespaces that will be streamed.

tablespaces\_streamed bigint

Number of tablespaces streamed. This counter only advances when the phase is streaming database files.

<span id="page-50-1"></span>**Table 28.45. Base Backup Phases**

| Phase                                | Description                                                                                                                                                       |
|--------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| initializing                         | The WAL sender process is preparing to begin the backup. This<br>phase is expected to be very brief.                                                              |
| waiting for check<br>point to finish | The WAL sender process is currently performing pg_back<br>up_start to prepare to take a base backup, and waiting for the<br>start-of-backup checkpoint to finish. |
| estimating backup                    | The WAL sender process is currently estimating the total amount                                                                                                   |
| size                                 | of database files that will be streamed as a base backup.                                                                                                         |
| streaming database                   | The WAL sender process is currently streaming database files as                                                                                                   |
| files                                | a base backup.                                                                                                                                                    |
| waiting for wal                      | The WAL sender process is currently performing pg_back                                                                                                            |
| archiving to finish                  | up_stop to finish the backup, and waiting for all the WAL files                                                                                                   |

| Phase                     | Description                                                                                                                                                                                                                                                                   |
|---------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|                           | required for the base backup to be successfully archived. If either<br>wal-method=none orwal-method=stream is spec<br>ified in pg_basebackup, the backup will end when this phase is<br>completed.                                                                            |
| transferring wal<br>files | The WAL sender process is currently transferring all WAL logs<br>generated during the backup. This phase occurs after wait<br>ing for wal archiving to finish phase ifwal<br>method=fetch is specified in pg_basebackup. The backup will<br>end when this phase is completed. |

# <span id="page-51-0"></span>**28.4.6. COPY Progress Reporting**

Whenever COPY is running, the pg\_stat\_progress\_copy view will contain one row for each backend that is currently running a COPY command. The table below describes the information that will be reported and provides information about how to interpret it.

**Table 28.46. pg\_stat\_progress\_copy View**

| Column Type<br>Description                                                                                                                                                                                                             |
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| pid integer<br>Process ID of backend.                                                                                                                                                                                                  |
| datid oid<br>OID of the database to which this backend is connected.                                                                                                                                                                   |
| datname name<br>Name of the database to which this backend is connected.                                                                                                                                                               |
| relid oid<br>OID of the table on which the COPY command is executed. It is set to 0 if copying from<br>a SELECT query.                                                                                                                 |
| command text<br>The command that is running: COPY FROM, or COPY TO.                                                                                                                                                                    |
| type text<br>The io type that the data is read from or written to: FILE, PROGRAM, PIPE (for COPY<br>FROM STDIN and COPY TO STDOUT), or CALLBACK (used for example during the<br>initial table synchronization in logical replication). |
| bytes_processed bigint<br>Number of bytes already processed by COPY command.                                                                                                                                                           |
| bytes_total bigint<br>Size of source file for COPY FROM command in bytes. It is set to 0 if not available.                                                                                                                             |
| tuples_processed bigint<br>Number of tuples already processed by COPY command.                                                                                                                                                         |
| tuples_excluded bigint<br>Number of tuples not processed because they were excluded by the WHERE clause of the<br>COPY command.                                                                                                        |