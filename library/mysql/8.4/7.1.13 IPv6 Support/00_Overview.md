---
source: MySQL 8.4 Reference
title: 00_Overview
---

Support for IPv6 in MySQL includes these capabilities:

• MySQL Server can accept TCP/IP connections from clients connecting over IPv6. For example, this command connects over IPv6 to the MySQL server on the local host:

```
$> mysql -h ::1
```

To use this capability, two things must be true:

- Your system must be configured to support IPv6. See [Section 7.1.13.1, "Verifying System Support](#page-182-0) [for IPv6".](#page-182-0)
- The default MySQL server configuration permits IPv6 connections in addition to IPv4 connections. To change the default configuration, start the server with the bind\_address system variable set to an appropriate value. See Section 7.1.8, "Server System Variables".
- MySQL account names permit IPv6 addresses to enable DBAs to specify privileges for clients that connect to the server over IPv6. See Section 8.2.4, "Specifying Account Names". IPv6 addresses can be specified in account names in statements such as CREATE USER, GRANT, and REVOKE. For example:

```
mysql> CREATE USER 'bill'@'::1' IDENTIFIED BY 'secret';
mysql> GRANT SELECT ON mydb.* TO 'bill'@'::1';
```

- IPv6 functions enable conversion between string and internal format IPv6 address formats, and checking whether values represent valid IPv6 addresses. For example, INET6\_ATON() and INET6\_NTOA() are similar to INET\_ATON() and INET\_NTOA(), but handle IPv6 addresses in addition to IPv4 addresses. See Section 14.23, "Miscellaneous Functions".
- Group Replication group members can use IPv6 addresses for communications within the group. A group can contain a mix of members using IPv6 and members using IPv4. See Section 20.5.5, "Support For IPv6 And For Mixed IPv6 And IPv4 Groups".

The following sections describe how to set up MySQL so that clients can connect to the server over IPv6.

# <span id="page-182-0"></span>**7.1.13.1 Verifying System Support for IPv6**

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