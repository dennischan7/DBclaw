---
source: MySQL 8.4 Reference
title: 00_Overview
---

If Perl reports that it cannot find the ../mysql/mysql.so module, the problem is probably that Perl cannot locate the libmysqlclient.so shared library. You should be able to fix this problem by one of the following methods:

- Copy libmysqlclient.so to the directory where your other shared libraries are located (probably /usr/lib or /lib).
- Modify the -L options used to compile DBD::mysql to reflect the actual location of libmysqlclient.so.
- On Linux, you can add the path name of the directory where libmysqlclient.so is located to the /etc/ld.so.conf file.
- Add the path name of the directory where libmysqlclient.so is located to the LD\_RUN\_PATH environment variable. Some systems use LD\_LIBRARY\_PATH instead.

Note that you may also need to modify the -L options if there are other libraries that the linker fails to find. For example, if the linker cannot find libc because it is in /lib and the link command specifies - L/usr/lib, change the -L option to -L/lib or add -L/lib to the existing link command.

If you get the following errors from DBD::mysql, you are probably using gcc (or using an old binary compiled with gcc):

```
/usr/bin/perl: can't resolve symbol '__moddi3'
/usr/bin/perl: can't resolve symbol '__divdi3'
```

Add -L/usr/lib/gcc-lib/... -lgcc to the link command when the mysql.so library gets built (check the output from make for mysql.so when you compile the Perl client). The -L option should specify the path name of the directory where libgcc.a is located on your system.

Another cause of this problem may be that Perl and MySQL are not both compiled with gcc. In this case, you can solve the mismatch by compiling both with gcc.

# <span id="page-52-0"></span>Chapter 3 Upgrading MySQL

# **Table of Contents**

| 3.1 Before You Begin 223                                                    |     |
|-----------------------------------------------------------------------------|-----|
| 3.2 Upgrade Paths 224                                                       |     |
| 3.3 Upgrade Best Practices 225                                              |     |
| 3.4 What the MySQL Upgrade Process Upgrades 228                             |     |
| 3.5 Changes in MySQL 8.4 230                                                |     |
| 3.6 Preparing Your Installation for Upgrade 232                             |     |
| 3.7 Upgrading MySQL Binary or Package-based Installations on Unix/Linux 234 |     |
| 3.8 Upgrading MySQL with the MySQL Yum Repository 238                       |     |
| 3.9 Upgrading MySQL with the MySQL APT Repository 240                       |     |
| 3.10 Upgrading MySQL with the MySQL SLES Repository                         | 240 |
| 3.11 Upgrading MySQL on Windows 240                                         |     |
| 3.12 Upgrading a Docker Installation of MySQL 241                           |     |
| 3.13 Upgrade Troubleshooting 241                                            |     |
| 3.14 Rebuilding or Repairing Tables or Indexes 242                          |     |
| 3.15 Copying MySQL Databases to Another Machine 243                         |     |
|                                                                             |     |

This chapter describes the steps to upgrade a MySQL installation.

Upgrading is a common procedure, as you pick up bug fixes within the same MySQL release series or significant features between major MySQL releases. You perform this procedure first on some test systems to make sure everything works smoothly, and then on the production systems.

![](_page_52_Picture_5.jpeg)

### **Note**

In the following discussion, MySQL commands that must be run using a MySQL account with administrative privileges include -u root on the command line to specify the MySQL root user. Commands that require a password for root also include a -p option. Because -p is followed by no option value, such commands prompt for the password. Type the password when prompted and press Enter.

