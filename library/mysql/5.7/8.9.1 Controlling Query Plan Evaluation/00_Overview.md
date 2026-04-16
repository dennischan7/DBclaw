---
source: MySQL 5.7 Reference
title: 00_Overview
---

The task of the query optimizer is to find an optimal plan for executing an SQL query. Because the difference in performance between "good" and "bad" plans can be orders of magnitude (that is, seconds versus hours or even days), most query optimizers, including that of MySQL, perform a more or less exhaustive search for an optimal plan among all possible query evaluation plans. For join queries, the number of possible plans investigated by the MySQL optimizer grows exponentially with the number of tables referenced in a query. For small numbers of tables (typically less than 7 to 10) this is not a problem. However, when larger queries are submitted, the time spent in query optimization may easily become the major bottleneck in the server's performance.

A more flexible method for query optimization enables the user to control how exhaustive the optimizer is in its search for an optimal query evaluation plan. The general idea is that the fewer plans that are investigated by the optimizer, the less time it spends in compiling a query. On the other hand, because the optimizer skips some plans, it may miss finding an optimal plan.

The behavior of the optimizer with respect to the number of plans it evaluates can be controlled using two system variables:

• The optimizer\_prune\_level variable tells the optimizer to skip certain plans based on estimates of the number of rows accessed for each table. Our experience shows that this kind of "educated guess" rarely misses optimal plans, and may dramatically reduce query compilation

times. That is why this option is on (optimizer\_prune\_level=1) by default. However, if you believe that the optimizer missed a better query plan, this option can be switched off (optimizer\_prune\_level=0) with the risk that query compilation may take much longer. Note that, even with the use of this heuristic, the optimizer still explores a roughly exponential number of plans.

• The optimizer\_search\_depth variable tells how far into the "future" of each incomplete plan the optimizer should look to evaluate whether it should be expanded further. Smaller values of optimizer\_search\_depth may result in orders of magnitude smaller query compilation times. For example, queries with 12, 13, or more tables may easily require hours and even days to compile if optimizer\_search\_depth is close to the number of tables in the query. At the same time, if compiled with optimizer\_search\_depth equal to 3 or 4, the optimizer may compile in less than a minute for the same query. If you are unsure of what a reasonable value is for optimizer\_search\_depth, this variable can be set to 0 to tell the optimizer to determine the value automatically.

## <span id="page-86-0"></span>**8.9.2 Switchable Optimizations**

The optimizer\_switch system variable enables control over optimizer behavior. Its value is a set of flags, each of which has a value of on or off to indicate whether the corresponding optimizer behavior is enabled or disabled. This variable has global and session values and can be changed at runtime. The global default can be set at server startup.

To see the current set of optimizer flags, select the variable value:

```
mysql> SELECT @@optimizer_switch\G
*************************** 1. row ***************************
@@optimizer_switch: index_merge=on,index_merge_union=on,
 index_merge_sort_union=on,
 index_merge_intersection=on,
 engine_condition_pushdown=on,
 index_condition_pushdown=on,
 mrr=on,mrr_cost_based=on,
 block_nested_loop=on,batched_key_access=off,
 materialization=on,semijoin=on,loosescan=on,
 firstmatch=on,duplicateweedout=on,
 subquery_materialization_cost_based=on,
 use_index_extensions=on,
 condition_fanout_filter=on,derived_merge=on,
 prefer_ordering_index=on
```

To change the value of optimizer\_switch, assign a value consisting of a comma-separated list of one or more commands:

```
SET [GLOBAL|SESSION] optimizer_switch='command[,command]...';
```

Each command value should have one of the forms shown in the following table.

| Command Syntax   | Meaning                                         |
|------------------|-------------------------------------------------|
| default          | Reset every optimization to its default value   |
| opt_name=default | Set the named optimization to its default value |
| opt_name=off     | Disable the named optimization                  |
| opt_name=on      | Enable the named optimization                   |

The order of the commands in the value does not matter, although the default command is executed first if present. Setting an opt\_name flag to default sets it to whichever of on or off is its default value. Specifying any given opt\_name more than once in the value is not permitted and causes an error. Any errors in the value cause the assignment to fail with an error, leaving the value of optimizer\_switch unchanged.

The following list describes the permissible opt\_name flag names, grouped by optimization strategy:

