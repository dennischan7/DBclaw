---
source: MySQL 8.4 Reference
title: 00_Overview
---

Database administrators should use the following guidelines to keep passwords secure.

MySQL stores passwords for user accounts in the mysql.user system table. Access to this table should never be granted to any nonadministrative accounts.

Account passwords can be expired so that users must reset them. See Section 8.2.15, "Password Management", and Section 8.2.16, "Server Handling of Expired Passwords".

The validate\_password plugin can be used to enforce a policy on acceptable password. See Section 8.4.3, "The Password Validation Component".

A user who has access to modify the plugin directory (the value of the plugin\_dir system variable) or the my.cnf file that specifies the plugin directory location can replace plugins and modify the capabilities provided by plugins, including authentication plugins.

Files such as log files to which passwords might be written should be protected. See [Section 8.1.2.3,](#page-159-0) ["Passwords and Logging"](#page-159-0).

# <span id="page-159-0"></span>**8.1.2.3 Passwords and Logging**

Passwords can be written as plain text in SQL statements such as CREATE USER, GRANT and SET PASSWORD. If such statements are logged by the MySQL server as written, passwords in them become visible to anyone with access to the logs.

Statement logging avoids writing passwords as cleartext for the following statements:

```
CREATE USER ... IDENTIFIED BY ...
ALTER USER ... IDENTIFIED BY ...
SET PASSWORD ...
START REPLICA ... PASSWORD = ...
CREATE SERVER ... OPTIONS(... PASSWORD ...)
ALTER SERVER ... OPTIONS(... PASSWORD ...)
```

Passwords in those statements are rewritten to not appear literally in statement text written to the general query log, slow query log, and binary log. Rewriting does not apply to other statements. In particular, INSERT or UPDATE statements for the mysql.user system table that refer to literal passwords are logged as is, so you should avoid such statements. (Direct modification of grant tables is discouraged, anyway.)

For the general query log, password rewriting can be suppressed by starting the server with the --log-raw option. For security reasons, this option is not recommended for production use. For diagnostic purposes, it may be useful to see the exact text of statements as received by the server.

By default, contents of audit log files produced by the audit log plugin are not encrypted and may contain sensitive information, such as the text of SQL statements. For security reasons, audit log files should be written to a directory accessible only to the MySQL server and to users with a legitimate reason to view the log. See Section 8.4.5.3, "MySQL Enterprise Audit Security Considerations".

Statements received by the server may be rewritten if a query rewrite plugin is installed (see [Query](https://dev.mysql.com/doc/extending-mysql/8.4/en/plugin-types.md#query-rewrite-plugin-type) [Rewrite Plugins](https://dev.mysql.com/doc/extending-mysql/8.4/en/plugin-types.md#query-rewrite-plugin-type)). In this case, the --log-raw option affects statement logging as follows:

- Without --log-raw, the server logs the statement returned by the query rewrite plugin. This may differ from the statement as received.
- With --log-raw, the server logs the original statement as received.

An implication of password rewriting is that statements that cannot be parsed (due, for example, to syntax errors) are not written to the general query log because they cannot be known to be password free. Use cases that require logging of all statements including those with errors should use the - log-raw option, bearing in mind that this also bypasses password rewriting.

Password rewriting occurs only when plain text passwords are expected. For statements with syntax that expect a password hash value, no rewriting occurs. If a plain text password is supplied erroneously for such syntax, the password is logged as given, without rewriting.

To guard log files against unwarranted exposure, locate them in a directory that restricts access to the server and the database administrator. If the server logs to tables in the mysql database, grant access to those tables only to the database administrator.

Replicas store the password for the replication source server in their connection metadata repository, which by default is a table in the mysql database named slave\_master\_info. The use of a file in the data directory for the connection metadata repository is now deprecated, but still possible (see Section 19.2.4, "Relay Log and Replication Metadata Repositories"). Ensure that the connection metadata repository can be accessed only by the database administrator. An alternative to storing the password in the connection metadata repository is to use the START REPLICA or START GROUP\_REPLICATION statement to specify credentials for connecting to the source.

Use a restricted access mode to protect database backups that include log tables or log files containing passwords.

# <span id="page-160-0"></span>**8.1.3 Making MySQL Secure Against Attackers**

When you connect to a MySQL server, you should use a password. The password is not transmitted as cleartext over the connection.

All other information is transferred as text, and can be read by anyone who is able to watch the connection. If the connection between the client and the server goes through an untrusted network, and you are concerned about this, you can use the compressed protocol to make traffic much more difficult to decipher. You can also use MySQL's internal SSL support to make the connection even more secure. See Section 8.3, "Using Encrypted Connections". Alternatively, use SSH to get an encrypted TCP/IP connection between a MySQL server and a MySQL client. You can find an Open Source SSH client at [http://www.openssh.org/,](http://www.openssh.org/) and a comparison of both Open Source and Commercial SSH clients at [http://en.wikipedia.org/wiki/Comparison\\_of\\_SSH\\_clients](http://en.wikipedia.org/wiki/Comparison_of_SSH_clients).

To make a MySQL system secure, you should strongly consider the following suggestions:

• Require all MySQL accounts to have a password. A client program does not necessarily know the identity of the person running it. It is common for client/server applications that the user can specify any user name to the client program. For example, anyone can use the mysql program to connect as any other person simply by invoking it as mysql -u other\_user db\_name if other\_user has no password. If all accounts have a password, connecting using another user's account becomes much more difficult.

For a discussion of methods for setting passwords, see Section 8.2.14, "Assigning Account Passwords".

- Make sure that the only Unix user account with read or write privileges in the database directories is the account that is used for running mysqld.
- Never run the MySQL server as the Unix root user. This is extremely dangerous, because any user with the [FILE](#page-175-2) privilege is able to cause the server to create files as root (for example, ~root/.bashrc). To prevent this, mysqld refuses to run as root unless that is specified explicitly using the --user=root option.

mysqld can (and should) be run as an ordinary, unprivileged user instead. You can create a separate Unix account named mysql to make everything even more secure. Use this account only for administering MySQL. To start mysqld as a different Unix user, add a user option that specifies the user name in the [mysqld] group of the my.cnf option file where you specify server options. For example:

```
[mysqld]
user=mysql
```

This causes the server to start as the designated user whether you start it manually or by using mysqld\_safe or mysql.server. For more details, see [Section 8.1.5, "How to Run MySQL as a](#page-162-0) [Normal User"](#page-162-0).

Running mysqld as a Unix user other than root does not mean that you need to change the root user name in the user table. User names for MySQL accounts have nothing to do with user names for Unix accounts.

• Do not grant the [FILE](#page-175-2) privilege to nonadministrative users. Any user that has this privilege can write a file anywhere in the file system with the privileges of the mysqld daemon. This includes the server's data directory containing the files that implement the privilege tables. To make [FILE](#page-175-2)privilege operations a bit safer, files generated with SELECT ... INTO OUTFILE do not overwrite existing files and are writable by everyone.

The [FILE](#page-175-2) privilege may also be used to read any file that is world-readable or accessible to the Unix user that the server runs as. With this privilege, you can read any file into a database table. This could be abused, for example, by using LOAD DATA to load /etc/passwd into a table, which then can be displayed with SELECT.

To limit the location in which files can be read and written, set the secure\_file\_priv system to a specific directory. See Section 7.1.8, "Server System Variables".

- Encrypt binary log files and relay log files. Encryption helps to protect these files and the potentially sensitive data contained in them from being misused by outside attackers, and also from unauthorized viewing by users of the operating system where they are stored. You enable encryption on a MySQL server by setting the binlog\_encryption system variable to ON. For more information, see Section 19.3.2, "Encrypting Binary Log Files and Relay Log Files".
- Do not grant the [PROCESS](#page-175-3) or [SUPER](#page-177-1) privilege to nonadministrative users. The output of mysqladmin processlist and SHOW PROCESSLIST shows the text of any statements currently being executed, so any user who is permitted to see the server process list might be able to see statements issued by other users.

mysqld reserves an extra connection for users who have the [CONNECTION\\_ADMIN](#page-181-1) or [SUPER](#page-177-1) privilege, so that a MySQL root user can log in and check server activity even if all normal connections are in use.

The [SUPER](#page-177-1) privilege can be used to terminate client connections, change server operation by changing the value of system variables, and control replication servers.

- Do not permit the use of symlinks to tables. (This capability can be disabled with the --skipsymbolic-links option.) This is especially important if you run mysqld as root, because anyone that has write access to the server's data directory then could delete any file in the system! See Section 10.12.2.2, "Using Symbolic Links for MyISAM Tables on Unix".
- Stored programs and views should be written using the security guidelines discussed in Section 27.6, "Stored Object Access Control".
- If you do not trust your DNS, you should use IP addresses rather than host names in the grant tables. In any case, you should be very careful about creating grant table entries using host name values that contain wildcards.
- If you want to restrict the number of connections permitted to a single account, you can do so by setting the max\_user\_connections variable in mysqld. The CREATE USER and ALTER USER statements also support resource control options for limiting the extent of server use permitted to an account. See Section 15.7.1.3, "CREATE USER Statement", and Section 15.7.1.1, "ALTER USER Statement".
- If the plugin directory is writable by the server, it may be possible for a user to write executable code to a file in the directory using SELECT ... INTO DUMPFILE. This can be prevented by making plugin\_dir read only to the server or by setting secure\_file\_priv to a directory where SELECT writes can be made safely.

# <span id="page-161-0"></span>**8.1.4 Security-Related mysqld Options and Variables**

The following table shows mysqld options and system variables that affect security. For descriptions of each of these, see Section 7.1.7, "Server Command Options", and Section 7.1.8, "Server System Variables".

**Table 8.1 Security Option and Variable Summary**

| Name                        | Cmd-Line | Option File | System Var | Status Var | Var Scope | Dynamic |
|-----------------------------|----------|-------------|------------|------------|-----------|---------|
| allow<br>suspicious<br>udfs | Yes      | Yes         |            |            |           |         |
| automatic_sp_privileges Yes |          | Yes         | Yes        |            | Global    | Yes     |
| chroot                      | Yes      | Yes         |            |            |           |         |
| local_infile                | Yes      | Yes         | Yes        |            | Global    | Yes     |
| safe-user<br>create         | Yes      | Yes         |            |            |           |         |
| secure_file_privYes         |          | Yes         | Yes        |            | Global    | No      |
| skip-grant<br>tables        | Yes      | Yes         |            |            |           |         |
| skip_name_resolve Yes       |          | Yes         | Yes        |            | Global    | No      |
| skip_networkingYes          |          | Yes         | Yes        |            | Global    | No      |
| skip_show_database Yes      |          | Yes         | Yes        |            | Global    | No      |

# <span id="page-162-0"></span>**8.1.5 How to Run MySQL as a Normal User**

On Windows, you can run the server as a Windows service using a normal user account.

On Linux, for installations performed using a MySQL repository or RPM packages, the MySQL server mysqld should be started by the local mysql operating system user. Starting by another operating system user is not supported by the init scripts that are included as part of the MySQL repositories.

On Unix (or Linux for installations performed using tar.gz packages) , the MySQL server mysqld can be started and run by any user. However, you should avoid running the server as the Unix root user for security reasons. To change mysqld to run as a normal unprivileged Unix user user\_name, you must do the following:

- 1. Stop the server if it is running (use mysqladmin shutdown).
- 2. Change the database directories and files so that user\_name has privileges to read and write files in them (you might need to do this as the Unix root user):

```
$> chown -R user_name /path/to/mysql/datadir
```

If you do not do this, the server cannot access databases or tables when it runs as user\_name.

If directories or files within the MySQL data directory are symbolic links, chown -R might not follow symbolic links for you. If it does not, you must also follow those links and change the directories and files they point to.

- 3. Start the server as user user\_name. Another alternative is to start mysqld as the Unix root user and use the --user=user\_name option. mysqld starts, then switches to run as the Unix user user\_name before accepting any connections.
- 4. To start the server as the given user automatically at system startup time, specify the user name by adding a user option to the [mysqld] group of the /etc/my.cnf option file or the my.cnf option file in the server's data directory. For example:

```
[mysqld]
user=user_name
```

If your Unix machine itself is not secured, you should assign passwords to the MySQL root account in the grant tables. Otherwise, any user with a login account on that machine can run the mysql client with a --user=root option and perform any operation. (It is a good idea to assign passwords to

MySQL accounts in any case, but especially so when other login accounts exist on the server host.) See Section 2.9.4, "Securing the Initial MySQL Account".

# <span id="page-163-0"></span>**8.1.6 Security Considerations for LOAD DATA LOCAL**

The LOAD DATA statement loads a data file into a table. The statement can load a file located on the server host, or, if the LOCAL keyword is specified, on the client host.

The LOCAL version of LOAD DATA has two potential security issues:

- Because LOAD DATA LOCAL is an SQL statement, parsing occurs on the server side, and transfer of the file from the client host to the server host is initiated by the MySQL server, which tells the client the file named in the statement. In theory, a patched server could tell the client program to transfer a file of the server's choosing rather than the file named in the statement. Such a server could access any file on the client host to which the client user has read access. (A patched server could in fact reply with a file-transfer request to any statement, not just LOAD DATA LOCAL, so a more fundamental issue is that clients should not connect to untrusted servers.)
- In a Web environment where the clients are connecting from a Web server, a user could use LOAD DATA LOCAL to read any files that the Web server process has read access to (assuming that a user could run any statement against the SQL server). In this environment, the client with respect to the MySQL server actually is the Web server, not a remote program being run by users who connect to the Web server.

To avoid connecting to untrusted servers, clients can establish a secure connection and verify the server identity by connecting using the --ssl-mode=VERIFY\_IDENTITY option and the appropriate CA certificate. To implement this level of verification, you must first ensure that the CA certificate for the server is reliably available to the replica, otherwise availability issues will result. For more information, see Command Options for Encrypted Connections.

To avoid LOAD DATA issues, clients should avoid using LOCAL unless proper client-side precautions have been taken.

For control over local data loading, MySQL permits the capability to be enabled or disabled. MySQL also enables clients to restrict local data loading operations to files located in a designated directory.

- [Enabling or Disabling Local Data Loading Capability](#page-163-1)
- [Restricting Files Permitted for Local Data Loading](#page-164-0)
- [MySQL Shell and Local Data Loading](#page-165-0)

## <span id="page-163-1"></span>**Enabling or Disabling Local Data Loading Capability**

Administrators and applications can configure whether to permit local data loading as follows:

- On the server side:
  - The local\_infile system variable controls server-side LOCAL capability. Depending on the local\_infile setting, the server refuses or permits local data loading by clients that request local data loading.
  - By default, local\_infile is disabled. (This is a change from previous versions of MySQL.) To cause the server to refuse or permit LOAD DATA LOCAL statements explicitly (regardless of how client programs and libraries are configured at build time or runtime), start mysqld with local\_infile disabled or enabled. local\_infile can also be set at runtime.
- On the client side:
  - The ENABLED\_LOCAL\_INFILE CMake option controls the compiled-in default LOCAL capability for the MySQL client library (see Section 2.8.7, "MySQL Source-Configuration Options"). Clients that make no explicit arrangements therefore have LOCAL capability disabled or enabled according to the ENABLED\_LOCAL\_INFILE setting specified at MySQL build time.

- By default, the client library in MySQL binary distributions is compiled with ENABLED\_LOCAL\_INFILE disabled. If you compile MySQL from source, configure it with ENABLED\_LOCAL\_INFILE disabled or enabled based on whether clients that make no explicit arrangements should have LOCAL capability disabled or enabled.
- For client programs that use the C API, local data loading capability is determined by the default compiled into the MySQL client library. To enable or disable it explicitly, invoke the [mysql\\_options\(\)](https://dev.mysql.com/doc/c-api/8.4/en/mysql-options.md) C API function to disable or enable the MYSQL\_OPT\_LOCAL\_INFILE option. See [mysql\\_options\(\)](https://dev.mysql.com/doc/c-api/8.4/en/mysql-options.md).
- For the mysql client, local data loading capability is determined by the default compiled into the MySQL client library. To disable or enable it explicitly, use the --local-infile=0 or --localinfile[=1] option.
- For the mysqlimport client, local data loading is not used by default. To disable or enable it explicitly, use the --local=0 or --local[=1] option.
- If you use LOAD DATA LOCAL in Perl scripts or other programs that read the [client] group from option files, you can add a local-infile option setting to that group. To prevent problems for programs that do not understand this option, specify it using the loose- prefix:

```
[client]
loose-local-infile=0
```

or:

```
[client]
loose-local-infile=1
```

• In all cases, successful use of a LOCAL load operation by a client also requires that the server permits local loading.

If LOCAL capability is disabled, on either the server or client side, a client that attempts to issue a LOAD DATA LOCAL statement receives the following error message:

```
ERROR 3950 (42000): Loading local data is disabled; this must be
enabled on both the client and server side
```

# <span id="page-164-0"></span>**Restricting Files Permitted for Local Data Loading**

The MySQL client library enables client applications to restrict local data loading operations to files located in a designated directory. Certain MySQL client programs take advantage of this capability.

Client programs that use the C API can control which files to permit for load data loading using the MYSQL\_OPT\_LOCAL\_INFILE and MYSQL\_OPT\_LOAD\_DATA\_LOCAL\_DIR options of the [mysql\\_options\(\)](https://dev.mysql.com/doc/c-api/8.4/en/mysql-options.md) C API function (see [mysql\\_options\(\)](https://dev.mysql.com/doc/c-api/8.4/en/mysql-options.md)).

The effect of MYSQL\_OPT\_LOAD\_DATA\_LOCAL\_DIR depends on whether LOCAL data loading is enabled or disabled:

- If LOCAL data loading is enabled, either by default in the MySQL client library or by explicitly enabling MYSQL\_OPT\_LOCAL\_INFILE, the MYSQL\_OPT\_LOAD\_DATA\_LOCAL\_DIR option has no effect.
- If LOCAL data loading is disabled, either by default in the MySQL client library or by explicitly disabling MYSQL\_OPT\_LOCAL\_INFILE, the MYSQL\_OPT\_LOAD\_DATA\_LOCAL\_DIR option can be used to designate a permitted directory for locally loaded files. In this case, LOCAL data loading is permitted but restricted to files located in the designated directory. Interpretation of the MYSQL\_OPT\_LOAD\_DATA\_LOCAL\_DIR value is as follows:
  - If the value is the null pointer (the default), it names no directory, with the result that no files are permitted for LOCAL data loading.

• If the value is a directory path name, LOCAL data loading is permitted but restricted to files located in the named directory. Comparison of the directory path name and the path name of files to be loaded is case-sensitive regardless of the case sensitivity of the underlying file system.

MySQL client programs use the preceding [mysql\\_options\(\)](https://dev.mysql.com/doc/c-api/8.4/en/mysql-options.md) options as follows:

- The mysql client has a --load-data-local-dir option that takes a directory path or an empty string. mysql uses the option value to set the MYSQL\_OPT\_LOAD\_DATA\_LOCAL\_DIR option (with an empty string setting the value to the null pointer). The effect of --load-data-local-dir depends on whether LOCAL data loading is enabled:
  - If LOCAL data loading is enabled, either by default in the MySQL client library or by specifying local-infile[=1], the --load-data-local-dir option is ignored.
  - If LOCAL data loading is disabled, either by default in the MySQL client library or by specifying local-infile=0, the --load-data-local-dir option applies.

When --load-data-local-dir applies, the option value designates the directory in which local data files must be located. Comparison of the directory path name and the path name of files to be loaded is case-sensitive regardless of the case sensitivity of the underlying file system. If the option value is the empty string, it names no directory, with the result that no files are permitted for local data loading.

- mysqlimport sets MYSQL\_OPT\_LOAD\_DATA\_LOCAL\_DIR for each file that it processes so that the directory containing the file is the permitted local loading directory.
- For data loading operations corresponding to LOAD DATA statements, mysqlbinlog extracts the files from the binary log events, writes them as temporary files to the local file system, and writes LOAD DATA LOCAL statements to cause the files to be loaded. By default, mysqlbinlog writes these temporary files to an operating system-specific directory. The --local-load option can be used to explicitly specify the directory where mysqlbinlog should prepare local temporary files.

Because other processes can write files to the default system-specific directory, it is advisable to specify the --local-load option to mysqlbinlog to designate a different directory for data files, and then designate that same directory by specifying the --load-data-local-dir option to mysql when processing the output from mysqlbinlog.

## <span id="page-165-0"></span>**MySQL Shell and Local Data Loading**

MySQL Shell provides a number of utilities to dump tables, schemas, or server instances and load them into other instances. When you use these utilities to handle the data, MySQL Shell provides additional functions such as input preprocessing, multithreaded parallel loading, file compression and decompression, and handling access to Oracle Cloud Infrastructure Object Storage buckets. To get the best functionality, always use the most recent version available of MySQL Shell's dump and dump loading utilities.

MySQL Shell's data upload utilities use LOAD DATA LOCAL INFILE statements to upload data, so the local\_infile system variable must be set to ON on the target server instance. You can do this before uploading the data, and remove it again afterwards. The utilities handle the file transfer requests safely to deal with the security considerations discussed in this topic.

MySQL Shell includes these dump and dump loading utilities:

| Table export utility | Exports a MySQL relational table into a data file, which can be       |
|----------------------|-----------------------------------------------------------------------|
| util.exportTable()   | uploaded to a MySQL server instance using MySQL Shell's parallel      |
|                      | table import utility, imported to a different application, or used as |
|                      | a logical backup. The utility has preset options and customization    |
|                      | options to produce different output formats.                          |

Parallel table import utility util.importTable() Imports a data file to a MySQL relational table. The data file can be the output from MySQL Shell's table export utility or another

Instance dump utility util.dumpInstance(), schema dump utility util.dumpSchemas(), and table dump utility util.dumpTables()

Dump loading utility util.loadDump() format supported by the utility's preset and customization options. The utility can carry out input preprocessing before adding the data to the table. It can accept multiple data files to merge into a single relational table, and automatically decompresses compressed files.

Export an instance, schema, or table to a set of dump files, which can then be uploaded to a MySQL instance using MySQL Shell's dump loading utility. The utilities provide Oracle Cloud Infrastructure Object Storage streaming, MySQL HeatWave Service compatibility checks and modifications, and the ability to carry out a dry run to identify issues before proceeding with the dump.

Import dump files created using MySQL Shell's instance, schema, or table dump utility into a MySQL HeatWave Service DB System or a MySQL Server instance. The utility manages the upload process and provides data streaming from remote storage, parallel loading of tables or table chunks, progress state tracking, resume and reset capability, and the option of concurrent loading while the dump is still taking place. MySQL Shell's parallel table import utility can be used in combination with the dump loading utility to modify data before uploading it to the target MySQL instance.

For details of the utilities, see [MySQL Shell Utilities.](https://dev.mysql.com/doc/mysql-shell/8.4/en/mysql-shell-utilities.md)

# <span id="page-166-0"></span>**8.1.7 Client Programming Security Guidelines**

Client applications that access MySQL should use the following guidelines to avoid interpreting external data incorrectly or exposing sensitive information.

- [Handle External Data Properly](#page-166-1)
- [Handle MySQL Error Messages Properly](#page-167-0)

## <span id="page-166-1"></span>**Handle External Data Properly**

Applications that access MySQL should not trust any data entered by users, who can try to trick your code by entering special or escaped character sequences in Web forms, URLs, or whatever application you have built. Be sure that your application remains secure if a user tries to perform SQL injection by entering something like ; DROP DATABASE mysql; into a form. This is an extreme example, but large security leaks and data loss might occur as a result of hackers using similar techniques, if you do not prepare for them.

A common mistake is to protect only string data values. Remember to check numeric data as well. If an application generates a query such as SELECT \* FROM table WHERE ID=234 when a user enters the value 234, the user can enter the value 234 OR 1=1 to cause the application to generate the query SELECT \* FROM table WHERE ID=234 OR 1=1. As a result, the server retrieves every row in the table. This exposes every row and causes excessive server load. The simplest way to protect from this type of attack is to use single quotation marks around the numeric constants: SELECT \* FROM table WHERE ID='234'. If the user enters extra information, it all becomes part of the string. In a numeric context, MySQL automatically converts this string to a number and strips any trailing nonnumeric characters from it.

Sometimes people think that if a database contains only publicly available data, it need not be protected. This is incorrect. Even if it is permissible to display any row in the database, you should still protect against denial of service attacks (for example, those that are based on the technique in the preceding paragraph that causes the server to waste resources). Otherwise, your server becomes unresponsive to legitimate users.

Checklist:

- Enable strict SQL mode to tell the server to be more restrictive of what data values it accepts. See Section 7.1.11, "Server SQL Modes".
- Try to enter single and double quotation marks (' and ") in all of your Web forms. If you get any kind of MySQL error, investigate the problem right away.
- Try to modify dynamic URLs by adding %22 ("), %23 (#), and %27 (') to them.
- Try to modify data types in dynamic URLs from numeric to character types using the characters shown in the previous examples. Your application should be safe against these and similar attacks.
- Try to enter characters, spaces, and special symbols rather than numbers in numeric fields. Your application should remove them before passing them to MySQL or else generate an error. Passing unchecked values to MySQL is very dangerous!
- Check the size of data before passing it to MySQL.
- Have your application connect to the database using a user name different from the one you use for administrative purposes. Do not give your applications any access privileges they do not need.

Many application programming interfaces provide a means of escaping special characters in data values. Properly used, this prevents application users from entering values that cause the application to generate statements that have a different effect than you intend:

- MySQL SQL statements: Use SQL prepared statements and accept data values only by means of placeholders; see Section 15.5, "Prepared Statements".
- MySQL C API: Use the [mysql\\_real\\_escape\\_string\\_quote\(\)](https://dev.mysql.com/doc/c-api/8.4/en/mysql-real-escape-string-quote.md) API call. Alternatively, use the C API prepared statement interface and accept data values only by means of placeholders; see [C API](https://dev.mysql.com/doc/c-api/8.4/en/c-api-prepared-statement-interface.md) [Prepared Statement Interface](https://dev.mysql.com/doc/c-api/8.4/en/c-api-prepared-statement-interface.md).
- MySQL++: Use the escape and quote modifiers for query streams.
- PHP: Use either the mysqli or pdo\_mysql extensions, and not the older ext/mysql extension. The preferred API's support the improved MySQL authentication protocol and passwords, as well as prepared statements with placeholders. See also [MySQL and PHP](https://dev.mysql.com/doc/apis-php/en/).

If the older ext/mysql extension must be used, then for escaping use the [mysql\\_real\\_escape\\_string\\_quote\(\)](https://dev.mysql.com/doc/c-api/8.4/en/mysql-real-escape-string-quote.md) function and not [mysql\\_escape\\_string\(\)](https://dev.mysql.com/doc/c-api/8.4/en/mysql-escape-string.md) or addslashes() because only [mysql\\_real\\_escape\\_string\\_quote\(\)](https://dev.mysql.com/doc/c-api/8.4/en/mysql-real-escape-string-quote.md) is character set-aware; the other functions can be "bypassed" when using (invalid) multibyte character sets.

- Perl DBI: Use placeholders or the quote() method.
- Java JDBC: Use a PreparedStatement object and placeholders.

Other programming interfaces might have similar capabilities.

## <span id="page-167-0"></span>**Handle MySQL Error Messages Properly**

It is the application's responsibility to intercept errors that occur as a result of executing SQL statements with the MySQL database server and handle them appropriately.

The information returned in a MySQL error is not gratuitous because that information is key in debugging MySQL using applications. It would be nearly impossible, for example, to debug a common 10-way join SELECT statement without providing information regarding which databases, tables, and other objects are involved with problems. Thus, MySQL errors must sometimes necessarily contain references to the names of those objects.

A simple but insecure approach for an application when it receives such an error from MySQL is to intercept it and display it verbatim to the client. However, revealing error information is a known application vulnerability type [\(CWE-209](http://cwe.mitre.org/data/definitions/209.md)) and the application developer must ensure the application does not have this vulnerability.

For example, an application that displays a message such as this exposes both a database name and a table name to clients, which is information a client might attempt to exploit:

```
ERROR 1146 (42S02): Table 'mydb.mytable' doesn't exist
```

Instead, the proper behavior for an application when it receives such an error from MySQL is to log appropriate information, including the error information, to a secure audit location only accessible to trusted personnel. The application can return something more generic such as "Internal Error" to the user.

# <span id="page-168-0"></span>**8.2 Access Control and Account Management**

MySQL enables the creation of accounts that permit client users to connect to the server and access data managed by the server. The primary function of the MySQL privilege system is to authenticate a user who connects from a given host and to associate that user with privileges on a database such as SELECT, INSERT, UPDATE, and DELETE. Additional functionality includes the ability to grant privileges for administrative operations.

To control which users can connect, each account can be assigned authentication credentials such as a password. The user interface to MySQL accounts consists of SQL statements such as CREATE USER, GRANT, and REVOKE. See Section 15.7.1, "Account Management Statements".

The MySQL privilege system ensures that all users may perform only the operations permitted to them. As a user, when you connect to a MySQL server, your identity is determined by the host from which you connect and the user name you specify. When you issue requests after connecting, the system grants privileges according to your identity and what you want to do.

MySQL considers both your host name and user name in identifying you because there is no reason to assume that a given user name belongs to the same person on all hosts. For example, the user joe who connects from office.example.com need not be the same person as the user joe who connects from home.example.com. MySQL handles this by enabling you to distinguish users on different hosts that happen to have the same name: You can grant one set of privileges for connections by joe from office.example.com, and a different set of privileges for connections by joe from home.example.com. To see what privileges a given account has, use the SHOW GRANTS statement. For example:

```
SHOW GRANTS FOR 'joe'@'office.example.com';
SHOW GRANTS FOR 'joe'@'home.example.com';
```

Internally, the server stores privilege information in the grant tables of the mysql system database. The MySQL server reads the contents of these tables into memory when it starts and bases access-control decisions on the in-memory copies of the grant tables.

MySQL access control involves two stages when you run a client program that connects to the server:

**Stage 1:** The server accepts or rejects the connection based on your identity and whether you can verify your identity by supplying the correct password.

**Stage 2:** Assuming that you can connect, the server checks each statement you issue to determine whether you have sufficient privileges to perform it. For example, if you try to select rows from a table in a database or drop a table from the database, the server verifies that you have the [SELECT](#page-177-2) privilege for the table or the [DROP](#page-174-1) privilege for the database.

For a more detailed description of what happens during each stage, see Section 8.2.6, "Access Control, Stage 1: Connection Verification", and Section 8.2.7, "Access Control, Stage 2: Request Verification". For help in diagnosing privilege-related problems, see Section 8.2.22, "Troubleshooting Problems Connecting to MySQL".

If your privileges are changed (either by yourself or someone else) while you are connected, those changes do not necessarily take effect immediately for the next statement that you issue. For details about the conditions under which the server reloads the grant tables, see Section 8.2.13, "When Privilege Changes Take Effect".

There are some things that you cannot do with the MySQL privilege system:

- You cannot explicitly specify that a given user should be denied access. That is, you cannot explicitly match a user and then refuse the connection.
- You cannot specify that a user has privileges to create or drop tables in a database but not to create or drop the database itself.
- A password applies globally to an account. You cannot associate a password with a specific object such as a database, table, or routine.

# <span id="page-169-0"></span>**8.2.1 Account User Names and Passwords**

MySQL stores accounts in the user table of the mysql system database. An account is defined in terms of a user name and the client host or hosts from which the user can connect to the server. For information about account representation in the user table, see [Section 8.2.3, "Grant Tables"](#page-190-0).

An account may also have authentication credentials such as a password. The credentials are handled by the account authentication plugin. MySQL supports multiple authentication plugins. Some of them use built-in authentication methods, whereas others enable authentication using external authentication methods. See Section 8.2.17, "Pluggable Authentication".

There are several distinctions between the way user names and passwords are used by MySQL and your operating system:

- User names, as used by MySQL for authentication purposes, have nothing to do with user names (login names) as used by Windows or Unix. On Unix, most MySQL clients by default try to log in using the current Unix user name as the MySQL user name, but that is for convenience only. The default can be overridden easily, because client programs permit any user name to be specified with a -u or --user option. This means that anyone can attempt to connect to the server using any user name, so you cannot make a database secure in any way unless all MySQL accounts have passwords. Anyone who specifies a user name for an account that has no password can connect successfully to the server.
- MySQL user names are up to 32 characters long. Operating system user names may have a different maximum length.

![](_page_169_Picture_11.jpeg)

### **Warning**

The MySQL user name length limit is hardcoded in MySQL servers and clients, and trying to circumvent it by modifying the definitions of the tables in the mysql database does not work.

You should never alter the structure of tables in the mysql database in any manner whatsoever except by means of the procedure that is described in Chapter 3, Upgrading MySQL. Attempting to redefine the MySQL system tables in any other fashion results in undefined and unsupported behavior. The server is free to ignore rows that become malformed as a result of such modifications.

• To authenticate client connections for accounts that use built-in authentication methods, the server uses passwords stored in the user table. These passwords are distinct from passwords for logging in to your operating system. There is no necessary connection between the "external" password you use to log in to a Windows or Unix machine and the password you use to access the MySQL server on that machine.

If the server authenticates a client using some other plugin, the authentication method that the plugin implements may or may not use a password stored in the user table. In this case, it is possible that an external password is also used to authenticate to the MySQL server.

• Passwords stored in the user table are encrypted using plugin-specific algorithms.

• If the user name and password contain only ASCII characters, it is possible to connect to the server regardless of character set settings. To enable connections when the user name or password contain non-ASCII characters, client applications should call the [mysql\\_options\(\)](https://dev.mysql.com/doc/c-api/8.4/en/mysql-options.md) C API function with the MYSQL\_SET\_CHARSET\_NAME option and appropriate character set name as arguments. This causes authentication to take place using the specified character set. Otherwise, authentication fails unless the server default character set is the same as the encoding in the authentication defaults.

Standard MySQL client programs support a --default-character-set option that causes [mysql\\_options\(\)](https://dev.mysql.com/doc/c-api/8.4/en/mysql-options.md) to be called as just described. In addition, character set autodetection is supported as described in Section 12.4, "Connection Character Sets and Collations". For programs that use a connector that is not based on the C API, the connector may provide an equivalent to [mysql\\_options\(\)](https://dev.mysql.com/doc/c-api/8.4/en/mysql-options.md) that can be used instead. Check the connector documentation.

The preceding notes do not apply for ucs2, utf16, and utf32, which are not permitted as client character sets.

The MySQL installation process populates the grant tables with an initial root account, as described in Section 2.9.4, "Securing the Initial MySQL Account", which also discusses how to assign a password to it. Thereafter, you normally set up, modify, and remove MySQL accounts using statements such as CREATE USER, DROP USER, GRANT, and REVOKE. See Section 8.2.8, "Adding Accounts, Assigning Privileges, and Dropping Accounts", and Section 15.7.1, "Account Management Statements".

To connect to a MySQL server with a command-line client, specify user name and password options as necessary for the account that you want to use:

```
$> mysql --user=finley --password db_name
```

If you prefer short options, the command looks like this:

```
$> mysql -u finley -p db_name
```

If you omit the password value following the --password or -p option on the command line (as just shown), the client prompts for one. Alternatively, the password can be specified on the command line:

```
$> mysql --user=finley --password=password db_name
$> mysql -u finley -ppassword db_name
```

If you use the -p option, there must be no space between -p and the following password value.

Specifying a password on the command line should be considered insecure. See [Section 8.1.2.1,](#page-157-1) ["End-User Guidelines for Password Security".](#page-157-1) To avoid giving the password on the command line, use an option file or a login path file. See Section 6.2.2.2, "Using Option Files", and Section 6.6.7, "mysql\_config\_editor — MySQL Configuration Utility".

For additional information about specifying user names, passwords, and other connection parameters, see Section 6.2.4, "Connecting to the MySQL Server Using Command Options".

# <span id="page-170-0"></span>**8.2.2 Privileges Provided by MySQL**

The privileges granted to a MySQL account determine which operations the account can perform. MySQL privileges differ in the contexts in which they apply and at different levels of operation:

- Administrative privileges enable users to manage operation of the MySQL server. These privileges are global because they are not specific to a particular database.
- Database privileges apply to a database and to all objects within it. These privileges can be granted for specific databases, or globally so that they apply to all databases.
- Privileges for database objects such as tables, indexes, views, and stored routines can be granted for specific objects within a database, for all objects of a given type within a database (for example, all tables in a database), or globally for all objects of a given type in all databases.

Privileges also differ in terms of whether they are static (built in to the server) or dynamic (defined at runtime). Whether a privilege is static or dynamic affects its availability to be granted to user accounts and roles. For information about the differences between static and dynamic privileges, see [Static](#page-188-0) [Versus Dynamic Privileges.](#page-188-0))

Information about account privileges is stored in the grant tables in the mysql system database. For a description of the structure and contents of these tables, see [Section 8.2.3, "Grant Tables".](#page-190-0) The MySQL server reads the contents of the grant tables into memory when it starts, and reloads them under the circumstances indicated in Section 8.2.13, "When Privilege Changes Take Effect". The server bases access-control decisions on the in-memory copies of the grant tables.

![](_page_171_Picture_3.jpeg)

#### **Important**

Some MySQL releases introduce changes to the grant tables to add new privileges or features. To make sure that you can take advantage of any new capabilities, update your grant tables to the current structure whenever you upgrade MySQL. See Chapter 3, Upgrading MySQL.

The following sections summarize the available privileges, provide more detailed descriptions of each privilege, and offer usage guidelines.

- [Summary of Available Privileges](#page-171-0)
- [Static Privilege Descriptions](#page-173-0)
- [Dynamic Privilege Descriptions](#page-179-0)
- [Privilege-Granting Guidelines](#page-187-1)
- [Static Versus Dynamic Privileges](#page-188-0)
- [Migrating Accounts from SUPER to Dynamic Privileges](#page-189-0)

## <span id="page-171-0"></span>**Summary of Available Privileges**

The following table shows the static privilege names used in GRANT and REVOKE statements, along with the column name associated with each privilege in the grant tables and the context in which the privilege applies.

**Table 8.2 Permissible Static Privileges for GRANT and REVOKE**

| Privilege               | Grant Table Column           | Context                       |
|-------------------------|------------------------------|-------------------------------|
| ALL [PRIVILEGES]        | Synonym for "all privileges" | Server administration         |
| ALTER                   | Alter_priv                   | Tables                        |
| ALTER ROUTINE           | Alter_routine_priv           | Stored routines               |
| CREATE                  | Create_priv                  | Databases, tables, or indexes |
| CREATE ROLE             | Create_role_priv             | Server administration         |
| CREATE ROUTINE          | Create_routine_priv          | Stored routines               |
| CREATE TABLESPACE       | Create_tablespace_priv       | Server administration         |
| CREATE TEMPORARY TABLES | Create_tmp_table_priv        | Tables                        |
| CREATE USER             | Create_user_priv             | Server administration         |
| CREATE VIEW             | Create_view_priv             | Views                         |
| DELETE                  | Delete_priv                  | Tables                        |
| DROP                    | Drop_priv                    | Databases, tables, or views   |
| DROP ROLE               | Drop_role_priv               | Server administration         |
| EVENT                   | Event_priv                   | Databases                     |
| EXECUTE                 | Execute_priv                 | Stored routines               |

| Privilege          | Grant Table Column          | Context                                  |
|--------------------|-----------------------------|------------------------------------------|
| FILE               | File_priv                   | File access on server host               |
| GRANT OPTION       | Grant_priv                  | Databases, tables, or stored<br>routines |
| INDEX              | Index_priv                  | Tables                                   |
| INSERT             | Insert_priv                 | Tables or columns                        |
| LOCK TABLES        | Lock_tables_priv            | Databases                                |
| PROCESS            | Process_priv                | Server administration                    |
| PROXY              | See proxies_priv table      | Server administration                    |
| REFERENCES         | References_priv             | Databases or tables                      |
| RELOAD             | Reload_priv                 | Server administration                    |
| REPLICATION CLIENT | Repl_client_priv            | Server administration                    |
| REPLICATION SLAVE  | Repl_slave_priv             | Server administration                    |
| SELECT             | Select_priv                 | Tables or columns                        |
| SHOW DATABASES     | Show_db_priv                | Server administration                    |
| SHOW VIEW          | Show_view_priv              | Views                                    |
| SHUTDOWN           | Shutdown_priv               | Server administration                    |
| SUPER              | Super_priv                  | Server administration                    |
| TRIGGER            | Trigger_priv                | Tables                                   |
| UPDATE             | Update_priv                 | Tables or columns                        |
| USAGE              | Synonym for "no privileges" | Server administration                    |

The following table shows the dynamic privilege names used in GRANT and REVOKE statements, along with the context in which the privilege applies.

**Table 8.3 Permissible Dynamic Privileges for GRANT and REVOKE**

| Privilege                   | Context                                   |
|-----------------------------|-------------------------------------------|
| ALLOW_NONEXISTENT_DEFINER   | Orphan object protection                  |
| APPLICATION_PASSWORD_ADMIN  | Dual password administration              |
| AUDIT_ABORT_EXEMPT          | Allow queries blocked by audit log filter |
| AUDIT_ADMIN                 | Audit log administration                  |
| AUTHENTICATION_POLICY_ADMIN | Authentication administration             |
| BACKUP_ADMIN                | Backup administration                     |
| BINLOG_ADMIN                | Backup and Replication administration     |
| BINLOG_ENCRYPTION_ADMIN     | Backup and Replication administration     |
| CLONE_ADMIN                 | Clone administration                      |
| CONNECTION_ADMIN            | Server administration                     |
| ENCRYPTION_KEY_ADMIN        | Server administration                     |
| FIREWALL_ADMIN              | Firewall administration                   |
| FIREWALL_EXEMPT             | Firewall administration                   |
| FIREWALL_USER               | Firewall administration                   |
| FLUSH_OPTIMIZER_COSTS       | Server administration                     |
| FLUSH_PRIVILEGES            | Server administration                     |
| FLUSH_STATUS                | Server administration                     |

| Privilege                    | Context                                                   |
|------------------------------|-----------------------------------------------------------|
| FLUSH_TABLES                 | Server administration                                     |
| FLUSH_USER_RESOURCES         | Server administration                                     |
| GROUP_REPLICATION_ADMIN      | Replication administration                                |
| GROUP_REPLICATION_STREAM     | Replication administration                                |
| INNODB_REDO_LOG_ARCHIVE      | Redo log archiving administration                         |
| INNODB_REDO_LOG_ENABLE       | Redo log administration                                   |
| MASKING_DICTIONARIES_ADMIN   | Server administration                                     |
| NDB_STORED_USER              | NDB Cluster                                               |
| OPTIMIZE_LOCAL_TABLE         | OPTIMIZE LOCAL TABLE statements                           |
| PASSWORDLESS_USER_ADMIN      | Authentication administration                             |
| PERSIST_RO_VARIABLES_ADMIN   | Server administration                                     |
| REPLICATION_APPLIER          | PRIVILEGE_CHECKS_USER for a replication<br>channel        |
| REPLICATION_SLAVE_ADMIN      | Replication administration                                |
| RESOURCE_GROUP_ADMIN         | Resource group administration                             |
| RESOURCE_GROUP_USER          | Resource group administration                             |
| ROLE_ADMIN                   | Server administration                                     |
| SENSITIVE_VARIABLES_OBSERVER | Server administration                                     |
| SESSION_VARIABLES_ADMIN      | Server administration                                     |
| SET_ANY_DEFINER              | Server administration                                     |
| SHOW_ROUTINE                 | Server administration                                     |
| SKIP_QUERY_REWRITE           | Server administration                                     |
| SYSTEM_USER                  | Server administration                                     |
| SYSTEM_VARIABLES_ADMIN       | Server administration                                     |
| TABLE_ENCRYPTION_ADMIN       | Server administration                                     |
| TELEMETRY_LOG_ADMIN          | Telemetry log administration for MySQL<br>HeatWave on AWS |
| TP_CONNECTION_ADMIN          | Thread pool administration                                |
| TRANSACTION_GTID_TAG         | Replication administration                                |
| VERSION_TOKEN_ADMIN          | Server administration                                     |
| XA_RECOVER_ADMIN             | Server administration                                     |

# <span id="page-173-0"></span>**Static Privilege Descriptions**

Static privileges are built in to the server, in contrast to dynamic privileges, which are defined at runtime. The following list describes each static privilege available in MySQL.

Particular SQL statements might have more specific privilege requirements than indicated here. If so, the description for the statement in question provides the details.

# <span id="page-173-1"></span>• [ALL](#page-173-1), [ALL PRIVILEGES](#page-173-1)

These privilege specifiers are shorthand for "all privileges available at a given privilege level" (except [GRANT OPTION](#page-175-6)). For example, granting [ALL](#page-173-1) at the global or table level grants all global privileges or all table-level privileges, respectively.

<span id="page-173-2"></span>• [ALTER](#page-173-2)

Enables use of the ALTER TABLE statement to change the structure of tables. ALTER TABLE also requires the [CREATE](#page-174-3) and [INSERT](#page-175-0) privileges. Renaming a table requires [ALTER](#page-173-2) and [DROP](#page-174-1) on the old table, [CREATE](#page-174-3), and [INSERT](#page-175-0) on the new table.

#### <span id="page-174-2"></span>• [ALTER ROUTINE](#page-174-2)

Enables use of statements that alter or drop stored routines (stored procedures and functions). For routines that fall within the scope at which the privilege is granted and for which the user is not the user named as the routine DEFINER, also enables access to routine properties other than the routine definition.

#### <span id="page-174-3"></span>• [CREATE](#page-174-3)

Enables use of statements that create new databases and tables.

#### <span id="page-174-4"></span>• [CREATE ROLE](#page-174-4)

Enables use of the CREATE ROLE statement. (The [CREATE USER](#page-174-8) privilege also enables use of the CREATE ROLE statement.) See Section 8.2.10, "Using Roles".

The [CREATE ROLE](#page-174-4) and [DROP ROLE](#page-175-4) privileges are not as powerful as [CREATE USER](#page-174-8) because they can be used only to create and drop accounts. They cannot be used as [CREATE USER](#page-174-8) can be modify account attributes or rename accounts. See User and Role Interchangeability.

#### <span id="page-174-5"></span>• [CREATE ROUTINE](#page-174-5)

Enables use of statements that create stored routines (stored procedures and functions). For routines that fall within the scope at which the privilege is granted and for which the user is not the user named as the routine DEFINER, also enables access to routine properties other than the routine definition.

#### <span id="page-174-6"></span>• [CREATE TABLESPACE](#page-174-6)

Enables use of statements that create, alter, or drop tablespaces and log file groups.

#### <span id="page-174-7"></span>• [CREATE TEMPORARY TABLES](#page-174-7)

Enables the creation of temporary tables using the CREATE TEMPORARY TABLE statement.

After a session has created a temporary table, the server performs no further privilege checks on the table. The creating session can perform any operation on the table, such as DROP TABLE, INSERT, UPDATE, or SELECT. For more information, see Section 15.1.20.2, "CREATE TEMPORARY TABLE Statement".

#### <span id="page-174-8"></span>• [CREATE USER](#page-174-8)

Enables use of the ALTER USER, CREATE ROLE, CREATE USER, DROP ROLE, DROP USER, RENAME USER, and REVOKE ALL PRIVILEGES statements.

### <span id="page-174-9"></span>• [CREATE VIEW](#page-174-9)

Enables use of the CREATE VIEW statement.

#### <span id="page-174-0"></span>• [DELETE](#page-174-0)

Enables rows to be deleted from tables in a database.

# <span id="page-174-1"></span>• [DROP](#page-174-1)

Enables use of statements that drop (remove) existing databases, tables, and views. The [DROP](#page-174-1) privilege is required to use the ALTER TABLE ... DROP PARTITION statement on a partitioned table. The [DROP](#page-174-1) privilege is also required for TRUNCATE TABLE.

#### <span id="page-175-4"></span>• [DROP ROLE](#page-175-4)

Enables use of the DROP ROLE statement. (The [CREATE USER](#page-174-8) privilege also enables use of the DROP ROLE statement.) See Section 8.2.10, "Using Roles".

The [CREATE ROLE](#page-174-4) and [DROP ROLE](#page-175-4) privileges are not as powerful as [CREATE USER](#page-174-8) because they can be used only to create and drop accounts. They cannot be used as [CREATE USER](#page-174-8) can be modify account attributes or rename accounts. See User and Role Interchangeability.

### <span id="page-175-5"></span>• [EVENT](#page-175-5)

Enables use of statements that create, alter, drop, or display events for the Event Scheduler.

## <span id="page-175-1"></span>• [EXECUTE](#page-175-1)

Enables use of statements that execute stored routines (stored procedures and functions). For routines that fall within the scope at which the privilege is granted and for which the user is not the user named as the routine DEFINER, also enables access to routine properties other than the routine definition.

### <span id="page-175-2"></span>• [FILE](#page-175-2)

Affects the following operations and server behaviors:

- Enables reading and writing files on the server host using the LOAD DATA and SELECT ... INTO OUTFILE statements and the LOAD\_FILE() function. A user who has the [FILE](#page-175-2) privilege can read any file on the server host that is either world-readable or readable by the MySQL server. (This implies the user can read any file in any database directory, because the server can access any of those files.)
- Enables creating new files in any directory where the MySQL server has write access. This includes the server's data directory containing the files that implement the privilege tables.
- Enables use of the DATA DIRECTORY or INDEX DIRECTORY table option for the CREATE TABLE statement.

As a security measure, the server does not overwrite existing files.

To limit the location in which files can be read and written, set the secure\_file\_priv system variable to a specific directory. See Section 7.1.8, "Server System Variables".

#### <span id="page-175-6"></span>• [GRANT OPTION](#page-175-6)

Enables you to grant to or revoke from other users those privileges that you yourself possess.

### <span id="page-175-7"></span>• [INDEX](#page-175-7)

Enables use of statements that create or drop (remove) indexes. [INDEX](#page-175-7) applies to existing tables. If you have the [CREATE](#page-174-3) privilege for a table, you can include index definitions in the CREATE TABLE statement.

#### <span id="page-175-0"></span>• [INSERT](#page-175-0)

Enables rows to be inserted into tables in a database. [INSERT](#page-175-0) is also required for the ANALYZE TABLE, OPTIMIZE TABLE, and REPAIR TABLE table-maintenance statements.

#### <span id="page-175-8"></span>• [LOCK TABLES](#page-175-8)

Enables use of explicit LOCK TABLES statements to lock tables for which you have the [SELECT](#page-177-2) privilege. This includes use of write locks, which prevents other sessions from reading the locked table.

# <span id="page-175-3"></span>• [PROCESS](#page-175-3)

The [PROCESS](#page-175-3) privilege controls access to information about threads executing within the server (that is, information about statements being executed by sessions). Thread information available using the SHOW PROCESSLIST statement, the mysqladmin processlist command, the Information Schema PROCESSLIST table, and the Performance Schema processlist table is accessible as follows:

- With the [PROCESS](#page-175-3) privilege, a user has access to information about all threads, even those belonging to other users.
- Without the [PROCESS](#page-175-3) privilege, nonanonymous users have access to information about their own threads but not threads for other users, and anonymous users have no access to thread information.

![](_page_176_Picture_4.jpeg)

#### **Note**

The Performance Schema threads table also provides thread information, but table access uses a different privilege model. See Section 29.12.22.8, "The threads Table".

The [PROCESS](#page-175-3) privilege also enables use of the SHOW ENGINE statement, access to the INFORMATION\_SCHEMA InnoDB tables (tables with names that begin with INNODB\_), and access to the INFORMATION\_SCHEMA FILES table.

<span id="page-176-1"></span>• [PROXY](#page-176-1)

Enables one user to impersonate or become known as another user. See Section 8.2.19, "Proxy Users".

<span id="page-176-2"></span>• [REFERENCES](#page-176-2)

Creation of a foreign key constraint requires the [REFERENCES](#page-176-2) privilege for the parent table.

<span id="page-176-0"></span>• [RELOAD](#page-176-0)

The [RELOAD](#page-176-0) enables the following operations:

- Use of the FLUSH statement.
- Use of mysqladmin commands that are equivalent to FLUSH operations: flush-hosts, flushlogs, flush-privileges, flush-status, flush-tables, refresh, and reload.

The reload command tells the server to reload the grant tables into memory. flushprivileges is a synonym for reload. The refresh command closes and reopens the log files and flushes all tables. The other flush-xxx commands perform functions similar to refresh, but are more specific and may be preferable in some instances. For example, if you want to flush just the log files, flush-logs is a better choice than refresh.

- Use of mysqldump options that perform various FLUSH operations: --flush-logs and source-data.
- Use of the RESET BINARY LOGS AND GTIDS and RESET REPLICA statements.
- <span id="page-176-3"></span>• [REPLICATION CLIENT](#page-176-3)

Enables use of the SHOW BINARY LOG STATUS, SHOW REPLICA STATUS, and SHOW BINARY LOGS statements.

<span id="page-176-4"></span>• [REPLICATION SLAVE](#page-176-4)

Enables the account to request updates that have been made to databases on the replication source server, using the SHOW REPLICAS, SHOW RELAYLOG EVENTS, and SHOW BINLOG EVENTS

statements. This privilege is also required to use the mysqlbinlog options --read-fromremote-server (-R) and --read-from-remote-source. Grant this privilege to accounts that are used by replicas to connect to the current server as their replication source server.

#### <span id="page-177-2"></span>• [SELECT](#page-177-2)

Enables rows to be selected from tables in a database. SELECT statements require the [SELECT](#page-177-2) privilege only if they actually access tables. Some SELECT statements do not access tables and can be executed without permission for any database. For example, you can use SELECT as a simple calculator to evaluate expressions that make no reference to tables:

```
SELECT 1+1;
SELECT PI()*2;
```

The [SELECT](#page-177-2) privilege is also needed for other statements that read column values. For example, [SELECT](#page-177-2) is needed for columns referenced on the right hand side of col\_name=expr assignment in UPDATE statements or for columns named in the WHERE clause of DELETE or UPDATE statements.

The [SELECT](#page-177-2) privilege is needed for tables or views used with EXPLAIN, including any underlying tables in view definitions.

#### <span id="page-177-3"></span>• [SHOW DATABASES](#page-177-3)

Enables the account to see database names by issuing the SHOW DATABASE statement. Accounts that do not have this privilege see only databases for which they have some privileges, and cannot use the statement at all if the server was started with the --skip-show-database option.

![](_page_177_Picture_9.jpeg)

#### **Caution**

Because any static global privilege is considered a privilege for all databases, any static global privilege enables a user to see all database names with SHOW DATABASES or by examining the SCHEMATA table of INFORMATION\_SCHEMA, except databases that have been restricted at the database level by partial revokes.

#### <span id="page-177-4"></span>• [SHOW VIEW](#page-177-4)

Enables use of the SHOW CREATE VIEW statement. This privilege is also needed for views used with EXPLAIN.

## <span id="page-177-0"></span>• [SHUTDOWN](#page-177-0)

Enables use of the SHUTDOWN and RESTART statements, the mysqladmin shutdown command, and the [mysql\\_shutdown\(\)](https://dev.mysql.com/doc/c-api/8.4/en/mysql-shutdown.md) C API function.

#### <span id="page-177-1"></span>• [SUPER](#page-177-1)

[SUPER](#page-177-1) is a powerful and far-reaching privilege and should not be granted lightly. If an account needs to perform only a subset of [SUPER](#page-177-1) operations, it may be possible to achieve the desired privilege set

by instead granting one or more dynamic privileges, each of which confers more limited capabilities. See [Dynamic Privilege Descriptions](#page-179-0).

![](_page_178_Picture_2.jpeg)

#### **Note**

[SUPER](#page-177-1) is deprecated, and you should expect it to be removed in a future version of MySQL. See [Migrating Accounts from SUPER to Dynamic](#page-189-0) [Privileges.](#page-189-0)

[SUPER](#page-177-1) affects the following operations and server behaviors:

- Enables system variable changes at runtime:
  - Enables server configuration changes to global system variables with SET GLOBAL and SET PERSIST.

The corresponding dynamic privilege is [SYSTEM\\_VARIABLES\\_ADMIN](#page-186-1).

• Enables setting restricted session system variables that require a special privilege.

The corresponding dynamic privilege is [SESSION\\_VARIABLES\\_ADMIN](#page-184-5).

See also Section 7.1.9.1, "System Variable Privileges".

• Enables changes to global transaction characteristics (see Section 15.3.7, "SET TRANSACTION Statement").

The corresponding dynamic privilege is [SYSTEM\\_VARIABLES\\_ADMIN](#page-186-1).

• Enables the account to start and stop replication, including Group Replication.

The corresponding dynamic privilege is [REPLICATION\\_SLAVE\\_ADMIN](#page-184-1) for regular replication, [GROUP\\_REPLICATION\\_ADMIN](#page-182-5) for Group Replication.

• Enables use of CHANGE REPLICATION SOURCE TO and CHANGE REPLICATION FILTER statements.

The corresponding dynamic privilege is [REPLICATION\\_SLAVE\\_ADMIN](#page-184-1).

• Enables binary log control by means of the PURGE BINARY LOGS and BINLOG statements.

The corresponding dynamic privilege is [BINLOG\\_ADMIN](#page-181-2).

• Enables setting the effective authorization ID when executing a view or stored program. A user with this privilege can specify any account in the DEFINER attribute of a view or stored program.

The corresponding dynamic privileges are [SET\\_ANY\\_DEFINER](#page-185-1) and [ALLOW\\_NONEXISTENT\\_DEFINER](#page-180-1).

- Enables use of the CREATE SERVER, ALTER SERVER, and DROP SERVER statements.
- Enables use of the mysqladmin debug command.
- Enables InnoDB encryption key rotation.

The corresponding dynamic privilege is [ENCRYPTION\\_KEY\\_ADMIN](#page-181-4).

• Enables execution of Version Tokens functions.

The corresponding dynamic privilege is [VERSION\\_TOKEN\\_ADMIN](#page-187-0).

• Enables granting and revoking roles, use of the WITH ADMIN OPTION clause of the GRANT statement, and nonempty <graphml> element content in the result from the ROLES\_GRAPHML() function.

The corresponding dynamic privilege is [ROLE\\_ADMIN](#page-184-4).

- Enables control over client connections not permitted to non-[SUPER](#page-177-1) accounts:
  - Enables use of the KILL statement or mysqladmin kill command to kill threads belonging to other accounts. (An account can always kill its own threads.)
  - The server does not execute init\_connect system variable content when [SUPER](#page-177-1) clients connect.
  - The server accepts one connection from a [SUPER](#page-177-1) client even if the connection limit configured by the max\_connections system variable is reached.
  - A server in offline mode (offline\_mode enabled) does not terminate [SUPER](#page-177-1) client connections at the next client request, and accepts new connections from [SUPER](#page-177-1) clients.
  - Updates can be performed even when the read\_only system variable is enabled. This applies to explicit table updates, and to use of account-management statements such as GRANT and REVOKE that update tables implicitly.

The corresponding dynamic privilege for the preceding connection control operations is [CONNECTION\\_ADMIN](#page-181-1).

You may also need the [SUPER](#page-177-1) privilege to create or alter stored functions if binary logging is enabled, as described in Section 27.7, "Stored Program Binary Logging".

#### <span id="page-179-1"></span>• [TRIGGER](#page-179-1)

Enables trigger operations. You must have this privilege for a table to create, drop, execute, or display triggers for that table.

When a trigger is activated (by a user who has privileges to execute INSERT, UPDATE, or DELETE statements for the table associated with the trigger), trigger execution requires that the user who defined the trigger still have the [TRIGGER](#page-179-1) privilege for the table.

#### <span id="page-179-2"></span>• [UPDATE](#page-179-2)

Enables rows to be updated in tables in a database.

#### <span id="page-179-3"></span>• [USAGE](#page-179-3)

This privilege specifier stands for "no privileges." It is used at the global level with GRANT to specify clauses such as WITH GRANT OPTION without naming specific account privileges in the privilege list. SHOW GRANTS displays [USAGE](#page-179-3) to indicate that an account has no privileges at a privilege level.

## <span id="page-179-0"></span>**Dynamic Privilege Descriptions**

Dynamic privileges are defined at runtime, in contrast to static privileges, which are built in to the server. The following list describes each dynamic privilege available in MySQL.

Most dynamic privileges are defined at server startup. Others are defined by a particular component or plugin, as indicated in the privilege descriptions. In such cases, the privilege is unavailable unless the component or plugin that defines it is enabled.

Particular SQL statements might have more specific privilege requirements than indicated here. If so, the description for the statement in question provides the details.

### <span id="page-180-1"></span>• [ALLOW\\_NONEXISTENT\\_DEFINER](#page-180-1)

Enables overriding security checks designed to prevent operations that (perhaps inadvertently) cause stored objects to become orphaned or that cause adoption of stored objects that are currently orphaned. Without this privilege, any attempt to produce an orphaned SQL procedure, function, or view results in an error. An attempt to produce orphaned objects using CREATE PROCEDURE, CREATE FUNCTION, CREATE TRIGGER, CREATE EVENT, or CREATE VIEW also requires [SET\\_ANY\\_DEFINER](#page-185-1) in addition to [ALLOW\\_NONEXISTENT\\_DEFINER](#page-180-1), so that a definer different from the current user is permissible.

For details, see Orphan Stored Objects.

### <span id="page-180-2"></span>• [APPLICATION\\_PASSWORD\\_ADMIN](#page-180-2)

For dual-password capability, this privilege enables use of the RETAIN CURRENT PASSWORD and DISCARD OLD PASSWORD clauses for ALTER USER and SET PASSWORD statements that apply to your own account. This privilege is required to manipulate your own secondary password because most users require only one password.

If an account is to be permitted to manipulate secondary passwords for all accounts, it should be granted the [CREATE USER](#page-174-8) privilege rather than [APPLICATION\\_PASSWORD\\_ADMIN](#page-180-2).

For more information about use of dual passwords, see Section 8.2.15, "Password Management".

#### <span id="page-180-3"></span>• [AUDIT\\_ABORT\\_EXEMPT](#page-180-3)

Allows queries blocked by an "abort" item in the audit log filter. This privilege is defined by the audit\_log plugin; see Section 8.4.5, "MySQL Enterprise Audit".

Accounts created with the [SYSTEM\\_USER](#page-185-3) privilege have the [AUDIT\\_ABORT\\_EXEMPT](#page-180-3) privilege assigned automatically when they are created. The [AUDIT\\_ABORT\\_EXEMPT](#page-180-3) privilege is also assigned to existing accounts with the [SYSTEM\\_USER](#page-185-3) privilege when you carry out an upgrade procedure, if no existing accounts have that privilege assigned. Accounts with the [SYSTEM\\_USER](#page-185-3) privilege can therefore be used to regain access to a system following an audit misconfiguration.

#### <span id="page-180-4"></span>• [AUDIT\\_ADMIN](#page-180-4)

Enables audit log configuration. This privilege is defined by the audit\_log plugin; see Section 8.4.5, "MySQL Enterprise Audit".

### <span id="page-180-0"></span>• [BACKUP\\_ADMIN](#page-180-0)

Enables execution of the LOCK INSTANCE FOR BACKUP statement and access to the Performance Schema log\_status table.

![](_page_180_Picture_15.jpeg)

#### **Note**

Besides [BACKUP\\_ADMIN](#page-180-0), the [SELECT](#page-177-2) privilege on the log\_status table is also needed for its access.

The [BACKUP\\_ADMIN](#page-180-0) privilege is automatically granted to users with the [RELOAD](#page-176-0) privilege when performing an in-place upgrade to MySQL 8.4 from an earlier version.

#### <span id="page-180-5"></span>• [AUTHENTICATION\\_POLICY\\_ADMIN](#page-180-5)

The authentication\_policy system variable places certain constraints on how the authentication-related clauses of CREATE USER and ALTER USER statements may be used. A user who has the [AUTHENTICATION\\_POLICY\\_ADMIN](#page-180-5) privilege is not subject to these constraints. (A warning does occur for statements that otherwise would not be permitted.)

For details about the constraints imposed by authentication\_policy, see the description of that variable.

<span id="page-181-2"></span>• [BINLOG\\_ADMIN](#page-181-2)

Enables binary log control by means of the PURGE BINARY LOGS and BINLOG statements.

<span id="page-181-3"></span>• [BINLOG\\_ENCRYPTION\\_ADMIN](#page-181-3)

Enables setting the system variable binlog\_encryption, which activates or deactivates encryption for binary log files and relay log files. This ability is not provided by the [BINLOG\\_ADMIN](#page-181-2), [SYSTEM\\_VARIABLES\\_ADMIN](#page-186-1), or [SESSION\\_VARIABLES\\_ADMIN](#page-184-5) privileges. The related system variable binlog\_rotate\_encryption\_master\_key\_at\_startup, which rotates the binary log master key automatically when the server is restarted, does not require this privilege.

<span id="page-181-0"></span>• [CLONE\\_ADMIN](#page-181-0)

Enables execution of the CLONE statements. Includes [BACKUP\\_ADMIN](#page-180-0) and [SHUTDOWN](#page-177-0) privileges.

<span id="page-181-1"></span>• [CONNECTION\\_ADMIN](#page-181-1)

Enables use of the KILL statement or mysqladmin kill command to kill threads belonging to other accounts. (An account can always kill its own threads.)

Enables setting system variables related to client connections, or circumventing restrictions related to client connections. [CONNECTION\\_ADMIN](#page-181-1) is required to activate MySQL Server's offline mode, which is done by changing the value of the offline\_mode system variable to ON.

The [CONNECTION\\_ADMIN](#page-181-1) privilege enables administrators with it to bypass effects of these system variables:

- init\_connect: The server does not execute init\_connect system variable content when [CONNECTION\\_ADMIN](#page-181-1) clients connect.
- max\_connections: The server accepts one connection from a [CONNECTION\\_ADMIN](#page-181-1) client even if the connection limit configured by the max\_connections system variable is reached.
- offline\_mode: A server in offline mode (offline\_mode enabled) does not terminate [CONNECTION\\_ADMIN](#page-181-1) client connections at the next client request, and accepts new connections from [CONNECTION\\_ADMIN](#page-181-1) clients.
- read\_only: Updates from [CONNECTION\\_ADMIN](#page-181-1) clients can be performed even when the read\_only system variable is enabled. This applies to explicit table updates, and to account management statements such as GRANT and REVOKE that update tables implicitly.

Group Replication group members need the [CONNECTION\\_ADMIN](#page-181-1) privilege so that Group Replication connections are not terminated if one of the servers involved is placed in offline mode. If the MySQL communication stack is in use (group\_replication\_communication\_stack = MYSQL), without this privilege, a member that is placed in offline mode is expelled from the group.

<span id="page-181-4"></span>• [ENCRYPTION\\_KEY\\_ADMIN](#page-181-4)

Enables InnoDB encryption key rotation.

<span id="page-181-5"></span>• [FIREWALL\\_ADMIN](#page-181-5)

Enables a user to administer firewall rules for any user. This privilege is defined by the MYSQL\_FIREWALL plugin; see Section 8.4.7, "MySQL Enterprise Firewall".

<span id="page-181-6"></span>• [FIREWALL\\_EXEMPT](#page-181-6)

A user with this privilege is exempt from firewall restrictions. This privilege is defined by the MYSQL\_FIREWALL plugin; see Section 8.4.7, "MySQL Enterprise Firewall".

<span id="page-181-7"></span>• [FIREWALL\\_USER](#page-181-7)

Enables users to update their own firewall rules. This privilege is defined by the MYSQL\_FIREWALL plugin; see Section 8.4.7, "MySQL Enterprise Firewall".

<span id="page-182-0"></span>• [FLUSH\\_OPTIMIZER\\_COSTS](#page-182-0)

Enables use of the FLUSH OPTIMIZER\_COSTS statement.

<span id="page-182-1"></span>• [FLUSH\\_PRIVILEGES](#page-182-1)

Enables use of the FLUSH PRIVILEGES statement.

<span id="page-182-2"></span>• [FLUSH\\_STATUS](#page-182-2)

Enables use of the FLUSH STATUS statement.

<span id="page-182-3"></span>• [FLUSH\\_TABLES](#page-182-3)

Enables use of the FLUSH TABLES statement.

<span id="page-182-4"></span>• [FLUSH\\_USER\\_RESOURCES](#page-182-4)

Enables use of the FLUSH USER\_RESOURCES statement.

<span id="page-182-5"></span>• [GROUP\\_REPLICATION\\_ADMIN](#page-182-5)

Enables the account to start and stop Group Replication using the START GROUP REPLICATION and STOP GROUP REPLICATION statements, to change the global setting for the group\_replication\_consistency system variable, and to use the group\_replication\_set\_write\_concurrency() and group\_replication\_set\_communication\_protocol() functions. Grant this privilege to accounts that are used to administer servers that are members of a replication group.

<span id="page-182-6"></span>• [GROUP\\_REPLICATION\\_STREAM](#page-182-6)

Allows a user account to be used for establishing Group Replication's group communication connections. It must be granted to a recovery user when the MySQL communication stack is used for Group Replication (group\_replication\_communication\_stack=MYSQL).

<span id="page-182-7"></span>• [INNODB\\_REDO\\_LOG\\_ARCHIVE](#page-182-7)

Enables the account to activate and deactivate redo log archiving.

<span id="page-182-8"></span>• [INNODB\\_REDO\\_LOG\\_ENABLE](#page-182-8)

Enables use of the ALTER INSTANCE {ENABLE|DISABLE} INNODB REDO\_LOG statement to enable or disable redo logging.

See Disabling Redo Logging.

<span id="page-182-9"></span>• [MASKING\\_DICTIONARIES\\_ADMIN](#page-182-9)

Enables the account to add and remove dictionary terms using the masking\_dictionary\_term\_add() and masking\_dictionary\_term\_remove() component functions. Accounts also require this dynamic privilege to remove a full dictionary using the masking\_dictionary\_remove() function, which removes all of the terms associated with the named dictionary currently in the mysql.masking\_dictionaries table.

See Section 8.5, "MySQL Enterprise Data Masking and De-Identification".

### <span id="page-183-0"></span>• [NDB\\_STORED\\_USER](#page-183-0)

Enables the user or role and its privileges to be shared and synchronized between all NDB-enabled MySQL servers as soon as they join a given NDB Cluster. This privilege is available only if the NDB storage engine is enabled.

Any changes to or revocations of privileges made for the given user or role are synchronized immediately with all connected MySQL servers (SQL nodes). You should be aware that there is no guarantee that multiple statements affecting privileges originating from different SQL nodes are executed on all SQL nodes in the same order. For this reason, it is highly recommended that all user administration be done from a single designated SQL node.

NDB\_STORED\_USER is a global privilege and must be granted or revoked using ON \*.\*. Trying to set any other scope for this privilege results in an error. This privilege can be given to most application and administrative users, but it cannot be granted to system reserved accounts such as mysql.session@localhost or mysql.infoschema@localhost.

A user that has been granted the NDB\_STORED\_USER privilege is stored in NDB (and thus shared by all SQL nodes), as is a role with this privilege. A user that is merely granted a role that has NDB\_STORED\_USER is not stored in NDB; each NDB stored user must be granted the privilege explicitly.

For more detailed information about how this works in NDB, see Section 25.6.13, "Privilege Synchronization and NDB\_STORED\_USER".

<span id="page-183-1"></span>• [OPTIMIZE\\_LOCAL\\_TABLE](#page-183-1)

Enables use of OPTIMIZE LOCAL TABLE and OPTIMIZE NO\_WRITE\_TO\_BINLOG TABLE statements.

<span id="page-183-2"></span>• [PASSWORDLESS\\_USER\\_ADMIN](#page-183-2)

This privilege applies to passwordless user accounts:

- For account creation, a user who executes CREATE USER to create a passwordless account must possess the [PASSWORDLESS\\_USER\\_ADMIN](#page-183-2) privilege.
- In replication context, the [PASSWORDLESS\\_USER\\_ADMIN](#page-183-2) privilege applies to replication users and enables replication of ALTER USER ... MODIFY statements for user accounts that are configured for passwordless authentication.

For information about passwordless authentication, see WebAuthn Passwordless Authentication.

<span id="page-183-3"></span>• [PERSIST\\_RO\\_VARIABLES\\_ADMIN](#page-183-3)

For users who also have [SYSTEM\\_VARIABLES\\_ADMIN](#page-186-1), [PERSIST\\_RO\\_VARIABLES\\_ADMIN](#page-183-3) enables use of SET PERSIST\_ONLY to persist global system variables to the mysqld-auto.cnf option file in the data directory. This statement is similar to SET PERSIST but does not modify the runtime global system variable value. This makes SET PERSIST\_ONLY suitable for configuring read-only system variables that can be set only at server startup.

See also Section 7.1.9.1, "System Variable Privileges".

<span id="page-183-4"></span>• [REPLICATION\\_APPLIER](#page-183-4)

Enables the account to act as the PRIVILEGE\_CHECKS\_USER for a replication channel, and to execute BINLOG statements in mysqlbinlog output. Grant this privilege to accounts that are assigned using CHANGE REPLICATION SOURCE TO to provide a security context for replication channels, and to handle replication errors on those channels. As well as the REPLICATION\_APPLIER privilege, you must also give the account the required privileges to execute the transactions received by the replication channel or contained in the mysqlbinlog output,

for example to update the affected tables. For more information, see Section 19.3.3, "Replication Privilege Checks".

<span id="page-184-1"></span>• [REPLICATION\\_SLAVE\\_ADMIN](#page-184-1)

Enables the account to connect to the replication source server, start and stop replication using the START REPLICA and STOP REPLICA statements, and use the CHANGE REPLICATION SOURCE TO and CHANGE REPLICATION FILTER statements. Grant this privilege to accounts that are used by replicas to connect to the current server as their replication source server. This privilege does not apply to Group Replication; use GROUP\_REPLICATION\_ADMIN for that.

<span id="page-184-2"></span>• [RESOURCE\\_GROUP\\_ADMIN](#page-184-2)

Enables resource group management, consisting of creating, altering, and dropping resource groups, and assignment of threads and statements to resource groups. A user with this privilege can perform any operation relating to resource groups.

<span id="page-184-3"></span>• [RESOURCE\\_GROUP\\_USER](#page-184-3)

Enables assigning threads and statements to resource groups. A user with this privilege can use the SET RESOURCE GROUP statement and the RESOURCE\_GROUP optimizer hint.

<span id="page-184-4"></span>• [ROLE\\_ADMIN](#page-184-4)

Enables granting and revoking roles, use of the WITH ADMIN OPTION clause of the GRANT statement, and nonempty <graphml> element content in the result from the ROLES\_GRAPHML() function. Required to set the value of the mandatory\_roles system variable.

<span id="page-184-0"></span>• [SENSITIVE\\_VARIABLES\\_OBSERVER](#page-184-0)

Enables a holder to view the values of sensitive system variables in the Performance Schema tables global\_variables, session\_variables, variables\_by\_thread, and persisted\_variables, to issue SELECT statements to return their values, and to track changes to them in session trackers for connections. Users without this privilege cannot view or track those system variable values. See Persisting Sensitive System Variables.

<span id="page-184-6"></span>• [SERVICE\\_CONNECTION\\_ADMIN](#page-184-6)

Enables connections to the network interface that permits only administrative connections (see Section 7.1.12.1, "Connection Interfaces").

<span id="page-184-5"></span>• [SESSION\\_VARIABLES\\_ADMIN](#page-184-5)

For most system variables, setting the session value requires no special privileges and can be done by any user to affect the current session. For some system variables, setting the session value can have effects outside the current session and thus is a restricted operation. For these, the [SESSION\\_VARIABLES\\_ADMIN](#page-184-5) privilege enables the user to set the session value.

If a system variable is restricted and requires a special privilege to set the session value, the variable description indicates that restriction. Examples include binlog\_format, sql\_log\_bin, and sql\_log\_off.

The [SESSION\\_VARIABLES\\_ADMIN](#page-184-5) privilege is a subset of the [SYSTEM\\_VARIABLES\\_ADMIN](#page-186-1) and [SUPER](#page-177-1) privileges. A user who has either of those privileges is also permitted to set restricted session variables and effectively has [SESSION\\_VARIABLES\\_ADMIN](#page-184-5) by implication and need not be granted [SESSION\\_VARIABLES\\_ADMIN](#page-184-5) explicitly.

See also Section 7.1.9.1, "System Variable Privileges".

### <span id="page-185-1"></span>• [SET\\_ANY\\_DEFINER](#page-185-1)

Enables setting the effective authorization ID when executing a view or stored program. A user with this privilege can specify any account as the DEFINER attribute for CREATE PROCEDURE, CREATE FUNCTION, CREATE TRIGGER, CREATE EVENT, ALTER EVENT, CREATE VIEW, and ALTER VIEW. Without this privilege, only the effective authentication ID can be specified.

Stored programs execute with the privileges of the specified account, so ensure that you follow the risk minimization guidelines listed in Section 27.6, "Stored Object Access Control".

#### <span id="page-185-2"></span>• [SHOW\\_ROUTINE](#page-185-2)

Enables a user to access definitions and properties of all stored routines (stored procedures and functions), even those for which the user is not named as the routine DEFINER. This access includes:

- The contents of the Information Schema ROUTINES table.
- The SHOW CREATE FUNCTION and SHOW CREATE PROCEDURE statements.
- The SHOW FUNCTION CODE and SHOW PROCEDURE CODE statements.
- The SHOW FUNCTION STATUS and SHOW PROCEDURE STATUS statements.

[SHOW\\_ROUTINE](#page-185-2) may be granted instead as a privilege with a more restricted scope that permits access to routine definitions. (That is, an administrator can rescind global [SELECT](#page-177-2) from users that do not otherwise require it and grant [SHOW\\_ROUTINE](#page-185-2) instead.) This enables an account to back up stored routines without requiring a broad privilege.

#### <span id="page-185-0"></span>• [SKIP\\_QUERY\\_REWRITE](#page-185-0)

Queries issued by a user with this privilege are not subject to being rewritten by the Rewriter plugin (see [Section 7.6.4, "The Rewriter Query Rewrite Plugin"\)](#page-76-0).

This privilege should be granted to users issuing administrative or control statements that should not be rewritten, as well as to PRIVILEGE\_CHECKS\_USER accounts (see Section 19.3.3, "Replication Privilege Checks") used to apply statements from a replication source.

<span id="page-185-3"></span>• [SYSTEM\\_USER](#page-185-3)

The [SYSTEM\\_USER](#page-185-3) privilege distinguishes system users from regular users:

- A user with the [SYSTEM\\_USER](#page-185-3) privilege is a system user.
- A user without the [SYSTEM\\_USER](#page-185-3) privilege is a regular user.

The [SYSTEM\\_USER](#page-185-3) privilege has an effect on the accounts to which a given user can apply its other privileges, as well as whether the user is protected from other accounts:

- A system user can modify both system and regular accounts. That is, a user who has the appropriate privileges to perform a given operation on regular accounts is enabled by possession of [SYSTEM\\_USER](#page-185-3) to also perform the operation on system accounts. A system account can be modified only by system users with appropriate privileges, not by regular users.
- A regular user with appropriate privileges can modify regular accounts, but not system accounts. A regular account can be modified by both system and regular users with appropriate privileges.

This also means that database objects created by users with the [SYSTEM\\_USER](#page-185-3) privilege cannot be modified or dropped by users without the privilege. This also applies to routines for which the definer has this privilege.

For more information, see Section 8.2.11, "Account Categories".

The protection against modification by regular accounts that is afforded to system accounts by the [SYSTEM\\_USER](#page-185-3) privilege does not apply to regular accounts that have privileges on the mysql system schema and thus can directly modify the grant tables in that schema. For full protection, do not grant mysql schema privileges to regular accounts. See Protecting System Accounts Against Manipulation by Regular Accounts.

If the audit\_log plugin is in use (see Section 8.4.5, "MySQL Enterprise Audit"), accounts with the [SYSTEM\\_USER](#page-185-3) privilege are automatically assigned the [AUDIT\\_ABORT\\_EXEMPT](#page-180-3) privilege, which permits their queries to be executed even if an "abort" item configured in the filter would block them. Accounts with the [SYSTEM\\_USER](#page-185-3) privilege can therefore be used to regain access to a system following an audit misconfiguration.

<span id="page-186-1"></span>• [SYSTEM\\_VARIABLES\\_ADMIN](#page-186-1)

Affects the following operations and server behaviors:

- Enables system variable changes at runtime:
  - Enables server configuration changes to global system variables with SET GLOBAL and SET PERSIST.
  - Enables server configuration changes to global system variables with SET PERSIST\_ONLY, if the user also has [PERSIST\\_RO\\_VARIABLES\\_ADMIN](#page-183-3).
  - Enables setting restricted session system variables that require a special privilege. In effect, [SYSTEM\\_VARIABLES\\_ADMIN](#page-186-1) implies [SESSION\\_VARIABLES\\_ADMIN](#page-184-5) without explicitly granting [SESSION\\_VARIABLES\\_ADMIN](#page-184-5).

See also Section 7.1.9.1, "System Variable Privileges".

- Enables changes to global transaction characteristics (see Section 15.3.7, "SET TRANSACTION Statement").
- <span id="page-186-2"></span>• [TABLE\\_ENCRYPTION\\_ADMIN](#page-186-2)

Enables a user to override default encryption settings when table\_encryption\_privilege\_check is enabled; see Defining an Encryption Default for Schemas and General Tablespaces.

<span id="page-186-3"></span>• [TELEMETRY\\_LOG\\_ADMIN](#page-186-3)

Enables telemetry log configuration. This privilege is defined by the telemetry\_log plugin, which is deployed through MySQL HeatWave on AWS.

<span id="page-186-0"></span>• [TP\\_CONNECTION\\_ADMIN](#page-186-0)

Enables connecting to the server with a privileged connection. When the limit defined by thread\_pool\_max\_transactions\_limit has been reached, new connections are not permitted, unless overridden by thread\_pool\_longrun\_trx\_limit. A privileged connection ignores the transaction limit and permits connecting to the server to increase the transaction limit, remove the limit, or kill running transactions. This privilege is not granted to any user by default. To establish a privileged connection, the user initiating a connection must have the [TP\\_CONNECTION\\_ADMIN](#page-186-0) privilege.

A privileged connection can execute statements and start transactions when the limit defined by thread\_pool\_max\_transactions\_limit has been reached. A privileged connection is placed in the Admin thread group. See [Privileged Connections](#page-74-1).

## <span id="page-187-2"></span>• [TRANSACTION\\_GTID\\_TAG](#page-187-2)

Required for setting the gtid\_next system variable to AUTOMATIC:TAG or UUID:TAG:NUMBER on a replication source server. In addition, at least one of [SYSTEM\\_VARIABLES\\_ADMIN](#page-186-1), [SESSION\\_VARIABLES\\_ADMIN](#page-184-5), or [REPLICATION\\_APPLIER](#page-183-4) is also required to set gtid\_next to one of these values on the source.

The REPLICATION\_CHECKS\_APPLIER must also have this privilege as well as the REPLICATION\_APPLIER privilege to set gtid\_next to AUTOMATIC:TAG. This is checked when starting the replication applier thread.

This privilege is also required to set the gtid\_purged server system variable.

For more information about using tagged GTIDs, see the description of gtid\_next, as well as Section 19.1.4, "Changing GTID Mode on Online Servers".

<span id="page-187-0"></span>• [VERSION\\_TOKEN\\_ADMIN](#page-187-0)

Enables execution of Version Tokens functions. This privilege is defined by the version\_tokens plugin; see [Section 7.6.6, "Version Tokens"](#page-87-0).

<span id="page-187-3"></span>• [XA\\_RECOVER\\_ADMIN](#page-187-3)

Enables execution of the XA RECOVER statement; see Section 15.3.8.1, "XA Transaction SQL Statements".

Prior to MySQL 8.4, any user could execute the XA RECOVER statement to discover the XID values for outstanding prepared XA transactions, possibly leading to commit or rollback of an XA transaction by a user other than the one who started it. In MySQL 8.4, XA RECOVER is permitted only to users who have the [XA\\_RECOVER\\_ADMIN](#page-187-3) privilege, which is expected to be granted only to administrative users who have need for it. This might be the case, for example, for administrators of an XA application if it has crashed and it is necessary to find outstanding transactions started by the application so they can be rolled back. This privilege requirement prevents users from discovering the XID values for outstanding prepared XA transactions other than their own. It does not affect normal commit or rollback of an XA transaction because the user who started it knows its XID.

## <span id="page-187-1"></span>**Privilege-Granting Guidelines**

It is a good idea to grant to an account only those privileges that it needs. You should exercise particular caution in granting the [FILE](#page-175-2) and administrative privileges:

- [FILE](#page-175-2) can be abused to read into a database table any files that the MySQL server can read on the server host. This includes all world-readable files and files in the server's data directory. The table can then be accessed using SELECT to transfer its contents to the client host.
- [GRANT OPTION](#page-175-6) enables users to give their privileges to other users. Two users that have different privileges and with the [GRANT OPTION](#page-175-6) privilege are able to combine privileges.
- [ALTER](#page-173-2) may be used to subvert the privilege system by renaming tables.
- [SHUTDOWN](#page-177-0) can be abused to deny service to other users entirely by terminating the server.
- [PROCESS](#page-175-3) can be used to view the plain text of currently executing statements, including statements that set or change passwords.
- [SUPER](#page-177-1) can be used to terminate other sessions or change how the server operates.
- Privileges granted for the mysql system database itself can be used to change passwords and other access privilege information:
  - Passwords are stored encrypted, so a malicious user cannot simply read them to know the plain text password. However, a user with write access to the mysql.user system table

authentication\_string column can change an account's password, and then connect to the MySQL server using that account.

- [INSERT](#page-175-0) or [UPDATE](#page-179-2) granted for the mysql system database enable a user to add privileges or modify existing privileges, respectively.
- [DROP](#page-174-1) for the mysql system database enables a user to remote privilege tables, or even the database itself.

# <span id="page-188-0"></span>**Static Versus Dynamic Privileges**

MySQL supports static and dynamic privileges:

- Static privileges are built in to the server. They are always available to be granted to user accounts and cannot be unregistered.
- Dynamic privileges can be registered and unregistered at runtime. This affects their availability: A dynamic privilege that has not been registered cannot be granted.

For example, the [SELECT](#page-177-2) and [INSERT](#page-175-0) privileges are static and always available, whereas a dynamic privilege becomes available only if the component that implements it has been enabled.

The remainder of this section describes how dynamic privileges work in MySQL. The discussion uses the term "components" but applies equally to plugins.

![](_page_188_Picture_10.jpeg)

#### **Note**

Server administrators should be aware of which server components define dynamic privileges. For MySQL distributions, documentation of components that define dynamic privileges describes those privileges.

Third-party components may also define dynamic privileges; an administrator should understand those privileges and not install components that might conflict or compromise server operation. For example, one component conflicts with another if both define a privilege with the same name. Component developers can reduce the likelihood of this occurrence by choosing privilege names having a prefix based on the component name.

The server maintains the set of registered dynamic privileges internally in memory. Unregistration occurs at server shutdown.

Normally, a component that defines dynamic privileges registers them when it is installed, during its initialization sequence. When uninstalled, a component does not unregister its registered dynamic privileges. (This is current practice, not a requirement. That is, components could, but do not, unregister at any time privileges they register.)

No warning or error occurs for attempts to register an already registered dynamic privilege. Consider the following sequence of statements:

```
INSTALL COMPONENT 'my_component';
UNINSTALL COMPONENT 'my_component';
INSTALL COMPONENT 'my_component';
```

The first INSTALL COMPONENT statement registers any privileges defined by component my\_component, but UNINSTALL COMPONENT does not unregister them. For the second INSTALL COMPONENT statement, the component privileges it registers are found to be already registered, but no warnings or errors occur.

Dynamic privileges apply only at the global level. The server stores information about current assignments of dynamic privileges to user accounts in the mysql.global\_grants system table:

• The server automatically registers privileges named in global\_grants during server startup (unless the --skip-grant-tables option is given).

- The GRANT and REVOKE statements modify the contents of global\_grants.
- Dynamic privilege assignments listed in global\_grants are persistent. They are not removed at server shutdown.

Example: The following statement grants to user u1 the privileges required to control replication (including Group Replication) on a replica, and to modify system variables:

```
GRANT REPLICATION_SLAVE_ADMIN, GROUP_REPLICATION_ADMIN, BINLOG_ADMIN
ON *.* TO 'u1'@'localhost';
```

Granted dynamic privileges appear in the output from the SHOW GRANTS statement and the INFORMATION\_SCHEMA USER\_PRIVILEGES table.

For GRANT and REVOKE at the global level, any named privileges not recognized as static are checked against the current set of registered dynamic privileges and granted if found. Otherwise, an error occurs to indicate an unknown privilege identifier.

For GRANT and REVOKE the meaning of ALL [PRIVILEGES] at the global level includes all static global privileges, as well as all currently registered dynamic privileges:

- GRANT ALL at the global level grants all static global privileges and all currently registered dynamic privileges. A dynamic privilege registered subsequent to execution of the GRANT statement is not granted retroactively to any account.
- REVOKE ALL at the global level revokes all granted static global privileges and all granted dynamic privileges.

The FLUSH PRIVILEGES statement reads the global\_grants table for dynamic privilege assignments and registers any unregistered privileges found there.

For descriptions of the dynamic privileges provided by MySQL Server and components included in MySQL distributions, see [Section 8.2.2, "Privileges Provided by MySQL".](#page-170-0)

## <span id="page-189-0"></span>**Migrating Accounts from SUPER to Dynamic Privileges**

In MySQL 8.4, many operations that previously required the [SUPER](#page-177-1) privilege are also associated with a dynamic privilege of more limited scope. (For descriptions of these privileges, see [Section 8.2.2,](#page-170-0) ["Privileges Provided by MySQL".](#page-170-0)) Each such operation can be permitted to an account by granting the associated dynamic privilege rather than [SUPER](#page-177-1). This change improves security by enabling DBAs to avoid granting [SUPER](#page-177-1) and tailor user privileges more closely to the operations permitted. [SUPER](#page-177-1) is now deprecated; expect it to be removed in a future version of MySQL.

When removal of [SUPER](#page-177-1) occurs, operations that formerly required [SUPER](#page-177-1) fail unless accounts granted [SUPER](#page-177-1) are migrated to the appropriate dynamic privileges. Use the following instructions to accomplish that goal so that accounts are ready prior to [SUPER](#page-177-1) removal:

1. Execute this query to identify accounts that are granted [SUPER](#page-177-1):

```
SELECT GRANTEE FROM INFORMATION_SCHEMA.USER_PRIVILEGES
WHERE PRIVILEGE_TYPE = 'SUPER';
```

2. For each account identified by the preceding query, determine the operations for which it needs [SUPER](#page-177-1). Then grant the dynamic privileges corresponding to those operations, and revoke [SUPER](#page-177-1).

For example, if 'u1'@'localhost' requires [SUPER](#page-177-1) for binary log purging and system variable modification, these statements make the required changes to the account:

```
GRANT BINLOG_ADMIN, SYSTEM_VARIABLES_ADMIN ON *.* TO 'u1'@'localhost';
REVOKE SUPER ON *.* FROM 'u1'@'localhost';
```

After you have modified all applicable accounts, the INFORMATION\_SCHEMA query in the first step should produce an empty result set.

# <span id="page-190-0"></span>**8.2.3 Grant Tables**

The mysql system database includes several grant tables that contain information about user accounts and the privileges held by them. This section describes those tables. For information about other tables in the system database, see [Section 7.3, "The mysql System Schema"](#page-6-0).

The discussion here describes the underlying structure of the grant tables and how the server uses their contents when interacting with clients. However, normally you do not modify the grant tables directly. Modifications occur indirectly when you use account-management statements such as CREATE USER, GRANT, and REVOKE to set up accounts and control the privileges available to each one. See Section 15.7.1, "Account Management Statements". When you use such statements to perform account manipulations, the server modifies the grant tables on your behalf.

![](_page_190_Picture_4.jpeg)

#### **Note**

Direct modification of grant tables using statements such as INSERT, UPDATE, or DELETE is discouraged and done at your own risk. The server is free to ignore rows that become malformed as a result of such modifications.

For any operation that modifies a grant table, the server checks whether the table has the expected structure and produces an error if not. To update the tables to the expected structure, perform the MySQL upgrade procedure. See Chapter 3, Upgrading MySQL.

- [Grant Table Overview](#page-190-1)
- [The user and db Grant Tables](#page-192-0)
- [The tables\\_priv and columns\\_priv Grant Tables](#page-196-0)
- [The procs\\_priv Grant Table](#page-196-1)
- [The proxies\\_priv Grant Table](#page-196-2)
- [The global\\_grants Grant Table](#page-197-0)
- [The default\\_roles Grant Table](#page-197-1)
- [The role\\_edges Grant Table](#page-197-2)
- [The password\\_history Grant Table](#page-197-3)
- [Grant Table Scope Column Properties](#page-198-0)
- [Grant Table Privilege Column Properties](#page-198-1)
- [Grant Table Concurrency](#page-199-1)

## <span id="page-190-1"></span>**Grant Table Overview**

These mysql database tables contain grant information:

- [user](#page-192-0): User accounts, static global privileges, and other nonprivilege columns.
- [global\\_grants](#page-197-0): Dynamic global privileges.
- [db](#page-192-0): Database-level privileges.
- [tables\\_priv](#page-196-0): Table-level privileges.
- [columns\\_priv](#page-196-0): Column-level privileges.
- [procs\\_priv](#page-196-1): Stored procedure and function privileges.

- [proxies\\_priv](#page-196-2): Proxy-user privileges.
- [default\\_roles](#page-197-1): Default user roles.
- [role\\_edges](#page-197-2): Edges for role subgraphs.
- [password\\_history](#page-197-3): Password change history.

For information about the differences between static and dynamic global privileges, see [Static Versus](#page-188-0) [Dynamic Privileges](#page-188-0).)

Grant tables use the InnoDB storage engine and are transactional. Each statement either succeeds for all named users or rolls back and has no effect if any error occurs.

Each grant table contains scope columns and privilege columns:

- Scope columns determine the scope of each row in the tables; that is, the context in which the row applies. For example, a user table row with Host and User values of 'h1.example.net' and 'bob' applies to authenticating connections made to the server from the host h1.example.net by a client that specifies a user name of bob. Similarly, a db table row with Host, User, and Db column values of 'h1.example.net', 'bob' and 'reports' applies when bob connects from the host h1.example.net to access the reports database. The tables\_priv and columns\_priv tables contain scope columns indicating tables or table/column combinations to which each row applies. The procs\_priv scope columns indicate the stored routine to which each row applies.
- Privilege columns indicate which privileges a table row grants; that is, which operations it permits to be performed. The server combines the information in the various grant tables to form a complete description of a user's privileges. Section 8.2.7, "Access Control, Stage 2: Request Verification", describes the rules for this.

In addition, a grant table may contain columns used for purposes other than scope or privilege assessment.

The server uses the grant tables in the following manner:

• The user table scope columns determine whether to reject or permit incoming connections. For permitted connections, any privileges granted in the user table indicate the user's static global privileges. Any privileges granted in this table apply to all databases on the server.

![](_page_191_Picture_13.jpeg)

### **Caution**

Because any static global privilege is considered a privilege for all databases, any static global privilege enables a user to see all database names with SHOW DATABASES or by examining the SCHEMATA table of INFORMATION\_SCHEMA, except databases that have been restricted at the database level by partial revokes.

- The global\_grants table lists current assignments of dynamic global privileges to user accounts. For each row, the scope columns determine which user has the privilege named in the privilege column.
- The db table scope columns determine which users can access which databases from which hosts. The privilege columns determine the permitted operations. A privilege granted at the database level applies to the database and to all objects in the database, such as tables and stored programs.
- The tables\_priv and columns\_priv tables are similar to the db table, but are more fine-grained: They apply at the table and column levels rather than at the database level. A privilege granted at the table level applies to the table and to all its columns. A privilege granted at the column level applies only to a specific column.
- The procs\_priv table applies to stored routines (stored procedures and functions). A privilege granted at the routine level applies only to a single procedure or function.

- The proxies\_priv table indicates which users can act as proxies for other users and whether a user can grant the [PROXY](#page-176-1) privilege to other users.
- The default\_roles and role\_edges tables contain information about role relationships.
- The password\_history table retains previously chosen passwords to enable restrictions on password reuse. See Section 8.2.15, "Password Management".

The server reads the contents of the grant tables into memory when it starts. You can tell it to reload the tables by issuing a FLUSH PRIVILEGES statement or executing a mysqladmin flushprivileges or mysqladmin reload command. Changes to the grant tables take effect as indicated in Section 8.2.13, "When Privilege Changes Take Effect".

When you modify an account, it is a good idea to verify that your changes have the intended effect. To check the privileges for a given account, use the SHOW GRANTS statement. For example, to determine the privileges that are granted to an account with user name and host name values of bob and pc84.example.com, use this statement:

```
SHOW GRANTS FOR 'bob'@'pc84.example.com';
```

To display nonprivilege properties of an account, use SHOW CREATE USER:

SHOW CREATE USER 'bob'@'pc84.example.com';

## <span id="page-192-0"></span>**The user and db Grant Tables**

The server uses the user and db tables in the mysql database at both the first and second stages of access control (see [Section 8.2, "Access Control and Account Management"](#page-168-0)). The columns in the user and db tables are shown here.

**Table 8.4 user and db Table Columns**

| Table Name        | user                  | db                    |
|-------------------|-----------------------|-----------------------|
| Scope columns     | Host                  | Host                  |
|                   | User                  | Db                    |
|                   |                       | User                  |
| Privilege columns | Select_priv           | Select_priv           |
|                   | Insert_priv           | Insert_priv           |
|                   | Update_priv           | Update_priv           |
|                   | Delete_priv           | Delete_priv           |
|                   | Index_priv            | Index_priv            |
|                   | Alter_priv            | Alter_priv            |
|                   | Create_priv           | Create_priv           |
|                   | Drop_priv             | Drop_priv             |
|                   | Grant_priv            | Grant_priv            |
|                   | Create_view_priv      | Create_view_priv      |
|                   | Show_view_priv        | Show_view_priv        |
|                   | Create_routine_priv   | Create_routine_priv   |
|                   | Alter_routine_priv    | Alter_routine_priv    |
|                   | Execute_priv          | Execute_priv          |
|                   | Trigger_priv          | Trigger_priv          |
|                   | Event_priv            | Event_priv            |
|                   | Create_tmp_table_priv | Create_tmp_table_priv |
|                   | Lock_tables_priv      | Lock_tables_priv      |

| Table Name               | user                     | db              |
|--------------------------|--------------------------|-----------------|
|                          | References_priv          | References_priv |
|                          | Reload_priv              |                 |
|                          | Shutdown_priv            |                 |
|                          | Process_priv             |                 |
|                          | File_priv                |                 |
|                          | Show_db_priv             |                 |
|                          | Super_priv               |                 |
|                          | Repl_slave_priv          |                 |
|                          | Repl_client_priv         |                 |
|                          | Create_user_priv         |                 |
|                          | Create_tablespace_priv   |                 |
|                          | Create_role_priv         |                 |
|                          | Drop_role_priv           |                 |
| Security columns         | ssl_type                 |                 |
|                          | ssl_cipher               |                 |
|                          | x509_issuer              |                 |
|                          | x509_subject             |                 |
|                          | plugin                   |                 |
|                          | authentication_string    |                 |
|                          | password_expired         |                 |
|                          | password_last_changed    |                 |
|                          | password_lifetime        |                 |
|                          | account_locked           |                 |
|                          | Password_reuse_history   |                 |
|                          | Password_reuse_time      |                 |
|                          | Password_require_current |                 |
|                          | User_attributes          |                 |
| Resource control columns | max_questions            |                 |
|                          | max_updates              |                 |
|                          | max_connections          |                 |
|                          | max_user_connections     |                 |

The user table plugin and authentication\_string columns store authentication plugin and credential information.

The server uses the plugin named in the plugin column of an account row to authenticate connection attempts for the account.

The plugin column must be nonempty. At startup, and at runtime when FLUSH PRIVILEGES is executed, the server checks user table rows. For any row with an empty plugin column, the server writes a warning to the error log of this form:

```
[Warning] User entry 'user_name'@'host_name' has an empty plugin
value. The user will be ignored and no one can login with this user
anymore.
```

To assign a plugin to an account that is missing one, use the ALTER USER statement.

The password\_expired column permits DBAs to expire account passwords and require users to reset their password. The default password\_expired value is 'N', but can be set to 'Y' with the ALTER USER statement. After an account's password has been expired, all operations performed by the account in subsequent connections to the server result in an error until the user issues an ALTER USER statement to establish a new account password.

![](_page_194_Picture_2.jpeg)

#### **Note**

Although it is possible to "reset" an expired password by setting it to its current value, it is preferable, as a matter of good policy, to choose a different password. DBAs can enforce non-reuse by establishing an appropriate password-reuse policy. See Password Reuse Policy.

password\_last\_changed is a TIMESTAMP column indicating when the password was last changed. The value is non-NULL only for accounts that use a MySQL built-in authentication plugin (mysql\_native\_password which is deprecated, sha256\_password which is deprecated, or caching\_sha2\_password). The value is NULL for other accounts, such as those authenticated using an external authentication system.

password\_last\_changed is updated by the CREATE USER, ALTER USER, and SET PASSWORD statements, and by GRANT statements that create an account or change an account password.

password\_lifetime indicates the account password lifetime, in days. If the password is past its lifetime (assessed using the password\_last\_changed column), the server considers the password expired when clients connect using the account. A value of N greater than zero means that the password must be changed every N days. A value of 0 disables automatic password expiration. If the value is NULL (the default), the global expiration policy applies, as defined by the default\_password\_lifetime system variable.

account\_locked indicates whether the account is locked (see Section 8.2.20, "Account Locking").

Password\_reuse\_history is the value of the PASSWORD HISTORY option for the account, or NULL for the default history.

Password\_reuse\_time is the value of the PASSWORD REUSE INTERVAL option for the account, or NULL for the default interval.

Password\_require\_current corresponds to the value of the PASSWORD REQUIRE option for the account, as shown by the following table.

**Table 8.5 Permitted Password\_require\_current Values**

| Password_require_current Value | Corresponding PASSWORD REQUIRE Option |
|--------------------------------|---------------------------------------|
| 'Y'                            | PASSWORD REQUIRE CURRENT              |
| 'N'                            | PASSWORD REQUIRE CURRENT OPTIONAL     |
| NULL                           | PASSWORD REQUIRE CURRENT DEFAULT      |

User\_attributes is a JSON-format column that stores account attributes not stored in other columns. The INFORMATION\_SCHEMA exposes these attributes through the USER\_ATTRIBUTES table.

The User\_attributes column may contain these attributes:

- additional\_password: The secondary password, if any. See Dual Password Support.
- Restrictions: Restriction lists, if any. Restrictions are added by partial-revoke operations. The attribute value is an array of elements that each have Database and Restrictions keys indicating the name of a restricted database and the applicable restrictions on it (see Section 8.2.12, "Privilege Restriction Using Partial Revokes").
- Password\_locking: The conditions for failed-login tracking and temporary account locking, if any (see Failed-Login Tracking and Temporary Account Locking). The Password\_locking

attribute is updated according to the FAILED\_LOGIN\_ATTEMPTS and PASSWORD\_LOCK\_TIME options of the CREATE USER and ALTER USER statements. The attribute value is a hash with failed\_login\_attempts and password\_lock\_time\_days keys indicating the value of such options as have been specified for the account. If a key is missing, its value is implicitly 0. If a key value is implicitly or explicitly 0, the corresponding capability is disabled.

• multi\_factor\_authentication: Rows in the mysql.user system table have a plugin column that indicates an authentication plugin. For single-factor authentication, that plugin is the only authentication factor. For two-factor or three-factor forms of multifactor authentication, that plugin corresponds to the first authentication factor, but additional information must be stored for the second and third factors. The multi\_factor\_authentication attribute holds this information.

The multi\_factor\_authentication value is an array, where each array element is a hash that describes an authentication factor using these attributes:

- plugin: The name of the authentication plugin.
- authentication\_string: The authentication string value.
- passwordless: A flag that denotes whether the user is meant to be used without a password (with a security token as the only authentication method).
- requires\_registration: a flag that defines whether the user account has registered a security token.

The first and second array elements describe multifactor authentication factors 2 and 3.

If no attributes apply, User\_attributes is NULL.

Example: An account that has a secondary password and partially revoked database privileges has additional\_password and Restrictions attributes in the column value:

```
mysql> SELECT User_attributes FROM mysql.User WHERE User = 'u'\G
*************************** 1. row ***************************
User_attributes: {"Restrictions":
 [{"Database": "mysql", "Privileges": ["SELECT"]}],
 "additional_password": "hashed_credentials"}
```

To determine which attributes are present, use the JSON\_KEYS() function:

```
SELECT User, Host, JSON_KEYS(User_attributes)
FROM mysql.user WHERE User_attributes IS NOT NULL;
```

To extract a particular attribute, such as Restrictions, do this:

```
SELECT User, Host, User_attributes->>'$.Restrictions'
FROM mysql.user WHERE User_attributes->>'$.Restrictions' <> '';
```

Here is an example of the kind of information stored for multi\_factor\_authentication:

```
{
 "multi_factor_authentication": [
 {
 "plugin": "authentication_ldap_simple",
 "passwordless": 0,
 "authentication_string": "ldap auth string",
 "requires_registration": 0
 },
 {
 "plugin": "authentication_webauthn",
 "passwordless": 0,
 "authentication_string": "",
 "requires_registration": 1
 }
 ]
}
```

# <span id="page-196-0"></span>**The tables\_priv and columns\_priv Grant Tables**

During the second stage of access control, the server performs request verification to ensure that each client has sufficient privileges for each request that it issues. In addition to the user and db grant tables, the server may also consult the tables\_priv and columns\_priv tables for requests that involve tables. The latter tables provide finer privilege control at the table and column levels. They have the columns shown in the following table.

**Table 8.6 tables\_priv and columns\_priv Table Columns**

| Table Name        | tables_priv | columns_priv |
|-------------------|-------------|--------------|
| Scope columns     | Host        | Host         |
|                   | Db          | Db           |
|                   | User        | User         |
|                   | Table_name  | Table_name   |
|                   |             | Column_name  |
| Privilege columns | Table_priv  | Column_priv  |
|                   | Column_priv |              |
| Other columns     | Timestamp   | Timestamp    |
|                   | Grantor     |              |

The Timestamp and Grantor columns are set to the current timestamp and the CURRENT\_USER value, respectively, but are otherwise unused.

## <span id="page-196-1"></span>**The procs\_priv Grant Table**

For verification of requests that involve stored routines, the server may consult the procs\_priv table, which has the columns shown in the following table.

**Table 8.7 procs\_priv Table Columns**

| Table Name        | procs_priv   |
|-------------------|--------------|
| Scope columns     | Host         |
|                   | Db           |
|                   | User         |
|                   | Routine_name |
|                   | Routine_type |
| Privilege columns | Proc_priv    |
| Other columns     | Timestamp    |
|                   | Grantor      |

The Routine\_type column is an ENUM column with values of 'FUNCTION' or 'PROCEDURE' to indicate the type of routine the row refers to. This column enables privileges to be granted separately for a function and a procedure with the same name.

The Timestamp and Grantor columns are unused.

## <span id="page-196-2"></span>**The proxies\_priv Grant Table**

The proxies\_priv table records information about proxy accounts. It has these columns:

- Host, User: The proxy account; that is, the account that has the [PROXY](#page-176-1) privilege for the proxied account.
- Proxied\_host, Proxied\_user: The proxied account.

- Grantor, Timestamp: Unused.
- With\_grant: Whether the proxy account can grant the [PROXY](#page-176-1) privilege to other accounts.

For an account to be able to grant the [PROXY](#page-176-1) privilege to other accounts, it must have a row in the proxies\_priv table with With\_grant set to 1 and Proxied\_host and Proxied\_user set to indicate the account or accounts for which the privilege can be granted. For example, the 'root'@'localhost' account created during MySQL installation has a row in the proxies\_priv table that enables granting the [PROXY](#page-176-1) privilege for ''@'', that is, for all users and all hosts. This enables root to set up proxy users, as well as to delegate to other accounts the authority to set up proxy users. See Section 8.2.19, "Proxy Users".

# <span id="page-197-0"></span>**The global\_grants Grant Table**

The global\_grants table lists current assignments of dynamic global privileges to user accounts. The table has these columns:

- USER, HOST: The user name and host name of the account to which the privilege is granted.
- PRIV: The privilege name.
- WITH\_GRANT\_OPTION: Whether the account can grant the privilege to other accounts.

# <span id="page-197-1"></span>**The default\_roles Grant Table**

The default\_roles table lists default user roles. It has these columns:

- HOST, USER: The account or role to which the default role applies.
- DEFAULT\_ROLE\_HOST, DEFAULT\_ROLE\_USER: The default role.

# <span id="page-197-2"></span>**The role\_edges Grant Table**

The role\_edges table lists edges for role subgraphs. It has these columns:

- FROM\_HOST, FROM\_USER: The account that is granted a role.
- TO\_HOST, TO\_USER: The role that is granted to the account.
- WITH\_ADMIN\_OPTION: Whether the account can grant the role to and revoke it from other accounts by using WITH ADMIN OPTION.

## <span id="page-197-3"></span>**The password\_history Grant Table**

The password\_history table contains information about password changes. It has these columns:

- Host, User: The account for which the password change occurred.
- Password\_timestamp: The time when the password change occurred.
- Password: The new password hash value.

The password\_history table accumulates a sufficient number of nonempty passwords per account to enable MySQL to perform checks against both the account password history length and reuse interval. Automatic pruning of entries that are outside both limits occurs when password-change attempts occur.

![](_page_197_Picture_24.jpeg)

## **Note**

The empty password does not count in the password history and is subject to reuse at any time.

If an account is renamed, its entries are renamed to match. If an account is dropped or its authentication plugin is changed, its entries are removed.

## <span id="page-198-0"></span>**Grant Table Scope Column Properties**

Scope columns in the grant tables contain strings. The default value for each is the empty string. The following table shows the number of characters permitted in each column.

**Table 8.8 Grant Table Scope Column Lengths**

| Column Name        | Maximum Permitted Characters |
|--------------------|------------------------------|
| Host, Proxied_host | 255                          |
| User, Proxied_user | 32                           |
| Db                 | 64                           |
| Table_name         | 64                           |
| Column_name        | 64                           |
| Routine_name       | 64                           |

Host and Proxied\_host values are converted to lowercase before being stored in the grant tables.

For access-checking purposes, comparisons of User, Proxied\_user, authentication\_string, Db, and Table\_name values are case-sensitive. Comparisons of Host, Proxied\_host, Column\_name, and Routine\_name values are not case-sensitive.

## <span id="page-198-1"></span>**Grant Table Privilege Column Properties**

The user and db tables list each privilege in a separate column that is declared as ENUM('N','Y') DEFAULT 'N'. In other words, each privilege can be disabled or enabled, with the default being disabled.

The tables\_priv, columns\_priv, and procs\_priv tables declare the privilege columns as SET columns. Values in these columns can contain any combination of the privileges controlled by the table. Only those privileges listed in the column value are enabled.

**Table 8.9 Set-Type Privilege Column Values**

| Table Name   | Column Name | Possible Set Elements                                                                                                                                      |
|--------------|-------------|------------------------------------------------------------------------------------------------------------------------------------------------------------|
| tables_priv  | Table_priv  | 'Select', 'Insert',<br>'Update', 'Delete',<br>'Create', 'Drop',<br>'Grant', 'References',<br>'Index', 'Alter',<br>'Create View', 'Show<br>view', 'Trigger' |
| tables_priv  | Column_priv | 'Select', 'Insert',<br>'Update', 'References'                                                                                                              |
| columns_priv | Column_priv | 'Select', 'Insert',<br>'Update', 'References'                                                                                                              |
| procs_priv   | Proc_priv   | 'Execute', 'Alter<br>Routine', 'Grant'                                                                                                                     |

Only the user and global\_grants tables specify administrative privileges, such as [RELOAD](#page-176-0), [SHUTDOWN](#page-177-0), and [SYSTEM\\_VARIABLES\\_ADMIN](#page-186-1). Administrative operations are operations on the server itself and are not database-specific, so there is no reason to list these privileges in the other grant tables. Consequently, the server need consult only the user and global\_grants tables to determine whether a user can perform an administrative operation.

The [FILE](#page-175-2) privilege also is specified only in the user table. It is not an administrative privilege as such, but a user's ability to read or write files on the server host is independent of the database being accessed.

# <span id="page-199-1"></span>**Grant Table Concurrency**

To permit concurrent DML and DDL operations on MySQL grant tables, read operations that previously acquired row locks on MySQL grant tables are executed as non-locking reads. Operations that are performed as non-locking reads on MySQL grant tables include:

- SELECT statements and other read-only statements that read data from grant tables through join lists and subqueries, including SELECT ... FOR SHARE statements, using any transaction isolation level.
- DML operations that read data from grant tables (through join lists or subqueries) but do not modify them, using any transaction isolation level.

Statements that no longer acquire row locks when reading data from grant tables report a warning if executed while using statement-based replication.

When using -binlog\_format=mixed, DML operations that read data from grant tables are written to the binary log as row events to make the operations safe for mixed-mode replication.

SELECT ... FOR SHARE statements that read data from grant tables report a warning. With the FOR SHARE clause, read locks are not supported on grant tables.

DML operations that read data from grant tables and are executed using the SERIALIZABLE isolation level report a warning. Read locks that would normally be acquired when using the SERIALIZABLE isolation level are not supported on grant tables.

# <span id="page-199-0"></span>**8.2.4 Specifying Account Names**

MySQL account names consist of a user name and a host name, which enables creation of distinct accounts for users with the same user name who connect from different hosts. This section describes the syntax for account names, including special values and wildcard rules.

In most respects, account names are similar to MySQL role names, with some differences described at Section 8.2.5, "Specifying Role Names".

Account names appear in SQL statements such as CREATE USER, GRANT, and SET PASSWORD and follow these rules:

- Account name syntax is 'user\_name'@'host\_name'.
- The @'host\_name' part is optional. An account name consisting only of a user name is equivalent to 'user\_name'@'%'. For example, 'me' is equivalent to 'me'@'%'.
- The user name and host name need not be quoted if they are legal as unquoted identifiers. Quotes must be used if a user\_name string contains special characters (such as space or -), or a host\_name string contains special characters or wildcard characters (such as . or %). For example, in the account name 'test-user'@'%.com', both the user name and host name parts require quotes.
- Quote user names and host names as identifiers or as strings, using either backticks (`), single quotation marks ('), or double quotation marks ("). For string-quoting and identifier-quoting guidelines, see Section 11.1.1, "String Literals", and Section 11.2, "Schema Object Names". In SHOW statement results, user names and host names are quoted using backticks (`).
- The user name and host name parts, if quoted, must be quoted separately. That is, write 'me'@'localhost', not 'me@localhost'. (The latter is actually equivalent to 'me@localhost'@'%', although this behavior is now deprecated.)
- A reference to the CURRENT\_USER or CURRENT\_USER() function is equivalent to specifying the current client's user name and host name literally.

MySQL stores account names in grant tables in the mysql system database using separate columns for the user name and host name parts:

- The user table contains one row for each account. The User and Host columns store the user name and host name. This table also indicates which global privileges the account has.
- Other grant tables indicate privileges an account has for databases and objects within databases. These tables have User and Host columns to store the account name. Each row in these tables associates with the account in the user table that has the same User and Host values.
- For access-checking purposes, comparisons of User values are case-sensitive. Comparisons of Host values are not case-sensitive.

For additional detail about the properties of user names and host names as stored in the grant tables, such as maximum length, see Grant Table Scope Column Properties.

User names and host names have certain special values or wildcard conventions, as described following.

The user name part of an account name is either a nonblank value that literally matches the user name for incoming connection attempts, or a blank value (the empty string) that matches any user name. An account with a blank user name is an anonymous user. To specify an anonymous user in SQL statements, use a quoted empty user name part, such as ''@'localhost'.

The host name part of an account name can take many forms, and wildcards are permitted:

- A host value can be a host name or an IP address (IPv4 or IPv6). The name 'localhost' indicates the local host. The IP address '127.0.0.1' indicates the IPv4 loopback interface. The IP address '::1' indicates the IPv6 loopback interface.
- Use of the % and \_ wildcard characters is permitted in host name or IP address values, but is deprecated and thus subject to removal in a future version of MySQL. These characters have the same meaning as for pattern-matching operations performed with the LIKE operator. For example, a host value of '%' matches any host name, whereas a value of '%.mysql.com' matches any host in the mysql.com domain. '198.51.100.%' matches any host in the 198.51.100 class C network.

Because IP wildcard values are permitted in host values (for example, '198.51.100.%' to match every host on a subnet), someone could try to exploit this capability by naming a host 198.51.100.somewhere.com. To foil such attempts, MySQL does not perform matching on host names that start with digits and a dot. For example, if a host is named 1.2.example.com, its name never matches the host part of account names. An IP wildcard value can match only IP addresses, not host names.

If partial\_revokes is ON, MySQL treats % and \_ in grants as literal characters, and not as wildcards. Use of these wildcards is deprecated (regardless of this variable's value); you should expect this functionality to be removed in a future version of MySQL.

• For a host value specified as an IPv4 address, a netmask can be given to indicate how many address bits to use for the network number. Netmask notation cannot be used for IPv6 addresses.

The syntax is host\_ip/netmask. For example:

```
CREATE USER 'david'@'198.51.100.0/255.255.255.0';
```

This enables david to connect from any client host having an IP address client\_ip for which the following condition is true:

```
client_ip & netmask = host_ip
```

That is, for the CREATE USER statement just shown:

```
client_ip & 255.255.255.0 = 198.51.100.0
```

IP addresses that satisfy this condition range from 198.51.100.0 to 198.51.100.255.

A netmask typically begins with bits set to 1, followed by bits set to 0. Examples:

- 198.0.0.0/255.0.0.0: Any host on the 198 class A network
- 198.51.0.0/255.255.0.0: Any host on the 198.51 class B network
- 198.51.100.0/255.255.255.0: Any host on the 198.51.100 class C network
- 198.51.100.1: Only the host with this specific IP address
- A host value specified as an IPv4 address can be written using CIDR notation, such as 198.51.100.44/24.

The server performs matching of host values in account names against the client host using the value returned by the system DNS resolver for the client host name or IP address. Except in the case that the account host value is specified using netmask notation, the server performs this comparison as a string match, even for an account host value given as an IP address. This means that you should specify account host values in the same format used by DNS. Here are examples of problems to watch out for:

- Suppose that a host on the local network has a fully qualified name of host1.example.com. If DNS returns name lookups for this host as host1.example.com, use that name in account host values. If DNS returns just host1, use host1 instead.
- If DNS returns the IP address for a given host as 198.51.100.2, that matches an account host value of 198.51.100.2 but not 198.051.100.2. Similarly, it matches an account host pattern like 198.51.100.% but not 198.051.100.%.

To avoid problems like these, it is advisable to check the format in which your DNS returns host names and addresses. Use values in the same format in MySQL account names.

# <span id="page-1-0"></span>**8.2.5 Specifying Role Names**

MySQL role names refer to roles, which are named collections of privileges. For role usage examples, see [Section 8.2.10, "Using Roles".](#page-10-0)

Role names have syntax and semantics similar to account names; see Section 8.2.4, "Specifying Account Names". As stored in the grant tables, they have the same properties as account names, which are described in Grant Table Scope Column Properties.

Role names differ from account names in these respects:

- The user part of role names cannot be blank. Thus, there is no "anonymous role" analogous to the concept of "anonymous user."
- As for an account name, omitting the host part of a role name results in a host part of '%'. But unlike '%' in an account name, a host part of '%' in a role name has no wildcard properties. For example, for a name 'me'@'%' used as a role name, the host part ('%') is just a literal value; it has no "any host" matching property.
- Netmask notation in the host part of a role name has no significance.
- An account name is permitted to be CURRENT\_USER() in several contexts. A role name is not.

It is possible for a row in the mysql.user system table to serve as both an account and a role. In this case, any special user or host name matching properties do not apply in contexts for which the name is used as a role name. For example, you cannot execute the following statement with the expectation that it sets the current session roles using all roles that have a user part of myrole and any host name:

```
SET ROLE 'myrole'@'%';
```

Instead, the statement sets the active role for the session to the role with exactly the name 'myrole'@'%'.

For this reason, role names are often specified using only the user name part and letting the host name part implicitly be '%'. Specifying a role with a non-'%' host part can be useful if you intend to create a name that works both as a role an as a user account that is permitted to connect from the given host.

# <span id="page-2-0"></span>**8.2.6 Access Control, Stage 1: Connection Verification**

When you attempt to connect to a MySQL server, the server accepts or rejects the connection based on these conditions:

- Your identity and whether you can verify it by supplying the proper credentials.
- Whether your account is locked or unlocked.

The server checks credentials first, then account locking state. A failure at either step causes the server to deny access to you completely. Otherwise, the server accepts the connection, and then enters Stage 2 and waits for requests.

The server performs identity and credentials checking using columns in the user table, accepting the connection only if these conditions are satisfied:

- The client host name and user name match the Host and User columns in some user table row. For the rules governing permissible Host and User values, see Section 8.2.4, "Specifying Account Names".
- The client supplies the credentials specified in the row (for example, a password), as indicated by the authentication\_string column. Credentials are interpreted using the authentication plugin named in the plugin column.
- The row indicates that the account is unlocked. Locking state is recorded in the account\_locked column, which must have a value of 'N'. Account locking can be set or changed with the CREATE USER or ALTER USER statement.

Your identity is based on two pieces of information:

- Your MySQL user name.
- The client host from which you connect.

If the User column value is nonblank, the user name in an incoming connection must match exactly. If the User value is blank, it matches any user name. If the user table row that matches an incoming connection has a blank user name, the user is considered to be an anonymous user with no name, not a user with the name that the client actually specified. This means that a blank user name is used for all further access checking for the duration of the connection (that is, during Stage 2).

The authentication\_string column can be blank. This is not a wildcard and does not mean that any password matches. It means that the user must connect without specifying a password. The authentication method implemented by the plugin that authenticates the client may or may not use the password in the authentication\_string column. In this case, it is possible that an external password is also used to authenticate to the MySQL server.

Nonblank password values stored in the authentication\_string column of the user table are encrypted. MySQL does not store passwords as cleartext for anyone to see. Rather, the password supplied by a user who is attempting to connect is encrypted (using the password hashing method implemented by the account authentication plugin). The encrypted password then is used during the connection process when checking whether the password is correct. This is done without the encrypted password ever traveling over the connection. See Section 8.2.1, "Account User Names and Passwords".

From the MySQL server's point of view, the encrypted password is the real password, so you should never give anyone access to it. In particular, do not give nonadministrative users read access to tables in the mysql system database.

The following table shows how various combinations of User and Host values in the user table apply to incoming connections.

| User Value | Host Value       | Permissible Connections                                                                                               |
|------------|------------------|-----------------------------------------------------------------------------------------------------------------------|
| 'fred'     | 'h1.example.net' | fred, connecting from<br>h1.example.net                                                                               |
| ''         | 'h1.example.net' | Any user, connecting from<br>h1.example.net                                                                           |
| 'fred'     | '%'              | fred, connecting from any host                                                                                        |
| ''         | '%'              | Any user, connecting from any<br>host                                                                                 |
| 'fred'     | '%.example.net'  | fred, connecting from any host<br>in the example.net domain                                                           |
| 'fred'     | 'x.example.%'    | fred, connecting from<br>x.example.net,<br>x.example.com,<br>x.example.edu, and so on;<br>this is probably not useful |
| 'fred'     | '198.51.100.177' | fred, connecting from<br>the host with IP address<br>198.51.100.177                                                   |
| 'fred'     | '198.51.100.%'   | fred, connecting from any host<br>in the 198.51.100 class C<br>subnet                                                 |
| 'fred'     |                  | '198.51.100.0/255.255.255.0' Same as previous example                                                                 |

It is possible for the client host name and user name of an incoming connection to match more than one row in the user table. The preceding set of examples demonstrates this: Several of the entries shown match a connection from h1.example.net by fred.

When multiple matches are possible, the server must determine which of them to use. It resolves this issue as follows:

- Whenever the server reads the user table into memory, it sorts the rows.
- When a client attempts to connect, the server looks through the rows in sorted order.
- The server uses the first row that matches the client host name and user name.

The server uses sorting rules that order rows with the most-specific Host values first:

- Literal IP addresses and host names are the most specific.
- Accounts with an IP address in the host part have this order of specificity:
  - Accounts that have the host part given as an IP address:

```
CREATE USER 'user_name'@'127.0.0.1';
CREATE USER 'user_name'@'198.51.100.44';
```

• Accounts that have the host part given as an IP address using CIDR notation:

```
CREATE USER 'user_name'@'192.0.2.21/8';
CREATE USER 'user_name'@'198.51.100.44/16';
```

• Accounts that have the host part given as an IP address with a subnet mask:

```
CREATE USER 'user_name'@'192.0.2.0/255.255.255.0';
```

```
CREATE USER 'user_name'@'198.51.0.0/255.255.0.0';
```

- The pattern '%' means "any host" and is least specific.
- The empty string '' also means "any host" but sorts after '%'.

Non-TCP (socket file, named pipe, and shared memory) connections are treated as local connections and match a host part of localhost if there are any such accounts, or host parts with wildcards that match localhost otherwise (for example, local%, l%, %).

The treatment of '%' as equivalent to localhost is deprecated; you should expect this behavior to removed from a future version of MySQL.

Rows with the same Host value are ordered with the most-specific User values first. A blank User value means "any user" and is least specific, so for rows with the same Host value, nonanonymous users sort before anonymous users.

For rows with equally-specific Host and User values, the order is nondeterministic.

To see how this works, suppose that the user table looks like this:

```
+-----------+----------+-
| Host | User | ...
+-----------+----------+-
| % | root | ...
| % | jeffrey | ...
| localhost | root | ...
| localhost | | ...
+-----------+----------+-
```

When the server reads the table into memory, it sorts the rows using the rules just described. The result after sorting looks like this:

```
+-----------+----------+-
| Host | User | ...
+-----------+----------+-
| localhost | root | ...
| localhost | | ...
| % | jeffrey | ...
| % | root | ...
+-----------+----------+-
```

When a client attempts to connect, the server looks through the sorted rows and uses the first match found. For a connection from localhost by jeffrey, two of the rows from the table match: the one with Host and User values of 'localhost' and '', and the one with values of '%' and 'jeffrey'. The 'localhost' row appears first in sorted order, so that is the one the server uses.

Here is another example. Suppose that the user table looks like this:

```
+----------------+----------+-
| Host | User | ...
+----------------+----------+-
| % | jeffrey | ...
| h1.example.net | | ...
+----------------+----------+-
```

The sorted table looks like this:

```
+----------------+----------+-
| Host | User | ...
+----------------+----------+-
| h1.example.net | | ...
| % | jeffrey | ...
+----------------+----------+-
```

The first row matches a connection by any user from h1.example.net, whereas the second row matches a connection by jeffrey from any host.

![](_page_5_Picture_1.jpeg)

#### **Note**

It is a common misconception to think that, for a given user name, all rows that explicitly name that user are used first when the server attempts to find a match for the connection. This is not true. The preceding example illustrates this, where a connection from h1.example.net by jeffrey is first matched not by the row containing 'jeffrey' as the User column value, but by the row with no user name. As a result, jeffrey is authenticated as an anonymous user, even though he specified a user name when connecting.

If you are able to connect to the server, but your privileges are not what you expect, you probably are being authenticated as some other account. To find out what account the server used to authenticate you, use the CURRENT\_USER() function. (See Section 14.15, "Information Functions".) It returns a value in user\_name@host\_name format that indicates the User and Host values from the matching user table row. Suppose that jeffrey connects and issues the following query:

```
mysql> SELECT CURRENT_USER();
+----------------+
| CURRENT_USER() |
+----------------+
| @localhost |
+----------------+
```

The result shown here indicates that the matching user table row had a blank User column value. In other words, the server is treating jeffrey as an anonymous user.

Another way to diagnose authentication problems is to print out the user table and sort it by hand to see where the first match is being made.