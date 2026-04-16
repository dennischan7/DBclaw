# Oracle 12c - functions266
Source: https://docs.oracle.com/database/121/SQLRF/functions266.htm

[Go to main content](#BEGIN)

339/555 

# XMLROOT

Syntax

Purpose

`XMLROOT` lets you create a new XML value by providing version and standalone properties in the XML root information (prolog) of an existing XML value. If the `value_expr` already has a prolog, then the database returns an error. If the input is null, then the function returns null.

The value returned takes the following form:

```
<?xml version = "version" [ STANDALONE = "{yes | no}" ]?>
```

* The first `value_expr` specifies the XML value for which you are providing prolog information.
* In the `VERSION` clause, `value_expr` must resolve to a string representing a valid XML version. If you specify `NO` `VALUE` for `VERSION`, then the version defaults to 1.0.
* If you omit the optional `STANDALONE` clause, or if you specify it with `NO` `VALUE`, then the standalone property is absent from the value returned by the function.

Examples

The following statement uses the `DUAL` table to illustrate the syntax of `XMLROOT`:

```
SELECT XMLROOT ( XMLType('<poid>143598</poid>'), VERSION '1.0', STANDALONE YES)
   AS "XMLROOT" FROM DUAL;

XMLROOT
--------------------------------------------------------------------------------
<?xml version="1.0" standalone="yes"?>
<poid>143598</poid>
```

Scripting on this page enhances content navigation, but does not change the content in any way.