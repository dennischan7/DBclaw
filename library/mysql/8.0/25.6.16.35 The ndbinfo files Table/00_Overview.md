---
source: MySQL 8.0 Reference
title: 00_Overview
---

The files tables provides information about files and other objects used by NDB disk data tables, and contains the columns listed here:

• id

Object ID

• type

The type of object; one of Log file group, Tablespace, Undo file, or Data file

• name

The name of the object

• parent

ID of the parent object

• parent\_name

Name of the parent object

• free\_extents

Number of free extents

• total\_extents

Total number of extents

• extent\_size

Extent size (MB)

• initial\_size

Initial size (bytes)

• maximum\_size

Maximum size (bytes)

• autoextend\_size

Autoextend size (bytes)

For log file groups and tablespaces, parent is always 0, and the parent\_name, free\_extents, total\_extents, extent\_size, initial\_size, maximum\_size, and autoentend\_size columns are all NULL.

The files table is empty if no disk data objects have been created in NDB. See [Section 25.6.11.1,](#page-101-0) ["NDB Cluster Disk Data Objects"](#page-101-0), for more information.

The files table was added in NDB 8.0.29.

See also Section 28.3.15, "The INFORMATION\_SCHEMA FILES Table".