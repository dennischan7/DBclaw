---
source: PostgreSQL 16 Reference
title: 00_Overview
---

The planner cannot automatically determine whether a user-defined function or aggregate is parallel safe, parallel restricted, or parallel unsafe, because this would require predicting every operation that the function could possibly perform. In general, this is equivalent to the Halting Problem and therefore impossible. Even for simple functions where it could conceivably be done, we do not try, since this would be expensive and error-prone. Instead, all user-defined functions are assumed to be parallel unsafe unless otherwise marked. When using CREATE FUNCTION or ALTER FUNCTION, markings can be set by specifying PARALLEL SAFE, PARALLEL RESTRICTED, or PARALLEL UNSAFE as appropriate. When using CREATE AGGREGATE, the PARALLEL option can be specified with SAFE, RESTRICTED, or UNSAFE as the corresponding value.

Functions and aggregates must be marked PARALLEL UNSAFE if they write to the database, access sequences, change the transaction state even temporarily (e.g., a PL/pgSQL function that establishes an EXCEPTION block to catch errors), or make persistent changes to settings. Similarly, functions must be marked PARALLEL RESTRICTED if they access temporary tables, client connection state, cursors, prepared statements, or miscellaneous backend-local state that the system cannot synchronize across workers. For example, setseed and random are parallel restricted for this last reason.

In general, if a function is labeled as being safe when it is restricted or unsafe, or if it is labeled as being restricted when it is in fact unsafe, it may throw errors or produce wrong answers when used in a parallel query. C-language functions could in theory exhibit totally undefined behavior if mislabeled, since there is no way for the system to protect itself against arbitrary C code, but in most likely cases the result will be no worse than for any other function. If in doubt, it is probably best to label functions as UNSAFE.

If a function executed within a parallel worker acquires locks that are not held by the leader, for example by querying a table not referenced in the query, those locks will be released at worker exit, not end of transaction. If you write a function that does this, and this behavior difference is important to you, mark such functions as PARALLEL RESTRICTED to ensure that they execute only in the leader.

Note that the query planner does not consider deferring the evaluation of parallel-restricted functions or aggregates involved in the query in order to obtain a superior plan. So, for example, if a WHERE clause applied to a particular table is parallel restricted, the query planner will not consider performing a scan of that table in the parallel portion of a plan. In some cases, it would be possible (and perhaps even efficient) to include the scan of that table in the parallel portion of the query and defer the evaluation of the WHERE clause so that it happens above the Gather node. However, the planner does not do this.

# **Part III. Server Administration**

This part covers topics that are of interest to a PostgreSQL database administrator. This includes installation of the software, set up and configuration of the server, management of users and databases, and maintenance tasks. Anyone who runs a PostgreSQL server, even for personal use, but especially in production, should be familiar with the topics covered in this part.

The information in this part is arranged approximately in the order in which a new user should read it. But the chapters are self-contained and can be read individually as desired. The information in this part is presented in a narrative fashion in topical units. Readers looking for a complete description of a particular command should see Part VI.

The first few chapters are written so they can be understood without prerequisite knowledge, so new users who need to set up their own server can begin their exploration with this part. The rest of this part is about tuning and management; that material assumes that the reader is familiar with the general use of the PostgreSQL database system. Readers are encouraged to look at Part I and Part II for additional information.

# **Table of Contents**

