---
source: PostgreSQL 16 Reference
title: 00_Overview
---

One connects to a database using the following statement:

EXEC SQL CONNECT TO target [AS connection-name] [USER user-name];

The target can be specified in the following ways:

- dbname[@hostname][:port]
- tcp:postgresql://hostname[:port][/dbname][?options]
- unix:postgresql://localhost[:port][/dbname][?options]
- an SQL string literal containing one of the above forms
- a reference to a character variable containing one of the above forms (see examples)
- DEFAULT

The connection target DEFAULT initiates a connection to the default database under the default user name. No separate user name or connection name can be specified in that case.

If you specify the connection target directly (that is, not as a string literal or variable reference), then the components of the target are passed through normal SQL parsing; this means that, for example, the hostname must look like one or more SQL identifiers separated by dots, and those identifiers will be case-folded unless double-quoted. Values of any options must be SQL identifiers, integers, or variable references. Of course, you can put nearly anything into an SQL identifier by double-quoting it. In practice, it is probably less error-prone to use a (single-quoted) string literal or a variable reference than to write the connection target directly.

There are also different ways to specify the user name:

- username
- username/password
- username IDENTIFIED BY password
- username USING password

As above, the parameters username and password can be an SQL identifier, an SQL string literal, or a reference to a character variable.

If the connection target includes any options, those consist of keyword=value specifications separated by ampersands (&). The allowed key words are the same ones recognized by libpq (see Section 34.1.2). Spaces are ignored before any keyword or value, though not within or after one. Note that there is no way to write & within a value.

Notice that when specifying a socket connection (with the unix: prefix), the host name must be exactly localhost. To select a non-default socket directory, write the directory's pathname as the value of a host option in the options part of the target.

The connection-name is used to handle multiple connections in one program. It can be omitted if a program uses only one connection. The most recently opened connection becomes the current connection, which is used by default when an SQL statement is to be executed (see later in this chapter).

Here are some examples of CONNECT statements:

```
EXEC SQL CONNECT TO mydb@sql.mydomain.com;
EXEC SQL CONNECT TO tcp:postgresql://sql.mydomain.com/mydb AS
 myconnection USER john;
EXEC SQL BEGIN DECLARE SECTION;
```

```
const char *target = "mydb@sql.mydomain.com";
const char *user = "john";
const char *passwd = "secret";
EXEC SQL END DECLARE SECTION;
 ...
EXEC SQL CONNECT TO :target USER :user USING :passwd;
/* or EXEC SQL CONNECT TO :target USER :user/:passwd; */
```

The last example makes use of the feature referred to above as character variable references. You will see in later sections how C variables can be used in SQL statements when you prefix them with a colon.

Be advised that the format of the connection target is not specified in the SQL standard. So if you want to develop portable applications, you might want to use something based on the last example above to encapsulate the connection target string somewhere.

If untrusted users have access to a database that has not adopted a secure schema usage pattern, begin each session by removing publicly-writable schemas from search\_path. For example, add options=-c search\_path= to options, or issue EXEC SQL SELECT pg\_catalog.set\_config('search\_path', '', false); after connecting. This consideration is not specific to ECPG; it applies to every interface for executing arbitrary SQL commands.