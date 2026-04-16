# Oracle 23c - Data-Types
Source: https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/Data-Types.html

The data type boolean has the truth values `TRUE` and `FALSE`. If there is no `NOT NULL` constraint, the boolean data type also supports the truth value `UNKNOWN` as the null value.

You can use the boolean data type wherever data type appears in Oracle SQL syntax. For example, you can specify a boolean column with the keywords `BOOLEAN` or `BOOL` in `CREATE TABLE`:

```
CREATE TABLE example (id NUMBER, c1 BOOLEAN, c2 BOOL);
```

You can use SQL keywords `TRUE`, `FALSE` and `NULL` to represent states âTRUEâ, âFALSEâ, and âNULLâ respectively. For example, using the table `example` created above, you can insert the following:

```
INSERT INTO example VALUES (1, TRUE, NULL);
```

```
INSERT INTO example VALUES (2, FALSE, true);
```

You can use literals to represent "TRUE" and "FALSE" states. Case is not enforced in "TRUE" and "FALSE", you can have all lower case, all upper case, or a combination of upper and lower case. Leading and trailing white spaces are ignored.

Table 2-6 String Literals To Represent "TRUE" and "FALSE"

| STATE | TRUE | FALSE |
| --- | --- | --- |
| - | 'true' | 'false' |
| - | 'yes' | 'no' |
| - | 'on' | 'off' |
| - | '1' | '0' |
| - | 't' | 'f' |
| - | 'y' | 'n' |

Note that numbers are translated into boolean as follows:

Given the table `example` created below with two boolean columns `c1` and `c2`:

```
CREATE TABLE example (id NUMBER, c1 BOOLEAN, c2 BOOL);
```

Insert into `example` the following rows:

```
INSERT INTO example VALUES (1, TRUE, NULL);
INSERT INTO example VALUES (2, FALSE, true);
INSERT INTO example VALUES (3, 0, 'off');
INSERT INTO example VALUES (4, 'no', 'yes');
INSERT INTO example VALUES (5, 'f', 't' );
INSERT INTO example VALUES (6, false, true);
INSERT INTO example VALUES (7, 'on', 'off');
INSERT INTO example VALUES (8, -3.14, 1);
```

`SELECT` of a boolean type column always returns `TRUE` , `FALSE`. A value of `NULL` returns nothing.

```
SELECT * FROM example;
ID          C1      C2
---------- -----    -----
1          TRUE  
2          FALSE    TRUE
3          FALSE    FALSE
4          FALSE    TRUE
5          FALSE    TRUE
6          FALSE    TRUE
7          TRUE     FALSE
8          TRUE     TRUE
8 rows selected.
```

Constraints on Boolean Columns

The following constraints are supported on boolean columns:

* `NOT NULL`
* `UNIQUE`
* `PRIMARY KEY`
* `FOREIGN KEY`
* `CHECK`

Comparison and Assignment of Booleans

The following comparison operators are supported to compare boolean values: `=, !=, < >, <, <=, >, >=, GREATEST, LEAST, [NOT] IN`

```
SELECT * FROM example WHERE c1 = c2;

	ID   C1	C2
---------   -------  --------
	 3   FALSE    FALSE
	 8   TRUE     TRUE
```

```
SELECT * FROM example e1
WHERE c1 >= ALL (SELECT c2 FROM example e2 WHERE e2.id > e1.id);  

	ID    C1       C2
---------   -----    -------
	 1    TRUE
	 7    TRUE     FALSE
	 8    TRUE     TRUE
```

Operations on Booleans that Return Booleans

You can use the `NOT`, `AND`, and `OR` operators on SQL conditions, boolean columns, and boolean constants. For example:

```
 SELECT * FROM example WHERE NOT c2;

	ID    C1	 C2
---------    ------   ------
	 3    FALSE     FALSE
	 7    TRUE      FALSE
```

```
SELECT * FROM example WHERE c1 AND c2;

	ID   C1      C2
----------  -----  -------
	 8   TRUE    TRUE
```

```
SELECT * FROM example WHERE c1 AND TRUE;

	ID    C1	C2
----------   -------  -------
	 7    TRUE     FALSE
	 8    TRUE     TRUE
	 1    TRUE
```

