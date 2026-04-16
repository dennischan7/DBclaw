---
source: MySQL 8.4 Reference
title: 00_Overview
---

The InnoDB master thread and other threads perform various tasks in the background, most of which are I/O related, such as flushing dirty pages from the buffer pool and writing changes from the change buffer to the appropriate secondary indexes. InnoDB attempts to perform these tasks in a way that does not adversely affect the normal working of the server. It tries to estimate the available I/O bandwidth and tune its activities to take advantage of available capacity.

The innodb\_io\_capacity variable defines the overall I/O capacity available to InnoDB. It should be set to approximately the number of I/O operations that the system can perform per second (IOPS). When innodb\_io\_capacity is set, InnoDB estimates the I/O bandwidth available for background tasks based on the set value.

You can set innodb\_io\_capacity to a value of 100 or greater. The default value is 10000. Typically, faster hard drives, RAID configurations, and solid state drives (SSDs) benefit from higher values than do lower-end storage devices, such as hard drives up to 7200 RPMs.

Ideally, keep the setting as low as practical, but not so low that background activities fall behind. If the value is too high, data is removed from the buffer pool and change buffer too quickly for caching to provide a significant benefit. For busy systems capable of higher I/O rates, you can set a higher value to help the server handle the background maintenance work associated with a high rate of row changes. Generally, you can increase the value as a function of the number of drives used for InnoDB I/O. For example, you can increase the value on systems that use multiple disks or SSDs.

Although you can specify a high value such as a million, in practice such large values have little benefit. Generally, a value higher than 20000 is not recommended unless you are certain that lower values are insufficient for your workload. See also the innodb\_io\_capacity\_max option that automatically increases this value when flushing falls behind.

Consider write workload when tuning innodb\_io\_capacity. Systems with large write workloads are likely to benefit from a higher setting. A lower setting may be sufficient for systems with a small write workload.

The innodb\_io\_capacity setting is not a per buffer pool instance setting. Available I/O capacity is distributed equally among buffer pool instances for flushing activities.

You can set the innodb\_io\_capacity value in the MySQL option file (my.cnf or my.ini) or modify it at runtime using a SET GLOBAL statement, which requires privileges sufficient to set global system variables. See Section 7.1.9.1, "System Variable Privileges".

## **Ignoring I/O Capacity at Checkpoints**

The innodb\_flush\_sync variable, which is enabled by default, causes the innodb\_io\_capacity setting to be ignored during bursts of I/O activity that occur at checkpoints. To adhere to the I/O rate defined by the innodb\_io\_capacity and innodb\_io\_capacity\_max settings, disable innodb\_flush\_sync.

You can set the innodb\_flush\_sync value in the MySQL option file (my.cnf or my.ini) or modify it at runtime using a SET GLOBAL statement, which requires privileges sufficient to set global system variables. See Section 7.1.9.1, "System Variable Privileges".

## **Configuring an I/O Capacity Maximum**

If flushing activity falls behind, InnoDB can flush more aggressively, at a higher rate of I/ O operations per second (IOPS) than defined by the innodb\_io\_capacity variable. The innodb\_io\_capacity\_max variable defines a maximum number of IOPS performed by InnoDB background tasks in such situations.

If you specify an innodb\_io\_capacity setting at startup but do not specify a value for innodb\_io\_capacity\_max, innodb\_io\_capacity\_max defaults to twice the value of innodb\_io\_capacity.

When configuring innodb\_io\_capacity\_max, twice the innodb\_io\_capacity is often a good starting point. As with the innodb\_io\_capacity setting, keep the setting as low as practical, but not so low that InnoDB cannot sufficiently extend rate of IOPS beyond the innodb\_io\_capacity setting.

Consider write workload when tuning innodb\_io\_capacity\_max. Systems with large write workloads may benefit from a higher setting. A lower setting may be sufficient for systems with a small write workload.

innodb\_io\_capacity\_max cannot be set to a value lower than the innodb\_io\_capacity value.

Setting innodb\_io\_capacity\_max to DEFAULT using a SET statement (SET GLOBAL innodb\_io\_capacity\_max=DEFAULT) sets innodb\_io\_capacity\_max to the default value. Before MySQL 8.4, this set it to the maximum value instead of the default value.

The innodb\_io\_capacity\_max limit applies to all buffer pool instances. It is not a per buffer pool instance setting.