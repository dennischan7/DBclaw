---
source: MySQL 8.0 Reference
title: 00_Overview
---

MySQL includes several components and plugins that implement security features:

- Plugins for authenticating attempts by clients to connect to MySQL Server. Plugins are available for several authentication protocols. For general discussion of the authentication process, see Section 8.2.17, "Pluggable Authentication". For characteristics of specific authentication plugins, see [Section 8.4.1, "Authentication Plugins".](#page-37-0)
- A password-validation component for implementing password strength policies and assessing the strength of potential passwords. See [Section 8.4.3, "The Password Validation Component"](#page-131-0).
- Keyring plugins that provide secure storage for sensitive information. See [Section 8.4.4, "The](#page-143-0) [MySQL Keyring"](#page-143-0).
- (MySQL Enterprise Edition only) MySQL Enterprise Audit, implemented using a server plugin, uses the open MySQL Audit API to enable standard, policy-based monitoring and logging of connection and query activity executed on specific MySQL servers. Designed to meet the Oracle audit specification, MySQL Enterprise Audit provides an out of box, easy to use auditing and compliance solution for applications that are governed by both internal and external regulatory guidelines. See Section 8.4.5, "MySQL Enterprise Audit".
- A function enables applications to add their own message events to the audit log. See Section 8.4.6, "The Audit Message Component".
- (MySQL Enterprise Edition only) MySQL Enterprise Firewall, an application-level firewall that enables database administrators to permit or deny SQL statement execution based on matching against lists of accepted statement patterns. This helps harden MySQL Server against attacks such as SQL injection or attempts to exploit applications by using them outside of their legitimate query workload characteristics. See Section 8.4.7, "MySQL Enterprise Firewall".

• (MySQL Enterprise Edition only) MySQL Enterprise Data Masking and De-Identification, implemented as a plugin library containing a plugin and a set of functions. Data masking hides sensitive information by replacing real values with substitutes. MySQL Enterprise Data Masking and De-Identification functions enable masking existing data using several methods such as obfuscation (removing identifying characteristics), generation of formatted random data, and data replacement or substitution. See Section 8.5, "MySQL Enterprise Data Masking and De-Identification".

# <span id="page-37-0"></span>**8.4.1 Authentication Plugins**

![](_page_37_Picture_3.jpeg)

### **Note**

If you are looking for information about the authentication\_oci plugin, it is MySQL HeatWave Service only. See [authentication\\_oci plugin](https://docs.oracle.com/en-us/iaas/mysql-database/doc/connecting-db-system.md#MYAAS-GUID-232CA959-1FDD-4AA8-A77D-0A551C881C09), in the MySQL HeatWave Service manual.

The following sections describe pluggable authentication methods available in MySQL and the plugins that implement these methods. For general discussion of the authentication process, see Section 8.2.17, "Pluggable Authentication".

The default authentication plugin is determined as described in The Default Authentication Plugin.