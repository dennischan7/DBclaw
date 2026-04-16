---
source: MySQL 8.0 Reference
title: 00_Overview
---

Support for IPv6 in MySQL includes these capabilities:

• MySQL Server can accept TCP/IP connections from clients connecting over IPv6. For example, this command connects over IPv6 to the MySQL server on the local host:

```
$> mysql -h ::1
```

To use this capability, two things must be true:

- Your system must be configured to support IPv6. See [Section 7.1.13.1, "Verifying System Support](#page-118-0) [for IPv6".](#page-118-0)
- The default MySQL server configuration permits IPv6 connections in addition to IPv4 connections. To change the default configuration, start the server with the bind\_address system variable set to an appropriate value. See Section 7.1.8, "Server System Variables".
- MySQL account names permit IPv6 addresses to enable DBAs to specify privileges for clients that connect to the server over IPv6. See Section 8.2.4, "Specifying Account Names". IPv6 addresses

can be specified in account names in statements such as CREATE USER, GRANT, and REVOKE. For example:

```
mysql> CREATE USER 'bill'@'::1' IDENTIFIED BY 'secret';
mysql> GRANT SELECT ON mydb.* TO 'bill'@'::1';
```

- IPv6 functions enable conversion between string and internal format IPv6 address formats, and checking whether values represent valid IPv6 addresses. For example, INET6\_ATON() and INET6\_NTOA() are similar to INET\_ATON() and INET\_NTOA(), but handle IPv6 addresses in addition to IPv4 addresses. See Section 14.23, "Miscellaneous Functions".
- From MySQL 8.0.14, Group Replication group members can use IPv6 addresses for communications within the group. A group can contain a mix of members using IPv6 and members using IPv4. See Section 20.5.5, "Support For IPv6 And For Mixed IPv6 And IPv4 Groups".

The following sections describe how to set up MySQL so that clients can connect to the server over IPv6.

## <span id="page-118-0"></span>**7.1.13.1 Verifying System Support for IPv6**

Before MySQL Server can accept IPv6 connections, the operating system on your server host must support IPv6. As a simple test to determine whether that is true, try this command:

```
$> ping6 ::1
16 bytes from ::1, icmp_seq=0 hlim=64 time=0.171 ms
16 bytes from ::1, icmp_seq=1 hlim=64 time=0.077 ms
...
```

To produce a description of your system's network interfaces, invoke ifconfig -a and look for IPv6 addresses in the output.

If your host does not support IPv6, consult your system documentation for instructions on enabling it. It might be that you need only reconfigure an existing network interface to add an IPv6 address. Or a more extensive change might be needed, such as rebuilding the kernel with IPv6 options enabled.

These links may be helpful in setting up IPv6 on various platforms:

- [Windows](https://msdn.microsoft.com/en-us/library/dd163569.aspx)
- [Gentoo Linux](http://www.gentoo.org/doc/en/ipv6.xml)
- [Ubuntu Linux](https://wiki.ubuntu.com/IPv6)
- [Linux \(Generic\)](http://www.tldp.org/HOWTO/Linux+IPv6-HOWTO/)
- [macOS](https://support.apple.com/en-us/HT202237)

### **7.1.13.2 Configuring the MySQL Server to Permit IPv6 Connections**

The MySQL server listens on one or more network sockets for TCP/IP connections. Each socket is bound to one address, but it is possible for an address to map onto multiple network interfaces.

Set the bind\_address system variable at server startup to specify the TCP/IP connections that a server instance accepts. As of MySQL 8.0.13, you can specify multiple values for this option, including any combination of IPv6 addresses, IPv4 addresses, and host names that resolve to IPv6 or IPv4 addresses. Alternatively, you can specify one of the wildcard address formats that permit listening on multiple network interfaces. A value of \*, which is the default, or a value of ::, permit both IPv4 and IPv6 connections on all server host IPv4 and IPv6 interfaces. For more information, see the bind\_address description in Section 7.1.8, "Server System Variables".

### **7.1.13.3 Connecting Using the IPv6 Local Host Address**

The following procedure shows how to configure MySQL to permit IPv6 connections by clients that connect to the local server using the ::1 local host address. The instructions given here assume that your system supports IPv6.

1. Start the MySQL server with an appropriate bind\_address setting to permit it to accept IPv6 connections. For example, put the following lines in the server option file and restart the server:

```
[mysqld]
bind_address = *
```

Specifying \* (or ::) as the value for bind\_address permits both IPv4 and IPv6 connections on all server host IPv4 and IPv6 interfaces. If you want to bind the server to a specific list of addresses, you can do this as of MySQL 8.0.13 by specifying a comma-separated list of values for bind\_address. This example specifies the local host addresses for both IPv4 and IPv6:

```
[mysqld]
bind_address = 127.0.0.1,::1
```

For more information, see the bind\_address description in Section 7.1.8, "Server System Variables".

2. As an administrator, connect to the server and create an account for a local user who can connect from the ::1 local IPv6 host address:

```
mysql> CREATE USER 'ipv6user'@'::1' IDENTIFIED BY 'ipv6pass';
```

For the permitted syntax of IPv6 addresses in account names, see Section 8.2.4, "Specifying Account Names". In addition to the CREATE USER statement, you can issue GRANT statements that give specific privileges to the account, although that is not necessary for the remaining steps in this procedure.

3. Invoke the mysql client to connect to the server using the new account:

```
$> mysql -h ::1 -u ipv6user -pipv6pass
```

4. Try some simple statements that show connection information:

```
mysql> STATUS
...
Connection: ::1 via TCP/IP
...
mysql> SELECT CURRENT_USER(), @@bind_address;
+----------------+----------------+
| CURRENT_USER() | @@bind_address |
+----------------+----------------+
| ipv6user@::1 | :: |
+----------------+----------------+
```

### **7.1.13.4 Connecting Using IPv6 Nonlocal Host Addresses**

The following procedure shows how to configure MySQL to permit IPv6 connections by remote clients. It is similar to the preceding procedure for local clients, but the server and client hosts are distinct and each has its own nonlocal IPv6 address. The example uses these addresses:

```
Server host: 2001:db8:0:f101::1
Client host: 2001:db8:0:f101::2
```

These addresses are chosen from the nonroutable address range recommended by [IANA](http://www.iana.org/assignments/ipv6-unicast-address-assignments/ipv6-unicast-address-assignments.xml) for documentation purposes and suffice for testing on your local network. To accept IPv6 connections from clients outside the local network, the server host must have a public address. If your network provider assigns you an IPv6 address, you can use that. Otherwise, another way to obtain an address is to use an IPv6 broker; see [Section 7.1.13.5, "Obtaining an IPv6 Address from a Broker"](#page-120-0).

1. Start the MySQL server with an appropriate bind\_address setting to permit it to accept IPv6 connections. For example, put the following lines in the server option file and restart the server:

```
[mysqld]
bind_address = *
```

Specifying \* (or ::) as the value for bind\_address permits both IPv4 and IPv6 connections on all server host IPv4 and IPv6 interfaces. If you want to bind the server to a specific list of addresses, you can do this as of MySQL 8.0.13 by specifying a comma-separated list of values for bind\_address. This example specifies an IPv4 address as well as the required server host IPv6 address:

```
[mysqld]
bind_address = 198.51.100.20,2001:db8:0:f101::1
```

For more information, see the bind\_address description in Section 7.1.8, "Server System Variables".

2. On the server host (2001:db8:0:f101::1), create an account for a user who can connect from the client host (2001:db8:0:f101::2):

```
mysql> CREATE USER 'remoteipv6user'@'2001:db8:0:f101::2' IDENTIFIED BY 'remoteipv6pass';
```

3. On the client host (2001:db8:0:f101::2), invoke the mysql client to connect to the server using the new account:

```
$> mysql -h 2001:db8:0:f101::1 -u remoteipv6user -premoteipv6pass
```

4. Try some simple statements that show connection information:

```
mysql> STATUS
...
Connection: 2001:db8:0:f101::1 via TCP/IP
...
mysql> SELECT CURRENT_USER(), @@bind_address;
+-----------------------------------+----------------+
| CURRENT_USER() | @@bind_address |
+-----------------------------------+----------------+
| remoteipv6user@2001:db8:0:f101::2 | :: |
+-----------------------------------+----------------+
```

### <span id="page-120-0"></span>**7.1.13.5 Obtaining an IPv6 Address from a Broker**

If you do not have a public IPv6 address that enables your system to communicate over IPv6 outside your local network, you can obtain one from an IPv6 broker. The [Wikipedia IPv6 Tunnel Broker](http://en.wikipedia.org/wiki/List_of_IPv6_tunnel_brokers) [page](http://en.wikipedia.org/wiki/List_of_IPv6_tunnel_brokers) lists several brokers and their features, such as whether they provide static addresses and the supported routing protocols.

After configuring your server host to use a broker-supplied IPv6 address, start the MySQL server with an appropriate bind\_address setting to permit the server to accept IPv6 connections. You can specify \* (or ::) as the bind\_address value, or bind the server to the specific IPv6 address provided by the broker. For more information, see the bind\_address description in Section 7.1.8, "Server System Variables".

Note that if the broker allocates dynamic addresses, the address provided for your system might change the next time you connect to the broker. If so, any accounts you create that name the original address become invalid. To bind to a specific address but avoid this change-of-address problem, you might be able to arrange with the broker for a static IPv6 address.

The following example shows how to use Freenet6 as the broker and the gogoc IPv6 client package on Gentoo Linux.

1. Create an account at Freenet6 by visiting this URL and signing up:

```
http://gogonet.gogo6.com
```

2. After creating the account, go to this URL, sign in, and create a user ID and password for the IPv6 broker:

<http://gogonet.gogo6.com/page/freenet6-registration>

3. As root, install gogoc:

```
$> emerge gogoc
```

4. Edit /etc/gogoc/gogoc.conf to set the userid and password values. For example:

```
userid=gogouser
passwd=gogopass
```

5. Start gogoc:

```
$> /etc/init.d/gogoc start
```

To start gogoc each time your system boots, execute this command:

```
$> rc-update add gogoc default
```

6. Use ping6 to try to ping a host:

```
$> ping6 ipv6.google.com
```

7. To see your IPv6 address:

```
$> ifconfig tun
```