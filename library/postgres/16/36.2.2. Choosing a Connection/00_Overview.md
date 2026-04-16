---
source: PostgreSQL 16 Reference
title: 00_Overview
---

SQL statements in embedded SQL programs are by default executed on the current connection, that is, the most recently opened one. If an application needs to manage multiple connections, then there are three ways to handle this.

The first option is to explicitly choose a connection for each SQL statement, for example:

```
EXEC SQL AT connection-name SELECT ...;
```

This option is particularly suitable if the application needs to use several connections in mixed order.

If your application uses multiple threads of execution, they cannot share a connection concurrently. You must either explicitly control access to the connection (using mutexes) or use a connection for each thread.

The second option is to execute a statement to switch the current connection. That statement is:

```
EXEC SQL SET CONNECTION connection-name;
```

This option is particularly convenient if many statements are to be executed on the same connection.

Here is an example program managing multiple database connections:

```
#include <stdio.h>
EXEC SQL BEGIN DECLARE SECTION;
 char dbname[1024];
EXEC SQL END DECLARE SECTION;
int
main()
{
 EXEC SQL CONNECT TO testdb1 AS con1 USER testuser;
 EXEC SQL SELECT pg_catalog.set_config('search_path', '',
 false); EXEC SQL COMMIT;
```

```
 EXEC SQL CONNECT TO testdb2 AS con2 USER testuser;
 EXEC SQL SELECT pg_catalog.set_config('search_path', '',
 false); EXEC SQL COMMIT;
 EXEC SQL CONNECT TO testdb3 AS con3 USER testuser;
 EXEC SQL SELECT pg_catalog.set_config('search_path', '',
 false); EXEC SQL COMMIT;
 /* This query would be executed in the last opened database
 "testdb3". */
 EXEC SQL SELECT current_database() INTO :dbname;
 printf("current=%s (should be testdb3)\n", dbname);
 /* Using "AT" to run a query in "testdb2" */
 EXEC SQL AT con2 SELECT current_database() INTO :dbname;
 printf("current=%s (should be testdb2)\n", dbname);
 /* Switch the current connection to "testdb1". */
 EXEC SQL SET CONNECTION con1;
 EXEC SQL SELECT current_database() INTO :dbname;
 printf("current=%s (should be testdb1)\n", dbname);
 EXEC SQL DISCONNECT ALL;
 return 0;
}
This example would produce this output:
current=testdb3 (should be testdb3)
current=testdb2 (should be testdb2)
```

The third option is to declare an SQL identifier linked to the connection, for example:

```
EXEC SQL AT connection-name DECLARE statement-name STATEMENT;
EXEC SQL PREPARE statement-name FROM :dyn-string;
```

Once you link an SQL identifier to a connection, you execute dynamic SQL without an AT clause. Note that this option behaves like preprocessor directives, therefore the link is enabled only in the file.

Here is an example program using this option:

current=testdb1 (should be testdb1)

```
#include <stdio.h>
EXEC SQL BEGIN DECLARE SECTION;
char dbname[128];
char *dyn_sql = "SELECT current_database()";
EXEC SQL END DECLARE SECTION;
int main(){
 EXEC SQL CONNECT TO postgres AS con1;
 EXEC SQL CONNECT TO testdb AS con2;
 EXEC SQL AT con1 DECLARE stmt STATEMENT;
 EXEC SQL PREPARE stmt FROM :dyn_sql;
 EXEC SQL EXECUTE stmt INTO :dbname;
 printf("%s\n", dbname);
```

```
 EXEC SQL DISCONNECT ALL;
 return 0;
}
```

This example would produce this output, even if the default connection is testdb:

postgres