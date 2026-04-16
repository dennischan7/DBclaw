---
source: PostgreSQL 16 Reference
title: 00_Overview
---

*Window functions* provide the ability to perform calculations across sets of rows that are related to the current query row. See Section 3.5 for an introduction to this feature, and Section 4.2.8 for syntax details.

The built-in window functions are listed in [Table 9.64.](#page-0-0) Note that these functions *must* be invoked using window function syntax, i.e., an OVER clause is required.

In addition to these functions, any built-in or user-defined ordinary aggregate (i.e., not ordered-set or hypothetical-set aggregates) can be used as a window function; see Section 9.21 for a list of the builtin aggregates. Aggregate functions act as window functions only when an OVER clause follows the call; otherwise they act as plain aggregates and return a single row for the entire set.

### **Table 9.64. General-Purpose Window Functions**

<span id="page-0-0"></span>

| Function<br>Description                                                                                                                                                                                                                                                                                                                                                                                                                     |  |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--|
| row_number () → bigint<br>Returns the number of the current row within its partition, counting from 1.                                                                                                                                                                                                                                                                                                                                      |  |
| rank () → bigint<br>Returns the rank of the current row, with gaps; that is, the row_number of the first row<br>in its peer group.                                                                                                                                                                                                                                                                                                          |  |
| dense_rank () → bigint<br>Returns the rank of the current row, without gaps; this function effectively counts peer<br>groups.                                                                                                                                                                                                                                                                                                               |  |
| percent_rank () → double precision<br>Returns the relative rank of the current row, that is (rank - 1) / (total partition rows - 1).<br>The value thus ranges from 0 to 1 inclusive.                                                                                                                                                                                                                                                        |  |
| cume_dist () → double precision<br>Returns the cumulative distribution, that is (number of partition rows preceding or peers<br>with current row) / (total partition rows). The value thus ranges from 1/N to 1.                                                                                                                                                                                                                            |  |
| ntile ( num_buckets integer ) → integer<br>Returns an integer ranging from 1 to the argument value, dividing the partition as equally<br>as possible.                                                                                                                                                                                                                                                                                       |  |
| lag ( value anycompatible [, offset integer [, default anycompatible ]] ) →<br>anycompatible<br>Returns value evaluated at the row that is offset rows before the current row within<br>the partition; if there is no such row, instead returns default (which must be of a type<br>compatible with value). Both offset and default are evaluated with respect to the<br>current row. If omitted, offset defaults to 1 and default to NULL. |  |

#### **Description**

lead ( value anycompatible [, offset integer [, default anycompatible ]] )

→ anycompatible

Returns value evaluated at the row that is offset rows after the current row within the partition; if there is no such row, instead returns default (which must be of a type compatible with value). Both offset and default are evaluated with respect to the current row. If omitted, offset defaults to 1 and default to NULL.

first\_value ( value anyelement ) → anyelement

Returns value evaluated at the row that is the first row of the window frame.

last\_value ( value anyelement ) → anyelement

Returns value evaluated at the row that is the last row of the window frame.

nth\_value ( value anyelement, n integer ) → anyelement

Returns value evaluated at the row that is the n'th row of the window frame (counting from 1); returns NULL if there is no such row.

All of the functions listed in [Table 9.64](#page-0-0) depend on the sort ordering specified by the ORDER BY clause of the associated window definition. Rows that are not distinct when considering only the ORDER BY columns are said to be *peers*. The four ranking functions (including cume\_dist) are defined so that they give the same answer for all rows of a peer group.

Note that first\_value, last\_value, and nth\_value consider only the rows within the "window frame", which by default contains the rows from the start of the partition through the last peer of the current row. This is likely to give unhelpful results for last\_value and sometimes also nth\_value. You can redefine the frame by adding a suitable frame specification (RANGE, ROWS or GROUPS) to the OVER clause. See Section 4.2.8 for more information about frame specifications.

When an aggregate function is used as a window function, it aggregates over the rows within the current row's window frame. An aggregate used with ORDER BY and the default window frame definition produces a "running sum" type of behavior, which may or may not be what's wanted. To obtain aggregation over the whole partition, omit ORDER BY or use ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING. Other frame specifications can be used to obtain other effects.

## **Note**

The SQL standard defines a RESPECT NULLS or IGNORE NULLS option for lead, lag, first\_value, last\_value, and nth\_value. This is not implemented in PostgreSQL: the behavior is always the same as the standard's default, namely RESPECT NULLS. Likewise, the standard's FROM FIRST or FROM LAST option for nth\_value is not implemented: only the default FROM FIRST behavior is supported. (You can achieve the result of FROM LAST by reversing the ORDER BY ordering.)

# <span id="page-1-0"></span>**9.23. Subquery Expressions**

This section describes the SQL-compliant subquery expressions available in PostgreSQL. All of the expression forms documented in this section return Boolean (true/false) results.