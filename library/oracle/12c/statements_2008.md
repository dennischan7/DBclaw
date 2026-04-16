# Oracle 12c - statements_2008
Source: https://docs.oracle.com/database/121/SQLRF/statements_2008.htm

Prerequisites

You must be connected to a CDB.

To specify the `pdb_unplug_clause`, the current container must be the root, you must be authenticated `AS` `SYSDBA` or `AS` `SYSOPER`, and the `SYSDBA` or `SYSOPER` privilege must be either granted to you commonly, or granted to you locally in the root and locally in the PDB you want to unplug.

To specify the `pdb_settings_clauses`, the current container must be the PDB whose settings you want to modify and you must have the `ALTER` `DATABASE` privilege, either granted commonly or granted locally in the PDB. To specify the `pdb_logging_clauses` or the `RENAME` `GLOBAL_NAME` clause, you must also have the `RESTRICTED` `SESSION` privilege, either granted commonly or granted locally in the PDB being renamed, and the PDB must be in `READ` `WRITE` `RESTRICTED` mode.

To specify the `pdb_datafile_clause`, the current container must be the PDB whose datafiles you want to bring online or take offline and you must have the `ALTER` `DATABASE` privilege, either granted commonly or granted locally in the PDB.

To specify the `pdb_recovery_clauses`, the current container must be the PDB you want to back up or recover and you must have the `ALTER` `DATABASE` privilege, either granted commonly or granted locally in the PDB.

To specify the `pdb_change_state` clause, the current container must be the PDB whose state you want to change and you must be authenticated `AS` `SYSBACKUP`, `AS` `SYSDBA`, `AS` `SYSDG`, or `AS` `SYSOPER`.

To specify the `pdb_change_state_from_root` clause, the current container must be the root, you must be authenticated `AS` `SYSBACKUP`, `AS` `SYSDBA`, `AS` `SYSDG`, or `AS` `SYSOPER`, and the `SYSBACKUP`, `SYSDBA`, `SYSDG`, or `SYSOPER` privilege must be either granted to you commonly, or granted to you locally in the root and locally in the PDB(s) whose state(s) you want to change.

Semantics

pdb\_unplug\_clause

This clause lets you unplug a PDB from a CDB. When you unplug a PDB, Oracle stores metadata for the PDB in an XML file. You can use this XML file to subsequently plug the PDB into a CDB.

* For `pdb_name`, specify the name of the PDB you want to unplug. The PDB must be closed—that is, the open mode must be `MOUNTED`. In an Oracle Real Application Clusters (Oracle RAC) environment, the PDB must be closed in all Oracle RAC instances.
* For `filename`, specify the full path name of the XML file in which to store the metadata for the unplugged PDB.

After a PDB is unplugged, it remains in the CDB with an open mode of `MOUNTED` and a status of `UNPLUGGED`. The only operation you can perform on an unplugged PDB is `DROP` `PLUGGABLE` `DATABASE`, which will remove it from the CDB. You must drop the PDB before you can plug it into the same CDB or another CDB.

pdb\_settings\_clauses

These clauses lets you modify various settings for a PDB.

pdb\_name

You can optionally use `pdb_name` to specify the name of the PDB whose settings you want to modify.

DEFAULT EDITION Clause

