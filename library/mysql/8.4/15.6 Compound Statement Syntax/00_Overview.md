---
source: MySQL 8.4 Reference
title: 00_Overview
---

This section describes the syntax for the [BEGIN ... END](#page-177-0) compound statement and other statements that can be used in the body of stored programs: Stored procedures and functions, triggers, and events. These objects are defined in terms of SQL code that is stored on the server for later invocation (see Chapter 27, Stored Objects).

A compound statement is a block that can contain other blocks; declarations for variables, condition handlers, and cursors; and flow control constructs such as loops and conditional tests.

# <span id="page-177-0"></span>**15.6.1 BEGIN ... END Compound Statement**

```
[begin_label:] BEGIN
 [statement_list]
END [end_label]
```

[BEGIN ... END](#page-177-0) syntax is used for writing compound statements, which can appear within stored programs (stored procedures and functions, triggers, and events). A compound statement can contain multiple statements, enclosed by the BEGIN and END keywords. statement\_list represents a list of one or more statements, each terminated by a semicolon (;) statement delimiter. The statement\_list itself is optional, so the empty compound statement (BEGIN END) is legal.

```
BEGIN ... END blocks can be nested.
```

Use of multiple statements requires that a client is able to send statement strings containing the ; statement delimiter. In the mysql command-line client, this is handled with the delimiter command. Changing the ; end-of-statement delimiter (for example, to //) permit ; to be used in a program body. For an example, see Section 27.1, "Defining Stored Programs".

A [BEGIN ... END](#page-177-0) block can be labeled. See [Section 15.6.2, "Statement Labels"](#page-177-1).

The optional [NOT] ATOMIC clause is not supported. This means that no transactional savepoint is set at the start of the instruction block and the BEGIN clause used in this context has no effect on the current transaction.

![](_page_177_Picture_13.jpeg)

#### **Note**

Within all stored programs, the parser treats [BEGIN \[WORK\]](#page-125-1) as the beginning of a [BEGIN ... END](#page-177-0) block. To begin a transaction in this context, use [START](#page-125-1) [TRANSACTION](#page-125-1) instead.

# <span id="page-177-1"></span>**15.6.2 Statement Labels**

```
[begin_label:] BEGIN
 [statement_list]
END [end_label]
[begin_label:] LOOP
 statement_list
END LOOP [end_label]
[begin_label:] REPEAT
 statement_list
UNTIL search_condition
END REPEAT [end_label]
[begin_label:] WHILE search_condition DO
 statement_list
END WHILE [end_label]
```

Labels are permitted for [BEGIN ... END](#page-177-0) blocks and for the [LOOP](#page-182-0), [REPEAT](#page-183-0), and [WHILE](#page-183-1) statements. Label use for those statements follows these rules:

- begin\_label must be followed by a colon.
- begin\_label can be given without end\_label. If end\_label is present, it must be the same as begin\_label.
- end\_label cannot be given without begin\_label.
- Labels at the same nesting level must be distinct.
- Labels can be up to 16 characters long.

To refer to a label within the labeled construct, use an [ITERATE](#page-182-1) or [LEAVE](#page-182-2) statement. The following example uses those statements to continue iterating or terminate the loop:

```
CREATE PROCEDURE doiterate(p1 INT)
BEGIN
 label1: LOOP
 SET p1 = p1 + 1;
 IF p1 < 10 THEN ITERATE label1; END IF;
 LEAVE label1;
 END LOOP label1;
END;
```

The scope of a block label does not include the code for handlers declared within the block. For details, see [Section 15.6.7.2, "DECLARE ... HANDLER Statement".](#page-187-0)

# <span id="page-178-0"></span>**15.6.3 DECLARE Statement**

The [DECLARE](#page-178-0) statement is used to define various items local to a program:

- Local variables. See [Section 15.6.4, "Variables in Stored Programs".](#page-178-1)
- Conditions and handlers. See [Section 15.6.7, "Condition Handling".](#page-186-0)
- Cursors. See [Section 15.6.6, "Cursors"](#page-184-0).

[DECLARE](#page-178-0) is permitted only inside a [BEGIN ... END](#page-177-0) compound statement and must be at its start, before any other statements.

Declarations must follow a certain order. Cursor declarations must appear before handler declarations. Variable and condition declarations must appear before cursor or handler declarations.

# <span id="page-178-1"></span>**15.6.4 Variables in Stored Programs**

System variables and user-defined variables can be used in stored programs, just as they can be used outside stored-program context. In addition, stored programs can use DECLARE to define local variables, and stored routines (procedures and functions) can be declared to take parameters that communicate values between the routine and its caller.

- To declare local variables, use the [DECLARE](#page-179-1) statement, as described in [Section 15.6.4.1, "Local](#page-179-1) [Variable DECLARE Statement"](#page-179-1).
- Variables can be set directly with the SET statement. See Section 15.7.6.1, "SET Syntax for Variable Assignment".
- Results from queries can be retrieved into local variables using [SELECT ... INTO](#page-76-0) var\_list or by opening a cursor and using [FETCH ... INTO](#page-185-0) var\_list. See [Section 15.2.13.1, "SELECT ...](#page-76-0) [INTO Statement",](#page-76-0) and [Section 15.6.6, "Cursors".](#page-184-0)

For information about the scope of local variables and how MySQL resolves ambiguous names, see [Section 15.6.4.2, "Local Variable Scope and Resolution"](#page-179-0).

It is not permitted to assign the value DEFAULT to stored procedure or function parameters or stored program local variables (for example with a SET var\_name = DEFAULT statement). In MySQL 8.4, this results in a syntax error.

## <span id="page-179-1"></span>**15.6.4.1 Local Variable DECLARE Statement**

```
DECLARE var_name [, var_name] ... type [DEFAULT value]
```

This statement declares local variables within stored programs. To provide a default value for a variable, include a DEFAULT clause. The value can be specified as an expression; it need not be a constant. If the DEFAULT clause is missing, the initial value is NULL.

Local variables are treated like stored routine parameters with respect to data type and overflow checking. See Section 15.1.17, "CREATE PROCEDURE and CREATE FUNCTION Statements".

Variable declarations must appear before cursor or handler declarations.

Local variable names are not case-sensitive. Permissible characters and quoting rules are the same as for other identifiers, as described in Section 11.2, "Schema Object Names".

The scope of a local variable is the [BEGIN ... END](#page-177-0) block within which it is declared. The variable can be referred to in blocks nested within the declaring block, except those blocks that declare a variable with the same name.

For examples of variable declarations, see [Section 15.6.4.2, "Local Variable Scope and Resolution"](#page-179-0).

## <span id="page-179-0"></span>**15.6.4.2 Local Variable Scope and Resolution**

The scope of a local variable is the [BEGIN ... END](#page-177-0) block within which it is declared. The variable can be referred to in blocks nested within the declaring block, except those blocks that declare a variable with the same name.

Because local variables are in scope only during stored program execution, references to them are not permitted in prepared statements created within a stored program. Prepared statement scope is the current session, not the stored program, so the statement could be executed after the program ends, at which point the variables would no longer be in scope. For example, SELECT ... INTO local\_var cannot be used as a prepared statement. This restriction also applies to stored procedure and function parameters. See [Section 15.5.1, "PREPARE Statement"](#page-174-0).

A local variable should not have the same name as a table column. If an SQL statement, such as a [SELECT ... INTO](#page-70-0) statement, contains a reference to a column and a declared local variable with the same name, MySQL currently interprets the reference as the name of a variable. Consider the following procedure definition:

```
CREATE PROCEDURE sp1 (x VARCHAR(5))
BEGIN
 DECLARE xname VARCHAR(5) DEFAULT 'bob';
 DECLARE newname VARCHAR(5);
 DECLARE xid INT;
 SELECT xname, id INTO newname, xid
 FROM table1 WHERE xname = xname;
 SELECT newname;
END;
```

MySQL interprets xname in the [SELECT](#page-70-0) statement as a reference to the xname variable rather than the xname column. Consequently, when the procedure sp1()is called, the newname variable returns the value 'bob' regardless of the value of the table1.xname column.

Similarly, the cursor definition in the following procedure contains a [SELECT](#page-70-0) statement that refers to xname. MySQL interprets this as a reference to the variable of that name rather than a column reference.

```
CREATE PROCEDURE sp2 (x VARCHAR(5))
```

```
BEGIN
 DECLARE xname VARCHAR(5) DEFAULT 'bob';
 DECLARE newname VARCHAR(5);
 DECLARE xid INT;
 DECLARE done TINYINT DEFAULT 0;
 DECLARE cur1 CURSOR FOR SELECT xname, id FROM table1;
 DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
 OPEN cur1;
 read_loop: LOOP
 FETCH FROM cur1 INTO newname, xid;
 IF done THEN LEAVE read_loop; END IF;
 SELECT newname;
 END LOOP;
 CLOSE cur1;
END;
```

See also Section 27.8, "Restrictions on Stored Programs".