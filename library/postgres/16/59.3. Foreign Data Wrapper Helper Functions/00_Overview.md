---
source: PostgreSQL 16 Reference
title: 00_Overview
---

Several helper functions are exported from the core server so that authors of foreign data wrappers can get easy access to attributes of FDW-related objects, such as FDW options. To use any of these functions, you need to include the header file foreign/foreign.h in your source file. That header also defines the struct types that are returned by these functions.

```
ForeignDataWrapper *
GetForeignDataWrapperExtended(Oid fdwid, bits16 flags);
```

This function returns a ForeignDataWrapper object for the foreign-data wrapper with the given OID. A ForeignDataWrapper object contains properties of the FDW (see foreign/foreign.h for details). flags is a bitwise-or'd bit mask indicating an extra set of options. It can take the value FDW\_MISSING\_OK, in which case a NULL result is returned to the caller instead of an error for an undefined object.

```
ForeignDataWrapper *
GetForeignDataWrapper(Oid fdwid);
```

This function returns a ForeignDataWrapper object for the foreign-data wrapper with the given OID. A ForeignDataWrapper object contains properties of the FDW (see foreign/foreign.h for details).

```
ForeignServer *
GetForeignServerExtended(Oid serverid, bits16 flags);
```

This function returns a ForeignServer object for the foreign server with the given OID. A ForeignServer object contains properties of the server (see foreign/foreign.h for details). flags is a bitwise-or'd bit mask indicating an extra set of options. It can take the value FSV\_MISSING\_OK, in which case a NULL result is returned to the caller instead of an error for an undefined object.

```
ForeignServer *
GetForeignServer(Oid serverid);
```

This function returns a ForeignServer object for the foreign server with the given OID. A ForeignServer object contains properties of the server (see foreign/foreign.h for details).

```
UserMapping *
GetUserMapping(Oid userid, Oid serverid);
```

This function returns a UserMapping object for the user mapping of the given role on the given server. (If there is no mapping for the specific user, it will return the mapping for PUBLIC, or throw error if there is none.) A UserMapping object contains properties of the user mapping (see foreign/foreign.h for details).

```
ForeignTable *
GetForeignTable(Oid relid);
```

This function returns a ForeignTable object for the foreign table with the given OID. A ForeignTable object contains properties of the foreign table (see foreign/foreign.h for details).

```
List *
GetForeignColumnOptions(Oid relid, AttrNumber attnum);
```

This function returns the per-column FDW options for the column with the given foreign table OID and attribute number, in the form of a list of DefElem. NIL is returned if the column has no options.

Some object types have name-based lookup functions in addition to the OID-based ones:

```
ForeignDataWrapper *
GetForeignDataWrapperByName(const char *name, bool missing_ok);
```

This function returns a ForeignDataWrapper object for the foreign-data wrapper with the given name. If the wrapper is not found, return NULL if missing\_ok is true, otherwise raise an error.

```
ForeignServer *
GetForeignServerByName(const char *name, bool missing_ok);
```

This function returns a ForeignServer object for the foreign server with the given name. If the server is not found, return NULL if missing\_ok is true, otherwise raise an error.

# <span id="page-64-0"></span>**59.4. Foreign Data Wrapper Query Planning**

The FDW callback functions GetForeignRelSize, GetForeignPaths, GetForeign-Plan, PlanForeignModify, GetForeignJoinPaths, GetForeignUpperPaths, and PlanDirectModify must fit into the workings of the PostgreSQL planner. Here are some notes about what they must do.

The information in root and baserel can be used to reduce the amount of information that has to be fetched from the foreign table (and therefore reduce the cost). baserel->baserestrictinfo is particularly interesting, as it contains restriction quals (WHERE clauses) that should be used to filter the rows to be fetched. (The FDW itself is not required to enforce these quals, as the core executor can check them instead.) baserel->reltarget->exprs can be used to determine which columns need to be fetched; but note that it only lists columns that have to be emitted by the ForeignScan plan node, not columns that are used in qual evaluation but not output by the query.

Various private fields are available for the FDW planning functions to keep information in. Generally, whatever you store in FDW private fields should be palloc'd, so that it will be reclaimed at the end of planning.

baserel->fdw\_private is a void pointer that is available for FDW planning functions to store information relevant to the particular foreign table. The core planner does not touch it except to initialize it to NULL when the RelOptInfo node is created. It is useful for passing information forward from GetForeignRelSize to GetForeignPaths and/or GetForeignPaths to GetForeignPlan, thereby avoiding recalculation.

GetForeignPaths can identify the meaning of different access paths by storing private information in the fdw\_private field of ForeignPath nodes. fdw\_private is declared as a List pointer, but could actually contain anything since the core planner does not touch it. However, best practice is to use a representation that's dumpable by nodeToString, for use with debugging support available in the backend.

GetForeignPlan can examine the fdw\_private field of the selected ForeignPath node, and can generate fdw\_exprs and fdw\_private lists to be placed in the ForeignScan plan node, where they will be available at execution time. Both of these lists must be represented in a form that copyObject knows how to copy. The fdw\_private list has no other restrictions and is not interpreted by the core backend in any way. The fdw\_exprs list, if not NIL, is expected to contain expression trees that are intended to be executed at run time. These trees will undergo post-processing by the planner to make them fully executable.

