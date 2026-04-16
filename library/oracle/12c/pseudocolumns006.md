# Oracle 12c - pseudocolumns006
Source: https://docs.oracle.com/database/121/SQLRF/pseudocolumns006.htm

[Go to main content](#BEGIN)

27/555 

# OBJECT\_VALUE Pseudocolumn

The `OBJECT_VALUE` pseudocolumn returns system-generated names for the columns of an object table, `XMLType` table, object view, or `XMLType` view. This pseudocolumn is useful for identifying the value of a substitutable row in an object table and for creating object views with the `WITH` `OBJECT` `IDENTIFIER` clause.

Note:

In earlier releases, this pseudocolumn was called

`SYS_NC_ROWINFO$`

. That name is still supported for backward compatibility. However, Oracle recommends that you use the more intuitive name

`OBJECT_VALUE`

.

Scripting on this page enhances content navigation, but does not change the content in any way.