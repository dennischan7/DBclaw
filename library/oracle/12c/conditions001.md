# Oracle 12c - conditions001
Source: https://docs.oracle.com/database/121/SQLRF/conditions001.htm

# About SQL Conditions

Conditions can have several forms, as shown in the following syntax.

condition::=

If you have installed Oracle Text, then you can create conditions with the built-in operators that are part of that product, including `CONTAINS`, `CATSEARCH`, and `MATCHES`. For more information on these Oracle Text elements, refer to [Oracle Text Reference](../CCREF/csql.md#CCREF0103).

The sections that follow describe the various forms of conditions. You must use appropriate condition syntax whenever `condition` appears in SQL statements.

You can use a condition in the `WHERE` clause of these statements:

You can use a condition in any of these clauses of the `SELECT` statement:

* `WHERE`
* `START` `WITH`
* `CONNECT` `BY`
* `HAVING`

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

A condition could be said to be of a logical data type, although Oracle Database does not formally support such a data type.

The following simple condition always evaluates to `TRUE`:

```
1 = 1
```

The following more complex condition adds the `salary` value to the `commission_pct` value (substituting the value 0 for null) and determines whether the sum is greater than the number constant 25000:

```
NVL(salary, 0) + NVL(salary + (salary*commission_pct, 0) > 25000)
```

Logical conditions can combine multiple conditions into a single condition. For example, you can use the `AND` condition to combine two conditions:

```
(1 = 1) AND (5 < 7)
```

Here are some valid conditions:

```
name = 'SMITH' 
employees.department_id = departments.department_id 
hire_date > '01-JAN-08' 
job_id IN ('SA_MAN', 'SA_REP') 
salary BETWEEN 5000 AND 10000
commission_pct IS NULL AND salary = 2100
```

See Also:

The description of each statement in

[Chapter 10](statements_1.md#g2257928)

through

[Chapter 19](statements_10.md#g2232147)

for the restrictions on the conditions in that statement

## Condition Precedence

Precedence is the order in which Oracle Database evaluates different conditions in the same expression. When evaluating an expression containing multiple conditions, Oracle evaluates conditions with higher precedence before evaluating those with lower precedence. Oracle evaluates conditions with equal precedence from left to right within an expression, with the following exceptions:

[Table 6-1](#BABBCFGD) lists the levels of precedence among SQL condition from high to low. Conditions listed on the same line have the same precedence. As the table indicates, Oracle evaluates operators before conditions.

Table 6-1 SQL Condition Precedence

| Type of Condition | Purpose |
| --- | --- |
| SQL operators are evaluated before SQL conditions | See ["Operator Precedence"](operators001.md#i1028541) |
| `=, !=, <, >, <=, >=,` | comparison |
| `IS [NOT] NULL, LIKE, [NOT] BETWEEN, [NOT] IN, EXISTS, IS OF` `type` | comparison |
| `NOT` | exponentiation, logical negation |
| `AND` | conjunction |
| `OR` | disjunction |