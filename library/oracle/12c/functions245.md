# Oracle 12c - functions245
Source: https://docs.oracle.com/database/121/SQLRF/functions245.htm

[Go to main content](#BEGIN)

318/555 

# VALUE

Syntax

Purpose

`VALUE` takes as its argument a correlation variable (table alias) associated with a row of an object table and returns object instances stored in the object table. The type of the object instances is the same type as the object table.

Examples

The following example uses the sample table `oe.persons`, which is created in ["Substitutable Table and Column Examples"](statements_7002.md#i2090577):

```
SELECT VALUE(p) FROM persons p;

VALUE(P)(NAME, SSN)
-------------------------------------------------------------
PERSON_T('Bob', 1234)
EMPLOYEE_T('Joe', 32456, 12, 100000)
PART_TIME_EMP_T('Tim', 5678, 13, 1000, 20)
```

Scripting on this page enhances content navigation, but does not change the content in any way.