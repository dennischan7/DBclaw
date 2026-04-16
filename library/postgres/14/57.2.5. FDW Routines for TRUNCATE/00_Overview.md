---
source: PostgreSQL 14 Reference
title: 00_Overview
---

```
void
ExecForeignTruncate(List *rels,
 DropBehavior behavior,
 bool restart_seqs);
```

Truncate foreign tables. This function is called when TRUNCATE is executed on a foreign table. rels is a list of Relation data structures of foreign tables to truncate.

behavior is either DROP\_RESTRICT or DROP\_CASCADE indicating that the RESTRICT or CAS-CADE option was requested in the original TRUNCATE command, respectively.

If restart\_seqs is true, the original TRUNCATE command requested the RESTART IDEN-TITY behavior, otherwise the CONTINUE IDENTITY behavior was requested.

Note that the ONLY options specified in the original TRUNCATE command are not passed to Exec-ForeignTruncate. This behavior is similar to the callback functions of SELECT, UPDATE and DELETE on a foreign table.

ExecForeignTruncate is invoked once per foreign server for which foreign tables are to be truncated. This means that all foreign tables included in rels must belong to the same server.

If the ExecForeignTruncate pointer is set to NULL, attempts to truncate foreign tables will fail with an error message.

## <span id="page-157-0"></span>**57.2.6. FDW Routines for Row Locking**

If an FDW wishes to support *late row locking* (as described in [Section 57.5](#page-166-0)), it must provide the following callback functions:

```
RowMarkType
GetForeignRowMarkType(RangeTblEntry *rte,
 LockClauseStrength strength);
```

Report which row-marking option to use for a foreign table. rte is the RangeTblEntry node for the table and strength describes the lock strength requested by the relevant FOR UPDATE/SHARE clause, if any. The result must be a member of the RowMarkType enum type.

This function is called during query planning for each foreign table that appears in an UPDATE, DELETE, or SELECT FOR UPDATE/SHARE query and is not the target of UPDATE or DELETE.

If the GetForeignRowMarkType pointer is set to NULL, the ROW\_MARK\_COPY option is always used. (This implies that RefetchForeignRow will never be called, so it need not be provided either.)

See [Section 57.5](#page-166-0) for more information.

```
void
RefetchForeignRow(EState *estate,
 ExecRowMark *erm,
 Datum rowid,
 TupleTableSlot *slot,
 bool *updated);
```

Re-fetch one tuple slot from the foreign table, after locking it if required. estate is global execution state for the query. erm is the ExecRowMark struct describing the target foreign table and the row lock type (if any) to acquire. rowid identifies the tuple to be fetched. slot contains nothing useful upon call, but can be used to hold the returned tuple. updated is an output parameter.

This function should store the tuple into the provided slot, or clear it if the row lock couldn't be obtained. The row lock type to acquire is defined by erm->markType, which is the value previously returned by GetForeignRowMarkType. (ROW\_MARK\_REFERENCE means to just re-fetch the tuple without acquiring any lock, and ROW\_MARK\_COPY will never be seen by this routine.)

In addition, \*updated should be set to true if what was fetched was an updated version of the tuple rather than the same version previously obtained. (If the FDW cannot be sure about this, always returning true is recommended.)

Note that by default, failure to acquire a row lock should result in raising an error; returning with an empty slot is only appropriate if the SKIP LOCKED option is specified by erm->waitPolicy.

The rowid is the ctid value previously read for the row to be re-fetched. Although the rowid value is passed as a Datum, it can currently only be a tid. The function API is chosen in hopes that it may be possible to allow other data types for row IDs in future.

If the RefetchForeignRow pointer is set to NULL, attempts to re-fetch rows will fail with an error message.

See [Section 57.5](#page-166-0) for more information.

```
bool
RecheckForeignScan(ForeignScanState *node,
 TupleTableSlot *slot);
```

Recheck that a previously-returned tuple still matches the relevant scan and join qualifiers, and possibly provide a modified version of the tuple. For foreign data wrappers which do not perform join pushdown, it will typically be more convenient to set this to NULL and instead set fdw\_recheck\_quals appropriately. When outer joins are pushed down, however, it isn't sufficient to reapply the checks relevant to all the base tables to the result tuple, even if all needed attributes are present, because failure to match some qualifier might result in some attributes going to NULL, rather than in no tuple being returned. RecheckForeignScan can recheck qualifiers and return true if they are still satisfied and false otherwise, but it can also store a replacement tuple into the supplied slot.

To implement join pushdown, a foreign data wrapper will typically construct an alternative local join plan which is used only for rechecks; this will become the outer subplan of the ForeignScan. When a recheck is required, this subplan can be executed and the resulting tuple can be stored in the slot. This plan need not be efficient since no base table will return more than one row; for example, it may implement all joins as nested loops. The function GetExistingLocalJoinPath may be used to search existing paths for a suitable local join path, which can be used as the alternative local join plan. GetExistingLocalJoinPath searches for an unparameterized path in the path list of the specified join relation. (If it does not find such a path, it returns NULL, in which case a foreign data wrapper may build the local path by itself or may choose not to create access paths for that join.)