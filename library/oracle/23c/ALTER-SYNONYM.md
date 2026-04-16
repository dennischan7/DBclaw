# Oracle 23c - ALTER-SYNONYM
Source: https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/ALTER-SYNONYM.html

Purpose

Use the `ALTER` `SYNONYM` statement to modify an existing synonym.

Prerequisites

To modify a private synonym in another user's schema, you must have the `CREATE` `ANY` `SYNONYM` and `DROP` `ANY` `SYNONYM` system privileges.

To modify a `PUBLIC` synonym, you must have the `CREATE` `PUBLIC` `SYNONYM` and `DROP` `PUBLIC` `SYNONYM` system privileges.

PUBLIC

Specify `PUBLIC` if `synonym` is a public synonym. You cannot use this clause to change a public synonym to a private synonym, or vice versa.

IF EXISTS

Specify `IF EXISTS` to alter an existing table.

Specifying `IF NOT EXISTS` with `ALTER VIEW` results in `ORA-11544: Incorrect IF EXISTS clause for ALTER/DROP statement`.

schema

Specify the schema containing the synonym. If you omit `schema`, then Oracle Database assumes the synonym is in your own schema.

synonym

Specify the name of the synonym to be altered.

EDITIONABLE | NONEDITIONABLE

Use these clauses to specify whether the synonym becomes an editioned or noneditioned object if editioning is later enabled for the schema object type `SYNONYM` in `schema`. The default is `EDITIONABLE`. For information about altering editioned and noneditioned objects, see [Oracle Database Development Guide](/pls/topic/lookup?ctx=en/database/oracle/oracle-database/26/sqlrf&id=ADFNS1287).

Restriction on EDITIONABLE | NONEDITIONABLE

You cannot specify these clauses for a public synonym because editioning is always enabled for the object type `SYNONYM` in the `PUBLIC` schema.

COMPILE

Use this clause to compile `synonym`. A synonym places a dependency on its target object and becomes invalid if the target object is changed or dropped. When you compile an invalid synonym, it becomes valid again.

Note:

You can determine if a synonym is valid or invalid by querying the `STATUS` column of the `ALL_`, `DBA_`, and `USER_OBJECTS` data dictionary views.

Examples

The following examples modify synonyms that were created in the `CREATE` `SYNONYM` "[Examples](CREATE-SYNONYM.md#GUID-A806C82F-1171-478E-A910-F9C6C42739B2__G2266838)".

The following statement compiles synonym `offices`:

```
ALTER SYNONYM offices COMPILE;
```

The following statement compiles public synonym `emp_table`:

```
ALTER PUBLIC SYNONYM emp_table COMPILE;
```

The following statement causes synonym `offices` to remain a noneditioned object if editioning is later enabled for schema object type `SYNONYM` in the schema that contains the synonym `offices`:

```
ALTER SYNONYM offices NONEDITIONABLE;
```