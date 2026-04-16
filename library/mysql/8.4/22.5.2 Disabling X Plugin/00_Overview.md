---
source: MySQL 8.4 Reference
title: 00_Overview
---

The X Plugin can be disabled at startup by either setting [mysqlx=0](#page-26-0) in your MySQL configuration file, or by passing in either [--mysqlx=0](#page-26-0) or [--skip-mysqlx](#page-26-0) when starting the MySQL server.

Alternatively, use the -DWITH\_MYSQLX=OFF CMake option to compile MySQL Server without X Plugin.

# <span id="page-18-0"></span>**22.5.3 Using Encrypted Connections with X Plugin**

This section explains how to configure X Plugin to use encrypted connections. For more background information, see Section 8.3, "Using Encrypted Connections".

To enable configuring support for encrypted connections, X Plugin has mysqlx\_ssl\_xxx system variables, which can have different values from the ssl\_xxx system variables used with MySQL Server. For example, X Plugin can have SSL key, certificate, and certificate authority files that differ from those used for MySQL Server. These variables are described at [Section 22.5.6.2, "X](#page-26-1) [Plugin Options and System Variables"](#page-26-1). Similarly, X Plugin has its own Mysqlx\_ssl\_xxx status variables that correspond to the MySQL Server encrypted-connection Ssl\_xxx status variables. See [Section 22.5.6.3, "X Plugin Status Variables"](#page-38-0).

At initialization, X Plugin determines its TLS context for encrypted connections as follows:

- If all mysqlx\_ssl\_xxx system variables have their default values, X Plugin uses the same TLS context as the MySQL Server main connection interface, which is determined by the values of the ssl\_xxx system variables.
- If any mysqlx\_ssl\_xxx variable has a nondefault value, X Plugin uses the TLS context defined by the values of its own system variables. (This is the case if any mysqlx\_ssl\_xxx system variable is set to a value different from its default.)

This means that, on a server with X Plugin enabled, you can choose to have MySQL Protocol and X Protocol connections share the same encryption configuration by setting only the ssl\_xxx variables, or have separate encryption configurations for MySQL Protocol and X Protocol connections by configuring the ssl\_xxx and mysqlx\_ssl\_xxx variables separately.

To have MySQL Protocol and X Protocol connections use the same encryption configuration, set only the ssl\_xxx system variables in my.cnf:

```
[mysqld]
ssl_ca=ca.pem
ssl_cert=server-cert.pem
ssl_key=server-key.pem
```

To configure encryption separately for MySQL Protocol and X Protocol connections, set both the ssl\_xxx and mysqlx\_ssl\_xxx system variables in my.cnf:

```
[mysqld]
ssl_ca=ca1.pem
ssl_cert=server-cert1.pem
ssl_key=server-key1.pem
mysqlx_ssl_ca=ca2.pem
mysqlx_ssl_cert=server-cert2.pem
mysqlx_ssl_key=server-key2.pem
```

For general information about configuring connection-encryption support, see Section 8.3.1, "Configuring MySQL to Use Encrypted Connections". That discussion is written for MySQL Server, but the parameter names are similar for X Plugin. (The X Plugin mysqlx\_ssl\_xxx system variable names correspond to the MySQL Server ssl\_xxx system variable names.)

The tls\_version system variable that determines the permitted TLS versions for MySQL Protocol connections also applies to X Protocol connections. The permitted TLS versions for both types of connections are therefore the same.

Encryption per connection is optional, but a specific user can be required to use encryption for X Protocol and MySQL Protocol connections by including an appropriate REQUIRE clause in the CREATE USER statement that creates the user. For details, see Section 15.7.1.3, "CREATE USER Statement". Alternatively, to require all users to use encryption for X Protocol and MySQL Protocol connections, enable the require\_secure\_transport system variable. For additional information, see Configuring Encrypted Connections as Mandatory.