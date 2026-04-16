---
source: MySQL 8.0 Reference
title: 00_Overview
---

![](_page_58_Picture_15.jpeg)

## **Note**

Windows pluggable authentication is an extension included in MySQL Enterprise Edition, a commercial product. To learn more about commercial products, see<https://www.mysql.com/products/>.

MySQL Enterprise Edition for Windows supports an authentication method that performs external authentication on Windows, enabling MySQL Server to use native Windows services to authenticate client connections. Users who have logged in to Windows can connect from MySQL client programs to the server based on the information in their environment without specifying an additional password.

The client and server exchange data packets in the authentication handshake. As a result of this exchange, the server creates a security context object that represents the identity of the client in the Windows OS. This identity includes the name of the client account. Windows pluggable authentication uses the identity of the client to check whether it is a given account or a member of a group. By default, negotiation uses Kerberos to authenticate, then NTLM if Kerberos is unavailable.

Windows pluggable authentication provides these capabilities:

- External authentication: Windows authentication enables MySQL Server to accept connections from users defined outside the MySQL grant tables who have logged in to Windows.
- Proxy user support: Windows authentication can return to MySQL a user name different from the external user name passed by the client program. This means that the plugin can return the MySQL user that defines the privileges the external Windows-authenticated user should have. For example, a Windows user named joe can connect and have the privileges of a MySQL user named developer.

The following table shows the plugin and library file names. The file must be located in the directory named by the plugin\_dir system variable.

**Table 8.21 Plugin and Library Names for Windows Authentication**

| Plugin or File     | Plugin or File Name           |
|--------------------|-------------------------------|
| Server-side plugin | authentication_windows        |
| Client-side plugin | authentication_windows_client |
| Library file       | authentication_windows.dll    |

The library file includes only the server-side plugin. The client-side plugin is built into the libmysqlclient client library.

The server-side Windows authentication plugin is included only in MySQL Enterprise Edition. It is not included in MySQL community distributions. The client-side plugin is included in all distributions, including community distributions. This enables clients from any distribution to connect to a server that has the server-side plugin loaded.

The following sections provide installation and usage information specific to Windows pluggable authentication:

