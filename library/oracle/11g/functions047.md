# Oracle 11g - functions047
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/functions047.htm

[Go to main content](#BEGIN)

87/522 

# DATAOBJ\_TO\_PARTITION

Syntax

Purpose

`DATAOBJ_TO_PARTITION` is useful only to Data Cartridge developers who are performing data maintenance or query operations on system-partitioned tables that are used to store domain index data. The DML or query operations are triggered by corresponding operations on the base table of the domain index.

This function takes as arguments the name of the base table and the partition ID of the base table partition, both of which are passed to the function by the appropriate ODCIIndex method. The function returns the partition ID of the corresponding system-partitioned table, which can be used to perform the operation (DML or query) on that partition of the system-partitioned table.

Scripting on this page enhances content navigation, but does not change the content in any way.