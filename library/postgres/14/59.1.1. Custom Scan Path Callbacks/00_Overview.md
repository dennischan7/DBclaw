---
source: PostgreSQL 14 Reference
title: 00_Overview
---

```
Plan *(*PlanCustomPath) (PlannerInfo *root,
 RelOptInfo *rel,
 CustomPath *best_path,
 List *tlist,
 List *clauses,
 List *custom_plans);
```

Convert a custom path to a finished plan. The return value will generally be a CustomScan object, which the callback must allocate and initialize. See [Section 59.2](#page-172-0) for more details.

```
List *(*ReparameterizeCustomPathByChild) (PlannerInfo *root,
 List *custom_private,
 RelOptInfo *child_rel);
```

This callback is called while converting a path parameterized by the top-most parent of the given child relation child\_rel to be parameterized by the child relation. The callback is used to reparameterize any paths or translate any expression nodes saved in the given custom\_private member of a CustomPath. The callback may use reparameterize\_path\_by\_child, adjust\_appendrel\_attrs or adjust\_appendrel\_attrs\_multilevel as required.

# <span id="page-172-0"></span>**59.2. Creating Custom Scan Plans**

A custom scan is represented in a finished plan tree using the following structure:

```
typedef struct CustomScan
{
 Scan scan;
 uint32 flags;
 List *custom_plans;
 List *custom_exprs;
 List *custom_private;
 List *custom_scan_tlist;
 Bitmapset *custom_relids;
 const CustomScanMethods *methods;
```

```
} CustomScan;
```

scan must be initialized as for any other scan, including estimated costs, target lists, qualifications, and so on. flags is a bit mask with the same meaning as in CustomPath. custom\_plans can be used to store child Plan nodes. custom\_exprs should be used to store expression trees that will need to be fixed up by setrefs.c and subselect.c, while custom\_private should be used to store other private data that is only used by the custom scan provider itself. custom\_scan\_tlist can be NIL when scanning a base relation, indicating that the custom scan returns scan tuples that match the base relation's row type. Otherwise it is a target list describing the actual scan tuples. custom\_scan\_tlist must be provided for joins, and could be provided for scans if the custom scan provider can compute some non-Var expressions. custom\_relids is set by the core code to the set of relations (range table indexes) that this scan node handles; except when this scan is replacing a join, it will have only one member. methods must point to a (usually statically allocated) object implementing the required custom scan methods, which are further detailed below.

When a CustomScan scans a single relation, scan.scanrelid must be the range table index of the table to be scanned. When it replaces a join, scan.scanrelid should be zero.

Plan trees must be able to be duplicated using copyObject, so all the data stored within the "custom" fields must consist of nodes that that function can handle. Furthermore, custom scan providers cannot substitute a larger structure that embeds a CustomScan for the structure itself, as would be possible for a CustomPath or CustomScanState.