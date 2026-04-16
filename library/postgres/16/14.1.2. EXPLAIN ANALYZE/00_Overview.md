---
source: PostgreSQL 16 Reference
title: 00_Overview
---

It is possible to check the accuracy of the planner's estimates by using EXPLAIN's ANALYZE option. With this option, EXPLAIN actually executes the query, and then displays the true row counts and true run time accumulated within each plan node, along with the same estimates that a plain EXPLAIN shows. For example, we might get a result like this:

```
EXPLAIN ANALYZE SELECT *
FROM tenk1 t1, tenk2 t2
WHERE t1.unique1 < 10 AND t1.unique2 = t2.unique2;
 QUERY
 PLAN
-------------------------------------------------------------------
--------------------------------------------------------------
 Nested Loop (cost=4.65..118.62 rows=10 width=488) (actual
 time=0.128..0.377 rows=10 loops=1)
 -> Bitmap Heap Scan on tenk1 t1 (cost=4.36..39.47 rows=10
 width=244) (actual time=0.057..0.121 rows=10 loops=1)
 Recheck Cond: (unique1 < 10)
 -> Bitmap Index Scan on tenk1_unique1 (cost=0.00..4.36
 rows=10 width=0) (actual time=0.024..0.024 rows=10 loops=1)
 Index Cond: (unique1 < 10)
 -> Index Scan using tenk2_unique2 on tenk2 t2 (cost=0.29..7.91
 rows=1 width=244) (actual time=0.021..0.022 rows=1 loops=10)
 Index Cond: (unique2 = t1.unique2)
 Planning time: 0.181 ms
 Execution time: 0.501 ms
```

Note that the "actual time" values are in milliseconds of real time, whereas the cost estimates are expressed in arbitrary units; so they are unlikely to match up. The thing that's usually most important to look for is whether the estimated row counts are reasonably close to reality. In this example the estimates were all dead-on, but that's quite unusual in practice.

In some query plans, it is possible for a subplan node to be executed more than once. For example, the inner index scan will be executed once per outer row in the above nested-loop plan. In such cases, the loops value reports the total number of executions of the node, and the actual time and rows values shown are averages per-execution. This is done to make the numbers comparable with the way that the cost estimates are shown. Multiply by the loops value to get the total time actually spent in the node. In the above example, we spent a total of 0.220 milliseconds executing the index scans on tenk2.

In some cases EXPLAIN ANALYZE shows additional execution statistics beyond the plan node execution times and row counts. For example, Sort and Hash nodes provide extra information:

```
EXPLAIN ANALYZE SELECT *
FROM tenk1 t1, tenk2 t2
WHERE t1.unique1 < 100 AND t1.unique2 = t2.unique2 ORDER BY
 t1.fivethous;
 QUERY PLAN
-------------------------------------------------------------------
-------------------------------------------------------------------
------
 Sort (cost=717.34..717.59 rows=101 width=488) (actual
 time=7.761..7.774 rows=100 loops=1)
 Sort Key: t1.fivethous
 Sort Method: quicksort Memory: 77kB
 -> Hash Join (cost=230.47..713.98 rows=101 width=488) (actual
 time=0.711..7.427 rows=100 loops=1)
 Hash Cond: (t2.unique2 = t1.unique2)
```

```
 -> Seq Scan on tenk2 t2 (cost=0.00..445.00 rows=10000
 width=244) (actual time=0.007..2.583 rows=10000 loops=1)
 -> Hash (cost=229.20..229.20 rows=101 width=244) (actual
 time=0.659..0.659 rows=100 loops=1)
 Buckets: 1024 Batches: 1 Memory Usage: 28kB
 -> Bitmap Heap Scan on tenk1 t1 (cost=5.07..229.20
 rows=101 width=244) (actual time=0.080..0.526 rows=100 loops=1)
 Recheck Cond: (unique1 < 100)
 -> Bitmap Index Scan on tenk1_unique1 
 (cost=0.00..5.04 rows=101 width=0) (actual time=0.049..0.049
 rows=100 loops=1)
 Index Cond: (unique1 < 100)
 Planning time: 0.194 ms
 Execution time: 8.008 ms
```

