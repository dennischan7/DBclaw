---
source: MySQL 8.0 Reference
title: 00_Overview
---

MySQL account information is stored in the tables of the mysql system schema. This database and the access control system are discussed extensively in Chapter 7, MySQL Server Administration, which you should consult for additional details.

![](_page_14_Picture_8.jpeg)

#### **Important**

Some MySQL releases introduce changes to the grant tables to add new privileges or features. To make sure that you can take advantage of any new capabilities, update your grant tables to the current structure whenever you upgrade MySQL. See Chapter 3, Upgrading MySQL.

When the read\_only system variable is enabled, account-management statements require the CONNECTION\_ADMIN privilege (or the deprecated SUPER privilege), in addition to any other required privileges. This is because they modify tables in the mysql system schema.

Account management statements are atomic and crash safe. For more information, see Section 15.1.1, "Atomic Data Definition Statement Support".

## <span id="page-14-0"></span>**15.7.1.1 ALTER USER Statement**

```
ALTER USER [IF EXISTS]
 user [auth_option] [, user [auth_option]] ...
 [REQUIRE {NONE | tls_option [[AND] tls_option] ...}]
 [WITH resource_option [resource_option] ...]
 [password_option | lock_option] ...
 [COMMENT 'comment_string' | ATTRIBUTE 'json_object']
ALTER USER [IF EXISTS]
 USER() user_func_auth_option
ALTER USER [IF EXISTS]
 user [registration_option]
ALTER USER [IF EXISTS]
 USER() [registration_option]
ALTER USER [IF EXISTS]
 user DEFAULT ROLE
 {NONE | ALL | role [, role ] ...}
user:
 (see Section 8.2.4, "Specifying Account Names")
auth_option: {
 IDENTIFIED BY 'auth_string'
 [REPLACE 'current_auth_string']
 [RETAIN CURRENT PASSWORD]
 | IDENTIFIED BY RANDOM PASSWORD
 [REPLACE 'current_auth_string']
 [RETAIN CURRENT PASSWORD]
 | IDENTIFIED WITH auth_plugin
```

```
 | IDENTIFIED WITH auth_plugin BY 'auth_string'
 [REPLACE 'current_auth_string']
 [RETAIN CURRENT PASSWORD]
 | IDENTIFIED WITH auth_plugin BY RANDOM PASSWORD
 [REPLACE 'current_auth_string']
 [RETAIN CURRENT PASSWORD]
 | IDENTIFIED WITH auth_plugin AS 'auth_string'
 | DISCARD OLD PASSWORD
 | ADD factor factor_auth_option [ADD factor factor_auth_option]
 | MODIFY factor factor_auth_option [MODIFY factor factor_auth_option]
 | DROP factor [DROP factor]
}
user_func_auth_option: {
 IDENTIFIED BY 'auth_string'
 [REPLACE 'current_auth_string']
 [RETAIN CURRENT PASSWORD]
 | DISCARD OLD PASSWORD
}
factor_auth_option: {
 IDENTIFIED BY 'auth_string'
 | IDENTIFIED BY RANDOM PASSWORD
 | IDENTIFIED WITH auth_plugin BY 'auth_string'
 | IDENTIFIED WITH auth_plugin BY RANDOM PASSWORD
 | IDENTIFIED WITH auth_plugin AS 'auth_string'
}
registration_option: {
 factor INITIATE REGISTRATION
 | factor FINISH REGISTRATION SET CHALLENGE_RESPONSE AS 'auth_string'
 | factor UNREGISTER
}
factor: {2 | 3} FACTOR
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
 PASSWORD EXPIRE [DEFAULT | NEVER | INTERVAL N DAY]
 | PASSWORD HISTORY {DEFAULT | N}
 | PASSWORD REUSE INTERVAL {DEFAULT | N DAY}
 | PASSWORD REQUIRE CURRENT [DEFAULT | OPTIONAL]
 | FAILED_LOGIN_ATTEMPTS N
 | PASSWORD_LOCK_TIME {N | UNBOUNDED}
}
lock_option: {
 ACCOUNT LOCK
 | ACCOUNT UNLOCK
}
```

