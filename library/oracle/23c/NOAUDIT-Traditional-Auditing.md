# Oracle 23c - NOAUDIT-Traditional-Auditing
Source: https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/NOAUDIT-Traditional-Auditing.html

See Also:

Traditional auditing is desupported in 26ai. Databases migrated from earlier versions may still have traditional auditing policies configured. Those policies should be migrated to unified auditing. When migrated, the traditional audit policies may be removed with the `NOAUDIT` statement.

This section describes the `NOAUDIT` statement for traditional auditing, which is the same auditing functionality used in releases earlier than Oracle Database 12c.

Beginning with Oracle Database 12c, Oracle introduces unified auditing, which provides a full set of enhanced auditing features. For backward compatibility, traditional auditing is still supported. However, Oracle recommends that you plan the migration of your existing audit settings to the new unified audit policy syntax. For new audit requirements, Oracle recommends that you use the new unified auditing. Traditional auditing may be desupported in a future major release.

Purpose

Use the `NOAUDIT` statement to stop auditing operations previously enabled by the `AUDIT` statement.

The `NOAUDIT` statement must have the same syntax as the previous `AUDIT` statement. Further, it reverses the effects only of that particular statement. For example, suppose one `AUDIT` statement A enables auditing for a specific user. A second statement B enables auditing for all users. A `NOAUDIT` statement C to disable auditing for all users reverses statement B. However, statement C leaves statement A in effect and continues to audit the user that statement A specified.

Prerequisites

To stop auditing of SQL statements, you must have the `AUDIT` `SYSTEM` system privilege.

To stop auditing of schema objects, you must be the owner of the object on which you stop auditing or you must have the `AUDIT` `ANY` system privilege. In addition, if the object you chose for auditing is a directory, then even if you created it, you must have the `AUDIT` `ANY` system privilege.

To specify the `CONTAINER` clause, you must be connected to a multitenant container database (CDB). To specify `CONTAINER` `=` `ALL`, the current container must be the root and you must have the commonly granted `AUDIT` `SYSTEM` privilege in order to stop auditing for the issuances of a SQL statement, or the commonly granted `AUDIT` `ANY` privilege in order to stop auditing for the operations on a schema object. To specify `CONTAINER` `=` `CURRENT`, the current container must be a pluggable database (PDB) and you must have the locally granted `AUDIT` `SYSTEM` privilege in order to stop auditing the issuances of a SQL statement, or the locally granted `AUDIT` `ANY` privilege in order to stop auditing operations on a schema object.

audit\_operation\_clause::=

audit\_schema\_object\_clause::=

audit\_operation\_clause

Use the `audit_operation_clause` to stop auditing of a particular SQL statement.

statement\_option

For `sql_statement_shortcut`, specify the shortcut for the SQL statements for which auditing is to be stopped.

ALL

Specify `ALL` to stop auditing of all statement options currently being audited because of an earlier `AUDIT` `ALL` `...` statement. You cannot use this clause to reverse an earlier `AUDIT` `ALL` `STATEMENTS` `...` statement.

ALL STATEMENTS

Specify `ALL` `STATEMENTS` to reverse an earlier `AUDIT` `ALL` `STATEMENTS` `...` statement. You cannot use this clause to reverse an earlier `AUDIT` `ALL` `...` statement.

system\_privilege

