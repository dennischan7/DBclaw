# Oracle 12c - functions133
Source: https://docs.oracle.com/database/121/SQLRF/functions133.htm

[Go to main content](#BEGIN)

206/555 

# ORA\_DST\_AFFECTED

Syntax

Purpose

`ORA_DST_AFFECTED` is useful when you are changing the time zone data file for your database. The function takes as an argument a datetime expression that resolves to a `TIMESTAMP` `WITH` `TIME` `ZONE` value or a `VARRAY` object that contains `TIMESTAMP` `WITH` `TIME` `ZONE` values. The function returns `1` if the datetime value is affected by or will result in a "nonexisting time" or "duplicate time" error with the new time zone data. Otherwise, it returns 0.

This function can be issued only when changing the time zone data file of the database and upgrading the timestamp with the time zone data, and only between the execution of the `DBMS_DST`.`BEGIN_PREPARE` and the `DBMS_DST`.`END_PREPARE` procedures or between the execution of the `DBMS_DST`.`BEGIN_UPGRADE` and the `DBMS_DST`.`END_UPGRADE` procedures.

Scripting on this page enhances content navigation, but does not change the content in any way.