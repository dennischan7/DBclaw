# Oracle 11g - pseudocolumns005
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/pseudocolumns005.htm

[Go to main content](#BEGIN)

16/522 

# OBJECT\_ID Pseudocolumn

The `OBJECT_ID` pseudocolumn returns the object identifier of a column of an object table or view. Oracle uses this pseudocolumn as the primary key of an object table. `OBJECT_ID` is useful in `INSTEAD` `OF` triggers on views and for identifying the ID of a substitutable row in an object table.

Note:

In earlier releases, this pseudocolumn was called

`SYS_NC_OID$`

. That name is still supported for backward compatibility. However, Oracle recommends that you use the more intuitive name

`OBJECT_ID`

.

Scripting on this page enhances content navigation, but does not change the content in any way.