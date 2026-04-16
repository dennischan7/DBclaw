---
source: MySQL 8.4 Reference
title: 00_Overview
---

To install MySQL manually, do the following:

- 1. If you are upgrading from a previous version then refer to Section 3.11, "Upgrading MySQL on Windows" before beginning the upgrade process.
- 2. Make sure that you are logged in as a user with administrator privileges.
- 3. Choose an installation location. Traditionally, the MySQL server is installed in C:\mysql. If you do not install MySQL at C:\mysql, you must specify the path to the install directory during startup or in an option file. See [Section 2.3.3.2, "Creating an Option File"](#page-130-0).

![](_page_130_Picture_1.jpeg)

### **Note**

The MSI installs MySQL under C:\Program Files\MySQL\MySQL Server 8.4.

4. Extract the install archive to the chosen installation location using your preferred file-compression tool. Some tools may extract the archive to a folder within your chosen installation location. If this occurs, you can move the contents of the subfolder into the chosen installation location.

# <span id="page-130-0"></span>**2.3.3.2 Creating an Option File**

If you need to specify startup options when you run the server, you can indicate them on the command line or place them in an option file. For options that are used every time the server starts, you may find it most convenient to use an option file to specify your MySQL configuration. This is particularly true under the following circumstances:

- The installation or data directory locations are different from the default locations (C:\Program Files\MySQL\MySQL Server 8.4 and C:\Program Files\MySQL\MySQL Server 8.4\data).
- You need to tune the server settings, such as memory, cache, or InnoDB configuration information.

When the MySQL server starts on Windows, it looks for option files in several locations, such as the Windows directory, C:\, and the MySQL installation directory (for the full list of locations, see Section 6.2.2.2, "Using Option Files"). The Windows directory typically is named something like C: \WINDOWS. You can determine its exact location from the value of the WINDIR environment variable using the following command:

```
C:\> echo %WINDIR%
```

MySQL looks for options in each location first in the my.ini file, and then in the my.cnf file. However, to avoid confusion, it is best if you use only one file. If your PC uses a boot loader where C: is not the boot drive, your only option is to use the my.ini file. Whichever option file you use, it must be a plain text file.

![](_page_130_Picture_12.jpeg)

### **Note**

When using MySQL Configurator to configure MySQL Server, it creates the my.ini at the default location, and the user executing MySQL Configurator is granted full permissions to this new my.ini file.

In other words, be sure that the MySQL Server user has permission to read the my.ini file.

You can also make use of the example option files included with your MySQL distribution; see Section 7.1.2, "Server Configuration Defaults".

An option file can be created and modified with any text editor, such as Notepad. For example, if MySQL is installed in E:\mysql and the data directory is in E:\mydata\data, you can create an option file containing a [mysqld] section to specify values for the basedir and datadir options:

```
[mysqld]
# set basedir to your installation path
basedir=E:/mysql
# set datadir to the location of your data directory
datadir=E:/mydata/data
```

Microsoft Windows path names are specified in option files using (forward) slashes rather than backslashes. If you do use backslashes, double them:

[mysqld]

```
# set basedir to your installation path
basedir=E:\\mysql
# set datadir to the location of your data directory
datadir=E:\\mydata\\data
```

The rules for use of backslash in option file values are given in Section 6.2.2.2, "Using Option Files".

The ZIP archive does not include a data directory. To initialize a MySQL installation by creating the data directory and populating the tables in the mysql system database, initialize MySQL using either - initialize or --initialize-insecure. For additional information, see Section 2.9.1, "Initializing the Data Directory".

If you would like to use a data directory in a different location, you should copy the entire contents of the data directory to the new location. For example, if you want to use E:\mydata as the data directory instead, you must do two things:

- 1. Move the entire data directory and all of its contents from the default location (for example C: \Program Files\MySQL\MySQL Server 8.4\data) to E:\mydata.
- 2. Use a --datadir option to specify the new data directory location each time you start the server.

# <span id="page-131-0"></span>**2.3.3.3 Selecting a MySQL Server Type**

The following table shows the available servers for Windows in MySQL 8.4.

| Binary       | Description                                                                               |
|--------------|-------------------------------------------------------------------------------------------|
| mysqld       | Optimized binary with named-pipe support                                                  |
| mysqld-debug | Like mysqld, but compiled with full debugging<br>and automatic memory allocation checking |

Each of the servers in a distribution support the same set of storage engines. The SHOW ENGINES statement displays which engines a given server supports.

All Windows MySQL 8.4 servers have support for symbolic linking of database directories.

MySQL supports TCP/IP on all Windows platforms. MySQL servers on Windows also support named pipes, if you start the server with the named\_pipe system variable enabled. It is necessary to enable this variable explicitly because some users have experienced problems with shutting down the MySQL server when named pipes were used. The default is to use TCP/IP regardless of platform because named pipes are slower than TCP/IP in many Windows configurations.