---
source: MySQL 8.4 Reference
title: 00_Overview
---

## <span id="page-81-1"></span>**15.7.4.1 CREATE FUNCTION Statement for Loadable Functions**

```
CREATE [AGGREGATE] FUNCTION [IF NOT EXISTS] function_name
 RETURNS {STRING|INTEGER|REAL|DECIMAL}
 SONAME shared_library_name
```

This statement loads the loadable function named function\_name. (CREATE FUNCTION is also used to created stored functions; see Section 15.1.17, "CREATE PROCEDURE and CREATE FUNCTION Statements".)

A loadable function is a way to extend MySQL with a new function that works like a native (built-in) MySQL function such as ABS() or CONCAT(). See [Adding a Loadable Function](https://dev.mysql.com/doc/extending-mysql/8.4/en/adding-loadable-function.md).

function\_name is the name that should be used in SQL statements to invoke the function. The RETURNS clause indicates the type of the function's return value. DECIMAL is a legal value after RETURNS, but currently DECIMAL functions return string values and should be written like STRING functions.

IF NOT EXISTS prevents an error from occurring if there already exists a loadable function with the same name. It does not prevent an error from occurring if there already exists a built-in function having the same name. IF NOT EXISTS is also supported for CREATE FUNCTION statements. See Function Name Resolution.

The AGGREGATE keyword, if given, signifies that the function is an aggregate (group) function. An aggregate function works exactly like a native MySQL aggregate function such as SUM() or COUNT().

shared\_library\_name is the base name of the shared library file containing the code that implements the function. The file must be located in the plugin directory. This directory is given by the value of the plugin\_dir system variable. For more information, see Section 7.7.1, "Installing and Uninstalling Loadable Functions".

[CREATE FUNCTION](#page-81-1) requires the INSERT privilege for the mysql system schema because it adds a row to the mysql.func system table to register the function.

[CREATE FUNCTION](#page-81-1) also adds the function to the Performance Schema user\_defined\_functions table that provides runtime information about installed loadable functions. See Section 29.12.22.10, "The user\_defined\_functions Table".

![](_page_81_Picture_16.jpeg)

#### **Note**

Like the mysql.func system table, the Performance Schema user\_defined\_functions table lists loadable functions installed using [CREATE FUNCTION](#page-81-1). Unlike the mysql.func table, the user\_defined\_functions table also lists loadable functions installed automatically by server components or plugins. This difference makes

user\_defined\_functions preferable to mysql.func for checking which loadable functions are installed.

During the normal startup sequence, the server loads functions registered in the mysql.func table. If the server is started with the --skip-grant-tables option, functions registered in the table are not loaded and are unavailable.

![](_page_82_Picture_3.jpeg)

#### **Note**

To upgrade the shared library associated with a loadable function, issue a [DROP](#page-82-0) [FUNCTION](#page-82-0) statement, upgrade the shared library, and then issue a [CREATE](#page-81-1) [FUNCTION](#page-81-1) statement. If you upgrade the shared library first and then use [DROP](#page-82-0) [FUNCTION](#page-82-0), the server may unexpectedly shut down.

## <span id="page-82-0"></span>**15.7.4.2 DROP FUNCTION Statement for Loadable Functions**

```
DROP FUNCTION [IF EXISTS] function_name
```

This statement drops the loadable function named function\_name. (DROP FUNCTION is also used to drop stored functions; see Section 15.1.29, "DROP PROCEDURE and DROP FUNCTION Statements".)

[DROP FUNCTION](#page-82-0) is the complement of [CREATE FUNCTION](#page-81-1). It requires the DELETE privilege for the mysql system schema because it removes the row from the mysql.func system table that registers the function.

[DROP FUNCTION](#page-82-0) also removes the function from the Performance Schema user\_defined\_functions table that provides runtime information about installed loadable functions. See Section 29.12.22.10, "The user\_defined\_functions Table".

During the normal startup sequence, the server loads functions registered in the mysql.func table. Because [DROP FUNCTION](#page-82-0) removes the mysql.func row for the dropped function, the server does not load the function during subsequent restarts.

[DROP FUNCTION](#page-82-0) cannot be used to drop a loadable function that is installed automatically by components or plugins rather than by using [CREATE FUNCTION](#page-81-1). Such a function is also dropped automatically, when the component or plugin that installed it is uninstalled.

![](_page_82_Picture_13.jpeg)

## **Note**

To upgrade the shared library associated with a loadable function, issue a [DROP](#page-82-0) [FUNCTION](#page-82-0) statement, upgrade the shared library, and then issue a [CREATE](#page-81-1) [FUNCTION](#page-81-1) statement. If you upgrade the shared library first and then use [DROP](#page-82-0) [FUNCTION](#page-82-0), the server may unexpectedly shut down.

## <span id="page-82-1"></span>**15.7.4.3 INSTALL COMPONENT Statement**

```
INSTALL COMPONENT component_name [, component_name ...
 [SET variable = expr [, variable = expr] ...] 
 variable: {
 {GLOBAL | @@GLOBAL.} [component_prefix.]system_var_name
 | {PERSIST | @@PERSIST.} [component_prefix.]system_var_name
}
```

This statement installs one or more components, which become active immediately. A component provides services that are available to the server and other components; see Section 7.5, "MySQL Components". [INSTALL COMPONENT](#page-82-1) requires the INSERT privilege for the mysql.component system table because it adds a row to that table to register the component.

#### Example:

```
INSTALL COMPONENT 'file://component1', 'file://component2';
```

A component is named using a URN that begins with file:// and indicates the base name of the library file that implements the component, located in the directory named by the plugin\_dir system variable. Component names do not include any platform-dependent file name suffix such as .so or .dll. (These naming details are subject to change because component name interpretation is itself performed by a service and the component infrastructure makes it possible to replace the default service implementation with alternative implementations.)

[INSTALL COMPONENT](#page-82-1) permits setting the values of component system variables when you install one or more components. The SET clause enables you to specify variable values precisely when they are needed, without the inconvenience or limitations associated with other forms of assignment. Specifically, you can also set component variables with these alternatives:

- At server startup using options on the command line or in an option file, but doing so involves a server restart. The values do not take effect until you install the component. You can specify an invalid variable name for a component on the command line without triggering an error.
- Dynamically while the server is running by means of the SET statement, which enables you to modify operation of the server without having to stop and restart it. Setting a read-only variable is not permitted.

The optional SET clause applies a value, or values, only to the component specified in the [INSTALL](#page-82-1) [COMPONENT](#page-82-1) statement, rather than to all subsequent installations of that component. SET GLOBAL| PERSIST works for all types of variables, including read-only variables, without having to restart the server. A component system variable that you set using [INSTALL COMPONENT](#page-82-1) takes precedence over any conflicting value coming from the command line or an option file.

#### Example:

```
INSTALL COMPONENT 'file://component1', 'file://component2' 
 SET GLOBAL component1.var1 = 12 + 3, PERSIST component2.var2 = 'strings';
```

Omitting PERSIST or GLOBAL is equivalent to specifying GLOBAL.

Specifying PERSIST for any variable in SET silently executes SET PERSIST\_ONLY immediately after [INSTALL COMPONENT](#page-82-1) loads the components, but before updating the mysql.component table. If SET PERSIST\_ONLY fails, then the server unloads all of the previously loaded new components without persisting anything to mysql.component.

The SET clause accepts only valid variable names of the component being installed and emits an error message for all invalid names. Subqueries, stored functions, and aggregate functions are not permitted as part of the value expression. If you install a single component, it is not necessary to prefix the variable name with the component name.

![](_page_83_Picture_11.jpeg)

#### **Note**

While specifying a variable value using the SET clause is similar to that of the command line—it is available immediately at variable registration there is a distinct difference in how the SET clause handles invalid numerical values for boolean variables. For example, if you set a boolean variable to 11 (component1.boolvar = 11), you see the following behavior:

- SET clause yields true
- Command line yields false (11 is neither ON nor 1)

If any error occurs, the statement fails and has no effect. For example, this happens if a component name is erroneous, a named component does not exist or is already installed, or component initialization fails.

A loader service handles component loading, which includes adding installed components to the mysql.component system table that serves as a registry. For subsequent server restarts, any

components listed in mysql.component are loaded by the loader service during the startup sequence. This occurs even if the server is started with the --skip-grant-tables option.

If a component depends on services not present in the registry and you attempt to install the component without also installing the component or components that provide the services on which it depends, an error occurs:

```
ERROR 3527 (HY000): Cannot satisfy dependency for service 'component_a'
required by component 'component_b'.
```

To avoid this problem, either install all components in the same statement, or install the dependent component after installing any components on which it depends.

![](_page_84_Picture_5.jpeg)

#### **Note**

For keyring components, do not use [INSTALL COMPONENT](#page-82-1). Instead, configure keyring component loading using a manifest file. See Section 8.4.4.2, "Keyring Component Installation".

## <span id="page-84-0"></span>**15.7.4.4 INSTALL PLUGIN Statement**

```
INSTALL PLUGIN plugin_name SONAME 'shared_library_name'
```

This statement installs a server plugin. It requires the INSERT privilege for the mysql.plugin system table because it adds a row to that table to register the plugin.

plugin\_name is the name of the plugin as defined in the plugin descriptor structure contained in the library file (see [Plugin Data Structures](https://dev.mysql.com/doc/extending-mysql/8.4/en/plugin-data-structures.md)). Plugin names are not case-sensitive. For maximal compatibility, plugin names should be limited to ASCII letters, digits, and underscore because they are used in C source files, shell command lines, M4 and Bourne shell scripts, and SQL environments.

shared\_library\_name is the name of the shared library that contains the plugin code. The name includes the file name extension (for example, libmyplugin.so, libmyplugin.dll, or libmyplugin.dylib).

The shared library must be located in the plugin directory (the directory named by the plugin\_dir system variable). The library must be in the plugin directory itself, not in a subdirectory. By default, plugin\_dir is the plugin directory under the directory named by the pkglibdir configuration variable, but it can be changed by setting the value of plugin\_dir at server startup. For example, set its value in a my.cnf file:

```
[mysqld]
plugin_dir=/path/to/plugin/directory
```

If the value of plugin\_dir is a relative path name, it is taken to be relative to the MySQL base directory (the value of the basedir system variable).

[INSTALL PLUGIN](#page-84-0) loads and initializes the plugin code to make the plugin available for use. A plugin is initialized by executing its initialization function, which handles any setup that the plugin must perform before it can be used. When the server shuts down, it executes the deinitialization function for each plugin that is loaded so that the plugin has a chance to perform any final cleanup.

[INSTALL PLUGIN](#page-84-0) also registers the plugin by adding a line that indicates the plugin name and library file name to the mysql.plugin system table. During the normal startup sequence, the server loads and initializes plugins registered in mysql.plugin. This means that a plugin is installed with [INSTALL](#page-84-0) [PLUGIN](#page-84-0) only once, not every time the server starts. If the server is started with the --skip-granttables option, plugins registered in the mysql.plugin table are not loaded and are unavailable.

A plugin library can contain multiple plugins. For each of them to be installed, use a separate [INSTALL](#page-84-0) [PLUGIN](#page-84-0) statement. Each statement names a different plugin, but all of them specify the same library name.

[INSTALL PLUGIN](#page-84-0) causes the server to read option (my.cnf) files just as during server startup. This enables the plugin to pick up any relevant options from those files. It is possible to add plugin options to an option file even before loading a plugin (if the loose prefix is used). It is also possible to uninstall a plugin, edit my.cnf, and install the plugin again. Restarting the plugin this way enables it to the new option values without a server restart.

For options that control individual plugin loading at server startup, see Section 7.6.1, "Installing and Uninstalling Plugins". If you need to load plugins for a single server startup when the --skip-granttables option is given (which tells the server not to read system tables), use the --plugin-load option. See Section 7.1.7, "Server Command Options".

To remove a plugin, use the [UNINSTALL PLUGIN](#page-85-0) statement.

For additional information about plugin loading, see Section 7.6.1, "Installing and Uninstalling Plugins".

To see what plugins are installed, use the [SHOW PLUGINS](#page-119-0) statement or query the INFORMATION\_SCHEMA the PLUGINS table.

If you recompile a plugin library and need to reinstall it, you can use either of the following methods:

- Use [UNINSTALL PLUGIN](#page-85-0) to uninstall all plugins in the library, install the new plugin library file in the plugin directory, and then use [INSTALL PLUGIN](#page-84-0) to install all plugins in the library. This procedure has the advantage that it can be used without stopping the server. However, if the plugin library contains many plugins, you must issue many [INSTALL PLUGIN](#page-84-0) and [UNINSTALL PLUGIN](#page-85-0) statements.
- Stop the server, install the new plugin library file in the plugin directory, and restart the server.

## <span id="page-85-1"></span>**15.7.4.5 UNINSTALL COMPONENT Statement**

```
UNINSTALL COMPONENT component_name [, component_name ] ...
```

This statement deactivates and uninstalls one or more components. A component provides services that are available to the server and other components; see Section 7.5, "MySQL Components". [UNINSTALL COMPONENT](#page-85-1) is the complement of [INSTALL COMPONENT](#page-82-1). It requires the DELETE privilege for the mysql.component system table because it removes the row from that table that registers the component. [UNINSTALL COMPONENT](#page-85-1) does not undo persisted variables, including the variables persisted using INSTALL COMPONENT ... SET PERSIST.

#### Example:

```
UNINSTALL COMPONENT 'file://component1', 'file://component2';
```

For information about component naming, see [Section 15.7.4.3, "INSTALL COMPONENT Statement".](#page-82-1)

If any error occurs, the statement fails and has no effect. For example, this happens if a component name is erroneous, a named component is not installed, or cannot be uninstalled because other installed components depend on it.

A loader service handles component unloading, which includes removing uninstalled components from the mysql.component system table that serves as a registry. As a result, unloaded components are not loaded during the startup sequence for subsequent server restarts.

![](_page_85_Picture_17.jpeg)

#### **Note**

This statement has no effect for keyring components, which are loaded using a manifest file and cannot be uninstalled. See Section 8.4.4.2, "Keyring Component Installation".

## <span id="page-85-0"></span>**15.7.4.6 UNINSTALL PLUGIN Statement**

UNINSTALL PLUGIN plugin\_name

This statement removes an installed server plugin. [UNINSTALL PLUGIN](#page-85-0) is the complement of [INSTALL PLUGIN](#page-84-0). It requires the DELETE privilege for the mysql.plugin system table because it removes the row from that table that registers the plugin.

plugin\_name must be the name of some plugin that is listed in the mysql.plugin table. The server executes the plugin's deinitialization function and removes the row for the plugin from the mysql.plugin system table, so that subsequent server restarts do not load and initialize the plugin. [UNINSTALL PLUGIN](#page-85-0) does not remove the plugin's shared library file.

You cannot uninstall a plugin if any table that uses it is open.

Plugin removal has implications for the use of associated tables. For example, if a full-text parser plugin is associated with a FULLTEXT index on the table, uninstalling the plugin makes the table unusable. Any attempt to access the table results in an error. The table cannot even be opened, so you cannot drop an index for which the plugin is used. This means that uninstalling a plugin is something to do with care unless you do not care about the table contents. If you are uninstalling a plugin with no intention of reinstalling it later and you care about the table contents, you should dump the table with mysqldump and remove the WITH PARSER clause from the dumped CREATE TABLE statement so that you can reload the table later. If you do not care about the table, DROP TABLE can be used even if any plugins associated with the table are missing.

For additional information about plugin loading, see Section 7.6.1, "Installing and Uninstalling Plugins".

## <span id="page-86-0"></span>**15.7.5 CLONE Statement**

```
CLONE clone_action
clone_action: {
 LOCAL DATA DIRECTORY [=] 'clone_dir';
 | INSTANCE FROM 'user'@'host':port
 IDENTIFIED BY 'password'
 [DATA DIRECTORY [=] 'clone_dir']
 [REQUIRE [NO] SSL]
}
```

The [CLONE](#page-86-0) statement is used to clone data locally or from a remote MySQL server instance. To use [CLONE](#page-86-0) syntax, the clone plugin must be installed. See Section 7.6.7, "The Clone Plugin".

[CLONE LOCAL DATA DIRECTORY](#page-86-0) syntax clones data from the local MySQL data directory to a directory on the same server or node where the MySQL server instance runs. The 'clone\_dir' directory is the full path of the local directory that data is cloned to. An absolute path is required. The specified directory must not exist, but the specified path must be an existent path. The MySQL server requires the necessary write access to create the specified directory. For more information, see Section 7.6.7.2, "Cloning Data Locally".

[CLONE INSTANCE](#page-86-0) syntax clones data from a remote MySQL server instance (the donor) and transfers it to the MySQL instance where the cloning operation was initiated (the recipient).

- user is the clone user on the donor MySQL server instance.
- host is the hostname address of the donor MySQL server instance. Internet Protocol version 6 (IPv6) address format is not supported. An alias to the IPv6 address can be used instead. An IPv4 address can be used as is.
- port is the port number of the donor MySQL server instance. (The X Protocol port specified by mysqlx\_port is not supported. Connecting to the donor MySQL server instance through MySQL Router is also not supported.)
- IDENTIFIED BY 'password' specifies the password of the clone user on the donor MySQL server instance.
- DATA DIRECTORY [=] 'clone\_dir' is an optional clause used to specify a directory on the recipient for the data you are cloning. Use this option if you do not want to remove existing data

in the recipient data directory. An absolute path is required, and the directory must not exist. The MySQL server must have the necessary write access to create the directory.

When the optional DATA DIRECTORY [=] 'clone\_dir' clause is not used, a cloning operation removes existing data in the recipient data directory, replaces it with the cloned data, and automatically restarts the server afterward.

• [REQUIRE [NO] SSL] explicitly specifies whether an encrypted connection is to be used or not when transferring cloned data over the network. An error is returned if the explicit specification cannot be satisfied. If an SSL clause is not specified, clone attempts to establish an encrypted connection by default, falling back to an insecure connection if the secure connection attempt fails. A secure connection is required when cloning encrypted data regardless of whether this clause is specified. For more information, see Configuring an Encrypted Connection for Cloning.

For additional information about cloning data from a remote MySQL server instance, see Section 7.6.7.3, "Cloning Remote Data".

## <span id="page-87-1"></span>**15.7.6 SET Statements**

The [SET](#page-87-1) statement has several forms. Descriptions for those forms that are not associated with a specific server capability appear in subsections of this section:

- SET [var\\_name](#page-87-0) = value enables you to assign values to variables that affect the operation of the server or clients. See [Section 15.7.6.1, "SET Syntax for Variable Assignment".](#page-87-0)
- [SET CHARACTER SET](#page-92-0) and [SET NAMES](#page-92-1) assign values to character set and collation variables associated with the current connection to the server. See [Section 15.7.6.2, "SET CHARACTER SET](#page-92-0) [Statement",](#page-92-0) and [Section 15.7.6.3, "SET NAMES Statement".](#page-92-1)

Descriptions for the other forms appear elsewhere, grouped with other statements related to the capability they help implement:

- [SET DEFAULT ROLE](#page-59-0) and [SET ROLE](#page-62-0) set the default role and current role for user accounts. See [Section 15.7.1.9, "SET DEFAULT ROLE Statement",](#page-59-0) and [Section 15.7.1.11, "SET ROLE Statement".](#page-62-0)
- [SET PASSWORD](#page-60-0) assigns account passwords. See [Section 15.7.1.10, "SET PASSWORD Statement"](#page-60-0).
- SET RESOURCE GROUP assigns threads to a resource group. See [Section 15.7.2.4, "SET](#page-66-0) [RESOURCE GROUP Statement".](#page-66-0)
- SET TRANSACTION ISOLATION LEVEL sets the isolation level for transaction processing. See Section 15.3.7, "SET TRANSACTION Statement".

## <span id="page-87-0"></span>**15.7.6.1 SET Syntax for Variable Assignment**

```
SET variable = expr [, variable = expr] ...
variable: {
 user_var_name
 | param_name
 | local_var_name
 | {GLOBAL | @@GLOBAL.} system_var_name
 | {PERSIST | @@PERSIST.} system_var_name
 | {PERSIST_ONLY | @@PERSIST_ONLY.} system_var_name
 | [SESSION | @@SESSION. | @@] system_var_name
}
```

[SET](#page-87-0) syntax for variable assignment enables you to assign values to different types of variables that affect the operation of the server or clients:

- User-defined variables. See Section 11.4, "User-Defined Variables".
- Stored procedure and function parameters, and stored program local variables. See Section 15.6.4, "Variables in Stored Programs".

• System variables. See Section 7.1.8, "Server System Variables". System variables also can be set at server startup, as described in Section 7.1.9, "Using System Variables".

A [SET](#page-87-0) statement that assigns variable values is not written to the binary log, so in replication scenarios it affects only the host on which you execute it. To affect all replication hosts, execute the statement on each host.

The following sections describe [SET](#page-87-0) syntax for setting variables. They use the = assignment operator, but the := assignment operator is also permitted for this purpose.

- [User-Defined Variable Assignment](#page-88-0)
- [Parameter and Local Variable Assignment](#page-88-1)
- [System Variable Assignment](#page-88-2)
- [SET Error Handling](#page-90-0)
- [Multiple Variable Assignment](#page-91-0)
- [System Variable References in Expressions](#page-91-1)

### <span id="page-88-0"></span>**User-Defined Variable Assignment**

User-defined variables are created locally within a session and exist only within the context of that session; see Section 11.4, "User-Defined Variables".

A user-defined variable is written as @var\_name and is assigned an expression value as follows:

```
SET @var_name = expr;
```

#### Examples:

```
SET @name = 43;
SET @total_tax = (SELECT SUM(tax) FROM taxable_transactions);
```

As demonstrated by those statements, expr can range from simple (a literal value) to more complex (the value returned by a scalar subquery).

The Performance Schema user\_variables\_by\_thread table contains information about userdefined variables. See Section 29.12.10, "Performance Schema User-Defined Variable Tables".

### <span id="page-88-1"></span>**Parameter and Local Variable Assignment**

[SET](#page-87-0) applies to parameters and local variables in the context of the stored object within which they are defined. The following procedure uses the increment procedure parameter and counter local variable:

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

#### <span id="page-88-2"></span>**System Variable Assignment**

The MySQL server maintains system variables that configure its operation. A system variable can have a global value that affects server operation as a whole, a session value that affects the current session, or both. Many system variables are dynamic and can be changed at runtime using the [SET](#page-87-0) statement to affect operation of the current server instance. [SET](#page-87-0) can also be used to persist certain system variables to the mysqld-auto.cnf file in the data directory, to affect server operation for subsequent startups.

If a SET statement is issued for a sensitive system variable, the query is rewritten to replace the value with "<redacted>" before it is logged to the general log and audit log. This takes place even if secure storage through a keyring component is not available on the server instance.

If you change a session system variable, the value remains in effect within your session until you change the variable to a different value or the session ends. The change has no effect on other sessions.

If you change a global system variable, the value is remembered and used to initialize the session value for new sessions until you change the variable to a different value or the server exits. The change is visible to any client that accesses the global value. However, the change affects the corresponding session value only for clients that connect after the change. The global variable change does not affect the session value for any current client sessions (not even the session within which the global value change occurs).

To make a global system variable setting permanent so that it applies across server restarts, you can persist it to the mysqld-auto.cnf file in the data directory. It is also possible to make persistent configuration changes by manually modifying a my.cnf option file, but that is more cumbersome, and an error in a manually entered setting might not be discovered until much later. [SET](#page-87-0) statements that persist system variables are more convenient and avoid the possibility of malformed settings because settings with syntax errors do not succeed and do not change server configuration. For more information about persisting system variables and the mysqld-auto.cnf file, see Section 7.1.9.3, "Persisted System Variables".

![](_page_89_Picture_5.jpeg)

#### **Note**

Setting or persisting a global system variable value always requires special privileges. Setting a session system variable value normally requires no special privileges and can be done by any user, although there are exceptions. For more information, see Section 7.1.9.1, "System Variable Privileges".

The following discussion describes the syntax options for setting and persisting system variables:

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

• To persist a global system variable to the mysqld-auto.cnf option file in the data directory, precede the variable name by the PERSIST keyword or the @@PERSIST. qualifier:

```
SET PERSIST max_connections = 1000;
SET @@PERSIST.max_connections = 1000;
```

This [SET](#page-87-0) syntax enables you to make configuration changes at runtime that also persist across server restarts. Like [SET GLOBAL](#page-87-0), [SET PERSIST](#page-87-0) sets the global variable runtime value, but also writes the variable setting to the mysqld-auto.cnf file (replacing any existing variable setting if there is one).

• To persist a global system variable to the mysqld-auto.cnf file without setting the global variable runtime value, precede the variable name by the PERSIST\_ONLY keyword or the @@PERSIST\_ONLY. qualifier:

```
SET PERSIST_ONLY back_log = 100;
SET @@PERSIST_ONLY.back_log = 100;
```

Like PERSIST, PERSIST\_ONLY writes the variable setting to mysqld-auto.cnf. However, unlike PERSIST, PERSIST\_ONLY does not modify the global variable runtime value. This makes PERSIST\_ONLY suitable for configuring read-only system variables that can be set only at server startup.

To set a global system variable value to the compiled-in MySQL default value or a session system variable to the current corresponding global value, set the variable to the value DEFAULT. For example, the following two statements are identical in setting the session value of max\_join\_size to the current global value:

```
SET @@SESSION.max_join_size = DEFAULT;
SET @@SESSION.max_join_size = @@GLOBAL.max_join_size;
```

Using [SET](#page-87-0) to persist a global system variable to a value of DEFAULT or to its literal default value assigns the variable its default value and adds a setting for the variable to mysqld-auto.cnf. To remove the variable from the file, use [RESET PERSIST](#page-158-0).

Some system variables cannot be persisted or are persist-restricted. See Section 7.1.9.4, "Nonpersistible and Persist-Restricted System Variables".

A system variable implemented by a plugin can be persisted if the plugin is installed when the [SET](#page-87-0) statement is executed. Assignment of the persisted plugin variable takes effect for subsequent server restarts if the plugin is still installed. If the plugin is no longer installed, the plugin variable no longer exists when the server reads the mysqld-auto.cnf file. In this case, the server writes a warning to the error log and continues:

```
currently unknown variable 'var_name'
was read from the persisted config file
```

To display system variable names and values:

- Use the [SHOW VARIABLES](#page-143-0) statement; see [Section 15.7.7.41, "SHOW VARIABLES Statement"](#page-143-0).
- Several Performance Schema tables provide system variable information. See Section 29.12.14, "Performance Schema System Variable Tables".
- The Performance Schema variables\_info table contains information showing when and by which user each system variable was most recently set. See Section 29.12.14.2, "Performance Schema variables\_info Table".
- The Performance Schema persisted\_variables table provides an SQL interface to the mysqld-auto.cnf file, enabling its contents to be inspected at runtime using SELECT statements. See Section 29.12.14.1, "Performance Schema persisted\_variables Table".

### <span id="page-90-0"></span>**SET Error Handling**

If any variable assignment in a [SET](#page-87-0) statement fails, the entire statement fails and no variables are changed, nor is the mysqld-auto.cnf file changed.

[SET](#page-87-0) produces an error under the circumstances described here. Most of the examples show [SET](#page-87-0) statements that use keyword syntax (for example, GLOBAL or SESSION), but the principles are also true for statements that use the corresponding modifiers (for example, @@GLOBAL. or @@SESSION.).

• Use of [SET](#page-87-0) (any variant) to set a read-only variable:

```
mysql> SET GLOBAL version = 'abc';
```

```
ERROR 1238 (HY000): Variable 'version' is a read only variable
```

• Use of GLOBAL, PERSIST, or PERSIST\_ONLY to set a variable that has only a session value:

```
mysql> SET GLOBAL sql_log_bin = ON;
ERROR 1228 (HY000): Variable 'sql_log_bin' is a SESSION
variable and can't be used with SET GLOBAL
```

• Use of SESSION to set a variable that has only a global value:

```
mysql> SET SESSION max_connections = 1000;
ERROR 1229 (HY000): Variable 'max_connections' is a
GLOBAL variable and should be set with SET GLOBAL
```

• Omission of GLOBAL, PERSIST, or PERSIST\_ONLY to set a variable that has only a global value:

```
mysql> SET max_connections = 1000;
ERROR 1229 (HY000): Variable 'max_connections' is a
GLOBAL variable and should be set with SET GLOBAL
```

• Use of PERSIST or PERSIST\_ONLY to set a variable that cannot be persisted:

```
mysql> SET PERSIST port = 3307;
ERROR 1238 (HY000): Variable 'port' is a read only variable
mysql> SET PERSIST_ONLY port = 3307;
ERROR 1238 (HY000): Variable 'port' is a non persistent read only variable
```

- The @@GLOBAL., @@PERSIST., @@PERSIST\_ONLY., @@SESSION., and @@ modifiers apply only to system variables. An error occurs for attempts to apply them to user-defined variables, stored procedure or function parameters, or stored program local variables.
- Not all system variables can be set to DEFAULT. In such cases, assigning DEFAULT results in an error.
- An error occurs for attempts to assign DEFAULT to user-defined variables, stored procedure or function parameters, or stored program local variables.

#### <span id="page-91-0"></span>**Multiple Variable Assignment**

A [SET](#page-87-0) statement can contain multiple variable assignments, separated by commas. This statement assigns values to a user-defined variable and a system variable:

```
SET @x = 1, SESSION sql_mode = '';
```

If you set multiple system variables in a single statement, the most recent GLOBAL, PERSIST, PERSIST\_ONLY, or SESSION keyword in the statement is used for following assignments that have no keyword specified.

Examples of multiple-variable assignment:

```
SET GLOBAL sort_buffer_size = 1000000, SESSION sort_buffer_size = 1000000;
SET @@GLOBAL.sort_buffer_size = 1000000, @@LOCAL.sort_buffer_size = 1000000;
SET GLOBAL max_connections = 1000, sort_buffer_size = 1000000;
```

The @@GLOBAL., @@PERSIST., @@PERSIST\_ONLY., @@SESSION., and @@ modifiers apply only to the immediately following system variable, not any remaining system variables. This statement sets the sort\_buffer\_size global value to 50000 and the session value to 1000000:

```
SET @@GLOBAL.sort_buffer_size = 50000, sort_buffer_size = 1000000;
```

#### <span id="page-91-1"></span>**System Variable References in Expressions**

To refer to the value of a system variable in expressions, use one of the @@-modifiers (except @@PERSIST. and @@PERSIST\_ONLY., which are not permitted in expressions). For example, you can retrieve system variable values in a SELECT statement like this:

SELECT @@GLOBAL.sql\_mode, @@SESSION.sql\_mode, @@sql\_mode;

![](_page_92_Picture_2.jpeg)

#### **Note**

A reference to a system variable in an expression as @@var\_name (with @@ rather than @@GLOBAL. or @@SESSION.) returns the session value if it exists and the global value otherwise. This differs from SET @@var\_name = expr, which always refers to the session value.

## <span id="page-92-0"></span>**15.7.6.2 SET CHARACTER SET Statement**

```
SET {CHARACTER SET | CHARSET}
 {'charset_name' | DEFAULT}
```

This statement maps all strings sent between the server and the current client with the given mapping. SET CHARACTER SET sets three session system variables: character\_set\_client and character\_set\_results are set to the given character set, and character\_set\_connection to the value of character\_set\_database. See Section 12.4, "Connection Character Sets and Collations".

charset\_name may be quoted or unquoted.

The default character set mapping can be restored by using the value DEFAULT. The default depends on the server configuration.

Some character sets cannot be used as the client character set. Attempting to use them with [SET](#page-92-0) [CHARACTER SET](#page-92-0) produces an error. See Impermissible Client Character Sets.

## <span id="page-92-1"></span>**15.7.6.3 SET NAMES Statement**

```
SET NAMES {'charset_name'
 [COLLATE 'collation_name'] | DEFAULT}
```

This statement sets the three session system variables character\_set\_client, character\_set\_connection, and character\_set\_results to the given character set. Setting character\_set\_connection to charset\_name also sets collation\_connection to the default collation for charset\_name. See Section 12.4, "Connection Character Sets and Collations".

The optional COLLATE clause may be used to specify a collation explicitly. If given, the collation must one of the permitted collations for charset\_name.

charset\_name and collation\_name may be quoted or unquoted.

The default mapping can be restored by using a value of DEFAULT. The default depends on the server configuration.

Some character sets cannot be used as the client character set. Attempting to use them with [SET](#page-92-1) [NAMES](#page-92-1) produces an error. See Impermissible Client Character Sets.

## <span id="page-92-2"></span>**15.7.7 SHOW Statements**

[SHOW](#page-92-2) has many forms that provide information about databases, tables, columns, or status information about the server. This section describes those following:

```
SHOW BINARY LOG STATUS
SHOW BINARY LOGS
SHOW BINLOG EVENTS [IN 'log_name'] [FROM pos] [LIMIT [offset,] row_count]
SHOW {CHARACTER SET | CHARSET} [like_or_where]
SHOW COLLATION [like_or_where]
SHOW [FULL] COLUMNS FROM tbl_name [FROM db_name] [like_or_where]
SHOW CREATE DATABASE db_name
SHOW CREATE EVENT event_name
```

```
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
SHOW OPEN TABLES [FROM db_name] [like_or_where]
SHOW PLUGINS
SHOW PROCEDURE CODE proc_name
SHOW PROCEDURE STATUS [like_or_where]
SHOW PRIVILEGES
SHOW [FULL] PROCESSLIST
SHOW PROFILE [types] [FOR QUERY n] [OFFSET n] [LIMIT n]
SHOW PROFILES
SHOW RELAYLOG EVENTS [IN 'log_name'] [FROM pos] [LIMIT [offset,] row_count]
SHOW REPLICA STATUS [FOR CHANNEL channel]
SHOW REPLICAS
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

If the syntax for a given [SHOW](#page-92-2) statement includes a LIKE 'pattern' part, 'pattern' is a string that can contain the SQL % and \_ wildcard characters. The pattern is useful for restricting statement output to matching values.

Several [SHOW](#page-92-2) statements also accept a WHERE clause that provides more flexibility in specifying which rows to display. See Section 28.8, "Extensions to SHOW Statements".

In [SHOW](#page-92-2) statement results, user names and host names are quoted using backticks (`).

Many MySQL APIs (such as PHP) enable you to treat the result returned from a [SHOW](#page-92-2) statement as you would a result set from a SELECT; see Chapter 31, Connectors and APIs, or your API documentation for more information. In addition, you can work in SQL with results from queries on tables in the INFORMATION\_SCHEMA database, which you cannot easily do with results from [SHOW](#page-92-2) statements. See Chapter 28, INFORMATION\_SCHEMA Tables.

## <span id="page-93-0"></span>**15.7.7.1 SHOW BINARY LOG STATUS Statement**

```
SHOW BINARY LOG STATUS
```

This statement provides status information about binary log files on the source server, and requires the REPLICATION CLIENT privilege (or the deprecated SUPER privilege).

#### Example:

```
mysql> SHOW BINARY LOG STATUS\G
*************************** 1. row ***************************
 File: source-bin.000002
 Position: 1307
 Binlog_Do_DB: test
 Binlog_Ignore_DB: manual, mysql
Executed_Gtid_Set: 3E11FA47-71CA-11E1-9E33-C80AA9429562:1-5
```

```
1 row in set (0.00 sec)
```

When global transaction IDs are in use, Executed\_Gtid\_Set shows the set of GTIDs for transactions that have been executed on the source. This is the same as the value for the gtid\_executed system variable on this server, as well as the value for Executed\_Gtid\_Set in the output of [SHOW REPLICA](#page-128-0) [STATUS](#page-128-0) on this server.

## <span id="page-94-0"></span>**15.7.7.2 SHOW BINARY LOGS Statement**

```
SHOW BINARY LOGS
```

Lists the binary log files on the server. This statement is used as part of the procedure described in Section 15.4.1.1, "PURGE BINARY LOGS Statement", that shows how to determine which logs can be purged. [SHOW BINARY LOGS](#page-94-0) requires the REPLICATION CLIENT privilege (or the deprecated SUPER privilege).

Encrypted binary log files have a 512-byte file header that stores information required for encryption and decryption of the file. This is included in the file size displayed by [SHOW BINARY LOGS](#page-94-0). The Encrypted column shows whether or not the binary log file is encrypted. Binary log encryption is active if binlog\_encryption=ON is set for the server. Existing binary log files are not encrypted or decrypted if binary log encryption is activated or deactivated while the server is running.

```
mysql> SHOW BINARY LOGS;
+---------------+-----------+-----------+
| Log_name | File_size | Encrypted |
+---------------+-----------+-----------+
| binlog.000015 | 724935 | Yes |
| binlog.000016 | 733481 | Yes |
+---------------+-----------+-----------+
```

## <span id="page-94-1"></span>**15.7.7.3 SHOW BINLOG EVENTS Statement**

```
SHOW BINLOG EVENTS
 [IN 'log_name']
 [FROM pos]
 [LIMIT [offset,] row_count]
```

Shows the events in the binary log. If you do not specify 'log\_name', the first binary log is displayed. SHOW BINLOG EVENTS requires the REPLICATION SLAVE privilege.

The LIMIT clause has the same syntax as for the SELECT statement. See Section 15.2.13, "SELECT Statement".

![](_page_94_Picture_12.jpeg)

#### **Note**

Issuing a [SHOW BINLOG EVENTS](#page-94-1) with no LIMIT clause could start a very timeand resource-consuming process because the server returns to the client the complete contents of the binary log (which includes all statements executed by the server that modify data). As an alternative to [SHOW BINLOG EVENTS](#page-94-1), use the mysqlbinlog utility to save the binary log to a text file for later examination and analysis. See Section 6.6.9, "mysqlbinlog — Utility for Processing Binary Log Files".

[SHOW BINLOG EVENTS](#page-94-1) displays the following fields for each event in the binary log:

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

For compressed transaction payloads, the Transaction\_payload\_event is first printed as a single unit, then it is unpacked and each event inside it is printed.

Some events relating to the setting of user and system variables are not included in the output from [SHOW BINLOG EVENTS](#page-94-1). To get complete coverage of events within a binary log, use mysqlbinlog.

[SHOW BINLOG EVENTS](#page-94-1) does not work with relay log files. You can use [SHOW RELAYLOG EVENTS](#page-127-0) for this purpose.

## <span id="page-95-0"></span>**15.7.7.4 SHOW CHARACTER SET Statement**

```
SHOW {CHARACTER SET | CHARSET}
 [LIKE 'pattern' | WHERE expr]
```

The [SHOW CHARACTER SET](#page-95-0) statement shows all available character sets. The LIKE clause, if present, indicates which character set names to match. The WHERE clause can be given to select rows using more general conditions, as discussed in Section 28.8, "Extensions to SHOW Statements". For example:

```
mysql> SHOW CHARACTER SET LIKE 'latin%';
+---------+-----------------------------+-------------------+--------+
| Charset | Description | Default collation | Maxlen |
+---------+-----------------------------+-------------------+--------+
| latin1 | cp1252 West European | latin1_swedish_ci | 1 |
| latin2 | ISO 8859-2 Central European | latin2_general_ci | 1 |
| latin5 | ISO 8859-9 Turkish | latin5_turkish_ci | 1 |
| latin7 | ISO 8859-13 Baltic | latin7_general_ci | 1 |
+---------+-----------------------------+-------------------+--------+
```

[SHOW CHARACTER SET](#page-95-0) output has these columns:

• Charset

The character set name.

• Description

A description of the character set.

• Default collation

The default collation for the character set.

• Maxlen

The maximum number of bytes required to store one character.

The filename character set is for internal use only; consequently, [SHOW CHARACTER SET](#page-95-0) does not display it.

Character set information is also available from the INFORMATION\_SCHEMA CHARACTER\_SETS table.

## <span id="page-96-0"></span>**15.7.7.5 SHOW COLLATION Statement**

```
SHOW COLLATION
 [LIKE 'pattern' | WHERE expr]
```

This statement lists collations supported by the server. By default, the output from [SHOW COLLATION](#page-96-0) includes all available collations. The LIKE clause, if present, indicates which collation names to match. The WHERE clause can be given to select rows using more general conditions, as discussed in Section 28.8, "Extensions to SHOW Statements". For example:

|                                      | mysql> SHOW COLLATION WHERE Charset = 'latin1';<br>+++++++ |  |  |                                             |       |
|--------------------------------------|------------------------------------------------------------|--|--|---------------------------------------------|-------|
| Collation<br>+++++++                 |                                                            |  |  | Charset   Id   Default   Compiled   Sortlen |       |
| latin1_german1_ci   latin1   5       |                                                            |  |  | Yes                                         | <br>1 |
| latin1_swedish_ci   latin1   8   Yes |                                                            |  |  | Yes                                         | <br>1 |
| latin1_danish_ci   latin1   15       |                                                            |  |  | Yes                                         | <br>1 |
| latin1_german2_ci   latin1   31      |                                                            |  |  | Yes                                         | <br>2 |
| latin1_bin                           | latin1   47                                                |  |  | Yes                                         | <br>1 |
| latin1_general_ci   latin1   48      |                                                            |  |  | Yes                                         | <br>1 |
| latin1_general_cs   latin1   49      |                                                            |  |  | Yes                                         | <br>1 |
| latin1_spanish_ci   latin1   94      |                                                            |  |  | Yes                                         | <br>1 |
| +++++++                              |                                                            |  |  |                                             |       |

[SHOW COLLATION](#page-96-0) output has these columns:

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

• Pad\_attribute

The collation pad attribute, one of NO PAD or PAD SPACE. This attribute affects whether trailing spaces are significant in string comparisons; for more information, see Trailing Space Handling in Comparisons.

To see the default collation for each character set, use the following statement. Default is a reserved word, so to use it as an identifier, it must be quoted as such:

```
mysql> SHOW COLLATION WHERE `Default` = 'Yes';
+---------------------+----------+----+---------+----------+---------+
| Collation | Charset | Id | Default | Compiled | Sortlen |
+---------------------+----------+----+---------+----------+---------+
| big5_chinese_ci | big5 | 1 | Yes | Yes | 1 |
```

```
| dec8_swedish_ci | dec8 | 3 | Yes | Yes | 1 |
| cp850_general_ci | cp850 | 4 | Yes | Yes | 1 |
| hp8_english_ci | hp8 | 6 | Yes | Yes | 1 |
| koi8r_general_ci | koi8r | 7 | Yes | Yes | 1 |
| latin1_swedish_ci | latin1 | 8 | Yes | Yes | 1 |
...
```

Collation information is also available from the INFORMATION\_SCHEMA COLLATIONS table. See Section 28.3.6, "The INFORMATION\_SCHEMA COLLATIONS Table".

## <span id="page-97-0"></span>**15.7.7.6 SHOW COLUMNS Statement**

```
SHOW [EXTENDED] [FULL] {COLUMNS | FIELDS}
 {FROM | IN} tbl_name
 [{FROM | IN} db_name]
 [LIKE 'pattern' | WHERE expr]
```

[SHOW COLUMNS](#page-97-0) displays information about the columns in a given table. It also works for views. [SHOW](#page-97-0) [COLUMNS](#page-97-0) displays information only for those columns for which you have some privilege.

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

The optional EXTENDED keyword causes the output to include information about hidden columns that MySQL uses internally and are not accessible by users.

The optional FULL keyword causes the output to include the column collation and comments, as well as the privileges you have for each column.

The LIKE clause, if present, indicates which column names to match. The WHERE clause can be given to select rows using more general conditions, as discussed in Section 28.8, "Extensions to SHOW Statements".

The data types may differ from what you expect them to be based on a CREATE TABLE statement because MySQL sometimes changes data types when you create or alter a table. The conditions under which this occurs are described in Section 15.1.20.7, "Silent Column Specification Changes".

[SHOW COLUMNS](#page-97-0) displays the following values for each table column:

• Field

The name of the column.

• Type

The column data type.

• Collation

The collation for nonbinary string columns, or NULL for other columns. This value is displayed only if you use the FULL keyword.

### • Null

The column nullability. The value is YES if NULL values can be stored in the column, NO if not.

#### • Key

Whether the column is indexed:

- If Key is empty, the column either is not indexed or is indexed only as a secondary column in a multiple-column, nonunique index.
- If Key is PRI, the column is a PRIMARY KEY or is one of the columns in a multiple-column PRIMARY KEY.
- If Key is UNI, the column is the first column of a UNIQUE index. (A UNIQUE index permits multiple NULL values, but you can tell whether the column permits NULL by checking the Null field.)
- If Key is MUL, the column is the first column of a nonunique index in which multiple occurrences of a given value are permitted within the column.

If more than one of the Key values applies to a given column of a table, Key displays the one with the highest priority, in the order PRI, UNI, MUL.

A UNIQUE index may be displayed as PRI if it cannot contain NULL values and there is no PRIMARY KEY in the table. A UNIQUE index may display as MUL if several columns form a composite UNIQUE index; although the combination of the columns is unique, each column can still hold multiple occurrences of a given value.

#### • Default

The default value for the column. This is NULL if the column has an explicit default of NULL, or if the column definition includes no DEFAULT clause.

## • Extra

Any additional information that is available about a given column. The value is nonempty in these cases:

- auto\_increment for columns that have the AUTO\_INCREMENT attribute.
- on update CURRENT\_TIMESTAMP for TIMESTAMP or DATETIME columns that have the ON UPDATE CURRENT\_TIMESTAMP attribute.
- VIRTUAL GENERATED or STORED GENERATED for generated columns.
- DEFAULT\_GENERATED for columns that have an expression default value.
- Privileges

The privileges you have for the column. This value is displayed only if you use the FULL keyword.

### • Comment

Any comment included in the column definition. This value is displayed only if you use the FULL keyword.

Table column information is also available from the INFORMATION\_SCHEMA COLUMNS table. See Section 28.3.8, "The INFORMATION\_SCHEMA COLUMNS Table". The extended information about hidden columns is available only using SHOW EXTENDED COLUMNS; it cannot be obtained from the COLUMNS table.

You can list a table's columns with the mysqlshow db\_name tbl\_name command.

The DESCRIBE statement provides information similar to SHOW COLUMNS. See Section 15.8.1, "DESCRIBE Statement".

The SHOW CREATE TABLE, SHOW TABLE STATUS, and SHOW INDEX statements also provide information about tables. See Section 15.7.7, "SHOW Statements".

SHOW COLUMNS includes the table's generated invisible primary key, if it has one, by default. You can cause this information to be suppressed in the statement's output by setting show\_gipk\_in\_create\_table\_and\_information\_schema = OFF. For more information, see Section 15.1.20.11. "Generated Invisible Primary Keys".

#### <span id="page-99-0"></span>15.7.7.7 SHOW CREATE DATABASE Statement

```
SHOW CREATE {DATABASE | SCHEMA} [IF NOT EXISTS] db name
```

Shows the CREATE DATABASE statement that creates the named database. If the SHOW statement includes an IF NOT EXISTS clause, the output too includes such a clause. SHOW CREATE SCHEMA is a synonym for SHOW CREATE DATABASE.

```
mysql> SHOW CREATE DATABASE test\G

***********************************
```

SHOW CREATE DATABASE quotes table and column names according to the value of the sql\_quote\_show\_create option. See Section 7.1.8, "Server System Variables".

#### <span id="page-99-1"></span>15.7.7.8 SHOW CREATE EVENT Statement

```
SHOW CREATE EVENT event name
```

This statement displays the CREATE EVENT statement needed to re-create a given event. It requires the EVENT privilege for the database from which the event is to be shown. For example (using the same event e daily defined and then altered in Section 15.7.7.19, "SHOW EVENTS Statement"):

```
mysql> SHOW CREATE EVENT myschema.e daily\G
                         ** 1. row ***
              Event: e daily
           sql mode: ONLY FULL GROUP BY, STRICT TRANS TABLES,
                     NO ZERO IN DATE, NO ZERO DATE,
                      ERROR FOR DIVISION BY ZERO,
                      NO ENGINE SUBSTITUTION
          time zone: SYSTEM
       Create Event: CREATE DEFINER=`jon`@`ghidora` EVENT `e daily`
                       ON SCHEDULE EVERY 1 DAY
                       STARTS CURRENT TIMESTAMP + INTERVAL 6 HOUR
                       ON COMPLETION NOT PRESERVE
                       ENABLE
                        COMMENT 'Saves total number of sessions then
                             clears the table each day'
                        DO BEGIN
                         INSERT INTO site activity.totals (time, total)
                           SELECT CURRENT TIMESTAMP, COUNT(*)
                             FROM site activity.sessions;
                         DELETE FROM site_activity.sessions;
character set client: utf8mb4
collation connection: utf8mb4 0900 ai ci
Database Collation: utf8mb4 0900 ai ci
```

character\_set\_client is the session value of the character\_set\_client system variable when the event was created. collation\_connection is the session value of the collation\_connection system variable when the event was created. Database Collation is the collation of the database with which the event is associated.

The output reflects the current status of the event (ENABLE) rather than the status with which it was created.

## <span id="page-100-1"></span>**15.7.7.9 SHOW CREATE FUNCTION Statement**

```
SHOW CREATE FUNCTION func_name
```

This statement is similar to [SHOW CREATE PROCEDURE](#page-100-0) but for stored functions. See [Section 15.7.7.10, "SHOW CREATE PROCEDURE Statement".](#page-100-0)

## <span id="page-100-0"></span>**15.7.7.10 SHOW CREATE PROCEDURE Statement**

```
SHOW CREATE PROCEDURE proc_name
```

This statement is a MySQL extension. It returns the exact string that can be used to re-create the named stored procedure. A similar statement, [SHOW CREATE FUNCTION](#page-100-1), displays information about stored functions (see [Section 15.7.7.9, "SHOW CREATE FUNCTION Statement"](#page-100-1)).

To use either statement, you must be the user named as the routine DEFINER, have the SHOW\_ROUTINE privilege, have the SELECT privilege at the global level, or have the CREATE ROUTINE, ALTER ROUTINE, or EXECUTE privilege granted at a scope that includes the routine. The value displayed for the Create Procedure or Create Function field is NULL if you have only CREATE ROUTINE, ALTER ROUTINE, or EXECUTE.

```
mysql> SHOW CREATE PROCEDURE test.citycount\G
*************************** 1. row ***************************
 Procedure: citycount
 sql_mode: ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,
 NO_ZERO_IN_DATE,NO_ZERO_DATE,
 ERROR_FOR_DIVISION_BY_ZERO,
 NO_ENGINE_SUBSTITUTION
 Create Procedure: CREATE DEFINER=`me`@`localhost`
 PROCEDURE `citycount`(IN country CHAR(3), OUT cities INT)
 BEGIN
 SELECT COUNT(*) INTO cities FROM world.city
 WHERE CountryCode = country;
 END
character_set_client: utf8mb4
collation_connection: utf8mb4_0900_ai_ci
 Database Collation: utf8mb4_0900_ai_ci
mysql> SHOW CREATE FUNCTION test.hello\G
*************************** 1. row ***************************
 Function: hello
 sql_mode: ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,
 NO_ZERO_IN_DATE,NO_ZERO_DATE,
 ERROR_FOR_DIVISION_BY_ZERO,
 NO_ENGINE_SUBSTITUTION
 Create Function: CREATE DEFINER=`me`@`localhost`
 FUNCTION `hello`(s CHAR(20))
 RETURNS char(50) CHARSET utf8mb4
 DETERMINISTIC
 RETURN CONCAT('Hello, ',s,'!')
character_set_client: utf8mb4
collation_connection: utf8mb4_0900_ai_ci
 Database Collation: utf8mb4_0900_ai_ci
```

character\_set\_client is the session value of the character\_set\_client system variable when the routine was created. collation\_connection is the session value of the collation\_connection system variable when the routine was created. Database Collation is the collation of the database with which the routine is associated.

#### <span id="page-101-0"></span>15.7.7.11 SHOW CREATE TABLE Statement

```
SHOW CREATE TABLE tbl name
```

Shows the CREATE TABLE statement that creates the named table. To use this statement, you must have some privilege for the table. This statement also works with views.

```
mysql> SHOW CREATE TABLE t\G

***********************************
```

SHOW CREATE TABLE displays all CHECK constraints as table constraints. That is, a CHECK constraint originally specified as part of a column definition displays as a separate clause not part of the column definition. Example:

```
mysql> CREATE TABLE t1 (
```

SHOW CREATE TABLE quotes table and column names according to the value of the sql quote show create option. See Section 7.1.8, "Server System Variables".

When altering the storage engine of a table, table options that are not applicable to the new storage engine are retained in the table definition to enable reverting the table with its previously defined options to the original storage engine, if necessary. For example, when changing the storage engine from Innobs to MyISAM, options specific to Innobs, such as ROW\_FORMAT=COMPACT, are retained, as shown here:

```
mysql> CREATE TABLE t1 (c1 INT PRIMARY KEY) ROW_FORMAT=COMPACT ENGINE=InnoDB;
mysql> ALTER TABLE t1 ENGINE=MyISAM;
mysql> SHOW CREATE TABLE t1\G
*********************************
    Table: t1
Create Table: CREATE TABLE `t1` (
    `c1` int NOT NULL,
    PRIMARY KEY (`c1`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4 0900 ai ci ROW FORMAT=COMPACT
```

When creating a table with strict mode disabled, the storage engine's default row format is used if the specified row format is not supported. The actual row format of the table is reported in the Row\_format column in response to SHOW TABLE STATUS. SHOW CREATE TABLE shows the row format that was specified in the CREATE TABLE statement.

SHOW CREATE TABLE also includes the definition of the table's generated invisible primary key, if it has such a key, by default. You can cause this information to be suppressed in the statement's output by setting show\_gipk\_in\_create\_table\_and\_information\_schema = OFF. For more information, see Section 15.1.20.11. "Generated Invisible Primary Keys".

## <span id="page-102-1"></span>**15.7.7.12 SHOW CREATE TRIGGER Statement**

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
 NO_ENGINE_SUBSTITUTION
SQL Original Statement: CREATE DEFINER=`me`@`localhost` TRIGGER `ins_sum`
 BEFORE INSERT ON `account`
 FOR EACH ROW SET @sum = @sum + NEW.amount
 character_set_client: utf8mb4
 collation_connection: utf8mb4_0900_ai_ci
 Database Collation: utf8mb4_0900_ai_ci
 Created: 2018-08-08 10:10:12.61
```

[SHOW CREATE TRIGGER](#page-102-1) output has these columns:

- Trigger: The trigger name.
- sql\_mode: The SQL mode in effect when the trigger executes.
- SQL Original Statement: The CREATE TRIGGER statement that defines the trigger.
- character\_set\_client: The session value of the character\_set\_client system variable when the trigger was created.
- collation\_connection: The session value of the collation\_connection system variable when the trigger was created.
- Database Collation: The collation of the database with which the trigger is associated.
- Created: The date and time when the trigger was created. This is a TIMESTAMP(2) value (with a fractional part in hundredths of seconds) for triggers.

Trigger information is also available from the INFORMATION\_SCHEMA TRIGGERS table. See Section 28.3.44, "The INFORMATION\_SCHEMA TRIGGERS Table".

## <span id="page-102-0"></span>**15.7.7.13 SHOW CREATE USER Statement**

```
SHOW CREATE USER user
```

This statement shows the [CREATE USER](#page-28-0) statement that creates the named user. An error occurs if the user does not exist. The statement requires the SELECT privilege for the mysql system schema, except to see information for the current user. For the current user, the SELECT privilege for the mysql.user system table is required for display of the password hash in the IDENTIFIED AS clause; otherwise, the hash displays as <secret>.

To name the account, use the format described in Section 8.2.4, "Specifying Account Names". The host name part of the account name, if omitted, defaults to '%'. It is also possible to specify CURRENT\_USER or CURRENT\_USER() to refer to the account associated with the current session.

Password hash values displayed in the IDENTIFIED WITH clause of output from [SHOW CREATE](#page-102-0) [USER](#page-102-0) may contain unprintable characters that have adverse effects on terminal displays and in other environments. Enabling the print\_identified\_with\_as\_hex system variable causes [SHOW](#page-102-0) [CREATE USER](#page-102-0) to display such hash values as hexadecimal strings rather than as regular string literals. Hash values that do not contain unprintable characters still display as regular string literals, even with this variable enabled.

```
mysql> CREATE USER 'u1'@'localhost' IDENTIFIED BY 'secret';
```

```
mysql> SET print_identified_with_as_hex = ON;
mysql> SHOW CREATE USER 'u1'@'localhost'\G
*************************** 1. row ***************************
CREATE USER for u1@localhost: CREATE USER `u1`@`localhost`
IDENTIFIED WITH 'caching_sha2_password'
AS 0x244124303035240C7745603626313D613C4C10633E0A104B1E14135A544A7871567245614F4872344643546336546F624F6C7861326932752F45622F4F473273597557627139
REQUIRE NONE PASSWORD EXPIRE DEFAULT ACCOUNT UNLOCK
PASSWORD HISTORY DEFAULT PASSWORD REUSE INTERVAL DEFAULT
PASSWORD REQUIRE CURRENT DEFAULT
```

To display the privileges granted to an account, use the [SHOW GRANTS](#page-112-0) statement. See [Section 15.7.7.22, "SHOW GRANTS Statement".](#page-112-0)

## <span id="page-103-1"></span>**15.7.7.14 SHOW CREATE VIEW Statement**

```
SHOW CREATE VIEW view_name
```

This statement shows the CREATE VIEW statement that creates the named view.

```
mysql> SHOW CREATE VIEW v\G
*************************** 1. row ***************************
 View: v
 Create View: CREATE ALGORITHM=UNDEFINED
 DEFINER=`bob`@`localhost`
 SQL SECURITY DEFINER VIEW
 `v` AS select 1 AS `a`,2 AS `b`
character_set_client: utf8mb4
collation_connection: utf8mb4_0900_ai_ci
```

character\_set\_client is the session value of the character\_set\_client system variable when the view was created. collation\_connection is the session value of the collation\_connection system variable when the view was created.

Use of [SHOW CREATE VIEW](#page-103-1) requires the SHOW VIEW privilege, and the SELECT privilege for the view in question.

View information is also available from the INFORMATION\_SCHEMA VIEWS table. See Section 28.3.47, "The INFORMATION\_SCHEMA VIEWS Table".

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

The advantage of storing a view definition in canonical form is that changes made later to the value of sql\_mode do not affect the results from the view. However an additional consequence is that comments prior to SELECT are stripped from the definition by the server.

## <span id="page-103-0"></span>**15.7.7.15 SHOW DATABASES Statement**

```
SHOW {DATABASES | SCHEMAS}
```

```
 [LIKE 'pattern' | WHERE expr]
```

[SHOW DATABASES](#page-103-0) lists the databases on the MySQL server host. [SHOW SCHEMAS](#page-103-0) is a synonym for [SHOW DATABASES](#page-103-0). The LIKE clause, if present, indicates which database names to match. The WHERE clause can be given to select rows using more general conditions, as discussed in Section 28.8, "Extensions to SHOW Statements".

You see only those databases for which you have some kind of privilege, unless you have the global [SHOW DATABASES](#page-103-0) privilege. You can also get this list using the mysqlshow command.

If the server was started with the --skip-show-database option, you cannot use this statement at all unless you have the SHOW DATABASES privilege.

MySQL implements databases as directories in the data directory, so this statement simply lists directories in that location. However, the output may include names of directories that do not correspond to actual databases.

Database information is also available from the INFORMATION\_SCHEMA SCHEMATA table. See Section 28.3.31, "The INFORMATION\_SCHEMA SCHEMATA Table".

![](_page_104_Picture_7.jpeg)

#### **Caution**

Because any static global privilege is considered a privilege for all databases, any static global privilege enables a user to see all database names with [SHOW](#page-103-0) [DATABASES](#page-103-0) or by examining the SCHEMATA table of INFORMATION\_SCHEMA, except databases that have been restricted at the database level by partial revokes.

## <span id="page-104-0"></span>**15.7.7.16 SHOW ENGINE Statement**

```
SHOW ENGINE engine_name {STATUS | MUTEX}
```

[SHOW ENGINE](#page-104-0) displays operational information about a storage engine. It requires the PROCESS privilege. The statement has these variants:

```
SHOW ENGINE INNODB STATUS
SHOW ENGINE INNODB MUTEX
SHOW ENGINE PERFORMANCE_SCHEMA STATUS
```

SHOW ENGINE INNODB STATUS displays extensive information from the standard InnoDB Monitor about the state of the InnoDB storage engine. For information about the standard monitor and other InnoDB Monitors that provide information about InnoDB processing, see Section 17.17, "InnoDB Monitors".

SHOW ENGINE INNODB MUTEX displays InnoDB mutex and rw-lock statistics.

![](_page_104_Picture_16.jpeg)

#### **Note**

InnoDB mutexes and rwlocks can also be monitored using Performance Schema tables. See Section 17.16.2, "Monitoring InnoDB Mutex Waits Using Performance Schema".

Mutex statistics collection is configured dynamically using the following options:

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

Collection of mutex statistics for SHOW ENGINE INNODB MUTEX can also be enabled by setting innodb\_monitor\_enable='all', or disabled by setting innodb\_monitor\_disable='all'.

SHOW ENGINE INNODB MUTEX output has these columns:

• Type

Always InnoDB.

• Name

For mutexes, the Name field reports only the mutex name. For rwlocks, the Name field reports the source file where the rwlock is implemented, and the line number in the file where the rwlock is created. The line number is specific to your version of MySQL.

• Status

The mutex status. This field reports the number of spins, waits, and calls. Statistics for low-level operating system mutexes, which are implemented outside of InnoDB, are not reported.

- spins indicates the number of spins.
- waits indicates the number of mutex waits.
- calls indicates how many times the mutex was requested.

SHOW ENGINE INNODB MUTEX does not list mutexes and rw-locks for each buffer pool block, as the amount of output would be overwhelming on systems with a large buffer pool. SHOW ENGINE INNODB MUTEX does, however, print aggregate BUF\_BLOCK\_MUTEX spin, wait, and call values for buffer pool block mutexes and rw-locks. SHOW ENGINE INNODB MUTEX also does not list any mutexes or rwlocks that have never been waited on (os\_waits=0). Thus, SHOW ENGINE INNODB MUTEX only displays information about mutexes and rw-locks outside of the buffer pool that have caused at least one OS-level wait.

Use SHOW ENGINE PERFORMANCE\_SCHEMA STATUS to inspect the internal operation of the Performance Schema code:

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
 Type: performance_schema
 Name: performance_schema.memory
Status: 26459600
...
```

This statement is intended to help the DBA understand the effects that different Performance Schema options have on memory requirements.

Name values consist of two parts, which name an internal buffer and a buffer attribute, respectively. Interpret buffer names as follows:

• An internal buffer that is not exposed as a table is named within parentheses. Examples: (pfs\_cond\_class).size, (pfs\_mutex\_class).memory.

- An internal buffer that is exposed as a table in the performance\_schema database is named after the table, without parentheses. Examples: events\_waits\_history.size, mutex\_instances.count.
- A value that applies to the Performance Schema as a whole begins with performance\_schema. Example: performance\_schema.memory.

Buffer attributes have these meanings:

- size is the size of the internal record used by the implementation, such as the size of a row in a table. size values cannot be changed.
- count is the number of internal records, such as the number of rows in a table. count values can be changed using Performance Schema configuration options.
- For a table, tbl\_name.memory is the product of size and count. For the Performance Schema as a whole, performance\_schema.memory is the sum of all the memory used (the sum of all other memory values).

In some cases, there is a direct relationship between a Performance Schema configuration parameter and a SHOW ENGINE value. For example, events\_waits\_history\_long.count corresponds to performance\_schema\_events\_waits\_history\_long\_size. In other cases, the relationship is more complex. For example, events\_waits\_history.count corresponds to performance\_schema\_events\_waits\_history\_size (the number of rows per thread) multiplied by performance\_schema\_max\_thread\_instances (the number of threads).

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
| ndbcluster | binlog | latest_epoch=155467, latest_trans_epoch=148126,
 latest_received_binlog_epoch=0, latest_handled_binlog_epoch=0,
 latest_applied_binlog_epoch=0 |
+------------+-----------------------+--------------------------------------------------+
```

The Status column in each of these rows provides information about the MySQL server's connection to the cluster and about the cluster binary log's status, respectively. The Status information is in the form of comma-delimited set of name-value pairs.

The connection row's Status column contains the name-value pairs described in the following table.

| Name            | Value                                          |
|-----------------|------------------------------------------------|
| cluster_node_id | The node ID of the MySQL server in the cluster |

| Name                       | Value                                                                                                                             |
|----------------------------|-----------------------------------------------------------------------------------------------------------------------------------|
| connected_host             | The host name or IP address of the cluster<br>management server to which the MySQL server is<br>connected                         |
| connected_port             | The port used by the MySQL server to connect to<br>the management server (connected_host)                                         |
| number_of_data_nodes       | The number of data nodes configured for the<br>cluster (that is, the number of [ndbd] sections in<br>the cluster config.ini file) |
| number_of_ready_data_nodes | The number of data nodes in the cluster that are<br>actually running                                                              |
| connect_count              | The number of times this mysqld has connected<br>or reconnected to cluster data nodes                                             |

The binlog row's Status column contains information relating to NDB Cluster Replication. The name-value pairs it contains are described in the following table.

| Name                         | Value                                                                                                                                              |
|------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------|
| latest_epoch                 | The most recent epoch most recently run on this<br>MySQL server (that is, the sequence number of<br>the most recent transaction run on the server) |
| latest_trans_epoch           | The most recent epoch processed by the cluster's<br>data nodes                                                                                     |
| latest_received_binlog_epoch | The most recent epoch received by the binary log<br>thread                                                                                         |
| latest_handled_binlog_epoch  | The most recent epoch processed by the binary<br>log thread (for writing to the binary log)                                                        |
| latest_applied_binlog_epoch  | The most recent epoch actually written to the<br>binary log                                                                                        |

See Section 25.7, "NDB Cluster Replication", for more information.

The remaining rows from the output of SHOW ENGINE NDB STATUS which are most likely to prove useful in monitoring the cluster are listed here by Name:

- NdbTransaction: The number and size of NdbTransaction objects that have been created. An NdbTransaction is created each time a table schema operation (such as CREATE TABLE or ALTER TABLE) is performed on an NDB table.
- NdbOperation: The number and size of NdbOperation objects that have been created.
- NdbIndexScanOperation: The number and size of NdbIndexScanOperation objects that have been created.
- NdbIndexOperation: The number and size of NdbIndexOperation objects that have been created.
- NdbRecAttr: The number and size of NdbRecAttr objects that have been created. In general, one of these is created each time a data manipulation statement is performed by an SQL node.
- NdbBlob: The number and size of NdbBlob objects that have been created. An NdbBlob is created for each new operation involving a BLOB column in an NDB table.
- NdbReceiver: The number and size of any NdbReceiver object that have been created. The number in the created column is the same as the number of data nodes in the cluster to which the MySQL server has connected.

![](_page_108_Picture_1.jpeg)

#### Note

SHOW ENGINE NDB STATUS returns an empty result if no operations involving NDB tables have been performed during the current session by the MySQL client accessing the SQL node on which this statement is run.

## <span id="page-108-0"></span>15.7.7.17 SHOW ENGINES Statement

```
SHOW [STORAGE] ENGINES
```

SHOW ENGINES displays status information about the server's storage engines. This is particularly useful for checking whether a storage engine is supported, or to see what the default engine is.

For information about MySQL storage engines, see Chapter 17, *The InnoDB Storage Engine*, and Chapter 18, *Alternative Storage Engines*.

```
mysql> SHOW ENGINES\G
                   ***** 1. row **************
     Engine: MEMORY
    Support: YES
    Comment: Hash based, stored in memory, useful for temporary tables
Transactions: NO
        XA: NO
 Savepoints: NO
                 ****** 2. row **************
    Engine: InnoDB
    Support: DEFAULT
    Comment: Supports transactions, row-level locking, and foreign keys
Transactions: YES
        XA: YES
 Savepoints: YES
             ******* 3. row ***************
    Engine: PERFORMANCE SCHEMA
    Support: YES
    Comment: Performance Schema
Transactions: NO
        XA: NO
 Savepoints: NO
              ******** 4. row **************
    Engine: MyISAM
    Support: YES
    Comment: MyISAM storage engine
Transactions: NO
        AX · MU
 Savepoints: NO
             ******** 5. row **************
    Engine: MRG MYISAM
    Support: YES
    Comment: Collection of identical MyISAM tables
Transactions: NO
        VA · NO
 Savepoints: NO
              ******* 6. row **************
    Engine: BLACKHOLE
    Support: YES
    Comment: /dev/null storage engine (anything you write to it disappears)
Transactions: NO
        XA: NO
 Savepoints: NO
             ******** 7. row ***************
    Engine: CSV
    Support: YES
    Comment: CSV storage engine
Transactions: NO
        XA: NO
 Savepoints: NO
      ***************** 8. row ***************
    Engine: ARCHIVE
    Support: YES
    Comment: Archive storage engine
```

```
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

A value of DISABLED occurs either because the server was started with an option that disables the engine, or because not all options required to enable it were given. In the latter case, the error log should contain a reason indicating why the option is disabled. See Section 7.4.2, "The Error Log".

You might also see DISABLED for a storage engine if the server was compiled to support it, but was started with a --skip-engine\_name option. For the NDB storage engine, DISABLED means the server was compiled with support for NDB Cluster, but was not started with the --ndbcluster option.

All MySQL servers support MyISAM tables. It is not possible to disable MyISAM.

• Comment

A brief description of the storage engine.

• Transactions

Whether the storage engine supports transactions.

• XA

Whether the storage engine supports XA transactions.

• Savepoints

Whether the storage engine supports savepoints.

Storage engine information is also available from the INFORMATION\_SCHEMA ENGINES table. See Section 28.3.13, "The INFORMATION\_SCHEMA ENGINES Table".

## <span id="page-109-0"></span>**15.7.7.18 SHOW ERRORS Statement**

```
SHOW ERRORS [LIMIT [offset,] row_count]
SHOW COUNT(*) ERRORS
```

[SHOW ERRORS](#page-109-0) is a diagnostic statement that is similar to [SHOW WARNINGS](#page-145-0), except that it displays information only for errors, rather than for errors, warnings, and notes.

The LIMIT clause has the same syntax as for the SELECT statement. See Section 15.2.13, "SELECT Statement".

The [SHOW COUNT\(\\*\) ERRORS](#page-109-0) statement displays the number of errors. You can also retrieve this number from the error\_count variable:

```
SHOW COUNT(*) ERRORS;
SELECT @@error_count;
```

[SHOW ERRORS](#page-109-0) and error\_count apply only to errors, not warnings or notes. In other respects, they are similar to [SHOW WARNINGS](#page-145-0) and warning\_count. In particular, [SHOW ERRORS](#page-109-0) cannot display information for more than max\_error\_count messages, and error\_count can exceed the value of max\_error\_count if the number of errors exceeds max\_error\_count.

For more information, see [Section 15.7.7.42, "SHOW WARNINGS Statement".](#page-145-0)

## <span id="page-110-0"></span>**15.7.7.19 SHOW EVENTS Statement**

```
SHOW EVENTS
 [{FROM | IN} schema_name]
 [LIKE 'pattern' | WHERE expr]
```

This statement displays information about Event Manager events, which are discussed in Section 27.4, "Using the Event Scheduler". It requires the EVENT privilege for the database from which the events are to be shown.

In its simplest form, [SHOW EVENTS](#page-110-0) lists all of the events in the current schema:

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
 Interval value: 1
 Interval field: DAY
 Starts: 2018-08-08 11:06:34
 Ends: NULL
 Status: ENABLED
 Originator: 1
character_set_client: utf8mb4
collation_connection: utf8mb4_0900_ai_ci
 Database Collation: utf8mb4_0900_ai_ci
```

To see events for a specific schema, use the FROM clause. For example, to see events for the test schema, use the following statement:

```
SHOW EVENTS FROM test;
```

The LIKE clause, if present, indicates which event names to match. The WHERE clause can be given to select rows using more general conditions, as discussed in Section 28.8, "Extensions to SHOW Statements".

[SHOW EVENTS](#page-110-0) output has these columns:

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

• Ends

For a recurring event whose definition includes a ENDS clause, this column contains the corresponding DATETIME value. As with the Execute At column, this value resolves any expressions used. If there is no ENDS clause affecting the timing of the event, this column is NULL.

• Status

The event status. One of ENABLED, DISABLED, or REPLICA\_SIDE\_DISABLED. REPLICA\_SIDE\_DISABLED indicates that the creation of the event occurred on another MySQL server acting as a replication source and replicated to the current MySQL server which is acting as a replica, but the event is not presently being executed on the replica. For more information, see Section 19.5.1.16, "Replication of Invoked Features". information.

REPLICA\_SIDE\_DISABLED replaces SLAVESIDE\_DISABLED, which is now deprecated and subject to removal in a future version of MySQL.

• Originator

The server ID of the MySQL server on which the event was created; used in replication. This value may be updated by ALTER EVENT to the server ID of the server on which that statement occurs, if executed on a source server. The default value is 0.

• character\_set\_client

The session value of the character\_set\_client system variable when the event was created.

• collation\_connection

The session value of the collation\_connection system variable when the event was created.

• Database Collation

The collation of the database with which the event is associated.

For more information about REPLICA\_SIDE\_DISABLED and the Originator column, see Section 19.5.1.16, "Replication of Invoked Features".

Times displayed by [SHOW EVENTS](#page-110-0) are given in the event time zone, as discussed in Section 27.4.4, "Event Metadata".

Event information is also available from the INFORMATION\_SCHEMA EVENTS table. See Section 28.3.14, "The INFORMATION\_SCHEMA EVENTS Table".

The event action statement is not shown in the output of [SHOW EVENTS](#page-110-0). Use [SHOW CREATE EVENT](#page-99-1) or the INFORMATION\_SCHEMA EVENTS table.

## <span id="page-112-1"></span>**15.7.7.20 SHOW FUNCTION CODE Statement**

```
SHOW FUNCTION CODE func_name
```

This statement is similar to [SHOW PROCEDURE CODE](#page-121-0) but for stored functions. See [Section 15.7.7.29,](#page-121-0) ["SHOW PROCEDURE CODE Statement"](#page-121-0).

## <span id="page-112-2"></span>**15.7.7.21 SHOW FUNCTION STATUS Statement**

```
SHOW FUNCTION STATUS
 [LIKE 'pattern' | WHERE expr]
```

This statement is similar to [SHOW PROCEDURE STATUS](#page-121-1) but for stored functions. See [Section 15.7.7.30, "SHOW PROCEDURE STATUS Statement"](#page-121-1).

## <span id="page-112-0"></span>**15.7.7.22 SHOW GRANTS Statement**

```
SHOW GRANTS
 [FOR user_or_role
 [USING role [, role] ...]]
user_or_role: {
 user (see Section 8.2.4, "Specifying Account Names")
 | role (see Section 8.2.5, "Specifying Role Names".
}
```

This statement displays the privileges and roles that are assigned to a MySQL user account or role, in the form of [GRANT](#page-42-0) statements that must be executed to duplicate the privilege and role assignments.

![](_page_113_Picture_1.jpeg)

#### **Note**

To display nonprivilege information for MySQL accounts, use the [SHOW CREATE](#page-102-0) [USER](#page-102-0) statement. See [Section 15.7.7.13, "SHOW CREATE USER Statement"](#page-102-0).

[SHOW GRANTS](#page-112-0) requires the SELECT privilege for the mysql system schema, except to display privileges and roles for the current user.

To name the account or role for [SHOW GRANTS](#page-112-0), use the same format as for the [GRANT](#page-42-0) statement (for example, 'jeffrey'@'localhost'):

```
mysql> SHOW GRANTS FOR 'jeffrey'@'localhost';
+------------------------------------------------------------------+
| Grants for jeffrey@localhost |
+------------------------------------------------------------------+
| GRANT USAGE ON *.* TO `jeffrey`@`localhost` |
| GRANT SELECT, INSERT, UPDATE ON `db1`.* TO `jeffrey`@`localhost` |
+------------------------------------------------------------------+
```

The host part, if omitted, defaults to '%'. For additional information about specifying account and role names, see Section 8.2.4, "Specifying Account Names", and Section 8.2.5, "Specifying Role Names".

To display the privileges granted to the current user (the account you are using to connect to the server), you can use any of the following statements:

```
SHOW GRANTS;
SHOW GRANTS FOR CURRENT_USER;
SHOW GRANTS FOR CURRENT_USER();
```

If SHOW GRANTS FOR CURRENT\_USER (or any equivalent syntax) is used in definer context, such as within a stored procedure that executes with definer rather than invoker privileges, the grants displayed are those of the definer and not the invoker.

In MySQL 8.4 compared to previous series, [SHOW GRANTS](#page-112-0) no longer displays ALL PRIVILEGES in its global-privileges output because the meaning of ALL PRIVILEGES at the global level varies depending on which dynamic privileges are defined. Instead, [SHOW GRANTS](#page-112-0) explicitly lists each granted global privilege:

```
mysql> SHOW GRANTS FOR 'root'@'localhost';
+---------------------------------------------------------------------+
| Grants for root@localhost |
+---------------------------------------------------------------------+
| GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, RELOAD, |
| SHUTDOWN, PROCESS, FILE, REFERENCES, INDEX, ALTER, SHOW DATABASES, |
| SUPER, CREATE TEMPORARY TABLES, LOCK TABLES, EXECUTE, REPLICATION |
| SLAVE, REPLICATION CLIENT, CREATE VIEW, SHOW VIEW, CREATE ROUTINE, |
| ALTER ROUTINE, CREATE USER, EVENT, TRIGGER, CREATE TABLESPACE, |
| CREATE ROLE, DROP ROLE ON *.* TO `root`@`localhost` WITH GRANT |
| OPTION |
| GRANT PROXY ON ''@'' TO `root`@`localhost` WITH GRANT OPTION |
+---------------------------------------------------------------------+
```

Applications that process [SHOW GRANTS](#page-112-0) output should be adjusted accordingly.

At the global level, GRANT OPTION applies to all granted static global privileges if granted for any of them, but applies individually to granted dynamic privileges. [SHOW GRANTS](#page-112-0) displays global privileges this way:

- One line listing all granted static privileges, if there are any, including WITH GRANT OPTION if appropriate.
- One line listing all granted dynamic privileges for which GRANT OPTION is granted, if there are any, including WITH GRANT OPTION.
- One line listing all granted dynamic privileges for which GRANT OPTION is not granted, if there are any, without WITH GRANT OPTION.

With the optional USING clause, [SHOW GRANTS](#page-112-0) enables you to examine the privileges associated with roles for the user. Each role named in the USING clause must be granted to the user.

Suppose that user u1 is assigned roles r1 and r2, as follows:

```
CREATE ROLE 'r1', 'r2';
GRANT SELECT ON db1.* TO 'r1';
GRANT INSERT, UPDATE, DELETE ON db1.* TO 'r2';
CREATE USER 'u1'@'localhost' IDENTIFIED BY 'u1pass';
GRANT 'r1', 'r2' TO 'u1'@'localhost';
```

[SHOW GRANTS](#page-112-0) without USING shows the granted roles:

```
mysql> SHOW GRANTS FOR 'u1'@'localhost';
+---------------------------------------------+
| Grants for u1@localhost |
+---------------------------------------------+
| GRANT USAGE ON *.* TO `u1`@`localhost` |
| GRANT `r1`@`%`,`r2`@`%` TO `u1`@`localhost` |
+---------------------------------------------+
```

Adding a USING clause causes the statement to also display the privileges associated with each role named in the clause:

```
mysql> SHOW GRANTS FOR 'u1'@'localhost' USING 'r1';
+---------------------------------------------+
| Grants for u1@localhost |
+---------------------------------------------+
| GRANT USAGE ON *.* TO `u1`@`localhost` |
| GRANT SELECT ON `db1`.* TO `u1`@`localhost` |
| GRANT `r1`@`%`,`r2`@`%` TO `u1`@`localhost` |
+---------------------------------------------+
mysql> SHOW GRANTS FOR 'u1'@'localhost' USING 'r2';
+-------------------------------------------------------------+
| Grants for u1@localhost |
+-------------------------------------------------------------+
| GRANT USAGE ON *.* TO `u1`@`localhost` |
| GRANT INSERT, UPDATE, DELETE ON `db1`.* TO `u1`@`localhost` |
| GRANT `r1`@`%`,`r2`@`%` TO `u1`@`localhost` |
+-------------------------------------------------------------+
mysql> SHOW GRANTS FOR 'u1'@'localhost' USING 'r1', 'r2';
+---------------------------------------------------------------------+
| Grants for u1@localhost |
+---------------------------------------------------------------------+
| GRANT USAGE ON *.* TO `u1`@`localhost` |
| GRANT SELECT, INSERT, UPDATE, DELETE ON `db1`.* TO `u1`@`localhost` |
| GRANT `r1`@`%`,`r2`@`%` TO `u1`@`localhost` |
+---------------------------------------------------------------------+
```

![](_page_114_Picture_8.jpeg)

#### **Note**

A privilege granted to an account is always in effect, but a role is not. The active roles for an account can differ across and within sessions, depending on the value of the activate\_all\_roles\_on\_login system variable, the account default roles, and whether [SET ROLE](#page-62-0) has been executed within a session.

MySQL supports partial revocation of global privileges, such that a global privilege can be restricted from applying to particular schemas (see Section 8.2.12, "Privilege Restriction Using Partial Revokes"). To indicate which global schema privileges have been revoked for particular schemas, SHOW GRANTS output includes REVOKE statements:

```
mysql> SET PERSIST partial_revokes = ON;
mysql> CREATE USER u1;
mysql> GRANT SELECT, INSERT, DELETE ON *.* TO u1;
mysql> REVOKE SELECT, INSERT ON mysql.* FROM u1;
mysql> REVOKE DELETE ON world.* FROM u1;
mysql> SHOW GRANTS FOR u1;
+--------------------------------------------------+
| Grants for u1@% |
```

```
+--------------------------------------------------+
| GRANT SELECT, INSERT, DELETE ON *.* TO `u1`@`%` |
| REVOKE SELECT, INSERT ON `mysql`.* FROM `u1`@`%` |
| REVOKE DELETE ON `world`.* FROM `u1`@`%` |
+--------------------------------------------------+
```

[SHOW GRANTS](#page-112-0) does not display privileges that are available to the named account but are granted to a different account. For example, if an anonymous account exists, the named account might be able to use its privileges, but [SHOW GRANTS](#page-112-0) does not display them.

[SHOW GRANTS](#page-112-0) displays mandatory roles named in the mandatory\_roles system variable value as follows:

- [SHOW GRANTS](#page-112-0) without a FOR clause displays privileges for the current user, and includes mandatory roles.
- [SHOW GRANTS FOR](#page-112-0) user displays privileges for the named user, and does not include mandatory roles.

This behavior is for the benefit of applications that use the output of [SHOW GRANTS FOR](#page-112-0) user to determine which privileges are granted explicitly to the named user. Were that output to include mandatory roles, it would be difficult to distinguish roles granted explicitly to the user from mandatory roles.

For the current user, applications can determine privileges with or without mandatory roles by using [SHOW GRANTS](#page-112-0) or [SHOW GRANTS FOR CURRENT\\_USER](#page-112-0), respectively.

## <span id="page-115-0"></span>**15.7.7.23 SHOW INDEX Statement**

```
SHOW [EXTENDED] {INDEX | INDEXES | KEYS}
 {FROM | IN} tbl_name
 [{FROM | IN} db_name]
 [WHERE expr]
```

[SHOW INDEX](#page-115-0) returns table index information. The format resembles that of the SQLStatistics call in ODBC. This statement requires some privilege for any column in the table.

```
mysql> SHOW INDEX FROM City\G
*************************** 1. row ***************************
 Table: city
 Non_unique: 0
 Key_name: PRIMARY
 Seq_in_index: 1
 Column_name: ID
 Collation: A
 Cardinality: 4188
 Sub_part: NULL
 Packed: NULL
 Null:
 Index_type: BTREE
 Comment:
Index_comment:
 Visible: YES
 Expression: NULL
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
```

```
Index_comment:
 Visible: YES
 Expression: NULL
```

An alternative to tbl\_name FROM db\_name syntax is db\_name.tbl\_name. These two statements are equivalent:

```
SHOW INDEX FROM mytable FROM mydb;
SHOW INDEX FROM mydb.mytable;
```

The optional EXTENDED keyword causes the output to include information about hidden indexes that MySQL uses internally and are not accessible by users.

The WHERE clause can be given to select rows using more general conditions, as discussed in Section 28.8, "Extensions to SHOW Statements".

[SHOW INDEX](#page-115-0) returns the following fields:

• Table

The name of the table.

• Non\_unique

0 if the index cannot contain duplicates, 1 if it can.

• Key\_name

The name of the index. If the index is the primary key, the name is always PRIMARY.

• Seq\_in\_index

The column sequence number in the index, starting with 1.

• Column\_name

The column name. See also the description for the Expression column.

• Collation

How the column is sorted in the index. This can have values A (ascending), D (descending), or NULL (not sorted).

• Cardinality

An estimate of the number of unique values in the index. To update this number, run [ANALYZE](#page-66-1) [TABLE](#page-66-1) or (for MyISAM tables) myisamchk -a.

Cardinality is counted based on statistics stored as integers, so the value is not necessarily exact even for small tables. The higher the cardinality, the greater the chance that MySQL uses the index when doing joins.

• Sub\_part

The index prefix. That is, the number of indexed characters if the column is only partly indexed, NULL if the entire column is indexed.

![](_page_116_Picture_24.jpeg)

## **Note**

Prefix limits are measured in bytes. However, prefix lengths for index specifications in CREATE TABLE, ALTER TABLE, and CREATE INDEX statements are interpreted as number of characters for nonbinary string types (CHAR, VARCHAR, TEXT) and number of bytes for binary string types (BINARY, VARBINARY, BLOB). Take this into account when specifying a prefix length for a nonbinary string column that uses a multibyte character set.

For additional information about index prefixes, see Section 10.3.5, "Column Indexes", and Section 15.1.15, "CREATE INDEX Statement".

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

• Visible

Whether the index is visible to the optimizer. See Section 10.3.12, "Invisible Indexes".

• Expression

MySQL supports functional key parts (see Functional Key Parts); this affects both the Column\_name and Expression columns:

- For a nonfunctional key part, Column\_name indicates the column indexed by the key part and Expression is NULL.
- For a functional key part, Column\_name column is NULL and Expression indicates the expression for the key part.

Information about table indexes is also available from the INFORMATION\_SCHEMA STATISTICS table. See Section 28.3.34, "The INFORMATION\_SCHEMA STATISTICS Table". The extended information about hidden indexes is available only using SHOW EXTENDED INDEX; it cannot be obtained from the STATISTICS table.

You can list a table's indexes with the mysqlshow -k db\_name tbl\_name command.

SHOW INDEX includes the table's generated invisible key, if it has one, by default. You can cause this information to be suppressed in the statement's output by setting show\_gipk\_in\_create\_table\_and\_information\_schema = OFF. For more information, see Section 15.1.20.11, "Generated Invisible Primary Keys".