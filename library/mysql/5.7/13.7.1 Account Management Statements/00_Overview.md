---
source: MySQL 5.7 Reference
title: 00_Overview
---

MySQL account information is stored in the tables of the mysql system database. This database and the access control system are discussed extensively in Chapter 5, MySQL Server Administration, which you should consult for additional details.

![](_page_88_Picture_19.jpeg)

### **Important**

Some MySQL releases introduce changes to the grant tables to add new privileges or features. To make sure that you can take advantage of any new capabilities, update your grant tables to the current structure whenever you upgrade MySQL. See Section 2.10, "Upgrading MySQL".

When the read\_only system variable is enabled, account-management statements require the SUPER privilege, in addition to any other required privileges. This is because they modify tables in the mysql system database.

# <span id="page-89-0"></span>**13.7.1.1 ALTER USER Statement**

```
ALTER USER [IF EXISTS]
 user [auth_option] [, user [auth_option]] ...
 [REQUIRE {NONE | tls_option [[AND] tls_option] ...}]
 [WITH resource_option [resource_option] ...]
 [password_option | lock_option] ...
ALTER USER [IF EXISTS]
 USER() IDENTIFIED BY 'auth_string'
user:
 (see Section 6.2.4, "Specifying Account Names")
auth_option: {
 IDENTIFIED BY 'auth_string'
 | IDENTIFIED WITH auth_plugin
 | IDENTIFIED WITH auth_plugin BY 'auth_string'
 | IDENTIFIED WITH auth_plugin AS 'auth_string'
}
tls_option: {
 SSL
 | X509
 | CIPHER 'cipher'
 | ISSUER 'issuer'
 | SUBJECT 'subject'
}
resource_option: {
 MAX_QUERIES_PER_HOUR count
 | MAX_UPDATES_PER_HOUR count
 | MAX_CONNECTIONS_PER_HOUR count
 | MAX_USER_CONNECTIONS count
}
password_option: {
 PASSWORD EXPIRE
 | PASSWORD EXPIRE DEFAULT
 | PASSWORD EXPIRE NEVER
 | PASSWORD EXPIRE INTERVAL N DAY
}
lock_option: {
 ACCOUNT LOCK
 | ACCOUNT UNLOCK
}
```

