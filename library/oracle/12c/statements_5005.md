# Oracle 12c - statements_5005
Source: https://docs.oracle.com/database/121/SQLRF/statements_5005.htm

Semantics

database

Specify the name of the database to be created. The name must match the value of the `DB_NAME` initialization parameter. The name can be up to 8 bytes long and can contain only ASCII characters. Oracle Database writes this name into the control file. If you subsequently issue an `ALTER` `DATABASE` statement that explicitly specifies a database name, then Oracle Database verifies that name with the name in the control file.

The database name is case insensitive and is stored in uppercase ASCII characters. If you specify the database name as a quoted identifier, then the quotation marks are silently ignored.

Note:

You cannot use special characters from European or Asian character sets in a database name. For example, characters with umlauts are not allowed.

If you omit the database name from a `CREATE` `DATABASE` statement, then Oracle Database uses the name specified by the initialization parameter `DB_NAME`. The `DB_NAME` initialization parameter must be set in the database initialization parameter file, and if you specify a different name from the value of that parameter, then the database returns an error. Refer to ["Database Object Naming Rules"](sql_elements008.md#i27570) for additional rules to which database names should adhere.

USER SYS ..., USER SYSTEM ...

Use these clauses to establish passwords for the `SYS` and `SYSTEM` users. These clauses are not mandatory in this release. However, if you specify either clause, then you must specify both clauses.

If you do not specify these clauses, then Oracle Database creates default passwords `change_on_install` for user `SYS` and `manager` for user `SYSTEM`. You can subsequently change these passwords using the `ALTER` `USER` statement. You can also use `ALTER` `USER` to add password management attributes after database creation.

CONTROLFILE REUSE Clause

Specify `CONTROLFILE` `REUSE` to reuse existing control files identified by the initialization parameter `CONTROL_FILES`, overwriting any information they currently contain. Normally you use this clause only when you are re-creating a database, rather than creating one for the first time. When you create a database for the first time, Oracle Database creates a control file in the default destination, which is dependent on the value or several initialization parameters. See `CREATE` `CONTROLFILE`, ["Semantics"](statements_5004.md#i2146881).

You cannot use this clause if you also specify a parameter value that requires that the control file be larger than the existing files. These parameters are `MAXLOGFILES`, `MAXLOGMEMBERS`, `MAXLOGHISTORY`, `MAXDATAFILES`, and `MAXINSTANCES`.

If you omit this clause and any of the files specified by `CONTROL_FILES` already exist, then the database returns an error.

MAXDATAFILES Clause

Specify the initial sizing of the data files section of the control file at `CREATE` `DATABASE` or `CREATE` `CONTROLFILE` time. An attempt to add a file whose number is greater than `MAXDATAFILES`, but less than or equal to `DB_FILES`, causes the Oracle Database control file to expand automatically so that the data files section can accommodate more files.

The number of data files accessible to your instance is also limited by the initialization parameter `DB_FILES`.

MAXINSTANCES Clause

Specify the maximum number of instances that can simultaneously have this database mounted and open. This value takes precedence over the value of initialization parameter `INSTANCES`. The minimum value is 1. The maximum value is 1055. The default depends on your operating system.

CHARACTER SET Clause

Specify the character set the database uses to store data. The supported character sets and default value of this parameter depend on your operating system.

Restriction on CHARACTER SET You cannot specify the `AL16UTF16` character set as the database character set.

NATIONAL CHARACTER SET Clause

Specify the national character set used to store data in columns specifically defined as `NCHAR`, `NCLOB`, or `NVARCHAR2`. Valid values are `AL16UTF16` and `UTF8`. The default is `AL16UTF16`.

SET DEFAULT TABLESPACE Clause

Use this clause to determine the default type of subsequently created tablespaces and of the `SYSTEM` and `SYSAUX` tablespaces. Specify either `BIGFILE` or `SMALLFILE` to set the default type of subsequently created tablespaces as a bigfile or smallfile tablespace, respectively.

* A bigfile tablespace contains only one data file or temp file, which can contain up to approximately 4 billion (232) blocks. The maximum size of the single data file or temp file is 128 terabytes (TB) for a tablespace with 32K blocks and 32TB for a tablespace with 8K blocks.
* A smallfile tablespace is a traditional Oracle tablespace, which can contain 1022 data files or temp files, each of which can contain up to approximately 4 million (222) blocks.

If you omit this clause, then Oracle Database creates smallfile tablespaces by default.

database\_logging\_clauses

Use the `database_logging_clauses` to determine how Oracle Database will handle redo log files for this database.

LOGFILE Clause

Specify one or more files to be used as redo log files. Use the `redo_log_file_spec` form of `file_specification` to create regular redo log files in an operating system file system or to create Oracle ASM disk group redo log files. When using a form of `ASM_filename`, you cannot specify the `autoextend_clause` of `redo_log_file_spec.`

The `redo_log_file_spec` clause specifies a redo log file group containing one or more redo log file members (copies). All redo log files specified in a `CREATE` `DATABASE` statement are added to redo log thread number 1.

If you omit the `LOGFILE` clause, then Oracle Database creates an Oracle-managed log file member in the default destination, which is one of the following locations (in order of precedence):

* If `DB_CREATE_ONLINE_LOG_DEST_``n` is set, then the database creates a log file member in each directory specified, up to the value of the `MAXLOGMEMBERS` initialization parameter.
* If the `DB_CREATE_ONLINE_LOG_DEST_``n` parameter is not set, but both the `DB_CREATE_FILE_DEST` and `DB_RECOVERY_FILE_DEST` initialization parameters are set, then the database creates one Oracle-managed log file member in each of those locations. The log file in the `DB_CREATE_FILE_DEST` destination is the first member.
* If only the `DB_CREATE_FILE_DEST` initialization parameter is specified, then Oracle Database creates a log file member in that location.
* If only the `DB_RECOVERY_FILE_DEST` initialization parameter is specified, then Oracle Database creates a log file member in that location.

In all these cases, the parameter settings must correctly specify operating system filenames or creation form Oracle ASM filenames, as appropriate.

If no values are set for any of these parameters, then the database creates a log file in the default location for the operating system on which the database is running. This log file is not an Oracle Managed File.

GROUP integer Specify the number that identifies the redo log file group. The value of `integer` can range from 1 to the value of the `MAXLOGFILES` parameter. A database must have at least two redo log file groups. You cannot specify multiple redo log file groups having the same `GROUP` value. If you omit this parameter, then Oracle Database generates its value automatically. You can examine the `GROUP` value for a redo log file group through the dynamic performance view `V$LOG`.

MAXLOGFILES Clause

Specify the maximum number of redo log file groups that can ever be created for the database. Oracle Database uses this value to determine how much space to allocate in the control file for the names of redo log files. The default, minimum, and maximum values depend on your operating system.

MAXLOGMEMBERS Clause

Specify the maximum number of members, or copies, for a redo log file group. Oracle Database uses this value to determine how much space to allocate in the control file for the names of redo log files. The minimum value is 1. The maximum and default values depend on your operating system.

MAXLOGHISTORY Clause

This parameter is useful only if you are using Oracle Database in `ARCHIVELOG` mode with Oracle Real Application Clusters (Oracle RAC). Specify the maximum number of archived redo log files for automatic media recovery of Oracle RAC. The database uses this value to determine how much space to allocate in the control file for the names of archived redo log files. The minimum value is 0. The default value is a multiple of the `MAXINSTANCES` value and depends on your operating system. The maximum value is limited only by the maximum size of the control file.

ARCHIVELOG

Specify `ARCHIVELOG` if you want the contents of a redo log file group to be archived before the group can be reused. This clause prepares for the possibility of media recovery.

NOARCHIVELOG

Specify `NOARCHIVELOG` if the contents of a redo log file group need not be archived before the group can be reused. This clause does not allow for the possibility of media recovery.

The default is `NOARCHIVELOG` mode. After creating the database, you can change between `ARCHIVELOG` mode and `NOARCHIVELOG` mode with the `ALTER` `DATABASE` statement.

FORCE LOGGING

Use this clause to put the database into `FORCE` `LOGGING` mode. Oracle Database will log all changes in the database except for changes in temporary tablespaces and temporary segments. This setting takes precedence over and is independent of any `NOLOGGING` or `FORCE` `LOGGING` settings you specify for individual tablespaces and any `NOLOGGING` settings you specify for individual database objects.

`FORCE` `LOGGING` mode is persistent across instances of the database. If you shut down and restart the database, then the database is still in `FORCE` `LOGGING` mode. However, if you re-create the control file, then Oracle Database will take the database out of `FORCE` `LOGGING` mode unless you specify `FORCE` `LOGGING` in the `CREATE` `CONTROLFILE` statement.

tablespace\_clauses

Use the tablespace clauses to configure the `SYSTEM` and `SYSAUX` tablespaces and to specify a default temporary tablespace and an undo tablespace.

extent\_management\_clause

Use this clause to create a locally managed `SYSTEM` tablespace. If you omit this clause, then the `SYSTEM` tablespace will be dictionary managed.

Caution:

When you create a locally managed

`SYSTEM`

tablespace, you cannot change it to be dictionary managed, nor can you create any other dictionary-managed tablespaces in this database.

If you specify this clause, then the database must have a default temporary tablespace, because a locally managed `SYSTEM` tablespace cannot store temporary segments.

* If you specify `EXTENT` `MANAGEMENT` `LOCAL` but you do not specify the `DATAFILE` clause, then you can omit the `default_temp_tablespace` clause. Oracle Database will create a default temporary tablespace called `TEMP` with one data file of size 10M with autoextend disabled.
* If you specify both `EXTENT` `MANAGEMENT` `LOCAL` and the `DATAFILE` clause, then you must also specify the `default_temp_tablespace` clause and explicitly specify a temp file for that temporary tablespace.

If you have opened the instance in automatic undo mode, similar requirements exist for the database undo tablespace:

* If you specify `EXTENT` `MANAGEMENT` `LOCAL` but you do not specify the `DATAFILE` clause, then you can omit the `undo_tablespace` clause. Oracle Database will create an undo tablespace named `SYS_UNDOTBS`.
* If you specify both `EXTENT` `MANAGEMENT` `LOCAL` and the `DATAFILE` clause, then you must also specify the `undo_tablespace` clause and explicitly specify a data file for that tablespace.

DATAFILE Clause

Specify one or more files to be used as data files. All these files become part of the `SYSTEM` tablespace. Use the data `file_tempfile_spec` form of `file_specification` to create regular data files and temp files in an operating system file system or to create Oracle ASM disk group files.

Caution:

This clause is optional, as is the

`DATAFILE`

clause of the

`undo_tablespace`

clause. Therefore, to avoid ambiguity, if your intention is to specify a data file for the

`SYSTEM`

tablespace with this clause, then do

not

specify it immediately after an

`undo_tablespace`

clause that does not include the optional

`DATAFILE`

clause. If you do so, then Oracle Database will interpret the

`DATAFILE`

clause to be part of the

`undo_tablespace`

clause.

The syntax for specifying data files for the `SYSTEM` tablespace is the same as that for specifying data files during tablespace creation using the `CREATE` `TABLESPACE` statement, whether you are storing files using Oracle ASM or in a file system.

If you are running the database in automatic undo mode and you specify a data file name for the `SYSTEM` tablespace, then Oracle Database expects to generate data files for all tablespaces. Oracle Database does this automatically if you are using Oracle Managed Files—you have set a value for the `DB_CREATE_FILE_DEST` initialization parameter. However, if you are not using Oracle Managed Files and you specify this clause, then you must also specify the `undo_tablespace` clause and the `default_temp_tablespace` clause.

If you omit this clause, then:

* If the `DB_CREATE_FILE_DEST` initialization parameter is set, then Oracle Database creates a 100 MB Oracle-managed data file with a system-generated name in the default file destination specified in the parameter.
* If the `DB_CREATE_FILE_DEST` initialization parameter is not set, then Oracle Database creates one data file whose name and size depend on your operating system.

SYSAUX Clause

Oracle Database creates both the `SYSTEM` and `SYSAUX` tablespaces as part of every database. Use this clause if you are not using Oracle Managed Files and you want to specify one or more data files for the `SYSAUX` tablespace.

You must specify this clause if you have specified one or more data files for the `SYSTEM` tablespace using the `DATAFILE` clause. If you are using Oracle Managed Files and you omit this clause, then the database creates the `SYSAUX` data files in the default location set up for Oracle Managed Files.

If you have enabled Oracle Managed Files and you omit the `SYSAUX` clause, then the database creates the `SYSAUX` tablespace as an online, permanent, locally managed tablespace with one data file of 100 MB, with logging enabled and automatic segment-space management.

The syntax for specifying data files for the `SYSAUX` tablespace is the same as that for specifying data files during tablespace creation using the `CREATE` `TABLESPACE` statement, whether you are storing files using Oracle ASM or in a file system.

default\_tablespace

Specify this clause to create a default permanent tablespace for the database. Oracle Database creates a smallfile tablespace and subsequently will assign to this tablespace any non-`SYSTEM` users for whom you do not specify a different permanent tablespace. If you do not specify this clause, then the `SYSTEM` tablespace is the default permanent tablespace for non-`SYSTEM` users.

The `DATAFILE` clause and `extent_management_clause` have the same semantics they have in a `CREATE` `TABLESPACE` statement. Refer to ["DATAFILE | TEMPFILE Clause"](statements_7003.md#i2171920) and [extent\_management\_clause](statements_7003.md#i2063392) for information on these clauses.

default\_temp\_tablespace

Specify this clause to create a default temporary tablespace for the database. Oracle Database will assign to this temporary tablespace any users for whom you do not specify a different temporary tablespace. If you do not specify this clause, and if the database does not create a default temporary tablespace automatically in the process of creating a locally managed `SYSTEM` tablespace, then the `SYSTEM` tablespace is the default temporary tablespace.

Specify `BIGFILE` or `SMALLFILE` to determine whether the default temporary tablespace is a bigfile or smallfile tablespace. These clauses have the same semantics as in the ["SET DEFAULT TABLESPACE Clause"](#i2177341).

The `TEMPFILE` clause part of this clause is optional if you have enabled Oracle Managed Files by setting the `DB_CREATE_FILE_DEST` initialization parameter. If you have not specified a value for this parameter, then the `TEMPFILE` clause is required. If you have specified `BIGFILE`, then you can specify only one temp file in this clause.

The syntax for specifying temp files for the default temporary tablespace is the same as that for specifying temp files during temporary tablespace creation using the `CREATE` `TABLESPACE` statement, whether you are storing files using Oracle ASM or in a file system.

Note:

On some operating systems, Oracle does not allocate space for a temp file until the temp file blocks are actually accessed. This delay in space allocation results in faster creation and resizing of temp files, but it requires that sufficient disk space is available when the temp files are later used. To avoid potential problems, before you create or resize a temp file, ensure that the available disk space exceeds the size of the new temp file or the increased size of a resized temp file. The excess space should allow for anticipated increases in disk space use by unrelated operations as well. Then proceed with the creation or resizing operation.

Restrictions on Default Temporary Tablespaces Default temporary tablespaces are subject to the following restrictions:

The `extent_management_clause` clause has the same semantics in `CREATE` `DATABASE` and `CREATE` `TABLESPACE` statements. For complete information, refer to the `CREATE` `TABLESPACE` ... [extent\_management\_clause](statements_7003.md#i2063392) .

undo\_tablespace

If you have opened the instance in automatic undo mode (the `UNDO_MANAGEMENT` initialization parameter is set to `AUTO`, which is the default), then you can specify the `undo_tablespace` to create a tablespace to be used for undo data. Oracle strongly recommends that you use automatic undo mode. However, if you want undo space management to be handled by way of rollback segments, then you must omit this clause. You can also omit this clause if you have set a value for the `UNDO_TABLESPACE` initialization parameter. If that parameter has been set, and if you specify this clause, then `tablespace` must be the same as that parameter value.

* Specify `BIGFILE` if you want the undo tablespace to be a bigfile tablespace. A bigfile tablespace contains only one data file, which can be up to 8 exabytes (8 million terabytes) in size.
* Specify `SMALLFILE` if you want the undo tablespace to be a smallfile tablespace. A smallfile tablespace is a traditional Oracle Database tablespace, which can contain 1022 data files or temp files, each of which can contain up to approximately 4 million (222) blocks.
* The `DATAFILE` clause part of this clause is optional if you have enabled Oracle Managed Files by setting the `DB_CREATE_FILE_DEST` initialization parameter. If you have not specified a value for this parameter, then the `DATAFILE` clause is required. If you have specified `BIGFILE`, then you can specify only one data file in this clause.

The syntax for specifying data files for the undo tablespace is the same as that for specifying data files during tablespace creation using the `CREATE` `TABLESPACE` statement, whether you are storing files using Oracle ASM or in a file system.

If you specify this clause, then Oracle Database creates an undo tablespace named `tablespace`, creates the specified data file(s) as part of the undo tablespace, and assigns this tablespace as the undo tablespace of the instance. Oracle Database will manage undo data using this undo tablespace. The `DATAFILE` clause of this clause has the same behavior as described in ["DATAFILE Clause"](#i2150088).

If you have specified a value for the `UNDO_TABLESPACE` initialization parameter in your initialization parameter file before mounting the database, then you must specify the same name in this clause. If these names differ, then Oracle Database will return an error when you open the database.

If you omit this clause, then Oracle Database creates a default database with a default smallfile undo tablespace named `SYS_UNDOTBS` and assigns this default tablespace as the undo tablespace of the instance. This undo tablespace allocates disk space from the default files used by the `CREATE` `DATABASE` statement, and it has an initial extent of 10M. Oracle Database handles the system-generated data file as described in ["DATAFILE Clause"](#i2150088). If Oracle Database is unable to create the undo tablespace, then the entire `CREATE` `DATABASE` operation fails.

set\_time\_zone\_clause

Use the `SET` `TIME_ZONE` clause to set the time zone of the database. You can specify the time zone in two ways:

* By specifying a displacement from UTC (Coordinated Universal Time—formerly Greenwich Mean Time). The valid range of `hh:mi` is -12:00 to +14:00.
* By specifying a time zone region. To see a listing of valid time zone region names, query the `TZNAME` column of the `V$TIMEZONE_NAMES` dynamic performance view.

Note:

Oracle recommends that you set the database time zone to UTC (

`0:00`

). Doing so can improve performance, especially across databases, as no conversion of time zones will be required.

Oracle Database normalizes all `TIMESTAMP` `WITH` `LOCAL` `TIME` `ZONE` data to the time zone of the database when the data is stored on disk. If you do not specify the `SET` `TIME_ZONE` clause, then the database uses the operating system time zone of the server. If the operating system time zone is not a valid Oracle Database time zone, then the database time zone defaults to UTC.

USER\_DATA TABLESPACE Clause

This clause lets you create a tablespace that is used for storing user data and database options such as Oracle XML DB.

* If you specify this clause when creating a multitenant container database (CDB), then the tablespace is created as part of the seed. Pluggable databases (PDBs) subsequently created using the seed will include this tablespace and its data file. The tablespace and data file specified in this clause are not used by the root.
* If you specify this clause when creating a non-CDB, then the tablespace is created as part of the non-CDB.

Specify `BIGFILE` or `SMALLFILE` to determine whether the tablespace is a bigfile or smallfile tablespace. If you omit these clauses, then Oracle Database creates a tablespace of the type that you specify with the `SET` `DEFAULT` `TABLESPACE` clause. If you do not specify the `SET` `DEFAULT` `TABLESPACE` clause, then Oracle Database creates a smallfile tablespace. These clauses have the same semantics as in the ["SET DEFAULT TABLESPACE Clause"](#i2177341).

Use the `datafile_tempfile_spec` clause to specify one or more data files for the tablespace. Refer to [datafile\_tempfile\_spec](clauses004.md#i1030551) for the full semantics of this clause.

enable\_pluggable\_database

Specify this clause to create a CDB. Before issuing the `CREATE` `DATABASE` statement, you must set the `ENABLE_PLUGGABLE_DATABASE` initialization parameter to `TRUE`. The `CREATE` `DATABASE` statement will create a CDB that contains a root and a seed container. You can then create PDBs in the CDB by using the `CREATE PLUGGABLE DATABASE` statement. If you omit the `enable_pluggable_database` clause, then a non-CDB is created and it can never contain any containers.

file\_name\_convert

Use the `file_name_convert` clause to determine how the database generates the names of files (such as data files and wallet files) associated with the seed by using the names of files associated with the root.

* For `filename_pattern`, specify a string found in file names associated with the root.
* For `replacement_filename_pattern`, specify a replacement string.

Oracle Database will replace `filename_pattern` with `replacement_filename_pattern` when generating the names of files associated with the seed.

File name patterns cannot match files or directories managed by Oracle Managed Files.

You can specify `FILE_NAME_CONVERT` `=` `NONE`, which is the same as omitting this clause. If you omit this clause, then the database first attempts to use Oracle Managed Files to generate seed file names. If you are not using Oracle Managed Files, then the database uses the `PDB_FILE_NAME_CONVERT` initialization parameter to generate file names. If this parameter is not set, then an error occurs.

tablespace\_datafile\_clauses

Use these clauses to specify attributes for all data files comprising the `SYSTEM` and `SYSAUX` tablespaces in the seed PDB. If you do not specify `SIZE` `size_clause`, then the data file size for a given tablespace will be set to a predetermined fraction of the size of the corresponding root data file. If you do not specify the `autoextend_clause`, then those values are inherited from the root.

Refer to [size\_clause](clauses008.md#CHDEIJBC) and [autoextend\_clause](clauses004.md#CJAJIHDC) for the full semantics of these clauses.