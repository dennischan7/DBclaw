# Oracle 11g - statements_9017
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/statements_9017.htm

# NOAUDIT

Purpose

Use the `NOAUDIT` statement to stop auditing operations previously enabled by the `AUDIT` statement.

The `NOAUDIT` statement must have the same syntax as the previous `AUDIT` statement. Further, it reverses the effects only of that particular statement. For example, suppose one `AUDIT` statement A enables auditing for a specific user. A second statement B enables auditing for all users. A `NOAUDIT` statement C to disable auditing for all users reverses statement B. However, statement C leaves statement A in effect and continues to audit the user that statement A specified.

See Also:

[AUDIT](statements_4007.md#i2059073)

for more information on auditing

Prerequisites

To stop auditing of SQL statements, you must have the `AUDIT` `SYSTEM` system privilege.

To stop auditing of schema objects, you must be the owner of the object on which you stop auditing or you must have the `AUDIT` `ANY` system privilege. In addition, if the object you chose for auditing is a directory, then even if you created it, you must have the `AUDIT` `ANY` system privilege.

Semantics

audit\_operation\_clause

Use the `audit_operation_clause` to stop auditing of a particular SQL statement.

statement\_option For `sql_statement_shortcut`, specify the shortcut for the SQL statements for which auditing is to be stopped. Refer to [Table 13-1](statements_4007.md#BABEFEAC) and [Table 13-2](statements_4007.md#g2274817) for a list of the SQL statement shortcuts and the SQL statements they audit.

ALL Specify `ALL` to stop auditing of all statement options currently being audited because of an earlier `AUDIT` `ALL` `...` statement. You cannot use this clause to reverse an earlier `AUDIT` `ALL` `STATEMENTS` `...` statement.

ALL STATEMENTS Specify `ALL` `STATEMENTS` to reverse an earlier `AUDIT` `ALL` `STATEMENTS` `...` statement. You cannot use this clause to reverse an earlier `AUDIT` `ALL` `...` statement.

system\_privilege For `system_privilege`, specify the system privilege for which auditing is to be stopped. Refer to [Table 18-1](statements_9013.md#BABEFFEE) for a list of the system privileges and the statements they authorize.

ALL PRIVILEGES Specify `ALL` `PRIVILEGES` to stop auditing of all system privileges currently being audited.

auditing\_by\_clause

Use the `auditing_by_clause` to stop auditing only for SQL statements issued by the specified users in their subsequent sessions. If you omit this clause, then Oracle Database stops auditing for all users' statements, except for the situation described for `WHENEVER` `SUCCESSFUL`.

audit\_schema\_object\_clause

Use the `audit_schema_object_clause` to stop auditing of a particular database object.

sql\_operation For `sql_operation`, specify the type of operation for which auditing is to be stopped on the object specified in the `ON` clause. Refer to [Table 13-3](statements_4007.md#BABCFIEA) for a list of these options.

ALL Specify `ALL` as a shortcut equivalent to specifying all SQL operations applicable for the type of object.

auditing\_on\_clause  The `auditing_on_clause` lets you specify the particular schema object for which auditing is to be stopped.

* For object, specify the object name of a table, view, sequence, stored procedure, function, or package, materialized view, or library. If you do not qualify `object` with `schema`, then Oracle Database assumes the object is in your own schema. Refer to [AUDIT](statements_4007.md#i2059073) for information on auditing specific schema objects.
* The `DIRECTORY` clause lets you specify the name of the directory on which auditing is to be stopped.
* Specify `DEFAULT` to remove the specified object options as default object options for subsequently created objects.

NETWORK Use this clause to discontinue auditing of database link usage and logins.

WHENEVER [NOT] SUCCESSFUL Specify `WHENEVER` `SUCCESSFUL` to stop auditing only for SQL statements and operations on schema objects that complete successfully.

Specify `WHENEVER` `NOT` `SUCCESSFUL` to stop auditing only for statements and operations that result in Oracle Database errors.

If you omit this clause, then the database stops auditing for all statements or operations, regardless of success or failure.

Examples

Stop Auditing of SQL Statements Related to Roles: Example If you have chosen auditing for every SQL statement that creates or drops a role, then you can stop auditing of such statements by issuing the following statement:

```
NOAUDIT ROLE;
```

Stop Auditing of Updates or Queries on Objects Owned by a Particular User: Example If you have chosen auditing for any statement that queries or updates any table issued by the users `hr` and `oe`, then you can stop auditing for queries by `hr` by issuing the following statement:

```
NOAUDIT SELECT TABLE BY hr;
```

The preceding statement stops auditing only queries by `hr`, so the database continues to audit queries and updates by `oe` as well as updates by `hr`.

Stop Auditing of Statements Authorized by a Particular Object Privilege: Example To stop auditing on all statements that are authorized by `DELETE` `ANY` `TABLE` system privilege, issue the following statement:

```
NOAUDIT DELETE ANY TABLE;
```

Stop Auditing of Queries on a Particular Object: Example If you have chosen auditing for every SQL statement that queries the `employees` table in the schema `hr`, then you can stop auditing for such queries by issuing the following statement:

```
NOAUDIT SELECT 
   ON hr.employees;
```

Stop Auditing of Queries that Complete Successfully: Example You can stop auditing for queries that complete successfully by issuing the following statement:

```
NOAUDIT SELECT 
   ON hr.employees
   WHENEVER SUCCESSFUL;
```

This statement stops auditing only for successful queries. Oracle Database continues to audit queries resulting in Oracle Database errors.