The Sort node shows the sort method used (in particular, whether the sort was in-memory or on-disk) and the amount of memory or disk space needed. The Hash node shows the number of hash buckets and batches as well as the peak amount of memory used for the hash table. (If the number of batches exceeds one, there will also be disk space usage involved, but that is not shown.)

Another type of extra information is the number of rows removed by a filter condition:

```
EXPLAIN ANALYZE SELECT * FROM tenk1 WHERE ten < 7;
 QUERY PLAN
-------------------------------------------------------------------
--------------------------------------
 Seq Scan on tenk1 (cost=0.00..483.00 rows=7000 width=244) (actual
 time=0.016..5.107 rows=7000 loops=1)
 Filter: (ten < 7)
 Rows Removed by Filter: 3000
 Planning time: 0.083 ms
 Execution time: 5.905 ms
```

These counts can be particularly valuable for filter conditions applied at join nodes. The "Rows Removed" line only appears when at least one scanned row, or potential join pair in the case of a join node, is rejected by the filter condition.

A case similar to filter conditions occurs with "lossy" index scans. For example, consider this search for polygons containing a specific point:

```
EXPLAIN ANALYZE SELECT * FROM polygon_tbl WHERE f1 @> polygon
 '(0.5,2.0)';
 QUERY PLAN
-------------------------------------------------------------------
-----------------------------------
 Seq Scan on polygon_tbl (cost=0.00..1.05 rows=1 width=32) (actual
 time=0.044..0.044 rows=0 loops=1)
 Filter: (f1 @> '((0.5,2))'::polygon)
 Rows Removed by Filter: 4
 Planning time: 0.040 ms
 Execution time: 0.083 ms
```

The planner thinks (quite correctly) that this sample table is too small to bother with an index scan, so we have a plain sequential scan in which all the rows got rejected by the filter condition. But if we force an index scan to be used, we see:

```
SET enable_seqscan TO off;
EXPLAIN ANALYZE SELECT * FROM polygon_tbl WHERE f1 @> polygon
 '(0.5,2.0)';
 QUERY PLAN
-------------------------------------------------------------------
-------------------------------------------------------
 Index Scan using gpolygonind on polygon_tbl (cost=0.13..8.15
 rows=1 width=32) (actual time=0.062..0.062 rows=0 loops=1)
 Index Cond: (f1 @> '((0.5,2))'::polygon)
 Rows Removed by Index Recheck: 1
 Planning time: 0.034 ms
 Execution time: 0.144 ms
```

Here we can see that the index returned one candidate row, which was then rejected by a recheck of the index condition. This happens because a GiST index is "lossy" for polygon containment tests: it actually returns the rows with polygons that overlap the target, and then we have to do the exact containment test on those rows.

EXPLAIN has a BUFFERS option that can be used with ANALYZE to get even more run time statistics:

```
EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM tenk1 WHERE unique1 < 100
 AND unique2 > 9000;
```

QUERY

PLAN

-------------------------------------------------------------------

```
--------------------------------------------------------------
 Bitmap Heap Scan on tenk1 (cost=25.08..60.21 rows=10 width=244)
 (actual time=0.323..0.342 rows=10 loops=1)
 Recheck Cond: ((unique1 < 100) AND (unique2 > 9000))
 Buffers: shared hit=15
 -> BitmapAnd (cost=25.08..25.08 rows=10 width=0) (actual
 time=0.309..0.309 rows=0 loops=1)
 Buffers: shared hit=7
 -> Bitmap Index Scan on tenk1_unique1 (cost=0.00..5.04
 rows=101 width=0) (actual time=0.043..0.043 rows=100 loops=1)
 Index Cond: (unique1 < 100)
 Buffers: shared hit=2
 -> Bitmap Index Scan on tenk1_unique2 (cost=0.00..19.78
 rows=999 width=0) (actual time=0.227..0.227 rows=999 loops=1)
 Index Cond: (unique2 > 9000)
 Buffers: shared hit=5
 Planning time: 0.088 ms
 Execution time: 0.423 ms
```

