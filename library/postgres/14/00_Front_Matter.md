---
source: PostgreSQL 14 Reference
title: 00_Front_Matter
---

# **PostgreSQL 14.22 Documentation**

**The PostgreSQL Global Development Group**

### **PostgreSQL 14.22 Documentation**

The PostgreSQL Global Development Group Copyright © 1996–2026 The PostgreSQL Global Development Group

#### **Legal Notice**

PostgreSQL Database Management System (also known as Postgres, formerly known as Postgres95)

Portions Copyright © 1996-2026, PostgreSQL Global Development Group

Portions Copyright © 1994, The Regents of the University of California

Permission to use, copy, modify, and distribute this software and its documentation for any purpose, without fee, and without a written agreement is hereby granted, provided that the above copyright notice and this paragraph and the following two paragraphs appear in all copies.

IN NO EVENT SHALL THE UNIVERSITY OF CALIFORNIA BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS, ARISING OUT OF THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF THE UNIVERSITY OF CALIFORNIA HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

THE UNIVERSITY OF CALIFORNIA SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. THE SOFTWARE PROVIDED HEREUNDER IS ON AN "AS-IS" BASIS, AND THE UNIVERSITY OF CALIFORNIA HAS NO OBLIGATIONS TO PROVIDE MAIN-TENANCE, SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS.

## **Table of Contents**

| Preface                            |       |
|------------------------------------|-------|
| 1. What Is PostgreSQL?             | xxxii |
| 2. A Brief History of PostgreSQL   |       |
| 2.1. The Berkeley POSTGRES Project |       |
| 2.2. Postgres95x                   |       |
| 2.3. PostgreSQL                    |       |
| 3. Conventions                     |       |
| 4. Further Information             |       |
| 5. Bug Reporting Guidelines        |       |
| 5.1. Identifying Bugs              |       |
| 5.2. What to Report                |       |
| 5.3. Where to Report Bugs          |       |
| I. Tutorial                        |       |
| 1. Getting Started                 |       |
| 1.1. Installation                  |       |
| 1.2. Architectural Fundamentals    |       |
| 1.3. Creating a Database           |       |
|                                    |       |
| 1.4. Accessing a Database          |       |
| 2. The SQL Language                |       |
| 2.1. Introduction                  |       |
| 2.2. Concepts                      |       |
| 2.3. Creating a New Table          |       |
| 2.4. Populating a Table With Rows  |       |
| 2.5. Querying a Table              |       |
| 2.6. Joins Between Tables          |       |
| 2.7. Aggregate Functions           |       |
| 2.8. Updates                       |       |
| 2.9. Deletions                     |       |
| 3. Advanced Features               |       |
| 3.1. Introduction                  |       |
| 3.2. Views                         |       |
| 3.3. Foreign Keys                  | 17    |
| 3.4. Transactions                  | 18    |
| 3.5. Window Functions              | 20    |
| 3.6. Inheritance                   | 23    |
| 3.7. Conclusion                    | 24    |
| II. The SQL Language               | 25    |
| 4. SQL Syntax                      | 33    |
| 4.1. Lexical Structure             | 33    |
| 4.2. Value Expressions             | 42    |
| 4.3. Calling Functions             | 55    |
| 5. Data Definition                 |       |
| 5.1. Table Basics                  |       |
| 5.2. Default Values                |       |
| 5.3. Generated Columns             |       |
| 5.4. Constraints                   |       |
| 5.5. System Columns                |       |
| 5.6. Modifying Tables              |       |
| 5.7. Privileges                    |       |
| 5.8. Row Security Policies         |       |
| 5.9. Schemas                       |       |
| 5.10. Inheritance                  |       |
| 5.11. Table Partitioning           |       |
| 5.12. Foreign Data                 |       |
|                                    |       |
| 5.13. Other Database Objects       | 103   |

| 5.14. Dependency Tracking                         | 105 |
|---------------------------------------------------|-----|
| 6. Data Manipulation                              | 108 |
| 6.1. Inserting Data                               | 108 |
| 6.2. Updating Data                                | 109 |
| 6.3. Deleting Data                                |     |
| 6.4. Returning Data from Modified Rows            | 110 |
| 7. Queries                                        | 112 |
| 7.1. Overview                                     | 112 |
| 7.2. Table Expressions                            | 112 |
| 7.3. Select Lists                                 | 128 |
| 7.4. Combining Queries (UNION, INTERSECT, EXCEPT) | 130 |
| 7.5. Sorting Rows (ORDER BY)                      | 131 |
| 7.6. LIMIT and OFFSET                             | 132 |
| 7.7. VALUES Lists                                 | 132 |
| 7.8. WITH Queries (Common Table Expressions)      | 133 |
| 8. Data Types                                     | 143 |
| 8.1. Numeric Types                                |     |
| 8.2. Monetary Types                               | 149 |
| 8.3. Character Types                              | 150 |
| 8.4. Binary Data Types                            |     |
| 8.5. Date/Time Types                              |     |
| 8.6. Boolean Type                                 |     |
| 8.7. Enumerated Types                             |     |
| 8.8. Geometric Types                              |     |
| 8.9. Network Address Types                        |     |
| 8.10. Bit String Types                            |     |
| 8.11. Text Search Types                           |     |
| 8.12. UUID Type                                   |     |
| 8.13. XML Type                                    |     |
| 8.14. JSON Types                                  |     |
| 8.15. Arrays                                      |     |
| 8.16. Composite Types                             |     |
| 8.17. Range Types                                 |     |
| 8.18. Domain Types                                |     |
| 8.19. Object Identifier Types                     |     |
| 8.20. pg lsn Type                                 |     |
| 8.21. Pseudo-Types                                |     |
| 9. Functions and Operators                        |     |
| 9.1. Logical Operators                            |     |
| 9.2. Comparison Functions and Operators           |     |
| 9.3. Mathematical Functions and Operators         |     |
| 9.4. String Functions and Operators               |     |
| 9.5. Binary String Functions and Operators        |     |
| 9.6. Bit String Functions and Operators           |     |
| 9.7. Pattern Matching                             |     |
| 9.8. Data Type Formatting Functions               |     |
| 9.9. Date/Time Functions and Operators            |     |
| 9.10. Enum Support Functions                      |     |
| 9.11. Geometric Functions and Operators           |     |
| 9.12. Network Address Functions and Operators     |     |
| 9.13. Text Search Functions and Operators         |     |
| 9.14. UUID Functions                              |     |
| 9.15. XML Functions                               |     |
| 9.16. JSON Functions and Operators                |     |
| 9.17. Sequence Manipulation Functions             |     |
| 9.18. Conditional Expressions                     |     |
| 9.19. Array Functions and Operators               |     |
| 9.20. Range/Multirange Functions and Operators    |     |
| 6                                                 |     |

| 9.21. Aggregate Functions                                              | 347 |
|------------------------------------------------------------------------|-----|
| 9.22. Window Functions                                                 | 354 |
| 9.23. Subquery Expressions                                             |     |
| 9.24. Row and Array Comparisons                                        |     |
| 9.25. Set Returning Functions                                          |     |
| 9.26. System Information Functions and Operators                       |     |
|                                                                        |     |
| 9.27. System Administration Functions                                  |     |
| 9.28. Trigger Functions                                                |     |
| 9.29. Event Trigger Functions                                          |     |
| 9.30. Statistics Information Functions                                 |     |
| 10. Type Conversion                                                    | 403 |
| 10.1. Overview                                                         | 403 |
| 10.2. Operators                                                        | 404 |
| 10.3. Functions                                                        | 408 |
| 10.4. Value Storage                                                    |     |
| 10.5. UNION, CASE, and Related Constructs                              |     |
| 10.6. SELECT Output Columns                                            |     |
| 11. Indexes                                                            |     |
|                                                                        |     |
| 11.1. Introduction                                                     |     |
| 11.2. Index Types                                                      |     |
| 11.3. Multicolumn Indexes                                              |     |
| 11.4. Indexes and ORDER BY                                             |     |
| 11.5. Combining Multiple Indexes                                       | 421 |
| 11.6. Unique Indexes                                                   | 422 |
| 11.7. Indexes on Expressions                                           | 422 |
| 11.8. Partial Indexes                                                  | 423 |
| 11.9. Index-Only Scans and Covering Indexes                            |     |
| 11.10. Operator Classes and Operator Families                          |     |
| 11.11. Indexes and Collations                                          |     |
| 11.12. Examining Index Usage                                           |     |
| 12. Full Text Search                                                   |     |
|                                                                        |     |
| 12.1. Introduction                                                     |     |
| 12.2. Tables and Indexes                                               |     |
| 12.3. Controlling Text Search                                          |     |
| 12.4. Additional Features                                              |     |
| 12.5. Parsers                                                          | 451 |
| 12.6. Dictionaries                                                     |     |
| 12.7. Configuration Example                                            | 462 |
| 12.8. Testing and Debugging Text Search                                |     |
| 12.9. Preferred Index Types for Text Search                            |     |
| 12.10. psql Support                                                    |     |
| 12.11. Limitations                                                     |     |
| 13. Concurrency Control                                                |     |
| 13.1. Introduction                                                     |     |
|                                                                        |     |
| 13.2. Transaction Isolation                                            |     |
| 13.3. Explicit Locking                                                 |     |
| 13.4. Data Consistency Checks at the Application Level                 |     |
| 13.5. Caveats                                                          |     |
| 13.6. Locking and Indexes                                              |     |
| 14. Performance Tips                                                   | 489 |
| 14.1. Using EXPLAIN                                                    | 489 |
| 14.2. Statistics Used by the Planner                                   |     |
| 14.3. Controlling the Planner with Explicit JOIN Clauses               |     |
| 14.4. Populating a Database                                            |     |
| 14.5. Non-Durable Settings                                             |     |
| 15. Parallel Query                                                     |     |
| 15.1. How Parallel Query Works                                         |     |
| 15.1. How Parallel Query Works  15.2. When Can Parallel Query Be Used? |     |
| 13.4. When Can Parallel Query De Used?                                 | 213 |

| 15.3. Parallel Plans                                        | 514 |
|-------------------------------------------------------------|-----|
| 15.4. Parallel Safety                                       | 516 |
| III. Server Administration                                  | 518 |
| 16. Installation from Binaries                              | 525 |
| 17. Installation from Source Code                           | 526 |
| 17.1. Short Version                                         | 526 |
| 17.2. Requirements                                          | 526 |
| 17.3. Getting the Source                                    | 528 |
| 17.4. Installation Procedure                                | 528 |
| 17.5. Post-Installation Setup                               | 541 |
| 17.6. Supported Platforms                                   | 542 |
| 17.7. Platform-Specific Notes                               | 542 |
| 18. Installation from Source Code on Windows                | 548 |
| 18.1. Building with Visual C++ or the Microsoft Windows SDK |     |
| 19. Server Setup and Operation                              | 554 |
| 19.1. The PostgreSQL User Account                           |     |
| 19.2. Creating a Database Cluster                           |     |
| 19.3. Starting the Database Server                          |     |
| 19.4. Managing Kernel Resources                             |     |
| 19.5. Shutting Down the Server                              |     |
| 19.6. Upgrading a PostgreSQL Cluster                        |     |
| 19.7. Preventing Server Spoofing                            |     |
| 19.8. Encryption Options                                    |     |
| 19.9. Secure TCP/IP Connections with SSL                    |     |
| 19.10. Secure TCP/IP Connections with GSSAPI Encryption     |     |
| 19.11. Secure TCP/IP Connections with SSH Tunnels           |     |
| 19.12. Registering Event Log on Windows                     |     |
| 20. Server Configuration                                    |     |
| 20.1. Setting Parameters                                    |     |
| 20.2. File Locations                                        |     |
| 20.3. Connections and Authentication                        |     |
| 20.4. Resource Consumption                                  |     |
| 20.5. Write Ahead Log                                       |     |
| 20.6. Replication                                           |     |
| 20.7. Query Planning                                        |     |
| 20.8. Error Reporting and Logging                           |     |
| 20.9. Run-time Statistics                                   |     |
| 20.10. Automatic Vacuuming                                  |     |
| 20.11. Client Connection Defaults                           |     |
| 20.12. Lock Management                                      |     |
| 20.13. Version and Platform Compatibility                   |     |
| 20.14. Error Handling                                       |     |
| 20.15. Preset Options                                       |     |
| 20.16. Customized Options                                   |     |
| 20.17. Developer Options                                    |     |
| 20.18. Short Options                                        |     |
| 21. Client Authentication                                   |     |
| 21.1. The pg hba.conf File                                  |     |
| 21.2. User Name Maps                                        |     |
| 21.3. Authentication Methods                                |     |
| 21.4. Trust Authentication                                  |     |
| 21.5. Password Authentication                               |     |
| 21.6. GSSAPI Authentication                                 |     |
| 21.7. SSPI Authentication                                   |     |
| 21.8. Ident Authentication                                  |     |
| 21.9. Peer Authentication                                   |     |
| 21.10. LDAP Authentication                                  |     |
| 21.11. RADIUS Authentication                                |     |
| 21111 10 10 10 10 10 10 10 10 10 10 10 10                   | 010 |

|                   | 21.12. Certificate Authentication                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |                                                                                                                                                 |
|-------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------|
|                   | 21.13. PAM Authentication                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | 679                                                                                                                                             |
|                   | 21.14. BSD Authentication                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | 680                                                                                                                                             |
|                   | 21.15. Authentication Problems                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | 680                                                                                                                                             |
| 22.               | Database Roles                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | 682                                                                                                                                             |
|                   | 22.1. Database Roles                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | 682                                                                                                                                             |
|                   | 22.2. Role Attributes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | 683                                                                                                                                             |
|                   | 22.3. Role Membership                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | 684                                                                                                                                             |
|                   | 22.4. Dropping Roles                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |                                                                                                                                                 |
|                   | 22.5. Predefined Roles                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |                                                                                                                                                 |
|                   | 22.6. Function Security                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |                                                                                                                                                 |
| 23.               | Managing Databases                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |                                                                                                                                                 |
| 25.               | 23.1. Overview                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |                                                                                                                                                 |
|                   | 23.2. Creating a Database                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |                                                                                                                                                 |
|                   | 23.3. Template Databases                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |                                                                                                                                                 |
|                   | 23.4. Database Configuration                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |                                                                                                                                                 |
|                   | 23.5. Destroying a Database                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |                                                                                                                                                 |
|                   | 23.6. Tablespaces                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |                                                                                                                                                 |
| 24                | Localization                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |                                                                                                                                                 |
| 24.               |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |                                                                                                                                                 |
|                   | 24.1. Locale Support                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |                                                                                                                                                 |
|                   | 24.2. Collation Support                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |                                                                                                                                                 |
| 25                | 24.3. Character Set Support                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |                                                                                                                                                 |
| 25.               | Routine Database Maintenance Tasks                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |                                                                                                                                                 |
|                   | 25.1. Routine Vacuuming                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |                                                                                                                                                 |
|                   | 25.2. Routine Reindexing                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |                                                                                                                                                 |
|                   | 25.3. Log File Maintenance                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |                                                                                                                                                 |
| 26.               | Backup and Restore                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |                                                                                                                                                 |
|                   | 26.1. SQL Dump                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |                                                                                                                                                 |
|                   | 26.2. File System Level Backup                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |                                                                                                                                                 |
|                   |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |                                                                                                                                                 |
|                   | 26.3. Continuous Archiving and Point-in-Time Recovery (PITR)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |                                                                                                                                                 |
| 27.               | High Availability, Load Balancing, and Replication                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | 742                                                                                                                                             |
| 27.               |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | 742                                                                                                                                             |
| 27.               | High Availability, Load Balancing, and Replication                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | 742<br>742                                                                                                                                      |
| 27.               | High Availability, Load Balancing, and Replication                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | 742<br>742<br>745                                                                                                                               |
| 27.               | High Availability, Load Balancing, and Replication  27.1. Comparison of Different Solutions  27.2. Log-Shipping Standby Servers                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | 742<br>742<br>745<br>754                                                                                                                        |
|                   | High Availability, Load Balancing, and Replication  27.1. Comparison of Different Solutions  27.2. Log-Shipping Standby Servers  27.3. Failover                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | 742<br>742<br>745<br>754<br>755                                                                                                                 |
|                   | High Availability, Load Balancing, and Replication  27.1. Comparison of Different Solutions  27.2. Log-Shipping Standby Servers  27.3. Failover  27.4. Hot Standby                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | 742<br>745<br>745<br>754<br>755<br>763                                                                                                          |
|                   | High Availability, Load Balancing, and Replication  27.1. Comparison of Different Solutions  27.2. Log-Shipping Standby Servers  27.3. Failover  27.4. Hot Standby  Monitoring Database Activity  28.1. Standard Unix Tools                                                                                                                                                                                                                                                                                                                                                                                                                                                         | 742<br>745<br>745<br>754<br>755<br>763                                                                                                          |
|                   | High Availability, Load Balancing, and Replication  27.1. Comparison of Different Solutions  27.2. Log-Shipping Standby Servers  27.3. Failover  27.4. Hot Standby  Monitoring Database Activity  28.1. Standard Unix Tools  28.2. The Statistics Collector                                                                                                                                                                                                                                                                                                                                                                                                                         | 742<br>745<br>754<br>755<br>763<br>764                                                                                                          |
|                   | High Availability, Load Balancing, and Replication  27.1. Comparison of Different Solutions  27.2. Log-Shipping Standby Servers  27.3. Failover  27.4. Hot Standby  Monitoring Database Activity  28.1. Standard Unix Tools  28.2. The Statistics Collector  28.3. Viewing Locks                                                                                                                                                                                                                                                                                                                                                                                                    | 742<br>745<br>754<br>755<br>763<br>763<br>764<br>798                                                                                            |
|                   | High Availability, Load Balancing, and Replication  27.1. Comparison of Different Solutions  27.2. Log-Shipping Standby Servers  27.3. Failover  27.4. Hot Standby  Monitoring Database Activity  28.1. Standard Unix Tools  28.2. The Statistics Collector  28.3. Viewing Locks  28.4. Progress Reporting                                                                                                                                                                                                                                                                                                                                                                          | 742<br>745<br>754<br>755<br>763<br>764<br>798<br>798                                                                                            |
| 28.               | High Availability, Load Balancing, and Replication  27.1. Comparison of Different Solutions  27.2. Log-Shipping Standby Servers  27.3. Failover  27.4. Hot Standby  Monitoring Database Activity  28.1. Standard Unix Tools  28.2. The Statistics Collector  28.3. Viewing Locks  28.4. Progress Reporting  28.5. Dynamic Tracing                                                                                                                                                                                                                                                                                                                                                   | 742<br>745<br>754<br>755<br>763<br>763<br>764<br>798<br>798<br>806                                                                              |
| 28.               | High Availability, Load Balancing, and Replication  27.1. Comparison of Different Solutions  27.2. Log-Shipping Standby Servers  27.3. Failover  27.4. Hot Standby  Monitoring Database Activity  28.1. Standard Unix Tools  28.2. The Statistics Collector  28.3. Viewing Locks  28.4. Progress Reporting  28.5. Dynamic Tracing  Monitoring Disk Usage                                                                                                                                                                                                                                                                                                                            | 742<br>745<br>754<br>755<br>763<br>763<br>764<br>798<br>806<br>815                                                                              |
| 28.               | High Availability, Load Balancing, and Replication  27.1. Comparison of Different Solutions  27.2. Log-Shipping Standby Servers  27.3. Failover  27.4. Hot Standby  Monitoring Database Activity  28.1. Standard Unix Tools  28.2. The Statistics Collector  28.3. Viewing Locks  28.4. Progress Reporting  28.5. Dynamic Tracing  Monitoring Disk Usage  29.1. Determining Disk Usage                                                                                                                                                                                                                                                                                              | 742<br>745<br>754<br>755<br>763<br>763<br>764<br>798<br>806<br>815<br>815                                                                       |
| 28.               | High Availability, Load Balancing, and Replication  27.1. Comparison of Different Solutions  27.2. Log-Shipping Standby Servers  27.3. Failover  27.4. Hot Standby  Monitoring Database Activity  28.1. Standard Unix Tools  28.2. The Statistics Collector  28.3. Viewing Locks  28.4. Progress Reporting  28.5. Dynamic Tracing  Monitoring Disk Usage  29.1. Determining Disk Usage  29.2. Disk Full Failure                                                                                                                                                                                                                                                                     | 742<br>745<br>754<br>755<br>763<br>763<br>764<br>798<br>806<br>815<br>815                                                                       |
| 28.               | High Availability, Load Balancing, and Replication  27.1. Comparison of Different Solutions  27.2. Log-Shipping Standby Servers  27.3. Failover  27.4. Hot Standby  Monitoring Database Activity  28.1. Standard Unix Tools  28.2. The Statistics Collector  28.3. Viewing Locks  28.4. Progress Reporting  28.5. Dynamic Tracing  Monitoring Disk Usage  29.1. Determining Disk Usage  29.2. Disk Full Failure  Reliability and the Write-Ahead Log                                                                                                                                                                                                                                | 742<br>745<br>754<br>755<br>763<br>763<br>764<br>798<br>806<br>815<br>816<br>817                                                                |
| 28.               | High Availability, Load Balancing, and Replication  27.1. Comparison of Different Solutions  27.2. Log-Shipping Standby Servers  27.3. Failover  27.4. Hot Standby  Monitoring Database Activity  28.1. Standard Unix Tools  28.2. The Statistics Collector  28.3. Viewing Locks  28.4. Progress Reporting  28.5. Dynamic Tracing  Monitoring Disk Usage  29.1. Determining Disk Usage  29.2. Disk Full Failure  Reliability and the Write-Ahead Log  30.1. Reliability                                                                                                                                                                                                             | 742<br>745<br>754<br>755<br>763<br>764<br>798<br>806<br>815<br>816<br>817<br>817                                                                |
| 28.               | High Availability, Load Balancing, and Replication  27.1. Comparison of Different Solutions  27.2. Log-Shipping Standby Servers  27.3. Failover  27.4. Hot Standby  Monitoring Database Activity  28.1. Standard Unix Tools  28.2. The Statistics Collector  28.3. Viewing Locks  28.4. Progress Reporting  28.5. Dynamic Tracing  Monitoring Disk Usage  29.1. Determining Disk Usage  29.2. Disk Full Failure  Reliability and the Write-Ahead Log  30.1. Reliability  30.2. Data Checksums                                                                                                                                                                                       | 742<br>745<br>754<br>755<br>763<br>764<br>798<br>806<br>815<br>816<br>817<br>817<br>819                                                         |
| 28.               | High Availability, Load Balancing, and Replication  27.1. Comparison of Different Solutions  27.2. Log-Shipping Standby Servers  27.3. Failover  27.4. Hot Standby  Monitoring Database Activity  28.1. Standard Unix Tools  28.2. The Statistics Collector  28.3. Viewing Locks  28.4. Progress Reporting  28.5. Dynamic Tracing  Monitoring Disk Usage  29.1. Determining Disk Usage  29.2. Disk Full Failure  Reliability and the Write-Ahead Log  30.1. Reliability  30.2. Data Checksums  30.3. Write-Ahead Logging (WAL)                                                                                                                                                      | 742<br>745<br>754<br>755<br>763<br>763<br>764<br>798<br>806<br>815<br>815<br>817<br>817<br>819                                                  |
| 28.               | High Availability, Load Balancing, and Replication  27.1. Comparison of Different Solutions  27.2. Log-Shipping Standby Servers  27.3. Failover  27.4. Hot Standby  Monitoring Database Activity  28.1. Standard Unix Tools  28.2. The Statistics Collector  28.3. Viewing Locks  28.4. Progress Reporting  28.5. Dynamic Tracing  Monitoring Disk Usage  29.1. Determining Disk Usage  29.2. Disk Full Failure  Reliability and the Write-Ahead Log  30.1. Reliability  30.2. Data Checksums  30.3. Write-Ahead Logging (WAL)  30.4. Asynchronous Commit                                                                                                                           | 742<br>745<br>754<br>755<br>763<br>763<br>764<br>798<br>806<br>815<br>817<br>817<br>819<br>820                                                  |
| 28.               | High Availability, Load Balancing, and Replication  27.1. Comparison of Different Solutions  27.2. Log-Shipping Standby Servers  27.3. Failover  27.4. Hot Standby  Monitoring Database Activity  28.1. Standard Unix Tools  28.2. The Statistics Collector  28.3. Viewing Locks  28.4. Progress Reporting  28.5. Dynamic Tracing  Monitoring Disk Usage  29.1. Determining Disk Usage  29.2. Disk Full Failure  Reliability and the Write-Ahead Log  30.1. Reliability  30.2. Data Checksums  30.3. Write-Ahead Logging (WAL)  30.4. Asynchronous Commit  30.5. WAL Configuration                                                                                                  | 742<br>745<br>754<br>755<br>763<br>763<br>764<br>798<br>806<br>815<br>816<br>817<br>819<br>819<br>820<br>821                                    |
| 28.<br>29.<br>30. | High Availability, Load Balancing, and Replication  27.1. Comparison of Different Solutions  27.2. Log-Shipping Standby Servers  27.3. Failover  27.4. Hot Standby  Monitoring Database Activity  28.1. Standard Unix Tools  28.2. The Statistics Collector  28.3. Viewing Locks  28.4. Progress Reporting  28.5. Dynamic Tracing  Monitoring Disk Usage  29.1. Determining Disk Usage  29.2. Disk Full Failure  Reliability and the Write-Ahead Log  30.1. Reliability  30.2. Data Checksums  30.3. Write-Ahead Logging (WAL)  30.4. Asynchronous Commit  30.5. WAL Configuration  30.6. WAL Internals                                                                             | 742<br>742<br>745<br>754<br>755<br>763<br>764<br>798<br>806<br>815<br>817<br>817<br>819<br>820<br>821<br>824                                    |
| 28.<br>29.<br>30. | High Availability, Load Balancing, and Replication  27.1. Comparison of Different Solutions  27.2. Log-Shipping Standby Servers  27.3. Failover  27.4. Hot Standby  Monitoring Database Activity  28.1. Standard Unix Tools  28.2. The Statistics Collector  28.3. Viewing Locks  28.4. Progress Reporting  28.5. Dynamic Tracing  Monitoring Disk Usage  29.1. Determining Disk Usage  29.2. Disk Full Failure  Reliability and the Write-Ahead Log  30.1. Reliability  30.2. Data Checksums  30.3. Write-Ahead Logging (WAL)  30.4. Asynchronous Commit  30.5. WAL Configuration  30.6. WAL Internals  Logical Replication                                                        | 742<br>742<br>745<br>754<br>755<br>763<br>764<br>798<br>806<br>815<br>817<br>819<br>820<br>821<br>824<br>826                                    |
| 28.<br>29.<br>30. | High Availability, Load Balancing, and Replication  27.1. Comparison of Different Solutions  27.2. Log-Shipping Standby Servers  27.3. Failover  27.4. Hot Standby  Monitoring Database Activity  28.1. Standard Unix Tools  28.2. The Statistics Collector  28.3. Viewing Locks  28.4. Progress Reporting  28.5. Dynamic Tracing  Monitoring Disk Usage  29.1. Determining Disk Usage  29.2. Disk Full Failure  Reliability and the Write-Ahead Log  30.1. Reliability  30.2. Data Checksums  30.3. Write-Ahead Logging (WAL)  30.4. Asynchronous Commit  30.5. WAL Configuration  30.6. WAL Internals  Logical Replication  31.1. Publication                                     | 742<br>742<br>745<br>754<br>755<br>763<br>764<br>798<br>806<br>815<br>817<br>817<br>819<br>820<br>821<br>824<br>826<br>826                      |
| 28.<br>29.<br>30. | High Availability, Load Balancing, and Replication  27.1. Comparison of Different Solutions  27.2. Log-Shipping Standby Servers  27.3. Failover  27.4. Hot Standby  Monitoring Database Activity  28.1. Standard Unix Tools  28.2. The Statistics Collector  28.3. Viewing Locks  28.4. Progress Reporting  28.5. Dynamic Tracing  Monitoring Disk Usage  29.1. Determining Disk Usage  29.2. Disk Full Failure  Reliability and the Write-Ahead Log  30.1. Reliability  30.2. Data Checksums  30.3. Write-Ahead Logging (WAL)  30.4. Asynchronous Commit  30.5. WAL Configuration  30.6. WAL Internals  Logical Replication  31.1. Publication  31.2. Subscription                 | 742<br>742<br>745<br>754<br>755<br>763<br>763<br>764<br>798<br>806<br>815<br>817<br>819<br>820<br>821<br>824<br>826<br>826<br>827               |
| 28.<br>29.<br>30. | High Availability, Load Balancing, and Replication 27.1. Comparison of Different Solutions 27.2. Log-Shipping Standby Servers 27.3. Failover 27.4. Hot Standby  Monitoring Database Activity 28.1. Standard Unix Tools 28.2. The Statistics Collector 28.3. Viewing Locks 28.4. Progress Reporting 28.5. Dynamic Tracing  Monitoring Disk Usage 29.1. Determining Disk Usage 29.2. Disk Full Failure  Reliability and the Write-Ahead Log 30.1. Reliability 30.2. Data Checksums 30.3. Write-Ahead Logging (WAL) 30.4. Asynchronous Commit 30.5. WAL Configuration 30.6. WAL Internals  Logical Replication 31.1. Publication 31.2. Subscription 31.3. Conflicts                    | 742<br>742<br>745<br>754<br>755<br>763<br>763<br>764<br>798<br>806<br>815<br>817<br>817<br>819<br>820<br>821<br>824<br>826<br>827<br>828        |
| 28.<br>29.<br>30. | High Availability, Load Balancing, and Replication 27.1. Comparison of Different Solutions 27.2. Log-Shipping Standby Servers 27.3. Failover 27.4. Hot Standby  Monitoring Database Activity 28.1. Standard Unix Tools 28.2. The Statistics Collector 28.3. Viewing Locks 28.4. Progress Reporting 28.5. Dynamic Tracing  Monitoring Disk Usage 29.1. Determining Disk Usage 29.2. Disk Full Failure  Reliability and the Write-Ahead Log 30.1. Reliability 30.2. Data Checksums 30.3. Write-Ahead Logging (WAL) 30.4. Asynchronous Commit 30.5. WAL Configuration 30.6. WAL Internals  Logical Replication 31.1. Publication 31.2. Subscription 31.3. Conflicts 31.4. Restrictions | 742<br>742<br>745<br>754<br>755<br>763<br>763<br>764<br>798<br>806<br>815<br>816<br>817<br>819<br>820<br>821<br>824<br>826<br>827<br>828<br>828 |
| 28.<br>29.<br>30. | High Availability, Load Balancing, and Replication 27.1. Comparison of Different Solutions 27.2. Log-Shipping Standby Servers 27.3. Failover 27.4. Hot Standby  Monitoring Database Activity 28.1. Standard Unix Tools 28.2. The Statistics Collector 28.3. Viewing Locks 28.4. Progress Reporting 28.5. Dynamic Tracing  Monitoring Disk Usage 29.1. Determining Disk Usage 29.2. Disk Full Failure  Reliability and the Write-Ahead Log 30.1. Reliability 30.2. Data Checksums 30.3. Write-Ahead Logging (WAL) 30.4. Asynchronous Commit 30.5. WAL Configuration 30.6. WAL Internals  Logical Replication 31.1. Publication 31.2. Subscription 31.3. Conflicts                    | 742<br>742<br>745<br>754<br>755<br>763<br>764<br>798<br>806<br>815<br>817<br>819<br>820<br>821<br>824<br>826<br>826<br>827<br>828<br>828<br>829 |

| 31.7. Security                                    | 830   |
|---------------------------------------------------|-------|
| 31.8. Configuration Settings                      | . 830 |
| 31.9. Quick Setup                                 | 831   |
| 32. Just-in-Time Compilation (JIT)                | 832   |
| 32.1. What Is JIT compilation?                    | 832   |
| 32.2. When to JIT?                                | 832   |
| 32.3. Configuration                               | 834   |
| 32.4. Extensibility                               | 834   |
| 33. Regression Tests                              | . 835 |
| 33.1. Running the Tests                           | 835   |
| 33.2. Test Evaluation                             | 839   |
| 33.3. Variant Comparison Files                    | 841   |
| 33.4. TAP Tests                                   | . 842 |
| 33.5. Test Coverage Examination                   | 843   |
| IV. Client Interfaces                             |       |
| 34. libpq — C Library                             | 849   |
| 34.1. Database Connection Control Functions       | 849   |
| 34.2. Connection Status Functions                 | 865   |
| 34.3. Command Execution Functions                 | . 871 |
| 34.4. Asynchronous Command Processing             |       |
| 34.5. Pipeline Mode                               |       |
| 34.6. Retrieving Query Results Row-by-Row         |       |
| 34.7. Canceling Queries in Progress               |       |
| 34.8. The Fast-Path Interface                     |       |
| 34.9. Asynchronous Notification                   |       |
| 34.10. Functions Associated with the COPY Command |       |
| 34.11. Control Functions                          | 903   |
| 34.12. Miscellaneous Functions                    | 905   |
| 34.13. Notice Processing                          |       |
| 34.14. Event System                               |       |
| 34.15. Environment Variables                      |       |
| 34.16. The Password File                          |       |
| 34.17. The Connection Service File                |       |
| 34.18. LDAP Lookup of Connection Parameters       |       |
| 34.19. SSL Support                                |       |
| 34.20. Behavior in Threaded Programs              |       |
| 34.21. Building libpq Programs                    |       |
| 34.22. Example Programs                           |       |
| 35. Large Objects                                 |       |
| 35.1. Introduction                                | . 937 |
| 35.2. Implementation Features                     | . 937 |
| 35.3. Client Interfaces                           | . 937 |
| 35.4. Server-Side Functions                       | 942   |
| 35.5. Example Program                             | . 943 |
| 36. ECPG — Embedded SQL in C                      | 949   |
| 36.1. The Concept                                 | . 949 |
| 36.2. Managing Database Connections               | . 949 |
| 36.3. Running SQL Commands                        | 953   |
| 36.4. Using Host Variables                        | 956   |
| 36.5. Dynamic SQL                                 |       |
| 36.6. pgtypes Library                             | . 972 |
| 36.7. Using Descriptor Areas                      |       |
| 36.8. Error Handling                              | . 999 |
| 36.9. Preprocessor Directives                     |       |
| 36.10. Processing Embedded SQL Programs           |       |
| 36.11. Library Functions                          |       |
| 36.12. Large Objects                              |       |
| 36.13. C++ Applications                           | 1011  |

|       | . Embedded SQL Commands                |      |
|-------|----------------------------------------|------|
|       | . Informix Compatibility Mode          |      |
|       | . Oracle Compatibility Mode            |      |
|       | . Internals                            |      |
|       | ormation Schema                        |      |
| 37.1. | The Schema                             | 1057 |
|       | Data Types                             |      |
| 37.3. | information_schema_catalog_name        | 1058 |
|       | administrable_role_authorizations      |      |
| 37.5. | applicable_roles                       | 1058 |
| 37.6. | attributes                             | 1059 |
|       | character_sets                         |      |
| 37.8. | check_constraint_routine_usage         | 1062 |
| 37.9. | check_constraints                      | 1062 |
| 37.10 | collations                             | 1063 |
| 37.11 | .collation_character_set_applicability | 1063 |
| 37.12 | .column_column_usage                   | 1064 |
| 37.13 | .column_domain_usage                   | 1064 |
| 37.14 | .column_options                        | 1064 |
| 37.15 | .column_privileges                     | 1065 |
| 37.16 | .column_udt_usage                      | 1066 |
| 37.17 | . columns                              | 1066 |
| 37.18 | .constraint_column_usage               | 1069 |
| 37.19 | .constraint table usage                | 1070 |
| 37.20 | .data_type_privileges                  | 1070 |
| 37.21 | . domain_constraints                   | 1071 |
| 37.22 | .domain_udt_usage                      | 1071 |
| 37.23 | domains                                | 1072 |
| 37.24 | .element_types                         | 1074 |
| 37.25 | . enabled_roles                        | 1076 |
| 37.26 | .foreign_data_wrapper_options          | 1076 |
| 37.27 | .foreign_data_wrappers                 | 1077 |
| 37.28 | .foreign_server_options                | 1077 |
| 37.29 | foreign_servers                        | 1077 |
| 37.30 | foreign_table_options                  | 1078 |
| 37.31 | foreign_tables                         | 1078 |
| 37.32 | .key_column_usage                      | 1079 |
| 37.33 | . parameters                           | 1079 |
| 37.34 | referential_constraints                | 1081 |
| 37.35 | role_column_grants                     | 1082 |
|       | role_routine_grants                    |      |
| 37.37 | role_table_grants                      | 1083 |
| 37.38 | role_udt_grants                        | 1084 |
|       | role_usage_grants                      |      |
|       | .routine_column_usage                  |      |
|       | .routine_privileges                    |      |
| 37.42 | .routine_routine_usage                 | 1086 |
| 37.43 | .routine_sequence_usage                | 1087 |
| 37.44 | routine_table_usage                    | 1087 |
|       | routines                               |      |
| 37.46 | . schemata                             | 1092 |
| 37.47 | . sequences                            | 1092 |
| 37.48 | .sql_features                          | 1093 |
| 37.49 | .sql_implementation_info               | 1094 |
| 37.50 | .sql_parts                             | 1094 |
|       | .sql_sizing                            |      |
| 37.52 | table_constraints                      | 1095 |
|       | .table privileges                      |      |

| 37.54. tables                                      | 1096 |
|----------------------------------------------------|------|
| 37.55. transforms                                  | 1097 |
| 37.56. triggered_update_columns                    | 1098 |
| 37.57. triggers                                    |      |
| 37.58. udt privileges                              |      |
| 37.59. usage privileges                            |      |
| 37.60. user defined types                          |      |
| 37.61. user mapping options                        |      |
| 37.62. user mappings                               |      |
| 37.63. view column usage                           |      |
| 37.64. view routine usage                          |      |
| 37.65. view table usage                            |      |
| 37.66. views                                       |      |
|                                                    |      |
| V. Server Programming                              |      |
| 38. Extending SQL                                  |      |
| 38.1. How Extensibility Works                      |      |
| 38.2. The PostgreSQL Type System                   |      |
| 38.3. User-Defined Functions                       |      |
| 38.4. User-Defined Procedures                      |      |
| 38.5. Query Language (SQL) Functions               |      |
| 38.6. Function Overloading                         |      |
| 38.7. Function Volatility Categories               | 1135 |
| 38.8. Procedural Language Functions                |      |
| 38.9. Internal Functions                           | 1137 |
| 38.10. C-Language Functions                        | 1137 |
| 38.11. Function Optimization Information           | 1158 |
| 38.12. User-Defined Aggregates                     | 1159 |
| 38.13. User-Defined Types                          |      |
| 38.14. User-Defined Operators                      |      |
| 38.15. Operator Optimization Information           |      |
| 38.16. Interfacing Extensions to Indexes           |      |
| 38.17. Packaging Related Objects into an Extension |      |
| 38.18. Extension Building Infrastructure           |      |
| 39. Triggers                                       |      |
| 39.1. Overview of Trigger Behavior                 |      |
|                                                    |      |
| 39.2. Visibility of Data Changes                   |      |
| 39.3. Writing Trigger Functions in C               |      |
| 39.4. A Complete Trigger Example                   |      |
| 40. Event Triggers                                 | 1211 |
| 40.1. Overview of Event Trigger Behavior           |      |
| 40.2. Event Trigger Firing Matrix                  |      |
| 40.3. Writing Event Trigger Functions in C         |      |
| 40.4. A Complete Event Trigger Example             |      |
| 40.5. A Table Rewrite Event Trigger Example        |      |
| 41. The Rule System                                |      |
| 41.1. The Query Tree                               |      |
| 41.2. Views and the Rule System                    |      |
| 41.3. Materialized Views                           | 1227 |
| 41.4. Rules on INSERT, UPDATE, and DELETE          | 1230 |
| 41.5. Rules and Privileges                         |      |
| 41.6. Rules and Command Status                     |      |
| 41.7. Rules Versus Triggers                        |      |
| 42. Procedural Languages                           |      |
| 42.1. Installing Procedural Languages              |      |
| 43. PL/pgSQL — SQL Procedural Language             |      |
| 43.1. Overview                                     |      |
| 43.2. Structure of PL/pgSQL                        |      |
| 43.3. Declarations                                 |      |

|     | 43.4. Expressions                                 |      |
|-----|---------------------------------------------------|------|
|     | 43.5. Basic Statements                            | 1259 |
|     | 43.6. Control Structures                          | 1267 |
|     | 43.7. Cursors                                     | 1282 |
|     | 43.8. Transaction Management                      | 1288 |
|     | 43.9. Errors and Messages                         | 1289 |
|     | 43.10. Trigger Functions                          | 1291 |
|     | 43.11. PL/pgSQL under the Hood                    | 1300 |
|     | 43.12. Tips for Developing in PL/pgSQL            |      |
|     | 43.13. Porting from Oracle PL/SQL                 |      |
| 44. | PL/Tcl — Tcl Procedural Language                  |      |
|     | 44.1. Overview                                    |      |
|     | 44.2. PL/Tcl Functions and Arguments              |      |
|     | 44.3. Data Values in PL/Tcl                       |      |
|     | 44.4. Global Data in PL/Tcl                       |      |
|     | 44.5. Database Access from PL/Tcl                 |      |
|     | 44.6. Trigger Functions in PL/Tcl                 |      |
|     | 44.7. Event Trigger Functions in PL/Tcl           |      |
|     | 44.8. Error Handling in PL/Tcl                    |      |
|     | 44.9. Explicit Subtransactions in PL/Tcl          |      |
|     | 44.10. Transaction Management                     |      |
|     | 44.11. PL/Tcl Configuration                       |      |
|     | 44.12. Tcl Procedure Names                        |      |
| 15  |                                                   |      |
| 43. | PL/Perl — Perl Procedural Language                |      |
|     | 45.1. PL/Perl Functions and Arguments             |      |
|     | 45.2. Data Values in PL/Perl                      |      |
|     | 45.3. Built-in Functions                          |      |
|     | 45.4. Global Values in PL/Perl                    |      |
|     | 45.5. Trusted and Untrusted PL/Perl               |      |
|     | 45.6. PL/Perl Triggers                            |      |
|     | 45.7. PL/Perl Event Triggers                      |      |
|     | 45.8. PL/Perl Under the Hood                      |      |
| 46. | PL/Python — Python Procedural Language            |      |
|     | 46.1. Python 2 vs. Python 3                       |      |
|     | 46.2. PL/Python Functions                         |      |
|     | 46.3. Data Values                                 |      |
|     | 46.4. Sharing Data                                |      |
|     | 46.5. Anonymous Code Blocks                       | 1352 |
|     | 46.6. Trigger Functions                           | 1352 |
|     | 46.7. Database Access                             | 1353 |
|     | 46.8. Explicit Subtransactions                    | 1357 |
|     | 46.9. Transaction Management                      | 1358 |
|     | 46.10. Utility Functions                          | 1359 |
|     | 46.11. Environment Variables                      | 1360 |
| 47. | Server Programming Interface                      | 1361 |
|     | 47.1. Interface Functions                         |      |
|     | 47.2. Interface Support Functions                 |      |
|     | 47.3. Memory Management                           |      |
|     | 47.4. Transaction Management                      |      |
|     | 47.5. Visibility of Data Changes                  |      |
|     | 47.6. Examples                                    |      |
| 48  | Background Worker Processes                       |      |
|     | Logical Decoding                                  |      |
| чΣ. | 49.1. Logical Decoding Examples                   |      |
|     | 49.2. Logical Decoding Concepts                   |      |
|     |                                                   |      |
|     | 49.3. Streaming Replication Protocol Interface    |      |
|     | 49.4. Logical Decoding SQL Interface              |      |
|     | 49.5. System Catalogs Related to Logical Decoding | 143/ |

| 49.6. Logical Decoding Output Plugins                      | 1437 |
|------------------------------------------------------------|------|
| 49.7. Logical Decoding Output Writers                      | 1445 |
| 49.8. Synchronous Replication Support for Logical Decoding | 1445 |
| 49.9. Streaming of Large Transactions for Logical Decoding | 1446 |
| 49.10. Two-phase Commit Support for Logical Decoding       | 1447 |
| 50. Replication Progress Tracking                          | 1449 |
| VI. Reference                                              |      |
| I. SQL Commands                                            | 1455 |
| ABORT                                                      |      |
| ALTER AGGREGATE                                            | 1460 |
| ALTER COLLATION                                            |      |
| ALTER CONVERSION                                           |      |
| ALTER DATABASE                                             |      |
| ALTER DEFAULT PRIVILEGES                                   |      |
| ALTER DOMAIN                                               |      |
| ALTER EVENT TRIGGER                                        |      |
|                                                            |      |
| ALTER EXTENSIONALTER FOREIGN DATA WRAPPER                  |      |
|                                                            |      |
| ALTER FOREIGN TABLE                                        |      |
| ALTER FUNCTION                                             |      |
| ALTER GROUP                                                |      |
| ALTER INDEX                                                |      |
| ALTER LANGUAGE                                             |      |
| ALTER LARGE OBJECT                                         |      |
| ALTER MATERIALIZED VIEW                                    |      |
| ALTER OPERATOR                                             |      |
| ALTER OPERATOR CLASS                                       |      |
| ALTER OPERATOR FAMILY                                      |      |
| ALTER POLICY                                               |      |
| ALTER PROCEDURE                                            |      |
| ALTER PUBLICATION                                          |      |
| ALTER ROLE                                                 |      |
| ALTER ROUTINE                                              |      |
| ALTER RULE                                                 |      |
| ALTER SCHEMA                                               |      |
| ALTER SEQUENCE                                             |      |
| ALTER SERVER                                               |      |
| ALTER STATISTICS                                           | 1529 |
| ALTER SUBSCRIPTION                                         | 1530 |
| ALTER SYSTEM                                               | 1533 |
| ALTER TABLE                                                | 1535 |
| ALTER TABLESPACE                                           |      |
| ALTER TEXT SEARCH CONFIGURATION                            |      |
| ALTER TEXT SEARCH DICTIONARY                               | 1556 |
| ALTER TEXT SEARCH PARSER                                   | 1558 |
| ALTER TEXT SEARCH TEMPLATE                                 | 1559 |
| ALTER TRIGGER                                              | 1560 |
| ALTER TYPE                                                 | 1562 |
| ALTER USER                                                 | 1567 |
| ALTER USER MAPPING                                         | 1568 |
| ALTER VIEW                                                 | 1569 |
| ANALYZE                                                    | 1571 |
| BEGIN                                                      | 1574 |
| CALL                                                       | 1576 |
| CHECKPOINT                                                 | 1578 |
| CLOSE                                                      |      |
| CLUSTER                                                    | 1580 |
| COMMENT                                                    | 1583 |

| COMMIT                           |      |
|----------------------------------|------|
| COMMIT PREPARED                  | 1589 |
| COPY                             | 1590 |
| CREATE ACCESS METHOD             | 1600 |
| CREATE AGGREGATE                 | 1601 |
| CREATE CAST                      | 1609 |
| CREATE COLLATION                 |      |
| CREATE CONVERSION                |      |
| CREATE DATABASE                  |      |
| CREATE DOMAIN                    |      |
| CREATE EVENT TRIGGER             |      |
|                                  |      |
| CREATE EXTENSION                 |      |
| CREATE FOREIGN DATA WRAPPER      |      |
| CREATE FOREIGN TABLE             |      |
| CREATE FUNCTION                  |      |
| CREATE GROUP                     | 1646 |
| CREATE INDEX                     | 1647 |
| CREATE LANGUAGE                  | 1656 |
| CREATE MATERIALIZED VIEW         | 1659 |
| CREATE OPERATOR                  |      |
| CREATE OPERATOR CLASS            |      |
| CREATE OPERATOR FAMILY           |      |
| CREATE POLICY                    |      |
| CREATE PROCEDURE                 |      |
|                                  |      |
| CREATE PUBLICATION               |      |
| CREATE ROLE                      |      |
| CREATE RULE                      |      |
| CREATE SCHEMA                    |      |
| CREATE SEQUENCE                  |      |
| CREATE SERVER                    |      |
| CREATE STATISTICS                |      |
| CREATE SUBSCRIPTION              | 1702 |
| CREATE TABLE                     | 1705 |
| CREATE TABLE AS                  | 1727 |
| CREATE TABLESPACE                | 1730 |
| CREATE TEXT SEARCH CONFIGURATION | 1732 |
| CREATE TEXT SEARCH DICTIONARY    | 1733 |
| CREATE TEXT SEARCH PARSER        | 1735 |
| CREATE TEXT SEARCH TEMPLATE      |      |
| CREATE TRANSFORM                 |      |
| CREATE TRIGGER                   |      |
| CREATE TYPE                      |      |
| CREATE USER                      |      |
| CREATE USER MAPPING              |      |
|                                  |      |
| CREATE VIEW                      |      |
| DEALLOCATE                       |      |
| DECLARE                          |      |
| DELETE                           |      |
| DISCARD                          | 1772 |
| DO                               |      |
| DROP ACCESS METHOD               |      |
| DROP AGGREGATE                   | 1776 |
| DROP CAST                        |      |
| DROP COLLATION                   |      |
| DROP CONVERSION                  |      |
| DROP DATABASE                    |      |
| DROP DOMAIN                      |      |
| DROP EVENT TRIGGER               |      |
|                                  | -,00 |

| DROP EXTENSION                 | 1784 |
|--------------------------------|------|
| DROP FOREIGN DATA WRAPPER      | 1785 |
| DROP FOREIGN TABLE             | 1786 |
| DROP FUNCTION                  |      |
| DROP GROUP                     |      |
| DROP INDEX                     |      |
| DROP LANGUAGE                  |      |
| DROP MATERIALIZED VIEW         |      |
| DROP OPERATOR                  |      |
| DROP OPERATOR CLASS            |      |
| DROP OPERATOR FAMILY           |      |
| DROP OWNED                     |      |
| DROP POLICY                    |      |
| DROP PROCEDURE                 |      |
| DROP PUBLICATION               |      |
| DROP ROLE                      |      |
|                                |      |
| DROP ROUTINE                   |      |
| DROP RULE                      |      |
| DROP SCHEMA                    |      |
| DROP SEQUENCE                  |      |
| DROP SERVER                    |      |
| DROP STATISTICS                |      |
| DROP SUBSCRIPTION              |      |
| DROP TABLE                     |      |
| DROP TABLESPACE                | 1816 |
| DROP TEXT SEARCH CONFIGURATION | 1817 |
| DROP TEXT SEARCH DICTIONARY    | 1818 |
| DROP TEXT SEARCH PARSER        | 1819 |
| DROP TEXT SEARCH TEMPLATE      |      |
| DROP TRANSFORM                 |      |
| DROP TRIGGER                   | 1822 |
| DROP TYPE                      |      |
| DROP USER                      |      |
| DROP USER MAPPING              |      |
| DROP VIEW                      |      |
| END                            |      |
| EXECUTE                        |      |
| EXPLAIN                        |      |
| FETCH                          |      |
| GRANT                          |      |
| IMPORT FOREIGN SCHEMA          |      |
| INSERT                         |      |
| LISTEN                         |      |
| LOAD                           |      |
|                                |      |
| LOCK                           |      |
| MOVE                           |      |
| NOTIFY                         |      |
| PREPARE                        |      |
| PREPARE TRANSACTION            |      |
| REASSIGN OWNED                 |      |
| REFRESH MATERIALIZED VIEW      |      |
| REINDEX                        |      |
| RELEASE SAVEPOINT              |      |
| RESET                          |      |
| REVOKE                         | 1880 |
| ROLLBACK                       |      |
| ROLLBACK PREPARED              | 1885 |
| ROLLBACK TO SAVEPOINT          |      |

| SAVEPOINT                             |       | 1888 |
|---------------------------------------|-------|------|
| SECURITY LABEL                        |       |      |
| SELECT                                |       | 1893 |
| SELECT INTO                           |       | 1915 |
| SET                                   |       | 1917 |
| SET CONSTRAINTS                       |       | 1920 |
| SET ROLE                              |       | 1921 |
| SET SESSION AUTHORIZATION             |       | 1923 |
| SET TRANSACTION                       |       | 1925 |
| SHOW                                  |       | 1928 |
| START TRANSACTION                     | ••••• | 1930 |
| TRUNCATE                              |       | 1931 |
| UNLISTEN                              | ••••• | 1933 |
| UPDATE                                | ••••• | 1935 |
| VACUUM                                |       | 1940 |
| VALUES                                |       |      |
| II. PostgreSQL Client Applications    |       |      |
| clusterdb                             |       |      |
| createdb                              |       |      |
| createuser                            |       |      |
| dropdb                                |       |      |
| dropuser                              |       |      |
| ecpg                                  |       |      |
| pg amcheck                            |       |      |
| pg_basebackup                         |       |      |
| pgbench                               |       |      |
| pg config                             |       |      |
| pg dump                               |       |      |
| pg dumpall                            |       |      |
| pg isready                            |       |      |
| pg receivewal                         |       |      |
| pg recvlogical                        |       |      |
| pg restore                            |       |      |
| pg verifybackup                       |       |      |
| psql                                  |       |      |
| reindexdb                             |       |      |
| vacuumdb                              |       |      |
| III. PostgreSQL Server Applications   |       |      |
| initdb                                |       |      |
| pg_archivecleanup                     |       |      |
| pg_checksums                          |       |      |
| pg_controldata                        |       |      |
| pg_ctl                                |       |      |
| pg_resetwal                           |       |      |
| pg_rewind                             |       |      |
| pg_test_fsync                         |       |      |
| pg_test_timing                        |       |      |
| pg_upgrade                            |       |      |
| pg_waldump                            |       |      |
| postgres                              |       |      |
| postmaster                            |       |      |
| VII. Internals                        |       |      |
| 51. Overview of PostgreSQL Internals  |       |      |
| 51.1. The Path of a Query             |       |      |
| 51.2. How Connections Are Established |       |      |
| 51.2. How Connections Are Established |       |      |
| 51.4. The PostgreSQL Rule System      |       |      |
| 51.5. Planner/Optimizer               |       |      |
| 21.3. I familier/Optimizer            |       | 2130 |

| 51.6. Executor                 | <br>2159 |
|--------------------------------|----------|
| 52. System Catalogs            |          |
| 52.1. Overview                 |          |
| 52.2. pg aggregate             |          |
| 52.3. pg am                    |          |
| 52.4. pg amop                  |          |
| 52.5. pg amproc                |          |
| 52.6. pg attrdef               |          |
| 52.7. pg attribute             |          |
| 52.8. pg authid                |          |
| 52.9. pg auth members          |          |
| 52.10. pg cast                 |          |
| 52.11. pg class                |          |
| 52.12. pg collation            |          |
| 52.13. pg constraint           |          |
| 52.14. pg conversion           |          |
| 52.15. pg database             |          |
| 52.16. pg db role setting      |          |
| 52.17. pg default acl          |          |
| 52.18. pg depend               |          |
| 52.19. pg description          |          |
| 52.20. pg enum                 |          |
| 52.21. pg event trigger        |          |
| 52.22. pg extension            |          |
| 52.23. pg foreign data wrapper |          |
| 52.24. pg foreign server       |          |
| 52.25. pg foreign table        |          |
| 52.26. pg index                |          |
| 52.27. pg inherits             |          |
| 52.28. pg init privs           |          |
| 52.29. pg language             |          |
| 52.30. pg largeobject          |          |
| 52.31. pg largeobject metadata |          |
| 52.32. pg namespace            |          |
| 52.33. pg opclass              |          |
| 52.34. pg operator             |          |
| 52.35. pg opfamily             |          |
| 52.36. pg partitioned table    |          |
| 52.37. pg policy               |          |
| 52.38. pg proc                 |          |
| 52.39. pg publication          |          |
| 52.40. pg publication rel      |          |
| 52.41. pg range                |          |
| 52.42. pg replication origin   |          |
| 52.43. pg rewrite              |          |
| 52.44. pg seclabel             |          |
| 52.45. pg sequence             |          |
| 52.46. pg shdepend             |          |
| 52.47. pg shdescription        |          |
| 52.48. pg shseclabel           |          |
| 52.49. pg statistic            |          |
| 52.50. pg statistic ext        |          |
| 52.51. pg statistic ext data   |          |
| 52.52. pg subscription         |          |
| 52.53. pg subscription rel     |          |
| 52.54. pg tablespace           |          |
| 52.55. pg transform            |          |
| 52.56. pg trigger              |          |

|             | 52.57. pg_ts_config                          |      |
|-------------|----------------------------------------------|------|
|             | 52.58. pg_ts_config_map                      | 2207 |
|             | 52.59. pg_ts_dict                            | 2207 |
|             | 52.60. pg ts parser                          | 2207 |
|             | 52.61. pg ts template                        | 2208 |
|             | 52.62. pg type                               | 2208 |
|             | 52.63. pg user mapping                       |      |
|             | 52.64. System Views                          |      |
|             | 52.65. pg available extensions               |      |
|             | 52.66. pg available extension versions       |      |
|             | 52.67. pg backend memory contexts            |      |
|             | 52.68. pg config                             |      |
|             | 52.69. pg cursors                            |      |
|             | 52.70. pg file settings                      |      |
|             | 52.70. pg_file_settings                      |      |
|             | <del>-</del>                                 |      |
|             | 52.72 pg_hba_file_rules                      |      |
|             | 52.73. pg_indexes                            |      |
|             | 52.74. pg_locks                              |      |
|             | 52.75. pg_matviews                           |      |
|             | 52.76. pg_policies                           |      |
|             | 52.77. pg_prepared_statements                |      |
|             | 52.78. pg_prepared_xacts                     |      |
|             | 52.79. pg_publication_tables                 |      |
|             | 52.80. pg_replication_origin_status          |      |
|             | 52.81. pg_replication_slots                  |      |
|             | 52.82. pg_roles                              |      |
|             | 52.83. pg_rules                              |      |
|             | 52.84. pg_seclabels                          | 2226 |
|             | 52.85. pg sequences                          | 2227 |
|             | 52.86. pg settings                           | 2228 |
|             | 52.87. pg shadow                             |      |
|             | 52.88. pg shmem allocations                  |      |
|             | 52.89. pg stats                              |      |
|             | 52.90. pg stats ext                          |      |
|             | 52.91. pg stats ext exprs                    |      |
|             | 52.92. pg tables                             |      |
|             | 52.93. pg timezone abbrevs                   |      |
|             | 52.94. pg_timezone_names                     |      |
|             | 52.95. pg_user                               |      |
|             | 52.96. pg user mappings                      |      |
|             | 52.97. pg_views                              |      |
| 53          | Frontend/Backend Protocol                    |      |
| <i>JJ</i> . | 53.1. Overview                               |      |
|             |                                              |      |
|             | 53.2. Message Flow                           |      |
|             | 53.3. SASL Authentication                    |      |
|             | 53.4. Streaming Replication Protocol         |      |
|             | 53.5. Logical Streaming Replication Protocol |      |
|             | 53.6. Message Data Types                     |      |
|             | 53.7. Message Formats                        |      |
|             | 53.8. Error and Notice Message Fields        |      |
|             | 53.9. Logical Replication Message Formats    |      |
|             | 53.10. Summary of Changes since Protocol 2.0 |      |
| 54.         | PostgreSQL Coding Conventions                |      |
|             | 54.1. Formatting                             |      |
|             | 54.2. Reporting Errors Within the Server     |      |
|             | 54.3. Error Message Style Guide              |      |
|             | 54.4. Miscellaneous Coding Conventions       | 2300 |
| 55          | Native I anguage Support                     | 2302 |

|      | 55.1. For the Translator                               | 2302  |
|------|--------------------------------------------------------|-------|
|      | 55.2. For the Programmer                               | 2304  |
| 56.  | Writing a Procedural Language Handler                  | 2308  |
| 57.  | Writing a Foreign Data Wrapper                         | 2310  |
|      | 57.1. Foreign Data Wrapper Functions                   | 2310  |
|      | 57.2. Foreign Data Wrapper Callback Routines           | 2310  |
|      | 57.3. Foreign Data Wrapper Helper Functions            | 2326  |
|      | 57.4. Foreign Data Wrapper Query Planning              | 2327  |
|      | 57.5. Row Locking in Foreign Data Wrappers             |       |
| 58.  | Writing a Table Sampling Method                        |       |
|      | 58.1. Sampling Method Support Functions                | 2331  |
| 59.  | Writing a Custom Scan Provider                         |       |
|      | 59.1. Creating Custom Scan Paths                       |       |
|      | 59.2. Creating Custom Scan Plans                       |       |
|      | 59.3. Executing Custom Scans                           |       |
| 60.  | Genetic Query Optimizer                                |       |
|      | 60.1. Query Handling as a Complex Optimization Problem |       |
|      | 60.2. Genetic Algorithms                               |       |
|      | 60.3. Genetic Query Optimization (GEQO) in PostgreSQL  |       |
|      | 60.4. Further Reading                                  |       |
| 61.  | Table Access Method Interface Definition               |       |
|      | Index Access Method Interface Definition               |       |
| 02.  | 62.1. Basic API Structure for Indexes                  |       |
|      | 62.2. Index Access Method Functions                    |       |
|      | 62.3. Index Scanning                                   |       |
|      | 62.4. Index Locking Considerations                     |       |
|      | 62.5. Index Uniqueness Checks                          |       |
|      | 62.6. Index Cost Estimation Functions                  |       |
| 63   | Generic WAL Records                                    |       |
|      | B-Tree Indexes                                         |       |
| 0 1. | 64.1. Introduction                                     |       |
|      | 64.2. Behavior of B-Tree Operator Classes              |       |
|      | 64.3. B-Tree Support Functions                         |       |
|      | 64.4. Implementation                                   |       |
| 65   | GiST Indexes                                           |       |
| 05.  | 65.1. Introduction                                     |       |
|      | 65.2. Built-in Operator Classes                        |       |
|      | 65.3. Extensibility                                    |       |
|      | 65.4. Implementation                                   |       |
|      | 65.5. Examples                                         |       |
| 66   | SP-GiST Indexes                                        |       |
| 00.  | 66.1. Introduction                                     |       |
|      | 66.2. Built-in Operator Classes                        |       |
|      | 66.3. Extensibility                                    |       |
|      | 66.4. Implementation                                   |       |
|      | 66.5. Examples                                         |       |
| 67   | GIN Indexes                                            |       |
| 07.  | 67.1. Introduction                                     |       |
|      |                                                        |       |
|      | 67.2. Built-in Operator Classes                        |       |
|      | 67.3. Extensibility                                    |       |
|      | 67.4. Implementation                                   |       |
|      | 67.5. GIN Tips and Tricks                              |       |
|      | 67.6. Limitations                                      |       |
| 60   | 67.7. Examples                                         |       |
| υð.  | BRIN Indexes                                           |       |
|      | 68.1. Introduction                                     |       |
|      | 68.2. Built-in Operator Classes                        |       |
|      | 68.3. Extensibility                                    | Z41.3 |

|       | 69. Hash Indexes                                     | 2418 |
|-------|------------------------------------------------------|------|
|       | 69.1. Overview                                       | 2418 |
|       | 69.2. Implementation                                 | 2419 |
|       | 70. Database Physical Storage                        | 2420 |
|       | 70.1. Database File Layout                           | 2420 |
|       | 70.2. TOAST                                          | 2422 |
|       | 70.3. Free Space Map                                 |      |
|       | 70.4. Visibility Map                                 |      |
|       | 70.5. The Initialization Fork                        |      |
|       | 70.6. Database Page Layout                           |      |
|       | 70.7. Heap-Only Tuples (HOT)                         |      |
|       | 71. System Catalog Declarations and Initial Contents |      |
|       | 71.1. System Catalog Declaration Rules               |      |
|       | 71.2. System Catalog Declaration Rules               |      |
|       | 71.2. System Catalog Initial Data                    |      |
|       | 71.4. BKI Commands                                   |      |
|       |                                                      |      |
|       | 71.5. Structure of the Bootstrap BKI File            |      |
|       | 71.6. BKI Example                                    |      |
|       | 72. How the Planner Uses Statistics                  |      |
|       | 72.1. Row Estimation Examples                        |      |
|       | 72.2. Multivariate Statistics Examples               |      |
|       | 72.3. Planner Statistics and Security                |      |
|       | 73. Backup Manifest Format                           |      |
|       | 73.1. Backup Manifest Top-level Object               |      |
|       | 73.2. Backup Manifest File Object                    |      |
|       | 73.3. Backup Manifest WAL Range Object               |      |
| VIII. | Appendixes                                           | 2452 |
|       | A. PostgreSQL Error Codes                            | 2459 |
|       | B. Date/Time Support                                 | 2468 |
|       | B.1. Date/Time Input Interpretation                  | 2468 |
|       | B.2. Handling of Invalid or Ambiguous Timestamps     | 2469 |
|       | B.3. Date/Time Key Words                             |      |
|       | B.4. Date/Time Configuration Files                   |      |
|       | B.5. POSIX Time Zone Specifications                  |      |
|       | B.6. History of Units                                |      |
|       | B.7. Julian Dates                                    |      |
|       | C. SQL Key Words                                     |      |
|       | D. SQL Conformance                                   |      |
|       | D.1. Supported Features                              |      |
|       | D.2. Unsupported Features                            |      |
|       | D.3. XML Limits and Conformance to SQL/XML           |      |
|       | E. Release Notes                                     |      |
|       | E.1. Release 14.22                                   |      |
|       | E.1. Release 14.22  E.2. Release 14.21               |      |
|       |                                                      |      |
|       | E.3. Release 14.20                                   |      |
|       | E.4. Release 14.19                                   |      |
|       | E.5. Release 14.18                                   |      |
|       | E.6. Release 14.17                                   |      |
|       | E.7. Release 14.16                                   |      |
|       | E.8. Release 14.15                                   |      |
|       | E.9. Release 14.14                                   |      |
|       | E.10. Release 14.13                                  |      |
|       | E.11. Release 14.12                                  |      |
|       | E.12. Release 14.11                                  |      |
|       | E.13. Release 14.10                                  |      |
|       | E.14. Release 14.9                                   | 2572 |
|       |                                                      |      |
|       | E.15. Release 14.8 E.16. Release 14.7                |      |

| E.17. Release 14.6              |      |
|---------------------------------|------|
| E.18. Release 14.5              |      |
| E.19. Release 14.4              |      |
| E.20. Release 14.3              | 2595 |
| E.21. Release 14.2              | 2601 |
| E.22. Release 14.1              | 2606 |
| E.23. Release 14                | 2611 |
| E.24. Prior Releases            | 2634 |
| F. Additional Supplied Modules  |      |
| F.1. adminpack                  |      |
| F.2. amcheck                    |      |
| F.3. auth delay                 |      |
| F.4. auto explain               |      |
| F.5. bloom                      |      |
| F.6. btree gin                  |      |
| F.7. btree gist                 |      |
| F.8. citext                     |      |
|                                 |      |
| F.9. cube                       |      |
| F.10. dblink                    |      |
| F.11. dict_int                  |      |
| F.12. dict_xsyn                 |      |
| F.13. earthdistance             |      |
| F.14. file_fdw                  |      |
| F.15. fuzzystrmatch             |      |
| F.16. hstore                    |      |
| F.17. intagg                    |      |
| F.18. intarray                  | 2706 |
| F.19. isn                       | 2709 |
| F.20. lo                        | 2713 |
| F.21. ltree                     | 2714 |
| F.22. old snapshot              | 2721 |
| F.23. pageinspect               | 2721 |
| F.24. passwordcheck             | 2731 |
| F.25. pg buffercache            | 2732 |
| F.26. pgcrypto                  | 2733 |
| F.27. pg freespacemap           | 2744 |
| F.28. pg prewarm                |      |
| F.29. pgrowlocks                |      |
| F.30. pg_stat_statements        |      |
| F.31. pgstattuple               |      |
| F.32. pg surgery                |      |
| F.33. pg_trgm                   |      |
| F.34. pg_visibility             |      |
| F.35. postgres fdw              |      |
| F.36. seg                       |      |
| F.37. sepgsql                   |      |
|                                 |      |
| F.38. spi                       |      |
| F.39. sslinfo                   |      |
| F.40. tablefunc                 |      |
| F.41. ten                       |      |
| F.42. test_decoding             |      |
| F.43. tsm_system_rows           |      |
| F.44. tsm_system_time           |      |
| F.45. unaccent                  |      |
| F.46. uuid-ossp                 |      |
| F.47. xml2                      |      |
| G. Additional Supplied Programs | 2810 |
| G.1. Client Applications        | 2810 |
|                                 |      |

#### PostgreSQL 14.22 Documentation

|        | G.2. Server Applications                            | 2817 |
|--------|-----------------------------------------------------|------|
|        | H. External Projects                                | 2818 |
|        | H.1. Client Interfaces                              | 2818 |
|        | H.2. Administration Tools                           | 2818 |
|        | H.3. Procedural Languages                           | 2818 |
|        | H.4. Extensions                                     | 2818 |
|        | I. The Source Code Repository                       | 2819 |
|        | I.1. Getting the Source via Git                     | 2819 |
|        | J. Documentation                                    | 2820 |
|        | J.1. DocBook                                        | 2820 |
|        | J.2. Tool Sets                                      | 2820 |
|        | J.3. Building the Documentation                     | 2822 |
|        | J.4. Documentation Authoring                        | 2824 |
|        | J.5. Style Guide                                    | 2824 |
|        | K. PostgreSQL Limits                                | 2827 |
|        | L. Acronyms                                         | 2828 |
|        | M. Glossary                                         | 2834 |
|        | N. Color Support                                    | 2846 |
|        | N.1. When Color is Used                             | 2846 |
|        | N.2. Configuring the Colors                         | 2846 |
|        | O. Obsolete or Renamed Features                     |      |
|        | O.1. recovery.conf file merged into postgresql.conf |      |
|        | O.2. Default Roles Renamed to Predefined Roles      | 2847 |
|        | O.3. pg_xlogdump renamed to pg_waldump              | 2847 |
|        | O.4. pg_resetxlog renamed to pg_resetwal            |      |
|        | O.5. pg_receivexlog renamed to pg_receivewal        |      |
| Biblio | ography                                             | 2849 |
| Index  |                                                     | 2851 |

# **List of Figures**

| 60.1. Structure of a Genetic Algorithm | 2340 |
|----------------------------------------|------|
| 67.1. GIN Internals                    | 2402 |
| 70.1. Page Layout                      | 2428 |

## **List of Tables**

| 4.1. Backslash Escape Sequences                               |      |
|---------------------------------------------------------------|------|
| 4.2. Operator Precedence (highest to lowest)                  | . 41 |
| 5.1. ACL Privilege Abbreviations                              |      |
| 5.2. Summary of Access Privileges                             |      |
| 8.1. Data Types                                               |      |
| 8.2. Numeric Types                                            | 144  |
| 8.3. Monetary Types                                           | 149  |
| 8.4. Character Types                                          | 150  |
| 8.5. Special Character Types                                  |      |
| 8.6. Binary Data Types                                        | 152  |
| 8.7. bytea Literal Escaped Octets                             | 153  |
| 8.8. bytea Output Escaped Octets                              |      |
| 8.9. Date/Time Types                                          | 154  |
| 8.10. Date Input                                              | 156  |
| 8.11. Time Input                                              | 156  |
| 8.12. Time Zone Input                                         | 157  |
| 8.13. Special Date/Time Inputs                                |      |
| 8.14. Date/Time Output Styles                                 | 159  |
| 8.15. Date Order Conventions                                  |      |
| 8.16. ISO 8601 Interval Unit Abbreviations                    |      |
| 8.17. Interval Input                                          |      |
| 8.18. Interval Output Style Examples                          |      |
| 8.19. Boolean Data Type                                       |      |
| 8.20. Geometric Types                                         |      |
| 8.21. Network Address Types                                   |      |
| 8.22. cidr Type Input Examples                                |      |
| 8.23. JSON Primitive Types and Corresponding PostgreSQL Types | 179  |
| 8.24. jsonpath Variables                                      | 187  |
| 8.25. jsonpath Accessors                                      |      |
| 8.26. Object Identifier Types                                 |      |
| 8.27. Pseudo-Types                                            |      |
| 9.1. Comparison Operators                                     |      |
| 9.2. Comparison Predicates                                    |      |
| 9.3. Comparison Functions                                     |      |
| 9.4. Mathematical Operators                                   |      |
| 9.5. Mathematical Functions                                   |      |
| 9.6. Random Functions                                         |      |
| 9.7. Trigonometric Functions                                  |      |
| 9.8. Hyperbolic Functions                                     |      |
| 9.9. SQL String Functions and Operators                       |      |
| 9.10. Other String Functions                                  |      |
| 9.11. SQL Binary String Functions and Operators               |      |
| 9.12. Other Binary String Functions                           |      |
| 9.13. Text/Binary String Conversion Functions                 |      |
| 9.14. Bit String Operators                                    |      |
| 9.15. Bit String Functions                                    |      |
| 9.16. Regular Expression Match Operators                      |      |
| 9.17. Regular Expression Atoms                                |      |
|                                                               |      |
| 9.18. Regular Expression Quantifiers                          |      |
| 9.19. Regular Expression Constraints                          |      |
| 9.20. Regular Expression Character-Entry Escapes              |      |
| 9.21. Regular Expression Class-Shorthand Escapes              |      |
| 9.22. Regular Expression Constraint Escapes                   |      |
| 9.23. Regular Expression Back References                      |      |
| 9.24. ARE Embedded-Option Letters                             | 233  |

|       | Formatting Functions                                         |     |
|-------|--------------------------------------------------------------|-----|
|       | Template Patterns for Date/Time Formatting                   |     |
| 9.27. | Template Pattern Modifiers for Date/Time Formatting          | 263 |
|       | Template Patterns for Numeric Formatting                     |     |
|       | Template Pattern Modifiers for Numeric Formatting            |     |
|       | to char Examples                                             |     |
|       | Date/Time Operators                                          |     |
|       | Date/Time Functions                                          |     |
|       | AT TIME ZONE Variants                                        |     |
|       | Enum Support Functions                                       |     |
|       | Geometric Operators                                          |     |
|       |                                                              |     |
|       | Geometric Functions                                          |     |
|       | Geometric Type Conversion Functions                          |     |
|       | IP Address Operators                                         |     |
|       | IP Address Functions                                         |     |
|       | MAC Address Functions                                        |     |
|       | Text Search Operators                                        |     |
|       | Text Search Functions                                        |     |
| 9.43. | Text Search Debugging Functions                              | 299 |
| 9.44. | json and jsonb Operators                                     | 316 |
| 9.45. | Additional jsonb Operators                                   | 317 |
| 9.46. | JSON Creation Functions                                      | 318 |
| 9.47. | JSON Processing Functions                                    | 319 |
| 9.48. | jsonpath Operators and Methods                               | 329 |
|       | jsonpath Filter Expression Elements                          |     |
| 9.50. | Sequence Functions                                           | 333 |
| 9.51. | Array Operators                                              | 338 |
|       | Array Functions                                              |     |
|       | Range Operators                                              |     |
| 9.54. | Multirange Operators                                         | 342 |
| 9.55. | Range Functions                                              | 345 |
| 9.56. | Multirange Functions                                         | 346 |
| 9.57. | General-Purpose Aggregate Functions                          | 347 |
| 9.58. | Aggregate Functions for Statistics                           | 350 |
| 9.59. | Ordered-Set Aggregate Functions                              | 352 |
| 9.60. | Hypothetical-Set Aggregate Functions                         | 352 |
|       | Grouping Operations                                          |     |
| 9.62. | General-Purpose Window Functions                             | 354 |
| 9.63. | Series Generating Functions                                  | 361 |
|       | Subscript Generating Functions                               |     |
| 9.65. | Session Information Functions                                | 364 |
|       | Access Privilege Inquiry Functions                           |     |
| 9.67. | aclitem Operators                                            | 368 |
|       | aclitem Functions                                            |     |
|       | Schema Visibility Inquiry Functions                          |     |
|       | System Catalog Information Functions                         |     |
|       | Index Column Properties                                      |     |
|       | Index Properties                                             |     |
|       | Index Access Method Properties                               |     |
|       | Object Information and Addressing Functions                  |     |
|       | Comment Information Functions                                |     |
|       | Transaction ID and Snapshot Information Functions            |     |
|       | Snapshot Components                                          |     |
|       | Deprecated Transaction ID and Snapshot Information Functions |     |
|       | Committed Transaction Information Functions                  |     |
|       | Control Data Functions                                       |     |
|       | pg control checkpoint Output Columns                         |     |
|       | pg control system Output Columns                             |     |

| 9.83. pg control init Output Columns                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | 381                                                                                                     |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------|
| 9.84. pg_control_recovery Output Columns                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |                                                                                                         |
| 9.85. Configuration Settings Functions                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | 381                                                                                                     |
| 9.86. Server Signaling Functions                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |                                                                                                         |
| 9.87. Backup Control Functions                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |                                                                                                         |
| 9.88. Recovery Information Functions                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | 386                                                                                                     |
| 9.89. Recovery Control Functions                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |                                                                                                         |
| 9.90. Snapshot Synchronization Functions                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |                                                                                                         |
| 9.91. Replication Management Functions                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |                                                                                                         |
| 9.92. Database Object Size Functions                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |                                                                                                         |
| 9.93. Database Object Location Functions                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |                                                                                                         |
| 9.94. Collation Management Functions                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |                                                                                                         |
| 9.95. Partitioning Information Functions                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |                                                                                                         |
| 9.96. Index Maintenance Functions                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |                                                                                                         |
| 9.97. Generic File Access Functions                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |                                                                                                         |
| 9.98. Advisory Lock Functions                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |                                                                                                         |
| 9.99. Built-In Trigger Functions                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |                                                                                                         |
| 9.100. Table Rewrite Information Functions                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |                                                                                                         |
| 12.1. Default Parser's Token Types                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |                                                                                                         |
| 13.1. Transaction Isolation Levels                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |                                                                                                         |
| 13.2. Conflicting Lock Modes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |                                                                                                         |
| 13.3. Conflicting Row-Level Locks                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |                                                                                                         |
| 19.1. System V IPC Parameters                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |                                                                                                         |
| 19.2. SSL Server File Usage                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |                                                                                                         |
| 20.1. synchronous_commit Modes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |                                                                                                         |
| 20.2. Message Severity Levels                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |                                                                                                         |
| 20.3. Short Option Key                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |                                                                                                         |
| 22.1. Predefined Roles                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |                                                                                                         |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |                                                                                                         |
| 24.1. PostgreSQL Character Sets                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |                                                                                                         |
| 24.2. Built-in Client/Server Character Set Conversions                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | 708                                                                                                     |
| <ul><li>24.2. Built-in Client/Server Character Set Conversions</li><li>24.3. All Built-in Character Set Conversions</li></ul>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | 708<br>709                                                                                              |
| <ul> <li>24.2. Built-in Client/Server Character Set Conversions</li> <li>24.3. All Built-in Character Set Conversions</li> <li>27.1. High Availability, Load Balancing, and Replication Feature Matrix</li> </ul>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | 708<br>709<br>744                                                                                       |
| 24.2. Built-in Client/Server Character Set Conversions 24.3. All Built-in Character Set Conversions 27.1. High Availability, Load Balancing, and Replication Feature Matrix 28.1. Dynamic Statistics Views                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | 708<br>709<br>744<br>765                                                                                |
| 24.2. Built-in Client/Server Character Set Conversions 24.3. All Built-in Character Set Conversions 27.1. High Availability, Load Balancing, and Replication Feature Matrix 28.1. Dynamic Statistics Views 28.2. Collected Statistics Views                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | 708<br>709<br>744<br>765<br>766                                                                         |
| 24.2. Built-in Client/Server Character Set Conversions 24.3. All Built-in Character Set Conversions 27.1. High Availability, Load Balancing, and Replication Feature Matrix 28.1. Dynamic Statistics Views 28.2. Collected Statistics Views 28.3. pg_stat_activity View                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | 708<br>709<br>744<br>765<br>768                                                                         |
| 24.2. Built-in Client/Server Character Set Conversions 24.3. All Built-in Character Set Conversions 27.1. High Availability, Load Balancing, and Replication Feature Matrix 28.1. Dynamic Statistics Views 28.2. Collected Statistics Views 28.3. pg_stat_activity View 28.4. Wait Event Types                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | 708<br>709<br>744<br>765<br>766<br>768                                                                  |
| 24.2. Built-in Client/Server Character Set Conversions 24.3. All Built-in Character Set Conversions 27.1. High Availability, Load Balancing, and Replication Feature Matrix 28.1. Dynamic Statistics Views 28.2. Collected Statistics Views 28.3. pg_stat_activity View 28.4. Wait Event Types 28.5. Wait Events of Type Activity                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | 708 709 744 765 766 768 770                                                                             |
| 24.2. Built-in Client/Server Character Set Conversions 24.3. All Built-in Character Set Conversions 27.1. High Availability, Load Balancing, and Replication Feature Matrix 28.1. Dynamic Statistics Views 28.2. Collected Statistics Views 28.3. pg_stat_activity View 28.4. Wait Event Types 28.5. Wait Events of Type Activity 28.6. Wait Events of Type BufferPin                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | 708 709 744 765 766 768 770 771                                                                         |
| 24.2. Built-in Client/Server Character Set Conversions 24.3. All Built-in Character Set Conversions 27.1. High Availability, Load Balancing, and Replication Feature Matrix 28.1. Dynamic Statistics Views 28.2. Collected Statistics Views 28.3. pg_stat_activity View 28.4. Wait Event Types 28.5. Wait Events of Type Activity 28.6. Wait Events of Type BufferPin 28.7. Wait Events of Type Client                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | 708 709 744 765 766 770 771 772                                                                         |
| 24.2. Built-in Client/Server Character Set Conversions 24.3. All Built-in Character Set Conversions 27.1. High Availability, Load Balancing, and Replication Feature Matrix 28.1. Dynamic Statistics Views 28.2. Collected Statistics Views 28.3. pg_stat_activity View 28.4. Wait Event Types 28.5. Wait Events of Type Activity 28.6. Wait Events of Type BufferPin 28.7. Wait Events of Type Client 28.8. Wait Events of Type Extension                                                                                                                                                                                                                                                                                                                                                                                                                                                      | 708 709 744 765 766 770 771 772 772                                                                     |
| 24.2. Built-in Client/Server Character Set Conversions 24.3. All Built-in Character Set Conversions 27.1. High Availability, Load Balancing, and Replication Feature Matrix 28.1. Dynamic Statistics Views 28.2. Collected Statistics Views 28.3. pg_stat_activity View 28.4. Wait Event Types 28.5. Wait Events of Type Activity 28.6. Wait Events of Type BufferPin 28.7. Wait Events of Type Client 28.8. Wait Events of Type Extension 28.9. Wait Events of Type IO                                                                                                                                                                                                                                                                                                                                                                                                                         | 708 709 744 765 766 770 771 771 772 772                                                                 |
| 24.2. Built-in Client/Server Character Set Conversions 24.3. All Built-in Character Set Conversions 27.1. High Availability, Load Balancing, and Replication Feature Matrix 28.1. Dynamic Statistics Views 28.2. Collected Statistics Views 28.3. pg_stat_activity View 28.4. Wait Event Types 28.5. Wait Events of Type Activity 28.6. Wait Events of Type BufferPin 28.7. Wait Events of Type Client 28.8. Wait Events of Type Extension 28.9. Wait Events of Type IO 28.10. Wait Events of Type IPC                                                                                                                                                                                                                                                                                                                                                                                          | 708 709 744 765 768 770 771 771 772 772 772                                                             |
| 24.2. Built-in Client/Server Character Set Conversions 24.3. All Built-in Character Set Conversions 27.1. High Availability, Load Balancing, and Replication Feature Matrix 28.1. Dynamic Statistics Views 28.2. Collected Statistics Views 28.3. pg_stat_activity View 28.4. Wait Event Types 28.5. Wait Events of Type Activity 28.6. Wait Events of Type BufferPin 28.7. Wait Events of Type Client 28.8. Wait Events of Type Extension 28.9. Wait Events of Type IO 28.10. Wait Events of Type IPC 28.11. Wait Events of Type Lock                                                                                                                                                                                                                                                                                                                                                          | 708 709 744 765 766 770 771 771 772 772 775                                                             |
| 24.2. Built-in Client/Server Character Set Conversions 24.3. All Built-in Character Set Conversions 27.1. High Availability, Load Balancing, and Replication Feature Matrix 28.1. Dynamic Statistics Views 28.2. Collected Statistics Views 28.3. pg_stat_activity View 28.4. Wait Event Types 28.5. Wait Events of Type Activity 28.6. Wait Events of Type BufferPin 28.7. Wait Events of Type Client 28.8. Wait Events of Type Extension 28.9. Wait Events of Type IO 28.10. Wait Events of Type IPC 28.11. Wait Events of Type Lock 28.12. Wait Events of Type LWLock                                                                                                                                                                                                                                                                                                                        | 708 709 744 765 766 770 771 771 772 772 775 777                                                         |
| 24.2. Built-in Client/Server Character Set Conversions 24.3. All Built-in Character Set Conversions 27.1. High Availability, Load Balancing, and Replication Feature Matrix 28.1. Dynamic Statistics Views 28.2. Collected Statistics Views 28.3. pg_stat_activity View 28.4. Wait Event Types 28.5. Wait Events of Type Activity 28.6. Wait Events of Type BufferPin 28.7. Wait Events of Type Client 28.8. Wait Events of Type Extension 28.9. Wait Events of Type IO 28.10. Wait Events of Type IPC 28.11. Wait Events of Type Lock 28.12. Wait Events of Type LwLock 28.13. Wait Events of Type Timeout                                                                                                                                                                                                                                                                                     | 708 709 744 765 766 770 771 772 772 775 777 777                                                         |
| 24.2. Built-in Client/Server Character Set Conversions 24.3. All Built-in Character Set Conversions 27.1. High Availability, Load Balancing, and Replication Feature Matrix 28.1. Dynamic Statistics Views 28.2. Collected Statistics Views 28.3. pg_stat_activity View 28.4. Wait Event Types 28.5. Wait Events of Type Activity 28.6. Wait Events of Type BufferPin 28.7. Wait Events of Type Client 28.8. Wait Events of Type Extension 28.9. Wait Events of Type IO 28.10. Wait Events of Type IPC 28.11. Wait Events of Type Lock 28.12. Wait Events of Type LwLock 28.13. Wait Events of Type Timeout 28.14. pg_stat_replication View                                                                                                                                                                                                                                                     | 708 709 744 765 766 770 771 772 772 772 775 777 777                                                     |
| 24.2. Built-in Client/Server Character Set Conversions 24.3. All Built-in Character Set Conversions 27.1. High Availability, Load Balancing, and Replication Feature Matrix 28.1. Dynamic Statistics Views 28.2. Collected Statistics Views 28.3. pg_stat_activity View 28.4. Wait Event Types 28.5. Wait Events of Type Activity 28.6. Wait Events of Type BufferPin 28.7. Wait Events of Type Client 28.8. Wait Events of Type Extension 28.9. Wait Events of Type IO 28.10. Wait Events of Type IPC 28.11. Wait Events of Type Lock 28.12. Wait Events of Type Lock 28.13. Wait Events of Type Timeout 28.14. pg_stat_replication View 28.15. pg_stat_replication_slots View                                                                                                                                                                                                                 | 708 709 744 765 766 770 771 772 772 775 777 780 783                                                     |
| 24.2. Built-in Client/Server Character Set Conversions 24.3. All Built-in Character Set Conversions 27.1. High Availability, Load Balancing, and Replication Feature Matrix 28.1. Dynamic Statistics Views 28.2. Collected Statistics Views 28.3. pg_stat_activity View 28.4. Wait Event Types 28.5. Wait Events of Type Activity 28.6. Wait Events of Type BufferPin 28.7. Wait Events of Type Client 28.8. Wait Events of Type Extension 28.9. Wait Events of Type IPC 28.10. Wait Events of Type IPC 28.11. Wait Events of Type Lock 28.12. Wait Events of Type LwLock 28.13. Wait Events of Type Timeout 28.14. pg_stat_replication View 28.15. pg_stat_wal_receiver View                                                                                                                                                                                                                   | 708 709 744 765 766 770 771 772 772 775 777 780 781 783 784                                             |
| 24.2. Built-in Client/Server Character Set Conversions 24.3. All Built-in Character Set Conversions 27.1. High Availability, Load Balancing, and Replication Feature Matrix 28.1. Dynamic Statistics Views 28.2. Collected Statistics Views 28.3. pg_stat_activity View 28.4. Wait Event Types 28.5. Wait Events of Type Activity 28.6. Wait Events of Type BufferPin 28.7. Wait Events of Type Client 28.8. Wait Events of Type Extension 28.9. Wait Events of Type IPC 28.10. Wait Events of Type IPC 28.11. Wait Events of Type Lock 28.12. Wait Events of Type LwLock 28.13. Wait Events of Type Timeout 28.14. pg_stat_replication View 28.15. pg_stat_wal_receiver View 28.17. pg_stat_subscription View                                                                                                                                                                                  | 708 709 744 765 766 770 771 772 772 775 777 780 781 783 784                                             |
| 24.2. Built-in Client/Server Character Set Conversions 24.3. All Built-in Character Set Conversions 27.1. High Availability, Load Balancing, and Replication Feature Matrix 28.1. Dynamic Statistics Views 28.2. Collected Statistics Views 28.3. pg_stat_activity View 28.4. Wait Event Types 28.5. Wait Events of Type Activity 28.6. Wait Events of Type BufferPin 28.7. Wait Events of Type Client 28.8. Wait Events of Type Extension 28.9. Wait Events of Type IO 28.10. Wait Events of Type IPC 28.11. Wait Events of Type Lock 28.12. Wait Events of Type Lock 28.13. Wait Events of Type Timeout 28.14. pg_stat_replication View 28.15. pg_stat_replication_slots View 28.17. pg_stat_subscription View 28.18. pg_stat_ssl View                                                                                                                                                        | 708 709 744 765 766 770 771 772 772 775 777 780 781 783 785 785                                         |
| 24.2. Built-in Client/Server Character Set Conversions 24.3. All Built-in Character Set Conversions 27.1. High Availability, Load Balancing, and Replication Feature Matrix 28.1. Dynamic Statistics Views 28.2. Collected Statistics Views 28.3. pg_stat_activity View 28.4. Wait Event Types 28.5. Wait Events of Type Activity 28.6. Wait Events of Type BufferPin 28.7. Wait Events of Type Client 28.8. Wait Events of Type Extension 28.9. Wait Events of Type IPC 28.10. Wait Events of Type IPC 28.11. Wait Events of Type Lock 28.12. Wait Events of Type Timeout 28.14. pg_stat_replication View 28.15. pg_stat_replication_slots View 28.16. pg_stat_subscription View 28.17. pg_stat_subscription View 28.18. pg_stat_ssl View 28.19. pg_stat_gssapi View                                                                                                                           | 708 709 744 765 766 770 771 772 772 775 777 780 781 783 784 785 785                                     |
| 24.2. Built-in Client/Server Character Set Conversions 24.3. All Built-in Character Set Conversions 27.1. High Availability, Load Balancing, and Replication Feature Matrix 28.1. Dynamic Statistics Views 28.2. Collected Statistics Views 28.3. pg_stat_activity View 28.4. Wait Event Types 28.5. Wait Events of Type Activity 28.6. Wait Events of Type BufferPin 28.7. Wait Events of Type Client 28.8. Wait Events of Type Extension 28.9. Wait Events of Type IPC 28.10. Wait Events of Type IPC 28.11. Wait Events of Type Lock 28.12. Wait Events of Type Timeout 28.14. pg_stat_replication View 28.15. pg_stat_replication_slots View 28.16. pg_stat_subscription View 28.17. pg_stat_subscription View 28.18. pg_stat_ssl View 28.19. pg_stat_archiver View 28.20. pg_stat_archiver View                                                                                            | 708 709 744 765 766 770 771 772 772 775 777 777 780 781 785 785 786                                     |
| 24.2. Built-in Client/Server Character Set Conversions 24.3. All Built-in Character Set Conversions 27.1. High Availability, Load Balancing, and Replication Feature Matrix 28.1. Dynamic Statistics Views 28.2. Collected Statistics Views 28.3. pg_stat_activity View 28.4. Wait Event Types 28.5. Wait Events of Type Activity 28.6. Wait Events of Type BufferPin 28.7. Wait Events of Type Client 28.8. Wait Events of Type Extension 28.9. Wait Events of Type IO 28.10. Wait Events of Type IPC 28.11. Wait Events of Type Lock 28.12. Wait Events of Type Lock 28.13. Wait Events of Type Timeout 28.14. pg_stat_replication View 28.15. pg_stat_replication_slots View 28.16. pg_stat_subscription View 28.17. pg_stat_subscription View 28.18. pg_stat_archiver View 28.20. pg_stat_archiver View 28.21. pg_stat_bgwriter View                                                        | 708 709 744 765 766 770 771 772 772 772 775 777 780 781 785 785 786 786                                 |
| 24.2. Built-in Client/Server Character Set Conversions 24.3. All Built-in Character Set Conversions 27.1. High Availability, Load Balancing, and Replication Feature Matrix 28.1. Dynamic Statistics Views 28.2. Collected Statistics Views 28.3. pg_stat_activity View 28.4. Wait Event Types 28.5. Wait Events of Type Activity 28.6. Wait Events of Type BufferPin 28.7. Wait Events of Type Extension 28.9. Wait Events of Type ID 28.10. Wait Events of Type IPC 28.11. Wait Events of Type IPC 28.11. Wait Events of Type Lock 28.12. Wait Events of Type LwLock 28.13. Wait Events of Type Timeout 28.14. pg_stat_replication View 28.15. pg_stat_activation View 28.16. pg_stat_subscription View 28.17. pg_stat_subscription View 28.18. pg_stat_activer View 28.19. pg_stat_archiver View 28.20. pg_stat_bysriter View 28.21. pg_stat_bysriter View 28.22. pg_stat_wal View           | 708 709 744 765 766 770 771 772 772 775 777 780 781 783 784 785 786 786 787                             |
| 24.2. Built-in Client/Server Character Set Conversions 24.3. All Built-in Character Set Conversions 27.1. High Availability, Load Balancing, and Replication Feature Matrix 28.1. Dynamic Statistics Views 28.2. Collected Statistics Views 28.3. pg_stat_activity View 28.4. Wait Event Types 28.5. Wait Events of Type Activity 28.6. Wait Events of Type BufferPin 28.7. Wait Events of Type Client 28.8. Wait Events of Type Extension 28.9. Wait Events of Type IO 28.10. Wait Events of Type IPC 28.11. Wait Events of Type Lock 28.12. Wait Events of Type LWLock 28.13. Wait Events of Type Timeout 28.14. pg_stat_replication View 28.15. pg_stat_replication_slots View 28.16. pg_stat_wal_receiver View 28.17. pg_stat_subscription View 28.18. pg_stat_ssl View 28.19. pg_stat_archiver View 28.20. pg_stat_archiver View 28.21. pg_stat_database View 28.22. pg_stat_database View | 708 709 744 765 766 770 771 772 772 775 777 780 781 783 784 785 786 786 787                             |
| 24.2. Built-in Client/Server Character Set Conversions 24.3. All Built-in Character Set Conversions 27.1. High Availability, Load Balancing, and Replication Feature Matrix 28.1. Dynamic Statistics Views 28.2. Collected Statistics Views 28.3. pg_stat_activity View 28.4. Wait Event Types 28.5. Wait Events of Type Activity 28.6. Wait Events of Type BufferPin 28.7. Wait Events of Type Extension 28.9. Wait Events of Type IPC 28.10. Wait Events of Type IPC 28.11. Wait Events of Type IPC 28.13. Wait Events of Type LwLock 28.14. pg_stat_replication View 28.15. pg_stat_replication_slots View 28.16. pg_stat_wal_receiver View 28.17. pg_stat_subscription View 28.18. pg_stat_ssl View 28.19. pg_stat_archiver View 28.20. pg_stat_archiver View 28.20. pg_stat_bal_balance View 28.21. pg_stat_database_conflicts View 28.24. pg_stat_database_conflicts View                 | 708 709 744 765 766 770 771 772 772 775 777 780 781 785 785 785 786 787 788 788                         |
| 24.2. Built-in Client/Server Character Set Conversions 24.3. All Built-in Character Set Conversions 27.1. High Availability, Load Balancing, and Replication Feature Matrix 28.1. Dynamic Statistics Views 28.2. Collected Statistics Views 28.3. pg_stat_activity View 28.4. Wait Event Types 28.5. Wait Events of Type Activity 28.6. Wait Events of Type BufferPin 28.7. Wait Events of Type Client 28.8. Wait Events of Type Extension 28.9. Wait Events of Type IO 28.10. Wait Events of Type IPC 28.11. Wait Events of Type Lock 28.12. Wait Events of Type LWLock 28.13. Wait Events of Type Timeout 28.14. pg_stat_replication View 28.15. pg_stat_replication_slots View 28.16. pg_stat_wal_receiver View 28.17. pg_stat_subscription View 28.18. pg_stat_ssl View 28.19. pg_stat_archiver View 28.20. pg_stat_archiver View 28.21. pg_stat_database View 28.22. pg_stat_database View | 708 709 744 765 766 770 771 772 772 775 777 780 781 785 785 786 786 786 786 787 789 789 789 789 789 789 |

| 28.27. pg_statio_all_tables View 793                                                   |      |
|----------------------------------------------------------------------------------------|------|
| 28.28. pg_statio_all_indexes View 793                                                  |      |
| 28.29. pg_statio_all_sequences View 794                                                |      |
| 28.30. pg_stat_user_functions View 794                                                 |      |
| 28.31. pg_stat_slru View 795                                                           |      |
| 28.32. Additional Statistics Functions 795                                             |      |
| 28.33. Per-Backend Statistics Functions 797                                            |      |
| 28.34. pg_stat_progress_analyze View 798                                               |      |
| 28.35. ANALYZE Phases 799                                                              |      |
| 28.36. pg_stat_progress_create_index View                                              | 800  |
| 28.37. CREATE INDEX Phases 800                                                         |      |
| 28.38. pg_stat_progress_vacuum View 802                                                |      |
| 28.39. VACUUM Phases                                                                   | 802  |
| 28.40. pg_stat_progress_cluster View 803                                               |      |
| 28.41. CLUSTER and VACUUM FULL Phases 804                                              |      |
| 28.42. pg_stat_progress_basebackup View                                                | 804  |
| 28.43. Base Backup Phases                                                              | 805  |
| 28.44. pg_stat_progress_copy View 805                                                  |      |
| 28.45. Built-in DTrace Probes 806                                                      |      |
| 28.46. Defined Types Used in Probe Parameters                                          | 812  |
| 34.1. SSL Mode Descriptions 922                                                        |      |
| 34.2. Libpq/Client SSL File Usage 923                                                  |      |
| 35.1. SQL-Oriented Large Object Functions 942                                          |      |
| 36.1. Mapping Between PostgreSQL Data Types and C Variable Types 958                   |      |
| 36.2. Valid Input Formats for PGTYPESdate_from_asc 976                                 |      |
| 36.3. Valid Input Formats for PGTYPESdate_fmt_asc 978                                  |      |
| 36.4. Valid Input Formats for rdefmtdate 979                                           |      |
| 36.5. Valid Input Formats for PGTYPEStimestamp_from_asc 980                            |      |
| 37.1. information_schema_catalog_name Columns 1058                                     |      |
| 37.2. administrable_role_authorizations Columns 1058<br>37.3. applicable_roles Columns | 1058 |
| 37.4. attributes Columns                                                               | 1059 |
| 37.5. character_sets Columns                                                           | 1061 |
| 37.6. check_constraint_routine_usage Columns 1062                                      |      |
| 37.7. check_constraints Columns                                                        | 1062 |
| 37.8. collations Columns                                                               | 1063 |
| 37.9. collation_character_set_applicability Columns 1063                               |      |
| 37.10. column_column_usage Columns 1064                                                |      |
| 37.11. column_domain_usage Columns 1064                                                |      |
| 37.12. column_options Columns 1065                                                     |      |
| 37.13. column_privileges Columns 1065                                                  |      |
| 37.14. column_udt_usage Columns 1066                                                   |      |
| 37.15. columns Columns 1066                                                            |      |
| 37.16. constraint_column_usage Columns 1069                                            |      |
| 37.17. constraint_table_usage Columns 1070                                             |      |
| 37.18. data_type_privileges Columns 1071                                               |      |
| 37.19. domain_constraints Columns 1071                                                 |      |
| 37.20. domain_udt_usage Columns 1072                                                   |      |
| 37.21. domains Columns 1072                                                            |      |
| 37.22. element_types Columns 1074                                                      |      |
| 37.23. enabled_roles Columns 1076                                                      |      |
| 37.24. foreign_data_wrapper_options Columns 1076                                       |      |
| 37.25. foreign_data_wrappers Columns 1077                                              |      |
| 37.26. foreign_server_options Columns 1077                                             |      |
| 37.27. foreign_servers Columns 1077                                                    |      |
| 37.28. foreign_table_options Columns 1078                                              |      |
| 37.29. foreign_tables Columns 1078                                                     |      |
| 37.30. key_column_usage Columns 1079                                                   |      |

| 37.31. parameters Columns                       |      |
|-------------------------------------------------|------|
| 37.32. referential constraints Columns          | 1081 |
| 37.33. role column grants Columns               |      |
| 37.34. role routine grants Columns              |      |
| 37.35. role table grants Columns                |      |
| 37.36. role udt grants Columns                  |      |
| 37.37. role_usage_grants Columns                |      |
| 37.38. routine column usage Columns             |      |
| 37.39. routine privileges Columns               |      |
| 37.40. routine_routine_usage Columns            |      |
|                                                 |      |
| 37.41. routine_sequence_usage Columns           |      |
| 37.42 routine_table_usage Columns               |      |
| 37.43. routines Columns                         |      |
| 37.44. schemata Columns                         |      |
| 37.45. sequences Columns                        |      |
| 37.46. sql_features Columns                     | 1093 |
| 37.47. sql_implementation_info Columns          | 1094 |
| 37.48. sql parts Columns                        |      |
| 37.49. sql sizing Columns                       | 1095 |
| 37.50. table constraints Columns                |      |
| 37.51. table privileges Columns                 |      |
| 37.52. tables Columns                           |      |
| 37.53. transforms Columns                       |      |
| 37.54. triggered update columns Columns         |      |
| 37.55. triggers Columns                         | 1098 |
| 37.56. udt privileges Columns                   |      |
|                                                 |      |
| 37.57. usage_privileges Columns                 |      |
| 37.58. user_defined_types Columns               | 1101 |
| 37.59. user_mapping_options Columns             |      |
| 37.60. user_mappings Columns                    |      |
| 37.61. view_column_usage Columns                |      |
| 37.62. view_routine_usage Columns               | 1104 |
| 37.63. view_table_usage Columns                 |      |
| 37.64. views Columns                            |      |
| 38.1. Polymorphic Types                         |      |
| 38.2. Equivalent C Types for Built-in SQL Types |      |
| 38.3. B-Tree Strategies                         | 1176 |
| 38.4. Hash Strategies                           | 1177 |
| 38.5. GiST Two-Dimensional "R-tree" Strategies  |      |
| 38.6. SP-GiST Point Strategies                  |      |
| 38.7. GIN Array Strategies                      |      |
| 38.8. BRIN Minmax Strategies                    |      |
| 38.9. B-Tree Support Functions                  |      |
| 38.10. Hash Support Functions                   |      |
| 38.11. GiST Support Functions                   |      |
| **                                              |      |
| 38.12. SP-GiST Support Functions                |      |
| 38.13. GIN Support Functions                    |      |
| 38.14. BRIN Support Functions                   |      |
| 40.1. Event Trigger Support by Command Tag      |      |
| 43.1. Available Diagnostics Items               |      |
| 43.2. Error Diagnostics Items                   |      |
| 281. Policies Applied by Command Type           |      |
| 282. pgbench Automatic Variables                | 1989 |
| 283. pgbench Operators                          | 1992 |
| 284. pgbench Functions                          | 1994 |
| 52.1. System Catalogs                           |      |
| 52.2. pg aggregate Columns                      |      |
| 52.3. pg am Columns                             |      |
| <del></del>                                     |      |

| 52.4. pg amop Columns                  | 21         | 65         |
|----------------------------------------|------------|------------|
| 52.5. pg amproc Columns                |            |            |
| 52.6. pg attrdef Columns               |            |            |
| 52.7. pg attribute Columns             |            |            |
| 52.8. pg authid Columns                |            |            |
| 52.9. pg auth members Columns          |            |            |
| 52.10. pg cast Columns                 |            |            |
| 52.11. pg class Columns                |            |            |
| 52.12. pg collation Columns            |            |            |
| 52.13. pg constraint Columns           |            |            |
| 52.14. pg conversion Columns           |            |            |
| 52.15. pg database Columns             |            |            |
| 52.16. pg db role setting Columns      |            |            |
| 52.17. pg default acl Columns          | . 21<br>21 | 78         |
| 52.18. pg depend Columns               |            |            |
| 52.19. pg description Columns          |            |            |
| 52.20. pg enum Columns                 |            |            |
|                                        |            |            |
| 52.21. pg_event_trigger Columns        |            |            |
| 52.22. pg_extension Columns            |            |            |
| 52.23. pg_foreign_data_wrapper Columns |            |            |
| 52.24. pg_foreign_server Columns       |            |            |
| 52.25. pg_foreign_table Columns        |            |            |
| 52.26. pg_index Columns                |            |            |
| 52.27. pg_inherits Columns             |            |            |
| 52.28. pg_init_privs Columns           |            |            |
| 52.29. pg_language Columns             |            |            |
| 52.30. pg_largeobject Columns          |            |            |
| 52.31. pg_largeobject_metadata Columns | . 21       | 88         |
| 52.32. pg_namespace Columns            |            |            |
| 52.33. pg_opclass Columns              | . 21       | 88         |
| 52.34. pg_operator Columns             |            |            |
| 52.35. pg_opfamily Columns             |            |            |
| 52.36. pg_partitioned_table Columns    | . 21       | 90         |
| 52.37. pg_policy Columns               |            |            |
| 52.38. pg_proc Columns                 | . 21       | 92         |
| 52.39. pg publication Columns          |            |            |
| 52.40. pg publication rel Columns      | . 21       | 95         |
| 52.41. pg range Columns                | . 21       | 95         |
| 52.42. pg replication origin Columns   | . 21       | 96         |
| 52.43. pg rewrite Columns              |            |            |
| 52.44. pg seclabel Columns             | . 21       | 97         |
| 52.45. pg sequence Columns             |            |            |
| 52.46. pg shdepend Columns             |            |            |
| 52.47. pg shdescription Columns        |            |            |
| 52.48. pg shseclabel Columns           |            |            |
| 52.49. pg statistic Columns            |            |            |
| 52.50. pg statistic ext Columns        |            |            |
| 52.51. pg statistic ext data Columns   |            |            |
| 52.52. pg subscription Columns         |            |            |
| 52.52. pg_subscription rel Columns     |            |            |
| 52.53. pg_subscription_ref columns     |            |            |
| 52.55. pg transform Columns            |            |            |
| 52.56. pg trigger Columns              |            |            |
| 52.50. pg_trigger Columns              |            |            |
|                                        |            |            |
| 52.58. pg_ts_config_map Columns        |            |            |
|                                        |            |            |
| 52.60. pg_ts_parser Columns            |            | 208<br>208 |
|                                        | _ / /      | · · · X    |

| 52.62. pg_type Columns                                                |              |
|-----------------------------------------------------------------------|--------------|
| 52.63. typcategory Codes                                              | 2211         |
| 52.64. pg_user_mapping Columns                                        |              |
| 52.65. System Views                                                   | 2212         |
| 52.66. pg available extensions Columns                                | 2213         |
| 52.67. pg available extension versions Columns                        | 2214         |
| 52.68. pg backend memory contexts Columns                             |              |
| 52.69. pg config Columns                                              |              |
| 52.70. pg cursors Columns                                             |              |
| 52.71. pg file settings Columns                                       |              |
| 52.72. pg group Columns                                               |              |
| 52.73. pg hba file rules Columns                                      |              |
| 52.74. pg indexes Columns                                             | 2218         |
| 52.75. pg locks Columns                                               | 2219         |
| 52.76. pg matviews Columns                                            |              |
|                                                                       |              |
| 52.77. pg_policies Columns                                            |              |
| 52.78. pg_prepared_statements Columns                                 |              |
| 52.79. pg_prepared_xacts Columns                                      |              |
| 52.80. pg_publication_tables Columns                                  |              |
| 52.81. pg_replication_origin_status Columns                           | 2224         |
| 52.82. pg_replication_slots Columns                                   | 2224         |
| 52.83. pg roles Columns                                               | 2225         |
| 52.84. pg rules Columns                                               | 2226         |
| 52.85. pg seclabels Columns                                           |              |
| 52.86. pg sequences Columns                                           |              |
| 52.87. pg settings Columns                                            |              |
| 52.88. pg shadow Columns                                              |              |
| 52.89. pg shmem allocations Columns                                   |              |
| 52.90. pg stats Columns                                               | 2231         |
|                                                                       |              |
| 52.91. pg_stats_ext Columns                                           |              |
| 52.92. pg_stats_ext_exprs Columns                                     |              |
| 52.93. pg_tables Columns                                              |              |
| 52.94. pg_timezone_abbrevs Columns                                    |              |
| 52.95. pg_timezone_names Columns                                      | 2236         |
| 52.96. pg_user Columns                                                |              |
| 52.97. pg user mappings Columns                                       | 2237         |
| 52.98. pg views Columns                                               | 2238         |
| 65.1. Built-in GiST Operator Classes                                  |              |
| 66.1. Built-in SP-GiST Operator Classes                               |              |
| 67.1. Built-in GIN Operator Classes                                   |              |
| 68.1. Built-in BRIN Operator Classes                                  |              |
| 68.2. Function and Support Numbers for Minmax Operator Classes        |              |
|                                                                       |              |
| 68.3. Function and Support Numbers for Inclusion Operator Classes     |              |
| 68.4. Procedure and Support Numbers for Bloom Operator Classes        |              |
| 68.5. Procedure and Support Numbers for minmax-multi Operator Classes |              |
| 70.1. Contents of PGDATA                                              |              |
| 70.2. Page Layout                                                     |              |
| 70.3. PageHeaderData Layout                                           | 2427         |
| 70.4. HeapTupleHeaderData Layout                                      | 2428         |
| A.1. PostgreSQL Error Codes                                           |              |
| B.1. Month Names                                                      |              |
| B.2. Day of the Week Names                                            |              |
| B.3. Date/Time Field Modifiers                                        |              |
| C.1. SQL Key Words                                                    |              |
| F.1. adminpack Functions                                              |              |
|                                                                       |              |
| F.2. Cube External Representations                                    |              |
| F.3. Cube Operators  F.4. Cube Functions                              | 2654<br>2654 |
| E 4 LUDE FUNCTIONS                                                    | 70.74        |

#### PostgreSQL 14.22 Documentation

| F.5. Cube-Based Earthdistance Functions                 | 2691 |
|---------------------------------------------------------|------|
| F.6. Point-Based Earthdistance Operators                | 2692 |
| F.7. hstore Operators                                   | 2698 |
| F.8. hstore Functions                                   |      |
| F.9. intarray Functions                                 | 2706 |
| F.10. intarray Operators                                | 2707 |
| F.11. isn Data Types                                    | 2709 |
| F.12. isn Functions                                     | 2711 |
| F.13. ltree Operators                                   | 2716 |
| F.14. ltree Functions                                   | 2717 |
| F.15. pg buffercache Columns                            | 2732 |
| F.16. Supported Algorithms for crypt()                  | 2734 |
| F.17. Iteration Counts for crypt ()                     | 2735 |
| F.18. Hash Algorithm Speeds                             | 2736 |
| F.19. Summary of Functionality with and without OpenSSL | 2743 |
| F.20. pgrowlocks Output Columns                         | 2746 |
| F.21. pg stat statements Columns                        | 2748 |
| F.22. pg stat statements info Columns                   | 2751 |
| F.23. pgstattuple Output Columns                        | 2755 |
| F.24. pgstattuple approx Output Columns                 | 2758 |
| F.25. pg trgm Functions                                 | 2761 |
| F.26. pg trgm Operators                                 |      |
| F.27. seg External Representations                      | 2776 |
| F.28. Examples of Valid seg Input                       | 2776 |
| F.29. Seg GiST Operators                                | 2777 |
| F.30. Sepgsql Functions                                 | 2785 |
| F.31. tablefunc Functions                               | 2789 |
| F.32. connectby Parameters                              | 2796 |
| F.33. Functions for UUID Generation                     | 2804 |
| F.34. Functions Returning UUID Constants                | 2805 |
| F.35. xml2 Functions                                    | 2806 |
| F.36. xpath table Parameters                            | 2807 |
| K.1. PostgreSQL Limitations                             | 2827 |

## **List of Examples**

| 8.1. Using the Character Types                                                        | 151  |
|---------------------------------------------------------------------------------------|------|
| 8.2. Using the boolean Type 164                                                       |      |
| 8.3. Using the Bit String Types 172                                                   |      |
| 9.1. XSLT Stylesheet for Converting SQL/XML Output to HTML                            | 314  |
| 10.1. Square Root Operator Type Resolution 405                                        |      |
| 10.2. String Concatenation Operator Type Resolution 406                               |      |
| 10.3. Absolute-Value and Negation Operator Type Resolution 406                        |      |
| 10.4. Array Inclusion Operator Type Resolution 407                                    |      |
| 10.5. Custom Operator on a Domain Type 407                                            |      |
| 10.6. Rounding Function Argument Type Resolution                                      | 410  |
| 10.7. Variadic Function Resolution 410                                                |      |
| 10.8. Substring Function Type Resolution 411                                          |      |
| 10.9. character Storage Type Conversion 412                                           |      |
| 10.10. Type Resolution with Underspecified Types in a Union 413                       |      |
| 10.11. Type Resolution in a Simple Union 413                                          |      |
| 10.12. Type Resolution in a Transposed Union 414                                      |      |
| 10.13. Type Resolution in a Nested Union 414                                          |      |
| 11.1. Setting up a Partial Index to Exclude Common Values 423                         |      |
| 11.2. Setting up a Partial Index to Exclude Uninteresting Values 424                  |      |
| 11.3. Setting up a Partial Unique Index                                               | 425  |
| 11.4. Do Not Use Partial Indexes as a Substitute for Partitioning 425                 |      |
| 21.1. Example pg_hba.conf Entries 666                                                 |      |
| 21.2. An Example pg_ident.conf File 669                                               |      |
| 34.1. libpq Example Program 1 926                                                     |      |
| 34.2. libpq Example Program 2 929                                                     |      |
| 34.3. libpq Example Program 3 932                                                     |      |
| 35.1. Large Objects with libpq Example Program 943                                    |      |
| 36.1. Example SQLDA Program                                                           | 996  |
| 36.2. ECPG Program Accessing Large Objects 1010                                       |      |
| 42.1. Manual Installation of PL/Perl 1247                                             |      |
| 43.1. Quoting Values in Dynamic Queries 1264                                          |      |
| 43.2. Exceptions with UPDATE/INSERT 1279                                              |      |
| 43.3. A PL/pgSQL Trigger Function 1293                                                |      |
| 43.4. A PL/pgSQL Trigger Function for Auditing 1294                                   |      |
| 43.5. A PL/pgSQL View Trigger Function for Auditing 1295                              |      |
| 43.6. A PL/pgSQL Trigger Function for Maintaining a Summary Table 1296                |      |
| 43.7. Auditing with Transition Tables 1298                                            |      |
| 43.8. A PL/pgSQL Event Trigger Function 1300                                          |      |
| 43.9. Porting a Simple Function from PL/SQL to PL/pgSQL 1308                          |      |
| 43.10. Porting a Function that Creates Another Function from PL/SQL to PL/pgSQL 1309  |      |
| 43.11. Porting a Procedure With String Manipulation and OUT Parameters from PL/SQL to |      |
| PL/pgSQL 1310                                                                         |      |
| 43.12. Porting a Procedure from PL/SQL to PL/pgSQL                                    | 1312 |
| F.1. Create a Foreign Table for PostgreSQL CSV Logs 2693                              |      |

# <span id="page-31-0"></span>**Preface**

This book is the official documentation of PostgreSQL. It has been written by the PostgreSQL developers and other volunteers in parallel to the development of the PostgreSQL software. It describes all the functionality that the current version of PostgreSQL officially supports.

To make the large amount of information about PostgreSQL manageable, this book has been organized in several parts. Each part is targeted at a different class of users, or at users in different stages of their PostgreSQL experience:

- [Part I](#page-38-0) is an informal introduction for new users.
- [Part II](#page-62-0) documents the SQL query language environment, including data types and functions, as well as user-level performance tuning. Every PostgreSQL user should read this.
- Part III describes the installation and administration of the server. Everyone who runs a PostgreSQL server, be it for private use or for others, should read this part.
- Part IV describes the programming interfaces for PostgreSQL client programs.
- Part V contains information for advanced users about the extensibility capabilities of the server. Topics include user-defined data types and functions.
- Part VI contains reference information about SQL commands, client and server programs. This part supports the other parts with structured information sorted by command or program.
- Part VII contains assorted information that might be of use to PostgreSQL developers.

# <span id="page-31-1"></span>**1. What Is PostgreSQL?**

PostgreSQL is an object-relational database management system (ORDBMS) based on [POSTGRES,](https://dsf.berkeley.edu/postgres.md) [Version 4.2](https://dsf.berkeley.edu/postgres.md)<sup>1</sup> , developed at the University of California at Berkeley Computer Science Department. POSTGRES pioneered many concepts that only became available in some commercial database systems much later.

PostgreSQL is an open-source descendant of this original Berkeley code. It supports a large part of the SQL standard and offers many modern features:

- complex queries
- foreign keys
- triggers
- updatable views
- transactional integrity
- multiversion concurrency control

Also, PostgreSQL can be extended by the user in many ways, for example by adding new

- data types
- functions
- operators
- aggregate functions
- index methods
- procedural languages

And because of the liberal license, PostgreSQL can be used, modified, and distributed by anyone free of charge for any purpose, be it private, commercial, or academic.

# <span id="page-31-2"></span>**2. A Brief History of PostgreSQL**

<sup>1</sup> <https://dsf.berkeley.edu/postgres.html>

The object-relational database management system now known as PostgreSQL is derived from the POSTGRES package written at the University of California at Berkeley. With decades of development behind it, PostgreSQL is now the most advanced open-source database available anywhere.

## <span id="page-32-0"></span>2.1. The Berkeley POSTGRES Project

The POSTGRES project, led by Professor Michael Stonebraker, was sponsored by the Defense Advanced Research Projects Agency (DARPA), the Army Research Office (ARO), the National Science Foundation (NSF), and ESL, Inc. The implementation of POSTGRES began in 1986. The initial concepts for the system were presented in [ston86], and the definition of the initial data model appeared in [rowe87]. The design of the rule system at that time was described in [ston87a]. The rationale and architecture of the storage manager were detailed in [ston87b].

POSTGRES has undergone several major releases since then. The first "demoware" system became operational in 1987 and was shown at the 1988 ACM-SIGMOD Conference. Version 1, described in [ston90a], was released to a few external users in June 1989. In response to a critique of the first rule system ([ston89]), the rule system was redesigned ([ston90b]), and Version 2 was released in June 1990 with the new rule system. Version 3 appeared in 1991 and added support for multiple storage managers, an improved query executor, and a rewritten rule system. For the most part, subsequent releases until Postgres95 (see below) focused on portability and reliability.

POSTGRES has been used to implement many different research and production applications. These include: a financial data analysis system, a jet engine performance monitoring package, an asteroid tracking database, a medical information database, and several geographic information systems. POSTGRES has also been used as an educational tool at several universities. Finally, Illustra Information Technologies (later merged into Informix<sup>2</sup>, which is now owned by IBM<sup>3</sup>) picked up the code and commercialized it. In late 1992, POSTGRES became the primary data manager for the Sequoia 2000 scientific computing project described in [ston92].

The size of the external user community nearly doubled during 1993. It became increasingly obvious that maintenance of the prototype code and support was taking up large amounts of time that should have been devoted to database research. In an effort to reduce this support burden, the Berkeley POST-GRES project officially ended with Version 4.2.

## <span id="page-32-1"></span>2.2. Postgres95

In 1994, Andrew Yu and Jolly Chen added an SQL language interpreter to POSTGRES. Under a new name, Postgres95 was subsequently released to the web to find its own way in the world as an open-source descendant of the original POSTGRES Berkeley code.

Postgres95 code was completely ANSI C and trimmed in size by 25%. Many internal changes improved performance and maintainability. Postgres95 release 1.0.x ran about 30–50% faster on the Wisconsin Benchmark compared to POSTGRES, Version 4.2. Apart from bug fixes, the following were the major enhancements:

- The query language PostQUEL was replaced with SQL (implemented in the server). (Interface library libpq was named after PostQUEL.) Subqueries were not supported until PostgreSQL (see below), but they could be imitated in Postgres95 with user-defined SQL functions. Aggregate functions were re-implemented. Support for the GROUP BY query clause was also added.
- A new program (psql) was provided for interactive SQL queries, which used GNU Readline. This largely superseded the old monitor program.
- A new front-end library, libpgtcl, supported Tcl-based clients. A sample shell, pgtclsh, provided new Tcl commands to interface Tcl programs with the Postgres95 server.

<sup>&</sup>lt;sup>2</sup> https://www.ibm.com/analytics/informix

<sup>3</sup> https://www.ibm.com/

- The large-object interface was overhauled. The inversion large objects were the only mechanism for storing large objects. (The inversion file system was removed.)
- The instance-level rule system was removed. Rules were still available as rewrite rules.
- A short tutorial introducing regular SQL features as well as those of Postgres95 was distributed with the source code.
- GNU make (instead of BSD make) was used for the build. Also, Postgres95 could be compiled with an unpatched GCC (data alignment of doubles was fixed).

## <span id="page-33-0"></span>**2.3. PostgreSQL**

By 1996, it became clear that the name "Postgres95" would not stand the test of time. We chose a new name, PostgreSQL, to reflect the relationship between the original POSTGRES and the more recent versions with SQL capability. At the same time, we set the version numbering to start at 6.0, putting the numbers back into the sequence originally begun by the Berkeley POSTGRES project.

Postgres is still considered an official project name, both because of tradition and because people find it easier to pronounce Postgres than PostgreSQL.

The emphasis during development of Postgres95 was on identifying and understanding existing problems in the server code. With PostgreSQL, the emphasis has shifted to augmenting features and capabilities, although work continues in all areas.

Details about what has happened in PostgreSQL since then can be found in Appendix E.

# <span id="page-33-1"></span>**3. Conventions**

The following conventions are used in the synopsis of a command: brackets ([ and ]) indicate optional parts. Braces ({ and }) and vertical lines (|) indicate that you must choose one alternative. Dots (...) mean that the preceding element can be repeated. All other symbols, including parentheses, should be taken literally.

Where it enhances the clarity, SQL commands are preceded by the prompt =>, and shell commands are preceded by the prompt \$. Normally, prompts are not shown, though.

An *administrator* is generally a person who is in charge of installing and running the server. A *user* could be anyone who is using, or wants to use, any part of the PostgreSQL system. These terms should not be interpreted too narrowly; this book does not have fixed presumptions about system administration procedures.

# <span id="page-33-2"></span>**4. Further Information**

Besides the documentation, that is, this book, there are other resources about PostgreSQL:

Wiki

The PostgreSQL [wiki](https://wiki.postgresql.org)<sup>4</sup> contains the project's [FAQ](https://wiki.postgresql.org/wiki/Frequently_Asked_Questions)<sup>5</sup> (Frequently Asked Questions) list, [TODO](https://wiki.postgresql.org/wiki/Todo)<sup>6</sup> list, and detailed information about many more topics.

Web Site

The PostgreSQL [web site](https://www.postgresql.org)<sup>7</sup> carries details on the latest release and other information to make your work or play with PostgreSQL more productive.

<sup>4</sup> <https://wiki.postgresql.org>

<sup>5</sup> [https://wiki.postgresql.org/wiki/Frequently\\_Asked\\_Questions](https://wiki.postgresql.org/wiki/Frequently_Asked_Questions)

<sup>6</sup> <https://wiki.postgresql.org/wiki/Todo>

<sup>7</sup> <https://www.postgresql.org>

#### Mailing Lists

The mailing lists are a good place to have your questions answered, to share experiences with other users, and to contact the developers. Consult the PostgreSQL web site for details.

#### Yourself!

PostgreSQL is an open-source project. As such, it depends on the user community for ongoing support. As you begin to use PostgreSQL, you will rely on others for help, either through the documentation or through the mailing lists. Consider contributing your knowledge back. Read the mailing lists and answer questions. If you learn something which is not in the documentation, write it up and contribute it. If you add features to the code, contribute them.

# <span id="page-34-0"></span>**5. Bug Reporting Guidelines**

When you find a bug in PostgreSQL we want to hear about it. Your bug reports play an important part in making PostgreSQL more reliable because even the utmost care cannot guarantee that every part of PostgreSQL will work on every platform under every circumstance.

The following suggestions are intended to assist you in forming bug reports that can be handled in an effective fashion. No one is required to follow them but doing so tends to be to everyone's advantage.

We cannot promise to fix every bug right away. If the bug is obvious, critical, or affects a lot of users, chances are good that someone will look into it. It could also happen that we tell you to update to a newer version to see if the bug happens there. Or we might decide that the bug cannot be fixed before some major rewrite we might be planning is done. Or perhaps it is simply too hard and there are more important things on the agenda. If you need help immediately, consider obtaining a commercial support contract.

## <span id="page-34-1"></span>**5.1. Identifying Bugs**

Before you report a bug, please read and re-read the documentation to verify that you can really do whatever it is you are trying. If it is not clear from the documentation whether you can do something or not, please report that too; it is a bug in the documentation. If it turns out that a program does something different from what the documentation says, that is a bug. That might include, but is not limited to, the following circumstances:

- A program terminates with a fatal signal or an operating system error message that would point to a problem in the program. (A counterexample might be a "disk full" message, since you have to fix that yourself.)
- A program produces the wrong output for any given input.
- A program refuses to accept valid input (as defined in the documentation).
- A program accepts invalid input without a notice or error message. But keep in mind that your idea of invalid input might be our idea of an extension or compatibility with traditional practice.
- PostgreSQL fails to compile, build, or install according to the instructions on supported platforms.

Here "program" refers to any executable, not only the backend process.

Being slow or resource-hogging is not necessarily a bug. Read the documentation or ask on one of the mailing lists for help in tuning your applications. Failing to comply to the SQL standard is not necessarily a bug either, unless compliance for the specific feature is explicitly claimed.

Before you continue, check on the TODO list and in the FAQ to see if your bug is already known. If you cannot decode the information on the TODO list, report your problem. The least we can do is make the TODO list clearer.

## <span id="page-35-0"></span>**5.2. What to Report**

The most important thing to remember about bug reporting is to state all the facts and only facts. Do not speculate what you think went wrong, what "it seemed to do", or which part of the program has a fault. If you are not familiar with the implementation you would probably guess wrong and not help us a bit. And even if you are, educated explanations are a great supplement to but no substitute for facts. If we are going to fix the bug we still have to see it happen for ourselves first. Reporting the bare facts is relatively straightforward (you can probably copy and paste them from the screen) but all too often important details are left out because someone thought it does not matter or the report would be understood anyway.

The following items should be contained in every bug report:

• The exact sequence of steps *from program start-up* necessary to reproduce the problem. This should be self-contained; it is not enough to send in a bare SELECT statement without the preceding CRE-ATE TABLE and INSERT statements, if the output should depend on the data in the tables. We do not have the time to reverse-engineer your database schema, and if we are supposed to make up our own data we would probably miss the problem.

The best format for a test case for SQL-related problems is a file that can be run through the psql frontend that shows the problem. (Be sure to not have anything in your ~/.psqlrc start-up file.) An easy way to create this file is to use pg\_dump to dump out the table declarations and data needed to set the scene, then add the problem query. You are encouraged to minimize the size of your example, but this is not absolutely necessary. If the bug is reproducible, we will find it either way.

If your application uses some other client interface, such as PHP, then please try to isolate the offending queries. We will probably not set up a web server to reproduce your problem. In any case remember to provide the exact input files; do not guess that the problem happens for "large files" or "midsize databases", etc. since this information is too inexact to be of use.

• The output you got. Please do not say that it "didn't work" or "crashed". If there is an error message, show it, even if you do not understand it. If the program terminates with an operating system error, say which. If nothing at all happens, say so. Even if the result of your test case is a program crash or otherwise obvious it might not happen on our platform. The easiest thing is to copy the output from the terminal, if possible.

#### **Note**

If you are reporting an error message, please obtain the most verbose form of the message. In psql, say \set VERBOSITY verbose beforehand. If you are extracting the message from the server log, set the run-time parameter log\_error\_verbosity to verbose so that all details are logged.

#### **Note**

In case of fatal errors, the error message reported by the client might not contain all the information available. Please also look at the log output of the database server. If you do not keep your server's log output, this would be a good time to start doing so.

• The output you expected is very important to state. If you just write "This command gives me that output." or "This is not what I expected.", we might run it ourselves, scan the output, and think it looks OK and is exactly what we expected. We should not have to spend the time to decode the exact semantics behind your commands. Especially refrain from merely saying that "This is not what SQL says/Oracle does." Digging out the correct behavior from SQL is not a fun undertaking, nor do we all know how all the other relational databases out there behave. (If your problem is a program crash, you can obviously omit this item.)

- Any command line options and other start-up options, including any relevant environment variables or configuration files that you changed from the default. Again, please provide exact information. If you are using a prepackaged distribution that starts the database server at boot time, you should try to find out how that is done.
- Anything you did at all differently from the installation instructions.
- The PostgreSQL version. You can run the command SELECT version(); to find out the version of the server you are connected to. Most executable programs also support a --version option; at least postgres --version and psql --version should work. If the function or the options do not exist then your version is more than old enough to warrant an upgrade. If you run a prepackaged version, such as RPMs, say so, including any subversion the package might have. If you are talking about a Git snapshot, mention that, including the commit hash.

If your version is older than 14.22 we will almost certainly tell you to upgrade. There are many bug fixes and improvements in each new release, so it is quite possible that a bug you have encountered in an older release of PostgreSQL has already been fixed. We can only provide limited support for sites using older releases of PostgreSQL; if you require more than we can provide, consider acquiring a commercial support contract.

• Platform information. This includes the kernel name and version, C library, processor, memory information, and so on. In most cases it is sufficient to report the vendor and version, but do not assume everyone knows what exactly "Debian" contains or that everyone runs on x86\_64. If you have installation problems then information about the toolchain on your machine (compiler, make, and so on) is also necessary.

Do not be afraid if your bug report becomes rather lengthy. That is a fact of life. It is better to report everything the first time than us having to squeeze the facts out of you. On the other hand, if your input files are huge, it is fair to ask first whether somebody is interested in looking into it. Here is an [article](https://www.chiark.greenend.org.uk/~sgtatham/bugs.md)<sup>8</sup> that outlines some more tips on reporting bugs.

Do not spend all your time to figure out which changes in the input make the problem go away. This will probably not help solving it. If it turns out that the bug cannot be fixed right away, you will still have time to find and share your work-around. Also, once again, do not waste your time guessing why the bug exists. We will find that out soon enough.

When writing a bug report, please avoid confusing terminology. The software package in total is called "PostgreSQL", sometimes "Postgres" for short. If you are specifically talking about the backend process, mention that, do not just say "PostgreSQL crashes". A crash of a single backend process is quite different from crash of the parent "postgres" process; please don't say "the server crashed" when you mean a single backend process went down, nor vice versa. Also, client programs such as the interactive frontend "psql" are completely separate from the backend. Please try to be specific about whether the problem is on the client or server side.

## <span id="page-36-0"></span>**5.3. Where to Report Bugs**

In general, send bug reports to the bug report mailing list at <pgsql-bugs@lists.postgresql.org>. You are requested to use a descriptive subject for your email message, perhaps parts of the error message.

Another method is to fill in the bug report web-form available at the project's [web site](https://www.postgresql.org/)<sup>9</sup> . Entering a bug report this way causes it to be mailed to the <pgsql-bugs@lists.postgresql.org> mailing list.

<sup>8</sup> <https://www.chiark.greenend.org.uk/~sgtatham/bugs.html>

<sup>9</sup> <https://www.postgresql.org/>

If your bug report has security implications and you'd prefer that it not become immediately visible in public archives, don't send it to pgsql-bugs. Security issues can be reported privately to <security@postgresql.org>.

Do not send bug reports to any of the user mailing lists, such as <pgsql-sql@lists.postgresql.org> or <pgsql-general@lists.postgresql.org>. These mailing lists are for answering user questions, and their subscribers normally do not wish to receive bug reports. More importantly, they are unlikely to fix them.

Also, please do *not* send reports to the developers' mailing list <pgsql-hackers@lists.postgresql.org>. This list is for discussing the development of PostgreSQL, and it would be nice if we could keep the bug reports separate. We might choose to take up a discussion about your bug report on pgsql-hackers, if the problem needs more review.

If you have a problem with the documentation, the best place to report it is the documentation mailing list <pgsql-docs@lists.postgresql.org>. Please be specific about what part of the documentation you are unhappy with.

If your bug is a portability problem on a non-supported platform, send mail to <pgsql-hackers@lists.postgresql.org>, so we (and you) can work on porting PostgreSQL to your platform.

#### **Note**

Due to the unfortunate amount of spam going around, all of the above lists will be moderated unless you are subscribed. That means there will be some delay before the email is delivered. If you wish to subscribe to the lists, please visit <https://lists.postgresql.org/> for instructions.

# **Part I. Tutorial**

<span id="page-38-0"></span>Welcome to the PostgreSQL Tutorial. The following few chapters are intended to give a simple introduction to PostgreSQL, relational database concepts, and the SQL language to those who are new to any one of these aspects. We only assume some general knowledge about how to use computers. No particular Unix or programming experience is required. This part is mainly intended to give you some hands-on experience with important aspects of the PostgreSQL system. It makes no attempt to be a complete or thorough treatment of the topics it covers.

After you have worked through this tutorial you might want to move on to reading [Part II](#page-62-0) to gain a more formal knowledge of the SQL language, or Part IV for information about developing applications for PostgreSQL. Those who set up and manage their own server should also read Part III.

## **Table of Contents**

| 1. Getting Started                |
|-----------------------------------|
| 1.1. Installation                 |
| 1.2. Architectural Fundamentals   |
| 1.3. Creating a Database          |
| 1.4. Accessing a Database         |
| 2. The SQL Language               |
| 2.1. Introduction                 |
| 2.2. Concepts                     |
| 2.3. Creating a New Table         |
| 2.4. Populating a Table With Rows |
| 2.5. Querying a Table             |
| 2.6. Joins Between Tables         |
| 2.7. Aggregate Functions          |
| 2.8. Updates                      |
| 2.9. Deletions                    |
| 3. Advanced Features              |
| 3.1. Introduction                 |
| 3.2. Views                        |
| 3.3. Foreign Keys                 |
| 3.4. Transactions                 |
| 3.5. Window Functions             |
| 3.6. Inheritance                  |
| 3.7. Conclusion                   |

# <span id="page-40-0"></span>**Chapter 1. Getting Started**

# <span id="page-40-1"></span>**1.1. Installation**

Before you can use PostgreSQL you need to install it, of course. It is possible that PostgreSQL is already installed at your site, either because it was included in your operating system distribution or because the system administrator already installed it. If that is the case, you should obtain information from the operating system documentation or your system administrator about how to access PostgreSQL.

If you are not sure whether PostgreSQL is already available or whether you can use it for your experimentation then you can install it yourself. Doing so is not hard and it can be a good exercise. PostgreSQL can be installed by any unprivileged user; no superuser (root) access is required.

If you are installing PostgreSQL yourself, then refer to Chapter 17 for instructions on installation, and return to this guide when the installation is complete. Be sure to follow closely the section about setting up the appropriate environment variables.

If your site administrator has not set things up in the default way, you might have some more work to do. For example, if the database server machine is a remote machine, you will need to set the PGHOST environment variable to the name of the database server machine. The environment variable PGPORT might also have to be set. The bottom line is this: if you try to start an application program and it complains that it cannot connect to the database, you should consult your site administrator or, if that is you, the documentation to make sure that your environment is properly set up. If you did not understand the preceding paragraph then read the next section.

# <span id="page-40-2"></span>**1.2. Architectural Fundamentals**

Before we proceed, you should understand the basic PostgreSQL system architecture. Understanding how the parts of PostgreSQL interact will make this chapter somewhat clearer.

In database jargon, PostgreSQL uses a client/server model. A PostgreSQL session consists of the following cooperating processes (programs):

- A server process, which manages the database files, accepts connections to the database from client applications, and performs database actions on behalf of the clients. The database server program is called postgres.
- The user's client (frontend) application that wants to perform database operations. Client applications can be very diverse in nature: a client could be a text-oriented tool, a graphical application, a web server that accesses the database to display web pages, or a specialized database maintenance tool. Some client applications are supplied with the PostgreSQL distribution; most are developed by users.

As is typical of client/server applications, the client and the server can be on different hosts. In that case they communicate over a TCP/IP network connection. You should keep this in mind, because the files that can be accessed on a client machine might not be accessible (or might only be accessible using a different file name) on the database server machine.

The PostgreSQL server can handle multiple concurrent connections from clients. To achieve this it starts ("forks") a new process for each connection. From that point on, the client and the new server process communicate without intervention by the original postgres process. Thus, the supervisor server process is always running, waiting for client connections, whereas client and associated server processes come and go. (All of this is of course invisible to the user. We only mention it here for completeness.)

# <span id="page-40-3"></span>**1.3. Creating a Database**

The first test to see whether you can access the database server is to try to create a database. A running PostgreSQL server can manage many databases. Typically, a separate database is used for each project or for each user.

Possibly, your site administrator has already created a database for your use. In that case you can omit this step and skip ahead to the next section.

To create a new database, in this example named mydb, you use the following command:

#### \$ **createdb mydb**

If this produces no response then this step was successful and you can skip over the remainder of this section.

If you see a message similar to:

```
createdb: command not found
```

then PostgreSQL was not installed properly. Either it was not installed at all or your shell's search path was not set to include it. Try calling the command with an absolute path instead:

#### \$ **/usr/local/pgsql/bin/createdb mydb**

The path at your site might be different. Contact your site administrator or check the installation instructions to correct the situation.

Another response could be this:

```
createdb: error: connection to server on socket "/
tmp/.s.PGSQL.5432" failed: No such file or directory
 Is the server running locally and accepting connections on
 that socket?
```

This means that the server was not started, or it is not listening where createdb expects to contact it. Again, check the installation instructions or consult the administrator.

Another response could be this:

```
createdb: error: connection to server on socket "/
tmp/.s.PGSQL.5432" failed: FATAL: role "joe" does not exist
```

where your own login name is mentioned. This will happen if the administrator has not created a PostgreSQL user account for you. (PostgreSQL user accounts are distinct from operating system user accounts.) If you are the administrator, see Chapter 22 for help creating accounts. You will need to become the operating system user under which PostgreSQL was installed (usually postgres) to create the first user account. It could also be that you were assigned a PostgreSQL user name that is different from your operating system user name; in that case you need to use the -U switch or set the PGUSER environment variable to specify your PostgreSQL user name.

If you have a user account but it does not have the privileges required to create a database, you will see the following:

```
createdb: error: database creation failed: ERROR: permission
 denied to create database
```

Not every user has authorization to create new databases. If PostgreSQL refuses to create databases for you then the site administrator needs to grant you permission to create databases. Consult your site administrator if this occurs. If you installed PostgreSQL yourself then you should log in for the purposes of this tutorial under the user account that you started the server as. <sup>1</sup>

You can also create databases with other names. PostgreSQL allows you to create any number of databases at a given site. Database names must have an alphabetic first character and are limited to 63 bytes in length. A convenient choice is to create a database with the same name as your current user name. Many tools assume that database name as the default, so it can save you some typing. To create that database, simply type:

#### \$ **createdb**

If you do not want to use your database anymore you can remove it. For example, if you are the owner (creator) of the database mydb, you can destroy it using the following command:

#### \$ **dropdb mydb**

(For this command, the database name does not default to the user account name. You always need to specify it.) This action physically removes all files associated with the database and cannot be undone, so this should only be done with a great deal of forethought.

More about createdb and dropdb can be found in createdb and dropdb respectively.

# <span id="page-42-0"></span>**1.4. Accessing a Database**

Once you have created a database, you can access it by:

- Running the PostgreSQL interactive terminal program, called *psql*, which allows you to interactively enter, edit, and execute SQL commands.
- Using an existing graphical frontend tool like pgAdmin or an office suite with ODBC or JDBC support to create and manipulate a database. These possibilities are not covered in this tutorial.
- Writing a custom application, using one of the several available language bindings. These possibilities are discussed further in Part IV.

You probably want to start up psql to try the examples in this tutorial. It can be activated for the mydb database by typing the command:

#### \$ **psql mydb**

If you do not supply the database name then it will default to your user account name. You already discovered this scheme in the previous section using createdb.

In psql, you will be greeted with the following message:

```
psql (14.22)
Type "help" for help.
mydb=>
```

The last line could also be:

<sup>1</sup> As an explanation for why this works: PostgreSQL user names are separate from operating system user accounts. When you connect to a database, you can choose what PostgreSQL user name to connect as; if you don't, it will default to the same name as your current operating system account. As it happens, there will always be a PostgreSQL user account that has the same name as the operating system user that started the server, and it also happens that that user always has permission to create databases. Instead of logging in as that user you can also specify the -U option everywhere to select a PostgreSQL user name to connect as.

```
mydb=#
```

That would mean you are a database superuser, which is most likely the case if you installed the PostgreSQL instance yourself. Being a superuser means that you are not subject to access controls. For the purposes of this tutorial that is not important.

If you encounter problems starting psql then go back to the previous section. The diagnostics of createdb and psql are similar, and if the former worked the latter should work as well.

The last line printed out by psql is the prompt, and it indicates that psql is listening to you and that you can type SQL queries into a work space maintained by psql. Try out these commands:

```
mydb=> SELECT version();
 version
-------------------------------------------------------------------
-----------------------
 PostgreSQL 14.22 on x86_64-pc-linux-gnu, compiled by gcc (Debian
 4.9.2-10) 4.9.2, 64-bit
(1 row)
mydb=> SELECT current_date;
 date
------------
 2016-01-07
(1 row)
mydb=> SELECT 2 + 2;
 ?column?
----------
 4
(1 row)
```

The psql program has a number of internal commands that are not SQL commands. They begin with the backslash character, "\". For example, you can get help on the syntax of various PostgreSQL SQL commands by typing:

```
mydb=> \h
```

To get out of psql, type:

```
mydb=> \q
```

and psql will quit and return you to your command shell. (For more internal commands, type \? at the psql prompt.) The full capabilities of psql are documented in psql. In this tutorial we will not use these features explicitly, but you can use them yourself when it is helpful.

# <span id="page-44-0"></span>**Chapter 2. The SQL Language**

# <span id="page-44-1"></span>**2.1. Introduction**

This chapter provides an overview of how to use SQL to perform simple operations. This tutorial is only intended to give you an introduction and is in no way a complete tutorial on SQL. Numerous books have been written on SQL, including [melt93] and [date97]. You should be aware that some PostgreSQL language features are extensions to the standard.

In the examples that follow, we assume that you have created a database named mydb, as described in the previous chapter, and have been able to start psql.

Examples in this manual can also be found in the PostgreSQL source distribution in the directory src/tutorial/. (Binary distributions of PostgreSQL might not provide those files.) To use those files, first change to that directory and run make:

```
$ cd .../src/tutorial
$ make
```

This creates the scripts and compiles the C files containing user-defined functions and types. Then, to start the tutorial, do the following:

```
$ psql -s mydb
...
mydb=> \i basics.sql
```

The \i command reads in commands from the specified file. psql's -s option puts you in single step mode which pauses before sending each statement to the server. The commands used in this section are in the file basics.sql.

# <span id="page-44-2"></span>**2.2. Concepts**

 PostgreSQL is a *relational database management system* (RDBMS). That means it is a system for managing data stored in *relations*. Relation is essentially a mathematical term for *table*. The notion of storing data in tables is so commonplace today that it might seem inherently obvious, but there are a number of other ways of organizing databases. Files and directories on Unix-like operating systems form an example of a hierarchical database. A more modern development is the object-oriented database.

 Each table is a named collection of *rows*. Each row of a given table has the same set of named *columns*, and each column is of a specific data type. Whereas columns have a fixed order in each row, it is important to remember that SQL does not guarantee the order of the rows within the table in any way (although they can be explicitly sorted for display).

 Tables are grouped into databases, and a collection of databases managed by a single PostgreSQL server instance constitutes a database *cluster*.

# <span id="page-44-3"></span>**2.3. Creating a New Table**

You can create a new table by specifying the table name, along with all column names and their types:

```
CREATE TABLE weather (
 city varchar(80),
 temp_lo int, -- low temperature
 temp_hi int, -- high temperature
 prcp real, -- precipitation
 date date
);
```

You can enter this into psql with the line breaks. psql will recognize that the command is not terminated until the semicolon.

White space (i.e., spaces, tabs, and newlines) can be used freely in SQL commands. That means you can type the command aligned differently than above, or even all on one line. Two dashes ("--") introduce comments. Whatever follows them is ignored up to the end of the line. SQL is case insensitive about key words and identifiers, except when identifiers are double-quoted to preserve the case (not done above).

varchar(80) specifies a data type that can store arbitrary character strings up to 80 characters in length. int is the normal integer type. real is a type for storing single precision floating-point numbers. date should be self-explanatory. (Yes, the column of type date is also named date. This might be convenient or confusing — you choose.)

PostgreSQL supports the standard SQL types int, smallint, real, double precision, char(N), varchar(N), date, time, timestamp, and interval, as well as other types of general utility and a rich set of geometric types. PostgreSQL can be customized with an arbitrary number of user-defined data types. Consequently, type names are not key words in the syntax, except where required to support special cases in the SQL standard.

The second example will store cities and their associated geographical location:

```
CREATE TABLE cities (
 name varchar(80),
 location point
);
```

The point type is an example of a PostgreSQL-specific data type.

 Finally, it should be mentioned that if you don't need a table any longer or want to recreate it differently you can remove it using the following command:

```
DROP TABLE tablename;
```

# <span id="page-45-0"></span>**2.4. Populating a Table With Rows**

The INSERT statement is used to populate a table with rows:

```
INSERT INTO weather VALUES ('San Francisco', 46, 50, 0.25,
 '1994-11-27');
```

Note that all data types use rather obvious input formats. Constants that are not simple numeric values usually must be surrounded by single quotes ('), as in the example. The date type is actually quite flexible in what it accepts, but for this tutorial we will stick to the unambiguous format shown here.

The point type requires a coordinate pair as input, as shown here:

```
INSERT INTO cities VALUES ('San Francisco', '(-194.0, 53.0)');
```

The syntax used so far requires you to remember the order of the columns. An alternative syntax allows you to list the columns explicitly:

```
INSERT INTO weather (city, temp_lo, temp_hi, prcp, date)
 VALUES ('San Francisco', 43, 57, 0.0, '1994-11-29');
```

You can list the columns in a different order if you wish or even omit some columns, e.g., if the precipitation is unknown:

```
INSERT INTO weather (date, city, temp_hi, temp_lo)
 VALUES ('1994-11-29', 'Hayward', 54, 37);
```

Many developers consider explicitly listing the columns better style than relying on the order implicitly.

Please enter all the commands shown above so you have some data to work with in the following sections.

 You could also have used COPY to load large amounts of data from flat-text files. This is usually faster because the COPY command is optimized for this application while allowing less flexibility than INSERT. An example would be:

```
COPY weather FROM '/home/user/weather.txt';
```

where the file name for the source file must be available on the machine running the backend process, not the client, since the backend process reads the file directly. The data inserted above into the weather table could also be inserted from a file containing (values are separated by a tab character):

```
San Francisco 46 50 0.25 1994-11-27
San Francisco 43 57 0.0 1994-11-29
Hayward 37 54 \N 1994-11-29
```

You can read more about the COPY command in COPY.

# <span id="page-46-0"></span>**2.5. Querying a Table**

 To retrieve data from a table, the table is *queried*. An SQL SELECT statement is used to do this. The statement is divided into a select list (the part that lists the columns to be returned), a table list (the part that lists the tables from which to retrieve the data), and an optional qualification (the part that specifies any restrictions). For example, to retrieve all the rows of table weather, type:

```
SELECT * FROM weather;
```

Here \* is a shorthand for "all columns". 1 So the same result would be had with:

```
SELECT city, temp_lo, temp_hi, prcp, date FROM weather;
```

The output should be:

```
 city | temp_lo | temp_hi | prcp | date
---------------+---------+---------+------+------------
```

<sup>1</sup> While SELECT \* is useful for off-the-cuff queries, it is widely considered bad style in production code, since adding a column to the table would change the results.

```
 San Francisco | 46 | 50 | 0.25 | 1994-11-27
 San Francisco | 43 | 57 | 0 | 1994-11-29
 Hayward | 37 | 54 | | 1994-11-29
(3 rows)
```

You can write expressions, not just simple column references, in the select list. For example, you can do:

```
SELECT city, (temp_hi+temp_lo)/2 AS temp_avg, date FROM weather;
```

This should give:

| city          |  | temp_avg | date            |
|---------------|--|----------|-----------------|
| ++            |  |          |                 |
| San Francisco |  |          | 48   1994-11-27 |
| San Francisco |  |          | 50   1994-11-29 |
| Hayward       |  |          | 45   1994-11-29 |
| (3 rows)      |  |          |                 |

Notice how the AS clause is used to relabel the output column. (The AS clause is optional.)

A query can be "qualified" by adding a WHERE clause that specifies which rows are wanted. The WHERE clause contains a Boolean (truth value) expression, and only rows for which the Boolean expression is true are returned. The usual Boolean operators (AND, OR, and NOT) are allowed in the qualification. For example, the following retrieves the weather of San Francisco on rainy days:

```
SELECT * FROM weather
 WHERE city = 'San Francisco' AND prcp > 0.0;
```

Result:

```
 city | temp_lo | temp_hi | prcp | date
---------------+---------+---------+------+------------
 San Francisco | 46 | 50 | 0.25 | 1994-11-27
(1 row)
```

You can request that the results of a query be returned in sorted order:

```
SELECT * FROM weather
 ORDER BY city;
```

| city            |  | temp_lo   temp_hi   prcp |    |  | date                   |
|-----------------|--|--------------------------|----|--|------------------------|
| ++++<br>Hayward |  | 37                       | 54 |  | 1994-11-29             |
| San Francisco   |  | 43                       | 57 |  | 0   1994-11-29         |
| San Francisco   |  | 46                       |    |  | 50   0.25   1994-11-27 |

In this example, the sort order isn't fully specified, and so you might get the San Francisco rows in either order. But you'd always get the results shown above if you do:

```
SELECT * FROM weather
 ORDER BY city, temp_lo;
```

You can request that duplicate rows be removed from the result of a query:

```
SELECT DISTINCT city
 FROM weather;
 city
---------------
 Hayward
 San Francisco
(2 rows)
```

Here again, the result row ordering might vary. You can ensure consistent results by using DISTINCT and ORDER BY together: <sup>2</sup>

```
SELECT DISTINCT city
 FROM weather
 ORDER BY city;
```

# <span id="page-48-0"></span>**2.6. Joins Between Tables**

Thus far, our queries have only accessed one table at a time. Queries can access multiple tables at once, or access the same table in such a way that multiple rows of the table are being processed at the same time. Queries that access multiple tables (or multiple instances of the same table) at one time are called *join* queries. They combine rows from one table with rows from a second table, with an expression specifying which rows are to be paired. For example, to return all the weather records together with the location of the associated city, the database needs to compare the city column of each row of the weather table with the name column of all rows in the cities table, and select the pairs of rows where these values match.<sup>3</sup> This would be accomplished by the following query:

```
SELECT * FROM weather JOIN cities ON city = name;
```

```
 city | temp_lo | temp_hi | prcp | date | name 
 | location
---------------+---------+---------+------+------------
+---------------+-----------
 San Francisco | 46 | 50 | 0.25 | 1994-11-27 | San
 Francisco | (-194,53)
 San Francisco | 43 | 57 | 0 | 1994-11-29 | San
 Francisco | (-194,53)
(2 rows)
```

Observe two things about the result set:

- There is no result row for the city of Hayward. This is because there is no matching entry in the cities table for Hayward, so the join ignores the unmatched rows in the weather table. We will see shortly how this can be fixed.
- There are two columns containing the city name. This is correct because the lists of columns from the weather and cities tables are concatenated. In practice this is undesirable, though, so you will probably want to list the output columns explicitly rather than using \*:

<sup>2</sup> In some database systems, including older versions of PostgreSQL, the implementation of DISTINCT automatically orders the rows and so ORDER BY is unnecessary. But this is not required by the SQL standard, and current PostgreSQL does not guarantee that DISTINCT causes the rows to be ordered.

<sup>3</sup> This is only a conceptual model. The join is usually performed in a more efficient manner than actually comparing each possible pair of rows, but this is invisible to the user.

```
SELECT city, temp_lo, temp_hi, prcp, date, location
 FROM weather JOIN cities ON city = name;
```

Since the columns all had different names, the parser automatically found which table they belong to. If there were duplicate column names in the two tables you'd need to *qualify* the column names to show which one you meant, as in:

```
SELECT weather.city, weather.temp_lo, weather.temp_hi,
 weather.prcp, weather.date, cities.location
 FROM weather JOIN cities ON weather.city = cities.name;
```

It is widely considered good style to qualify all column names in a join query, so that the query won't fail if a duplicate column name is later added to one of the tables.

Join queries of the kind seen thus far can also be written in this form:

```
SELECT *
 FROM weather, cities
 WHERE city = name;
```

This syntax pre-dates the JOIN/ON syntax, which was introduced in SQL-92. The tables are simply listed in the FROM clause, and the comparison expression is added to the WHERE clause. The results from this older implicit syntax and the newer explicit JOIN/ON syntax are identical. But for a reader of the query, the explicit syntax makes its meaning easier to understand: The join condition is introduced by its own key word whereas previously the condition was mixed into the WHERE clause together with other conditions.

Now we will figure out how we can get the Hayward records back in. What we want the query to do is to scan the weather table and for each row to find the matching cities row(s). If no matching row is found we want some "empty values" to be substituted for the cities table's columns. This kind of query is called an *outer join*. (The joins we have seen so far are *inner joins*.) The command looks like this:

```
SELECT *
 FROM weather LEFT OUTER JOIN cities ON weather.city =
 cities.name;
 city | temp_lo | temp_hi | prcp | date | name 
 | location
---------------+---------+---------+------+------------
+---------------+-----------
 Hayward | 37 | 54 | | 1994-11-29 | 
 |
 San Francisco | 46 | 50 | 0.25 | 1994-11-27 | San
 Francisco | (-194,53)
 San Francisco | 43 | 57 | 0 | 1994-11-29 | San
 Francisco | (-194,53)
(3 rows)
```

This query is called a *left outer join* because the table mentioned on the left of the join operator will have each of its rows in the output at least once, whereas the table on the right will only have those rows output that match some row of the left table. When outputting a left-table row for which there is no right-table match, empty (null) values are substituted for the right-table columns.

**Exercise:** There are also right outer joins and full outer joins. Try to find out what those do.

We can also join a table against itself. This is called a *self join*. As an example, suppose we wish to find all the weather records that are in the temperature range of other weather records. So we need to compare the temp\_lo and temp\_hi columns of each weather row to the temp\_lo and temp\_hi columns of all other weather rows. We can do this with the following query:

```
SELECT w1.city, w1.temp_lo AS low, w1.temp_hi AS high,
 w2.city, w2.temp_lo AS low, w2.temp_hi AS high
 FROM weather w1 JOIN weather w2
 ON w1.temp_lo < w2.temp_lo AND w1.temp_hi > w2.temp_hi;
 city | low | high | city | low | high
---------------+-----+------+---------------+-----+------
 San Francisco | 43 | 57 | San Francisco | 46 | 50
 Hayward | 37 | 54 | San Francisco | 46 | 50
(2 rows)
```

Here we have relabeled the weather table as w1 and w2 to be able to distinguish the left and right side of the join. You can also use these kinds of aliases in other queries to save some typing, e.g.:

```
SELECT *
 FROM weather w JOIN cities c ON w.city = c.name;
```

You will encounter this style of abbreviating quite frequently.

# <span id="page-50-0"></span>**2.7. Aggregate Functions**

Like most other relational database products, PostgreSQL supports *aggregate functions*. An aggregate function computes a single result from multiple input rows. For example, there are aggregates to compute the count, sum, avg (average), max (maximum) and min (minimum) over a set of rows.

As an example, we can find the highest low-temperature reading anywhere with:

```
SELECT max(temp_lo) FROM weather;
 max
-----
 46
(1 row)
```

If we wanted to know what city (or cities) that reading occurred in, we might try:

```
SELECT city FROM weather WHERE temp_lo = max(temp_lo); WRONG
```

but this will not work since the aggregate max cannot be used in the WHERE clause. (This restriction exists because the WHERE clause determines which rows will be included in the aggregate calculation; so obviously it has to be evaluated before aggregate functions are computed.) However, as is often the case the query can be restated to accomplish the desired result, here by using a *subquery*:

```
SELECT city FROM weather
 WHERE temp_lo = (SELECT max(temp_lo) FROM weather);
```

```
 city
---------------
 San Francisco
(1 row)
```

This is OK because the subquery is an independent computation that computes its own aggregate separately from what is happening in the outer query.

 Aggregates are also very useful in combination with GROUP BY clauses. For example, we can get the number of readings and the maximum low temperature observed in each city with:

```
SELECT city, count(*), max(temp_lo)
 FROM weather
 GROUP BY city;
 city | count | max
---------------+-------+-----
 Hayward | 1 | 37
 San Francisco | 2 | 46
(2 rows)
```

which gives us one output row per city. Each aggregate result is computed over the table rows matching that city. We can filter these grouped rows using HAVING:

```
SELECT city, count(*), max(temp_lo)
 FROM weather
 GROUP BY city
 HAVING max(temp_lo) < 40;
 city | count | max
---------+-------+-----
 Hayward | 1 | 37
(1 row)
```

which gives us the same results for only the cities that have all temp\_lo values below 40. Finally, if we only care about cities whose names begin with "S", we might do:

```
SELECT city, count(*), max(temp_lo)
 FROM weather
 WHERE city LIKE 'S%' -- 1
 GROUP BY city;
 city | count | max
---------------+-------+-----
 San Francisco | 2 | 46
(1 row)
```

**[1](#page-51-0)** The LIKE operator does pattern matching and is explained in Section 9.7.

It is important to understand the interaction between aggregates and SQL's WHERE and HAVING clauses. The fundamental difference between WHERE and HAVING is this: WHERE selects input rows before groups and aggregates are computed (thus, it controls which rows go into the aggregate computation), whereas HAVING selects group rows after groups and aggregates are computed. Thus, the WHERE clause must not contain aggregate functions; it makes no sense to try to use an aggregate to determine which rows will be inputs to the aggregates. On the other hand, the HAVING clause always contains aggregate functions. (Strictly speaking, you are allowed to write a HAVING clause that doesn't use aggregates, but it's seldom useful. The same condition could be used more efficiently at the WHERE stage.)

In the previous example, we can apply the city name restriction in WHERE, since it needs no aggregate. This is more efficient than adding the restriction to HAVING, because we avoid doing the grouping and aggregate calculations for all rows that fail the WHERE check.

Another way to select the rows that go into an aggregate computation is to use FILTER, which is a per-aggregate option:

```
SELECT city, count(*) FILTER (WHERE temp_lo < 45), max(temp_lo)
 FROM weather
 GROUP BY city;
 city | count | max
---------------+-------+-----
 Hayward | 1 | 37
 San Francisco | 1 | 46
(2 rows)
```

FILTER is much like WHERE, except that it removes rows only from the input of the particular aggregate function that it is attached to. Here, the count aggregate counts only rows with temp\_lo below 45; but the max aggregate is still applied to all rows, so it still finds the reading of 46.

# <span id="page-52-0"></span>**2.8. Updates**

You can update existing rows using the UPDATE command. Suppose you discover the temperature readings are all off by 2 degrees after November 28. You can correct the data as follows:

```
UPDATE weather
 SET temp_hi = temp_hi - 2, temp_lo = temp_lo - 2
 WHERE date > '1994-11-28';
```

Look at the new state of the data:

```
SELECT * FROM weather;
```

| city                  |  | temp_lo   temp_hi   prcp |    |  | date                   |
|-----------------------|--|--------------------------|----|--|------------------------|
| ++++<br>San Francisco |  | 46                       |    |  | 50   0.25   1994-11-27 |
| San Francisco         |  | 41                       | 55 |  | 0   1994-11-29         |
| Hayward               |  | 35                       | 52 |  | 1994-11-29             |
| (3 rows)              |  |                          |    |  |                        |

# <span id="page-52-1"></span>**2.9. Deletions**

Rows can be removed from a table using the DELETE command. Suppose you are no longer interested in the weather of Hayward. Then you can do the following to delete those rows from the table:

```
DELETE FROM weather WHERE city = 'Hayward';
```

All weather records belonging to Hayward are removed.

SELECT \* FROM weather;

| city                                     | temp_lo   temp_hi   prcp |    |  | date                                     |
|------------------------------------------|--------------------------|----|--|------------------------------------------|
| ++++<br>San Francisco  <br>San Francisco | 46  <br>41               | 55 |  | 50   0.25   1994-11-27<br>0   1994-11-29 |
| (2 rows)                                 |                          |    |  |                                          |

One should be wary of statements of the form

```
DELETE FROM tablename;
```

Without a qualification, DELETE will remove *all* rows from the given table, leaving it empty. The system will not request confirmation before doing this!

# <span id="page-54-0"></span>**Chapter 3. Advanced Features**

# <span id="page-54-1"></span>**3.1. Introduction**

In the previous chapter we have covered the basics of using SQL to store and access your data in PostgreSQL. We will now discuss some more advanced features of SQL that simplify management and prevent loss or corruption of your data. Finally, we will look at some PostgreSQL extensions.

This chapter will on occasion refer to examples found in [Chapter 2](#page-44-0) to change or improve them, so it will be useful to have read that chapter. Some examples from this chapter can also be found in advanced.sql in the tutorial directory. This file also contains some sample data to load, which is not repeated here. (Refer to [Section 2.1](#page-44-1) for how to use the file.)

# <span id="page-54-2"></span>**3.2. Views**

Refer back to the queries in [Section 2.6.](#page-48-0) Suppose the combined listing of weather records and city location is of particular interest to your application, but you do not want to type the query each time you need it. You can create a *view* over the query, which gives a name to the query that you can refer to like an ordinary table:

```
CREATE VIEW myview AS
 SELECT name, temp_lo, temp_hi, prcp, date, location
 FROM weather, cities
 WHERE city = name;
SELECT * FROM myview;
```

Making liberal use of views is a key aspect of good SQL database design. Views allow you to encapsulate the details of the structure of your tables, which might change as your application evolves, behind consistent interfaces.

Views can be used in almost any place a real table can be used. Building views upon other views is not uncommon.

# <span id="page-54-3"></span>**3.3. Foreign Keys**

Recall the weather and cities tables from [Chapter 2](#page-44-0). Consider the following problem: You want to make sure that no one can insert rows in the weather table that do not have a matching entry in the cities table. This is called maintaining the *referential integrity* of your data. In simplistic database systems this would be implemented (if at all) by first looking at the cities table to check if a matching record exists, and then inserting or rejecting the new weather records. This approach has a number of problems and is very inconvenient, so PostgreSQL can do this for you.

The new declaration of the tables would look like this:

```
CREATE TABLE cities (
 name varchar(80) primary key,
 location point
);
CREATE TABLE weather (
 city varchar(80) references cities(name),
 temp_lo int,
```

```
 temp_hi int,
 prcp real,
 date date
);
```

Now try inserting an invalid record:

```
INSERT INTO weather VALUES ('Berkeley', 45, 53, 0.0, '1994-11-28');
ERROR: insert or update on table "weather" violates foreign key
 constraint "weather_city_fkey"
DETAIL: Key (city)=(Berkeley) is not present in table "cities".
```

The behavior of foreign keys can be finely tuned to your application. We will not go beyond this simple example in this tutorial, but just refer you to [Chapter 5](#page-95-0) for more information. Making correct use of foreign keys will definitely improve the quality of your database applications, so you are strongly encouraged to learn about them.

# <span id="page-55-0"></span>**3.4. Transactions**

*Transactions* are a fundamental concept of all database systems. The essential point of a transaction is that it bundles multiple steps into a single, all-or-nothing operation. The intermediate states between the steps are not visible to other concurrent transactions, and if some failure occurs that prevents the transaction from completing, then none of the steps affect the database at all.

For example, consider a bank database that contains balances for various customer accounts, as well as total deposit balances for branches. Suppose that we want to record a payment of \$100.00 from Alice's account to Bob's account. Simplifying outrageously, the SQL commands for this might look like:

```
UPDATE accounts SET balance = balance - 100.00
 WHERE name = 'Alice';
UPDATE branches SET balance = balance - 100.00
 WHERE name = (SELECT branch_name FROM accounts WHERE name =
 'Alice');
UPDATE accounts SET balance = balance + 100.00
 WHERE name = 'Bob';
UPDATE branches SET balance = balance + 100.00
 WHERE name = (SELECT branch_name FROM accounts WHERE name =
 'Bob');
```

The details of these commands are not important here; the important point is that there are several separate updates involved to accomplish this rather simple operation. Our bank's officers will want to be assured that either all these updates happen, or none of them happen. It would certainly not do for a system failure to result in Bob receiving \$100.00 that was not debited from Alice. Nor would Alice long remain a happy customer if she was debited without Bob being credited. We need a guarantee that if something goes wrong partway through the operation, none of the steps executed so far will take effect. Grouping the updates into a *transaction* gives us this guarantee. A transaction is said to be *atomic*: from the point of view of other transactions, it either happens completely or not at all.

We also want a guarantee that once a transaction is completed and acknowledged by the database system, it has indeed been permanently recorded and won't be lost even if a crash ensues shortly thereafter. For example, if we are recording a cash withdrawal by Bob, we do not want any chance that the debit to his account will disappear in a crash just after he walks out the bank door. A transactional database guarantees that all the updates made by a transaction are logged in permanent storage (i.e., on disk) before the transaction is reported complete.

Another important property of transactional databases is closely related to the notion of atomic updates: when multiple transactions are running concurrently, each one should not be able to see the incomplete changes made by others. For example, if one transaction is busy totalling all the branch balances, it would not do for it to include the debit from Alice's branch but not the credit to Bob's branch, nor vice versa. So transactions must be all-or-nothing not only in terms of their permanent effect on the database, but also in terms of their visibility as they happen. The updates made so far by an open transaction are invisible to other transactions until the transaction completes, whereupon all the updates become visible simultaneously.

In PostgreSQL, a transaction is set up by surrounding the SQL commands of the transaction with BEGIN and COMMIT commands. So our banking transaction would actually look like:

```
BEGIN;
UPDATE accounts SET balance = balance - 100.00
 WHERE name = 'Alice';
-- etc etc
COMMIT;
```

If, partway through the transaction, we decide we do not want to commit (perhaps we just noticed that Alice's balance went negative), we can issue the command ROLLBACK instead of COMMIT, and all our updates so far will be canceled.

PostgreSQL actually treats every SQL statement as being executed within a transaction. If you do not issue a BEGIN command, then each individual statement has an implicit BEGIN and (if successful) COMMIT wrapped around it. A group of statements surrounded by BEGIN and COMMIT is sometimes called a *transaction block*.

#### **Note**

Some client libraries issue BEGIN and COMMIT commands automatically, so that you might get the effect of transaction blocks without asking. Check the documentation for the interface you are using.

It's possible to control the statements in a transaction in a more granular fashion through the use of *savepoints*. Savepoints allow you to selectively discard parts of the transaction, while committing the rest. After defining a savepoint with SAVEPOINT, you can if needed roll back to the savepoint with ROLLBACK TO. All the transaction's database changes between defining the savepoint and rolling back to it are discarded, but changes earlier than the savepoint are kept.

After rolling back to a savepoint, it continues to be defined, so you can roll back to it several times. Conversely, if you are sure you won't need to roll back to a particular savepoint again, it can be released, so the system can free some resources. Keep in mind that either releasing or rolling back to a savepoint will automatically release all savepoints that were defined after it.

All this is happening within the transaction block, so none of it is visible to other database sessions. When and if you commit the transaction block, the committed actions become visible as a unit to other sessions, while the rolled-back actions never become visible at all.

Remembering the bank database, suppose we debit \$100.00 from Alice's account, and credit Bob's account, only to find later that we should have credited Wally's account. We could do it using savepoints like this:

```
BEGIN;
UPDATE accounts SET balance = balance - 100.00
 WHERE name = 'Alice';
SAVEPOINT my_savepoint;
```

```
UPDATE accounts SET balance = balance + 100.00
 WHERE name = 'Bob';
-- oops ... forget that and use Wally's account
ROLLBACK TO my_savepoint;
UPDATE accounts SET balance = balance + 100.00
 WHERE name = 'Wally';
COMMIT;
```

This example is, of course, oversimplified, but there's a lot of control possible in a transaction block through the use of savepoints. Moreover, ROLLBACK TO is the only way to regain control of a transaction block that was put in aborted state by the system due to an error, short of rolling it back completely and starting again.

# <span id="page-57-0"></span>**3.5. Window Functions**

A *window function* performs a calculation across a set of table rows that are somehow related to the current row. This is comparable to the type of calculation that can be done with an aggregate function. However, window functions do not cause rows to become grouped into a single output row like nonwindow aggregate calls would. Instead, the rows retain their separate identities. Behind the scenes, the window function is able to access more than just the current row of the query result.

Here is an example that shows how to compare each employee's salary with the average salary in his or her department:

```
SELECT depname, empno, salary, avg(salary) OVER (PARTITION BY
 depname) FROM empsalary;
```

| depname   |  |    |   | empno   salary | avg                          |
|-----------|--|----|---|----------------|------------------------------|
|           |  |    |   |                | +++                          |
| develop   |  | 11 |   |                | 5200   5020.0000000000000000 |
| develop   |  |    | 7 |                | 4200   5020.0000000000000000 |
| develop   |  |    | 9 |                | 4500   5020.0000000000000000 |
| develop   |  |    | 8 |                | 6000   5020.0000000000000000 |
| develop   |  | 10 |   |                | 5200   5020.0000000000000000 |
| personnel |  |    | 5 |                | 3500   3700.0000000000000000 |
| personnel |  |    | 2 |                | 3900   3700.0000000000000000 |
| sales     |  |    | 3 |                | 4800   4866.6666666666666667 |
| sales     |  |    | 1 |                | 5000   4866.6666666666666667 |
| sales     |  |    | 4 |                | 4800   4866.6666666666666667 |
| (10 rows) |  |    |   |                |                              |

The first three output columns come directly from the table empsalary, and there is one output row for each row in the table. The fourth column represents an average taken across all the table rows that have the same depname value as the current row. (This actually is the same function as the non-window avg aggregate, but the OVER clause causes it to be treated as a window function and computed across the window frame.)

A window function call always contains an OVER clause directly following the window function's name and argument(s). This is what syntactically distinguishes it from a normal function or nonwindow aggregate. The OVER clause determines exactly how the rows of the query are split up for processing by the window function. The PARTITION BY clause within OVER divides the rows into groups, or partitions, that share the same values of the PARTITION BY expression(s). For each row, the window function is computed across the rows that fall into the same partition as the current row.

You can also control the order in which rows are processed by window functions using ORDER BY within OVER. (The window ORDER BY does not even have to match the order in which the rows are output.) Here is an example:

```
SELECT depname, empno, salary,
 rank() OVER (PARTITION BY depname ORDER BY salary DESC)
FROM empsalary;
```

| depname   |  |    |   | empno   salary   rank |   |
|-----------|--|----|---|-----------------------|---|
| +++       |  |    |   |                       |   |
| develop   |  |    | 8 | 6000                  | 1 |
| develop   |  | 10 |   | 5200                  | 2 |
| develop   |  | 11 |   | 5200                  | 2 |
| develop   |  |    | 9 | 4500                  | 4 |
| develop   |  |    | 7 | 4200                  | 5 |
| personnel |  |    | 2 | 3900                  | 1 |
| personnel |  |    | 5 | 3500                  | 2 |
| sales     |  |    | 1 | 5000                  | 1 |
| sales     |  |    | 4 | 4800                  | 2 |
| sales     |  |    | 3 | 4800                  | 2 |
| (10 rows) |  |    |   |                       |   |

As shown here, the rank function produces a numerical rank for each distinct ORDER BY value in the current row's partition, using the order defined by the ORDER BY clause. rank needs no explicit parameter, because its behavior is entirely determined by the OVER clause.

The rows considered by a window function are those of the "virtual table" produced by the query's FROM clause as filtered by its WHERE, GROUP BY, and HAVING clauses if any. For example, a row removed because it does not meet the WHERE condition is not seen by any window function. A query can contain multiple window functions that slice up the data in different ways using different OVER clauses, but they all act on the same collection of rows defined by this virtual table.

We already saw that ORDER BY can be omitted if the ordering of rows is not important. It is also possible to omit PARTITION BY, in which case there is a single partition containing all rows.

There is another important concept associated with window functions: for each row, there is a set of rows within its partition called its *window frame*. Some window functions act only on the rows of the window frame, rather than of the whole partition. By default, if ORDER BY is supplied then the frame consists of all rows from the start of the partition up through the current row, plus any following rows that are equal to the current row according to the ORDER BY clause. When ORDER BY is omitted the default frame consists of all rows in the partition. <sup>1</sup> Here is an example using sum:

SELECT salary, sum(salary) OVER () FROM empsalary;

| salary    | sum          |
|-----------|--------------|
| +         |              |
|           | 5200   47100 |
|           | 5000   47100 |
|           | 3500   47100 |
|           | 4800   47100 |
|           | 3900   47100 |
|           | 4200   47100 |
|           | 4500   47100 |
|           | 4800   47100 |
|           | 6000   47100 |
|           | 5200   47100 |
| (10 rows) |              |

<sup>1</sup> There are options to define the window frame in other ways, but this tutorial does not cover them. See [Section 4.2.8](#page-84-0) for details.

Above, since there is no ORDER BY in the OVER clause, the window frame is the same as the partition, which for lack of PARTITION BY is the whole table; in other words each sum is taken over the whole table and so we get the same result for each output row. But if we add an ORDER BY clause, we get very different results:

```
SELECT salary, sum(salary) OVER (ORDER BY salary) FROM empsalary;
```

| salary    | sum          |
|-----------|--------------|
| +         |              |
| 3500      | 3500         |
| 3900      | 7400         |
|           | 4200   11600 |
|           | 4500   16100 |
|           | 4800   25700 |
|           | 4800   25700 |
|           | 5000   30700 |
|           | 5200   41100 |
|           | 5200   41100 |
|           | 6000   47100 |
| (10 rows) |              |

Here the sum is taken from the first (lowest) salary up through the current one, including any duplicates of the current one (notice the results for the duplicated salaries).

Window functions are permitted only in the SELECT list and the ORDER BY clause of the query. They are forbidden elsewhere, such as in GROUP BY, HAVING and WHERE clauses. This is because they logically execute after the processing of those clauses. Also, window functions execute after non-window aggregate functions. This means it is valid to include an aggregate function call in the arguments of a window function, but not vice versa.

If there is a need to filter or group rows after the window calculations are performed, you can use a sub-select. For example:

```
SELECT depname, empno, salary, enroll_date
FROM
 (SELECT depname, empno, salary, enroll_date,
 rank() OVER (PARTITION BY depname ORDER BY salary DESC,
 empno) AS pos
 FROM empsalary
 ) AS ss
WHERE pos < 3;
```

The above query only shows the rows from the inner query having rank less than 3.

When a query involves multiple window functions, it is possible to write out each one with a separate OVER clause, but this is duplicative and error-prone if the same windowing behavior is wanted for several functions. Instead, each windowing behavior can be named in a WINDOW clause and then referenced in OVER. For example:

```
SELECT sum(salary) OVER w, avg(salary) OVER w
 FROM empsalary
 WINDOW w AS (PARTITION BY depname ORDER BY salary DESC);
```

More details about window functions can be found in [Section 4.2.8,](#page-84-0) Section 9.22, [Section 7.2.5,](#page-165-1) and the SELECT reference page.

# <span id="page-60-0"></span>**3.6. Inheritance**

Inheritance is a concept from object-oriented databases. It opens up interesting new possibilities of database design.

Let's create two tables: A table cities and a table capitals. Naturally, capitals are also cities, so you want some way to show the capitals implicitly when you list all cities. If you're really clever you might invent some scheme like this:

```
CREATE TABLE capitals (
 name text,
 population real,
 elevation int, -- (in ft)
 state char(2)
);
CREATE TABLE non_capitals (
 name text,
 population real,
 elevation int -- (in ft)
);
CREATE VIEW cities AS
 SELECT name, population, elevation FROM capitals
 UNION
 SELECT name, population, elevation FROM non_capitals;
```

This works OK as far as querying goes, but it gets ugly when you need to update several rows, for one thing.

A better solution is this:

```
CREATE TABLE cities (
 name text,
 population real,
 elevation int -- (in ft)
);
CREATE TABLE capitals (
 state char(2) UNIQUE NOT NULL
) INHERITS (cities);
```

In this case, a row of capitals *inherits* all columns (name, population, and elevation) from its *parent*, cities. The type of the column name is text, a native PostgreSQL type for variable length character strings. The capitals table has an additional column, state, which shows its state abbreviation. In PostgreSQL, a table can inherit from zero or more other tables.

For example, the following query finds the names of all cities, including state capitals, that are located at an elevation over 500 feet:

```
SELECT name, elevation
 FROM cities
 WHERE elevation > 500;
```

which returns:

| name      | elevation |
|-----------|-----------|
|           | +         |
| Las Vegas | 2174      |
| Mariposa  | <br>1953  |
| Madison   | <br>845   |
| (3 rows)  |           |

On the other hand, the following query finds all the cities that are not state capitals and are situated at an elevation over 500 feet:

```
SELECT name, elevation
 FROM ONLY cities
 WHERE elevation > 500;
 name | elevation
-----------+-----------
 Las Vegas | 2174
 Mariposa | 1953
(2 rows)
```

Here the ONLY before cities indicates that the query should be run over only the cities table, and not tables below cities in the inheritance hierarchy. Many of the commands that we have already discussed — SELECT, UPDATE, and DELETE — support this ONLY notation.

#### **Note**

Although inheritance is frequently useful, it has not been integrated with unique constraints or foreign keys, which limits its usefulness. See [Section 5.10](#page-125-0) for more detail.

# <span id="page-61-0"></span>**3.7. Conclusion**

PostgreSQL has many features not touched upon in this tutorial introduction, which has been oriented toward newer users of SQL. These features are discussed in more detail in the remainder of this book.

If you feel you need more introductory material, please visit the PostgreSQL [web site](https://www.postgresql.org)<sup>2</sup> for links to more resources.

<sup>2</sup> <https://www.postgresql.org>

# **Part II. The SQL Language**

<span id="page-62-0"></span>This part describes the use of the SQL language in PostgreSQL. We start with describing the general syntax of SQL, then explain how to create the structures to hold data, how to populate the database, and how to query it. The middle part lists the available data types and functions for use in SQL commands. The rest treats several aspects that are important for tuning a database for optimal performance.

The information in this part is arranged so that a novice user can follow it start to end to gain a full understanding of the topics without having to refer forward too many times. The chapters are intended to be self-contained, so that advanced users can read the chapters individually as they choose. The information in this part is presented in a narrative fashion in topical units. Readers looking for a complete description of a particular command should see Part VI.

Readers of this part should know how to connect to a PostgreSQL database and issue SQL commands. Readers that are unfamiliar with these issues are encouraged to read [Part I](#page-38-0) first. SQL commands are typically entered using the PostgreSQL interactive terminal psql, but other programs that have similar functionality can be used as well.

## **Table of Contents**

| 4. SQL Syntax                            |      |
|------------------------------------------|------|
| 4.1. Lexical Structure                   | . 33 |
| 4.1.1. Identifiers and Key Words         |      |
| 4.1.2. Constants                         | . 35 |
| 4.1.3. Operators                         | . 39 |
| 4.1.4. Special Characters                | . 40 |
| 4.1.5. Comments                          | . 40 |
| 4.1.6. Operator Precedence               | . 41 |
| 4.2. Value Expressions                   | . 42 |
| 4.2.1. Column References                 | . 42 |
| 4.2.2. Positional Parameters             | . 43 |
| 4.2.3. Subscripts                        | . 43 |
| 4.2.4. Field Selection                   |      |
| 4.2.5. Operator Invocations              |      |
| 4.2.6. Function Calls                    |      |
| 4.2.7. Aggregate Expressions             |      |
| 4.2.8. Window Function Calls             |      |
| 4.2.9. Type Casts                        |      |
| 4.2.10. Collation Expressions            |      |
| 4.2.11. Scalar Subqueries                |      |
| 4.2.12. Array Constructors               |      |
| 4.2.13. Row Constructors                 |      |
| 4.2.14. Expression Evaluation Rules      |      |
| 4.3. Calling Functions                   |      |
|                                          |      |
| 4.3.1. Using Positional Notation         |      |
| 4.3.2. Using Named Notation              |      |
| 4.3.3. Using Mixed Notation              |      |
| 5. Data Definition                       |      |
| 5.1. Table Basics                        |      |
| 5.2. Default Values                      |      |
| 5.3. Generated Columns                   |      |
| 5.4. Constraints                         |      |
| 5.4.1. Check Constraints                 |      |
| 5.4.2. Not-Null Constraints              |      |
| 5.4.3. Unique Constraints                |      |
| 5.4.4. Primary Keys                      |      |
| 5.4.5. Foreign Keys                      |      |
| 5.4.6. Exclusion Constraints             | . 69 |
| 5.5. System Columns                      | . 69 |
| 5.6. Modifying Tables                    |      |
| 5.6.1. Adding a Column                   | . 70 |
| 5.6.2. Removing a Column                 | . 71 |
| 5.6.3. Adding a Constraint               | . 71 |
| 5.6.4. Removing a Constraint             | . 72 |
| 5.6.5. Changing a Column's Default Value | . 72 |
| 5.6.6. Changing a Column's Data Type     | . 72 |
| 5.6.7. Renaming a Column                 |      |
| 5.6.8. Renaming a Table                  |      |
| 5.7. Privileges                          |      |
| 5.8. Row Security Policies               |      |
| 5.9. Schemas                             |      |
| 5.9.1. Creating a Schema                 |      |
| 5.9.2. The Public Schema                 |      |
| 5.9.3. The Schema Search Path            |      |
| 5.9.4. Schemas and Privileges            |      |
| э.э.т. эоношая ана т түнөдөг             | . 00 |

| 5.9.5. The System Catalog Schema                    |      |
|-----------------------------------------------------|------|
| 5.9.6. Usage Patterns                               |      |
| 5.9.7. Portability                                  |      |
| 5.10. Inheritance                                   |      |
| 5.10.1. Caveats                                     |      |
| 5.11. Table Partitioning                            | 91   |
| 5.11.1. Overview                                    | 91   |
| 5.11.2. Declarative Partitioning                    | 92   |
| 5.11.3. Partitioning Using Inheritance              | . 97 |
| 5.11.4. Partition Pruning                           | 102  |
| 5.11.5. Partitioning and Constraint Exclusion       | 103  |
| 5.11.6. Best Practices for Declarative Partitioning |      |
| 5.12. Foreign Data                                  |      |
| 5.13. Other Database Objects                        |      |
| 5.14. Dependency Tracking                           |      |
| 6. Data Manipulation                                |      |
| 6.1. Inserting Data                                 |      |
| 6.2. Updating Data                                  |      |
|                                                     |      |
| 6.3. Deleting Data                                  |      |
| 6.4. Returning Data from Modified Rows              |      |
| 7. Queries                                          |      |
| 7.1. Overview                                       |      |
| 7.2. Table Expressions                              |      |
| 7.2.1. The FROM Clause                              |      |
| 7.2.2. The WHERE Clause                             |      |
| 7.2.3. The GROUP BY and HAVING Clauses              |      |
| 7.2.4. GROUPING SETS, CUBE, and ROLLUP              |      |
| 7.2.5. Window Function Processing                   |      |
| 7.3. Select Lists                                   |      |
| 7.3.1. Select-List Items                            | 128  |
| 7.3.2. Column Labels                                | 129  |
| 7.3.3. DISTINCT                                     | 129  |
| 7.4. Combining Queries (UNION, INTERSECT, EXCEPT)   | 130  |
| 7.5. Sorting Rows (ORDER BY)                        |      |
| 7.6. LIMIT and OFFSET                               |      |
| 7.7. VALUES Lists                                   |      |
| 7.8. WITH Queries (Common Table Expressions)        |      |
| 7.8.1. SELECT in WITH                               |      |
| 7.8.2. Recursive Queries                            |      |
| 7.8.3. Common Table Expression Materialization      |      |
| 7.8.4. Data-Modifying Statements in WITH            |      |
| 8. Data Types                                       |      |
|                                                     |      |
| 8.1. Numeric Types                                  |      |
| 8.1.1. Integer Types                                |      |
| 8.1.2. Arbitrary Precision Numbers                  |      |
| 8.1.3. Floating-Point Types                         |      |
| 8.1.4. Serial Types                                 |      |
| 8.2. Monetary Types                                 |      |
| 8.3. Character Types                                |      |
| 8.4. Binary Data Types                              |      |
| 8.4.1. bytea Hex Format                             |      |
| 8.4.2. bytea Escape Format                          |      |
| 8.5. Date/Time Types                                |      |
| 8.5.1. Date/Time Input                              |      |
| 8.5.2. Date/Time Output                             |      |
| 8.5.3. Time Zones                                   | 160  |
| 8.5.4. Interval Input                               | 161  |
| 8.5.5. Interval Output                              |      |

| 8.6. Boolean Type                              | . 164 |
|------------------------------------------------|-------|
| 8.7. Enumerated Types                          | 165   |
| 8.7.1. Declaration of Enumerated Types         | . 165 |
| 8.7.2. Ordering                                | 165   |
| 8.7.3. Type Safety                             | . 166 |
| 8.7.4. Implementation Details                  | . 166 |
| 8.8. Geometric Types                           | 167   |
| 8.8.1. Points                                  | . 167 |
| 8.8.2. Lines                                   | . 167 |
| 8.8.3. Line Segments                           | . 167 |
| 8.8.4. Boxes                                   | . 168 |
| 8.8.5. Paths                                   | . 168 |
| 8.8.6. Polygons                                | . 168 |
| 8.8.7. Circles                                 | . 169 |
| 8.9. Network Address Types                     |       |
| 8.9.1. inet                                    | 169   |
| 8.9.2. cidr                                    | 170   |
| 8.9.3. inet vs. cidr                           | 170   |
| 8.9.4. macaddr                                 | 170   |
| 8.9.5. macaddr8                                | 171   |
| 8.10. Bit String Types                         | 171   |
| 8.11. Text Search Types                        | . 172 |
| 8.11.1. tsvector                               | . 172 |
| 8.11.2. tsquery                                | . 174 |
| 8.12. UUID Type                                |       |
| 8.13. XML Type                                 | . 175 |
| 8.13.1. Creating XML Values                    |       |
| 8.13.2. Encoding Handling                      |       |
| 8.13.3. Accessing XML Values                   | . 177 |
| 8.14. JSON Types                               |       |
| 8.14.1. JSON Input and Output Syntax           | 179   |
| 8.14.2. Designing JSON Documents               |       |
| 8.14.3. jsonb Containment and Existence        |       |
| 8.14.4. jsonb Indexing                         |       |
| 8.14.5. jsonb Subscripting                     |       |
| 8.14.6. Transforms                             |       |
| 8.14.7. jsonpath Type                          |       |
| 8.15. Arrays                                   |       |
| 8.15.1. Declaration of Array Types             |       |
| 8.15.2. Array Value Input                      |       |
| 8.15.3. Accessing Arrays                       |       |
| 8.15.4. Modifying Arrays                       |       |
| 8.15.5. Searching in Arrays                    |       |
| 8.15.6. Array Input and Output Syntax          |       |
| 8.16. Composite Types                          |       |
| 8.16.1. Declaration of Composite Types         |       |
| 8.16.2. Constructing Composite Values          |       |
| 8.16.3. Accessing Composite Types              |       |
| 8.16.4. Modifying Composite Types              |       |
| 8.16.5. Using Composite Types in Queries       |       |
| 8.16.6. Composite Type Input and Output Syntax |       |
| 8.17. Range Types                              |       |
| 8.17.1. Built-in Range and Multirange Types    |       |
| 8.17.2. Examples                               | 204   |
| 8.17.3. Inclusive and Exclusive Bounds         |       |
| 8.17.4. Infinite (Unbounded) Ranges            |       |
| 8.17.5. Range Input/Output                     |       |
| 0.17.0. Constructing ranges and multiranges    | . ∠∪0 |

|    | 8.17.7. Discrete Range Types                   | . 207 |
|----|------------------------------------------------|-------|
|    | 8.17.8. Defining New Range Types               | 207   |
|    | 8.17.9. Indexing                               | 208   |
|    | 8.17.10. Constraints on Ranges                 |       |
|    | 8.18. Domain Types                             |       |
|    | 8.19. Object Identifier Types                  |       |
|    | 8.20. pg lsn Type                              |       |
|    | 8.21. Pseudo-Types                             |       |
| 9. | Functions and Operators                        |       |
|    | 9.1. Logical Operators                         |       |
|    | 9.2. Comparison Functions and Operators        |       |
|    | 9.3. Mathematical Functions and Operators      |       |
|    | 9.4. String Functions and Operators            |       |
|    | 9.4.1. format                                  |       |
|    | 9.5. Binary String Functions and Operators     |       |
|    | 9.6. Bit String Functions and Operators        |       |
|    | 9.7. Pattern Matching                          |       |
|    | 9.7.1 LIKE                                     |       |
|    | 9.7.2. SIMILAR TO Regular Expressions          |       |
|    |                                                |       |
|    | 9.7.3. POSIX Regular Expressions               |       |
|    | 9.8. Data Type Formatting Functions            |       |
|    | 9.9. Date/Time Functions and Operators         |       |
|    | 9.9.1. EXTRACT, date_part                      |       |
|    | 9.9.2. date_trunc                              |       |
|    | 9.9.3. date_bin                                |       |
|    | 9.9.4. AT TIME ZONE                            |       |
|    | 9.9.5. Current Date/Time                       |       |
|    | 9.9.6. Delaying Execution                      |       |
|    | 9.10. Enum Support Functions                   |       |
|    | 9.11. Geometric Functions and Operators        |       |
|    | 9.12. Network Address Functions and Operators  |       |
|    | 9.13. Text Search Functions and Operators      |       |
|    | 9.14. UUID Functions                           |       |
|    | 9.15. XML Functions                            |       |
|    | 9.15.1. Producing XML Content                  |       |
|    | 9.15.2. XML Predicates                         |       |
|    | 9.15.3. Processing XML                         | 307   |
|    | 9.15.4. Mapping Tables to XML                  | 311   |
|    | 9.16. JSON Functions and Operators             |       |
|    | 9.16.1. Processing and Creating JSON Data      | 315   |
|    | 9.16.2. The SQL/JSON Path Language             | 325   |
|    | 9.17. Sequence Manipulation Functions          | 333   |
|    | 9.18. Conditional Expressions                  | 334   |
|    | 9.18.1. CASE                                   | . 335 |
|    | 9.18.2. COALESCE                               | 336   |
|    | 9.18.3. NULLIF                                 | . 337 |
|    | 9.18.4. GREATEST and LEAST                     | 337   |
|    | 9.19. Array Functions and Operators            |       |
|    | 9.20. Range/Multirange Functions and Operators |       |
|    | 9.21. Aggregate Functions                      |       |
|    | 9.22. Window Functions                         |       |
|    | 9.23. Subquery Expressions                     |       |
|    | 9.23.1. EXISTS                                 |       |
|    | 9.23.2. IN                                     |       |
|    | 9.23.3. NOT IN                                 |       |
|    | 9.23.4. ANY/SOME                               |       |
|    | 9.23.5. ALL                                    |       |
|    | 9.23.6. Single-Row Comparison                  |       |
|    |                                                | -220  |

| 9.24. Row and Array Comparisons                     | 358 |
|-----------------------------------------------------|-----|
| 9.24.1. IN                                          | 358 |
| 9.24.2. NOT IN                                      | 358 |
| 9.24.3. ANY/SOME (array)                            | 359 |
| 9.24.4. ALL (array)                                 |     |
| 9.24.5. Row Constructor Comparison                  |     |
| 9.24.6. Composite Type Comparison                   |     |
| 9.25. Set Returning Functions                       |     |
| 9.26. System Information Functions and Operators    |     |
|                                                     |     |
| 9.27. System Administration Functions               |     |
| 9.27.1. Configuration Settings Functions            |     |
| 9.27.2. Server Signaling Functions                  |     |
| 9.27.3. Backup Control Functions                    |     |
| 9.27.4. Recovery Control Functions                  |     |
| 9.27.5. Snapshot Synchronization Functions          |     |
| 9.27.6. Replication Management Functions            | 388 |
| 9.27.7. Database Object Management Functions        | 391 |
| 9.27.8. Index Maintenance Functions                 | 393 |
| 9.27.9. Generic File Access Functions               |     |
| 9.27.10. Advisory Lock Functions                    |     |
| 9.28. Trigger Functions                             |     |
| 9.29. Event Trigger Functions                       |     |
| 9.29.1. Capturing Changes at Command End            |     |
| 9.29.2. Processing Objects Dropped by a DDL Command |     |
|                                                     |     |
| 9.29.3. Handling a Table Rewrite Event              |     |
| 9.30. Statistics Information Functions              |     |
| 9.30.1. Inspecting MCV Lists                        |     |
| 10. Type Conversion                                 |     |
| 10.1. Overview                                      |     |
| 10.2. Operators                                     |     |
| 10.3. Functions                                     |     |
| 10.4. Value Storage                                 |     |
| 10.5. UNION, CASE, and Related Constructs           |     |
| 10.6. SELECT Output Columns                         |     |
| 11. Indexes                                         | 416 |
| 11.1. Introduction                                  | 416 |
| 11.2. Index Types                                   | 417 |
| 11.2.1. B-Tree                                      | 417 |
| 11.2.2. Hash                                        | 418 |
| 11.2.3. GiST                                        |     |
| 11.2.4. SP-GiST                                     |     |
| 11.2.5. GIN                                         |     |
| 11.2.6. BRIN                                        |     |
| 11.3. Multicolumn Indexes                           |     |
| 11.4. Indexes and ORDER BY                          |     |
|                                                     |     |
| 11.5. Combining Multiple Indexes                    |     |
| 11.6. Unique Indexes                                |     |
| 11.7. Indexes on Expressions                        |     |
| 11.8. Partial Indexes                               |     |
| 11.9. Index-Only Scans and Covering Indexes         |     |
| 11.10. Operator Classes and Operator Families       |     |
| 11.11. Indexes and Collations                       |     |
| 11.12. Examining Index Usage                        | 430 |
| 12. Full Text Search                                |     |
| 12.1. Introduction                                  | 432 |
| 12.1.1. What Is a Document?                         | 433 |
| 12.1.2. Basic Text Matching                         | 433 |
|                                                     | 435 |

| 12.2. Tables and Indexes                                     |     |
|--------------------------------------------------------------|-----|
| 12.2.1. Searching a Table                                    |     |
| 12.2.2. Creating Indexes                                     |     |
| 12.3. Controlling Text Search                                |     |
| 12.3.1. Parsing Documents                                    | 438 |
| 12.3.2. Parsing Queries                                      | 439 |
| 12.3.3. Ranking Search Results                               | 442 |
| 12.3.4. Highlighting Results                                 | 444 |
| 12.4. Additional Features                                    |     |
| 12.4.1. Manipulating Documents                               | 445 |
| 12.4.2. Manipulating Queries                                 |     |
| 12.4.3. Triggers for Automatic Updates                       |     |
| 12.4.4. Gathering Document Statistics                        |     |
| 12.5. Parsers                                                |     |
| 12.6. Dictionaries                                           |     |
| 12.6.1. Stop Words                                           |     |
| 12.6.2. Simple Dictionary                                    |     |
| ÷ · · · · · · · · · · · · · · · · · · ·                      |     |
| 12.6.3. Synonym Dictionary                                   |     |
| 12.6.4. Thesaurus Dictionary                                 |     |
| 12.6.5. Ispell Dictionary                                    |     |
| 12.6.6. Snowball Dictionary                                  |     |
| 12.7. Configuration Example                                  |     |
| 12.8. Testing and Debugging Text Search                      |     |
| 12.8.1. Configuration Testing                                |     |
| 12.8.2. Parser Testing                                       |     |
| 12.8.3. Dictionary Testing                                   |     |
| 12.9. Preferred Index Types for Text Search                  |     |
| 12.10. psql Support                                          |     |
| 12.11. Limitations                                           | 473 |
| 13. Concurrency Control                                      | 474 |
| 13.1. Introduction                                           | 474 |
| 13.2. Transaction Isolation                                  | 474 |
| 13.2.1. Read Committed Isolation Level                       | 475 |
| 13.2.2. Repeatable Read Isolation Level                      |     |
| 13.2.3. Serializable Isolation Level                         |     |
| 13.3. Explicit Locking                                       |     |
| 13.3.1. Table-Level Locks                                    |     |
| 13.3.2. Row-Level Locks                                      |     |
| 13.3.3. Page-Level Locks                                     |     |
| 13.3.4. Deadlocks                                            |     |
| 13.3.5. Advisory Locks                                       |     |
|                                                              |     |
| 13.4. Data Consistency Checks at the Application Level       |     |
| 13.4.1. Enforcing Consistency with Serializable Transactions |     |
| 13.4.2. Enforcing Consistency with Explicit Blocking Locks   |     |
| 13.5. Caveats                                                |     |
| 13.6. Locking and Indexes                                    |     |
| 14. Performance Tips                                         |     |
| 14.1. Using EXPLAIN                                          |     |
| 14.1.1. EXPLAIN Basics                                       |     |
| 14.1.2. EXPLAIN ANALYZE                                      |     |
| 14.1.3. Caveats                                              |     |
| 14.2. Statistics Used by the Planner                         | 501 |
| 14.2.1. Single-Column Statistics                             | 501 |
| 14.2.2. Extended Statistics                                  | 503 |
| 14.3. Controlling the Planner with Explicit JOIN Clauses     | 506 |
| 14.4. Populating a Database                                  |     |
| 14.4.1. Disable Autocommit                                   |     |
| 14.4.2. Use COPY                                             |     |
|                                                              |     |

#### The SQL Language

| 14.4.3. Remove Indexes                                 | 509 |
|--------------------------------------------------------|-----|
| 14.4.4. Remove Foreign Key Constraints                 | 509 |
| 14.4.5. Increase maintenance work mem                  |     |
| 14.4.6. Increase max wal size                          | 509 |
| 14.4.7. Disable WAL Archival and Streaming Replication | 509 |
| 14.4.8. Run ANALYZE Afterwards                         | 510 |
| 14.4.9. Some Notes about pg dump                       | 510 |
| 14.5. Non-Durable Settings                             | 511 |
| 15. Parallel Query                                     | 512 |
| 15.1. How Parallel Query Works                         |     |
| 15.2. When Can Parallel Query Be Used?                 | 513 |
| 15.3. Parallel Plans                                   |     |
| 15.3.1. Parallel Scans                                 |     |
| 15.3.2. Parallel Joins                                 | 514 |
| 15.3.3. Parallel Aggregation                           | 515 |
| 15.3.4. Parallel Append                                | 515 |
| 15.3.5. Parallel Plan Tips                             |     |
| 15.4. Parallel Safety                                  |     |
| 15.4.1. Parallel Labeling for Functions and Aggregates |     |

# <span id="page-70-0"></span>**Chapter 4. SQL Syntax**

This chapter describes the syntax of SQL. It forms the foundation for understanding the following chapters which will go into detail about how SQL commands are applied to define and modify data.

We also advise users who are already familiar with SQL to read this chapter carefully because it contains several rules and concepts that are implemented inconsistently among SQL databases or that are specific to PostgreSQL.

# <span id="page-70-1"></span>**4.1. Lexical Structure**

SQL input consists of a sequence of *commands*. A command is composed of a sequence of *tokens*, terminated by a semicolon (";"). The end of the input stream also terminates a command. Which tokens are valid depends on the syntax of the particular command.

A token can be a *key word*, an *identifier*, a *quoted identifier*, a *literal* (or constant), or a special character symbol. Tokens are normally separated by whitespace (space, tab, newline), but need not be if there is no ambiguity (which is generally only the case if a special character is adjacent to some other token type).

For example, the following is (syntactically) valid SQL input:

```
SELECT * FROM MY_TABLE;
UPDATE MY_TABLE SET A = 5;
INSERT INTO MY_TABLE VALUES (3, 'hi there');
```

This is a sequence of three commands, one per line (although this is not required; more than one command can be on a line, and commands can usefully be split across lines).

Additionally, *comments* can occur in SQL input. They are not tokens, they are effectively equivalent to whitespace.

The SQL syntax is not very consistent regarding what tokens identify commands and which are operands or parameters. The first few tokens are generally the command name, so in the above example we would usually speak of a "SELECT", an "UPDATE", and an "INSERT" command. But for instance the UPDATE command always requires a SET token to appear in a certain position, and this particular variation of INSERT also requires a VALUES in order to be complete. The precise syntax rules for each command are described in Part VI.

## <span id="page-70-2"></span>**4.1.1. Identifiers and Key Words**

Tokens such as SELECT, UPDATE, or VALUES in the example above are examples of *key words*, that is, words that have a fixed meaning in the SQL language. The tokens MY\_TABLE and A are examples of *identifiers*. They identify names of tables, columns, or other database objects, depending on the command they are used in. Therefore they are sometimes simply called "names". Key words and identifiers have the same lexical structure, meaning that one cannot know whether a token is an identifier or a key word without knowing the language. A complete list of key words can be found in Appendix C.

SQL identifiers and key words must begin with a letter (a-z, but also letters with diacritical marks and non-Latin letters) or an underscore (\_). Subsequent characters in an identifier or key word can be letters, underscores, digits (0-9), or dollar signs (\$). Note that dollar signs are not allowed in identifiers according to the letter of the SQL standard, so their use might render applications less portable. The SQL standard will not define a key word that contains digits or starts or ends with an underscore, so identifiers of this form are safe against possible conflict with future extensions of the standard.

 The system uses no more than NAMEDATALEN-1 bytes of an identifier; longer names can be written in commands, but they will be truncated. By default, NAMEDATALEN is 64 so the maximum identifier length is 63 bytes. If this limit is problematic, it can be raised by changing the NAMEDATALEN constant in src/include/pg\_config\_manual.h.

Key words and unquoted identifiers are case insensitive. Therefore:

```
UPDATE MY_TABLE SET A = 5;
can equivalently be written as:
uPDaTE my_TabLE SeT a = 5;
```

A convention often used is to write key words in upper case and names in lower case, e.g.:

```
UPDATE my_table SET a = 5;
```

 There is a second kind of identifier: the *delimited identifier* or *quoted identifier*. It is formed by enclosing an arbitrary sequence of characters in double-quotes ("). A delimited identifier is always an identifier, never a key word. So "select" could be used to refer to a column or table named "select", whereas an unquoted select would be taken as a key word and would therefore provoke a parse error when used where a table or column name is expected. The example can be written with quoted identifiers like this:

```
UPDATE "my_table" SET "a" = 5;
```

Quoted identifiers can contain any character, except the character with code zero. (To include a double quote, write two double quotes.) This allows constructing table or column names that would otherwise not be possible, such as ones containing spaces or ampersands. The length limitation still applies.

Quoting an identifier also makes it case-sensitive, whereas unquoted names are always folded to lower case. For example, the identifiers FOO, foo, and "foo" are considered the same by PostgreSQL, but "Foo" and "FOO" are different from these three and each other. (The folding of unquoted names to lower case in PostgreSQL is incompatible with the SQL standard, which says that unquoted names should be folded to upper case. Thus, foo should be equivalent to "FOO" not "foo" according to the standard. If you want to write portable applications you are advised to always quote a particular name or never quote it.)

A variant of quoted identifiers allows including escaped Unicode characters identified by their code points. This variant starts with U& (upper or lower case U followed by ampersand) immediately before the opening double quote, without any spaces in between, for example U&"foo". (Note that this creates an ambiguity with the operator &. Use spaces around the operator to avoid this problem.) Inside the quotes, Unicode characters can be specified in escaped form by writing a backslash followed by the four-digit hexadecimal code point number or alternatively a backslash followed by a plus sign followed by a six-digit hexadecimal code point number. For example, the identifier "data" could be written as

```
U&"d\0061t\+000061"
```

The following less trivial example writes the Russian word "slon" (elephant) in Cyrillic letters:

```
U&"\0441\043B\043E\043D"
```

If a different escape character than backslash is desired, it can be specified using the UESCAPE clause after the string, for example:

```
U&"d!0061t!+000061" UESCAPE '!'
```

The escape character can be any single character other than a hexadecimal digit, the plus sign, a single quote, a double quote, or a whitespace character. Note that the escape character is written in single quotes, not double quotes, after UESCAPE.

To include the escape character in the identifier literally, write it twice.

Either the 4-digit or the 6-digit escape form can be used to specify UTF-16 surrogate pairs to compose characters with code points larger than U+FFFF, although the availability of the 6-digit form technically makes this unnecessary. (Surrogate pairs are not stored directly, but are combined into a single code point.)

If the server encoding is not UTF-8, the Unicode code point identified by one of these escape sequences is converted to the actual server encoding; an error is reported if that's not possible.

## <span id="page-72-0"></span>**4.1.2. Constants**

There are three kinds of *implicitly-typed constants* in PostgreSQL: strings, bit strings, and numbers. Constants can also be specified with explicit types, which can enable more accurate representation and more efficient handling by the system. These alternatives are discussed in the following subsections.

### <span id="page-72-1"></span>**4.1.2.1. String Constants**

 A string constant in SQL is an arbitrary sequence of characters bounded by single quotes ('), for example 'This is a string'. To include a single-quote character within a string constant, write two adjacent single quotes, e.g., 'Dianne''s horse'. Note that this is *not* the same as a double-quote character (").

Two string constants that are only separated by whitespace *with at least one newline* are concatenated and effectively treated as if the string had been written as one constant. For example:

```
SELECT 'foo'
'bar';
is equivalent to:
SELECT 'foobar';
but:
SELECT 'foo' 'bar';
```

is not valid syntax. (This slightly bizarre behavior is specified by SQL; PostgreSQL is following the standard.)

### **4.1.2.2. String Constants with C-Style Escapes**

PostgreSQL also accepts "escape" string constants, which are an extension to the SQL standard. An escape string constant is specified by writing the letter E (upper or lower case) just before the opening single quote, e.g., E'foo'. (When continuing an escape string constant across lines, write E only before the first opening quote.) Within an escape string, a backslash character (\) begins a C-like *backslash escape* sequence, in which the combination of backslash and following character(s) represent a special byte value, as shown in [Table 4.1.](#page-73-0)

**Table 4.1. Backslash Escape Sequences**

<span id="page-73-0"></span>

| Backslash Escape Sequence         | Interpretation                                       |
|-----------------------------------|------------------------------------------------------|
| \b                                | backspace                                            |
| \f                                | form feed                                            |
| \n                                | newline                                              |
| \r                                | carriage return                                      |
| \t                                | tab                                                  |
| \o, \oo, \ooo (o = 0–7)           | octal byte value                                     |
| \xh, \xhh (h = 0–9, A–F)          | hexadecimal byte value                               |
| \uxxxx, \Uxxxxxxxx (x = 0–9, A–F) | 16 or 32-bit hexadecimal Unicode character val<br>ue |

Any other character following a backslash is taken literally. Thus, to include a backslash character, write two backslashes (\\). Also, a single quote can be included in an escape string by writing \', in addition to the normal way of ''.

It is your responsibility that the byte sequences you create, especially when using the octal or hexadecimal escapes, compose valid characters in the server character set encoding. A useful alternative is to use Unicode escapes or the alternative Unicode escape syntax, explained in [Section 4.1.2.3;](#page-73-1) then the server will check that the character conversion is possible.

### **Caution**

If the configuration parameter standard\_conforming\_strings is off, then PostgreSQL recognizes backslash escapes in both regular and escape string constants. However, as of PostgreSQL 9.1, the default is on, meaning that backslash escapes are recognized only in escape string constants. This behavior is more standards-compliant, but might break applications which rely on the historical behavior, where backslash escapes were always recognized. As a workaround, you can set this parameter to off, but it is better to migrate away from using backslash escapes. If you need to use a backslash escape to represent a special character, write the string constant with an E.

In addition to standard\_conforming\_strings, the configuration parameters escape\_string\_warning and backslash\_quote govern treatment of backslashes in string constants.

The character with the code zero cannot be in a string constant.

### <span id="page-73-1"></span>**4.1.2.3. String Constants with Unicode Escapes**

PostgreSQL also supports another type of escape syntax for strings that allows specifying arbitrary Unicode characters by code point. A Unicode escape string constant starts with U& (upper or lower case letter U followed by ampersand) immediately before the opening quote, without any spaces in between, for example U&'foo'. (Note that this creates an ambiguity with the operator &. Use spaces around the operator to avoid this problem.) Inside the quotes, Unicode characters can be specified in escaped form by writing a backslash followed by the four-digit hexadecimal code point number or alternatively a backslash followed by a plus sign followed by a six-digit hexadecimal code point number. For example, the string 'data' could be written as

U&'d\0061t\+000061'

The following less trivial example writes the Russian word "slon" (elephant) in Cyrillic letters:

```
U&'\0441\043B\043E\043D'
```

If a different escape character than backslash is desired, it can be specified using the UESCAPE clause after the string, for example:

```
U&'d!0061t!+000061' UESCAPE '!'
```

The escape character can be any single character other than a hexadecimal digit, the plus sign, a single quote, a double quote, or a whitespace character.

To include the escape character in the string literally, write it twice.

Either the 4-digit or the 6-digit escape form can be used to specify UTF-16 surrogate pairs to compose characters with code points larger than U+FFFF, although the availability of the 6-digit form technically makes this unnecessary. (Surrogate pairs are not stored directly, but are combined into a single code point.)

If the server encoding is not UTF-8, the Unicode code point identified by one of these escape sequences is converted to the actual server encoding; an error is reported if that's not possible.

Also, the Unicode escape syntax for string constants only works when the configuration parameter standard\_conforming\_strings is turned on. This is because otherwise this syntax could confuse clients that parse the SQL statements to the point that it could lead to SQL injections and similar security issues. If the parameter is set to off, this syntax will be rejected with an error message.

#### **4.1.2.4. Dollar-Quoted String Constants**

While the standard syntax for specifying string constants is usually convenient, it can be difficult to understand when the desired string contains many single quotes, since each of those must be doubled. To allow more readable queries in such situations, PostgreSQL provides another way, called "dollar quoting", to write string constants. A dollar-quoted string constant consists of a dollar sign (\$), an optional "tag" of zero or more characters, another dollar sign, an arbitrary sequence of characters that makes up the string content, a dollar sign, the same tag that began this dollar quote, and a dollar sign. For example, here are two different ways to specify the string "Dianne's horse" using dollar quoting:

```
$$Dianne's horse$$
$SomeTag$Dianne's horse$SomeTag$
```

Notice that inside the dollar-quoted string, single quotes can be used without needing to be escaped. Indeed, no characters inside a dollar-quoted string are ever escaped: the string content is always written literally. Backslashes are not special, and neither are dollar signs, unless they are part of a sequence matching the opening tag.

It is possible to nest dollar-quoted string constants by choosing different tags at each nesting level. This is most commonly used in writing function definitions. For example:

```
$function$
BEGIN
 RETURN ($1 ~ $q$[\t\r\n\v\\]$q$);
END;
$function$
```

Here, the sequence \$q\$[\t\r\n\v\\]\$q\$ represents a dollar-quoted literal string [\t\r\n\v \\], which will be recognized when the function body is executed by PostgreSQL. But since the sequence does not match the outer dollar quoting delimiter \$function\$, it is just some more characters within the constant so far as the outer string is concerned.

The tag, if any, of a dollar-quoted string follows the same rules as an unquoted identifier, except that it cannot contain a dollar sign. Tags are case sensitive, so \$tag\$String content\$tag\$ is correct, but \$TAG\$String content\$tag\$ is not.

A dollar-quoted string that follows a keyword or identifier must be separated from it by whitespace; otherwise the dollar quoting delimiter would be taken as part of the preceding identifier.

Dollar quoting is not part of the SQL standard, but it is often a more convenient way to write complicated string literals than the standard-compliant single quote syntax. It is particularly useful when representing string constants inside other constants, as is often needed in procedural function definitions. With single-quote syntax, each backslash in the above example would have to be written as four backslashes, which would be reduced to two backslashes in parsing the original string constant, and then to one when the inner string constant is re-parsed during function execution.

#### **4.1.2.5. Bit-String Constants**

Bit-string constants look like regular string constants with a B (upper or lower case) immediately before the opening quote (no intervening whitespace), e.g., B'1001'. The only characters allowed within bit-string constants are 0 and 1.

Alternatively, bit-string constants can be specified in hexadecimal notation, using a leading X (upper or lower case), e.g., X'1FF'. This notation is equivalent to a bit-string constant with four binary digits for each hexadecimal digit.

Both forms of bit-string constant can be continued across lines in the same way as regular string constants. Dollar quoting cannot be used in a bit-string constant.

#### **4.1.2.6. Numeric Constants**

Numeric constants are accepted in these general forms:

```
digits
digits.[digits][e[+-]digits]
[digits].digits[e[+-]digits]
digitse[+-]digits
```

where digits is one or more decimal digits (0 through 9). At least one digit must be before or after the decimal point, if one is used. At least one digit must follow the exponent marker (e), if one is present. There cannot be any spaces or other characters embedded in the constant. Note that any leading plus or minus sign is not actually considered part of the constant; it is an operator applied to the constant.

These are some examples of valid numeric constants:

```
42
3.5
4.
.001
5e2
1.925e-3
```

 A numeric constant that contains neither a decimal point nor an exponent is initially presumed to be type integer if its value fits in type integer (32 bits); otherwise it is presumed to be type bigint if its value fits in type bigint (64 bits); otherwise it is taken to be type numeric. Constants that contain decimal points and/or exponents are always initially presumed to be type numeric.

The initially assigned data type of a numeric constant is just a starting point for the type resolution algorithms. In most cases the constant will be automatically coerced to the most appropriate type depending on context. When necessary, you can force a numeric value to be interpreted as a specific data type by casting it. For example, you can force a numeric value to be treated as type real (float4) by writing:

```
REAL '1.23' -- string style
1.23::REAL -- PostgreSQL (historical) style
```

These are actually just special cases of the general casting notations discussed next.

### <span id="page-76-1"></span>**4.1.2.7. Constants of Other Types**

A constant of an *arbitrary* type can be entered using any one of the following notations:

```
type 'string'
'string'::type
CAST ( 'string' AS type )
```

The string constant's text is passed to the input conversion routine for the type called type. The result is a constant of the indicated type. The explicit type cast can be omitted if there is no ambiguity as to the type the constant must be (for example, when it is assigned directly to a table column), in which case it is automatically coerced.

The string constant can be written using either regular SQL notation or dollar-quoting.

It is also possible to specify a type coercion using a function-like syntax:

```
typename ( 'string' )
```

but not all type names can be used in this way; see [Section 4.2.9](#page-86-0) for details.

The ::, CAST(), and function-call syntaxes can also be used to specify run-time type conversions of arbitrary expressions, as discussed in [Section 4.2.9](#page-86-0). To avoid syntactic ambiguity, the type 'string' syntax can only be used to specify the type of a simple literal constant. Another restriction on the type 'string' syntax is that it does not work for array types; use :: or CAST() to specify the type of an array constant.

The CAST() syntax conforms to SQL. The type 'string' syntax is a generalization of the standard: SQL specifies this syntax only for a few data types, but PostgreSQL allows it for all types. The syntax with :: is historical PostgreSQL usage, as is the function-call syntax.

## <span id="page-76-0"></span>**4.1.3. Operators**

An operator name is a sequence of up to NAMEDATALEN-1 (63 by default) characters from the following list:

```
+ - * / < > = ~ ! @ # % ^ & | ` ?
```

There are a few restrictions on operator names, however:

- -- and /\* cannot appear anywhere in an operator name, since they will be taken as the start of a comment.
- A multiple-character operator name cannot end in + or -, unless the name also contains at least one of these characters:

```
~ ! @ # % ^ & | ` ?
```

For example, @- is an allowed operator name, but \*- is not. This restriction allows PostgreSQL to parse SQL-compliant queries without requiring spaces between tokens.

When working with non-SQL-standard operator names, you will usually need to separate adjacent operators with spaces to avoid ambiguity. For example, if you have defined a prefix operator named @, you cannot write X\*@Y; you must write X\* @Y to ensure that PostgreSQL reads it as two operator names not one.

## <span id="page-77-0"></span>**4.1.4. Special Characters**

Some characters that are not alphanumeric have a special meaning that is different from being an operator. Details on the usage can be found at the location where the respective syntax element is described. This section only exists to advise the existence and summarize the purposes of these characters.

- A dollar sign (\$) followed by digits is used to represent a positional parameter in the body of a function definition or a prepared statement. In other contexts the dollar sign can be part of an identifier or a dollar-quoted string constant.
- Parentheses (()) have their usual meaning to group expressions and enforce precedence. In some cases parentheses are required as part of the fixed syntax of a particular SQL command.
- Brackets ([]) are used to select the elements of an array. See Section 8.15 for more information on arrays.
- Commas (,) are used in some syntactical constructs to separate the elements of a list.
- The semicolon (;) terminates an SQL command. It cannot appear anywhere within a command, except within a string constant or quoted identifier.
- The colon (:) is used to select "slices" from arrays. (See Section 8.15.) In certain SQL dialects (such as Embedded SQL), the colon is used to prefix variable names.
- The asterisk (\*) is used in some contexts to denote all the fields of a table row or composite value. It also has a special meaning when used as the argument of an aggregate function, namely that the aggregate does not require any explicit parameter.
- The period (.) is used in numeric constants, and to separate schema, table, and column names.

## <span id="page-77-1"></span>**4.1.5. Comments**

A comment is a sequence of characters beginning with double dashes and extending to the end of the line, e.g.:

```
-- This is a standard SQL comment
```

Alternatively, C-style block comments can be used:

```
/* multiline comment
 * with nesting: /* nested block comment */
 */
```

where the comment begins with /\* and extends to the matching occurrence of \*/. These block comments nest, as specified in the SQL standard but unlike C, so that one can comment out larger blocks of code that might contain existing block comments.

A comment is removed from the input stream before further syntax analysis and is effectively replaced by whitespace.

## <span id="page-78-1"></span>**4.1.6. Operator Precedence**

[Table 4.2](#page-78-0) shows the precedence and associativity of the operators in PostgreSQL. Most operators have the same precedence and are left-associative. The precedence and associativity of the operators is hardwired into the parser. Add parentheses if you want an expression with multiple operators to be parsed in some other way than what the precedence rules imply.

<span id="page-78-0"></span>**Table 4.2. Operator Precedence (highest to lowest)**

| Operator/Element                 | Associativity | Description                                           |
|----------------------------------|---------------|-------------------------------------------------------|
|                                  | left          | table/column name separator                           |
| ::                               | left          | PostgreSQL-style typecast                             |
| [ ]                              | left          | array element selection                               |
| + -                              | right         | unary plus, unary minus                               |
| COLLATE                          | left          | collation selection                                   |
| AT                               | left          | AT TIME ZONE                                          |
| ^                                | left          | exponentiation                                        |
| * / %                            | left          | multiplication, division, modulo                      |
| + -                              | left          | addition, subtraction                                 |
| (any other operator)             | left          | all other native and user-defined oper<br>ators       |
| BETWEEN IN LIKE ILIKE<br>SIMILAR |               | range containment, set membership,<br>string matching |
| < > = <= >= <>                   |               | comparison operators                                  |
| IS ISNULL NOTNULL                |               | IS TRUE, IS FALSE, IS NULL,<br>IS DISTINCT FROM, etc  |
| NOT                              | right         | logical negation                                      |
| AND                              | left          | logical conjunction                                   |
| OR                               | left          | logical disjunction                                   |

Note that the operator precedence rules also apply to user-defined operators that have the same names as the built-in operators mentioned above. For example, if you define a "+" operator for some custom data type it will have the same precedence as the built-in "+" operator, no matter what yours does.

When a schema-qualified operator name is used in the OPERATOR syntax, as for example in:

```
SELECT 3 OPERATOR(pg_catalog.+) 4;
```

the OPERATOR construct is taken to have the default precedence shown in [Table 4.2](#page-78-0) for "any other operator". This is true no matter which specific operator appears inside OPERATOR().

#### **Note**

PostgreSQL versions before 9.5 used slightly different operator precedence rules. In particular, <= >= and <> used to be treated as generic operators; IS tests used to have higher priority; and NOT BETWEEN and related constructs acted inconsistently, being taken in some cases as having the precedence of NOT rather than BETWEEN. These rules were changed for better compliance with the SQL standard and to reduce confusion from inconsistent treatment of logically equivalent constructs. In most cases, these changes will result in no behavioral change, or perhaps in "no such operator" failures which can be resolved by adding parentheses. However there are corner cases in which a query might change behavior without any parsing error being reported.

# <span id="page-79-0"></span>**4.2. Value Expressions**

Value expressions are used in a variety of contexts, such as in the target list of the SELECT command, as new column values in INSERT or UPDATE, or in search conditions in a number of commands. The result of a value expression is sometimes called a *scalar*, to distinguish it from the result of a table expression (which is a table). Value expressions are therefore also called *scalar expressions* (or even simply *expressions*). The expression syntax allows the calculation of values from primitive parts using arithmetic, logical, set, and other operations.

A value expression is one of the following:

- A constant or literal value
- A column reference
- A positional parameter reference, in the body of a function definition or prepared statement
- A subscripted expression
- A field selection expression
- An operator invocation
- A function call
- An aggregate expression
- A window function call
- A type cast
- A collation expression
- A scalar subquery
- An array constructor
- A row constructor
- Another value expression in parentheses (used to group subexpressions and override precedence)

In addition to this list, there are a number of constructs that can be classified as an expression but do not follow any general syntax rules. These generally have the semantics of a function or operator and are explained in the appropriate location in Chapter 9. An example is the IS NULL clause.

We have already discussed constants in [Section 4.1.2](#page-72-0). The following sections discuss the remaining options.

## <span id="page-79-1"></span>**4.2.1. Column References**

A column can be referenced in the form:

correlation.columnname

correlation is the name of a table (possibly qualified with a schema name), or an alias for a table defined by means of a FROM clause. The correlation name and separating dot can be omitted if the column name is unique across all the tables being used in the current query. (See also [Chapter 7](#page-149-0).)

## <span id="page-80-0"></span>**4.2.2. Positional Parameters**

A positional parameter reference is used to indicate a value that is supplied externally to an SQL statement. Parameters are used in SQL function definitions and in prepared queries. Some client libraries also support specifying data values separately from the SQL command string, in which case parameters are used to refer to the out-of-line data values. The form of a parameter reference is:

\$number

For example, consider the definition of a function, dept, as:

```
CREATE FUNCTION dept(text) RETURNS dept
 AS $$ SELECT * FROM dept WHERE name = $1 $$
 LANGUAGE SQL;
```

Here the \$1 references the value of the first function argument whenever the function is invoked.

## <span id="page-80-1"></span>**4.2.3. Subscripts**

If an expression yields a value of an array type, then a specific element of the array value can be extracted by writing

```
expression[subscript]
```

or multiple adjacent elements (an "array slice") can be extracted by writing

```
expression[lower_subscript:upper_subscript]
```

(Here, the brackets [ ] are meant to appear literally.) Each subscript is itself an expression, which will be rounded to the nearest integer value.

In general the array expression must be parenthesized, but the parentheses can be omitted when the expression to be subscripted is just a column reference or positional parameter. Also, multiple subscripts can be concatenated when the original array is multidimensional. For example:

```
mytable.arraycolumn[4]
mytable.two_d_column[17][34]
$1[10:42]
(arrayfunction(a,b))[42]
```

The parentheses in the last example are required. See Section 8.15 for more about arrays.

## <span id="page-80-2"></span>**4.2.4. Field Selection**

If an expression yields a value of a composite type (row type), then a specific field of the row can be extracted by writing

```
expression.fieldname
```

In general the row expression must be parenthesized, but the parentheses can be omitted when the expression to be selected from is just a table reference or positional parameter. For example:

```
mytable.mycolumn
```

```
$1.somecolumn
(rowfunction(a,b)).col3
```

(Thus, a qualified column reference is actually just a special case of the field selection syntax.) An important special case is extracting a field from a table column that is of a composite type:

```
(compositecol).somefield
(mytable.compositecol).somefield
```

The parentheses are required here to show that compositecol is a column name not a table name, or that mytable is a table name not a schema name in the second case.

You can ask for all fields of a composite value by writing .\*:

```
(compositecol).*
```

This notation behaves differently depending on context; see Section 8.16.5 for details.

## <span id="page-81-0"></span>**4.2.5. Operator Invocations**

There are two possible syntaxes for an operator invocation:

```
expression operator expression (binary infix operator)
operator expression (unary prefix operator)
```

where the operator token follows the syntax rules of [Section 4.1.3](#page-76-0), or is one of the key words AND, OR, and NOT, or is a qualified operator name in the form:

```
OPERATOR(schema.operatorname)
```

Which particular operators exist and whether they are unary or binary depends on what operators have been defined by the system or the user. Chapter 9 describes the built-in operators.

## <span id="page-81-1"></span>**4.2.6. Function Calls**

The syntax for a function call is the name of a function (possibly qualified with a schema name), followed by its argument list enclosed in parentheses:

```
function_name ([expression [, expression ... ]] )
```

For example, the following computes the square root of 2:

```
sqrt(2)
```

The list of built-in functions is in Chapter 9. Other functions can be added by the user.

When issuing queries in a database where some users mistrust other users, observe security precautions from Section 10.3 when writing function calls.

The arguments can optionally have names attached. See [Section 4.3](#page-92-0) for details.

#### **Note**

A function that takes a single argument of composite type can optionally be called using fieldselection syntax, and conversely field selection can be written in functional style. That is, the notations col(table) and table.col are interchangeable. This behavior is not SQL- standard but is provided in PostgreSQL because it allows use of functions to emulate "computed fields". For more information see Section 8.16.5.

## <span id="page-82-0"></span>**4.2.7. Aggregate Expressions**

An *aggregate expression* represents the application of an aggregate function across the rows selected by a query. An aggregate function reduces multiple inputs to a single output value, such as the sum or average of the inputs. The syntax of an aggregate expression is one of the following:

```
aggregate_name (expression [ , ... ] [ order_by_clause ] ) [ FILTER
 ( WHERE filter_clause ) ]
aggregate_name (ALL expression [ , ... ] [ order_by_clause ] )
 [ FILTER ( WHERE filter_clause ) ]
aggregate_name (DISTINCT expression [ , ... ] [ order_by_clause ] )
 [ FILTER ( WHERE filter_clause ) ]
aggregate_name ( * ) [ FILTER ( WHERE filter_clause ) ]
aggregate_name ( [ expression [ , ... ] ] ) WITHIN GROUP
 ( order_by_clause ) [ FILTER ( WHERE filter_clause ) ]
```

where aggregate\_name is a previously defined aggregate (possibly qualified with a schema name) and expression is any value expression that does not itself contain an aggregate expression or a window function call. The optional order\_by\_clause and filter\_clause are described below.

The first form of aggregate expression invokes the aggregate once for each input row. The second form is the same as the first, since ALL is the default. The third form invokes the aggregate once for each distinct value of the expression (or distinct set of values, for multiple expressions) found in the input rows. The fourth form invokes the aggregate once for each input row; since no particular input value is specified, it is generally only useful for the count(\*) aggregate function. The last form is used with *ordered-set* aggregate functions, which are described below.

Most aggregate functions ignore null inputs, so that rows in which one or more of the expression(s) yield null are discarded. This can be assumed to be true, unless otherwise specified, for all built-in aggregates.

For example, count(\*) yields the total number of input rows; count(f1) yields the number of input rows in which f1 is non-null, since count ignores nulls; and count(distinct f1) yields the number of distinct non-null values of f1.

Ordinarily, the input rows are fed to the aggregate function in an unspecified order. In many cases this does not matter; for example, min produces the same result no matter what order it receives the inputs in. However, some aggregate functions (such as array\_agg and string\_agg) produce results that depend on the ordering of the input rows. When using such an aggregate, the optional order\_by\_clause can be used to specify the desired ordering. The order\_by\_clause has the same syntax as for a query-level ORDER BY clause, as described in [Section 7.5](#page-168-0), except that its expressions are always just expressions and cannot be output-column names or numbers. For example:

```
SELECT array_agg(a ORDER BY b DESC) FROM table;
```

When dealing with multiple-argument aggregate functions, note that the ORDER BY clause goes after all the aggregate arguments. For example, write this:

```
SELECT string_agg(a, ',' ORDER BY a) FROM table;
not this:
```

```
SELECT string_agg(a ORDER BY a, ',') FROM table; -- incorrect
```

The latter is syntactically valid, but it represents a call of a single-argument aggregate function with two ORDER BY keys (the second one being rather useless since it's a constant).

If DISTINCT is specified in addition to an order\_by\_clause, then all the ORDER BY expressions must match regular arguments of the aggregate; that is, you cannot sort on an expression that is not included in the DISTINCT list.

#### **Note**

The ability to specify both DISTINCT and ORDER BY in an aggregate function is a PostgreSQL extension.

Placing ORDER BY within the aggregate's regular argument list, as described so far, is used when ordering the input rows for general-purpose and statistical aggregates, for which ordering is optional. There is a subclass of aggregate functions called *ordered-set aggregates* for which an order\_by\_clause is *required*, usually because the aggregate's computation is only sensible in terms of a specific ordering of its input rows. Typical examples of ordered-set aggregates include rank and percentile calculations. For an ordered-set aggregate, the order\_by\_clause is written inside WITHIN GROUP (...), as shown in the final syntax alternative above. The expressions in the order\_by\_clause are evaluated once per input row just like regular aggregate arguments, sorted as per the order\_by\_clause's requirements, and fed to the aggregate function as input arguments. (This is unlike the case for a non-WITHIN GROUP order\_by\_clause, which is not treated as argument(s) to the aggregate function.) The argument expressions preceding WITHIN GROUP, if any, are called *direct arguments* to distinguish them from the *aggregated arguments* listed in the order\_by\_clause. Unlike regular aggregate arguments, direct arguments are evaluated only once per aggregate call, not once per input row. This means that they can contain variables only if those variables are grouped by GROUP BY; this restriction is the same as if the direct arguments were not inside an aggregate expression at all. Direct arguments are typically used for things like percentile fractions, which only make sense as a single value per aggregation calculation. The direct argument list can be empty; in this case, write just () not (\*). (PostgreSQL will actually accept either spelling, but only the first way conforms to the SQL standard.)

An example of an ordered-set aggregate call is:

```
SELECT percentile_cont(0.5) WITHIN GROUP (ORDER BY income) FROM
 households;
 percentile_cont
-----------------
 50489
```

which obtains the 50th percentile, or median, value of the income column from table households. Here, 0.5 is a direct argument; it would make no sense for the percentile fraction to be a value varying across rows.

If FILTER is specified, then only the input rows for which the filter\_clause evaluates to true are fed to the aggregate function; other rows are discarded. For example:

```
SELECT
 count(*) AS unfiltered,
 count(*) FILTER (WHERE i < 5) AS filtered
FROM generate_series(1,10) AS s(i);
 unfiltered | filtered
------------+----------
```

```
 10 | 4
(1 row)
```

The predefined aggregate functions are described in Section 9.21. Other aggregate functions can be added by the user.

An aggregate expression can only appear in the result list or HAVING clause of a SELECT command. It is forbidden in other clauses, such as WHERE, because those clauses are logically evaluated before the results of aggregates are formed.

When an aggregate expression appears in a subquery (see [Section 4.2.11](#page-88-0) and Section 9.23), the aggregate is normally evaluated over the rows of the subquery. But an exception occurs if the aggregate's arguments (and filter\_clause if any) contain only outer-level variables: the aggregate then belongs to the nearest such outer level, and is evaluated over the rows of that query. The aggregate expression as a whole is then an outer reference for the subquery it appears in, and acts as a constant over any one evaluation of that subquery. The restriction about appearing only in the result list or HAVING clause applies with respect to the query level that the aggregate belongs to.

## <span id="page-84-0"></span>**4.2.8. Window Function Calls**

A *window function call* represents the application of an aggregate-like function over some portion of the rows selected by a query. Unlike non-window aggregate calls, this is not tied to grouping of the selected rows into a single output row — each row remains separate in the query output. However the window function has access to all the rows that would be part of the current row's group according to the grouping specification (PARTITION BY list) of the window function call. The syntax of a window function call is one of the following:

```
function_name ([expression [, expression ... ]]) [ FILTER
 ( WHERE filter_clause ) ] OVER window_name
function_name ([expression [, expression ... ]]) [ FILTER
 ( WHERE filter_clause ) ] OVER ( window_definition )
function_name ( * ) [ FILTER ( WHERE filter_clause ) ]
 OVER window_name
function_name ( * ) [ FILTER ( WHERE filter_clause ) ] OVER
 ( window_definition )
where window_definition has the syntax
[ existing_window_name ]
[ PARTITION BY expression [, ...] ]
[ ORDER BY expression [ ASC | DESC | USING operator ] [ NULLS
 { FIRST | LAST } ] [, ...] ]
[ frame_clause ]
The optional frame_clause can be one of
{ RANGE | ROWS | GROUPS } frame_start [ frame_exclusion ]
{ RANGE | ROWS | GROUPS } BETWEEN frame_start AND frame_end
 [ frame_exclusion ]
where frame_start and frame_end can be one of
UNBOUNDED PRECEDING
offset PRECEDING
CURRENT ROW
offset FOLLOWING
```

UNBOUNDED FOLLOWING

and frame\_exclusion can be one of

EXCLUDE CURRENT ROW EXCLUDE GROUP EXCLUDE TIES EXCLUDE NO OTHERS

Here, expression represents any value expression that does not itself contain window function calls.

window\_name is a reference to a named window specification defined in the query's WINDOW clause. Alternatively, a full window\_definition can be given within parentheses, using the same syntax as for defining a named window in the WINDOW clause; see the SELECT reference page for details. It's worth pointing out that OVER wname is not exactly equivalent to OVER (wname ...); the latter implies copying and modifying the window definition, and will be rejected if the referenced window specification includes a frame clause.

The PARTITION BY clause groups the rows of the query into *partitions*, which are processed separately by the window function. PARTITION BY works similarly to a query-level GROUP BY clause, except that its expressions are always just expressions and cannot be output-column names or numbers. Without PARTITION BY, all rows produced by the query are treated as a single partition. The ORDER BY clause determines the order in which the rows of a partition are processed by the window function. It works similarly to a query-level ORDER BY clause, but likewise cannot use output-column names or numbers. Without ORDER BY, rows are processed in an unspecified order.

The frame\_clause specifies the set of rows constituting the *window frame*, which is a subset of the current partition, for those window functions that act on the frame instead of the whole partition. The set of rows in the frame can vary depending on which row is the current row. The frame can be specified in RANGE, ROWS or GROUPS mode; in each case, it runs from the frame\_start to the frame\_end. If frame\_end is omitted, the end defaults to CURRENT ROW.

A frame\_start of UNBOUNDED PRECEDING means that the frame starts with the first row of the partition, and similarly a frame\_end of UNBOUNDED FOLLOWING means that the frame ends with the last row of the partition.

In RANGE or GROUPS mode, a frame\_start of CURRENT ROW means the frame starts with the current row's first *peer* row (a row that the window's ORDER BY clause sorts as equivalent to the current row), while a frame\_end of CURRENT ROW means the frame ends with the current row's last peer row. In ROWS mode, CURRENT ROW simply means the current row.

In the offset PRECEDING and offset FOLLOWING frame options, the offset must be an expression not containing any variables, aggregate functions, or window functions. The meaning of the offset depends on the frame mode:

- In ROWS mode, the offset must yield a non-null, non-negative integer, and the option means that the frame starts or ends the specified number of rows before or after the current row.
- In GROUPS mode, the offset again must yield a non-null, non-negative integer, and the option means that the frame starts or ends the specified number of *peer groups* before or after the current row's peer group, where a peer group is a set of rows that are equivalent in the ORDER BY ordering. (There must be an ORDER BY clause in the window definition to use GROUPS mode.)
- In RANGE mode, these options require that the ORDER BY clause specify exactly one column. The offset specifies the maximum difference between the value of that column in the current row and its value in preceding or following rows of the frame. The data type of the offset expression varies depending on the data type of the ordering column. For numeric ordering columns it is typically of the same type as the ordering column, but for datetime ordering columns it is an interval.

For example, if the ordering column is of type date or timestamp, one could write RANGE BETWEEN '1 day' PRECEDING AND '10 days' FOLLOWING. The offset is still required to be non-null and non-negative, though the meaning of "non-negative" depends on its data type.

In any case, the distance to the end of the frame is limited by the distance to the end of the partition, so that for rows near the partition ends the frame might contain fewer rows than elsewhere.

Notice that in both ROWS and GROUPS mode, 0 PRECEDING and 0 FOLLOWING are equivalent to CURRENT ROW. This normally holds in RANGE mode as well, for an appropriate data-type-specific meaning of "zero".

The frame\_exclusion option allows rows around the current row to be excluded from the frame, even if they would be included according to the frame start and frame end options. EXCLUDE CUR-RENT ROW excludes the current row from the frame. EXCLUDE GROUP excludes the current row and its ordering peers from the frame. EXCLUDE TIES excludes any peers of the current row from the frame, but not the current row itself. EXCLUDE NO OTHERS simply specifies explicitly the default behavior of not excluding the current row or its peers.

The default framing option is RANGE UNBOUNDED PRECEDING, which is the same as RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW. With ORDER BY, this sets the frame to be all rows from the partition start up through the current row's last ORDER BY peer. Without ORDER BY, this means all rows of the partition are included in the window frame, since all rows become peers of the current row.

Restrictions are that frame\_start cannot be UNBOUNDED FOLLOWING, frame\_end cannot be UNBOUNDED PRECEDING, and the frame\_end choice cannot appear earlier in the above list of frame\_start and frame\_end options than the frame\_start choice does — for example RANGE BETWEEN CURRENT ROW AND offset PRECEDING is not allowed. But, for example, ROWS BETWEEN 7 PRECEDING AND 8 PRECEDING is allowed, even though it would never select any rows.

If FILTER is specified, then only the input rows for which the filter\_clause evaluates to true are fed to the window function; other rows are discarded. Only window functions that are aggregates accept a FILTER clause.

The built-in window functions are described in Table 9.62. Other window functions can be added by the user. Also, any built-in or user-defined general-purpose or statistical aggregate can be used as a window function. (Ordered-set and hypothetical-set aggregates cannot presently be used as window functions.)

The syntaxes using \* are used for calling parameter-less aggregate functions as window functions, for example count(\*) OVER (PARTITION BY x ORDER BY y). The asterisk (\*) is customarily not used for window-specific functions. Window-specific functions do not allow DISTINCT or ORDER BY to be used within the function argument list.

Window function calls are permitted only in the SELECT list and the ORDER BY clause of the query.

More information about window functions can be found in [Section 3.5](#page-57-0), Section 9.22, and [Section 7.2.5.](#page-165-1)

## <span id="page-86-0"></span>**4.2.9. Type Casts**

A type cast specifies a conversion from one data type to another. PostgreSQL accepts two equivalent syntaxes for type casts:

```
CAST ( expression AS type )
expression::type
```

The CAST syntax conforms to SQL; the syntax with :: is historical PostgreSQL usage.

When a cast is applied to a value expression of a known type, it represents a run-time type conversion. The cast will succeed only if a suitable type conversion operation has been defined. Notice that this is subtly different from the use of casts with constants, as shown in [Section 4.1.2.7](#page-76-1). A cast applied to an unadorned string literal represents the initial assignment of a type to a literal constant value, and so it will succeed for any type (if the contents of the string literal are acceptable input syntax for the data type).

An explicit type cast can usually be omitted if there is no ambiguity as to the type that a value expression must produce (for example, when it is assigned to a table column); the system will automatically apply a type cast in such cases. However, automatic casting is only done for casts that are marked "OK to apply implicitly" in the system catalogs. Other casts must be invoked with explicit casting syntax. This restriction is intended to prevent surprising conversions from being applied silently.

It is also possible to specify a type cast using a function-like syntax:

```
typename ( expression )
```

However, this only works for types whose names are also valid as function names. For example, double precision cannot be used this way, but the equivalent float8 can. Also, the names interval, time, and timestamp can only be used in this fashion if they are double-quoted, because of syntactic conflicts. Therefore, the use of the function-like cast syntax leads to inconsistencies and should probably be avoided.

#### **Note**

The function-like syntax is in fact just a function call. When one of the two standard cast syntaxes is used to do a run-time conversion, it will internally invoke a registered function to perform the conversion. By convention, these conversion functions have the same name as their output type, and thus the "function-like syntax" is nothing more than a direct invocation of the underlying conversion function. Obviously, this is not something that a portable application should rely on. For further details see CREATE CAST.

## <span id="page-87-0"></span>**4.2.10. Collation Expressions**

The COLLATE clause overrides the collation of an expression. It is appended to the expression it applies to:

```
expr COLLATE collation
```

where collation is a possibly schema-qualified identifier. The COLLATE clause binds tighter than operators; parentheses can be used when necessary.

If no collation is explicitly specified, the database system either derives a collation from the columns involved in the expression, or it defaults to the default collation of the database if no column is involved in the expression.

The two common uses of the COLLATE clause are overriding the sort order in an ORDER BY clause, for example:

```
SELECT a, b, c FROM tbl WHERE ... ORDER BY a COLLATE "C";
```

and overriding the collation of a function or operator call that has locale-sensitive results, for example:

```
SELECT * FROM tbl WHERE a > 'foo' COLLATE "C";
```

Note that in the latter case the COLLATE clause is attached to an input argument of the operator we wish to affect. It doesn't matter which argument of the operator or function call the COLLATE clause is attached to, because the collation that is applied by the operator or function is derived by considering all arguments, and an explicit COLLATE clause will override the collations of all other arguments. (Attaching non-matching COLLATE clauses to more than one argument, however, is an error. For more details see Section 24.2.) Thus, this gives the same result as the previous example:

```
SELECT * FROM tbl WHERE a COLLATE "C" > 'foo';
But this is an error:
SELECT * FROM tbl WHERE (a > 'foo') COLLATE "C";
```

because it attempts to apply a collation to the result of the > operator, which is of the non-collatable data type boolean.

## <span id="page-88-0"></span>**4.2.11. Scalar Subqueries**

A scalar subquery is an ordinary SELECT query in parentheses that returns exactly one row with one column. (See [Chapter 7](#page-149-0) for information about writing queries.) The SELECT query is executed and the single returned value is used in the surrounding value expression. It is an error to use a query that returns more than one row or more than one column as a scalar subquery. (But if, during a particular execution, the subquery returns no rows, there is no error; the scalar result is taken to be null.) The subquery can refer to variables from the surrounding query, which will act as constants during any one evaluation of the subquery. See also Section 9.23 for other expressions involving subqueries.

For example, the following finds the largest city population in each state:

```
SELECT name, (SELECT max(pop) FROM cities WHERE cities.state =
 states.name)
 FROM states;
```

## <span id="page-88-1"></span>**4.2.12. Array Constructors**

An array constructor is an expression that builds an array value using values for its member elements. A simple array constructor consists of the key word ARRAY, a left square bracket [, a list of expressions (separated by commas) for the array element values, and finally a right square bracket ]. For example:

```
SELECT ARRAY[1,2,3+4];
 array
---------
 {1,2,7}
(1 row)
```

By default, the array element type is the common type of the member expressions, determined using the same rules as for UNION or CASE constructs (see Section 10.5). You can override this by explicitly casting the array constructor to the desired type, for example:

```
SELECT ARRAY[1,2,22.7]::integer[];
 array
----------
 {1,2,23}
(1 row)
```

This has the same effect as casting each expression to the array element type individually. For more on casting, see [Section 4.2.9.](#page-86-0)

Multidimensional array values can be built by nesting array constructors. In the inner constructors, the key word ARRAY can be omitted. For example, these produce the same result:

```
SELECT ARRAY[ARRAY[1,2], ARRAY[3,4]];
 array
---------------
 {{1,2},{3,4}}
(1 row)
SELECT ARRAY[[1,2],[3,4]];
 array
---------------
 {{1,2},{3,4}}
(1 row)
```

Since multidimensional arrays must be rectangular, inner constructors at the same level must produce sub-arrays of identical dimensions. Any cast applied to the outer ARRAY constructor propagates automatically to all the inner constructors.

Multidimensional array constructor elements can be anything yielding an array of the proper kind, not only a sub-ARRAY construct. For example:

```
CREATE TABLE arr(f1 int[], f2 int[]);
INSERT INTO arr VALUES (ARRAY[[1,2],[3,4]], ARRAY[[5,6],[7,8]]);
SELECT ARRAY[f1, f2, '{{9,10},{11,12}}'::int[]] FROM arr;
 array
------------------------------------------------
 {{{1,2},{3,4}},{{5,6},{7,8}},{{9,10},{11,12}}}
(1 row)
```

You can construct an empty array, but since it's impossible to have an array with no type, you must explicitly cast your empty array to the desired type. For example:

```
SELECT ARRAY[]::integer[];
 array
-------
 {}
(1 row)
```

It is also possible to construct an array from the results of a subquery. In this form, the array constructor is written with the key word ARRAY followed by a parenthesized (not bracketed) subquery. For example:

```
SELECT ARRAY(SELECT oid FROM pg_proc WHERE proname LIKE 'bytea%');
 array
------------------------------------------------------------------
 {2011,1954,1948,1952,1951,1244,1950,2005,1949,1953,2006,31,2412}
(1 row)
SELECT ARRAY(SELECT ARRAY[i, i*2] FROM generate_series(1,5) AS
 a(i));
```

```
 array
----------------------------------
 {{1,2},{2,4},{3,6},{4,8},{5,10}}
(1 row)
```

The subquery must return a single column. If the subquery's output column is of a non-array type, the resulting one-dimensional array will have an element for each row in the subquery result, with an element type matching that of the subquery's output column. If the subquery's output column is of an array type, the result will be an array of the same type but one higher dimension; in this case all the subquery rows must yield arrays of identical dimensionality, else the result would not be rectangular.

The subscripts of an array value built with ARRAY always begin with one. For more information about arrays, see Section 8.15.

## <span id="page-90-0"></span>**4.2.13. Row Constructors**

A row constructor is an expression that builds a row value (also called a composite value) using values for its member fields. A row constructor consists of the key word ROW, a left parenthesis, zero or more expressions (separated by commas) for the row field values, and finally a right parenthesis. For example:

```
SELECT ROW(1,2.5,'this is a test');
```

The key word ROW is optional when there is more than one expression in the list.

A row constructor can include the syntax rowvalue.\*, which will be expanded to a list of the elements of the row value, just as occurs when the .\* syntax is used at the top level of a SELECT list (see Section 8.16.5). For example, if table t has columns f1 and f2, these are the same:

```
SELECT ROW(t.*, 42) FROM t;
SELECT ROW(t.f1, t.f2, 42) FROM t;
```

#### **Note**

Before PostgreSQL 8.2, the .\* syntax was not expanded in row constructors, so that writing ROW(t.\*, 42) created a two-field row whose first field was another row value. The new behavior is usually more useful. If you need the old behavior of nested row values, write the inner row value without .\*, for instance ROW(t, 42).

By default, the value created by a ROW expression is of an anonymous record type. If necessary, it can be cast to a named composite type — either the row type of a table, or a composite type created with CREATE TYPE AS. An explicit cast might be needed to avoid ambiguity. For example:

```
CREATE TABLE mytable(f1 int, f2 float, f3 text);
CREATE FUNCTION getf1(mytable) RETURNS int AS 'SELECT $1.f1'
 LANGUAGE SQL;
-- No cast needed since only one getf1() exists
SELECT getf1(ROW(1,2.5,'this is a test'));
 getf1
-------
 1
(1 row)
```

```
CREATE TYPE myrowtype AS (f1 int, f2 text, f3 numeric);
CREATE FUNCTION getf1(myrowtype) RETURNS int AS 'SELECT $1.f1'
 LANGUAGE SQL;
-- Now we need a cast to indicate which function to call:
SELECT getf1(ROW(1,2.5,'this is a test'));
ERROR: function getf1(record) is not unique
SELECT getf1(ROW(1,2.5,'this is a test')::mytable);
 getf1
-------
 1
(1 row)
SELECT getf1(CAST(ROW(11,'this is a test',2.5) AS myrowtype));
 getf1
-------
 11
(1 row)
```

Row constructors can be used to build composite values to be stored in a composite-type table column, or to be passed to a function that accepts a composite parameter. Also, it is possible to compare two row values or test a row with IS NULL or IS NOT NULL, for example:

```
SELECT ROW(1,2.5,'this is a test') = ROW(1, 3, 'not the same');
SELECT ROW(table.*) IS NULL FROM table; -- detect all-null rows
```

For more detail see Section 9.24. Row constructors can also be used in connection with subqueries, as discussed in Section 9.23.

## <span id="page-91-0"></span>**4.2.14. Expression Evaluation Rules**

The order of evaluation of subexpressions is not defined. In particular, the inputs of an operator or function are not necessarily evaluated left-to-right or in any other fixed order.

Furthermore, if the result of an expression can be determined by evaluating only some parts of it, then other subexpressions might not be evaluated at all. For instance, if one wrote:

```
SELECT true OR somefunc();
```

then somefunc() would (probably) not be called at all. The same would be the case if one wrote:

```
SELECT somefunc() OR true;
```

Note that this is not the same as the left-to-right "short-circuiting" of Boolean operators that is found in some programming languages.

As a consequence, it is unwise to use functions with side effects as part of complex expressions. It is particularly dangerous to rely on side effects or evaluation order in WHERE and HAVING clauses, since those clauses are extensively reprocessed as part of developing an execution plan. Boolean expressions (AND/OR/NOT combinations) in those clauses can be reorganized in any manner allowed by the laws of Boolean algebra.

When it is essential to force evaluation order, a CASE construct (see Section 9.18) can be used. For example, this is an untrustworthy way of trying to avoid division by zero in a WHERE clause:

```
SELECT ... WHERE x > 0 AND y/x > 1.5;
```

But this is safe:

```
SELECT ... WHERE CASE WHEN x > 0 THEN y/x > 1.5 ELSE false END;
```

A CASE construct used in this fashion will defeat optimization attempts, so it should only be done when necessary. (In this particular example, it would be better to sidestep the problem by writing y > 1.5\*x instead.)

CASE is not a cure-all for such issues, however. One limitation of the technique illustrated above is that it does not prevent early evaluation of constant subexpressions. As described in Section 38.7, functions and operators marked IMMUTABLE can be evaluated when the query is planned rather than when it is executed. Thus for example

```
SELECT CASE WHEN x > 0 THEN x ELSE 1/0 END FROM tab;
```

is likely to result in a division-by-zero failure due to the planner trying to simplify the constant subexpression, even if every row in the table has x > 0 so that the ELSE arm would never be entered at run time.

While that particular example might seem silly, related cases that don't obviously involve constants can occur in queries executed within functions, since the values of function arguments and local variables can be inserted into queries as constants for planning purposes. Within PL/pgSQL functions, for example, using an IF-THEN-ELSE statement to protect a risky computation is much safer than just nesting it in a CASE expression.

Another limitation of the same kind is that a CASE cannot prevent evaluation of an aggregate expression contained within it, because aggregate expressions are computed before other expressions in a SELECT list or HAVING clause are considered. For example, the following query can cause a division-by-zero error despite seemingly having protected against it:

```
SELECT CASE WHEN min(employees) > 0
 THEN avg(expenses / employees)
 END
 FROM departments;
```

The min() and avg() aggregates are computed concurrently over all the input rows, so if any row has employees equal to zero, the division-by-zero error will occur before there is any opportunity to test the result of min(). Instead, use a WHERE or FILTER clause to prevent problematic input rows from reaching an aggregate function in the first place.

# <span id="page-92-0"></span>**4.3. Calling Functions**

PostgreSQL allows functions that have named parameters to be called using either *positional* or *named* notation. Named notation is especially useful for functions that have a large number of parameters, since it makes the associations between parameters and actual arguments more explicit and reliable. In positional notation, a function call is written with its argument values in the same order as they are defined in the function declaration. In named notation, the arguments are matched to the function parameters by name and can be written in any order. For each notation, also consider the effect of function argument types, documented in Section 10.3.

In either notation, parameters that have default values given in the function declaration need not be written in the call at all. But this is particularly useful in named notation, since any combination of parameters can be omitted; while in positional notation parameters can only be omitted from right to left.

PostgreSQL also supports *mixed* notation, which combines positional and named notation. In this case, positional parameters are written first and named parameters appear after them.

The following examples will illustrate the usage of all three notations, using the following function definition:

```
CREATE FUNCTION concat_lower_or_upper(a text, b text, uppercase
 boolean DEFAULT false)
RETURNS text
AS
$$
 SELECT CASE
 WHEN $3 THEN UPPER($1 || ' ' || $2)
 ELSE LOWER($1 || ' ' || $2)
 END;
$$
LANGUAGE SQL IMMUTABLE STRICT;
```

Function concat\_lower\_or\_upper has two mandatory parameters, a and b. Additionally there is one optional parameter uppercase which defaults to false. The a and b inputs will be concatenated, and forced to either upper or lower case depending on the uppercase parameter. The remaining details of this function definition are not important here (see Chapter 38 for more information).

## <span id="page-93-0"></span>**4.3.1. Using Positional Notation**

Positional notation is the traditional mechanism for passing arguments to functions in PostgreSQL. An example is:

```
SELECT concat_lower_or_upper('Hello', 'World', true);
 concat_lower_or_upper 
-----------------------
 HELLO WORLD
(1 row)
```

All arguments are specified in order. The result is upper case since uppercase is specified as true. Another example is:

```
SELECT concat_lower_or_upper('Hello', 'World');
 concat_lower_or_upper 
-----------------------
 hello world
(1 row)
```

Here, the uppercase parameter is omitted, so it receives its default value of false, resulting in lower case output. In positional notation, arguments can be omitted from right to left so long as they have defaults.

## <span id="page-93-1"></span>**4.3.2. Using Named Notation**

In named notation, each argument's name is specified using => to separate it from the argument expression. For example:

```
SELECT concat_lower_or_upper(a => 'Hello', b => 'World');
 concat_lower_or_upper 
-----------------------
```

```
 hello world
(1 row)
```

Again, the argument uppercase was omitted so it is set to false implicitly. One advantage of using named notation is that the arguments may be specified in any order, for example:

```
SELECT concat_lower_or_upper(a => 'Hello', b => 'World', uppercase
 => true);
 concat_lower_or_upper 
-----------------------
 HELLO WORLD
(1 row)
SELECT concat_lower_or_upper(a => 'Hello', uppercase => true, b =>
 'World');
 concat_lower_or_upper 
-----------------------
 HELLO WORLD
(1 row)
```

An older syntax based on ":=" is supported for backward compatibility:

```
SELECT concat_lower_or_upper(a := 'Hello', uppercase := true, b :=
 'World');
 concat_lower_or_upper 
-----------------------
 HELLO WORLD
(1 row)
```

## <span id="page-94-0"></span>**4.3.3. Using Mixed Notation**

The mixed notation combines positional and named notation. However, as already mentioned, named arguments cannot precede positional arguments. For example:

```
SELECT concat_lower_or_upper('Hello', 'World', uppercase => true);
 concat_lower_or_upper 
-----------------------
 HELLO WORLD
(1 row)
```

In the above query, the arguments a and b are specified positionally, while uppercase is specified by name. In this example, that adds little except documentation. With a more complex function having numerous parameters that have default values, named or mixed notation can save a great deal of writing and reduce chances for error.

#### **Note**

Named and mixed call notations currently cannot be used when calling an aggregate function (but they do work when an aggregate function is used as a window function).

# <span id="page-95-0"></span>**Chapter 5. Data Definition**

This chapter covers how one creates the database structures that will hold one's data. In a relational database, the raw data is stored in tables, so the majority of this chapter is devoted to explaining how tables are created and modified and what features are available to control what data is stored in the tables. Subsequently, we discuss how tables can be organized into schemas, and how privileges can be assigned to tables. Finally, we will briefly look at other features that affect the data storage, such as inheritance, table partitioning, views, functions, and triggers.

# <span id="page-95-1"></span>**5.1. Table Basics**

A table in a relational database is much like a table on paper: It consists of rows and columns. The number and order of the columns is fixed, and each column has a name. The number of rows is variable — it reflects how much data is stored at a given moment. SQL does not make any guarantees about the order of the rows in a table. When a table is read, the rows will appear in an unspecified order, unless sorting is explicitly requested. This is covered in [Chapter 7.](#page-149-0) Furthermore, SQL does not assign unique identifiers to rows, so it is possible to have several completely identical rows in a table. This is a consequence of the mathematical model that underlies SQL but is usually not desirable. Later in this chapter we will see how to deal with this issue.

Each column has a data type. The data type constrains the set of possible values that can be assigned to a column and assigns semantics to the data stored in the column so that it can be used for computations. For instance, a column declared to be of a numerical type will not accept arbitrary text strings, and the data stored in such a column can be used for mathematical computations. By contrast, a column declared to be of a character string type will accept almost any kind of data but it does not lend itself to mathematical calculations, although other operations such as string concatenation are available.

PostgreSQL includes a sizable set of built-in data types that fit many applications. Users can also define their own data types. Most built-in data types have obvious names and semantics, so we defer a detailed explanation to [Chapter 8.](#page-180-0) Some of the frequently used data types are integer for whole numbers, numeric for possibly fractional numbers, text for character strings, date for dates, time for time-of-day values, and timestamp for values containing both date and time.

To create a table, you use the aptly named CREATE TABLE command. In this command you specify at least a name for the new table, the names of the columns and the data type of each column. For example:

```
CREATE TABLE my_first_table (
 first_column text,
 second_column integer
);
```

This creates a table named my\_first\_table with two columns. The first column is named first\_column and has a data type of text; the second column has the name second\_column and the type integer. The table and column names follow the identifier syntax explained in [Sec](#page-70-2)[tion 4.1.1.](#page-70-2) The type names are usually also identifiers, but there are some exceptions. Note that the column list is comma-separated and surrounded by parentheses.

Of course, the previous example was heavily contrived. Normally, you would give names to your tables and columns that convey what kind of data they store. So let's look at a more realistic example:

```
CREATE TABLE products (
 product_no integer,
 name text,
```

```
 price numeric
);
```

(The numeric type can store fractional components, as would be typical of monetary amounts.)

#### **Tip**

When you create many interrelated tables it is wise to choose a consistent naming pattern for the tables and columns. For instance, there is a choice of using singular or plural nouns for table names, both of which are favored by some theorist or other.

There is a limit on how many columns a table can contain. Depending on the column types, it is between 250 and 1600. However, defining a table with anywhere near this many columns is highly unusual and often a questionable design.

If you no longer need a table, you can remove it using the DROP TABLE command. For example:

```
DROP TABLE my_first_table;
DROP TABLE products;
```

Attempting to drop a table that does not exist is an error. Nevertheless, it is common in SQL script files to unconditionally try to drop each table before creating it, ignoring any error messages, so that the script works whether or not the table exists. (If you like, you can use the DROP TABLE IF EXISTS variant to avoid the error messages, but this is not standard SQL.)

If you need to modify a table that already exists, see [Section 5.6](#page-107-0) later in this chapter.

With the tools discussed so far you can create fully functional tables. The remainder of this chapter is concerned with adding features to the table definition to ensure data integrity, security, or convenience. If you are eager to fill your tables with data now you can skip ahead to [Chapter 6](#page-145-0) and read the rest of this chapter later.

# <span id="page-96-0"></span>**5.2. Default Values**

A column can be assigned a default value. When a new row is created and no values are specified for some of the columns, those columns will be filled with their respective default values. A data manipulation command can also request explicitly that a column be set to its default value, without having to know what that value is. (Details about data manipulation commands are in [Chapter 6](#page-145-0).)

 If no default value is declared explicitly, the default value is the null value. This usually makes sense because a null value can be considered to represent unknown data.

In a table definition, default values are listed after the column data type. For example:

```
CREATE TABLE products (
 product_no integer,
 name text,
 price numeric DEFAULT 9.99
);
```

The default value can be an expression, which will be evaluated whenever the default value is inserted (*not* when the table is created). A common example is for a timestamp column to have a default of CURRENT\_TIMESTAMP, so that it gets set to the time of row insertion. Another common example is generating a "serial number" for each row. In PostgreSQL this is typically done by something like:

```
CREATE TABLE products (
 product_no integer DEFAULT nextval('products_product_no_seq'),
 ...
);
```

where the nextval() function supplies successive values from a *sequence object* (see Section 9.17). This arrangement is sufficiently common that there's a special shorthand for it:

```
CREATE TABLE products (
 product_no SERIAL,
 ...
);
```

The SERIAL shorthand is discussed further in [Section 8.1.4.](#page-185-0)

# <span id="page-97-0"></span>**5.3. Generated Columns**

A generated column is a special column that is always computed from other columns. Thus, it is for columns what a view is for tables. There are two kinds of generated columns: stored and virtual. A stored generated column is computed when it is written (inserted or updated) and occupies storage as if it were a normal column. A virtual generated column occupies no storage and is computed when it is read. Thus, a virtual generated column is similar to a view and a stored generated column is similar to a materialized view (except that it is always updated automatically). PostgreSQL currently implements only stored generated columns.

To create a generated column, use the GENERATED ALWAYS AS clause in CREATE TABLE, for example:

```
CREATE TABLE people (
 ...,
 height_cm numeric,
 height_in numeric GENERATED ALWAYS AS (height_cm / 2.54) STORED
);
```

The keyword STORED must be specified to choose the stored kind of generated column. See CREATE TABLE for more details.

A generated column cannot be written to directly. In INSERT or UPDATE commands, a value cannot be specified for a generated column, but the keyword DEFAULT may be specified.

Consider the differences between a column with a default and a generated column. The column default is evaluated once when the row is first inserted if no other value was provided; a generated column is updated whenever the row changes and cannot be overridden. A column default may not refer to other columns of the table; a generation expression would normally do so. A column default can use volatile functions, for example random() or functions referring to the current time; this is not allowed for generated columns.

Several restrictions apply to the definition of generated columns and tables involving generated columns:

- The generation expression can only use immutable functions and cannot use subqueries or reference anything other than the current row in any way.
- A generation expression cannot reference another generated column.
- A generation expression cannot reference a system column, except tableoid.

- A generated column cannot have a column default or an identity definition.
- A generated column cannot be part of a partition key.
- Foreign tables can have generated columns. See CREATE FOREIGN TABLE for details.
- For inheritance:
  - If a parent column is a generated column, a child column must also be a generated column using the same expression. In the definition of the child column, leave off the GENERATED clause, as it will be copied from the parent.
  - In case of multiple inheritance, if one parent column is a generated column, then all parent columns must be generated columns and with the same expression.
  - If a parent column is not a generated column, a child column may be defined to be a generated column or not.

Additional considerations apply to the use of generated columns.

- Generated columns maintain access privileges separately from their underlying base columns. So, it is possible to arrange it so that a particular role can read from a generated column but not from the underlying base columns.
- Generated columns are, conceptually, updated after BEFORE triggers have run. Therefore, changes made to base columns in a BEFORE trigger will be reflected in generated columns. But conversely, it is not allowed to access generated columns in BEFORE triggers.
- Generated columns are skipped for logical replication.

# <span id="page-98-0"></span>**5.4. Constraints**

Data types are a way to limit the kind of data that can be stored in a table. For many applications, however, the constraint they provide is too coarse. For example, a column containing a product price should probably only accept positive values. But there is no standard data type that accepts only positive numbers. Another issue is that you might want to constrain column data with respect to other columns or rows. For example, in a table containing product information, there should be only one row for each product number.

To that end, SQL allows you to define constraints on columns and tables. Constraints give you as much control over the data in your tables as you wish. If a user attempts to store data in a column that would violate a constraint, an error is raised. This applies even if the value came from the default value definition.

## <span id="page-98-1"></span>**5.4.1. Check Constraints**

A check constraint is the most generic constraint type. It allows you to specify that the value in a certain column must satisfy a Boolean (truth-value) expression. For instance, to require positive product prices, you could use:

```
CREATE TABLE products (
 product_no integer,
 name text,
 price numeric CHECK (price > 0)
);
```

As you see, the constraint definition comes after the data type, just like default value definitions. Default values and constraints can be listed in any order. A check constraint consists of the key word CHECK followed by an expression in parentheses. The check constraint expression should involve the column thus constrained, otherwise the constraint would not make too much sense.

You can also give the constraint a separate name. This clarifies error messages and allows you to refer to the constraint when you need to change it. The syntax is:

```
CREATE TABLE products (
 product_no integer,
 name text,
 price numeric CONSTRAINT positive_price CHECK (price > 0)
);
```

So, to specify a named constraint, use the key word CONSTRAINT followed by an identifier followed by the constraint definition. (If you don't specify a constraint name in this way, the system chooses a name for you.)

A check constraint can also refer to several columns. Say you store a regular price and a discounted price, and you want to ensure that the discounted price is lower than the regular price:

```
CREATE TABLE products (
 product_no integer,
 name text,
 price numeric CHECK (price > 0),
 discounted_price numeric CHECK (discounted_price > 0),
 CHECK (price > discounted_price)
);
```

The first two constraints should look familiar. The third one uses a new syntax. It is not attached to a particular column, instead it appears as a separate item in the comma-separated column list. Column definitions and these constraint definitions can be listed in mixed order.

We say that the first two constraints are column constraints, whereas the third one is a table constraint because it is written separately from any one column definition. Column constraints can also be written as table constraints, while the reverse is not necessarily possible, since a column constraint is supposed to refer to only the column it is attached to. (PostgreSQL doesn't enforce that rule, but you should follow it if you want your table definitions to work with other database systems.) The above example could also be written as:

```
CREATE TABLE products (
 product_no integer,
 name text,
 price numeric,
 CHECK (price > 0),
 discounted_price numeric,
 CHECK (discounted_price > 0),
 CHECK (price > discounted_price)
);
or even:
CREATE TABLE products (
 product_no integer,
 name text,
 price numeric CHECK (price > 0),
 discounted_price numeric,
```

```
 CHECK (discounted_price > 0 AND price > discounted_price)
);
```

It's a matter of taste.

Names can be assigned to table constraints in the same way as column constraints:

```
CREATE TABLE products (
 product_no integer,
 name text,
 price numeric,
 CHECK (price > 0),
 discounted_price numeric,
 CHECK (discounted_price > 0),
 CONSTRAINT valid_discount CHECK (price > discounted_price)
);
```

It should be noted that a check constraint is satisfied if the check expression evaluates to true or the null value. Since most expressions will evaluate to the null value if any operand is null, they will not prevent null values in the constrained columns. To ensure that a column does not contain null values, the not-null constraint described in the next section can be used.

#### **Note**

PostgreSQL does not support CHECK constraints that reference table data other than the new or updated row being checked. While a CHECK constraint that violates this rule may appear to work in simple tests, it cannot guarantee that the database will not reach a state in which the constraint condition is false (due to subsequent changes of the other row(s) involved). This would cause a database dump and restore to fail. The restore could fail even when the complete database state is consistent with the constraint, due to rows not being loaded in an order that will satisfy the constraint. If possible, use UNIQUE, EXCLUDE, or FOREIGN KEY constraints to express cross-row and cross-table restrictions.

If what you desire is a one-time check against other rows at row insertion, rather than a continuously-maintained consistency guarantee, a custom trigger can be used to implement that. (This approach avoids the dump/restore problem because pg\_dump does not reinstall triggers until after restoring data, so that the check will not be enforced during a dump/restore.)

#### **Note**

PostgreSQL assumes that CHECK constraints' conditions are immutable, that is, they will always give the same result for the same input row. This assumption is what justifies examining CHECK constraints only when rows are inserted or updated, and not at other times. (The warning above about not referencing other table data is really a special case of this restriction.)

An example of a common way to break this assumption is to reference a user-defined function in a CHECK expression, and then change the behavior of that function. PostgreSQL does not disallow that, but it will not notice if there are rows in the table that now violate the CHECK constraint. That would cause a subsequent database dump and restore to fail. The recommended way to handle such a change is to drop the constraint (using ALTER TABLE), adjust the function definition, and re-add the constraint, thereby rechecking it against all table rows.

## <span id="page-100-0"></span>**5.4.2. Not-Null Constraints**

A not-null constraint simply specifies that a column must not assume the null value. A syntax example:

```
CREATE TABLE products (
 product_no integer NOT NULL,
 name text NOT NULL,
 price numeric
);
```

A not-null constraint is always written as a column constraint. A not-null constraint is functionally equivalent to creating a check constraint CHECK (column\_name IS NOT NULL), but in PostgreSQL creating an explicit not-null constraint is more efficient. The drawback is that you cannot give explicit names to not-null constraints created this way.

Of course, a column can have more than one constraint. Just write the constraints one after another:

```
CREATE TABLE products (
 product_no integer NOT NULL,
 name text NOT NULL,
 price numeric NOT NULL CHECK (price > 0)
);
```

The order doesn't matter. It does not necessarily determine in which order the constraints are checked.

The NOT NULL constraint has an inverse: the NULL constraint. This does not mean that the column must be null, which would surely be useless. Instead, this simply selects the default behavior that the column might be null. The NULL constraint is not present in the SQL standard and should not be used in portable applications. (It was only added to PostgreSQL to be compatible with some other database systems.) Some users, however, like it because it makes it easy to toggle the constraint in a script file. For example, you could start with:

```
CREATE TABLE products (
 product_no integer NULL,
 name text NULL,
 price numeric NULL
);
```

and then insert the NOT key word where desired.

#### **Tip**

In most database designs the majority of columns should be marked not null.

## <span id="page-101-0"></span>**5.4.3. Unique Constraints**

Unique constraints ensure that the data contained in a column, or a group of columns, is unique among all the rows in the table. The syntax is:

```
CREATE TABLE products (
 product_no integer UNIQUE,
 name text,
 price numeric
);
```

when written as a column constraint, and:

```
CREATE TABLE products (
 product_no integer,
 name text,
 price numeric,
 UNIQUE (product_no)
);
```

when written as a table constraint.

To define a unique constraint for a group of columns, write it as a table constraint with the column names separated by commas:

```
CREATE TABLE example (
 a integer,
 b integer,
 c integer,
 UNIQUE (a, c)
);
```

This specifies that the combination of values in the indicated columns is unique across the whole table, though any one of the columns need not be (and ordinarily isn't) unique.

You can assign your own name for a unique constraint, in the usual way:

```
CREATE TABLE products (
 product_no integer CONSTRAINT must_be_different UNIQUE,
 name text,
 price numeric
);
```

Adding a unique constraint will automatically create a unique B-tree index on the column or group of columns listed in the constraint. A uniqueness restriction covering only some rows cannot be written as a unique constraint, but it is possible to enforce such a restriction by creating a unique partial index.

In general, a unique constraint is violated if there is more than one row in the table where the values of all of the columns included in the constraint are equal. However, two null values are never considered equal in this comparison. That means even in the presence of a unique constraint it is possible to store duplicate rows that contain a null value in at least one of the constrained columns. This behavior conforms to the SQL standard, but we have heard that other SQL databases might not follow this rule. So be careful when developing applications that are intended to be portable.

## <span id="page-102-0"></span>**5.4.4. Primary Keys**

A primary key constraint indicates that a column, or group of columns, can be used as a unique identifier for rows in the table. This requires that the values be both unique and not null. So, the following two table definitions accept the same data:

```
CREATE TABLE products (
 product_no integer UNIQUE NOT NULL,
 name text,
 price numeric
);
```

```
CREATE TABLE products (
 product_no integer PRIMARY KEY,
 name text,
 price numeric
);
```

Primary keys can span more than one column; the syntax is similar to unique constraints:

```
CREATE TABLE example (
 a integer,
 b integer,
 c integer,
 PRIMARY KEY (a, c)
);
```

Adding a primary key will automatically create a unique B-tree index on the column or group of columns listed in the primary key, and will force the column(s) to be marked NOT NULL.

A table can have at most one primary key. (There can be any number of unique and not-null constraints, which are functionally almost the same thing, but only one can be identified as the primary key.) Relational database theory dictates that every table must have a primary key. This rule is not enforced by PostgreSQL, but it is usually best to follow it.

Primary keys are useful both for documentation purposes and for client applications. For example, a GUI application that allows modifying row values probably needs to know the primary key of a table to be able to identify rows uniquely. There are also various ways in which the database system makes use of a primary key if one has been declared; for example, the primary key defines the default target column(s) for foreign keys referencing its table.

## <span id="page-103-0"></span>**5.4.5. Foreign Keys**

A foreign key constraint specifies that the values in a column (or a group of columns) must match the values appearing in some row of another table. We say this maintains the *referential integrity* between two related tables.

Say you have the product table that we have used several times already:

```
CREATE TABLE products (
 product_no integer PRIMARY KEY,
 name text,
 price numeric
);
```

Let's also assume you have a table storing orders of those products. We want to ensure that the orders table only contains orders of products that actually exist. So we define a foreign key constraint in the orders table that references the products table:

```
CREATE TABLE orders (
 order_id integer PRIMARY KEY,
 product_no integer REFERENCES products (product_no),
 quantity integer
);
```

Now it is impossible to create orders with non-NULL product\_no entries that do not appear in the products table.

We say that in this situation the orders table is the *referencing* table and the products table is the *referenced* table. Similarly, there are referencing and referenced columns.

You can also shorten the above command to:

```
CREATE TABLE orders (
 order_id integer PRIMARY KEY,
 product_no integer REFERENCES products,
 quantity integer
);
```

because in absence of a column list the primary key of the referenced table is used as the referenced column(s).

You can assign your own name for a foreign key constraint, in the usual way.

A foreign key can also constrain and reference a group of columns. As usual, it then needs to be written in table constraint form. Here is a contrived syntax example:

```
CREATE TABLE t1 (
 a integer PRIMARY KEY,
 b integer,
 c integer,
 FOREIGN KEY (b, c) REFERENCES other_table (c1, c2)
);
```

Of course, the number and type of the constrained columns need to match the number and type of the referenced columns.

Sometimes it is useful for the "other table" of a foreign key constraint to be the same table; this is called a *self-referential* foreign key. For example, if you want rows of a table to represent nodes of a tree structure, you could write

```
CREATE TABLE tree (
 node_id integer PRIMARY KEY,
 parent_id integer REFERENCES tree,
 name text,
 ...
);
```

A top-level node would have NULL parent\_id, while non-NULL parent\_id entries would be constrained to reference valid rows of the table.

A table can have more than one foreign key constraint. This is used to implement many-to-many relationships between tables. Say you have tables about products and orders, but now you want to allow one order to contain possibly many products (which the structure above did not allow). You could use this table structure:

```
CREATE TABLE products (
 product_no integer PRIMARY KEY,
 name text,
 price numeric
);
CREATE TABLE orders (
 order_id integer PRIMARY KEY,
```

```
 shipping_address text,
 ...
);
CREATE TABLE order_items (
 product_no integer REFERENCES products,
 order_id integer REFERENCES orders,
 quantity integer,
 PRIMARY KEY (product_no, order_id)
);
```

Notice that the primary key overlaps with the foreign keys in the last table.

We know that the foreign keys disallow creation of orders that do not relate to any products. But what if a product is removed after an order is created that references it? SQL allows you to handle that as well. Intuitively, we have a few options:

- Disallow deleting a referenced product
- Delete the orders as well
- Something else?

To illustrate this, let's implement the following policy on the many-to-many relationship example above: when someone wants to remove a product that is still referenced by an order (via order\_items), we disallow it. If someone removes an order, the order items are removed as well:

```
CREATE TABLE products (
 product_no integer PRIMARY KEY,
 name text,
 price numeric
);
CREATE TABLE orders (
 order_id integer PRIMARY KEY,
 shipping_address text,
 ...
);
CREATE TABLE order_items (
 product_no integer REFERENCES products ON DELETE RESTRICT,
 order_id integer REFERENCES orders ON DELETE CASCADE,
 quantity integer,
 PRIMARY KEY (product_no, order_id)
);
```

Restricting and cascading deletes are the two most common options. RESTRICT prevents deletion of a referenced row. NO ACTION means that if any referencing rows still exist when the constraint is checked, an error is raised; this is the default behavior if you do not specify anything. (The essential difference between these two choices is that NO ACTION allows the check to be deferred until later in the transaction, whereas RESTRICT does not.) CASCADE specifies that when a referenced row is deleted, row(s) referencing it should be automatically deleted as well. There are two other options: SET NULL and SET DEFAULT. These cause the referencing column(s) in the referencing row(s) to be set to nulls or their default values, respectively, when the referenced row is deleted. Note that these do not excuse you from observing any constraints. For example, if an action specifies SET DEFAULT but the default value would not satisfy the foreign key constraint, the operation will fail.

Analogous to ON DELETE there is also ON UPDATE which is invoked when a referenced column is changed (updated). The possible actions are the same. In this case, CASCADE means that the updated values of the referenced column(s) should be copied into the referencing row(s).

Normally, a referencing row need not satisfy the foreign key constraint if any of its referencing columns are null. If MATCH FULL is added to the foreign key declaration, a referencing row escapes satisfying the constraint only if all its referencing columns are null (so a mix of null and non-null values is guaranteed to fail a MATCH FULL constraint). If you don't want referencing rows to be able to avoid satisfying the foreign key constraint, declare the referencing column(s) as NOT NULL.

A foreign key must reference columns that either are a primary key or form a unique constraint, or are columns from a non-partial unique index. This means that the referenced columns always have an index to allow efficient lookups on whether a referencing row has a match. Since a DELETE of a row from the referenced table or an UPDATE of a referenced column will require a scan of the referencing table for rows matching the old value, it is often a good idea to index the referencing columns too. Because this is not always needed, and there are many choices available on how to index, the declaration of a foreign key constraint does not automatically create an index on the referencing columns.

More information about updating and deleting data is in [Chapter 6](#page-145-0). Also see the description of foreign key constraint syntax in the reference documentation for CREATE TABLE.

## <span id="page-106-1"></span>**5.4.6. Exclusion Constraints**

Exclusion constraints ensure that if any two rows are compared on the specified columns or expressions using the specified operators, at least one of these operator comparisons will return false or null. The syntax is:

```
CREATE TABLE circles (
 c circle,
 EXCLUDE USING gist (c WITH &&)
);
See also CREATE TABLE ... CONSTRAINT ... EXCLUDE for details.
```

Adding an exclusion constraint will automatically create an index of the type specified in the constraint declaration.

# <span id="page-106-0"></span>**5.5. System Columns**

Every table has several *system columns* that are implicitly defined by the system. Therefore, these names cannot be used as names of user-defined columns. (Note that these restrictions are separate from whether the name is a key word or not; quoting a name will not allow you to escape these restrictions.) You do not really need to be concerned about these columns; just know they exist.

```
tableoid
```

The OID of the table containing this row. This column is particularly handy for queries that select from partitioned tables (see [Section 5.11\)](#page-128-0) or inheritance hierarchies (see [Section 5.10](#page-125-0)), since without it, it's difficult to tell which individual table a row came from. The tableoid can be joined against the oid column of pg\_class to obtain the table name.

xmin

The identity (transaction ID) of the inserting transaction for this row version. (A row version is an individual state of a row; each update of a row creates a new row version for the same logical row.)

cmin

The command identifier (starting at zero) within the inserting transaction.

xmax

The identity (transaction ID) of the deleting transaction, or zero for an undeleted row version. It is possible for this column to be nonzero in a visible row version. That usually indicates that the deleting transaction hasn't committed yet, or that an attempted deletion was rolled back.

cmax

The command identifier within the deleting transaction, or zero.

ctid

The physical location of the row version within its table. Note that although the ctid can be used to locate the row version very quickly, a row's ctid will change if it is updated or moved by VACUUM FULL. Therefore ctid is useless as a long-term row identifier. A primary key should be used to identify logical rows.

Transaction identifiers are also 32-bit quantities. In a long-lived database it is possible for transaction IDs to wrap around. This is not a fatal problem given appropriate maintenance procedures; see Chapter 25 for details. It is unwise, however, to depend on the uniqueness of transaction IDs over the long term (more than one billion transactions).

Command identifiers are also 32-bit quantities. This creates a hard limit of 232 (4 billion) SQL commands within a single transaction. In practice this limit is not a problem — note that the limit is on the number of SQL commands, not the number of rows processed. Also, only commands that actually modify the database contents will consume a command identifier.

# <span id="page-107-0"></span>**5.6. Modifying Tables**

When you create a table and you realize that you made a mistake, or the requirements of the application change, you can drop the table and create it again. But this is not a convenient option if the table is already filled with data, or if the table is referenced by other database objects (for instance a foreign key constraint). Therefore PostgreSQL provides a family of commands to make modifications to existing tables. Note that this is conceptually distinct from altering the data contained in the table: here we are interested in altering the definition, or structure, of the table.

#### You can:

- Add columns
- Remove columns
- Add constraints
- Remove constraints
- Change default values
- Change column data types
- Rename columns
- Rename tables

All these actions are performed using the ALTER TABLE command, whose reference page contains details beyond those given here.

## <span id="page-107-1"></span>**5.6.1. Adding a Column**

To add a column, use a command like:

ALTER TABLE products ADD COLUMN description text;

The new column is initially filled with whatever default value is given (null if you don't specify a DEFAULT clause).

### **Tip**

From PostgreSQL 11, adding a column with a constant default value no longer means that each row of the table needs to be updated when the ALTER TABLE statement is executed. Instead, the default value will be returned the next time the row is accessed, and applied when the table is rewritten, making the ALTER TABLE very fast even on large tables.

However, if the default value is volatile (e.g., clock\_timestamp()) each row will need to be updated with the value calculated at the time ALTER TABLE is executed. To avoid a potentially lengthy update operation, particularly if you intend to fill the column with mostly nondefault values anyway, it may be preferable to add the column with no default, insert the correct values using UPDATE, and then add any desired default as described below.

You can also define constraints on the column at the same time, using the usual syntax:

```
ALTER TABLE products ADD COLUMN description text CHECK (description
 <> '');
```

In fact all the options that can be applied to a column description in CREATE TABLE can be used here. Keep in mind however that the default value must satisfy the given constraints, or the ADD will fail. Alternatively, you can add constraints later (see below) after you've filled in the new column correctly.

## <span id="page-108-0"></span>**5.6.2. Removing a Column**

To remove a column, use a command like:

```
ALTER TABLE products DROP COLUMN description;
```

Whatever data was in the column disappears. Table constraints involving the column are dropped, too. However, if the column is referenced by a foreign key constraint of another table, PostgreSQL will not silently drop that constraint. You can authorize dropping everything that depends on the column by adding CASCADE:

```
ALTER TABLE products DROP COLUMN description CASCADE;
```

See [Section 5.14](#page-142-2) for a description of the general mechanism behind this.

## <span id="page-108-1"></span>**5.6.3. Adding a Constraint**

To add a constraint, the table constraint syntax is used. For example:

```
ALTER TABLE products ADD CHECK (name <> '');
ALTER TABLE products ADD CONSTRAINT some_name UNIQUE (product_no);
ALTER TABLE products ADD FOREIGN KEY (product_group_id) REFERENCES
 product_groups;
```

To add a not-null constraint, which cannot be written as a table constraint, use this syntax:

```
ALTER TABLE products ALTER COLUMN product_no SET NOT NULL;
```

The constraint will be checked immediately, so the table data must satisfy the constraint before it can be added.

## <span id="page-109-0"></span>**5.6.4. Removing a Constraint**

To remove a constraint you need to know its name. If you gave it a name then that's easy. Otherwise the system assigned a generated name, which you need to find out. The psql command \d tablename can be helpful here; other interfaces might also provide a way to inspect table details. Then the command is:

```
ALTER TABLE products DROP CONSTRAINT some_name;
```

As with dropping a column, you need to add CASCADE if you want to drop a constraint that something else depends on. An example is that a foreign key constraint depends on a unique or primary key constraint on the referenced column(s).

This works the same for all constraint types except not-null constraints. To drop a not null constraint use:

```
ALTER TABLE products ALTER COLUMN product_no DROP NOT NULL;
```

(Recall that not-null constraints do not have names.)

## <span id="page-109-1"></span>**5.6.5. Changing a Column's Default Value**

To set a new default for a column, use a command like:

```
ALTER TABLE products ALTER COLUMN price SET DEFAULT 7.77;
```

Note that this doesn't affect any existing rows in the table, it just changes the default for future INSERT commands.

To remove any default value, use:

```
ALTER TABLE products ALTER COLUMN price DROP DEFAULT;
```

This is effectively the same as setting the default to null. As a consequence, it is not an error to drop a default where one hadn't been defined, because the default is implicitly the null value.

## <span id="page-109-2"></span>**5.6.6. Changing a Column's Data Type**

To convert a column to a different data type, use a command like:

```
ALTER TABLE products ALTER COLUMN price TYPE numeric(10,2);
```

This will succeed only if each existing entry in the column can be converted to the new type by an implicit cast. If a more complex conversion is needed, you can add a USING clause that specifies how to compute the new values from the old.

PostgreSQL will attempt to convert the column's default value (if any) to the new type, as well as any constraints that involve the column. But these conversions might fail, or might produce surprising results. It's often best to drop any constraints on the column before altering its type, and then add back suitably modified constraints afterwards.

## <span id="page-109-3"></span>**5.6.7. Renaming a Column**

To rename a column:

ALTER TABLE products RENAME COLUMN product\_no TO product\_number;

## <span id="page-110-1"></span>**5.6.8. Renaming a Table**

To rename a table:

ALTER TABLE products RENAME TO items;

# <span id="page-110-0"></span>**5.7. Privileges**

When an object is created, it is assigned an owner. The owner is normally the role that executed the creation statement. For most kinds of objects, the initial state is that only the owner (or a superuser) can do anything with the object. To allow other roles to use it, *privileges* must be granted.

There are different kinds of privileges: SELECT, INSERT, UPDATE, DELETE, TRUNCATE, REF-ERENCES, TRIGGER, CREATE, CONNECT, TEMPORARY, EXECUTE, and USAGE. The privileges applicable to a particular object vary depending on the object's type (table, function, etc). More detail about the meanings of these privileges appears below. The following sections and chapters will also show you how these privileges are used.

The right to modify or destroy an object is inherent in being the object's owner, and cannot be granted or revoked in itself. (However, like all privileges, that right can be inherited by members of the owning role; see Section 22.3.)

An object can be assigned to a new owner with an ALTER command of the appropriate kind for the object, for example

```
ALTER TABLE table_name OWNER TO new_owner;
```

Superusers can always do this; ordinary roles can only do it if they are both the current owner of the object (or a member of the owning role) and a member of the new owning role. All object privileges of the old owner are transferred to the new owner along with the ownership.

To assign privileges, the GRANT command is used. For example, if joe is an existing role, and accounts is an existing table, the privilege to update the table can be granted with:

```
GRANT UPDATE ON accounts TO joe;
```

Writing ALL in place of a specific privilege grants all privileges that are relevant for the object type.

The special "role" name PUBLIC can be used to grant a privilege to every role on the system. Also, "group" roles can be set up to help manage privileges when there are many users of a database for details see Chapter 22.

To revoke a previously-granted privilege, use the fittingly named REVOKE command:

```
REVOKE ALL ON accounts FROM PUBLIC;
```

Ordinarily, only the object's owner (or a superuser) can grant or revoke privileges on an object. However, it is possible to grant a privilege "with grant option", which gives the recipient the right to grant it in turn to others. If the grant option is subsequently revoked then all who received the privilege from that recipient (directly or through a chain of grants) will lose the privilege. For details see the GRANT and REVOKE reference pages.

An object's owner can choose to revoke their own ordinary privileges, for example to make a table read-only for themselves as well as others. But owners are always treated as holding all grant options, so they can always re-grant their own privileges.

The available privileges are:

SELECT

Allows SELECT from any column, or specific column(s), of a table, view, materialized view, or other table-like object. Also allows use of COPY TO. This privilege is also needed to reference existing column values in UPDATE or DELETE. For sequences, this privilege also allows use of the currval function. For large objects, this privilege allows the object to be read.

INSERT

Allows INSERT of a new row into a table, view, etc. Can be granted on specific column(s), in which case only those columns may be assigned to in the INSERT command (other columns will therefore receive default values). Also allows use of COPY FROM.

UPDATE

Allows UPDATE of any column, or specific column(s), of a table, view, etc. (In practice, any nontrivial UPDATE command will require SELECT privilege as well, since it must reference table columns to determine which rows to update, and/or to compute new values for columns.) SELECT ... FOR UPDATE and SELECT ... FOR SHARE also require this privilege on at least one column, in addition to the SELECT privilege. For sequences, this privilege allows use of the nextval and setval functions. For large objects, this privilege allows writing or truncating the object.

DELETE

Allows DELETE of a row from a table, view, etc. (In practice, any nontrivial DELETE command will require SELECT privilege as well, since it must reference table columns to determine which rows to delete.)

TRUNCATE

Allows TRUNCATE on a table.

REFERENCES

Allows creation of a foreign key constraint referencing a table, or specific column(s) of a table.

TRIGGER

Allows creation of a trigger on a table, view, etc.

CREATE

For databases, allows new schemas and publications to be created within the database, and allows trusted extensions to be installed within the database.

For schemas, allows new objects to be created within the schema. To rename an existing object, you must own the object *and* have this privilege for the containing schema.

For tablespaces, allows tables, indexes, and temporary files to be created within the tablespace, and allows databases to be created that have the tablespace as their default tablespace.

Note that revoking this privilege will not alter the existence or location of existing objects.

#### CONNECT

Allows the grantee to connect to the database. This privilege is checked at connection startup (in addition to checking any restrictions imposed by pg\_hba.conf).

#### TEMPORARY

Allows temporary tables to be created while using the database.

#### EXECUTE

Allows calling a function or procedure, including use of any operators that are implemented on top of the function. This is the only type of privilege that is applicable to functions and procedures.

#### USAGE

For procedural languages, allows use of the language for the creation of functions in that language. This is the only type of privilege that is applicable to procedural languages.

For schemas, allows access to objects contained in the schema (assuming that the objects' own privilege requirements are also met). Essentially this allows the grantee to "look up" objects within the schema. Without this permission, it is still possible to see the object names, e.g., by querying system catalogs. Also, after revoking this permission, existing sessions might have statements that have previously performed this lookup, so this is not a completely secure way to prevent object access.

For sequences, allows use of the currval and nextval functions.

For types and domains, allows use of the type or domain in the creation of tables, functions, and other schema objects. (Note that this privilege does not control all "usage" of the type, such as values of the type appearing in queries. It only prevents objects from being created that depend on the type. The main purpose of this privilege is controlling which users can create dependencies on a type, which could prevent the owner from changing the type later.)

For foreign-data wrappers, allows creation of new servers using the foreign-data wrapper.

For foreign servers, allows creation of foreign tables using the server. Grantees may also create, alter, or drop their own user mappings associated with that server.

The privileges required by other commands are listed on the reference page of the respective command.

PostgreSQL grants privileges on some types of objects to PUBLIC by default when the objects are created. No privileges are granted to PUBLIC by default on tables, table columns, sequences, foreign data wrappers, foreign servers, large objects, schemas, or tablespaces. For other types of objects, the default privileges granted to PUBLIC are as follows: CONNECT and TEMPORARY (create temporary tables) privileges for databases; EXECUTE privilege for functions and procedures; and USAGE privilege for languages and data types (including domains). The object owner can, of course, REVOKE both default and expressly granted privileges. (For maximum security, issue the REVOKE in the same transaction that creates the object; then there is no window in which another user can use the object.) Also, these default privilege settings can be overridden using the ALTER DEFAULT PRIVILEGES command.

[Table 5.1](#page-112-0) shows the one-letter abbreviations that are used for these privilege types in *ACL* (Access Control List) values. You will see these letters in the output of the psql commands listed below, or when looking at ACL columns of system catalogs.

<span id="page-112-0"></span>**Table 5.1. ACL Privilege Abbreviations**

| Privilege<br>Abbreviation |            | Applicable Object Types               |  |  |  |  |
|---------------------------|------------|---------------------------------------|--|--|--|--|
| SELECT                    | r ("read") | LARGE OBJECT, SEQUENCE, TABLE (and ta |  |  |  |  |
|                           |            | ble-like objects), table column       |  |  |  |  |

| Privilege  | Abbreviation | Applicable Object Types                                                              |
|------------|--------------|--------------------------------------------------------------------------------------|
| INSERT     | a ("append") | TABLE, table column                                                                  |
| UPDATE     | w ("write")  | LARGE OBJECT, SEQUENCE, TABLE, table<br>column                                       |
| DELETE     | d            | TABLE                                                                                |
| TRUNCATE   | D            | TABLE                                                                                |
| REFERENCES | x            | TABLE, table column                                                                  |
| TRIGGER    | t            | TABLE                                                                                |
| CREATE     | C            | DATABASE, SCHEMA, TABLESPACE                                                         |
| CONNECT    | c            | DATABASE                                                                             |
| TEMPORARY  | T            | DATABASE                                                                             |
| EXECUTE    | X            | FUNCTION, PROCEDURE                                                                  |
| USAGE      | U            | DOMAIN, FOREIGN DATA WRAPPER,<br>FOREIGN SERVER, LANGUAGE, SCHEMA,<br>SEQUENCE, TYPE |

[Table 5.2](#page-113-0) summarizes the privileges available for each type of SQL object, using the abbreviations shown above. It also shows the psql command that can be used to examine privilege settings for each object type.

<span id="page-113-0"></span>**Table 5.2. Summary of Access Privileges**

| Object Type                    | All Privileges | Default PUBLIC<br>Privileges | psql Command |
|--------------------------------|----------------|------------------------------|--------------|
| DATABASE                       | CTc            | Tc                           | \l           |
| DOMAIN                         | U              | U                            | \dD+         |
| FUNCTION or PROCEDURE          | X              | X                            | \df+         |
| FOREIGN DATA WRAPPER           | U              | none                         | \dew+        |
| FOREIGN SERVER                 | U              | none                         | \des+        |
| LANGUAGE                       | U              | U                            | \dL+         |
| LARGE OBJECT                   | rw             | none                         |              |
| SCHEMA                         | UC             | none                         | \dn+         |
| SEQUENCE                       | rwU            | none                         | \dp          |
| TABLE (and table-like objects) | arwdDxt        | none                         | \dp          |
| Table column                   | arwx           | none                         | \dp          |
| TABLESPACE                     | C              | none                         | \db+         |
| TYPE                           | U              | U                            | \dT+         |

 The privileges that have been granted for a particular object are displayed as a list of aclitem entries, each having the format:

grantee=privilege-abbreviation[\*].../grantor

Each aclitem lists all the permissions of one grantee that have been granted by a particular grantor. Specific privileges are represented by one-letter abbreviations from [Table 5.1,](#page-112-0) with \* appended if the privilege was granted with grant option. For example, calvin=r\*w/hobbes specifies that the role calvin has the privilege SELECT (r) with grant option (\*) as well as the non-grantable privilege UPDATE (w), both granted by the role hobbes. If calvin also has some privileges on the same object granted by a different grantor, those would appear as a separate aclitem entry. An empty grantee field in an aclitem stands for PUBLIC.

As an example, suppose that user miriam creates table mytable and does:

```
GRANT SELECT ON mytable TO PUBLIC;
GRANT SELECT, UPDATE, INSERT ON mytable TO admin;
GRANT SELECT (col1), UPDATE (col1) ON mytable TO miriam_rw;
```

Then psql's \dp command would show:

```
=> \dp mytable
 Access privileges
 Schema | Name | Type | Access privileges | Column
 privileges | Policies
--------+---------+-------+-----------------------
+-----------------------+----------
 public | mytable | table | miriam=arwdDxt/miriam+| col1: 
 +|
 | | | =r/miriam +| miriam_rw=rw/
miriam |
 | | | admin=arw/miriam | 
 |
(1 row)
```

If the "Access privileges" column is empty for a given object, it means the object has default privileges (that is, its privileges entry in the relevant system catalog is null). Default privileges always include all privileges for the owner, and can include some privileges for PUBLIC depending on the object type, as explained above. The first GRANT or REVOKE on an object will instantiate the default privileges (producing, for example, miriam=arwdDxt/miriam) and then modify them per the specified request. Similarly, entries are shown in "Column privileges" only for columns with nondefault privileges. (Note: for this purpose, "default privileges" always means the built-in default privileges for the object's type. An object whose privileges have been affected by an ALTER DEFAULT PRIVILEGES command will always be shown with an explicit privilege entry that includes the effects of the ALTER.)

Notice that the owner's implicit grant options are not marked in the access privileges display. A \* will appear only when grant options have been explicitly granted to someone.

# <span id="page-114-0"></span>**5.8. Row Security Policies**

In addition to the SQL-standard [privilege system](#page-110-0) available through GRANT, tables can have *row security policies* that restrict, on a per-user basis, which rows can be returned by normal queries or inserted, updated, or deleted by data modification commands. This feature is also known as *Row-Level Security*. By default, tables do not have any policies, so that if a user has access privileges to a table according to the SQL privilege system, all rows within it are equally available for querying or updating.

When row security is enabled on a table (with ALTER TABLE ... ENABLE ROW LEVEL SECURI-TY), all normal access to the table for selecting rows or modifying rows must be allowed by a row security policy. (However, the table's owner is typically not subject to row security policies.) If no policy exists for the table, a default-deny policy is used, meaning that no rows are visible or can be modified. Operations that apply to the whole table, such as TRUNCATE and REFERENCES, are not subject to row security.

Row security policies can be specific to commands, or to roles, or to both. A policy can be specified to apply to ALL commands, or to SELECT, INSERT, UPDATE, or DELETE. Multiple roles can be assigned to a given policy, and normal role membership and inheritance rules apply.

To specify which rows are visible or modifiable according to a policy, an expression is required that returns a Boolean result. This expression will be evaluated for each row prior to any conditions or functions coming from the user's query. (The only exceptions to this rule are leakproof functions, which are guaranteed to not leak information; the optimizer may choose to apply such functions ahead of the row-security check.) Rows for which the expression does not return true will not be processed. Separate expressions may be specified to provide independent control over the rows which are visible and the rows which are allowed to be modified. Policy expressions are run as part of the query and with the privileges of the user running the query, although security-definer functions can be used to access data not available to the calling user.

Superusers and roles with the BYPASSRLS attribute always bypass the row security system when accessing a table. Table owners normally bypass row security as well, though a table owner can choose to be subject to row security with ALTER TABLE ... FORCE ROW LEVEL SECURITY.

Enabling and disabling row security, as well as adding policies to a table, is always the privilege of the table owner only.

Policies are created using the CREATE POLICY command, altered using the ALTER POLICY command, and dropped using the DROP POLICY command. To enable and disable row security for a given table, use the ALTER TABLE command.

Each policy has a name and multiple policies can be defined for a table. As policies are table-specific, each policy for a table must have a unique name. Different tables may have policies with the same name.

When multiple policies apply to a given query, they are combined using either OR (for permissive policies, which are the default) or using AND (for restrictive policies). This is similar to the rule that a given role has the privileges of all roles that they are a member of. Permissive vs. restrictive policies are discussed further below.

As a simple example, here is how to create a policy on the account relation to allow only members of the managers role to access rows, and only rows of their accounts:

```
CREATE TABLE accounts (manager text, company text, contact_email
 text);
ALTER TABLE accounts ENABLE ROW LEVEL SECURITY;
CREATE POLICY account_managers ON accounts TO managers
 USING (manager = current_user);
```

The policy above implicitly provides a WITH CHECK clause identical to its USING clause, so that the constraint applies both to rows selected by a command (so a manager cannot SELECT, UPDATE, or DELETE existing rows belonging to a different manager) and to rows modified by a command (so rows belonging to a different manager cannot be created via INSERT or UPDATE).

If no role is specified, or the special user name PUBLIC is used, then the policy applies to all users on the system. To allow all users to access only their own row in a users table, a simple policy can be used:

```
CREATE POLICY user_policy ON users
 USING (user_name = current_user);
```

This works similarly to the previous example.

To use a different policy for rows that are being added to the table compared to those rows that are visible, multiple policies can be combined. This pair of policies would allow all users to view all rows in the users table, but only modify their own:

```
CREATE POLICY user_sel_policy ON users
 FOR SELECT
 USING (true);
CREATE POLICY user_mod_policy ON users
 USING (user_name = current_user);
```

In a SELECT command, these two policies are combined using OR, with the net effect being that all rows can be selected. In other command types, only the second policy applies, so that the effects are the same as before.

Row security can also be disabled with the ALTER TABLE command. Disabling row security does not remove any policies that are defined on the table; they are simply ignored. Then all rows in the table are visible and modifiable, subject to the standard SQL privileges system.

Below is a larger example of how this feature can be used in production environments. The table passwd emulates a Unix password file:

```
-- Simple passwd-file based example
CREATE TABLE passwd (
 user_name text UNIQUE NOT NULL,
 pwhash text,
 uid int PRIMARY KEY,
 gid int NOT NULL,
 real_name text NOT NULL,
 home_phone text,
 extra_info text,
 home_dir text NOT NULL,
 shell text NOT NULL
);
CREATE ROLE admin; -- Administrator
CREATE ROLE bob; -- Normal user
CREATE ROLE alice; -- Normal user
-- Populate the table
INSERT INTO passwd VALUES
 ('admin','xxx',0,0,'Admin','111-222-3333',null,'/root','/bin/
dash');
INSERT INTO passwd VALUES
 ('bob','xxx',1,1,'Bob','123-456-7890',null,'/home/bob','/bin/
zsh');
INSERT INTO passwd VALUES
 ('alice','xxx',2,1,'Alice','098-765-4321',null,'/home/alice','/
bin/zsh');
-- Be sure to enable row-level security on the table
ALTER TABLE passwd ENABLE ROW LEVEL SECURITY;
-- Create policies
-- Administrator can see all rows and add any rows
CREATE POLICY admin_all ON passwd TO admin USING (true) WITH CHECK
 (true);
-- Normal users can view all rows
CREATE POLICY all_view ON passwd FOR SELECT USING (true);
-- Normal users can update their own records, but
-- limit which shells a normal user is allowed to set
CREATE POLICY user_mod ON passwd FOR UPDATE
```

```
 USING (current_user = user_name)
 WITH CHECK (
 current_user = user_name AND
 shell IN ('/bin/bash','/bin/sh','/bin/dash','/bin/zsh','/bin/
tcsh')
 );
-- Allow admin all normal rights
GRANT SELECT, INSERT, UPDATE, DELETE ON passwd TO admin;
-- Users only get select access on public columns
GRANT SELECT
 (user_name, uid, gid, real_name, home_phone, extra_info,
 home_dir, shell)
 ON passwd TO public;
-- Allow users to update certain columns
GRANT UPDATE
 (pwhash, real_name, home_phone, extra_info, shell)
 ON passwd TO public;
```

As with any security settings, it's important to test and ensure that the system is behaving as expected. Using the example above, this demonstrates that the permission system is working properly.

```
-- admin can view all rows and fields
postgres=> set role admin;
SET
postgres=> table passwd;
 user_name | pwhash | uid | gid | real_name | home_phone |
 extra_info | home_dir | shell
-----------+--------+-----+-----+-----------+--------------
+------------+-------------+-----------
 admin | xxx | 0 | 0 | Admin | 111-222-3333 | 
 | /root | /bin/dash
 bob | xxx | 1 | 1 | Bob | 123-456-7890 | 
 | /home/bob | /bin/zsh
 alice | xxx | 2 | 1 | Alice | 098-765-4321 | 
 | /home/alice | /bin/zsh
(3 rows)
-- Test what Alice is able to do
postgres=> set role alice;
SET
postgres=> table passwd;
ERROR: permission denied for table passwd
postgres=> select
 user_name,real_name,home_phone,extra_info,home_dir,shell from
 passwd;
 user_name | real_name | home_phone | extra_info | home_dir | 
 shell
-----------+-----------+--------------+------------+-------------
+-----------
 admin | Admin | 111-222-3333 | | /root 
 | /bin/dash
 bob | Bob | 123-456-7890 | | /home/bob 
 | /bin/zsh
 alice | Alice | 098-765-4321 | | /home/alice
 | /bin/zsh
(3 rows)
```

```
postgres=> update passwd set user_name = 'joe';
ERROR: permission denied for table passwd
-- Alice is allowed to change her own real_name, but no others
postgres=> update passwd set real_name = 'Alice Doe';
UPDATE 1
postgres=> update passwd set real_name = 'John Doe' where user_name
 = 'admin';
UPDATE 0
postgres=> update passwd set shell = '/bin/xx';
ERROR: new row violates WITH CHECK OPTION for "passwd"
postgres=> delete from passwd;
ERROR: permission denied for table passwd
postgres=> insert into passwd (user_name) values ('xxx');
ERROR: permission denied for table passwd
-- Alice can change her own password; RLS silently prevents
 updating other rows
postgres=> update passwd set pwhash = 'abc';
UPDATE 1
```

All of the policies constructed thus far have been permissive policies, meaning that when multiple policies are applied they are combined using the "OR" Boolean operator. While permissive policies can be constructed to only allow access to rows in the intended cases, it can be simpler to combine permissive policies with restrictive policies (which the records must pass and which are combined using the "AND" Boolean operator). Building on the example above, we add a restrictive policy to require the administrator to be connected over a local Unix socket to access the records of the passwd table:

```
CREATE POLICY admin_local_only ON passwd AS RESTRICTIVE TO admin
 USING (pg_catalog.inet_client_addr() IS NULL);
```

We can then see that an administrator connecting over a network will not see any records, due to the restrictive policy:

```
=> SELECT current_user;
 current_user 
--------------
 admin
(1 row)
=> select inet_client_addr();
 inet_client_addr 
------------------
 127.0.0.1
(1 row)
=> TABLE passwd;
 user_name | pwhash | uid | gid | real_name | home_phone |
 extra_info | home_dir | shell
-----------+--------+-----+-----+-----------+------------
+------------+----------+-------
(0 rows)
=> UPDATE passwd set pwhash = NULL;
UPDATE 0
```

Referential integrity checks, such as unique or primary key constraints and foreign key references, always bypass row security to ensure that data integrity is maintained. Care must be taken when developing schemas and row level policies to avoid "covert channel" leaks of information through such referential integrity checks.

In some contexts it is important to be sure that row security is not being applied. For example, when taking a backup, it could be disastrous if row security silently caused some rows to be omitted from the backup. In such a situation, you can set the row\_security configuration parameter to off. This does not in itself bypass row security; what it does is throw an error if any query's results would get filtered by a policy. The reason for the error can then be investigated and fixed.

In the examples above, the policy expressions consider only the current values in the row to be accessed or updated. This is the simplest and best-performing case; when possible, it's best to design row security applications to work this way. If it is necessary to consult other rows or other tables to make a policy decision, that can be accomplished using sub-SELECTs, or functions that contain SELECTs, in the policy expressions. Be aware however that such accesses can create race conditions that could allow information leakage if care is not taken. As an example, consider the following table design:

```
-- definition of privilege groups
CREATE TABLE groups (group_id int PRIMARY KEY,
 group_name text NOT NULL);
INSERT INTO groups VALUES
 (1, 'low'),
 (2, 'medium'),
 (5, 'high');
GRANT ALL ON groups TO alice; -- alice is the administrator
GRANT SELECT ON groups TO public;
-- definition of users' privilege levels
CREATE TABLE users (user_name text PRIMARY KEY,
 group_id int NOT NULL REFERENCES groups);
INSERT INTO users VALUES
 ('alice', 5),
 ('bob', 2),
 ('mallory', 2);
GRANT ALL ON users TO alice;
GRANT SELECT ON users TO public;
-- table holding the information to be protected
CREATE TABLE information (info text,
 group_id int NOT NULL REFERENCES groups);
INSERT INTO information VALUES
 ('barely secret', 1),
 ('slightly secret', 2),
 ('very secret', 5);
ALTER TABLE information ENABLE ROW LEVEL SECURITY;
-- a row should be visible to/updatable by users whose security
 group_id is
-- greater than or equal to the row's group_id
CREATE POLICY fp_s ON information FOR SELECT
```

```
 USING (group_id <= (SELECT group_id FROM users WHERE user_name =
 current_user));
CREATE POLICY fp_u ON information FOR UPDATE
 USING (group_id <= (SELECT group_id FROM users WHERE user_name =
 current_user));
-- we rely only on RLS to protect the information table
GRANT ALL ON information TO public;
```

Now suppose that alice wishes to change the "slightly secret" information, but decides that mallory should not be trusted with the new content of that row, so she does:

```
BEGIN;
UPDATE users SET group_id = 1 WHERE user_name = 'mallory';
UPDATE information SET info = 'secret from mallory' WHERE group_id
 = 2;
COMMIT;
```

That looks safe; there is no window wherein mallory should be able to see the "secret from mallory" string. However, there is a race condition here. If mallory is concurrently doing, say,

```
SELECT * FROM information WHERE group_id = 2 FOR UPDATE;
```

and her transaction is in READ COMMITTED mode, it is possible for her to see "secret from mallory". That happens if her transaction reaches the information row just after alice's does. It blocks waiting for alice's transaction to commit, then fetches the updated row contents thanks to the FOR UPDATE clause. However, it does *not* fetch an updated row for the implicit SELECT from users, because that sub-SELECT did not have FOR UPDATE; instead the users row is read with the snapshot taken at the start of the query. Therefore, the policy expression tests the old value of mallory's privilege level and allows her to see the updated row.

There are several ways around this problem. One simple answer is to use SELECT ... FOR SHARE in sub-SELECTs in row security policies. However, that requires granting UPDATE privilege on the referenced table (here users) to the affected users, which might be undesirable. (But another row security policy could be applied to prevent them from actually exercising that privilege; or the sub-SELECT could be embedded into a security definer function.) Also, heavy concurrent use of row share locks on the referenced table could pose a performance problem, especially if updates of it are frequent. Another solution, practical if updates of the referenced table are infrequent, is to take an ACCESS EXCLUSIVE lock on the referenced table when updating it, so that no concurrent transactions could be examining old row values. Or one could just wait for all concurrent transactions to end after committing an update of the referenced table and before making changes that rely on the new security situation.

For additional details see CREATE POLICY and ALTER TABLE.

# <span id="page-120-0"></span>**5.9. Schemas**

A PostgreSQL database cluster contains one or more named databases. Roles and a few other object types are shared across the entire cluster. A client connection to the server can only access data in a single database, the one specified in the connection request.

#### **Note**

Users of a cluster do not necessarily have the privilege to access every database in the cluster. Sharing of role names means that there cannot be different roles named, say, joe in two databases in the same cluster; but the system can be configured to allow joe access to only some of the databases.

A database contains one or more named *schemas*, which in turn contain tables. Schemas also contain other kinds of named objects, including data types, functions, and operators. The same object name can be used in different schemas without conflict; for example, both schema1 and myschema can contain tables named mytable. Unlike databases, schemas are not rigidly separated: a user can access objects in any of the schemas in the database they are connected to, if they have privileges to do so.

There are several reasons why one might want to use schemas:

- To allow many users to use one database without interfering with each other.
- To organize database objects into logical groups to make them more manageable.
- Third-party applications can be put into separate schemas so they do not collide with the names of other objects.

Schemas are analogous to directories at the operating system level, except that schemas cannot be nested.

## <span id="page-121-0"></span>**5.9.1. Creating a Schema**

To create a schema, use the CREATE SCHEMA command. Give the schema a name of your choice. For example:

```
CREATE SCHEMA myschema;
```

To create or access objects in a schema, write a *qualified name* consisting of the schema name and table name separated by a dot:

```
schema.table
```

This works anywhere a table name is expected, including the table modification commands and the data access commands discussed in the following chapters. (For brevity we will speak of tables only, but the same ideas apply to other kinds of named objects, such as types and functions.)

Actually, the even more general syntax

```
database.schema.table
```

can be used too, but at present this is just for pro forma compliance with the SQL standard. If you write a database name, it must be the same as the database you are connected to.

So to create a table in the new schema, use:

```
CREATE TABLE myschema.mytable (
 ...
);
```

To drop a schema if it's empty (all objects in it have been dropped), use:

```
DROP SCHEMA myschema;
```

To drop a schema including all contained objects, use:

```
DROP SCHEMA myschema CASCADE;
```

See [Section 5.14](#page-142-2) for a description of the general mechanism behind this.

Often you will want to create a schema owned by someone else (since this is one of the ways to restrict the activities of your users to well-defined namespaces). The syntax for that is:

```
CREATE SCHEMA schema_name AUTHORIZATION user_name;
```

You can even omit the schema name, in which case the schema name will be the same as the user name. See [Section 5.9.6](#page-124-1) for how this can be useful.

Schema names beginning with pg\_ are reserved for system purposes and cannot be created by users.

## <span id="page-122-0"></span>**5.9.2. The Public Schema**

In the previous sections we created tables without specifying any schema names. By default such tables (and other objects) are automatically put into a schema named "public". Every new database contains such a schema. Thus, the following are equivalent:

```
CREATE TABLE products ( ... );
and:
CREATE TABLE public.products ( ... );
```

## <span id="page-122-1"></span>**5.9.3. The Schema Search Path**

Qualified names are tedious to write, and it's often best not to wire a particular schema name into applications anyway. Therefore tables are often referred to by *unqualified names*, which consist of just the table name. The system determines which table is meant by following a *search path*, which is a list of schemas to look in. The first matching table in the search path is taken to be the one wanted. If there is no match in the search path, an error is reported, even if matching table names exist in other schemas in the database.

The ability to create like-named objects in different schemas complicates writing a query that references precisely the same objects every time. It also opens up the potential for users to change the behavior of other users' queries, maliciously or accidentally. Due to the prevalence of unqualified names in queries and their use in PostgreSQL internals, adding a schema to search\_path effectively trusts all users having CREATE privilege on that schema. When you run an ordinary query, a malicious user able to create objects in a schema of your search path can take control and execute arbitrary SQL functions as though you executed them.

The first schema named in the search path is called the current schema. Aside from being the first schema searched, it is also the schema in which new tables will be created if the CREATE TABLE command does not specify a schema name.

To show the current search path, use the following command:

```
SHOW search_path;
```

In the default setup this returns:

```
 search_path
--------------
 "$user", public
```

The first element specifies that a schema with the same name as the current user is to be searched. If no such schema exists, the entry is ignored. The second element refers to the public schema that we have seen already.

The first schema in the search path that exists is the default location for creating new objects. That is the reason that by default objects are created in the public schema. When objects are referenced in any other context without schema qualification (table modification, data modification, or query commands) the search path is traversed until a matching object is found. Therefore, in the default configuration, any unqualified access again can only refer to the public schema.

To put our new schema in the path, we use:

```
SET search_path TO myschema,public;
```

(We omit the \$user here because we have no immediate need for it.) And then we can access the table without schema qualification:

```
DROP TABLE mytable;
```

Also, since myschema is the first element in the path, new objects would by default be created in it.

We could also have written:

```
SET search_path TO myschema;
```

Then we no longer have access to the public schema without explicit qualification. There is nothing special about the public schema except that it exists by default. It can be dropped, too.

See also Section 9.26 for other ways to manipulate the schema search path.

The search path works in the same way for data type names, function names, and operator names as it does for table names. Data type and function names can be qualified in exactly the same way as table names. If you need to write a qualified operator name in an expression, there is a special provision: you must write

```
OPERATOR(schema.operator)
```

This is needed to avoid syntactic ambiguity. An example is:

```
SELECT 3 OPERATOR(pg_catalog.+) 4;
```

In practice one usually relies on the search path for operators, so as not to have to write anything so ugly as that.

## <span id="page-123-0"></span>**5.9.4. Schemas and Privileges**

By default, users cannot access any objects in schemas they do not own. To allow that, the owner of the schema must grant the USAGE privilege on the schema. To allow users to make use of the objects in the schema, additional privileges might need to be granted, as appropriate for the object.

A user can also be allowed to create objects in someone else's schema. To allow that, the CREATE privilege on the schema needs to be granted. Note that by default, everyone has CREATE and USAGE privileges on the schema public. This allows all users that are able to connect to a given database to create objects in its public schema. Some [usage patterns](#page-124-1) call for revoking that privilege:

```
REVOKE CREATE ON SCHEMA public FROM PUBLIC;
```

(The first "public" is the schema, the second "public" means "every user". In the first sense it is an identifier, in the second sense it is a key word, hence the different capitalization; recall the guidelines from [Section 4.1.1](#page-70-2).)

## <span id="page-124-0"></span>**5.9.5. The System Catalog Schema**

In addition to public and user-created schemas, each database contains a pg\_catalog schema, which contains the system tables and all the built-in data types, functions, and operators. pg\_catalog is always effectively part of the search path. If it is not named explicitly in the path then it is implicitly searched *before* searching the path's schemas. This ensures that built-in names will always be findable. However, you can explicitly place pg\_catalog at the end of your search path if you prefer to have user-defined names override built-in names.

Since system table names begin with pg\_, it is best to avoid such names to ensure that you won't suffer a conflict if some future version defines a system table named the same as your table. (With the default search path, an unqualified reference to your table name would then be resolved as the system table instead.) System tables will continue to follow the convention of having names beginning with pg\_, so that they will not conflict with unqualified user-table names so long as users avoid the pg\_ prefix.

## <span id="page-124-1"></span>**5.9.6. Usage Patterns**

Schemas can be used to organize your data in many ways. A *secure schema usage pattern* prevents untrusted users from changing the behavior of other users' queries. When a database does not use a secure schema usage pattern, users wishing to securely query that database would take protective action at the beginning of each session. Specifically, they would begin each session by setting search\_path to the empty string or otherwise removing non-superuser-writable schemas from search\_path. There are a few usage patterns easily supported by the default configuration:

- Constrain ordinary users to user-private schemas. To implement this, issue REVOKE CREATE ON SCHEMA public FROM PUBLIC, and create a schema for each user with the same name as that user. Recall that the default search path starts with \$user, which resolves to the user name. Therefore, if each user has a separate schema, they access their own schemas by default. After adopting this pattern in a database where untrusted users had already logged in, consider auditing the public schema for objects named like objects in schema pg\_catalog. This pattern is a secure schema usage pattern unless an untrusted user is the database owner or holds the CREATEROLE privilege, in which case no secure schema usage pattern exists.
- Remove the public schema from the default search path, by modifying postgresql.conf or by issuing ALTER ROLE ALL SET search\_path = "\$user". Everyone retains the ability to create objects in the public schema, but only qualified names will choose those objects. While qualified table references are fine, calls to functions in the public schema will be unsafe or unreliable. If you create functions or extensions in the public schema, use the first pattern instead. Otherwise, like the first pattern, this is secure unless an untrusted user is the database owner or holds the CREATEROLE privilege.
- Keep the default. All users access the public schema implicitly. This simulates the situation where schemas are not available at all, giving a smooth transition from the non-schema-aware world. However, this is never a secure pattern. It is acceptable only when the database has a single user or a few mutually-trusting users.

For any pattern, to install shared applications (tables to be used by everyone, additional functions provided by third parties, etc.), put them into separate schemas. Remember to grant appropriate privileges to allow the other users to access them. Users can then refer to these additional objects by qualifying the names with a schema name, or they can put the additional schemas into their search path, as they choose.

## <span id="page-125-1"></span>**5.9.7. Portability**

In the SQL standard, the notion of objects in the same schema being owned by different users does not exist. Moreover, some implementations do not allow you to create schemas that have a different name than their owner. In fact, the concepts of schema and user are nearly equivalent in a database system that implements only the basic schema support specified in the standard. Therefore, many users consider qualified names to really consist of user\_name.table\_name. This is how PostgreSQL will effectively behave if you create a per-user schema for every user.

Also, there is no concept of a public schema in the SQL standard. For maximum conformance to the standard, you should not use the public schema.

Of course, some SQL database systems might not implement schemas at all, or provide namespace support by allowing (possibly limited) cross-database access. If you need to work with those systems, then maximum portability would be achieved by not using schemas at all.

# <span id="page-125-0"></span>**5.10. Inheritance**

PostgreSQL implements table inheritance, which can be a useful tool for database designers. (SQL:1999 and later define a type inheritance feature, which differs in many respects from the features described here.)

Let's start with an example: suppose we are trying to build a data model for cities. Each state has many cities, but only one capital. We want to be able to quickly retrieve the capital city for any particular state. This can be done by creating two tables, one for state capitals and one for cities that are not capitals. However, what happens when we want to ask for data about a city, regardless of whether it is a capital or not? The inheritance feature can help to resolve this problem. We define the capitals table so that it inherits from cities:

```
CREATE TABLE cities (
 name text,
 population float,
 elevation int -- in feet
);
CREATE TABLE capitals (
 state char(2)
) INHERITS (cities);
```

In this case, the capitals table *inherits* all the columns of its parent table, cities. State capitals also have an extra column, state, that shows their state.

In PostgreSQL, a table can inherit from zero or more other tables, and a query can reference either all rows of a table or all rows of a table plus all of its descendant tables. The latter behavior is the default. For example, the following query finds the names of all cities, including state capitals, that are located at an elevation over 500 feet:

```
SELECT name, elevation
 FROM cities
 WHERE elevation > 500;
```

Given the sample data from the PostgreSQL tutorial (see [Section 2.1\)](#page-44-1), this returns:

| name      |  | elevation |
|-----------|--|-----------|
| +         |  |           |
| Las Vegas |  | 2174      |
| Mariposa  |  | 1953      |
| Madison   |  | 845       |

On the other hand, the following query finds all the cities that are not state capitals and are situated at an elevation over 500 feet:

```
SELECT name, elevation
 FROM ONLY cities
 WHERE elevation > 500;
 name | elevation
-----------+-----------
 Las Vegas | 2174
 Mariposa | 1953
```

Here the ONLY keyword indicates that the query should apply only to cities, and not any tables below cities in the inheritance hierarchy. Many of the commands that we have already discussed — SELECT, UPDATE and DELETE — support the ONLY keyword.

You can also write the table name with a trailing \* to explicitly specify that descendant tables are included:

```
SELECT name, elevation
 FROM cities*
 WHERE elevation > 500;
```

Writing \* is not necessary, since this behavior is always the default. However, this syntax is still supported for compatibility with older releases where the default could be changed.

In some cases you might wish to know which table a particular row originated from. There is a system column called tableoid in each table which can tell you the originating table:

```
SELECT c.tableoid, c.name, c.elevation
FROM cities c
WHERE c.elevation > 500;
```

which returns:

| tableoid | name               |  | elevation  |
|----------|--------------------|--|------------|
|          | 139793   Las Vegas |  | ++<br>2174 |
|          | 139793   Mariposa  |  | 1953       |
|          | 139798   Madison   |  | 845        |

(If you try to reproduce this example, you will probably get different numeric OIDs.) By doing a join with pg\_class you can see the actual table names:

```
SELECT p.relname, c.name, c.elevation
FROM cities c, pg_class p
WHERE c.elevation > 500 AND c.tableoid = p.oid;
```

which returns:

| relname            |  | name      |  | elevation |
|--------------------|--|-----------|--|-----------|
|                    |  |           |  | ++        |
| cities             |  | Las Vegas |  | 2174      |
| cities             |  | Mariposa  |  | 1953      |
| capitals   Madison |  |           |  | 845       |

Another way to get the same effect is to use the regclass alias type, which will print the table OID symbolically:

```
SELECT c.tableoid::regclass, c.name, c.elevation
FROM cities c
WHERE c.elevation > 500;
```

Inheritance does not automatically propagate data from INSERT or COPY commands to other tables in the inheritance hierarchy. In our example, the following INSERT statement will fail:

```
INSERT INTO cities (name, population, elevation, state)
VALUES ('Albany', NULL, NULL, 'NY');
```

We might hope that the data would somehow be routed to the capitals table, but this does not happen: INSERT always inserts into exactly the table specified. In some cases it is possible to redirect the insertion using a rule (see Chapter 41). However that does not help for the above case because the cities table does not contain the column state, and so the command will be rejected before the rule can be applied.

All check constraints and not-null constraints on a parent table are automatically inherited by its children, unless explicitly specified otherwise with NO INHERIT clauses. Other types of constraints (unique, primary key, and foreign key constraints) are not inherited.

A table can inherit from more than one parent table, in which case it has the union of the columns defined by the parent tables. Any columns declared in the child table's definition are added to these. If the same column name appears in multiple parent tables, or in both a parent table and the child's definition, then these columns are "merged" so that there is only one such column in the child table. To be merged, columns must have the same data types, else an error is raised. Inheritable check constraints and not-null constraints are merged in a similar fashion. Thus, for example, a merged column will be marked not-null if any one of the column definitions it came from is marked not-null. Check constraints are merged if they have the same name, and the merge will fail if their conditions are different.

Table inheritance is typically established when the child table is created, using the INHERITS clause of the CREATE TABLE statement. Alternatively, a table which is already defined in a compatible way can have a new parent relationship added, using the INHERIT variant of ALTER TABLE. To do this the new child table must already include columns with the same names and types as the columns of the parent. It must also include check constraints with the same names and check expressions as those of the parent. Similarly an inheritance link can be removed from a child using the NO INHERIT variant of ALTER TABLE. Dynamically adding and removing inheritance links like this can be useful when the inheritance relationship is being used for table partitioning (see [Section 5.11\)](#page-128-0).

One convenient way to create a compatible table that will later be made a new child is to use the LIKE clause in CREATE TABLE. This creates a new table with the same columns as the source table. If there are any CHECK constraints defined on the source table, the INCLUDING CONSTRAINTS option to LIKE should be specified, as the new child must have constraints matching the parent to be considered compatible.

A parent table cannot be dropped while any of its children remain. Neither can columns or check constraints of child tables be dropped or altered if they are inherited from any parent tables. If you wish to remove a table and all of its descendants, one easy way is to drop the parent table with the CASCADE option (see [Section 5.14](#page-142-2)).

ALTER TABLE will propagate any changes in column data definitions and check constraints down the inheritance hierarchy. Again, dropping columns that are depended on by other tables is only possible when using the CASCADE option. ALTER TABLE follows the same rules for duplicate column merging and rejection that apply during CREATE TABLE.

Inherited queries perform access permission checks on the parent table only. Thus, for example, granting UPDATE permission on the cities table implies permission to update rows in the capitals table as well, when they are accessed through cities. This preserves the appearance that the data is (also) in the parent table. But the capitals table could not be updated directly without an additional grant. In a similar way, the parent table's row security policies (see [Section 5.8](#page-114-0)) are applied to rows coming from child tables during an inherited query. A child table's policies, if any, are applied only when it is the table explicitly named in the query; and in that case, any policies attached to its parent(s) are ignored.

Foreign tables (see [Section 5.12\)](#page-142-0) can also be part of inheritance hierarchies, either as parent or child tables, just as regular tables can be. If a foreign table is part of an inheritance hierarchy then any operations not supported by the foreign table are not supported on the whole hierarchy either.

## <span id="page-128-1"></span>**5.10.1. Caveats**

Note that not all SQL commands are able to work on inheritance hierarchies. Commands that are used for data querying, data modification, or schema modification (e.g., SELECT, UPDATE, DELETE, most variants of ALTER TABLE, but not INSERT or ALTER TABLE ... RENAME) typically default to including child tables and support the ONLY notation to exclude them. Commands that do database maintenance and tuning (e.g., REINDEX, VACUUM) typically only work on individual, physical tables and do not support recursing over inheritance hierarchies. The respective behavior of each individual command is documented in its reference page (SQL Commands).

A serious limitation of the inheritance feature is that indexes (including unique constraints) and foreign key constraints only apply to single tables, not to their inheritance children. This is true on both the referencing and referenced sides of a foreign key constraint. Thus, in the terms of the above example:

- If we declared cities.name to be UNIQUE or a PRIMARY KEY, this would not stop the capitals table from having rows with names duplicating rows in cities. And those duplicate rows would by default show up in queries from cities. In fact, by default capitals would have no unique constraint at all, and so could contain multiple rows with the same name. You could add a unique constraint to capitals, but this would not prevent duplication compared to cities.
- Similarly, if we were to specify that cities.name REFERENCES some other table, this constraint would not automatically propagate to capitals. In this case you could work around it by manually adding the same REFERENCES constraint to capitals.
- Specifying that another table's column REFERENCES cities(name) would allow the other table to contain city names, but not capital names. There is no good workaround for this case.

Some functionality not implemented for inheritance hierarchies is implemented for declarative partitioning. Considerable care is needed in deciding whether partitioning with legacy inheritance is useful for your application.

# <span id="page-128-0"></span>**5.11. Table Partitioning**

PostgreSQL supports basic table partitioning. This section describes why and how to implement partitioning as part of your database design.

## <span id="page-128-2"></span>**5.11.1. Overview**

Partitioning refers to splitting what is logically one large table into smaller physical pieces. Partitioning can provide several benefits:

- Query performance can be improved dramatically in certain situations, particularly when most of the heavily accessed rows of the table are in a single partition or a small number of partitions. Partitioning effectively substitutes for the upper tree levels of indexes, making it more likely that the heavily-used parts of the indexes fit in memory.
- When queries or updates access a large percentage of a single partition, performance can be improved by using a sequential scan of that partition instead of using an index, which would require random-access reads scattered across the whole table.
- Bulk loads and deletes can be accomplished by adding or removing partitions, if the usage pattern is accounted for in the partitioning design. Dropping an individual partition using DROP TABLE, or doing ALTER TABLE DETACH PARTITION, is far faster than a bulk operation. These commands also entirely avoid the VACUUM overhead caused by a bulk DELETE.
- Seldom-used data can be migrated to cheaper and slower storage media.

These benefits will normally be worthwhile only when a table would otherwise be very large. The exact point at which a table will benefit from partitioning depends on the application, although a rule of thumb is that the size of the table should exceed the physical memory of the database server.

PostgreSQL offers built-in support for the following forms of partitioning:

#### Range Partitioning

The table is partitioned into "ranges" defined by a key column or set of columns, with no overlap between the ranges of values assigned to different partitions. For example, one might partition by date ranges, or by ranges of identifiers for particular business objects. Each range's bounds are understood as being inclusive at the lower end and exclusive at the upper end. For example, if one partition's range is from 1 to 10, and the next one's range is from 10 to 20, then value 10 belongs to the second partition not the first.

#### List Partitioning

The table is partitioned by explicitly listing which key value(s) appear in each partition.

#### Hash Partitioning

The table is partitioned by specifying a modulus and a remainder for each partition. Each partition will hold the rows for which the hash value of the partition key divided by the specified modulus will produce the specified remainder.

If your application needs to use other forms of partitioning not listed above, alternative methods such as inheritance and UNION ALL views can be used instead. Such methods offer flexibility but do not have some of the performance benefits of built-in declarative partitioning.

## <span id="page-129-0"></span>**5.11.2. Declarative Partitioning**

PostgreSQL allows you to declare that a table is divided into partitions. The table that is divided is referred to as a *partitioned table*. The declaration includes the *partitioning method* as described above, plus a list of columns or expressions to be used as the *partition key*.

The partitioned table itself is a "virtual" table having no storage of its own. Instead, the storage belongs to *partitions*, which are otherwise-ordinary tables associated with the partitioned table. Each partition stores a subset of the data as defined by its *partition bounds*. All rows inserted into a partitioned table will be routed to the appropriate one of the partitions based on the values of the partition key column(s). Updating the partition key of a row will cause it to be moved into a different partition if it no longer satisfies the partition bounds of its original partition.

Partitions may themselves be defined as partitioned tables, resulting in *sub-partitioning*. Although all partitions must have the same columns as their partitioned parent, partitions may have their own indexes, constraints and default values, distinct from those of other partitions. See CREATE TABLE for more details on creating partitioned tables and partitions.

It is not possible to turn a regular table into a partitioned table or vice versa. However, it is possible to add an existing regular or partitioned table as a partition of a partitioned table, or remove a partition from a partitioned table turning it into a standalone table; this can simplify and speed up many maintenance processes. See ALTER TABLE to learn more about the ATTACH PARTITION and DETACH PARTITION sub-commands.

Partitions can also be [foreign tables,](#page-142-0) although considerable care is needed because it is then the user's responsibility that the contents of the foreign table satisfy the partitioning rule. There are some other restrictions as well. See CREATE FOREIGN TABLE for more information.

#### **5.11.2.1. Example**

Suppose we are constructing a database for a large ice cream company. The company measures peak temperatures every day as well as ice cream sales in each region. Conceptually, we want a table like:

```
CREATE TABLE measurement (
 city_id int not null,
 logdate date not null,
 peaktemp int,
 unitsales int
);
```

We know that most queries will access just the last week's, month's or quarter's data, since the main use of this table will be to prepare online reports for management. To reduce the amount of old data that needs to be stored, we decide to keep only the most recent 3 years worth of data. At the beginning of each month we will remove the oldest month's data. In this situation we can use partitioning to help us meet all of our different requirements for the measurements table.

To use declarative partitioning in this case, use the following steps:

1. Create the measurement table as a partitioned table by specifying the PARTITION BY clause, which includes the partitioning method (RANGE in this case) and the list of column(s) to use as the partition key.

```
CREATE TABLE measurement (
 city_id int not null,
 logdate date not null,
 peaktemp int,
 unitsales int
) PARTITION BY RANGE (logdate);
```

2. Create partitions. Each partition's definition must specify bounds that correspond to the partitioning method and partition key of the parent. Note that specifying bounds such that the new partition's values would overlap with those in one or more existing partitions will cause an error.

Partitions thus created are in every way normal PostgreSQL tables (or, possibly, foreign tables). It is possible to specify a tablespace and storage parameters for each partition separately.

For our example, each partition should hold one month's worth of data, to match the requirement of deleting one month's data at a time. So the commands might look like:

```
CREATE TABLE measurement_y2006m02 PARTITION OF measurement
 FOR VALUES FROM ('2006-02-01') TO ('2006-03-01');
CREATE TABLE measurement_y2006m03 PARTITION OF measurement
```

```
 FOR VALUES FROM ('2006-03-01') TO ('2006-04-01');
...
CREATE TABLE measurement_y2007m11 PARTITION OF measurement
 FOR VALUES FROM ('2007-11-01') TO ('2007-12-01');
CREATE TABLE measurement_y2007m12 PARTITION OF measurement
 FOR VALUES FROM ('2007-12-01') TO ('2008-01-01')
 TABLESPACE fasttablespace;
CREATE TABLE measurement_y2008m01 PARTITION OF measurement
 FOR VALUES FROM ('2008-01-01') TO ('2008-02-01')
 WITH (parallel_workers = 4)
 TABLESPACE fasttablespace;
```

(Recall that adjacent partitions can share a bound value, since range upper bounds are treated as exclusive bounds.)

If you wish to implement sub-partitioning, again specify the PARTITION BY clause in the commands used to create individual partitions, for example:

```
CREATE TABLE measurement_y2006m02 PARTITION OF measurement
 FOR VALUES FROM ('2006-02-01') TO ('2006-03-01')
 PARTITION BY RANGE (peaktemp);
```

After creating partitions of measurement\_y2006m02, any data inserted into measurement that is mapped to measurement\_y2006m02 (or data that is directly inserted into measurement\_y2006m02, which is allowed provided its partition constraint is satisfied) will be further redirected to one of its partitions based on the peaktemp column. The partition key specified may overlap with the parent's partition key, although care should be taken when specifying the bounds of a sub-partition such that the set of data it accepts constitutes a subset of what the partition's own bounds allow; the system does not try to check whether that's really the case.

Inserting data into the parent table that does not map to one of the existing partitions will cause an error; an appropriate partition must be added manually.

It is not necessary to manually create table constraints describing the partition boundary conditions for partitions. Such constraints will be created automatically.

3. Create an index on the key column(s), as well as any other indexes you might want, on the partitioned table. (The key index is not strictly necessary, but in most scenarios it is helpful.) This automatically creates a matching index on each partition, and any partitions you create or attach later will also have such an index. An index or unique constraint declared on a partitioned table is "virtual" in the same way that the partitioned table is: the actual data is in child indexes on the individual partition tables.

```
CREATE INDEX ON measurement (logdate);
```

4. Ensure that the enable\_partition\_pruning configuration parameter is not disabled in postgresql.conf. If it is, queries will not be optimized as desired.

In the above example we would be creating a new partition each month, so it might be wise to write a script that generates the required DDL automatically.

#### **5.11.2.2. Partition Maintenance**

Normally the set of partitions established when initially defining the table is not intended to remain static. It is common to want to remove partitions holding old data and periodically add new partitions for new data. One of the most important advantages of partitioning is precisely that it allows this otherwise painful task to be executed nearly instantaneously by manipulating the partition structure, rather than physically moving large amounts of data around.

The simplest option for removing old data is to drop the partition that is no longer necessary:

```
DROP TABLE measurement_y2006m02;
```

This can very quickly delete millions of records because it doesn't have to individually delete every record. Note however that the above command requires taking an ACCESS EXCLUSIVE lock on the parent table.

Another option that is often preferable is to remove the partition from the partitioned table but retain access to it as a table in its own right. This has two forms:

```
ALTER TABLE measurement DETACH PARTITION measurement_y2006m02;
ALTER TABLE measurement DETACH PARTITION measurement_y2006m02
 CONCURRENTLY;
```

These allow further operations to be performed on the data before it is dropped. For example, this is often a useful time to back up the data using COPY, pg\_dump, or similar tools. It might also be a useful time to aggregate data into smaller formats, perform other data manipulations, or run reports. The first form of the command requires an ACCESS EXCLUSIVE lock on the parent table. Adding the CONCURRENTLY qualifier as in the second form allows the detach operation to require only SHARE UPDATE EXCLUSIVE lock on the parent table, but see ALTER TABLE ... DETACH PARTITION for details on the restrictions.

Similarly we can add a new partition to handle new data. We can create an empty partition in the partitioned table just as the original partitions were created above:

```
CREATE TABLE measurement_y2008m02 PARTITION OF measurement
 FOR VALUES FROM ('2008-02-01') TO ('2008-03-01')
 TABLESPACE fasttablespace;
```

As an alternative, it is sometimes more convenient to create the new table outside the partition structure, and attach it as a partition later. This allows new data to be loaded, checked, and transformed prior to it appearing in the partitioned table. Moreover, the ATTACH PARTITION operation requires only SHARE UPDATE EXCLUSIVE lock on the partitioned table, as opposed to the ACCESS EX-CLUSIVE lock that is required by CREATE TABLE ... PARTITION OF, so it is more friendly to concurrent operations on the partitioned table. The CREATE TABLE ... LIKE option is helpful to avoid tediously repeating the parent table's definition:

```
CREATE TABLE measurement_y2008m02
 (LIKE measurement INCLUDING DEFAULTS INCLUDING CONSTRAINTS)
 TABLESPACE fasttablespace;
ALTER TABLE measurement_y2008m02 ADD CONSTRAINT y2008m02
 CHECK ( logdate >= DATE '2008-02-01' AND logdate < DATE
 '2008-03-01' );
\copy measurement_y2008m02 from 'measurement_y2008m02'
-- possibly some other data preparation work
ALTER TABLE measurement ATTACH PARTITION measurement_y2008m02
 FOR VALUES FROM ('2008-02-01') TO ('2008-03-01' );
```

Before running the ATTACH PARTITION command, it is recommended to create a CHECK constraint on the table to be attached that matches the expected partition constraint, as illustrated above. That way, the system will be able to skip the scan which is otherwise needed to validate the implicit partition constraint. Without the CHECK constraint, the table will be scanned to validate the partition constraint while holding an ACCESS EXCLUSIVE lock on that partition. It is recommended to drop the nowredundant CHECK constraint after the ATTACH PARTITION is complete. If the table being attached is itself a partitioned table, then each of its sub-partitions will be recursively locked and scanned until either a suitable CHECK constraint is encountered or the leaf partitions are reached.

Similarly, if the partitioned table has a DEFAULT partition, it is recommended to create a CHECK constraint which excludes the to-be-attached partition's constraint. If this is not done then the DEFAULT partition will be scanned to verify that it contains no records which should be located in the partition being attached. This operation will be performed whilst holding an ACCESS EXCLUSIVE lock on the DEFAULT partition. If the DEFAULT partition is itself a partitioned table, then each of its partitions will be recursively checked in the same way as the table being attached, as mentioned above.

As explained above, it is possible to create indexes on partitioned tables so that they are applied automatically to the entire hierarchy. This is very convenient, as not only will the existing partitions become indexed, but also any partitions that are created in the future will. One limitation is that it's not possible to use the CONCURRENTLY qualifier when creating such a partitioned index. To avoid long lock times, it is possible to use CREATE INDEX ON ONLY the partitioned table; such an index is marked invalid, and the partitions do not get the index applied automatically. The indexes on partitions can be created individually using CONCURRENTLY, and then *attached* to the index on the parent using ALTER INDEX .. ATTACH PARTITION. Once indexes for all partitions are attached to the parent index, the parent index is marked valid automatically. Example:

```
CREATE INDEX measurement_usls_idx ON ONLY measurement (unitsales);
CREATE INDEX CONCURRENTLY measurement_usls_200602_idx
 ON measurement_y2006m02 (unitsales);
ALTER INDEX measurement_usls_idx
 ATTACH PARTITION measurement_usls_200602_idx;
...
```

This technique can be used with UNIQUE and PRIMARY KEY constraints too; the indexes are created implicitly when the constraint is created. Example:

```
ALTER TABLE ONLY measurement ADD UNIQUE (city_id, logdate);
ALTER TABLE measurement_y2006m02 ADD UNIQUE (city_id, logdate);
ALTER INDEX measurement_city_id_logdate_key
 ATTACH PARTITION measurement_y2006m02_city_id_logdate_key;
...
```

#### **5.11.2.3. Limitations**

The following limitations apply to partitioned tables:

- To create a unique or primary key constraint on a partitioned table, the partition keys must not include any expressions or function calls and the constraint's columns must include all of the partition key columns. This limitation exists because the individual indexes making up the constraint can only directly enforce uniqueness within their own partitions; therefore, the partition structure itself must guarantee that there are not duplicates in different partitions.
- There is no way to create an exclusion constraint spanning the whole partitioned table. It is only possible to put such a constraint on each leaf partition individually. Again, this limitation stems from not being able to enforce cross-partition restrictions.
- BEFORE ROW triggers on INSERT cannot change which partition is the final destination for a new row.

• Mixing temporary and permanent relations in the same partition tree is not allowed. Hence, if the partitioned table is permanent, so must be its partitions and likewise if the partitioned table is temporary. When using temporary relations, all members of the partition tree have to be from the same session.

Individual partitions are linked to their partitioned table using inheritance behind-the-scenes. However, it is not possible to use all of the generic features of inheritance with declaratively partitioned tables or their partitions, as discussed below. Notably, a partition cannot have any parents other than the partitioned table it is a partition of, nor can a table inherit from both a partitioned table and a regular table. That means partitioned tables and their partitions never share an inheritance hierarchy with regular tables.

Since a partition hierarchy consisting of the partitioned table and its partitions is still an inheritance hierarchy, tableoid and all the normal rules of inheritance apply as described in [Section 5.10,](#page-125-0) with a few exceptions:

- Partitions cannot have columns that are not present in the parent. It is not possible to specify columns when creating partitions with CREATE TABLE, nor is it possible to add columns to partitions after-the-fact using ALTER TABLE. Tables may be added as a partition with ALTER TABLE ... ATTACH PARTITION only if their columns exactly match the parent.
- Both CHECK and NOT NULL constraints of a partitioned table are always inherited by all its partitions. CHECK constraints that are marked NO INHERIT are not allowed to be created on partitioned tables. You cannot drop a NOT NULL constraint on a partition's column if the same constraint is present in the parent table.
- Using ONLY to add or drop a constraint on only the partitioned table is supported as long as there are no partitions. Once partitions exist, using ONLY will result in an error for any constraints other than UNIQUE and PRIMARY KEY. Instead, constraints on the partitions themselves can be added and (if they are not present in the parent table) dropped.
- As a partitioned table does not have any data itself, attempts to use TRUNCATE ONLY on a partitioned table will always return an error.

## <span id="page-134-0"></span>**5.11.3. Partitioning Using Inheritance**

While the built-in declarative partitioning is suitable for most common use cases, there are some circumstances where a more flexible approach may be useful. Partitioning can be implemented using table inheritance, which allows for several features not supported by declarative partitioning, such as:

- For declarative partitioning, partitions must have exactly the same set of columns as the partitioned table, whereas with table inheritance, child tables may have extra columns not present in the parent.
- Table inheritance allows for multiple inheritance.
- Declarative partitioning only supports range, list and hash partitioning, whereas table inheritance allows data to be divided in a manner of the user's choosing. (Note, however, that if constraint exclusion is unable to prune child tables effectively, query performance might be poor.)

### **5.11.3.1. Example**

This example builds a partitioning structure equivalent to the declarative partitioning example above. Use the following steps:

1. Create the "root" table, from which all of the "child" tables will inherit. This table will contain no data. Do not define any check constraints on this table, unless you intend them to be applied equally to all child tables. There is no point in defining any indexes or unique constraints on it, either. For our example, the root table is the measurement table as originally defined:

```
CREATE TABLE measurement (
```

```
 city_id int not null,
 logdate date not null,
 peaktemp int,
 unitsales int
);
```

2. Create several "child" tables that each inherit from the root table. Normally, these tables will not add any columns to the set inherited from the root. Just as with declarative partitioning, these tables are in every way normal PostgreSQL tables (or foreign tables).

```
CREATE TABLE measurement_y2006m02 () INHERITS (measurement);
CREATE TABLE measurement_y2006m03 () INHERITS (measurement);
...
CREATE TABLE measurement_y2007m11 () INHERITS (measurement);
CREATE TABLE measurement_y2007m12 () INHERITS (measurement);
CREATE TABLE measurement_y2008m01 () INHERITS (measurement);
```

3. Add non-overlapping table constraints to the child tables to define the allowed key values in each.

Typical examples would be:

```
CHECK ( x = 1 )
CHECK ( county IN ( 'Oxfordshire', 'Buckinghamshire',
 'Warwickshire' ))
CHECK ( outletID >= 100 AND outletID < 200 )
```

Ensure that the constraints guarantee that there is no overlap between the key values permitted in different child tables. A common mistake is to set up range constraints like:

```
CHECK ( outletID BETWEEN 100 AND 200 )
CHECK ( outletID BETWEEN 200 AND 300 )
```

This is wrong since it is not clear which child table the key value 200 belongs in. Instead, ranges should be defined in this style:

```
CREATE TABLE measurement_y2006m02 (
 CHECK ( logdate >= DATE '2006-02-01' AND logdate < DATE
 '2006-03-01' )
) INHERITS (measurement);
CREATE TABLE measurement_y2006m03 (
 CHECK ( logdate >= DATE '2006-03-01' AND logdate < DATE
 '2006-04-01' )
) INHERITS (measurement);
...
CREATE TABLE measurement_y2007m11 (
 CHECK ( logdate >= DATE '2007-11-01' AND logdate < DATE
 '2007-12-01' )
) INHERITS (measurement);
CREATE TABLE measurement_y2007m12 (
 CHECK ( logdate >= DATE '2007-12-01' AND logdate < DATE
 '2008-01-01' )
) INHERITS (measurement);
CREATE TABLE measurement_y2008m01 (
```

```
 CHECK ( logdate >= DATE '2008-01-01' AND logdate < DATE
 '2008-02-01' )
) INHERITS (measurement);
```

4. For each child table, create an index on the key column(s), as well as any other indexes you might want.

```
CREATE INDEX measurement_y2006m02_logdate ON
 measurement_y2006m02 (logdate);
CREATE INDEX measurement_y2006m03_logdate ON
 measurement_y2006m03 (logdate);
CREATE INDEX measurement_y2007m11_logdate ON
 measurement_y2007m11 (logdate);
CREATE INDEX measurement_y2007m12_logdate ON
 measurement_y2007m12 (logdate);
CREATE INDEX measurement_y2008m01_logdate ON
 measurement_y2008m01 (logdate);
```

5. We want our application to be able to say INSERT INTO measurement ... and have the data be redirected into the appropriate child table. We can arrange that by attaching a suitable trigger function to the root table. If data will be added only to the latest child, we can use a very simple trigger function:

```
CREATE OR REPLACE FUNCTION measurement_insert_trigger()
RETURNS TRIGGER AS $$
BEGIN
 INSERT INTO measurement_y2008m01 VALUES (NEW.*);
 RETURN NULL;
END;
$$
LANGUAGE plpgsql;
```

After creating the function, we create a trigger which calls the trigger function:

```
CREATE TRIGGER insert_measurement_trigger
 BEFORE INSERT ON measurement
 FOR EACH ROW EXECUTE FUNCTION measurement_insert_trigger();
```

We must redefine the trigger function each month so that it always inserts into the current child table. The trigger definition does not need to be updated, however.

We might want to insert data and have the server automatically locate the child table into which the row should be added. We could do this with a more complex trigger function, for example:

```
CREATE OR REPLACE FUNCTION measurement_insert_trigger()
RETURNS TRIGGER AS $$
BEGIN
 IF ( NEW.logdate >= DATE '2006-02-01' AND
 NEW.logdate < DATE '2006-03-01' ) THEN
 INSERT INTO measurement_y2006m02 VALUES (NEW.*);
 ELSIF ( NEW.logdate >= DATE '2006-03-01' AND
 NEW.logdate < DATE '2006-04-01' ) THEN
 INSERT INTO measurement_y2006m03 VALUES (NEW.*);
 ...
 ELSIF ( NEW.logdate >= DATE '2008-01-01' AND
 NEW.logdate < DATE '2008-02-01' ) THEN
 INSERT INTO measurement_y2008m01 VALUES (NEW.*);
```

```
 ELSE
 RAISE EXCEPTION 'Date out of range. Fix the
 measurement_insert_trigger() function!';
 END IF;
 RETURN NULL;
END;
$$
LANGUAGE plpgsql;
```

The trigger definition is the same as before. Note that each IF test must exactly match the CHECK constraint for its child table.

While this function is more complex than the single-month case, it doesn't need to be updated as often, since branches can be added in advance of being needed.

#### **Note**

In practice, it might be best to check the newest child first, if most inserts go into that child. For simplicity, we have shown the trigger's tests in the same order as in other parts of this example.

A different approach to redirecting inserts into the appropriate child table is to set up rules, instead of a trigger, on the root table. For example:

```
CREATE RULE measurement_insert_y2006m02 AS
ON INSERT TO measurement WHERE
 ( logdate >= DATE '2006-02-01' AND logdate < DATE
 '2006-03-01' )
DO INSTEAD
 INSERT INTO measurement_y2006m02 VALUES (NEW.*);
...
CREATE RULE measurement_insert_y2008m01 AS
ON INSERT TO measurement WHERE
 ( logdate >= DATE '2008-01-01' AND logdate < DATE
 '2008-02-01' )
DO INSTEAD
 INSERT INTO measurement_y2008m01 VALUES (NEW.*);
```

A rule has significantly more overhead than a trigger, but the overhead is paid once per query rather than once per row, so this method might be advantageous for bulk-insert situations. In most cases, however, the trigger method will offer better performance.

Be aware that COPY ignores rules. If you want to use COPY to insert data, you'll need to copy into the correct child table rather than directly into the root. COPY does fire triggers, so you can use it normally if you use the trigger approach.

Another disadvantage of the rule approach is that there is no simple way to force an error if the set of rules doesn't cover the insertion date; the data will silently go into the root table instead.

6. Ensure that the constraint\_exclusion configuration parameter is not disabled in postgresql.conf; otherwise child tables may be accessed unnecessarily.

As we can see, a complex table hierarchy could require a substantial amount of DDL. In the above example we would be creating a new child table each month, so it might be wise to write a script that generates the required DDL automatically.

### **5.11.3.2. Maintenance for Inheritance Partitioning**

To remove old data quickly, simply drop the child table that is no longer necessary:

```
DROP TABLE measurement_y2006m02;
```

To remove the child table from the inheritance hierarchy table but retain access to it as a table in its own right:

```
ALTER TABLE measurement_y2006m02 NO INHERIT measurement;
```

To add a new child table to handle new data, create an empty child table just as the original children were created above:

```
CREATE TABLE measurement_y2008m02 (
 CHECK ( logdate >= DATE '2008-02-01' AND logdate < DATE
 '2008-03-01' )
) INHERITS (measurement);
```

Alternatively, one may want to create and populate the new child table before adding it to the table hierarchy. This could allow data to be loaded, checked, and transformed before being made visible to queries on the parent table.

```
CREATE TABLE measurement_y2008m02
 (LIKE measurement INCLUDING DEFAULTS INCLUDING CONSTRAINTS);
ALTER TABLE measurement_y2008m02 ADD CONSTRAINT y2008m02
 CHECK ( logdate >= DATE '2008-02-01' AND logdate < DATE
 '2008-03-01' );
\copy measurement_y2008m02 from 'measurement_y2008m02'
-- possibly some other data preparation work
ALTER TABLE measurement_y2008m02 INHERIT measurement;
```

#### **5.11.3.3. Caveats**

The following caveats apply to partitioning implemented using inheritance:

- There is no automatic way to verify that all of the CHECK constraints are mutually exclusive. It is safer to create code that generates child tables and creates and/or modifies associated objects than to write each by hand.
- Indexes and foreign key constraints apply to single tables and not to their inheritance children, hence they have some [caveats](#page-128-1) to be aware of.
- The schemes shown here assume that the values of a row's key column(s) never change, or at least do not change enough to require it to move to another partition. An UPDATE that attempts to do that will fail because of the CHECK constraints. If you need to handle such cases, you can put suitable update triggers on the child tables, but it makes management of the structure much more complicated.
- If you are using manual VACUUM or ANALYZE commands, don't forget that you need to run them on each child table individually. A command like:

```
ANALYZE measurement;
```

will only process the root table.

- INSERT statements with ON CONFLICT clauses are unlikely to work as expected, as the ON CONFLICT action is only taken in case of unique violations on the specified target relation, not its child relations.
- Triggers or rules will be needed to route rows to the desired child table, unless the application is explicitly aware of the partitioning scheme. Triggers may be complicated to write, and will be much slower than the tuple routing performed internally by declarative partitioning.

## <span id="page-139-0"></span>**5.11.4. Partition Pruning**

*Partition pruning* is a query optimization technique that improves performance for declaratively partitioned tables. As an example:

```
SET enable_partition_pruning = on; -- the default
SELECT count(*) FROM measurement WHERE logdate >= DATE
 '2008-01-01';
```

Without partition pruning, the above query would scan each of the partitions of the measurement table. With partition pruning enabled, the planner will examine the definition of each partition and prove that the partition need not be scanned because it could not contain any rows meeting the query's WHERE clause. When the planner can prove this, it excludes (*prunes*) the partition from the query plan.

By using the EXPLAIN command and the enable\_partition\_pruning configuration parameter, it's possible to show the difference between a plan for which partitions have been pruned and one for which they have not. A typical unoptimized plan for this type of table setup is:

```
SET enable_partition_pruning = off;
EXPLAIN SELECT count(*) FROM measurement WHERE logdate >= DATE
 '2008-01-01';
 QUERY PLAN
-------------------------------------------------------------------
----------------
 Aggregate (cost=188.76..188.77 rows=1 width=8)
 -> Append (cost=0.00..181.05 rows=3085 width=0)
 -> Seq Scan on measurement_y2006m02 (cost=0.00..33.12
 rows=617 width=0)
 Filter: (logdate >= '2008-01-01'::date)
 -> Seq Scan on measurement_y2006m03 (cost=0.00..33.12
 rows=617 width=0)
 Filter: (logdate >= '2008-01-01'::date)
...
 -> Seq Scan on measurement_y2007m11 (cost=0.00..33.12
 rows=617 width=0)
 Filter: (logdate >= '2008-01-01'::date)
 -> Seq Scan on measurement_y2007m12 (cost=0.00..33.12
 rows=617 width=0)
 Filter: (logdate >= '2008-01-01'::date)
 -> Seq Scan on measurement_y2008m01 (cost=0.00..33.12
 rows=617 width=0)
 Filter: (logdate >= '2008-01-01'::date)
```

Some or all of the partitions might use index scans instead of full-table sequential scans, but the point here is that there is no need to scan the older partitions at all to answer this query. When we enable partition pruning, we get a significantly cheaper plan that will deliver the same answer:

```
SET enable_partition_pruning = on;
```

```
EXPLAIN SELECT count(*) FROM measurement WHERE logdate >= DATE
 '2008-01-01';
 QUERY PLAN
-------------------------------------------------------------------
----------------
 Aggregate (cost=37.75..37.76 rows=1 width=8)
 -> Seq Scan on measurement_y2008m01 (cost=0.00..33.12 rows=617
 width=0)
 Filter: (logdate >= '2008-01-01'::date)
```

Note that partition pruning is driven only by the constraints defined implicitly by the partition keys, not by the presence of indexes. Therefore it isn't necessary to define indexes on the key columns. Whether an index needs to be created for a given partition depends on whether you expect that queries that scan the partition will generally scan a large part of the partition or just a small part. An index will be helpful in the latter case but not the former.

Partition pruning can be performed not only during the planning of a given query, but also during its execution. This is useful as it can allow more partitions to be pruned when clauses contain expressions whose values are not known at query planning time, for example, parameters defined in a PREPARE statement, using a value obtained from a subquery, or using a parameterized value on the inner side of a nested loop join. Partition pruning during execution can be performed at any of the following times:

- During initialization of the query plan. Partition pruning can be performed here for parameter values which are known during the initialization phase of execution. Partitions which are pruned during this stage will not show up in the query's EXPLAIN or EXPLAIN ANALYZE. It is possible to determine the number of partitions which were removed during this phase by observing the "Subplans Removed" property in the EXPLAIN output. It's important to note that any partitions removed by the partition pruning done at this stage are still locked at the beginning of execution.
- During actual execution of the query plan. Partition pruning may also be performed here to remove partitions using values which are only known during actual query execution. This includes values from subqueries and values from execution-time parameters such as those from parameterized nested loop joins. Since the value of these parameters may change many times during the execution of the query, partition pruning is performed whenever one of the execution parameters being used by partition pruning changes. Determining if partitions were pruned during this phase requires careful inspection of the loops property in the EXPLAIN ANALYZE output. Subplans corresponding to different partitions may have different values for it depending on how many times each of them was pruned during execution. Some may be shown as (never executed) if they were pruned every time.

Partition pruning can be disabled using the enable\_partition\_pruning setting.

## <span id="page-140-0"></span>**5.11.5. Partitioning and Constraint Exclusion**

*Constraint exclusion* is a query optimization technique similar to partition pruning. While it is primarily used for partitioning implemented using the legacy inheritance method, it can be used for other purposes, including with declarative partitioning.

Constraint exclusion works in a very similar way to partition pruning, except that it uses each table's CHECK constraints — which gives it its name — whereas partition pruning uses the table's partition bounds, which exist only in the case of declarative partitioning. Another difference is that constraint exclusion is only applied at plan time; there is no attempt to remove partitions at execution time.

The fact that constraint exclusion uses CHECK constraints, which makes it slow compared to partition pruning, can sometimes be used as an advantage: because constraints can be defined even on declaratively-partitioned tables, in addition to their internal partition bounds, constraint exclusion may be able to elide additional partitions from the query plan.

The default (and recommended) setting of constraint\_exclusion is neither on nor off, but an intermediate setting called partition, which causes the technique to be applied only to queries that are likely to be working on inheritance partitioned tables. The on setting causes the planner to examine CHECK constraints in all queries, even simple ones that are unlikely to benefit.

The following caveats apply to constraint exclusion:

- Constraint exclusion is only applied during query planning, unlike partition pruning, which can also be applied during query execution.
- Constraint exclusion only works when the query's WHERE clause contains constants (or externally supplied parameters). For example, a comparison against a non-immutable function such as CUR-RENT\_TIMESTAMP cannot be optimized, since the planner cannot know which child table the function's value might fall into at run time.
- Keep the partitioning constraints simple, else the planner may not be able to prove that child tables might not need to be visited. Use simple equality conditions for list partitioning, or simple range tests for range partitioning, as illustrated in the preceding examples. A good rule of thumb is that partitioning constraints should contain only comparisons of the partitioning column(s) to constants using B-tree-indexable operators, because only B-tree-indexable column(s) are allowed in the partition key.
- All constraints on all children of the parent table are examined during constraint exclusion, so large numbers of children are likely to increase query planning time considerably. So the legacy inheritance based partitioning will work well with up to perhaps a hundred child tables; don't try to use many thousands of children.

## <span id="page-141-0"></span>**5.11.6. Best Practices for Declarative Partitioning**

The choice of how to partition a table should be made carefully, as the performance of query planning and execution can be negatively affected by poor design.

One of the most critical design decisions will be the column or columns by which you partition your data. Often the best choice will be to partition by the column or set of columns which most commonly appear in WHERE clauses of queries being executed on the partitioned table. WHERE clauses that are compatible with the partition bound constraints can be used to prune unneeded partitions. However, you may be forced into making other decisions by requirements for the PRIMARY KEY or a UNIQUE constraint. Removal of unwanted data is also a factor to consider when planning your partitioning strategy. An entire partition can be detached fairly quickly, so it may be beneficial to design the partition strategy in such a way that all data to be removed at once is located in a single partition.

Choosing the target number of partitions that the table should be divided into is also a critical decision to make. Not having enough partitions may mean that indexes remain too large and that data locality remains poor which could result in low cache hit ratios. However, dividing the table into too many partitions can also cause issues. Too many partitions can mean longer query planning times and higher memory consumption during both query planning and execution, as further described below. When choosing how to partition your table, it's also important to consider what changes may occur in the future. For example, if you choose to have one partition per customer and you currently have a small number of large customers, consider the implications if in several years you instead find yourself with a large number of small customers. In this case, it may be better to choose to partition by HASH and choose a reasonable number of partitions rather than trying to partition by LIST and hoping that the number of customers does not increase beyond what it is practical to partition the data by.

Sub-partitioning can be useful to further divide partitions that are expected to become larger than other partitions. Another option is to use range partitioning with multiple columns in the partition key. Either of these can easily lead to excessive numbers of partitions, so restraint is advisable.

It is important to consider the overhead of partitioning during query planning and execution. The query planner is generally able to handle partition hierarchies with up to a few thousand partitions fairly well, provided that typical queries allow the query planner to prune all but a small number of partitions. Planning times become longer and memory consumption becomes higher when more partitions remain after the planner performs partition pruning. Another reason to be concerned about having a large number of partitions is that the server's memory consumption may grow significantly over time, especially if many sessions touch large numbers of partitions. That's because each partition requires its metadata to be loaded into the local memory of each session that touches it.

With data warehouse type workloads, it can make sense to use a larger number of partitions than with an OLTP type workload. Generally, in data warehouses, query planning time is less of a concern as the majority of processing time is spent during query execution. With either of these two types of workload, it is important to make the right decisions early, as re-partitioning large quantities of data can be painfully slow. Simulations of the intended workload are often beneficial for optimizing the partitioning strategy. Never just assume that more partitions are better than fewer partitions, nor viceversa.

# <span id="page-142-0"></span>**5.12. Foreign Data**

PostgreSQL implements portions of the SQL/MED specification, allowing you to access data that resides outside PostgreSQL using regular SQL queries. Such data is referred to as *foreign data*. (Note that this usage is not to be confused with foreign keys, which are a type of constraint within the database.)

Foreign data is accessed with help from a *foreign data wrapper*. A foreign data wrapper is a library that can communicate with an external data source, hiding the details of connecting to the data source and obtaining data from it. There are some foreign data wrappers available as contrib modules; see Appendix F. Other kinds of foreign data wrappers might be found as third party products. If none of the existing foreign data wrappers suit your needs, you can write your own; see Chapter 57.

To access foreign data, you need to create a *foreign server* object, which defines how to connect to a particular external data source according to the set of options used by its supporting foreign data wrapper. Then you need to create one or more *foreign tables*, which define the structure of the remote data. A foreign table can be used in queries just like a normal table, but a foreign table has no storage in the PostgreSQL server. Whenever it is used, PostgreSQL asks the foreign data wrapper to fetch data from the external source, or transmit data to the external source in the case of update commands.

Accessing remote data may require authenticating to the external data source. This information can be provided by a *user mapping*, which can provide additional data such as user names and passwords based on the current PostgreSQL role.

For additional information, see CREATE FOREIGN DATA WRAPPER, CREATE SERVER, CRE-ATE USER MAPPING, CREATE FOREIGN TABLE, and IMPORT FOREIGN SCHEMA.

# <span id="page-142-1"></span>**5.13. Other Database Objects**

Tables are the central objects in a relational database structure, because they hold your data. But they are not the only objects that exist in a database. Many other kinds of objects can be created to make the use and management of the data more efficient or convenient. They are not discussed in this chapter, but we give you a list here so that you are aware of what is possible:

- Views
- Functions, procedures, and operators
- Data types and domains
- Triggers and rewrite rules

Detailed information on these topics appears in Part V.

# <span id="page-142-2"></span>**5.14. Dependency Tracking**

When you create complex database structures involving many tables with foreign key constraints, views, triggers, functions, etc. you implicitly create a net of dependencies between the objects. For instance, a table with a foreign key constraint depends on the table it references.

To ensure the integrity of the entire database structure, PostgreSQL makes sure that you cannot drop objects that other objects still depend on. For example, attempting to drop the products table we considered in [Section 5.4.5,](#page-103-0) with the orders table depending on it, would result in an error message like this:

```
DROP TABLE products;
ERROR: cannot drop table products because other objects depend on
 it
DETAIL: constraint orders_product_no_fkey on table orders depends
 on table products
HINT: Use DROP ... CASCADE to drop the dependent objects too.
```

The error message contains a useful hint: if you do not want to bother deleting all the dependent objects individually, you can run:

```
DROP TABLE products CASCADE;
```

and all the dependent objects will be removed, as will any objects that depend on them, recursively. In this case, it doesn't remove the orders table, it only removes the foreign key constraint. It stops there because nothing depends on the foreign key constraint. (If you want to check what DROP ... CASCADE will do, run DROP without CASCADE and read the DETAIL output.)

Almost all DROP commands in PostgreSQL support specifying CASCADE. Of course, the nature of the possible dependencies varies with the type of the object. You can also write RESTRICT instead of CASCADE to get the default behavior, which is to prevent dropping objects that any other objects depend on.

#### **Note**

According to the SQL standard, specifying either RESTRICT or CASCADE is required in a DROP command. No database system actually enforces that rule, but whether the default behavior is RESTRICT or CASCADE varies across systems.

If a DROP command lists multiple objects, CASCADE is only required when there are dependencies outside the specified group. For example, when saying DROP TABLE tab1, tab2 the existence of a foreign key referencing tab1 from tab2 would not mean that CASCADE is needed to succeed.

For a user-defined function or procedure whose body is defined as a string literal, PostgreSQL tracks dependencies associated with the function's externally-visible properties, such as its argument and result types, but *not* dependencies that could only be known by examining the function body. As an example, consider this situation:

```
CREATE TYPE rainbow AS ENUM ('red', 'orange', 'yellow',
 'green', 'blue', 'purple');
CREATE TABLE my_colors (color rainbow, note text);
CREATE FUNCTION get_color_note (rainbow) RETURNS text AS
 'SELECT note FROM my_colors WHERE color = $1'
```

```
 LANGUAGE SQL;
```

(See Section 38.5 for an explanation of SQL-language functions.) PostgreSQL will be aware that the get\_color\_note function depends on the rainbow type: dropping the type would force dropping the function, because its argument type would no longer be defined. But PostgreSQL will not consider get\_color\_note to depend on the my\_colors table, and so will not drop the function if the table is dropped. While there are disadvantages to this approach, there are also benefits. The function is still valid in some sense if the table is missing, though executing it would cause an error; creating a new table of the same name would allow the function to work again.

On the other hand, for a SQL-language function or procedure whose body is written in SQL-standard style, the body is parsed at function definition time and all dependencies recognized by the parser are stored. Thus, if we write the function above as

```
CREATE FUNCTION get_color_note (rainbow) RETURNS text
BEGIN ATOMIC
 SELECT note FROM my_colors WHERE color = $1;
END;
```

then the function's dependency on the my\_colors table will be known and enforced by DROP.

# <span id="page-145-0"></span>**Chapter 6. Data Manipulation**

The previous chapter discussed how to create tables and other structures to hold your data. Now it is time to fill the tables with data. This chapter covers how to insert, update, and delete table data. The chapter after this will finally explain how to extract your long-lost data from the database.

# <span id="page-145-1"></span>**6.1. Inserting Data**

When a table is created, it contains no data. The first thing to do before a database can be of much use is to insert data. Data is inserted one row at a time. You can also insert more than one row in a single command, but it is not possible to insert something that is not a complete row. Even if you know only some column values, a complete row must be created.

To create a new row, use the INSERT command. The command requires the table name and column values. For example, consider the products table from [Chapter 5:](#page-95-0)

```
CREATE TABLE products (
 product_no integer,
 name text,
 price numeric
);
```

An example command to insert a row would be:

```
INSERT INTO products VALUES (1, 'Cheese', 9.99);
```

The data values are listed in the order in which the columns appear in the table, separated by commas. Usually, the data values will be literals (constants), but scalar expressions are also allowed.

The above syntax has the drawback that you need to know the order of the columns in the table. To avoid this you can also list the columns explicitly. For example, both of the following commands have the same effect as the one above:

```
INSERT INTO products (product_no, name, price) VALUES (1, 'Cheese',
 9.99);
INSERT INTO products (name, price, product_no) VALUES ('Cheese',
 9.99, 1);
```

Many users consider it good practice to always list the column names.

If you don't have values for all the columns, you can omit some of them. In that case, the columns will be filled with their default values. For example:

```
INSERT INTO products (product_no, name) VALUES (1, 'Cheese');
INSERT INTO products VALUES (1, 'Cheese');
```

The second form is a PostgreSQL extension. It fills the columns from the left with as many values as are given, and the rest will be defaulted.

For clarity, you can also request default values explicitly, for individual columns or for the entire row:

```
INSERT INTO products (product_no, name, price) VALUES (1, 'Cheese',
 DEFAULT);
```

```
INSERT INTO products DEFAULT VALUES;
```

You can insert multiple rows in a single command:

```
INSERT INTO products (product_no, name, price) VALUES
 (1, 'Cheese', 9.99),
 (2, 'Bread', 1.99),
 (3, 'Milk', 2.99);
```

It is also possible to insert the result of a query (which might be no rows, one row, or many rows):

```
INSERT INTO products (product_no, name, price)
 SELECT product_no, name, price FROM new_products
 WHERE release_date = 'today';
```

This provides the full power of the SQL query mechanism [\(Chapter 7\)](#page-149-0) for computing the rows to be inserted.

#### **Tip**

When inserting a lot of data at the same time, consider using the COPY command. It is not as flexible as the INSERT command, but is more efficient. Refer to Section 14.4 for more information on improving bulk loading performance.

# <span id="page-146-0"></span>**6.2. Updating Data**

The modification of data that is already in the database is referred to as updating. You can update individual rows, all the rows in a table, or a subset of all rows. Each column can be updated separately; the other columns are not affected.

To update existing rows, use the UPDATE command. This requires three pieces of information:

- 1. The name of the table and column to update
- 2. The new value of the column
- 3. Which row(s) to update

Recall from [Chapter 5](#page-95-0) that SQL does not, in general, provide a unique identifier for rows. Therefore it is not always possible to directly specify which row to update. Instead, you specify which conditions a row must meet in order to be updated. Only if you have a primary key in the table (independent of whether you declared it or not) can you reliably address individual rows by choosing a condition that matches the primary key. Graphical database access tools rely on this fact to allow you to update rows individually.

For example, this command updates all products that have a price of 5 to have a price of 10:

```
UPDATE products SET price = 10 WHERE price = 5;
```

This might cause zero, one, or many rows to be updated. It is not an error to attempt an update that does not match any rows.

Let's look at that command in detail. First is the key word UPDATE followed by the table name. As usual, the table name can be schema-qualified, otherwise it is looked up in the path. Next is the key word SET followed by the column name, an equal sign, and the new column value. The new column value can be any scalar expression, not just a constant. For example, if you want to raise the price of all products by 10% you could use:

```
UPDATE products SET price = price * 1.10;
```

As you see, the expression for the new value can refer to the existing value(s) in the row. We also left out the WHERE clause. If it is omitted, it means that all rows in the table are updated. If it is present, only those rows that match the WHERE condition are updated. Note that the equals sign in the SET clause is an assignment while the one in the WHERE clause is a comparison, but this does not create any ambiguity. Of course, the WHERE condition does not have to be an equality test. Many other operators are available (see Chapter 9). But the expression needs to evaluate to a Boolean result.

You can update more than one column in an UPDATE command by listing more than one assignment in the SET clause. For example:

```
UPDATE mytable SET a = 5, b = 3, c = 1 WHERE a > 0;
```

# <span id="page-147-0"></span>**6.3. Deleting Data**

So far we have explained how to add data to tables and how to change data. What remains is to discuss how to remove data that is no longer needed. Just as adding data is only possible in whole rows, you can only remove entire rows from a table. In the previous section we explained that SQL does not provide a way to directly address individual rows. Therefore, removing rows can only be done by specifying conditions that the rows to be removed have to match. If you have a primary key in the table then you can specify the exact row. But you can also remove groups of rows matching a condition, or you can remove all rows in the table at once.

You use the DELETE command to remove rows; the syntax is very similar to the UPDATE command. For instance, to remove all rows from the products table that have a price of 10, use:

```
DELETE FROM products WHERE price = 10;
If you simply write:
DELETE FROM products;
```

then all rows in the table will be deleted! Caveat programmer.

# <span id="page-147-1"></span>**6.4. Returning Data from Modified Rows**

Sometimes it is useful to obtain data from modified rows while they are being manipulated. The INSERT, UPDATE, and DELETE commands all have an optional RETURNING clause that supports this. Use of RETURNING avoids performing an extra database query to collect the data, and is especially valuable when it would otherwise be difficult to identify the modified rows reliably.

The allowed contents of a RETURNING clause are the same as a SELECT command's output list (see [Section 7.3](#page-165-0)). It can contain column names of the command's target table, or value expressions using those columns. A common shorthand is RETURNING \*, which selects all columns of the target table in order.

In an INSERT, the data available to RETURNING is the row as it was inserted. This is not so useful in trivial inserts, since it would just repeat the data provided by the client. But it can be very handy when relying on computed default values. For example, when using a [serial](#page-185-0) column to provide unique identifiers, RETURNING can return the ID assigned to a new row:

```
CREATE TABLE users (firstname text, lastname text, id serial
 primary key);
```

```
INSERT INTO users (firstname, lastname) VALUES ('Joe', 'Cool')
 RETURNING id;
```

The RETURNING clause is also very useful with INSERT ... SELECT.

In an UPDATE, the data available to RETURNING is the new content of the modified row. For example:

```
UPDATE products SET price = price * 1.10
 WHERE price <= 99.99
 RETURNING name, price AS new_price;
```

In a DELETE, the data available to RETURNING is the content of the deleted row. For example:

```
DELETE FROM products
 WHERE obsoletion_date = 'today'
 RETURNING *;
```

If there are triggers (Chapter 39) on the target table, the data available to RETURNING is the row as modified by the triggers. Thus, inspecting columns computed by triggers is another common use-case for RETURNING.

# <span id="page-149-0"></span>**Chapter 7. Queries**

The previous chapters explained how to create tables, how to fill them with data, and how to manipulate that data. Now we finally discuss how to retrieve the data from the database.

# <span id="page-149-1"></span>**7.1. Overview**

The process of retrieving or the command to retrieve data from a database is called a *query*. In SQL the SELECT command is used to specify queries. The general syntax of the SELECT command is

```
[WITH with_queries] SELECT select_list FROM table_expression
 [sort_specification]
```

The following sections describe the details of the select list, the table expression, and the sort specification. WITH queries are treated last since they are an advanced feature.

A simple kind of query has the form:

```
SELECT * FROM table1;
```

Assuming that there is a table called table1, this command would retrieve all rows and all userdefined columns from table1. (The method of retrieval depends on the client application. For example, the psql program will display an ASCII-art table on the screen, while client libraries will offer functions to extract individual values from the query result.) The select list specification \* means all columns that the table expression happens to provide. A select list can also select a subset of the available columns or make calculations using the columns. For example, if table1 has columns named a, b, and c (and perhaps others) you can make the following query:

```
SELECT a, b + c FROM table1;
```

(assuming that b and c are of a numerical data type). See [Section 7.3](#page-165-0) for more details.

FROM table1 is a simple kind of table expression: it reads just one table. In general, table expressions can be complex constructs of base tables, joins, and subqueries. But you can also omit the table expression entirely and use the SELECT command as a calculator:

```
SELECT 3 * 4;
```

This is more useful if the expressions in the select list return varying results. For example, you could call a function this way:

```
SELECT random();
```

# <span id="page-149-2"></span>**7.2. Table Expressions**

A *table expression* computes a table. The table expression contains a FROM clause that is optionally followed by WHERE, GROUP BY, and HAVING clauses. Trivial table expressions simply refer to a table on disk, a so-called base table, but more complex expressions can be used to modify or combine base tables in various ways.

The optional WHERE, GROUP BY, and HAVING clauses in the table expression specify a pipeline of successive transformations performed on the table derived in the FROM clause. All these transformations produce a virtual table that provides the rows that are passed to the select list to compute the output rows of the query.

## <span id="page-150-0"></span>**7.2.1. The FROM Clause**

The FROM clause derives a table from one or more other tables given in a comma-separated table reference list.

```
FROM table_reference [, table_reference [, ...]]
```

A table reference can be a table name (possibly schema-qualified), or a derived table such as a subquery, a JOIN construct, or complex combinations of these. If more than one table reference is listed in the FROM clause, the tables are cross-joined (that is, the Cartesian product of their rows is formed; see below). The result of the FROM list is an intermediate virtual table that can then be subject to transformations by the WHERE, GROUP BY, and HAVING clauses and is finally the result of the overall table expression.

When a table reference names a table that is the parent of a table inheritance hierarchy, the table reference produces rows of not only that table but all of its descendant tables, unless the key word ONLY precedes the table name. However, the reference produces only the columns that appear in the named table — any columns added in subtables are ignored.

Instead of writing ONLY before the table name, you can write \* after the table name to explicitly specify that descendant tables are included. There is no real reason to use this syntax any more, because searching descendant tables is now always the default behavior. However, it is supported for compatibility with older releases.

### **7.2.1.1. Joined Tables**

A joined table is a table derived from two other (real or derived) tables according to the rules of the particular join type. Inner, outer, and cross-joins are available. The general syntax of a joined table is

```
T1 join_type T2 [ join_condition ]
```

Joins of all types can be chained together, or nested: either or both T1 and T2 can be joined tables. Parentheses can be used around JOIN clauses to control the join order. In the absence of parentheses, JOIN clauses nest left-to-right.

#### **Join Types**

Cross join

```
T1 CROSS JOIN T2
```

For every possible combination of rows from T1 and T2 (i.e., a Cartesian product), the joined table will contain a row consisting of all columns in T1 followed by all columns in T2. If the tables have N and M rows respectively, the joined table will have N \* M rows.

FROM T1 CROSS JOIN T2 is equivalent to FROM T1 INNER JOIN T2 ON TRUE (see below). It is also equivalent to FROM T1, T2.

#### **Note**

This latter equivalence does not hold exactly when more than two tables appear, because JOIN binds more tightly than comma. For example FROM T1 CROSS JOIN T2 INNER JOIN T3 ON condition is not the same as FROM T1, T2 INNER JOIN T3 ON condition because the condition can reference T1 in the first case but not the second.

#### Qualified joins

```
T1 { [INNER] | { LEFT | RIGHT | FULL } [OUTER] } JOIN T2
 ON boolean_expression
T1 { [INNER] | { LEFT | RIGHT | FULL } [OUTER] } JOIN T2 USING
 ( join column list )
T1 NATURAL { [INNER] | { LEFT | RIGHT | FULL } [OUTER] } JOIN T2
```

The words INNER and OUTER are optional in all forms. INNER is the default; LEFT, RIGHT, and FULL imply an outer join.

The *join condition* is specified in the ON or USING clause, or implicitly by the word NATURAL. The join condition determines which rows from the two source tables are considered to "match", as explained in detail below.

The possible types of qualified join are:

```
INNER JOIN
```

For each row R1 of T1, the joined table has a row for each row in T2 that satisfies the join condition with R1.

```
LEFT OUTER JOIN
```

First, an inner join is performed. Then, for each row in T1 that does not satisfy the join condition with any row in T2, a joined row is added with null values in columns of T2. Thus, the joined table always has at least one row for each row in T1.

```
RIGHT OUTER JOIN
```

First, an inner join is performed. Then, for each row in T2 that does not satisfy the join condition with any row in T1, a joined row is added with null values in columns of T1. This is the converse of a left join: the result table will always have a row for each row in T2.

```
FULL OUTER JOIN
```

First, an inner join is performed. Then, for each row in T1 that does not satisfy the join condition with any row in T2, a joined row is added with null values in columns of T2. Also, for each row of T2 that does not satisfy the join condition with any row in T1, a joined row with null values in the columns of T1 is added.

The ON clause is the most general kind of join condition: it takes a Boolean value expression of the same kind as is used in a WHERE clause. A pair of rows from T1 and T2 match if the ON expression evaluates to true.

The USING clause is a shorthand that allows you to take advantage of the specific situation where both sides of the join use the same name for the joining column(s). It takes a comma-separated list of the shared column names and forms a join condition that includes an equality comparison for each one. For example, joining T1 and T2 with USING (a, b) produces the join condition ON T1.a = T2.a AND T1.b = T2.b.

Furthermore, the output of JOIN USING suppresses redundant columns: there is no need to print both of the matched columns, since they must have equal values. While JOIN ON produces all columns from T1 followed by all columns from T2, JOIN USING produces one output column for each of the listed column pairs (in the listed order), followed by any remaining columns from T1, followed by any remaining columns from T2.

 Finally, NATURAL is a shorthand form of USING: it forms a USING list consisting of all column names that appear in both input tables. As with USING, these columns appear only once in the output table. If there are no common column names, NATURAL JOIN behaves like JOIN ... ON TRUE, producing a cross-product join.

#### **Note**

USING is reasonably safe from column changes in the joined relations since only the listed columns are combined. NATURAL is considerably more risky since any schema changes to either relation that cause a new matching column name to be present will cause the join to combine that new column as well.

To put this together, assume we have tables t1:

| num   name |             |
|------------|-------------|
|            | +           |
| 1   a      |             |
| 2   b      |             |
| 3   c      |             |
| and t2:    |             |
|            | num   value |
|            | +           |
|            | 1   xxx     |
|            | 3   yyy     |
|            | 5   zzz     |

then we get the following results for the various joins:

```
=> SELECT * FROM t1 CROSS JOIN t2;
 num | name | num | value
-----+------+-----+-------
 1 | a | 1 | xxx
 1 | a | 3 | yyy
 1 | a | 5 | zzz
 2 | b | 1 | xxx
 2 | b | 3 | yyy
 2 | b | 5 | zzz
 3 | c | 1 | xxx
 3 | c | 3 | yyy
 3 | c | 5 | zzz
(9 rows)
```

```
=> SELECT * FROM t1 INNER JOIN t2 ON t1.num = t2.num;
 num | name | num | value
-----+------+-----+-------
 1 | a | 1 | xxx
 3 | c | 3 | yyy
(2 rows)
=> SELECT * FROM t1 INNER JOIN t2 USING (num);
 num | name | value
-----+------+-------
 1 | a | xxx
```

```
 3 | c | yyy
(2 rows)
=> SELECT * FROM t1 NATURAL INNER JOIN t2;
 num | name | value
-----+------+-------
 1 | a | xxx
 3 | c | yyy
(2 rows)
=> SELECT * FROM t1 LEFT JOIN t2 ON t1.num = t2.num;
 num | name | num | value
-----+------+-----+-------
 1 | a | 1 | xxx
 2 | b | |
 3 | c | 3 | yyy
(3 rows)
=> SELECT * FROM t1 LEFT JOIN t2 USING (num);
 num | name | value
-----+------+-------
 1 | a | xxx
 2 | b |
 3 | c | yyy
(3 rows)
=> SELECT * FROM t1 RIGHT JOIN t2 ON t1.num = t2.num;
 num | name | num | value
-----+------+-----+-------
 1 | a | 1 | xxx
 3 | c | 3 | yyy
 | | 5 | zzz
(3 rows)
=> SELECT * FROM t1 FULL JOIN t2 ON t1.num = t2.num;
 num | name | num | value
-----+------+-----+-------
 1 | a | 1 | xxx
 2 | b | |
 3 | c | 3 | yyy
 | | 5 | zzz
(4 rows)
```

The join condition specified with ON can also contain conditions that do not relate directly to the join. This can prove useful for some queries but needs to be thought out carefully. For example:

```
=> SELECT * FROM t1 LEFT JOIN t2 ON t1.num = t2.num AND t2.value =
 'xxx';
 num | name | num | value
-----+------+-----+-------
 1 | a | 1 | xxx
 2 | b | |
 3 | c | |
(3 rows)
```

Notice that placing the restriction in the WHERE clause produces a different result:

```
=> SELECT * FROM t1 LEFT JOIN t2 ON t1.num = t2.num WHERE t2.value
 = 'xxx';
 num | name | num | value
-----+------+-----+-------
 1 | a | 1 | xxx
(1 row)
```

This is because a restriction placed in the ON clause is processed *before* the join, while a restriction placed in the WHERE clause is processed *after* the join. That does not matter with inner joins, but it matters a lot with outer joins.

#### <span id="page-154-0"></span>**7.2.1.2. Table and Column Aliases**

A temporary name can be given to tables and complex table references to be used for references to the derived table in the rest of the query. This is called a *table alias*.

To create a table alias, write

```
FROM table_reference AS alias
or
FROM table_reference alias
```

The AS key word is optional noise. alias can be any identifier.

A typical application of table aliases is to assign short identifiers to long table names to keep the join clauses readable. For example:

```
SELECT * FROM some_very_long_table_name s JOIN
 another_fairly_long_name a ON s.id = a.num;
```

The alias becomes the new name of the table reference so far as the current query is concerned — it is not allowed to refer to the table by the original name elsewhere in the query. Thus, this is not valid:

```
SELECT * FROM my_table AS m WHERE my_table.a > 5; -- wrong
```

Table aliases are mainly for notational convenience, but it is necessary to use them when joining a table to itself, e.g.:

```
SELECT * FROM people AS mother JOIN people AS child ON mother.id =
 child.mother_id;
```

Additionally, an alias is required if the table reference is a subquery (see [Section 7.2.1.3](#page-155-0)).

Parentheses are used to resolve ambiguities. In the following example, the first statement assigns the alias b to the second instance of my\_table, but the second statement assigns the alias to the result of the join:

```
SELECT * FROM my_table AS a CROSS JOIN my_table AS b ...
SELECT * FROM (my_table AS a CROSS JOIN my_table) AS b ...
```

Another form of table aliasing gives temporary names to the columns of the table, as well as the table itself:

```
FROM table_reference [AS] alias ( column1 [, column2 [, ...]] )
```

If fewer column aliases are specified than the actual table has columns, the remaining columns are not renamed. This syntax is especially useful for self-joins or subqueries.

When an alias is applied to the output of a JOIN clause, the alias hides the original name(s) within the JOIN. For example:

```
SELECT a.* FROM my_table AS a JOIN your_table AS b ON ...
is valid SQL, but:
SELECT a.* FROM (my_table AS a JOIN your_table AS b ON ...) AS c
is not valid; the table alias a is not visible outside the alias c.
```

### <span id="page-155-0"></span>**7.2.1.3. Subqueries**

Subqueries specifying a derived table must be enclosed in parentheses and *must* be assigned a table alias name (as in [Section 7.2.1.2](#page-154-0)). For example:

```
FROM (SELECT * FROM table1) AS alias_name
```

This example is equivalent to FROM table1 AS alias\_name. More interesting cases, which cannot be reduced to a plain join, arise when the subquery involves grouping or aggregation.

A subquery can also be a VALUES list:

```
FROM (VALUES ('anne', 'smith'), ('bob', 'jones'), ('joe', 'blow'))
 AS names(first, last)
```

Again, a table alias is required. Assigning alias names to the columns of the VALUES list is optional, but is good practice. For more information see [Section 7.7](#page-169-1).

#### **7.2.1.4. Table Functions**

Table functions are functions that produce a set of rows, made up of either base data types (scalar types) or composite data types (table rows). They are used like a table, view, or subquery in the FROM clause of a query. Columns returned by table functions can be included in SELECT, JOIN, or WHERE clauses in the same manner as columns of a table, view, or subquery.

Table functions may also be combined using the ROWS FROM syntax, with the results returned in parallel columns; the number of result rows in this case is that of the largest function result, with smaller results padded with null values to match.

```
function_call [WITH ORDINALITY] [[AS] table_alias [(column_alias
 [, ... ])]]
ROWS FROM( function_call [, ... ] ) [WITH ORDINALITY]
 [[AS] table_alias [(column_alias [, ... ])]]
```

If the WITH ORDINALITY clause is specified, an additional column of type bigint will be added to the function result columns. This column numbers the rows of the function result set, starting from 1. (This is a generalization of the SQL-standard syntax for UNNEST ... WITH ORDINALITY.) By default, the ordinal column is called ordinality, but a different column name can be assigned to it using an AS clause.

The special table function UNNEST may be called with any number of array parameters, and it returns a corresponding number of columns, as if UNNEST (Section 9.19) had been called on each parameter separately and combined using the ROWS FROM construct.

```
UNNEST( array_expression [, ... ] ) [WITH ORDINALITY]
 [[AS] table_alias [(column_alias [, ... ])]]
```

If no table\_alias is specified, the function name is used as the table name; in the case of a ROWS FROM() construct, the first function's name is used.

If column aliases are not supplied, then for a function returning a base data type, the column name is also the same as the function name. For a function returning a composite type, the result columns get the names of the individual attributes of the type.

Some examples:

```
CREATE TABLE foo (fooid int, foosubid int, fooname text);
CREATE FUNCTION getfoo(int) RETURNS SETOF foo AS $$
 SELECT * FROM foo WHERE fooid = $1;
$$ LANGUAGE SQL;
SELECT * FROM getfoo(1) AS t1;
SELECT * FROM foo
 WHERE foosubid IN (
 SELECT foosubid
 FROM getfoo(foo.fooid) z
 WHERE z.fooid = foo.fooid
 );
CREATE VIEW vw_getfoo AS SELECT * FROM getfoo(1);
SELECT * FROM vw_getfoo;
```

In some cases it is useful to define table functions that can return different column sets depending on how they are invoked. To support this, the table function can be declared as returning the pseudo-type record with no OUT parameters. When such a function is used in a query, the expected row structure must be specified in the query itself, so that the system can know how to parse and plan the query. This syntax looks like:

```
function_call [AS] alias (column_definition [, ... ])
function_call AS [alias] (column_definition [, ... ])
ROWS FROM( ... function_call AS (column_definition [, ... ])
 [, ... ] )
```

When not using the ROWS FROM() syntax, the column\_definition list replaces the column alias list that could otherwise be attached to the FROM item; the names in the column definitions serve as column aliases. When using the ROWS FROM() syntax, a column\_definition list can be attached to each member function separately; or if there is only one member function and no WITH ORDINALITY clause, a column\_definition list can be written in place of a column alias list following ROWS FROM().

Consider this example:

```
SELECT *
```

```
 FROM dblink('dbname=mydb', 'SELECT proname, prosrc FROM
 pg_proc')
 AS t1(proname name, prosrc text)
 WHERE proname LIKE 'bytea%';
```

The dblink function (part of the dblink module) executes a remote query. It is declared to return record since it might be used for any kind of query. The actual column set must be specified in the calling query so that the parser knows, for example, what \* should expand to.

This example uses ROWS FROM:

```
SELECT *
FROM ROWS FROM
 (
 json_to_recordset('[{"a":40,"b":"foo"},
{"a":"100","b":"bar"}]')
 AS (a INTEGER, b TEXT),
 generate_series(1, 3)
 ) AS x (p, q, s)
ORDER BY p;
 p | q | s
-----+-----+---
 40 | foo | 1
 100 | bar | 2
 | | 3
```

It joins two functions into a single FROM target. json\_to\_recordset() is instructed to return two columns, the first integer and the second text. The result of generate\_series() is used directly. The ORDER BY clause sorts the column values as integers.

### **7.2.1.5. LATERAL Subqueries**

Subqueries appearing in FROM can be preceded by the key word LATERAL. This allows them to reference columns provided by preceding FROM items. (Without LATERAL, each subquery is evaluated independently and so cannot cross-reference any other FROM item.)

Table functions appearing in FROM can also be preceded by the key word LATERAL, but for functions the key word is optional; the function's arguments can contain references to columns provided by preceding FROM items in any case.

A LATERAL item can appear at the top level in the FROM list, or within a JOIN tree. In the latter case it can also refer to any items that are on the left-hand side of a JOIN that it is on the right-hand side of.

When a FROM item contains LATERAL cross-references, evaluation proceeds as follows: for each row of the FROM item providing the cross-referenced column(s), or set of rows of multiple FROM items providing the columns, the LATERAL item is evaluated using that row or row set's values of the columns. The resulting row(s) are joined as usual with the rows they were computed from. This is repeated for each row or set of rows from the column source table(s).

A trivial example of LATERAL is

```
SELECT * FROM foo, LATERAL (SELECT * FROM bar WHERE bar.id =
 foo.bar_id) ss;
```

This is not especially useful since it has exactly the same result as the more conventional

```
SELECT * FROM foo, bar WHERE bar.id = foo.bar_id;
```

LATERAL is primarily useful when the cross-referenced column is necessary for computing the row(s) to be joined. A common application is providing an argument value for a set-returning function. For example, supposing that vertices(polygon) returns the set of vertices of a polygon, we could identify close-together vertices of polygons stored in a table with:

```
SELECT p1.id, p2.id, v1, v2
FROM polygons p1, polygons p2,
 LATERAL vertices(p1.poly) v1,
 LATERAL vertices(p2.poly) v2
WHERE (v1 <-> v2) < 10 AND p1.id != p2.id;
```

This query could also be written

```
SELECT p1.id, p2.id, v1, v2
FROM polygons p1 CROSS JOIN LATERAL vertices(p1.poly) v1,
 polygons p2 CROSS JOIN LATERAL vertices(p2.poly) v2
WHERE (v1 <-> v2) < 10 AND p1.id != p2.id;
```

or in several other equivalent formulations. (As already mentioned, the LATERAL key word is unnecessary in this example, but we use it for clarity.)

It is often particularly handy to LEFT JOIN to a LATERAL subquery, so that source rows will appear in the result even if the LATERAL subquery produces no rows for them. For example, if get\_product\_names() returns the names of products made by a manufacturer, but some manufacturers in our table currently produce no products, we could find out which ones those are like this:

```
SELECT m.name
FROM manufacturers m LEFT JOIN LATERAL get_product_names(m.id)
 pname ON true
WHERE pname IS NULL;
```

## <span id="page-158-0"></span>**7.2.2. The WHERE Clause**

The syntax of the WHERE clause is

```
WHERE search_condition
```

where search\_condition is any value expression (see [Section 4.2\)](#page-79-0) that returns a value of type boolean.

After the processing of the FROM clause is done, each row of the derived virtual table is checked against the search condition. If the result of the condition is true, the row is kept in the output table, otherwise (i.e., if the result is false or null) it is discarded. The search condition typically references at least one column of the table generated in the FROM clause; this is not required, but otherwise the WHERE clause will be fairly useless.

#### **Note**

The join condition of an inner join can be written either in the WHERE clause or in the JOIN clause. For example, these table expressions are equivalent:

```
FROM a, b WHERE a.id = b.id AND b.val > 5
```

and:

```
FROM a INNER JOIN b ON (a.id = b.id) WHERE b.val > 5
or perhaps even:
```

FROM a NATURAL JOIN b WHERE b.val > 5

Which one of these you use is mainly a matter of style. The JOIN syntax in the FROM clause is probably not as portable to other SQL database management systems, even though it is in the SQL standard. For outer joins there is no choice: they must be done in the FROM clause. The ON or USING clause of an outer join is *not* equivalent to a WHERE condition, because it results in the addition of rows (for unmatched input rows) as well as the removal of rows in the final result.

Here are some examples of WHERE clauses:

```
SELECT ... FROM fdt WHERE c1 > 5
SELECT ... FROM fdt WHERE c1 IN (1, 2, 3)
SELECT ... FROM fdt WHERE c1 IN (SELECT c1 FROM t2)
SELECT ... FROM fdt WHERE c1 IN (SELECT c3 FROM t2 WHERE c2 =
 fdt.c1 + 10)
SELECT ... FROM fdt WHERE c1 BETWEEN (SELECT c3 FROM t2 WHERE c2 =
 fdt.c1 + 10) AND 100
SELECT ... FROM fdt WHERE EXISTS (SELECT c1 FROM t2 WHERE c2 >
 fdt.c1)
```

fdt is the table derived in the FROM clause. Rows that do not meet the search condition of the WHERE clause are eliminated from fdt. Notice the use of scalar subqueries as value expressions. Just like any other query, the subqueries can employ complex table expressions. Notice also how fdt is referenced in the subqueries. Qualifying c1 as fdt.c1 is only necessary if c1 is also the name of a column in the derived input table of the subquery. But qualifying the column name adds clarity even when it is not needed. This example shows how the column naming scope of an outer query extends into its inner queries.

## <span id="page-159-0"></span>**7.2.3. The GROUP BY and HAVING Clauses**

After passing the WHERE filter, the derived input table might be subject to grouping, using the GROUP BY clause, and elimination of group rows using the HAVING clause.

```
SELECT select_list
 FROM ...
 [WHERE ...]
 GROUP BY grouping_column_reference
 [, grouping_column_reference]...
```

The GROUP BY clause is used to group together those rows in a table that have the same values in all the columns listed. The order in which the columns are listed does not matter. The effect is to combine each set of rows having common values into one group row that represents all rows in the group. This is done to eliminate redundancy in the output and/or compute aggregates that apply to these groups. For instance:

```
=> SELECT * FROM test1;
 x | y
---+---
 a | 3
 c | 2
 b | 5
 a | 1
(4 rows)
=> SELECT x FROM test1 GROUP BY x;
 x
---
 a
 b
 c
(3 rows)
```

In the second query, we could not have written SELECT \* FROM test1 GROUP BY x, because there is no single value for the column y that could be associated with each group. The grouped-by columns can be referenced in the select list since they have a single value in each group.

In general, if a table is grouped, columns that are not listed in GROUP BY cannot be referenced except in aggregate expressions. An example with aggregate expressions is:

```
=> SELECT x, sum(y) FROM test1 GROUP BY x;
 x | sum
---+-----
 a | 4
 b | 5
 c | 2
(3 rows)
```

Here sum is an aggregate function that computes a single value over the entire group. More information about the available aggregate functions can be found in Section 9.21.

#### **Tip**

Grouping without aggregate expressions effectively calculates the set of distinct values in a column. This can also be achieved using the DISTINCT clause (see [Section 7.3.3](#page-166-1)).

Here is another example: it calculates the total sales for each product (rather than the total sales of all products):

```
SELECT product_id, p.name, (sum(s.units) * p.price) AS sales
 FROM products p LEFT JOIN sales s USING (product_id)
 GROUP BY product_id, p.name, p.price;
```

In this example, the columns product\_id, p.name, and p.price must be in the GROUP BY clause since they are referenced in the query select list (but see below). The column s.units does not have to be in the GROUP BY list since it is only used in an aggregate expression (sum(...)), which represents the sales of a product. For each product, the query returns a summary row about all sales of the product.

If the products table is set up so that, say, product\_id is the primary key, then it would be enough to group by product\_id in the above example, since name and price would be *functionally dependent* on the product ID, and so there would be no ambiguity about which name and price value to return for each product ID group.

In strict SQL, GROUP BY can only group by columns of the source table but PostgreSQL extends this to also allow GROUP BY to group by columns in the select list. Grouping by value expressions instead of simple column names is also allowed.

If a table has been grouped using GROUP BY, but only certain groups are of interest, the HAVING clause can be used, much like a WHERE clause, to eliminate groups from the result. The syntax is:

```
SELECT select_list FROM ... [WHERE ...] GROUP BY ...
 HAVING boolean_expression
```

Expressions in the HAVING clause can refer both to grouped expressions and to ungrouped expressions (which necessarily involve an aggregate function).

#### Example:

```
=> SELECT x, sum(y) FROM test1 GROUP BY x HAVING sum(y) > 3;
 x | sum
---+-----
 a | 4
 b | 5
(2 rows)
=> SELECT x, sum(y) FROM test1 GROUP BY x HAVING x < 'c';
 x | sum
---+-----
 a | 4
 b | 5
(2 rows)
```

Again, a more realistic example:

```
SELECT product_id, p.name, (sum(s.units) * (p.price - p.cost)) AS
 profit
 FROM products p LEFT JOIN sales s USING (product_id)
 WHERE s.date > CURRENT_DATE - INTERVAL '4 weeks'
 GROUP BY product_id, p.name, p.price, p.cost
 HAVING sum(p.price * s.units) > 5000;
```

In the example above, the WHERE clause is selecting rows by a column that is not grouped (the expression is only true for sales during the last four weeks), while the HAVING clause restricts the output to groups with total gross sales over 5000. Note that the aggregate expressions do not necessarily need to be the same in all parts of the query.

If a query contains aggregate function calls, but no GROUP BY clause, grouping still occurs: the result is a single group row (or perhaps no rows at all, if the single row is then eliminated by HAVING). The same is true if it contains a HAVING clause, even without any aggregate function calls or GROUP BY clause.

## <span id="page-162-0"></span>**7.2.4. GROUPING SETS, CUBE, and ROLLUP**

More complex grouping operations than those described above are possible using the concept of *grouping sets*. The data selected by the FROM and WHERE clauses is grouped separately by each specified grouping set, aggregates computed for each group just as for simple GROUP BY clauses, and then the results returned. For example:

#### => **SELECT \* FROM items\_sold;** brand | size | sales -------+------+------- Foo | L | 10 Foo | M | 20 Bar | M | 15 Bar | L | 5 (4 rows)

=> **SELECT brand, size, sum(sales) FROM items\_sold GROUP BY GROUPING SETS ((brand), (size), ());**

```
 brand | size | sum
-------+------+-----
 Foo | | 30
 Bar | | 20
 | L | 15
 | M | 35
 | | 50
(5 rows)
```

Each sublist of GROUPING SETS may specify zero or more columns or expressions and is interpreted the same way as though it were directly in the GROUP BY clause. An empty grouping set means that all rows are aggregated down to a single group (which is output even if no input rows were present), as described above for the case of aggregate functions with no GROUP BY clause.

References to the grouping columns or expressions are replaced by null values in result rows for grouping sets in which those columns do not appear. To distinguish which grouping a particular output row resulted from, see Table 9.61.

A shorthand notation is provided for specifying two common types of grouping set. A clause of the form

```
ROLLUP ( e1, e2, e3, ... )
```

represents the given list of expressions and all prefixes of the list including the empty list; thus it is equivalent to

```
GROUPING SETS (
 ( e1, e2, e3, ... ),
 ...
 ( e1, e2 ),
 ( e1 ),
 ( )
)
```

This is commonly used for analysis over hierarchical data; e.g., total salary by department, division, and company-wide total.

A clause of the form

```
CUBE ( e1, e2, ... )
```

represents the given list and all of its possible subsets (i.e., the power set). Thus

```
CUBE ( a, b, c )
is equivalent to
GROUPING SETS (
 ( a, b, c ),
 ( a, b ),
 ( a, c ),
 ( a ),
 ( b, c ),
 ( b ),
 ( c ),
 ( )
)
```

The individual elements of a CUBE or ROLLUP clause may be either individual expressions, or sublists of elements in parentheses. In the latter case, the sublists are treated as single units for the purposes of generating the individual grouping sets. For example:

```
CUBE ( (a, b), (c, d) )
is equivalent to
GROUPING SETS (
 ( a, b, c, d ),
 ( a, b ),
 ( c, d ),
 ( )
)
and
ROLLUP ( a, (b, c), d )
is equivalent to
GROUPING SETS (
 ( a, b, c, d ),
 ( a, b, c ),
 ( a ),
 ( )
)
```

The CUBE and ROLLUP constructs can be used either directly in the GROUP BY clause, or nested inside a GROUPING SETS clause. If one GROUPING SETS clause is nested inside another, the effect is the same as if all the elements of the inner clause had been written directly in the outer clause.

If multiple grouping items are specified in a single GROUP BY clause, then the final list of grouping sets is the cross product of the individual items. For example:

```
GROUP BY a, CUBE (b, c), GROUPING SETS ((d), (e))
is equivalent to
GROUP BY GROUPING SETS (
 (a, b, c, d), (a, b, c, e),
 (a, b, d), (a, b, e),
 (a, c, d), (a, c, e),
 (a, d), (a, e)
)
```

 When specifying multiple grouping items together, the final set of grouping sets might contain duplicates. For example:

```
GROUP BY ROLLUP (a, b), ROLLUP (a, c)
is equivalent to
GROUP BY GROUPING SETS (
 (a, b, c),
 (a, b),
 (a, b),
 (a, c),
 (a),
 (a),
 (a, c),
 (a),
 ()
)
```

If these duplicates are undesirable, they can be removed using the DISTINCT clause directly on the GROUP BY. Therefore:

```
GROUP BY DISTINCT ROLLUP (a, b), ROLLUP (a, c)
is equivalent to
GROUP BY GROUPING SETS (
 (a, b, c),
 (a, b),
 (a, c),
 (a),
 ()
)
```

This is not the same as using SELECT DISTINCT because the output rows may still contain duplicates. If any of the ungrouped columns contains NULL, it will be indistinguishable from the NULL used when that same column is grouped.

#### **Note**

The construct (a, b) is normally recognized in expressions as a [row constructor](#page-90-0). Within the GROUP BY clause, this does not apply at the top levels of expressions, and (a, b) is parsed as a list of expressions as described above. If for some reason you *need* a row constructor in a grouping expression, use ROW(a, b).

## <span id="page-165-1"></span>**7.2.5. Window Function Processing**

If the query contains any window functions (see [Section 3.5](#page-57-0), Section 9.22 and [Section 4.2.8\)](#page-84-0), these functions are evaluated after any grouping, aggregation, and HAVING filtering is performed. That is, if the query uses any aggregates, GROUP BY, or HAVING, then the rows seen by the window functions are the group rows instead of the original table rows from FROM/WHERE.

When multiple window functions are used, all the window functions having equivalent PARTITION BY and ORDER BY clauses in their window definitions are guaranteed to see the same ordering of the input rows, even if the ORDER BY does not uniquely determine the ordering. However, no guarantees are made about the evaluation of functions having different PARTITION BY or ORDER BY specifications. (In such cases a sort step is typically required between the passes of window function evaluations, and the sort is not guaranteed to preserve ordering of rows that its ORDER BY sees as equivalent.)

Currently, window functions always require presorted data, and so the query output will be ordered according to one or another of the window functions' PARTITION BY/ORDER BY clauses. It is not recommended to rely on this, however. Use an explicit top-level ORDER BY clause if you want to be sure the results are sorted in a particular way.

# <span id="page-165-0"></span>**7.3. Select Lists**

As shown in the previous section, the table expression in the SELECT command constructs an intermediate virtual table by possibly combining tables, views, eliminating rows, grouping, etc. This table is finally passed on to processing by the *select list*. The select list determines which *columns* of the intermediate table are actually output.

## <span id="page-165-2"></span>**7.3.1. Select-List Items**

The simplest kind of select list is \* which emits all columns that the table expression produces. Otherwise, a select list is a comma-separated list of value expressions (as defined in [Section 4.2](#page-79-0)). For instance, it could be a list of column names:

```
SELECT a, b, c FROM ...
```

The columns names a, b, and c are either the actual names of the columns of tables referenced in the FROM clause, or the aliases given to them as explained in [Section 7.2.1.2](#page-154-0). The name space available in the select list is the same as in the WHERE clause, unless grouping is used, in which case it is the same as in the HAVING clause.

If more than one table has a column of the same name, the table name must also be given, as in:

```
SELECT tbl1.a, tbl2.a, tbl1.b FROM ...
```

When working with multiple tables, it can also be useful to ask for all the columns of a particular table:

```
SELECT tbl1.*, tbl2.a FROM ...
```

See Section 8.16.5 for more about the table\_name.\* notation.

If an arbitrary value expression is used in the select list, it conceptually adds a new virtual column to the returned table. The value expression is evaluated once for each result row, with the row's values substituted for any column references. But the expressions in the select list do not have to reference any columns in the table expression of the FROM clause; they can be constant arithmetic expressions, for instance.

## <span id="page-166-0"></span>**7.3.2. Column Labels**

The entries in the select list can be assigned names for subsequent processing, such as for use in an ORDER BY clause or for display by the client application. For example:

```
SELECT a AS value, b + c AS sum FROM ...
```

If no output column name is specified using AS, the system assigns a default column name. For simple column references, this is the name of the referenced column. For function calls, this is the name of the function. For complex expressions, the system will generate a generic name.

The AS key word is usually optional, but in some cases where the desired column name matches a PostgreSQL key word, you must write AS or double-quote the column name in order to avoid ambiguity. (Appendix C shows which key words require AS to be used as a column label.) For example, FROM is one such key word, so this does not work:

```
SELECT a from, b + c AS sum FROM ...
but either of these do:
```

```
SELECT a AS from, b + c AS sum FROM ...
SELECT a "from", b + c AS sum FROM ...
```

For greatest safety against possible future key word additions, it is recommended that you always either write AS or double-quote the output column name.

#### **Note**

The naming of output columns here is different from that done in the FROM clause (see [Sec](#page-154-0)[tion 7.2.1.2](#page-154-0)). It is possible to rename the same column twice, but the name assigned in the select list is the one that will be passed on.

## <span id="page-166-1"></span>**7.3.3. DISTINCT**

After the select list has been processed, the result table can optionally be subject to the elimination of duplicate rows. The DISTINCT key word is written directly after SELECT to specify this:

```
SELECT DISTINCT select_list ...
```

(Instead of DISTINCT the key word ALL can be used to specify the default behavior of retaining all rows.)

Obviously, two rows are considered distinct if they differ in at least one column value. Null values are considered equal in this comparison.

Alternatively, an arbitrary expression can determine what rows are to be considered distinct:

```
SELECT DISTINCT ON (expression [, expression ...]) select_list ...
```

Here expression is an arbitrary value expression that is evaluated for all rows. A set of rows for which all the expressions are equal are considered duplicates, and only the first row of the set is kept in the output. Note that the "first row" of a set is unpredictable unless the query is sorted on enough columns to guarantee a unique ordering of the rows arriving at the DISTINCT filter. (DISTINCT ON processing occurs after ORDER BY sorting.)

The DISTINCT ON clause is not part of the SQL standard and is sometimes considered bad style because of the potentially indeterminate nature of its results. With judicious use of GROUP BY and subqueries in FROM, this construct can be avoided, but it is often the most convenient alternative.

# <span id="page-167-0"></span>**7.4. Combining Queries (UNION, INTERSECT, EXCEPT)**

The results of two queries can be combined using the set operations union, intersection, and difference. The syntax is

```
query1 UNION [ALL] query2
query1 INTERSECT [ALL] query2
query1 EXCEPT [ALL] query2
```

where query1 and query2 are queries that can use any of the features discussed up to this point.

UNION effectively appends the result of query2 to the result of query1 (although there is no guarantee that this is the order in which the rows are actually returned). Furthermore, it eliminates duplicate rows from its result, in the same way as DISTINCT, unless UNION ALL is used.

INTERSECT returns all rows that are both in the result of query1 and in the result of query2. Duplicate rows are eliminated unless INTERSECT ALL is used.

EXCEPT returns all rows that are in the result of query1 but not in the result of query2. (This is sometimes called the *difference* between two queries.) Again, duplicates are eliminated unless EX-CEPT ALL is used.

In order to calculate the union, intersection, or difference of two queries, the two queries must be "union compatible", which means that they return the same number of columns and the corresponding columns have compatible data types, as described in Section 10.5.

Set operations can be combined, for example

```
query1 UNION query2 EXCEPT query3
which is equivalent to
(query1 UNION query2) EXCEPT query3
```

As shown here, you can use parentheses to control the order of evaluation. Without parentheses, UNION and EXCEPT associate left-to-right, but INTERSECT binds more tightly than those two operators. Thus

```
query1 UNION query2 INTERSECT query3
```

means

```
query1 UNION (query2 INTERSECT query3)
```

You can also surround an individual query with parentheses. This is important if the query needs to use any of the clauses discussed in following sections, such as LIMIT. Without parentheses, you'll get a syntax error, or else the clause will be understood as applying to the output of the set operation rather than one of its inputs. For example,

```
SELECT a FROM b UNION SELECT x FROM y LIMIT 10
is accepted, but it means
(SELECT a FROM b UNION SELECT x FROM y) LIMIT 10
not
SELECT a FROM b UNION (SELECT x FROM y LIMIT 10)
```

# <span id="page-168-0"></span>**7.5. Sorting Rows (ORDER BY)**

After a query has produced an output table (after the select list has been processed) it can optionally be sorted. If sorting is not chosen, the rows will be returned in an unspecified order. The actual order in that case will depend on the scan and join plan types and the order on disk, but it must not be relied on. A particular output ordering can only be guaranteed if the sort step is explicitly chosen.

The ORDER BY clause specifies the sort order:

```
SELECT select_list
 FROM table_expression
 ORDER BY sort_expression1 [ASC | DESC] [NULLS { FIRST | LAST }]
 [, sort_expression2 [ASC | DESC] [NULLS { FIRST |
 LAST }] ...]
```

The sort expression(s) can be any expression that would be valid in the query's select list. An example is:

```
SELECT a, b FROM table1 ORDER BY a + b, c;
```

When more than one expression is specified, the later values are used to sort rows that are equal according to the earlier values. Each expression can be followed by an optional ASC or DESC keyword to set the sort direction to ascending or descending. ASC order is the default. Ascending order puts smaller values first, where "smaller" is defined in terms of the < operator. Similarly, descending order is determined with the > operator. <sup>1</sup>

The NULLS FIRST and NULLS LAST options can be used to determine whether nulls appear before or after non-null values in the sort ordering. By default, null values sort as if larger than any non-null value; that is, NULLS FIRST is the default for DESC order, and NULLS LAST otherwise.

Note that the ordering options are considered independently for each sort column. For example ORDER BY x, y DESC means ORDER BY x ASC, y DESC, which is not the same as ORDER BY x DESC, y DESC.

Actually, PostgreSQL uses the *default B-tree operator class* for the expression's data type to determine the sort ordering for ASC and DESC. Conventionally, data types will be set up so that the < and > operators correspond to this sort ordering, but a user-defined data type's designer could choose to do something different.

A sort\_expression can also be the column label or number of an output column, as in:

```
SELECT a + b AS sum, c FROM table1 ORDER BY sum;
SELECT a, max(b) FROM table1 GROUP BY a ORDER BY 1;
```

both of which sort by the first output column. Note that an output column name has to stand alone, that is, it cannot be used in an expression — for example, this is *not* correct:

```
SELECT a + b AS sum, c FROM table1 ORDER BY sum + c; --
 wrong
```

This restriction is made to reduce ambiguity. There is still ambiguity if an ORDER BY item is a simple name that could match either an output column name or a column from the table expression. The output column is used in such cases. This would only cause confusion if you use AS to rename an output column to match some other table column's name.

ORDER BY can be applied to the result of a UNION, INTERSECT, or EXCEPT combination, but in this case it is only permitted to sort by output column names or numbers, not by expressions.

# <span id="page-169-0"></span>**7.6. LIMIT and OFFSET**

LIMIT and OFFSET allow you to retrieve just a portion of the rows that are generated by the rest of the query:

```
SELECT select_list
 FROM table_expression
 [ ORDER BY ... ]
 [ LIMIT { number | ALL } ] [ OFFSET number ]
```

If a limit count is given, no more than that many rows will be returned (but possibly fewer, if the query itself yields fewer rows). LIMIT ALL is the same as omitting the LIMIT clause, as is LIMIT with a NULL argument.

OFFSET says to skip that many rows before beginning to return rows. OFFSET 0 is the same as omitting the OFFSET clause, as is OFFSET with a NULL argument.

If both OFFSET and LIMIT appear, then OFFSET rows are skipped before starting to count the LIMIT rows that are returned.

When using LIMIT, it is important to use an ORDER BY clause that constrains the result rows into a unique order. Otherwise you will get an unpredictable subset of the query's rows. You might be asking for the tenth through twentieth rows, but tenth through twentieth in what ordering? The ordering is unknown, unless you specified ORDER BY.

The query optimizer takes LIMIT into account when generating query plans, so you are very likely to get different plans (yielding different row orders) depending on what you give for LIMIT and OFFSET. Thus, using different LIMIT/OFFSET values to select different subsets of a query result *will give inconsistent results* unless you enforce a predictable result ordering with ORDER BY. This is not a bug; it is an inherent consequence of the fact that SQL does not promise to deliver the results of a query in any particular order unless ORDER BY is used to constrain the order.

The rows skipped by an OFFSET clause still have to be computed inside the server; therefore a large OFFSET might be inefficient.

# <span id="page-169-1"></span>**7.7. VALUES Lists**

VALUES provides a way to generate a "constant table" that can be used in a query without having to actually create and populate a table on-disk. The syntax is

```
VALUES ( expression [, ...] ) [, ...]
```

Each parenthesized list of expressions generates a row in the table. The lists must all have the same number of elements (i.e., the number of columns in the table), and corresponding entries in each list must have compatible data types. The actual data type assigned to each column of the result is determined using the same rules as for UNION (see Section 10.5).

As an example:

```
VALUES (1, 'one'), (2, 'two'), (3, 'three');
```

will return a table of two columns and three rows. It's effectively equivalent to:

```
SELECT 1 AS column1, 'one' AS column2
UNION ALL
SELECT 2, 'two'
UNION ALL
SELECT 3, 'three';
```

By default, PostgreSQL assigns the names column1, column2, etc. to the columns of a VALUES table. The column names are not specified by the SQL standard and different database systems do it differently, so it's usually better to override the default names with a table alias list, like this:

```
=> SELECT * FROM (VALUES (1, 'one'), (2, 'two'), (3, 'three')) AS t
 (num,letter);
 num | letter
-----+--------
 1 | one
 2 | two
 3 | three
(3 rows)
```

Syntactically, VALUES followed by expression lists is treated as equivalent to:

```
SELECT select_list FROM table_expression
```

and can appear anywhere a SELECT can. For example, you can use it as part of a UNION, or attach a sort\_specification (ORDER BY, LIMIT, and/or OFFSET) to it. VALUES is most commonly used as the data source in an INSERT command, and next most commonly as a subquery.

For more information see VALUES.

# <span id="page-170-0"></span>**7.8. WITH Queries (Common Table Expressions)**

WITH provides a way to write auxiliary statements for use in a larger query. These statements, which are often referred to as Common Table Expressions or CTEs, can be thought of as defining temporary tables that exist just for one query. Each auxiliary statement in a WITH clause can be a SELECT, INSERT, UPDATE, or DELETE; and the WITH clause itself is attached to a primary statement that can also be a SELECT, INSERT, UPDATE, or DELETE.

## <span id="page-171-0"></span>**7.8.1. SELECT in WITH**

The basic value of SELECT in WITH is to break down complicated queries into simpler parts. An example is:

```
WITH regional_sales AS (
 SELECT region, SUM(amount) AS total_sales
 FROM orders
 GROUP BY region
), top_regions AS (
 SELECT region
 FROM regional_sales
 WHERE total_sales > (SELECT SUM(total_sales)/10 FROM
 regional_sales)
)
SELECT region,
 product,
 SUM(quantity) AS product_units,
 SUM(amount) AS product_sales
FROM orders
WHERE region IN (SELECT region FROM top_regions)
GROUP BY region, product;
```

which displays per-product sales totals in only the top sales regions. The WITH clause defines two auxiliary statements named regional\_sales and top\_regions, where the output of regional\_sales is used in top\_regions and the output of top\_regions is used in the primary SELECT query. This example could have been written without WITH, but we'd have needed two levels of nested sub-SELECTs. It's a bit easier to follow this way.

## <span id="page-171-1"></span>**7.8.2. Recursive Queries**

 The optional RECURSIVE modifier changes WITH from a mere syntactic convenience into a feature that accomplishes things not otherwise possible in standard SQL. Using RECURSIVE, a WITH query can refer to its own output. A very simple example is this query to sum the integers from 1 through 100:

```
WITH RECURSIVE t(n) AS (
 VALUES (1)
 UNION ALL
 SELECT n+1 FROM t WHERE n < 100
)
SELECT sum(n) FROM t;
```

The general form of a recursive WITH query is always a *non-recursive term*, then UNION (or UNION ALL), then a *recursive term*, where only the recursive term can contain a reference to the query's own output. Such a query is executed as follows:

#### **Recursive Query Evaluation**

- 1. Evaluate the non-recursive term. For UNION (but not UNION ALL), discard duplicate rows. Include all remaining rows in the result of the recursive query, and also place them in a temporary *working table*.
- 2. So long as the working table is not empty, repeat these steps:
  - a. Evaluate the recursive term, substituting the current contents of the working table for the recursive self-reference. For UNION (but not UNION ALL), discard duplicate rows and

rows that duplicate any previous result row. Include all remaining rows in the result of the recursive query, and also place them in a temporary *intermediate table*.

b. Replace the contents of the working table with the contents of the intermediate table, then empty the intermediate table.

#### **Note**

While RECURSIVE allows queries to be specified recursively, internally such queries are evaluated iteratively.

In the example above, the working table has just a single row in each step, and it takes on the values from 1 through 100 in successive steps. In the 100th step, there is no output because of the WHERE clause, and so the query terminates.

Recursive queries are typically used to deal with hierarchical or tree-structured data. A useful example is this query to find all the direct and indirect sub-parts of a product, given only a table that shows immediate inclusions:

```
WITH RECURSIVE included_parts(sub_part, part, quantity) AS (
 SELECT sub_part, part, quantity FROM parts WHERE part =
 'our_product'
 UNION ALL
 SELECT p.sub_part, p.part, p.quantity * pr.quantity
 FROM included_parts pr, parts p
 WHERE p.part = pr.sub_part
)
SELECT sub_part, SUM(quantity) as total_quantity
FROM included_parts
GROUP BY sub_part
```

#### **7.8.2.1. Search Order**

When computing a tree traversal using a recursive query, you might want to order the results in either depth-first or breadth-first order. This can be done by computing an ordering column alongside the other data columns and using that to sort the results at the end. Note that this does not actually control in which order the query evaluation visits the rows; that is as always in SQL implementation-dependent. This approach merely provides a convenient way to order the results afterwards.

To create a depth-first order, we compute for each result row an array of rows that we have visited so far. For example, consider the following query that searches a table tree using a link field:

```
WITH RECURSIVE search_tree(id, link, data) AS (
 SELECT t.id, t.link, t.data
 FROM tree t
 UNION ALL
 SELECT t.id, t.link, t.data
 FROM tree t, search_tree st
 WHERE t.id = st.link
)
SELECT * FROM search_tree;
```

To add depth-first ordering information, you can write this:

```
WITH RECURSIVE search_tree(id, link, data, path) AS (
 SELECT t.id, t.link, t.data, ARRAY[t.id]
 FROM tree t
 UNION ALL
 SELECT t.id, t.link, t.data, path || t.id
 FROM tree t, search_tree st
 WHERE t.id = st.link
)
SELECT * FROM search_tree ORDER BY path;
```

In the general case where more than one field needs to be used to identify a row, use an array of rows. For example, if we needed to track fields f1 and f2:

```
WITH RECURSIVE search_tree(id, link, data, path) AS (
 SELECT t.id, t.link, t.data, ARRAY[ROW(t.f1, t.f2)]
 FROM tree t
 UNION ALL
 SELECT t.id, t.link, t.data, path || ROW(t.f1, t.f2)
 FROM tree t, search_tree st
 WHERE t.id = st.link
)
SELECT * FROM search_tree ORDER BY path;
```

#### **Tip**

Omit the ROW() syntax in the common case where only one field needs to be tracked. This allows a simple array rather than a composite-type array to be used, gaining efficiency.

To create a breadth-first order, you can add a column that tracks the depth of the search, for example:

```
WITH RECURSIVE search_tree(id, link, data, depth) AS (
 SELECT t.id, t.link, t.data, 0
 FROM tree t
 UNION ALL
 SELECT t.id, t.link, t.data, depth + 1
 FROM tree t, search_tree st
 WHERE t.id = st.link
)
SELECT * FROM search_tree ORDER BY depth;
```

To get a stable sort, add data columns as secondary sorting columns.

#### **Tip**

The recursive query evaluation algorithm produces its output in breadth-first search order. However, this is an implementation detail and it is perhaps unsound to rely on it. The order of the rows within each level is certainly undefined, so some explicit ordering might be desired in any case.

There is built-in syntax to compute a depth- or breadth-first sort column. For example:

```
WITH RECURSIVE search_tree(id, link, data) AS (
```

```
 SELECT t.id, t.link, t.data
 FROM tree t
 UNION ALL
 SELECT t.id, t.link, t.data
 FROM tree t, search_tree st
 WHERE t.id = st.link
) SEARCH DEPTH FIRST BY id SET ordercol
SELECT * FROM search_tree ORDER BY ordercol;
WITH RECURSIVE search_tree(id, link, data) AS (
 SELECT t.id, t.link, t.data
 FROM tree t
 UNION ALL
 SELECT t.id, t.link, t.data
 FROM tree t, search_tree st
 WHERE t.id = st.link
) SEARCH BREADTH FIRST BY id SET ordercol
SELECT * FROM search_tree ORDER BY ordercol;
```

This syntax is internally expanded to something similar to the above hand-written forms. The SEARCH clause specifies whether depth- or breadth first search is wanted, the list of columns to track for sorting, and a column name that will contain the result data that can be used for sorting. That column will implicitly be added to the output rows of the CTE.

### **7.8.2.2. Cycle Detection**

When working with recursive queries it is important to be sure that the recursive part of the query will eventually return no tuples, or else the query will loop indefinitely. Sometimes, using UNION instead of UNION ALL can accomplish this by discarding rows that duplicate previous output rows. However, often a cycle does not involve output rows that are completely duplicate: it may be necessary to check just one or a few fields to see if the same point has been reached before. The standard method for handling such situations is to compute an array of the already-visited values. For example, consider again the following query that searches a table graph using a link field:

```
WITH RECURSIVE search_graph(id, link, data, depth) AS (
 SELECT g.id, g.link, g.data, 0
 FROM graph g
 UNION ALL
 SELECT g.id, g.link, g.data, sg.depth + 1
 FROM graph g, search_graph sg
 WHERE g.id = sg.link
)
SELECT * FROM search_graph;
```

This query will loop if the link relationships contain cycles. Because we require a "depth" output, just changing UNION ALL to UNION would not eliminate the looping. Instead we need to recognize whether we have reached the same row again while following a particular path of links. We add two columns is\_cycle and path to the loop-prone query:

```
WITH RECURSIVE search_graph(id, link, data, depth, is_cycle, path)
 AS (
 SELECT g.id, g.link, g.data, 0,
 false,
 ARRAY[g.id]
 FROM graph g
 UNION ALL
 SELECT g.id, g.link, g.data, sg.depth + 1,
```

```
 g.id = ANY(path),
 path || g.id
 FROM graph g, search_graph sg
 WHERE g.id = sg.link AND NOT is_cycle
)
SELECT * FROM search_graph;
```

Aside from preventing cycles, the array value is often useful in its own right as representing the "path" taken to reach any particular row.

In the general case where more than one field needs to be checked to recognize a cycle, use an array of rows. For example, if we needed to compare fields f1 and f2:

```
WITH RECURSIVE search_graph(id, link, data, depth, is_cycle, path)
 AS (
 SELECT g.id, g.link, g.data, 0,
 false,
 ARRAY[ROW(g.f1, g.f2)]
 FROM graph g
 UNION ALL
 SELECT g.id, g.link, g.data, sg.depth + 1,
 ROW(g.f1, g.f2) = ANY(path),
 path || ROW(g.f1, g.f2)
 FROM graph g, search_graph sg
 WHERE g.id = sg.link AND NOT is_cycle
)
SELECT * FROM search_graph;
```

#### **Tip**

Omit the ROW() syntax in the common case where only one field needs to be checked to recognize a cycle. This allows a simple array rather than a composite-type array to be used, gaining efficiency.

There is built-in syntax to simplify cycle detection. The above query can also be written like this:

```
WITH RECURSIVE search_graph(id, link, data, depth) AS (
 SELECT g.id, g.link, g.data, 1
 FROM graph g
 UNION ALL
 SELECT g.id, g.link, g.data, sg.depth + 1
 FROM graph g, search_graph sg
 WHERE g.id = sg.link
) CYCLE id SET is_cycle USING path
SELECT * FROM search_graph;
```

and it will be internally rewritten to the above form. The CYCLE clause specifies first the list of columns to track for cycle detection, then a column name that will show whether a cycle has been detected, and finally the name of another column that will track the path. The cycle and path columns will implicitly be added to the output rows of the CTE.

#### **Tip**

The cycle path column is computed in the same way as the depth-first ordering column show in the previous section. A query can have both a SEARCH and a CYCLE clause, but a depth-first search specification and a cycle detection specification would create redundant computations, so it's more efficient to just use the CYCLE clause and order by the path column. If breadthfirst ordering is wanted, then specifying both SEARCH and CYCLE can be useful.

A helpful trick for testing queries when you are not certain if they might loop is to place a LIMIT in the parent query. For example, this query would loop forever without the LIMIT:

```
WITH RECURSIVE t(n) AS (
 SELECT 1
 UNION ALL
 SELECT n+1 FROM t
)
SELECT n FROM t LIMIT 100;
```

This works because PostgreSQL's implementation evaluates only as many rows of a WITH query as are actually fetched by the parent query. Using this trick in production is not recommended, because other systems might work differently. Also, it usually won't work if you make the outer query sort the recursive query's results or join them to some other table, because in such cases the outer query will usually try to fetch all of the WITH query's output anyway.

## <span id="page-176-0"></span>**7.8.3. Common Table Expression Materialization**

A useful property of WITH queries is that they are normally evaluated only once per execution of the parent query, even if they are referred to more than once by the parent query or sibling WITH queries. Thus, expensive calculations that are needed in multiple places can be placed within a WITH query to avoid redundant work. Another possible application is to prevent unwanted multiple evaluations of functions with side-effects. However, the other side of this coin is that the optimizer is not able to push restrictions from the parent query down into a multiply-referenced WITH query, since that might affect all uses of the WITH query's output when it should affect only one. The multiply-referenced WITH query will be evaluated as written, without suppression of rows that the parent query might discard afterwards. (But, as mentioned above, evaluation might stop early if the reference(s) to the query demand only a limited number of rows.)

However, if a WITH query is non-recursive and side-effect-free (that is, it is a SELECT containing no volatile functions) then it can be folded into the parent query, allowing joint optimization of the two query levels. By default, this happens if the parent query references the WITH query just once, but not if it references the WITH query more than once. You can override that decision by specifying MATERIALIZED to force separate calculation of the WITH query, or by specifying NOT MATERIALIZED to force it to be merged into the parent query. The latter choice risks duplicate computation of the WITH query, but it can still give a net savings if each usage of the WITH query needs only a small part of the WITH query's full output.

A simple example of these rules is

```
WITH w AS (
 SELECT * FROM big_table
)
SELECT * FROM w WHERE key = 123;
```

This WITH query will be folded, producing the same execution plan as

```
SELECT * FROM big_table WHERE key = 123;
```

In particular, if there's an index on key, it will probably be used to fetch just the rows having key = 123. On the other hand, in

```
WITH w AS (
 SELECT * FROM big_table
)
SELECT * FROM w AS w1 JOIN w AS w2 ON w1.key = w2.ref
WHERE w2.key = 123;
```

the WITH query will be materialized, producing a temporary copy of big\_table that is then joined with itself — without benefit of any index. This query will be executed much more efficiently if written as

```
WITH w AS NOT MATERIALIZED (
 SELECT * FROM big_table
)
SELECT * FROM w AS w1 JOIN w AS w2 ON w1.key = w2.ref
WHERE w2.key = 123;
```

so that the parent query's restrictions can be applied directly to scans of big\_table.

An example where NOT MATERIALIZED could be undesirable is

```
WITH w AS (
 SELECT key, very_expensive_function(val) as f FROM some_table
)
SELECT * FROM w AS w1 JOIN w AS w2 ON w1.f = w2.f;
```

Here, materialization of the WITH query ensures that very\_expensive\_function is evaluated only once per table row, not twice.

The examples above only show WITH being used with SELECT, but it can be attached in the same way to INSERT, UPDATE, or DELETE. In each case it effectively provides temporary table(s) that can be referred to in the main command.

## <span id="page-177-0"></span>**7.8.4. Data-Modifying Statements in WITH**

You can use data-modifying statements (INSERT, UPDATE, or DELETE) in WITH. This allows you to perform several different operations in the same query. An example is:

```
WITH moved_rows AS (
 DELETE FROM products
 WHERE
 "date" >= '2010-10-01' AND
 "date" < '2010-11-01'
 RETURNING *
)
INSERT INTO products_log
SELECT * FROM moved_rows;
```

This query effectively moves rows from products to products\_log. The DELETE in WITH deletes the specified rows from products, returning their contents by means of its RETURNING clause; and then the primary query reads that output and inserts it into products\_log.

A fine point of the above example is that the WITH clause is attached to the INSERT, not the sub-SELECT within the INSERT. This is necessary because data-modifying statements are only allowed in WITH clauses that are attached to the top-level statement. However, normal WITH visibility rules apply, so it is possible to refer to the WITH statement's output from the sub-SELECT.

Data-modifying statements in WITH usually have RETURNING clauses (see [Section 6.4](#page-147-1)), as shown in the example above. It is the output of the RETURNING clause, *not* the target table of the data-modifying statement, that forms the temporary table that can be referred to by the rest of the query. If a data-modifying statement in WITH lacks a RETURNING clause, then it forms no temporary table and cannot be referred to in the rest of the query. Such a statement will be executed nonetheless. A notparticularly-useful example is:

```
WITH t AS (
 DELETE FROM foo
)
DELETE FROM bar;
```

This example would remove all rows from tables foo and bar. The number of affected rows reported to the client would only include rows removed from bar.

Recursive self-references in data-modifying statements are not allowed. In some cases it is possible to work around this limitation by referring to the output of a recursive WITH, for example:

```
WITH RECURSIVE included_parts(sub_part, part) AS (
 SELECT sub_part, part FROM parts WHERE part = 'our_product'
 UNION ALL
 SELECT p.sub_part, p.part
 FROM included_parts pr, parts p
 WHERE p.part = pr.sub_part
)
DELETE FROM parts
 WHERE part IN (SELECT part FROM included_parts);
```

This query would remove all direct and indirect subparts of a product.

Data-modifying statements in WITH are executed exactly once, and always to completion, independently of whether the primary query reads all (or indeed any) of their output. Notice that this is different from the rule for SELECT in WITH: as stated in the previous section, execution of a SELECT is carried only as far as the primary query demands its output.

The sub-statements in WITH are executed concurrently with each other and with the main query. Therefore, when using data-modifying statements in WITH, the order in which the specified updates actually happen is unpredictable. All the statements are executed with the same *snapshot* (see Chapter 13), so they cannot "see" one another's effects on the target tables. This alleviates the effects of the unpredictability of the actual order of row updates, and means that RETURNING data is the only way to communicate changes between different WITH sub-statements and the main query. An example of this is that in

```
WITH t AS (
 UPDATE products SET price = price * 1.05
 RETURNING *
)
SELECT * FROM products;
```

the outer SELECT would return the original prices before the action of the UPDATE, while in

```
WITH t AS (
 UPDATE products SET price = price * 1.05
 RETURNING *
)
SELECT * FROM t;
```

the outer SELECT would return the updated data.

Trying to update the same row twice in a single statement is not supported. Only one of the modifications takes place, but it is not easy (and sometimes not possible) to reliably predict which one. This also applies to deleting a row that was already updated in the same statement: only the update is performed. Therefore you should generally avoid trying to modify a single row twice in a single statement. In particular avoid writing WITH sub-statements that could affect the same rows changed by the main statement or a sibling sub-statement. The effects of such a statement will not be predictable.

At present, any table used as the target of a data-modifying statement in WITH must not have a conditional rule, nor an ALSO rule, nor an INSTEAD rule that expands to multiple statements.

# <span id="page-180-0"></span>**Chapter 8. Data Types**

PostgreSQL has a rich set of native data types available to users. Users can add new types to PostgreSQL using the CREATE TYPE command.

[Table 8.1](#page-180-1) shows all the built-in general-purpose data types. Most of the alternative names listed in the "Aliases" column are the names used internally by PostgreSQL for historical reasons. In addition, some internally used or deprecated types are available, but are not listed here.

<span id="page-180-1"></span>**Table 8.1. Data Types**

| Name                           | Aliases               | Description                                           |
|--------------------------------|-----------------------|-------------------------------------------------------|
| bigint                         | int8                  | signed eight-byte integer                             |
| bigserial                      | serial8               | autoincrementing eight-byte integer                   |
| bit [ (n) ]                    |                       | fixed-length bit string                               |
| bit varying [ (n) ]            | varbit<br>[ (n) ]     | variable-length bit string                            |
| boolean                        | bool                  | logical Boolean (true/false)                          |
| box                            |                       | rectangular box on a plane                            |
| bytea                          |                       | binary data ("byte array")                            |
| character [ (n) ]              | char [ (n) ]          | fixed-length character string                         |
| character varying [ (n) ]      | varchar<br>[ (n) ]    | variable-length character string                      |
| cidr                           |                       | IPv4 or IPv6 network address                          |
| circle                         |                       | circle on a plane                                     |
| date                           |                       | calendar date (year, month, day)                      |
| double precision               | float, float8         | double precision floating-point num<br>ber (8 bytes)  |
| inet                           |                       | IPv4 or IPv6 host address                             |
| integer                        | int, int4             | signed four-byte integer                              |
| interval [ fields ]<br>[ (p) ] |                       | time span                                             |
| json                           |                       | textual JSON data                                     |
| jsonb                          |                       | binary JSON data, decomposed                          |
| line                           |                       | infinite line on a plane                              |
| lseg                           |                       | line segment on a plane                               |
| macaddr                        |                       | MAC (Media Access Control) address                    |
| macaddr8                       |                       | MAC (Media Access Control) address<br>(EUI-64 format) |
| money                          |                       | currency amount                                       |
| numeric [ (p, s) ]             | decimal<br>[ (p, s) ] | exact numeric of selectable precision                 |
| path                           |                       | geometric path on a plane                             |
| pg_lsn                         |                       | PostgreSQL Log Sequence Number                        |
| pg_snapshot                    |                       | user-level transaction ID snapshot                    |
| point                          |                       | geometric point on a plane                            |

| Name                                        | Aliases     | Description                                                         |
|---------------------------------------------|-------------|---------------------------------------------------------------------|
| polygon                                     |             | closed geometric path on a plane                                    |
| real                                        | float4      | single precision floating-point number<br>(4 bytes)                 |
| smallint                                    | int2        | signed two-byte integer                                             |
| smallserial                                 | serial2     | autoincrementing two-byte integer                                   |
| serial                                      | serial4     | autoincrementing four-byte integer                                  |
| text                                        |             | variable-length character string                                    |
| time [ (p) ] [ without<br>time zone ]       |             | time of day (no time zone)                                          |
| time [ (p) ] with time<br>zone              | timetz      | time of day, including time zone                                    |
| timestamp [ (p) ] [ with<br>out time zone ] |             | date and time (no time zone)                                        |
| timestamp [ (p) ] with<br>time zone         | timestamptz | date and time, including time zone                                  |
| tsquery                                     |             | text search query                                                   |
| tsvector                                    |             | text search document                                                |
| txid_snapshot                               |             | user-level transaction ID snapshot<br>(deprecated; see pg_snapshot) |
| uuid                                        |             | universally unique identifier                                       |
| xml                                         |             | XML data                                                            |

#### **Compatibility**

The following types (or spellings thereof) are specified by SQL: bigint, bit, bit varying, boolean, char, character varying, character, varchar, date, double precision, integer, interval, numeric, decimal, real, smallint, time (with or without time zone), timestamp (with or without time zone), xml.

Each data type has an external representation determined by its input and output functions. Many of the built-in types have obvious external formats. However, several types are either unique to PostgreSQL, such as geometric paths, or have several possible formats, such as the date and time types. Some of the input and output functions are not invertible, i.e., the result of an output function might lose accuracy when compared to the original input.

# <span id="page-181-0"></span>**8.1. Numeric Types**

Numeric types consist of two-, four-, and eight-byte integers, four- and eight-byte floating-point numbers, and selectable-precision decimals. [Table 8.2](#page-181-1) lists the available types.

<span id="page-181-1"></span>**Table 8.2. Numeric Types**

| Name     | Storage Size Description |                            | Range                                           |
|----------|--------------------------|----------------------------|-------------------------------------------------|
| smallint | 2 bytes                  | small-range integer        | -32768 to +32767                                |
| integer  | 4 bytes                  | typical choice for integer | -2147483648 to<br>+2147483647                   |
| bigint   | 8 bytes                  | large-range integer        | -9223372036854775808 to<br>+9223372036854775807 |

| Name             | Storage Size Description |                                    | Range                                                                                              |
|------------------|--------------------------|------------------------------------|----------------------------------------------------------------------------------------------------|
| decimal          | variable                 | user-specified precision,<br>exact | up to 131072 digits before<br>the decimal point; up to<br>16383 digits after the deci<br>mal point |
| numeric          | variable                 | user-specified precision,<br>exact | up to 131072 digits before<br>the decimal point; up to<br>16383 digits after the deci<br>mal point |
| real             | 4 bytes                  | variable-precision, inexact        | 6 decimal digits precision                                                                         |
| double precision | 8 bytes                  | variable-precision, inexact        | 15 decimal digits precision                                                                        |
| smallserial      | 2 bytes                  | small autoincrementing in<br>teger | 1 to 32767                                                                                         |
| serial           | 4 bytes                  | autoincrementing integer           | 1 to 2147483647                                                                                    |
| bigserial        | 8 bytes                  | large autoincrementing in<br>teger | 1 to<br>9223372036854775807                                                                        |

The syntax of constants for the numeric types is described in [Section 4.1.2](#page-72-0). The numeric types have a full set of corresponding arithmetic operators and functions. Refer to Chapter 9 for more information. The following sections describe the types in detail.

## <span id="page-182-0"></span>**8.1.1. Integer Types**

The types smallint, integer, and bigint store whole numbers, that is, numbers without fractional components, of various ranges. Attempts to store values outside of the allowed range will result in an error.

The type integer is the common choice, as it offers the best balance between range, storage size, and performance. The smallint type is generally only used if disk space is at a premium. The bigint type is designed to be used when the range of the integer type is insufficient.

SQL only specifies the integer types integer (or int), smallint, and bigint. The type names int2, int4, and int8 are extensions, which are also used by some other SQL database systems.

## <span id="page-182-1"></span>**8.1.2. Arbitrary Precision Numbers**

The type numeric can store numbers with a very large number of digits. It is especially recommended for storing monetary amounts and other quantities where exactness is required. Calculations with numeric values yield exact results where possible, e.g., addition, subtraction, multiplication. However, calculations on numeric values are very slow compared to the integer types, or to the floating-point types described in the next section.

We use the following terms below: The *precision* of a numeric is the total count of significant digits in the whole number, that is, the number of digits to both sides of the decimal point. The *scale* of a numeric is the count of decimal digits in the fractional part, to the right of the decimal point. So the number 23.5141 has a precision of 6 and a scale of 4. Integers can be considered to have a scale of zero.

Both the maximum precision and the maximum scale of a numeric column can be configured. To declare a column of type numeric use the syntax:

NUMERIC(precision, scale)

The precision must be positive, the scale zero or positive. Alternatively:

NUMERIC(precision)

selects a scale of 0. Specifying:

NUMERIC

without any precision or scale creates an "unconstrained numeric" column in which numeric values of any length can be stored, up to the implementation limits. A column of this kind will not coerce input values to any particular scale, whereas numeric columns with a declared scale will coerce input values to that scale. (The SQL standard requires a default scale of 0, i.e., coercion to integer precision. We find this a bit useless. If you're concerned about portability, always specify the precision and scale explicitly.)

#### **Note**

The maximum precision that can be explicitly specified in a NUMERIC type declaration is 1000. An unconstrained NUMERIC column is subject to the limits described in [Table 8.2](#page-181-1).

If the scale of a value to be stored is greater than the declared scale of the column, the system will round the value to the specified number of fractional digits. Then, if the number of digits to the left of the decimal point exceeds the declared precision minus the declared scale, an error is raised.

Numeric values are physically stored without any extra leading or trailing zeroes. Thus, the declared precision and scale of a column are maximums, not fixed allocations. (In this sense the numeric type is more akin to varchar(n) than to char(n).) The actual storage requirement is two bytes for each group of four decimal digits, plus three to eight bytes overhead.

In addition to ordinary numeric values, the numeric type has several special values:

Infinity -Infinity NaN

These are adapted from the IEEE 754 standard, and represent "infinity", "negative infinity", and "nota-number", respectively. When writing these values as constants in an SQL command, you must put quotes around them, for example UPDATE table SET x = '-Infinity'. On input, these strings are recognized in a case-insensitive manner. The infinity values can alternatively be spelled inf and -inf.

The infinity values behave as per mathematical expectations. For example, Infinity plus any finite value equals Infinity, as does Infinity plus Infinity; but Infinity minus Infinity yields NaN (not a number), because it has no well-defined interpretation. Note that an infinity can only be stored in an unconstrained numeric column, because it notionally exceeds any finite precision limit.

The NaN (not a number) value is used to represent undefined calculational results. In general, any operation with a NaN input yields another NaN. The only exception is when the operation's other inputs are such that the same output would be obtained if the NaN were to be replaced by any finite or infinite numeric value; then, that output value is used for NaN too. (An example of this principle is that NaN raised to the zero power yields one.)

#### **Note**

In most implementations of the "not-a-number" concept, NaN is not considered equal to any other numeric value (including NaN). In order to allow numeric values to be sorted and used in tree-based indexes, PostgreSQL treats NaN values as equal, and greater than all non-NaN values.

The types decimal and numeric are equivalent. Both types are part of the SQL standard.

When rounding values, the numeric type rounds ties away from zero, while (on most machines) the real and double precision types round ties to the nearest even number. For example:

```
SELECT x,
 round(x::numeric) AS num_round,
 round(x::double precision) AS dbl_round
FROM generate_series(-3.5, 3.5, 1) as x;
 x | num_round | dbl_round
------+-----------+-----------
 -3.5 | -4 | -4
 -2.5 | -3 | -2
 -1.5 | -2 | -2
 -0.5 | -1 | -0
 0.5 | 1 | 0
 1.5 | 2 | 2
 2.5 | 3 | 2
 3.5 | 4 | 4
(8 rows)
```

## <span id="page-184-0"></span>**8.1.3. Floating-Point Types**

The data types real and double precision are inexact, variable-precision numeric types. On all currently supported platforms, these types are implementations of IEEE Standard 754 for Binary Floating-Point Arithmetic (single and double precision, respectively), to the extent that the underlying processor, operating system, and compiler support it.

Inexact means that some values cannot be converted exactly to the internal format and are stored as approximations, so that storing and retrieving a value might show slight discrepancies. Managing these errors and how they propagate through calculations is the subject of an entire branch of mathematics and computer science and will not be discussed here, except for the following points:

- If you require exact storage and calculations (such as for monetary amounts), use the numeric type instead.
- If you want to do complicated calculations with these types for anything important, especially if you rely on certain behavior in boundary cases (infinity, underflow), you should evaluate the implementation carefully.
- Comparing two floating-point values for equality might not always work as expected.

On all currently supported platforms, the real type has a range of around 1E-37 to 1E+37 with a precision of at least 6 decimal digits. The double precision type has a range of around 1E-307 to 1E+308 with a precision of at least 15 digits. Values that are too large or too small will cause an error. Rounding might take place if the precision of an input number is too high. Numbers too close to zero that are not representable as distinct from zero will cause an underflow error.

By default, floating point values are output in text form in their shortest precise decimal representation; the decimal value produced is closer to the true stored binary value than to any other value representable in the same binary precision. (However, the output value is currently never *exactly* midway between two representable values, in order to avoid a widespread bug where input routines do not properly respect the round-to-nearest-even rule.) This value will use at most 17 significant decimal digits for float8 values, and at most 9 digits for float4 values.

#### **Note**

This shortest-precise output format is much faster to generate than the historical rounded format.

For compatibility with output generated by older versions of PostgreSQL, and to allow the output precision to be reduced, the extra\_float\_digits parameter can be used to select rounded decimal output instead. Setting a value of 0 restores the previous default of rounding the value to 6 (for float4) or 15 (for float8) significant decimal digits. Setting a negative value reduces the number of digits further; for example -2 would round output to 4 or 13 digits respectively.

Any value of extra\_float\_digits greater than 0 selects the shortest-precise format.

#### **Note**

Applications that wanted precise values have historically had to set extra\_float\_digits to 3 to obtain them. For maximum compatibility between versions, they should continue to do so.

In addition to ordinary numeric values, the floating-point types have several special values:

Infinity -Infinity NaN

These represent the IEEE 754 special values "infinity", "negative infinity", and "not-a-number", respectively. When writing these values as constants in an SQL command, you must put quotes around them, for example UPDATE table SET x = '-Infinity'. On input, these strings are recognized in a case-insensitive manner. The infinity values can alternatively be spelled inf and -inf.

#### **Note**

IEEE 754 specifies that NaN should not compare equal to any other floating-point value (including NaN). In order to allow floating-point values to be sorted and used in tree-based indexes, PostgreSQL treats NaN values as equal, and greater than all non-NaN values.

PostgreSQL also supports the SQL-standard notations float and float(p) for specifying inexact numeric types. Here, p specifies the minimum acceptable precision in *binary* digits. PostgreSQL accepts float(1) to float(24) as selecting the real type, while float(25) to float(53) select double precision. Values of p outside the allowed range draw an error. float with no precision specified is taken to mean double precision.

## <span id="page-185-0"></span>**8.1.4. Serial Types**

#### **Note**

This section describes a PostgreSQL-specific way to create an autoincrementing column. Another way is to use the SQL-standard identity column feature, described at CREATE TABLE.

The data types smallserial, serial and bigserial are not true types, but merely a notational convenience for creating unique identifier columns (similar to the AUTO\_INCREMENT property supported by some other databases). In the current implementation, specifying:

```
CREATE TABLE tablename (
 colname SERIAL
);
is equivalent to specifying:
CREATE SEQUENCE tablename_colname_seq AS integer;
CREATE TABLE tablename (
 colname integer NOT NULL DEFAULT
 nextval('tablename_colname_seq')
);
ALTER SEQUENCE tablename_colname_seq OWNED BY tablename.colname;
```

Thus, we have created an integer column and arranged for its default values to be assigned from a sequence generator. A NOT NULL constraint is applied to ensure that a null value cannot be inserted. (In most cases you would also want to attach a UNIQUE or PRIMARY KEY constraint to prevent duplicate values from being inserted by accident, but this is not automatic.) Lastly, the sequence is marked as "owned by" the column, so that it will be dropped if the column or table is dropped.

#### **Note**

Because smallserial, serial and bigserial are implemented using sequences, there may be "holes" or gaps in the sequence of values which appears in the column, even if no rows are ever deleted. A value allocated from the sequence is still "used up" even if a row containing that value is never successfully inserted into the table column. This may happen, for example, if the inserting transaction rolls back. See nextval() in Section 9.17 for details.

To insert the next value of the sequence into the serial column, specify that the serial column should be assigned its default value. This can be done either by excluding the column from the list of columns in the INSERT statement, or through the use of the DEFAULT key word.

The type names serial and serial4 are equivalent: both create integer columns. The type names bigserial and serial8 work the same way, except that they create a bigint column. bigserial should be used if you anticipate the use of more than 231 identifiers over the lifetime of the table. The type names smallserial and serial2 also work the same way, except that they create a smallint column.

The sequence created for a serial column is automatically dropped when the owning column is dropped. You can drop the sequence without dropping the column, but this will force removal of the column default expression.

# <span id="page-186-0"></span>**8.2. Monetary Types**

The money type stores a currency amount with a fixed fractional precision; see [Table 8.3](#page-186-1). The fractional precision is determined by the database's lc\_monetary setting. The range shown in the table assumes there are two fractional digits. Input is accepted in a variety of formats, including integer and floating-point literals, as well as typical currency formatting, such as '\$1,000.00'. Output is generally in the latter form but depends on the locale.

<span id="page-186-1"></span>**Table 8.3. Monetary Types**

| Name  | Storage Size Description |                 | Range                       |
|-------|--------------------------|-----------------|-----------------------------|
| money | 8 bytes                  | currency amount | -92233720368547758.08       |
|       |                          |                 | to<br>+92233720368547758.07 |

Since the output of this data type is locale-sensitive, it might not work to load money data into a database that has a different setting of lc\_monetary. To avoid problems, before restoring a dump into a new database make sure lc\_monetary has the same or equivalent value as in the database that was dumped.

Values of the numeric, int, and bigint data types can be cast to money. Conversion from the real and double precision data types can be done by casting to numeric first, for example:

```
SELECT '12.34'::float8::numeric::money;
```

However, this is not recommended. Floating point numbers should not be used to handle money due to the potential for rounding errors.

A money value can be cast to numeric without loss of precision. Conversion to other types could potentially lose precision, and must also be done in two stages:

```
SELECT '52093.89'::money::numeric::float8;
```

Division of a money value by an integer value is performed with truncation of the fractional part towards zero. To get a rounded result, divide by a floating-point value, or cast the money value to numeric before dividing and back to money afterwards. (The latter is preferable to avoid risking precision loss.) When a money value is divided by another money value, the result is double precision (i.e., a pure number, not money); the currency units cancel each other out in the division.

# <span id="page-187-1"></span><span id="page-187-0"></span>**8.3. Character Types**

**Table 8.4. Character Types**

| Name                             | Description                |
|----------------------------------|----------------------------|
| character varying(n), varchar(n) | variable-length with limit |
| character(n), char(n)            | fixed-length, blank padded |
| text                             | variable unlimited length  |

[Table 8.4](#page-187-1) shows the general-purpose character types available in PostgreSQL.

SQL defines two primary character types: character varying(n) and character(n), where n is a positive integer. Both of these types can store strings up to n characters (not bytes) in length. An attempt to store a longer string into a column of these types will result in an error, unless the excess characters are all spaces, in which case the string will be truncated to the maximum length. (This somewhat bizarre exception is required by the SQL standard.) If the string to be stored is shorter than the declared length, values of type character will be space-padded; values of type character varying will simply store the shorter string.

If one explicitly casts a value to character varying(n) or character(n), then an overlength value will be truncated to n characters without raising an error. (This too is required by the SQL standard.)

The notations varchar(n) and char(n) are aliases for character varying(n) and character(n), respectively. If specified, the length must be greater than zero and cannot exceed 10485760. character without length specifier is equivalent to character(1). If character varying is used without length specifier, the type accepts strings of any size. The latter is a PostgreSQL extension.

In addition, PostgreSQL provides the text type, which stores strings of any length. Although the type text is not in the SQL standard, several other SQL database management systems have it as well.

Values of type character are physically padded with spaces to the specified width n, and are stored and displayed that way. However, trailing spaces are treated as semantically insignificant and disregarded when comparing two values of type character. In collations where whitespace is significant, this behavior can produce unexpected results; for example SELECT 'a '::CHAR(2) collate "C" < E'a\n'::CHAR(2) returns true, even though C locale would consider a space to be greater than a newline. Trailing spaces are removed when converting a character value to one of the other string types. Note that trailing spaces *are* semantically significant in character varying and text values, and when using pattern matching, that is LIKE and regular expressions.

The characters that can be stored in any of these data types are determined by the database character set, which is selected when the database is created. Regardless of the specific character set, the character with code zero (sometimes called NUL) cannot be stored. For more information refer to Section 24.3.

The storage requirement for a short string (up to 126 bytes) is 1 byte plus the actual string, which includes the space padding in the case of character. Longer strings have 4 bytes of overhead instead of 1. Long strings are compressed by the system automatically, so the physical requirement on disk might be less. Very long values are also stored in background tables so that they do not interfere with rapid access to shorter column values. In any case, the longest possible character string that can be stored is about 1 GB. (The maximum value that will be allowed for n in the data type declaration is less than that. It wouldn't be useful to change this because with multibyte character encodings the number of characters and bytes can be quite different. If you desire to store long strings with no specific upper limit, use text or character varying without a length specifier, rather than making up an arbitrary length limit.)

#### <span id="page-188-1"></span>**Tip**

There is no performance difference among these three types, apart from increased storage space when using the blank-padded type, and a few extra CPU cycles to check the length when storing into a length-constrained column. While character(n) has performance advantages in some other database systems, there is no such advantage in PostgreSQL; in fact character(n) is usually the slowest of the three because of its additional storage costs. In most situations text or character varying should be used instead.

Refer to [Section 4.1.2.1](#page-72-1) for information about the syntax of string literals, and to Chapter 9 for information about available operators and functions.

#### <span id="page-188-0"></span>**Example 8.1. Using the Character Types**

```
CREATE TABLE test1 (a character(4));
INSERT INTO test1 VALUES ('ok');
SELECT a, char_length(a) FROM test1; -- 1
 a | char_length
------+-------------
 ok | 2
CREATE TABLE test2 (b varchar(5));
INSERT INTO test2 VALUES ('ok');
INSERT INTO test2 VALUES ('good ');
INSERT INTO test2 VALUES ('too long');
ERROR: value too long for type character varying(5)
INSERT INTO test2 VALUES ('too long'::varchar(5)); -- explicit
 truncation
SELECT b, char_length(b) FROM test2;
```

| b     | char_length |   |
|-------|-------------|---|
| ok    | +<br>       | 2 |
| good  |             | 5 |
| too l |             | 5 |

**[1](#page-188-1)** The char\_length function is discussed in Section 9.4.

There are two other fixed-length character types in PostgreSQL, shown in [Table 8.5](#page-189-1). The name type exists *only* for the storage of identifiers in the internal system catalogs and is not intended for use by the general user. Its length is currently defined as 64 bytes (63 usable characters plus terminator) but should be referenced using the constant NAMEDATALEN in C source code. The length is set at compile time (and is therefore adjustable for special uses); the default maximum length might change in a future release. The type "char" (note the quotes) is different from char(1) in that it only uses one byte of storage. It is internally used in the system catalogs as a simplistic enumeration type.

<span id="page-189-1"></span>**Table 8.5. Special Character Types**

| Name   | Storage Size | Description                    |
|--------|--------------|--------------------------------|
| "char" | 1 byte       | single-byte internal type      |
| name   | 64 bytes     | internal type for object names |

# <span id="page-189-2"></span><span id="page-189-0"></span>**8.4. Binary Data Types**

The bytea data type allows storage of binary strings; see [Table 8.6](#page-189-2).

**Table 8.6. Binary Data Types**

| Name  | Storage Size                               | Description                   |
|-------|--------------------------------------------|-------------------------------|
| bytea | 1 or 4 bytes plus the actual binary string | variable-length binary string |

A binary string is a sequence of octets (or bytes). Binary strings are distinguished from character strings in two ways. First, binary strings specifically allow storing octets of value zero and other "nonprintable" octets (usually, octets outside the decimal range 32 to 126). Character strings disallow zero octets, and also disallow any other octet values and sequences of octet values that are invalid according to the database's selected character set encoding. Second, operations on binary strings process the actual bytes, whereas the processing of character strings depends on locale settings. In short, binary strings are appropriate for storing data that the programmer thinks of as "raw bytes", whereas character strings are appropriate for storing text.

The bytea type supports two formats for input and output: "hex" format and PostgreSQL's historical "escape" format. Both of these are always accepted on input. The output format depends on the configuration parameter bytea\_output; the default is hex. (Note that the hex format was introduced in PostgreSQL 9.0; earlier versions and some tools don't understand it.)

The SQL standard defines a different binary string type, called BLOB or BINARY LARGE OBJECT. The input format is different from bytea, but the provided functions and operators are mostly the same.

## <span id="page-189-3"></span>**8.4.1. bytea Hex Format**

The "hex" format encodes binary data as 2 hexadecimal digits per byte, most significant nibble first. The entire string is preceded by the sequence \x (to distinguish it from the escape format). In some contexts, the initial backslash may need to be escaped by doubling it (see [Section 4.1.2.1](#page-72-1)). For input, the hexadecimal digits can be either upper or lower case, and whitespace is permitted between digit pairs (but not within a digit pair nor in the starting \x sequence). The hex format is compatible with a wide range of external applications and protocols, and it tends to be faster to convert than the escape format, so its use is preferred.

#### Example:

```
SET bytea_output = 'hex';
SELECT '\xDEADBEEF'::bytea;
 bytea
------------
 \xdeadbeef
```

## <span id="page-190-1"></span>**8.4.2. bytea Escape Format**

The "escape" format is the traditional PostgreSQL format for the bytea type. It takes the approach of representing a binary string as a sequence of ASCII characters, while converting those bytes that cannot be represented as an ASCII character into special escape sequences. If, from the point of view of the application, representing bytes as characters makes sense, then this representation can be convenient. But in practice it is usually confusing because it fuzzes up the distinction between binary strings and character strings, and also the particular escape mechanism that was chosen is somewhat unwieldy. Therefore, this format should probably be avoided for most new applications.

When entering bytea values in escape format, octets of certain values *must* be escaped, while all octet values *can* be escaped. In general, to escape an octet, convert it into its three-digit octal value and precede it by a backslash. Backslash itself (octet decimal value 92) can alternatively be represented by double backslashes. [Table 8.7](#page-190-0) shows the characters that must be escaped, and gives the alternative escape sequences where applicable.

<span id="page-190-0"></span>

| Table 8.7. bytea Literal Escaped Octets |  |  |  |
|-----------------------------------------|--|--|--|
|-----------------------------------------|--|--|--|

| Decimal Octet<br>Value    | Description               | Escaped Input<br>Representation | Example       | Hex Representa<br>tion |
|---------------------------|---------------------------|---------------------------------|---------------|------------------------|
| 0                         | zero octet                | '\000'                          | '\000'::bytea | \x00                   |
| 39                        | single quote              | '''' or<br>'\047'               | ''''::bytea   | \x27                   |
| 92                        | backslash                 | '\\' or<br>'\134'               | '\\'::bytea   | \x5c                   |
| 0 to 31 and 127<br>to 255 | "non-printable"<br>octets | '\xxx' (octal<br>value)         | '\001'::bytea | \x01                   |

The requirement to escape *non-printable* octets varies depending on locale settings. In some instances you can get away with leaving them unescaped.

The reason that single quotes must be doubled, as shown in [Table 8.7](#page-190-0), is that this is true for any string literal in an SQL command. The generic string-literal parser consumes the outermost single quotes and reduces any pair of single quotes to one data character. What the bytea input function sees is just one single quote, which it treats as a plain data character. However, the bytea input function treats backslashes as special, and the other behaviors shown in [Table 8.7](#page-190-0) are implemented by that function.

In some contexts, backslashes must be doubled compared to what is shown above, because the generic string-literal parser will also reduce pairs of backslashes to one data character; see [Section 4.1.2.1.](#page-72-1)

Bytea octets are output in hex format by default. If you change bytea\_output to escape, "nonprintable" octets are converted to their equivalent three-digit octal value and preceded by one backslash. Most "printable" octets are output by their standard representation in the client character set, e.g.:

```
SET bytea_output = 'escape';
SELECT 'abc \153\154\155 \052\251\124'::bytea;
 bytea
----------------
 abc klm *\251T
```

The octet with decimal value 92 (backslash) is doubled in the output. Details are in [Table 8.8](#page-191-1).

<span id="page-191-1"></span>**Table 8.8. bytea Output Escaped Octets**

| Decimal Octet<br>Value    | Description               | Escaped Output<br>Representation       | Example       | Output Result |
|---------------------------|---------------------------|----------------------------------------|---------------|---------------|
| 92                        | backslash                 | \\                                     | '\134'::bytea | \\            |
| 0 to 31 and 127<br>to 255 | "non-printable"<br>octets | \xxx (octal val<br>ue)                 | '\001'::bytea | \001          |
| 32 to 126                 | "printable" octets        | client character<br>set representation | '\176'::bytea | ~             |

Depending on the front end to PostgreSQL you use, you might have additional work to do in terms of escaping and unescaping bytea strings. For example, you might also have to escape line feeds and carriage returns if your interface automatically translates these.

# <span id="page-191-0"></span>**8.5. Date/Time Types**

PostgreSQL supports the full set of SQL date and time types, shown in [Table 8.9.](#page-191-2) The operations available on these data types are described in Section 9.9. Dates are counted according to the Gregorian calendar, even in years before that calendar was introduced (see Section B.6 for more information).

<span id="page-191-2"></span>**Table 8.9. Date/Time Types**

| Name                                                 | Storage Size | Description                                 | Low Value           | High Value         | Resolution    |
|------------------------------------------------------|--------------|---------------------------------------------|---------------------|--------------------|---------------|
| timestamp<br>[ (p) ]<br>[ with<br>out time<br>zone ] | 8 bytes      | both date and<br>time (no time<br>zone)     | 4713 BC             | 294276 AD          | 1 microsecond |
| timestamp<br>[ (p) ]<br>with time<br>zone            | 8 bytes      | both date and<br>time, with time<br>zone    | 4713 BC             | 294276 AD          | 1 microsecond |
| date                                                 | 4 bytes      | date (no time<br>of day)                    | 4713 BC             | 5874897 AD         | 1 day         |
| time<br>[ (p) ]<br>[ with<br>out time<br>zone ]      | 8 bytes      | time of day (no<br>date)                    | 00:00:00            | 24:00:00           | 1 microsecond |
| time<br>[ (p) ]<br>with time<br>zone                 | 12 bytes     | time of day<br>(no date), with<br>time zone | 00:00:00+1559       | 24:00:00-1559      | 1 microsecond |
| interval<br>[ fields ]<br>[ (p) ]                    | 16 bytes     | time interval                               | -178000000<br>years | 178000000<br>years | 1 microsecond |

#### **Note**

The SQL standard requires that writing just timestamp be equivalent to timestamp without time zone, and PostgreSQL honors that behavior. timestamptz is accepted as an abbreviation for timestamp with time zone; this is a PostgreSQL extension.

time, timestamp, and interval accept an optional precision value p which specifies the number of fractional digits retained in the seconds field. By default, there is no explicit bound on precision. The allowed range of p is from 0 to 6.

The interval type has an additional option, which is to restrict the set of stored fields by writing one of these phrases:

YEAR MONTH DAY HOUR MINUTE SECOND YEAR TO MONTH DAY TO HOUR DAY TO MINUTE DAY TO SECOND HOUR TO MINUTE HOUR TO SECOND MINUTE TO SECOND

Note that if both fields and p are specified, the fields must include SECOND, since the precision applies only to the seconds.

The type time with time zone is defined by the SQL standard, but the definition exhibits properties which lead to questionable usefulness. In most cases, a combination of date, time, timestamp without time zone, and timestamp with time zone should provide a complete range of date/time functionality required by any application.

## <span id="page-192-0"></span>**8.5.1. Date/Time Input**

Date and time input is accepted in almost any reasonable format, including ISO 8601, SQL-compatible, traditional POSTGRES, and others. For some formats, ordering of day, month, and year in date input is ambiguous and there is support for specifying the expected ordering of these fields. Set the DateStyle parameter to MDY to select month-day-year interpretation, DMY to select day-month-year interpretation, or YMD to select year-month-day interpretation.

PostgreSQL is more flexible in handling date/time input than the SQL standard requires. See Appendix B for the exact parsing rules of date/time input and for the recognized text fields including months, days of the week, and time zones.

Remember that any date or time literal input needs to be enclosed in single quotes, like text strings. Refer to [Section 4.1.2.7](#page-76-1) for more information. SQL requires the following syntax

```
type [ (p) ] 'value'
```

where p is an optional precision specification giving the number of fractional digits in the seconds field. Precision can be specified for time, timestamp, and interval types, and can range from 0 to 6. If no precision is specified in a constant specification, it defaults to the precision of the literal value (but not more than 6 digits).

#### <span id="page-193-0"></span>**8.5.1.1. Dates**

[Table 8.10](#page-193-0) shows some possible inputs for the date type.

**Table 8.10. Date Input**

| Example          | Description                                                                                |
|------------------|--------------------------------------------------------------------------------------------|
| 1999-01-08       | ISO 8601; January 8 in any mode (recommended format)                                       |
| January 8, 1999  | unambiguous in any datestyle input mode                                                    |
| 1/8/1999         | January 8 in MDY mode; August 1 in DMY mode                                                |
| 1/18/1999        | January 18 in MDY mode; rejected in other modes                                            |
| 01/02/03         | January 2, 2003 in MDY mode; February 1, 2003 in DMY mode;<br>February 3, 2001 in YMD mode |
| 1999-Jan-08      | January 8 in any mode                                                                      |
| Jan-08-1999      | January 8 in any mode                                                                      |
| 08-Jan-1999      | January 8 in any mode                                                                      |
| 99-Jan-08        | January 8 in YMD mode, else error                                                          |
| 08-Jan-99        | January 8, except error in YMD mode                                                        |
| Jan-08-99        | January 8, except error in YMD mode                                                        |
| 19990108         | ISO 8601; January 8, 1999 in any mode                                                      |
| 990108           | ISO 8601; January 8, 1999 in any mode                                                      |
| 1999.008         | year and day of year                                                                       |
| J2451187         | Julian date                                                                                |
| January 8, 99 BC | year 99 BC                                                                                 |

#### **8.5.1.2. Times**

The time-of-day types are time [ (p) ] without time zone and time [ (p) ] with time zone. time alone is equivalent to time without time zone.

Valid input for these types consists of a time of day followed by an optional time zone. (See [Table 8.11](#page-193-1) and [Table 8.12](#page-194-0).) If a time zone is specified in the input for time without time zone, it is silently ignored. You can also specify a date but it will be ignored, except when you use a time zone name that involves a daylight-savings rule, such as America/New\_York. In this case specifying the date is required in order to determine whether standard or daylight-savings time applies. The appropriate time zone offset is recorded in the time with time zone value and is output as stored; it is not adjusted to the active time zone.

<span id="page-193-1"></span>**Table 8.11. Time Input**

| Example      | Description                                |
|--------------|--------------------------------------------|
| 04:05:06.789 | ISO 8601                                   |
| 04:05:06     | ISO 8601                                   |
| 04:05        | ISO 8601                                   |
| 040506       | ISO 8601                                   |
| 04:05 AM     | same as 04:05; AM does not affect<br>value |

| Example                              | Description                                                  |
|--------------------------------------|--------------------------------------------------------------|
| 04:05 PM                             | same as 16:05; input hour must be <=<br>12                   |
| 04:05:06.789-8                       | ISO 8601, with time zone as UTC off<br>set                   |
| 04:05:06-08:00                       | ISO 8601, with time zone as UTC off<br>set                   |
| 04:05-08:00                          | ISO 8601, with time zone as UTC off<br>set                   |
| 040506-08                            | ISO 8601, with time zone as UTC off<br>set                   |
| 040506+0730                          | ISO 8601, with fractional-hour time<br>zone as UTC offset    |
| 040506+07:30:00                      | UTC offset specified to seconds (not<br>allowed in ISO 8601) |
| 04:05:06 PST                         | time zone specified by abbreviation                          |
| 2003-04-12 04:05:06 America/New_York | time zone specified by full name                             |

<span id="page-194-0"></span>**Table 8.12. Time Zone Input**

| Example          | Description                                   |
|------------------|-----------------------------------------------|
| PST              | Abbreviation (for Pacific Standard Time)      |
| America/New_York | Full time zone name                           |
| PST8PDT          | POSIX-style time zone specification           |
| -8:00:00         | UTC offset for PST                            |
| -8:00            | UTC offset for PST (ISO 8601 extended format) |
| -800             | UTC offset for PST (ISO 8601 basic format)    |
| -8               | UTC offset for PST (ISO 8601 basic format)    |
| zulu             | Military abbreviation for UTC                 |
| z                | Short form of zulu (also in ISO 8601)         |

Refer to [Section 8.5.3](#page-197-1) for more information on how to specify time zones.

### **8.5.1.3. Time Stamps**

Valid input for the time stamp types consists of the concatenation of a date and a time, followed by an optional time zone, followed by an optional AD or BC. (Alternatively, AD/BC can appear before the time zone, but this is not the preferred ordering.) Thus:

1999-01-08 04:05:06

and:

1999-01-08 04:05:06 -8:00

are valid values, which follow the ISO 8601 standard. In addition, the common format:

January 8 04:05:06 1999 PST

is supported.

The SQL standard differentiates timestamp without time zone and timestamp with time zone literals by the presence of a "+" or "-" symbol and time zone offset after the time. Hence, according to the standard,

```
TIMESTAMP '2004-10-19 10:23:54'
```

is a timestamp without time zone, while

```
TIMESTAMP '2004-10-19 10:23:54+02'
```

is a timestamp with time zone. PostgreSQL never examines the content of a literal string before determining its type, and therefore will treat both of the above as timestamp without time zone. To ensure that a literal is treated as timestamp with time zone, give it the correct explicit type:

```
TIMESTAMP WITH TIME ZONE '2004-10-19 10:23:54+02'
```

In a value that has been determined to be timestamp without time zone, PostgreSQL will silently ignore any time zone indication. That is, the resulting value is derived from the date/time fields in the input string, and is not adjusted for time zone.

For timestamp with time zone values, an input string that includes an explicit time zone will be converted to UTC (*Universal Coordinated Time*) using the appropriate offset for that time zone. If no time zone is stated in the input string, then it is assumed to be in the time zone indicated by the system's TimeZone parameter, and is converted to UTC using the offset for the timezone zone. In either case, the value is stored internally as UTC, and the originally stated or assumed time zone is not retained.

When a timestamp with time zone value is output, it is always converted from UTC to the current timezone zone, and displayed as local time in that zone. To see the time in another time zone, either change timezone or use the AT TIME ZONE construct (see Section 9.9.4).

Conversions between timestamp without time zone and timestamp with time zone normally assume that the timestamp without time zone value should be taken or given as timezone local time. A different time zone can be specified for the conversion using AT TIME ZONE.

### **8.5.1.4. Special Values**

PostgreSQL supports several special date/time input values for convenience, as shown in [Table 8.13.](#page-195-0) The values infinity and -infinity are specially represented inside the system and will be displayed unchanged; but the others are simply notational shorthands that will be converted to ordinary date/time values when read. (In particular, now and related strings are converted to a specific time value as soon as they are read.) All of these values need to be enclosed in single quotes when used as constants in SQL commands.

<span id="page-195-0"></span>**Table 8.13. Special Date/Time Inputs**

| Input String | Valid Types     | Description                                       |
|--------------|-----------------|---------------------------------------------------|
| epoch        | date, timestamp | 1970-01-01 00:00:00+00 (Unix<br>system time zero) |
| infinity     | date, timestamp | later than all other time stamps                  |
| -infinity    | date, timestamp | earlier than all other time<br>stamps             |

| Input String | Valid Types           | Description                      |
|--------------|-----------------------|----------------------------------|
| now          | date, time, timestamp | current transaction's start time |
| today        | date, timestamp       | midnight (00:00) today           |
| tomorrow     | date, timestamp       | midnight (00:00) tomorrow        |
| yesterday    | date, timestamp       | midnight (00:00) yesterday       |
| allballs     | time                  | 00:00:00.00 UTC                  |

The following SQL-compatible functions can also be used to obtain the current time value for the corresponding data type: CURRENT\_DATE, CURRENT\_TIME, CURRENT\_TIMESTAMP, LOCALTIME, LOCALTIMESTAMP. (See Section 9.9.5.) Note that these are SQL functions and are *not* recognized in data input strings.

#### **Caution**

While the input strings now, today, tomorrow, and yesterday are fine to use in interactive SQL commands, they can have surprising behavior when the command is saved to be executed later, for example in prepared statements, views, and function definitions. The string can be converted to a specific time value that continues to be used long after it becomes stale. Use one of the SQL functions instead in such contexts. For example, CURRENT\_DATE + 1 is safer than 'tomorrow'::date.

## <span id="page-196-1"></span>**8.5.2. Date/Time Output**

The output format of the date/time types can be set to one of the four styles ISO 8601, SQL (Ingres), traditional POSTGRES (Unix date format), or German. The default is the ISO format. (The SQL standard requires the use of the ISO 8601 format. The name of the "SQL" output format is a historical accident.) [Table 8.14](#page-196-0) shows examples of each output style. The output of the date and time types is generally only the date or time part in accordance with the given examples. However, the POSTGRES style outputs date-only values in ISO format.

<span id="page-196-0"></span>**Table 8.14. Date/Time Output Styles**

| Style Specification | Description                | Example                      |
|---------------------|----------------------------|------------------------------|
| ISO                 | ISO 8601, SQL stan<br>dard | 1997-12-17 07:37:16-08       |
| SQL                 | traditional style          | 12/17/1997 07:37:16.00 PST   |
| Postgres            | original style             | Wed Dec 17 07:37:16 1997 PST |
| German              | regional style             | 17.12.1997 07:37:16.00 PST   |

#### **Note**

ISO 8601 specifies the use of uppercase letter T to separate the date and time. PostgreSQL accepts that format on input, but on output it uses a space rather than T, as shown above. This is for readability and for consistency with [RFC 3339](https://datatracker.ietf.org/doc/html/rfc3339)<sup>1</sup> as well as some other database systems.

In the SQL and POSTGRES styles, day appears before month if DMY field ordering has been specified, otherwise month appears before day. (See [Section 8.5.1](#page-192-0) for how this setting also affects interpretation of input values.) [Table 8.15](#page-197-0) shows examples.

<sup>1</sup> <https://datatracker.ietf.org/doc/html/rfc3339>

**Table 8.15. Date Order Conventions**

<span id="page-197-0"></span>

| datestyle Setting | Input Ordering | Example Output               |
|-------------------|----------------|------------------------------|
| SQL, DMY          | day/month/year | 17/12/1997 15:37:16.00 CET   |
| SQL, MDY          | month/day/year | 12/17/1997 07:37:16.00 PST   |
| Postgres, DMY     | day/month/year | Wed 17 Dec 07:37:16 1997 PST |

In the ISO style, the time zone is always shown as a signed numeric offset from UTC, with positive sign used for zones east of Greenwich. The offset will be shown as hh (hours only) if it is an integral number of hours, else as hh:mm if it is an integral number of minutes, else as hh:mm:ss. (The third case is not possible with any modern time zone standard, but it can appear when working with timestamps that predate the adoption of standardized time zones.) In the other date styles, the time zone is shown as an alphabetic abbreviation if one is in common use in the current zone. Otherwise it appears as a signed numeric offset in ISO 8601 basic format (hh or hhmm).

The date/time style can be selected by the user using the SET datestyle command, the DateStyle parameter in the postgresql.conf configuration file, or the PGDATESTYLE environment variable on the server or client.

The formatting function to\_char (see Section 9.8) is also available as a more flexible way to format date/time output.

## <span id="page-197-1"></span>**8.5.3. Time Zones**

Time zones, and time-zone conventions, are influenced by political decisions, not just earth geometry. Time zones around the world became somewhat standardized during the 1900s, but continue to be prone to arbitrary changes, particularly with respect to daylight-savings rules. PostgreSQL uses the widely-used IANA (Olson) time zone database for information about historical time zone rules. For times in the future, the assumption is that the latest known rules for a given time zone will continue to be observed indefinitely far into the future.

PostgreSQL endeavors to be compatible with the SQL standard definitions for typical usage. However, the SQL standard has an odd mix of date and time types and capabilities. Two obvious problems are:

- Although the date type cannot have an associated time zone, the time type can. Time zones in the real world have little meaning unless associated with a date as well as a time, since the offset can vary through the year with daylight-saving time boundaries.
- The default time zone is specified as a constant numeric offset from UTC. It is therefore impossible to adapt to daylight-saving time when doing date/time arithmetic across DST boundaries.

To address these difficulties, we recommend using date/time types that contain both date and time when using time zones. We do *not* recommend using the type time with time zone (though it is supported by PostgreSQL for legacy applications and for compliance with the SQL standard). PostgreSQL assumes your local time zone for any type containing only date or time.

All timezone-aware dates and times are stored internally in UTC. They are converted to local time in the zone specified by the TimeZone configuration parameter before being displayed to the client.

PostgreSQL allows you to specify time zones in three different forms:

- A full time zone name, for example America/New\_York. The recognized time zone names are listed in the pg\_timezone\_names view (see Section 52.94). PostgreSQL uses the widely-used IANA time zone data for this purpose, so the same time zone names are also recognized by other software.
- A time zone abbreviation, for example PST. Such a specification merely defines a particular offset from UTC, in contrast to full time zone names which can imply a set of daylight savings transition rules as well. The recognized abbreviations are listed in the pg\_timezone\_abbrevs view (see

Section 52.93). You cannot set the configuration parameters TimeZone or log\_timezone to a time zone abbreviation, but you can use abbreviations in date/time input values and with the AT TIME ZONE operator.

• In addition to the timezone names and abbreviations, PostgreSQL will accept POSIX-style time zone specifications, as described in Section B.5. This option is not normally preferable to using a named time zone, but it may be necessary if no suitable IANA time zone entry is available.

In short, this is the difference between abbreviations and full names: abbreviations represent a specific offset from UTC, whereas many of the full names imply a local daylight-savings time rule, and so have two possible UTC offsets. As an example, 2014-06-04 12:00 America/New\_York represents noon local time in New York, which for this particular date was Eastern Daylight Time (UTC-4). So 2014-06-04 12:00 EDT specifies that same time instant. But 2014-06-04 12:00 EST specifies noon Eastern Standard Time (UTC-5), regardless of whether daylight savings was nominally in effect on that date.

To complicate matters, some jurisdictions have used the same timezone abbreviation to mean different UTC offsets at different times; for example, in Moscow MSK has meant UTC+3 in some years and UTC+4 in others. PostgreSQL interprets such abbreviations according to whatever they meant (or had most recently meant) on the specified date; but, as with the EST example above, this is not necessarily the same as local civil time on that date.

In all cases, timezone names and abbreviations are recognized case-insensitively. (This is a change from PostgreSQL versions prior to 8.2, which were case-sensitive in some contexts but not others.)

Neither timezone names nor abbreviations are hard-wired into the server; they are obtained from configuration files stored under .../share/timezone/ and .../share/timezonesets/ of the installation directory (see Section B.4).

The TimeZone configuration parameter can be set in the file postgresql.conf, or in any of the other standard ways described in Chapter 20. There are also some special ways to set it:

- The SQL command SET TIME ZONE sets the time zone for the session. This is an alternative spelling of SET TIMEZONE TO with a more SQL-spec-compatible syntax.
- The PGTZ environment variable is used by libpq clients to send a SET TIME ZONE command to the server upon connection.

## <span id="page-198-0"></span>**8.5.4. Interval Input**

interval values can be written using the following verbose syntax:

```
[@] quantity unit [quantity unit...] [direction]
```

where quantity is a number (possibly signed); unit is microsecond, millisecond, second, minute, hour, day, week, month, year, decade, century, millennium, or abbreviations or plurals of these units; direction can be ago or empty. The at sign (@) is optional noise. The amounts of the different units are implicitly added with appropriate sign accounting. ago negates all the fields. This syntax is also used for interval output, if IntervalStyle is set to postgres\_verbose.

Quantities of days, hours, minutes, and seconds can be specified without explicit unit markings. For example, '1 12:59:10' is read the same as '1 day 12 hours 59 min 10 sec'. Also, a combination of years and months can be specified with a dash; for example '200-10' is read the same as '200 years 10 months'. (These shorter forms are in fact the only ones allowed by the SQL standard, and are used for output when IntervalStyle is set to sql\_standard.)

Interval values can also be written as ISO 8601 time intervals, using either the "format with designators" of the standard's section 4.4.3.2 or the "alternative format" of section 4.4.3.3. The format with designators looks like this:

```
P quantity unit [ quantity unit ...] [ T [ quantity unit ...]]
```

The string must start with a P, and may include a T that introduces the time-of-day units. The available unit abbreviations are given in [Table 8.16.](#page-199-0) Units may be omitted, and may be specified in any order, but units smaller than a day must appear after T. In particular, the meaning of M depends on whether it is before or after T.

<span id="page-199-0"></span>**Table 8.16. ISO 8601 Interval Unit Abbreviations**

| Abbreviation | Meaning                    |
|--------------|----------------------------|
| Y            | Years                      |
| M            | Months (in the date part)  |
| W            | Weeks                      |
| D            | Days                       |
| H            | Hours                      |
| M            | Minutes (in the time part) |
| S            | Seconds                    |

In the alternative format:

```
P [ years-months-days ] [ T hours:minutes:seconds ]
```

the string must begin with P, and a T separates the date and time parts of the interval. The values are given as numbers similar to ISO 8601 dates.

When writing an interval constant with a fields specification, or when assigning a string to an interval column that was defined with a fields specification, the interpretation of unmarked quantities depends on the fields. For example INTERVAL '1' YEAR is read as 1 year, whereas INTER-VAL '1' means 1 second. Also, field values "to the right" of the least significant field allowed by the fields specification are silently discarded. For example, writing INTERVAL '1 day 2:03:04' HOUR TO MINUTE results in dropping the seconds field, but not the day field.

According to the SQL standard all fields of an interval value must have the same sign, so a leading negative sign applies to all fields; for example the negative sign in the interval literal '-1 2:03:04' applies to both the days and hour/minute/second parts. PostgreSQL allows the fields to have different signs, and traditionally treats each field in the textual representation as independently signed, so that the hour/minute/second part is considered positive in this example. If IntervalStyle is set to sql\_standard then a leading sign is considered to apply to all fields (but only if no additional signs appear). Otherwise the traditional PostgreSQL interpretation is used. To avoid ambiguity, it's recommended to attach an explicit sign to each field if any field is negative.

Internally, interval values are stored as three integral fields: months, days, and microseconds. These fields are kept separate because the number of days in a month varies, while a day can have 23 or 25 hours if a daylight savings time transition is involved. An interval input string that uses other units is normalized into this format, and then reconstructed in a standardized way for output, for example:

```
SELECT '2 years 15 months 100 weeks 99 hours 123456789
 milliseconds'::interval;
 interval
---------------------------------------
 3 years 3 mons 700 days 133:17:36.789
```

Here weeks, which are understood as "7 days", have been kept separate, while the smaller and larger time units were combined and normalized.

Input field values can have fractional parts, for example '1.5 weeks' or '01:02:03.45'. However, because interval internally stores only integral fields, fractional values must be converted into smaller units. Fractional parts of units greater than months are truncated to be an integer number of months, e.g. '1.5 years' becomes '1 year 6 mons'. Fractional parts of weeks and days are computed to be an integer number of days and microseconds, assuming 30 days per month and 24 hours per day, e.g., '1.75 months' becomes 1 mon 22 days 12:00:00. Only seconds will ever be shown as fractional on output.

<span id="page-0-0"></span>[Table 8.17](#page-0-0) shows some examples of valid interval input.

**Table 8.17. Interval Input**

| Example                                               | Description                                                                        |
|-------------------------------------------------------|------------------------------------------------------------------------------------|
| 1-2                                                   | SQL standard format: 1 year 2 months                                               |
| 3 4:05:06                                             | SQL standard format: 3 days 4 hours 5 minutes 6<br>seconds                         |
| 1 year 2 months 3 days 4 hours 5<br>minutes 6 seconds | Traditional Postgres format: 1 year 2 months 3<br>days 4 hours 5 minutes 6 seconds |
| P1Y2M3DT4H5M6S                                        | ISO 8601 "format with designators": same<br>meaning as above                       |
| P0001-02-03T04:05:06                                  | ISO 8601 "alternative format": same meaning as<br>above                            |

## **8.5.5. Interval Output**

As previously explained, PostgreSQL stores interval values as months, days, and microseconds. For output, the months field is converted to years and months by dividing by 12. The days field is shown as-is. The microseconds field is converted to hours, minutes, seconds, and fractional seconds. Thus months, minutes, and seconds will never be shown as exceeding the ranges 0–11, 0–59, and 0– 59 respectively, while the displayed years, days, and hours fields can be quite large. (The [justi](#page-108-0)[fy\\_days](#page-108-0) and [justify\\_hours](#page-108-1) functions can be used if it is desirable to transpose large days or hours values into the next higher field.)

The output format of the interval type can be set to one of the four styles sql\_standard, postgres, postgres\_verbose, or iso\_8601, using the command SET intervalstyle. The default is the postgres format. [Table 8.18](#page-0-1) shows examples of each output style.

The sql\_standard style produces output that conforms to the SQL standard's specification for interval literal strings, if the interval value meets the standard's restrictions (either year-month only or day-time only, with no mixing of positive and negative components). Otherwise the output looks like a standard year-month literal string followed by a day-time literal string, with explicit signs added to disambiguate mixed-sign intervals.

The output of the postgres style matches the output of PostgreSQL releases prior to 8.4 when the DateStyle parameter was set to ISO.

The output of the postgres\_verbose style matches the output of PostgreSQL releases prior to 8.4 when the DateStyle parameter was set to non-ISO output.

The output of the iso\_8601 style matches the "format with designators" described in section 4.4.3.2 of the ISO 8601 standard.

<span id="page-0-1"></span>**Table 8.18. Interval Output Style Examples**

| Style Specification | Year-Month Interval | Day-Time Interval | Mixed Interval   |
|---------------------|---------------------|-------------------|------------------|
| sql_standard        | 1-2                 | 3 4:05:06         | -1-2 +3 -4:05:06 |

| Style Specification              | Year-Month Interval | Day-Time Interval                 | Mixed Interval                                          |
|----------------------------------|---------------------|-----------------------------------|---------------------------------------------------------|
| postgres                         | 1 year 2 mons       | 3 days 04:05:06                   | -1 year -2 mons +3<br>days -04:05:06                    |
| postgres_verbose @ 1 year 2 mons |                     | @ 3 days 4 hours 5<br>mins 6 secs | @ 1 year 2 mons -3<br>days 4 hours 5 mins 6<br>secs ago |
| iso_8601                         | P1Y2M               | P3DT4H5M6S                        | P-1Y-2M3D<br>T-4H-5M-6S                                 |