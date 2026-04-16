---
source: MySQL 8.4 Reference
title: 00_Overview
---

MySQL Enterprise Data Masking and De-Identification implements these elements:

- A table for persistent storage of dictionaries and terms.
- A component named component\_masking that implements masking functionality and exposes it as service interface for developers.

Developers who wish to incorporate the same service functions used by component\_masking should consult the internal\components\masking\component\_masking.h file in a MySQL source distribution or https://dev.mysql.com/doc/dev/mysql-server/latest.

• A component named component\_masking\_functions that provides loadable functions.

The set of loadable functions enables an SQL-level API for performing masking and de-identification operations. Some of the functions require the MASKING\_DICTIONARIES\_ADMIN dynamic privilege.

## <span id="page-181-1"></span>**8.5.2.1 MySQL Enterprise Data Masking and De-Identification Component Installation**

Components provide expanded access to MySQL Enterprise Data Masking and De-Identification functionality. Previously, MySQL implemented masking and de-identification capabilities as a plugin library file containing a plugin and several loadable functions. Before you begin the component installation, remove the data\_masking plugin and all of its loadable functions to avoid conflicts. For instructions, see Section 8.5.3.1, "MySQL Enterprise Data Masking and De-Identification Plugin Installation".

MySQL Enterprise Data Masking and De-Identification database table and components are:

• masking\_dictionaries table

Purpose: A table that provides persistent storage for masking dictionaries and terms. While the mysql system schema is the traditional storage option, creating a dedicated schema for this purpose is also permitted. A dedicated schema might be preferable for these reasons:

- The mysql system schema is not backed up by a logical backup, such as mysqldump or load operations.
- A dedicated schema makes outbound replication easier.
- A user or role requires no mysql schema privileges when preforming related data-masking tasks in the dedicated schema.
- component\_masking component

Purpose: The component implements the core of the masking functionality and exposes it as services.

URN: file://component\_masking

• component\_masking\_functions component

Purpose: The component exposes all functionality of the component\_masking component as loadable functions. Some of the functions require the MASKING\_DICTIONARIES\_ADMIN dynamic privilege.

```
URN: file://component_masking_functions
```

If the components and functions are used on a replication source server, install them on all replica servers as well to avoid replication issues. While the components are loaded, information about them is available as described in Section 7.5.2, "Obtaining Component Information". For general information about installing or uninstalling components, see Section 7.5.1, "Installing and Uninstalling Components".

MySQL Enterprise Data Masking and De-Identification supports these setup and removal procedures:

- [Install Using the mysql System Schema](#page-181-0)
- [Install Using a Dedicated Schema](#page-182-0)
- [Uninstall MySQL Enterprise Data Masking and De-Identification Components](#page-182-1)

## <span id="page-181-0"></span>**Install Using the mysql System Schema**

![](_page_181_Picture_21.jpeg)

#### **Note**

Consider using a dedicated schema to store data-masking dictionaries (see [Install Using a Dedicated Schema](#page-182-0)).

To set up MySQL Enterprise Data Masking and De-Identification:

1. Run masking\_functions\_install.sql to add the masking\_dictionaries table to the mysql schema and install the components. The script is located in the share directory of your MySQL installation.

```
$> mysql -u root -p -D mysql < [path/]masking_functions_install.sql
Enter password: (enter root password here)
```

## <span id="page-182-0"></span>**Install Using a Dedicated Schema**

To set up MySQL Enterprise Data Masking and De-Identification:

1. Create a database to store the masking\_dictionaries table. For example, to use mask\_db as the database name, execute this statement:

```
$> mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS mask_db"
Enter password: (enter root password here)
```

2. Run masking\_functions\_install.sql to add the masking\_dictionaries table to the mask\_db schema and install the components. The script is located in the share directory of your MySQL installation.

```
$> mysql -u root -p -D mask_db < [path/]masking_functions_install.sql
Enter password: (enter root password here)
```

3. Set and persist the mask\_db schema at startup by preceding the component\_masking.masking\_database read-only variable name by the PERSIST\_ONLY keyword.

```
$> mysql -u root -p -e "SET PERSIST_ONLY component_masking.masking_database=mask_db"
Enter password: (enter root password here)
```

After modifying the variable, restart the server to cause the new setting to take effect.

## <span id="page-182-1"></span>**Uninstall MySQL Enterprise Data Masking and De-Identification Components**

To remove MySQL Enterprise Data Masking and De-Identification when using the mysql system schema:

1. Run masking\_functions\_uninstall.sql to remove the masking\_dictionaries table from the appropriate schema and uninstall the components. The script is located in the share directory of your MySQL installation. The example here specifies the mysql database.

```
$> mysql -u root -p -D mysql < [path/]masking_functions_uninstall.sql
Enter password: (enter root password here)
```

To remove MySQL Enterprise Data Masking and De-Identification when using a dedicated schema:

1. Run masking\_functions\_uninstall.sql to remove the masking\_dictionaries table from the appropriate schema and uninstall the components. The script is located in the share directory of your MySQL installation. The example here specifies the mask\_db database.

```
$> mysql -u root -p -D mask_db < [path/]masking_functions_uninstall.sql
Enter password: (enter root password here)
```

2. Stop persisting the component\_masking.masking\_database variable.

```
$> mysql -u root -p -e "RESET PERSIST component_masking.masking_database"
Enter password: (enter root password here)
```

3. [Optional] Drop the dedicated schema to ensure that it is not used for other purposes.

```
DROP DATABASE mask_db;
```