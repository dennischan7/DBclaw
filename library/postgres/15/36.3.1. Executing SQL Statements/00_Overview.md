---
source: PostgreSQL 15 Reference
title: 00_Overview
---

Creating a table:

```
EXEC SQL CREATE TABLE foo (number integer, ascii char(16));
EXEC SQL CREATE UNIQUE INDEX num1 ON foo(number);
EXEC SQL COMMIT;
Inserting rows:
EXEC SQL INSERT INTO foo (number, ascii) VALUES (9999, 'doodad');
EXEC SQL COMMIT;
Deleting rows:
EXEC SQL DELETE FROM foo WHERE number = 9999;
EXEC SQL COMMIT;
Updates:
```

```
EXEC SQL UPDATE foo
 SET ascii = 'foobar'
 WHERE number = 9999;
EXEC SQL COMMIT;
```

SELECT statements that return a single result row can also be executed using EXEC SQL directly. To handle result sets with multiple rows, an application has to use a cursor; see [Section 36.3.2](#page-15-0) below. (As a special case, an application can fetch multiple rows at once into an array host variable; see [Section 36.4.4.3.1](#page-23-0).)

Single-row select:

```
EXEC SQL SELECT foo INTO :FooBar FROM table1 WHERE ascii =
 'doodad';
```

Also, a configuration parameter can be retrieved with the SHOW command:

```
EXEC SQL SHOW search_path INTO :var;
```

The tokens of the form :something are *host variables*, that is, they refer to variables in the C program. They are explained in [Section 36.4](#page-17-0).

# <span id="page-15-0"></span>**36.3.2. Using Cursors**

To retrieve a result set holding multiple rows, an application has to declare a cursor and fetch each row from the cursor. The steps to use a cursor are the following: declare a cursor, open it, fetch a row from the cursor, repeat, and finally close it.

Select using cursors:

```
EXEC SQL DECLARE foo_bar CURSOR FOR
 SELECT number, ascii FROM foo
 ORDER BY ascii;
EXEC SQL OPEN foo_bar;
EXEC SQL FETCH foo_bar INTO :FooBar, DooDad;
...
EXEC SQL CLOSE foo_bar;
EXEC SQL COMMIT;
```

For more details about declaring a cursor, see [DECLARE;](#page-82-0) for more details about fetching rows from a cursor, see FETCH.

### **Note**

The ECPG DECLARE command does not actually cause a statement to be sent to the PostgreSQL backend. The cursor is opened in the backend (using the backend's DECLARE command) at the point when the OPEN command is executed.