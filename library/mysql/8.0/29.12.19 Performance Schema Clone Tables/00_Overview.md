---
source: MySQL 8.0 Reference
title: 00_Overview
---

![](_page_56_Picture_22.jpeg)

#### **Note**

The Performance Schema tables described here are available as of MySQL 8.0.17.

The following sections describe the Performance Schema tables associated with the clone plugin (see Section 7.6.7, "The Clone Plugin"). The tables provide information about cloning operations.

• clone\_status: status information about the current or last executed cloning operation.

• clone\_progress: progress information about the current or last executed cloning operation.

The Performance Schema clone tables are implemented by the clone plugin and are loaded and unloaded when that plugin is loaded and unloaded (see Section 7.6.7.1, "Installing the Clone Plugin"). No special configuration step for the tables is needed. However, the tables depend on the clone plugin being enabled. If the clone plugin is loaded but disabled, the tables are not created.

The Performance Schema clone plugin tables are used only on the recipient MySQL server instance. The data is persisted across server shutdown and restart.