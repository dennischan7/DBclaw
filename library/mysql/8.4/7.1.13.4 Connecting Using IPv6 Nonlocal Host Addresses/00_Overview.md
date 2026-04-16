---
source: MySQL 8.4 Reference
title: 00_Overview
---

The following procedure shows how to configure MySQL to permit IPv6 connections by remote clients. It is similar to the preceding procedure for local clients, but the server and client hosts are distinct and each has its own nonlocal IPv6 address. The example uses these addresses:

```
Server host: 2001:db8:0:f101::1
Client host: 2001:db8:0:f101::2
```

These addresses are chosen from the nonroutable address range recommended by [IANA](http://www.iana.org/assignments/ipv6-unicast-address-assignments/ipv6-unicast-address-assignments.xml) for documentation purposes and suffice for testing on your local network. To accept IPv6 connections from clients outside the local network, the server host must have a public address. If your network provider assigns you an IPv6 address, you can use that. Otherwise, another way to obtain an address is to use an IPv6 broker; see [Section 7.1.13.5, "Obtaining an IPv6 Address from a Broker"](#page-184-0).

1. Start the MySQL server with an appropriate bind\_address setting to permit it to accept IPv6 connections. For example, put the following lines in the server option file and restart the server:

```
[mysqld]
bind_address = *
```

Specifying \* (or ::) as the value for bind\_address permits both IPv4 and IPv6 connections on all server host IPv4 and IPv6 interfaces. If you want to bind the server to a specific list of addresses, you can do this by specifying a comma-separated list of values for bind\_address. This example specifies an IPv4 address as well as the required server host IPv6 address:

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

## <span id="page-184-0"></span>**7.1.13.5 Obtaining an IPv6 Address from a Broker**

If you do not have a public IPv6 address that enables your system to communicate over IPv6 outside your local network, you can obtain one from an IPv6 broker. The [Wikipedia IPv6 Tunnel Broker](http://en.wikipedia.org/wiki/List_of_IPv6_tunnel_brokers) [page](http://en.wikipedia.org/wiki/List_of_IPv6_tunnel_brokers) lists several brokers and their features, such as whether they provide static addresses and the supported routing protocols.

After configuring your server host to use a broker-supplied IPv6 address, start the MySQL server with an appropriate bind\_address setting to permit the server to accept IPv6 connections. You can specify \* (or ::) as the bind\_address value, or bind the server to the specific IPv6 address provided by the broker. For more information, see the bind\_address description in Section 7.1.8, "Server System Variables".

Note that if the broker allocates dynamic addresses, the address provided for your system might change the next time you connect to the broker. If so, any accounts you create that name the original address become invalid. To bind to a specific address but avoid this change-of-address problem, you might be able to arrange with the broker for a static IPv6 address.

The following example shows how to use Freenet6 as the broker and the gogoc IPv6 client package on Gentoo Linux.

1. Create an account at Freenet6 by visiting this URL and signing up:

```
http://gogonet.gogo6.com
```

2. After creating the account, go to this URL, sign in, and create a user ID and password for the IPv6 broker:

```
http://gogonet.gogo6.com/page/freenet6-registration
```

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