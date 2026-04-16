# Oracle 21c - About-SQL-Conditions
Source: https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/About-SQL-Conditions.html

If you have installed Oracle Text, then you can create conditions with the built-in operators that are part of that product, including `CONTAINS`, `CATSEARCH`, and `MATCHES`. For more information on these Oracle Text elements, refer to [Oracle Text
Reference](/pls/topic/lookup?ctx=en/database/oracle/oracle-database/21/sqlrf&id=CCREF0103).

The sections that follow describe the various forms of conditions. You must use appropriate condition syntax whenever `condition` appears in SQL statements.

You can use a condition in the `WHERE` clause of these statements:

You can use a condition in any of these clauses of the `SELECT` statement:

* `WHERE`
* `START` `WITH`
* `CONNECT` `BY`
* `HAVING`

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

Oracle Database does not accept all conditions in all parts of all SQL statements. Refer to the section devoted to a particular SQL statement in this book for information on restrictions on the conditions in that statement.