| 16. Installation from Binaries                              |     |
|-------------------------------------------------------------|-----|
| 17. Installation from Source Code                           | 539 |
| 17.1. Requirements                                          | 539 |
| 17.2. Getting the Source                                    | 541 |
| 17.3. Building and Installation with Autoconf and Make      | 541 |
| 17.3.1. Short Version                                       | 541 |
| 17.3.2. Installation Procedure                              | 541 |
| 17.3.3. configure Options                                   | 544 |
| 17.3.4. configure Environment Variables                     |     |
| 17.4. Building and Installation with Meson                  |     |
| 17.4.1. Short Version                                       |     |
| 17.4.2. Installation Procedure                              |     |
| 17.4.3. meson setup Options                                 |     |
| 17.5. Post-Installation Setup                               |     |
| 17.5.1. Shared Libraries                                    |     |
| 17.5.2. Environment Variables                               |     |
| 17.6. Supported Platforms                                   |     |
| 17.7. Platform-Specific Notes                               |     |
| 17.7.1 AIX                                                  |     |
| 17.7.2. Cygwin                                              |     |
|                                                             |     |
| 17.7.4 Mi. GWAL in Wi. 1                                    |     |
| 17.7.4. MinGW/Native Windows                                |     |
| 17.7.5. Solaris                                             |     |
| 18. Installation from Source Code on Windows                |     |
| 18.1. Building with Visual C++ or the Microsoft Windows SDK |     |
| 18.1.1. Requirements                                        |     |
| 18.1.2. Special Considerations for 64-Bit Windows           |     |
| 18.1.3. Building                                            |     |
| 18.1.4. Cleaning and Installing                             |     |
| 18.1.5. Running the Regression Tests                        |     |
| 19. Server Setup and Operation                              | 576 |
| 19.1. The PostgreSQL User Account                           | 576 |
| 19.2. Creating a Database Cluster                           | 576 |
| 19.2.1. Use of Secondary File Systems                       | 578 |
| 19.2.2. File Systems                                        | 578 |
| 19.3. Starting the Database Server                          | 578 |
| 19.3.1. Server Start-up Failures                            | 580 |
| 19.3.2. Client Connection Problems                          | 581 |
| 19.4. Managing Kernel Resources                             |     |
| 19.4.1. Shared Memory and Semaphores                        |     |
| 19.4.2. systemd RemoveIPC                                   |     |
| 19.4.3. Resource Limits                                     |     |
| 19.4.4. Linux Memory Overcommit                             |     |
| 19.4.5. Linux Huge Pages                                    |     |
| 19.5. Shutting Down the Server                              |     |
| 19.6. Upgrading a PostgreSQL Cluster                        |     |
| 19.6.1. Upgrading Data via pg_dumpall                       |     |
| 19.6.2. Upgrading Data via pg_upgrade                       |     |
|                                                             |     |
| 19.6.3. Upgrading Data via Replication                      |     |
| 19.7. Preventing Server Spoofing                            |     |
| 19.8. Encryption Options                                    |     |
| 19.9. Secure TCP/IP Connections with SSL                    |     |
| 19.9.1. Basic Setup                                         |     |
| 19.9.2. OpenSSL Configuration                               |     |
| 19.9.3. Using Client Certificates                           | 596 |

| 19.9.4. SSL Server File Usage                                 |       |
|---------------------------------------------------------------|-------|
| 19.9.5. Creating Certificates                                 |       |
| 19.10. Secure TCP/IP Connections with GSSAPI Encryption       |       |
| 19.10.1. Basic Setup                                          | 599   |
| 19.11. Secure TCP/IP Connections with SSH Tunnels             | . 599 |
| 19.12. Registering Event Log on Windows                       | 600   |
| 20. Server Configuration                                      |       |
| 20.1. Setting Parameters                                      |       |
| 20.1.1. Parameter Names and Values                            |       |
| 20.1.2. Parameter Interaction via the Configuration File      |       |
| 20.1.3. Parameter Interaction via SQL                         |       |
| 20.1.4. Parameter Interaction via the Shell                   |       |
| 20.1.5. Managing Configuration File Contents                  |       |
| 20.2. File Locations                                          |       |
| 20.3. Connections and Authentication                          |       |
| 20.3.1. Connection Settings                                   |       |
| 20.3.2. TCP Settings                                          |       |
| 20.3.3. Authentication                                        |       |
| 20.3.4. SSL                                                   |       |
| 20.4. Resource Consumption                                    |       |
| 20.4.1. Memory                                                |       |
| 20.4.1. Memory 20.4.2. Disk                                   |       |
| 20.4.2. Disk 20.4.3. Kernel Resource Usage                    |       |
| 20.4.4. Cost-based Vacuum Delay                               |       |
|                                                               |       |
| 20.4.5. Background Writer                                     |       |
| 20.4.6. Asynchronous Behavior                                 |       |
| 20.5. Write Ahead Log                                         |       |
| 20.5.1. Settings                                              |       |
| 20.5.2. Checkpoints                                           |       |
| 20.5.3. Archiving                                             |       |
| 20.5.4. Recovery                                              |       |
| 20.5.5. Archive Recovery                                      |       |
| 20.5.6. Recovery Target                                       |       |
| 20.6. Replication                                             |       |
| 20.6.1. Sending Servers                                       |       |
| 20.6.2. Primary Server                                        |       |
| 20.6.3. Standby Servers                                       |       |
| 20.6.4. Subscribers                                           |       |
| 20.7. Query Planning                                          | 640   |
| 20.7.1. Planner Method Configuration                          | . 640 |
| 20.7.2. Planner Cost Constants                                | . 642 |
| 20.7.3. Genetic Query Optimizer                               | . 644 |
| 20.7.4. Other Planner Options                                 | . 645 |
| 20.8. Error Reporting and Logging                             |       |
| 20.8.1. Where to Log                                          |       |
| 20.8.2. When to Log                                           |       |
| 20.8.3. What to Log                                           |       |
| 20.8.4. Using CSV-Format Log Output                           |       |
| 20.8.5. Using JSON-Format Log Output                          |       |
| 20.8.6. Process Title                                         |       |
| 20.9. Run-time Statistics                                     |       |
| 20.9.1. Cumulative Query and Index Statistics                 |       |
| 20.9.2. Statistics Monitoring                                 |       |
| 20.10. Automatic Vacuuming                                    |       |
| 20.10. Automatic vacualing  20.11. Client Connection Defaults |       |
| 20.11.1 Statement Behavior                                    |       |
| 20.11.1. Statement Behavior                                   |       |
| 20.11.2. Eocale and Formatting                                |       |
| 20.11.3. Differed Diotary 1101044111g                         | . 013 |

