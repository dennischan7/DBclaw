---
source: MySQL 8.4 Reference
title: 00_Front_Matter
---

# **MySQL 8.4 Reference Manual Including MySQL NDB Cluster 8.4**

### **Abstract**

This is the MySQL Reference Manual. It documents MySQL 8.4 through 8.4.8, as well as NDB Cluster 8.4 through 8.4.8, respectively. It may include documentation of features of MySQL versions that have not yet been released. For information about which versions have been released, see the [MySQL 8.4 Release Notes.](https://dev.mysql.com/doc/relnotes/mysql/8.4/en/)

**MySQL 8.4 features.** This manual describes features that are not included in every edition of MySQL 8.4; such features may not be included in the edition of MySQL 8.4 licensed to you. If you have any questions about the features included in your edition of MySQL 8.4, refer to your MySQL 8.4 license agreement or contact your Oracle sales representative.

For notes detailing the changes in each release, see the [MySQL 8.4 Release Notes.](https://dev.mysql.com/doc/relnotes/mysql/8.4/en/)

For legal information, including licensing information, see the [Preface and Legal Notices](#page-26-0).

For help with using MySQL, please visit the [MySQL Forums,](http://forums.mysql.com) where you can discuss your issues with other MySQL users.

Document generated on: 2026-04-08 (revision: 84563)

# **Table of Contents**

| Preface and Legal Notices xxvii                                                    |     |
|------------------------------------------------------------------------------------|-----|
| 1 General Information 1                                                            |     |
| 1.1 About This Manual 2                                                            |     |
| 1.2 Overview of the MySQL Database Management System 4                             |     |
| 1.2.1 What is MySQL? 4                                                             |     |
| 1.2.2 The Main Features of MySQL 5                                                 |     |
| 1.2.3 History of MySQL 8                                                           |     |
| 1.3 MySQL Releases: Innovation and LTS 9                                           |     |
| 1.4 What Is New in MySQL 8.4 since MySQL 8.0 10                                    |     |
| 1.5 Server and Status Variables and Options Added, Deprecated, or Removed in MySQL |     |
| 8.4 since 8.0                                                                      | 33  |
| 1.6 How to Report Bugs or Problems 41                                              |     |
| 1.7 MySQL Standards Compliance 45                                                  |     |
| 1.7.1 MySQL Extensions to Standard SQL 46                                          |     |
| 1.7.2 MySQL Differences from Standard SQL 49                                       |     |
| 1.7.3 How MySQL Deals with Constraints 52                                          |     |
| 2 Installing MySQL                                                                 | 55  |
| 2.1 General Installation Guidance 57                                               |     |
| 2.1.1 Supported Platforms 57                                                       |     |
| 2.1.2 Which MySQL Version and Distribution to Install 57                           |     |
| 2.1.3 How to Get MySQL 58                                                          |     |
| 2.1.4 Verifying Package Integrity Using MD5 Checksums or GnuPG 59                  |     |
| 2.1.5 Installation Layouts 74                                                      |     |
| 2.1.6 Compiler-Specific Build Characteristics 75                                   |     |
| 2.2 Installing MySQL on Unix/Linux Using Generic Binaries 75                       |     |
| 2.3 Installing MySQL on Microsoft Windows 78                                       |     |
| 2.3.1 Choosing an Installation Package 81                                          |     |
| 2.3.2 Configuration: Using MySQL Configurator 82                                   |     |
| 2.3.3 Configuration: Manually 100                                                  |     |
| 2.3.4 Troubleshooting a Microsoft Windows MySQL Server Installation 108            |     |
| 2.3.5 Windows Postinstallation Procedures                                          | 109 |
| 2.3.6 Windows Platform Restrictions 111                                            |     |
| 2.4 Installing MySQL on macOS 113                                                  |     |
| 2.4.1 General Notes on Installing MySQL on macOS 113                               |     |
| 2.4.2 Installing MySQL on macOS Using Native Packages 114                          |     |
| 2.4.3 Installing and Using the MySQL Launch Daemon 116                             |     |
| 2.4.4 Installing and Using the MySQL Preference Pane 119                           |     |
| 2.5 Installing MySQL on Linux 123                                                  |     |
| 2.5.1 Installing MySQL on Linux Using the MySQL Yum Repository 124                 |     |
| 2.5.2 Installing MySQL on Linux Using the MySQL APT Repository 129                 |     |
| 2.5.3 Using the MySQL SLES Repository 138                                          |     |
| 2.5.4 Installing MySQL on Linux Using RPM Packages from Oracle 143                 |     |
| 2.5.5 Installing MySQL on Linux Using Debian Packages from Oracle 148              |     |
| 2.5.6 Deploying MySQL on Linux with Docker Containers 149                          |     |
| 2.5.7 Installing MySQL on Linux from the Native Software Repositories 161          |     |
| 2.5.8 Installing MySQL on Linux with Juju 163                                      |     |
| 2.5.9 Managing MySQL Server with systemd 163                                       |     |
| 2.6 Installing MySQL Using Unbreakable Linux Network (ULN)                         | 168 |
| 2.7 Installing MySQL on Solaris 169                                                |     |
| 2.7.1 Installing MySQL on Solaris Using a Solaris PKG                              | 169 |
| 2.8 Installing MySQL from Source 170                                               |     |
| 2.8.1 Source Installation Methods 171                                              |     |
| 2.8.2 Source Installation Prerequisites                                            | 171 |
| 2.8.3 MySQL Layout for Source Installation 173                                     |     |
| 2.8.4 Installing MySQL Using a Standard Source Distribution 173                    |     |

| 2.8.5 Installing MySQL Using a Development Source Tree 177                  |     |
|-----------------------------------------------------------------------------|-----|
| 2.8.6 Configuring SSL Library Support 178                                   |     |
| 2.8.7 MySQL Source-Configuration Options 179                                |     |
| 2.8.8 Dealing with Problems Compiling MySQL 204                             |     |
| 2.8.9 MySQL Configuration and Third-Party Tools 205                         |     |
| 2.8.10 Generating MySQL Doxygen Documentation Content 205                   |     |
| 2.9 Postinstallation Setup and Testing 206                                  |     |
| 2.9.1 Initializing the Data Directory                                       | 207 |
| 2.9.2 Starting the Server 212                                               |     |
| 2.9.3 Testing the Server 215                                                |     |
| 2.9.4 Securing the Initial MySQL Account 216                                |     |
| 2.9.5 Starting and Stopping MySQL Automatically 218                         |     |
| 2.10 Perl Installation Notes 219                                            |     |
| 2.10.1 Installing Perl on Unix 220                                          |     |
| 2.10.2 Installing ActiveState Perl on Windows 220                           |     |
| 2.10.3 Problems Using the Perl DBI/DBD Interface 221                        |     |
| 3 Upgrading MySQL                                                           | 223 |
| 3.1 Before You Begin 223                                                    |     |
| 3.2 Upgrade Paths 224                                                       |     |
| 3.3 Upgrade Best Practices 225                                              |     |
| 3.4 What the MySQL Upgrade Process Upgrades 228                             |     |
| 3.5 Changes in MySQL 8.4 230                                                |     |
| 3.6 Preparing Your Installation for Upgrade 232                             |     |
| 3.7 Upgrading MySQL Binary or Package-based Installations on Unix/Linux 234 |     |
| 3.8 Upgrading MySQL with the MySQL Yum Repository 238                       |     |
| 3.9 Upgrading MySQL with the MySQL APT Repository 240                       |     |
| 3.10 Upgrading MySQL with the MySQL SLES Repository 240                     |     |
| 3.11 Upgrading MySQL on Windows 240                                         |     |
| 3.12 Upgrading a Docker Installation of MySQL 241                           |     |
| 3.13 Upgrade Troubleshooting 241                                            |     |
| 3.14 Rebuilding or Repairing Tables or Indexes 242                          |     |
| 3.15 Copying MySQL Databases to Another Machine 243                         |     |
| 4 Downgrading MySQL 245                                                     |     |
| 5 Tutorial 247                                                              |     |
| 5.1 Connecting to and Disconnecting from the Server 247                     |     |
| 5.2 Entering Queries 248                                                    |     |
| 5.3 Creating and Using a Database 251                                       |     |
| 5.3.1 Creating and Selecting a Database 252                                 |     |
| 5.3.2 Creating a Table 253                                                  |     |
| 5.3.3 Loading Data into a Table 254                                         |     |
| 5.3.4 Retrieving Information from a Table 255                               |     |
| 5.4 Getting Information About Databases and Tables 268                      |     |
| 5.5 Using mysql in Batch Mode 269                                           |     |
| 5.6 Examples of Common Queries 270                                          |     |
| 5.6.1 The Maximum Value for a Column 271                                    |     |
| 5.6.2 The Row Holding the Maximum of a Certain Column 271                   |     |
| 5.6.3 Maximum of Column per Group 271                                       |     |
| 5.6.4 The Rows Holding the Group-wise Maximum of a Certain Column 272       |     |
| 5.6.5 Using User-Defined Variables 273                                      |     |
| 5.6.6 Using Foreign Keys 273                                                |     |
| 5.6.7 Searching on Two Keys 275                                             |     |
| 5.6.8 Calculating Visits Per Day 275                                        |     |
| 5.6.9 Using AUTO_INCREMENT 276                                              |     |
| 5.7 Using MySQL with Apache 278                                             |     |
| 6 MySQL Programs 281                                                        |     |
| 6.1 Overview of MySQL Programs 282                                          |     |
| 6.2 Using MySQL Programs 285                                                |     |
| 6.2.1 Invoking MySQL Programs 285                                           |     |
|                                                                             |     |

| 6.2.2 Specifying Program Options 286                                         |     |
|------------------------------------------------------------------------------|-----|
| 6.2.3 Command Options for Connecting to the Server 300                       |     |
| 6.2.4 Connecting to the MySQL Server Using Command Options 312               |     |
| 6.2.5 Connecting to the Server Using URI-Like Strings or Key-Value Pairs 315 |     |
| 6.2.6 Connecting to the Server Using DNS SRV Records 322                     |     |
| 6.2.7 Connection Transport Protocols 323                                     |     |
| 6.2.8 Connection Compression Control 324                                     |     |
| 6.2.9 Setting Environment Variables 328                                      |     |
| 6.3 Server and Server-Startup Programs                                       | 329 |
| 6.3.1 mysqld — The MySQL Server 329                                          |     |
| 6.3.2 mysqld_safe — MySQL Server Startup Script 329                          |     |
| 6.3.3 mysql.server — MySQL Server Startup Script 338                         |     |
| 6.3.4 mysqld_multi — Manage Multiple MySQL Servers 340                       |     |
| 6.4 Installation-Related Programs 345                                        |     |
| 6.4.1 comp_err — Compile MySQL Error Message File 345                        |     |
|                                                                              |     |
| 6.4.2 mysql_secure_installation — Improve MySQL Installation Security 347    |     |
| 6.4.3 mysql_tzinfo_to_sql — Load the Time Zone Tables 353                    |     |
| 6.5 Client Programs 353                                                      |     |
| 6.5.1 mysql — The MySQL Command-Line Client 353                              |     |
| 6.5.2 mysqladmin — A MySQL Server Administration Program                     | 399 |
| 6.5.3 mysqlcheck — A Table Maintenance Program 414                           |     |
| 6.5.4 mysqldump — A Database Backup Program                                  | 428 |
| 6.5.5 mysqlimport — A Data Import Program 465                                |     |
| 6.5.6 mysqlshow — Display Database, Table, and Column Information 479        |     |
| 6.5.7 mysqlslap — A Load Emulation Client 491                                |     |
| 6.6 Administrative and Utility Programs 508                                  |     |
| 6.6.1 ibd2sdi — InnoDB Tablespace SDI Extraction Utility 508                 |     |
| 6.6.2 innochecksum — Offline InnoDB File Checksum Utility 513                |     |
| 6.6.3 myisam_ftdump — Display Full-Text Index information 520                |     |
| 6.6.4 myisamchk — MyISAM Table-Maintenance Utility 521                       |     |
| 6.6.5 myisamlog — Display MyISAM Log File Contents 540                       |     |
| 6.6.6 myisampack — Generate Compressed, Read-Only MyISAM Tables 541          |     |
| 6.6.7 mysql_config_editor — MySQL Configuration Utility                      | 547 |
| 6.6.8 mysql_migrate_keyring — Keyring Key Migration Utility 554              |     |
| 6.6.9 mysqlbinlog — Utility for Processing Binary Log Files 563              |     |
| 6.6.10 mysqldumpslow — Summarize Slow Query Log Files 593                    |     |
| 6.7 Program Development Utilities 596                                        |     |
| 6.7.1 mysql_config — Display Options for Compiling Clients 596               |     |
| 6.7.2 my_print_defaults — Display Options from Option Files 597              |     |
| 6.8 Miscellaneous Programs 599                                               |     |
| 6.8.1 perror — Display MySQL Error Message Information 599                   |     |
|                                                                              |     |
| 6.9 Environment Variables 599<br>6.10 Unix Signal Handling in MySQL 602      |     |
|                                                                              |     |
| 7 MySQL Server Administration 603                                            |     |
| 7.1 The MySQL Server 604                                                     |     |
| 7.1.1 Configuring the Server 605                                             |     |
| 7.1.2 Server Configuration Defaults                                          | 606 |
| 7.1.3 Server Configuration Validation 606                                    |     |
| 7.1.4 Server Option, System Variable, and Status Variable Reference 607      |     |
| 7.1.5 Server System Variable Reference 656                                   |     |
| 7.1.6 Server Status Variable Reference 681                                   |     |
| 7.1.7 Server Command Options 698                                             |     |
| 7.1.8 Server System Variables                                                | 723 |
| 7.1.9 Using System Variables 878                                             |     |
| 7.1.10 Server Status Variables 909                                           |     |
| 7.1.11 Server SQL Modes 933                                                  |     |
| 7.1.12 Connection Management 945                                             |     |
| 7.1.13 IPv6 Support 952                                                      |     |
|                                                                              |     |

| 7.1.14 Network Namespace Support                                         |       |
|--------------------------------------------------------------------------|-------|
| 7.1.15 MySQL Server Time Zone Support                                    | . 961 |
| 7.1.16 Resource Groups                                                   | . 966 |
| 7.1.17 Server-Side Help Support                                          | . 971 |
| 7.1.18 Server Tracking of Client Session State                           | . 971 |
| 7.1.19 The Server Shutdown Process                                       |       |
| 7.2 The MySQL Data Directory                                             |       |
| 7.3 The mysql System Schema                                              |       |
| 7.4 MySQL Server Logs                                                    |       |
| 7.4.1 Selecting General Query Log and Slow Query Log Output Destinations |       |
| 7.4.2 The Error Log                                                      |       |
| 7.4.3 The General Query Log                                              |       |
| 7.4.4 The Binary Log                                                     |       |
| 7.4.5 The Slow Query Log                                                 |       |
| 7.4.6 Server Log Maintenance                                             |       |
| 7.5 MySQL Components                                                     |       |
| 7.5.1 Installing and Uninstalling Components                             |       |
| 7.5.2 Obtaining Component Information                                    |       |
| 7.5.3 Error Log Components                                               |       |
| 7.5.4 Query Attribute Components                                         |       |
| 7.5.5 Scheduler Component                                                |       |
| 7.6 MySQL Server Plugins                                                 |       |
| 7.6.1 Installing and Uninstalling Plugins                                |       |
| 7.6.2 Obtaining Server Plugin Information                                |       |
|                                                                          |       |
| 7.6.3 MySQL Enterprise Thread Pool                                       |       |
| 7.6.4 The Rewriter Query Rewrite Plugin                                  |       |
| 7.6.5 The ddl_rewriter Plugin                                            |       |
| 7.6.6 Version Tokens                                                     |       |
| 7.6.7 The Clone Plugin                                                   |       |
| 7.6.8 The Keyring Proxy Bridge Plugin                                    |       |
| 7.6.9 MySQL Plugin Services                                              |       |
| 7.7 MySQL Server Loadable Functions                                      |       |
| 7.7.1 Installing and Uninstalling Loadable Functions                     |       |
| 7.7.2 Obtaining Information About Loadable Functions                     |       |
| 7.8 Running Multiple MySQL Instances on One Machine                      | 1103  |
| 7.8.1 Setting Up Multiple Data Directories                               |       |
| 7.8.2 Running Multiple MySQL Instances on Windows                        |       |
| 7.8.3 Running Multiple MySQL Instances on Unix                           |       |
| 7.8.4 Using Client Programs in a Multiple-Server Environment             |       |
| 7.9 Debugging MySQL                                                      |       |
| 7.9.1 Debugging a MySQL Server                                           |       |
| 7.9.2 Debugging a MySQL Client                                           |       |
| 7.9.3 The LOCK_ORDER Tool                                                |       |
| 7.9.4 The DBUG Package                                                   |       |
| 8 Security                                                               |       |
| 8.1 General Security Issues                                              | 1126  |
| 8.1.1 Security Guidelines                                                |       |
| 8.1.2 Keeping Passwords Secure                                           |       |
| 8.1.3 Making MySQL Secure Against Attackers                              | 1131  |
| 8.1.4 Security-Related mysqld Options and Variables                      |       |
| 8.1.5 How to Run MySQL as a Normal User                                  |       |
| 8.1.6 Security Considerations for LOAD DATA LOCAL                        |       |
| 8.1.7 Client Programming Security Guidelines                             |       |
| 8.2 Access Control and Account Management                                |       |
| 8.2.1 Account User Names and Passwords                                   |       |
| 8.2.2 Privileges Provided by MySQL                                       |       |
| 8.2.3 Grant Tables                                                       |       |
| 8.2.4 Specifying Account Names                                           |       |
|                                                                          |       |

| 8.2.5 Specifying Role Names 1172                                          |      |
|---------------------------------------------------------------------------|------|
| 8.2.6 Access Control, Stage 1: Connection Verification 1173               |      |
| 8.2.7 Access Control, Stage 2: Request Verification 1176                  |      |
| 8.2.8 Adding Accounts, Assigning Privileges, and Dropping Accounts 1178   |      |
| 8.2.9 Reserved Accounts 1181                                              |      |
| 8.2.10 Using Roles 1181                                                   |      |
| 8.2.11 Account Categories 1188                                            |      |
|                                                                           |      |
| 8.2.12 Privilege Restriction Using Partial Revokes 1191                   |      |
| 8.2.13 When Privilege Changes Take Effect 1197                            |      |
| 8.2.14 Assigning Account Passwords 1198                                   |      |
| 8.2.15 Password Management 1199                                           |      |
| 8.2.16 Server Handling of Expired Passwords 1210                          |      |
| 8.2.17 Pluggable Authentication 1212                                      |      |
| 8.2.18 Multifactor Authentication 1218                                    |      |
| 8.2.19 Proxy Users                                                        | 1221 |
| 8.2.20 Account Locking 1229                                               |      |
| 8.2.21 Setting Account Resource Limits 1229                               |      |
| 8.2.22 Troubleshooting Problems Connecting to MySQL 1231                  |      |
| 8.2.23 SQL-Based Account Activity Auditing 1235                           |      |
|                                                                           |      |
| 8.3 Using Encrypted Connections 1237                                      |      |
| 8.3.1 Configuring MySQL to Use Encrypted Connections 1238                 |      |
| 8.3.2 Encrypted Connection TLS Protocols and Ciphers 1246                 |      |
| 8.3.3 Creating SSL and RSA Certificates and Keys 1252                     |      |
| 8.3.4 Connecting to MySQL Remotely from Windows with SSH 1260             |      |
| 8.3.5 Reusing SSL Sessions 1261                                           |      |
| 8.4 Security Components and Plugins 1263                                  |      |
| 8.4.1 Authentication Plugins 1264                                         |      |
| 8.4.2 Connection Control Plugins 1357                                     |      |
| 8.4.3 The Password Validation Component 1363                              |      |
| 8.4.4 The MySQL Keyring 1375                                              |      |
|                                                                           |      |
| 8.4.5 MySQL Enterprise Audit 1434                                         |      |
| 8.4.6 The Audit Message Component 1517                                    |      |
| 8.4.7 MySQL Enterprise Firewall 1520                                      |      |
| 8.5 MySQL Enterprise Data Masking and De-Identification 1549              |      |
| 8.5.1 Data-Masking Components Versus the Data-Masking Plugin 1551         |      |
| 8.5.2 MySQL Enterprise Data Masking and De-Identification Components 1551 |      |
| 8.5.3 MySQL Enterprise Data Masking and De-Identification Plugin 1577     |      |
| 8.6 MySQL Enterprise Encryption 1593                                      |      |
| 8.6.1 MySQL Enterprise Encryption Installation and Upgrading 1594         |      |
| 8.6.2 Configuring MySQL Enterprise Encryption                             | 1595 |
| 8.6.3 MySQL Enterprise Encryption Usage and Examples 1595                 |      |
|                                                                           |      |
| 8.6.4 MySQL Enterprise Encryption Function Reference                      | 1597 |
| 8.6.5 MySQL Enterprise Encryption Component Function Descriptions 1597    |      |
| 8.7 SELinux 1601                                                          |      |
| 8.7.1 Check if SELinux is Enabled 1602                                    |      |
| 8.7.2 Changing the SELinux Mode 1602                                      |      |
| 8.7.3 MySQL Server SELinux Policies 1602                                  |      |
| 8.7.4 SELinux File Context 1603                                           |      |
| 8.7.5 SELinux TCP Port Context 1604                                       |      |
| 8.7.6 Troubleshooting SELinux 1605                                        |      |
| 8.8 FIPS Support 1606                                                     |      |
|                                                                           |      |
| 9 Backup and Recovery 1609                                                |      |
| 9.1 Backup and Recovery Types 1610                                        |      |
| 9.2 Database Backup Methods 1613                                          |      |
| 9.3 Example Backup and Recovery Strategy 1615                             |      |
| 9.3.1 Establishing a Backup Policy                                        | 1615 |
| 9.3.2 Using Backups for Recovery 1617                                     |      |
| 9.3.3 Backup Strategy Summary 1618                                        |      |
|                                                                           |      |

| 9.4 Using mysqldump for Backups 1618                                            |      |
|---------------------------------------------------------------------------------|------|
| 9.4.1 Dumping Data in SQL Format with mysqldump 1619                            |      |
| 9.4.2 Reloading SQL-Format Backups                                              | 1620 |
| 9.4.3 Dumping Data in Delimited-Text Format with mysqldump 1620                 |      |
| 9.4.4 Reloading Delimited-Text Format Backups 1621                              |      |
| 9.4.5 mysqldump Tips 1622                                                       |      |
| 9.5 Point-in-Time (Incremental) Recovery 1624                                   |      |
| 9.5.1 Point-in-Time Recovery Using Binary Log 1624                              |      |
| 9.5.2 Point-in-Time Recovery Using Event Positions 1625                         |      |
| 9.6 MyISAM Table Maintenance and Crash Recovery 1627                            |      |
| 9.6.1 Using myisamchk for Crash Recovery 1627                                   |      |
| 9.6.2 How to Check MyISAM Tables for Errors 1628                                |      |
| 9.6.3 How to Repair MyISAM Tables 1629                                          |      |
| 9.6.4 MyISAM Table Optimization 1631                                            |      |
| 9.6.5 Setting Up a MyISAM Table Maintenance Schedule 1631                       |      |
| 10 Optimization 1633                                                            |      |
| 10.1 Optimization Overview 1635                                                 |      |
| 10.2 Optimizing SQL Statements 1636                                             |      |
| 10.2.1 Optimizing SELECT Statements 1636                                        |      |
| 10.2.2 Optimizing Subqueries, Derived Tables, View References, and Common Table |      |
| Expressions 1686                                                                |      |
| 10.2.3 Optimizing INFORMATION_SCHEMA Queries 1699                               |      |
| 10.2.4 Optimizing Performance Schema Queries 1702                               |      |
| 10.2.5 Optimizing Data Change Statements 1704                                   |      |
| 10.2.6 Optimizing Database Privileges 1705                                      |      |
| 10.2.7 Other Optimization Tips                                                  | 1705 |
| 10.3 Optimization and Indexes 1706                                              |      |
| 10.3.1 How MySQL Uses Indexes 1706                                              |      |
| 10.3.2 Primary Key Optimization 1707                                            |      |
| 10.3.3 SPATIAL Index Optimization 1707                                          |      |
| 10.3.4 Foreign Key Optimization 1708                                            |      |
| 10.3.5 Column Indexes 1708                                                      |      |
| 10.3.6 Multiple-Column Indexes 1709                                             |      |
| 10.3.7 Verifying Index Usage 1711                                               |      |
| 10.3.8 InnoDB and MyISAM Index Statistics Collection 1711                       |      |
| 10.3.9 Comparison of B-Tree and Hash Indexes 1712                               |      |
| 10.3.10 Use of Index Extensions 1714                                            |      |
| 10.3.11 Optimizer Use of Generated Column Indexes 1716                          |      |
| 10.3.12 Invisible Indexes 1717                                                  |      |
| 10.3.13 Descending Indexes 1719                                                 |      |
| 10.3.14 Indexed Lookups from TIMESTAMP Columns 1721                             |      |
| 10.4 Optimizing Database Structure 1723                                         |      |
| 10.4.1 Optimizing Data Size 1723                                                |      |
| 10.4.2 Optimizing MySQL Data Types 1725                                         |      |
| 10.4.3 Optimizing for Many Tables 1726                                          |      |
| 10.4.4 Internal Temporary Table Use in MySQL 1727                               |      |
| 10.4.5 Limits on Number of Databases and Tables 1731                            |      |
| 10.4.6 Limits on Table Size 1731                                                |      |
| 10.4.7 Limits on Table Column Count and Row Size 1732                           |      |
| 10.5 Optimizing for InnoDB Tables                                               | 1735 |
| 10.5.1 Optimizing Storage Layout for InnoDB Tables 1735                         |      |
| 10.5.2 Optimizing InnoDB Transaction Management 1735                            |      |
| 10.5.3 Optimizing InnoDB Read-Only Transactions 1736                            |      |
| 10.5.4 Optimizing InnoDB Redo Logging 1737                                      |      |
| 10.5.5 Bulk Data Loading for InnoDB Tables 1738                                 |      |
| 10.5.6 Optimizing InnoDB Queries 1740                                           |      |
| 10.5.7 Optimizing InnoDB DDL Operations 1740                                    |      |
| 10.5.8 Optimizing InnoDB Disk I/O 1740                                          |      |
|                                                                                 |      |

| 10.5.9 Optimizing InnoDB Configuration Variables 1744                   |      |
|-------------------------------------------------------------------------|------|
| 10.5.10 Optimizing InnoDB for Systems with Many Tables 1745             |      |
| 10.6 Optimizing for MyISAM Tables 1745                                  |      |
| 10.6.1 Optimizing MyISAM Queries 1745                                   |      |
| 10.6.2 Bulk Data Loading for MyISAM Tables 1747                         |      |
| 10.6.3 Optimizing REPAIR TABLE Statements 1748                          |      |
| 10.7 Optimizing for MEMORY Tables 1749                                  |      |
| 10.8 Understanding the Query Execution Plan 1750                        |      |
| 10.8.1 Optimizing Queries with EXPLAIN 1750                             |      |
| 10.8.2 EXPLAIN Output Format 1751                                       |      |
| 10.8.3 Extended EXPLAIN Output Format 1764                              |      |
| 10.8.4 Obtaining Execution Plan Information for a Named Connection 1766 |      |
| 10.8.5 Estimating Query Performance 1767                                |      |
| 10.9 Controlling the Query Optimizer 1767                               |      |
| 10.9.1 Controlling Query Plan Evaluation 1767                           |      |
|                                                                         |      |
| 10.9.2 Switchable Optimizations 1768                                    |      |
| 10.9.3 Optimizer Hints 1778                                             |      |
| 10.9.4 Index Hints 1792                                                 |      |
| 10.9.5 The Optimizer Cost Model                                         | 1794 |
| 10.9.6 Optimizer Statistics 1798                                        |      |
| 10.10 Buffering and Caching 1801                                        |      |
| 10.10.1 InnoDB Buffer Pool Optimization 1801                            |      |
| 10.10.2 The MyISAM Key Cache 1801                                       |      |
| 10.10.3 Caching of Prepared Statements and Stored Programs 1805         |      |
| 10.11 Optimizing Locking Operations 1807                                |      |
| 10.11.1 Internal Locking Methods 1807                                   |      |
| 10.11.2 Table Locking Issues 1809                                       |      |
| 10.11.3 Concurrent Inserts                                              | 1811 |
| 10.11.4 Metadata Locking 1811                                           |      |
| 10.11.5 External Locking 1814                                           |      |
| 10.12 Optimizing the MySQL Server 1815                                  |      |
| 10.12.1 Optimizing Disk I/O 1815                                        |      |
|                                                                         |      |
| 10.12.2 Using Symbolic Links 1817                                       |      |
| 10.12.3 Optimizing Memory Use 1820                                      |      |
| 10.13 Measuring Performance (Benchmarking) 1826                         |      |
| 10.13.1 Measuring the Speed of Expressions and Functions 1827           |      |
| 10.13.2 Using Your Own Benchmarks 1827                                  |      |
| 10.13.3 Measuring Performance with performance_schema 1827              |      |
| 10.14 Examining Server Thread (Process) Information 1828                |      |
| 10.14.1 Accessing the Process List 1828                                 |      |
| 10.14.2 Thread Command Values 1830                                      |      |
| 10.14.3 General Thread States 1832                                      |      |
| 10.14.4 Replication Source Thread States 1838                           |      |
| 10.14.5 Replication I/O (Receiver) Thread States                        | 1839 |
| 10.14.6 Replication SQL Thread States 1840                              |      |
| 10.14.7 Replication Connection Thread States                            | 1842 |
| 10.14.8 NDB Cluster Thread States 1842                                  |      |
| 10.14.9 Event Scheduler Thread States 1843                              |      |
| 10.15 Tracing the Optimizer                                             | 1843 |
| 10.15.1 Typical Usage 1843                                              |      |
| 10.15.2 System Variables Controlling Tracing 1843                       |      |
| 10.15.3 Traceable Statements 1844                                       |      |
|                                                                         |      |
| 10.15.4 Tuning Trace Purging 1845                                       |      |
| 10.15.5 Tracing Memory Usage 1846                                       |      |
| 10.15.6 Privilege Checking 1846                                         |      |
| 10.15.7 Interaction with thedebug Option 1846                           |      |
| 10.15.8 The optimizer_trace System Variable 1846                        |      |
| 10.15.9 The end_markers_in_json System Variable 1846                    |      |

| 10.15.10 Selecting Optimizer Features to Trace                        | 1846 |
|-----------------------------------------------------------------------|------|
| 10.15.11 Trace General Structure 1847                                 |      |
| 10.15.12 Example 1847                                                 |      |
| 10.15.13 Displaying Traces in Other Applications                      | 1857 |
| 10.15.14 Preventing the Use of Optimizer Trace 1857                   |      |
| 10.15.15 Testing Optimizer Trace 1858                                 |      |
| 10.15.16 Optimizer Trace Implementation                               | 1858 |
| 11 Language Structure 1859                                            |      |
| 11.1 Literal Values 1859                                              |      |
| 11.1.1 String Literals 1859                                           |      |
| 11.1.2 Numeric Literals 1862                                          |      |
| 11.1.3 Date and Time Literals 1862                                    |      |
| 11.1.4 Hexadecimal Literals 1867                                      |      |
| 11.1.5 Bit-Value Literals                                             | 1869 |
| 11.1.6 Boolean Literals 1871                                          |      |
| 11.1.7 NULL Values 1871                                               |      |
| 11.2 Schema Object Names 1871                                         |      |
|                                                                       |      |
| 11.2.1 Identifier Length Limits 1873                                  |      |
| 11.2.2 Identifier Qualifiers 1874                                     |      |
| 11.2.3 Identifier Case Sensitivity 1875                               |      |
| 11.2.4 Mapping of Identifiers to File Names 1877                      |      |
| 11.2.5 Function Name Parsing and Resolution 1879                      |      |
| 11.3 Keywords and Reserved Words 1882                                 |      |
| 11.4 User-Defined Variables 1910                                      |      |
| 11.5 Expressions 1913                                                 |      |
| 11.6 Query Attributes 1917                                            |      |
| 11.7 Comments 1920                                                    |      |
| 12 Character Sets, Collations, Unicode 1923                           |      |
| 12.1 Character Sets and Collations in General 1924                    |      |
| 12.2 Character Sets and Collations in MySQL 1925                      |      |
| 12.2.1 Character Set Repertoire 1927                                  |      |
| 12.2.2 UTF-8 for Metadata 1929                                        |      |
| 12.3 Specifying Character Sets and Collations 1930                    |      |
| 12.3.1 Collation Naming Conventions 1930                              |      |
| 12.3.2 Server Character Set and Collation                             | 1931 |
| 12.3.3 Database Character Set and Collation 1932                      |      |
| 12.3.4 Table Character Set and Collation 1933                         |      |
| 12.3.5 Column Character Set and Collation 1934                        |      |
| 12.3.6 Character String Literal Character Set and Collation 1935      |      |
| 12.3.7 The National Character Set 1937                                |      |
| 12.3.8 Character Set Introducers 1937                                 |      |
| 12.3.9 Examples of Character Set and Collation Assignment 1939        |      |
| 12.3.10 Compatibility with Other DBMSs 1940                           |      |
| 12.4 Connection Character Sets and Collations 1940                    |      |
| 12.5 Configuring Application Character Set and Collation 1945         |      |
| 12.6 Error Message Character Set 1947                                 |      |
| 12.7 Column Character Set Conversion 1948                             |      |
| 12.8 Collation Issues 1949                                            |      |
|                                                                       |      |
| 12.8.1 Using COLLATE in SQL Statements 1949                           |      |
| 12.8.2 COLLATE Clause Precedence 1950                                 |      |
| 12.8.3 Character Set and Collation Compatibility 1950                 |      |
| 12.8.4 Collation Coercibility in Expressions 1950                     |      |
| 12.8.5 The binary Collation Compared to _bin Collations 1952          |      |
| 12.8.6 Examples of the Effect of Collation 1954                       |      |
| 12.8.7 Using Collation in INFORMATION_SCHEMA Searches 1955            |      |
| 12.9 Unicode Support 1957                                             |      |
| 12.9.1 The utf8mb4 Character Set (4-Byte UTF-8 Unicode Encoding) 1959 |      |
| 12.9.2 The utf8mb3 Character Set (3-Byte UTF-8 Unicode Encoding) 1960 |      |

| 12.9.3 The utf8 Character Set (Deprecated alias for utf8mb3) 1961            |      |
|------------------------------------------------------------------------------|------|
| 12.9.4 The ucs2 Character Set (UCS-2 Unicode Encoding) 1961                  |      |
| 12.9.5 The utf16 Character Set (UTF-16 Unicode Encoding) 1961                |      |
| 12.9.6 The utf16le Character Set (UTF-16LE Unicode Encoding) 1962            |      |
| 12.9.7 The utf32 Character Set (UTF-32 Unicode Encoding) 1962                |      |
| 12.9.8 Converting Between 3-Byte and 4-Byte Unicode Character Sets 1962      |      |
| 12.10 Supported Character Sets and Collations 1965                           |      |
| 12.10.1 Unicode Character Sets 1965                                          |      |
| 12.10.2 West European Character Sets 1973                                    |      |
| 12.10.3 Central European Character Sets 1974                                 |      |
| 12.10.4 South European and Middle East Character Sets 1975                   |      |
| 12.10.5 Baltic Character Sets 1976                                           |      |
| 12.10.6 Cyrillic Character Sets 1976                                         |      |
| 12.10.7 Asian Character Sets 1977                                            |      |
| 12.10.8 The Binary Character Set 1981                                        |      |
| 12.11 Restrictions on Character Sets 1982                                    |      |
| 12.12 Setting the Error Message Language 1982                                |      |
| 12.13 Adding a Character Set 1983                                            |      |
| 12.13.1 Character Definition Arrays 1985                                     |      |
| 12.13.2 String Collating Support for Complex Character Sets 1986             |      |
| 12.13.3 Multi-Byte Character Support for Complex Character Sets 1986         |      |
| 12.14 Adding a Collation to a Character Set 1986                             |      |
| 12.14.1 Collation Implementation Types 1987                                  |      |
| 12.14.2 Choosing a Collation ID 1990                                         |      |
| 12.14.3 Adding a Simple Collation to an 8-Bit Character Set                  | 1991 |
|                                                                              |      |
| 12.14.4 Adding a UCA Collation to a Unicode Character Set 1992               |      |
| 12.15 Character Set Configuration 1998                                       |      |
| 12.16 MySQL Server Locale Support 1999                                       |      |
| 13 Data Types 2005                                                           |      |
| 13.1 Numeric Data Types 2006                                                 |      |
| 13.1.1 Numeric Data Type Syntax 2006                                         |      |
| 13.1.2 Integer Types (Exact Value) - INTEGER, INT, SMALLINT, TINYINT,        |      |
| MEDIUMINT, BIGINT 2010                                                       |      |
| 13.1.3 Fixed-Point Types (Exact Value) - DECIMAL, NUMERIC 2010               |      |
| 13.1.4 Floating-Point Types (Approximate Value) - FLOAT, DOUBLE 2011         |      |
| 13.1.5 Bit-Value Type - BIT 2011                                             |      |
| 13.1.6 Numeric Type Attributes 2011                                          |      |
| 13.1.7 Out-of-Range and Overflow Handling 2013                               |      |
| 13.2 Date and Time Data Types 2014                                           |      |
| 13.2.1 Date and Time Data Type Syntax 2015                                   |      |
| 13.2.2 The DATE, DATETIME, and TIMESTAMP Types 2017                          |      |
| 13.2.3 The TIME Type 2019                                                    |      |
| 13.2.4 The YEAR Type 2019                                                    |      |
| 13.2.5 Automatic Initialization and Updating for TIMESTAMP and DATETIME 2020 |      |
| 13.2.6 Fractional Seconds in Time Values 2023                                |      |
| 13.2.7 What Calendar Is Used By MySQL? 2024                                  |      |
| 13.2.8 Conversion Between Date and Time Types 2025                           |      |
| 13.2.9 2-Digit Years in Dates 2026                                           |      |
| 13.3 String Data Types 2026                                                  |      |
| 13.3.1 String Data Type Syntax 2026                                          |      |
| 13.3.2 The CHAR and VARCHAR Types 2030                                       |      |
| 13.3.3 The BINARY and VARBINARY Types                                        | 2031 |
| 13.3.4 The BLOB and TEXT Types                                               | 2032 |
| 13.3.5 The ENUM Type 2034                                                    |      |
| 13.3.6 The SET Type 2037                                                     |      |
| 13.4 Spatial Data Types 2039                                                 |      |
| 13.4.1 Spatial Data Types 2041                                               |      |
| 13.4.2 The OpenGIS Geometry Model 2042                                       |      |
|                                                                              |      |

| 13.4.3 Supported Spatial Data Formats 2047                                  |      |
|-----------------------------------------------------------------------------|------|
| 13.4.4 Geometry Well-Formedness and Validity 2050                           |      |
| 13.4.5 Spatial Reference System Support 2051                                |      |
| 13.4.6 Creating Spatial Columns 2052                                        |      |
| 13.4.7 Populating Spatial Columns 2052                                      |      |
| 13.4.8 Fetching Spatial Data 2053                                           |      |
| 13.4.9 Optimizing Spatial Analysis 2054                                     |      |
| 13.4.10 Creating Spatial Indexes 2054                                       |      |
| 13.4.11 Using Spatial Indexes 2055                                          |      |
| 13.5 The JSON Data Type 2057                                                |      |
| 13.6 Data Type Default Values 2072                                          |      |
| 13.7 Data Type Storage Requirements 2075                                    |      |
| 13.8 Choosing the Right Type for a Column 2079                              |      |
| 13.9 Using Data Types from Other Database Engines 2079                      |      |
| 14 Functions and Operators 2081                                             |      |
| 14.1 Built-In Function and Operator Reference 2083                          |      |
| 14.2 Loadable Function Reference 2100                                       |      |
|                                                                             |      |
| 14.3 Type Conversion in Expression Evaluation 2104                          |      |
| 14.4 Operators 2108                                                         |      |
| 14.4.1 Operator Precedence 2109                                             |      |
| 14.4.2 Comparison Functions and Operators 2110                              |      |
| 14.4.3 Logical Operators 2117                                               |      |
| 14.4.4 Assignment Operators 2118                                            |      |
| 14.5 Flow Control Functions 2120                                            |      |
| 14.6 Numeric Functions and Operators 2122                                   |      |
| 14.6.1 Arithmetic Operators 2123                                            |      |
| 14.6.2 Mathematical Functions 2125                                          |      |
| 14.7 Date and Time Functions 2134                                           |      |
| 14.8 String Functions and Operators 2157                                    |      |
| 14.8.1 String Comparison Functions and Operators 2172                       |      |
| 14.8.2 Regular Expressions 2176                                             |      |
| 14.8.3 Character Set and Collation of Function Results 2183                 |      |
| 14.9 Full-Text Search Functions 2184                                        |      |
| 14.9.1 Natural Language Full-Text Searches 2186                             |      |
| 14.9.2 Boolean Full-Text Searches 2189                                      |      |
| 14.9.3 Full-Text Searches with Query Expansion 2194                         |      |
| 14.9.4 Full-Text Stopwords 2195                                             |      |
| 14.9.5 Full-Text Restrictions 2199                                          |      |
| 14.9.6 Fine-Tuning MySQL Full-Text Search 2200                              |      |
| 14.9.7 Adding a User-Defined Collation for Full-Text Indexing 2203          |      |
| 14.9.8 ngram Full-Text Parser 2205                                          |      |
| 14.9.9 MeCab Full-Text Parser Plugin 2207                                   |      |
| 14.10 Cast Functions and Operators 2211                                     |      |
| 14.11 XML Functions 2225                                                    |      |
|                                                                             |      |
| 14.12 Bit Functions and Operators 2235                                      |      |
| 14.13 Encryption and Compression Functions 2245                             |      |
| 14.14 Locking Functions 2253                                                |      |
| 14.15 Information Functions 2255                                            |      |
| 14.16 Spatial Analysis Functions                                            | 2266 |
| 14.16.1 Spatial Function Reference                                          | 2267 |
| 14.16.2 Argument Handling by Spatial Functions 2269                         |      |
| 14.16.3 Functions That Create Geometry Values from WKT Values 2270          |      |
| 14.16.4 Functions That Create Geometry Values from WKB Values 2272          |      |
| 14.16.5 MySQL-Specific Functions That Create Geometry Values 2274           |      |
| 14.16.6 Geometry Format Conversion Functions 2275                           |      |
| 14.16.7 Geometry Property Functions 2277                                    |      |
| 14.16.8 Spatial Operator Functions 2289                                     |      |
| 14.16.9 Functions That Test Spatial Relations Between Geometry Objects 2296 |      |

| 14.16.10 Spatial Geohash Functions 2307                                 |      |
|-------------------------------------------------------------------------|------|
| 14.16.11 Spatial GeoJSON Functions 2309                                 |      |
| 14.16.12 Spatial Aggregate Functions 2311                               |      |
| 14.16.13 Spatial Convenience Functions 2313                             |      |
| 14.17 JSON Functions 2316                                               |      |
| 14.17.1 JSON Function Reference 2317                                    |      |
| 14.17.2 Functions That Create JSON Values                               | 2319 |
| 14.17.3 Functions That Search JSON Values 2320                          |      |
|                                                                         |      |
| 14.17.4 Functions That Modify JSON Values 2334                          |      |
| 14.17.5 Functions That Return JSON Value Attributes 2343                |      |
| 14.17.6 JSON Table Functions 2345                                       |      |
| 14.17.7 JSON Schema Validation Functions 2350                           |      |
| 14.17.8 JSON Utility Functions 2356                                     |      |
| 14.18 Replication Functions 2361                                        |      |
| 14.18.1 Group Replication Functions 2362                                |      |
| 14.18.2 Functions Used with Global Transaction Identifiers (GTIDs) 2370 |      |
| 14.18.3 Asynchronous Replication Channel Failover Functions 2372        |      |
| 14.18.4 Position-Based Synchronization Functions                        | 2377 |
| 14.19 Aggregate Functions 2378                                          |      |
| 14.19.1 Aggregate Function Descriptions 2378                            |      |
| 14.19.2 GROUP BY Modifiers 2388                                         |      |
| 14.19.3 MySQL Handling of GROUP BY 2394                                 |      |
| 14.19.4 Detection of Functional Dependence 2397                         |      |
| 14.20 Window Functions 2400                                             |      |
| 14.20.1 Window Function Descriptions 2401                               |      |
| 14.20.2 Window Function Concepts and Syntax 2407                        |      |
|                                                                         |      |
| 14.20.3 Window Function Frame Specification 2411                        |      |
| 14.20.4 Named Windows 2414                                              |      |
| 14.20.5 Window Function Restrictions 2415                               |      |
| 14.21 Performance Schema Functions 2416                                 |      |
| 14.22 Internal Functions 2419                                           |      |
| 14.23 Miscellaneous Functions 2420                                      |      |
| 14.24 Precision Math                                                    | 2434 |
| 14.24.1 Types of Numeric Values 2434                                    |      |
| 14.24.2 DECIMAL Data Type Characteristics 2435                          |      |
| 14.24.3 Expression Handling 2436                                        |      |
| 14.24.4 Rounding Behavior                                               | 2437 |
| 14.24.5 Precision Math Examples 2438                                    |      |
| 15 SQL Statements 2443                                                  |      |
| 15.1 Data Definition Statements 2444                                    |      |
| 15.1.1 Atomic Data Definition Statement Support 2444                    |      |
| 15.1.2 ALTER DATABASE Statement 2448                                    |      |
| 15.1.3 ALTER EVENT Statement 2453                                       |      |
| 15.1.4 ALTER FUNCTION Statement 2455                                    |      |
| 15.1.5 ALTER INSTANCE Statement 2455                                    |      |
|                                                                         |      |
| 15.1.6 ALTER LOGFILE GROUP Statement                                    | 2457 |
| 15.1.7 ALTER PROCEDURE Statement 2458                                   |      |
| 15.1.8 ALTER SERVER Statement 2459                                      |      |
| 15.1.9 ALTER TABLE Statement 2459                                       |      |
| 15.1.10 ALTER TABLESPACE Statement 2482                                 |      |
| 15.1.11 ALTER VIEW Statement 2484                                       |      |
| 15.1.12 CREATE DATABASE Statement 2484                                  |      |
| 15.1.13 CREATE EVENT Statement 2485                                     |      |
| 15.1.14 CREATE FUNCTION Statement 2489                                  |      |
| 15.1.15 CREATE INDEX Statement 2489                                     |      |
| 15.1.16 CREATE LOGFILE GROUP Statement 2503                             |      |
| 15.1.17 CREATE PROCEDURE and CREATE FUNCTION Statements 2505            |      |
| 15.1.18 CREATE SERVER Statement                                         | 2510 |
|                                                                         |      |

| 15.1.19 CREATE SPATIAL REFERENCE SYSTEM Statement                   | 2511 |
|---------------------------------------------------------------------|------|
| 15.1.20 CREATE TABLE Statement 2516                                 |      |
| 15.1.21 CREATE TABLESPACE Statement 2574                            |      |
| 15.1.22 CREATE TRIGGER Statement 2581                               |      |
| 15.1.23 CREATE VIEW Statement 2584                                  |      |
| 15.1.24 DROP DATABASE Statement 2587                                |      |
| 15.1.25 DROP EVENT Statement 2588                                   |      |
| 15.1.26 DROP FUNCTION Statement 2588                                |      |
| 15.1.27 DROP INDEX Statement 2589                                   |      |
| 15.1.28 DROP LOGFILE GROUP Statement 2589                           |      |
| 15.1.29 DROP PROCEDURE and DROP FUNCTION Statements 2589            |      |
| 15.1.30 DROP SERVER Statement 2590                                  |      |
| 15.1.31 DROP SPATIAL REFERENCE SYSTEM Statement 2590                |      |
| 15.1.32 DROP TABLE Statement 2591                                   |      |
| 15.1.33 DROP TABLESPACE Statement 2592                              |      |
| 15.1.34 DROP TRIGGER Statement 2593                                 |      |
| 15.1.35 DROP VIEW Statement 2593                                    |      |
|                                                                     |      |
| 15.1.36 RENAME TABLE Statement 2593                                 |      |
| 15.1.37 TRUNCATE TABLE Statement 2595                               |      |
| 15.2 Data Manipulation Statements 2596                              |      |
| 15.2.1 CALL Statement 2596                                          |      |
| 15.2.2 DELETE Statement 2598                                        |      |
| 15.2.3 DO Statement 2602                                            |      |
| 15.2.4 EXCEPT Clause 2602                                           |      |
| 15.2.5 HANDLER Statement 2603                                       |      |
| 15.2.6 IMPORT TABLE Statement 2605                                  |      |
| 15.2.7 INSERT Statement 2607                                        |      |
| 15.2.8 INTERSECT Clause 2617                                        |      |
| 15.2.9 LOAD DATA Statement                                          | 2618 |
| 15.2.10 LOAD XML Statement 2629                                     |      |
| 15.2.11 Parenthesized Query Expressions 2636                        |      |
| 15.2.12 REPLACE Statement 2638                                      |      |
| 15.2.13 SELECT Statement 2641                                       |      |
| 15.2.14 Set Operations with UNION, INTERSECT, and EXCEPT 2656       |      |
| 15.2.15 Subqueries 2661                                             |      |
| 15.2.16 TABLE Statement 2676                                        |      |
| 15.2.17 UPDATE Statement 2679                                       |      |
| 15.2.18 UNION Clause 2682                                           |      |
| 15.2.19 VALUES Statement 2683                                       |      |
| 15.2.20 WITH (Common Table Expressions) 2685                        |      |
| 15.3 Transactional and Locking Statements                           | 2696 |
|                                                                     |      |
| 15.3.1 START TRANSACTION, COMMIT, and ROLLBACK Statements 2696      |      |
| 15.3.2 Statements That Cannot Be Rolled Back 2699                   |      |
| 15.3.3 Statements That Cause an Implicit Commit 2699                |      |
| 15.3.4 SAVEPOINT, ROLLBACK TO SAVEPOINT, and RELEASE SAVEPOINT      |      |
| Statements 2700                                                     |      |
| 15.3.5 LOCK INSTANCE FOR BACKUP and UNLOCK INSTANCE Statements 2701 |      |
| 15.3.6 LOCK TABLES and UNLOCK TABLES Statements 2702                |      |
| 15.3.7 SET TRANSACTION Statement 2707                               |      |
| 15.3.8 XA Transactions 2710                                         |      |
| 15.4 Replication Statements 2715                                    |      |
| 15.4.1 SQL Statements for Controlling Source Servers 2715           |      |
| 15.4.2 SQL Statements for Controlling Replica Servers 2718          |      |
| 15.4.3 SQL Statements for Controlling Group Replication 2740        |      |
| 15.5 Prepared Statements 2742                                       |      |
| 15.5.1 PREPARE Statement 2745                                       |      |
| 15.5.2 EXECUTE Statement 2747                                       |      |
| 15.5.3 DEALLOCATE PREPARE Statement 2747                            |      |
|                                                                     |      |

| 15.6 Compound Statement Syntax                             | 2748 |
|------------------------------------------------------------|------|
| 15.6.1 BEGIN END Compound Statement                        |      |
| 15.6.2 Statement Labels                                    |      |
| 15.6.3 DECLARE Statement                                   |      |
| 15.6.4 Variables in Stored Programs                        |      |
| 15.6.5 Flow Control Statements                             |      |
| 15.6.6 Cursors                                             |      |
| 15.6.7 Condition Handling                                  |      |
| 15.6.8 Restrictions on Condition Handling                  |      |
|                                                            |      |
| 15.7 Database Administration Statements                    |      |
| 15.7.1 Account Management Statements                       |      |
| 15.7.2 Resource Group Management Statements                |      |
| 15.7.3 Table Maintenance Statements                        |      |
| 15.7.4 Component, Plugin, and Loadable Function Statements |      |
| 15.7.5 CLONE Statement                                     |      |
| 15.7.6 SET Statements                                      |      |
| 15.7.7 SHOW Statements                                     |      |
| 15.7.8 Other Administrative Statements                     |      |
| 15.8 Utility Statements                                    | 2931 |
| 15.8.1 DESCRIBE Statement                                  | 2931 |
| 15.8.2 EXPLAIN Statement                                   | 2931 |
| 15.8.3 HELP Statement                                      | 2940 |
| 15.8.4 USE Statement                                       | 2942 |
| 16 MySQL Data Dictionary                                   | 2943 |
| 16.1 Data Dictionary Schema                                | 2943 |
| 16.2 Removal of File-based Metadata Storage                | 2944 |
| 16.3 Transactional Storage of Dictionary Data              | 2945 |
| 16.4 Dictionary Object Cache                               |      |
| 16.5 INFORMATION_SCHEMA and Data Dictionary Integration    |      |
| 16.6 Serialized Dictionary Information (SDI)               |      |
| 16.7 Data Dictionary Usage Differences                     |      |
| 16.8 Data Dictionary Limitations                           |      |
| 17 The InnoDB Storage Engine                               |      |
| 17.1 Introduction to InnoDB                                |      |
| 17.1.1 Benefits of Using InnoDB Tables                     |      |
| 17.1.2 Best Practices for InnoDB Tables                    |      |
| 17.1.3 Verifying that InnoDB is the Default Storage Engine |      |
| 17.1.4 Testing and Benchmarking with InnoDB                |      |
| 17.2 InnoDB and the ACID Model                             |      |
| 17.3 InnoDB Multi-Versioning                               |      |
| 17.4 InnoDB Architecture                                   |      |
| 17.5 InnoDB In-Memory Structures                           |      |
| 17.5.1 Buffer Pool                                         |      |
| 17.5.1 Builer Fooi                                         |      |
|                                                            |      |
| 17.5.3 Adaptive Hash Index                                 |      |
| 17.5.4 Log Buffer                                          |      |
| 17.6 InnoDB On-Disk Structures                             |      |
| 17.6.1 Tables                                              |      |
| 17.6.2 Indexes                                             |      |
| 17.6.3 Tablespaces                                         |      |
| 17.6.4 Doublewrite Buffer                                  |      |
| 17.6.5 Redo Log                                            |      |
| 17.6.6 Undo Logs                                           |      |
| 17.7 InnoDB Locking and Transaction Model                  |      |
| 17.7.1 InnoDB Locking                                      |      |
| 17.7.2 InnoDB Transaction Model                            |      |
| 17.7.3 Locks Set by Different SQL Statements in InnoDB     |      |
| 17.7.4 Phantom Rows                                        | 3045 |

| 17.7.5 Deadlocks in InnoDB 3046                                              |      |
|------------------------------------------------------------------------------|------|
| 17.7.6 Transaction Scheduling 3052                                           |      |
| 17.8 InnoDB Configuration 3052                                               |      |
| 17.8.1 InnoDB Startup Configuration 3052                                     |      |
| 17.8.2 Configuring InnoDB for Read-Only Operation 3058                       |      |
| 17.8.3 InnoDB Buffer Pool Configuration 3060                                 |      |
| 17.8.4 Configuring Thread Concurrency for InnoDB 3074                        |      |
| 17.8.5 Configuring the Number of Background InnoDB I/O Threads 3075          |      |
| 17.8.6 Using Asynchronous I/O on Linux 3076                                  |      |
| 17.8.7 Configuring InnoDB I/O Capacity 3076                                  |      |
| 17.8.8 Configuring Spin Lock Polling 3078                                    |      |
| 17.8.9 Purge Configuration 3079                                              |      |
| 17.8.10 Configuring Optimizer Statistics for InnoDB 3080                     |      |
| 17.8.11 Configuring the Merge Threshold for Index Pages                      | 3091 |
| 17.8.12 Enabling Automatic InnoDB Configuration for a Dedicated MySQL Server | 3093 |
| 17.9 InnoDB Table and Page Compression 3095                                  |      |
| 17.9.1 InnoDB Table Compression 3095                                         |      |
| 17.9.2 InnoDB Page Compression 3109                                          |      |
| 17.10 InnoDB Row Formats                                                     | 3112 |
| 17.11 InnoDB Disk I/O and File Space Management                              | 3118 |
| 17.11.1 InnoDB Disk I/O 3119                                                 |      |
| 17.11.2 File Space Management                                                | 3119 |
| 17.11.3 InnoDB Checkpoints                                                   | 3121 |
| 17.11.4 Defragmenting a Table 3121                                           |      |
| 17.11.5 Reclaiming Disk Space with TRUNCATE TABLE 3122                       |      |
| 17.12 InnoDB and Online DDL 3122                                             |      |
| 17.12.1 Online DDL Operations 3123                                           |      |
| 17.12.2 Online DDL Performance and Concurrency 3138                          |      |
| 17.12.3 Online DDL Space Requirements 3141                                   |      |
| 17.12.4 Online DDL Memory Management 3142                                    |      |
| 17.12.5 Configuring Parallel Threads for Online DDL Operations 3142          |      |
| 17.12.6 Simplifying DDL Statements with Online DDL 3143                      |      |
| 17.12.7 Online DDL Failure Conditions                                        | 3143 |
| 17.12.8 Online DDL Limitations 3144                                          |      |
| 17.13 InnoDB Data-at-Rest Encryption 3144                                    |      |
| 17.14 InnoDB Startup Options and System Variables 3153                       |      |
| 17.15 InnoDB INFORMATION_SCHEMA Tables 3237                                  |      |
| 17.15.1 InnoDB INFORMATION_SCHEMA Tables about Compression 3237              |      |
| 17.15.2 InnoDB INFORMATION_SCHEMA Transaction and Locking Information 3239   |      |
|                                                                              |      |
| 17.15.3 InnoDB INFORMATION_SCHEMA Schema Object Tables 3246                  |      |
| 17.15.4 InnoDB INFORMATION_SCHEMA FULLTEXT Index Tables 3251                 |      |
| 17.15.5 InnoDB INFORMATION_SCHEMA Buffer Pool Tables 3254                    |      |
| 17.15.6 InnoDB INFORMATION_SCHEMA Metrics Table                              | 3258 |
| 17.15.7 InnoDB INFORMATION_SCHEMA Temporary Table Info Table                 | 3267 |
| 17.15.8 Retrieving InnoDB Tablespace Metadata from                           |      |
| INFORMATION_SCHEMA.FILES 3268                                                |      |
| 17.16 InnoDB Integration with MySQL Performance Schema                       | 3269 |
| 17.16.1 Monitoring ALTER TABLE Progress for InnoDB Tables Using Performance  |      |
| Schema 3271                                                                  |      |
| 17.16.2 Monitoring InnoDB Mutex Waits Using Performance Schema 3273          |      |
| 17.17 InnoDB Monitors 3276                                                   |      |
| 17.17.1 InnoDB Monitor Types                                                 | 3277 |
| 17.17.2 Enabling InnoDB Monitors 3277                                        |      |
| 17.17.3 InnoDB Standard Monitor and Lock Monitor Output                      | 3279 |
| 17.18 InnoDB Backup and Recovery 3283                                        |      |
| 17.18.1 InnoDB Backup 3283                                                   |      |
| 17.18.2 InnoDB Recovery 3284                                                 |      |
| 17.19 InnoDB and MySQL Replication 3286                                      |      |

| 17.20 InnoDB Troubleshooting 3288                                                                                               |      |
|---------------------------------------------------------------------------------------------------------------------------------|------|
| 17.20.1 Troubleshooting InnoDB I/O Problems 3288                                                                                |      |
| 17.20.2 Troubleshooting Recovery Failures 3289                                                                                  |      |
| 17.20.3 Forcing InnoDB Recovery                                                                                                 | 3289 |
| 17.20.4 Troubleshooting InnoDB Data Dictionary Operations 3291                                                                  |      |
| 17.20.5 InnoDB Error Handling 3292                                                                                              |      |
| 17.21 InnoDB Limits 3292                                                                                                        |      |
| 17.22 InnoDB Restrictions and Limitations                                                                                       | 3294 |
| 18 Alternative Storage Engines 3295                                                                                             |      |
| 18.1 Setting the Storage Engine 3298                                                                                            |      |
| 18.2 The MyISAM Storage Engine 3299                                                                                             |      |
| 18.2.1 MyISAM Startup Options 3302                                                                                              |      |
| 18.2.2 Space Needed for Keys 3303                                                                                               |      |
| 18.2.3 MyISAM Table Storage Formats 3303                                                                                        |      |
| 18.2.4 MyISAM Table Problems 3306                                                                                               |      |
| 18.3 The MEMORY Storage Engine                                                                                                  | 3307 |
| 18.4 The CSV Storage Engine                                                                                                     | 3312 |
| 18.4.1 Repairing and Checking CSV Tables 3312                                                                                   |      |
| 18.4.2 CSV Limitations 3313                                                                                                     |      |
| 18.5 The ARCHIVE Storage Engine 3313                                                                                            |      |
| 18.6 The BLACKHOLE Storage Engine                                                                                               | 3315 |
| 18.7 The MERGE Storage Engine 3317                                                                                              |      |
| 18.7.1 MERGE Table Advantages and Disadvantages 3319                                                                            |      |
| 18.7.2 MERGE Table Problems 3320                                                                                                |      |
| 18.8 The FEDERATED Storage Engine 3322                                                                                          |      |
| 18.8.1 FEDERATED Storage Engine Overview 3322                                                                                   |      |
| 18.8.2 How to Create FEDERATED Tables 3323                                                                                      |      |
| 18.8.3 FEDERATED Storage Engine Notes and Tips 3326                                                                             |      |
| 18.8.4 FEDERATED Storage Engine Resources 3327                                                                                  |      |
| 18.9 The EXAMPLE Storage Engine 3327                                                                                            |      |
| 18.10 Other Storage Engines 3328                                                                                                |      |
| 18.11 Overview of MySQL Storage Engine Architecture 3328                                                                        |      |
| 18.11.1 Pluggable Storage Engine Architecture 3329                                                                              |      |
| 18.11.2 The Common Database Server Layer 3329                                                                                   |      |
| 19 Replication 3331                                                                                                             |      |
| 19.1 Configuring Replication 3333                                                                                               |      |
| 19.1.1 Binary Log File Position Based Replication Configuration Overview                                                        | 3333 |
| 19.1.2 Setting Up Binary Log File Position Based Replication 3334                                                               |      |
| 19.1.3 Replication with Global Transaction Identifiers 3345                                                                     |      |
| 19.1.4 Changing GTID Mode on Online Servers 3367                                                                                |      |
| 19.1.5 MySQL Multi-Source Replication                                                                                           | 3373 |
| 19.1.6 Replication and Binary Logging Options and Variables 3378                                                                |      |
| 19.1.7 Common Replication Administration Tasks 3475                                                                             |      |
| 19.2 Replication Implementation 3481                                                                                            |      |
| 19.2.1 Replication Formats 3481                                                                                                 |      |
| 19.2.2 Replication Channels 3489                                                                                                |      |
| 19.2.3 Replication Threads 3492                                                                                                 |      |
| 19.2.4 Relay Log and Replication Metadata Repositories 3495                                                                     |      |
| 19.2.5 How Servers Evaluate Replication Filtering Rules 3502                                                                    |      |
| 19.3 Replication Security 3510                                                                                                  |      |
| 19.3.1 Setting Up Replication to Use Encrypted Connections                                                                      | 3511 |
| 19.3.2 Encrypting Binary Log Files and Relay Log Files 3513                                                                     |      |
| 19.3.3 Replication Privilege Checks 3516                                                                                        |      |
| 19.4 Replication Solutions 3522                                                                                                 |      |
| 19.4.1 Using Replication for Backups 3523                                                                                       |      |
|                                                                                                                                 |      |
| 19.4.2 Handling an Unexpected Halt of a Replica 3526                                                                            |      |
| 19.4.3 Monitoring Row-based Replication 3529<br>19.4.4 Using Replication with Different Source and Replica Storage Engines 3529 |      |
|                                                                                                                                 |      |

| 19.4.5 Using Replication for Scale-Out 3530                                           |      |
|---------------------------------------------------------------------------------------|------|
| 19.4.6 Replicating Different Databases to Different Replicas 3532                     |      |
| 19.4.7 Improving Replication Performance 3533                                         |      |
| 19.4.8 Switching Sources During Failover                                              | 3534 |
| 19.4.9 Switching Sources and Replicas with Asynchronous Connection Failover 3536      |      |
| 19.4.10 Semisynchronous Replication 3540                                              |      |
| 19.4.11 Delayed Replication 3545                                                      |      |
| 19.5 Replication Notes and Tips 3547                                                  |      |
| 19.5.1 Replication Features and Issues 3547                                           |      |
|                                                                                       |      |
| 19.5.2 Replication Compatibility Between MySQL Versions 3574                          |      |
| 19.5.3 Upgrading or Downgrading a Replication Topology 3575                           |      |
| 19.5.4 Troubleshooting Replication                                                    | 3576 |
| 19.5.5 How to Report Replication Bugs or Problems 3577                                |      |
| 20 Group Replication                                                                  | 3579 |
| 20.1 Group Replication Background 3580                                                |      |
| 20.1.1 Replication Technologies 3581                                                  |      |
| 20.1.2 Group Replication Use Cases 3584                                               |      |
| 20.1.3 Multi-Primary and Single-Primary Modes 3585                                    |      |
| 20.1.4 Group Replication Services 3589                                                |      |
| 20.1.5 Group Replication Plugin Architecture 3591                                     |      |
| 20.2 Getting Started 3593                                                             |      |
| 20.2.1 Deploying Group Replication in Single-Primary Mode 3593                        |      |
| 20.2.2 Deploying Group Replication Locally 3605                                       |      |
| 20.3 Requirements and Limitations 3606                                                |      |
| 20.3.1 Group Replication Requirements 3606                                            |      |
| 20.3.2 Group Replication Limitations 3609                                             |      |
| 20.4 Monitoring Group Replication 3611                                                |      |
|                                                                                       |      |
| 20.4.1 GTIDs and Group Replication 3612                                               |      |
| 20.4.2 Group Replication Server States 3613                                           |      |
| 20.4.3 The replication_group_members Table                                            | 3614 |
| 20.4.4 The replication_group_member_stats Table 3615                                  |      |
| 20.5 Group Replication Operations 3615                                                |      |
| 20.5.1 Configuring an Online Group 3615                                               |      |
| 20.5.2 Restarting a Group 3621                                                        |      |
| 20.5.3 Transaction Consistency Guarantees 3622                                        |      |
| 20.5.4 Distributed Recovery 3629                                                      |      |
| 20.5.5 Support For IPv6 And For Mixed IPv6 And IPv4 Groups                            | 3643 |
| 20.5.6 Using MySQL Enterprise Backup with Group Replication 3644                      |      |
| 20.6 Group Replication Security 3650                                                  |      |
| 20.6.1 Communication Stack for Connection Security Management 3650                    |      |
| 20.6.2 Securing Group Communication Connections with Secure Socket Layer (SSL) . 3653 |      |
| 20.6.3 Securing Distributed Recovery Connections 3655                                 |      |
| 20.6.4 Group Replication IP Address Permissions 3659                                  |      |
| 20.7 Group Replication Performance and Troubleshooting 3662                           |      |
| 20.7.1 Fine Tuning the Group Communication Thread 3662                                |      |
| 20.7.2 Flow Control 3662                                                              |      |
| 20.7.3 Single Consensus Leader 3664                                                   |      |
| 20.7.4 Message Compression 3665                                                       |      |
| 20.7.5 Message Fragmentation 3667                                                     |      |
|                                                                                       |      |
| 20.7.6 XCom Cache Management 3667                                                     |      |
| 20.7.7 Responses to Failure Detection and Network Partitioning 3669                   |      |
| 20.7.8 Handling a Network Partition and Loss of Quorum 3674                           |      |
| 20.7.9 Monitoring Group Replication Memory Usage with Performance Schema              |      |
| Memory Instrumentation 3679                                                           |      |
| 20.8 Upgrading Group Replication 3688                                                 |      |
| 20.8.1 Combining Different Member Versions in a Group 3688                            |      |
| 20.8.2 Group Replication Offline Upgrade                                              | 3690 |
| 20.8.3 Group Replication Online Upgrade                                               | 3690 |

| 20.9 Group Replication Variables 3694                                                |      |
|--------------------------------------------------------------------------------------|------|
| 20.9.1 Group Replication System Variables 3696                                       |      |
| 20.9.2 Group Replication Status Variables 3738                                       |      |
| 20.10 Frequently Asked Questions 3740                                                |      |
| 21 MySQL Shell 3745                                                                  |      |
| 22 Using MySQL as a Document Store                                                   | 3747 |
| 22.1 Interfaces to a MySQL Document Store 3748                                       |      |
| 22.2 Document Store Concepts 3748                                                    |      |
| 22.3 JavaScript Quick-Start Guide: MySQL Shell for Document Store 3749               |      |
| 22.3.1 MySQL Shell 3750                                                              |      |
| 22.3.2 Download and Import world_x Database 3751                                     |      |
| 22.3.3 Documents and Collections 3752                                                |      |
| 22.3.4 Relational Tables 3762                                                        |      |
| 22.3.5 Documents in Tables 3768                                                      |      |
| 22.4 Python Quick-Start Guide: MySQL Shell for Document Store 3769                   |      |
| 22.4.1 MySQL Shell 3769                                                              |      |
| 22.4.2 Download and Import world_x Database 3771                                     |      |
|                                                                                      |      |
| 22.4.3 Documents and Collections 3771                                                |      |
| 22.4.4 Relational Tables 3782                                                        |      |
| 22.4.5 Documents in Tables 3788                                                      |      |
| 22.5 X Plugin 3789                                                                   |      |
| 22.5.1 Checking X Plugin Installation 3789                                           |      |
| 22.5.2 Disabling X Plugin 3789                                                       |      |
| 22.5.3 Using Encrypted Connections with X Plugin 3789                                |      |
| 22.5.4 Using X Plugin with the Caching SHA-2 Authentication Plugin 3790              |      |
| 22.5.5 Connection Compression with X Plugin 3791                                     |      |
| 22.5.6 X Plugin Options and Variables 3794                                           |      |
| 22.5.7 Monitoring X Plugin                                                           | 3814 |
| 23 InnoDB Cluster 3817                                                               |      |
| 24 InnoDB ReplicaSet 3819                                                            |      |
| 25 MySQL NDB Cluster 8.4                                                             | 3821 |
| 25.1 General Information 3822                                                        |      |
| 25.2 NDB Cluster Overview 3824                                                       |      |
| 25.2.1 NDB Cluster Core Concepts 3826                                                |      |
| 25.2.2 NDB Cluster Nodes, Node Groups, Fragment Replicas, and Partitions 3829        |      |
| 25.2.3 NDB Cluster Hardware, Software, and Networking Requirements 3832              |      |
| 25.2.4 What is New in MySQL NDB Cluster 8.4                                          | 3833 |
| 25.2.5 Options, Variables, and Parameters Added, Deprecated or Removed in NDB        |      |
| 8.4 3837                                                                             |      |
| 25.2.6 MySQL Server Using InnoDB Compared with NDB Cluster 3838                      |      |
| 25.2.7 Known Limitations of NDB Cluster 3840                                         |      |
| 25.3 NDB Cluster Installation 3852                                                   |      |
| 25.3.1 Installation of NDB Cluster on Linux 3854                                     |      |
| 25.3.2 Installing NDB Cluster on Windows                                             | 3862 |
|                                                                                      |      |
| 25.3.3 Initial Configuration of NDB Cluster                                          | 3871 |
| 25.3.4 Initial Startup of NDB Cluster 3872                                           |      |
| 25.3.5 NDB Cluster Example with Tables and Data 3873                                 |      |
| 25.3.6 Safe Shutdown and Restart of NDB Cluster 3876                                 |      |
| 25.3.7 Upgrading and Downgrading NDB Cluster                                         | 3877 |
| 25.4 Configuration of NDB Cluster 3878                                               |      |
| 25.4.1 Quick Test Setup of NDB Cluster 3878                                          |      |
| 25.4.2 Overview of NDB Cluster Configuration Parameters, Options, and Variables 3880 |      |
| 25.4.3 NDB Cluster Configuration Files 3902                                          |      |
|                                                                                      |      |
| 25.4.4 Using High-Speed Interconnects with NDB Cluster 4104                          |      |
| 25.5 NDB Cluster Programs 4105                                                       |      |
| 25.5.1 ndbd — The NDB Cluster Data Node Daemon 4105                                  |      |
| 25.5.2 ndbinfo_select_all — Select From ndbinfo Tables 4114                          |      |

| 25.5.4 ndb_mgmd — The NDB Cluster Management Server Daemon 4120                |      |
|--------------------------------------------------------------------------------|------|
| 25.5.5 ndb_mgm — The NDB Cluster Management Client 4130                        |      |
| 25.5.6 ndb_blob_tool — Check and Repair BLOB and TEXT columns of NDB Cluster   |      |
| Tables 4135                                                                    |      |
| 25.5.7 ndb_config — Extract NDB Cluster Configuration Information 4140         |      |
| 25.5.8 ndb_delete_all — Delete All Rows from an NDB Table 4151                 |      |
| 25.5.9 ndb_desc — Describe NDB Tables                                          | 4154 |
| 25.5.10 ndb_drop_index — Drop Index from an NDB Table 4163                     |      |
|                                                                                |      |
| 25.5.11 ndb_drop_table — Drop an NDB Table 4167                                |      |
| 25.5.12 ndb_error_reporter — NDB Error-Reporting Utility 4171                  |      |
| 25.5.13 ndb_import — Import CSV Data Into NDB 4172                             |      |
| 25.5.14 ndb_index_stat — NDB Index Statistics Utility 4185                     |      |
| 25.5.15 ndb_move_data — NDB Data Copy Utility                                  | 4191 |
| 25.5.16 ndb_perror — Obtain NDB Error Message Information 4196                 |      |
| 25.5.17 ndb_print_backup_file — Print NDB Backup File Contents 4198            |      |
| 25.5.18 ndb_print_file — Print NDB Disk Data File Contents                     | 4202 |
| 25.5.19 ndb_print_frag_file — Print NDB Fragment List File Contents 4203       |      |
| 25.5.20 ndb_print_schema_file — Print NDB Schema File Contents 4204            |      |
| 25.5.21 ndb_print_sys_file — Print NDB System File Contents 4204               |      |
| 25.5.22 ndb_redo_log_reader — Check and Print Content of Cluster Redo Log 4204 |      |
| 25.5.23 ndb_restore — Restore an NDB Cluster Backup 4206                       |      |
| 25.5.24 ndb_secretsfile_reader — Obtain Key Information from an Encrypted NDB  |      |
| Data File 4228                                                                 |      |
| 25.5.25 ndb_select_all — Print Rows from an NDB Table 4230                     |      |
| 25.5.26 ndb_select_count — Print Row Counts for NDB Tables 4236                |      |
| 25.5.27 ndb_show_tables — Display List of NDB Tables 4239                      |      |
| 25.5.28 ndb_sign_keys — Create, Sign, and Manage TLS Keys and Certificates for |      |
| NDB Cluster 4243                                                               |      |
| 25.5.29 ndb_size.pl — NDBCLUSTER Size Requirement Estimator 4251               |      |
|                                                                                |      |
| 25.5.30 ndb_top — View CPU usage information for NDB threads 4253              |      |
| 25.5.31 ndb_waiter — Wait for NDB Cluster to Reach a Given Status 4258         |      |
| 25.5.32 ndbxfrm — Compress, Decompress, Encrypt, and Decrypt Files Created by  |      |
| NDB Cluster 4264                                                               |      |
| 25.6 Management of NDB Cluster 4269                                            |      |
| 25.6.1 Commands in the NDB Cluster Management Client 4270                      |      |
| 25.6.2 NDB Cluster Log Messages 4276                                           |      |
| 25.6.3 Event Reports Generated in NDB Cluster 4294                             |      |
| 25.6.4 Summary of NDB Cluster Start Phases 4306                                |      |
| 25.6.5 Performing a Rolling Restart of an NDB Cluster 4308                     |      |
| 25.6.6 NDB Cluster Single User Mode 4310                                       |      |
| 25.6.7 Adding NDB Cluster Data Nodes Online 4311                               |      |
| 25.6.8 Online Backup of NDB Cluster 4321                                       |      |
| 25.6.9 Importing Data Into MySQL Cluster 4327                                  |      |
| 25.6.10 MySQL Server Usage for NDB Cluster 4328                                |      |
| 25.6.11 NDB Cluster Disk Data Tables 4330                                      |      |
| 25.6.12 Online Operations with ALTER TABLE in NDB Cluster 4336                 |      |
| 25.6.13 Privilege Synchronization and NDB_STORED_USER 4339                     |      |
| 25.6.14 NDB API Statistics Counters and Variables 4340                         |      |
| 25.6.15 ndbinfo: The NDB Cluster Information Database 4352                     |      |
| 25.6.16 INFORMATION_SCHEMA Tables for NDB Cluster 4440                         |      |
| 25.6.17 NDB Cluster and the Performance Schema 4441                            |      |
| 25.6.18 Quick Reference: NDB Cluster SQL Statements 4442                       |      |
| 25.6.19 NDB Cluster Security 4449                                              |      |
| 25.7 NDB Cluster Replication 4462                                              |      |
| 25.7.1 NDB Cluster Replication: Abbreviations and Symbols 4464                 |      |
|                                                                                |      |
| 25.7.2 General Requirements for NDB Cluster Replication 4464                   |      |
| 25.7.3 Known Issues in NDB Cluster Replication 4465                            |      |
| 25.7.4 NDB Cluster Replication Schema and Tables 4471                          |      |

| 25.7.5 Preparing the NDB Cluster for Replication                             | 4478 |
|------------------------------------------------------------------------------|------|
| 25.7.6 Starting NDB Cluster Replication (Single Replication Channel) 4480    |      |
| 25.7.7 Using Two Replication Channels for NDB Cluster Replication 4482       |      |
| 25.7.8 Implementing Failover with NDB Cluster Replication 4483               |      |
| 25.7.9 NDB Cluster Backups With NDB Cluster Replication 4484                 |      |
| 25.7.10 NDB Cluster Replication: Bidirectional and Circular Replication 4490 |      |
| 25.7.11 NDB Cluster Replication Using the Multithreaded Applier 4494         |      |
| 25.7.12 NDB Cluster Replication Conflict Resolution 4497                     |      |
| 25.8 NDB Cluster Release Notes 4514                                          |      |
| 26 Partitioning 4515                                                         |      |
|                                                                              |      |
| 26.1 Overview of Partitioning in MySQL 4516                                  |      |
| 26.2 Partitioning Types 4518                                                 |      |
| 26.2.1 RANGE Partitioning 4520                                               |      |
| 26.2.2 LIST Partitioning 4524                                                |      |
| 26.2.3 COLUMNS Partitioning                                                  | 4527 |
| 26.2.4 HASH Partitioning 4534                                                |      |
| 26.2.5 KEY Partitioning 4537                                                 |      |
| 26.2.6 Subpartitioning 4538                                                  |      |
| 26.2.7 How MySQL Partitioning Handles NULL 4540                              |      |
| 26.3 Partition Management 4544                                               |      |
| 26.3.1 Management of RANGE and LIST Partitions 4545                          |      |
| 26.3.2 Management of HASH and KEY Partitions 4551                            |      |
| 26.3.3 Exchanging Partitions and Subpartitions with Tables 4552              |      |
| 26.3.4 Maintenance of Partitions 4559                                        |      |
| 26.3.5 Obtaining Information About Partitions 4560                           |      |
| 26.4 Partition Pruning 4563                                                  |      |
| 26.5 Partition Selection 4565                                                |      |
| 26.6 Restrictions and Limitations on Partitioning 4571                       |      |
| 26.6.1 Partitioning Keys, Primary Keys, and Unique Keys 4576                 |      |
| 26.6.2 Partitioning Limitations Relating to Storage Engines 4579             |      |
| 26.6.3 Partitioning Limitations Relating to Functions 4580                   |      |
| 27 Stored Objects 4583                                                       |      |
| 27.1 Defining Stored Programs 4584                                           |      |
| 27.2 Using Stored Routines 4585                                              |      |
| 27.2.1 Stored Routine Syntax 4586                                            |      |
| 27.2.2 Stored Routines and MySQL Privileges                                  | 4586 |
| 27.2.3 Stored Routine Metadata 4587                                          |      |
| 27.2.4 Stored Procedures, Functions, Triggers, and LAST_INSERT_ID() 4587     |      |
| 27.3 Using Triggers 4587                                                     |      |
| 27.3.1 Trigger Syntax and Examples 4588                                      |      |
| 27.3.2 Trigger Metadata 4592                                                 |      |
| 27.4 Using the Event Scheduler                                               | 4592 |
| 27.4.1 Event Scheduler Overview 4593                                         |      |
| 27.4.2 Event Scheduler Configuration 4593                                    |      |
| 27.4.3 Event Syntax 4596                                                     |      |
| 27.4.4 Event Metadata 4596                                                   |      |
| 27.4.5 Event Scheduler Status 4597                                           |      |
| 27.4.6 The Event Scheduler and MySQL Privileges 4597                         |      |
| 27.5 Using Views 4600                                                        |      |
| 27.5.1 View Syntax 4600                                                      |      |
|                                                                              |      |
| 27.5.2 View Processing Algorithms 4600                                       |      |
| 27.5.3 Updatable and Insertable Views 4601                                   |      |
| 27.5.4 The View WITH CHECK OPTION Clause 4604                                |      |
| 27.5.5 View Metadata 4605                                                    |      |
| 27.6 Stored Object Access Control 4605                                       |      |
| 27.7 Stored Program Binary Logging 4609                                      |      |
| 27.8 Restrictions on Stored Programs 4615                                    |      |
| 27.9 Restrictions on Views 4618                                              |      |

| 28 INFORMATION_SCHEMA Tables 4621                                          |      |
|----------------------------------------------------------------------------|------|
| 28.1 Introduction 4622                                                     |      |
| 28.2 INFORMATION_SCHEMA Table Reference                                    | 4625 |
| 28.3 INFORMATION_SCHEMA General Tables 4629                                |      |
| 28.3.1 INFORMATION_SCHEMA General Table Reference 4629                     |      |
| 28.3.2 The INFORMATION_SCHEMA ADMINISTRABLE_ROLE_AUTHORIZATIONS            |      |
| Table 4630                                                                 |      |
| 28.3.3 The INFORMATION_SCHEMA APPLICABLE_ROLES Table 4631                  |      |
| 28.3.4 The INFORMATION_SCHEMA CHARACTER_SETS Table 4632                    |      |
| 28.3.5 The INFORMATION_SCHEMA CHECK_CONSTRAINTS Table 4632                 |      |
| 28.3.6 The INFORMATION_SCHEMA COLLATIONS Table 4633                        |      |
|                                                                            |      |
| 28.3.7 The INFORMATION_SCHEMA                                              |      |
| COLLATION_CHARACTER_SET_APPLICABILITY Table 4633                           |      |
| 28.3.8 The INFORMATION_SCHEMA COLUMNS Table 4634                           |      |
| 28.3.9 The INFORMATION_SCHEMA COLUMNS_EXTENSIONS Table 4636                |      |
| 28.3.10 The INFORMATION_SCHEMA COLUMN_PRIVILEGES Table 4637                |      |
| 28.3.11 The INFORMATION_SCHEMA COLUMN_STATISTICS Table 4638                |      |
| 28.3.12 The INFORMATION_SCHEMA ENABLED_ROLES Table 4638                    |      |
| 28.3.13 The INFORMATION_SCHEMA ENGINES Table 4638                          |      |
| 28.3.14 The INFORMATION_SCHEMA EVENTS Table 4639                           |      |
| 28.3.15 The INFORMATION_SCHEMA FILES Table 4643                            |      |
| 28.3.16 The INFORMATION_SCHEMA KEY_COLUMN_USAGE Table 4648                 |      |
| 28.3.17 The INFORMATION_SCHEMA KEYWORDS Table 4650                         |      |
| 28.3.18 The INFORMATION_SCHEMA ndb_transid_mysql_connection_map Table 4650 |      |
| 28.3.19 The INFORMATION_SCHEMA OPTIMIZER_TRACE Table                       | 4651 |
| 28.3.20 The INFORMATION_SCHEMA PARAMETERS Table 4652                       |      |
| 28.3.21 The INFORMATION_SCHEMA PARTITIONS Table 4653                       |      |
| 28.3.22 The INFORMATION_SCHEMA PLUGINS Table 4656                          |      |
| 28.3.23 The INFORMATION_SCHEMA PROCESSLIST Table 4657                      |      |
| 28.3.24 The INFORMATION_SCHEMA PROFILING Table 4659                        |      |
| 28.3.25 The INFORMATION_SCHEMA REFERENTIAL_CONSTRAINTS Table 4660          |      |
| 28.3.26 The INFORMATION_SCHEMA RESOURCE_GROUPS Table 4661                  |      |
| 28.3.27 The INFORMATION_SCHEMA ROLE_COLUMN_GRANTS Table 4662               |      |
| 28.3.28 The INFORMATION_SCHEMA ROLE_ROUTINE_GRANTS Table 4662              |      |
| 28.3.29 The INFORMATION_SCHEMA ROLE_TABLE_GRANTS Table 4663                |      |
| 28.3.30 The INFORMATION_SCHEMA ROUTINES Table 4664                         |      |
| 28.3.31 The INFORMATION_SCHEMA SCHEMATA Table 4667                         |      |
|                                                                            |      |
| 28.3.32 The INFORMATION_SCHEMA SCHEMATA_EXTENSIONS Table 4667              |      |
| 28.3.33 The INFORMATION_SCHEMA SCHEMA_PRIVILEGES Table 4668                |      |
| 28.3.34 The INFORMATION_SCHEMA STATISTICS Table 4669                       |      |
| 28.3.35 The INFORMATION_SCHEMA ST_GEOMETRY_COLUMNS Table 4671              |      |
| 28.3.36 The INFORMATION_SCHEMA ST_SPATIAL_REFERENCE_SYSTEMS                |      |
| Table 4672                                                                 |      |
| 28.3.37 The INFORMATION_SCHEMA ST_UNITS_OF_MEASURE Table 4673              |      |
| 28.3.38 The INFORMATION_SCHEMA TABLES Table 4674                           |      |
| 28.3.39 The INFORMATION_SCHEMA TABLES_EXTENSIONS Table 4677                |      |
| 28.3.40 The INFORMATION_SCHEMA TABLESPACES_EXTENSIONS Table 4678           |      |
| 28.3.41 The INFORMATION_SCHEMA TABLE_CONSTRAINTS Table 4678                |      |
| 28.3.42 The INFORMATION_SCHEMA TABLE_CONSTRAINTS_EXTENSIONS Table 4679     |      |
| 28.3.43 The INFORMATION_SCHEMA TABLE_PRIVILEGES Table 4679                 |      |
| 28.3.44 The INFORMATION_SCHEMA TRIGGERS Table 4680                         |      |
| 28.3.45 The INFORMATION_SCHEMA USER_ATTRIBUTES Table 4682                  |      |
| 28.3.46 The INFORMATION_SCHEMA USER_PRIVILEGES Table 4683                  |      |
| 28.3.47 The INFORMATION_SCHEMA VIEWS Table 4683                            |      |
| 28.3.48 The INFORMATION_SCHEMA VIEW_ROUTINE_USAGE Table 4685               |      |
| 28.3.49 The INFORMATION_SCHEMA VIEW_TABLE_USAGE Table 4685                 |      |
| 28.4 INFORMATION_SCHEMA InnoDB Tables 4686                                 |      |
| 28.4.1 INFORMATION_SCHEMA InnoDB Table Reference 4686                      |      |
|                                                                            |      |

| 28.4.2 The INFORMATION_SCHEMA INNODB_BUFFER_PAGE Table                 | 4687 |
|------------------------------------------------------------------------|------|
| 28.4.3 The INFORMATION_SCHEMA INNODB_BUFFER_PAGE_LRU Table 4691        |      |
| 28.4.4 The INFORMATION_SCHEMA INNODB_BUFFER_POOL_STATS Table 4694      |      |
| 28.4.5 The INFORMATION_SCHEMA INNODB_CACHED_INDEXES Table              | 4697 |
| 28.4.6 The INFORMATION_SCHEMA INNODB_CMP and INNODB_CMP_RESET          |      |
| Tables 4698                                                            |      |
| 28.4.7 The INFORMATION_SCHEMA INNODB_CMPMEM and                        |      |
| INNODB_CMPMEM_RESET Tables 4699                                        |      |
| 28.4.8 The INFORMATION_SCHEMA INNODB_CMP_PER_INDEX and                 |      |
| INNODB_CMP_PER_INDEX_RESET Tables                                      | 4701 |
| 28.4.9 The INFORMATION_SCHEMA INNODB_COLUMNS Table 4702                |      |
| 28.4.10 The INFORMATION_SCHEMA INNODB_DATAFILES Table 4703             |      |
| 28.4.11 The INFORMATION_SCHEMA INNODB_FIELDS Table 4704                |      |
| 28.4.12 The INFORMATION_SCHEMA INNODB_FOREIGN Table 4705               |      |
| 28.4.13 The INFORMATION_SCHEMA INNODB_FOREIGN_COLS Table 4705          |      |
| 28.4.14 The INFORMATION_SCHEMA INNODB_FT_BEING_DELETED Table 4706      |      |
| 28.4.15 The INFORMATION_SCHEMA INNODB_FT_CONFIG Table 4707             |      |
| 28.4.16 The INFORMATION_SCHEMA INNODB_FT_DEFAULT_STOPWORD Table . 4708 |      |
| 28.4.17 The INFORMATION_SCHEMA INNODB_FT_DELETED Table 4709            |      |
| 28.4.18 The INFORMATION_SCHEMA INNODB_FT_INDEX_CACHE Table 4709        |      |
| 28.4.19 The INFORMATION_SCHEMA INNODB_FT_INDEX_TABLE Table 4711        |      |
| 28.4.20 The INFORMATION_SCHEMA INNODB_INDEXES Table 4712               |      |
|                                                                        |      |
| 28.4.21 The INFORMATION_SCHEMA INNODB_METRICS Table 4714               |      |
| 28.4.22 The INFORMATION_SCHEMA INNODB_SESSION_TEMP_TABLESPACES         |      |
| Table 4716                                                             |      |
| 28.4.23 The INFORMATION_SCHEMA INNODB_TABLES Table 4717                |      |
| 28.4.24 The INFORMATION_SCHEMA INNODB_TABLESPACES Table 4718           |      |
| 28.4.25 The INFORMATION_SCHEMA INNODB_TABLESPACES_BRIEF Table          | 4720 |
| 28.4.26 The INFORMATION_SCHEMA INNODB_TABLESTATS View 4721             |      |
| 28.4.27 The INFORMATION_SCHEMA INNODB_TEMP_TABLE_INFO Table 4723       |      |
| 28.4.28 The INFORMATION_SCHEMA INNODB_TRX Table 4723                   |      |
| 28.4.29 The INFORMATION_SCHEMA INNODB_VIRTUAL Table 4726               |      |
| 28.5 INFORMATION_SCHEMA Thread Pool Tables 4727                        |      |
| 28.5.1 INFORMATION_SCHEMA Thread Pool Table Reference 4728             |      |
| 28.5.2 The INFORMATION_SCHEMA TP_THREAD_GROUP_STATE Table 4728         |      |
| 28.5.3 The INFORMATION_SCHEMA TP_THREAD_GROUP_STATS Table 4728         |      |
| 28.5.4 The INFORMATION_SCHEMA TP_THREAD_STATE Table 4729               |      |
| 28.6 INFORMATION_SCHEMA Connection Control Tables 4729                 |      |
| 28.6.1 INFORMATION_SCHEMA Connection Control Table Reference           | 4729 |
| 28.6.2 The INFORMATION_SCHEMA                                          |      |
| CONNECTION_CONTROL_FAILED_LOGIN_ATTEMPTS Table 4729                    |      |
| 28.7 INFORMATION_SCHEMA MySQL Enterprise Firewall Tables 4730          |      |
| 28.7.1 INFORMATION_SCHEMA Firewall Table Reference 4730                |      |
| 28.7.2 The INFORMATION_SCHEMA MYSQL_FIREWALL_USERS Table 4730          |      |
| 28.7.3 The INFORMATION_SCHEMA MYSQL_FIREWALL_WHITELIST Table 4731      |      |
| 28.8 Extensions to SHOW Statements 4731                                |      |
| 29 MySQL Performance Schema 4735                                       |      |
| 29.1 Performance Schema Quick Start 4737                               |      |
| 29.2 Performance Schema Build Configuration 4743                       |      |
| 29.3 Performance Schema Startup Configuration 4743                     |      |
| 29.4 Performance Schema Runtime Configuration 4745                     |      |
| 29.4.1 Performance Schema Event Timing 4746                            |      |
| 29.4.2 Performance Schema Event Filtering 4748                         |      |
| 29.4.3 Event Pre-Filtering 4749                                        |      |
| 29.4.4 Pre-Filtering by Instrument 4750                                |      |
| 29.4.5 Pre-Filtering by Object 4752                                    |      |
| 29.4.6 Pre-Filtering by Thread 4753                                    |      |
| 29.4.7 Pre-Filtering by Consumer 4755                                  |      |
|                                                                        |      |

| 29.4.8 Example Consumer Configurations 4758                           |      |
|-----------------------------------------------------------------------|------|
| 29.4.9 Naming Instruments or Consumers for Filtering Operations 4763  |      |
| 29.4.10 Determining What Is Instrumented 4763                         |      |
| 29.5 Performance Schema Queries                                       | 4764 |
| 29.6 Performance Schema Instrument Naming Conventions 4764            |      |
| 29.7 Performance Schema Status Monitoring 4768                        |      |
| 29.8 Performance Schema Atom and Molecule Events 4771                 |      |
| 29.9 Performance Schema Tables for Current and Historical Events 4771 |      |
| 29.10 Performance Schema Statement Digests and Sampling 4773          |      |
| 29.11 Performance Schema General Table Characteristics 4777           |      |
| 29.12 Performance Schema Table Descriptions 4778                      |      |
| 29.12.1 Performance Schema Table Reference 4778                       |      |
| 29.12.2 Performance Schema Setup Tables 4782                          |      |
| 29.12.3 Performance Schema Instance Tables 4791                       |      |
| 29.12.4 Performance Schema Wait Event Tables 4796                     |      |
| 29.12.5 Performance Schema Stage Event Tables 4801                    |      |
| 29.12.6 Performance Schema Statement Event Tables 4807                |      |
|                                                                       |      |
| 29.12.7 Performance Schema Transaction Tables 4817                    |      |
| 29.12.8 Performance Schema Connection Tables 4825                     |      |
| 29.12.9 Performance Schema Connection Attribute Tables                | 4829 |
| 29.12.10 Performance Schema User-Defined Variable Tables 4833         |      |
| 29.12.11 Performance Schema Replication Tables 4833                   |      |
| 29.12.12 Performance Schema NDB Cluster Tables 4856                   |      |
| 29.12.13 Performance Schema Lock Tables 4859                          |      |
| 29.12.14 Performance Schema System Variable Tables                    | 4867 |
| 29.12.15 Performance Schema Status Variable Tables 4871               |      |
| 29.12.16 Performance Schema Thread Pool Tables                        | 4873 |
| 29.12.17 Performance Schema Firewall Tables 4880                      |      |
| 29.12.18 Performance Schema Keyring Tables 4881                       |      |
| 29.12.19 Performance Schema Clone Tables 4883                         |      |
| 29.12.20 Performance Schema Summary Tables                            | 4885 |
| 29.12.21 Performance Schema Telemetry Tables 4912                     |      |
| 29.12.22 Performance Schema Miscellaneous Tables 4915                 |      |
| 29.13 Performance Schema Option and Variable Reference 4934           |      |
| 29.14 Performance Schema Command Options                              | 4938 |
| 29.15 Performance Schema System Variables 4939                        |      |
| 29.16 Performance Schema Status Variables 4959                        |      |
| 29.17 The Performance Schema Memory-Allocation Model 4962             |      |
| 29.18 Performance Schema and Plugins 4963                             |      |
| 29.19 Using the Performance Schema to Diagnose Problems 4963          |      |
| 29.19.1 Query Profiling Using Performance Schema 4964                 |      |
| 29.19.2 Obtaining Parent Event Information 4966                       |      |
| 29.20 Restrictions on Performance Schema 4967                         |      |
| 30 MySQL sys Schema 4969                                              |      |
| 30.1 Prerequisites for Using the sys Schema 4969                      |      |
| 30.2 Using the sys Schema 4970                                        |      |
|                                                                       |      |
| 30.3 sys Schema Progress Reporting 4971                               |      |
| 30.4 sys Schema Object Reference 4972                                 |      |
| 30.4.1 sys Schema Object Index 4972                                   |      |
| 30.4.2 sys Schema Tables and Triggers 4977                            |      |
| 30.4.3 sys Schema Views 4979                                          |      |
| 30.4.4 sys Schema Stored Procedures                                   | 5019 |
| 30.4.5 sys Schema Stored Functions 5037                               |      |
| 31 Connectors and APIs 5049                                           |      |
| 31.1 MySQL Connector/C++ 5051                                         |      |
| 31.2 MySQL Connector/J                                                | 5052 |
| 31.3 MySQL Connector/NET                                              | 5052 |
| 31.4 MySQL Connector/ODBC 5052                                        |      |

| 31.5 MySQL Connector/Python                                                       | 5052    |
|-----------------------------------------------------------------------------------|---------|
| 31.6 MySQL Connector/Node.js                                                      | 5052    |
| 31.7 MySQL C API                                                                  | 5052    |
| 31.8 MySQL PHP API                                                                |         |
| 31.9 MySQL Perl API                                                               |         |
| 31.10 MySQL Python API                                                            |         |
| 31.11 MySQL Ruby APIs                                                             |         |
| 31.11.1 The MySQL/Ruby API                                                        |         |
| 31.11.2 The Ruby/MySQL API                                                        |         |
| 31.12 MySQL Tcl API                                                               |         |
| 31.13 MySQL Eiffel Wrapper                                                        |         |
| 32 MySQL Enterprise Edition                                                       |         |
| 32.1 MySQL Enterprise Backup Overview                                             |         |
| 32.2 MySQL Enterprise Security Overview                                           |         |
| 32.3 MySQL Enterprise Encryption Overview                                         |         |
| 32.4 MySQL Enterprise Audit Overview                                              |         |
| 32.5 MySQL Enterprise Firewall Overview                                           |         |
| 32.6 MySQL Enterprise Thread Pool Overview                                        |         |
|                                                                                   |         |
| 32.7 MySQL Enterprise Data Masking and De-Identification Overview                 |         |
| 32.8 MySQL Telemetry                                                              |         |
| 33 MySQL Workbench                                                                |         |
| 34 MySQL on OCI Marketplace                                                       |         |
| 34.1 Prerequisites to Deploying MySQL EE on Oracle Cloud Infrastructure           |         |
| 34.2 Deploying MySQL EE on Oracle Cloud Infrastructure                            |         |
| 34.3 Configuring Network Access                                                   |         |
| 34.4 Connecting                                                                   |         |
| 34.5 Maintenance                                                                  |         |
| 35 Telemetry                                                                      |         |
| 35.1 Installing OpenTelemetry Support                                             |         |
| 35.2 Telemetry Variables                                                          |         |
| 35.3 OpenTelemetry Trace                                                          |         |
| 35.3.1 Configuring Trace Telemetry                                                |         |
| 35.3.2 Trace Format                                                               |         |
| 35.4 OpenTelemetry Metrics                                                        |         |
| 35.4.1 Configuring Metrics Telemetry                                              |         |
| 35.4.2 Server Meters                                                              | . 5083  |
| 35.4.3 Server Metrics                                                             | 5083    |
| A MySQL 8.4 Frequently Asked Questions                                            | . 5099  |
| A.1 MySQL 8.4 FAQ: General                                                        | 5099    |
| A.2 MySQL 8.4 FAQ: Storage Engines                                                | 5101    |
| A.3 MySQL 8.4 FAQ: Server SQL Mode                                                |         |
| A.4 MySQL 8.4 FAQ: Stored Procedures and Functions                                |         |
| A.5 MySQL 8.4 FAQ: Triggers                                                       |         |
| A.6 MySQL 8.4 FAQ: Views                                                          |         |
| A.7 MySQL 8.4 FAQ: INFORMATION_SCHEMA                                             |         |
| A.8 MySQL 8.4 FAQ: Migration                                                      |         |
| A.9 MySQL 8.4 FAQ: Security                                                       |         |
| A.10 MySQL 8.4 FAQ: NDB Cluster                                                   |         |
| A.11 MySQL 8.4 FAQ: MySQL Chinese, Japanese, and Korean Character Sets            |         |
| A.12 MySQL 8.4 FAQ: Connectors & APIs                                             |         |
| A.13 MySQL 8.4 FAQ: C API, libmysql                                               |         |
| A.14 MySQL 8.4 FAQ: C Ar I, librilysql                                            |         |
| A.15 MySQL 8.4 FAQ: Neplication  A.15 MySQL 8.4 FAQ: MySQL Enterprise Thread Pool |         |
| A.16 MySQL 8.4 FAQ: InnoDB Change Buffer                                          |         |
| A.17 MySQL 8.4 FAQ: InnoDB Data-at-Rest Encryption                                |         |
|                                                                                   |         |
| A.18 MySQL 8.4 FAQ: Virtualization Support                                        |         |
| B Error Messages and Common Problems                                              |         |
| DILICHOLIVIESSAGE SOUICES AND FIEITIERIS                                          | . ວ ເ4/ |

# MySQL 8.4 Reference Manual

| B.2 Error Information Interfaces                 | 5149 |
|--------------------------------------------------|------|
| B.3 Problems and Common Errors                   | 5151 |
| B.3.1 How to Determine What Is Causing a Problem | 5151 |
| B.3.2 Common Errors When Using MySQL Programs    |      |
| B.3.3 Administration-Related Issues              | 5163 |
| B.3.4 Query-Related Issues                       | 5171 |
| B.3.5 Optimizer-Related Issues                   | 5177 |
| B.3.6 Table Definition-Related Issues            | 5178 |
| B.3.7 Known Issues in MySQL                      | 5179 |
| C Indexes                                        | 5183 |
| MySQL Glossary                                   | 5955 |

# <span id="page-26-0"></span>Preface and Legal Notices

This is the Reference Manual for the MySQL Database System, for the 8.4.8 LTS release. For license information, see the [Legal Notices](#page-26-1).

This manual is not intended for use with older versions of the MySQL software due to the many functional and other differences between MySQL 8.4 and previous versions. If you are using an earlier release of the MySQL software, please refer to the appropriate manual. For example, [MySQL 8.0](https://dev.mysql.com/doc/refman/8.0/en/) [Reference Manual](https://dev.mysql.com/doc/refman/8.0/en/) covers the 8.0 bugfix series of MySQL software releases.

**Licensing information—MySQL 8.4.** This product may include third-party software, used under license. If you are using a Commercial release of MySQL 8.4, see the [MySQL 8.4 Commercial Release](https://downloads.mysql.com/docs/licenses/mysqld-8.4-com-en.pdf) [License Information User Manual](https://downloads.mysql.com/docs/licenses/mysqld-8.4-com-en.pdf) for licensing information, including licensing information relating to third-party software that may be included in this Commercial release. If you are using a Community release of MySQL 8.4, see the [MySQL 8.4 Community Release License Information User Manual](https://downloads.mysql.com/docs/licenses/mysqld-8.4-gpl-en.pdf) for licensing information, including licensing information relating to third-party software that may be included in this Community release.

**Licensing information—MySQL NDB Cluster 8.4.** This product may include third-party software, used under license. If you are using a Commercial release of MySQL NDB Cluster 8.4, see the [MySQL](https://downloads.mysql.com/docs/licenses/cluster-8.4-com-en.pdf) [NDB Cluster 8.4 Commercial Release License Information User Manual](https://downloads.mysql.com/docs/licenses/cluster-8.4-com-en.pdf) for licensing information, including licensing information relating to third-party software that may be included in this Commercial release. If you are using a Community release of MySQL NDB Cluster 8.4, see the [MySQL NDB](https://downloads.mysql.com/docs/licenses/cluster-8.4-gpl-en.pdf) [Cluster 8.4 Community Release License Information User Manual](https://downloads.mysql.com/docs/licenses/cluster-8.4-gpl-en.pdf) for licensing information, including licensing information relating to third-party software that may be included in this Community release.

# <span id="page-26-1"></span>**Legal Notices**

Copyright © 1997, 2026, Oracle and/or its affiliates.

### **License Restrictions**

This software and related documentation are provided under a license agreement containing restrictions on use and disclosure and are protected by intellectual property laws. Except as expressly permitted in your license agreement or allowed by law, you may not use, copy, reproduce, translate, broadcast, modify, license, transmit, distribute, exhibit, perform, publish, or display any part, in any form, or by any means. Reverse engineering, disassembly, or decompilation of this software, unless required by law for interoperability, is prohibited.

### **Warranty Disclaimer**

The information contained herein is subject to change without notice and is not warranted to be errorfree. If you find any errors, please report them to us in writing.

## **Restricted Rights Notice**

If this is software, software documentation, data (as defined in the Federal Acquisition Regulation), or related documentation that is delivered to the U.S. Government or anyone licensing it on behalf of the U.S. Government, then the following notice is applicable:

U.S. GOVERNMENT END USERS: Oracle programs (including any operating system, integrated software, any programs embedded, installed, or activated on delivered hardware, and modifications of such programs) and Oracle computer documentation or other Oracle data delivered to or accessed by U.S. Government end users are "commercial computer software," "commercial computer software documentation," or "limited rights data" pursuant to the applicable Federal Acquisition Regulation and agency-specific supplemental regulations. As such, the use, reproduction, duplication, release, display, disclosure, modification, preparation of derivative works, and/or adaptation of i) Oracle programs (including any operating system, integrated software, any programs embedded, installed, or activated on delivered hardware, and modifications of such programs), ii) Oracle computer documentation and/

or iii) other Oracle data, is subject to the rights and limitations specified in the license contained in the applicable contract. The terms governing the U.S. Government's use of Oracle cloud services are defined by the applicable contract for such services. No other rights are granted to the U.S. Government.

### **Hazardous Applications Notice**

This software or hardware is developed for general use in a variety of information management applications. It is not developed or intended for use in any inherently dangerous applications, including applications that may create a risk of personal injury. If you use this software or hardware in dangerous applications, then you shall be responsible to take all appropriate fail-safe, backup, redundancy, and other measures to ensure its safe use. Oracle Corporation and its affiliates disclaim any liability for any damages caused by use of this software or hardware in dangerous applications.

### **Trademark Notice**

Oracle, Java, MySQL, and NetSuite are registered trademarks of Oracle and/or its affiliates. Other names may be trademarks of their respective owners.

Intel and Intel Inside are trademarks or registered trademarks of Intel Corporation. All SPARC trademarks are used under license and are trademarks or registered trademarks of SPARC International, Inc. AMD, Epyc, and the AMD logo are trademarks or registered trademarks of Advanced Micro Devices. UNIX is a registered trademark of The Open Group.

### **Third-Party Content, Products, and Services Disclaimer**

This software or hardware and documentation may provide access to or information about content, products, and services from third parties. Oracle Corporation and its affiliates are not responsible for and expressly disclaim all warranties of any kind with respect to third-party content, products, and services unless otherwise set forth in an applicable agreement between you and Oracle. Oracle Corporation and its affiliates will not be responsible for any loss, costs, or damages incurred due to your access to or use of third-party content, products, or services, except as set forth in an applicable agreement between you and Oracle.

### **Use of This Documentation**

This documentation is NOT distributed under a GPL license. Use of this documentation is subject to the following terms:

You may create a printed copy of this documentation solely for your own personal use. Conversion to other formats is allowed as long as the actual content is not altered or edited in any way. You shall not publish or distribute this documentation in any form or on any media, except if you distribute the documentation in a manner similar to how Oracle disseminates it (that is, electronically for download on a Web site with the software) or on a CD-ROM or similar medium, provided however that the documentation is disseminated together with the software on the same medium. Any other use, such as any dissemination of printed copies or use of this documentation, in whole or in part, in another publication, requires the prior written consent from an authorized representative of Oracle. Oracle and/ or its affiliates reserve any and all rights to this documentation not expressly granted above.

# **Documentation Accessibility**

For information about Oracle's commitment to accessibility, visit the Oracle Accessibility Program website at

[http://www.oracle.com/pls/topic/lookup?ctx=acc&id=docacc.](http://www.oracle.com/pls/topic/lookup?ctx=acc&id=docacc)

# **Access to Oracle Support for Accessibility**

Oracle customers that have purchased support have access to electronic support through My Oracle Support. For information, visit

|  | topic/lookup?ctx=acc&id=trs if you are hearing impaired. |  |  |
|--|----------------------------------------------------------|--|--|
|  |                                                          |  |  |
|  |                                                          |  |  |
|  |                                                          |  |  |
|  |                                                          |  |  |
|  |                                                          |  |  |
|  |                                                          |  |  |
|  |                                                          |  |  |
|  |                                                          |  |  |
|  |                                                          |  |  |
|  |                                                          |  |  |
|  |                                                          |  |  |
|  |                                                          |  |  |
|  |                                                          |  |  |
|  |                                                          |  |  |
|  |                                                          |  |  |
|  |                                                          |  |  |
|  |                                                          |  |  |
|  |                                                          |  |  |
|  |                                                          |  |  |
|  |                                                          |  |  |
|  |                                                          |  |  |
|  |                                                          |  |  |
|  |                                                          |  |  |
|  |                                                          |  |  |
|  |                                                          |  |  |
|  |                                                          |  |  |
|  |                                                          |  |  |
|  |                                                          |  |  |

# <span id="page-30-0"></span>Chapter 1 General Information

# **Table of Contents**

| 1.1 About This Manual 2                                                                |    |
|----------------------------------------------------------------------------------------|----|
| 1.2 Overview of the MySQL Database Management System 4                                 |    |
| 1.2.1 What is MySQL? 4                                                                 |    |
| 1.2.2 The Main Features of MySQL 5                                                     |    |
| 1.2.3 History of MySQL 8                                                               |    |
| 1.3 MySQL Releases: Innovation and LTS                                                 | 9  |
| 1.4 What Is New in MySQL 8.4 since MySQL 8.0 10                                        |    |
| 1.5 Server and Status Variables and Options Added, Deprecated, or Removed in MySQL 8.4 |    |
| since 8.0                                                                              | 33 |
| 1.6 How to Report Bugs or Problems 41                                                  |    |
| 1.7 MySQL Standards Compliance 45                                                      |    |
| 1.7.1 MySQL Extensions to Standard SQL 46                                              |    |
| 1.7.2 MySQL Differences from Standard SQL 49                                           |    |
| 1.7.3 How MySQL Deals with Constraints 52                                              |    |

The MySQL software delivers a very fast, multithreaded, multi-user, and robust SQL (Structured Query Language) database server. MySQL Server is intended for mission-critical, heavy-load production systems as well as for embedding into mass-deployed software. Oracle is a registered trademark of Oracle Corporation and/or its affiliates. MySQL is a trademark of Oracle Corporation and/or its affiliates, and shall not be used by Customer without Oracle's express written authorization. Other names may be trademarks of their respective owners.

The MySQL software is Dual Licensed. Users can choose to use the MySQL software as an Open Source product under the terms of the GNU General Public License [\(http://www.fsf.org/licenses/](http://www.fsf.org/licenses/)) or can purchase a standard commercial license from Oracle. See [http://www.mysql.com/company/legal/](http://www.mysql.com/company/legal/licensing/) [licensing/](http://www.mysql.com/company/legal/licensing/) for more information on our licensing policies.

The following list describes some sections of particular interest in this manual:

- For a discussion of MySQL Database Server capabilities, see [Section 1.2.2, "The Main Features of](#page-34-0) [MySQL".](#page-34-0)
- For an overview of new MySQL features, see [Section 1.4, "What Is New in MySQL 8.4 since MySQL](#page-39-0) [8.0"](#page-39-0). For information about the changes in each version, see the [Release Notes.](https://dev.mysql.com/doc/relnotes/mysql/8.4/en/)
- For installation instructions, see Chapter 2, [Installing MySQL](#page-84-0). For information about upgrading MySQL, see Chapter 3, Upgrading MySQL.
- For a tutorial introduction to the MySQL Database Server, see Chapter 5, Tutorial.
- For information about configuring and administering MySQL Server, see Chapter 7, MySQL Server Administration.
- For information about security in MySQL, see Chapter 8, Security.
- For information about setting up replication servers, see Chapter 19, Replication.
- For information about MySQL Enterprise, the commercial MySQL release with advanced features and management tools, see Chapter 32, MySQL Enterprise Edition.
- For answers to a number of questions that are often asked concerning the MySQL Database Server and its capabilities, see Appendix A, MySQL 8.4 Frequently Asked Questions.

• For a history of new features and bug fixes, see the [Release Notes.](https://dev.mysql.com/doc/relnotes/mysql/8.4/en/)

![](_page_31_Picture_2.jpeg)

### **Important**

To report problems or bugs, please use the instructions at [Section 1.6,](#page-70-0) ["How to Report Bugs or Problems"](#page-70-0). If you find a security bug in MySQL Server, please let us know immediately by sending an email message to <secalert\_us@oracle.com>. Exception: Support customers should report all problems, including security bugs, to Oracle Support.

# <span id="page-31-0"></span>**1.1 About This Manual**

This is the Reference Manual for the MySQL Database System, version 8.4, through release 8.4.8. Differences between minor versions of MySQL 8.4 are noted in the present text with reference to release numbers (8.4.x). For license information, see the [Legal Notices](#page-26-1).

This manual is not intended for use with older versions of the MySQL software due to the many functional and other differences between MySQL 8.4 and previous versions. If you are using an earlier release of the MySQL software, please refer to the appropriate manual. For example, the [MySQL 8.0](https://dev.mysql.com/doc/refman/8.0/en/) [Reference Manual](https://dev.mysql.com/doc/refman/8.0/en/) covers the 8.0 bugfix series of MySQL software releases.

Because this manual serves as a reference, it does not provide general instruction on SQL or relational database concepts. It also does not teach you how to use your operating system or command-line interpreter.

The MySQL Database Software is under constant development, and the Reference Manual is updated frequently as well. The most recent version of the manual is available online in searchable form at <https://dev.mysql.com/doc/>. Other formats also are available there, including downloadable HTML and PDF versions.

The source code for MySQL itself contains internal documentation written using Doxygen. The generated Doxygen content is available from [https://dev.mysql.com/doc/index-other.html.](https://dev.mysql.com/doc/index-other.md) It is also possible to generate this content locally from a MySQL source distribution using the instructions at Section 2.8.10, "Generating MySQL Doxygen Documentation Content".

If you have questions about using MySQL, join the [MySQL Community Slack.](https://mysqlcommunity.slack.com/) If you have suggestions concerning additions or corrections to the manual itself, please send them to the [http://www.mysql.com/](http://www.mysql.com/company/contact/) [company/contact/](http://www.mysql.com/company/contact/).

# **Typographical and Syntax Conventions**

This manual uses certain typographical conventions:

- Text in this style is used for SQL statements; database, table, and column names; program listings and source code; and environment variables. Example: "To reload the grant tables, use the FLUSH PRIVILEGES statement."
- **Text in this style** indicates input that you type in examples.
- Text in this style indicates the names of executable programs and scripts, examples being mysql (the MySQL command-line client program) and mysqld (the MySQL server executable).
- Text in this style is used for variable input for which you should substitute a value of your own choosing.
- Text in this style is used for emphasis.
- **Text in this style** is used in table headings and to convey especially strong emphasis.

- Text in this style is used to indicate a program option that affects how the program is executed, or that supplies information that is needed for the program to function in a certain way. Example: "The --host option (short form -h) tells the mysql client program the hostname or IP address of the MySQL server that it should connect to".
- File names and directory names are written like this: "The global my.cnf file is located in the /etc directory."
- Character sequences are written like this: "To specify a wildcard, use the '%' character."

When commands or statements are prefixed by a prompt, we use these:

```
$> type a command here
#> type a command as root here
C:\> type a command here (Windows only)
mysql> type a mysql statement here
```

Commands are issued in your command interpreter. On Unix, this is typically a program such as sh, csh, or bash. On Windows, the equivalent program is command.com or cmd.exe, typically run in a console window. Statements prefixed by mysql are issued in the mysql command-line client.

![](_page_32_Picture_7.jpeg)

### **Note**

When you enter a command or statement shown in an example, do not type the prompt shown in the example.

In some areas different systems may be distinguished from each other to show that commands should be executed in two different environments. For example, while working with replication the commands might be prefixed with source and replica:

```
source> type a mysql statement on the replication source here
replica> type a mysql statement on the replica here
```

Database, table, and column names must often be substituted into statements. To indicate that such substitution is necessary, this manual uses db\_name, tbl\_name, and col\_name. For example, you might see a statement like this:

```
mysql> SELECT col_name FROM db_name.tbl_name;
```

This means that if you were to enter a similar statement, you would supply your own database, table, and column names, perhaps like this:

```
mysql> SELECT author_name FROM biblio_db.author_list;
```

SQL keywords are not case-sensitive and may be written in any lettercase. This manual uses uppercase.

In syntax descriptions, square brackets ("[" and "]") indicate optional words or clauses. For example, in the following statement, IF EXISTS is optional:

```
DROP TABLE [IF EXISTS] tbl_name
```

When a syntax element consists of a number of alternatives, the alternatives are separated by vertical bars ("|"). When one member from a set of choices may be chosen, the alternatives are listed within square brackets ("[" and "]"):

```
TRIM([[BOTH | LEADING | TRAILING] [remstr] FROM] str)
```

When one member from a set of choices must be chosen, the alternatives are listed within braces ("{" and "}"):

```
{DESCRIBE | DESC} tbl_name [col_name | wild]
```

An ellipsis (...) indicates the omission of a section of a statement, typically to provide a shorter version of more complex syntax. For example, SELECT ... INTO OUTFILE is shorthand for the form of SELECT statement that has an INTO OUTFILE clause following other parts of the statement.

An ellipsis can also indicate that the preceding syntax element of a statement may be repeated. In the following example, multiple reset\_option values may be given, with each of those after the first preceded by commas:

```
RESET reset_option [,reset_option] ...
```

Commands for setting shell variables are shown using Bourne shell syntax. For example, the sequence to set the CC environment variable and run the configure command looks like this in Bourne shell syntax:

```
$> CC=gcc ./configure
```

If you are using csh or tcsh, you must issue commands somewhat differently:

```
$> setenv CC gcc
$> ./configure
```

# **Manual Authorship**

The Reference Manual source files are written in DocBook XML format. The HTML version and other formats are produced automatically, primarily using the DocBook XSL stylesheets. For information about DocBook, see <http://docbook.org/>

This manual was originally written by David Axmark and Michael "Monty" Widenius. It is maintained by the MySQL Documentation Team, consisting of Edward Gilmore, Sudharsana Gomadam, Kim seong Loh, Garima Sharma, Carlos Ortiz, Daniel So, and Jon Stephens.

# <span id="page-33-0"></span>**1.2 Overview of the MySQL Database Management System**

# <span id="page-33-1"></span>**1.2.1 What is MySQL?**

MySQL, the most popular Open Source SQL database management system, is developed, distributed, and supported by Oracle Corporation.

The MySQL website [\(http://www.mysql.com/](http://www.mysql.com/)) provides the latest information about MySQL software.

# • **MySQL is a database management system.**

A database is a structured collection of data. It may be anything from a simple shopping list to a picture gallery or the vast amounts of information in a corporate network. To add, access, and process data stored in a computer database, you need a database management system such as MySQL Server. Since computers are very good at handling large amounts of data, database management systems play a central role in computing, as standalone utilities, or as parts of other applications.

### • **MySQL databases are relational.**

 A relational database stores data in separate tables rather than putting all the data in one big storeroom. The database structures are organized into physical files optimized for speed. The logical model, with objects such as databases, tables, views, rows, and columns, offers a flexible programming environment. You set up rules governing the relationships between different data fields, such as one-to-one, one-to-many, unique, required or optional, and "pointers" between different tables. The database enforces these rules, so that with a well-designed database, your application never sees inconsistent, duplicate, orphan, out-of-date, or missing data.

The SQL part of "MySQL" stands for "Structured Query Language". SQL is the most common standardized language used to access databases. Depending on your programming environment, you might enter SQL directly (for example, to generate reports), embed SQL statements into code written in another language, or use a language-specific API that hides the SQL syntax.

SQL is defined by the ANSI/ISO SQL Standard. The SQL standard has been evolving since 1986 and several versions exist. In this manual, "SQL-92" refers to the standard released in 1992, "SQL:1999" refers to the standard released in 1999, and "SQL:2003" refers to the current version of the standard. We use the phrase "the SQL standard" to mean the current version of the SQL Standard at any time.

### • **MySQL software is Open Source.**

 Open Source means that it is possible for anyone to use and modify the software. Anybody can download the MySQL software from the Internet and use it without paying anything. If you wish, you may study the source code and change it to suit your needs. The MySQL software uses the GPL (GNU General Public License), [http://www.fsf.org/licenses/,](http://www.fsf.org/licenses/) to define what you may and may not do with the software in different situations. If you feel uncomfortable with the GPL or need to embed MySQL code into a commercial application, you can buy a commercially licensed version from us. See the MySQL Licensing Overview for more information [\(http://www.mysql.com/company/legal/](http://www.mysql.com/company/legal/licensing/) [licensing/\)](http://www.mysql.com/company/legal/licensing/).

## • **The MySQL Database Server is very fast, reliable, scalable, and easy to use.**

If that is what you are looking for, you should give it a try. MySQL Server can run comfortably on a desktop or laptop, alongside your other applications, web servers, and so on, requiring little or no attention. If you dedicate an entire machine to MySQL, you can adjust the settings to take advantage of all the memory, CPU power, and I/O capacity available. MySQL can also scale up to clusters of machines, networked together.

MySQL Server was originally developed to handle large databases much faster than existing solutions and has been successfully used in highly demanding production environments for several years. Although under constant development, MySQL Server today offers a rich and useful set of functions. Its connectivity, speed, and security make MySQL Server highly suited for accessing databases on the Internet.

### • **MySQL Server works in client/server or embedded systems.**

The MySQL Database Software is a client/server system that consists of a multithreaded SQL server that supports different back ends, several different client programs and libraries, administrative tools, and a wide range of application programming interfaces (APIs).

We also provide MySQL Server as an embedded multithreaded library that you can link into your application to get a smaller, faster, easier-to-manage standalone product.

### • **A large amount of contributed MySQL software is available.**

MySQL Server has a practical set of features developed in close cooperation with our users. It is very likely that your favorite application or language supports the MySQL Database Server.

### • **MySQL HeatWave.**

MySQL HeatWave is a fully managed database service, powered by the MySQL HeatWave inmemory query accelerator. It is the only cloud service that combines transactions, real-time analytics across data warehouses and data lakes, and machine learning in one MySQL Database; without the complexity, latency, risks, and cost of ETL duplication. It is available on OCI, AWS, and Azure. Learn more at:<https://www.oracle.com/mysql/>.

The official way to pronounce "MySQL" is "My Ess Que Ell" (not "my sequel"), but we do not mind if you pronounce it as "my sequel" or in some other localized way.

# <span id="page-34-0"></span>**1.2.2 The Main Features of MySQL**

This section describes some of the important characteristics of the MySQL Database Software. In most respects, the roadmap applies to all versions of MySQL. For information about features as they are introduced into MySQL on a series-specific basis, see the "In a Nutshell" section of the appropriate Manual:

- MySQL 8.4: [Section 1.4, "What Is New in MySQL 8.4 since MySQL 8.0"](#page-39-0)
- MySQL 8.0: [What Is New in MySQL 8.0](https://dev.mysql.com/doc/refman/8.0/en/mysql-nutshell.md)
- MySQL 5.7: [What Is New in MySQL 5.7](https://dev.mysql.com/doc/refman/5.7/en/mysql-nutshell.md)

# **Internals and Portability**

- Written in C and C++.
- Tested with a broad range of different compilers.
- Works on many different platforms. See [https://www.mysql.com/support/supportedplatforms/](https://www.mysql.com/support/supportedplatforms/database.md) [database.html.](https://www.mysql.com/support/supportedplatforms/database.md)
- For portability, configured using CMake.
- Tested with Purify (a commercial memory leakage detector) as well as with Valgrind, a GPL tool [\(https://valgrind.org/](https://valgrind.org/)).
- Uses multi-layered server design with independent modules.
- Designed to be fully multithreaded using kernel threads, to easily use multiple CPUs if they are available.
- Provides transactional and nontransactional storage engines.
- Uses very fast B-tree disk tables (MyISAM) with index compression.
- Designed to make it relatively easy to add other storage engines. This is useful if you want to provide an SQL interface for an in-house database.
- Uses a very fast thread-based memory allocation system.
- Executes very fast joins using an optimized nested-loop join.
- Implements in-memory hash tables, which are used as temporary tables.
- Implements SQL functions using a highly optimized class library that should be as fast as possible. Usually there is no memory allocation at all after query initialization.
- Provides the server as a separate program for use in a client/server networked environment.

# **Data Types**

- Many data types: signed/unsigned integers 1, 2, 3, 4, and 8 bytes long, FLOAT, DOUBLE, CHAR, VARCHAR, BINARY, VARBINARY, TEXT, BLOB, DATE, TIME, DATETIME, TIMESTAMP, YEAR, SET, ENUM, and OpenGIS spatial types. See Chapter 13, Data Types.
- Fixed-length and variable-length string types.

# **Statements and Functions**

• Full operator and function support in the SELECT list and WHERE clause of queries. For example:

```
mysql> SELECT CONCAT(first_name, ' ', last_name)
 -> FROM citizen
 -> WHERE income/dependents > 10000 AND age > 30;
```

- Full support for SQL GROUP BY and ORDER BY clauses. Support for group functions (COUNT(), AVG(), STD(), SUM(), MAX(), MIN(), and GROUP\_CONCAT()).
- Support for LEFT OUTER JOIN and RIGHT OUTER JOIN with both standard SQL and ODBC syntax.
- Support for aliases on tables and columns as required by standard SQL.
- Support for DELETE, INSERT, REPLACE, and UPDATE to return the number of rows that were changed (affected), or to return the number of rows matched instead by setting a flag when connecting to the server.
- Support for MySQL-specific SHOW statements that retrieve information about databases, storage engines, tables, and indexes. Support for the INFORMATION\_SCHEMA database, implemented according to standard SQL.
- An EXPLAIN statement to show how the optimizer resolves a query.
- Independence of function names from table or column names. For example, ABS is a valid column name. The only restriction is that for a function call, no spaces are permitted between the function name and the "(" that follows it. See Section 11.3, "Keywords and Reserved Words".
- You can refer to tables from different databases in the same statement.

# **Security**

- A privilege and password system that is very flexible and secure, and that enables host-based verification.
- Password security by encryption of all password traffic when you connect to a server.

# **Scalability and Limits**

- Support for large databases. We use MySQL Server with databases that contain 50 million records. We also know of users who use MySQL Server with 200,000 tables and about 5,000,000,000 rows.
- Support for up to 64 indexes per table. Each index may consist of 1 to 16 columns or parts of columns. The maximum index width for InnoDB tables is either 767 bytes or 3072 bytes. See Section 17.21, "InnoDB Limits". The maximum index width for MyISAM tables is 1000 bytes. See Section 18.2, "The MyISAM Storage Engine". An index may use a prefix of a column for CHAR, VARCHAR, BLOB, or TEXT column types.

# **Connectivity**

- Clients can connect to MySQL Server using several protocols:
  - Clients can connect using TCP/IP sockets on any platform.
  - On Windows systems, clients can connect using named pipes if the server is started with the named\_pipe system variable enabled. Windows servers also support shared-memory connections if started with the shared\_memory system variable enabled. Clients can connect through shared memory by using the --protocol=memory option.
  - On Unix systems, clients can connect using Unix domain socket files.
- MySQL client programs can be written in many languages. A client library written in C is available for clients written in C or C++, or for any language that provides C bindings.
- APIs for C, C++, Eiffel, Java, Perl, PHP, Python, Ruby, and Tcl are available, enabling MySQL clients to be written in many languages. See Chapter 31, Connectors and APIs.
- The Connector/ODBC (MyODBC) interface provides MySQL support for client programs that use ODBC (Open Database Connectivity) connections. For example, you can use MS Access to connect

to your MySQL server. Clients can be run on Windows or Unix. Connector/ODBC source is available. All ODBC 2.5 functions are supported, as are many others. See [MySQL Connector/ODBC Developer](https://dev.mysql.com/doc/connector-odbc/en/) [Guide.](https://dev.mysql.com/doc/connector-odbc/en/)

- The Connector/J interface provides MySQL support for Java client programs that use JDBC connections. Clients can be run on Windows or Unix. Connector/J source is available. See [MySQL](https://dev.mysql.com/doc/connector-j/en/) [Connector/J Developer Guide.](https://dev.mysql.com/doc/connector-j/en/)
- MySQL Connector/NET enables developers to easily create .NET applications that require secure, high-performance data connectivity with MySQL. It implements the required ADO.NET interfaces and integrates into ADO.NET aware tools. Developers can build applications using their choice of .NET languages. MySQL Connector/NET is a fully managed ADO.NET driver written in 100% pure C#. See [MySQL Connector/NET Developer Guide](https://dev.mysql.com/doc/connector-net/en/).

# **Localization**

- The server can provide error messages to clients in many languages. See Section 12.12, "Setting the Error Message Language".
- Full support for several different character sets, including latin1 (cp1252), german, big5, ujis, several Unicode character sets, and more. For example, the Scandinavian characters "å", "ä" and "ö" are permitted in table and column names.
- All data is saved in the chosen character set.
- Sorting and comparisons are done according to the default character set and collation. It is possible to change this when the MySQL server is started (see Section 12.3.2, "Server Character Set and Collation"). To see an example of very advanced sorting, look at the Czech sorting code. MySQL Server supports many different character sets that can be specified at compile time and runtime.
- The server time zone can be changed dynamically, and individual clients can specify their own time zone. See Section 7.1.15, "MySQL Server Time Zone Support".

# **Clients and Tools**

- MySQL includes several client and utility programs. These include both command-line programs such as mysqldump and mysqladmin, and graphical programs such as MySQL Workbench.
- MySQL Server has built-in support for SQL statements to check, optimize, and repair tables. These statements are available from the command line through the mysqlcheck client. MySQL also includes myisamchk, a very fast command-line utility for performing these operations on MyISAM tables. See Chapter 6, MySQL Programs.
- MySQL programs can be invoked with the --help or -? option to obtain online assistance.

# <span id="page-37-0"></span>**1.2.3 History of MySQL**

We started out with the intention of using the mSQL database system to connect to our tables using our own fast low-level (ISAM) routines. However, after some testing, we came to the conclusion that mSQL was not fast enough or flexible enough for our needs. This resulted in a new SQL interface to our database but with almost the same API interface as mSQL. This API was designed to enable third-party code that was written for use with mSQL to be ported easily for use with MySQL.

MySQL is named after co-founder Monty Widenius's daughter, My.

The name of the MySQL Dolphin (our logo) is "Sakila," which was chosen from a huge list of names suggested by users in our "Name the Dolphin" contest. The winning name was submitted by Ambrose Twebaze, an Open Source software developer from Eswatini (formerly Swaziland), Africa. According to Ambrose, the feminine name Sakila has its roots in SiSwati, the local language of Eswatini. Sakila is also the name of a town in Arusha, Tanzania, near Ambrose's country of origin, Uganda.

# <span id="page-38-0"></span>**1.3 MySQL Releases: Innovation and LTS**

The MySQL release model is divided into two main tracks: LTS (Long-Term Support) and Innovation. All LTS and Innovation releases include bug and security fixes, and are considered production-grade quality.

**Figure 1.1 MySQL Release Schedule**

# **MySQL LTS Releases**

- Audience: If your environment requires a stable set of features and a longer support period.
- Behavior: These releases only contain necessary fixes to reduce the risks associated with changes in the database software's behavior. There are no removals within an LTS release. Features can be removed (and added) only in the first LTS release (such as 8.4.0 LTS) but not later.
- Support: An LTS series follows the [Oracle Lifetime Support](https://www.oracle.com/support/lifetime-support/software.md) Policy, which includes 5 years of premier support and 3 years of extended support.

# **MySQL Innovation Releases**

- Audience: If you want access to the latest features, improvements, and changes. These releases are ideal for developers and DBAs working in fast-paced development environments with high levels of automated tests and modern continuous integration techniques for faster upgrade cycles.
- Behavior: Apart from new features in innovation releases, behavior changes are also expected as code is refactored, deprecated functionality is removed, and when MySQL is modified to behave more in line with SQL Standards. This will not happen within an LTS release.

Behavior changes can have a big impact, especially when dealing with anything application-related, such as SQL syntax, new reserved words, query execution, and query performance. Behavior changes might require application changes which can involve considerable effort to migrate. We intend to provide the necessary tools and configuration settings to make these transitions easier.

• Support: Innovation releases are supported until the next Innovation release.

# **MySQL Portfolio**

MySQL Server, MySQL Shell, MySQL Router, MySQL Operator for Kubernetes, and MySQL NDB Cluster have both Innovation and LTS releases.

MySQL Connectors have one release using the latest version number but remain compatible with all supported MySQL Server versions. For example, MySQL Connector/Python 9.0.0 is compatible with MySQL Server 8.0, 8.4, and 9.0.

# **Installing, Upgrading, and Downgrading**

Having two tracks affects how MySQL is installed, upgraded, and downgraded. Typically you choose one particular track and all upgrades progress accordingly.

When using the official MySQL repository, the desired track is defined in the repository configuration. For example, with [Yum](#page-153-0) choose mysql-innovation-community to install and upgrade Innovation releases or mysql-8.4-lts-community to install and upgrade MySQL 8.4.x releases.

### **LTS Notes**

Functionality remains the same and data format does not change in an LTS series, therefore in-place upgrades and downgrades are possible within the LTS series. For example, MySQL 8.4.0 can be upgraded to a later MySQL 8.4.x release. Additional upgrade and downgrade methods are available, such as the clone plugin.

Upgrading to the next LTS series is supported, such as 8.4.x LTS to 9.7.x LTS, while skipping an LTS series is not supported. For example, 8.4.x LTS can't skip 9.7.x LTS to directly upgrade to 10.7.x LTS.

### **Innovation Notes**

An Innovation installation follows similar behavior in that an Innovation release upgrades to a more recent Innovation series release. For example, MySQL 9.0.0 Innovation would upgrade to MySQL 9.3.0.

The main difference is that you cannot directly upgrade between an Innovation series of different major versions, such as 8.3.0 to 9.0.0. Instead, first upgrade to the nearest LTS series and then upgrade to the following Innovation series. For example, upgrading 8.3.0 to 8.4.0, and then 8.4.0 to 9.0.0, is a valid upgrade path.

To help make the transition easier, the official MySQL repository treats the first LTS release as both LTS and Innovation, so for example with the Innovation track enabled in your local repository configuration, MySQL 8.3.0 upgrades to 8.4.0, and later to 9.0.0.

Innovation release downgrades require a logical dump and load.

### **Additional Information and Examples**

For additional information and specific example supported scenarios, see Section 3.2, "Upgrade Paths" or Chapter 4, Downgrading MySQL. They describe available options to perform in-place updates (that replace binaries with the latest packages), a logical dump and load (such as using mysqldump or [MySQL Shell's dump utilities](https://dev.mysql.com/doc/mysql-shell/8.4/en/mysql-shell-utilities-dump-instance-schema.md)), cloning data with the clone plugin, and asynchronous replication for servers in a replication topology.

# <span id="page-39-0"></span>**1.4 What Is New in MySQL 8.4 since MySQL 8.0**

This section summarizes what has been added to, deprecated in, changed, and removed from MySQL 8.4 since MySQL 8.0. A companion section lists MySQL server options and variables that have been added, deprecated, or removed in MySQL 8.4; see [Section 1.5, "Server and Status Variables and](#page-62-0) [Options Added, Deprecated, or Removed in MySQL 8.4 since 8.0".](#page-62-0)

• [Features Added or Changed in MySQL 8.4](#page-40-0)

- [Features Deprecated in MySQL 8.4](#page-51-0)
- [Features Removed in MySQL 8.4](#page-52-0)

# <span id="page-40-0"></span>**Features Added or Changed in MySQL 8.4**

The following features have been added to MySQL 8.4:

• **MySQL native password authentication changes.** Beginning with MySQL 8.4.0, the deprecated mysql\_native\_password authentication plugin is no longer enabled by default. To enable it, start the server with --mysql-native-password=ON (added in MySQL 8.4.0), or by including mysql\_native\_password=ON in the [mysqld] section of your MySQL configuration file (added in MySQL 8.4.0).

For more information about enabling, using, and disabling mysql\_native\_password, see Section 8.4.1.1, "Native Pluggable Authentication".

• **InnoDB system variable default value changes.** The default values for a number of server system variables relating to the InnoDB storage engine were changed in MySQL 8.4.0, as shown in the following table:

**Table 1.1 InnoDB system variable default values in MySQL 8.4 differing from MySQL 8.0**

| InnoDB<br>System<br>Variable<br>Name | New Default Value (MySQL 8.4)                                                                                                                                                                                                                                                                                                                                                                                                                                   | Previous Default Value (MySQL 8.0)             |
|--------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------|
|                                      | OFF if MADV_DONTDUMP is supported,<br>innodb_buffer_pool_in_core_file<br>otherwise ON                                                                                                                                                                                                                                                                                                                                                                           | ON                                             |
|                                      | If innodb_buffer_pool_size<br>innodb_buffer_pool_instances<br><= 1 GiB, then<br>innodb_buffer_pool_instances=1<br>If innodb_buffer_pool_size > 1 GiB,<br>then this is the minimum value from the<br>following two calculated hints in the range of<br>1-64:<br>•<br>Buffer pool hint: Calculated as 1/2<br>of (innodb_buffer_pool_size /<br>innodb_buffer_pool_chunk_size)<br>•<br>CPU hint: Calculated as 1/4 of the<br>number of available logical processors | 8 (or 1 if innodb_buffer_pool_size < 1<br>GiB) |
|                                      | innodb_change_buffering<br>none                                                                                                                                                                                                                                                                                                                                                                                                                                 | all                                            |
| <br>innodb<br>dedicated<br>server    | If ON, the value of innodb_flush_method<br>is no longer changed as in<br>MySQL 8.0, but the calculation of<br>innodb_redo_log_capacity is changed<br>from memory-based to CPU-based. For<br>more information, see Section 17.8.12,<br>"Enabling Automatic InnoDB Configuration<br>for a Dedicated MySQL Server". (The actual<br>default value of this variable is OFF; this is<br>unchanged from MySQL 8.0.)                                                    | OFF                                            |
|                                      | innodb_adaptive_hash_index<br>OFF                                                                                                                                                                                                                                                                                                                                                                                                                               | ON                                             |
|                                      | 2<br>innodb_doublewrite_files                                                                                                                                                                                                                                                                                                                                                                                                                                   | innodb_buffer_pool_instances * 2               |

| InnoDB<br>System<br>Variable<br>Name  | New Default Value (MySQL 8.4)                                                                          | Previous Default Value (MySQL 8.0)                              |
|---------------------------------------|--------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------|
|                                       | 128<br>innodb_doublewrite_pages                                                                        | innodb_write_io_threads, which<br>meant a default of 4          |
| on Linux                              | O_DIRECT if supported, otherwise fsync<br>innodb_flush_method                                          | fsync                                                           |
|                                       | 10000<br>innodb_io_capacity                                                                            | 200                                                             |
|                                       | 2 * innodb_io_capacity<br>innodb_io_capacity_max                                                       | 2 * innodb_io_capacity, with a<br>minimum default value of 2000 |
|                                       | 67108864 (64 MiB)<br>innodb_log_buffer_size                                                            | 16777216 (16 MiB)                                               |
|                                       | innodb_numa_interleave<br>ON                                                                           | OFF                                                             |
|                                       | innodb_page_cleaners<br>innodb_buffer_pool_instances                                                   | 4                                                               |
|                                       | available logical processors / 8, with a<br>innodb_parallel_read_threads<br>minimum default value of 4 | 4                                                               |
|                                       | 1 if available logical processors is <= 16,<br>innodb_purge_threads<br>otherwise 4                     | 4                                                               |
|                                       | available logical processors / 2, with a<br>innodb_read_io_threads<br>minimum default value of 4       | 4                                                               |
|                                       | innodb_use_fdatasync<br>ON                                                                             | OFF                                                             |
|                                       | 3% of total memory, with a default value<br>temptable_max_ram<br>within a range of 1-4 GiB             | 1073741824 (1 GiB)                                              |
|                                       | 0, which means OFF<br>temptable_max_mmap                                                               | 1073741824 (1 GiB)                                              |
| (Deprecated<br>in<br>MySQL<br>8.0.26) | temptable_use_mmap<br>OFF                                                                              | ON                                                              |

• **Clone plugin.** The clone plugin versioning requirement was relaxed to allow cloning between different point releases in the same series. In other words, only the major and minor version numbers must match when previously the point release number also had to match.

For example, clone functionality now permits cloning 8.4.0 to 8.4.14 and vice-versa.

• **SASL-based LDAP authentication on Windows.** On Microsoft Windows, the server plugin for SASL-based LDAP authentication is now supported. This means that Windows clients can now use GSSAPI/Kerberos for authenticating with the authentication\_ldap\_sasl\_client plugin.

For more information, see SASL-Based LDAP Authentication (Without Proxying).

• **MySQL Replication: SOURCE\_RETRY\_COUNT change.** The default value for the SOURCE\_RETRY\_COUNT option of the CHANGE REPLICATION SOURCE TO statement was changed to 10. This means that, using the default values for this option and for SOURCE\_CONNECT\_RETRY (60), the replica waits 60 seconds between reconnection attempts, and keeps attempting to reconnect at this rate for 10 minutes before timing out and failing over.

This change also applies to the default value of the deprecated --master-retry-count server option. (You should use SOURCE\_RETRY\_COUNT, instead.)

For more information, see Section 19.4.9.1, "Asynchronous Connection Failover for Sources".

• **MySQL Replication: tagged GTIDs.** The format of global transaction identifiers (GIDs) used in MySQL Replication and Group Replication has been extended to enable identification of groups of transactions, making it possible to assign a unique name to the GTIDs which belong to a specific group of transactions. For example, transactions containing data operations can easily be distinguished from those arising from administrative operations simply by comparing their GTIDs.

The new GTID format is UUID:TAG:NUMBER, where TAG is a string of up to 8 characters, which is enabled by setting the value of the gtid\_next system variable to AUTOMATIC:TAG, added in this release (see the description of the variable for tag format and other information). This tag persists for all transactions originating in the current session (unless changed using SET gtid\_next), and is applied at commit time for such transactions, or, when using Group Replication, at certification time. It is also possible to set gtid\_next to UUID:TAG:NUMBER to set the UUID of a single transaction to an arbitrary value, along with assigning it a custom tag. The assignments of UUID and NUMBER are otherwise unchanged from previous MySQL releases. In either case, the user is responsible for making sure that the tag is unique to a given replication topology.

The original UUID:NUMBER format for GTIDs continues to be supported unchanged, as implemented in previous versions of MySQL; changes to existing replication setups using GTIDs are not required.

Setting gtid\_next to AUTOMATIC:TAG or UUID:TAG:NUMBER requires a new TRANSACTION\_GTID\_TAG privilege which is added in this release; this is true both on the originating server as well as for the PRIVILEGE\_CHECKS\_APPLIER for the replica applier thread. This also means that an administrator can now restrict the use of SET @gtid\_next=AUTOMATIC:TAG or UUID:TAG:NUMBER to a desired set of MySQL users or roles so that that only those users related to a given data or operational domain can commit new transactions with assigned tags.

![](_page_42_Picture_5.jpeg)

### **Note**

When upgrading from a previous version of MySQL to MySQL 8.4, any user accounts or roles which already have the BINLOG\_ADMIN privilege are automatically granted the TRANSACTION\_GTID\_TAG privilege.

The built-in functions GTID\_SUBSET(), GTID\_SUBTRACT(), and WAIT\_FOR\_EXECUTED\_GTID\_SET() are compatible with tagged GTIDs.

For more information, see the descriptions of the gtid\_next system variable and the TRANSACTION\_GTID\_TAG privilege, as well as Section 19.1.4, "Changing GTID Mode on Online Servers".

• **Replication: SQL\_AFTER\_GTIDS and MTA.** The START REPLICA statement option SQL\_AFTER\_GTIDS is now compatible with the multi-threaded applier. (Previously, when MTA was enabled and the user attempted to use this option, the statement raised the warning [ER\\_MTA\\_FEATURE\\_IS\\_NOT\\_SUPPORTED](https://dev.mysql.com/doc/mysql-errors/8.4/en/server-error-reference.md#error_er_mta_feature_is_not_supported), and the replica was switched to single-threaded mode.) This means that a replica which needs to catch up with missing transactions can now do so without losing the performance advantage from multithreading.

For more information, see Section 15.4.2.4, "START REPLICA Statement", as well as the documentation for the replica\_parallel\_workers system variable. See also Section 19.2.3.2, "Monitoring Replication Applier Worker Threads", and Section 25.7.11, "NDB Cluster Replication Using the Multithreaded Applier".

- **Replication terminology backwards compatibility.** This release adds the --output-asversion option for mysqldump. This option allows you to create a dump from a MySQL 8.2 or newer server that is compatible with older versions of MySQL; its value, one of those listed here, determines the compatibility of replication terminology used in the dump:
  - SERVER: Gets the version of the server and uses the latest versions of replication statements and variable names compatible with that MySQL version.

- BEFORE\_8\_2\_0: Output is compatible with MySQL servers running versions 8.0.23 through 8.1.0, inclusive.
- BEFORE\_8\_0\_23: Output is compatible with MySQL servers running versions prior to 8.0.23.

See the description of this option for more information.

In addition a new value is added to those already allowed for the terminology\_use\_previous system variable. BEFORE\_8\_2\_0 causes the server to print DISABLE ON SLAVE (now deprecated) instead of DISABLE ON REPLICA in the output of SHOW CREATE EVENT. The existing value BEFORE\_8\_0\_26 now also has this effect in addition to those it already had previously.

- The MySQL version number used in version-specific comments supports a major version consisting of one or two digits; this means that the entire version can be either five or six digits long. For more information about how this change affects handling of versioned comments in MySQL, see Section 11.7, "Comments".
- **group\_replication\_set\_as\_primary() and DDL statements.** The group\_replication\_set\_as\_primary() function waits for ongoing DDL statements such as ALTER TABLE when waiting for all transactions to complete, prior to electing a new primary.

For more information, see the description of this function.

• **DDL and DCL statement tracking for group\_replication\_set\_as\_primary().** 

group\_replication\_set\_as\_primary() now waits for the following statements to complete before a new primary is elected:

- ALTER DATABASE
- ALTER FUNCTION
- ALTER INSTANCE
- ALTER PROCEDURE
- ALTER SERVER
- ALTER TABLESPACE
- ALTER USER
- ALTER VIEW
- CREATE DATABASE
- CREATE FUNCTION
- CREATE PROCEDURE
- CREATE ROLE
- CREATE SERVER
- CREATE SPATIAL REFERENCE SYSTEM
- CREATE TABLESPACE
- CREATE TRIGGER
- CREATE USER
- CREATE VIEW
- DROP DATABASE
- DROP FUNCTION
- DROP PROCEDURE
- DROP ROLE
- DROP SERVER
- DROP SPATIAL REFERENCE SYSTEM
- DROP TABLESPACE
- DROP TRIGGER
- DROP USER
- DROP VIEW
- GRANT
- RENAME TABLE

### • REVOKE

These are in addition to those statements added in MySQL 8.1 or otherwise already supported in this regard. For more information, including a listing of all such statements supported in MySQL 8.3, see the description of the group\_replication\_set\_as\_primary() function.

• **Group Replication version compatibility.** Version compatibility for servers within groups has been extended as follows:

In-place downgrades of servers within groups are supported within the MySQL 8.4 LTS series. For example, a member of a group running MySQL 8.4.2 can be downgraded to MySQL 8.4.0.

Similarly, cross-version group membership is also supported within the 8.4 release series. For example, a server running MySQL 8.4.0 can join a group all of whose members currently run MySQL 8.4.2, as can a server running MySQL 8.4.3.

- **Group Replication variable defaults.** The default values of two server system variables relating to Group Replication have been changed in MySQL 8.4:
  - The default value of the group\_replication\_consistency system variable was changed to BEFORE\_ON\_PRIMARY\_FAILOVER in MySQL 8.4.0. (Previously, it was EVENTUAL.)
  - The default value of the group\_replication\_exit\_state\_action system variable was changed to OFFLINE\_MODE in MySQL 8.4.0. (Previously, it was READ\_ONLY.)

For more information, see Section 20.5.3.2, "Configuring Transaction Consistency Guarantees", and Section 20.7.7, "Responses to Failure Detection and Network Partitioning", as well as the descriptions of the variables listed.

• Added a number of status variables specific to the Group Replication plugin that improve diagnosis and troubleshooting of network instabilities, providing statistics about network usage, control messages, and data messages for each group member.

See Section 20.9.2, "Group Replication Status Variables", for more information.

As part of this work, a new MEMBER\_FAILURE\_SUSPICIONS\_COUNT column was added to the Performance Schema replication\_group\_communication\_information table. The contents of this column are formatted as a JSON array whose keys are group members ID and whose values are the number of times the group member has been considered suspect. See the description of this table for more information.

• **FLUSH\_PRIVILEGES privilege.** A new privilege is added in MySQL 8.4.0 specifically to allow use of FLUSH PRIVILEGES statements. Unlike the RELOAD privilege, the FLUSH\_PRIVILEGES privilege applies only to FLUSH PRIVILEGES statements.

In MySQL 8.4, the RELOAD privilege continues to be supported in this capacity to provide backwards compatibility.

When upgrading, a check is performed to see whether there are any users having the FLUSH\_PRIVILEGES privilege; if there are none, any users having the RELOAD privilege are automatically assigned the new privilege as well.

If you downgrade from MySQL 8.4 (or later) to a version of MySQL which does not support the FLUSH\_PRIVILEGES privilege, a user previously granted this privilege is unable to execute FLUSH PRIVILEGES statements unless the user has the RELOAD privilege.

• **OPTIMIZE\_LOCAL\_TABLE privilege.** MySQL 8.4.0 adds a new OPTIMIZE\_LOCAL\_TABLE privilege. Users must have this privilege to execute OPTIMIZE LOCAL TABLE and OPTIMIZE NO\_WRITE\_TO\_BINLOG TABLE statements.

When upgrading from a previous release series, users having the SYSTEM\_USER privilege are automatically granted the OPTIMIZE\_LOCAL\_TABLE privilege.

- **MySQL Enterprise Data Masking and De-Identification.** Data-masking components added support for specifying a dedicated schema to store the related internal table and masking functions. Previously, the mysql system schema provided the only storage option. The new component\_masking.masking\_database read-only variable enables setting and persisting an alternative schema name at server startup.
- **Flushing of data masking dictionaries.** The MySQL Enterprise Data Masking and De-Identification component now includes the ability to flush the data on the secondary or replica into memory. This can be done in either of the ways described here:
  - A flush can be performed by the user at any time using the masking\_dictionaries\_flush() function added in this release.
  - The component can be configured to flush the memory periodically, leveraging the Scheduler component, by setting the new component\_masking.dictionaries\_flush\_interval\_seconds system variable to an appropriate value.

For more information, see Section 8.5, "MySQL Enterprise Data Masking and De-Identification", and the descriptions of these items.

• **Automatic histogram updates.** MySQL 8.4.0 adds support for automatic updates of histograms. When this feature is enabled for a given histogram, it is updated whenever ANALYZE TABLE is run on the table to which it belongs. In addition, automatic recalculation of persistent statistics by InnoDB (see Section 17.8.10.1, "Configuring Persistent Optimizer Statistics Parameters") also updates the histogram. Histogram updates continue to use the same number of buckets as they were originally specified with, if any.

You can enable this feature when specifying the histogram by including the AUTO UPDATE option for the ANALYZE TABLE statement. To disable it, include MANUAL UPDATE instead. MANUAL UPDATE (no automatic updates) is the default if neither option is specified.

For more information, see Histogram Statistics Analysis.

- Added the tls-certificates-enforced-validation system variable, which permits a DBA to enforce certificate validation at server startup or when using the ALTER INSTANCE RELOAD TLS statement to reload certificates at runtime. With enforcement enabled, discovering an invalid certificate halts server invocation at startup, prevents loading invalid certificates at runtime, and emits warnings. For more information, see Configuring Certificate Validation Enforcement.
- Added server system variables to control the amount of time MySQL accounts that connect to a MySQL server using LDAP pluggable authentication must wait when the LDAP server is down or unresponsive. The default timeout became 30 seconds for the following simple and SASL-based LDAP authentication variables:
  - authentication\_ldap\_simple\_connect\_timeout
  - authentication\_ldap\_simple\_response\_timeout
  - authentication\_ldap\_sasl\_connect\_timeout

• authentication\_ldap\_sasl\_response\_timeout

Connection and response timeouts are configurable through the system variables on Linux platforms only. For more information, see Setting Timeouts for LDAP Pluggable Authentication.

• Logging of the shutdown process was enhanced, with the addition of startup and shutdown messages for the MySQL server, plugins, and components. Such messages are now also logged for closing connections. These additions should facilitate troubleshooting and debugging problems, particularly in the event that the server takes an excessively long time to shut down.

For more information, see Section 7.4.2, "The Error Log".

- **Additions to server startup and shutdown messages.** Added the following types of messages to the server startup and shutdown processes as noted in this list:
  - Start and end messages for server initialization when the server is started with --initialize or --initialize-insecure; these are in addition to and distinct from those shown during normal server startup and shutdown.
  - Start and end messages for InnoDB initialization.
  - Start and end messages for init file execution during server initialization.
  - Start and end messages for for execution of compiled-in statements during server initialization.
  - Start and end mesages for crash recovery during server startup (if crash recovery occurs).
  - Start and end messages for initialization of dynamic plugins during server startup.
  - Start and end messages for compoenents initialization step (apparent during server startup).
  - Messages for shutdown of replica threads, as well as graceful and forceful shutdown of connection threads, during server shutdown.
  - Start and end messages for shutdown of plugins and components during server shutdown.
  - Exit code (return value) information with shutdown messages during initialization or server shutdown and end)

In addition, if the server was built using WITH\_SYSTEMD, the server now includes every systemd message in the error log.

- Added the SHOW PARSE\_TREE statement, which shows the JSON-formatted parse tree for a SELECT statement. This statement is intended for testing and development use only, and not in production. It is available only in debug builds, or if MySQL was built from source using the CMake - DWITH\_SHOW\_PARSE\_TREE option, and is not included or supported in release builds.
- **Thread pool plugin connection information.** Added thread pool connection information to the MySQL Performance Schema, as follows:
  - Added a tp\_connections table, with information about each thread pool connection.
  - Added the following columns to the tp\_thread\_state table: TIME\_OF\_ATTACH, MARKED\_STALLED, STATE, EVENT\_COUNT, ACCUMULATED\_EVENT\_TIME, EXEC\_COUNT, and ACCUMULATED\_EXEC\_TIME
  - Added the following columns to the tp\_thread\_group\_state table: EFFECTIVE\_MAX\_TRANSACTIONS\_LIMIT, NUM\_QUERY\_THREADS, TIME\_OF\_LAST\_THREAD\_CREATION, NUM\_CONNECT\_HANDLER\_THREAD\_IN\_SLEEP, THREADS\_BOUND\_TO\_TRANSACTION, QUERY\_THREADS\_COUNT, and TIME\_OF\_EARLIEST\_CON\_EXPIRE.

For more information, see Section 7.6.3, "MySQL Enterprise Thread Pool", and Section 29.12.16, "Performance Schema Thread Pool Tables".

- **Information Schema PROCESSLIST table usage.** Although the INFORMATION\_SCHEMA.PROCESSLIST table was deprecated in MySQL 8.0.35 and 8.2.0, interest remains in tracking its usage. This release adds two system status variables providing information about accesses to the PROCESSLIST table, listed here:
  - Deprecated\_use\_i\_s\_processlist\_count provides a count of the number of references to the PROCESSLIST table in queries since the server was last started.
  - Deprecated\_use\_i\_s\_processlist\_last\_timestamp stores the time the PROCESSLIST table was last accessed. This is a timestamp value (number of microseconds since the Unix Epoch).
- **Hash table optimization for set operations.** MySQL 8.2 improves performance of statements using the set operations EXCEPT and INTERSECT by means of a new hash table optimization which is enabled automatically for such statements, and controlled by setting the hash\_set\_operations optimizer switch; to disable this optimization and cause the optimizer to used the old temporary table optimization from previous versions of MySQL, set this flag to off.

The amount of memory allocated for this optimization can be controlled by setting the value of the set\_operations\_buffer\_size server system variable; increasing the buffer size can further improve execution times of some statements using these operations.

See Section 10.9.2, "Switchable Optimizations", for more information.

- **WITH\_LD CMake option.** WITH\_LD: Define whether to use the llvm lld or mold linker, otherwise use the standard linker. WITH\_LD also replaces the [USE\\_LD\\_LLD](https://dev.mysql.com/doc/refman/8.0/en/source-configuration-options.md#option_cmake_use_ld_lld) CMake option that was removed in MySQL 8.3.0.
- **MySQL Enterprise Firewall enhancements.** A number of enhancements were made since MySQL 8.0 to MySQL Enterprise Firewall. These are listed here:
  - Stored procedures provided by MySQL Enterprise Firewall now behave in transactional fashion. When an error occurs during execution of a firewall stored procedure, an error is reported, and all changes made by the stored procedure up to that point in time are rolled back.
  - Firewall stored procedures now avoid performing unnecessary combinations of DELETE plus INSERT statements, as well as those of INSERT IGNORE plus UPDATE operations, thus consuming less time and fewer resources, making them faster and more efficient.
  - User-based stored procedures and UDFs, deprecated in MySQL 8.0.26, now raise a deprecation warning. Specifically calling either of sp\_set\_firewall\_mode() or sp\_reload\_firewall\_rules() generates such a warning. See Firewall Account Profile Stored Procedures, as well as Migrating Account Profiles to Group Profiles, for more information.
  - MySQL Enterprise Firewall now permits its memory cache to be reloaded periodically with data stored in the firewall tables. The mysql\_firewall\_reload\_interval\_seconds system variable sets the periodic-reload schedule to use at runtime or it disables reloads by default. Previous implementations reloaded the cache only at server startup or when the server-side plugin was reinstalled.
  - Added the mysql\_firewall\_database server system variable to enable storing internal tables, functions, and stored procedures in a custom schema.
  - Added the uninstall\_firewall.sql script to simplify removing an installed firewall.

For more information about firewall stored procedures, see MySQL Enterprise Firewall Stored Procedures.

- **Pluggable authentication.** Added support for authentication to MySQL Server using devices such as smart cards, security keys, and biometric readers in a WebAuthn context. The new WebAuthn authentication method is based on the FIDO and FIDO2 standards. It uses a pair of plugins, authentication\_webauthn on the server side and authentication\_webauthn\_client on the client side. The server-side WebAuthn authentication plugin is included only in MySQL Enterprise Edition distributions.
- **Keyring migration.** Migration from a keyring component to a keyring plugin is supported. To perform such a migration, use the --keyring-migration-from-component server option introduced in MySQL 8.4.0, setting --keyring-migration-source to the name of the source component, and --keyring-migration-destination the name of the target plugin.

See Key Migration Using a Migration Server, for more information.

- **MySQL Enterprise Audit.** Added the audit\_log\_filter\_uninstall.sql script to simplify removing MySQL Enterprise Audit.
- **New Keywords.** Keywords added in MySQL 8.4 since MySQL 8.0. Reserved keywords are marked with (R).

AUTO, BERNOULLI, GTIDS, LOG, MANUAL (R), PARALLEL (R), PARSE\_TREE, QUALIFY (R), S3, and TABLESAMPLE (R).

• **Preemptive group replication certification garbage collection.** A system variable added in MySQL 8.4.0 group\_replication\_preemptive\_garbage\_collection enables preemptive garbage collection for group replication running in single-primary mode, keeping only the write sets for those transactions that have not yet been committed. This can save time and memory consumption. An additional system variable group\_replication\_preemptive\_garbage\_collection\_rows\_threshold (also introduced in MySQL 8.4.0) sets a lower limit on the number of certification rows needed to trigger preemptive garbage collection if it is enabled; the default is 100000.

In multi-primary mode, each write set in the certification information is required from the moment a transaction is certified until it is committed on all members, which makes it necessary to detect conflicts between transactions. In single-primary mode, where we need be concerned only about transaction dependencies, this is not an issue; this means write sets need be kept only until certification is complete.

It is not possible to change the group replication mode between single-primary and multi-primary when group\_replication\_preemptive\_garbage\_collection is enabled.

See Section 20.7.9, "Monitoring Group Replication Memory Usage with Performance Schema Memory Instrumentation", for help with obtaining information about memory consumed by this process.

- **Sanitized relay log recovery.** In MySQL 8.4.0 and later, it is possible to recover the relay log with any incomplete transactions removed. The relay log is now sanitized when the server is started with --relay-log-recovery=OFF (the default), meaning that all of the following items are removed:
  - Transactions which remain uncompleted at the end of the relay log
  - Relay log files containing incomplete transactions or parts thereof only
  - References in the relay log index file to relay log files which have thus been removed

For more information, see the description of the relay\_log\_recovery server system variable.

• **MySQL upgrade history file.** As part of the installation process in MySQL 8.4.0 and later, a file in JSON format named mysql\_upgrade\_history is created in the server's data directory, or updated if it already exists. This file includes information about the MySQL server version installed, when it was installed, and whether the release was part of an LTS series or an Innovation series.

A typical mysql\_upgrade\_history file might look something like this (formatting adjusted for readability):

```
{
 "file_format":"1",
 "upgrade_history":
 [
 {
 "date":"2024-03-15 22:02:35",
 "version":"8.4.0",
 "maturity":"LTS",
 "initialize":true
 },
 {
 "date":"2024-05-17 17:46:12",
 "version":"8.4.1",
 "maturity":"LTS",
 "initialize":false
 }
 ]
}
```

In addition, the installation process now checks for the presence of a mysql\_upgrade\_info file (deprecated in MySQL 8.0, and is no longer used). If found, the file is removed.

• **mysql client --system-command option.** The --system-command option for the mysql client, available in MySQL 8.4.3 and later, enables or disables the system command.

This option is enabled by default. To disable it, use --system-command=OFF or --skip-systemcommand, which causes the system command to be rejected with an error.

• **mysql client --commands option.** The mysql client --commands option, introduced in MySQL 8.4.6, enables or disables most mysql client commands.

This option is enabled by default. To disable it, start the mysql client with --commands=OFF or - skip-commands.

For more information, see Section 6.5.1.1, "mysql Client Options".

• **Scalar correlated subqueries to derived tables.** MySQL 8.4.0 lifts a previous restriction on transforming a correlated scalar subquery to a derived table such that an operand of the equality expression which did not contain an outer reference could be a simple column reference only.

This means that inner columns can be contained in deterministic expressions, as shown here:

```
func1(.., funcN(.., inner-column-a, ..), inner-column-b) = outside-expression
inner-column-a + inner-column-b = outside-expression
```

For example, the following query is now supported for optimization:

```
SELECT * FROM t1 
 WHERE ( SELECT func(t2.a) FROM t2 
 WHERE func(t2.a) = t1.a ) > 0;
```

The inner operand cannot contain outer column references; likewise, the outer operand cannot contain inner column references. In addition, the inner operand cannot contain a subquery.

If the transformed subquery has explicit grouping, functional dependency analysis may be excessively pessimistic, resulting in an error such as ERROR 1055 (42000): Expression #2 of SELECT list is not in GROUP BY clause and contains nonaggregated column .... For the InnoDB storage engine, the transform is disabled by default (that is, the subquery\_to\_derived flag of the optimizer\_switch variable is not enabled); in this case, such queries pass without raising any errors, but are also not transformed.

See Section 15.2.15.7, "Correlated Subqueries", for more information.

# <span id="page-51-0"></span>**Features Deprecated in MySQL 8.4**

The following features are deprecated in MySQL 8.4 and may be removed in a future series. Where alternatives are shown, applications should be updated to use them.

For applications that use features deprecated in MySQL 8.4 that have been removed in a later MySQL version, statements may fail when replicated from a MySQL 8.4 source to a replica running a later version, or may have different effects on source and replica. To avoid such problems, applications that use features deprecated in 8.4 should be revised to avoid them and use alternatives when possible.

• **group\_replication\_allow\_local\_lower\_version\_join system variable.** The group\_replication\_allow\_local\_lower\_version\_join system variable is deprecated, and setting it causes a warning ([ER\\_WARN\\_DEPRECATED\\_SYNTAX\\_NO\\_REPLACEMENT](https://dev.mysql.com/doc/mysql-errors/8.4/en/server-error-reference.md#error_er_warn_deprecated_syntax_no_replacement)) to be logged.

You should expect this variable to be removed in a future version of MySQL. Since the functionality enabled by setting group\_replication\_allow\_local\_lower\_version\_join is no longer useful, no replacement for it is planned.

• **Group Replication recovery metadata.** Group Replication recovery no longer depends on writing of view change events to the binary log to mark changes in group membership; instead, when all members of a group are MySQL version 8.3.0 or later, members share compressed recovery metadata, and no such event is logged (or assigned a GTID) when a new member joins the group.

Recovery metadata includes the GCS view ID, GTID\_SET of certified transactions, and certification information, as well as a list of online members.

Since View\_change\_log\_event no longer plays a role in recovery, the group\_replication\_view\_change\_uuid system variable is no longer needed, and so is now deprecated; expect its removal in a future MySQL release. You should be aware that no replacement or alternative for this variable or its functionality is planned, and develop your applications accordingly.

• **WAIT\_UNTIL\_SQL\_THREAD\_AFTER\_GTIDS() function.** The WAIT\_UNTIL\_SQL\_THREAD\_AFTER\_GTIDS() SQL function was deprecated in MySQL 8.0, and is no longer supported as of MySQL 8.2. Attempting to invoke this function now causes a syntax error.

Instead of WAIT\_UNTIL\_SQL\_THREAD\_AFTER\_GTIDS(), it is recommended that you use WAIT\_FOR\_EXECUTED\_GTID\_SET(), which allows you to wait for specific GTIDS. This works regardless of the replication channel or the user client through which the specified transactions arrive on the server.

• **GTID-based replication and IGNORE\_SERVER\_IDS.** When global transaction identifiers (GTIDs) are used for replication, transactions that have already been applied are automatically ignored. This means that IGNORE\_SERVER\_IDS is not compatible with GTID mode. If gtid\_mode is ON, CHANGE REPLICATION SOURCE TO with a non-empty IGNORE\_SERVER\_IDS list is rejected with an error. Likewise, if any existing replication channel was created with a list of server IDs to be ignored, SET gtid\_mode=ON is also rejected. Before starting GTID-based replication, check for and clear any ignored server ID lists on the servers involved; you can do this by checking the output from SHOW REPLICA STATUS. In such cases, you can clear the list by issuing CHANGE REPLICATION SOURCE TO with an empty list of server IDs, as shown here:

CHANGE REPLICATION SOURCE TO IGNORE\_SERVER\_IDS = ();

See Section 19.1.3.7, "Restrictions on Replication with GTIDs", for more information.

• **Binary log transaction dependency tracking and logging format.** Using writeset information for conflict detection has been found to cause issues with dependency tracking; for this reason, we now limit the usage of writesets for conflict checks to when row-based logging is in effect.

This means that, in such cases, binlog\_format must be ROW, and MIXED is no longer supported.

• **expire\_logs\_days system variable.** The expire\_logs\_days server system variable, deprecated in MySQL 8.0, has been removed. Attempting to get or set this variable at runtime, or to start mysqld with the equivalent option (--expire-logs-days), now results in an error.

In place of expire\_logs\_days, use binlog\_expire\_logs\_seconds, which allows you to specify expiration periods other than (only) in an integral number of days.

• **Wildcard characters in database grants.** The use of the characters % and \_ as wildcards in database grants was deprecated in MySQL 8.2.0. You should expect for the wildcard functionality to removed in a future MySQL release and for these characters always to be treated as literals, as they are already whenever the value of the partial\_revokes server system variable is ON.

In addition, the treatment of % by the server as a synonym for localhost when checking privileges is now also deprecated as of MySQL 8.2.0 and thus subject to removal in a future version of MySQL.

- **--character-set-client-handshake option.** The [--character-set-client-handshake](https://dev.mysql.com/doc/refman/8.0/en/server-options.md#option_mysqld_character-set-client-handshake) server option, originally intended for use with upgrades from very old versions of MySQL, is now deprecated and a warning is issued whenever it is used. You should expect this option to be removed in a future version of MySQL; applications depending on this option should begin migration away from it as soon as possible.
- **Nonstandard foreign keys.** The use of non-unique or partial keys as foreign keys is nonstandard, and is deprecated in MySQL. Beginning with MySQL 8.4.0, you must explicitly enable such keys by setting restrict\_fk\_on\_non\_standard\_key to OFF, or by starting the server with --skip-restrict-fk-on-non-standard-key.

restrict\_fk\_on\_non\_standard\_key is ON by default, which means that trying to use a nonstandard key as a foreign key in a CREATE TABLE or other SQL statement is rejected with [ER\\_WARN\\_DEPRECATED\\_NON\\_STANDARD\\_KEY](https://dev.mysql.com/doc/mysql-errors/8.4/en/server-error-reference.md#error_er_warn_deprecated_non_standard_key). Setting it to ON allows such statements to run, but they raise the same error as a warning.

Upgrades from MySQL 8.0 are supported even if there are tables containing foreign keys referring to non-unique or partial keys. In such cases, the server writes a list of warning messages containing the names of any foreign keys which refer to nonstandard keys.

# <span id="page-52-0"></span>**Features Removed in MySQL 8.4**

The following items are obsolete and have been removed in MySQL 8.4. Where alternatives are shown, applications should be updated to use them.

For MySQL 8.3 applications that use features removed in MySQL 8.4, statements may fail when replicated from a MySQL 8.3 source to a MySQL 8.4 replica, or may have different effects on source and replica. To avoid such problems, applications that use features removed in MySQL 8.4 should be revised to avoid them and use alternatives when possible.

- **Server options and variables removed.** A number of server options and variables supported in previous versions of MySQL have been removed in MySQL 8.4. Attempting to set any of them in MySQL 8.4 raises an error. These options and variables are listed here:
  - binlog\_transaction\_dependency\_tracking: Deprecated in MySQL 8.0.35 and MySQL 8.2.0. There are no plans to replace this variable or its functionality, which has been made internal to the server. In MySQL 8.4 (and later), when multithreaded replicas are in use, the source mysqld uses always writesets to generate dependency information for the binary log; this has the same effect as setting binlog\_transaction\_dependency\_tracking to WRITESET in previous versions of MySQL.

- group\_replication\_recovery\_complete\_at: Deprecated in MySQL 8.0.34. In MySQL 8.4 and later, the policy applied during the distributed recovery process is always to mark a new member online only after it has received, certified, and applied all transactions that took place before it joined the group; this is equivalent to setting group\_replication\_recovery\_complete\_at to TRANSACTIONS\_APPLIED in previous versions of MySQL.
- avoid\_temporal\_upgrade and show\_old\_temporals: Both of these variables were deprecated in MySQL 5.6; neither of them had any effect in recent versions of MySQL. Both variables have been removed; there are no plans to replace either of them.
- --no-dd-upgrade: Deprecated in MySQL 8.0.16, now removed. Use --upgrade=NONE instead.
- --old and --new: Both deprecated in MySQL 8.0.35 and MySQL 8.2.0, and now removed.
- --language: Deprecated in MySQL 5.5, and now removed.
- The --ssl and --admin-ssl server options, as well as the have\_ssl and have\_openssl server system variables, were deprecated in MySQL 8.0.26. They are all removed in this release. Use --tls-version and --admin-tls-version instead.
- The default\_authentication\_plugin system variable, deprecated in MySQL 8.0.27, is removed as of MySQL 8.4.0. Use authentication\_policy instead.

As part of the removal of default\_authentication\_plugin, the syntax for authentication\_policy has been changed. See the description of authentication\_policy for more information.

- **--skip-host-cache server option.** This option has been removed; start the server with host-cache-size=0 instead. See Section 7.1.12.3, "DNS Lookups and the Host Cache".
- **--innodb and --skip-innodb server options.** These options have been removed. The InnoDB storage engine is always enabled, and it is not possible to disable it.
- **--character-set-client-handshake and --old-style-user-limits server options.** These options were formerly used for compatibility with very old versions of MySQL which are no longer supported or maintained, and thus no longer serve any useful purpose.
- **FLUSH HOSTS statement.** The FLUSH HOSTS statement, deprecated in MySQL 8.0.23, has been removed. To clear the host cache, issue TRUNCATE TABLE performance\_schema.host\_cache or mysqladmin flush-hosts.
- **Obsolete replication options and variables.** A number of options and variables relating to MySQL Replication were deprecated in previous versions of MySQL, and have been removed from MySQL 8.4. Attempting to use any of these now causes the server to raise a syntax error. These options and variables are listed here:
  - --slave-rows-search-algorithms: The algorithm used by the replication applier to look up table rows when applying updates or deletes is now always HASH\_SCAN,INDEX\_SCAN, and is no longer configurable by the user.
  - log\_bin\_use\_v1\_events: This allowed source servers running MySQL 5.7 and newer to replicate to earlier versions of MySQL which are no longer supported or maintained.
  - --relay-log-info-file, --relay-log-info-repository, --master-info-file, --master-info-repository: The use of files for the applier metadata repository and the connection metadata repository has been superseded by crash-safe tables, and is no longer supported. See Section 19.2.4.2, "Replication Metadata Repositories".

- transaction\_write\_set\_extraction
- group\_replication\_ip\_whitelist: Use group\_replication\_ip\_allowlist instead.
- group\_replication\_primary\_member: No longer needed; check the MEMBER\_ROLE column of the Performance Schema replication\_group\_members table instead.
- **Replication SQL syntax.** A number of SQL statements used in MySQL Replication which were deprecated in earlier versions of MySQL are no longer supported in MySQL 8.4. Attempting to use any of these statements now produces a syntax error. These statements can be divided into two groups those relating to source servers, and those referring to replicas, as shown here:

As part of this work, the DISABLE ON SLAVE option for CREATE EVENT and ALTER EVENT is now deprecated, and is superseded by DISABLE ON REPLICA. The corresponding term

SLAVESIDE\_DISABLED is also now deprecated,and no longer used in event descriptions such as in the Information Schema EVENTS table; REPLICA\_SIDE\_DISABLED is now shown instead.

- Statements which have been removed, which relate to replication source servers, are listed here:
  - CHANGE MASTER TO: Use CHANGE REPLICATION SOURCE TO.
  - RESET MASTER: Use RESET BINARY LOGS AND GTIDS.
  - SHOW MASTER STATUS: Use SHOW BINARY LOG STATUS.
  - PURGE MASTER LOGS: Use PURGE BINARY LOGS.
  - SHOW MASTER LOGS: Use SHOW BINARY LOGS.
- Removed SQL statements relating to replicas are listed here:
  - START SLAVE: Use START REPLICA.
  - STOP SLAVE: Use STOP REPLICA.
  - SHOW SLAVE STATUS: Use SHOW REPLICA STATUS.
  - SHOW SLAVE HOSTS: Use SHOW REPLICAS.
  - RESET SLAVE: Use RESET REPLICA.

All of the statements listed previously were removed from MySQL test programs and files, as well as from any other internal use.

In addition, a number of deprecated options formerly supported by CHANGE REPLICATION SOURCE TO and START REPLICA have been removed and are no longer accepted by the server. The removed options for each of these SQL statements are listed next.

- Options removed from CHANGE REPLICATION SOURCE TO are listed here:
  - MASTER\_AUTO\_POSITION: Use SOURCE\_AUTO\_POSITION.
  - MASTER\_HOST: Use SOURCE\_HOST.
  - MASTER\_BIND: Use SOURCE\_BIND.
  - MASTER\_UseR: Use SOURCE\_UseR.
  - MASTER\_PASSWORD: Use SOURCE\_PASSWORD.
  - MASTER\_PORT: Use SOURCE\_PORT.
  - MASTER\_CONNECT\_RETRY: Use SOURCE\_CONNECT\_RETRY.
  - MASTER\_RETRY\_COUNT: Use SOURCE\_RETRY\_COUNT.
  - MASTER\_DELAY: Use SOURCE\_DELAY.
  - MASTER\_SSL: Use SOURCE\_SSL.
  - MASTER\_SSL\_CA: Use SOURCE\_SSL\_CA.
  - MASTER\_SSL\_CAPATH: Use SOURCE\_SSL\_CAPATH.
  - MASTER\_SSL\_CIPHER: Use SOURCE\_SSL\_CIPHER.

- MASTER\_SSL\_CRL: Use SOURCE\_SSL\_CRL.
- MASTER\_SSL\_CRLPATH: Use SOURCE\_SSL\_CRLPATH.
- MASTER\_SSL\_KEY: Use SOURCE\_SSL\_KEY.
- MASTER\_SSL\_VERIFY\_SERVER\_CERT: Use SOURCE\_SSL\_VERIFY\_SERVER\_CERT.
- MASTER\_TLS\_VERSION: Use SOURCE\_TLS\_VERSION.
- MASTER\_TLS\_CIPHERSUITES: Use SOURCE\_TLS\_CIPHERSUITES.
- MASTER\_SSL\_CERT: Use SOURCE\_SSL\_CERT.
- MASTER\_PUBLIC\_KEY\_PATH: Use SOURCE\_PUBLIC\_KEY\_PATH.
- GET\_MASTER\_PUBLIC\_KEY: Use GET\_SOURCE\_PUBLIC\_KEY.
- MASTER\_HEARTBEAT\_PERIOD: Use SOURCE\_HEARTBEAT\_PERIOD.
- MASTER\_COMPRESSION\_ALGORITHMS: Use SOURCE\_COMPRESSION\_ALGORITHMS.
- MASTER\_ZSTD\_COMPRESSION\_LEVEL: Use SOURCE\_ZSTD\_COMPRESSION\_LEVEL.
- MASTER\_LOG\_FILE: Use SOURCE\_LOG\_FILE.
- MASTER\_LOG\_POS: Use SOURCE\_LOG\_POS.
- Options removed from the START REPLICA statement are listed here:
  - MASTER\_LOG\_FILE: Use SOURCE\_LOG\_FILE.
  - MASTER\_LOG\_POS: Use SOURCE\_LOG\_POS.
- **System variables and NULL.** It is not intended or supported for a MySQL server startup option to be set to NULL (--my-option=NULL) and have it interpreted by the server as SQL NULL, and should not be possible. MySQL 8.1 (and later) specifically disallows setting startup options to NULL in this fashion, and rejects an attempt to do with an error. Attempts to set the corresponding server system variables to NULL using SET or similar in the mysql client are also rejected.

The server system variables in the following list are excepted from the restriction just described:

- admin\_ssl\_ca
- admin\_ssl\_capath
- admin\_ssl\_cert
- admin\_ssl\_cipher
- admin\_tls\_ciphersuites
- admin\_ssl\_key
- admin\_ssl\_crl
- admin\_ssl\_crlpath
- basedir
- character\_sets\_dir

- ft\_stopword\_file
- group\_replication\_recovery\_tls\_ciphersuites
- init\_file
- lc\_messages\_dir
- plugin\_dir
- relay\_log
- [relay\\_log\\_info\\_file](https://dev.mysql.com/doc/refman/8.0/en/replication-options-replica.md#sysvar_relay_log_info_file)
- replica\_load\_tmpdir
- ssl\_ca
- ssl\_capath
- ssl\_cert
- ssl\_cipher
- ssl\_crl
- ssl\_crlpath
- ssl\_key
- socket
- tls\_ciphersuites
- tmpdir

See also Section 7.1.8, "Server System Variables".

• **Identifiers with an initial dollar sign.** The use of the dollar sign (\$) as the initial character of an unquoted identifier was deprecated in MySQL 8.0, and is restricted in MySQL 8.1 and later;

using an unquoted identifier beginning with a dollar sign and containing one or more dollar signs (in addition to the first one) now generates a syntax error.

Unquoted identifiers starting with \$ are not affected by this restriction if they do not contain any additional \$ characters.

See Section 11.2, "Schema Object Names".

Also as part of this work, the following server status variables, previously deprecated, have been removed. They are listed here, along with their replacements:

- Com\_slave\_start: Use Com\_replica\_start.
- Com\_slave\_stop: Use Com\_replica\_stop.
- Com\_show\_slave\_status: Use Com\_show\_replica\_status.
- Com\_show\_slave\_hosts: Use Com\_show\_replicas.
- Com\_show\_master\_status: Use Com\_show\_binary\_log\_status.
- Com\_change\_master: Use Com\_change\_replication\_source.

The variables just listed as removed no longer appear in the output of statements such as SHOW STATUS. See also Com\_xxx Variables.

- **Plugins.** A number of plugins were removed in MySQL 8.4.0, and are listed here, along with any system variables and other features associated with them which were also removed or otherwise affected by the plugin removal:
  - authentication\_fido and authentication\_fido\_client plugins: Use the authentication\_webauthn plugin instead. See Section 8.4.1.11, "WebAuthn Pluggable Authentication".

The authentication\_fido\_rp\_id server system variable, mysql client --fido-registerfactor option, and the -DWITH\_FIDO CMake option were also removed.

• keyring\_file plugin: Use the component\_keyring\_file component instead. See Section 8.4.4.4, "Using the component\_keyring\_file File-Based Keyring Component".

The keyring\_file\_data system variable was also removed. In addition, the CMake options - DINSTALL\_MYSQLKEYRINGDIR and -DWITH\_KEYRING\_TEST were removed.

• keyring\_encrypted\_file plugin: Use the component\_keyring\_encrypted\_file component instead. See Section 8.4.4.5, "Using the component\_keyring\_encrypted\_file Encrypted File-Based Keyring Component".

The keyring\_encrypted\_file\_data and keyring\_encrypted\_file\_password system variables were also removed.

• keyring\_oci plugin: Use the component\_keyring\_oci component instead. See Section 8.4.4.9, "Using the Oracle Cloud Infrastructure Vault Keyring Component".

The following server system variables were also removed: keyring\_oci\_ca\_certificate, keyring\_oci\_compartment, keyring\_oci\_encryption\_endpoint, keyring\_oci\_key\_file, keyring\_oci\_key\_fingerprint, keyring\_oci\_management\_endpoint, keyring\_oci\_master\_key,

keyring\_oci\_secrets\_endpoint, keyring\_oci\_tenancy, keyring\_oci\_user, keyring\_oci\_vaults\_endpoint, and keyring\_oci\_virtual\_vault.

- openssl\_udf plugin: Use the MySQL Enterprise Encryption (component\_enterprise\_encryption) component instead; see Section 8.6, "MySQL Enterprise Encryption".
- **Support for weak ciphers.** When configuring encrypted connections, MySQL 8.4.0 and later no longer allow specifying any cipher that does not meet the following requirements:
  - Conforms to proper TLS version (TLS v1.2 or TLSv1.3, as appropriate)
  - Provides perfect forward secrecy
  - Uses SHA2 in cipher, certificate, or both
  - Uses AES in GCM or any other AEAD algorithms or modes

This has implications for setting the following system variables:

- ssl\_cipher
- admin\_ssl\_cipher
- tls\_ciphersuites
- admin\_tls\_ciphersuites

See the descriptions of these variables for their permitted values in MySQL 8.4, and more information.

![](_page_59_Picture_14.jpeg)

### **Note**

libmysqlclient continues to support additional ciphers that do not satisfy these conditions in order to retain the ability to connect to older versions of MySQL.

• **INFORMATION\_SCHEMA.TABLESPACES.** The INFORMATION\_SCHEMA.TABLESPACES table, which was not actually used, was deprecated in MySQL 8.0.22 and has now been removed.

![](_page_59_Picture_18.jpeg)

# **Note**

For NDB tables, the Information Schema FILES table provides tablespacerelated information.

For InnoDB tables, the Information Schema INNODB\_TABLESPACES and INNODB\_DATAFILES tables provide tablespace metadata.

- **DROP TABLESPACE and ALTER TABLESPACE: ENGINE clause.** The ENGINE clause for DROP TABLESPACE and ALTER TABLESPACE statements was deprecated in MySQL 8.0. In MySQL 8.4, it is no longer supported, and causes an error if you attempt to use it with DROP TABLESPACE or ALTER TABLESPACE ... DROP DATAFILE. ENGINE is also no longer supported for all other variants of ALTER TABLESPACE, with the two exceptions listed here:
  - ALTER TABLESPACE ... ADD DATAFILE ENGINE={NDB|NDBCLUSTER}
  - ALTER UNDO TABLESPACE ... SET {ACTIVE|INACTIVE} ENGINE=INNODB

For more information, see the documentation for these statements.

- **LOW\_PRIORITY with LOCK TABLES ... WRITE.** The LOW\_PRIORITY clause of the LOCK TABLES ... WRITE statement had had no effect since MySQL 5.5, and was deprecated in MySQL 5.6. It is no longer supported in MySQL 8.4; including it in LOCK TABLES now causes a syntax error.
- **EXPLAIN FORMAT=JSON format versioning.** It is now possible to choose between 2 versions of the JSON output format used by EXPLAIN FORMAT=JSON statements using the explain\_json\_format\_version server system variable introduced in this release. Setting this variable to 1 causes the server to use Version 1, which is the linear format which was always used for output from such statements in MySQL 8.2 and earlier. This is the default value and format in MySQL 8.4. Setting explain\_json\_format\_version to 2 causes the Version 2 format to be used; this JSON output format is based on access paths, and is intended to provide better compatibility with future versions of the MySQL Optimizer.

See Obtaining Execution Plan Information, for more information and examples.

• **Capturing EXPLAIN FORMAT=JSON output.** EXPLAIN FORMAT=JSON was extended with an INTO option, which provides the ability to store JSON-formatted EXPLAIN output in a user variable where it can be worked with using MySQL JSON functions, like this:

```
mysql> EXPLAIN FORMAT=JSON INTO @myex SELECT name FROM a WHERE id = 2;
Query OK, 0 rows affected (0.00 sec)
mysql> SELECT JSON_EXTRACT(@myex, "$.query_block.table.key");
+------------------------------------------------+
| JSON_EXTRACT(@myex, "$.query_block.table.key") |
+------------------------------------------------+
| "PRIMARY" |
+------------------------------------------------+
1 row in set (0.01 sec)
```

This option can be used only if the EXPLAIN statement also contains FORMAT=JSON; otherwise, a syntax error results. This requirement is not affected by the value of explain\_format.

INTO can be used with any explainable statement with the exception of EXPLAIN FOR CONNECTION. It cannot be used with EXPLAIN ANALYZE.

For more information and examples, see Obtaining Execution Plan Information.

• **EXPLAIN FOR SCHEMA.** Added a FOR SCHEMA option to the EXPLAIN statement. The syntax is as shown here, where stmt is an explainable statement:

```
EXPLAIN [options] FOR SCHEMA schema_name stmt
```

This causes stmt to be run as if in the named schema.

FOR DATABASE is also supported as a synonym.

This option is not compatible with FOR CONNECTION.

See Obtaining Execution Plan Information, for more information.

• **Client comments preserved.** In MySQL 8.0, the stripping of comments from the mysql client was the default behavior; the default was changed to preserve such comments.

To enable the stripping of comments as was performed in MySQL 8.0 and earlier, start the mysql client with --skip-comments.

• **AUTO\_INCREMENT and floating-point columns.** The use of the AUTO\_INCREMENT modifier with FLOAT and DOUBLE columns in CREATE TABLE and ALTER TABLE statements was

deprecated in MySQL 8.0; support for it is removed altogether in MySQL 8.4, where it raises [ER\\_WRONG\\_FIELD\\_SPEC](https://dev.mysql.com/doc/mysql-errors/8.4/en/server-error-reference.md#error_er_wrong_field_spec) (Incorrect column specifier for column).

Before upgrading to MySQL 8.4 from a previous series, you must fix any table that contains a FLOAT or DOUBLE column with AUTO\_INCREMENT so that the table no longer uses either of these. Otherwise, the upgrade fails .

- **mysql\_ssl\_rsa\_setup utility.** The mysql\_ssl\_rsa\_setup utility, deprecated in MySQL 8.0.34, has been removed. For MySQL distributions compiled using OpenSSL, the MySQL server can perform automatic generation of missing SSL and RSA files at startup. See Section 8.3.3.1, "Creating SSL and RSA Certificates and Keys using MySQL", for more information.
- **MySQL Privileges.** Added the SET\_ANY\_DEFINER privilege for definer object creation and the ALLOW\_NONEXISTENT\_DEFINER privilege for orphan object protection. Together these privileges coexist with the deprecated [SET\\_USER\\_ID](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.md#priv_set-user-id) privilege.
- **SET\_USER\_ID privilege.** The SET\_USER\_ID privilege, deprecated in MySQL 8.2.0, has been removed. use in GRANT statements now causes a syntax error

Instead of SET\_USER\_ID, you can use the SET\_ANY\_DEFINER privilege for definer object creation, and the ALLOW\_NONEXISTENT\_DEFINER privileges for orphan object protection.

Both privileges are required to produce orphaned SQL objects using CREATE PROCEDURE, CREATE FUNCTION, CREATE TRIGGER, CREATE EVENT, or CREATE VIEW.

- **--abort-slave-event-count and --disconnect-slave-event-count server options.** The MySQL server startup options --abort-slave-event-count and --disconnect-slave-eventcount, formerly used in testing, were deprecated in MySQL 8.0, and have been removed in this release. Attempting to start mysqld with either of these options now results in an error.
- **mysql\_upgrade utility.** The mysql\_upgrade utility, deprecated in MySQL 8.0.16, has been removed.
- **mysqlpump utility.** The mysqlpump utility along with its helper utilities lz4\_decompress and zlib\_decompress, deprecated in MySQL 8.0.34, were removed. Instead, use mysqldump or [MySQL Shell's dump utilities](https://dev.mysql.com/doc/mysql-shell/8.4/en/mysql-shell-utilities-dump-instance-schema.md).
- **Obsolete CMake options.** The following options for compiling the server with CMake were obsolete and have been removed:
  - USE\_LD\_LLD: Use WITH\_LD=lld instead.
  - WITH\_BOOST, DOWNLOAD\_BOOST, DOWNLOAD\_BOOST\_TIMEOUT: These options are no longer necessary; MySQL now includes and uses a bundled version of Boost when compiling from source.
- **Removed Keywords.** Keywords removed in MySQL 8.4 since MySQL 8.0. Reserved keywords are marked with (R).

```
GET_MASTER_PUBLIC_KEY, MASTER_AUTO_POSITION, MASTER_BIND (R),
MASTER_COMPRESSION_ALGORITHMS, MASTER_CONNECT_RETRY, MASTER_DELAY,
MASTER_HEARTBEAT_PERIOD, MASTER_HOST, MASTER_LOG_FILE, MASTER_LOG_POS,
MASTER_PASSWORD, MASTER_PORT, MASTER_PUBLIC_KEY_PATH, MASTER_RETRY_COUNT,
MASTER_SSL, MASTER_SSL_CA, MASTER_SSL_CAPATH, MASTER_SSL_CERT,
MASTER_SSL_CIPHER, MASTER_SSL_CRL, MASTER_SSL_CRLPATH, MASTER_SSL_KEY,
MASTER_SSL_VERIFY_SERVER_CERT (R), MASTER_TLS_CIPHERSUITES,
MASTER_TLS_VERSION, MASTER_USER, and MASTER_ZSTD_COMPRESSION_LEVEL.
```

• **Index prefixes in partitioning key.** Columns with index prefixes were allowed in the partitioning key for a partitioned table in MySQL 8.0, and raised a warning with no other effects when creating, altering, or upgrading a partitioned table. Such columns are no longer permitted in partitioned tables, and using any such columns in the partitioning key causes the CREATE TABLE or ALTER TABLE statement in they occur to be rejected with an error.

For more information, see Column index prefixes not supported for key partitioning.

# <span id="page-62-0"></span>**1.5 Server and Status Variables and Options Added, Deprecated, or Removed in MySQL 8.4 since 8.0**

- [Options and Variables Introduced in MySQL 8.4](#page-62-1)
- [Options and Variables Deprecated in MySQL 8.4](#page-66-0)
- [Options and Variables Removed in MySQL 8.4](#page-67-0)

This section lists server variables, status variables, and options that were added for the first time, have been deprecated, or have been removed in MySQL 8.4 since 8.0.

# <span id="page-62-1"></span>**Options and Variables Introduced in MySQL 8.4**

The following system variables, status variables, and server options have been added in MySQL 8.4.

- Audit\_log\_direct\_writes: Number of direct writes to the audit log file. Added in MySQL 8.1.0.
- Com\_show\_binary\_log\_status: Count of SHOW BINARY LOG STATUS statements; use instead of Com\_show\_master\_status. Added in MySQL 8.2.0.
- Deprecated\_use\_i\_s\_processlist\_count: Number of times Information Schema processlist table has been accessed. Added in MySQL 8.3.0.
- Deprecated\_use\_i\_s\_processlist\_last\_timestamp: Time of most recent access to Information Schema processlist table (timestamp). Added in MySQL 8.3.0.
- Gr\_all\_consensus\_proposals\_count: Sum of all proposals that were initiated and terminated in this node. Added in MySQL 8.1.0.
- Gr\_all\_consensus\_time\_sum: The sum of elapsed time of all consensus rounds started and finished in this node. Togheter with count\_all\_consensus\_proposals, we can identify if the individual consensus time has a trend of going up, thus signaling a possible problem. Added in MySQL 8.1.0.
- Gr\_certification\_garbage\_collector\_count: Number of times certification garbage collection did run. Added in MySQL 8.1.0.
- Gr\_certification\_garbage\_collector\_time\_sum: Sum of the time in micro-seconds that certification garbage collection runs took. Added in MySQL 8.1.0.
- Gr\_consensus\_bytes\_received\_sum: The sum of all socket-level bytes that were received to from group nodes having as a destination this node. Added in MySQL 8.1.0.
- Gr\_consensus\_bytes\_sent\_sum: Sum of all socket-level bytes that were sent to all group nodes originating on this node. Socket-level bytes mean that we will report more data here than in the sent messages, because they are multiplexed and sent to each member. As an example, if we have a group with 3 members and we send a 100 bytes message, this value will account for 300 bytes, since we send 100 bytes to each node. Added in MySQL 8.1.0.
- Gr\_control\_messages\_sent\_bytes\_sum: Sum of bytes of control messages sent by this member. The size is the on-the-wire size. Added in MySQL 8.1.0.
- Gr\_control\_messages\_sent\_count: Number of control messages sent by this member. Added in MySQL 8.1.0.
- Gr\_control\_messages\_sent\_roundtrip\_time\_sum: Sum of the roundtrip time in microseconds of control messages sent by this member. The time is measured between the send and the delivery of the message on the sender member. This time will measure the time between the

- send and the delivery of the message on the majority of the members of the group (that includes the sender). Added in MySQL 8.1.0.
- Gr\_data\_messages\_sent\_bytes\_sum: Sum of bytes of data messages sent by this member. The size is the on-the-wire size. Added in MySQL 8.1.0.
- Gr\_data\_messages\_sent\_count: Number of data messages sent by this member. Counts the number of transaction data messages sent. Added in MySQL 8.1.0.
- Gr\_data\_messages\_sent\_roundtrip\_time\_sum: Sum of the roundtrip time in micro-seconds of data messages sent by this member. The time is measured between the send and the delivery of the message on the sender member. This time will measure the time between the send and the delivery of the message on the majority of the members of the group (that includes the sender). Added in MySQL 8.1.0.
- Gr\_empty\_consensus\_proposals\_count: Sum of all empty proposal rounds that were initiated and terminated in this node. Added in MySQL 8.1.0.
- Gr\_extended\_consensus\_count: The number of full 3-Phase PAXOS that this node initiated. If this number grows, it means that at least of the node is having issues answering to Proposals, either by slowliness or network issues. Use togheter with count\_member\_failure\_suspicions to try and do some diagnose. Added in MySQL 8.1.0.
- Gr\_last\_consensus\_end\_timestamp: The time in which our last consensus proposal was approved. Reported in a timestamp format. This is an indicator if the group is halted or making slow progress. Added in MySQL 8.1.0.
- Gr\_total\_messages\_sent\_count: The number of high-level messages that this node sent to the group. These messages are the ones the we receive via the API to be proposed to the group. XCom has a batching mechanism, that will gather these messages and propose them all togheter. This will acocunt the number of message before being batched. Added in MySQL 8.1.0.
- Gr\_transactions\_consistency\_after\_sync\_count: Number of transactions on secondaries that waited to start, while waiting for transactions from the primary with group\_replication\_consistency= AFTER and BEFORE\_AND\_AFTER to be committed. Added in MySQL 8.1.0.
- Gr\_transactions\_consistency\_after\_sync\_time\_sum: Sum of the time in micro-seconds that transactions on secondaries waited to start, while waiting for transactions from the primary with group\_replication\_consistency= AFTER and BEFORE\_AND\_AFTER to be committed. Added in MySQL 8.1.0.
- Gr\_transactions\_consistency\_after\_termination\_count: Number of transactions executed with group\_replication\_consistency= AFTER and BEFORE\_AND\_AFTER. Added in MySQL 8.1.0.
- Gr\_transactions\_consistency\_after\_termination\_time\_sum: Sum of the time in micro-seconds spent between the delivery of the transaction executed with group\_replication\_consistency=AFTER and BEFORE\_AND\_AFTER, and the acknowledge of the other group members that the transaction is prepared. It does not include the transaction send roundtrip time. Added in MySQL 8.1.0.
- Gr\_transactions\_consistency\_before\_begin\_count: Number of transactions executed with group\_replication\_consistency= BEFORE and BEFORE\_AND\_AFTER. Added in MySQL 8.1.0.
- Gr\_transactions\_consistency\_before\_begin\_time\_sum: Sum of the time in microseconds that the member waited until its group\_replication\_applier channel was consumed before execute the transaction with group\_replication\_consistency= BEFORE and BEFORE\_AND\_AFTER. Added in MySQL 8.1.0.
- Performance\_schema\_meter\_lost: Number of meter instruments that failed to be created. Added in MySQL 8.2.0.

- Performance\_schema\_metric\_lost: Number of metric instruments that failed to be created. Added in MySQL 8.2.0.
- Telemetry\_metrics\_supported: Whether server telemetry metrics is supported. Added in MySQL 8.2.0.
- Tls\_sni\_server\_name: Server name supplied by the client. Added in MySQL 8.1.0.
- authentication\_ldap\_sasl\_connect\_timeout: SASL-Based LDAP server connection timeout. Added in MySQL 8.1.0.
- authentication\_ldap\_sasl\_response\_timeout: Simple LDAP server response timeout. Added in MySQL 8.1.0.
- authentication\_ldap\_simple\_connect\_timeout: Simple LDAP server connection timeout. Added in MySQL 8.1.0.
- authentication\_ldap\_simple\_response\_timeout: Simple LDAP server response timeout. Added in MySQL 8.1.0.
- authentication\_webauthn\_rp\_id: Relying party ID for multifactor authentication. Added in MySQL 8.2.0.
- check-table-functions: How to proceed when scanning data dictionary for functions used in table constraints and other expressions, and such a function causes an error. Use WARN to log warnings; ABORT (default) also logs warnings, and halts any upgrade in progress. Added in MySQL 8.4.5.
- component\_masking.dictionaries\_flush\_interval\_seconds: How long for scheduler to wait until attempting to schedule next execution, in seconds. Added in MySQL 8.3.0.
- component\_masking.masking\_database: Database to use for masking dictionaries. Added in MySQL 8.3.0.
- group\_replication\_preemptive\_garbage\_collection: Enable preemptive garbage collection in single-primary mode; no effect in multi-primary mode. Added in MySQL 8.4.0.
- group\_replication\_preemptive\_garbage\_collection\_rows\_threshold: Number of rows of certification information required to trigger preemptive garbage collection in single-primary mode when enabled by group\_replication\_preemptive\_garbage\_collection. Added in MySQL 8.4.0.
- keyring-migration-from-component: Keyring migration is from component to plugin. Added in MySQL 8.4.0.
- mysql-native-password: Enable mysql\_native\_password authentication plugin. Added in MySQL 8.4.0.
- mysql\_firewall\_database: Database from which MySQL Enterprise Firewall plugin sources its tables and stored procedures. Added in MySQL 8.2.0.
- mysql\_firewall\_reload\_interval\_seconds: Reload MySQL Enterprise Firewall plugin data at specified intervals. Added in MySQL 8.2.0.
- performance\_schema\_max\_meter\_classes: Maximum number of meter instruments which can be created. Added in MySQL 8.2.0.
- performance\_schema\_max\_metric\_classes: Maximum number of metric instruments which can be created. Added in MySQL 8.2.0.
- restrict\_fk\_on\_non\_standard\_key: Disallow creation of foreign keys on non-unique or partial keys. Added in MySQL 8.4.0.
- set\_operations\_buffer\_size: Amount of memory available for hashing of set operations. Added in MySQL 8.2.0.

- telemetry.live\_sessions: Displays the current number of sessions instrumented with telemetry. Added in MySQL 8.1.0.
- telemetry.metrics\_enabled: Controls whether telemetry metrics are collected or not. Added in MySQL 8.3.0.
- telemetry.metrics\_reader\_frequency\_1: . Added in MySQL 8.3.0.
- telemetry.metrics\_reader\_frequency\_2: . Added in MySQL 8.3.0.
- telemetry.metrics\_reader\_frequency\_3: . Added in MySQL 8.3.0.
- telemetry.otel\_bsp\_max\_export\_batch\_size: Maximum batch size. Added in MySQL 8.1.0.
- telemetry.otel\_bsp\_max\_queue\_size: Maximum queue size. Added in MySQL 8.1.0.
- telemetry.otel\_bsp\_schedule\_delay: Delay interval between two consecutive exports in milliseconds. Added in MySQL 8.1.0.
- telemetry.otel\_exporter\_otlp\_metrics\_certificates: The trusted certificate to use when verifying a server's TLS credentials. Added in MySQL 8.3.0.
- telemetry.otel\_exporter\_otlp\_metrics\_cipher: TLS cipher to use for metrics (TLS 1.2). Added in MySQL 8.3.0.
- telemetry.otel\_exporter\_otlp\_metrics\_cipher\_suite: TLS cipher to use for metrics (TLS 1.3). Added in MySQL 8.3.0.
- telemetry.otel\_exporter\_otlp\_metrics\_client\_certificates: Client certificate/chain trust for clients private key in PEM format. Added in MySQL 8.3.0.
- telemetry.otel\_exporter\_otlp\_metrics\_client\_key: Client's private key in PEM format. Added in MySQL 8.3.0.
- telemetry.otel\_exporter\_otlp\_metrics\_compression: Compression used by exporter. Added in MySQL 8.3.0.
- telemetry.otel\_exporter\_otlp\_metrics\_endpoint: Metrics endpoint URL. Added in MySQL 8.3.0.
- telemetry.otel\_exporter\_otlp\_metrics\_headers: Key-value pairs to be used as headers associated with HTTP requests. Added in MySQL 8.3.0.
- telemetry.otel\_exporter\_otlp\_metrics\_max\_tls: Maximum TLS version to use for metrics. Added in MySQL 8.3.0.
- telemetry.otel\_exporter\_otlp\_metrics\_min\_tls: Minimum TLS version to use for metrics. Added in MySQL 8.3.0.
- telemetry.otel\_exporter\_otlp\_metrics\_protocol: Specifies the OTLP transport protocol. Added in MySQL 8.3.0.
- telemetry.otel\_exporter\_otlp\_metrics\_timeout: Time OLTP exporter waits for each batch export. Added in MySQL 8.3.0.
- telemetry.otel\_exporter\_otlp\_traces\_certificates: The trusted certificate to use when verifying a server's TLS credentials.. Added in MySQL 8.1.0.
- telemetry.otel\_exporter\_otlp\_traces\_cipher: TLS cipher to use for traces (TLS 1.2). Added in MySQL 8.3.0.
- telemetry.otel\_exporter\_otlp\_traces\_cipher\_suite: TLS cipher to use for traces (TLS 1.3). Added in MySQL 8.3.0.

- telemetry.otel\_exporter\_otlp\_traces\_client\_certificates: Client certificate/chain trust for clients private key in PEM format.. Added in MySQL 8.1.0.
- telemetry.otel\_exporter\_otlp\_traces\_client\_key: Client's private key in PEM format.. Added in MySQL 8.1.0.
- telemetry.otel\_exporter\_otlp\_traces\_compression: Compression used by exporter. Added in MySQL 8.1.0.
- telemetry.otel\_exporter\_otlp\_traces\_endpoint: Target URL to which the exporter sends traces. Added in MySQL 8.1.0.
- telemetry.otel\_exporter\_otlp\_traces\_headers: Key-value pairs to be used as headers associated with HTTP requests. Added in MySQL 8.1.0.
- telemetry.otel\_exporter\_otlp\_traces\_max\_tls: Maximum TLS version to use for traces. Added in MySQL 8.3.0.
- telemetry.otel\_exporter\_otlp\_traces\_min\_tls: Minimum TLS version to use for traces. Added in MySQL 8.3.0.
- telemetry.otel\_exporter\_otlp\_traces\_protocol: OTLP transport protocol. Added in MySQL 8.1.0.
- telemetry.otel\_exporter\_otlp\_traces\_timeout: Time OLTP exporter waits for each batch export. Added in MySQL 8.1.0.
- telemetry.otel\_log\_level: Controls which opentelemetry logs are printed in the server logs (Linux only). Added in MySQL 8.1.0.
- telemetry.otel\_resource\_attributes: See corresponding OpenTelemetry variable OTEL\_RESOURCE\_ATTRIBUTES.. Added in MySQL 8.1.0.
- telemetry.query\_text\_enabled: Controls whether the SQL query text is included in the trace (Linux only). Added in MySQL 8.1.0.
- telemetry.trace\_enabled: Controls whether telemetry traces are collected or not (Linux only). Added in MySQL 8.1.0.
- thread\_pool\_longrun\_trx\_limit: When all threads using thread\_pool\_max\_transactions\_limit have been executing longer than this number of milliseconds, limit for group is suspended. Added in MySQL 8.4.0.
- tls\_certificates\_enforced\_validation: Whether to validate server and CA certificates. Added in MySQL 8.1.0.

# <span id="page-66-0"></span>**Options and Variables Deprecated in MySQL 8.4**

The following system variables, status variables, and options have been deprecated in MySQL 8.4.

- Com\_show\_master\_status: Count of SHOW MASTER STATUS statements. Deprecated in MySQL 8.2.0.
- authentication\_fido\_rp\_id: Relying party ID for FIDO multifactor authentication. Deprecated in MySQL 8.2.0.
- binlog\_transaction\_dependency\_tracking: Source of dependency information (commit timestamps or transaction write sets) from which to assess which transactions can be executed in parallel by replica's multithreaded applier. Deprecated in MySQL 8.2.0.
- [character-set-client-handshake](https://dev.mysql.com/doc/refman/8.0/en/server-options.md#option_mysqld_character-set-client-handshake): Do not ignore client side character set value sent during handshake. Deprecated in MySQL 8.2.0.

- group\_replication\_allow\_local\_lower\_version\_join: Allow current server to join group even if it has lower plugin version than group. Deprecated in MySQL 8.4.0.
- group\_replication\_view\_change\_uuid: UUID for view change event GTIDs. Deprecated in MySQL 8.3.0.
- mysql-native-password: Enable mysql\_native\_password authentication plugin. Deprecated in MySQL 8.4.0.
- new: Use very new, possibly 'unsafe' functions. Deprecated in MySQL 8.2.0.
- old: Cause server to revert to certain behaviors present in older versions. Deprecated in MySQL 8.2.0.
- performance\_schema\_show\_processlist: Select SHOW PROCESSLIST implementation. Deprecated in MySQL 8.2.0.
- restrict\_fk\_on\_non\_standard\_key: Disallow creation of foreign keys on non-unique or partial keys. Deprecated in MySQL 8.4.0.
- [skip-character-set-client-handshake](https://dev.mysql.com/doc/refman/8.0/en/server-options.md#option_mysqld_character-set-client-handshake): Ignore client side character set value sent during handshake. Deprecated in MySQL 8.2.0.
- skip-new: Do not use new, possibly wrong routines. Deprecated in MySQL 8.2.0.

# <span id="page-67-0"></span>**Options and Variables Removed in MySQL 8.4**

The following system variables, status variables, and options have been removed in MySQL 8.4.

- Com\_change\_master: Count of CHANGE REPLICATION SOURCE TO and CHANGE MASTER TO statements. Removed in MySQL 8.4.0.
- Com\_show\_master\_status: Count of SHOW MASTER STATUS statements. Removed in MySQL 8.4.0.
- Com\_show\_slave\_hosts: Count of SHOW REPLICAS and SHOW SLAVE HOSTS statements. Removed in MySQL 8.4.0.
- Com\_show\_slave\_status: Count of SHOW REPLICA STATUS and SHOW SLAVE STATUS statements. Removed in MySQL 8.4.0.
- Com\_slave\_start: Count of START REPLICA and START SLAVE statements. Removed in MySQL 8.4.0.
- Com\_slave\_stop: Count of STOP REPLICA and STOP SLAVE statements. Removed in MySQL 8.4.0.
- Replica\_rows\_last\_search\_algorithm\_used: Search algorithm most recently used by this replica to locate rows for row-based replication (index, table, or hash scan). Removed in MySQL 8.3.0.
- abort-slave-event-count: Option used by mysql-test for debugging and testing of replication. Removed in MySQL 8.2.0.
- admin-ssl: Enable connection encryption. Removed in MySQL 8.4.0.
- authentication\_fido\_rp\_id: Relying party ID for FIDO multifactor authentication. Removed in MySQL 8.4.0.
- avoid\_temporal\_upgrade: Whether ALTER TABLE should upgrade pre-5.6.4 temporal columns. Removed in MySQL 8.4.0.

- binlog\_transaction\_dependency\_tracking: Source of dependency information (commit timestamps or transaction write sets) from which to assess which transactions can be executed in parallel by replica's multithreaded applier. Removed in MySQL 8.4.0.
- character-set-client-handshake: Do not ignore client side character set value sent during handshake. Removed in MySQL 8.3.0.
- daemon\_memcached\_enable\_binlog: . Removed in MySQL 8.3.0.
- daemon\_memcached\_engine\_lib\_name: Shared library implementing InnoDB memcached plugin. Removed in MySQL 8.3.0.
- daemon\_memcached\_engine\_lib\_path: Directory which contains shared library implementing InnoDB memcached plugin. Removed in MySQL 8.3.0.
- daemon\_memcached\_option: Space-separated options which are passed to underlying memcached daemon on startup. Removed in MySQL 8.3.0.
- daemon\_memcached\_r\_batch\_size: Specifies how many memcached read operations to perform before doing COMMIT to start new transaction. Removed in MySQL 8.3.0.
- daemon\_memcached\_w\_batch\_size: Specifies how many memcached write operations to perform before doing COMMIT to start new transaction. Removed in MySQL 8.3.0.
- default\_authentication\_plugin: Default authentication plugin. Removed in MySQL 8.4.0.
- disconnect-slave-event-count: Option used by mysql-test for debugging and testing of replication. Removed in MySQL 8.2.0.
- expire\_logs\_days: Purge binary logs after this many days. Removed in MySQL 8.2.0.
- group\_replication\_ip\_whitelist: List of hosts permitted to connect to group. Removed in MySQL 8.3.0.
- group\_replication\_primary\_member: Primary member UUID when group operates in singleprimary mode. Empty string if group is operating in multi-primary mode. Removed in MySQL 8.3.0.
- group\_replication\_recovery\_complete\_at: Recovery policies when handling cached transactions after state transfer. Removed in MySQL 8.4.0.
- have\_openssl: Whether mysqld supports SSL connections. Removed in MySQL 8.4.0.
- have\_ssl: Whether mysqld supports SSL connections. Removed in MySQL 8.4.0.
- innodb: Enable InnoDB (if this version of MySQL supports it). Removed in MySQL 8.3.0.
- innodb\_api\_bk\_commit\_interval: How often to auto-commit idle connections which use InnoDB memcached interface, in seconds. Removed in MySQL 8.3.0.
- innodb\_api\_disable\_rowlock: . Removed in MySQL 8.3.0.
- innodb\_api\_enable\_binlog: Allows use of InnoDB memcached plugin with MySQL binary log. Removed in MySQL 8.3.0.
- innodb\_api\_enable\_mdl: Locks table used by InnoDB memcached plugin, so that it cannot be dropped or altered by DDL through SQL interface. Removed in MySQL 8.3.0.
- innodb\_api\_trx\_level: Allows control of transaction isolation level on queries processed by memcached interface. Removed in MySQL 8.3.0.
- keyring\_encrypted\_file\_data: keyring\_encrypted\_file plugin data file. Removed in MySQL 8.4.0.

- keyring\_encrypted\_file\_password: keyring\_encrypted\_file plugin password. Removed in MySQL 8.4.0.
- keyring\_file\_data: keyring\_file plugin data file. Removed in MySQL 8.4.0.
- keyring\_oci\_ca\_certificate: CA certificate file for peer authentication. Removed in MySQL 8.4.0.
- keyring\_oci\_compartment: OCI compartment OCID. Removed in MySQL 8.4.0.
- keyring\_oci\_encryption\_endpoint: OCI encryption server endpoint. Removed in MySQL 8.4.0.
- keyring\_oci\_key\_file: OCI RSA private key file. Removed in MySQL 8.4.0.
- keyring\_oci\_key\_fingerprint: OCI RSA private key file fingerprint. Removed in MySQL 8.4.0.
- keyring\_oci\_management\_endpoint: OCI management server endpoint. Removed in MySQL 8.4.0.
- keyring\_oci\_master\_key: OCI master key OCID. Removed in MySQL 8.4.0.
- keyring\_oci\_secrets\_endpoint: OCI secrets server endpoint. Removed in MySQL 8.4.0.
- keyring\_oci\_tenancy: OCI tenancy OCID. Removed in MySQL 8.4.0.
- keyring\_oci\_user: OCI user OCID. Removed in MySQL 8.4.0.
- keyring\_oci\_vaults\_endpoint: OCI vaults server endpoint. Removed in MySQL 8.4.0.
- keyring\_oci\_virtual\_vault: OCI vault OCID. Removed in MySQL 8.4.0.
- language: Client error messages in given language. May be given as full path. Removed in MySQL 8.4.0.
- log\_bin\_use\_v1\_row\_events: Whether server is using version 1 binary log row events. Removed in MySQL 8.3.0.
- master-info-file: Location and name of file that remembers source and where I/O replication thread is in source's binary log. Removed in MySQL 8.3.0.
- master\_info\_repository: Whether to write connection metadata repository, containing source information and replication I/O thread location in source's binary log, to file or table. Removed in MySQL 8.3.0.
- new: Use very new, possibly 'unsafe' functions. Removed in MySQL 8.4.0.
- no-dd-upgrade: Prevent automatic upgrade of data dictionary tables at startup. Removed in MySQL 8.4.0.
- old: Cause server to revert to certain behaviors present in older versions. Removed in MySQL 8.4.0.
- old-style-user-limits: Enable old-style user limits (before 5.0.3, user resources were counted per each user+host vs. per account). Removed in MySQL 8.3.0.
- relay\_log\_info\_file: File name for applier metadata repository in which replica records information about relay logs. Removed in MySQL 8.3.0.
- relay\_log\_info\_repository: Whether to write location of replication SQL thread in relay logs to file or table. Removed in MySQL 8.3.0.
- show\_old\_temporals: Whether SHOW CREATE TABLE should indicate pre-5.6.4 temporal columns. Removed in MySQL 8.4.0.

- skip-character-set-client-handshake: Ignore client side character set value sent during handshake. Removed in MySQL 8.3.0.
- skip-host-cache: Do not cache host names. Removed in MySQL 8.3.0.
- skip-ssl: Disable connection encryption. Removed in MySQL 8.4.0.
- slave\_rows\_search\_algorithms: Determines search algorithms used for replica update batching. Any 2 or 3 from this list: INDEX\_SEARCH, TABLE\_SCAN, HASH\_SCAN. Removed in MySQL 8.3.0.
- ssl: Enable connection encryption. Removed in MySQL 8.4.0.
- transaction\_write\_set\_extraction: Defines algorithm used to hash writes extracted during transaction. Removed in MySQL 8.3.0.

# <span id="page-70-0"></span>**1.6 How to Report Bugs or Problems**

Before posting a bug report about a problem, please try to verify that it is a bug and that it has not been reported already:

- Start by searching the MySQL online manual at [https://dev.mysql.com/doc/.](https://dev.mysql.com/doc/) We try to keep the manual up to date by updating it frequently with solutions to newly found problems. In addition, the release notes accompanying the manual can be particularly useful since it is quite possible that a newer version contains a solution to your problem. The release notes are available at the location just given for the manual.
- If you get a parse error for an SQL statement, please check your syntax closely. If you cannot find something wrong with it, it is extremely likely that your current version of MySQL Server doesn't support the syntax you are using. If you are using the current version and the manual doesn't cover the syntax that you are using, MySQL Server doesn't support your statement.

If the manual covers the syntax you are using, but you have an older version of MySQL Server, you should check the MySQL change history to see when the syntax was implemented. In this case, you have the option of upgrading to a newer version of MySQL Server.

- For solutions to some common problems, see Section B.3, "Problems and Common Errors".
- Search the bugs database at <http://bugs.mysql.com/>to see whether the bug has been reported and fixed.
- You can also use<http://www.mysql.com/search/> to search all the Web pages (including the manual) that are located at the MySQL website.

If you cannot find an answer in the manual, the bugs database, or the mailing list archives, check with your local MySQL expert. If you still cannot find an answer to your question, please use the following guidelines for reporting the bug.

The normal way to report bugs is to visit [http://bugs.mysql.com/,](http://bugs.mysql.com/) which is the address for our bugs database. This database is public and can be browsed and searched by anyone. If you log in to the system, you can enter new reports.

Bugs posted in the bugs database at<http://bugs.mysql.com/> that are corrected for a given release are noted in the release notes.

If you find a security bug in MySQL Server, please let us know immediately by sending an email message to <secalert\_us@oracle.com>. Exception: Support customers should report all problems, including security bugs, to Oracle Support at <http://support.oracle.com/>.

To discuss problems with other users, you can use the [MySQL Community Slack.](https://mysqlcommunity.slack.com/)

Writing a good bug report takes patience, but doing it right the first time saves time both for us and for yourself. A good bug report, containing a full test case for the bug, makes it very likely that we will fix

the bug in the next release. This section helps you write your report correctly so that you do not waste your time doing things that may not help us much or at all. Please read this section carefully and make sure that all the information described here is included in your report.

Preferably, you should test the problem using the latest production or development version of MySQL Server before posting. Anyone should be able to repeat the bug by just using mysql test < script\_file on your test case or by running the shell or Perl script that you include in the bug report. Any bug that we are able to repeat has a high chance of being fixed in the next MySQL release.

It is most helpful when a good description of the problem is included in the bug report. That is, give a good example of everything you did that led to the problem and describe, in exact detail, the problem itself. The best reports are those that include a full example showing how to reproduce the bug or problem. See Section 7.9, "Debugging MySQL".

Remember that it is possible for us to respond to a report containing too much information, but not to one containing too little. People often omit facts because they think they know the cause of a problem and assume that some details do not matter. A good principle to follow is that if you are in doubt about stating something, state it. It is faster and less troublesome to write a couple more lines in your report than to wait longer for the answer if we must ask you to provide information that was missing from the initial report.

The most common errors made in bug reports are (a) not including the version number of the MySQL distribution that you use, and (b) not fully describing the platform on which the MySQL server is installed (including the platform type and version number). These are highly relevant pieces of information, and in 99 cases out of 100, the bug report is useless without them. Very often we get questions like, "Why doesn't this work for me?" Then we find that the feature requested wasn't implemented in that MySQL version, or that a bug described in a report has been fixed in newer MySQL versions. Errors often are platform-dependent. In such cases, it is next to impossible for us to fix anything without knowing the operating system and the version number of the platform.

If you compiled MySQL from source, remember also to provide information about your compiler if it is related to the problem. Often people find bugs in compilers and think the problem is MySQLrelated. Most compilers are under development all the time and become better version by version. To determine whether your problem depends on your compiler, we need to know what compiler you used. Note that every compiling problem should be regarded as a bug and reported accordingly.

If a program produces an error message, it is very important to include the message in your report. If we try to search for something from the archives, it is better that the error message reported exactly matches the one that the program produces. (Even the lettercase should be observed.) It is best to copy and paste the entire error message into your report. You should never try to reproduce the message from memory.

If you have a problem with Connector/ODBC (MyODBC), please try to generate a trace file and send it with your report. See [How to Report Connector/ODBC Problems or Bugs.](https://dev.mysql.com/doc/connector-odbc/en/connector-odbc-support-bug-report.md)

If your report includes long query output lines from test cases that you run with the mysql commandline tool, you can make the output more readable by using the --vertical option or the \G statement terminator. The EXPLAIN SELECT example later in this section demonstrates the use of \G.

Please include the following information in your report:

- The version number of the MySQL distribution you are using (for example, MySQL 5.7.10). You can find out which version you are running by executing mysqladmin version. The mysqladmin program can be found in the bin directory under your MySQL installation directory.
- The manufacturer and model of the machine on which you experience the problem.
- The operating system name and version. If you work with Windows, you can usually get the name and version number by double-clicking your My Computer icon and pulling down the "Help/About Windows" menu. For most Unix-like operating systems, you can get this information by executing the command uname -a.

- Sometimes the amount of memory (real and virtual) is relevant. If in doubt, include these values.
- The contents of the docs/INFO\_BIN file from your MySQL installation. This file contains information about how MySQL was configured and compiled.
- If you are using a source distribution of the MySQL software, include the name and version number of the compiler that you used. If you have a binary distribution, include the distribution name.
- If the problem occurs during compilation, include the exact error messages and also a few lines of context around the offending code in the file where the error occurs.
- If mysqld died, you should also report the statement that caused mysqld to unexpectedly exit. You can usually get this information by running mysqld with query logging enabled, and then looking in the log after mysqld exits. See Section 7.9, "Debugging MySQL".
- If a database table is related to the problem, include the output from the SHOW CREATE TABLE db\_name.tbl\_name statement in the bug report. This is a very easy way to get the definition of any table in a database. The information helps us create a situation matching the one that you have experienced.
- The SQL mode in effect when the problem occurred can be significant, so please report the value of the sql\_mode system variable. For stored procedure, stored function, and trigger objects, the relevant sql\_mode value is the one in effect when the object was created. For a stored procedure or function, the SHOW CREATE PROCEDURE or SHOW CREATE FUNCTION statement shows the relevant SQL mode, or you can query INFORMATION\_SCHEMA for the information:

```
SELECT ROUTINE_SCHEMA, ROUTINE_NAME, SQL_MODE
FROM INFORMATION_SCHEMA.ROUTINES;
```

For triggers, you can use this statement:

```
SELECT EVENT_OBJECT_SCHEMA, EVENT_OBJECT_TABLE, TRIGGER_NAME, SQL_MODE
FROM INFORMATION_SCHEMA.TRIGGERS;
```

• For performance-related bugs or problems with SELECT statements, you should always include the output of EXPLAIN SELECT ..., and at least the number of rows that the SELECT statement produces. You should also include the output from SHOW CREATE TABLE tbl\_name for each table that is involved. The more information you provide about your situation, the more likely it is that someone can help you.

The following is an example of a very good bug report. The statements are run using the mysql command-line tool. Note the use of the \G statement terminator for statements that would otherwise provide very long output lines that are difficult to read.

```
mysql> SHOW VARIABLES;
mysql> SHOW COLUMNS FROM ...\G
 <output from SHOW COLUMNS>
mysql> EXPLAIN SELECT ...\G
 <output from EXPLAIN>
mysql> FLUSH STATUS;
mysql> SELECT ...;
 <A short version of the output from SELECT,
 including the time taken to run the query>
mysql> SHOW STATUS;
 <output from SHOW STATUS>
```

• If a bug or problem occurs while running mysqld, try to provide an input script that reproduces the anomaly. This script should include any necessary source files. The more closely the script can reproduce your situation, the better. If you can make a reproducible test case, you should upload it to be attached to the bug report.

If you cannot provide a script, you should at least include the output from mysqladmin variables extended-status processlist in your report to provide some information on how your system is performing.

- If you cannot produce a test case with only a few rows, or if the test table is too big to be included in the bug report (more than 10 rows), you should dump your tables using mysqldump and create a README file that describes your problem. Create a compressed archive of your files using tar and gzip or zip. After you initiate a bug report for our bugs database at<http://bugs.mysql.com/>, click the Files tab in the bug report for instructions on uploading the archive to the bugs database.
- If you believe that the MySQL server produces a strange result from a statement, include not only the result, but also your opinion of what the result should be, and an explanation describing the basis for your opinion.
- When you provide an example of the problem, it is better to use the table names, variable names, and so forth that exist in your actual situation than to come up with new names. The problem could be related to the name of a table or variable. These cases are rare, perhaps, but it is better to be safe than sorry. After all, it should be easier for you to provide an example that uses your actual situation, and it is by all means better for us. If you have data that you do not want to be visible to others in the bug report, you can upload it using the Files tab as previously described. If the information is really top secret and you do not want to show it even to us, go ahead and provide an example using other names, but please regard this as the last choice.
- Include all the options given to the relevant programs, if possible. For example, indicate the options that you use when you start the mysqld server, as well as the options that you use to run any MySQL client programs. The options to programs such as mysqld and mysql, and to the configure script, are often key to resolving problems and are very relevant. It is never a bad idea to include them. If your problem involves a program written in a language such as Perl or PHP, please include the language processor's version number, as well as the version for any modules that the program uses. For example, if you have a Perl script that uses the DBI and DBD::mysql modules, include the version numbers for Perl, DBI, and DBD::mysql.
- If your question is related to the privilege system, please include the output of mysqladmin reload, and all the error messages you get when trying to connect. When you test your privileges, you should execute mysqladmin reload version and try to connect with the program that gives you trouble.
- If you have a patch for a bug, do include it. But do not assume that the patch is all we need, or that we can use it, if you do not provide some necessary information such as test cases showing the bug that your patch fixes. We might find problems with your patch or we might not understand it at all. If so, we cannot use it.
  - If we cannot verify the exact purpose of the patch, we will not use it. Test cases help us here. Show that the patch handles all the situations that may occur. If we find a borderline case (even a rare one) where the patch will not work, it may be useless.
- Guesses about what the bug is, why it occurs, or what it depends on are usually wrong. Even the MySQL team cannot guess such things without first using a debugger to determine the real cause of a bug.
- Indicate in your bug report that you have checked the reference manual and mail archive so that others know you have tried to solve the problem yourself.
- If your data appears corrupt or you get errors when you access a particular table, first check your tables with CHECK TABLE. If that statement reports any errors:
  - The InnoDB crash recovery mechanism handles cleanup when the server is restarted after being killed, so in typical operation there is no need to "repair" tables. If you encounter an error with InnoDB tables, restart the server and see whether the problem persists, or whether the error affected only cached data in memory. If data is corrupted on disk, consider restarting with the innodb\_force\_recovery option enabled so that you can dump the affected tables.
  - For non-transactional tables, try to repair them with REPAIR TABLE or with myisamchk. See Chapter 7, MySQL Server Administration.

If you are running Windows, please verify the value of lower\_case\_table\_names using the SHOW VARIABLES LIKE 'lower\_case\_table\_names' statement. This variable affects how the server handles lettercase of database and table names. Its effect for a given value should be as described in Section 11.2.3, "Identifier Case Sensitivity".

- If you often get corrupted tables, you should try to find out when and why this happens. In this case, the error log in the MySQL data directory may contain some information about what happened. (This is the file with the .err suffix in the name.) See Section 7.4.2, "The Error Log". Please include any relevant information from this file in your bug report. Normally mysqld should never corrupt a table if nothing killed it in the middle of an update. If you can find the cause of mysqld dying, it is much easier for us to provide you with a fix for the problem. See Section B.3.1, "How to Determine What Is Causing a Problem".
- If possible, download and install the most recent version of MySQL Server and check whether it solves your problem. All versions of the MySQL software are thoroughly tested and should work without problems. We believe in making everything as backward-compatible as possible, and you should be able to switch MySQL versions without difficulty. See [Section 2.1.2, "Which MySQL](#page-86-2) [Version and Distribution to Install".](#page-86-2)

# <span id="page-74-0"></span>**1.7 MySQL Standards Compliance**

This section describes how MySQL relates to the ANSI/ISO SQL standards. MySQL Server has many extensions to the SQL standard, and here you can find out what they are and how to use them. You can also find information about functionality missing from MySQL Server, and how to work around some of the differences.

The SQL standard has been evolving since 1986 and several versions exist. In this manual, "SQL-92" refers to the standard released in 1992. "SQL:1999", "SQL:2003", "SQL:2008", and "SQL:2011" refer to the versions of the standard released in the corresponding years, with the last being the most recent version. We use the phrase "the SQL standard" or "standard SQL" to mean the current version of the SQL Standard at any time.

One of our main goals with the product is to continue to work toward compliance with the SQL standard, but without sacrificing speed or reliability. We are not afraid to add extensions to SQL or support for non-SQL features if this greatly increases the usability of MySQL Server for a large segment of our user base. The HANDLER interface is an example of this strategy. See Section 15.2.5, "HANDLER Statement".

We continue to support transactional and nontransactional databases to satisfy both mission-critical 24/7 usage and heavy Web or logging usage.

MySQL Server was originally designed to work with medium-sized databases (10-100 million rows, or about 100MB per table) on small computer systems. Today MySQL Server handles terabyte-sized databases.

We are not targeting real-time support, although MySQL replication capabilities offer significant functionality.

MySQL supports ODBC levels 0 to 3.51.

MySQL supports high-availability database clustering using the NDBCLUSTER storage engine. See Chapter 25, MySQL NDB Cluster 8.4.

We implement XML functionality which supports most of the W3C XPath standard. See Section 14.11, "XML Functions".

MySQL supports a native JSON data type as defined by RFC 7159, and based on the ECMAScript standard (ECMA-262). See Section 13.5, "The JSON Data Type". MySQL also implements a subset of the SQL/JSON functions specified by a pre-publication draft of the SQL:2016 standard; see Section 14.17, "JSON Functions", for more information.

# **Selecting SQL Modes**

The MySQL server can operate in different SQL modes, and can apply these modes differently for different clients, depending on the value of the sql\_mode system variable. DBAs can set the global SQL mode to match site server operating requirements, and each application can set its session SQL mode to its own requirements.

Modes affect the SQL syntax MySQL supports and the data validation checks it performs. This makes it easier to use MySQL in different environments and to use MySQL together with other database servers.

For more information on setting the SQL mode, see Section 7.1.11, "Server SQL Modes".

# **Running MySQL in ANSI Mode**

To run MySQL Server in ANSI mode, start mysqld with the --ansi option. Running the server in ANSI mode is the same as starting it with the following options:

```
--transaction-isolation=SERIALIZABLE --sql-mode=ANSI
```

To achieve the same effect at runtime, execute these two statements:

```
SET GLOBAL TRANSACTION ISOLATION LEVEL SERIALIZABLE;
SET GLOBAL sql_mode = 'ANSI';
```

You can see that setting the sql\_mode system variable to 'ANSI' enables all SQL mode options that are relevant for ANSI mode as follows:

```
mysql> SET GLOBAL sql_mode='ANSI';
mysql> SELECT @@GLOBAL.sql_mode;
 -> 'REAL_AS_FLOAT,PIPES_AS_CONCAT,ANSI_QUOTES,IGNORE_SPACE,ANSI'
```

Running the server in ANSI mode with --ansi is not quite the same as setting the SQL mode to 'ANSI' because the --ansi option also sets the transaction isolation level.

See Section 7.1.7, "Server Command Options".

# <span id="page-75-0"></span>**1.7.1 MySQL Extensions to Standard SQL**

MySQL Server supports some extensions that you are not likely to find in other SQL DBMSs. Be warned that if you use them, your code is most likely not portable to other SQL servers. In some cases, you can write code that includes MySQL extensions, but is still portable, by using comments of the following form:

```
/*! MySQL-specific code */
```

In this case, MySQL Server parses and executes the code within the comment as it would any other SQL statement, but other SQL servers should ignore the extensions. For example, MySQL Server recognizes the STRAIGHT\_JOIN keyword in the following statement, but other servers should not:

```
SELECT /*! STRAIGHT_JOIN */ col1 FROM table1,table2 WHERE ...
```

If you add a version number after the ! character, the syntax within the comment is executed only if the MySQL version is greater than or equal to the specified version number. The KEY\_BLOCK\_SIZE clause in the following comment is executed only by servers from MySQL 5.1.10 or higher:

```
CREATE TABLE t1(a INT, KEY (a)) /*!50110 KEY_BLOCK_SIZE=1024 */;
```

The following descriptions list MySQL extensions, organized by category.

## • Organization of data on disk

MySQL Server maps each database to a directory under the MySQL data directory, and maps tables within a database to file names in the database directory. Consequently, database and table names are case-sensitive in MySQL Server on operating systems that have case-sensitive file names (such as most Unix systems). See Section 11.2.3, "Identifier Case Sensitivity".

- General language syntax
  - By default, strings can be enclosed by " as well as '. If the ANSI\_QUOTES SQL mode is enabled, strings can be enclosed only by ' and the server interprets strings enclosed by " as identifiers.
  - \ is the escape character in strings.
  - In SQL statements, you can access tables from different databases with the db\_name.tbl\_name syntax. Some SQL servers provide the same functionality but call this User space. MySQL Server doesn't support tablespaces such as used in statements like this: CREATE TABLE ralph.my\_table ... IN my\_tablespace.
- SQL statement syntax
  - The ANALYZE TABLE, CHECK TABLE, OPTIMIZE TABLE, and REPAIR TABLE statements.
  - The CREATE DATABASE, DROP DATABASE, and ALTER DATABASE statements. See Section 15.1.12, "CREATE DATABASE Statement", Section 15.1.24, "DROP DATABASE Statement", and Section 15.1.2, "ALTER DATABASE Statement".
  - The DO statement.
  - EXPLAIN SELECT to obtain a description of how tables are processed by the query optimizer.
  - The FLUSH and RESET statements.
  - The SET statement. See Section 15.7.6.1, "SET Syntax for Variable Assignment".
  - The SHOW statement. See Section 15.7.7, "SHOW Statements". The information produced by many of the MySQL-specific SHOW statements can be obtained in more standard fashion by using SELECT to query INFORMATION\_SCHEMA. See Chapter 28, INFORMATION\_SCHEMA Tables.
  - Use of LOAD DATA. In many cases, this syntax is compatible with Oracle LOAD DATA. See Section 15.2.9, "LOAD DATA Statement".
  - Use of RENAME TABLE. See Section 15.1.36, "RENAME TABLE Statement".
  - Use of REPLACE instead of DELETE plus INSERT. See Section 15.2.12, "REPLACE Statement".
  - Use of CHANGE col\_name, DROP col\_name, or DROP INDEX, IGNORE or RENAME in ALTER TABLE statements. Use of multiple ADD, ALTER, DROP, or CHANGE clauses in an ALTER TABLE statement. See Section 15.1.9, "ALTER TABLE Statement".
  - Use of index names, indexes on a prefix of a column, and use of INDEX or KEY in CREATE TABLE statements. See Section 15.1.20, "CREATE TABLE Statement".
  - Use of TEMPORARY or IF NOT EXISTS with CREATE TABLE.
  - Use of IF EXISTS with DROP TABLE and DROP DATABASE.
  - The capability of dropping multiple tables with a single DROP TABLE statement.
  - The ORDER BY and LIMIT clauses of the UPDATE and DELETE statements.
  - INSERT INTO tbl\_name SET col\_name = ... syntax.

- The DELAYED clause of the INSERT and REPLACE statements.
- The LOW\_PRIORITY clause of the INSERT, REPLACE, DELETE, and UPDATE statements.
- Use of INTO OUTFILE or INTO DUMPFILE in SELECT statements. See Section 15.2.13, "SELECT Statement".
- Options such as STRAIGHT\_JOIN or SQL\_SMALL\_RESULT in SELECT statements.
- You don't need to name all selected columns in the GROUP BY clause. This gives better performance for some very specific, but quite normal queries. See Section 14.19, "Aggregate Functions".
- You can specify ASC and DESC with GROUP BY, not just with ORDER BY.
- The ability to set variables in a statement with the := assignment operator. See Section 11.4, "User-Defined Variables".
- Data types
  - The MEDIUMINT, SET, and ENUM data types, and the various BLOB and TEXT data types.
  - The AUTO\_INCREMENT, BINARY, NULL, UNSIGNED, and ZEROFILL data type attributes.
- Functions and operators
  - To make it easier for users who migrate from other SQL environments, MySQL Server supports aliases for many functions. For example, all string functions support both standard SQL syntax and ODBC syntax.
  - MySQL Server understands the || and && operators to mean logical OR and AND, as in the C programming language. In MySQL Server, || and OR are synonyms, as are && and AND. Because of this nice syntax, MySQL Server doesn't support the standard SQL || operator for string concatenation; use CONCAT() instead. Because CONCAT() takes any number of arguments, it is easy to convert use of the || operator to MySQL Server.
  - Use of COUNT(DISTINCT value\_list) where value\_list has more than one element.
  - String comparisons are case-insensitive by default, with sort ordering determined by the collation of the current character set, which is utf8mb4 by default. To perform case-sensitive comparisons instead, you should declare your columns with the BINARY attribute or use the BINARY cast, which causes comparisons to be done using the underlying character code values rather than a lexical ordering.
  - The % operator is a synonym for MOD(). That is, N % M is equivalent to MOD(N,M). % is supported for C programmers and for compatibility with PostgreSQL.
  - The =, <>, <=, <, >=, >, <<, >>, <=>, AND, OR, or LIKE operators may be used in expressions in the output column list (to the left of the FROM) in SELECT statements. For example:

```
mysql> SELECT col1=1 AND col2=2 FROM my_table;
```

- The LAST\_INSERT\_ID() function returns the most recent AUTO\_INCREMENT value. See Section 14.15, "Information Functions".
- LIKE is permitted on numeric values.
- The REGEXP and NOT REGEXP extended regular expression operators.
- CONCAT() or CHAR() with one argument or more than two arguments. (In MySQL Server, these functions can take a variable number of arguments.)

- The BIT\_COUNT(), CASE, ELT(), FROM\_DAYS(), FORMAT(), IF(), MD5(), PERIOD\_ADD(), PERIOD\_DIFF(), TO\_DAYS(), and WEEKDAY() functions.
- Use of TRIM() to trim substrings. Standard SQL supports removal of single characters only.
- The GROUP BY functions STD(), BIT\_OR(), BIT\_AND(), BIT\_XOR(), and GROUP\_CONCAT(). See Section 14.19, "Aggregate Functions".

# <span id="page-78-0"></span>**1.7.2 MySQL Differences from Standard SQL**

We try to make MySQL Server follow the ANSI SQL standard and the ODBC SQL standard, but MySQL Server performs operations differently in some cases:

- There are several differences between the MySQL and standard SQL privilege systems. For example, in MySQL, privileges for a table are not automatically revoked when you delete a table. You must explicitly issue a REVOKE statement to revoke privileges for a table. For more information, see Section 15.7.1.8, "REVOKE Statement".
- The CAST() function does not support cast to REAL or BIGINT. See Section 14.10, "Cast Functions and Operators".