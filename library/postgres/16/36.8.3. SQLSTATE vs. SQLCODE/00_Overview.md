---
source: PostgreSQL 16 Reference
title: 00_Overview
---

The fields sqlca.sqlstate and sqlca.sqlcode are two different schemes that provide error codes. Both are derived from the SQL standard, but SQLCODE has been marked deprecated in the SQL-92 edition of the standard and has been dropped in later editions. Therefore, new applications are strongly encouraged to use SQLSTATE.

SQLSTATE is a five-character array. The five characters contain digits or upper-case letters that represent codes of various error and warning conditions. SQLSTATE has a hierarchical scheme: the first two characters indicate the general class of the condition, the last three characters indicate a subclass of the general condition. A successful state is indicated by the code 00000. The SQLSTATE codes are for the most part defined in the SQL standard. The PostgreSQL server natively supports SQLSTATE error codes; therefore a high degree of consistency can be achieved by using this error code scheme throughout all applications. For further information see Appendix A.

SQLCODE, the deprecated error code scheme, is a simple integer. A value of 0 indicates success, a positive value indicates success with additional information, a negative value indicates an error. The SQL standard only defines the positive value +100, which indicates that the last command returned or affected zero rows, and no specific negative values. Therefore, this scheme can only achieve poor portability and does not have a hierarchical code assignment. Historically, the embedded SQL processor for PostgreSQL has assigned some specific SQLCODE values for its use, which are listed below with their numeric value and their symbolic name. Remember that these are not portable to other SQL implementations. To simplify the porting of applications to the SQLSTATE scheme, the corresponding SQLSTATE is also listed. There is, however, no one-to-one or one-to-many mapping between the two schemes (indeed it is many-to-many), so you should consult the global SQLSTATE listing in Appendix A in each case.

These are the assigned SQLCODE values:

```
0 (ECPG_NO_ERROR)
   Indicates no error. (SQLSTATE 00000)
100 (ECPG_NOT_FOUND)
```

This is a harmless condition indicating that the last command retrieved or processed zero rows, or that you are at the end of the cursor. (SQLSTATE 02000)

When processing a cursor in a loop, you could use this code as a way to detect when to abort the loop, like this:

```
while (1)
{
 EXEC SQL FETCH ... ;
 if (sqlca.sqlcode == ECPG_NOT_FOUND)
 break;
}
```

But WHENEVER NOT FOUND DO BREAK effectively does this internally, so there is usually no advantage in writing this out explicitly.

```
-12 (ECPG_OUT_OF_MEMORY)
```

Indicates that your virtual memory is exhausted. The numeric value is defined as -ENOMEM. (SQLSTATE YE001)

```
-200 (ECPG_UNSUPPORTED)
```

Indicates the preprocessor has generated something that the library does not know about. Perhaps you are running incompatible versions of the preprocessor and the library. (SQLSTATE YE002)

```
-201 (ECPG_TOO_MANY_ARGUMENTS)
```

This means that the command specified more host variables than the command expected. (SQLS-TATE 07001 or 07002)

```
-202 (ECPG_TOO_FEW_ARGUMENTS)
```

This means that the command specified fewer host variables than the command expected. (SQLS-TATE 07001 or 07002)

```
-203 (ECPG_TOO_MANY_MATCHES)
```

This means a query has returned multiple rows but the statement was only prepared to store one result row (for example, because the specified variables are not arrays). (SQLSTATE 21000)

```
-204 (ECPG_INT_FORMAT)
```

The host variable is of type int and the datum in the database is of a different type and contains a value that cannot be interpreted as an int. The library uses strtol() for this conversion. (SQLSTATE 42804)

```
-205 (ECPG_UINT_FORMAT)
```

The host variable is of type unsigned int and the datum in the database is of a different type and contains a value that cannot be interpreted as an unsigned int. The library uses strtoul() for this conversion. (SQLSTATE 42804)

```
-206 (ECPG_FLOAT_FORMAT)
```

The host variable is of type float and the datum in the database is of another type and contains a value that cannot be interpreted as a float. The library uses strtod() for this conversion. (SQLSTATE 42804)

```
-207 (ECPG_NUMERIC_FORMAT)
```

The host variable is of type numeric and the datum in the database is of another type and contains a value that cannot be interpreted as a numeric value. (SQLSTATE 42804)

```
-208 (ECPG_INTERVAL_FORMAT)
```