| 20.11.4. Other Defaults                                              | 674 |
|----------------------------------------------------------------------|-----|
| 20.12. Lock Management                                               | 675 |
| 20.13. Version and Platform Compatibility                            | 676 |
| 20.13.1. Previous PostgreSQL Versions                                |     |
| 20.13.2. Platform and Client Compatibility                           |     |
| 20.14. Error Handling                                                |     |
| 20.15. Preset Options                                                |     |
| •                                                                    |     |
| 20.16. Customized Options                                            |     |
| 20.17. Developer Options                                             |     |
| 20.18. Short Options                                                 |     |
| 21. Client Authentication                                            |     |
| 21.1. The pg_hba.conf File                                           |     |
| 21.2. User Name Maps                                                 |     |
| 21.3. Authentication Methods                                         | 698 |
| 21.4. Trust Authentication                                           | 698 |
| 21.5. Password Authentication                                        | 699 |
| 21.6. GSSAPI Authentication                                          |     |
| 21.7. SSPI Authentication                                            |     |
| 21.8. Ident Authentication                                           |     |
| 21.9. Peer Authentication                                            |     |
| 21.10. LDAP Authentication                                           |     |
|                                                                      |     |
| 21.11. RADIUS Authentication                                         |     |
| 21.12. Certificate Authentication                                    |     |
| 21.13. PAM Authentication                                            |     |
| 21.14. BSD Authentication                                            |     |
| 21.15. Authentication Problems                                       |     |
| 22. Database Roles                                                   | 710 |
| 22.1. Database Roles                                                 | 710 |
| 22.2. Role Attributes                                                | 711 |
| 22.3. Role Membership                                                |     |
| 22.4. Dropping Roles                                                 |     |
| 22.5. Predefined Roles                                               |     |
| 22.6. Function Security                                              |     |
| 23. Managing Databases                                               |     |
| e e                                                                  |     |
| 23.1. Overview                                                       |     |
| 23.2. Creating a Database                                            |     |
| 23.3. Template Databases                                             |     |
| 23.4. Database Configuration                                         |     |
| 23.5. Destroying a Database                                          |     |
| 23.6. Tablespaces                                                    | 721 |
| 24. Localization                                                     | 724 |
| 24.1. Locale Support                                                 | 724 |
| 24.1.1. Overview                                                     | 724 |
| 24.1.2. Behavior                                                     | 725 |
| 24.1.3. Selecting Locales                                            |     |
| 24.1.4. Locale Providers                                             |     |
| 24.1.5. ICU Locales                                                  |     |
| 24.1.6. Problems                                                     |     |
| 24.2. Collation Support                                              |     |
|                                                                      |     |
| 24.2.1. Concepts                                                     |     |
| 24.2.2. Managing Collations                                          |     |
| 24.2.3. ICU Custom Collations                                        |     |
| 24.3. Character Set Support                                          |     |
| 24.3.1. Supported Character Sets                                     |     |
| 24.3.2. Setting the Character Set                                    |     |
| 24.3.3. Automatic Character Set Conversion Between Server and Client |     |
| 24.3.4. Available Character Set Conversions                          | 743 |
| 24.3.5. Further Reading                                              |     |