SQL statements can be executed using the [mysql](#page-182-0) command-line client (connect as root to ensure that you have the necessary privileges).

# <span id="page-52-1"></span>**3.1 Before You Begin**

Review the information in this section before upgrading. Perform any recommended actions.

- Understand what may occur during an upgrade. See [Section 3.4, "What the MySQL Upgrade](#page-57-0) [Process Upgrades".](#page-57-0)
- Protect your data by creating a backup. The backup should include the mysql system database, which contains the MySQL data dictionary tables and system tables. See Section 9.2, "Database Backup Methods".

![](_page_52_Picture_13.jpeg)

### **Important**

Downgrade from MySQL 8.4 to MySQL 8.3, or from a MySQL 8.4 release to a previous MySQL 8.4 release, is not supported. The only supported alternative is to restore a backup taken before upgrading. It is therefore imperative that you back up your data before starting the upgrade process.

• Review [Section 3.2, "Upgrade Paths"](#page-53-0) to ensure that your intended upgrade path is supported.

- Review [Section 3.5, "Changes in MySQL 8.4"](#page-59-0) for changes that you should be aware of before upgrading. Some changes may require action.
- Review Section 1.4, "What Is New in MySQL 8.4 since MySQL 8.0" for deprecated and removed features. An upgrade may require changes with respect to those features if you use any of them.
- Review Section 1.5, "Server and Status Variables and Options Added, Deprecated, or Removed in MySQL 8.4 since 8.0". If you use deprecated or removed variables, an upgrade may require configuration changes.
- Review the [Release Notes](https://dev.mysql.com/doc/relnotes/mysql/8.4/en/) for information about fixes, changes, and new features.
- If you use replication, review Section 19.5.3, "Upgrading or Downgrading a Replication Topology".
- Review [Section 3.3, "Upgrade Best Practices"](#page-54-0) and plan accordingly.
- Upgrade procedures vary by platform and how the initial installation was performed. Use the procedure that applies to your current MySQL installation:
  - For binary and package-based installations on non-Windows platforms, refer to [Section 3.7,](#page-63-0) ["Upgrading MySQL Binary or Package-based Installations on Unix/Linux".](#page-63-0)

![](_page_53_Picture_9.jpeg)

#### **Note**

For supported Linux distributions, the preferred method for upgrading package-based installations is to use the MySQL software repositories (MySQL Yum Repository, MySQL APT Repository, and MySQL SLES Repository).

- For installations on an Enterprise Linux platform or Fedora using the MySQL Yum Repository, refer to [Section 3.8, "Upgrading MySQL with the MySQL Yum Repository"](#page-67-0).
- For installations on Ubuntu using the MySQL APT repository, refer to [Section 3.9, "Upgrading](#page-69-0) [MySQL with the MySQL APT Repository".](#page-69-0)
- For installations on SLES using the MySQL SLES repository, refer to [Section 3.10, "Upgrading](#page-69-1) [MySQL with the MySQL SLES Repository".](#page-69-1)
- For installations performed using Docker, refer to [Section 3.12, "Upgrading a Docker Installation of](#page-70-0) [MySQL".](#page-70-0)
- For installations on Windows, refer to [Section 3.11, "Upgrading MySQL on Windows".](#page-69-2)
- If your MySQL installation contains a large amount of data that might take a long time to convert after an in-place upgrade, it may be useful to create a test instance for assessing the conversions that are required and the work involved to perform them. To create a test instance, make a copy of your MySQL instance that contains the mysql database and other databases without the data. Run the upgrade procedure on the test instance to assess the work involved to perform the actual data conversion.
- Rebuilding and reinstalling MySQL language interfaces is recommended when you install or upgrade to a new release of MySQL. This applies to MySQL interfaces such as PHP mysql extensions and the Perl DBD::mysql module.

# <span id="page-53-0"></span>**3.2 Upgrade Paths**

![](_page_53_Picture_20.jpeg)

### **Notes**

• Make sure you understand the MySQL release model for MySQL for MySQL long long-term support (LTS) and Innovation versions before proceeding with a downgrade.

- We recommend checking upgrade compatibility with MySQL Shell's [Upgrade](https://dev.mysql.com/doc/mysql-shell/8.4/en/mysql-shell-utilities-upgrade.md) [Checker Utility](https://dev.mysql.com/doc/mysql-shell/8.4/en/mysql-shell-utilities-upgrade.md) before performing an upgrade.
- A replication topology is upgraded by following the rolling upgrade scheme described at Section 19.5.3, "Upgrading or Downgrading a Replication Topology", which uses one of the supported single-server methods for each individual server upgrade.
- Monthly Rapid Updates (MRUs) and hot fixes also count as releases in this documentation.

**Table 3.1 Upgrade Paths for MySQL Server**

| Upgrade Path                                                                            | Path<br>Examples                                                                                       | Supported Upgrade Methods                                                                                                                         |
|-----------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------|
| Within an LTS or Bugfix series                                                          | 8.0.37 to<br>8.0.41 or<br>8.4.0 to 8.4.4                                                               | In-place upgrade, logical dump and load,<br>replication, and MySQL Clone                                                                          |
| From an LTS or Bugfix series to<br>the next LTS series                                  | 8.0.37 to 8.4.x<br>LTS                                                                                 | In-place upgrade, logical dump and load, and<br>replication                                                                                       |
| From an LTS or Bugfix release to<br>an Innovation release before the<br>next LTS series | 8.0.34 to 8.3.0<br>or 8.4.0 to<br>9.0.0                                                                | In-place upgrade, logical dump and load, and<br>replication                                                                                       |
| From an Innovation series to the<br>next LTS series                                     | 8.3.0 to 8.4<br>LTS                                                                                    | In-place upgrade, logical dump and load, and<br>replication                                                                                       |
| From an Innovation series to an<br>Innovation release after the next<br>LTS series      | Not allowed,<br>two steps<br>are required:<br>8.3.0 to 8.4<br>LTS, and 8.4<br>LTS to 9.x<br>Innovation | In-place upgrade, logical dump and load, and<br>replication                                                                                       |
| From within an Innovation series                                                        | 8.1.0 to 8.3.0                                                                                         | In-place upgrade, logical dump and load, and<br>replication                                                                                       |
| From MySQL 5.7 to an LTS or<br>Innovation release                                       | MySQL 5.7 to<br>8.4                                                                                    | A bugfix or LTS series cannot be skipped, so in<br>this example first upgrade MySQL 5.7 to MySQL<br>8.0, and then upgrade MySQL 8.0 to MySQL 8.4. |

# <span id="page-54-0"></span>**3.3 Upgrade Best Practices**

MySQL supports upgrading between minor versions (within an LTS series) and to the next major version (across an LTS series). Upgrading provides the latest features, performance, and security fixes.

To prepare and help ensure that your upgrade to the latest MySQL release is successful, we recommend the following best practices:

- [Decide on Major or Minor Version for Upgrade](#page-55-0)
- [Decide on Upgrade Type](#page-55-1)
- [Review Supported Platforms](#page-55-2)
- [Understand MySQL Server Changes](#page-55-3)
- [Run Upgrade Checker and Fix Incompatibilities](#page-55-4)

- [Run Applications in a Test Environment](#page-56-0)
- [Benchmark Applications and Workload Performance](#page-56-1)
- [Run Both MySQL Versions in Parallel](#page-56-2)
- [Run Final Test Upgrade](#page-56-3)
- [Check MySQL Backup](#page-56-4)
- [Upgrade Production Server](#page-56-5)
- [Enterprise Support](#page-56-6)

## <span id="page-55-0"></span>**Decide on Major or Minor Version for Upgrade**

The MySQL Release Model makes a distinction between LTS (Long Term Support) and Innovation Releases. LTS releases have 8+ years of support and are meant for production use. Innovation Releases provide users with the latest features and capabilities. Learn more about the MySQL Release Model.

Performing a minor version upgrade is straightforward while major version upgrades require strategic planning and additional testing before the upgrade. This guide is especially useful for major version upgrades.

## <span id="page-55-1"></span>**Decide on Upgrade Type**

There are three main ways to upgrade MySQL; read the associated documentation to determine which type of upgrade is best suited for your situation.

- [An in-place upgrade](#page-64-0): replacing the MySQL Server packages.
- [A logical upgrade](#page-65-0): exporting SQL from the old MySQL instance to the new.
- A replication topology upgrade: account for each server's topology role.

# <span id="page-55-2"></span>**Review Supported Platforms**

If your current operating system is not supported by the new version of MySQL, then plan to upgrade the operating system as otherwise an in-place upgrade is not supported.

For a current list of supported platforms, see: [https://www.mysql.com/support/supportedplatforms/](https://www.mysql.com/support/supportedplatforms/database.md) [database.html](https://www.mysql.com/support/supportedplatforms/database.md)

# <span id="page-55-3"></span>**Understand MySQL Server Changes**

Each major version comes with new features, changes in behavior, deprecations, and removals. It is important to understand the impact of each of these to existing applications.

See: [Section 3.5, "Changes in MySQL 8.4".](#page-59-0)

# <span id="page-55-4"></span>**Run Upgrade Checker and Fix Incompatibilities**

MySQL Shell's [Upgrade Checker Utility](https://dev.mysql.com/doc/mysql-shell/8.4/en/mysql-shell-utilities-upgrade.md) detects incompatibilities between database versions that must be addressed before performing the upgrade. The util.checkForServerUpgrade() function verifies that MySQL server instances are ready to upgrade. Connect to the existing MySQL server and select the MySQL Server version you plan to upgrade to for the utility to report issues to address prior to an upgrade. These include incompatibilities in data types, storage engines, and so on.

You are ready to upgrade when the upgrade checking utility no longer reports any issues.

## <span id="page-56-0"></span>**Run Applications in a Test Environment**

After completing the upgrade checker's requirements, next test your applications on the new target MySQL server. Check for errors and warnings in the MySQL error log and application logs.

## <span id="page-56-1"></span>**Benchmark Applications and Workload Performance**

We recommend benchmarking your own applications and workloads by comparing how they perform using the previous and new versions of MySQL. Usually, newer MySQL versions add features and improve performance but there are cases where an upgrade might run slower for specific queries. Possible issues resulting in performance regressions:

- Prior server configuration is not optimal for newer version
- Changes to data types
- Additional storage required by Multi-byte character set support
- Storage engines changes
- Dropped or changed indexes
- Stronger encryption
- Stronger authentication
- SQL optimizer changes
- Newer version of MySQL require additional memory
- Physical or Virtual Hardware is slower compute or storage

For related information and potential mitigation techniques, see [Valid Performance Regressions](https://dev.mysql.com/doc/refman/8.0/en/upgrading-from-previous-series.md#upgrade-performance-regressions).

# <span id="page-56-2"></span>**Run Both MySQL Versions in Parallel**

To minimize risk, it is best keep the current system running while running the upgraded system in parallel.

# <span id="page-56-3"></span>**Run Final Test Upgrade**

Practice and do a run though prior to upgrading your production server. Thoroughly test the upgrade procedures before upgrading a production system.

# <span id="page-56-4"></span>**Check MySQL Backup**

Check that the full backup exists and is viable before performing the upgrade.

# <span id="page-56-5"></span>**Upgrade Production Server**

You are ready to complete the upgrade.

# <span id="page-56-6"></span>**Enterprise Support**

If you're a MySQL Enterprise Edition customer, you can also contact the MySQL Support Team experts with any questions you may have.

# <span id="page-57-0"></span>**3.4 What the MySQL Upgrade Process Upgrades**

Installing a new version of MySQL may require upgrading these parts of the existing installation:

- The mysql system schema, which contains tables that store information required by the MySQL server as it runs (see Section 7.3, "The mysql System Schema"). mysql schema tables fall into two broad categories:
  - Data dictionary tables, which store database object metadata.
  - System tables (that is, the remaining non-data dictionary tables), which are used for other operational purposes.
- Other schemas, some of which are built in and may be considered "owned" by the server, and others which are not:
  - The performance\_schema, INFORMATION\_SCHEMA, ndbinfo, and sys schemas.
  - User schemas.

Two distinct version numbers are associated with parts of the installation that may require upgrading:

- The data dictionary version. This applies to the data dictionary tables.
- The server version, also known as the MySQL version. This applies to the system tables and objects in other schemas.

In both cases, the actual version applicable to the existing MySQL installation is stored in the data dictionary, and the current expected version is compiled into the new version of MySQL. When an actual version is lower than the current expected version, those parts of the installation associated with that version must be upgraded to the current version. If both versions indicate an upgrade is needed, the data dictionary upgrade must occur first.

As a reflection of the two distinct versions just mentioned, the upgrade occurs in two steps:

• Step 1: Data dictionary upgrade.

This step upgrades:

- The data dictionary tables in the mysql schema. If the actual data dictionary version is lower than the current expected version, the server creates data dictionary tables with updated definitions, copies persisted metadata to the new tables, atomically replaces the old tables with the new ones, and reinitializes the data dictionary.
- The Performance Schema, INFORMATION\_SCHEMA, and ndbinfo.
- Step 2: Server upgrade.

This step comprises all other upgrade tasks. If the server version of the existing MySQL installation is lower than that of the new installed MySQL version, everything else must be upgraded:

- The system tables in the mysql schema (the remaining non-data dictionary tables).
- The sys schema.
- User schemas.

The data dictionary upgrade (step 1) is the responsibility of the server, which performs this task as necessary at startup unless invoked with an option that prevents it from doing so. The option is - upgrade=NONE.

If the data dictionary is out of date but the server is prevented from upgrading it, the server does not run, and exits with an error instead. For example:

```
[ERROR] [MY-013381] [Server] Server shutting down because upgrade is
required, yet prohibited by the command line option '--upgrade=NONE'.
[ERROR] [MY-010334] [Server] Failed to initialize DD Storage Engine
[ERROR] [MY-010020] [Server] Data Dictionary initialization failed.
```

The --upgrade server option controls whether and how the server performs an automatic upgrade at startup:

- With no option or with --upgrade=AUTO, the server upgrades anything it determines to be out of date (steps 1 and 2).
- With --upgrade=NONE, the server upgrades nothing (skips steps 1 and 2), but also exits with an error if the data dictionary must be upgraded. It is not possible to run the server with an out-of-date data dictionary; the server insists on either upgrading it or exiting.
- With --upgrade=MINIMAL, the server upgrades the data dictionary, the Performance Schema, and the INFORMATION\_SCHEMA, if necessary (step 1). Note that following an upgrade with this option, Group Replication cannot be started, because system tables on which the replication internals depend are not updated, and reduced functionality might also be apparent in other areas.
- With --upgrade=FORCE, the server upgrades the data dictionary, the Performance Schema, and the INFORMATION\_SCHEMA, if necessary (step 1), and forces an upgrade of everything else (step 2). Expect server startup to take longer with this option because the server checks all objects in all schemas.

FORCE is useful to force step 2 actions to be performed if the server thinks they are not necessary. One way that FORCE differs from AUTO is that with FORCE, the server re-creates system tables such as help tables or time zone tables if they are missing.

Additional notes about what occurs during upgrade step 2:

• Step 2 installs the sys schema if it is not installed, and upgrades it to the current version otherwise. An error occurs if a sys schema exists but has no version view, on the assumption that its absence indicates a user-created schema:

```
A sys schema exists with no sys.version view. If
you have a user created sys schema, this must be renamed for the
upgrade to succeed.
```

To upgrade in this case, remove or rename the existing sys schema first. Then perform the upgrade procedure again. (It may be necessary to force step 2.)

To prevent the sys schema check, start the server with the --upgrade=NONE or - upgrade=MINIMAL option.

- Step 2 upgrades the system tables to ensure that they have the current structure, and this includes the help tables but not the time zone tables. The procedure for loading time zone tables is platform dependent and requires decision making by the DBA, so it cannot be done automatically.
- When Step 2 is upgrading the system tables in the mysql schema, the column order in the primary key of the mysql.db, mysql.tables\_priv, mysql.columns\_priv and mysql.procs\_priv tables is changed to place the host name and user name columns together. Placing the host name and user name together means that index lookup can be used, which improves performance for CREATE USER, DROP USER, and RENAME USER statements, and for ACL checks for multiple users with multiple privileges. Dropping and re-creating the index is necessary and might take some time if the system has a large number of users and privileges.
- Step 2 processes all tables in all user schemas as necessary. Table checking might take a long time to complete. Each table is locked and therefore unavailable to other sessions while it is being processed. Check and repair operations can be time-consuming, particularly for large tables. Table checking uses the FOR UPGRADE option of the CHECK TABLE statement. For details about what this option entails, see Section 15.7.3.2, "CHECK TABLE Statement".

To prevent table checking, start the server with the --upgrade=NONE or --upgrade=MINIMAL option.

To force table checking, start the server with the --upgrade=FORCE option.

• Step 2 marks all checked and repaired tables with the current MySQL version number. This ensures that the next time upgrade checking occurs with the same version of the server, it can be determined whether there is any need to check or repair a given table again.

# <span id="page-59-0"></span>**3.5 Changes in MySQL 8.4**

Before upgrading to MySQL 8.4, review the changes described in the following sections to identify those that apply to your current MySQL installation and applications.

- [Incompatible Changes in MySQL 8.4](#page-59-1)
- [Changed Server Defaults](#page-60-0)

In addition, you can consult the resources listed here:

- Section 1.4, "What Is New in MySQL 8.4 since MySQL 8.0"
- [MySQL 8.4 Release Notes](https://dev.mysql.com/doc/relnotes/mysql/8.4/en/)

## <span id="page-59-1"></span>**Incompatible Changes in MySQL 8.4**

This section contains information about incompatible changes in MySQL 8.4.

• **Spatial indexes.** When upgrading to MySQL 8.4.4 or later, it is recommended that you drop any spatial indexes beforehand, then re-create them after the upgrade is complete. Alternatively, you can drop and re-create such indexes immediately following the upgrade, but before making use of any of the tables in which they occur.

For more information, see Section 13.4.10, "Creating Spatial Indexes".

- **WAIT\_UNTIL\_SQL\_THREAD\_AFTER\_GTIDS() function removed.** The WAIT\_UNTIL\_SQL\_THREAD\_AFTER\_GTIDS() SQL function, deprecated in MySQL 8.0 has been removed; attempting to invoke it now causes a syntax error. Use WAIT\_FOR\_EXECUTED\_GTID\_SET() instead.
- **authentication\_fido and authentication\_fido\_client no longer available on some platforms.** Due to upgrading the libfido2 library bundled with the server to version 1.13.0, which requires OpenSSL 1.1.1 or higher, the authentication\_fido and authentication\_fido\_client authentication plugins are no longer available on Enterprise Linux 6, Enterprise Linux 7, Solaris 11, or SUSE Enterprise Linux 12.
- **NULL disallowed for command-line options.** Setting server variables equal to SQL NULL on the command line is not supported. In MySQL 8.4, setting any of these to NULL is specifically disallowed, and attempting to do is rejected with an error.

```
The following variables are excepted from this restriction: admin_ssl_ca, admin_ssl_capath,
admin_ssl_cert, admin_ssl_cipher, admin_tls_ciphersuites, admin_ssl_key,
admin_ssl_crl, admin_ssl_crlpath, basedir, character_sets_dir,
ft_stopword_file, group_replication_recovery_tls_ciphersuites,
init_file, lc_messages_dir, plugin_dir, relay_log, relay_log_info_file,
replica_load_tmpdir, ssl_ca, ssl_capath, ssl_cert, ssl_cipher, ssl_crl,
ssl_crlpath, ssl_key, socket, tls_ciphersuites, and tmpdir.
```

See also Section 7.1.8, "Server System Variables".

For additional information about changes in MySQL 8.4, see Section 1.4, "What Is New in MySQL 8.4 since MySQL 8.0".

## <span id="page-60-0"></span>**Changed Server Defaults**

This section contains information about MySQL server system variables whose default values have changed in MySQL 8.4 as compared to MySQL 8.0.

| System Variable                                                                | Old Default                             | New Default                                                                                                                                                  |  |
|--------------------------------------------------------------------------------|-----------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------|--|
| InnoDB changes                                                                 |                                         |                                                                                                                                                              |  |
| innodb_adaptive_hash_indexON                                                   |                                         | OFF                                                                                                                                                          |  |
| innodb_buffer_pool_in_core_file ON                                             |                                         | OFF                                                                                                                                                          |  |
| innodb_buffer_pool_instances innodb_buffer_pool_size <<br>1GB: 1; otherwise: 8 |                                         | innodb_buffer_pool_size<br><= 1GB: 1; otherwise:<br>MIN( 0.5 *<br>(innodb_buffer_pool_size<br>/<br>innodb_buffer_pool_chunk_size),<br>0.25 * number_of_cpus) |  |
| innodb_change_buffering                                                        | all                                     | none                                                                                                                                                         |  |
| innodb_doublewrite_files                                                       | innodb_buffer_pool_instances<br>* 2     | 2                                                                                                                                                            |  |
| innodb_doublewrite_pages                                                       | Value of<br>innodb_write_io_threads     | 128                                                                                                                                                          |  |
| innodb_flush_method                                                            | fsync                                   | O_DIRECT if supported,<br>otherwise fsync                                                                                                                    |  |
| innodb_io_capacity                                                             | 200                                     | 10000                                                                                                                                                        |  |
| innodb_io_capacity_max                                                         | MIN(2 *<br>innodb_io_capacity,<br>2000) |                                                                                                                                                              |  |
| innodb_log_buffer_size                                                         | 16777216                                | 67108864                                                                                                                                                     |  |
| innodb_numa_interleave                                                         | OFF                                     | ON                                                                                                                                                           |  |
| innodb_page_cleaners                                                           | 4                                       | Value of<br>innodb_buffer_pool_instances                                                                                                                     |  |
| innodb_parallel_read_threads 4                                                 |                                         | MIN(number_of_cpus / 8,<br>4)                                                                                                                                |  |
| innodb_purge_threads                                                           | 4                                       | If number_of_cpus <= 16: 1;<br>otherwise: 4                                                                                                                  |  |
| innodb_use_fdatasync                                                           | OFF                                     | ON                                                                                                                                                           |  |
| Group Replication changes                                                      |                                         |                                                                                                                                                              |  |
| group_replication_consistency EVENTUAL                                         |                                         | BEFORE_ON_PRIMARY_FAILOVER                                                                                                                                   |  |
| group_replication_exit_state_action                                            | READ_ONLY                               | OFFLINE_MODE                                                                                                                                                 |  |
| Temporary table changes                                                        |                                         |                                                                                                                                                              |  |
| temptable_max_mmap                                                             | 1073741824                              | 0                                                                                                                                                            |  |
| temptable_max_ram                                                              | 1073741824                              |                                                                                                                                                              |  |
| temptable_use_mmap                                                             | ON                                      | OFF                                                                                                                                                          |  |
|                                                                                |                                         |                                                                                                                                                              |  |

For more information about options or variables which have been added, see [Option and Variable](https://dev.mysql.com/doc/mysqld-version-reference/en/optvar-changes-8-4.md) [Changes for MySQL 8.4](https://dev.mysql.com/doc/mysqld-version-reference/en/optvar-changes-8-4.md), in the MySQL Server Version Reference.

Although the new defaults are the best configuration choices for most use cases, there are special cases, as well as legacy reasons for using existing configuration choices. For example, some people prefer to upgrade to MySQL 8.4 with as few changes to their applications or operational environment as possible. We recommend to evaluate all the new defaults and use as many as you can.

The Performance Schema variables\_info table shows, for each system variable, the source from which it was most recently set, as well as its range of values. This provides SQL access to all there is to know about a system variable and its values.

# <span id="page-61-0"></span>**3.6 Preparing Your Installation for Upgrade**

Before upgrading to the latest MySQL 8.4 release, ensure the upgrade readiness of your current MySQL 8.0 or MySQL 8.4 server instance by performing the preliminary checks described below. The upgrade process may fail otherwise.

![](_page_61_Picture_5.jpeg)

#### **Tip**

Consider using the [MySQL Shell upgrade checker utility](https://dev.mysql.com/doc/mysql-shell/8.4/en/mysql-shell-utilities-upgrade.md) that enables you to verify whether MySQL server instances are ready for upgrade. You can select a target MySQL Server release to which you plan to upgrade, ranging from the MySQL Server 8.0.11 up to the MySQL Server release number that matches the current MySQL Shell release number. The upgrade checker utility carries out the automated checks that are relevant for the specified target release, and advises you of further relevant checks that you should make manually. The upgrade checker works for all Bugfix, Innovation, and LTS releases of MySQL. Installation instructions for MySQL Shell can be found [here](https://dev.mysql.com/doc/mysql-shell/8.4/en/mysql-shell-install.md).

#### Preliminary checks:

- 1. The following issues must not be present:
  - There must be no tables that use obsolete data types or functions.
  - There must be no orphan .frm files.
  - Triggers must not have a missing or empty definer or an invalid creation context (indicated by the character\_set\_client, collation\_connection, Database Collation attributes displayed by SHOW TRIGGERS or the INFORMATION\_SCHEMA TRIGGERS table). Any such triggers must be dumped and restored to fix the issue.

To check for these issues, execute this command:

```
mysqlcheck -u root -p --all-databases --check-upgrade
```

If mysqlcheck reports any errors, correct the issues.

2. There must be no partitioned tables that use a storage engine that does not have native partitioning support. To identify such tables, execute this query:

```
SELECT TABLE_SCHEMA, TABLE_NAME
 FROM INFORMATION_SCHEMA.TABLES
 WHERE ENGINE NOT IN ('innodb', 'ndbcluster')
 AND CREATE_OPTIONS LIKE '%partitioned%';
```

Any table reported by the query must be altered to use InnoDB or be made nonpartitioned. To change a table storage engine to InnoDB, execute this statement:

```
ALTER TABLE table_name ENGINE = INNODB;
```

For information about converting MyISAM tables to InnoDB, see Section 17.6.1.5, "Converting Tables from MyISAM to InnoDB".

To make a partitioned table nonpartitioned, execute this statement:

```
ALTER TABLE table_name REMOVE PARTITIONING;
```

- 3. Some keywords may be reserved in MySQL 8.4 that were not reserved previously. See Section 11.3, "Keywords and Reserved Words". This can cause words previously used as identifiers to become illegal. To fix affected statements, use identifier quoting. See Section 11.2, "Schema Object Names".
- 4. There must be no tables in the MySQL 8.3 mysql system database that have the same name as a table used by the MySQL 8.4 data dictionary. To identify tables with those names, execute this query:

```
SELECT TABLE_SCHEMA, TABLE_NAME
FROM INFORMATION_SCHEMA.TABLES
WHERE 
 LOWER(TABLE_SCHEMA) = 'mysql'
 AND 
 LOWER(TABLE_NAME) IN
 (
 'catalogs',
 'character_sets',
 'check_constraints',
 'collations',
 'column_statistics',
 'column_type_elements',
 'columns',
 'dd_properties',
 'events',
 'foreign_key_column_usage',
 'foreign_keys',
 'index_column_usage',
 'index_partitions',
 'index_stats',
 'indexes',
 'parameter_type_elements',
 'parameters',
 'resource_groups',
 'routines',
 'schemata',
 'st_spatial_reference_systems',
 'table_partition_values',
 'table_partitions',
 'table_stats',
 'tables',
 'tablespace_files',
 'tablespaces',
 'triggers',
 'view_routine_usage',
 'view_table_usage'
 );
```

Any tables reported by the query must be dropped or renamed (use RENAME TABLE). This may also entail changes to applications that use the affected tables.

5. There must be no tables that have foreign key constraint names longer than 64 characters. Use this query to identify tables with constraint names that are too long:

```
SELECT TABLE_SCHEMA, TABLE_NAME
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME IN
 (SELECT LEFT(SUBSTR(ID,INSTR(ID,'/')+1),
 INSTR(SUBSTR(ID,INSTR(ID,'/')+1),'_ibfk_')-1)
 FROM INFORMATION_SCHEMA.INNODB_SYS_FOREIGN
 WHERE LENGTH(SUBSTR(ID,INSTR(ID,'/')+1))>64);
```

For a table with a constraint name that exceeds 64 characters, drop the constraint and add it back with constraint name that does not exceed 64 characters (use ALTER TABLE).

- 6. There must be no obsolete SQL modes defined by sql\_mode system variable. Attempting to use an obsolete SQL mode prevents MySQL 8.4 from starting. Applications that use obsolete SQL modes should be revised to avoid them. For information about SQL modes removed in MySQL 8.4, see [Server Changes](https://dev.mysql.com/doc/refman/8.0/en/upgrading-from-previous-series.md#upgrade-server-changes).
- 7. Only upgrade a MySQL server instance that was properly shut down. If the instance unexpectedly shutdown, then restart the instance and shut it down with innodb\_fast\_shutdown=0 before upgrade.
- 8. There must be no views with explicitly defined columns names that exceed 64 characters (views with column names up to 255 characters were permitted in MySQL 5.7). To avoid upgrade errors, such views should be altered before upgrading. Currently, the only method of identify views with column names that exceed 64 characters is to inspect the view definition using SHOW CREATE VIEW. You can also inspect view definitions by querying the Information Schema VIEWS table.
- 9. There must be no tables or stored procedures with individual ENUM or SET column elements that exceed 255 characters or 1020 bytes in length. Prior to MySQL 8.4, the maximum combined length of ENUM or SET column elements was 64K. In MySQL 8.4, the maximum character length of an individual ENUM or SET column element is 255 characters, and the maximum byte length is 1020 bytes. (The 1020 byte limit supports multibyte character sets). Before upgrading to MySQL 8.0, modify any ENUM or SET column elements that exceed the new limits. Failing to do so causes the upgrade to fail with an error.
- 10. Your MySQL 8.3 installation must not use features that are not supported by MySQL 8.4. Any changes here are necessarily installation specific, but the following example illustrates the kind of thing to look for:

Some server startup options and system variables have been removed in MySQL 8.4. See Features Removed in MySQL 8.4, and Section 1.5, "Server and Status Variables and Options Added, Deprecated, or Removed in MySQL 8.4 since 8.0". If you use any of these, an upgrade requires configuration changes.

11. If you intend to change the lower\_case\_table\_names setting to 1 at upgrade time, ensure that schema and table names are lowercase before upgrading. Otherwise, a failure could occur due to a schema or table name lettercase mismatch. You can use the following queries to check for schema and table names containing uppercase characters:

```
mysql> select TABLE_NAME, if(sha(TABLE_NAME) !=sha(lower(TABLE_NAME)),'Yes','No') as UpperCase from information_schema.tables;
```

If lower\_case\_table\_names=1, table and schema names are checked by the upgrade process to ensure that all characters are lowercase. If table or schema names are found to contain uppercase characters, the upgrade process fails with an error.

![](_page_63_Picture_10.jpeg)

#### **Note**

Changing the lower\_case\_table\_names setting at upgrade time is not recommended.

If upgrade to MySQL 8.4 fails due to any of the issues outlined above, the server reverts all changes to the data directory. In this case, remove all redo log files and restart the MySQL 8.3 server on the existing data directory to address the errors. The redo log files (ib\_logfile\*) reside in the MySQL data directory by default. After the errors are fixed, perform a slow shutdown (by setting innodb\_fast\_shutdown=0) before attempting the upgrade again.

# <span id="page-63-0"></span>**3.7 Upgrading MySQL Binary or Package-based Installations on Unix/Linux**

This section describes how to upgrade MySQL binary and package-based installations on Unix/Linux. In-place and logical upgrade methods are described.

- [In-Place Upgrade](#page-64-0)
- [Logical Upgrade](#page-65-0)
- [MySQL Cluster Upgrade](#page-67-1)

## <span id="page-64-0"></span>**In-Place Upgrade**

An in-place upgrade involves shutting down the old MySQL server, replacing the old MySQL binaries or packages with the new ones, restarting MySQL on the existing data directory, and upgrading any remaining parts of the existing installation that require upgrading. For details about what may need upgrading, see [Section 3.4, "What the MySQL Upgrade Process Upgrades"](#page-57-0).

![](_page_64_Picture_6.jpeg)

### **Note**

If you are upgrading an installation originally produced by installing multiple RPM packages, upgrade all the packages, not just some. For example, if you previously installed the server and client RPMs, do not upgrade just the server RPM.

For some Linux platforms, MySQL installation from RPM or Debian packages includes systemd support for managing MySQL server startup and shutdown. On these platforms, [mysqld\\_safe](#page-158-1) is not installed. In such cases, use systemd for server startup and shutdown instead of the methods used in the following instructions. See Section 2.5.9, "Managing MySQL Server with systemd".

For upgrades to MySQL Cluster installations, see also [MySQL Cluster Upgrade.](#page-67-1)

To perform an in-place upgrade:

- 1. Review the information in [Section 3.1, "Before You Begin".](#page-52-1)
- 2. Ensure the upgrade readiness of your installation by completing the preliminary checks in [Section 3.6, "Preparing Your Installation for Upgrade".](#page-61-0)
- 3. If you use XA transactions with InnoDB, run XA RECOVER before upgrading to check for uncommitted XA transactions. If results are returned, either commit or rollback the XA transactions by issuing an XA COMMIT or XA ROLLBACK statement.
- 4. If you normally run your MySQL server configured with innodb\_fast\_shutdown set to 2 (cold shutdown), configure it to perform a fast or slow shutdown by executing either of these statements:

```
SET GLOBAL innodb_fast_shutdown = 1; -- fast shutdown
SET GLOBAL innodb_fast_shutdown = 0; -- slow shutdown
```

With a fast or slow shutdown, InnoDB leaves its undo logs and data files in a state that can be dealt with in case of file format differences between releases.

5. Shut down the old MySQL server. For example:

```
mysqladmin -u root -p shutdown
```

- 6. Upgrade the MySQL binaries or packages. If upgrading a binary installation, unpack the new MySQL binary distribution package. See Obtain and Unpack the Distribution. For package-based installations, install the new packages.
- 7. Start the MySQL 8.4 server, using the existing data directory. For example:

```
mysqld_safe --user=mysql --datadir=/path/to/existing-datadir &
```

If there are encrypted InnoDB tablespaces, use the --early-plugin-load option to load the keyring plugin.

When you start the MySQL 8.4 server, it automatically detects whether data dictionary tables are present. If not, the server creates them in the data directory, populates them with metadata, and then proceeds with its normal startup sequence. During this process, the server upgrades metadata for all database objects, including databases, tablespaces, system and user tables, views, and stored programs (stored procedures and functions, triggers, and Event Scheduler events). The server also removes files that previously were used for metadata storage. For example, after upgrading from MySQL 8.3 to MySQL 8.4, you may notice that tables no longer have .frm files.

If this step fails, the server reverts all changes to the data directory. In this case, you should remove all redo log files, start your MySQL 8.3 server on the same data directory, and fix the cause of any errors. Then perform another slow shutdown of the 8.3 server and start the MySQL 8.4 server to try again.

8. In the previous step, the server upgrades the data dictionary as necessary, making any changes required in the mysql system database between MySQL 8.3 and MySQL 8.4, so that you can take advantage of new privileges or capabilities. It also brings the Performance Schema, INFORMATION\_SCHEMA, and sys databases up to date for MySQL 8.4, and examines all user databases for incompatibilities with the current version of MySQL.

![](_page_65_Picture_4.jpeg)

#### **Note**

The upgrade process does not upgrade the contents of the time zone tables. For upgrade instructions, see Section 7.1.15, "MySQL Server Time Zone Support".

## <span id="page-65-0"></span>**Logical Upgrade**

A logical upgrade involves exporting SQL from the old MySQL instance using a backup or export utility such as mysqldump, installing the new MySQL server, and applying the SQL to your new MySQL instance. For details about what may need upgrading, see [Section 3.4, "What the MySQL Upgrade](#page-57-0) [Process Upgrades".](#page-57-0)

![](_page_65_Picture_9.jpeg)

#### **Note**

For some Linux platforms, MySQL installation from RPM or Debian packages includes systemd support for managing MySQL server startup and shutdown. On these platforms, [mysqld\\_safe](#page-158-1) is not installed. In such cases, use systemd for server startup and shutdown instead of the methods used in the following instructions. See Section 2.5.9, "Managing MySQL Server with systemd".

![](_page_65_Picture_12.jpeg)

#### **Warning**

Applying SQL extracted from a previous MySQL release to a new MySQL release may result in errors due to incompatibilities introduced by new, changed, deprecated, or removed features and capabilities. Consequently, SQL extracted from a previous MySQL release may require modification to enable a logical upgrade.

To identify incompatibilities before upgrading to the latest MySQL 8.4 release, perform the steps described in [Section 3.6, "Preparing Your Installation for](#page-61-0) [Upgrade".](#page-61-0)

To perform a logical upgrade:

- 1. Review the information in [Section 3.1, "Before You Begin".](#page-52-1)
- 2. Export your existing data from the previous MySQL installation:

mysqldump -u root -p

```
 --add-drop-table --routines --events
 --all-databases --force > data-for-upgrade.sql
```

![](_page_66_Picture_2.jpeg)

### **Note**

Use the --routines and --events options with mysqldump (as shown above) if your databases include stored programs. The --all-databases option includes all databases in the dump, including the mysql database that holds the system tables.

![](_page_66_Picture_5.jpeg)

### **Important**

If you have tables that contain generated columns, use the mysqldump utility provided with MySQL 5.7.9 or higher to create your dump files. The mysqldump utility provided in earlier releases uses incorrect syntax for generated column definitions (Bug #20769542). You can use the Information Schema COLUMNS table to identify tables with generated columns.

3. Shut down the old MySQL server. For example:

```
mysqladmin -u root -p shutdown
```

- 4. Install MySQL 8.4. For installation instructions, see Chapter 2, Installing MySQL.
- 5. Initialize a new data directory, as described in [Section 2.9.1, "Initializing the Data Directory"](#page-36-0). For example:

```
mysqld --initialize --datadir=/path/to/8.4-datadir
```

Copy the temporary 'root'@'localhost' password displayed to your screen or written to your error log for later use.

6. Start the MySQL 8.4 server, using the new data directory. For example:

```
mysqld_safe --user=mysql --datadir=/path/to/8.4-datadir &
```

7. Reset the root password:

```
$> mysql -u root -p
Enter password: **** <- enter temporary root password
mysql> ALTER USER USER() IDENTIFIED BY 'your new password';
```

8. Load the previously created dump file into the new MySQL server. For example:

```
mysql -u root -p --force < data-for-upgrade.sql
```

![](_page_66_Picture_20.jpeg)

#### **Note**

It is not recommended to load a dump file when GTIDs are enabled on the server (gtid\_mode=ON), if your dump file includes system tables. mysqldump issues DML instructions for the system tables which use the non-transactional MyISAM storage engine, and this combination is not permitted when GTIDs are enabled. Also be aware that loading a dump file from a server with GTIDs enabled, into another server with GTIDs enabled, causes different transaction identifiers to be generated.

9. Perform any remaining upgrade operations:

Shut down the server, then restart it with the --upgrade=FORCE option to perform the remaining upgrade tasks:

```
mysqladmin -u root -p shutdown
```

mysqld\_safe --user=mysql --datadir=/path/to/8.4-datadir --upgrade=FORCE &

Upon restart with --upgrade=FORCE, the server makes any changes required in the mysql system schema between MySQL 8.3 and MySQL 8.4, so that you can take advantage of new privileges or capabilities. It also brings the Performance Schema, INFORMATION\_SCHEMA, and sys schema up to date for MySQL 8.4, and examines all user schemas for incompatibilities with the current version of MySQL.

![](_page_67_Picture_3.jpeg)

#### **Note**

The upgrade process does not upgrade the contents of the time zone tables. For upgrade instructions, see Section 7.1.15, "MySQL Server Time Zone Support".

# <span id="page-67-1"></span>**MySQL Cluster Upgrade**

The information in this section is an adjunct to the in-place upgrade procedure described in [In-Place](#page-64-0) [Upgrade](#page-64-0), for use if you are upgrading MySQL Cluster.

A MySQL Cluster upgrade can be performed as a regular rolling upgrade, following the usual three ordered steps:

- 1. Upgrade MGM nodes.
- 2. Upgrade data nodes one at a time.
- 3. Upgrade API nodes one at a time (including MySQL servers).

There are two steps to upgrading each individual mysqld:

1. Import the data dictionary.

Start the new server with the --upgrade=MINIMAL option to upgrade the data dictionary but not the system tables.

The MySQL server must be connected to NDB for this phase to complete. If any NDB or NDBINFO tables exist, and the server cannot connect to the cluster, it exits with an error message:

Failed to Populate DD tables.

2. Upgrade the system tables by restarting each individual [mysqld](#page-158-0) without the --upgrade=MINIMAL option.

# <span id="page-67-0"></span>**3.8 Upgrading MySQL with the MySQL Yum Repository**

For supported Yum-based platforms (see Section 2.5.1, "Installing MySQL on Linux Using the MySQL Yum Repository", for a list), you can perform an in-place upgrade for MySQL (that is, replacing the old version and then running the new version using the old data files) with the MySQL Yum repository.

![](_page_67_Picture_20.jpeg)

### **Notes**

- An innovation series, such as MySQL 9.6, is in a separate track than an LTS series, such as MySQL 8.4. The LTS series is active by default.
- Before performing any update to MySQL, follow carefully the instructions in Chapter 3, [Upgrading MySQL](#page-52-0). Among other instructions discussed there, it is especially important to back up your database before the update.
- The following instructions assume you have installed MySQL with the MySQL Yum repository or with an RPM package directly downloaded from [MySQL](https://dev.mysql.com/downloads/)

![](_page_68_Picture_1.jpeg)

[Developer Zone's MySQL Download page;](https://dev.mysql.com/downloads/) if that is not the case, following the instructions in Replacing a Native Third-Party Distribution of MySQL.

# **Selecting a Target Series** 1.

By default, the MySQL Yum repository updates MySQL to the latest version in the release track you have chosen during installation (see Selecting a Release Series for details), which means, for example, a 8.0.x installation is not updated to a 8.4.x release automatically. To update to another release series, you must first disable the subrepository for the series that has been selected (by default, or by yourself) and enable the subrepository for your target series. To do that, see the general instructions given in Selecting a Release Series for editing the subrepository entries in the /etc/yum.repos.d/mysql-community.repo file.

As a general rule, to upgrade from one bugfix series to another, go to the next bugfix series rather than skipping a bugfix series. For example, if you are currently running MySQL 5.7 and wish to upgrade to MySQL 8.4, upgrade to MySQL 8.0 first before upgrading to MySQL 8.4. For additional details, see [Section 3.5, "Changes in MySQL 8.4".](#page-59-0)

- For important information about upgrading from MySQL 5.7 to 8.0, see [Upgrading from MySQL](https://dev.mysql.com/doc/refman/8.0/en/upgrading-from-previous-series.md) [5.7 to 8.0.](https://dev.mysql.com/doc/refman/8.0/en/upgrading-from-previous-series.md)
- For important information about upgrading from MySQL 8.0 to 8.4, see [Upgrading from MySQL](http://dev.mysql.com/doc/refman/8.4/en/upgrading-from-previous-series.md) [8.0 to 8.4.](http://dev.mysql.com/doc/refman/8.4/en/upgrading-from-previous-series.md)
- In-place downgrading of MySQL is not supported by the MySQL Yum repository. Follow the instructions in Chapter 4, [Downgrading MySQL](#page-74-0).

# **Upgrading MySQL** 2.

Upgrade MySQL components using standard yum (or dnf) commands, such as MySQL Server:

```
sudo yum update mysql-server
```

For platforms that are dnf-enabled:

```
sudo dnf upgrade mysql-server
```

Alternatively, you can update MySQL by telling Yum to update everything on your system, which might take considerably more time. For platforms that are not dnf-enabled:

sudo yum update

For platforms that are dnf-enabled:

sudo dnf upgrade

![](_page_68_Picture_18.jpeg)

### **Note**

The MySQL server always restarts after an update by Yum.

You can also update only a specific component. Use the following command to list all the installed packages for the MySQL components (for dnf-enabled systems, replace yum in the command with dnf):

```
sudo yum list installed | grep "^mysql"
```

After identifying the package name of the component of your choice, update the package with the following command, replacing package-name with the name of the package. For platforms that are not dnf-enabled:

sudo yum update package-name

### For dnf-enabled platforms:

sudo dnf upgrade package-name

## **Upgrading the Shared Client Libraries**

After updating MySQL using the Yum repository, applications compiled with older versions of the shared client libraries should continue to work.

If you recompile applications and dynamically link them with the updated libraries: As typical with new versions of shared libraries where there are differences or additions in symbol versioning between the newer and older libraries (for example, between the newer, standard 8.4 shared client libraries and some older—prior or variant—versions of the shared libraries shipped natively by the Linux distributions' software repositories, or from some other sources), any applications compiled using the updated, newer shared libraries require those updated libraries on systems where the applications are deployed. As expected, if those libraries are not in place, the applications requiring the shared libraries fail. For this reason, be sure to deploy the packages for the shared libraries from MySQL on those systems. To do this, add the MySQL Yum repository to the systems (see Adding the MySQL Yum Repository) and install the latest shared libraries using the instructions given in Installing Additional MySQL Products and Components with Yum.

# <span id="page-69-0"></span>**3.9 Upgrading MySQL with the MySQL APT Repository**

On Debian and Ubuntu platforms, to perform an in-place upgrade of MySQL and its components, use the MySQL APT repository. See Upgrading MySQL with the MySQL APT Repository.

# <span id="page-69-1"></span>**3.10 Upgrading MySQL with the MySQL SLES Repository**

On the SUSE Linux Enterprise Server (SLES) platform, to perform an in-place upgrade of MySQL and its components, use the MySQL SLES repository. See Upgrading MySQL with the MySQL SLES Repository.

# <span id="page-69-2"></span>**3.11 Upgrading MySQL on Windows**

To upgrade MySQL on Windows, either [download and execute the latest MySQL Server MSI](#page-69-3) or [use](#page-70-2) [the Windows ZIP archive distribution.](#page-70-2)

![](_page_69_Picture_12.jpeg)

### **Note**

Unlike MySQL 8.4, MySQL 8.0 uses MySQL Installer to install and upgrade MySQL Server along with most other MySQL products; but MySQL Installer is not available with MySQL 8.1 and higher. However, the configuration functionality used in MySQL Installer is available as of MySQL 8.1 using Section 2.3.2, "Configuration: Using MySQL Configurator" that is bundled with both the MSI and Zip archive.

The approach you select depends on how the existing installation was performed. Before proceeding, review Chapter 3, [Upgrading MySQL](#page-52-0) for additional information on upgrading MySQL that is not specific to Windows.

# <span id="page-69-3"></span>**Upgrading MySQL with MSI**

Download and execute the latest MSI. Although upgrading between release series is not directly supported, the "Custom Setup" option allows defining an installation location as otherwise the MSI installs to the standard location, such as C:\Program Files\MySQL\MySQL Server 8.4\.

Execute MySQL Configurator to configure your installation.

## <span id="page-70-2"></span>**Upgrading MySQL Using the Windows ZIP Distribution**

To perform an upgrade using the Windows ZIP archive distribution:

- 1. Download the latest Windows ZIP Archive distribution of MySQL from [https://dev.mysql.com/](https://dev.mysql.com/downloads/) [downloads/.](https://dev.mysql.com/downloads/)
- 2. If the server is running, stop it. If the server is installed as a service, stop the service with the following command from the command prompt:

```
C:\> SC STOP mysqld_service_name
```

Alternatively, use NET STOP mysqld\_service\_name .

If you are not running the MySQL server as a service, use mysqladmin to stop it. For example, before upgrading from MySQL 8.3 to 8.4, use mysqladmin from MySQL 8.3 as follows:

C:\> **"C:\Program Files\MySQL\MySQL Server 8.3\bin\mysqladmin" -u root shutdown**

![](_page_70_Picture_9.jpeg)

#### **Note**

If the MySQL root user account has a password, invoke mysqladmin with the -p option and enter the password when prompted.

- 3. Extract the ZIP archive. You may either overwrite your existing MySQL installation (usually located at C:\mysql), or install it into a different directory, such as C:\mysql8. Overwriting the existing installation is recommended.
- 4. Restart the server. For example, use the SC START mysqld\_service\_name or NET START mysqld\_service\_name command if you run MySQL as a service, or invoke [mysqld](#page-158-0) directly otherwise.
- 5. If you encounter errors, see Section 2.3.4, "Troubleshooting a Microsoft Windows MySQL Server Installation".

# <span id="page-70-0"></span>**3.12 Upgrading a Docker Installation of MySQL**

To upgrade a Docker installation of MySQL, refer to Upgrading a MySQL Server Container.

# <span id="page-70-1"></span>**3.13 Upgrade Troubleshooting**

- A schema mismatch in a MySQL 8.3 instance between the .frm file of a table and the InnoDB data dictionary can cause an upgrade to MySQL 8.4 to fail. Such mismatches may be due to .frm file corruption. To address this issue, dump and restore affected tables before attempting the upgrade again.
- If problems occur, such as that the new [mysqld](#page-158-0) server does not start, verify that you do not have an old my.cnf file from your previous installation. You can check this with the [--print-defaults](#page-124-0) option (for example, [mysqld --print-defaults](#page-158-0)). If this command displays anything other than the program name, you have an active my.cnf file that affects server or client operation.
- If, after an upgrade, you experience problems with compiled client programs, such as Commands out of sync or unexpected core dumps, you probably have used old header or library files when compiling your programs. In this case, check the date for your mysql.h file and libmysqlclient.a library to verify that they are from the new MySQL distribution. If not, recompile your programs with the new headers and libraries. Recompilation might also be necessary for programs compiled against the shared client library if the library major version number has changed (for example, from libmysqlclient.so.20 to libmysqlclient.so.21).

- If you have created a loadable function with a given name and upgrade MySQL to a version that implements a new built-in function with the same name, the loadable function becomes inaccessible. To correct this, use DROP FUNCTION to drop the loadable function, and then use CREATE FUNCTION to re-create the loadable function with a different nonconflicting name. The same is true if the new version of MySQL implements a built-in function with the same name as an existing stored function. See Section 11.2.5, "Function Name Parsing and Resolution", for the rules describing how the server interprets references to different kinds of functions.
- If upgrade to MySQL 8.4 fails due to any of the issues outlined in [Section 3.6, "Preparing Your](#page-61-0) [Installation for Upgrade",](#page-61-0) the server reverts all changes to the data directory. In this case, remove all redo log files and restart the MySQL 8.3 server on the existing data directory to address the errors. The redo log files (ib\_logfile\*) reside in the MySQL data directory by default. After the errors are fixed, perform a slow shutdown (by setting innodb\_fast\_shutdown=0) before attempting the upgrade again.

# <span id="page-71-0"></span>**3.14 Rebuilding or Repairing Tables or Indexes**

This section describes how to rebuild or repair tables or indexes, which may be necessitated by:

- Changes to how MySQL handles data types or character sets. For example, an error in a collation might have been corrected, necessitating a table rebuild to update the indexes for character columns that use the collation.
- Required table repairs or upgrades reported by CHECK TABLE or mysqlcheck.

Methods for rebuilding a table include:

- [Dump and Reload Method](#page-71-1)
- [ALTER TABLE Method](#page-72-1)
- [REPAIR TABLE Method](#page-72-2)

# <span id="page-71-1"></span>**Dump and Reload Method**

If you are rebuilding tables because a different version of MySQL cannot handle them after a binary (in-place) upgrade or downgrade, you must use the dump-and-reload method. Dump the tables before upgrading or downgrading using your original version of MySQL. Then reload the tables after upgrading or downgrading.

If you use the dump-and-reload method of rebuilding tables only for the purpose of rebuilding indexes, you can perform the dump either before or after upgrading or downgrading. Reloading still must be done afterward.

If you need to rebuild an InnoDB table because a CHECK TABLE operation indicates that a table upgrade is required, use mysqldump to create a dump file and [mysql](#page-182-0) to reload the file. If the CHECK TABLE operation indicates that there is a corruption or causes InnoDB to fail, refer to Section 17.20.3, "Forcing InnoDB Recovery" for information about using the innodb\_force\_recovery option to restart InnoDB. To understand the type of problem that CHECK TABLE may be encountering, refer to the InnoDB notes in Section 15.7.3.2, "CHECK TABLE Statement".

To rebuild a table by dumping and reloading it, use mysqldump to create a dump file and [mysql](#page-182-0) to reload the file:

```
mysqldump db_name t1 > dump.sql
mysql db_name < dump.sql
```

To rebuild all the tables in a single database, specify the database name without any following table name:

```
mysqldump db_name > dump.sql
```

```
mysql db_name < dump.sql
```

To rebuild all tables in all databases, use the --all-databases option:

```
mysqldump --all-databases > dump.sql
mysql < dump.sql
```

## <span id="page-72-1"></span>**ALTER TABLE Method**

To rebuild a table with ALTER TABLE, use a "null" alteration; that is, an ALTER TABLE statement that "changes" the table to use the storage engine that it already has. For example, if t1 is an InnoDB table, use this statement:

```
ALTER TABLE t1 ENGINE = InnoDB;
```

If you are not sure which storage engine to specify in the ALTER TABLE statement, use SHOW CREATE TABLE to display the table definition.

# <span id="page-72-2"></span>**REPAIR TABLE Method**

The REPAIR TABLE method is only applicable to MyISAM, ARCHIVE, and CSV tables.

You can use REPAIR TABLE if the table checking operation indicates that there is a corruption or that an upgrade is required. For example, to repair a MyISAM table, use this statement:

```
REPAIR TABLE t1;
```

mysqlcheck --repair provides command-line access to the REPAIR TABLE statement. This can be a more convenient means of repairing tables because you can use the --databases or --alldatabases option to repair all tables in specific databases or all databases, respectively:

```
mysqlcheck --repair --databases db_name ...
mysqlcheck --repair --all-databases
```

# <span id="page-72-0"></span>**3.15 Copying MySQL Databases to Another Machine**

In cases where you need to transfer databases between different architectures, you can use mysqldump to create a file containing SQL statements. You can then transfer the file to the other machine and feed it as input to the [mysql](#page-182-0) client.

Use mysqldump --help to see what options are available.

![](_page_72_Picture_17.jpeg)

### **Note**

If GTIDs are in use on the server where you create the dump (gtid\_mode=ON), by default, mysqldump includes the contents of the gtid\_executed set in the dump to transfer these to the new machine. The results of this can vary depending on the MySQL Server versions involved. Check the description for the mysqldump --set-gtid-purged option to find what happens with the versions you are using, and how to change the behavior if the outcome of the default behavior is not suitable for your situation.

The easiest (although not the fastest) way to move a database between two machines is to run the following commands on the machine on which the database is located:

```
mysqladmin -h 'other_hostname' create db_name
mysqldump db_name | mysql -h 'other_hostname' db_name
```

If you want to copy a database from a remote machine over a slow network, you can use these commands:

```
mysqladmin create db_name
```

```
mysqldump -h 'other_hostname' --compress db_name | mysql db_name
```

You can also store the dump in a file, transfer the file to the target machine, and then load the file into the database there. For example, you can dump a database to a compressed file on the source machine like this:

```
mysqldump --quick db_name | gzip > db_name.gz
```

Transfer the file containing the database contents to the target machine and run these commands there:

```
mysqladmin create db_name
gunzip < db_name.gz | mysql db_name
```

You can also use mysqldump and mysqlimport to transfer the database. For large tables, this is much faster than simply using mysqldump. In the following commands, DUMPDIR represents the full path name of the directory you use to store the output from mysqldump.

First, create the directory for the output files and dump the database:

```
mkdir DUMPDIR
mysqldump --tab=DUMPDIR
 db_name
```

Then transfer the files in the DUMPDIR directory to some corresponding directory on the target machine and load the files into MySQL there:

```
mysqladmin create db_name # create database
cat DUMPDIR/*.sql | mysql db_name # create tables in database
mysqlimport db_name
 DUMPDIR/*.txt # load data into tables
```

Do not forget to copy the mysql database because that is where the grant tables are stored. You might have to run commands as the MySQL root user on the new machine until you have the mysql database in place.

After you import the mysql database on the new machine, execute mysqladmin flushprivileges so that the server reloads the grant table information.

# <span id="page-74-0"></span>Chapter 4 Downgrading MySQL

![](_page_74_Picture_1.jpeg)

#### **Notes**

- Make sure you understand the MySQL release model for MySQL long-term support (LTS) and Innovation releases before proceeding with a downgrade.
- A replication topology is downgraded by following the rolling downgrade scheme described at Section 19.5.3, "Upgrading or Downgrading a Replication Topology", which uses one of the supported single-server methods for each individual server downgrade.
- Monthly Rapid Updates (MRUs) and hot fixes also count as releases in this documentation.

**Table 4.1 Downgrade Paths for MySQL Server**

| Downgrade Path                                                                        | Path Examples                 | Supported Downgrade Methods                                           |
|---------------------------------------------------------------------------------------|-------------------------------|-----------------------------------------------------------------------|
| Within an LTS series                                                                  | 8.4.y LTS to 8.4.x LTS        | In-place, logical dump and load, MySQL Clone, or by using replication |
| From an LTS or Bugfix series to the previous LTS or<br>Bugfix series                  | 8.4.x LTS to 8.0.y            | Logical dump and load or by using replication                         |
| From an LTS or Bugfix series to an Innovation series after<br>the previous LTS series | 8.4.x LTS to 8.3.0 Innovation | Logical dump and load or by using replication                         |
| From within an Innovation series                                                      | 9.6 to 9.5                    | Logical dump and load or by using replication                         |
|                                                                                       |                               |                                                                       |

Downgrading to MySQL 5.7 or earlier is not supported.

# Chapter 5 Tutorial

# **Table of Contents**

| 5.1 Connecting to and Disconnecting from the Server 247               |     |
|-----------------------------------------------------------------------|-----|
| 5.2 Entering Queries 248                                              |     |
| 5.3 Creating and Using a Database 251                                 |     |
| 5.3.1 Creating and Selecting a Database 252                           |     |
| 5.3.2 Creating a Table 253                                            |     |
| 5.3.3 Loading Data into a Table 254                                   |     |
| 5.3.4 Retrieving Information from a Table 255                         |     |
| 5.4 Getting Information About Databases and Tables 268                |     |
| 5.5 Using mysql in Batch Mode 269                                     |     |
| 5.6 Examples of Common Queries 270                                    |     |
| 5.6.1 The Maximum Value for a Column 271                              |     |
| 5.6.2 The Row Holding the Maximum of a Certain Column                 | 271 |
| 5.6.3 Maximum of Column per Group 271                                 |     |
| 5.6.4 The Rows Holding the Group-wise Maximum of a Certain Column 272 |     |
| 5.6.5 Using User-Defined Variables 273                                |     |
| 5.6.6 Using Foreign Keys 273                                          |     |
| 5.6.7 Searching on Two Keys 275                                       |     |
| 5.6.8 Calculating Visits Per Day                                      | 275 |
| 5.6.9 Using AUTO_INCREMENT 276                                        |     |
| 5.7 Using MySQL with Apache 278                                       |     |

This chapter provides a tutorial introduction to MySQL by showing how to use the [mysql](#page-182-0) client program to create and use a simple database. [mysql](#page-182-0) (sometimes referred to as the "terminal monitor" or just "monitor") is an interactive program that enables you to connect to a MySQL server, run queries, and view the results. [mysql](#page-182-0) may also be used in batch mode: you place your queries in a file beforehand, then tell [mysql](#page-182-0) to execute the contents of the file. Both ways of using [mysql](#page-182-0) are covered here.

To see a list of options provided by [mysql](#page-182-0), invoke it with the [--help](#page-187-0) option:

```
$> mysql --help
```

This chapter assumes that [mysql](#page-182-0) is installed on your machine and that a MySQL server is available to which you can connect. If this is not true, contact your MySQL administrator. (If you are the administrator, you need to consult the relevant portions of this manual, such as Chapter 7, MySQL Server Administration.)

This chapter describes the entire process of setting up and using a database. If you are interested only in accessing an existing database, you may want to skip the sections that describe how to create the database and the tables it contains.

Because this chapter is tutorial in nature, many details are necessarily omitted. Consult the relevant sections of the manual for more information on the topics covered here.

# <span id="page-76-0"></span>**5.1 Connecting to and Disconnecting from the Server**

To connect to the server, you usually need to provide a MySQL user name when you invoke [mysql](#page-182-0) and, most likely, a password. If the server runs on a machine other than the one where you log in, you must also specify a host name. Contact your administrator to find out what connection parameters you should use to connect (that is, what host, user name, and password to use). Once you know the proper parameters, you should be able to connect like this:

```
$> mysql -h host -u user -p
```

```
Enter password: ********
```

host and user represent the host name where your MySQL server is running and the user name of your MySQL account. Substitute appropriate values for your setup. The \*\*\*\*\*\*\*\* represents your password; enter it when [mysql](#page-182-0) displays the Enter password: prompt.

If that works, you should see some introductory information followed by a mysql> prompt:

```
$> mysql -h host -u user -p
Enter password: ********
Welcome to the MySQL monitor. Commands end with ; or \g.
Your MySQL connection id is 25338 to server version: 8.4.8-standard
Type 'help;' or '\h' for help. Type '\c' to clear the buffer.
mysql>
```

The mysql> prompt tells you that [mysql](#page-182-0) is ready for you to enter SQL statements.

If you are logging in on the same machine that MySQL is running on, you can omit the host, and simply use the following:

```
$> mysql -u user -p
```

If, when you attempt to log in, you get an error message such as ERROR 2002 (HY000): Can't connect to local MySQL server through socket '/tmp/mysql.sock' (2), it means that the MySQL server daemon (Unix) or service (Windows) is not running. Consult the administrator or see the section of Chapter 2, Installing MySQL that is appropriate to your operating system.

For help with other problems often encountered when trying to log in, see Section B.3.2, "Common Errors When Using MySQL Programs".

Some MySQL installations permit users to connect as the anonymous (unnamed) user to the server running on the local host. If this is the case on your machine, you should be able to connect to that server by invoking [mysql](#page-182-0) without any options:

```
$> mysql
```

After you have connected successfully, you can disconnect any time by typing QUIT (or \q) at the mysql> prompt:

```
mysql> QUIT
Bye
```

On Unix, you can also disconnect by pressing Control+D.

Most examples in the following sections assume that you are connected to the server. They indicate this by the mysql> prompt.

# <span id="page-77-0"></span>**5.2 Entering Queries**

Make sure that you are connected to the server, as discussed in the previous section. Doing so does not in itself select any database to work with, but that is okay. At this point, it is more important to find out a little about how to issue queries than to jump right in creating tables, loading data into them, and retrieving data from them. This section describes the basic principles of entering queries, using several queries you can try out to familiarize yourself with how [mysql](#page-182-0) works.

Here is a simple query that asks the server to tell you its version number and the current date. Type it in as shown here following the mysql> prompt and press Enter:

```
mysql> SELECT VERSION(), CURRENT_DATE;
+-----------+--------------+
| VERSION() | CURRENT_DATE |
+-----------+--------------+
```

```
| 8.4.0-tr | 2024-01-25 |
+-----------+--------------+
1 row in set (0.00 sec)
mysql>
```

This query illustrates several things about [mysql](#page-182-0):

- A query normally consists of an SQL statement followed by a semicolon. (There are some exceptions where a semicolon may be omitted. QUIT, mentioned earlier, is one of them. We'll get to others later.)
- When you issue a query, [mysql](#page-182-0) sends it to the server for execution and displays the results, then prints another mysql> prompt to indicate that it is ready for another query.
- [mysql](#page-182-0) displays query output in tabular form (rows and columns). The first row contains labels for the columns. The rows following are the query results. Normally, column labels are the names of the columns you fetch from database tables. If you're retrieving the value of an expression rather than a table column (as in the example just shown), [mysql](#page-182-0) labels the column using the expression itself.
- [mysql](#page-182-0) shows how many rows were returned and how long the query took to execute, which gives you a rough idea of server performance. These values are imprecise because they represent wall clock time (not CPU or machine time), and because they are affected by factors such as server load and network latency. (For brevity, the "rows in set" line is sometimes not shown in the remaining examples in this chapter.)

Keywords may be entered in any lettercase. The following queries are equivalent:

```
mysql> SELECT VERSION(), CURRENT_DATE;
mysql> select version(), current_date;
mysql> SeLeCt vErSiOn(), current_DATE;
```

Here is another query. It demonstrates that you can use [mysql](#page-182-0) as a simple calculator:

```
mysql> SELECT SIN(PI()/4), (4+1)*5;
+------------------+---------+
| SIN(PI()/4) | (4+1)*5 |
+------------------+---------+
| 0.70710678118655 | 25 |
+------------------+---------+
1 row in set (0.02 sec)
```

The queries shown thus far have been relatively short, single-line statements. You can even enter multiple statements on a single line. Just end each one with a semicolon:

```
mysql> SELECT VERSION(); SELECT NOW();
+-----------+
| VERSION() |
+-----------+
| 8.4.0-tr |
+-----------+
1 row in set (0.00 sec)
+---------------------+
| NOW() |
+---------------------+
| 2024-01-25 18:33:04 |
+---------------------+
1 row in set (0.00 sec)
```

A query need not be given all on a single line, so lengthy queries that require several lines are not a problem. [mysql](#page-182-0) determines where your statement ends by looking for the terminating semicolon, not by looking for the end of the input line. (In other words, [mysql](#page-182-0) accepts free-format input: it collects input lines but does not execute them until it sees the semicolon.)

Here is a simple multiple-line statement:

```
mysql> SELECT
 -> USER()
 -> ,
 -> CURRENT_DATE;
+---------------+--------------+
| USER() | CURRENT_DATE |
+---------------+--------------+
| jon@localhost | 2018-08-24 |
+---------------+--------------+
```

In this example, notice how the prompt changes from mysql> to -> after you enter the first line of a multiple-line query. This is how [mysql](#page-182-0) indicates that it has not yet seen a complete statement and is waiting for the rest. The prompt is your friend, because it provides valuable feedback. If you use that feedback, you can always be aware of what [mysql](#page-182-0) is waiting for.

If you decide you do not want to execute a query that you are in the process of entering, cancel it by typing \c:

```
mysql> SELECT
 -> USER()
 -> \c
mysql>
```

Here, too, notice the prompt. It switches back to mysql> after you type \c, providing feedback to indicate that [mysql](#page-182-0) is ready for a new query.

The following table shows each of the prompts you may see and summarizes what they mean about the state that [mysql](#page-182-0) is in.

| Prompt | Meaning                                                                                          |
|--------|--------------------------------------------------------------------------------------------------|
| mysql> | Ready for new query                                                                              |
| ->     | Waiting for next line of multiple-line query                                                     |
| '>     | Waiting for next line, waiting for completion of a<br>string that began with a single quote (')  |
| ">     | Waiting for next line, waiting for completion of a<br>string that began with a double quote (")  |
| `>     | Waiting for next line, waiting for completion of an<br>identifier that began with a backtick (`) |
| /*>    | Waiting for next line, waiting for completion of a<br>comment that began with /*                 |

Multiple-line statements commonly occur by accident when you intend to issue a query on a single line, but forget the terminating semicolon. In this case, [mysql](#page-182-0) waits for more input:

```
mysql> SELECT USER()
 ->
```

If this happens to you (you think you've entered a statement but the only response is a -> prompt), most likely [mysql](#page-182-0) is waiting for the semicolon. If you don't notice what the prompt is telling you, you might sit there for a while before realizing what you need to do. Enter a semicolon to complete the statement, and [mysql](#page-182-0) executes it:

```
mysql> SELECT USER()
 -> ;
+---------------+
| USER() |
+---------------+
| jon@localhost |
+---------------+
```

The '> and "> prompts occur during string collection (another way of saying that MySQL is waiting for completion of a string). In MySQL, you can write strings surrounded by either ' or " characters (for example, 'hello' or "goodbye"), and [mysql](#page-182-0) lets you enter strings that span multiple lines. When you see a '> or "> prompt, it means that you have entered a line containing a string that begins with a ' or " quote character, but have not yet entered the matching quote that terminates the string. This often indicates that you have inadvertently left out a quote character. For example:

```
mysql> SELECT * FROM my_table WHERE name = 'Smith AND age < 30;
 '>
```

If you enter this SELECT statement, then press **Enter** and wait for the result, nothing happens. Instead of wondering why this query takes so long, notice the clue provided by the '> prompt. It tells you that [mysql](#page-182-0) expects to see the rest of an unterminated string. (Do you see the error in the statement? The string 'Smith is missing the second single quotation mark.)

At this point, what do you do? The simplest thing is to cancel the query. However, you cannot just type \c in this case, because [mysql](#page-182-0) interprets it as part of the string that it is collecting. Instead, enter the closing quote character (so [mysql](#page-182-0) knows you've finished the string), then type \c:

```
mysql> SELECT * FROM my_table WHERE name = 'Smith AND age < 30;
 '> '\c
mysql>
```

The prompt changes back to mysql>, indicating that [mysql](#page-182-0) is ready for a new query.

The `> prompt is similar to the '> and "> prompts, but indicates that you have begun but not completed a backtick-quoted identifier.

It is important to know what the '>, ">, and `> prompts signify, because if you mistakenly enter an unterminated string, any further lines you type appear to be ignored by [mysql](#page-182-0)—including a line containing QUIT. This can be quite confusing, especially if you do not know that you need to supply the terminating quote before you can cancel the current query.

![](_page_80_Picture_9.jpeg)

### **Note**

Multiline statements from this point on are written without the secondary (-> or other) prompts, to make it easier to copy and paste the statements to try for yourself.

# <span id="page-80-0"></span>**5.3 Creating and Using a Database**

Once you know how to enter SQL statements, you are ready to access a database.

Suppose that you have several pets in your home (your menagerie) and you would like to keep track of various types of information about them. You can do so by creating tables to hold your data and loading them with the desired information. Then you can answer different sorts of questions about your animals by retrieving data from the tables. This section shows you how to perform the following operations:

- Create a database
- Create a table
- Load data into the table
- Retrieve data from the table in various ways
- Use multiple tables

The menagerie database is simple (deliberately), but it is not difficult to think of real-world situations in which a similar type of database might be used. For example, a database like this could be used by a farmer to keep track of livestock, or by a veterinarian to keep track of patient records. A menagerie distribution containing some of the queries and sample data used in the following sections can be

obtained from the MySQL website. It is available in both compressed tar file and Zip formats at [https://](https://dev.mysql.com/doc/) [dev.mysql.com/doc/](https://dev.mysql.com/doc/).

Use the SHOW statement to find out what databases currently exist on the server:

```
mysql> SHOW DATABASES;
+----------+
| Database |
+----------+
| mysql |
| test |
| tmp |
+----------+
```

The mysql database describes user access privileges. The test database often is available as a workspace for users to try things out.

The list of databases displayed by the statement may be different on your machine; SHOW DATABASES does not show databases that you have no privileges for if you do not have the SHOW DATABASES privilege. See Section 15.7.7.15, "SHOW DATABASES Statement".

If the test database exists, try to access it:

```
mysql> USE test
Database changed
```

USE, like QUIT, does not require a semicolon. (You can terminate such statements with a semicolon if you like; it does no harm.) The USE statement is special in another way, too: it must be given on a single line.

You can use the test database (if you have access to it) for the examples that follow, but anything you create in that database can be removed by anyone else with access to it. For this reason, you should probably ask your MySQL administrator for permission to use a database of your own. Suppose that you want to call yours menagerie. The administrator needs to execute a statement like this:

```
mysql> GRANT ALL ON menagerie.* TO 'your_mysql_name'@'your_client_host';
```

where your\_mysql\_name is the MySQL user name assigned to you and your\_client\_host is the host from which you connect to the server.

# <span id="page-81-0"></span>**5.3.1 Creating and Selecting a Database**

If the administrator creates your database for you when setting up your permissions, you can begin using it. Otherwise, you need to create it yourself:

```
mysql> CREATE DATABASE menagerie;
```

Under Unix, database names are case-sensitive (unlike SQL keywords), so you must always refer to your database as menagerie, not as Menagerie, MENAGERIE, or some other variant. This is also true for table names. (Under Windows, this restriction does not apply, although you must refer to databases and tables using the same lettercase throughout a given query. However, for a variety of reasons, the recommended best practice is always to use the same lettercase that was used when the database was created.)

![](_page_81_Picture_16.jpeg)

#### **Note**

If you get an error such as ERROR 1044 (42000): Access denied for user 'micah'@'localhost' to database 'menagerie' when attempting to create a database, this means that your user account does not have the necessary privileges to do so. Discuss this with the administrator or see Section 8.2, "Access Control and Account Management".

Creating a database does not select it for use; you must do that explicitly. To make menagerie the current database, use this statement:

```
mysql> USE menagerie
Database changed
```

Your database needs to be created only once, but you must select it for use each time you begin a [mysql](#page-182-0) session. You can do this by issuing a USE statement as shown in the example. Alternatively, you can select the database on the command line when you invoke [mysql](#page-182-0). Just specify its name after any connection parameters that you might need to provide. For example:

```
$> mysql -h host -u user -p menagerie
Enter password: ********
```

![](_page_82_Picture_4.jpeg)

#### **Important**

menagerie in the command just shown is **not** your password. If you want to supply your password on the command line after the -p option, you must do so with no intervening space (for example, as -ppassword, not as -p password). However, putting your password on the command line is not recommended, because doing so exposes it to snooping by other users logged in on your machine.

![](_page_82_Picture_7.jpeg)

#### **Note**

You can see at any time which database is currently selected using SELECT DATABASE().

## <span id="page-82-0"></span>**5.3.2 Creating a Table**

Creating the database is the easy part, but at this point it is empty, as SHOW TABLES tells you:

```
mysql> SHOW TABLES;
Empty set (0.00 sec)
```

The harder part is deciding what the structure of your database should be: what tables you need and what columns should be in each of them.

You want a table that contains a record for each of your pets. This can be called the pet table, and it should contain, as a bare minimum, each animal's name. Because the name by itself is not very interesting, the table should contain other information. For example, if more than one person in your family keeps pets, you might want to list each animal's owner. You might also want to record some basic descriptive information such as species and sex.

How about age? That might be of interest, but it is not a good thing to store in a database. Age changes as time passes, which means you'd have to update your records often. Instead, it is better to store a fixed value such as date of birth. Then, whenever you need age, you can calculate it as the difference between the current date and the birth date. MySQL provides functions for doing date arithmetic, so this is not difficult. Storing birth date rather than age has other advantages, too:

- You can use the database for tasks such as generating reminders for upcoming pet birthdays. (If you think this type of query is somewhat silly, note that it is the same question you might ask in the context of a business database to identify clients to whom you need to send out birthday greetings in the current week or month, for that computer-assisted personal touch.)
- You can calculate age in relation to dates other than the current date. For example, if you store death date in the database, you can easily calculate how old a pet was when it died.

You can probably think of other types of information that would be useful in the pet table, but the ones identified so far are sufficient: name, owner, species, sex, birth, and death.

Use a CREATE TABLE statement to specify the layout of your table:

```
mysql> CREATE TABLE pet (name VARCHAR(20), owner VARCHAR(20),
 species VARCHAR(20), sex CHAR(1), birth DATE, death DATE);
```

VARCHAR is a good choice for the name, owner, and species columns because the column values vary in length. The lengths in those column definitions need not all be the same, and need not be 20. You can normally pick any length from 1 to 65535, whatever seems most reasonable to you. If you make a poor choice and it turns out later that you need a longer field, MySQL provides an ALTER TABLE statement.

Several types of values can be chosen to represent sex in animal records, such as 'm' and 'f', or perhaps 'male' and 'female'. It is simplest to use the single characters 'm' and 'f'.

The use of the DATE data type for the birth and death columns is a fairly obvious choice.

Once you have created a table, SHOW TABLES should produce some output:

```
mysql> SHOW TABLES;
+---------------------+
| Tables in menagerie |
+---------------------+
| pet |
+---------------------+
```

To verify that your table was created the way you expected, use a DESCRIBE statement:

| mysql> DESCRIBE pet;<br>+++++++ |      |                   |  |     |  |  |                                           |      |
|---------------------------------|------|-------------------|--|-----|--|--|-------------------------------------------|------|
| Field                           | Type |                   |  |     |  |  | Null   Key   Default   Extra  <br>+++++++ |      |
| name                            |      | varchar(20)   YES |  |     |  |  | NULL                                      | <br> |
| owner                           |      | varchar(20)   YES |  |     |  |  | NULL                                      | <br> |
| species   varchar(20)   YES     |      |                   |  |     |  |  | NULL                                      | <br> |
| sex                             |      | char(1)           |  | YES |  |  | NULL                                      | <br> |
| birth                           | date |                   |  | YES |  |  | NULL                                      | <br> |
| death                           | date |                   |  | YES |  |  | NULL                                      | <br> |
|                                 |      |                   |  |     |  |  | +++++++                                   |      |

You can use DESCRIBE any time, for example, if you forget the names of the columns in your table or what types they have.

For more information about MySQL data types, see Chapter 13, Data Types.

# <span id="page-83-0"></span>**5.3.3 Loading Data into a Table**

After creating your table, you need to populate it. The LOAD DATA and INSERT statements are useful for this.

Suppose that your pet records can be described as shown here. (Observe that MySQL expects dates in 'YYYY-MM-DD' format; this may differ from what you are used to.)

| name     | owner  | species | sex | birth      | death      |
|----------|--------|---------|-----|------------|------------|
| Fluffy   | Harold | cat     | f   | 1993-02-04 |            |
| Claws    | Gwen   | cat     | m   | 1994-03-17 |            |
| Buffy    | Harold | dog     | f   | 1989-05-13 |            |
| Fang     | Benny  | dog     | m   | 1990-08-27 |            |
| Bowser   | Diane  | dog     | m   | 1979-08-31 | 1995-07-29 |
| Chirpy   | Gwen   | bird    | f   | 1998-09-11 |            |
| Whistler | Gwen   | bird    |     | 1997-12-09 |            |
| Slim     | Benny  | snake   | m   | 1996-04-29 |            |

Because you are beginning with an empty table, an easy way to populate it is to create a text file containing a row for each of your animals, then load the contents of the file into the table with a single statement.

You could create a text file pet.txt containing one record per line, with values separated by tabs, and given in the order in which the columns were listed in the CREATE TABLE statement. For missing values (such as unknown sexes or death dates for animals that are still living), you can use NULL values. To represent these in your text file, use \N (backslash, capital-N). For example, the record for Whistler the bird would look like this (where the whitespace between values is a single tab character):

```
Whistler Gwen bird \N 1997-12-09 \N
```

To load the text file pet.txt into the pet table, use this statement:

```
mysql> LOAD DATA LOCAL INFILE '/path/pet.txt' INTO TABLE pet;
```

If you created the file on Windows with an editor that uses \r\n as a line terminator, you should use this statement instead:

```
mysql> LOAD DATA LOCAL INFILE '/path/pet.txt' INTO TABLE pet
 LINES TERMINATED BY '\r\n';
```

(On an Apple machine running macOS, you would likely want to use LINES TERMINATED BY '\r'.)

You can specify the column value separator and end of line marker explicitly in the LOAD DATA statement if you wish, but the defaults are tab and linefeed. These are sufficient for the statement to read the file pet.txt properly.

If the statement fails, it is likely that your MySQL installation does not have local file capability enabled by default. See Section 8.1.6, "Security Considerations for LOAD DATA LOCAL", for information on how to change this.

When you want to add new records one at a time, the INSERT statement is useful. In its simplest form, you supply values for each column, in the order in which the columns were listed in the CREATE TABLE statement. Suppose that Diane gets a new hamster named "Puffball." You could add a new record using an INSERT statement like this:

```
mysql> INSERT INTO pet
 VALUES ('Puffball','Diane','hamster','f','1999-03-30',NULL);
```

String and date values are specified as quoted strings here. Also, with INSERT, you can insert NULL directly to represent a missing value. You do not use \N like you do with LOAD DATA.

From this example, you should be able to see that there would be a lot more typing involved to load your records initially using several INSERT statements rather than a single LOAD DATA statement.

# <span id="page-84-0"></span>**5.3.4 Retrieving Information from a Table**

The SELECT statement is used to pull information from a table. The general form of the statement is:

```
SELECT what_to_select
FROM which_table
WHERE conditions_to_satisfy;
```

what\_to\_select indicates what you want to see. This can be a list of columns, or \* to indicate "all columns." which\_table indicates the table from which you want to retrieve data. The WHERE clause is optional. If it is present, conditions\_to\_satisfy specifies one or more conditions that rows must satisfy to qualify for retrieval.