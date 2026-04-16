---
source: MySQL 8.0 Reference
title: 00_Overview
---

MySQL Server SELinux policy modules are typically installed by default. You can view installed modules using the semodule -l command. MySQL Server SELinux policy modules include:

- mysqld\_selinux
- mysqld\_safe\_selinux

For information about MySQL Server SELinux policy modules, refer to the SELinux manual pages. The manual pages provide information about types and Booleans associated with the MySQL service. Manual pages are named in the service-name\_selinux format.

```
man mysqld_selinux
```

If SELinux manual pages are not available, refer to your distribution's SELinux documentation for information about how to generate manual pages using the sepolicy manpage utility.

## <span id="page-189-0"></span>**8.7.4 SELinux File Context**

The MySQL Server reads from and writes to many files. If the SELinux context is not set correctly for these files, access to the files could be denied.

The instructions that follow use the semanage binary to manage file context; on RHEL, it's part of the policycoreutils-python-utils package:

```
yum install -y policycoreutils-python-utils
```

After installing the semanage binary, you can list MySQL file contexts using semanage with the fcontext option.

```
semanage fcontext -l | grep -i mysql
```

## **Setting the MySQL Data Directory Context**

The default data directory location is /var/lib/mysql/; and the SELinux context used is mysqld\_db\_t.

If you edit the configuration file to use a different location for the data directory, or for any of the files normally in the data directory (such as the binary logs), you may need to set the context for the new location. For example:

```
semanage fcontext -a -t mysqld_db_t "/path/to/my/custom/datadir(/.*)?"
restorecon -Rv /path/to/my/custom/datadir
semanage fcontext -a -t mysqld_db_t "/path/to/my/custom/logdir(/.*)?"
restorecon -Rv /path/to/my/custom/logdir
```

## **Setting the MySQL Error Log File Context**

The default location for RedHat RPMs is /var/log/mysqld.log; and the SELinux context type used is mysqld\_log\_t.

If you edit the configuration file to use a different location, you may need to set the context for the new location. For example:

```
semanage fcontext -a -t mysqld_log_t "/path/to/my/custom/error.log"
restorecon -Rv /path/to/my/custom/error.log
```

## **Setting the PID File Context**

The default location for the PID file is /var/run/mysqld/mysqld.pid; and the SELinux context type used is mysqld\_var\_run\_t.

If you edit the configuration file to use a different location, you may need to set the context for the new location. For example:

```
semanage fcontext -a -t mysqld_var_run_t "/path/to/my/custom/pidfile/directory/.*?"
restorecon -Rv /path/to/my/custom/pidfile/directory
```

## **Setting the Unix Domain Socket Context**

The default location for the Unix domain socket is /var/lib/mysql/mysql.sock; and the SELinux context type used is mysqld\_var\_run\_t.

If you edit the configuration file to use a different location, you may need to set the context for the new location. For example:

```
semanage fcontext -a -t mysqld_var_run_t "/path/to/my/custom/mysql\.sock"
restorecon -Rv /path/to/my/custom/mysql.sock
```

## **Setting the secure\_file\_priv Directory Context**

For MySQL versions since 5.6.34, 5.7.16, and 8.0.11.

Installing the MySQL Server RPM creates a /var/lib/mysql-files/ directory but does not set the SELinux context for it. The /var/lib/mysql-files/ directory is intended to be used for operations such as SELECT ... INTO OUTFILE.

If you enabled the use of this directory by setting secure\_file\_priv, you may need to set the context like so:

```
semanage fcontext -a -t mysqld_db_t "/var/lib/mysql-files/(/.*)?"
restorecon -Rv /var/lib/mysql-files
```

Edit this path if you used a different location. For security purposes, this directory should never be within the data directory.

For more information about this variable, see the secure\_file\_priv documentation.

## <span id="page-191-0"></span>**8.7.5 SELinux TCP Port Context**

The instructions that follow use the semanage binary to manage port context; on RHEL, it's part of the policycoreutils-python-utils package:

```
yum install -y policycoreutils-python-utils
```

After installing the semanage binary, you can list ports defined with the mysqld\_port\_t context using semanage with the port option.

```
$> semanage port -l | grep mysqld
mysqld_port_t tcp 1186, 3306, 63132-63164
```