# Oracle 11g - statements_4007
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/statements_4007.htm

Prerequisites

To audit issuances of a SQL statement, you must have the `AUDIT` `SYSTEM` system privilege. However, the `AUDIT` `SYSTEM` system privilege is not required when you use the `IN` `SESSION` `CURRENT` clause.

To collect auditing results, you must enable auditing by setting the initialization parameter `AUDIT_TRAIL` to a value other than the default setting of `NONE`. You can specify auditing options regardless of whether auditing is enabled. However, Oracle Database does not generate audit records until you enable auditing.

To audit operations on a schema object, the object you choose for auditing must be in your own schema or you must have `AUDIT` `ANY` system privilege. In addition, if the object you choose for auditing is a directory object, even if you created it, then you must have `AUDIT` `ANY` system privilege.

Note:

The

`AUDIT` `ANY`

system privileges allows the grantee to audit any object in any schema except the

`SYS`

schema. You can allow such a grantee to audit objects in the

`SYS`

schema by setting the

`O7_DICTIONARY_ACCESSIBILITY`

initialization parameter to

`TRUE`

. For security reasons, Oracle recommends that you use this setting only with great caution.

Semantics

audit\_operation\_clause

Use the `audit_operation_clause` to audit specified operations, regardless of the schema objects affected by the operations.

sql\_statement\_shortcut

