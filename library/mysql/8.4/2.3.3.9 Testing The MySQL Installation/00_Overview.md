---
source: MySQL 8.4 Reference
title: 00_Overview
---

You can test whether the MySQL server is working by executing any of the following commands:

```
C:\> "C:\Program Files\MySQL\MySQL Server 8.4\bin\mysqlshow"
C:\> "C:\Program Files\MySQL\MySQL Server 8.4\bin\mysqlshow" -u root mysql
C:\> "C:\Program Files\MySQL\MySQL Server 8.4\bin\mysqladmin" version status proc
C:\> "C:\Program Files\MySQL\MySQL Server 8.4\bin\mysql" test
```

If mysqld is slow to respond to TCP/IP connections from client programs, there is probably a problem with your DNS. In this case, start mysqld with the skip\_name\_resolve system variable enabled and use only localhost and IP addresses in the Host column of the MySQL grant tables. (Be sure that an account exists that specifies an IP address or you may not be able to connect.)

You can force a MySQL client to use a named-pipe connection rather than TCP/IP by specifying the - pipe or --protocol=PIPE option, or by specifying . (period) as the host name. Use the --socket option to specify the name of the pipe if you do not want to use the default pipe name.

If you have set a password for the root account, deleted the anonymous account, or created a new user account, then to connect to the MySQL server you must use the appropriate -u and -p options with the commands shown previously. See Section 6.2.4, "Connecting to the MySQL Server Using Command Options".

For more information about mysqlshow, see Section 6.5.6, "mysqlshow — Display Database, Table, and Column Information".

# <span id="page-137-0"></span>**2.3.4 Troubleshooting a Microsoft Windows MySQL Server Installation**

When installing and running MySQL for the first time, you may encounter certain errors that prevent the MySQL server from starting. This section helps you diagnose and correct some of these errors.

Your first resource when troubleshooting server issues is the error log. The MySQL server uses the error log to record information relevant to the error that prevents the server from starting. The error log is located in the data directory specified in your my.ini file. The default data directory location is C: \Program Files\MySQL\MySQL Server 8.4\data, or C:\ProgramData\Mysql on Windows 7 and Windows Server 2008. The C:\ProgramData directory is hidden by default. You need to change your folder options to see the directory and contents. For more information on the error log and understanding the content, see Section 7.4.2, "The Error Log".