```
SELECT * FROM example WHERE c1 OR c2;

	ID    C1	  C2
----------   --------- ------
        1    TRUE
	 2    FALSE     TRUE
	 4    FALSE     TRUE
	 5    FALSE     TRUE
	 6    FALSE     TRUE
	 7    TRUE      FALSE
	 8    TRUE      TRUE

7 rows selected.
```

Boolean Operator `NOT`

The `NOT` (TRUE) is FALSE. `NOT` (FALSE) is true. `NOT` (NULL) is NULL.

Boolean Operator `AND`

Truth Table for the AND Boolean Operator

|  |  |  |  |
| --- | --- | --- | --- |
| AND | TRUE | FALSE | NULL |
| TRUE | TRUE | FALSE | NULL |
| FALSE | FALSE | FALSE | FALSE |
| NULL | FALSE | FALSE | NULL |

Boolean Operator `OR`

Truth Table for the OR Boolean Operator

|  |  |  |  |
| --- | --- | --- | --- |
| OR | TRUE | FALSE | NULL |
| TRUE | TRUE | TRUE | TRUE |
| FALSE | TRUE | FALSE | NULL |
| NULL | TRUE | NULL | NULL |

Boolean Operator `IS`

Truth Table for the IS Boolean Operator

|  |  |  |  |
| --- | --- | --- | --- |
| IS | TRUE | FALSE | NULL |
| TRUE | TRUE | FALSE | FALSE |
| FALSE | FALSE | TRUE | FALSE |
| NULL | FALSE | FALSE | TRUE |

Boolean Operator `IS NOT`

Truth Table for the IS NOT Boolean Operator

|  |  |  |  |
| --- | --- | --- | --- |
| IS NOT | TRUE | FALSE | NULL |
| TRUE | FALSE | TRUE | TRUE |
| FALSE | TRUE | FALSE | TRUE |
| NULL | TRUE | TRUE | FALSE |

In addition to supporting SQL conditions, the `NOT`, `AND`, and `OR` operators support operations on boolean columns and boolean constants. For example, these are all valid statements:

```
SELECT * FROM example WHERE NOT c2;
SELECT * FROM example WHERE c1 AND c2;
SELECT * FROM example WHERE c1 AND TRUE;
SELECT * FROM example WHERE c1 OR c2;
```

You can use `IS [NOT] NULL` on a boolean value expression to determine its state. For example:

```
SELECT * FROM example WHERE c2 IS NULL;

	ID  C1	    C2
---------- ----------- -----------
	 1  TRUE
```

Booleans in SQL Expressions

Boolean expressions are supported in SQL syntax wherever `expr` is used.

SQL expressions and conditions have been enhanced to support the new boolean data type. Links to relevant SQL syntax:

[BOOLEAN Expressions](boolean-expressions.md#GUID-E492D339-5AAF-43C1-95B8-88DB1CDED0D9)

CAST Between Boolean Data Type and Other Oracle Built-In Data Types

The rules to cast between `BOOLEAN` and other Oracle built-in data types are as follows:

When casting

`BOOLEAN`

to numeric :

When casting numeric to

`BOOLEAN`

:

* If the numeric value is non-zero (e.g., 1, 2, -3, 1.2), then resulting value is true.
* If the numeric value is zero, then resulting value is false.

When casting

 `BOOLEAN`

to

`CHAR(n)`

and

`NCHAR(n)`

:

* If the boolean value is true and `n` is not less than 4, then the resulting value is 'TRUE' extended on the right by `n` - 4 spaces.
* If the boolean value is false and `n` is not less than 5, then the resulting value is 'FALSE' extended on the right by `n` – 5 spaces.
* Otherwise, a data exception error is raised.

When casting a character string to boolean, leading and trailing spaces of the character string are ignored. If the resulting character string is one of the accepted literals used to determine a valid boolean value, then the result is that valid boolean value.

When casting

`BOOLEAN`

to

`VARCHAR(n)`

,

`NVARCHAR(n)`

* If the boolean value is true and `n` is not less than 4, then resulting value is true.
* If the boolean value is false and `n` is not less than 5, then resulting value is false.
* Otherwise, a data exception error is raised.

You can use the function `TO_BOOLEAN` to explicitly convert character value expressions or numeric value expressions to boolean values.

Functions `TO_CHAR`, `TO_NCHAR`, `TO_CLOB`, `TO_NCLOB`, `TO_NUMBER`, `TO_BINARY_DOUBLE`, and `TO_BINARY_FLOAT` have boolean overloads to convert boolean values to number or character types.