Use this clause to designate the specified edition as the default edition for the PDB. For the full semantics of this clause, refer to ["DEFAULT EDITION Clause"](statements_1006.md#BABEADGC) in the `ALTER` `DATABASE` documentation.

SET DEFAULT TABLESPACE Clause

Use this clause to specify or change the default type of tablespaces subsequently created in the PDB. For the full semantics of this clause, refer to ["SET DEFAULT TABLESPACE Clause"](statements_1006.md#BGBDJGGH) in the `ALTER` `DATABASE` documentation.

DEFAULT TABLESPACE Clause

Use this clause to establish or change the default permanent tablespace of the PDB. For the full semantics of this clause, refer to ["DEFAULT TABLESPACE Clause"](statements_1006.md#BGBIJBIC) in the `ALTER` `DATABASE` documentation.

DEFAULT TEMPORARY TABLESPACE Clause

Use this clause to change the default temporary tablespace of the PDB to a new tablespace or tablespace group. For the full semantics of this clause, refer to ["DEFAULT TEMPORARY TABLESPACE Clause"](statements_1006.md#BGBEIJJD) in the `ALTER` `DATABASE` documentation.

RENAME GLOBAL\_NAME TO Clause

Use this clause to change the global name of the PDB. The new global name must be unique within the CDB. For an Oracle Real Application Clusters (Oracle RAC) database, the PDB must be open in `READ` `WRITE` `RESTRICTED` mode on the current instance only. The PDB must be closed on all other instances. For the full semantics of this clause, refer to ["RENAME GLOBAL\_NAME Clause"](statements_1006.md#i2141769) in the `ALTER` `DATABASE` documentation.

Note:

When you change the global name of a PDB, be sure to change the

`PLUGGABLE` `DATABASE`

property for database services that are used to connect to the PDB.

set\_time\_zone\_clauses

Use this clause to modify the time zone setting for the PDB. For the full semantics of this clause, refer to [set\_time\_zone\_clause](statements_1006.md#i2197908) in the `ALTER` `DATABASE` documentation.

database\_file\_clauses

Use this clause to modify data files and temp files for the PDB. For the full semantics of this clause, refer to [database\_file\_clauses](statements_1006.md#i2078824) in the `ALTER` `DATABASE` documentation.

supplemental\_db\_logging

Use these clauses to instruct Oracle Database to add or stop adding supplemental data into the log stream for the PDB. The `ADD` `SUPPLEMENTAL` `LOG` clause has the side effect of instructing the database to add minimal supplemental data into the log stream for the entire CDB. For the full semantics of this clause, refer to [supplemental\_db\_logging](statements_1006.md#i2153841) in the `ALTER` `DATABASE` documentation.

pdb\_storage\_clause

Use this clause to modify the storage limits for a PDB.

This clause has the same semantics as the [pdb\_storage\_clause](statements_6010.md#CACJAAGI) in the `CREATE` `PLUGGABLE` `DATABASE` documentation, with the following additions:

* If you specify `MAXSIZE` `size_clause`, then the value you specify for `size_clause` must be greater than or equal to the combined size of the existing tablespaces belonging to the PDB. Otherwise, an error occurs.
* If you specify `MAX_SHARED_TEMP_SIZE` `size_clause`, and the value you specify for `size_clause` is less than that used by sessions that are connected to the PDB, then no additional storage in the shared temporary tablespace will be available for sessions connected to the PDB until the amount of storage used by them becomes smaller than the value you specify for `size_clause`.

pdb\_logging\_clauses

Use these clauses to set or change the logging characteristics of the PDB.

logging\_clause

Use this clause to change the default logging attribute for tablespaces subsequently created within the PDB. This clause has the same semantics as the [logging\_clause](statements_6010.md#CACJIEBE) in the `CREATE` `PLUGGABLE` `DATABASE` documentation.

pdb\_force\_logging\_clause

Use this clause to place a PDB into force logging or force nologging mode or take a PDB out of force logging or force nologging mode.

Force logging mode instructs the database to log all changes in the PDB, except changes in temporary tablespaces and temporary segments. Force nologging mode instructs the database to not log any changes in the PDB.

CDB-wide force logging mode takes precedence over PDB-level force nologging mode. PDB-level force logging mode and force nologging mode take precedence over and are independent of any `LOGGING`, `NOLOGGING`, or `FORCE` `LOGGING` settings you specify for individual tablespaces in the PDB and any `LOGGING` or `NOLOGGING` settings you specify for individual database objects in the PDB.

* Specify `ENABLE` `FORCE` `LOGGING` to place the PDB in force logging mode. If the PDB is currently in force nologging mode, then specifying this clause results in an error. You must first specify `DISABLE` `FORCE` `NOLOGGING`.
* Specify `DISABLE` `FORCE` `LOGGING` to take the PDB out of force logging mode. If the PDB is not currently in force logging mode, then specifying this clause results in an error.
* Specify `ENABLE` `FORCE` `NOLOGGING` to place the PDB in force nologging mode. If the PDB is currently in force logging mode, then specifying this clause results in an error. You must first specify `DISABLE` `FORCE` `LOGGING`.
* Specify `DISABLE` `FORCE` `NOLOGGING` to take the PDB out of force nologging mode. If the PDB is not currently in force nologging mode, then specifying this clause results in an error.

This clause does not change the default `LOGGING` or `NOLOGGING` mode of the PDB specified by the [logging\_clause](#BGBDDAGI).

pdb\_datafile\_clause

This clause lets you bring data files associated with a PDB online or take them offline. The PDB must be closed when you issue this clause.

* For `pdb_name`, specify the name of the PDB. If the current container is the PDB, then you can omit `pdb_name`.
* The `DATAFILE` clauses let you specify the data files you want to bring online or take offline. Use `filename` or `filenumber` to identify specific data files by name or by number. You can view data file names and numbers by querying the `NAME` and `FILE#` columns of the `V$DATAFILE` dynamic performance view. Use `ALL` to specify all datafiles associated with the PDB.
* Specify `ONLINE` to bring the data files online or `OFFLINE` to take the data files offline.

pdb\_recovery\_clauses

Use the `pdb_recovery_clauses` to back up and recover a PDB.

pdb\_name

You can optionally use `pdb_name` to specify the name of the PDB you want to back up or recover.

pdb\_general\_recovery

This clause lets you control media recovery for the PDB or standby database or for specified tablespaces or files. The `pdb_general_recovery` clause has the same semantics as the `general_recovery` clause of `ALTER` `DATABASE`. Refer to the [general\_recovery](statements_1006.md#i2208874) clause of `ALTER` `DATABASE` for more information.

BACKUP Clauses

Use these clauses to move all of the data files in the PDB into or out of online backup mode (also called hot backup mode). These clauses have the same semantics in `ALTER` `PLUGGABLE` `DATABASE` and `ALTER` `DATABASE`. Refer to the ["BACKUP Clauses"](statements_1006.md#i2150230) of `ALTER` `DATABASE` for more information.

RECOVERY Clauses

Use these clauses to enable or disable a PDB for recovery. The PDB must be closed—that is, the open mode must be `MOUNTED`. The `RECOVERY` clauses are available starting with Oracle Database 12c Release 1 (12.1.0.2).

* Specify `ENABLE` `RECOVERY` to bring all data files that belong to a PDB online and enable the PDB for recovery.
* Specify `DISABLE` `RECOVERY` to take all data files that belong to a PDB offline and disable the PDB for recovery.

pdb\_change\_state

This clause enables you to change the state, or open mode, of a PDB. [Table 11-1](#CCHJEFGC) lists the open modes of a PDB.

* Specify the `pdb_open` clause to change the open mode to `READ` `WRITE`, `READ` `ONLY`, or `MIGRATE`.
* Specify the `pdb_close` clause to change the open mode to `MOUNTED`.

Table 11-1 PDB Open Modes

| Open Mode | Description |
| --- | --- |
| `READ` `WRITE` | A PDB in open read/write mode allows queries and user transactions to proceed and allows users to generate redo logs. |
| `READ` `ONLY` | A PDB in open read-only mode allows queries but does not allow user changes. |
| `MIGRATE` | When a PDB is in open migrate mode, you can run database upgrade scripts on the PDB. |
| `MOUNTED` | When a PDB is in mounted mode, it behaves like a non-CDB in mounted mode. It does not allow changes to any objects, and it is accessible only to database administrators. It cannot read from or write to data files. Information about the PDB is removed from memory caches. Cold backups of the PDB are possible. |

You can view the open mode of a PDB by querying the `OPEN_MODE` column of the `V$PDBS` view.

pdb\_name

You can optionally use `pdb_name` to specify the name of the PDB whose open mode you want to change.

pdb\_open

This clause lets you change the open mode of a PDB to `READ` `WRITE`, `READ` `ONLY`, or `MIGRATE`. When you specify this clause, the PDB must be in `MOUNTED` mode unless you specify the `FORCE` keyword.

If you do not specify `READ` `WRITE` or `READ` `ONLY`, then the default is `READ` `WRITE`. The exception is when the PDB belongs to a CDB that is used as a physical standby database, in which case the default is `READ` `ONLY`.

READ WRITE Specify this clause to change the open mode to `READ` `WRITE`.

READ ONLY Specify this clause to change the open mode to `READ` `ONLY`.

[READ WRITE] UPGRADE Specify this clause to change the open mode to `MIGRATE`. The `READ` `WRITE` keywords are optional and are provided for semantic clarity.

RESTRICTED If you specify the optional `RESTRICTED` keyword, then the PDB is accessible only to users with the `RESTRICTED` `SESSION` privilege in the PDB.

If the PDB is in `READ` `WRITE` or `READ` `ONLY` mode, and you specify the `RESTRICTED` and `FORCE` keywords while changing the open mode, then all sessions connected to the PDB that do not have the `RESTRICTED` `SESSION` privilege in the PDB are terminated, and their transactions are rolled back.

FORCE Specify this keyword to change the open mode of a PDB from `READ` `WRITE` to `READ` `ONLY`, or from `READ` `ONLY` to `READ` `WRITE`. The `FORCE` keyword allows users to remain connected to the PDB while the open mode is changed.

When you specify `FORCE` to change the open mode of a PDB from `READ` `WRITE` to `READ` `ONLY`, any `READ` `WRITE` transaction that is open when you change the open mode will not be allowed to perform any more DML operations or to `COMMIT`.

Restriction on FORCE You cannot specify the `FORCE` keyword if the PDB is currently in `MIGRATE` mode, and you cannot specify the `FORCE` keyword to change a currently open PDB to `MIGRATE` mode.

RESETLOGS Specify this clause to create a new PDB incarnation and open the PDB in `READ` `WRITE` mode after point-in-time recovery of the PDB.

instances\_clause In an Oracle Real Application Clusters environment, use this clause to modify the state of the PDB in the specified Oracle RAC instances. If you omit this clause, then the state of the PDB is modified only in the current instance.

* Use `instance_name` to specify one or more instance names, in a comma-separated list enclosed in parenthesis. This modifies the state of the PDB only in those instances.
* Specify `ALL` to modify the state of the PDB in all instances.
* Specify `ALL` `EXCEPT` to modify the state of the PDB in all instances except the specified instances.

If the PDB is already open in one or more instances, then you can open it in additional instances, but it must be opened in the same mode as in the instances in which it is already open.

pdb\_close

This clause lets you change the open mode of a PDB to `MOUNTED`. When you specify this clause, the PDB must be in `READ` `WRITE`, `READ` `ONLY`, or `MIGRATE` mode. This clause is the PDB equivalent of the SQL\*Plus `SHUTDOWN` command.

IMMEDIATE If you specify the optional `IMMEDIATE` keyword, then this clause is the PDB equivalent of the SQL\*Plus `SHUTDOWN` command with the immediate mode. Otherwise, the PDB is shut down with the normal mode.

instances\_clause In an Oracle Real Application Clusters environment, use this clause to modify the state of the PDB in the specified Oracle RAC instances. You can close a PDB in some instances and leave it open in others. Refer to the [instances\_clause](#CCHDCJCE) for the full semantics of this clause.

relocate\_clause In an Oracle Real Application Clusters environment, use this clause to instruct the database to reopen the PDB on a different Oracle RAC instance.

* Specify `RELOCATE` to reopen the PDB on a different instance that is selected by Oracle Database.
* Specify `RELOCATE` `TO` `'``instance_name``'` to reopen the PDB in the specified instance.
* Specify `NORELOCATE` to close the PDB in the current instance. This is the default.

pdb\_save\_or\_discard\_state

Use this clause to instruct the database to save or discard the open mode of the PDB when the CDB restarts.

* If you specify `SAVE`, then the PDB's open mode after the CDB restarts will be identical to its open mode just before the CDB restarted.
* If you specify `DISCARD`, then the PDB's open mode after the CDB restarts will be `MOUNTED`. This is the default.

instances\_clause In an Oracle Real Application Clusters environment, use this clause to instruct the database to save or discard the open mode of the PDB in the specified Oracle RAC instances. If you omit this clause, then the database applies the `SAVE` or `DISCARD` setting only to the PDB in the current instance.

* Use `instance_name` to specify one or more instance names, in a comma-separated list enclosed in parenthesis. This applies the `SAVE` or `DISCARD` setting to the PDB only in those instances.
* Specify `ALL` to apply the `SAVE` or `DISCARD` setting to the PDB in all instances.
* Specify `ALL` `EXCEPT` to apply the `SAVE` or `DISCARD` setting to the PDB in all instances except the specified instances.

pdb\_change\_state\_from\_root

This clause enables you to modify the state of one or more PDBs.

* Specify the `pdb_name` for one or more PDBs whose state you want to modify.
* Specify `ALL` to modify the state of all PDBs in the CDB.
* Specify `ALL` `EXCEPT` to modify the state of all PDBs in the CDB except those specified by using `pdb_name`.

If a PDB is already in the specified state, then the PDB's state is unchanged and no error is returned. If the state of a PDB cannot be changed, then an error occurs only for that PDB.

Refer to [pdb\_open](#BGBBCHJH) and [pdb\_close](#CCHFFJDB) for the full semantics of these clauses.

Examples

Unplugging a PDB from a CDB: Example The following statement unplugs PDB `pdb1` and stores metadata for the PDB into XML file `/oracle/data/pdb1.xml`:

```
ALTER PLUGGABLE DATABASE pdb1
  UNPLUG INTO '/oracle/data/pdb1.xml';
```

Modifying the Settings of a PDB: Example The following statement changes the limit for the amount of storage used by all tablespaces in PDB `pdb2` to 500M:

```
ALTER PLUGGABLE DATABASE pdb2
  STORAGE (MAXSIZE 500M);
```

Taking the Data Files of a PDB Offline: Example The following statement takes the data files associated with PDB `pdb3` offline:

```
ALTER PLUGGABLE DATABASE pdb3
  DATAFILE ALL OFFLINE;
```

Changing the State of a PDB: Examples Assume that PDB `pdb4` is closed—that is, its open mode is `MOUNTED`. The following statement opens `pdb4` with open mode `READ` `ONLY`:

```
ALTER PLUGGABLE DATABASE pdb4
  OPEN READ ONLY;
```

The following statement uses the `FORCE` keyword to change the open mode of `pdb4` from `READ` `ONLY` to `READ` `WRITE`:

```
ALTER PLUGGABLE DATABASE pdb4
  OPEN READ WRITE FORCE;
```

The following statement closes PDB `pdb4`:

```
ALTER PLUGGABLE DATABASE pdb4
  CLOSE;
```

The following statement opens PDB pdb4 with open mode `READ` `ONLY`. Because the `RESTRICTED` keyword is specified, the PDB is accessible only to users with the `RESTRICTED` `SESSION` privilege in the PDB.

```
ALTER PLUGGABLE DATABASE pdb4
  OPEN READ ONLY RESTRICTED;
```

Assume that PDB `pdb5` is closed—that is, its open mode is `MOUNTED`. In an Oracle Real Application Clusters environment, the following statement opens PDB `pdb5` with open mode `READ` `WRITE` in instances `ORCLDB_1` and `ORCLDB_2`:

```
ALTER PLUGGABLE DATABASE pdb5
  OPEN READ WRITE INSTANCES = ('ORCLDB_1', 'ORCLDB_2');
```

In an Oracle Real Application Clusters environment, the following statement closes PDB `pdb6` in the current instance and instructs the database to reopen `pdb6` in instance `ORCLDB_3`:

```
ALTER PLUGGABLE DATABASE pdb6
  CLOSE RELOCATE TO 'ORCLDB_3';
```

Changing the State of All PDBs in a CDB: Example Assume that the current container is the root. The following statement opens all PDBs in the CDB with open mode `READ` `ONLY`:

```
ALTER PLUGGABLE DATABASE ALL
  OPEN READ ONLY;
```