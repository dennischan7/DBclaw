---
source: MySQL 8.0 Reference
title: 00_Overview
---

This section describes the system and status variables that the CONNECTION\_CONTROL plugin provides to enable its operation to be configured and monitored.

- [Connection Control Plugin System Variables](#page-129-2)
- [Connection Control Plugin Status Variables](#page-130-2)

# <span id="page-129-2"></span><span id="page-129-1"></span>**Connection Control Plugin System Variables**

If the CONNECTION\_CONTROL plugin is installed, it exposes these system variables:

• [connection\\_control\\_failed\\_connections\\_threshold](#page-129-1)

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

1500

• Setting this variable to zero disables failed-connection counting. In this case, the server never adds delays.

For information about how [connection\\_control\\_failed\\_connections\\_threshold](#page-129-1) interacts with other connection control system and status variables, see [Section 8.4.2.1, "Connection Control](#page-125-0) [Plugin Installation".](#page-125-0)

<span id="page-130-1"></span>• [connection\\_control\\_max\\_connection\\_delay](#page-130-1)

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

The maximum delay in milliseconds for server response to failed connection attempts, if [connection\\_control\\_failed\\_connections\\_threshold](#page-129-1) is greater than zero.

For information about how [connection\\_control\\_max\\_connection\\_delay](#page-130-1) interacts with other connection control system and status variables, see [Section 8.4.2.1, "Connection Control Plugin](#page-125-0) [Installation"](#page-125-0).

<span id="page-130-0"></span>• [connection\\_control\\_min\\_connection\\_delay](#page-130-0)

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

The minimum delay in milliseconds for server response to failed connection attempts, if [connection\\_control\\_failed\\_connections\\_threshold](#page-129-1) is greater than zero.

For information about how [connection\\_control\\_min\\_connection\\_delay](#page-130-0) interacts with other connection control system and status variables, see [Section 8.4.2.1, "Connection Control Plugin](#page-125-0) [Installation"](#page-125-0).

# <span id="page-130-2"></span>**Connection Control Plugin Status Variables**

If the CONNECTION\_CONTROL plugin is installed, it exposes this status variable:

<span id="page-131-1"></span>• [Connection\\_control\\_delay\\_generated](#page-131-1)

The number of times the server added a delay to its response to a failed connection attempt. This does not count attempts that occur before reaching the threshold defined by the [connection\\_control\\_failed\\_connections\\_threshold](#page-129-1) system variable.

This variable provides a simple counter. For more detailed connection control monitoring information, examine the INFORMATION\_SCHEMA CONNECTION\_CONTROL\_FAILED\_LOGIN\_ATTEMPTS table; see Section 28.6.2, "The INFORMATION\_SCHEMA CONNECTION\_CONTROL\_FAILED\_LOGIN\_ATTEMPTS Table".

Assigning a value to [connection\\_control\\_failed\\_connections\\_threshold](#page-129-1) at runtime resets [Connection\\_control\\_delay\\_generated](#page-131-1) to zero.

# <span id="page-131-0"></span>**8.4.3 The Password Validation Component**

The validate\_password component serves to improve security by requiring account passwords and enabling strength testing of potential passwords. This component exposes system variables that enable you to configure password policy, and status variables for component monitoring.

![](_page_131_Picture_7.jpeg)

#### **Note**

In MySQL 8.0, the validate\_password plugin was reimplemented as the validate\_password component. (For general information about components, see Section 7.5, "MySQL Components".) The following instructions describe how to use the component, not the plugin. For instructions on using the plugin form of validate\_password, see [The Password Validation Plugin,](https://dev.mysql.com/doc/refman/5.7/en/validate-password.md) in [MySQL](https://dev.mysql.com/doc/refman/5.7/en/) [5.7 Reference Manual.](https://dev.mysql.com/doc/refman/5.7/en/)

The plugin form of validate\_password is still available but is deprecated; expect it to be removed in a future version of MySQL. MySQL installations that use the plugin should make the transition to using the component instead. See [Section 8.4.3.3, "Transitioning to the Password Validation Component"](#page-142-0).

The validate\_password component implements these capabilities:

- For SQL statements that assign a password supplied as a cleartext value, validate\_password checks the password against the current password policy and rejects the password if it is weak (the statement returns an [ER\\_NOT\\_VALID\\_PASSWORD](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_not_valid_password) error). This applies to the ALTER USER, CREATE USER, and SET PASSWORD statements.
- For CREATE USER statements, validate\_password requires that a password be given, and that it satisfies the password policy. This is true even if an account is locked initially because otherwise unlocking the account later would cause it to become accessible without a password that satisfies the policy.
- validate\_password implements a VALIDATE\_PASSWORD\_STRENGTH() SQL function that assesses the strength of potential passwords. This function takes a password argument and returns an integer from 0 (weak) to 100 (strong).

![](_page_131_Picture_15.jpeg)

#### **Note**

For statements that assign or modify account passwords (ALTER USER, CREATE USER, and SET PASSWORD), the validate\_password capabilities described here apply only to accounts that use an authentication plugin that stores credentials internally to MySQL. For accounts that use plugins that perform authentication against a credentials system external to MySQL, password management must be handled externally against that system as well. For more information about internal credentials storage, see Section 8.2.15, "Password Management".

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

To configure password checking, modify the system variables having names of the form validate\_password.xxx; these are the parameters that control password policy. See [Section 8.4.3.2, "Password Validation Options and Variables".](#page-133-0)

If validate\_password is not installed, the validate\_password.xxx system variables are not available, passwords in statements are not checked, and the VALIDATE\_PASSWORD\_STRENGTH() function always returns 0. For example, without the plugin installed, accounts can be assigned passwords shorter than 8 characters, or no password at all.

Assuming that validate\_password is installed, it implements three levels of password checking: LOW, MEDIUM, and STRONG. The default is MEDIUM; to change this, modify the value of [validate\\_password.policy](#page-137-0). The policies implement increasingly strict password tests. The following descriptions refer to default parameter values, which can be modified by changing the appropriate system variables.

- LOW policy tests password length only. Passwords must be at least 8 characters long. To change this length, modify [validate\\_password.length](#page-136-0).
- MEDIUM policy adds the conditions that passwords must contain at least 1 numeric character, 1 lowercase character, 1 uppercase character, and 1 special (nonalphanumeric) character. To change these values, modify [validate\\_password.number\\_count](#page-137-1), [validate\\_password.mixed\\_case\\_count](#page-136-1), and [validate\\_password.special\\_char\\_count](#page-138-0).
- STRONG policy adds the condition that password substrings of length 4 or longer must not match words in the dictionary file, if one has been specified. To specify the dictionary file, modify [validate\\_password.dictionary\\_file](#page-135-0).

In addition, validate\_password supports the capability of rejecting passwords that match the user name part of the effective user account for the current session, either forward or in reverse. To provide control over this capability, validate\_password exposes a [validate\\_password.check\\_user\\_name](#page-135-1) system variable, which is enabled by default.

# <span id="page-133-1"></span>**8.4.3.1 Password Validation Component Installation and Uninstallation**

This section describes how to install and uninstall the validate\_password password-validation component. For general information about installing and uninstalling components, see Section 7.5, "MySQL Components".

![](_page_133_Picture_7.jpeg)

### **Note**

If you install MySQL 8.0 using the [MySQL Yum repository](https://dev.mysql.com/downloads/repo/yum/), [MySQL SLES](https://dev.mysql.com/downloads/repo/suse/) [Repository,](https://dev.mysql.com/downloads/repo/suse/) or RPM packages provided by Oracle, the validate\_password component is enabled by default after you start your MySQL Server for the first time.

Upgrades to MySQL 8.0 from 5.7 using Yum or RPM packages leave the validate\_password plugin in place. To make the transition from the validate\_password plugin to the validate\_password component, see [Section 8.4.3.3, "Transitioning to the Password Validation Component"](#page-142-0).

To be usable by the server, the component library file must be located in the MySQL plugin directory (the directory named by the plugin\_dir system variable). If necessary, configure the plugin directory location by setting the value of plugin\_dir at server startup.

To install the validate\_password component, use this statement:

```
INSTALL COMPONENT 'file://component_validate_password';
```

Component installation is a one-time operation that need not be done per server startup. INSTALL COMPONENT loads the component, and also registers it in the mysql.component system table to cause it to be loaded during subsequent server startups.

To uninstall the validate\_password component, use this statement:

```
UNINSTALL COMPONENT 'file://component_validate_password';
```

UNINSTALL COMPONENT unloads the component, and unregisters it from the mysql.component system table to cause it not to be loaded during subsequent server startups.

# <span id="page-133-0"></span>**8.4.3.2 Password Validation Options and Variables**

This section describes the system and status variables that validate\_password provides to enable its operation to be configured and monitored.

- [Password Validation Component System Variables](#page-134-0)
- [Password Validation Component Status Variables](#page-138-1)

- [Password Validation Plugin Options](#page-138-2)
- [Password Validation Plugin System Variables](#page-139-0)
- [Password Validation Plugin Status Variables](#page-141-0)

## <span id="page-134-0"></span>**Password Validation Component System Variables**

If the validate\_password component is enabled, it exposes several system variables that enable configuration of password checking:

```
mysql> SHOW VARIABLES LIKE 'validate_password.%';
+-------------------------------------------------+--------+
| Variable_name | Value |
+-------------------------------------------------+--------+
| validate_password.changed_characters_percentage | 0 |
| validate_password.check_user_name | ON |
| validate_password.dictionary_file | |
| validate_password.length | 8 |
| validate_password.mixed_case_count | 1 |
| validate_password.number_count | 1 |
| validate_password.policy | MEDIUM |
| validate_password.special_char_count | 1 |
+-------------------------------------------------+--------+
```

To change how passwords are checked, you can set these system variables at server startup or at runtime. The following list describes the meaning of each variable.

<span id="page-134-1"></span>• [validate\\_password.changed\\_characters\\_percentage](#page-134-1)

| Command-Line Format  | validate-password.changed<br>characters-percentage[=value] |  |
|----------------------|------------------------------------------------------------|--|
| System Variable      | validate_password.changed_characters_percentage            |  |
| Scope                | Global                                                     |  |
| Dynamic              | Yes                                                        |  |
| SET_VAR Hint Applies | No                                                         |  |
| Type                 | Integer                                                    |  |
| Default Value        | 0                                                          |  |
| Minimum Value        | 0                                                          |  |
| Maximum Value        | 100                                                        |  |
|                      |                                                            |  |

Indicates the minimum number of characters, as a percentage of all characters, in a password that a user must change before validate\_password accepts a new password for the user's own account. This applies only when changing an existing password, and has no effect when setting a user account's initial password.

This variable is not available unless validate\_password is installed.

By default, validate\_password.changed\_characters\_percentage permits all of the characters from the current password to be reused in the new password. The range of valid percentages is 0 to 100. If set to 100 percent, all of the characters from the current password are rejected, regardless of the casing. Characters 'abc' and 'ABC' are considered to be the same characters. If validate\_password rejects the new password, it reports an error indicating the minimum number of characters that must differ.

If the ALTER USER statement does not provide the existing password in a REPLACE clause, this variable is not enforced. Whether the REPLACE clause is required is subject to the password verification policy as it applies to a given account. For an overview of the policy, see Password Verification-Required Policy.

<span id="page-135-1"></span>• [validate\\_password.check\\_user\\_name](#page-135-1)

| Command-Line Format  | validate-password.check-user<br>name[={OFF ON}] |
|----------------------|-------------------------------------------------|
| System Variable      | validate_password.check_user_name               |
| Scope                | Global                                          |
| Dynamic              | Yes                                             |
| SET_VAR Hint Applies | No                                              |
| Type                 | Boolean                                         |
| Default Value        | ON                                              |

Whether validate\_password compares passwords to the user name part of the effective user account for the current session and rejects them if they match. This variable is unavailable unless validate\_password is installed.

By default, [validate\\_password.check\\_user\\_name](#page-135-1) is enabled. This variable controls user name matching independent of the value of [validate\\_password.policy](#page-137-0).

When [validate\\_password.check\\_user\\_name](#page-135-1) is enabled, it has these effects:

- Checking occurs in all contexts for which validate\_password is invoked, which includes use of statements such as ALTER USER or SET PASSWORD to change the current user's password, and invocation of functions such as VALIDATE\_PASSWORD\_STRENGTH().
- The user names used for comparison are taken from the values of the USER() and CURRENT\_USER() functions for the current session. An implication is that a user who has sufficient privileges to set another user's password can set the password to that user's name, and cannot set that user' password to the name of the user executing the statement. For example, 'root'@'localhost' can set the password for 'jeffrey'@'localhost' to 'jeffrey', but cannot set the password to 'root.
- Only the user name part of the USER() and CURRENT\_USER() function values is used, not the host name part. If a user name is empty, no comparison occurs.
- If a password is the same as the user name or its reverse, a match occurs and the password is rejected.
- User-name matching is case-sensitive. The password and user name values are compared as binary strings on a byte-by-byte basis.
- If a password matches the user name, VALIDATE\_PASSWORD\_STRENGTH() returns 0 regardless of how other validate\_password system variables are set.
- <span id="page-135-0"></span>• [validate\\_password.dictionary\\_file](#page-135-0)

| Command-Line Format  | validate-password.dictionary<br>file=file_name |
|----------------------|------------------------------------------------|
| System Variable      | validate_password.dictionary_file              |
| Scope                | Global                                         |
| Dynamic              | Yes                                            |
| SET_VAR Hint Applies | No                                             |

The path name of the dictionary file that validate\_password uses for checking passwords. This variable is unavailable unless validate\_password is installed.

By default, this variable has an empty value and dictionary checks are not performed. For dictionary checks to occur, the variable value must be nonempty. If the file is named as a relative path, it is interpreted relative to the server data directory. File contents should be lowercase, one word per line. Contents are treated as having a character set of utf8mb3. The maximum permitted file size is 1MB.

For the dictionary file to be used during password checking, the password policy must be set to 2 (STRONG); see the description of the [validate\\_password.policy](#page-137-0) system variable. Assuming that is true, each substring of the password of length 4 up to 100 is compared to the words in the dictionary file. Any match causes the password to be rejected. Comparisons are not case-sensitive.

For VALIDATE\_PASSWORD\_STRENGTH(), the password is checked against all policies, including STRONG, so the strength assessment includes the dictionary check regardless of the [validate\\_password.policy](#page-137-0) value.

[validate\\_password.dictionary\\_file](#page-135-0) can be set at runtime and assigning a value causes the named file to be read without a server restart.

<span id="page-136-0"></span>• [validate\\_password.length](#page-136-0)

| Command-Line Format  | validate-password.length=# |
|----------------------|----------------------------|
| System Variable      | validate_password.length   |
| Scope                | Global                     |
| Dynamic              | Yes                        |
| SET_VAR Hint Applies | No                         |
| Type                 | Integer                    |
| Default Value        | 8                          |
| Minimum Value        | 0                          |

The minimum number of characters that validate\_password requires passwords to have. This variable is unavailable unless validate\_password is installed.

The [validate\\_password.length](#page-136-0) minimum value is a function of several other related system variables. The value cannot be set less than the value of this expression:

```
validate_password.number_count
+ validate_password.special_char_count
+ (2 * validate_password.mixed_case_count)
```

If validate\_password adjusts the value of [validate\\_password.length](#page-136-0) due to the preceding constraint, it writes a message to the error log.

<span id="page-136-1"></span>• [validate\\_password.mixed\\_case\\_count](#page-136-1)

| Command-Line Format  | validate-password.mixed-case       |
|----------------------|------------------------------------|
|                      | count=#                            |
| System Variable      | validate_password.mixed_case_count |
| Scope                | Global                             |
| Dynamic              | Yes                                |
| SET_VAR Hint Applies | No                                 |
| Type                 | Integer<br>1507                    |

| Default Value | 1 |
|---------------|---|
| Minimum Value | 0 |

The minimum number of lowercase and uppercase characters that validate\_password requires passwords to have if the password policy is MEDIUM or stronger. This variable is unavailable unless validate\_password is installed.

For a given [validate\\_password.mixed\\_case\\_count](#page-136-1) value, the password must have that many lowercase characters, and that many uppercase characters.

<span id="page-137-1"></span>• [validate\\_password.number\\_count](#page-137-1)

| Command-Line Format  | validate-password.number-count=# |
|----------------------|----------------------------------|
| System Variable      | validate_password.number_count   |
| Scope                | Global                           |
| Dynamic              | Yes                              |
| SET_VAR Hint Applies | No                               |
| Type                 | Integer                          |
| Default Value        | 1                                |
| Minimum Value        | 0                                |

The minimum number of numeric (digit) characters that validate\_password requires passwords to have if the password policy is MEDIUM or stronger. This variable is unavailable unless validate\_password is installed.

<span id="page-137-0"></span>• [validate\\_password.policy](#page-137-0)

| Command-Line Format  | validate-password.policy=value |
|----------------------|--------------------------------|
| System Variable      | validate_password.policy       |
| Scope                | Global                         |
| Dynamic              | Yes                            |
| SET_VAR Hint Applies | No                             |
| Type                 | Enumeration                    |
| Default Value        | 1                              |
| Valid Values         | 0                              |
|                      | 1                              |
|                      | 2                              |

The password policy enforced by validate\_password. This variable is unavailable unless validate\_password is installed.

[validate\\_password.policy](#page-137-0) affects how validate\_password uses its other policysetting system variables, except for checking passwords against user names, which is controlled independently by [validate\\_password.check\\_user\\_name](#page-135-1).

The [validate\\_password.policy](#page-137-0) value can be specified using numeric values 0, 1, 2, or the corresponding symbolic values LOW, MEDIUM, STRONG. The following table describes the tests performed for each policy. For the length test, the required length is the value of the [validate\\_password.length](#page-136-0) system variable. Similarly, the required values for the other tests are given by other validate\_password.xxx variables.

| Policy      | Tests Performed                                                                  |
|-------------|----------------------------------------------------------------------------------|
| 0 or LOW    | Length                                                                           |
| 1 or MEDIUM | Length; numeric, lowercase/uppercase, and<br>special characters                  |
| 2 or STRONG | Length; numeric, lowercase/uppercase, and<br>special characters; dictionary file |

<span id="page-138-0"></span>• [validate\\_password.special\\_char\\_count](#page-138-0)

| Command-Line Format  | validate-password.special-char<br>count=# |
|----------------------|-------------------------------------------|
| System Variable      | validate_password.special_char_count      |
| Scope                | Global                                    |
| Dynamic              | Yes                                       |
| SET_VAR Hint Applies | No                                        |
| Type                 | Integer                                   |
| Default Value        | 1                                         |
| Minimum Value        | 0                                         |

The minimum number of nonalphanumeric characters that validate\_password requires passwords to have if the password policy is MEDIUM or stronger. This variable is unavailable unless validate\_password is installed.

# <span id="page-138-1"></span>**Password Validation Component Status Variables**

If the validate\_password component is enabled, it exposes status variables that provide operational information:

| mysql> SHOW STATUS LIKE 'validate_password.%';                                                                                                  |           |
|-------------------------------------------------------------------------------------------------------------------------------------------------|-----------|
| +++<br>  Variable_name                                                                                                                          | Value<br> |
| +++<br>  validate_password.dictionary_file_last_parsed   2019-10-03 08:33:49  <br>  validate_password.dictionary_file_words_count   1902<br>+++ |           |

The following list describes the meaning of each status variable.

<span id="page-138-3"></span>• [validate\\_password.dictionary\\_file\\_last\\_parsed](#page-138-3)

When the dictionary file was last parsed. This variable is unavailable unless validate\_password is installed.

<span id="page-138-4"></span>• [validate\\_password.dictionary\\_file\\_words\\_count](#page-138-4)

The number of words read from the dictionary file. This variable is unavailable unless validate\_password is installed.

## <span id="page-138-2"></span>**Password Validation Plugin Options**

![](_page_138_Picture_15.jpeg)

## **Note**

In MySQL 8.0, the validate\_password plugin was reimplemented as the validate\_password component. The validate\_password plugin is deprecated; expect it to be removed in a future version of MySQL. Consequently, its options are also deprecated, and you should expect them to be removed as well. MySQL installations that use the plugin should make the transition to using the component instead. See [Section 8.4.3.3, "Transitioning to](#page-142-0) [the Password Validation Component"](#page-142-0).

To control activation of the validate\_password plugin, use this option:

<span id="page-139-1"></span>• [--validate-password\[=](#page-139-1)value]

| Command-Line Format | validate-password[=value] |
|---------------------|---------------------------|
| Type                | Enumeration               |
| Default Value       | ON                        |
| Valid Values        | ON                        |
|                     | OFF                       |
|                     | FORCE                     |
|                     | FORCE_PLUS_PERMANENT      |

This option controls how the server loads the deprecated validate\_password plugin at startup. The value should be one of those available for plugin-loading options, as described in Section 7.6.1, "Installing and Uninstalling Plugins". For example, [--validate](#page-139-1)[password=FORCE\\_PLUS\\_PERMANENT](#page-139-1) tells the server to load the plugin at startup and prevents it from being removed while the server is running.

This option is available only if the validate\_password plugin has been previously registered with INSTALL PLUGIN or is loaded with --plugin-load-add. See [Section 8.4.3.1, "Password](#page-133-1) [Validation Component Installation and Uninstallation".](#page-133-1)

## <span id="page-139-0"></span>**Password Validation Plugin System Variables**

![](_page_139_Picture_8.jpeg)

# **Note**

In MySQL 8.0, the validate\_password plugin was reimplemented as the validate\_password component. The validate\_password plugin is deprecated; expect it to be removed in a future version of MySQL. Consequently, its system variables are also deprecated and you should expect them to be removed as well. Use the corresponding system variables of the validate\_password component instead; see [Password Validation](#page-134-0) [Component System Variables](#page-134-0). MySQL installations that use the plugin should make the transition to using the component instead. See [Section 8.4.3.3,](#page-142-0) ["Transitioning to the Password Validation Component".](#page-142-0)

<span id="page-139-2"></span>• [validate\\_password\\_check\\_user\\_name](#page-139-2)

| Command-Line Format  | validate-password-check-user<br>name[={OFF ON}] |
|----------------------|-------------------------------------------------|
| System Variable      | validate_password_check_user_name               |
| Scope                | Global                                          |
| Dynamic              | Yes                                             |
| SET_VAR Hint Applies | No                                              |
| Type                 | Boolean                                         |
| Default Value        | ON                                              |

This validate\_password plugin system variable is deprecated; expect it to be removed in a future version of MySQL. Use the corresponding [validate\\_password.check\\_user\\_name](#page-135-1) system variable of the validate\_password component instead.

<span id="page-140-0"></span>• [validate\\_password\\_dictionary\\_file](#page-140-0)

| Command-Line Format  | validate-password-dictionary<br>file=file_name |
|----------------------|------------------------------------------------|
| System Variable      | validate_password_dictionary_file              |
| Scope                | Global                                         |
| Dynamic              | Yes                                            |
| SET_VAR Hint Applies | No                                             |
| Type                 | File name                                      |

This validate\_password plugin system variable is deprecated; expect it to be removed in a future version of MySQL. Use the corresponding [validate\\_password.dictionary\\_file](#page-135-0) system variable of the validate\_password component instead.

<span id="page-140-1"></span>• [validate\\_password\\_length](#page-140-1)

| Command-Line Format  | validate-password-length=# |
|----------------------|----------------------------|
| System Variable      | validate_password_length   |
| Scope                | Global                     |
| Dynamic              | Yes                        |
| SET_VAR Hint Applies | No                         |
| Type                 | Integer                    |
| Default Value        | 8                          |
| Minimum Value        | 0                          |

This validate\_password plugin system variable is deprecated; expect it to be removed in a future version of MySQL. Use the corresponding [validate\\_password.length](#page-136-0) system variable of the validate\_password component instead.

<span id="page-140-2"></span>• [validate\\_password\\_mixed\\_case\\_count](#page-140-2)

| Command-Line Format  | validate-password-mixed-case<br>count=# |
|----------------------|-----------------------------------------|
| System Variable      | validate_password_mixed_case_count      |
| Scope                | Global                                  |
| Dynamic              | Yes                                     |
| SET_VAR Hint Applies | No                                      |
| Type                 | Integer                                 |
| Default Value        | 1                                       |
| Minimum Value        | 0                                       |

This validate\_password plugin system variable is deprecated; expect it to be removed in a future version of MySQL. Use the corresponding [validate\\_password.mixed\\_case\\_count](#page-136-1) system variable of the validate\_password component instead.

<span id="page-141-1"></span>• [validate\\_password\\_number\\_count](#page-141-1)

| Command-Line Format  | validate-password-number-count=# |
|----------------------|----------------------------------|
| System Variable      | validate_password_number_count   |
| Scope                | Global                           |
| Dynamic              | Yes                              |
| SET_VAR Hint Applies | No                               |
| Type                 | Integer                          |
| Default Value        | 1                                |
| Minimum Value        | 0                                |

This validate\_password plugin system variable is deprecated; expect it to be removed in a future version of MySQL. Use the corresponding [validate\\_password.number\\_count](#page-137-1) system variable of the validate\_password component instead.

<span id="page-141-2"></span>• [validate\\_password\\_policy](#page-141-2)

| Command-Line Format  | validate-password-policy=value |
|----------------------|--------------------------------|
| System Variable      | validate_password_policy       |
| Scope                | Global                         |
| Dynamic              | Yes                            |
| SET_VAR Hint Applies | No                             |
| Type                 | Enumeration                    |
| Default Value        | 1                              |
| Valid Values         | 0                              |
|                      | 1                              |
|                      | 2                              |

This validate\_password plugin system variable is deprecated; expect it to be removed in a future version of MySQL. Use the corresponding [validate\\_password.policy](#page-137-0) system variable of the validate\_password component instead.

<span id="page-141-3"></span>• [validate\\_password\\_special\\_char\\_count](#page-141-3)

| Command-Line Format  | validate-password-special-char<br>count=# |
|----------------------|-------------------------------------------|
| System Variable      | validate_password_special_char_count      |
| Scope                | Global                                    |
| Dynamic              | Yes                                       |
| SET_VAR Hint Applies | No                                        |
| Type                 | Integer                                   |
| Default Value        | 1                                         |
| Minimum Value        | 0                                         |

This validate\_password plugin system variable is deprecated; expect it to be removed in a future version of MySQL. Use the corresponding [validate\\_password.special\\_char\\_count](#page-138-0) system variable of the validate\_password component instead.

## <span id="page-141-0"></span>**Password Validation Plugin Status Variables**

![](_page_142_Picture_1.jpeg)

## **Note**

In MySQL 8.0, the validate\_password plugin was reimplemented as the validate\_password component. The validate\_password plugin is deprecated; expect it to be removed in a future version of MySQL. Consequently, its status variables are also deprecated; expect it to be removed. Use the corresponding status variables of the validate\_password component; see [Password Validation Component Status Variables.](#page-138-1) MySQL installations that use the plugin should make the transition to using the component instead. See [Section 8.4.3.3, "Transitioning to the Password](#page-142-0) [Validation Component".](#page-142-0)

<span id="page-142-1"></span>• [validate\\_password\\_dictionary\\_file\\_last\\_parsed](#page-142-1)

This validate\_password plugin status variable is deprecated; expect it to be removed in a future version of MySQL. Use the corresponding [validate\\_password.dictionary\\_file\\_last\\_parsed](#page-138-3) status variable of the validate\_password component instead.

<span id="page-142-2"></span>• [validate\\_password\\_dictionary\\_file\\_words\\_count](#page-142-2)

This validate\_password plugin status variable is deprecated; expect it to be removed in a future version of MySQL. Use the corresponding [validate\\_password.dictionary\\_file\\_words\\_count](#page-138-4) status variable of the validate\_password component instead.

# <span id="page-142-0"></span>**8.4.3.3 Transitioning to the Password Validation Component**

![](_page_142_Picture_9.jpeg)

#### **Note**

In MySQL 8.0, the validate\_password plugin was reimplemented as the validate\_password component. The validate\_password plugin is deprecated; expect it to be removed in a future version of MySQL.

MySQL installations that currently use the validate\_password plugin should make the transition to using the validate\_password component instead. To do so, use the following procedure. The procedure installs the component before uninstalling the plugin, to avoid having a time window during which no password validation occurs. (The component and plugin can be installed simultaneously. In this case, the server attempts to use the component, falling back to the plugin if the component is unavailable.)

1. Install the validate\_password component:

```
INSTALL COMPONENT 'file://component_validate_password';
```

- 2. Test the validate\_password component to ensure that it works as expected. If you need to set any validate\_password.xxx system variables, you can do so at runtime using SET GLOBAL. (Any option file changes that must be made are performed in the next step.)
- 3. Adjust any references to the plugin system and status variables to refer to the corresponding component system and status variables. Suppose that previously you had configured the plugin at startup using an option file like this:

```
[mysqld]
validate-password=FORCE_PLUS_PERMANENT
validate_password_dictionary_file=/usr/share/dict/words
validate_password_length=10
validate_password_number_count=2
```

Those settings are appropriate for the plugin, but must be modified to apply to the component. To adjust the option file, omit the [--validate-password](#page-139-1) option (it applies only to the plugin, not

the component), and modify the system variable references from no-dot names appropriate for the plugin to dotted names appropriate for the component:

```
[mysqld]
validate_password.dictionary_file=/usr/share/dict/words
validate_password.length=10
validate_password.number_count=2
```

Similar adjustments are needed for applications that refer at runtime to validate\_password plugin system and status variables. Change the no-dot plugin variable names to the corresponding dotted component variable names.

4. Uninstall the validate\_password plugin:

```
UNINSTALL PLUGIN validate_password;
```

If the validate\_password plugin is loaded at server startup using a --plugin-load or - plugin-load-add option, omit that option from the server startup procedure. For example, if the option is listed in a server option file, remove it from the file.

5. Restart the server.

# <span id="page-143-0"></span>**8.4.4 The MySQL Keyring**

MySQL Server supports a keyring that enables internal server components and plugins to securely store sensitive information for later retrieval. The implementation comprises these elements:

• Keyring components and plugins that manage a backing store or communicate with a storage back end. Keyring use involves installing one from among the available components and plugins. Keyring components and plugins both manage keyring data but are configured differently and may have operational differences (see [Section 8.4.4.1, "Keyring Components Versus Keyring Plugins"\)](#page-145-0).

These keyring components are available:

- component\_keyring\_file: Stores keyring data in a file local to the server host. Available in MySQL Community Edition and MySQL Enterprise Edition distributions as of MySQL 8.0.24. See [Section 8.4.4.4, "Using the component\\_keyring\\_file File-Based Keyring Component"](#page-150-0).
- component\_keyring\_encrypted\_file: Stores keyring data in an encrypted, passwordprotected file local to the server host. Available in MySQL Enterprise Edition distributions as of MySQL 8.0.24. See [Section 8.4.4.5, "Using the component\\_keyring\\_encrypted\\_file Encrypted File-](#page-153-0)[Based Keyring Component".](#page-153-0)
- component\_keyring\_oci: Stores keyring data in the Oracle Cloud Infrastructure Vault. Available in MySQL Enterprise Edition distributions as of MySQL 8.0.31. See [Section 8.4.4.11,](#page-174-0) ["Using the Oracle Cloud Infrastructure Vault Keyring Component"](#page-174-0).

These keyring plugins are available:

- keyring\_file (deprecated as of MySQL 8.0.34): Stores keyring data in a file local to the server host. Available in MySQL Community Edition and MySQL Enterprise Edition distributions. See [Section 8.4.4.6, "Using the keyring\\_file File-Based Keyring Plugin"](#page-156-0).
- keyring\_encrypted\_file (deprecated as of MySQL 8.0.34): Stores keyring data in an encrypted, password-protected file local to the server host. Available in MySQL Enterprise Edition distributions. See [Section 8.4.4.7, "Using the keyring\\_encrypted\\_file Encrypted File-Based Keyring](#page-157-0) [Plugin"](#page-157-0).
- keyring\_okv: A KMIP 1.1 plugin for use with KMIP-compatible back end keyring storage products such as Oracle Key Vault and Gemalto SafeNet KeySecure Appliance. Available in MySQL Enterprise Edition distributions. See [Section 8.4.4.8, "Using the keyring\\_okv KMIP Plugin"](#page-158-0).

- keyring\_aws: Communicates with the Amazon Web Services Key Management Service for key generation and uses a local file for key storage. Available in MySQL Enterprise Edition distributions. See [Section 8.4.4.9, "Using the keyring\\_aws Amazon Web Services Keyring Plugin"](#page-164-0).
- keyring\_hashicorp: Communicates with HashiCorp Vault for back end storage. Available in MySQL Enterprise Edition distributions as of MySQL 8.0.18. See [Section 8.4.4.10, "Using the](#page-167-0) [HashiCorp Vault Keyring Plugin"](#page-167-0).
- keyring\_oci (deprecated as of MySQL 8.0.31): Communicates with Oracle Cloud Infrastructure Vault for back end storage. Available in MySQL Enterprise Edition distributions as of MySQL 8.0.22. See [Section 8.4.4.12, "Using the Oracle Cloud Infrastructure Vault Keyring Plugin"](#page-178-0).
- A keyring service interface for keyring key management. This service is accessible at two levels:
  - SQL interface: In SQL statements, call the functions described in [Section 8.4.4.15, "General-](#page-189-0)[Purpose Keyring Key-Management Functions"](#page-189-0).
  - C interface: In C-language code, call the keyring service functions described in Section 7.6.9.2, "The Keyring Service".
- Key metadata access:
  - The Performance Schema keyring\_keys table exposes metadata for keys in the keyring. Key metadata includes key IDs, key owners, and backend key IDs. The keyring\_keys table does not expose any sensitive keyring data such as key contents. Available as of MySQL 8.0.16. See Section 29.12.18.2, "The keyring\_keys table".
  - The Performance Schema keyring\_component\_status table provides status information about the keyring component in use, if one is installed. Available as of MySQL 8.0.24. See Section 29.12.18.1, "The keyring\_component\_status Table".
- A key migration capability. MySQL supports migration of keys between keystores, enabling DBAs to switch a MySQL installation from one keystore to another. See [Section 8.4.4.14, "Migrating Keys](#page-182-0) [Between Keyring Keystores"](#page-182-0).
- The implementation of keyring plugins is revised as of MySQL 8.0.24 to use the component infrastructure. This is facilitated using the built-in plugin named daemon\_keyring\_proxy\_plugin that acts as a bridge between the plugin and component service APIs. See Section 7.6.8, "The Keyring Proxy Bridge Plugin".

![](_page_144_Picture_12.jpeg)

#### **Warning**

For encryption key management, the component\_keyring\_file and component\_keyring\_encrypted\_file components, and the keyring\_file and keyring\_encrypted\_file plugins are not intended as a regulatory compliance solution. Security standards such as PCI, FIPS, and others require use of key management systems to secure, manage, and protect encryption keys in key vaults or hardware security modules (HSMs).

Within MySQL, keyring service consumers include:

- The InnoDB storage engine uses the keyring to store its key for tablespace encryption. See Section 17.13, "InnoDB Data-at-Rest Encryption".
- MySQL Enterprise Audit uses the keyring to store the audit log file encryption password. See Encrypting Audit Log Files.
- Binary log and relay log management supports keyring-based encryption of log files. With log file encryption activated, the keyring stores the keys used to encrypt passwords for the binary log files and relay log files. See Section 19.3.2, "Encrypting Binary Log Files and Relay Log Files".

• The master key to decrypt the file key that decrypts the persisted values of sensitive system variables is stored in the keyring. A keyring component must be enabled on the MySQL Server instance to support secure storage for persisted system variable values, rather than a keyring plugin, which do not support the function. See Persisting Sensitive System Variables.

For general keyring installation instructions, see [Section 8.4.4.2, "Keyring Component Installation",](#page-145-1) and [Section 8.4.4.3, "Keyring Plugin Installation".](#page-148-0) For installation and configuration information specific to a given keyring component or plugin, see the section describing it.

For information about using the keyring functions, see [Section 8.4.4.15, "General-Purpose Keyring](#page-189-0) [Key-Management Functions"](#page-189-0).

Keyring components, plugins, and functions access a keyring service that provides the interface to the keyring. For information about accessing this service and writing keyring plugins, see Section 7.6.9.2, "The Keyring Service", and [Writing Keyring Plugins](https://dev.mysql.com/doc/extending-mysql/8.0/en/writing-keyring-plugins.md).

# <span id="page-145-0"></span>**8.4.4.1 Keyring Components Versus Keyring Plugins**

The MySQL Keyring originally implemented keystore capabilities using server plugins, but began transitioning to use the component infrastructure in MySQL 8.0.24. This section briefly compares keyring components and plugins to provide an overview of their differences. It may assist you in making the transition from plugins to components, or, if you are just beginning to use the keyring, assist you in choosing whether to use a component versus using a plugin.

- Keyring plugin loading uses the --early-plugin-load option. Keyring component loading uses a manifest.
- Keyring plugin configuration is based on plugin-specific system variables. For keyring components, no system variables are used. Instead, each component has its own configuration file.
- Keyring components have fewer restrictions than keyring plugins with respect to key types and lengths. See [Section 8.4.4.13, "Supported Keyring Key Types and Lengths".](#page-181-0)

![](_page_145_Picture_10.jpeg)

#### **Note**

component\_keyring\_oci (like the keyring\_oci plugin) can only generate keys of type AES with a size of 16, 24, or 32 bytes.

• Keyring components support secure storage for persisted system variable values, whereas keyring plugins do not support the function.

A keyring component must be enabled on the MySQL server instance to support secure storage for persisted system variable values. The sensitive data that can be protected in this way includes items such as private keys and passwords that appear in the values of system variables. In the operating system file where persisted system variables are stored, the names and values of sensitive system variables are stored in an encrypted format, along with a generated file key to decrypt them. The generated file key is in turn encrypted using a master key that is stored in a keyring. See Persisting Sensitive System Variables.

# <span id="page-145-1"></span>**8.4.4.2 Keyring Component Installation**

Keyring service consumers require that a keyring component or plugin be installed:

- To use a keyring component, begin with the instructions here.
- To use a keyring plugin instead, begin with [Section 8.4.4.3, "Keyring Plugin Installation".](#page-148-0)
- If you intend to use keyring functions in conjunction with the chosen keyring component or plugin, install the functions after installing that component or plugin, using the instructions in [Section 8.4.4.15, "General-Purpose Keyring Key-Management Functions"](#page-189-0).

![](_page_146_Picture_1.jpeg)

## **Note**

Only one keyring component or plugin should be enabled at a time. Enabling multiple keyring components or plugins is unsupported and results may not be as anticipated.

MySQL provides these keyring component choices:

- component\_keyring\_file: Stores keyring data in a file local to the server host. Available in MySQL Community Edition and MySQL Enterprise Edition distributions.
- component\_keyring\_encrypted\_file: Stores keyring data in an encrypted, passwordprotected file local to the server host. Available in MySQL Enterprise Edition distributions.
- component\_keyring\_oci: Stores keyring data in the Oracle Cloud Infrastructure Vault. Available in MySQL Enterprise Edition distributions.

To be usable by the server, the component library file must be located in the MySQL plugin directory (the directory named by the plugin\_dir system variable). If necessary, configure the plugin directory location by setting the value of plugin\_dir at server startup.

A keyring component or plugin must be loaded early during the server startup sequence so that other components can access it as necessary during their own initialization. For example, the InnoDB storage engine uses the keyring for tablespace encryption, so a keyring component or plugin must be loaded and available prior to InnoDB initialization.

![](_page_146_Picture_10.jpeg)

#### **Note**

A keyring component must be enabled on the MySQL server instance if you need to support secure storage for persisted system variable values. The keyring plugin does not support the function. See Persisting Sensitive System Variables.

Unlike keyring plugins, keyring components are not loaded using the --early-plugin-load server option or configured using system variables. Instead, the server determines which keyring component to load during startup using a manifest, and the loaded component consults its own configuration file when it initializes. Therefore, to install a keyring component, you must:

- 1. Write a manifest that tells the server which keyring component to load.
- 2. Write a configuration file for that keyring component.

The first step in installing a keyring component is writing a manifest that indicates which component to load. During startup, the server reads either a global manifest file, or a global manifest file paired with a local manifest file:

- The server attempts to read its global manifest file from the directory where the server is installed.
- If the global manifest file indicates use of a local manifest file, the server attempts to read its local manifest file from the data directory.
- Although global and local manifest files are located in different directories, the file name is mysqld.my in both locations.
- It is not an error for a manifest file not to exist. In this case, the server attempts no component loading associated with the file.

Local manifest files permit setting up component loading for multiple instances of the server, such that loading instructions for each server instance are specific to a given data directory instance. This enables different MySQL instances to use different keyring components.

Server manifest files have these properties:

- A manifest file must be in valid JSON format.
- A manifest file permits these items:
  - "read\_local\_manifest": This item is permitted only in the global manifest file. If the item is not present, the server uses only the global manifest file. If the item is present, its value is true or false, indicating whether the server should read component-loading information from the local manifest file.

If the "read\_local\_manifest" item is present in the global manifest file along with other items, the server checks the "read\_local\_manifest" item value first:

- If the value is false, the server processes the other items in the global manifest file and ignores the local manifest file.
- If the value is true, the server ignores the other items in the global manifest file and attempts to read the local manifest file.
- "components": This item indicates which component to load. The item value is a string that specifies a valid component URN, such as "file://component\_keyring\_file". A component URN begins with file:// and indicates the base name of the library file located in the MySQL plugin directory that implements the component.
- Server access to a manifest file should be read only. For example, a mysqld.my server manifest file may be owned by root and be read/write to root, but should be read only to the account used to run the MySQL server. If the manifest file is found during startup to be read/write to that account, the server writes a warning to the error log suggesting that the file be made read only.
- The database administrator has the responsibility for creating any manifest files to be used, and for ensuring that their access mode and contents are correct. If an error occurs, server startup fails and the administrator must correct any issues indicated by diagnostics in the server error log.

Given the preceding manifest file properties, to configure the server to load component\_keyring\_file, create a global manifest file named mysqld.my in the mysqld installation directory, and optionally create a local manifest file, also named mysqld.my, in the data directory. The following instructions describe how to load component\_keyring\_file. To load a different keyring component, substitute its name for component\_keyring\_file.

• To use a global manifest file only, the file contents look like this:

```
{
 "components": "file://component_keyring_file"
}
```

Create this file in the directory where mysqld is installed.

• Alternatively, to use a global and local manifest file pair, the global file looks like this:

```
{
 "read_local_manifest": true
}
```

Create this file in the directory where mysqld is installed.

The local file looks like this:

```
{
 "components": "file://component_keyring_file"
}
```

Create this file in the data directory.

With the manifest in place, proceed to configuring the keyring component. To do this, check the notes for your chosen keyring component for configuration instructions specific to that component:

- component\_keyring\_file: [Section 8.4.4.4, "Using the component\\_keyring\\_file File-Based](#page-150-0) [Keyring Component".](#page-150-0)
- component\_keyring\_encrypted\_file: [Section 8.4.4.5, "Using the](#page-153-0) [component\\_keyring\\_encrypted\\_file Encrypted File-Based Keyring Component".](#page-153-0)
- component\_keyring\_oci: [Section 8.4.4.11, "Using the Oracle Cloud Infrastructure Vault Keyring](#page-174-0) [Component"](#page-174-0).

After performing any component-specific configuration, start the server. Verify component installation by examining the Performance Schema keyring\_component\_status table:

```
mysql> SELECT * FROM performance_schema.keyring_component_status;
+---------------------+-------------------------------------------------+
| STATUS_KEY | STATUS_VALUE |
+---------------------+-------------------------------------------------+
| Component_name | component_keyring_file |
| Author | Oracle Corporation |
| License | GPL |
| Implementation_name | component_keyring_file |
| Version | 1.0 |
| Component_status | Active |
| Data_file | /usr/local/mysql/keyring/component_keyring_file |
| Read_only | No |
+---------------------+-------------------------------------------------+
```

A Component\_status value of Active indicates that the component initialized successfully.

If the component cannot be loaded, server startup fails. Check the server error log for diagnostic messages. If the component loads but fails to initialize due to configuration problems, the server starts but the Component\_status value is Disabled. Check the server error log, correct the configuration issues, and use the ALTER INSTANCE RELOAD KEYRING statement to reload the configuration.

Keyring components should be loaded only by using a manifest file, not by using the INSTALL COMPONENT statement. Keyring components loaded using that statement may be available too late in the server startup sequence for certain components that use the keyring, such as InnoDB, because they are registered in the mysql.component system table and loaded automatically for subsequent server restarts. But mysql.component is an InnoDB table, so any components named in it can be loaded during startup only after InnoDB initialization.

If no keyring component or plugin is available when a component tries to access the keyring service, the service cannot be used by that component. As a result, the component may fail to initialize or may initialize with limited functionality. For example, if InnoDB finds that there are encrypted tablespaces when it initializes, it attempts to access the keyring. If the keyring is unavailable, InnoDB can access only unencrypted tablespaces.

# <span id="page-148-0"></span>**8.4.4.3 Keyring Plugin Installation**

Keyring service consumers require that a keyring component or plugin be installed:

- To use a keyring plugin, begin with the instructions here. (Also, for general information about installing plugins, see Section 7.6.1, "Installing and Uninstalling Plugins".)
- To use a keyring component instead, begin with [Section 8.4.4.2, "Keyring Component Installation"](#page-145-1).
- If you intend to use keyring functions in conjunction with the chosen keyring component or plugin, install the functions after installing that component or plugin, using the instructions in [Section 8.4.4.15, "General-Purpose Keyring Key-Management Functions"](#page-189-0).

![](_page_148_Picture_15.jpeg)

#### **Note**

Only one keyring component or plugin should be enabled at a time. Enabling multiple keyring components or plugins is unsupported and results may not be as anticipated.

A keyring component must be enabled on the MySQL Server instance if you need to support secure storage for persisted system variable values, rather than a keyring plugin, which do not support the function. See Persisting Sensitive System Variables.

MySQL provides these keyring plugin choices:

- keyring\_file (deprecated as of MySQL 8.0.34): Stores keyring data in a file local to the server host. Available in MySQL Community Edition and MySQL Enterprise Edition distributions. For instructions about installing the component that replaces this plugin, see [Section 8.4.4.2, "Keyring](#page-145-1) [Component Installation".](#page-145-1)
- keyring\_encrypted\_file (deprecated as of MySQL 8.0.34): Stores keyring data in an encrypted, password-protected file local to the server host. Available in MySQL Enterprise Edition distributions. For instructions about installing the component that replaces this plugin, see [Section 8.4.4.2, "Keyring Component Installation".](#page-145-1)
- keyring\_okv: A KMIP 1.1 plugin for use with KMIP-compatible back end keyring storage products such as Oracle Key Vault and Gemalto SafeNet KeySecure Appliance. Available in MySQL Enterprise Edition distributions.
- keyring\_aws: Communicates with the Amazon Web Services Key Management Service as a back end for key generation and uses a local file for key storage. Available in MySQL Enterprise Edition distributions.
- keyring\_hashicorp: Communicates with HashiCorp Vault for back end storage. Available in MySQL Enterprise Edition distributions.
- keyring\_oci(deprecated as of MySQL 8.0.31): Communicates with Oracle Cloud Infrastructure Vault for back end storage. See [Section 8.4.4.12, "Using the Oracle Cloud Infrastructure Vault](#page-178-0) [Keyring Plugin".](#page-178-0)

To be usable by the server, the plugin library file must be located in the MySQL plugin directory (the directory named by the plugin\_dir system variable). If necessary, configure the plugin directory location by setting the value of plugin\_dir at server startup.

A keyring component or plugin must be loaded early during the server startup sequence so that other components can access it as necessary during their own initialization. For example, the InnoDB storage engine uses the keyring for tablespace encryption, so a keyring component or plugin must be loaded and available prior to InnoDB initialization.

Installation for each keyring plugin is similar. The following instructions describe how to install keyring\_file. To use a different keyring plugin, substitute its name for keyring\_file.

The keyring\_file plugin library file base name is keyring\_file. The file name suffix differs per platform (for example, .so for Unix and Unix-like systems, .dll for Windows).

To load the plugin, use the --early-plugin-load option to name the plugin library file that contains it. For example, on platforms where the plugin library file suffix is .so, use these lines in the server my.cnf file, adjusting the .so suffix for your platform as necessary:

```
[mysqld]
early-plugin-load=keyring_file.so
```

Before starting the server, check the notes for your chosen keyring plugin for configuration instructions specific to that plugin:

- keyring\_file: [Section 8.4.4.6, "Using the keyring\\_file File-Based Keyring Plugin".](#page-156-0)
- keyring\_encrypted\_file: [Section 8.4.4.7, "Using the keyring\\_encrypted\\_file Encrypted File-](#page-157-0)[Based Keyring Plugin".](#page-157-0)

- keyring\_okv: [Section 8.4.4.8, "Using the keyring\\_okv KMIP Plugin".](#page-158-0)
- keyring\_aws: [Section 8.4.4.9, "Using the keyring\\_aws Amazon Web Services Keyring Plugin"](#page-164-0)
- keyring\_hashicorp: [Section 8.4.4.10, "Using the HashiCorp Vault Keyring Plugin"](#page-167-0)
- keyring\_oci: [Section 8.4.4.12, "Using the Oracle Cloud Infrastructure Vault Keyring Plugin"](#page-178-0)

After performing any plugin-specific configuration, start the server. Verify plugin installation by examining the Information Schema PLUGINS table or use the SHOW PLUGINS statement (see Section 7.6.2, "Obtaining Server Plugin Information"). For example:

```
mysql> SELECT PLUGIN_NAME, PLUGIN_STATUS
 FROM INFORMATION_SCHEMA.PLUGINS
 WHERE PLUGIN_NAME LIKE 'keyring%';
+--------------+---------------+
| PLUGIN_NAME | PLUGIN_STATUS |
+--------------+---------------+
| keyring_file | ACTIVE |
+--------------+---------------+
```

If the plugin fails to initialize, check the server error log for diagnostic messages.

Plugins can be loaded by methods other than --early-plugin-load, such as the --plugin-load or --plugin-load-add option or the INSTALL PLUGIN statement. However, keyring plugins loaded using those methods may be available too late in the server startup sequence for certain components that use the keyring, such as InnoDB:

- Plugin loading using --plugin-load or --plugin-load-add occurs after InnoDB initialization.
- Plugins installed using INSTALL PLUGIN are registered in the mysql.plugin system table and loaded automatically for subsequent server restarts. However, because mysql.plugin is an InnoDB table, any plugins named in it can be loaded during startup only after InnoDB initialization.

If no keyring component or plugin is available when a component tries to access the keyring service, the service cannot be used by that component. As a result, the component may fail to initialize or may initialize with limited functionality. For example, if InnoDB finds that there are encrypted tablespaces when it initializes, it attempts to access the keyring. If the keyring is unavailable, InnoDB can access only unencrypted tablespaces. To ensure that InnoDB can access encrypted tablespaces as well, use --early-plugin-load to load the keyring plugin.

# <span id="page-150-0"></span>**8.4.4.4 Using the component\_keyring\_file File-Based Keyring Component**

The component\_keyring\_file keyring component stores keyring data in a file local to the server host.

![](_page_150_Picture_14.jpeg)

#### **Warning**

For encryption key management, the component\_keyring\_file and component\_keyring\_encrypted\_file components are not intended as a regulatory compliance solution. Security standards such as PCI, FIPS, and others require use of key management systems to secure, manage, and protect encryption keys in key vaults or hardware security modules (HSMs).

To use component\_keyring\_file for keystore management in the most common scenario, create two files: a manifest file that tells the server to load component\_keyring\_file, and a configuration file that specifies where to store the keys. Both files should be readable only by the appropriate user that runs the server, typically mysql.

The manifest file must be named mysqld.my and added to the same directory where mysqld is installed. The file looks like this:

```
{
 "components": "file://component_keyring_file"
```

}

The configuration file must be named component\_keyring\_file.cnf and added to the plugin directory. It contains the path to the file where the server stores keys:

```
{
 "path": "/usr/local/mysql/keyring/component_keyring_file.keys",
 "read_only": false
}
```

After adding the two files, restart mysqld. Verify component installation by examining the Performance Schema keyring\_component\_status table:

```
mysql> SELECT * FROM performance_schema.keyring_component_status;
```

A Component\_status value of Active indicates that the component initialized successfully.

If the server startup fails or the Component\_status value is Disabled, check the server error log.

For more details and to review other scenarios, see [Section 8.4.4.2, "Keyring Component Installation"](#page-145-1) and [Configuration Notes.](#page-151-0)

- [Configuration Notes](#page-151-0)
- [Keyring Component Usage](#page-153-1)

# <span id="page-151-0"></span>**Configuration Notes**

When it initializes, component\_keyring\_file reads either a global configuration file, or a global configuration file paired with a local configuration file:

- The component attempts to read its global configuration file from the directory where the component library file is installed (that is, the server plugin directory).
- If the global configuration file indicates use of a local configuration file, the component attempts to read its local configuration file from the data directory.
- Although global and local configuration files are located in different directories, the file name is component\_keyring\_file.cnf in both locations.
- It is an error for no configuration file to exist. component\_keyring\_file cannot initialize without a valid configuration.

Local configuration files permit setting up multiple server instances to use component\_keyring\_file, such that component configuration for each server instance is specific to a given data directory instance. This enables the same keyring component to be used with a distinct data file for each instance.

component\_keyring\_file configuration files have these properties:

- A configuration file must be in valid JSON format.
- A configuration file must have the appropriate file permission that allows MySQL to read it. Since the file contains sensitive information, it should be set to world readable.
- A configuration file permits these configuration items:
  - "read\_local\_config": This item is permitted only in the global configuration file. If the item is not present, the component uses only the global configuration file. If the item is present, its value is true or false, indicating whether the component should read configuration information from the local configuration file.

If the "read\_local\_config" item is present in the global configuration file along with other items, the component checks the "read\_local\_config" item value first:

- If the value is false, the component processes the other items in the global configuration file and ignores the local configuration file.
- If the value is true, the component ignores the other items in the global configuration file and attempts to read the local configuration file.
- "path": The item value is a string that names the file to use for storing keyring data. The file should be named using an absolute path, not a relative path. This item is mandatory in the configuration. If not specified, component\_keyring\_file initialization fails.
- "read\_only": The item value indicates whether the keyring data file is read only. The item value is true (read only) or false (read/write). This item is mandatory in the configuration. If not specified, component\_keyring\_file initialization fails.
- The database administrator has the responsibility for creating any configuration files to be used, and for ensuring that their contents are correct. If an error occurs, server startup fails and the administrator must correct any issues indicated by diagnostics in the server error log.

Given the preceding configuration file properties, to configure component\_keyring\_file, create a global configuration file named component\_keyring\_file.cnf in the directory where the component\_keyring\_file library file is installed, and optionally create a local configuration file, also named component\_keyring\_file.cnf, in the data directory. The following instructions assume that a keyring data file named /usr/local/mysql/keyring/component\_keyring\_file.keys is to be used in read/write fashion.

![](_page_152_Picture_7.jpeg)

#### **Note**

For Windows systems, the path to the /usr/local/mysql/keyring/ component\_keyring\_file.keys file can be in C:\ProgramData. It should not be in C:\Program Files.

• To use a global configuration file only, the file contents look like this:

```
{
 "path": "/usr/local/mysql/keyring/component_keyring_file.keys",
 "read_only": false
}
```

Create this file in the directory where the component\_keyring\_file library file is installed.

This path must not point to or include the MySQL data directory. The path must be readable and writable by the system MySQL user (Windows: NETWORK SERVICES; Linux: mysql user; MacOS: \_mysql user). It should not be accessible to other users.

• Alternatively, to use a global and local configuration file pair, the global file looks like this:

```
{
 "read_local_config": true
}
```

Create this file in the directory where the component\_keyring\_file library file is installed.

The local file looks like this:

```
{
 "path": "/usr/local/mysql/keyring/component_keyring_file.keys",
 "read_only": false
}
```

This path must not point to or include the MySQL data directory. The path must be readable and writable by the system MySQL user (Windows: NETWORK SERVICES; Linux: mysql user; MacOS: \_mysql user). It should not be accessible to other users.

## <span id="page-153-1"></span>**Keyring Component Usage**

Keyring operations are transactional: component\_keyring\_file uses a backup file during write operations to ensure that it can roll back to the original file if an operation fails. The backup file has the same name as the data file with a suffix of .backup.

component\_keyring\_file supports the functions that comprise the standard MySQL Keyring service interface. Keyring operations performed by those functions are accessible in SQL statements as described in [Section 8.4.4.15, "General-Purpose Keyring Key-Management Functions"](#page-189-0).

#### Example:

```
SELECT keyring_key_generate('MyKey', 'AES', 32);
SELECT keyring_key_remove('MyKey');
```

For information about the characteristics of key values permitted by component\_keyring\_file, see [Section 8.4.4.13, "Supported Keyring Key Types and Lengths"](#page-181-0).

# <span id="page-153-0"></span>**8.4.4.5 Using the component\_keyring\_encrypted\_file Encrypted File-Based Keyring Component**

![](_page_153_Picture_8.jpeg)

#### **Note**

component\_keyring\_encrypted\_file is an extension included in MySQL Enterprise Edition, a commercial product. To learn more about commercial products, see<https://www.mysql.com/products/>.

The component\_keyring\_encrypted\_file keyring component stores keyring data in an encrypted, password-protected file local to the server host.

![](_page_153_Picture_12.jpeg)

#### **Warning**

For encryption key management, the component\_keyring\_file and component\_keyring\_encrypted\_file components are not intended as a regulatory compliance solution. Security standards such as PCI, FIPS, and others require use of key management systems to secure, manage, and protect encryption keys in key vaults or hardware security modules (HSMs).

To use component\_keyring\_encrypted\_file for keystore management in the most common scenario, create two files: a manifest file that tells the server to load component\_keyring\_encrypted\_file, and a configuration file that specifies where to store the keys. Both files should be readable only by the appropriate user that runs the server, typically mysql.

The manifest file must be named mysqld.my and added to the same directory where mysqld is installed. The file looks like this:

```
{
 "components": "file://component_keyring_encrypted_file"
}
```

The configuration file must be named component\_keyring\_encrypted\_file.cnf and added to the plugin directory. It contains the path to the file where the server stores keys:

```
{
 "path": "/usr/local/mysql/keyring/component_keyring_encrypted_file.keys",
 "password": "password",
 "read_only": false
}
```

After adding the two files, restart mysqld. Verify component installation by examining the Performance Schema keyring\_component\_status table:

```
mysql> SELECT * FROM performance_schema.keyring_component_status;
```

A Component\_status value of Active indicates that the component initialized successfully.

If the server startup fails or the Component\_status value is Disabled, check the server error log.

For more details and to review other scenarios, see [Section 8.4.4.2, "Keyring Component Installation"](#page-145-1) and [Configuration Notes.](#page-154-0)

- [Configuration Notes](#page-154-0)
- [Encrypted Keyring Component Usage](#page-156-1)

## <span id="page-154-0"></span>**Configuration Notes**

When it initializes, component\_keyring\_encrypted\_file reads either a global configuration file, or a global configuration file paired with a local configuration file:

- The component attempts to read its global configuration file from the directory where the component library file is installed (that is, the server plugin directory).
- If the global configuration file indicates use of a local configuration file, the component attempts to read its local configuration file from the data directory.
- Although global and local configuration files are located in different directories, the file name is component\_keyring\_encrypted\_file.cnf in both locations.
- If component\_keyring\_encrypted\_file cannot find the configuration file, an error results, and the component cannot initialize.

Local configuration files permit setting up multiple server instances to use component\_keyring\_encrypted\_file, such that component configuration for each server instance is specific to a given data directory instance. This enables the same keyring component to be used with a distinct data file for each instance.

component\_keyring\_encrypted\_file configuration files have these properties:

- A configuration file must be in valid JSON format.
- A configuration file must have the appropriate file permission that allows MySQL to read it. Since the file contains sensitive information, it should be set to world readable.
- A configuration file permits these configuration items:
  - "read\_local\_config": This item is permitted only in the global configuration file. If the item is not present, the component uses only the global configuration file. If the item is present, its value is true or false, indicating whether the component should read configuration information from the local configuration file.

If the "read\_local\_config" item is present in the global configuration file along with other items, the component checks the "read\_local\_config" item value first:

- If the value is false, the component processes the other items in the global configuration file and ignores the local configuration file.
- If the value is true, the component ignores the other items in the global configuration file and attempts to read the local configuration file.
- "path": The item value is a string that names the file to use for storing keyring data. The file should be named using an absolute path, not a relative path. This item is mandatory in the configuration. If not specified, component\_keyring\_encrypted\_file initialization fails.
- "password": The item value is a string that specifies the password for accessing the data file. This item is mandatory in the configuration. If not specified, component\_keyring\_encrypted\_file initialization fails.

- "read\_only": The item value indicates whether the keyring data file is read only. The item value is true (read only) or false (read/write). This item is mandatory in the configuration. If not specified, component\_keyring\_encrypted\_file initialization fails.
- The database administrator has the responsibility for creating any configuration files to be used, and for ensuring that their contents are correct. If an error occurs, server startup fails and the administrator must correct any issues indicated by diagnostics in the server error log.
- Any configuration file that stores a password should have a restrictive mode and be accessible only to the account used to run the MySQL server.

Given the preceding configuration file properties, to configure component\_keyring\_encrypted\_file, create a global configuration file named component\_keyring\_encrypted\_file.cnf in the directory where the component\_keyring\_encrypted\_file library file is installed, and optionally create a local configuration file, also named component\_keyring\_encrypted\_file.cnf, in the data directory. The following instructions assume that a keyring data file named /usr/local/mysql/keyring/ component\_keyring\_encrypted\_file.keys is to be used in read/write fashion. You must also choose a password.

![](_page_155_Picture_5.jpeg)

#### **Note**

For Windows systems, the path to the /usr/local/mysql/keyring/ component\_keyring\_encrypted\_file.keys file can be in C: \ProgramData. It should not be in C:\Program Files.

• To use a global configuration file only, the file contents look like this:

```
{
 "path": "/usr/local/mysql/keyring/component_keyring_encrypted_file.keys",
 "password": "password",
 "read_only": false
}
```

Create this file in the directory where the component\_keyring\_encrypted\_file library file is installed.

This path must not point to or include the MySQL data directory. The path must be readable and writable by the system MySQL user (Windows: NETWORK SERVICES; Linux: mysql user; MacOS: \_mysql user). It should not be accessible to other users.

• Alternatively, to use a global and local configuration file pair, the global file looks like this:

```
{
 "read_local_config": true
}
```

Create this file in the directory where the component\_keyring\_encrypted\_file library file is installed.

The local file looks like this:

```
{
 "path": "/usr/local/mysql/keyring/component_keyring_encrypted_file.keys",
 "password": "password",
 "read_only": false
}
```

This path must not point to or include the MySQL data directory. The path must be readable and writable by the system MySQL user (Windows: NETWORK SERVICES; Linux: mysql user; MacOS: \_mysql user). It should not be accessible to other users.

# <span id="page-156-1"></span>**Encrypted Keyring Component Usage**

Keyring operations are transactional: component\_keyring\_encrypted\_file uses a backup file during write operations to ensure that it can roll back to the original file if an operation fails. The backup file has the same name as the data file with a suffix of .backup.

component\_keyring\_encrypted\_file supports the functions that comprise the standard MySQL Keyring service interface. Keyring operations performed by those functions are accessible in SQL statements as described in [Section 8.4.4.15, "General-Purpose Keyring Key-Management Functions".](#page-189-0)

#### Example:

```
SELECT keyring_key_generate('MyKey', 'AES', 32);
SELECT keyring_key_remove('MyKey');
```

For information about the characteristics of key values permitted by component\_keyring\_encrypted\_file, see [Section 8.4.4.13, "Supported Keyring Key Types and](#page-181-0) [Lengths".](#page-181-0)

# <span id="page-156-0"></span>**8.4.4.6 Using the keyring\_file File-Based Keyring Plugin**

The keyring\_file keyring plugin stores keyring data in a file local to the server host.

As of MySQL 8.0.34, this plugin is deprecated and subject to removal in a future release of MySQL. Instead, consider using the component\_keyring\_file component for storing keyring data (see [Section 8.4.4.4, "Using the component\\_keyring\\_file File-Based Keyring Component"](#page-150-0)).

![](_page_156_Picture_10.jpeg)

#### **Warning**

For encryption key management, the keyring\_file plugin is not intended as a regulatory compliance solution. Security standards such as PCI, FIPS, and others require use of key management systems to secure, manage, and protect encryption keys in key vaults or hardware security modules (HSMs).

To install keyring\_file, use the general instructions found in [Section 8.4.4.3, "Keyring Plugin](#page-148-0) [Installation"](#page-148-0), together with the configuration information specific to keyring\_file found here.

To be usable during the server startup process, keyring\_file must be loaded using the --earlyplugin-load option. The keyring\_file\_data system variable optionally configures the location of the file used by the keyring\_file plugin for data storage. The default value is platform specific. To configure the file location explicitly, set the variable value at startup. For example, use these lines in the server my.cnf file, adjusting the .so suffix and file location for your platform as necessary:

```
[mysqld]
early-plugin-load=keyring_file.so
keyring_file_data=/usr/local/mysql/mysql-keyring/keyring
```

If keyring\_file\_data is set to a new location, the keyring plugin creates a new, empty file containing no keys; this means that any existing encrypted tables can no longer be accessed.

Keyring operations are transactional: The keyring\_file plugin uses a backup file during write operations to ensure that it can roll back to the original file if an operation fails. The backup file has the same name as the value of the keyring\_file\_data system variable with a suffix of .backup.

For additional information about keyring\_file\_data, see Section 8.4.4.19, "Keyring System Variables".

To ensure that keys are flushed only when the correct keyring storage file exists, keyring\_file stores a SHA-256 checksum of the keyring in the file. Before updating the file, the plugin verifies that it contains the expected checksum.

The keyring\_file plugin supports the functions that comprise the standard MySQL Keyring service interface. Keyring operations performed by those functions are accessible at two levels:

- SQL interface: In SQL statements, call the functions described in [Section 8.4.4.15, "General-Purpose](#page-189-0) [Keyring Key-Management Functions"](#page-189-0).
- C interface: In C-language code, call the keyring service functions described in Section 7.6.9.2, "The Keyring Service".

Example (using the SQL interface):

```
SELECT keyring_key_generate('MyKey', 'AES', 32);
SELECT keyring_key_remove('MyKey');
```

For information about the characteristics of key values permitted by keyring\_file, see [Section 8.4.4.13, "Supported Keyring Key Types and Lengths"](#page-181-0).

# <span id="page-157-0"></span>**8.4.4.7 Using the keyring\_encrypted\_file Encrypted File-Based Keyring Plugin**

![](_page_157_Picture_7.jpeg)

#### **Note**

The keyring\_encrypted\_file plugin is an extension included in MySQL Enterprise Edition, a commercial product. To learn more about commercial products, see<https://www.mysql.com/products/>.

The keyring\_encrypted\_file keyring plugin stores keyring data in an encrypted, passwordprotected file local to the server host.

As of MySQL 8.0.34, this plugin is deprecated and subject to removal in a future release of MySQL. Instead, consider using the component\_encrypted\_keyring\_file component for storing keyring data (see [Section 8.4.4.5, "Using the component\\_keyring\\_encrypted\\_file Encrypted File-Based Keyring](#page-153-0) [Component"](#page-153-0)).

![](_page_157_Picture_12.jpeg)

#### **Warning**

For encryption key management, the keyring\_encrypted\_file plugin is not intended as a regulatory compliance solution. Security standards such as PCI, FIPS, and others require use of key management systems to secure, manage, and protect encryption keys in key vaults or hardware security modules (HSMs).

To install keyring\_encrypted\_file, use the general instructions found in [Section 8.4.4.3, "Keyring](#page-148-0) [Plugin Installation",](#page-148-0) together with the configuration information specific to keyring\_encrypted\_file found here.

To be usable during the server startup process, keyring\_encrypted\_file must be loaded using the --early-plugin-load option. To specify the password for encrypting the keyring data file, set the keyring\_encrypted\_file\_password system variable. (The password is mandatory; if not specified at server startup, keyring\_encrypted\_file initialization fails.) The keyring\_encrypted\_file\_data system variable optionally configures the location of the file used by the keyring\_encrypted\_file plugin for data storage. The default value is platform specific. To configure the file location explicitly, set the variable value at startup. For example, use these lines in the server my.cnf file, adjusting the .so suffix and file location for your platform as necessary and substituting your chosen password:

```
[mysqld]
early-plugin-load=keyring_encrypted_file.so
keyring_encrypted_file_data=/usr/local/mysql/mysql-keyring/keyring-encrypted
keyring_encrypted_file_password=password
```

Because the my.cnf file stores a password when written as shown, it should have a restrictive mode and be accessible only to the account used to run the MySQL server.

Keyring operations are transactional: The keyring\_encrypted\_file plugin uses a backup file during write operations to ensure that it can roll back to the original file if an operation fails. The backup file has the same name as the value of the keyring\_encrypted\_file\_data system variable with a suffix of .backup.

For additional information about the system variables used to configure the keyring\_encrypted\_file plugin, see Section 8.4.4.19, "Keyring System Variables".

To ensure that keys are flushed only when the correct keyring storage file exists, keyring\_encrypted\_file stores a SHA-256 checksum of the keyring in the file. Before updating the file, the plugin verifies that it contains the expected checksum. In addition, keyring\_encrypted\_file encrypts file contents using AES before writing the file, and decrypts file contents after reading the file.

The keyring\_encrypted\_file plugin supports the functions that comprise the standard MySQL Keyring service interface. Keyring operations performed by those functions are accessible at two levels:

- SQL interface: In SQL statements, call the functions described in [Section 8.4.4.15, "General-Purpose](#page-189-0) [Keyring Key-Management Functions"](#page-189-0).
- C interface: In C-language code, call the keyring service functions described in Section 7.6.9.2, "The Keyring Service".

Example (using the SQL interface):

```
SELECT keyring_key_generate('MyKey', 'AES', 32);
SELECT keyring_key_remove('MyKey');
```

For information about the characteristics of key values permitted by keyring\_encrypted\_file, see [Section 8.4.4.13, "Supported Keyring Key Types and Lengths"](#page-181-0).

# <span id="page-158-0"></span>**8.4.4.8 Using the keyring\_okv KMIP Plugin**

![](_page_158_Picture_10.jpeg)

#### **Note**

The keyring\_okv plugin is an extension included in MySQL Enterprise Edition, a commercial product. To learn more about commercial products, see <https://www.mysql.com/products/>.

The Key Management Interoperability Protocol (KMIP) enables communication of cryptographic keys between a key management server and its clients. The keyring\_okv keyring plugin uses the KMIP 1.1 protocol to communicate securely as a client of a KMIP back end. Keyring material is generated exclusively by the back end, not by keyring\_okv. The plugin works with these KMIP-compatible products:

- Oracle Key Vault
- Gemalto SafeNet KeySecure Appliance
- Townsend Alliance Key Manager
- Entrust KeyControl

Each MySQL Server instance must be registered separately as a client for KMIP. If two or more MySQL Server instances use the same set of credentials, they can interfere with each other's functioning.

The keyring\_okv plugin supports the functions that comprise the standard MySQL Keyring service interface. Keyring operations performed by those functions are accessible at two levels:

- SQL interface: In SQL statements, call the functions described in [Section 8.4.4.15, "General-Purpose](#page-189-0) [Keyring Key-Management Functions"](#page-189-0).
- C interface: In C-language code, call the keyring service functions described in Section 7.6.9.2, "The Keyring Service".

Example (using the SQL interface):

```
SELECT keyring_key_generate('MyKey', 'AES', 32);
SELECT keyring_key_remove('MyKey');
```

For information about the characteristics of key values permitted by keyring\_okv, [Section 8.4.4.13,](#page-181-0) ["Supported Keyring Key Types and Lengths"](#page-181-0).

To install keyring\_okv, use the general instructions found in [Section 8.4.4.3, "Keyring Plugin](#page-148-0) [Installation"](#page-148-0), together with the configuration information specific to keyring\_okv found here.

- [General keyring\\_okv Configuration](#page-159-0)
- [Configuring keyring\\_okv for Oracle Key Vault](#page-160-0)
- [Configuring keyring\\_okv for Gemalto SafeNet KeySecure Appliance](#page-162-0)
- [Configuring keyring\\_okv for Townsend Alliance Key Manager](#page-163-0)
- [Configuring keyring\\_okv for Entrust KeyControl](#page-163-1)
- [Password-Protecting the keyring\\_okv Key File](#page-163-2)

# <span id="page-159-0"></span>**General keyring\_okv Configuration**

Regardless of which KMIP back end the keyring\_okv plugin uses for keyring storage, the keyring\_okv\_conf\_dir system variable configures the location of the directory used by keyring\_okv for its support files. The default value is empty, so you must set the variable to name a properly configured directory before the plugin can communicate with the KMIP back end. Unless you do so, keyring\_okv writes a message to the error log during server startup that it cannot communicate:

```
[Warning] Plugin keyring_okv reported: 'For keyring_okv to be
initialized, please point the keyring_okv_conf_dir variable to a directory
containing Oracle Key Vault configuration file and ssl materials'
```

The keyring\_okv\_conf\_dir variable must name a directory that contains the following items:

- okvclient.ora: A file that contains details of the KMIP back end with which keyring\_okv communicates.
- ssl: A directory that contains the certificate and key files required to establish a secure connection with the KMIP back end: CA.pem, cert.pem, and key.pem. If the key file is password-protected, the ssl directory can contain a single-line text file named password.txt containing the password needed to decrypt the key file.

Both the okvclient.ora file and ssl directory with the certificate and key files are required for keyring\_okv to work properly. The procedure used to populate the configuration directory with these files depends on the KMIP back end used with keyring\_okv, as described elsewhere.

The configuration directory used by keyring\_okv as the location for its support files should have a restrictive mode and be accessible only to the account used to run the MySQL server. For example, on Unix and Unix-like systems, to use the /usr/local/mysql/mysql-keyring-okv directory, the following commands (executed as root) create the directory and set its mode and ownership:

```
cd /usr/local/mysql
mkdir mysql-keyring-okv
chmod 750 mysql-keyring-okv
chown mysql mysql-keyring-okv
chgrp mysql mysql-keyring-okv
```

To be usable during the server startup process, keyring\_okv must be loaded using the --earlyplugin-load option. Also, set the keyring\_okv\_conf\_dir system variable to tell keyring\_okv where to find its configuration directory. For example, use these lines in the server my.cnf file, adjusting the .so suffix and directory location for your platform as necessary:

```
[mysqld]
early-plugin-load=keyring_okv.so
keyring_okv_conf_dir=/usr/local/mysql/mysql-keyring-okv
```

For additional information about keyring\_okv\_conf\_dir, see Section 8.4.4.19, "Keyring System Variables".

## <span id="page-160-0"></span>**Configuring keyring\_okv for Oracle Key Vault**

The discussion here assumes that you are familiar with Oracle Key Vault. Some pertinent information sources:

- [Oracle Key Vault site](http://www.oracle.com/technetwork/database/options/key-management/overview/index.md)
- [Oracle Key Vault documentation](http://www.oracle.com/technetwork/database/options/key-management/documentation/index.md)

In Oracle Key Vault terminology, clients that use Oracle Key Vault to store and retrieve security objects are called endpoints. To communicate with Oracle Key Vault, it is necessary to register as an endpoint and enroll by downloading and installing endpoint support files. Note that you must register a separate endpoint for each MySQL Server instance. If two or more MySQL Server instances use the same endpoint, they can interfere with each other's functioning.

The following procedure briefly summarizes the process of setting up keyring\_okv for use with Oracle Key Vault:

- 1. Create the configuration directory for the keyring\_okv plugin to use.
- 2. Register an endpoint with Oracle Key Vault to obtain an enrollment token.
- 3. Use the enrollment token to obtain the okvclient.jar client software download.
- 4. Install the client software to populate the keyring\_okv configuration directory that contains the Oracle Key Vault support files.

To get more information about these steps, see [Enrolling and Upgrading Endpoints for Oracle Key](https://docs.oracle.com/en/database/oracle/key-vault/21.11/okvag/okv_endpoints.md#GUID-5C1A6874-C7A9-41C6-859D-9FFD9010E13D) [Vault.](https://docs.oracle.com/en/database/oracle/key-vault/21.11/okvag/okv_endpoints.md#GUID-5C1A6874-C7A9-41C6-859D-9FFD9010E13D) The information references Oracle Database, but you can follow the same steps for MySQL.

Use the following procedure to configure keyring\_okv and Oracle Key Vault to work together. This description only summarizes how to interact with Oracle Key Vault. For details, visit the [Oracle Key](http://www.oracle.com/technetwork/database/options/key-management/overview/index.md) [Vault](http://www.oracle.com/technetwork/database/options/key-management/overview/index.md) site and consult the Oracle Key Vault Administrator's Guide.

- 1. Create the configuration directory that contains the Oracle Key Vault support files, and make sure that the keyring\_okv\_conf\_dir system variable is set to name that directory (for details, see [General keyring\\_okv Configuration\)](#page-159-0).
- 2. Log in to the Oracle Key Vault management console as a user who has the System Administrator role.
- 3. Select the Endpoints tab to arrive at the Endpoints page. On the Endpoints page, click Add.
- 4. Provide the required endpoint information and click Register. The endpoint type should be Other. Successful registration results in an enrollment token.
- 5. Log out from the Oracle Key Vault server.
- 6. Connect again to the Oracle Key Vault server, this time without logging in. Use the endpoint enrollment token to enroll and request the okvclient.jar software download. Save this file to your system.
- 7. Install the okvclient.jar file using the following command (you must have JDK 1.4 or higher):

```
java -jar okvclient.jar -d dir_name [-v]
```

The directory name following the -d option is the location in which to install extracted files. The -v option, if given, causes log information to be produced that may be useful if the command fails.

When the command asks for an Oracle Key Vault endpoint password, do not provide one. Instead, press **Enter**. (The result is that no password is required when the endpoint connects to Oracle Key Vault.)

The preceding command produces an okvclient.ora file, which should be in this location under the directory named by the -d option in the preceding java -jar command:

```
install_dir/conf/okvclient.ora
```

The expected file contents include lines that look like this:

```
SERVER=host_ip:port_num
STANDBY_SERVER=host_ip:port_num
```

The SERVER variable is mandatory, and the STANDBY\_SERVER variable is optional. The keyring\_okv plugin attempts to communicate with the server running on the host named by the SERVER variable and falls back to STANDBY\_SERVER if that fails.

![](_page_161_Picture_8.jpeg)

#### **Note**

If the existing file is not in this format, then create a new file with the lines shown in the previous example. Also, consider backing up the okvclient.ora file before you run the okvutil command. Restore the file as needed.

From MySQL 8.0.29, you can specify more than one standby server (up to a maximum of 64). If you do, the keyring\_okv plugin iterates over them until it can establish a connection, and fails if it cannot. To add extra standby servers, edit the okvclient.ora file to specify the IP addresses and port numbers of the servers as a comma-separated list in the value of the STANDBY\_SERVER variable. For example:

```
STANDBY_SERVER=host_ip:port_num,host_ip:port_num,host_ip:port_num,host_ip:port_num
```

Ensure that the list of standby servers is kept short, accurate, and up to date, and servers that are no longer valid are removed. There is a 20-second wait for each connection attempt, so the presence of a long list of invalid servers can significantly affect the keyring\_okv plugin's connection time and therefore the server startup time.

8. Go to the Oracle Key Vault installer directory and test the setup by running this command:

```
okvutil/bin/okvutil list
```

The output should look something like this:

```
Unique ID Type Identifier
255AB8DE-C97F-482C-E053-0100007F28B9 Symmetric Key -
264BF6E0-A20E-7C42-E053-0100007FB29C Symmetric Key -
```

For a fresh Oracle Key Vault server (a server without any key in it), the output looks like this instead, to indicate that there are no keys in the vault:

```
no objects found
```

9. Use this command to extract the ssl directory containing SSL materials from the okvclient.jar file:

```
jar xf okvclient.jar ssl
```

10. Copy the Oracle Key Vault support files (the okvclient.ora file and the ssl directory) into the configuration directory.

11. (Optional) If you wish to password-protect the key file, use the instructions in [Password-Protecting](#page-163-2) [the keyring\\_okv Key File.](#page-163-2)

After completing the preceding procedure, restart the MySQL server. It loads the keyring\_okv plugin and keyring\_okv uses the files in its configuration directory to communicate with Oracle Key Vault.

## <span id="page-162-0"></span>**Configuring keyring\_okv for Gemalto SafeNet KeySecure Appliance**

Gemalto SafeNet KeySecure Appliance uses the KMIP protocol (version 1.1 or 1.2). The keyring\_okv keyring plugin (which supports KMIP 1.1) can use KeySecure as its KMIP back end for keyring storage.

Use the following procedure to configure keyring\_okv and KeySecure to work together. The description only summarizes how to interact with KeySecure. For details, consult the section named Add a KMIP Server in the [KeySecure User Guide.](https://www2.gemalto.com/aws-marketplace/usage/vks/uploadedFiles/Support_and_Downloads/AWS/007-012362-001-keysecure-appliance-user-guide-v7.1.0.pdf)

- 1. Create the configuration directory that contains the KeySecure support files, and make sure that the keyring\_okv\_conf\_dir system variable is set to name that directory (for details, see [General](#page-159-0) [keyring\\_okv Configuration\)](#page-159-0).
- 2. In the configuration directory, create a subdirectory named ssl to use for storing the required SSL certificate and key files.
- 3. In the configuration directory, create a file named okvclient.ora. It should have following format:

```
SERVER=host_ip:port_num
STANDBY_SERVER=host_ip:port_num
```

For example, if KeySecure is running on host 198.51.100.20 and listening on port 9002, and also running on alternative host 203.0.113.125 and listening on port 8041, the okvclient.ora file looks like this:

```
SERVER=198.51.100.20:9002
STANDBY_SERVER=203.0.113.125:8041
```

From MySQL 8.0.29, you can specify more than one standby server (up to a maximum of 64). If you do, the keyring\_okv plugin iterates over them until it can establish a connection, and fails if it cannot. To add extra standby servers, edit the okvclient.ora file to specify the IP addresses and port numbers of the servers as a comma-separated list in the value of the STANDBY\_SERVER variable. For example:

```
STANDBY_SERVER=host_ip:port_num,host_ip:port_num,host_ip:port_num,host_ip:port_num
```

Ensure that the list of standby servers is kept short, accurate, and up to date, and servers that are no longer valid are removed. There is a 20-second wait for each connection attempt, so the presence of a long list of invalid servers can significantly affect the keyring\_okv plugin's connection time and therefore the server startup time.

- 4. Connect to the KeySecure Management Console as an administrator with credentials for Certificate Authorities access.
- 5. Navigate to Security >> Local CAs and create a local certificate authority (CA).
- 6. Go to Trusted CA Lists. Select Default and click on Properties. Then select Edit for Trusted Certificate Authority List and add the CA just created.
- 7. Download the CA and save it in the ssl directory as a file named CA.pem.
- 8. Navigate to Security >> Certificate Requests and create a certificate. Then you can download a compressed tar file containing certificate PEM files.
- 9. Extract the PEM files from in the downloaded file. For example, if the file name is csr\_w\_pk\_pkcs8.gz, decompress and unpack it using this command:

```
tar zxvf csr_w_pk_pkcs8.gz
```

Two files result from the extraction operation: certificate\_request.pem and private\_key\_pkcs8.pem.

10. Use this openssl command to decrypt the private key and create a file named key.pem:

```
openssl pkcs8 -in private_key_pkcs8.pem -out key.pem
```

- 11. Copy the key.pem file into the ssl directory.
- 12. Copy the certificate request in certificate\_request.pem into the clipboard.
- 13. Navigate to Security >> Local CAs. Select the same CA that you created earlier (the one you downloaded to create the CA.pem file), and click Sign Request. Paste the Certificate Request from the clipboard, choose a certificate purpose of Client (the keyring is a client of KeySecure), and click Sign Request. The result is a certificate signed with the selected CA in a new page.
- 14. Copy the signed certificate to the clipboard, then save the clipboard contents as a file named cert.pem in the ssl directory.
- 15. (Optional) If you wish to password-protect the key file, use the instructions in [Password-Protecting](#page-163-2) [the keyring\\_okv Key File.](#page-163-2)

After completing the preceding procedure, restart the MySQL server. It loads the keyring\_okv plugin and keyring\_okv uses the files in its configuration directory to communicate with KeySecure.

## <span id="page-163-0"></span>**Configuring keyring\_okv for Townsend Alliance Key Manager**

Townsend Alliance Key Manager uses the KMIP protocol. The keyring\_okv keyring plugin can use Alliance Key Manager as its KMIP back end for keyring storage. For additional information, see [Alliance Key Manager for MySQL.](https://www.townsendsecurity.com/product/encryption-key-management-mysql)

# <span id="page-163-1"></span>**Configuring keyring\_okv for Entrust KeyControl**

Entrust KeyControl uses the KMIP protocol. The keyring\_okv keyring plugin can use Entrust KeyControl as its KMIP back end for keyring storage. For additional information, see the [Oracle MySQL](https://www.entrust.com/-/media/documentation/integration-guides/oracle-mysql-enterprise-keycontrol-nshield-ig.pdf) [and Entrust KeyControl with nShield HSM Integration Guide.](https://www.entrust.com/-/media/documentation/integration-guides/oracle-mysql-enterprise-keycontrol-nshield-ig.pdf)

## <span id="page-163-2"></span>**Password-Protecting the keyring\_okv Key File**

You can optionally protect the key file with a password and supply a file containing the password to enable the key file to be decrypted. To so do, change location to the ssl directory and perform these steps:

1. Encrypt the key.pem key file. For example, use a command like this, and enter the encryption password at the prompts:

```
$> openssl rsa -des3 -in key.pem -out key.pem.new
Enter PEM pass phrase:
Verifying - Enter PEM pass phrase:
```

- 2. Save the encryption password in a single-line text file named password.txt in the ssl directory.
- 3. Verify that the encrypted key file can be decrypted using the following command. The decrypted file should display on the console:

```
$> openssl rsa -in key.pem.new -passin file:password.txt
```

- 4. Remove the original key.pem file and rename key.pem.new to key.pem.
- 5. Change the ownership and access mode of new key.pem file and password.txt file as necessary to ensure that they have the same restrictions as other files in the ssl directory.

# <span id="page-164-0"></span>**8.4.4.9 Using the keyring\_aws Amazon Web Services Keyring Plugin**

![](_page_164_Picture_2.jpeg)

#### **Note**

The keyring\_aws plugin is an extension included in MySQL Enterprise Edition, a commercial product. To learn more about commercial products, see <https://www.mysql.com/products/>.

The keyring\_aws keyring plugin communicates with the Amazon Web Services Key Management Service (AWS KMS) as a back end for key generation and uses a local file for key storage. All keyring material is generated exclusively by the AWS server, not by keyring\_aws.

MySQL Enterprise Edition can work with keyring\_aws on Red Hat Enterprise Linux, SUSE Linux Enterprise Server, Debian, Ubuntu, macOS, and Windows. MySQL Enterprise Edition does not support the use of keyring\_aws on these platforms:

- EL6
- Generic Linux (glibc2.12)
- SLES 12 (with versions after MySQL Server 5.7)
- Solaris

The discussion here assumes that you are familiar with AWS in general and KMS in particular. Some pertinent information sources:

- [AWS site](https://aws.amazon.com/kms/)
- [KMS documentation](https://docs.aws.amazon.com/kms/)

The following sections provide configuration and usage information for the keyring\_aws keyring plugin:

- [keyring\\_aws Configuration](#page-164-1)
- [keyring\\_aws Operation](#page-166-0)
- [keyring\\_aws Credential Changes](#page-166-1)

## <span id="page-164-1"></span>**keyring\_aws Configuration**

To install keyring\_aws, use the general instructions found in [Section 8.4.4.3, "Keyring Plugin](#page-148-0) [Installation"](#page-148-0), together with the plugin-specific configuration information found here.

The plugin library file contains the keyring\_aws plugin and two loadable functions, [keyring\\_aws\\_rotate\\_cmk\(\)](#page-196-0) and [keyring\\_aws\\_rotate\\_keys\(\)](#page-197-0).

To configure keyring\_aws, you must obtain a secret access key that provides credentials for communicating with AWS KMS and write it to a configuration file:

- 1. Create an AWS KMS account.
- 2. Use AWS KMS to create a secret access key ID and secret access key. The access key serves to verify your identity and that of your applications.
- 3. Use the AWS KMS account to create a KMS key ID. At MySQL startup, set the keyring\_aws\_cmk\_id system variable to the CMK ID value. This variable is mandatory and there is no default. (Its value can be changed at runtime if desired using SET GLOBAL.)
- 4. If necessary, create the directory in which the configuration file should be located. The directory should have a restrictive mode and be accessible only to the account used to run the MySQL server. For example, on many Unix and Unix-like systems, such as Oracle Enterprise Linux,

to use /usr/local/mysql/mysql-keyring/keyring\_aws\_conf as the file name, the following commands (executed as root) create its parent directory and set the directory mode and ownership:

```
$> cd /usr/local/mysql
$> mkdir mysql-keyring
$> chmod 750 mysql-keyring
$> chown mysql mysql-keyring
$> chgrp mysql mysql-keyring
```

At MySQL startup, set the keyring\_aws\_conf\_file system variable to /usr/local/mysql/ mysql-keyring/keyring\_aws\_conf to indicate the configuration file location to the server.

The location of the configuration file may vary according to Linux distribution; the directory for this file may also already be provided by a system module or other application such as AppArmor. For example, under AppArmor on recent editions of Ubuntu Linux, the keyring directory is specified as /var/lib/mysql-keyring. See [Ubuntu Server: AppArmor](https://documentation.ubuntu.com/server/how-to/security/apparmor/index.md) for more information about using AppArmor on Ubuntu systems; see also [this example MySQL configuration file.](https://exampleconfig.com/view/mysql-ubuntu20-04-etc-apparmor-d-usr-sbin-mysqld) For other operating platforms, see the system documentation for guidance.

- 5. Prepare the keyring\_aws configuration file, which should contain two lines:
  - Line 1: The secret access key ID
  - Line 2: The secret access key

For example, if the key ID is wwwwwwwwwwwwwEXAMPLE and the key is xxxxxxxxxxxxx/ yyyyyyy/zzzzzzzzEXAMPLEKEY, the configuration file looks like this:

```
wwwwwwwwwwwwwEXAMPLE
xxxxxxxxxxxxx/yyyyyyy/zzzzzzzzEXAMPLEKEY
```

To be usable during the server startup process, keyring\_aws must be loaded using the - early-plugin-load option. The keyring\_aws\_cmk\_id system variable is mandatory and configures the KMS key ID obtained from the AWS KMS server. The keyring\_aws\_conf\_file and keyring\_aws\_data\_file system variables optionally configure the locations of the files used by the keyring\_aws plugin for configuration information and data storage. The file location variable default values are platform specific. To configure the locations explicitly, set the variable values at startup. For example, use these lines in the server my.cnf file, adjusting the .so suffix and file locations for your platform as necessary:

```
[mysqld]
early-plugin-load=keyring_aws.so
keyring_aws_cmk_id='arn:aws:kms:us-west-2:111122223333:key/abcd1234-ef56-ab12-cd34-ef56abcd1234'
keyring_aws_conf_file=/usr/local/mysql/mysql-keyring/keyring_aws_conf
keyring_aws_data_file=/usr/local/mysql/mysql-keyring/keyring_aws_data
```

For the keyring\_aws plugin to start successfully, the configuration file must exist and contain valid secret access key information, initialized as described previously. The storage file need not exist. If it does not, keyring\_aws attempts to create it (as well as its parent directory, if necessary).

![](_page_165_Picture_13.jpeg)

#### **Important**

The default AWS region is us-east-1. For any other region, you must also set keyring\_aws\_region explicitly in my.cnf.

For additional information about the system variables used to configure the keyring\_aws plugin, see Section 8.4.4.19, "Keyring System Variables".

Start the MySQL server and install the functions associated with the keyring\_aws plugin. This is a one-time operation, performed by executing the following statements, adjusting the .so suffix for your platform as necessary:

```
CREATE FUNCTION keyring_aws_rotate_cmk RETURNS INTEGER
```

```
 SONAME 'keyring_aws.so';
CREATE FUNCTION keyring_aws_rotate_keys RETURNS INTEGER
 SONAME 'keyring_aws.so';
```

For additional information about the keyring\_aws functions, see [Section 8.4.4.16, "Plugin-Specific](#page-196-1) [Keyring Key-Management Functions"](#page-196-1).

## <span id="page-166-0"></span>**keyring\_aws Operation**

At plugin startup, the keyring\_aws plugin reads the AWS secret access key ID and key from its configuration file. It also reads any encrypted keys contained in its storage file into its in-memory cache.

During operation, keyring\_aws maintains encrypted keys in the in-memory cache and uses the storage file as local persistent storage. Each keyring operation is transactional: keyring\_aws either successfully changes both the in-memory key cache and the keyring storage file, or the operation fails and the keyring state remains unchanged.

To ensure that keys are flushed only when the correct keyring storage file exists, keyring\_aws stores a SHA-256 checksum of the keyring in the file. Before updating the file, the plugin verifies that it contains the expected checksum.

The keyring\_aws plugin supports the functions that comprise the standard MySQL Keyring service interface. Keyring operations performed by these functions are accessible at two levels:

- SQL interface: In SQL statements, call the functions described in [Section 8.4.4.15, "General-Purpose](#page-189-0) [Keyring Key-Management Functions"](#page-189-0).
- C interface: In C-language code, call the keyring service functions described in Section 7.6.9.2, "The Keyring Service".

Example (using the SQL interface):

```
SELECT keyring_key_generate('MyKey', 'AES', 32);
SELECT keyring_key_remove('MyKey');
```

In addition, the [keyring\\_aws\\_rotate\\_cmk\(\)](#page-196-0) and [keyring\\_aws\\_rotate\\_keys\(\)](#page-197-0) functions "extend" the keyring plugin interface to provide AWS-related capabilities not covered by the standard keyring service interface. These capabilities are accessible only by calling these functions using SQL. There are no corresponding C-language key service functions.

For information about the characteristics of key values permitted by keyring\_aws, see [Section 8.4.4.13, "Supported Keyring Key Types and Lengths"](#page-181-0).

## <span id="page-166-1"></span>**keyring\_aws Credential Changes**

Assuming that the keyring\_aws plugin has initialized properly at server startup, it is possible to change the credentials used for communicating with AWS KMS:

- 1. Use AWS KMS to create a new secret access key ID and secret access key.
- 2. Store the new credentials in the configuration file (the file named by the keyring\_aws\_conf\_file system variable). The file format is as described previously.
- 3. Reinitialize the keyring\_aws plugin so that it re-reads the configuration file. Assuming that the new credentials are valid, the plugin should initialize successfully.

There are two ways to reinitialize the plugin:

- Restart the server. This is simpler and has no side effects, but is not suitable for installations that require minimal server downtime with as few restarts as possible.
- Reinitialize the plugin without restarting the server by executing the following statements, adjusting the .so suffix for your platform as necessary:

UNINSTALL PLUGIN keyring\_aws; INSTALL PLUGIN keyring\_aws SONAME 'keyring\_aws.so';

![](_page_167_Picture_2.jpeg)

#### **Note**

In addition to loading a plugin at runtime, INSTALL PLUGIN has the side effect of registering the plugin it in the mysql.plugin system table. Because of this, if you decide to stop using keyring\_aws, it is not sufficient to remove the --early-plugin-load option from the set of options used to start the server. That stops the plugin from loading early, but the server still attempts to load it when it gets to the point in the startup sequence where it loads the plugins registered in mysql.plugin.

Consequently, if you execute the UNINSTALL PLUGIN plus INSTALL PLUGIN sequence just described to change the AWS KMS credentials, then to stop using keyring\_aws, it is necessary to execute UNINSTALL PLUGIN again to unregister the plugin in addition to removing the - early-plugin-load option.

# <span id="page-167-0"></span>**8.4.4.10 Using the HashiCorp Vault Keyring Plugin**

![](_page_167_Picture_7.jpeg)

#### **Note**

The keyring\_hashicorp plugin is an extension included in MySQL Enterprise Edition, a commercial product. To learn more about commercial products, see<https://www.mysql.com/products/>.

The keyring\_hashicorp keyring plugin communicates with HashiCorp Vault for back end storage. The plugin supports HashiCorp Vault AppRole authentication. No key information is permanently stored in MySQL server local storage. (An optional in-memory key cache may be used as intermediate storage.) Random key generation is performed on the MySQL server side, with the keys subsequently stored to Hashicorp Vault.

The keyring\_hashicorp plugin supports the functions that comprise the standard MySQL Keyring service interface. Keyring operations performed by those functions are accessible at two levels:

- SQL interface: In SQL statements, call the functions described in [Section 8.4.4.15, "General-Purpose](#page-189-0) [Keyring Key-Management Functions"](#page-189-0).
- C interface: In C-language code, call the keyring service functions described in Section 7.6.9.2, "The Keyring Service".

Example (using the SQL interface):

```
SELECT keyring_key_generate('MyKey', 'AES', 32);
SELECT keyring_key_remove('MyKey');
```

For information about the characteristics of key values permitted by keyring\_hashicorp, see [Section 8.4.4.13, "Supported Keyring Key Types and Lengths"](#page-181-0).

To install keyring\_hashicorp, use the general instructions found in [Section 8.4.4.3, "Keyring Plugin](#page-148-0) [Installation"](#page-148-0), together with the configuration information specific to keyring\_hashicorp found here. Plugin-specific configuration includes preparation of the certificate and key files needed for connecting to HashiCorp Vault, as well as configuring HashiCorp Vault itself. The following sections provide the necessary instructions.

- [Certificate and Key Preparation](#page-168-0)
- [HashiCorp Vault Setup](#page-169-0)
- [keyring\\_hashicorp Configuration](#page-172-0)

## <span id="page-168-0"></span>**Certificate and Key Preparation**

The keyring\_hashicorp plugin requires a secure connection to the HashiCorp Vault server, employing the HTTPS protocol. A typical setup includes a set of certificate and key files:

- company.crt: A custom CA certificate belonging to the organization. This file is used both by HashiCorp Vault server and the keyring\_hashicorp plugin.
- vault.key: The private key of the HashiCorp Vault server instance. This file is used by HashiCorp Vault server.
- vault.crt: The certificate of the HashiCorp Vault server instance. This file must be signed by the organization CA certificate.

The following instructions describe how to create the certificate and key files using OpenSSL. (If you already have those files, proceed to [HashiCorp Vault Setup](#page-169-0).) The instructions as shown apply to Linux platforms and may require adjustment for other platforms.

![](_page_168_Picture_7.jpeg)

## **Important**

Certificates generated by these instructions are self-signed, which may not be very secure. After you gain experience using such files, consider obtaining certificate/key material from a registered certificate authority.

1. Prepare the company and HashiCorp Vault server keys.

Use the following commands to generate the key files:

```
openssl genrsa -aes256 -out company.key 4096
openssl genrsa -aes256 -out vault.key 2048
```

The commands produce files holding the company private key (company.key) and the Vault server private key (vault.key). The keys are randomly generated RSA keys of 4,096 and 2,048 bits, respectively.

Each command prompts for a password. For testing purposes, the password is not required. To disable it, omit the -aes256 argument.

The key files hold sensitive information and should be stored in a secure location. The password (also sensitive) is required later, so write it down and store it in a secure location.

(Optional) To check key file content and validity, use the following commands:

```
openssl rsa -in company.key -check
openssl rsa -in vault.key -check
```

2. Create the company CA certificate.

Use the following command to create a company CA certificate file named company.crt that is valid for 365 days (enter the command on a single line):

```
openssl req -x509 -new -nodes -key company.key
 -sha256 -days 365 -out company.crt
```

If you used the -aes256 argument to perform key encryption during key generation, you are prompted for the company key password during CA certificate creation. You are also prompted for information about the certificate holder (that is, you or your company), as shown here:

```
Country Name (2 letter code) [AU]:
State or Province Name (full name) [Some-State]:
Locality Name (eg, city) []:
Organization Name (eg, company) [Internet Widgits Pty Ltd]:
Organizational Unit Name (eg, section) []:
Common Name (e.g. server FQDN or YOUR name) []:
Email Address []:
```

Answer the prompts with appropriate values.

3. Create a certificate signing request.

To create a HashiCorp Vault server certificate, a Certificate Signing Request (CSR) must be prepared for the newly created server key. Create a configuration file named request.conf containing the following lines. If the HashiCorp Vault server does not run on the local host, substitute appropriate CN and IP values, and make any other changes required.

```
[req]
distinguished_name = vault
x509_entensions = v3_req
prompt = no
[vault]
C = US
ST = CA
L = RWC
O = Company
CN = 127.0.0.1
[v3_req]
subjectAltName = @alternatives
authorityKeyIdentifier = keyid,issuer
basicConstraints = CA:TRUE
[alternatives]
IP = 127.0.0.1
```

Use this command to create the signing request:

```
openssl req -new -key vault.key -config request.conf -out request.csr
```

The output file (request.csr) is an intermediate file that serves as input for creation of the server certificate.

4. Create the HashiCorp Vault server certificate.

Sign the combined information from the HashiCorp Vault server key (vault.key) and the CSR (request.csr) with the company certificate (company.crt) to create the HashiCorp Vault server certificate (vault.crt). Use the following command to do this (enter the command on a single line):

```
openssl x509 -req -in request.csr
 -CA company.crt -CAkey company.key -CAcreateserial
 -out vault.crt -days 365 -sha256
```

To make the vault.crt server certificate useful, append the contents of the company.crt company certificate to it. This is required so that the company certificate is delivered along with the server certificate in requests.

```
cat company.crt >> vault.crt
```

If you display the contents of the vault.crt file, it should look like this:

```
-----BEGIN CERTIFICATE-----
... content of HashiCorp Vault server certificate ...
-----END CERTIFICATE-----
-----BEGIN CERTIFICATE-----
... content of company certificate ...
-----END CERTIFICATE-----
```

## <span id="page-169-0"></span>**HashiCorp Vault Setup**

The following instructions describe how to create a HashiCorp Vault setup that facilitates testing the keyring\_hashicorp plugin.

![](_page_170_Picture_1.jpeg)

## **Important**

A test setup is similar to a production setup, but production use of HashiCorp Vault entails additional security considerations such as use of non-self-signed certificates and storing the company certificate in the system trust store. You must implement whatever additional security steps are needed to satisfy your operational requirements.

These instructions assume availability of the certificate and key files created in [Certificate and Key](#page-168-0) [Preparation.](#page-168-0) See that section if you do not have those files.

1. Fetch the HashiCorp Vault binary.

Download the HashiCorp Vault binary appropriate for your platform from [https://www.vaultproject.io/](https://www.vaultproject.io/downloads.md) [downloads.html](https://www.vaultproject.io/downloads.md).

Extract the content of the archive to produce the executable vault command, which is used to perform HashiCorp Vault operations. If necessary, add the directory where you install the command to the system path.

(Optional) HashiCorp Vault supports autocomplete options that make it easier to use. For more information, see <https://learn.hashicorp.com/vault/getting-started/install#command-completion>.

2. Create the HashiCorp Vault server configuration file.

Prepare a configuration file named config.hcl with the following content. For the tls\_cert\_file, tls\_key\_file, and path values, substitute path names appropriate for your system.

```
listener "tcp" {
 address="127.0.0.1:8200"
 tls_cert_file="/home/username/certificates/vault.crt"
 tls_key_file="/home/username/certificates/vault.key"
}
storage "file" {
 path = "/home/username/vaultstorage/storage"
}
ui = true
```

3. Start the HashiCorp Vault server.

To start the Vault server, use the following command, where the -config option specifies the path to the configuration file just created:

```
vault server -config=config.hcl
```

During this step, you may be prompted for a password for the Vault server private key stored in the vault.key file.

The server should start, displaying some information on the console (IP, port, and so forth).

So that you can enter the remaining commands, put the vault server command in the background or open another terminal before continuing.

4. Initialize the HashiCorp Vault server.

![](_page_170_Picture_19.jpeg)

#### **Note**

The operations described in this step are required only when starting Vault the first time, to obtain the unseal key and root token. Subsequent Vault instance restarts require only unsealing using the unseal key.

Issue the following commands (assuming Bourne shell syntax):

```
export VAULT_SKIP_VERIFY=1
vault operator init -n 1 -t 1
```

The first command enables the vault command to temporarily ignore the fact that no company certificate has been added to the system trust store. It compensates for the fact that our self-signed CA is not added to that store. (For production use, such a certificate should be added.)

The second command creates a single unseal key with a requirement for a single unseal key to be present for unsealing. (For production use, an instance would have multiple unseal keys with up to that many keys required to be entered to unseal it. The unseal keys should be delivered to key custodians within the company. Use of a single key might be considered a security issue because that permits the vault to be unsealed by a single key custodian.)

Vault should reply with information about the unseal key and root token, plus some additional text (the actual unseal key and root token values differ from those shown here):

```
...
Unseal Key 1: I2xwcFQc892O0Nt2pBiRNlnkHzTUrWS+JybL39BjcOE=
Initial Root Token: s.vTvXeo3tPEYehfcd9WH7oUKz
...
```

Store the unseal key and root token in a secure location.

5. Unseal the HashiCorp Vault server.

Use this command to unseal the Vault server:

```
vault operator unseal
```

When prompted to enter the unseal key, use the key obtained previously during Vault initialization.

Vault should produce output indicating that setup is complete and the vault is unsealed.

6. Log in to the HashiCorp Vault server and verify its status.

Prepare the environment variables required for logging in as root:

```
vault login s.vTvXeo3tPEYehfcd9WH7oUKz
```

For the token value in that command, substitute the content of the root token obtained previously during Vault initialization.

Verify the Vault server status:

```
vault status
```

The output should contain these lines (among others):

```
...
Initialized true
Sealed false
...
```

7. Set up HashiCorp Vault authentication and storage.

![](_page_172_Picture_2.jpeg)

#### **Note**

The operations described in this step are needed only the first time the Vault instance is run. They need not be repeated afterward.

Enable the AppRole authentication method and verify that it is in the authentication method list:

```
vault auth enable approle
vault auth list
```

Enable the Vault KeyValue storage engine:

```
vault secrets enable -version=1 kv
```

Create and set up a role for use with the keyring\_hashicorp plugin (enter the command on a single line):

```
vault write auth/approle/role/mysql token_num_uses=0
 token_ttl=20m token_max_ttl=30m secret_id_num_uses=0
```

8. Add an AppRole security policy.

![](_page_172_Picture_12.jpeg)

### **Note**

The operations described in this step are needed only the first time the Vault instance is run. They need not be repeated afterward.

Prepare a policy that to permit the previously created role to access appropriate secrets. Create a new file named mysql.hcl with the following content:

```
path "kv/mysql/*" {
 capabilities = ["create", "read", "update", "delete", "list"]
}
```

![](_page_172_Picture_17.jpeg)

#### **Note**

kv/mysql/ in this example may need adjustment per your local installation policies and security requirements. If so, make the same adjustment wherever else kv/mysql/ appears in these instructions.

Import the policy file to the Vault server to create a policy named mysql-policy, then assign the policy to the new role:

```
vault policy write mysql-policy mysql.hcl
vault write auth/approle/role/mysql policies=mysql-policy
```

Obtain the ID of the newly created role and store it in a secure location:

```
vault read auth/approle/role/mysql/role-id
```

Generate a secret ID for the role and store it in a secure location:

```
vault write -f auth/approle/role/mysql/secret-id
```

After these AppRole role ID and secret ID credentials are generated, they are expected to remain valid indefinitely. They need not be generated again and the keyring\_hashicorp plugin can be configured with them for use on an ongoing basis. For more information about AuthRole authentication, visit [https://www.vaultproject.io/docs/auth/approle.html.](https://www.vaultproject.io/docs/auth/approle.md)

## <span id="page-172-0"></span>**keyring\_hashicorp Configuration**

The plugin library file contains the keyring\_hashicorp plugin and a loadable function, [keyring\\_hashicorp\\_update\\_config\(\)](#page-197-1). When the plugin initializes and terminates, it automatically loads and unloads the function. There is no need to load and unload the function manually.

The keyring\_hashicorp plugin supports the configuration parameters shown in the following table. To specify these parameters, assign values to the corresponding system variables.

| Configuration Parameter  | System Variable                  | Mandatory |
|--------------------------|----------------------------------|-----------|
| HashiCorp Server URL     | keyring_hashicorp_server_url No  |           |
| AppRole role ID          | keyring_hashicorp_role_id Yes    |           |
| AppRole secret ID        | keyring_hashicorp_secret_idYes   |           |
| Store path               | keyring_hashicorp_store_path Yes |           |
| Authorization Path       | keyring_hashicorp_auth_pathNo    |           |
| CA certificate file path | keyring_hashicorp_ca_path No     |           |
| Cache control            | keyring_hashicorp_caching No     |           |

To be usable during the server startup process, keyring\_hashicorp must be loaded using the - early-plugin-load option. As indicated by the preceding table, several plugin-related system variables are mandatory and must also be set. For example, use these lines in the server my.cnf file, adjusting the .so suffix and file locations for your platform as necessary:

```
[mysqld]
early-plugin-load=keyring_hashicorp.so
keyring_hashicorp_role_id='ee3b495c-d0c9-11e9-8881-8444c71c32aa'
keyring_hashicorp_secret_id='0512af29-d0ca-11e9-95ee-0010e00dd718'
keyring_hashicorp_store_path='/v1/kv/mysql'
keyring_hashicorp_auth_path='/v1/auth/approle/login'
```

![](_page_173_Picture_6.jpeg)

# **Note**

Per the [HashiCorp documentation,](https://www.vaultproject.io/api-docs) all API routes are prefixed with a protocol version (which you can see in the preceding example as /v1/ in the keyring\_hashicorp\_store\_path and keyring\_hashicorp\_auth\_path values). If HashiCorp develops new protocol versions, it may be necessary to change /v1/ to something else in your configuration.

MySQL Server authenticates against HashiCorp Vault using AppRole authentication. Successful authentication requires that two secrets be provided to Vault, a role ID and a secret ID, which are similar in concept to user name and password. The role ID and secret ID values to use are those obtained during the HashiCorp Vault setup procedure performed previously. To specify the two IDs, assign their respective values to the keyring\_hashicorp\_role\_id and keyring\_hashicorp\_secret\_id system variables. The setup procedure also results in a store path of /v1/kv/mysql, which is the value to assign to keyring\_hashicorp\_commit\_store\_path.

At plugin initialization time, keyring\_hashicorp attempts to connect to the HashiCorp Vault server using the configuration values. If the connection is successful, the plugin stores the values in corresponding system variables that have \_commit\_ in their name. For example, upon successful connection, the plugin stores the values of keyring\_hashicorp\_role\_id and keyring\_hashicorp\_store\_path in keyring\_hashicorp\_commit\_role\_id and keyring\_hashicorp\_commit\_store\_path.

Reconfiguration at runtime can be performed with the assistance of the [keyring\\_hashicorp\\_update\\_config\(\)](#page-197-1) function:

1. Use SET statements to assign the desired new values to the configuration system variables shown in the preceding table. These assignments in themselves have no effect on ongoing plugin operation.

- 2. Invoke [keyring\\_hashicorp\\_update\\_config\(\)](#page-197-1) to cause the plugin to reconfigure and reconnect to the HashiCorp Vault server using the new variable values.
- 3. If the connection is successful, the plugin stores the updated configuration values in corresponding system variables that have \_commit\_ in their name.

For example, if you have reconfigured HashiCorp Vault to listen on port 8201 rather than the default 8200, reconfigure keyring\_hashicorp like this:

```
mysql> SET GLOBAL keyring_hashicorp_server_url = 'https://127.0.0.1:8201';
Query OK, 0 rows affected (0.00 sec)
mysql> SELECT keyring_hashicorp_update_config();
+--------------------------------------+
| keyring_hashicorp_update_config() |
+--------------------------------------+
| Configuration update was successful. |
+--------------------------------------+
1 row in set (0.03 sec)
```

If the plugin is not able to connect to HashiCorp Vault during initialization or reconfiguration and there was no existing connection, the \_commit\_ system variables are set to 'Not committed' for stringvalued variables, and OFF for Boolean-valued variables. If the plugin is not able to connect but there was an existing connection, that connection remains active and the \_commit\_ variables reflect the values used for it.

![](_page_174_Picture_6.jpeg)

#### **Note**

If you do not set the mandatory system variables at server startup, or if some other plugin initialization error occurs, initialization fails. In this case, you can use the runtime reconfiguration procedure to initialize the plugin without restarting the server.

For additional information about the keyring\_hashicorp plugin-specific system variables and function, see Section 8.4.4.19, "Keyring System Variables", and [Section 8.4.4.16, "Plugin-Specific](#page-196-1) [Keyring Key-Management Functions"](#page-196-1).

# <span id="page-174-0"></span>**8.4.4.11 Using the Oracle Cloud Infrastructure Vault Keyring Component**

![](_page_174_Picture_11.jpeg)

# **Note**

The Oracle Cloud Infrastructure Vault keyring component is included in MySQL Enterprise Edition, a commercial product. To learn more about commercial products, see<https://www.mysql.com/products/>.

component\_keyring\_oci is part of the component infrastructure that communicates with Oracle Cloud Infrastructure Vault for back end storage. No key information is permanently stored in MySQL server local storage. All keys are stored in Oracle Cloud Infrastructure Vault, making this component well suited for Oracle Cloud Infrastructure MySQL customers for management of their MySQL Enterprise Edition keys.

In MySQL 8.0.24, MySQL Keyring began transitioning from plugins to use the component infrastructure. The introduction of component\_keyring\_oci in MySQL 8.0.31 is a continuation of that effort. For more information, see [Keyring Components Versus Keyring Plugins.](#page-145-0)

![](_page_174_Picture_16.jpeg)

## **Note**

Only one keyring component or plugin should be enabled at a time. Enabling multiple keyring components or plugins is unsupported and results may not be as anticipated.

To use component\_keyring\_oci for keystore management, you must:

- 1. Write a manifest that tells the server to load component\_keyring\_oci, as described in [Section 8.4.4.2, "Keyring Component Installation".](#page-145-1)
- 2. Write a configuration file for component\_keyring\_oci, as described here.

After writing a manifest and configuration file, you should be able to access keys that were created using the keyring\_oci plugin, provided that you specify the same set of configuration options to initialize the keyring component. The built-in backward compatibility of component\_keyring\_oci simplifies migrating from the keyring plugin to the component.

- [Configuration Notes](#page-175-0)
- [Verify the Component Installation](#page-178-1)
- [Vault Keyring Component Usage](#page-178-2)

## <span id="page-175-0"></span>**Configuration Notes**

When it initializes, component\_keyring\_oci reads either a global configuration file, or a global configuration file paired with a local configuration file:

- The component attempts to read its global configuration file from the directory where the component library file is installed (that is, the server plugin directory).
- If the global configuration file indicates use of a local configuration file, the component attempts to read its local configuration file from the data directory.
- Although global and local configuration files are located in different directories, the file name is component\_keyring\_oci.cnf in both locations.
- It is an error for no configuration file to exist. component\_keyring\_oci cannot initialize without a valid configuration.

Local configuration files permit setting up multiple server instances to use component\_keyring\_oci, such that component configuration for each server instance is specific to a given data directory instance. This enables the same keyring component to be used with a distinct Oracle Cloud Infrastructure Vault for each instance.

You are assumed to be familiar with Oracle Cloud Infrastructure concepts, but the following documentation may be helpful when setting up resources to be used by component\_keyring\_oci:

- [Overview of Vault](https://docs.cloud.oracle.com/iaas/Content/KeyManagement/Concepts/keyoverview.md)
- [Required Keys and OCIDs](https://docs.cloud.oracle.com/en-us/iaas/Content/API/Concepts/apisigningkey.md)
- [Managing Keys](https://docs.cloud.oracle.com/en-us/iaas/Content/KeyManagement/Tasks/managingkeys.md)
- [Managing Compartments](https://docs.cloud.oracle.com/en-us/iaas/Content/Identity/Tasks/managingcompartments.md)
- [Managing Vaults](https://docs.cloud.oracle.com/en-us/iaas/Content/KeyManagement/Tasks/managingvaults.md)
- [Managing Secrets](https://docs.cloud.oracle.com/en-us/iaas/Content/KeyManagement/Tasks/managingsecrets.md)

component\_keyring\_oci configuration files have these properties:

- A configuration file must be in valid JSON format.
- A configuration file must have the appropriate file permission that allows MySQL to read it. Since the file contains sensitive information, it should be set to world readable.
- A configuration file permits these configuration items:
  - "read\_local\_config": This item is permitted only in the global configuration file. If the item is not present, the component uses only the global configuration file. If the item is present, its value is

true or false, indicating whether the component should read configuration information from the local configuration file.

If the "read\_local\_config" item is present in the global configuration file along with other items, the component checks the "read\_local\_config" item value first:

- If the value is false, the component processes the other items in the global configuration file and ignores the local configuration file.
- If the value is true, the component ignores the other items in the global configuration file and attempts to read the local configuration file.
- "user": The OCID of the Oracle Cloud Infrastructure user that component\_keyring\_oci uses for connections. Prior to using component\_keyring\_oci, the user account must exist and be granted access to use the configured Oracle Cloud Infrastructure tenancy, compartment, and vault resources. To obtain the user OCID from the Console, use the instructions at [Required Keys and](https://docs.cloud.oracle.com/en-us/iaas/Content/API/Concepts/apisigningkey.md) [OCIDs](https://docs.cloud.oracle.com/en-us/iaas/Content/API/Concepts/apisigningkey.md).

This value is mandatory.

• "tenancy": The OCID of the Oracle Cloud Infrastructure tenancy that component\_keyring\_oci uses as the location of the MySQL compartment. Prior to using component\_keyring\_oci, you must create a tenancy if it does not exist. To obtain the tenancy OCID from the Console, use the instructions at [Required Keys and OCIDs](https://docs.cloud.oracle.com/en-us/iaas/Content/API/Concepts/apisigningkey.md).

This value is mandatory.

• "compartment": The OCID of the tenancy compartment that component\_keyring\_oci uses as the location of the MySQL keys. Prior to using component\_keyring\_oci, you must create a MySQL compartment or subcompartment if it does not exist. This compartment should contain no vault keys or vault secrets. It should not be used by systems other than MySQL Keyring. For information about managing compartments and obtaining the OCID, see [Managing Compartments](https://docs.cloud.oracle.com/en-us/iaas/Content/Identity/Tasks/managingcompartments.md).

This value is mandatory.

• "virtual\_vault": The OCID of the Oracle Cloud Infrastructure Vault that component\_keyring\_oci uses for encryption operations. Prior to using component\_keyring\_oci, you must create a new vault in the MySQL compartment if it does not exist. (Alternatively, you can reuse an existing vault that is in a parent compartment of the MySQL compartment.) Compartment users can see and use only the keys in their respective compartments. For information about creating a vault and obtaining the vault OCID, see [Managing](https://docs.cloud.oracle.com/en-us/iaas/Content/KeyManagement/Tasks/managingvaults.md) [Vaults.](https://docs.cloud.oracle.com/en-us/iaas/Content/KeyManagement/Tasks/managingvaults.md)

This value is mandatory.

• "encryption\_endpoint": The endpoint of the Oracle Cloud Infrastructure encryption server that component\_keyring\_oci uses for generating encrypted or encoded information (ciphertext) for new keys. The encryption endpoint is vault specific and Oracle Cloud Infrastructure assigns it at vault-creation time. To obtain the endpoint OCID, view the configuration details for your keyring\_oci vault, using the instructions at [Managing Vaults.](https://docs.cloud.oracle.com/en-us/iaas/Content/KeyManagement/Tasks/managingvaults.md)

This value is mandatory.

• "management\_endpoint": The endpoint of the Oracle Cloud Infrastructure key management server that component\_keyring\_oci uses for listing existing keys. The key management endpoint is vault specific and Oracle Cloud Infrastructure assigns it at vault-creation time. To

obtain the endpoint OCID, view the configuration details for your keyring\_oci vault, using the instructions at [Managing Vaults.](https://docs.cloud.oracle.com/en-us/iaas/Content/KeyManagement/Tasks/managingvaults.md)

This value is mandatory.

• "vaults\_endpoint": The endpoint of the Oracle Cloud Infrastructure vaults server that component\_keyring\_oci uses for obtaining the value of secrets. The vaults endpoint is vault specific and Oracle Cloud Infrastructure assigns it at vault-creation time. To obtain the endpoint OCID, view the configuration details for your keyring\_oci vault, using the instructions at [Managing](https://docs.cloud.oracle.com/en-us/iaas/Content/KeyManagement/Tasks/managingvaults.md) [Vaults.](https://docs.cloud.oracle.com/en-us/iaas/Content/KeyManagement/Tasks/managingvaults.md)

This value is mandatory.

• "secrets\_endpoint": The endpoint of the Oracle Cloud Infrastructure secrets server that component\_keyring\_oci uses for listing, creating, and retiring secrets. The secrets endpoint is vault specific and Oracle Cloud Infrastructure assigns it at vault-creation time. To obtain the endpoint OCID, view the configuration details for your keyring\_oci vault, using the instructions at [Managing Vaults](https://docs.cloud.oracle.com/en-us/iaas/Content/KeyManagement/Tasks/managingvaults.md).

This value is mandatory.

• "master\_key": The OCID of the Oracle Cloud Infrastructure master encryption key that component\_keyring\_oci uses for encryption of secrets. Prior to using component\_keyring\_oci, you must create a cryptographic key for the Oracle Cloud Infrastructure compartment if it does not exist. Provide a MySQL-specific name for the generated key and do not use it for other purposes. For information about key creation, see [Managing Keys.](https://docs.cloud.oracle.com/en-us/iaas/Content/KeyManagement/Tasks/managingkeys.md)

This value is mandatory.

• "key\_file": The path name of the file containing the RSA private key that component\_keyring\_oci uses for Oracle Cloud Infrastructure authentication. You must also upload the corresponding RSA public key using the Console. The Console displays the key fingerprint value, which you can use to set the "key\_fingerprint" value. For information about generating and uploading API keys, see [Required Keys and OCIDs](https://docs.cloud.oracle.com/en-us/iaas/Content/API/Concepts/apisigningkey.md).

This value is mandatory.

• "key\_fingerprint": The fingerprint of the RSA private key that component\_keyring\_oci uses for Oracle Cloud Infrastructure authentication. To obtain the key fingerprint while creating the API keys, execute this command:

```
openssl rsa -pubout -outform DER -in ~/.oci/oci_api_key.pem | openssl md5 -c
```

Alternatively, obtain the fingerprint from the Console, which automatically displays the fingerprint when you upload the RSA public key. For information about obtaining key fingerprints, see [Required Keys and OCIDs.](https://docs.cloud.oracle.com/en-us/iaas/Content/API/Concepts/apisigningkey.md)

This value is mandatory.

• "ca\_certificate": The path name of the CA certificate bundle file that component\_keyring\_oci component uses for Oracle Cloud Infrastructure certificate verification. The file contains one or more certificates for peer verification. If no file is specified, the default CA bundle installed on the system is used. If the value is set to disabled (case-sensitive), component\_keyring\_oci performs no certificate verification.

On Windows systems, this should be set to disabled, or to the path to a CA certificate bundle file.

Given the preceding configuration file properties, to configure component\_keyring\_oci, create a global configuration file named component\_keyring\_oci.cnf in the directory where the

component\_keyring\_oci library file is installed, and optionally create a local configuration file, also named component\_keyring\_oci.cnf, in the data directory.

## <span id="page-178-1"></span>**Verify the Component Installation**

After performing any component-specific configuration, start the server. Verify component installation by examining the Performance Schema keyring\_component\_status table:

```
mysql> SELECT * FROM performance_schema.keyring_component_status;
+---------------------+--------------------------------------------------------------------+
| STATUS_KEY | STATUS_VALUE |
+---------------------+--------------------------------------------------------------------+
| Component_name | component_keyring_oci |
| Author | Oracle Corporation |
| License | PROPRIETARY |
| Implementation_name | component_keyring_oci |
| Version | 1.0 |
| Component_status | Active |
| user | ocid1.user.oc1..aaaaaaaasqly<...> |
| tenancy | ocid1.tenancy.oc1..aaaaaaaai<...> |
| compartment | ocid1.compartment.oc1..aaaaaaaah2swh<...> |
| virtual_vault | ocid1.vault.oc1.iad.bbo5xyzkaaeuk.abuwcljtmvxp4r<...> |
| master_key | ocid1.key.oc1.iad.bbo5xyzkaaeuk.abuwcljrbsrewgap<...> |
| encryption_endpoint | bbo5xyzkaaeuk-crypto.kms.us-<...> |
| management_endpoint | bbo5xyzkaaeuk-management.kms.us-<...> |
| vaults_endpoint | vaults.us-<...> |
| secrets_endpoint | secrets.vaults.us-<...> |
| key_file | ~/.oci/oci_api_key.pem |
| key_fingerprint | ca:7c:e1:fa:86:b6:40:af:39:d6<...> |
| ca_certificate | disabled |
+---------------------+--------------------------------------------------------------------+
```

A Component\_status value of Active indicates that the component initialized successfully.

If the component cannot be loaded, server startup fails. Check the server error log for diagnostic messages. If the component loads but fails to initialize due to configuration problems, the server starts but the Component\_status value is Disabled. Check the server error log, correct the configuration issues, and use the ALTER INSTANCE RELOAD KEYRING statement to reload the configuration.

It is possible to query MySQL server for the list of existing keys. To see which keys exist, examine the Performance Schema keyring\_keys table.

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

## <span id="page-178-2"></span>**Vault Keyring Component Usage**

component\_keyring\_oci supports the functions that comprise the standard MySQL Keyring service interface. Keyring operations performed by those functions are accessible in SQL statements as described in [Section 8.4.4.15, "General-Purpose Keyring Key-Management Functions".](#page-189-0)

#### Example:

```
SELECT keyring_key_generate('MyKey', 'AES', 32);
SELECT keyring_key_remove('MyKey');
```

For information about the characteristics of key values permitted by component\_keyring\_oci, see [Section 8.4.4.13, "Supported Keyring Key Types and Lengths"](#page-181-0).

# <span id="page-178-0"></span>**8.4.4.12 Using the Oracle Cloud Infrastructure Vault Keyring Plugin**

![](_page_179_Picture_1.jpeg)

## **Note**

The keyring\_oci plugin is an extension included in MySQL Enterprise Edition, a commercial product. To learn more about commercial products, see <https://www.mysql.com/products/>.

The keyring\_oci plugin is a keyring plugin that communicates with Oracle Cloud Infrastructure Vault for back end storage. No key information is permanently stored in MySQL server local storage. All keys are stored in Oracle Cloud Infrastructure Vault, making this plugin well suited for Oracle Cloud Infrastructure MySQL customers for management of their MySQL Enterprise Edition keys.

As of MySQL 8.0.31, this plugin is deprecated and subject to removal in a future release of MySQL. Instead, consider using the component\_keyring\_oci component for storing keyring data (see [Section 8.4.4.11, "Using the Oracle Cloud Infrastructure Vault Keyring Component"](#page-174-0)).

The keyring\_oci plugin supports the functions that comprise the standard MySQL Keyring service interface. Keyring operations performed by those functions are accessible at two levels:

- SQL interface: In SQL statements, call the functions described in [Section 8.4.4.15, "General-Purpose](#page-189-0) [Keyring Key-Management Functions"](#page-189-0).
- C interface: In C-language code, call the keyring service functions described in Section 7.6.9.2, "The Keyring Service".

Example (using the SQL interface):

```
SELECT keyring_key_generate('MyKey', 'AES', 32);
SELECT keyring_key_remove('MyKey');
```

For information about the characteristics of key values permitted by keyring\_oci, see [Section 8.4.4.13, "Supported Keyring Key Types and Lengths"](#page-181-0).

To install keyring\_oci, use the general instructions found in [Section 8.4.4.3, "Keyring Plugin](#page-148-0) [Installation"](#page-148-0), together with the configuration information specific to keyring\_oci found here. Pluginspecific configuration involves setting a number of system variables to indicate the names or values of Oracle Cloud Infrastructure resources.

You are assumed to be familiar with Oracle Cloud Infrastructure concepts, but the following documentation may be helpful when setting up resources to be used by the keyring\_oci plugin:

- [Overview of Vault](https://docs.cloud.oracle.com/iaas/Content/KeyManagement/Concepts/keyoverview.md)
- [Resource Identifiers](https://docs.cloud.oracle.com/en-us/iaas/Content/General/Concepts/identifiers.md)
- [Required Keys and OCIDs](https://docs.cloud.oracle.com/en-us/iaas/Content/API/Concepts/apisigningkey.md)
- [Managing Keys](https://docs.cloud.oracle.com/en-us/iaas/Content/KeyManagement/Tasks/managingkeys.md)
- [Managing Compartments](https://docs.cloud.oracle.com/en-us/iaas/Content/Identity/Tasks/managingcompartments.md)
- [Managing Vaults](https://docs.cloud.oracle.com/en-us/iaas/Content/KeyManagement/Tasks/managingvaults.md)
- [Managing Secrets](https://docs.cloud.oracle.com/en-us/iaas/Content/KeyManagement/Tasks/managingsecrets.md)

The keyring\_oci plugin supports the configuration parameters shown in the following table. To specify these parameters, assign values to the corresponding system variables.

| Configuration Parameter | System Variable               | Mandatory |
|-------------------------|-------------------------------|-----------|
| User OCID               | keyring_oci_user              | Yes       |
| Tenancy OCID            | keyring_oci_tenancy           | Yes       |
| Compartment OCID        | keyring_oci_compartment       | Yes       |
| Vault OCID              | keyring_oci_virtual_vault Yes |           |

| Configuration Parameter           | System Variable                     | Mandatory |
|-----------------------------------|-------------------------------------|-----------|
| Master key OCID                   | keyring_oci_master_key              | Yes       |
| Encryption server endpoint        | keyring_oci_encryption_endpoint Yes |           |
| Key management server<br>endpoint | keyring_oci_management_endpoint Yes |           |
| Vaults server endpoint            | keyring_oci_vaults_endpointYes      |           |
| Secrets server endpoint           | keyring_oci_secrets_endpoint Yes    |           |
| RSA private key file              | keyring_oci_key_file                | Yes       |
| RSA private key fingerprint       | keyring_oci_key_fingerprintYes      |           |
| CA certificate bundle file        | keyring_oci_ca_certificateNo        |           |

To be usable during the server startup process, keyring\_oci must be loaded using the --earlyplugin-load option. As indicated by the preceding table, several plugin-related system variables are mandatory and must also be set:

- Oracle Cloud Infrastructure uses Oracle Cloud IDs (OCIDs) extensively to designate resources, and several keyring\_oci parameters specify OCID values of the resources to use. Consequently, prior to using the keyring\_oci plugin, these prerequisites must be satisfied:
  - A user for connecting to Oracle Cloud Infrastructure must exist. Create the user if necessary and assign the user OCID to the keyring\_oci\_user system variable.
  - The Oracle Cloud Infrastructure tenancy to be used must exist, as well as the MySQL compartment within the tenancy, and the vault within the compartment. Create these resources if necessary and make sure the user is enabled to use them. Assign the OCIDs for the tenancy, compartment and vault to the keyring\_oci\_tenancy, keyring\_oci\_compartment, and keyring\_oci\_virtual\_vault system variables.
  - A master key for encryption must exist. Create it if necessary and assign its OCID to the keyring\_oci\_master\_key system variable.
- Several server endpoints must be specified. These endpoints are vault specific and Oracle Cloud Infrastructure assigns them at vault-creation time. Obtain their values from the vault details page and assign them to the keyring\_oci\_encryption\_endpoint, keyring\_oci\_management\_endpoint, keyring\_oci\_vaults\_endpoint, and keyring\_oci\_secrets\_endpoint system variables.
- The Oracle Cloud Infrastructure API uses an RSA private/public key pair for authentication. To create this key pair and obtain the key fingerprint, use the instructions at [Required Keys and](https://docs.cloud.oracle.com/en-us/iaas/Content/API/Concepts/apisigningkey.md) [OCIDs](https://docs.cloud.oracle.com/en-us/iaas/Content/API/Concepts/apisigningkey.md). Assign the private key file name and key fingerprint to the keyring\_oci\_key\_file and keyring\_oci\_key\_fingerprint system variables.

In addition to the mandatory system variables, keyring\_oci\_ca\_certificate optionally may be set to specify a certificate authority (CA) certificate bundle file for peer authentication. On Windows systems, this variable should be set to disabled, or to the path to a CA certificate bundle file.

![](_page_180_Picture_10.jpeg)

#### **Important**

If you copy a parameter from the Oracle Cloud Infrastructure Console, the copied value may include an initial https:// part. Omit that part when setting the corresponding keyring\_oci system variable.

For example, to load and configure keyring\_oci, use these lines in the server my.cnf file (adjust the .so suffix and file location for your platform as necessary):

```
[mysqld]
early-plugin-load=keyring_oci.so
keyring_oci_user=ocid1.user.oc1..longAlphaNumericString
```

```
keyring_oci_tenancy=ocid1.tenancy.oc1..longAlphaNumericString
keyring_oci_compartment=ocid1.compartment.oc1..longAlphaNumericString
keyring_oci_virtual_vault=ocid1.vault.oc1.iad.shortAlphaNumericString.longAlphaNumericString
keyring_oci_master_key=ocid1.key.oc1.iad.shortAlphaNumericString.longAlphaNumericString
keyring_oci_encryption_endpoint=shortAlphaNumericString-crypto.kms.us-ashburn-1.oraclecloud.com
keyring_oci_management_endpoint=shortAlphaNumericString-management.kms.us-ashburn-1.oraclecloud.com
keyring_oci_vaults_endpoint=vaults.us-ashburn-1.oci.oraclecloud.com
keyring_oci_secrets_endpoint=secrets.vaults.us-ashburn-1.oci.oraclecloud.com
keyring_oci_key_file=file_name
keyring_oci_key_fingerprint=12:34:56:78:90:ab:cd:ef:12:34:56:78:90:ab:cd:ef
```

For additional information about the keyring\_oci plugin-specific system variables, see Section 8.4.4.19, "Keyring System Variables".

The keyring\_oci plugin does not support runtime reconfiguration and none of its system variables can be modified at runtime. To change configuration parameters, do this:

- Modify parameter settings in the my.cnf file, or use SET PERSIST\_ONLY for parameters that are persisted to mysqld-auto.conf.
- Restart the server.

# <span id="page-181-0"></span>**8.4.4.13 Supported Keyring Key Types and Lengths**

MySQL Keyring supports keys of different types (encryption algorithms) and lengths:

- The available key types depend on which keyring plugin is installed.
- The permitted key lengths are subject to multiple factors:
  - General keyring loadable-function interface limits (for keys managed using one of the keyring functions described in [Section 8.4.4.15, "General-Purpose Keyring Key-Management Functions"\)](#page-189-0), or limits from back end implementations. These length limits can vary by key operation type.
  - In addition to the general limits, individual keyring plugins may impose restrictions on key lengths per key type.

[Table 8.32, "General Keyring Key Length Limits"](#page-181-1) shows the general key-length limits. (The lower limits for keyring\_aws are imposed by the AWS KMS interface, not the keyring functions.) For keyring plugins, [Table 8.33, "Keyring Plugin Key Types and Lengths"](#page-181-2) shows the key types each keyring plugin permits, as well as any plugin-specific key-length restrictions. For most keyring components, the general key-length limits apply and there are no key-type restrictions.

![](_page_181_Picture_13.jpeg)

#### **Note**

component\_keyring\_oci (like the keyring\_oci plugin) can only generate keys of type AES with a size of 16, 24, or 32 bytes.

## **Table 8.32 General Keyring Key Length Limits**

<span id="page-181-1"></span>

| Key Operation | Maximum Key Length                                                   |
|---------------|----------------------------------------------------------------------|
| Generate key  | 16,384 bytes (2,048 prior to MySQL 8.0.18); 1,024<br>for keyring_aws |
| Store key     | 16,384 bytes (2,048 prior to MySQL 8.0.18); 4,096<br>for keyring_aws |
| Fetch key     | 16,384 bytes (2,048 prior to MySQL 8.0.18); 4,096<br>for keyring_aws |

## **Table 8.33 Keyring Plugin Key Types and Lengths**

<span id="page-181-2"></span>

| Plugin Name | Permitted Key Type | Plugin-Specific Length<br>Restrictions |
|-------------|--------------------|----------------------------------------|
| keyring_aws | AES                | 16, 24, or 32 bytes                    |

| Plugin Name            | Permitted Key Type | Plugin-Specific Length<br>Restrictions |
|------------------------|--------------------|----------------------------------------|
|                        | SECRET             | None                                   |
| keyring_encrypted_file | AES                | None                                   |
|                        | DSA                | None                                   |
|                        | RSA                | None                                   |
|                        | SECRET             | None                                   |
| keyring_file           | AES                | None                                   |
|                        | DSA                | None                                   |
|                        | RSA                | None                                   |
|                        | SECRET             | None                                   |
| keyring_hashicorp      | AES                | None                                   |
|                        | DSA                | None                                   |
|                        | RSA                | None                                   |
|                        | SECRET             | None                                   |
| keyring_oci            | AES                | 16, 24, or 32 bytes                    |
| keyring_okv            | AES                | 16, 24, or 32 bytes                    |
|                        | SECRET             | None                                   |

The SECRET key type, available as of MySQL 8.0.19, is intended for general-purpose storage of sensitive data using the MySQL keyring, and is supported by most keyring components and keyring plugins. The keyring encrypts and decrypts SECRET data as a byte stream upon storage and retrieval.

Example keyring operations involving the SECRET key type:

```
SELECT keyring_key_generate('MySecret1', 'SECRET', 20);
SELECT keyring_key_remove('MySecret1');
SELECT keyring_key_store('MySecret2', 'SECRET', 'MySecretData');
SELECT keyring_key_fetch('MySecret2');
SELECT keyring_key_length_fetch('MySecret2');
SELECT keyring_key_type_fetch('MySecret2');
SELECT keyring_key_remove('MySecret2');
```

# <span id="page-182-0"></span>**8.4.4.14 Migrating Keys Between Keyring Keystores**

A keyring migration copies keys from one keystore to another, enabling a DBA to switch a MySQL installation to a different keystore. A successful migration operation has this result:

- The destination keystore contains the keys it had prior to the migration, plus the keys from the source keystore.
- The source keystore remains the same before and after the migration (because keys are copied, not moved).

If a key to be copied already exists in the destination keystore, an error occurs and the destination keystore is restored to its premigration state.

The keyring manages keystores using keyring components and keyring plugins. This pertains to migration strategy because the way in which the source and destination keystores are managed determines whether a particular type of key migration is possible and the procedure for performing it:

- Migration from one keyring plugin to another: The MySQL server has an operational mode that provides this capability.
- Migration from a keyring plugin to a keyring component: The MySQL server has an operational mode that provides this capability as of MySQL 8.0.24.
- Migration from one keyring component to another: The mysql\_migrate\_keyring utility provides this capability. mysql\_migrate\_keyring is available as of MySQL 8.0.24.
- Migration from a keyring component to a keyring plugin: There is no provision for this capability.

The following sections discuss the characteristics of offline and online migrations and describe how to perform migrations.

- [Offline and Online Key Migrations](#page-183-0)
- [Key Migration Using a Migration Server](#page-184-0)
- [Key Migration Using the mysql\\_migrate\\_keyring Utility](#page-187-0)
- [Key Migration Involving Multiple Running Servers](#page-189-1)

## <span id="page-183-0"></span>**Offline and Online Key Migrations**

A key migration is either offline or online:

- Offline migration: For use when you are sure that no running server on the local host is using the source or destination keystore. In this case, the migration operation can copy keys from the source keystore to the destination without the possibility of a running server modifying keystore content during the operation.
- Online migration: For use when a running server on the local host is using the source keystore. In this case, care must be taken to prevent that server from updating keystores during the migration. This involves connecting to the running server and instructing it to pause keyring operations so that keys can be copied safely from the source keystore to the destination. When key copying is complete, the running server is permitted to resume keyring operations.

When you plan a key migration, use these points to decide whether it should be offline or online:

- Do not perform offline migration involving a keystore that is in use by a running server.
- Pausing keyring operations during an online migration is accomplished by connecting to the running server and setting its global keyring\_operations system variable to OFF before key copying and ON after key copying. This has several implications:
  - keyring\_operations was introduced in MySQL 5.7.21, so online migration is possible only if the running server is from MySQL 5.7.21 or higher. If the running server is older, you must stop it, perform an offline migration, and restart it. All migration instructions elsewhere that refer to keyring\_operations are subject to this condition.
  - The account used to connect to the running server must have the privileges required to modify keyring\_operations. These privileges are ENCRYPTION\_KEY\_ADMIN in addition to either SYSTEM\_VARIABLES\_ADMIN or the deprecated SUPER privilege.
  - If an online migration operation exits abnormally (for example, if it is forcibly terminated), it is possible for keyring\_operations to remain disabled on the running server, leaving it unable to perform keyring operations. In this case, it may be necessary to connect to the running server and enable keyring\_operations manually using this statement:

```
SET GLOBAL keyring_operations = ON;
```

• Online key migration provides for pausing keyring operations on a single running server. To perform a migration if multiple running servers are using the keystores involved, use the procedure described at [Key Migration Involving Multiple Running Servers.](#page-189-1)

## <span id="page-184-0"></span>**Key Migration Using a Migration Server**

![](_page_184_Picture_2.jpeg)

#### **Note**

Online key migration using a migration server is only supported if the running server allows socket connections or TCP/IP connections using TLS; it is not supported when, for example, the server is running on a Windows platform and only allows shared memory connections.

A MySQL server becomes a migration server if invoked in a special operational mode that supports key migration. A migration server does not accept client connections. Instead, it runs only long enough to migrate keys, then exits. A migration server reports errors to the console (the standard error output).

A migration server supports these migration types:

- Migration from one keyring plugin to another.
- Migration from a keyring plugin to a keyring component. This capability is available as of MySQL 8.0.24. Older servers support only migration from one keyring plugin to another, in which case the parts of these instructions that refer to keyring components do not apply.

A migration server does not support migration from one keyring component to another. For that type of migration, see [Key Migration Using the mysql\\_migrate\\_keyring Utility.](#page-187-0)

To perform a key migration operation using a migration server, determine the key migration options required to specify which keyring plugins or components are involved, and whether the migration is offline or online:

- To indicate the source keyring plugin and the destination keyring plugin or component, specify these options:
  - [--keyring-migration-source](#page-199-0): The source keyring plugin that manages the keys to be migrated.
  - [--keyring-migration-destination](#page-198-0): The destination keyring plugin or component to which the migrated keys are to be copied.
  - --keyring-migration-to-component: This option is required if the destination is a keyring component rather than a keyring plugin.

The [--keyring-migration-source](#page-199-0) and [--keyring-migration-destination](#page-198-0) options signify to the server that it should run in key migration mode. For key migration operations, both options are mandatory. Each plugin or component is specified using the name of its library file, including any platform-specific extension such as .so or .dll. The source and destination must differ, and the migration server must support them both.

- For an offline migration, no additional key migration options are needed.
- For an online migration, some running server currently is using the source or destination keystore. To invoke the migration server, specify additional key migration options that indicate how to connect to the running server. This is necessary so that the migration server can connect to the running server and tell it to pause keyring use during the migration operation.

Use of any of the following options signifies an online migration:

- [--keyring-migration-host](#page-198-1): The host where the running server is located. This is always the local host because the migration server can migrate keys only between keystores managed by local plugins and components.
- --keyring-migration-user, [--keyring-migration-password](#page-199-1): The account credentials to use to connect to the running server.

- [--keyring-migration-port](#page-199-2): For TCP/IP connections, the port number to connect to on the running server.
- [--keyring-migration-socket](#page-199-3): For Unix socket file or Windows named pipe connections, the socket file or named pipe to connect to on the running server.

For additional details about the key migration options, see [Section 8.4.4.18, "Keyring Command](#page-198-2) [Options".](#page-198-2)

Start the migration server with key migration options indicating the source and destination keystores and whether the migration is offline or online, possibly with other options. Keep the following considerations in mind:

- Other server options might be required, such as configuration parameters for the two keyring plugins. For example, if keyring\_file is the source or destination, you must set the keyring\_file\_data system variable if the keyring data file location is not the default location. Other non-keyring options may be required as well. One way to specify these options is by using --defaults-file to name an option file that contains the required options.
  - The migration server must not start up with its own keyring. This means that --defaults-file must not point to the same options file that is used to start the running server if it contains a line such as early-plugin-load=keyring\_file.so. Instead, it must point to a separate file that only contains options relevant to the migration.
  - If migrating from a plugin to a component:
    - The migration only works with a global component .cnf file. The migration does not work with a local config file and a global config file that attempts to read\_local\_config. If there are multiple instances running on the same machine, the global config file must be updated appropriately to migrate every individual key.
    - The component manifest file (mysqld.my) must not be present in the bin directory. However, the component configuration (for example, component\_keyring\_file.cnf) should be present in the plugin directory, so that the new keyring can be populated. After the migration is complete, add the manifest file to the directory and restart the MySQL server, so that the server starts using the new keyring.
- The migration server expects path name option values to be full paths. Relative path names may not be resolved as you expect.
- The user who invokes a server in key-migration mode must not be the root operating system user, unless the --user option is specified with a non-root user name to run the server as that user.
- The user a server in key-migration mode runs as must have permission to read and write any local keyring files, such as the data file for a file-based plugin.

If you invoke the migration server from a system account different from that normally used to run MySQL, it might create keyring directories or files that are inaccessible to the server during normal operation. Suppose that mysqld normally runs as the mysql operating system user, but you invoke the migration server while logged in as isabel. Any new directories or files created by the migration server are owned by isabel. Subsequent startup fails when a server run as the mysql operating system user attempts to access file system objects owned by isabel.

To avoid this issue, start the migration server as the root operating system user and provide a - user=user\_name option, where user\_name is the system account normally used to run MySQL. Alternatively, after the migration, examine the keyring-related file system objects and change their ownership and permissions if necessary using chown, chmod, or similar commands, so that the objects are accessible to the running server.

Example command line for offline migration between two keyring plugins (enter the command on a single line):

```
mysqld --defaults-file=/usr/local/mysql/etc/my.cnf
 --keyring-migration-source=keyring_file.so
 --keyring-migration-destination=keyring_encrypted_file.so
 --keyring_encrypted_file_password=password
```

Example command line for online migration between two keyring plugins:

```
mysqld --defaults-file=/usr/local/mysql/etc/my.cnf
 --keyring-migration-source=keyring_file.so
 --keyring-migration-destination=keyring_encrypted_file.so
 --keyring_encrypted_file_password=password
 --keyring-migration-host=127.0.0.1
 --keyring-migration-user=root
 --keyring-migration-password=root_password
```

To perform a migration when the destination is a keyring component rather than a keyring plugin, specify the --keyring-migration-to-component option, and name the component as the value of the [--keyring-migration-destination](#page-198-0) option.

Example command line for offline migration from a keyring plugin to a keyring component:

```
mysqld --defaults-file=/usr/local/mysql/etc/my.cnf
 --keyring-migration-to-component
 --keyring-migration-source=keyring_file.so
 --keyring-migration-destination=component_keyring_encrypted_file.so
```

Notice that in this case, no keyring\_encrypted\_file\_password value is specified. The password for the component data file is listed in the component configuration file.

Example command line for online migration from a keyring plugin to a keyring component:

```
mysqld --defaults-file=/usr/local/mysql/etc/my.cnf
 --keyring-migration-to-component
 --keyring-migration-source=keyring_file.so
 --keyring-migration-destination=component_keyring_encrypted_file.so
 --keyring-migration-host=127.0.0.1
 --keyring-migration-user=root
 --keyring-migration-password=root_password
```

The key migration server performs a migration operation as follows:

- 1. (Online migration only) Connect to the running server using the connection options.
- 2. (Online migration only) Disable keyring\_operations on the running server.
- 3. Load the keyring plugin/component libraries for the source and destination keystores.
- 4. Copy keys from the source keystore to the destination.
- 5. Unload the keyring plugin/component libraries for the source and destination keystores.
- 6. (Online migration only) Enable keyring\_operations on the running server.
- 7. (Online migration only) Disconnect from the running server.

If an error occurs during key migration, the destination keystore is restored to its premigration state.

After a successful online key migration operation, the running server might need to be restarted:

- If the running server was using the source keystore before the migration and should continue to use it after the migration, it need not be restarted after the migration.
- If the running server was using the destination keystore before the migration and should continue to use it after the migration, it should be restarted after the migration to load all keys migrated into the destination keystore.

• If the running server was using the source keystore before the migration but should use the destination keystore after the migration, it must be reconfigured to use the destination keystore and restarted. In this case, be aware that although the running server is paused from modifying the source keystore during the migration itself, it is not paused during the interval between the migration and the subsequent restart. Care should be taken that the server does not modify the source keystore during this interval because any such changes will not be reflected in the destination keystore.

## <span id="page-187-0"></span>**Key Migration Using the mysql\_migrate\_keyring Utility**

The mysql\_migrate\_keyring utility migrates keys from one keyring component to another. It does not support migrations involving keyring plugins. For that type of migration, use a MySQL server operating in key migration mode; see [Key Migration Using a Migration Server.](#page-184-0)

To perform a key migration operation using mysql\_migrate\_keyring, determine the key migration options required to specify which keyring components are involved, and whether the migration is offline or online:

- To indicate the source and destination keyring components and their location, specify these options:
  - --source-keyring: The source keyring component that manages the keys to be migrated.
  - --destination-keyring: The destination keyring component to which the migrated keys are to be copied.
  - --component-dir: The directory containing keyring component library files. This is typically the value of the plugin\_dir system variable for the local MySQL server.

All three options are mandatory. Each keyring component name is a component library file name specified without any platform-specific extension such as .so or .dll. For example, to use the component for which the library file is component\_keyring\_file.so, specify the option as - source-keyring=component\_keyring\_file. The source and destination must differ, and mysql\_migrate\_keyring must support them both.

- For an offline migration, no additional options are needed.
- For an online migration, some running server currently is using the source or destination keystore. In this case, specify the --online-migration option to signify an online migration. In addition, specify connection options indicating how to connect to the running server, so that mysql\_migrate\_keyring can connect to it and tell it to pause keyring use during the migration operation.

The --online-migration option is commonly used in conjunction with connection options such as these:

- --host: The host where the running server is located. This is always the local host because mysql\_migrate\_keyring can migrate keys only between keystores managed by local components.
- --user, --password: The account credentials to use to connect to the running server.
- --port: For TCP/IP connections, the port number to connect to on the running server.
- --socket: For Unix socket file or Windows named pipe connections, the socket file or named pipe to connect to on the running server.

For descriptions of all available options, see Section 6.6.8, "mysql\_migrate\_keyring — Keyring Key Migration Utility".

Start mysql\_migrate\_keyring with options indicating the source and destination keystores and whether the migration is offline or online, possibly with other options. Keep the following considerations in mind:

- The user who invokes mysql\_migrate\_keyring must not be the root operating system user.
- The user who invokes mysql\_migrate\_keyring must have permission to read and write any local keyring files, such as the data file for a file-based plugin.

If you invoke mysql\_migrate\_keyring from a system account different from that normally used to run MySQL, it might create keyring directories or files that are inaccessible to the server during normal operation. Suppose that mysqld normally runs as the mysql operating system user, but you invoke mysql\_migrate\_keyring while logged in as isabel. Any new directories or files created by mysql\_migrate\_keyring are owned by isabel. Subsequent startup fails when a server run as the mysql operating system user attempts to access file system objects owned by isabel.

To avoid this issue, invoke mysql\_migrate\_keyring as the mysql operating system user. Alternatively, after the migration, examine the keyring-related file system objects and change their ownership and permissions if necessary using chown, chmod, or similar commands, so that the objects are accessible to the running server.

Suppose that you want to migrate keys from component\_keyring\_file to component\_keyring\_encrypted\_file, and that the local server stores its keyring component library files in /usr/local/mysql/lib/plugin.

If no running server is using the keyring, an offline migration is permitted. Invoke mysql\_migrate\_keyring like this (enter the command on a single line):

```
mysql_migrate_keyring
 --component-dir=/usr/local/mysql/lib/plugin
 --source-keyring=component_keyring_file
 --destination-keyring=component_keyring_encrypted_file
```

If a running server is using the keyring, you must perform an online migration instead. In this case, the --online-migration option must be given, along with any connection options required to specify which server to connect to and the MySQL account to use.

The following command performs an online migration. It connects to the local server using a TCP/IP connection and the admin account. The command prompts for a password, which you should enter when prompted:

```
mysql_migrate_keyring
 --component-dir=/usr/local/mysql/lib/plugin
 --source-keyring=component_keyring_file
 --destination-keyring=component_keyring_encrypted_file
 --online-migration --host=127.0.0.1 --user=admin --password
```

mysql\_migrate\_keyring performs a migration operation as follows:

- 1. (Online migration only) Connect to the running server using the connection options.
- 2. (Online migration only) Disable keyring\_operations on the running server.
- 3. Load the keyring component libraries for the source and destination keystores.
- 4. Copy keys from the source keystore to the destination.
- 5. Unload the keyring component libraries for the source and destination keystores.
- 6. (Online migration only) Enable keyring\_operations on the running server.
- 7. (Online migration only) Disconnect from the running server.

If an error occurs during key migration, the destination keystore is restored to its premigration state.

After a successful online key migration operation, the running server might need to be restarted:

• If the running server was using the source keystore before the migration and should continue to use it after the migration, it need not be restarted after the migration.

- If the running server was using the destination keystore before the migration and should continue to use it after the migration, it should be restarted after the migration to load all keys migrated into the destination keystore.
- If the running server was using the source keystore before the migration but should use the destination keystore after the migration, it must be reconfigured to use the destination keystore and restarted. In this case, be aware that although the running server is paused from modifying the source keystore during the migration itself, it is not paused during the interval between the migration and the subsequent restart. Care should be taken that the server does not modify the source keystore during this interval because any such changes will not be reflected in the destination keystore.

## <span id="page-189-1"></span>**Key Migration Involving Multiple Running Servers**

Online key migration provides for pausing keyring operations on a single running server. To perform a migration if multiple running servers are using the keystores involved, use this procedure:

- 1. Connect to each running server manually and set keyring\_operations=OFF. This ensures that no running server is using the source or destination keystore and satisfies the required condition for offline migration.
- 2. Use a migration server or mysql\_migrate\_keyring to perform an offline key migration for each paused server.
- 3. Connect to each running server manually and set keyring\_operations=ON.

All running servers must support the keyring\_operations system variable. Any server that does not must be stopped before the migration and restarted after.

# <span id="page-189-0"></span>**8.4.4.15 General-Purpose Keyring Key-Management Functions**

MySQL Server supports a keyring service that enables internal components and plugins to store sensitive information securely for later retrieval.

MySQL Server also includes an SQL interface for keyring key management, implemented as a set of general-purpose functions that access the capabilities provided by the internal keyring service. The keyring functions are contained in a plugin library file, which also contains a keyring\_udf plugin that must be enabled prior to function invocation. For these functions to be used, a keyring plugin such as keyring\_file or keyring\_okv, or a keyring component such as component\_keyring\_file or component\_keyring\_encrypted\_file, must be enabled.

The functions described here are general-purpose and intended for use with any keyring component or plugin. A given keyring component or plugin may also provide functions of its own that are intended for use only with that component or plugin; see [Section 8.4.4.16, "Plugin-Specific Keyring Key-](#page-196-1)[Management Functions".](#page-196-1)

The following sections provide installation instructions for the keyring functions and demonstrate how to use them. For information about the keyring service functions invoked by these functions, see Section 7.6.9.2, "The Keyring Service". For general keyring information, see [Section 8.4.4, "The](#page-143-0) [MySQL Keyring"](#page-143-0).

- [Installing or Uninstalling General-Purpose Keyring Functions](#page-189-2)
- [Using General-Purpose Keyring Functions](#page-190-0)
- [General-Purpose Keyring Function Reference](#page-194-0)

## <span id="page-189-2"></span>**Installing or Uninstalling General-Purpose Keyring Functions**

This section describes how to install or uninstall the keyring functions, which are implemented in a plugin library file that also contains a keyring\_udf plugin. For general information about installing or uninstalling plugins and loadable functions, see Section 7.6.1, "Installing and Uninstalling Plugins", and Section 7.7.1, "Installing and Uninstalling Loadable Functions".

The keyring functions enable keyring key management operations, but the keyring\_udf plugin must also be installed because the functions do not work correctly without it. Attempts to use the functions without the keyring\_udf plugin result in an error.

To be usable by the server, the plugin library file must be located in the MySQL plugin directory (the directory named by the plugin\_dir system variable). If necessary, configure the plugin directory location by setting the value of plugin\_dir at server startup.

The plugin library file base name is keyring\_udf. The file name suffix differs per platform (for example, .so for Unix and Unix-like systems, .dll for Windows).

To install the keyring\_udf plugin and the keyring functions, use the INSTALL PLUGIN and CREATE FUNCTION statements, adjusting the .so suffix for your platform as necessary:

```
INSTALL PLUGIN keyring_udf SONAME 'keyring_udf.so';
CREATE FUNCTION keyring_key_generate RETURNS INTEGER
 SONAME 'keyring_udf.so';
CREATE FUNCTION keyring_key_fetch RETURNS STRING
 SONAME 'keyring_udf.so';
CREATE FUNCTION keyring_key_length_fetch RETURNS INTEGER
 SONAME 'keyring_udf.so';
CREATE FUNCTION keyring_key_type_fetch RETURNS STRING
 SONAME 'keyring_udf.so';
CREATE FUNCTION keyring_key_store RETURNS INTEGER
 SONAME 'keyring_udf.so';
CREATE FUNCTION keyring_key_remove RETURNS INTEGER
 SONAME 'keyring_udf.so';
```

If the plugin and functions are used on a source replication server, install them on all replicas as well to avoid replication issues.

Once installed as just described, the plugin and functions remain installed until uninstalled. To remove them, use the UNINSTALL PLUGIN and DROP FUNCTION statements:

```
UNINSTALL PLUGIN keyring_udf;
DROP FUNCTION keyring_key_generate;
DROP FUNCTION keyring_key_fetch;
DROP FUNCTION keyring_key_length_fetch;
DROP FUNCTION keyring_key_type_fetch;
DROP FUNCTION keyring_key_store;
DROP FUNCTION keyring_key_remove;
```

## <span id="page-190-0"></span>**Using General-Purpose Keyring Functions**

Before using the keyring general-purpose functions, install them according to the instructions provided in [Installing or Uninstalling General-Purpose Keyring Functions.](#page-189-2)

The keyring functions are subject to these constraints:

• To use any keyring function, the keyring\_udf plugin must be enabled. Otherwise, an error occurs:

```
ERROR 1123 (HY000): Can't initialize function 'keyring_key_generate';
This function requires keyring_udf plugin which is not installed.
Please install
```

To install the keyring\_udf plugin, see [Installing or Uninstalling General-Purpose Keyring](#page-189-2) [Functions](#page-189-2).

• The keyring functions invoke keyring service functions (see Section 7.6.9.2, "The Keyring Service"). The service functions in turn use whatever keyring plugin is installed (for example, keyring\_file or keyring\_okv). Therefore, to use any keyring function, some underlying keyring plugin must be enabled. Otherwise, an error occurs:

```
ERROR 3188 (HY000): Function 'keyring_key_generate' failed because
underlying keyring service returned an error. Please check if a
keyring plugin is installed and that provided arguments are valid
for the keyring you are using.
```

To install a keyring plugin, see [Section 8.4.4.3, "Keyring Plugin Installation"](#page-148-0).

• A user must possess the global EXECUTE privilege to use any keyring function. Otherwise, an error occurs:

```
ERROR 1123 (HY000): Can't initialize function 'keyring_key_generate';
The user is not privileged to execute this function. User needs to
have EXECUTE
```

To grant the global EXECUTE privilege to a user, use this statement:

```
GRANT EXECUTE ON *.* TO user;
```

Alternatively, should you prefer to avoid granting the global EXECUTE privilege while still permitting users to access specific key-management operations, "wrapper" stored programs can be defined (a technique described later in this section).

• A key stored in the keyring by a given user can be manipulated later only by the same user. That is, the value of the CURRENT\_USER() function at the time of key manipulation must have the same value as when the key was stored in the keyring. (This constraint rules out the use of the keyring functions for manipulation of instance-wide keys, such as those created by InnoDB to support tablespace encryption.)

To enable multiple users to perform operations on the same key, "wrapper" stored programs can be defined (a technique described later in this section).

• Keyring functions support the key types and lengths supported by the underlying keyring plugin. For information about keys specific to a particular keyring plugin, see [Section 8.4.4.13, "Supported](#page-181-0) [Keyring Key Types and Lengths"](#page-181-0).

To create a new random key and store it in the keyring, call [keyring\\_key\\_generate\(\)](#page-194-1), passing to it an ID for the key, along with the key type (encryption method) and its length in bytes. The following call creates a 2,048-bit DSA-encrypted key named MyKey:

```
mysql> SELECT keyring_key_generate('MyKey', 'DSA', 256);
+-------------------------------------------+
| keyring_key_generate('MyKey', 'DSA', 256) |
+-------------------------------------------+
| 1 |
+-------------------------------------------+
```

A return value of 1 indicates success. If the key cannot be created, the return value is NULL and an error occurs. One reason this might be is that the underlying keyring plugin does not support the specified combination of key type and key length; see [Section 8.4.4.13, "Supported Keyring Key Types](#page-181-0) [and Lengths"](#page-181-0).

To be able to check the return type regardless of whether an error occurs, use SELECT ... INTO @var\_name and test the variable value:

```
mysql> SELECT keyring_key_generate('', '', -1) INTO @x;
ERROR 3188 (HY000): Function 'keyring_key_generate' failed because
underlying keyring service returned an error. Please check if a
keyring plugin is installed and that provided arguments are valid
for the keyring you are using.
mysql> SELECT @x;
+------+
| @x |
+------+
| NULL |
+------+
```

```
mysql> SELECT keyring_key_generate('x', 'AES', 16) INTO @x;
mysql> SELECT @x;
+------+
| @x |
+------+
| 1 |
+------+
```

This technique also applies to other keyring functions that for failure return a value and an error.

The ID passed to [keyring\\_key\\_generate\(\)](#page-194-1) provides a means by which to refer to the key in subsequent functions calls. For example, use the key ID to retrieve its type as a string or its length in bytes as an integer:

```
mysql> SELECT keyring_key_type_fetch('MyKey');
+---------------------------------+
| keyring_key_type_fetch('MyKey') |
+---------------------------------+
| DSA |
+---------------------------------+
mysql> SELECT keyring_key_length_fetch('MyKey');
+-----------------------------------+
| keyring_key_length_fetch('MyKey') |
+-----------------------------------+
| 256 |
+-----------------------------------+
```

To retrieve a key value, pass the key ID to [keyring\\_key\\_fetch\(\)](#page-194-2). The following example uses HEX() to display the key value because it may contain nonprintable characters. The example also uses a short key for brevity, but be aware that longer keys provide better security:

```
mysql> SELECT keyring_key_generate('MyShortKey', 'DSA', 8);
+----------------------------------------------+
| keyring_key_generate('MyShortKey', 'DSA', 8) |
+----------------------------------------------+
| 1 |
+----------------------------------------------+
mysql> SELECT HEX(keyring_key_fetch('MyShortKey'));
+--------------------------------------+
| HEX(keyring_key_fetch('MyShortKey')) |
+--------------------------------------+
| 1DB3B0FC3328A24C |
+--------------------------------------+
```

Keyring functions treat key IDs, types, and values as binary strings, so comparisons are case-sensitive. For example, IDs of MyKey and mykey refer to different keys.

To remove a key, pass the key ID to [keyring\\_key\\_remove\(\)](#page-195-0):

```
mysql> SELECT keyring_key_remove('MyKey');
+-----------------------------+
| keyring_key_remove('MyKey') |
+-----------------------------+
| 1 |
+-----------------------------+
```

To obfuscate and store a key that you provide, pass the key ID, type, and value to [keyring\\_key\\_store\(\)](#page-196-2):

```
mysql> SELECT keyring_key_store('AES_key', 'AES', 'Secret string');
+------------------------------------------------------+
| keyring_key_store('AES_key', 'AES', 'Secret string') |
+------------------------------------------------------+
| 1 |
+------------------------------------------------------+
```

As indicated previously, a user must have the global EXECUTE privilege to call keyring functions, and the user who stores a key in the keyring initially must be the same user who performs subsequent operations on the key later, as determined from the CURRENT\_USER() value in effect for each function call. To permit key operations to users who do not have the global EXECUTE privilege or who may not be the key "owner," use this technique:

- 1. Define "wrapper" stored programs that encapsulate the required key operations and have a DEFINER value equal to the key owner.
- 2. Grant the EXECUTE privilege for specific stored programs to the individual users who should be able to invoke them.
- 3. If the operations implemented by the wrapper stored programs do not include key creation, create any necessary keys in advance, using the account named as the DEFINER in the stored program definitions.

This technique enables keys to be shared among users and provides to DBAs more fine-grained control over who can do what with keys, without having to grant global privileges.

The following example shows how to set up a shared key named SharedKey that is owned by the DBA, and a get\_shared\_key() stored function that provides access to the current key value. The value can be retrieved by any user with the EXECUTE privilege for that function, which is created in the key\_schema schema.

From a MySQL administrative account ('root'@'localhost' in this example), create the administrative schema and the stored function to access the key:

```
mysql> CREATE SCHEMA key_schema;
mysql> CREATE DEFINER = 'root'@'localhost'
 FUNCTION key_schema.get_shared_key()
 RETURNS BLOB READS SQL DATA
 RETURN keyring_key_fetch('SharedKey');
```

From the administrative account, ensure that the shared key exists:

```
mysql> SELECT keyring_key_generate('SharedKey', 'DSA', 8);
+---------------------------------------------+
| keyring_key_generate('SharedKey', 'DSA', 8) |
+---------------------------------------------+
| 1 |
+---------------------------------------------+
```

From the administrative account, create an ordinary user account to which key access is to be granted:

```
mysql> CREATE USER 'key_user'@'localhost'
 IDENTIFIED BY 'key_user_pwd';
```

From the key\_user account, verify that, without the proper EXECUTE privilege, the new account cannot access the shared key:

```
mysql> SELECT HEX(key_schema.get_shared_key());
ERROR 1370 (42000): execute command denied to user 'key_user'@'localhost'
for routine 'key_schema.get_shared_key'
```

From the administrative account, grant EXECUTE to key\_user for the stored function:

```
mysql> GRANT EXECUTE ON FUNCTION key_schema.get_shared_key
 TO 'key_user'@'localhost';
```

From the key\_user account, verify that the key is now accessible:

```
mysql> SELECT HEX(key_schema.get_shared_key());
+----------------------------------+
| HEX(key_schema.get_shared_key()) |
+----------------------------------+
| 9BAFB9E75CEEB013 |
```

+----------------------------------+

## <span id="page-194-0"></span>**General-Purpose Keyring Function Reference**

For each general-purpose keyring function, this section describes its purpose, calling sequence, and return value. For information about the conditions under which these functions can be invoked, see [Using General-Purpose Keyring Functions](#page-190-0).

<span id="page-194-2"></span>• [keyring\\_key\\_fetch\(](#page-194-2)key\_id)

Given a key ID, deobfuscates and returns the key value.

#### Arguments:

• key\_id: A string that specifies the key ID.

## Return value:

Returns the key value as a string for success, NULL if the key does not exist, or NULL and an error for failure.

![](_page_194_Picture_10.jpeg)

#### **Note**

Key values retrieved using [keyring\\_key\\_fetch\(\)](#page-194-2) are subject to the general keyring function limits described in [Section 8.4.4.13, "Supported](#page-181-0) [Keyring Key Types and Lengths"](#page-181-0). A key value longer than that length can be stored using a keyring service function (see Section 7.6.9.2, "The Keyring Service"), but if retrieved using [keyring\\_key\\_fetch\(\)](#page-194-2) is truncated to the general keyring function limit.

#### Example:

```
mysql> SELECT keyring_key_generate('RSA_key', 'RSA', 16);
+--------------------------------------------+
| keyring_key_generate('RSA_key', 'RSA', 16) |
+--------------------------------------------+
| 1 |
+--------------------------------------------+
mysql> SELECT HEX(keyring_key_fetch('RSA_key'));
+-----------------------------------+
| HEX(keyring_key_fetch('RSA_key')) |
+-----------------------------------+
| 91C2253B696064D3556984B6630F891A |
+-----------------------------------+
mysql> SELECT keyring_key_type_fetch('RSA_key');
+-----------------------------------+
| keyring_key_type_fetch('RSA_key') |
+-----------------------------------+
| RSA |
+-----------------------------------+
mysql> SELECT keyring_key_length_fetch('RSA_key');
+-------------------------------------+
| keyring_key_length_fetch('RSA_key') |
+-------------------------------------+
| 16 |
+-------------------------------------+
```

The example uses HEX() to display the key value because it may contain nonprintable characters. The example also uses a short key for brevity, but be aware that longer keys provide better security.

<span id="page-194-1"></span>• [keyring\\_key\\_generate\(](#page-194-1)key\_id, key\_type, key\_length)

Generates a new random key with a given ID, type, and length, and stores it in the keyring. The type and length values must be consistent with the values supported by the underlying keyring plugin. See [Section 8.4.4.13, "Supported Keyring Key Types and Lengths".](#page-181-0)

## Arguments:

- key\_id: A string that specifies the key ID.
- key\_type: A string that specifies the key type.
- key\_length: An integer that specifies the key length in bytes.

#### Return value:

Returns 1 for success, or NULL and an error for failure.

#### Example:

```
mysql> SELECT keyring_key_generate('RSA_key', 'RSA', 384);
+---------------------------------------------+
| keyring_key_generate('RSA_key', 'RSA', 384) |
+---------------------------------------------+
| 1 |
+---------------------------------------------+
```

<span id="page-195-1"></span>• [keyring\\_key\\_length\\_fetch\(](#page-195-1)key\_id)

Given a key ID, returns the key length.

## Arguments:

• key\_id: A string that specifies the key ID.

#### Return value:

Returns the key length in bytes as an integer for success, NULL if the key does not exist, or NULL and an error for failure.

#### Example:

See the description of [keyring\\_key\\_fetch\(\)](#page-194-2).

<span id="page-195-0"></span>• [keyring\\_key\\_remove\(](#page-195-0)key\_id)

Removes the key with a given ID from the keyring.

## Arguments:

• key\_id: A string that specifies the key ID.

## Return value:

Returns 1 for success, or NULL for failure.

#### Example:

```
mysql> SELECT keyring_key_remove('AES_key');
+-------------------------------+
| keyring_key_remove('AES_key') |
+-------------------------------+
| 1 |
+-------------------------------+
```

<span id="page-196-2"></span>• [keyring\\_key\\_store\(](#page-196-2)key\_id, key\_type, key)

Obfuscates and stores a key in the keyring.

#### Arguments:

- key\_id: A string that specifies the key ID.
- key\_type: A string that specifies the key type.
- key: A string that specifies the key value.

#### Return value:

Returns 1 for success, or NULL and an error for failure.

#### Example:

```
mysql> SELECT keyring_key_store('new key', 'DSA', 'My key value');
+-----------------------------------------------------+
| keyring_key_store('new key', 'DSA', 'My key value') |
+-----------------------------------------------------+
| 1 |
+-----------------------------------------------------+
```

<span id="page-196-3"></span>• [keyring\\_key\\_type\\_fetch\(](#page-196-3)key\_id)

Given a key ID, returns the key type.

#### Arguments:

• key\_id: A string that specifies the key ID.

### Return value:

Returns the key type as a string for success, NULL if the key does not exist, or NULL and an error for failure.

## Example:

See the description of [keyring\\_key\\_fetch\(\)](#page-194-2).

# <span id="page-196-1"></span>**8.4.4.16 Plugin-Specific Keyring Key-Management Functions**

For each keyring plugin-specific function, this section describes its purpose, calling sequence, and return value. For information about general-purpose keyring functions, see [Section 8.4.4.15, "General-](#page-189-0)[Purpose Keyring Key-Management Functions"](#page-189-0).

<span id="page-196-0"></span>• [keyring\\_aws\\_rotate\\_cmk\(\)](#page-196-0)

Associated keyring plugin: keyring\_aws

[keyring\\_aws\\_rotate\\_cmk\(\)](#page-196-0) rotates the AWS KMS key. Rotation changes only the key that AWS KMS uses for subsequent data key-encryption operations. AWS KMS maintains previous CMK versions, so keys generated using previous CMKs remain decryptable after rotation.

Rotation changes the CMK value used inside AWS KMS but does not change the ID used to refer to it, so there is no need to change the keyring\_aws\_cmk\_id system variable after calling [keyring\\_aws\\_rotate\\_cmk\(\)](#page-196-0).

This function requires the SUPER privilege.

Arguments: 1567

None.

Return value:

Returns 1 for success, or NULL and an error for failure.

<span id="page-197-0"></span>• [keyring\\_aws\\_rotate\\_keys\(\)](#page-197-0)

Associated keyring plugin: keyring\_aws

[keyring\\_aws\\_rotate\\_keys\(\)](#page-197-0) rotates keys stored in the keyring\_aws storage file named by the keyring\_aws\_data\_file system variable. Rotation sends each key stored in the file to AWS KMS for re-encryption using the value of the keyring\_aws\_cmk\_id system variable as the CMK value, and stores the new encrypted keys in the file.

[keyring\\_aws\\_rotate\\_keys\(\)](#page-197-0) is useful for key re-encryption under these circumstances:

- After rotating the CMK; that is, after invoking the [keyring\\_aws\\_rotate\\_cmk\(\)](#page-196-0) function.
- After changing the keyring\_aws\_cmk\_id system variable to a different key value.

This function requires the SUPER privilege.

Arguments:

None.

Return value:

Returns 1 for success, or NULL and an error for failure.

<span id="page-197-1"></span>• [keyring\\_hashicorp\\_update\\_config\(\)](#page-197-1)

Associated keyring plugin: keyring\_hashicorp

When invoked, the [keyring\\_hashicorp\\_update\\_config\(\)](#page-197-1) function causes keyring\_hashicorp to perform a runtime reconfiguration, as described in [keyring\\_hashicorp](#page-172-0) [Configuration](#page-172-0).

This function requires the SYSTEM\_VARIABLES\_ADMIN privilege because it modifies global system variables.

Arguments:

None.

Return value:

Returns the string 'Configuration update was successful.' for success, or 'Configuration update failed.' for failure.