For information regarding possible errors, also consult the console messages displayed when the MySQL service is starting. Use the SC START mysqld\_service\_name or NET START mysqld\_service\_name command from the command line after installing mysqld as a service to see any error messages regarding the starting of the MySQL server as a service. See [Section 2.3.3.8,](#page-134-0) ["Starting MySQL as a Windows Service"](#page-134-0).

The following examples show other common error messages you might encounter when installing MySQL and starting the server for the first time:

• If the MySQL server cannot find the mysql privileges database or other critical files, it displays these messages:

```
System error 1067 has occurred.
Fatal error: Can't open and lock privilege tables:
Table 'mysql.user' doesn't exist
```

These messages often occur when the MySQL base or data directories are installed in different locations than the default locations (C:\Program Files\MySQL\MySQL Server 8.4 and C: \Program Files\MySQL\MySQL Server 8.4\data, respectively).

This situation can occur when MySQL is upgraded and installed to a new location, but the configuration file is not updated to reflect the new location. In addition, old and new configuration files might conflict. Be sure to delete or rename any old configuration files when upgrading MySQL.

If you have installed MySQL to a directory other than C:\Program Files\MySQL\MySQL Server 8.4, ensure that the MySQL server is aware of this through the use of a configuration (my.ini) file. Put the my.ini file in your Windows directory, typically C:\WINDOWS. To determine its exact location from the value of the WINDIR environment variable, issue the following command from the command prompt:

```
C:\> echo %WINDIR%
```

You can create or modify an option file with any text editor, such as Notepad. For example, if MySQL is installed in E:\mysql and the data directory is D:\MySQLdata, you can create the option file and set up a [mysqld] section to specify values for the basedir and datadir options:

```
[mysqld]
# set basedir to your installation path
basedir=E:/mysql
# set datadir to the location of your data directory
datadir=D:/MySQLdata
```

Microsoft Windows path names are specified in option files using (forward) slashes rather than backslashes. If you do use backslashes, double them:

```
[mysqld]
# set basedir to your installation path
basedir=C:\\Program Files\\MySQL\\MySQL Server 8.4
# set datadir to the location of your data directory
datadir=D:\\MySQLdata
```

The rules for use of backslash in option file values are given in Section 6.2.2.2, "Using Option Files".

If you change the datadir value in your MySQL configuration file, you must move the contents of the existing MySQL data directory before restarting the MySQL server.

See [Section 2.3.3.2, "Creating an Option File"](#page-130-0).

• If you reinstall or upgrade MySQL without first stopping and removing the existing MySQL service, and then configure MySQL using MySQL Configurator, you might see this error:

```
Error: Cannot create Windows service for MySql. Error: 0
```

This occurs when the Configuration Wizard tries to install the service and finds an existing service with the same name.

One solution to this problem is to choose a service name other than mysql when using the configuration wizard. This enables the new service to be installed correctly, but leaves the outdated service in place. Although this is harmless, it is best to remove old services that are no longer in use.

To permanently remove the old mysql service, execute the following command as a user with administrative privileges, on the command line:

```
C:\> SC DELETE mysql
[SC] DeleteService SUCCESS
```

If the SC utility is not available for your version of Windows, download the delsrv utility from [http://](http://www.microsoft.com/windows2000/techinfo/reskit/tools/existing/delsrv-o.asp) [www.microsoft.com/windows2000/techinfo/reskit/tools/existing/delsrv-o.asp](http://www.microsoft.com/windows2000/techinfo/reskit/tools/existing/delsrv-o.asp) and use the delsrv mysql syntax.

# <span id="page-138-0"></span>**2.3.5 Windows Postinstallation Procedures**

GUI tools exist that perform most of the tasks described in this section, including:

- [MySQL Configurator](#page-111-0): Used to configure the MySQL server.
- MySQL Workbench: Manages the MySQL server and edits SQL statements.

If necessary, initialize the data directory and create the MySQL grant tables. Windows installation operations performed by MySQL Configurator can initialize the data directory automatically. For installation from a ZIP Archive package, initialize the data directory as described at Section 2.9.1, "Initializing the Data Directory".

Regarding passwords, if you configured MySQL using the MySQL Configurator, you may have already assigned a password to the initial root account. (See [Section 2.3.2, "Configuration: Using MySQL](#page-111-0) [Configurator"](#page-111-0).) Otherwise, use the password-assignment procedure given in Section 2.9.4, "Securing the Initial MySQL Account".

Before assigning a password, you might want to try running some client programs to make sure that you can connect to the server and that it is operating properly. Make sure that the server is running (see [Section 2.3.3.5, "Starting the Server for the First Time"\)](#page-131-1). You can also set up a MySQL service that runs automatically when Windows starts (see [Section 2.3.3.8, "Starting MySQL as a Windows](#page-134-0) [Service"\)](#page-134-0).

These instructions assume that your current location is the MySQL installation directory and that it has a bin subdirectory containing the MySQL programs used here. If that is not true, adjust the command path names accordingly.

If you installed MySQL using the MSI, the default installation directory is C:\Program Files\MySQL \MySQL Server 8.4:

```
C:\> cd "C:\Program Files\MySQL\MySQL Server 8.4"
```

A common installation location for installation from a ZIP archive is C:\mysql:

```
C:\> cd C:\mysql
```

Alternatively, add the bin directory to your PATH environment variable setting. That enables your command interpreter to find MySQL programs properly, so that you can run a program by typing only its name, not its path name. See [Section 2.3.3.7, "Customizing the PATH for MySQL Tools"](#page-133-0).

With the server running, issue the following commands to verify that you can retrieve information from the server. The output should be similar to that shown here.

Use mysqlshow to see what databases exist:

```
C:\> bin\mysqlshow
+--------------------+
| Databases |
+--------------------+
| information_schema |
| mysql |
| performance_schema |
| sys |
+--------------------+
```

The list of installed databases may vary, but always includes at least mysql and information\_schema.

The preceding command (and commands for other MySQL programs such as mysql) may not work if the correct MySQL account does not exist. For example, the program may fail with an error, or you may not be able to view all databases. If you configured MySQL using MySQL Configurator, the root user is created automatically with the password you supplied. In this case, you should use the -u root and -p options. (You must use those options if you have already secured the initial MySQL accounts.) With -p, the client program prompts for the root password. For example:

```
C:\> bin\mysqlshow -u root -p
Enter password: (enter root password here)
+--------------------+
| Databases |
+--------------------+
| information_schema |
| mysql |
| performance_schema |
| sys |
+--------------------+
```

If you specify a database name, mysqlshow displays a list of the tables within the database:

```
C:\> bin\mysqlshow mysql
Database: mysql
+---------------------------+
| Tables |
+---------------------------+
| columns_priv |
| component |
| db |
| default_roles |
| engine_cost |
| func |
| general_log |
| global_grants |
| gtid_executed |
| help_category |
| help_keyword |
| help_relation |
| help_topic |
| innodb_index_stats |
| innodb_table_stats |
| ndb_binlog_index |
| password_history |
| plugin |
| procs_priv |
| proxies_priv |
| role_edges |
| server_cost |
| servers |
| slave_master_info |
| slave_relay_log_info |
| slave_worker_info |
| slow_log |
| tables_priv |
| time_zone |
| time_zone_leap_second |
| time_zone_name |
| time_zone_transition |
| time_zone_transition_type |
| user |
+---------------------------+
```

Use the mysql program to select information from a table in the mysql database:

```
C:\> bin\mysql -e "SELECT User, Host, plugin FROM mysql.user" mysql
+------+-----------+-----------------------+
| User | Host | plugin |
+------+-----------+-----------------------+
| root | localhost | caching_sha2_password |
+------+-----------+-----------------------+
```

For more information about mysql and mysqlshow, see Section 6.5.1, "mysql — The MySQL Command-Line Client", and Section 6.5.6, "mysqlshow — Display Database, Table, and Column Information".

# <span id="page-140-0"></span>**2.3.6 Windows Platform Restrictions**

The following restrictions apply to use of MySQL on the Windows platform:

### • **Process memory**

On Windows 32-bit platforms, it is not possible by default to use more than 2GB of RAM within a single process, including MySQL. This is because the physical address limit on Windows 32-bit is 4GB and the default setting within Windows is to split the virtual address space between kernel (2GB) and user/applications (2GB).

Some versions of Windows have a boot time setting to enable larger applications by reducing the kernel application. Alternatively, to use more than 2GB, use a 64-bit version of Windows.

### • **File system aliases**

When using MyISAM tables, you cannot use aliases within Windows link to the data files on another volume and then link back to the main MySQL datadir location.

This facility is often used to move the data and index files to a RAID or other fast solution.

### • **Limited number of ports**

Windows systems have about 4,000 ports available for client connections, and after a connection on a port closes, it takes two to four minutes before the port can be reused. In situations where clients connect to and disconnect from the server at a high rate, it is possible for all available ports to be used up before closed ports become available again. If this happens, the MySQL server appears to be unresponsive even though it is running. Ports may be used by other applications running on the machine as well, in which case the number of ports available to MySQL is lower.

For more information about this problem, see<https://support.microsoft.com/kb/196271>.

### • **DATA DIRECTORY and INDEX DIRECTORY**

The DATA DIRECTORY clause of the CREATE TABLE statement is supported on Windows for InnoDB tables only, as described in Section 17.6.1.2, "Creating Tables Externally". For MyISAM and other storage engines, the DATA DIRECTORY and INDEX DIRECTORY clauses for CREATE TABLE are ignored on Windows and any other platforms with a nonfunctional realpath() call.

### • **DROP DATABASE**

You cannot drop a database that is in use by another session.

### • **Case-insensitive names**

File names are not case-sensitive on Windows, so MySQL database and table names are also not case-sensitive on Windows. The only restriction is that database and table names must be specified using the same case throughout a given statement. See Section 11.2.3, "Identifier Case Sensitivity".

### • **Directory and file names**

On Windows, MySQL Server supports only directory and file names that are compatible with the current ANSI code pages. For example, the following Japanese directory name does not work in the Western locale (code page 1252):

```
datadir="C:/私たちのプロジェクトのデータ"
```

The same limitation applies to directory and file names referred to in SQL statements, such as the data file path name in LOAD DATA.

# • **The \ path name separator character**

Path name components in Windows are separated by the \ character, which is also the escape character in MySQL. If you are using LOAD DATA or SELECT ... INTO OUTFILE, use Unix-style file names with / characters:

mysql> **LOAD DATA INFILE 'C:/tmp/skr.txt' INTO TABLE skr;**

```
mysql> SELECT * INTO OUTFILE 'C:/tmp/skr.txt' FROM skr;
```

Alternatively, you must double the \ character:

```
mysql> LOAD DATA INFILE 'C:\\tmp\\skr.txt' INTO TABLE skr;
mysql> SELECT * INTO OUTFILE 'C:\\tmp\\skr.txt' FROM skr;
```

### • **Problems with pipes**

Pipes do not work reliably from the Windows command-line prompt. If the pipe includes the character ^Z / CHAR(24), Windows thinks that it has encountered end-of-file and aborts the program.

This is mainly a problem when you try to apply a binary log as follows:

```
C:\> mysqlbinlog binary_log_file | mysql --user=root
```

If you have a problem applying the log and suspect that it is because of a ^Z / CHAR(24) character, you can use the following workaround:

```
C:\> mysqlbinlog binary_log_file --result-file=/tmp/bin.sql
C:\> mysql --user=root --execute "source /tmp/bin.sql"
```

The latter command also can be used to reliably read any SQL file that may contain binary data.

# <span id="page-142-0"></span>**2.4 Installing MySQL on macOS**

For a list of macOS versions that the MySQL server supports, see [https://www.mysql.com/support/](https://www.mysql.com/support/supportedplatforms/database.md) [supportedplatforms/database.html](https://www.mysql.com/support/supportedplatforms/database.md).

MySQL for macOS is available in a number of different forms:

- Native Package Installer, which uses the native macOS installer (DMG) to walk you through the installation of MySQL. For more information, see [Section 2.4.2, "Installing MySQL on macOS Using](#page-143-0) [Native Packages"](#page-143-0). You can use the package installer with macOS. The user you use to perform the installation must have administrator privileges.
- Compressed TAR archive, which uses a file packaged using the Unix tar and gzip commands. To use this method, you need to open a Terminal window. You do not need administrator privileges using this method; you can install the MySQL server anywhere using this method. For more information on using this method, you can use the generic instructions for using a tarball, [Section 2.2, "Installing MySQL on Unix/Linux Using Generic Binaries"](#page-104-1).

In addition to the core installation, the Package Installer also includes [Section 2.4.3, "Installing and](#page-145-0) [Using the MySQL Launch Daemon"](#page-145-0) and [Section 2.4.4, "Installing and Using the MySQL Preference](#page-148-0) [Pane"](#page-148-0) to simplify the management of your installation.

For additional information on using MySQL on macOS, see [Section 2.4.1, "General Notes on Installing](#page-142-1) [MySQL on macOS".](#page-142-1)

# <span id="page-142-1"></span>**2.4.1 General Notes on Installing MySQL on macOS**

You should keep the following issues and notes in mind:

• **Other MySQL installations**: The installation procedure does not recognize MySQL installations by package managers such as Homebrew. The installation and upgrade process is for MySQL packages provided by us. If other installations are present, then consider stopping them before executing this installer to avoid port conflicts.

**Homebrew**: For example, if you installed MySQL Server using Homebrew to its default location then the MySQL installer installs to a different location and won't upgrade the version from Homebrew. In this scenario you would end up with multiple MySQL installations that, by default, attempt to use the

same ports. Stop the other MySQL Server instances before running this installer, such as executing brew services stop mysql to stop the Homebrew's MySQL service.

- **Launchd**: A launchd daemon is installed that alters MySQL configuration options. Consider editing it if needed, see the documentation below for additional information. Also, macOS 10.10 removed startup item support in favor of launchd daemons. The optional MySQL preference pane under macOS **System Preferences** uses the launchd daemon.
- **Users**: You may need (or want) to create a specific mysql user to own the MySQL directory and data. You can do this through the Directory Utility, and the mysql user should already exist. For use in single user mode, an entry for \_mysql (note the underscore prefix) should already exist within the system /etc/passwd file.
- **Data**: Because the MySQL package installer installs the MySQL contents into a version and platform specific directory, you can use this to upgrade and migrate your database between versions. You need either to copy the data directory from the old version to the new version, or to specify an alternative datadir value to set location of the data directory. By default, the MySQL directories are installed under /usr/local/.
- **Aliases**: You might want to add aliases to your shell's resource file to make it easier to access commonly used programs such as mysql and mysqladmin from the command line. The syntax for bash is:

```
alias mysql=/usr/local/mysql/bin/mysql
alias mysqladmin=/usr/local/mysql/bin/mysqladmin
```

# For tcsh, use:

```
alias mysql /usr/local/mysql/bin/mysql
alias mysqladmin /usr/local/mysql/bin/mysqladmin
```

Even better, add /usr/local/mysql/bin to your PATH environment variable. You can do this by modifying the appropriate startup file for your shell. For more information, see Section 6.2.1, "Invoking MySQL Programs".

• **Removing**: After you have copied over the MySQL database files from the previous installation and have successfully started the new server, you should consider removing the old installation files to save disk space. Additionally, you should also remove older versions of the Package Receipt directories located in /Library/Receipts/mysql-VERSION.pkg.

# <span id="page-143-0"></span>**2.4.2 Installing MySQL on macOS Using Native Packages**

The package is located inside a disk image (.dmg) file that you first need to mount by double-clicking its icon in the Finder. It should then mount the image and display its contents.

![](_page_143_Picture_13.jpeg)

### **Note**

Before proceeding with the installation, be sure to stop all running MySQL server instances by using either the MySQL Manager Application (on macOS Server), the preference pane, or mysqladmin shutdown on the command line.

To install MySQL using the package installer:

- 1. Download the disk image (.dmg) file (the community version is available [here\)](https://dev.mysql.com/downloads/mysql/) that contains the MySQL package installer. Double-click the file to mount the disk image and see its contents.
  - Double-click the MySQL installer package from the disk. It is named according to the version of MySQL you have downloaded. For example, for MySQL server 8.4.8 it might be named mysql-8.4.8-macos-10.13-x86\_64.pkg.
- 2. The initial wizard introduction screen references the MySQL server version to install. Click **Continue** to begin the installation.

The MySQL community edition shows a copy of the relevant GNU General Public License. Click **Continue** and then **Agree** to continue.

3. From the **Installation Type** page you can either click **Install** to execute the installation wizard using all defaults, click **Customize** to alter which components to install (MySQL server, MySQL Test, Preference Pane, Launchd Support -- all but MySQL Test are enabled by default).

![](_page_144_Picture_3.jpeg)

### **Note**

Although the **Change Install Location** option is visible, the installation location cannot be changed.

**Figure 2.5 MySQL Package Installer Wizard: Customize**

![](_page_144_Picture_7.jpeg)

- 4. Click **Install** to install MySQL Server. The installation process ends here if upgrading a current MySQL Server installation, otherwise follow the wizard's additional configuration steps for your new MySQL Server installation.
- 5. After a successful new MySQL Server installation, complete the configuration by defining the root password and enabling (or disabling) the MySQL server at startup.
- 6. Define a password for the root user, and also toggle whether MySQL Server should start after the configuration step is complete.
- 7. **Summary** is the final step and references a successful and complete MySQL Server installation. **Close** the wizard.

MySQL server is now installed. If you chose to not start MySQL, then use either launchctl from the command line or start MySQL by clicking "Start" using the MySQL preference pane. For additional information, see [Section 2.4.3, "Installing and Using the MySQL Launch Daemon",](#page-145-0) and [Section 2.4.4,](#page-148-0) ["Installing and Using the MySQL Preference Pane".](#page-148-0) Use the MySQL Preference Pane or launchd to configure MySQL to automatically start at bootup.

When installing using the package installer, the files are installed into a directory within /usr/ local matching the name of the installation version and platform. For example, the installer file mysql-8.4.8-macos10.15-x86\_64.dmg installs MySQL into /usr/local/mysql-8.4.8 macos10.15-x86\_64/ with a symlink to /usr/local/mysql. The following table shows the layout of this MySQL installation directory.

![](_page_145_Picture_2.jpeg)

### **Note**

The macOS installation process does not create nor install a sample my.cnf MySQL configuration file.

**Table 2.8 MySQL Installation Layout on macOS**

<span id="page-145-1"></span>

| Directory       | Contents of Directory                                                                                                               |
|-----------------|-------------------------------------------------------------------------------------------------------------------------------------|
| bin             | mysqld server, client and utility programs                                                                                          |
| data            | Log files, databases, where /usr/local/<br>mysql/data/mysqld.local.err is the default<br>error log                                  |
| docs            | Helper documents, like the Release Notes and<br>build information                                                                   |
| include         | Include (header) files                                                                                                              |
| lib             | Libraries                                                                                                                           |
| man             | Unix manual pages                                                                                                                   |
| mysql-test      | MySQL test suite ('MySQL Test' is disabled by<br>default during the installation process when using<br>the installer package (DMG)) |
| share           | Miscellaneous support files, including error<br>messages, dictionary.txt, and rewriter SQL                                          |
| support-files   | Support scripts, such as<br>mysqld_multi.server, mysql.server, and<br>mysql-log-rotate.                                             |
| /tmp/mysql.sock | Location of the MySQL Unix socket                                                                                                   |

# <span id="page-145-0"></span>**2.4.3 Installing and Using the MySQL Launch Daemon**

macOS uses launch daemons to automatically start, stop, and manage processes and applications such as MySQL.

By default, the installation package (DMG) on macOS installs a launchd file named /Library/ LaunchDaemons/com.oracle.oss.mysql.mysqld.plist that contains a plist definition similar to:

```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
 <key>Label</key> <string>com.oracle.oss.mysql.mysqld</string>
 <key>ProcessType</key> <string>Interactive</string>
 <key>Disabled</key> <false/>
 <key>RunAtLoad</key> <true/>
 <key>KeepAlive</key> <true/>
 <key>SessionCreate</key> <true/>
 <key>LaunchOnlyOnce</key> <false/>
 <key>UserName</key> <string>_mysql</string>
 <key>GroupName</key> <string>_mysql</string>
 <key>ExitTimeOut</key> <integer>600</integer>
 <key>Program</key> <string>/usr/local/mysql/bin/mysqld</string>
 <key>ProgramArguments</key>
 <array>
```

```
 <string>/usr/local/mysql/bin/mysqld</string>
 <string>--user=_mysql</string>
 <string>--basedir=/usr/local/mysql</string>
 <string>--datadir=/usr/local/mysql/data</string>
 <string>--plugin-dir=/usr/local/mysql/lib/plugin</string>
 <string>--log-error=/usr/local/mysql/data/mysqld.local.err</string>
 <string>--pid-file=/usr/local/mysql/data/mysqld.local.pid</string>
 <string>--keyring-file-data=/usr/local/mysql/keyring/keyring</string>
 <string>--early-plugin-load=keyring_okv=keyring_okv.so</string>
 </array>
 <key>WorkingDirectory</key> <string>/usr/local/mysql</string>
</dict>
</plist>
```

![](_page_146_Picture_2.jpeg)

### **Note**

Some users report that adding a plist DOCTYPE declaration causes the launchd operation to fail, despite it passing the lint check. We suspect it's a copy-n-paste error. The md5 checksum of a file containing the above snippet is d925f05f6d1b6ee5ce5451b596d6baed.

To enable the launchd service, you can either:

• Open macOS system preferences and select the MySQL preference panel, and then execute **Start MySQL Server**.

**Figure 2.6 MySQL Preference Pane: Location**

The **Instances** page includes an option to start or stop MySQL, and **Initialize Database** recreates the data/ directory. **Uninstall** uninstalls MySQL Server and optionally the MySQL preference panel and launchd information.

**Figure 2.7 MySQL Preference Pane: Instances**

![](_page_147_Picture_2.jpeg)

• Or, manually load the launchd file.

```
$> cd /Library/LaunchDaemons
$> sudo launchctl load -F com.oracle.oss.mysql.mysqld.plist
```

• To configure MySQL to automatically start at bootup, you can:

\$> sudo launchctl load -w com.oracle.oss.mysql.mysqld.plist

![](_page_147_Picture_7.jpeg)

### **Note**

The upgrade process replaces your existing launchd file named com.oracle.oss.mysql.mysqld.plist.

### Additional launchd related information:

- The plist entries override my.cnf entries, because they are passed in as command line arguments. For additional information about passing in program options, see Section 6.2.2, "Specifying Program Options".
- The **ProgramArguments** section defines the command line options that are passed into the program, which is the mysqld binary in this case.

- The default plist definition is written with less sophisticated use cases in mind. For more complicated setups, you may want to remove some of the arguments and instead rely on a MySQL configuration file, such as my.cnf.
- If you edit the plist file, then uncheck the installer option when reinstalling or upgrading MySQL. Otherwise, your edited plist file is overwritten, and all edits are lost.

Because the default plist definition defines several **ProgramArguments**, you might remove most of these arguments and instead rely upon your my.cnf MySQL configuration file to define them. For example:

```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
 <key>Label</key> <string>com.oracle.oss.mysql.mysqld</string>
 <key>ProcessType</key> <string>Interactive</string>
 <key>Disabled</key> <false/>
 <key>RunAtLoad</key> <true/>
 <key>KeepAlive</key> <true/>
 <key>SessionCreate</key> <true/>
 <key>LaunchOnlyOnce</key> <false/>
 <key>UserName</key> <string>_mysql</string>
 <key>GroupName</key> <string>_mysql</string>
 <key>ExitTimeOut</key> <integer>600</integer>
 <key>Program</key> <string>/usr/local/mysql/bin/mysqld</string>
 <key>ProgramArguments</key>
 <array>
 <string>/usr/local/mysql/bin/mysqld</string>
 <string>--user=_mysql</string>
 <string>--basedir=/usr/local/mysql</string>
 <string>--datadir=/usr/local/mysql/data</string>
 <string>--plugin-dir=/usr/local/mysql/lib/plugin</string>
 <string>--log-error=/usr/local/mysql/data/mysqld.local.err</string>
 <string>--pid-file=/usr/local/mysql/data/mysqld.local.pid</string>
 <string>--keyring-file-data=/usr/local/mysql/keyring/keyring</string>
 <string>--early-plugin-load=keyring_okv=keyring_okv.so</string>
 </array>
 <key>WorkingDirectory</key> <string>/usr/local/mysql</string>
</dict>
</plist>
```

In this case, the basedir, datadir, plugin\_dir, log\_error, pid\_file, and --early-pluginload options were removed from the default plist ProgramArguments definition, which you might have defined in my.cnf instead.

# <span id="page-148-0"></span>**2.4.4 Installing and Using the MySQL Preference Pane**

The MySQL Installation Package includes a MySQL preference pane that enables you to start, stop, and control automated startup during boot of your MySQL installation.

This preference pane is installed by default, and is listed under your system's System Preferences window.

**Figure 2.8 MySQL Preference Pane: Location**

The MySQL preference pane is installed with the same DMG file that installs MySQL Server. Typically it is installed with MySQL Server but it can be installed by itself too.

To install the MySQL preference pane:

- 1. Go through the process of installing the MySQL server, as described in the documentation at [Section 2.4.2, "Installing MySQL on macOS Using Native Packages"](#page-143-0).
- 2. Click **Customize** at the **Installation Type** step. The "Preference Pane" option is listed there and enabled by default; make sure it is not deselected. The other options, such as MySQL Server, can be selected or deselected.

**Figure 2.9 MySQL Package Installer Wizard: Customize**

3. Complete the installation process.

![](_page_150_Picture_4.jpeg)

### **Note**

The MySQL preference pane only starts and stops MySQL installation installed from the MySQL package installation that have been installed in the default location.

Once the MySQL preference pane has been installed, you can control your MySQL server instance using this preference pane.

The **Instances** page includes an option to start or stop MySQL, and **Initialize Database** recreates the data/ directory. **Uninstall** uninstalls MySQL Server and optionally the MySQL preference panel and launchd information.

**Figure 2.10 MySQL Preference Pane: Instances**

![](_page_151_Picture_2.jpeg)

The **Configuration** page shows MySQL Server options including the path to the MySQL configuration file.

**Figure 2.11 MySQL Preference Pane: Configuration**

![](_page_152_Picture_2.jpeg)

The MySQL Preference Pane shows the current status of the MySQL server, showing **stopped** (in red) if the server is not running and **running** (in green) if the server has already been started. The preference pane also shows the current setting for whether the MySQL server has been set to start automatically.

# <span id="page-152-0"></span>**2.5 Installing MySQL on Linux**

Linux supports a number of different solutions for installing MySQL. We recommend that you use one of the distributions from Oracle, for which several methods for installation are available:

**Table 2.9 Linux Installation Methods and Information**

| Type    | Setup Method                        | Additional Information |
|---------|-------------------------------------|------------------------|
| Apt     | Enable the MySQL Apt<br>repository  | Documentation          |
| Yum     | Enable the MySQL Yum<br>repository  | Documentation          |
| Zypper  | Enable the MySQL SLES<br>repository | Documentation          |
| RPM     | Download a specific package         | Documentation          |
| DEB     | Download a specific package         | Documentation          |
| Generic | Download a generic package          | Documentation          |

| Type                                | Setup Method                                                                                                     | Additional Information |
|-------------------------------------|------------------------------------------------------------------------------------------------------------------|------------------------|
| Source                              | Compile from source                                                                                              | Documentation          |
| Docker                              | Use the Oracle Container<br>Registry. You can also use My<br>Oracle Support for the MySQL<br>Enterprise Edition. | Documentation          |
| Oracle Unbreakable Linux<br>Network | Use ULN channels                                                                                                 | Documentation          |

As an alternative, you can use the package manager on your system to automatically download and install MySQL with packages from the native software repositories of your Linux distribution. These native packages are often several versions behind the currently available release. You are also normally unable to install innovation releases, since these are not usually made available in the native repositories. For more information on using the native package installers, see [Section 2.5.7, "Installing](#page-190-0) [MySQL on Linux from the Native Software Repositories"](#page-190-0).

![](_page_153_Picture_3.jpeg)

### **Note**

For many Linux installations, you want to set up MySQL to be started automatically when your machine starts. Many of the native package installations perform this operation for you, but for source, binary and RPM solutions you may need to set this up separately. The required script, mysql.server, can be found in the support-files directory under the MySQL installation directory or in a MySQL source tree. You can install it as /etc/init.d/mysql for automatic MySQL startup and shutdown. See Section 6.3.3, "mysql.server — MySQL Server Startup Script".

# <span id="page-153-0"></span>**2.5.1 Installing MySQL on Linux Using the MySQL Yum Repository**

The [MySQL Yum repository](https://dev.mysql.com/downloads/repo/yum/) for Oracle Linux, Red Hat Enterprise Linux, CentOS, and Fedora provides RPM packages for installing the MySQL server, client, MySQL Workbench, MySQL Utilities, MySQL Router, MySQL Shell, Connector/ODBC, Connector/Python and so on (not all packages are available for all the distributions; see [Installing Additional MySQL Products and Components with Yum](#page-157-1) for details).

# **Before You Start**

As a popular, open-source software, MySQL, in its original or re-packaged form, is widely installed on many systems from various sources, including different software download sites, software repositories, and so on. The following instructions assume that MySQL is not already installed on your system using a third-party-distributed RPM package; if that is not the case, follow the instructions given at [Replacing](#page-157-0) [a Native Third-Party Distribution of MySQL.](#page-157-0)

![](_page_153_Picture_10.jpeg)

# **Note**

Repository setup RPM file names begin with mysql84, which describes the MySQL series that is enabled by default for installation. In this case, the MySQL 8.4 LTS subrepository is enabled by default. It also contains other subrepository versions, such as MySQL 8.0 and the MySQL Innovation Series, which are disabled by default.

# **Steps for a Fresh Installation of MySQL**

Follow these steps to choose and install the latest MySQL products:

# <span id="page-153-1"></span>**Adding the MySQL Yum Repository** 1.

Add the MySQL Yum repository to your system's repository list. This is typically a one-time operation that is performed by installing the RPM provided by MySQL. Follow these steps:

- a. Download it from the MySQL Yum Repository page ([https://dev.mysql.com/downloads/repo/](https://dev.mysql.com/downloads/repo/yum/) [yum/\)](https://dev.mysql.com/downloads/repo/yum/) in the MySQL Developer Zone.
- b. Select and download the release package for your platform.
- c. Install the downloaded release package. The package file format is:

```
mysql84-community-release-{platform}-{version-number}.noarch.rpm
```

- mysql84: Indicates the MySQL version that is enabled by default. In this case, MySQL 8.4 is enabled by default, and both MySQL 8.0 and the MySQL Innovation series are available but disabled by default.
- {platform}: The platform code, such as el7, el8, el9, fc41, or fc42. The 'el' represents Enterprise Linux, 'fc' for Fedora, and it ends with the platform's base version number.
- {version-number}: Version of the MySQL repository configuration RPM as they do receive occasional updates.

Install the RPM you downloaded for your system, for example:

```
$> sudo yum localinstall mysql84-community-release-{platform}-{version-number}.noarch.rpm
```

The installation command adds the MySQL Yum repository to your system's repository list and downloads the GnuPG key to check the integrity of the software packages. See [Section 2.1.4.2,](#page-88-2) ["Signature Checking Using GnuPG"](#page-88-2) for details on GnuPG key checking.

You can check that the MySQL Yum repository has been successfully added and enabled by the following command (for dnf-enabled systems, replace yum in the command with dnf):

```
$> yum repolist enabled | grep mysql.*-community
```

### Example output:

```
mysql-8.4-lts-community MySQL 8.4 LTS Community Server
mysql-tools-8.4-lts-community MySQL Tools 8.4 LTS Community
```

This also demonstrates that the latest LTS MySQL version is enabled by default. Methods to choose a different release series, such as the innovation track (which today is 9.6) or a previous series (such as MySQL 8.0), are described below.

![](_page_154_Picture_16.jpeg)

### **Note**

Once the MySQL Yum repository is enabled on your system, any systemwide update by the yum update command (or dnf upgrade for dnfenabled systems) upgrades MySQL packages on your system and replaces any native third-party packages, if Yum finds replacements for them in the MySQL Yum repository; see Section 3.8, "Upgrading MySQL with the MySQL Yum Repository", for a discussion on some possible effects of that on your system, see Upgrading the Shared Client Libraries.

# **Selecting a Release Series** 2.

When using the MySQL Yum repository, the latest bugfix series (currently MySQL 8.4) is selected for installation by default. If this is what you want, you can skip to the next step, [Installing MySQL](#page-156-0).

Within the MySQL Yum repository, each MySQL Community Server release series is hosted in a different subrepository. The subrepository for the latest LTS series (currently MySQL 8.4) is enabled by default, and the subrepositories for all other series' (for example, MySQL 8.0 and the MySQL Innovation series) are disabled by default. Use this command to see all available MySQLrelated subrepositories (for dnf-enabled systems, replace yum in the command with dnf):

```
$> yum repolist all | grep mysql
```

### Example output:

```
mysql-connectors-community MySQL Connectors Community enabled
mysql-tools-8.4-lts-community MySQL Tools 8.4 LTS Community enabled
mysql-tools-community MySQL Tools Community disabled
mysql-tools-innovation-community MySQL Tools Innovation Commu disabled
mysql-innovation-community MySQL Innovation Release Com disabled
mysql-8.4-lts-community MySQL 8.4 Community LTS Server enabled
mysql-8.4-lts-community-debuginfo MySQL 8.4 Community LTS Server - disabled
mysql-8.4-lts-community-source MySQL 8.4 Community LTS Server - disabled
mysql80-community MySQL 8.0 Community Server - disabled
mysql80-community-debuginfo MySQL 8.0 Community Server - disabled
mysql80-community-source MySQL 8.0 Community Server - disabled
```

To install the latest release from a specific series other than the latest LTS series, disable the bug subrepository for the latest LTS series and enable the subrepository for the specific series before running the installation command. If your platform supports the yum-config-manager or dnf config-manager command, you can do that by issuing the following commands to disable the subrepository for the 8.4 series and enable the one for the 8.0 series:

```
$> sudo yum-config-manager --disable mysql-8.4-lts-community
$> sudo yum-config-manager --enable mysql80-community
```

For dnf-enabled platforms:

```
$> sudo dnf config-manager --disable mysql-8.4-lts-community
$> sudo dnf config-manager --enable mysql80-community
```

Instead of using the config-manager commands you can manually edit the /etc/yum.repos.d/ mysql-community.repo file by toggling the enabled option. For example, a typical default entry for EL8:

```
[mysql-8.4-lts-community]
name=MySQL 8.4 LTS Community Server
baseurl=http://repo.mysql.com/yum/mysql-8.4-community/el/8/$basearch/
enabled=1
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-mysql-2025
```

Find the entry for the subrepository you want to configure and edit the enabled option. Specify enabled=0 to disable a subrepository or enabled=1 to enable a subrepository. For example, to install from the MySQL innovation track, make sure you have enabled=0 for the MySQL 8.4 subrepository entries and have enabled=1 for the innovation entries:

```
[mysql80-community]
name=MySQL 8.0 Community Server
baseurl=http://repo.mysql.com/yum/mysql-8.0-community/el/8/$basearch
enabled=1
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-mysql-2025
```

You should only enable subrepository for one release series at any time.

Verify that the correct subrepositories have been enabled and disabled by running the following command and checking its output (for dnf-enabled systems, replace yum in the command with dnf):

```
$> yum repolist enabled | grep mysql
```

# **Disabling the Default MySQL Module** 3.

(EL8 systems only) EL8-based systems such as RHEL8 and Oracle Linux 8 include a MySQL module that is enabled by default. Unless this module is disabled, it masks packages provided by MySQL repositories. To disable the included module and make the MySQL repository packages visible, use the following command (for dnf-enabled systems, replace yum in the command with dnf):

\$> **sudo yum module disable mysql**

# <span id="page-156-0"></span>4. **Installing MySQL**

Install MySQL by the following command (for dnf-enabled systems, replace yum in the command with dnf):

```
$> sudo yum install mysql-community-server
```

This installs the package for MySQL server (mysql-community-server) and also packages for the components required to run the server, including packages for the client (mysql-communityclient), the common error messages and character sets for client and server (mysqlcommunity-common), and the shared client libraries (mysql-community-libs).

# **Starting the MySQL Server** 5.

Start the MySQL server with the following command:

```
$> systemctl start mysqld
```

You can check the status of the MySQL server with the following command:

```
$> systemctl status mysqld
```

If the operating system is systemd enabled, standard systemctl (or alternatively, service with the arguments reversed) commands such as stop, start, status, and restart should be used to manage the MySQL server service. The mysqld service is enabled by default, and it starts at system reboot. See [Section 2.5.9, "Managing MySQL Server with systemd"](#page-192-1) for additional information.

At the initial start up of the server, the following happens, given that the data directory of the server is empty:

- The server is initialized.
- SSL certificate and key files are generated in the data directory.
- validate\_password is installed and enabled.
- A superuser account 'root'@'localhost is created. A password for the superuser is set and stored in the error log file. To reveal it, use the following command:

```
$> sudo grep 'temporary password' /var/log/mysqld.log
```

Change the root password as soon as possible by logging in with the generated, temporary password and set a custom password for the superuser account:

```
$> mysql -uroot -p
```

mysql> **ALTER USER 'root'@'localhost' IDENTIFIED BY 'MyNewPass4!';**

![](_page_156_Picture_23.jpeg)

### **Note**

validate\_password is installed by default. The default password policy implemented by validate\_password requires that passwords contain at least one uppercase letter, one lowercase letter, one digit, and one special character, and that the total password length is at least 8 characters.

For more information on the postinstallation procedures, see Section 2.9, "Postinstallation Setup and Testing".

<span id="page-157-2"></span>![](_page_157_Picture_2.jpeg)

### **Note**

Compatibility Information for EL7-based platforms: The following RPM packages from the native software repositories of the platforms are incompatible with the package from the MySQL Yum repository that installs the MySQL server. Once you have installed MySQL using the MySQL Yum repository, you cannot install these packages (and vice versa).

• akonadi-mysql

# <span id="page-157-1"></span>**Installing Additional MySQL Products and Components with Yum**

You can use Yum to install and manage individual components of MySQL. Some of these components are hosted in sub-repositories of the MySQL Yum repository: for example, the MySQL Connectors are to be found in the MySQL Connectors Community sub-repository, and the MySQL Workbench in MySQL Tools Community. You can use the following command to list the packages for all the MySQL components available for your platform from the MySQL Yum repository (for dnf-enabled systems, replace yum in the command with dnf):

```
$> sudo yum --disablerepo=\* --enablerepo='mysql*-community*' list available
```

Install any packages of your choice with the following command, replacing package-name with name of the package (for dnf-enabled systems, replace yum in the command with dnf):

```
$> sudo yum install package-name
```

For example, to install MySQL Workbench on Fedora:

```
$> sudo dnf install mysql-workbench-community
```

To install the shared client libraries (for dnf-enabled systems, replace yum in the command with dnf):

```
$> sudo yum install mysql-community-libs
```

# **Platform Specific Notes**

ARM Support

ARM 64-bit (aarch64) is supported on Oracle Linux 7 and requires the Oracle Linux 7 Software Collections Repository (ol7\_software\_collections). For example, to install the server:

```
$> yum-config-manager --enable ol7_software_collections
$> yum install mysql-community-server
```

# **Updating MySQL with Yum**

Besides installation, you can also perform updates for MySQL products and components using the MySQL Yum repository. See Section 3.8, "Upgrading MySQL with the MySQL Yum Repository" for details.

# <span id="page-157-0"></span>**Replacing a Native Third-Party Distribution of MySQL**

If you have installed a third-party distribution of MySQL from a native software repository (that is, a software repository provided by your own Linux distribution), follow these steps:

# **Backing Up Your Database** 1.

To avoid loss of data, always back up your database before trying to replace your MySQL installation using the MySQL Yum repository. See Chapter 9, Backup and Recovery, on how to back up your database.

# **Adding the MySQL Yum Repository** 2.

Add the MySQL Yum repository to your system's repository list by following the instructions given in [Adding the MySQL Yum Repository.](#page-153-1)

# **Replacing the Native Third-Party Distribution by a Yum Update or a DNF Upgrade** 3.

By design, the MySQL Yum repository replaces your native, third-party MySQL with the latest bugfix release from the MySQL Yum repository when you perform a yum update command (or dnf upgrade for dnf-enabled systems) on the system, or a yum update mysql-server (or dnf upgrade mysql-server for dnf-enabled systems).

After updating MySQL using the Yum repository, applications compiled with older versions of the shared client libraries should continue to work. However, if you want to recompile applications and dynamically link them with the updated libraries, see Upgrading the Shared Client Libraries, for some special considerations.

![](_page_158_Picture_6.jpeg)

### **Note**

For EL7-based platforms: See [Compatibility Information for EL7-based](#page-157-2) [platforms \[128\]](#page-157-2).

# <span id="page-158-0"></span>**2.5.2 Installing MySQL on Linux Using the MySQL APT Repository**

This section provides guidance on installing MySQL using the MySQL APT repository.

# **Steps for a Fresh Installation of MySQL**

![](_page_158_Picture_12.jpeg)

### **Note**

The following instructions assume that no version of MySQL (whether distributed by Oracle or other parties) has already been installed on your system; if that is not the case, follow the instructions given in [Replacing a Native](#page-162-0) [Distribution of MySQL Using the MySQL APT Repository](#page-162-0) or [Replacing a MySQL](#page-163-0) [Server Installed by a Direct deb Package Download](#page-163-0) instead.

<span id="page-158-1"></span>**Adding the MySQL Apt Repository.** First, add the MySQL APT repository to your system's software repository list. Follow these steps:

- 1. Go to the download page for the MySQL APT repository at [https://dev.mysql.com/downloads/repo/](https://dev.mysql.com/downloads/repo/apt/) [apt/.](https://dev.mysql.com/downloads/repo/apt/)
- 2. Select and download the release package for your Linux distribution.

Although this is not required for each update, it does update MySQL repository information to include the current information, which includes adding a new LTS series.

3. Install the downloaded release package with the following command, replacing versionspecific-package-name with the name of the downloaded package (preceded by its path, if you are not running the command inside the folder where the package is):

\$> **sudo dpkg -i /PATH/version-specific-package-name.deb**

For example, for version w.x.y-z of the package, the command is:

\$> **sudo dpkg -i mysql-apt-config\_w.x.y-z\_all.deb**

Note that the same package works on all supported Debian and Ubuntu platforms.

4. During the installation of the package, you will be asked to choose the versions of the MySQL server and other components (for example, the MySQL Workbench) that you want to install. If you are not sure which version to choose, do not change the default options selected for you. You can also choose **none** if you do not want a particular component to be installed. After making the choices for all components, choose **Ok** to finish the configuration and installation of the release package.

![](_page_159_Picture_2.jpeg)

### **Note**

The innovation track, which begins with MySQL 8.1, includes "-innovation-" in the component name.

You can always change your choices for the versions later; see [Selecting a Major Release Version](#page-159-0) for instructions.

5. Update package information from the MySQL APT repository with the following command (this step is mandatory):

```
$> sudo apt-get update
```

Instead of using the release package, you can also add and configure the MySQL APT repository manually; see [Appendix A: Adding and Configuring the MySQL APT Repository Manually](#page-166-0) for details.

![](_page_159_Picture_9.jpeg)

### **Note**

Once the MySQL APT repository is enabled on your system, you will no longer be able to install any MySQL packages from your platform's native software repositories until the MySQL APT repository is disabled.

![](_page_159_Picture_12.jpeg)

### **Note**

Once the MySQL APT repository is enabled on your system, any systemwide upgrade by the apt-get upgrade command will automatically upgrade the MySQL packages on your system and also replace any native MySQL packages you installed from your Linux distribution's software repository, if APT finds replacements for them from within the MySQL APT repository.

# <span id="page-159-0"></span>**Selecting a Major Release Version**

By default, all installations and upgrades for your MySQL server and the other required components come from the release series of the major version you have selected during the installation of the configuration package (see [Adding the MySQL Apt Repository](#page-158-1)). However, you can switch to another supported major release series at any time by reconfiguring the configuration package you have installed. Use the following command:

```
$> sudo dpkg-reconfigure mysql-apt-config
```

A dialogue box then asks you to choose the major release version you want. Make your selection and choose **Ok**. After returning to the command prompt, update package information from the MySQL APT repository with this command:

```
$> sudo apt-get update
```

The latest version in the selected series will then be installed when you use the apt-get install command next time.

You can use the same method to change the version for any other MySQL component you want to install with the MySQL APT repository.

# <span id="page-159-1"></span>**Installing MySQL with APT**

Install MySQL by the following command:

```
$> sudo apt-get install mysql-server
```

This installs the package for the MySQL server, as well as the packages for the client and for the database common files.

During the installation, you are asked to supply a password for the root user for your MySQL installation.

![](_page_160_Picture_3.jpeg)

### **Important**

Make sure you remember the root password you set. Users who want to set a password later can leave the **password** field blank in the dialogue box and just press **Ok**; in that case, root access to the server will be authenticated by Section 8.4.1.10, "Socket Peer-Credential Pluggable Authentication" for connections using a Unix socket file. You can set the root password later using the program mysql\_secure\_installation.

# <span id="page-160-0"></span>**Starting and Stopping the MySQL Server**

The MySQL server is started automatically after installation. You can check the status of the MySQL server with the following command:

```
$> systemctl status mysql
```

If the operating system is systemd enabled, standard systemctl (or alternatively, service with the arguments reversed) commands such as stop, start, status, and restart should be used to manage the MySQL server service. The mysql service is enabled by default, and it starts at system reboot. See [Section 2.5.9, "Managing MySQL Server with systemd"](#page-192-1) for additional information.

![](_page_160_Picture_10.jpeg)

### **Note**

A few third-party native repository packages that have dependencies on the native MySQL packages may not work with the MySQL APT repository packages and should not be used together with them; these include akonadibackend-mysql, handlersocket-mysql-5.5, and zoneminder.

# <span id="page-160-1"></span>**Installing Additional MySQL Products and Components with APT**

You can use APT to install individual components of MySQL from the MySQL APT repository. Assuming you already have the MySQL APT repository on your system's repository list (see [Adding](#page-158-1) [the MySQL Apt Repository](#page-158-1) for instructions), first, use the following command to get the latest package information from the MySQL APT repository:

```
$> sudo apt-get update
```

Install any packages of your choice with the following command, replacing package-name with name of the package to install:

```
$> sudo apt-get install package-name
```

For example, to install the MySQL Workbench:

```
$> sudo apt-get install mysql-workbench-community
```

To install the shared client libraries:

\$> **sudo apt-get install libmysqlclient21**

# **Installing MySQL from Source with the MySQL APT Repository**

![](_page_160_Picture_23.jpeg)

### **Note**

This feature is only supported on 64-bit systems.

You can download the source code for MySQL and build it using the MySQL APT Repository:

- 1. Add the MySQL APT repository to your system's repository list and choose the major release series you want (see [Adding the MySQL Apt Repository](#page-158-1) for instructions).
- 2. Update package information from the MySQL APT repository with the following command (this step is mandatory):

```
$> sudo apt-get update
```

3. Install packages that the build process depends on:

```
$> sudo apt-get build-dep mysql-server
```

4. Download the source code for the major components of MySQL and then build them (run this command in the folder in which you want the downloaded files and the builds to be located):

```
$> apt-get source -b mysql-server
```

deb packages for installing the various MySQL components are created.

5. Pick the deb packages for the MySQL components you need and install them with the command:

```
$> sudo dpkg -i package-name.deb
```

Notice that dependency relationships exist among the MySQL packages. For a basic installation of the MySQL server, install the database common files package, the client package, the client metapackage, the server package, and the server metapackage (in that order) with the following steps:

• Preconfigure the MySQL server package with the following command:

```
$> sudo dpkg-preconfigure mysql-community-server_version-and-platform-specific-part.deb
```

You will be asked to provide a password for the root user for your MySQL installation; see important information on root password given in [Installing MySQL with APT](#page-159-1) above. You might also be asked other questions regarding the installation.

• Install the required packages with a single command:

```
$> sudo dpkg -i mysql-{common,community-client,client,community-server,server}_*.deb
```

• If you are being warned of unmet dependencies by dpkg, you can fix them using apt-get:

```
sudo apt-get -f install
```

Here are where the files are installed on the system:

- All configuration files (like my.cnf) are under /etc/mysql
- All binaries, libraries, headers, etc., are under /usr/bin and /usr/sbin
- The data directory is under /var/lib/mysql

See also information given in [Starting and Stopping the MySQL Server](#page-160-0).

# <span id="page-161-0"></span>**Upgrading MySQL with the MySQL APT Repository**

![](_page_161_Picture_25.jpeg)

### **Notes**

- Before performing any upgrade to MySQL, follow carefully the instructions in Chapter 3, Upgrading MySQL. Among other instructions discussed there, it is especially important to back up your database before the upgrade.
- The following instructions assume that MySQL has been installed on your system using the MySQL APT repository; if that is not the case, follow

the instructions given in [Replacing a Native Distribution of MySQL Using](#page-162-0) [the MySQL APT Repository](#page-162-0) or [Replacing a MySQL Server Installed by a](#page-163-0) [Direct deb Package Download](#page-163-0) instead. Also notice that you cannot use the MySQL APT repository to upgrade a distribution of MySQL that you have installed from a nonnative software repository (for example, from MariaDB or Percona).

Use the MySQL APT repository to perform an in-place upgrade for your MySQL installation (that is, replacing the old version and then running the new version using the old data files) by following these steps:

- 1. Make sure you already have the MySQL APT repository on your system's repository list (see [Adding the MySQL Apt Repository](#page-158-1) for instructions).
- 2. Make sure you have the most up-to-date package information on the MySQL APT repository by running:

```
$> sudo apt-get update
```

3. Note that, by default, the MySQL APT repository will update MySQL to the release series you have selected when you were [adding the MySQL APT repository to your system](#page-158-1). If you want to upgrade to another release series, select it by following the steps given in [Selecting a Major](#page-159-0) [Release Version](#page-159-0).

As a general rule, to upgrade from one release series to another, go to the next series rather than skipping a series. For example, if you are currently running MySQL 5.7 and wish to upgrade to a newer series, upgrade to MySQL 8.0 first before upgrading to 8.4.

![](_page_162_Picture_8.jpeg)

### **Important**

In-place downgrading of MySQL is not supported by the MySQL APT repository. Follow the instructions in Chapter 4, Downgrading MySQL.

<span id="page-162-1"></span>4. Upgrade MySQL by the following command:

```
$> sudo apt-get install mysql-server
```

The MySQL server, client, and the database common files are upgraded if newer versions are available. To upgrade any other MySQL package, use the same apt-get install command and supply the name for the package you want to upgrade:

```
$> sudo apt-get install package-name
```

To see the names of the packages you have installed from the MySQL APT repository, use the following command:

```
$> dpkg -l | grep mysql | grep ii
```

![](_page_162_Picture_17.jpeg)

### **Note**

If you perform a system-wide upgrade using apt-get upgrade, only the MySQL library and development packages are upgraded with newer versions (if available). To upgrade other components including the server, client, test suite, etc., use the apt-get install command.

5. The MySQL server always restarts after an update by APT.

# <span id="page-162-0"></span>**Replacing a Native Distribution of MySQL Using the MySQL APT Repository**

Variants and forks of MySQL are distributed by different parties through their own software repositories or download sites. You can replace a native distribution of MySQL installed from your Linux platform's software repository with a distribution from the MySQL APT repository in a few steps.

![](_page_163_Picture_1.jpeg)

### **Note**

The MySQL APT repository can only replace distributions of MySQL maintained and distributed by Debian or Ubuntu. It cannot replace any MySQL forks found either inside or outside of the distributions' native repositories. To replace such MySQL forks, you have to uninstall them first before you install MySQL using the MySQL APT repository. Follow the instructions for uninstallation from the forks' distributors and, before you proceed, make sure you back up your data and you know how to restore them to a new server.

![](_page_163_Picture_4.jpeg)

### **Warning**

A few third-party native repository packages that have dependencies on the native MySQL packages may not work with the MySQL APT repository packages and should not be used together with them; these include akonadibackend-mysql, handlersocket-mysql-5.5, and zoneminder.

# **Backing Up Your Database** 1.

To avoid loss of data, always back up your database before trying to replace your MySQL installation using the MySQL APT repository. See Chapter 9, Backup and Recovery for instructions.

## **Adding the MySQL APT Repository and Selecting a Release Series** 2.

Add the MySQL APT repository to your system's repository list and select the release series you want by following the instructions given in [Adding the MySQL Apt Repository](#page-158-1).

## <span id="page-163-1"></span>**Replacing the Native Distribution by an APT Update** 3.

By design, the MySQL APT repository replaces your native distribution of MySQL when you perform upgrades on the MySQL packages. To perform the upgrades, follow the same instructions given in [Step 4](#page-162-1) in [Upgrading MySQL with the MySQL APT Repository.](#page-161-0)

![](_page_163_Picture_13.jpeg)

### **Warning**

Once the native distribution of MySQL has been replaced using the MySQL APT repository, purging the old MySQL packages from the native repository using the apt-get purge, apt-get remove --purge, or dpkg -P command might impact the newly installed MySQL server in various ways. Therefore, do not purge the old MySQL packages from the native repository packages.

# <span id="page-163-0"></span>**Replacing a MySQL Server Installed by a Direct deb Package Download**

deb packages from MySQL for installing the MySQL server and its components can either be downloaded from the [MySQL Developer Zone's MySQL Download page](https://dev.mysql.com/downloads/) or from the MySQL APT repository. The deb packages from the two sources are different, and they install and configure MySQL in different ways.

If you have installed MySQL with the MySQL Developer Zone's deb packages and now want to replace the installation using the ones from the MySQL APT repository, follow these steps:

- 1. Back up your database. See Chapter 9, Backup and Recovery for instructions.
- 2. Follow the steps given previously for [adding the MySQL APT repository.](#page-158-1)
- 3. Remove the old installation of MySQL by running:

```
$> sudo dpkg -P mysql
```

4. Install MySQL from the MySQL APT repository:

```
$> sudo apt-get install mysql-server
```

5. If needed, restore the data on the new MySQL installation. See Chapter 9, Backup and Recovery for instructions.

### **Removing MySQL with APT**

To uninstall the MySQL server and the related components that have been installed using the MySQL APT repository, first, remove the MySQL server using the following command:

```
$> sudo apt-get remove mysql-server
```

Then, remove any other software that was installed automatically with the MySQL server:

```
$> sudo apt-get autoremove
```

To uninstall other components, use the following command, replacing **package-name** with the name of the package of the component you want to remove:

```
$> sudo apt-get remove package-name
```

To see a list of packages you have installed from the MySQL APT repository, use the following command:

```
$> dpkg -l | grep mysql | grep ii
```

### **Special Notes on Upgrading the Shared Client Libraries**

You can install the shared client libraries from MySQL APT repository by the following command (see [Installing Additional MySQL Products and Components with APT](#page-160-1) for more details):

```
$> sudo apt-get install libmysqlclient21
```

If you already have the shared client libraries installed from you Linux platform's software repository, it can be updated by the MySQL APT repository with its own package by using the same command (see [Replacing the Native Distribution by an APT Update](#page-163-1) for more details).

After updating MySQL using the APT repository, applications compiled with older versions of the shared client libraries should continue to work.

If you recompile applications and dynamically link them with the updated libraries: as typical with new versions of shared libraries, any applications compiled using the updated, newer shared libraries might require those updated libraries on systems where the applications are deployed. If those libraries are not in place, the applications requiring the shared libraries might fail. Therefore, it is recommended that the packages for the shared libraries from MySQL be deployed on those systems. You can do this by adding the MySQL APT repository to the systems (see [Adding the MySQL Apt Repository\)](#page-158-1) and installing the latest shared client libraries using the command given at the beginning of this section.

# **Installing MySQL NDB Cluster Using the APT Repository**

![](_page_164_Picture_18.jpeg)

### **Notes**

- The MySQL APT repository supports installation of MySQL NDB Cluster on Debian and Ubuntu systems. For methods to install NDB Cluster on other Debian-based systems, see [Installing NDB Cluster Using .deb Files.](https://dev.mysql.com/doc/refman/5.7/en/mysql-cluster-install-debian.md)
- If you already have the MySQL server or MySQL NDB Cluster installed on your system, make sure it is stopped and you have your data and configuration files backed up before proceeding.

### <span id="page-164-0"></span>**Adding the MySQL APT Repository for MySQL NDB Cluster** 1.

Follow the steps in [Adding the MySQL Apt Repository](#page-158-1) to add the MySQL APT repository to your system's repository list. During the installation process of the configuration package, when you are asked which MySQL product you want to configure, choose "MySQL Server & Cluster"; when asked which version you wish to receive, choose "mysql-cluster-x.y." After returning to the command prompt, go to Step 2 below.

If you already have the configuration package installed on your system, make sure it is up-to-date by running the following command:

```
$> sudo apt-get install mysql-apt-config
```

Then, use the same method described in [Selecting a Major Release Version](#page-159-0) to select MySQL NDB Cluster for installation. When you are asked which MySQL product you want to configure, choose "MySQL Server & Cluster"; when asked which version you wish to receive, choose "mysqlcluster-x.y." After returning to the command prompt, update package information from the MySQL APT repository with this command:

```
$> sudo apt-get update
```

### **Installing MySQL NDB Cluster** 2.

For a minimal installation of MySQL NDB Cluster, follow these steps:

• Install the components for SQL nodes:

```
$> sudo apt-get install mysql-cluster-community-server
```

You will be asked to provide a password for the root user for your SQL node; see important information on the root password given in [Installing MySQL with APT](#page-159-1) above. You might also be asked other questions regarding the installation.

• Install the executables for management nodes:

```
$> sudo apt-get install mysql-cluster-community-management-server
```

• Install the executables for data nodes:

```
$> sudo apt-get install mysql-cluster-community-data-node
```

### **Configuring and Starting MySQL NDB Cluster** 3.

See Section 25.3.3, "Initial Configuration of NDB Cluster" on how to configure MySQL NDB Cluster and Section 25.3.4, "Initial Startup of NDB Cluster" on how to start it for the first time. When following those instructions, adjust them according to the following details regarding the SQL nodes of your NDB Cluster installation:

- All configuration files (like my.cnf) are under /etc/mysql
- All binaries, libraries, headers, etc., are under /usr/bin and /usr/sbin
- The data directory is /var/lib/mysql

# **Installing Additional MySQL NDB Cluster Products and Components**

You can use APT to install individual components and additional products of MySQL NDB Cluster from the MySQL APT repository. To do that, assuming you already have the MySQL APT repository on your system's repository list (see [Adding the MySQL Apt Repository for MySQL NDB Cluster](#page-164-0)), follow the same steps given in [Installing Additional MySQL Products and Components with APT](#page-160-1).

![](_page_165_Picture_22.jpeg)

### **Note**

Known issue: Currently, not all components required for running the MySQL NDB Cluster test suite are installed automatically when you install the test suite package (mysql-cluster-community-test). Install the following packages with apt-get install before you run the test suite:

- mysql-cluster-community-auto-installer
- mysql-cluster-community-management-server
- mysql-cluster-community-data-node
- mysql-cluster-community-memcached
- mysql-cluster-community-java
- ndbclient-dev

# <span id="page-166-0"></span>**Appendix A: Adding and Configuring the MySQL APT Repository Manually**

Here are the steps for adding manually the MySQL APT repository to your system's software repository list and configuring it, without using the release packages provided by MySQL:

• Download the MySQL GPG Public key (see [Section 2.1.4.2, "Signature Checking Using GnuPG"](#page-88-2) on how to do that) and save it to a file, without adding any spaces or special characters. Then, add the key to your system's GPG keyring with the following command:

\$> **sudo apt-key add path/to/signature-file**

• Alternatively, you can download the GPG key to your APT keyring directly using the apt-key utility:

\$> **sudo apt-key adv --keyserver pgp.mit.edu --recv-keys A8D3785C**

![](_page_166_Picture_13.jpeg)

### **Note**

The KeyID for MySQL 8.0.36 and later release packages is A8D3785C, as shown above. For earlier MySQL releases, the keyID is 3A79BD29. Using an incorrect key can cause a key verification error.

• Create a file named /etc/apt/sources.list.d/mysql.list, and put into it repository entries in the following format (this is not a command to execute):

deb http://repo.mysql.com/apt/{debian|ubuntu}/ {bookworm|jammy} {mysql-tools|mysql-8.4-lts|mysql-8.0}

Pick the relevant options for your repository set up:

- Choose "debian" or "ubuntu" according to your platform.
- Choose the appropriate version name for the version of your system; examples include "bookworm" (for Debian 12) and "jammy" (for Ubuntu 22.04).
- For installing the MySQL server, client, and database common files, choose "mysql-8.4", "mysql-8.0", or "mysql-innovation" according to the [MySQL series](#page-38-0) you want. To switch to another release series later, come back and adjust the entry with your new choice. This also includes access to tools such as MySQL Router and MySQL Shell.

![](_page_166_Picture_22.jpeg)

### **Note**

If you already have a version of MySQL installed on your system, do not choose a lower version at this step, or it might result in an unsupported downgrade operation.

• Include "mysql-tools" to install a connector.

For example, on the Ubuntu 22.04 platform use these lines in your mysql.list files to install MySQL 8.4 and the latest MySQL Connectors from the MySQL APT repository:

deb http://repo.mysql.com/apt/ubuntu/ jammy mysql-8.4 mysql-tools

• Use the following command to get the most up-to-date package information from the MySQL APT repository:

```
$> sudo apt-get update
```

You have configured your system to use the MySQL APT repository and are now ready to continue with [Installing MySQL with APT](#page-159-1) or [Installing Additional MySQL Products and Components with APT.](#page-160-1)

# <span id="page-167-0"></span>**2.5.3 Using the MySQL SLES Repository**

The MySQL SLES repository provides RPM packages for installing and managing the MySQL server, client, and other components on SUSE Enterprise Linux Server. This section contains information on obtaining and installing these packages.

# <span id="page-167-2"></span>**Adding the MySQL SLES Repository**

Add or update the official MySQL SLES repository for your system's repository list:

![](_page_167_Picture_8.jpeg)

### **Note**

The beginning part of the configuration file name, such as mysql84, describes the default MySQL series that is enabled for installation. In this case, the subrepository for MySQL 8.4 LTS is enabled by default. It also contains other subrepository versions, such as MySQL 8.0 and the MySQL Innovation Series.

### **New MySQL Repository Installation**

If the MySQL repository is not yet present on the system then:

- 1. Go to the download page for MySQL SLES repository at [https://dev.mysql.com/downloads/repo/](https://dev.mysql.com/downloads/repo/suse/) [suse/.](https://dev.mysql.com/downloads/repo/suse/)
- 2. Select and download the release package for your SLES version.
- 3. Install the downloaded release package with the following command, replacing package-name with the name of the downloaded package:

```
$> sudo rpm -Uvh package-name.rpm
```

For example, to install the SLES 15 package where # indicates the release number within a version such as 15-1:

```
$> sudo rpm -Uvh mysql84-community-release-sl15-#.noarch.rpm
```

# **Update an Existing MySQL Repository Installation**

If an older version is already present then update it:

- \$> **sudo zypper update mysql84-community-release**
- Although this is not required for each MySQL release, it does update MySQL repository information to include the current information. For example, mysql84-community-releasesl15-7.noarch.rpm is the first SUSE 15 repository configuration file that adds the innovation release track that begins with MySQL 8.1. series.

# <span id="page-167-1"></span>**Selecting a Release Series**

Within the MySQL SLES repository, different release series of the MySQL Community Server are hosted in different subrepositories. The subrepository for the latest bugfix series (currently MySQL 8.4) is enabled by default, and the subrepositories for all other series are disabled. Use this command to see all of the subrepositories in the MySQL SLES repository, and to see which of them are enabled or disabled:

```
$> zypper repos | grep mysql.*community
```

The innovation track is available for SLES 15 with entries such as mysql-innovation-community.

To install the latest release from a specific series, before running the installation command, make sure that the subrepository for the series you want is enabled and the subrepositories for other series are disabled. For example, on SLES 15, to disable the subrepositories for MySQL 8.4 server and tools, which are enabled by default, use the following:

```
$> sudo zypper modifyrepo -d mysql-8.4-lts-community
$> sudo zypper modifyrepo -d mysql-tools-community
```

Then, enable the subrepositories for the release series you want. For example, to enable the Innovation track on SLES 15:

```
$> sudo zypper modifyrepo -e mysql-innovation-community
$> sudo zypper modifyrepo -e mysql-tools-innovation-community
```

You should only enable a subrepository for one release series at any time.

Verify that the correct subrepositories have been enabled by running the following command and checking its output:

```
$> zypper repos -E | grep mysql.*community
 7 | mysql-connectors-community | MySQL Connectors Community | Yes | (r ) Yes | No
10 | mysql-innovation-community | MySQL Innovation Release Community Server | Yes | (r ) Yes | No
16 | mysql-tools-innovation-community | MySQL Tools Innovation Community | Yes | ( p) Yes | No
```

After that, use the following command to refresh the repository information for the enabled subrepository:

```
$> sudo zypper refresh
```

# <span id="page-168-0"></span>**Installing MySQL with Zypper**

With the official MySQL repository enabled, install MySQL Server:

```
$> sudo zypper install mysql-community-server
```

This installs the package for the MySQL server, as well as other required packages.

# <span id="page-168-1"></span>**Starting the MySQL Server**

Start the MySQL server with the following command:

```
$> systemctl start mysql
```

You can check the status of the MySQL server with the following command:

```
$> systemctl status mysql
```

If the operating system is systemd enabled, standard systemctl (or alternatively, service with the arguments reversed) commands such as stop, start, status, and restart should be used to manage the MySQL server service. The mysql service is enabled by default, and it starts at system reboot. See [Section 2.5.9, "Managing MySQL Server with systemd"](#page-192-1) for additional information.

MySQL Server Initialization: When the server is started for the first time, the server is initialized, and the following happens (if the data directory of the server is empty when the initialization process begins):

- The SSL certificate and key files are generated in the data directory.
- The validate\_password plugin is installed and enabled.
- A superuser account 'root'@'localhost' is created. A password for the superuser is set and stored in the error log file. To reveal it, use the following command:

\$> **sudo grep 'temporary password' /var/log/mysql/mysqld.log**

Change the root password as soon as possible by logging in with the generated, temporary password and set a custom password for the superuser account:

\$> **mysql -uroot -p** 

mysql> **ALTER USER 'root'@'localhost' IDENTIFIED BY 'MyNewPass4!';**

![](_page_169_Picture_5.jpeg)

### **Note**

MySQL's validate\_password plugin is installed by default. This will require that passwords contain at least one uppercase letter, one lowercase letter, one digit, and one special character, and that the total password length is at least 8 characters.

You can stop the MySQL Server with the following command:

\$> **sudo systemctl stop mysql**

# <span id="page-169-0"></span>**Installing Additional MySQL Products and Components**

You can install more components of MySQL. List subrepositories in the MySQL SLES repository with the following command:

```
$> zypper repos | grep mysql.*community
```

Use the following command to list the packages for the MySQL components available for a certain subrepository, changing subrepo-name to the name of the subrepository you are interested in :

```
$> zypper packages subrepo-name
```

Install any packages of your choice with the following command, replacing package-name with name of the package (you might need to enable first the subrepository for the package, using the same method for selecting a subrepository for a specific release series outlined in [Selecting a Release](#page-167-1) [Series](#page-167-1)):

```
$> sudo zypper install package-name
```

For example, to install the MySQL benchmark suite from the subrepository for the release series you have already enabled:

\$> **sudo zypper install mysql-community-bench**

# **Upgrading MySQL with the MySQL SLES Repository**

![](_page_169_Picture_20.jpeg)

### **Note**

• Before performing any update to MySQL, follow carefully the instructions in Chapter 3, Upgrading MySQL. Among other instructions discussed there, it is especially important to back up your database before the update.

Use the MySQL SLES repository to perform an in-place update (that is, replacing the old version of the server and then running the new version using the old data files) for your MySQL installation by following these steps (they assume you have installed MySQL with the MySQL SLES repository; if that is not the case, following the instructions in [Replacing MySQL Installed by an RPM from Other Sources](#page-170-0) instead):

### **Selecting a Target Series** 1.

During an update operation, by default, the MySQL SLES repository updates MySQL to the latest version in the release series you have chosen during installation (see [Selecting a Release Series](#page-167-1)

for details), which means. For example, a bugfix series installation, such as 8.4, will not update to an innovation series, such as 9.6. To update to another release series, you need to first disable the subrepository for the series that has been selected (by default, or by yourself) and enable the subrepository for your target series. To do that, follow the general instructions given in [Selecting a](#page-167-1) [Release Series.](#page-167-1)

As a general rule, to upgrade from one release series to another, go to the next series rather than skipping a series.

![](_page_170_Picture_3.jpeg)

### **Important**

In-place downgrading of MySQL is not supported by the MySQL SLES repository. Follow the instructions in Chapter 4, Downgrading MySQL.

# **Upgrading MySQL** 2.

Upgrade MySQL and its components by the following command:

```
$> sudo zypper update mysql-community-server
```

Alternatively, you can update MySQL by telling Zypper to update everything on your system (this might take considerably more time):

```
$> sudo zypper update
```

You can also update a specific component only. Use the following command to list all the installed packages from the MySQL SLES repository:

```
$> zypper packages -i | grep mysql-.*community
```

After identifying the package name of the component of your choice, update the package with the following command, replacing package-name with the name of the package:

```
$> sudo zypper update package-name
```

# <span id="page-170-0"></span>**Replacing MySQL Installed by an RPM from Other Sources**

RPMs for installing the MySQL Community Server and its components can be downloaded from MySQL either from the [MySQL Developer Zone,](https://dev.mysql.com/downloads/) from the native software repository of SLES, or from the MySQL SLES repository. The RPMs from the those sources might be different, and they might install and configure MySQL in different ways.

If you have installed MySQL with RPMs from the MySQL Developer Zone or the native software repository of SLES and want to replace the installation using the RPM from the MySQL SLES repository, follow these steps:

- 1. Back up your database to avoid data loss. See Chapter 9, Backup and Recovery on how to do that.
- 2. Stop your MySQL Server, if it is running. If the server is running as a service, you can stop it with the following command:

```
$> systemctl stop mysql
```

- 3. Follow the steps given for [Adding the MySQL SLES Repository](#page-167-2).
- 4. Follow the steps given for [Selecting a Release Series](#page-167-1).
- 5. Follow the steps given for [Installing MySQL with Zypper](#page-168-0). You will be asked if you want to replace the old packages with the new ones; for example:

```
Problem: mysql-community-server-5.6.22-2.sles11.x86_64 requires mysql-community-client = 5.6.22-2.sles11,
 but this requirement cannot be provided uninstallable providers:
 mysql-community-client-5.6.22-2.sles11.x86_64[mysql56-community]
```

```
 Solution 1: replacement of mysql-client-5.5.31-0.7.10.x86_64 with mysql-community-client-5.6.22-2.sles11.x86_64
 Solution 2: do not install mysql-community-server-5.6.22-2.sles11.x86_64
 Solution 3: break mysql-community-server-5.6.22-2.sles11.x86_64 by ignoring some of its dependencies
Choose from above solutions by number or cancel [1/2/3/c] (c)
```

Choose the "replacement" option ("Solution 1" in the example) to finish your installation from the MySQL SLES repository.

# <span id="page-171-0"></span>**Installing MySQL NDB Cluster Using the SLES Repository**

- The following instructions assume that neither the MySQL Server nor MySQL NDB Cluster has already been installed on your system; if that is not the case, remove the MySQL Server or MySQL NDB Cluster, including all its executables, libraries, configuration files, log files, and data directories, before you continue. However there is no need to remove the release package you might have used to enable the MySQL SLES repository on your system.
- The NDB Cluster Auto-Installer package has a dependency on the python2-crypto and pythonparamiko packages. Zypper can take care of this dependency if the Python repository has been enabled on your system.

# **Selecting the MySQL NDB Cluster Subrepository**

Within the MySQL SLES repository, the MySQL Community Server and MySQL NDB Cluster are hosted in different subrepositories. By default, the subrepository for the latest bugfix series of the MySQL Server is enabled and the subrepository for MySQL NDB Cluster is disabled. To install NDB Cluster, disable the subrepository for the MySQL Server and enable the subrepository for NDB Cluster. For example, disable the subrepository for MySQL 8.4, which is enabled by default, with the following command:

```
$> sudo zypper modifyrepo -d mysql-8.4-lts-community
```

Then, enable the subrepository for MySQL NDB Cluster:

```
$> sudo zypper modifyrepo -e mysql-cluster-8.4-community
```

Verify that the correct subrepositories have been enabled by running the following command and checking its output:

```
$> zypper repos -E | grep mysql.*community
10 | mysql-cluster-8.4-community | MySQL Cluster 8.4 Community | Yes | No
```

After that, use the following command to refresh the repository information for the enabled subrepository:

```
$> sudo zypper refresh
```

# **Installing MySQL NDB Cluster**

For a minimal installation of MySQL NDB Cluster, follow these steps:

• Install the components for SQL nodes:

```
$> sudo zypper install mysql-cluster-community-server
```

After the installation is completed, start and initialize the SQL node by following the steps given in [Starting the MySQL Server](#page-168-1).

If you choose to initialize the data directory manually using the mysqld --initialize command (see Section 2.9.1, "Initializing the Data Directory" for details), a root password is going to be generated and stored in the SQL node's error log; see [Starting the MySQL Server](#page-168-1) for how to find the password, and for a few things you need to know about it.

• Install the executables for management nodes:

```
$> sudo zypper install mysql-cluster-community-management-server
```

• Install the executables for data nodes:

```
$> sudo zypper install mysql-cluster-community-data-node
```

To install more NDB Cluster components, see [Installing Additional MySQL Products and Components](#page-169-0).

See Section 25.3.3, "Initial Configuration of NDB Cluster" on how to configure MySQL NDB Cluster and Section 25.3.4, "Initial Startup of NDB Cluster" on how to start it for the first time.

# <span id="page-172-1"></span>**Installing Additional MySQL NDB Cluster Products and Components**

You can use Zypper to install individual components and additional products of MySQL NDB Cluster from the MySQL SLES repository. To do that, assuming you already have the MySQL SLES repository on your system's repository list (if not, follow Step 1 and 2 of [Installing MySQL NDB Cluster Using the](#page-171-0) [SLES Repository](#page-171-0)), follow the same steps given in [Installing Additional MySQL NDB Cluster Products](#page-172-1) [and Components](#page-172-1).

![](_page_172_Picture_9.jpeg)

### **Note**

Known issue: Currently, not all components required for running the MySQL NDB Cluster test suite are installed automatically when you install the test suite package (mysql-cluster-community-test). Install the following packages with zypper install before you run the test suite:

- mysql-cluster-community-auto-installer
- mysql-cluster-community-management-server
- mysql-cluster-community-data-node
- mysql-cluster-community-memcached
- mysql-cluster-community-java
- mysql-cluster-community-ndbclient-devel

# <span id="page-172-0"></span>**2.5.4 Installing MySQL on Linux Using RPM Packages from Oracle**

The recommended way to install MySQL on RPM-based Linux distributions is by using the RPM packages provided by Oracle. There are two sources for obtaining them, for the Community Edition of MySQL:

- From the MySQL software repositories:
  - The MySQL Yum repository (see [Section 2.5.1, "Installing MySQL on Linux Using the MySQL Yum](#page-153-0) [Repository"](#page-153-0) for details).
  - The MySQL SLES repository (see [Section 2.5.3, "Using the MySQL SLES Repository"](#page-167-0) for details).
- From the [Download MySQL Community Server](https://dev.mysql.com/downloads/mysql/) page in the [MySQL Developer Zone](https://dev.mysql.com/).

![](_page_172_Picture_24.jpeg)

### **Note**

RPM distributions of MySQL are also provided by other vendors. Be aware that they may differ from those built by Oracle in features, capabilities, and conventions (including communication setup), and that the installation instructions in this manual do not necessarily apply to them. The vendor's instructions should be consulted instead.

# **MySQL RPM Packages**

**Table 2.10 RPM Packages for MySQL Community Edition**

| Package Name                    | Summary                                                                                                                                                                                                                         |
|---------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| mysql-community-client          | MySQL client applications and tools                                                                                                                                                                                             |
| mysql-community-client-plugins  | Shared plugins for MySQL client applications                                                                                                                                                                                    |
| mysql-community-common          | Common files for server and client libraries                                                                                                                                                                                    |
| mysql-community-devel           | Development header files and libraries for MySQL<br>database client applications                                                                                                                                                |
| mysql-community-embedded-compat | MySQL server as an embedded library with<br>compatibility for applications using version 18 of<br>the library                                                                                                                   |
| mysql-community-icu-data-files  | MySQL packaging of ICU data files needed by<br>MySQL regular expressions                                                                                                                                                        |
| mysql-community-libs            | Shared libraries for MySQL database client<br>applications                                                                                                                                                                      |
| mysql-community-libs-compat     | Shared compatibility libraries for previous MySQL<br>installations; only present if previous MySQL<br>versions are supported by the platform                                                                                    |
| mysql-community-server          | Database server and related tools                                                                                                                                                                                               |
| mysql-community-server-debug    | Debug server and plugin binaries                                                                                                                                                                                                |
| mysql-community-test            | Test suite for the MySQL server                                                                                                                                                                                                 |
| mysql-community                 | The source code RPM looks similar to mysql<br>community-8.4.8-1.el7.src.rpm, depending on<br>selected OS                                                                                                                        |
| Additional *debuginfo* RPMs     | There are several debuginfo packages: mysql<br>community-client-debuginfo, mysql-community<br>libs-debuginfo mysql-community-server-debug<br>debuginfo mysql-community-server-debuginfo,<br>and mysql-community-test-debuginfo. |

**Table 2.11 RPM Packages for the MySQL Enterprise Edition**

| Package Name                     | Summary                                                                                                       |
|----------------------------------|---------------------------------------------------------------------------------------------------------------|
| mysql-commercial-backup          | MySQL Enterprise Backup                                                                                       |
| mysql-commercial-client          | MySQL client applications and tools                                                                           |
| mysql-commercial-client-plugins  | Shared plugins for MySQL client applications                                                                  |
| mysql-commercial-common          | Common files for server and client libraries                                                                  |
| mysql-commercial-devel           | Development header files and libraries for MySQL<br>database client applications                              |
| mysql-commercial-embedded-compat | MySQL server as an embedded library with<br>compatibility for applications using version 18 of<br>the library |
| mysql-commercial-icu-data-files  | MySQL packaging of ICU data files needed by<br>MySQL regular expressions                                      |
| mysql-commercial-libs            | Shared libraries for MySQL database client<br>applications                                                    |
| mysql-commercial-libs-compat     | Shared compatibility libraries for previous MySQL<br>installations; only present if previous MySQL            |

| Package Name                | Summary                                                                                                                                                                                                                              |
|-----------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|                             | versions are supported by the platform. The<br>version of the libraries matches the version of the<br>libraries installed by default by the distribution you<br>are using.                                                           |
| mysql-commercial-server     | Database server and related tools                                                                                                                                                                                                    |
| mysql-commercial-test       | Test suite for the MySQL server                                                                                                                                                                                                      |
| Additional *debuginfo* RPMs | There are several debuginfo packages: mysql<br>commercial-client-debuginfo, mysql-commercial<br>libs-debuginfo mysql-commercial-server-debug<br>debuginfo mysql-commercial-server-debuginfo,<br>and mysql-commercial-test-debuginfo. |

The full names for the RPMs have the following syntax:

packagename-version-distribution-arch.rpm

The distribution and arch values indicate the Linux distribution and the processor type for which the package was built. See the table below for lists of the distribution identifiers:

**Table 2.12 MySQL Linux RPM Package Distribution Identifiers**

| Distribution Value                                                                | Intended Use                                                                                                                                                |
|-----------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------|
| el{version} where {version} is the major<br>Enterprise Linux version, such as el8 | EL6 (8.0), EL7, EL8, EL9, and EL10-based<br>platforms (for example, the corresponding<br>versions of Oracle Linux, Red Hat Enterprise<br>Linux, and CentOS) |
| fc{version} where {version} is the major<br>Fedora version, such as fc37          | Fedora 41 and 42                                                                                                                                            |
| sl5                                                                               | SUSE Linux Enterprise Server 15                                                                                                                             |

To see all files in an RPM package (for example, mysql-community-server), use the following command:

\$> **rpm -qpl mysql-community-server-version-distribution-arch.rpm**

The discussion in the rest of this section applies only to an installation process using the RPM packages directly downloaded from Oracle, instead of through a MySQL repository.

Dependency relationships exist among some of the packages. If you plan to install many of the packages, you may wish to download the RPM bundle tar file instead, which contains all the RPM packages listed above, so that you need not download them separately.

In most cases, you need to install the mysql-community-server, mysql-community-client, mysql-community-client-plugins, mysql-community-libs, mysql-community-icudata-files, mysql-community-common, and mysql-community-libs-compat packages to get a functional, standard MySQL installation. To perform such a standard, basic installation, go to the folder that contains all those packages (and, preferably, no other RPM packages with similar names), and issue the following command:

\$> **sudo yum install mysql-community-{server,client,client-plugins,icu-data-files,common,libs}-\***

Replace yum with zypper for SLES, and with dnf for Fedora.

While it is much preferable to use a high-level package management tool like yum to install the packages, users who prefer direct rpm commands can replace the yum install command with the rpm -Uvh command; however, using rpm -Uvh instead makes the installation process more prone to failure, due to potential dependency issues the installation process might run into.

To install only the client programs, you can skip mysql-community-server in your list of packages to install; issue the following command:

\$> **sudo yum install mysql-community-{client,client-plugins,common,libs}-\*** 

Replace yum with zypper for SLES, and with dnf for Fedora.

A standard installation of MySQL using the RPM packages result in files and resources created under the system directories, shown in the following table.

**Table 2.13 MySQL Installation Layout for Linux RPM Packages from the MySQL Developer Zone**

<span id="page-175-0"></span>

| Files or Resources                                                                    | Location                                                                                                          |
|---------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------|
| Client programs and scripts                                                           | /usr/bin                                                                                                          |
| mysqld server                                                                         | /usr/sbin                                                                                                         |
| Configuration file                                                                    | /etc/my.cnf                                                                                                       |
| Data directory                                                                        | /var/lib/mysql                                                                                                    |
| Error log file                                                                        | For RHEL, Oracle Linux, CentOS or Fedora<br>platforms: /var/log/mysqld.log<br>For SLES: /var/log/mysql/mysqld.log |
| Value of secure_file_priv                                                             | /var/lib/mysql-files                                                                                              |
| System V init script                                                                  | For RHEL, Oracle Linux, CentOS or Fedora<br>platforms: /etc/init.d/mysqld<br>For SLES: /etc/init.d/mysql          |
| Systemd service                                                                       | For RHEL, Oracle Linux, CentOS or Fedora<br>platforms: mysqld<br>For SLES: mysql                                  |
| Pid file                                                                              | /var/run/mysql/mysqld.pid                                                                                         |
| Socket                                                                                | /var/lib/mysql/mysql.sock                                                                                         |
| Keyring directory                                                                     | /var/lib/mysql-keyring                                                                                            |
| Unix manual pages                                                                     | /usr/share/man                                                                                                    |
| Include (header) files                                                                | /usr/include/mysql                                                                                                |
| Libraries                                                                             | /usr/lib/mysql                                                                                                    |
| Miscellaneous support files (for example, error<br>messages, and character set files) | /usr/share/mysql                                                                                                  |

The installation also creates a user named mysql and a group named mysql on the system.

![](_page_175_Picture_8.jpeg)

### **Notes**

• The mysql user is created using the -r and -s /bin/false options of the useradd command, so that it does not have login permissions to your server host (see [Creating the mysql User and Group](https://dev.mysql.com/doc/mysql-secure-deployment-guide/en/secure-deployment-install.md#secure-deployment-mysql-user) for details). To switch to the mysql user on your OS, use the --shell=/bin/bash option for the su command:

\$> su - mysql --shell=/bin/bash

• Installation of previous versions of MySQL using older packages might have created a configuration file named /usr/my.cnf. It is highly recommended that you examine the contents of the file and migrate the desired settings inside to the file /etc/my.cnf file, then remove /usr/my.cnf.

MySQL is NOT automatically started at the end of the installation process. For Red Hat Enterprise Linux, Oracle Linux, CentOS, and Fedora systems, use the following command to start MySQL:

```
$> systemctl start mysqld
```

For SLES systems, the command is the same, but the service name is different:

```
$> systemctl start mysql
```

If the operating system is systemd enabled, standard systemctl (or alternatively, service with the arguments reversed) commands such as stop, start, status, and restart should be used to manage the MySQL server service. The mysqld service is enabled by default, and it starts at system reboot. Notice that certain things might work differently on systemd platforms: for example, changing the location of the data directory might cause issues. See [Section 2.5.9, "Managing MySQL Server with](#page-192-1) [systemd"](#page-192-1) for additional information.

During an upgrade installation using RPM and DEB packages, if the MySQL server is running when the upgrade occurs then the MySQL server is stopped, the upgrade occurs, and the MySQL server is restarted. One exception: if the edition also changes during an upgrade (such as community to commercial, or vice-versa), then MySQL server is not restarted.

At the initial start up of the server, the following happens, given that the data directory of the server is empty:

- The server is initialized.
- An SSL certificate and key files are generated in the data directory.
- validate\_password is installed and enabled.
- A superuser account 'root'@'localhost' is created. A password for the superuser is set and stored in the error log file. To reveal it, use the following command for RHEL, Oracle Linux, CentOS, and Fedora systems:

```
$> sudo grep 'temporary password' /var/log/mysqld.log
```

Use the following command for SLES systems:

```
$> sudo grep 'temporary password' /var/log/mysql/mysqld.log
```

The next step is to log in with the generated, temporary password and set a custom password for the superuser account:

```
$> mysql -uroot -p
```

mysql> **ALTER USER 'root'@'localhost' IDENTIFIED BY 'MyNewPass4!';**

![](_page_176_Picture_18.jpeg)

### **Note**

validate\_password is installed by default. The default password policy implemented by validate\_password requires that passwords contain at least one uppercase letter, one lowercase letter, one digit, and one special character, and that the total password length is at least 8 characters.

If something goes wrong during installation, you might find debug information in the error log file /var/ log/mysqld.log.

For some Linux distributions, it might be necessary to increase the limit on number of file descriptors available to mysqld. See Section B.3.2.16, "File Not Found and Similar Errors"

**Installing Client Libraries from Multiple MySQL Versions.** It is possible to install multiple client library versions, such as for the case that you want to maintain compatibility with older applications

linked against previous libraries. To install an older client library, use the --oldpackage option with rpm. For example, to install mysql-community-libs-5.5 on an EL6 system that has libmysqlclient.21 from MySQL 8.0, use a command like this:

\$> **rpm --oldpackage -ivh mysql-community-libs-5.5.50-2.el6.x86\_64.rpm**

**Debug Package.** A special variant of MySQL Server compiled with the debug package has been included in the server RPM packages. It performs debugging and memory allocation checks and produces a trace file when the server is running. To use that debug version, start MySQL with / usr/sbin/mysqld-debug, instead of starting it as a service or with /usr/sbin/mysqld. See Section 7.9.4, "The DBUG Package" for the debug options you can use.

![](_page_177_Picture_4.jpeg)

### **Note**

The default plugin directory is /usr/lib64/mysql/plugin/debug and is configurable with plugin\_dir.

**Rebuilding RPMs from source SRPMs.** Source code SRPM packages for MySQL are available for download. They can be used as-is to rebuild the MySQL RPMs with the standard rpmbuild tool chain.

# <span id="page-177-0"></span>**2.5.5 Installing MySQL on Linux Using Debian Packages from Oracle**

Oracle provides Debian packages for installing MySQL on Debian or Debian-like Linux systems. The packages are available through two different channels:

- The [MySQL APT Repository](https://dev.mysql.com/downloads/repo/apt/). This is the preferred method for installing MySQL on Debian-like systems, as it provides a simple and convenient way to install and update MySQL products. For details, see [Section 2.5.2, "Installing MySQL on Linux Using the MySQL APT Repository"](#page-158-0).
- The [MySQL Developer Zone's Download Area](https://dev.mysql.com/downloads/). For details, see [Section 2.1.3, "How to Get MySQL".](#page-87-0) The following are some information on the Debian packages available there and the instructions for installing them:
  - Various Debian packages are provided in the MySQL Developer Zone for installing different components of MySQL on the current Debian and Ubuntu platforms. The preferred method is to use the tarball bundle, which contains the packages needed for a basic setup of MySQL. The tarball bundles have names in the format of mysql-server\_MVER-DVER\_CPU.debbundle.tar. MVER is the MySQL version and DVER is the Linux distribution version. The CPU value indicates the processor type or family for which the package is built, as shown in the following table:

**Table 2.14 MySQL Debian and Ubuntu Installation Packages CPU Identifiers**

| CPU Value | Intended Processor Type or Family   |
|-----------|-------------------------------------|
| i386      | Pentium processor or better, 32 bit |
| amd64     | 64-bit x86 processor                |

• After downloading the tarball, unpack it with the following command:

\$> **tar -xvf mysql-server\_MVER-DVER\_CPU.deb-bundle.tar**

• You may need to install the libaio library if it is not already present on your system:

\$> **sudo apt-get install libaio1**

• Preconfigure the MySQL server package with the following command:

\$> **sudo dpkg-preconfigure mysql-community-server\_\*.deb**

You are asked to provide a password for the root user for your MySQL installation. You might also be asked other questions regarding the installation.

![](_page_178_Picture_1.jpeg)

### **Important**

Make sure you remember the root password you set. Users who want to set a password later can leave the **password** field blank in the dialogue box and just press **OK**; in that case, root access to the server is authenticated using the MySQL Socket Peer-Credential Authentication Plugin for connections using a Unix socket file. You can set the root password later using mysql\_secure\_installation.

• For a basic installation of the MySQL server, install the database common files package, the client package, the client metapackage, the server package, and the server metapackage (in that order); you can do that with a single command:

\$> **sudo dpkg -i mysql-{common,community-client-plugins,community-client-core,community-client,client,community-server-core,community-server,server}\_\*.deb**

There are also packages with server-core and client-core in the package names. These contain binaries only and are installed automatically by the standard packages. Installing them by themselves does not result in a functioning MySQL setup.

If you are being warned of unmet dependencies by dpkg (such as libmecab2), you can fix them using apt-get:

**sudo apt-get -f install**

Here are where the files are installed on the system:

- All configuration files (like my.cnf) are under /etc/mysql
- All binaries, libraries, headers, etc., are under /usr/bin and /usr/sbin
- The data directory is under /var/lib/mysql

![](_page_178_Picture_13.jpeg)

# **Note**

Debian distributions of MySQL are also provided by other vendors. Be aware that they may differ from those built by Oracle in features, capabilities, and conventions (including communication setup), and that the instructions in this manual do not necessarily apply to installing them. The vendor's instructions should be consulted instead.

# <span id="page-178-0"></span>**2.5.6 Deploying MySQL on Linux with Docker Containers**

This section explains how to deploy MySQL Server using Docker containers.

While the docker client is used in the following instructions for demonstration purposes, in general, the MySQL container images provided by Oracle work with any container tools that are compliant with the [OCI 1.0 specification](https://opencontainers.org/posts/announcements/2021-05-04-oci-dist-spec-v1/).

![](_page_178_Picture_19.jpeg)

### **Warning**

Before deploying MySQL with Docker containers, make sure you understand the security risks of running containers and mitigate them properly.

# <span id="page-178-1"></span>**2.5.6.1 Basic Steps for MySQL Server Deployment with Docker**

![](_page_178_Picture_23.jpeg)

### **Warning**

The MySQL Docker images maintained by the MySQL team are built specifically for Linux platforms. Other platforms are not supported, and users using these MySQL Docker images on them are doing so at their own risk. See [the discussion here](#page-189-0) for some known limitations for running these containers on non-Linux operating systems.

- [Downloading a MySQL Server Docker Image](#page-179-0)
- [Starting a MySQL Server Instance](#page-180-0)
- [Connecting to MySQL Server from within the Container](#page-181-0)
- [Container Shell Access](#page-181-1)
- [Stopping and Deleting a MySQL Container](#page-181-2)
- [Upgrading a MySQL Server Container](#page-182-0)
- [More Topics on Deploying MySQL Server with Docker](#page-183-0)

### <span id="page-179-0"></span>**Downloading a MySQL Server Docker Image**

![](_page_179_Picture_10.jpeg)

### **Important**

For users of MySQL Enterprise Edition: A subscription is required to use the Docker images for MySQL Enterprise Edition. Subscriptions work by a Bring Your Own License model; see [How to Buy MySQL Products and Services](https://www.mysql.com/buy-mysql/) for details.

Downloading the server image in a separate step is not strictly necessary; however, performing this step before you create your Docker container ensures your local image is up to date. To download the MySQL Community Edition image from the [Oracle Container Registry \(OCR\),](https://container-registry.oracle.com/) run this command:

```
docker pull container-registry.oracle.com/mysql/community-server:tag
```

The tag is the label for the image version you want to pull (for example, 8.4, or 9.6, or latest). If **:tag** is omitted, the latest label is used, and the image for the latest GA release (which is the latest innovation release) of MySQL Community Server is downloaded.

To download the MySQL Enterprise Edition image from the OCR, you need to first accept the license agreement on the OCR and log in to the container repository with your Docker client. Follow these steps:

- Visit the OCR at<https://container-registry.oracle.com/> and choose **MySQL**.
- Under the list of MySQL repositories, choose enterprise-server.
- If you have not signed in to the OCR yet, click the **Sign in** button on the right of the page, and then enter your Oracle account credentials when prompted to.
- Follow the instructions on the right of the page to accept the license agreement.
- Log in to the OCR with your container client using, for example, the docker login command:

```
# docker login container-registry.oracle.com 
Username: Oracle-Account-ID
Password: password
Login successful.
```

Download the Docker image for MySQL Enterprise Edition from the OCR with this command:

```
docker pull container-registry.oracle.com/mysql/enterprise-server:tag
```

To download the MySQL Enterprise Edition image from [My Oracle Support](https://support.oracle.com/) website, go onto the website, sign in to your Oracle account, and perform these steps once you are on the landing page:

• Select the **Patches and Updates** tab.

- Go to the **Patch Search** region and, on the **Search** tab, switch to the **Product or Family (Advanced)** subtab.
- Enter "MySQL Server" for the **Product** field, and the desired version number in the **Release** field.
- Use the dropdowns for additional filters to select **Description**—**contains**, and enter "Docker" in the text field.

The following figure shows the search settings for the MySQL Enterprise Edition image for MySQL Server 8.0:

![](_page_180_Picture_5.jpeg)

- Click the **Search** button and, from the result list, select the version you want, and click the **Download** button.
- In the **File Download** dialogue box that appears, click and download the .zip file for the Docker image.

Unzip the downloaded .zip archive to obtain the tarball inside (mysql-enterpriseserver-version.tar), and then load the image by running this command:

```
docker load -i mysql-enterprise-server-version.tar
```

You can list downloaded Docker images with this command:

```
$> docker images
REPOSITORY TAG IMAGE ID CREATED SIZE
container-registry.oracle.com/mysql/community-server latest 1d9c2219ff69 2 months ago 496MB
```

### <span id="page-180-0"></span>**Starting a MySQL Server Instance**

To start a new Docker container for a MySQL Server, use the following command:

```
docker run --name=container_name --restart on-failure -d image_name:tag
```

image\_name is the name of the image to be used to start the container; see [Downloading a MySQL](#page-179-0) [Server Docker Image](#page-179-0) for more information.

The --name option, for supplying a custom name for your server container, is optional; if no container name is supplied, a random one is generated.

The --restart option is for configuring the [restart policy](https://docs.docker.com/config/containers/start-containers-automatically/) for your container; it should be set to the value on-failure, to enable support for server restart within a client session (which happens, for example, when the RESTART statement is executed by a client or during the configuration of an InnoDB Cluster instance). With the support for restart enabled, issuing a restart within a client session causes the server and the container to stop and then restart.

For example, to start a new Docker container for the MySQL Community Server, use this command:

```
docker run --name=mysql1 --restart on-failure -d container-registry.oracle.com/mysql/community-server:latest
```

To start a new Docker container for the MySQL Enterprise Server with a Docker image downloaded from the OCR, use this command:

```
docker run --name=mysql1 --restart on-failure -d container-registry.oracle.com/mysql/enterprise-server:latest
```

To start a new Docker container for the MySQL Enterprise Server with a Docker image downloaded from My Oracle Support, use this command:

```
docker run --name=mysql1 --restart on-failure -d mysql/enterprise-server:latest
```

If the Docker image of the specified name and tag has not been downloaded by an earlier docker pull or docker run command, the image is now downloaded. Initialization for the container begins, and the container appears in the list of running containers when you run the docker ps command. For example:

```
$> docker ps
CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES
4cd4129b3211 container-registry.oracle.com/mysql/community-server:latest "/entrypoint.sh mysq…" 8 seconds ago Up 7 seconds (health: starting) 3306/tcp, 33060-33061/tcp mysql1
```

The container initialization might take some time. When the server is ready for use, the STATUS of the container in the output of the docker ps command changes from (health: starting) to (healthy).

The -d option used in the docker run command above makes the container run in the background. Use this command to monitor the output from the container:

```
docker logs mysql1
```

Once initialization is finished, the command's output is going to contain the random password generated for the root user; check the password with, for example, this command:

```
$> docker logs mysql1 2>&1 | grep GENERATED
GENERATED ROOT PASSWORD: Axegh3kAJyDLaRuBemecis&EShOs
```

### <span id="page-181-0"></span>**Connecting to MySQL Server from within the Container**

Once the server is ready, you can run the mysql client within the MySQL Server container you just started, and connect it to the MySQL Server. Use the docker exec -it command to start a mysql client inside the Docker container you have started, like the following:

```
docker exec -it mysql1 mysql -uroot -p
```

When asked, enter the generated root password (see the last step in [Starting a MySQL Server](#page-180-0) [Instance](#page-180-0) above on how to find the password). Because the [MYSQL\\_ONETIME\\_PASSWORD](#page-188-0) option is true by default, after you have connected a mysql client to the server, you must reset the server root password by issuing this statement:

```
mysql> ALTER USER 'root'@'localhost' IDENTIFIED BY 'password';
```

Substitute password with the password of your choice. Once the password is reset, the server is ready for use.

### <span id="page-181-1"></span>**Container Shell Access**

To have shell access to your MySQL Server container, use the docker exec -it command to start a bash shell inside the container:

```
$> docker exec -it mysql1 bash
bash-4.2#
```

You can then run Linux commands inside the container. For example, to view contents in the server's data directory inside the container, use this command:

```
bash-4.2# ls /var/lib/mysql
auto.cnf ca.pem client-key.pem ib_logfile0 ibdata1 mysql mysql.sock.lock private_key.pem server-cert.pem sys
ca-key.pem client-cert.pem ib_buffer_pool ib_logfile1 ibtmp1 mysql.sock performance_schema public_key.pem server-key.pem
```

# <span id="page-181-2"></span>**Stopping and Deleting a MySQL Container**

To stop the MySQL Server container we have created, use this command:

```
docker stop mysql1
```

docker stop sends a SIGTERM signal to the mysqld process, so that the server is shut down gracefully.

Also notice that when the main process of a container (mysqld in the case of a MySQL Server container) is stopped, the Docker container stops automatically.

To start the MySQL Server container again:

```
docker start mysql1
```

To stop and start again the MySQL Server container with a single command:

```
docker restart mysql1
```

To delete the MySQL container, stop it first, and then use the docker rm command:

```
docker stop mysql1
docker rm mysql1
```

If you want the [Docker volume for the server's data directory](#page-184-0) to be deleted at the same time, add the v option to the docker rm command.

### <span id="page-182-0"></span>**Upgrading a MySQL Server Container**

![](_page_182_Picture_12.jpeg)

### **Important**

- Before performing any upgrade to MySQL, follow carefully the instructions in Chapter 3, Upgrading MySQL. Among other instructions discussed there, it is especially important to back up your database before the upgrade.
- The instructions in this section require that the server's data and configuration have been persisted on the host. See [Persisting Data and Configuration](#page-184-0) [Changes](#page-184-0) for details.

Follow these steps to upgrade a Docker installation of MySQL 8.4 to 9.6:

• Stop the MySQL 8.4 server (container name is mysql84 in this example):

```
docker stop mysql84
```

- Download the MySQL 9.6 Server Docker image. See instructions in [Downloading a MySQL Server](#page-179-0) [Docker Image](#page-179-0). Make sure you use the right tag for MySQL 9.6.
- Start a new MySQL 9.6 Docker container (named mysql96 in this example) with the old server data and configuration (with proper modifications if needed—see Chapter 3, Upgrading MySQL) that have been persisted on the host (by [bind-mounting](https://docs.docker.com/engine/reference/commandline/service_create/#add-bind-mounts-or-volumes) in this example). For the MySQL Community Server, run this command:

```
docker run --name=mysql84 \
 --mount type=bind,src=/path-on-host-machine/my.cnf,dst=/etc/my.cnf \
 --mount type=bind,src=/path-on-host-machine/datadir,dst=/var/lib/mysql \
 -d container-registry.oracle.com/mysql/community-server:9.6
```

If needed, adjust container-registry.oracle.com/mysql/community-server to the correct image name—for example, replace it with container-registry.oracle.com/mysql/ enterprise-server for MySQL Enterprise Edition images downloaded from the OCR, or mysql/ enterprise-server for MySQL Enterprise Edition images downloaded from My Oracle Support.

• Wait for the server to finish startup. You can check the status of the server using the docker ps command (see [Starting a MySQL Server Instance](#page-180-0) for how to do that).

Follow the same steps for upgrading within the 9.6 series (that is, from release 9.6.x to 9.6.y): stop the original container, and start a new one with a newer image on the old server data and configuration. If you used the 9.6 or the latest tag when starting your original container and there is now a new MySQL 9.6 release you want to upgrade to it, you must first pull the image for the new release with the command:

```
docker pull container-registry.oracle.com/mysql/community-server:9.6
```

You can then upgrade by starting a new container with the same tag on the old data and configuration (adjust the image name if you are using the MySQL Enterprise Edition; see [Downloading a MySQL](#page-179-0) [Server Docker Image](#page-179-0)):

```
docker run --name=mysql84new \
 --mount type=bind,src=/path-on-host-machine/my.cnf,dst=/etc/my.cnf \
 --mount type=bind,src=/path-on-host-machine/datadir,dst=/var/lib/mysql \
 -d container-registry.oracle.com/mysql/community-server:9.6
```

### <span id="page-183-0"></span>**More Topics on Deploying MySQL Server with Docker**

For more topics on deploying MySQL Server with Docker like server configuration, persisting data and configuration, server error log, and container environment variables, see [Section 2.5.6.2, "More Topics](#page-183-1) [on Deploying MySQL Server with Docker"](#page-183-1).

# <span id="page-183-1"></span>**2.5.6.2 More Topics on Deploying MySQL Server with Docker**

![](_page_183_Picture_8.jpeg)

### **Note**

Most of the following sample commands have containerregistry.oracle.com/mysql/community-server as the Docker image being used (like with the docker pull and docker run commands); change that if your image is from another repository—for example, replace it with container-registry.oracle.com/mysql/enterprise-server for MySQL Enterprise Edition images downloaded from the Oracle Container Registry (OCR), or mysql/enterprise-server for MySQL Enterprise Edition images downloaded from [My Oracle Support](https://support.oracle.com/).

- [The Optimized MySQL Installation for Docker](#page-183-2)
- [Configuring the MySQL Server](#page-184-1)
- [Persisting Data and Configuration Changes](#page-184-0)
- [Running Additional Initialization Scripts](#page-185-0)
- [Connect to MySQL from an Application in Another Docker Container](#page-185-1)
- [Server Error Log](#page-185-2)
- [Using MySQL Enterprise Backup with Docker](#page-186-0)
- [Using mysqldump with Docker](#page-187-0)
- [Known Issues](#page-188-1)
- [Docker Environment Variables](#page-188-2)

### <span id="page-183-2"></span>**The Optimized MySQL Installation for Docker**

Docker images for MySQL are optimized for code size, which means they only include crucial components that are expected to be relevant for the majority of users who run MySQL instances in Docker containers. A MySQL Docker installation is different from a common, non-Docker installation in the following aspects:

- Only a limited number of binaries are included.
- All binaries are stripped; they contain no debug information.

![](_page_184_Picture_3.jpeg)

### **Warning**

Any software updates or installations users perform to the Docker container (including those for MySQL components) may conflict with the optimized MySQL installation created by the Docker image. Oracle does not provide support for MySQL products running in such an altered container, or a container created from an altered Docker image.

# <span id="page-184-1"></span>**Configuring the MySQL Server**

When you start the MySQL Docker container, you can pass configuration options to the server through the docker run command. For example:

```
docker run --name mysql1 -d container-registry.oracle.com/mysql/community-server:tag --character-set-server=utf8mb4 --collation-server=utf8mb4_col
```

The command starts the MySQL Server with utf8mb4 as the default character set and utf8mb4\_col as the default collation for databases.

Another way to configure the MySQL Server is to prepare a configuration file and mount it at the location of the server configuration file inside the container. See [Persisting Data and Configuration](#page-184-0) [Changes](#page-184-0) for details.

### <span id="page-184-0"></span>**Persisting Data and Configuration Changes**

Docker containers are in principle ephemeral, and any data or configuration are expected to be lost if the container is deleted or corrupted (see discussions [here\)](https://docs.docker.com/engine/userguide/eng-image/dockerfile_best-practices/). [Docker volumes](https://docs.docker.com/engine/admin/volumes/volumes/) provides a mechanism to persist data created inside a Docker container. At its initialization, the MySQL Server container creates a Docker volume for the server data directory. The JSON output from the docker inspect command on the container includes a Mount key, whose value provides information on the data directory volume:

```
$> docker inspect mysql1
...
 "Mounts": [
 {
 "Type": "volume",
 "Name": "4f2d463cfc4bdd4baebcb098c97d7da3337195ed2c6572bc0b89f7e845d27652",
 "Source": "/var/lib/docker/volumes/4f2d463cfc4bdd4baebcb098c97d7da3337195ed2c6572bc0b89f7e845d27652/_data",
 "Destination": "/var/lib/mysql",
 "Driver": "local",
 "Mode": "",
 "RW": true,
 "Propagation": ""
 }
 ],
...
```

The output shows that the source directory /var/lib/docker/ volumes/4f2d463cfc4bdd4baebcb098c97d7da3337195ed2c6572bc0b89f7e845d27652/ \_data, in which data is persisted on the host, has been mounted at /var/lib/mysql, the server data directory inside the container.

Another way to preserve data is to [bind-mount](https://docs.docker.com/engine/reference/commandline/service_create/#add-bind-mounts-volumes-or-memory-filesystems) a host directory using the --mount option when creating the container. The same technique can be used to persist the configuration of the server. The following command creates a MySQL Server container and bind-mounts both the data directory and the server configuration file:

```
docker run --name=mysql1 \
--mount type=bind,src=/path-on-host-machine/my.cnf,dst=/etc/my.cnf \
--mount type=bind,src=/path-on-host-machine/datadir,dst=/var/lib/mysql \
-d container-registry.oracle.com/mysql/community-server:tag
```

The command mounts path-on-host-machine/my.cnf at /etc/my.cnf (the server configuration file inside the container), and path-on-host-machine/datadir at /var/lib/mysql (the data directory inside the container). The following conditions must be met for the bind-mounting to work:

• The configuration file path-on-host-machine/my.cnf must already exist, and it must contain the specification for starting the server by the user mysql:

```
[mysqld]
user=mysql
```

You can also include other server configuration options in the file.

• The data directory path-on-host-machine/datadir must already exist. For server initialization to happen, the directory must be empty. You can also mount a directory prepopulated with data and start the server with it; however, you must make sure you start the Docker container with the same configuration as the server that created the data, and any host files or directories required are mounted when starting the container.

# <span id="page-185-0"></span>**Running Additional Initialization Scripts**

If there are any .sh or .sql scripts you want to run on the database immediately after it has been created, you can put them into a host directory and then mount the directory at /dockerentrypoint-initdb.d/ inside the container. For example:

```
docker run --name=mysql1 \
--mount type=bind,src=/path-on-host-machine/scripts/,dst=/docker-entrypoint-initdb.d/ \
-d container-registry.oracle.com/mysql/community-server:tag
```

### <span id="page-185-1"></span>**Connect to MySQL from an Application in Another Docker Container**

By setting up a Docker network, you can allow multiple Docker containers to communicate with each other, so that a client application in another Docker container can access the MySQL Server in the server container. First, create a Docker network:

```
docker network create my-custom-net
```

Then, when you are creating and starting the server and the client containers, use the --network option to put them on network you created. For example:

```
docker run --name=mysql1 --network=my-custom-net -d container-registry.oracle.com/mysql/community-server
docker run --name=myapp1 --network=my-custom-net -d myapp
```

The myapp1 container can then connect to the mysql1 container with the mysql1 hostname and vice versa, as Docker automatically sets up a DNS for the given container names. In the following example, we run the mysql client from inside the myapp1 container to connect to host mysql1 in its own container:

```
docker exec -it myapp1 mysql --host=mysql1 --user=myuser --password
```

For other networking techniques for containers, see the [Docker container networking](https://docs.docker.com/engine/userguide/networking/) section in the Docker Documentation.

## <span id="page-185-2"></span>**Server Error Log**

When the MySQL Server is first started with your server container, a server error log is NOT generated if either of the following conditions is true:

- A server configuration file from the host has been mounted, but the file does not contain the system variable log\_error (see [Persisting Data and Configuration Changes](#page-184-0) on bind-mounting a server configuration file).
- A server configuration file from the host has not been mounted, but the Docker environment variable [MYSQL\\_LOG\\_CONSOLE](#page-189-1) is true (which is the variable's default state for MySQL 8.4 server

containers). The MySQL Server's error log is then redirected to stderr, so that the error log goes into the Docker container's log and is viewable using the docker logs mysqld-container command.

To make MySQL Server generate an error log when either of the two conditions is true, use the - log-error option to [configure the server](#page-184-1) to generate the error log at a specific location inside the container. To persist the error log, mount a host file at the location of the error log inside the container as explained in [Persisting Data and Configuration Changes.](#page-184-0) However, you must make sure your MySQL Server inside its container has write access to the mounted host file.

### <span id="page-186-0"></span>**Using MySQL Enterprise Backup with Docker**

MySQL Enterprise Backup is a commercially-licensed backup utility for MySQL Server, available with [MySQL Enterprise Edition](https://www.mysql.com/products/enterprise/). MySQL Enterprise Backup is included in the Docker installation of MySQL Enterprise Edition.

In the following example, we assume that you already have a MySQL Server running in a Docker container (see [Section 2.5.6.1, "Basic Steps for MySQL Server Deployment with Docker"](#page-178-1) on how to start a MySQL Server instance with Docker). For MySQL Enterprise Backup to back up the MySQL Server, it must have access to the server's data directory. This can be achieved by, for example, [bind](#page-184-0)[mounting a host directory on the data directory of the MySQL Server](#page-184-0) when you start the server:

```
docker run --name=mysqlserver \
--mount type=bind,src=/path-on-host-machine/datadir/,dst=/var/lib/mysql \
-d mysql/enterprise-server:8.4
```

With this command, the MySQL Server is started with a Docker image of the MySQL Enterprise Edition, and the host directory /path-on-host-machine/datadir/ has been mounted onto the server's data directory (/var/lib/mysql) inside the server container. We also assume that, after the server has been started, the required privileges have also been set up for MySQL Enterprise Backup to access the server (see [Grant MySQL Privileges to Backup Administrator,](https://dev.mysql.com/doc/mysql-enterprise-backup/8.4/en/mysqlbackup.privileges.md) for details). Use the following steps to back up and restore a MySQL Server instance.

To back up a MySQL Server instance running in a Docker container using MySQL Enterprise Backup with Docker, follow the steps listed here:

1. On the same host where the MySQL Server container is running, start another container with an image of MySQL Enterprise Edition to perform a back up with the MySQL Enterprise Backup command [backup-to-image](https://dev.mysql.com/doc/mysql-enterprise-backup/8.4/en/backup-commands-backup.md#option_meb_backup-to-image). Provide access to the server's data directory using the bind mount we created in the last step. Also, mount a host directory (/path-on-host-machine/backups/ in this example) onto the storage folder for backups in the container (/data/backups in the example) to persist the backups we are creating. Here is a sample command for this step, in which MySQL Enterprise Backup is started with a Docker image downloaded from [My Oracle Support](https://support.oracle.com/):

```
$> docker run \
--mount type=bind,src=/path-on-host-machine/datadir/,dst=/var/lib/mysql \
--mount type=bind,src=/path-on-host-machine/backups/,dst=/data/backups \
--rm mysql/enterprise-server:8.4 \
mysqlbackup -umysqlbackup -ppassword --backup-dir=/tmp/backup-tmp --with-timestamp \
--backup-image=/data/backups/db.mbi backup-to-image
```

It is important to check the end of the output by mysqlbackup to make sure the backup has been completed successfully.

2. The container exits once the backup job is finished and, with the --rm option used to start it, it is removed after it exits. An image backup has been created, and can be found in the host directory mounted in the last step for storing backups, as shown here:

```
$> ls /tmp/backups
db.mbi
```

To restore a MySQL Server instance in a Docker container using MySQL Enterprise Backup with Docker, follow the steps listed here:

1. Stop the MySQL Server container, which also stops the MySQL Server running inside:

```
docker stop mysqlserver
```

2. On the host, delete all contents in the bind mount for the MySQL Server data directory:

```
rm -rf /path-on-host-machine/datadir/*
```

3. Start a container with an image of MySQL Enterprise Edition to perform the restore with the MySQL Enterprise Backup command [copy-back-and-apply-log](https://dev.mysql.com/doc/mysql-enterprise-backup/8.4/en/backup-commands-restore.md#option_meb_copy-back-and-apply-log). Bind-mount the server's data directory and the storage folder for the backups, like what we did when we backed up the server:

```
$> docker run \
--mount type=bind,src=/path-on-host-machine/datadir/,dst=/var/lib/mysql \
--mount type=bind,src=/path-on-host-machine/backups/,dst=/data/backups \
--rm mysql/enterprise-server:8.4 \
mysqlbackup --backup-dir=/tmp/backup-tmp --with-timestamp \
--datadir=/var/lib/mysql --backup-image=/data/backups/db.mbi copy-back-and-apply-log
mysqlbackup completed OK! with 3 warnings
```

The container exits with the message " mysqlbackup completed OK!" once the backup job is finished and, with the --rm option used when starting it, it is removed after it exits.

4. Restart the server container, which also restarts the restored server, using the following command:

```
docker restart mysqlserver
```

Or, start a new MySQL Server on the restored data directory, as shown here:

```
docker run --name=mysqlserver2 \
--mount type=bind,src=/path-on-host-machine/datadir/,dst=/var/lib/mysql \
-d mysql/enterprise-server:8.4
```

Log on to the server to check that the server is running with the restored data.

## <span id="page-187-0"></span>**Using mysqldump with Docker**

Besides [using MySQL Enterprise Backup to back up a MySQL Server running in a Docker container,](#page-186-0) you can perform a logical backup of your server by using the mysqldump utility, run inside a Docker container.

The following instructions assume that you already have a MySQL Server running in a Docker container and, when the container was first started, a host directory /path-on-host-machine/ datadir/ has been mounted onto the server's data directory /var/lib/mysql (see [bind-mounting](#page-184-0) [a host directory on the data directory of the MySQL Server](#page-184-0) for details), which contains the Unix socket file by which mysqldump and mysql can connect to the server. We also assume that, after the server has been started, a user with the proper privileges (admin in this example) has been created, with which mysqldump can access the server. Use the following steps to back up and restore MySQL Server data:

Backing up MySQL Server data using mysqldump with Docker:

1. On the same host where the MySQL Server container is running, start another container with an image of MySQL Server to perform a backup with the mysqldump utility (see documentation of the utility for its functionality, options, and limitations). Provide access to the server's data directory by bind mounting /path-on-host-machine/datadir/. Also, mount a host directory (/pathon-host-machine/backups/ in this example) onto a storage folder for backups inside the container (/data/backups is used in this example) to persist the backups you are creating. Here is a sample command for backing up all databases on the server using this setup:

```
$> docker run --entrypoint "/bin/sh" \ 
--mount type=bind,src=/path-on-host-machine/datadir/,dst=/var/lib/mysql \
--mount type=bind,src=/path-on-host-machine/backups/,dst=/data/backups \
```

```
--rm container-registry.oracle.com/mysql/community-server:8.4 \
-c "mysqldump -uadmin --password='password' --all-databases > /data/backups/all-databases.sql"
```

In the command, the --entrypoint option is used so that the system shell is invoked after the container is started, and the -c option is used to specify the mysqldump command to be run in the shell, whose output is redirected to the file all-databases.sql in the backup directory.

2. The container exits once the backup job is finished and, with the --rm option used to start it, it is removed after it exits. A logical backup been created, and can be found in the host directory mounted for storing the backup, as shown here:

```
$> ls /path-on-host-machine/backups/
all-databases.sql
```

Restoring MySQL Server data using mysqldump with Docker:

- 1. Make sure you have a MySQL Server running in a container, onto which you want your backed-up data to be restored.
- 2. Start a container with an image of MySQL Server to perform the restore with a mysql client. Bindmount the server's data directory, as well as the storage folder that contains your backup:

```
$> docker run \
--mount type=bind,src=/path-on-host-machine/datadir/,dst=/var/lib/mysql \
--mount type=bind,src=/path-on-host-machine/backups/,dst=/data/backups \
--rm container-registry.oracle.com/mysql/community-server:8.4 \
mysql -uadmin --password='password' -e "source /data/backups/all-databases.sql"
```

The container exits once the backup job is finished and, with the --rm option used when starting it, it is removed after it exits.

3. Log on to the server to check that the restored data is now on the server.

### <span id="page-188-1"></span>**Known Issues**

• When using the server system variable audit\_log\_file to configure the audit log file name, use the loose option modifier with it; otherwise, Docker cannot start the server.

### <span id="page-188-2"></span>**Docker Environment Variables**

When you create a MySQL Server container, you can configure the MySQL instance by using the - env option (short form -e) and specifying one or more environment variables. No server initialization is performed if the mounted data directory is not empty, in which case setting any of these variables has no effect (see [Persisting Data and Configuration Changes\)](#page-184-0), and no existing contents of the directory, including server settings, are modified during container startup.

Environment variables which can be used to configure a MySQL instance are listed here:

- The boolean variables including [MYSQL\\_RANDOM\\_ROOT\\_PASSWORD](#page-188-3), [MYSQL\\_ONETIME\\_PASSWORD](#page-188-0), [MYSQL\\_ALLOW\\_EMPTY\\_PASSWORD](#page-189-2), and [MYSQL\\_LOG\\_CONSOLE](#page-189-1) are made true by setting them with any strings of nonzero lengths. Therefore, setting them to, for example, "0", "false", or "no" does not make them false, but actually makes them true. This is a known issue.
- <span id="page-188-3"></span>• [MYSQL\\_RANDOM\\_ROOT\\_PASSWORD](#page-188-3): When this variable is true (which is its default state, unless [MYSQL\\_ROOT\\_PASSWORD](#page-189-3) is set or [MYSQL\\_ALLOW\\_EMPTY\\_PASSWORD](#page-189-2) is set to true), a random password for the server's root user is generated when the Docker container is started. The password is printed to stdout of the container and can be found by looking at the container's log (see [Starting](#page-180-0) [a MySQL Server Instance](#page-180-0)).
- <span id="page-188-0"></span>• [MYSQL\\_ONETIME\\_PASSWORD](#page-188-0): When the variable is true (which is its default state, unless [MYSQL\\_ROOT\\_PASSWORD](#page-189-3) is set or [MYSQL\\_ALLOW\\_EMPTY\\_PASSWORD](#page-189-2) is set to true), the root user's password is set as expired and must be changed before MySQL can be used normally.

- <span id="page-189-4"></span>• [MYSQL\\_DATABASE](#page-189-4): This variable allows you to specify the name of a database to be created on image startup. If a user name and a password are supplied with [MYSQL\\_USER](#page-189-5) and [MYSQL\\_PASSWORD](#page-189-5), the user is created and granted superuser access to this database (corresponding to GRANT ALL). The specified database is created by a CREATE DATABASE IF NOT EXIST statement, so that the variable has no effect if the database already exists.
- <span id="page-189-5"></span>• [MYSQL\\_USER](#page-189-5), [MYSQL\\_PASSWORD](#page-189-5): These variables are used in conjunction to create a user and set that user's password, and the user is granted superuser permissions for the database specified by the [MYSQL\\_DATABASE](#page-189-4) variable. Both [MYSQL\\_USER](#page-189-5) and [MYSQL\\_PASSWORD](#page-189-5) are required for a user to be created—if any of the two variables is not set, the other is ignored. If both variables are set but [MYSQL\\_DATABASE](#page-189-4) is not, the user is created without any privileges.

![](_page_189_Picture_3.jpeg)

### **Note**

There is no need to use this mechanism to create the root superuser, which is created by default with the password set by either one of the mechanisms discussed in the descriptions for [MYSQL\\_ROOT\\_PASSWORD](#page-189-3) and [MYSQL\\_RANDOM\\_ROOT\\_PASSWORD](#page-188-3), unless [MYSQL\\_ALLOW\\_EMPTY\\_PASSWORD](#page-189-2) is true.

- <span id="page-189-6"></span>• [MYSQL\\_ROOT\\_HOST](#page-189-6): By default, MySQL creates the 'root'@'localhost' account. This account can only be connected to from inside the container as described in [Connecting to MySQL Server](#page-181-0) [from within the Container](#page-181-0). To allow root connections from other hosts, set this environment variable. For example, the value 172.17.0.1, which is the default Docker gateway IP, allows connections from the host machine that runs the container. The option accepts only one entry, but wildcards are allowed (for example, MYSQL\_ROOT\_HOST=172.\*.\*.\* or MYSQL\_ROOT\_HOST=%).
- <span id="page-189-1"></span>• [MYSQL\\_LOG\\_CONSOLE](#page-189-1): When the variable is true (which is its default state for MySQL 8.4 server containers), the MySQL Server's error log is redirected to stderr, so that the error log goes into the Docker container's log and is viewable using the docker logs mysqld-container command.

![](_page_189_Picture_8.jpeg)

### **Note**

The variable has no effect if a server configuration file from the host has been mounted (see [Persisting Data and Configuration Changes](#page-184-0) on bind-mounting a configuration file).

<span id="page-189-3"></span>• [MYSQL\\_ROOT\\_PASSWORD](#page-189-3): This variable specifies a password that is set for the MySQL root account.

![](_page_189_Picture_12.jpeg)

### **Warning**

Setting the MySQL root user password on the command line is insecure. As an alternative to specifying the password explicitly, you can set the variable with a container file path for a password file, and then mount a file from your host that contains the password at the container file path. This is still not very secure, as the location of the password file is still exposed. It is preferable to use the default settings of [MYSQL\\_RANDOM\\_ROOT\\_PASSWORD](#page-188-3) and [MYSQL\\_ONETIME\\_PASSWORD](#page-188-0) both being true.

<span id="page-189-2"></span>• [MYSQL\\_ALLOW\\_EMPTY\\_PASSWORD](#page-189-2). Set it to true to allow the container to be started with a blank password for the root user.

![](_page_189_Picture_16.jpeg)

### **Warning**

Setting this variable to true is insecure, because it is going to leave your MySQL instance completely unprotected, allowing anyone to gain complete superuser access. It is preferable to use the default settings of [MYSQL\\_RANDOM\\_ROOT\\_PASSWORD](#page-188-3) and [MYSQL\\_ONETIME\\_PASSWORD](#page-188-0) both being true.

# <span id="page-189-0"></span>**2.5.6.3 Deploying MySQL on Windows and Other Non-Linux Platforms with Docker**

![](_page_190_Picture_1.jpeg)

### **Warning**

The MySQL Docker images provided by Oracle are built specifically for Linux platforms. Other platforms are not supported, and users running the MySQL Docker images from Oracle on them are doing so at their own risk. This section discusses some known issues for the images when used on non-Linux platforms.

Known Issues for using the MySQL Server Docker images from Oracle on Windows include:

• If you are bind-mounting on the container's MySQL data directory (see [Persisting Data and](#page-184-0) [Configuration Changes](#page-184-0) for details), you have to set the location of the server socket file with the - socket option to somewhere outside of the MySQL data directory; otherwise, the server fails to start. This is because the way Docker for Windows handles file mounting does not allow a host file from being bind-mounted on the socket file.

# <span id="page-190-0"></span>**2.5.7 Installing MySQL on Linux from the Native Software Repositories**

Many Linux distributions include a version of the MySQL server, client tools, and development components in their native software repositories and can be installed with the platforms' standard package management systems. This section provides basic instructions for installing MySQL using those package management systems.

![](_page_190_Picture_8.jpeg)

### **Important**

Native packages are often several versions behind the currently available release. You are also normally unable to install development milestone releases (DMRs), since these are not usually made available in the native repositories. Before proceeding, we recommend that you check out the other installation options described in [Section 2.5, "Installing MySQL on Linux"](#page-152-0).

Distribution specific instructions are shown below:

• **Red Hat Linux, Fedora, CentOS**

![](_page_190_Picture_13.jpeg)

### **Note**

For a number of Linux distributions, you can install MySQL using the MySQL Yum repository instead of the platform's native software repository. See [Section 2.5.1, "Installing MySQL on Linux Using the MySQL Yum Repository"](#page-153-0) for details.

For Red Hat and similar distributions, the MySQL distribution is divided into a number of separate packages, mysql for the client tools, mysql-server for the server and associated tools, and mysql-libs for the libraries. The libraries are required if you want to provide connectivity from different languages and environments such as Perl, Python and others.

To install, use the yum command to specify the packages that you want to install. For example:

```
#> yum install mysql mysql-server mysql-libs mysql-server
Loaded plugins: presto, refresh-packagekit
Setting up Install Process
Resolving Dependencies
--> Running transaction check
---> Package mysql.x86_64 0:5.1.48-2.fc13 set to be updated
---> Package mysql-libs.x86_64 0:5.1.48-2.fc13 set to be updated
---> Package mysql-server.x86_64 0:5.1.48-2.fc13 set to be updated
--> Processing Dependency: perl-DBD-MySQL for package: mysql-server-5.1.48-2.fc13.x86_64
--> Running transaction check
---> Package perl-DBD-MySQL.x86_64 0:4.017-1.fc13 set to be updated
--> Finished Dependency Resolution
```

| Dependencies Resolved                                                                                                                                                                                                                                                                                                                                                                                                                        |                                      |                                                                                                                                                  |                                            |                                   |
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------|-----------------------------------|
| ================================================================================<br>Package                                                                                                                                                                                                                                                                                                                                                  | Arch                                 | Version                                                                                                                                          | Repository                                 | Size                              |
| ================================================================================<br>Installing:<br>mysql<br>mysql-libs<br>mysql-server<br>Installing for dependencies:<br>perl-DBD-MySQL<br>Transaction Summary<br>================================================================================                                                                                                                                          | x86_64<br>x86_64<br>x86_64<br>x86_64 | 5.1.48-2.fc13<br>5.1.48-2.fc13<br>5.1.48-2.fc13<br>4.017-1.fc13                                                                                  | updates<br>updates<br>updates<br>updates   | 889 k<br>1.2 M<br>8.1 M<br>136 k  |
| Upgrade<br>0 Package(s)<br>Total download size: 10 M<br>Installed size: 30 M<br>Is this ok [y/N]: y<br>Downloading Packages:<br>Setting up and reading Presto delta metadata<br>Processing delta metadata<br>Package(s) data still to download: 10 M<br>(1/4): mysql-5.1.48-2.fc13.x86_64.rpm<br>(2/4): mysql-libs-5.1.48-2.fc13.x86_64.rpm<br>(3/4): mysql-server-5.1.48-2.fc13.x86_64.rpm<br>(4/4): perl-DBD-MySQL-4.017-1.fc13.x86_64.rpm |                                      |                                                                                                                                                  | 889 kB<br>  1.2 MB<br>  8.1 MB<br>  136 kB | 00:04<br>00:06<br>00:40<br>00:00  |
| <br>Total<br>Running rpm_check_debug<br>Running Transaction Test<br>Transaction Test Succeeded<br>Running Transaction<br>Installing<br>Installing<br>Installing<br>Installing                                                                                                                                                                                                                                                                |                                      | : mysql-libs-5.1.48-2.fc13.x86_64<br>: mysql-5.1.48-2.fc13.x86_64<br>: perl-DBD-MySQL-4.017-1.fc13.x86_64<br>: mysql-server-5.1.48-2.fc13.x86_64 | 201 kB/s   10 MB                           | 00:52<br>1/4<br>2/4<br>3/4<br>4/4 |
| Installed:<br>mysql.x86_64 0:5.1.48-2.fc13<br>mysql-server.x86_64 0:5.1.48-2.fc13<br>Dependency Installed:                                                                                                                                                                                                                                                                                                                                   |                                      |                                                                                                                                                  | mysql-libs.x86_64 0:5.1.48-2.fc13          |                                   |
| perl-DBD-MySQL.x86_64 0:4.017-1.fc13<br>Complete!                                                                                                                                                                                                                                                                                                                                                                                            |                                      |                                                                                                                                                  |                                            |                                   |

MySQL and the MySQL server should now be installed. A sample configuration file is installed into / etc/my.cnf. To start the MySQL server use systemctl:

```
$> systemctl start mysqld
```

The database tables are automatically created for you, if they do not already exist. You should, however, run mysql\_secure\_installation to set the root passwords on your server.

### • **Debian, Ubuntu, Kubuntu**

![](_page_191_Picture_6.jpeg)

## **Note**

For supported Debian and Ubuntu versions, MySQL can be installed using the [MySQL APT Repository](https://dev.mysql.com/downloads/repo/apt/) instead of the platform's native software repository. See [Section 2.5.2, "Installing MySQL on Linux Using the MySQL](#page-158-0) [APT Repository"](#page-158-0) for details.

On Debian and related distributions, there are two packages for MySQL in their software repositories, mysql-client and mysql-server, for the client and server components respectively. You should specify an explicit version, for example mysql-client-5.1, to ensure that you install the version of MySQL that you want.

To download and install, including any dependencies, use the apt-get command, specifying the packages that you want to install.

![](_page_192_Picture_2.jpeg)

### **Note**

Before installing, make sure that you update your apt-get index files to ensure you are downloading the latest available version.

![](_page_192_Picture_5.jpeg)

### **Note**

The apt-get command installs a number of packages, including the MySQL server, in order to provide the typical tools and application environment. This can mean that you install a large number of packages in addition to the main MySQL package.

During installation, the initial database is created, and you are prompted for the MySQL root password (and confirmation). A configuration file is created in /etc/mysql/my.cnf. An init script is created in /etc/init.d/mysql.

The server should already be started. You can manually start and stop the server using:

```
#> service mysql [start|stop]
```

The service is automatically added to the 2, 3 and 4 run levels, with stop scripts in the single, shutdown and restart levels.

# <span id="page-192-0"></span>**2.5.8 Installing MySQL on Linux with Juju**

The Juju deployment framework supports easy installation and configuration of MySQL servers. For instructions, see [https://jujucharms.com/mysql/.](https://jujucharms.com/mysql/)

# <span id="page-192-1"></span>**2.5.9 Managing MySQL Server with systemd**

If you install MySQL using an RPM or Debian package on the following Linux platforms, server startup and shutdown is managed by systemd:

- RPM package platforms:
  - Enterprise Linux variants version 7 and higher
  - SUSE Linux Enterprise Server 12 and higher
  - Fedora 29 and higher
- Debian family platforms:
  - Debian platforms
  - Ubuntu platforms

If you install MySQL from a generic binary distribution on a platform that uses systemd, you can manually configure systemd support for MySQL following the instructions provided in the postinstallation setup section of the [MySQL 8.4 Secure Deployment Guide.](https://dev.mysql.com/doc/mysql-secure-deployment-guide/en/)

If you install MySQL from a source distribution on a platform that uses systemd, obtain systemd support for MySQL by configuring the distribution using the -DWITH\_SYSTEMD=1 CMake option. See Section 2.8.7, "MySQL Source-Configuration Options".

The following discussion covers these topics:

• [Overview of systemd](#page-193-0)

- [Configuring systemd for MySQL](#page-193-1)
- [Configuring Multiple MySQL Instances Using systemd](#page-195-0)
- [Migrating from mysqld\\_safe to systemd](#page-197-1)

![](_page_193_Picture_4.jpeg)

### **Note**

On platforms for which systemd support for MySQL is installed, scripts such as mysqld\_safe and the System V initialization script are unnecessary and are not installed. For example, mysqld\_safe can handle server restarts, but systemd provides the same capability, and does so in a manner consistent with management of other services rather than by using an application-specific program.

One implication of the non-use of mysqld\_safe on platforms that use systemd for server management is that use of [mysqld\_safe] or [safe\_mysqld] sections in option files is not supported and might lead to unexpected behavior.

Because systemd has the capability of managing multiple MySQL instances on platforms for which systemd support for MySQL is installed, mysqld\_multi and mysqld\_multi.server are unnecessary and are not installed.

# <span id="page-193-0"></span>**Overview of systemd**

systemd provides automatic MySQL server startup and shutdown. It also enables manual server management using the systemctl command. For example:

```
$> systemctl {start|stop|restart|status} mysqld
```

Alternatively, use the service command (with the arguments reversed), which is compatible with System V systems:

\$> **service mysqld {start|stop|restart|status}**

![](_page_193_Picture_14.jpeg)

# **Note**

For the systemctl command (and the alternative service command), if the MySQL service name is not mysqld then use the appropriate name. For example, use mysql rather than mysqld on Debian-based and SLES systems.

Support for systemd includes these files:

- mysqld.service (RPM platforms), mysql.service (Debian platforms): systemd service unit configuration file, with details about the MySQL service.
- mysqld@.service (RPM platforms), mysql@.service (Debian platforms): Like mysqld.service or mysql.service, but used for managing multiple MySQL instances.
- mysqld.tmpfiles.d: File containing information to support the tmpfiles feature. This file is installed under the name mysql.conf.
- mysqld\_pre\_systemd (RPM platforms), mysql-system-start (Debian platforms): Support script for the unit file. This script assists in creating the error log file only if the log location matches a pattern (/var/log/mysql\*.log for RPM platforms, /var/log/mysql/\*.log for Debian platforms). In other cases, the error log directory must be writable or the error log must be present and writable for the user running the mysqld process.

# <span id="page-193-1"></span>**Configuring systemd for MySQL**

To add or change systemd options for MySQL, these methods are available:

• Use a localized systemd configuration file.

- Arrange for systemd to set environment variables for the MySQL server process.
- Set the MYSQLD\_OPTS systemd variable.

To use a localized systemd configuration file, create the /etc/systemd/system/ mysqld.service.d directory if it does not exist. In that directory, create a file that contains a [Service] section listing the desired settings. For example:

```
[Service]
LimitNOFILE=max_open_files
Nice=nice_level
LimitCore=core_file_limit
Environment="LD_PRELOAD=/path/to/malloc/library"
Environment="TZ=time_zone_setting"
```

The discussion here uses override.conf as the name of this file. Newer versions of systemd support the following command, which opens an editor and permits you to edit the file:

```
systemctl edit mysqld # RPM platforms
systemctl edit mysql # Debian platforms
```

Whenever you create or change override.conf, reload the systemd configuration, then tell systemd to restart the MySQL service:

```
systemctl daemon-reload
systemctl restart mysqld # RPM platforms
systemctl restart mysql # Debian platforms
```

With systemd, the override.conf configuration method must be used for certain parameters, rather than settings in a [mysqld], [mysqld\_safe], or [safe\_mysqld] group in a MySQL option file:

- For some parameters, override.conf must be used because systemd itself must know their values and it cannot read MySQL option files to get them.
- Parameters that specify values otherwise settable only using options known to mysqld\_safe must be specified using systemd because there is no corresponding mysqld parameter.

For additional information about using systemd rather than mysqld\_safe, see [Migrating from](#page-197-1) [mysqld\\_safe to systemd](#page-197-1).

You can set the following parameters in override.conf:

- To set the number of file descriptors available to the MySQL server, use LimitNOFILE in override.conf rather than the open\_files\_limit system variable for mysqld or --openfiles-limit option for mysqld\_safe.
- To set the maximum core file size, use LimitCore in override.conf rather than the --corefile-size option for mysqld\_safe.
- To set the scheduling priority for the MySQL server, use Nice in override.conf rather than the --nice option for mysqld\_safe.

Some MySQL parameters are configured using environment variables:

- LD\_PRELOAD: Set this variable if the MySQL server should use a specific memory-allocation library.
- NOTIFY\_SOCKET: This environment variable specifies the socket that mysqld uses to communicate notification of startup completion and service status change with systemd. It is set by systemd when the mysqld service is started. The mysqld service reads the variable setting and writes to the defined location.

In MySQL 8.4, mysqld uses the Type=notify process startup type. (Type=forking was used in MySQL 5.7.) With Type=notify, systemd automatically configures a socket file and exports the path to the NOTIFY\_SOCKET environment variable.

• TZ: Set this variable to specify the default time zone for the server.

There are multiple ways to specify environment variable values for use by the MySQL server process managed by systemd:

- Use Environment lines in the override.conf file. For the syntax, see the example in the preceding discussion that describes how to use this file.
- Specify the values in the /etc/sysconfig/mysql file (create the file if it does not exist). Assign values using the following syntax:

```
LD_PRELOAD=/path/to/malloc/library
TZ=time_zone_setting
```

After modifying /etc/sysconfig/mysql, restart the server to make the changes effective:

```
systemctl restart mysqld # RPM platforms
systemctl restart mysql # Debian platforms
```

To specify options for mysqld without modifying systemd configuration files directly, set or unset the MYSQLD\_OPTS systemd variable. For example:

```
systemctl set-environment MYSQLD_OPTS="--general_log=1"
systemctl unset-environment MYSQLD_OPTS
```

MYSQLD\_OPTS can also be set in the /etc/sysconfig/mysql file.

After modifying the systemd environment, restart the server to make the changes effective:

```
systemctl restart mysqld # RPM platforms
systemctl restart mysql # Debian platforms
```

For platforms that use systemd, the data directory is initialized if empty at server startup. This might be a problem if the data directory is a remote mount that has temporarily disappeared: The mount point would appear to be an empty data directory, which then would be initialized as a new data directory. To suppress this automatic initialization behavior, specify the following line in the /etc/sysconfig/ mysql file (create the file if it does not exist):

```
NO_INIT=true
```

# <span id="page-195-0"></span>**Configuring Multiple MySQL Instances Using systemd**

This section describes how to configure systemd for multiple instances of MySQL.

![](_page_195_Picture_16.jpeg)

### **Note**

Because systemd has the capability of managing multiple MySQL instances on platforms for which systemd support is installed, mysqld\_multi and mysqld\_multi.server are unnecessary and are not installed.

To use multiple-instance capability, modify the my.cnf option file to include configuration of key options for each instance. These file locations are typical:

- /etc/my.cnf or /etc/mysql/my.cnf (RPM platforms)
- /etc/mysql/mysql.conf.d/mysqld.cnf (Debian platforms)

For example, to manage two instances named replica01 and replica02, add something like this to the option file:

## RPM platforms:

```
[mysqld@replica01]
datadir=/var/lib/mysql-replica01
socket=/var/lib/mysql-replica01/mysql.sock
port=3307
log-error=/var/log/mysqld-replica01.log
```

```
[mysqld@replica02]
datadir=/var/lib/mysql-replica02
socket=/var/lib/mysql-replica02/mysql.sock
port=3308
log-error=/var/log/mysqld-replica02.log
```

### Debian platforms:

```
[mysqld@replica01]
datadir=/var/lib/mysql-replica01
socket=/var/lib/mysql-replica01/mysql.sock
port=3307
log-error=/var/log/mysql/replica01.log
[mysqld@replica02]
datadir=/var/lib/mysql-replica02
socket=/var/lib/mysql-replica02/mysql.sock
port=3308
log-error=/var/log/mysql/replica02.log
```

The replica names shown here use @ as the delimiter because that is the only delimiter supported by systemd.

Instances then are managed by normal systemd commands, such as:

```
systemctl start mysqld@replica01
systemctl start mysqld@replica02
```

To enable instances to run at boot time, do this:

```
systemctl enable mysqld@replica01
systemctl enable mysqld@replica02
```

Use of wildcards is also supported. For example, this command displays the status of all replica instances:

```
systemctl status 'mysqld@replica*'
```

For management of multiple MySQL instances on the same machine, systemd automatically uses a different unit file:

- mysqld@.service rather than mysqld.service (RPM platforms)
- mysql@.service rather than mysql.service (Debian platforms)

In the unit file, %I and %i reference the parameter passed in after the @ marker and are used to manage the specific instance. For a command such as this:

```
systemctl start mysqld@replica01
```

systemd starts the server using a command such as this:

```
mysqld --defaults-group-suffix=@%I ...
```

The result is that the [server], [mysqld], and [mysqld@replica01] option groups are read and used for that instance of the service.

![](_page_196_Picture_19.jpeg)

### **Note**

On Debian platforms, AppArmor prevents the server from reading or writing / var/lib/mysql-replica\*, or anything other than the default locations. To address this, you must customize or disable the profile in /etc/apparmor.d/ usr.sbin.mysqld.

![](_page_196_Picture_22.jpeg)

### **Note**

On Debian platforms, the packaging scripts for MySQL uninstallation cannot currently handle mysqld@ instances. Before removing or upgrading the package, you must stop any extra instances manually first.

# <span id="page-197-1"></span>**Migrating from mysqld\_safe to systemd**

Because mysqld\_safe is not installed on platforms that use systemd to manage MySQL, options previously specified for that program (for example, in an [mysqld\_safe] or [safe\_mysqld] option group) must be specified another way:

• Some mysqld\_safe options are also understood by mysqld and can be moved from the [mysqld\_safe] or [safe\_mysqld] option group to the [mysqld] group. This does not include --pid-file, --open-files-limit, or --nice. To specify those options, use the override.conf systemd file, described previously.

![](_page_197_Picture_4.jpeg)

### **Note**

On systemd platforms, use of [mysqld\_safe] and [safe\_mysqld] option groups is not supported and may lead to unexpected behavior.

- For some mysqld\_safe options, there are alternative mysqld procedures. For example, the mysqld\_safe option for enabling syslog logging is --syslog, which is deprecated. To write error log output to the system log, use the instructions at Section 7.4.2.8, "Error Logging to the System Log".
- mysqld\_safe options not understood by mysqld can be specified in override.conf or environment variables. For example, with mysqld\_safe, if the server should use a specific memory allocation library, this is specified using the --malloc-lib option. For installations that manage the server with systemd, arrange to set the LD\_PRELOAD environment variable instead, as described previously.

# <span id="page-197-0"></span>**2.6 Installing MySQL Using Unbreakable Linux Network (ULN)**

Linux supports a number of different solutions for installing MySQL, covered in [Section 2.5,](#page-152-0) ["Installing MySQL on Linux".](#page-152-0) One of the methods, covered in this section, is installing from Oracle's Unbreakable Linux Network (ULN). You can find information about Oracle Linux and ULN under [http://](http://linux.oracle.com/) [linux.oracle.com/](http://linux.oracle.com/).

To use ULN, you need to obtain a ULN login and register the machine used for installation with ULN. This is described in detail in the [ULN FAQ](https://linux.oracle.com/uln_faq.md). The page also describes how to install and update packages.

Both Community and Commercial packages are supported, and each offers three MySQL channels:

- Server: MySQL Server
- Connectors: MySQL Connector/C++, MySQL Connector/J, MySQL Connector/ODBC, and MySQL Connector/Python.
- Tools: MySQL Router, MySQL Shell, and MySQL Workbench

The Community channels are available to all ULN users.

Accessing commercial MySQL ULN packages at oracle.linux.com requires you to provide a CSI with a valid commercial license for MySQL (Enterprise or Standard). As of this writing, valid purchases are 60944, 60945, 64911, and 64912. The appropriate CSI makes commercial MySQL subscription channels available in your ULN GUI interface.

Once MySQL has been installed using ULN, you can find information on starting and stopping the server, and more, at [Section 2.5.7, "Installing MySQL on Linux from the Native Software Repositories"](#page-190-0), particularly under [Section 2.5.4, "Installing MySQL on Linux Using RPM Packages from Oracle"](#page-172-0).

If you are changing your package source to use ULN and not changing which build of MySQL you are using, then back up your data, remove your existing binaries, and replace them with those from ULN. If a change of build is involved, we recommend the backup be a dump (from mysqldump or [MySQL](https://dev.mysql.com/doc/mysql-shell/8.4/en/mysql-shell-utilities-dump-instance-schema.md) [Shell's backup utility\)](https://dev.mysql.com/doc/mysql-shell/8.4/en/mysql-shell-utilities-dump-instance-schema.md) just in case you need to rebuild your data after the new binaries are in place.

If this shift to ULN crosses a version boundary, consult this section before proceeding: Chapter 3, Upgrading MySQL.

# <span id="page-198-0"></span>**2.7 Installing MySQL on Solaris**

![](_page_198_Picture_3.jpeg)

### **Note**

MySQL 8.4 supports Solaris 11.4 and higher

MySQL on Solaris is available in a number of different formats.

- For information on installing using the native Solaris PKG format, see [Section 2.7.1, "Installing](#page-198-1) [MySQL on Solaris Using a Solaris PKG".](#page-198-1)
- To use a standard tar binary installation, use the notes provided in [Section 2.2, "Installing MySQL](#page-104-1) [on Unix/Linux Using Generic Binaries".](#page-104-1) Check the notes and hints at the end of this section for Solaris specific notes that you may need before or after installation.

To obtain a binary MySQL distribution for Solaris in tarball or PKG format, [https://dev.mysql.com/](https://dev.mysql.com/downloads/mysql/8.4.md) [downloads/mysql/8.4.html](https://dev.mysql.com/downloads/mysql/8.4.md).

Additional notes to be aware of when installing and using MySQL on Solaris:

• If you want to use MySQL with the mysql user and group, use the groupadd and useradd commands:

```
groupadd mysql
useradd -g mysql -s /bin/false mysql
```

• If you install MySQL using a binary tarball distribution on Solaris, because the Solaris tar cannot handle long file names, use GNU tar (gtar) to unpack the distribution. If you do not have GNU tar on your system, install it with the following command:

```
pkg install archiver/gnu-tar
```

- You should mount any file systems on which you intend to store InnoDB files with the forcedirectio option. (By default mounting is done without this option.) Failing to do so causes a significant drop in performance when using the InnoDB storage engine on this platform.
- If you would like MySQL to start automatically, you can copy support-files/mysql.server to / etc/init.d and create a symbolic link to it named /etc/rc3.d/S99mysql.server.
- If too many processes try to connect very rapidly to mysqld, you should see this error in the MySQL log:

```
Error in accept: Protocol error
```

You might try starting the server with the --back\_log=50 option as a workaround for this.

• To configure the generation of core files on Solaris you should use the coreadm command. Because of the security implications of generating a core on a setuid() application, by default, Solaris does not support core files on setuid() programs. However, you can modify this behavior using coreadm. If you enable setuid() core files for the current user, they are generated using mode 600 and are owned by the superuser.

# <span id="page-198-1"></span>**2.7.1 Installing MySQL on Solaris Using a Solaris PKG**

You can install MySQL on Solaris using a binary package of the native Solaris PKG format instead of the binary tarball distribution.

To use this package, download the corresponding mysql-VERSION-solaris11- PLATFORM.pkg.gz file, then uncompress it. For example:

```
$> gunzip mysql-8.4.8-solaris11-x86_64.pkg.gz
```

To install a new package, use pkgadd and follow the onscreen prompts. You must have root privileges to perform this operation:

```
$> pkgadd -d mysql-8.4.8-solaris11-x86_64.pkg
The following packages are available:
 1 mysql MySQL Community Server (GPL)
 (i86pc) 8.4.8
Select package(s) you wish to process (or 'all' to process
all packages). (default: all) [?,??,q]:
```

The PKG installer installs all of the files and tools needed, and then initializes your database if one does not exist. To complete the installation, you should set the root password for MySQL as provided in the instructions at the end of the installation. Alternatively, you can run the mysql\_secure\_installation script that comes with the installation.

By default, the PKG package installs MySQL under the root path /opt/mysql. You can change only the installation root path when using pkgadd, which can be used to install MySQL in a different Solaris zone. If you need to install in a specific directory, use a binary tar file distribution.

The pkg installer copies a suitable startup script for MySQL into /etc/init.d/mysql. To enable MySQL to startup and shutdown automatically, you should create a link between this file and the init script directories. For example, to ensure safe startup and shutdown of MySQL you could use the following commands to add the right links:

```
$> ln /etc/init.d/mysql /etc/rc3.d/S91mysql
$> ln /etc/init.d/mysql /etc/rc0.d/K02mysql
```

To remove MySQL, the installed package name is mysql. You can use this in combination with the pkgrm command to remove the installation.

To upgrade when using the Solaris package file format, you must remove the existing installation before installing the updated package. Removal of the package does not delete the existing database information, only the server, binaries and support files. The typical upgrade sequence is therefore:

```
$> mysqladmin shutdown
$> pkgrm mysql
$> pkgadd -d mysql-8.4.8-solaris11-x86_64.pkg
$> mysqld_safe &
```

You should check the notes in Chapter 3, Upgrading MySQL before performing any upgrade.

# <span id="page-199-0"></span>**2.8 Installing MySQL from Source**

Building MySQL from the source code enables you to customize build parameters, compiler optimizations, and installation location. For a list of systems on which MySQL is known to run, see <https://www.mysql.com/support/supportedplatforms/database.html>.

Before you proceed with an installation from source, check whether Oracle produces a precompiled binary distribution for your platform and whether it works for you. We put a great deal of effort into ensuring that our binaries are built with the best possible options for optimal performance. Instructions for installing binary distributions are available in [Section 2.2, "Installing MySQL on Unix/Linux Using](#page-104-1) [Generic Binaries"](#page-104-1).

If you are interested in building MySQL from a source distribution using build options the same as or similar to those use by Oracle to produce binary distributions on your platform, obtain a binary distribution, unpack it, and look in the docs/INFO\_BIN file, which contains information about how that MySQL distribution was configured and compiled.

![](_page_199_Picture_15.jpeg)

### **Warning**

Building MySQL with nonstandard options may lead to reduced functionality, performance, or security.

The MySQL source code contains internal documentation written using Doxygen. The generated Doxygen content is available at<https://dev.mysql.com/doc/index-other.html>. It is also possible to generate this content locally from a MySQL source distribution using the instructions at [Section 2.8.10,](#page-34-0) ["Generating MySQL Doxygen Documentation Content"](#page-34-0).