| 25. Routine Database Maintenance Tasks                                                                                                                                                                                                                                        | . 748                                                                     |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------|
| 25.1. Routine Vacuuming                                                                                                                                                                                                                                                       | 748                                                                       |
| 25.1.1. Vacuuming Basics                                                                                                                                                                                                                                                      | 748                                                                       |
| 25.1.2. Recovering Disk Space                                                                                                                                                                                                                                                 | 749                                                                       |
| 25.1.3. Updating Planner Statistics                                                                                                                                                                                                                                           |                                                                           |
| 25.1.4. Updating the Visibility Map                                                                                                                                                                                                                                           | 751                                                                       |
| 25.1.5. Preventing Transaction ID Wraparound Failures                                                                                                                                                                                                                         | 751                                                                       |
| 25.1.6. The Autovacuum Daemon                                                                                                                                                                                                                                                 | . 755                                                                     |
| 25.2. Routine Reindexing                                                                                                                                                                                                                                                      | 757                                                                       |
| 25.3. Log File Maintenance                                                                                                                                                                                                                                                    | 758                                                                       |
| 26. Backup and Restore                                                                                                                                                                                                                                                        |                                                                           |
| 26.1. SQL Dump                                                                                                                                                                                                                                                                |                                                                           |
| 26.1.1. Restoring the Dump                                                                                                                                                                                                                                                    |                                                                           |
| 26.1.2. Using pg dumpall                                                                                                                                                                                                                                                      |                                                                           |
| 26.1.3. Handling Large Databases                                                                                                                                                                                                                                              |                                                                           |
| 26.2. File System Level Backup                                                                                                                                                                                                                                                |                                                                           |
| 26.3. Continuous Archiving and Point-in-Time Recovery (PITR)                                                                                                                                                                                                                  |                                                                           |
| 26.3.1. Setting Up WAL Archiving                                                                                                                                                                                                                                              |                                                                           |
| 26.3.2. Making a Base Backup                                                                                                                                                                                                                                                  |                                                                           |
| 26.3.3. Making a Base Backup Using the Low Level API                                                                                                                                                                                                                          |                                                                           |
| 26.3.4. Recovering Using a Continuous Archive Backup                                                                                                                                                                                                                          |                                                                           |
| 26.3.5. Timelines                                                                                                                                                                                                                                                             |                                                                           |
| 26.3.6. Tips and Examples                                                                                                                                                                                                                                                     |                                                                           |
| 26.3.7. Caveats                                                                                                                                                                                                                                                               |                                                                           |
| 27. High Availability, Load Balancing, and Replication                                                                                                                                                                                                                        |                                                                           |
| 27.1. Comparison of Different Solutions                                                                                                                                                                                                                                       |                                                                           |
| 27.2. Log-Shipping Standby Servers                                                                                                                                                                                                                                            |                                                                           |
| 27.2.1. Planning                                                                                                                                                                                                                                                              |                                                                           |
| 27.2.2. Standby Server Operation                                                                                                                                                                                                                                              |                                                                           |
| 27.2.3. Preparing the Primary for Standby Servers                                                                                                                                                                                                                             |                                                                           |
| 27.2.4. Setting Up a Standby Server                                                                                                                                                                                                                                           |                                                                           |
| 27.2.5. Streaming Replication                                                                                                                                                                                                                                                 |                                                                           |
| 27.2.6. Replication Slots                                                                                                                                                                                                                                                     |                                                                           |
| 27.2.7. Cascading Replication                                                                                                                                                                                                                                                 |                                                                           |
| 27.2.8. Synchronous Replication                                                                                                                                                                                                                                               |                                                                           |
| 27.2.9. Continuous Archiving in Standby                                                                                                                                                                                                                                       |                                                                           |
| 27.2.9. Continuous Archiving in Standay                                                                                                                                                                                                                                       |                                                                           |
| 27.4. Hot Standby                                                                                                                                                                                                                                                             |                                                                           |
| 27.4.1. User's Overview                                                                                                                                                                                                                                                       |                                                                           |
| 27.4.1. User's Overview                                                                                                                                                                                                                                                       |                                                                           |
| 27.4.2. Handing Query Conflicts 27.4.3. Administrator's Overview                                                                                                                                                                                                              |                                                                           |
|                                                                                                                                                                                                                                                                               |                                                                           |
| 27.4.4. Hot Standby Parameter Reference                                                                                                                                                                                                                                       |                                                                           |
|                                                                                                                                                                                                                                                                               |                                                                           |
| 28. Monitoring Database Activity                                                                                                                                                                                                                                              |                                                                           |
|                                                                                                                                                                                                                                                                               |                                                                           |
| 28.2. The Cumulative Statistics System                                                                                                                                                                                                                                        | /4/                                                                       |
| 20.2.1 Statistics Callaction Configuration                                                                                                                                                                                                                                    |                                                                           |
| 28.2.1. Statistics Collection Configuration                                                                                                                                                                                                                                   | 797                                                                       |
| 28.2.2. Viewing Statistics                                                                                                                                                                                                                                                    | 797<br>798                                                                |
| 28.2.2. Viewing Statistics                                                                                                                                                                                                                                                    | 797<br>798<br>801                                                         |
| 28.2.2. Viewing Statistics                                                                                                                                                                                                                                                    | 797<br>798<br>. 801<br>. 815                                              |
| 28.2.2. Viewing Statistics                                                                                                                                                                                                                                                    | 797<br>798<br>801<br>815<br>817                                           |
| 28.2.2. Viewing Statistics  28.2.3. pg_stat_activity  28.2.4. pg_stat_replication  28.2.5. pg_stat_replication_slots  28.2.6. pg_stat_wal_receiver                                                                                                                            | 797<br>798<br>. 801<br>. 815<br>. 817                                     |
| 28.2.2. Viewing Statistics  28.2.3. pg_stat_activity  28.2.4. pg_stat_replication  28.2.5. pg_stat_replication_slots  28.2.6. pg_stat_wal_receiver  28.2.7. pg_stat_recovery_prefetch                                                                                         | 797<br>798<br>801<br>815<br>817<br>818                                    |
| 28.2.2. Viewing Statistics  28.2.3. pg_stat_activity  28.2.4. pg_stat_replication  28.2.5. pg_stat_replication_slots  28.2.6. pg_stat_wal_receiver  28.2.7. pg_stat_recovery_prefetch  28.2.8. pg_stat_subscription                                                           | 797<br>798<br>. 801<br>. 815<br>. 817<br>. 818<br>. 819                   |
| 28.2.2. Viewing Statistics  28.2.3. pg_stat_activity  28.2.4. pg_stat_replication  28.2.5. pg_stat_replication_slots  28.2.6. pg_stat_wal_receiver  28.2.7. pg_stat_recovery_prefetch  28.2.8. pg_stat_subscription  28.2.9. pg_stat_subscription_stats                       | 797<br>798<br>. 801<br>. 815<br>. 817<br>. 818<br>. 819<br>. 820          |
| 28.2.2. Viewing Statistics  28.2.3. pg_stat_activity  28.2.4. pg_stat_replication  28.2.5. pg_stat_replication_slots  28.2.6. pg_stat_wal_receiver  28.2.7. pg_stat_recovery_prefetch  28.2.8. pg_stat_subscription  28.2.9. pg_stat_subscription_stats  28.2.10. pg_stat_ssl | 797<br>798<br>. 801<br>. 815<br>. 817<br>. 818<br>. 819<br>. 820          |
| 28.2.2. Viewing Statistics  28.2.3. pg_stat_activity  28.2.4. pg_stat_replication  28.2.5. pg_stat_replication_slots  28.2.6. pg_stat_wal_receiver  28.2.7. pg_stat_recovery_prefetch  28.2.8. pg_stat_subscription  28.2.9. pg_stat_subscription_stats                       | 797<br>798<br>. 801<br>. 815<br>. 817<br>. 818<br>. 819<br>. 820<br>. 820 |

