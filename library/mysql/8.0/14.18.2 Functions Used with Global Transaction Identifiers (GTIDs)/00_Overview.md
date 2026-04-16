---
source: MySQL 8.0 Reference
title: 00_Overview
---

The functions described in this section are used with GTID-based replication. It is important to keep in mind that all of these functions take string representations of GTID sets as arguments. As such, the GTID sets must always be quoted when used with them. See GTID Sets for more information.

The union of two GTID sets is simply their representations as strings, joined together with an interposed comma. In other words, you can define a very simple function for obtaining the union of two GTID sets, similar to that created here:

```
CREATE FUNCTION GTID_UNION(g1 TEXT, g2 TEXT)
 RETURNS TEXT DETERMINISTIC
 RETURN CONCAT(g1,',',g2);
```

For more information about GTIDs and how these GTID functions are used in practice, see Section 19.1.3, "Replication with Global Transaction Identifiers".

**Table 14.26 GTID Functions**

| Name                                                         | Description                                                             | Deprecated |
|--------------------------------------------------------------|-------------------------------------------------------------------------|------------|
| GTID_SUBSET()                                                | Return true if all GTIDs in subset<br>are also in set; otherwise false. |            |
| GTID_SUBTRACT()                                              | Return all GTIDs in set that are<br>not in subset.                      |            |
| WAIT_FOR_EXECUTED_GTID_SET() Wait until the given GTIDs have | executed on the replica.                                                |            |
| WAIT_UNTIL_SQL_THREAD_AFTER_GTIDS()                          | Use<br>WAIT_FOR_EXECUTED_GTID_SET().                                    | Yes        |

