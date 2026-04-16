---
source: PostgreSQL 15 Reference
title: 00_Overview
---

The PostgreSQL source code can be compiled with coverage testing instrumentation, so that it becomes possible to examine which parts of the code are covered by the regression tests or any other test suite that is run with the code. This is currently supported when compiling with GCC, and it requires the gcov and lcov programs.

A typical workflow looks like this:

```
./configure --enable-coverage ... OTHER OPTIONS ...
make
make check # or other test suite
make coverage-html
```

Then point your HTML browser to coverage/index.html.

If you don't have lcov or prefer text output over an HTML report, you can run

make coverage

instead of make coverage-html, which will produce .gcov output files for each source file relevant to the test. (make coverage and make coverage-html will overwrite each other's files, so mixing them might be confusing.)

You can run several different tests before making the coverage report; the execution counts will accumulate. If you want to reset the execution counts between test runs, run:

make coverage-clean

You can run the make coverage-html or make coverage command in a subdirectory if you want a coverage report for only a portion of the code tree.

Use make distclean to clean up when done.

# **Part IV. Client Interfaces**

This part describes the client programming interfaces distributed with PostgreSQL. Each of these chapters can be read independently. Note that there are many other programming interfaces for client programs that are distributed separately and contain their own documentation (Appendix H lists some of the more popular ones). Readers of this part should be familiar with using SQL commands to manipulate and query the database (see Part II) and of course with the programming language that the interface uses.

# **Table of Contents**

| 34. libpq — C Library                                  | 872 |
|--------------------------------------------------------|-----|
| 34.1. Database Connection Control Functions            |     |
| 34.1.1. Connection Strings                             |     |
| 34.1.2. Parameter Key Words                            |     |
| 34.2. Connection Status Functions                      |     |
| 34.3. Command Execution Functions                      |     |
| 34.3.1. Main Functions                                 |     |
| 34.3.2. Retrieving Query Result Information            |     |
| 34.3.3. Retrieving Other Result Information            |     |
| 34.3.4. Escaping Strings for Inclusion in SQL Commands |     |
| 34.4. Asynchronous Command Processing                  |     |
| 34.5. Pipeline Mode                                    |     |
| 34.5.1. Using Pipeline Mode                            |     |
| 34.5.2. Functions Associated with Pipeline Mode        |     |
| 34.5.3. When to Use Pipeline Mode                      |     |
| 34.6. Retrieving Query Results Row-by-Row              |     |
|                                                        |     |
| 34.7. Canceling Queries in Progress                    |     |
|                                                        |     |
| 34.9. Asynchronous Notification                        |     |
| 34.10. Functions Associated with the COPY Command      |     |
| 34.10.1. Functions for Sending COPY Data               |     |
| 34.10.2. Functions for Receiving COPY Data             |     |
| 34.10.3. Obsolete Functions for COPY                   |     |
| 34.11. Control Functions                               |     |
| 34.12. Miscellaneous Functions                         |     |
| 34.13. Notice Processing                               |     |
| 34.14. Event System                                    |     |
| 34.14.1. Event Types                                   |     |
| 34.14.2. Event Callback Procedure                      |     |
| 34.14.3. Event Support Functions                       |     |
| 34.14.4. Event Example                                 |     |
| 34.15. Environment Variables                           |     |
| 34.16. The Password File                               |     |
| 34.17. The Connection Service File                     |     |
| 34.18. LDAP Lookup of Connection Parameters            |     |
| 34.19. SSL Support                                     |     |
| 34.19.1. Client Verification of Server Certificates    |     |
| 34.19.2. Client Certificates                           |     |
| 34.19.3. Protection Provided in Different Modes        |     |
| 34.19.4. SSL Client File Usage                         |     |
| 34.19.5. SSL Library Initialization                    |     |
| 34.20. Behavior in Threaded Programs                   | 947 |
| 34.21. Building libpq Programs                         | 948 |
| 34.22. Example Programs                                | 949 |
| 35. Large Objects                                      | 961 |
| 35.1. Introduction                                     | 961 |
| 35.2. Implementation Features                          | 961 |
| 35.3. Client Interfaces                                | 961 |
| 35.3.1. Creating a Large Object                        | 962 |
| 35.3.2. Importing a Large Object                       |     |
| 35.3.3. Exporting a Large Object                       |     |
| 35.3.4. Opening an Existing Large Object               |     |
| 35.3.5. Writing Data to a Large Object                 |     |
| 35.3.6. Reading Data from a Large Object               |     |
| 35.3.7 Seeking in a Large Object                       |     |

### Client Interfaces

| 35.3.8. Obtaining the Seek Position of a Large Object       |       |
|-------------------------------------------------------------|-------|
| 35.3.9. Truncating a Large Object                           |       |
| 35.3.10. Closing a Large Object Descriptor                  |       |
| 35.3.11. Removing a Large Object                            |       |
| 35.4. Server-Side Functions                                 |       |
| 35.5. Example Program                                       |       |
| 36. ECPG — Embedded SQL in C                                | . 973 |
| 36.1. The Concept                                           | . 973 |
| 36.2. Managing Database Connections                         | . 973 |
| 36.2.1. Connecting to the Database Server                   |       |
| 36.2.2. Choosing a Connection                               |       |
| 36.2.3. Closing a Connection                                |       |
| 36.3. Running SQL Commands                                  |       |
| 36.3.1. Executing SQL Statements                            |       |
| 36.3.2. Using Cursors                                       |       |
| 36.3.3. Managing Transactions                               |       |
| 36.3.4. Prepared Statements                                 |       |
| 36.4. Using Host Variables                                  |       |
| 36.4.1. Overview                                            |       |
|                                                             |       |
| 36.4.2. Declare Sections                                    |       |
| 36.4.3. Retrieving Query Results                            |       |
| 36.4.4. Type Mapping                                        |       |
| 36.4.5. Handling Nonprimitive SQL Data Types                |       |
| 36.4.6. Indicators                                          |       |
| 36.5. Dynamic SQL                                           |       |
| 36.5.1. Executing Statements without a Result Set           |       |
| 36.5.2. Executing a Statement with Input Parameters         | . 995 |
| 36.5.3. Executing a Statement with a Result Set             | . 995 |
| 36.6. pgtypes Library                                       | . 996 |
| 36.6.1. Character Strings                                   | . 996 |
| 36.6.2. The numeric Type                                    | . 996 |
| 36.6.3. The date Type                                       |       |
| 36.6.4. The timestamp Type                                  |       |
| 36.6.5. The interval Type                                   |       |
| 36.6.6. The decimal Type                                    |       |
| 36.6.7. errno Values of pgtypeslib                          |       |
| 36.6.8. Special Constants of pgtypeslib                     |       |
| 36.7. Using Descriptor Areas                                |       |
| 36.7.1. Named SQL Descriptor Areas                          |       |
|                                                             |       |
| 36.7.2. SQLDA Descriptor Areas                              |       |
| 36.8. Error Handling                                        |       |
| 36.8.1. Setting Callbacks                                   |       |
| 36.8.2. sqlca                                               |       |
| 36.8.3. SQLSTATE vs. SQLCODE                                |       |
| 36.9. Preprocessor Directives                               |       |
| 36.9.1. Including Files                                     |       |
| 36.9.2. The define and undef Directives                     |       |
| 36.9.3. ifdef, ifndef, elif, else, and endif Directives     | 1031  |
| 36.10. Processing Embedded SQL Programs                     | 1032  |
| 36.11. Library Functions                                    | 1033  |
| 36.12. Large Objects                                        | 1034  |
| 36.13. C++ Applications                                     |       |
| 36.13.1. Scope for Host Variables                           |       |
| 36.13.2. C++ Application Development with External C Module |       |
| 36.14. Embedded SQL Commands                                |       |
| 36.15. Informix Compatibility Mode                          |       |
| 36.15.1. Additional Types                                   |       |
| 36.15.2. Additional/Missing Embedded SQL Statements         |       |
|                                                             |       |

### Client Interfaces

| 36.15.3. Informix-compatible SQLDA Descriptor Areas |      |
|-----------------------------------------------------|------|
| 36.15.4. Additional Functions                       |      |
| 36.15.5. Additional Constants                       | 1077 |
| 36.16. Oracle Compatibility Mode                    | 1078 |
| 36.17. Internals                                    | 1078 |
| 37. The Information Schema                          | 1081 |
| 37.1. The Schema                                    | 1081 |
| 37.2. Data Types                                    | 1081 |
| 37.3. information schema catalog name               |      |
| 37.4. administrable_role_authorizations             |      |
| 37.5. applicable roles                              |      |
| 37.6. attributes                                    |      |
| 37.7. character sets                                |      |
| 37.8. check constraint routine usage                |      |
| 37.9. check constraints                             |      |
| 37.10. collations                                   |      |
| 37.11. collation character set applicability        |      |
| 37.11. collaction_character_set_applicability       |      |
|                                                     |      |
| 37.13. column_domain_usage                          |      |
| 37.14. column_options                               |      |
| 37.15. column_privileges                            |      |
| 37.16. column_udt_usage                             |      |
| 37.17. columns                                      |      |
| 37.18. constraint_column_usage                      |      |
| 37.19. constraint_table_usage                       |      |
| 37.20. data_type_privileges                         |      |
| 37.21. domain_constraints                           |      |
| 37.22. domain_udt_usage                             |      |
| 37.23. domains                                      |      |
| 37.24. element_types                                |      |
| 37.25. enabled_roles                                |      |
| 37.26. foreign_data_wrapper_options                 |      |
| 37.27. foreign_data_wrappers                        |      |
| 37.28. foreign_server_options                       |      |
| 37.29. foreign_servers                              |      |
| 37.30. foreign_table_options                        |      |
| 37.31. foreign_tables                               |      |
| 37.32. key_column_usage                             |      |
| 37.33. parameters                                   |      |
| 37.34 referential_constraints                       |      |
| 37.35. role_column_grants                           |      |
| 37.36. role_routine_grants                          |      |
| 37.37. role_table_grants                            |      |
| 37.38. role_udt_grants                              |      |
| 37.39. role_usage_grants                            |      |
| 37.40. routine_column_usage                         |      |
| 37.41. routine_privileges                           |      |
| 37.42. routine_routine_usage                        | 1110 |
| 37.43. routine_sequence_usage                       | 1111 |
| 37.44 routine_table_usage                           |      |
| 37.45. routines                                     | 1112 |
| 37.46. schemata                                     |      |
| 37.47. sequences                                    | 1116 |
| 37.48. sql_features                                 | 1117 |
| 37.49. sql_implementation_info                      | 1118 |
| 37.50. sql_parts                                    |      |
| 37.51. sql_sizing                                   | 1119 |
| 37.52 table constraints                             | 1119 |

### Client Interfaces

| 37.53. | table_privileges         | 1120 |
|--------|--------------------------|------|
| 37.54. | tables                   | 1120 |
| 37.55. | transforms               | 1121 |
| 37.56. | triggered update columns | 1122 |
| 37.57. | triggers                 | 1122 |
| 37.58. | udt_privileges           | 1124 |
|        | usage privileges         |      |
| 37.60. | user defined types       | 1125 |
|        | user mapping options     |      |
| 37.62. | user mappings            | 1127 |
| 37.63. | view column usage        | 1127 |
| 37.64. | view routine usage       | 1128 |
| 37.65. | view table usage         | 1128 |
| 37.66. | views                    | 1129 |

# <span id="page-109-0"></span>**Chapter 34. libpq — C Library**

libpq is the C application programmer's interface to PostgreSQL. libpq is a set of library functions that allow client programs to pass queries to the PostgreSQL backend server and to receive the results of these queries.

libpq is also the underlying engine for several other PostgreSQL application interfaces, including those written for C++, Perl, Python, Tcl and ECPG. So some aspects of libpq's behavior will be important to you if you use one of those packages. In particular, [Section 34.15,](#page-176-0) [Section 34.16](#page-178-0) and [Section 34.19](#page-180-0) describe behavior that is visible to the user of any application that uses libpq.

Some short programs are included at the end of this chapter [\(Section 34.22\)](#page-186-0) to show how to write programs that use libpq. There are also several complete examples of libpq applications in the directory src/test/examples in the source code distribution.

Client programs that use libpq must include the header file libpq-fe.h and must link with the libpq library.

# <span id="page-109-1"></span>**34.1. Database Connection Control Functions**

The following functions deal with making a connection to a PostgreSQL backend server. An application program can have several backend connections open at one time. (One reason to do that is to access more than one database.) Each connection is represented by a PGconn object, which is obtained from the function [PQconnectdb](#page-110-0), [PQconnectdbParams](#page-109-2), or [PQsetdbLogin](#page-110-1). Note that these functions will always return a non-null object pointer, unless perhaps there is too little memory even to allocate the PGconn object. The [PQstatus](#page-127-0) function should be called to check the return value for a successful connection before queries are sent via the connection object.

## **Warning**

If untrusted users have access to a database that has not adopted a secure schema usage pattern, begin each session by removing publicly-writable schemas from search\_path. One can set parameter key word options to value -csearch\_path=. Alternately, one can issue PQexec(conn, "SELECT pg\_catalog.set\_config('search\_path', '', false)") after connecting. This consideration is not specific to libpq; it applies to every interface for executing arbitrary SQL commands.

## **Warning**

On Unix, forking a process with open libpq connections can lead to unpredictable results because the parent and child processes share the same sockets and operating system resources. For this reason, such usage is not recommended, though doing an exec from the child process to load a new executable is safe.

<span id="page-109-2"></span>PQconnectdbParams

Makes a new connection to the database server.

```
PGconn *PQconnectdbParams(const char * const *keywords,
 const char * const *values,
 int expand_dbname);
```

This function opens a new database connection using the parameters taken from two NULL-terminated arrays. The first, keywords, is defined as an array of strings, each one being a key word. The second, values, gives the value for each key word. Unlike [PQsetdbLogin](#page-110-1) below, the parameter set can be extended without changing the function signature, so use of this function (or its nonblocking analogs [PQconnectStartParams](#page-111-0) and PQconnectPoll) is preferred for new application programming.

The currently recognized parameter key words are listed in [Section 34.1.2](#page-118-0).

The passed arrays can be empty to use all default parameters, or can contain one or more parameter settings. They must be matched in length. Processing will stop at the first NULL entry in the keywords array. Also, if the values entry associated with a non-NULL keywords entry is NULL or an empty string, that entry is ignored and processing continues with the next pair of array entries.

When expand\_dbname is non-zero, the value for the first dbname key word is checked to see if it is a *connection string*. If so, it is "expanded" into the individual connection parameters extracted from the string. The value is considered to be a connection string, rather than just a database name, if it contains an equal sign (=) or it begins with a URI scheme designator. (More details on connection string formats appear in [Section 34.1.1](#page-116-0).) Only the first occurrence of dbname is treated in this way; any subsequent dbname parameter is processed as a plain database name.

In general the parameter arrays are processed from start to end. If any key word is repeated, the last value (that is not NULL or empty) is used. This rule applies in particular when a key word found in a connection string conflicts with one appearing in the keywords array. Thus, the programmer may determine whether array entries can override or be overridden by values taken from a connection string. Array entries appearing before an expanded dbname entry can be overridden by fields of the connection string, and in turn those fields are overridden by array entries appearing after dbname (but, again, only if those entries supply non-empty values).

After processing all the array entries and any expanded connection string, any connection parameters that remain unset are filled with default values. If an unset parameter's corresponding environment variable (see [Section 34.15\)](#page-176-0) is set, its value is used. If the environment variable is not set either, then the parameter's built-in default value is used.

<span id="page-110-0"></span>PQconnectdb

Makes a new connection to the database server.

```
PGconn *PQconnectdb(const char *conninfo);
```

This function opens a new database connection using the parameters taken from the string conninfo.

The passed string can be empty to use all default parameters, or it can contain one or more parameter settings separated by whitespace, or it can contain a URI. See [Section 34.1.1](#page-116-0) for details.

<span id="page-110-1"></span>PQsetdbLogin

Makes a new connection to the database server.

```
PGconn *PQsetdbLogin(const char *pghost,
 const char *pgport,
 const char *pgoptions,
 const char *pgtty,
 const char *dbName,
 const char *login,
```

```
 const char *pwd);
```

This is the predecessor of [PQconnectdb](#page-110-0) with a fixed set of parameters. It has the same functionality except that the missing parameters will always take on default values. Write NULL or an empty string for any one of the fixed parameters that is to be defaulted.

If the dbName contains an = sign or has a valid connection URI prefix, it is taken as a conninfo string in exactly the same way as if it had been passed to [PQconnectdb](#page-110-0), and the remaining parameters are then applied as specified for [PQconnectdbParams](#page-109-2).

pgtty is no longer used and any value passed will be ignored.

<span id="page-111-1"></span>PQsetdb

Makes a new connection to the database server.

```
PGconn *PQsetdb(char *pghost,
 char *pgport,
 char *pgoptions,
 char *pgtty,
 char *dbName);
```

This is a macro that calls [PQsetdbLogin](#page-110-1) with null pointers for the login and pwd parameters. It is provided for backward compatibility with very old programs.

```
PQconnectStartParams
PQconnectStart
PQconnectPoll
```

Make a connection to the database server in a nonblocking manner.

```
PGconn *PQconnectStartParams(const char * const *keywords,
 const char * const *values,
 int expand_dbname);
PGconn *PQconnectStart(const char *conninfo);
PostgresPollingStatusType PQconnectPoll(PGconn *conn);
```

These three functions are used to open a connection to a database server such that your application's thread of execution is not blocked on remote I/O whilst doing so. The point of this approach is that the waits for I/O to complete can occur in the application's main loop, rather than down inside [PQconnectdbParams](#page-109-2) or [PQconnectdb](#page-110-0), and so the application can manage this operation in parallel with other activities.

With [PQconnectStartParams](#page-111-0), the database connection is made using the parameters taken from the keywords and values arrays, and controlled by expand\_dbname, as described above for [PQconnectdbParams](#page-109-2).

With PQconnectStart, the database connection is made using the parameters taken from the string conninfo as described above for [PQconnectdb](#page-110-0).

Neither [PQconnectStartParams](#page-111-0) nor PQconnectStart nor PQconnectPoll will block, so long as a number of restrictions are met:

- The hostaddr parameter must be used appropriately to prevent DNS queries from being made. See the documentation of this parameter in [Section 34.1.2](#page-118-0) for details.
- If you call [PQtrace](#page-165-1), ensure that the stream object into which you trace will not block.

• You must ensure that the socket is in the appropriate state before calling PQconnectPoll, as described below.

To begin a nonblocking connection request, call PQconnectStart or [PQconnectStart-](#page-111-0)[Params](#page-111-0). If the result is null, then libpq has been unable to allocate a new PGconn structure. Otherwise, a valid PGconn pointer is returned (though not yet representing a valid connection to the database). Next call PQstatus(conn). If the result is CONNECTION\_BAD, the connection attempt has already failed, typically because of invalid connection parameters.

If PQconnectStart or [PQconnectStartParams](#page-111-0) succeeds, the next stage is to poll libpq so that it can proceed with the connection sequence. Use PQsocket(conn) to obtain the descriptor of the socket underlying the database connection. (Caution: do not assume that the socket remains the same across PQconnectPoll calls.) Loop thus: If PQconnectPoll(conn) last returned PGRES\_POLLING\_READING, wait until the socket is ready to read (as indicated by select(), poll(), or similar system function). Then call PQconnectPoll(conn) again. Conversely, if PQconnectPoll(conn) last returned PGRES\_POLLING\_WRITING, wait until the socket is ready to write, then call PQconnectPoll(conn) again. On the first iteration, i.e., if you have yet to call PQconnectPoll, behave as if it last returned PGRES\_POL-LING\_WRITING. Continue this loop until PQconnectPoll(conn) returns PGRES\_POL-LING\_FAILED, indicating the connection procedure has failed, or PGRES\_POLLING\_OK, indicating the connection has been successfully made.

At any time during connection, the status of the connection can be checked by calling [PQsta](#page-127-0)[tus](#page-127-0). If this call returns CONNECTION\_BAD, then the connection procedure has failed; if the call returns CONNECTION\_OK, then the connection is ready. Both of these states are equally detectable from the return value of PQconnectPoll, described above. Other states might also occur during (and only during) an asynchronous connection procedure. These indicate the current stage of the connection procedure and might be useful to provide feedback to the user for example. These statuses are:

```
CONNECTION_STARTED
```

Waiting for connection to be made.

```
CONNECTION_MADE
```

Connection OK; waiting to send.

```
CONNECTION_AWAITING_RESPONSE
```

Waiting for a response from the server.

```
CONNECTION_AUTH_OK
```

Received authentication; waiting for backend start-up to finish.

```
CONNECTION_SSL_STARTUP
```

Negotiating SSL encryption.

```
CONNECTION_SETENV
```

Negotiating environment-driven parameter settings.

```
CONNECTION_CHECK_WRITABLE
```

Checking if connection is able to handle write transactions.

```
CONNECTION_CONSUME
```

Consuming any remaining response messages on connection.

Note that, although these constants will remain (in order to maintain compatibility), an application should never rely upon these occurring in a particular order, or at all, or on the status always being one of these documented values. An application might do something like this:

```
switch(PQstatus(conn))
{
 case CONNECTION_STARTED:
 feedback = "Connecting...";
 break;
 case CONNECTION_MADE:
 feedback = "Connected to server...";
 break;
.
.
.
 default:
 feedback = "Connecting...";
}
```

The connect\_timeout connection parameter is ignored when using PQconnectPoll; it is the application's responsibility to decide whether an excessive amount of time has elapsed. Otherwise, PQconnectStart followed by a PQconnectPoll loop is equivalent to [PQcon](#page-110-0)[nectdb](#page-110-0).

Note that when PQconnectStart or [PQconnectStartParams](#page-111-0) returns a non-null pointer, you must call [PQfinish](#page-114-0) when you are finished with it, in order to dispose of the structure and any associated memory blocks. This must be done even if the connection attempt fails or is abandoned.

<span id="page-113-0"></span>PQconndefaults

Returns the default connection options.

```
PQconninfoOption *PQconndefaults(void);
typedef struct
{
 char *keyword; /* The keyword of the option */
 char *envvar; /* Fallback environment variable name */
 char *compiled; /* Fallback compiled in default value */
 char *val; /* Option's current value, or NULL */
 char *label; /* Label for field in connect dialog */
 char *dispchar; /* Indicates how to display this field
 in a connect dialog. Values are:
 "" Display entered value as is
 "*" Password field - hide value
 "D" Debug option - don't show by
 default */
 int dispsize; /* Field size in characters for dialog */
} PQconninfoOption;
```

Returns a connection options array. This can be used to determine all possible [PQconnectdb](#page-110-0) options and their current default values. The return value points to an array of PQconninfoOption structures, which ends with an entry having a null keyword pointer. The null pointer is returned if memory could not be allocated. Note that the current default values (val fields) will depend on environment variables and other context. A missing or invalid service file will be silently ignored. Callers must treat the connection options data as read-only.

After processing the options array, free it by passing it to [PQconninfoFree](#page-166-0). If this is not done, a small amount of memory is leaked for each call to [PQconndefaults](#page-113-0).

<span id="page-114-1"></span>PQconninfo

Returns the connection options used by a live connection.

```
PQconninfoOption *PQconninfo(PGconn *conn);
```

Returns a connection options array. This can be used to determine all possible [PQconnectdb](#page-110-0) options and the values that were used to connect to the server. The return value points to an array of PQconninfoOption structures, which ends with an entry having a null keyword pointer. All notes above for [PQconndefaults](#page-113-0) also apply to the result of [PQconninfo](#page-114-1).

<span id="page-114-2"></span>PQconninfoParse

Returns parsed connection options from the provided connection string.

```
PQconninfoOption *PQconninfoParse(const char *conninfo, char
 **errmsg);
```

Parses a connection string and returns the resulting options as an array; or returns NULL if there is a problem with the connection string. This function can be used to extract the [PQconnectdb](#page-110-0) options in the provided connection string. The return value points to an array of PQconninfoOption structures, which ends with an entry having a null keyword pointer.

All legal options will be present in the result array, but the PQconninfoOption for any option not present in the connection string will have val set to NULL; default values are not inserted.

If errmsg is not NULL, then \*errmsg is set to NULL on success, else to a malloc'd error string explaining the problem. (It is also possible for \*errmsg to be set to NULL and the function to return NULL; this indicates an out-of-memory condition.)

After processing the options array, free it by passing it to [PQconninfoFree](#page-166-0). If this is not done, some memory is leaked for each call to [PQconninfoParse](#page-114-2). Conversely, if an error occurs and errmsg is not NULL, be sure to free the error string using [PQfreemem](#page-165-2).

<span id="page-114-0"></span>PQfinish

Closes the connection to the server. Also frees memory used by the PGconn object.

```
void PQfinish(PGconn *conn);
```

Note that even if the server connection attempt fails (as indicated by [PQstatus](#page-127-0)), the application should call [PQfinish](#page-114-0) to free the memory used by the PGconn object. The PGconn pointer must not be used again after [PQfinish](#page-114-0) has been called.

<span id="page-114-3"></span>PQreset

Resets the communication channel to the server.

```
void PQreset(PGconn *conn);
```

This function will close the connection to the server and attempt to establish a new connection, using all the same parameters previously used. This might be useful for error recovery if a working connection is lost.

<span id="page-115-0"></span>PQresetStart PQresetPoll

Reset the communication channel to the server, in a nonblocking manner.

```
int PQresetStart(PGconn *conn);
PostgresPollingStatusType PQresetPoll(PGconn *conn);
```

These functions will close the connection to the server and attempt to establish a new connection, using all the same parameters previously used. This can be useful for error recovery if a working connection is lost. They differ from [PQreset](#page-114-3) (above) in that they act in a nonblocking manner. These functions suffer from the same restrictions as [PQconnectStartParams](#page-111-0), PQconnectStart and PQconnectPoll.

To initiate a connection reset, call [PQresetStart](#page-115-0). If it returns 0, the reset has failed. If it returns 1, poll the reset using PQresetPoll in exactly the same way as you would create the connection using PQconnectPoll.

<span id="page-115-1"></span>PQpingParams

[PQpingParams](#page-115-1) reports the status of the server. It accepts connection parameters identical to those of [PQconnectdbParams](#page-109-2), described above. It is not necessary to supply correct user name, password, or database name values to obtain the server status; however, if incorrect values are provided, the server will log a failed connection attempt.

```
PGPing PQpingParams(const char * const *keywords,
 const char * const *values,
 int expand_dbname);
```

The function returns one of the following values:

```
PQPING_OK
```

The server is running and appears to be accepting connections.

```
PQPING_REJECT
```

The server is running but is in a state that disallows connections (startup, shutdown, or crash recovery).

```
PQPING_NO_RESPONSE
```

The server could not be contacted. This might indicate that the server is not running, or that there is something wrong with the given connection parameters (for example, wrong port number), or that there is a network connectivity problem (for example, a firewall blocking the connection request).

```
PQPING_NO_ATTEMPT
```

No attempt was made to contact the server, because the supplied parameters were obviously incorrect or there was some client-side problem (for example, out of memory).

<span id="page-115-2"></span>PQping

[PQping](#page-115-2) reports the status of the server. It accepts connection parameters identical to those of [PQconnectdb](#page-110-0), described above. It is not necessary to supply correct user name, password, or database name values to obtain the server status; however, if incorrect values are provided, the server will log a failed connection attempt.

```
PGPing PQping(const char *conninfo);
```

The return values are the same as for [PQpingParams](#page-115-1).

```
PQsetSSLKeyPassHook_OpenSSL
```

PQsetSSLKeyPassHook\_OpenSSL lets an application override libpq's [default handling of](#page-181-0) [encrypted client certificate key files](#page-181-0) using [sslpassword](#page-123-0) or interactive prompting.

```
void PQsetSSLKeyPassHook_OpenSSL(PQsslKeyPassHook_OpenSSL_type
 hook);
```

The application passes a pointer to a callback function with signature:

```
int callback_fn(char *buf, int size, PGconn *conn);
```

which libpq will then call *instead of* its default PQdefaultSSLKeyPassHook\_OpenSSL handler. The callback should determine the password for the key and copy it to result-buffer buf of size size. The string in buf must be null-terminated. The callback must return the length of the password stored in buf excluding the null terminator. On failure, the callback should set buf[0] = '\0' and return 0. See PQdefaultSSLKeyPassHook\_OpenSSL in libpq's source code for an example.

If the user specified an explicit key location, its path will be in conn->sslkey when the callback is invoked. This will be empty if the default key path is being used. For keys that are engine specifiers, it is up to engine implementations whether they use the OpenSSL password callback or define their own handling.

The app callback may choose to delegate unhandled cases to PQdefaultSSLKey-PassHook\_OpenSSL, or call it first and try something else if it returns 0, or completely override it.

The callback *must not* escape normal flow control with exceptions, longjmp(...), etc. It must return normally.

```
PQgetSSLKeyPassHook_OpenSSL
```

PQgetSSLKeyPassHook\_OpenSSL returns the current client certificate key password hook, or NULL if none has been set.

```
PQsslKeyPassHook_OpenSSL_type PQgetSSLKeyPassHook_OpenSSL(void);
```

## <span id="page-116-0"></span>**34.1.1. Connection Strings**

Several libpq functions parse a user-specified string to obtain connection parameters. There are two accepted formats for these strings: plain keyword/value strings and URIs. URIs generally follow [RFC](https://datatracker.ietf.org/doc/html/rfc3986) [3986](https://datatracker.ietf.org/doc/html/rfc3986)<sup>1</sup> , except that multi-host connection strings are allowed as further described below.