# Oracle 23c - Column-Expressions
Source: https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/Column-Expressions.html

A column expression, which is designated as `column_expression` in subsequent syntax diagrams, is a limited form of `expr`. A column expression can be a simple expression, compound expression, function expression, boolean expression, or expression list, but it can contain only the following forms of expression:

* Columns of the subject table â the table being created, altered, or indexed
* Constants (strings or numbers)
* Deterministic functions â either SQL built-in functions or user-defined functions

No other expression forms described in this chapter are valid. In addition, compound expressions using the `PRIOR` keyword are not supported, nor are aggregate functions.

You can use a column expression for these purposes:

* To create a function-based index.
* To explicitly or implicitly define a virtual column. When you define a virtual column, the defining `column_expression` must refer only to columns of the subject table that have already been defined, in the current statement or in a prior statement.

  You cannot specify a call to a PL/SQL function in the defining expression for a virtual column that you want to use as a partitioning column.
* You can use `column_expression` directly as a partitioning key.

The combined components of a column expression must be deterministic. That is, the same set of input values must return the same set of output values.