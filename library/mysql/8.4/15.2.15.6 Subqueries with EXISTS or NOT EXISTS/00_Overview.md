---
source: MySQL 8.4 Reference
title: 00_Overview
---

If a subquery returns any rows at all, EXISTS subquery is TRUE, and NOT EXISTS subquery is FALSE. For example:

```
SELECT column1 FROM t1 WHERE EXISTS (SELECT * FROM t2);
```

Traditionally, an EXISTS subquery starts with SELECT \*, but it could begin with SELECT 5 or SELECT column1 or anything at all. MySQL ignores the [SELECT](#page-70-0) list in such a subquery, so it makes no difference.

For the preceding example, if t2 contains any rows, even rows with nothing but NULL values, the EXISTS condition is TRUE. This is actually an unlikely example because a [NOT] EXISTS subquery almost always contains correlations. Here are some more realistic examples:

• What kind of store is present in one or more cities?

```
SELECT DISTINCT store_type FROM stores
 WHERE EXISTS (SELECT * FROM cities_stores
 WHERE cities_stores.store_type = stores.store_type);
```

• What kind of store is present in no cities?

```
SELECT DISTINCT store_type FROM stores
 WHERE NOT EXISTS (SELECT * FROM cities_stores
 WHERE cities_stores.store_type = stores.store_type);
```

• What kind of store is present in all cities?

```
SELECT DISTINCT store_type FROM stores
 WHERE NOT EXISTS (
 SELECT * FROM cities WHERE NOT EXISTS (
 SELECT * FROM cities_stores
 WHERE cities_stores.city = cities.city
 AND cities_stores.store_type = stores.store_type));
```

The last example is a double-nested NOT EXISTS query. That is, it has a NOT EXISTS clause within a NOT EXISTS clause. Formally, it answers the question "does a city exist with a store that is not in Stores"? But it is easier to say that a nested NOT EXISTS answers the question "is x TRUE for all y?"

You can also use NOT EXISTS or NOT EXISTS with [TABLE](#page-105-0) in the subquery, like this:

```
SELECT column1 FROM t1 WHERE EXISTS (TABLE t2);
```

The results are the same as when using SELECT \* with no WHERE clause in the subquery.

# <span id="page-96-0"></span>**15.2.15.7 Correlated Subqueries**

A correlated subquery is a subquery that contains a reference to a table that also appears in the outer query. For example:

```
SELECT * FROM t1
 WHERE column1 = ANY (SELECT column1 FROM t2
 WHERE t2.column2 = t1.column2);
```

Notice that the subquery contains a reference to a column of t1, even though the subquery's FROM clause does not mention a table t1. So, MySQL looks outside the subquery, and finds t1 in the outer query.

Suppose that table t1 contains a row where column1 = 5 and column2 = 6; meanwhile, table t2 contains a row where column1 = 5 and column2 = 7. The simple expression ... WHERE column1 = ANY (SELECT column1 FROM t2) would be TRUE, but in this example, the WHERE clause within the subquery is FALSE (because (5,6) is not equal to (5,7)), so the expression as a whole is FALSE.

**Scoping rule:** MySQL evaluates from inside to outside. For example:

```
SELECT column1 FROM t1 AS x
 WHERE x.column1 = (SELECT column1 FROM t2 AS x
 WHERE x.column1 = (SELECT column1 FROM t3
 WHERE x.column2 = t3.column1));
```

In this statement, x.column2 must be a column in table t2 because SELECT column1 FROM t2 AS x ... renames t2. It is not a column in table t1 because SELECT column1 FROM t1 ... is an outer query that is farther out.

The optimizer can transform a correlated scalar subquery to a derived table when the subquery\_to\_derived flag of the optimizer\_switch variable is enabled. Consider the query shown here:

```
SELECT * FROM t1 
 WHERE ( SELECT a FROM t2 
 WHERE t2.a=t1.a ) > 0;
```

To avoid materializing several times for a given derived table, we can instead materialize—once —a derived table which adds a grouping on the join column from the table referenced in the inner query (t2.a) and then an outer join on the lifted predicate (t1.a = derived.a) in order to select the correct group to match up with the outer row. (If the subquery already has an explicit grouping, the extra grouping is added to the end of the grouping list.) The query previously shown can thus be rewritten like this:

```
SELECT t1.* FROM t1 
 LEFT OUTER JOIN
 (SELECT a, COUNT(*) AS ct FROM t2 GROUP BY a) AS derived
 ON t1.a = derived.a 
 AND 
 REJECT_IF(
 (ct > 1),
 "ERROR 1242 (21000): Subquery returns more than 1 row"
 )
 WHERE derived.a > 0;
```

In the rewritten query, REJECT\_IF() represents an internal function which tests a given condition (here, the comparison ct > 1) and raises a given error (in this case, [ER\\_SUBQUERY\\_NO\\_1\\_ROW](https://dev.mysql.com/doc/mysql-errors/8.4/en/server-error-reference.md#error_er_subquery_no_1_row)) if the condition is true. This reflects the cardinality check that the optimizer performs as part of evaluating the JOIN or WHERE clause, prior to evaluating any lifted predicate, which is done only if the subquery does not return more than one row.

This type of transformation can be performed, provided the following conditions are met:

- The subquery can be part of a [SELECT](#page-70-0) list, WHERE condition, or HAVING condition, but cannot be part of a [JOIN](#page-79-0) condition, and cannot contain a LIMIT or OFFSET clause. In addition, the subquery cannot contain any set operations such as [UNION](#page-111-0).
- The WHERE clause may contain one or more predicates, combined with AND. If the WHERE clause contains an OR clause, it cannot be transformed. At least one of the WHERE clause predicates must be eligible for transformation, and none of them may reject transformation.
- To be eligible for transformation, a WHERE clause predicate must be an equality predicate; other comparison predicates are not eligible for transformation. The predicate must employ the equality operator = for making the comparison; the null-safe <=> operator is not supported in this context.

In MySQL 8.4.0 and later, operands of the predicate can be column values, constants, or expressions including these, including deterministic functions called with column values as arguments.

- A WHERE clause predicate that contains only inner references is not eligible for transformation, since it can be evaluated before the grouping. A WHERE clause predicate that contains only outer references is eligible for transformation, even though it can be lifted up to the outer query block. This is made possible by adding a cardinality check without grouping in the derived table.
- To be eligible, a WHERE clause predicate must have one operand that contains only inner references and one operand that contains only outer references. If the predicate is not eligible due to this rule, transformation of the query is rejected.
- A correlated column can be present only in the subquery's WHERE clause (and not in the SELECT list, a JOIN or ORDER BY clause, a GROUP BY list, or a HAVING clause). Nor can there be any correlated column inside a derived table in the subquery's FROM list.
- A correlated column can not be contained in an aggregate function's list of arguments.
- A correlated column must be resolved in the query block directly containing the subquery being considered for transformation.
- A correlated column cannot be present in a nested scalar subquery in the WHERE clause.
- The subquery cannot contain any window functions, and must not contain any aggregate function which aggregates in a query block outer to the subquery. A COUNT() aggregate function, if contained in the SELECT list element of the subquery, must be at the topmost level, and cannot be part of an expression.

See also [Section 15.2.15.8, "Derived Tables".](#page-97-0)

## <span id="page-97-0"></span>**15.2.15.8 Derived Tables**

This section discusses general characteristics of derived tables. For information about lateral derived tables preceded by the LATERAL keyword, see [Section 15.2.15.9, "Lateral Derived Tables"](#page-100-0).

A derived table is an expression that generates a table within the scope of a query FROM clause. For example, a subquery in a [SELECT](#page-70-0) statement FROM clause is a derived table:

```
SELECT ... FROM (subquery) [AS] tbl_name ...
```

The JSON\_TABLE() function generates a table and provides another way to create a derived table:

```
SELECT * FROM JSON_TABLE(arg_list) [AS] tbl_name ...
```

The [AS] tbl\_name clause is mandatory because every table in a FROM clause must have a name. Any columns in the derived table must have unique names. Alternatively, tbl\_name may be followed by a parenthesized list of names for the derived table columns:

```
SELECT ... FROM (subquery) [AS] tbl_name (col_list) ...
```

The number of column names must be the same as the number of table columns.

For the sake of illustration, assume that you have this table:

```
CREATE TABLE t1 (s1 INT, s2 CHAR(5), s3 FLOAT);
```

Here is how to use a subquery in the FROM clause, using the example table:

```
INSERT INTO t1 VALUES (1,'1',1.0);
INSERT INTO t1 VALUES (2,'2',2.0);
SELECT sb1,sb2,sb3
 FROM (SELECT s1 AS sb1, s2 AS sb2, s3*2 AS sb3 FROM t1) AS sb
 WHERE sb1 > 1;
```

#### Result:

```
+------+------+------+
| sb1 | sb2 | sb3 |
+------+------+------+
| 2 | 2 | 4 |
+------+------+------+
```

Here is another example: Suppose that you want to know the average of a set of sums for a grouped table. This does not work:

```
SELECT AVG(SUM(column1)) FROM t1 GROUP BY column1;
```

However, this query provides the desired information:

```
SELECT AVG(sum_column1)
 FROM (SELECT SUM(column1) AS sum_column1
 FROM t1 GROUP BY column1) AS t1;
```

Notice that the column name used within the subquery (sum\_column1) is recognized in the outer query.

The column names for a derived table come from its select list:

```
mysql> SELECT * FROM (SELECT 1, 2, 3, 4) AS dt;
+---+---+---+---+
| 1 | 2 | 3 | 4 |
+---+---+---+---+
| 1 | 2 | 3 | 4 |
+---+---+---+---+
```

To provide column names explicitly, follow the derived table name with a parenthesized list of column names:

```
mysql> SELECT * FROM (SELECT 1, 2, 3, 4) AS dt (a, b, c, d);
+---+---+---+---+
| a | b | c | d |
+---+---+---+---+
| 1 | 2 | 3 | 4 |
+---+---+---+---+
```

A derived table can return a scalar, column, row, or table.

Derived tables are subject to these restrictions:

• A derived table cannot contain references to other tables of the same [SELECT](#page-70-0) (use a LATERAL derived table for that; see [Section 15.2.15.9, "Lateral Derived Tables"](#page-100-0)).

The optimizer determines information about derived tables in such a way that EXPLAIN does not need to materialize them. See Section 10.2.2.4, "Optimizing Derived Tables, View References, and Common Table Expressions with Merging or Materialization".

It is possible under certain circumstances that using EXPLAIN SELECT modifies table data. This can occur if the outer query accesses any tables and an inner query invokes a stored function that changes one or more rows of a table. Suppose that there are two tables t1 and t2 in database d1, and a stored function f1 that modifies t2, created as shown here:

```
CREATE DATABASE d1;
USE d1;
CREATE TABLE t1 (c1 INT);
CREATE TABLE t2 (c1 INT);
CREATE FUNCTION f1(p1 INT) RETURNS INT
 BEGIN
 INSERT INTO t2 VALUES (p1);
 RETURN p1;
 END;
```

Referencing the function directly in an EXPLAIN SELECT has no effect on t2, as shown here:

```
mysql> SELECT * FROM t2;
Empty set (0.02 sec)
mysql> EXPLAIN SELECT f1(5)\G
*************************** 1. row ***************************
 id: 1
 select_type: SIMPLE
 table: NULL
 partitions: NULL
 type: NULL
possible_keys: NULL
 key: NULL
 key_len: NULL
 ref: NULL
 rows: NULL
 filtered: NULL
 Extra: No tables used
1 row in set (0.01 sec)
mysql> SELECT * FROM t2;
Empty set (0.01 sec)
```

This is because the [SELECT](#page-70-0) statement did not reference any tables, as can be seen in the table and Extra columns of the output. This is also true of the following nested [SELECT](#page-70-0):

```
mysql> EXPLAIN SELECT NOW() AS a1, (SELECT f1(5)) AS a2\G
*************************** 1. row ***************************
 id: 1
 select_type: PRIMARY
 table: NULL
 type: NULL
possible_keys: NULL
 key: NULL
 key_len: NULL
 ref: NULL
 rows: NULL
 filtered: NULL
 Extra: No tables used
1 row in set, 1 warning (0.00 sec)
mysql> SHOW WARNINGS;
+-------+------+------------------------------------------+
| Level | Code | Message |
+-------+------+------------------------------------------+
| Note | 1249 | Select 2 was reduced during optimization |
+-------+------+------------------------------------------+
1 row in set (0.00 sec)
mysql> SELECT * FROM t2;
Empty set (0.00 sec)
```

However, if the outer [SELECT](#page-70-0) references any tables, the optimizer executes the statement in the subquery as well, with the result that t2 is modified:

```
mysql> EXPLAIN SELECT * FROM t1 AS a1, (SELECT f1(5)) AS a2\G
*************************** 1. row ***************************
 id: 1
 select_type: PRIMARY
 table: <derived2>
 partitions: NULL
 type: system
possible_keys: NULL
 key: NULL
 key_len: NULL
 ref: NULL
 rows: 1
 filtered: 100.00
 Extra: NULL
*************************** 2. row ***************************
 id: 1
 select_type: PRIMARY
 table: a1
 partitions: NULL
 type: ALL
possible_keys: NULL
 key: NULL
 key_len: NULL
 ref: NULL
 rows: 1
 filtered: 100.00
 Extra: NULL
*************************** 3. row ***************************
 id: 2
 select_type: DERIVED
 table: NULL
 partitions: NULL
 type: NULL
possible_keys: NULL
 key: NULL
 key_len: NULL
 ref: NULL
 rows: NULL
 filtered: NULL
 Extra: No tables used
3 rows in set (0.00 sec)
mysql> SELECT * FROM t2;
+------+
| c1 |
+------+
| 5 |
+------+
1 row in set (0.00 sec)
```

The derived table optimization can also be employed with many correlated (scalar) subqueries. For more information and examples, see [Section 15.2.15.7, "Correlated Subqueries".](#page-96-0)

## <span id="page-100-0"></span>**15.2.15.9 Lateral Derived Tables**

A derived table cannot normally refer to (depend on) columns of preceding tables in the same FROM clause. A derived table may be defined as a lateral derived table to specify that such references are permitted.

Nonlateral derived tables are specified using the syntax discussed in [Section 15.2.15.8, "Derived](#page-97-0) [Tables"](#page-97-0). The syntax for a lateral derived table is the same as for a nonlateral derived table except that the keyword LATERAL is specified before the derived table specification. The LATERAL keyword must precede each table to be used as a lateral derived table.

Lateral derived tables are subject to these restrictions:

• A lateral derived table can occur only in a FROM clause, either in a list of tables separated with commas or in a join specification (JOIN, INNER JOIN, CROSS JOIN, LEFT [OUTER] JOIN, or RIGHT [OUTER] JOIN).

• If a lateral derived table is in the right operand of a join clause and contains a reference to the left operand, the join operation must be an INNER JOIN, CROSS JOIN, or LEFT [OUTER] JOIN.

If the table is in the left operand and contains a reference to the right operand, the join operation must be an INNER JOIN, CROSS JOIN, or RIGHT [OUTER] JOIN.

- If a lateral derived table references an aggregate function, the function's aggregation query cannot be the one that owns the FROM clause in which the lateral derived table occurs.
- In accordance with the SQL standard, MySQL always treats a join with a table function such as JSON\_TABLE() as though LATERAL had been used. Since the LATERAL keyword is implicit, it is not allowed before JSON\_TABLE(); this is also according to the SQL standard.

The following discussion shows how lateral derived tables make possible certain SQL operations that cannot be done with nonlateral derived tables or that require less-efficient workarounds.

Suppose that we want to solve this problem: Given a table of people in a sales force (where each row describes a member of the sales force), and a table of all sales (where each row describes a sale: salesperson, customer, amount, date), determine the size and customer of the largest sale for each salesperson. This problem can be approached two ways.

First approach to solving the problem: For each salesperson, calculate the maximum sale size, and also find the customer who provided this maximum. In MySQL, that can be done like this:

```
SELECT
 salesperson.name,
 -- find maximum sale size for this salesperson
 (SELECT MAX(amount) AS amount
 FROM all_sales
 WHERE all_sales.salesperson_id = salesperson.id)
 AS amount,
 -- find customer for this maximum size
 (SELECT customer_name
 FROM all_sales
 WHERE all_sales.salesperson_id = salesperson.id
 AND all_sales.amount =
 -- find maximum size, again
 (SELECT MAX(amount) AS amount
 FROM all_sales
 WHERE all_sales.salesperson_id = salesperson.id))
 AS customer_name
FROM
 salesperson;
```

That query is inefficient because it calculates the maximum size twice per salesperson (once in the first subquery and once in the second).

We can try to achieve an efficiency gain by calculating the maximum once per salesperson and "caching" it in a derived table, as shown by this modified query:

```
SELECT
 salesperson.name,
 max_sale.amount,
 max_sale_customer.customer_name
FROM
 salesperson,
 -- calculate maximum size, cache it in transient derived table max_sale
 (SELECT MAX(amount) AS amount
 FROM all_sales
 WHERE all_sales.salesperson_id = salesperson.id)
 AS max_sale,
 -- find customer, reusing cached maximum size
 (SELECT customer_name
 FROM all_sales
 WHERE all_sales.salesperson_id = salesperson.id
 AND all_sales.amount =
 -- the cached maximum size
```

```
 max_sale.amount)
 AS max_sale_customer;
```

However, the query is illegal in SQL-92 because derived tables cannot depend on other tables in the same FROM clause. Derived tables must be constant over the query's duration, not contain references to columns of other FROM clause tables. As written, the query produces this error:

```
ERROR 1054 (42S22): Unknown column 'salesperson.id' in 'where clause'
```

In SQL:1999, the query becomes legal if the derived tables are preceded by the LATERAL keyword (which means "this derived table depends on previous tables on its left side"):

```
SELECT
 salesperson.name,
 max_sale.amount,
 max_sale_customer.customer_name
FROM
 salesperson,
 -- calculate maximum size, cache it in transient derived table max_sale
 LATERAL
 (SELECT MAX(amount) AS amount
 FROM all_sales
 WHERE all_sales.salesperson_id = salesperson.id)
 AS max_sale,
 -- find customer, reusing cached maximum size
 LATERAL
 (SELECT customer_name
 FROM all_sales
 WHERE all_sales.salesperson_id = salesperson.id
 AND all_sales.amount =
 -- the cached maximum size
 max_sale.amount)
 AS max_sale_customer;
```

A lateral derived table need not be constant and is brought up to date each time a new row from a preceding table on which it depends is processed by the top query.

Second approach to solving the problem: A different solution could be used if a subquery in the [SELECT](#page-70-0) list could return multiple columns:

```
SELECT
 salesperson.name,
 -- find maximum size and customer at same time
 (SELECT amount, customer_name
 FROM all_sales
 WHERE all_sales.salesperson_id = salesperson.id
 ORDER BY amount DESC LIMIT 1)
FROM
 salesperson;
```

That is efficient but illegal. It does not work because such subqueries can return only a single column:

```
ERROR 1241 (21000): Operand should contain 1 column(s)
```

One attempt at rewriting the query is to select multiple columns from a derived table:

```
SELECT
 salesperson.name,
 max_sale.amount,
 max_sale.customer_name
FROM
 salesperson,
 -- find maximum size and customer at same time
 (SELECT amount, customer_name
 FROM all_sales
 WHERE all_sales.salesperson_id = salesperson.id
 ORDER BY amount DESC LIMIT 1)
 AS max_sale;
```

However, that also does not work. The derived table is dependent on the salesperson table and thus fails without LATERAL:

```
ERROR 1054 (42S22): Unknown column 'salesperson.id' in 'where clause'
```

Adding the LATERAL keyword makes the query legal:

```
SELECT
 salesperson.name,
 max_sale.amount,
 max_sale.customer_name
FROM
 salesperson,
 -- find maximum size and customer at same time
 LATERAL
 (SELECT amount, customer_name
 FROM all_sales
 WHERE all_sales.salesperson_id = salesperson.id
 ORDER BY amount DESC LIMIT 1)
 AS max_sale;
```

In short, LATERAL is the efficient solution to all drawbacks in the two approaches just discussed.

# <span id="page-103-0"></span>**15.2.15.10 Subquery Errors**

There are some errors that apply only to subqueries. This section describes them.

• Unsupported subquery syntax:

```
ERROR 1235 (ER_NOT_SUPPORTED_YET)
SQLSTATE = 42000
Message = "This version of MySQL doesn't yet support
'LIMIT & IN/ALL/ANY/SOME subquery'"
```

This means that MySQL does not support statements like the following:

```
SELECT * FROM t1 WHERE s1 IN (SELECT s2 FROM t2 ORDER BY s1 LIMIT 1)
```

• Incorrect number of columns from subquery:

```
ERROR 1241 (ER_OPERAND_COL)
SQLSTATE = 21000
Message = "Operand should contain 1 column(s)"
```

This error occurs in cases like this:

```
SELECT (SELECT column1, column2 FROM t2) FROM t1;
```

You may use a subquery that returns multiple columns, if the purpose is row comparison. In other contexts, the subquery must be a scalar operand. See [Section 15.2.15.5, "Row Subqueries".](#page-94-0)

• Incorrect number of rows from subquery:

```
ERROR 1242 (ER_SUBSELECT_NO_1_ROW)
SQLSTATE = 21000
Message = "Subquery returns more than 1 row"
```

This error occurs for statements where the subquery must return at most one row but returns multiple rows. Consider the following example:

```
SELECT * FROM t1 WHERE column1 = (SELECT column1 FROM t2);
```

If SELECT column1 FROM t2 returns just one row, the previous query works. If the subquery returns more than one row, error 1242 occurs. In that case, the query should be rewritten as:

```
SELECT * FROM t1 WHERE column1 = ANY (SELECT column1 FROM t2);
```

• Incorrectly used table in subquery:

```
Error 1093 (ER_UPDATE_TABLE_USED)
SQLSTATE = HY000
Message = "You can't specify target table 'x'
for update in FROM clause"
```

This error occurs in cases such as the following, which attempts to modify a table and select from the same table in the subquery:

```
UPDATE t1 SET column2 = (SELECT MAX(column1) FROM t1);
```

You can use a common table expression or derived table to work around this. See [Section 15.2.15.12, "Restrictions on Subqueries"](#page-104-0).

All of the errors described in this section also apply when using [TABLE](#page-105-0) in subqueries.

For transactional storage engines, the failure of a subquery causes the entire statement to fail. For nontransactional storage engines, data modifications made before the error was encountered are preserved.