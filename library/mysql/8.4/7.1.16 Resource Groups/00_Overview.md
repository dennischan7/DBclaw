---
source: MySQL 8.4 Reference
title: 00_Overview
---

MySQL supports creation and management of resource groups, and permits assigning threads running within the server to particular groups so that threads execute according to the resources available to the group. Group attributes enable control over its resources, to enable or restrict resource consumption by threads in the group. DBAs can modify these attributes as appropriate for different workloads.

Currently, CPU time is a manageable resource, represented by the concept of "virtual CPU" as a term that includes CPU cores, hyperthreads, hardware threads, and so forth. The server determines at startup how many virtual CPUs are available, and database administrators with appropriate privileges can associate these CPUs with resource groups and assign threads to groups.

For example, to manage execution of batch jobs that need not execute with high priority, a DBA can create a Batch resource group, and adjust its priority up or down depending on how busy the server is. (Perhaps batch jobs assigned to the group should run at lower priority during the day and at higher priority during the night.) The DBA can also adjust the set of CPUs available to the group. Groups can be enabled or disabled to control whether threads are assignable to them.

The following sections describe aspects of resource group use in MySQL:

- [Resource Group Elements](#page-196-0)
- [Resource Group Attributes](#page-196-1)
- [Resource Group Management](#page-197-0)
- [Resource Group Replication](#page-198-0)
- [Resource Group Restrictions](#page-199-0)

![](_page_196_Picture_7.jpeg)

#### **Important**

On some platforms or MySQL server configurations, resource groups are unavailable or have limitations. In particular, Linux systems might require a manual step for some installation methods. For details, see [Resource Group](#page-199-0) [Restrictions](#page-199-0).

## <span id="page-196-0"></span>**Resource Group Elements**

These capabilities provide the SQL interface for resource group management in MySQL:

- SQL statements enable creating, altering, and dropping resource groups, and enable assigning threads to resource groups. An optimizer hint enables assigning individual statements to resource groups.
- Resource group privileges provide control over which users can perform resource group operations.
- The Information Schema RESOURCE\_GROUPS table exposes information about resource group definitions and the Performance Schema threads table shows the resource group assignment for each thread.
- Status variables provide execution counts for each management SQL statement.

## <span id="page-196-1"></span>**Resource Group Attributes**

Resource groups have attributes that define the group. All attributes can be set at group creation time. Some attributes are fixed at creation time; others can be modified any time thereafter.

These attributes are defined at resource group creation time and cannot be modified:

- Each group has a name. Resource group names are identifiers like table and column names, and need not be quoted in SQL statements unless they contain special characters or are reserved words. Group names are not case-sensitive and may be up to 64 characters long.
- Each group has a type, which is either SYSTEM or USER. The resource group type affects the range of priority values assignable to the group, as described later. This attribute together with the differences in permitted priorities enables system threads to be identified so as to protect them from contention for CPU resources against user threads.

System and user threads correspond to background and foreground threads as listed in the Performance Schema threads table.

These attributes are defined at resource group creation time and can be modified any time thereafter:

- The CPU affinity is the set of virtual CPUs the resource group can use. An affinity can be any nonempty subset of the available CPUs. If a group has no affinity, it can use all available CPUs.
- The thread priority is the execution priority for threads assigned to the resource group. Priority values range from -20 (highest priority) to 19 (lowest priority). The default priority is 0, for both system and user groups.

System groups are permitted a higher priority than user groups, ensuring that user threads never have a higher priority than system threads:

- For system resource groups, the permitted priority range is -20 to 0.
- For user resource groups, the permitted priority range is 0 to 19.
- Each group can be enabled or disabled, affording administrators control over thread assignment. Threads can be assigned only to enabled groups.

# <span id="page-197-0"></span>**Resource Group Management**

By default, there is one system group and one user group, named SYS\_default and USR\_default, respectively. These default groups cannot be dropped and their attributes cannot be modified. Each default group has no CPU affinity and priority 0.

Newly created system and user threads are assigned to the SYS\_default and USR\_default groups, respectively.

For user-defined resource groups, all attributes are assigned at group creation time. After a group has been created, its attributes can be modified, with the exception of the name and type attributes.

To create and manage user-defined resource groups, use these SQL statements:

- CREATE RESOURCE GROUP creates a new group. See Section 15.7.2.2, "CREATE RESOURCE GROUP Statement".
- ALTER RESOURCE GROUP modifies an existing group. See Section 15.7.2.1, "ALTER RESOURCE GROUP Statement".
- DROP RESOURCE GROUP drops an existing group. See Section 15.7.2.3, "DROP RESOURCE GROUP Statement".

Those statements require the RESOURCE\_GROUP\_ADMIN privilege.

To manage resource group assignments, use these capabilities:

- SET RESOURCE GROUP assigns threads to a group. See Section 15.7.2.4, "SET RESOURCE GROUP Statement".
- The RESOURCE\_GROUP optimizer hint assigns individual statements to a group. See Section 10.9.3, "Optimizer Hints".

Those operations require the RESOURCE\_GROUP\_ADMIN or RESOURCE\_GROUP\_USER privilege.

Resource group definitions are stored in the resource\_groups data dictionary table so that groups persist across server restarts. Because resource\_groups is part of the data dictionary, it is not directly accessible by users. Resource group information is available using the Information Schema RESOURCE\_GROUPS table, which is implemented as a view on the data dictionary table. See Section 28.3.26, "The INFORMATION\_SCHEMA RESOURCE\_GROUPS Table".

Initially, the RESOURCE\_GROUPS table has these rows describing the default groups:

```
mysql> SELECT * FROM INFORMATION_SCHEMA.RESOURCE_GROUPS\G
*************************** 1. row ***************************
 RESOURCE_GROUP_NAME: USR_default
 RESOURCE_GROUP_TYPE: USER
RESOURCE_GROUP_ENABLED: 1
 VCPU_IDS: 0-3
 THREAD_PRIORITY: 0
*************************** 2. row ***************************
 RESOURCE_GROUP_NAME: SYS_default
```

```
 RESOURCE_GROUP_TYPE: SYSTEM
RESOURCE_GROUP_ENABLED: 1
 VCPU_IDS: 0-3
 THREAD_PRIORITY: 0
```

The THREAD\_PRIORITY values are 0, indicating the default priority. The VCPU\_IDS values show a range comprising all available CPUs. For the default groups, the displayed value varies depending on the system on which the MySQL server runs.

Earlier discussion mentioned a scenario involving a resource group named Batch to manage execution of batch jobs that need not execute with high priority. To create such a group, use a statement similar to this:

```
CREATE RESOURCE GROUP Batch
 TYPE = USER
 VCPU = 2-3 -- assumes a system with at least 4 CPUs
 THREAD_PRIORITY = 10;
```

To verify that the resource group was created as expected, check the RESOURCE\_GROUPS table:

```
mysql> SELECT * FROM INFORMATION_SCHEMA.RESOURCE_GROUPS
 WHERE RESOURCE_GROUP_NAME = 'Batch'\G
*************************** 1. row ***************************
 RESOURCE_GROUP_NAME: Batch
 RESOURCE_GROUP_TYPE: USER
RESOURCE_GROUP_ENABLED: 1
 VCPU_IDS: 2-3
 THREAD_PRIORITY: 10
```

If the THREAD\_PRIORITY value is 0 rather than 10, check whether your platform or system configuration limits the resource group capability; see [Resource Group Restrictions.](#page-199-0)

To assign a thread to the Batch group, do this:

```
SET RESOURCE GROUP Batch FOR thread_id;
```

Thereafter, statements in the named thread execute with Batch group resources.

If a session's own current thread should be in the Batch group, execute this statement within the session:

```
SET RESOURCE GROUP Batch;
```

Thereafter, statements in the session execute with Batch group resources.

To execute a single statement using the Batch group, use the RESOURCE\_GROUP optimizer hint:

```
INSERT /*+ RESOURCE_GROUP(Batch) */ INTO t2 VALUES(2);
```

Threads assigned to the Batch group execute with its resources, which can be modified as desired:

• For times when the system is highly loaded, decrease the number of CPUs assigned to the group, lower its priority, or (as shown) both:

```
ALTER RESOURCE GROUP Batch
 VCPU = 3
 THREAD_PRIORITY = 19;
```

• For times when the system is lightly loaded, increase the number of CPUs assigned to the group, raise its priority, or (as shown) both:

```
ALTER RESOURCE GROUP Batch
 VCPU = 0-3
 THREAD_PRIORITY = 0;
```

# <span id="page-198-0"></span>**Resource Group Replication**

Resource group management is local to the server on which it occurs. Resource group SQL statements and modifications to the resource\_groups data dictionary table are not written to the binary log and are not replicated.

# <span id="page-199-0"></span>**Resource Group Restrictions**

On some platforms or MySQL server configurations, resource groups are unavailable or have limitations:

- Resource groups are unavailable if the thread pool plugin is installed.
- Resource groups are unavailable on macOS, which provides no API for binding CPUs to a thread.
- On FreeBSD and Solaris, resource group thread priorities are ignored. (Effectively, all threads run at priority 0.) Attempts to change priorities result in a warning:

```
mysql> ALTER RESOURCE GROUP abc THREAD_PRIORITY = 10;
Query OK, 0 rows affected, 1 warning (0.18 sec)
mysql> SHOW WARNINGS;
+---------+------+-------------------------------------------------------------+
| Level | Code | Message |
+---------+------+-------------------------------------------------------------+
| Warning | 4560 | Attribute thread_priority is ignored (using default value). |
+---------+------+-------------------------------------------------------------+
```

• On Linux, resource groups thread priorities are ignored unless the CAP\_SYS\_NICE capability is set. Granting CAP\_SYS\_NICE capability to a process enables a range of privileges; consult [http://](http://man7.org/linux/man-pages/man7/capabilities.7.md) [man7.org/linux/man-pages/man7/capabilities.7.html](http://man7.org/linux/man-pages/man7/capabilities.7.md) for the full list. Please be careful when enabling this capability.

On Linux platforms using systemd and kernel support for Ambient Capabilities (Linux 4.3 or newer), the recommended way to enable CAP\_SYS\_NICE capability is to modify the MySQL service file and leave the mysqld binary unmodified. To adjust the service file for MySQL, use this procedure:

- 1. Run the appropriate command for your platform:
  - Oracle Linux, Red Hat, and Fedora systems:

```
$> sudo systemctl edit mysqld
```

• SUSE, Ubuntu, and Debian systems:

```
$> sudo systemctl edit mysql
```

2. Using an editor, add the following text to the service file:

```
[Service]
AmbientCapabilities=CAP_SYS_NICE
```

3. Restart the MySQL service.

If you cannot enable the CAP\_SYS\_NICE capability as just described, it can be set manually using the setcap command, specifying the path name to the mysqld executable (this requires sudo access). You can check the capabilities using getcap. For example:

```
$> sudo setcap cap_sys_nice+ep /path/to/mysqld
$> getcap /path/to/mysqld
/path/to/mysqld = cap_sys_nice+ep
```

As a safety measure, restrict execution of the mysqld binary to the root user and users with mysql group membership:

```
$> sudo chown root:mysql /path/to/mysqld
$> sudo chmod 0750 /path/to/mysqld
```

![](_page_0_Picture_1.jpeg)

#### **Important**

If manual use of setcap is required, it must be performed after each reinstall.

• On Windows, threads run at one of five thread priority levels. The resource group thread priority range of -20 to 19 maps onto those levels as indicated in the following table.

**Table 7.6 Resource Group Thread Priority on Windows**

| Priority Range | Windows Priority Level       |
|----------------|------------------------------|
| -20 to -10     | THREAD_PRIORITY_HIGHEST      |
| -9 to -1       | THREAD_PRIORITY_ABOVE_NORMAL |
| 0              | THREAD_PRIORITY_NORMAL       |
| 1 to 10        | THREAD_PRIORITY_BELOW_NORMAL |
| 11 to 19       | THREAD_PRIORITY_LOWEST       |

# <span id="page-0-1"></span>**7.1.17 Server-Side Help Support**

MySQL Server supports a HELP statement that returns information from the MySQL Reference Manual (see Section 15.8.3, "HELP Statement"). This information is stored in several tables in the mysql schema (see [Section 7.3, "The mysql System Schema"\)](#page-6-0). Proper operation of the HELP statement requires that these help tables be initialized.

For a new installation of MySQL using a binary or source distribution on Unix, help-table content initialization occurs when you initialize the data directory (see Section 2.9.1, "Initializing the Data Directory"). For an RPM distribution on Linux or binary distribution on Windows, content initialization occurs as part of the MySQL installation process.

For a MySQL upgrade using a binary distribution, help-table content is upgraded automatically by the server. To upgrade it manually, locate the fill\_help\_tables.sql file in the share or share/ mysql directory. Change location into that directory and process the file with the mysql client as follows:

```
mysql -u root -p mysql < fill_help_tables.sql
```

The command shown here assumes that you connect to the server using an account such as root that has privileges for modifying tables in the mysql schema. Adjust the connection parameters as required.