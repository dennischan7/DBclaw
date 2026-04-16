# Oracle 11g - functions227
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/functions227.htm

[Go to main content](#BEGIN)

267/522 

# USER

Syntax

Purpose

`USER` returns the name of the session user (the user who logged on) with the data type `VARCHAR2`. Oracle Database compares values of this function with blank-padded comparison semantics.

In a distributed SQL statement, the `UID` and `USER` functions together identify the user on your local database. You cannot use these functions in the condition of a `CHECK` constraint.

Examples

The following example returns the current user and the user's UID:

```
SELECT USER, UID FROM DUAL;
```

Scripting on this page enhances content navigation, but does not change the content in any way.