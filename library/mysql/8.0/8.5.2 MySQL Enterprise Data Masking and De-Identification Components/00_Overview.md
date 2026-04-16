---
source: MySQL 8.0 Reference
title: 00_Overview
---

MySQL Enterprise Data Masking and De-Identification implements these elements:

- A table in the mysql system database for persistent storage of dictionaries and terms.
- A component named component\_masking that implements masking functionality and exposes it as service interface for developers.

Developers who wish to incorporate the same service functions used by component\_masking should consult the internal\components\masking\component\_masking.h file in a MySQL source distribution or https://dev.mysql.com/doc/dev/mysql-server/latest.

• A component named component\_masking\_functions that provides loadable functions.

The set of loadable functions enables an SQL-level API for performing masking and de-identification operations. Some of the functions require the MASKING\_DICTIONARIES\_ADMIN dynamic privilege.

## <span id="page-133-1"></span>**8.5.2.1 MySQL Enterprise Data Masking and De-Identification Component Installation**

As of MySQL 8.0.33, components provide access to MySQL Enterprise Data Masking and De-Identification functionality. Previously, MySQL implemented masking and de-identification capabilities as a plugin library file containing a plugin and several loadable functions. Before you begin the component installation, remove the data\_masking plugin and all of its loadable functions to avoid conflicts. For instructions, see [Section 8.5.3.1, "MySQL Enterprise Data Masking and De-Identification](#page-156-0) [Plugin Installation".](#page-156-0)

MySQL Enterprise Data Masking and De-Identification database table and components are:

• masking\_dictionaries table

Purpose: A table in the mysql system schema that provides persistent storage of dictionaries and terms.

• component\_masking component

Purpose: The component implements the core of the masking functionality and exposes it as services.

```
URN: file://component_masking
```

• component\_masking\_functions component

Purpose: The component exposes all functionality of the component\_masking component as loadable functions. Some of the functions require the MASKING\_DICTIONARIES\_ADMIN dynamic privilege.

```
URN: file://component_masking_functions
```

To set up MySQL Enterprise Data Masking and De-Identification, do the following:

1. Create the masking\_dictionaries table.

```
CREATE TABLE IF NOT EXISTS
mysql.masking_dictionaries(
 Dictionary VARCHAR(256) NOT NULL,
 Term VARCHAR(256) NOT NULL,
 UNIQUE INDEX dictionary_term_idx (Dictionary, Term),
 INDEX dictionary_idx (Dictionary)
) ENGINE = InnoDB DEFAULT CHARSET=utf8mb4;
```

2. Use the INSTALL COMPONENT SQL statement to install data masking components.

```
INSTALL COMPONENT 'file://component_masking';
INSTALL COMPONENT 'file://component_masking_functions';
```

If the components and functions are used on a replication source server, install them on all replica servers as well to avoid replication issues. While the components are loaded, information about them is available as described in Section 7.5.2, "Obtaining Component Information".

To remove MySQL Enterprise Data Masking and De-Identification, do the following:

1. Use the UNINSTALL COMPONENT SQL statement to uninstall the data masking components.

```
UNINSTALL COMPONENT 'file://component_masking_functions';
UNINSTALL COMPONENT 'file://component_masking';
```

2. Drop the masking\_dictionaries table.

```
DROP TABLE mysql.masking_dictionaries;
```

component\_masking\_functions installs all of the related loadable functions automatically. Similarly, the component when uninstalled also automatically uninstalls those functions. For general information about installing or uninstalling components, see Section 7.5.1, "Installing and Uninstalling Components".