In GetForeignPlan, generally the passed-in target list can be copied into the plan node as-is. The passed scan\_clauses list contains the same clauses as baserel->baserestrictinfo, but may be re-ordered for better execution efficiency. In simple cases the FDW can just strip RestrictInfo nodes from the scan\_clauses list (using extract\_actual\_clauses) and put all the clauses into the plan node's qual list, which means that all the clauses will be checked by the executor at run time. More complex FDWs may be able to check some of the clauses internally, in which case those clauses can be removed from the plan node's qual list so that the executor doesn't waste time rechecking them.

As an example, the FDW might identify some restriction clauses of the form foreign\_variable = sub\_expression, which it determines can be executed on the remote server given the locally-evaluated value of the sub\_expression. The actual identification of such a clause should happen during GetForeignPaths, since it would affect the cost estimate for the path. The path's fdw\_private field would probably include a pointer to the identified clause's RestrictInfo node. Then GetForeignPlan would remove that clause from scan\_clauses, but add the sub\_expression to fdw\_exprs to ensure that it gets massaged into executable form. It would probably also put control information into the plan node's fdw\_private field to tell the execution functions what to do at run time. The query transmitted to the remote server would involve something like WHERE foreign\_variable = \$1, with the parameter value obtained at run time from evaluation of the fdw\_exprs expression tree.

Any clauses removed from the plan node's qual list must instead be added to fdw\_recheck\_quals or rechecked by RecheckForeignScan in order to ensure correct behavior at the READ COM-MITTED isolation level. When a concurrent update occurs for some other table involved in the query, the executor may need to verify that all of the original quals are still satisfied for the tuple, possibly against a different set of parameter values. Using fdw\_recheck\_quals is typically easier than implementing checks inside RecheckForeignScan, but this method will be insufficient when outer joins have been pushed down, since the join tuples in that case might have some fields go to NULL without rejecting the tuple entirely.

Another ForeignScan field that can be filled by FDWs is fdw\_scan\_tlist, which describes the tuples returned by the FDW for this plan node. For simple foreign table scans this can be set to NIL, implying that the returned tuples have the row type declared for the foreign table. A non-NIL value must be a target list (list of TargetEntrys) containing Vars and/or expressions representing the returned columns. This might be used, for example, to show that the FDW has omitted some columns that it noticed won't be needed for the query. Also, if the FDW can compute expressions used by the query more cheaply than can be done locally, it could add those expressions to fdw\_scan\_tlist. Note that join plans (created from paths made by GetForeignJoinPaths) must always supply fdw\_scan\_tlist to describe the set of columns they will return.

The FDW should always construct at least one path that depends only on the table's restriction clauses. In join queries, it might also choose to construct path(s) that depend on join clauses, for example foreign\_variable = local\_variable. Such clauses will not be found in baserel->baserestrictinfo but must be sought in the relation's join lists. A path using such a clause is called a "parameterized path". It must identify the other relations used in the selected join clause(s) with a suitable value of param\_info; use get\_baserel\_parampathinfo to compute that value. In GetForeignPlan, the local\_variable portion of the join clause would be added to fdw\_exprs, and then at run time the case works the same as for an ordinary restriction clause.

If an FDW supports remote joins, GetForeignJoinPaths should produce ForeignPaths for potential remote joins in much the same way as GetForeignPaths works for base tables. Information about the intended join can be passed forward to GetForeignPlan in the same ways described above. However, baserestrictinfo is not relevant for join relations; instead, the relevant join clauses for a particular join are passed to GetForeignJoinPaths as a separate parameter (extra->restrictlist).

An FDW might additionally support direct execution of some plan actions that are above the level of scans and joins, such as grouping or aggregation. To offer such options, the FDW should generate paths and insert them into the appropriate *upper relation*. For example, a path representing remote aggregation should be inserted into the UPPERREL\_GROUP\_AGG relation, using add\_path. This path will be compared on a cost basis with local aggregation performed by reading a simple scan path for the foreign relation (note that such a path must also be supplied, else there will be an error at plan time). If the remote-aggregation path wins, which it usually would, it will be converted into a plan in the usual way, by calling GetForeignPlan. The recommended place to generate such paths is in the GetForeignUpperPaths callback function, which is called for each upper relation (i.e., each post-scan/join processing step), if all the base relations of the query come from the same FDW.