| 28.2.13. pg_stat_io                                  | 822 |
|------------------------------------------------------|-----|
| 28.2.14. pg_stat_bgwriter                            |     |
| 28.2.15. pg_stat_wal                                 | 825 |
| 28.2.16. pg_stat_database                            | 826 |
| 28.2.17. pg_stat_database_conflicts                  | 827 |
| 28.2.18. pg_stat_all_tables                          | 828 |
| 28.2.19. pg_stat_all_indexes                         | 829 |
| 28.2.20. pg_statio_all_tables                        | 830 |
| 28.2.21. pg_statio_all_indexes                       | 831 |
| 28.2.22. pg statio all sequences                     | 832 |
| 28.2.23. pg stat user functions                      | 832 |
| 28.2.24. pg stat slru                                | 832 |
| 28.2.25. Statistics Functions                        |     |
| 28.3. Viewing Locks                                  | 836 |
| 28.4. Progress Reporting                             | 836 |
| 28.4.1. ANALYZE Progress Reporting                   | 836 |
| 28.4.2. CLUSTER Progress Reporting                   |     |
| 28.4.3. COPY Progress Reporting                      |     |
| 28.4.4. CREATE INDEX Progress Reporting              |     |
| 28.4.5. VACUUM Progress Reporting                    |     |
| 28.4.6. Base Backup Progress Reporting               |     |
| 28.5. Dynamic Tracing                                |     |
| 28.5.1. Compiling for Dynamic Tracing                |     |
| 28.5.2. Built-in Probes                              |     |
| 28.5.3. Using Probes                                 |     |
| 28.5.4. Defining New Probes                          |     |
| 29. Monitoring Disk Usage                            |     |
| 29.1. Determining Disk Usage                         |     |
| 29.2. Disk Full Failure                              |     |
| 30. Reliability and the Write-Ahead Log              |     |
| 30.1. Reliability                                    |     |
| 30.2. Data Checksums                                 |     |
| 30.2.1. Off-line Enabling of Checksums               |     |
| 30.3. Write-Ahead Logging (WAL)                      |     |
| 30.4. Asynchronous Commit                            |     |
| 30.5. WAL Configuration                              |     |
| 30.6. WAL Internals                                  |     |
| 31. Logical Replication                              |     |
| 31.1. Publication                                    |     |
| 31.2. Subscription                                   |     |
| 31.2.1. Replication Slot Management                  |     |
| 31.2.2. Examples: Set Up Logical Replication         |     |
| 31.2.3. Examples: Deferred Replication Slot Creation |     |
| 31.3. Row Filters                                    |     |
| 31.3.1. Row Filter Rules                             |     |
| 31.3.2. Expression Restrictions                      |     |
| 31.3.3. UPDATE Transformations                       |     |
| 31.3.4. Partitioned Tables                           |     |
| 31.3.5. Initial Data Synchronization                 |     |
| 31.3.6. Combining Multiple Row Filters               |     |
| 31.3.7. Examples                                     |     |
| 31.4. Column Lists                                   |     |
| 31.4.1. Examples                                     |     |
| 31.5. Conflicts                                      |     |
| 31.6. Restrictions                                   |     |
| 31.7. Architecture                                   |     |
| 31.7.1. Initial Snapshot                             |     |
| •                                                    |     |
| 31.8. Monitoring                                     | 003 |

