# Oracle 11g - queries008
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/queries008.htm

# Unnesting of Nested Subqueries

Subqueries are nested when they appear in the `WHERE` clause of the parent statement. When Oracle Database evaluates a statement with a nested subquery, it must evaluate the subquery portion multiple times and may overlook some efficient access paths or joins.

Subquery unnesting unnests and merges the body of the subquery into the body of the statement that contains it, allowing the optimizer to consider them together when evaluating access paths and joins. The optimizer can unnest most subqueries, with some exceptions. Those exceptions include hierarchical subqueries and subqueries that contain a `ROWNUM` pseudocolumn, one of the set operators, a nested aggregate function, or a correlated reference to a query block that is not the immediate outer query block of the subquery.

Assuming no restrictions exist, the optimizer automatically unnests some (but not all) of the following nested subqueries:

* Uncorrelated `IN` subqueries
* `IN` and `EXISTS` correlated subqueries, as long as they do not contain aggregate functions or a `GROUP` `BY` clause

You can enable extended subquery unnesting by instructing the optimizer to unnest additional types of subqueries: