# Oracle 11g - queries009
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/queries009.htm

[Go to main content](#BEGIN)

347/522 

# Selecting from the DUAL Table

`DUAL` is a table automatically created by Oracle Database along with the data dictionary. `DUAL` is in the schema of the user `SYS` but is accessible by the name `DUAL` to all users. It has one column, `DUMMY`, defined to be `VARCHAR2(1)`, and contains one row with a value `X`. Selecting from the `DUAL` table is useful for computing a constant expression with the `SELECT` statement. Because `DUAL` has only one row, the constant is returned only once. Alternatively, you can select a constant, pseudocolumn, or expression from any table, but the value will be returned as many times as there are rows in the table. Refer to ["About SQL Functions"](functions001.md#CJAHCIID) for many examples of selecting a constant value from `DUAL`.

Note:

Beginning with Oracle Database 10

g

Release 1, logical I/O is not performed on the

`DUAL`

table when computing an expression that does not include the

`DUMMY`

column. This optimization is listed as

`FAST` `DUAL`

in the execution plan. If you

`SELECT`

the

`DUMMY`

column from

`DUAL`

, then this optimization does not take place and logical I/O occurs.

Scripting on this page enhances content navigation, but does not change the content in any way.