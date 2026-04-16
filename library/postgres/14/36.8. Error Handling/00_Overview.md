---
source: PostgreSQL 14 Reference
title: 00_Overview
---

This section describes how you can handle exceptional conditions and warnings in an embedded SQL program. There are two nonexclusive facilities for this.

- Callbacks can be configured to handle warning and error conditions using the WHENEVER command.
- Detailed information about the error or warning can be obtained from the sqlca variable.

## <span id="page-36-0"></span>**36.8.1. Setting Callbacks**

One simple method to catch errors and warnings is to set a specific action to be executed whenever a particular condition occurs. In general:

```
EXEC SQL WHENEVER condition action;
condition can be one of the following:
SQLERROR
```

The specified action is called whenever an error occurs during the execution of an SQL statement.

```
SQLWARNING
```

The specified action is called whenever a warning occurs during the execution of an SQL statement.

```
NOT FOUND
```

The specified action is called whenever an SQL statement retrieves or affects zero rows. (This condition is not an error, but you might be interested in handling it specially.)

action can be one of the following:

```
CONTINUE
```

This effectively means that the condition is ignored. This is the default.

```
GOTO label
GO TO label
```

Jump to the specified label (using a C goto statement).

```
SQLPRINT
```

Print a message to standard error. This is useful for simple programs or during prototyping. The details of the message cannot be configured.

STOP

Call exit(1), which will terminate the program.

DO BREAK

Execute the C statement break. This should only be used in loops or switch statements.

```
DO CONTINUE
```

Execute the C statement continue. This should only be used in loops statements. if executed, will cause the flow of control to return to the top of the loop.

```
CALL name (args)
DO name (args)
```

Call the specified C functions with the specified arguments. (This use is different from the meaning of CALL and DO in the normal PostgreSQL grammar.)

The SQL standard only provides for the actions CONTINUE and GOTO (and GO TO).

Here is an example that you might want to use in a simple program. It prints a simple message when a warning occurs and aborts the program when an error happens:

```
EXEC SQL WHENEVER SQLWARNING SQLPRINT;
EXEC SQL WHENEVER SQLERROR STOP;
```

The statement EXEC SQL WHENEVER is a directive of the SQL preprocessor, not a C statement. The error or warning actions that it sets apply to all embedded SQL statements that appear below the point where the handler is set, unless a different action was set for the same condition between the first EXEC SQL WHENEVER and the SQL statement causing the condition, regardless of the flow of control in the C program. So neither of the two following C program excerpts will have the desired effect:

```
/*
 * WRONG
 */
int main(int argc, char *argv[])
{
 ...
 if (verbose) {
 EXEC SQL WHENEVER SQLWARNING SQLPRINT;
 }
 ...
 EXEC SQL SELECT ...;
 ...
}
/*
 * WRONG
 */
int main(int argc, char *argv[])
{
 ...
 set_error_handler();
 ...
 EXEC SQL SELECT ...;
```

```
 ...
}
static void set_error_handler(void)
{
 EXEC SQL WHENEVER SQLERROR STOP;
}
```