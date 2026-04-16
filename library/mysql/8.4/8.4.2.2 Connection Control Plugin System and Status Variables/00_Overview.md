---
source: MySQL 8.4 Reference
title: 00_Overview
---

This section describes the system and status variables that the CONNECTION\_CONTROL plugin provides to enable its operation to be configured and monitored.

- [Connection Control Plugin System Variables](#page-190-2)
- [Connection Control Plugin Status Variables](#page-191-2)

# <span id="page-190-2"></span><span id="page-190-1"></span>**Connection Control Plugin System Variables**

If the CONNECTION\_CONTROL plugin is installed, it exposes these system variables:

• [connection\\_control\\_failed\\_connections\\_threshold](#page-190-1)

| Command-Line Format  | connection-control-failed<br>connections-threshold=# |  |
|----------------------|------------------------------------------------------|--|
| System Variable      | connection_control_failed_connections_threshold      |  |
| Scope                | Global                                               |  |
| Dynamic              | Yes                                                  |  |
| SET_VAR Hint Applies | No                                                   |  |
| Type                 | Integer                                              |  |
| Default Value        | 3                                                    |  |
| Minimum Value        | 0                                                    |  |
| Maximum Value        | 2147483647                                           |  |

The number of consecutive failed connection attempts permitted to accounts before the server adds a delay for subsequent connection attempts:

• If the variable has a nonzero value N, the server adds a delay beginning with consecutive failed attempt N+1. If an account has reached the point where connection responses are delayed, a delay also occurs for the next subsequent successful connection.

1361

• Setting this variable to zero disables failed-connection counting. In this case, the server never adds delays.

For information about how [connection\\_control\\_failed\\_connections\\_threshold](#page-190-1) interacts with other connection control system and status variables, see [Section 8.4.2.1, "Connection Control](#page-186-0) [Plugin Installation".](#page-186-0)

<span id="page-191-1"></span>• [connection\\_control\\_max\\_connection\\_delay](#page-191-1)

| Command-Line Format  | connection-control-max-connection<br>delay=# |
|----------------------|----------------------------------------------|
| System Variable      | connection_control_max_connection_delay      |
| Scope                | Global                                       |
| Dynamic              | Yes                                          |
| SET_VAR Hint Applies | No                                           |
| Type                 | Integer                                      |
| Default Value        | 2147483647                                   |
| Minimum Value        | 1000                                         |
| Maximum Value        | 2147483647                                   |
| Unit                 | milliseconds                                 |

The maximum delay in milliseconds for server response to failed connection attempts, if [connection\\_control\\_failed\\_connections\\_threshold](#page-190-1) is greater than zero.

For information about how [connection\\_control\\_max\\_connection\\_delay](#page-191-1) interacts with other connection control system and status variables, see [Section 8.4.2.1, "Connection Control Plugin](#page-186-0) [Installation"](#page-186-0).

<span id="page-191-0"></span>• [connection\\_control\\_min\\_connection\\_delay](#page-191-0)

| Command-Line Format  | connection-control-min-connection<br>delay=# |
|----------------------|----------------------------------------------|
| System Variable      | connection_control_min_connection_delay      |
| Scope                | Global                                       |
| Dynamic              | Yes                                          |
| SET_VAR Hint Applies | No                                           |
| Type                 | Integer                                      |
| Default Value        | 1000                                         |
| Minimum Value        | 1000                                         |
| Maximum Value        | 2147483647                                   |
| Unit                 | milliseconds                                 |

The minimum delay in milliseconds for server response to failed connection attempts, if [connection\\_control\\_failed\\_connections\\_threshold](#page-190-1) is greater than zero.

For information about how [connection\\_control\\_min\\_connection\\_delay](#page-191-0) interacts with other connection control system and status variables, see [Section 8.4.2.1, "Connection Control Plugin](#page-186-0) [Installation"](#page-186-0).

### <span id="page-191-2"></span>**Connection Control Plugin Status Variables**

If the CONNECTION\_CONTROL plugin is installed, it exposes this status variable:

<span id="page-192-1"></span>• [Connection\\_control\\_delay\\_generated](#page-192-1)

The number of times the server added a delay to its response to a failed connection attempt. This does not count attempts that occur before reaching the threshold defined by the [connection\\_control\\_failed\\_connections\\_threshold](#page-190-1) system variable.

This variable provides a simple counter. For more detailed connection control monitoring information, examine the INFORMATION\_SCHEMA CONNECTION\_CONTROL\_FAILED\_LOGIN\_ATTEMPTS table; see Section 28.6.2, "The INFORMATION\_SCHEMA CONNECTION\_CONTROL\_FAILED\_LOGIN\_ATTEMPTS Table".

Assigning a value to [connection\\_control\\_failed\\_connections\\_threshold](#page-190-1) at runtime resets [Connection\\_control\\_delay\\_generated](#page-192-1) to zero.

# <span id="page-192-0"></span>**8.4.3 The Password Validation Component**

The validate\_password component serves to improve security by requiring account passwords and enabling strength testing of potential passwords. This component exposes system variables that enable you to configure password policy, and status variables for component monitoring.

The validate\_password component implements these capabilities:

- For SQL statements that assign a password supplied as a cleartext value, validate\_password checks the password against the current password policy and rejects the password if it is weak (the statement returns an [ER\\_NOT\\_VALID\\_PASSWORD](https://dev.mysql.com/doc/mysql-errors/8.4/en/server-error-reference.md#error_er_not_valid_password) error). This applies to the ALTER USER, CREATE USER, and SET PASSWORD statements.
- For CREATE USER statements, validate\_password requires that a password be given, and that it satisfies the password policy. This is true even if an account is locked initially because otherwise unlocking the account later would cause it to become accessible without a password that satisfies the policy.
- validate\_password implements a VALIDATE\_PASSWORD\_STRENGTH() SQL function that assesses the strength of potential passwords. This function takes a password argument and returns an integer from 0 (weak) to 100 (strong).

![](_page_192_Picture_11.jpeg)

### **Note**

For statements that assign or modify account passwords (ALTER USER, CREATE USER, and SET PASSWORD), the validate\_password capabilities described here apply only to accounts that use an authentication plugin that stores credentials internally to MySQL. For accounts that use plugins that perform authentication against a credentials system external to MySQL, password management must be handled externally against that system as well. For more information about internal credentials storage, see [Section 8.2.15,](#page-28-0) ["Password Management".](#page-28-0)

The preceding restriction does not apply to use of the VALIDATE\_PASSWORD\_STRENGTH() function because it does not affect accounts directly.

#### Examples:

• validate\_password checks the cleartext password in the following statement. Under the default password policy, which requires passwords to be at least 8 characters long, the password is weak and the statement produces an error:

```
mysql> ALTER USER USER() IDENTIFIED BY 'abc';
ERROR 1819 (HY000): Your password does not satisfy the current
policy requirements
```

• Passwords specified as hashed values are not checked because the original password value is not available for checking:

```
mysql> ALTER USER 'jeffrey'@'localhost'
 IDENTIFIED WITH mysql_native_password
 AS '*0D3CED9BEC10A777AEC23CCC353A8C08A633045E';
Query OK, 0 rows affected (0.01 sec)
```

• This account-creation statement fails, even though the account is locked initially, because it does not include a password that satisfies the current password policy:

```
mysql> CREATE USER 'juanita'@'localhost' ACCOUNT LOCK;
ERROR 1819 (HY000): Your password does not satisfy the current
policy requirements
```

• To check a password, use the VALIDATE\_PASSWORD\_STRENGTH() function:

```
mysql> SELECT VALIDATE_PASSWORD_STRENGTH('weak');
+------------------------------------+
| VALIDATE_PASSWORD_STRENGTH('weak') |
+------------------------------------+
| 25 |
+------------------------------------+
mysql> SELECT VALIDATE_PASSWORD_STRENGTH('lessweak$_@123');
+----------------------------------------------+
| VALIDATE_PASSWORD_STRENGTH('lessweak$_@123') |
+----------------------------------------------+
| 50 |
+----------------------------------------------+
mysql> SELECT VALIDATE_PASSWORD_STRENGTH('N0Tweak$_@123!');
+----------------------------------------------+
| VALIDATE_PASSWORD_STRENGTH('N0Tweak$_@123!') |
+----------------------------------------------+
| 100 |
+----------------------------------------------+
```

To configure password checking, modify the system variables having names of the form validate\_password.xxx; these are the parameters that control password policy. See [Section 8.4.3.2, "Password Validation Options and Variables".](#page-194-0)

If validate\_password is not installed, the validate\_password.xxx system variables are not available, passwords in statements are not checked, and the VALIDATE\_PASSWORD\_STRENGTH() function always returns 0. For example, without the plugin installed, accounts can be assigned passwords shorter than 8 characters, or no password at all.

Assuming that validate\_password is installed, it implements three levels of password checking: LOW, MEDIUM, and STRONG. The default is MEDIUM; to change this, modify the value of [validate\\_password.policy](#page-198-0). The policies implement increasingly strict password tests. The following descriptions refer to default parameter values, which can be modified by changing the appropriate system variables.

- LOW policy tests password length only. Passwords must be at least 8 characters long. To change this length, modify [validate\\_password.length](#page-197-0).
- MEDIUM policy adds the conditions that passwords must contain at least 1 numeric character, 1 lowercase character, 1 uppercase character, and 1 special (nonalphanumeric) character. To change these values, modify [validate\\_password.number\\_count](#page-198-1), [validate\\_password.mixed\\_case\\_count](#page-197-1), and [validate\\_password.special\\_char\\_count](#page-199-0).
- STRONG policy adds the condition that password substrings of length 4 or longer must not match words in the dictionary file, if one has been specified. To specify the dictionary file, modify [validate\\_password.dictionary\\_file](#page-196-0).

In addition, validate\_password supports the capability of rejecting passwords that match the user name part of the effective user account for the current session, either forward

or in reverse. To provide control over this capability, validate\_password exposes a [validate\\_password.check\\_user\\_name](#page-195-0) system variable, which is enabled by default.