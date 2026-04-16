---
source: MySQL 5.7 Reference
title: 00_Overview
---

Development is ongoing, so no optimization tip is reliable for the long term. The following list provides some interesting tricks that you might want to play with. See also Section 8.2.2, "Optimizing Subqueries, Derived Tables, and View References".

• Use subquery clauses that affect the number or order of the rows in the subquery. For example:

```
SELECT * FROM t1 WHERE t1.column1 IN
 (SELECT column1 FROM t2 ORDER BY column1);
SELECT * FROM t1 WHERE t1.column1 IN
 (SELECT DISTINCT column1 FROM t2);
SELECT * FROM t1 WHERE EXISTS
 (SELECT * FROM t2 LIMIT 1);
```

• Replace a join with a subquery. For example, try this:

```
SELECT DISTINCT column1 FROM t1 WHERE t1.column1 IN (
 SELECT column1 FROM t2);
```

#### Instead of this:

```
SELECT DISTINCT t1.column1 FROM t1, t2
 WHERE t1.column1 = t2.column1;
```

- Some subqueries can be transformed to joins for compatibility with older versions of MySQL that do not support subqueries. However, in some cases, converting a subquery to a join may improve performance. See [Section 13.2.10.11, "Rewriting Subqueries as Joins"](#page-6-0).
- Move clauses from outside to inside the subquery. For example, use this query:

```
SELECT * FROM t1
 WHERE s1 IN (SELECT s1 FROM t1 UNION ALL SELECT s1 FROM t2);
```

#### Instead of this query:

```
SELECT * FROM t1
 WHERE s1 IN (SELECT s1 FROM t1) OR s1 IN (SELECT s1 FROM t2);
```

For another example, use this query:

```
SELECT (SELECT column1 + 5 FROM t1) FROM t2;
```

### Instead of this query:

```
SELECT (SELECT column1 FROM t1) + 5 FROM t2;
```

• Use a row subquery instead of a correlated subquery. For example, use this query:

```
SELECT * FROM t1
 WHERE (column1,column2) IN (SELECT column1,column2 FROM t2);
```

### Instead of this query:

```
SELECT * FROM t1
```

```
 WHERE EXISTS (SELECT * FROM t2 WHERE t2.column1=t1.column1
 AND t2.column2=t1.column2);
```

- Use NOT (a = ANY (...)) rather than a <> ALL (...).
- Use x = ANY (table containing (1,2)) rather than x=1 OR x=2.
- Use = ANY rather than EXISTS.
- For uncorrelated subqueries that always return one row, IN is always slower than =. For example, use this query:

```
SELECT * FROM t1
 WHERE t1.col_name = (SELECT a FROM t2 WHERE b = some_const);
```

Instead of this query:

```
SELECT * FROM t1
 WHERE t1.col_name IN (SELECT a FROM t2 WHERE b = some_const);
```

These tricks might cause programs to go faster or slower. Using MySQL facilities like the BENCHMARK() function, you can get an idea about what helps in your own situation. See Section 12.15, "Information Functions".

Some optimizations that MySQL itself makes are:

- MySQL executes uncorrelated subqueries only once. Use [EXPLAIN](#page-195-0) to make sure that a given subquery really is uncorrelated.
- MySQL rewrites IN, ALL, ANY, and SOME subqueries in an attempt to take advantage of the possibility that the select-list columns in the subquery are indexed.
- MySQL replaces subqueries of the following form with an index-lookup function, which [EXPLAIN](#page-195-0) describes as a special join type (unique\_subquery or index\_subquery):

```
... IN (SELECT indexed_column FROM single_table ...)
```

• MySQL enhances expressions of the following form with an expression involving MIN() or MAX(), unless NULL values or empty sets are involved:

```
value {ALL|ANY|SOME} {> | < | >= | <=} (uncorrelated subquery)
```

For example, this WHERE clause:

```
WHERE 5 > ALL (SELECT x FROM t)
```

might be treated by the optimizer like this:

```
WHERE 5 > (SELECT MAX(x) FROM t)
```

See also [MySQL Internals: How MySQL Transforms Subqueries.](https://dev.mysql.com/doc/internals/en/transformations.md)

## <span id="page-6-0"></span>**13.2.10.11 Rewriting Subqueries as Joins**

Sometimes there are other ways to test membership in a set of values than by using a subquery. Also, on some occasions, it is not only possible to rewrite a query without a subquery, but it can be more efficient to make use of some of these techniques rather than to use subqueries. One of these is the IN() construct:

For example, this query:

```
SELECT * FROM t1 WHERE id IN (SELECT id FROM t2);
```

Can be rewritten as:

```
SELECT DISTINCT t1.* FROM t1, t2 WHERE t1.id=t2.id;
```

### The queries:

```
SELECT * FROM t1 WHERE id NOT IN (SELECT id FROM t2);
SELECT * FROM t1 WHERE NOT EXISTS (SELECT id FROM t2 WHERE t1.id=t2.id);
```

#### Can be rewritten as:

```
SELECT table1.*
 FROM table1 LEFT JOIN table2 ON table1.id=table2.id
 WHERE table2.id IS NULL;
```

A LEFT [OUTER] JOIN can be faster than an equivalent subquery because the server might be able to optimize it better—a fact that is not specific to MySQL Server alone. Prior to SQL-92, outer joins did not exist, so subqueries were the only way to do certain things. Today, MySQL Server and many other modern database systems offer a wide range of outer join types.

MySQL Server supports multiple-table DELETE statements that can be used to efficiently delete rows based on information from one table or even from many tables at the same time. Multiple-table [UPDATE](#page-8-0) statements are also supported. See Section 13.2.2, "DELETE Statement", and [Section 13.2.11,](#page-8-0) ["UPDATE Statement".](#page-8-0)