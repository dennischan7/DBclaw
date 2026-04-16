---
source: MySQL 8.4 Reference
title: 00_Overview
---

At startup, InnoDB scans directories defined by the innodb\_directories variable for tablespace files. The paths of discovered tablespace files are validated against the paths recorded in the data dictionary. If the paths do not match, the paths in the data dictionary are updated.

The innodb\_validate\_tablespace\_paths variable permits disabling tablespace path validation. This feature is intended for environments where tablespaces files are not moved. Disabling path validation improves startup time on systems with a large number of tablespace files. If log\_error\_verbosity is set to 3, the following message is printed at startup when tablespace path validation is disabled:

[InnoDB] Skipping InnoDB tablespace path validation. Manually moved tablespace files will not be detected!

![](_page_46_Picture_12.jpeg)

#### **Warning**

Starting the server with tablespace path validation disabled after moving tablespace files can lead to undefined behavior.