For `system_privilege`, specify the system privilege for which auditing is to be stopped. Refer to [Table 18-2](GRANT.md#GUID-20B4E2C0-A7F8-4BC8-A5E8-BE61BDC41AC3__BABEFFEE "Column 1 names system privileges grouped by database object. Column 2 describes the operations authorized by the system privilege.") for a list of the system privileges and the statements they authorize.

ALL PRIVILEGES

Specify `ALL` `PRIVILEGES` to stop auditing of all system privileges currently being audited.

auditing\_by\_clause

Use the `auditing_by_clause` to stop auditing only for SQL statements issued by the specified users in their subsequent sessions. If you omit this clause, then Oracle Database stops auditing for all users' statements, except for the situation described for `WHENEVER` `SUCCESSFUL`.

audit\_schema\_object\_clause

Use the `audit_schema_object_clause` to stop auditing of a particular database object.

sql\_operation

For `sql_operation`, specify the type of operation for which auditing is to be stopped on the object specified in the `ON` clause.

ALL

Specify `ALL` as a shortcut equivalent to specifying all SQL operations applicable for the type of object.

auditing\_on\_clause

The `auditing_on_clause` lets you specify the particular schema object for which auditing is to be stopped.

* For object, specify the object name of a table, view, sequence, stored procedure, function, or package, materialized view, or library. If you do not qualify `object` with `schema`, then Oracle Database assumes the object is in your own schema.
* The `DIRECTORY` clause lets you specify the name of the directory on which auditing is to be stopped.
* The `SQL` `TRANSLATION` `PROFILE` clause lets you specify the SQL translation profile on which auditing is to be stopped.
* Specify `DEFAULT` to remove the specified object options as default object options for subsequently created objects.

NETWORK

Use this clause to discontinue auditing of database link usage and logins.

DIRECT\_PATH LOAD

Use this clause to discontinue auditing of SQL\*Loader direct path loads.

WHENEVER [NOT] SUCCESSFUL

Specify `WHENEVER` `SUCCESSFUL` to stop auditing only for SQL statements and operations on schema objects that complete successfully.

Specify `WHENEVER` `NOT` `SUCCESSFUL` to stop auditing only for SQL statements and operations that result in Oracle Database errors.

If you omit this clause, then the database stops auditing for all statements or operations, regardless of success or failure.

CONTAINER Clause

Use the `CONTAINER` clause to specify the scope of the `NOAUDIT` command.

* Specify `CONTAINER` `=` `CURRENT` to stop auditing in the PDB to which you are connected. If you specify the `auditing_by_clause`, then `user` must be a common user or local user in the current PDB. If you specify the `auditing_on_clause`, then the objects must be local objects in the current PDB.
* Specify `CONTAINER` `=` `ALL` to stop auditing across the entire CDB. If you specify the `auditing_by_clause`, then `user` must be a common user. If you do not specify the `auditing_by_clause`, then auditing is stopped for all common users and all local users in each PDB. If you specify the `auditing_on_clause`, then the objects must be common objects.

If you omit this clause, then `CONTAINER` `=` `CURRENT` is the default.

Examples

Stop Auditing of SQL Statements Related to Roles: Example

If you have chosen auditing for every SQL statement that creates or drops a role, then you can stop auditing of such statements by issuing the following statement:

```
NOAUDIT ROLE;
```

Stop Auditing of Updates or Queries on Objects Owned by a Particular User: Example

If you have chosen auditing for any statement that queries or updates any table issued by the users `hr` and `oe`, then you can stop auditing for queries by `hr` by issuing the following statement:

```
NOAUDIT SELECT TABLE BY hr;
```

The preceding statement stops auditing only queries by `hr`, so the database continues to audit queries and updates by `oe` as well as updates by `hr`.

Stop Auditing of Statements Authorized by a Particular Object Privilege: Example

To stop auditing on all statements that are authorized by `DELETE` `ANY` `TABLE` system privilege, issue the following statement:

```
NOAUDIT DELETE ANY TABLE;
```

Stop Auditing of Queries on a Particular Object: Example

If you have chosen auditing for every SQL statement that queries the `employees` table in the schema `hr`, then you can stop auditing for such queries by issuing the following statement:

```
NOAUDIT SELECT 
   ON hr.employees;
```

Stop Auditing of Queries that Complete Successfully: Example

You can stop auditing for queries that complete successfully by issuing the following statement:

```
NOAUDIT SELECT 
   ON hr.employees
   WHENEVER SUCCESSFUL;
```

This statement stops auditing only for successful queries. Oracle Database continues to audit queries resulting in Oracle Database errors.