### Server Administration

| 31.9. Security                                             | 885 |
|------------------------------------------------------------|-----|
| 31.10. Configuration Settings                              | 886 |
| 31.10.1. Publishers                                        | 886 |
| 31.10.2. Subscribers                                       | 886 |
| 31.11. Quick Setup                                         | 887 |
| 32. Just-in-Time Compilation (JIT)                         | 888 |
| 32.1. What Is JIT compilation?                             | 888 |
| 32.1.1. JIT Accelerated Operations                         | 888 |
| 32.1.2. Inlining                                           | 888 |
| 32.1.3. Optimization                                       | 888 |
| 32.2. When to JIT?                                         | 888 |
| 32.3. Configuration                                        | 890 |
| 32.4. Extensibility                                        | 890 |
| 32.4.1. Inlining Support for Extensions                    | 890 |
| 32.4.2. Pluggable JIT Providers                            | 890 |
| 33. Regression Tests                                       | 891 |
| 33.1. Running the Tests                                    | 891 |
| 33.1.1. Running the Tests Against a Temporary Installation |     |
| 33.1.2. Running the Tests Against an Existing Installation | 892 |
| 33.1.3. Additional Test Suites                             | 892 |
| 33.1.4. Locale and Encoding                                | 894 |
| 33.1.5. Custom Server Settings                             |     |
| 33.1.6. Extra Tests                                        | 894 |
| 33.2. Test Evaluation                                      | 895 |
| 33.2.1. Error Message Differences                          | 895 |
| 33.2.2. Locale Differences                                 | 895 |
| 33.2.3. Date and Time Differences                          | 896 |
| 33.2.4. Floating-Point Differences                         | 896 |
| 33.2.5. Row Ordering Differences                           |     |
| 33.2.6. Insufficient Stack Depth                           |     |
| 33.2.7. The "random" Test                                  |     |
| 33.2.8. Configuration Parameters                           |     |
| 33.3. Variant Comparison Files                             |     |
| 33.4. TAP Tests                                            |     |
| 33.4.1. Environment Variables                              |     |
| 33.5. Test Coverage Examination                            |     |
| 33.5.1. Coverage with Autoconf and Make                    |     |
| 33.5.2. Coverage with Meson                                |     |

# <span id="page-175-0"></span>**Chapter 16. Installation from Binaries**

