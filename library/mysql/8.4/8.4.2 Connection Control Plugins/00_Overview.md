---
source: MySQL 8.4 Reference
title: 00_Overview
---

MySQL Server includes a plugin library that enables administrators to introduce an increasing delay in server response to connection attempts after a configurable number of consecutive failed attempts. This capability provides a deterrent that slows down brute force attacks against MySQL user accounts. The plugin library contains two plugins:

• CONNECTION\_CONTROL checks incoming connection attempts and adds a delay to server responses as necessary. This plugin also exposes system variables that enable its operation to be configured and a status variable that provides rudimentary monitoring information.

The CONNECTION\_CONTROL plugin uses the audit plugin interface (see [Writing Audit Plugins](https://dev.mysql.com/doc/extending-mysql/8.4/en/writing-audit-plugins.md)). To collect information, it subscribes to the MYSQL\_AUDIT\_CONNECTION\_CLASSMASK event class, and processes MYSQL\_AUDIT\_CONNECTION\_CONNECT and MYSQL\_AUDIT\_CONNECTION\_CHANGE\_USER subevents to check whether the server should introduce a delay before responding to connection attempts.

• CONNECTION\_CONTROL\_FAILED\_LOGIN\_ATTEMPTS implements an INFORMATION\_SCHEMA table that exposes more detailed monitoring information for failed connection attempts. For more information about this table, see Section 28.6.2, "The INFORMATION\_SCHEMA CONNECTION\_CONTROL\_FAILED\_LOGIN\_ATTEMPTS Table".

The following sections provide information about connection control plugin installation and configuration.

# <span id="page-186-0"></span>**8.4.2.1 Connection Control Plugin Installation**

This section describes how to install the connection control plugins, CONNECTION\_CONTROL and CONNECTION\_CONTROL\_FAILED\_LOGIN\_ATTEMPTS. For general information about installing plugins, see Section 7.6.1, "Installing and Uninstalling Plugins".

To be usable by the server, the plugin library file must be located in the MySQL plugin directory (the directory named by the plugin\_dir system variable). If necessary, configure the plugin directory location by setting the value of plugin\_dir at server startup.

The plugin library file base name is connection\_control. The file name suffix differs per platform (for example, .so for Unix and Unix-like systems, .dll for Windows).

To load the plugins at server startup, use the --plugin-load-add option to name the library file that contains them. With this plugin-loading method, the option must be given each time the server starts. For example, put these lines in the server my.cnf file, adjusting the .so suffix for your platform as necessary:

```
[mysqld]
plugin-load-add=connection_control.so
```

After modifying my.cnf, restart the server to cause the new settings to take effect.

Alternatively, to load the plugins at runtime, use these statements, adjusting the .so suffix for your platform as necessary:

```
INSTALL PLUGIN CONNECTION_CONTROL
 SONAME 'connection_control.so';
```

```
INSTALL PLUGIN CONNECTION_CONTROL_FAILED_LOGIN_ATTEMPTS
 SONAME 'connection_control.so';
```

INSTALL PLUGIN loads the plugin immediately, and also registers it in the mysql.plugins system table to cause the server to load it for each subsequent normal startup without the need for - plugin-load-add.

To verify plugin installation, examine the Information Schema PLUGINS table or use the SHOW PLUGINS statement (see Section 7.6.2, "Obtaining Server Plugin Information"). For example:

```
mysql> SELECT PLUGIN_NAME, PLUGIN_STATUS
 FROM INFORMATION_SCHEMA.PLUGINS
 WHERE PLUGIN_NAME LIKE 'connection%';
+------------------------------------------+---------------+
| PLUGIN_NAME | PLUGIN_STATUS |
+------------------------------------------+---------------+
| CONNECTION_CONTROL | ACTIVE |
| CONNECTION_CONTROL_FAILED_LOGIN_ATTEMPTS | ACTIVE |
+------------------------------------------+---------------+
```

If a plugin fails to initialize, check the server error log for diagnostic messages.

If the plugins have been previously registered with INSTALL PLUGIN or are loaded with --pluginload-add, you can use the --connection-control and --connection-control-failedlogin-attempts options at server startup to control plugin activation. For example, to load the plugins at startup and prevent them from being removed at runtime, use these options:

```
[mysqld]
plugin-load-add=connection_control.so
connection-control=FORCE_PLUS_PERMANENT
connection-control-failed-login-attempts=FORCE_PLUS_PERMANENT
```

If it is desired to prevent the server from running without a given connection control plugin, use an option value of FORCE or FORCE\_PLUS\_PERMANENT to force server startup to fail if the plugin does not initialize successfully.

![](_page_187_Picture_9.jpeg)

### **Note**

It is possible to install one plugin without the other, but both must be installed for full connection control capability. In particular, installing only the CONNECTION\_CONTROL\_FAILED\_LOGIN\_ATTEMPTS plugin is of little use because, without the CONNECTION\_CONTROL plugin to provide the data that populates the CONNECTION\_CONTROL\_FAILED\_LOGIN\_ATTEMPTS table, the table is always empty.

- [Connection Delay Configuration](#page-187-0)
- [Connection Failure Assessment](#page-189-0)
- [Connection Failure Monitoring](#page-190-0)

### <span id="page-187-0"></span>**Connection Delay Configuration**

To enable configuring its operation, the CONNECTION\_CONTROL plugin exposes these system variables:

- [connection\\_control\\_failed\\_connections\\_threshold](#page-190-1): The number of consecutive failed connection attempts permitted to accounts before the server adds a delay for subsequent connection attempts. To disable failed-connection counting, set [connection\\_control\\_failed\\_connections\\_threshold](#page-190-1) to zero.
- [connection\\_control\\_min\\_connection\\_delay](#page-191-0): The minimum delay in milliseconds for connection failures above the threshold.
- [connection\\_control\\_max\\_connection\\_delay](#page-191-1): The maximum delay in milliseconds for connection failures above the threshold.

If [connection\\_control\\_failed\\_connections\\_threshold](#page-190-1) is nonzero, failed-connection counting is enabled and has these properties:

- The delay is zero up through [connection\\_control\\_failed\\_connections\\_threshold](#page-190-1) consecutive failed connection attempts.
- Thereafter, the server adds an increasing delay for subsequent consecutive attempts, until a successful connection occurs. The initial unadjusted delays begin at 1000 milliseconds (1 second) and increase by 1000 milliseconds per attempt. That is, once delay has been activated for an account, the unadjusted delays for subsequent failed attempts are 1000 milliseconds, 2000 milliseconds, 3000 milliseconds, and so forth.
- The actual delay experienced by a client is the unadjusted delay, adjusted to lie within the values of the [connection\\_control\\_min\\_connection\\_delay](#page-191-0) and [connection\\_control\\_max\\_connection\\_delay](#page-191-1) system variables, inclusive.
- Once delay has been activated for an account, the first successful connection thereafter by the account also experiences a delay, but failure counting is reset for subsequent connections.

For example, with the default [connection\\_control\\_failed\\_connections\\_threshold](#page-190-1) value of 3, there is no delay for the first three consecutive failed connection attempts by an account. The actual adjusted delays experienced by the account for the fourth and subsequent failed connections depend on the [connection\\_control\\_min\\_connection\\_delay](#page-191-0) and [connection\\_control\\_max\\_connection\\_delay](#page-191-1) values:

- If [connection\\_control\\_min\\_connection\\_delay](#page-191-0) and [connection\\_control\\_max\\_connection\\_delay](#page-191-1) are 1000 and 20000, the adjusted delays are the same as the unadjusted delays, up to a maximum of 20000 milliseconds. The fourth and subsequent failed connections are delayed by 1000 milliseconds, 2000 milliseconds, 3000 milliseconds, and so forth.
- If [connection\\_control\\_min\\_connection\\_delay](#page-191-0) and [connection\\_control\\_max\\_connection\\_delay](#page-191-1) are 1500 and 20000, the adjusted delays for the fourth and subsequent failed connections are 1500 milliseconds, 2000 milliseconds, 3000 milliseconds, and so forth, up to a maximum of 20000 milliseconds.
- If [connection\\_control\\_min\\_connection\\_delay](#page-191-0) and [connection\\_control\\_max\\_connection\\_delay](#page-191-1) are 2000 and 3000, the adjusted delays for the fourth and subsequent failed connections are 2000 milliseconds, 2000 milliseconds, and 3000 milliseconds, with all subsequent failed connections also delayed by 3000 milliseconds.

You can set the CONNECTION\_CONTROL system variables at server startup or runtime. Suppose that you want to permit four consecutive failed connection attempts before the server starts delaying its responses, with a minimum delay of 2000 milliseconds. To set the relevant variables at server startup, put these lines in the server my.cnf file:

```
[mysqld]
plugin-load-add=connection_control.so
connection-control-failed-connections-threshold=4
connection-control-min-connection-delay=2000
```

To set and persist the variables at runtime, use these statements:

```
SET PERSIST connection_control_failed_connections_threshold = 4;
SET PERSIST connection_control_min_connection_delay = 2000;
```

SET PERSIST sets a value for the running MySQL instance. It also saves the value, causing it to carry over to subsequent server restarts. To change a value for the running MySQL instance without having it carry over to subsequent restarts, use the GLOBAL keyword rather than PERSIST. See Section 15.7.6.1, "SET Syntax for Variable Assignment".

The [connection\\_control\\_min\\_connection\\_delay](#page-191-0) and [connection\\_control\\_max\\_connection\\_delay](#page-191-1) system variables both have minimum and maximum values of 1000 and 2147483647. In addition, the permitted range of values of each variable also depends on the current value of the other:

- [connection\\_control\\_min\\_connection\\_delay](#page-191-0) cannot be set greater than the current value of [connection\\_control\\_max\\_connection\\_delay](#page-191-1).
- [connection\\_control\\_max\\_connection\\_delay](#page-191-1) cannot be set less than the current value of [connection\\_control\\_min\\_connection\\_delay](#page-191-0).

Thus, to make the changes required for some configurations, you might need to set the variables in a specific order. Suppose that the current minimum and maximum delays are 1000 and 2000, and that you want to set them to 3000 and 5000. You cannot first set [connection\\_control\\_min\\_connection\\_delay](#page-191-0) to 3000 because that is greater than the current [connection\\_control\\_max\\_connection\\_delay](#page-191-1) value of 2000. Instead, set [connection\\_control\\_max\\_connection\\_delay](#page-191-1) to 5000, then set [connection\\_control\\_min\\_connection\\_delay](#page-191-0) to 3000.

### <span id="page-189-0"></span>**Connection Failure Assessment**

When the CONNECTION\_CONTROL plugin is installed, it checks connection attempts and tracks whether they fail or succeed. For this purpose, a failed connection attempt is one for which the client user and host match a known MySQL account but the provided credentials are incorrect, or do not match any known account.

Failed-connection counting is based on the user/host combination for each connection attempt. Determination of the applicable user name and host name takes proxying into account and occurs as follows:

- If the client user proxies another user, the account for failed-connection counting is the proxying user, not the proxied user. For example, if external\_user@example.com proxies proxy\_user@example.com, connection counting uses the proxying user, external\_user@example.com, rather than the proxied user, proxy\_user@example.com. Both external\_user@example.com and proxy\_user@example.com must have valid entries in the mysql.user system table and a proxy relationship between them must be defined in the mysql.proxies\_priv system table (see [Section 8.2.19, "Proxy Users"\)](#page-50-0).
- If the client user does not proxy another user, but does match a mysql.user entry, counting uses the CURRENT\_USER() value corresponding to that entry. For example, if a user user1 connecting from a host host1.example.com matches a user1@host1.example.com entry, counting uses user1@host1.example.com. If the user matches a user1@%.example.com, user1@%.com, or user1@% entry instead, counting uses user1@%.example.com, user1@%.com, or user1@%, respectively.

For the cases just described, the connection attempt matches some mysql.user entry, and whether the request succeeds or fails depends on whether the client provides the correct authentication credentials. For example, if the client presents an incorrect password, the connection attempt fails.

If the connection attempt matches no mysql.user entry, the attempt fails. In this case, no CURRENT\_USER() value is available and connection-failure counting uses the user name provided by the client and the client host as determined by the server. For example, if a client attempts to connect as user user2 from host host2.example.com, the user name part is available in the client request and the server determines the host information. The user/host combination used for counting is user2@host2.example.com.

![](_page_189_Picture_12.jpeg)

# **Note**

The server maintains information about which client hosts can possibly connect to the server (essentially the union of host values for mysql.user entries). If a client attempts to connect from any other host, the server rejects the attempt at an early stage of connection setup:

ERROR 1130 (HY000): Host 'host\_name' is not

allowed to connect to this MySQL server

Because this type of rejection occurs so early, CONNECTION\_CONTROL does not see it, and does not count it.

### <span id="page-190-0"></span>**Connection Failure Monitoring**

To monitor failed connections, use these information sources:

- The [Connection\\_control\\_delay\\_generated](#page-192-1) status variable indicates the number of times the server added a delay to its response to a failed connection attempt. This does not count attempts that occur before reaching the threshold defined by the [connection\\_control\\_failed\\_connections\\_threshold](#page-190-1) system variable.
- The INFORMATION\_SCHEMA CONNECTION\_CONTROL\_FAILED\_LOGIN\_ATTEMPTS table provides information about the current number of consecutive failed connection attempts per account (user/ host combination). This counts all failed attempts, regardless of whether they were delayed.

Assigning a value to [connection\\_control\\_failed\\_connections\\_threshold](#page-190-1) at runtime has these effects:

- All accumulated failed-connection counters are reset to zero.
- The [Connection\\_control\\_delay\\_generated](#page-192-1) status variable is reset to zero.
- The CONNECTION\_CONTROL\_FAILED\_LOGIN\_ATTEMPTS table becomes empty.