The host variable is of type interval and the datum in the database is of another type and contains a value that cannot be interpreted as an interval value. (SQLSTATE 42804)

```
-209 (ECPG_DATE_FORMAT)
```

The host variable is of type date and the datum in the database is of another type and contains a value that cannot be interpreted as a date value. (SQLSTATE 42804)

```
-210 (ECPG_TIMESTAMP_FORMAT)
```

The host variable is of type timestamp and the datum in the database is of another type and contains a value that cannot be interpreted as a timestamp value. (SQLSTATE 42804)

```
-211 (ECPG_CONVERT_BOOL)
```

This means the host variable is of type bool and the datum in the database is neither 't' nor 'f'. (SQLSTATE 42804)

```
-212 (ECPG_EMPTY)
```

The statement sent to the PostgreSQL server was empty. (This cannot normally happen in an embedded SQL program, so it might point to an internal error.) (SQLSTATE YE002)

```
-213 (ECPG_MISSING_INDICATOR)
```

A null value was returned and no null indicator variable was supplied. (SQLSTATE 22002)

```
-214 (ECPG_NO_ARRAY)
```

An ordinary variable was used in a place that requires an array. (SQLSTATE 42804)

```
-215 (ECPG_DATA_NOT_ARRAY)
```

The database returned an ordinary variable in a place that requires array value. (SQLSTATE 42804)

```
-216 (ECPG_ARRAY_INSERT)
```

The value could not be inserted into the array. (SQLSTATE 42804)

-220 (ECPG\_NO\_CONN)

The program tried to access a connection that does not exist. (SQLSTATE 08003)

-221 (ECPG\_NOT\_CONN)

The program tried to access a connection that does exist but is not open. (This is an internal error.) (SQLSTATE YE002)

-230 (ECPG\_INVALID\_STMT)

The statement you are trying to use has not been prepared. (SQLSTATE 26000)

-239 (ECPG\_INFORMIX\_DUPLICATE\_KEY)

Duplicate key error, violation of unique constraint (Informix compatibility mode). (SQLSTATE 23505)

-240 (ECPG\_UNKNOWN\_DESCRIPTOR)

The descriptor specified was not found. The statement you are trying to use has not been prepared. (SQLSTATE 33000)

-241 (ECPG\_INVALID\_DESCRIPTOR\_INDEX)

The descriptor index specified was out of range. (SQLSTATE 07009)

-242 (ECPG\_UNKNOWN\_DESCRIPTOR\_ITEM)

An invalid descriptor item was requested. (This is an internal error.) (SQLSTATE YE002)

-243 (ECPG\_VAR\_NOT\_NUMERIC)

During the execution of a dynamic statement, the database returned a numeric value and the host variable was not numeric. (SQLSTATE 07006)

-244 (ECPG\_VAR\_NOT\_CHAR)

During the execution of a dynamic statement, the database returned a non-numeric value and the host variable was numeric. (SQLSTATE 07006)

-284 (ECPG\_INFORMIX\_SUBSELECT\_NOT\_ONE)

A result of the subquery is not single row (Informix compatibility mode). (SQLSTATE 21000)

-400 (ECPG\_PGSQL)

Some error caused by the PostgreSQL server. The message contains the error message from the PostgreSQL server.

-401 (ECPG\_TRANS)

The PostgreSQL server signaled that we cannot start, commit, or rollback the transaction. (SQLS-TATE 08007)

-402 (ECPG\_CONNECT)

The connection attempt to the database did not succeed. (SQLSTATE 08001)

-403 (ECPG\_DUPLICATE\_KEY)

Duplicate key error, violation of unique constraint. (SQLSTATE 23505)

```
-404 (ECPG_SUBSELECT_NOT_ONE)
   A result for the subquery is not single row. (SQLSTATE 21000)
-602 (ECPG_WARNING_UNKNOWN_PORTAL)
   An invalid cursor name was specified. (SQLSTATE 34000)
-603 (ECPG_WARNING_IN_TRANSACTION)
   Transaction is in progress. (SQLSTATE 25001)
-604 (ECPG_WARNING_NO_TRANSACTION)
   There is no active (in-progress) transaction. (SQLSTATE 25P01)
-605 (ECPG_WARNING_PORTAL_EXISTS)
   An existing cursor name was specified. (SQLSTATE 42P03)
```