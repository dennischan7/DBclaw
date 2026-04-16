# Oracle 12c - functions001
Source: https://docs.oracle.com/database/121/SQLRF/functions001.htm

# About SQL Functions

SQL functions are built into Oracle Database and are available for use in various appropriate SQL statements. Do not confuse SQL functions with user-defined functions written in PL/SQL.

If you call a SQL function with an argument of a data type other than the data type expected by the SQL function, then Oracle attempts to convert the argument to the expected data type before performing the SQL function.

Nulls in SQL Functions  Most scalar functions return null when given a null argument. You can use the `NVL` function to return a value when a null occurs. For example, the expression `NVL(commission_pct,0)` returns 0 if `commission_pct` is null or the value of `commission_pct` if it is not null.

For information on how aggregate functions handle nulls, see ["Aggregate Functions"](functions003.md#i89203).

Syntax for SQL Functions In the syntax diagrams for SQL functions, arguments are indicated by their data types. When the parameter `function` appears in SQL syntax, replace it with one of the functions described in this section. Functions are grouped by the data types of their arguments and their return values.

Note:

When you apply SQL functions to LOB columns, Oracle Database creates temporary LOBs during SQL and PL/SQL processing. You should ensure that temporary tablespace quota is sufficient for storing these temporary LOBs for your application.

Note:

The combined values of the

`NLS_COMP`

and

`NLS_SORT`

settings determine the rules by which characters are sorted and compared. If

`NLS_COMP`

is set to

`LINGUISTIC`

for your database, then all entities in this chapter will be interpreted according to the rules specified by the

`NLS_SORT`

parameter. If

`NLS_COMP`

is not set to

`LINGUISTIC`

, then the functions are interpreted without regard to the

`NLS_SORT`

setting.

`NLS_SORT`

can be explicitly set. If it is not set explicitly, it is derived from

`NLS_LANGUAGE`

. Refer to

[Oracle Database Globalization Support Guide](../NLSPG/ch5lingsort.md#NLSPG005)

for more information on these settings.

The syntax showing the categories of functions follows:

function::=

single\_row\_function::=

The sections that follow list the built-in SQL functions in each of the groups illustrated in the preceding diagrams except user-defined functions. All of the built-in SQL functions are then described in alphabetical order.