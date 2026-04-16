---
source: PostgreSQL 15 Reference
title: 00_Overview
---

PostgreSQL, like any database software, requires that certain tasks be performed regularly to achieve optimum performance. The tasks discussed here are *required*, but they are repetitive in nature and can easily be automated using standard tools such as cron scripts or Windows' Task Scheduler. It is the database administrator's responsibility to set up appropriate scripts, and to check that they execute successfully.

One obvious maintenance task is the creation of backup copies of the data on a regular schedule. Without a recent backup, you have no chance of recovery after a catastrophe (disk failure, fire, mistakenly dropping a critical table, etc.). The backup and recovery mechanisms available in PostgreSQL are discussed at length in [Chapter 26](#page-171-0).

The other main category of maintenance task is periodic "vacuuming" of the database. This activity is discussed in [Section 25.1.](#page-159-0) Closely related to this is updating the statistics that will be used by the query planner, as discussed in [Section 25.1.3.](#page-161-0)

Another task that might need periodic attention is log file management. This is discussed in [Sec](#page-169-0)[tion 25.3.](#page-169-0)

[check\\_postgres](https://bucardo.org/check_postgres/)<sup>1</sup> is available for monitoring database health and reporting unusual conditions. check\_postgres integrates with Nagios and MRTG, but can be run standalone too.

PostgreSQL is low-maintenance compared to some other database management systems. Nonetheless, appropriate attention to these tasks will go far towards ensuring a pleasant and productive experience with the system.

# <span id="page-159-0"></span>**25.1. Routine Vacuuming**

PostgreSQL databases require periodic maintenance known as *vacuuming*. For many installations, it is sufficient to let vacuuming be performed by the *autovacuum daemon*, which is described in [Sec](#page-166-0)[tion 25.1.6.](#page-166-0) You might need to adjust the autovacuuming parameters described there to obtain best results for your situation. Some database administrators will want to supplement or replace the daemon's activities with manually-managed VACUUM commands, which typically are executed according to a schedule by cron or Task Scheduler scripts. To set up manually-managed vacuuming properly, it is essential to understand the issues discussed in the next few subsections. Administrators who rely on autovacuuming may still wish to skim this material to help them understand and adjust autovacuuming.