The numbers provided by BUFFERS help to identify which parts of the query are the most I/O-intensive.

Keep in mind that because EXPLAIN ANALYZE actually runs the query, any side-effects will happen as usual, even though whatever results the query might output are discarded in favor of printing the EXPLAIN data. If you want to analyze a data-modifying query without changing your tables, you can roll the command back afterwards, for example:

BEGIN;

```
EXPLAIN ANALYZE UPDATE tenk1 SET hundred = hundred + 1 WHERE
 unique1 < 100;
```

QUERY

PLAN

```
-------------------------------------------------------------------
-------------------------------------------------------------
 Update on tenk1 (cost=5.08..230.08 rows=0 width=0) (actual
 time=3.791..3.792 rows=0 loops=1)
 -> Bitmap Heap Scan on tenk1 (cost=5.08..230.08 rows=102
 width=10) (actual time=0.069..0.513 rows=100 loops=1)
 Recheck Cond: (unique1 < 100)
 Heap Blocks: exact=90
 -> Bitmap Index Scan on tenk1_unique1 (cost=0.00..5.05
 rows=102 width=0) (actual time=0.036..0.037 rows=300 loops=1)
 Index Cond: (unique1 < 100)
 Planning Time: 0.113 ms
```

ROLLBACK;

Execution Time: 3.850 ms

As seen in this example, when the query is an INSERT, UPDATE, DELETE, or MERGE command, the actual work of applying the table changes is done by a top-level Insert, Update, Delete, or Merge plan node. The plan nodes underneath this node perform the work of locating the old rows and/or computing the new data. So above, we see the same sort of bitmap table scan we've seen already, and its output is fed to an Update node that stores the updated rows. It's worth noting that although the data-modifying node can take a considerable amount of run time (here, it's consuming the lion's share of the time), the planner does not currently add anything to the cost estimates to account for that work. That's because the work to be done is the same for every correct query plan, so it doesn't affect planning decisions.

When an UPDATE, DELETE, or MERGE command affects an inheritance hierarchy, the output might look like this:

```
EXPLAIN UPDATE parent SET f2 = f2 + 1 WHERE f1 = 101;
 QUERY PLAN
-------------------------------------------------------------------
-----------------------------------
 Update on parent (cost=0.00..24.59 rows=0 width=0)
 Update on parent parent_1
 Update on child1 parent_2
 Update on child2 parent_3
 Update on child3 parent_4
 -> Result (cost=0.00..24.59 rows=4 width=14)
 -> Append (cost=0.00..24.54 rows=4 width=14)
 -> Seq Scan on parent parent_1 (cost=0.00..0.00
 rows=1 width=14)
 Filter: (f1 = 101)
 -> Index Scan using child1_pkey on child1 parent_2 
 (cost=0.15..8.17 rows=1 width=14)
 Index Cond: (f1 = 101)
 -> Index Scan using child2_pkey on child2 parent_3 
 (cost=0.15..8.17 rows=1 width=14)
 Index Cond: (f1 = 101)
 -> Index Scan using child3_pkey on child3 parent_4 
 (cost=0.15..8.17 rows=1 width=14)
 Index Cond: (f1 = 101)
```

In this example the Update node needs to consider three child tables as well as the originally-mentioned parent table. So there are four input scanning subplans, one per table. For clarity, the Update node is annotated to show the specific target tables that will be updated, in the same order as the corresponding subplans.

The Planning time shown by EXPLAIN ANALYZE is the time it took to generate the query plan from the parsed query and optimize it. It does not include parsing or rewriting.

The Execution time shown by EXPLAIN ANALYZE includes executor start-up and shut-down time, as well as the time to run any triggers that are fired, but it does not include parsing, rewriting, or planning time. Time spent executing BEFORE triggers, if any, is included in the time for the related Insert, Update, or Delete node; but time spent executing AFTER triggers is not counted there because AFTER triggers are fired after completion of the whole plan. The total time spent in each trigger (either BEFORE or AFTER) is also shown separately. Note that deferred constraint triggers will not be executed until end of transaction and are thus not considered at all by EXPLAIN ANALYZE.