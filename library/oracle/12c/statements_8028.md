# Oracle 12c - statements_8028
Source: https://docs.oracle.com/database/121/SQLRF/statements_8028.htm

# DROP PLUGGABLE DATABASE

Purpose

Use the `DROP` `PLUGGABLE` `DATABASE` statement to drop a pluggable database (PDB).

When you drop a PDB, the control file of the multitenant container database (CDB) is modified to remove all references to the dropped PDB and its data files. Archived logs and backups associated with the dropped PDB are not deleted. You can delete them using Oracle Recovery Manager (RMAN), or you can retain them in case you subsequently want to perform point-in-time recovery of the PDB.

Caution:

You cannot roll back a

`DROP` `PLUGGABLE` `DATABASE`

statement.

Prerequisites

You must be connected to a CDB.

The current container must be the root, you must be authenticated `AS` `SYSDBA` or `AS` `SYSOPER`, and the `SYSDBA` or `SYSOPER` privilege must be either granted to you commonly, or granted to you locally in the root and locally in PDB you want to drop.

To specify `KEEP` `DATAFILES` (the default), the PDB you want to drop must be unplugged.

To specify `INCLUDING` `DATAFILES`, the PDB you want to drop must be in mounted mode or it must be unplugged.

Semantics

pdb\_name

Specify the name of the PDB you want to drop. You cannot drop the seed (`PDB$SEED`).

KEEP DATAFILES

Specify `KEEP` `DATAFILES` to retain the data files associated with the PDB after the PDB is dropped. The temp file for the PDB is deleted because it is no longer needed. This is the default.

Keeping data files may be useful in scenarios where a PDB that is unplugged from one CDB is plugged into another CDB, with both CDBs sharing storage devices.

INCLUDING DATAFILES

Specify `INCLUDING` `DATAFILES` to delete the data files associated with the PDB being dropped. The temp file for the PDB is also deleted.

Restriction on Dropping SNAPSHOT COPY PDBs If a PDB was created with the `SNAPSHOT` `COPY` clause, then you must specify `INCLUDING` `DATAFILES` when you drop the PDB.

Examples

Dropping a PDB: Example The following statement drops the PDB `pdb1` and its associated data files:

```
DROP PLUGGABLE DATABASE pdb1
  INCLUDING DATAFILES;
```