---
source: PostgreSQL 14 Reference
title: 00_Overview
---

```
List *
ImportForeignSchema(ImportForeignSchemaStmt *stmt, Oid serverOid);
```

Obtain a list of foreign table creation commands. This function is called when executing IMPORT FOREIGN SCHEMA, and is passed the parse tree for that statement, as well as the OID of the foreign server to use. It should return a list of C strings, each of which must contain a CREATE FOREIGN TABLE command. These strings will be parsed and executed by the core server.

Within the ImportForeignSchemaStmt struct, remote\_schema is the name of the remote schema from which tables are to be imported. list\_type identifies how to filter table names: FD-W\_IMPORT\_SCHEMA\_ALL means that all tables in the remote schema should be imported (in this case table\_list is empty), FDW\_IMPORT\_SCHEMA\_LIMIT\_TO means to include only tables listed in table\_list, and FDW\_IMPORT\_SCHEMA\_EXCEPT means to exclude the tables listed in table\_list. options is a list of options used for the import process. The meanings of the options are up to the FDW. For example, an FDW could use an option to define whether the NOT NULL attributes of columns should be imported. These options need not have anything to do with those supported by the FDW as database object options.

The FDW may ignore the local\_schema field of the ImportForeignSchemaStmt, because the core server will automatically insert that name into the parsed CREATE FOREIGN TABLE commands.

The FDW does not have to concern itself with implementing the filtering specified by list\_type and table\_list, either, as the core server will automatically skip any returned commands for tables excluded according to those options. However, it's often useful to avoid the work of creating commands for excluded tables in the first place. The function IsImportableForeignTable() may be useful to test whether a given foreign-table name will pass the filter.

If the FDW does not support importing table definitions, the ImportForeignSchema pointer can be set to NULL.