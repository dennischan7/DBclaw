---
source: MySQL 8.4 Reference
title: 00_Overview
---

The following sections describe the Performance Schema tables associated with MySQL Enterprise Firewall (see Section 8.4.7, "MySQL Enterprise Firewall"). They provide information about firewall operation:

- [firewall\\_groups](#page-109-0): Information about firewall group profiles.
- [firewall\\_group\\_allowlist](#page-110-0): Allowlist rules of registered firewall group profiles.
- [firewall\\_membership](#page-110-1): Members (accounts) of registered firewall group profiles.

### <span id="page-109-0"></span>**29.12.17.1 The firewall\_groups Table**

The [firewall\\_groups](#page-109-0) table provides a view into the in-memory data cache for MySQL Enterprise Firewall. It lists names and operational modes of registered firewall group profiles. It is used in conjunction with the mysql.firewall\_groups system table that provides persistent storage of firewall data; see MySQL Enterprise Firewall Tables.

The [firewall\\_groups](#page-109-0) table has these columns:

• NAME

The group profile name.

• MODE

The current operational mode for the profile. Permitted mode values are OFF, DETECTING, PROTECTING, and RECORDING. For details about their meanings, see Firewall Concepts.

• USERHOST

The training account for the group profile, to be used when the profile is in RECORDING mode. The value is NULL, or a non-NULL account that has the format user\_name@host\_name:

- If the value is NULL, the firewall records allowlist rules for statements received from any account that is a member of the group.
- If the value is non-NULL, the firewall records allowlist rules only for statements received from the named account (which should be a member of the group).

The [firewall\\_groups](#page-109-0) table has no indexes.

TRUNCATE TABLE is not permitted for the [firewall\\_groups](#page-109-0) table.

# <span id="page-110-0"></span>**29.12.17.2 The firewall\_group\_allowlist Table**

The [firewall\\_group\\_allowlist](#page-110-0) table provides a view into the in-memory data cache for MySQL Enterprise Firewall. It lists allowlist rules of registered firewall group profiles. It is used in conjunction with the mysql.firewall\_group\_allowlist system table that provides persistent storage of firewall data; see MySQL Enterprise Firewall Tables.

The [firewall\\_group\\_allowlist](#page-110-0) table has these columns:

• NAME

The group profile name.

• RULE

A normalized statement indicating an acceptable statement pattern for the profile. A profile allowlist is the union of its rules.

The [firewall\\_group\\_allowlist](#page-110-0) table has no indexes.

TRUNCATE TABLE is not permitted for the [firewall\\_group\\_allowlist](#page-110-0) table.

### <span id="page-110-1"></span>**29.12.17.3 The firewall\_membership Table**

The [firewall\\_membership](#page-110-1) table provides a view into the in-memory data cache for MySQL Enterprise Firewall. It lists the members (accounts) of registered firewall group profiles. It is used in conjunction with the mysql.firewall\_membership system table that provides persistent storage of firewall data; see MySQL Enterprise Firewall Tables.

The [firewall\\_membership](#page-110-1) table has these columns:

• GROUP\_ID

The group profile name.

• MEMBER\_ID

The name of an account that is a member of the profile.

The [firewall\\_membership](#page-110-1) table has no indexes.

TRUNCATE TABLE is not permitted for the [firewall\\_membership](#page-110-1) table.