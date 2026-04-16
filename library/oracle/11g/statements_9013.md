# Oracle 11g - statements_9013
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/statements_9013.htm

|  |  |
| --- | --- |
| Advisor Framework Privileges: All of the advisor framework privileges are part of the DBA role. | — |
| `ADVISOR` | Access the advisor framework through PL/SQL packages such as `DBMS_ADVISOR` and `DBMS_SQLTUNE`.  Refer to [Oracle Database PL/SQL Packages and Types Reference](../../appdev.112/e40758/toc.md) for information on these packages. |
| `ADMINISTER SQL TUNING SET` | Create, drop, select (read), load (write), and delete a SQL tuning set owned by the grantee through the `DBMS_SQLTUNE` package. |
| `ADMINISTER ANY SQL TUNING SET` | Create, drop, select (read), load (write), and delete a SQL tuning set owned by any user through the `DBMS_SQLTUNE` package. |
| `CREATE ANY SQL PROFILE` | Accept a SQL Profile recommended by the SQL Tuning Advisor, which is accessed through Enterprise Manager or by the `DBMS_SQLTUNE` package.  Note: This privilege has been deprecated in favor of `ADMINISTER` `SQL` `MANAGEMENT` `OBJECT`. |
| `ALTER ANY SQL PROFILE` | Alter the attributes of an existing SQL Profile.  Note: This privilege has been deprecated in favor of `ADMINISTER` `SQL` `MANAGEMENT` `OBJECT`. |
| `DROP ANY SQL PROFILE` | Drop an existing SQL Profile.  Note: This privilege has been deprecated in favor of `ADMINISTER` `SQL` `MANAGEMENT` `OBJECT`. |
| `ADMINISTER SQL MANAGEMENT OBJECT` | Create, alter, and drop a SQL Profile owned by any user through the `DBMS_SQLTUNE` package. |
| CLUSTERS: | — |
| `CREATE CLUSTER` | Create clusters in the grantee's schema. |
| `CREATE ANY CLUSTER` | Create a cluster in any schema. Behaves similarly to `CREATE` `ANY` `TABLE`. |
| `ALTER ANY CLUSTER` | Alter clusters in any schema. |
| `DROP ANY CLUSTER` | Drop clusters in any schema. |
| CONTEXTS: | — |
| `CREATE ANY CONTEXT` | Create any context namespace. |
| `DROP ANY CONTEXT` | Drop any context namespace. |
| DATA REDACTION: | — |
| `EXEMPT REDACTION POLICY` | Bypass any existing Oracle Data Redaction policies and view actual data from tables or views on which Data Redaction policies are defined.  Note: This privilege is available starting with Oracle Database 11g Release 2 (11.2.0.4). |
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
| `CREATE ANY DIMENSION` | Create dimensions in any schema. |
| `ALTER ANY DIMENSION` | Alter dimensions in any schema. |
| `DROP ANY DIMENSION` | Drop dimensions in any schema. |
| DIRECTORIES: | — |
| `CREATE ANY DIRECTORY` | Create directory database objects. |
| `DROP ANY DIRECTORY` | Drop directory database objects. |
| EDITIONS: | — |
| `CREATE ANY EDITION` | Create editions. |
| `DROP ANY EDITION` | Drop editions. |
| FLASHBACK DATA ARCHIVES: | — |
| `FLASHBACK` `ARCHIVE` `ADMINISTER` | Create, alter, or drop any flashback data archive. |
| INDEXES: | — |
| `CREATE ANY INDEX` | Create in any schema a domain index or an index on any table in any schema. |
| `ALTER ANY INDEX` | Alter indexes in any schema. |
| `DROP ANY INDEX` | Drop indexes in any schema. |
| INDEXTYPES: | — |
| `CREATE INDEXTYPE` | Create an indextype in the grantee's schema. |
| `CREATE ANY INDEXTYPE` | Create an indextype in any schema and create a comment on an indextype in any schema. |
| `ALTER ANY INDEXTYPE` | Modify indextypes in any schema. |
| `DROP ANY INDEXTYPE` | Drop an indextype in any schema. |
| `EXECUTE ANY INDEXTYPE` | Reference an indextype in any schema. |
| JOB SCHEDULER OBJECTS: | The following privileges are needed to execute procedures in the `DBMS_SCHEDULER` package. This privileges do not apply to lightweight jobs, which are not database objects. Refer to [Oracle Database Administrator's Guide](../../server.112/e25494/schedadmin.md#ADMIN035) for more information about lightweight jobs. |
| `CREATE JOB` | Create jobs, schedules, or programs in the grantee's schema. |
| `CREATE ANY JOB` | Create, alter, or drop jobs, chains, schedules, programs, or credentials in any schema except `SYS`.  Caution: This extremely powerful privilege allows the grantee to execute code as any other user. It should be granted with caution. |
| `CREATE EXTERNAL JOB` | Create in the grantee's schema an executable scheduler job that runs on the operating system. |
| `EXECUTE ANY PROGRAM` | Use any program in a job in the grantee's schema. |
| `EXECUTE ANY CLASS` | Specify any job class in a job in the grantee's schema. |
| `MANAGE SCHEDULER` | Create, alter, or drop any job class, window, or window group. |
| LIBRARIES: | Caution: `CREATE` `LIBARARY`, `CREATE` `ANY` `LIBRARY`, `ALTER` `ANY` `LIBRARY`, and `EXECUTE` `ANY` `LIBRARY` are extremely powerful privileges that should be granted only to trusted users. Refer to [Oracle Database Security Guide](../../network.112/e36292/guidelines.md#DBSEG499) before granting these privileges. |
| `CREATE LIBRARY` | Create external procedure or function libraries in the grantee's schema. |
| `CREATE ANY LIBRARY` | Create external procedure or function libraries in any schema. |
| `ALTER ANY LIBRARY` | Alter external procedure or function libraries in any schema. |
| `DROP ANY LIBRARY` | Drop external procedure or function libraries in any schema. |
| `EXECUTE ANY LIBRARY` | Use external procedure or function libraries in any schema. |
| MATERIALIZED VIEWS: | — |
| `CREATE MATERIALIZED VIEW` | Create a materialized view in the grantee's schema. |
| `CREATE ANY MATERIALIZED VIEW` | Create materialized views in any schema. |
| `ALTER ANY MATERIALIZED VIEW` | Alter materialized views in any schema. |
| `DROP ANY MATERIALIZED VIEW` | Drop materialized views in any schema. |
| `QUERY REWRITE` | This privilege has been deprecated. No privileges are needed for a user to enable rewrite for a materialized view that references tables or views in the user's own schema. |
| `GLOBAL QUERY REWRITE` | Enable rewrite using a materialized view when that materialized view references tables or views in any schema. |
| `ON COMMIT REFRESH` | Create a refresh-on-commit materialized view on any table in the database.  Alter a refresh-on-demand materialized on any table in the database to refresh-on-commit. |
| `FLASHBACK ANY TABLE` | Issue a SQL Flashback Query on any table, view, or materialized view in any schema. This privilege is not needed to execute the `DBMS_FLASHBACK` procedures. |
| MINING MODELS: | — |
| `CREATE MINING MODEL` | Create mining models in the grantee's schema using the `DBMS_DATA_MINING.CREATE_MODEL` procedure. |
| `CREATE ANY MINING MODEL` | Create mining models in any schema using the `DBMS_DATA_MINING.CREATE_MODEL` procedure. |
| `ALTER ANY MINING MODEL` | Change the mining model name or the associated cost matrix of any model in any schema by using the applicable `DBMS_DATA_MINING` procedures. |
| `DROP ANY MINING MODEL` | Drop any mining model in any schema by using the `DBMS_DATA_MINING.DROP_MODEL` procedure. |
| `SELECT ANY MINING MODEL` | Score or view any model in any schema. Scoring is done either with the `PREDICTION` family of SQL functions or with the `DBMS_DATA_MINING.APPLY` procedure. Viewing the model is done with the `DBMS_DATA_MINING.GET_MODEL_DETAILS_*` procedures. |
| `COMMENT ANY MINING MODEL` | Create a comment on any model in any schema using the SQL `COMMENT` statement. |
| OLAP CUBES: | The following privileges are valid when you are using Oracle Database with the OLAP option. |
| `CREATE CUBE` | Create an OLAP cube in the grantee's schema. |
| `CREATE ANY CUBE` | Create an OLAP cube in any schema. |
| `ALTER ANY CUBE` | Alter an OLAP cube in any schema. |
| `DROP ANY CUBE` | Drop any OLAP cube in any schema. |
| `SELECT ANY CUBE` | Query or view any OLAP cube in any schema. |
| `UPDATE ANY CUBE` | Update any cube in any schema. |
| OLAP CUBE MEASURE FOLDERS: | The following privileges are valid when you are using Oracle Database with the OLAP option. |
| `CREATE MEASURE FOLDER` | Create an OLAP measure folder in the grantee's schema. |
| `CREATE ANY MEASURE FOLDER` | Create an OLAP measure folder in any schema. |
| `DELETE ANY MEASURE FOLDER` | Delete from any OLAP measure folder in any schema. |
| `DROP ANY MEASURE FOLDER` | Drop any measure folder in any schema. |
| `INSERT ANY MEASURE FOLDER` | Insert a measure into any measure folder in any schema. |
| OLAP CUBE DIMENSIONS: | The following privileges are valid when you are using Oracle Database with the OLAP option. |
| `CREATE CUBE DIMENSION` | Create an OLAP cube dimension in the grantee's schema. |
| `CREATE ANY CUBE DIMENSION` | Create an OLAP cube dimension in any schema. |
| `ALTER ANY CUBE DIMENSION` | Alter an OLAP cube dimension in any schema. |
| `DELETE ANY CUBE DIMENSION` | Delete from an OLAP cube dimension in any schema. |
| `DROP ANY CUBE DIMENSION` | Drop an OLAP cube dimension in any schema. |
| `INSERT ANY CUBE DIMENSION` | Insert into an OLAP cube dimension in any schema. |
| `SELECT ANY CUBE DIMENSION` | View or query an OLAP cube dimension in any schema. |
| `UPDATE ANY CUBE DIMENSION` | Update an OLAP cube dimension in any schema. |
| OLAP CUBE BUILD PROCESSES: | — |
| `CREATE CUBE BUILD PROCESS` | Create an OLAP cube build process in the grantee's schema. |
| `CREATE ANY CUBE BUILD PROCESS` | Create an OLAP cube build process in any schema. |
| `DROP ANY CUBE BUILD PROCESS` | Drop an OLAP cube build process in any schema. |
| `UPDATE ANY CUBE BUILD PROCESS` | Update an OLAP cube build process in any schema. |
| OPERATORS: | — |
| `CREATE OPERATOR` | Create an operator and its bindings in the grantee's schema. |
| `CREATE ANY OPERATOR` | Create an operator and its bindings in any schema and create a comment on an operator in any schema. |
| `ALTER ANY OPERATOR` | Modify an operator in any schema. |
| `DROP ANY OPERATOR` | Drop an operator in any schema. |
| `EXECUTE ANY OPERATOR` | Reference an operator in any schema. |
| OUTLINES: | — |
| `CREATE ANY OUTLINE` | Create public outlines that can be used in any schema that uses outlines. |
| `ALTER ANY OUTLINE` | Modify outlines. |
| `DROP ANY OUTLINE` | Drop outlines. |
| PLAN MANAGEMENT: | — |
| `ADMINISTER SQL MANAGEMENT OBJECT` | Perform controlled manipulation of plan history and SQL plan baselines maintained for various SQL statements. |
| PROCEDURES: | — |
| `CREATE PROCEDURE` | Create stored procedures, functions, and packages in the grantee's schema. |
| `CREATE ANY PROCEDURE` | Create stored procedures, functions, and packages in any schema. |
| `ALTER ANY PROCEDURE` | Alter stored procedures, functions, or packages in any schema. |
| `DROP ANY PROCEDURE` | Drop stored procedures, functions, or packages in any schema. |
| `EXECUTE ANY PROCEDURE` | Execute procedures or functions, either standalone or packaged.  Reference public package variables in any schema. |
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
| `CREATE ANY SEQUENCE` | Create sequences in any schema. |
| `ALTER ANY SEQUENCE` | Alter any sequence in the database. |
| `DROP ANY SEQUENCE` | Drop sequences in any schema. |
| `SELECT ANY SEQUENCE` | Reference sequences in any schema. |
| SESSIONS: | — |
| `CREATE SESSION` | Connect to the database. |
| `ALTER RESOURCE COST` | Set costs for session resources. |
| `ALTER SESSION` | Enable and disable the SQL trace facility. |
| `RESTRICTED SESSION` | Logon after the instance is started using the SQL\*Plus `STARTUP` `RESTRICT` statement. |
| SNAPSHOTS: | See `MATERIALIZED` `VIEWS` |
| SYNONYMS: | Caution: `CREATE` `PUBLIC` `SYNONYM` and `DROP` `PUBLIC` `SYNONYM` are extremely powerful privileges that should be granted only to trusted users. Refer to [Oracle Database Security Guide](../../network.112/e36292/guidelines.md#DBSEG499) before granting these privileges. |
| `CREATE SYNONYM` | Create synonyms in the grantee's schema. |
| `CREATE ANY SYNONYM` | Create private synonyms in any schema. |
| `CREATE PUBLIC SYNONYM` | Create public synonyms. |
| `DROP ANY SYNONYM` | Drop private synonyms in any schema. |
| `DROP PUBLIC SYNONYM` | Drop public synonyms. |
| TABLES: | Note: For external tables, the only valid privileges are `CREATE` `ANY` `TABLE`, `ALTER` `ANY` `TABLE`, `DROP` `ANY` `TABLE`, and `SELECT` `ANY` `TABLE`. |
| `CREATE TABLE` | Create a table in the grantee's schema. |
| `CREATE ANY TABLE` | Create a table in any schema. The owner of the schema containing the table must have space quota on the tablespace to contain the table. |
| `ALTER ANY TABLE` | Alter any table or view in any schema. |
| `BACKUP ANY TABLE` | Use the Export utility to incrementally export objects from the schema of other users. |
| `DELETE ANY TABLE` | Delete rows from tables, table partitions, or views in any schema. |
| `DROP ANY TABLE` | Drop or truncate tables or table partitions in any schema. |
| `INSERT ANY TABLE` | Insert rows into tables and views in any schema. |
| `LOCK ANY TABLE` | Lock tables and views in any schema. |
| `SELECT ANY TABLE` | Query tables, views, or materialized views in any schema. |
| `FLASHBACK ANY TABLE` | Issue a SQL Flashback Query on any table, view, or materialized view in any schema. This privilege is not needed to execute the `DBMS_FLASHBACK` procedures. |
| `UPDATE ANY TABLE` | Update rows in tables and views in any schema. |
| TABLESPACES: | — |
| `CREATE TABLESPACE` | Create tablespaces. |
| `ALTER TABLESPACE` | Alter tablespaces. |
| `DROP TABLESPACE` | Drop tablespaces. |
| `MANAGE TABLESPACE` | Take tablespaces offline and online and begin and end tablespace backups. |
| `UNLIMITED TABLESPACE` | Use an unlimited amount of any tablespace. This privilege overrides any specific quotas assigned. If you revoke this privilege from a user, then the user's schema objects remain but further tablespace allocation is denied unless authorized by specific tablespace quotas. You cannot grant this system privilege to roles. |
| TRIGGERS: | — |
| `CREATE TRIGGER` | Create a database trigger in the grantee's schema. |
| `CREATE ANY TRIGGER` | Create database triggers in any schema. |
| `ALTER ANY TRIGGER` | Enable, disable, or compile database triggers in any schema. |
| `DROP ANY TRIGGER` | Drop database triggers in any schema. |
| `ADMINISTER DATABASE TRIGGER` | Create a trigger on `DATABASE`. You must also have the `CREATE` `TRIGGER` or `CREATE` `ANY` `TRIGGER` system privilege. |
| TYPES: | — |
| `CREATE TYPE` | Create object types and object type bodies in the grantee's schema. |
| `CREATE ANY TYPE` | Create object types and object type bodies in any schema. |
| `ALTER ANY TYPE` | Alter object types in any schema. |
| `DROP ANY TYPE` | Drop object types and object type bodies in any schema. |
| `EXECUTE ANY TYPE` | Use and reference object types and collection types in any schema, and invoke methods of an object type in any schema if you make the grant to a specific user. If you grant `EXECUTE` `ANY` `TYPE` to a role, then users holding the enabled role will not be able to invoke methods of an object type in any schema. |
| `UNDER ANY TYPE` | Create subtypes under any nonfinal object types. |
| USERS: | — |
| `CREATE USER` | Create users. This privilege also allows the creator to:   * Assign quotas on any tablespace. * Set default and temporary tablespaces. * Assign a profile as part of a `CREATE` `USER` statement. |
| `ALTER USER` | Alter any user. This privilege authorizes the grantee to:   * Change another user's password or authentication method. * Assign quotas on any tablespace. * Set default and temporary tablespaces. * Assign a profile and default roles. |
| `DROP USER` | Drop users |
| VIEWS: | — |
| `CREATE VIEW` | Create views in the grantee's schema. |
| `CREATE ANY VIEW` | Create views in any schema. |
| `DROP ANY VIEW` | Drop views in any schema. |
| `UNDER ANY VIEW` | Create subviews under any object views. |
| `FLASHBACK ANY TABLE` | Issue a SQL Flashback Query on any table, view, or materialized view in any schema. This privilege is not needed to execute the `DBMS_FLASHBACK` procedures. |
| `MERGE ANY VIEW` | If a user has been granted the `MERGE` `ANY` `VIEW` privilege, then for any query issued by that user, the optimizer can use view merging to improve query performance without performing the checks that would otherwise be performed to ensure that view merging does not violate any security intentions of the view creator. See also Oracle Database Reference for information on the [`OPTIMIZER_SECURE_VIEW_MERGING`](../../server.112/e40402/initparams172.md#REFRN10262) parameter and [Oracle Database Performance Tuning Guide](../../server.112/e41573/optimops.md#PFGRF001) for information on view merging. |
| MISCELLANEOUS: | — |
| `ANALYZE ANY` | Analyze any table, cluster, or index in any schema. |
| `AUDIT ANY` | Audit any object in any schema using `AUDIT` `schema_objects` statements. |
| `BECOME` `USER` | Allows users of the Data Pump Import utility (impdp) and the original Import utility (imp) to assume the identity of another user in order to perform operations that cannot be directly performed by a third party (for example, loading objects such as object privilege grants).  Allows Streams administrators to create or alter capture users and apply users in a Streams environment. By default this privilege is part of the DBA role. Database Vault removes this privileges from the DBA role. Therefore, this privilege is needed by Streams only in an environment where Database Vault is installed. |
| `CHANGE` `NOTIFICATION` | Create a registration on queries and receive database change notifications in response to DML or DDL changes to the objects associated with the registered queries. Refer to [Oracle Database Advanced Application Developer's Guide](../../appdev.112/e41502/adfns_cqn.md#ADFNS018) for more information on database change notification. |
| `COMMENT ANY TABLE` | Comment on any table, view, or column in any schema. |
| `EXEMPT ACCESS POLICY` | Bypass fine-grained access control.  Caution: This is a very powerful system privilege, as it lets the grantee bypass application-driven security policies. Database administrators should use caution when granting this privilege. |
| `FORCE ANY TRANSACTION` | Force the commit or rollback of any in-doubt distributed transaction in the local database.  Induce the failure of a distributed transaction. |
| `FORCE TRANSACTION` | Force the commit or rollback of the grantee's in-doubt distributed transactions in the local database. |
| `GRANT` `ANY` `OBJECT` `PRIVILEGE` | Grant any object privilege that the object owner is permitted to grant.  Revoke any object privilege that was granted by the object owner or by some other user with the `GRANT` `ANY` `OBJECT` `PRIVILEGE` privilege. |
| `GRANT ANY PRIVILEGE` | Grant any system privilege. |
| `RESUMABLE` | Enable resumable space allocation. |
| `SELECT ANY DICTIONARY` | Query any data dictionary object in the `SYS` schema. This privilege lets you selectively override the default `FALSE` setting of the `O7_DICTIONARY_ACCESSIBILITY` initialization parameter. |
| `SELECT ANY TRANSACTION` | Query the contents of the `FLASHBACK_TRANSACTION_QUERY` view.  Caution: This is a very powerful system privilege, as it lets the grantee view all data in the database, including past data. This privilege should be granted only to users who need to use the Oracle Flashback Transaction Query feature. |
| `SYSDBA` | Perform `STARTUP` and `SHUTDOWN` operations.  `ALTER` `DATABASE`: open, mount, back up, or change character set.  `CREATE` `DATABASE`.  `ARCHIVELOG` and `RECOVERY`.  `CREATE` `SPFILE`.  Includes the `RESTRICTED` `SESSION` privilege. |
| `SYSOPER` | Perform `STARTUP` and `SHUTDOWN` operations.  `ALTER` `DATABASE`: open, mount, or back up.  `ARCHIVELOG` and `RECOVERY`.  `CREATE` `SPFILE`.  Includes the `RESTRICTED` `SESSION` privilege. |