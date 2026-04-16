---
source: MySQL 8.0 Reference
title: 00_Overview
---

This section describes sources of information about keyring use.

To see whether a keyring plugin is loaded, check the Information Schema PLUGINS table or use the SHOW PLUGINS statement (see Section 7.6.2, "Obtaining Server Plugin Information"). For example:

```
mysql> SELECT PLUGIN_NAME, PLUGIN_STATUS
 FROM INFORMATION_SCHEMA.PLUGINS
 WHERE PLUGIN_NAME LIKE 'keyring%';
+--------------+---------------+
```

```
| PLUGIN_NAME | PLUGIN_STATUS |
+--------------+---------------+
| keyring_file | ACTIVE |
+--------------+---------------+
```

To see which keys exist, check the Performance Schema keyring\_keys table:

```
mysql> SELECT * FROM performance_schema.keyring_keys;
+-----------------------------+--------------+----------------+
| KEY_ID | KEY_OWNER | BACKEND_KEY_ID |
+-----------------------------+--------------+----------------+
| audit_log-20210322T130749-1 | | |
| MyKey | me@localhost | |
| YourKey | me@localhost | |
+-----------------------------+--------------+----------------+
```

To see whether a keyring component is loaded, check the Performance Schema keyring\_component\_status table. For example:

| mysql> SELECT * FROM performance_schema.keyring_component_status;                                                                                                                                                                                                                                                           |  |  |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--|--|
| +++<br>  STATUS_KEY<br>  STATUS_VALUE                                                                                                                                                                                                                                                                                       |  |  |
| +++<br>  Component_name<br>  component_keyring_file<br>  Author<br>  Oracle Corporation<br>  License<br>  GPL<br>  Implementation_name   component_keyring_file<br>  Version<br>  1.0<br>  Component_status<br>  Active<br>  Data_file<br>  /usr/local/mysql/keyring/component_keyring_file  <br>  Read_only<br>  No<br>+++ |  |  |

A Component\_status value of Active indicates that the component initialized successfully. If the component loaded but failed to initialize, the value is Disabled.

# <span id="page-198-2"></span><span id="page-198-0"></span>**8.4.4.18 Keyring Command Options**

MySQL supports the following keyring-related command-line options:

• [--keyring-migration-destination=](#page-198-0)plugin

| Command-Line Format | keyring-migration<br>destination=plugin_name |
|---------------------|----------------------------------------------|
| Type                | String                                       |

The destination keyring plugin for key migration. See [Section 8.4.4.14, "Migrating Keys Between](#page-182-0) [Keyring Keystores"](#page-182-0). The option value interpretation depends on whether --keyring-migrationto-component is specified:

- If no, the option value is a keyring plugin, interpreted the same way as for [--keyring](#page-199-0)[migration-source](#page-199-0).
  - If yes, the option value is a keyring component, specified as the component library name in the plugin directory, including any platform-specific extension such as .so or .dll.

![](_page_198_Picture_14.jpeg)

•

#### **Note**

[--keyring-migration-source](#page-199-0) and [--keyring-migration](#page-198-0)[destination](#page-198-0) are mandatory for all keyring migration operations. The source and destination plugins must differ, and the migration server must support both plugins.

<span id="page-198-1"></span>• [--keyring-migration-host=](#page-198-1)host\_name

| Command-Line Format | keyring-migration-host=host_name |
|---------------------|----------------------------------|
| Type                | String                           |
| Default Value       | localhost                        |

The host location of the running server that is currently using one of the key migration keystores. See [Section 8.4.4.14, "Migrating Keys Between Keyring Keystores"](#page-182-0). Migration always occurs on the local host, so the option always specifies a value for connecting to a local server, such as localhost, 127.0.0.1, ::1, or the local host IP address or host name.

<span id="page-199-1"></span>• [--keyring-migration-password\[=](#page-199-1)password]

| Command-Line Format | keyring-migration   |
|---------------------|---------------------|
|                     | password[=password] |
| Type                | String              |

The password of the MySQL account used for connecting to the running server that is currently using one of the key migration keystores. See [Section 8.4.4.14, "Migrating Keys Between Keyring](#page-182-0) [Keystores".](#page-182-0)

The password value is optional. If not given, the server prompts for one. If given, there must be no space between [--keyring-migration-password=](#page-199-1) and the password following it. If no password option is specified, the default is to send no password.

Specifying a password on the command line should be considered insecure. See Section 8.1.2.1, "End-User Guidelines for Password Security". You can use an option file to avoid giving the password on the command line. In this case, the file should have a restrictive mode and be accessible only to the account used to run the migration server.

<span id="page-199-2"></span>• [--keyring-migration-port=](#page-199-2)port\_num

| Command-Line Format | keyring-migration-port=port_num |
|---------------------|---------------------------------|
| Type                | Numeric                         |
| Default Value       | 3306                            |

For TCP/IP connections, the port number for connecting to the running server that is currently using one of the key migration keystores. See [Section 8.4.4.14, "Migrating Keys Between Keyring](#page-182-0) [Keystores".](#page-182-0)

<span id="page-199-3"></span>• [--keyring-migration-socket=](#page-199-3)path

| Command-Line Format | keyring-migration<br>socket={file_name pipe_name} |
|---------------------|---------------------------------------------------|
| Type                | String                                            |

For Unix socket file or Windows named pipe connections, the socket file or named pipe for connecting to the running server that is currently using one of the key migration keystores. See [Section 8.4.4.14, "Migrating Keys Between Keyring Keystores"](#page-182-0).

<span id="page-199-0"></span>• [--keyring-migration-source=](#page-199-0)plugin

| Command-Line Format | keyring-migration  |
|---------------------|--------------------|
|                     | source=plugin_name |

| Type | String |
|------|--------|
|------|--------|

The source keyring plugin for key migration. See Section 8.4.4.14, "Migrating Keys Between Keyring Keystores".

The option value is similar to that for --plugin-load, except that only one plugin library can be specified. The value is given as plugin\_library or name=plugin\_library, where plugin\_library is the name of a library file that contains plugin code, and name is the name of a plugin to load. If a plugin library is named without any preceding plugin name, the server loads all plugins in the library. With a preceding plugin name, the server loads only the named plugin from the library. The server looks for plugin library files in the directory named by the plugin\_dir system variable.

![](_page_0_Picture_4.jpeg)

#### **Note**

--keyring-migration-source and --keyring-migrationdestination are mandatory for all keyring migration operations. The source and destination plugins must differ, and the migration server must support both plugins.

<span id="page-0-0"></span>• [--keyring-migration-to-component](#page-0-0)

| Command-Line Format | keyring-migration-to<br>component[={OFF ON}] |
|---------------------|----------------------------------------------|
| Type                | Boolean                                      |
| Default Value       | OFF                                          |

Indicates that a key migration is from a keyring plugin to a keyring component. This option makes it possible to migrate keys from any keyring plugin to any keyring component, which facilitates transitioning a MySQL installation from keyring plugins to keyring components.

For key migration from one keyring component to another, use the mysql\_migrate\_keyring utility. Migration from a keyring component to a keyring plugin is not supported. See Section 8.4.4.14, "Migrating Keys Between Keyring Keystores".

<span id="page-0-1"></span>• [--keyring-migration-user=](#page-0-1)user\_name

| Command-Line Format | keyring-migration-user=user_name |
|---------------------|----------------------------------|
| Type                | String                           |

The user name of the MySQL account used for connecting to the running server that is currently using one of the key migration keystores. See Section 8.4.4.14, "Migrating Keys Between Keyring Keystores".