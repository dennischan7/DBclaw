---
source: MySQL 8.4 Reference
title: 00_Overview
---

The following sections describe the Performance Schema tables associated with the MySQL keyring (see Section 8.4.4, "The MySQL Keyring"). They provide information about keyring operation:

- [keyring\\_component\\_status](#page-111-0): Information about the keyring component in use.
- [keyring\\_keys](#page-111-1): Metadata for keys in the MySQL keyring.

### <span id="page-111-0"></span>**29.12.18.1 The keyring\_component\_status Table**

The [keyring\\_component\\_status](#page-111-0) table provides status information about the properties of the keyring component in use, if one is installed. The table is empty if no keyring component is installed (for example, if the keyring is not being used, or is configured to manage the keystore using a keyring plugin rather than a keyring component).

There is no fixed set of properties. Each keyring component is free to define its own set.

Example [keyring\\_component\\_status](#page-111-0) contents:

```
mysql> SELECT * FROM performance_schema.keyring_component_status;
+---------------------+-------------------------------------------------+
| STATUS_KEY | STATUS_VALUE |
+---------------------+-------------------------------------------------+
| Component_name | component_keyring_file |
| Author | Oracle Corporation |
| License | GPL |
| Implementation_name | component_keyring_file |
| Version | 1.0 |
| Component_status | Active |
| Data_file | /usr/local/mysql/keyring/component_keyring_file |
| Read_only | No |
+---------------------+-------------------------------------------------+
```

The [keyring\\_component\\_status](#page-111-0) table has these columns:

• STATUS\_KEY

The status item name.

• STATUS\_VALUE

The status item value.

The [keyring\\_component\\_status](#page-111-0) table has no indexes.

TRUNCATE TABLE is not permitted for the [keyring\\_component\\_status](#page-111-0) table.

### <span id="page-111-1"></span>**29.12.18.2 The keyring\_keys table**

MySQL Server supports a keyring that enables internal server components and plugins to securely store sensitive information for later retrieval. See Section 8.4.4, "The MySQL Keyring".

The [keyring\\_keys](#page-111-1) table exposes metadata for keys in the keyring. Key metadata includes key IDs, key owners, and backend key IDs. The [keyring\\_keys](#page-111-1) table does not expose any sensitive keyring data such as key contents.

The [keyring\\_keys](#page-111-1) table has these columns:

• KEY\_ID

The key identifier.

• KEY\_OWNER

The owner of the key.

• BACKEND\_KEY\_ID

The ID used for the key by the keyring backend.

The [keyring\\_keys](#page-111-1) table has no indexes.

TRUNCATE TABLE is not permitted for the [keyring\\_keys](#page-111-1) table.