<span id="page-173-0"></span>• [GTID\\_SUBSET\(](#page-173-0)set1,set2)

Given two sets of global transaction identifiers set1 and set2, returns true if all GTIDs in set1 are also in set2. Returns NULL if set1 or set2 is NULL. Returns false otherwise.

The GTID sets used with this function are represented as strings, as shown in the following examples:

```
mysql> SELECT GTID_SUBSET('3E11FA47-71CA-11E1-9E33-C80AA9429562:23',
 -> '3E11FA47-71CA-11E1-9E33-C80AA9429562:21-57')\G
*************************** 1. row ***************************
GTID_SUBSET('3E11FA47-71CA-11E1-9E33-C80AA9429562:23',
```

```
 '3E11FA47-71CA-11E1-9E33-C80AA9429562:21-57'): 1
1 row in set (0.00 sec)
mysql> SELECT GTID_SUBSET('3E11FA47-71CA-11E1-9E33-C80AA9429562:23-25',
 -> '3E11FA47-71CA-11E1-9E33-C80AA9429562:21-57')\G
*************************** 1. row ***************************
GTID_SUBSET('3E11FA47-71CA-11E1-9E33-C80AA9429562:23-25',
 '3E11FA47-71CA-11E1-9E33-C80AA9429562:21-57'): 1
1 row in set (0.00 sec)
mysql> SELECT GTID_SUBSET('3E11FA47-71CA-11E1-9E33-C80AA9429562:20-25',
 -> '3E11FA47-71CA-11E1-9E33-C80AA9429562:21-57')\G
*************************** 1. row ***************************
GTID_SUBSET('3E11FA47-71CA-11E1-9E33-C80AA9429562:20-25',
 '3E11FA47-71CA-11E1-9E33-C80AA9429562:21-57'): 0
1 row in set (0.00 sec)
```

<span id="page-174-0"></span>• [GTID\\_SUBTRACT\(](#page-174-0)set1,set2)

Given two sets of global transaction identifiers set1 and set2, returns only those GTIDs from set1 that are not in set2. Returns NULL if set1 or set2 is NULL.

All GTID sets used with this function are represented as strings and must be quoted, as shown in these examples:

```
mysql> SELECT GTID_SUBTRACT('3E11FA47-71CA-11E1-9E33-C80AA9429562:21-57',
 -> '3E11FA47-71CA-11E1-9E33-C80AA9429562:21')\G
*************************** 1. row ***************************
GTID_SUBTRACT('3E11FA47-71CA-11E1-9E33-C80AA9429562:21-57',
 '3E11FA47-71CA-11E1-9E33-C80AA9429562:21'): 3e11fa47-71ca-11e1-9e33-c80aa9429562:22-57
1 row in set (0.00 sec)
mysql> SELECT GTID_SUBTRACT('3E11FA47-71CA-11E1-9E33-C80AA9429562:21-57',
 -> '3E11FA47-71CA-11E1-9E33-C80AA9429562:20-25')\G
*************************** 1. row ***************************
GTID_SUBTRACT('3E11FA47-71CA-11E1-9E33-C80AA9429562:21-57',
 '3E11FA47-71CA-11E1-9E33-C80AA9429562:20-25'): 3e11fa47-71ca-11e1-9e33-c80aa9429562:26-57
1 row in set (0.00 sec)
mysql> SELECT GTID_SUBTRACT('3E11FA47-71CA-11E1-9E33-C80AA9429562:21-57',
 -> '3E11FA47-71CA-11E1-9E33-C80AA9429562:23-24')\G
*************************** 1. row ***************************
GTID_SUBTRACT('3E11FA47-71CA-11E1-9E33-C80AA9429562:21-57',
 '3E11FA47-71CA-11E1-9E33-C80AA9429562:23-24'): 3e11fa47-71ca-11e1-9e33-c80aa9429562:21-22:25-57
1 row in set (0.01 sec)
```

Subtracting a GTID set from itself produces an empty set, as shown here:

```
mysql> SELECT GTID_SUBTRACT('3E11FA47-71CA-11E1-9E33-C80AA9429562:21-57',
 -> '3E11FA47-71CA-11E1-9E33-C80AA9429562:21-57')\G
*************************** 1. row ***************************
GTID_SUBTRACT('3E11FA47-71CA-11E1-9E33-C80AA9429562:21-57',
 '3E11FA47-71CA-11E1-9E33-C80AA9429562:21-57'): 
1 row in set (0.00 sec)
```

<span id="page-174-1"></span>• [WAIT\\_FOR\\_EXECUTED\\_GTID\\_SET\(](#page-174-1)gtid\_set[, timeout])

Wait until the server has applied all of the transactions whose global transaction identifiers are contained in gtid\_set; that is, until the condition GTID\_SUBSET(gtid\_subset, @@GLOBAL.gtid\_executed) holds. See Section 19.1.3.1, "GTID Format and Storage" for a definition of GTID sets.

If a timeout is specified, and timeout seconds elapse before all of the transactions in the GTID set have been applied, the function stops waiting. timeout is optional, and the default timeout is 0 seconds, in which case the function always waits until all of the transactions in the GTID set have been applied. timeout must be greater than or equal to 0; when running in strict SQL mode, a negative timeout value is immediately rejected with an error ([ER\\_WRONG\\_ARGUMENTS](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_wrong_arguments)); otherwise the function returns NULL, and raises a warning.

WAIT\_FOR\_EXECUTED\_GTID\_SET() monitors all the GTIDs that are applied on the server, including transactions that arrive from all replication channels and user clients. It does not take into account whether replication channels have been started or stopped.

For more information, see Section 19.1.3, "Replication with Global Transaction Identifiers".

GTID sets used with this function are represented as strings and so must be quoted as shown in the following example:

```
mysql> SELECT WAIT_FOR_EXECUTED_GTID_SET('3E11FA47-71CA-11E1-9E33-C80AA9429562:1-5');
 -> 0
```

For a syntax description for GTID sets, see Section 19.1.3.1, "GTID Format and Storage".

For WAIT\_FOR\_EXECUTED\_GTID\_SET(), the return value is the state of the query, where 0 represents success, and 1 represents timeout. Any other failures generate an error.

gtid\_mode cannot be changed to OFF while any client is using this function to wait for GTIDs to be applied.

```
• WAIT_UNTIL_SQL_THREAD_AFTER_GTIDS(gtid_set[, timeout][,channel])
 WAIT_UNTIL_SQL_THREAD_AFTER_GTIDS() is deprecated. Use
 WAIT_FOR_EXECUTED_GTID_SET() instead, which works regardless of the replication channel or
 user client through which the specified transactions arrive on the server.
```