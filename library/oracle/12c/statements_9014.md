# Oracle 12c - statements_9014
Source: https://docs.oracle.com/database/121/SQLRF/statements_9014.htm

|  |  |
| --- | --- |
| Advisor Framework Privileges: All of the advisor framework privileges are part of the DBA role. | — |
| `ADVISOR` | Access the advisor framework through PL/SQL packages such as `DBMS_ADVISOR` and `DBMS_SQLTUNE`.  Refer to [Oracle Database PL/SQL Packages and Types Reference](../ARPLS/toc.md) for information on these packages. |
| `ADMINISTER SQL TUNING SET` | Create, drop, select (read), load (write), and delete a SQL tuning set owned by the grantee through the `DBMS_SQLTUNE` package. |
| `ADMINISTER ANY SQL TUNING SET` | Create, drop, select (read), load (write), and delete a SQL tuning set owned by any user through the `DBMS_SQLTUNE` package. |
| `CREATE ANY SQL PROFILE` | Accept a SQL Profile recommended by the SQL Tuning Advisor, which is accessed through Enterprise Manager or by the `DBMS_SQLTUNE` package.  Note: This privilege has been deprecated in favor of `ADMINISTER` `SQL` `MANAGEMENT` `OBJECT`. |
| `ALTER ANY SQL PROFILE` | Alter the attributes of an existing SQL Profile.  Note: This privilege has been deprecated in favor of `ADMINISTER` `SQL` `MANAGEMENT` `OBJECT`. |
| `DROP ANY SQL PROFILE` | Drop existing SQL Profiles.  Note: This privilege has been deprecated in favor of `ADMINISTER` `SQL` `MANAGEMENT` `OBJECT`. |
| `ADMINISTER SQL MANAGEMENT OBJECT` | Create, alter, and drop SQL Profiles owned by any user through the `DBMS_SQLTUNE` package. |
| CLUSTERS: | — |
| `CREATE CLUSTER` | Create clusters in the grantee's schema. |
| `CREATE ANY CLUSTER` | Create clusters in any schema except `SYS`. Behaves similarly to `CREATE` `ANY` `TABLE`. |
| `ALTER ANY CLUSTER` | Alter clusters in any schema except `SYS`. |
| `DROP ANY CLUSTER` | Drop clusters in any schema except `SYS`. |
| CONTEXTS: | — |
| `CREATE ANY CONTEXT` | Create any context namespace. |
| `DROP ANY CONTEXT` | Drop any context namespace. |
| DATA REDACTION: | — |
| `EXEMPT` `REDACTION` `POLICY` | Bypass any existing Oracle Data Redaction policies and view actual data from tables or views on which Data Redaction policies are defined. |
| DATABASE: | — |
| `ALTER DATABASE` | Alter the database. |
| `ALTER SYSTEM` | Issue `ALTER` `SYSTEM` statements. |
| `AUDIT SYSTEM` | Issue `AUDIT` statements. |
| DATABASE LINKS: | — |
| `CREATE DATABASE LINK` | Create private database links in the grantee's schema. |
| `CREATE PUBLIC DATABASE LINK` | Create public database links. |
| `ALTER` `DATABASE` `LINK` | Modify a fixed-user database link when the password of the connection or authentication user changes. |
| `ALTER` `PUBLIC` `DATABASE` `LINK` | Modify a public fixed-user database link when the password of the connection or authentication user changes. |
| `DROP PUBLIC DATABASE LINK` | Drop public database links. |
| DEBUGGING: | — |
| `DEBUG` `CONNECT` `SESSION` | Connect the current session to a debugger. |
| `DEBUG` `ANY` `PROCEDURE` | Debug all PL/SQL and Java code in any database object. Display information on all SQL statements executed by the application.  Note: Granting this privilege is equivalent to granting the `DEBUG` object privilege on all applicable objects in the database. |
| DICTIONARIES: | — |
| `ANALYZE` `ANY` `DICTIONARY` | Analyze any data dictionary object. |
| DIMENSIONS: | — |
| `CREATE DIMENSION` | Create dimensions in the grantee's schema. |
| `CREATE ANY DIMENSION` | Create dimensions in any schema except `SYS`. |
| `ALTER ANY DIMENSION` | Alter dimensions in any schema except `SYS`. |
| `DROP ANY DIMENSION` | Drop dimensions in any schema except `SYS`. |
| DIRECTORIES: | — |
| `CREATE ANY DIRECTORY` | Create directory database objects. |
| `DROP ANY DIRECTORY` | Drop directory database objects. |
| EDITIONS: | — |
| `CREATE ANY EDITION` | Create editions. |
| `DROP ANY EDITION` | Drop editions. |
| FLASHBACK DATA ARCHIVES: | — |
| `FLASHBACK` `ARCHIVE` `ADMINISTER` | Create, alter, or drop any flashback data archive. |
| INDEXES: | — |
| `CREATE ANY INDEX` | Create in any schema, except `SYS`, a domain index or an index on any table in any schema except `SYS`. |
| `ALTER ANY INDEX` | Alter indexes in any schema except `SYS`. |
| `DROP ANY INDEX` | Drop indexes in any schema except `SYS`. |
| INDEXTYPES: | — |
| `CREATE INDEXTYPE` | Create indextypes in the grantee's schema. |
| `CREATE ANY INDEXTYPE` | Create indextypes in any schema except `SYS` and create comments on an indextype in any schema except `SYS`. |
| `ALTER ANY INDEXTYPE` | Modify indextypes in any schema except `SYS`. |
| `DROP ANY INDEXTYPE` | Drop indextypes in any schema except `SYS`. |
| `EXECUTE ANY INDEXTYPE` | Reference indextypes in any schema except `SYS`. |
| JOB SCHEDULER OBJECTS: | The following privileges are needed to execute procedures in the `DBMS_SCHEDULER` package. This privileges do not apply to lightweight jobs, which are not database objects. Refer to [Oracle Database Administrator's Guide](../ADMIN/schedadmin.md#ADMIN035) for more information about lightweight jobs. |
| `CREATE JOB` | Create, alter, or drop jobs, chains, schedules, programs, or credentials in the grantee's schema. |
| `CREATE ANY JOB` | Create, alter, or drop jobs, chains, schedules, programs, or credentials in any schema except `SYS`.  Note: This extremely powerful privilege allows the grantee to execute code as any other user. It should be granted with caution. |
| `CREATE EXTERNAL JOB` | Create in the grantee's schema an executable scheduler job that runs on the operating system. |
| `EXECUTE ANY CLASS` | Specify any job class in a job in the grantee's schema. |
| `EXECUTE ANY PROGRAM` | Use any program in a job in the grantee's schema. |
| `MANAGE SCHEDULER` | Create, alter, or drop any job class, window, or window group. |
| KEY MANAGEMENT FRAMEWORK: | — |
| `ADMINISTER` `KEY` `MANAGEMENT` | Manage keys and keystores. |
| LIBRARIES: | Caution: `CREATE` `LIBARARY`, `CREATE` `ANY` `LIBRARY`, `ALTER` `ANY` `LIBRARY`, and `EXECUTE` `ANY` `LIBRARY` are extremely powerful privileges that should be granted only to trusted users. Refer to [Oracle Database Security Guide](../DBSEG/guidelines.md#DBSEG499) before granting these privileges. |
| `CREATE LIBRARY` | Create external procedure or function libraries in the grantee's schema. |
| `CREATE ANY LIBRARY` | Create external procedure or function libraries in any schema except `SYS`. |
| `ALTER ANY LIBRARY` | Alter external procedure or function libraries in any schema except `SYS`. |
| `DROP ANY LIBRARY` | Drop external procedure or function libraries in any schema except `SYS`. |
| `EXECUTE ANY LIBRARY` | Use external procedure or function libraries in any schema except `SYS`. |
| LOGMINER: | — |
| `LOGMINING` | Execute procedures in the `DBMS_LOGMNR` package in a CDB. Query the contents of the `V$LOGMNR_CONTENTS` view. |
| MATERIALIZED VIEWS: | — |
| `CREATE MATERIALIZED VIEW` | Create a materialized view in the grantee's schema. |
| `CREATE ANY MATERIALIZED VIEW` | Create materialized views in any schema except `SYS`. |
| `ALTER ANY MATERIALIZED VIEW` | Alter materialized views in any schema except `SYS`. |
| `DROP ANY MATERIALIZED VIEW` | Drop materialized views in any schema except `SYS`. |
| `QUERY REWRITE` | This privilege has been deprecated. No privileges are needed for a user to enable rewrite for a materialized view that references tables or views in the user's own schema. |
| `GLOBAL QUERY REWRITE` | Enable rewrite using a materialized view when that materialized view references tables or views in any schema except `SYS`. |
| `ON COMMIT REFRESH` | Create a refresh-on-commit materialized view on any table in the database.  Alter a refresh-on-demand materialized view on any table in the database to refresh-on-commit. |
| `FLASHBACK ANY TABLE` | Issue a SQL Flashback Query on a table, view, or materialized view in any schema except `SYS`. This privilege is not needed to execute the `DBMS_FLASHBACK` procedures. |
| MINING MODELS: | — |
| `CREATE MINING MODEL` | Create mining models in the grantee's schema using the `DBMS_DATA_MINING.CREATE_MODEL` procedure. |
| `CREATE ANY MINING MODEL` | Create mining models in any schema, except `SYS`, using the `DBMS_DATA_MINING.CREATE_MODEL` procedure. |
| `ALTER ANY MINING MODEL` | Change the mining model name or the associated cost matrix of any model in any schema, except `SYS`, using the applicable `DBMS_DATA_MINING` procedures. |
| `DROP ANY MINING MODEL` | Drop mining models in any schema, except `SYS`, using the `DBMS_DATA_MINING.DROP_MODEL` procedure. |
| `SELECT ANY MINING MODEL` | Score or view mining models in any schema except `SYS`. Scoring is done either with the `PREDICTION` family of SQL functions or with the `DBMS_DATA_MINING.APPLY` procedure. Viewing the model is done with the `DBMS_DATA_MINING.GET_MODEL_DETAILS_*` procedures. |
| `COMMENT ANY MINING MODEL` | Create comments on mining models in any schema, except `SYS`, using the SQL `COMMENT` statement. |
| OLAP CUBES: | The following privileges are valid when you are using Oracle Database with the OLAP option. |
| `CREATE CUBE` | Create OLAP cubes in the grantee's schema. |
| `CREATE ANY CUBE` | Create OLAP cubes in any schema except `SYS`. |
| `ALTER ANY CUBE` | Alter OLAP cubes in any schema except `SYS`. |
| `DROP ANY CUBE` | Drop OLAP cubes in any schema except `SYS`. |
| `SELECT ANY CUBE` | Query or view OLAP cubes in any schema except `SYS`. |
| `UPDATE ANY CUBE` | Update OLAP cubes in any schema except `SYS`. |
| OLAP CUBE MEASURE FOLDERS: | The following privileges are valid when you are using Oracle Database with the OLAP option. |
| `CREATE MEASURE FOLDER` | Create OLAP measure folders in the grantee's schema. |
| `CREATE ANY MEASURE FOLDER` | Create OLAP measure folders in any schema except `SYS`. |
| `DELETE ANY MEASURE FOLDER` | Delete a measure from an OLAP measure folder in any schema except `SYS`. |
| `DROP ANY MEASURE FOLDER` | Drop OLAP measure folders in any schema except `SYS`. |
| `INSERT ANY MEASURE FOLDER` | Insert a measure into an OLAP measure folder in any schema except `SYS`. |
| OLAP CUBE DIMENSIONS: | The following privileges are valid when you are using Oracle Database with the OLAP option. |
| `CREATE CUBE DIMENSION` | Create OLAP cube dimensions in the grantee's schema. |
| `CREATE ANY CUBE DIMENSION` | Create OLAP cube dimensions in any schema except `SYS`. |
| `ALTER ANY CUBE DIMENSION` | Alter OLAP cube dimensions in any schema except `SYS`. |
| `DELETE ANY CUBE DIMENSION` | Delete from OLAP cube dimensions in any schema except `SYS`. |
| `DROP ANY CUBE DIMENSION` | Drop OLAP cube dimensions in any schema except `SYS`. |
| `INSERT ANY CUBE DIMENSION` | Insert into OLAP cube dimensions in any schema except `SYS`. |
| `SELECT ANY CUBE DIMENSION` | View or query OLAP cube dimensions in any schema except `SYS`. |
| `UPDATE ANY CUBE DIMENSION` | Update OLAP cube dimensions in any schema except `SYS`. |
| OLAP CUBE BUILD PROCESSES: | — |
| `CREATE CUBE BUILD PROCESS` | Create OLAP cube build processes in the grantee's schema. |
| `CREATE ANY CUBE BUILD PROCESS` | Create OLAP cube build processes in any schema except `SYS`. |
| `DROP ANY CUBE BUILD PROCESS` | Drop OLAP cube build processes in any schema except `SYS`. |
| `UPDATE ANY CUBE BUILD PROCESS` | Update OLAP cube build processes in any schema except `SYS`. |
| OPERATORS: | — |
| `CREATE OPERATOR` | Create an operator and its bindings in the grantee's schema. |
| `CREATE ANY OPERATOR` | Create an operator and its bindings in any schema and create a comment on an operator in any schema. |
| `ALTER ANY OPERATOR` | Modify operators in any schema. |
| `DROP ANY OPERATOR` | Drop operators in any schema. |
| `EXECUTE ANY OPERATOR` | Reference operators in any schema. |
| OUTLINES: | — |
| `CREATE ANY OUTLINE` | Create public outlines that can be used in any schema that uses outlines. |
| `ALTER ANY OUTLINE` | Modify outlines. |
| `DROP ANY OUTLINE` | Drop outlines. |
| PLAN MANAGEMENT: | — |
| `ADMINISTER SQL MANAGEMENT OBJECT` | Perform controlled manipulation of plan history and SQL plan baselines maintained for various SQL statements. |
| PLUGGABLE DATABASES: | — |
| `CREATE` `PLUGGABLE` `DATABASE` | Create a PDB.  Plug in a PDB that was previously unplugged from a CDB.  Clone a PDB. |
| `SET` `CONTAINER` | Allow a common user to switch into the container for which this privilege was granted. This privilege can be granted only to a common user or common role. |
| PROCEDURES: | — |
| `CREATE PROCEDURE` | Create stored procedures, functions, and packages in the grantee's schema. |
| `CREATE ANY PROCEDURE` | Create stored procedures, functions, and packages in any schema except `SYS`. |
| `ALTER ANY PROCEDURE` | Alter stored procedures, functions, or packages in any schema except `SYS`. |
| `DROP ANY PROCEDURE` | Drop stored procedures, functions, or packages in any schema except `SYS`. |
| `EXECUTE ANY PROCEDURE` | Execute procedures or functions, either standalone or packaged.  Reference public package variables in any schema except `SYS`. |
| PROFILES: | — |
| `CREATE PROFILE` | Create profiles. |
| `ALTER PROFILE` | Alter profiles. |
| `DROP PROFILE` | Drop profiles. |
| ROLES: | — |
| `CREATE ROLE` | Create roles. |
| `ALTER ANY ROLE` | Alter any role in the database. |
| `DROP ANY ROLE` | Drop roles. |
| `GRANT ANY ROLE` | Grant any role in the database. |
| ROLLBACK SEGMENTS: | — |
| `CREATE ROLLBACK SEGMENT` | Create rollback segments. |
| `ALTER ROLLBACK SEGMENT` | Alter rollback segments. |
| `DROP ROLLBACK SEGMENT` | Drop rollback segments. |
| SEQUENCES: | — |
| `CREATE SEQUENCE` | Create sequences in the grantee's schema. |
| `CREATE ANY SEQUENCE` | Create sequences in any schema except `SYS`. |
| `ALTER ANY SEQUENCE` | Alter sequences in any schema except `SYS`. |
| `DROP ANY SEQUENCE` | Drop sequences in any schema except `SYS`. |
| `SELECT ANY SEQUENCE` | Reference sequences in any schema except `SYS`. |
| SESSIONS: | — |
| `CREATE SESSION` | Connect to the database. |
| `ALTER RESOURCE COST` | Set costs for session resources. |
| `ALTER SESSION` | Enable and disable the SQL trace facility. |
| `RESTRICTED SESSION` | Logon after the instance is started using the SQL\*Plus `STARTUP` `RESTRICT` statement. |
| SNAPSHOTS: | See `MATERIALIZED` `VIEWS` |
| SQL TRANSLATION PROFILES: | — |
| `CREATE` `SQL` `TRANSLATION` `PROFILE` | Create SQL translation profiles in the grantee's schema. |
| `CREATE` `ANY` `SQL` `TRANSLATION` `PROFILE` | Create SQL translation profiles in any schema except `SYS`. |
| `ALTER` `ANY` `SQL` `TRANSLATION` `PROFILE` | Alter the translator, custom SQL statement translations, or custom error translations of a SQL translation profile in any schema except `SYS`. |
| `USE` `ANY` `SQL` `TRANSLATION` `PROFILE` | Use SQL translation profiles in any schema except `SYS`. |
| `DROP` `ANY` `SQL` `TRANSLATION` `PROFILE` | Drop SQL translation profiles in any schema except `SYS`. |
| `TRANSLATE` `ANY` `SQL` | Translate SQL through the grantee's SQL translation profile for any user. |
| SYNONYMS: | Caution: `CREATE` `PUBLIC` `SYNONYM` and `DROP` `PUBLIC` `SYNONYM` are extremely powerful privileges that should be granted only to trusted users. Refer to [Oracle Database Security Guide](../DBSEG/guidelines.md#DBSEG499) before granting these privileges. |
| `CREATE SYNONYM` | Create synonyms in the grantee's schema. |
| `CREATE ANY SYNONYM` | Create private synonyms in any schema except `SYS`. |
| `CREATE PUBLIC SYNONYM` | Create public synonyms. |
| `DROP ANY SYNONYM` | Drop private synonyms in any schema except `SYS`. |
| `DROP PUBLIC SYNONYM` | Drop public synonyms. |
| TABLES: | Note: For external tables, the only valid privileges are `CREATE` `ANY` `TABLE`, `ALTER` `ANY` `TABLE`, `DROP` `ANY` `TABLE`, `READ` `ANY` `TABLE`, and `SELECT` `ANY` `TABLE`. |
| `CREATE TABLE` | Create tables in the grantee's schema. |
| `CREATE ANY TABLE` | Create tables in any schema except `SYS`. The owner of the schema containing the table must have space quota on the tablespace to contain the table. |
| `ALTER ANY TABLE` | Alter a table or view in any schema except `SYS`. |
| `BACKUP ANY TABLE` | Use the Export utility to incrementally export objects from the schema of other users except `SYS`. |
| `DELETE ANY TABLE` | Delete rows from tables, table partitions, or views in any schema except `SYS`. |
| `DROP ANY TABLE` | Drop or truncate tables or table partitions in any schema except `SYS`. |
| `INSERT ANY TABLE` | Insert rows into tables and views in any schema except `SYS`. |
| `LOCK ANY TABLE` | Lock tables and views in any schema except `SYS`. |
| `READ` `ANY` `TABLE` | Query tables, views, or materialized views in any schema except `SYS`.  Note: This privilege is available starting with Oracle Database 12c Release 1 (12.1.0.2). |
| `SELECT ANY TABLE` | Query tables, views, or materialized views in any schema except `SYS`. Obtain row locks using a `SELECT` ... `FOR` `UPDATE`. |
| `FLASHBACK ANY TABLE` | Issue a SQL Flashback Query on any table, view, or materialized view in any schema except `SYS`. This privilege is not needed to execute the `DBMS_FLASHBACK` procedures. |
| `UPDATE ANY TABLE` | Update rows in tables and views in any schema except `SYS`. |
| TABLESPACES: | — |
| `CREATE TABLESPACE` | Create tablespaces. |
| `ALTER TABLESPACE` | Alter tablespaces. |
| `DROP TABLESPACE` | Drop tablespaces. |
| `MANAGE TABLESPACE` | Take tablespaces offline and online and begin and end tablespace backups. |
| `UNLIMITED TABLESPACE` | Use an unlimited amount of any tablespace. This privilege overrides any specific quotas assigned. If you revoke this privilege from a user, then the user's schema objects remain but further tablespace allocation is denied unless authorized by specific tablespace quotas. You cannot grant this system privilege to roles. |
| TRIGGERS: | — |
| `CREATE TRIGGER` | Create database triggers in the grantee's schema. |
| `CREATE ANY TRIGGER` | Create database triggers in any schema except `SYS`. |
| `ALTER ANY TRIGGER` | Enable, disable, or compile database triggers in any schema except `SYS`. |
| `DROP ANY TRIGGER` | Drop database triggers in any schema except `SYS`. |
| `ADMINISTER DATABASE TRIGGER` | Create a trigger on `DATABASE`. You must also have the `CREATE` `TRIGGER` or `CREATE` `ANY` `TRIGGER` system privilege. |
| TYPES: | — |
| `CREATE TYPE` | Create object types and object type bodies in the grantee's schema. |
| `CREATE ANY TYPE` | Create object types and object type bodies in any schema except `SYS`. |
| `ALTER ANY TYPE` | Alter object types in any schema except `SYS`. |
| `DROP ANY TYPE` | Drop object types and object type bodies in any schema except `SYS`. |
| `EXECUTE ANY TYPE` | Use and reference object types and collection types in any schema, except `SYS`, and invoke methods of an object type in any schema, except `SYS`, if you make the grant to a specific user. If you grant `EXECUTE` `ANY` `TYPE` to a role, then users holding the enabled role will not be able to invoke methods of an object type in any schema. |
| `UNDER ANY TYPE` | Create subtypes under any nonfinal object types. |
| USERS: | — |
| `CREATE USER` | Create users. This privilege also allows the creator to:   * Assign quotas on any tablespace. * Set default and temporary tablespaces. * Assign a profile as part of a `CREATE` `USER` statement. |
| `ALTER USER` | Alter any user. This privilege authorizes the grantee to:   * Change another user's password or authentication method. * Assign quotas on any tablespace. * Set default and temporary tablespaces. * Assign a profile and default roles. |
| `DROP USER` | Drop users |
| VIEWS: | — |
| `CREATE VIEW` | Create views in the grantee's schema. |
| `CREATE ANY VIEW` | Create views in any schema except `SYS`. |
| `DROP ANY VIEW` | Drop views in any schema except `SYS`. |
| `UNDER ANY VIEW` | Create subviews under any object views. |
| `FLASHBACK ANY TABLE` | Issue a SQL Flashback Query on any table, view, or materialized view in any schema except `SYS`. This privilege is not needed to execute the `DBMS_FLASHBACK` procedures. |
| `MERGE ANY VIEW` | If a user has been granted the `MERGE` `ANY` `VIEW` privilege, then for any query issued by that user, the optimizer can use view merging to improve query performance without performing the checks that would otherwise be performed to ensure that view merging does not violate any security intentions of the view creator. See also Oracle Database Reference for information on the [`OPTIMIZER_SECURE_VIEW_MERGING`](../REFRN/GUID-08F07A0F-44C0-4DA6-B5F3-790F8C05980A.md#REFRN10262) parameter and [Oracle Database SQL Tuning Guide](../TGSQL/tgsql_transform.md#TGSQL209) for information on view merging. |
| MISCELLANEOUS: | — |
| `ANALYZE ANY` | Analyze a table, cluster, or index in any schema except `SYS`. |
| `AUDIT ANY` | Audit an object in any schema, except `SYS`, using `AUDIT` `schema_objects` statements. |
| `BECOME` `USER` | Allow users of the Data Pump Import utility (impdp) and the original Import utility (imp) to assume the identity of another user in order to perform operations that cannot be directly performed by a third party (for example, loading objects such as object privilege grants).  Allow Streams administrators to create or alter capture users and apply users in a Streams environment. By default this privilege is part of the DBA role. Database Vault removes this privileges from the DBA role. Therefore, this privilege is needed by Streams only in an environment where Database Vault is installed. |
| `CHANGE` `NOTIFICATION` | Create a registration on queries and receive database change notifications in response to DML or DDL changes to the objects associated with the registered queries. Refer to [Oracle Database Development Guide](../ADFNS/adfns_cqn.md#ADFNS018) for more information on database change notification. |
| `COMMENT ANY TABLE` | Comment on a table, view, or column in any schema except `SYS`. |
| `EXEMPT ACCESS POLICY` | Bypass fine-grained access control.  Caution: This is a very powerful system privilege, as it lets the grantee bypass application-driven security policies. Database administrators should use caution when granting this privilege. |
| `FORCE ANY TRANSACTION` | Force the commit or rollback of any in-doubt distributed transaction in the local database.  Induce the failure of a distributed transaction. |
| `FORCE TRANSACTION` | Force the commit or rollback of the grantee's in-doubt distributed transactions in the local database. |
| `GRANT` `ANY` `OBJECT` `PRIVILEGE` | Grant any object privilege that the object owner is permitted to grant.  Revoke any object privilege that was granted by the object owner or by some other user with the `GRANT` `ANY` `OBJECT` `PRIVILEGE` privilege. |
| `GRANT ANY PRIVILEGE` | Grant any system privilege. |
| `INHERIT` `ANY` `PRIVILEGES` | Execute invoker's rights procedures owned by the grantee with the privileges of the invoker. |
| `KEEP` `DATE` `TIME` | The `SYSDATE` and `SYSTIMESTAMP` functions return their original values during replay for Application Continuity when the grantee is running the application. This privilege is useful for providing bind variable consistency after recoverable errors.  Note: If this privilege is granted or revoked between runtime and failover of a request, then the original values are not returned during replay for Application Continuity for that request. |
| `KEEP` `SYSGUID` | The `SYS_GUID` function returns its original value during replay for Application Continuity when the grantee is running the application. This privilege is useful for providing bind variable consistency after recoverable errors.  Note: If this privilege is granted or revoked between runtime and failover of a request, then the original value is not returned during replay for Application Continuity for that request. |
| `PURGE` `DBA_RECYCLEBIN` | Remove all objects from the system-wide recycle bin. |
| `RESUMABLE` | Enable resumable space allocation. |
| `SELECT ANY DICTIONARY` | Query any data dictionary object in the `SYS` schema, with the exception of the following objects: `DEFAULT_PWD$`, `ENC$`, `LINK$`, `USER$`, `USER_HISTORY$`, and `XS$VERIFIERS`.  This privilege lets you selectively override the default `FALSE` setting of the `O7_DICTIONARY_ACCESSIBILITY` initialization parameter. |
| `SELECT ANY TRANSACTION` | Query the contents of the `FLASHBACK_TRANSACTION_QUERY` view.  Caution: This is a very powerful system privilege, as it lets the grantee view all data in the database, including past data. This privilege should be granted only to users who need to use the Oracle Flashback Transaction Query feature. |
| `SYSBACKUP` | Perform the following backup and recovery operations:  `STARTUP` and `SHUTDOWN`.  `CREATE` `CONTROLFILE`.  `CREATE` `PFILE` and `CREATE` `SPFILE`.  `FLASHBACK` `DATABASE`.  Create, use, view, and drop restore points (including guaranteed restore points).  Execute procedures in the `DBMS_DATAPUMP`, `DBMS_PIPE`, `DBMS_TDB`, and `DBMS_TTS` packages.  `SELECT` on `X$` tables, `V$` views, and `GV$` views.  Includes the `ALTER` `DATABASE`, `ALTER` `SESSION`, `ALTER` `SYSTEM`, `ALTER` `TABLESPACE`, `CREATE` `ANY` `CLUSTER`, `CREATE` `ANY` `DIRECTORY`, `CREATE` `ANY` `TABLE`, `CREATE` `SESSION`, `DROP` `DATABASE`, `DROP` `TABLESPACE`, `RESUMABLE`, `SELECT` `ANY` `DICTIONARY`, `SELECT` `ANY` `TRANSACTION`, `UNLIMITED` `TABLESPACE` privileges and the `SELECT_CATALOG_ROLE` role. |
| `SYSDBA` | `STARTUP` and `SHUTDOWN`.  `ALTER` `DATABASE`: open, mount, back up, or change character set.  `CREATE` `DATABASE`.  `DROP` `DATABASE`.  `ARCHIVELOG` and `RECOVERY`.  `CREATE` `SPFILE`.  Includes the `RESTRICTED` `SESSION` privilege. |
| `SYSDG` | Perform the following Oracle Data Guard operations:  `STARTUP` and `SHUTDOWN`.  `FLASHBACK` `DATABASE`.  Create, use, view, and drop restore points (including guaranteed restore points).  `SELECT` on `X$` tables, `V$` views, and `GV$` views.  Includes the `ALTER` `DATABASE`, `ALTER` `SESSION`, `ALTER` `SYSTEM`, `CREATE` `SESSION`, and `SELECT` `ANY` `DICTIONARY` privileges. |
| `SYSKM` | Perform the following encryption key management operations:  Connect to the database even if the database is not open.  `SELECT` on the following views when the database is open: `V$CLIENT_SECRETS`, `V$ENCRYPTED_TABLESPACES`, `V$ENCRYPTION_KEYS`, `V$ENCRYPTION_WALLET` and `V$WALLET`.  Includes the `ADMINISTER` `KEY` `MANAGEMENT` and `CREATE` `SESSION` privileges. |
| `SYSOPER` | `STARTUP` and `SHUTDOWN` operations.  `ALTER` `DATABASE`: open, mount, or back up.  `ARCHIVELOG` and `RECOVERY`.  `CREATE` `SPFILE`.  Includes the `RESTRICTED` `SESSION` privilege. |