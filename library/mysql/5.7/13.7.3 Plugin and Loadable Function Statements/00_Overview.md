---
source: MySQL 5.7 Reference
title: 00_Overview
---

## <span id="page-127-1"></span>**13.7.3.1 CREATE FUNCTION Statement for Loadable Functions**

```
CREATE [AGGREGATE] FUNCTION function_name
 RETURNS {STRING|INTEGER|REAL|DECIMAL}
 SONAME shared_library_name
```

This statement loads the loadable function named function\_name. (CREATE FUNCTION is also used to created stored functions; see Section 13.1.16, "CREATE PROCEDURE and CREATE FUNCTION Statements".)

A loadable function is a way to extend MySQL with a new function that works like a native (built-in) MySQL function such as ABS() or CONCAT(). See [Adding a Loadable Function](https://dev.mysql.com/doc/extending-mysql/5.7/en/adding-loadable-function.md).

function\_name is the name that should be used in SQL statements to invoke the function. The RETURNS clause indicates the type of the function's return value. DECIMAL is a legal value after RETURNS, but currently DECIMAL functions return string values and should be written like STRING functions.

The AGGREGATE keyword, if given, signifies that the function is an aggregate (group) function. An aggregate function works exactly like a native MySQL aggregate function such as SUM() or COUNT().

shared\_library\_name is the base name of the shared library file containing the code that implements the function. The file must be located in the plugin directory. This directory is given by the value of the plugin\_dir system variable. For more information, see Section 5.6.1, "Installing and Uninstalling Loadable Functions".

[CREATE FUNCTION](#page-127-1) requires the INSERT privilege for the mysql system database because it adds a row to the mysql.func system table to register the function.

During the normal startup sequence, the server loads functions registered in the mysql.func table. If the server is started with the --skip-grant-tables option, functions registered in the table are not loaded and are unavailable.

![](_page_128_Picture_2.jpeg)

#### **Note**

To upgrade the shared library associated with a loadable function, issue a [DROP](#page-128-1) [FUNCTION](#page-128-1) statement, upgrade the shared library, and then issue a [CREATE](#page-127-1) [FUNCTION](#page-127-1) statement. If you upgrade the shared library first and then use [DROP](#page-128-1) [FUNCTION](#page-128-1), the server may unexpectedly shut down.

## <span id="page-128-1"></span>**13.7.3.2 DROP FUNCTION Statement for Loadable Functions**

```
DROP FUNCTION [IF EXISTS] function_name
```

This statement drops the loadable function named function\_name. (DROP FUNCTION is also used to drop stored functions; see Section 13.1.27, "DROP PROCEDURE and DROP FUNCTION Statements".)

[DROP FUNCTION](#page-128-1) is the complement of [CREATE FUNCTION](#page-127-1). It requires the DELETE privilege for the mysql system database because it removes the row from the mysql.func system table that registers the function.

During the normal startup sequence, the server loads functions registered in the mysql.func table. Because [DROP FUNCTION](#page-128-1) removes the mysql.func row for the dropped function, the server does not load the function during subsequent restarts.

![](_page_128_Picture_10.jpeg)

#### **Note**

To upgrade the shared library associated with a loadable function, issue a [DROP](#page-128-1) [FUNCTION](#page-128-1) statement, upgrade the shared library, and then issue a [CREATE](#page-127-1) [FUNCTION](#page-127-1) statement. If you upgrade the shared library first and then use [DROP](#page-128-1) [FUNCTION](#page-128-1), the server may unexpectedly shut down.

# <span id="page-128-0"></span>**13.7.3.3 INSTALL PLUGIN Statement**

```
INSTALL PLUGIN plugin_name SONAME 'shared_library_name'
```

This statement installs a server plugin. It requires the INSERT privilege for the mysql.plugin system table because it adds a row to that table to register the plugin.

plugin\_name is the name of the plugin as defined in the plugin descriptor structure contained in the library file (see [Plugin Data Structures](https://dev.mysql.com/doc/extending-mysql/5.7/en/plugin-data-structures.md)). Plugin names are not case-sensitive. For maximal compatibility, plugin names should be limited to ASCII letters, digits, and underscore because they are used in C source files, shell command lines, M4 and Bourne shell scripts, and SQL environments.

shared\_library\_name is the name of the shared library that contains the plugin code. The name includes the file name extension (for example, libmyplugin.so, libmyplugin.dll, or libmyplugin.dylib).

The shared library must be located in the plugin directory (the directory named by the plugin\_dir system variable). The library must be in the plugin directory itself, not in a subdirectory. By default, plugin\_dir is the plugin directory under the directory named by the pkglibdir configuration variable, but it can be changed by setting the value of plugin\_dir at server startup. For example, set its value in a my.cnf file:

```
[mysqld]
plugin_dir=/path/to/plugin/directory
```

If the value of plugin\_dir is a relative path name, it is taken to be relative to the MySQL base directory (the value of the basedir system variable).

[INSTALL PLUGIN](#page-128-0) loads and initializes the plugin code to make the plugin available for use. A plugin is initialized by executing its initialization function, which handles any setup that the plugin must perform before it can be used. When the server shuts down, it executes the deinitialization function for each plugin that is loaded so that the plugin has a chance to perform any final cleanup.

[INSTALL PLUGIN](#page-128-0) also registers the plugin by adding a line that indicates the plugin name and library file name to the mysql.plugin system table. During the normal startup sequence, the server loads and initializes plugins registered in mysql.plugin. This means that a plugin is installed with [INSTALL](#page-128-0) [PLUGIN](#page-128-0) only once, not every time the server starts. If the server is started with the --skip-granttables option, plugins registered in the mysql.plugin table are not loaded and are unavailable.

A plugin library can contain multiple plugins. For each of them to be installed, use a separate [INSTALL](#page-128-0) [PLUGIN](#page-128-0) statement. Each statement names a different plugin, but all of them specify the same library name.

[INSTALL PLUGIN](#page-128-0) causes the server to read option (my.cnf) files just as during server startup. This enables the plugin to pick up any relevant options from those files. It is possible to add plugin options to an option file even before loading a plugin (if the loose prefix is used). It is also possible to uninstall a plugin, edit my.cnf, and install the plugin again. Restarting the plugin this way enables it to the new option values without a server restart.

For options that control individual plugin loading at server startup, see Section 5.5.1, "Installing and Uninstalling Plugins". If you need to load plugins for a single server startup when the --skip-granttables option is given (which tells the server not to read system tables), use the --plugin-load option. See Section 5.1.6, "Server Command Options".

To remove a plugin, use the [UNINSTALL PLUGIN](#page-129-0) statement.

For additional information about plugin loading, see Section 5.5.1, "Installing and Uninstalling Plugins".

To see what plugins are installed, use the [SHOW PLUGINS](#page-157-0) statement or query the INFORMATION\_SCHEMA the PLUGINS table.

If you recompile a plugin library and need to reinstall it, you can use either of the following methods:

- Use [UNINSTALL PLUGIN](#page-129-0) to uninstall all plugins in the library, install the new plugin library file in the plugin directory, and then use [INSTALL PLUGIN](#page-128-0) to install all plugins in the library. This procedure has the advantage that it can be used without stopping the server. However, if the plugin library contains many plugins, you must issue many [INSTALL PLUGIN](#page-128-0) and [UNINSTALL PLUGIN](#page-129-0) statements.
- Stop the server, install the new plugin library file in the plugin directory, and restart the server.

## <span id="page-129-0"></span>**13.7.3.4 UNINSTALL PLUGIN Statement**

UNINSTALL PLUGIN plugin\_name

This statement removes an installed server plugin. [UNINSTALL PLUGIN](#page-129-0) is the complement of [INSTALL PLUGIN](#page-128-0). It requires the DELETE privilege for the mysql.plugin system table because it removes the row from that table that registers the plugin.

plugin\_name must be the name of some plugin that is listed in the mysql.plugin table. The server executes the plugin's deinitialization function and removes the row for the plugin from the mysql.plugin system table, so that subsequent server restarts do not load and initialize the plugin. [UNINSTALL PLUGIN](#page-129-0) does not remove the plugin's shared library file.

You cannot uninstall a plugin if any table that uses it is open.

Plugin removal has implications for the use of associated tables. For example, if a full-text parser plugin is associated with a FULLTEXT index on the table, uninstalling the plugin makes the table unusable.

Any attempt to access the table results in an error. The table cannot even be opened, so you cannot drop an index for which the plugin is used. This means that uninstalling a plugin is something to do with care unless you do not care about the table contents. If you are uninstalling a plugin with no intention of reinstalling it later and you care about the table contents, you should dump the table with mysqldump and remove the WITH PARSER clause from the dumped CREATE TABLE statement so that you can reload the table later. If you do not care about the table, DROP TABLE can be used even if any plugins associated with the table are missing.

For additional information about plugin loading, see Section 5.5.1, "Installing and Uninstalling Plugins".

# <span id="page-130-1"></span>**13.7.4 SET Statements**

The [SET](#page-130-1) statement has several forms. Descriptions for those forms that are not associated with a specific server capability appear in subsections of this section:

- SET [var\\_name](#page-130-0) = value enables you to assign values to variables that affect the operation of the server or clients. See [Section 13.7.4.1, "SET Syntax for Variable Assignment".](#page-130-0)
- [SET CHARACTER SET](#page-133-0) and [SET NAMES](#page-134-1) assign values to character set and collation variables associated with the current connection to the server. See [Section 13.7.4.2, "SET CHARACTER SET](#page-133-0) [Statement",](#page-133-0) and [Section 13.7.4.3, "SET NAMES Statement".](#page-134-1)

Descriptions for the other forms appear elsewhere, grouped with other statements related to the capability they help implement:

- [SET PASSWORD](#page-114-1) assigns account passwords. See [Section 13.7.1.7, "SET PASSWORD Statement".](#page-114-1)
- [SET TRANSACTION ISOLATION LEVEL](#page-21-0) sets the isolation level for transaction processing. See [Section 13.3.6, "SET TRANSACTION Statement"](#page-21-0).

## <span id="page-130-0"></span>**13.7.4.1 SET Syntax for Variable Assignment**

```
SET variable = expr [, variable = expr] ...
variable: {
 user_var_name
 | param_name
 | local_var_name
 | {GLOBAL | @@GLOBAL.} system_var_name
 | [SESSION | @@SESSION. | @@] system_var_name
}
```

[SET](#page-130-0) syntax for variable assignment enables you to assign values to different types of variables that affect the operation of the server or clients:

- User-defined variables. See Section 9.4, "User-Defined Variables".
- Stored procedure and function parameters, and stored program local variables. See [Section 13.6.4,](#page-54-0) ["Variables in Stored Programs"](#page-54-0).
- System variables. See Section 5.1.7, "Server System Variables". System variables also can be set at server startup, as described in Section 5.1.8, "Using System Variables".

A [SET](#page-130-0) statement that assigns variable values is not written to the binary log, so in replication scenarios it affects only the host on which you execute it. To affect all replication hosts, execute the statement on each host.

The following sections describe [SET](#page-130-0) syntax for setting variables. They use the = assignment operator, but the := assignment operator is also permitted for this purpose.

• [User-Defined Variable Assignment](#page-131-0)

- [Parameter and Local Variable Assignment](#page-131-1)
- [System Variable Assignment](#page-131-2)
- [SET Error Handling](#page-132-0)
- [Multiple Variable Assignment](#page-133-1)
- [System Variable References in Expressions](#page-133-2)

### <span id="page-131-0"></span>**User-Defined Variable Assignment**

User-defined variables are created locally within a session and exist only within the context of that session; see Section 9.4, "User-Defined Variables".

A user-defined variable is written as @var\_name and is assigned an expression value as follows:

```
SET @var_name = expr;
```

### Examples:

```
SET @name = 43;
SET @total_tax = (SELECT SUM(tax) FROM taxable_transactions);
```

As demonstrated by those statements, expr can range from simple (a literal value) to more complex (the value returned by a scalar subquery).

The Performance Schema user\_variables\_by\_thread table contains information about userdefined variables. See Section 25.12.10, "Performance Schema User-Defined Variable Tables".

## <span id="page-131-1"></span>**Parameter and Local Variable Assignment**

[SET](#page-130-0) applies to parameters and local variables in the context of the stored object within which they are defined. The following procedure uses the increment procedure parameter and counter local variable:

```
CREATE PROCEDURE p(increment INT)
BEGIN
 DECLARE counter INT DEFAULT 0;
 WHILE counter < 10 DO
 -- ... do work ...
 SET counter = counter + increment;
 END WHILE;
END;
```

### <span id="page-131-2"></span>**System Variable Assignment**

The MySQL server maintains system variables that configure its operation. A system variable can have a global value that affects server operation as a whole, a session value that affects the current session, or both. Many system variables are dynamic and can be changed at runtime using the [SET](#page-130-0) statement to affect operation of the current server instance. (To make a global system variable setting permanent so that it applies across server restarts, you should also set it in an option file.)

If you change a session system variable, the value remains in effect within your session until you change the variable to a different value or the session ends. The change has no effect on other sessions.

If you change a global system variable, the value is remembered and used to initialize the session value for new sessions until you change the variable to a different value or the server exits. The change is visible to any client that accesses the global value. However, the change affects the corresponding session value only for clients that connect after the change. The global variable change does not affect

the session value for any current client sessions (not even the session within which the global value change occurs).

![](_page_132_Picture_2.jpeg)

### **Note**

Setting a global system variable value always requires special privileges. Setting a session system variable value normally requires no special privileges and can be done by any user, although there are exceptions. For more information, see Section 5.1.8.1, "System Variable Privileges".

The following discussion describes the syntax options for setting system variables:

• To assign a value to a global system variable, precede the variable name by the GLOBAL keyword or the @@GLOBAL. qualifier:

```
SET GLOBAL max_connections = 1000;
SET @@GLOBAL.max_connections = 1000;
```

• To assign a value to a session system variable, precede the variable name by the SESSION or LOCAL keyword, by the @@SESSION., @@LOCAL., or @@ qualifier, or by no keyword or no modifier at all:

```
SET SESSION sql_mode = 'TRADITIONAL';
SET LOCAL sql_mode = 'TRADITIONAL';
SET @@SESSION.sql_mode = 'TRADITIONAL';
SET @@LOCAL.sql_mode = 'TRADITIONAL';
SET @@sql_mode = 'TRADITIONAL';
SET sql_mode = 'TRADITIONAL';
```

A client can change its own session variables, but not those of any other client.

To set a global system variable value to the compiled-in MySQL default value or a session system variable to the current corresponding global value, set the variable to the value DEFAULT. For example, the following two statements are identical in setting the session value of max\_join\_size to the current global value:

```
SET @@SESSION.max_join_size = DEFAULT;
SET @@SESSION.max_join_size = @@GLOBAL.max_join_size;
```

To display system variable names and values:

- Use the [SHOW VARIABLES](#page-180-0) statement; see [Section 13.7.5.39, "SHOW VARIABLES Statement"](#page-180-0).
- Several Performance Schema tables provide system variable information. See Section 25.12.13, "Performance Schema System Variable Tables".

### <span id="page-132-0"></span>**SET Error Handling**

If any variable assignment in a [SET](#page-130-0) statement fails, the entire statement fails and no variables are changed.

[SET](#page-130-0) produces an error under the circumstances described here. Most of the examples show [SET](#page-130-0) statements that use keyword syntax (for example, GLOBAL or SESSION), but the principles are also true for statements that use the corresponding modifiers (for example, @@GLOBAL. or @@SESSION.).

• Use of [SET](#page-130-0) (any variant) to set a read-only variable:

```
mysql> SET GLOBAL version = 'abc';
ERROR 1238 (HY000): Variable 'version' is a read only variable
```

• Use of GLOBAL to set a variable that has only a session value:

```
mysql> SET GLOBAL sql_log_bin = ON;
ERROR 1231 (42000): Variable 'sql_log_bin' can't be
```

```
set to the value of 'ON'
```

• Use of SESSION to set a variable that has only a global value:

```
mysql> SET SESSION max_connections = 1000;
ERROR 1229 (HY000): Variable 'max_connections' is a
GLOBAL variable and should be set with SET GLOBAL
```

• Omission of GLOBAL to set a variable that has only a global value:

```
mysql> SET max_connections = 1000;
ERROR 1229 (HY000): Variable 'max_connections' is a
GLOBAL variable and should be set with SET GLOBAL
```

- The @@GLOBAL., @@SESSION., and @@ modifiers apply only to system variables. An error occurs for attempts to apply them to user-defined variables, stored procedure or function parameters, or stored program local variables.
- Not all system variables can be set to DEFAULT. In such cases, assigning DEFAULT results in an error.
- An error occurs for attempts to assign DEFAULT to user-defined variables, stored procedure or function parameters, or stored program local variables.

### <span id="page-133-1"></span>**Multiple Variable Assignment**

A [SET](#page-130-0) statement can contain multiple variable assignments, separated by commas. This statement assigns a value to a user-defined variable and a system variable:

```
SET @x = 1, SESSION sql_mode = '';
```

If you set multiple system variables in a single statement, the most recent GLOBAL or SESSION keyword in the statement is used for following assignments that have no keyword specified.

Examples of multiple-variable assignment:

```
SET GLOBAL sort_buffer_size = 1000000, SESSION sort_buffer_size = 1000000;
SET @@GLOBAL.sort_buffer_size = 1000000, @@LOCAL.sort_buffer_size = 1000000;
SET GLOBAL max_connections = 1000, sort_buffer_size = 1000000;
```

The @@GLOBAL., @@SESSION., and @@ modifiers apply only to the immediately following system variable, not any remaining system variables. This statement sets the sort\_buffer\_size global value to 50000 and the session value to 1000000:

```
SET @@GLOBAL.sort_buffer_size = 50000, sort_buffer_size = 1000000;
```

### <span id="page-133-2"></span>**System Variable References in Expressions**

To refer to the value of a system variable in expressions, use one of the @@-modifiers. For example, you can retrieve system variable values in a SELECT statement like this:

```
SELECT @@GLOBAL.sql_mode, @@SESSION.sql_mode, @@sql_mode;
```

![](_page_133_Picture_20.jpeg)

### **Note**

A reference to a system variable in an expression as @@var\_name (with @@ rather than @@GLOBAL. or @@SESSION.) returns the session value if it exists and the global value otherwise. This differs from SET @@var\_name = expr, which always refers to the session value.

# <span id="page-133-0"></span>**13.7.4.2 SET CHARACTER SET Statement**

```
SET {CHARACTER SET | CHARSET}
```

```
 {'charset_name' | DEFAULT}
```

This statement maps all strings sent between the server and the current client with the given mapping. SET CHARACTER SET sets three session system variables: character\_set\_client and character\_set\_results are set to the given character set, and character\_set\_connection to the value of character\_set\_database. See Section 10.4, "Connection Character Sets and Collations".

charset\_name may be quoted or unquoted.

The default character set mapping can be restored by using the value DEFAULT. The default depends on the server configuration.

Some character sets cannot be used as the client character set. Attempting to use them with [SET](#page-133-0) [CHARACTER SET](#page-133-0) produces an error. See Impermissible Client Character Sets.

# <span id="page-134-1"></span>**13.7.4.3 SET NAMES Statement**

```
SET NAMES {'charset_name'
 [COLLATE 'collation_name'] | DEFAULT}
```

This statement sets the three session system variables character\_set\_client, character\_set\_connection, and character\_set\_results to the given character set. Setting character\_set\_connection to charset\_name also sets collation\_connection to the default collation for charset\_name. See Section 10.4, "Connection Character Sets and Collations".

The optional COLLATE clause may be used to specify a collation explicitly. If given, the collation must one of the permitted collations for charset\_name.

charset\_name and collation\_name may be quoted or unquoted.

The default mapping can be restored by using a value of DEFAULT. The default depends on the server configuration.

Some character sets cannot be used as the client character set. Attempting to use them with [SET](#page-134-1) [NAMES](#page-134-1) produces an error. See Impermissible Client Character Sets.

# <span id="page-134-0"></span>**13.7.5 SHOW Statements**

[SHOW](#page-134-0) has many forms that provide information about databases, tables, columns, or status information about the server. This section describes those following:

```
SHOW {BINARY | MASTER} LOGS
SHOW BINLOG EVENTS [IN 'log_name'] [FROM pos] [LIMIT [offset,] row_count]
SHOW {CHARACTER SET | CHARSET} [like_or_where]
SHOW COLLATION [like_or_where]
SHOW [FULL] COLUMNS FROM tbl_name [FROM db_name] [like_or_where]
SHOW CREATE DATABASE db_name
SHOW CREATE EVENT event_name
SHOW CREATE FUNCTION func_name
SHOW CREATE PROCEDURE proc_name
SHOW CREATE TABLE tbl_name
SHOW CREATE TRIGGER trigger_name
SHOW CREATE VIEW view_name
SHOW DATABASES [like_or_where]
SHOW ENGINE engine_name {STATUS | MUTEX}
SHOW [STORAGE] ENGINES
SHOW ERRORS [LIMIT [offset,] row_count]
SHOW EVENTS
SHOW FUNCTION CODE func_name
SHOW FUNCTION STATUS [like_or_where]
SHOW GRANTS FOR user
SHOW INDEX FROM tbl_name [FROM db_name]
```

```
SHOW MASTER STATUS
SHOW OPEN TABLES [FROM db_name] [like_or_where]
SHOW PLUGINS
SHOW PROCEDURE CODE proc_name
SHOW PROCEDURE STATUS [like_or_where]
SHOW PRIVILEGES
SHOW [FULL] PROCESSLIST
SHOW PROFILE [types] [FOR QUERY n] [OFFSET n] [LIMIT n]
SHOW PROFILES
SHOW RELAYLOG EVENTS [IN 'log_name'] [FROM pos] [LIMIT [offset,] row_count]
SHOW SLAVE HOSTS
SHOW SLAVE STATUS [FOR CHANNEL channel]
SHOW [GLOBAL | SESSION] STATUS [like_or_where]
SHOW TABLE STATUS [FROM db_name] [like_or_where]
SHOW [FULL] TABLES [FROM db_name] [like_or_where]
SHOW TRIGGERS [FROM db_name] [like_or_where]
SHOW [GLOBAL | SESSION] VARIABLES [like_or_where]
SHOW WARNINGS [LIMIT [offset,] row_count]
like_or_where: {
 LIKE 'pattern'
 | WHERE expr
}
```

If the syntax for a given [SHOW](#page-134-0) statement includes a LIKE 'pattern' part, 'pattern' is a string that can contain the SQL % and \_ wildcard characters. The pattern is useful for restricting statement output to matching values.

Several [SHOW](#page-134-0) statements also accept a WHERE clause that provides more flexibility in specifying which rows to display. See Section 24.8, "Extensions to SHOW Statements".

Many MySQL APIs (such as PHP) enable you to treat the result returned from a [SHOW](#page-134-0) statement as you would a result set from a SELECT; see Chapter 27, Connectors and APIs, or your API documentation for more information. In addition, you can work in SQL with results from queries on tables in the INFORMATION\_SCHEMA database, which you cannot easily do with results from [SHOW](#page-134-0) statements. See Chapter 24, INFORMATION\_SCHEMA Tables.

## <span id="page-135-0"></span>**13.7.5.1 SHOW BINARY LOGS Statement**

```
SHOW BINARY LOGS
SHOW MASTER LOGS
```

Lists the binary log files on the server. This statement is used as part of the procedure described in [Section 13.4.1.1, "PURGE BINARY LOGS Statement",](#page-29-0) that shows how to determine which logs can be purged. A user with the SUPER or REPLICATION CLIENT privilege may execute this statement.

```
mysql> SHOW BINARY LOGS;
+---------------+-----------+
| Log_name | File_size |
+---------------+-----------+
| binlog.000015 | 724935 |
| binlog.000016 | 733481 |
+---------------+-----------+
```

[SHOW MASTER LOGS](#page-135-0) is equivalent to [SHOW BINARY LOGS](#page-135-0).

# <span id="page-135-1"></span>**13.7.5.2 SHOW BINLOG EVENTS Statement**

```
SHOW BINLOG EVENTS
 [IN 'log_name']
 [FROM pos]
 [LIMIT [offset,] row_count]
```

Shows the events in the binary log. If you do not specify 'log\_name', the first binary log is displayed. [SHOW BINLOG EVENTS](#page-135-1) requires the REPLICATION SLAVE privilege.

The LIMIT clause has the same syntax as for the SELECT statement. See Section 13.2.9, "SELECT Statement".

![](_page_136_Picture_2.jpeg)

### **Note**

Issuing a [SHOW BINLOG EVENTS](#page-135-1) with no LIMIT clause could start a very timeand resource-consuming process because the server returns to the client the complete contents of the binary log (which includes all statements executed by the server that modify data). As an alternative to [SHOW BINLOG EVENTS](#page-135-1), use the mysqlbinlog utility to save the binary log to a text file for later examination and analysis. See Section 4.6.7, "mysqlbinlog — Utility for Processing Binary Log Files".

[SHOW BINLOG EVENTS](#page-135-1) displays the following fields for each event in the binary log:

• Log\_name

The name of the file that is being listed.

• Pos

The position at which the event occurs.

• Event\_type

An identifier that describes the event type.

• Server\_id

The server ID of the server on which the event originated.

• End\_log\_pos

The position at which the next event begins, which is equal to Pos plus the size of the event.

• Info

More detailed information about the event type. The format of this information depends on the event type.

![](_page_136_Picture_18.jpeg)

### **Note**

Some events relating to the setting of user and system variables are not included in the output from [SHOW BINLOG EVENTS](#page-135-1). To get complete coverage of events within a binary log, use mysqlbinlog.

![](_page_136_Picture_21.jpeg)

# **Note**

[SHOW BINLOG EVENTS](#page-135-1) does not work with relay log files. You can use [SHOW](#page-165-0) [RELAYLOG EVENTS](#page-165-0) for this purpose.

## <span id="page-136-0"></span>**13.7.5.3 SHOW CHARACTER SET Statement**

```
SHOW {CHARACTER SET | CHARSET}
 [LIKE 'pattern' | WHERE expr]
```

The [SHOW CHARACTER SET](#page-136-0) statement shows all available character sets. The LIKE clause, if present, indicates which character set names to match. The WHERE clause can be given to select rows using more general conditions, as discussed in Section 24.8, "Extensions to SHOW Statements". For example:

```
mysql> SHOW CHARACTER SET LIKE 'latin%';
+---------+-----------------------------+-------------------+--------+
```

| +++++<br>  latin1   cp1252 West European<br>  latin1_swedish_ci  <br>1                                                                                                                                       |
|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| latin2   ISO 8859-2 Central European   latin2_general_ci  <br>1  <br>  latin5   ISO 8859-9 Turkish<br>  latin5_turkish_ci  <br>1  <br>  latin7   ISO 8859-13 Baltic<br>  latin7_general_ci  <br>1  <br>+++++ |

[SHOW CHARACTER SET](#page-136-0) output has these columns:

• Charset

The character set name.

• Description

A description of the character set.

• Default collation

The default collation for the character set.

• Maxlen

The maximum number of bytes required to store one character.

The filename character set is for internal use only; consequently, [SHOW CHARACTER SET](#page-136-0) does not display it.

Character set information is also available from the INFORMATION\_SCHEMA CHARACTER\_SETS table.

## <span id="page-137-0"></span>**13.7.5.4 SHOW COLLATION Statement**

```
SHOW COLLATION
 [LIKE 'pattern' | WHERE expr]
```

This statement lists collations supported by the server. By default, the output from [SHOW COLLATION](#page-137-0) includes all available collations. The LIKE clause, if present, indicates which collation names to match. The WHERE clause can be given to select rows using more general conditions, as discussed in Section 24.8, "Extensions to SHOW Statements". For example:

```
mysql> SHOW COLLATION WHERE Charset = 'latin1';
+-------------------+---------+----+---------+----------+---------+
| Collation | Charset | Id | Default | Compiled | Sortlen |
+-------------------+---------+----+---------+----------+---------+
| latin1_german1_ci | latin1 | 5 | | Yes | 1 |
| latin1_swedish_ci | latin1 | 8 | Yes | Yes | 1 |
| latin1_danish_ci | latin1 | 15 | | Yes | 1 |
| latin1_german2_ci | latin1 | 31 | | Yes | 2 |
| latin1_bin | latin1 | 47 | | Yes | 1 |
| latin1_general_ci | latin1 | 48 | | Yes | 1 |
| latin1_general_cs | latin1 | 49 | | Yes | 1 |
| latin1_spanish_ci | latin1 | 94 | | Yes | 1 |
+-------------------+---------+----+---------+----------+---------+
```

[SHOW COLLATION](#page-137-0) output has these columns:

• Collation

The collation name.

• Charset

The name of the character set with which the collation is associated.

• Id

The collation ID.

• Default

Whether the collation is the default for its character set.

• Compiled

Whether the character set is compiled into the server.

• Sortlen

This is related to the amount of memory required to sort strings expressed in the character set.

To see the default collation for each character set, use the following statement. Default is a reserved word, so to use it as an identifier, it must be quoted as such:

```
mysql> SHOW COLLATION WHERE `Default` = 'Yes';
+---------------------+----------+----+---------+----------+---------+
| Collation | Charset | Id | Default | Compiled | Sortlen |
+---------------------+----------+----+---------+----------+---------+
| big5_chinese_ci | big5 | 1 | Yes | Yes | 1 |
| dec8_swedish_ci | dec8 | 3 | Yes | Yes | 1 |
| cp850_general_ci | cp850 | 4 | Yes | Yes | 1 |
| hp8_english_ci | hp8 | 6 | Yes | Yes | 1 |
| koi8r_general_ci | koi8r | 7 | Yes | Yes | 1 |
| latin1_swedish_ci | latin1 | 8 | Yes | Yes | 1 |
...
```

Collation information is also available from the INFORMATION\_SCHEMA COLLATIONS table. See Section 24.3.3, "The INFORMATION\_SCHEMA COLLATIONS Table".

## <span id="page-138-0"></span>**13.7.5.5 SHOW COLUMNS Statement**

```
SHOW [FULL] {COLUMNS | FIELDS}
 {FROM | IN} tbl_name
 [{FROM | IN} db_name]
 [LIKE 'pattern' | WHERE expr]
```

[SHOW COLUMNS](#page-138-0) displays information about the columns in a given table. It also works for views. [SHOW](#page-138-0) [COLUMNS](#page-138-0) displays information only for those columns for which you have some privilege.

```
mysql> SHOW COLUMNS FROM City;
+-------------+----------+------+-----+---------+----------------+
| Field | Type | Null | Key | Default | Extra |
+-------------+----------+------+-----+---------+----------------+
| ID | int(11) | NO | PRI | NULL | auto_increment |
| Name | char(35) | NO | | | |
| CountryCode | char(3) | NO | MUL | | |
| District | char(20) | NO | | | |
| Population | int(11) | NO | | 0 | |
+-------------+----------+------+-----+---------+----------------+
```

An alternative to tbl\_name FROM db\_name syntax is db\_name.tbl\_name. These two statements are equivalent:

```
SHOW COLUMNS FROM mytable FROM mydb;
SHOW COLUMNS FROM mydb.mytable;
```

The optional FULL keyword causes the output to include the column collation and comments, as well as the privileges you have for each column.

The LIKE clause, if present, indicates which column names to match. The WHERE clause can be given to select rows using more general conditions, as discussed in Section 24.8, "Extensions to SHOW Statements".

The data types may differ from what you expect them to be based on a CREATE TABLE statement because MySQL sometimes changes data types when you create or alter a table. The conditions under which this occurs are described in Section 13.1.18.6, "Silent Column Specification Changes".

[SHOW COLUMNS](#page-138-0) displays the following values for each table column:

• Field

The column name.

• Type

The column data type.

• Collation

The collation for nonbinary string columns, or NULL for other columns. This value is displayed only if you use the FULL keyword.

• Null

The column nullability. The value is YES if NULL values can be stored in the column, NO if not.

• Key

Whether the column is indexed:

- If Key is empty, the column either is not indexed or is indexed only as a secondary column in a multiple-column, nonunique index.
- If Key is PRI, the column is a PRIMARY KEY or is one of the columns in a multiple-column PRIMARY KEY.
- If Key is UNI, the column is the first column of a UNIQUE index. (A UNIQUE index permits multiple NULL values, but you can tell whether the column permits NULL by checking the Null field.)
- If Key is MUL, the column is the first column of a nonunique index in which multiple occurrences of a given value are permitted within the column.

If more than one of the Key values applies to a given column of a table, Key displays the one with the highest priority, in the order PRI, UNI, MUL.

A UNIQUE index may be displayed as PRI if it cannot contain NULL values and there is no PRIMARY KEY in the table. A UNIQUE index may display as MUL if several columns form a composite UNIQUE index; although the combination of the columns is unique, each column can still hold multiple occurrences of a given value.

• Default

The default value for the column. This is NULL if the column has an explicit default of NULL, or if the column definition includes no DEFAULT clause.

• Extra

Any additional information that is available about a given column. The value is nonempty in these cases:

- auto\_increment for columns that have the AUTO\_INCREMENT attribute.
- on update CURRENT\_TIMESTAMP for TIMESTAMP or DATETIME columns that have the ON UPDATE CURRENT\_TIMESTAMP attribute.
- VIRTUAL GENERATED or STORED GENERATED for generated columns.

• Privileges

The privileges you have for the column. This value is displayed only if you use the FULL keyword.

• Comment

Any comment included in the column definition. This value is displayed only if you use the FULL keyword.

Table column information is also available from the INFORMATION\_SCHEMA COLUMNS table. See Section 24.3.5, "The INFORMATION SCHEMA COLUMNS Table".

You can list a table's columns with the mysqlshow db name tbl name command.

The DESCRIBE statement provides information similar to SHOW COLUMNS. See Section 13.8.1, "DESCRIBE Statement".

The SHOW CREATE TABLE, SHOW TABLE STATUS, and SHOW INDEX statements also provide information about tables. See Section 13.7.5, "SHOW Statements".

#### <span id="page-140-0"></span>13.7.5.6 SHOW CREATE DATABASE Statement

```
SHOW CREATE {DATABASE | SCHEMA} [IF NOT EXISTS] db name
```

Shows the CREATE DATABASE statement that creates the named database. If the SHOW statement includes an IF NOT EXISTS clause, the output too includes such a clause. SHOW CREATE SCHEMA is a synonym for SHOW CREATE DATABASE.

```
mysql> SHOW CREATE DATABASE test\G
********************************
  Database: test
Create Database: CREATE DATABASE `test`
```

SHOW CREATE DATABASE quotes table and column names according to the value of the sql quote show create option. See Section 5.1.7, "Server System Variables".

### <span id="page-140-1"></span>13.7.5.7 SHOW CREATE EVENT Statement

```
SHOW CREATE EVENT event_name
```

This statement displays the CREATE EVENT statement needed to re-create a given event. It requires the EVENT privilege for the database from which the event is to be shown. For example (using the same event e daily defined and then altered in Section 13.7.5.18, "SHOW EVENTS Statement"):

```
mysql> SHOW CREATE EVENT myschema.e_daily\G

***********************************
```

```
 clears the table each day'
 DO BEGIN
 INSERT INTO site_activity.totals (time, total)
 SELECT CURRENT_TIMESTAMP, COUNT(*)
 FROM site_activity.sessions;
 DELETE FROM site_activity.sessions;
 END
character_set_client: utf8
collation_connection: utf8_general_ci
 Database Collation: latin1_swedish_ci
```

character\_set\_client is the session value of the character\_set\_client system variable when the event was created. collation\_connection is the session value of the collation\_connection system variable when the event was created. Database Collation is the collation of the database with which the event is associated.

The output reflects the current status of the event (ENABLE) rather than the status with which it was created.

# <span id="page-141-1"></span>**13.7.5.8 SHOW CREATE FUNCTION Statement**

```
SHOW CREATE FUNCTION func_name
```

This statement is similar to [SHOW CREATE PROCEDURE](#page-141-0) but for stored functions. See [Section 13.7.5.9,](#page-141-0) ["SHOW CREATE PROCEDURE Statement"](#page-141-0).

# <span id="page-141-0"></span>**13.7.5.9 SHOW CREATE PROCEDURE Statement**

```
SHOW CREATE PROCEDURE proc_name
```

This statement is a MySQL extension. It returns the exact string that can be used to re-create the named stored procedure. A similar statement, [SHOW CREATE FUNCTION](#page-141-1), displays information about stored functions (see [Section 13.7.5.8, "SHOW CREATE FUNCTION Statement"](#page-141-1)).

To use either statement, you must be the user named in the routine DEFINER clause or have SELECT access to the mysql.proc table. If you do not have privileges for the routine itself, the value displayed for the Create Procedure or Create Function column is NULL.

```
mysql> SHOW CREATE PROCEDURE test.citycount\G
*************************** 1. row ***************************
 Procedure: citycount
 sql_mode: ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,
 NO_ZERO_IN_DATE,NO_ZERO_DATE,
 ERROR_FOR_DIVISION_BY_ZERO,
 NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION
 Create Procedure: CREATE DEFINER=`me`@`localhost`
 PROCEDURE `citycount`(IN country CHAR(3), OUT cities INT)
 BEGIN
 SELECT COUNT(*) INTO cities FROM world.city
 WHERE CountryCode = country;
 END
character_set_client: utf8
collation_connection: utf8_general_ci
 Database Collation: latin1_swedish_ci
mysql> SHOW CREATE FUNCTION test.hello\G
*************************** 1. row ***************************
 Function: hello
 sql_mode: ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,
 NO_ZERO_IN_DATE,NO_ZERO_DATE,
 ERROR_FOR_DIVISION_BY_ZERO,
 NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION
 Create Function: CREATE DEFINER=`me`@`localhost`
 FUNCTION `hello`(s CHAR(20))
 RETURNS char(50) CHARSET latin1
 DETERMINISTIC
 RETURN CONCAT('Hello, ',s,'!')
```

```
character_set_client: utf8
collation_connection: utf8_general_ci
 Database Collation: latin1_swedish_ci
```

character\_set\_client is the session value of the character\_set\_client system variable when the routine was created. collation\_connection is the session value of the collation\_connection system variable when the routine was created. Database Collation is the collation of the database with which the routine is associated.

# <span id="page-142-0"></span>**13.7.5.10 SHOW CREATE TABLE Statement**

```
SHOW CREATE TABLE tbl_name
```

Shows the CREATE TABLE statement that creates the named table. To use this statement, you must have some privilege for the table. This statement also works with views.

```
mysql> SHOW CREATE TABLE t\G
*************************** 1. row ***************************
 Table: t
Create Table: CREATE TABLE `t` (
 `id` int(11) NOT NULL AUTO_INCREMENT,
 `s` char(60) DEFAULT NULL,
 PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
```

[SHOW CREATE TABLE](#page-142-0) quotes table and column names according to the value of the sql\_quote\_show\_create option. See Section 5.1.7, "Server System Variables".

When altering the storage engine of a table, table options that are not applicable to the new storage engine are retained in the table definition to enable reverting the table with its previously defined options to the original storage engine, if necessary. For example, when changing the storage engine from InnoDB to MyISAM, InnoDB-specific options such as ROW\_FORMAT=COMPACT are retained.

```
mysql> CREATE TABLE t1 (c1 INT PRIMARY KEY) ROW_FORMAT=COMPACT ENGINE=InnoDB;
mysql> ALTER TABLE t1 ENGINE=MyISAM;
mysql> SHOW CREATE TABLE t1\G
*************************** 1. row ***************************
 Table: t1
Create Table: CREATE TABLE `t1` (
 `c1` int(11) NOT NULL,
 PRIMARY KEY (`c1`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 ROW_FORMAT=COMPACT
```

When creating a table with strict mode disabled, the storage engine's default row format is used if the specified row format is not supported. The actual row format of the table is reported in the Row\_format column in response to [SHOW TABLE STATUS](#page-175-0). [SHOW CREATE TABLE](#page-142-0) shows the row format that was specified in the CREATE TABLE statement.

## <span id="page-142-1"></span>**13.7.5.11 SHOW CREATE TRIGGER Statement**

```
SHOW CREATE TRIGGER trigger_name
```

This statement shows the CREATE TRIGGER statement that creates the named trigger. This statement requires the TRIGGER privilege for the table associated with the trigger.

```
mysql> SHOW CREATE TRIGGER ins_sum\G
*************************** 1. row ***************************
 Trigger: ins_sum
 sql_mode: ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,
 NO_ZERO_IN_DATE,NO_ZERO_DATE,
 ERROR_FOR_DIVISION_BY_ZERO,
 NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION
SQL Original Statement: CREATE DEFINER=`me`@`localhost` TRIGGER ins_sum
 BEFORE INSERT ON account
 FOR EACH ROW SET @sum = @sum + NEW.amount
```

```
 character_set_client: utf8
 collation_connection: utf8_general_ci
 Database Collation: latin1_swedish_ci
 Created: 2018-08-08 10:10:07.90
```

[SHOW CREATE TRIGGER](#page-142-1) output has these columns:

- Trigger: The trigger name.
- sql\_mode: The SQL mode in effect when the trigger executes.
- SQL Original Statement: The CREATE TRIGGER statement that defines the trigger.
- character\_set\_client: The session value of the character\_set\_client system variable when the trigger was created.
- collation\_connection: The session value of the collation\_connection system variable when the trigger was created.
- Database Collation: The collation of the database with which the trigger is associated.
- Created: The date and time when the trigger was created. This is a TIMESTAMP(2) value (with a fractional part in hundredths of seconds) for triggers created in MySQL 5.7.2 or later, NULL for triggers created prior to 5.7.2.

Trigger information is also available from the INFORMATION\_SCHEMA TRIGGERS table. See Section 24.3.29, "The INFORMATION\_SCHEMA TRIGGERS Table".

# <span id="page-143-1"></span>**13.7.5.12 SHOW CREATE USER Statement**

```
SHOW CREATE USER user
```

This statement shows the [CREATE USER](#page-95-0) statement that creates the named user. An error occurs if the user does not exist. The statement requires the SELECT privilege for the mysql system database, except to display information for the current user.

To name the account, use the format described in Section 6.2.4, "Specifying Account Names". The host name part of the account name, if omitted, defaults to '%'. It is also possible to specify CURRENT\_USER or CURRENT\_USER() to refer to the account associated with the current session.

```
mysql> SHOW CREATE USER 'root'@'localhost'\G
*************************** 1. row ***************************
CREATE USER for root@localhost: CREATE USER 'root'@'localhost'
IDENTIFIED WITH 'mysql_native_password'
AS '*2470C0C06DEE42FD1618BB99005ADCA2EC9D1E19'
REQUIRE NONE PASSWORD EXPIRE DEFAULT ACCOUNT UNLOCK
```

The output format is affected by the setting of the log\_builtin\_as\_identified\_by\_password system variable.

To display the privileges granted to an account, use the [SHOW GRANTS](#page-154-0) statement. See [Section 13.7.5.21, "SHOW GRANTS Statement".](#page-154-0)

# <span id="page-143-0"></span>**13.7.5.13 SHOW CREATE VIEW Statement**

```
SHOW CREATE VIEW view_name
```

This statement shows the CREATE VIEW statement that creates the named view.

```
mysql> SHOW CREATE VIEW v\G
*************************** 1. row ***************************
 View: v
 Create View: CREATE ALGORITHM=UNDEFINED
```

```
 DEFINER=`bob`@`localhost`
 SQL SECURITY DEFINER VIEW
 `v` AS select 1 AS `a`,2 AS `b`
character_set_client: utf8
collation_connection: utf8_general_ci
```

character\_set\_client is the session value of the character\_set\_client system variable when the view was created. collation\_connection is the session value of the collation\_connection system variable when the view was created.

Use of [SHOW CREATE VIEW](#page-143-0) requires the SHOW VIEW privilege, and the SELECT privilege for the view in question.

View information is also available from the INFORMATION\_SCHEMA VIEWS table. See Section 24.3.31, "The INFORMATION\_SCHEMA VIEWS Table".

MySQL lets you use different sql\_mode settings to tell the server the type of SQL syntax to support. For example, you might use the ANSI SQL mode to ensure MySQL correctly interprets the standard SQL concatenation operator, the double bar (||), in your queries. If you then create a view that concatenates items, you might worry that changing the sql\_mode setting to a value different from ANSI could cause the view to become invalid. But this is not the case. No matter how you write out a view definition, MySQL always stores it the same way, in a canonical form. Here is an example that shows how the server changes a double bar concatenation operator to a CONCAT() function:

```
mysql> SET sql_mode = 'ANSI';
Query OK, 0 rows affected (0.00 sec)
mysql> CREATE VIEW test.v AS SELECT 'a' || 'b' as col1;
Query OK, 0 rows affected (0.01 sec)
mysql> SHOW CREATE VIEW test.v\G
*************************** 1. row ***************************
 View: v
 Create View: CREATE VIEW "v" AS select concat('a','b') AS "col1"
...
1 row in set (0.00 sec)
```

The advantage of storing a view definition in canonical form is that changes made later to the value of sql\_mode does not affect the results from the view. However an additional consequence is that comments prior to SELECT are stripped from the definition by the server.

# <span id="page-144-0"></span>**13.7.5.14 SHOW DATABASES Statement**

```
SHOW {DATABASES | SCHEMAS}
 [LIKE 'pattern' | WHERE expr]
```

[SHOW DATABASES](#page-144-0) lists the databases on the MySQL server host. [SHOW SCHEMAS](#page-144-0) is a synonym for [SHOW DATABASES](#page-144-0). The LIKE clause, if present, indicates which database names to match. The WHERE clause can be given to select rows using more general conditions, as discussed in Section 24.8, "Extensions to SHOW Statements".

You see only those databases for which you have some kind of privilege, unless you have the global [SHOW DATABASES](#page-144-0) privilege. You can also get this list using the mysqlshow command.

If the server was started with the --skip-show-database option, you cannot use this statement at all unless you have the SHOW DATABASES privilege.

MySQL implements databases as directories in the data directory, so this statement simply lists directories in that location. However, the output may include names of directories that do not correspond to actual databases.

Database information is also available from the INFORMATION\_SCHEMA SCHEMATA table. See Section 24.3.22, "The INFORMATION\_SCHEMA SCHEMATA Table".

![](_page_145_Picture_1.jpeg)

#### **Caution**

Because a global privilege is considered a privilege for all databases, any global privilege enables a user to see all database names with [SHOW DATABASES](#page-144-0) or by examining the INFORMATION\_SCHEMA SCHEMATA table.

# <span id="page-145-0"></span>**13.7.5.15 SHOW ENGINE Statement**

```
SHOW ENGINE engine_name {STATUS | MUTEX}
```

[SHOW ENGINE](#page-145-0) displays operational information about a storage engine. It requires the PROCESS privilege. The statement has these variants:

```
SHOW ENGINE INNODB STATUS
SHOW ENGINE INNODB MUTEX
SHOW ENGINE PERFORMANCE_SCHEMA STATUS
```

[SHOW ENGINE INNODB STATUS](#page-145-0) displays extensive information from the standard InnoDB Monitor about the state of the InnoDB storage engine. For information about the standard monitor and other InnoDB Monitors that provide information about InnoDB processing, see Section 14.18, "InnoDB Monitors".

[SHOW ENGINE INNODB MUTEX](#page-145-0) displays InnoDB mutex and rw-lock statistics.

![](_page_145_Picture_10.jpeg)

#### **Note**

InnoDB mutexes and rwlocks can also be monitored using Performance Schema tables. See Section 14.17.2, "Monitoring InnoDB Mutex Waits Using Performance Schema".

[SHOW ENGINE INNODB MUTEX](#page-145-0) output was removed in MySQL 5.7.2. It was revised and reintroduced in MySQL 5.7.8.

In MySQL 5.7.8, mutex statistics collection is configured dynamically using the following options:

• To enable the collection of mutex statistics, run:

```
SET GLOBAL innodb_monitor_enable='latch';
```

• To reset mutex statistics, run:

```
SET GLOBAL innodb_monitor_reset='latch';
```

• To disable the collection of mutex statistics, run:

```
SET GLOBAL innodb_monitor_disable='latch';
```

Collection of mutex statistics for [SHOW ENGINE INNODB MUTEX](#page-145-0) can also be enabled by setting innodb\_monitor\_enable='all', or disabled by setting innodb\_monitor\_disable='all'.

[SHOW ENGINE INNODB MUTEX](#page-145-0) output has these columns:

• Type

Always InnoDB.

• Name

Prior to MySQL 5.7.8, the Name field reports the source file where the mutex is implemented, and the line number in the file where the mutex is created. The line number is specific to your version of MySQL. As of MySQL 5.7.8, only the mutex name is reported. File name and line number are still reported for rwlocks.

• Status

The mutex status.

Prior to MySQL 5.7.8, the Status field displays several values if WITH\_DEBUG was defined at MySQL compilation time. If WITH\_DEBUG was not defined, the statement displays only the os\_waits value. In the latter case (without WITH\_DEBUG), the information on which the output is based is insufficient to distinguish regular mutexes and mutexes that protect rwlocks (which permit multiple readers or a single writer). Consequently, the output may appear to contain multiple rows for the same mutex. Pre-MySQL 5.7.8 Status field values include:

- count indicates how many times the mutex was requested.
- spin\_waits indicates how many times the spinlock had to run.
- spin\_rounds indicates the number of spinlock rounds. (spin\_rounds divided by spin\_waits provides the average round count.)
- os\_waits indicates the number of operating system waits. This occurs when the spinlock did not work (the mutex was not locked during the spinlock and it was necessary to yield to the operating system and wait).
- os\_yields indicates the number of times a thread trying to lock a mutex gave up its timeslice and yielded to the operating system (on the presumption that permitting other threads to run frees the mutex so that it can be locked).
- os\_wait\_times indicates the amount of time (in ms) spent in operating system waits. In MySQL 5.7 timing is disabled and this value is always 0.

As of MySQL 5.7.8, the Status field reports the number of spins, waits, and calls. Statistics for lowlevel operating system mutexes, which are implemented outside of InnoDB, are not reported.

- spins indicates the number of spins.
- waits indicates the number of mutex waits.
- calls indicates how many times the mutex was requested.

SHOW ENGINE INNODB MUTEX does not list mutexes and rw-locks for each buffer pool block, as the amount of output would be overwhelming on systems with a large buffer pool. SHOW ENGINE INNODB MUTEX does, however, print aggregate BUF\_BLOCK\_MUTEX spin, wait, and call values for buffer pool block mutexes and rw-locks. SHOW ENGINE INNODB MUTEX also does not list any mutexes or rwlocks that have never been waited on (os\_waits=0). Thus, SHOW ENGINE INNODB MUTEX only displays information about mutexes and rw-locks outside of the buffer pool that have caused at least one OS-level wait.

Use [SHOW ENGINE PERFORMANCE\\_SCHEMA STATUS](#page-145-0) to inspect the internal operation of the Performance Schema code:

```
mysql> SHOW ENGINE PERFORMANCE_SCHEMA STATUS\G
...
*************************** 3. row ***************************
 Type: performance_schema
 Name: events_waits_history.size
Status: 76
*************************** 4. row ***************************
 Type: performance_schema
 Name: events_waits_history.count
Status: 10000
*************************** 5. row ***************************
 Type: performance_schema
 Name: events_waits_history.memory
Status: 760000
...
*************************** 57. row ***************************
```

```
 Type: performance_schema
 Name: performance_schema.memory
Status: 26459600
...
```

This statement is intended to help the DBA understand the effects that different Performance Schema options have on memory requirements.

Name values consist of two parts, which name an internal buffer and a buffer attribute, respectively. Interpret buffer names as follows:

- An internal buffer that is not exposed as a table is named within parentheses. Examples: (pfs\_cond\_class).size, (pfs\_mutex\_class).memory.
- An internal buffer that is exposed as a table in the performance\_schema database is named after the table, without parentheses. Examples: events\_waits\_history.size, mutex\_instances.count.
- A value that applies to the Performance Schema as a whole begins with performance\_schema. Example: performance\_schema.memory.

Buffer attributes have these meanings:

- size is the size of the internal record used by the implementation, such as the size of a row in a table. size values cannot be changed.
- count is the number of internal records, such as the number of rows in a table. count values can be changed using Performance Schema configuration options.
- For a table, tbl\_name.memory is the product of size and count. For the Performance Schema as a whole, performance\_schema.memory is the sum of all the memory used (the sum of all other memory values).

In some cases, there is a direct relationship between a Performance Schema configuration parameter and a SHOW ENGINE value. For example, events\_waits\_history\_long.count corresponds to performance\_schema\_events\_waits\_history\_long\_size. In other cases, the relationship is more complex. For example, events\_waits\_history.count corresponds to performance\_schema\_events\_waits\_history\_size (the number of rows per thread) multiplied by performance\_schema\_max\_thread\_instances ( the number of threads).

**SHOW ENGINE NDB STATUS.** If the server has the NDB storage engine enabled, SHOW ENGINE NDB STATUS displays cluster status information such as the number of connected data nodes, the cluster connectstring, and cluster binary log epochs, as well as counts of various Cluster API objects created by the MySQL Server when connected to the cluster. Sample output from this statement is shown here:

```
mysql> SHOW ENGINE NDB STATUS;
+------------+-----------------------+--------------------------------------------------+
| Type | Name | Status |
+------------+-----------------------+--------------------------------------------------+
| ndbcluster | connection | cluster_node_id=7,
 connected_host=198.51.100.103, connected_port=1186, number_of_data_nodes=4,
 number_of_ready_data_nodes=3, connect_count=0 |
| ndbcluster | NdbTransaction | created=6, free=0, sizeof=212 |
| ndbcluster | NdbOperation | created=8, free=8, sizeof=660 |
| ndbcluster | NdbIndexScanOperation | created=1, free=1, sizeof=744 |
| ndbcluster | NdbIndexOperation | created=0, free=0, sizeof=664 |
| ndbcluster | NdbRecAttr | created=1285, free=1285, sizeof=60 |
| ndbcluster | NdbApiSignal | created=16, free=16, sizeof=136 |
| ndbcluster | NdbLabel | created=0, free=0, sizeof=196 |
| ndbcluster | NdbBranch | created=0, free=0, sizeof=24 |
| ndbcluster | NdbSubroutine | created=0, free=0, sizeof=68 |
| ndbcluster | NdbCall | created=0, free=0, sizeof=16 |
| ndbcluster | NdbBlob | created=1, free=1, sizeof=264 |
| ndbcluster | NdbReceiver | created=4, free=0, sizeof=68 |
```

```
| ndbcluster | binlog | latest_epoch=155467, latest_trans_epoch=148126,
 latest_received_binlog_epoch=0, latest_handled_binlog_epoch=0,
 latest_applied_binlog_epoch=0 |
+------------+-----------------------+--------------------------------------------------+
```

The Status column in each of these rows provides information about the MySQL server's connection to the cluster and about the cluster binary log's status, respectively. The Status information is in the form of comma-delimited set of name/value pairs.

The connection row's Status column contains the name/value pairs described in the following table.

| Name                       | Value                                                                                                                             |
|----------------------------|-----------------------------------------------------------------------------------------------------------------------------------|
| cluster_node_id            | The node ID of the MySQL server in the cluster                                                                                    |
| connected_host             | The host name or IP address of the cluster<br>management server to which the MySQL server is<br>connected                         |
| connected_port             | The port used by the MySQL server to connect to<br>the management server (connected_host)                                         |
| number_of_data_nodes       | The number of data nodes configured for the<br>cluster (that is, the number of [ndbd] sections in<br>the cluster config.ini file) |
| number_of_ready_data_nodes | The number of data nodes in the cluster that are<br>actually running                                                              |
| connect_count              | The number of times this mysqld has connected<br>or reconnected to cluster data nodes                                             |

The binlog row's Status column contains information relating to NDB Cluster Replication. The name/value pairs it contains are described in the following table.

| Name                         | Value                                                                                                                                              |
|------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------|
| latest_epoch                 | The most recent epoch most recently run on this<br>MySQL server (that is, the sequence number of<br>the most recent transaction run on the server) |
| latest_trans_epoch           | The most recent epoch processed by the cluster's<br>data nodes                                                                                     |
| latest_received_binlog_epoch | The most recent epoch received by the binary log<br>thread                                                                                         |
| latest_handled_binlog_epoch  | The most recent epoch processed by the binary<br>log thread (for writing to the binary log)                                                        |
| latest_applied_binlog_epoch  | The most recent epoch actually written to the<br>binary log                                                                                        |

See Section 21.7, "NDB Cluster Replication", for more information.

The remaining rows from the output of SHOW ENGINE NDB STATUS which are most likely to prove useful in monitoring the cluster are listed here by Name:

- NdbTransaction: The number and size of NdbTransaction objects that have been created. An NdbTransaction is created each time a table schema operation (such as CREATE TABLE or ALTER TABLE) is performed on an NDB table.
- NdbOperation: The number and size of NdbOperation objects that have been created.
- NdbIndexScanOperation: The number and size of NdbIndexScanOperation objects that have been created.

- NdbIndexOperation: The number and size of NdbIndexOperation objects that have been created.
- NdbRecAttr: The number and size of NdbRecAttr objects that have been created. In general, one of these is created each time a data manipulation statement is performed by an SQL node.
- NdbBlob: The number and size of NdbBlob objects that have been created. An NdbBlob is created for each new operation involving a BLOB column in an NDB table.
- NdbReceiver: The number and size of any NdbReceiver object that have been created. The
  number in the created column is the same as the number of data nodes in the cluster to which the
  MySQL server has connected.

![](_page_149_Picture_5.jpeg)

#### Note

SHOW ENGINE NDB STATUS returns an empty result if no operations involving NDB tables have been performed during the current session by the MySQL client accessing the SQL node on which this statement is run.

#### <span id="page-149-0"></span>13.7.5.16 SHOW ENGINES Statement

```
SHOW [STORAGE] ENGINES
```

SHOW ENGINES displays status information about the server's storage engines. This is particularly useful for checking whether a storage engine is supported, or to see what the default engine is.

For information about MySQL storage engines, see Chapter 14, *The InnoDB Storage Engine*, and Chapter 15, *Alternative Storage Engines*.

```
mysql> SHOW ENGINES\G
                   ***** 1. row **********
     Engine: InnoDB
    Support: DEFAULT
    Comment: Supports transactions, row-level locking, and foreign keys
Transactions: YES
        XA: YES
 Savepoints: YES
                 ****** 2. row ***************
    Engine: MRG MYISAM
    Support: YES
    Comment: Collection of identical MyISAM tables
Transactions: NO
        XA: NO
 Savepoints: NO
                  ****** 3. row **************
    Engine: MEMORY
    Support: YES
    Comment: Hash based, stored in memory, useful for temporary tables
Transactions: NO
        XA: NO
 Savepoints: NO
                ****** 4 row **************
    Engine: BLACKHOLE
    Support: YES
    Comment: /dev/null storage engine (anything you write to it disappears)
Transactions: NO
        XA: NO
 Savepoints: NO
                  ***** 5. row **************
    Engine: MyISAM
    Support: YES
    Comment: MyISAM storage engine
Transactions: NO
        XA: NO
 Savepoints: NO
                 ****** 6. row *************
    Engine: CSV
```

```
Support: YES
    Comment: CSV storage engine
Transactions: NO
        XA: NO
 Savepoints: NO
       *************** 7. row ***************
    Engine: ARCHIVE
    Support: YES
    Comment: Archive storage engine
Transactions: NO
        XA: NO
 Savepoints: NO
         *********** 8. row **************
    Engine: PERFORMANCE SCHEMA
    Support: YES
    Comment: Performance Schema
Transactions: NO
        XA: NO
 Savepoints: NO
      ****************** 9. row ***************
    Engine: FEDERATED
    Support: YES
    Comment: Federated MySQL storage engine
Transactions: NO
        XA: NO
 Savepoints: NO
```

The output from SHOW ENGINES may vary according to the MySQL version used and other factors.

SHOW ENGINES output has these columns:

• Engine

The name of the storage engine.

• Support

The server's level of support for the storage engine, as shown in the following table.

| Value    | Meaning                                       |
|----------|-----------------------------------------------|
| YES      | The engine is supported and is active         |
| DEFAULT  | Like YES, plus this is the default engine     |
| NO       | The engine is not supported                   |
| DISABLED | The engine is supported but has been disabled |

A value of NO means that the server was compiled without support for the engine, so it cannot be enabled at runtime.

A value of DISABLED occurs either because the server was started with an option that disables the engine, or because not all options required to enable it were given. In the latter case, the error log should contain a reason indicating why the option is disabled. See Section 5.4.2, "The Error Log".

You might also see <code>DISABLED</code> for a storage engine if the server was compiled to support it, but was started with a <code>--skip-engine\_name</code> option. For the <code>NDB</code> storage engine, <code>DISABLED</code> means the server was compiled with support for NDB Cluster, but was not started with the <code>--ndbcluster</code> option.

All MySQL servers support MyISAM tables. It is not possible to disable MyISAM.

• Comment

A brief description of the storage engine.

• Transactions

Whether the storage engine supports transactions.

• XA

Whether the storage engine supports XA transactions.

• Savepoints

Whether the storage engine supports savepoints.

Storage engine information is also available from the INFORMATION\_SCHEMA ENGINES table. See Section 24.3.7, "The INFORMATION\_SCHEMA ENGINES Table".

# <span id="page-151-0"></span>**13.7.5.17 SHOW ERRORS Statement**

```
SHOW ERRORS [LIMIT [offset,] row_count]
SHOW COUNT(*) ERRORS
```

[SHOW ERRORS](#page-151-0) is a diagnostic statement that is similar to [SHOW WARNINGS](#page-182-0), except that it displays information only for errors, rather than for errors, warnings, and notes.

The LIMIT clause has the same syntax as for the SELECT statement. See Section 13.2.9, "SELECT Statement".

The [SHOW COUNT\(\\*\) ERRORS](#page-151-0) statement displays the number of errors. You can also retrieve this number from the error\_count variable:

```
SHOW COUNT(*) ERRORS;
SELECT @@error_count;
```

[SHOW ERRORS](#page-151-0) and error\_count apply only to errors, not warnings or notes. In other respects, they are similar to [SHOW WARNINGS](#page-182-0) and warning\_count. In particular, [SHOW ERRORS](#page-151-0) cannot display information for more than max\_error\_count messages, and error\_count can exceed the value of max\_error\_count if the number of errors exceeds max\_error\_count.

For more information, see [Section 13.7.5.40, "SHOW WARNINGS Statement".](#page-182-0)

# <span id="page-151-1"></span>**13.7.5.18 SHOW EVENTS Statement**

```
SHOW EVENTS
 [{FROM | IN} schema_name]
 [LIKE 'pattern' | WHERE expr]
```

This statement displays information about Event Manager events, which are discussed in Section 23.4, "Using the Event Scheduler". It requires the EVENT privilege for the database from which the events are to be shown.

In its simplest form, [SHOW EVENTS](#page-151-1) lists all of the events in the current schema:

```
mysql> SELECT CURRENT_USER(), SCHEMA();
+----------------+----------+
| CURRENT_USER() | SCHEMA() |
+----------------+----------+
| jon@ghidora | myschema |
+----------------+----------+
1 row in set (0.00 sec)
mysql> SHOW EVENTS\G
*************************** 1. row ***************************
 Db: myschema
 Name: e_daily
 Definer: jon@ghidora
 Time zone: SYSTEM
 Type: RECURRING
 Execute at: NULL
```

```
 Interval value: 1
 Interval field: DAY
 Starts: 2018-08-08 11:06:34
 Ends: NULL
 Status: ENABLED
 Originator: 1
character_set_client: utf8
collation_connection: utf8_general_ci
 Database Collation: latin1_swedish_ci
```

To see events for a specific schema, use the FROM clause. For example, to see events for the test schema, use the following statement:

```
SHOW EVENTS FROM test;
```

The LIKE clause, if present, indicates which event names to match. The WHERE clause can be given to select rows using more general conditions, as discussed in Section 24.8, "Extensions to SHOW Statements".

[SHOW EVENTS](#page-151-1) output has these columns:

• Db

The name of the schema (database) to which the event belongs.

• Name

The name of the event.

• Definer

The account of the user who created the event, in 'user\_name'@'host\_name' format.

• Time zone

The event time zone, which is the time zone used for scheduling the event and that is in effect within the event as it executes. The default value is SYSTEM.

• Type

The event repetition type, either ONE TIME (transient) or RECURRING (repeating).

• Execute At

For a one-time event, this is the DATETIME value specified in the AT clause of the CREATE EVENT statement used to create the event, or of the last ALTER EVENT statement that modified the event. The value shown in this column reflects the addition or subtraction of any INTERVAL value included in the event's AT clause. For example, if an event is created using ON SCHEDULE AT CURRENT\_TIMESTAMP + '1:6' DAY\_HOUR, and the event was created at 2018-02-09 14:05:30, the value shown in this column would be '2018-02-10 20:05:30'. If the event's timing is determined by an EVERY clause instead of an AT clause (that is, if the event is recurring), the value of this column is NULL.

• Interval Value

For a recurring event, the number of intervals to wait between event executions. For a transient event, the value of this column is always NULL.

• Interval Field

The time units used for the interval which a recurring event waits before repeating. For a transient event, the value of this column is always NULL.

• Starts

The start date and time for a recurring event. This is displayed as a DATETIME value, and is NULL if no start date and time are defined for the event. For a transient event, this column is always NULL. For a recurring event whose definition includes a STARTS clause, this column contains the corresponding DATETIME value. As with the Execute At column, this value resolves any expressions used. If there is no STARTS clause affecting the timing of the event, this column is NULL

### • Ends

For a recurring event whose definition includes a ENDS clause, this column contains the corresponding DATETIME value. As with the Execute At column, this value resolves any expressions used. If there is no ENDS clause affecting the timing of the event, this column is NULL.

### • Status

The event status. One of ENABLED, DISABLED, or SLAVESIDE\_DISABLED. SLAVESIDE\_DISABLED indicates that the creation of the event occurred on another MySQL server acting as a replication source and replicated to the current MySQL server which is acting as a replica, but the event is not presently being executed on the replica. For more information, see Section 16.4.1.16, "Replication of Invoked Features". information.

### • Originator

The server ID of the MySQL server on which the event was created; used in replication. This value may be updated by ALTER EVENT to the server ID of the server on which that statement occurs, if executed on a source server. The default value is 0.

• character\_set\_client

The session value of the character\_set\_client system variable when the event was created.

• collation\_connection

The session value of the collation\_connection system variable when the event was created.

• Database Collation

The collation of the database with which the event is associated.

For more information about SLAVESIDE\_DISABLED and the Originator column, see Section 16.4.1.16, "Replication of Invoked Features".

Times displayed by [SHOW EVENTS](#page-151-1) are given in the event time zone, as discussed in Section 23.4.4, "Event Metadata".

Event information is also available from the INFORMATION\_SCHEMA EVENTS table. See Section 24.3.8, "The INFORMATION\_SCHEMA EVENTS Table".

The event action statement is not shown in the output of [SHOW EVENTS](#page-151-1). Use [SHOW CREATE EVENT](#page-140-1) or the INFORMATION\_SCHEMA EVENTS table.

## <span id="page-153-0"></span>**13.7.5.19 SHOW FUNCTION CODE Statement**

```
SHOW FUNCTION CODE func_name
```

This statement is similar to [SHOW PROCEDURE CODE](#page-159-0) but for stored functions. See [Section 13.7.5.27,](#page-159-0) ["SHOW PROCEDURE CODE Statement"](#page-159-0).

## <span id="page-153-1"></span>**13.7.5.20 SHOW FUNCTION STATUS Statement**

```
SHOW FUNCTION STATUS
 [LIKE 'pattern' | WHERE expr]
```

This statement is similar to [SHOW PROCEDURE STATUS](#page-160-1) but for stored functions. See [Section 13.7.5.28, "SHOW PROCEDURE STATUS Statement"](#page-160-1).

## <span id="page-154-0"></span>**13.7.5.21 SHOW GRANTS Statement**

```
SHOW GRANTS [FOR user]
```

This statement displays the privileges that are assigned to a MySQL user account, in the form of [GRANT](#page-103-0) statements that must be executed to duplicate the privilege assignments.

![](_page_154_Picture_5.jpeg)

#### **Note**

To display nonprivilege information for MySQL accounts, use the [SHOW CREATE](#page-143-1) [USER](#page-143-1) statement. See [Section 13.7.5.12, "SHOW CREATE USER Statement"](#page-143-1).

[SHOW GRANTS](#page-154-0) requires the SELECT privilege for the mysql system database, except to display privileges for the current user.

To name the account for [SHOW GRANTS](#page-154-0), use the same format as for the [GRANT](#page-103-0) statement (for example, 'jeffrey'@'localhost'):

```
mysql> SHOW GRANTS FOR 'jeffrey'@'localhost';
+------------------------------------------------------------------+
| Grants for jeffrey@localhost |
+------------------------------------------------------------------+
| GRANT USAGE ON *.* TO `jeffrey`@`localhost` |
| GRANT SELECT, INSERT, UPDATE ON `db1`.* TO `jeffrey`@`localhost` |
+------------------------------------------------------------------+
```

The host part, if omitted, defaults to '%'. For additional information about specifying account names, see Section 6.2.4, "Specifying Account Names".

To display the privileges granted to the current user (the account you are using to connect to the server), you can use any of the following statements:

```
SHOW GRANTS;
SHOW GRANTS FOR CURRENT_USER;
SHOW GRANTS FOR CURRENT_USER();
```

If SHOW GRANTS FOR CURRENT\_USER (or any equivalent syntax) is used in definer context, such as within a stored procedure that executes with definer rather than invoker privileges, the grants displayed are those of the definer and not the invoker.

[SHOW GRANTS](#page-154-0) does not display privileges that are available to the named account but are granted to a different account. For example, if an anonymous account exists, the named account might be able to use its privileges, but [SHOW GRANTS](#page-154-0) does not display them.

SHOW GRANTS output does not include IDENTIFIED BY PASSWORD clauses. Use the [SHOW CREATE](#page-143-1) [USER](#page-143-1) statement instead. See [Section 13.7.5.12, "SHOW CREATE USER Statement"](#page-143-1).

## <span id="page-154-1"></span>**13.7.5.22 SHOW INDEX Statement**

```
SHOW {INDEX | INDEXES | KEYS}
 {FROM | IN} tbl_name
 [{FROM | IN} db_name]
 [WHERE expr]
```

[SHOW INDEX](#page-154-1) returns table index information. The format resembles that of the SQLStatistics call in ODBC. This statement requires some privilege for any column in the table.

```
mysql> SHOW INDEX FROM City\G
*************************** 1. row ***************************
 Table: city
 Non_unique: 0
 Key_name: PRIMARY
 Seq_in_index: 1
```

```
 Column_name: ID
 Collation: A
 Cardinality: 4188
 Sub_part: NULL
 Packed: NULL
 Null:
 Index_type: BTREE
 Comment:
Index_comment:
*************************** 2. row ***************************
 Table: city
 Non_unique: 1
 Key_name: CountryCode
 Seq_in_index: 1
 Column_name: CountryCode
 Collation: A
 Cardinality: 232
 Sub_part: NULL
 Packed: NULL
 Null:
 Index_type: BTREE
 Comment:
Index_comment:
```

An alternative to tbl\_name FROM db\_name syntax is db\_name.tbl\_name. These two statements are equivalent:

```
SHOW INDEX FROM mytable FROM mydb;
SHOW INDEX FROM mydb.mytable;
```

The WHERE clause can be given to select rows using more general conditions, as discussed in Section 24.8, "Extensions to SHOW Statements".

[SHOW INDEX](#page-154-1) returns the following fields:

• Table

The name of the table.

• Non\_unique

0 if the index cannot contain duplicates, 1 if it can.

• Key\_name

The name of the index. If the index is the primary key, the name is always PRIMARY.

• Seq\_in\_index

The column sequence number in the index, starting with 1.

• Column\_name

The name of the column.

• Collation

How the column is sorted in the index. This can have values A (ascending) or NULL (not sorted).

• Cardinality

An estimate of the number of unique values in the index. To update this number, run [ANALYZE](#page-116-0) [TABLE](#page-116-0) or (for MyISAM tables) myisamchk -a.

Cardinality is counted based on statistics stored as integers, so the value is not necessarily exact even for small tables. The higher the cardinality, the greater the chance that MySQL uses the index when doing joins.

• Sub\_part

The index prefix. That is, the number of indexed characters if the column is only partly indexed, NULL if the entire column is indexed.

![](_page_156_Picture_3.jpeg)

#### **Note**

Prefix limits are measured in bytes. However, prefix lengths for index specifications in CREATE TABLE, ALTER TABLE, and CREATE INDEX statements are interpreted as number of characters for nonbinary string types (CHAR, VARCHAR, TEXT) and number of bytes for binary string types (BINARY, VARBINARY, BLOB). Take this into account when specifying a prefix length for a nonbinary string column that uses a multibyte character set.

For additional information about index prefixes, see Section 8.3.4, "Column Indexes", and Section 13.1.14, "CREATE INDEX Statement".

• Packed

Indicates how the key is packed. NULL if it is not.

• Null

Contains YES if the column may contain NULL values and '' if not.

• Index\_type

The index method used (BTREE, FULLTEXT, HASH, RTREE).

• Comment

Information about the index not described in its own column, such as disabled if the index is disabled.

• Index\_comment

Any comment provided for the index with a COMMENT attribute when the index was created.

Information about table indexes is also available from the INFORMATION\_SCHEMA STATISTICS table. See Section 24.3.24, "The INFORMATION\_SCHEMA STATISTICS Table".

You can list a table's indexes with the mysqlshow -k db\_name tbl\_name command.

# <span id="page-156-0"></span>**13.7.5.23 SHOW MASTER STATUS Statement**

```
SHOW MASTER STATUS
```

This statement provides status information about the binary log files of the source. It requires either the SUPER or REPLICATION CLIENT privilege.

#### Example:

```
mysql> SHOW MASTER STATUS\G
*************************** 1. row ***************************
 File: source-bin.000002
 Position: 1307
 Binlog_Do_DB: test
 Binlog_Ignore_DB: manual, mysql
Executed_Gtid_Set: 3E11FA47-71CA-11E1-9E33-C80AA9429562:1-5
1 row in set (0.00 sec)
```

When global transaction IDs are in use, Executed\_Gtid\_Set shows the set of GTIDs for transactions that have been executed on the source. This is the same as the value for the gtid\_executed system

variable on this server, as well as the value for Executed\_Gtid\_Set in the output of [SHOW SLAVE](#page-167-0) [STATUS](#page-167-0) on this server.

# <span id="page-157-1"></span>**13.7.5.24 SHOW OPEN TABLES Statement**

```
SHOW OPEN TABLES
 [{FROM | IN} db_name]
 [LIKE 'pattern' | WHERE expr]
```

[SHOW OPEN TABLES](#page-157-1) lists the non-TEMPORARY tables that are currently open in the table cache. See Section 8.4.3.1, "How MySQL Opens and Closes Tables". The FROM clause, if present, restricts the tables shown to those present in the db\_name database. The LIKE clause, if present, indicates which table names to match. The WHERE clause can be given to select rows using more general conditions, as discussed in Section 24.8, "Extensions to SHOW Statements".

[SHOW OPEN TABLES](#page-157-1) output has these columns:

• Database

The database containing the table.

• Table

The table name.

• In\_use

The number of table locks or lock requests there are for the table. For example, if one client acquires a lock for a table using LOCK TABLE t1 WRITE, In\_use is 1. If another client issues LOCK TABLE t1 WRITE while the table remains locked, the client blocks waiting for the lock, but the lock request causes In\_use to be 2. If the count is zero, the table is open but not currently being used. In\_use is also increased by the HANDLER ... OPEN statement and decreased by HANDLER ... CLOSE.

• Name\_locked

Whether the table name is locked. Name locking is used for operations such as dropping or renaming tables.

If you have no privileges for a table, it does not show up in the output from [SHOW OPEN TABLES](#page-157-1).

# <span id="page-157-0"></span>**13.7.5.25 SHOW PLUGINS Statement**

```
SHOW PLUGINS
```

[SHOW PLUGINS](#page-157-0) displays information about server plugins.

Example of [SHOW PLUGINS](#page-157-0) output:

```
mysql> SHOW PLUGINS\G
*************************** 1. row ***************************
 Name: binlog
 Status: ACTIVE
 Type: STORAGE ENGINE
Library: NULL
License: GPL
*************************** 2. row ***************************
 Name: CSV
 Status: ACTIVE
 Type: STORAGE ENGINE
Library: NULL
License: GPL
*************************** 3. row ***************************
 Name: MEMORY
 Status: ACTIVE
 Type: STORAGE ENGINE
```

```
Library: NULL
License: GPL
*************************** 4. row ***************************
 Name: MyISAM
 Status: ACTIVE
 Type: STORAGE ENGINE
Library: NULL
License: GPL
...
```

[SHOW PLUGINS](#page-157-0) output has these columns:

• Name

The name used to refer to the plugin in statements such as [INSTALL PLUGIN](#page-128-0) and [UNINSTALL](#page-129-0) [PLUGIN](#page-129-0).

• Status

The plugin status, one of ACTIVE, INACTIVE, DISABLED, or DELETED.

• Type

The type of plugin, such as STORAGE ENGINE, INFORMATION\_SCHEMA, or AUTHENTICATION.

• Library

The name of the plugin shared library file. This is the name used to refer to the plugin file in statements such as [INSTALL PLUGIN](#page-128-0) and [UNINSTALL PLUGIN](#page-129-0). This file is located in the directory named by the plugin\_dir system variable. If the library name is NULL, the plugin is compiled in and cannot be uninstalled with [UNINSTALL PLUGIN](#page-129-0).

• License

How the plugin is licensed (for example, GPL).

For plugins installed with [INSTALL PLUGIN](#page-128-0), the Name and Library values are also registered in the mysql.plugin system table.

For information about plugin data structures that form the basis of the information displayed by [SHOW](#page-157-0) [PLUGINS](#page-157-0), see [The MySQL Plugin API](https://dev.mysql.com/doc/extending-mysql/5.7/en/plugin-api.md).

Plugin information is also available from the INFORMATION\_SCHEMA .PLUGINS table. See Section 24.3.17, "The INFORMATION\_SCHEMA PLUGINS Table".

## <span id="page-158-0"></span>**13.7.5.26 SHOW PRIVILEGES Statement**

```
SHOW PRIVILEGES
```

[SHOW PRIVILEGES](#page-158-0) shows the list of system privileges that the MySQL server supports. The exact list of privileges depends on the version of your server.

```
mysql> SHOW PRIVILEGES\G
*************************** 1. row ***************************
Privilege: Alter
 Context: Tables
 Comment: To alter the table
*************************** 2. row ***************************
Privilege: Alter routine
 Context: Functions,Procedures
 Comment: To alter or drop stored functions/procedures
*************************** 3. row ***************************
Privilege: Create
 Context: Databases,Tables,Indexes
 Comment: To create new databases and tables
```

```
**************************************
```

Privileges belonging to a specific user are displayed by the SHOW GRANTS statement. See Section 13.7.5.21. "SHOW GRANTS Statement", for more information.

#### <span id="page-159-0"></span>13.7.5.27 SHOW PROCEDURE CODE Statement

```
SHOW PROCEDURE CODE proc name
```

This statement is a MySQL extension that is available only for servers that have been built with debugging support. It displays a representation of the internal implementation of the named stored procedure. A similar statement, SHOW FUNCTION CODE, displays information about stored functions (see Section 13.7.5.19, "SHOW FUNCTION CODE Statement").

To use either statement, you must be the owner of the routine or have SELECT access to the mysql.proc table.

If the named routine is available, each statement produces a result set. Each row in the result set corresponds to one "instruction" in the routine. The first column is Pos, which is an ordinal number beginning with 0. The second column is Instruction, which contains an SQL statement (usually changed from the original source), or a directive which has meaning only to the stored-routine handler.

```
mysql> DELIMITER //
mysql> CREATE PROCEDURE p1 ()
      BECTN
        DECLARE fanta INT DEFAULT 55;
        DROP TABLE t2;
        LOOP
          INSERT INTO t3 VALUES (fanta);
          END LOOP;
Query OK, 0 rows affected (0.01 sec)
mysql> SHOW PROCEDURE CODE p1//
| Pos | Instruction
   0 | set fanta@0 55
   1 | stmt 9 "DROP TABLE t2"
   2 | stmt 5 "INSERT INTO t3 VALUES (fanta)" |
   3 | jump 2
4 rows in set (0.00 sec)
mvsql> CREATE FUNCTION test.hello (s CHAR(20))
      PETTIENS CHAR (50) DETERMINISTIC
     RETURN CONCAT('Hello, ',s,'!');
Query OK, 0 rows affected (0.00 sec)
mysql> SHOW FUNCTION CODE test.hello;
| Pos | Instruction
| 0 | freturn 254 concat('Hello, ',s@0,'!') |
1 row in set (0.00 sec)
```

In this example, the nonexecutable BEGIN and END statements have disappeared, and for the DECLARE variable\_name statement, only the executable part appears (the part where the default is assigned). For each statement that is taken from source, there is a code word stmt followed by a type

(9 means DROP, 5 means INSERT, and so on). The final row contains an instruction jump 2, meaning GOTO instruction #2.

#### <span id="page-160-1"></span>13.7.5.28 SHOW PROCEDURE STATUS Statement

```
SHOW PROCEDURE STATUS
[LIKE 'pattern' | WHERE expr]
```

This statement is a MySQL extension. It returns characteristics of a stored procedure, such as the database, name, type, creator, creation and modification dates, and character set information. A similar statement, SHOW FUNCTION STATUS, displays information about stored functions (see Section 13.7.5.20, "SHOW FUNCTION STATUS Statement").

To use either statement, you must be the owner of the routine or have SELECT access to the mysql.proc table.

The LIKE clause, if present, indicates which procedure or function names to match. The WHERE clause can be given to select rows using more general conditions, as discussed in Section 24.8, "Extensions to SHOW Statements".

```
mysql> SHOW PROCEDURE STATUS LIKE 'sp1'\G
      ****************** 1. row ****************
                 Db: test
               Name: sp1
               Type: PROCEDURE
            Definer: testuser@localhost
           Modified: 2018-08-08 13:54:11
            Created: 2018-08-08 13:54:11
      Security type: DEFINER
            Comment:
character_set client: utf8
collation_connection: utf8_general_ci
    Database Collation: latin1_swedish_ci
myscl> SHOW FUNCTION STATUS LIKE 'hello'\G
      ***** 1. row ****
                 Db: test
               Name: hello
               Type: FUNCTION
            Definer: testuser@localhost
           Modified: 2020-03-10 11:09:33
            Created: 2020-03-10 11:09:33
      Security type: DEFINER
            Comment:
character set client: utf8
collation connection: utf8 general ci
 Database Collation: latin1 swedish ci
```

character\_set\_client is the session value of the character\_set\_client system variable when the routine was created. collation\_connection is the session value of the collation\_connection system variable when the routine was created. Database Collation is the collation of the database with which the routine is associated.

Stored routine information is also available from the <code>INFORMATION\_SCHEMA PARAMETERS</code> and <code>ROUTINES</code> tables. See Section 24.3.15, "The <code>INFORMATION\_SCHEMA PARAMETERS Table</code>", and Section 24.3.21, "The <code>INFORMATION\_SCHEMA ROUTINES Table</code>".

#### <span id="page-160-0"></span>13.7.5.29 SHOW PROCESSLIST Statement

```
SHOW [FULL] PROCESSLIST
```

The MySQL process list indicates the operations currently being performed by the set of threads executing within the server. The SHOW PROCESSLIST statement is one source of process information. For a comparison of this statement with other sources, see Sources of Process Information.

If you have the PROCESS privilege, you can see all threads, even those belonging to other users. Otherwise (without the PROCESS privilege), nonanonymous users have access to information about

their own threads but not threads for other users, and anonymous users have no access to thread information.

Without the FULL keyword, SHOW PROCESSLIST displays only the first 100 characters of each statement in the Info field.

The SHOW PROCESSLIST statement is very useful if you get the "too many connections" error message and want to find out what is going on. MySQL reserves one extra connection to be used by accounts that have the SUPER privilege, to ensure that administrators should always be able to connect and check the system (assuming that you are not giving this privilege to all your users).

Threads can be killed with the KILL statement. See Section 13.7.6.4, "KILL Statement".

Example of SHOW PROCESSLIST output:

```
mysql> SHOW FULL PROCESSLIST\G
            ******** 1. row ***************
  User: system user
  Host:
   db: NULL
Command: Connect
  Time: 1030455
 State: Waiting for master to send event
  Info: NULL
             ******* 2. row **************
   Td: 2
  User: system user
  Host:
   db: NULL
Command: Connect
  Time: 1004
 State: Has read all relay log; waiting for the slave
       I/O thread to update it
  Info: NULL
               ******* 3 row *************
   Id: 3112
  User: replikator
  Host: artemis:2204
   db: NULL
Command: Binlog Dump
  Time: 2144
 State: Has sent all binlog to slave; waiting for binlog to be updated
  Info: NULL
            ******** 4. row **************
   Td: 3113
  User: replikator
  Host: iconnect2:45781
   db: NULL
Command: Binlog Dump
  Time: 2086
 State: Has sent all binlog to slave; waiting for binlog to be updated
  Info. NIII.I.
             ******** 5. row ***************
   Id: 3123
  User: stefan
  Host: localhost
   db: apollon
Command: Ouerv
  Time: 0
 State: NULL
  Info: SHOW FULL PROCESSLIST
```

SHOW PROCESSLIST output has these columns:

• Id

The connection identifier. This is the same value displayed in the ID column of the INFORMATION SCHEMA PROCESSLIST table, displayed in the PROCESSLIST ID column of the

Performance Schema threads table, and returned by the CONNECTION\_ID() function within the thread.

### • User

The MySQL user who issued the statement. A value of system user refers to a nonclient thread spawned by the server to handle tasks internally, for example, a delayed-row handler thread or an I/O or SQL thread used on replica hosts. For system user, there is no host specified in the Host column. unauthenticated user refers to a thread that has become associated with a client connection but for which authentication of the client user has not yet occurred. event\_scheduler refers to the thread that monitors scheduled events (see Section 23.4, "Using the Event Scheduler").

### • Host

The host name of the client issuing the statement (except for system user, for which there is no host). The host name for TCP/IP connections is reported in host\_name:client\_port format to make it easier to determine which client is doing what.

• db

The default database for the thread, or NULL if none has been selected.

### • Command

The type of command the thread is executing on behalf of the client, or Sleep if the session is idle. For descriptions of thread commands, see Section 8.14, "Examining Server Thread (Process) Information". The value of this column corresponds to the COM\_xxx commands of the client/server protocol and Com\_xxx status variables. See Section 5.1.9, "Server Status Variables".

### • Time

The time in seconds that the thread has been in its current state. For a replica SQL thread, the value is the number of seconds between the timestamp of the last replicated event and the real time of the replica host. See Section 16.2.3, "Replication Threads".

### • State

An action, event, or state that indicates what the thread is doing. For descriptions of State values, see Section 8.14, "Examining Server Thread (Process) Information".

Most states correspond to very quick operations. If a thread stays in a given state for many seconds, there might be a problem that needs to be investigated.

# • Info

The statement the thread is executing, or NULL if it is executing no statement. The statement might be the one sent to the server, or an innermost statement if the statement executes other statements. For example, if a CALL statement executes a stored procedure that is executing a SELECT statement, the Info value shows the SELECT statement.

# <span id="page-162-0"></span>**13.7.5.30 SHOW PROFILE Statement**

```
SHOW PROFILE [type [, type] ... ]
 [FOR QUERY n]
 [LIMIT row_count [OFFSET offset]]
type: {
 ALL
 | BLOCK IO
 | CONTEXT SWITCHES
 | CPU
 | IPC
 | MEMORY
 | PAGE FAULTS
```

```
 | SOURCE
 | SWAPS
}
```

The [SHOW PROFILE](#page-162-0) and [SHOW PROFILES](#page-165-1) statements display profiling information that indicates resource usage for statements executed during the course of the current session.

![](_page_163_Picture_3.jpeg)

### **Note**

The [SHOW PROFILE](#page-162-0) and [SHOW PROFILES](#page-165-1) statements are deprecated; expect them to be removed in a future MySQL release. Use the Performance Schema instead; see Section 25.19.1, "Query Profiling Using Performance Schema".

To control profiling, use the profiling session variable, which has a default value of 0 (OFF). Enable profiling by setting profiling to 1 or ON:

```
mysql> SET profiling = 1;
```

[SHOW PROFILES](#page-165-1) displays a list of the most recent statements sent to the server. The size of the list is controlled by the profiling\_history\_size session variable, which has a default value of 15. The maximum value is 100. Setting the value to 0 has the practical effect of disabling profiling.

All statements are profiled except [SHOW PROFILE](#page-162-0) and [SHOW PROFILES](#page-165-1), so neither of those statements appears in the profile list. Malformed statements are profiled. For example, SHOW PROFILING is an illegal statement, and a syntax error occurs if you try to execute it, but it shows up in the profiling list.

[SHOW PROFILE](#page-162-0) displays detailed information about a single statement. Without the FOR QUERY n clause, the output pertains to the most recently executed statement. If FOR QUERY n is included, [SHOW](#page-162-0) [PROFILE](#page-162-0) displays information for statement n. The values of n correspond to the Query\_ID values displayed by [SHOW PROFILES](#page-165-1).

The LIMIT row\_count clause may be given to limit the output to row\_count rows. If LIMIT is given, OFFSET offset may be added to begin the output offset rows into the full set of rows.

By default, [SHOW PROFILE](#page-162-0) displays Status and Duration columns. The Status values are like the State values displayed by [SHOW PROCESSLIST](#page-160-0), although there might be some minor differences in interpretion for the two statements for some status values (see Section 8.14, "Examining Server Thread (Process) Information").

Optional type values may be specified to display specific additional types of information:

- ALL displays all information
- BLOCK IO displays counts for block input and output operations
- CONTEXT SWITCHES displays counts for voluntary and involuntary context switches
- CPU displays user and system CPU usage times
- IPC displays counts for messages sent and received
- MEMORY is not currently implemented
- PAGE FAULTS displays counts for major and minor page faults
- SOURCE displays the names of functions from the source code, together with the name and line number of the file in which the function occurs
- SWAPS displays swap counts

Profiling is enabled per session. When a session ends, its profiling information is lost.

```
mysql> SELECT @@profiling;
+-------------+
```

```
| @@profiling |
+-------------+
| 0 |
+-------------+
1 row in set (0.00 sec)
mysql> SET profiling = 1;
Query OK, 0 rows affected (0.00 sec)
mysql> DROP TABLE IF EXISTS t1;
Query OK, 0 rows affected, 1 warning (0.00 sec)
mysql> CREATE TABLE T1 (id INT);
Query OK, 0 rows affected (0.01 sec)
mysql> SHOW PROFILES;
+----------+----------+--------------------------+
| Query_ID | Duration | Query |
+----------+----------+--------------------------+
| 0 | 0.000088 | SET PROFILING = 1 |
| 1 | 0.000136 | DROP TABLE IF EXISTS t1 |
| 2 | 0.011947 | CREATE TABLE t1 (id INT) |
+----------+----------+--------------------------+
3 rows in set (0.00 sec)
mysql> SHOW PROFILE;
+----------------------+----------+
| Status | Duration |
+----------------------+----------+
| checking permissions | 0.000040 |
| creating table | 0.000056 |
| After create | 0.011363 |
| query end | 0.000375 |
| freeing items | 0.000089 |
| logging slow query | 0.000019 |
| cleaning up | 0.000005 |
+----------------------+----------+
7 rows in set (0.00 sec)
mysql> SHOW PROFILE FOR QUERY 1;
+--------------------+----------+
| Status | Duration |
+--------------------+----------+
| query end | 0.000107 |
| freeing items | 0.000008 |
| logging slow query | 0.000015 |
| cleaning up | 0.000006 |
+--------------------+----------+
4 rows in set (0.00 sec)
mysql> SHOW PROFILE CPU FOR QUERY 2;
+----------------------+----------+----------+------------+
| Status | Duration | CPU_user | CPU_system |
+----------------------+----------+----------+------------+
| checking permissions | 0.000040 | 0.000038 | 0.000002 |
| creating table | 0.000056 | 0.000028 | 0.000028 |
| After create | 0.011363 | 0.000217 | 0.001571 |
| query end | 0.000375 | 0.000013 | 0.000028 |
| freeing items | 0.000089 | 0.000010 | 0.000014 |
| logging slow query | 0.000019 | 0.000009 | 0.000010 |
| cleaning up | 0.000005 | 0.000003 | 0.000002 |
+----------------------+----------+----------+------------+
7 rows in set (0.00 sec)
```

![](_page_164_Picture_2.jpeg)

#### **Note**

Profiling is only partially functional on some architectures. For values that depend on the getrusage() system call, NULL is returned on systems such as Windows that do not support the call. In addition, profiling is per process and not per thread. This means that activity on threads within the server other than your own may affect the timing information that you see.

Profiling information is also available from the INFORMATION\_SCHEMA PROFILING table. See Section 24.3.19, "The INFORMATION\_SCHEMA PROFILING Table". For example, the following queries are equivalent:

```
SHOW PROFILE FOR QUERY 2;
SELECT STATE, FORMAT(DURATION, 6) AS DURATION
FROM INFORMATION_SCHEMA.PROFILING
WHERE QUERY_ID = 2 ORDER BY SEQ;
```

# <span id="page-165-1"></span>**13.7.5.31 SHOW PROFILES Statement**

```
SHOW PROFILES
```

The [SHOW PROFILES](#page-165-1) statement, together with [SHOW PROFILE](#page-162-0), displays profiling information that indicates resource usage for statements executed during the course of the current session. For more information, see [Section 13.7.5.30, "SHOW PROFILE Statement"](#page-162-0).

![](_page_165_Picture_6.jpeg)

#### **Note**

The [SHOW PROFILE](#page-162-0) and [SHOW PROFILES](#page-165-1) statements are deprecated; expect them to be removed in a future MySQL release. Use the Performance Schema instead; see Section 25.19.1, "Query Profiling Using Performance Schema".

## <span id="page-165-0"></span>**13.7.5.32 SHOW RELAYLOG EVENTS Statement**

```
SHOW RELAYLOG EVENTS
 [IN 'log_name']
 [FROM pos]
 [LIMIT [offset,] row_count]
 [channel_option]
channel_option:
 FOR CHANNEL channel
```

Shows the events in the relay log of a replica. If you do not specify 'log\_name', the first relay log is displayed. This statement has no effect on the source. [SHOW RELAYLOG EVENTS](#page-165-0) requires the REPLICATION SLAVE privilege.

The LIMIT clause has the same syntax as for the SELECT statement. See Section 13.2.9, "SELECT Statement".

![](_page_165_Picture_13.jpeg)

### **Note**

Issuing a [SHOW RELAYLOG EVENTS](#page-165-0) with no LIMIT clause could start a very time- and resource-consuming process because the server returns to the client the complete contents of the relay log (including all statements modifying data that have been received by the replica).

The optional FOR CHANNEL channel clause enables you to name which replication channel the statement applies to. Providing a FOR CHANNEL channel clause applies the statement to a specific replication channel. If no channel is named and no extra channels exist, the statement applies to the default channel.

When using multiple replication channels, if a [SHOW RELAYLOG EVENTS](#page-165-0) statement does not have a channel defined using a FOR CHANNEL channel clause an error is generated. See Section 16.2.2, "Replication Channels" for more information.

[SHOW RELAYLOG EVENTS](#page-165-0) displays the following fields for each event in the relay log:

• Log\_name

The name of the file that is being listed.

• Pos

The position at which the event occurs.

• Event\_type

An identifier that describes the event type.

• Server\_id

The server ID of the server on which the event originated.

• End\_log\_pos

The value of End\_log\_pos for this event in the source's binary log.

• Info

More detailed information about the event type. The format of this information depends on the event type.

![](_page_166_Picture_11.jpeg)

#### **Note**

Some events relating to the setting of user and system variables are not included in the output from [SHOW RELAYLOG EVENTS](#page-165-0). To get complete coverage of events within a relay log, use mysqlbinlog.

# <span id="page-166-0"></span>**13.7.5.33 SHOW SLAVE HOSTS Statement**

SHOW SLAVE HOSTS

Displays a list of replicas currently registered with the source.

SHOW SLAVE HOSTS should be executed on a server that acts as a replication source. SHOW SLAVE HOSTS requires the REPLICATION SLAVE privilege. The statement displays information about servers that are or have been connected as replicas, with each row of the result corresponding to one replica server, as shown here:

```
mysql> SHOW SLAVE HOSTS;
+------------+-----------+------+-----------+--------------------------------------+
| Server_id | Host | Port | Master_id | Slave_UUID |
+------------+-----------+------+-----------+--------------------------------------+
| 192168010 | iconnect2 | 3306 | 192168011 | 14cb6624-7f93-11e0-b2c0-c80aa9429562 |
| 1921680101 | athena | 3306 | 192168011 | 07af4990-f41f-11df-a566-7ac56fdaf645 |
+------------+-----------+------+-----------+--------------------------------------+
```

- Server\_id: The unique server ID of the replica server, as configured in the replica server's option file, or on the command line with --server-id=value.
- Host: The host name of the replica server as specified on the replica with the --report-host option. This can differ from the machine name as configured in the operating system.
- User: The replica server user name as, specified on the replica with the --report-user option. Statement output includes this column only if the source server is started with the --show-slaveauth-info option.
- Password: The replica server password as, specified on the replica with the --report-password option. Statement output includes this column only if the source server is started with the --showslave-auth-info option.
- Port: The port on the source to which the replica server is listening, as specified on the replica with the --report-port option.

A zero in this column means that the replica port (--report-port) was not set.

- Master\_id: The unique server ID of the source server that the replica server is replicating from. This is the server ID of the server on which SHOW SLAVE HOSTS is executed, so this same value is listed for each row in the result.
- Slave\_UUID: The globally unique ID of this replica, as generated on the replica and found in the replica's auto.cnf file.

# <span id="page-167-0"></span>**13.7.5.34 SHOW SLAVE STATUS Statement**

```
SHOW SLAVE STATUS [FOR CHANNEL channel]
```

This statement provides status information on essential parameters of the replica threads. It requires either the SUPER or REPLICATION CLIENT privilege.

If you issue this statement using the mysql client, you can use a \G statement terminator rather than a semicolon to obtain a more readable vertical layout:

```
mysql> SHOW SLAVE STATUS\G
*************************** 1. row ***************************
 Slave_IO_State: Waiting for master to send event
 Master_Host: localhost
 Master_User: repl
 Master_Port: 13000
 Connect_Retry: 60
 Master_Log_File: source-bin.000002
 Read_Master_Log_Pos: 1307
 Relay_Log_File: replica-relay-bin.000003
 Relay_Log_Pos: 1508
 Relay_Master_Log_File: source-bin.000002
 Slave_IO_Running: Yes
 Slave_SQL_Running: Yes
 Replicate_Do_DB:
 Replicate_Ignore_DB:
 Replicate_Do_Table:
 Replicate_Ignore_Table:
 Replicate_Wild_Do_Table:
 Replicate_Wild_Ignore_Table:
 Last_Errno: 0
 Last_Error:
 Skip_Counter: 0
 Exec_Master_Log_Pos: 1307
 Relay_Log_Space: 1858
 Until_Condition: None
 Until_Log_File:
 Until_Log_Pos: 0
 Master_SSL_Allowed: No
 Master_SSL_CA_File:
 Master_SSL_CA_Path:
 Master_SSL_Cert:
 Master_SSL_Cipher:
 Master_SSL_Key:
 Seconds_Behind_Master: 0
Master_SSL_Verify_Server_Cert: No
 Last_IO_Errno: 0
 Last_IO_Error:
 Last_SQL_Errno: 0
 Last_SQL_Error:
 Replicate_Ignore_Server_Ids:
 Master_Server_Id: 1
 Master_UUID: 3e11fa47-71ca-11e1-9e33-c80aa9429562
 Master_Info_File: /var/mysqld.2/data/master.info
 SQL_Delay: 0
 SQL_Remaining_Delay: NULL
 Slave_SQL_Running_State: Reading event from the relay log
 Master_Retry_Count: 10
 Master_Bind:
 Last_IO_Error_Timestamp:
 Last_SQL_Error_Timestamp:
 Master_SSL_Crl:
 Master_SSL_Crlpath:
```

```
 Retrieved_Gtid_Set: 3e11fa47-71ca-11e1-9e33-c80aa9429562:1-5
 Executed_Gtid_Set: 3e11fa47-71ca-11e1-9e33-c80aa9429562:1-5
 Auto_Position: 1
 Replicate_Rewrite_DB:
 Channel_name:
 Master_TLS_Version: TLSv1.2
```

The Performance Schema provides tables that expose replication information. This is similar to the information available from the [SHOW SLAVE STATUS](#page-167-0) statement, but represented in table form. For details, see Section 25.12.11, "Performance Schema Replication Tables".

The following list describes the fields returned by [SHOW SLAVE STATUS](#page-167-0). For additional information about interpreting their meanings, see Section 16.1.7.1, "Checking Replication Status".

• Slave\_IO\_State

A copy of the State field of the [SHOW PROCESSLIST](#page-160-0) output for the replica I/O thread. This tells you what the thread is doing: trying to connect to the source, waiting for events from the source, reconnecting to the source, and so on. For a listing of possible states, see Section 8.14.6, "Replication Replica I/O Thread States".

• Master\_Host

The source host that the replica is connected to.

• Master\_User

The user name of the account used to connect to the source.

• Master\_Port

The port used to connect to the source.

• Connect\_Retry

The number of seconds between connect retries (default 60). This can be set with the [CHANGE](#page-32-0) [MASTER TO](#page-32-0) statement.

• Master\_Log\_File

The name of the source binary log file from which the I/O thread is currently reading.

• Read\_Master\_Log\_Pos

The position in the current source binary log file up to which the I/O thread has read.

• Relay\_Log\_File

The name of the relay log file from which the SQL thread is currently reading and executing.

• Relay\_Log\_Pos

The position in the current relay log file up to which the SQL thread has read and executed.

• Relay\_Master\_Log\_File

The name of the source binary log file containing the most recent event executed by the SQL thread.

• Slave\_IO\_Running

Whether the I/O thread is started and has connected successfully to the source. Internally, the state of this thread is represented by one of the following three values:

• **MYSQL\_SLAVE\_NOT\_RUN.** The replica I/O thread is not running. For this state, Slave\_IO\_Running is No.

- **MYSQL\_SLAVE\_RUN\_NOT\_CONNECT.** The replica I/O thread is running, but is not connected to a replication source. For this state, Slave\_IO\_Running is Connecting.
- **MYSQL\_SLAVE\_RUN\_CONNECT.** The replica I/O thread is running, and is connected to a replication source. For this state, Slave\_IO\_Running is Yes.

The value of the Slave\_running system status variable corresponds with this value.

• Slave\_SQL\_Running

Whether the SQL thread is started.

• Replicate\_Do\_DB, Replicate\_Ignore\_DB

The lists of databases that were specified with the --replicate-do-db and --replicateignore-db options, if any.

• Replicate\_Do\_Table, Replicate\_Ignore\_Table, Replicate\_Wild\_Do\_Table, Replicate\_Wild\_Ignore\_Table

The lists of tables that were specified with the --replicate-do-table, --replicate-ignoretable, --replicate-wild-do-table, and --replicate-wild-ignore-table options, if any.

• Last\_Errno, Last\_Error

These columns are aliases for Last\_SQL\_Errno and Last\_SQL\_Error.

Issuing [RESET MASTER](#page-30-0) or [RESET SLAVE](#page-40-0) resets the values shown in these columns.

![](_page_169_Picture_13.jpeg)

#### **Note**

When the replica SQL thread receives an error, it reports the error first, then stops the SQL thread. This means that there is a small window of time during which [SHOW SLAVE STATUS](#page-167-0) shows a nonzero value for Last\_SQL\_Errno even though Slave\_SQL\_Running still displays Yes.

• Skip\_Counter

The current value of the sql\_slave\_skip\_counter system variable. See [Section 13.4.2.4, "SET](#page-42-1) [GLOBAL sql\\_slave\\_skip\\_counter Syntax"](#page-42-1).

• Exec\_Master\_Log\_Pos

The position in the current source binary log file to which the SQL thread has read and executed, marking the start of the next transaction or event to be processed. You can use this value with the [CHANGE MASTER TO](#page-32-0) statement's MASTER\_LOG\_POS option when starting a new replica from an existing replica, so that the new replica reads from this point. The coordinates given by (Relay\_Master\_Log\_File, Exec\_Master\_Log\_Pos) in the source's binary log correspond to the coordinates given by (Relay\_Log\_File, Relay\_Log\_Pos) in the relay log.

Inconsistencies in the sequence of transactions from the relay log which have been executed can cause this value to be a "low-water mark". In other words, transactions appearing before the position are guaranteed to have committed, but transactions after the position may have committed or not. If these gaps need to be corrected, use [START SLAVE UNTIL SQL\\_AFTER\\_MTS\\_GAPS](#page-42-0). See Section 16.4.1.32, "Replication and Transaction Inconsistencies" for more information.

• Relay\_Log\_Space

The total combined size of all existing relay log files.

• Until\_Condition, Until\_Log\_File, Until\_Log\_Pos

The values specified in the UNTIL clause of the [START SLAVE](#page-42-0) statement.

Until\_Condition has these values:

- None if no UNTIL clause was specified
- Master if the replica is reading until a given position in the source's binary log
- Relay if the replica is reading until a given position in its relay log
- SQL\_BEFORE\_GTIDS if the replica SQL thread is processing transactions until it has reached the first transaction whose GTID is listed in the gtid\_set.
- SQL\_AFTER\_GTIDS if the replica threads are processing all transactions until the last transaction in the gtid\_set has been processed by both threads.
- [SQL\\_AFTER\\_MTS\\_GAPS](#page-42-0) if a multithreaded replica's SQL threads are running until no more gaps are found in the relay log.

Until\_Log\_File and Until\_Log\_Pos indicate the log file name and position that define the coordinates at which the SQL thread stops executing.

For more information on UNTIL clauses, see [Section 13.4.2.5, "START SLAVE Statement"](#page-42-0).

• Master\_SSL\_Allowed, Master\_SSL\_CA\_File, Master\_SSL\_CA\_Path, Master\_SSL\_Cert, Master\_SSL\_Cipher, Master\_SSL\_CRL\_File, Master\_SSL\_CRL\_Path, Master\_SSL\_Key, Master\_SSL\_Verify\_Server\_Cert

These fields show the SSL parameters used by the replica to connect to the source, if any.

Master\_SSL\_Allowed has these values:

- Yes if an SSL connection to the source is permitted
- No if an SSL connection to the source is not permitted
- Ignored if an SSL connection is permitted but the replica server does not have SSL support enabled

The values of the other SSL-related fields correspond to the values of the MASTER\_SSL\_CA, MASTER\_SSL\_CAPATH, MASTER\_SSL\_CERT, MASTER\_SSL\_CIPHER, MASTER\_SSL\_CRL, MASTER\_SSL\_CRLPATH, MASTER\_SSL\_KEY, and MASTER\_SSL\_VERIFY\_SERVER\_CERT options to the [CHANGE MASTER TO](#page-32-0) statement. See [Section 13.4.2.1, "CHANGE MASTER TO Statement"](#page-32-0).

• Seconds\_Behind\_Master

This field is an indication of how "late" the replica is:

- When the replica is actively processing updates, this field shows the difference between the current timestamp on the replica and the original timestamp logged on the source for the event currently being processed on the replica.
- When no event is currently being processed on the replica, this value is 0.

In essence, this field measures the time difference in seconds between the replica SQL thread and the replica I/O thread. If the network connection between source and replica is fast, the replica I/ O thread is very close to the source, so this field is a good approximation of how late the replica SQL thread is compared to the source. If the network is slow, this is not a good approximation; the replica SQL thread may quite often be caught up with the slow-reading replica I/O thread, so Seconds\_Behind\_Master often shows a value of 0, even if the I/O thread is late compared to the source. In other words, this column is useful only for fast networks.

This time difference computation works even if the source and replica do not have identical clock times, provided that the difference, computed when the replica I/O thread starts, remains constant from then on. Any changes—including NTP updates—can lead to clock skews that can make calculation of Seconds\_Behind\_Master less reliable.

In MySQL 5.7, this field is NULL (undefined or unknown) if the replica SQL thread is not running, or if the SQL thread has consumed all of the relay log and the replica I/O thread is not running. (In older versions of MySQL, this field was NULL if the replica SQL thread or the replica I/O thread was not running or was not connected to the source.) If the I/O thread is running but the relay log is exhausted, Seconds\_Behind\_Master is set to 0.

The value of Seconds\_Behind\_Master is based on the timestamps stored in events, which are preserved through replication. This means that if a source M1 is itself a replica of M0, any event from M1's binary log that originates from M0's binary log has M0's timestamp for that event. This enables MySQL to replicate TIMESTAMP successfully. However, the problem for Seconds\_Behind\_Master is that if M1 also receives direct updates from clients, the Seconds\_Behind\_Master value randomly fluctuates because sometimes the last event from M1 originates from M0 and sometimes is the result of a direct update on M1.

When using a multithreaded replica, you should keep in mind that this value is based on Exec\_Master\_Log\_Pos, and so may not reflect the position of the most recently committed transaction.

• Last\_IO\_Errno, Last\_IO\_Error

The error number and error message of the most recent error that caused the I/O thread to stop. An error number of 0 and message of the empty string mean "no error." If the Last\_IO\_Error value is not empty, the error values also appear in the replica's error log.

I/O error information includes a timestamp showing when the most recent I/O thread error occurred. This timestamp uses the format YYMMDD hh:mm:ss, and appears in the Last\_IO\_Error\_Timestamp column.

Issuing [RESET MASTER](#page-30-0) or [RESET SLAVE](#page-40-0) resets the values shown in these columns.

• Last\_SQL\_Errno, Last\_SQL\_Error

The error number and error message of the most recent error that caused the SQL thread to stop. An error number of 0 and message of the empty string mean "no error." If the Last\_SQL\_Error value is not empty, the error values also appear in the replica's error log.

If the replica is multithreaded, the SQL thread is the coordinator for worker threads. In this case, the Last\_SQL\_Error field shows exactly what the Last\_Error\_Message column in the Performance Schema replication\_applier\_status\_by\_coordinator table shows. The field value is modified to suggest that there may be more failures in the other worker threads which can be seen in the replication\_applier\_status\_by\_worker table that shows each worker thread's status. If that table is not available, the replica error log can be used. The log or the replication\_applier\_status\_by\_worker table should also be used to learn more about the failure shown by [SHOW SLAVE STATUS](#page-167-0) or the coordinator table.

SQL error information includes a timestamp showing when the most recent SQL thread error occurred. This timestamp uses the format YYMMDD hh:mm:ss, and appears in the Last\_SQL\_Error\_Timestamp column.

Issuing [RESET MASTER](#page-30-0) or [RESET SLAVE](#page-40-0) resets the values shown in these columns.

In MySQL 5.7, all error codes and messages displayed in the Last\_SQL\_Errno and Last\_SQL\_Error columns correspond to error values listed in [Server Error Message Reference.](https://dev.mysql.com/doc/mysql-errors/5.7/en/server-error-reference.md) This was not always true in previous versions. (Bug #11760365, Bug #52768)

• Replicate\_Ignore\_Server\_Ids

In MySQL 5.7, you set a replica to ignore events from 0 or more sources using the IGNORE\_SERVER\_IDS option of the [CHANGE MASTER TO](#page-32-0) statement. By default this is blank, and is usually modified only when using a circular or other multi-source replication setup. The message shown for Replicate\_Ignore\_Server\_Ids when not blank consists of a comma-delimited list of one or more numbers, indicating the server IDs to be ignored. For example:

Replicate\_Ignore\_Server\_Ids: 2, 6, 9

![](_page_172_Picture_4.jpeg)

#### **Note**

Ignored\_server\_ids also shows the server IDs to be ignored, but is a space-delimited list, which is preceded by the total number of server IDs to be ignored. For example, if a [CHANGE MASTER TO](#page-32-0) statement containing the IGNORE\_SERVER\_IDS = (2,6,9) option has been issued to tell a replica to ignore sources having the server ID 2, 6, or 9, that information appears as shown here:

Ignored\_server\_ids: 3, 2, 6, 9

The first number (in this case 3) shows the number of server IDs being ignored.

Replicate\_Ignore\_Server\_Ids filtering is performed by the I/O thread, rather than by the SQL thread, which means that events which are filtered out are not written to the relay log. This differs from the filtering actions taken by server options such --replicate-do-table, which apply to the SQL thread.

• Master\_Server\_Id

The server\_id value from the source.

• Master\_UUID

The server\_uuid value from the source.

• Master\_Info\_File

The location of the master.info file.

• SQL\_Delay

The number of seconds that the replica must lag the source.

• SQL\_Remaining\_Delay

When Slave\_SQL\_Running\_State is Waiting until MASTER\_DELAY seconds after master executed event, this field contains the number of delay seconds remaining. At other times, this field is NULL.

• Slave\_SQL\_Running\_State

The state of the SQL thread (analogous to Slave\_IO\_State). The value is identical to the State value of the SQL thread as displayed by [SHOW PROCESSLIST](#page-160-0). Section 8.14.7, "Replication Replica SQL Thread States", provides a listing of possible states

• Master\_Retry\_Count

The number of times the replica can attempt to reconnect to the source in the event of a lost connection. This value can be set using the MASTER\_RETRY\_COUNT option of the [CHANGE MASTER](#page-32-0) [TO](#page-32-0) statement (preferred) or the older --master-retry-count server option (still supported for backward compatibility).

• Master\_Bind

The network interface that the replica is bound to, if any. This is set using the MASTER\_BIND option for the [CHANGE MASTER TO](#page-32-0) statement.

• Last\_IO\_Error\_Timestamp

A timestamp in YYMMDD hh:mm:ss format that shows when the most recent I/O error took place.

• Last\_SQL\_Error\_Timestamp

A timestamp in YYMMDD hh:mm:ss format that shows when the most recent SQL error occurred.

• Retrieved\_Gtid\_Set

The set of global transaction IDs corresponding to all transactions received by this replica. Empty if GTIDs are not in use. See GTID Sets for more information.

This is the set of all GTIDs that exist or have existed in the relay logs. Each GTID is added as soon as the Gtid\_log\_event is received. This can cause partially transmitted transactions to have their GTIDs included in the set.

When all relay logs are lost due to executing [RESET SLAVE](#page-40-0) or [CHANGE MASTER TO](#page-32-0), or due to the effects of the --relay-log-recovery option, the set is cleared. When relay\_log\_purge = 1, the newest relay log is always kept, and the set is not cleared.

• Executed\_Gtid\_Set

The set of global transaction IDs written in the binary log. This is the same as the value for the global gtid\_executed system variable on this server, as well as the value for Executed\_Gtid\_Set in the output of [SHOW MASTER STATUS](#page-156-0) on this server. Empty if GTIDs are not in use. See GTID Sets for more information.

• Auto\_Position

1 if autopositioning is in use; otherwise 0.

• Replicate\_Rewrite\_DB

The Replicate\_Rewrite\_DB value displays any replication filtering rules that were specified. For example, if the following replication filter rule was set:

```
CHANGE REPLICATION FILTER REPLICATE_REWRITE_DB=((db1,db2), (db3,db4));
```

the Replicate\_Rewrite\_DB value displays:

```
Replicate_Rewrite_DB: (db1,db2),(db3,db4)
```

For more information, see [Section 13.4.2.2, "CHANGE REPLICATION FILTER Statement".](#page-38-0)

• Channel\_name

The replication channel which is being displayed. There is always a default replication channel, and more replication channels can be added. See Section 16.2.2, "Replication Channels" for more information.

• Master\_TLS\_Version

The TLS version used on the source. For TLS version information, see Section 6.3.2, "Encrypted Connection TLS Protocols and Ciphers". This column was added in MySQL 5.7.10.

## <span id="page-173-0"></span>**13.7.5.35 SHOW STATUS Statement**

```
SHOW [GLOBAL | SESSION] STATUS
```

[LIKE 'pattern' | WHERE expr]

![](_page_174_Picture_2.jpeg)

### **Note**

The value of the show\_compatibility\_56 system variable affects the information available from and privileges required for the statement described here. For details, see the description of that variable in Section 5.1.7, "Server System Variables".

[SHOW STATUS](#page-173-0) provides server status information (see Section 5.1.9, "Server Status Variables"). This statement does not require any privilege. It requires only the ability to connect to the server.

Status variable information is also available from these sources:

- Performance Schema tables. See Section 25.12.14, "Performance Schema Status Variable Tables".
- The GLOBAL\_STATUS and SESSION\_STATUS tables. See Section 24.3.10, "The INFORMATION\_SCHEMA GLOBAL\_STATUS and SESSION\_STATUS Tables".
- The mysqladmin extended-status command. See Section 4.5.2, "mysqladmin A MySQL Server Administration Program".

For [SHOW STATUS](#page-173-0), a LIKE clause, if present, indicates which variable names to match. A WHERE clause can be given to select rows using more general conditions, as discussed in Section 24.8, "Extensions to SHOW Statements".

[SHOW STATUS](#page-173-0) accepts an optional GLOBAL or SESSION variable scope modifier:

- With a GLOBAL modifier, the statement displays the global status values. A global status variable may represent status for some aspect of the server itself (for example, Aborted\_connects), or the aggregated status over all connections to MySQL (for example, Bytes\_received and Bytes\_sent). If a variable has no global value, the session value is displayed.
- With a SESSION modifier, the statement displays the status variable values for the current connection. If a variable has no session value, the global value is displayed. LOCAL is a synonym for SESSION.
- If no modifier is present, the default is SESSION.

The scope for each status variable is listed at Section 5.1.9, "Server Status Variables".

Each invocation of the [SHOW STATUS](#page-173-0) statement uses an internal temporary table and increments the global Created\_tmp\_tables value.

Partial output is shown here. The list of names and values may differ for your server. The meaning of each variable is given in Section 5.1.9, "Server Status Variables".

| mysql> SHOW STATUS;                  |                  |  |
|--------------------------------------|------------------|--|
| +++<br>  Variable_name<br>+++        | Value            |  |
| Aborted_clients                      | 0                |  |
| Aborted_connects<br>  Bytes_received | 0<br>  155372598 |  |
| Bytes_sent                           | 1176560426       |  |
| Connections                          | 30023            |  |
| Created_tmp_disk_tables   0          |                  |  |
| Created_tmp_tables                   | 8340             |  |
| Created_tmp_files<br>                | 60               |  |
| Open_tables                          | 1                |  |
| Open_files                           | 2                |  |
| Open_streams                         | 0                |  |
| Opened_tables                        | 44600            |  |
| Questions                            | 2026873          |  |

```
...
| Table_locks_immediate | 1920382 |
| Table_locks_waited | 0 |
| Threads_cached | 0 |
| Threads_created | 30022 |
| Threads_connected | 1 |
| Threads_running | 1 |
| Uptime | 80380 |
+--------------------------+------------+
```

With a LIKE clause, the statement displays only rows for those variables with names that match the pattern:

```
mysql> SHOW STATUS LIKE 'Key%';
+--------------------+----------+
| Variable_name | Value |
+--------------------+----------+
| Key_blocks_used | 14955 |
| Key_read_requests | 96854827 |
| Key_reads | 162040 |
| Key_write_requests | 7589728 |
| Key_writes | 3813196 |
+--------------------+----------+
```

## <span id="page-175-0"></span>**13.7.5.36 SHOW TABLE STATUS Statement**

```
SHOW TABLE STATUS
 [{FROM | IN} db_name]
 [LIKE 'pattern' | WHERE expr]
```

[SHOW TABLE STATUS](#page-175-0) works likes [SHOW TABLES](#page-178-0), but provides a lot of information about each non-TEMPORARY table. You can also get this list using the mysqlshow --status db\_name command. The LIKE clause, if present, indicates which table names to match. The WHERE clause can be given to select rows using more general conditions, as discussed in Section 24.8, "Extensions to SHOW Statements".

This statement also displays information about views.

[SHOW TABLE STATUS](#page-175-0) output has these columns:

• Name

The name of the table.

• Engine

The storage engine for the table. See Chapter 14, The InnoDB Storage Engine, and Chapter 15, Alternative Storage Engines.

For partitioned tables, Engine shows the name of the storage engine used by all partitions.

• Version

The version number of the table's .frm file.

• Row\_format

The row-storage format (Fixed, Dynamic, Compressed, Redundant, Compact). For MyISAM tables, Dynamic corresponds to what myisamchk -dvv reports as Packed. InnoDB table format is either Redundant or Compact when using the Antelope file format, or Compressed or Dynamic when using the Barracuda file format.

• Rows

The number of rows. Some storage engines, such as MyISAM, store the exact count. For other storage engines, such as InnoDB, this value is an approximation, and may vary from the actual value by as much as 40% to 50%. In such cases, use SELECT COUNT(\*) to obtain an accurate count.

The Rows value is NULL for INFORMATION\_SCHEMA tables.

For InnoDB tables, the row count is only a rough estimate used in SQL optimization. (This is also true if the InnoDB table is partitioned.)

• Avg\_row\_length

The average row length.

Refer to the notes at the end of this section for related information.

• Data\_length

For MyISAM, Data\_length is the length of the data file, in bytes.

For InnoDB, Data\_length is the approximate amount of space allocated for the clustered index, in bytes. Specifically, it is the clustered index size, in pages, multiplied by the InnoDB page size.

Refer to the notes at the end of this section for information regarding other storage engines.

• Max\_data\_length

For MyISAM, Max\_data\_length is maximum length of the data file. This is the total number of bytes of data that can be stored in the table, given the data pointer size used.

Unused for InnoDB.

Refer to the notes at the end of this section for information regarding other storage engines.

• Index\_length

For MyISAM, Index\_length is the length of the index file, in bytes.

For InnoDB, Index\_length is the approximate amount of space allocated for non-clustered indexes, in bytes. Specifically, it is the sum of non-clustered index sizes, in pages, multiplied by the InnoDB page size.

Refer to the notes at the end of this section for information regarding other storage engines.

• Data\_free

The number of allocated but unused bytes.

InnoDB tables report the free space of the tablespace to which the table belongs. For a table located in the shared tablespace, this is the free space of the shared tablespace. If you are using multiple tablespaces and the table has its own tablespace, the free space is for only that table. Free space means the number of bytes in completely free extents minus a safety margin. Even if free space displays as 0, it may be possible to insert rows as long as new extents need not be allocated.

For NDB Cluster, Data\_free shows the space allocated on disk for, but not used by, a Disk Data table or fragment on disk. (In-memory data resource usage is reported by the Data\_length column.)

For partitioned tables, this value is only an estimate and may not be absolutely correct. A more accurate method of obtaining this information in such cases is to query the INFORMATION\_SCHEMA PARTITIONS table, as shown in this example:

```
SELECT SUM(DATA_FREE)
 FROM INFORMATION_SCHEMA.PARTITIONS
 WHERE TABLE_SCHEMA = 'mydb'
```

```
 AND TABLE_NAME = 'mytable';
```

For more information, see Section 24.3.16, "The INFORMATION\_SCHEMA PARTITIONS Table".

• Auto\_increment

The next AUTO\_INCREMENT value.

• Create\_time

When the table was created.

• Update\_time

When the data file was last updated. For some storage engines, this value is NULL. For example, InnoDB stores multiple tables in its system tablespace and the data file timestamp does not apply. Even with file-per-table mode with each InnoDB table in a separate .ibd file, change buffering can delay the write to the data file, so the file modification time is different from the time of the last insert, update, or delete. For MyISAM, the data file timestamp is used; however, on Windows the timestamp is not updated by updates, so the value is inaccurate.

Update\_time displays a timestamp value for the last [UPDATE](#page-8-0), INSERT, or DELETE performed on InnoDB tables that are not partitioned. For MVCC, the timestamp value reflects the [COMMIT](#page-11-0) time, which is considered the last update time. Timestamps are not persisted when the server is restarted or when the table is evicted from the InnoDB data dictionary cache.

The Update\_time column also shows this information for partitioned InnoDB tables.

• Check\_time

When the table was last checked. Not all storage engines update this time, in which case, the value is always NULL.

For partitioned InnoDB tables, Check\_time is always NULL.

• Collation

The table default collation. The output does not explicitly list the table default character set, but the collation name begins with the character set name.

• Checksum

The live checksum value, if any.

• Create\_options

Extra options used with CREATE TABLE.

Create\_options shows partitioned for a partitioned table.

Create\_options shows the ENCRYPTION option specified when creating or altering a file-per-table tablespace.

When creating a table with strict mode disabled, the storage engine's default row format is used if the specified row format is not supported. The actual row format of the table is reported in the Row\_format column. Create\_options shows the row format that was specified in the CREATE TABLE statement.

When altering the storage engine of a table, table options that are not applicable to the new storage engine are retained in the table definition to enable reverting the table with its previously defined options to the original storage engine, if necessary. Create\_options may show retained options.

• Comment

The comment used when creating the table (or information as to why MySQL could not access the table information).

### **Notes**

- For InnoDB tables, [SHOW TABLE STATUS](#page-175-0) does not give accurate statistics except for the physical size reserved by the table. The row count is only a rough estimate used in SQL optimization.
- For NDB tables, the output of this statement shows appropriate values for the Avg\_row\_length and Data\_length columns, with the exception that BLOB columns are not taken into account.
- For NDB tables, Data\_length includes data stored in main memory only; the Max\_data\_length and Data\_free columns apply to Disk Data.
- For NDB Cluster Disk Data tables, Max\_data\_length shows the space allocated for the disk part of a Disk Data table or fragment. (In-memory data resource usage is reported by the Data\_length column.)
- For MEMORY tables, the Data\_length, Max\_data\_length, and Index\_length values approximate the actual amount of allocated memory. The allocation algorithm reserves memory in large amounts to reduce the number of allocation operations.
- For views, all columns displayed by [SHOW TABLE STATUS](#page-175-0) are NULL except that Name indicates the view name and Comment says VIEW.

Table information is also available from the INFORMATION\_SCHEMA TABLES table. See Section 24.3.25, "The INFORMATION\_SCHEMA TABLES Table".

## <span id="page-178-0"></span>**13.7.5.37 SHOW TABLES Statement**

```
SHOW [FULL] TABLES
 [{FROM | IN} db_name]
 [LIKE 'pattern' | WHERE expr]
```

[SHOW TABLES](#page-178-0) lists the non-TEMPORARY tables in a given database. You can also get this list using the mysqlshow db\_name command. The LIKE clause, if present, indicates which table names to match. The WHERE clause can be given to select rows using more general conditions, as discussed in Section 24.8, "Extensions to SHOW Statements".

Matching performed by the LIKE clause is dependent on the setting of the lower\_case\_table\_names system variable.

This statement also lists any views in the database. The optional FULL modifier causes [SHOW TABLES](#page-178-0) to display a second output column with values of BASE TABLE for a table, VIEW for a view, or SYSTEM VIEW for an INFORMATION\_SCHEMA table.

If you have no privileges for a base table or view, it does not show up in the output from [SHOW TABLES](#page-178-0) or mysqlshow db\_name.

Table information is also available from the INFORMATION\_SCHEMA TABLES table. See Section 24.3.25, "The INFORMATION\_SCHEMA TABLES Table".

## <span id="page-178-1"></span>**13.7.5.38 SHOW TRIGGERS Statement**

```
SHOW TRIGGERS
 [{FROM | IN} db_name]
 [LIKE 'pattern' | WHERE expr]
```

[SHOW TRIGGERS](#page-178-1) lists the triggers currently defined for tables in a database (the default database unless a FROM clause is given). This statement returns results only for databases and tables for which you have the TRIGGER privilege. The LIKE clause, if present, indicates which table names (not trigger names) to match and causes the statement to display triggers for those tables. The WHERE clause can

be given to select rows using more general conditions, as discussed in Section 24.8, "Extensions to SHOW Statements".

For the ins\_sum trigger defined in Section 23.3, "Using Triggers", the output of [SHOW TRIGGERS](#page-178-1) is as shown here:

```
mysql> SHOW TRIGGERS LIKE 'acc%'\G
*************************** 1. row ***************************
 Trigger: ins_sum
 Event: INSERT
 Table: account
 Statement: SET @sum = @sum + NEW.amount
 Timing: BEFORE
 Created: 2018-08-08 10:10:12.61
 sql_mode: ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,
 NO_ZERO_IN_DATE,NO_ZERO_DATE,
 ERROR_FOR_DIVISION_BY_ZERO,
 NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION
 Definer: me@localhost
character_set_client: utf8
collation_connection: utf8_general_ci
 Database Collation: latin1_swedish_ci
```

[SHOW TRIGGERS](#page-178-1) output has these columns:

• Trigger

The name of the trigger.

• Event

The trigger event. This is the type of operation on the associated table for which the trigger activates. The value is INSERT (a row was inserted), DELETE (a row was deleted), or UPDATE (a row was modified).

• Table

The table for which the trigger is defined.

• Statement

The trigger body; that is, the statement executed when the trigger activates.

• Timing

Whether the trigger activates before or after the triggering event. The value is BEFORE or AFTER.

• Created

The date and time when the trigger was created. This is a TIMESTAMP(2) value (with a fractional part in hundredths of seconds) for triggers created in MySQL 5.7.2 or later, NULL for triggers created prior to 5.7.2.

• sql\_mode

The SQL mode in effect when the trigger was created, and under which the trigger executes. For the permitted values, see Section 5.1.10, "Server SQL Modes".

• Definer

The account of the user who created the trigger, in 'user\_name'@'host\_name' format.

• character\_set\_client

The session value of the character\_set\_client system variable when the trigger was created.

• collation\_connection

The session value of the collation\_connection system variable when the trigger was created.

• Database Collation

The collation of the database with which the trigger is associated.

Trigger information is also available from the INFORMATION\_SCHEMA TRIGGERS table. See Section 24.3.29, "The INFORMATION\_SCHEMA TRIGGERS Table".

## <span id="page-180-0"></span>**13.7.5.39 SHOW VARIABLES Statement**

```
SHOW [GLOBAL | SESSION] VARIABLES
 [LIKE 'pattern' | WHERE expr]
```

![](_page_180_Picture_8.jpeg)

#### **Note**

The value of the show\_compatibility\_56 system variable affects the information available from and privileges required for the statement described here. For details, see the description of that variable in Section 5.1.7, "Server System Variables".

[SHOW VARIABLES](#page-180-0) shows the values of MySQL system variables (see Section 5.1.7, "Server System Variables"). This statement does not require any privilege. It requires only the ability to connect to the server.

System variable information is also available from these sources:

- Performance Schema tables. See Section 25.12.13, "Performance Schema System Variable Tables".
- The GLOBAL\_VARIABLES and SESSION\_VARIABLES tables. See Section 24.3.11, "The INFORMATION\_SCHEMA GLOBAL\_VARIABLES and SESSION\_VARIABLES Tables".
- The mysqladmin variables command. See Section 4.5.2, "mysqladmin A MySQL Server Administration Program".

For [SHOW VARIABLES](#page-180-0), a LIKE clause, if present, indicates which variable names to match. A WHERE clause can be given to select rows using more general conditions, as discussed in Section 24.8, "Extensions to SHOW Statements".

[SHOW VARIABLES](#page-180-0) accepts an optional GLOBAL or SESSION variable scope modifier:

- With a GLOBAL modifier, the statement displays global system variable values. These are the values used to initialize the corresponding session variables for new connections to MySQL. If a variable has no global value, no value is displayed.
- With a SESSION modifier, the statement displays the system variable values that are in effect for the current connection. If a variable has no session value, the global value is displayed. LOCAL is a synonym for SESSION.
- If no modifier is present, the default is SESSION.

The scope for each system variable is listed at Section 5.1.7, "Server System Variables".

[SHOW VARIABLES](#page-180-0) is subject to a version-dependent display-width limit. For variables with very long values that are not completely displayed, use SELECT as a workaround. For example:

```
SELECT @@GLOBAL.innodb_data_file_path;
```

Most system variables can be set at server startup (read-only variables such as version\_comment are exceptions). Many can be changed at runtime with the [SET](#page-130-0) statement. See Section 5.1.8, "Using System Variables", and [Section 13.7.4.1, "SET Syntax for Variable Assignment"](#page-130-0).

Partial output is shown here. The list of names and values may differ for your server. Section 5.1.7, "Server System Variables", describes the meaning of each variable, and Section 5.1.1, "Configuring the Server", provides information about tuning them.

```
mysql> SHOW VARIABLES;
+-----------------------------------------+---------------------------+
| Variable_name | Value |
+-----------------------------------------+---------------------------+
| auto_increment_increment | 1 |
| auto_increment_offset | 1 |
| autocommit | ON |
| automatic_sp_privileges | ON |
| back_log | 50 |
| basedir | /home/jon/bin/mysql-5.5 |
| big_tables | OFF |
| binlog_cache_size | 32768 |
| binlog_direct_non_transactional_updates | OFF |
| binlog_format | STATEMENT |
| binlog_stmt_cache_size | 32768 |
| bulk_insert_buffer_size | 8388608 |
...
| max_allowed_packet | 4194304 |
| max_binlog_cache_size | 18446744073709547520 |
| max_binlog_size | 1073741824 |
| max_binlog_stmt_cache_size | 18446744073709547520 |
| max_connect_errors | 100 |
| max_connections | 151 |
| max_delayed_threads | 20 |
| max_error_count | 64 |
| max_heap_table_size | 16777216 |
| max_insert_delayed_threads | 20 |
| max_join_size | 18446744073709551615 |
...
| thread_handling | one-thread-per-connection |
| thread_stack | 262144 |
| time_format | %H:%i:%s |
| time_zone | SYSTEM |
| timestamp | 1316689732 |
| tmp_table_size | 16777216 |
| tmpdir | /tmp |
| transaction_alloc_block_size | 8192 |
| transaction_isolation | REPEATABLE-READ |
| transaction_prealloc_size | 4096 |
| transaction_read_only | OFF |
| tx_isolation | REPEATABLE-READ |
| tx_read_only | OFF |
| unique_checks | ON |
| updatable_views_with_limit | YES |
| version | 5.7.44 |
| version_comment | Source distribution |
| version_compile_machine | x86_64 |
| version_compile_os | Linux |
| wait_timeout | 28800 |
| warning_count | 0 |
+-----------------------------------------+---------------------------+
```

With a LIKE clause, the statement displays only rows for those variables with names that match the pattern. To obtain the row for a specific variable, use a LIKE clause as shown:

```
SHOW VARIABLES LIKE 'max_join_size';
SHOW SESSION VARIABLES LIKE 'max_join_size';
```

To get a list of variables whose name match a pattern, use the % wildcard character in a LIKE clause:

```
SHOW VARIABLES LIKE '%size%';
SHOW GLOBAL VARIABLES LIKE '%size%';
```

Wildcard characters can be used in any position within the pattern to be matched. Strictly speaking, because \_ is a wildcard that matches any single character, you should escape it as \\_ to match it literally. In practice, this is rarely necessary.

# <span id="page-182-0"></span>**13.7.5.40 SHOW WARNINGS Statement**

```
SHOW WARNINGS [LIMIT [offset,] row_count]
SHOW COUNT(*) WARNINGS
```

[SHOW WARNINGS](#page-182-0) is a diagnostic statement that displays information about the conditions (errors, warnings, and notes) resulting from executing a statement in the current session. Warnings are generated for DML statements such as INSERT, [UPDATE](#page-8-0), and LOAD DATA as well as DDL statements such as CREATE TABLE and ALTER TABLE.

The LIMIT clause has the same syntax as for the SELECT statement. See Section 13.2.9, "SELECT Statement".

[SHOW WARNINGS](#page-182-0) is also used following [EXPLAIN](#page-195-0), to display the extended information generated by [EXPLAIN](#page-195-0). See Section 8.8.3, "Extended EXPLAIN Output Format".

[SHOW WARNINGS](#page-182-0) displays information about the conditions resulting from execution of the most recent nondiagnostic statement in the current session. If the most recent statement resulted in an error during parsing, [SHOW WARNINGS](#page-182-0) shows the resulting conditions, regardless of statement type (diagnostic or nondiagnostic).

The [SHOW COUNT\(\\*\) WARNINGS](#page-182-0) diagnostic statement displays the total number of errors, warnings, and notes. You can also retrieve this number from the warning\_count system variable:

```
SHOW COUNT(*) WARNINGS;
SELECT @@warning_count;
```

A difference in these statements is that the first is a diagnostic statement that does not clear the message list. The second, because it is a SELECT statement is considered nondiagnostic and does clear the message list.

A related diagnostic statement, [SHOW ERRORS](#page-151-0), shows only error conditions (it excludes warnings and notes), and [SHOW COUNT\(\\*\) ERRORS](#page-182-0) statement displays the total number of errors. See [Section 13.7.5.17, "SHOW ERRORS Statement"](#page-151-0). [GET DIAGNOSTICS](#page-66-0) can be used to examine information for individual conditions. See [Section 13.6.7.3, "GET DIAGNOSTICS Statement"](#page-66-0).

Here is a simple example that shows data-conversion warnings for INSERT. The example assumes that strict SQL mode is disabled. With strict mode enabled, the warnings would become errors and terminate the INSERT.

```
mysql> CREATE TABLE t1 (a TINYINT NOT NULL, b CHAR(4));
Query OK, 0 rows affected (0.05 sec)
mysql> INSERT INTO t1 VALUES(10,'mysql'), (NULL,'test'), (300,'xyz');
Query OK, 3 rows affected, 3 warnings (0.00 sec)
Records: 3 Duplicates: 0 Warnings: 3
mysql> SHOW WARNINGS\G
*************************** 1. row ***************************
 Level: Warning
 Code: 1265
Message: Data truncated for column 'b' at row 1
*************************** 2. row ***************************
 Level: Warning
 Code: 1048
Message: Column 'a' cannot be null
*************************** 3. row ***************************
 Level: Warning
 Code: 1264
Message: Out of range value for column 'a' at row 3
3 rows in set (0.00 sec)
```

The max\_error\_count system variable controls the maximum number of error, warning, and note messages for which the server stores information, and thus the number of messages that [SHOW](#page-182-0)

[WARNINGS](#page-182-0) displays. To change the number of messages the server can store, change the value of max\_error\_count. The default is 64.

max\_error\_count controls only how many messages are stored, not how many are counted. The value of warning\_count is not limited by max\_error\_count, even if the number of messages generated exceeds max\_error\_count. The following example demonstrates this. The ALTER TABLE statement produces three warning messages (strict SQL mode is disabled for the example to prevent an error from occuring after a single conversion issue). Only one message is stored and displayed because max\_error\_count has been set to 1, but all three are counted (as shown by the value of warning\_count):

```
mysql> SHOW VARIABLES LIKE 'max_error_count';
+-----------------+-------+
| Variable_name | Value |
+-----------------+-------+
| max_error_count | 64 |
+-----------------+-------+
1 row in set (0.00 sec)
mysql> SET max_error_count=1, sql_mode = '';
Query OK, 0 rows affected (0.00 sec)
mysql> ALTER TABLE t1 MODIFY b CHAR;
Query OK, 3 rows affected, 3 warnings (0.00 sec)
Records: 3 Duplicates: 0 Warnings: 3
mysql> SHOW WARNINGS;
+---------+------+----------------------------------------+
| Level | Code | Message |
+---------+------+----------------------------------------+
| Warning | 1263 | Data truncated for column 'b' at row 1 |
+---------+------+----------------------------------------+
1 row in set (0.00 sec)
mysql> SELECT @@warning_count;
+-----------------+
| @@warning_count |
+-----------------+
| 3 |
+-----------------+
1 row in set (0.01 sec)
```

To disable message storage, set max\_error\_count to 0. In this case, warning\_count still indicates how many warnings occurred, but messages are not stored and cannot be displayed.

The sql\_notes system variable controls whether note messages increment warning\_count and whether the server stores them. By default, sql\_notes is 1, but if set to 0, notes do not increment warning\_count and the server does not store them:

```
mysql> SET sql_notes = 1;
mysql> DROP TABLE IF EXISTS test.no_such_table;
Query OK, 0 rows affected, 1 warning (0.00 sec)
mysql> SHOW WARNINGS;
+-------+------+------------------------------------+
| Level | Code | Message |
+-------+------+------------------------------------+
| Note | 1051 | Unknown table 'test.no_such_table' |
+-------+------+------------------------------------+
1 row in set (0.00 sec)
mysql> SET sql_notes = 0;
mysql> DROP TABLE IF EXISTS test.no_such_table;
Query OK, 0 rows affected (0.00 sec)
mysql> SHOW WARNINGS;
Empty set (0.00 sec)
```

The MySQL server sends to each client a count indicating the total number of errors, warnings, and notes resulting from the most recent statement executed by that client. From the C API, this value can be obtained by calling [mysql\\_warning\\_count\(\)](https://dev.mysql.com/doc/c-api/5.7/en/mysql-warning-count.md). See [mysql\\_warning\\_count\(\).](https://dev.mysql.com/doc/c-api/5.7/en/mysql-warning-count.md)

In the mysql client, you can enable and disable automatic warnings display using the warnings and nowarning commands, respectively, or their shortcuts, \W and \w (see Section 4.5.1.2, "mysql Client Commands"). For example:

```
mysql> \W
Show warnings enabled.
mysql> SELECT 1/0;
+------+
| 1/0 |
+------+
| NULL |
+------+
1 row in set, 1 warning (0.03 sec)
Warning (Code 1365): Division by 0
mysql> \w
Show warnings disabled.
```