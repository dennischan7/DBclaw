---
source: MySQL 5.7 Reference
title: 00_Overview
---

Server-side cursors are implemented in the C API using the [mysql\\_stmt\\_attr\\_set\(\)](https://dev.mysql.com/doc/c-api/5.7/en/mysql-stmt-attr-set.md) function. The same implementation is used for cursors in stored routines. A server-side cursor enables a result set to be generated on the server side, but not transferred to the client except for those rows that the client requests. For example, if a client executes a query but is only interested in the first row, the remaining rows are not transferred.

In MySQL, a server-side cursor is materialized into an internal temporary table. Initially, this is a MEMORY table, but is converted to a MyISAM table when its size exceeds the minimum value of the max\_heap\_table\_size and tmp\_table\_size system variables. The same restrictions apply to internal temporary tables created to hold the result set for a cursor as for other uses of internal temporary tables. See Section 8.4.4, "Internal Temporary Table Use in MySQL". One limitation of the implementation is that for a large result set, retrieving its rows through a cursor might be slow.

Cursors are read only; you cannot use a cursor to update rows.

UPDATE WHERE CURRENT OF and DELETE WHERE CURRENT OF are not implemented, because updatable cursors are not supported.

Cursors are nonholdable (not held open after a commit).

Cursors are asensitive.

Cursors are nonscrollable.

Cursors are not named. The statement handler acts as the cursor ID.

You can have open only a single cursor per prepared statement. If you need several cursors, you must prepare several statements.

You cannot use a cursor for a statement that generates a result set if the statement is not supported in prepared mode. This includes statements such as [CHECK TABLE](#page-118-0), HANDLER READ, and [SHOW](#page-135-1) [BINLOG EVENTS](#page-135-1).

# <span id="page-62-0"></span>**13.6.7 Condition Handling**

Conditions may arise during stored program execution that require special handling, such as exiting the current program block or continuing execution. Handlers can be defined for general conditions such as warnings or exceptions, or for specific conditions such as a particular error code. Specific conditions can be assigned names and referred to that way in handlers.

To name a condition, use the [DECLARE ... CONDITION](#page-62-1) statement. To declare a handler, use the [DECLARE ... HANDLER](#page-63-0) statement. See [Section 13.6.7.1, "DECLARE ... CONDITION Statement",](#page-62-1) and [Section 13.6.7.2, "DECLARE ... HANDLER Statement"](#page-63-0). For information about how the server chooses handlers when a condition occurs, see [Section 13.6.7.6, "Scope Rules for Handlers"](#page-81-0).

To raise a condition, use the [SIGNAL](#page-76-0) statement. To modify condition information within a condition handler, use [RESIGNAL](#page-72-0). See [Section 13.6.7.1, "DECLARE ... CONDITION Statement"](#page-62-1), and [Section 13.6.7.2, "DECLARE ... HANDLER Statement".](#page-63-0)

To retrieve information from the diagnostics area, use the [GET DIAGNOSTICS](#page-66-0) statement (see [Section 13.6.7.3, "GET DIAGNOSTICS Statement"](#page-66-0)). For information about the diagnostics area, see [Section 13.6.7.7, "The MySQL Diagnostics Area"](#page-84-0).

## <span id="page-62-1"></span>**13.6.7.1 DECLARE ... CONDITION Statement**

```
DECLARE condition_name CONDITION FOR condition_value
condition_value: {
 mysql_error_code
 | SQLSTATE [VALUE] sqlstate_value
}
```

The [DECLARE ... CONDITION](#page-62-1) statement declares a named error condition, associating a name with a condition that needs specific handling. The name can be referred to in a subsequent [DECLARE ...](#page-63-0) [HANDLER](#page-63-0) statement (see [Section 13.6.7.2, "DECLARE ... HANDLER Statement"](#page-63-0)).

Condition declarations must appear before cursor or handler declarations.

The condition\_value for [DECLARE ... CONDITION](#page-62-1) indicates the specific condition or class of conditions to associate with the condition name. It can take the following forms:

• mysql\_error\_code: An integer literal indicating a MySQL error code.

Do not use MySQL error code 0 because that indicates success rather than an error condition. For a list of MySQL error codes, see [Server Error Message Reference.](https://dev.mysql.com/doc/mysql-errors/5.7/en/server-error-reference.md)

• SQLSTATE [VALUE] sqlstate\_value: A 5-character string literal indicating an SQLSTATE value.

Do not use SQLSTATE values that begin with '00' because those indicate success rather than an error condition. For a list of SQLSTATE values, see [Server Error Message Reference.](https://dev.mysql.com/doc/mysql-errors/5.7/en/server-error-reference.md)

Condition names referred to in [SIGNAL](#page-76-0) or use [RESIGNAL](#page-72-0) statements must be associated with SQLSTATE values, not MySQL error codes.

Using names for conditions can help make stored program code clearer. For example, this handler applies to attempts to drop a nonexistent table, but that is apparent only if you know that 1051 is the MySQL error code for "unknown table":

```
DECLARE CONTINUE HANDLER FOR 1051
 BEGIN
 -- body of handler
 END;
```

By declaring a name for the condition, the purpose of the handler is more readily seen:

```
DECLARE no_such_table CONDITION FOR 1051;
DECLARE CONTINUE HANDLER FOR no_such_table
 BEGIN
 -- body of handler
 END;
```

Here is a named condition for the same condition, but based on the corresponding SQLSTATE value rather than the MySQL error code:

```
DECLARE no_such_table CONDITION FOR SQLSTATE '42S02';
DECLARE CONTINUE HANDLER FOR no_such_table
 BEGIN
 -- body of handler
 END;
```

## <span id="page-63-0"></span>**13.6.7.2 DECLARE ... HANDLER Statement**

```
DECLARE handler_action HANDLER
 FOR condition_value [, condition_value] ...
 statement
handler_action: {
 CONTINUE
 | EXIT
 | UNDO
}
condition_value: {
 mysql_error_code
 | SQLSTATE [VALUE] sqlstate_value
 | condition_name
 | SQLWARNING
 | NOT FOUND
 | SQLEXCEPTION
}
```

The [DECLARE ... HANDLER](#page-63-0) statement specifies a handler that deals with one or more conditions. If one of these conditions occurs, the specified statement executes. statement can be a simple statement such as SET var\_name = value, or a compound statement written using BEGIN and END (see [Section 13.6.1, "BEGIN ... END Compound Statement"\)](#page-52-0).

Handler declarations must appear after variable or condition declarations.

The handler\_action value indicates what action the handler takes after execution of the handler statement:

- CONTINUE: Execution of the current program continues.
- EXIT: Execution terminates for the [BEGIN ... END](#page-52-0) compound statement in which the handler is declared. This is true even if the condition occurs in an inner block.
- UNDO: Not supported.

The condition\_value for [DECLARE ... HANDLER](#page-63-0) indicates the specific condition or class of conditions that activates the handler. It can take the following forms:

• mysql\_error\_code: An integer literal indicating a MySQL error code, such as 1051 to specify "unknown table":

```
DECLARE CONTINUE HANDLER FOR 1051
 BEGIN
 -- body of handler
 END;
```

Do not use MySQL error code 0 because that indicates success rather than an error condition. For a list of MySQL error codes, see [Server Error Message Reference.](https://dev.mysql.com/doc/mysql-errors/5.7/en/server-error-reference.md)

• SQLSTATE [VALUE] sqlstate\_value: A 5-character string literal indicating an SQLSTATE value, such as '42S01' to specify "unknown table":

```
DECLARE CONTINUE HANDLER FOR SQLSTATE '42S02'
 BEGIN
 -- body of handler
 END;
```

Do not use SQLSTATE values that begin with '00' because those indicate success rather than an error condition. For a list of SQLSTATE values, see [Server Error Message Reference.](https://dev.mysql.com/doc/mysql-errors/5.7/en/server-error-reference.md)

- condition\_name: A condition name previously specified with [DECLARE ... CONDITION](#page-62-1). A condition name can be associated with a MySQL error code or SQLSTATE value. See [Section 13.6.7.1, "DECLARE ... CONDITION Statement"](#page-62-1).
- SQLWARNING: Shorthand for the class of SQLSTATE values that begin with '01'.

```
DECLARE CONTINUE HANDLER FOR SQLWARNING
 BEGIN
 -- body of handler
 END;
```

• NOT FOUND: Shorthand for the class of SQLSTATE values that begin with '02'. This is relevant within the context of cursors and is used to control what happens when a cursor reaches the end of a data set. If no more rows are available, a No Data condition occurs with SQLSTATE value '02000'. To detect this condition, you can set up a handler for it or for a NOT FOUND condition.

```
DECLARE CONTINUE HANDLER FOR NOT FOUND
 BEGIN
 -- body of handler
 END;
```

For another example, see [Section 13.6.6, "Cursors".](#page-59-1) The NOT FOUND condition also occurs for SELECT ... INTO var\_list statements that retrieve no rows.

• SQLEXCEPTION: Shorthand for the class of SQLSTATE values that do not begin with '00', '01', or '02'.

```
DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
 BEGIN
 -- body of handler
 END;
```

For information about how the server chooses handlers when a condition occurs, see [Section 13.6.7.6,](#page-81-0) ["Scope Rules for Handlers".](#page-81-0)

If a condition occurs for which no handler has been declared, the action taken depends on the condition class:

- For SQLEXCEPTION conditions, the stored program terminates at the statement that raised the condition, as if there were an EXIT handler. If the program was called by another stored program, the calling program handles the condition using the handler selection rules applied to its own handlers.
- For SQLWARNING conditions, the program continues executing, as if there were a CONTINUE handler.
- For NOT FOUND conditions, if the condition was raised normally, the action is CONTINUE. If it was raised by [SIGNAL](#page-76-0) or [RESIGNAL](#page-72-0), the action is EXIT.

The following example uses a handler for SQLSTATE '23000', which occurs for a duplicate-key error:

```
mysql> CREATE TABLE test.t (s1 INT, PRIMARY KEY (s1));
Query OK, 0 rows affected (0.00 sec)
```

```
mysql> delimiter //
mysql> CREATE PROCEDURE handlerdemo ()
 BEGIN
 DECLARE CONTINUE HANDLER FOR SQLSTATE '23000' SET @x2 = 1;
 SET @x = 1;
 INSERT INTO test.t VALUES (1);
 SET @x = 2;
 INSERT INTO test.t VALUES (1);
 SET @x = 3;
 END;
 //
Query OK, 0 rows affected (0.00 sec)
mysql> CALL handlerdemo()//
Query OK, 0 rows affected (0.00 sec)
mysql> SELECT @x//
 +------+
 | @x |
 +------+
 | 3 |
 +------+
 1 row in set (0.00 sec)
```

Notice that @x is 3 after the procedure executes, which shows that execution continued to the end of the procedure after the error occurred. If the [DECLARE ... HANDLER](#page-63-0) statement had not been present, MySQL would have taken the default action (EXIT) after the second INSERT failed due to the PRIMARY KEY constraint, and SELECT @x would have returned 2.

To ignore a condition, declare a CONTINUE handler for it and associate it with an empty block. For example:

```
DECLARE CONTINUE HANDLER FOR SQLWARNING BEGIN END;
```

The scope of a block label does not include the code for handlers declared within the block. Therefore, the statement associated with a handler cannot use [ITERATE](#page-57-0) or [LEAVE](#page-58-2) to refer to labels for blocks that enclose the handler declaration. Consider the following example, where the [REPEAT](#page-58-1) block has a label of retry:

```
CREATE PROCEDURE p ()
BEGIN
 DECLARE i INT DEFAULT 3;
 retry:
 REPEAT
 BEGIN
 DECLARE CONTINUE HANDLER FOR SQLWARNING
 BEGIN
 ITERATE retry; # illegal
 END;
 IF i < 0 THEN
 LEAVE retry; # legal
 END IF;
 SET i = i - 1;
 END;
 UNTIL FALSE END REPEAT;
END;
```

The retry label is in scope for the [IF](#page-56-0) statement within the block. It is not in scope for the CONTINUE handler, so the reference there is invalid and results in an error:

```
ERROR 1308 (42000): LEAVE with no matching label: retry
```

To avoid references to outer labels in handlers, use one of these strategies:

• To leave the block, use an EXIT handler. If no block cleanup is required, the [BEGIN ... END](#page-52-0) handler body can be empty:

```
DECLARE EXIT HANDLER FOR SQLWARNING BEGIN END;
```

Otherwise, put the cleanup statements in the handler body:

```
DECLARE EXIT HANDLER FOR SQLWARNING
 BEGIN
 block cleanup statements
 END;
```

• To continue execution, set a status variable in a CONTINUE handler that can be checked in the enclosing block to determine whether the handler was invoked. The following example uses the variable done for this purpose:

```
CREATE PROCEDURE p ()
BEGIN
 DECLARE i INT DEFAULT 3;
 DECLARE done INT DEFAULT FALSE;
 retry:
 REPEAT
 BEGIN
 DECLARE CONTINUE HANDLER FOR SQLWARNING
 BEGIN
 SET done = TRUE;
 END;
 IF done OR i < 0 THEN
 LEAVE retry;
 END IF;
 SET i = i - 1;
 END;
 UNTIL FALSE END REPEAT;
END;
```

# <span id="page-66-0"></span>**13.6.7.3 GET DIAGNOSTICS Statement**

```
GET [CURRENT | STACKED] DIAGNOSTICS {
 statement_information_item
 [, statement_information_item] ...
 | CONDITION condition_number
 condition_information_item
 [, condition_information_item] ...
}
statement_information_item:
 target = statement_information_item_name
condition_information_item:
 target = condition_information_item_name
statement_information_item_name: {
 NUMBER
 | ROW_COUNT
}
condition_information_item_name: {
 CLASS_ORIGIN
 | SUBCLASS_ORIGIN
 | RETURNED_SQLSTATE
 | MESSAGE_TEXT
 | MYSQL_ERRNO
 | CONSTRAINT_CATALOG
 | CONSTRAINT_SCHEMA
 | CONSTRAINT_NAME
 | CATALOG_NAME
 | SCHEMA_NAME
 | TABLE_NAME
 | COLUMN_NAME
 | CURSOR_NAME
}
condition_number, target:
```

```
 (see following discussion)
```

SQL statements produce diagnostic information that populates the diagnostics area. The [GET](#page-66-0) [DIAGNOSTICS](#page-66-0) statement enables applications to inspect this information. (You can also use [SHOW](#page-182-0) [WARNINGS](#page-182-0) or [SHOW ERRORS](#page-151-0) to see conditions or errors.)

No special privileges are required to execute [GET DIAGNOSTICS](#page-66-0).

The keyword CURRENT means to retrieve information from the current diagnostics area. The keyword STACKED means to retrieve information from the second diagnostics area, which is available only if the current context is a condition handler. If neither keyword is given, the default is to use the current diagnostics area.

The [GET DIAGNOSTICS](#page-66-0) statement is typically used in a handler within a stored program. It is a MySQL extension that [GET \[CURRENT\] DIAGNOSTICS](#page-66-0) is permitted outside handler context to check the execution of any SQL statement. For example, if you invoke the mysql client program, you can enter these statements at the prompt:

```
mysql> DROP TABLE test.no_such_table;
ERROR 1051 (42S02): Unknown table 'test.no_such_table'
mysql> GET DIAGNOSTICS CONDITION 1
 @p1 = RETURNED_SQLSTATE, @p2 = MESSAGE_TEXT;
mysql> SELECT @p1, @p2;
+-------+------------------------------------+
| @p1 | @p2 |
+-------+------------------------------------+
| 42S02 | Unknown table 'test.no_such_table' |
+-------+------------------------------------+
```

This extension applies only to the current diagnostics area. It does not apply to the second diagnostics area because GET STACKED DIAGNOSTICS is permitted only if the current context is a condition handler. If that is not the case, a GET STACKED DIAGNOSTICS when handler not active error occurs.

For a description of the diagnostics area, see [Section 13.6.7.7, "The MySQL Diagnostics Area".](#page-84-0) Briefly, it contains two kinds of information:

- Statement information, such as the number of conditions that occurred or the affected-rows count.
- Condition information, such as the error code and message. If a statement raises multiple conditions, this part of the diagnostics area has a condition area for each one. If a statement raises no conditions, this part of the diagnostics area is empty.

For a statement that produces three conditions, the diagnostics area contains statement and condition information like this:

```
Statement information:
 row count
 ... other statement information items ...
Condition area list:
 Condition area 1:
 error code for condition 1
 error message for condition 1
 ... other condition information items ...
 Condition area 2:
 error code for condition 2:
 error message for condition 2
 ... other condition information items ...
 Condition area 3:
 error code for condition 3
 error message for condition 3
 ... other condition information items ...
```

[GET DIAGNOSTICS](#page-66-0) can obtain either statement or condition information, but not both in the same statement:

• To obtain statement information, retrieve the desired statement items into target variables. This instance of [GET DIAGNOSTICS](#page-66-0) assigns the number of available conditions and the rows-affected count to the user variables @p1 and @p2:

```
GET DIAGNOSTICS @p1 = NUMBER, @p2 = ROW_COUNT;
```

• To obtain condition information, specify the condition number and retrieve the desired condition items into target variables. This instance of [GET DIAGNOSTICS](#page-66-0) assigns the SQLSTATE value and error message to the user variables @p3 and @p4:

```
GET DIAGNOSTICS CONDITION 1
 @p3 = RETURNED_SQLSTATE, @p4 = MESSAGE_TEXT;
```

The retrieval list specifies one or more target = item\_name assignments, separated by commas. Each assignment names a target variable and either a statement\_information\_item\_name or condition\_information\_item\_name designator, depending on whether the statement retrieves statement or condition information.

Valid target designators for storing item information can be stored procedure or function parameters, stored program local variables declared with [DECLARE](#page-53-1), or user-defined variables.

Valid condition\_number designators can be stored procedure or function parameters, stored program local variables declared with [DECLARE](#page-53-1), user-defined variables, system variables, or literals. A character literal may include a \_charset introducer. A warning occurs if the condition number is not in the range from 1 to the number of condition areas that have information. In this case, the warning is added to the diagnostics area without clearing it.

When a condition occurs, MySQL does not populate all condition items recognized by [GET](#page-66-0) [DIAGNOSTICS](#page-66-0). For example:

```
mysql> GET DIAGNOSTICS CONDITION 1
 @p5 = SCHEMA_NAME, @p6 = TABLE_NAME;
mysql> SELECT @p5, @p6;
+------+------+
| @p5 | @p6 |
+------+------+
| | |
+------+------+
```

In standard SQL, if there are multiple conditions, the first condition relates to the SQLSTATE value returned for the previous SQL statement. In MySQL, this is not guaranteed. To get the main error, you cannot do this:

```
GET DIAGNOSTICS CONDITION 1 @errno = MYSQL_ERRNO;
```

Instead, retrieve the condition count first, then use it to specify which condition number to inspect:

```
GET DIAGNOSTICS @cno = NUMBER;
GET DIAGNOSTICS CONDITION @cno @errno = MYSQL_ERRNO;
```

For information about permissible statement and condition information items, and which ones are populated when a condition occurs, see [Diagnostics Area Information Items](#page-84-1).

Here is an example that uses [GET DIAGNOSTICS](#page-66-0) and an exception handler in stored procedure context to assess the outcome of an insert operation. If the insert was successful, the procedure uses [GET DIAGNOSTICS](#page-66-0) to get the rows-affected count. This shows that you can use [GET DIAGNOSTICS](#page-66-0) multiple times to retrieve information about a statement as long as the current diagnostics area has not been cleared.

```
CREATE PROCEDURE do_insert(value INT)
BEGIN
 -- Declare variables to hold diagnostics area information
 DECLARE code CHAR(5) DEFAULT '00000';
 DECLARE msg TEXT;
```

```
 DECLARE nrows INT;
 DECLARE result TEXT;
 -- Declare exception handler for failed insert
 DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
 BEGIN
 GET DIAGNOSTICS CONDITION 1
 code = RETURNED_SQLSTATE, msg = MESSAGE_TEXT;
 END;
 -- Perform the insert
 INSERT INTO t1 (int_col) VALUES(value);
 -- Check whether the insert was successful
 IF code = '00000' THEN
 GET DIAGNOSTICS nrows = ROW_COUNT;
 SET result = CONCAT('insert succeeded, row count = ',nrows);
 ELSE
 SET result = CONCAT('insert failed, error = ',code,', message = ',msg);
 END IF;
 -- Say what happened
 SELECT result;
END;
```

Suppose that t1.int\_col is an integer column that is declared as NOT NULL. The procedure produces these results when invoked to insert non-NULL and NULL values, respectively:

```
mysql> CALL do_insert(1);
+---------------------------------+
| result |
+---------------------------------+
| insert succeeded, row count = 1 |
+---------------------------------+
mysql> CALL do_insert(NULL);
+-------------------------------------------------------------------------+
| result |
+-------------------------------------------------------------------------+
| insert failed, error = 23000, message = Column 'int_col' cannot be null |
+-------------------------------------------------------------------------+
```

When a condition handler activates, a push to the diagnostics area stack occurs:

- The first (current) diagnostics area becomes the second (stacked) diagnostics area and a new current diagnostics area is created as a copy of it.
- [GET \[CURRENT\] DIAGNOSTICS](#page-66-0) and [GET STACKED DIAGNOSTICS](#page-66-0) can be used within the handler to access the contents of the current and stacked diagnostics areas.
- Initially, both diagnostics areas return the same result, so it is possible to get information from the current diagnostics area about the condition that activated the handler, as long as you execute no statements within the handler that change its current diagnostics area.
- However, statements executing within the handler can modify the current diagnostics area, clearing and setting its contents according to the normal rules (see [How the Diagnostics Area is Cleared and](#page-85-0) [Populated](#page-85-0)).

A more reliable way to obtain information about the handler-activating condition is to use the stacked diagnostics area, which cannot be modified by statements executing within the handler except [RESIGNAL](#page-72-0). For information about when the current diagnostics area is set and cleared, see [Section 13.6.7.7, "The MySQL Diagnostics Area"](#page-84-0).

The next example shows how GET STACKED DIAGNOSTICS can be used within a handler to obtain information about the handled exception, even after the current diagnostics area has been modified by handler statements.

Within a stored procedure p(), we attempt to insert two values into a table that contains a TEXT NOT NULL column. The first value is a non-NULL string and the second is NULL. The column prohibits NULL values, so the first insert succeeds but the second causes an exception. The procedure includes an exception handler that maps attempts to insert NULL into inserts of the empty string:

```
DROP TABLE IF EXISTS t1;
CREATE TABLE t1 (c1 TEXT NOT NULL);
DROP PROCEDURE IF EXISTS p;
delimiter //
CREATE PROCEDURE p ()
BEGIN
 -- Declare variables to hold diagnostics area information
 DECLARE errcount INT;
 DECLARE errno INT;
 DECLARE msg TEXT;
 DECLARE EXIT HANDLER FOR SQLEXCEPTION
 BEGIN
 -- Here the current DA is nonempty because no prior statements
 -- executing within the handler have cleared it
 GET CURRENT DIAGNOSTICS CONDITION 1
 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
 SELECT 'current DA before mapped insert' AS op, errno, msg;
 GET STACKED DIAGNOSTICS CONDITION 1
 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
 SELECT 'stacked DA before mapped insert' AS op, errno, msg;
 -- Map attempted NULL insert to empty string insert
 INSERT INTO t1 (c1) VALUES('');
 -- Here the current DA should be empty (if the INSERT succeeded),
 -- so check whether there are conditions before attempting to
 -- obtain condition information
 GET CURRENT DIAGNOSTICS errcount = NUMBER;
 IF errcount = 0
 THEN
 SELECT 'mapped insert succeeded, current DA is empty' AS op;
 ELSE
 GET CURRENT DIAGNOSTICS CONDITION 1
 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
 SELECT 'current DA after mapped insert' AS op, errno, msg;
 END IF ;
 GET STACKED DIAGNOSTICS CONDITION 1
 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
 SELECT 'stacked DA after mapped insert' AS op, errno, msg;
 END;
 INSERT INTO t1 (c1) VALUES('string 1');
 INSERT INTO t1 (c1) VALUES(NULL);
END;
//
delimiter ;
CALL p();
SELECT * FROM t1;
```

When the handler activates, a copy of the current diagnostics area is pushed to the diagnostics area stack. The handler first displays the contents of the current and stacked diagnostics areas, which are both the same initially:

```
+---------------------------------+-------+----------------------------+
| op | errno | msg |
+---------------------------------+-------+----------------------------+
| current DA before mapped insert | 1048 | Column 'c1' cannot be null |
+---------------------------------+-------+----------------------------+
+---------------------------------+-------+----------------------------+
| op | errno | msg |
+---------------------------------+-------+----------------------------+
| stacked DA before mapped insert | 1048 | Column 'c1' cannot be null |
+---------------------------------+-------+----------------------------+
```

Statements executing after the [GET DIAGNOSTICS](#page-66-0) statements may reset the current diagnostics area. statements may reset the current diagnostics area. For example, the handler maps the NULL insert to an empty-string insert and displays the result. The new insert succeeds and clears the current diagnostics area, but the stacked diagnostics area remains unchanged and still contains information about the condition that activated the handler:

```
+----------------------------------------------+
| op |
+----------------------------------------------+
| mapped insert succeeded, current DA is empty |
+----------------------------------------------+
+--------------------------------+-------+----------------------------+
| op | errno | msg |
+--------------------------------+-------+----------------------------+
| stacked DA after mapped insert | 1048 | Column 'c1' cannot be null |
+--------------------------------+-------+----------------------------+
```

When the condition handler ends, its current diagnostics area is popped from the stack and the stacked diagnostics area becomes the current diagnostics area in the stored procedure.

After the procedure returns, the table contains two rows. The empty row results from the attempt to insert NULL that was mapped to an empty-string insert:

```
+----------+
| c1 |
+----------+
| string 1 |
| |
+----------+
```

In the preceding example, the first two [GET DIAGNOSTICS](#page-66-0) statements within the condition handler that retrieve information from the current and stacked diagnostics areas return the same values. This is not the case if statements that reset the current diagnostics area executed earlier within the handler. Suppose that p() is rewritten to place the [DECLARE](#page-53-1) statements within the handler definition rather than preceding it:

```
CREATE PROCEDURE p ()
BEGIN
 DECLARE EXIT HANDLER FOR SQLEXCEPTION
 BEGIN
 -- Declare variables to hold diagnostics area information
 DECLARE errcount INT;
 DECLARE errno INT;
 DECLARE msg TEXT;
 GET CURRENT DIAGNOSTICS CONDITION 1
 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
 SELECT 'current DA before mapped insert' AS op, errno, msg;
 GET STACKED DIAGNOSTICS CONDITION 1
 errno = MYSQL_ERRNO, msg = MESSAGE_TEXT;
 SELECT 'stacked DA before mapped insert' AS op, errno, msg;
...
```

In this case, the result is version dependent:

• Before MySQL 5.7.2, [DECLARE](#page-53-1) does not change the current diagnostics area, so the first two [GET](#page-66-0) [DIAGNOSTICS](#page-66-0) statements return the same result, just as in the original version of p().

In MySQL 5.7.2, work was done to ensure that all nondiagnostic statements populate the diagnostics area, per the SQL standard. [DECLARE](#page-53-1) is one of them, so in 5.7.2 and higher, [DECLARE](#page-53-1) statements executing at the beginning of the handler clear the current diagnostics area and the [GET](#page-66-0) [DIAGNOSTICS](#page-66-0) statements produce different results:

```
+---------------------------------+-------+------+
| op | errno | msg |
+---------------------------------+-------+------+
| current DA before mapped insert | NULL | NULL |
+---------------------------------+-------+------+
+---------------------------------+-------+----------------------------+
```

```
| op | errno | msg |
+---------------------------------+-------+----------------------------+
| stacked DA before mapped insert | 1048 | Column 'c1' cannot be null |
+---------------------------------+-------+----------------------------+
```

To avoid this issue within a condition handler when seeking to obtain information about the condition that activated the handler, be sure to access the stacked diagnostics area, not the current diagnostics area.

## <span id="page-72-0"></span>**13.6.7.4 RESIGNAL Statement**

```
RESIGNAL [condition_value]
 [SET signal_information_item
 [, signal_information_item] ...]
condition_value: {
 SQLSTATE [VALUE] sqlstate_value
 | condition_name
}
signal_information_item:
 condition_information_item_name = simple_value_specification
condition_information_item_name: {
 CLASS_ORIGIN
 | SUBCLASS_ORIGIN
 | MESSAGE_TEXT
 | MYSQL_ERRNO
 | CONSTRAINT_CATALOG
 | CONSTRAINT_SCHEMA
 | CONSTRAINT_NAME
 | CATALOG_NAME
 | SCHEMA_NAME
 | TABLE_NAME
 | COLUMN_NAME
 | CURSOR_NAME
}
condition_name, simple_value_specification:
 (see following discussion)
```

[RESIGNAL](#page-72-0) passes on the error condition information that is available during execution of a condition handler within a compound statement inside a stored procedure or function, trigger, or event. [RESIGNAL](#page-72-0) may change some or all information before passing it on. [RESIGNAL](#page-72-0) is related to [SIGNAL](#page-76-0), but instead of originating a condition as [SIGNAL](#page-76-0) does, [RESIGNAL](#page-72-0) relays existing condition information, possibly after modifying it.

[RESIGNAL](#page-72-0) makes it possible to both handle an error and return the error information. Otherwise, by executing an SQL statement within the handler, information that caused the handler's activation is destroyed. [RESIGNAL](#page-72-0) also can make some procedures shorter if a given handler can handle part of a situation, then pass the condition "up the line" to another handler.

No privileges are required to execute the [RESIGNAL](#page-72-0) statement.

All forms of [RESIGNAL](#page-72-0) require that the current context be a condition handler. Otherwise, [RESIGNAL](#page-72-0) is illegal and a RESIGNAL when handler not active error occurs.

To retrieve information from the diagnostics area, use the [GET DIAGNOSTICS](#page-66-0) statement (see [Section 13.6.7.3, "GET DIAGNOSTICS Statement"](#page-66-0)). For information about the diagnostics area, see [Section 13.6.7.7, "The MySQL Diagnostics Area"](#page-84-0).

- [RESIGNAL Overview](#page-73-0)
- [RESIGNAL Alone](#page-73-1)
- [RESIGNAL with New Signal Information](#page-74-0)

- [RESIGNAL with a Condition Value and Optional New Signal Information](#page-75-0)
- [RESIGNAL Requires Condition Handler Context](#page-76-1)

### <span id="page-73-0"></span>**RESIGNAL Overview**

For condition\_value and signal\_information\_item, the definitions and rules are the same for [RESIGNAL](#page-72-0) as for [SIGNAL](#page-76-0). For example, the condition\_value can be an SQLSTATE value, and the value can indicate errors, warnings, or "not found." For additional information, see [Section 13.6.7.5,](#page-76-0) ["SIGNAL Statement".](#page-76-0)

The [RESIGNAL](#page-72-0) statement takes condition\_value and SET clauses, both of which are optional. This leads to several possible uses:

• [RESIGNAL](#page-72-0) alone:

RESIGNAL;

• [RESIGNAL](#page-72-0) with new signal information:

```
RESIGNAL SET signal_information_item [, signal_information_item] ...;
```

• [RESIGNAL](#page-72-0) with a condition value and possibly new signal information:

```
RESIGNAL condition_value
 [SET signal_information_item [, signal_information_item] ...];
```

These use cases all cause changes to the diagnostics and condition areas:

- A diagnostics area contains one or more condition areas.
- A condition area contains condition information items, such as the SQLSTATE value, MYSQL\_ERRNO, or MESSAGE\_TEXT.

There is a stack of diagnostics areas. When a handler takes control, it pushes a diagnostics area to the top of the stack, so there are two diagnostics areas during handler execution:

- The first (current) diagnostics area, which starts as a copy of the last diagnostics area, but is overwritten by the first statement in the handler that changes the current diagnostics area.
- The last (stacked) diagnostics area, which has the condition areas that were set up before the handler took control.

The maximum number of condition areas in a diagnostics area is determined by the value of the max\_error\_count system variable. See [Diagnostics Area-Related System Variables](#page-87-0).

### <span id="page-73-1"></span>**RESIGNAL Alone**

A simple [RESIGNAL](#page-72-0) alone means "pass on the error with no change." It restores the last diagnostics area and makes it the current diagnostics area. That is, it "pops" the diagnostics area stack.

Within a condition handler that catches a condition, one use for [RESIGNAL](#page-72-0) alone is to perform some other actions, and then pass on without change the original condition information (the information that existed before entry into the handler).

#### Example:

```
DROP TABLE IF EXISTS xx;
delimiter //
CREATE PROCEDURE p ()
BEGIN
 DECLARE EXIT HANDLER FOR SQLEXCEPTION
 BEGIN
```

```
 SET @error_count = @error_count + 1;
 IF @a = 0 THEN RESIGNAL; END IF;
 END;
 DROP TABLE xx;
END//
delimiter ;
SET @error_count = 0;
SET @a = 0;
CALL p();
```

Suppose that the DROP TABLE xx statement fails. The diagnostics area stack looks like this:

```
DA 1. ERROR 1051 (42S02): Unknown table 'xx'
```

Then execution enters the EXIT handler. It starts by pushing a diagnostics area to the top of the stack, which now looks like this:

```
DA 1. ERROR 1051 (42S02): Unknown table 'xx'
DA 2. ERROR 1051 (42S02): Unknown table 'xx'
```

At this point, the contents of the first (current) and second (stacked) diagnostics areas are the same. The first diagnostics area may be modified by statements executing subsequently within the handler.

Usually a procedure statement clears the first diagnostics area. BEGIN is an exception, it does not clear, it does nothing. SET is not an exception, it clears, performs the operation, and produces a result of "success." The diagnostics area stack now looks like this:

```
DA 1. ERROR 0000 (00000): Successful operation
DA 2. ERROR 1051 (42S02): Unknown table 'xx'
```

At this point, if @a = 0, [RESIGNAL](#page-72-0) pops the diagnostics area stack, which now looks like this:

```
DA 1. ERROR 1051 (42S02): Unknown table 'xx'
```

And that is what the caller sees.

If @a is not 0, the handler simply ends, which means that there is no more use for the current diagnostics area (it has been "handled"), so it can be thrown away, causing the stacked diagnostics area to become the current diagnostics area again. The diagnostics area stack looks like this:

```
DA 1. ERROR 0000 (00000): Successful operation
```

The details make it look complex, but the end result is quite useful: Handlers can execute without destroying information about the condition that caused activation of the handler.

### <span id="page-74-0"></span>**RESIGNAL with New Signal Information**

[RESIGNAL](#page-72-0) with a SET clause provides new signal information, so the statement means "pass on the error with changes":

```
RESIGNAL SET signal_information_item [, signal_information_item] ...;
```

As with [RESIGNAL](#page-72-0) alone, the idea is to pop the diagnostics area stack so that the original information goes out. Unlike [RESIGNAL](#page-72-0) alone, anything specified in the SET clause changes.

#### Example:

```
DROP TABLE IF EXISTS xx;
delimiter //
CREATE PROCEDURE p ()
BEGIN
 DECLARE EXIT HANDLER FOR SQLEXCEPTION
 BEGIN
 SET @error_count = @error_count + 1;
 IF @a = 0 THEN RESIGNAL SET MYSQL_ERRNO = 5; END IF;
```

```
 END;
 DROP TABLE xx;
END//
delimiter ;
SET @error_count = 0;
SET @a = 0;
CALL p();
```

Remember from the previous discussion that [RESIGNAL](#page-72-0) alone results in a diagnostics area stack like this:

```
DA 1. ERROR 1051 (42S02): Unknown table 'xx'
```

The RESIGNAL SET MYSQL\_ERRNO = 5 statement results in this stack instead, which is what the caller sees:

```
DA 1. ERROR 5 (42S02): Unknown table 'xx'
```

In other words, it changes the error number, and nothing else.

The [RESIGNAL](#page-72-0) statement can change any or all of the signal information items, making the first condition area of the diagnostics area look quite different.

### <span id="page-75-0"></span>**RESIGNAL with a Condition Value and Optional New Signal Information**

[RESIGNAL](#page-72-0) with a condition value means "push a condition into the current diagnostics area." If the SET clause is present, it also changes the error information.

```
RESIGNAL condition_value
 [SET signal_information_item [, signal_information_item] ...];
```

This form of [RESIGNAL](#page-72-0) restores the last diagnostics area and makes it the current diagnostics area. That is, it "pops" the diagnostics area stack, which is the same as what a simple [RESIGNAL](#page-72-0) alone would do. However, it also changes the diagnostics area depending on the condition value or signal information.

#### Example:

```
DROP TABLE IF EXISTS xx;
delimiter //
CREATE PROCEDURE p ()
BEGIN
 DECLARE EXIT HANDLER FOR SQLEXCEPTION
 BEGIN
 SET @error_count = @error_count + 1;
 IF @a = 0 THEN RESIGNAL SQLSTATE '45000' SET MYSQL_ERRNO=5; END IF;
 END;
 DROP TABLE xx;
END//
delimiter ;
SET @error_count = 0;
SET @a = 0;
SET @@max_error_count = 2;
CALL p();
SHOW ERRORS;
```

This is similar to the previous example, and the effects are the same, except that if [RESIGNAL](#page-72-0) happens, the current condition area looks different at the end. (The reason the condition adds to rather than replaces the existing condition is the use of a condition value.)

The [RESIGNAL](#page-72-0) statement includes a condition value (SQLSTATE '45000'), so it adds a new condition area, resulting in a diagnostics area stack that looks like this:

```
DA 1. (condition 2) ERROR 1051 (42S02): Unknown table 'xx'
 (condition 1) ERROR 5 (45000) Unknown table 'xx'
```

The result of CALL p() and [SHOW ERRORS](#page-151-0) for this example is:

```
mysql> CALL p();
ERROR 5 (45000): Unknown table 'xx'
mysql> SHOW ERRORS;
+-------+------+----------------------------------+
| Level | Code | Message |
+-------+------+----------------------------------+
| Error | 1051 | Unknown table 'xx' |
| Error | 5 | Unknown table 'xx' |
+-------+------+----------------------------------+
```

### <span id="page-76-1"></span>**RESIGNAL Requires Condition Handler Context**

All forms of [RESIGNAL](#page-72-0) require that the current context be a condition handler. Otherwise, [RESIGNAL](#page-72-0) is illegal and a RESIGNAL when handler not active error occurs. For example:

```
mysql> CREATE PROCEDURE p () RESIGNAL;
Query OK, 0 rows affected (0.00 sec)
mysql> CALL p();
ERROR 1645 (0K000): RESIGNAL when handler not active
```

Here is a more difficult example:

```
delimiter //
CREATE FUNCTION f () RETURNS INT
BEGIN
 RESIGNAL;
 RETURN 5;
END//
CREATE PROCEDURE p ()
BEGIN
 DECLARE EXIT HANDLER FOR SQLEXCEPTION SET @a=f();
 SIGNAL SQLSTATE '55555';
END//
delimiter ;
CALL p();
```

[RESIGNAL](#page-72-0) occurs within the stored function f(). Although f() itself is invoked within the context of the EXIT handler, execution within f() has its own context, which is not handler context. Thus, RESIGNAL within f() results in a "handler not active" error.

# <span id="page-76-0"></span>**13.6.7.5 SIGNAL Statement**

```
SIGNAL condition_value
 [SET signal_information_item
 [, signal_information_item] ...]
condition_value: {
 SQLSTATE [VALUE] sqlstate_value
 | condition_name
}
signal_information_item:
 condition_information_item_name = simple_value_specification
condition_information_item_name: {
 CLASS_ORIGIN
 | SUBCLASS_ORIGIN
 | MESSAGE_TEXT
 | MYSQL_ERRNO
 | CONSTRAINT_CATALOG
 | CONSTRAINT_SCHEMA
 | CONSTRAINT_NAME
 | CATALOG_NAME
 | SCHEMA_NAME
 | TABLE_NAME
 | COLUMN_NAME
```

```
 | CURSOR_NAME
}
condition_name, simple_value_specification:
 (see following discussion)
```

[SIGNAL](#page-76-0) is the way to "return" an error. [SIGNAL](#page-76-0) provides error information to a handler, to an outer portion of the application, or to the client. Also, it provides control over the error's characteristics (error number, SQLSTATE value, message). Without [SIGNAL](#page-76-0), it is necessary to resort to workarounds such as deliberately referring to a nonexistent table to cause a routine to return an error.

No privileges are required to execute the [SIGNAL](#page-76-0) statement.

To retrieve information from the diagnostics area, use the [GET DIAGNOSTICS](#page-66-0) statement (see [Section 13.6.7.3, "GET DIAGNOSTICS Statement"](#page-66-0)). For information about the diagnostics area, see [Section 13.6.7.7, "The MySQL Diagnostics Area"](#page-84-0).

- [SIGNAL Overview](#page-77-0)
- [Signal Condition Information Items](#page-79-0)
- [Effect of Signals on Handlers, Cursors, and Statements](#page-80-0)

### <span id="page-77-0"></span>**SIGNAL Overview**

The condition\_value in a [SIGNAL](#page-76-0) statement indicates the error value to be returned. It can be an SQLSTATE value (a 5-character string literal) or a condition\_name that refers to a named condition previously defined with [DECLARE ... CONDITION](#page-62-1) (see [Section 13.6.7.1, "DECLARE ... CONDITION](#page-62-1) [Statement"\)](#page-62-1).

An SQLSTATE value can indicate errors, warnings, or "not found." The first two characters of the value indicate its error class, as discussed in [Signal Condition Information Items](#page-79-0). Some signal values cause statement termination; see [Effect of Signals on Handlers, Cursors, and Statements.](#page-80-0)

The SQLSTATE value for a [SIGNAL](#page-76-0) statement should not start with '00' because such values indicate success and are not valid for signaling an error. This is true whether the SQLSTATE value is specified directly in the [SIGNAL](#page-76-0) statement or in a named condition referred to in the statement. If the value is invalid, a Bad SQLSTATE error occurs.

To signal a generic SQLSTATE value, use '45000', which means "unhandled user-defined exception."

The [SIGNAL](#page-76-0) statement optionally includes a SET clause that contains multiple signal items, in a list of condition\_information\_item\_name = simple\_value\_specification assignments, separated by commas.

Each condition\_information\_item\_name may be specified only once in the SET clause. Otherwise, a Duplicate condition information item error occurs.

Valid simple\_value\_specification designators can be specified using stored procedure or function parameters, stored program local variables declared with [DECLARE](#page-53-1), user-defined variables, system variables, or literals. A character literal may include a \_charset introducer.

For information about permissible condition\_information\_item\_name values, see [Signal](#page-79-0) [Condition Information Items](#page-79-0).

The following procedure signals an error or warning depending on the value of pval, its input parameter:

```
CREATE PROCEDURE p (pval INT)
BEGIN
 DECLARE specialty CONDITION FOR SQLSTATE '45000';
 IF pval = 0 THEN
```

```
 SIGNAL SQLSTATE '01000';
 ELSEIF pval = 1 THEN
 SIGNAL SQLSTATE '45000'
 SET MESSAGE_TEXT = 'An error occurred';
 ELSEIF pval = 2 THEN
 SIGNAL specialty
 SET MESSAGE_TEXT = 'An error occurred';
 ELSE
 SIGNAL SQLSTATE '01000'
 SET MESSAGE_TEXT = 'A warning occurred', MYSQL_ERRNO = 1000;
 SIGNAL SQLSTATE '45000'
 SET MESSAGE_TEXT = 'An error occurred', MYSQL_ERRNO = 1001;
 END IF;
END;
```

If pval is 0, p() signals a warning because SQLSTATE values that begin with '01' are signals in the warning class. The warning does not terminate the procedure, and can be seen with [SHOW WARNINGS](#page-182-0) after the procedure returns.

If pval is 1, p() signals an error and sets the MESSAGE\_TEXT condition information item. The error terminates the procedure, and the text is returned with the error information.

If pval is 2, the same error is signaled, although the SQLSTATE value is specified using a named condition in this case.

If pval is anything else, p() first signals a warning and sets the message text and error number condition information items. This warning does not terminate the procedure, so execution continues and p() then signals an error. The error does terminate the procedure. The message text and error number set by the warning are replaced by the values set by the error, which are returned with the error information.

[SIGNAL](#page-76-0) is typically used within stored programs, but it is a MySQL extension that it is permitted outside handler context. For example, if you invoke the mysql client program, you can enter any of these statements at the prompt:

```
SIGNAL SQLSTATE '77777';
CREATE TRIGGER t_bi BEFORE INSERT ON t
 FOR EACH ROW SIGNAL SQLSTATE '77777';
CREATE EVENT e ON SCHEDULE EVERY 1 SECOND
 DO SIGNAL SQLSTATE '77777';
```

[SIGNAL](#page-76-0) executes according to the following rules:

If the [SIGNAL](#page-76-0) statement indicates a particular SQLSTATE value, that value is used to signal the condition specified. Example:

```
CREATE PROCEDURE p (divisor INT)
BEGIN
 IF divisor = 0 THEN
 SIGNAL SQLSTATE '22012';
 END IF;
END;
```

If the [SIGNAL](#page-76-0) statement uses a named condition, the condition must be declared in some scope that applies to the [SIGNAL](#page-76-0) statement, and must be defined using an SQLSTATE value, not a MySQL error number. Example:

```
CREATE PROCEDURE p (divisor INT)
BEGIN
 DECLARE divide_by_zero CONDITION FOR SQLSTATE '22012';
 IF divisor = 0 THEN
 SIGNAL divide_by_zero;
 END IF;
END;
```

If the named condition does not exist in the scope of the [SIGNAL](#page-76-0) statement, an Undefined CONDITION error occurs.

If [SIGNAL](#page-76-0) refers to a named condition that is defined with a MySQL error number rather than an SQLSTATE value, a SIGNAL/RESIGNAL can only use a CONDITION defined with SQLSTATE error occurs. The following statements cause that error because the named condition is associated with a MySQL error number:

```
DECLARE no_such_table CONDITION FOR 1051;
SIGNAL no_such_table;
```

If a condition with a given name is declared multiple times in different scopes, the declaration with the most local scope applies. Consider the following procedure:

```
CREATE PROCEDURE p (divisor INT)
BEGIN
 DECLARE my_error CONDITION FOR SQLSTATE '45000';
 IF divisor = 0 THEN
 BEGIN
 DECLARE my_error CONDITION FOR SQLSTATE '22012';
 SIGNAL my_error;
 END;
 END IF;
 SIGNAL my_error;
END;
```

If divisor is 0, the first [SIGNAL](#page-76-0) statement executes. The innermost my\_error condition declaration applies, raising SQLSTATE '22012'.

If divisor is not 0, the second [SIGNAL](#page-76-0) statement executes. The outermost my\_error condition declaration applies, raising SQLSTATE '45000'.

For information about how the server chooses handlers when a condition occurs, see [Section 13.6.7.6,](#page-81-0) ["Scope Rules for Handlers".](#page-81-0)

Signals can be raised within exception handlers:

```
CREATE PROCEDURE p ()
BEGIN
 DECLARE EXIT HANDLER FOR SQLEXCEPTION
 BEGIN
 SIGNAL SQLSTATE VALUE '99999'
 SET MESSAGE_TEXT = 'An error occurred';
 END;
 DROP TABLE no_such_table;
END;
```

CALL p() reaches the DROP TABLE statement. There is no table named no\_such\_table, so the error handler is activated. The error handler destroys the original error ("no such table") and makes a new error with SQLSTATE '99999' and message An error occurred.

### <span id="page-79-0"></span>**Signal Condition Information Items**

The following table lists the names of diagnostics area condition information items that can be set in a [SIGNAL](#page-76-0) (or [RESIGNAL](#page-72-0)) statement. All items are standard SQL except MYSQL\_ERRNO, which is a MySQL extension. For more information about these items see [Section 13.6.7.7, "The MySQL](#page-84-0) [Diagnostics Area".](#page-84-0)

```
Item Name Definition
--------- ----------
CLASS_ORIGIN VARCHAR(64)
SUBCLASS_ORIGIN VARCHAR(64)
CONSTRAINT_CATALOG VARCHAR(64)
CONSTRAINT_SCHEMA VARCHAR(64)
CONSTRAINT_NAME VARCHAR(64)
CATALOG_NAME VARCHAR(64)
```

```
SCHEMA_NAME VARCHAR(64)
TABLE_NAME VARCHAR(64)
COLUMN_NAME VARCHAR(64)
CURSOR_NAME VARCHAR(64)
MESSAGE_TEXT VARCHAR(128)
MYSQL_ERRNO SMALLINT UNSIGNED
```

The character set for character items is UTF-8.

It is illegal to assign NULL to a condition information item in a [SIGNAL](#page-76-0) statement.

A [SIGNAL](#page-76-0) statement always specifies an SQLSTATE value, either directly, or indirectly by referring to a named condition defined with an SQLSTATE value. The first two characters of an SQLSTATE value are its class, and the class determines the default value for the condition information items:

• Class = '00' (success)

Illegal. SQLSTATE values that begin with '00' indicate success and are not valid for [SIGNAL](#page-76-0).

• Class = '01' (warning)

```
MESSAGE_TEXT = 'Unhandled user-defined warning condition';
MYSQL_ERRNO = ER_SIGNAL_WARN
```

• Class = '02' (not found)

```
MESSAGE_TEXT = 'Unhandled user-defined not found condition';
MYSQL_ERRNO = ER_SIGNAL_NOT_FOUND
```

• Class > '02' (exception)

```
MESSAGE_TEXT = 'Unhandled user-defined exception condition';
MYSQL_ERRNO = ER_SIGNAL_EXCEPTION
```

For legal classes, the other condition information items are set as follows:

```
CLASS_ORIGIN = SUBCLASS_ORIGIN = '';
CONSTRAINT_CATALOG = CONSTRAINT_SCHEMA = CONSTRAINT_NAME = '';
CATALOG_NAME = SCHEMA_NAME = TABLE_NAME = COLUMN_NAME = '';
CURSOR_NAME = '';
```

The error values that are accessible after [SIGNAL](#page-76-0) executes are the SQLSTATE value raised by the [SIGNAL](#page-76-0) statement and the MESSAGE\_TEXT and MYSQL\_ERRNO items. These values are available from the C API:

- [mysql\\_sqlstate\(\)](https://dev.mysql.com/doc/c-api/5.7/en/mysql-sqlstate.md) returns the SQLSTATE value.
- [mysql\\_errno\(\)](https://dev.mysql.com/doc/c-api/5.7/en/mysql-errno.md) returns the MYSQL\_ERRNO value.
- [mysql\\_error\(\)](https://dev.mysql.com/doc/c-api/5.7/en/mysql-error.md) returns the MESSAGE\_TEXT value.

At the SQL level, the output from [SHOW WARNINGS](#page-182-0) and [SHOW ERRORS](#page-151-0) indicates the MYSQL\_ERRNO and MESSAGE\_TEXT values in the Code and Message columns.

To retrieve information from the diagnostics area, use the [GET DIAGNOSTICS](#page-66-0) statement (see [Section 13.6.7.3, "GET DIAGNOSTICS Statement"](#page-66-0)). For information about the diagnostics area, see [Section 13.6.7.7, "The MySQL Diagnostics Area"](#page-84-0).

### <span id="page-80-0"></span>**Effect of Signals on Handlers, Cursors, and Statements**

Signals have different effects on statement execution depending on the signal class. The class determines how severe an error is. MySQL ignores the value of the sql\_mode system variable; in particular, strict SQL mode does not matter. MySQL also ignores IGNORE: The intent of [SIGNAL](#page-76-0) is to raise a user-generated error explicitly, so a signal is never ignored.

In the following descriptions, "unhandled" means that no handler for the signaled SQLSTATE value has been defined with [DECLARE ... HANDLER](#page-63-0).

• Class = '00' (success)

Illegal. SQLSTATE values that begin with '00' indicate success and are not valid for [SIGNAL](#page-76-0).

• Class = '01' (warning)

The value of the warning\_count system variable goes up. [SHOW WARNINGS](#page-182-0) shows the signal. SQLWARNING handlers catch the signal.

Warnings cannot be returned from stored functions because the [RETURN](#page-59-2) statement that causes the function to return clears the diagnostic area. The statement thus clears any warnings that may have been present there (and resets warning\_count to 0).

• Class = '02' (not found)

NOT FOUND handlers catch the signal. There is no effect on cursors. If the signal is unhandled in a stored function, statements end.

• Class > '02' (exception)

SQLEXCEPTION handlers catch the signal. If the signal is unhandled in a stored function, statements end.

• Class = '40'

Treated as an ordinary exception.

# <span id="page-81-0"></span>**13.6.7.6 Scope Rules for Handlers**

A stored program may include handlers to be invoked when certain conditions occur within the program. The applicability of each handler depends on its location within the program definition and on the condition or conditions that it handles:

• A handler declared in a [BEGIN ... END](#page-52-0) block is in scope only for the SQL statements following the handler declarations in the block. If the handler itself raises a condition, it cannot handle that condition, nor can any other handlers declared in the block. In the following example, handlers H1 and H2 are in scope for conditions raised by statements stmt1 and stmt2. But neither H1 nor H2 are in scope for conditions raised in the body of H1 or H2.

```
BEGIN -- outer block
 DECLARE EXIT HANDLER FOR ...; -- handler H1
 DECLARE EXIT HANDLER FOR ...; -- handler H2
 stmt1;
 stmt2;
END;
```

• A handler is in scope only for the block in which it is declared, and cannot be activated for conditions occurring outside that block. In the following example, handler H1 is in scope for stmt1 in the inner block, but not for stmt2 in the outer block:

```
BEGIN -- outer block
 BEGIN -- inner block
 DECLARE EXIT HANDLER FOR ...; -- handler H1
 stmt1;
 END;
 stmt2;
END;
```

• A handler can be specific or general. A specific handler is for a MySQL error code, SQLSTATE value, or condition name. A general handler is for a condition in the SQLWARNING, SQLEXCEPTION, or NOT FOUND class. Condition specificity is related to condition precedence, as described later.

Multiple handlers can be declared in different scopes and with different specificities. For example, there might be a specific MySQL error code handler in an outer block, and a general SQLWARNING handler in an inner block. Or there might be handlers for a specific MySQL error code and the general SQLWARNING class in the same block.

Whether a handler is activated depends not only on its own scope and condition value, but on what other handlers are present. When a condition occurs in a stored program, the server searches for applicable handlers in the current scope (current [BEGIN ... END](#page-52-0) block). If there are no applicable handlers, the search continues outward with the handlers in each successive containing scope (block). When the server finds one or more applicable handlers at a given scope, it chooses among them based on condition precedence:

- A MySQL error code handler takes precedence over an SQLSTATE value handler.
- An SQLSTATE value handler takes precedence over general SQLWARNING, SQLEXCEPTION, or NOT FOUND handlers.
- An SQLEXCEPTION handler takes precedence over an SQLWARNING handler.
- It is possible to have several applicable handlers with the same precedence. For example, a statement could generate multiple warnings with different error codes, for each of which an error-specific handler exists. In this case, the choice of which handler the server activates is nondeterministic, and may change depending on the circumstances under which the condition occurs.

One implication of the handler selection rules is that if multiple applicable handlers occur in different scopes, handlers with the most local scope take precedence over handlers in outer scopes, even over those for more specific conditions.

If there is no appropriate handler when a condition occurs, the action taken depends on the class of the condition:

- For SQLEXCEPTION conditions, the stored program terminates at the statement that raised the condition, as if there were an EXIT handler. If the program was called by another stored program, the calling program handles the condition using the handler selection rules applied to its own handlers.
- For SQLWARNING conditions, the program continues executing, as if there were a CONTINUE handler.
- For NOT FOUND conditions, if the condition was raised normally, the action is CONTINUE. If it was raised by [SIGNAL](#page-76-0) or [RESIGNAL](#page-72-0), the action is EXIT.

The following examples demonstrate how MySQL applies the handler selection rules.

This procedure contains two handlers, one for the specific SQLSTATE value ('42S02') that occurs for attempts to drop a nonexistent table, and one for the general SQLEXCEPTION class:

```
CREATE PROCEDURE p1()
BEGIN
 DECLARE CONTINUE HANDLER FOR SQLSTATE '42S02'
 SELECT 'SQLSTATE handler was activated' AS msg;
 DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
 SELECT 'SQLEXCEPTION handler was activated' AS msg;
 DROP TABLE test.t;
END;
```

Both handlers are declared in the same block and have the same scope. However, SQLSTATE handlers take precedence over SQLEXCEPTION handlers, so if the table t is nonexistent, the DROP TABLE statement raises a condition that activates the SQLSTATE handler:

```
mysql> CALL p1();
```

```
+--------------------------------+
| msg |
+--------------------------------+
| SQLSTATE handler was activated |
+--------------------------------+
```

This procedure contains the same two handlers. But this time, the DROP TABLE statement and SQLEXCEPTION handler are in an inner block relative to the SQLSTATE handler:

```
CREATE PROCEDURE p2()
BEGIN -- outer block
 DECLARE CONTINUE HANDLER FOR SQLSTATE '42S02'
 SELECT 'SQLSTATE handler was activated' AS msg;
 BEGIN -- inner block
 DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
 SELECT 'SQLEXCEPTION handler was activated' AS msg;
 DROP TABLE test.t; -- occurs within inner block
 END;
END;
```

In this case, the handler that is more local to where the condition occurs takes precedence. The SQLEXCEPTION handler activates, even though it is more general than the SQLSTATE handler:

```
mysql> CALL p2();
+------------------------------------+
| msg |
+------------------------------------+
| SQLEXCEPTION handler was activated |
+------------------------------------+
```

In this procedure, one of the handlers is declared in a block inner to the scope of the DROP TABLE statement:

```
CREATE PROCEDURE p3()
BEGIN -- outer block
 DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
 SELECT 'SQLEXCEPTION handler was activated' AS msg;
 BEGIN -- inner block
 DECLARE CONTINUE HANDLER FOR SQLSTATE '42S02'
 SELECT 'SQLSTATE handler was activated' AS msg;
 END;
 DROP TABLE test.t; -- occurs within outer block
END;
```

Only the SQLEXCEPTION handler applies because the other one is not in scope for the condition raised by the DROP TABLE:

```
mysql> CALL p3();
+------------------------------------+
| msg |
+------------------------------------+
| SQLEXCEPTION handler was activated |
+------------------------------------+
```

In this procedure, both handlers are declared in a block inner to the scope of the DROP TABLE statement:

```
CREATE PROCEDURE p4()
BEGIN -- outer block
 BEGIN -- inner block
 DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
 SELECT 'SQLEXCEPTION handler was activated' AS msg;
 DECLARE CONTINUE HANDLER FOR SQLSTATE '42S02'
 SELECT 'SQLSTATE handler was activated' AS msg;
 END;
 DROP TABLE test.t; -- occurs within outer block
```

```
END;
```

Neither handler applies because they are not in scope for the DROP TABLE. The condition raised by the statement goes unhandled and terminates the procedure with an error:

```
mysql> CALL p4();
ERROR 1051 (42S02): Unknown table 'test.t'
```

# <span id="page-84-0"></span>**13.6.7.7 The MySQL Diagnostics Area**

SQL statements produce diagnostic information that populates the diagnostics area. Standard SQL has a diagnostics area stack, containing a diagnostics area for each nested execution context. Standard SQL also supports [GET STACKED DIAGNOSTICS](#page-66-0) syntax for referring to the second diagnostics area during condition handler execution. MySQL supports the STACKED keyword as of MySQL 5.7. Before that, MySQL does not support STACKED; there is a single diagnostics area containing information from the most recent statement that wrote to it.

The following discussion describes the structure of the diagnostics area in MySQL, the information items recognized by MySQL, how statements clear and set the diagnostics area, and how diagnostics areas are pushed to and popped from the stack.

- [Diagnostics Area Structure](#page-84-2)
- [Diagnostics Area Information Items](#page-84-1)
- [How the Diagnostics Area is Cleared and Populated](#page-85-0)
- [How the Diagnostics Area Stack Works](#page-87-1)
- [Diagnostics Area-Related System Variables](#page-87-0)

### <span id="page-84-2"></span>**Diagnostics Area Structure**

The diagnostics area contains two kinds of information:

- Statement information, such as the number of conditions that occurred or the affected-rows count.
- Condition information, such as the error code and message. If a statement raises multiple conditions, this part of the diagnostics area has a condition area for each one. If a statement raises no conditions, this part of the diagnostics area is empty.

For a statement that produces three conditions, the diagnostics area contains statement and condition information like this:

```
Statement information:
 row count
 ... other statement information items ...
Condition area list:
 Condition area 1:
 error code for condition 1
 error message for condition 1
 ... other condition information items ...
 Condition area 2:
 error code for condition 2:
 error message for condition 2
 ... other condition information items ...
 Condition area 3:
 error code for condition 3
 error message for condition 3
 ... other condition information items ...
```

### <span id="page-84-1"></span>**Diagnostics Area Information Items**

The diagnostics area contains statement and condition information items. Numeric items are integers. The character set for character items is UTF-8. No item can be NULL. If a statement or condition item is not set by a statement that populates the diagnostics area, its value is 0 or the empty string, depending on the item data type.

The statement information part of the diagnostics area contains these items:

- NUMBER: An integer indicating the number of condition areas that have information.
- ROW\_COUNT: An integer indicating the number of rows affected by the statement. ROW\_COUNT has the same value as the ROW\_COUNT() function (see Section 12.15, "Information Functions").

The condition information part of the diagnostics area contains a condition area for each condition. Condition areas are numbered from 1 to the value of the NUMBER statement condition item. If NUMBER is 0, there are no condition areas.

Each condition area contains the items in the following list. All items are standard SQL except MYSQL\_ERRNO, which is a MySQL extension. The definitions apply for conditions generated other than by a signal (that is, by a [SIGNAL](#page-76-0) or [RESIGNAL](#page-72-0) statement). For nonsignal conditions, MySQL populates only those condition items not described as always empty. The effects of signals on the condition area are described later.

- CLASS\_ORIGIN: A string containing the class of the RETURNED\_SQLSTATE value. If the RETURNED\_SQLSTATE value begins with a class value defined in SQL standards document ISO 9075-2 (section 24.1, SQLSTATE), CLASS\_ORIGIN is 'ISO 9075'. Otherwise, CLASS\_ORIGIN is 'MySQL'.
- SUBCLASS\_ORIGIN: A string containing the subclass of the RETURNED\_SQLSTATE value. If CLASS\_ORIGIN is 'ISO 9075' or RETURNED\_SQLSTATE ends with '000', SUBCLASS\_ORIGIN is 'ISO 9075'. Otherwise, SUBCLASS\_ORIGIN is 'MySQL'.
- RETURNED\_SQLSTATE: A string that indicates the SQLSTATE value for the condition.
- MESSAGE\_TEXT: A string that indicates the error message for the condition.
- MYSQL\_ERRNO: An integer that indicates the MySQL error code for the condition.
- CONSTRAINT\_CATALOG, CONSTRAINT\_SCHEMA, CONSTRAINT\_NAME: Strings that indicate the catalog, schema, and name for a violated constraint. They are always empty.
- CATALOG\_NAME, SCHEMA\_NAME, TABLE\_NAME, COLUMN\_NAME: Strings that indicate the catalog, schema, table, and column related to the condition. They are always empty.
- CURSOR\_NAME: A string that indicates the cursor name. This is always empty.

For the RETURNED\_SQLSTATE, MESSAGE\_TEXT, and MYSQL\_ERRNO values for particular errors, see [Server Error Message Reference.](https://dev.mysql.com/doc/mysql-errors/5.7/en/server-error-reference.md)

If a [SIGNAL](#page-76-0) (or [RESIGNAL](#page-72-0)) statement populates the diagnostics area, its SET clause can assign to any condition information item except RETURNED\_SQLSTATE any value that is legal for the item data type. [SIGNAL](#page-76-0) also sets the RETURNED\_SQLSTATE value, but not directly in its SET clause. That value comes from the [SIGNAL](#page-76-0) statement SQLSTATE argument.

[SIGNAL](#page-76-0) also sets statement information items. It sets NUMBER to 1. It sets ROW\_COUNT to −1 for errors and 0 otherwise.

### <span id="page-85-0"></span>**How the Diagnostics Area is Cleared and Populated**

Nondiagnostic SQL statements populate the diagnostics area automatically, and its contents can be set explicitly with the [SIGNAL](#page-76-0) and [RESIGNAL](#page-72-0) statements. The diagnostics area can be examined with [GET](#page-66-0) [DIAGNOSTICS](#page-66-0) to extract specific items, or with [SHOW WARNINGS](#page-182-0) or [SHOW ERRORS](#page-151-0) to see conditions or errors.

SQL statements clear and set the diagnostics area as follows:

- When the server starts executing a statement after parsing it, it clears the diagnostics area for nondiagnostic statements. Diagnostic statements do not clear the diagnostics area. These statements are diagnostic:
  - [GET DIAGNOSTICS](#page-66-0)
  - [SHOW ERRORS](#page-151-0)
  - [SHOW WARNINGS](#page-182-0)
- If a statement raises a condition, the diagnostics area is cleared of conditions that belong to earlier statements. The exception is that conditions raised by [GET DIAGNOSTICS](#page-66-0) and [RESIGNAL](#page-72-0) are added to the diagnostics area without clearing it.

Thus, even a statement that does not normally clear the diagnostics area when it begins executing clears it if the statement raises a condition.

The following example shows the effect of various statements on the diagnostics area, using [SHOW](#page-182-0) [WARNINGS](#page-182-0) to display information about conditions stored there.

This DROP TABLE statement clears the diagnostics area and populates it when the condition occurs:

```
mysql> DROP TABLE IF EXISTS test.no_such_table;
Query OK, 0 rows affected, 1 warning (0.01 sec)
mysql> SHOW WARNINGS;
+-------+------+------------------------------------+
| Level | Code | Message |
+-------+------+------------------------------------+
| Note | 1051 | Unknown table 'test.no_such_table' |
+-------+------+------------------------------------+
1 row in set (0.00 sec)
```

This [SET](#page-130-0) statement generates an error, so it clears and populates the diagnostics area:

```
mysql> SET @x = @@x;
ERROR 1193 (HY000): Unknown system variable 'x'
mysql> SHOW WARNINGS;
+-------+------+-----------------------------+
| Level | Code | Message |
+-------+------+-----------------------------+
| Error | 1193 | Unknown system variable 'x' |
+-------+------+-----------------------------+
1 row in set (0.00 sec)
```

The previous [SET](#page-130-0) statement produced a single condition, so 1 is the only valid condition number for [GET DIAGNOSTICS](#page-66-0) at this point. The following statement uses a condition number of 2, which produces a warning that is added to the diagnostics area without clearing it:

```
mysql> GET DIAGNOSTICS CONDITION 2 @p = MESSAGE_TEXT;
Query OK, 0 rows affected, 1 warning (0.00 sec)
mysql> SHOW WARNINGS;
+-------+------+------------------------------+
| Level | Code | Message |
+-------+------+------------------------------+
| Error | 1193 | Unknown system variable 'xx' |
| Error | 1753 | Invalid condition number |
+-------+------+------------------------------+
2 rows in set (0.00 sec)
```

Now there are two conditions in the diagnostics area, so the same [GET DIAGNOSTICS](#page-66-0) statement succeeds:

```
mysql> GET DIAGNOSTICS CONDITION 2 @p = MESSAGE_TEXT;
Query OK, 0 rows affected (0.00 sec)
```

```
mysql> SELECT @p;
+--------------------------+
| @p |
+--------------------------+
| Invalid condition number |
+--------------------------+
1 row in set (0.01 sec)
```

## <span id="page-87-1"></span>**How the Diagnostics Area Stack Works**

When a push to the diagnostics area stack occurs, the first (current) diagnostics area becomes the second (stacked) diagnostics area and a new current diagnostics area is created as a copy of it. Diagnostics areas are pushed to and popped from the stack under the following circumstances:

• Execution of a stored program

A push occurs before the program executes and a pop occurs afterward. If the stored program ends while handlers are executing, there can be more than one diagnostics area to pop; this occurs due to an exception for which there are no appropriate handlers or due to [RETURN](#page-59-2) in the handler.

Any warning or error conditions in the popped diagnostics areas then are added to the current diagnostics area, except that, for triggers, only errors are added. When the stored program ends, the caller sees these conditions in its current diagonstics area.

• Execution of a condition handler within a stored program

When a push occurs as a result of condition handler activation, the stacked diagnostics area is the area that was current within the stored program prior to the push. The new now-current diagnostics area is the handler's current diagnostics area. [GET \[CURRENT\] DIAGNOSTICS](#page-66-0) and [GET STACKED](#page-66-0) [DIAGNOSTICS](#page-66-0) can be used within the handler to access the contents of the current (handler) and stacked (stored program) diagnostics areas. Initially, they return the same result, but statements executing within the handler modify the current diagnostics area, clearing and setting its contents according to the normal rules (see [How the Diagnostics Area is Cleared and Populated](#page-85-0)). The stacked diagnostics area cannot be modified by statements executing within the handler except [RESIGNAL](#page-72-0).

If the handler executes successfully, the current (handler) diagnostics area is popped and the stacked (stored program) diagnostics area again becomes the current diagnostics area. Conditions added to the handler diagnostics area during handler execution are added to the current diagnostics area.

• Execution of [RESIGNAL](#page-72-0)

The [RESIGNAL](#page-72-0) statement passes on the error condition information that is available during execution of a condition handler within a compound statement inside a stored program. [RESIGNAL](#page-72-0) may change some or all information before passing it on, modifying the diagnostics stack as described in [Section 13.6.7.4, "RESIGNAL Statement"](#page-72-0).

### <span id="page-87-0"></span>**Diagnostics Area-Related System Variables**

Certain system variables control or are related to some aspects of the diagnostics area:

- max\_error\_count controls the number of condition areas in the diagnostics area. If more conditions than this occur, MySQL silently discards information for the excess conditions. (Conditions added by [RESIGNAL](#page-72-0) are always added, with older conditions being discarded as necessary to make room.)
- warning\_count indicates the number of conditions that occurred. This includes errors, warnings, and notes. Normally, NUMBER and warning\_count are the same. However, as the number of conditions generated exceeds max\_error\_count, the value of warning\_count continues to rise whereas NUMBER remains capped at max\_error\_count because no additional conditions are stored in the diagnostics area.

- error\_count indicates the number of errors that occurred. This value includes "not found" and exception conditions, but excludes warnings and notes. Like warning\_count, its value can exceed max\_error\_count.
- If the sql\_notes system variable is set to 0, notes are not stored and do not increment warning\_count.

Example: If max\_error\_count is 10, the diagnostics area can contain a maximum of 10 condition areas. Suppose that a statement raises 20 conditions, 12 of which are errors. In that case, the diagnostics area contains the first 10 conditions, NUMBER is 10, warning\_count is 20, and error\_count is 12.

Changes to the value of max\_error\_count have no effect until the next attempt to modify the diagnostics area. If the diagnostics area contains 10 condition areas and max\_error\_count is set to 5, that has no immediate effect on the size or content of the diagnostics area.