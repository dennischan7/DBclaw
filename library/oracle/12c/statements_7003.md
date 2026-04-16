# Oracle 12c - statements_7003
Source: https://docs.oracle.com/database/121/SQLRF/statements_7003.htm

Semantics

BIGFILE | SMALLFILE

Use this clause to determine whether the tablespace is a bigfile or smallfile tablespace. This clause overrides any default tablespace type setting for the database.

* A bigfile tablespace contains only one data file or temp file, which can contain up to approximately 4 billion (232) blocks. The minimum size of the single data file or temp file is 12 megabytes (MB) for a tablespace with 32K blocks and 7MB for a tablespace with 8K blocks. The maximum size of the single data file or temp file is 128 terabytes (TB) for a tablespace with 32K blocks and 32TB for a tablespace with 8K blocks.
* A smallfile tablespace is a traditional Oracle tablespace, which can contain 1022 data files or temp files, each of which can contain up to approximately 4 million (222) blocks.

If you omit this clause, then Oracle Database uses the current default tablespace type of permanent or temporary tablespace set for the database. If you specify `BIGFILE` for a permanent tablespace, then the database by default creates a locally managed tablespace with automatic segment-space management.

Restriction on Bigfile Tablespaces You can specify only one data file in the `DATAFILE` clause or one temp file in the `TEMPFILE` clause.

permanent\_tablespace\_clause

Use the following clauses to create a permanent tablespace. (Some of these clauses are also used to create a temporary or undo tablespace.)

tablespace

