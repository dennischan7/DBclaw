# Oracle 12c - statements_1004
Source: https://docs.oracle.com/database/121/SQLRF/statements_1004.htm

Semantics

policy

Specify the name of the unified audit policy to be modified. The policy must have been created using the `CREATE` `AUDIT` `POLICY` statement. You can find descriptions of all unified audit policies by querying the `AUDIT_UNIFIED_POLICIES` view.

ADD | DROP

Use the `ADD` clause to add privileges to be audited to `policy`.

Use the `DROP` clause to remove privileges to be audited from `policy`.

Refer to [privilege\_audit\_clause](statements_5001.md#BGECCGCH), [action\_audit\_clause](statements_5001.md#BGEGECCJ), and [role\_audit\_clause](statements_5001.md#BGEDDDBI) of `CREATE` `AUDIT` `POLICY` for the full semantics of these clauses.

CONDITION

Use this clause to drop, add, or replace the audit condition for `policy`.

Specify `DROP` to drop the audit condition from `policy`.

Specify `'``audit_condition``'` ... to add or replace the audit condition for `policy`.

Refer to [audit\_condition](statements_5001.md#BGEBAIJA), [EVALUATE PER STATEMENT](statements_5001.md#BGEJBBDB), [EVALUATE PER SESSION](statements_5001.md#BGECIFGJ), and [EVALUATE PER INSTANCE](statements_5001.md#BGEJIBAE) of `CREATE` `AUDIT` `POLICY` for the full semantics of these clauses.

Examples

The following examples modify unified audit policies that were created in the `CREATE` `AUDIT` `POLICY` ["Examples"](statements_5001.md#BGEGDCFA).

Adding Privileges, Actions, and Roles to a Unified Audit Policy: Examples The following statement adds the system privileges `CREATE` `ANY` `TABLE` and `DROP` `ANY` `TABLE` to unified audit policy `dml_pol`:

```
ALTER AUDIT POLICY dml_pol
  ADD PRIVILEGES CREATE ANY TABLE, DROP ANY TABLE;
```

The following statement adds the system actions `CREATE` `JAVA`, `ALTER` `JAVA`, and `DROP` `JAVA` to unified audit policy `java_pol`:

```
ALTER AUDIT POLICY java_pol
  ADD ACTIONS CREATE JAVA, ALTER JAVA, DROP JAVA;
```

The following statement adds the role `dba` to unified audit policy `table_pol`:

```
ALTER AUDIT POLICY table_pol
  ADD ROLES dba;
```

The following statement adds multiple system privileges, actions, and roles to unified audit policy `security_pol`:

```
ALTER AUDIT POLICY security_pol
  ADD PRIVILEGES CREATE ANY LIBRARY, DROP ANY LIBRARY
      ACTIONS DELETE on hr.employees,
              INSERT on hr.employees,
              UPDATE on hr.employees,
              ALL on hr.departments
      ROLES dba, connect;
```

Dropping Privileges, Actions, and Roles from a Unified Audit Policy: Examples The following statement drops the system privilege `CREATE` `ANY` `TABLE` from unified audit policy `table_pol`:

```
ALTER AUDIT POLICY table_pol
  DROP PRIVILEGES CREATE ANY TABLE;
```

The following statement drops the `INSERT` and `UPDATE` actions on `hr`.`employees` from unified audit policy `dml_pol`:

```
ALTER AUDIT POLICY dml_pol
  DROP ACTIONS INSERT on hr.employees,
               UPDATE on hr.employees;
```

The following statement drops the role `java_deploy` from unified audit policy `java_pol`:

```
ALTER AUDIT POLICY java_pol
  DROP ROLES java_deploy;
```

The following statement drops a system privilege, an action, and a role from unified audit policy `hr_admin_pol`:

```
ALTER AUDIT POLICY hr_admin_pol
  DROP PRIVILEGES CREATE ANY TABLE
       ACTIONS LOCK TABLE
       ROLES audit_viewer;
```

Adding and Dropping Actions for a Unified Audit Policy: Example The following statement adds `EXPORT` actions for Oracle Data Pump to unified audit policy `dp_actions_pol` and drops `IMPORT` actions for Oracle Data Pump:

```
ALTER AUDIT POLICY dp_actions_pol
  ADD ACTIONS COMPONENT = datapump EXPORT
  DROP ACTIONS COMPONENT = datapump IMPORT;
```

Dropping the Audit Condition from a Unified Audit Policy: Example The following statement drops the audit condition from unified audit policy `order_updates_pol`:

```
ALTER AUDIT POLICY order_updates_pol
  CONDITION DROP;
```

Modifying the Audit Condition for a Unified Audit Policy: Example The following statement modifies the audit condition for unified audit policy `emp_updates_pol` so that the policy is enforced only when the auditable statement is issued by a user whose UID is 102:

```
ALTER AUDIT POLICY emp_updates_pol
  CONDITION 'UID = 102'
  EVALUATE PER STATEMENT;
```