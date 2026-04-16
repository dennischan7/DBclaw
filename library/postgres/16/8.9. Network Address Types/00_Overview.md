---
source: PostgreSQL 16 Reference
title: 00_Overview
---

PostgreSQL offers data types to store IPv4, IPv6, and MAC addresses, as shown in [Table 8.21](#page-9-0). It is better to use these types instead of plain text types to store network addresses, because these types offer input error checking and specialized operators and functions (see [Section 9.12](#page-135-0)).

<span id="page-9-0"></span>**Table 8.21. Network Address Types**

| Name     | Storage Size  | Description                      |
|----------|---------------|----------------------------------|
| cidr     | 7 or 19 bytes | IPv4 and IPv6 networks           |
| inet     | 7 or 19 bytes | IPv4 and IPv6 hosts and networks |
| macaddr  | 6 bytes       | MAC addresses                    |
| macaddr8 | 8 bytes       | MAC addresses (EUI-64 format)    |

When sorting inet or cidr data types, IPv4 addresses will always sort before IPv6 addresses, including IPv4 addresses encapsulated or mapped to IPv6 addresses, such as ::10.2.3.4 or ::ffff:10.4.3.2.