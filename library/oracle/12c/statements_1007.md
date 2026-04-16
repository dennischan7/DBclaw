# Oracle 12c - statements_1007
Source: https://docs.oracle.com/database/121/SQLRF/statements_1007.htm

[Go to main content](#BEGIN)

374/555 

# ALTER DATABASE LINK

Purpose

Use the `ALTER` `DATABASE` `LINK` statement to modify a fixed-user database link when the password of the connection or authentication user changes.

Notes:

* You cannot use this statement to change the connection or authentication user associated with the database link. To change `user`, you must re-create the database link.
* You cannot use this statement to change the password of a connection or authentication user. You must use the [ALTER USER](statements_4003.md#i2058207) statement for this purpose, and then alter the database link with the `ALTER` `DATABASE` `LINK` statement.
* This statement is valid only for fixed-user database links, not for connected-user or current user database links. See [CREATE DATABASE LINK](statements_5006.md#i2061505) for more information on these two types of database links.

Prerequisites

To alter a private database link, you must have the `ALTER` `DATABASE` `LINK` system privilege. To alter a public database link, you must have the `ALTER` `PUBLIC` `DATABASE` `LINK` system privilege.

Semantics

The `ALTER` `DATABASE` `LINK` statement is intended only to update fixed-user database links with the current passwords of connection and authentication users. Therefore, any clauses valid in a `CREATE` `DATABASE` `LINK` statement that do not appear in the syntax diagram above are not valid in an `ALTER` `DATABASE` `LINK` statement. The semantics of all of the clauses permitted in this statement are the same as the semantics for those clauses in `CREATE` `DATABASE` `LINK`. Refer to [CREATE DATABASE LINK](statements_5006.md#i2061505) for this information.

Examples

The following statements show the valid variations of the `ALTER` `DATABASE` `LINK` statement:

```
ALTER DATABASE LINK private_link 
  CONNECT TO hr IDENTIFIED BY hr_new_password;

ALTER PUBLIC DATABASE LINK public_link
  CONNECT TO scott IDENTIFIED BY scott_new_password;

ALTER SHARED PUBLIC DATABASE LINK shared_pub_link
  CONNECT TO scott IDENTIFIED BY scott_new_password
  AUTHENTICATED BY hr IDENTIFIED BY hr_new_password;

ALTER SHARED DATABASE LINK shared_pub_link
  CONNECT TO scott IDENTIFIED BY scott_new_password;
```

Scripting on this page enhances content navigation, but does not change the content in any way.