---
source: PostgreSQL 16 Reference
title: 00_Overview
---

Each publication can optionally specify which columns of each table are replicated to subscribers. The table on the subscriber side must have at least all the columns that are published. If no column list is specified, then all columns on the publisher are replicated. See CREATE PUBLICATION for details on the syntax.

The choice of columns can be based on behavioral or performance reasons. However, do not rely on this feature for security: a malicious subscriber is able to obtain data from columns that are not specifically published. If security is a consideration, protections can be applied at the publisher side.

If no column list is specified, any columns added to the table later are automatically replicated. This means that having a column list which names all columns is not the same as having no column list at all.

A column list can contain only simple column references. The order of columns in the list is not preserved.

Specifying a column list when the publication also publishes FOR TABLES IN SCHEMA is not supported.

For partitioned tables, the publication parameter publish\_via\_partition\_root determines which column list is used. If publish\_via\_partition\_root is true, the root partitioned table's column list is used. Otherwise, if publish\_via\_partition\_root is false (the default), each partition's column list is used.

If a publication publishes UPDATE or DELETE operations, any column list must include the table's replica identity columns (see REPLICA IDENTITY). If a publication publishes only INSERT operations, then the column list may omit replica identity columns.

Column lists have no effect for the TRUNCATE command.

During initial data synchronization, only the published columns are copied. However, if the subscriber is from a release prior to 15, then all the columns in the table are copied during initial data synchronization, ignoring any column lists.

### **Warning: Combining Column Lists from Multiple Publications**

There's currently no support for subscriptions comprising several publications where the same table has been published with different column lists. CREATE SUBSCRIPTION disallows creating such subscriptions, but it is still possible to get into that situation by adding or altering column lists on the publication side after a subscription has been created.

This means changing the column lists of tables on publications that are already subscribed could lead to errors being thrown on the subscriber side.

If a subscription is affected by this problem, the only way to resume replication is to adjust one of the column lists on the publication side so that they all match; and then either recreate the subscription, or use ALTER SUBSCRIPTION ... DROP PUBLICATION to remove one of the offending publications and add it again.