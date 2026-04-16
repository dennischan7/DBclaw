---
source: MySQL 8.0 Reference
title: 00_Overview
---

The Juju deployment framework supports easy installation and configuration of MySQL servers. For instructions, see [https://jujucharms.com/mysql/.](https://jujucharms.com/mysql/)

# <span id="page-47-0"></span>**2.5.9 Managing MySQL Server with systemd**

If you install MySQL using an RPM or Debian package on the following Linux platforms, server startup and shutdown is managed by systemd:

- RPM package platforms:
  - Enterprise Linux variants version 7 and higher
  - SUSE Linux Enterprise Server 12 and higher
  - Fedora 29 and higher
- Debian family platforms:
  - Debian platforms
  - Ubuntu platforms

If you install MySQL from a generic binary distribution on a platform that uses systemd, you can manually configure systemd support for MySQL following the instructions provided in the postinstallation setup section of the [MySQL Secure Deployment Guide.](https://dev.mysql.com/doc/mysql-secure-deployment-guide/en/)

If you install MySQL from a source distribution on a platform that uses systemd, obtain systemd support for MySQL by configuring the distribution using the [-DWITH\\_SYSTEMD=1](#page-87-0) CMake option. See [Section 2.8.7, "MySQL Source-Configuration Options"](#page-63-0).

The following discussion covers these topics:

- [Overview of systemd](#page-47-1)
- [Configuring systemd for MySQL](#page-48-0)
- [Configuring Multiple MySQL Instances Using systemd](#page-50-0)
- [Migrating from mysqld\\_safe to systemd](#page-51-0)

![](_page_47_Picture_19.jpeg)

## **Note**

On platforms for which systemd support for MySQL is installed, scripts such as mysqld\_safe and the System V initialization script are unnecessary and are not installed. For example, mysqld\_safe can handle server restarts, but systemd provides the same capability, and does so in a manner consistent with management of other services rather than by using an application-specific program.

One implication of the non-use of mysqld\_safe on platforms that use systemd for server management is that use of [mysqld\_safe] or [safe\_mysqld] sections in option files is not supported and might lead to unexpected behavior.

Because systemd has the capability of managing multiple MySQL instances on platforms for which systemd support for MySQL is installed, mysqld\_multi and mysqld\_multi.server are unnecessary and are not installed.

### <span id="page-47-1"></span>**Overview of systemd**

systemd provides automatic MySQL server startup and shutdown. It also enables manual server management using the systemctl command. For example:

```
$> systemctl {start|stop|restart|status} mysqld
```

Alternatively, use the service command (with the arguments reversed), which is compatible with System V systems:

\$> **service mysqld {start|stop|restart|status}**

![](_page_48_Picture_4.jpeg)

### **Note**

For the systemctl command (and the alternative service command), if the MySQL service name is not mysqld then use the appropriate name. For example, use mysql rather than mysqld on Debian-based and SLES systems.

Support for systemd includes these files:

- mysqld.service (RPM platforms), mysql.service (Debian platforms): systemd service unit configuration file, with details about the MySQL service.
- mysqld@.service (RPM platforms), mysql@.service (Debian platforms): Like mysqld.service or mysql.service, but used for managing multiple MySQL instances.
- mysqld.tmpfiles.d: File containing information to support the tmpfiles feature. This file is installed under the name mysql.conf.
- mysqld\_pre\_systemd (RPM platforms), mysql-system-start (Debian platforms): Support script for the unit file. This script assists in creating the error log file only if the log location matches a pattern (/var/log/mysql\*.log for RPM platforms, /var/log/mysql/\*.log for Debian platforms). In other cases, the error log directory must be writable or the error log must be present and writable for the user running the mysqld process.

## <span id="page-48-0"></span>**Configuring systemd for MySQL**

To add or change systemd options for MySQL, these methods are available:

- Use a localized systemd configuration file.
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

For additional information about using systemd rather than mysqld\_safe, see [Migrating from](#page-51-0) [mysqld\\_safe to systemd](#page-51-0).

You can set the following parameters in override.conf:

- To set the number of file descriptors available to the MySQL server, use LimitNOFILE in override.conf rather than the open\_files\_limit system variable for mysqld or --openfiles-limit option for mysqld\_safe.
- To set the maximum core file size, use LimitCore in override.conf rather than the --corefile-size option for mysqld\_safe.
- To set the scheduling priority for the MySQL server, use Nice in override.conf rather than the --nice option for mysqld\_safe.

Some MySQL parameters are configured using environment variables:

- LD\_PRELOAD: Set this variable if the MySQL server should use a specific memory-allocation library.
- NOTIFY\_SOCKET: This environment variable specifies the socket that mysqld uses to communicate notification of startup completion and service status change with systemd. It is set by systemd when the mysqld service is started. The mysqld service reads the variable setting and writes to the defined location.

In MySQL 8.0, mysqld uses the Type=notify process startup type. (Type=forking was used in MySQL 5.7.) With Type=notify, systemd automatically configures a socket file and exports the path to the NOTIFY\_SOCKET environment variable.

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

NO\_INIT=true

## <span id="page-50-0"></span>**Configuring Multiple MySQL Instances Using systemd**

This section describes how to configure systemd for multiple instances of MySQL.

![](_page_50_Picture_5.jpeg)

### **Note**

Because systemd has the capability of managing multiple MySQL instances on platforms for which systemd support is installed, mysqld\_multi and mysqld\_multi.server are unnecessary and are not installed.

To use multiple-instance capability, modify the my.cnf option file to include configuration of key options for each instance. These file locations are typical:

- /etc/my.cnf or /etc/mysql/my.cnf (RPM platforms)
- /etc/mysql/mysql.conf.d/mysqld.cnf (Debian platforms)

For example, to manage two instances named replica01 and replica02, add something like this to the option file:

#### RPM platforms:

```
[mysqld@replica01]
datadir=/var/lib/mysql-replica01
socket=/var/lib/mysql-replica01/mysql.sock
port=3307
log-error=/var/log/mysqld-replica01.log
[mysqld@replica02]
datadir=/var/lib/mysql-replica02
socket=/var/lib/mysql-replica02/mysql.sock
port=3308
log-error=/var/log/mysqld-replica02.log
```

#### Debian platforms:

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

![](_page_51_Picture_11.jpeg)

#### **Note**

On Debian platforms, AppArmor prevents the server from reading or writing / var/lib/mysql-replica\*, or anything other than the default locations. To address this, you must customize or disable the profile in /etc/apparmor.d/ usr.sbin.mysqld.

![](_page_51_Picture_14.jpeg)

### **Note**

On Debian platforms, the packaging scripts for MySQL uninstallation cannot currently handle mysqld@ instances. Before removing or upgrading the package, you must stop any extra instances manually first.

## <span id="page-51-0"></span>**Migrating from mysqld\_safe to systemd**

Because mysqld\_safe is not installed on platforms that use systemd to manage MySQL, options previously specified for that program (for example, in an [mysqld\_safe] or [safe\_mysqld] option group) must be specified another way:

• Some mysqld\_safe options are also understood by mysqld and can be moved from the [mysqld\_safe] or [safe\_mysqld] option group to the [mysqld] group. This does not include --pid-file, --open-files-limit, or --nice. To specify those options, use the override.conf systemd file, described previously.

![](_page_51_Picture_20.jpeg)

### **Note**

On systemd platforms, use of [mysqld\_safe] and [safe\_mysqld] option groups is not supported and may lead to unexpected behavior.

- For some mysqld\_safe options, there are alternative mysqld procedures. For example, the mysqld\_safe option for enabling syslog logging is --syslog, which is deprecated. To write error log output to the system log, use the instructions at Section 7.4.2.8, "Error Logging to the System Log".
- mysqld\_safe options not understood by mysqld can be specified in override.conf or environment variables. For example, with mysqld\_safe, if the server should use a specific memory allocation library, this is specified using the --malloc-lib option. For installations that manage the server with systemd, arrange to set the LD\_PRELOAD environment variable instead, as described previously.

# <span id="page-52-0"></span>**2.6 Installing MySQL Using Unbreakable Linux Network (ULN)**

Linux supports a number of different solutions for installing MySQL, covered in [Section 2.5,](#page-20-0) ["Installing MySQL on Linux".](#page-20-0) One of the methods, covered in this section, is installing from Oracle's Unbreakable Linux Network (ULN). You can find information about Oracle Linux and ULN under [http://](http://linux.oracle.com/) [linux.oracle.com/](http://linux.oracle.com/).

To use ULN, you need to obtain a ULN login and register the machine used for installation with ULN. This is described in detail in the [ULN FAQ](https://linux.oracle.com/uln_faq.md). The page also describes how to install and update packages.

Both Community and Commercial packages are supported, and each offers three MySQL channels:

- Server: MySQL Server
- Connectors: MySQL Connector/C++, MySQL Connector/J, MySQL Connector/ODBC, and MySQL Connector/Python.
- Tools: MySQL Router, MySQL Shell, and MySQL Workbench

The Community channels are available to all ULN users.

Accessing commercial MySQL ULN packages at oracle.linux.com requires you to provide a CSI with a valid commercial license for MySQL (Enterprise or Standard). As of this writing, valid purchases are 60944, 60945, 64911, and 64912. The appropriate CSI makes commercial MySQL subscription channels available in your ULN GUI interface.

Once MySQL has been installed using ULN, you can find information on starting and stopping the server, and more, at [Section 2.5.7, "Installing MySQL on Linux from the Native Software Repositories"](#page-44-0), particularly under [Section 2.5.4, "Installing MySQL on Linux Using RPM Packages from Oracle"](#page-26-1).

If you are changing your package source to use ULN and not changing which build of MySQL you are using, then back up your data, remove your existing binaries, and replace them with those from ULN. If a change of build is involved, we recommend the backup be a dump (mysqldump or mysqlpump or from [MySQL Shell's backup utility](https://dev.mysql.com/doc/mysql-shell/8.0/en/mysql-shell-utilities-dump-instance-schema.md)) just in case you need to rebuild your data after the new binaries are in place. If this shift to ULN crosses a version boundary, consult this section before proceeding: Chapter 3, [Upgrading MySQL](#page-110-0).

![](_page_52_Picture_12.jpeg)

### **Note**

Oracle Linux 8 is supported as of MySQL 8.0.17, and the community Tools and Connectors channels were added with the MySQL 8.0.24 release.