---
source: PostgreSQL 15 Reference
title: 00_Overview
---

You can use the following directives to compile code sections conditionally:

```
EXEC SQL ifdef name;
```

Checks a name and processes subsequent lines if name has been defined via EXEC SQL define name.

```
EXEC SQL ifndef name;
```

Checks a name and processes subsequent lines if name has *not* been defined via EXEC SQL define name.

```
EXEC SQL elif name;
```

Begins an optional alternative section after an EXEC SQL ifdef name or EXEC SQL ifndef name directive. Any number of elif sections can appear. Lines following an elif will be processed if name has been defined *and* no previous section of the same ifdef/ifndef...endif construct has been processed.

```
EXEC SQL else;
```

Begins an optional, final alternative section after an EXEC SQL ifdef name or EXEC SQL ifndef name directive. Subsequent lines will be processed if no previous section of the same ifdef/ifndef...endif construct has been processed.

```
EXEC SQL endif;
```

Ends an ifdef/ifndef...endif construct. Subsequent lines are processed normally.

ifdef/ifndef...endif constructs can be nested, up to 127 levels deep.

This example will compile exactly one of the three SET TIMEZONE commands:

```
EXEC SQL ifdef TZVAR;
EXEC SQL SET TIMEZONE TO TZVAR;
EXEC SQL elif TZNAME;
EXEC SQL SET TIMEZONE TO TZNAME;
EXEC SQL else;
EXEC SQL SET TIMEZONE TO 'GMT';
EXEC SQL endif;
```

# <span id="page-69-0"></span>**36.10. Processing Embedded SQL Programs**

Now that you have an idea how to form embedded SQL C programs, you probably want to know how to compile them. Before compiling you run the file through the embedded SQL C preprocessor, which converts the SQL statements you used to special function calls. After compiling, you must link with a special library that contains the needed functions. These functions fetch information from the arguments, perform the SQL command using the libpq interface, and put the result in the arguments specified for output.

The preprocessor program is called ecpg and is included in a normal PostgreSQL installation. Embedded SQL programs are typically named with an extension .pgc. If you have a program file called prog1.pgc, you can preprocess it by simply calling:

```
ecpg prog1.pgc
```

This will create a file called prog1.c. If your input files do not follow the suggested naming pattern, you can specify the output file explicitly using the -o option.

The preprocessed file can be compiled normally, for example:

```
cc -c prog1.c
```

The generated C source files include header files from the PostgreSQL installation, so if you installed PostgreSQL in a location that is not searched by default, you have to add an option such as -I/usr/ local/pgsql/include to the compilation command line.

To link an embedded SQL program, you need to include the libecpg library, like so:

```
cc -o myprog prog1.o prog2.o ... -lecpg
```

Again, you might have to add an option like -L/usr/local/pgsql/lib to that command line.

You can use pg\_config or pkg-config with package name libecpg to get the paths for your installation.

If you manage the build process of a larger project using make, it might be convenient to include the following implicit rule to your makefiles:

```
ECPG = ecpg
%.c: %.pgc
 $(ECPG) $<
```

The complete syntax of the ecpg command is detailed in ecpg.

The ecpg library is thread-safe by default. However, you might need to use some threading command-line options to compile your client code.

# <span id="page-70-0"></span>**36.11. Library Functions**

The libecpg library primarily contains "hidden" functions that are used to implement the functionality expressed by the embedded SQL commands. But there are some functions that can usefully be called directly. Note that this makes your code unportable.

• ECPGdebug(int on, FILE \*stream) turns on debug logging if called with the first argument non-zero. Debug logging is done on stream. The log contains all SQL statements with all the input variables inserted, and the results from the PostgreSQL server. This can be very useful when searching for errors in your SQL statements.

### **Note**

On Windows, if the ecpg libraries and an application are compiled with different flags, this function call will crash the application because the internal representation of the FILE pointers differ. Specifically, multithreaded/single-threaded, release/debug, and static/dynamic flags should be the same for the library and all applications using that library.

• ECPGget\_PGconn(const char \*connection\_name) returns the library database connection handle identified by the given name. If connection\_name is set to NULL, the current connection handle is returned. If no connection handle can be identified, the function returns NULL. The returned connection handle can be used to call any other functions from libpq, if necessary.

### **Note**

It is a bad idea to manipulate database connection handles made from ecpg directly with libpq routines.

- ECPGtransactionStatus(const char \*connection\_name) returns the current transaction status of the given connection identified by connection\_name. See Section 34.2 and libpq's PQtransactionStatus for details about the returned status codes.
- ECPGstatus(int lineno, const char\* connection\_name) returns true if you are connected to a database and false if not. connection\_name can be NULL if a single connection is being used.