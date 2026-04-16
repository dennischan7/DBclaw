---
source: PostgreSQL 14 Reference
title: 00_Overview
---

If an FDW supports performing remote post-scan/join processing, such as remote aggregation, it should provide this callback function:

```
void
GetForeignUpperPaths(PlannerInfo *root,
 UpperRelationKind stage,
 RelOptInfo *input_rel,
 RelOptInfo *output_rel,
 void *extra);
```

Create possible access paths for *upper relation* processing, which is the planner's term for all postscan/join query processing, such as aggregation, window functions, sorting, and table updates. This optional function is called during query planning. Currently, it is called only if all base relation(s) involved in the query belong to the same FDW. This function should generate ForeignPath path(s) for any post-scan/join processing that the FDW knows how to perform remotely (use create\_foreign\_upper\_path to build them), and call add\_path to add these paths to the indicated upper relation. As with GetForeignJoinPaths, it is not necessary that this function succeed in creating any paths, since paths involving local processing are always possible.

The stage parameter identifies which post-scan/join step is currently being considered. output\_rel is the upper relation that should receive paths representing computation of this step, and input\_rel is the relation representing the input to this step. The extra parameter provides additional details, currently, it is set only for UPPERREL\_PARTIAL\_GROUP\_AGG or UPPER-REL\_GROUP\_AGG, in which case it points to a GroupPathExtraData structure; or for UPPER-REL\_FINAL, in which case it points to a FinalPathExtraData structure. (Note that Foreign-Path paths added to output\_rel would typically not have any direct dependency on paths of the input\_rel, since their processing is expected to be done externally. However, examining paths previously generated for the previous processing step can be useful to avoid redundant planning work.)

