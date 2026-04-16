---
source: PostgreSQL 15 Reference
title: 00_Overview
---

Event trigger functions can be written in PL/Tcl. PostgreSQL requires that a function that is to be called as an event trigger must be declared as a function with no arguments and a return type of event\_trigger.

The information from the trigger manager is passed to the function body in the following variables:

```
$TG_event
```

The name of the event the trigger is fired for.

```
$TG_tag
```

The command tag for which the trigger is fired.

The return value of the trigger function is ignored.

Here's a little example event trigger function that simply raises a NOTICE message each time a supported command is executed:

```
CREATE OR REPLACE FUNCTION tclsnitch() RETURNS event_trigger AS $$
 elog NOTICE "tclsnitch: $TG_event $TG_tag"
$$ LANGUAGE pltcl;
CREATE EVENT TRIGGER tcl_a_snitch ON ddl_command_start EXECUTE
 FUNCTION tclsnitch();
```

# <span id="page-185-0"></span>**44.8. Error Handling in PL/Tcl**

Tcl code within or called from a PL/Tcl function can raise an error, either by executing some invalid operation or by generating an error using the Tcl error command or PL/Tcl's elog command. Such errors can be caught within Tcl using the Tcl catch command. If an error is not caught but is allowed to propagate out to the top level of execution of the PL/Tcl function, it is reported as an SQL error in the function's calling query.

Conversely, SQL errors that occur within PL/Tcl's spi\_exec, spi\_prepare, and spi\_execp commands are reported as Tcl errors, so they are catchable by Tcl's catch command. (Each of these PL/Tcl commands runs its SQL operation in a subtransaction, which is rolled back on error, so that any partially-completed operation is automatically cleaned up.) Again, if an error propagates out to the top level without being caught, it turns back into an SQL error.

Tcl provides an errorCode variable that can represent additional information about an error in a form that is easy for Tcl programs to interpret. The contents are in Tcl list format, and the first word identifies the subsystem or library reporting the error; beyond that the contents are left to the individual subsystem or library. For database errors reported by PL/Tcl commands, the first word is POSTGRES, the second word is the PostgreSQL version number, and additional words are field name/value pairs providing detailed information about the error. Fields SQLSTATE, condition, and message are always supplied (the first two represent the error code and condition name as shown in Appendix A). Fields that may be present include detail, hint, context, schema, table, column, datatype, constraint, statement, cursor\_position, filename, lineno, and funcname.

A convenient way to work with PL/Tcl's errorCode information is to load it into an array, so that the field names become array subscripts. Code for doing that might look like

```
if {[catch { spi_exec $sql_command }]} {
 if {[lindex $::errorCode 0] == "POSTGRES"} {
 array set errorArray $::errorCode
 if {$errorArray(condition) == "undefined_table"} {
 # deal with missing table
 } else {
 # deal with some other type of SQL error
 }
 }
}
```

(The double colons explicitly specify that errorCode is a global variable.)

# <span id="page-186-0"></span>**44.9. Explicit Subtransactions in PL/Tcl**

Recovering from errors caused by database access as described in [Section 44.8](#page-185-0) can lead to an undesirable situation where some operations succeed before one of them fails, and after recovering from that error the data is left in an inconsistent state. PL/Tcl offers a solution to this problem in the form of explicit subtransactions.

Consider a function that implements a transfer between two accounts:

```
CREATE FUNCTION transfer_funds() RETURNS void AS $$
 if [catch {
 spi_exec "UPDATE accounts SET balance = balance - 100 WHERE
 account_name = 'joe'"
 spi_exec "UPDATE accounts SET balance = balance + 100 WHERE
 account_name = 'mary'"
 } errormsg] {
 set result [format "error transferring funds: %s"
 $errormsg]
```

```
 } else {
 set result "funds transferred successfully"
 }
 spi_exec "INSERT INTO operations (result) VALUES ('[quote
 $result]')"
$$ LANGUAGE pltcl;
```

If the second UPDATE statement results in an exception being raised, this function will log the failure, but the result of the first UPDATE will nevertheless be committed. In other words, the funds will be withdrawn from Joe's account, but will not be transferred to Mary's account. This happens because each spi\_exec is a separate subtransaction, and only one of those subtransactions got rolled back.

To handle such cases, you can wrap multiple database operations in an explicit subtransaction, which will succeed or roll back as a whole. PL/Tcl provides a subtransaction command to manage this. We can rewrite our function as:

```
CREATE FUNCTION transfer_funds2() RETURNS void AS $$
 if [catch {
 subtransaction {
 spi_exec "UPDATE accounts SET balance = balance - 100
 WHERE account_name = 'joe'"
 spi_exec "UPDATE accounts SET balance = balance + 100
 WHERE account_name = 'mary'"
 }
 } errormsg] {
 set result [format "error transferring funds: %s"
 $errormsg]
 } else {
 set result "funds transferred successfully"
 }
 spi_exec "INSERT INTO operations (result) VALUES ('[quote
 $result]')"
$$ LANGUAGE pltcl;
```

Note that use of catch is still required for this purpose. Otherwise the error would propagate to the top level of the function, preventing the desired insertion into the operations table. The subtransaction command does not trap errors, it only assures that all database operations executed inside its scope will be rolled back together when an error is reported.

A rollback of an explicit subtransaction occurs on any error reported by the contained Tcl code, not only errors originating from database access. Thus a regular Tcl exception raised inside a subtransaction command will also cause the subtransaction to be rolled back. However, non-error exits out of the contained Tcl code (for instance, due to return) do not cause a rollback.