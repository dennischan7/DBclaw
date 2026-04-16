---
source: PostgreSQL 16 Reference
title: 00_Overview
---

If a query that is expected to do so does not produce a parallel plan, you can try reducing parallel\_setup\_cost or parallel\_tuple\_cost. Of course, this plan may turn out to be slower than the serial plan that the planner preferred, but this will not always be the case. If you don't get a parallel plan even with very small values of these settings (e.g., after setting them both to zero), there may be some reason why the query planner is unable to generate a parallel plan for your query. See [Section 15.2](#page-163-0) and [Section 15.4](#page-166-0) for information on why this may be the case.

When executing a parallel plan, you can use EXPLAIN (ANALYZE, VERBOSE) to display perworker statistics for each plan node. This may be useful in determining whether the work is being evenly distributed between all plan nodes and more generally in understanding the performance characteristics of the plan.

# <span id="page-166-0"></span>**15.4. Parallel Safety**

The planner classifies operations involved in a query as either *parallel safe*, *parallel restricted*, or *parallel unsafe*. A parallel safe operation is one that does not conflict with the use of parallel query. A parallel restricted operation is one that cannot be performed in a parallel worker, but that can be performed in the leader while parallel query is in use. Therefore, parallel restricted operations can never occur below a Gather or Gather Merge node, but can occur elsewhere in a plan that contains such a node. A parallel unsafe operation is one that cannot be performed while parallel query is in use, not even in the leader. When a query contains anything that is parallel unsafe, parallel query is completely disabled for that query.

The following operations are always parallel restricted:

- Scans of common table expressions (CTEs).
- Scans of temporary tables.
- Scans of foreign tables, unless the foreign data wrapper has an IsForeignScanParallelSafe API that indicates otherwise.
- Plan nodes to which an InitPlan is attached.
- Plan nodes that reference a correlated SubPlan.