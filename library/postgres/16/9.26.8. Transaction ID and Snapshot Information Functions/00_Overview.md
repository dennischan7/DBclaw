---
source: PostgreSQL 16 Reference
title: 00_Overview
---

The functions shown in [Table 9.80](#page-26-0) provide server transaction information in an exportable form. The main use of these functions is to determine which transactions were committed between two snapshots.

### <span id="page-26-0"></span>**Table 9.80. Transaction ID and Snapshot Information Functions**

### **Function**

### **Description**

age ( xid ) → integer

Returns the number of transactions between the supplied transaction id and the current transaction counter.

mxid\_age ( xid ) → integer

Returns the number of multixacts IDs between the supplied multixact ID and the current multixacts counter.

```
pg_current_xact_id () → xid8
```

Returns the current transaction's ID. It will assign a new one if the current transaction does not have one already (because it has not performed any database updates); see Section 74.1 for details. If executed in a subtransaction, this will return the top-level transaction ID; see Section 74.3 for details.

```
pg_current_xact_id_if_assigned () → xid8
```

Returns the current transaction's ID, or NULL if no ID is assigned yet. (It's best to use this variant if the transaction might otherwise be read-only, to avoid unnecessary consumption of an XID.) If executed in a subtransaction, this will return the top-level transaction ID.

```
pg_xact_status ( xid8 ) → text
```

Reports the commit status of a recent transaction. The result is one of in progress, committed, or aborted, provided that the transaction is recent enough that the system retains the commit status of that transaction. If it is old enough that no references to the transaction survive in the system and the commit status information has been discarded, the result is NULL. Applications might use this function, for example, to determine whether their transaction committed or aborted after the application and database server become disconnected while a COMMIT is in progress. Note that prepared transactions are

#### **Description**

reported as in progress; applications must check pg\_prepared\_xacts if they need to determine whether a transaction ID belongs to a prepared transaction.

pg\_current\_snapshot () → pg\_snapshot

Returns a current *snapshot*, a data structure showing which transaction IDs are now inprogress. Only top-level transaction IDs are included in the snapshot; subtransaction IDs are not shown; see Section 74.3 for details.

pg\_snapshot\_xip ( pg\_snapshot ) → setof xid8

Returns the set of in-progress transaction IDs contained in a snapshot.

pg\_snapshot\_xmax ( pg\_snapshot ) → xid8

Returns the xmax of a snapshot.

pg\_snapshot\_xmin ( pg\_snapshot ) → xid8

Returns the xmin of a snapshot.

pg\_visible\_in\_snapshot ( xid8, pg\_snapshot ) → boolean

Is the given transaction ID *visible* according to this snapshot (that is, was it completed before the snapshot was taken)? Note that this function will not give the correct answer for a subtransaction ID (subxid); see Section 74.3 for details.

pg\_get\_multixact\_members ( multixid xid ) → setof record ( xid xid, mode text )

Returns the transaction ID and lock mode for each member of the specified multixact ID. The lock modes forupd, fornokeyupd, sh, and keysh correspond to the row-level locks FOR UPDATE, FOR NO KEY UPDATE, FOR SHARE, and FOR KEY SHARE, respectively, as described in [Section 13.3.2](#page-132-0). Two additional modes are specific to multixacts: nokeyupd, used by updates that do not modify key columns, and upd, used by updates or deletes that modify key columns.

The internal transaction ID type xid is 32 bits wide and wraps around every 4 billion transactions. However, the functions shown in [Table 9.80](#page-26-0), except age, mxid\_age, and pg\_get\_multixact\_members, use a 64-bit type xid8 that does not wrap around during the life of an installation and can be converted to xid by casting if required; see Section 74.1 for details. The data type pg\_snapshot stores information about transaction ID visibility at a particular moment in time. Its components are described in [Table 9.81.](#page-27-0) pg\_snapshot's textual representation is xmin:xmax:xip\_list. For example 10:20:10,14,15 means xmin=10, xmax=20, xip\_list=10, 14, 15.

<span id="page-27-0"></span>**Table 9.81. Snapshot Components**

| Name     | Description                                                                                                                                                                                                                                                                                                                                  |
|----------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| xmin     | Lowest transaction ID that was still active. All<br>transaction IDs less than xmin are either com<br>mitted and visible, or rolled back and dead.                                                                                                                                                                                            |
| xmax     | One past the highest completed transaction<br>ID. All transaction IDs greater than or equal to<br>xmax had not yet completed as of the time of<br>the snapshot, and thus are invisible.                                                                                                                                                      |
| xip_list | Transactions in progress at the time of the snap<br>shot. A transaction ID that is xmin <= X <<br>xmax and not in this list was already completed<br>at the time of the snapshot, and thus is either vis<br>ible or dead according to its commit status. This<br>list does not include the transaction IDs of sub<br>transactions (subxids). |

In releases of PostgreSQL before 13 there was no xid8 type, so variants of these functions were provided that used bigint to represent a 64-bit XID, with a correspondingly distinct snapshot data type txid\_snapshot. These older functions have txid in their names. They are still supported for backward compatibility, but may be removed from a future release. See [Table 9.82](#page-28-0).

<span id="page-28-0"></span>**Table 9.82. Deprecated Transaction ID and Snapshot Information Functions**

```
Function
      Description
txid_current () → bigint
      See pg_current_xact_id().
txid_current_if_assigned () → bigint
      See pg_current_xact_id_if_assigned().
txid_current_snapshot () → txid_snapshot
      See pg_current_snapshot().
txid_snapshot_xip ( txid_snapshot ) → setof bigint
      See pg_snapshot_xip().
txid_snapshot_xmax ( txid_snapshot ) → bigint
      See pg_snapshot_xmax().
txid_snapshot_xmin ( txid_snapshot ) → bigint
      See pg_snapshot_xmin().
txid_visible_in_snapshot ( bigint, txid_snapshot ) → boolean
      See pg_visible_in_snapshot().
txid_status ( bigint ) → text
      See pg_xact_status().
```