---
source: MySQL 8.0 Reference
title: 00_Overview
---

![](_page_54_Picture_1.jpeg)

#### **Note**

The Performance Schema tables described here are available as of MySQL 8.0.23. Prior to MySQL 8.0.23, use the corresponding INFORMATION\_SCHEMA tables instead; see MySQL Enterprise Firewall Tables.

The following sections describe the Performance Schema tables associated with MySQL Enterprise Firewall (see Section 8.4.7, "MySQL Enterprise Firewall"). They provide information about firewall operation:

- [firewall\\_groups](#page-54-0): Information about firewall group profiles.
- [firewall\\_group\\_allowlist](#page-54-1): Allowlist rules of registered firewall group profiles.
- [firewall\\_membership](#page-55-0): Members (accounts) of registered firewall group profiles.

## <span id="page-54-0"></span>**29.12.17.1 The firewall\_groups Table**

The [firewall\\_groups](#page-54-0) table provides a view into the in-memory data cache for MySQL Enterprise Firewall. It lists names and operational modes of registered firewall group profiles. It is used in conjunction with the mysql.firewall\_groups system table that provides persistent storage of firewall data; see MySQL Enterprise Firewall Tables.

The [firewall\\_groups](#page-54-0) table has these columns:

• NAME

The group profile name.

• MODE

The current operational mode for the profile. Permitted mode values are OFF, DETECTING, PROTECTING, and RECORDING. For details about their meanings, see Firewall Concepts.

• USERHOST

The training account for the group profile, to be used when the profile is in RECORDING mode. The value is NULL, or a non-NULL account that has the format user\_name@host\_name:

- If the value is NULL, the firewall records allowlist rules for statements received from any account that is a member of the group.
- If the value is non-NULL, the firewall records allowlist rules only for statements received from the named account (which should be a member of the group).

The [firewall\\_groups](#page-54-0) table has no indexes.

TRUNCATE TABLE is not permitted for the [firewall\\_groups](#page-54-0) table.

The [firewall\\_groups](#page-54-0) table was added in MySQL 8.0.23.

### <span id="page-54-1"></span>**29.12.17.2 The firewall\_group\_allowlist Table**

The [firewall\\_group\\_allowlist](#page-54-1) table provides a view into the in-memory data cache for MySQL Enterprise Firewall. It lists allowlist rules of registered firewall group profiles. It is used in conjunction with the mysql.firewall\_group\_allowlist system table that provides persistent storage of firewall data; see MySQL Enterprise Firewall Tables.

The [firewall\\_group\\_allowlist](#page-54-1) table has these columns:

• NAME

The group profile name.

• RULE

A normalized statement indicating an acceptable statement pattern for the profile. A profile allowlist is the union of its rules.

The [firewall\\_group\\_allowlist](#page-54-1) table has no indexes.

TRUNCATE TABLE is not permitted for the [firewall\\_group\\_allowlist](#page-54-1) table.

The [firewall\\_group\\_allowlist](#page-54-1) table was added in MySQL 8.0.23.

## <span id="page-55-0"></span>**29.12.17.3 The firewall\_membership Table**

The [firewall\\_membership](#page-55-0) table provides a view into the in-memory data cache for MySQL Enterprise Firewall. It lists the members (accounts) of registered firewall group profiles. It is used in conjunction with the mysql.firewall\_membership system table that provides persistent storage of firewall data; see MySQL Enterprise Firewall Tables.

The [firewall\\_membership](#page-55-0) table has these columns:

• GROUP\_ID

The group profile name.

• MEMBER\_ID

The name of an account that is a member of the profile.

The [firewall\\_membership](#page-55-0) table has no indexes.

TRUNCATE TABLE is not permitted for the [firewall\\_membership](#page-55-0) table.

The [firewall\\_membership](#page-55-0) table was added in MySQL 8.0.23.