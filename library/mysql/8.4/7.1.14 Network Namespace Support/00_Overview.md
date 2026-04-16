---
source: MySQL 8.4 Reference
title: 00_Overview
---

A network namespace is a logical copy of the network stack from the host system. Network namespaces are useful for setting up containers or virtual environments. Each namespace has its own IP addresses, network interfaces, routing tables, and so forth. The default or global namespace is the one in which the host system physical interfaces exist.

Namespace-specific address spaces can lead to problems when MySQL connections cross namespaces. For example, the network address space for a MySQL instance running in a container or virtual network may differ from the address space of the host machine. This can produce phenomena such as a client connection from an address in one namespace appearing to the MySQL server to be coming from a different address, even for client and server running on the same machine. Suppose that both processes run on a host with IP address 203.0.113.10 but use different namespaces. A connection may produce a result like this:

```
$> mysql --user=admin --host=203.0.113.10 --protocol=tcp
mysql> SELECT USER();
+--------------------+
| USER() |
+--------------------+
| admin@198.51.100.2 |
+--------------------+
```

In this case, the expected USER() value is admin@203.0.113.10. Such behavior can make it difficult to assign account permissions properly if the address from which an connection originates is not what it appears.

To address this issue, MySQL enables specifying the network namespace to use for TCP/IP connections, so that both endpoints of connections use an agreed-upon common address space.

MySQL supports network namespaces on platforms that implement them. Support within MySQL applies to:

- The MySQL server, mysqld.
- X Plugin.
- The mysql client and the mysqlxtest test suite client. (Other clients are not supported. They must be invoked from within the network namespace of the server to which they are to connect.)
- Regular replication.
- Group Replication, only when using the MySQL communication stack to establish group communication connections.

The following sections describe how to use network namespaces in MySQL:

- [Host System Prerequisites](#page-186-0)
- [MySQL Configuration](#page-188-0)
- [Network Namespace Monitoring](#page-190-1)

# <span id="page-186-0"></span>**Host System Prerequisites**

Prior to using network namespace support in MySQL, these host system prerequisites must be satisfied:

- The host operating system must support network namespaces. (For example, Linux.)
- Any network namespace to be used by MySQL must first be created on the host system.
- Host name resolution must be configured by the system administrator to support network namespaces.

![](_page_186_Picture_17.jpeg)

#### **Note**

A known limitation is that, within MySQL, host name resolution does not work for names specified in network namespace-specific host files. For example, if the address for a host name in the red namespace is specified in the / etc/netns/red/hosts file, binding to the name fails on both the server and client sides. The workaround is to use the IP address rather than the host name.

• The system administrator must enable the CAP\_SYS\_ADMIN operating system privilege for the MySQL binaries that support network namespaces (mysqld, mysql, mysqlxtest).

![](_page_186_Picture_21.jpeg)

#### **Important**

Enabling CAP\_SYS\_ADMIN is a security sensitive operation because it enables a process to perform other privileged actions in addition to setting namespaces. For a description of its effects, see [https://man7.org/linux/man](https://man7.org/linux/man-pages/man7/capabilities.7.md)[pages/man7/capabilities.7.html](https://man7.org/linux/man-pages/man7/capabilities.7.md).

Because CAP\_SYS\_ADMIN must be enabled explicitly by the system administrator, MySQL binaries by default do not have network namespace support enabled. The system administrator should evaluate the security implications of running MySQL processes with CAP\_SYS\_ADMIN before enabling it.

The instructions in the following example set up network namespaces named red and blue. The names you choose may differ, as may the network addresses and interfaces on your host system.

Invoke the commands shown here either as the root operating system user or by prefixing each command with sudo. For example, to invoke the ip or setcap command if you are not root, use sudo ip or sudo setcap.

To configure network namespaces, use the ip command. For some operations, the ip command must execute within a particular namespace (which must already exist). In such cases, begin the command like this:

```
ip netns exec namespace_name
```

For example, this command executes within the red namespace to bring up the loopback interface:

```
ip netns exec red ip link set lo up
```

To add namespaces named red and blue, each with its own virtual Ethernet device used as a link between namespaces and its own loopback interface:

```
ip netns add red
ip link add veth-red type veth peer name vpeer-red
ip link set vpeer-red netns red
ip addr add 192.0.2.1/24 dev veth-red
ip link set veth-red up
ip netns exec red ip addr add 192.0.2.2/24 dev vpeer-red
ip netns exec red ip link set vpeer-red up
ip netns exec red ip link set lo up
ip netns add blue
ip link add veth-blue type veth peer name vpeer-blue
ip link set vpeer-blue netns blue
ip addr add 198.51.100.1/24 dev veth-blue
ip link set veth-blue up
ip netns exec blue ip addr add 198.51.100.2/24 dev vpeer-blue
ip netns exec blue ip link set vpeer-blue up
ip netns exec blue ip link set lo up
# if you want to enable inter-subnet routing...
sysctl net.ipv4.ip_forward=1
ip netns exec red ip route add default via 192.0.2.1
ip netns exec blue ip route add default via 198.51.100.1
```

A diagram of the links between namespaces looks like this:

```
red global blue
192.0.2.2 <=> 192.0.2.1
(vpeer-red) (veth-red)
 198.51.100.1 <=> 198.51.100.2
 (veth-blue) (vpeer-blue)
```

To check which namespaces and links exist:

```
ip netns list
ip link list
```

To see the routing tables for the global and named namespaces:

```
ip route show
ip netns exec red ip route show
ip netns exec blue ip route show
```

To remove the red and blue links and namespaces:

```
ip link del veth-red
ip link del veth-blue
```

```
ip netns del red
ip netns del blue
sysctl net.ipv4.ip_forward=0
```

So that the MySQL binaries that include network namespace support can actually use namespaces, you must grant them the CAP\_SYS\_ADMIN capability. The following setcap commands assume that you have changed location to the directory containing your MySQL binaries (adjust the pathname for your system as necessary):

```
cd /usr/local/mysql/bin
```

To grant CAP\_SYS\_ADMIN capability to the appropriate binaries:

```
setcap cap_sys_admin+ep ./mysqld
setcap cap_sys_admin+ep ./mysql
setcap cap_sys_admin+ep ./mysqlxtest
```

To check CAP\_SYS\_ADMIN capability:

```
$> getcap ./mysqld ./mysql ./mysqlxtest
./mysqld = cap_sys_admin+ep
./mysql = cap_sys_admin+ep
./mysqlxtest = cap_sys_admin+ep
```

To remove CAP\_SYS\_ADMIN capability:

```
setcap -r ./mysqld
setcap -r ./mysql
setcap -r ./mysqlxtest
```

![](_page_188_Picture_10.jpeg)

### **Important**

If you reinstall binaries to which you have previously applied setcap, you must use setcap again. For example, if you perform an in-place MySQL upgrade, failure to grant the CAP\_SYS\_ADMIN capability again results in namespacerelated failures. The server fails with this error for attempts to bind to an address with a named namespace:

```
[ERROR] [MY-013408] [Server] setns() failed with error 'Operation not permitted'
```

A client invoked with the --network-namespace option fails like this:

```
ERROR: Network namespace error: Operation not permitted
```

## <span id="page-188-0"></span>**MySQL Configuration**

Assuming that the preceding host system prerequisites have been satisfied, MySQL enables configuring the server-side namespace for the listening (inbound) side of connections and the clientside namespace for the outbound side of connections.

On the server side, the bind\_address, admin\_address, and mysqlx\_bind\_address system variables have extended syntax for specifying the network namespace to use for a given IP address or host name on which to listen for incoming connections. To specify a namespace for an address, add a slash and the namespace name. For example, a server my.cnf file might contain these lines:

```
[mysqld]
bind_address = 127.0.1.1,192.0.2.2/red,198.51.100.2/blue
admin_address = 102.0.2.2/red
mysqlx_bind_address = 102.0.2.2/red
```

These rules apply:

• A network namespace can be specified for an IP address or a host name.

- A network namespace cannot be specified for a wildcard IP address.
- For a given address, the network namespace is optional. If given, it must be specified as a /ns suffix immediately following the address.
- An address with no /ns suffix uses the host system global namespace. The global namespace is therefore the default.
- An address with a /ns suffix uses the namespace named ns.
- The host system must support network namespaces and each named namespace must previously have been set up. Naming a nonexistent namespace produces an error.
- bind\_address and mysqlx\_bind\_address accept a list of multiple comma-separated addresses, the variable value can specify addresses in the global namespace, in named namespaces, or a mix.

If an error occurs during server startup for attempts to use a namespace, the server does not start. If errors occur for X Plugin during plugin initialization such that it is unable to bind to any address, the plugin fails its initialization sequence and the server does not load it.

On the client side, a network namespace can be specified in these contexts:

• For the mysql client and the mysqlxtest test suite client, use the --network-namespace option. For example:

```
mysql --host=192.0.2.2 --network-namespace=red
```

If the --network-namespace option is omitted, the connection uses the default (global) namespace.

• For replication connections from replica servers to source servers, use the CHANGE REPLICATION SOURCE TO statement and specify the NETWORK\_NAMESPACE option. For example:

```
CHANGE REPLICATION SOURCE TO
 SOURCE_HOST = '192.0.2.2',
 NETWORK_NAMESPACE = 'red';
```

If the NETWORK\_NAMESPACE option is omitted, replication connections use the default (global) namespace.

The following example sets up a MySQL server that listens for connections in the global, red, and blue namespaces, and shows how to configure accounts that connect from the red and blue namespaces. It is assumed that the red and blue namespaces have already been created as shown in [Host System Prerequisites](#page-186-0).

1. Configure the server to listen on addresses in multiple namespaces. Put these lines in the server my.cnf file and start the server:

```
[mysqld]
bind_address = 127.0.1.1,192.0.2.2/red,198.51.100.2/blue
```

The value tells the server to listen on the loopback address 127.0.0.1 in the global namespace, the address 192.0.2.2 in the red namespace, and the address 198.51.100.2 in the blue namespace.

2. Connect to the server in the global namespace and create accounts that have permission to connect from an address in the address space of each named namespace:

```
$> mysql -u root -h 127.0.0.1 -p
Enter password: root_password
mysql> CREATE USER 'red_user'@'192.0.2.2'
 IDENTIFIED BY 'red_user_password';
mysql> CREATE USER 'blue_user'@'198.51.100.2'
```

```
 IDENTIFIED BY 'blue_user_password';
```

3. Verify that you can connect to the server in each named namespace:

```
$> mysql -u red_user -h 192.0.2.2 --network-namespace=red -p
Enter password: red_user_password
mysql> SELECT USER();
+--------------------+
| USER() |
+--------------------+
| red_user@192.0.2.2 |
+--------------------+
```

```
$> mysql -u blue_user -h 198.51.100.2 --network-namespace=blue -p
Enter password: blue_user_password
mysql> SELECT USER();
+------------------------+
| USER() |
+------------------------+
| blue_user@198.51.100.2 |
+------------------------+
```

![](_page_190_Picture_5.jpeg)

#### **Note**

You might see different results from USER(), which can return a value that includes a host name rather than an IP address if your DNS is configured to be able to resolve the address to the corresponding host name and the server is not run with the [skip\\_name\\_resolve](#page-67-2) system variable enabled.

You might also try invoking mysql without the --network-namespace option to see whether the connection attempt succeeds, and, if so, how the USER() value is affected.

## <span id="page-190-1"></span>**Network Namespace Monitoring**

For replication monitoring purposes, these information sources have a column that displays the applicable network namespace for connections:

- The Performance Schema replication\_connection\_configuration table. See Section 29.12.11.11, "The replication\_connection\_configuration Table".
- The replica server connection metadata repository. See Section 19.2.4.2, "Replication Metadata Repositories".
- The SHOW REPLICA STATUS statement.

# <span id="page-190-0"></span>**7.1.15 MySQL Server Time Zone Support**

This section describes the time zone settings maintained by MySQL, how to load the system tables required for named time support, how to stay current with time zone changes, and how to enable leapsecond support.

Time zone offsets are also supported for inserted datetime values; see Section 13.2.2, "The DATE, DATETIME, and TIMESTAMP Types", for more information.

For information about time zone settings in replication setups, see Section 19.5.1.14, "Replication and System Functions" and Section 19.5.1.33, "Replication and Time Zones".

- [Time Zone Variables](#page-191-0)
- [Populating the Time Zone Tables](#page-192-0)
- [Staying Current with Time Zone Changes](#page-193-0)

• [Time Zone Leap Second Support](#page-194-0)

# <span id="page-191-0"></span>**Time Zone Variables**

MySQL Server maintains several time zone settings:

• The server system time zone. When the server starts, it attempts to determine the time zone of the host machine and uses it to set the [system\\_time\\_zone](#page-84-2) system variable.

To explicitly specify the system time zone for MySQL Server at startup, set the TZ environment variable before you start mysqld. If you start the server using mysqld\_safe, its --timezone option provides another way to set the system time zone. The permissible values for TZ and - timezone are system dependent. Consult your operating system documentation to see what values are acceptable.

• The server current time zone. The global [time\\_zone](#page-96-0) system variable indicates the time zone the server currently is operating in. The initial [time\\_zone](#page-96-0) value is 'SYSTEM', which indicates that the server time zone is the same as the system time zone.

![](_page_191_Picture_7.jpeg)

#### **Note**

If set to SYSTEM, every MySQL function call that requires a time zone calculation makes a system library call to determine the current system time zone. This call may be protected by a global mutex, resulting in contention.

The initial global server time zone value can be specified explicitly at startup with the --defaulttime-zone option on the command line, or you can use the following line in an option file:

```
default-time-zone='timezone'
```

If you have the SYSTEM\_VARIABLES\_ADMIN privilege (or the deprecated SUPER privilege), you can set the global server time zone value at runtime with this statement:

```
SET GLOBAL time_zone = timezone;
```

• Per-session time zones. Each client that connects has its own session time zone setting, given by the session [time\\_zone](#page-96-0) variable. Initially, the session variable takes its value from the global [time\\_zone](#page-96-0) variable, but the client can change its own time zone with this statement:

```
SET time_zone = timezone;
```

The session time zone setting affects display and storage of time values that are zone-sensitive. This includes the values displayed by functions such as NOW() or CURTIME(), and values stored in and retrieved from TIMESTAMP columns. Values for TIMESTAMP columns are converted from the session time zone to UTC for storage, and from UTC to the session time zone for retrieval.

The session time zone setting does not affect values displayed by functions such as UTC\_TIMESTAMP() or values in DATE, TIME, or DATETIME columns. Nor are values in those data types stored in UTC; the time zone applies for them only when converting from TIMESTAMP values. If you want locale-specific arithmetic for DATE, TIME, or DATETIME values, convert them to UTC, perform the arithmetic, and then convert back.

The current global and session time zone values can be retrieved like this:

```
SELECT @@GLOBAL.time_zone, @@SESSION.time_zone;
```

timezone values can be given in several formats, none of which are case-sensitive:

- As the value 'SYSTEM', indicating that the server time zone is the same as the system time zone.
- As a string indicating an offset from UTC of the form [H]H:MM, prefixed with a + or -, such as '+10:00', '-6:00', or '+05:30'. A leading zero can optionally be used for hours values less

than 10; MySQL prepends a leading zero when storing and retrieving the value in such cases. MySQL converts '-00:00' or '-0:00' to '+00:00'.

This value must be in the range '-13:59' to '+14:00', inclusive.

• As a named time zone, such as 'Europe/Helsinki', 'US/Eastern', 'MET', or 'UTC'.

![](_page_192_Picture_4.jpeg)

#### **Note**

Named time zones can be used only if the time zone information tables in the mysql database have been created and populated. Otherwise, use of a named time zone results in an error:

```
mysql> SET time_zone = 'UTC';
ERROR 1298 (HY000): Unknown or incorrect time zone: 'UTC'
```

## <span id="page-192-0"></span>**Populating the Time Zone Tables**

Several tables in the mysql system schema exist to store time zone information (see Section 7.3, "The mysql System Schema"). The MySQL installation procedure creates the time zone tables, but does not load them. To do so manually, use the following instructions.

![](_page_192_Picture_10.jpeg)

#### **Note**

Loading the time zone information is not necessarily a one-time operation because the information changes occasionally. When such changes occur, applications that use the old rules become out of date and you may find it necessary to reload the time zone tables to keep the information used by your MySQL server current. See [Staying Current with Time Zone Changes.](#page-193-0)

If your system has its own zoneinfo database (the set of files describing time zones), use the mysql\_tzinfo\_to\_sql program to load the time zone tables. Examples of such systems are Linux, macOS, FreeBSD, and Solaris. One likely location for these files is the /usr/share/zoneinfo directory. If your system has no zoneinfo database, you can use a downloadable package, as described later in this section.

To load the time zone tables from the command line, pass the zoneinfo directory path name to mysql\_tzinfo\_to\_sql and send the output into the mysql program. For example:

```
mysql_tzinfo_to_sql /usr/share/zoneinfo | mysql -u root -p mysql
```

The mysql command shown here assumes that you connect to the server using an account such as root that has privileges for modifying tables in the mysql system schema. Adjust the connection parameters as required.

mysql\_tzinfo\_to\_sql reads your system's time zone files and generates SQL statements from them. mysql processes those statements to load the time zone tables.

mysql\_tzinfo\_to\_sql also can be used to load a single time zone file or generate leap second information:

• To load a single time zone file tz\_file that corresponds to a time zone name tz\_name, invoke mysql\_tzinfo\_to\_sql like this:

```
mysql_tzinfo_to_sql tz_file tz_name | mysql -u root -p mysql
```

With this approach, you must execute a separate command to load the time zone file for each named zone that the server needs to know about.

• If your time zone must account for leap seconds, initialize leap second information like this, where tz\_file is the name of your time zone file:

```
mysql_tzinfo_to_sql --leap tz_file | mysql -u root -p mysql
```

After running mysql\_tzinfo\_to\_sql, restart the server so that it does not continue to use any previously cached time zone data.

If your system has no zoneinfo database (for example, Windows), you can use a package containing SQL statements that is available for download at the MySQL Developer Zone:

<https://dev.mysql.com/downloads/timezones.html>

![](_page_193_Picture_4.jpeg)

#### **Warning**

Do not use a downloadable time zone package if your system has a zoneinfo database. Use the mysql\_tzinfo\_to\_sql utility instead. Otherwise, you may cause a difference in datetime handling between MySQL and other applications on your system.

To use an SQL-statement time zone package that you have downloaded, unpack it, then load the unpacked file contents into the time zone tables:

mysql -u root -p mysql < file\_name

Then restart the server.

![](_page_193_Picture_10.jpeg)

### **Warning**

Do not use a downloadable time zone package that contains MyISAM tables. That is intended for older MySQL versions. MySQL now uses InnoDB for the time zone tables. Trying to replace them with MyISAM tables causes problems.

# <span id="page-193-0"></span>**Staying Current with Time Zone Changes**

When time zone rules change, applications that use the old rules become out of date. To stay current, it is necessary to make sure that your system uses current time zone information is used. For MySQL, there are multiple factors to consider in staying current:

- The operating system time affects the value that the MySQL server uses for times if its time zone is set to SYSTEM. Make sure that your operating system is using the latest time zone information. For most operating systems, the latest update or service pack prepares your system for the time changes. Check the website for your operating system vendor for an update that addresses the time changes.
- If you replace the system's /etc/localtime time zone file with a version that uses rules differing from those in effect at mysqld startup, restart mysqld so that it uses the updated rules. Otherwise, mysqld might not notice when the system changes its time.
- If you use named time zones with MySQL, make sure that the time zone tables in the mysql database are up to date:
  - If your system has its own zoneinfo database, reload the MySQL time zone tables whenever the zoneinfo database is updated.
  - For systems that do not have their own zoneinfo database, check the MySQL Developer Zone for updates. When a new update is available, download it and use it to replace the content of your current time zone tables.

For instructions for both methods, see [Populating the Time Zone Tables.](#page-192-0) mysqld caches time zone information that it looks up, so after updating the time zone tables, restart mysqld to make sure that it does not continue to serve outdated time zone data.

If you are uncertain whether named time zones are available, for use either as the server's time zone setting or by clients that set their own time zone, check whether your time zone tables are empty. The following query determines whether the table that contains time zone names has any rows:

```
mysql> SELECT COUNT(*) FROM mysql.time_zone_name;
+----------+
| COUNT(*) |
+----------+
| 0 |
+----------+
```

A count of zero indicates that the table is empty. In this case, no applications currently are using named time zones, and you need not update the tables (unless you want to enable named time zone support). A count greater than zero indicates that the table is not empty and that its contents are available to be used for named time zone support. In this case, be sure to reload your time zone tables so that applications that use named time zones can obtain correct query results.

To check whether your MySQL installation is updated properly for a change in Daylight Saving Time rules, use a test like the one following. The example uses values that are appropriate for the 2007 DST 1-hour change that occurs in the United States on March 11 at 2 a.m.

The test uses this query:

```
SELECT
 CONVERT_TZ('2007-03-11 2:00:00','US/Eastern','US/Central') AS time1,
 CONVERT_TZ('2007-03-11 3:00:00','US/Eastern','US/Central') AS time2;
```

The two time values indicate the times at which the DST change occurs, and the use of named time zones requires that the time zone tables be used. The desired result is that both queries return the same result (the input time, converted to the equivalent value in the 'US/Central' time zone).

Before updating the time zone tables, you see an incorrect result like this:

```
+---------------------+---------------------+
| time1 | time2 |
+---------------------+---------------------+
| 2007-03-11 01:00:00 | 2007-03-11 02:00:00 |
+---------------------+---------------------+
```

After updating the tables, you should see the correct result:

```
+---------------------+---------------------+
| time1 | time2 |
+---------------------+---------------------+
| 2007-03-11 01:00:00 | 2007-03-11 01:00:00 |
+---------------------+---------------------+
```

## <span id="page-194-0"></span>**Time Zone Leap Second Support**

Leap second values are returned with a time part that ends with :59:59. This means that a function such as NOW() can return the same value for two or three consecutive seconds during the leap second. It remains true that literal temporal values having a time part that ends with :59:60 or :59:61 are considered invalid.

If it is necessary to search for TIMESTAMP values one second before the leap second, anomalous results may be obtained if you use a comparison with 'YYYY-MM-DD hh:mm:ss' values. The following example demonstrates this. It changes the session time zone to UTC so there is no difference between internal TIMESTAMP values (which are in UTC) and displayed values (which have time zone correction applied).

```
mysql> CREATE TABLE t1 (
 a INT,
 ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
 PRIMARY KEY (ts)
 );
Query OK, 0 rows affected (0.01 sec)
mysql> -- change to UTC
mysql> SET time_zone = '+00:00';
Query OK, 0 rows affected (0.00 sec)
```

```
mysql> -- Simulate NOW() = '2008-12-31 23:59:59'
mysql> SET timestamp = 1230767999;
Query OK, 0 rows affected (0.00 sec)
mysql> INSERT INTO t1 (a) VALUES (1);
Query OK, 1 row affected (0.00 sec)
mysql> -- Simulate NOW() = '2008-12-31 23:59:60'
mysql> SET timestamp = 1230768000;
Query OK, 0 rows affected (0.00 sec)
mysql> INSERT INTO t1 (a) VALUES (2);
Query OK, 1 row affected (0.00 sec)
mysql> -- values differ internally but display the same
mysql> SELECT a, ts, UNIX_TIMESTAMP(ts) FROM t1;
+------+---------------------+--------------------+
| a | ts | UNIX_TIMESTAMP(ts) |
+------+---------------------+--------------------+
| 1 | 2008-12-31 23:59:59 | 1230767999 |
| 2 | 2008-12-31 23:59:59 | 1230768000 |
+------+---------------------+--------------------+
2 rows in set (0.00 sec)
mysql> -- only the non-leap value matches
mysql> SELECT * FROM t1 WHERE ts = '2008-12-31 23:59:59';
+------+---------------------+
| a | ts |
+------+---------------------+
| 1 | 2008-12-31 23:59:59 |
+------+---------------------+
1 row in set (0.00 sec)
mysql> -- the leap value with seconds=60 is invalid
mysql> SELECT * FROM t1 WHERE ts = '2008-12-31 23:59:60';
Empty set, 2 warnings (0.00 sec)
```

To work around this, you can use a comparison based on the UTC value actually stored in the column, which has the leap second correction applied:

```
mysql> -- selecting using UNIX_TIMESTAMP value return leap value
mysql> SELECT * FROM t1 WHERE UNIX_TIMESTAMP(ts) = 1230768000;
+------+---------------------+
| a | ts |
+------+---------------------+
| 2 | 2008-12-31 23:59:59 |
+------+---------------------+
1 row in set (0.00 sec)
```