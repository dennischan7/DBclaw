# Oracle 12c - functions055
Source: https://docs.oracle.com/database/121/SQLRF/functions055.htm

[Go to main content](#BEGIN)

128/555 

# DATAOBJ\_TO\_PARTITION

Syntax

Purpose

`DATAOBJ_TO_PARTITION` is useful only to Data Cartridge developers who are performing data maintenance or query operations on system-partitioned tables that are used to store domain index data. The DML or query operations are triggered by corresponding operations on the base table of the domain index.

This function takes as arguments the name of the base table and the partition ID of the base table partition, both of which are passed to the function by the appropriate ODCIIndex method. The function returns the absolute partition number of the corresponding system-partitioned table, which can be used to perform the operation (DML or query) on that partition of the system-partitioned table.

Note:

If the base table is interval partitioned, then Oracle recommends that you instead use the

`DATAOBJ_TO_MAT_PARTITION`

function. Refer to

[DATAOBJ\_TO\_MAT\_PARTITION](functions054.md#CJAEIJAG)

for more information.

Scripting on this page enhances content navigation, but does not change the content in any way.