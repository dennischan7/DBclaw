# Oracle 23c - DROP-SYNONYM
Source: https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/DROP-SYNONYM.html

Purpose

Use the `DROP` `SYNONYM` statement to remove a synonym from the database or to change the definition of a synonym by dropping and re-creating it.

Prerequisites

To drop a private synonym, either the synonym must be in your own schema or you must have the `DROP` `ANY` `SYNONYM` system privilege.

To drop a `PUBLIC` synonym, you must have the `DROP` `PUBLIC` `SYNONYM` system privilege.

drop\_synonym::=

drop\_synonym::=

PUBLIC

You must specify `PUBLIC` to drop a public synonym. You cannot specify `schema` if you have specified `PUBLIC`.

IF EXISTS

Specify `IF EXISTS` to drop an existing object.

Specifying `IF NOT EXISTS` with `DROP` results in `ORA-11544: Incorrect IF EXISTS clause for ALTER/DROP statement`.

schema

Specify the schema containing the synonym. If you omit `schema`, then Oracle Database assumes the synonym is in your own schema.

synonym

Specify the name of the synonym to be dropped.

If you drop a synonym for the master table of a materialized view, and if the defining query of the materialized view specified the synonym rather than the actual table name, then Oracle Database marks the materialized view unusable.

If an object type synonym has any dependent tables or user-defined types, then you cannot drop the synonym unless you also specify `FORCE`.

FORCE

Specify `FORCE` to drop the synonym even if it has dependent tables or user-defined types.

Note:

Oracle does not recommend that you specify `FORCE` to drop object type synonyms with dependencies. This operation can result in invalidation of other user-defined types or marking `UNUSED` the table columns that depend on the synonym. For information about type dependencies, see [Oracle Database Object-Relational Developer's Guide](/pls/topic/lookup?ctx=en/database/oracle/oracle-database/26/sqlrf&id=ADOBJ00402).