- <span id="page-87-2"></span>• Batched Key Access Flags
  - [batched\\_key\\_access](#page-87-2) (default off)

Controls use of BKA join algorithm.

For [batched\\_key\\_access](#page-87-2) to have any effect when set to on, the [mrr](#page-88-5) flag must also be on. Currently, the cost estimation for MRR is too pessimistic. Hence, it is also necessary for [mrr\\_cost\\_based](#page-88-6) to be off for BKA to be used.

For more information, see Section 8.2.1.11, "Block Nested-Loop and Batched Key Access Joins".

- <span id="page-87-3"></span>• Block Nested-Loop Flags
  - [block\\_nested\\_loop](#page-87-3) (default on)

Controls use of BNL join algorithm.

For more information, see Section 8.2.1.11, "Block Nested-Loop and Batched Key Access Joins".

- <span id="page-87-4"></span>• Condition Filtering Flags
  - [condition\\_fanout\\_filter](#page-87-4) (default on)

Controls use of condition filtering.

For more information, see Section 8.2.1.12, "Condition Filtering".

- <span id="page-87-0"></span>• Derived Table Merging Flags
  - [derived\\_merge](#page-87-0) (default on)

Controls merging of derived tables and views into outer query block.

The [derived\\_merge](#page-87-0) flag controls whether the optimizer attempts to merge derived tables and view references into the outer query block, assuming that no other rule prevents merging; for example, an ALGORITHM directive for a view takes precedence over the [derived\\_merge](#page-87-0) setting. By default, the flag is on to enable merging.

For more information, see [Section 8.2.2.4, "Optimizing Derived Tables and View References with](#page-21-0) [Merging or Materialization"](#page-21-0).

- <span id="page-87-5"></span>• Engine Condition Pushdown Flags
  - [engine\\_condition\\_pushdown](#page-87-5) (default on)

Controls engine condition pushdown.

For more information, see Section 8.2.1.4, "Engine Condition Pushdown Optimization".

- <span id="page-87-6"></span>• Index Condition Pushdown Flags
  - [index\\_condition\\_pushdown](#page-87-6) (default on)

Controls index condition pushdown.

For more information, see Section 8.2.1.5, "Index Condition Pushdown Optimization".

- <span id="page-87-1"></span>• Index Extensions Flags
  - [use\\_index\\_extensions](#page-87-1) (default on)

Controls use of index extensions.

For more information, see [Section 8.3.9, "Use of Index Extensions".](#page-38-0)

- <span id="page-88-4"></span>• Index Merge Flags
  - [index\\_merge](#page-88-4) (default on)

Controls all Index Merge optimizations.

<span id="page-88-7"></span>• [index\\_merge\\_intersection](#page-88-7) (default on)

Controls the Index Merge Intersection Access optimization.

<span id="page-88-8"></span>• [index\\_merge\\_sort\\_union](#page-88-8) (default on)

Controls the Index Merge Sort-Union Access optimization.

<span id="page-88-9"></span>• [index\\_merge\\_union](#page-88-9) (default on)

Controls the Index Merge Union Access optimization.

For more information, see Section 8.2.1.3, "Index Merge Optimization".

- <span id="page-88-0"></span>• Limit Optimization Flags
  - [prefer\\_ordering\\_index](#page-88-0) (default on)

Controls whether, in the case of a query having an ORDER BY or GROUP BY with a LIMIT clause, the optimizer tries to use an ordered index instead of an unordered index, a filesort, or some other optimization. This optimzation is performed by default whenever the optimizer determines that using it would allow for faster execution of the query.

Because the algorithm that makes this determination cannot handle every conceivable case (due in part to the assumption that the distribution of data is always more or less uniform), there are cases in which this optimization may not be desirable. Prior to MySQL 5.7.33, it ws not possible to disable this optimization, but in MySQL 5.7.33 and later, while it remains the default behavior, it can be disabled by setting the [prefer\\_ordering\\_index](#page-88-0) flag to off.

For more information and examples, see [Section 8.2.1.17, "LIMIT Query Optimization".](#page-7-0)

- <span id="page-88-5"></span>• Multi-Range Read Flags
  - [mrr](#page-88-5) (default on)

Controls the Multi-Range Read strategy.

<span id="page-88-6"></span>• [mrr\\_cost\\_based](#page-88-6) (default on)

Controls use of cost-based MRR if [mrr=on](#page-88-5).

For more information, see Section 8.2.1.10, "Multi-Range Read Optimization".

- <span id="page-88-3"></span>• Semijoin Flags
  - [duplicateweedout](#page-88-3) (default on)

Controls the semijoin Duplicate Weedout strategy.

<span id="page-88-1"></span>• [firstmatch](#page-88-1) (default on)

Controls the semijoin FirstMatch strategy.

<span id="page-88-2"></span>• [loosescan](#page-88-2) (default on)

Controls the semijoin LooseScan strategy (not to be confused with Loose Index Scan for GROUP BY).

<span id="page-89-0"></span>• [semijoin](#page-89-0) (default on)

Controls all semijoin strategies.

The [semijoin](#page-89-0), [firstmatch](#page-88-1), [loosescan](#page-88-2), and [duplicateweedout](#page-88-3) flags enable control over semijoin strategies. The [semijoin](#page-89-0) flag controls whether semijoins are used. If it is set to on, the [firstmatch](#page-88-1) and [loosescan](#page-88-2) flags enable finer control over the permitted semijoin strategies.

If the [duplicateweedout](#page-88-3) semijoin strategy is disabled, it is not used unless all other applicable strategies are also disabled.

If [semijoin](#page-89-0) and [materialization](#page-89-1) are both on, semijoins also use materialization where applicable. These flags are on by default.

For more information, see [Section 8.2.2.1, "Optimizing Subqueries, Derived Tables, and View](#page-13-1) [References with Semijoin Transformations"](#page-13-1).

- <span id="page-89-1"></span>• Subquery Materialization Flags
  - [materialization](#page-89-1) (default on)

Controls materialization (including semijoin materialization).

<span id="page-89-2"></span>• [subquery\\_materialization\\_cost\\_based](#page-89-2) (default on)

Use cost-based materialization choice.

The [materialization](#page-89-1) flag controls whether subquery materialization is used. If [semijoin](#page-89-0) and [materialization](#page-89-1) are both on, semijoins also use materialization where applicable. These flags are on by default.

The [subquery\\_materialization\\_cost\\_based](#page-89-2) flag enables control over the choice between subquery materialization and IN-to-EXISTS subquery transformation. If the flag is on (the default), the optimizer performs a cost-based choice between subquery materialization and IN-to-EXISTS subquery transformation if either method could be used. If the flag is off, the optimizer chooses subquery materialization over IN-to-EXISTS subquery transformation.

For more information, see [Section 8.2.2, "Optimizing Subqueries, Derived Tables, and View](#page-13-0) [References"](#page-13-0).

When you assign a value to optimizer\_switch, flags that are not mentioned keep their current values. This makes it possible to enable or disable specific optimizer behaviors in a single statement without affecting other behaviors. The statement does not depend on what other optimizer flags exist and what their values are. Suppose that all Index Merge optimizations are enabled:

```
mysql> SELECT @@optimizer_switch\G
*************************** 1. row ***************************
@@optimizer_switch: index_merge=on,index_merge_union=on,
 index_merge_sort_union=on,
 index_merge_intersection=on,
 engine_condition_pushdown=on,
 index_condition_pushdown=on,
 mrr=on,mrr_cost_based=on,
 block_nested_loop=on,batched_key_access=off,
 materialization=on,semijoin=on,loosescan=on,
 firstmatch=on,duplicateweedout=on,
 subquery_materialization_cost_based=on,
 use_index_extensions=on,
 condition_fanout_filter=on,derived_merge=on,
 prefer_ordering_index=on
```

If the server is using the Index Merge Union or Index Merge Sort-Union access methods for certain queries and you want to check whether the optimizer performs better without them, set the variable value like this:

```
mysql> SET optimizer_switch='index_merge_union=off,index_merge_sort_union=off';
mysql> SELECT @@optimizer_switch\G
*************************** 1. row ***************************
@@optimizer_switch: index_merge=on,index_merge_union=off,
 index_merge_sort_union=off,
 index_merge_intersection=on,
 engine_condition_pushdown=on,
 index_condition_pushdown=on,
 mrr=on,mrr_cost_based=on,
 block_nested_loop=on,batched_key_access=off,
 materialization=on,semijoin=on,loosescan=on,
 firstmatch=on,duplicateweedout=on,
 subquery_materialization_cost_based=on,
 use_index_extensions=on,
 condition_fanout_filter=on,derived_merge=on,
 prefer_ordering_index=on
```

## <span id="page-90-0"></span>**8.9.3 Optimizer Hints**

One means of control over optimizer strategies is to set the optimizer\_switch system variable (see [Section 8.9.2, "Switchable Optimizations"](#page-86-0)). Changes to this variable affect execution of all subsequent queries; to affect one query differently from another, it is necessary to change optimizer\_switch before each one.

another way to control the optimizer is by using optimizer hints, which can be specified within individual statements. Because optimizer hints apply on a per-statement basis, they provide finer control over statement execution plans than can be achieved using optimizer\_switch. For example, you can enable an optimization for one table in a statement and disable the optimization for a different table. Hints within a statement take precedence over optimizer\_switch flags.

#### Examples:

```
SELECT /*+ NO_RANGE_OPTIMIZATION(t3 PRIMARY, f2_idx) */ f1
 FROM t3 WHERE f1 > 30 AND f1 < 33;
SELECT /*+ BKA(t1) NO_BKA(t2) */ * FROM t1 INNER JOIN t2 WHERE ...;
SELECT /*+ NO_ICP(t1, t2) */ * FROM t1 INNER JOIN t2 WHERE ...;
SELECT /*+ SEMIJOIN(FIRSTMATCH, LOOSESCAN) */ * FROM t1 ...;
EXPLAIN SELECT /*+ NO_ICP(t1) */ * FROM t1 WHERE ...;
```

![](_page_90_Picture_8.jpeg)

## **Note**

The mysql client by default strips comments from SQL statements sent to the server (including optimizer hints) until MySQL 5.7.7, when it was changed to pass optimizer hints to the server. To ensure that optimizer hints are not stripped if you are using an older version of the mysql client with a version of the server that understands optimizer hints, invoke mysql with the - comments option.

Optimizer hints, described here, differ from index hints, described in [Section 8.9.4, "Index Hints"](#page-96-0). Optimizer and index hints may be used separately or together.

- [Optimizer Hint Overview](#page-91-0)
- [Optimizer Hint Syntax](#page-91-1)
- [Table-Level Optimizer Hints](#page-92-0)
- [Index-Level Optimizer Hints](#page-93-0)
- [Subquery Optimizer Hints](#page-94-0)

- [Statement Execution Time Optimizer Hints](#page-95-0)
- [Optimizer Hints for Naming Query Blocks](#page-95-1)

## <span id="page-91-0"></span>**Optimizer Hint Overview**

Optimizer hints apply at different scope levels:

- Global: The hint affects the entire statement
- Query block: The hint affects a particular query block within a statement
- Table-level: The hint affects a particular table within a query block
- Index-level: The hint affects a particular index within a table

The following table summarizes the available optimizer hints, the optimizer strategies they affect, and the scope or scopes at which they apply. More details are given later.

**Table 8.2 Optimizer Hints Available**

| Hint Name             | Description                                                 | Applicable Scopes  |
|-----------------------|-------------------------------------------------------------|--------------------|
| BKA, NO_BKA           | Affects Batched Key Access join<br>processing               | Query block, table |
| BNL, NO_BNL           | Affects Block Nested-Loop join<br>processing                | Query block, table |
| MAX_EXECUTION_TIME    | Limits statement execution time                             | Global             |
| MRR, NO_MRR           | Affects Multi-Range Read<br>optimization                    | Table, index       |
| NO_ICP                | Affects Index Condition<br>Pushdown optimization            | Table, index       |
| NO_RANGE_OPTIMIZATION | Affects range optimization                                  | Table, index       |
| QB_NAME               | Assigns name to query block                                 | Query block        |
| SEMIJOIN, NO_SEMIJOIN | semijoin strategies                                         | Query block        |
| SUBQUERY              | Affects materialization, IN<br>to-EXISTS subquery stratgies | Query block        |

Disabling an optimization prevents the optimizer from using it. Enabling an optimization means the optimizer is free to use the strategy if it applies to statement execution, not that the optimizer necessarily uses it.

## <span id="page-91-1"></span>**Optimizer Hint Syntax**

MySQL supports comments in SQL statements as described in Section 9.6, "Comments". Optimizer hints must be specified within /\*+ ... \*/ comments. That is, optimizer hints use a variant of / \* ... \*/ C-style comment syntax, with a + character following the /\* comment opening sequence. Examples:

```
/*+ BKA(t1) */
/*+ BNL(t1, t2) */
/*+ NO_RANGE_OPTIMIZATION(t4 PRIMARY) */
/*+ QB_NAME(qb2) */
```

Whitespace is permitted after the + character.

The parser recognizes optimizer hint comments after the initial keyword of SELECT, UPDATE, INSERT, REPLACE, and DELETE statements. Hints are permitted in these contexts:

• At the beginning of query and data change statements:

```
SELECT /*+ ... */ ...
INSERT /*+ ... */ ...
REPLACE /*+ ... */ ...
UPDATE /*+ ... */ ...
DELETE /*+ ... */ ...
```

• At the beginning of query blocks:

```
(SELECT /*+ ... */ ... )
(SELECT ... ) UNION (SELECT /*+ ... */ ... )
(SELECT /*+ ... */ ... ) UNION (SELECT /*+ ... */ ... )
UPDATE ... WHERE x IN (SELECT /*+ ... */ ...)
INSERT ... SELECT /*+ ... */ ...
```

• In hintable statements prefaced by EXPLAIN. For example:

```
EXPLAIN SELECT /*+ ... */ ...
EXPLAIN UPDATE ... WHERE x IN (SELECT /*+ ... */ ...)
```

The implication is that you can use EXPLAIN to see how optimizer hints affect execution plans. Use SHOW WARNINGS immediately after EXPLAIN to see how hints are used. The extended EXPLAIN output displayed by a following SHOW WARNINGS indicates which hints were used. Ignored hints are not displayed.

A hint comment may contain multiple hints, but a query block cannot contain multiple hint comments. This is valid:

```
SELECT /*+ BNL(t1) BKA(t2) */ ...
```

But this is invalid:

```
SELECT /*+ BNL(t1) */ /* BKA(t2) */ ...
```

When a hint comment contains multiple hints, the possibility of duplicates and conflicts exists. The following general guidelines apply. For specific hint types, additional rules may apply, as indicated in the hint descriptions.

- Duplicate hints: For a hint such as /\*+ MRR(idx1) MRR(idx1) \*/, MySQL uses the first hint and issues a warning about the duplicate hint.
- Conflicting hints: For a hint such as /\*+ MRR(idx1) NO\_MRR(idx1) \*/, MySQL uses the first hint and issues a warning about the second conflicting hint.

Query block names are identifiers and follow the usual rules about what names are valid and how to quote them (see [Section 9.2, "Schema Object Names"](#page-175-0)).

Hint names, query block names, and strategy names are not case-sensitive. References to table and index names follow the usual identifier case sensitivity rules (see [Section 9.2.3, "Identifier Case](#page-179-0) [Sensitivity"](#page-179-0)).

## <span id="page-92-0"></span>**Table-Level Optimizer Hints**

Table-level hints affect use of the Block Nested-Loop (BNL) and Batched Key Access (BKA) joinprocessing algorithms (see Section 8.2.1.11, "Block Nested-Loop and Batched Key Access Joins"). These hint types apply to specific tables, or all tables in a query block.

Syntax of table-level hints:

```
hint_name([@query_block_name] [tbl_name [, tbl_name] ...])
hint_name([tbl_name@query_block_name [, tbl_name@query_block_name] ...])
```

The syntax refers to these terms:

• hint\_name: These hint names are permitted:

- [BKA](#page-92-0), [NO\\_BKA](#page-92-0): Enable or disable BKA for the specified tables.
- [BNL](#page-92-0), [NO\\_BNL](#page-92-0): Enable or disable BNL for the specified tables.

![](_page_93_Picture_3.jpeg)

#### **Note**

To use a BNL or BKA hint to enable join buffering for any inner table of an outer join, join buffering must be enabled for all inner tables of the outer join.

• tbl\_name: The name of a table used in the statement. The hint applies to all tables that it names. If the hint names no tables, it applies to all tables of the query block in which it occurs.

If a table has an alias, hints must refer to the alias, not the table name.

Table names in hints cannot be qualified with schema names.

• query\_block\_name: The query block to which the hint applies. If the hint includes no leading @query\_block\_name, the hint applies to the query block in which it occurs. For tbl\_name@query\_block\_name syntax, the hint applies to the named table in the named query block. To assign a name to a query block, see [Optimizer Hints for Naming Query Blocks](#page-95-1).

#### Examples:

```
SELECT /*+ NO_BKA(t1, t2) */ t1.* FROM t1 INNER JOIN t2 INNER JOIN t3;
SELECT /*+ NO_BNL() BKA(t1) */ t1.* FROM t1 INNER JOIN t2 INNER JOIN t3;
```

A table-level hint applies to tables that receive records from previous tables, not sender tables. Consider this statement:

```
SELECT /*+ BNL(t2) */ FROM t1, t2;
```

If the optimizer chooses to process t1 first, it applies a Block Nested-Loop join to t2 by buffering the rows from t1 before starting to read from t2. If the optimizer instead chooses to process t2 first, the hint has no effect because t2 is a sender table.

### <span id="page-93-0"></span>**Index-Level Optimizer Hints**

Index-level hints affect which index-processing strategies the optimizer uses for particular tables or indexes. These hint types affect use of Index Condition Pushdown (ICP), Multi-Range Read (MRR), and range optimizations (see Section 8.2.1, "Optimizing SELECT Statements").

Syntax of index-level hints:

```
hint_name([@query_block_name] tbl_name [index_name [, index_name] ...])
hint_name(tbl_name@query_block_name [index_name [, index_name] ...])
```

The syntax refers to these terms:

- hint\_name: These hint names are permitted:
  - [MRR](#page-93-0), [NO\\_MRR](#page-93-0): Enable or disable MRR for the specified table or indexes. MRR hints apply only to InnoDB and MyISAM tables.
  - [NO\\_ICP](#page-93-0): Disable ICP for the specified table or indexes. By default, ICP is a candidate optimization strategy, so there is no hint for enabling it.
  - [NO\\_RANGE\\_OPTIMIZATION](#page-93-0): Disable index range access for the specified table or indexes. This hint also disables Index Merge and Loose Index Scan for the table or indexes. By default, range access is a candidate optimization strategy, so there is no hint for enabling it.

This hint may be useful when the number of ranges may be high and range optimization would require many resources.

- tbl\_name: The table to which the hint applies.
- index\_name: The name of an index in the named table. The hint applies to all indexes that it names. If the hint names no indexes, it applies to all indexes in the table.

To refer to a primary key, use the name PRIMARY. To see the index names for a table, use SHOW INDEX.

• query\_block\_name: The query block to which the hint applies. If the hint includes no leading @query\_block\_name, the hint applies to the query block in which it occurs. For tbl\_name@query\_block\_name syntax, the hint applies to the named table in the named query block. To assign a name to a query block, see [Optimizer Hints for Naming Query Blocks](#page-95-1).

#### Examples:

```
SELECT /*+ MRR(t1) */ * FROM t1 WHERE f2 <= 3 AND 3 <= f3;
SELECT /*+ NO_RANGE_OPTIMIZATION(t3 PRIMARY, f2_idx) */ f1
 FROM t3 WHERE f1 > 30 AND f1 < 33;
INSERT INTO t3(f1, f2, f3)
 (SELECT /*+ NO_ICP(t2) */ t2.f1, t2.f2, t2.f3 FROM t1,t2
 WHERE t1.f1=t2.f1 AND t2.f2 BETWEEN t1.f1
 AND t1.f2 AND t2.f2 + 1 >= t1.f1 + 1);
```

## <span id="page-94-0"></span>**Subquery Optimizer Hints**

Subquery hints affect whether to use semijoin transformations and which semijoin strategies to permit, and, when semijoins are not used, whether to use subquery materialization or IN-to-EXISTS transformations. For more information about these optimizations, see [Section 8.2.2, "Optimizing](#page-13-0) [Subqueries, Derived Tables, and View References"](#page-13-0).

Syntax of hints that affect semijoin strategies:

```
hint_name([@query_block_name] [strategy [, strategy] ...])
```

The syntax refers to these terms:

- hint\_name: These hint names are permitted:
  - [SEMIJOIN](#page-94-0), [NO\\_SEMIJOIN](#page-94-0): Enable or disable the named semijoin strategies.
- strategy: A semijoin strategy to be enabled or disabled. These strategy names are permitted: DUPSWEEDOUT, FIRSTMATCH, LOOSESCAN, MATERIALIZATION.

For [SEMIJOIN](#page-94-0) hints, if no strategies are named, semijoin is used if possible based on the strategies enabled according to the optimizer\_switch system variable. If strategies are named but inapplicable for the statement, DUPSWEEDOUT is used.

For [NO\\_SEMIJOIN](#page-94-0) hints, if no strategies are named, semijoin is not used. If strategies are named that rule out all applicable strategies for the statement, DUPSWEEDOUT is used.

If one subquery is nested within another and both are merged into a semijoin of an outer query, any specification of semijoin strategies for the innermost query are ignored. [SEMIJOIN](#page-94-0) and [NO\\_SEMIJOIN](#page-94-0) hints can still be used to enable or disable semijoin transformations for such nested subqueries.

If DUPSWEEDOUT is disabled, on occasion the optimizer may generate a query plan that is far from optimal. This occurs due to heuristic pruning during greedy search, which can be avoided by setting optimizer\_prune\_level=0.

#### Examples:

```
SELECT /*+ NO_SEMIJOIN(@subq1 FIRSTMATCH, LOOSESCAN) */ * FROM t2
 WHERE t2.a IN (SELECT /*+ QB_NAME(subq1) */ a FROM t3);
SELECT /*+ SEMIJOIN(@subq1 MATERIALIZATION, DUPSWEEDOUT) */ * FROM t2
 WHERE t2.a IN (SELECT /*+ QB_NAME(subq1) */ a FROM t3);
```

Syntax of hints that affect whether to use subquery materialization or IN-to-EXISTS transformations:

```
SUBQUERY([@query_block_name] strategy)
```

The hint name is always [SUBQUERY](#page-94-0).

For [SUBQUERY](#page-94-0) hints, these strategy values are permitted: INTOEXISTS, MATERIALIZATION.

#### Examples:

```
SELECT id, a IN (SELECT /*+ SUBQUERY(MATERIALIZATION) */ a FROM t1) FROM t2;
SELECT * FROM t2 WHERE t2.a IN (SELECT /*+ SUBQUERY(INTOEXISTS) */ a FROM t1);
```

For semijoin and [SUBQUERY](#page-94-0) hints, a leading @query\_block\_name specifies the query block to which the hint applies. If the hint includes no leading @query\_block\_name, the hint applies to the query block in which it occurs. To assign a name to a query block, see [Optimizer Hints for Naming Query](#page-95-1) [Blocks](#page-95-1).

If a hint comment contains multiple subquery hints, the first is used. If there are other following hints of that type, they produce a warning. Following hints of other types are silently ignored.

## <span id="page-95-0"></span>**Statement Execution Time Optimizer Hints**

The [MAX\\_EXECUTION\\_TIME](#page-95-0) hint is permitted only for SELECT statements. It places a limit N (a timeout value in milliseconds) on how long a statement is permitted to execute before the server terminates it:

```
MAX_EXECUTION_TIME(N)
```

Example with a timeout of 1 second (1000 milliseconds):

```
SELECT /*+ MAX_EXECUTION_TIME(1000) */ * FROM t1 INNER JOIN t2 WHERE ...
```

The [MAX\\_EXECUTION\\_TIME\(](#page-95-0)N) hint sets a statement execution timeout of N milliseconds. If this option is absent or N is 0, the statement timeout established by the max\_execution\_time system variable applies.

The [MAX\\_EXECUTION\\_TIME](#page-95-0) hint is applicable as follows:

- For statements with multiple SELECT keywords, such as unions or statements with subqueries, [MAX\\_EXECUTION\\_TIME](#page-95-0) applies to the entire statement and must appear after the first SELECT.
- It applies to read-only SELECT statements. Statements that are not read only are those that invoke a stored function that modifies data as a side effect.
- It does not apply to SELECT statements in stored programs and is ignored.

## <span id="page-95-1"></span>**Optimizer Hints for Naming Query Blocks**

Table-level, index-level, and subquery optimizer hints permit specific query blocks to be named as part of their argument syntax. To create these names, use the [QB\\_NAME](#page-95-1) hint, which assigns a name to the query block in which it occurs:

```
QB_NAME(name)
```

[QB\\_NAME](#page-95-1) hints can be used to make explicit in a clear way which query blocks other hints apply to. They also permit all non-query block name hints to be specified within a single hint comment for easier understanding of complex statements. Consider the following statement:

```
SELECT ...
 FROM (SELECT ...
 FROM (SELECT ... FROM ...)) ...
```

[QB\\_NAME](#page-95-1) hints assign names to query blocks in the statement:

```
SELECT /*+ QB_NAME(qb1) */ ...
```

```
 FROM (SELECT /*+ QB_NAME(qb2) */ ...
 FROM (SELECT /*+ QB_NAME(qb3) */ ... FROM ...)) ...
```

Then other hints can use those names to refer to the appropriate query blocks:

```
SELECT /*+ QB_NAME(qb1) MRR(@qb1 t1) BKA(@qb2) NO_MRR(@qb3t1 idx1, id2) */ ...
 FROM (SELECT /*+ QB_NAME(qb2) */ ...
 FROM (SELECT /*+ QB_NAME(qb3) */ ... FROM ...)) ...
```

The resulting effect is as follows:

- [MRR\(@qb1 t1\)](#page-93-0) applies to table t1 in query block qb1.
- [BKA\(@qb2\)](#page-92-0) applies to query block qb2.
- [NO\\_MRR\(@qb3 t1 idx1, id2\)](#page-93-0) applies to indexes idx1 and idx2 in table t1 in query block qb3.

Query block names are identifiers and follow the usual rules about what names are valid and how to quote them (see [Section 9.2, "Schema Object Names"](#page-175-0)). For example, a query block name that contains spaces must be quoted, which can be done using backticks:

```
SELECT /*+ BKA(@`my hint name`) */ ...
 FROM (SELECT /*+ QB_NAME(`my hint name`) */ ...) ...
```

If the ANSI\_QUOTES SQL mode is enabled, it is also possible to quote query block names within double quotation marks:

```
SELECT /*+ BKA(@"my hint name") */ ...
 FROM (SELECT /*+ QB_NAME("my hint name") */ ...) ...
```

## <span id="page-96-0"></span>**8.9.4 Index Hints**

Index hints give the optimizer information about how to choose indexes during query processing. Index hints, described here, differ from optimizer hints, described in [Section 8.9.3, "Optimizer Hints".](#page-90-0) Index and optimizer hints may be used separately or together.

Index hints apply to SELECT and UPDATE statements. They also work with multi-table DELETE statements, but not with single-table DELETE, as shown later in this section.

Index hints are specified following a table name. (For the general syntax for specifying tables in a SELECT statement, see Section 13.2.9.2, "JOIN Clause".) The syntax for referring to an individual table, including index hints, looks like this:

```
tbl_name [[AS] alias] [index_hint_list]
index_hint_list:
 index_hint [index_hint] ...
index_hint:
 USE {INDEX|KEY}
 [FOR {JOIN|ORDER BY|GROUP BY}] ([index_list])
 | {IGNORE|FORCE} {INDEX|KEY}
 [FOR {JOIN|ORDER BY|GROUP BY}] (index_list)
index_list:
 index_name [, index_name] ...
```

The USE INDEX (index\_list) hint tells MySQL to use only one of the named indexes to find rows in the table. The alternative syntax IGNORE INDEX (index\_list) tells MySQL to not use some particular index or indexes. These hints are useful if EXPLAIN shows that MySQL is using the wrong index from the list of possible indexes.

The FORCE INDEX hint acts like USE INDEX (index\_list), with the addition that a table scan is assumed to be very expensive. In other words, a table scan is used only if there is no way to use one of the named indexes to find rows in the table.

Each hint requires index names, not column names. To refer to a primary key, use the name PRIMARY. To see the index names for a table, use the SHOW INDEX statement or the Information Schema STATISTICS table.

An index\_name value need not be a full index name. It can be an unambiguous prefix of an index name. If a prefix is ambiguous, an error occurs.

### Examples:

```
SELECT * FROM table1 USE INDEX (col1_index,col2_index)
 WHERE col1=1 AND col2=2 AND col3=3;
SELECT * FROM table1 IGNORE INDEX (col3_index)
 WHERE col1=1 AND col2=2 AND col3=3;
```

The syntax for index hints has the following characteristics:

- It is syntactically valid to omit index\_list for USE INDEX, which means "use no indexes." Omitting index\_list for FORCE INDEX or IGNORE INDEX is a syntax error.
- You can specify the scope of an index hint by adding a FOR clause to the hint. This provides more fine-grained control over optimizer selection of an execution plan for various phases of query processing. To affect only the indexes used when MySQL decides how to find rows in the table and how to process joins, use FOR JOIN. To influence index usage for sorting or grouping rows, use FOR ORDER BY or FOR GROUP BY.
- You can specify multiple index hints:

```
SELECT * FROM t1 USE INDEX (i1) IGNORE INDEX FOR ORDER BY (i2) ORDER BY a;
```

It is not an error to name the same index in several hints (even within the same hint):

```
SELECT * FROM t1 USE INDEX (i1) USE INDEX (i1,i1);
```

However, it is an error to mix USE INDEX and FORCE INDEX for the same table:

```
SELECT * FROM t1 USE INDEX FOR JOIN (i1) FORCE INDEX FOR JOIN (i2);
```

If an index hint includes no FOR clause, the scope of the hint is to apply to all parts of the statement. For example, this hint:

```
IGNORE INDEX (i1)
```

is equivalent to this combination of hints:

```
IGNORE INDEX FOR JOIN (i1)
IGNORE INDEX FOR ORDER BY (i1)
IGNORE INDEX FOR GROUP BY (i1)
```

In MySQL 5.0, hint scope with no FOR clause was to apply only to row retrieval. To cause the server to use this older behavior when no FOR clause is present, enable the old system variable at server startup. Take care about enabling this variable in a replication setup. With statement-based binary logging, having different modes for the source and replicas might lead to replication errors.

When index hints are processed, they are collected in a single list by type (USE, FORCE, IGNORE) and by scope (FOR JOIN, FOR ORDER BY, FOR GROUP BY). For example:

```
SELECT * FROM t1
 USE INDEX () IGNORE INDEX (i2) USE INDEX (i1) USE INDEX (i2);
```

is equivalent to:

```
SELECT * FROM t1
 USE INDEX (i1,i2) IGNORE INDEX (i2);
```

The index hints then are applied for each scope in the following order:

- 1. {USE|FORCE} INDEX is applied if present. (If not, the optimizer-determined set of indexes is used.)
- 2. IGNORE INDEX is applied over the result of the previous step. For example, the following two queries are equivalent:

```
SELECT * FROM t1 USE INDEX (i1) IGNORE INDEX (i2) USE INDEX (i2);
SELECT * FROM t1 USE INDEX (i1);
```

For FULLTEXT searches, index hints work as follows:

- For natural language mode searches, index hints are silently ignored. For example, IGNORE INDEX(i1) is ignored with no warning and the index is still used.
- For boolean mode searches, index hints with FOR ORDER BY or FOR GROUP BY are silently ignored. Index hints with FOR JOIN or no FOR modifier are honored. In contrast to how hints apply for non-FULLTEXT searches, the hint is used for all phases of query execution (finding rows and retrieval, grouping, and ordering). This is true even if the hint is given for a non-FULLTEXT index.

For example, the following two queries are equivalent:

```
SELECT * FROM t
 USE INDEX (index1)
 IGNORE INDEX FOR ORDER BY (index1)
 IGNORE INDEX FOR GROUP BY (index1)
 WHERE ... IN BOOLEAN MODE ... ;
SELECT * FROM t
 USE INDEX (index1)
 WHERE ... IN BOOLEAN MODE ... ;
```

Index hints work with DELETE statements, but only if you use multi-table DELETE syntax, as shown here:

```
mysql> EXPLAIN DELETE FROM t1 USE INDEX(col2)
 -> WHERE col1 BETWEEN 1 AND 100 AND COL2 BETWEEN 1 AND 100\G
ERROR 1064 (42000): You have an error in your SQL syntax; check the manual that
corresponds to your MySQL server version for the right syntax to use near 'use
index(col2) where col1 between 1 and 100 and col2 between 1 and 100' at line 1
mysql> EXPLAIN DELETE t1.* FROM t1 USE INDEX(col2)
 -> WHERE col1 BETWEEN 1 AND 100 AND COL2 BETWEEN 1 AND 100\G
*************************** 1. row ***************************
 id: 1
 select_type: DELETE
 table: t1
 partitions: NULL
 type: range
possible_keys: col2
 key: col2
 key_len: 5
 ref: NULL
 rows: 72
 filtered: 11.11
 Extra: Using where
1 row in set, 1 warning (0.00 sec)
```