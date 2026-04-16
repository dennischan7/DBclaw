---
source: MySQL 5.7 Reference
title: 00_Overview
---

**Table 12.6 Assignment Operators**

| Name | Description                                                                                         |  |
|------|-----------------------------------------------------------------------------------------------------|--|
| :=   | Assign a value                                                                                      |  |
| =    | Assign a value (as part of a SET statement, or as<br>part of the SET clause in an UPDATE statement) |  |

<span id="page-0-2"></span>• [:=](#page-0-2)

Assignment operator. Causes the user variable on the left hand side of the operator to take on the value to its right. The value on the right hand side may be a literal value, another variable storing a value, or any legal expression that yields a scalar value, including the result of a query (provided that this value is a scalar value). You can perform multiple assignments in the same SET statement. You can perform multiple assignments in the same statement.

Unlike [=](#page-1-0), the [:=](#page-0-2) operator is never interpreted as a comparison operator. This means you can use [:=](#page-0-2) in any valid SQL statement (not just in SET statements) to assign a value to a variable.

```
mysql> SELECT @var1, @var2;
 -> NULL, NULL
mysql> SELECT @var1 := 1, @var2;
 -> 1, NULL
mysql> SELECT @var1, @var2;
 -> 1, NULL
mysql> SELECT @var1, @var2 := @var1;
 -> 1, 1
mysql> SELECT @var1, @var2;
 -> 1, 1
mysql> SELECT @var1:=COUNT(*) FROM t1;
 -> 4
mysql> SELECT @var1;
 -> 4
```

You can make value assignments using [:=](#page-0-2) in other statements besides SELECT, such as UPDATE, as shown here:

```
mysql> SELECT @var1;
 -> 4
mysql> SELECT * FROM t1;
 -> 1, 3, 5, 7
mysql> UPDATE t1 SET c1 = 2 WHERE c1 = @var1:= 1;
Query OK, 1 row affected (0.00 sec)
Rows matched: 1 Changed: 1 Warnings: 0
mysql> SELECT @var1;
 -> 1
mysql> SELECT * FROM t1;
 -> 2, 3, 5, 7
```

While it is also possible both to set and to read the value of the same variable in a single SQL statement using the [:=](#page-0-2) operator, this is not recommended. Section 9.4, "User-Defined Variables", explains why you should avoid doing this.

<span id="page-1-0"></span>• [=](#page-1-0)

This operator is used to perform value assignments in two cases, described in the next two paragraphs.

Within a SET statement, = is treated as an assignment operator that causes the user variable on the left hand side of the operator to take on the value to its right. (In other words, when used in a SET statement, = is treated identically to [:=](#page-0-2).) The value on the right hand side may be a literal value, another variable storing a value, or any legal expression that yields a scalar value, including the result of a query (provided that this value is a scalar value). You can perform multiple assignments in the same SET statement.

In the SET clause of an UPDATE statement, = also acts as an assignment operator; in this case, however, it causes the column named on the left hand side of the operator to assume the value given to the right, provided any WHERE conditions that are part of the UPDATE are met. You can make multiple assignments in the same SET clause of an UPDATE statement.

In any other context, = is treated as a comparison operator.

```
mysql> SELECT @var1, @var2;
 -> NULL, NULL
mysql> SELECT @var1 := 1, @var2;
```

```
 -> 1, NULL
mysql> SELECT @var1, @var2;
 -> 1, NULL
mysql> SELECT @var1, @var2 := @var1;
 -> 1, 1
mysql> SELECT @var1, @var2;
 -> 1, 1
```

For more information, see Section 13.7.4.1, "SET Syntax for Variable Assignment", Section 13.2.11, "UPDATE Statement", and Section 13.2.10, "Subqueries".