Specify a shortcut to audit the use of specific SQL statements. [Table 13-1](#BABEFEAC) and [Table 13-2](#g2274817) list the shortcuts and the SQL statements they audit.

Note:

Do not confuse SQL statement shortcuts with system privileges. For example:

* An `AUDIT` `USER` statement specifies the `USER` shortcut for auditing of all `CREATE` `USER`, `ALTER` `USER`, and `DROP` `USER` SQL statements. Auditing in this case includes an operation in which a user changes his or her own password with an `ALTER` `USER` statement.
* An `AUDIT` `ALTER` `USER` statement specifies the `ALTER` `USER` system privilege for auditing of all operations that make use of that system privilege. Auditing in this case does not include an operation in which a user changes his or her own password, because that operation does not require the `ALTER` `USER` system privilege.

For each audited operation, Oracle Database produces an audit record containing this information:

* The user performing the operation
* The type of operation
* The object involved in the operation
* The date and time of the operation

Oracle Database writes audit records to the audit trail, which is a database table containing audit records. You can review database activity by examining the audit trail through data dictionary views.

system\_privilege

Specify a system privilege to audit SQL statements and other operations that are authorized by the specified system privilege.

Note:

Auditing the use of a system privilege containing the

`ANY`

keyword is more restrictive than auditing the use of the same privilege without the

`ANY`

keyword. For example:

* `AUDIT` `CREATE` `PROCEDURE` audits the statements issued using either the `CREATE` `PROCEDURE` or `CREATE` `ANY` `PROCEDURE` privilege.
* `AUDIT` `CREATE` `ANY` `PROCEDURE` audits only those statements issued using the `CREATE` `ANY` `PROCEDURE` privilege.

Rather than specifying many individual system privileges, you can specify the roles `CONNECT`, `RESOURCE`, and `DBA`. Doing so is equivalent to auditing all of the system privileges granted to those roles.

Oracle Database also provides three shortcuts for specifying groups of system privileges and statement options at once:

ALL Specify `ALL` to audit all statements options shown in [Table 13-1](#BABEFEAC) but not the additional statement options shown in [Table 13-2](#g2274817).

ALL STATEMENTS Specify `ALL` `STATEMENTS` to audit all top-level SQL statements executed. Top-level SQL statements are issued directly by a user. SQL statements run from within a PL/SQL procedure or function are not considered top-level statements. Therefore, this clause does not audit the statements executed within PL/SQL procedures or functions. However, the execution of the PL/SQL procedure or function itself is audited. This clause is useful if you want to audit all the statements in a specific environment, regardless of other auditing configurations that are system wide or user specific.

ALL PRIVILEGES Specify `ALL` `PRIVILEGES` to audit system privileges.

Note:

Oracle recommends that you specify individual system privileges and statement options for auditing rather than roles or shortcuts. The specific system privileges and statement options encompassed by roles and shortcuts change from one release to the next and may not be supported in future versions of Oracle Database.

auditing\_by\_clause

Specify the `auditing_by_clause` to restrict auditing to only SQL statements issued by the specified users. If you omit this clause, then Oracle Database audits all users' statements.

IN SESSION CURRENT

Use this clause to limit auditing to the current session.

audit\_schema\_object\_clause

Use the `audit_schema_object_clause` to audit operations on specific schema objects.

sql\_operation

Specify the SQL operation to be audited. [Table 13-3](#BABCFIEA) shows the types of objects that can be audited, and for each object the SQL statements that can be audited. For example, if you choose to audit a table with the `ALTER` operation, then Oracle Database audits all `ALTER` `TABLE` statements issued against the table. If you choose to audit a sequence with the `SELECT` operation, then the database audits all statements that use any values of the sequence.

ALL

Specify `ALL` as a shortcut equivalent to specifying all SQL operations applicable for the type of object.

auditing\_on\_clause

The `auditing_on_clause` lets you specify the particular schema object to be audited.

schema Specify the schema containing the object chosen for auditing. If you omit `schema`, then Oracle Database assumes the object is in your own schema.

object Specify the name of the object to be audited. The object must be a table, view, sequence, stored procedure, function, package, materialized view, mining model, or library.

You can also specify a synonym for a table, view, sequence, procedure, stored function, package, materialized view, or user-defined type.

ON DEFAULT  Specify `ON` `DEFAULT` to establish the specified object options as default object options for subsequently created objects. After you have established these default auditing options, any subsequently created object is automatically audited with those options. The default auditing options for a view are always the union of the auditing options for the base tables of the view. You can see the current default auditing options by querying the `ALL_DEF_AUDIT_OPTS` data dictionary view.

When you change the default auditing options, the auditing options for previously created objects remain the same. You can change the auditing options for an existing object only by specifying the object in the `ON` clause of the `AUDIT` statement.

ON DIRECTORY  The `ON` `DIRECTORY` clause lets you specify the name of a directory chosen for auditing.

ON MINING MODEL  The `ON` `MINING` `MODEL` clause lets you specify the name of a mining model to be audited.

NETWORK

Use this clause to detect internal failures in the network layer.

BY SESSION

In earlier releases, `BY` `SESSION` caused the database to write a single record for all SQL statements or operations of the same type executed on the same schema objects in the same session. Beginning with this release of Oracle Database, both `BY` `SESSION` and `BY` `ACCESS` cause Oracle Database to write one audit record for each audited statement and operation. `BY` `SESSION` continues to populate different values to the audit trail compared with `BY` `ACCESS`. Oracle recommends that you include the `BY` `ACCESS` clause for all `AUDIT` statements, which results in a more detailed audit record. If you specify neither clause, then `BY` `SESSION` is the default.

Note:

This change applies only to schema object audit options, statement options and system privileges that audit SQL statements other than data definition language (DDL) statements. The database has always audited

`BY` `ACCESS`

all SQL statements and system privileges that audit a DDL statement.

BY ACCESS

Specify `BY` `ACCESS` if you want Oracle Database to write one record for each audited statement and operation.

Note:

If you specify either a SQL statement shortcut or a system privilege that audits a data definition language (DDL) statement, then the database always audits by access. In all other cases, the database honors the

`BY` `SESSION`

or

`BY` `ACCESS`

specification.

For statement options and system privileges that audit SQL statements other than DDL, you can specify either `BY` `SESSION` or `BY` `ACCESS`. `BY` `SESSION` is the default.

WHENEVER [NOT] SUCCESSFUL

Specify `WHENEVER` `SUCCESSFUL` to audit only SQL statements and operations that succeed.

Specify `WHENEVER` `NOT` `SUCCESSFUL` to audit only statements and operations that fail or result in errors.

If you omit this clause, then Oracle Database performs the audit regardless of success or failure.

Examples

Auditing SQL Statements Relating to Roles: Example  To choose auditing for every SQL statement that creates, alters, drops, or sets a role, regardless of whether the statement completes successfully, issue the following statement:

```
AUDIT ROLE;
```

To choose auditing for every statement that successfully creates, alters, drops, or sets a role, issue the following statement:

```
AUDIT ROLE
    WHENEVER SUCCESSFUL;
```

To choose auditing for every `CREATE` `ROLE`, `ALTER` `ROLE`, `DROP` `ROLE`, or `SET` `ROLE` statement that results in an Oracle Database error, issue the following statement:

```
AUDIT ROLE
    WHENEVER NOT SUCCESSFUL;
```

Auditing Query and Update SQL Statements: Example To choose auditing for any statement that queries or updates any table, issue the following statement:

```
AUDIT SELECT TABLE, UPDATE TABLE;
```

To choose auditing for statements issued by the users `hr` and `oe` that query or update a table or view, issue the following statement

```
AUDIT SELECT TABLE, UPDATE TABLE
    BY hr, oe;
```

Auditing Deletions: Example To choose auditing for statements issued using the `DELETE` `ANY` `TABLE` system privilege, issue the following statement:

```
AUDIT DELETE ANY TABLE;
```

Auditing Statements Relating to Directories: Examples To choose auditing for statements issued using the `CREATE` `ANY` `DIRECTORY` system privilege, issue the following statement:

```
AUDIT CREATE ANY DIRECTORY;
```

To choose auditing for `CREATE` `DIRECTORY` (and `DROP` `DIRECTORY`) statements that do not use the `CREATE` `ANY` `DIRECTORY` system privilege, issue the following statement:

```
AUDIT DIRECTORY;
```

To choose auditing for every statement that reads files from the `bfile_dir` directory, issue the following statement:

```
AUDIT READ ON DIRECTORY bfile_dir;
```

Auditing Queries on a Table: Example To choose auditing for every SQL statement that queries the `employees` table in the schema `hr`, issue the following statement:

```
AUDIT SELECT
    ON hr.employees;
```

To choose auditing for every statement that successfully queries the `employees` table in the schema `hr`, issue the following statement:

```
AUDIT SELECT 
    ON hr.employees
    WHENEVER SUCCESSFUL;
```

To choose auditing for every statement that queries the `employees` table in the schema `hr` and results in an Oracle Database error, issue the following statement:

```
AUDIT SELECT 
    ON hr.employees
    WHENEVER NOT SUCCESSFUL;
```

Auditing Inserts and Updates on a Table: Example To choose auditing for every statement that inserts or updates a row in the `customers` table in the schema `oe`, issue the following statement:

```
AUDIT INSERT, UPDATE
    ON oe.customers;
```

Auditing Operations on a Sequence: Example To choose auditing for every statement that performs any operation on the `employees_seq` sequence in the schema `hr`, issue the following statement:

```
AUDIT ALL
    ON hr.employees_seq;
```

The preceding statement uses the `ALL` shortcut to choose auditing for the following statements that operate on the sequence:

Setting Default Auditing Options: Example The following statement specifies default auditing options for objects created in the future:

```
AUDIT ALTER, GRANT, INSERT, UPDATE, DELETE
    ON DEFAULT;
```

Any objects created later are automatically configured for audit with the specified options that apply to them.

* If you create a table, then Oracle Database automatically configures audit options `ALTER`, `GRANT`, `INSERT`, `UPDATE`, or `DELETE` issued against the table.
* If you create a view, then Oracle Database automatically configures audit options `GRANT`, `INSERT`, `UPDATE`, or `DELETE` against the view.
* If you create a sequence, then Oracle Database automatically configures audit options `ALTER` or `GRANT` against the sequence.
* If you create a procedure, package, or function, then Oracle Database automatically configures audit options `ALTER` or `GRANT` against it.