PostgreSQL is available in the form of binary packages for most common operating systems today. When available, this is the recommended way to install PostgreSQL for users of the system. Building from source (see [Chapter 17\)](#page-176-0) is only recommended for people developing PostgreSQL or extensions.

For an updated list of platforms providing binary packages, please visit the download section on the PostgreSQL website at<https://www.postgresql.org/download/> and follow the instructions for the specific platform.

# <span id="page-176-0"></span>**Chapter 17. Installation from Source Code**

This chapter describes the installation of PostgreSQL using the source code distribution. If you are installing a pre-packaged distribution, such as an RPM or Debian package, ignore this chapter and see [Chapter 16](#page-175-0) instead.

If you are building PostgreSQL for Microsoft Windows, read this chapter if you intend to build with MinGW or Cygwin; but if you intend to build with Microsoft's Visual C++, see Chapter 18 instead.

# <span id="page-176-1"></span>**17.1. Requirements**

In general, a modern Unix-compatible platform should be able to run PostgreSQL. The platforms that had received specific testing at the time of release are described in Section 17.6 below.

The following software packages are required for building PostgreSQL:

• GNU make version 3.81 or newer is required; other make programs or older GNU make versions will *not* work. (GNU make is sometimes installed under the name gmake.) To test for GNU make enter:

### **make --version**

• Alternatively, PostgreSQL can be built using [Meson](https://mesonbuild.com/)<sup>1</sup> . This is currently experimental and only works when building from a Git checkout (not from a distribution tarball). If you choose to use Meson, then you don't need GNU make, but the other requirements below still apply.

The minimum required version of Meson is 0.54.

- You need an ISO/ANSI C compiler (at least C99-compliant). Recent versions of GCC are recommended, but PostgreSQL is known to build using a wide variety of compilers from different vendors.
- tar is required to unpack the source distribution, in addition to either gzip or bzip2.
- The GNU Readline library is used by default. It allows psql (the PostgreSQL command line SQL interpreter) to remember each command you type, and allows you to use arrow keys to recall and edit previous commands. This is very helpful and is strongly recommended. If you don't want to use it then you must specify the --without-readline option to configure. As an alternative, you can often use the BSD-licensed libedit library, originally developed on NetBSD. The libedit library is GNU Readline-compatible and is used if libreadline is not found, or if --withlibedit-preferred is used as an option to configure. If you are using a package-based Linux distribution, be aware that you need both the readline and readline-devel packages, if those are separate in your distribution.
- The zlib compression library is used by default. If you don't want to use it then you must specify the --without-zlib option to configure. Using this option disables support for compressed archives in pg\_dump and pg\_restore.
- The ICU library is used by default. If you don't want to use it then you must specify the --without-icu option to configure. Using this option disables support for ICU collation features (see Section 24.2).

ICU support requires the ICU4C package to be installed. The minimum required version of ICU4C is currently 4.2.

<sup>1</sup> <https://mesonbuild.com/>

By default, pkg-config will be used to find the required compilation options. This is supported for ICU4C version 4.6 and later. For older versions, or if pkg-config is not available, the variables ICU\_CFLAGS and ICU\_LIBS can be specified to configure, like in this example:

```
./configure ... ICU_CFLAGS='-I/some/where/include' ICU_LIBS='-L/
some/where/lib -licui18n -licuuc -licudata'
```

(If ICU4C is in the default search path for the compiler, then you still need to specify nonempty strings in order to avoid use of pkg-config, for example, ICU\_CFLAGS=' '.)

The following packages are optional. They are not required in the default configuration, but they are needed when certain build options are enabled, as explained below:

• To build the server programming language PL/Perl you need a full Perl installation, including the libperl library and the header files. The minimum required version is Perl 5.14. Since PL/Perl will be a shared library, the libperl library must be a shared library also on most platforms. This appears to be the default in recent Perl versions, but it was not in earlier versions, and in any case it is the choice of whomever installed Perl at your site. configure will fail if building PL/ Perl is selected but it cannot find a shared libperl. In that case, you will have to rebuild and install Perl manually to be able to build PL/Perl. During the configuration process for Perl, request a shared library.

If you intend to make more than incidental use of PL/Perl, you should ensure that the Perl installation was built with the usemultiplicity option enabled (perl -V will show whether this is the case).

• To build the PL/Python server programming language, you need a Python installation with the header files and the sysconfig module. The minimum required version is Python 3.2.

Since PL/Python will be a shared library, the libpython library must be a shared library also on most platforms. This is not the case in a default Python installation built from source, but a shared library is available in many operating system distributions. configure will fail if building PL/ Python is selected but it cannot find a shared libpython. That might mean that you either have to install additional packages or rebuild (part of) your Python installation to provide this shared library. When building from source, run Python's configure with the --enable-shared flag.

- To build the PL/Tcl procedural language, you of course need a Tcl installation. The minimum required version is Tcl 8.4.
- To enable Native Language Support (NLS), that is, the ability to display a program's messages in a language other than English, you need an implementation of the Gettext API. Some operating systems have this built-in (e.g., Linux, NetBSD, Solaris), for other systems you can download an addon package from <https://www.gnu.org/software/gettext/>. If you are using the Gettext implementation in the GNU C library, then you will additionally need the GNU Gettext package for some utility programs. For any of the other implementations you will not need it.
- You need OpenSSL, if you want to support encrypted client connections. OpenSSL is also required for random number generation on platforms that do not have /dev/urandom (except Windows). The minimum required version is 1.0.1.
- You need MIT Kerberos (for GSSAPI), OpenLDAP, and/or PAM, if you want to support authentication using those services.
- You need LZ4, if you want to support compression of data with that method; see default\_toast\_compression and wal\_compression.
- You need Zstandard, if you want to support compression of data with that method; see wal\_compression. The minimum required version is 1.4.0.

• To build the PostgreSQL documentation, there is a separate set of requirements; see Section J.2.

If you are building from a Git tree instead of using a released source package, or if you want to do server development, you also need the following packages:

- Flex and Bison are needed to build from a Git checkout, or if you changed the actual scanner and parser definition files. If you need them, be sure to get Flex 2.5.35 or later and Bison 2.3 or later. Other lex and yacc programs cannot be used.
- Perl 5.14 or later is needed to build from a Git checkout, or if you changed the input files for any of the build steps that use Perl scripts. If building on Windows you will need Perl in any case. Perl is also required to run some test suites.

If you need to get a GNU package, you can find it at your local GNU mirror site (see [https://](https://www.gnu.org/prep/ftp) [www.gnu.org/prep/ftp](https://www.gnu.org/prep/ftp) for a list) or at <ftp://ftp.gnu.org/gnu/>.

# <span id="page-178-0"></span>**17.2. Getting the Source**

The PostgreSQL source code for released versions can be obtained from the download section of our website: <https://www.postgresql.org/ftp/source/>. Download the postgresql-version.tar.gz or postgresql-version.tar.bz2 file you're interested in, then unpack it:

```
tar xf postgresql-version.tar.bz2
```

This will create a directory postgresql-version under the current directory with the PostgreSQL sources. Change into that directory for the rest of the installation procedure.

Alternatively, you can use the Git version control system; see Section I.1 for more information.

# <span id="page-178-1"></span>**17.3. Building and Installation with Autoconf and Make**

# <span id="page-178-2"></span>**17.3.1. Short Version**

```
./configure
make
su
make install
adduser postgres
mkdir -p /usr/local/pgsql/data
chown postgres /usr/local/pgsql/data
su - postgres
/usr/local/pgsql/bin/initdb -D /usr/local/pgsql/data
/usr/local/pgsql/bin/pg_ctl -D /usr/local/pgsql/data -l logfile
 start
/usr/local/pgsql/bin/createdb test
/usr/local/pgsql/bin/psql test
```

The long version is the rest of this section.

# <span id="page-178-4"></span><span id="page-178-3"></span>**17.3.2. Installation Procedure**

1. **Configuration**

The first step of the installation procedure is to configure the source tree for your system and choose the options you would like. This is done by running the configure script. For a default installation simply enter:

### **./configure**

This script will run a number of tests to determine values for various system dependent variables and detect any quirks of your operating system, and finally will create several files in the build tree to record what it found.

You can also run configure in a directory outside the source tree, and then build there, if you want to keep the build directory separate from the original source files. This procedure is called a *VPATH* build. Here's how:

```
mkdir build_dir
cd build_dir
/path/to/source/tree/configure [options go here]
make
```

The default configuration will build the server and utilities, as well as all client applications and interfaces that require only a C compiler. All files will be installed under /usr/local/pgsql by default.

You can customize the build and installation process by supplying one or more command line options to configure. Typically you would customize the install location, or the set of optional features that are built. configure has a large number of options, which are described in [Section 17.3.3.](#page-181-0)

Also, configure responds to certain environment variables, as described in [Section 17.3.4.](#page-188-0) These provide additional ways to customize the configuration.

### 2. **Build**

To start the build, type either of:

### **make make all**

(Remember to use GNU make.) The build will take a few minutes depending on your hardware.

If you want to build everything that can be built, including the documentation (HTML and man pages), and the additional modules (contrib), type instead:

### **make world**

If you want to build everything that can be built, including the additional modules (contrib), but without the documentation, type instead:

### **make world-bin**

If you want to invoke the build from another makefile rather than manually, you must unset MAKELEVEL or set it to zero, for instance like this:

build-postgresql:

\$(MAKE) -C postgresql MAKELEVEL=0 all

Failure to do that can lead to strange error messages, typically about missing header files.

#### 3. **Regression Tests**

If you want to test the newly built server before you install it, you can run the regression tests at this point. The regression tests are a test suite to verify that PostgreSQL runs on your machine in the way the developers expected it to. Type:

#### **make check**

(This won't work as root; do it as an unprivileged user.) See Chapter 33 for detailed information about interpreting the test results. You can repeat this test at any later time by issuing the same command.

### 4. **Installing the Files**

## **Note**

If you are upgrading an existing system be sure to read Section 19.6, which has instructions about upgrading a cluster.

To install PostgreSQL enter:

### **make install**

This will install files into the directories that were specified in [Step 1.](#page-178-4) Make sure that you have appropriate permissions to write into that area. Normally you need to do this step as root. Alternatively, you can create the target directories in advance and arrange for appropriate permissions to be granted.

To install the documentation (HTML and man pages), enter:

#### **make install-docs**

If you built the world above, type instead:

### **make install-world**

This also installs the documentation.

If you built the world without the documentation above, type instead:

### **make install-world-bin**

You can use make install-strip instead of make install to strip the executable files and libraries as they are installed. This will save some space. If you built with debugging support, stripping will effectively remove the debugging support, so it should only be done if debugging is no longer needed. install-strip tries to do a reasonable job saving space, but it does not have perfect knowledge of how to strip every unneeded byte from an executable file, so if you want to save all the disk space you possibly can, you will have to do manual work.

The standard installation provides all the header files needed for client application development as well as for server-side program development, such as custom functions or data types written in C.

**Client-only installation:** If you want to install only the client applications and interface libraries, then you can use these commands:

```
make -C src/bin install
make -C src/include install
make -C src/interfaces install
make -C doc install
```

src/bin has a few binaries for server-only use, but they are small.

**Uninstallation:** To undo the installation use the command make uninstall. However, this will not remove any created directories.

**Cleaning:** After the installation you can free disk space by removing the built files from the source tree with the command make clean. This will preserve the files made by the configure program, so that you can rebuild everything with make later on. To reset the source tree to the state in which it was distributed, use make distclean. If you are going to build for several platforms within the same source tree you must do this and re-configure for each platform. (Alternatively, use a separate build tree for each platform, so that the source tree remains unmodified.)

If you perform a build and then discover that your configure options were wrong, or if you change anything that configure investigates (for example, software upgrades), then it's a good idea to do make distclean before reconfiguring and rebuilding. Without this, your changes in configuration choices might not propagate everywhere they need to.

# <span id="page-181-0"></span>**17.3.3. configure Options**

configure's command line options are explained below. This list is not exhaustive (use ./configure --help to get one that is). The options not covered here are meant for advanced use-cases such as cross-compilation, and are documented in the standard Autoconf documentation.