- [Installing Windows Pluggable Authentication](#page-59-0)
- [Uninstalling Windows Pluggable Authentication](#page-60-0)
- [Using Windows Pluggable Authentication](#page-60-1)

For general information about pluggable authentication in MySQL, see Section 8.2.17, "Pluggable Authentication". For proxy user information, see Section 8.2.19, "Proxy Users".

# <span id="page-59-0"></span>**Installing Windows Pluggable Authentication**

This section describes how to install the server-side Windows authentication plugin. For general information about installing plugins, see Section 7.6.1, "Installing and Uninstalling Plugins".

To be usable by the server, the plugin library file must be located in the MySQL plugin directory (the directory named by the plugin\_dir system variable). If necessary, configure the plugin directory location by setting the value of plugin\_dir at server startup.

To load the plugin at server startup, use the --plugin-load-add option to name the library file that contains it. With this plugin-loading method, the option must be given each time the server starts. For example, put these lines in the server my.cnf file:

```
[mysqld]
plugin-load-add=authentication_windows.dll
```

After modifying my.cnf, restart the server to cause the new settings to take effect.

Alternatively, to load the plugin at runtime, use this statement:

```
INSTALL PLUGIN authentication_windows SONAME 'authentication_windows.dll';
```

INSTALL PLUGIN loads the plugin immediately, and also registers it in the mysql.plugins system table to cause the server to load it for each subsequent normal startup without the need for - plugin-load-add.

To verify plugin installation, examine the Information Schema PLUGINS table or use the SHOW PLUGINS statement (see Section 7.6.2, "Obtaining Server Plugin Information"). For example:

```
mysql> SELECT PLUGIN_NAME, PLUGIN_STATUS
 FROM INFORMATION_SCHEMA.PLUGINS
 WHERE PLUGIN_NAME LIKE '%windows%';
+------------------------+---------------+
| PLUGIN_NAME | PLUGIN_STATUS |
+------------------------+---------------+
| authentication_windows | ACTIVE |
+------------------------+---------------+
```

If the plugin fails to initialize, check the server error log for diagnostic messages.

To associate MySQL accounts with the Windows authentication plugin, see [Using Windows Pluggable Authentication](#page-60-1). Additional plugin control is provided by the authentication\_windows\_use\_principal\_name and authentication\_windows\_log\_level system variables. See Section 7.1.8, "Server System Variables".

## <span id="page-60-0"></span>**Uninstalling Windows Pluggable Authentication**

The method used to uninstall the Windows authentication plugin depends on how you installed it:

- If you installed the plugin at server startup using a --plugin-load-add option, restart the server without the option.
- If you installed the plugin at runtime using an INSTALL PLUGIN statement, it remains installed across server restarts. To uninstall it, use UNINSTALL PLUGIN:

```
UNINSTALL PLUGIN authentication_windows;
```

In addition, remove any startup options that set Windows plugin-related system variables.

## <span id="page-60-1"></span>**Using Windows Pluggable Authentication**

The Windows authentication plugin supports the use of MySQL accounts such that users who have logged in to Windows can connect to the MySQL server without having to specify an additional password. It is assumed that the server is running with the server-side plugin enabled, as described in [Installing Windows Pluggable Authentication](#page-59-0). Once the DBA has enabled the server-side plugin and set up accounts to use it, clients can connect using those accounts with no other setup required on their part.

To refer to the Windows authentication plugin in the IDENTIFIED WITH clause of a CREATE USER statement, use the name authentication\_windows. Suppose that the Windows users Rafal and Tasha should be permitted to connect to MySQL, as well as any users in the Administrators or Power Users group. To set this up, create a MySQL account named sql\_admin that uses the Windows plugin for authentication:

```
CREATE USER sql_admin
 IDENTIFIED WITH authentication_windows
 AS 'Rafal, Tasha, Administrators, "Power Users"';
```

The plugin name is authentication\_windows. The string following the AS keyword is the authentication string. It specifies that the Windows users named Rafal or Tasha are permitted to authenticate to the server as the MySQL user sql\_admin, as are any Windows users in the Administrators or Power Users group. The latter group name contains a space, so it must be quoted with double quote characters.

After you create the sql\_admin account, a user who has logged in to Windows can attempt to connect to the server using that account:

```
C:\> mysql --user=sql_admin
```

No password is required here. The authentication\_windows plugin uses the Windows security API to check which Windows user is connecting. If that user is named Rafal or Tasha, or is a member of the Administrators or Power Users group, the server grants access and the client is authenticated as sql\_admin and has whatever privileges are granted to the sql\_admin account. Otherwise, the server denies access.

Authentication string syntax for the Windows authentication plugin follows these rules:

- The string consists of one or more user mappings separated by commas.
- Each user mapping associates a Windows user or group name with a MySQL user name:

```
win_user_or_group_name=mysql_user_name
win_user_or_group_name
```

For the latter syntax, with no mysql\_user\_name value given, the implicit value is the MySQL user created by the CREATE USER statement. Thus, these statements are equivalent:

```
CREATE USER sql_admin
 IDENTIFIED WITH authentication_windows
 AS 'Rafal, Tasha, Administrators, "Power Users"';
CREATE USER sql_admin
 IDENTIFIED WITH authentication_windows
 AS 'Rafal=sql_admin, Tasha=sql_admin, Administrators=sql_admin,
 "Power Users"=sql_admin';
```

- Each backslash character (\) in a value must be doubled because backslash is the escape character in MySQL strings.
- Leading and trailing spaces not inside double quotation marks are ignored.
- Unquoted win\_user\_or\_group\_name and mysql\_user\_name values can contain anything except equal sign, comma, or space.
- If a win\_user\_or\_group\_name and or mysql\_user\_name value is quoted with double quotation marks, everything between the quotation marks is part of the value. This is necessary, for example, if the name contains space characters. All characters within double quotes are legal except double quotation mark and backslash. To include either character, escape it with a backslash.
- win\_user\_or\_group\_name values use conventional syntax for Windows principals, either local or in a domain. Examples (note the doubling of backslashes):

```
domain\\user
.\\user
domain\\group
.\\group
BUILTIN\\WellKnownGroup
```

When invoked by the server to authenticate a client, the plugin scans the authentication string left to right for a user or group match to the Windows user. If there is a match, the plugin returns the corresponding mysql\_user\_name to the MySQL server. If there is no match, authentication fails.

A user name match takes preference over a group name match. Suppose that the Windows user named win\_user is a member of win\_group and the authentication string looks like this:

```
'win_group = sql_user1, win_user = sql_user2'
```

When win\_user connects to the MySQL server, there is a match both to win\_group and to win\_user. The plugin authenticates the user as sql\_user2 because the more-specific user match takes precedence over the group match, even though the group is listed first in the authentication string.

Windows authentication always works for connections from the same computer on which the server is running. For cross-computer connections, both computers must be registered with Microsoft Active Directory. If they are in the same Windows domain, it is unnecessary to specify a domain name. It is also possible to permit connections from a different domain, as in this example:

```
CREATE USER sql_accounting
 IDENTIFIED WITH authentication_windows
 AS 'SomeDomain\\Accounting';
```

Here SomeDomain is the name of the other domain. The backslash character is doubled because it is the MySQL escape character within strings.

MySQL supports the concept of proxy users whereby a client can connect and authenticate to the MySQL server using one account but while connected has the privileges of another account (see Section 8.2.19, "Proxy Users"). Suppose that you want Windows users to connect using a single user name but be mapped based on their Windows user and group names onto specific MySQL accounts as follows:

- The local\_user and MyDomain\domain\_user local and domain Windows users should map to the local\_wlad MySQL account.
- Users in the MyDomain\Developers domain group should map to the local\_dev MySQL account.
- Local machine administrators should map to the local\_admin MySQL account.

To set this up, create a proxy account for Windows users to connect to, and configure this account so that users and groups map to the appropriate MySQL accounts (local\_wlad, local\_dev, local\_admin). In addition, grant the MySQL accounts the privileges appropriate to the operations they need to perform. The following instructions use win\_proxy as the proxy account, and local\_wlad, local\_dev, and local\_admin as the proxied accounts.

1. Create the proxy MySQL account:

```
CREATE USER win_proxy
 IDENTIFIED WITH authentication_windows
 AS 'local_user = local_wlad,
 MyDomain\\domain_user = local_wlad,
 MyDomain\\Developers = local_dev,
 BUILTIN\\Administrators = local_admin';
```

2. For proxying to work, the proxied accounts must exist, so create them:

```
CREATE USER local_wlad
 IDENTIFIED WITH mysql_no_login;
CREATE USER local_dev
 IDENTIFIED WITH mysql_no_login;
CREATE USER local_admin
 IDENTIFIED WITH mysql_no_login;
```

The proxied accounts use the mysql\_no\_login authentication plugin to prevent clients from using the accounts to log in directly to the MySQL server. Instead, users who authenticate using Windows are expected to use the win\_proxy proxy account. (This assumes that the plugin is installed. For instructions, see [Section 8.4.1.9, "No-Login Pluggable Authentication".](#page-94-0)) For alternative methods of protecting proxied accounts against direct use, see Preventing Direct Login to Proxied Accounts.

You should also execute GRANT statements (not shown) that grant each proxied account the privileges required for MySQL access.

3. Grant to the proxy account the PROXY privilege for each proxied account:

```
GRANT PROXY ON local_wlad TO win_proxy;
```

```
GRANT PROXY ON local_dev TO win_proxy;
GRANT PROXY ON local_admin TO win_proxy;
```

Now the Windows users local\_user and MyDomain\domain\_user can connect to the MySQL server as win\_proxy and when authenticated have the privileges of the account given in the authentication string (in this case, local\_wlad). A user in the MyDomain\Developers group who connects as win\_proxy has the privileges of the local\_dev account. A user in the BUILTIN \Administrators group has the privileges of the local\_admin account.

To configure authentication so that all Windows users who do not have their own MySQL account go through a proxy account, substitute the default proxy account (''@'') for win\_proxy in the preceding instructions. For information about default proxy accounts, see Section 8.2.19, "Proxy Users".

![](_page_63_Picture_4.jpeg)

## **Note**

If your MySQL installation has anonymous users, they might conflict with the default proxy user. For more information about this issue, and ways of dealing with it, see Default Proxy User and Anonymous User Conflicts.

To use the Windows authentication plugin with Connector/NET connection strings in Connector/NET 8.0 and higher, see [Connector/NET Authentication](https://dev.mysql.com/doc/connector-net/en/connector-net-authentication.md).

# <span id="page-63-0"></span>**8.4.1.7 LDAP Pluggable Authentication**

![](_page_63_Picture_9.jpeg)

#### **Note**

LDAP pluggable authentication is an extension included in MySQL Enterprise Edition, a commercial product. To learn more about commercial products, see <https://www.mysql.com/products/>.

MySQL Enterprise Edition supports an authentication method that enables MySQL Server to use LDAP (Lightweight Directory Access Protocol) to authenticate MySQL users by accessing directory services such as X.500. MySQL uses LDAP to fetch user, credential, and group information.

LDAP pluggable authentication provides these capabilities:

- External authentication: LDAP authentication enables MySQL Server to accept connections from users defined outside the MySQL grant tables in LDAP directories.
- Proxy user support: LDAP authentication can return to MySQL a user name different from the external user name passed by the client program, based on the LDAP groups the external user is a member of. This means that an LDAP plugin can return the MySQL user that defines the privileges the external LDAP-authenticated user should have. For example, an LDAP user named joe can connect and have the privileges of a MySQL user named developer, if the LDAP group for joe is developer.
- Security: Using TLS, connections to the LDAP server can be secure.

Server and client plugins are available for simple and SASL-based LDAP authentication. On Microsoft Windows, the server plugin for SASL-based LDAP authentication is not supported, but the client plugin is.

The following tables show the plugin and library file names for simple and SASL-based LDAP authentication. The file name suffix might differ on your system. The files must be located in the directory named by the plugin\_dir system variable.

**Table 8.22 Plugin and Library Names for Simple LDAP Authentication**

| Plugin or File          | Plugin or File Name           |
|-------------------------|-------------------------------|
| Server-side plugin name | authentication_ldap_simple    |
| Client-side plugin name | mysql_clear_password          |
| Library file name       | authentication_ldap_simple.so |

**Table 8.23 Plugin and Library Names for SASL-Based LDAP Authentication**

| Plugin or File          | Plugin or File Name                                                |
|-------------------------|--------------------------------------------------------------------|
| Server-side plugin name | authentication_ldap_sasl                                           |
| Client-side plugin name | authentication_ldap_sasl_client                                    |
| Library file names      | authentication_ldap_sasl.so,<br>authentication_ldap_sasl_client.so |

The library files include only the authentication\_ldap\_XXX authentication plugins. The client-side mysql\_clear\_password plugin is built into the libmysqlclient client library.

Each server-side LDAP plugin works with a specific client-side plugin:

- The server-side authentication\_ldap\_simple plugin performs simple LDAP authentication. For connections by accounts that use this plugin, client programs use the client-side mysql\_clear\_password plugin, which sends the password to the server as cleartext. No password hashing or encryption is used, so a secure connection between the MySQL client and server is recommended to prevent password exposure.
- The server-side authentication\_ldap\_sasl plugin performs SASL-based LDAP authentication. For connections by accounts that use this plugin, client programs use the clientside authentication\_ldap\_sasl\_client plugin. The client-side and server-side SASL LDAP plugins use SASL messages for secure transmission of credentials within the LDAP protocol, to avoid sending the cleartext password between the MySQL client and server.

![](_page_64_Picture_7.jpeg)

#### **Note**

On Microsoft Windows, the server plugin for SASL-based LDAP authentication is not supported, but the client plugin is supported. On other platforms, both the server and client plugins are supported.

The server-side LDAP authentication plugins are included only in MySQL Enterprise Edition. They are not included in MySQL community distributions. The client-side SASL LDAP plugin is included in all distributions, including community distributions, and, as mentioned previously, the client-side mysql\_clear\_password plugin is built into the libmysqlclient client library, which also is included in all distributions. This enables clients from any distribution to connect to a server that has the appropriate server-side plugin loaded.

The following sections provide installation and usage information specific to LDAP pluggable authentication:

- [Prerequisites for LDAP Pluggable Authentication](#page-65-0)
- [How LDAP Authentication of MySQL Users Works](#page-65-1)
- [Installing LDAP Pluggable Authentication](#page-66-0)
- [Uninstalling LDAP Pluggable Authentication](#page-68-0)
- [LDAP Pluggable Authentication and ldap.conf](#page-68-1)
- [Using LDAP Pluggable Authentication](#page-69-0)
- [Simple LDAP Authentication \(Without Proxying\)](#page-70-0)
- [SASL-Based LDAP Authentication \(Without Proxying\)](#page-71-0)
- [LDAP Authentication with Proxying](#page-72-0)
- [LDAP Authentication Group Preference and Mapping Specification](#page-74-0)
- [LDAP Authentication User DN Suffixes](#page-75-0)

- [LDAP Authentication Methods](#page-76-0)
- [The GSSAPI/Kerberos Authentication Method](#page-76-1)
- [LDAP Search Referral](#page-82-0)

For general information about pluggable authentication in MySQL, see Section 8.2.17, "Pluggable Authentication". For information about the mysql\_clear\_password plugin, see [Section 8.4.1.4,](#page-47-0) ["Client-Side Cleartext Pluggable Authentication".](#page-47-0) For proxy user information, see Section 8.2.19, "Proxy Users".

![](_page_65_Picture_5.jpeg)

## **Note**

If your system supports PAM and permits LDAP as a PAM authentication method, another way to use LDAP for MySQL user authentication is to use the server-side authentication\_pam plugin. See [Section 8.4.1.5, "PAM](#page-48-0) [Pluggable Authentication"](#page-48-0).

# <span id="page-65-0"></span>**Prerequisites for LDAP Pluggable Authentication**

To use LDAP pluggable authentication for MySQL, these prerequisites must be satisfied:

- An LDAP server must be available for the LDAP authentication plugins to communicate with.
- LDAP users to be authenticated by MySQL must be present in the directory managed by the LDAP server.
- An LDAP client library must be available on systems where the server-side authentication\_ldap\_sasl or authentication\_ldap\_simple plugin is used. Currently, supported libraries are the Windows native LDAP library, or the OpenLDAP library on non-Windows systems.
- To use SASL-based LDAP authentication:
  - The LDAP server must be configured to communicate with a SASL server.
  - A SASL client library must be available on systems where the client-side authentication\_ldap\_sasl\_client plugin is used. Currently, the only supported library is the Cyrus SASL library.
  - To use a particular SASL authentication method, any other services required by that method must be available. For example, to use GSSAPI/Kerberos, a GSSAPI library and Kerberos services must be available.

## <span id="page-65-1"></span>**How LDAP Authentication of MySQL Users Works**

This section provides an overview of how MySQL and LDAP work together to authenticate MySQL users. For examples showing how to set up MySQL accounts to use specific LDAP authentication plugins, see [Using LDAP Pluggable Authentication](#page-69-0). For information about authentication methods available to the LDAP plugins, see [LDAP Authentication Methods](#page-76-0).

The client connects to the MySQL server, providing the MySQL client user name and a password:

- For simple LDAP authentication, the client-side and server-side plugins communicate the password as cleartext. A secure connection between the MySQL client and server is recommended to prevent password exposure.
- For SASL-based LDAP authentication, the client-side and server-side plugins avoid sending the cleartext password between the MySQL client and server. For example, the plugins might use SASL messages for secure transmission of credentials within the LDAP protocol. For the GSSAPI authentication method, the client-side and server-side plugins communicate securely using Kerberos without using LDAP messages directly.

If the client user name and host name match no MySQL account, the connection is rejected.

If there is a matching MySQL account, authentication against LDAP occurs. The LDAP server looks for an entry matching the user and authenticates the entry against the LDAP password:

- If the MySQL account names an LDAP user distinguished name (DN), LDAP authentication uses that value and the LDAP password provided by the client. (To associate an LDAP user DN with a MySQL account, include a BY clause that specifies an authentication string in the CREATE USER statement that creates the account.)
- If the MySQL account names no LDAP user DN, LDAP authentication uses the user name and LDAP password provided by the client. In this case, the authentication plugin first binds to the LDAP server using the root DN and password as credentials to find the user DN based on the client user name, then authenticates that user DN against the LDAP password. This bind using the root credentials fails if the root DN and password are set to incorrect values, or are empty (not set) and the LDAP server does not permit anonymous connections.

If the LDAP server finds no match or multiple matches, authentication fails and the client connection is rejected.

If the LDAP server finds a single match, LDAP authentication succeeds (assuming that the password is correct), the LDAP server returns the LDAP entry, and the authentication plugin determines the name of the authenticated user based on that entry:

- If the LDAP entry has a group attribute (by default, the cn attribute), the plugin returns its value as the authenticated user name.
- If the LDAP entry has no group attribute, the authentication plugin returns the client user name as the authenticated user name.

The MySQL server compares the client user name with the authenticated user name to determine whether proxying occurs for the client session:

- If the names are the same, no proxying occurs: The MySQL account matching the client user name is used for privilege checking.
- If the names differ, proxying occurs: MySQL looks for an account matching the authenticated user name. That account becomes the proxied user, which is used for privilege checking. The MySQL account that matched the client user name is treated as the external proxy user.

## <span id="page-66-0"></span>**Installing LDAP Pluggable Authentication**

This section describes how to install the server-side LDAP authentication plugins. For general information about installing plugins, see Section 7.6.1, "Installing and Uninstalling Plugins".

To be usable by the server, the plugin library files must be located in the MySQL plugin directory (the directory named by the plugin\_dir system variable). If necessary, configure the plugin directory location by setting the value of plugin\_dir at server startup.

The server-side plugin library file base names are authentication\_ldap\_simple and authentication\_ldap\_sasl. The file name suffix differs per platform (for example, .so for Unix and Unix-like systems, .dll for Windows).

![](_page_66_Picture_16.jpeg)

## **Note**

On Microsoft Windows, the server plugin for SASL-based LDAP authentication is not supported, but the client plugin is supported. On other platforms, both the server and client plugins are supported.

To load the plugins at server startup, use --plugin-load-add options to name the library files that contain them. With this plugin-loading method, the options must be given each time the server starts. Also, specify values for any plugin-provided system variables you wish to configure.

Each server-side LDAP plugin exposes a set of system variables that enable its operation to be configured. Setting most of these is optional, but you must set the variables that specify the LDAP server host (so the plugin knows where to connect) and base distinguished name for LDAP bind operations (to limit the scope of searches and obtain faster searches). For details about all LDAP system variables, see [Section 8.4.1.13, "Pluggable Authentication System Variables".](#page-107-0)

To load the plugins and set the LDAP server host and base distinguished name for LDAP bind operations, put lines such as these in your my.cnf file, adjusting the .so suffix for your platform as necessary:

```
[mysqld]
plugin-load-add=authentication_ldap_simple.so
authentication_ldap_simple_server_host=127.0.0.1
authentication_ldap_simple_bind_base_dn="dc=example,dc=com"
plugin-load-add=authentication_ldap_sasl.so
authentication_ldap_sasl_server_host=127.0.0.1
authentication_ldap_sasl_bind_base_dn="dc=example,dc=com"
```

After modifying my.cnf, restart the server to cause the new settings to take effect.

Alternatively, to load the plugins at runtime, use these statements, adjusting the .so suffix for your platform as necessary:

```
INSTALL PLUGIN authentication_ldap_simple
 SONAME 'authentication_ldap_simple.so';
INSTALL PLUGIN authentication_ldap_sasl
 SONAME 'authentication_ldap_sasl.so';
```

INSTALL PLUGIN loads the plugin immediately, and also registers it in the mysql.plugins system table to cause the server to load it for each subsequent normal startup without the need for - plugin-load-add.

After installing the plugins at runtime, the system variables that they expose become available and you can add settings for them to your my.cnf file to configure the plugins for subsequent restarts. For example:

```
[mysqld]
authentication_ldap_simple_server_host=127.0.0.1
authentication_ldap_simple_bind_base_dn="dc=example,dc=com"
authentication_ldap_sasl_server_host=127.0.0.1
authentication_ldap_sasl_bind_base_dn="dc=example,dc=com"
```

After modifying my.cnf, restart the server to cause the new settings to take effect.

To set and persist each value at runtime rather than at startup, use these statements:

```
SET PERSIST authentication_ldap_simple_server_host='127.0.0.1';
SET PERSIST authentication_ldap_simple_bind_base_dn='dc=example,dc=com';
SET PERSIST authentication_ldap_sasl_server_host='127.0.0.1';
SET PERSIST authentication_ldap_sasl_bind_base_dn='dc=example,dc=com';
```

SET PERSIST sets a value for the running MySQL instance. It also saves the value, causing it to carry over to subsequent server restarts. To change a value for the running MySQL instance without having it carry over to subsequent restarts, use the GLOBAL keyword rather than PERSIST. See Section 15.7.6.1, "SET Syntax for Variable Assignment".

To verify plugin installation, examine the Information Schema PLUGINS table or use the SHOW PLUGINS statement (see Section 7.6.2, "Obtaining Server Plugin Information"). For example:

```
mysql> SELECT PLUGIN_NAME, PLUGIN_STATUS
 FROM INFORMATION_SCHEMA.PLUGINS
 WHERE PLUGIN_NAME LIKE '%ldap%';
+----------------------------+---------------+
| PLUGIN_NAME | PLUGIN_STATUS |
+----------------------------+---------------+
| authentication_ldap_sasl | ACTIVE |
| authentication_ldap_simple | ACTIVE |
```

+----------------------------+---------------+

If a plugin fails to initialize, check the server error log for diagnostic messages.

To associate MySQL accounts with an LDAP plugin, see [Using LDAP Pluggable Authentication.](#page-69-0)

![](_page_68_Picture_4.jpeg)

#### **Additional Notes for SELinux**

On systems running EL6 or EL that have SELinux enabled, changes to the SELinux policy are required to enable the MySQL LDAP plugins to communicate with the LDAP service:

1. Create a file mysqlldap.te with these contents:

```
module mysqlldap 1.0;
require {
 type ldap_port_t;
 type mysqld_t;
 class tcp_socket name_connect;
}
#============= mysqld_t ==============
allow mysqld_t ldap_port_t:tcp_socket name_connect;
```

2. Compile the security policy module into a binary representation:

```
checkmodule -M -m mysqlldap.te -o mysqlldap.mod
```

3. Create an SELinux policy module package:

```
semodule_package -m mysqlldap.mod -o mysqlldap.pp
```

4. Install the module package:

```
semodule -i mysqlldap.pp
```

5. When the SELinux policy changes have been made, restart the MySQL server:

```
service mysqld restart
```

## <span id="page-68-0"></span>**Uninstalling LDAP Pluggable Authentication**

The method used to uninstall the LDAP authentication plugins depends on how you installed them:

- If you installed the plugins at server startup using --plugin-load-add options, restart the server without those options.
- If you installed the plugins at runtime using INSTALL PLUGIN, they remain installed across server restarts. To uninstall them, use UNINSTALL PLUGIN:

```
UNINSTALL PLUGIN authentication_ldap_simple;
UNINSTALL PLUGIN authentication_ldap_sasl;
```

In addition, remove from your my.cnf file any startup options that set LDAP plugin-related system variables. If you used SET PERSIST to persist LDAP system variables, use RESET PERSIST to remove the settings.

## <span id="page-68-1"></span>**LDAP Pluggable Authentication and ldap.conf**

For installations that use OpenLDAP, the ldap.conf file provides global defaults for LDAP clients. Options can be set in this file to affect LDAP clients, including the LDAP authentication plugins. OpenLDAP uses configuration options in this order of precedence:

- Configuration specified by the LDAP client.
- Configuration specified in the ldap.conf file. To disable use of this file, set the LDAPNOINIT environment variable.
- OpenLDAP library built-in defaults.

If the library defaults or ldap.conf values do not yield appropriate option values, an LDAP authentication plugin may be able to set related variables to affect the LDAP configuration directly. For example, LDAP plugins can override ldap.conf for parameters such as these:

- TLS configuration: System variables are available to enable TLS and control CA configuration, such as [authentication\\_ldap\\_simple\\_tls](#page-124-0) and [authentication\\_ldap\\_simple\\_ca\\_path](#page-119-0) for simple LDAP authentication, and [authentication\\_ldap\\_sasl\\_tls](#page-116-0) and [authentication\\_ldap\\_sasl\\_ca\\_path](#page-112-0) for SASL LDAP authentication.
- LDAP referral. See [LDAP Search Referral.](#page-82-0)

For more information about ldap.conf consult the ldap.conf(5) man page.

## <span id="page-69-0"></span>**Using LDAP Pluggable Authentication**

This section describes how to enable MySQL accounts to connect to the MySQL server using LDAP pluggable authentication. It is assumed that the server is running with the appropriate server-side plugins enabled, as described in [Installing LDAP Pluggable Authentication](#page-66-0), and that the appropriate client-side plugins are available on the client host.

This section does not describe LDAP configuration or administration. You are assumed to be familiar with those topics.

The two server-side LDAP plugins each work with a specific client-side plugin:

- The server-side authentication\_ldap\_simple plugin performs simple LDAP authentication. For connections by accounts that use this plugin, client programs use the client-side mysql\_clear\_password plugin, which sends the password to the server as cleartext. No password hashing or encryption is used, so a secure connection between the MySQL client and server is recommended to prevent password exposure.
- The server-side authentication\_ldap\_sasl plugin performs SASL-based LDAP authentication. For connections by accounts that use this plugin, client programs use the clientside authentication\_ldap\_sasl\_client plugin. The client-side and server-side SASL LDAP plugins use SASL messages for secure transmission of credentials within the LDAP protocol, to avoid sending the cleartext password between the MySQL client and server.

Overall requirements for LDAP authentication of MySQL users:

- There must be an LDAP directory entry for each user to be authenticated.
- There must be a MySQL user account that specifies a server-side LDAP authentication plugin and optionally names the associated LDAP user distinguished name (DN). (To associate an LDAP user DN with a MySQL account, include a BY clause in the CREATE USER statement that creates the account.) If an account names no LDAP string, LDAP authentication uses the user name specified by the client to find the LDAP entry.
- Client programs connect using the connection method appropriate for the server-side authentication plugin the MySQL account uses. For LDAP authentication, connections require the MySQL user name and LDAP password. In addition, for accounts that use the server-side authentication\_ldap\_simple plugin, invoke client programs with the --enable-cleartextplugin option to enable the client-side mysql\_clear\_password plugin.

The instructions here assume the following scenario:

- MySQL users betsy and boris authenticate to the LDAP entries for betsy\_ldap and boris\_ldap, respectively. (It is not necessary that the MySQL and LDAP user names differ. The use of different names in this discussion helps clarify whether an operation context is MySQL or LDAP.)
- LDAP entries use the uid attribute to specify user names. This may vary depending on LDAP server. Some LDAP servers use the cn attribute for user names rather than uid. To change the attribute, modify the [authentication\\_ldap\\_simple\\_user\\_search\\_attr](#page-124-1) or [authentication\\_ldap\\_sasl\\_user\\_search\\_attr](#page-117-0) system variable appropriately.
- These LDAP entries are available in the directory managed by the LDAP server, to provide distinguished name values that uniquely identify each user:

```
uid=betsy_ldap,ou=People,dc=example,dc=com
uid=boris_ldap,ou=People,dc=example,dc=com
```

• CREATE USER statements that create MySQL accounts name an LDAP user in the BY clause, to indicate which LDAP entry the MySQL account authenticates against.

The instructions for setting up an account that uses LDAP authentication depend on which server-side LDAP plugin is used. The following sections describe several usage scenarios.

## <span id="page-70-0"></span>**Simple LDAP Authentication (Without Proxying)**

The procedure outlined in this section requires that

[authentication\\_ldap\\_simple\\_group\\_search\\_attr](#page-119-1) be set to an empty string, like this:

```
SET GLOBAL.authentication_ldap_simple_group_search_attr='';
```

Otherwise, proxying is used by default.

To set up a MySQL account for simple LDAP authentication, use a CREATE USER statement to specify the authentication\_ldap\_simple plugin, optionally including the LDAP user distinguished name (DN), as shown here:

```
CREATE USER user
 IDENTIFIED WITH authentication_ldap_simple
 [BY 'LDAP user DN'];
```

Suppose that MySQL user betsy has this entry in the LDAP directory:

```
uid=betsy_ldap,ou=People,dc=example,dc=com
```

Then the statement to create the MySQL account for betsy looks like this:

```
CREATE USER 'betsy'@'localhost'
 IDENTIFIED WITH authentication_ldap_simple
 AS 'uid=betsy_ldap,ou=People,dc=example,dc=com';
```

The authentication string specified in the BY clause does not include the LDAP password. That must be provided by the client user at connect time.

Clients connect to the MySQL server by providing the MySQL user name and LDAP password, and by enabling the client-side mysql\_clear\_password plugin:

```
$> mysql --user=betsy --password --enable-cleartext-plugin
Enter password: betsy_ldap_password
```

![](_page_70_Picture_21.jpeg)

## **Note**

The client-side mysql\_clear\_password authentication plugin leaves the password untouched, so client programs send it to the MySQL server as cleartext. This enables the password to be passed as is to the LDAP server. A cleartext password is necessary to use the server-side LDAP library without SASL, but may be a security problem in some configurations. These measures minimize the risk:

- To make inadvertent use of the mysql\_clear\_password plugin less likely, MySQL clients must explicitly enable it (for example, with the --enablecleartext-plugin option). See [Section 8.4.1.4, "Client-Side Cleartext](#page-47-0) [Pluggable Authentication"](#page-47-0).
- To avoid password exposure with the mysql\_clear\_password plugin enabled, MySQL clients should connect to the MySQL server using an encrypted connection. See [Section 8.3.1, "Configuring MySQL to Use](#page-8-0) [Encrypted Connections".](#page-8-0)

The authentication process occurs as follows:

- 1. The client-side plugin sends betsy and betsy\_password as the client user name and LDAP password to the MySQL server.
- 2. The connection attempt matches the 'betsy'@'localhost' account. The server-side LDAP plugin finds that this account has an authentication string of 'uid=betsy\_ldap,ou=People,dc=example,dc=com' to name the LDAP user DN. The plugin sends this string and the LDAP password to the LDAP server.
- 3. The LDAP server finds the LDAP entry for betsy\_ldap and the password matches, so LDAP authentication succeeds.
- 4. The LDAP entry has no group attribute, so the server-side plugin returns the client user name (betsy) as the authenticated user. This is the same user name supplied by the client, so no proxying occurs and the client session uses the 'betsy'@'localhost' account for privilege checking.

Had the CREATE USER statement contained no BY clause to specify the betsy\_ldap LDAP distinguished name, authentication attempts would use the user name provided by the client (in this case, betsy). In the absence of an LDAP entry for betsy, authentication would fail.

# <span id="page-71-0"></span>**SASL-Based LDAP Authentication (Without Proxying)**

The procedure outlined in this section requires that

[authentication\\_ldap\\_sasl\\_group\\_search\\_attr](#page-112-1) be set to an empty string, like this:

```
SET GLOBAL.authentication_ldap_sasl_group_search_attr='';
```

Otherwise, proxying is used by default.

To set up a MySQL account for SALS LDAP authentication, use a CREATE USER statement to specify the authentication\_ldap\_sasl plugin, optionally including the LDAP user distinguished name (DN), as shown here:

```
CREATE USER user
 IDENTIFIED WITH authentication_ldap_sasl
 [BY 'LDAP user DN'];
```

Suppose that MySQL user boris has this entry in the LDAP directory:

```
uid=boris_ldap,ou=People,dc=example,dc=com
```

Then the statement to create the MySQL account for boris looks like this:

```
CREATE USER 'boris'@'localhost'
 IDENTIFIED WITH authentication_ldap_sasl
 AS 'uid=boris_ldap,ou=People,dc=example,dc=com';
```

The authentication string specified in the BY clause does not include the LDAP password. That must be provided by the client user at connect time.

Clients connect to the MySQL server by providing the MySQL user name and LDAP password:

```
$> mysql --user=boris --password
Enter password: boris_ldap_password
```

For the server-side authentication\_ldap\_sasl plugin, clients use the client-side authentication\_ldap\_sasl\_client plugin. If a client program does not find the client-side plugin, specify a --plugin-dir option that names the directory where the plugin library file is installed.

The authentication process for boris is similar to that previously described for betsy with simple LDAP authentication, except that the client-side and server-side SASL LDAP plugins use SASL messages for secure transmission of credentials within the LDAP protocol, to avoid sending the cleartext password between the MySQL client and server.

# <span id="page-72-0"></span>**LDAP Authentication with Proxying**

LDAP authentication plugins support proxying, enabling a user to connect to the MySQL server as one user but assume the privileges of a different user. This section describes basic LDAP plugin proxy support. The LDAP plugins also support specification of group preference and proxy user mapping; see [LDAP Authentication Group Preference and Mapping Specification.](#page-74-0)

The proxying implementation described here is based on use of LDAP group attribute values to map connecting MySQL users who authenticate using LDAP onto other MySQL accounts that define different sets of privileges. Users do not connect directly through the accounts that define the privileges. Instead, they connect through a default proxy account authenticated with LDAP, such that all external logins are mapped to the proxied MySQL accounts that hold the privileges. Any user who connects using the proxy account is mapped to one of those proxied MySQL accounts, the privileges for which determine the database operations permitted to the external user.

The instructions here assume the following scenario:

- LDAP entries use the uid and cn attributes to specify user name and group values, respectively. To use different user and group attribute names, set the appropriate plugin-specific system variables:
  - For the authentication\_ldap\_simple plugin: Set [authentication\\_ldap\\_simple\\_user\\_search\\_attr](#page-124-1) and [authentication\\_ldap\\_simple\\_group\\_search\\_attr](#page-119-1).
  - For the authentication\_ldap\_sasl plugin: Set [authentication\\_ldap\\_sasl\\_user\\_search\\_attr](#page-117-0) and [authentication\\_ldap\\_sasl\\_group\\_search\\_attr](#page-112-1).
- These LDAP entries are available in the directory managed by the LDAP server, to provide distinguished name values that uniquely identify each user:

```
uid=basha,ou=People,dc=example,dc=com,cn=accounting
uid=basil,ou=People,dc=example,dc=com,cn=front_office
```

At connect time, the group attribute values become the authenticated user names, so they name the accounting and front\_office proxied accounts.

• The examples assume use of SASL LDAP authentication. Make the appropriate adjustments for simple LDAP authentication.

Create the default proxy MySQL account:

```
CREATE USER ''@'%'
 IDENTIFIED WITH authentication_ldap_sasl;
```

The proxy account definition has no AS 'auth\_string' clause to name an LDAP user DN. Thus:

• When a client connects, the client user name becomes the LDAP user name to search for.

• The matching LDAP entry is expected to include a group attribute naming the proxied MySQL account that defines the privileges the client should have.

![](_page_73_Picture_2.jpeg)

## **Note**

If your MySQL installation has anonymous users, they might conflict with the default proxy user. For more information about this issue, and ways of dealing with it, see Default Proxy User and Anonymous User Conflicts.

Create the proxied accounts and grant to each one the privileges it should have:

```
CREATE USER 'accounting'@'localhost'
 IDENTIFIED WITH mysql_no_login;
CREATE USER 'front_office'@'localhost'
 IDENTIFIED WITH mysql_no_login;
GRANT ALL PRIVILEGES
 ON accountingdb.*
 TO 'accounting'@'localhost';
GRANT ALL PRIVILEGES
 ON frontdb.*
 TO 'front_office'@'localhost';
```

The proxied accounts use the mysql\_no\_login authentication plugin to prevent clients from using the accounts to log in directly to the MySQL server. Instead, users who authenticate using LDAP are expected to use the default ''@'%' proxy account. (This assumes that the mysql\_no\_login plugin is installed. For instructions, see [Section 8.4.1.9, "No-Login Pluggable Authentication".](#page-94-0)) For alternative methods of protecting proxied accounts against direct use, see Preventing Direct Login to Proxied Accounts.

Grant to the proxy account the PROXY privilege for each proxied account:

```
GRANT PROXY
 ON 'accounting'@'localhost'
 TO ''@'%';
GRANT PROXY
 ON 'front_office'@'localhost'
 TO ''@'%';
```

Use the mysql command-line client to connect to the MySQL server as basha.

```
$> mysql --user=basha --password
Enter password: basha_password (basha LDAP password)
```

Authentication occurs as follows:

- 1. The server authenticates the connection using the default ''@'%' proxy account, for client user basha.
- 2. The matching LDAP entry is:

```
uid=basha,ou=People,dc=example,dc=com,cn=accounting
```

- 3. The matching LDAP entry has group attribute cn=accounting, so accounting becomes the authenticated proxied user.
- 4. The authenticated user differs from the client user name basha, with the result that basha is treated as a proxy for accounting, and basha assumes the privileges of the proxied accounting account. The following query returns output as shown:

```
mysql> SELECT USER(), CURRENT_USER(), @@proxy_user;
+-----------------+----------------------+--------------+
| USER() | CURRENT_USER() | @@proxy_user |
+-----------------+----------------------+--------------+
| basha@localhost | accounting@localhost | ''@'%' |
+-----------------+----------------------+--------------+
```

This demonstrates that basha uses the privileges granted to the proxied accounting MySQL account, and that proxying occurs through the default proxy user account.

Now connect as basil instead:

```
$> mysql --user=basil --password
Enter password: basil_password (basil LDAP password)
```

The authentication process for basil is similar to that previously described for basha:

- 1. The server authenticates the connection using the default ''@'%' proxy account, for client user basil.
- 2. The matching LDAP entry is:

```
uid=basil,ou=People,dc=example,dc=com,cn=front_office
```

- 3. The matching LDAP entry has group attribute cn=front\_office, so front\_office becomes the authenticated proxied user.
- 4. The authenticated user differs from the client user name basil, with the result that basil is treated as a proxy for front\_office, and basil assumes the privileges of the proxied front\_office account. The following query returns output as shown:

```
mysql> SELECT USER(), CURRENT_USER(), @@proxy_user;
+-----------------+------------------------+--------------+
| USER() | CURRENT_USER() | @@proxy_user |
+-----------------+------------------------+--------------+
| basil@localhost | front_office@localhost | ''@'%' |
+-----------------+------------------------+--------------+
```

This demonstrates that basil uses the privileges granted to the proxied front\_office MySQL account, and that proxying occurs through the default proxy user account.

## <span id="page-74-0"></span>**LDAP Authentication Group Preference and Mapping Specification**

As described in [LDAP Authentication with Proxying,](#page-72-0) basic LDAP authentication proxying works by the principle that the plugin uses the first group name returned by the LDAP server as the MySQL proxied user account name. This simple capability does not enable specifying any preference about which group name to use if the LDAP server returns multiple group names, or specifying any name other than the group name as the proxied user name.

As of MySQL 8.0.14, for MySQL accounts that use LDAP authentication, the authentication string can specify the following information to enable greater proxying flexibility:

- A list of groups in preference order, such that the plugin uses the first group name in the list that matches a group returned by the LDAP server.
- A mapping from group names to proxied user names, such that a group name when matched can provide a specified name to use as the proxied user. This provides an alternative to using the group name as the proxied user.

Consider the following MySQL proxy account definition:

```
CREATE USER ''@'%'
 IDENTIFIED WITH authentication_ldap_sasl
 AS '+ou=People,dc=example,dc=com#grp1=usera,grp2,grp3=userc';
```

The authentication string has a user DN suffix ou=People,dc=example,dc=com prefixed by the + character. Thus, as described in [LDAP Authentication User DN Suffixes,](#page-75-0) the full user DN is constructed from the user DN suffix as specified, plus the client user name as the uid attribute.

The remaining part of the authentication string begins with #, which signifies the beginning of group preference and mapping information. This part of the authentication string lists group names in the order grp1, grp2, grp3. The LDAP plugin compares that list with the set of group names returned by the LDAP server, looking in list order for a match against the returned names. The plugin uses the first match, or if there is no match, authentication fails.

Suppose that the LDAP server returns groups grp3, grp2, and grp7. The LDAP plugin uses grp2 because it is the first group in the authentication string that matches, even though it is not the first group returned by the LDAP server. If the LDAP server returns grp4, grp2, and grp1, the plugin uses grp1 even though grp2 also matches. grp1 has a precedence higher than grp2 because it is listed earlier in the authentication string.

Assuming that the plugin finds a group name match, it performs mapping from that group name to the MySQL proxied user name, if there is one. For the example proxy account, mapping occurs as follows:

- If the matching group name is grp1 or grp3, those are associated in the authentication string with user names usera and userc, respectively. The plugin uses the corresponding associated user name as the proxied user name.
- If the matching group name is grp2, there is no associated user name in the authentication string. The plugin uses grp2 as the proxied user name.

If the LDAP server returns a group in DN format, the LDAP plugin parses the group DN to extract the group name from it.

To specify LDAP group preference and mapping information, these principles apply:

- Begin the group preference and mapping part of the authentication string with a # prefix character.
- The group preference and mapping specification is a list of one or more items, separated by commas. Each item has the form group\_name=user\_name or group\_name. Items should be listed in group name preference order. For a group name selected by the plugin as a match from set of group names returned by the LDAP server, the two syntaxes differ in effect as follows:
  - For an item specified as group\_name=user\_name (with a user name), the group name maps to the user name, which is used as the MySQL proxied user name.
  - For an item specified as group\_name (with no user name), the group name is used as the MySQL proxied user name.
- To quote a group or user name that contains special characters such as space, surround it by double quote (") characters. For example, if an item has group and user names of my group name and my user name, it must be written in a group mapping using quotes:

```
"my group name"="my user name"
```

If an item has group and user names of my\_group\_name and my\_user\_name (which contain no special characters), it may but need not be written using quotes. Any of the following are valid:

```
my_group_name=my_user_name
my_group_name="my_user_name"
"my_group_name"=my_user_name
"my_group_name"="my_user_name"
```

- To escape a character, precede it by a backslash (\). This is useful particularly to include a literal double quote or backslash, which are otherwise not included literally.
- A user DN need not be present in the authentication string, but if present, it must precede the group preference and mapping part. A user DN can be given as a full user DN, or as a user DN suffix with a + prefix character. (See [LDAP Authentication User DN Suffixes.](#page-75-0))

# <span id="page-75-0"></span>**LDAP Authentication User DN Suffixes**

LDAP authentication plugins permit the authentication string that provides user DN information to begin with a + prefix character:

• In the absence of a + character, the authentication string value is treated as is without modification.

• If the authentication string begins with +, the plugin constructs the full user DN value from the user name sent by the client, together with the DN specified in the authentication string (with the + removed). In the constructed DN, the client user name becomes the value of the attribute that specifies LDAP user names. This is uid by default; to change the attribute, modify the appropriate system variable ([authentication\\_ldap\\_simple\\_user\\_search\\_attr](#page-124-1) or [authentication\\_ldap\\_sasl\\_user\\_search\\_attr](#page-117-0)). The authentication string is stored as given in the mysql.user system table, with the full user DN constructed on the fly before authentication.

This account authentication string does not have + at the beginning, so it is taken as the full user DN:

```
CREATE USER 'baldwin'
 IDENTIFIED WITH authentication_ldap_simple
 AS 'uid=admin,ou=People,dc=example,dc=com';
```

The client connects with the user name specified in the account (baldwin). In this case, that name is not used because the authentication string has no prefix and thus fully specifies the user DN.

This account authentication string does have + at the beginning, so it is taken as just part of the user DN:

```
CREATE USER 'accounting'
 IDENTIFIED WITH authentication_ldap_simple
 AS '+ou=People,dc=example,dc=com';
```

The client connects with the user name specified in the account (accounting), which in this case is used as the uid attribute together with the authentication string to construct the user DN: uid=accounting,ou=People,dc=example,dc=com

The accounts in the preceding examples have a nonempty user name, so the client always connects to the MySQL server using the same name as specified in the account definition. If an account has an empty user name, such as the default anonymous ''@'%' proxy account described in [LDAP](#page-72-0) [Authentication with Proxying,](#page-72-0) clients might connect to the MySQL server with varying user names. But the principle is the same: If the authentication string begins with +, the plugin uses the user name sent by the client together with the authentication string to construct the user DN.

# <span id="page-76-0"></span>**LDAP Authentication Methods**

The LDAP authentication plugins use a configurable authentication method. The appropriate system variable and available method choices are plugin-specific:

- For the authentication\_ldap\_simple plugin: Set the [authentication\\_ldap\\_simple\\_auth\\_method\\_name](#page-117-1) system variable to configure the method. The permitted choices are SIMPLE and AD-FOREST.
- For the authentication\_ldap\_sasl plugin: Set the [authentication\\_ldap\\_sasl\\_auth\\_method\\_name](#page-109-0) system variable to configure the method. The permitted choices are SCRAM-SHA-1, SCRAM-SHA-256, and GSSAPI. (To determine which SASL LDAP methods are actually available on the host system, check the value of the Authentication\_ldap\_sasl\_supported\_methods status variable.)

See the system variable descriptions for information about each permitted method. Also, depending on the method, additional configuration may be needed, as described in the following sections.

## <span id="page-76-1"></span>**The GSSAPI/Kerberos Authentication Method**

Generic Security Service Application Program Interface (GSSAPI) is a security abstraction interface. Kerberos is an instance of a specific security protocol that can be used through that abstract interface. Using GSSAPI, applications authenticate to Kerberos to obtain service credentials, then use those credentials in turn to enable secure access to other services.

One such service is LDAP, which is used by the client-side and server-side SASL LDAP authentication plugins. When the [authentication\\_ldap\\_sasl\\_auth\\_method\\_name](#page-109-0) system variable is set to GSSAPI, these plugins use the GSSAPI/Kerberos authentication method. In this case, the plugins

communicate securely using Kerberos without using LDAP messages directly. The server-side plugin then communicates with the LDAP server to interpret LDAP authentication messages and retrieve LDAP groups.

GSSAPI/Kerberos is supported as an LDAP authentication method for MySQL servers and clients on Linux. It is useful in Linux environments where applications have access to LDAP through Microsoft Active Directory, which has Kerberos enabled by default.

The following discussion provides information about the configuration requirements for using the GSSAPI method. Familiarity is assumed with Kerberos concepts and operation. The following list briefly defines several common Kerberos terms. You may also find the Glossary section of [RFC 4120](https://tools.ietf.org/html/rfc4120) helpful.

- Principal: A named entity, such as a user or server.
- KDC: The key distribution center, comprising the AS and TGS:
  - AS: The authentication server; provides the initial ticket-granting ticket needed to obtain additional tickets.
  - TGS: The ticket-granting server; provides additional tickets to Kerberos clients that possess a valid TGT.
- TGT: The ticket-granting ticket; presented to the TGS to obtain service tickets for service access.

LDAP authentication using Kerberos requires both a KDC server and an LDAP server. This requirement can be satisfied in different ways:

- Active Directory includes both servers, with Kerberos authentication enabled by default in the Active Directory LDAP server.
- OpenLDAP provides an LDAP server, but a separate KDC server may be needed, with additional Kerberos setup required.

Kerberos must also be available on the client host. A client contacts the AS using a password to obtain a TGT. The client then uses the TGT to obtain access from the TGS to other services, such as LDAP.

The following sections discuss the configuration steps to use GSSAPI/Kerberos for SASL LDAP authentication in MySQL:

- [Verify Kerberos and LDAP Availability](#page-77-0)
- [Configure the Server-Side SASL LDAP Authentication Plugin for GSSAPI/Kerberos](#page-78-0)
- [Create a MySQL Account That Uses GSSAPI/Kerberos for LDAP Authentication](#page-79-0)
- [Use the MySQL Account to Connect to the MySQL Server](#page-80-0)
- [Client Configuration Parameters for LDAP Authentication](#page-82-1)

## <span id="page-77-0"></span>**Verify Kerberos and LDAP Availability**

The following example shows how to test availability of Kerberos in Active Directory. The example makes these assumptions:

- Active Directory is running on the host named ldap\_auth.example.com with IP address 198.51.100.10.
- MySQL-related Kerberos authentication and LDAP lookups use the MYSQL.LOCAL domain.
- A principal named bredon@MYSQL.LOCAL is registered with the KDC. (In later discussion, this principal name is also associated with the MySQL account that authenticates to the MySQL server using GSSAPI/Kerberos.)

With those assumptions satisfied, follow this procedure:

1. Verify that the Kerberos library is installed and configured correctly in the operating system. For example, to configure a MYSQL.LOCAL domain for use during MySQL authentication, the /etc/ krb5.conf Kerberos configuration file should contain something like this:

```
[realms]
 MYSQL.LOCAL = {
 kdc = ldap_auth.example.com
 admin_server = ldap_auth.example.com
 default_domain = MYSQL.LOCAL
 }
```

2. You may need to add an entry to /etc/hosts for the server host:

```
198.51.100.10 ldap_auth ldap_auth.example.com
```

- 3. Check whether Kerberos authentication works correctly:
  - a. Use kinit to authenticate to Kerberos:

```
$> kinit bredon@MYSQL.LOCAL
Password for bredon@MYSQL.LOCAL: (enter password here)
```

The command authenticates for the Kerberos principal named bredon@MYSQL.LOCAL. Enter the principal's password when the command prompts for it. The KDC returns a TGT that is cached on the client side for use by other Kerberos-aware applications.

b. Use klist to check whether the TGT was obtained correctly. The output should be similar to this:

```
$> klist
Ticket cache: FILE:/tmp/krb5cc_244306
Default principal: bredon@MYSQL.LOCAL
Valid starting Expires Service principal
03/23/2021 08:18:33 03/23/2021 18:18:33 krbtgt/MYSQL.LOCAL@MYSQL.LOCAL
```

4. Check whether ldapsearch works with the Kerberos TGT using this command, which searches for users in the MYSQL.LOCAL domain:

```
ldapsearch -h 198.51.100.10 -Y GSSAPI -b "dc=MYSQL,dc=LOCAL"
```

#### <span id="page-78-0"></span>**Configure the Server-Side SASL LDAP Authentication Plugin for GSSAPI/Kerberos**

Assuming that the LDAP server is accessible through Kerberos as just described, configure the serverside SASL LDAP authentication plugin to use the GSSAPI/Kerberos authentication method. (For general LDAP plugin installation information, see [Installing LDAP Pluggable Authentication](#page-66-0).) Here is an example of plugin-related settings the server my.cnf file might contain:

```
[mysqld]
plugin-load-add=authentication_ldap_sasl.so
authentication_ldap_sasl_auth_method_name="GSSAPI"
authentication_ldap_sasl_server_host=198.51.100.10
authentication_ldap_sasl_server_port=389
authentication_ldap_sasl_bind_root_dn="cn=admin,cn=users,dc=MYSQL,dc=LOCAL"
authentication_ldap_sasl_bind_root_pwd="password"
authentication_ldap_sasl_bind_base_dn="cn=users,dc=MYSQL,dc=LOCAL"
authentication_ldap_sasl_user_search_attr="sAMAccountName"
```

Those option file settings configure the SASL LDAP plugin as follows:

- The --plugin-load-add option loads the plugin (adjust the .so suffix for your platform as necessary). If you loaded the plugin previously using an INSTALL PLUGIN statement, this option is unnecessary.
- [authentication\\_ldap\\_sasl\\_auth\\_method\\_name](#page-109-0) must be set to GSSAPI to use GSSAPI/ Kerberos as the SASL LDAP authentication method.

- [authentication\\_ldap\\_sasl\\_server\\_host](#page-115-0) and [authentication\\_ldap\\_sasl\\_server\\_port](#page-116-1) indicate the IP address and port number of the Active Directory server host for authentication.
- [authentication\\_ldap\\_sasl\\_bind\\_root\\_dn](#page-111-0) and [authentication\\_ldap\\_sasl\\_bind\\_root\\_pwd](#page-112-2) configure the root DN and password for group search capability. This capability is required, but users may not have privileges to search. In such cases, it is necessary to provide root DN information:
  - In the DN option value, admin should be the name of an administrative LDAP account that has privileges to perform user searches.
  - In the password option value, password should be the admin account password.
- [authentication\\_ldap\\_sasl\\_bind\\_base\\_dn](#page-110-0) indicates the user DN base path, so that searches look for users in the MYSQL.LOCAL domain.
- [authentication\\_ldap\\_sasl\\_user\\_search\\_attr](#page-117-0) specifies a standard Active Directory search attribute, sAMAccountName. This attribute is used in searches to match logon names; attribute values are not the same as the user DN values.

### <span id="page-79-0"></span>**Create a MySQL Account That Uses GSSAPI/Kerberos for LDAP Authentication**

MySQL authentication using the SASL LDAP authentication plugin with the GSSAPI/Kerberos method is based on a user that is a Kerberos principal. The following discussion uses a principal named bredon@MYSQL.LOCAL as this user, which must be registered in several places:

- The Kerberos administrator should register the user name as a Kerberos principal. This name should include a domain name. Clients use the principal name and password to authenticate with Kerberos and obtain a TGT.
- The LDAP administrator should register the user name in an LDAP entry. For example:

uid=bredon,dc=MYSQL,dc=LOCAL

![](_page_79_Picture_12.jpeg)

## **Note**

In Active Directory (which uses Kerberos as the default authentication method), creating a user creates both the Kerberos principal and the LDAP entry.

• The MySQL DBA should create an account that has the Kerberos principal name as the user name and that authenticates using the SASL LDAP plugin.

Assume that the Kerberos principal and LDAP entry have been registered by the appropriate service administrators, and that, as previously described in [Installing LDAP Pluggable Authentication,](#page-66-0) and [Configure the Server-Side SASL LDAP Authentication Plugin for GSSAPI/Kerberos](#page-78-0), the MySQL server has been started with appropriate configuration settings for the server-side SASL LDAP plugin. The MySQL DBA then creates a MySQL account that corresponds to the Kerberos principal name, including the domain name.

![](_page_79_Picture_17.jpeg)

## **Note**

The SASL LDAP plugin uses a constant user DN for Kerberos authentication and ignores any user DN configured from MySQL. This has certain implications:

- For any MySQL account that uses GSSAPI/Kerberos authentication, the authentication string in CREATE USER or ALTER USER statements should contain no user DN because it has no effect.
- Because the authentication string contains no user DN, it should contain group mapping information, to enable the user to be handled as a proxy user

that is mapped onto the desired proxied user. For information about proxying with the LDAP authentication plugin, see [LDAP Authentication with Proxying](#page-72-0).

The following statements create a proxy user named bredon@MYSQL.LOCAL that assumes the privileges of the proxied user named proxied\_krb\_usr. Other GSSAPI/Kerberos users that should have the same privileges can similarly be created as proxy users for the same proxied user.

```
-- create proxy account
CREATE USER 'bredon@MYSQL.LOCAL'
 IDENTIFIED WITH authentication_ldap_sasl
 BY '#krb_grp=proxied_krb_user';
-- create proxied account and grant its privileges;
-- use mysql_no_login plugin to prevent direct login
CREATE USER 'proxied_krb_user'
 IDENTIFIED WITH mysql_no_login;
GRANT ALL
 ON krb_user_db.*
 TO 'proxied_krb_user';
-- grant to proxy account the
-- PROXY privilege for proxied account
GRANT PROXY
 ON 'proxied_krb_user'
 TO 'bredon@MYSQL.LOCAL';
```

Observe closely the quoting for the proxy account name in the first CREATE USER statement and the GRANT PROXY statement:

- For most MySQL accounts, the user and host are separate parts of the account name, and thus are quoted separately as 'user\_name'@'host\_name'.
- For LDAP Kerberos authentication, the user part of the account name includes the principal domain, so 'bredon@MYSQL.LOCAL' is quoted as a single value. Because no host part is given, the full MySQL account name uses the default of '%' as the host part: 'bredon@MYSQL.LOCAL'@'%'

![](_page_80_Picture_7.jpeg)

## **Note**

When creating an account that authenticates using the authentication\_ldap\_sasl SASL LDAP authentication plugin with the GSSAPI/Kerberos authentication method, the CREATE USER statement includes the realm as part of the user name. This differs from creating accounts that use the authentication\_kerberos Kerberos plugin. For such accounts, the CREATE USER statement does not include the realm as part of the user name. Instead, specify the realm as the authentication string in the BY clause. See [Create a MySQL Account That Uses Kerberos Authentication](#page-88-0).

The proxied account uses the mysql\_no\_login authentication plugin to prevent clients from using the account to log in directly to the MySQL server. Instead, it is expected that users who authenticate using LDAP use the bredon@MYSQL.LOCAL proxy account. (This assumes that the mysql\_no\_login plugin is installed. For instructions, see [Section 8.4.1.9, "No-Login Pluggable Authentication"](#page-94-0).) For alternative methods of protecting proxied accounts against direct use, see Preventing Direct Login to Proxied Accounts.

#### <span id="page-80-0"></span>**Use the MySQL Account to Connect to the MySQL Server**

After a MySQL account that authenticates using GSSAPI/Kerberos has been set up, clients can use it to connect to the MySQL server. Kerberos authentication can take place either prior to or at the time of MySQL client program invocation:

• Prior to invoking the MySQL client program, the client user can obtain a TGT from the KDC independently of MySQL. For example, the client user can use kinit to authenticate to Kerberos by providing a Kerberos principal name and the principal password:

```
$> kinit bredon@MYSQL.LOCAL
Password for bredon@MYSQL.LOCAL: (enter password here)
```

The resulting TGT is cached and becomes available for use by other Kerberos-aware applications, such as programs that use the client-side SASL LDAP authentication plugin. In this case, the MySQL client program authenticates to the MySQL server using the TGT, so invoke the client without specifying a user name or password:

```
mysql --default-auth=authentication_ldap_sasl_client
```

As just described, when the TGT is cached, user-name and password options are not needed in the client command. If the command includes them anyway, they are handled as follows:

- If the command includes a user name, authentication fails if that name does not match the principal name in the TGT.
- If the command includes a password, the client-side plugin ignores it. Because authentication is based on the TGT, it can succeed even if the user-provided password is incorrect. For this reason, the plugin produces a warning if a valid TGT is found that causes a password to be ignored.
- If the Kerberos cache contains no TGT, the client-side SASL LDAP authentication plugin itself can obtain the TGT from the KDC. Invoke the client with options for the name and password of the Kerberos principal associated with the MySQL account (enter the command on a single line, then enter the principal password when prompted):

```
mysql --default-auth=authentication_ldap_sasl_client
 --user=bredon@MYSQL.LOCAL
 --password
```

• If the Kerberos cache contains no TGT and the client command specifies no principal name as the user name, authentication fails.

If you are uncertain whether a TGT exists, you can use klist to check.

Authentication occurs as follows:

- 1. The client uses the TGT to authenticate using Kerberos.
- 2. The server finds the LDAP entry for the principal and uses it to authenticate the connection for the bredon@MYSQL.LOCAL MySQL proxy account.
- 3. The group mapping information in the proxy account authentication string ('#krb\_grp=proxied\_krb\_user') indicates that the authenticated proxied user should be proxied\_krb\_user.
- 4. bredon@MYSQL.LOCAL is treated as a proxy for proxied\_krb\_user, and the following query returns output as shown:

```
mysql> SELECT USER(), CURRENT_USER(), @@proxy_user;
+------------------------------+--------------------+--------------------------+
| USER() | CURRENT_USER() | @@proxy_user |
+------------------------------+--------------------+--------------------------+
| bredon@MYSQL.LOCAL@localhost | proxied_krb_user@% | 'bredon@MYSQL.LOCAL'@'%' |
+------------------------------+--------------------+--------------------------+
```

The USER() value indicates the user name used for the client command (bredon@MYSQL.LOCAL) and the host from which the client connected (localhost).

The CURRENT\_USER() value is the full name of the proxied user account, which consists of the proxied\_krb\_user user part and the % host part.

The @@proxy\_user value indicates the full name of the account used to make the connection to the MySQL server, which consists of the bredon@MYSQL.LOCAL user part and the % host part.

This demonstrates that proxying occurs through the bredon@MYSQL.LOCAL proxy user account, and that bredon@MYSQL.LOCAL assumes the privileges granted to the proxied\_krb\_user proxied user account.

A TGT once obtained is cached on the client side and can be used until it expires without specifying the password again. However the TGT is obtained, the client-side plugin uses it to acquire service tickets and communicate with the server-side plugin.

![](_page_82_Picture_3.jpeg)

#### **Note**

When the client-side authentication plugin itself obtains the TGT, the client user may not want the TGT to be reused. As described in [Client Configuration](#page-82-1) [Parameters for LDAP Authentication](#page-82-1), the local /etc/krb5.conf file can be used to cause the client-side plugin to destroy the TGT when done with it.

The server-side plugin has no access to the TGT itself or the Kerberos password used to obtain it.

The LDAP authentication plugins have no control over the caching mechanism (storage in a local file, in memory, and so forth), but Kerberos utilities such as kswitch may be available for this purpose.

## <span id="page-82-1"></span>**Client Configuration Parameters for LDAP Authentication**

The authentication\_ldap\_sasl\_client client-side SASL LDAP plugin reads the local / etc/krb5.conf file. If this file is missing or inaccessible, an error occurs. Assuming that the file is accessible, it can include an optional [appdefaults] section to provide information used by the plugin. Place the information within the mysql part of the section. For example:

```
[appdefaults]
 mysql = {
 ldap_server_host = "ldap_host.example.com"
 ldap_destroy_tgt = true
 }
```

The client-side plugin recognizes these parameters in the mysql section:

- The ldap\_server\_host value specifies the LDAP server host and can be useful when that host differs from the KDC server host specified in the [realms] section. By default, the plugin uses the KDC server host as the LDAP server host.
- The ldap\_destroy\_tgt value indicates whether the client-side plugin destroys the TGT after obtaining and using it. By default, ldap\_destroy\_tgt is false, but can be set to true to avoid TGT reuse. (This setting applies only to TGTs created by the client-side plugin, not TGTs created by other plugins or externally to MySQL.)

## <span id="page-82-0"></span>**LDAP Search Referral**

An LDAP server can be configured to delegate LDAP searches to another LDAP server, a functionality known as LDAP referral. Suppose that the server a.example.com holds a "dc=example,dc=com" root DN and wishes to delegate searches to another server b.example.com. To enable this, a.example.com would be configured with a named referral object having these attributes:

```
dn: dc=subtree,dc=example,dc=com
objectClass: referral
objectClass: extensibleObject
dc: subtree
ref: ldap://b.example.com/dc=subtree,dc=example,dc=com
```

An issue with enabling LDAP referral is that searches can fail with LDAP operation errors when the search base DN is the root DN, and referral objects are not set. A MySQL DBA might wish to avoid such referral errors for the LDAP authentication plugins, even though LDAP referral might be set globally in the ldap.conf configuration file. To configure on a plugin-specific basis whether the LDAP server should use LDAP referral when communicating with each plugin, set the [authentication\\_ldap\\_simple\\_referral](#page-122-0) and [authentication\\_ldap\\_sasl\\_referral](#page-115-1)

system variables. Setting either variable to ON or OFF causes the corresponding LDAP authentication plugin to tell the LDAP server whether to use referral during MySQL authentication. Each variable has a plugin-specific effect and does not affect other applications that communicate with the LDAP server. Both variables are OFF by default.