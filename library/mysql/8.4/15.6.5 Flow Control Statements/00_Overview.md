---
source: MySQL 8.4 Reference
title: 00_Overview
---

MySQL supports the [IF](#page-181-0), [CASE](#page-180-0), [ITERATE](#page-182-1), [LEAVE](#page-182-2) [LOOP](#page-182-0), [WHILE](#page-183-1), and [REPEAT](#page-183-0) constructs for flow control within stored programs. It also supports [RETURN](#page-183-2) within stored functions.

Many of these constructs contain other statements, as indicated by the grammar specifications in the following sections. Such constructs may be nested. For example, an [IF](#page-181-0) statement might contain a [WHILE](#page-183-1) loop, which itself contains a [CASE](#page-180-0) statement.

MySQL does not support FOR loops.

# <span id="page-180-0"></span>**15.6.5.1 CASE Statement**

```
CASE case_value
 WHEN when_value THEN statement_list
 [WHEN when_value THEN statement_list] ...
 [ELSE statement_list]
END CASE
```

Or:

```
CASE
 WHEN search_condition THEN statement_list
 [WHEN search_condition THEN statement_list] ...
 [ELSE statement_list]
END CASE
```

The [CASE](#page-180-0) statement for stored programs implements a complex conditional construct.

![](_page_180_Picture_12.jpeg)

#### **Note**

There is also a CASE operator, which differs from the [CASE](#page-180-0) statement described here. See Section 14.5, "Flow Control Functions". The [CASE](#page-180-0) statement cannot have an ELSE NULL clause, and it is terminated with END CASE instead of END.

For the first syntax, case\_value is an expression. This value is compared to the when\_value expression in each WHEN clause until one of them is equal. When an equal when\_value is found, the corresponding THEN clause statement\_list executes. If no when\_value is equal, the ELSE clause statement\_list executes, if there is one.

This syntax cannot be used to test for equality with NULL because NULL = NULL is false. See Section 5.3.4.6, "Working with NULL Values".

For the second syntax, each WHEN clause search\_condition expression is evaluated until one is true, at which point its corresponding THEN clause statement\_list executes. If no search\_condition is equal, the ELSE clause statement\_list executes, if there is one.

If no when\_value or search\_condition matches the value tested and the [CASE](#page-180-0) statement contains no ELSE clause, a Case not found for CASE statement error results.

Each statement\_list consists of one or more SQL statements; an empty statement\_list is not permitted.

To handle situations where no value is matched by any WHEN clause, use an ELSE containing an empty [BEGIN ... END](#page-177-0) block, as shown in this example. (The indentation used here in the ELSE clause is for purposes of clarity only, and is not otherwise significant.)

```
DELIMITER |
CREATE PROCEDURE p()
 BEGIN
 DECLARE v INT DEFAULT 1;
 CASE v
 WHEN 2 THEN SELECT v;
 WHEN 3 THEN SELECT 0;
 ELSE
 BEGIN
 END;
 END CASE;
 END;
 |
```

## <span id="page-181-0"></span>**15.6.5.2 IF Statement**

```
IF search_condition THEN statement_list
 [ELSEIF search_condition THEN statement_list] ...
 [ELSE statement_list]
END IF
```

The [IF](#page-181-0) statement for stored programs implements a basic conditional construct.

![](_page_181_Picture_8.jpeg)

#### **Note**

There is also an IF() function, which differs from the [IF](#page-181-0) statement described here. See Section 14.5, "Flow Control Functions". The [IF](#page-181-0) statement can have THEN, ELSE, and ELSEIF clauses, and it is terminated with END IF.

If a given search\_condition evaluates to true, the corresponding THEN or ELSEIF clause statement\_list executes. If no search\_condition matches, the ELSE clause statement\_list executes.

Each statement\_list consists of one or more SQL statements; an empty statement\_list is not permitted.

An IF ... END IF block, like all other flow-control blocks used within stored programs, must be terminated with a semicolon, as shown in this example:

```
DELIMITER //
CREATE FUNCTION SimpleCompare(n INT, m INT)
 RETURNS VARCHAR(20)
 BEGIN
 DECLARE s VARCHAR(20);
 IF n > m THEN SET s = '>';
 ELSEIF n = m THEN SET s = '=';
 ELSE SET s = '<';
 END IF;
 SET s = CONCAT(n, ' ', s, ' ', m);
 RETURN s;
```

```
 END //
DELIMITER ;
```

As with other flow-control constructs, IF ... END IF blocks may be nested within other flow-control constructs, including other [IF](#page-181-0) statements. Each [IF](#page-181-0) must be terminated by its own END IF followed by a semicolon. You can use indentation to make nested flow-control blocks more easily readable by humans (although this is not required by MySQL), as shown here:

```
DELIMITER //
CREATE FUNCTION VerboseCompare (n INT, m INT)
 RETURNS VARCHAR(50)
 BEGIN
 DECLARE s VARCHAR(50);
 IF n = m THEN SET s = 'equals';
 ELSE
 IF n > m THEN SET s = 'greater';
 ELSE SET s = 'less';
 END IF;
 SET s = CONCAT('is ', s, ' than');
 END IF;
 SET s = CONCAT(n, ' ', s, ' ', m, '.');
 RETURN s;
 END //
DELIMITER ;
```

In this example, the inner [IF](#page-181-0) is evaluated only if n is not equal to m.

# <span id="page-182-1"></span>**15.6.5.3 ITERATE Statement**

```
ITERATE label
```

[ITERATE](#page-182-1) can appear only within [LOOP](#page-182-0), [REPEAT](#page-183-0), and [WHILE](#page-183-1) statements. [ITERATE](#page-182-1) means "start the loop again."

For an example, see [Section 15.6.5.5, "LOOP Statement".](#page-182-0)

# <span id="page-182-2"></span>**15.6.5.4 LEAVE Statement**

```
LEAVE label
```

This statement is used to exit the flow control construct that has the given label. If the label is for the outermost stored program block, [LEAVE](#page-182-2) exits the program.

[LEAVE](#page-182-2) can be used within [BEGIN ... END](#page-177-0) or loop constructs ([LOOP](#page-182-0), [REPEAT](#page-183-0), [WHILE](#page-183-1)).

For an example, see [Section 15.6.5.5, "LOOP Statement".](#page-182-0)

## <span id="page-182-0"></span>**15.6.5.5 LOOP Statement**

```
[begin_label:] LOOP
 statement_list
END LOOP [end_label]
```

[LOOP](#page-182-0) implements a simple loop construct, enabling repeated execution of the statement list, which consists of one or more statements, each terminated by a semicolon (;) statement delimiter. The statements within the loop are repeated until the loop is terminated. Usually, this is accomplished with a [LEAVE](#page-182-2) statement. Within a stored function, [RETURN](#page-183-2) can also be used, which exits the function entirely.

Neglecting to include a loop-termination statement results in an infinite loop.

A [LOOP](#page-182-0) statement can be labeled. For the rules regarding label use, see [Section 15.6.2, "Statement](#page-177-1) [Labels".](#page-177-1)

#### Example:

```
CREATE PROCEDURE doiterate(p1 INT)
BEGIN
 label1: LOOP
 SET p1 = p1 + 1;
 IF p1 < 10 THEN
 ITERATE label1;
 END IF;
 LEAVE label1;
 END LOOP label1;
 SET @x = p1;
END;
```

## <span id="page-183-0"></span>**15.6.5.6 REPEAT Statement**

```
[begin_label:] REPEAT
 statement_list
UNTIL search_condition
END REPEAT [end_label]
```

The statement list within a [REPEAT](#page-183-0) statement is repeated until the search\_condition expression is true. Thus, a [REPEAT](#page-183-0) always enters the loop at least once. statement\_list consists of one or more statements, each terminated by a semicolon (;) statement delimiter.

A [REPEAT](#page-183-0) statement can be labeled. For the rules regarding label use, see [Section 15.6.2, "Statement](#page-177-1) [Labels".](#page-177-1)

#### Example:

```
mysql> delimiter //
mysql> CREATE PROCEDURE dorepeat(p1 INT)
 BEGIN
 SET @x = 0;
 REPEAT
 SET @x = @x + 1;
 UNTIL @x > p1 END REPEAT;
 END
 //
Query OK, 0 rows affected (0.00 sec)
mysql> CALL dorepeat(1000)//
Query OK, 0 rows affected (0.00 sec)
mysql> SELECT @x//
+------+
| @x |
+------+
| 1001 |
+------+
1 row in set (0.00 sec)
```

# <span id="page-183-2"></span>**15.6.5.7 RETURN Statement**

```
RETURN expr
```

The [RETURN](#page-183-2) statement terminates execution of a stored function and returns the value expr to the function caller. There must be at least one [RETURN](#page-183-2) statement in a stored function. There may be more than one if the function has multiple exit points.

This statement is not used in stored procedures, triggers, or events. The [LEAVE](#page-182-2) statement can be used to exit a stored program of those types.

# <span id="page-183-1"></span>**15.6.5.8 WHILE Statement**

```
[begin_label:] WHILE search_condition DO
 statement_list
END WHILE [end_label]
```

The statement list within a [WHILE](#page-183-1) statement is repeated as long as the search\_condition expression is true. statement\_list consists of one or more SQL statements, each terminated by a semicolon (;) statement delimiter.

A [WHILE](#page-183-1) statement can be labeled. For the rules regarding label use, see [Section 15.6.2, "Statement](#page-177-1) [Labels".](#page-177-1)

#### Example:

```
CREATE PROCEDURE dowhile()
BEGIN
 DECLARE v1 INT DEFAULT 5;
 WHILE v1 > 0 DO
 ...
 SET v1 = v1 - 1;
 END WHILE;
END;
```

# <span id="page-184-0"></span>**15.6.6 Cursors**

MySQL supports cursors inside stored programs. The syntax is as in embedded SQL. Cursors have these properties:

- Asensitive: The server may or may not make a copy of its result table
- Read only: Not updatable
- Nonscrollable: Can be traversed only in one direction and cannot skip rows

Cursor declarations must appear before handler declarations and after variable and condition declarations.

### Example:

```
CREATE PROCEDURE curdemo()
BEGIN
 DECLARE done INT DEFAULT FALSE;
 DECLARE a CHAR(16);
 DECLARE b, c INT;
 DECLARE cur1 CURSOR FOR SELECT id,data FROM test.t1;
 DECLARE cur2 CURSOR FOR SELECT i FROM test.t2;
 DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
 OPEN cur1;
 OPEN cur2;
 read_loop: LOOP
 FETCH cur1 INTO a, b;
 FETCH cur2 INTO c;
 IF done THEN
 LEAVE read_loop;
 END IF;
 IF b < c THEN
 INSERT INTO test.t3 VALUES (a,b);
 ELSE
 INSERT INTO test.t3 VALUES (a,c);
 END IF;
 END LOOP;
 CLOSE cur1;
 CLOSE cur2;
END;
```