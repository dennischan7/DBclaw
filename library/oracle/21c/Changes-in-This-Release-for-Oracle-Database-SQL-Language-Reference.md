# Oracle 21c - Changes-in-This-Release-for-Oracle-Database-SQL-Language-Reference
Source: https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/Changes-in-This-Release-for-Oracle-Database-SQL-Language-Reference.html

The following features are new in Release 21c:

ALTER TABLE MOVE for Partitioned and Subpartitioned Heap-Organized Tables

You can move all the partitions and subpartitions of a partitioned heap-organized table with a single `ALTER TABLE MOVE` statement.

SecureFiles Defragmentation

With release 21c, you can use the `shrink_clause` of the `ALTER TABLE` statement to modify SecureFile LOB segments.

Standby CDB continuity

You can use the `pdb_managed_recovery` clause of the `ALTER PLUGGABLE DATABASE` statement to recover a PDB in instances where the PDB is within a physical standby CDB.

Auditing for Oracle XML DB HTTP and FTP Services

You can use the `PROTOCOL` component of `CREATE AUDIT POLICY` to audit FTP and HTTP messages.

Unified Audit Policies Enforced on the Current User

The unified audit policy created with `CREATE AUDIT POLICY` becomes active immediately for the current session and subsequent sessions as soon as the `AUDIT POLICY` statement is executed.

New DIRECTORY\_DATASTORE Data Store Type for Oracle Text

You can use a new data store type called `DIRECTORY_DATASTORE` instead of the `FILE_DATASTORE` data type. `DIRECTORY_DATASTORE` provides greater security because it enables file access to be based on directory objects.

`FILE_DATASTORE` is deprecated.

New NETWORK\_DATASTORE Data Store Type for Oracle Text

You can use a new data store type called `NETWORK_DATASTORE` instead of the `URL_DATASTORE` data type. `NETWORK_DATASTORE` provides greater security because it enables file access to be based on directory objects.

`URL_DATASTORE` is deprecated.

Automatic In-Memory Management Enhancements

Automatic In-Memory Management enables, populates, evicts, and recompresses segments without user intervention.

Specify `MEMCOMPRESS` `AUTO` in the `inmemory_memcompress` clause to instruct the database to manage the segment.

Oracle Blockchain Table

Blockchain tables enable you to implement a centralized ledger model where all participants in the blockchain network have access to the same tamper-resistant ledger. You can create blockchain tables with the `CREATE TABLE` statement.

Active Data Guard - Standby Result Cache

The result cache in an Active Data Guard standby database is utilized to cache results of queries that were run on the physical standby database. You can enable `STANDBY` in the `result_cache_clause` .

In-Memory Full Text Columns

You can apply the `INMEMORY TEXT` clause to non-scalar columns in an In-Memory table. This clause enables fast In-Memory searching of text, XML, or JSON documents using the `CONTAINS()` or`JSON_TEXTCONTAINS ()` operators .

SQL Macros

You can create SQL Macros (SQM) to factor out common SQL expressions and statements into reusable, parameterized constructs that can be used in other SQL statements. SQL macros can either be scalar expressions, typically used in `SELECT` lists, `WHERE`, `GROUPBY` and `HAVING` clauses, to encapsulate calculations and business logic or can be table expressions, typically used in a `FROM` clause.

SQL macros increase developer productivity, simplify collaborative development, and improve code quality.

Unicode 12.1 Support

Oracle Database 21c complies with version 12.1 of the Unicode Standard.

Bitwise Aggregate Functions

The new aggregate functions `BIT_AND_AGG`, `BIT_OR_AGG`, and `BIT_XOR_ADD` enable bitwise aggregation of integer columns and columns that can be converted or rounded to integer values.

New Analytical and Statistical Aggregate Functions

New analytical and statistical aggregate functions are available in SQL:

* `CHECKSUM` computes the checksum of the input values or expression.
* `KURTOSIS` functions `KURTOSIS_POP` and `KURTOSIS_SAMP`, measure the tailedness of a data set where a higher value means more of the variance within the data set is the result of infrequent extreme deviations as opposed to frequent modestly sized deviations. Note that a normal distribution has a kurtosis of zero.
* `SKEWNESS` functions `SKEWNESS_POP` and `SKEWNESS_SAMP`, are measures of asymmetry in data. A positive skewness is means the data skews to the right of the center point. A negative skewness means the data skews to the left.