See [Section 57.4](#page-164-0) for additional information.

## <span id="page-151-0"></span>**57.2.4. FDW Routines for Updating Foreign Tables**

If an FDW supports writable foreign tables, it should provide some or all of the following callback functions depending on the needs and capabilities of the FDW:

```
void
AddForeignUpdateTargets(PlannerInfo *root,
 Index rtindex,
 RangeTblEntry *target_rte,
 Relation target_relation);
```

UPDATE and DELETE operations are performed against rows previously fetched by the table-scanning functions. The FDW may need extra information, such as a row ID or the values of primary-key columns, to ensure that it can identify the exact row to update or delete. To support that, this function can add extra hidden, or "junk", target columns to the list of columns that are to be retrieved from the foreign table during an UPDATE or DELETE.

To do that, construct a Var representing an extra value you need, and pass it to add\_row\_identity\_var, along with a name for the junk column. (You can do this more than once if several columns are needed.) You must choose a distinct junk column name for each different Var you need, except that Vars that are identical except for the varno field can and should share a column name. The core system uses the junk column names tableoid for a table's tableoid column, ctid or ctidN for ctid, wholerow for a whole-row Var marked with vartype = RECORD, and wholerowN for a whole-row Var with vartype equal to the table's declared row type. Re-use these names when you can (the planner will combine duplicate requests for identical junk columns). If you need another kind of junk column besides these, it might be wise to choose a name prefixed with your extension name, to avoid conflicts against other FDWs.

If the AddForeignUpdateTargets pointer is set to NULL, no extra target expressions are added. (This will make it impossible to implement DELETE operations, though UPDATE may still be feasible if the FDW relies on an unchanging primary key to identify rows.)

```
List *
PlanForeignModify(PlannerInfo *root,
 ModifyTable *plan,
 Index resultRelation,
 int subplan_index);
```

Perform any additional planning actions needed for an insert, update, or delete on a foreign table. This function generates the FDW-private information that will be attached to the ModifyTable plan node that performs the update action. This private information must have the form of a List, and will be delivered to BeginForeignModify during the execution stage.

root is the planner's global information about the query. plan is the ModifyTable plan node, which is complete except for the fdwPrivLists field. resultRelation identifies the target foreign table by its range table index. subplan\_index identifies which target of the ModifyTable plan node this is, counting from zero; use this if you want to index into per-target-relation substructures of the plan node.

See [Section 57.4](#page-164-0) for additional information.

If the PlanForeignModify pointer is set to NULL, no additional plan-time actions are taken, and the fdw\_private list delivered to BeginForeignModify will be NIL.

```
void
BeginForeignModify(ModifyTableState *mtstate,
 ResultRelInfo *rinfo,
 List *fdw_private,
 int subplan_index,
 int eflags);
```

Begin executing a foreign table modification operation. This routine is called during executor startup. It should perform any initialization needed prior to the actual table modifications. Subsequently, ExecForeignInsert/ExecForeignBatchInsert, ExecForeignUpdate or Exec-ForeignDelete will be called for tuple(s) to be inserted, updated, or deleted.

mtstate is the overall state of the ModifyTable plan node being executed; global data about the plan and execution state is available via this structure. rinfo is the ResultRelInfo struct describing the target foreign table. (The ri\_FdwState field of ResultRelInfo is available for the FDW to store any private state it needs for this operation.) fdw\_private contains the private data generated by PlanForeignModify, if any. subplan\_index identifies which target of the ModifyTable plan node this is. eflags contains flag bits describing the executor's operating mode for this plan node.

Note that when (eflags & EXEC\_FLAG\_EXPLAIN\_ONLY) is true, this function should not perform any externally-visible actions; it should only do the minimum required to make the node state valid for ExplainForeignModify and EndForeignModify.

If the BeginForeignModify pointer is set to NULL, no action is taken during executor startup.

```
TupleTableSlot *
ExecForeignInsert(EState *estate,
 ResultRelInfo *rinfo,
 TupleTableSlot *slot,
 TupleTableSlot *planSlot);
```

Insert one tuple into the foreign table. estate is global execution state for the query. rinfo is the ResultRelInfo struct describing the target foreign table. slot contains the tuple to be inserted; it will match the row-type definition of the foreign table. planSlot contains the tuple that was generated by the ModifyTable plan node's subplan; it differs from slot in possibly containing additional "junk" columns. (The planSlot is typically of little interest for INSERT cases, but is provided for completeness.)

The return value is either a slot containing the data that was actually inserted (this might differ from the data supplied, for example as a result of trigger actions), or NULL if no row was actually inserted (again, typically as a result of triggers). The passed-in slot can be re-used for this purpose.

The data in the returned slot is used only if the INSERT statement has a RETURNING clause or involves a view WITH CHECK OPTION; or if the foreign table has an AFTER ROW trigger. Triggers require all columns, but the FDW could choose to optimize away returning some or all columns depending on the contents of the RETURNING clause or WITH CHECK OPTION constraints. Regardless, some slot must be returned to indicate success, or the query's reported row count will be wrong.

If the ExecForeignInsert pointer is set to NULL, attempts to insert into the foreign table will fail with an error message.

Note that this function is also called when inserting routed tuples into a foreign-table partition or executing COPY FROM on a foreign table, in which case it is called in a different way than it is in the INSERT case. See the callback functions described below that allow the FDW to support that.

```
TupleTableSlot **
ExecForeignBatchInsert(EState *estate,
 ResultRelInfo *rinfo,
 TupleTableSlot **slots,
 TupleTableSlot **planSlots,
 int *numSlots);
```

Insert multiple tuples in bulk into the foreign table. The parameters are the same for ExecForeignInsert except slots and planSlots contain multiple tuples and \*numSlots specifies the number of tuples in those arrays.

The return value is an array of slots containing the data that was actually inserted (this might differ from the data supplied, for example as a result of trigger actions.) The passed-in slots can be reused for this purpose. The number of successfully inserted tuples is returned in \*numSlots.

The data in the returned slot is used only if the INSERT statement involves a view WITH CHECK OPTION; or if the foreign table has an AFTER ROW trigger. Triggers require all columns, but the FDW could choose to optimize away returning some or all columns depending on the contents of the WITH CHECK OPTION constraints.

If the ExecForeignBatchInsert or GetForeignModifyBatchSize pointer is set to NULL, attempts to insert into the foreign table will use ExecForeignInsert. This function is not used if the INSERT has the RETURNING clause.

Note that this function is also called when inserting routed tuples into a foreign-table partition. See the callback functions described below that allow the FDW to support that.

```
int
GetForeignModifyBatchSize(ResultRelInfo *rinfo);
```

Report the maximum number of tuples that a single ExecForeignBatchInsert call can handle for the specified foreign table. The executor passes at most the given number of tuples to ExecForeignBatchInsert. rinfo is the ResultRelInfo struct describing the target foreign table. The FDW is expected to provide a foreign server and/or foreign table option for the user to set this value, or some hard-coded value.

If the ExecForeignBatchInsert or GetForeignModifyBatchSize pointer is set to NULL, attempts to insert into the foreign table will use ExecForeignInsert.

```
TupleTableSlot *
ExecForeignUpdate(EState *estate,
 ResultRelInfo *rinfo,
 TupleTableSlot *slot,
 TupleTableSlot *planSlot);
```

Update one tuple in the foreign table. estate is global execution state for the query. rinfo is the ResultRelInfo struct describing the target foreign table. slot contains the new data for the tuple; it will match the row-type definition of the foreign table. planSlot contains the tuple that was generated by the ModifyTable plan node's subplan. Unlike slot, this tuple contains only the new values for columns changed by the query, so do not rely on attribute numbers of the foreign table to index into planSlot. Also, planSlot typically contains additional "junk" columns. In particular, any junk columns that were requested by AddForeignUpdateTargets will be available from this slot.

The return value is either a slot containing the row as it was actually updated (this might differ from the data supplied, for example as a result of trigger actions), or NULL if no row was actually updated (again, typically as a result of triggers). The passed-in slot can be re-used for this purpose.

The data in the returned slot is used only if the UPDATE statement has a RETURNING clause or involves a view WITH CHECK OPTION; or if the foreign table has an AFTER ROW trigger. Triggers require all columns, but the FDW could choose to optimize away returning some or all columns depending on the contents of the RETURNING clause or WITH CHECK OPTION constraints. Regardless, some slot must be returned to indicate success, or the query's reported row count will be wrong.

If the ExecForeignUpdate pointer is set to NULL, attempts to update the foreign table will fail with an error message.

```
TupleTableSlot *
ExecForeignDelete(EState *estate,
 ResultRelInfo *rinfo,
 TupleTableSlot *slot,
 TupleTableSlot *planSlot);
```

Delete one tuple from the foreign table. estate is global execution state for the query. rinfo is the ResultRelInfo struct describing the target foreign table. slot contains nothing useful upon call, but can be used to hold the returned tuple. planSlot contains the tuple that was generated by the ModifyTable plan node's subplan; in particular, it will carry any junk columns that were requested by AddForeignUpdateTargets. The junk column(s) must be used to identify the tuple to be deleted.

The return value is either a slot containing the row that was deleted, or NULL if no row was deleted (typically as a result of triggers). The passed-in slot can be used to hold the tuple to be returned.

The data in the returned slot is used only if the DELETE query has a RETURNING clause or the foreign table has an AFTER ROW trigger. Triggers require all columns, but the FDW could choose to optimize away returning some or all columns depending on the contents of the RETURNING clause. Regardless, some slot must be returned to indicate success, or the query's reported row count will be wrong.

If the ExecForeignDelete pointer is set to NULL, attempts to delete from the foreign table will fail with an error message.

```
void
EndForeignModify(EState *estate,
 ResultRelInfo *rinfo);
```

End the table update and release resources. It is normally not important to release palloc'd memory, but for example open files and connections to remote servers should be cleaned up.

If the EndForeignModify pointer is set to NULL, no action is taken during executor shutdown.

Tuples inserted into a partitioned table by INSERT or COPY FROM are routed to partitions. If an FDW supports routable foreign-table partitions, it should also provide the following callback functions. These functions are also called when COPY FROM is executed on a foreign table.

void

```
BeginForeignInsert(ModifyTableState *mtstate,
 ResultRelInfo *rinfo);
```

Begin executing an insert operation on a foreign table. This routine is called right before the first tuple is inserted into the foreign table in both cases when it is the partition chosen for tuple routing and the target specified in a COPY FROM command. It should perform any initialization needed prior to the actual insertion. Subsequently, ExecForeignInsert or ExecForeignBatchInsert will be called for tuple(s) to be inserted into the foreign table.

mtstate is the overall state of the ModifyTable plan node being executed; global data about the plan and execution state is available via this structure. rinfo is the ResultRelInfo struct describing the target foreign table. (The ri\_FdwState field of ResultRelInfo is available for the FDW to store any private state it needs for this operation.)

When this is called by a COPY FROM command, the plan-related global data in mtstate is not provided and the planSlot parameter of ExecForeignInsert subsequently called for each inserted tuple is NULL, whether the foreign table is the partition chosen for tuple routing or the target specified in the command.

If the BeginForeignInsert pointer is set to NULL, no action is taken for the initialization.

Note that if the FDW does not support routable foreign-table partitions and/or executing COPY FROM on foreign tables, this function or ExecForeignInsert/ExecForeignBatchInsert subsequently called must throw error as needed.

```
void
EndForeignInsert(EState *estate,
 ResultRelInfo *rinfo);
```

End the insert operation and release resources. It is normally not important to release palloc'd memory, but for example open files and connections to remote servers should be cleaned up.

If the EndForeignInsert pointer is set to NULL, no action is taken for the termination.

```
int
IsForeignRelUpdatable(Relation rel);
```

Report which update operations the specified foreign table supports. The return value should be a bit mask of rule event numbers indicating which operations are supported by the foreign table, using the CmdType enumeration; that is, (1 << CMD\_UPDATE) = 4 for UPDATE, (1 << CMD\_INSERT) = 8 for INSERT, and (1 << CMD\_DELETE) = 16 for DELETE.

If the IsForeignRelUpdatable pointer is set to NULL, foreign tables are assumed to be insertable, updatable, or deletable if the FDW provides ExecForeignInsert, ExecForeignUpdate, or ExecForeignDelete respectively. This function is only needed if the FDW supports some tables that are updatable and some that are not. (Even then, it's permissible to throw an error in the execution routine instead of checking in this function. However, this function is used to determine updatability for display in the information\_schema views.)

Some inserts, updates, and deletes to foreign tables can be optimized by implementing an alternative set of interfaces. The ordinary interfaces for inserts, updates, and deletes fetch rows from the remote server and then modify those rows one at a time. In some cases, this row-by-row approach is necessary, but it can be inefficient. If it is possible for the foreign server to determine which rows should be modified without actually retrieving them, and if there are no local structures which would affect the operation (row-level local triggers, stored generated columns, or WITH CHECK OPTION constraints from parent views), then it is possible to arrange things so that the entire operation is performed on the remote server. The interfaces described below make this possible.

```
bool
PlanDirectModify(PlannerInfo *root,
 ModifyTable *plan,
 Index resultRelation,
 int subplan_index);
```

Decide whether it is safe to execute a direct modification on the remote server. If so, return true after performing planning actions needed for that. Otherwise, return false. This optional function is called during query planning. If this function succeeds, BeginDirectModify, IterateDirectModify and EndDirectModify will be called at the execution stage, instead. Otherwise, the table modification will be executed using the table-updating functions described above. The parameters are the same as for PlanForeignModify.

To execute the direct modification on the remote server, this function must rewrite the target subplan with a ForeignScan plan node that executes the direct modification on the remote server. The operation and resultRelation fields of the ForeignScan must be set appropriately. operation must be set to the CmdType enumeration corresponding to the statement kind (that is, CMD\_UPDATE for UPDATE, CMD\_INSERT for INSERT, and CMD\_DELETE for DELETE), and the resultRelation argument must be copied to the resultRelation field.

See [Section 57.4](#page-164-0) for additional information.

If the PlanDirectModify pointer is set to NULL, no attempts to execute a direct modification on the remote server are taken.

```
void
BeginDirectModify(ForeignScanState *node,
 int eflags);
```

Prepare to execute a direct modification on the remote server. This is called during executor startup. It should perform any initialization needed prior to the direct modification (that should be done upon the first call to IterateDirectModify). The ForeignScanState node has already been created, but its fdw\_state field is still NULL. Information about the table to modify is accessible through the ForeignScanState node (in particular, from the underlying ForeignScan plan node, which contains any FDW-private information provided by PlanDirectModify). eflags contains flag bits describing the executor's operating mode for this plan node.

Note that when (eflags & EXEC\_FLAG\_EXPLAIN\_ONLY) is true, this function should not perform any externally-visible actions; it should only do the minimum required to make the node state valid for ExplainDirectModify and EndDirectModify.

If the BeginDirectModify pointer is set to NULL, no attempts to execute a direct modification on the remote server are taken.

```
TupleTableSlot *
IterateDirectModify(ForeignScanState *node);
```

When the INSERT, UPDATE or DELETE query doesn't have a RETURNING clause, just return NULL after a direct modification on the remote server. When the query has the clause, fetch one result containing the data needed for the RETURNING calculation, returning it in a tuple table slot (the node's ScanTupleSlot should be used for this purpose). The data that was actually inserted, updated or deleted must be stored in node->resultRelInfo->ri\_projectReturning->pi\_exprContext->ecxt\_scantuple. Return NULL if no more rows are available. Note that this is called in a short-lived memory context that will be reset between invocations. Create a memory context in BeginDirectModify if you need longer-lived storage, or use the es\_query\_cxt of the node's EState.

The rows returned must match the fdw\_scan\_tlist target list if one was supplied, otherwise they must match the row type of the foreign table being updated. If you choose to optimize away fetching columns that are not needed for the RETURNING calculation, you should insert nulls in those column positions, or else generate a fdw\_scan\_tlist list with those columns omitted.

Whether the query has the clause or not, the query's reported row count must be incremented by the FDW itself. When the query doesn't have the clause, the FDW must also increment the row count for the ForeignScanState node in the EXPLAIN ANALYZE case.

If the IterateDirectModify pointer is set to NULL, no attempts to execute a direct modification on the remote server are taken.

```
void
EndDirectModify(ForeignScanState *node);
```

Clean up following a direct modification on the remote server. It is normally not important to release palloc'd memory, but for example open files and connections to the remote server should be cleaned up.

If the EndDirectModify pointer is set to NULL, no attempts to execute a direct modification on the remote server are taken.