---
source: MySQL 8.0 Reference
title: 00_Overview
---

MySQL includes a test plugin that checks account credentials and logs success or failure to the server error log. This is a loadable plugin (not built in) and must be installed prior to use.

The test plugin source code is separate from the server source, unlike the built-in native plugin, so it can be examined as a relatively simple example demonstrating how to write a loadable authentication plugin.

![](_page_105_Picture_8.jpeg)

#### **Note**

This plugin is intended for testing and development purposes, and is not for use in production environments or on servers that are exposed to public networks.

The following table shows the plugin and library file names. The file name suffix might differ on your system. The file must be located in the directory named by the plugin\_dir system variable.

**Table 8.28 Plugin and Library Names for Test Authentication**

| Plugin or File     | Plugin or File Name |
|--------------------|---------------------|
| Server-side plugin | test_plugin_server  |
| Client-side plugin | auth_test_plugin    |
| Library file       | auth_test_plugin.so |

The following sections provide installation and usage information specific to test pluggable authentication:

- [Installing Test Pluggable Authentication](#page-105-0)
- [Uninstalling Test Pluggable Authentication](#page-106-0)
- [Using Test Pluggable Authentication](#page-106-1)

For general information about pluggable authentication in MySQL, see Section 8.2.17, "Pluggable Authentication".

## <span id="page-105-0"></span>**Installing Test Pluggable Authentication**

This section describes how to install the server-side test authentication plugin. For general information about installing plugins, see Section 7.6.1, "Installing and Uninstalling Plugins".

To be usable by the server, the plugin library file must be located in the MySQL plugin directory (the directory named by the plugin\_dir system variable). If necessary, configure the plugin directory location by setting the value of plugin\_dir at server startup.

To load the plugin at server startup, use the --plugin-load-add option to name the library file that contains it. With this plugin-loading method, the option must be given each time the server starts. For example, put these lines in the server my.cnf file, adjusting the .so suffix for your platform as necessary:

[mysqld]

```
plugin-load-add=auth_test_plugin.so
```

After modifying my.cnf, restart the server to cause the new settings to take effect.

Alternatively, to load the plugin at runtime, use this statement, adjusting the .so suffix for your platform as necessary:

```
INSTALL PLUGIN test_plugin_server SONAME 'auth_test_plugin.so';
```

INSTALL PLUGIN loads the plugin immediately, and also registers it in the mysql.plugins system table to cause the server to load it for each subsequent normal startup without the need for - plugin-load-add.

To verify plugin installation, examine the Information Schema PLUGINS table or use the SHOW PLUGINS statement (see Section 7.6.2, "Obtaining Server Plugin Information"). For example:

```
mysql> SELECT PLUGIN_NAME, PLUGIN_STATUS
 FROM INFORMATION_SCHEMA.PLUGINS
 WHERE PLUGIN_NAME LIKE '%test_plugin%';
+--------------------+---------------+
| PLUGIN_NAME | PLUGIN_STATUS |
+--------------------+---------------+
| test_plugin_server | ACTIVE |
+--------------------+---------------+
```

If the plugin fails to initialize, check the server error log for diagnostic messages.

To associate MySQL accounts with the test plugin, see [Using Test Pluggable Authentication.](#page-106-1)

## <span id="page-106-0"></span>**Uninstalling Test Pluggable Authentication**

The method used to uninstall the test authentication plugin depends on how you installed it:

- If you installed the plugin at server startup using a --plugin-load-add option, restart the server without the option.
- If you installed the plugin at runtime using an INSTALL PLUGIN statement, it remains installed across server restarts. To uninstall it, use UNINSTALL PLUGIN:

```
UNINSTALL PLUGIN test_plugin_server;
```

## <span id="page-106-1"></span>**Using Test Pluggable Authentication**

To use the test authentication plugin, create an account and name that plugin in the IDENTIFIED WITH clause:

```
CREATE USER 'testuser'@'localhost'
IDENTIFIED WITH test_plugin_server
BY 'testpassword';
```

The test authentication plugin also requires creating a proxy user as follows:

```
CREATE USER testpassword@localhost;
GRANT PROXY ON testpassword@localhost TO testuser@localhost;
```

Then provide the --user and --password options for that account when you connect to the server. For example:

```
$> mysql --user=testuser --password
Enter password: testpassword
```

The plugin fetches the password as received from the client and compares it with the value stored in the authentication\_string column of the account row in the mysql.user system table. If the two values match, the plugin returns the authentication\_string value as the new effective user ID.

You can look in the server error log for a message indicating whether authentication succeeded (notice that the password is reported as the "user"):

```
[Note] Plugin test_plugin_server reported:
'successfully authenticated user testpassword'
```

# <span id="page-107-0"></span>**8.4.1.13 Pluggable Authentication System Variables**

These variables are unavailable unless the appropriate server-side plugin is installed:

- authentication\_ldap\_sasl for system variables with names of the form authentication\_ldap\_sasl\_xxx
- authentication\_ldap\_simple for system variables with names of the form authentication\_ldap\_simple\_xxx

**Table 8.29 Authentication Plugin System Variable Summary**

| Name                      | Cmd-Line                                              | Option File | System Var | Status Var | Var Scope | Dynamic |
|---------------------------|-------------------------------------------------------|-------------|------------|------------|-----------|---------|
| authentication_fido_rp_id | Yes                                                   | Yes         | Yes        |            | Global    | Yes     |
|                           | authentication_kerberos_service_key_tab<br>Yes        | Yes         | Yes        |            | Global    | No      |
|                           | authentication_kerberos_service_principal<br>Yes      | Yes         | Yes        |            | Global    | Yes     |
|                           | authentication_ldap_sasl_auth_method_name<br>Yes      | Yes         | Yes        |            | Global    | Yes     |
|                           | authentication_ldap_sasl_bind_base_dn<br>Yes          | Yes         | Yes        |            | Global    | Yes     |
|                           | authentication_ldap_sasl_bind_root_dn<br>Yes          | Yes         | Yes        |            | Global    | Yes     |
|                           | authentication_ldap_sasl_bind_root_pwd<br>Yes         | Yes         | Yes        |            | Global    | Yes     |
|                           | authentication_ldap_sasl_ca_path<br>Yes               | Yes         | Yes        |            | Global    | Yes     |
|                           | authentication_ldap_sasl_group_search_attr<br>Yes     | Yes         | Yes        |            | Global    | Yes     |
|                           | authentication_ldap_sasl_group_search_filter<br>Yes   | Yes         | Yes        |            | Global    | Yes     |
|                           | authentication_ldap_sasl_init_pool_size<br>Yes        | Yes         | Yes        |            | Global    | Yes     |
|                           | authentication_ldap_sasl_log_status<br>Yes            | Yes         | Yes        |            | Global    | Yes     |
|                           | authentication_ldap_sasl_max_pool_size<br>Yes         | Yes         | Yes        |            | Global    | Yes     |
|                           | authentication_ldap_sasl_referral<br>Yes              | Yes         | Yes        |            | Global    | Yes     |
|                           | authentication_ldap_sasl_server_host<br>Yes           | Yes         | Yes        |            | Global    | Yes     |
|                           | authentication_ldap_sasl_server_port<br>Yes           | Yes         | Yes        |            | Global    | Yes     |
|                           | authentication_ldap_sasl_tls<br>Yes                   | Yes         | Yes        |            | Global    | Yes     |
|                           | authentication_ldap_sasl_user_search_attr<br>Yes      | Yes         | Yes        |            | Global    | Yes     |
|                           | authentication_ldap_simple_auth_method_name<br>Yes    | Yes         | Yes        |            | Global    | Yes     |
|                           | authentication_ldap_simple_bind_base_dn<br>Yes        | Yes         | Yes        |            | Global    | Yes     |
|                           | authentication_ldap_simple_bind_root_dn<br>Yes        | Yes         | Yes        |            | Global    | Yes     |
|                           | authentication_ldap_simple_bind_root_pwd<br>Yes       | Yes         | Yes        |            | Global    | Yes     |
|                           | authentication_ldap_simple_ca_path<br>Yes             | Yes         | Yes        |            | Global    | Yes     |
|                           | authentication_ldap_simple_group_search_attr<br>Yes   | Yes         | Yes        |            | Global    | Yes     |
|                           | authentication_ldap_simple_group_search_filter<br>Yes | Yes         | Yes        |            | Global    | Yes     |
|                           | authentication_ldap_simple_init_pool_size<br>Yes      | Yes         | Yes        |            | Global    | Yes     |
|                           | authentication_ldap_simple_log_status<br>Yes          | Yes         | Yes        |            | Global    | Yes     |
|                           | authentication_ldap_simple_max_pool_size<br>Yes       | Yes         | Yes        |            | Global    | Yes     |
|                           | authentication_ldap_simple_referral<br>Yes            | Yes         | Yes        |            | Global    | Yes     |
|                           | authentication_ldap_simple_server_host<br>Yes         | Yes         | Yes        |            | Global    | Yes     |

| Name                      | Cmd-Line                                      | Option File                                        | System Var | Status Var | Var Scope | Dynamic |
|---------------------------|-----------------------------------------------|----------------------------------------------------|------------|------------|-----------|---------|
|                           | authentication_ldap_simple_server_port<br>Yes | Yes                                                | Yes        |            | Global    | Yes     |
|                           | authentication_ldap_simple_tls<br>Yes         | Yes                                                | Yes        |            | Global    | Yes     |
|                           | Yes                                           | authentication_ldap_simple_user_search_attr<br>Yes | Yes        |            | Global    | Yes     |
| authentication_policy Yes |                                               | Yes                                                | Yes        |            | Global    | Yes     |
|                           | authentication_windows_log_level<br>Yes       | Yes                                                | Yes        |            | Global    | No      |
|                           | Yes                                           | authentication_windows_use_principal_name<br>Yes   | Yes        |            | Global    | No      |

## <span id="page-108-1"></span>• [authentication\\_fido\\_rp\\_id](#page-108-1)

| Command-Line Format  | authentication-fido-rp-id=value |
|----------------------|---------------------------------|
| Deprecated           | Yes                             |
| System Variable      | authentication_fido_rp_id       |
| Scope                | Global                          |
| Dynamic              | Yes                             |
| SET_VAR Hint Applies | No                              |
| Type                 | String                          |
| Default Value        | MySQL                           |

This variable specifies the relying party ID used for FIDO device registration and FIDO authentication. If FIDO authentication is attempted and this value is not the one expected by the FIDO device, the device assumes that it is not talking to the correct server and an error occurs. The maximum value length is 255 characters.

![](_page_108_Picture_5.jpeg)

#### **Note**

As of MySQL 8.0.35, this plugin variable is deprecated and subject to removal in a future MySQL release.

<span id="page-108-0"></span>• [authentication\\_kerberos\\_service\\_key\\_tab](#page-108-0)

| Command-Line Format  | authentication-kerberos-service<br>key-tab=file_name |
|----------------------|------------------------------------------------------|
| System Variable      | authentication_kerberos_service_key_tab              |
| Scope                | Global                                               |
| Dynamic              | No                                                   |
| SET_VAR Hint Applies | No                                                   |
| Type                 | File name                                            |
| Default Value        | datadir/mysql.keytab                                 |
|                      |                                                      |

The name of the server-side key-table ("keytab") file containing Kerberos service keys to authenticate MySQL service tickets received from clients. The file name should be given as an absolute path name. If this variable is not set, the default is mysql.keytab in the data directory.

The file must exist and contain a valid key for the service principal name (SPN) or authentication of clients will fail. (The SPN and same key also must be created in the Kerberos server.) The file may contain multiple service principal names and their respective key combinations.

The file must be generated by the Kerberos server administrator and be copied to a location accessible by the MySQL server. The file can be validated to make sure that it is correct and was copied properly using this command:

```
klist -k file_name
```

For information about keytab files, see [https://web.mit.edu/kerberos/krb5-latest/doc/basic/](https://web.mit.edu/kerberos/krb5-latest/doc/basic/keytab_def.md) [keytab\\_def.html.](https://web.mit.edu/kerberos/krb5-latest/doc/basic/keytab_def.md)

<span id="page-109-1"></span>• [authentication\\_kerberos\\_service\\_principal](#page-109-1)

| Command-Line Format  | authentication-kerberos-service<br>principal=name |  |  |
|----------------------|---------------------------------------------------|--|--|
| System Variable      | authentication_kerberos_service_principal         |  |  |
| Scope                | Global                                            |  |  |
| Dynamic              | Yes                                               |  |  |
| SET_VAR Hint Applies | No                                                |  |  |
| Type                 | String                                            |  |  |
| Default Value        | mysql/host_name@realm_name                        |  |  |

The Kerberos service principal name (SPN) that the MySQL server sends to clients.

The value is composed from the service name (mysql), a host name, and a realm name. The default value is mysql/host\_name@realm\_name. The realm in the service principal name enables retrieving the exact service key.

To use a nondefault value, set the value using the same format. For example, to use a host name of krbauth.example.com and a realm of MYSQL.LOCAL, set [authentication\\_kerberos\\_service\\_principal](#page-109-1) to mysql/ krbauth.example.com@MYSQL.LOCAL.

The service principal name and service key must already be present in the database managed by the KDC server.

There can be service principal names that differ only by realm name.

<span id="page-109-0"></span>• [authentication\\_ldap\\_sasl\\_auth\\_method\\_name](#page-109-0)

| Command-Line Format  | authentication-ldap-sasl-auth<br>method-name=value |  |
|----------------------|----------------------------------------------------|--|
| System Variable      | authentication_ldap_sasl_auth_method_name          |  |
| Scope                | Global                                             |  |
| Dynamic              | Yes                                                |  |
| SET_VAR Hint Applies | No                                                 |  |
| Type                 | String                                             |  |
| Default Value        | SCRAM-SHA-1                                        |  |
| Valid Values         | SCRAM-SHA-1                                        |  |
|                      | SCRAM-SHA-256                                      |  |

GSSAPI

For SASL LDAP authentication, the authentication method name. Communication between the authentication plugin and the LDAP server occurs according to this authentication method to ensure password security.

These authentication method values are permitted:

• SCRAM-SHA-1: Use a SASL challenge-response mechanism.

The client-side authentication\_ldap\_sasl\_client plugin communicates with the SASL server, using the password to create a challenge and obtain a SASL request buffer, then passes this buffer to the server-side authentication\_ldap\_sasl plugin. The client-side and serverside SASL LDAP plugins use SASL messages for secure transmission of credentials within the LDAP protocol, to avoid sending the cleartext password between the MySQL client and server.

• SCRAM-SHA-256: Use a SASL challenge-response mechanism.

This method is similar to SCRAM-SHA-1, but is more secure. It is available in MySQL 8.0.23 and higher. It requires an OpenLDAP server built using Cyrus SASL 2.1.27 or higher.

• GSSAPI: Use Kerberos, a passwordless and ticket-based protocol.

GSSAPI/Kerberos is supported as an authentication method for MySQL clients and servers only on Linux. It is useful in Linux environments where applications access LDAP using Microsoft Active Directory, which has Kerberos enabled by default.

The client-side authentication\_ldap\_sasl\_client plugin obtains a service ticket using the ticket-granting ticket (TGT) from Kerberos, but does not use LDAP services directly. The serverside authentication\_ldap\_sasl plugin routes Kerberos messages between the client-side plugin and the LDAP server. Using the credentials thus obtained, the server-side plugin then communicates with the LDAP server to interpret LDAP authentication messages and retrieve LDAP groups.

<span id="page-110-0"></span>• [authentication\\_ldap\\_sasl\\_bind\\_base\\_dn](#page-110-0)

| Command-Line Format  | authentication-ldap-sasl-bind<br>base-dn=value |
|----------------------|------------------------------------------------|
| System Variable      | authentication_ldap_sasl_bind_base_dn          |
| Scope                | Global                                         |
| Dynamic              | Yes                                            |
| SET_VAR Hint Applies | No                                             |
| Type                 | String                                         |

| Default Value | NULL |
|---------------|------|
|---------------|------|

For SASL LDAP authentication, the base distinguished name (DN). This variable can be used to limit the scope of searches by anchoring them at a certain location (the "base") within the search tree.

Suppose that members of one set of LDAP user entries each have this form:

```
uid=user_name,ou=People,dc=example,dc=com
```

And that members of another set of LDAP user entries each have this form:

```
uid=user_name,ou=Admin,dc=example,dc=com
```

Then searches work like this for different base DN values:

- If the base DN is ou=People,dc=example,dc=com: Searches find user entries only in the first set.
- If the base DN is ou=Admin,dc=example,dc=com: Searches find user entries only in the second set.
- If the base DN is ou=dc=example,dc=com: Searches find user entries in the first or second set.

In general, more specific base DN values result in faster searches because they limit the search scope more.

<span id="page-111-0"></span>• [authentication\\_ldap\\_sasl\\_bind\\_root\\_dn](#page-111-0)

| Command-Line Format  | authentication-ldap-sasl-bind<br>root-dn=value |
|----------------------|------------------------------------------------|
| System Variable      | authentication_ldap_sasl_bind_root_dn          |
| Scope                | Global                                         |
| Dynamic              | Yes                                            |
| SET_VAR Hint Applies | No                                             |
| Type                 | String                                         |
| Default Value        | NULL                                           |

For SASL LDAP authentication, the root distinguished name (DN). This variable is used in conjunction with [authentication\\_ldap\\_sasl\\_bind\\_root\\_pwd](#page-112-2) as the credentials for authenticating to the LDAP server for the purpose of performing searches. Authentication uses either one or two LDAP bind operations, depending on whether the MySQL account names an LDAP user DN:

- If the account does not name a user DN: authentication\_ldap\_sasl performs an initial LDAP binding using [authentication\\_ldap\\_sasl\\_bind\\_root\\_dn](#page-111-0) and [authentication\\_ldap\\_sasl\\_bind\\_root\\_pwd](#page-112-2). (These are both empty by default, so if they are not set, the LDAP server must permit anonymous connections.) The resulting bind LDAP handle is used to search for the user DN, based on the client user name. authentication\_ldap\_sasl performs a second bind using the user DN and client-supplied password.
- If the account does name a user DN: The first bind operation is unnecessary in this case. authentication\_ldap\_sasl performs a single bind using the user DN and client-supplied password. This is faster than if the MySQL account does not specify an LDAP user DN.

<span id="page-112-2"></span>• [authentication\\_ldap\\_sasl\\_bind\\_root\\_pwd](#page-112-2)

| Command-Line Format  | authentication-ldap-sasl-bind<br>root-pwd=value |
|----------------------|-------------------------------------------------|
| System Variable      | authentication_ldap_sasl_bind_root_pwd          |
| Scope                | Global                                          |
| Dynamic              | Yes                                             |
| SET_VAR Hint Applies | No                                              |
| Type                 | String                                          |
| Default Value        | NULL                                            |

For SASL LDAP authentication, the password for the root distinguished name. This variable is used in conjunction with [authentication\\_ldap\\_sasl\\_bind\\_root\\_dn](#page-111-0). See the description of that variable.

<span id="page-112-0"></span>• [authentication\\_ldap\\_sasl\\_ca\\_path](#page-112-0)

| Command-Line Format  | authentication-ldap-sasl-ca<br>path=value |
|----------------------|-------------------------------------------|
| System Variable      | authentication_ldap_sasl_ca_path          |
| Scope                | Global                                    |
| Dynamic              | Yes                                       |
| SET_VAR Hint Applies | No                                        |
| Type                 | String                                    |
| Default Value        | NULL                                      |

For SASL LDAP authentication, the absolute path of the certificate authority file. Specify this file if it is desired that the authentication plugin perform verification of the LDAP server certificate.

![](_page_112_Picture_7.jpeg)

# **Note**

In addition to setting the [authentication\\_ldap\\_sasl\\_ca\\_path](#page-112-0) variable to the file name, you must add the appropriate certificate authority certificates to the file and enable the [authentication\\_ldap\\_sasl\\_tls](#page-116-0) system variable. These variables can be set to override the default OpenLDAP TLS configuration; see [LDAP Pluggable Authentication and ldap.conf](#page-68-1)

<span id="page-112-1"></span>• [authentication\\_ldap\\_sasl\\_group\\_search\\_attr](#page-112-1)

| Command-Line Format  | authentication-ldap-sasl-group<br>search-attr=value |  |
|----------------------|-----------------------------------------------------|--|
| System Variable      | authentication_ldap_sasl_group_search_attr          |  |
| Scope                | Global                                              |  |
| Dynamic              | Yes                                                 |  |
| SET_VAR Hint Applies | No                                                  |  |
| Type                 | String                                              |  |
| Default Value        | cn                                                  |  |

For SASL LDAP authentication, the name of the attribute that specifies group names in LDAP directory entries. If [authentication\\_ldap\\_sasl\\_group\\_search\\_attr](#page-112-1) has its default value of cn, searches return the cn value as the group name. For example, if an LDAP entry with a uid value of user1 has a cn attribute of mygroup, searches for user1 return mygroup as the group name.

This variable should be the empty string if you want no group or proxy authentication.

If the group search attribute is isMemberOf, LDAP authentication directly retrieves the user attribute isMemberOf value and assigns it as group information. If the group search attribute is not isMemberOf, LDAP authentication searches for all groups where the user is a member. (The latter is the default behavior.) This behavior is based on how LDAP group information can be stored two ways: 1) A group entry can have an attribute named memberUid or member with a value that is a user name; 2) A user entry can have an attribute named isMemberOf with values that are group names.

<span id="page-113-0"></span>• [authentication\\_ldap\\_sasl\\_group\\_search\\_filter](#page-113-0)

| Command-Line Format  | authentication-ldap-sasl-group<br>search-filter=value                                 |  |
|----------------------|---------------------------------------------------------------------------------------|--|
| System Variable      | authentication_ldap_sasl_group_search_filter                                          |  |
| Scope                | Global                                                                                |  |
| Dynamic              | Yes                                                                                   |  |
| SET_VAR Hint Applies | No                                                                                    |  |
| Type                 | String                                                                                |  |
| Default Value        | ( (&(objectClass=posixGroup)<br>(memberUid=%s))(&(objectClass=group)<br>(member=%s))) |  |

For SASL LDAP authentication, the custom group search filter.

The search filter value can contain {UA} and {UD} notation to represent the user name and the full user DN. For example, {UA} is replaced with a user name such as "admin", whereas {UD} is replaced with a use full DN such as "uid=admin,ou=People,dc=example,dc=com". The following value is the default, which supports both OpenLDAP and Active Directory:

```
(|(&(objectClass=posixGroup)(memberUid={UA}))
 (&(objectClass=group)(member={UD})))
```

In some cases for the user scenario, memberOf is a simple user attribute that holds no group information. For additional flexibility, an optional {GA} prefix can be used with the group search attribute. Any group attribute with a {GA} prefix is treated as a user attribute having group names. For example, with a value of {GA}MemberOf, if the group value is the DN, the first attribute value from the group DN is returned as the group name.

<span id="page-113-1"></span>• [authentication\\_ldap\\_sasl\\_init\\_pool\\_size](#page-113-1)

| Command-Line Format  | authentication-ldap-sasl-init<br>pool-size=# |
|----------------------|----------------------------------------------|
| System Variable      | authentication_ldap_sasl_init_pool_size      |
| Scope                | Global                                       |
| Dynamic              | Yes                                          |
| SET_VAR Hint Applies | No                                           |
| Type                 | Integer                                      |
| Default Value        | 10                                           |
| Minimum Value        | 0                                            |
| Maximum Value        | 32767                                        |

| Unit | connections |
|------|-------------|
|------|-------------|

For SASL LDAP authentication, the initial size of the pool of connections to the LDAP server. Choose the value for this variable based on the average number of concurrent authentication requests to the LDAP server.

The plugin uses [authentication\\_ldap\\_sasl\\_init\\_pool\\_size](#page-113-1) and [authentication\\_ldap\\_sasl\\_max\\_pool\\_size](#page-115-2) together for connection-pool management:

- When the authentication plugin initializes, it creates [authentication\\_ldap\\_sasl\\_init\\_pool\\_size](#page-113-1) connections, unless [authentication\\_ldap\\_sasl\\_max\\_pool\\_size=0](#page-115-2) to disable pooling.
- If the plugin receives an authentication request when there are no free connections in the current connection pool, the plugin can create a new connection, up to the maximum connection pool size given by [authentication\\_ldap\\_sasl\\_max\\_pool\\_size](#page-115-2).
- If the plugin receives a request when the pool size is already at its maximum and there are no free connections, authentication fails.
- When the plugin unloads, it closes all pooled connections.

Changes to plugin system variable settings may have no effect on connections already in the pool. For example, modifying the LDAP server host, port, or TLS settings does not affect existing connections. However, if the original variable values were invalid and the connection pool could not be initialized, the plugin attempts to reinitialize the pool for the next LDAP request. In this case, the new system variable values are used for the reinitialization attempt.

If [authentication\\_ldap\\_sasl\\_max\\_pool\\_size=0](#page-115-2) to disable pooling, each LDAP connection opened by the plugin uses the values the system variables have at that time.

<span id="page-114-0"></span>• [authentication\\_ldap\\_sasl\\_log\\_status](#page-114-0)

| Command-Line Format  | authentication-ldap-sasl-log<br>status=# |
|----------------------|------------------------------------------|
| System Variable      | authentication_ldap_sasl_log_status      |
| Scope                | Global                                   |
| Dynamic              | Yes                                      |
| SET_VAR Hint Applies | No                                       |
| Type                 | Integer                                  |
| Default Value        | 1                                        |
| Minimum Value        | 1                                        |
| Maximum Value        | 6                                        |

For SASL LDAP authentication, the logging level for messages written to the error log. The following table shows the permitted level values and their meanings.

**Table 8.30 Log Levels for authentication\_ldap\_sasl\_log\_status**

| Option Value | Types of Messages Logged                         |
|--------------|--------------------------------------------------|
| 1            | No messages                                      |
| 2            | Error messages                                   |
| 3            | Error and warning messages                       |
| 4            | 1485<br>Error, warning, and information messages |

| Option Value | Types of Messages Logged                                            |
|--------------|---------------------------------------------------------------------|
| 5            | Same as previous level plus debugging<br>messages from MySQL        |
| 6            | Same as previous level plus debugging<br>messages from LDAP library |

Log level 6 is available as of MySQL 8.0.18.

On the client side, messages can be logged to the standard output by setting the AUTHENTICATION\_LDAP\_CLIENT\_LOG environment variable. The permitted and default values are the same as for [authentication\\_ldap\\_sasl\\_log\\_status](#page-114-0).

The AUTHENTICATION\_LDAP\_CLIENT\_LOG environment variable applies only to SASL LDAP authentication. It has no effect for simple LDAP authentication because the client plugin in that case is mysql\_clear\_password, which knows nothing about LDAP operations.

<span id="page-115-2"></span>• [authentication\\_ldap\\_sasl\\_max\\_pool\\_size](#page-115-2)

| Command-Line Format  | authentication-ldap-sasl-max-pool<br>size=# |
|----------------------|---------------------------------------------|
| System Variable      | authentication_ldap_sasl_max_pool_size      |
| Scope                | Global                                      |
| Dynamic              | Yes                                         |
| SET_VAR Hint Applies | No                                          |
| Type                 | Integer                                     |
| Default Value        | 1000                                        |
| Minimum Value        | 0                                           |
| Maximum Value        | 32767                                       |
| Unit                 | connections                                 |

For SASL LDAP authentication, the maximum size of the pool of connections to the LDAP server. To disable connection pooling, set this variable to 0.

This variable is used in conjunction with [authentication\\_ldap\\_sasl\\_init\\_pool\\_size](#page-113-1). See the description of that variable.

<span id="page-115-1"></span>• [authentication\\_ldap\\_sasl\\_referral](#page-115-1)

| Command-Line Format  | authentication-ldap-sasl<br>referral[={OFF ON}] |
|----------------------|-------------------------------------------------|
| System Variable      | authentication_ldap_sasl_referral               |
| Scope                | Global                                          |
| Dynamic              | Yes                                             |
| SET_VAR Hint Applies | No                                              |
| Type                 | Boolean                                         |
| Default Value        | OFF                                             |

For SASL LDAP authentication, whether to enable LDAP search referral. See [LDAP Search Referral.](#page-82-0)

This variable can be set to override the default OpenLDAP referral configuration; see [LDAP](#page-68-1) [Pluggable Authentication and ldap.conf](#page-68-1)

<span id="page-115-0"></span>• [authentication\\_ldap\\_sasl\\_server\\_host](#page-115-0)

| Command-Line Format  | authentication-ldap-sasl-server<br>host=host_name |
|----------------------|---------------------------------------------------|
| System Variable      | authentication_ldap_sasl_server_host              |
| Scope                | Global                                            |
| Dynamic              | Yes                                               |
| SET_VAR Hint Applies | No                                                |
| Type                 | String                                            |

The LDAP server host for SASL LDAP authentication; this can be a host name or IP address.

<span id="page-116-1"></span>• [authentication\\_ldap\\_sasl\\_server\\_port](#page-116-1)

| Command-Line Format  | authentication-ldap-sasl-server<br>port=port_num |
|----------------------|--------------------------------------------------|
| System Variable      | authentication_ldap_sasl_server_port             |
| Scope                | Global                                           |
| Dynamic              | Yes                                              |
| SET_VAR Hint Applies | No                                               |
| Type                 | Integer                                          |
| Default Value        | 389                                              |
| Minimum Value        | 1                                                |
| Maximum Value        | 32376                                            |

For SASL LDAP authentication, the LDAP server TCP/IP port number.

As of MySQL 8.0.14, if the LDAP port number is configured as 636 or 3269, the plugin uses LDAPS (LDAP over SSL) instead of LDAP. (LDAPS differs from startTLS.)

<span id="page-116-0"></span>• [authentication\\_ldap\\_sasl\\_tls](#page-116-0)

| Command-Line Format  | authentication-ldap-sasl<br>tls[={OFF ON}] |
|----------------------|--------------------------------------------|
| System Variable      | authentication_ldap_sasl_tls               |
| Scope                | Global                                     |
| Dynamic              | Yes                                        |
| SET_VAR Hint Applies | No                                         |
| Type                 | Boolean                                    |
| Default Value        | OFF                                        |

For SASL LDAP authentication, whether connections by the plugin to the LDAP server are secure. If this variable is enabled, the plugin uses TLS to connect securely to the LDAP server. This variable can be set to override the default OpenLDAP TLS configuration; see [LDAP](#page-68-1) [Pluggable Authentication and ldap.conf](#page-68-1) If you enable this variable, you may also wish to set the [authentication\\_ldap\\_sasl\\_ca\\_path](#page-112-0) variable.

MySQL LDAP plugins support the StartTLS method, which initializes TLS on top of a plain LDAP connection.

As of MySQL 8.0.14, LDAPS can be used by setting the [authentication\\_ldap\\_sasl\\_server\\_port](#page-116-1) system variable. <span id="page-117-0"></span>• [authentication\\_ldap\\_sasl\\_user\\_search\\_attr](#page-117-0)

| Command-Line Format  | authentication-ldap-sasl-user<br>search-attr=value |  |
|----------------------|----------------------------------------------------|--|
| System Variable      | authentication_ldap_sasl_user_search_attr          |  |
| Scope                | Global                                             |  |
| Dynamic              | Yes                                                |  |
| SET_VAR Hint Applies | No                                                 |  |
| Type                 | String                                             |  |
| Default Value        | uid                                                |  |

For SASL LDAP authentication, the name of the attribute that specifies user names in LDAP directory entries. If a user distinguished name is not provided, the authentication plugin searches for the name using this attribute. For example, if the [authentication\\_ldap\\_sasl\\_user\\_search\\_attr](#page-117-0) value is uid, a search for the user name user1 finds entries with a uid value of user1.

<span id="page-117-1"></span>• [authentication\\_ldap\\_simple\\_auth\\_method\\_name](#page-117-1)

| Command-Line Format  | authentication-ldap-simple-auth<br>method-name=value |
|----------------------|------------------------------------------------------|
| System Variable      | authentication_ldap_simple_auth_method_name          |
| Scope                | Global                                               |
| Dynamic              | Yes                                                  |
| SET_VAR Hint Applies | No                                                   |
| Type                 | String                                               |
| Default Value        | SIMPLE                                               |
| Valid Values         | SIMPLE                                               |
|                      | AD-FOREST                                            |

For simple LDAP authentication, the authentication method name. Communication between the authentication plugin and the LDAP server occurs according to this authentication method.

![](_page_117_Picture_7.jpeg)

# **Note**

For all simple LDAP authentication methods, it is recommended to also set TLS parameters to require that communication with the LDAP server take place over secure connections.

These authentication method values are permitted:

- SIMPLE: Use simple LDAP authentication. This method uses either one or two LDAP bind operations, depending on whether the MySQL account names an LDAP user distinguished name. See the description of [authentication\\_ldap\\_simple\\_bind\\_root\\_dn](#page-118-0).
- AD-FOREST: A variation on SIMPLE, such that authentication searches all domains in the Active Directory forest, performing an LDAP bind to each Active Directory domain until the user is found in some domain.
- [authentication\\_ldap\\_simple\\_bind\\_base\\_dn](#page-117-2)

<span id="page-117-2"></span>

|      | Command-Line Format | authentication-ldap-simple-bind |
|------|---------------------|---------------------------------|
| 1488 |                     | base-dn=value                   |

| System Variable      | authentication_ldap_simple_bind_base_dn |
|----------------------|-----------------------------------------|
| Scope                | Global                                  |
| Dynamic              | Yes                                     |
| SET_VAR Hint Applies | No                                      |
| Type                 | String                                  |
| Default Value        | NULL                                    |

For simple LDAP authentication, the base distinguished name (DN). This variable can be used to limit the scope of searches by anchoring them at a certain location (the "base") within the search tree.

Suppose that members of one set of LDAP user entries each have this form:

```
uid=user_name,ou=People,dc=example,dc=com
```

And that members of another set of LDAP user entries each have this form:

```
uid=user_name,ou=Admin,dc=example,dc=com
```

Then searches work like this for different base DN values:

- If the base DN is ou=People,dc=example,dc=com: Searches find user entries only in the first set.
- If the base DN is ou=Admin,dc=example,dc=com: Searches find user entries only in the second set.
- If the base DN is ou=dc=example,dc=com: Searches find user entries in the first or second set.

In general, more specific base DN values result in faster searches because they limit the search scope more.

<span id="page-118-0"></span>• [authentication\\_ldap\\_simple\\_bind\\_root\\_dn](#page-118-0)

| Command-Line Format  | authentication-ldap-simple-bind<br>root-dn=value |
|----------------------|--------------------------------------------------|
| System Variable      | authentication_ldap_simple_bind_root_dn          |
| Scope                | Global                                           |
| Dynamic              | Yes                                              |
| SET_VAR Hint Applies | No                                               |
| Type                 | String                                           |
| Default Value        | NULL                                             |

For simple LDAP authentication, the root distinguished name (DN). This variable is used in conjunction with [authentication\\_ldap\\_simple\\_bind\\_root\\_pwd](#page-119-2) as the credentials for authenticating to the LDAP server for the purpose of performing searches. Authentication uses either one or two LDAP bind operations, depending on whether the MySQL account names an LDAP user DN:

• If the account does not name a user DN: authentication\_ldap\_simple performs an initial LDAP binding using [authentication\\_ldap\\_simple\\_bind\\_root\\_dn](#page-118-0) and [authentication\\_ldap\\_simple\\_bind\\_root\\_pwd](#page-119-2). (These are both empty by default, so if they are not set, the LDAP server must permit anonymous connections.) The resulting bind LDAP handle is used to search for the user DN, based on the client user name. authentication\_ldap\_simple performs a second bind using the user DN and client-supplied password.

- If the account does name a user DN: The first bind operation is unnecessary in this case. authentication\_ldap\_simple performs a single bind using the user DN and client-supplied password. This is faster than if the MySQL account does not specify an LDAP user DN.
- <span id="page-119-2"></span>• [authentication\\_ldap\\_simple\\_bind\\_root\\_pwd](#page-119-2)

| Command-Line Format  | authentication-ldap-simple-bind<br>root-pwd=value |
|----------------------|---------------------------------------------------|
| System Variable      | authentication_ldap_simple_bind_root_pwd          |
| Scope                | Global                                            |
| Dynamic              | Yes                                               |
| SET_VAR Hint Applies | No                                                |
| Type                 | String                                            |
| Default Value        | NULL                                              |

For simple LDAP authentication, the password for the root distinguished name. This variable is used in conjunction with [authentication\\_ldap\\_simple\\_bind\\_root\\_dn](#page-118-0). See the description of that variable.

<span id="page-119-0"></span>• [authentication\\_ldap\\_simple\\_ca\\_path](#page-119-0)

| Command-Line Format  | authentication-ldap-simple-ca<br>path=value |
|----------------------|---------------------------------------------|
| System Variable      | authentication_ldap_simple_ca_path          |
| Scope                | Global                                      |
| Dynamic              | Yes                                         |
| SET_VAR Hint Applies | No                                          |
| Type                 | String                                      |
| Default Value        | NULL                                        |

For simple LDAP authentication, the absolute path of the certificate authority file. Specify this file if it is desired that the authentication plugin perform verification of the LDAP server certificate.

![](_page_119_Picture_8.jpeg)

#### **Note**

In addition to setting the [authentication\\_ldap\\_simple\\_ca\\_path](#page-119-0) variable to the file name, you must add the appropriate certificate authority certificates to the file and enable the [authentication\\_ldap\\_simple\\_tls](#page-124-0) system variable. These variables can be set to override the default OpenLDAP TLS configuration; see [LDAP Pluggable Authentication and](#page-68-1) [ldap.conf](#page-68-1)

<span id="page-119-1"></span>• [authentication\\_ldap\\_simple\\_group\\_search\\_attr](#page-119-1)

| Command-Line Format  | authentication-ldap-simple-group<br>search-attr=value |  |
|----------------------|-------------------------------------------------------|--|
| System Variable      | authentication_ldap_simple_group_search_attr          |  |
| Scope                | Global                                                |  |
| Dynamic              | Yes                                                   |  |
| SET_VAR Hint Applies | No                                                    |  |
| Type                 | String                                                |  |

| Default Value | cn |
|---------------|----|
|---------------|----|

For simple LDAP authentication, the name of the attribute that specifies group names in LDAP directory entries. If [authentication\\_ldap\\_simple\\_group\\_search\\_attr](#page-119-1) has its default value of cn, searches return the cn value as the group name. For example, if an LDAP entry with a uid value of user1 has a cn attribute of mygroup, searches for user1 return mygroup as the group name.

If the group search attribute is isMemberOf, LDAP authentication directly retrieves the user attribute isMemberOf value and assigns it as group information. If the group search attribute is not isMemberOf, LDAP authentication searches for all groups where the user is a member. (The latter is the default behavior.) This behavior is based on how LDAP group information can be stored two ways: 1) A group entry can have an attribute named memberUid or member with a value that is a user name; 2) A user entry can have an attribute named isMemberOf with values that are group names.

<span id="page-120-0"></span>• [authentication\\_ldap\\_simple\\_group\\_search\\_filter](#page-120-0)

| search-filter=value                                                                   |                                  |
|---------------------------------------------------------------------------------------|----------------------------------|
| authentication_ldap_simple_group_search_filter                                        |                                  |
| Global                                                                                |                                  |
| Yes                                                                                   |                                  |
| No                                                                                    |                                  |
| String                                                                                |                                  |
| ( (&(objectClass=posixGroup)<br>(memberUid=%s))(&(objectClass=group)<br>(member=%s))) |                                  |
|                                                                                       | authentication-ldap-simple-group |

For simple LDAP authentication, the custom group search filter.

The search filter value can contain {UA} and {UD} notation to represent the user name and the full user DN. For example, {UA} is replaced with a user name such as "admin", whereas {UD} is replaced with a use full DN such as "uid=admin,ou=People,dc=example,dc=com". The following value is the default, which supports both OpenLDAP and Active Directory:

```
(|(&(objectClass=posixGroup)(memberUid={UA}))
 (&(objectClass=group)(member={UD})))
```

In some cases for the user scenario, memberOf is a simple user attribute that holds no group information. For additional flexibility, an optional {GA} prefix can be used with the group search attribute. Any group attribute with a {GA} prefix is treated as a user attribute having group names. For example, with a value of {GA}MemberOf, if the group value is the DN, the first attribute value from the group DN is returned as the group name.

<span id="page-120-1"></span>• [authentication\\_ldap\\_simple\\_init\\_pool\\_size](#page-120-1)

| Command-Line Format  | authentication-ldap-simple-init<br>pool-size=# |  |
|----------------------|------------------------------------------------|--|
| System Variable      | authentication_ldap_simple_init_pool_size      |  |
| Scope                | Global                                         |  |
| Dynamic              | Yes                                            |  |
| SET_VAR Hint Applies | No                                             |  |
| Type                 | Integer                                        |  |

| Default Value | 10          |
|---------------|-------------|
| Minimum Value | 0           |
| Maximum Value | 32767       |
| Unit          | connections |

For simple LDAP authentication, the initial size of the pool of connections to the LDAP server. Choose the value for this variable based on the average number of concurrent authentication requests to the LDAP server.

The plugin uses [authentication\\_ldap\\_simple\\_init\\_pool\\_size](#page-120-1) and [authentication\\_ldap\\_simple\\_max\\_pool\\_size](#page-122-1) together for connection-pool management:

- When the authentication plugin initializes, it creates [authentication\\_ldap\\_simple\\_init\\_pool\\_size](#page-120-1) connections, unless [authentication\\_ldap\\_simple\\_max\\_pool\\_size=0](#page-122-1) to disable pooling.
- If the plugin receives an authentication request when there are no free connections in the current connection pool, the plugin can create a new connection, up to the maximum connection pool size given by [authentication\\_ldap\\_simple\\_max\\_pool\\_size](#page-122-1).
- If the plugin receives a request when the pool size is already at its maximum and there are no free connections, authentication fails.
- When the plugin unloads, it closes all pooled connections.

Changes to plugin system variable settings may have no effect on connections already in the pool. For example, modifying the LDAP server host, port, or TLS settings does not affect existing connections. However, if the original variable values were invalid and the connection pool could not be initialized, the plugin attempts to reinitialize the pool for the next LDAP request. In this case, the new system variable values are used for the reinitialization attempt.

If [authentication\\_ldap\\_simple\\_max\\_pool\\_size=0](#page-122-1) to disable pooling, each LDAP connection opened by the plugin uses the values the system variables have at that time.

<span id="page-121-0"></span>• [authentication\\_ldap\\_simple\\_log\\_status](#page-121-0)

| Command-Line Format  | authentication-ldap-simple-log<br>status=# |
|----------------------|--------------------------------------------|
| System Variable      | authentication_ldap_simple_log_status      |
| Scope                | Global                                     |
| Dynamic              | Yes                                        |
| SET_VAR Hint Applies | No                                         |
| Type                 | Integer                                    |
| Default Value        | 1                                          |
| Minimum Value        | 1                                          |
| Maximum Value        | 6                                          |

For simple LDAP authentication, the logging level for messages written to the error log. The following table shows the permitted level values and their meanings.

**Table 8.31 Log Levels for authentication\_ldap\_simple\_log\_status**

|      | Option Value | Types of Messages Logged |
|------|--------------|--------------------------|
| 1492 | 1            | No messages              |

| Option Value | Types of Messages Logged                                            |
|--------------|---------------------------------------------------------------------|
| 2            | Error messages                                                      |
| 3            | Error and warning messages                                          |
| 4            | Error, warning, and information messages                            |
| 5            | Same as previous level plus debugging<br>messages from MySQL        |
| 6            | Same as previous level plus debugging<br>messages from LDAP library |

Log level 6 is available as of MySQL 8.0.18.

<span id="page-122-1"></span>• [authentication\\_ldap\\_simple\\_max\\_pool\\_size](#page-122-1)

| Command-Line Format  | authentication-ldap-simple-max<br>pool-size=# |
|----------------------|-----------------------------------------------|
| System Variable      | authentication_ldap_simple_max_pool_size      |
| Scope                | Global                                        |
| Dynamic              | Yes                                           |
| SET_VAR Hint Applies | No                                            |
| Type                 | Integer                                       |
| Default Value        | 1000                                          |
| Minimum Value        | 0                                             |
| Maximum Value        | 32767                                         |
| Unit                 | connections                                   |

For simple LDAP authentication, the maximum size of the pool of connections to the LDAP server. To disable connection pooling, set this variable to 0.

This variable is used in conjunction with [authentication\\_ldap\\_simple\\_init\\_pool\\_size](#page-120-1). See the description of that variable.

<span id="page-122-0"></span>• [authentication\\_ldap\\_simple\\_referral](#page-122-0)

| Command-Line Format  | authentication-ldap-simple<br>referral[={OFF ON}] |
|----------------------|---------------------------------------------------|
| System Variable      | authentication_ldap_simple_referral               |
| Scope                | Global                                            |
| Dynamic              | Yes                                               |
| SET_VAR Hint Applies | No                                                |
| Type                 | Boolean                                           |
| Default Value        | OFF                                               |

For simple LDAP authentication, whether to enable LDAP search referral. See [LDAP Search](#page-82-0) [Referral.](#page-82-0)

<span id="page-122-2"></span>• [authentication\\_ldap\\_simple\\_server\\_host](#page-122-2)

| Command-Line Format | authentication-ldap-simple-server           |
|---------------------|---------------------------------------------|
|                     | host=host_name                              |
| System Variable     | authentication_ldap_simple_server_host 1493 |

| Scope                | Global |
|----------------------|--------|
| Dynamic              | Yes    |
| SET_VAR Hint Applies | No     |
| Type                 | String |

For simple LDAP authentication, the LDAP server host. The permitted values for this variable depend on the authentication method:

- For [authentication\\_ldap\\_simple\\_auth\\_method\\_name=SIMPLE](#page-117-1): The LDAP server host can be a host name or IP address.
- For [authentication\\_ldap\\_simple\\_auth\\_method\\_name=AD-FOREST](#page-117-1). The LDAP server host can be an Active Directory domain name. For example, for an LDAP server URL of ldap:// example.mem.local:389, the domain name can be mem.local.

An Active Directory forest setup can have multiple domains (LDAP server IPs), which can be discovered using DNS. On Unix and Unix-like systems, some additional setup may be required to configure your DNS server with SRV records that specify the LDAP servers for the Active Directory domain. For information about DNS SRV, see [RFC 2782.](https://tools.ietf.org/html/rfc2782)

Suppose that your configuration has these properties:

- The name server that provides information about Active Directory domains has IP address 10.172.166.100.
- The LDAP servers have names ldap1.mem.local through ldap3.mem.local and IP addresses 10.172.166.101 through 10.172.166.103.

You want the LDAP servers to be discoverable using SRV searches. For example, at the command line, a command like this should list the LDAP servers:

```
host -t SRV _ldap._tcp.mem.local
```

Perform the DNS configuration as follows:

1. Add a line to /etc/resolv.conf to specify the name server that provides information about Active Directory domains:

```
nameserver 10.172.166.100
```

2. Configure the appropriate zone file for the name server with SRV records for the LDAP servers:

```
_ldap._tcp.mem.local. 86400 IN SRV 0 100 389 ldap1.mem.local.
_ldap._tcp.mem.local. 86400 IN SRV 0 100 389 ldap2.mem.local.
_ldap._tcp.mem.local. 86400 IN SRV 0 100 389 ldap3.mem.local.
```

3. It may also be necessary to specify the IP address for the LDAP servers in /etc/hosts if the server host cannot be resolved. For example, add lines like this to the file:

```
10.172.166.101 ldap1.mem.local
10.172.166.102 ldap2.mem.local
10.172.166.103 ldap3.mem.local
```

With the DNS configured as just described, the server-side LDAP plugin can discover the LDAP servers and tries to authenticate in all domains until authentication succeeds or there are no more servers.

Windows needs no such settings as just described. Given the LDAP server host in the [authentication\\_ldap\\_simple\\_server\\_host](#page-122-2) value, the Windows LDAP library searches all domains and attempts to authenticate.

<span id="page-124-2"></span>• [authentication\\_ldap\\_simple\\_server\\_port](#page-124-2)

| Command-Line Format  | authentication-ldap-simple-server<br>port=port_num |
|----------------------|----------------------------------------------------|
| System Variable      | authentication_ldap_simple_server_port             |
| Scope                | Global                                             |
| Dynamic              | Yes                                                |
| SET_VAR Hint Applies | No                                                 |
| Type                 | Integer                                            |
| Default Value        | 389                                                |
| Minimum Value        | 1                                                  |
| Maximum Value        | 32376                                              |

For simple LDAP authentication, the LDAP server TCP/IP port number.

As of MySQL 8.0.14, if the LDAP port number is configured as 636 or 3269, the plugin uses LDAPS (LDAP over SSL) instead of LDAP. (LDAPS differs from startTLS.)

<span id="page-124-0"></span>• [authentication\\_ldap\\_simple\\_tls](#page-124-0)

| Command-Line Format  | authentication-ldap-simple<br>tls[={OFF ON}] |
|----------------------|----------------------------------------------|
|                      |                                              |
| System Variable      | authentication_ldap_simple_tls               |
| Scope                | Global                                       |
| Dynamic              | Yes                                          |
| SET_VAR Hint Applies | No                                           |
| Type                 | Boolean                                      |
| Default Value        | OFF                                          |

For simple LDAP authentication, whether connections by the plugin to the LDAP server are secure. If this variable is enabled, the plugin uses TLS to connect securely to the LDAP server. This variable can be set to override the default OpenLDAP TLS configuration; see [LDAP](#page-68-1) [Pluggable Authentication and ldap.conf](#page-68-1) If you enable this variable, you may also wish to set the [authentication\\_ldap\\_simple\\_ca\\_path](#page-119-0) variable.

MySQL LDAP plugins support the StartTLS method, which initializes TLS on top of a plain LDAP connection.

As of MySQL 8.0.14, LDAPS can be used by setting the [authentication\\_ldap\\_simple\\_server\\_port](#page-124-2) system variable.

<span id="page-124-1"></span>• [authentication\\_ldap\\_simple\\_user\\_search\\_attr](#page-124-1)

| Command-Line Format  | authentication-ldap-simple-user<br>search-attr=value |
|----------------------|------------------------------------------------------|
| System Variable      | authentication_ldap_simple_user_search_attr          |
| Scope                | Global                                               |
| Dynamic              | Yes                                                  |
| SET_VAR Hint Applies | No                                                   |
| Type                 | String                                               |

| Default Value | uid |
|---------------|-----|
|---------------|-----|

For simple LDAP authentication, the name of the attribute that specifies user names in LDAP directory entries. If a user distinguished name is not provided, the authentication plugin searches for the name using this attribute. For example, if the [authentication\\_ldap\\_simple\\_user\\_search\\_attr](#page-124-1) value is uid, a search for the user name user1 finds entries with a uid value of user1.