PlanForeignModify and the other callbacks described in [Section 59.2.4](#page-51-0) are designed around the assumption that the foreign relation will be scanned in the usual way and then individual row updates will be driven by a local ModifyTable plan node. This approach is necessary for the general case where an update requires reading local tables as well as foreign tables. However, if the operation could be executed entirely by the foreign server, the FDW could generate a path representing that and insert it into the UPPERREL\_FINAL upper relation, where it would compete against the ModifyTable approach. This approach could also be used to implement remote SELECT FOR UPDATE, rather than using the row locking callbacks described in [Section 59.2.6.](#page-58-0) Keep in mind that a path inserted into UPPERREL\_FINAL is responsible for implementing *all* behavior of the query.

When planning an UPDATE or DELETE, PlanForeignModify and PlanDirectModify can look up the RelOptInfo struct for the foreign table and make use of the baserel->fdw\_private data previously created by the scan-planning functions. However, in INSERT the target table is not scanned so there is no RelOptInfo for it. The List returned by PlanForeignModify has the same restrictions as the fdw\_private list of a ForeignScan plan node, that is it must contain only structures that copyObject knows how to copy.

INSERT with an ON CONFLICT clause does not support specifying the conflict target, as unique constraints or exclusion constraints on remote tables are not locally known. This in turn implies that ON CONFLICT DO UPDATE is not supported, since the specification is mandatory there.

# <span id="page-67-0"></span>**59.5. Row Locking in Foreign Data Wrappers**

If an FDW's underlying storage mechanism has a concept of locking individual rows to prevent concurrent updates of those rows, it is usually worthwhile for the FDW to perform row-level locking with as close an approximation as practical to the semantics used in ordinary PostgreSQL tables. There are multiple considerations involved in this.

One key decision to be made is whether to perform *early locking* or *late locking*. In early locking, a row is locked when it is first retrieved from the underlying store, while in late locking, the row is locked only when it is known that it needs to be locked. (The difference arises because some rows may be discarded by locally-checked restriction or join conditions.) Early locking is much simpler and avoids extra round trips to a remote store, but it can cause locking of rows that need not have been locked, resulting in reduced concurrency or even unexpected deadlocks. Also, late locking is only possible if the row to be locked can be uniquely re-identified later. Preferably the row identifier should identify a specific version of the row, as PostgreSQL TIDs do.

By default, PostgreSQL ignores locking considerations when interfacing to FDWs, but an FDW can perform early locking without any explicit support from the core code. The API functions described in [Section 59.2.6,](#page-58-0) which were added in PostgreSQL 9.5, allow an FDW to use late locking if it wishes.

An additional consideration is that in READ COMMITTED isolation mode, PostgreSQL may need to re-check restriction and join conditions against an updated version of some target tuple. Rechecking join conditions requires re-obtaining copies of the non-target rows that were previously joined to the target tuple. When working with standard PostgreSQL tables, this is done by including the TIDs of the non-target tables in the column list projected through the join, and then re-fetching non-target rows when required. This approach keeps the join data set compact, but it requires inexpensive re-fetch capability, as well as a TID that can uniquely identify the row version to be re-fetched. By default, therefore, the approach used with foreign tables is to include a copy of the entire row fetched from a foreign table in the column list projected through the join. This puts no special demands on the FDW but can result in reduced performance of merge and hash joins. An FDW that is capable of meeting the re-fetch requirements can choose to do it the first way.

For an UPDATE or DELETE on a foreign table, it is recommended that the ForeignScan operation on the target table perform early locking on the rows that it fetches, perhaps via the equivalent of SELECT FOR UPDATE. An FDW can detect whether a table is an UPDATE/DELETE target at plan time by comparing its relid to root->parse->resultRelation, or at execution time by using ExecRelationIsTargetRelation(). An alternative possibility is to perform late locking within the ExecForeignUpdate or ExecForeignDelete callback, but no special support is provided for this.

For foreign tables that are specified to be locked by a SELECT FOR UPDATE/SHARE command, the ForeignScan operation can again perform early locking by fetching tuples with the equivalent of SELECT FOR UPDATE/SHARE. To perform late locking instead, provide the callback functions defined in [Section 59.2.6](#page-58-0). In GetForeignRowMarkType, select rowmark option ROW\_MARK\_EX-CLUSIVE, ROW\_MARK\_NOKEYEXCLUSIVE, ROW\_MARK\_SHARE, or ROW\_MARK\_KEYSHARE depending on the requested lock strength. (The core code will act the same regardless of which of these four options you choose.) Elsewhere, you can detect whether a foreign table was specified to be locked by this type of command by using get\_plan\_rowmark at plan time, or ExecFindRowMark at execution time; you must check not only whether a non-null rowmark struct is returned, but that its strength field is not LCS\_NONE.

Lastly, for foreign tables that are used in an UPDATE, DELETE or SELECT FOR UPDATE/SHARE command but are not specified to be row-locked, you can override the default choice to copy entire rows by having GetForeignRowMarkType select option ROW\_MARK\_REFERENCE when it sees lock strength LCS\_NONE. This will cause RefetchForeignRow to be called with that value for markType; it should then re-fetch the row without acquiring any new lock. (If you have a GetForeignRowMarkType function but don't wish to re-fetch unlocked rows, select option ROW\_MARK\_COPY for LCS\_NONE.)

See src/include/nodes/lockoptions.h, the comments for RowMarkType and Plan-RowMark in src/include/nodes/plannodes.h, and the comments for ExecRowMark in src/include/nodes/execnodes.h for additional information.