The [ALTER USER](#page-89-0) statement modifies MySQL accounts. It enables authentication, SSL/TLS, resourcelimit, and password-management properties to be modified for existing accounts. It can also be used to lock and unlock accounts.

To use [ALTER USER](#page-89-0), you must have the global CREATE USER privilege or the UPDATE privilege for the mysql system database. When the read\_only system variable is enabled, [ALTER USER](#page-89-0) additionally requires the SUPER privilege.

By default, an error occurs if you try to modify a user that does not exist. If the IF EXISTS clause is given, the statement produces a warning for each named user that does not exist, rather than an error.

![](_page_89_Picture_7.jpeg)

#### **Important**

Under some circumstances, [ALTER USER](#page-89-0) may be recorded in server logs or on the client side in a history file such as ~/.mysql\_history, which means that cleartext passwords may be read by anyone having read access to that

information. For information about the conditions under which this occurs for the server logs and how to control it, see Section 6.1.2.3, "Passwords and Logging". For similar information about client-side logging, see Section 4.5.1.3, "mysql Client Logging".

There are several aspects to the [ALTER USER](#page-89-0) statement, described under the following topics:

- [ALTER USER Overview](#page-90-0)
- [ALTER USER Authentication Options](#page-91-0)
- [ALTER USER SSL/TLS Options](#page-92-0)
- [ALTER USER Resource-Limit Options](#page-94-0)
- [ALTER USER Password-Management Options](#page-94-1)
- [ALTER USER Account-Locking Options](#page-95-1)

### <span id="page-90-0"></span>**ALTER USER Overview**

For each affected account, [ALTER USER](#page-89-0) modifies the corresponding row in the mysql.user system table to reflect the properties specified in the statement. Unspecified properties retain their current values.

Each account name uses the format described in Section 6.2.4, "Specifying Account Names". The host name part of the account name, if omitted, defaults to '%'. It is also possible to specify CURRENT\_USER or CURRENT\_USER() to refer to the account associated with the current session.

In one case only, the account may be specified with the USER() function:

```
ALTER USER USER() IDENTIFIED BY 'auth_string';
```

This syntax enables changing your own password without naming your account literally.

For [ALTER USER](#page-89-0) syntax that permits an auth\_option value to follow a user value, auth\_option indicates how the account authenticates by specifying an account authentication plugin, credentials (for example, a password), or both. Each auth\_option value applies only to the account named immediately preceding it.

Following the user specifications, the statement may include options for SSL/TLS, resource-limit, password-management, and locking properties. All such options are global to the statement and apply to all accounts named in the statement.

Example: Change an account's password and expire it. As a result, the user must connect with the named password and choose a new one at the next connection:

```
ALTER USER 'jeffrey'@'localhost'
 IDENTIFIED BY 'new_password' PASSWORD EXPIRE;
```

Example: Modify an account to use the sha256\_password authentication plugin and the given password. Require that a new password be chosen every 180 days:

```
ALTER USER 'jeffrey'@'localhost'
 IDENTIFIED WITH sha256_password BY 'new_password'
 PASSWORD EXPIRE INTERVAL 180 DAY;
```

Example: Lock or unlock an account:

```
ALTER USER 'jeffrey'@'localhost' ACCOUNT LOCK;
ALTER USER 'jeffrey'@'localhost' ACCOUNT UNLOCK;
```

Example: Require an account to connect using SSL and establish a limit of 20 connections per hour:

```
ALTER USER 'jeffrey'@'localhost'
 REQUIRE SSL WITH MAX_CONNECTIONS_PER_HOUR 20;
```

Example: Alter multiple accounts, specifying some per-account properties and some global properties:

```
ALTER USER
 'jeffrey'@'localhost' IDENTIFIED BY 'new_password',
 'jeanne'@'localhost'
 REQUIRE SSL WITH MAX_USER_CONNECTIONS 2;
```

The IDENTIFIED BY value following jeffrey applies only to its immediately preceding account, so it changes the password to 'jeffrey\_new\_password' only for jeffrey. For jeanne, there is no per-account value (thus leaving the password unchanged).

The remaining properties apply globally to all accounts named in the statement, so for both accounts:

- Connections are required to use SSL.
- The account can be used for a maximum of two simultaneous connections.

In the absence of a particular type of option, the account remains unchanged in that respect. For example, with no locking option, the locking state of the account is not changed.

### <span id="page-91-0"></span>**ALTER USER Authentication Options**

An account name may be followed by an auth\_option authentication option that specifies the account authentication plugin, credentials, or both:

• auth\_plugin names an authentication plugin. The plugin name can be a quoted string literal or an unquoted name. Plugin names are stored in the plugin column of the mysql.user system table.

For auth\_option syntax that does not specify an authentication plugin, the default plugin is indicated by the value of the default\_authentication\_plugin system variable. For descriptions of each plugin, see Section 6.4.1, "Authentication Plugins".

- Credentials are stored in the mysql.user system table. An 'auth\_string' value specifies account credentials, either as a cleartext (unencrypted) string or hashed in the format expected by the authentication plugin associated with the account, respectively:
  - For syntax that uses BY 'auth\_string', the string is cleartext and is passed to the authentication plugin for possible hashing. The result returned by the plugin is stored in the mysql.user table. A plugin may use the value as specified, in which case no hashing occurs.
  - For syntax that uses AS 'auth\_string', the string is assumed to be already in the format the authentication plugin requires, and is stored as is in the mysql.user table. If a plugin requires a hashed value, the value must be already hashed in a format appropriate for the plugin, or the value cannot be used by the plugin and correct authentication of client connections cannot occur.
  - If an authentication plugin performs no hashing of the authentication string, the BY 'auth\_string' and AS 'auth\_string' clauses have the same effect: The authentication string is stored as is in the mysql.user system table.

[ALTER USER](#page-89-0) permits these auth\_option syntaxes:

• IDENTIFIED BY 'auth\_string'

Sets the account authentication plugin to the default plugin, passes the cleartext 'auth\_string' value to the plugin for possible hashing, and stores the result in the account row in the mysql.user system table.

• IDENTIFIED WITH auth\_plugin

Sets the account authentication plugin to auth\_plugin, clears the credentials to the empty string (the credentials are associated with the old authentication plugin, not the new one), and stores the result in the account row in the mysql.user system table.

In addition, the password is marked expired. The user must choose a new one when next connecting.

• IDENTIFIED WITH auth\_plugin BY 'auth\_string'

Sets the account authentication plugin to auth\_plugin, passes the cleartext 'auth\_string' value to the plugin for possible hashing, and stores the result in the account row in the mysql.user system table.

• IDENTIFIED WITH auth\_plugin AS 'auth\_string'

Sets the account authentication plugin to auth\_plugin and stores the 'auth\_string' value as is in the mysql.user account row. If the plugin requires a hashed string, the string is assumed to be already hashed in the format the plugin requires.

Example: Specify the password as cleartext; the default plugin is used:

```
ALTER USER 'jeffrey'@'localhost'
 IDENTIFIED BY 'password';
```

Example: Specify the authentication plugin, along with a cleartext password value:

```
ALTER USER 'jeffrey'@'localhost'
 IDENTIFIED WITH mysql_native_password
 BY 'password';
```

Example: Specify the authentication plugin, along with a hashed password value:

```
ALTER USER 'jeffrey'@'localhost'
 IDENTIFIED WITH mysql_native_password
 AS '*6C8989366EAF75BB670AD8EA7A7FC1176A95CEF4';
```

For additional information about setting passwords and authentication plugins, see Section 6.2.10, "Assigning Account Passwords", and Section 6.2.13, "Pluggable Authentication".

### <span id="page-92-0"></span>**ALTER USER SSL/TLS Options**

MySQL can check X.509 certificate attributes in addition to the usual authentication that is based on the user name and credentials. For background information on the use of SSL/TLS with MySQL, see Section 6.3, "Using Encrypted Connections".

To specify SSL/TLS-related options for a MySQL account, use a REQUIRE clause that specifies one or more tls\_option values.

Order of REQUIRE options does not matter, but no option can be specified twice. The AND keyword is optional between REQUIRE options.

[ALTER USER](#page-89-0) permits these tls\_option values:

• NONE

Indicates that all accounts named by the statement have no SSL or X.509 requirements. Unencrypted connections are permitted if the user name and password are valid. Encrypted connections can be used, at the client's option, if the client has the proper certificate and key files.

```
ALTER USER 'jeffrey'@'localhost' REQUIRE NONE;
```

Clients attempt to establish a secure connection by default. For clients that have REQUIRE NONE, the connection attempt falls back to an unencrypted connection if a secure connection cannot be established. To require an encrypted connection, a client need specify only the --sslmode=REQUIRED option; the connection attempt fails if a secure connection cannot be established.

### • SSL

Tells the server to permit only encrypted connections for all accounts named by the statement.

```
ALTER USER 'jeffrey'@'localhost' REQUIRE SSL;
```

Clients attempt to establish a secure connection by default. For accounts that have REQUIRE SSL, the connection attempt fails if a secure connection cannot be established.

### • X509

For all accounts named by the statement, requires that clients present a valid certificate, but the exact certificate, issuer, and subject do not matter. The only requirement is that it should be possible to verify its signature with one of the CA certificates. Use of X.509 certificates always implies encryption, so the SSL option is unnecessary in this case.

```
ALTER USER 'jeffrey'@'localhost' REQUIRE X509;
```

For accounts with REQUIRE X509, clients must specify the --ssl-key and --ssl-cert options to connect. (It is recommended but not required that --ssl-ca also be specified so that the public certificate provided by the server can be verified.) This is true for ISSUER and SUBJECT as well because those REQUIRE options imply the requirements of X509.

• ISSUER 'issuer'

For all accounts named by the statement, requires that clients present a valid X.509 certificate issued by CA 'issuer'. If a client presents a certificate that is valid but has a different issuer, the server rejects the connection. Use of X.509 certificates always implies encryption, so the SSL option is unnecessary in this case.

```
ALTER USER 'jeffrey'@'localhost'
 REQUIRE ISSUER '/C=SE/ST=Stockholm/L=Stockholm/
 O=MySQL/CN=CA/emailAddress=ca@example.com';
```

Because ISSUER implies the requirements of X509, clients must specify the --ssl-key and - ssl-cert options to connect. (It is recommended but not required that --ssl-ca also be specified so that the public certificate provided by the server can be verified.)

• SUBJECT 'subject'

For all accounts named by the statement, requires that clients present a valid X.509 certificate containing the subject subject. If a client presents a certificate that is valid but has a different subject, the server rejects the connection. Use of X.509 certificates always implies encryption, so the SSL option is unnecessary in this case.

```
ALTER USER 'jeffrey'@'localhost'
 REQUIRE SUBJECT '/C=SE/ST=Stockholm/L=Stockholm/
 O=MySQL demo client certificate/
 CN=client/emailAddress=client@example.com';
```

MySQL does a simple string comparison of the 'subject' value to the value in the certificate, so lettercase and component ordering must be given exactly as present in the certificate.

Because SUBJECT implies the requirements of X509, clients must specify the --ssl-key and - ssl-cert options to connect. (It is recommended but not required that --ssl-ca also be specified so that the public certificate provided by the server can be verified.)

• CIPHER 'cipher'

For all accounts named by the statement, requires a specific cipher method for encrypting connections. This option is needed to ensure that ciphers and key lengths of sufficient strength are used. Encryption can be weak if old algorithms using short encryption keys are used.

```
ALTER USER 'jeffrey'@'localhost'
```

```
 REQUIRE CIPHER 'EDH-RSA-DES-CBC3-SHA';
```

The SUBJECT, ISSUER, and CIPHER options can be combined in the REQUIRE clause:

```
ALTER USER 'jeffrey'@'localhost'
 REQUIRE SUBJECT '/C=SE/ST=Stockholm/L=Stockholm/
 O=MySQL demo client certificate/
 CN=client/emailAddress=client@example.com'
 AND ISSUER '/C=SE/ST=Stockholm/L=Stockholm/
 O=MySQL/CN=CA/emailAddress=ca@example.com'
 AND CIPHER 'EDH-RSA-DES-CBC3-SHA';
```

### <span id="page-94-0"></span>**ALTER USER Resource-Limit Options**

It is possible to place limits on use of server resources by an account, as discussed in Section 6.2.16, "Setting Account Resource Limits". To do so, use a WITH clause that specifies one or more resource\_option values.

Order of WITH options does not matter, except that if a given resource limit is specified multiple times, the last instance takes precedence.

[ALTER USER](#page-89-0) permits these resource\_option values:

• MAX\_QUERIES\_PER\_HOUR count, MAX\_UPDATES\_PER\_HOUR count, MAX\_CONNECTIONS\_PER\_HOUR count

For all accounts named by the statement, these options restrict how many queries, updates, and connections to the server are permitted to each account during any given one-hour period. (Queries for which results are served from the query cache do not count against the MAX\_QUERIES\_PER\_HOUR limit.) If count is 0 (the default), this means that there is no limitation for the account.

• MAX\_USER\_CONNECTIONS count

For all accounts named by the statement, restricts the maximum number of simultaneous connections to the server by each account. A nonzero count specifies the limit for the account explicitly. If count is 0 (the default), the server determines the number of simultaneous connections for the account from the global value of the max\_user\_connections system variable. If max\_user\_connections is also zero, there is no limit for the account.

#### Example:

```
ALTER USER 'jeffrey'@'localhost'
 WITH MAX_QUERIES_PER_HOUR 500 MAX_UPDATES_PER_HOUR 100;
```

### <span id="page-94-1"></span>**ALTER USER Password-Management Options**

[ALTER USER](#page-89-0) supports several password\_option values for password expiration management, to either expire an account password manually or establish its password expiration policy. Policy options do not expire the password. Instead, they determine how the server applies automatic expiration to the account based on account password age. For a given account, its password age is assessed from the date and time of the most recent password change.

This section describes the syntax for password-management options. For information about establishing policy for password management, see Section 6.2.11, "Password Management".

If multiple password-management options are specified, the last one takes precedence.

These options apply only to accounts that use an authentication plugin that stores credentials internally to MySQL. For accounts that use a plugin that performs authentication against a credentials system that is external to MySQL, password management must be handled externally against that system

as well. For more information about internal credentials storage, see Section 6.2.11, "Password Management".

A client session operates in restricted mode if the account password was expired manually or if the password age is considered greater than its permitted lifetime per the automatic expiration policy. In restricted mode, operations performed within the session result in an error until the user establishes a new account password. For information about restricted mode, see Section 6.2.12, "Server Handling of Expired Passwords".

![](_page_95_Picture_3.jpeg)

#### **Note**

Although it is possible to "reset" an expired password by setting it to its current value, it is preferable, as a matter of good policy, to choose a different password.

[ALTER USER](#page-89-0) permits these password\_option values for controlling password expiration:

• PASSWORD EXPIRE

Immediately marks the password expired for all accounts named by the statement.

```
ALTER USER 'jeffrey'@'localhost' PASSWORD EXPIRE;
```

• PASSWORD EXPIRE DEFAULT

Sets all accounts named by the statement so that the global expiration policy applies, as specified by the default\_password\_lifetime system variable.

```
ALTER USER 'jeffrey'@'localhost' PASSWORD EXPIRE DEFAULT;
```

• PASSWORD EXPIRE NEVER

This expiration option overrides the global policy for all accounts named by the statement. For each, it disables password expiration so that the password never expires.

```
ALTER USER 'jeffrey'@'localhost' PASSWORD EXPIRE NEVER;
```

• PASSWORD EXPIRE INTERVAL N DAY

This expiration option overrides the global policy for all accounts named by the statement. For each, it sets the password lifetime to N days. The following statement requires the password to be changed every 180 days:

```
ALTER USER 'jeffrey'@'localhost' PASSWORD EXPIRE INTERVAL 180 DAY;
```

### <span id="page-95-1"></span>**ALTER USER Account-Locking Options**

MySQL supports account locking and unlocking using the ACCOUNT LOCK and ACCOUNT UNLOCK options, which specify the locking state for an account. For additional discussion, see Section 6.2.15, "Account Locking".

If multiple account-locking options are specified, the last one takes precedence.

# <span id="page-95-0"></span>**13.7.1.2 CREATE USER Statement**

```
CREATE USER [IF NOT EXISTS]
 user [auth_option] [, user [auth_option]] ...
 [REQUIRE {NONE | tls_option [[AND] tls_option] ...}]
 [WITH resource_option [resource_option] ...]
 [password_option | lock_option] ...
user:
 (see Section 6.2.4, "Specifying Account Names")
```

```
auth_option: {
 IDENTIFIED BY 'auth_string'
 | IDENTIFIED WITH auth_plugin
 | IDENTIFIED WITH auth_plugin BY 'auth_string'
 | IDENTIFIED WITH auth_plugin AS 'auth_string'
 | IDENTIFIED BY PASSWORD 'auth_string'
}
tls_option: {
 SSL
 | X509
 | CIPHER 'cipher'
 | ISSUER 'issuer'
 | SUBJECT 'subject'
}
resource_option: {
 MAX_QUERIES_PER_HOUR count
 | MAX_UPDATES_PER_HOUR count
 | MAX_CONNECTIONS_PER_HOUR count
 | MAX_USER_CONNECTIONS count
}
password_option: {
 PASSWORD EXPIRE
 | PASSWORD EXPIRE DEFAULT
 | PASSWORD EXPIRE NEVER
 | PASSWORD EXPIRE INTERVAL N DAY
}
lock_option: {
 ACCOUNT LOCK
 | ACCOUNT UNLOCK
}
```

The [CREATE USER](#page-95-0) statement creates new MySQL accounts. It enables authentication, SSL/TLS, resource-limit, and password-management properties to be established for new accounts, and controls whether accounts are initially locked or unlocked.

To use [CREATE USER](#page-95-0), you must have the global CREATE USER privilege, or the INSERT privilege for the mysql system database. When the read\_only system variable is enabled, [CREATE USER](#page-95-0) additionally requires the SUPER privilege.

An error occurs if you try to create an account that already exists. If the IF NOT EXISTS clause is given, the statement produces a warning for each named account that already exists, rather than an error.

![](_page_96_Picture_5.jpeg)

### **Important**

Under some circumstances, [CREATE USER](#page-95-0) may be recorded in server logs or on the client side in a history file such as ~/.mysql\_history, which means that cleartext passwords may be read by anyone having read access to that information. For information about the conditions under which this occurs for the server logs and how to control it, see Section 6.1.2.3, "Passwords and Logging". For similar information about client-side logging, see Section 4.5.1.3, "mysql Client Logging".

There are several aspects to the [CREATE USER](#page-95-0) statement, described under the following topics:

- [CREATE USER Overview](#page-97-0)
- [CREATE USER Authentication Options](#page-98-0)
- [CREATE USER SSL/TLS Options](#page-99-0)
- [CREATE USER Resource-Limit Options](#page-101-0)

- [CREATE USER Password-Management Options](#page-101-1)
- [CREATE USER Account-Locking Options](#page-102-1)

### <span id="page-97-0"></span>**CREATE USER Overview**

For each account, [CREATE USER](#page-95-0) creates a new row in the mysql.user system table. The account row reflects the properties specified in the statement. Unspecified properties are set to their default values:

- Authentication: The authentication plugin defined by the default\_authentication\_plugin system variable, and empty credentials
- SSL/TLS: NONE
- Resource limits: Unlimited
- Password management: PASSWORD EXPIRE DEFAULT
- Account locking: ACCOUNT UNLOCK

An account when first created has no privileges. To assign privileges to this account, use one or more [GRANT](#page-103-0) statements.

Each account name uses the format described in Section 6.2.4, "Specifying Account Names". For example:

```
CREATE USER 'jeffrey'@'localhost' IDENTIFIED BY 'password';
```

The host name part of the account name, if omitted, defaults to '%'.

Each user value naming an account may be followed by an optional auth\_option value that indicates how the account authenticates. These values enable account authentication plugins and credentials (for example, a password) to be specified. Each auth\_option value applies only to the account named immediately preceding it.

Following the user specifications, the statement may include options for SSL/TLS, resource-limit, password-management, and locking properties. All such options are global to the statement and apply to all accounts named in the statement.

Example: Create an account that uses the default authentication plugin and the given password. Mark the password expired so that the user must choose a new one at the first connection to the server:

```
CREATE USER 'jeffrey'@'localhost'
 IDENTIFIED BY 'new_password' PASSWORD EXPIRE;
```

Example: Create an account that uses the sha256\_password authentication plugin and the given password. Require that a new password be chosen every 180 days:

```
CREATE USER 'jeffrey'@'localhost'
 IDENTIFIED WITH sha256_password BY 'new_password'
 PASSWORD EXPIRE INTERVAL 180 DAY;
```

Example: Create multiple accounts, specifying some per-account properties and some global properties:

```
CREATE USER
 'jeffrey'@'localhost' IDENTIFIED WITH mysql_native_password
 BY 'new_password1',
 'jeanne'@'localhost' IDENTIFIED WITH sha256_password
 BY 'new_password2'
 REQUIRE X509 WITH MAX_QUERIES_PER_HOUR 60
 ACCOUNT LOCK;
```

Each auth\_option value (IDENTIFIED WITH ... BY in this case) applies only to the account named immediately preceding it, so each account uses the immediately following authentication plugin and password.

The remaining properties apply globally to all accounts named in the statement, so for both accounts:

- Connections must be made using a valid X.509 certificate.
- Up to 60 queries per hour are permitted.
- The account is locked initially, so effectively it is a placeholder and cannot be used until an administrator unlocks it.

### <span id="page-98-0"></span>**CREATE USER Authentication Options**

An account name may be followed by an auth\_option authentication option that specifies the account authentication plugin, credentials, or both:

• auth\_plugin names an authentication plugin. The plugin name can be a quoted string literal or an unquoted name. Plugin names are stored in the plugin column of the mysql.user system table.

For auth\_option syntax that does not specify an authentication plugin, the default plugin is indicated by the value of the default\_authentication\_plugin system variable. For descriptions of each plugin, see Section 6.4.1, "Authentication Plugins".

- Credentials are stored in the mysql.user system table. An 'auth\_string' value specifies account credentials, either as a cleartext (unencrypted) string or hashed in the format expected by the authentication plugin associated with the account, respectively:
  - For syntax that uses BY 'auth\_string', the string is cleartext and is passed to the authentication plugin for possible hashing. The result returned by the plugin is stored in the mysql.user table. A plugin may use the value as specified, in which case no hashing occurs.
  - For syntax that uses AS 'auth\_string', the string is assumed to be already in the format the authentication plugin requires, and is stored as is in the mysql.user table. If a plugin requires a hashed value, the value must be already hashed in a format appropriate for the plugin, or the value cannot be used by the plugin and correct authentication of client connections cannot occur.
  - If an authentication plugin performs no hashing of the authentication string, the BY 'auth\_string' and AS 'auth\_string' clauses have the same effect: The authentication string is stored as is in the mysql.user system table.

[CREATE USER](#page-95-0) permits these auth\_option syntaxes:

• IDENTIFIED BY 'auth\_string'

Sets the account authentication plugin to the default plugin, passes the cleartext 'auth\_string' value to the plugin for possible hashing, and stores the result in the account row in the mysql.user system table.

• IDENTIFIED WITH auth\_plugin

Sets the account authentication plugin to auth\_plugin, clears the credentials to the empty string, and stores the result in the account row in the mysql.user system table.

• IDENTIFIED WITH auth\_plugin BY 'auth\_string'

Sets the account authentication plugin to auth\_plugin, passes the cleartext 'auth\_string' value to the plugin for possible hashing, and stores the result in the account row in the mysql.user system table.

• IDENTIFIED WITH auth\_plugin AS 'auth\_string'

Sets the account authentication plugin to auth\_plugin and stores the 'auth\_string' value as is in the mysql.user account row. If the plugin requires a hashed string, the string is assumed to be already hashed in the format the plugin requires.

• IDENTIFIED BY PASSWORD 'auth\_string'

Sets the account authentication plugin to the default plugin and stores the 'auth\_string' value as is in the mysql.user account row. If the plugin requires a hashed string, the string is assumed to be already hashed in the format the plugin requires.

![](_page_99_Picture_4.jpeg)

#### **Note**

IDENTIFIED BY PASSWORD syntax is deprecated; expect it to be removed in a future MySQL release.

Example: Specify the password as cleartext; the default plugin is used:

```
CREATE USER 'jeffrey'@'localhost'
 IDENTIFIED BY 'password';
```

Example: Specify the authentication plugin, along with a cleartext password value:

```
CREATE USER 'jeffrey'@'localhost'
 IDENTIFIED WITH mysql_native_password BY 'password';
```

In each case, the password value stored in the account row is the cleartext value 'password' after it has been hashed by the authentication plugin associated with the account.

For additional information about setting passwords and authentication plugins, see Section 6.2.10, "Assigning Account Passwords", and Section 6.2.13, "Pluggable Authentication".

### <span id="page-99-0"></span>**CREATE USER SSL/TLS Options**

MySQL can check X.509 certificate attributes in addition to the usual authentication that is based on the user name and credentials. For background information on the use of SSL/TLS with MySQL, see Section 6.3, "Using Encrypted Connections".

To specify SSL/TLS-related options for a MySQL account, use a REQUIRE clause that specifies one or more tls\_option values.

Order of REQUIRE options does not matter, but no option can be specified twice. The AND keyword is optional between REQUIRE options.

[CREATE USER](#page-95-0) permits these tls\_option values:

• NONE

Indicates that all accounts named by the statement have no SSL or X.509 requirements. Unencrypted connections are permitted if the user name and password are valid. Encrypted connections can be used, at the client's option, if the client has the proper certificate and key files.

```
CREATE USER 'jeffrey'@'localhost' REQUIRE NONE;
```

Clients attempt to establish a secure connection by default. For clients that have REQUIRE NONE, the connection attempt falls back to an unencrypted connection if a secure connection cannot be established. To require an encrypted connection, a client need specify only the --sslmode=REQUIRED option; the connection attempt fails if a secure connection cannot be established.

NONE is the default if no SSL-related REQUIRE options are specified.

• SSL

Tells the server to permit only encrypted connections for all accounts named by the statement.

```
CREATE USER 'jeffrey'@'localhost' REQUIRE SSL;
```

Clients attempt to establish a secure connection by default. For accounts that have REQUIRE SSL, the connection attempt fails if a secure connection cannot be established.

• X509

For all accounts named by the statement, requires that clients present a valid certificate, but the exact certificate, issuer, and subject do not matter. The only requirement is that it should be possible to verify its signature with one of the CA certificates. Use of X.509 certificates always implies encryption, so the SSL option is unnecessary in this case.

```
CREATE USER 'jeffrey'@'localhost' REQUIRE X509;
```

For accounts with REQUIRE X509, clients must specify the --ssl-key and --ssl-cert options to connect. (It is recommended but not required that --ssl-ca also be specified so that the public certificate provided by the server can be verified.) This is true for ISSUER and SUBJECT as well because those REQUIRE options imply the requirements of X509.

• ISSUER 'issuer'

For all accounts named by the statement, requires that clients present a valid X.509 certificate issued by CA 'issuer'. If a client presents a certificate that is valid but has a different issuer, the server rejects the connection. Use of X.509 certificates always implies encryption, so the SSL option is unnecessary in this case.

```
CREATE USER 'jeffrey'@'localhost'
 REQUIRE ISSUER '/C=SE/ST=Stockholm/L=Stockholm/
 O=MySQL/CN=CA/emailAddress=ca@example.com';
```

Because ISSUER implies the requirements of X509, clients must specify the --ssl-key and - ssl-cert options to connect. (It is recommended but not required that --ssl-ca also be specified so that the public certificate provided by the server can be verified.)

• SUBJECT 'subject'

For all accounts named by the statement, requires that clients present a valid X.509 certificate containing the subject subject. If a client presents a certificate that is valid but has a different subject, the server rejects the connection. Use of X.509 certificates always implies encryption, so the SSL option is unnecessary in this case.

```
CREATE USER 'jeffrey'@'localhost'
 REQUIRE SUBJECT '/C=SE/ST=Stockholm/L=Stockholm/
 O=MySQL demo client certificate/
 CN=client/emailAddress=client@example.com';
```

MySQL does a simple string comparison of the 'subject' value to the value in the certificate, so lettercase and component ordering must be given exactly as present in the certificate.

Because SUBJECT implies the requirements of X509, clients must specify the --ssl-key and - ssl-cert options to connect. (It is recommended but not required that --ssl-ca also be specified so that the public certificate provided by the server can be verified.)

• CIPHER 'cipher'

For all accounts named by the statement, requires a specific cipher method for encrypting connections. This option is needed to ensure that ciphers and key lengths of sufficient strength are used. Encryption can be weak if old algorithms using short encryption keys are used.

```
CREATE USER 'jeffrey'@'localhost'
 REQUIRE CIPHER 'EDH-RSA-DES-CBC3-SHA';
```

The SUBJECT, ISSUER, and CIPHER options can be combined in the REQUIRE clause:

```
CREATE USER 'jeffrey'@'localhost'
 REQUIRE SUBJECT '/C=SE/ST=Stockholm/L=Stockholm/
 O=MySQL demo client certificate/
 CN=client/emailAddress=client@example.com'
 AND ISSUER '/C=SE/ST=Stockholm/L=Stockholm/
 O=MySQL/CN=CA/emailAddress=ca@example.com'
 AND CIPHER 'EDH-RSA-DES-CBC3-SHA';
```

### <span id="page-101-0"></span>**CREATE USER Resource-Limit Options**

It is possible to place limits on use of server resources by an account, as discussed in Section 6.2.16, "Setting Account Resource Limits". To do so, use a WITH clause that specifies one or more resource\_option values.

Order of WITH options does not matter, except that if a given resource limit is specified multiple times, the last instance takes precedence.

[CREATE USER](#page-95-0) permits these resource\_option values:

• MAX\_QUERIES\_PER\_HOUR count, MAX\_UPDATES\_PER\_HOUR count, MAX\_CONNECTIONS\_PER\_HOUR count

For all accounts named by the statement, these options restrict how many queries, updates, and connections to the server are permitted to each account during any given one-hour period. (Queries for which results are served from the query cache do not count against the MAX\_QUERIES\_PER\_HOUR limit.) If count is 0 (the default), this means that there is no limitation for the account.

• MAX\_USER\_CONNECTIONS count

For all accounts named by the statement, restricts the maximum number of simultaneous connections to the server by each account. A nonzero count specifies the limit for the account explicitly. If count is 0 (the default), the server determines the number of simultaneous connections for the account from the global value of the max\_user\_connections system variable. If max\_user\_connections is also zero, there is no limit for the account.

## Example:

```
CREATE USER 'jeffrey'@'localhost'
 WITH MAX_QUERIES_PER_HOUR 500 MAX_UPDATES_PER_HOUR 100;
```

### <span id="page-101-1"></span>**CREATE USER Password-Management Options**

Account passwords have an age, assessed from the date and time of the most recent password change.

[CREATE USER](#page-95-0) supports several password\_option values for password expiration management, to either expire an account password manually or establish its password expiration policy. Policy options do not expire the password. Instead, they determine how the server applies automatic expiration to the account based on account password age. For a given account, its password age is assessed from the date and time of the most recent password change.

This section describes the syntax for password-management options. For information about establishing policy for password management, see Section 6.2.11, "Password Management".

If multiple password-management options are specified, the last one takes precedence.

These options apply only to accounts that use an authentication plugin that stores credentials internally to MySQL. For accounts that use a plugin that performs authentication against a credentials system that is external to MySQL, password management must be handled externally against that system

as well. For more information about internal credentials storage, see Section 6.2.11, "Password Management".

A client session operates in restricted mode if the account password was expired manually or if the password age is considered greater than its permitted lifetime per the automatic expiration policy. In restricted mode, operations performed within the session result in an error until the user establishes a new account password. For information about restricted mode, see Section 6.2.12, "Server Handling of Expired Passwords".

[CREATE USER](#page-95-0) permits these password\_option values for controlling password expiration:

• PASSWORD EXPIRE

Immediately marks the password expired for all accounts named by the statement.

```
CREATE USER 'jeffrey'@'localhost' PASSWORD EXPIRE;
```

• PASSWORD EXPIRE DEFAULT

Sets all accounts named by the statement so that the global expiration policy applies, as specified by the default\_password\_lifetime system variable.

```
CREATE USER 'jeffrey'@'localhost' PASSWORD EXPIRE DEFAULT;
```

• PASSWORD EXPIRE NEVER

This expiration option overrides the global policy for all accounts named by the statement. For each, it disables password expiration so that the password never expires.

```
CREATE USER 'jeffrey'@'localhost' PASSWORD EXPIRE NEVER;
```

• PASSWORD EXPIRE INTERVAL N DAY

This expiration option overrides the global policy for all accounts named by the statement. For each, it sets the password lifetime to N days. The following statement requires the password to be changed every 180 days:

```
CREATE USER 'jeffrey'@'localhost' PASSWORD EXPIRE INTERVAL 180 DAY;
```

### <span id="page-102-1"></span>**CREATE USER Account-Locking Options**

MySQL supports account locking and unlocking using the ACCOUNT LOCK and ACCOUNT UNLOCK options, which specify the locking state for an account. For additional discussion, see Section 6.2.15, "Account Locking".

If multiple account-locking options are specified, the last one takes precedence.

# <span id="page-102-0"></span>**13.7.1.3 DROP USER Statement**

```
DROP USER [IF EXISTS] user [, user] ...
```

The [DROP USER](#page-102-0) statement removes one or more MySQL accounts and their privileges. It removes privilege rows for the account from all grant tables.

To use [DROP USER](#page-102-0), you must have the global CREATE USER privilege, or the DELETE privilege for the mysql system database. When the read\_only system variable is enabled, [DROP USER](#page-102-0) additionally requires the SUPER privilege.

An error occurs if you try to drop an account that does not exist. If the IF EXISTS clause is given, the statement produces a warning for each named user that does not exist, rather than an error.

Each account name uses the format described in Section 6.2.4, "Specifying Account Names". For example:

```
DROP USER 'jeffrey'@'localhost';
```

The host name part of the account name, if omitted, defaults to '%'.

![](_page_103_Picture_3.jpeg)

### **Important**

[DROP USER](#page-102-0) does not automatically close any open user sessions. Rather, in the event that a user with an open session is dropped, the statement does not take effect until that user's session is closed. Once the session is closed, the user is dropped, and that user's next attempt to log in fails. This is by design.

[DROP USER](#page-102-0) does not automatically drop or invalidate databases or objects within them that the old user created. This includes stored programs or views for which the DEFINER attribute names the dropped user. Attempts to access such objects may produce an error if they execute in definer security context. (For information about security context, see Section 23.6, "Stored Object Access Control".)

## <span id="page-103-0"></span>**13.7.1.4 GRANT Statement**

```
GRANT
 priv_type [(column_list)]
 [, priv_type [(column_list)]] ...
 ON [object_type] priv_level
 TO user [auth_option] [, user [auth_option]] ...
 [REQUIRE {NONE | tls_option [[AND] tls_option] ...}]
 [WITH {GRANT OPTION | resource_option} ...]
GRANT PROXY ON user
 TO user [, user] ...
 [WITH GRANT OPTION]
object_type: {
 TABLE
 | FUNCTION
 | PROCEDURE
}
priv_level: {
 *
 | *.*
 | db_name.*
 | db_name.tbl_name
 | tbl_name
 | db_name.routine_name
}
user:
 (see Section 6.2.4, "Specifying Account Names")
auth_option: {
 IDENTIFIED BY 'auth_string'
 | IDENTIFIED WITH auth_plugin
 | IDENTIFIED WITH auth_plugin BY 'auth_string'
 | IDENTIFIED WITH auth_plugin AS 'auth_string'
 | IDENTIFIED BY PASSWORD 'auth_string'
}
tls_option: {
 SSL
 | X509
 | CIPHER 'cipher'
 | ISSUER 'issuer'
 | SUBJECT 'subject'
}
resource_option: {
 | MAX_QUERIES_PER_HOUR count
 | MAX_UPDATES_PER_HOUR count
 | MAX_CONNECTIONS_PER_HOUR count
 | MAX_USER_CONNECTIONS count
```

}

The [GRANT](#page-103-0) statement grants privileges to MySQL user accounts. There are several aspects to the [GRANT](#page-103-0) statement, described under the following topics:

- [GRANT General Overview](#page-104-0)
- [Object Quoting Guidelines](#page-105-0)
- [Privileges Supported by MySQL](#page-107-0)
- [Account Names and Passwords](#page-109-0)
- [Global Privileges](#page-110-0)
- [Database Privileges](#page-110-1)
- [Table Privileges](#page-111-0)
- [Column Privileges](#page-111-1)
- [Stored Routine Privileges](#page-111-2)
- [Proxy User Privileges](#page-111-3)
- [Implicit Account Creation](#page-112-0)
- [Other Account Characteristics](#page-112-1)
- [MySQL and Standard SQL Versions of GRANT](#page-113-1)

### <span id="page-104-0"></span>**GRANT General Overview**

The [GRANT](#page-103-0) statement grants privileges to MySQL user accounts.

To grant a privilege with [GRANT](#page-103-0), you must have the GRANT OPTION privilege, and you must have the privileges that you are granting. (Alternatively, if you have the UPDATE privilege for the grant tables in the mysql system database, you can grant any account any privilege.) When the read\_only system variable is enabled, [GRANT](#page-103-0) additionally requires the SUPER privilege.

The [REVOKE](#page-114-0) statement is related to [GRANT](#page-103-0) and enables administrators to remove account privileges. See [Section 13.7.1.6, "REVOKE Statement"](#page-114-0).

Each account name uses the format described in Section 6.2.4, "Specifying Account Names". For example:

```
GRANT ALL ON db1.* TO 'jeffrey'@'localhost';
```

The host name part of the account, if omitted, defaults to '%'.

Normally, a database administrator first uses [CREATE USER](#page-95-0) to create an account and define its nonprivilege characteristics such as its password, whether it uses secure connections, and limits on access to server resources, then uses [GRANT](#page-103-0) to define its privileges. [ALTER USER](#page-89-0) may be used to change the nonprivilege characteristics of existing accounts. For example:

```
CREATE USER 'jeffrey'@'localhost' IDENTIFIED BY 'password';
GRANT ALL ON db1.* TO 'jeffrey'@'localhost';
GRANT SELECT ON db2.invoice TO 'jeffrey'@'localhost';
ALTER USER 'jeffrey'@'localhost' WITH MAX_QUERIES_PER_HOUR 90;
```

![](_page_104_Picture_25.jpeg)

#### **Note**

Examples shown here include no IDENTIFIED clause. It is assumed that you establish passwords with [CREATE USER](#page-95-0) at account-creation time to avoid creating insecure accounts.

![](_page_105_Picture_1.jpeg)

### **Note**

If an account named in a [GRANT](#page-103-0) statement does not already exist, [GRANT](#page-103-0) may create it under the conditions described later in the discussion of the NO\_AUTO\_CREATE\_USER SQL mode. It is also possible to use [GRANT](#page-103-0) to specify nonprivilege account characteristics such as whether it uses secure connections and limits on access to server resources.

However, use of [GRANT](#page-103-0) to create accounts or define nonprivilege characteristics is deprecated in MySQL 5.7. Instead, perform these tasks using [CREATE USER](#page-95-0) or [ALTER USER](#page-89-0).

From the mysql program, [GRANT](#page-103-0) responds with Query OK, 0 rows affected when executed successfully. To determine what privileges result from the operation, use [SHOW GRANTS](#page-154-0). See [Section 13.7.5.21, "SHOW GRANTS Statement".](#page-154-0)

![](_page_105_Picture_6.jpeg)

#### **Important**

Under some circumstances, [GRANT](#page-103-0) may be recorded in server logs or on the client side in a history file such as ~/.mysql\_history, which means that cleartext passwords may be read by anyone having read access to that information. For information about the conditions under which this occurs for the server logs and how to control it, see Section 6.1.2.3, "Passwords and Logging". For similar information about client-side logging, see Section 4.5.1.3, "mysql Client Logging".

[GRANT](#page-103-0) supports host names up to 60 characters long. User names can be up to 32 characters. Database, table, column, and routine names can be up to 64 characters.

![](_page_105_Picture_10.jpeg)

#### **Warning**

Do not attempt to change the permissible length for user names by altering the mysql.user system table. Doing so results in unpredictable behavior which may even make it impossible for users to log in to the MySQL server. Never alter the structure of tables in the mysql system database in any manner except by means of the procedure described in Section 2.10, "Upgrading MySQL".

### <span id="page-105-0"></span>**Object Quoting Guidelines**

Several objects within [GRANT](#page-103-0) statements are subject to quoting, although quoting is optional in many cases: Account, database, table, column, and routine names. For example, if a user\_name or host\_name value in an account name is legal as an unquoted identifier, you need not quote it. However, quotation marks are necessary to specify a user\_name string containing special characters (such as -), or a host\_name string containing special characters or wildcard characters such as % (for example, 'test-user'@'%.com'). Quote the user name and host name separately.

To specify quoted values:

- Quote database, table, column, and routine names as identifiers.
- Quote user names and host names as identifiers or as strings.
- Quote passwords as strings.

For string-quoting and identifier-quoting guidelines, see Section 9.1.1, "String Literals", and Section 9.2, "Schema Object Names".

The \_ and % wildcards are permitted when specifying database names in [GRANT](#page-103-0) statements that grant privileges at the database level (GRANT ... ON db\_name.\*). This means, for example, that to use

a \_ character as part of a database name, specify it using the \ escape character as \\_ in the [GRANT](#page-103-0) statement, to prevent the user from being able to access additional databases matching the wildcard pattern (for example, GRANT ... ON `foo\\_bar`.\* TO ...).

Issuing multiple GRANT statements containing wildcards may not have the expected effect on DML statements; when resolving grants involving wildcards, MySQL takes only the first matching grant into consideration. In other words, if a user has two database-level grants using wildcards that match the same database, the grant which was created first is applied. Consider the database db and table t created using the statements shown here:

```
mysql> CREATE DATABASE db;
Query OK, 1 row affected (0.01 sec)
mysql> CREATE TABLE db.t (c INT);
Query OK, 0 rows affected (0.01 sec)
mysql> INSERT INTO db.t VALUES ROW(1);
Query OK, 1 row affected (0.00 sec)
```

Next (assuming that the current account is the MySQL root account or another account having the necessary privileges), we create a user u then issue two GRANT statements containing wildcards, like this:

```
mysql> CREATE USER u;
Query OK, 0 rows affected (0.01 sec)
mysql> GRANT SELECT ON `d_`.* TO u;
Query OK, 0 rows affected (0.01 sec)
mysql> GRANT INSERT ON `d%`.* TO u;
Query OK, 0 rows affected (0.00 sec)
mysql> EXIT
Bye
```

If we end the session and then log in again with the mysql client, this time as u, we see that this account has only the privilege provided by the first matching grant, but not the second:

```
$> mysql -uu -hlocalhost
```

```
Welcome to the MySQL monitor. Commands end with ; or \g.
Your MySQL connection id is 10
Server version: 5.7.52-tr Source distribution
Copyright (c) 2000, 2023, Oracle and/or its affiliates.
Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.
Type 'help;' or '\h' for help. Type '\c' to clear the current input
statement.
mysql> TABLE db.t;
+------+
| c |
+------+
| 1 |
+------+
1 row in set (0.00 sec)
mysql> INSERT INTO db.t VALUES ROW(2);
ERROR 1142 (42000): INSERT command denied to user 'u'@'localhost' for table 't'
```

When a database name is not used to grant privileges at the database level, but as a qualifier for granting privileges to some other object such as a table or routine (for example, GRANT ... ON db\_name.tbl\_name), MySQL interprets wildcard characters as literal characters.

### <span id="page-107-0"></span>**Privileges Supported by MySQL**

The following table summarizes the permissible priv\_type privilege types that can be specified for the [GRANT](#page-103-0) and [REVOKE](#page-114-0) statements, and the levels at which each privilege can be granted. For additional information about each privilege, see Section 6.2.2, "Privileges Provided by MySQL".

**Table 13.8 Permissible Privileges for GRANT and REVOKE**

| Privilege               | Meaning and Grantable Levels                                                                                              |
|-------------------------|---------------------------------------------------------------------------------------------------------------------------|
| ALL [PRIVILEGES]        | Grant all privileges at specified access level<br>except GRANT OPTION and PROXY.                                          |
| ALTER                   | Enable use of ALTER TABLE. Levels: Global,<br>database, table.                                                            |
| ALTER ROUTINE           | Enable stored routines to be altered or dropped.<br>Levels: Global, database, routine.                                    |
| CREATE                  | Enable database and table creation. Levels:<br>Global, database, table.                                                   |
| CREATE ROUTINE          | Enable stored routine creation. Levels: Global,<br>database.                                                              |
| CREATE TABLESPACE       | Enable tablespaces and log file groups to be<br>created, altered, or dropped. Level: Global.                              |
| CREATE TEMPORARY TABLES | Enable use of CREATE TEMPORARY TABLE.<br>Levels: Global, database.                                                        |
| CREATE USER             | Enable use of CREATE USER, DROP USER,<br>RENAME USER, and REVOKE ALL PRIVILEGES.<br>Level: Global.                        |
| CREATE VIEW             | Enable views to be created or altered. Levels:<br>Global, database, table.                                                |
| DELETE                  | Enable use of DELETE. Level: Global, database,<br>table.                                                                  |
| DROP                    | Enable databases, tables, and views to be<br>dropped. Levels: Global, database, table.                                    |
| EVENT                   | Enable use of events for the Event Scheduler.<br>Levels: Global, database.                                                |
| EXECUTE                 | Enable the user to execute stored routines.<br>Levels: Global, database, routine.                                         |
| FILE                    | Enable the user to cause the server to read or<br>write files. Level: Global.                                             |
| GRANT OPTION            | Enable privileges to be granted to or removed<br>from other accounts. Levels: Global, database,<br>table, routine, proxy. |
| INDEX                   | Enable indexes to be created or dropped. Levels:<br>Global, database, table.                                              |
| INSERT                  | Enable use of INSERT. Levels: Global, database,<br>table, column.                                                         |
| LOCK TABLES             | Enable use of LOCK TABLES on tables for which<br>you have the SELECT privilege. Levels: Global,<br>database.              |
| PROCESS                 | Enable the user to see all processes with SHOW<br>PROCESSLIST. Level: Global.                                             |
| PROXY                   | Enable user proxying. Level: From user to user.                                                                           |

| Privilege          | Meaning and Grantable Levels                                                                                                                                       |
|--------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| REFERENCES         | Enable foreign key creation. Levels: Global,<br>database, table, column.                                                                                           |
| RELOAD             | Enable use of FLUSH operations. Level: Global.                                                                                                                     |
| REPLICATION CLIENT | Enable the user to ask where source or replica<br>servers are. Level: Global.                                                                                      |
| REPLICATION SLAVE  | Enable replicas to read binary log events from the<br>source. Level: Global.                                                                                       |
| SELECT             | Enable use of SELECT. Levels: Global, database,<br>table, column.                                                                                                  |
| SHOW DATABASES     | Enable SHOW DATABASES to show all databases.<br>Level: Global.                                                                                                     |
| SHOW VIEW          | Enable use of SHOW CREATE VIEW. Levels:<br>Global, database, table.                                                                                                |
| SHUTDOWN           | Enable use of mysqladmin shutdown. Level:<br>Global.                                                                                                               |
| SUPER              | Enable use of other administrative operations<br>such as CHANGE MASTER TO, KILL, PURGE<br>BINARY LOGS, SET GLOBAL, and mysqladmin<br>debug command. Level: Global. |
| TRIGGER            | Enable trigger operations. Levels: Global,<br>database, table.                                                                                                     |
| UPDATE             | Enable use of UPDATE. Levels: Global, database,<br>table, column.                                                                                                  |
| USAGE              | Synonym for "no privileges"                                                                                                                                        |

A trigger is associated with a table. To create or drop a trigger, you must have the TRIGGER privilege for the table, not the trigger.

In [GRANT](#page-103-0) statements, the ALL [PRIVILEGES] or PROXY privilege must be named by itself and cannot be specified along with other privileges. ALL [PRIVILEGES] stands for all privileges available for the level at which privileges are to be granted except for the GRANT OPTION and PROXY privileges.

USAGE can be specified to create a user that has no privileges, or to specify the REQUIRE or WITH clauses for an account without changing its existing privileges. (However, use of [GRANT](#page-103-0) to define nonprivilege characteristics is deprecated.

MySQL account information is stored in the tables of the mysql system database. For additional details, consult Section 6.2, "Access Control and Account Management", which discusses the mysql system database and the access control system extensively.

If the grant tables hold privilege rows that contain mixed-case database or table names and the lower\_case\_table\_names system variable is set to a nonzero value, [REVOKE](#page-114-0) cannot be used to revoke these privileges. It is necessary to manipulate the grant tables directly. ([GRANT](#page-103-0) does not create such rows when lower\_case\_table\_names is set, but such rows might have been created prior to setting that variable.)

Privileges can be granted at several levels, depending on the syntax used for the ON clause. For [REVOKE](#page-114-0), the same ON syntax specifies which privileges to remove.

For the global, database, table, and routine levels, [GRANT ALL](#page-103-0) assigns only the privileges that exist at the level you are granting. For example, GRANT ALL ON db\_name.\* is a database-level statement, so it does not grant any global-only privileges such as FILE. Granting ALL does not assign the GRANT OPTION or PROXY privilege.

The object\_type clause, if present, should be specified as TABLE, FUNCTION, or PROCEDURE when the following object is a table, a stored function, or a stored procedure.

The privileges that a user holds for a database, table, column, or routine are formed additively as the logical OR of the account privileges at each of the privilege levels, including the global level. It is not possible to deny a privilege granted at a higher level by absence of that privilege at a lower level. For example, this statement grants the SELECT and INSERT privileges globally:

```
GRANT SELECT, INSERT ON *.* TO u1;
```

The globally granted privileges apply to all databases, tables, and columns, even though not granted at any of those lower levels.

Details of the privilege-checking procedure are presented in Section 6.2.6, "Access Control, Stage 2: Request Verification".

If you are using table, column, or routine privileges for even one user, the server examines table, column, and routine privileges for all users and this slows down MySQL a bit. Similarly, if you limit the number of queries, updates, or connections for any users, the server must monitor these values.

MySQL enables you to grant privileges on databases or tables that do not exist. For tables, the privileges to be granted must include the CREATE privilege. This behavior is by design, and is intended to enable the database administrator to prepare user accounts and privileges for databases or tables that are to be created at a later time.

![](_page_109_Picture_8.jpeg)

### **Important**

MySQL does not automatically revoke any privileges when you drop a database or table. However, if you drop a routine, any routine-level privileges granted for that routine are revoked.

### <span id="page-109-0"></span>**Account Names and Passwords**

A user value in a [GRANT](#page-103-0) statement indicates a MySQL account to which the statement applies. To accommodate granting rights to users from arbitrary hosts, MySQL supports specifying the user value in the form 'user\_name'@'host\_name'.

You can specify wildcards in the host name. For example, 'user\_name'@'%.example.com' applies to user\_name for any host in the example.com domain, and 'user\_name'@'198.51.100.%' applies to user\_name for any host in the 198.51.100 class C subnet.

The simple form 'user\_name' is a synonym for 'user\_name'@'%'.

MySQL does not support wildcards in user names. To refer to an anonymous user, specify an account with an empty user name with the [GRANT](#page-103-0) statement:

```
GRANT ALL ON test.* TO ''@'localhost' ...;
```

In this case, any user who connects from the local host with the correct password for the anonymous user is permitted access, with the privileges associated with the anonymous user account.

For additional information about user name and host name values in account names, see Section 6.2.4, "Specifying Account Names".

![](_page_109_Picture_19.jpeg)

#### **Warning**

If you permit local anonymous users to connect to the MySQL server, you should also grant privileges to all local users as 'user\_name'@'localhost'. Otherwise, the anonymous user account for localhost in the mysql.user system table is used when named users try to log in to the MySQL server from the local machine. For details, see Section 6.2.5, "Access Control, Stage 1: Connection Verification".

To determine whether this issue applies to you, execute the following query, which lists any anonymous users:

```
SELECT Host, User FROM mysql.user WHERE User='';
```

To avoid the problem just described, delete the local anonymous user account using this statement:

```
DROP USER ''@'localhost';
```

For [GRANT](#page-103-0) syntax that permits an auth\_option value to follow a user value, auth\_option begins with IDENTIFIED and indicates how the account authenticates by specifying an account authentication plugin, credentials (for example, a password), or both. Syntax of the auth\_option clause is the same as for the [CREATE USER](#page-95-0) statement. For details, see [Section 13.7.1.2, "CREATE](#page-95-0) [USER Statement"](#page-95-0).

![](_page_110_Picture_6.jpeg)

#### **Note**

Use of [GRANT](#page-103-0) to define account authentication characteristics is deprecated in MySQL 5.7. Instead, establish or change authentication characteristics using [CREATE USER](#page-95-0) or [ALTER USER](#page-89-0). Expect this [GRANT](#page-103-0) capability to be removed in a future MySQL release.

When IDENTIFIED is present and you have the global grant privilege (GRANT OPTION), any password specified becomes the new password for the account, even if the account exists and already has a password. Without IDENTIFIED, the account password remains unchanged.

### <span id="page-110-0"></span>**Global Privileges**

Global privileges are administrative or apply to all databases on a given server. To assign global privileges, use ON \*.\* syntax:

```
GRANT ALL ON *.* TO 'someuser'@'somehost';
GRANT SELECT, INSERT ON *.* TO 'someuser'@'somehost';
```

The CREATE TABLESPACE, CREATE USER, FILE, PROCESS, RELOAD, REPLICATION CLIENT, REPLICATION SLAVE, SHOW DATABASES, SHUTDOWN, and SUPER privileges are administrative and can only be granted globally.

Other privileges can be granted globally or at more specific levels.

GRANT OPTION granted at the global level for any global privilege applies to all global privileges.

MySQL stores global privileges in the mysql.user system table.

### <span id="page-110-1"></span>**Database Privileges**

Database privileges apply to all objects in a given database. To assign database-level privileges, use ON db\_name.\* syntax:

```
GRANT ALL ON mydb.* TO 'someuser'@'somehost';
GRANT SELECT, INSERT ON mydb.* TO 'someuser'@'somehost';
```

If you use ON \* syntax (rather than ON \*.\*), privileges are assigned at the database level for the default database. An error occurs if there is no default database.

The CREATE, DROP, EVENT, GRANT OPTION, LOCK TABLES, and REFERENCES privileges can be specified at the database level. Table or routine privileges also can be specified at the database level, in which case they apply to all tables or routines in the database.

MySQL stores database privileges in the mysql.db system table.

### <span id="page-111-0"></span>**Table Privileges**

Table privileges apply to all columns in a given table. To assign table-level privileges, use ON db\_name.tbl\_name syntax:

```
GRANT ALL ON mydb.mytbl TO 'someuser'@'somehost';
GRANT SELECT, INSERT ON mydb.mytbl TO 'someuser'@'somehost';
```

If you specify tbl\_name rather than db\_name.tbl\_name, the statement applies to tbl\_name in the default database. An error occurs if there is no default database.

The permissible priv\_type values at the table level are ALTER, CREATE VIEW, CREATE, DELETE, DROP, GRANT OPTION, INDEX, INSERT, REFERENCES, SELECT, SHOW VIEW, TRIGGER, and UPDATE.

Table-level privileges apply to base tables and views. They do not apply to tables created with CREATE TEMPORARY TABLE, even if the table names match. For information about TEMPORARY table privileges, see Section 13.1.18.2, "CREATE TEMPORARY TABLE Statement".

MySQL stores table privileges in the mysql.tables\_priv system table.

### <span id="page-111-1"></span>**Column Privileges**

Column privileges apply to single columns in a given table. Each privilege to be granted at the column level must be followed by the column or columns, enclosed within parentheses.

```
GRANT SELECT (col1), INSERT (col1, col2) ON mydb.mytbl TO 'someuser'@'somehost';
```

The permissible priv\_type values for a column (that is, when you use a column\_list clause) are INSERT, REFERENCES, SELECT, and UPDATE.

MySQL stores column privileges in the mysql.columns\_priv system table.

### <span id="page-111-2"></span>**Stored Routine Privileges**

The ALTER ROUTINE, CREATE ROUTINE, EXECUTE, and GRANT OPTION privileges apply to stored routines (procedures and functions). They can be granted at the global and database levels. Except for CREATE ROUTINE, these privileges can be granted at the routine level for individual routines.

```
GRANT CREATE ROUTINE ON mydb.* TO 'someuser'@'somehost';
GRANT EXECUTE ON PROCEDURE mydb.myproc TO 'someuser'@'somehost';
```

The permissible priv\_type values at the routine level are ALTER ROUTINE, EXECUTE, and GRANT OPTION. CREATE ROUTINE is not a routine-level privilege because you must have the privilege at the global or database level to create a routine in the first place.

MySQL stores routine-level privileges in the mysql.procs\_priv system table.

### <span id="page-111-3"></span>**Proxy User Privileges**

The PROXY privilege enables one user to be a proxy for another. The proxy user impersonates or takes the identity of the proxied user; that is, it assumes the privileges of the proxied user.

```
GRANT PROXY ON 'localuser'@'localhost' TO 'externaluser'@'somehost';
```

When PROXY is granted, it must be the only privilege named in the [GRANT](#page-103-0) statement, the REQUIRE clause cannot be given, and the only permitted WITH option is WITH GRANT OPTION.

Proxying requires that the proxy user authenticate through a plugin that returns the name of the proxied user to the server when the proxy user connects, and that the proxy user have the PROXY privilege for the proxied user. For details and examples, see Section 6.2.14, "Proxy Users".

MySQL stores proxy privileges in the mysql.proxies\_priv system table.

### <span id="page-112-0"></span>**Implicit Account Creation**

If an account named in a [GRANT](#page-103-0) statement does not exist, the action taken depends on the NO\_AUTO\_CREATE\_USER SQL mode:

- If NO\_AUTO\_CREATE\_USER is not enabled, [GRANT](#page-103-0) creates the account. This is very insecure unless you specify a nonempty password using IDENTIFIED BY.
- If NO\_AUTO\_CREATE\_USER is enabled, [GRANT](#page-103-0) fails and does not create the account, unless you specify a nonempty password using IDENTIFIED BY or name an authentication plugin using IDENTIFIED WITH.

If the account already exists, IDENTIFIED WITH is prohibited because it is intended only for use when creating new accounts.

### <span id="page-112-1"></span>**Other Account Characteristics**

MySQL can check X.509 certificate attributes in addition to the usual authentication that is based on the user name and credentials. For background information on the use of SSL with MySQL, see Section 6.3, "Using Encrypted Connections".

The optional REQUIRE clause specifies SSL-related options for a MySQL account. The syntax is the same as for the [CREATE USER](#page-95-0) statement. For details, see [Section 13.7.1.2, "CREATE USER](#page-95-0) [Statement".](#page-95-0)

![](_page_112_Picture_9.jpeg)

#### **Note**

Use of [GRANT](#page-103-0) to define account SSL characteristics is deprecated in MySQL 5.7. Instead, establish or change SSL characteristics using [CREATE USER](#page-95-0) or [ALTER USER](#page-89-0). Expect this [GRANT](#page-103-0) capability to be removed in a future MySQL release.

The optional WITH clause is used for these purposes:

- To enable a user to grant privileges to other users
- To specify resource limits for a user

The WITH GRANT OPTION clause gives the user the ability to give to other users any privileges the user has at the specified privilege level.

To grant the GRANT OPTION privilege to an account without otherwise changing its privileges, do this:

```
GRANT USAGE ON *.* TO 'someuser'@'somehost' WITH GRANT OPTION;
```

Be careful to whom you give the GRANT OPTION privilege because two users with different privileges may be able to combine privileges!

You cannot grant another user a privilege which you yourself do not have; the GRANT OPTION privilege enables you to assign only those privileges which you yourself possess.

Be aware that when you grant a user the GRANT OPTION privilege at a particular privilege level, any privileges the user possesses (or may be given in the future) at that level can also be granted by that user to other users. Suppose that you grant a user the INSERT privilege on a database. If you then grant the SELECT privilege on the database and specify WITH GRANT OPTION, that user can give to other users not only the SELECT privilege, but also INSERT. If you then grant the UPDATE privilege to the user on the database, the user can grant INSERT, SELECT, and UPDATE.

For a nonadministrative user, you should not grant the ALTER privilege globally or for the mysql system database. If you do that, the user can try to subvert the privilege system by renaming tables!

For additional information about security risks associated with particular privileges, see Section 6.2.2, "Privileges Provided by MySQL".

It is possible to place limits on use of server resources by an account, as discussed in Section 6.2.16, "Setting Account Resource Limits". To do so, use a WITH clause that specifies one or more resource\_option values. Limits not specified retain their current values. The syntax is the same as for the [CREATE USER](#page-95-0) statement. For details, see [Section 13.7.1.2, "CREATE USER Statement"](#page-95-0).

![](_page_113_Picture_2.jpeg)

### **Note**

Use of [GRANT](#page-103-0) to define account resource limits is deprecated in MySQL 5.7. Instead, establish or change resource limits using [CREATE USER](#page-95-0) or [ALTER](#page-89-0) [USER](#page-89-0). Expect this [GRANT](#page-103-0) capability to be removed in a future MySQL release.

### <span id="page-113-1"></span>**MySQL and Standard SQL Versions of GRANT**

The biggest differences between the MySQL and standard SQL versions of [GRANT](#page-103-0) are:

- MySQL associates privileges with the combination of a host name and user name and not with only a user name.
- Standard SQL does not have global or database-level privileges, nor does it support all the privilege types that MySQL supports.
- MySQL does not support the standard SQL UNDER privilege.
- Standard SQL privileges are structured in a hierarchical manner. If you remove a user, all privileges the user has been granted are revoked. This is also true in MySQL if you use [DROP USER](#page-102-0). See [Section 13.7.1.3, "DROP USER Statement"](#page-102-0).
- In standard SQL, when you drop a table, all privileges for the table are revoked. In standard SQL, when you revoke a privilege, all privileges that were granted based on that privilege are also revoked. In MySQL, privileges can be dropped with [DROP USER](#page-102-0) or [REVOKE](#page-114-0) statements.
- In MySQL, it is possible to have the INSERT privilege for only some of the columns in a table. In this case, you can still execute INSERT statements on the table, provided that you insert values only for those columns for which you have the INSERT privilege. The omitted columns are set to their implicit default values if strict SQL mode is not enabled. In strict mode, the statement is rejected if any of the omitted columns have no default value. (Standard SQL requires you to have the INSERT privilege on all columns.) For information about strict SQL mode and implicit default values, see Section 5.1.10, "Server SQL Modes", and Section 11.6, "Data Type Default Values".

## <span id="page-113-0"></span>**13.7.1.5 RENAME USER Statement**

```
RENAME USER old_user TO new_user
 [, old_user TO new_user] ...
```

The [RENAME USER](#page-113-0) statement renames existing MySQL accounts. An error occurs for old accounts that do not exist or new accounts that already exist.

To use [RENAME USER](#page-113-0), you must have the global CREATE USER privilege, or the UPDATE privilege for the mysql system database. When the read\_only system variable is enabled, [RENAME USER](#page-113-0) additionally requires the SUPER privilege.

Each account name uses the format described in Section 6.2.4, "Specifying Account Names". For example:

```
RENAME USER 'jeffrey'@'localhost' TO 'jeff'@'127.0.0.1';
```

The host name part of the account name, if omitted, defaults to '%'.

[RENAME USER](#page-113-0) causes the privileges held by the old user to be those held by the new user. However, [RENAME USER](#page-113-0) does not automatically drop or invalidate databases or objects within them that the old user created. This includes stored programs or views for which the DEFINER attribute names the old user. Attempts to access such objects may produce an error if they execute in definer security context. (For information about security context, see Section 23.6, "Stored Object Access Control".)

The privilege changes take effect as indicated in Section 6.2.9, "When Privilege Changes Take Effect".

# <span id="page-114-0"></span>**13.7.1.6 REVOKE Statement**

```
REVOKE
 priv_type [(column_list)]
 [, priv_type [(column_list)]] ...
 ON [object_type] priv_level
 FROM user [, user] ...
REVOKE ALL [PRIVILEGES], GRANT OPTION
 FROM user [, user] ...
REVOKE PROXY ON user
 FROM user [, user] ...
```

The [REVOKE](#page-114-0) statement enables system administrators to revoke privileges from MySQL accounts.

For details on the levels at which privileges exist, the permissible priv\_type, priv\_level, and object\_type values, and the syntax for specifying users and passwords, see [Section 13.7.1.4,](#page-103-0) ["GRANT Statement"](#page-103-0).

When the read\_only system variable is enabled, [REVOKE](#page-114-0) requires the SUPER privilege in addition to any other required privileges described in the following discussion.

Each account name uses the format described in Section 6.2.4, "Specifying Account Names". For example:

```
REVOKE INSERT ON *.* FROM 'jeffrey'@'localhost';
```

The host name part of the account name, if omitted, defaults to '%'.

To use the first [REVOKE](#page-114-0) syntax, you must have the GRANT OPTION privilege, and you must have the privileges that you are revoking.

To revoke all privileges, use the second syntax, which drops all global, database, table, column, and routine privileges for the named user or users:

```
REVOKE ALL PRIVILEGES, GRANT OPTION FROM user [, user] ...
```

To use this [REVOKE](#page-114-0) syntax, you must have the global CREATE USER privilege, or the UPDATE privilege for the mysql system database.

User accounts from which privileges are to be revoked must exist, but the privileges to be revoked need not be currently granted to them.

[REVOKE](#page-114-0) removes privileges, but does not remove rows from the mysql.user system table. To remove a user account entirely, use [DROP USER](#page-102-0). See [Section 13.7.1.3, "DROP USER Statement"](#page-102-0).

If the grant tables hold privilege rows that contain mixed-case database or table names and the lower\_case\_table\_names system variable is set to a nonzero value, [REVOKE](#page-114-0) cannot be used to revoke these privileges. It is necessary to manipulate the grant tables directly. ([GRANT](#page-103-0) does not create such rows when lower\_case\_table\_names is set, but such rows might have been created prior to setting the variable.)

When successfully executed from the mysql program, [REVOKE](#page-114-0) responds with Query OK, 0 rows affected. To determine what privileges remain after the operation, use [SHOW GRANTS](#page-154-0). See [Section 13.7.5.21, "SHOW GRANTS Statement".](#page-154-0)

# <span id="page-114-1"></span>**13.7.1.7 SET PASSWORD Statement**

```
SET PASSWORD [FOR user] = password_option
password_option: {
 'auth_string'
 | PASSWORD('auth_string')
```

}

The [SET PASSWORD](#page-114-1) statement assigns a password to a MySQL user account. 'auth\_string' represents a cleartext (unencrypted) password.

![](_page_115_Picture_3.jpeg)

#### **Note**

- [SET PASSWORD ... = PASSWORD\('](#page-114-1)auth\_string') syntax is deprecated in MySQL 5.7 and is removed in MySQL 8.0.
- [SET PASSWORD ... = '](#page-114-1)auth\_string' syntax is not deprecated, but [ALTER USER](#page-89-0) is the preferred statement for account alterations, including assigning passwords. For example:

ALTER USER user IDENTIFIED BY 'auth\_string';

![](_page_115_Picture_8.jpeg)

#### **Important**

Under some circumstances, [SET PASSWORD](#page-114-1) may be recorded in server logs or on the client side in a history file such as ~/.mysql\_history, which means that cleartext passwords may be read by anyone having read access to that information. For information about the conditions under which this occurs for the server logs and how to control it, see Section 6.1.2.3, "Passwords and Logging". For similar information about client-side logging, see Section 4.5.1.3, "mysql Client Logging".

[SET PASSWORD](#page-114-1) can be used with or without a FOR clause that explicitly names a user account:

• With a FOR user clause, the statement sets the password for the named account, which must exist:

```
SET PASSWORD FOR 'jeffrey'@'localhost' = 'auth_string';
```

• With no FOR user clause, the statement sets the password for the current user:

```
SET PASSWORD = 'auth_string';
```

Any client who connects to the server using a nonanonymous account can change the password for that account. (In particular, you can change your own password.) To see which account the server authenticated you as, invoke the CURRENT\_USER() function:

```
SELECT CURRENT_USER();
```

If a FOR user clause is given, the account name uses the format described in Section 6.2.4, "Specifying Account Names". For example:

```
SET PASSWORD FOR 'bob'@'%.example.org' = 'auth_string';
```

The host name part of the account name, if omitted, defaults to '%'.

Setting the password for a named account (with a FOR clause) requires the UPDATE privilege for the mysql system database. Setting the password for yourself (for a nonanonymous account with no FOR clause) requires no special privileges. When the read\_only system variable is enabled, [SET](#page-114-1) [PASSWORD](#page-114-1) requires the SUPER privilege in addition to any other required privileges.

The password can be specified in these ways:

• Use a string without PASSWORD()

```
SET PASSWORD FOR 'jeffrey'@'localhost' = 'password';
```

[SET PASSWORD](#page-114-1) interprets the string as a cleartext string, passes it to the authentication plugin associated with the account, and stores the result returned by the plugin in the account row in the mysql.user system table. (The plugin is given the opportunity to hash the value into the encryption format it expects. The plugin may use the value as specified, in which case no hashing occurs.)

• Use the PASSWORD() function (deprecated in MySQL 5.7)

```
SET PASSWORD FOR 'jeffrey'@'localhost' = PASSWORD('password');
```

The PASSWORD() argument is the cleartext (unencrypted) password. PASSWORD() hashes the password and returns the encrypted password string for storage in the account row in the mysql.user system table.

The PASSWORD() function hashes the password using the hashing method determined by the value of the old\_passwords system variable value. Be sure that old\_passwords has the value corresponding to the hashing method expected by the authentication plugin associated with the account. For example, if the account uses the mysql\_native\_password plugin, the old\_passwords value must be 0:

```
SET old_passwords = 0;
SET PASSWORD FOR 'jeffrey'@'localhost' = PASSWORD('password');
```

If the old\_passwords value differs from that required by the authentication plugin, the hashed password value returned by PASSWORD() cannot be used by the plugin and correct authentication of client connections cannot occur.

The following table shows, for each password hashing method, the permitted value of old\_passwords and which authentication plugins use the hashing method.

| Password Hashing Method  | old_passwords Value | Associated Authentication<br>Plugin |
|--------------------------|---------------------|-------------------------------------|
| MySQL 4.1 native hashing | 0                   | mysql_native_password               |
| SHA-256 hashing          | 2                   | sha256_password                     |

For additional information about setting passwords and authentication plugins, see Section 6.2.10, "Assigning Account Passwords", and Section 6.2.13, "Pluggable Authentication".