The [ALTER USER](#page-14-0) statement modifies MySQL accounts. It enables authentication, role, SSL/TLS, resource-limit, password-management, comment, and attribute properties to be modified for existing accounts. It can also be used to lock and unlock accounts.

In most cases, [ALTER USER](#page-14-0) requires the global CREATE USER privilege, or the UPDATE privilege for the mysql system schema. The exceptions are:

• Any client who connects to the server using a nonanonymous account can change the password for that account. (In particular, you can change your own password.) To see which account the server authenticated you as, invoke the CURRENT\_USER() function:

SELECT CURRENT\_USER();

- For DEFAULT ROLE syntax, [ALTER USER](#page-14-0) requires these privileges:
  - Setting the default roles for another user requires the global CREATE USER privilege, or the UPDATE privilege for the mysql.default\_roles system table.
  - Setting the default roles for yourself requires no special privileges, as long as the roles you want as the default have been granted to you.
- Statements that modify secondary passwords require these privileges:
  - The APPLICATION\_PASSWORD\_ADMIN privilege is required to use the RETAIN CURRENT PASSWORD or DISCARD OLD PASSWORD clause for [ALTER USER](#page-14-0) statements that apply to your own account. The privilege is required to manipulate your own secondary password because most users require only one password.
  - If an account is to be permitted to manipulate secondary passwords for all accounts, it requires the CREATE USER privilege rather than APPLICATION\_PASSWORD\_ADMIN.

When the read\_only system variable is enabled, [ALTER USER](#page-14-0) additionally requires the CONNECTION\_ADMIN privilege (or the deprecated SUPER privilege).

As of MySQL 8.0.27, these additional privilege considerations apply:

- The authentication\_policy system variable places certain constraints on how the authentication-related clauses of [ALTER USER](#page-14-0) statements may be used; for details, see the description of that variable. These constraints do not apply if you have the AUTHENTICATION\_POLICY\_ADMIN privilege.
- To modify an account that uses passwordless authentication, you must have the PASSWORDLESS\_USER\_ADMIN privilege.

By default, an error occurs if you try to modify a user that does not exist. If the IF EXISTS clause is given, the statement produces a warning for each named user that does not exist, rather than an error.

![](_page_16_Picture_14.jpeg)

#### **Important**

Under some circumstances, [ALTER USER](#page-14-0) may be recorded in server logs or on the client side in a history file such as ~/.mysql\_history, which means that cleartext passwords may be read by anyone having read access to that information. For information about the conditions under which this occurs for the server logs and how to control it, see Section 8.1.2.3, "Passwords and Logging". For similar information about client-side logging, see Section 6.5.1.3, "mysql Client Logging".

There are several aspects to the [ALTER USER](#page-14-0) statement, described under the following topics:

- [ALTER USER Overview](#page-17-0)
- [ALTER USER Authentication Options](#page-18-0)
- [ALTER USER Multifactor Authentication Options](#page-22-0)
- [ALTER USER Registration Options](#page-22-1)
- [ALTER USER Role Options](#page-22-2)
- [ALTER USER SSL/TLS Options](#page-23-0)

- [ALTER USER Resource-Limit Options](#page-24-0)
- [ALTER USER Password-Management Options](#page-25-0)
- [ALTER USER Comment and Attribute Options](#page-28-0)
- [ALTER USER Account-Locking Options](#page-29-0)
- [ALTER USER Binary Logging](#page-29-1)

## <span id="page-17-0"></span>**ALTER USER Overview**

For each affected account, [ALTER USER](#page-14-0) modifies the corresponding row in the mysql.user system table to reflect the properties specified in the statement. Unspecified properties retain their current values.

Each account name uses the format described in Section 8.2.4, "Specifying Account Names". The host name part of the account name, if omitted, defaults to '%'. It is also possible to specify CURRENT\_USER or CURRENT\_USER() to refer to the account associated with the current session.

In one case only, the account may be specified with the USER() function:

```
ALTER USER USER() IDENTIFIED BY 'auth_string';
```

This syntax enables changing your own password without naming your account literally. (The syntax also supports the REPLACE, RETAIN CURRENT PASSWORD, and DISCARD OLD PASSWORD clauses described at [ALTER USER Authentication Options](#page-18-0).)

For [ALTER USER](#page-14-0) syntax that permits an auth\_option value to follow a user value, auth\_option indicates how the account authenticates by specifying an account authentication plugin, credentials (for example, a password), or both. Each auth\_option value applies only to the account named immediately preceding it.

Following the user specifications, the statement may include options for SSL/TLS, resource-limit, password-management, and locking properties. All such options are global to the statement and apply to all accounts named in the statement.

Example: Change an account's password and expire it. As a result, the user must connect with the named password and choose a new one at the next connection:

```
ALTER USER 'jeffrey'@'localhost'
 IDENTIFIED BY 'new_password' PASSWORD EXPIRE;
```

Example: Modify an account to use the caching\_sha2\_password authentication plugin and the given password. Require that a new password be chosen every 180 days, and enable failed-login tracking, such that three consecutive incorrect passwords cause temporary account locking for two days:

```
ALTER USER 'jeffrey'@'localhost'
 IDENTIFIED WITH caching_sha2_password BY 'new_password'
 PASSWORD EXPIRE INTERVAL 180 DAY
 FAILED_LOGIN_ATTEMPTS 3 PASSWORD_LOCK_TIME 2;
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
 'jeffrey'@'localhost'
 IDENTIFIED BY 'jeffrey_new_password',
 'jeanne'@'localhost',
 'josh'@'localhost'
 IDENTIFIED BY 'josh_new_password'
 REPLACE 'josh_current_password'
 RETAIN CURRENT PASSWORD
 REQUIRE SSL WITH MAX_USER_CONNECTIONS 2
 PASSWORD HISTORY 5;
```

The IDENTIFIED BY value following jeffrey applies only to its immediately preceding account, so it changes the password to 'jeffrey\_new\_password' only for jeffrey. For jeanne, there is no per-account value (thus leaving the password unchanged). For josh, IDENTIFIED BY establishes a new password ('josh\_new\_password'), REPLACE is specified to verify that the user issuing the [ALTER USER](#page-14-0) statement knows the current password ('josh\_current\_password'), and that current password is also retained as the account secondary password. (As a result, josh can connect with either the primary or secondary password.)

The remaining properties apply globally to all accounts named in the statement, so for both accounts:

- Connections are required to use SSL.
- The account can be used for a maximum of two simultaneous connections.
- Password changes cannot reuse any of the five most recent passwords.

Example: Discard the secondary password for josh, leaving the account with only its primary password:

```
ALTER USER 'josh'@'localhost' DISCARD OLD PASSWORD;
```

In the absence of a particular type of option, the account remains unchanged in that respect. For example, with no locking option, the locking state of the account is not changed.

## <span id="page-18-0"></span>**ALTER USER Authentication Options**

An account name may be followed by an auth\_option authentication option that specifies the account authentication plugin, credentials, or both. It may also include a password-verification clause that specifies the account current password to be replaced, and clauses that manage whether an account has a secondary password.

![](_page_18_Picture_12.jpeg)

## **Note**

Clauses for random password generation, password verification, and secondary passwords apply only to accounts that use an authentication plugin that stores credentials internally to MySQL. For accounts that use a plugin that performs authentication against a credentials system that is external to MySQL, password management must be handled externally against that system as well. For more information about internal credentials storage, see Section 8.2.15, "Password Management".

• auth\_plugin names an authentication plugin. The plugin name can be a quoted string literal or an unquoted name. Plugin names are stored in the plugin column of the mysql.user system table.

For auth\_option syntax that does not specify an authentication plugin, the server assigns the default plugin, determined as described in The Default Authentication Plugin. For descriptions of each plugin, see Section 8.4.1, "Authentication Plugins".

• Credentials that are stored internally are stored in the mysql.user system table. An 'auth\_string' value or RANDOM PASSWORD specifies account credentials, either as a cleartext (unencrypted) string or hashed in the format expected by the authentication plugin associated with the account, respectively:

- For syntax that uses BY 'auth\_string', the string is cleartext and is passed to the authentication plugin for possible hashing. The result returned by the plugin is stored in the mysql.user table. A plugin may use the value as specified, in which case no hashing occurs.
- For syntax that uses BY RANDOM PASSWORD, MySQL generates a random password and as cleartext and passes it to the authentication plugin for possible hashing. The result returned by the plugin is stored in the mysql.user table. A plugin may use the value as specified, in which case no hashing occurs.

Randomly generated passwords are available as of MySQL 8.0.18 and have the characteristics described in Random Password Generation.

• For syntax that uses AS 'auth\_string', the string is assumed to be already in the format the authentication plugin requires, and is stored as is in the mysql.user table. If a plugin requires a hashed value, the value must be already hashed in a format appropriate for the plugin; otherwise, the value cannot be used by the plugin and correct authentication of client connections does not occur.

As of MySQL 8.0.17, a hashed string can be either a string literal or a hexadecimal value. The latter corresponds to the type of value displayed by [SHOW CREATE USER](#page-105-0) for password hashes containing unprintable characters when the print\_identified\_with\_as\_hex system variable is enabled.

- If an authentication plugin performs no hashing of the authentication string, the BY 'auth\_string' and AS 'auth\_string' clauses have the same effect: The authentication string is stored as is in the mysql.user system table.
- The REPLACE 'current\_auth\_string' clause performs password verification and is available as of MySQL 8.0.13. If given:
  - REPLACE specifies the account current password to be replaced, as a cleartext (unencrypted) string.
  - The clause must be given if password changes for the account are required to specify the current password, as verification that the user attempting to make the change actually knows the current password.
  - The clause is optional if password changes for the account may but need not specify the current password.
  - The statement fails if the clause is given but does not match the current password, even if the clause is optional.
  - REPLACE can be specified only when changing the account password for the current user.

For more information about password verification by specifying the current password, see Section 8.2.15, "Password Management".

- The RETAIN CURRENT PASSWORD and DISCARD OLD PASSWORD clauses implement dualpassword capability and are available as of MySQL 8.0.14. Both are optional, but if given, have the following effects:
  - RETAIN CURRENT PASSWORD retains an account current password as its secondary password, replacing any existing secondary password. The new password becomes the primary password, but clients can use the account to connect to the server using either the primary or secondary password. (Exception: If the new password specified by the [ALTER USER](#page-14-0) statement is empty, the secondary password becomes empty as well, even if RETAIN CURRENT PASSWORD is given.)
  - If you specify RETAIN CURRENT PASSWORD for an account that has an empty primary password, the statement fails.

- If an account has a secondary password and you change its primary password without specifying RETAIN CURRENT PASSWORD, the secondary password remains unchanged.
- If you change the authentication plugin assigned to the account, the secondary password is discarded. If you change the authentication plugin and also specify RETAIN CURRENT PASSWORD, the statement fails.
- DISCARD OLD PASSWORD discards the secondary password, if one exists. The account retains only its primary password, and clients can use the account to connect to the server only with the primary password.

For more information about use of dual passwords, see Section 8.2.15, "Password Management".

[ALTER USER](#page-14-0) permits these auth\_option syntaxes:

• IDENTIFIED BY 'auth\_string' [REPLACE 'current\_auth\_string'] [RETAIN CURRENT PASSWORD]

Sets the account authentication plugin to the default plugin, passes the cleartext 'auth\_string' value to the plugin for possible hashing, and stores the result in the account row in the mysql.user system table.

The REPLACE clause, if given, specifies the account current password, as described previously in this section.

The RETAIN CURRENT PASSWORD clause, if given, causes the account current password to be retained as its secondary password, as described previously in this section.

• IDENTIFIED BY RANDOM PASSWORD [REPLACE 'current\_auth\_string'] [RETAIN CURRENT PASSWORD]

Sets the account authentication plugin to the default plugin, generates a random password, passes the cleartext password value to the plugin for possible hashing, and stores the result in the account row in the mysql.user system table. The statement also returns the cleartext password in a result set to make it available to the user or application executing the statement. For details about the result set and characteristics of randomly generated passwords, see Random Password Generation.

The REPLACE clause, if given, specifies the account current password, as described previously in this section.

The RETAIN CURRENT PASSWORD clause, if given, causes the account current password to be retained as its secondary password, as described previously in this section.

• IDENTIFIED WITH auth\_plugin

Sets the account authentication plugin to auth\_plugin, clears the credentials to the empty string (the credentials are associated with the old authentication plugin, not the new one), and stores the result in the account row in the mysql.user system table.

In addition, the password is marked expired. The user must choose a new one when next connecting.

• IDENTIFIED WITH auth\_plugin BY 'auth\_string' [REPLACE 'current\_auth\_string'] [RETAIN CURRENT PASSWORD]

Sets the account authentication plugin to auth\_plugin, passes the cleartext 'auth\_string' value to the plugin for possible hashing, and stores the result in the account row in the mysql.user system table.

The REPLACE clause, if given, specifies the account current password, as described previously in this section.

The RETAIN CURRENT PASSWORD clause, if given, causes the account current password to be retained as its secondary password, as described previously in this section.

• IDENTIFIED WITH auth\_plugin BY RANDOM PASSWORD [REPLACE 'current\_auth\_string'] [RETAIN CURRENT PASSWORD]

Sets the account authentication plugin to auth\_plugin, generates a random password, passes the cleartext password value to the plugin for possible hashing, and stores the result in the account row in the mysql.user system table. The statement also returns the cleartext password in a result set to make it available to the user or application executing the statement. For details about the result set and characteristics of randomly generated passwords, see Random Password Generation.

The REPLACE clause, if given, specifies the account current password, as described previously in this section.

The RETAIN CURRENT PASSWORD clause, if given, causes the account current password to be retained as its secondary password, as described previously in this section.

• IDENTIFIED WITH auth\_plugin AS 'auth\_string'

Sets the account authentication plugin to auth\_plugin and stores the 'auth\_string' value as is in the mysql.user account row. If the plugin requires a hashed string, the string is assumed to be already hashed in the format the plugin requires.

• DISCARD OLD PASSWORD

Discards the account secondary password, if there is one, as described previously in this section.

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

Example: Like the preceding example, but in addition, specify the current password as a cleartext value to satisfy any account requirement that the user making the change knows that password:

```
ALTER USER 'jeffrey'@'localhost'
 IDENTIFIED WITH mysql_native_password
 BY 'password'
 REPLACE 'current_password';
```

The preceding statement fails unless the current user is jeffrey because REPLACE is permitted only for changes to the current user's password.

Example: Establish a new primary password and retain the existing password as the secondary password:

```
ALTER USER 'jeffrey'@'localhost'
 IDENTIFIED BY 'new_password'
 RETAIN CURRENT PASSWORD;
```

Example: Discard the secondary password, leaving the account with only its primary password:

```
ALTER USER 'jeffery'@'localhost' DISCARD OLD PASSWORD;
```

Example: Specify the authentication plugin, along with a hashed password value:

```
ALTER USER 'jeffrey'@'localhost'
```

```
 IDENTIFIED WITH mysql_native_password
 AS '*6C8989366EAF75BB670AD8EA7A7FC1176A95CEF4';
```

For additional information about setting passwords and authentication plugins, see Section 8.2.14, "Assigning Account Passwords", and Section 8.2.17, "Pluggable Authentication".

## <span id="page-22-0"></span>**ALTER USER Multifactor Authentication Options**

As of MySQL 8.0.27, [ALTER USER](#page-14-0) has ADD, MODIFY, and DROP clauses that enable authentication factors to be added, modified, or dropped. In each case, the clause specifies an operation to perform on one authentication factor, and optionally an operation on another authentication factor. For each operation, the factor item specifies the FACTOR keyword preceded by the number 2 or 3 to indicate whether the operation applies to the second or third authentication factor. (1 is not permitted in this context. To act on the first authentication factor, use the syntax described in [ALTER USER](#page-18-0) [Authentication Options.](#page-18-0))

[ALTER USER](#page-14-0) multifactor authentication clause constraints are defined by the authentication\_policy system variable. For example, the authentication\_policy setting controls the number of authentication factors that accounts may have, and for each factor, which authentication methods are permitted. See Configuring the Multifactor Authentication Policy.

When [ALTER USER](#page-14-0) adds, modifies, or drops second and third factors in a single statement, operations are executed sequentially, but if any operation in the sequence fails the entire [ALTER USER](#page-14-0) statement fails.

For ADD, each named factor must not already exist or it cannot be added. For MODIFY and DROP, each named factor must exist to be modified or dropped. If a second and third factor are defined, dropping the second factor causes the third factor to take its place as the second factor.

This statement drops authentication factors 2 and 3, which has the effect of converting the account from 3FA to 1FA:

```
ALTER USER 'user' DROP 2 FACTOR 3 FACTOR;
```

For additional ADD, MODIFY, and DROP examples, see Getting Started with Multifactor Authentication.

For information about factor-specific rules that determine the default authentication plugin for authentication clauses that do not name a plugin, see The Default Authentication Plugin.

## <span id="page-22-1"></span>**ALTER USER Registration Options**

As of MySQL 8.0.27, [ALTER USER](#page-14-0) has clauses that enable FIDO devices to be registered and unregistered. For more information, see Using FIDO Authentication, FIDO Device Unregistration, and the mysql client --fido-register-factor option description.

The mysql client --fido-register-factor option, used for FIDO device registration, causes the mysql client to generate and execute INITIATE REGISTRATION and FINISH REGISTRATION statements. These statements are not intended for manual execution.

#### <span id="page-22-2"></span>**ALTER USER Role Options**

[ALTER USER ... DEFAULT ROLE](#page-14-0) defines which roles become active when the user connects to the server and authenticates, or when the user executes the [SET ROLE DEFAULT](#page-65-0) statement during a session.

[ALTER USER ... DEFAULT ROLE](#page-14-0) is alternative syntax for [SET DEFAULT ROLE](#page-62-0) (see [Section 15.7.1.9, "SET DEFAULT ROLE Statement"\)](#page-62-0). However, [ALTER USER](#page-14-0) can set the default for only a single user, whereas [SET DEFAULT ROLE](#page-62-0) can set the default for multiple users. On the other hand, you can specify CURRENT\_USER as the user name for the [ALTER USER](#page-14-0) statement, whereas you cannot for [SET DEFAULT ROLE](#page-62-0).

Each user account name uses the format described previously.

Each role name uses the format described in Section 8.2.5, "Specifying Role Names". For example:

```
ALTER USER 'joe'@'10.0.0.1' DEFAULT ROLE administrator, developer;
```

The host name part of the role name, if omitted, defaults to '%'.

The clause following the DEFAULT ROLE keywords permits these values:

- NONE: Set the default to NONE (no roles).
- ALL: Set the default to all roles granted to the account.
- role [, role ] ...: Set the default to the named roles, which must exist and be granted to the account at the time [ALTER USER ... DEFAULT ROLE](#page-14-0) is executed.

#### <span id="page-23-0"></span>**ALTER USER SSL/TLS Options**

MySQL can check X.509 certificate attributes in addition to the usual authentication that is based on the user name and credentials. For background information on the use of SSL/TLS with MySQL, see Section 8.3, "Using Encrypted Connections".

To specify SSL/TLS-related options for a MySQL account, use a REQUIRE clause that specifies one or more tls\_option values.

Order of REQUIRE options does not matter, but no option can be specified twice. The AND keyword is optional between REQUIRE options.

[ALTER USER](#page-14-0) permits these tls\_option values:

• NONE

Indicates that all accounts named by the statement have no SSL or X.509 requirements. Unencrypted connections are permitted if the user name and password are valid. Encrypted connections can be used, at the client's option, if the client has the proper certificate and key files.

```
ALTER USER 'jeffrey'@'localhost' REQUIRE NONE;
```

Clients attempt to establish a secure connection by default. For clients that have REQUIRE NONE, the connection attempt falls back to an unencrypted connection if a secure connection cannot be established. To require an encrypted connection, a client need specify only the --sslmode=REQUIRED option; the connection attempt fails if a secure connection cannot be established.

• SSL

Tells the server to permit only encrypted connections for all accounts named by the statement.

```
ALTER USER 'jeffrey'@'localhost' REQUIRE SSL;
```

Clients attempt to establish a secure connection by default. For accounts that have REQUIRE SSL, the connection attempt fails if a secure connection cannot be established.

• X509

For all accounts named by the statement, requires that clients present a valid certificate, but the exact certificate, issuer, and subject do not matter. The only requirement is that it should be possible to verify its signature with one of the CA certificates. Use of X.509 certificates always implies encryption, so the SSL option is unnecessary in this case.

```
ALTER USER 'jeffrey'@'localhost' REQUIRE X509;
```

For accounts with REQUIRE X509, clients must specify the --ssl-key and --ssl-cert options to connect. (It is recommended but not required that --ssl-ca also be specified so that the public

certificate provided by the server can be verified.) This is true for ISSUER and SUBJECT as well because those REQUIRE options imply the requirements of X509.

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

#### <span id="page-24-0"></span>**ALTER USER Resource-Limit Options**

It is possible to place limits on use of server resources by an account, as discussed in Section 8.2.21, "Setting Account Resource Limits". To do so, use a WITH clause that specifies one or more resource\_option values.

Order of WITH options does not matter, except that if a given resource limit is specified multiple times, the last instance takes precedence.

[ALTER USER](#page-14-0) permits these resource\_option values:

• MAX\_QUERIES\_PER\_HOUR count, MAX\_UPDATES\_PER\_HOUR count, MAX\_CONNECTIONS\_PER\_HOUR count

For all accounts named by the statement, these options restrict how many queries, updates, and connections to the server are permitted to each account during any given one-hour period. If count is 0 (the default), this means that there is no limitation for the account.

• MAX\_USER\_CONNECTIONS count

For all accounts named by the statement, restricts the maximum number of simultaneous connections to the server by each account. A nonzero count specifies the limit for the account explicitly. If count is 0 (the default), the server determines the number of simultaneous connections for the account from the global value of the max\_user\_connections system variable. If max\_user\_connections is also zero, there is no limit for the account.

#### Example:

```
ALTER USER 'jeffrey'@'localhost'
 WITH MAX_QUERIES_PER_HOUR 500 MAX_UPDATES_PER_HOUR 100;
```

#### <span id="page-25-0"></span>**ALTER USER Password-Management Options**

[ALTER USER](#page-14-0) supports several password\_option values for password management:

- Password expiration options: You can expire an account password manually and establish its password expiration policy. Policy options do not expire the password. Instead, they determine how the server applies automatic expiration to the account based on password age, which is assessed from the date and time of the most recent account password change.
- Password reuse options: You can restrict password reuse based on number of password changes, time elapsed, or both.
- Password verification-required options: You can indicate whether attempts to change an account password must specify the current password, as verification that the user attempting to make the change actually knows the current password.
- Incorrect-password failed-login tracking options: You can cause the server to track failed login attempts and temporarily lock accounts for which too many consecutive incorrect passwords are given. The required number of failures and the lock time are configurable.

This section describes the syntax for password-management options. For information about establishing policy for password management, see Section 8.2.15, "Password Management".

If multiple password-management options of a given type are specified, the last one takes precedence. For example, PASSWORD EXPIRE DEFAULT PASSWORD EXPIRE NEVER is the same as PASSWORD EXPIRE NEVER.

![](_page_25_Picture_16.jpeg)

#### **Note**

Except for the options that pertain to failed-login tracking, passwordmanagement options apply only to accounts that use an authentication plugin that stores credentials internally to MySQL. For accounts that use a plugin that performs authentication against a credentials system that is external to MySQL, password management must be handled externally against that system as well. For more information about internal credentials storage, see Section 8.2.15, "Password Management".

A client has an expired password if the account password was expired manually or the password age is considered greater than its permitted lifetime per the automatic expiration policy. In this case, the server either disconnects the client or restricts the operations permitted to it (see Section 8.2.16, "Server Handling of Expired Passwords"). Operations performed by a restricted client result in an error until the user establishes a new account password.

![](_page_26_Picture_2.jpeg)

#### **Note**

Although it is possible to "reset" an expired password by setting it to its current value, it is preferable, as a matter of good policy, to choose a different password. DBAs can enforce non-reuse by establishing an appropriate password-reuse policy. See Password Reuse Policy.

[ALTER USER](#page-14-0) permits these password\_option values for controlling password expiration:

• PASSWORD EXPIRE

Immediately marks the password expired for all accounts named by the statement.

ALTER USER 'jeffrey'@'localhost' PASSWORD EXPIRE;

• PASSWORD EXPIRE DEFAULT

Sets all accounts named by the statement so that the global expiration policy applies, as specified by the default\_password\_lifetime system variable.

ALTER USER 'jeffrey'@'localhost' PASSWORD EXPIRE DEFAULT;

• PASSWORD EXPIRE NEVER

This expiration option overrides the global policy for all accounts named by the statement. For each, it disables password expiration so that the password never expires.

ALTER USER 'jeffrey'@'localhost' PASSWORD EXPIRE NEVER;

• PASSWORD EXPIRE INTERVAL N DAY

This expiration option overrides the global policy for all accounts named by the statement. For each, it sets the password lifetime to N days. The following statement requires the password to be changed every 180 days:

```
ALTER USER 'jeffrey'@'localhost' PASSWORD EXPIRE INTERVAL 180 DAY;
```

[ALTER USER](#page-14-0) permits these password\_option values for controlling reuse of previous passwords based on required minimum number of password changes:

• PASSWORD HISTORY DEFAULT

Sets all accounts named by the statement so that the global policy about password history length applies, to prohibit reuse of passwords before the number of changes specified by the password\_history system variable.

ALTER USER 'jeffrey'@'localhost' PASSWORD HISTORY DEFAULT;

• PASSWORD HISTORY N

This history-length option overrides the global policy for all accounts named by the statement. For each, it sets the password history length to N passwords, to prohibit reusing any of the N most recently chosen passwords. The following statement prohibits reuse of any of the previous 6 passwords:

```
ALTER USER 'jeffrey'@'localhost' PASSWORD HISTORY 6;
```

[ALTER USER](#page-14-0) permits these password\_option values for controlling reuse of previous passwords based on time elapsed:

• PASSWORD REUSE INTERVAL DEFAULT

Sets all statements named by the account so that the global policy about time elapsed applies, to prohibit reuse of passwords newer than the number of days specified by the password\_reuse\_interval system variable.

ALTER USER 'jeffrey'@'localhost' PASSWORD REUSE INTERVAL DEFAULT;

• PASSWORD REUSE INTERVAL N DAY

This time-elapsed option overrides the global policy for all accounts named by the statement. For each, it sets the password reuse interval to N days, to prohibit reuse of passwords newer than that many days. The following statement prohibits password reuse for 360 days:

ALTER USER 'jeffrey'@'localhost' PASSWORD REUSE INTERVAL 360 DAY;

[ALTER USER](#page-14-0) permits these password\_option values for controlling whether attempts to change an account password must specify the current password, as verification that the user attempting to make the change actually knows the current password:

• PASSWORD REQUIRE CURRENT

This verification option overrides the global policy for all accounts named by the statement. For each, it requires that password changes specify the current password.

ALTER USER 'jeffrey'@'localhost' PASSWORD REQUIRE CURRENT;

• PASSWORD REQUIRE CURRENT OPTIONAL

This verification option overrides the global policy for all accounts named by the statement. For each, it does not require that password changes specify the current password. (The current password may but need not be given.)

ALTER USER 'jeffrey'@'localhost' PASSWORD REQUIRE CURRENT OPTIONAL;

• PASSWORD REQUIRE CURRENT DEFAULT

Sets all statements named by the account so that the global policy about password verification applies, as specified by the password\_require\_current system variable.

```
ALTER USER 'jeffrey'@'localhost' PASSWORD REQUIRE CURRENT DEFAULT;
```

As of MySQL 8.0.19, [ALTER USER](#page-14-0) permits these password\_option values for controlling failed-login tracking:

• FAILED\_LOGIN\_ATTEMPTS N

Whether to track account login attempts that specify an incorrect password. N must be a number from 0 to 32767. A value of 0 disables failed-login tracking. Values greater than 0 indicate how many consecutive password failures cause temporary account locking (if PASSWORD\_LOCK\_TIME is also nonzero).

• PASSWORD\_LOCK\_TIME {N | UNBOUNDED}

How long to lock the account after too many consecutive login attempts provide an incorrect password. N must be a number from 0 to 32767, or UNBOUNDED. A value of 0 disables temporary account locking. Values greater than 0 indicate how long to lock the account in days. A value of UNBOUNDED causes the account locking duration to be unbounded; once locked, the account remains in a locked state until unlocked. For information about the conditions under which unlocking occurs, see Failed-Login Tracking and Temporary Account Locking.

For failed-login tracking and temporary locking to occur, an account's FAILED\_LOGIN\_ATTEMPTS and PASSWORD\_LOCK\_TIME options both must be nonzero. The following statement modifies an account such that it remains locked for two days after four consecutive password failures:

```
ALTER USER 'jeffrey'@'localhost'
 FAILED_LOGIN_ATTEMPTS 4 PASSWORD_LOCK_TIME 2;
```

### <span id="page-28-0"></span>**ALTER USER Comment and Attribute Options**

MySQL 8.0.21 and higher supports user comments and user attributes, as described in [Section 15.7.1.3, "CREATE USER Statement".](#page-30-0) These can be modified employing ALTER USER by means of the COMMENT and ATTRIBUTE options, respectively. You cannot specify both options in the same ALTER USER statement; attempting to do so results in a syntax error.

The user comment and user attribute are stored in the Information Schema USER\_ATTRIBUTES table as a JSON object; the user comment is stored as the value for a comment key in the ATTRIBUTE column of this table, as shown later in this discussion. The COMMENT text can be any arbitrary quoted text, and replaces any existing user comment. The ATTRIBUTE value must be the valid string representation of a JSON object. This is merged with any existing user attribute as if the JSON\_MERGE\_PATCH() function had been used on the existing user attribute and the new one; for any keys that are re-used, the new value overwrites the old one, as shown here:

```
mysql> SELECT * FROM INFORMATION_SCHEMA.USER_ATTRIBUTES
 -> WHERE USER='bill' AND HOST='localhost';
+------+-----------+----------------+
| USER | HOST | ATTRIBUTE |
+------+-----------+----------------+
| bill | localhost | {"foo": "bar"} |
+------+-----------+----------------+
1 row in set (0.11 sec)
mysql> ALTER USER 'bill'@'localhost' ATTRIBUTE '{"baz": "faz", "foo": "moo"}';
Query OK, 0 rows affected (0.22 sec)
mysql> SELECT * FROM INFORMATION_SCHEMA.USER_ATTRIBUTES
 -> WHERE USER='bill' AND HOST='localhost';
+------+-----------+------------------------------+
| USER | HOST | ATTRIBUTE |
+------+-----------+------------------------------+
| bill | localhost | {"baz": "faz", "foo": "moo"} |
+------+-----------+------------------------------+
1 row in set (0.00 sec)
```

To remove a key and its value from the user attribute, set the key to JSON null (must be lowercase and unquoted), like this:

```
mysql> ALTER USER 'bill'@'localhost' ATTRIBUTE '{"foo": null}';
Query OK, 0 rows affected (0.08 sec)
mysql> SELECT * FROM INFORMATION_SCHEMA.USER_ATTRIBUTES
 -> WHERE USER='bill' AND HOST='localhost';
+------+-----------+----------------+
| USER | HOST | ATTRIBUTE |
+------+-----------+----------------+
| bill | localhost | {"baz": "faz"} |
+------+-----------+----------------+
1 row in set (0.00 sec)
```

To set an existing user comment to an empty string, use ALTER USER ... COMMENT ''. This leaves an empty comment value in the USER\_ATTRIBUTES table; to remove the user comment completely, use ALTER USER ... ATTRIBUTE ... with the value for the column key set to JSON null (unquoted, in lower case). This is illustrated by the following sequence of SQL statements:

```
mysql> ALTER USER 'bill'@'localhost' COMMENT 'Something about Bill';
Query OK, 0 rows affected (0.06 sec)
mysql> SELECT * FROM INFORMATION_SCHEMA.USER_ATTRIBUTES
 -> WHERE USER='bill' AND HOST='localhost';
+------+-----------+---------------------------------------------------+
| USER | HOST | ATTRIBUTE |
+------+-----------+---------------------------------------------------+
| bill | localhost | {"baz": "faz", "comment": "Something about Bill"} |
```

```
+------+-----------+---------------------------------------------------+
1 row in set (0.00 sec)
mysql> ALTER USER 'bill'@'localhost' COMMENT '';
Query OK, 0 rows affected (0.09 sec)
mysql> SELECT * FROM INFORMATION_SCHEMA.USER_ATTRIBUTES
 -> WHERE USER='bill' AND HOST='localhost';
+------+-----------+-------------------------------+
| USER | HOST | ATTRIBUTE |
+------+-----------+-------------------------------+
| bill | localhost | {"baz": "faz", "comment": ""} |
+------+-----------+-------------------------------+
1 row in set (0.00 sec)
mysql> ALTER USER 'bill'@'localhost' ATTRIBUTE '{"comment": null}';
Query OK, 0 rows affected (0.07 sec)
mysql> SELECT * FROM INFORMATION_SCHEMA.USER_ATTRIBUTES
 -> WHERE USER='bill' AND HOST='localhost';
+------+-----------+----------------+
| USER | HOST | ATTRIBUTE |
+------+-----------+----------------+
| bill | localhost | {"baz": "faz"} |
+------+-----------+----------------+
1 row in set (0.00 sec)
```

## <span id="page-29-0"></span>**ALTER USER Account-Locking Options**

MySQL supports account locking and unlocking using the ACCOUNT LOCK and ACCOUNT UNLOCK options, which specify the locking state for an account. For additional discussion, see Section 8.2.20, "Account Locking".

If multiple account-locking options are specified, the last one takes precedence.

[ALTER USER ... ACCOUNT UNLOCK](#page-14-0) unlocks any account named by the statement that is temporarily locked due to too many failed logins. See Section 8.2.15, "Password Management".

#### <span id="page-29-1"></span>**ALTER USER Binary Logging**

[ALTER USER](#page-14-0) is written to the binary log if it succeeds, but not if it fails; in that case, rollback occurs and no changes are made. A statement written to the binary log includes all named users. If the IF EXISTS clause is given, this includes even users that do not exist and were not altered.

If the original statement changes the credentials for a user, the statement written to the binary log specifies the applicable authentication plugin for that user, determined as follows:

- The plugin named in the original statement, if one was specified.
- Otherwise, the plugin associated with the user account if the user exists, or the default authentication plugin if the user does not exist. (If the statement written to the binary log must specify a particular authentication plugin for a user, include it in the original statement.)

If the server adds the default authentication plugin for any users in the statement written to the binary log, it writes a warning to the error log naming those users.

If the original statement specifies the FAILED\_LOGIN\_ATTEMPTS or PASSWORD\_LOCK\_TIME option, the statement written to the binary log includes the option.

[ALTER USER](#page-14-0) statements with clauses that support multifactor authentication (MFA) are written to the binary log with the exception of ALTER USER user factor INITIATE REGISTRATION statements.

• ALTER USER user factor FINISH REGISTRATION SET CHALLENGE\_RESPONSE AS 'auth\_string' statements are written to the binary log as ALTER USER user MODIFY factor IDENTIFIED WITH authentication\_fido AS fido\_hash\_string;

• In a replication context, the replication user requires PASSWORDLESS\_USER\_ADMIN privilege to execute ALTER USER ... MODIFY operations on accounts configured for passwordless authentication using the authentication\_fido plugin.

## <span id="page-30-1"></span>**15.7.1.2 CREATE ROLE Statement**

```
CREATE ROLE [IF NOT EXISTS] role [, role ] ...
```

[CREATE ROLE](#page-30-1) creates one or more roles, which are named collections of privileges. To use this statement, you must have the global CREATE ROLE or CREATE USER privilege. When the read\_only system variable is enabled, [CREATE ROLE](#page-30-1) additionally requires the CONNECTION\_ADMIN privilege (or the deprecated SUPER privilege).

A role when created is locked, has no password, and is assigned the default authentication plugin. (These role attributes can be changed later with the [ALTER USER](#page-14-0) statement, by users who have the global CREATE USER privilege.)

[CREATE ROLE](#page-30-1) either succeeds for all named roles or rolls back and has no effect if any error occurs. By default, an error occurs if you try to create a role that already exists. If the IF NOT EXISTS clause is given, the statement produces a warning for each named role that already exists, rather than an error.

The statement is written to the binary log if it succeeds, but not if it fails; in that case, rollback occurs and no changes are made. A statement written to the binary log includes all named roles. If the IF NOT EXISTS clause is given, this includes even roles that already exist and were not created.

Each role name uses the format described in Section 8.2.5, "Specifying Role Names". For example:

```
CREATE ROLE 'admin', 'developer';
CREATE ROLE 'webapp'@'localhost';
```

The host name part of the role name, if omitted, defaults to '%'.

For role usage examples, see Section 8.2.10, "Using Roles".

## <span id="page-30-0"></span>**15.7.1.3 CREATE USER Statement**

```
CREATE USER [IF NOT EXISTS]
 user [auth_option] [, user [auth_option]] ...
 DEFAULT ROLE role [, role ] ...
 [REQUIRE {NONE | tls_option [[AND] tls_option] ...}]
 [WITH resource_option [resource_option] ...]
 [password_option | lock_option] ...
 [COMMENT 'comment_string' | ATTRIBUTE 'json_object']
user:
 (see Section 8.2.4, "Specifying Account Names")
auth_option: {
 IDENTIFIED BY 'auth_string' [AND 2fa_auth_option]
 | IDENTIFIED BY RANDOM PASSWORD [AND 2fa_auth_option]
 | IDENTIFIED WITH auth_plugin [AND 2fa_auth_option]
 | IDENTIFIED WITH auth_plugin BY 'auth_string' [AND 2fa_auth_option]
 | IDENTIFIED WITH auth_plugin BY RANDOM PASSWORD [AND 2fa_auth_option]
 | IDENTIFIED WITH auth_plugin AS 'auth_string' [AND 2fa_auth_option]
 | IDENTIFIED WITH auth_plugin [initial_auth_option]
}
2fa_auth_option: {
 IDENTIFIED BY 'auth_string' [AND 3fa_auth_option]
 | IDENTIFIED BY RANDOM PASSWORD [AND 3fa_auth_option]
 | IDENTIFIED WITH auth_plugin [AND 3fa_auth_option]
 | IDENTIFIED WITH auth_plugin BY 'auth_string' [AND 3fa_auth_option]
 | IDENTIFIED WITH auth_plugin BY RANDOM PASSWORD [AND 3fa_auth_option]
 | IDENTIFIED WITH auth_plugin AS 'auth_string' [AND 3fa_auth_option]
```

```
}
3fa_auth_option: {
 IDENTIFIED BY 'auth_string'
 | IDENTIFIED BY RANDOM PASSWORD
 | IDENTIFIED WITH auth_plugin
 | IDENTIFIED WITH auth_plugin BY 'auth_string'
 | IDENTIFIED WITH auth_plugin BY RANDOM PASSWORD
 | IDENTIFIED WITH auth_plugin AS 'auth_string'
}
initial_auth_option: {
 INITIAL AUTHENTICATION IDENTIFIED BY {RANDOM PASSWORD | 'auth_string'}
 | INITIAL AUTHENTICATION IDENTIFIED WITH auth_plugin AS 'auth_string'
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
 PASSWORD EXPIRE [DEFAULT | NEVER | INTERVAL N DAY]
 | PASSWORD HISTORY {DEFAULT | N}
 | PASSWORD REUSE INTERVAL {DEFAULT | N DAY}
 | PASSWORD REQUIRE CURRENT [DEFAULT | OPTIONAL]
 | FAILED_LOGIN_ATTEMPTS N
 | PASSWORD_LOCK_TIME {N | UNBOUNDED}
}
lock_option: {
 ACCOUNT LOCK
 | ACCOUNT UNLOCK
}
```

The [CREATE USER](#page-30-0) statement creates new MySQL accounts. It enables authentication, role, SSL/TLS, resource-limit, password-management, comment, and attribute properties to be established for new accounts. It also controls whether accounts are initially locked or unlocked.

To use [CREATE USER](#page-30-0), you must have the global CREATE USER privilege, or the INSERT privilege for the mysql system schema. When the read\_only system variable is enabled, [CREATE USER](#page-30-0) additionally requires the CONNECTION\_ADMIN privilege (or the deprecated SUPER privilege).

As of MySQL 8.0.27, these additional privilege considerations apply:

- The authentication\_policy system variable places certain constraints on how the authentication-related clauses of [CREATE USER](#page-30-0) statements may be used; for details, see the description of that variable. These constraints do not apply if you have the AUTHENTICATION\_POLICY\_ADMIN privilege.
- To create an account that uses passwordless authentication, you must have the PASSWORDLESS\_USER\_ADMIN privilege.

As of MySQL 8.0.22, [CREATE USER](#page-30-0) fails with an error if any account to be created is named as the DEFINER attribute for any stored object. (That is, the statement fails if creating an account would cause the account to adopt a currently orphaned stored object.) To perform the operation anyway, you must have the SET\_USER\_ID privilege; in this case, the statement succeeds with a warning rather than failing with an error. Without SET\_USER\_ID, to perform the user-creation operation, drop the

orphan objects, create the account and grant its privileges, and then re-create the dropped objects. For additional information, including how to identify which objects name a given account as the DEFINER attribute, see Orphan Stored Objects.

[CREATE USER](#page-30-0) either succeeds for all named users or rolls back and has no effect if any error occurs. By default, an error occurs if you try to create a user that already exists. If the IF NOT EXISTS clause is given, the statement produces a warning for each named user that already exists, rather than an error.

![](_page_32_Picture_3.jpeg)

#### **Important**

Under some circumstances, [CREATE USER](#page-30-0) may be recorded in server logs or on the client side in a history file such as ~/.mysql\_history, which means that cleartext passwords may be read by anyone having read access to that information. For information about the conditions under which this occurs for the server logs and how to control it, see Section 8.1.2.3, "Passwords and Logging". For similar information about client-side logging, see Section 6.5.1.3, "mysql Client Logging".

There are several aspects to the [CREATE USER](#page-30-0) statement, described under the following topics:

- [CREATE USER Overview](#page-32-0)
- [CREATE USER Authentication Options](#page-34-0)
- [CREATE USER Multifactor Authentication Options](#page-36-0)
- [CREATE USER Role Options](#page-36-1)
- [CREATE USER SSL/TLS Options](#page-37-0)
- [CREATE USER Resource-Limit Options](#page-38-0)
- [CREATE USER Password-Management Options](#page-39-0)
- [CREATE USER Comment and Attribute Options](#page-41-0)
- [CREATE USER Account-Locking Options](#page-43-0)
- [CREATE USER Binary Logging](#page-43-1)

#### <span id="page-32-0"></span>**CREATE USER Overview**

For each account, [CREATE USER](#page-30-0) creates a new row in the mysql.user system table. The account row reflects the properties specified in the statement. Unspecified properties are set to their default values:

- Authentication: The default authentication plugin (determined as described in The Default Authentication Plugin), and empty credentials
- Default role: NONE
- SSL/TLS: NONE
- Resource limits: Unlimited
- Password management: PASSWORD EXPIRE DEFAULT PASSWORD HISTORY DEFAULT PASSWORD REUSE INTERVAL DEFAULT PASSWORD REQUIRE CURRENT DEFAULT; failed-login tracking and temporary account locking are disabled
- Account locking: ACCOUNT UNLOCK

An account when first created has no privileges and the default role NONE. To assign privileges or roles to this account, use one or more [GRANT](#page-45-0) statements.

Each account name uses the format described in Section 8.2.4, "Specifying Account Names". For example:

```
CREATE USER 'jeffrey'@'localhost' IDENTIFIED BY 'password';
```

The host name part of the account name, if omitted, defaults to '%'. You should be aware that, while MySQL 8.0 treats grants made to such a user as though they had been granted to 'user'@'localhost', this behavior is deprecated as of MySQL 8.0.35, and thus subject to removal in a future version of MySQL.

Each user value naming an account may be followed by an optional auth\_option value that indicates how the account authenticates. These values enable account authentication plugins and credentials (for example, a password) to be specified. Each auth\_option value applies only to the account named immediately preceding it.

Following the user specifications, the statement may include options for SSL/TLS, resource-limit, password-management, and locking properties. All such options are global to the statement and apply to all accounts named in the statement.

Example: Create an account that uses the default authentication plugin and the given password. Mark the password expired so that the user must choose a new one at the first connection to the server:

```
CREATE USER 'jeffrey'@'localhost'
 IDENTIFIED BY 'new_password' PASSWORD EXPIRE;
```

Example: Create an account that uses the caching\_sha2\_password authentication plugin and the given password. Require that a new password be chosen every 180 days, and enable failed-login tracking, such that three consecutive incorrect passwords cause temporary account locking for two days:

```
CREATE USER 'jeffrey'@'localhost'
 IDENTIFIED WITH caching_sha2_password BY 'new_password'
 PASSWORD EXPIRE INTERVAL 180 DAY
 FAILED_LOGIN_ATTEMPTS 3 PASSWORD_LOCK_TIME 2;
```

Example: Create multiple accounts, specifying some per-account properties and some global properties:

```
CREATE USER
 'jeffrey'@'localhost' IDENTIFIED WITH mysql_native_password
 BY 'new_password1',
 'jeanne'@'localhost' IDENTIFIED WITH caching_sha2_password
 BY 'new_password2'
 REQUIRE X509 WITH MAX_QUERIES_PER_HOUR 60
 PASSWORD HISTORY 5
 ACCOUNT LOCK;
```

Each auth\_option value (IDENTIFIED WITH ... BY in this case) applies only to the account named immediately preceding it, so each account uses the immediately following authentication plugin and password.

The remaining properties apply globally to all accounts named in the statement, so for both accounts:

- Connections must be made using a valid X.509 certificate.
- Up to 60 queries per hour are permitted.
- Password changes cannot reuse any of the five most recent passwords.
- The account is locked initially, so effectively it is a placeholder and cannot be used until an administrator unlocks it.

## <span id="page-34-0"></span>**CREATE USER Authentication Options**

An account name may be followed by an auth\_option authentication option that specifies the account authentication plugin, credentials, or both.

![](_page_34_Picture_3.jpeg)

#### **Note**

Prior to MySQL 8.0.27, auth\_option defines the sole method by which an account authenticates. That is, all accounts use one-factor/single-factor authentication (1FA/SFA). MySQL 8.0.27 and higher supports multifactor authentication (MFA), such that accounts can have up to three authentication methods. That is, accounts can use two-factor authentication (2FA) or threefactor authentication (3FA). The syntax and semantics of auth\_option remain unchanged, but auth\_option may be followed by specifications for additional authentication methods. This section describes auth\_option. For details about the optional MFA-related following clauses, see [CREATE USER](#page-36-0) [Multifactor Authentication Options.](#page-36-0)

![](_page_34_Picture_6.jpeg)

#### **Note**

Clauses for random password generation apply only to accounts that use an authentication plugin that stores credentials internally to MySQL. For accounts that use a plugin that performs authentication against a credentials system that is external to MySQL, password management must be handled externally against that system as well. For more information about internal credentials storage, see Section 8.2.15, "Password Management".

• auth\_plugin names an authentication plugin. The plugin name can be a quoted string literal or an unquoted name. Plugin names are stored in the plugin column of the mysql.user system table.

For auth\_option syntax that does not specify an authentication plugin, the server assigns the default plugin, determined as described in The Default Authentication Plugin. For descriptions of each plugin, see Section 8.4.1, "Authentication Plugins".

- Credentials that are stored internally are stored in the mysql.user system table. An 'auth\_string' value or RANDOM PASSWORD specifies account credentials, either as a cleartext (unencrypted) string or hashed in the format expected by the authentication plugin associated with the account, respectively:
  - For syntax that uses BY 'auth\_string', the string is cleartext and is passed to the authentication plugin for possible hashing. The result returned by the plugin is stored in the mysql.user table. A plugin may use the value as specified, in which case no hashing occurs.
  - For syntax that uses BY RANDOM PASSWORD, MySQL generates a random password and as cleartext and passes it to the authentication plugin for possible hashing. The result returned by the plugin is stored in the mysql.user table. A plugin may use the value as specified, in which case no hashing occurs.

Randomly generated passwords are available as of MySQL 8.0.18 and have the characteristics described in Random Password Generation.

• For syntax that uses AS 'auth\_string', the string is assumed to be already in the format the authentication plugin requires, and is stored as is in the mysql.user table. If a plugin requires a hashed value, the value must be already hashed in a format appropriate for the plugin; otherwise, the value cannot be used by the plugin and correct authentication of client connections does not occur.

As of MySQL 8.0.17, a hashed string can be either a string literal or a hexadecimal value. The latter corresponds to the type of value displayed by [SHOW CREATE USER](#page-105-0) for password hashes containing unprintable characters when the print\_identified\_with\_as\_hex system variable is enabled.

![](_page_35_Picture_1.jpeg)

#### **Important**

Although we show 'auth\_string' with quotation marks, a hexadecimal value used for this purpose must not be quoted.

• If an authentication plugin performs no hashing of the authentication string, the BY 'auth\_string' and AS 'auth\_string' clauses have the same effect: The authentication string is stored as is in the mysql.user system table.

[CREATE USER](#page-30-0) permits these auth\_option syntaxes:

• IDENTIFIED BY 'auth\_string'

Sets the account authentication plugin to the default plugin, passes the cleartext 'auth\_string' value to the plugin for possible hashing, and stores the result in the account row in the mysql.user system table.

• IDENTIFIED BY RANDOM PASSWORD

Sets the account authentication plugin to the default plugin, generates a random password, passes the cleartext password value to the plugin for possible hashing, and stores the result in the account row in the mysql.user system table. The statement also returns the cleartext password in a result set to make it available to the user or application executing the statement. For details about the result set and characteristics of randomly generated passwords, see Random Password Generation.

• IDENTIFIED WITH auth\_plugin

Sets the account authentication plugin to auth\_plugin, clears the credentials to the empty string, and stores the result in the account row in the mysql.user system table.

• IDENTIFIED WITH auth\_plugin BY 'auth\_string'

Sets the account authentication plugin to auth\_plugin, passes the cleartext 'auth\_string' value to the plugin for possible hashing, and stores the result in the account row in the mysql.user system table.

• IDENTIFIED WITH auth\_plugin BY RANDOM PASSWORD

Sets the account authentication plugin to auth\_plugin, generates a random password, passes the cleartext password value to the plugin for possible hashing, and stores the result in the account row in the mysql.user system table. The statement also returns the cleartext password in a result set to make it available to the user or application executing the statement. For details about the result set and characteristics of randomly generated passwords, see Random Password Generation.

• IDENTIFIED WITH auth\_plugin AS 'auth\_string'

Sets the account authentication plugin to auth\_plugin and stores the 'auth\_string' value as is in the mysql.user account row. If the plugin requires a hashed string, the string is assumed to be already hashed in the format the plugin requires.

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

For additional information about setting passwords and authentication plugins, see Section 8.2.14, "Assigning Account Passwords", and Section 8.2.17, "Pluggable Authentication".

## <span id="page-36-0"></span>**CREATE USER Multifactor Authentication Options**

The auth\_option part of [CREATE USER](#page-30-0) defines an authentication method for one-factor/single-factor authentication (1FA/SFA). As of MySQL 8.0.27, [CREATE USER](#page-30-0) has clauses that support multifactor authentication (MFA), such that accounts can have up to three authentication methods. That is, accounts can use two-factor authentication (2FA) or three-factor authentication (3FA).

The authentication\_policy system variable defines constraints for [CREATE USER](#page-30-0) statements with multifactor authentication (MFA) clauses. For example, the authentication\_policy setting controls the number of authentication factors that accounts may have, and for each factor, which authentication methods are permitted. See Configuring the Multifactor Authentication Policy.

For information about factor-specific rules that determine the default authentication plugin for authentication clauses that name no plugin, see The Default Authentication Plugin.

Following auth\_option, there may appear different optional MFA clauses:

• 2fa\_auth\_option: Specifies a factor 2 authentication method. The following example defines caching\_sha2\_password as the factor 1 authentication method, and authentication\_ldap\_sasl as the factor 2 authentication method.

```
CREATE USER 'u1'@'localhost'
 IDENTIFIED WITH caching_sha2_password
 BY 'sha2_password'
 AND IDENTIFIED WITH authentication_ldap_sasl
 AS 'uid=u1_ldap,ou=People,dc=example,dc=com';
```

• 3fa\_auth\_option: Following 2fa\_auth\_option, there may appear a 3fa\_auth\_option clause to specify a factor 3 authentication method. The following example defines caching\_sha2\_password as the factor 1 authentication method, authentication\_ldap\_sasl as the factor 2 authentication method, and authentication\_fido as the factor 3 authentication method

```
CREATE USER 'u1'@'localhost'
 IDENTIFIED WITH caching_sha2_password
 BY 'sha2_password'
 AND IDENTIFIED WITH authentication_ldap_sasl
 AS 'uid=u1_ldap,ou=People,dc=example,dc=com'
 AND IDENTIFIED WITH authentication_fido;
```

• initial\_auth\_option: Specifies an initial authentication method for configuring FIDO passwordless authentication. As shown in the following, temporary authentication using either a generated random password or a user-specified auth-string is required to enable FIDO passwordless authentication.

```
CREATE USER user
 IDENTIFIED WITH authentication_fido
 INITIAL AUTHENTICATION IDENTIFIED BY {RANDOM PASSWORD | 'auth_string'};
```

For information about configuring passwordless authentication using FIDO pluggable authentication, See FIDO Passwordless Authentication.

### <span id="page-36-1"></span>**CREATE USER Role Options**

The DEFAULT ROLE clause defines which roles become active when the user connects to the server and authenticates, or when the user executes the [SET ROLE DEFAULT](#page-65-0) statement during a session.

Each role name uses the format described in Section 8.2.5, "Specifying Role Names". For example:

```
CREATE USER 'joe'@'10.0.0.1' DEFAULT ROLE administrator, developer;
```

The host name part of the role name, if omitted, defaults to '%'.

The DEFAULT ROLE clause permits a list of one or more comma-separated role names. These roles must exist at the time [CREATE USER](#page-30-0) is executed; otherwise the statement raises an error ([ER\\_USER\\_DOES\\_NOT\\_EXIST](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_user_does_not_exist)), and the user is not created.

## <span id="page-37-0"></span>**CREATE USER SSL/TLS Options**

MySQL can check X.509 certificate attributes in addition to the usual authentication that is based on the user name and credentials. For background information on the use of SSL/TLS with MySQL, see Section 8.3, "Using Encrypted Connections".

To specify SSL/TLS-related options for a MySQL account, use a REQUIRE clause that specifies one or more tls\_option values.

Order of REQUIRE options does not matter, but no option can be specified twice. The AND keyword is optional between REQUIRE options.

[CREATE USER](#page-30-0) permits these tls\_option values:

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

#### <span id="page-38-0"></span>**CREATE USER Resource-Limit Options**

It is possible to place limits on use of server resources by an account, as discussed in Section 8.2.21, "Setting Account Resource Limits". To do so, use a WITH clause that specifies one or more resource\_option values.

Order of WITH options does not matter, except that if a given resource limit is specified multiple times, the last instance takes precedence.

[CREATE USER](#page-30-0) permits these resource\_option values:

• MAX\_QUERIES\_PER\_HOUR count, MAX\_UPDATES\_PER\_HOUR count, MAX\_CONNECTIONS\_PER\_HOUR count

For all accounts named by the statement, these options restrict how many queries, updates, and connections to the server are permitted to each account during any given one-hour period. If count is 0 (the default), this means that there is no limitation for the account.

• MAX\_USER\_CONNECTIONS count

For all accounts named by the statement, restricts the maximum number of simultaneous connections to the server by each account. A nonzero count specifies the limit for the account explicitly. If count is 0 (the default), the server determines the number of simultaneous connections for the account from the global value of the max\_user\_connections system variable. If max\_user\_connections is also zero, there is no limit for the account.

#### Example:

```
CREATE USER 'jeffrey'@'localhost'
 WITH MAX_QUERIES_PER_HOUR 500 MAX_UPDATES_PER_HOUR 100;
```

## <span id="page-39-0"></span>**CREATE USER Password-Management Options**

[CREATE USER](#page-30-0) supports several password\_option values for password management:

- Password expiration options: You can expire an account password manually and establish its password expiration policy. Policy options do not expire the password. Instead, they determine how the server applies automatic expiration to the account based on password age, which is assessed from the date and time of the most recent account password change.
- Password reuse options: You can restrict password reuse based on number of password changes, time elapsed, or both.
- Password verification-required options: You can indicate whether attempts to change an account password must specify the current password, as verification that the user attempting to make the change actually knows the current password.
- Incorrect-password failed-login tracking options: You can cause the server to track failed login attempts and temporarily lock accounts for which too many consecutive incorrect passwords are given. The required number of failures and the lock time are configurable.

This section describes the syntax for password-management options. For information about establishing policy for password management, see Section 8.2.15, "Password Management".

If multiple password-management options of a given type are specified, the last one takes precedence. For example, PASSWORD EXPIRE DEFAULT PASSWORD EXPIRE NEVER is the same as PASSWORD EXPIRE NEVER.

![](_page_39_Picture_13.jpeg)

#### **Note**

Except for the options that pertain to failed-login tracking, passwordmanagement options apply only to accounts that use an authentication plugin that stores credentials internally to MySQL. For accounts that use a plugin that performs authentication against a credentials system that is external to MySQL, password management must be handled externally against that system as well. For more information about internal credentials storage, see Section 8.2.15, "Password Management".

A client has an expired password if the account password was expired manually or the password age is considered greater than its permitted lifetime per the automatic expiration policy. In this case, the server either disconnects the client or restricts the operations permitted to it (see Section 8.2.16, "Server Handling of Expired Passwords"). Operations performed by a restricted client result in an error until the user establishes a new account password.

[CREATE USER](#page-30-0) permits these password\_option values for controlling password expiration:

• PASSWORD EXPIRE

Immediately marks the password expired for all accounts named by the statement.

```
CREATE USER 'jeffrey'@'localhost' PASSWORD EXPIRE;
```

### • PASSWORD EXPIRE DEFAULT

Sets all accounts named by the statement so that the global expiration policy applies, as specified by the default\_password\_lifetime system variable.

CREATE USER 'jeffrey'@'localhost' PASSWORD EXPIRE DEFAULT;

#### • PASSWORD EXPIRE NEVER

This expiration option overrides the global policy for all accounts named by the statement. For each, it disables password expiration so that the password never expires.

CREATE USER 'jeffrey'@'localhost' PASSWORD EXPIRE NEVER;

#### • PASSWORD EXPIRE INTERVAL N DAY

This expiration option overrides the global policy for all accounts named by the statement. For each, it sets the password lifetime to N days. The following statement requires the password to be changed every 180 days:

```
CREATE USER 'jeffrey'@'localhost' PASSWORD EXPIRE INTERVAL 180 DAY;
```

[CREATE USER](#page-30-0) permits these password\_option values for controlling reuse of previous passwords based on required minimum number of password changes:

#### • PASSWORD HISTORY DEFAULT

Sets all accounts named by the statement so that the global policy about password history length applies, to prohibit reuse of passwords before the number of changes specified by the password\_history system variable.

CREATE USER 'jeffrey'@'localhost' PASSWORD HISTORY DEFAULT;

#### • PASSWORD HISTORY N

This history-length option overrides the global policy for all accounts named by the statement. For each, it sets the password history length to N passwords, to prohibit reusing any of the N most recently chosen passwords. The following statement prohibits reuse of any of the previous 6 passwords:

```
CREATE USER 'jeffrey'@'localhost' PASSWORD HISTORY 6;
```

[CREATE USER](#page-30-0) permits these password\_option values for controlling reuse of previous passwords based on time elapsed:

#### • PASSWORD REUSE INTERVAL DEFAULT

Sets all statements named by the account so that the global policy about time elapsed applies, to prohibit reuse of passwords newer than the number of days specified by the password\_reuse\_interval system variable.

CREATE USER 'jeffrey'@'localhost' PASSWORD REUSE INTERVAL DEFAULT;

## • PASSWORD REUSE INTERVAL N DAY

This time-elapsed option overrides the global policy for all accounts named by the statement. For each, it sets the password reuse interval to N days, to prohibit reuse of passwords newer than that many days. The following statement prohibits password reuse for 360 days:

```
CREATE USER 'jeffrey'@'localhost' PASSWORD REUSE INTERVAL 360 DAY;
```

[CREATE USER](#page-30-0) permits these password\_option values for controlling whether attempts to change an account password must specify the current password, as verification that the user attempting to make the change actually knows the current password:

## • PASSWORD REQUIRE CURRENT

This verification option overrides the global policy for all accounts named by the statement. For each, it requires that password changes specify the current password.

```
CREATE USER 'jeffrey'@'localhost' PASSWORD REQUIRE CURRENT;
```

• PASSWORD REQUIRE CURRENT OPTIONAL

This verification option overrides the global policy for all accounts named by the statement. For each, it does not require that password changes specify the current password. (The current password may but need not be given.)

```
CREATE USER 'jeffrey'@'localhost' PASSWORD REQUIRE CURRENT OPTIONAL;
```

• PASSWORD REQUIRE CURRENT DEFAULT

Sets all statements named by the account so that the global policy about password verification applies, as specified by the password\_require\_current system variable.

```
CREATE USER 'jeffrey'@'localhost' PASSWORD REQUIRE CURRENT DEFAULT;
```

As of MySQL 8.0.19, [CREATE USER](#page-30-0) permits these password\_option values for controlling failedlogin tracking:

• FAILED\_LOGIN\_ATTEMPTS N

Whether to track account login attempts that specify an incorrect password. N must be a number from 0 to 32767. A value of 0 disables failed-login tracking. Values greater than 0 indicate how many consecutive password failures cause temporary account locking (if PASSWORD\_LOCK\_TIME is also nonzero).

• PASSWORD\_LOCK\_TIME {N | UNBOUNDED}

How long to lock the account after too many consecutive login attempts provide an incorrect password. N must be a number from 0 to 32767, or UNBOUNDED. A value of 0 disables temporary account locking. Values greater than 0 indicate how long to lock the account in days. A value of UNBOUNDED causes the account locking duration to be unbounded; once locked, the account remains in a locked state until unlocked. For information about the conditions under which unlocking occurs, see Failed-Login Tracking and Temporary Account Locking.

For failed-login tracking and temporary locking to occur, an account's FAILED\_LOGIN\_ATTEMPTS and PASSWORD\_LOCK\_TIME options both must be nonzero. The following statement creates an account that remains locked for two days after four consecutive password failures:

```
CREATE USER 'jeffrey'@'localhost'
 FAILED_LOGIN_ATTEMPTS 4 PASSWORD_LOCK_TIME 2;
```

#### <span id="page-41-0"></span>**CREATE USER Comment and Attribute Options**

As of MySQL 8.0.21, you can create an account with an optional comment or attribute, as described here:

#### • **User comment**

To set a user comment, add COMMENT 'user\_comment' to the CREATE USER statement, where user\_comment is the text of the user comment.

Example (omitting any other options):

```
CREATE USER 'jon'@'localhost' COMMENT 'Some information about Jon';
```

## • **User attribute**

A user attribute is a JSON object made up of one or more key-value pairs, and is set by including ATTRIBUTE 'json\_object' as part of CREATE USER. json\_object must be a valid JSON object.

Example (omitting any other options):

```
CREATE USER 'jim'@'localhost'
 ATTRIBUTE '{"fname": "James", "lname": "Scott", "phone": "123-456-7890"}';
```

User comments and user attributes are stored together in the ATTRIBUTE column of the Information Schema USER\_ATTRIBUTES table. This query displays the row in this table inserted by the statement just shown for creating the user jim@localhost:

```
mysql> SELECT * FROM INFORMATION_SCHEMA.USER_ATTRIBUTES
 -> WHERE USER = 'jim' AND HOST = 'localhost'\G
*************************** 1. row ***************************
 USER: jim
 HOST: localhost
ATTRIBUTE: {"fname": "James", "lname": "Scott", "phone": "123-456-7890"}
1 row in set (0.00 sec)
```

The COMMENT option in actuality provides a shortcut for setting a user attribute whose only element has comment as its key and whose value is the argument supplied for the option. You can see this by executing the statement CREATE USER 'jon'@'localhost' COMMENT 'Some information about Jon', and observing the row which it inserts into the USER\_ATTRIBUTES table:

```
mysql> CREATE USER 'jon'@'localhost' COMMENT 'Some information about Jon';
Query OK, 0 rows affected (0.06 sec)
mysql> SELECT * FROM INFORMATION_SCHEMA.USER_ATTRIBUTES
 -> WHERE USER = 'jon' AND HOST = 'localhost';
+------+-----------+-------------------------------------------+
| USER | HOST | ATTRIBUTE |
+------+-----------+-------------------------------------------+
| jon | localhost | {"comment": "Some information about Jon"} |
+------+-----------+-------------------------------------------+
1 row in set (0.00 sec)
```

You cannot use COMMENT and ATTRIBUTE together in the same CREATE USER statement; attempting to do so causes a syntax error. To set a user comment concurrently with setting a user attribute, use ATTRIBUTE and include in its argument a value with a comment key, like this:

```
mysql> CREATE USER 'bill'@'localhost'
 -> ATTRIBUTE '{"fname":"William", "lname":"Schmidt",
 -> "comment":"Website developer"}';
Query OK, 0 rows affected (0.16 sec)
```

Since the content of the ATTRIBUTE row is a JSON object, you can employ any appropriate MySQL JSON functions or operators to manipulate it, as shown here:

```
mysql> SELECT
 -> USER AS User,
 -> HOST AS Host,
 -> CONCAT(ATTRIBUTE->>"$.fname"," ",ATTRIBUTE->>"$.lname") AS 'Full Name',
 -> ATTRIBUTE->>"$.comment" AS Comment
 -> FROM INFORMATION_SCHEMA.USER_ATTRIBUTES
 -> WHERE USER='bill' AND HOST='localhost';
+------+-----------+-----------------+-------------------+
| User | Host | Full Name | Comment |
+------+-----------+-----------------+-------------------+
| bill | localhost | William Schmidt | Website developer |
+------+-----------+-----------------+-------------------+
1 row in set (0.00 sec)
```

To set or to make changes in the user comment or user attribute for an existing user, you can use a COMMENT or ATTRIBUTE option with an [ALTER USER](#page-14-0) statement.

Because the user comment and user attribute are stored together internally in a single JSON column, this sets an upper limit on their maximum combined size; see JSON Storage Requirements, for more information.

See also the description of the Information Schema USER\_ATTRIBUTES table for more information and examples.

#### <span id="page-43-0"></span>**CREATE USER Account-Locking Options**

MySQL supports account locking and unlocking using the ACCOUNT LOCK and ACCOUNT UNLOCK options, which specify the locking state for an account. For additional discussion, see Section 8.2.20, "Account Locking".

If multiple account-locking options are specified, the last one takes precedence.

## <span id="page-43-1"></span>**CREATE USER Binary Logging**

[CREATE USER](#page-30-0) is written to the binary log if it succeeds, but not if it fails; in that case, rollback occurs and no changes are made. A statement written to the binary log includes all named users. If the IF NOT EXISTS clause is given, this includes even users that already exist and were not created.

The statement written to the binary log specifies an authentication plugin for each user, determined as follows:

- The plugin named in the original statement, if one was specified.
- Otherwise, the default authentication plugin. In particular, if a user u1 already exists and uses a nondefault authentication plugin, the statement written to the binary log for CREATE USER IF NOT EXISTS u1 names the default authentication plugin. (If the statement written to the binary log must specify a nondefault authentication plugin for a user, include it in the original statement.)

If the server adds the default authentication plugin for any nonexisting users in the statement written to the binary log, it writes a warning to the error log naming those users.

If the original statement specifies the FAILED\_LOGIN\_ATTEMPTS or PASSWORD\_LOCK\_TIME option, the statement written to the binary log includes the option.

[CREATE USER](#page-30-0) statements with clauses that support multifactor authentication (MFA) are written to the binary log.

• CREATE USER ... IDENTIFIED WITH .. INITIAL AUTHENTICATION IDENTIFIED WITH ... statements are written to the binary log as CREATE USER .. IDENTIFIED WITH .. INITIAL AUTHENTICATION IDENTIFIED WITH .. AS 'password-hash', where the password-hash is the user-specified auth-string or the random password generated by server when the RANDOM PASSWORD clause is specified.

## <span id="page-43-2"></span>**15.7.1.4 DROP ROLE Statement**

```
DROP ROLE [IF EXISTS] role [, role ] ...
```

[DROP ROLE](#page-43-2) removes one or more roles (named collections of privileges). To use this statement, you must have the global DROP ROLE or CREATE USER privilege. When the read\_only system variable is enabled, [DROP ROLE](#page-43-2) additionally requires the CONNECTION\_ADMIN privilege (or the deprecated SUPER privilege).

As of MySQL 8.0.16, users who have the CREATE USER privilege can use this statement to drop accounts that are locked or unlocked. Users who have the DROP ROLE privilege can use this statement only to drop accounts that are locked (unlocked accounts are presumably user accounts used to log in to the server and not just as roles).

Roles named in the mandatory\_roles system variable value cannot be dropped.

[DROP ROLE](#page-43-2) either succeeds for all named roles or rolls back and has no effect if any error occurs. By default, an error occurs if you try to drop a role that does not exist. If the IF EXISTS clause is given, the statement produces a warning for each named role that does not exist, rather than an error.

The statement is written to the binary log if it succeeds, but not if it fails; in that case, rollback occurs and no changes are made. A statement written to the binary log includes all named roles. If the IF EXISTS clause is given, this includes even roles that do not exist and were not dropped.

Each role name uses the format described in Section 8.2.5, "Specifying Role Names". For example:

```
DROP ROLE 'admin', 'developer';
DROP ROLE 'webapp'@'localhost';
```

The host name part of the role name, if omitted, defaults to '%'.

A dropped role is automatically revoked from any user account (or role) to which the role was granted. Within any current session for such an account, its adjusted privileges apply beginning with the next statement executed.

For role usage examples, see Section 8.2.10, "Using Roles".

## <span id="page-44-0"></span>**15.7.1.5 DROP USER Statement**

```
DROP USER [IF EXISTS] user [, user] ...
```

The [DROP USER](#page-44-0) statement removes one or more MySQL accounts and their privileges. It removes privilege rows for the account from all grant tables.

Roles named in the mandatory\_roles system variable value cannot be dropped.

To use [DROP USER](#page-44-0), you must have the global CREATE USER privilege, or the DELETE privilege for the mysql system schema. When the read\_only system variable is enabled, [DROP USER](#page-44-0) additionally requires the CONNECTION\_ADMIN privilege (or the deprecated SUPER privilege).

As of MySQL 8.0.22, [DROP USER](#page-44-0) fails with an error if any account to be dropped is named as the DEFINER attribute for any stored object. (That is, the statement fails if dropping an account would cause a stored object to become orphaned.) To perform the operation anyway, you must have the SET\_USER\_ID privilege; in this case, the statement succeeds with a warning rather than failing with an error. For additional information, including how to identify which objects name a given account as the DEFINER attribute, see Orphan Stored Objects.

[DROP USER](#page-44-0) either succeeds for all named users or rolls back and has no effect if any error occurs. By default, an error occurs if you try to drop a user that does not exist. If the IF EXISTS clause is given, the statement produces a warning for each named user that does not exist, rather than an error.

The statement is written to the binary log if it succeeds, but not if it fails; in that case, rollback occurs and no changes are made. A statement written to the binary log includes all named users. If the IF EXISTS clause is given, this includes even users that do not exist and were not dropped.

Each account name uses the format described in Section 8.2.4, "Specifying Account Names". For example:

```
DROP USER 'jeffrey'@'localhost';
```

The host name part of the account name, if omitted, defaults to '%'.

![](_page_44_Picture_19.jpeg)

#### **Important**

[DROP USER](#page-44-0) does not automatically close any open user sessions. Rather, in the event that a user with an open session is dropped, the statement does not take effect until that user's session is closed. Once the session is closed, the user is dropped, and that user's next attempt to log in fails. This is by design.

[DROP USER](#page-44-0) does not automatically drop or invalidate databases or objects within them that the old user created. This includes stored programs or views for which the DEFINER attribute names the dropped user. Attempts to access such objects may produce an error if they execute in definer security context. (For information about security context, see Section 27.6, "Stored Object Access Control".)

## <span id="page-45-0"></span>**15.7.1.6 GRANT Statement**

```
GRANT
 priv_type [(column_list)]
 [, priv_type [(column_list)]] ...
 ON [object_type] priv_level
 TO user_or_role [, user_or_role] ...
 [WITH GRANT OPTION]
 [AS user
 [WITH ROLE
 DEFAULT
 | NONE
 | ALL
 | ALL EXCEPT role [, role ] ...
 | role [, role ] ...
 ]
 ]
}
GRANT PROXY ON user_or_role
 TO user_or_role [, user_or_role] ...
 [WITH GRANT OPTION]
GRANT role [, role] ...
 TO user_or_role [, user_or_role] ...
 [WITH ADMIN OPTION]
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
user_or_role: {
 user (see Section 8.2.4, "Specifying Account Names")
 | role (see Section 8.2.5, "Specifying Role Names")
}
```

The [GRANT](#page-45-0) statement assigns privileges and roles to MySQL user accounts and roles. There are several aspects to the [GRANT](#page-45-0) statement, described under the following topics:

- [GRANT General Overview](#page-46-0)
- [Object Quoting Guidelines](#page-47-0)
- [Account Names](#page-49-0)
- [Privileges Supported by MySQL](#page-49-1)
- [Global Privileges](#page-54-0)
- [Database Privileges](#page-54-1)

- [Table Privileges](#page-54-2)
- [Column Privileges](#page-55-0)
- [Stored Routine Privileges](#page-55-1)
- [Proxy User Privileges](#page-55-2)
- [Granting Roles](#page-55-3)
- The AS [Clause and Privilege Restrictions](#page-56-0)
- [Other Account Characteristics](#page-57-0)
- [MySQL and Standard SQL Versions of GRANT](#page-58-0)

### <span id="page-46-0"></span>**GRANT General Overview**

The [GRANT](#page-45-0) statement enables system administrators to grant privileges and roles, which can be granted to user accounts and roles. These syntax restrictions apply:

- [GRANT](#page-45-0) cannot mix granting both privileges and roles in the same statement. A given [GRANT](#page-45-0) statement must grant either privileges or roles.
- The ON clause distinguishes whether the statement grants privileges or roles:
  - With ON, the statement grants privileges.
  - Without ON, the statement grants roles.
  - It is permitted to assign both privileges and roles to an account, but you must use separate [GRANT](#page-45-0) statements, each with syntax appropriate to what is to be granted.

For more information about roles, see Section 8.2.10, "Using Roles".

To grant a privilege with [GRANT](#page-45-0), you must have the GRANT OPTION privilege, and you must have the privileges that you are granting. (Alternatively, if you have the UPDATE privilege for the grant tables in the mysql system schema, you can grant any account any privilege.) When the read\_only system variable is enabled, [GRANT](#page-45-0) additionally requires the CONNECTION\_ADMIN privilege (or the deprecated SUPER privilege).

[GRANT](#page-45-0) either succeeds for all named users and roles or rolls back and has no effect if any error occurs. The statement is written to the binary log only if it succeeds for all named users and roles.

The [REVOKE](#page-59-0) statement is related to [GRANT](#page-45-0) and enables administrators to remove account privileges. See [Section 15.7.1.8, "REVOKE Statement"](#page-59-0).

Each account name uses the format described in Section 8.2.4, "Specifying Account Names". Each role name uses the format described in Section 8.2.5, "Specifying Role Names". For example:

```
GRANT ALL ON db1.* TO 'jeffrey'@'localhost';
GRANT 'role1', 'role2' TO 'user1'@'localhost', 'user2'@'localhost';
GRANT SELECT ON world.* TO 'role3';
```

The host name part of the account or role name, if omitted, defaults to '%'.

Normally, a database administrator first uses [CREATE USER](#page-30-0) to create an account and define its nonprivilege characteristics such as its password, whether it uses secure connections, and limits on access to server resources, then uses [GRANT](#page-45-0) to define its privileges. [ALTER USER](#page-14-0) may be used to change the nonprivilege characteristics of existing accounts. For example:

```
CREATE USER 'jeffrey'@'localhost' IDENTIFIED BY 'password';
GRANT ALL ON db1.* TO 'jeffrey'@'localhost';
GRANT SELECT ON db2.invoice TO 'jeffrey'@'localhost';
```

ALTER USER 'jeffrey'@'localhost' WITH MAX\_QUERIES\_PER\_HOUR 90;

From the mysql program, [GRANT](#page-45-0) responds with Query OK, 0 rows affected when executed successfully. To determine what privileges result from the operation, use [SHOW GRANTS](#page-115-0). See [Section 15.7.7.21, "SHOW GRANTS Statement".](#page-115-0)

![](_page_47_Picture_3.jpeg)

#### **Important**

Under some circumstances, [GRANT](#page-45-0) may be recorded in server logs or on the client side in a history file such as ~/.mysql\_history, which means that cleartext passwords may be read by anyone having read access to that information. For information about the conditions under which this occurs for the server logs and how to control it, see Section 8.1.2.3, "Passwords and Logging". For similar information about client-side logging, see Section 6.5.1.3, "mysql Client Logging".

[GRANT](#page-45-0) supports host names up to 255 characters long (60 characters prior to MySQL 8.0.17). User names can be up to 32 characters. Database, table, column, and routine names can be up to 64 characters.

![](_page_47_Picture_7.jpeg)

#### **Warning**

Do not attempt to change the permissible length for user names by altering the mysql.user system table. Doing so results in unpredictable behavior which may even make it impossible for users to log in to the MySQL server. Never alter the structure of tables in the mysql system schema in any manner except by means of the procedure described in Chapter 3, Upgrading MySQL.

## <span id="page-47-0"></span>**Object Quoting Guidelines**

Several objects within [GRANT](#page-45-0) statements are subject to quoting, although quoting is optional in many cases: Account, role, database, table, column, and routine names. For example, if a user\_name or host\_name value in an account name is legal as an unquoted identifier, you need not quote it. However, quotation marks are necessary to specify a user\_name string containing special characters (such as -), or a host\_name string containing special characters or wildcard characters such as % (for example, 'test-user'@'%.com'). Quote the user name and host name separately.

To specify quoted values:

- Quote database, table, column, and routine names as identifiers.
- Quote user names and host names as identifiers or as strings.
- Quote passwords as strings.

For string-quoting and identifier-quoting guidelines, see Section 11.1.1, "String Literals", and Section 11.2, "Schema Object Names".

![](_page_47_Picture_17.jpeg)

#### **Important**

The use of the wildcard characters % and \_ as described in the next few paragraphs is deprecated as of MySQL 8.0.35 and thus subject to removal in a future version of MySQL.

The \_ and % wildcards are permitted when specifying database names in [GRANT](#page-45-0) statements that grant privileges at the database level (GRANT ... ON db\_name.\*). This means, for example, that to use a \_ character as part of a database name, specify it using the \ escape character as \\_ in the [GRANT](#page-45-0) statement, to prevent the user from being able to access additional databases matching the wildcard pattern (for example, GRANT ... ON `foo\\_bar`.\* TO ...).

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
```

Bye

If we end the session and then log in again with the mysql client, this time as u, we see that this account has only the privilege provided by the first matching grant, but not the second:

```
$> mysql -uu -hlocalhost
```

```
Welcome to the MySQL monitor. Commands end with ; or \g.
Your MySQL connection id is 10
Server version: 8.0.46-tr Source distribution
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

In privilege assignments, MySQL interprets occurrences of unescaped \_ and % SQL wildcard characters in database names as literal characters under these circumstances:

- When a database name is not used to grant privileges at the database level, but as a qualifier for granting privileges to some other object such as a table or routine (for example, GRANT ... ON db\_name.tbl\_name).
- Enabling partial\_revokes causes MySQL to interpret unescaped \_ and % wildcard characters in database names as literal characters, just as if they had been escaped as \\_ and \%. Because

this changes how MySQL interprets privileges, it may be advisable to avoid unescaped wildcard characters in privilege assignments for installations where partial\_revokes may be enabled. For more information, see Section 8.2.12, "Privilege Restriction Using Partial Revokes".

#### <span id="page-49-0"></span>**Account Names**

A user value in a [GRANT](#page-45-0) statement indicates a MySQL account to which the statement applies. To accommodate granting rights to users from arbitrary hosts, MySQL supports specifying the user value in the form 'user\_name'@'host\_name'.

You can specify wildcards in the host name. For example, 'user\_name'@'%.example.com' applies to user\_name for any host in the example.com domain, and 'user\_name'@'198.51.100.%' applies to user\_name for any host in the 198.51.100 class C subnet.

The simple form 'user\_name' is a synonym for 'user\_name'@'%'.

![](_page_49_Picture_6.jpeg)

#### **Note**

MySQL automatically assigns all privileges granted to 'username'@'%' to the 'username'@'localhost' account as well. This behavior is deprecated in MySQL 8.0.35 and later MySQL 8.0 releases, and is subject to removal in a future version of MySQL.

MySQL does not support wildcards in user names. To refer to an anonymous user, specify an account with an empty user name with the [GRANT](#page-45-0) statement:

```
GRANT ALL ON test.* TO ''@'localhost' ...;
```

In this case, any user who connects from the local host with the correct password for the anonymous user is permitted access, with the privileges associated with the anonymous-user account.

For additional information about user name and host name values in account names, see Section 8.2.4, "Specifying Account Names".

![](_page_49_Picture_13.jpeg)

#### **Warning**

If you permit local anonymous users to connect to the MySQL server, you should also grant privileges to all local users as 'user\_name'@'localhost'. Otherwise, the anonymous user account for localhost in the mysql.user system table is used when named users try to log in to the MySQL server from the local machine. For details, see Section 8.2.6, "Access Control, Stage 1: Connection Verification".

To determine whether this issue applies to you, execute the following query, which lists any anonymous users:

```
SELECT Host, User FROM mysql.user WHERE User='';
```

To avoid the problem just described, delete the local anonymous user account using this statement:

DROP USER ''@'localhost';

## <span id="page-49-1"></span>**Privileges Supported by MySQL**

The following tables summarize the permissible static and dynamic priv\_type privilege types that can be specified for the [GRANT](#page-45-0) and [REVOKE](#page-59-0) statements, and the levels at which each privilege can be granted. For additional information about each privilege, see Section 8.2.2, "Privileges Provided by MySQL". For information about the differences between static and dynamic privileges, see Static Versus Dynamic Privileges.

**Table 15.11 Permissible Static Privileges for GRANT and REVOKE**

| Privilege               | Meaning and Grantable Levels                                                                                              |
|-------------------------|---------------------------------------------------------------------------------------------------------------------------|
| ALL [PRIVILEGES]        | Grant all privileges at specified access level<br>except GRANT OPTION and PROXY.                                          |
| ALTER                   | Enable use of ALTER TABLE. Levels: Global,<br>database, table.                                                            |
| ALTER ROUTINE           | Enable stored routines to be altered or dropped.<br>Levels: Global, database, routine.                                    |
| CREATE                  | Enable database and table creation. Levels:<br>Global, database, table.                                                   |
| CREATE ROLE             | Enable role creation. Level: Global.                                                                                      |
| CREATE ROUTINE          | Enable stored routine creation. Levels: Global,<br>database.                                                              |
| CREATE TABLESPACE       | Enable tablespaces and log file groups to be<br>created, altered, or dropped. Level: Global.                              |
| CREATE TEMPORARY TABLES | Enable use of CREATE TEMPORARY TABLE.<br>Levels: Global, database.                                                        |
| CREATE USER             | Enable use of CREATE USER, DROP USER,<br>RENAME USER, and REVOKE ALL PRIVILEGES.<br>Level: Global.                        |
| CREATE VIEW             | Enable views to be created or altered. Levels:<br>Global, database, table.                                                |
| DELETE                  | Enable use of DELETE. Level: Global, database,<br>table.                                                                  |
| DROP                    | Enable databases, tables, and views to be<br>dropped. Levels: Global, database, table.                                    |
| DROP ROLE               | Enable roles to be dropped. Level: Global.                                                                                |
| EVENT                   | Enable use of events for the Event Scheduler.<br>Levels: Global, database.                                                |
| EXECUTE                 | Enable the user to execute stored routines.<br>Levels: Global, database, routine.                                         |
| FILE                    | Enable the user to cause the server to read or<br>write files. Level: Global.                                             |
| GRANT OPTION            | Enable privileges to be granted to or removed<br>from other accounts. Levels: Global, database,<br>table, routine, proxy. |
| INDEX                   | Enable indexes to be created or dropped. Levels:<br>Global, database, table.                                              |
| INSERT                  | Enable use of INSERT. Levels: Global, database,<br>table, column.                                                         |
| LOCK TABLES             | Enable use of LOCK TABLES on tables for which<br>you have the SELECT privilege. Levels: Global,<br>database.              |
| PROCESS                 | Enable the user to see all processes with SHOW<br>PROCESSLIST. Level: Global.                                             |
| PROXY                   | Enable user proxying. Level: From user to user.                                                                           |
| REFERENCES              | Enable foreign key creation. Levels: Global,<br>database, table, column.                                                  |

| Privilege          | Meaning and Grantable Levels                                                                                                                                                                        |
|--------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| RELOAD             | Enable use of FLUSH operations. Level: Global.                                                                                                                                                      |
| REPLICATION CLIENT | Enable the user to ask where source or replica<br>servers are. Level: Global.                                                                                                                       |
| REPLICATION SLAVE  | Enable replicas to read binary log events from the<br>source. Level: Global.                                                                                                                        |
| SELECT             | Enable use of SELECT. Levels: Global, database,<br>table, column.                                                                                                                                   |
| SHOW DATABASES     | Enable SHOW DATABASES to show all databases.<br>Level: Global.                                                                                                                                      |
| SHOW VIEW          | Enable use of SHOW CREATE VIEW. Levels:<br>Global, database, table.                                                                                                                                 |
| SHUTDOWN           | Enable use of mysqladmin shutdown. Level:<br>Global.                                                                                                                                                |
| SUPER              | Enable use of other administrative operations<br>such as CHANGE REPLICATION SOURCE TO,<br>CHANGE MASTER TO, KILL, PURGE BINARY<br>LOGS, SET GLOBAL, and mysqladmin debug<br>command. Level: Global. |
| TRIGGER            | Enable trigger operations. Levels: Global,<br>database, table.                                                                                                                                      |
| UPDATE             | Enable use of UPDATE. Levels: Global, database,<br>table, column.                                                                                                                                   |
| USAGE              | Synonym for "no privileges"                                                                                                                                                                         |

**Table 15.12 Permissible Dynamic Privileges for GRANT and REVOKE**

| Privilege                   | Meaning and Grantable Levels                                                   |
|-----------------------------|--------------------------------------------------------------------------------|
| APPLICATION_PASSWORD_ADMIN  | Enable dual password administration. Level:<br>Global.                         |
| AUDIT_ABORT_EXEMPT          | Allow queries blocked by audit log filter. Level:<br>Global.                   |
| AUDIT_ADMIN                 | Enable audit log configuration. Level: Global.                                 |
| AUTHENTICATION_POLICY_ADMIN | Enable authentication policy administration. Level:<br>Global.                 |
| BACKUP_ADMIN                | Enable backup administration. Level: Global.                                   |
| BINLOG_ADMIN                | Enable binary log control. Level: Global.                                      |
| BINLOG_ENCRYPTION_ADMIN     | Enable activation and deactivation of binary log<br>encryption. Level: Global. |
| CLONE_ADMIN                 | Enable clone administration. Level: Global.                                    |
| CONNECTION_ADMIN            | Enable connection limit/restriction control. Level:<br>Global.                 |
| ENCRYPTION_KEY_ADMIN        | Enable InnoDB key rotation. Level: Global.                                     |
| FIREWALL_ADMIN              | Enable firewall rule administration, any user.<br>Level: Global.               |
| FIREWALL_EXEMPT             | Exempt user from firewall restrictions. Level:<br>Global.                      |
| FIREWALL_USER               | Enable firewall rule administration, self. Level:<br>Global.                   |

| Privilege                  | Meaning and Grantable Levels                                                       |
|----------------------------|------------------------------------------------------------------------------------|
| FLUSH_OPTIMIZER_COSTS      | Enable optimizer cost reloading. Level: Global.                                    |
| FLUSH_STATUS               | Enable status indicator flushing. Level: Global.                                   |
| FLUSH_TABLES               | Enable table flushing. Level: Global.                                              |
| FLUSH_USER_RESOURCES       | Enable user-resource flushing. Level: Global.                                      |
| GROUP_REPLICATION_ADMIN    | Enable Group Replication control. Level: Global.                                   |
| INNODB_REDO_LOG_ARCHIVE    | Enable redo log archiving administration. Level:<br>Global.                        |
| INNODB_REDO_LOG_ENABLE     | Enable or disable redo logging. Level: Global.                                     |
| NDB_STORED_USER            | Enable sharing of user or role between SQL<br>nodes (NDB Cluster). Level: Global.  |
| PASSWORDLESS_USER_ADMIN    | Enable passwordless user account administration.<br>Level: Global.                 |
| PERSIST_RO_VARIABLES_ADMIN | Enable persisting read-only system variables.<br>Level: Global.                    |
| REPLICATION_APPLIER        | Act as the PRIVILEGE_CHECKS_USER for a<br>replication channel. Level: Global.      |
| REPLICATION_SLAVE_ADMIN    | Enable regular replication control. Level: Global.                                 |
| RESOURCE_GROUP_ADMIN       | Enable resource group administration. Level:<br>Global.                            |
| RESOURCE_GROUP_USER        | Enable resource group administration. Level:<br>Global.                            |
| ROLE_ADMIN                 | Enable roles to be granted or revoked, use of<br>WITH ADMIN OPTION. Level: Global. |
| SESSION_VARIABLES_ADMIN    | Enable setting restricted session system variables.<br>Level: Global.              |
| SET_USER_ID                | Enable setting non-self DEFINER values. Level:<br>Global.                          |
| SHOW_ROUTINE               | Enable access to stored routine definitions. Level:<br>Global.                     |
| SKIP_QUERY_REWRITE         | Do not rewrite queries executed by this user.<br>Level: Global.                    |
| SYSTEM_USER                | Designate account as system account. Level:<br>Global.                             |
| SYSTEM_VARIABLES_ADMIN     | Enable modifying or persisting global system<br>variables. Level: Global.          |
| TABLE_ENCRYPTION_ADMIN     | Enable overriding default encryption settings.<br>Level: Global.                   |
| TELEMETRY_LOG_ADMIN        | Enable telemetry log configuration for MySQL<br>HeatWave on AWS. Level: Global.    |
| TP_CONNECTION_ADMIN        | Enable thread pool connection administration.<br>Level: Global.                    |
| VERSION_TOKEN_ADMIN        | Enable use of Version Tokens functions. Level:<br>Global.                          |
| XA_RECOVER_ADMIN           | Enable XA RECOVER execution. Level: Global.                                        |
|                            |                                                                                    |

A trigger is associated with a table. To create or drop a trigger, you must have the TRIGGER privilege for the table, not the trigger.

In [GRANT](#page-45-0) statements, the ALL [PRIVILEGES] or PROXY privilege must be named by itself and cannot be specified along with other privileges. ALL [PRIVILEGES] stands for all privileges available for the level at which privileges are to be granted except for the GRANT OPTION and PROXY privileges.

MySQL account information is stored in the tables of the mysql system schema. For additional details, consult Section 8.2, "Access Control and Account Management", which discusses the mysql system schema and the access control system extensively.

If the grant tables hold privilege rows that contain mixed-case database or table names and the lower\_case\_table\_names system variable is set to a nonzero value, [REVOKE](#page-59-0) cannot be used to revoke these privileges. It is necessary in such cases to manipulate the grant tables directly. ([GRANT](#page-45-0) does not create such rows when lower\_case\_table\_names is set, but such rows might have been created prior to setting that variable. The lower\_case\_table\_names setting can only be configured at server startup.)

Privileges can be granted at several levels, depending on the syntax used for the ON clause. For [REVOKE](#page-59-0), the same ON syntax specifies which privileges to remove.

For the global, database, table, and routine levels, [GRANT ALL](#page-45-0) assigns only the privileges that exist at the level you are granting. For example, GRANT ALL ON db\_name.\* is a database-level statement, so it does not grant any global-only privileges such as FILE. Granting ALL does not assign the GRANT OPTION or PROXY privilege.

The object\_type clause, if present, should be specified as TABLE, FUNCTION, or PROCEDURE when the following object is a table, a stored function, or a stored procedure.

The privileges that a user holds for a database, table, column, or routine are formed additively as the logical OR of the account privileges at each of the privilege levels, including the global level. It is not possible to deny a privilege granted at a higher level by absence of that privilege at a lower level. For example, this statement grants the SELECT and INSERT privileges globally:

```
GRANT SELECT, INSERT ON *.* TO u1;
```

The globally granted privileges apply to all databases, tables, and columns, even though not granted at any of those lower levels.

As of MySQL 8.0.16, it is possible to explicitly deny a privilege granted at the global level by revoking it for particular databases, if the partial\_revokes system variable is enabled:

```
GRANT SELECT, INSERT, UPDATE ON *.* TO u1;
REVOKE INSERT, UPDATE ON db1.* FROM u1;
```

The result of the preceding statements is that SELECT applies globally to all tables, whereas INSERT and UPDATE apply globally except to tables in db1. Account access to db1 is read only.

Details of the privilege-checking procedure are presented in Section 8.2.7, "Access Control, Stage 2: Request Verification".

If you are using table, column, or routine privileges for even one user, the server examines table, column, and routine privileges for all users and this slows down MySQL a bit. Similarly, if you limit the number of queries, updates, or connections for any users, the server must monitor these values.

MySQL enables you to grant privileges on databases or tables that do not exist. For tables, the privileges to be granted must include the CREATE privilege. This behavior is by design, and is intended to enable the database administrator to prepare user accounts and privileges for databases or tables that are to be created at a later time.

![](_page_53_Picture_16.jpeg)

#### **Important**

MySQL does not automatically revoke any privileges when you drop a database or table. However, if you drop a routine, any routine-level privileges granted for that routine are revoked.

#### <span id="page-54-0"></span>**Global Privileges**

Global privileges are administrative or apply to all databases on a given server. To assign global privileges, use ON \*.\* syntax:

```
GRANT ALL ON *.* TO 'someuser'@'somehost';
GRANT SELECT, INSERT ON *.* TO 'someuser'@'somehost';
```

The CREATE TABLESPACE, CREATE USER, FILE, PROCESS, RELOAD, REPLICATION CLIENT, REPLICATION SLAVE, SHOW DATABASES, SHUTDOWN, and SUPER, CREATE ROLE and DROP ROLE static privileges are administrative and can only be granted globally.

Dynamic privileges are all global and can only be granted globally.

Other privileges can be granted globally or at more specific levels.

The effect of GRANT OPTION granted at the global level differs for static and dynamic privileges:

- GRANT OPTION granted for any static global privilege applies to all static global privileges.
- GRANT OPTION granted for any dynamic privilege applies only to that dynamic privilege.

GRANT ALL at the global level grants all static global privileges and all currently registered dynamic privileges. A dynamic privilege registered subsequent to execution of the GRANT statement is not granted retroactively to any account.

MySQL stores global privileges in the mysql.user system table.

### <span id="page-54-1"></span>**Database Privileges**

Database privileges apply to all objects in a given database. To assign database-level privileges, use ON db\_name.\* syntax:

```
GRANT ALL ON mydb.* TO 'someuser'@'somehost';
GRANT SELECT, INSERT ON mydb.* TO 'someuser'@'somehost';
```

If you use ON \* syntax (rather than ON \*.\*), privileges are assigned at the database level for the default database. An error occurs if there is no default database.

The CREATE, DROP, EVENT, GRANT OPTION, LOCK TABLES, and REFERENCES privileges can be specified at the database level. Table or routine privileges also can be specified at the database level, in which case they apply to all tables or routines in the database.

MySQL stores database privileges in the mysql.db system table.

## <span id="page-54-2"></span>**Table Privileges**

Table privileges apply to all columns in a given table. To assign table-level privileges, use ON db\_name.tbl\_name syntax:

```
GRANT ALL ON mydb.mytbl TO 'someuser'@'somehost';
GRANT SELECT, INSERT ON mydb.mytbl TO 'someuser'@'somehost';
```

If you specify tbl\_name rather than db\_name.tbl\_name, the statement applies to tbl\_name in the default database. An error occurs if there is no default database.

The permissible priv\_type values at the table level are ALTER, CREATE VIEW, CREATE, DELETE, DROP, GRANT OPTION, INDEX, INSERT, REFERENCES, SELECT, SHOW VIEW, TRIGGER, and UPDATE.

Table-level privileges apply to base tables and views. They do not apply to tables created with CREATE TEMPORARY TABLE, even if the table names match. For information about TEMPORARY table privileges, see Section 15.1.20.2, "CREATE TEMPORARY TABLE Statement".

MySQL stores table privileges in the mysql.tables\_priv system table.

#### <span id="page-55-0"></span>**Column Privileges**

Column privileges apply to single columns in a given table. Each privilege to be granted at the column level must be followed by the column or columns, enclosed within parentheses.

```
GRANT SELECT (col1), INSERT (col1, col2) ON mydb.mytbl TO 'someuser'@'somehost';
```

The permissible priv\_type values for a column (that is, when you use a column\_list clause) are INSERT, REFERENCES, SELECT, and UPDATE.

MySQL stores column privileges in the mysql.columns\_priv system table.

## <span id="page-55-1"></span>**Stored Routine Privileges**

The ALTER ROUTINE, CREATE ROUTINE, EXECUTE, and GRANT OPTION privileges apply to stored routines (procedures and functions). They can be granted at the global and database levels. Except for CREATE ROUTINE, these privileges can be granted at the routine level for individual routines.

```
GRANT CREATE ROUTINE ON mydb.* TO 'someuser'@'somehost';
GRANT EXECUTE ON PROCEDURE mydb.myproc TO 'someuser'@'somehost';
```

The permissible priv\_type values at the routine level are ALTER ROUTINE, EXECUTE, and GRANT OPTION. CREATE ROUTINE is not a routine-level privilege because you must have the privilege at the global or database level to create a routine in the first place.

MySQL stores routine-level privileges in the mysql.procs\_priv system table.

## <span id="page-55-2"></span>**Proxy User Privileges**

The PROXY privilege enables one user to be a proxy for another. The proxy user impersonates or takes the identity of the proxied user; that is, it assumes the privileges of the proxied user.

```
GRANT PROXY ON 'localuser'@'localhost' TO 'externaluser'@'somehost';
```

When PROXY is granted, it must be the only privilege named in the [GRANT](#page-45-0) statement, and the only permitted WITH option is WITH GRANT OPTION.

Proxying requires that the proxy user authenticate through a plugin that returns the name of the proxied user to the server when the proxy user connects, and that the proxy user have the PROXY privilege for the proxied user. For details and examples, see Section 8.2.19, "Proxy Users".

MySQL stores proxy privileges in the mysql.proxies\_priv system table.

#### <span id="page-55-3"></span>**Granting Roles**

GRANT syntax without an ON clause grants roles rather than individual privileges. A role is a named collection of privileges; see Section 8.2.10, "Using Roles". For example:

```
GRANT 'role1', 'role2' TO 'user1'@'localhost', 'user2'@'localhost';
```

Each role to be granted must exist, as well as each user account or role to which it is to be granted. As of MySQL 8.0.16, roles cannot be granted to anonymous users.

Granting a role does not automatically cause the role to be active. For information about role activation and inactivation, see Activating Roles.

These privileges are required to grant roles:

- If you have the ROLE\_ADMIN privilege (or the deprecated SUPER privilege), you can grant or revoke any role to users or roles.
- If you were granted a role with a [GRANT](#page-45-0) statement that includes the WITH ADMIN OPTION clause, you become able to grant that role to other users or roles, or revoke it from other users or roles, as long as the role is active at such time as you subsequently grant or revoke it. This includes the ability to use WITH ADMIN OPTION itself.

• To grant a role that has the SYSTEM\_USER privilege, you must have the SYSTEM\_USER privilege.

It is possible to create circular references with [GRANT](#page-45-0). For example:

```
CREATE USER 'u1', 'u2';
CREATE ROLE 'r1', 'r2';
GRANT 'u1' TO 'u1'; -- simple loop: u1 => u1
GRANT 'r1' TO 'r1'; -- simple loop: r1 => r1
GRANT 'r2' TO 'u2';
GRANT 'u2' TO 'r2'; -- mixed user/role loop: u2 => r2 => u2
```

Circular grant references are permitted but add no new privileges or roles to the grantee because a user or role already has its privileges and roles.

## <span id="page-56-0"></span>**The AS Clause and Privilege Restrictions**

As of MySQL 8.0.16, [GRANT](#page-45-0) has an AS user [WITH ROLE] clause that specifies additional information about the privilege context to use for statement execution. This syntax is visible at the SQL level, although its primary purpose is to enable uniform replication across all nodes of grantor privilege restrictions imposed by partial revokes, by causing those restrictions to appear in the binary log. For information about partial revokes, see Section 8.2.12, "Privilege Restriction Using Partial Revokes".

When the AS user clause is specified, statement execution takes into account any privilege restrictions associated with the named user, including all roles specified by WITH ROLE, if present. The result is that the privileges actually granted by the statement may be reduced relative to those specified.

These conditions apply to the AS user clause:

- AS has an effect only when the named user has privilege restrictions (which implies that the partial\_revokes system variable is enabled).
- If WITH ROLE is given, all roles named must be granted to the named user.
- The named user should be a MySQL account specified as 'user\_name'@'host\_name', CURRENT\_USER, or CURRENT\_USER(). The current user may be named together with WITH ROLE for the case that the executing user wants [GRANT](#page-45-0) to execute with a set of roles applied that may differ from the roles active within the current session.
- AS cannot be used to gain privileges not possessed by the user who executes the [GRANT](#page-45-0) statement. The executing user must have at least the privileges to be granted, but the AS clause can only restrict the privileges granted, not escalate them.
- With respect to the privileges to be granted, AS cannot specify a user/role combination that has more privileges (fewer restrictions) than the user who executes the [GRANT](#page-45-0) statement. The AS user/role combination is permitted to have more privileges than the executing user, but only if the statement does not grant those additional privileges.
- AS is supported only for granting global privileges (ON \*.\*).
- AS is not supported for PROXY grants.

The following example illustrates the effect of the AS clause. Create a user u1 that has some global privileges, as well as restrictions on those privileges:

```
CREATE USER u1;
GRANT SELECT, INSERT, UPDATE, DELETE ON *.* TO u1;
REVOKE INSERT, UPDATE ON schema1.* FROM u1;
REVOKE SELECT ON schema2.* FROM u1;
```

Also create a role r1 that lifts some of the privilege restrictions and grant the role to u1:

```
CREATE ROLE r1;
GRANT INSERT ON schema1.* TO r1;
GRANT SELECT ON schema2.* TO r1;
GRANT r1 TO u1;
```

Now, using an account that has no privilege restrictions of its own, grant to multiple users the same set of global privileges, but each with different restrictions imposed by the AS clause, and check which privileges are actually granted.

• The [GRANT](#page-45-0) statement here has no AS clause, so the privileges granted are exactly those specified:

```
mysql> CREATE USER u2;
mysql> GRANT SELECT, INSERT, UPDATE ON *.* TO u2;
mysql> SHOW GRANTS FOR u2;
+-------------------------------------------------+
| Grants for u2@% |
+-------------------------------------------------+
| GRANT SELECT, INSERT, UPDATE ON *.* TO `u2`@`%` |
+-------------------------------------------------+
```

• The [GRANT](#page-45-0) statement here has an AS clause, so the privileges granted are those specified but with the restrictions from u1 applied:

```
mysql> CREATE USER u3;
mysql> GRANT SELECT, INSERT, UPDATE ON *.* TO u3 AS u1;
mysql> SHOW GRANTS FOR u3;
+----------------------------------------------------+
| Grants for u3@% |
+----------------------------------------------------+
| GRANT SELECT, INSERT, UPDATE ON *.* TO `u3`@`%` |
| REVOKE INSERT, UPDATE ON `schema1`.* FROM `u3`@`%` |
| REVOKE SELECT ON `schema2`.* FROM `u3`@`%` |
+----------------------------------------------------+
```

As mentioned previously, the AS clause can only add privilege restrictions; it cannot escalate privileges. Thus, although u1 has the DELETE privilege, that is not included in the privileges granted because the statement does not specify granting DELETE.

• The AS clause for the [GRANT](#page-45-0) statement here makes the role r1 active for u1. That role lifts some of the restrictions on u1. Consequently, the privileges granted have some restrictions, but not so many as for the previous [GRANT](#page-45-0) statement:

```
mysql> CREATE USER u4;
mysql> GRANT SELECT, INSERT, UPDATE ON *.* TO u4 AS u1 WITH ROLE r1;
mysql> SHOW GRANTS FOR u4;
+-------------------------------------------------+
| Grants for u4@% |
+-------------------------------------------------+
| GRANT SELECT, INSERT, UPDATE ON *.* TO `u4`@`%` |
| REVOKE UPDATE ON `schema1`.* FROM `u4`@`%` |
+-------------------------------------------------+
```

If a [GRANT](#page-45-0) statement includes an AS user clause, privilege restrictions on the user who executes the statement are ignored (rather than applied as they would be in the absence of an AS clause).

#### <span id="page-57-0"></span>**Other Account Characteristics**

The optional WITH clause is used to enable a user to grant privileges to other users. The WITH GRANT OPTION clause gives the user the ability to give to other users any privileges the user has at the specified privilege level.

To grant the GRANT OPTION privilege to an account without otherwise changing its privileges, do this:

```
GRANT USAGE ON *.* TO 'someuser'@'somehost' WITH GRANT OPTION;
```

Be careful to whom you give the GRANT OPTION privilege because two users with different privileges may be able to combine privileges!

You cannot grant another user a privilege which you yourself do not have; the GRANT OPTION privilege enables you to assign only those privileges which you yourself possess.

Be aware that when you grant a user the GRANT OPTION privilege at a particular privilege level, any privileges the user possesses (or may be given in the future) at that level can also be granted by that user to other users. Suppose that you grant a user the INSERT privilege on a database. If you then grant the SELECT privilege on the database and specify WITH GRANT OPTION, that user can give to other users not only the SELECT privilege, but also INSERT. If you then grant the UPDATE privilege to the user on the database, the user can grant INSERT, SELECT, and UPDATE.

For a nonadministrative user, you should not grant the ALTER privilege globally or for the mysql system schema. If you do that, the user can try to subvert the privilege system by renaming tables!

For additional information about security risks associated with particular privileges, see Section 8.2.2, "Privileges Provided by MySQL".

## <span id="page-58-0"></span>**MySQL and Standard SQL Versions of GRANT**

The biggest differences between the MySQL and standard SQL versions of [GRANT](#page-45-0) are:

- MySQL associates privileges with the combination of a host name and user name and not with only a user name.
- Standard SQL does not have global or database-level privileges, nor does it support all the privilege types that MySQL supports.
- MySQL does not support the standard SQL UNDER privilege.
- Standard SQL privileges are structured in a hierarchical manner. If you remove a user, all privileges the user has been granted are revoked. This is also true in MySQL if you use [DROP USER](#page-44-0). See [Section 15.7.1.5, "DROP USER Statement"](#page-44-0).
- In standard SQL, when you drop a table, all privileges for the table are revoked. In standard SQL, when you revoke a privilege, all privileges that were granted based on that privilege are also revoked. In MySQL, privileges can be dropped with [DROP USER](#page-44-0) or [REVOKE](#page-59-0) statements.
- In MySQL, it is possible to have the INSERT privilege for only some of the columns in a table. In this case, you can still execute INSERT statements on the table, provided that you insert values only for those columns for which you have the INSERT privilege. The omitted columns are set to their implicit default values if strict SQL mode is not enabled. In strict mode, the statement is rejected if any of the omitted columns have no default value. (Standard SQL requires you to have the INSERT privilege on all columns.) For information about strict SQL mode and implicit default values, see Section 7.1.11, "Server SQL Modes", and Section 13.6, "Data Type Default Values".

## <span id="page-58-1"></span>**15.7.1.7 RENAME USER Statement**

```
RENAME USER old_user TO new_user
 [, old_user TO new_user] ...
```

The [RENAME USER](#page-58-1) statement renames existing MySQL accounts. An error occurs for old accounts that do not exist or new accounts that already exist.

To use [RENAME USER](#page-58-1), you must have the global CREATE USER privilege, or the UPDATE privilege for the mysql system schema. When the read\_only system variable is enabled, [RENAME USER](#page-58-1) additionally requires the CONNECTION\_ADMIN privilege (or the deprecated SUPER privilege).

As of MySQL 8.0.22, [RENAME USER](#page-58-1) fails with an error if any account to be renamed is named as the DEFINER attribute for any stored object. (That is, the statement fails if renaming an account would cause a stored object to become orphaned.) To perform the operation anyway, you must have the SET\_USER\_ID privilege; in this case, the statement succeeds with a warning rather than failing with an error. For additional information, including how to identify which objects name a given account as the DEFINER attribute, see Orphan Stored Objects.

Each account name uses the format described in Section 8.2.4, "Specifying Account Names". For example:

```
RENAME USER 'jeffrey'@'localhost' TO 'jeff'@'127.0.0.1';
```

The host name part of the account name, if omitted, defaults to '%'.

[RENAME USER](#page-58-1) causes the privileges held by the old user to be those held by the new user. However, [RENAME USER](#page-58-1) does not automatically drop or invalidate databases or objects within them that the old user created. This includes stored programs or views for which the DEFINER attribute names the old user. Attempts to access such objects may produce an error if they execute in definer security context. (For information about security context, see Section 27.6, "Stored Object Access Control".)

The privilege changes take effect as indicated in Section 8.2.13, "When Privilege Changes Take Effect".

## <span id="page-59-0"></span>**15.7.1.8 REVOKE Statement**

```
REVOKE [IF EXISTS]
 priv_type [(column_list)]
 [, priv_type [(column_list)]] ...
 ON [object_type] priv_level
 FROM user_or_role [, user_or_role] ...
 [IGNORE UNKNOWN USER]
REVOKE [IF EXISTS] ALL [PRIVILEGES], GRANT OPTION
 FROM user_or_role [, user_or_role] ...
 [IGNORE UNKNOWN USER]
REVOKE [IF EXISTS] PROXY ON user_or_role
 FROM user_or_role [, user_or_role] ...
 [IGNORE UNKNOWN USER]
REVOKE [IF EXISTS] role [, role ] ...
 FROM user_or_role [, user_or_role ] ...
 [IGNORE UNKNOWN USER]
user_or_role: {
 user (see Section 8.2.4, "Specifying Account Names")
 | role (see Section 8.2.5, "Specifying Role Names"
}
```

The [REVOKE](#page-59-0) statement enables system administrators to revoke privileges and roles, which can be revoked from user accounts and roles.

For details on the levels at which privileges exist, the permissible priv\_type, priv\_level, and object\_type values, and the syntax for specifying users and passwords, see [Section 15.7.1.6,](#page-45-0) ["GRANT Statement"](#page-45-0).

For information about roles, see Section 8.2.10, "Using Roles".

When the read\_only system variable is enabled, [REVOKE](#page-59-0) requires the CONNECTION\_ADMIN or privilege (or the deprecated SUPER privilege), in addition to any other required privileges described in the following discussion.

Beginning with MySQL 8.0.30, all the forms shown for REVOKE support an IF EXISTS option as well as an IGNORE UNKNOWN USER option. With neither of these modifications, [REVOKE](#page-59-0) either succeeds for all named users and roles, or rolls back and has no effect if any error occurs; the statement is written to the binary log only if it succeeds for all named users and roles. The precise effects of IF EXISTS and IGNORE UNKNOWN USER are discussed later in this section.

Each account name uses the format described in Section 8.2.4, "Specifying Account Names". Each role name uses the format described in Section 8.2.5, "Specifying Role Names". For example:

```
REVOKE INSERT ON *.* FROM 'jeffrey'@'localhost';
REVOKE 'role1', 'role2' FROM 'user1'@'localhost', 'user2'@'localhost';
```

```
REVOKE SELECT ON world.* FROM 'role3';
```

The host name part of the account or role name, if omitted, defaults to '%'.

To use the first [REVOKE](#page-59-0) syntax, you must have the GRANT OPTION privilege, and you must have the privileges that you are revoking.

To revoke all privileges from a user, use one of the following statements; either of these statements drops all global, database, table, column, and routine privileges for the named users or roles:

```
REVOKE ALL PRIVILEGES, GRANT OPTION
 FROM user_or_role [, user_or_role] ...
REVOKE ALL ON *.*
 FROM user_or_role [, user_or_role] ...
```

Neither of the two statements just shown revokes any roles.

To use these [REVOKE](#page-59-0) statements, you must have the global CREATE USER privilege, or the UPDATE privilege for the mysql system schema.

The syntax for which the [REVOKE](#page-59-0) keyword is followed by one or more role names takes a FROM clause indicating one or more users or roles from which to revoke the roles.

The IF EXISTS and IGNORE UNKNOWN USER options (MySQL 8.0.30 and later) have the effects listed here:

• IF EXISTS means that, if the target user or role exists but no such privilege or role is found assigned to the target for any reason, a warning is raised, instead of an error; if no privilege or role named by the statement is assigned to the target, the statement has no (other) effect. Otherwise, REVOKE executes normally; if the user does not exist, the statement raises an error.

Example: Given table t1 in database test, we execute the following statements, with the results shown.

```
mysql> CREATE USER jerry@localhost;
Query OK, 0 rows affected (0.01 sec)
mysql> REVOKE SELECT ON test.t1 FROM jerry@localhost;
ERROR 1147 (42000): There is no such grant defined for user 'jerry' on host
'localhost' on table 't1' 
mysql> REVOKE IF EXISTS SELECT ON test.t1 FROM jerry@localhost;
Query OK, 0 rows affected, 1 warning (0.00 sec)
mysql> SHOW WARNINGS\G
*************************** 1. row ***************************
 Level: Warning
 Code: 1147
Message: There is no such grant defined for user 'jerry' on host 'localhost' on
table 't1' 
1 row in set (0.00 sec)
```

IF EXISTS causes an error to be demoted to a warning even if the privilege or role named does not exist, or the statement attempts to assign it at the wrong level.

• If the REVOKE statement includes IGNORE UNKNOWN USER, the statement raises a warning for any target user or role named in the statement but not found; if no target named by the statement exists, REVOKE succeeds but has no actual effect. Otherwise, the statement executes as usual, and attempting to revoke a privilege not assigned to the target for whatever reason raises an error, as expected.

Example (continuing from the previous example):

```
mysql> DROP USER IF EXISTS jerry@localhost;
Query OK, 0 rows affected (0.01 sec)
```

```
mysql> REVOKE SELECT ON test.t1 FROM jerry@localhost;
ERROR 1147 (42000): There is no such grant defined for user 'jerry' on host
'localhost' on table 't1' 
mysql> REVOKE SELECT ON test.t1 FROM jerry@localhost IGNORE UNKNOWN USER;
Query OK, 0 rows affected, 1 warning (0.01 sec)
mysql> SHOW WARNINGS\G
*************************** 1. row ***************************
 Level: Warning
 Code: 3162
Message: Authorization ID jerry does not exist.
1 row in set (0.00 sec)
```

• The combination of IF EXISTS and IGNORE UNKNOWN USER means that REVOKE never raises an error for an unknown target user or role or for an unassigned or unavailable privilege, and the statement as whole in such cases succeeds; roles or privileges are removed from existing target users or roles whenever possible, and any revocation which is not possible raises a warning and executes as a NOOP.

Example (again continuing from example in the previous item):

```
# No such user, no such role
mysql> DROP ROLE IF EXISTS Bogus;
Query OK, 0 rows affected, 1 warning (0.02 sec)
mysql> SHOW WARNINGS;
+-------+------+----------------------------------------------+
| Level | Code | Message |
+-------+------+----------------------------------------------+
| Note | 3162 | Authorization ID 'Bogus'@'%' does not exist. |
+-------+------+----------------------------------------------+
1 row in set (0.00 sec)
# This statement attempts to revoke a nonexistent role from a nonexistent user
mysql> REVOKE Bogus ON test FROM jerry@localhost;
ERROR 3619 (HY000): Illegal privilege level specified for test
# The same, with IF EXISTS
mysql> REVOKE IF EXISTS Bogus ON test FROM jerry@localhost;
ERROR 1147 (42000): There is no such grant defined for user 'jerry' on host
'localhost' on table 'test' 
# The same, with IGNORE UNKNOWN USER
mysql> REVOKE Bogus ON test FROM jerry@localhost IGNORE UNKNOWN USER;
ERROR 3619 (HY000): Illegal privilege level specified for test
# The same, with both options
mysql> REVOKE IF EXISTS Bogus ON test FROM jerry@localhost IGNORE UNKNOWN USER;
Query OK, 0 rows affected, 2 warnings (0.01 sec)
mysql> SHOW WARNINGS;
+---------+------+--------------------------------------------+
| Level | Code | Message |
+---------+------+--------------------------------------------+
| Warning | 3619 | Illegal privilege level specified for test |
| Warning | 3162 | Authorization ID jerry does not exist. |
+---------+------+--------------------------------------------+
2 rows in set (0.00 sec)
```

Roles named in the mandatory\_roles system variable value cannot be revoked. When IF EXISTS and IGNORE UNKNOWN USER are used together in a statement that tries to remove a mandatory privilege, the error normally raised by attempting to do this is demoted to a warning; the statement executes successfully, but does not make any changes.

A revoked role immediately affects any user account from which it was revoked, such that within any current session for the account, its privileges are adjusted for the next statement executed.

Revoking a role revokes the role itself, not the privileges that it represents. Suppose that an account is granted a role that includes a given privilege, and is also granted the privilege explicitly or another role that includes the privilege. In this case, the account still possesses that privilege if the first role is revoked. For example, if an account is granted two roles that each include SELECT, the account still can select after either role is revoked.

REVOKE ALL ON \*.\* (at the global level) revokes all granted static global privileges and all granted dynamic privileges.

A revoked privilege that is granted but not known to the server is revoked with a warning. This situation can occur for dynamic privileges. For example, a dynamic privilege can be granted while the component that registers it is installed, but if that component is subsequently uninstalled, the privilege becomes unregistered, although accounts that possess the privilege still possess it and it can be revoked from them.

[REVOKE](#page-59-0) removes privileges, but does not remove rows from the mysql.user system table. To remove a user account entirely, use [DROP USER](#page-44-0). See [Section 15.7.1.5, "DROP USER Statement"](#page-44-0).

If the grant tables hold privilege rows that contain mixed-case database or table names and the lower\_case\_table\_names system variable is set to a nonzero value, [REVOKE](#page-59-0) cannot be used to revoke these privileges. It is necessary in such cases to manipulate the grant tables directly. ([GRANT](#page-45-0) does not create such rows when lower\_case\_table\_names is set, but such rows might have been created prior to setting the variable. The lower\_case\_table\_names setting can only be configured when initializing the server.)

When successfully executed from the mysql program, [REVOKE](#page-59-0) responds with Query OK, 0 rows affected. To determine what privileges remain after the operation, use [SHOW GRANTS](#page-115-0). See [Section 15.7.7.21, "SHOW GRANTS Statement".](#page-115-0)

## <span id="page-62-0"></span>**15.7.1.9 SET DEFAULT ROLE Statement**

```
SET DEFAULT ROLE
 {NONE | ALL | role [, role ] ...}
 TO user [, user ] ...
```

For each user named immediately after the TO keyword, this statement defines which roles become active when the user connects to the server and authenticates, or when the user executes the [SET](#page-65-0) [ROLE DEFAULT](#page-65-0) statement during a session.

[SET DEFAULT ROLE](#page-62-0) is alternative syntax for [ALTER USER ... DEFAULT ROLE](#page-14-0) (see [Section 15.7.1.1, "ALTER USER Statement"\)](#page-14-0). However, [ALTER USER](#page-14-0) can set the default for only a single user, whereas [SET DEFAULT ROLE](#page-62-0) can set the default for multiple users. On the other hand, you can specify CURRENT\_USER as the user name for the [ALTER USER](#page-14-0) statement, whereas you cannot for [SET DEFAULT ROLE](#page-62-0).

[SET DEFAULT ROLE](#page-62-0) requires these privileges:

- Setting the default roles for another user requires the global CREATE USER privilege, or the UPDATE privilege for the mysql.default\_roles system table.
- Setting the default roles for yourself requires no special privileges, as long as the roles you want as the default have been granted to you.

Each role name uses the format described in Section 8.2.5, "Specifying Role Names". For example:

```
SET DEFAULT ROLE 'admin', 'developer' TO 'joe'@'10.0.0.1';
```

The host name part of the role name, if omitted, defaults to '%'.

The clause following the DEFAULT ROLE keywords permits these values:

- NONE: Set the default to NONE (no roles).
- ALL: Set the default to all roles granted to the account.

• role [, role ] ...: Set the default to the named roles, which must exist and be granted to the account at the time [SET DEFAULT ROLE](#page-62-0) is executed.

![](_page_63_Picture_2.jpeg)

#### **Note**

[SET DEFAULT ROLE](#page-62-0) and [SET ROLE DEFAULT](#page-65-0) are different statements:

- [SET DEFAULT ROLE](#page-62-0) defines which account roles to activate by default within account sessions.
- [SET ROLE DEFAULT](#page-65-0) sets the active roles within the current session to the current account default roles.

For role usage examples, see Section 8.2.10, "Using Roles".

## <span id="page-63-0"></span>**15.7.1.10 SET PASSWORD Statement**

```
SET PASSWORD [FOR user] auth_option
 [REPLACE 'current_auth_string']
 [RETAIN CURRENT PASSWORD]
auth_option: {
 = 'auth_string'
 | TO RANDOM
}
```

The [SET PASSWORD](#page-63-0) statement assigns a password to a MySQL user account. The password may be either explicitly specified in the statement or randomly generated by MySQL. The statement may also include a password-verification clause that specifies the account current password to be replaced, and a clause that manages whether an account has a secondary password. 'auth\_string' and 'current\_auth\_string' each represent a cleartext (unencrypted) password.

![](_page_63_Picture_11.jpeg)

#### **Note**

Rather than using [SET PASSWORD](#page-63-0) to assign passwords, [ALTER USER](#page-14-0) is the preferred statement for account alterations, including assigning passwords. For example:

ALTER USER user IDENTIFIED BY 'auth\_string';

![](_page_63_Picture_15.jpeg)

#### **Note**

Clauses for random password generation, password verification, and secondary passwords apply only to accounts that use an authentication plugin that stores credentials internally to MySQL. For accounts that use a plugin that performs authentication against a credentials system that is external to MySQL, password management must be handled externally against that system as well. For more information about internal credentials storage, see Section 8.2.15, "Password Management".

The REPLACE 'current\_auth\_string' clause performs password verification and is available as of MySQL 8.0.13. If given:

- REPLACE specifies the account current password to be replaced, as a cleartext (unencrypted) string.
- The clause must be given if password changes for the account are required to specify the current password, as verification that the user attempting to make the change actually knows the current password.
- The clause is optional if password changes for the account may but need not specify the current password.
- The statement fails if the clause is given but does not match the current password, even if the clause is optional.

• REPLACE can be specified only when changing the account password for the current user.

For more information about password verification by specifying the current password, see Section 8.2.15, "Password Management".

The RETAIN CURRENT PASSWORD clause implements dual-password capability and is available as of MySQL 8.0.14. If given:

- RETAIN CURRENT PASSWORD retains an account current password as its secondary password, replacing any existing secondary password. The new password becomes the primary password, but clients can use the account to connect to the server using either the primary or secondary password. (Exception: If the new password specified by the [SET PASSWORD](#page-63-0) statement is empty, the secondary password becomes empty as well, even if RETAIN CURRENT PASSWORD is given.)
- If you specify RETAIN CURRENT PASSWORD for an account that has an empty primary password, the statement fails.
- If an account has a secondary password and you change its primary password without specifying RETAIN CURRENT PASSWORD, the secondary password remains unchanged.

For more information about use of dual passwords, see Section 8.2.15, "Password Management".

[SET PASSWORD](#page-63-0) permits these auth\_option syntaxes:

• = 'auth\_string'

Assigns the account the given literal password.

• TO RANDOM

Assigns the account a password randomly generated by MySQL. The statement also returns the cleartext password in a result set to make it available to the user or application executing the statement.

For details about the result set and characteristics of randomly generated passwords, see Random Password Generation.

Random password generation is available as of MySQL 8.0.18.

![](_page_64_Picture_15.jpeg)

#### **Important**

Under some circumstances, [SET PASSWORD](#page-63-0) may be recorded in server logs or on the client side in a history file such as ~/.mysql\_history, which means that cleartext passwords may be read by anyone having read access to that information. For information about the conditions under which this occurs for the server logs and how to control it, see Section 8.1.2.3, "Passwords and Logging". For similar information about client-side logging, see Section 6.5.1.3, "mysql Client Logging".

[SET PASSWORD](#page-63-0) can be used with or without a FOR clause that explicitly names a user account:

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

If a FOR user clause is given, the account name uses the format described in Section 8.2.4, "Specifying Account Names". For example:

```
SET PASSWORD FOR 'bob'@'%.example.org' = 'auth_string';
```

The host name part of the account name, if omitted, defaults to '%'.

[SET PASSWORD](#page-63-0) interprets the string as a cleartext string, passes it to the authentication plugin associated with the account, and stores the result returned by the plugin in the account row in the mysql.user system table. (The plugin is given the opportunity to hash the value into the encryption format it expects. The plugin may use the value as specified, in which case no hashing occurs.)

Setting the password for a named account (with a FOR clause) requires the UPDATE privilege for the mysql system schema. Setting the password for yourself (for a nonanonymous account with no FOR clause) requires no special privileges.

Statements that modify secondary passwords require these privileges:

- The APPLICATION\_PASSWORD\_ADMIN privilege is required to use the RETAIN CURRENT PASSWORD clause for [SET PASSWORD](#page-63-0) statements that apply to your own account. The privilege is required to manipulate your own secondary password because most users require only one password.
- If an account is to be permitted to manipulate secondary passwords for all accounts, it should be granted the CREATE USER privilege rather than APPLICATION\_PASSWORD\_ADMIN.

When the read\_only system variable is enabled, [SET PASSWORD](#page-63-0) requires the CONNECTION\_ADMIN privilege (or the deprecated SUPER privilege), in addition to any other required privileges.

For additional information about setting passwords and authentication plugins, see Section 8.2.14, "Assigning Account Passwords", and Section 8.2.17, "Pluggable Authentication".

## <span id="page-65-0"></span>**15.7.1.11 SET ROLE Statement**

```
SET ROLE {
 DEFAULT
 | NONE
 | ALL
 | ALL EXCEPT role [, role ] ...
 | role [, role ] ...
}
```

[SET ROLE](#page-65-0) modifies the current user's effective privileges within the current session by specifying which of its granted roles are active. Granted roles include those granted explicitly to the user and those named in the mandatory\_roles system variable value.

#### Examples:

```
SET ROLE DEFAULT;
SET ROLE 'role1', 'role2';
SET ROLE ALL;
SET ROLE ALL EXCEPT 'role1', 'role2';
```

Each role name uses the format described in Section 8.2.5, "Specifying Role Names". The host name part of the role name, if omitted, defaults to '%'.

Privileges that the user has been granted directly (rather than through roles) remain unaffected by changes to the active roles.

The statement permits these role specifiers:

• DEFAULT: Activate the account default roles. Default roles are those specified with [SET DEFAULT](#page-62-0) [ROLE](#page-62-0).

When a user connects to the server and authenticates successfully, the server determines which roles to activate as the default roles. If the activate\_all\_roles\_on\_login system variable is enabled, the server activates all granted roles. Otherwise, the server executes [SET ROLE DEFAULT](#page-65-0) implicitly. The server activates only default roles that can be activated. The server writes warnings to its error log for default roles that cannot be activated, but the client receives no warnings.

If a user executes [SET ROLE DEFAULT](#page-65-0) during a session, an error occurs if any default role cannot be activated (for example, if it does not exist or is not granted to the user). In this case, the current active roles are not changed.

- NONE: Set the active roles to NONE (no active roles).
- ALL: Activate all roles granted to the account.
- ALL EXCEPT role [, role ] ...: Activate all roles granted to the account except those named. The named roles need not exist or be granted to the account.
- role [, role ] ...: Activate the named roles, which must be granted to the account.

![](_page_66_Picture_8.jpeg)

#### **Note**

[SET DEFAULT ROLE](#page-62-0) and [SET ROLE DEFAULT](#page-65-0) are different statements:

- [SET DEFAULT ROLE](#page-62-0) defines which account roles to activate by default within account sessions.
- [SET ROLE DEFAULT](#page-65-0) sets the active roles within the current session to the current account default roles.

For role usage examples, see Section 8.2.10, "Using Roles".