All of these new aggregate functions support the keywords `ALL`, `DISTINCT`, and `UNIQUE`.

`ANY_VALUE`, a function to simplify and optimize the performance of `GROUP BY` statements, returns a random value in a group and is optimized to return the first value in the group. It ensures that there are no comparisons for any incoming row and eliminates the necessity to specify every column as part of the `GROUP BY` clause.

With these additional SQL aggregation functions, you can write more efficient code and benefit from faster in-database processing.

PREDICTION Function Syntax

These `PREDICTION` functions have a new `_ordered` syntax for scoring a model that requires ordered data, such as a Multivariate State Estimation Technique - Sequential Probability Ratio Test (MSET-SPRT) model:

* `PREDICTION`
* `PREDICTION_COST`
* `PREDICTION_DETAILS`
* `PREDICTION_PROBABILITY`
* `PREDICTION_SET`

Enhanced SQL Set Operators

The SQL set operators now support all keywords as defined in ANSI SQL. The new operator `EXCEPT` [`ALL`] is functionally equivalent to `MINUS` [`ALL`]. The operators `MINUS` and `INTERSECT` now support the keyword `ALL`.

Database In-Memory External Table Enhancements

The `INMEMORY` clause is supported at the table level and partition level of a partitioned external table or hybrid external table. For hybrid tables, the table-level `INMEMORY` attribute applies to all partitions, whether internal or external.

New JSON data type

`JSON` is a new SQL and PL/SQL data type for JSON data. It provides a substantial increase in query and update performance compared to textual JSON.

JSON Scalar Allowed at Top Level of JSON Document (RFC 8259 Support)

JSON documents in Oracle Database can now have a top-level JSON scalar value. Previously they had to have a JSON object or array value.

New Oracle SQL Function JSON\_TRANSFORM

You can use SQL function `JSON_TRANSFORM` to update parts of a JSON document without having to parse and rebuild it.

Enhanced Analytic Functions

Analytical window functions now supports the `EXCLUDE` options of the SQL standard window frame clause. The `query_block` clause of the `SELECT` statement now supports the `window_clause`, which implements the window clause of the SQL standard table expression as defined in the SQL:2011 standard.

Enhanced Database Availability with Zero Downtime to Switch Over to an Updated PKCS#11 Library

Starting with this release, Oracle Database can switch over to an updated PKCS#11 library without incurring any system downtime.

You can use the new `ADMINISTER KEY MANAGEMENT SWITCHOVER LIBRARY FOR ALL CONTAINERS` statement to enable an Oracle database to switch over from the PKCS#11 library that it is currently using to the updated PKCS#11 library.

Enhanced Double Parity Protection for Flex and Extended Disk Groups

You can use double parity protection for write-once files in a Oracle ASM Flex Disk Group which provides greater protection against multiple hardware failures.

Oracle ASM Flex Disk Group Support for Cloning a PDB in one CDB to a New PDB in a Different CDB

You can clone a PDB in a CDB to a new PDB in a different CDB using the `prepare_clause` of `ALTER PLUGGABLE DATABASE`.

File Group Templates

With file group templates you can customize and set default file group properties for automatically created file groups, enabling you to customize file group properties that are inherited by a number of databases.

Specify the `TEMPLATE` option of the `add_filegroup_clause` of `ALTER DISKGROUP`.

Automatic Index Optimization

You can enable Automatic Data Optimization (ADO) functionality to provide compression and optimization capability on indexes using the `index_ilm_clause` of `CREATE INDEX` and `ALTER INDEX`.

Gradual Database Password Change for Applications

Starting with Release 21c, an application can change its database passwords without an administrator having to schedule downtime.

You can enable gradual database password rollover period by setting a non-zero value to the `PASSWORD_ROLLOVER_TIME` user profile parameter using `CREATE PROFILE` or `ALTER PROFILE`.

After you set the time for the gradual password rollover period, you can use the `ALTER USER` statement to change the user's password and propagate the new password to all clients before the `PASSWORD_ROLLOVER_TIME` ends.

Minimum Password Length Enforcement for All PDBs

Starting with this release, you can enforce a minimum password length on all PDBs by setting a mandatory profile in the CDB root using `CREATE PROFILE`.