Specify the name of the tablespace to be created. The name must satisfy the requirements listed in ["Database Object Naming Rules"](sql_elements008.md#i27570).

Note on the SYSAUX Tablespace 

`SYSAUX` is a required auxiliary system tablespace. You must use the `CREATE` `TABLESPACE` statement to create the `SYSAUX` tablespace if you are upgrading from a release earlier than Oracle Database 11g. You must have the `SYSDBA` system privilege to specify this clause, and you must have opened the database in `UPGRADE` mode.

You must specify `EXTENT` `MANAGEMENT` `LOCAL` and `SEGMENT` `SPACE` `MANAGEMENT` `AUTO` for the `SYSAUX` tablespace. The `DATAFILE` clause is optional only if you have enabled Oracle Managed Files. See ["DATAFILE | TEMPFILE Clause"](#i2171920) for the behavior of the `DATAFILE` clause.

Take care to allocate sufficient space for the `SYSAUX` tablespace. For guidelines on creating this tablespace, refer to [Oracle Database Upgrade Guide](../UPGRD/upgrade.md#UPGRD003).

Restrictions on the SYSAUX Tablespace You cannot specify `OFFLINE` or `TEMPORARY` for the `SYSAUX` tablespace.

DATAFILE | TEMPFILE Clause

Specify the data files to make up the permanent tablespace or the temp files to make up the temporary tablespace. Use the `datafile_tempfile_spec` form of `file_specification` to create regular data files and temp files in an operating system file system or to create Oracle Automatic Storage Management (Oracle ASM) disk group files.

You must specify the `DATAFILE` or `TEMPFILE` clause unless you have enabled Oracle Managed Files by setting a value for the `DB_CREATE_FILE_DEST` initialization parameter. For Oracle ASM disk group files, the parameter must be set to a multiple file creation form of Oracle ASM filenames. If this parameter is set, then the database creates a system-named 100 MB file in the default file destination specified in the parameter. The file has `AUTOEXTEND` enabled and an unlimited maximum size.

Note:

Media recovery does not recognize temp files.

Notes on Specifying Data Files and Temp Files 

* You can create a tablespace within an Oracle ASM disk group by providing only the disk group name in the `datafile_tempfile_spec`. In this case, Oracle ASM creates a data file in the specified disk group with a system-generated filename. The data file is auto-extensible with an unlimited maximum size and a default size of 100 MB. You can use the `autoextend_clause` to override the default size.
* If you use one of the reference forms of the `ASM_filename`, which refers to an existing file, then you must also specify `REUSE`.

Note:

On some operating systems, Oracle does not allocate space for a temp file until the temp file blocks are actually accessed. This delay in space allocation results in faster creation and resizing of temp files, but it requires that sufficient disk space is available when the temp files are later used. To avoid potential problems, before you create or resize a temp file, ensure that the available disk space exceeds the size of the new temp file or the increased size of a resized temp file. The excess space should allow for anticipated increases in disk space use by unrelated operations as well. Then proceed with the creation or resizing operation.

MINIMUM EXTENT Clause

This clause is valid only for a dictionary-managed tablespace. Specify the minimum size of an extent in the tablespace. This clause lets you control free space fragmentation in the tablespace by ensuring that the size of every used or free extent in a tablespace is at least as large as, and is a multiple of, the value specified in the `size_clause`.

BLOCKSIZE Clause

Use the `BLOCKSIZE` clause to specify a nonstandard block size for the tablespace. In order to specify this clause, the `DB_CACHE_SIZE` and at least one `DB_``n``K_CACHE_SIZE` parameter must be set, and the integer you specify in this clause must correspond with the setting of one `DB_``n``K_CACHE_SIZE` parameter setting.

Restriction on BLOCKSIZE You cannot specify nonstandard block sizes for a temporary tablespace or if you intend to assign this tablespace as the temporary tablespace for any users.

Note:

Oracle recommend that you do not store tablespaces with a 2K block size on 4K sector size disks, because performance degradation can result.

logging\_clause

Specify the default logging attributes of all tables, indexes, materialized views, materialized view logs, and partitions within the tablespace. This clause is not valid for a temporary or undo tablespace.

If you omit this clause, then the default is `LOGGING`. The exception is creating a tablespace in a PDB. In this case, if you omit this clause, then the tablespace uses the logging attribute of the PDB. Refer to the [logging\_clause](statements_6010.md#CACJIEBE) of `CREATE` `PLUGGABLE` `DATABASE` for more information.

The tablespace-level logging attribute can be overridden by logging specifications at the table, index, materialized view, materialized view log, and partition levels.

FORCE LOGGING

Use this clause to put the tablespace into `FORCE` `LOGGING` mode. Oracle Database will log all changes to all objects in the tablespace except changes to temporary segments, overriding any `NOLOGGING` setting for individual objects. The database must be open and in `READ` `WRITE` mode.

This setting does not exclude the `NOLOGGING` attribute. You can specify both `FORCE` `LOGGING` and `NOLOGGING`. In this case, `NOLOGGING` is the default logging mode for objects subsequently created in the tablespace, but the database ignores this default as long as the tablespace or the database is in `FORCE` `LOGGING` mode. If you subsequently take the tablespace out of `FORCE` `LOGGING` mode, then the `NOLOGGING` default is once again enforced.

Restriction on Forced Logging You cannot specify `FORCE` `LOGGING` for an undo or temporary tablespace.

ENCRYPTION Clause

Use this clause to specify the encryption properties of the tablespace. This clause does not actually encrypt the tablespace. You must also specify the `ENCRYPT` keyword as part of the `DEFAULT` `storage_clause` in this statement in order for the tablespace to be encrypted. In addition, you must already have used `ALTER` `SYSTEM` `SET` `ENCRYPTION` `WALLET` `OPEN` `IDENTIFIED` `BY` ... to load the TDE master key into database memory for the duration of the instance, or establish a connection to the HSM to send the encrypted table and tablespace keys to the HSM and receive them back decrypted. For more information, see ["SET ENCRYPTION WALLET Clause"](statements_2017.md#BABFBJBI).

Note:

You cannot decrypt a tablespace that has been created encrypted. You must create an unencrypted tablespace and re-create the database objects in the unencrypted tablespace.

tablespace\_encryption\_spec Specify `USING` '`encrypt_algorithm`' to indicate the name of the encryption algorithm to be used. Valid algorithms are `AES256`, `AES192`, `AES128` and `3DES168`. If you omit this clause, then the database uses `AES128`.

DEFAULT Clause

The `DEFAULT` clause lets you specify default parameters for the tablespace.

table\_compression Use the `table_compression` clause to specify default compression of data for all tables created in the tablespace. This clause is not valid for a temporary tablespace. Refer to the [table\_compression](statements_7002.md#i2128733) clause of `CREATE` `TABLE` for the full semantics of this clause.

inmemory\_clause Use the `inmemory_clause` to specify the default In-Memory Column Store (IM column store) settings for all tables and materialized views created in the tablespace. This clause is not valid for a temporary tablespace.

* Specify `INMEMORY` to enable all tables and materialized views for the IM column store.

  You can optionally use the `inmemory_parameters` clause to specify how the table or materialized view data is stored in the IM column store. The `inmemory_parameters` clause has the same semantics in `CREATE` `TABLE` and `CREATE` `TABLESPACE`. Refer to the [inmemory\_parameters](statements_7002.md#CEGIDFIC) clause of `CREATE` `TABLE` for the full semantics of this clause.
* Specify `NO` `INMEMORY` to disable all tables and materialized views for the IM column store. This is the default.

ilm\_clause Use the `ilm_clause` to specify default Automatic Data Optimization settings for all tables created in the tablespace. This clause is not valid for a temporary tablespace. Refer to the [ilm\_clause](statements_7002.md#CJAIIDEA) of `CREATE` `TABLE` for the full semantics of this clause.

storage\_clause Use the `storage_clause` to specify storage parameters for all objects created in the tablespace. This clause is not valid for a temporary tablespace or a locally managed tablespace. For a dictionary-managed tablespace, you can specify the following storage parameters with this clause: `ENCRYPT`, `INITIAL`, `NEXT`, `MINEXTENTS`, `MAXEXTENTS`, `MAXSIZE`, and `PCTINCREASE`. Refer to [storage\_clause](clauses009.md#i997450) for more information.

ONLINE | OFFLINE Clauses

Use these clauses to determine whether the tablespace is online or offline. This clause is not valid for a temporary tablespace.

ONLINE  Specify `ONLINE` to make the tablespace available immediately after creation to users who have been granted access to the tablespace. This is the default.

OFFLINE  Specify `OFFLINE` to make the tablespace unavailable immediately after creation.

The data dictionary view `DBA_TABLESPACES` indicates whether each tablespace is online or offline.

extent\_management\_clause

The `extent_management_clause` lets you specify how the extents of the tablespace will be managed.

Note:

After you have specified extent management with this clause, you can change extent management only by migrating the tablespace.

* `AUTOALLOCATE` specifies that the tablespace is system managed. Users cannot specify an extent size. You cannot specify `AUTOALLOCATE` for a temporary tablespace.
* `UNIFORM` specifies that the tablespace is managed with uniform extents of `SIZE` bytes.The default `SIZE` is 1 megabyte. All extents of temporary tablespaces are of uniform size, so this keyword is optional for a temporary tablespace. However, you must specify `UNIFORM` in order to specify `SIZE`. You cannot specify `UNIFORM` for an undo tablespace.

If you do not specify `AUTOALLOCATE` or `UNIFORM`, then the default is `UNIFORM` for temporary tablespaces and `AUTOALLOCATE` for all other types of tablespaces.

If you do not specify the `extent_management_clause`, then Oracle Database interprets the `MINIMUM` `EXTENT` clause and the `DEFAULT` `storage_clause` to determine extent management.

Note:

The

`DICTIONARY`

keyword is deprecated. It is still supported for backward compatibility. However, Oracle recommends that you create locally managed tablespaces. Locally managed tablespaces are much more efficiently managed than dictionary-managed tablespaces. The creation of new dictionary-managed tablespaces is scheduled for desupport.

Restrictions on Extent Management Extent management is subject to the following restrictions:

* A permanent locally managed tablespace can contain only permanent objects. If you need a locally managed tablespace to store temporary objects, for example, if you will assign it as a user's temporary tablespace, then use the `temporary_tablespace_clause`.
* If you specify this clause, then you cannot specify `DEFAULT` `storage_clause,` `MINIMUM` `EXTENT`, or the `temporary_tablespace_clause`.

segment\_management\_clause

The `segment_management_clause` is relevant only for permanent, locally managed tablespaces. It lets you specify whether Oracle Database should track the used and free space in the segments in the tablespace using free lists or bitmaps. This clause is not valid for a temporary tablespace.

AUTO  Specify `AUTO` if you want the database to manage the free space of segments in the tablespace using a bitmap. If you specify `AUTO`, then the database ignores any specification for `PCTUSED`, `FREELIST`, and `FREELIST` `GROUPS` in subsequent storage specifications for objects in this tablespace. This setting is called automatic segment-space management and is the default.

MANUAL Specify `MANUAL` if you want the database to manage the free space of segments in the tablespace using free lists. Oracle strongly recommends that you do not use this setting and that you create tablespaces with automatic segment-space management.

To determine the segment management of an existing tablespace, query the `SEGMENT_SPACE_MANAGEMENT` column of the `DBA_TABLESPACES` or `USER_TABLESPACES` data dictionary view.

Notes:

If you specify

`AUTO`

segment management, then:

* If you set extent management to `LOCAL` `UNIFORM`, then you must ensure that each extent contains at least 5 database blocks.
* If you set extent management to `LOCAL` `AUTOALLOCATE`, and if the database block size is 16K or greater, then Oracle manages segment space by creating extents with a minimum size of 5 blocks rounded up to 64K.

Restrictions on Automatic Segment-Space Management This clause is subject to the following restrictions:

* You can specify this clause only for a permanent, locally managed tablespace.
* You cannot specify this clause for the `SYSTEM` tablespace.

flashback\_mode\_clause

Use this clause in conjunction with the `ALTER` `DATABASE` `FLASHBACK` clause to specify whether the tablespace can participate in `FLASHBACK` `DATABASE` operations. This clause is useful if you have the database in `FLASHBACK` mode but you do not want Oracle Database to maintain Flashback log data for this tablespace.

This clause is not valid for temporary or undo tablespaces.

FLASHBACK ON Specify `FLASHBACK` `ON` to put the tablespace in `FLASHBACK` mode. Oracle Database will save Flashback log data for this tablespace and the tablespace can participate in a `FLASHBACK` `DATABASE` operation. If you omit the `flashback_mode_clause`, then `FLASHBACK` `ON` is the default.

FLASHBACK OFF Specify `FLASHBACK` `OFF` to take the tablespace out of `FLASHBACK` mode. Oracle Database will not save any Flashback log data for this tablespace. You must take the data files in this tablespace offline or drop them prior to any subsequent `FLASHBACK` `DATABASE` operation. Alternatively, you can take the entire tablespace offline. In either case, the database does not drop existing Flashback logs.

Note:

The

`FLASHBACK`

mode of a tablespace is independent of the

`FLASHBACK`

mode of an individual table.

temporary\_tablespace\_clause

Use this clause to create a locally managed temporary tablespace, which is an allocation of space in the database that can contain transient data that persists only for the duration of a session. This transient data cannot be recovered after process or instance failure.

The transient data can be user-generated schema objects such as temporary tables or system-generated data such as temp space used by hash joins and sort operations. When a temporary tablespace, or a tablespace group of which this tablespace is a member, is assigned to a particular user, then Oracle Database uses the tablespace for sorting operations in transactions initiated by that user.

The `TEMPFILE` clause is described in ["DATAFILE | TEMPFILE Clause"](#i2171920). The `extent_management_clause` is described in [extent\_management\_clause](#i2063392) .

tablespace\_group\_clause

This clause is relevant only for temporary tablespaces. Use this clause to determine whether `tablespace` is a member of a tablespace group. A tablespace group lets you assign multiple temporary tablespaces to a single user and increases the addressability of temporary tablespaces.

* Specify a group name to indicate that `tablespace` is a member of this tablespace group. The group name cannot be the same as `tablespace` or any other existing tablespace. If the tablespace group already exists, then Oracle Database adds the new tablespace to that group. If the tablespace group does not exist, then the database creates the group and adds the new tablespace to that group.
* Specify an empty string (' ') to indicate that `tablespace` is not a member of any tablespace group.

Restrictions on Temporary Tablespaces The data stored in temporary tablespaces persists only for the duration of a session. Therefore, only a subset of the `CREATE` `TABLESPACE` clauses are relevant for temporary tablespaces. The only clauses you can specify for a temporary tablespace are the `TEMPFILE` clause, the `tablespace_group_clause`, and the `extent_management_clause`.

undo\_tablespace\_clause

Specify `UNDO` to create an undo tablespace. When you run the database in automatic undo management mode, Oracle Database manages undo space using the undo tablespace instead of rollback segments. This clause is useful if you are now running in automatic undo management mode but your database was not created in automatic undo management mode.

Oracle Database always assigns an undo tablespace when you start up the database in automatic undo management mode. If no undo tablespace has been assigned to this instance, then the database uses the `SYSTEM` rollback segment. You can avoid this by creating an undo tablespace, which the database will implicitly assign to the instance if no other undo tablespace is currently assigned.

The `DATAFILE` clause is described in ["DATAFILE | TEMPFILE Clause"](#i2171920).

extent\_management\_clause

It is unnecessary to specify the `extent_management_clause` when creating an undo tablespace, because undo tablespaces must be locally managed tablespaces that use `AUTOALLOCATE` extent management. If you do specify this clause, then you must specify `EXTENT` `MANAGEMENT` `LOCAL` or `EXTENT` `MANAGEMENT` `LOCAL` `AUTOALLOCATE`, both of which are the same as omitting this clause. Refer to [extent\_management\_clause](#i2063392) for the full semantics of this clause.

tablespace\_retention\_clause

This clause is valid only for undo tablespaces.

* `RETENTION` `GUARANTEE` specifies that Oracle Database should preserve unexpired undo data in all undo segments of `tablespace` even if doing so forces the failure of ongoing operations that need undo space in those segments. This setting is useful if you need to issue an Oracle Flashback Query or an Oracle Flashback Transaction Query to diagnose and correct a problem with the data.
* `RETENTION` `NOGUARANTEE` returns the undo behavior to normal. Space occupied by unexpired undo data in undo segments can be consumed if necessary by ongoing transactions. This is the default.

Restrictions on Undo Tablespaces Undo tablespaces are subject to the following restrictions:

* You cannot create database objects in this tablespace. It is reserved for system-managed undo data.
* The only clauses you can specify for an undo tablespace are the `DATAFILE` clause and the `extent_management_clause` to specify local `AUTOALLOCATE` extent management. You cannot specify local `UNIFORM` extent management or dictionary extent management using the `extent_management_clause`. All undo tablespaces are created permanent, read/write, and in logging mode. Values for `MINIMUM` `EXTENT` and `DEFAULT` `STORAGE` are system generated.

Examples

These examples assume that your database is using 8K blocks.

Creating a Bigfile Tablespace: Example The following example creates a bigfile tablespace `bigtbs_01` with a data file `bigtbs_f1.dbf` of 20 MB:

```
CREATE BIGFILE TABLESPACE bigtbs_01
  DATAFILE 'bigtbs_f1.dbf'
  SIZE 20M AUTOEXTEND ON;
```

Creating an Undo Tablespace: Example The following example creates a 10 MB undo tablespace `undots1`:

```
CREATE UNDO TABLESPACE undots1
   DATAFILE 'undotbs_1a.dbf'
   SIZE 10M AUTOEXTEND ON
   RETENTION GUARANTEE;
```

Creating a Temporary Tablespace: Example This statement shows how the temporary tablespace that serves as the default temporary tablespace for database users in the sample database was created:

```
CREATE TEMPORARY TABLESPACE temp_demo
   TEMPFILE 'temp01.dbf' SIZE 5M AUTOEXTEND ON;
```

Assuming that the default database block size is 2K, and that each bit in the map represents one extent, then each bit maps 2,500 blocks.

The following example sets the default location for data file creation and then creates a tablespace with an Oracle-managed temp file in the default location. The temp file is 100 M and is autoextensible with unlimited maximum size. These are the default values for Oracle Managed Files:

```
ALTER SYSTEM SET DB_CREATE_FILE_DEST = '$ORACLE_HOME/rdbms/dbs';

CREATE TEMPORARY TABLESPACE tbs_05;
```

Adding a Temporary Tablespace to a Tablespace Group: Example The following statement creates the `tbs_temp_02` temporary tablespace as a member of the `tbs_grp_01` tablespace group. If the tablespace group does not already exist, then Oracle Database creates it during execution of this statement:

```
CREATE TEMPORARY TABLESPACE tbs_temp_02
  TEMPFILE 'temp02.dbf' SIZE 5M AUTOEXTEND ON
  TABLESPACE GROUP tbs_grp_01;
```

Creating Basic Tablespaces: Examples This statement creates a tablespace named `tbs_01` with one data file:

```
CREATE TABLESPACE tbs_01 
   DATAFILE 'tbs_f2.dbf' SIZE 40M 
   ONLINE;
```

This statement creates tablespace `tbs_03` with one data file and allocates every extent as a multiple of 500K:

```
CREATE TABLESPACE tbs_03 
   DATAFILE 'tbs_f03.dbf' SIZE 20M
   LOGGING;
```

Enabling Autoextend for a Tablespace: Example This statement creates a tablespace named `tbs_02` with one data file. When more space is required, 500 kilobyte extents will be added up to a maximum size of 100 megabytes:

```
CREATE TABLESPACE tbs_02 
   DATAFILE 'diskb:tbs_f5.dbf' SIZE 500K REUSE
   AUTOEXTEND ON NEXT 500K MAXSIZE 100M;
```

Creating a Locally Managed Tablespace: Example The following statement assumes that the database block size is 2K.

```
CREATE TABLESPACE tbs_04 DATAFILE 'file_1.dbf' SIZE 10M
   EXTENT MANAGEMENT LOCAL UNIFORM SIZE 128K;
```

This statement creates a locally managed tablespace in which every extent is 128K and each bit in the bit map describes 64 blocks.

The following statement creates a locally managed tablespace with uniform extents and shows an example of a table stored in that tablespace:

```
CREATE TABLESPACE lmt1 DATAFILE 'lmt_file2.dbf' SIZE 100m REUSE
  EXTENT MANAGEMENT LOCAL UNIFORM SIZE 1M;

CREATE TABLE lmt_table1 (col1 NUMBER, col2 VARCHAR2(20))
  TABLESPACE lmt1 STORAGE (INITIAL 2m);
```

The initial segment size of the table is 2M.

The following example creates a locally managed tablespace without uniform extents:

```
CREATE TABLESPACE lmt2 DATAFILE 'lmt_file3.dbf' SIZE 100m REUSE 
  EXTENT MANAGEMENT LOCAL;

CREATE TABLE lmt_table2 (col1 NUMBER, col2 VARCHAR2(20)) 
  TABLESPACE lmt2 STORAGE (INITIAL 2m MAXSIZE 100m);
```

The initial segment size of the table is 2M. Oracle Database determines the size of each extent and the total number of extents allocated to satisfy the initial segment size. The segment's maximum size is limited to 100M.

Creating an Encrypted Tablespace: Example In the following example, the first statement enables encryption for the database by opening the wallet. The second statement creates an encrypted tablespace.

```
ALTER SYSTEM SET ENCRYPTION WALLET OPEN IDENTIFIED BY "wallet_password";

CREATE TABLESPACE encrypt_ts
  DATAFILE '$ORACLE_HOME/dbs/encrypt_df.dbf' SIZE 1M
  ENCRYPTION USING 'AES256'
  DEFAULT STORAGE (ENCRYPT);
```

Specifying Segment Space Management for a Tablespace: Example The following example creates a tablespace with automatic segment-space management:

```
CREATE TABLESPACE auto_seg_ts DATAFILE 'file_2.dbf' SIZE 1M
   EXTENT MANAGEMENT LOCAL
   SEGMENT SPACE MANAGEMENT AUTO;
```

Creating Oracle Managed Files: Examples The following example sets the default location for data file creation and creates a tablespace with a data file in the default location. The data file is 100M and is autoextensible with an unlimited maximum size:

```
ALTER SYSTEM SET DB_CREATE_FILE_DEST = '$ORACLE_HOME/rdbms/dbs';

CREATE TABLESPACE omf_ts1;
```

The following example creates a tablespace with an Oracle-managed data file of 100M that is not autoextensible:

```
CREATE TABLESPACE omf_ts2 DATAFILE AUTOEXTEND OFF;
```