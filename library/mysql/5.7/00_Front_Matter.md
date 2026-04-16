---
source: MySQL 5.7 Reference
title: 00_Front_Matter
---

# **MySQL 5.7 Reference Manual Including MySQL NDB Cluster 7.5 and NDB Cluster 7.6**

#### **Abstract**

This is the MySQL Reference Manual. It documents MySQL 5.7 through 5.7.52, as well as NDB Cluster releases based on version 7.5 of NDB through 5.7.44-ndb-7.5.36, respectively. It may include documentation of features of MySQL versions that have not yet been released. For information about which versions have been released, see the [MySQL 5.7 Release Notes](https://dev.mysql.com/doc/relnotes/mysql/5.7/en/).

**MySQL 5.7 features.** This manual describes features that are not included in every edition of MySQL 5.7; such features may not be included in the edition of MySQL 5.7 licensed to you. If you have any questions about the features included in your edition of MySQL 5.7, refer to your MySQL 5.7 license agreement or contact your Oracle sales representative.

For notes detailing the changes in each release, see the [MySQL 5.7 Release Notes.](https://dev.mysql.com/doc/relnotes/mysql/5.7/en/)

For legal information, including licensing information, see the [Preface and Legal Notices](#page-24-0).

For help with using MySQL, please visit the [MySQL Forums,](http://forums.mysql.com) where you can discuss your issues with other MySQL users.

Document generated on: 2026-04-08 (revision: 84563)

## **Table of Contents**

| Preface and Legal Notices xxv                                                      |     |
|------------------------------------------------------------------------------------|-----|
| 1 General Information 1                                                            |     |
| 1.1 About This Manual 2                                                            |     |
| 1.2 Overview of the MySQL Database Management System 4                             |     |
| 1.2.1 What is MySQL? 4                                                             |     |
| 1.2.2 The Main Features of MySQL 5                                                 |     |
| 1.2.3 History of MySQL 8                                                           |     |
| 1.3 What Is New in MySQL 5.7 8                                                     |     |
| 1.4 Server and Status Variables and Options Added, Deprecated, or Removed in MySQL |     |
| 5.7 24                                                                             |     |
| 1.5 How to Report Bugs or Problems 40                                              |     |
| 1.6 MySQL Standards Compliance 44                                                  |     |
| 1.6.1 MySQL Extensions to Standard SQL 45                                          |     |
| 1.6.2 MySQL Differences from Standard SQL 48                                       |     |
| 1.6.3 How MySQL Deals with Constraints 51                                          |     |
| 2 Installing and Upgrading MySQL 55                                                |     |
| 2.1 General Installation Guidance 57                                               |     |
| 2.1.1 Supported Platforms 58                                                       |     |
| 2.1.2 Which MySQL Version and Distribution to Install 58                           |     |
| 2.1.3 How to Get MySQL 59                                                          |     |
| 2.1.4 Verifying Package Integrity Using MD5 Checksums or GnuPG 59                  |     |
| 2.1.5 Installation Layouts 75                                                      |     |
| 2.1.6 Compiler-Specific Build Characteristics 75                                   |     |
| 2.2 Installing MySQL on Unix/Linux Using Generic Binaries 76                       |     |
| 2.3 Installing MySQL on Microsoft Windows 79                                       |     |
| 2.3.1 MySQL Installation Layout on Microsoft Windows 81                            |     |
| 2.3.2 Choosing an Installation Package 82                                          |     |
| 2.3.3 MySQL Installer for Windows 83                                               |     |
| 2.3.4 Installing MySQL on Microsoft Windows Using a noinstall ZIP Archive 112      |     |
| 2.3.5 Troubleshooting a Microsoft Windows MySQL Server Installation 121            |     |
| 2.3.6 Windows Postinstallation Procedures                                          | 122 |
| 2.3.7 Windows Platform Restrictions 124                                            |     |
| 2.4 Installing MySQL on macOS 125                                                  |     |
| 2.4.1 General Notes on Installing MySQL on macOS 126                               |     |
| 2.4.2 Installing MySQL on macOS Using Native Packages 127                          |     |
| 2.4.3 Installing a MySQL Launch Daemon                                             | 132 |
| 2.4.4 Installing and Using the MySQL Preference Pane 135                           |     |
| 2.5 Installing MySQL on Linux 139                                                  |     |
| 2.5.1 Installing MySQL on Linux Using the MySQL Yum Repository 140                 |     |
| 2.5.2 Replacing a Third-Party Distribution of MySQL Using the MySQL Yum            |     |
| Repository                                                                         | 144 |
| 2.5.3 Installing MySQL on Linux Using the MySQL APT Repository 146                 |     |
| 2.5.4 Installing MySQL on Linux Using the MySQL SLES Repository 146                |     |
| 2.5.5 Installing MySQL on Linux Using RPM Packages from Oracle 146                 |     |
| 2.5.6 Installing MySQL on Linux Using Debian Packages from Oracle 151              |     |
| 2.5.7 Deploying MySQL on Linux with Docker 153                                     |     |
| 2.5.8 Installing MySQL on Linux from the Native Software Repositories 162          |     |
| 2.5.9 Installing MySQL on Linux with Juju 165                                      |     |
| 2.5.10 Managing MySQL Server with systemd                                          | 165 |
|                                                                                    |     |
| 2.6 Installing MySQL Using Unbreakable Linux Network (ULN)                         | 170 |
| 2.7 Installing MySQL on Solaris 171                                                |     |
| 2.7.1 Installing MySQL on Solaris Using a Solaris PKG                              | 172 |
| 2.8 Installing MySQL from Source 173                                               |     |
| 2.8.1 Source Installation Methods 173                                              |     |
| 2.8.2 Source Installation Prerequisites                                            | 173 |

| 2.8.3 MySQL Layout for Source Installation 175                              |     |
|-----------------------------------------------------------------------------|-----|
| 2.8.4 Installing MySQL Using a Standard Source Distribution 175             |     |
| 2.8.5 Installing MySQL Using a Development Source Tree 179                  |     |
| 2.8.6 Configuring SSL Library Support 181                                   |     |
| 2.8.7 MySQL Source-Configuration Options 182                                |     |
| 2.8.8 Dealing with Problems Compiling MySQL 203                             |     |
| 2.8.9 MySQL Configuration and Third-Party Tools 204                         |     |
| 2.9 Postinstallation Setup and Testing 205                                  |     |
| 2.9.1 Initializing the Data Directory                                       | 205 |
| 2.9.2 Starting the Server 211                                               |     |
| 2.9.3 Testing the Server 214                                                |     |
| 2.9.4 Securing the Initial MySQL Account 215                                |     |
| 2.9.5 Starting and Stopping MySQL Automatically 217                         |     |
| 2.10 Upgrading MySQL 218                                                    |     |
| 2.10.1 Before You Begin 218                                                 |     |
| 2.10.2 Upgrade Paths 219                                                    |     |
| 2.10.3 Changes in MySQL 5.7 220                                             |     |
| 2.10.4 Upgrading MySQL Binary or Package-based Installations on Unix/Linux  | 229 |
| 2.10.5 Upgrading MySQL with the MySQL Yum Repository 232                    |     |
| 2.10.6 Upgrading MySQL with the MySQL APT Repository 233                    |     |
|                                                                             |     |
| 2.10.7 Upgrading MySQL with the MySQL SLES Repository 233                   |     |
| 2.10.8 Upgrading MySQL on Windows 234                                       |     |
| 2.10.9 Upgrading a Docker Installation of MySQL 235                         |     |
| 2.10.10 Upgrading MySQL with Directly-Downloaded RPM Packages 235           |     |
| 2.10.11 Upgrade Troubleshooting 237                                         |     |
| 2.10.12 Rebuilding or Repairing Tables or Indexes 237                       |     |
| 2.10.13 Copying MySQL Databases to Another Machine 238                      |     |
| 2.11 Downgrading MySQL 239                                                  |     |
| 2.11.1 Before You Begin 240                                                 |     |
| 2.11.2 Downgrade Paths 240                                                  |     |
| 2.11.3 Downgrade Notes 240                                                  |     |
| 2.11.4 Downgrading Binary and Package-based Installations on Unix/Linux 243 |     |
| 2.11.5 Downgrade Troubleshooting 245                                        |     |
| 2.12 Perl Installation Notes 246                                            |     |
| 2.12.1 Installing Perl on Unix 246                                          |     |
| 2.12.2 Installing ActiveState Perl on Windows 247                           |     |
| 2.12.3 Problems Using the Perl DBI/DBD Interface 247                        |     |
| 3 Tutorial 249                                                              |     |
| 3.1 Connecting to and Disconnecting from the Server 249                     |     |
| 3.2 Entering Queries 250                                                    |     |
| 3.3 Creating and Using a Database 253                                       |     |
| 3.3.1 Creating and Selecting a Database 254                                 |     |
| 3.3.2 Creating a Table 255                                                  |     |
| 3.3.3 Loading Data into a Table 256                                         |     |
| 3.3.4 Retrieving Information from a Table 257                               |     |
| 3.4 Getting Information About Databases and Tables 270                      |     |
| 3.5 Using mysql in Batch Mode 271                                           |     |
| 3.6 Examples of Common Queries 272                                          |     |
| 3.6.1 The Maximum Value for a Column 273                                    |     |
| 3.6.2 The Row Holding the Maximum of a Certain Column 273                   |     |
| 3.6.3 Maximum of Column per Group 273                                       |     |
| 3.6.4 The Rows Holding the Group-wise Maximum of a Certain Column 274       |     |
| 3.6.5 Using User-Defined Variables 274                                      |     |
| 3.6.6 Using Foreign Keys 275                                                |     |
| 3.6.7 Searching on Two Keys 277                                             |     |
| 3.6.8 Calculating Visits Per Day 277                                        |     |
| 3.6.9 Using AUTO_INCREMENT 278                                              |     |
| 3.7 Using MySQL with Apache 280                                             |     |
|                                                                             |     |

| 4 MySQL Programs 281                                                       |     |
|----------------------------------------------------------------------------|-----|
| 4.1 Overview of MySQL Programs 282                                         |     |
| 4.2 Using MySQL Programs 286                                               |     |
| 4.2.1 Invoking MySQL Programs 286                                          |     |
| 4.2.2 Specifying Program Options 287                                       |     |
| 4.2.3 Command Options for Connecting to the Server 300                     |     |
| 4.2.4 Connecting to the MySQL Server Using Command Options 311             |     |
| 4.2.5 Connection Transport Protocols 314                                   |     |
| 4.2.6 Connection Compression Control 315                                   |     |
| 4.2.7 Setting Environment Variables 316                                    |     |
| 4.3 Server and Server-Startup Programs                                     | 317 |
| 4.3.1 mysqld — The MySQL Server 317                                        |     |
| 4.3.2 mysqld_safe — MySQL Server Startup Script 317                        |     |
| 4.3.3 mysql.server — MySQL Server Startup Script 326                       |     |
| 4.3.4 mysqld_multi — Manage Multiple MySQL Servers 328                     |     |
| 4.4 Installation-Related Programs 333                                      |     |
| 4.4.1 comp_err — Compile MySQL Error Message File 333                      |     |
| 4.4.2 mysql_install_db — Initialize MySQL Data Directory 335               |     |
| 4.4.3 mysql_plugin — Configure MySQL Server Plugins 344                    |     |
| 4.4.4 mysql_secure_installation — Improve MySQL Installation Security 346  |     |
| 4.4.5 mysql_ssl_rsa_setup — Create SSL/RSA Files 351                       |     |
| 4.4.6 mysql_tzinfo_to_sql — Load the Time Zone Tables 354                  |     |
| 4.4.7 mysql_upgrade — Check and Upgrade MySQL Tables                       | 354 |
| 4.5 Client Programs 364                                                    |     |
| 4.5.1 mysql — The MySQL Command-Line Client 364                            |     |
| 4.5.2 mysqladmin — A MySQL Server Administration Program                   | 403 |
| 4.5.3 mysqlcheck — A Table Maintenance Program 416                         |     |
|                                                                            |     |
| 4.5.4 mysqldump — A Database Backup Program                                | 430 |
| 4.5.5 mysqlimport — A Data Import Program 461                              |     |
| 4.5.6 mysqlpump — A Database Backup Program                                | 474 |
| 4.5.7 mysqlshow — Display Database, Table, and Column Information 496      |     |
| 4.5.8 mysqlslap — A Load Emulation Client 506                              |     |
| 4.6 Administrative and Utility Programs 521                                |     |
| 4.6.1 innochecksum — Offline InnoDB File Checksum Utility 521              |     |
| 4.6.2 myisam_ftdump — Display Full-Text Index information 528              |     |
| 4.6.3 myisamchk — MyISAM Table-Maintenance Utility 529                     |     |
| 4.6.4 myisamlog — Display MyISAM Log File Contents 548                     |     |
| 4.6.5 myisampack — Generate Compressed, Read-Only MyISAM Tables 549        |     |
| 4.6.6 mysql_config_editor — MySQL Configuration Utility                    | 556 |
| 4.6.7 mysqlbinlog — Utility for Processing Binary Log Files 562            |     |
| 4.6.8 mysqldumpslow — Summarize Slow Query Log Files 590                   |     |
| 4.7 Program Development Utilities 592                                      |     |
| 4.7.1 mysql_config — Display Options for Compiling Clients 592             |     |
| 4.7.2 my_print_defaults — Display Options from Option Files 594            |     |
| 4.7.3 resolve_stack_dump — Resolve Numeric Stack Trace Dump to Symbols 595 |     |
| 4.8 Miscellaneous Programs 596                                             |     |
| 4.8.1 lz4_decompress — Decompress mysqlpump LZ4-Compressed Output 596      |     |
| 4.8.2 perror — Display MySQL Error Message Information 596                 |     |
| 4.8.3 replace — A String-Replacement Utility 597                           |     |
| 4.8.4 resolveip — Resolve Host name to IP Address or Vice Versa 598        |     |
| 4.8.5 zlib_decompress — Decompress mysqlpump ZLIB-Compressed Output 598    |     |
| 4.9 Environment Variables 599                                              |     |
| 4.10 Unix Signal Handling in MySQL 601                                     |     |
| 5 MySQL Server Administration 605                                          |     |
| 5.1 The MySQL Server 606                                                   |     |
| 5.1.1 Configuring the Server 606                                           |     |
| 5.1.2 Server Configuration Defaults                                        | 608 |
| 5.1.3 Server Option, System Variable, and Status Variable Reference 608    |     |

| 5.1.4 Server System Variable Reference                                   |       |
|--------------------------------------------------------------------------|-------|
| 5.1.5 Server Status Variable Reference                                   | 666   |
| 5.1.6 Server Command Options                                             | . 680 |
| 5.1.7 Server System Variables                                            |       |
| 5.1.8 Using System Variables                                             |       |
| 5.1.9 Server Status Variables                                            |       |
| 5.1.10 Server SQL Modes                                                  |       |
| 5.1.11 Connection Management                                             |       |
|                                                                          |       |
| 5.1.12 IPv6 Support                                                      |       |
| 5.1.13 MySQL Server Time Zone Support                                    |       |
| 5.1.14 Server-Side Help Support                                          |       |
| 5.1.15 Server Tracking of Client Session State                           |       |
| 5.1.16 The Server Shutdown Process                                       |       |
| 5.2 The MySQL Data Directory                                             |       |
| 5.3 The mysql System Database                                            | 895   |
| 5.4 MySQL Server Logs                                                    | . 898 |
| 5.4.1 Selecting General Query Log and Slow Query Log Output Destinations | 899   |
| 5.4.2 The Error Log                                                      |       |
| 5.4.3 The General Query Log                                              |       |
| 5.4.4 The Binary Log                                                     |       |
| 5.4.5 The Slow Query Log                                                 |       |
| 5.4.6 The DDL Log                                                        |       |
|                                                                          |       |
| 5.4.7 Server Log Maintenance                                             |       |
| 5.5 MySQL Server Plugins                                                 |       |
| 5.5.1 Installing and Uninstalling Plugins                                |       |
| 5.5.2 Obtaining Server Plugin Information                                |       |
| 5.5.3 MySQL Enterprise Thread Pool                                       |       |
| 5.5.4 The Rewriter Query Rewrite Plugin                                  |       |
| 5.5.5 Version Tokens                                                     | 942   |
| 5.5.6 MySQL Plugin Services                                              | 953   |
| 5.6 MySQL Server Loadable Functions                                      | 960   |
| 5.6.1 Installing and Uninstalling Loadable Functions                     |       |
| 5.6.2 Obtaining Information About Loadable Functions                     |       |
| 5.7 Running Multiple MySQL Instances on One Machine                      |       |
| 5.7.1 Setting Up Multiple Data Directories                               |       |
| 5.7.2 Running Multiple MySQL Instances on Windows                        |       |
| 5.7.3 Running Multiple MySQL Instances on Unix                           |       |
| 5.7.4 Using Client Programs in a Multiple-Server Environment             |       |
|                                                                          |       |
| 5.8 Debugging MySQL                                                      |       |
| 5.8.1 Debugging a MySQL Server                                           |       |
| 5.8.2 Debugging a MySQL Client                                           |       |
| 5.8.3 The DBUG Package                                                   |       |
| 5.8.4 Tracing mysqld Using DTrace                                        |       |
| 6 Security                                                               |       |
| 6.1 General Security Issues                                              |       |
| 6.1.1 Security Guidelines                                                | 1000  |
| 6.1.2 Keeping Passwords Secure                                           | 1002  |
| 6.1.3 Making MySQL Secure Against Attackers                              |       |
| 6.1.4 Security-Related mysqld Options and Variables                      |       |
| 6.1.5 How to Run MySQL as a Normal User                                  |       |
| 6.1.6 Security Considerations for LOAD DATA LOCAL                        |       |
| 6.1.7 Client Programming Security Guidelines                             |       |
| 6.2 Access Control and Account Management                                |       |
| 6.2.1 Account User Names and Passwords                                   |       |
|                                                                          |       |
| 6.2.2 Privileges Provided by MySQL                                       |       |
| 6.2.3 Grant Tables                                                       |       |
| 6.2.4 Specifying Account Names                                           |       |
| 6.2.5 Access Control, Stage 1: Connection Verification                   | 1034  |

| 6.2.7 Adding Accounts, Assigning Privileges, and Dropping Accounts 1039                   | 6.2.6 Access Control, Stage 2: Request Verification 1038 |
|-------------------------------------------------------------------------------------------|----------------------------------------------------------|
|                                                                                           |                                                          |
| 6.2.8 Reserved Accounts 1042                                                              |                                                          |
| 6.2.9 When Privilege Changes Take Effect 1043                                             |                                                          |
| 6.2.10 Assigning Account Passwords 1043                                                   |                                                          |
| 6.2.11 Password Management 1045                                                           |                                                          |
| 6.2.12 Server Handling of Expired Passwords 1047                                          |                                                          |
| 6.2.13 Pluggable Authentication 1049                                                      |                                                          |
| 6.2.14 Proxy Users                                                                        | 1053                                                     |
| 6.2.15 Account Locking 1060                                                               |                                                          |
| 6.2.16 Setting Account Resource Limits 1060                                               |                                                          |
| 6.2.17 Troubleshooting Problems Connecting to MySQL 1062                                  |                                                          |
| 6.2.18 SQL-Based Account Activity Auditing 1067                                           |                                                          |
| 6.3 Using Encrypted Connections 1068                                                      |                                                          |
| 6.3.1 Configuring MySQL to Use Encrypted Connections 1070                                 |                                                          |
| 6.3.2 Encrypted Connection TLS Protocols and Ciphers 1075                                 |                                                          |
|                                                                                           |                                                          |
| 6.3.3 Creating SSL and RSA Certificates and Keys 1081                                     |                                                          |
| 6.3.4 SSL Library-Dependent Capabilities                                                  | 1090                                                     |
| 6.3.5 Connecting to MySQL Remotely from Windows with SSH 1091                             |                                                          |
| 6.4 Security Plugins 1091                                                                 |                                                          |
| 6.4.1 Authentication Plugins 1092                                                         |                                                          |
| 6.4.2 Connection Control Plugins 1157                                                     |                                                          |
| 6.4.3 The Password Validation Plugin 1163                                                 |                                                          |
| 6.4.4 The MySQL Keyring 1170                                                              |                                                          |
| 6.4.5 MySQL Enterprise Audit 1204                                                         |                                                          |
| 6.4.6 MySQL Enterprise Firewall 1270                                                      |                                                          |
| 6.5 MySQL Enterprise Data Masking and De-Identification 1285                              |                                                          |
| 6.5.1 MySQL Enterprise Data Masking and De-Identification Elements 1287                   |                                                          |
| 6.5.2 Installing or Uninstalling MySQL Enterprise Data Masking and De-Identification 1287 |                                                          |
| 6.5.3 Using MySQL Enterprise Data Masking and De-Identification 1288                      |                                                          |
| 6.5.4 MySQL Enterprise Data Masking and De-Identification Function Reference 1293         |                                                          |
| 6.5.5 MySQL Enterprise Data Masking and De-Identification Function Descriptions 1294      |                                                          |
| 6.6 MySQL Enterprise Encryption 1302                                                      |                                                          |
| 6.6.1 MySQL Enterprise Encryption Installation 1303                                       |                                                          |
|                                                                                           |                                                          |
|                                                                                           |                                                          |
| 6.6.2 MySQL Enterprise Encryption Usage and Examples 1303                                 |                                                          |
| 6.6.3 MySQL Enterprise Encryption Function Reference                                      | 1306                                                     |
| 6.6.4 MySQL Enterprise Encryption Function Descriptions 1306                              |                                                          |
| 6.7 SELinux 1310                                                                          |                                                          |
| 6.7.1 Check if SELinux is Enabled 1310                                                    |                                                          |
| 6.7.2 Changing the SELinux Mode 1311                                                      |                                                          |
| 6.7.3 MySQL Server SELinux Policies 1311                                                  |                                                          |
| 6.7.4 SELinux File Context 1311                                                           |                                                          |
| 6.7.5 SELinux TCP Port Context 1313                                                       |                                                          |
| 6.7.6 Troubleshooting SELinux 1314                                                        |                                                          |
| 7 Backup and Recovery 1317                                                                |                                                          |
| 7.1 Backup and Recovery Types 1318                                                        |                                                          |
| 7.2 Database Backup Methods 1321                                                          |                                                          |
| 7.3 Example Backup and Recovery Strategy 1323                                             |                                                          |
| 7.3.1 Establishing a Backup Policy                                                        | 1323                                                     |
| 7.3.2 Using Backups for Recovery 1325                                                     |                                                          |
| 7.3.3 Backup Strategy Summary 1326                                                        |                                                          |
| 7.4 Using mysqldump for Backups 1326                                                      |                                                          |
| 7.4.1 Dumping Data in SQL Format with mysqldump 1326                                      |                                                          |
| 7.4.2 Reloading SQL-Format Backups                                                        | 1327                                                     |
| 7.4.3 Dumping Data in Delimited-Text Format with mysqldump 1328                           |                                                          |
| 7.4.4 Reloading Delimited-Text Format Backups 1329                                        |                                                          |
| 7.4.5 mysqldump Tips 1330                                                                 |                                                          |

| 7.5.1 Point-in-Time Recovery Using Binary Log 1332                     |      |
|------------------------------------------------------------------------|------|
| 7.5.2 Point-in-Time Recovery Using Event Positions 1333                |      |
| 7.6 MyISAM Table Maintenance and Crash Recovery 1334                   |      |
| 7.6.1 Using myisamchk for Crash Recovery 1335                          |      |
| 7.6.2 How to Check MyISAM Tables for Errors 1336                       |      |
| 7.6.3 How to Repair MyISAM Tables 1336                                 |      |
| 7.6.4 MyISAM Table Optimization 1338                                   |      |
| 7.6.5 Setting Up a MyISAM Table Maintenance Schedule 1339              |      |
| 8 Optimization 1341                                                    |      |
| 8.1 Optimization Overview 1343                                         |      |
| 8.2 Optimizing SQL Statements 1344                                     |      |
| 8.2.1 Optimizing SELECT Statements 1344                                |      |
| 8.2.2 Optimizing Subqueries, Derived Tables, and View References 1386  |      |
| 8.2.3 Optimizing INFORMATION_SCHEMA Queries 1396                       |      |
| 8.2.4 Optimizing Data Change Statements 1401                           |      |
| 8.2.5 Optimizing Database Privileges 1402                              |      |
| 8.2.6 Other Optimization Tips 1402                                     |      |
| 8.3 Optimization and Indexes 1403                                      |      |
| 8.3.1 How MySQL Uses Indexes 1403                                      |      |
| 8.3.2 Primary Key Optimization 1404                                    |      |
| 8.3.3 Foreign Key Optimization 1405                                    |      |
| 8.3.4 Column Indexes 1405                                              |      |
| 8.3.5 Multiple-Column Indexes 1406                                     |      |
| 8.3.6 Verifying Index Usage 1408                                       |      |
| 8.3.7 InnoDB and MyISAM Index Statistics Collection 1408               |      |
| 8.3.8 Comparison of B-Tree and Hash Indexes 1409                       |      |
| 8.3.9 Use of Index Extensions 1411                                     |      |
| 8.3.10 Optimizer Use of Generated Column Indexes 1413                  |      |
| 8.3.11 Indexed Lookups from TIMESTAMP Columns 1414                     |      |
| 8.4 Optimizing Database Structure 1416                                 |      |
| 8.4.1 Optimizing Data Size 1416                                        |      |
| 8.4.2 Optimizing MySQL Data Types 1418                                 |      |
| 8.4.3 Optimizing for Many Tables                                       | 1420 |
| 8.4.4 Internal Temporary Table Use in MySQL 1421                       |      |
| 8.4.5 Limits on Number of Databases and Tables 1423                    |      |
| 8.4.6 Limits on Table Size 1423                                        |      |
| 8.4.7 Limits on Table Column Count and Row Size 1424                   |      |
| 8.5 Optimizing for InnoDB Tables 1427                                  |      |
| 8.5.1 Optimizing Storage Layout for InnoDB Tables 1427                 |      |
| 8.5.2 Optimizing InnoDB Transaction Management 1428                    |      |
| 8.5.3 Optimizing InnoDB Read-Only Transactions 1429                    |      |
| 8.5.4 Optimizing InnoDB Redo Logging 1430                              |      |
| 8.5.5 Bulk Data Loading for InnoDB Tables 1430                         |      |
| 8.5.6 Optimizing InnoDB Queries 1431                                   |      |
| 8.5.7 Optimizing InnoDB DDL Operations 1432                            |      |
| 8.5.8 Optimizing InnoDB Disk I/O                                       | 1432 |
| 8.5.9 Optimizing InnoDB Configuration Variables 1435                   |      |
| 8.5.10 Optimizing InnoDB for Systems with Many Tables 1436             |      |
| 8.6 Optimizing for MyISAM Tables 1437                                  |      |
| 8.6.1 Optimizing MyISAM Queries                                        | 1437 |
| 8.6.2 Bulk Data Loading for MyISAM Tables 1438                         |      |
| 8.6.3 Optimizing REPAIR TABLE Statements 1439                          |      |
| 8.7 Optimizing for MEMORY Tables                                       | 1441 |
| 8.8 Understanding the Query Execution Plan 1441                        |      |
| 8.8.1 Optimizing Queries with EXPLAIN 1441                             |      |
| 8.8.2 EXPLAIN Output Format 1442                                       |      |
| 8.8.3 Extended EXPLAIN Output Format 1455                              |      |
| 8.8.4 Obtaining Execution Plan Information for a Named Connection 1457 |      |
|                                                                        |      |

| 8.8.5 Estimating Query Performance                        | 1458 |
|-----------------------------------------------------------|------|
| 8.9 Controlling the Query Optimizer                       | 1458 |
| 8.9.1 Controlling Query Plan Evaluation                   |      |
| 8.9.2 Switchable Optimizations                            |      |
| 8.9.3 Optimizer Hints                                     |      |
| 8.9.4 Index Hints                                         |      |
| 8.9.5 The Optimizer Cost Model                            |      |
| 8.10 Buffering and Caching                                |      |
| 8.10.1 InnoDB Buffer Pool Optimization                    |      |
|                                                           |      |
| 8.10.2 The MylSAM Key Cache                               |      |
| 8.10.3 The MySQL Query Cache                              |      |
| 8.10.4 Caching of Prepared Statements and Stored Programs |      |
| 8.11 Optimizing Locking Operations                        |      |
| 8.11.1 Internal Locking Methods                           |      |
| 8.11.2 Table Locking Issues                               |      |
| 8.11.3 Concurrent Inserts                                 | 1491 |
| 8.11.4 Metadata Locking                                   | 1492 |
| 8.11.5 External Locking                                   | 1495 |
| 8.12 Optimizing the MySQL Server                          | 1496 |
| 8.12.1 System Factors                                     |      |
| 8.12.2 Optimizing Disk I/O                                |      |
| 8.12.3 Using Symbolic Links                               |      |
| 8.12.4 Optimizing Memory Use                              |      |
| 8.13 Measuring Performance (Benchmarking)                 |      |
| 8.13.1 Measuring the Speed of Expressions and Functions   |      |
| 8.13.2 Using Your Own Benchmarks                          |      |
| 8.13.3 Measuring Performance with performance_schema      |      |
| 8.14 Examining Server Thread (Process) Information        |      |
| 8.14.1 Accessing the Process List                         |      |
| 8.14.2 Thread Command Values                              |      |
| 8.14.3 General Thread States                              |      |
|                                                           |      |
| 8.14.4 Query Cache Thread States                          |      |
| 8.14.5 Replication Source Thread States                   |      |
| 8.14.6 Replication Replica I/O Thread States              | 1520 |
| 8.14.7 Replication Replica SQL Thread States              |      |
| 8.14.8 Replication Replica Connection Thread States       |      |
| 8.14.9 NDB Cluster Thread States                          |      |
| 8.14.10 Event Scheduler Thread States                     |      |
| 8.15 Tracing the Optimizer                                |      |
| 8.15.1 Typical Usage                                      |      |
| 8.15.2 System Variables Controlling Tracing               |      |
| 8.15.3 Traceable Statements                               | 1524 |
| 8.15.4 Tuning Trace Purging                               | 1525 |
| 8.15.5 Tracing Memory Usage                               | 1526 |
| 8.15.6 Privilege Checking                                 | 1526 |
| 8.15.7 Interaction with thedebug Option                   | 1526 |
| 8.15.8 The optimizer_trace System Variable                | 1526 |
| 8.15.9 The end_markers_in_json System Variable            |      |
| 8.15.10 Selecting Optimizer Features to Trace             |      |
| 8.15.11 Trace General Structure                           | 1527 |
| 8.15.12 Example                                           |      |
| 8.15.13 Displaying Traces in Other Applications           |      |
| 8.15.14 Preventing the Use of Optimizer Trace             |      |
| 8.15.15 Testing Optimizer Trace                           |      |
| 8.15.16 Optimizer Trace Implementation                    |      |
| 9 Language Structure                                      |      |
| 9.1 Literal Values                                        |      |
| 9.1 String Literals                                       | 1539 |

| 9.1.2 Numeric Literals 1542                                             |      |
|-------------------------------------------------------------------------|------|
| 9.1.3 Date and Time Literals                                            | 1542 |
| 9.1.4 Hexadecimal Literals 1544                                         |      |
| 9.1.5 Bit-Value Literals 1546                                           |      |
| 9.1.6 Boolean Literals 1547                                             |      |
| 9.1.7 NULL Values 1548                                                  |      |
| 9.2 Schema Object Names 1548                                            |      |
| 9.2.1 Identifier Length Limits 1549                                     |      |
| 9.2.2 Identifier Qualifiers 1550                                        |      |
| 9.2.3 Identifier Case Sensitivity 1552                                  |      |
| 9.2.4 Mapping of Identifiers to File Names                              | 1554 |
| 9.2.5 Function Name Parsing and Resolution 1556                         |      |
| 9.3 Keywords and Reserved Words 1560                                    |      |
| 9.4 User-Defined Variables 1582                                         |      |
| 9.5 Expressions                                                         | 1585 |
| 9.6 Comments                                                            | 1589 |
| 10 Character Sets, Collations, Unicode 1591                             |      |
| 10.1 Character Sets and Collations in General 1592                      |      |
| 10.2 Character Sets and Collations in MySQL 1593                        |      |
| 10.2.1 Character Set Repertoire 1594                                    |      |
|                                                                         |      |
| 10.2.2 UTF-8 for Metadata 1596                                          |      |
| 10.3 Specifying Character Sets and Collations 1597                      |      |
| 10.3.1 Collation Naming Conventions 1597                                |      |
| 10.3.2 Server Character Set and Collation                               | 1598 |
| 10.3.3 Database Character Set and Collation 1599                        |      |
| 10.3.4 Table Character Set and Collation 1600                           |      |
| 10.3.5 Column Character Set and Collation 1601                          |      |
| 10.3.6 Character String Literal Character Set and Collation 1602        |      |
| 10.3.7 The National Character Set 1604                                  |      |
| 10.3.8 Character Set Introducers 1604                                   |      |
| 10.3.9 Examples of Character Set and Collation Assignment 1606          |      |
| 10.3.10 Compatibility with Other DBMSs 1607                             |      |
| 10.4 Connection Character Sets and Collations 1607                      |      |
| 10.5 Configuring Application Character Set and Collation 1613           |      |
| 10.6 Error Message Character Set 1614                                   |      |
| 10.7 Column Character Set Conversion 1615                               |      |
| 10.8 Collation Issues 1616                                              |      |
| 10.8.1 Using COLLATE in SQL Statements 1616                             |      |
| 10.8.2 COLLATE Clause Precedence 1617                                   |      |
| 10.8.3 Character Set and Collation Compatibility 1617                   |      |
| 10.8.4 Collation Coercibility in Expressions 1617                       |      |
| 10.8.5 The binary Collation Compared to _bin Collations 1619            |      |
| 10.8.6 Examples of the Effect of Collation 1621                         |      |
| 10.8.7 Using Collation in INFORMATION_SCHEMA Searches 1622              |      |
| 10.9 Unicode Support 1624                                               |      |
| 10.9.1 The utf8mb4 Character Set (4-Byte UTF-8 Unicode Encoding) 1626   |      |
| 10.9.2 The utf8mb3 Character Set (3-Byte UTF-8 Unicode Encoding) 1626   |      |
| 10.9.3 The utf8 Character Set (Alias for utf8mb3) 1627                  |      |
| 10.9.4 The ucs2 Character Set (UCS-2 Unicode Encoding) 1627             |      |
|                                                                         |      |
| 10.9.5 The utf16 Character Set (UTF-16 Unicode Encoding) 1627           |      |
| 10.9.6 The utf16le Character Set (UTF-16LE Unicode Encoding) 1628       |      |
| 10.9.7 The utf32 Character Set (UTF-32 Unicode Encoding) 1628           |      |
| 10.9.8 Converting Between 3-Byte and 4-Byte Unicode Character Sets 1628 |      |
| 10.10 Supported Character Sets and Collations 1631                      |      |
| 10.10.1 Unicode Character Sets 1632                                     |      |
| 10.10.2 West European Character Sets 1636                               |      |
| 10.10.3 Central European Character Sets 1638                            |      |
| 10.10.4 South European and Middle East Character Sets 1639              |      |

| 10.10.5 Baltic Character Sets 1639                                           |      |
|------------------------------------------------------------------------------|------|
| 10.10.6 Cyrillic Character Sets 1640                                         |      |
| 10.10.7 Asian Character Sets 1640                                            |      |
| 10.10.8 The Binary Character Set 1644                                        |      |
| 10.11 Restrictions on Character Sets 1645                                    |      |
| 10.12 Setting the Error Message Language 1646                                |      |
| 10.13 Adding a Character Set 1646                                            |      |
| 10.13.1 Character Definition Arrays 1648                                     |      |
| 10.13.2 String Collating Support for Complex Character Sets 1649             |      |
| 10.13.3 Multi-Byte Character Support for Complex Character Sets 1649         |      |
| 10.14 Adding a Collation to a Character Set 1650                             |      |
| 10.14.1 Collation Implementation Types 1651                                  |      |
| 10.14.2 Choosing a Collation ID 1653                                         |      |
| 10.14.3 Adding a Simple Collation to an 8-Bit Character Set                  | 1654 |
| 10.14.4 Adding a UCA Collation to a Unicode Character Set 1655               |      |
| 10.15 Character Set Configuration 1662                                       |      |
| 10.16 MySQL Server Locale Support 1663                                       |      |
| 11 Data Types 1667                                                           |      |
| 11.1 Numeric Data Types 1668                                                 |      |
| 11.1.1 Numeric Data Type Syntax 1668                                         |      |
| 11.1.2 Integer Types (Exact Value) - INTEGER, INT, SMALLINT, TINYINT,        |      |
|                                                                              |      |
| MEDIUMINT, BIGINT 1671                                                       |      |
| 11.1.3 Fixed-Point Types (Exact Value) - DECIMAL, NUMERIC 1672               |      |
| 11.1.4 Floating-Point Types (Approximate Value) - FLOAT, DOUBLE 1672         |      |
| 11.1.5 Bit-Value Type - BIT 1673                                             |      |
| 11.1.6 Numeric Type Attributes 1673                                          |      |
| 11.1.7 Out-of-Range and Overflow Handling 1674                               |      |
| 11.2 Date and Time Data Types 1675                                           |      |
| 11.2.1 Date and Time Data Type Syntax 1677                                   |      |
| 11.2.2 The DATE, DATETIME, and TIMESTAMP Types 1679                          |      |
| 11.2.3 The TIME Type 1680                                                    |      |
| 11.2.4 The YEAR Type 1681                                                    |      |
| 11.2.5 2-Digit YEAR(2) Limitations and Migrating to 4-Digit YEAR 1681        |      |
| 11.2.6 Automatic Initialization and Updating for TIMESTAMP and DATETIME 1684 |      |
| 11.2.7 Fractional Seconds in Time Values 1687                                |      |
| 11.2.8 What Calendar Is Used By MySQL? 1688                                  |      |
| 11.2.9 Conversion Between Date and Time Types 1689                           |      |
| 11.2.10 2-Digit Years in Dates 1690                                          |      |
| 11.3 String Data Types 1690                                                  |      |
| 11.3.1 String Data Type Syntax 1690                                          |      |
| 11.3.2 The CHAR and VARCHAR Types 1694                                       |      |
| 11.3.3 The BINARY and VARBINARY Types                                        | 1695 |
| 11.3.4 The BLOB and TEXT Types                                               | 1697 |
| 11.3.5 The ENUM Type 1698                                                    |      |
| 11.3.6 The SET Type 1701                                                     |      |
| 11.4 Spatial Data Types 1703                                                 |      |
| 11.4.1 Spatial Data Types 1705                                               |      |
| 11.4.2 The OpenGIS Geometry Model 1705                                       |      |
| 11.4.3 Supported Spatial Data Formats 1711                                   |      |
| 11.4.4 Geometry Well-Formedness and Validity 1714                            |      |
| 11.4.5 Creating Spatial Columns 1714                                         |      |
| 11.4.6 Populating Spatial Columns 1715                                       |      |
| 11.4.7 Fetching Spatial Data 1716                                            |      |
| 11.4.8 Optimizing Spatial Analysis 1716                                      |      |
| 11.4.9 Creating Spatial Indexes 1716                                         |      |
|                                                                              |      |
| 11.4.10 Using Spatial Indexes 1717                                           |      |
| 11.5 The JSON Data Type 1719                                                 |      |
| 11.6 Data Type Default Values 1732                                           |      |

| 11.7 Data Type Storage Requirements 1734                                    |      |
|-----------------------------------------------------------------------------|------|
| 11.8 Choosing the Right Type for a Column 1738                              |      |
| 11.9 Using Data Types from Other Database Engines 1738                      |      |
| 12 Functions and Operators 1741                                             |      |
| 12.1 Built-In Function and Operator Reference 1742                          |      |
| 12.2 Loadable Function Reference 1758                                       |      |
| 12.3 Type Conversion in Expression Evaluation 1760                          |      |
| 12.4 Operators 1764                                                         |      |
| 12.4.1 Operator Precedence 1765                                             |      |
| 12.4.2 Comparison Functions and Operators 1766                              |      |
| 12.4.3 Logical Operators 1772                                               |      |
| 12.4.4 Assignment Operators 1773                                            |      |
| 12.5 Flow Control Functions 1775                                            |      |
| 12.6 Numeric Functions and Operators 1777                                   |      |
| 12.6.1 Arithmetic Operators 1778                                            |      |
| 12.6.2 Mathematical Functions 1780                                          |      |
| 12.7 Date and Time Functions 1788                                           |      |
| 12.8 String Functions and Operators 1809                                    |      |
| 12.8.1 String Comparison Functions and Operators 1824                       |      |
| 12.8.2 Regular Expressions 1828                                             |      |
| 12.8.3 Character Set and Collation of Function Results 1833                 |      |
| 12.9 Full-Text Search Functions 1834                                        |      |
| 12.9.1 Natural Language Full-Text Searches 1836                             |      |
| 12.9.2 Boolean Full-Text Searches 1839                                      |      |
| 12.9.3 Full-Text Searches with Query Expansion 1844                         |      |
| 12.9.4 Full-Text Stopwords 1845                                             |      |
| 12.9.5 Full-Text Restrictions 1849                                          |      |
| 12.9.6 Fine-Tuning MySQL Full-Text Search 1850                              |      |
| 12.9.7 Adding a User-Defined Collation for Full-Text Indexing 1853          |      |
| 12.9.8 ngram Full-Text Parser 1854                                          |      |
| 12.9.9 MeCab Full-Text Parser Plugin 1857                                   |      |
| 12.10 Cast Functions and Operators 1861                                     |      |
| 12.11 XML Functions 1867                                                    |      |
| 12.12 Bit Functions and Operators 1878                                      |      |
| 12.13 Encryption and Compression Functions 1881                             |      |
| 12.14 Locking Functions 1892                                                |      |
| 12.15 Information Functions 1895                                            |      |
| 12.16 Spatial Analysis Functions                                            | 1904 |
| 12.16.1 Spatial Function Reference                                          | 1904 |
| 12.16.2 Argument Handling by Spatial Functions 1909                         |      |
| 12.16.3 Functions That Create Geometry Values from WKT Values 1910          |      |
| 12.16.4 Functions That Create Geometry Values from WKB Values 1913          |      |
| 12.16.5 MySQL-Specific Functions That Create Geometry Values 1916           |      |
| 12.16.6 Geometry Format Conversion Functions 1916                           |      |
| 12.16.7 Geometry Property Functions 1917                                    |      |
| 12.16.8 Spatial Operator Functions 1926                                     |      |
| 12.16.9 Functions That Test Spatial Relations Between Geometry Objects 1929 |      |
| 12.16.10 Spatial Geohash Functions 1935                                     |      |
| 12.16.11 Spatial GeoJSON Functions 1936                                     |      |
| 12.16.12 Spatial Convenience Functions 1937                                 |      |
| 12.17 JSON Functions 1940                                                   |      |
| 12.17.1 JSON Function Reference 1940                                        |      |
| 12.17.2 Functions That Create JSON Values                                   | 1942 |
| 12.17.3 Functions That Search JSON Values 1943                              |      |
| 12.17.4 Functions That Modify JSON Values 1951                              |      |
| 12.17.5 Functions That Return JSON Value Attributes 1961                    |      |
| 12.17.6 JSON Utility Functions 1963                                         |      |
| 12.18 Functions Used with Global Transaction Identifiers (GTIDs) 1966       |      |
|                                                                             |      |

| 12.19 Aggregate Functions                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | 1909                                                                                                                                                                                 |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 12.19.1 Aggregate Function Descriptions                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | 1969                                                                                                                                                                                 |
| 12.19.2 GROUP BY Modifiers                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |                                                                                                                                                                                      |
| 12.19.3 MySQL Handling of GROUP BY                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | 1979                                                                                                                                                                                 |
| 12.19.4 Detection of Functional Dependence                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | 1982                                                                                                                                                                                 |
| 12.20 Miscellaneous Functions                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | 1985                                                                                                                                                                                 |
| 12.21 Precision Math                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | 1993                                                                                                                                                                                 |
| 12.21.1 Types of Numeric Values                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | 1994                                                                                                                                                                                 |
| 12.21.2 DECIMAL Data Type Characteristics                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |                                                                                                                                                                                      |
| 12.21.3 Expression Handling                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | 1995                                                                                                                                                                                 |
| 12.21.4 Rounding Behavior                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |                                                                                                                                                                                      |
| 12.21.5 Precision Math Examples                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |                                                                                                                                                                                      |
| 13 SQL Statements                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |                                                                                                                                                                                      |
| 13.1 Data Definition Statements                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |                                                                                                                                                                                      |
| 13.1.1 ALTER DATABASE Statement                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |                                                                                                                                                                                      |
| 13.1.2 ALTER EVENT Statement                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |                                                                                                                                                                                      |
| 13.1.3 ALTER FUNCTION Statement                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |                                                                                                                                                                                      |
| 13.1.4 ALTER INSTANCE Statement                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |                                                                                                                                                                                      |
| 13.1.5 ALTER LOGFILE GROUP Statement                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |                                                                                                                                                                                      |
| 13.1.6 ALTER PROCEDURE Statement                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |                                                                                                                                                                                      |
| 13.1.7 ALTER SERVER Statement                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |                                                                                                                                                                                      |
| 13.1.8 ALTER TABLE Statement                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |                                                                                                                                                                                      |
| 13.1.9 ALTER TABLESPACE Statement                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |                                                                                                                                                                                      |
| 13.1.10 ALTER VIEW Statement                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |                                                                                                                                                                                      |
| 13.1.11 CREATE DATABASE Statement                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |                                                                                                                                                                                      |
| 13.1.12 CREATE EVENT Statement                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |                                                                                                                                                                                      |
| 13.1.13 CREATE EVENT Statement                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |                                                                                                                                                                                      |
| 13.1.14 CREATE INDEX Statement                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |                                                                                                                                                                                      |
| 13.1.15 CREATE LOGFILE GROUP Statement                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |                                                                                                                                                                                      |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |                                                                                                                                                                                      |
| 12 1 16 CDEATE DDOCEDIDE and CDEATE ELINCTION Statements                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | ·/////////////////////////////////////                                                                                                                                               |
| 13.1.16 CREATE PROCEDURE and CREATE FUNCTION Statements                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |                                                                                                                                                                                      |
| 13.1.17 CREATE SERVER Statement                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | 2050                                                                                                                                                                                 |
| 13.1.17 CREATE SERVER Statement                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | 2050<br>2051                                                                                                                                                                         |
| 13.1.17 CREATE SERVER Statement                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | 2050<br>2051<br>2097                                                                                                                                                                 |
| 13.1.17 CREATE SERVER Statement 13.1.18 CREATE TABLE Statement 13.1.19 CREATE TABLESPACE Statement 13.1.20 CREATE TRIGGER Statement                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | 2050<br>2051<br>2097<br>2103                                                                                                                                                         |
| 13.1.17 CREATE SERVER Statement 13.1.18 CREATE TABLE Statement 13.1.19 CREATE TABLESPACE Statement 13.1.20 CREATE TRIGGER Statement 13.1.21 CREATE VIEW Statement                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | 2050<br>2051<br>2097<br>2103<br>2105                                                                                                                                                 |
| 13.1.17 CREATE SERVER Statement 13.1.18 CREATE TABLE Statement 13.1.19 CREATE TABLESPACE Statement 13.1.20 CREATE TRIGGER Statement 13.1.21 CREATE VIEW Statement 13.1.22 DROP DATABASE Statement                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | 2050<br>2051<br>2097<br>2103<br>2105<br>2110                                                                                                                                         |
| 13.1.17 CREATE SERVER Statement 13.1.18 CREATE TABLE Statement 13.1.19 CREATE TABLESPACE Statement 13.1.20 CREATE TRIGGER Statement 13.1.21 CREATE VIEW Statement 13.1.22 DROP DATABASE Statement 13.1.23 DROP EVENT Statement                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | 2050<br>2051<br>2097<br>2103<br>2105<br>2110<br>2111                                                                                                                                 |
| 13.1.17 CREATE SERVER Statement 13.1.18 CREATE TABLE Statement 13.1.19 CREATE TABLESPACE Statement 13.1.20 CREATE TRIGGER Statement 13.1.21 CREATE VIEW Statement 13.1.22 DROP DATABASE Statement 13.1.23 DROP EVENT Statement 13.1.24 DROP FUNCTION Statement                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | 2050<br>2051<br>2097<br>2103<br>2105<br>2110<br>2111<br>2111                                                                                                                         |
| 13.1.17 CREATE SERVER Statement 13.1.18 CREATE TABLE Statement 13.1.19 CREATE TABLESPACE Statement 13.1.20 CREATE TRIGGER Statement 13.1.21 CREATE VIEW Statement 13.1.22 DROP DATABASE Statement 13.1.23 DROP EVENT Statement 13.1.24 DROP FUNCTION Statement 13.1.25 DROP INDEX Statement                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | 2050<br>2051<br>2097<br>2103<br>2105<br>2110<br>2111<br>2111                                                                                                                         |
| 13.1.17 CREATE SERVER Statement 13.1.18 CREATE TABLE Statement 13.1.19 CREATE TABLESPACE Statement 13.1.20 CREATE TRIGGER Statement 13.1.21 CREATE VIEW Statement 13.1.22 DROP DATABASE Statement 13.1.23 DROP EVENT Statement 13.1.24 DROP FUNCTION Statement 13.1.25 DROP INDEX Statement 13.1.26 DROP LOGFILE GROUP Statement                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | 2050<br>2051<br>2097<br>2103<br>2105<br>2110<br>2111<br>2111<br>2111                                                                                                                 |
| 13.1.17 CREATE SERVER Statement 13.1.18 CREATE TABLE Statement 13.1.19 CREATE TABLESPACE Statement 13.1.20 CREATE TRIGGER Statement 13.1.21 CREATE VIEW Statement 13.1.22 DROP DATABASE Statement 13.1.23 DROP EVENT Statement 13.1.24 DROP FUNCTION Statement 13.1.25 DROP INDEX Statement 13.1.26 DROP LOGFILE GROUP Statement 13.1.27 DROP PROCEDURE and DROP FUNCTION Statements                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | 2050<br>2051<br>2097<br>2103<br>2105<br>2110<br>2111<br>2111<br>2111<br>2112<br>2112                                                                                                 |
| 13.1.17 CREATE SERVER Statement 13.1.18 CREATE TABLE Statement 13.1.19 CREATE TABLESPACE Statement 13.1.20 CREATE TRIGGER Statement 13.1.21 CREATE VIEW Statement 13.1.22 DROP DATABASE Statement 13.1.23 DROP EVENT Statement 13.1.24 DROP FUNCTION Statement 13.1.25 DROP INDEX Statement 13.1.26 DROP LOGFILE GROUP Statement 13.1.27 DROP PROCEDURE and DROP FUNCTION Statements 13.1.28 DROP SERVER Statement                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | 2050<br>2051<br>2097<br>2103<br>2105<br>2110<br>2111<br>2111<br>2111<br>2112<br>2112<br>2112                                                                                         |
| 13.1.17 CREATE SERVER Statement 13.1.18 CREATE TABLE Statement 13.1.19 CREATE TABLESPACE Statement 13.1.20 CREATE TRIGGER Statement 13.1.21 CREATE VIEW Statement 13.1.22 DROP DATABASE Statement 13.1.23 DROP EVENT Statement 13.1.24 DROP FUNCTION Statement 13.1.25 DROP INDEX Statement 13.1.26 DROP LOGFILE GROUP Statement 13.1.27 DROP PROCEDURE and DROP FUNCTION Statements 13.1.28 DROP SERVER Statement 13.1.29 DROP TABLE Statement                                                                                                                                                                                                                                                                                                                                                                                                                                                | 2050<br>2051<br>2097<br>2103<br>2105<br>2110<br>2111<br>2111<br>2112<br>2112<br>2112<br>2112                                                                                         |
| 13.1.17 CREATE SERVER Statement 13.1.18 CREATE TABLE Statement 13.1.19 CREATE TABLESPACE Statement 13.1.20 CREATE TRIGGER Statement 13.1.21 CREATE VIEW Statement 13.1.22 DROP DATABASE Statement 13.1.23 DROP EVENT Statement 13.1.24 DROP FUNCTION Statement 13.1.25 DROP INDEX Statement 13.1.26 DROP LOGFILE GROUP Statement 13.1.27 DROP PROCEDURE and DROP FUNCTION Statements 13.1.28 DROP SERVER Statement 13.1.29 DROP TABLE Statement 13.1.30 DROP TABLESPACE Statement                                                                                                                                                                                                                                                                                                                                                                                                              | 2050<br>2051<br>2097<br>2103<br>2105<br>2110<br>2111<br>2111<br>2112<br>2112<br>2112<br>2113                                                                                         |
| 13.1.17 CREATE SERVER Statement 13.1.18 CREATE TABLE Statement 13.1.19 CREATE TABLESPACE Statement 13.1.20 CREATE TRIGGER Statement 13.1.21 CREATE VIEW Statement 13.1.22 DROP DATABASE Statement 13.1.23 DROP EVENT Statement 13.1.24 DROP FUNCTION Statement 13.1.25 DROP INDEX Statement 13.1.26 DROP LOGFILE GROUP Statement 13.1.27 DROP PROCEDURE and DROP FUNCTION Statements 13.1.28 DROP SERVER Statement 13.1.29 DROP TABLE Statement 13.1.30 DROP TABLE Statement 13.1.31 DROP TRIGGER Statement                                                                                                                                                                                                                                                                                                                                                                                    | 2050<br>2051<br>2097<br>2103<br>2105<br>2110<br>2111<br>2111<br>2112<br>2112<br>2112<br>2112                                                                                         |
| 13.1.17 CREATE SERVER Statement 13.1.18 CREATE TABLE Statement 13.1.19 CREATE TABLESPACE Statement 13.1.20 CREATE TRIGGER Statement 13.1.21 CREATE VIEW Statement 13.1.22 DROP DATABASE Statement 13.1.23 DROP EVENT Statement 13.1.24 DROP FUNCTION Statement 13.1.25 DROP INDEX Statement 13.1.26 DROP LOGFILE GROUP Statement 13.1.27 DROP PROCEDURE and DROP FUNCTION Statements 13.1.28 DROP SERVER Statement 13.1.29 DROP TABLE Statement 13.1.30 DROP TABLESPACE Statement 13.1.31 DROP TRIGGER Statement 13.1.32 DROP VIEW Statement                                                                                                                                                                                                                                                                                                                                                   | 2050<br>2051<br>2097<br>2103<br>2105<br>2110<br>2111<br>2111<br>2112<br>2112<br>2112<br>2112                                                                                         |
| 13.1.17 CREATE SERVER Statement 13.1.18 CREATE TABLE Statement 13.1.19 CREATE TABLESPACE Statement 13.1.20 CREATE TRIGGER Statement 13.1.21 CREATE VIEW Statement 13.1.22 DROP DATABASE Statement 13.1.23 DROP EVENT Statement 13.1.24 DROP FUNCTION Statement 13.1.25 DROP INDEX Statement 13.1.26 DROP LOGFILE GROUP Statement 13.1.27 DROP PROCEDURE and DROP FUNCTION Statements 13.1.28 DROP SERVER Statement 13.1.29 DROP TABLE Statement 13.1.30 DROP TABLE Statement 13.1.31 DROP TRIGGER Statement 13.1.32 DROP VIEW Statement 13.1.33 RENAME TABLE Statement                                                                                                                                                                                                                                                                                                                         | 2050<br>2051<br>2097<br>2103<br>2105<br>2110<br>2111<br>2111<br>2112<br>2112<br>2112<br>2112                                                                                         |
| 13.1.17 CREATE SERVER Statement 13.1.18 CREATE TABLE Statement 13.1.19 CREATE TABLESPACE Statement 13.1.20 CREATE TRIGGER Statement 13.1.21 CREATE VIEW Statement 13.1.22 DROP DATABASE Statement 13.1.23 DROP EVENT Statement 13.1.24 DROP FUNCTION Statement 13.1.25 DROP INDEX Statement 13.1.25 DROP INDEX Statement 13.1.26 DROP LOGFILE GROUP Statement 13.1.27 DROP PROCEDURE and DROP FUNCTION Statements 13.1.28 DROP SERVER Statement 13.1.29 DROP TABLE Statement 13.1.30 DROP TABLE Statement 13.1.31 DROP TRIGGER Statement 13.1.32 DROP VIEW Statement 13.1.33 RENAME TABLE Statement 13.1.34 TRUNCATE TABLE Statement                                                                                                                                                                                                                                                           | 2050<br>2051<br>2097<br>2103<br>2105<br>2110<br>2111<br>2111<br>2112<br>2112<br>2112<br>2113<br>2114<br>2115<br>2115<br>2116                                                         |
| 13.1.17 CREATE SERVER Statement 13.1.18 CREATE TABLE Statement 13.1.19 CREATE TABLESPACE Statement 13.1.20 CREATE TRIGGER Statement 13.1.21 CREATE VIEW Statement 13.1.22 DROP DATABASE Statement 13.1.23 DROP EVENT Statement 13.1.24 DROP FUNCTION Statement 13.1.25 DROP INDEX Statement 13.1.26 DROP LOGFILE GROUP Statement 13.1.27 DROP PROCEDURE and DROP FUNCTION Statements 13.1.28 DROP SERVER Statement 13.1.29 DROP TABLE Statement 13.1.30 DROP TABLE Statement 13.1.31 DROP TRIGGER Statement 13.1.32 DROP VIEW Statement 13.1.33 RENAME TABLE Statement 13.1.34 TRUNCATE TABLE Statement                                                                                                                                                                                                                                                                                        | 2050<br>2051<br>2097<br>2103<br>2105<br>2110<br>2111<br>2111<br>2112<br>2112<br>2112<br>2113<br>2114<br>2115<br>2116<br>2117                                                         |
| 13.1.17 CREATE SERVER Statement 13.1.18 CREATE TABLE Statement 13.1.19 CREATE TABLESPACE Statement 13.1.20 CREATE TRIGGER Statement 13.1.21 CREATE VIEW Statement 13.1.22 DROP DATABASE Statement 13.1.23 DROP EVENT Statement 13.1.24 DROP FUNCTION Statement 13.1.25 DROP INDEX Statement 13.1.26 DROP LOGFILE GROUP Statement 13.1.27 DROP PROCEDURE and DROP FUNCTION Statements 13.1.28 DROP SERVER Statement 13.1.29 DROP TABLE Statement 13.1.30 DROP TABLE Statement 13.1.31 DROP TRIGGER Statement 13.1.32 DROP VIEW Statement 13.1.33 RENAME TABLE Statement 13.1.34 TRUNCATE TABLE Statement 13.2.1 CALL Statement 13.2.2 Data Manipulation Statements 13.2.1 CALL Statement                                                                                                                                                                                                        | 2050<br>2051<br>2097<br>2103<br>2105<br>2110<br>2111<br>2111<br>2112<br>2112<br>2112<br>2112                                                                                         |
| 13.1.17 CREATE SERVER Statement 13.1.18 CREATE TABLE Statement 13.1.19 CREATE TABLESPACE Statement 13.1.20 CREATE TRIGGER Statement 13.1.21 CREATE VIEW Statement 13.1.22 DROP DATABASE Statement 13.1.23 DROP EVENT Statement 13.1.24 DROP FUNCTION Statement 13.1.25 DROP INDEX Statement 13.1.26 DROP LOGFILE GROUP Statement 13.1.27 DROP PROCEDURE and DROP FUNCTION Statements 13.1.28 DROP SERVER Statement 13.1.29 DROP TABLE Statement 13.1.30 DROP TABLE Statement 13.1.31 DROP TRIGGER Statement 13.1.32 DROP VIEW Statement 13.1.33 RENAME TABLE Statement 13.1.34 TRUNCATE TABLE Statement 13.2.2 Data Manipulation Statements 13.2.1 CALL Statement 13.2.2 DELETE Statement                                                                                                                                                                                                      | 2050<br>2051<br>2097<br>2103<br>2105<br>2110<br>2111<br>2111<br>2112<br>2112<br>2112<br>2112                                                                                         |
| 13.1.17 CREATE SERVER Statement 13.1.18 CREATE TABLE Statement 13.1.19 CREATE TABLESPACE Statement 13.1.20 CREATE TRIGGER Statement 13.1.21 CREATE VIEW Statement 13.1.22 DROP DATABASE Statement 13.1.23 DROP EVENT Statement 13.1.24 DROP FUNCTION Statement 13.1.25 DROP INDEX Statement 13.1.26 DROP LOGFILE GROUP Statement 13.1.27 DROP PROCEDURE and DROP FUNCTION Statements 13.1.28 DROP SERVER Statement 13.1.29 DROP TABLE Statement 13.1.30 DROP TABLE Statement 13.1.31 DROP TRIGGER Statement 13.1.32 DROP VIEW Statement 13.1.33 RENAME TABLE Statement 13.1.34 TRUNCATE TABLE Statement 13.2.2 Data Manipulation Statements 13.2.1 CALL Statement 13.2.2 DELETE Statement 13.2.3 DO Statement                                                                                                                                                                                  | 2050<br>2051<br>2097<br>2103<br>2105<br>2110<br>2111<br>2111<br>2112<br>2112<br>2112<br>2113<br>2114<br>2115<br>2116<br>2117<br>2117<br>2119<br>2122                                 |
| 13.1.17 CREATE SERVER Statement 13.1.18 CREATE TABLE Statement 13.1.19 CREATE TABLESPACE Statement 13.1.20 CREATE TRIGGER Statement 13.1.21 CREATE VIEW Statement 13.1.22 DROP DATABASE Statement 13.1.23 DROP EVENT Statement 13.1.24 DROP FUNCTION Statement 13.1.25 DROP INDEX Statement 13.1.26 DROP LOGFILE GROUP Statement 13.1.27 DROP PROCEDURE and DROP FUNCTION Statements 13.1.28 DROP SERVER Statement 13.1.29 DROP TABLE Statement 13.1.30 DROP TABLE Statement 13.1.31 DROP TRIGGER Statement 13.1.32 DROP VIEW Statement 13.1.33 RENAME TABLE Statement 13.1.34 TRUNCATE TABLE Statement 13.1.3 Data Manipulation Statements 13.2 Data Manipulation Statements 13.2.1 CALL Statement 13.2.2 DELETE Statement 13.2.3 DO Statement 13.2.3 DO Statement 13.2.4 HANDLER Statement                                                                                                   | 2050<br>2051<br>2097<br>2103<br>2105<br>2110<br>2111<br>2111<br>2112<br>2112<br>2112<br>2113<br>2114<br>2115<br>2115<br>2116<br>2117<br>2119<br>2122<br>2123                         |
| 13.1.17 CREATE SERVER Statement 13.1.18 CREATE TABLE Statement 13.1.19 CREATE TABLESPACE Statement 13.1.20 CREATE TRIGGER Statement 13.1.21 CREATE VIEW Statement 13.1.22 DROP DATABASE Statement 13.1.23 DROP EVENT Statement 13.1.24 DROP FUNCTION Statement 13.1.25 DROP INDEX Statement 13.1.26 DROP LOGFILE GROUP Statement 13.1.27 DROP PROCEDURE and DROP FUNCTION Statements 13.1.28 DROP SERVER Statement 13.1.29 DROP TABLE Statement 13.1.30 DROP TABLE Statement 13.1.31 DROP TRIGGER Statement 13.1.32 DROP VIEW Statement 13.1.33 TRINCATE TABLE Statement 13.1.34 TRUNCATE TABLE Statement 13.2 Data Manipulation Statements 13.2.1 CALL Statement 13.2.2 DELETE Statement 13.2.3 DO Statement 13.2.4 HANDLER Statement 13.2.5 INSERT Statement                                                                                                                                 | 2050<br>2051<br>2097<br>2103<br>2105<br>2110<br>2111<br>2111<br>2112<br>2112<br>2112<br>2113<br>2114<br>2115<br>2115<br>2116<br>2117<br>2119<br>2122<br>2123<br>2124                 |
| 13.1.17 CREATE SERVER Statement 13.1.18 CREATE TABLE Statement 13.1.19 CREATE TABLESPACE Statement 13.1.20 CREATE TRIGGER Statement 13.1.21 CREATE VIEW Statement 13.1.22 DROP DATABASE Statement 13.1.23 DROP EVENT Statement 13.1.24 DROP FUNCTION Statement 13.1.25 DROP INDEX Statement 13.1.26 DROP LOGFILE GROUP Statement 13.1.27 DROP PROCEDURE and DROP FUNCTION Statements 13.1.28 DROP SERVER Statement 13.1.29 DROP TABLE Statement 13.1.30 DROP TABLE Statement 13.1.31 DROP TRIGGER Statement 13.1.32 DROP VIEW Statement 13.1.33 RENAME TABLE Statement 13.1.34 TRUNCATE TABLE Statement 13.1.35 Data Manipulation Statements 13.2.1 CALL Statement 13.2.2 DELETE Statement 13.2.3 DO Statement 13.2.4 HANDLER Statement 13.2.5 INSERT Statement 13.2.5 INSERT Statement                                                                                                        | 2050<br>2051<br>2097<br>2103<br>2105<br>2110<br>2111<br>2111<br>2112<br>2112<br>2112<br>2115<br>2115                                                                                 |
| 13.1.17 CREATE SERVER Statement         13.1.18 CREATE TABLE Statement         13.1.20 CREATE TRIGGER Statement         13.1.21 CREATE VIEW Statement         13.1.22 DROP DATABASE Statement         13.1.23 DROP EVENT Statement         13.1.24 DROP FUNCTION Statement         13.1.25 DROP INDEX Statement         13.1.26 DROP LOGFILE GROUP Statement         13.1.27 DROP PROCEDURE and DROP FUNCTION Statements         13.1.28 DROP SERVER Statement         13.1.30 DROP TABLE Statement         13.1.31 DROP TRIGGER Statement         13.1.32 DROP VIEW Statement         13.1.33 RENAME TABLE Statement         13.1.34 TRUNCATE TABLE Statement         13.2.1 CALL Statement         13.2.2 DELETE Statement         13.2.3 DO Statement         13.2.4 HANDLER Statement         13.2.5 INSERT Statement         13.2.6 LOAD DATA Statement         13.2.7 LOAD XML Statement | 2050<br>2051<br>2097<br>2103<br>2105<br>2110<br>2111<br>2111<br>2112<br>2112<br>2112<br>2113<br>2114<br>2115<br>2116<br>2117<br>2117<br>2119<br>2122<br>2123<br>2124<br>2132<br>2143 |
| 13.1.17 CREATE SERVER Statement 13.1.18 CREATE TABLE Statement 13.1.19 CREATE TABLESPACE Statement 13.1.20 CREATE TRIGGER Statement 13.1.21 CREATE VIEW Statement 13.1.22 DROP DATABASE Statement 13.1.23 DROP EVENT Statement 13.1.24 DROP FUNCTION Statement 13.1.25 DROP INDEX Statement 13.1.26 DROP LOGFILE GROUP Statement 13.1.27 DROP PROCEDURE and DROP FUNCTION Statements 13.1.28 DROP SERVER Statement 13.1.29 DROP TABLE Statement 13.1.30 DROP TABLE Statement 13.1.31 DROP TRIGGER Statement 13.1.32 DROP VIEW Statement 13.1.33 RENAME TABLE Statement 13.1.34 TRUNCATE TABLE Statement 13.1.35 Data Manipulation Statements 13.2.1 CALL Statement 13.2.2 DELETE Statement 13.2.3 DO Statement 13.2.4 HANDLER Statement 13.2.5 INSERT Statement 13.2.5 INSERT Statement                                                                                                        | 2050<br>2051<br>2097<br>2103<br>2105<br>2110<br>2111<br>2111<br>2112<br>2112<br>2112<br>2113<br>2114<br>2115<br>2116<br>2117<br>2117<br>2119<br>2122<br>2123<br>2124<br>2132<br>2143 |

|           | 13.2.10 Subqueries                                               |        |
|-----------|------------------------------------------------------------------|--------|
|           | 13.2.11 UPDATE Statement                                         | . 2181 |
| 13.3      | Transactional and Locking Statements                             | . 2184 |
|           | 13.3.1 START TRANSACTION, COMMIT, and ROLLBACK Statements        | . 2184 |
|           | 13.3.2 Statements That Cannot Be Rolled Back                     | . 2187 |
|           | 13.3.3 Statements That Cause an Implicit Commit                  | . 2187 |
|           | 13.3.4 SAVEPOINT, ROLLBACK TO SAVEPOINT, and RELEASE SAVEPOINT   |        |
|           | Statements                                                       |        |
|           | 13.3.5 LOCK TABLES and UNLOCK TABLES Statements                  |        |
|           | 13.3.6 SET TRANSACTION Statement                                 |        |
|           | 13.3.7 XA Transactions                                           |        |
| 13.4      | Replication Statements                                           |        |
|           | 13.4.1 SQL Statements for Controlling Replication Source Servers |        |
|           | 13.4.2 SQL Statements for Controlling Replica Servers            |        |
|           | 13.4.3 SQL Statements for Controlling Group Replication          |        |
| 13.5      | Prepared Statements                                              |        |
|           | 13.5.1 PREPARE Statement                                         |        |
|           | 13.5.2 EXECUTE Statement                                         |        |
|           | 13.5.3 DEALLOCATE PREPARE Statement                              |        |
| 13.6      | Compound Statements                                              |        |
|           | 13.6.1 BEGIN END Compound Statement                              |        |
|           | 13.6.2 Statement Labels                                          |        |
|           | 13.6.3 DECLARE Statement                                         |        |
|           | 13.6.4 Variables in Stored Programs                              |        |
|           | 13.6.5 Flow Control Statements                                   |        |
|           | 13.6.6 Cursors                                                   |        |
|           | 13.6.7 Condition Handling                                        | 2235   |
| 13.7      | Database Administration Statements                               | . 2261 |
|           | 13.7.1 Account Management Statements                             | . 2261 |
|           | 13.7.2 Table Maintenance Statements                              | . 2289 |
|           | 13.7.3 Plugin and Loadable Function Statements                   | . 2300 |
|           | 13.7.4 SET Statements                                            | . 2303 |
|           | 13.7.5 SHOW Statements                                           | 2307   |
|           | 13.7.6 Other Administrative Statements                           |        |
| 13.8      | Utility Statements                                               | . 2368 |
|           | 13.8.1 DESCRIBE Statement                                        |        |
|           | 13.8.2 EXPLAIN Statement                                         | 2368   |
|           | 13.8.3 HELP Statement                                            | . 2370 |
|           | 13.8.4 USE Statement                                             | . 2372 |
| 14 The In | noDB Storage Engine                                              | . 2373 |
| 14.1      | Introduction to InnoDB                                           | . 2374 |
|           | 14.1.1 Benefits of Using InnoDB Tables                           | . 2376 |
|           | 14.1.2 Best Practices for InnoDB Tables                          |        |
|           | 14.1.3 Verifying that InnoDB is the Default Storage Engine       | . 2377 |
|           | 14.1.4 Testing and Benchmarking with InnoDB                      |        |
|           | 14.1.5 Turning Off InnoDB                                        |        |
| 14.2      | InnoDB and the ACID Model                                        |        |
|           | InnoDB Multi-Versioning                                          |        |
|           | InnoDB Architecture                                              |        |
|           | InnoDB In-Memory Structures                                      |        |
|           | 14.5.1 Buffer Pool                                               |        |
|           | 14.5.2 Change Buffer                                             |        |
|           | 14.5.3 Adaptive Hash Index                                       |        |
|           | 14.5.4 Log Buffer                                                |        |
| 14.6      | InnoDB On-Disk Structures                                        |        |
|           | 14.6.1 Tables                                                    |        |
|           | 14.6.2 Indexes                                                   |        |
|           | 14.6.3 Tablespaces                                               |        |
|           | •                                                                |        |

| 14.6.4 InnoDB Data Dictionary 2436                                         |      |
|----------------------------------------------------------------------------|------|
| 14.6.5 Doublewrite Buffer 2436                                             |      |
| 14.6.6 Redo Log 2436                                                       |      |
| 14.6.7 Undo Logs                                                           | 2437 |
| 14.7 InnoDB Locking and Transaction Model 2438                             |      |
| 14.7.1 InnoDB Locking 2439                                                 |      |
| 14.7.2 InnoDB Transaction Model 2443                                       |      |
| 14.7.3 Locks Set by Different SQL Statements in InnoDB 2450                |      |
| 14.7.4 Phantom Rows 2454                                                   |      |
| 14.7.5 Deadlocks in InnoDB 2454                                            |      |
| 14.8 InnoDB Configuration 2457                                             |      |
| 14.8.1 InnoDB Startup Configuration 2457                                   |      |
| 14.8.2 Configuring InnoDB for Read-Only Operation 2463                     |      |
| 14.8.3 InnoDB Buffer Pool Configuration 2464                               |      |
| 14.8.4 Configuring the Memory Allocator for InnoDB 2476                    |      |
| 14.8.5 Configuring Thread Concurrency for InnoDB 2477                      |      |
| 14.8.6 Configuring the Number of Background InnoDB I/O Threads 2478        |      |
| 14.8.7 Using Asynchronous I/O on Linux 2478                                |      |
| 14.8.8 Configuring InnoDB I/O Capacity 2479                                |      |
| 14.8.9 Configuring Spin Lock Polling 2480                                  |      |
| 14.8.10 Purge Configuration 2481                                           |      |
| 14.8.11 Configuring Optimizer Statistics for InnoDB 2482                   |      |
|                                                                            |      |
| 14.8.12 Configuring the Merge Threshold for Index Pages                    | 2493 |
| 14.9 InnoDB Table and Page Compression 2495                                |      |
| 14.9.1 InnoDB Table Compression 2496                                       |      |
| 14.9.2 InnoDB Page Compression 2510                                        |      |
| 14.10 InnoDB File-Format Management 2513                                   |      |
| 14.10.1 Enabling File Formats 2514                                         |      |
| 14.10.2 Verifying File Format Compatibility 2514                           |      |
| 14.10.3 Identifying the File Format in Use 2517                            |      |
| 14.10.4 Modifying the File Format 2518                                     |      |
| 14.11 InnoDB Row Formats                                                   | 2518 |
| 14.12 InnoDB Disk I/O and File Space Management                            | 2525 |
| 14.12.1 InnoDB Disk I/O 2525                                               |      |
| 14.12.2 File Space Management                                              | 2526 |
| 14.12.3 InnoDB Checkpoints                                                 | 2527 |
| 14.12.4 Defragmenting a Table 2527                                         |      |
| 14.12.5 Reclaiming Disk Space with TRUNCATE TABLE 2528                     |      |
| 14.13 InnoDB and Online DDL 2528                                           |      |
| 14.13.1 Online DDL Operations 2529                                         |      |
| 14.13.2 Online DDL Performance and Concurrency 2541                        |      |
| 14.13.3 Online DDL Space Requirements 2544                                 |      |
| 14.13.4 Simplifying DDL Statements with Online DDL 2545                    |      |
| 14.13.5 Online DDL Failure Conditions                                      | 2545 |
| 14.13.6 Online DDL Limitations 2546                                        |      |
| 14.14 InnoDB Data-at-Rest Encryption 2547                                  |      |
| 14.15 InnoDB Startup Options and System Variables 2551                     |      |
| 14.16 InnoDB INFORMATION_SCHEMA Tables 2629                                |      |
| 14.16.1 InnoDB INFORMATION_SCHEMA Tables about Compression 2629            |      |
| 14.16.2 InnoDB INFORMATION_SCHEMA Transaction and Locking Information 2631 |      |
| 14.16.3 InnoDB INFORMATION_SCHEMA System Tables                            | 2638 |
| 14.16.4 InnoDB INFORMATION_SCHEMA FULLTEXT Index Tables 2643               |      |
| 14.16.5 InnoDB INFORMATION_SCHEMA Buffer Pool Tables 2646                  |      |
| 14.16.6 InnoDB INFORMATION_SCHEMA Metrics Table                            | 2650 |
| 14.16.7 InnoDB INFORMATION_SCHEMA Temporary Table Info Table               | 2658 |
| 14.16.8 Retrieving InnoDB Tablespace Metadata from                         |      |
| INFORMATION_SCHEMA.FILES 2659                                              |      |
| 14.17 InnoDB Integration with MySQL Performance Schema                     | 2661 |
|                                                                            |      |

| 14.17.1 Monitoring ALTER TABLE Progress for InnoDB Tables Using Performance |      |
|-----------------------------------------------------------------------------|------|
| Schema 2662                                                                 |      |
| 14.17.2 Monitoring InnoDB Mutex Waits Using Performance Schema 2664         |      |
| 14.18 InnoDB Monitors 2668                                                  |      |
| 14.18.1 InnoDB Monitor Types                                                | 2668 |
| 14.18.2 Enabling InnoDB Monitors 2668                                       |      |
| 14.18.3 InnoDB Standard Monitor and Lock Monitor Output                     | 2670 |
| 14.19 InnoDB Backup and Recovery 2675                                       |      |
| 14.19.1 InnoDB Backup 2675                                                  |      |
| 14.19.2 InnoDB Recovery 2676                                                |      |
| 14.20 InnoDB and MySQL Replication 2679                                     |      |
| 14.21 InnoDB memcached Plugin 2680                                          |      |
| 14.21.1 Benefits of the InnoDB memcached Plugin 2681                        |      |
| 14.21.2 InnoDB memcached Architecture 2682                                  |      |
| 14.21.3 Setting Up the InnoDB memcached Plugin 2683                         |      |
| 14.21.4 Security Considerations for the InnoDB memcached Plugin 2688        |      |
| 14.21.5 Writing Applications for the InnoDB memcached Plugin 2690           |      |
| 14.21.6 The InnoDB memcached Plugin and Replication 2702                    |      |
| 14.21.7 InnoDB memcached Plugin Internals 2705                              |      |
| 14.21.8 Troubleshooting the InnoDB memcached Plugin 2710                    |      |
| 14.22 InnoDB Troubleshooting 2712                                           |      |
| 14.22.1 Troubleshooting InnoDB I/O Problems 2713                            |      |
| 14.22.2 Forcing InnoDB Recovery                                             | 2713 |
| 14.22.3 Troubleshooting InnoDB Data Dictionary Operations 2715              |      |
| 14.22.4 InnoDB Error Handling 2719                                          |      |
| 14.23 InnoDB Limits 2719                                                    |      |
| 14.24 InnoDB Restrictions and Limitations                                   | 2721 |
| 15 Alternative Storage Engines 2723                                         |      |
| 15.1 Setting the Storage Engine 2726                                        |      |
| 15.2 The MyISAM Storage Engine 2727                                         |      |
| 15.2.1 MyISAM Startup Options 2729                                          |      |
| 15.2.2 Space Needed for Keys 2731                                           |      |
| 15.2.3 MyISAM Table Storage Formats 2731                                    |      |
| 15.2.4 MyISAM Table Problems 2734                                           |      |
| 15.3 The MEMORY Storage Engine                                              | 2735 |
| 15.4 The CSV Storage Engine                                                 | 2739 |
| 15.4.1 Repairing and Checking CSV Tables 2740                               |      |
| 15.4.2 CSV Limitations 2741                                                 |      |
| 15.5 The ARCHIVE Storage Engine 2741                                        |      |
| 15.6 The BLACKHOLE Storage Engine                                           | 2742 |
| 15.7 The MERGE Storage Engine 2745                                          |      |
| 15.7.1 MERGE Table Advantages and Disadvantages 2747                        |      |
| 15.7.2 MERGE Table Problems 2748                                            |      |
| 15.8 The FEDERATED Storage Engine 2749                                      |      |
|                                                                             |      |
| 15.8.1 FEDERATED Storage Engine Overview 2750                               |      |
| 15.8.2 How to Create FEDERATED Tables 2751                                  |      |
| 15.8.3 FEDERATED Storage Engine Notes and Tips 2753                         |      |
| 15.8.4 FEDERATED Storage Engine Resources 2755                              |      |
| 15.9 The EXAMPLE Storage Engine 2755                                        |      |
| 15.10 Other Storage Engines 2755                                            |      |
| 15.11 Overview of MySQL Storage Engine Architecture 2755                    |      |
| 15.11.1 Pluggable Storage Engine Architecture 2756                          |      |
| 15.11.2 The Common Database Server Layer 2756                               |      |
| 16 Replication 2759                                                         |      |
| 16.1 Configuring Replication 2760                                           |      |
| 16.1.1 Binary Log File Position Based Replication Configuration Overview    | 2761 |
| 16.1.2 Setting Up Binary Log File Position Based Replication 2761           |      |
| 16.1.3 Replication with Global Transaction Identifiers 2771                 |      |

| 16.1.4 Changing Replication Modes on Online Servers 2791                        |      |
|---------------------------------------------------------------------------------|------|
| 16.1.5 MySQL Multi-Source Replication                                           | 2797 |
| 16.1.6 Replication and Binary Logging Options and Variables 2802                |      |
| 16.1.7 Common Replication Administration Tasks 2877                             |      |
| 16.2 Replication Implementation 2883                                            |      |
| 16.2.1 Replication Formats 2883                                                 |      |
| 16.2.2 Replication Channels 2890                                                |      |
| 16.2.3 Replication Threads 2894                                                 |      |
| 16.2.4 Relay Log and Replication Metadata Repositories 2896                     |      |
| 16.2.5 How Servers Evaluate Replication Filtering Rules 2902                    |      |
| 16.3 Replication Solutions 2908                                                 |      |
| 16.3.1 Using Replication for Backups 2909                                       |      |
| 16.3.2 Handling an Unexpected Halt of a Replica 2912                            |      |
| 16.3.3 Using Replication with Different Source and Replica Storage Engines 2914 |      |
|                                                                                 |      |
| 16.3.4 Using Replication for Scale-Out 2915                                     |      |
| 16.3.5 Replicating Different Databases to Different Replicas 2917               |      |
| 16.3.6 Improving Replication Performance 2918                                   |      |
| 16.3.7 Switching Sources During Failover                                        | 2919 |
| 16.3.8 Setting Up Replication to Use Encrypted Connections                      | 2921 |
| 16.3.9 Semisynchronous Replication 2922                                         |      |
| 16.3.10 Delayed Replication 2928                                                |      |
| 16.4 Replication Notes and Tips 2929                                            |      |
| 16.4.1 Replication Features and Issues 2929                                     |      |
| 16.4.2 Replication Compatibility Between MySQL Versions 2953                    |      |
| 16.4.3 Upgrading a Replication Topology 2954                                    |      |
| 16.4.4 Troubleshooting Replication                                              | 2956 |
| 16.4.5 How to Report Replication Bugs or Problems 2957                          |      |
| 17 Group Replication                                                            | 2959 |
| 17.1 Group Replication Background 2960                                          |      |
| 17.1.1 Replication Technologies 2961                                            |      |
| 17.1.2 Group Replication Use Cases 2963                                         |      |
| 17.1.3 Group Replication Details 2964                                           |      |
| 17.2 Getting Started 2966                                                       |      |
| 17.2.1 Deploying Group Replication in Single-Primary Mode 2966                  |      |
| 17.2.2 Deploying Group Replication Locally 2976                                 |      |
| 17.3 Requirements and Limitations 2978                                          |      |
| 17.3.1 Group Replication Requirements 2978                                      |      |
| 17.3.2 Group Replication Limitations 2980                                       |      |
| 17.4 Monitoring Group Replication 2982                                          |      |
| 17.4.1 Group Replication Server States 2982                                     |      |
| 17.4.2 The replication_group_members Table                                      | 2983 |
| 17.4.3 The replication_group_member_stats Table 2984                            |      |
| 17.5 Group Replication Operations 2984                                          |      |
| 17.5.1 Deploying in Multi-Primary or Single-Primary Mode 2984                   |      |
|                                                                                 |      |
| 17.5.2 Tuning Recovery                                                          | 2986 |
| 17.5.3 Network Partitioning 2987                                                |      |
| 17.5.4 Restarting a Group 2992                                                  |      |
| 17.5.5 Using MySQL Enterprise Backup with Group Replication 2994                |      |
| 17.6 Group Replication Security 2999                                            |      |
| 17.6.1 Group Replication IP Address Allowlisting 2999                           |      |
| 17.6.2 Group Replication Secure Socket Layer (SSL) Support 3000                 |      |
| 17.6.3 Group Replication and Virtual Private Networks (VPNs) 3002               |      |
| 17.7 Group Replication Variables 3002                                           |      |
| 17.7.1 Group Replication System Variables 3003                                  |      |
| 17.7.2 Group Replication Status Variables 3022                                  |      |
| 17.8 Frequently Asked Questions 3022                                            |      |
| 17.9 Group Replication Technical Details 3026                                   |      |
| 17.9.1 Group Replication Plugin Architecture 3026                               |      |

| 17.9.2 The Group 3028                                                                |      |
|--------------------------------------------------------------------------------------|------|
| 17.9.3 Data Manipulation Statements 3028                                             |      |
| 17.9.4 Data Definition Statements 3028                                               |      |
| 17.9.5 Distributed Recovery 3029                                                     |      |
| 17.9.6 Observability 3035                                                            |      |
| 17.9.7 Group Replication Performance 3036                                            |      |
| 18 MySQL Shell 3041                                                                  |      |
| 19 Using MySQL as a Document Store                                                   | 3043 |
| 19.1 Key Concepts 3044                                                               |      |
| 19.2 Setting Up MySQL as a Document Store 3045                                       |      |
| 19.2.1 Installing MySQL Shell 3047                                                   |      |
| 19.2.2 Starting MySQL Shell 3050                                                     |      |
| 19.3 Quick-Start Guide: MySQL for Visual Studio 3051                                 |      |
| 19.4 X Plugin 3052                                                                   |      |
|                                                                                      |      |
| 19.4.1 Using Encrypted Connections with X Plugin 3052                                |      |
| 19.4.2 X Plugin Options and Variables 3053                                           |      |
| 19.4.3 Monitoring X Plugin                                                           | 3065 |
| 20 InnoDB Cluster 3067                                                               |      |
| 21 MySQL NDB Cluster 7.5 and NDB Cluster 7.6                                         | 3069 |
| 21.1 General Information 3070                                                        |      |
| 21.2 NDB Cluster Overview 3073                                                       |      |
| 21.2.1 NDB Cluster Core Concepts 3074                                                |      |
| 21.2.2 NDB Cluster Nodes, Node Groups, Fragment Replicas, and Partitions 3077        |      |
| 21.2.3 NDB Cluster Hardware, Software, and Networking Requirements 3080              |      |
| 21.2.4 What is New in MySQL NDB Cluster 3081                                         |      |
| 21.2.5 NDB: Added, Deprecated, and Removed Options, Variables, and Parameters 3097   |      |
| 21.2.6 MySQL Server Using InnoDB Compared with NDB Cluster 3101                      |      |
| 21.2.7 Known Limitations of NDB Cluster 3104                                         |      |
| 21.3 NDB Cluster Installation 3116                                                   |      |
| 21.3.1 Installation of NDB Cluster on Linux 3118                                     |      |
| 21.3.2 Installing NDB Cluster on Windows                                             | 3126 |
| 21.3.3 Initial Configuration of NDB Cluster                                          | 3134 |
| 21.3.4 Initial Startup of NDB Cluster 3136                                           |      |
| 21.3.5 NDB Cluster Example with Tables and Data 3137                                 |      |
| 21.3.6 Safe Shutdown and Restart of NDB Cluster 3140                                 |      |
| 21.3.7 Upgrading and Downgrading NDB Cluster                                         | 3141 |
| 21.3.8 The NDB Cluster Auto-Installer (NDB 7.5) (NO LONGER SUPPORTED) 3144           |      |
| 21.3.9 The NDB Cluster Auto-Installer (NO LONGER SUPPORTED) 3144                     |      |
| 21.4 Configuration of NDB Cluster 3145                                               |      |
| 21.4.1 Quick Test Setup of NDB Cluster 3145                                          |      |
| 21.4.2 Overview of NDB Cluster Configuration Parameters, Options, and Variables 3147 |      |
| 21.4.3 NDB Cluster Configuration Files 3165                                          |      |
| 21.4.4 Using High-Speed Interconnects with NDB Cluster 3344                          |      |
| 21.5 NDB Cluster Programs 3344                                                       |      |
| 21.5.1 ndbd — The NDB Cluster Data Node Daemon 3344                                  |      |
| 21.5.2 ndbinfo_select_all — Select From ndbinfo Tables 3354                          |      |
| 21.5.3 ndbmtd — The NDB Cluster Data Node Daemon (Multi-Threaded) 3360               |      |
| 21.5.4 ndb_mgmd — The NDB Cluster Management Server Daemon 3361                      |      |
| 21.5.5 ndb_mgm — The NDB Cluster Management Client 3372                              |      |
| 21.5.6 ndb_blob_tool — Check and Repair BLOB and TEXT columns of NDB Cluster         |      |
| Tables 3377                                                                          |      |
|                                                                                      |      |
| 21.5.7 ndb_config — Extract NDB Cluster Configuration Information 3383               |      |
| 21.5.8 ndb_cpcd — Automate Testing for NDB Development 3394                          |      |
| 21.5.9 ndb_delete_all — Delete All Rows from an NDB Table 3394                       |      |
| 21.5.10 ndb_desc — Describe NDB Tables 3399                                          |      |
| 21.5.11 ndb_drop_index — Drop Index from an NDB Table 3408                           |      |
| 21.5.12 ndb_drop_table — Drop an NDB Table 3413                                      |      |
| 21.5.13 ndb_error_reporter — NDB Error-Reporting Utility 3417                        |      |

| 21.5.14 ndb_import — Import CSV Data Into NDB 3418                             |      |
|--------------------------------------------------------------------------------|------|
| 21.5.15 ndb_index_stat — NDB Index Statistics Utility 3434                     |      |
| 21.5.16 ndb_move_data — NDB Data Copy Utility                                  | 3442 |
| 21.5.17 ndb_perror — Obtain NDB Error Message Information 3447                 |      |
| 21.5.18 ndb_print_backup_file — Print NDB Backup File Contents 3449            |      |
| 21.5.19 ndb_print_file — Print NDB Disk Data File Contents                     | 3449 |
| 21.5.20 ndb_print_frag_file — Print NDB Fragment List File Contents 3450       |      |
| 21.5.21 ndb_print_schema_file — Print NDB Schema File Contents 3451            |      |
| 21.5.22 ndb_print_sys_file — Print NDB System File Contents 3451               |      |
| 21.5.23 ndb_redo_log_reader — Check and Print Content of Cluster Redo Log 3452 |      |
| 21.5.24 ndb_restore — Restore an NDB Cluster Backup 3454                       |      |
| 21.5.25 ndb_select_all — Print Rows from an NDB Table 3482                     |      |
| 21.5.26 ndb_select_count — Print Row Counts for NDB Tables 3489                |      |
| 21.5.27 ndb_show_tables — Display List of NDB Tables 3493                      |      |
| 21.5.28 ndb_size.pl — NDBCLUSTER Size Requirement Estimator 3498               |      |
| 21.5.29 ndb_top — View CPU usage information for NDB threads 3500              |      |
| 21.5.30 ndb_waiter — Wait for NDB Cluster to Reach a Given Status 3506         |      |
|                                                                                |      |
| 21.6 Management of NDB Cluster 3512                                            |      |
| 21.6.1 Commands in the NDB Cluster Management Client 3513                      |      |
| 21.6.2 NDB Cluster Log Messages 3519                                           |      |
| 21.6.3 Event Reports Generated in NDB Cluster 3537                             |      |
| 21.6.4 Summary of NDB Cluster Start Phases 3549                                |      |
| 21.6.5 Performing a Rolling Restart of an NDB Cluster 3551                     |      |
| 21.6.6 NDB Cluster Single User Mode 3553                                       |      |
| 21.6.7 Adding NDB Cluster Data Nodes Online 3554                               |      |
| 21.6.8 Online Backup of NDB Cluster 3564                                       |      |
| 21.6.9 Importing Data Into MySQL Cluster 3569                                  |      |
| 21.6.10 MySQL Server Usage for NDB Cluster 3570                                |      |
| 21.6.11 NDB Cluster Disk Data Tables 3571                                      |      |
| 21.6.12 Online Operations with ALTER TABLE in NDB Cluster 3577                 |      |
| 21.6.13 Distributed Privileges Using Shared Grant Tables 3580                  |      |
| 21.6.14 NDB API Statistics Counters and Variables 3583                         |      |
| 21.6.15 ndbinfo: The NDB Cluster Information Database 3594                     |      |
| 21.6.16 INFORMATION_SCHEMA Tables for NDB Cluster 3663                         |      |
| 21.6.17 Quick Reference: NDB Cluster SQL Statements 3664                       |      |
| 21.6.18 NDB Cluster Security Issues 3672                                       |      |
| 21.7 NDB Cluster Replication 3678                                              |      |
| 21.7.1 NDB Cluster Replication: Abbreviations and Symbols 3680                 |      |
| 21.7.2 General Requirements for NDB Cluster Replication 3680                   |      |
| 21.7.3 Known Issues in NDB Cluster Replication 3682                            |      |
| 21.7.4 NDB Cluster Replication Schema and Tables 3688                          |      |
| 21.7.5 Preparing the NDB Cluster for Replication                               | 3695 |
| 21.7.6 Starting NDB Cluster Replication (Single Replication Channel) 3697      |      |
| 21.7.7 Using Two Replication Channels for NDB Cluster Replication 3698         |      |
| 21.7.8 Implementing Failover with NDB Cluster Replication 3699                 |      |
| 21.7.9 NDB Cluster Backups With NDB Cluster Replication 3701                   |      |
| 21.7.10 NDB Cluster Replication: Bidirectional and Circular Replication 3707   |      |
|                                                                                |      |
| 21.7.11 NDB Cluster Replication Conflict Resolution 3711                       |      |
| 21.8 NDB Cluster Release Notes 3723                                            |      |
| 22 Partitioning 3725                                                           |      |
| 22.1 Overview of Partitioning in MySQL 3727                                    |      |
| 22.2 Partitioning Types 3730                                                   |      |
| 22.2.1 RANGE Partitioning 3731                                                 |      |
| 22.2.2 LIST Partitioning 3735                                                  |      |
| 22.2.3 COLUMNS Partitioning                                                    | 3738 |
| 22.2.4 HASH Partitioning 3745                                                  |      |
| 22.2.5 KEY Partitioning 3748                                                   |      |
| 22.2.6 Subpartitioning 3749                                                    |      |
|                                                                                |      |

| 22.2.7 How MySQL Partitioning Handles NULL 3752                          |      |
|--------------------------------------------------------------------------|------|
| 22.3 Partition Management 3757                                           |      |
| 22.3.1 Management of RANGE and LIST Partitions 3758                      |      |
| 22.3.2 Management of HASH and KEY Partitions 3763                        |      |
| 22.3.3 Exchanging Partitions and Subpartitions with Tables 3764          |      |
|                                                                          |      |
| 22.3.4 Maintenance of Partitions 3771                                    |      |
| 22.3.5 Obtaining Information About Partitions 3773                       |      |
| 22.4 Partition Pruning 3775                                              |      |
| 22.5 Partition Selection 3778                                            |      |
| 22.6 Restrictions and Limitations on Partitioning 3783                   |      |
| 22.6.1 Partitioning Keys, Primary Keys, and Unique Keys 3790             |      |
| 22.6.2 Partitioning Limitations Relating to Storage Engines 3794         |      |
| 22.6.3 Partitioning Limitations Relating to Functions 3795               |      |
| 22.6.4 Partitioning and Locking 3796                                     |      |
| 23 Stored Objects 3799                                                   |      |
| 23.1 Defining Stored Programs 3800                                       |      |
| 23.2 Using Stored Routines 3801                                          |      |
|                                                                          |      |
| 23.2.1 Stored Routine Syntax 3802                                        |      |
| 23.2.2 Stored Routines and MySQL Privileges                              | 3802 |
| 23.2.3 Stored Routine Metadata 3803                                      |      |
| 23.2.4 Stored Procedures, Functions, Triggers, and LAST_INSERT_ID() 3803 |      |
| 23.3 Using Triggers 3803                                                 |      |
| 23.3.1 Trigger Syntax and Examples 3804                                  |      |
| 23.3.2 Trigger Metadata 3808                                             |      |
| 23.4 Using the Event Scheduler                                           | 3808 |
| 23.4.1 Event Scheduler Overview 3808                                     |      |
| 23.4.2 Event Scheduler Configuration 3809                                |      |
| 23.4.3 Event Syntax 3811                                                 |      |
| 23.4.4 Event Metadata 3812                                               |      |
|                                                                          |      |
| 23.4.5 Event Scheduler Status 3812                                       |      |
| 23.4.6 The Event Scheduler and MySQL Privileges 3813                     |      |
| 23.5 Using Views 3816                                                    |      |
| 23.5.1 View Syntax 3816                                                  |      |
| 23.5.2 View Processing Algorithms 3816                                   |      |
| 23.5.3 Updatable and Insertable Views 3817                               |      |
| 23.5.4 The View WITH CHECK OPTION Clause 3820                            |      |
| 23.5.5 View Metadata 3821                                                |      |
| 23.6 Stored Object Access Control 3821                                   |      |
| 23.7 Stored Program Binary Logging 3825                                  |      |
| 23.8 Restrictions on Stored Programs 3830                                |      |
| 23.9 Restrictions on Views 3834                                          |      |
| 24 INFORMATION_SCHEMA Tables 3837                                        |      |
| 24.1 Introduction 3838                                                   |      |
|                                                                          |      |
| 24.2 INFORMATION_SCHEMA Table Reference                                  | 3841 |
| 24.3 INFORMATION_SCHEMA General Tables 3844                              |      |
| 24.3.1 INFORMATION_SCHEMA General Table Reference 3844                   |      |
| 24.3.2 The INFORMATION_SCHEMA CHARACTER_SETS Table 3845                  |      |
| 24.3.3 The INFORMATION_SCHEMA COLLATIONS Table 3845                      |      |
| 24.3.4 The INFORMATION_SCHEMA                                            |      |
| COLLATION_CHARACTER_SET_APPLICABILITY Table 3846                         |      |
| 24.3.5 The INFORMATION_SCHEMA COLUMNS Table 3846                         |      |
| 24.3.6 The INFORMATION_SCHEMA COLUMN_PRIVILEGES Table 3849               |      |
| 24.3.7 The INFORMATION_SCHEMA ENGINES Table 3849                         |      |
| 24.3.8 The INFORMATION_SCHEMA EVENTS Table 3850                          |      |
| 24.3.9 The INFORMATION_SCHEMA FILES Table 3854                           |      |
|                                                                          |      |
| 24.3.10 The INFORMATION_SCHEMA GLOBAL_STATUS and SESSION_STATUS          |      |
| Tables 3861                                                              |      |

| 24.3.11 The INFORMATION_SCHEMA GLOBAL_VARIABLES and                        |      |
|----------------------------------------------------------------------------|------|
| SESSION_VARIABLES Tables 3861                                              |      |
| 24.3.12 The INFORMATION_SCHEMA KEY_COLUMN_USAGE Table 3861                 |      |
| 24.3.13 The INFORMATION_SCHEMA ndb_transid_mysql_connection_map Table 3863 |      |
| 24.3.14 The INFORMATION_SCHEMA OPTIMIZER_TRACE Table                       | 3864 |
| 24.3.15 The INFORMATION_SCHEMA PARAMETERS Table 3864                       |      |
| 24.3.16 The INFORMATION_SCHEMA PARTITIONS Table 3866                       |      |
| 24.3.17 The INFORMATION_SCHEMA PLUGINS Table 3869                          |      |
|                                                                            |      |
| 24.3.18 The INFORMATION_SCHEMA PROCESSLIST Table 3870                      |      |
| 24.3.19 The INFORMATION_SCHEMA PROFILING Table 3871                        |      |
| 24.3.20 The INFORMATION_SCHEMA REFERENTIAL_CONSTRAINTS Table 3872          |      |
| 24.3.21 The INFORMATION_SCHEMA ROUTINES Table 3873                         |      |
| 24.3.22 The INFORMATION_SCHEMA SCHEMATA Table 3876                         |      |
| 24.3.23 The INFORMATION_SCHEMA SCHEMA_PRIVILEGES Table 3877                |      |
| 24.3.24 The INFORMATION_SCHEMA STATISTICS Table 3877                       |      |
| 24.3.25 The INFORMATION_SCHEMA TABLES Table 3879                           |      |
| 24.3.26 The INFORMATION_SCHEMA TABLESPACES Table 3882                      |      |
| 24.3.27 The INFORMATION_SCHEMA TABLE_CONSTRAINTS Table 3883                |      |
| 24.3.28 The INFORMATION_SCHEMA TABLE_PRIVILEGES Table 3883                 |      |
| 24.3.29 The INFORMATION_SCHEMA TRIGGERS Table 3884                         |      |
| 24.3.30 The INFORMATION_SCHEMA USER_PRIVILEGES Table 3886                  |      |
| 24.3.31 The INFORMATION_SCHEMA VIEWS Table 3886                            |      |
| 24.4 INFORMATION_SCHEMA InnoDB Tables 3888                                 |      |
|                                                                            |      |
| 24.4.1 INFORMATION_SCHEMA InnoDB Table Reference 3888                      |      |
| 24.4.2 The INFORMATION_SCHEMA INNODB_BUFFER_PAGE Table                     | 3889 |
| 24.4.3 The INFORMATION_SCHEMA INNODB_BUFFER_PAGE_LRU Table 3892            |      |
| 24.4.4 The INFORMATION_SCHEMA INNODB_BUFFER_POOL_STATS Table 3895          |      |
| 24.4.5 The INFORMATION_SCHEMA INNODB_CMP and INNODB_CMP_RESET              |      |
| Tables 3898                                                                |      |
| 24.4.6 The INFORMATION_SCHEMA INNODB_CMPMEM and                            |      |
| INNODB_CMPMEM_RESET Tables 3900                                            |      |
| 24.4.7 The INFORMATION_SCHEMA INNODB_CMP_PER_INDEX and                     |      |
| INNODB_CMP_PER_INDEX_RESET Tables                                          | 3901 |
| 24.4.8 The INFORMATION_SCHEMA INNODB_FT_BEING_DELETED Table 3902           |      |
| 24.4.9 The INFORMATION_SCHEMA INNODB_FT_CONFIG Table 3903                  |      |
| 24.4.10 The INFORMATION_SCHEMA INNODB_FT_DEFAULT_STOPWORD Table . 3904     |      |
| 24.4.11 The INFORMATION_SCHEMA INNODB_FT_DELETED Table 3905                |      |
| 24.4.12 The INFORMATION_SCHEMA INNODB_FT_INDEX_CACHE Table 3906            |      |
| 24.4.13 The INFORMATION_SCHEMA INNODB_FT_INDEX_TABLE Table 3907            |      |
| 24.4.14 The INFORMATION_SCHEMA INNODB_LOCKS Table 3909                     |      |
| 24.4.15 The INFORMATION_SCHEMA INNODB_LOCK_WAITS Table 3910                |      |
| 24.4.16 The INFORMATION_SCHEMA INNODB_METRICS Table 3911                   |      |
|                                                                            |      |
| 24.4.17 The INFORMATION_SCHEMA INNODB_SYS_COLUMNS Table 3913               |      |
| 24.4.18 The INFORMATION_SCHEMA INNODB_SYS_DATAFILES Table                  | 3914 |
| 24.4.19 The INFORMATION_SCHEMA INNODB_SYS_FIELDS Table 3915                |      |
| 24.4.20 The INFORMATION_SCHEMA INNODB_SYS_FOREIGN Table 3916               |      |
| 24.4.21 The INFORMATION_SCHEMA INNODB_SYS_FOREIGN_COLS Table 3916          |      |
| 24.4.22 The INFORMATION_SCHEMA INNODB_SYS_INDEXES Table 3917               |      |
| 24.4.23 The INFORMATION_SCHEMA INNODB_SYS_TABLES Table 3918                |      |
| 24.4.24 The INFORMATION_SCHEMA INNODB_SYS_TABLESPACES Table 3920           |      |
| 24.4.25 The INFORMATION_SCHEMA INNODB_SYS_TABLESTATS View                  | 3921 |
| 24.4.26 The INFORMATION_SCHEMA INNODB_SYS_VIRTUAL Table                    | 3923 |
| 24.4.27 The INFORMATION_SCHEMA INNODB_TEMP_TABLE_INFO Table 3924           |      |
| 24.4.28 The INFORMATION_SCHEMA INNODB_TRX Table 3925                       |      |
| 24.5 INFORMATION_SCHEMA Thread Pool Tables 3928                            |      |
| 24.5.1 INFORMATION_SCHEMA Thread Pool Table Reference 3928                 |      |
| 24.5.2 The INFORMATION_SCHEMA TP_THREAD_GROUP_STATE Table 3928             |      |
| 24.5.3 The INFORMATION_SCHEMA TP_THREAD_GROUP_STATS Table 3930             |      |
|                                                                            |      |

| 24.5.4 The INFORMATION_SCHEMA TP_THREAD_STATE Table 3931                     |      |
|------------------------------------------------------------------------------|------|
| 24.6 INFORMATION_SCHEMA Connection Control Tables 3932                       |      |
| 24.6.1 INFORMATION_SCHEMA Connection Control Table Reference                 | 3932 |
| 24.6.2 The INFORMATION_SCHEMA                                                |      |
| CONNECTION_CONTROL_FAILED_LOGIN_ATTEMPTS Table 3932                          |      |
| 24.7 INFORMATION_SCHEMA MySQL Enterprise Firewall Tables 3933                |      |
| 24.7.1 INFORMATION_SCHEMA Firewall Table Reference 3933                      |      |
| 24.7.2 The INFORMATION_SCHEMA MYSQL_FIREWALL_USERS Table 3933                |      |
| 24.7.3 The INFORMATION_SCHEMA MYSQL_FIREWALL_WHITELIST Table 3934            |      |
| 24.8 Extensions to SHOW Statements 3934                                      |      |
| 25 MySQL Performance Schema 3937                                             |      |
|                                                                              |      |
| 25.1 Performance Schema Quick Start 3939                                     |      |
| 25.2 Performance Schema Build Configuration 3944                             |      |
| 25.3 Performance Schema Startup Configuration 3945                           |      |
| 25.4 Performance Schema Runtime Configuration 3947                           |      |
| 25.4.1 Performance Schema Event Timing 3948                                  |      |
| 25.4.2 Performance Schema Event Filtering 3951                               |      |
| 25.4.3 Event Pre-Filtering 3953                                              |      |
| 25.4.4 Pre-Filtering by Instrument 3953                                      |      |
| 25.4.5 Pre-Filtering by Object 3955                                          |      |
| 25.4.6 Pre-Filtering by Thread 3957                                          |      |
| 25.4.7 Pre-Filtering by Consumer 3959                                        |      |
| 25.4.8 Example Consumer Configurations 3961                                  |      |
| 25.4.9 Naming Instruments or Consumers for Filtering Operations 3966         |      |
| 25.4.10 Determining What Is Instrumented 3966                                |      |
| 25.5 Performance Schema Queries                                              | 3967 |
| 25.6 Performance Schema Instrument Naming Conventions 3967                   |      |
| 25.7 Performance Schema Status Monitoring 3970                               |      |
| 25.8 Performance Schema Atom and Molecule Events 3973                        |      |
| 25.9 Performance Schema Tables for Current and Historical Events 3974        |      |
| 25.10 Performance Schema Statement Digests 3975                              |      |
| 25.11 Performance Schema General Table Characteristics 3979                  |      |
| 25.12 Performance Schema Table Descriptions 3980                             |      |
| 25.12.1 Performance Schema Table Reference 3980                              |      |
| 25.12.2 Performance Schema Setup Tables 3984                                 |      |
| 25.12.3 Performance Schema Instance Tables 3989                              |      |
| 25.12.4 Performance Schema Wait Event Tables 3994                            |      |
| 25.12.5 Performance Schema Stage Event Tables 3999                           |      |
| 25.12.6 Performance Schema Statement Event Tables 4005                       |      |
| 25.12.7 Performance Schema Transaction Tables 4015                           |      |
| 25.12.8 Performance Schema Connection Tables 4023                            |      |
| 25.12.9 Performance Schema Connection Attribute Tables                       | 4026 |
| 25.12.10 Performance Schema User-Defined Variable Tables 4029                |      |
| 25.12.11 Performance Schema Replication Tables 4029                          |      |
| 25.12.12 Performance Schema Lock Tables 4040                                 |      |
| 25.12.13 Performance Schema System Variable Tables                           | 4044 |
| 25.12.14 Performance Schema Status Variable Tables 4045                      |      |
| 25.12.15 Performance Schema Summary Tables                                   | 4046 |
| 25.12.16 Performance Schema Miscellaneous Tables 4066                        |      |
| 25.13 Performance Schema Option and Variable Reference 4077                  |      |
| 25.14 Performance Schema Command Options                                     | 4080 |
| 25.15 Performance Schema System Variables 4081                               |      |
| 25.16 Performance Schema Status Variables 4098                               |      |
| 25.17 The Performance Schema Memory-Allocation Model 4101                    |      |
| 25.18 Performance Schema and Plugins 4102                                    |      |
|                                                                              |      |
| 25.19 Using the Performance Schema to Diagnose Problems 4102                 |      |
| 25.19.1 Query Profiling Using Performance Schema 4103                        |      |
| 25.20 Migrating to Performance Schema System and Status Variable Tables 4105 |      |

| 25.21 Restrictions on Performance Schema                               | 4107   |
|------------------------------------------------------------------------|--------|
| 26 MySQL sys Schema                                                    | . 4109 |
| 26.1 Prerequisites for Using the sys Schema                            | 4109   |
| 26.2 Using the sys Schema                                              |        |
| 26.3 sys Schema Progress Reporting                                     |        |
| 26.4 sys Schema Object Reference                                       |        |
| 26.4.1 sys Schema Object Index                                         |        |
|                                                                        |        |
| 26.4.2 sys Schema Tables and Triggers                                  |        |
| 26.4.3 sys Schema Views                                                |        |
| 26.4.4 sys Schema Stored Procedures                                    |        |
| 26.4.5 sys Schema Stored Functions                                     |        |
| 27 Connectors and APIs                                                 |        |
| 27.1 MySQL Connector/C++                                               | 4192   |
| 27.2 MySQL Connector/J                                                 | 4192   |
| 27.3 MySQL Connector/NET                                               | 4192   |
| 27.4 MySQL Connector/ODBC                                              | . 4192 |
| 27.5 MySQL Connector/Python                                            |        |
| 27.6 libmysgld, the Embedded MySQL Server Library                      |        |
| 27.6.1 Compiling Programs with libmysqld                               |        |
| 27.6.2 Restrictions When Using the Embedded MySQL Server               |        |
| 27.6.3 Options with the Embedded Server                                |        |
|                                                                        |        |
| 27.6.4 Embedded Server Examples                                        |        |
| 27.7 MySQL C API                                                       |        |
| 27.8 MySQL PHP API                                                     |        |
| 27.9 MySQL Perl API                                                    |        |
| 27.10 MySQL Python API                                                 |        |
| 27.11 MySQL Ruby APIs                                                  | 4199   |
| 27.11.1 The MySQL/Ruby API                                             | 4199   |
| 27.11.2 The Ruby/MySQL API                                             |        |
| 27.12 MySQL Tcl API                                                    |        |
| 27.13 MySQL Eiffel Wrapper                                             |        |
| 28 MySQL Enterprise Edition                                            |        |
| 28.1 MySQL Enterprise Backup Overview                                  |        |
| 28.2 MySQL Enterprise Security Overview                                |        |
|                                                                        |        |
| 28.3 MySQL Enterprise Encryption Overview                              |        |
| 28.4 MySQL Enterprise Audit Overview                                   |        |
| 28.5 MySQL Enterprise Firewall Overview                                |        |
| 28.6 MySQL Enterprise Thread Pool Overview                             |        |
| 28.7 MySQL Enterprise Data Masking and De-Identification Overview      |        |
| 28.8 MySQL Telemetry                                                   | . 4203 |
| 29 MySQL Workbench                                                     | 4205   |
| A MySQL 5.7 Frequently Asked Questions                                 | . 4207 |
| A.1 MySQL 5.7 FAQ: General                                             |        |
| A.2 MySQL 5.7 FAQ: Storage Engines                                     |        |
| A.3 MySQL 5.7 FAQ: Server SQL Mode                                     |        |
| A.4 MySQL 5.7 FAQ: Stored Procedures and Functions                     |        |
| A.5 MySQL 5.7 FAQ: Stored Frocedures and Functions                     |        |
| A.6 MySQL 5.7 FAQ: Higgers  A.6 MySQL 5.7 FAQ: Views                   |        |
|                                                                        |        |
| A.7 MySQL 5.7 FAQ: INFORMATION_SCHEMA                                  |        |
| A.8 MySQL 5.7 FAQ: Migration                                           |        |
| A.9 MySQL 5.7 FAQ: Security                                            |        |
| A.10 MySQL 5.7 FAQ: NDB Cluster                                        |        |
| A.11 MySQL 5.7 FAQ: MySQL Chinese, Japanese, and Korean Character Sets |        |
| A.12 MySQL 5.7 FAQ: Connectors & APIs                                  |        |
| A.13 MySQL 5.7 FAQ: C API, libmysql                                    | 4245   |
| A.14 MySQL 5.7 FAQ: Replication                                        | 4246   |
| A.15 MySQL 5.7 FAQ: MySQL Enterprise Thread Pool                       |        |
| A.16 MvSQL 5.7 FAQ: InnoDB Change Buffer                               |        |

## MySQL 5.7 Reference Manual

| A.17 MySQL 5.7 FAQ: InnoDB Data-at-Rest Encryption | 4253 |
|----------------------------------------------------|------|
| A.18 MySQL 5.7 FAQ: Virtualization Support         | 4255 |
| B Error Messages and Common Problems               | 4257 |
| B.1 Error Message Sources and Elements             | 4257 |
| B.2 Error Information Interfaces                   | 4259 |
| B.3 Problems and Common Errors                     | 4260 |
| B.3.1 How to Determine What Is Causing a Problem   | 4260 |
| B.3.2 Common Errors When Using MySQL Programs      | 4262 |
| B.3.3 Administration-Related Issues                | 4272 |
| B.3.4 Query-Related Issues                         | 4280 |
| B.3.5 Optimizer-Related Issues                     |      |
| B.3.6 Table Definition-Related Issues              | 4288 |
| B.3.7 Known Issues in MySQL                        | 4289 |
| C Indexes                                          |      |
| MySQL Glossary                                     | 4963 |
|                                                    |      |

## <span id="page-24-0"></span>Preface and Legal Notices

This is the Reference Manual for the MySQL Database System, version 5.7, through release 5.7.44. Differences between minor versions of MySQL 5.7 are noted in the present text with reference to release numbers (5.7.x). For license information, see the [Legal Notices](#page-24-1).

This manual is not intended for use with older versions of the MySQL software due to the many functional and other differences between MySQL 5.7 and previous versions. If you are using an earlier release of the MySQL software, please refer to the appropriate manual. For example, [MySQL 5.6](https://dev.mysql.com/doc/refman/5.6/en/) [Reference Manual](https://dev.mysql.com/doc/refman/5.6/en/) covers the 5.6 series of MySQL software releases.

If you are using MySQL 8.0, please refer to the [MySQL 8.0 Reference Manual](https://dev.mysql.com/doc/refman/8.0/en/).

**Licensing information—MySQL 5.7.** This product may include third-party software, used under license. If you are using a Commercial release of MySQL 5.7, see the [MySQL 5.7 Commercial Release](https://downloads.mysql.com/docs/licenses/mysqld-5.7-com-en.pdf) [License Information User Manual](https://downloads.mysql.com/docs/licenses/mysqld-5.7-com-en.pdf) for licensing information, including licensing information relating to third-party software that may be included in this Commercial release. If you are using a Community release of MySQL 5.7, see the [MySQL 5.7 Community Release License Information User Manual](https://downloads.mysql.com/docs/licenses/mysqld-5.7-gpl-en.pdf) for licensing information, including licensing information relating to third-party software that may be included in this Community release.

**Licensing information—MySQL NDB Cluster 7.5.** This product may include third-party software, used under license. If you are using a Commercial release of NDB Cluster 7.5, see the [MySQL NDB](https://downloads.mysql.com/docs/licenses/cluster-7.5-com-en.pdf) [Cluster 7.5 Commercial Release License Information User Manual](https://downloads.mysql.com/docs/licenses/cluster-7.5-com-en.pdf) for licensing information relating to third-party software that may be included in this Commercial release. If you are using a Community release of NDB Cluster 7.5, see the [MySQL NDB Cluster 7.5 Community Release License Information](https://downloads.mysql.com/docs/licenses/cluster-7.5-gpl-en.pdf) [User Manual](https://downloads.mysql.com/docs/licenses/cluster-7.5-gpl-en.pdf) for licensing information relating to third-party software that may be included in this Community release.

**Licensing information—MySQL NDB Cluster 7.6.** If you are using a Commercial release of MySQL NDB Cluster 7.6, see the [MySQL NDB Cluster 7.6 Commercial Release License Information](https://downloads.mysql.com/docs/licenses/cluster-7.6-com-en.pdf) [User Manual](https://downloads.mysql.com/docs/licenses/cluster-7.6-com-en.pdf) for licensing information, including licensing information relating to third-party software that may be included in this Commercial release. If you are using a Community release of MySQL NDB Cluster 7.6, see the [MySQL NDB Cluster 7.6 Community Release License Information User Manual](https://downloads.mysql.com/docs/licenses/cluster-7.6-gpl-en.pdf) for licensing information, including licensing information relating to third-party software that may be included in this Community release.

## <span id="page-24-1"></span>**Legal Notices**

Copyright © 1997, 2026, Oracle and/or its affiliates.

### **License Restrictions**

This software and related documentation are provided under a license agreement containing restrictions on use and disclosure and are protected by intellectual property laws. Except as expressly permitted in your license agreement or allowed by law, you may not use, copy, reproduce, translate, broadcast, modify, license, transmit, distribute, exhibit, perform, publish, or display any part, in any form, or by any means. Reverse engineering, disassembly, or decompilation of this software, unless required by law for interoperability, is prohibited.

#### **Warranty Disclaimer**

The information contained herein is subject to change without notice and is not warranted to be errorfree. If you find any errors, please report them to us in writing.

#### **Restricted Rights Notice**

If this is software, software documentation, data (as defined in the Federal Acquisition Regulation), or related documentation that is delivered to the U.S. Government or anyone licensing it on behalf of the U.S. Government, then the following notice is applicable:

U.S. GOVERNMENT END USERS: Oracle programs (including any operating system, integrated software, any programs embedded, installed, or activated on delivered hardware, and modifications of such programs) and Oracle computer documentation or other Oracle data delivered to or accessed by U.S. Government end users are "commercial computer software," "commercial computer software documentation," or "limited rights data" pursuant to the applicable Federal Acquisition Regulation and agency-specific supplemental regulations. As such, the use, reproduction, duplication, release, display, disclosure, modification, preparation of derivative works, and/or adaptation of i) Oracle programs (including any operating system, integrated software, any programs embedded, installed, or activated on delivered hardware, and modifications of such programs), ii) Oracle computer documentation and/ or iii) other Oracle data, is subject to the rights and limitations specified in the license contained in the applicable contract. The terms governing the U.S. Government's use of Oracle cloud services are defined by the applicable contract for such services. No other rights are granted to the U.S. Government.

#### **Hazardous Applications Notice**

This software or hardware is developed for general use in a variety of information management applications. It is not developed or intended for use in any inherently dangerous applications, including applications that may create a risk of personal injury. If you use this software or hardware in dangerous applications, then you shall be responsible to take all appropriate fail-safe, backup, redundancy, and other measures to ensure its safe use. Oracle Corporation and its affiliates disclaim any liability for any damages caused by use of this software or hardware in dangerous applications.

#### **Trademark Notice**

Oracle, Java, MySQL, and NetSuite are registered trademarks of Oracle and/or its affiliates. Other names may be trademarks of their respective owners.

Intel and Intel Inside are trademarks or registered trademarks of Intel Corporation. All SPARC trademarks are used under license and are trademarks or registered trademarks of SPARC International, Inc. AMD, Epyc, and the AMD logo are trademarks or registered trademarks of Advanced Micro Devices. UNIX is a registered trademark of The Open Group.

#### **Third-Party Content, Products, and Services Disclaimer**

This software or hardware and documentation may provide access to or information about content, products, and services from third parties. Oracle Corporation and its affiliates are not responsible for and expressly disclaim all warranties of any kind with respect to third-party content, products, and services unless otherwise set forth in an applicable agreement between you and Oracle. Oracle Corporation and its affiliates will not be responsible for any loss, costs, or damages incurred due to your access to or use of third-party content, products, or services, except as set forth in an applicable agreement between you and Oracle.

#### **Use of This Documentation**

This documentation is NOT distributed under a GPL license. Use of this documentation is subject to the following terms:

You may create a printed copy of this documentation solely for your own personal use. Conversion to other formats is allowed as long as the actual content is not altered or edited in any way. You shall not publish or distribute this documentation in any form or on any media, except if you distribute the documentation in a manner similar to how Oracle disseminates it (that is, electronically for download on a Web site with the software) or on a CD-ROM or similar medium, provided however that the documentation is disseminated together with the software on the same medium. Any other use, such as any dissemination of printed copies or use of this documentation, in whole or in part, in another publication, requires the prior written consent from an authorized representative of Oracle. Oracle and/ or its affiliates reserve any and all rights to this documentation not expressly granted above.

## **Documentation Accessibility**

For information about Oracle's commitment to accessibility, visit the Oracle Accessibility Program website at

[http://www.oracle.com/pls/topic/lookup?ctx=acc&id=docacc.](http://www.oracle.com/pls/topic/lookup?ctx=acc&id=docacc)

## **Access to Oracle Support for Accessibility**

Oracle customers that have purchased support have access to electronic support through My Oracle Support. For information, visit

<http://www.oracle.com/pls/topic/lookup?ctx=acc&id=info> or visit [http://www.oracle.com/pls/](http://www.oracle.com/pls/topic/lookup?ctx=acc&id=trs) [topic/lookup?ctx=acc&id=trs](http://www.oracle.com/pls/topic/lookup?ctx=acc&id=trs) if you are hearing impaired.

## <span id="page-28-0"></span>Chapter 1 General Information

## **Table of Contents**

| 1.1 About This Manual 2                                                                   |  |
|-------------------------------------------------------------------------------------------|--|
| 1.2 Overview of the MySQL Database Management System 4                                    |  |
| 1.2.1 What is MySQL? 4                                                                    |  |
| 1.2.2 The Main Features of MySQL 5                                                        |  |
| 1.2.3 History of MySQL 8                                                                  |  |
| 1.3 What Is New in MySQL 5.7 8                                                            |  |
| 1.4 Server and Status Variables and Options Added, Deprecated, or Removed in MySQL 5.7 24 |  |
| 1.5 How to Report Bugs or Problems 40                                                     |  |
| 1.6 MySQL Standards Compliance 44                                                         |  |
| 1.6.1 MySQL Extensions to Standard SQL 45                                                 |  |
| 1.6.2 MySQL Differences from Standard SQL 48                                              |  |
| 1.6.3 How MySQL Deals with Constraints 51                                                 |  |

The MySQL software delivers a very fast, multithreaded, multi-user, and robust SQL (Structured Query Language) database server. MySQL Server is intended for mission-critical, heavy-load production systems as well as for embedding into mass-deployed software. Oracle is a registered trademark of Oracle Corporation and/or its affiliates. MySQL is a trademark of Oracle Corporation and/or its affiliates, and shall not be used by Customer without Oracle's express written authorization. Other names may be trademarks of their respective owners.

The MySQL software is Dual Licensed. Users can choose to use the MySQL software as an Open Source product under the terms of the GNU General Public License [\(http://www.fsf.org/licenses/](http://www.fsf.org/licenses/)) or can purchase a standard commercial license from Oracle. See [http://www.mysql.com/company/legal/](http://www.mysql.com/company/legal/licensing/) [licensing/](http://www.mysql.com/company/legal/licensing/) for more information on our licensing policies.

The following list describes some sections of particular interest in this manual:

- For a discussion of MySQL Database Server capabilities, see [Section 1.2.2, "The Main Features of](#page-32-0) [MySQL".](#page-32-0)
- For an overview of new MySQL features, see [Section 1.3, "What Is New in MySQL 5.7"](#page-35-1). For information about the changes in each version, see the [Release Notes](https://dev.mysql.com/doc/relnotes/mysql/5.7/en/).
- For installation instructions, see Chapter 2, [Installing and Upgrading MySQL](#page-82-0). For information about upgrading MySQL, see Section 2.10, "Upgrading MySQL".
- For a tutorial introduction to the MySQL Database Server, see Chapter 3, Tutorial.
- For information about configuring and administering MySQL Server, see Chapter 5, MySQL Server Administration.
- For information about security in MySQL, see Chapter 6, Security.
- For information about setting up replication servers, see Chapter 16, Replication.
- For information about MySQL Enterprise, the commercial MySQL release with advanced features and management tools, see Chapter 28, MySQL Enterprise Edition.
- For answers to a number of questions that are often asked concerning the MySQL Database Server and its capabilities, see Appendix A, MySQL 5.7 Frequently Asked Questions.
- For a history of new features and bug fixes, see the [Release Notes.](https://dev.mysql.com/doc/relnotes/mysql/5.7/en/)

![](_page_29_Picture_1.jpeg)

#### **Important**

To report problems or bugs, please use the instructions at [Section 1.5,](#page-67-0) ["How to Report Bugs or Problems"](#page-67-0). If you find a security bug in MySQL Server, please let us know immediately by sending an email message to <secalert\_us@oracle.com>. Exception: Support customers should report all problems, including security bugs, to Oracle Support.

## <span id="page-29-0"></span>**1.1 About This Manual**

This is the Reference Manual for the MySQL Database System, version 5.7, through release 5.7.44. Differences between minor versions of MySQL 5.7 are noted in the present text with reference to release numbers (5.7.x). For license information, see the [Legal Notices](#page-24-1).

This manual is not intended for use with older versions of the MySQL software due to the many functional and other differences between MySQL 5.7 and previous versions. If you are using an earlier release of the MySQL software, please refer to the appropriate manual. For example, [MySQL 5.6](https://dev.mysql.com/doc/refman/5.6/en/) [Reference Manual](https://dev.mysql.com/doc/refman/5.6/en/) covers the 5.6 series of MySQL software releases.

If you are using MySQL 8.0, please refer to the [MySQL 8.0 Reference Manual](https://dev.mysql.com/doc/refman/8.0/en/).

Because this manual serves as a reference, it does not provide general instruction on SQL or relational database concepts. It also does not teach you how to use your operating system or command-line interpreter.

The MySQL Database Software is under constant development, and the Reference Manual is updated frequently as well. The most recent version of the manual is available online in searchable form at <https://dev.mysql.com/doc/>. Other formats also are available there, including downloadable HTML and PDF versions.

If you have questions about using MySQL, join the [MySQL Community Slack.](https://mysqlcommunity.slack.com/) If you have suggestions concerning additions or corrections to the manual itself, please send them to the [http://www.mysql.com/](http://www.mysql.com/company/contact/) [company/contact/](http://www.mysql.com/company/contact/).

## **Typographical and Syntax Conventions**

This manual uses certain typographical conventions:

- Text in this style is used for SQL statements; database, table, and column names; program listings and source code; and environment variables. Example: "To reload the grant tables, use the FLUSH PRIVILEGES statement."
- **Text in this style** indicates input that you type in examples.
- Text in this style indicates the names of executable programs and scripts, examples being mysql (the MySQL command-line client program) and mysqld (the MySQL server executable).
- Text in this style is used for variable input for which you should substitute a value of your own choosing.
- Text in this style is used for emphasis.
- **Text in this style** is used in table headings and to convey especially strong emphasis.
- Text in this style is used to indicate a program option that affects how the program is executed, or that supplies information that is needed for the program to function in a certain way. Example: "The --host option (short form -h) tells the mysql client program the hostname or IP address of the MySQL server that it should connect to".
- File names and directory names are written like this: "The global my.cnf file is located in the /etc directory."

• Character sequences are written like this: "To specify a wildcard, use the '%' character."

When commands or statements are prefixed by a prompt, we use these:

```
$> type a command here
#> type a command as root here
C:\> type a command here (Windows only)
mysql> type a mysql statement here
```

Commands are issued in your command interpreter. On Unix, this is typically a program such as sh, csh, or bash. On Windows, the equivalent program is command.com or cmd.exe, typically run in a console window. Statements prefixed by mysql are issued in the mysql command-line client.

![](_page_30_Picture_5.jpeg)

#### **Note**

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

## **Manual Authorship**

The Reference Manual source files are written in DocBook XML format. The HTML version and other formats are produced automatically, primarily using the DocBook XSL stylesheets. For information about DocBook, see <http://docbook.org/>

This manual was originally written by David Axmark and Michael "Monty" Widenius. It is maintained by the MySQL Documentation Team, consisting of Edward Gilmore, Sudharsana Gomadam, Kim seong Loh, Garima Sharma, Carlos Ortiz, Daniel So, and Jon Stephens.

## <span id="page-31-0"></span>**1.2 Overview of the MySQL Database Management System**

## <span id="page-31-1"></span>**1.2.1 What is MySQL?**

MySQL, the most popular Open Source SQL database management system, is developed, distributed, and supported by Oracle Corporation.

The MySQL website [\(http://www.mysql.com/](http://www.mysql.com/)) provides the latest information about MySQL software.

#### • **MySQL is a database management system.**

A database is a structured collection of data. It may be anything from a simple shopping list to a picture gallery or the vast amounts of information in a corporate network. To add, access, and process data stored in a computer database, you need a database management system such as MySQL Server. Since computers are very good at handling large amounts of data, database management systems play a central role in computing, as standalone utilities, or as parts of other applications.

#### • **MySQL databases are relational.**

 A relational database stores data in separate tables rather than putting all the data in one big storeroom. The database structures are organized into physical files optimized for speed. The logical model, with objects such as databases, tables, views, rows, and columns, offers a flexible programming environment. You set up rules governing the relationships between different data fields, such as one-to-one, one-to-many, unique, required or optional, and "pointers" between different tables. The database enforces these rules, so that with a well-designed database, your application never sees inconsistent, duplicate, orphan, out-of-date, or missing data.

The SQL part of "MySQL" stands for "Structured Query Language". SQL is the most common standardized language used to access databases. Depending on your programming environment, you might enter SQL directly (for example, to generate reports), embed SQL statements into code written in another language, or use a language-specific API that hides the SQL syntax.

SQL is defined by the ANSI/ISO SQL Standard. The SQL standard has been evolving since 1986 and several versions exist. In this manual, "SQL-92" refers to the standard released in 1992, "SQL:1999" refers to the standard released in 1999, and "SQL:2003" refers to the current version of the standard. We use the phrase "the SQL standard" to mean the current version of the SQL Standard at any time.

### • **MySQL software is Open Source.**

 Open Source means that it is possible for anyone to use and modify the software. Anybody can download the MySQL software from the Internet and use it without paying anything. If you wish, you may study the source code and change it to suit your needs. The MySQL software uses the GPL (GNU General Public License), [http://www.fsf.org/licenses/,](http://www.fsf.org/licenses/) to define what you may and may not do with the software in different situations. If you feel uncomfortable with the GPL or need to embed MySQL code into a commercial application, you can buy a commercially licensed version from us. See the MySQL Licensing Overview for more information [\(http://www.mysql.com/company/legal/](http://www.mysql.com/company/legal/licensing/) [licensing/\)](http://www.mysql.com/company/legal/licensing/).

#### • **The MySQL Database Server is very fast, reliable, scalable, and easy to use.**

If that is what you are looking for, you should give it a try. MySQL Server can run comfortably on a desktop or laptop, alongside your other applications, web servers, and so on, requiring little or no attention. If you dedicate an entire machine to MySQL, you can adjust the settings to take advantage of all the memory, CPU power, and I/O capacity available. MySQL can also scale up to clusters of machines, networked together.

MySQL Server was originally developed to handle large databases much faster than existing solutions and has been successfully used in highly demanding production environments for several years. Although under constant development, MySQL Server today offers a rich and useful set of functions. Its connectivity, speed, and security make MySQL Server highly suited for accessing databases on the Internet.

#### • **MySQL Server works in client/server or embedded systems.**

The MySQL Database Software is a client/server system that consists of a multithreaded SQL server that supports different back ends, several different client programs and libraries, administrative tools, and a wide range of application programming interfaces (APIs).

We also provide MySQL Server as an embedded multithreaded library that you can link into your application to get a smaller, faster, easier-to-manage standalone product.

#### • **A large amount of contributed MySQL software is available.**

MySQL Server has a practical set of features developed in close cooperation with our users. It is very likely that your favorite application or language supports the MySQL Database Server.

#### • **MySQL HeatWave.**

MySQL HeatWave is a fully managed database service, powered by the MySQL HeatWave inmemory query accelerator. It is the only cloud service that combines transactions, real-time analytics across data warehouses and data lakes, and machine learning in one MySQL Database; without the complexity, latency, risks, and cost of ETL duplication. It is available on OCI, AWS, and Azure. Learn more at:<https://www.oracle.com/mysql/>.

The official way to pronounce "MySQL" is "My Ess Que Ell" (not "my sequel"), but we do not mind if you pronounce it as "my sequel" or in some other localized way.

## <span id="page-32-0"></span>**1.2.2 The Main Features of MySQL**

This section describes some of the important characteristics of the MySQL Database Software. In most respects, the roadmap applies to all versions of MySQL. For information about features as they are introduced into MySQL on a series-specific basis, see the "In a Nutshell" section of the appropriate Manual:

- MySQL 8.4: [What Is New in MySQL 8.4 since MySQL 8.0](https://dev.mysql.com/doc/refman/8.4/en/mysql-nutshell.md)
- MySQL 8.0: [What Is New in MySQL 8.0](https://dev.mysql.com/doc/refman/8.0/en/mysql-nutshell.md)
- MySQL 5.7: [Section 1.3, "What Is New in MySQL 5.7"](#page-35-1)

## **Internals and Portability**

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

### **Data Types**

- Many data types: signed/unsigned integers 1, 2, 3, 4, and 8 bytes long, FLOAT, DOUBLE, CHAR, VARCHAR, BINARY, VARBINARY, TEXT, BLOB, DATE, TIME, DATETIME, TIMESTAMP, YEAR, SET, ENUM, and OpenGIS spatial types. See Chapter 11, Data Types.
- Fixed-length and variable-length string types.

### **Statements and Functions**

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
- Independence of function names from table or column names. For example, ABS is a valid column name. The only restriction is that for a function call, no spaces are permitted between the function name and the "(" that follows it. See Section 9.3, "Keywords and Reserved Words".
- You can refer to tables from different databases in the same statement.

### **Security**

- A privilege and password system that is very flexible and secure, and that enables host-based verification.
- Password security by encryption of all password traffic when you connect to a server.

## **Scalability and Limits**

- Support for large databases. We use MySQL Server with databases that contain 50 million records. We also know of users who use MySQL Server with 200,000 tables and about 5,000,000,000 rows.
- Support for up to 64 indexes per table. Each index may consist of 1 to 16 columns or parts of columns. The maximum index width for InnoDB tables is either 767 bytes or 3072 bytes. See Section 14.23, "InnoDB Limits". The maximum index width for MyISAM tables is 1000 bytes. See Section 15.2, "The MyISAM Storage Engine". An index may use a prefix of a column for CHAR, VARCHAR, BLOB, or TEXT column types.

## **Connectivity**

- Clients can connect to MySQL Server using several protocols:
  - Clients can connect using TCP/IP sockets on any platform.
  - On Windows systems, clients can connect using named pipes if the server is started with the named\_pipe system variable enabled. Windows servers also support shared-memory connections if started with the shared\_memory system variable enabled. Clients can connect through shared memory by using the --protocol=memory option.
  - On Unix systems, clients can connect using Unix domain socket files.
- MySQL client programs can be written in many languages. A client library written in C is available for clients written in C or C++, or for any language that provides C bindings.
- APIs for C, C++, Eiffel, Java, Perl, PHP, Python, Ruby, and Tcl are available, enabling MySQL clients to be written in many languages. See Chapter 27, Connectors and APIs.
- The Connector/ODBC (MyODBC) interface provides MySQL support for client programs that use ODBC (Open Database Connectivity) connections. For example, you can use MS Access to connect to your MySQL server. Clients can be run on Windows or Unix. Connector/ODBC source is available. All ODBC 2.5 functions are supported, as are many others. See [MySQL Connector/ODBC Developer](https://dev.mysql.com/doc/connector-odbc/en/) [Guide.](https://dev.mysql.com/doc/connector-odbc/en/)
- The Connector/J interface provides MySQL support for Java client programs that use JDBC connections. Clients can be run on Windows or Unix. Connector/J source is available. See [MySQL](https://dev.mysql.com/doc/connector-j/en/) [Connector/J Developer Guide.](https://dev.mysql.com/doc/connector-j/en/)
- MySQL Connector/NET enables developers to easily create .NET applications that require secure, high-performance data connectivity with MySQL. It implements the required ADO.NET interfaces and

integrates into ADO.NET aware tools. Developers can build applications using their choice of .NET languages. MySQL Connector/NET is a fully managed ADO.NET driver written in 100% pure C#. See [MySQL Connector/NET Developer Guide](https://dev.mysql.com/doc/connector-net/en/).

### **Localization**

- The server can provide error messages to clients in many languages. See Section 10.12, "Setting the Error Message Language".
- Full support for several different character sets, including latin1 (cp1252), german, big5, ujis, several Unicode character sets, and more. For example, the Scandinavian characters "å", "ä" and "ö" are permitted in table and column names.
- All data is saved in the chosen character set.
- Sorting and comparisons are done according to the default character set and collation. It is possible to change this when the MySQL server is started (see Section 10.3.2, "Server Character Set and Collation"). To see an example of very advanced sorting, look at the Czech sorting code. MySQL Server supports many different character sets that can be specified at compile time and runtime.
- The server time zone can be changed dynamically, and individual clients can specify their own time zone. See Section 5.1.13, "MySQL Server Time Zone Support".

## **Clients and Tools**

- MySQL includes several client and utility programs. These include both command-line programs such as mysqldump and mysqladmin, and graphical programs such as MySQL Workbench.
- MySQL Server has built-in support for SQL statements to check, optimize, and repair tables. These statements are available from the command line through the mysqlcheck client. MySQL also includes myisamchk, a very fast command-line utility for performing these operations on MyISAM tables. See Chapter 4, MySQL Programs.
- MySQL programs can be invoked with the --help or -? option to obtain online assistance.

## <span id="page-35-0"></span>**1.2.3 History of MySQL**

We started out with the intention of using the mSQL database system to connect to our tables using our own fast low-level (ISAM) routines. However, after some testing, we came to the conclusion that mSQL was not fast enough or flexible enough for our needs. This resulted in a new SQL interface to our database but with almost the same API interface as mSQL. This API was designed to enable third-party code that was written for use with mSQL to be ported easily for use with MySQL.

MySQL is named after co-founder Monty Widenius's daughter, My.

The name of the MySQL Dolphin (our logo) is "Sakila," which was chosen from a huge list of names suggested by users in our "Name the Dolphin" contest. The winning name was submitted by Ambrose Twebaze, an Open Source software developer from Eswatini (formerly Swaziland), Africa. According to Ambrose, the feminine name Sakila has its roots in SiSwati, the local language of Eswatini. Sakila is also the name of a town in Arusha, Tanzania, near Ambrose's country of origin, Uganda.

## <span id="page-35-1"></span>**1.3 What Is New in MySQL 5.7**

This section summarizes what has been added to, deprecated in, and removed from MySQL 5.7. A companion section lists MySQL server options and variables that have been added, deprecated, or removed in MySQL 5.7; see [Section 1.4, "Server and Status Variables and Options Added,](#page-51-0) [Deprecated, or Removed in MySQL 5.7"](#page-51-0).

- [Features Added in MySQL 5.7](#page-36-0)
- [Features Deprecated in MySQL 5.7](#page-45-0)

• [Features Removed in MySQL 5.7](#page-49-0)

## <span id="page-36-0"></span>**Features Added in MySQL 5.7**

The following features have been added to MySQL 5.7:

- **Security improvements.** These security enhancements were added:
  - In MySQL 8.0, caching\_sha2\_password is the default authentication plugin. To enable MySQL 5.7 clients to connect to 8.0 servers using accounts that authenticate using caching\_sha2\_password, the MySQL 5.7 client library and client programs support the caching\_sha2\_password client-side authentication plugin as of MySQL 5.7.23. This improves compatibility of MySQL 5.7 with MySQL 8.0 and higher servers. See Section 6.4.1.4, "Caching SHA-2 Pluggable Authentication".
  - The server now requires account rows in the mysql.user system table to have a nonempty plugin column value and disables accounts with an empty value. For server upgrade instructions, see Section 2.10.3, "Changes in MySQL 5.7". DBAs are advised to also convert accounts that use the mysql\_old\_password authentication plugin to use mysql\_native\_password instead, because support for mysql\_old\_password has been removed. For account upgrade instructions, see Section 6.4.1.3, "Migrating Away from Pre-4.1 Password Hashing and the mysql\_old\_password Plugin".
  - MySQL now enables database administrators to establish a policy for automatic password expiration: Any user who connects to the server using an account for which the password is past its permitted lifetime must change the password. For more information, see Section 6.2.11, "Password Management".
  - Administrators can lock and unlock accounts for better control over who can log in. For more information, see Section 6.2.15, "Account Locking".
  - To make it easier to support secure connections, MySQL servers compiled using OpenSSL can automatically generate missing SSL and RSA certificate and key files at startup. See Section 6.3.3.1, "Creating SSL and RSA Certificates and Keys using MySQL".

All servers, if not configured for SSL explicitly, attempt to enable SSL automatically at startup if they find the requisite SSL files in the data directory. See Section 6.3.1, "Configuring MySQL to Use Encrypted Connections".

In addition, MySQL distributions include a mysql\_ssl\_rsa\_setup utility that can be invoked manually to create SSL and RSA key and certificate files. For more information, see Section 4.4.5, "mysql\_ssl\_rsa\_setup — Create SSL/RSA Files".

- MySQL deployments installed using mysqld --initialize are secure by default. The following changes have been implemented as the default deployment characteristics:
  - The installation process creates only a single root account, 'root'@'localhost', automatically generates a random password for this account, and marks the password expired. The MySQL administrator must connect as root using the random password and assign a new password. (The server writes the random password to the error log.)
  - Installation creates no anonymous-user accounts.
  - Installation creates no test database.

For more information, see Section 2.9.1, "Initializing the Data Directory".

• MySQL Enterprise Edition now provides data masking and de-identification capabilities. Data masking hides sensitive information by replacing real values with substitutes. MySQL Enterprise Data Masking and De-Identification functions enable masking existing data using several methods such as obfuscation (removing identifying characteristics), generation of formatted random data, and data replacement or substitution. For more information, see Section 6.5, "MySQL Enterprise Data Masking and De-Identification".

- MySQL now sets the access control granted to clients on the named pipe to the minimum necessary for successful communication on Windows. Newer MySQL client software can open named pipe connections without any additional configuration. If older client software cannot be upgraded immediately, the new named\_pipe\_full\_access\_group system variable can be used to give a Windows group the necessary permissions to open a named pipe connection. Membership in the full-access group should be restricted and temporary.
- **SQL mode changes.** Strict SQL mode for transactional storage engines (STRICT\_TRANS\_TABLES) is now enabled by default.

Implementation for the ONLY\_FULL\_GROUP\_BY SQL mode has been made more sophisticated, to no longer reject deterministic queries that previously were rejected. In consequence, this mode is now enabled by default, to prohibit only nondeterministic queries containing expressions not guaranteed to be uniquely determined within a group.

The ERROR\_FOR\_DIVISION\_BY\_ZERO, NO\_ZERO\_DATE, and NO\_ZERO\_IN\_DATE SQL modes are now deprecated but enabled by default. The long term plan is to have them included in strict SQL mode and to remove them as explicit modes in a future MySQL release. See SQL Mode Changes in MySQL 5.7.

The changes to the default SQL mode result in a default sql\_mode system variable value with these modes enabled: ONLY\_FULL\_GROUP\_BY, STRICT\_TRANS\_TABLES, NO\_ZERO\_IN\_DATE, NO\_ZERO\_DATE, ERROR\_FOR\_DIVISION\_BY\_ZERO, NO\_AUTO\_CREATE\_USER, and NO\_ENGINE\_SUBSTITUTION.

- **Online ALTER TABLE.** ALTER TABLE now supports a RENAME INDEX clause that renames an index. The change is made in place without a table-copy operation. It works for all storage engines. See Section 13.1.8, "ALTER TABLE Statement".
- **ngram and MeCab full-text parser plugins.** MySQL provides a built-in full-text ngram parser plugin that supports Chinese, Japanese, and Korean (CJK), and an installable MeCab full-text parser plugin for Japanese.

For more information, see Section 12.9.8, "ngram Full-Text Parser", and Section 12.9.9, "MeCab Full-Text Parser Plugin".

- **InnoDB enhancements.** These InnoDB enhancements were added:
  - VARCHAR column size can be increased using an in-place ALTER TABLE, as in this example:

```
ALTER TABLE t1 ALGORITHM=INPLACE, CHANGE COLUMN c1 c1 VARCHAR(255);
```

This is true as long as the number of length bytes required by a VARCHAR column remains the same. For VARCHAR columns of 0 to 255 bytes in size, one length byte is required to encode the value. For VARCHAR columns of 256 bytes in size or more, two length bytes are required. As a result, in-place ALTER TABLE only supports increasing VARCHAR column size from 0 to 255 bytes, or from 256 bytes to a greater size. In-place ALTER TABLE does not support increasing the size of a VARCHAR column from less than 256 bytes to a size equal to or greater than 256 bytes. In this

case, the number of required length bytes changes from 1 to 2, which is only supported by a table copy (ALGORITHM=COPY).

Decreasing VARCHAR size using in-place ALTER TABLE is not supported. Decreasing VARCHAR size requires a table copy (ALGORITHM=COPY).

For more information, see Section 14.13.1, "Online DDL Operations".

- DDL performance for InnoDB temporary tables is improved through optimization of CREATE TABLE, DROP TABLE, TRUNCATE TABLE, and ALTER TABLE statements.
- InnoDB temporary table metadata is no longer stored to InnoDB system tables. Instead, a new table, INNODB\_TEMP\_TABLE\_INFO, provides users with a snapshot of active temporary tables. The table contains metadata and reports on all user and system-created temporary tables that are active within a given InnoDB instance. The table is created when the first SELECT statement is run against it.
- InnoDB now supports MySQL-supported spatial data types. Prior to this release, InnoDB would store spatial data as binary BLOB data. BLOB remains the underlying data type but spatial data types are now mapped to a new InnoDB internal data type, DATA\_GEOMETRY.
- There is now a separate tablespace for all non-compressed InnoDB temporary tables. The new tablespace is always recreated on server startup and is located in DATADIR by default. A newly added configuration file option, innodb\_temp\_data\_file\_path, allows for a user-defined temporary data file path.
- innochecksum functionality is enhanced with several new options and extended capabilities. See Section 4.6.1, "innochecksum — Offline InnoDB File Checksum Utility".
- A new type of non-redo undo log for both normal and compressed temporary tables and related objects now resides in the temporary tablespace. For more information, see Section 14.6.7, "Undo Logs".
- InnoDB buffer pool dump and load operations are enhanced. A new system variable, innodb\_buffer\_pool\_dump\_pct, allows you to specify the percentage of most recently used pages in each buffer pool to read out and dump. When there is other I/O activity being performed by InnoDB background tasks, InnoDB attempts to limit the number of buffer pool load operations per second using the innodb\_io\_capacity setting.
- Support is added to InnoDB for full-text parser plugins. For information about full-text parser plugins, see [Full-Text Parser Plugins](https://dev.mysql.com/doc/extending-mysql/5.7/en/plugin-types.md#full-text-plugin-type) and [Writing Full-Text Parser Plugins.](https://dev.mysql.com/doc/extending-mysql/5.7/en/writing-full-text-plugins.md)
- InnoDB supports multiple page cleaner threads for flushing dirty pages from buffer pool instances. A new system variable, innodb\_page\_cleaners, is used to specify the number of page cleaner threads. The default value of 1 maintains the previous configuration in which there is a single page

cleaner thread. This enhancement builds on work completed in MySQL 5.6, which introduced a single page cleaner thread to offload buffer pool flushing work from the InnoDB master thread.

- Online DDL support is extended to the following operations for regular and partitioned InnoDB tables:
  - OPTIMIZE TABLE
  - ALTER TABLE ... FORCE
  - ALTER TABLE ... ENGINE=INNODB (when run on an InnoDB table)

Online DDL support reduces table rebuild time and permits concurrent DML. See Section 14.13, "InnoDB and Online DDL".

- The Fusion-io Non-Volatile Memory (NVM) file system on Linux provides atomic write capability, which makes the InnoDB doublewrite buffer redundant. The InnoDB doublewrite buffer is automatically disabled for system tablespace files (ibdata files) located on Fusion-io devices that support atomic writes.
- InnoDB supports the Transportable Tablespace feature for partitioned InnoDB tables and individual InnoDB table partitions. This enhancement eases backup procedures for partitioned tables and enables copying of partitioned tables and individual table partitions between MySQL instances. For more information, see Section 14.6.1.3, "Importing InnoDB Tables".
- The innodb\_buffer\_pool\_size parameter is dynamic, allowing you to resize the buffer pool without restarting the server. The resizing operation, which involves moving pages to a new location in memory, is performed in chunks. Chunk size is configurable using the new innodb\_buffer\_pool\_chunk\_size configuration option. You can monitor resizing progress using the new Innodb\_buffer\_pool\_resize\_status status variable. For more information, see Configuring InnoDB Buffer Pool Size Online.
- Multithreaded page cleaner support (innodb\_page\_cleaners) is extended to shutdown and recovery phases.
- InnoDB supports indexing of spatial data types using SPATIAL indexes, including use of ALTER TABLE ... ALGORITHM=INPLACE for online operations (ADD SPATIAL INDEX).
- InnoDB performs a bulk load when creating or rebuilding indexes. This method of index creation is known as a "sorted index build". This enhancement, which improves the efficiency of index creation, also applies to full-text indexes. A new global configuration option, innodb\_fill\_factor, defines the percentage of space on each page that is filled with data during a sorted index build, with the remaining space reserved for future index growth. For more information, see Section 14.6.2.3, "Sorted Index Builds".
- A new log record type (MLOG\_FILE\_NAME) is used to identify tablespaces that have been modified since the last checkpoint. This enhancement simplifies tablespace discovery during crash recovery and eliminates scans on the file system prior to redo log application. For more information about the benefits of this enhancement, see Tablespace Discovery During Crash Recovery.

This enhancement changes the redo log format, requiring that MySQL be shut down cleanly before upgrading to or downgrading from MySQL 5.7.5.

- You can truncate undo logs that reside in undo tablespaces. This feature is enabled using the innodb\_undo\_log\_truncate configuration option. For more information, see Truncating Undo Tablespaces.
- InnoDB supports native partitioning. Previously, InnoDB relied on the ha\_partition handler, which creates a handler object for each partition. With native partitioning, a partitioned InnoDB

table uses a single partition-aware handler object. This enhancement reduces the amount of memory required for partitioned InnoDB tables.

As of MySQL 5.7.9, mysql\_upgrade looks for and attempts to upgrade partitioned InnoDB tables that were created using the ha\_partition handler. Also in MySQL 5.7.9 and later, you can upgrade such tables by name in the mysql client using ALTER TABLE ... UPGRADE PARTITIONING.

• InnoDB supports the creation of general tablespaces using CREATE TABLESPACE syntax.

```
CREATE TABLESPACE `tablespace_name`
 ADD DATAFILE 'file_name.ibd'
 [FILE_BLOCK_SIZE = n]
```

General tablespaces can be created outside of the MySQL data directory, are capable of holding multiple tables, and support tables of all row formats.

Tables are added to a general tablespace using CREATE TABLE tbl\_name ... TABLESPACE [=] tablespace\_name or ALTER TABLE tbl\_name TABLESPACE [=] tablespace\_name syntax.

For more information, see Section 14.6.3.3, "General Tablespaces".

- DYNAMIC replaces COMPACT as the implicit default row format for InnoDB tables. A new configuration option, innodb\_default\_row\_format, specifies the default InnoDB row format. For more information, see Defining the Row Format of a Table.
- As of MySQL 5.7.11, InnoDB supports data-at-rest encryption for file-per-table tablespaces. Encryption is enabled by specifying the ENCRYPTION option when creating or altering an InnoDB table. This feature relies on a keyring plugin for encryption key management. For more information, see Section 6.4.4, "The MySQL Keyring", and Section 14.14, "InnoDB Data-at-Rest Encryption".
- As of MySQL 5.7.24, the [zlib library](http://www.zlib.net/) version bundled with MySQL was raised from version 1.2.3 to version 1.2.11. MySQL implements compression with the help of the zlib library.

If you use InnoDB compressed tables, see Section 2.10.3, "Changes in MySQL 5.7" for related upgrade implications.

• **JSON support.** Beginning with MySQL 5.7.8, MySQL supports a native JSON type. JSON values are not stored as strings, instead using an internal binary format that permits quick read access to document elements. JSON documents stored in JSON columns are automatically validated whenever they are inserted or updated, with an invalid document producing an error. JSON documents are normalized on creation, and can be compared using most comparison operators such as =, <, <=, >, >=, <>, !=, and <=>; for information about supported operators as well as precedence and other rules that MySQL follows when comparing JSON values, see Comparison and Ordering of JSON Values.

MySQL 5.7.8 also introduces a number of functions for working with JSON values. These functions include those listed here:

- Functions that create JSON values: JSON\_ARRAY(), JSON\_MERGE(), and JSON\_OBJECT(). See Section 12.17.2, "Functions That Create JSON Values".
- Functions that search JSON values: JSON\_CONTAINS(), JSON\_CONTAINS\_PATH(), JSON\_EXTRACT(), JSON\_KEYS(), and JSON\_SEARCH(). See Section 12.17.3, "Functions That Search JSON Values".
- Functions that modify JSON values: JSON\_APPEND(), JSON\_ARRAY\_APPEND(), JSON\_ARRAY\_INSERT(), JSON\_INSERT(), JSON\_QUOTE(), JSON\_REMOVE(),

JSON\_REPLACE(), JSON\_SET(), and JSON\_UNQUOTE(). See Section 12.17.4, "Functions That Modify JSON Values".

• Functions that provide information about JSON values: JSON\_DEPTH(), JSON\_LENGTH(), JSON\_TYPE(), and JSON\_VALID(). See Section 12.17.5, "Functions That Return JSON Value Attributes".

In MySQL 5.7.9 and later, you can use column->path as shorthand for JSON\_EXTRACT(column, path). This works as an alias for a column wherever a column identifier can occur in an SQL statement, including WHERE, ORDER BY, and GROUP BY clauses. This includes SELECT, UPDATE, DELETE, CREATE TABLE, and other SQL statements. The left hand side must be a JSON column identifier (and not an alias). The right hand side is a quoted JSON path expression which is evaluated against the JSON document returned as the column value.

MySQL 5.7.22 adds the following JSON functions:

- Two JSON aggregation functions JSON\_ARRAYAGG() and JSON\_OBJECTAGG(). JSON\_ARRAYAGG() takes a column or expression as its argument, and aggregates the result as a single JSON array. The expression can evaluate to any MySQL data type; this does not have to be a JSON value. JSON\_OBJECTAGG() takes two columns or expressions which it interprets as a key and a value; it returns the result as a single JSON object. For more information and examples, see Section 12.19, "Aggregate Functions".
- The JSON utility function JSON\_PRETTY(), which outputs an existing JSON value in an easy-toread format; each JSON object member or array value is printed on a separate line, and a child object or array is intended 2 spaces with respect to its parent.

This function also works with a string that can be parsed as a JSON value.

See also Section 12.17.6, "JSON Utility Functions".

• The JSON utility function JSON\_STORAGE\_SIZE(), which returns the storage space in bytes used for the binary representation of a JSON document prior to any partial update (see previous item).

This function also accepts a valid string representation of a JSON document. For such a value, JSON\_STORAGE\_SIZE() returns the space used by its binary representation following its conversion to a JSON document. For a variable containing the string representation of a JSON document, JSON\_STORAGE\_FREE() returns zero. Either function produces an error if its (non-null) argument cannot be parsed as a valid JSON document, and NULL if the argument is NULL.

For more information and examples, see Section 12.17.6, "JSON Utility Functions".

- A JSON merge function intended to conform to [RFC 7396.](https://tools.ietf.org/html/rfc7396) JSON\_MERGE\_PATCH(), when used on 2 JSON objects, merges them into a single JSON object that has as members a union of the following sets:
  - Each member of the first object for which there is no member with the same key in the second object.
  - Each member of the second object for which there is no member having the same key in the first object, and whose value is not the JSON null literal.
  - Each member having a key that exists in both objects, and whose value in the second object is not the JSON null literal.

As part of this work, the JSON\_MERGE() function has been renamed JSON\_MERGE\_PRESERVE(). JSON\_MERGE() continues to be recognized as an alias for JSON\_MERGE\_PRESERVE() in MySQL 5.7, but is now deprecated and is subject to removal in a future version of MySQL.

For more information and examples, see Section 12.17.4, "Functions That Modify JSON Values".

See Section 12.17.3, "Functions That Search JSON Values", for more information about -> and JSON\_EXTRACT(). For information about JSON path support in MySQL 5.7, see Searching and Modifying JSON Values. See also Indexing a Generated Column to Provide a JSON Column Index.

• **System and status variables.** System and status variable information is now available in Performance Schema tables, in preference to use of INFORMATION\_SCHEMA tables to obtain these variable. This also affects the operation of the SHOW VARIABLES and SHOW STATUS statements. The value of the show\_compatibility\_56 system variable affects the output produced from and privileges required for system and status variable statements and tables. For details, see the description of that variable in Section 5.1.7, "Server System Variables".

![](_page_42_Picture_9.jpeg)

### **Note**

The default for show\_compatibility\_56 is OFF. Applications that require 5.6 behavior should set this variable to ON until such time as they have been migrated to the new behavior for system variables and status variables. See Section 25.20, "Migrating to Performance Schema System and Status Variable Tables"

- **sys schema.** MySQL distributions now include the sys schema, which is a set of objects that help DBAs and developers interpret data collected by the Performance Schema. sys schema objects can be used for typical tuning and diagnosis use cases. For more information, see Chapter 26, MySQL sys Schema.
- **Condition handling.** MySQL now supports stacked diagnostics areas. When the diagnostics area stack is pushed, the first (current) diagnostics area becomes the second (stacked) diagnostics area and a new current diagnostics area is created as a copy of it. Within a condition handler, executed statements modify the new current diagnostics area, but GET STACKED DIAGNOSTICS can be used to inspect the stacked diagnostics area to obtain information about the condition that caused the handler to activate, independent of current conditions within the handler itself. (Previously, there was a single diagnostics area. To inspect handler-activating conditions within a handler, it was necessary to check this diagnostics area before executing any statements that could change it.) See Section 13.6.7.3, "GET DIAGNOSTICS Statement", and Section 13.6.7.7, "The MySQL Diagnostics Area".
- **Optimizer.** These optimizer enhancements were added:
  - EXPLAIN can be used to obtain the execution plan for an explainable statement executing in a named connection:

EXPLAIN [options] FOR CONNECTION connection\_id;

For more information, see Section 8.8.4, "Obtaining Execution Plan Information for a Named Connection".

- It is possible to provide hints to the optimizer within individual SQL statements, which enables finer control over statement execution plans than can be achieved using the optimizer\_switch system variable. Hints are also permitted in statements used with EXPLAIN, enabling you to see how hints affect execution plans. For more information, see Section 8.9.3, "Optimizer Hints".
- **prefer\_ordering\_index flag.** By default, MySQL attempts to use an ordered index for any ORDER BY or GROUP BY query that has a LIMIT clause, whenever the optimizer determines that this would result in faster execution. Because it is possible in some cases that choosing a different optimization for such queries actually performs better, it is possible as of MySQL 5.7.33 to disable this optimization by setting the prefer\_ordering\_index flag to off.

The default value for this flag is on.

For more information and examples, see Section 8.9.2, "Switchable Optimizations", and Section 8.2.1.17, "LIMIT Query Optimization".

- **Triggers.** Previously, a table could have at most one trigger for each combination of trigger event (INSERT, UPDATE, DELETE) and action time (BEFORE, AFTER). This limitation has been lifted and multiple triggers are permitted. For more information, see Section 23.3, "Using Triggers".
- **Logging.** These logging enhancements were added:
  - Previously, on Unix and Unix-like systems, MySQL support for sending the server error log to syslog was implemented by having mysqld\_safe capture server error output and pass it to syslog. The server now includes native syslog support, which has been extended to include Windows. For more information about sending server error output to syslog, see Section 5.4.2, "The Error Log".
  - The mysql client now has a --syslog option that causes interactive statements to be sent to the system syslog facility. Logging is suppressed for statements that match the default "ignore" pattern list ("\*IDENTIFIED\*:\*PASSWORD\*"), as well as statements that match any patterns specified using the --histignore option. See Section 4.5.1.3, "mysql Client Logging".
- **Generated Columns.** MySQL now supports the specification of generated columns in CREATE TABLE and ALTER TABLE statements. Values of a generated column are computed from an expression specified at column creation time. Generated columns can be virtual (computed "on the fly" when rows are read) or stored (computed when rows are inserted or updated). For more information, see Section 13.1.18.7, "CREATE TABLE and Generated Columns".
- **mysql client.** Previously, **Control+C** in mysql interrupted the current statement if there was one, or exited mysql if not. Now **Control+C** interrupts the current statement if there was one, or cancels any partial input line otherwise, but does not exit.
- **Database name rewriting with mysqlbinlog.** Renaming of databases by mysqlbinlog when reading from binary logs written using the row-based format is now supported using the - rewrite-db option added in MySQL 5.7.1.

This option uses the format --rewrite-db='dboldname->dbnewname'. You can implement multiple rewrite rules, by specifying the option multiple times.

- **HANDLER with partitioned tables.** The HANDLER statement may now be used with userpartitioned tables. Such tables may use any of the available partitioning types (see Section 22.2, "Partitioning Types").
- **Index condition pushdown support for partitioned tables.** Queries on partitioned tables using the InnoDB or MyISAM storage engine may employ the index condition pushdown optimization that

was introduced in MySQL 5.6. See Section 8.2.1.5, "Index Condition Pushdown Optimization", for more information.

- **WITHOUT VALIDATION support for ALTER TABLE ... EXCHANGE PARTITION.** As of MySQL 5.7.5, ALTER TABLE ... EXCHANGE PARTITION syntax includes an optional {WITH|WITHOUT} VALIDATION clause. When WITHOUT VALIDATION is specified, ALTER TABLE ... EXCHANGE PARTITION does not perform row-by-row validation when exchanging a populated table with the partition, permitting database administrators to assume responsibility for ensuring that rows are within the boundaries of the partition definition. WITH VALIDATION is the default behavior and need not be specified explicitly. For more information, see Section 22.3.3, "Exchanging Partitions and Subpartitions with Tables".
- **Source dump thread improvements.** The source dump thread was refactored to reduce lock contention and improve source throughput. Previous to MySQL 5.7.2, the dump thread took a lock on the binary log whenever reading an event; in MySQL 5.7.2 and later, this lock is held only while reading the position at the end of the last successfully written event. This means both that multiple dump threads are now able to read concurrently from the binary log file, and that dump threads are now able to read while clients are writing to the binary log.
- **Character set support.** MySQL 5.7.4 includes a gb18030 character set that supports the China National Standard GB18030 character set. For more information about MySQL character set support, see Chapter 10, Character Sets, Collations, Unicode.
- **Changing the replication source without STOP SLAVE.** In MySQL 5.7.4 and later, the strict requirement to execute STOP SLAVE prior to issuing any CHANGE MASTER TO statement is removed. Instead of depending on whether the replica is stopped, the behavior of CHANGE MASTER TO now depends on the states of the replica SQL thread and replica I/O threads; which of these threads is stopped or running now determines the options that can or cannot be used with a CHANGE MASTER TO statement at a given point in time. The rules for making this determination are listed here:
  - If the SQL thread is stopped, you can execute CHANGE MASTER TO using any combination of RELAY\_LOG\_FILE, RELAY\_LOG\_POS, and MASTER\_DELAY options, even if the replica I/O thread is running. No other options may be used with this statement when the I/O thread is running.
  - If the I/O thread is stopped, you can execute CHANGE MASTER TO using any of the options for this statement (in any allowed combination) except RELAY\_LOG\_FILE, RELAY\_LOG\_POS, or MASTER\_DELAY, even when the SQL thread is running. These three options may not be used when the I/O thread is running.
  - Both the SQL thread and the I/O thread must be stopped before issuing CHANGE MASTER TO ... MASTER\_AUTO\_POSITION = 1.

You can check the current state of the replica SQL and I/O threads using SHOW SLAVE STATUS.

If you are using statement-based replication and temporary tables, it is possible for a CHANGE MASTER TO statement following a STOP SLAVE statement to leave behind temporary tables on the replica. As part of this set of improvements, a warning is now issued whenever CHANGE MASTER TO is issued following STOP SLAVE when statement-based replication is in use and Slave\_open\_temp\_tables remains greater than 0.

For more information, see Section 13.4.2.1, "CHANGE MASTER TO Statement", and Section 16.3.7, "Switching Sources During Failover".

- **Test suite.** The MySQL test suite now uses InnoDB as the default storage engine.
- **Multi-source replication is now possible.** MySQL Multi-Source Replication adds the ability to replicate from multiple sources to a replica. MySQL Multi-Source Replication topologies can be

used to back up multiple servers to a single server, to merge table shards, and consolidate data from multiple servers to a single server. See Section 16.1.5, "MySQL Multi-Source Replication".

As part of MySQL Multi-Source Replication, replication channels have been added. Replication channels enable a replica to open multiple connections to replicate from, with each channel being a connection to a source. See Section 16.2.2, "Replication Channels".

- **Group Replication Performance Schema tables.** MySQL 5.7 adds a number of new tables to the Performance Schema to provide information about replication groups and channels. These include the following tables:
  - replication\_applier\_configuration
  - replication\_applier\_status
  - replication\_applier\_status\_by\_coordinator
  - replication\_applier\_status\_by\_worker
  - replication\_connection\_configuration
  - replication\_connection\_status
  - replication\_group\_members
  - replication\_group\_member\_stats

All of these tables were added in MySQL 5.7.2, except for replication\_group\_members and replication\_group\_member\_stats, which were added in MySQL 5.7.6. For more information, see Section 25.12.11, "Performance Schema Replication Tables".

- **Group Replication SQL.** The following statements were added in MySQL 5.7.6 for controlling Group Replication:
  - START GROUP\_REPLICATION
  - STOP GROUP\_REPLICATION

For more information, see Section 13.4.3, "SQL Statements for Controlling Group Replication".

## <span id="page-45-0"></span>**Features Deprecated in MySQL 5.7**

The following features are deprecated in MySQL 5.7 and may be removed in a future series. Where alternatives are shown, applications should be updated to use them.

For applications that use features deprecated in MySQL 5.7 that have been removed in a higher MySQL series, statements may fail when replicated from a MySQL 5.7 source to a higher-series replica, or may have different effects on source and replica. To avoid such problems, applications that use features deprecated in 5.7 should be revised to avoid them and use alternatives when possible.

• The ERROR\_FOR\_DIVISION\_BY\_ZERO, NO\_ZERO\_DATE, and NO\_ZERO\_IN\_DATE SQL modes are now deprecated but enabled by default. The long term plan is to have them included in strict SQL mode and to remove them as explicit modes in a future MySQL release.

The deprecated ERROR\_FOR\_DIVISION\_BY\_ZERO, NO\_ZERO\_DATE, and NO\_ZERO\_IN\_DATE SQL modes are still recognized so that statements that name them do not produce an error, but are expected to be removed in a future version of MySQL. To make advance preparation for versions of MySQL in which these mode names do not exist, applications should be modified not to refer to them. See SQL Mode Changes in MySQL 5.7.

- These SQL modes are now deprecated; expect them to be removed in a future version of MySQL: DB2, MAXDB, MSSQL, MYSQL323, MYSQL40, ORACLE, POSTGRESQL, NO\_FIELD\_OPTIONS, NO\_KEY\_OPTIONS, NO\_TABLE\_OPTIONS. These deprecations have two implications:
  - Assigning a deprecated mode to the sql\_mode system variable produces a warning.
  - With the MAXDB SQL mode enabled, using CREATE TABLE or ALTER TABLE to add a TIMESTAMP column to a table produces a warning.
- Changes to account-management statements make the following features obsolete. They are now deprecated:
  - Using GRANT to create users. Instead, use CREATE USER. Following this practice makes the NO\_AUTO\_CREATE\_USER SQL mode immaterial for GRANT statements, so it too is deprecated.
  - Using GRANT to modify account properties other than privilege assignments. This includes authentication, SSL, and resource-limit properties. Instead, establish such properties at accountcreation time with CREATE USER or modify them afterward with ALTER USER.
  - IDENTIFIED BY PASSWORD 'auth\_string' syntax for CREATE USER and GRANT. Instead, use IDENTIFIED WITH auth\_plugin AS 'auth\_string' for CREATE USER and ALTER USER, where the 'auth\_string' value is in a format compatible with the named plugin.
  - The PASSWORD() function is deprecated and should be avoided in any context. Thus, SET PASSWORD ... = PASSWORD('auth\_string') syntax is also deprecated. SET PASSWORD ... = 'auth\_string' syntax is not deprecated; nevertheless, ALTER USER is now the preferred statement for assigning passwords.
  - The old\_passwords system variable. Account authentication plugins can no longer be left unspecified in the mysql.user system table, so any statement that assigns a password from a cleartext string can unambiguously determine the hashing method to use on the string before storing it in the mysql.user table. This renders old\_passwords superflous.
- The query cache is deprecated. Deprecation includes these items:
  - The FLUSH QUERY CACHE and RESET QUERY CACHE statements.
  - The SQL\_CACHE and SQL\_NO\_CACHE SELECT modifiers.
  - These system variables: have\_query\_cache, ndb\_cache\_check\_time, query\_cache\_limit, query\_cache\_min\_res\_unit, query\_cache\_size, query\_cache\_type, query\_cache\_wlock\_invalidate.
  - These status variables: Qcache\_free\_blocks, Qcache\_free\_memory, Qcache\_hits, Qcache\_inserts, Qcache\_lowmem\_prunes, Qcache\_not\_cached, Qcache\_queries\_in\_cache, Qcache\_total\_blocks.
- Previously, the --transaction-isolation and --transaction-read-only server startup options corresponded to the tx\_isolation and tx\_read\_only system variables. For better name correspondence between startup option and system variable names, transaction\_isolation and transaction\_read\_only have been created as aliases for tx\_isolation and tx\_read\_only. The tx\_isolation and tx\_read\_only variables are now deprecated;expect them to be removed in MySQL 8.0. Applications should be adjusted to use transaction\_isolation and transaction\_read\_only instead.
- The --skip-innodb option and its synonyms (--innodb=OFF, --disable-innodb, and so forth) are deprecated. These options have no effect as of MySQL 5.7. because InnoDB cannot be disabled.
- The client-side --ssl and --ssl-verify-server-cert options are deprecated. Use --sslmode=REQUIRED instead of --ssl=1 or --enable-ssl. Use --ssl-mode=DISABLED instead of

--ssl=0, --skip-ssl, or --disable-ssl. Use --ssl-mode=VERIFY\_IDENTITY instead of - ssl-verify-server-cert options. (The server-side --ssl option is not deprecated.)

For the C API, MYSQL\_OPT\_SSL\_ENFORCE and MYSQL\_OPT\_SSL\_VERIFY\_SERVER\_CERT options for [mysql\\_options\(\)](https://dev.mysql.com/doc/c-api/5.7/en/mysql-options.md) correspond to the client-side --ssl and --ssl-verifyserver-cert options and are deprecated. Use MYSQL\_OPT\_SSL\_MODE with an option value of SSL\_MODE\_REQUIRED or SSL\_MODE\_VERIFY\_IDENTITY instead.

- The log\_warnings system variable and --log-warnings server option are deprecated. Use the log\_error\_verbosity system variable instead.
- The --temp-pool server option is deprecated.
- The binlog\_max\_flush\_queue\_time system variable does nothing in MySQL 5.7, and is deprecated as of MySQL 5.7.9.
- The innodb\_support\_xa system variable, which enables InnoDB support for two-phase commit in XA transactions, is deprecated as of MySQL 5.7.10. InnoDB support for two-phase commit in XA transactions is always enabled as of MySQL 5.7.10.
- The metadata\_locks\_cache\_size and metadata\_locks\_hash\_instances system variables are deprecated. These do nothing as of MySQL 5.7.4.
- The sync\_frm system variable is deprecated.
- The global character\_set\_database and collation\_database system variables are deprecated; expect them to be removed in a future version of MySQL.

Assigning a value to the session character\_set\_database and collation\_database system variables is deprecated and assignments produce a warning. The session variables are expected to become read only in a future version of MySQL, and assignments to them to produce an error, while remaining possible to read the session variables to determine the database character set and collation for the default database.

- The global scope for the sql\_log\_bin system variable has been deprecated, and this variable can now be set with session scope only. The statement SET GLOBAL SQL\_LOG\_BIN now produces an error. It remains possible to read the global value of sql\_log\_bin, but doing so produces a warning. You should act now to remove from your applications any dependencies on reading this value; the global scope sql\_log\_bin is removed in MySQL 8.0.
- With the introduction of the data dictionary in MySQL 8.0, the --ignore-db-dir option and ignore\_db\_dirs system variable became superfluous and were removed in that version. Consequently, they are deprecated in MySQL 5.7.
- GROUP BY implicitly sorts by default (that is, in the absence of ASC or DESC designators), but relying on implicit GROUP BY sorting in MySQL 5.7 is deprecated. To achieve a specific sort order of grouped results, it is preferable to use To produce a given sort order, use explicit ASC or DESC designators for GROUP BY columns or provide an ORDER BY clause. GROUP BY sorting is a MySQL extension that may change in a future release; for example, to make it possible for the optimizer to order groupings in whatever manner it deems most efficient and to avoid the sorting overhead.
- The EXTENDED and PARTITIONS keywords for the EXPLAIN statement are deprecated. These keywords are still recognized but are now unnecessary because their effect is always enabled.
- The ENCRYPT(), ENCODE(), DECODE(), DES\_ENCRYPT(), and DES\_DECRYPT() encryption functions are deprecated. For ENCRYPT(), consider using SHA2() instead for one-way hashing. For the others, consider using AES\_ENCRYPT() and AES\_DECRYPT() instead. The --des-key-file option, the have\_crypt system variable, the DES\_KEY\_FILE option for the FLUSH statement, and the HAVE\_CRYPT CMake option also are deprecated.
- The MBREqual() spatial function is deprecated. Use MBREquals() instead.

- The functions described in Section 12.16.4, "Functions That Create Geometry Values from WKB Values" previously accepted either WKB strings or geometry arguments. Use of geometry arguments is deprecated. See that section for guidelines for migrating queries away from using geometry arguments.
- The INFORMATION\_SCHEMA PROFILING table is deprecated. Use the Performance Schema instead; see Chapter 25, MySQL Performance Schema.
- The INFORMATION\_SCHEMA INNODB\_LOCKS and INNODB\_LOCK\_WAITS tables are deprecated, to be removed in MySQL 8.0, which provides replacement Performance Schema tables.
- The Performance Schema setup\_timers table is deprecated and is removed in MySQL 8.0, as is the TICK row in the performance\_timers table.
- The sys schema sys.version view is deprecated; expect it be removed in a future version of MySQL. Affected applications should be adjusted to use an alternative instead. For example, use the VERSION() function to retrieve the MySQL server version.
- Treatment of \N as a synonym for NULL in SQL statements is deprecated and is removed in MySQL 8.0; use NULL instead.

This change does not affect text file import or export operations performed with LOAD DATA or SELECT ... INTO OUTFILE, for which NULL continues to be represented by \N. See Section 13.2.6, "LOAD DATA Statement".

- PROCEDURE ANALYSE() syntax is deprecated.
- Comment stripping by the mysql client and the options to control it (--skip-comments, comments) are deprecated.
- mysqld\_safe support for syslog output is deprecated. Use the native server syslog support used instead. See Section 5.4.2, "The Error Log".
- Conversion of pre-MySQL 5.1 database names containing special characters to 5.1 format with the addition of a #mysql50# prefix is deprecated. Because of this, the --fix-db-names and --fixtable-names options for mysqlcheck and the UPGRADE DATA DIRECTORY NAME clause for the ALTER DATABASE statement are also deprecated.

Upgrades are supported only from one release series to another (for example, 5.0 to 5.1, or 5.1 to 5.5), so there should be little remaining need for conversion of older 5.0 database names to current versions of MySQL. As a workaround, upgrade a MySQL 5.0 installation to MySQL 5.1 before upgrading to a more recent release.

• mysql\_install\_db functionality has been integrated into the MySQL server, mysqld. To use this capability to initialize a MySQL installation, if you previously invoked mysql\_install\_db manually, invoke mysqld with the --initialize or --initialize-insecure option, depending on whether you want the server to generate a random password for the initial 'root'@'localhost' account.

mysql\_install\_db is now deprecated, as is the special --bootstrap option that mysql\_install\_db passes to mysqld.

- The mysql\_plugin utility is deprecated. Alternatives include loading plugins at server startup using the --plugin-load or --plugin-load-add option, or at runtime using the INSTALL PLUGIN statement.
- The resolveip utility is deprecated. nslookup, host, or dig can be used instead.
- The resolve\_stack\_dump utility is deprecated. Stack traces from official MySQL builds are always symbolized, so there is no need to use resolve\_stack\_dump.
- The [mysql\\_kill\(\)](https://dev.mysql.com/doc/c-api/5.7/en/mysql-kill.md), [mysql\\_list\\_fields\(\)](https://dev.mysql.com/doc/c-api/5.7/en/mysql-list-fields.md), [mysql\\_list\\_processes\(\)](https://dev.mysql.com/doc/c-api/5.7/en/mysql-list-processes.md), and [mysql\\_refresh\(\)](https://dev.mysql.com/doc/c-api/5.7/en/mysql-refresh.md) C API functions are deprecated. The same is true of the corresponding

COM\_PROCESS\_KILL, COM\_FIELD\_LIST, COM\_PROCESS\_INFO, and COM\_REFRESH client/server protocol commands. Instead, use [mysql\\_query\(\)](https://dev.mysql.com/doc/c-api/5.7/en/mysql-query.md) to execute a KILL, SHOW COLUMNS, SHOW PROCESSLIST, or FLUSH statement, respectively.

- The mysql\_shutdown() C API function is deprecated. Instead, use [mysql\\_query\(\)](https://dev.mysql.com/doc/c-api/5.7/en/mysql-query.md) to execute a SHUTDOWN statement.
- The libmysqld embedded server library is deprecated as of MySQL 5.7.19. These are also deprecated:
  - The mysql\_config --libmysqld-libs, --embedded-libs, and --embedded options
  - The CMake WITH\_EMBEDDED\_SERVER, WITH\_EMBEDDED\_SHARED\_LIBRARY, and INSTALL\_SECURE\_FILE\_PRIV\_EMBEDDEDDIR options
  - The (undocumented) mysql --server-arg option
  - The mysqltest --embedded-server, --server-arg, and --server-file options
  - The mysqltest\_embedded and mysql\_client\_test\_embedded test programs

Because libmysqld uses an API comparable to that of libmysqlclient, the migration path away from libmysqld is straightforward:

- 1. Bring up a standalone MySQL server (mysqld).
- 2. Modify application code to remove API calls that are specific to libmysqld.
- 3. Modify application code to connect to the standalone MySQL server.
- 4. Modify build scripts to use libmysqlclient rather than libmysqld. For example, if you use mysql\_config, invoke it with the --libs option rather than --libmysqld-libs.
- The replace utility is deprecated.
- Support for DTrace is deprecated.
- The JSON\_MERGE() function is deprecated as of MySQL 5.7.22. Use JSON\_MERGE\_PRESERVE() instead.
- Support for placing table partitions in shared InnoDB tablespaces is deprecated as of MySQL 5.7.24. Shared tablespaces include the InnoDB system tablespace and general tablespaces. For information about identifying partitions in shared tablespaces and moving them to file-per-table tablespaces, see [Preparing Your Installation for Upgrade](https://dev.mysql.com/doc/refman/8.0/en/upgrade-prerequisites.md).
- Support for TABLESPACE = innodb\_file\_per\_table and TABLESPACE = innodb\_temporary clauses with CREATE TEMPORARY TABLE is deprecated as of MySQL 5.7.24.
- The --ndb perror option is deprecated. Use the ndb\_perror utility instead.
- The myisam\_repair\_threads system variable myisam\_repair\_threads are deprecated as of MySQL 5.7.38; expect support for both to be removed in a future release of MySQL.

From MySQL 5.7.38, values other than 1 (the default) for myisam\_repair\_threads produce a warning.

## <span id="page-49-0"></span>**Features Removed in MySQL 5.7**

The following items are obsolete and have been removed in MySQL 5.7. Where alternatives are shown, applications should be updated to use them.

For MySQL 5.6 applications that use features removed in MySQL 5.7, statements may fail when replicated from a MySQL 5.6 source to a MySQL 5.7 replica, or may have different effects on source and replica. To avoid such problems, applications that use features removed in MySQL 5.7 should be revised to avoid them and use alternatives when possible.

- Support for passwords that use the older pre-4.1 password hashing format is removed, which involves the following changes. Applications that use any feature no longer supported must be modified.
  - The mysql\_old\_password authentication plugin is removed. Accounts that use this plugin are disabled at startup and the server writes an "unknown plugin" message to the error log. For instructions on upgrading accounts that use this plugin, see Section 6.4.1.3, "Migrating Away from Pre-4.1 Password Hashing and the mysql\_old\_password Plugin".
  - The --secure-auth option to the server and client programs is the default, but is now a no-op. It is deprecated; expect it to be removed in a future MySQL release.
  - The --skip-secure-auth option to the server and client programs is no longer supported and using it produces an error.
  - The secure\_auth system variable permits only a value of 1; a value of 0 is no longer permitted.
  - For the old\_passwords system variable, a value of 1 (produce pre-4.1 hashes) is no longer permitted.
  - The OLD\_PASSWORD() function is removed.
- In MySQL 5.6.6, the 2-digit YEAR(2) data type was deprecated. Support for YEAR(2) is now removed. Once you upgrade to MySQL 5.7.5 or higher, any remaining 2-digit YEAR(2) columns must be converted to 4-digit YEAR columns to become usable again. For conversion strategies, see Section 11.2.5, "2-Digit YEAR(2) Limitations and Migrating to 4-Digit YEAR". For example, run mysql\_upgrade after upgrading.
- The innodb\_mirrored\_log\_groups system variable. The only supported value was 1, so it had no purpose.
- The storage\_engine system variable. Use default\_storage\_engine instead.
- The thread\_concurrency system variable.
- The timed\_mutexes system variable, which had no effect.
- The IGNORE clause for ALTER TABLE.
- INSERT DELAYED is no longer supported. The server recognizes but ignores the DELAYED keyword, handles the insert as a nondelayed insert, and generates an ER\_WARN\_LEGACY\_SYNTAX\_CONVERTED warning. ("INSERT DELAYED is no longer supported. The statement was converted to INSERT.") Similarly, REPLACE DELAYED is handled as a nondelayed replace. You should expect the DELAYED keyword to be removed in a future release.

In addition, several DELAYED-related options or features were removed:

- The --delayed-insert option for mysqldump.
- The COUNT\_WRITE\_DELAYED, SUM\_TIMER\_WRITE\_DELAYED, MIN\_TIMER\_WRITE\_DELAYED, AVG\_TIMER\_WRITE\_DELAYED, and MAX\_TIMER\_WRITE\_DELAYED columns of the Performance Schema table\_lock\_waits\_summary\_by\_table table.
- mysqlbinlog no longer writes comments mentioning INSERT DELAYED.
- Database symlinking on Windows using .sym files has been removed because it is redundant with native symlink support available using mklink. Any .sym file symbolic links are now ignored and should be replaced with symlinks created using mklink. See Section 8.12.3.3, "Using Symbolic Links for Databases on Windows".

- The unused --basedir, --datadir, and --tmpdir options for mysql\_upgrade were removed.
- Previously, program options could be specified in full or as any unambiguous prefix. For example, the --compress option could be given to mysqldump as --compr, but not as --comp because the latter is ambiguous. Option prefixes are no longer supported; only full options are accepted. This is because prefixes can cause problems when new options are implemented for programs and a prefix that is currently unambiguous might become ambiguous in the future. Some implications of this change:
  - The --key-buffer option must now be specified as --key-buffer-size.
  - The --skip-grant option must now be specified as --skip-grant-tables.
- SHOW ENGINE INNODB MUTEX output is removed. Comparable information can be generated by creating views on Performance Schema tables.
- The InnoDB Tablespace Monitor and InnoDB Table Monitor are removed. For the Table Monitor, equivalent information can be obtained from InnoDB INFORMATION\_SCHEMA tables.
- The specially named tables used to enable and disable the standard InnoDB Monitor and InnoDB Lock Monitor (innodb\_monitor and innodb\_lock\_monitor) are removed and replaced by two dynamic system variables: innodb\_status\_output and innodb\_status\_output\_locks. For additional information, see Section 14.18, "InnoDB Monitors".
- The innodb\_use\_sys\_malloc and innodb\_additional\_mem\_pool\_size system variables, deprecated in MySQL 5.6.3, were removed.
- The msql2mysql, mysql\_convert\_table\_format, mysql\_find\_rows, mysql\_fix\_extensions, mysql\_setpermission, mysql\_waitpid, mysql\_zap, mysqlaccess, and mysqlbug utilities.
- The mysqlhotcopy utility. Alternatives include mysqldump and MySQL Enterprise Backup.
- The binary-configure.sh script.
- The INNODB\_PAGE\_ATOMIC\_REF\_COUNT CMake option is removed.
- The innodb\_create\_intrinsic option is removed.
- The innodb\_optimize\_point\_storage option and related internal data types (DATA\_POINT and DATA\_VAR\_POINT) are removed.
- The innodb\_log\_checksum\_algorithm option is removed.
- The myisam\_repair\_threads system variable as of MySQL 5.7.39.

## <span id="page-51-0"></span>**1.4 Server and Status Variables and Options Added, Deprecated, or Removed in MySQL 5.7**

- [Options and Variables Introduced in MySQL 5.7](#page-51-1)
- [Options and Variables Deprecated in MySQL 5.7](#page-64-0)
- [Options and Variables Removed in MySQL 5.7](#page-66-0)

This section lists server variables, status variables, and options that were added for the first time, have been deprecated, or have been removed in MySQL 5.7.

## <span id="page-51-1"></span>**Options and Variables Introduced in MySQL 5.7**

The following system variables, status variables, and server options have been added in MySQL 5.7.

• Audit\_log\_current\_size: Audit log file current size. Added in MySQL 5.7.9.

- Audit\_log\_event\_max\_drop\_size: Size of largest dropped audited event. Added in MySQL 5.7.9.
- Audit\_log\_events: Number of handled audited events. Added in MySQL 5.7.9.
- Audit\_log\_events\_filtered: Number of filtered audited events. Added in MySQL 5.7.9.
- Audit\_log\_events\_lost: Number of dropped audited events. Added in MySQL 5.7.9.
- Audit\_log\_events\_written: Number of written audited events. Added in MySQL 5.7.9.
- Audit\_log\_total\_size: Combined size of written audited events. Added in MySQL 5.7.9.
- Audit\_log\_write\_waits: Number of write-delayed audited events. Added in MySQL 5.7.9.
- Com\_change\_repl\_filter: Count of CHANGE REPLICATION FILTER statements. Added in MySQL 5.7.3.
- Com\_explain\_other: Count of EXPLAIN FOR CONNECTION statements. Added in MySQL 5.7.2.
- Com\_group\_replication\_start: Count of START GROUP\_REPLICATION statements. Added in MySQL 5.7.6.
- Com\_group\_replication\_stop: Count of STOP GROUP\_REPLICATION statements. Added in MySQL 5.7.6.
- Com\_show\_create\_user: Count of SHOW CREATE USER statements. Added in MySQL 5.7.6.
- Com\_show\_slave\_status\_nonblocking: Count of SHOW REPLICA | SLAVE STATUS NONBLOCKING statements. Added in MySQL 5.7.0.
- Com\_shutdown: Count of SHUTDOWN statements. Added in MySQL 5.7.9.
- Connection\_control\_delay\_generated: How many times server delayed connection request. Added in MySQL 5.7.17.
- Firewall\_access\_denied: Number of statements rejected by MySQL Enterprise Firewall plugin. Added in MySQL 5.7.9.
- Firewall\_access\_granted: Number of statements accepted by MySQL Enterprise Firewall plugin. Added in MySQL 5.7.9.
- Firewall\_cached\_entries: Number of statements recorded by MySQL Enterprise Firewall plugin. Added in MySQL 5.7.9.
- Innodb\_buffer\_pool\_resize\_status: Status of dynamic buffer pool resizing operation. Added in MySQL 5.7.5.
- Locked\_connects: Number of attempts to connect to locked accounts. Added in MySQL 5.7.6.
- Max\_execution\_time\_exceeded: Number of statements that exceeded execution timeout value. Added in MySQL 5.7.8.
- Max\_execution\_time\_set: Number of statements for which execution timeout was set. Added in MySQL 5.7.8.
- Max\_execution\_time\_set\_failed: Number of statements for which execution timeout setting failed. Added in MySQL 5.7.8.
- Max\_statement\_time\_exceeded: Number of statements that exceeded execution timeout value. Added in MySQL 5.7.4.
- Max\_statement\_time\_set: Number of statements for which execution timeout was set. Added in MySQL 5.7.4.

- Max\_statement\_time\_set\_failed: Number of statements for which execution timeout setting failed. Added in MySQL 5.7.4.
- Max\_used\_connections\_time: Time at which Max\_used\_connections reached its current value. Added in MySQL 5.7.5.
- Performance\_schema\_index\_stat\_lost: Number of indexes for which statistics were lost. Added in MySQL 5.7.6.
- Performance\_schema\_memory\_classes\_lost: How many memory instruments could not be loaded. Added in MySQL 5.7.2.
- Performance\_schema\_metadata\_lock\_lost: Number of metadata locks that could not be recorded. Added in MySQL 5.7.3.
- Performance\_schema\_nested\_statement\_lost: Number of stored program statements for which statistics were lost. Added in MySQL 5.7.2.
- Performance\_schema\_prepared\_statements\_lost: Number of prepared statements that could not be instrumented. Added in MySQL 5.7.4.
- Performance\_schema\_program\_lost: Number of stored programs for which statistics were lost. Added in MySQL 5.7.2.
- Performance\_schema\_table\_lock\_stat\_lost: Number of tables for which lock statistics were lost. Added in MySQL 5.7.6.
- Rewriter\_number\_loaded\_rules: Number of rewrite rules successfully loaded into memory. Added in MySQL 5.7.6.
- Rewriter\_number\_reloads: Number of reloads of rules table into memory. Added in MySQL 5.7.6.
- Rewriter\_number\_rewritten\_queries: Number of queries rewritten since plugin was loaded. Added in MySQL 5.7.6.
- Rewriter\_reload\_error: Whether error occurred when last loading rewriting rules into memory. Added in MySQL 5.7.6.
- audit-log: Whether to activate audit log plugin. Added in MySQL 5.7.9.
- audit\_log\_buffer\_size: Size of audit log buffer. Added in MySQL 5.7.9.
- audit\_log\_compression: Audit log file compression method. Added in MySQL 5.7.21.
- audit\_log\_connection\_policy: Audit logging policy for connection-related events. Added in MySQL 5.7.9.
- audit\_log\_current\_session: Whether to audit current session. Added in MySQL 5.7.9.
- audit\_log\_disable: Whether to disable the audit log. Added in MySQL 5.7.37.
- audit\_log\_encryption: Audit log file encryption method. Added in MySQL 5.7.21.
- audit\_log\_exclude\_accounts: Accounts not to audit. Added in MySQL 5.7.9.
- audit\_log\_file: Name of audit log file. Added in MySQL 5.7.9.
- audit\_log\_filter\_id: ID of current audit log filter. Added in MySQL 5.7.13.
- audit\_log\_flush: Close and reopen audit log file. Added in MySQL 5.7.9.
- audit\_log\_format: Audit log file format. Added in MySQL 5.7.9.
- audit\_log\_format\_unix\_timestamp: Whether to include Unix timestamp in JSON-format audit log. Added in MySQL 5.7.35.

- audit\_log\_include\_accounts: Accounts to audit. Added in MySQL 5.7.9.
- audit\_log\_policy: Audit logging policy. Added in MySQL 5.7.9.
- audit\_log\_read\_buffer\_size: Audit log file read buffer size. Added in MySQL 5.7.21.
- audit\_log\_rotate\_on\_size: Close and reopen audit log file at this size. Added in MySQL 5.7.9.
- audit\_log\_statement\_policy: Audit logging policy for statement-related events. Added in MySQL 5.7.9.
- audit\_log\_strategy: Audit logging strategy. Added in MySQL 5.7.9.
- authentication\_ldap\_sasl\_auth\_method\_name: Authentication method name. Added in MySQL 5.7.19.
- authentication\_ldap\_sasl\_bind\_base\_dn: LDAP server base distinguished name. Added in MySQL 5.7.19.
- authentication\_ldap\_sasl\_bind\_root\_dn: LDAP server root distinguished name. Added in MySQL 5.7.19.
- authentication\_ldap\_sasl\_bind\_root\_pwd: LDAP server root bind password. Added in MySQL 5.7.19.
- authentication\_ldap\_sasl\_ca\_path: LDAP server certificate authority file name. Added in MySQL 5.7.19.
- authentication\_ldap\_sasl\_group\_search\_attr: LDAP server group search attribute. Added in MySQL 5.7.19.
- authentication\_ldap\_sasl\_group\_search\_filter: LDAP custom group search filter. Added in MySQL 5.7.21.
- authentication\_ldap\_sasl\_init\_pool\_size: LDAP server initial connection pool size. Added in MySQL 5.7.19.
- authentication\_ldap\_sasl\_log\_status: LDAP server log level. Added in MySQL 5.7.19.
- authentication\_ldap\_sasl\_max\_pool\_size: LDAP server maximum connection pool size. Added in MySQL 5.7.19.
- authentication\_ldap\_sasl\_server\_host: LDAP server host name or IP address. Added in MySQL 5.7.19.
- authentication\_ldap\_sasl\_server\_port: LDAP server port number. Added in MySQL 5.7.19.
- authentication\_ldap\_sasl\_tls: Whether to use encrypted connections to LDAP server. Added in MySQL 5.7.19.
- authentication\_ldap\_sasl\_user\_search\_attr: LDAP server user search attribute. Added in MySQL 5.7.19.
- authentication\_ldap\_simple\_auth\_method\_name: Authentication method name. Added in MySQL 5.7.19.
- authentication\_ldap\_simple\_bind\_base\_dn: LDAP server base distinguished name. Added in MySQL 5.7.19.
- authentication\_ldap\_simple\_bind\_root\_dn: LDAP server root distinguished name. Added in MySQL 5.7.19.
- authentication\_ldap\_simple\_bind\_root\_pwd: LDAP server root bind password. Added in MySQL 5.7.19.

- authentication\_ldap\_simple\_ca\_path: LDAP server certificate authority file name. Added in MySQL 5.7.19.
- authentication\_ldap\_simple\_group\_search\_attr: LDAP server group search attribute. Added in MySQL 5.7.19.
- authentication\_ldap\_simple\_group\_search\_filter: LDAP custom group search filter. Added in MySQL 5.7.21.
- authentication\_ldap\_simple\_init\_pool\_size: LDAP server initial connection pool size. Added in MySQL 5.7.19.
- authentication\_ldap\_simple\_log\_status: LDAP server log level. Added in MySQL 5.7.19.
- authentication\_ldap\_simple\_max\_pool\_size: LDAP server maximum connection pool size. Added in MySQL 5.7.19.
- authentication\_ldap\_simple\_server\_host: LDAP server host name or IP address. Added in MySQL 5.7.19.
- authentication\_ldap\_simple\_server\_port: LDAP server port number. Added in MySQL 5.7.19.
- authentication\_ldap\_simple\_tls: Whether to use encrypted connections to LDAP server. Added in MySQL 5.7.19.
- authentication\_ldap\_simple\_user\_search\_attr: LDAP server user search attribute. Added in MySQL 5.7.19.
- authentication\_windows\_log\_level: Windows authentication plugin logging level. Added in MySQL 5.7.9.
- authentication\_windows\_use\_principal\_name: Whether to use Windows authentication plugin principal name. Added in MySQL 5.7.9.
- auto\_generate\_certs: Whether to autogenerate SSL key and certificate files. Added in MySQL 5.7.5.
- avoid\_temporal\_upgrade: Whether ALTER TABLE should upgrade pre-5.6.4 temporal columns. Added in MySQL 5.7.6.
- binlog\_error\_action: Controls what happens when server cannot write to binary log. Added in MySQL 5.7.6.
- binlog\_group\_commit\_sync\_delay: Sets number of microseconds to wait before synchronizing transactions to disk. Added in MySQL 5.7.5.
- binlog\_group\_commit\_sync\_no\_delay\_count: Sets maximum number of transactions to wait for before aborting current delay specified by binlog\_group\_commit\_sync\_delay. Added in MySQL 5.7.5.
- binlog\_gtid\_simple\_recovery: Controls how binary logs are iterated during GTID recovery. Added in MySQL 5.7.6.
- binlog\_transaction\_dependency\_history\_size: Number of row hashes kept for looking up transaction that last updated some row. Added in MySQL 5.7.22.
- binlog\_transaction\_dependency\_tracking: Source of dependency information (commit timestamps or transaction write sets) from which to assess which transactions can be executed in parallel by replica's multithreaded applier. Added in MySQL 5.7.22.
- binlogging\_impossible\_mode: Deprecated and later removed. Use binlog\_error\_action instead. Added in MySQL 5.7.5.

- block\_encryption\_mode: Mode for block-based encryption algorithms. Added in MySQL 5.7.4.
- check\_proxy\_users: Whether built-in authentication plugins do proxying. Added in MySQL 5.7.7.
- connection\_control\_failed\_connections\_threshold: Consecutive failed connection attempts before delays occur. Added in MySQL 5.7.17.
- connection\_control\_max\_connection\_delay: Maximum delay (milliseconds) for server response to failed connection attempts. Added in MySQL 5.7.17.
- connection\_control\_min\_connection\_delay: Minimum delay (milliseconds) for server response to failed connection attempts. Added in MySQL 5.7.17.
- daemonize: Run as System V daemon. Added in MySQL 5.7.6.
- default\_authentication\_plugin: Default authentication plugin. Added in MySQL 5.7.2.
- default\_password\_lifetime: Age in days when passwords effectively expire. Added in MySQL 5.7.4.
- disable-partition-engine-check: Whether to disable startup check for tables without native partitioning. Added in MySQL 5.7.17.
- disabled\_storage\_engines: Storage engines that cannot be used to create tables. Added in MySQL 5.7.8.
- disconnect\_on\_expired\_password: Whether server disconnects clients with expired passwords if clients cannot handle such accounts. Added in MySQL 5.7.1.
- early-plugin-load: Specify plugins to load before loading mandatory built-in plugins and before storage engine initialization. Added in MySQL 5.7.11.
- executed\_gtids\_compression\_period: Renamed to gtid\_executed\_compression\_period. Added in MySQL 5.7.5.
- group\_replication\_allow\_local\_disjoint\_gtids\_join: Allow current server to join group even if it has transactions not present in group. Added in MySQL 5.7.17.
- group\_replication\_allow\_local\_lower\_version\_join: Allow current server to join group even if it has lower plugin version than group. Added in MySQL 5.7.17.
- group\_replication\_auto\_increment\_increment: Determines interval between successive column values for transactions executing on this server. Added in MySQL 5.7.17.
- group\_replication\_bootstrap\_group: Configure this server to bootstrap group. Added in MySQL 5.7.17.
- group\_replication\_components\_stop\_timeout: Timeout, in seconds, that plugin waits for each component when shutting down. Added in MySQL 5.7.17.
- group\_replication\_compression\_threshold: Value in bytes above which (LZ4) compression is enforced; when set to zero, deactivates compression. Added in MySQL 5.7.17.
- group\_replication\_enforce\_update\_everywhere\_checks: Enable or disable strict consistency checks for multi-source update everywhere. Added in MySQL 5.7.17.
- group\_replication\_exit\_state\_action: How instance behaves when it leaves group involuntarily. Added in MySQL 5.7.24.
- group\_replication\_flow\_control\_applier\_threshold: Number of waiting transactions in applier queue which trigger flow control. Added in MySQL 5.7.17.
- group\_replication\_flow\_control\_certifier\_threshold: Number of waiting transactions in certifier queue that trigger flow control. Added in MySQL 5.7.17.

- group\_replication\_flow\_control\_mode: Mode used for flow control. Added in MySQL 5.7.17.
- group\_replication\_force\_members: Comma separated list of peer addresses, such as host1:port1,host2:port2. Added in MySQL 5.7.17.
- group\_replication\_group\_name: Name of group. Added in MySQL 5.7.17.
- group\_replication\_group\_seeds: List of peer addresses, comma separated list such as host1:port1,host2:port2. Added in MySQL 5.7.17.
- group\_replication\_gtid\_assignment\_block\_size: Number of consecutive GTIDs that are reserved for each member; each member consumes its blocks and reserves more when needed. Added in MySQL 5.7.17.
- group\_replication\_ip\_whitelist: List of hosts permitted to connect to group. Added in MySQL 5.7.17.
- group\_replication\_local\_address: Local address in host:port format. Added in MySQL 5.7.17.
- group\_replication\_member\_weight: Chance of this member being elected as primary. Added in MySQL 5.7.20.
- group\_replication\_poll\_spin\_loops: Number of times group communication thread waits. Added in MySQL 5.7.17.
- group\_replication\_recovery\_complete\_at: Recovery policies when handling cached transactions after state transfer. Added in MySQL 5.7.17.
- group\_replication\_recovery\_reconnect\_interval: Sleep time, in seconds, between reconnection attempts when no donor was found in group. Added in MySQL 5.7.17.
- group\_replication\_recovery\_retry\_count: Number of times that joining member tries to connect to available donors before giving up. Added in MySQL 5.7.17.
- group\_replication\_recovery\_ssl\_ca: File that contains list of trusted SSL Certificate Authorities. Added in MySQL 5.7.17.
- group\_replication\_recovery\_ssl\_capath: Directory that contains trusted SSL Certificate Authority certificate files. Added in MySQL 5.7.17.
- group\_replication\_recovery\_ssl\_cert: Name of SSL certificate file to use for establishing encrypted connection. Added in MySQL 5.7.17.
- group\_replication\_recovery\_ssl\_cipher: Permissible ciphers for SSL encryption. Added in MySQL 5.7.17.
- group\_replication\_recovery\_ssl\_crl: File that contains certificate revocation lists. Added in MySQL 5.7.17.
- group\_replication\_recovery\_ssl\_crlpath: Directory that contains certificate revocation-list files. Added in MySQL 5.7.17.
- group\_replication\_recovery\_ssl\_key: Name of SSL key file to use for establishing encrypted connection. Added in MySQL 5.7.17.
- group\_replication\_recovery\_ssl\_verify\_server\_cert: Make recovery process check server Common Name value in certificate sent by donor. Added in MySQL 5.7.17.
- group\_replication\_recovery\_use\_ssl: Whether Group Replication recovery connection should use SSL. Added in MySQL 5.7.17.

- group\_replication\_single\_primary\_mode: Instructs group to use single server for read/write workload. Added in MySQL 5.7.17.
- group\_replication\_ssl\_mode: Desired security state of connection between Group Replication members. Added in MySQL 5.7.17.
- group\_replication\_start\_on\_boot: Whether server should start Group Replication during server startup. Added in MySQL 5.7.17.
- group\_replication\_transaction\_size\_limit: Sets maximum size of transaction in bytes which group accepts. Added in MySQL 5.7.19.
- group\_replication\_unreachable\_majority\_timeout: How long to wait for network partitions that result in minority to leave group. Added in MySQL 5.7.19.
- gtid\_executed\_compression\_period: Compress gtid\_executed table each time this many transactions have occurred. 0 means never compress this table. Applies only when binary logging is disabled. Added in MySQL 5.7.6.
- have\_statement\_timeout: Whether statement execution timeout is available. Added in MySQL 5.7.4.
- initialize: Whether to run in initialization mode (secure). Added in MySQL 5.7.6.
- initialize-insecure: Whether to run in initialization mode (insecure). Added in MySQL 5.7.6.
- innodb\_adaptive\_hash\_index\_parts: Partitions adaptive hash index search system into n partitions, with each partition protected by separate latch. Each index is bound to specific partition based on space ID and index ID attributes. Added in MySQL 5.7.8.
- innodb\_background\_drop\_list\_empty: Delays table creation until background drop list is empty (debug). Added in MySQL 5.7.10.
- innodb\_buffer\_pool\_chunk\_size: Chunk size used when resizing buffer pool. Added in MySQL 5.7.5.
- innodb\_buffer\_pool\_dump\_pct: Percentage of most recently used pages for each buffer pool to read out and dump. Added in MySQL 5.7.2.
- innodb\_compress\_debug: Compresses all tables using specified compression algorithm. Added in MySQL 5.7.8.
- innodb\_deadlock\_detect: Enables or disables deadlock detection. Added in MySQL 5.7.15.
- innodb\_default\_row\_format: Default row format for InnoDB tables. Added in MySQL 5.7.9.
- innodb\_disable\_resize\_buffer\_pool\_debug: Disables resizing of InnoDB buffer pool. Added in MySQL 5.7.6.
- innodb\_fill\_factor: Percentage for B-tree leaf and non-leaf page space to be filled with data. Remaining space is reserved for future growth. Added in MySQL 5.7.5.
- innodb\_flush\_sync: Enable innodb\_flush\_sync to ignore the innodb\_io\_capacity and innodb\_io\_capacity\_max settings for bursts of I/O activity that occur at checkpoints. Disable innodb\_flush\_sync to adhere to limits on I/O activity as defined by innodb\_io\_capacity and innodb\_io\_capacity\_max. Added in MySQL 5.7.8.
- innodb\_ft\_result\_cache\_limit: InnoDB FULLTEXT search query result cache limit. Added in MySQL 5.7.2.
- innodb\_ft\_total\_cache\_size: Total memory allocated for InnoDB FULLTEXT search index cache. Added in MySQL 5.7.2.

- innodb\_log\_checkpoint\_now: Debug option that forces InnoDB to write checkpoint. Added in MySQL 5.7.2.
- innodb\_log\_checksum\_algorithm: Specifies how to generate and verify checksum stored in each redo log disk block. Added in MySQL 5.7.8.
- innodb\_log\_checksums: Enables or disables checksums for redo log pages. Added in MySQL 5.7.9.
- innodb\_log\_write\_ahead\_size: Redo log write-ahead block size. Added in MySQL 5.7.4.
- innodb\_max\_undo\_log\_size: Sets threshold for truncating InnoDB undo log. Added in MySQL 5.7.5.
- innodb\_merge\_threshold\_set\_all\_debug: Overrides current MERGE\_THRESHOLD setting with specified value for all indexes that are currently in dictionary cache. Added in MySQL 5.7.6.
- innodb\_numa\_interleave: Enables NUMA MPOL\_INTERLEAVE memory policy for allocation of InnoDB buffer pool. Added in MySQL 5.7.9.
- innodb\_optimize\_point\_storage: Enable this option to store POINT data as fixed-length data rather than variable-length data. Added in MySQL 5.7.5.
- innodb\_page\_cleaners: Number of page cleaner threads. Added in MySQL 5.7.4.
- innodb\_purge\_rseg\_truncate\_frequency: Rate at which undo log purge should be invoked as part of purge action. Value = n invokes undo log purge on every nth iteration of purge invocation. Added in MySQL 5.7.5.
- innodb\_stats\_include\_delete\_marked: Include delete-marked records when calculating persistent InnoDB statistics. Added in MySQL 5.7.17.
- innodb\_status\_output: Used to enable or disable periodic output for standard InnoDB Monitor. Also used in combination with innodb\_status\_output\_locks to enable and disable periodic output for InnoDB Lock Monitor. Added in MySQL 5.7.4.
- innodb\_status\_output\_locks: Used to enable or disable periodic output for standard InnoDB Lock Monitor. innodb\_status\_output must also be enabled to produce periodic output for InnoDB Lock Monitor. Added in MySQL 5.7.4.
- innodb\_sync\_debug: Enables InnoDB sync debug checking. Added in MySQL 5.7.8.
- innodb\_temp\_data\_file\_path: Path to temporary tablespace data files and their sizes. Added in MySQL 5.7.1.
- innodb\_tmpdir: Directory location for temporary table files created during online ALTER TABLE operations. Added in MySQL 5.7.11.
- innodb\_undo\_log\_truncate: Enable this option to mark InnoDB undo tablespace for truncation. Added in MySQL 5.7.5.
- internal\_tmp\_disk\_storage\_engine: Storage engine for internal temporary tables. Added in MySQL 5.7.5.
- keyring-migration-destination: Key migration destination keyring plugin. Added in MySQL 5.7.21.
- keyring-migration-host: Host name for connecting to running server for key migration. Added in MySQL 5.7.21.
- keyring-migration-password: Password for connecting to running server for key migration. Added in MySQL 5.7.21.
- keyring-migration-port: TCP/IP port number for connecting to running server for key migration. Added in MySQL 5.7.21.

- keyring-migration-socket: Unix socket file or Windows named pipe for connecting to running server for key migration. Added in MySQL 5.7.21.
- keyring-migration-source: Key migration source keyring plugin. Added in MySQL 5.7.21.
- keyring-migration-user: User name for connecting to running server for key migration. Added in MySQL 5.7.21.
- keyring\_aws\_cmk\_id: AWS keyring plugin customer master key ID value. Added in MySQL 5.7.19.
- keyring\_aws\_conf\_file: AWS keyring plugin configuration file location. Added in MySQL 5.7.19.
- keyring\_aws\_data\_file: AWS keyring plugin storage file location. Added in MySQL 5.7.19.
- keyring\_aws\_region: AWS keyring plugin region. Added in MySQL 5.7.19.
- keyring\_encrypted\_file\_data: keyring\_encrypted\_file plugin data file. Added in MySQL 5.7.21.
- keyring\_encrypted\_file\_password: keyring\_encrypted\_file plugin password. Added in MySQL 5.7.21.
- keyring\_file\_data: keyring\_file plugin data file. Added in MySQL 5.7.11.
- keyring\_okv\_conf\_dir: Oracle Key Vault keyring plugin configuration directory. Added in MySQL 5.7.12.
- keyring\_operations: Whether keyring operations are enabled. Added in MySQL 5.7.21.
- log\_backward\_compatible\_user\_definitions: Whether to log CREATE/ALTER USER, GRANT in backward-compatible fashion. Added in MySQL 5.7.6.
- log\_builtin\_as\_identified\_by\_password: Whether to log CREATE/ALTER USER, GRANT in backward-compatible fashion. Added in MySQL 5.7.9.
- log\_error\_verbosity: Error logging verbosity level. Added in MySQL 5.7.2.
- log\_slow\_admin\_statements: Log slow OPTIMIZE, ANALYZE, ALTER and other administrative statements to slow query log if it is open. Added in MySQL 5.7.1.
- log\_slow\_slave\_statements: Cause slow statements as executed by replica to be written to slow query log. Added in MySQL 5.7.1.
- log\_statements\_unsafe\_for\_binlog: Disables error 1592 warnings being written to error log. Added in MySQL 5.7.11.
- log\_syslog: Whether to write error log to syslog. Added in MySQL 5.7.5.
- log\_syslog\_facility: Facility for syslog messages. Added in MySQL 5.7.5.
- log\_syslog\_include\_pid: Whether to include server PID in syslog messages. Added in MySQL 5.7.5.
- log\_syslog\_tag: Tag for server identifier in syslog messages. Added in MySQL 5.7.5.
- log\_timestamps: Log timestamp format. Added in MySQL 5.7.2.
- max\_digest\_length: Maximum digest size in bytes. Added in MySQL 5.7.6.
- max\_execution\_time: Statement execution timeout value. Added in MySQL 5.7.8.
- max\_points\_in\_geometry: Maximum number of points in geometry values for ST\_Buffer\_Strategy(). Added in MySQL 5.7.8.
- max\_statement\_time: Statement execution timeout value. Added in MySQL 5.7.4.

- mecab\_charset: Character set currently used by MeCab full-text parser plugin. Added in MySQL 5.7.6.
- mecab\_rc\_file: Path to mecabrc configuration file for MeCab parser for full-text search. Added in MySQL 5.7.6.
- mysql\_firewall\_mode: Whether MySQL Enterprise Firewall plugin is operational. Added in MySQL 5.7.9.
- mysql\_firewall\_trace: Whether to enable MySQL Enterprise Firewall plugin trace. Added in MySQL 5.7.9.
- mysql\_native\_password\_proxy\_users: Whether mysql\_native\_password authentication plugin does proxying. Added in MySQL 5.7.7.
- mysqlx: Whether X Plugin is initialized. Added in MySQL 5.7.12.
- mysqlx\_bind\_address: Network address X Plugin uses for connections. Added in MySQL 5.7.17.
- mysqlx\_connect\_timeout: Maximum permitted waiting time in seconds for a connection to set up a session. Added in MySQL 5.7.12.
- mysqlx\_idle\_worker\_thread\_timeout: Time in seconds after which idle worker threads are terminated. Added in MySQL 5.7.12.
- mysqlx\_max\_allowed\_packet: Maximum size of network packets that can be received by X Plugin. Added in MySQL 5.7.12.
- mysqlx\_max\_connections: Maximum number of concurrent client connections X Plugin can accept. Added in MySQL 5.7.12.
- mysqlx\_min\_worker\_threads: Minimum number of worker threads used for handling client requests. Added in MySQL 5.7.12.
- mysqlx\_port: Port number on which X Plugin accepts TCP/IP connections. Added in MySQL 5.7.12.
- mysqlx\_port\_open\_timeout: Time which X Plugin waits when accepting connections. Added in MySQL 5.7.17.
- mysqlx\_socket: Path to socket where X Plugin listens for connections. Added in MySQL 5.7.15.
- mysqlx\_ssl\_ca: File that contains list of trusted SSL Certificate Authorities. Added in MySQL 5.7.12.
- mysqlx\_ssl\_capath: Directory that contains trusted SSL Certificate Authority certificate files. Added in MySQL 5.7.12.
- mysqlx\_ssl\_cert: File that contains X.509 certificate. Added in MySQL 5.7.12.
- mysqlx\_ssl\_cipher: Permissible ciphers for connection encryption. Added in MySQL 5.7.12.
- mysqlx\_ssl\_crl: File that contains certificate revocation lists. Added in MySQL 5.7.12.
- mysqlx\_ssl\_crlpath: Directory that contains certificate revocation list files. Added in MySQL 5.7.12.
- mysqlx\_ssl\_key: File that contains X.509 key. Added in MySQL 5.7.12.
- named\_pipe\_full\_access\_group: Name of Windows group granted full access to named pipe. Added in MySQL 5.7.25.
- ngram\_token\_size: Defines n-gram token size for full-text search ngram parser. Added in MySQL 5.7.6.

- offline\_mode: Whether server is offline. Added in MySQL 5.7.5.
- parser\_max\_mem\_size: Maximum amount of memory available to parser. Added in MySQL 5.7.12.
- performance-schema-consumer-events-transactions-current: Configure eventstransactions-current consumer. Added in MySQL 5.7.3.
- performance-schema-consumer-events-transactions-history: Configure eventstransactions-history consumer. Added in MySQL 5.7.3.
- performance-schema-consumer-events-transactions-history-long: Configure eventstransactions-history-long consumer. Added in MySQL 5.7.3.
- performance\_schema\_events\_transactions\_history\_long\_size: Number of rows in events\_transactions\_history\_long table. Added in MySQL 5.7.3.
- performance\_schema\_events\_transactions\_history\_size: Number of rows per thread in events\_transactions\_history table. Added in MySQL 5.7.3.
- performance\_schema\_max\_digest\_length: Maximum Performance Schema digest size in bytes. Added in MySQL 5.7.8.
- performance\_schema\_max\_index\_stat: Maximum number of indexes to keep statistics for. Added in MySQL 5.7.6.
- performance\_schema\_max\_memory\_classes: Maximum number of memory instruments. Added in MySQL 5.7.2.
- performance\_schema\_max\_metadata\_locks: Maximum number of metadata locks to track. Added in MySQL 5.7.3.
- performance\_schema\_max\_prepared\_statements\_instances: Number of rows in prepared\_statements\_instances table. Added in MySQL 5.7.4.
- performance\_schema\_max\_program\_instances: Maximum number of stored programs for statistics. Added in MySQL 5.7.2.
- performance\_schema\_max\_sql\_text\_length: Maximum number of bytes stored from SQL statements. Added in MySQL 5.7.6.
- performance\_schema\_max\_statement\_stack: Maximum stored program nesting for statistics. Added in MySQL 5.7.2.
- performance\_schema\_max\_table\_lock\_stat: Maximum number of tables to keep lock statistics for. Added in MySQL 5.7.6.
- performance\_schema\_show\_processlist: Select SHOW PROCESSLIST implementation. Added in MySQL 5.7.39.
- range\_optimizer\_max\_mem\_size: Limit on range optimizer memory consumption. Added in MySQL 5.7.9.
- rbr\_exec\_mode: Allows for switching server between IDEMPOTENT mode (key and some other errors suppressed) and STRICT mode; STRICT mode is default. Added in MySQL 5.7.1.
- replication\_optimize\_for\_static\_plugin\_config: Shared locks for semisynchronous replication. Added in MySQL 5.7.33.
- replication\_sender\_observe\_commit\_only: Limited callbacks for semisynchronous replication. Added in MySQL 5.7.33.
- require\_secure\_transport: Whether client connections must use secure transport. Added in MySQL 5.7.8.

- rewriter\_enabled: Whether query rewrite plugin is enabled. Added in MySQL 5.7.6.
- rewriter\_verbose: For internal use. Added in MySQL 5.7.6.
- rpl\_semi\_sync\_master\_wait\_for\_slave\_count: Number of replica acknowledgments source must receive per transaction before proceeding. Added in MySQL 5.7.3.
- rpl\_semi\_sync\_master\_wait\_point: Wait point for replica transaction receipt acknowledgment. Added in MySQL 5.7.2.
- rpl\_stop\_slave\_timeout: Number of seconds that STOP REPLICA or STOP SLAVE waits before timing out. Added in MySQL 5.7.2.
- session\_track\_gtids: Enables tracker which can be set to track different GTIDs. Added in MySQL 5.7.6.
- session\_track\_schema: Whether to track schema changes. Added in MySQL 5.7.4.
- session\_track\_state\_change: Whether to track session state changes. Added in MySQL 5.7.4.
- session\_track\_system\_variables: Session variables to track changes for. Added in MySQL 5.7.4.
- session\_track\_transaction\_info: How to perform transaction tracking. Added in MySQL 5.7.8.
- sha256\_password\_auto\_generate\_rsa\_keys: Whether to generate RSA key-pair files automatically. Added in MySQL 5.7.5.
- sha256\_password\_proxy\_users: Whether sha256\_password authentication plugin does proxying. Added in MySQL 5.7.7.
- show\_compatibility\_56: Compatibility for SHOW STATUS/VARIABLES. Added in MySQL 5.7.6.
- show\_create\_table\_verbosity: Whether to display ROW\_FORMAT in SHOW CREATE TABLE even if it has default value. Added in MySQL 5.7.22.
- show\_old\_temporals: Whether SHOW CREATE TABLE should indicate pre-5.6.4 temporal columns. Added in MySQL 5.7.6.
- simplified\_binlog\_gtid\_recovery: Renamed to binlog\_gtid\_simple\_recovery. Added in MySQL 5.7.5.
- slave\_parallel\_type: Tells replica to use timestamp information (LOGICAL\_CLOCK) or database partioning (DATABASE) to parallelize transactions. Added in MySQL 5.7.2.
- slave\_preserve\_commit\_order: Ensures that all commits by replica workers happen in same order as on source to maintain consistency when using parallel applier threads. Added in MySQL 5.7.5.
- super\_read\_only: Whether to ignore SUPER exceptions to read-only mode. Added in MySQL 5.7.8.
- thread\_pool\_algorithm: Thread pool algorithm. Added in MySQL 5.7.9.
- thread\_pool\_high\_priority\_connection: Whether current session is high priority. Added in MySQL 5.7.9.
- thread\_pool\_max\_unused\_threads: Maximum permissible number of unused threads. Added in MySQL 5.7.9.
- thread\_pool\_prio\_kickup\_timer: How long before statement is moved to high-priority execution. Added in MySQL 5.7.9.
- thread\_pool\_size: Number of thread groups in thread pool. Added in MySQL 5.7.9.

- thread\_pool\_stall\_limit: How long before statement is defined as stalled. Added in MySQL 5.7.9.
- tls\_version: Permissible TLS protocols for encrypted connections. Added in MySQL 5.7.10.
- transaction\_write\_set\_extraction: Defines algorithm used to hash writes extracted during transaction. Added in MySQL 5.7.6.
- validate\_password\_check\_user\_name: Whether to check passwords against user name. Added in MySQL 5.7.15.
- validate\_password\_dictionary\_file\_last\_parsed: When dictionary file was last parsed. Added in MySQL 5.7.8.
- validate\_password\_dictionary\_file\_words\_count: Number of words in dictionary file. Added in MySQL 5.7.8.
- version\_tokens\_session: Client token list for Version Tokens. Added in MySQL 5.7.8.
- version\_tokens\_session\_number: For internal use. Added in MySQL 5.7.8.

## <span id="page-64-0"></span>**Options and Variables Deprecated in MySQL 5.7**

The following system variables, status variables, and options have been deprecated in MySQL 5.7.

- Innodb\_available\_undo\_logs: Total number of InnoDB rollback segments; different from innodb\_rollback\_segments, which displays number of active rollback segments. Deprecated in MySQL 5.7.19.
- Qcache\_free\_blocks: Number of free memory blocks in query cache. Deprecated in MySQL 5.7.20.
- Qcache\_free\_memory: Amount of free memory for query cache. Deprecated in MySQL 5.7.20.
- Qcache\_hits: Number of query cache hits. Deprecated in MySQL 5.7.20.
- Qcache\_inserts: Number of query cache inserts. Deprecated in MySQL 5.7.20.
- Qcache\_lowmem\_prunes: Number of queries which were deleted from query cache due to lack of free memory in cache. Deprecated in MySQL 5.7.20.
- Qcache\_not\_cached: Number of noncached queries (not cacheable, or not cached due to query\_cache\_type setting). Deprecated in MySQL 5.7.20.
- Qcache\_queries\_in\_cache: Number of queries registered in query cache. Deprecated in MySQL 5.7.20.
- Qcache\_total\_blocks: Total number of blocks in query cache. Deprecated in MySQL 5.7.20.
- Slave\_heartbeat\_period: Replica's replication heartbeat interval, in seconds. Deprecated in MySQL 5.7.6.
- Slave\_last\_heartbeat: Shows when latest heartbeat signal was received, in TIMESTAMP format. Deprecated in MySQL 5.7.6.
- Slave\_received\_heartbeats: Number of heartbeats received by replica since previous reset. Deprecated in MySQL 5.7.6.
- Slave\_retried\_transactions: Total number of times since startup that replication SQL thread has retried transactions. Deprecated in MySQL 5.7.6.
- Slave\_running: State of this server as replica (replication I/O thread status). Deprecated in MySQL 5.7.6.

- avoid\_temporal\_upgrade: Whether ALTER TABLE should upgrade pre-5.6.4 temporal columns. Deprecated in MySQL 5.7.6.
- binlog\_max\_flush\_queue\_time: How long to read transactions before flushing to binary log. Deprecated in MySQL 5.7.9.
- bootstrap: Used by mysql installation scripts. Deprecated in MySQL 5.7.6.
- des-key-file: Load keys for des\_encrypt() and des\_encrypt from given file. Deprecated in MySQL 5.7.6.
- disable-partition-engine-check: Whether to disable startup check for tables without native partitioning. Deprecated in MySQL 5.7.17.
- group\_replication\_allow\_local\_disjoint\_gtids\_join: Allow current server to join group even if it has transactions not present in group. Deprecated in MySQL 5.7.21.
- have\_crypt: Availability of crypt() system call. Deprecated in MySQL 5.7.6.
- have\_query\_cache: Whether mysqld supports query cache. Deprecated in MySQL 5.7.20.
- ignore-db-dir: Treat directory as nondatabase directory. Deprecated in MySQL 5.7.16.
- ignore\_db\_dirs: Directories treated as nondatabase directories. Deprecated in MySQL 5.7.16.
- innodb: Enable InnoDB (if this version of MySQL supports it). Deprecated in MySQL 5.7.5.
- innodb\_file\_format: Format for new InnoDB tables. Deprecated in MySQL 5.7.7.
- innodb\_file\_format\_check: Whether InnoDB performs file format compatibility checking. Deprecated in MySQL 5.7.7.
- innodb\_file\_format\_max: File format tag in shared tablespace. Deprecated in MySQL 5.7.7.
- innodb\_large\_prefix: Enables longer keys for column prefix indexes. Deprecated in MySQL 5.7.7.
- innodb\_support\_xa: Enable InnoDB support for XA two-phase commit. Deprecated in MySQL 5.7.10.
- innodb\_undo\_logs: Number of undo logs (rollback segments) used by InnoDB; alias for innodb\_rollback\_segments. Deprecated in MySQL 5.7.19.
- innodb\_undo\_tablespaces: Number of tablespace files that rollback segments are divided between. Deprecated in MySQL 5.7.21.
- log-warnings: Write some noncritical warnings to log file. Deprecated in MySQL 5.7.2.
- metadata\_locks\_cache\_size: Size of metadata locks cache. Deprecated in MySQL 5.7.4.
- metadata\_locks\_hash\_instances: Number of metadata lock hashes. Deprecated in MySQL 5.7.4.
- myisam\_repair\_threads: Number of threads to use when repairing MyISAM tables. 1 disables parallel repair. Deprecated in MySQL 5.7.38.
- old\_passwords: Selects password hashing method for PASSWORD(). Deprecated in MySQL 5.7.6.
- partition: Enable (or disable) partitioning support. Deprecated in MySQL 5.7.16.
- query\_cache\_limit: Do not cache results that are bigger than this. Deprecated in MySQL 5.7.20.
- query\_cache\_min\_res\_unit: Minimal size of unit in which space for results is allocated (last unit is trimmed after writing all result data). Deprecated in MySQL 5.7.20.

- query\_cache\_size: Memory allocated to store results from old queries. Deprecated in MySQL 5.7.20.
- query\_cache\_type: Query cache type. Deprecated in MySQL 5.7.20.
- query\_cache\_wlock\_invalidate: Invalidate queries in query cache on LOCK for write. Deprecated in MySQL 5.7.20.
- secure\_auth: Disallow authentication for accounts that have old (pre-4.1) passwords. Deprecated in MySQL 5.7.5.
- show\_compatibility\_56: Compatibility for SHOW STATUS/VARIABLES. Deprecated in MySQL 5.7.6.
- show\_old\_temporals: Whether SHOW CREATE TABLE should indicate pre-5.6.4 temporal columns. Deprecated in MySQL 5.7.6.
- skip-partition: Do not enable user-defined partitioning. Deprecated in MySQL 5.7.16.
- sync\_frm: Sync .frm to disk on create. Enabled by default. Deprecated in MySQL 5.7.6.
- temp-pool: Using this option causes most temporary files created to use small set of names, rather than unique name for each new file. Deprecated in MySQL 5.7.18.
- tx\_isolation: Default transaction isolation level. Deprecated in MySQL 5.7.20.
- tx\_read\_only: Default transaction access mode. Deprecated in MySQL 5.7.20.

## <span id="page-66-0"></span>**Options and Variables Removed in MySQL 5.7**

The following system variables, status variables, and options have been removed in MySQL 5.7.

- Com\_show\_slave\_status\_nonblocking: Count of SHOW REPLICA | SLAVE STATUS NONBLOCKING statements. Removed in MySQL 5.7.6.
- Max\_statement\_time\_exceeded: Number of statements that exceeded execution timeout value. Removed in MySQL 5.7.8.
- Max\_statement\_time\_set: Number of statements for which execution timeout was set. Removed in MySQL 5.7.8.
- Max\_statement\_time\_set\_failed: Number of statements for which execution timeout setting failed. Removed in MySQL 5.7.8.
- binlogging\_impossible\_mode: Deprecated and later removed. Use binlog\_error\_action instead. Removed in MySQL 5.7.6.
- default-authentication-plugin: Default authentication plugin. Removed in MySQL 5.7.2.
- executed\_gtids\_compression\_period: Renamed to gtid\_executed\_compression\_period. Removed in MySQL 5.7.6.
- innodb\_additional\_mem\_pool\_size: Size of memory pool InnoDB uses to store data dictionary information and other internal data structures. Removed in MySQL 5.7.4.
- innodb\_log\_checksum\_algorithm: Specifies how to generate and verify checksum stored in each redo log disk block. Removed in MySQL 5.7.9.
- innodb\_optimize\_point\_storage: Enable this option to store POINT data as fixed-length data rather than variable-length data. Removed in MySQL 5.7.6.
- innodb\_use\_sys\_malloc: Whether InnoDB uses OS or own memory allocator. Removed in MySQL 5.7.4.

- log-slow-admin-statements: Log slow OPTIMIZE, ANALYZE, ALTER and other administrative statements to slow query log if it is open. Removed in MySQL 5.7.1.
- log-slow-slave-statements: Cause slow statements as executed by replica to be written to slow query log. Removed in MySQL 5.7.1.
- log\_backward\_compatible\_user\_definitions: Whether to log CREATE/ALTER USER, GRANT in backward-compatible fashion. Removed in MySQL 5.7.9.
- max\_statement\_time: Statement execution timeout value. Removed in MySQL 5.7.8.
- myisam\_repair\_threads: Number of threads to use when repairing MyISAM tables. 1 disables parallel repair. Removed in MySQL 5.7.39.
- simplified\_binlog\_gtid\_recovery: Renamed to binlog\_gtid\_simple\_recovery. Removed in MySQL 5.7.6.
- storage\_engine: Default storage engine. Removed in MySQL 5.7.5.
- thread\_concurrency: Permits application to provide hint to threads system for desired number of threads which should be run at one time. Removed in MySQL 5.7.2.
- timed\_mutexes: Specify whether to time mutexes (only InnoDB mutexes are currently supported). Removed in MySQL 5.7.5.

## <span id="page-67-0"></span>**1.5 How to Report Bugs or Problems**

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

Writing a good bug report takes patience, but doing it right the first time saves time both for us and for yourself. A good bug report, containing a full test case for the bug, makes it very likely that we will fix the bug in the next release. This section helps you write your report correctly so that you do not waste your time doing things that may not help us much or at all. Please read this section carefully and make sure that all the information described here is included in your report.

Preferably, you should test the problem using the latest production or development version of MySQL Server before posting. Anyone should be able to repeat the bug by just using mysql test < script\_file on your test case or by running the shell or Perl script that you include in the bug report. Any bug that we are able to repeat has a high chance of being fixed in the next MySQL release.

It is most helpful when a good description of the problem is included in the bug report. That is, give a good example of everything you did that led to the problem and describe, in exact detail, the problem itself. The best reports are those that include a full example showing how to reproduce the bug or problem. See Section 5.8, "Debugging MySQL".

Remember that it is possible for us to respond to a report containing too much information, but not to one containing too little. People often omit facts because they think they know the cause of a problem and assume that some details do not matter. A good principle to follow is that if you are in doubt about stating something, state it. It is faster and less troublesome to write a couple more lines in your report than to wait longer for the answer if we must ask you to provide information that was missing from the initial report.

The most common errors made in bug reports are (a) not including the version number of the MySQL distribution that you use, and (b) not fully describing the platform on which the MySQL server is installed (including the platform type and version number). These are highly relevant pieces of information, and in 99 cases out of 100, the bug report is useless without them. Very often we get questions like, "Why doesn't this work for me?" Then we find that the feature requested wasn't implemented in that MySQL version, or that a bug described in a report has been fixed in newer MySQL versions. Errors often are platform-dependent. In such cases, it is next to impossible for us to fix anything without knowing the operating system and the version number of the platform.

If you compiled MySQL from source, remember also to provide information about your compiler if it is related to the problem. Often people find bugs in compilers and think the problem is MySQLrelated. Most compilers are under development all the time and become better version by version. To determine whether your problem depends on your compiler, we need to know what compiler you used. Note that every compiling problem should be regarded as a bug and reported accordingly.

If a program produces an error message, it is very important to include the message in your report. If we try to search for something from the archives, it is better that the error message reported exactly matches the one that the program produces. (Even the lettercase should be observed.) It is best to copy and paste the entire error message into your report. You should never try to reproduce the message from memory.

If you have a problem with Connector/ODBC (MyODBC), please try to generate a trace file and send it with your report. See [How to Report Connector/ODBC Problems or Bugs.](https://dev.mysql.com/doc/connector-odbc/en/connector-odbc-support-bug-report.md)

If your report includes long query output lines from test cases that you run with the mysql commandline tool, you can make the output more readable by using the --vertical option or the \G statement terminator. The EXPLAIN SELECT example later in this section demonstrates the use of \G.

Please include the following information in your report:

• The version number of the MySQL distribution you are using (for example, MySQL 5.7.10). You can find out which version you are running by executing mysqladmin version. The mysqladmin program can be found in the bin directory under your MySQL installation directory.

- The manufacturer and model of the machine on which you experience the problem.
- The operating system name and version. If you work with Windows, you can usually get the name and version number by double-clicking your My Computer icon and pulling down the "Help/About Windows" menu. For most Unix-like operating systems, you can get this information by executing the command uname -a.
- Sometimes the amount of memory (real and virtual) is relevant. If in doubt, include these values.
- The contents of the docs/INFO\_BIN file from your MySQL installation. This file contains information about how MySQL was configured and compiled.
- If you are using a source distribution of the MySQL software, include the name and version number of the compiler that you used. If you have a binary distribution, include the distribution name.
- If the problem occurs during compilation, include the exact error messages and also a few lines of context around the offending code in the file where the error occurs.
- If mysqld died, you should also report the statement that caused mysqld to unexpectedly exit. You can usually get this information by running mysqld with query logging enabled, and then looking in the log after mysqld exits. See Section 5.8, "Debugging MySQL".
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

• If a bug or problem occurs while running mysqld, try to provide an input script that reproduces the anomaly. This script should include any necessary source files. The more closely the script can

reproduce your situation, the better. If you can make a reproducible test case, you should upload it to be attached to the bug report.

If you cannot provide a script, you should at least include the output from mysqladmin variables extended-status processlist in your report to provide some information on how your system is performing.

- If you cannot produce a test case with only a few rows, or if the test table is too big to be included in the bug report (more than 10 rows), you should dump your tables using mysqldump and create a README file that describes your problem. Create a compressed archive of your files using tar and gzip or zip. After you initiate a bug report for our bugs database at<http://bugs.mysql.com/>, click the Files tab in the bug report for instructions on uploading the archive to the bugs database.
- If you believe that the MySQL server produces a strange result from a statement, include not only the result, but also your opinion of what the result should be, and an explanation describing the basis for your opinion.
- When you provide an example of the problem, it is better to use the table names, variable names, and so forth that exist in your actual situation than to come up with new names. The problem could be related to the name of a table or variable. These cases are rare, perhaps, but it is better to be safe than sorry. After all, it should be easier for you to provide an example that uses your actual situation, and it is by all means better for us. If you have data that you do not want to be visible to others in the bug report, you can upload it using the Files tab as previously described. If the information is really top secret and you do not want to show it even to us, go ahead and provide an example using other names, but please regard this as the last choice.
- Include all the options given to the relevant programs, if possible. For example, indicate the options that you use when you start the mysqld server, as well as the options that you use to run any MySQL client programs. The options to programs such as mysqld and mysql, and to the configure script, are often key to resolving problems and are very relevant. It is never a bad idea to include them. If your problem involves a program written in a language such as Perl or PHP, please include the language processor's version number, as well as the version for any modules that the program uses. For example, if you have a Perl script that uses the DBI and DBD::mysql modules, include the version numbers for Perl, DBI, and DBD::mysql.
- If your question is related to the privilege system, please include the output of mysqladmin reload, and all the error messages you get when trying to connect. When you test your privileges, you should execute mysqladmin reload version and try to connect with the program that gives you trouble.
- If you have a patch for a bug, do include it. But do not assume that the patch is all we need, or that we can use it, if you do not provide some necessary information such as test cases showing the bug that your patch fixes. We might find problems with your patch or we might not understand it at all. If so, we cannot use it.

If we cannot verify the exact purpose of the patch, we will not use it. Test cases help us here. Show that the patch handles all the situations that may occur. If we find a borderline case (even a rare one) where the patch will not work, it may be useless.

- Guesses about what the bug is, why it occurs, or what it depends on are usually wrong. Even the MySQL team cannot guess such things without first using a debugger to determine the real cause of a bug.
- Indicate in your bug report that you have checked the reference manual and mail archive so that others know you have tried to solve the problem yourself.
- If your data appears corrupt or you get errors when you access a particular table, first check your tables with CHECK TABLE. If that statement reports any errors:
  - The InnoDB crash recovery mechanism handles cleanup when the server is restarted after being killed, so in typical operation there is no need to "repair" tables. If you encounter an error with

InnoDB tables, restart the server and see whether the problem persists, or whether the error affected only cached data in memory. If data is corrupted on disk, consider restarting with the innodb\_force\_recovery option enabled so that you can dump the affected tables.

• For non-transactional tables, try to repair them with REPAIR TABLE or with myisamchk. See Chapter 5, MySQL Server Administration.

If you are running Windows, please verify the value of lower\_case\_table\_names using the SHOW VARIABLES LIKE 'lower\_case\_table\_names' statement. This variable affects how the server handles lettercase of database and table names. Its effect for a given value should be as described in Section 9.2.3, "Identifier Case Sensitivity".

- If you often get corrupted tables, you should try to find out when and why this happens. In this case, the error log in the MySQL data directory may contain some information about what happened. (This is the file with the .err suffix in the name.) See Section 5.4.2, "The Error Log". Please include any relevant information from this file in your bug report. Normally mysqld should never corrupt a table if nothing killed it in the middle of an update. If you can find the cause of mysqld dying, it is much easier for us to provide you with a fix for the problem. See Section B.3.1, "How to Determine What Is Causing a Problem".
- If possible, download and install the most recent version of MySQL Server and check whether it solves your problem. All versions of the MySQL software are thoroughly tested and should work without problems. We believe in making everything as backward-compatible as possible, and you should be able to switch MySQL versions without difficulty. See [Section 2.1.2, "Which MySQL](#page-85-1) [Version and Distribution to Install".](#page-85-1)

## <span id="page-71-0"></span>**1.6 MySQL Standards Compliance**

This section describes how MySQL relates to the ANSI/ISO SQL standards. MySQL Server has many extensions to the SQL standard, and here you can find out what they are and how to use them. You can also find information about functionality missing from MySQL Server, and how to work around some of the differences.

The SQL standard has been evolving since 1986 and several versions exist. In this manual, "SQL-92" refers to the standard released in 1992. "SQL:1999", "SQL:2003", "SQL:2008", and "SQL:2011" refer to the versions of the standard released in the corresponding years, with the last being the most recent version. We use the phrase "the SQL standard" or "standard SQL" to mean the current version of the SQL Standard at any time.

One of our main goals with the product is to continue to work toward compliance with the SQL standard, but without sacrificing speed or reliability. We are not afraid to add extensions to SQL or support for non-SQL features if this greatly increases the usability of MySQL Server for a large segment of our user base. The HANDLER interface is an example of this strategy. See Section 13.2.4, "HANDLER Statement".

We continue to support transactional and nontransactional databases to satisfy both mission-critical 24/7 usage and heavy Web or logging usage.

MySQL Server was originally designed to work with medium-sized databases (10-100 million rows, or about 100MB per table) on small computer systems. Today MySQL Server handles terabytesized databases, but the code can also be compiled in a reduced version suitable for hand-held and embedded devices. The compact design of the MySQL server makes development in both directions possible without any conflicts in the source tree.

We are not targeting real-time support, although MySQL replication capabilities offer significant functionality.

MySQL supports ODBC levels 0 to 3.51.

MySQL supports high-availability database clustering using the NDBCLUSTER storage engine. See Chapter 21, MySQL NDB Cluster 7.5 and NDB Cluster 7.6.

We implement XML functionality which supports most of the W3C XPath standard. See Section 12.11, "XML Functions".

MySQL (5.7.8 and later) supports a native JSON data type as defined by RFC 7159, and based on the ECMAScript standard (ECMA-262). See Section 11.5, "The JSON Data Type". MySQL also implements a subset of the SQL/JSON functions specified by a pre-publication draft of the SQL:2016 standard; see Section 12.17, "JSON Functions", for more information.

## **Selecting SQL Modes**

The MySQL server can operate in different SQL modes, and can apply these modes differently for different clients, depending on the value of the sql\_mode system variable. DBAs can set the global SQL mode to match site server operating requirements, and each application can set its session SQL mode to its own requirements.

Modes affect the SQL syntax MySQL supports and the data validation checks it performs. This makes it easier to use MySQL in different environments and to use MySQL together with other database servers.

For more information on setting the SQL mode, see Section 5.1.10, "Server SQL Modes".

## **Running MySQL in ANSI Mode**

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

See Section 5.1.6, "Server Command Options".

## <span id="page-72-0"></span>**1.6.1 MySQL Extensions to Standard SQL**

MySQL Server supports some extensions that are likely not to be found in other SQL DBMSs. Be warned that if you use them, your code is not portable to other SQL servers. In some cases, you can write code that includes MySQL extensions, but is still portable, by using comments of the following form:

```
/*! MySQL-specific code */
```

In this case, MySQL Server parses and executes the code within the comment as it would any other SQL statement, but other SQL servers ignore the extensions. For example, MySQL Server recognizes the STRAIGHT\_JOIN keyword in the following statement, but other servers do not:

```
SELECT /*! STRAIGHT_JOIN */ col1 FROM table1,table2 WHERE ...
```

If you add a version number after the ! character, the syntax within the comment is executed only if the MySQL version is greater than or equal to the specified version number. The KEY\_BLOCK\_SIZE clause in the following comment is executed only by servers from MySQL 5.1.10 or higher:

```
CREATE TABLE t1(a INT, KEY (a)) /*!50110 KEY_BLOCK_SIZE=1024 */;
```

The following descriptions list MySQL extensions, organized by category.

• Organization of data on disk

MySQL Server maps each database to a directory under the MySQL data directory, and maps tables within a database to file names in the database directory. This has a few implications:

- Database and table names are case-sensitive in MySQL Server on operating systems that have case-sensitive file names (such as most Unix systems). See Section 9.2.3, "Identifier Case Sensitivity".
- You can use standard system commands to back up, rename, move, delete, and copy tables that are managed by the MyISAM storage engine. For example, it is possible to rename a MyISAM table by renaming the .MYD, .MYI, and .frm files to which the table corresponds. (Nevertheless, it is preferable to use RENAME TABLE or ALTER TABLE ... RENAME and let the server rename the files.)
- General language syntax
  - By default, strings can be enclosed by " as well as '. If the ANSI\_QUOTES SQL mode is enabled, strings can be enclosed only by ' and the server interprets strings enclosed by " as identifiers.
  - \ is the escape character in strings.
  - In SQL statements, you can access tables from different databases with the db\_name.tbl\_name syntax. Some SQL servers provide the same functionality but call this User space. MySQL Server does not support tablespaces such as used in statements like this: CREATE TABLE ralph.my\_table ... IN my\_tablespace.
- SQL statement syntax
  - The ANALYZE TABLE, CHECK TABLE, OPTIMIZE TABLE, and REPAIR TABLE statements.
  - The CREATE DATABASE, DROP DATABASE, and ALTER DATABASE statements. See Section 13.1.11, "CREATE DATABASE Statement", Section 13.1.22, "DROP DATABASE Statement", and Section 13.1.1, "ALTER DATABASE Statement".
  - The DO statement.
  - EXPLAIN SELECT to obtain a description of how tables are processed by the query optimizer.
  - The FLUSH and RESET statements.
  - The SET statement. See Section 13.7.4.1, "SET Syntax for Variable Assignment".
  - The SHOW statement. See Section 13.7.5, "SHOW Statements". The information produced by many of the MySQL-specific SHOW statements can be obtained in more standard fashion by using SELECT to query INFORMATION\_SCHEMA. See Chapter 24, INFORMATION\_SCHEMA Tables.
  - Use of LOAD DATA. In many cases, this syntax is compatible with Oracle LOAD DATA. See Section 13.2.6, "LOAD DATA Statement".
  - Use of RENAME TABLE. See Section 13.1.33, "RENAME TABLE Statement".
  - Use of REPLACE instead of DELETE plus INSERT. See Section 13.2.8, "REPLACE Statement".
  - Use of CHANGE col\_name, DROP col\_name, or DROP INDEX, IGNORE or RENAME in ALTER TABLE statements. Use of multiple ADD, ALTER, DROP, or CHANGE clauses in an ALTER TABLE statement. See Section 13.1.8, "ALTER TABLE Statement".
  - Use of index names, indexes on a prefix of a column, and use of INDEX or KEY in CREATE TABLE statements. See Section 13.1.18, "CREATE TABLE Statement".

- Use of TEMPORARY or IF NOT EXISTS with CREATE TABLE.
- Use of IF EXISTS with DROP TABLE and DROP DATABASE.
- The capability of dropping multiple tables with a single DROP TABLE statement.
- The ORDER BY and LIMIT clauses of the UPDATE and DELETE statements.
- INSERT INTO tbl\_name SET col\_name = ... syntax.
- The DELAYED clause of the INSERT and REPLACE statements.
- The LOW\_PRIORITY clause of the INSERT, REPLACE, DELETE, and UPDATE statements.
- Use of INTO OUTFILE or INTO DUMPFILE in SELECT statements. See Section 13.2.9, "SELECT Statement".
- Options such as STRAIGHT\_JOIN or SQL\_SMALL\_RESULT in SELECT statements.
- You don't need to name all selected columns in the GROUP BY clause. This gives better performance for some very specific, but quite normal queries. See Section 12.19, "Aggregate Functions".
- You can specify ASC and DESC with GROUP BY, not just with ORDER BY.
- The ability to set variables in a statement with the := assignment operator. See Section 9.4, "User-Defined Variables".
- Data types
  - The MEDIUMINT, SET, and ENUM data types, and the various BLOB and TEXT data types.
  - The AUTO\_INCREMENT, BINARY, NULL, UNSIGNED, and ZEROFILL data type attributes.
- Functions and operators
  - To make it easier for users who migrate from other SQL environments, MySQL Server supports aliases for many functions. For example, all string functions support both standard SQL syntax and ODBC syntax.
  - MySQL Server understands the || and && operators to mean logical OR and AND, as in the C programming language. In MySQL Server, || and OR are synonyms, as are && and AND. Because of this nice syntax, MySQL Server does not support the standard SQL || operator for string concatenation; use CONCAT() instead. Because CONCAT() takes any number of arguments, it is easy to convert use of the || operator to MySQL Server.
  - Use of COUNT(DISTINCT value\_list) where value\_list has more than one element.
  - String comparisons are case-insensitive by default, with sort ordering determined by the collation of the current character set, which is latin1 (cp1252 West European) by default. To perform case-sensitive comparisons instead, you should declare your columns with the BINARY attribute or use the BINARY cast, which causes comparisons to be done using the underlying character code values rather than a lexical ordering.
  - The % operator is a synonym for MOD(). That is, N % M is equivalent to MOD(N,M). % is supported for C programmers and for compatibility with PostgreSQL.
  - The =, <>, <=, <, >=, >, <<, >>, <=>, AND, OR, or LIKE operators may be used in expressions in the output column list (to the left of the FROM) in SELECT statements. For example:

mysql> **SELECT col1=1 AND col2=2 FROM my\_table;**

- The LAST\_INSERT\_ID() function returns the most recent AUTO\_INCREMENT value. See Section 12.15, "Information Functions".
- LIKE is permitted on numeric values.
- The REGEXP and NOT REGEXP extended regular expression operators.
- CONCAT() or CHAR() with one argument or more than two arguments. (In MySQL Server, these functions can take a variable number of arguments.)
- The BIT\_COUNT(), CASE, ELT(), FROM\_DAYS(), FORMAT(), IF(), PASSWORD(), ENCRYPT(), MD5(), ENCODE(), DECODE(), PERIOD\_ADD(), PERIOD\_DIFF(), TO\_DAYS(), and WEEKDAY() functions.
- Use of TRIM() to trim substrings. Standard SQL supports removal of single characters only.
- The GROUP BY functions STD(), BIT\_OR(), BIT\_AND(), BIT\_XOR(), and GROUP\_CONCAT(). See Section 12.19, "Aggregate Functions".

## <span id="page-75-0"></span>**1.6.2 MySQL Differences from Standard SQL**

We try to make MySQL Server follow the ANSI SQL standard and the ODBC SQL standard, but MySQL Server performs operations differently in some cases:

- There are several differences between the MySQL and standard SQL privilege systems. For example, in MySQL, privileges for a table are not automatically revoked when you delete a table. You must explicitly issue a REVOKE statement to revoke privileges for a table. For more information, see Section 13.7.1.6, "REVOKE Statement".
- The CAST() function does not support cast to REAL or BIGINT. See Section 12.10, "Cast Functions and Operators".

### **1.6.2.1 SELECT INTO TABLE Differences**

MySQL Server does not support the SELECT ... INTO TABLE Sybase SQL extension. Instead, MySQL Server supports the INSERT INTO ... SELECT standard SQL syntax, which is basically the same thing. See Section 13.2.5.1, "INSERT ... SELECT Statement". For example:

```
INSERT INTO tbl_temp2 (fld_id)
 SELECT tbl_temp1.fld_order_id
 FROM tbl_temp1 WHERE tbl_temp1.fld_order_id > 100;
```

Alternatively, you can use SELECT ... INTO OUTFILE or CREATE TABLE ... SELECT.

You can use SELECT ... INTO with user-defined variables. The same syntax can also be used inside stored routines using cursors and local variables. See Section 13.2.9.1, "SELECT ... INTO Statement".

### **1.6.2.2 UPDATE Differences**

If you access a column from the table to be updated in an expression, UPDATE uses the current value of the column. The second assignment in the following statement sets col2 to the current (updated) col1 value, not the original col1 value. The result is that col1 and col2 have the same value. This behavior differs from standard SQL.

```
UPDATE t1 SET col1 = col1 + 1, col2 = col1;
```

### **1.6.2.3 FOREIGN KEY Constraint Differences**

The MySQL implementation of foreign key constraints differs from the SQL standard in the following key respects:

- If there are several rows in the parent table with the same referenced key value, InnoDB performs a foreign key check as if the other parent rows with the same key value do not exist. For example, if you define a RESTRICT type constraint, and there is a child row with several parent rows, InnoDB does not permit the deletion of any of the parent rows.
- If ON UPDATE CASCADE or ON UPDATE SET NULL recurses to update the same table it has previously updated during the same cascade, it acts like RESTRICT. This means that you cannot use self-referential ON UPDATE CASCADE or ON UPDATE SET NULL operations. This is to prevent infinite loops resulting from cascaded updates. A self-referential ON DELETE SET NULL, on the other hand, is possible, as is a self-referential ON DELETE CASCADE. Cascading operations may not be nested more than 15 levels deep.
- In an SQL statement that inserts, deletes, or updates many rows, foreign key constraints (like unique constraints) are checked row-by-row. When performing foreign key checks, InnoDB sets shared rowlevel locks on child or parent records that it must examine. MySQL checks foreign key constraints immediately; the check is not deferred to transaction commit. According to the SQL standard, the default behavior should be deferred checking. That is, constraints are only checked after the entire SQL statement has been processed. This means that it is not possible to delete a row that refers to itself using a foreign key.
- No storage engine, including InnoDB, recognizes or enforces the MATCH clause used in referentialintegrity constraint definitions. Use of an explicit MATCH clause does not have the specified effect, and it causes ON DELETE and ON UPDATE clauses to be ignored. Specifying the MATCH should be avoided.

The MATCH clause in the SQL standard controls how NULL values in a composite (multiple-column) foreign key are handled when comparing to a primary key in the referenced table. MySQL essentially implements the semantics defined by MATCH SIMPLE, which permits a foreign key to be all or partially NULL. In that case, a (child table) row containing such a foreign key can be inserted even though it does not match any row in the referenced (parent) table. (It is possible to implement other semantics using triggers.)

• MySQL requires that the referenced columns be indexed for performance reasons. However, MySQL does not enforce a requirement that the referenced columns be UNIQUE or be declared NOT NULL.

A FOREIGN KEY constraint that references a non-UNIQUE key is not standard SQL but rather an InnoDB extension. The NDB storage engine, on the other hand, requires an explicit unique key (or primary key) on any column referenced as a foreign key.

The handling of foreign key references to nonunique keys or keys that contain NULL values is not well defined for operations such as UPDATE or DELETE CASCADE. You are advised to use foreign keys that reference only UNIQUE (including PRIMARY) and NOT NULL keys.

- For storage engines that do not support foreign keys (such as MyISAM), MySQL Server parses and ignores foreign key specifications.
- MySQL parses but ignores "inline REFERENCES specifications" (as defined in the SQL standard) where the references are defined as part of the column specification. MySQL accepts REFERENCES clauses only when specified as part of a separate FOREIGN KEY specification.

Defining a column to use a REFERENCES tbl\_name(col\_name) clause has no actual effect and serves only as a memo or comment to you that the column which you are currently defining is intended to refer to a column in another table. It is important to realize when using this syntax that:

- MySQL does not perform any sort of check to make sure that col\_name actually exists in tbl\_name (or even that tbl\_name itself exists).
- MySQL does not perform any sort of action on tbl\_name such as deleting rows in response to actions taken on rows in the table which you are defining; in other words, this syntax induces no ON DELETE or ON UPDATE behavior whatsoever. (Although you can write an ON DELETE or ON UPDATE clause as part of the REFERENCES clause, it is also ignored.)

• This syntax creates a column; it does **not** create any sort of index or key.

You can use a column so created as a join column, as shown here:

```
CREATE TABLE person (
 id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
 name CHAR(60) NOT NULL,
 PRIMARY KEY (id)
);
CREATE TABLE shirt (
 id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
 style ENUM('t-shirt', 'polo', 'dress') NOT NULL,
 color ENUM('red', 'blue', 'orange', 'white', 'black') NOT NULL,
 owner SMALLINT UNSIGNED NOT NULL REFERENCES person(id),
 PRIMARY KEY (id)
);
INSERT INTO person VALUES (NULL, 'Antonio Paz');
SELECT @last := LAST_INSERT_ID();
INSERT INTO shirt VALUES
(NULL, 'polo', 'blue', @last),
(NULL, 'dress', 'white', @last),
(NULL, 't-shirt', 'blue', @last);
INSERT INTO person VALUES (NULL, 'Lilliana Angelovska');
SELECT @last := LAST_INSERT_ID();
INSERT INTO shirt VALUES
(NULL, 'dress', 'orange', @last),
(NULL, 'polo', 'red', @last),
(NULL, 'dress', 'blue', @last),
(NULL, 't-shirt', 'white', @last);
SELECT * FROM person;
+----+---------------------+
| id | name |
+----+---------------------+
| 1 | Antonio Paz |
| 2 | Lilliana Angelovska |
+----+---------------------+
SELECT * FROM shirt;
+----+---------+--------+-------+
| id | style | color | owner |
+----+---------+--------+-------+
| 1 | polo | blue | 1 |
| 2 | dress | white | 1 |
| 3 | t-shirt | blue | 1 |
| 4 | dress | orange | 2 |
| 5 | polo | red | 2 |
| 6 | dress | blue | 2 |
| 7 | t-shirt | white | 2 |
+----+---------+--------+-------+
SELECT s.* FROM person p INNER JOIN shirt s
 ON s.owner = p.id
 WHERE p.name LIKE 'Lilliana%'
 AND s.color <> 'white';
+----+-------+--------+-------+
| id | style | color | owner |
+----+-------+--------+-------+
| 4 | dress | orange | 2 |
| 5 | polo | red | 2 |
| 6 | dress | blue | 2 |
```

+----+-------+--------+-------+

When used in this fashion, the REFERENCES clause is not displayed in the output of SHOW CREATE TABLE or DESCRIBE:

```
SHOW CREATE TABLE shirt\G
*************************** 1. row ***************************
Table: shirt
Create Table: CREATE TABLE `shirt` (
`id` smallint(5) unsigned NOT NULL auto_increment,
`style` enum('t-shirt','polo','dress') NOT NULL,
`color` enum('red','blue','orange','white','black') NOT NULL,
`owner` smallint(5) unsigned NOT NULL,
PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1
```

For information about foreign key constraints, see Section 13.1.18.5, "FOREIGN KEY Constraints".

## **1.6.2.4 '--' as the Start of a Comment**

Standard SQL uses the C syntax /\* this is a comment \*/ for comments, and MySQL Server supports this syntax as well. MySQL also support extensions to this syntax that enable MySQL-specific SQL to be embedded in the comment; see Section 9.6, "Comments".

MySQL Server also uses # as the start comment character. This is nonstandard.

Standard SQL also uses "--" as a start-comment sequence. MySQL Server supports a variant of the -- comment style; the -- start-comment sequence is accepted as such, but must be followed by a whitespace character such as a space or newline. The space is intended to prevent problems with generated SQL queries that use constructs such as the following, which updates the balance to reflect a charge:

```
UPDATE account SET balance=balance-charge
WHERE account_id=user_id
```

Consider what happens when charge has a negative value such as -1, which might be the case when an amount is credited to the account. In this case, the generated statement looks like this:

```
UPDATE account SET balance=balance--1
WHERE account_id=5752;
```

balance--1 is valid standard SQL, but -- is interpreted as the start of a comment, and part of the expression is discarded. The result is a statement that has a completely different meaning than intended:

```
UPDATE account SET balance=balance
WHERE account_id=5752;
```

This statement produces no change in value at all. To keep this from happening, MySQL requires a whitespace character following the -- for it to be recognized as a start-comment sequence in MySQL Server, so that an expression such as balance--1 is always safe to use.

## <span id="page-78-0"></span>**1.6.3 How MySQL Deals with Constraints**

MySQL enables you to work both with transactional tables that permit rollback and with nontransactional tables that do not. Because of this, constraint handling is a bit different in MySQL than in other DBMSs. We must handle the case when you have inserted or updated a lot of rows in a nontransactional table for which changes cannot be rolled back when an error occurs.

The basic philosophy is that MySQL Server tries to produce an error for anything that it can detect while parsing a statement to be executed, and tries to recover from any errors that occur while executing the statement. We do this in most cases, but not yet for all.

The options MySQL has when an error occurs are to stop the statement in the middle or to recover as well as possible from the problem and continue. By default, the server follows the latter course. This means, for example, that the server may coerce invalid values to the closest valid values.

Several SQL mode options are available to provide greater control over handling of bad data values and whether to continue statement execution or abort when errors occur. Using these options, you can configure MySQL Server to act in a more traditional fashion that is like other DBMSs that reject improper input. The SQL mode can be set globally at server startup to affect all clients. Individual clients can set the SQL mode at runtime, which enables each client to select the behavior most appropriate for its requirements. See Section 5.1.10, "Server SQL Modes".

The following sections describe how MySQL Server handles different types of constraints.

### **1.6.3.1 PRIMARY KEY and UNIQUE Index Constraints**

Normally, errors occur for data-change statements (such as INSERT or UPDATE) that would violate primary-key, unique-key, or foreign-key constraints. If you are using a transactional storage engine such as InnoDB, MySQL automatically rolls back the statement. If you are using a nontransactional storage engine, MySQL stops processing the statement at the row for which the error occurred and leaves any remaining rows unprocessed.

MySQL supports an IGNORE keyword for INSERT, UPDATE, and so forth. If you use it, MySQL ignores primary-key or unique-key violations and continues processing with the next row. See the section for the statement that you are using (Section 13.2.5, "INSERT Statement", Section 13.2.11, "UPDATE Statement", and so forth).

You can get information about the number of rows actually inserted or updated with the [mysql\\_info\(\)](https://dev.mysql.com/doc/c-api/5.7/en/mysql-info.md) C API function. You can also use the SHOW WARNINGS statement. See [mysql\\_info\(\),](https://dev.mysql.com/doc/c-api/5.7/en/mysql-info.md) and Section 13.7.5.40, "SHOW WARNINGS Statement".

InnoDB and NDB tables support foreign keys. See [Section 1.6.3.2, "FOREIGN KEY Constraints"](#page-79-0).

### <span id="page-79-0"></span>**1.6.3.2 FOREIGN KEY Constraints**

Foreign keys let you cross-reference related data across tables, and foreign key constraints help keep this spread-out data consistent.

MySQL supports ON UPDATE and ON DELETE foreign key references in CREATE TABLE and ALTER TABLE statements. The available referential actions are RESTRICT (the default), CASCADE, SET NULL, and NO ACTION.

SET DEFAULT is also supported by the MySQL Server but is currently rejected as invalid by InnoDB. Since MySQL does not support deferred constraint checking, NO ACTION is treated as RESTRICT. For the exact syntax supported by MySQL for foreign keys, see Section 13.1.18.5, "FOREIGN KEY Constraints".

MATCH FULL, MATCH PARTIAL, and MATCH SIMPLE are allowed, but their use should be avoided, as they cause the MySQL Server to ignore any ON DELETE or ON UPDATE clause used in the same statement. MATCH options do not have any other effect in MySQL, which in effect enforces MATCH SIMPLE semantics full-time.

MySQL requires that foreign key columns be indexed; if you create a table with a foreign key constraint but no index on a given column, an index is created.

You can obtain information about foreign keys from the Information Schema KEY\_COLUMN\_USAGE table. An example of a query against this table is shown here:

```
mysql> SELECT TABLE_SCHEMA, TABLE_NAME, COLUMN_NAME, CONSTRAINT_NAME
 > FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
 > WHERE REFERENCED_TABLE_SCHEMA IS NOT NULL;
```

| TABLE_SCHEMA   TABLE_NAME |                                                                                   |           | +++++<br>  COLUMN_NAME   CONSTRAINT_NAME |
|---------------------------|-----------------------------------------------------------------------------------|-----------|------------------------------------------|
| fk1<br>  fk1<br>  fk1     | myuser<br>  product_order   customer_id   f2<br>  product_order   product_id   f1 | myuser_id | +++++<br>  f<br> <br> <br>               |
| 3 rows in set (0.01 sec)  |                                                                                   |           | +++++                                    |

Information about foreign keys on InnoDB tables can also be found in the INNODB\_SYS\_FOREIGN and INNODB\_SYS\_FOREIGN\_COLS tables, in the INFORMATION\_SCHEMA database.

InnoDB and NDB tables support foreign keys.

### **1.6.3.3 Constraints on Invalid Data**

MySQL 5.7.5 and later uses strict SQL mode by default, which treats invalid values such that the server rejects them and aborts the statement in which they occur (see Section 5.1.10, "Server SQL Modes"). Previously, MySQL was much more forgiving of incorrect values used in data entry; this now requires disabling of strict mode, which is not recommended. The remainder of this section discusses the old behavior followed by MySQL when strict mode has been disabled.

If you are not using strict mode, then whenever you insert an "incorrect" value into a column, such as a NULL into a NOT NULL column or a too-large numeric value into a numeric column, MySQL sets the column to the "best possible value" instead of producing an error: The following rules describe in more detail how this works:

- If you try to store an out of range value into a numeric column, MySQL Server instead stores zero, the smallest possible value, or the largest possible value, whichever is closest to the invalid value.
- For strings, MySQL stores either the empty string or as much of the string as can be stored in the column.
- If you try to store a string that does not start with a number into a numeric column, MySQL Server stores 0.
- Invalid values for ENUM and SET columns are handled as described in [Section 1.6.3.4, "ENUM and](#page-81-0) [SET Constraints"](#page-81-0).
- MySQL permits you to store certain incorrect date values into DATE and DATETIME columns (such as '2000-02-31' or '2000-02-00'). In this case, when an application has not enabled strict SQL mode, it up to the application to validate the dates before storing them. If MySQL can store a date value and retrieve exactly the same value, MySQL stores it as given. If the date is totally wrong (outside the server's ability to store it), the special "zero" date value '0000-00-00' is stored in the column instead.
- If you try to store NULL into a column that does not take NULL values, an error occurs for singlerow INSERT statements. For multiple-row INSERT statements or for INSERT INTO ... SELECT statements, MySQL Server stores the implicit default value for the column data type. In general, this is 0 for numeric types, the empty string ('') for string types, and the "zero" value for date and time types. Implicit default values are discussed in Section 11.6, "Data Type Default Values".
- If an INSERT statement specifies no value for a column, MySQL inserts its default value if the column definition includes an explicit DEFAULT clause. If the definition has no such DEFAULT clause, MySQL inserts the implicit default value for the column data type.

The reason for using the preceding rules when strict mode is not in effect is that we cannot check these conditions until the statement has begun executing. We cannot just roll back if we encounter a problem after updating a few rows, because the storage engine may not support rollback. The option of terminating the statement is not that good; in this case, the update would be "half done," which is probably the worst possible scenario. In this case, it is better to "do the best you can" and then continue as if nothing happened.

You can select stricter treatment of input values by using the STRICT\_TRANS\_TABLES or STRICT\_ALL\_TABLES SQL modes:

```
SET sql_mode = 'STRICT_TRANS_TABLES';
SET sql_mode = 'STRICT_ALL_TABLES';
```

STRICT\_TRANS\_TABLES enables strict mode for transactional storage engines, and also to some extent for nontransactional engines. It works like this:

- For transactional storage engines, bad data values occurring anywhere in a statement cause the statement to abort and roll back.
- For nontransactional storage engines, a statement aborts if the error occurs in the first row to be inserted or updated. (When the error occurs in the first row, the statement can be aborted to leave the table unchanged, just as for a transactional table.) Errors in rows after the first do not abort the statement, because the table has already been changed by the first row. Instead, bad data values are adjusted and result in warnings rather than errors. In other words, with STRICT\_TRANS\_TABLES, a wrong value causes MySQL to roll back all updates done so far, if that can be done without changing the table. But once the table has been changed, further errors result in adjustments and warnings.

For even stricter checking, enable STRICT\_ALL\_TABLES. This is the same as STRICT\_TRANS\_TABLES except that for nontransactional storage engines, errors abort the statement even for bad data in rows following the first row. This means that if an error occurs partway through a multiple-row insert or update for a nontransactional table, a partial update results. Earlier rows are inserted or updated, but those from the point of the error on are not. To avoid this for nontransactional tables, either use single-row statements or else use STRICT\_TRANS\_TABLES if conversion warnings rather than errors are acceptable. To avoid problems in the first place, do not use MySQL to check column content. It is safest (and often faster) to let the application ensure that it passes only valid values to the database.

With either of the strict mode options, you can cause errors to be treated as warnings by using INSERT IGNORE or UPDATE IGNORE rather than INSERT or UPDATE without IGNORE.

### <span id="page-81-0"></span>**1.6.3.4 ENUM and SET Constraints**

ENUM and SET columns provide an efficient way to define columns that can contain only a given set of values. See Section 11.3.5, "The ENUM Type", and Section 11.3.6, "The SET Type".

Unless strict mode is disabled (not recommended, but see Section 5.1.10, "Server SQL Modes"), the definition of a ENUM or SET column acts as a constraint on values entered into the column. An error occurs for values that do not satisfy these conditions:

- An ENUM value must be one of those listed in the column definition, or the internal numeric equivalent thereof. The value cannot be the error value (that is, 0 or the empty string). For a column defined as ENUM('a','b','c'), values such as '', 'd', or 'ax' are invalid and are rejected.
- A SET value must be the empty string or a value consisting only of the values listed in the column definition separated by commas. For a column defined as SET('a','b','c'), values such as 'd' or 'a,b,c,d' are invalid and are rejected.

Errors for invalid values can be suppressed in strict mode if you use INSERT IGNORE or UPDATE IGNORE. In this case, a warning is generated rather than an error. For ENUM, the value is inserted as the error member (0). For SET, the value is inserted as given except that any invalid substrings are deleted. For example, 'a,x,b,y' results in a value of 'a,b'.

## <span id="page-82-0"></span>Chapter 2 Installing and Upgrading MySQL

## **Table of Contents**

| 2.1 General Installation Guidance 57                                                   |     |
|----------------------------------------------------------------------------------------|-----|
| 2.1.1 Supported Platforms 58                                                           |     |
| 2.1.2 Which MySQL Version and Distribution to Install 58                               |     |
| 2.1.3 How to Get MySQL 59                                                              |     |
| 2.1.4 Verifying Package Integrity Using MD5 Checksums or GnuPG 59                      |     |
| 2.1.5 Installation Layouts 75                                                          |     |
| 2.1.6 Compiler-Specific Build Characteristics 75                                       |     |
| 2.2 Installing MySQL on Unix/Linux Using Generic Binaries 76                           |     |
| 2.3 Installing MySQL on Microsoft Windows 79                                           |     |
| 2.3.1 MySQL Installation Layout on Microsoft Windows 81                                |     |
| 2.3.2 Choosing an Installation Package 82                                              |     |
| 2.3.3 MySQL Installer for Windows 83                                                   |     |
| 2.3.4 Installing MySQL on Microsoft Windows Using a noinstall ZIP Archive 112          |     |
| 2.3.5 Troubleshooting a Microsoft Windows MySQL Server Installation 121                |     |
| 2.3.6 Windows Postinstallation Procedures                                              | 122 |
| 2.3.7 Windows Platform Restrictions 124                                                |     |
| 2.4 Installing MySQL on macOS 125                                                      |     |
| 2.4.1 General Notes on Installing MySQL on macOS 126                                   |     |
| 2.4.2 Installing MySQL on macOS Using Native Packages 127                              |     |
| 2.4.3 Installing a MySQL Launch Daemon 132                                             |     |
| 2.4.4 Installing and Using the MySQL Preference Pane 135                               |     |
| 2.5 Installing MySQL on Linux 139                                                      |     |
| 2.5.1 Installing MySQL on Linux Using the MySQL Yum Repository 140                     |     |
| 2.5.2 Replacing a Third-Party Distribution of MySQL Using the MySQL Yum Repository 144 |     |
| 2.5.3 Installing MySQL on Linux Using the MySQL APT Repository 146                     |     |
| 2.5.4 Installing MySQL on Linux Using the MySQL SLES Repository 146                    |     |
| 2.5.5 Installing MySQL on Linux Using RPM Packages from Oracle 146                     |     |
| 2.5.6 Installing MySQL on Linux Using Debian Packages from Oracle                      | 151 |
| 2.5.7 Deploying MySQL on Linux with Docker 153                                         |     |
| 2.5.8 Installing MySQL on Linux from the Native Software Repositories 162              |     |
| 2.5.9 Installing MySQL on Linux with Juju 165                                          |     |
| 2.5.10 Managing MySQL Server with systemd 165                                          |     |
| 2.6 Installing MySQL Using Unbreakable Linux Network (ULN) 170                         |     |
| 2.7 Installing MySQL on Solaris 171                                                    |     |
| 2.7.1 Installing MySQL on Solaris Using a Solaris PKG 172                              |     |
| 2.8 Installing MySQL from Source 173                                                   |     |
| 2.8.1 Source Installation Methods 173                                                  |     |
| 2.8.2 Source Installation Prerequisites 173                                            |     |
| 2.8.3 MySQL Layout for Source Installation 175                                         |     |
| 2.8.4 Installing MySQL Using a Standard Source Distribution 175                        |     |
| 2.8.5 Installing MySQL Using a Development Source Tree 179                             |     |
| 2.8.6 Configuring SSL Library Support 181                                              |     |
| 2.8.7 MySQL Source-Configuration Options 182                                           |     |
| 2.8.8 Dealing with Problems Compiling MySQL 203                                        |     |
|                                                                                        |     |
| 2.8.9 MySQL Configuration and Third-Party Tools 204                                    |     |
| 2.9 Postinstallation Setup and Testing 205                                             |     |
| 2.9.1 Initializing the Data Directory                                                  | 205 |
| 2.9.2 Starting the Server 211                                                          |     |
| 2.9.3 Testing the Server 214                                                           |     |
| 2.9.4 Securing the Initial MySQL Account 215                                           |     |
| 2.9.5 Starting and Stopping MySQL Automatically 217                                    |     |
| 2.10 Upgrading MySQL 218                                                               |     |

| 2.10.1 Before You Begin 218                                                    |     |
|--------------------------------------------------------------------------------|-----|
| 2.10.2 Upgrade Paths 219                                                       |     |
| 2.10.3 Changes in MySQL 5.7                                                    | 220 |
| 2.10.4 Upgrading MySQL Binary or Package-based Installations on Unix/Linux 229 |     |
| 2.10.5 Upgrading MySQL with the MySQL Yum Repository 232                       |     |
| 2.10.6 Upgrading MySQL with the MySQL APT Repository 233                       |     |
| 2.10.7 Upgrading MySQL with the MySQL SLES Repository 233                      |     |
| 2.10.8 Upgrading MySQL on Windows 234                                          |     |
| 2.10.9 Upgrading a Docker Installation of MySQL 235                            |     |
| 2.10.10 Upgrading MySQL with Directly-Downloaded RPM Packages 235              |     |
| 2.10.11 Upgrade Troubleshooting 237                                            |     |
| 2.10.12 Rebuilding or Repairing Tables or Indexes 237                          |     |
| 2.10.13 Copying MySQL Databases to Another Machine 238                         |     |
| 2.11 Downgrading MySQL 239                                                     |     |
| 2.11.1 Before You Begin 240                                                    |     |
| 2.11.2 Downgrade Paths 240                                                     |     |
| 2.11.3 Downgrade Notes 240                                                     |     |
| 2.11.4 Downgrading Binary and Package-based Installations on Unix/Linux 243    |     |
| 2.11.5 Downgrade Troubleshooting 245                                           |     |
| 2.12 Perl Installation Notes 246                                               |     |
| 2.12.1 Installing Perl on Unix 246                                             |     |
| 2.12.2 Installing ActiveState Perl on Windows 247                              |     |
| 2.12.3 Problems Using the Perl DBI/DBD Interface 247                           |     |

This chapter describes how to obtain and install MySQL. A summary of the procedure follows and later sections provide the details. If you plan to upgrade an existing version of MySQL to a newer version rather than install MySQL for the first time, see Section 2.10, "Upgrading MySQL", for information about upgrade procedures and about issues that you should consider before upgrading.

If you are interested in migrating to MySQL from another database system, see Section A.8, "MySQL 5.7 FAQ: Migration", which contains answers to some common questions concerning migration issues.

Installation of MySQL generally follows the steps outlined here:

#### 1. **Determine whether MySQL runs and is supported on your platform.**

Please note that not all platforms are equally suitable for running MySQL, and that not all platforms on which MySQL is known to run are officially supported by Oracle Corporation. For information about those platforms that are officially supported, see [https://www.mysql.com/support/](https://www.mysql.com/support/supportedplatforms/database.md) [supportedplatforms/database.html](https://www.mysql.com/support/supportedplatforms/database.md) on the MySQL website.

### 2. **Choose which distribution to install.**

Several versions of MySQL are available, and most are available in several distribution formats. You can choose from pre-packaged distributions containing binary (precompiled) programs or source code. When in doubt, use a binary distribution. Oracle also provides access to the MySQL source code for those who want to see recent developments and test new code. To determine which version and type of distribution you should use, see [Section 2.1.2, "Which MySQL Version](#page-85-1) [and Distribution to Install".](#page-85-1)

#### 3. **Download the distribution that you want to install.**

For instructions, see [Section 2.1.3, "How to Get MySQL".](#page-86-0) To verify the integrity of the distribution, use the instructions in [Section 2.1.4, "Verifying Package Integrity Using MD5 Checksums or](#page-86-1) [GnuPG".](#page-86-1)

### 4. **Install the distribution.**

To install MySQL from a binary distribution, use the instructions in [Section 2.2, "Installing MySQL](#page-103-0) [on Unix/Linux Using Generic Binaries".](#page-103-0) Alternatively, use the [Secure Deployment Guide](https://dev.mysql.com/doc/mysql-secure-deployment-guide/5.7/en/), which

provides procedures for deploying a generic binary distribution of MySQL Enterprise Edition Server with features for managing the security of your MySQL installation.

To install MySQL from a source distribution or from the current development source tree, use the instructions in Section 2.8, "Installing MySQL from Source".

#### 5. **Perform any necessary postinstallation setup.**

After installing MySQL, see Section 2.9, "Postinstallation Setup and Testing" for information about making sure the MySQL server is working properly. Also refer to the information provided in Section 2.9.4, "Securing the Initial MySQL Account". This section describes how to secure the initial MySQL root user account, which has no password until you assign one. The section applies whether you install MySQL using a binary or source distribution.

6. If you want to run the MySQL benchmark scripts, Perl support for MySQL must be available. See Section 2.12, "Perl Installation Notes".

Instructions for installing MySQL on different platforms and environments is available on a platform by platform basis:

#### • **Unix, Linux**

For instructions on installing MySQL on most Linux and Unix platforms using a generic binary (for example, a .tar.gz package), see [Section 2.2, "Installing MySQL on Unix/Linux Using Generic](#page-103-0) [Binaries"](#page-103-0).

For information on building MySQL entirely from the source code distributions or the source code repositories, see Section 2.8, "Installing MySQL from Source"

For specific platform help on installation, configuration, and building from source see the corresponding platform section:

- Linux, including notes on distribution specific methods, see [Section 2.5, "Installing MySQL on](#page-166-0) [Linux"](#page-166-0).
- Solaris, including PKG and IPS formats, see [Section 2.7, "Installing MySQL on Solaris"](#page-198-0).
- IBM AIX, see [Section 2.7, "Installing MySQL on Solaris"](#page-198-0).

#### • **Microsoft Windows**

For instructions on installing MySQL on Microsoft Windows, using either the MySQL Installer or Zipped binary, see [Section 2.3, "Installing MySQL on Microsoft Windows"](#page-106-0).

For details and instructions on building MySQL from source code using Microsoft Visual Studio, see Section 2.8, "Installing MySQL from Source".

#### • **macOS**

For installation on macOS, including using both the binary package and native PKG formats, see [Section 2.4, "Installing MySQL on macOS".](#page-152-0)

For information on making use of an macOS Launch Daemon to automatically start and stop MySQL, see [Section 2.4.3, "Installing a MySQL Launch Daemon".](#page-159-0)

For information on the MySQL Preference Pane, see [Section 2.4.4, "Installing and Using the MySQL](#page-162-0) [Preference Pane"](#page-162-0).

## <span id="page-84-0"></span>**2.1 General Installation Guidance**

The immediately following sections contain the information necessary to choose, download, and verify your distribution. The instructions in later sections of the chapter describe how to install the distribution that you choose. For binary distributions, see the instructions at [Section 2.2, "Installing MySQL on](#page-103-0) [Unix/Linux Using Generic Binaries"](#page-103-0) or the corresponding section for your platform if available. To build MySQL from source, use the instructions in Section 2.8, "Installing MySQL from Source".

## <span id="page-85-0"></span>**2.1.1 Supported Platforms**

MySQL platform support evolves over time; please refer to [https://www.mysql.com/support/](https://www.mysql.com/support/supportedplatforms/database.md) [supportedplatforms/database.html](https://www.mysql.com/support/supportedplatforms/database.md) for the latest updates.

## <span id="page-85-1"></span>**2.1.2 Which MySQL Version and Distribution to Install**

When preparing to install MySQL, decide which version and distribution format (binary or source) to use.

First, decide whether to install a development release or a General Availability (GA) release. Development releases have the newest features, but are not recommended for production use. GA releases, also called production or stable releases, are meant for production use. We recommend using the most recent GA release.

The naming scheme in MySQL 5.7 uses release names that consist of three numbers and an optional suffix; for example, **mysql-5.7.1-m1**. The numbers within the release name are interpreted as follows:

- The first number (**5**) is the major version number.
- The second number (**7**) is the minor version number. Taken together, the major and minor numbers constitute the release series number. The series number describes the stable feature set.
- The third number (**1**) is the version number within the release series. This is incremented for each new bugfix release. In most cases, the most recent version within a series is the best choice.

Release names can also include a suffix to indicate the stability level of the release. Releases within a series progress through a set of suffixes to indicate how the stability level improves. The possible suffixes are:

- **mN** (for example, **m1**, **m2**, **m3**, ...) indicates a milestone number. MySQL development uses a milestone model, in which each milestone introduces a small subset of thoroughly tested features. From one milestone to the next, feature interfaces may change or features may even be removed, based on feedback provided by community members who try these early releases. Features within milestone releases may be considered to be of pre-production quality.
- **rc** indicates a Release Candidate (RC). Release candidates are believed to be stable, having passed all of MySQL's internal testing. New features may still be introduced in RC releases, but the focus shifts to fixing bugs to stabilize features introduced earlier within the series.
- Absence of a suffix indicates a General Availability (GA) or Production release. GA releases are stable, having successfully passed through the earlier release stages, and are believed to be reliable, free of serious bugs, and suitable for use in production systems.

Development within a series begins with milestone releases, followed by RC releases, and finally reaches GA status releases.

After choosing which MySQL version to install, decide which distribution format to install for your operating system. For most use cases, a binary distribution is the right choice. Binary distributions are available in native format for many platforms, such as RPM packages for Linux or DMG packages for macOS. Distributions are also available in more generic formats such as Zip archives or compressed tar files. On Windows, you can use [the MySQL Installer](#page-110-0) to install a binary distribution.

Under some circumstances, it may be preferable to install MySQL from a source distribution:

• You want to install MySQL at some explicit location. The standard binary distributions are ready to run at any installation location, but you might require even more flexibility to place MySQL components where you want.

- You want to configure mysqld with features that might not be included in the standard binary distributions. Here is a list of the most common extra options used to ensure feature availability:
  - -DWITH\_LIBWRAP=1 for TCP wrappers support.
  - -DWITH\_ZLIB={system|bundled} for features that depend on compression
  - -DWITH\_DEBUG=1 for debugging support

For additional information, see Section 2.8.7, "MySQL Source-Configuration Options".

- You want to configure mysqld without some features that are included in the standard binary distributions. For example, distributions normally are compiled with support for all character sets. If you want a smaller MySQL server, you can recompile it with support for only the character sets you need.
- You want to read or modify the C and C++ code that makes up MySQL. For this purpose, obtain a source distribution.
- Source distributions contain more tests and examples than binary distributions.

## <span id="page-86-0"></span>**2.1.3 How to Get MySQL**

Check our downloads page at<https://dev.mysql.com/downloads/> for information about the current version of MySQL and for downloading instructions.

For RPM-based Linux platforms that use Yum as their package management system, MySQL can be installed using the [MySQL Yum Repository](https://dev.mysql.com/downloads/repo/yum/). See [Section 2.5.1, "Installing MySQL on Linux Using the](#page-167-0) [MySQL Yum Repository"](#page-167-0) for details.

For Debian-based Linux platforms, MySQL can be installed using the [MySQL APT Repository](https://dev.mysql.com/downloads/repo/apt/). See [Section 2.5.3, "Installing MySQL on Linux Using the MySQL APT Repository"](#page-173-0) for details.

For SUSE Linux Enterprise Server (SLES) platforms, MySQL can be installed using the [MySQL SLES](https://dev.mysql.com/downloads/repo/suse/) [Repository.](https://dev.mysql.com/downloads/repo/suse/) See [Section 2.5.4, "Installing MySQL on Linux Using the MySQL SLES Repository"](#page-173-1) for details.

To obtain the latest development source, see Section 2.8.5, "Installing MySQL Using a Development Source Tree".

## <span id="page-86-1"></span>**2.1.4 Verifying Package Integrity Using MD5 Checksums or GnuPG**

After downloading the MySQL package that suits your needs and before attempting to install it, make sure that it is intact and has not been tampered with. There are three means of integrity checking:

- MD5 checksums
- Cryptographic signatures using GnuPG, the GNU Privacy Guard
- For RPM packages, the built-in RPM integrity verification mechanism

The following sections describe how to use these methods.

If you notice that the MD5 checksum or GPG signatures do not match, first try to download the respective package one more time, perhaps from another mirror site.

### <span id="page-86-2"></span>**2.1.4.1 Verifying the MD5 Checksum**

After you have downloaded a MySQL package, you should make sure that its MD5 checksum matches the one provided on the MySQL download pages. Each package has an individual checksum that

you can verify against the package that you downloaded. The correct MD5 checksum is listed on the downloads page for each MySQL product; compare it against the MD5 checksum of the file (product) that you download.

Each operating system and setup offers its own version of tools for checking the MD5 checksum. Typically the command is named md5sum, or it may be named md5, and some operating systems do not ship it at all. On Linux, it is part of the **GNU Text Utilities** package, which is available for a wide range of platforms. You can also download the source code from<http://www.gnu.org/software/textutils/>. If you have OpenSSL installed, you can use the command openssl md5 package\_name instead. A Windows implementation of the md5 command line utility is available from [http://www.fourmilab.ch/](http://www.fourmilab.ch/md5/) [md5/](http://www.fourmilab.ch/md5/). winMd5Sum is a graphical MD5 checking tool that can be obtained from [http://www.nullriver.com/](http://www.nullriver.com/index/products/winmd5sum) [index/products/winmd5sum](http://www.nullriver.com/index/products/winmd5sum). Our Microsoft Windows examples assume the name md5.exe.

Linux and Microsoft Windows examples:

```
$> md5sum mysql-standard-5.7.44-linux-i686.tar.gz
aaab65abbec64d5e907dcd41b8699945 mysql-standard-5.7.44-linux-i686.tar.gz
$> md5.exe mysql-installer-community-5.7.44.msi
```

You should verify that the resulting checksum (the string of hexadecimal digits) matches the one displayed on the download page immediately below the respective package.

aaab65abbec64d5e907dcd41b8699945 mysql-installer-community-5.7.44.msi

![](_page_87_Picture_6.jpeg)

### **Note**

Make sure to verify the checksum of the archive file (for example, the .zip, .tar.gz, or .msi file) and not of the files that are contained inside of the archive. In other words, verify the file before extracting its contents.

## <span id="page-87-0"></span>**2.1.4.2 Signature Checking Using GnuPG**

Another method of verifying the integrity and authenticity of a package is to use cryptographic signatures. This is more reliable than using [MD5 checksums,](#page-86-2) but requires more work.

We sign MySQL downloadable packages with GnuPG (GNU Privacy Guard). GnuPG is an Open Source alternative to the well-known Pretty Good Privacy (PGP) by Phil Zimmermann. Most Linux distributions ship with GnuPG installed by default. Otherwise, see<http://www.gnupg.org/>for more information about GnuPG and how to obtain and install it.

To verify the signature for a specific package, you first need to obtain a copy of our public GPG build key, which you can download from [http://pgp.mit.edu/.](http://pgp.mit.edu/) The key that you want to obtain is named mysql-build@oss.oracle.com. The keyID for MySQL 5.7.37 packages and higher is 3A79BD29. After obtaining this key, you should compare it with the key shown following, before using it verify MySQL packages. Alternatively, you can copy and paste the key directly from the text below.

![](_page_87_Picture_13.jpeg)

### **Note**

The following public GPG build key is for MySQL 5.7.37 packages and higher. For the public GPG build key for earlier MySQL release packages (keyID 5072E1F5), see [Section 2.1.4.5, "GPG Public Build Key for Archived](#page-94-0) [Packages"](#page-94-0).

```
-----BEGIN PGP PUBLIC KEY BLOCK-----
Version: SKS 1.1.6
Comment: Hostname: pgp.mit.edu
mQINBGG4urcBEACrbsRa7tSSyxSfFkB+KXSbNM9rxYqoB78u107skReefq4/+Y72TpDvlDZL
mdv/lK0IpLa3bnvsM9IE1trNLrfi+JES62kaQ6hePPgn2RqxyIirt2seSi3Z3n3jlEg+mSdh
AvW+b+hFnqxo+TY0U+RBwDi4oO0YzHefkYPSmNPdlxRPQBMv4GPTNfxERx6XvVSPcL1+jQ4R
2cQFBryNhidBFIkoCOszjWhm+WnbURsLheBp757lqEyrpCufz77zlq2gEi+wtPHItfqsx3rz
```

```
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
{\tt rWE31QS0bR15Az10/fg7ia65vQGMOC0TLpgChTbcZHtozeFqva4IeEgE4xN+6r8WtgSYeGGD}
RmeMEVjPM9dzQObf+SvGd58u2z9f2aqPK1H32c69RLoA0mHRe7Wkv4izeJUc5tumUY0e80jd
enZZjT3hjLh6tM+mrp2oWnQIoed4LxUwldhMOj0rYXv6laLGJ1FsW5eSke7ohBLcfBBTKnMC
BohROHy2E63Wggfsdn3UYzfqZ8cfbXetkXuLS/OM3MXbiNjg+E1YzjgWrkayu7yLakZx+mx6
sHPIJYm2hzkniMG29d5mG17ZT9emP9b+CfgGUxoXJkjs0gnD144bwGJ0dmIBu3ajVAaHODXy
Y/zdDMGjskfEYbNXCAY2FRZSE58tgTvPKD++Kd2KGplMU2EIFT7JYfKhHAB5DGMkx92HUMid
sTSKHe+OnnnoFmu4anmDU31i
=Xabo
   --END PGP PUBLIC KEY BLOCK----
```

To import the build key into your personal public GPG keyring, use <code>gpg --import</code>. For example, if you have saved the key in a file named <code>mysql\_pubkey.asc</code>, the import command looks like this:

```
$> gpg --import mysql_pubkey.asc
gpg: key 3A79BD29: public key "MySQL Release Engineering
<mysql-build@oss.oracle.com>" imported
gpg: Total number processed: 1
gpg:
```

You can also download the key from the public keyserver using the public key id, 3A79BD29:

```
$> gpg --recv-keys 3A79BD29
gpg: requesting key 3A79BD29 from hkp server keys.gnupg.net
gpg: key 3A79BD29: "MySQL Release Engineering <mysql-build@oss.oracle.com>"
1 new user ID
gpg: key 3A79BD29: "MySQL Release Engineering <mysql-build@oss.oracle.com>"
53 new signatures
gpg: no ultimately trusted keys found
gpg: Total number processed: 1
gpg: new user IDs: 1
gpg: new signatures: 53
```

If you want to import the key into your RPM configuration to validate RPM install packages, you should be able to import the key directly:

```
$> rpm --import mysql_pubkey.asc
```

If you experience problems or require RPM specific information, see [Section 2.1.4.4, "Signature](#page-93-0) [Checking Using RPM"](#page-93-0).

After you have downloaded and imported the public build key, download your desired MySQL package and the corresponding signature, which also is available from the download page. The signature file has the same name as the distribution file with an .asc extension, as shown by the examples in the following table.

**Table 2.1 MySQL Package and Signature Files for Source files**

| File Type         | File Name                                      |
|-------------------|------------------------------------------------|
| Distribution file | mysql-standard-5.7.44-linux<br>i686.tar.gz     |
| Signature file    | mysql-standard-5.7.44-linux<br>i686.tar.gz.asc |

Make sure that both files are stored in the same directory and then run the following command to verify the signature for the distribution file:

```
$> gpg --verify package_name.asc
```

If the downloaded package is valid, you should see a Good signature message similar to this one:

```
$> gpg --verify mysql-standard-5.7.44-linux-i686.tar.gz.asc
gpg: Signature made Tue 01 Feb 2011 02:38:30 AM CST using DSA key ID 3A79BD29
gpg: Good signature from "MySQL Release Engineering <mysql-build@oss.oracle.com>"
```

The Good signature message indicates that the file signature is valid, when compared to the signature listed on our site. But you might also see warnings, like so:

```
$> gpg --verify mysql-standard-5.7.44-linux-i686.tar.gz.asc
gpg: Signature made Wed 23 Jan 2013 02:25:45 AM PST using DSA key ID 3A79BD29
gpg: checking the trustdb
gpg: no ultimately trusted keys found
gpg: Good signature from "MySQL Release Engineering <mysql-build@oss.oracle.com>"
gpg: WARNING: This key is not certified with a trusted signature!
gpg: There is no indication that the signature belongs to the owner.
Primary key fingerprint: A4A9 4068 76FC BD3C 4567 70C8 8C71 8D3B 5072 E1F5
```

That is normal, as they depend on your setup and configuration. Here are explanations for these warnings:

- gpg: no ultimately trusted keys found: This means that the specific key is not "ultimately trusted" by you or your web of trust, which is okay for the purposes of verifying file signatures.
- WARNING: This key is not certified with a trusted signature! There is no indication that the signature belongs to the owner.: This refers to your level of trust in your belief that you possess our real public key. This is a personal decision. Ideally, a MySQL developer would hand you the key in person, but more commonly, you downloaded it. Was the download tampered with? Probably not, but this decision is up to you. Setting up a web of trust is one method for trusting them.

See the GPG documentation for more information on how to work with public keys.

### **2.1.4.3 Signature Checking Using Gpg4win for Windows**

The [Section 2.1.4.2, "Signature Checking Using GnuPG"](#page-87-0) section describes how to verify MySQL downloads using GPG. That guide also applies to Microsoft Windows, but another option is to use a GUI tool like [Gpg4win.](http://www.gpg4win.org/) You may use a different tool but our examples are based on Gpg4win, and utilize its bundled Kleopatra GUI.

Download and install Gpg4win, and then load Kleopatra. The dialog should look similar to:

**Figure 2.1 Kleopatra: Initial Screen**

![](_page_90_Figure_2.jpeg)

Next, add the MySQL Release Engineering certificate. Do this by clicking **File**, **Lookup Certificates on Server**. Type "Mysql Release Engineering" into the search box and press **Search**.

**Figure 2.2 Kleopatra: Lookup Certificates on Server Wizard: Finding a Certificate**

![](_page_90_Figure_5.jpeg)

Select the "MySQL Release Engineering" certificate. The Fingerprint and Key-ID must be "3A79BD29" for MySQL 5.7.37 and higher or "5072E1F5" for MySQL 5.7.36 and earlier, or choose **Details...** to confirm the certificate is valid. Now, import it by clicking **Import**. An import dialog is displayed; choose **Okay**, and this certificate should now be listed under the **Imported Certificates** tab.

Next, configure the trust level for our certificate. Select our certificate, then from the main menu select **Certificates**, **Change Owner Trust...**. We suggest choosing **I believe checks are very accurate** for our certificate, as otherwise you might not be able to verify our signature. Select **I believe checks are very accurate** to enable "full trust" and then press **OK**.

**Figure 2.3 Kleopatra: Change Trust level for MySQL Release Engineering**

![](_page_91_Figure_2.jpeg)

Next, verify the downloaded MySQL package file. This requires files for both the packaged file, and the signature. The signature file must have the same name as the packaged file but with an appended .asc extension, as shown by the example in the following table. The signature is linked to on the downloads page for each MySQL product. You must create the .asc file with this signature.

**Table 2.2 MySQL Package and Signature Files for MySQL Installer for Microsoft Windows**

| File Type         | File Name                            |
|-------------------|--------------------------------------|
| Distribution file | mysql-installer-community-5.7.44.msi |
| Signature file    | mysql-installer                      |
|                   | community-5.7.44.msi.asc             |

Make sure that both files are stored in the same directory and then run the following command to verify the signature for the distribution file. Either drag and drop the signature (.asc) file into Kleopatra, or load the dialog from **File**, **Decrypt/Verify Files...**, and then choose either the .msi or .asc file.

**Figure 2.4 Kleopatra: The Decrypt and Verify Files Dialog**

![](_page_92_Picture_2.jpeg)

Click **Decrypt/Verify** to check the file. The two most common results look like the following, and although the yellow warning looks problematic, the following means that the file check passed with success. You may now run this installer.

**Figure 2.5 Kleopatra: the Decrypt and Verify Results Dialog: All operations completed**

![](_page_92_Picture_5.jpeg)

Seeing a red "The signature is bad" error means the file is invalid. Do not execute the MSI file if you see this error.

**Figure 2.6 Kleopatra: the Decrypt and Verify Results Dialog: Bad**

![](_page_93_Picture_2.jpeg)

The [Section 2.1.4.2, "Signature Checking Using GnuPG"](#page-87-0) section explains why you probably don't see a green Good signature result.

## <span id="page-93-0"></span>**2.1.4.4 Signature Checking Using RPM**

For RPM packages, there is no separate signature. RPM packages have a built-in GPG signature and MD5 checksum. You can verify a package by running the following command:

```
$> rpm --checksig package_name.rpm
```

#### Example:

```
$> rpm --checksig mysql-community-server-5.7.44-1.el8.x86_64.rpm
MySQL-server-5.7.44-1.el8.x86_64.rpm: digests signatures OK
```

![](_page_93_Picture_9.jpeg)

#### **Note**

If you are using RPM 4.1 and it complains about (GPG) NOT OK (MISSING KEYS: GPG#3a79bd29), even though you have imported the MySQL public build key into your own GPG keyring, you need to import the key into the RPM keyring first. RPM 4.1 no longer uses your personal GPG keyring (or GPG itself). Rather, RPM maintains a separate keyring because it is a system-wide application and a user's GPG public keyring is a user-specific file. To import the MySQL public key into the RPM keyring, first obtain the key, then use rpm - import to import the key. For example:

```
$> gpg --export -a 3a79bd29 > 3a79bd29.asc
$> rpm --import 3a79bd29.asc
```

Alternatively, rpm also supports loading the key directly from a URL:

```
$> rpm --import https://repo.mysql.com/RPM-GPG-KEY-mysql-2022
```

You can also obtain the MySQL public key from this manual page: [Section 2.1.4.2, "Signature](#page-87-0) [Checking Using GnuPG"](#page-87-0).

## <span id="page-94-0"></span>**2.1.4.5 GPG Public Build Key for Archived Packages**

The following GPG public build key (keyID 5072E1F5) can be used to verify the authenticity and integrity of MySQL 5.7.36 packages and earlier. For signature checking instructions, see [Section 2.1.4.2, "Signature Checking Using GnuPG".](#page-87-0)

### **GPG Public Build Key for MySQL 5.7.36 Packages and Earlier**

-----BEGIN PGP PUBLIC KEY BLOCK----- Version: SKS 1.1.6 Comment: Hostname: pgp.mit.edu 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  ${\tt SYwlg0r9+191FwKFvfk0jX1ZGk6GP27zTw49yopW9kFw/AUZXlwQHOYAL3gnslwPz5LwiTyJ} \\$ QkxAYYvdByZk4GjOi+HzqGPspNIQEeUteXzfbPz0fWEt64tudeqYu/fN5QVLGS/WHfkuFkuo qwNBFcu5TPEYcwGkuE/IZZEniOEiBBABAqAMBOJPBAkXBOMAEnUAAAoJEJcOuJvKV618AG8H /0LLr1yM6osbLAhOzcKmD//jSOZ2FIBXGKUmK8/onlu5sUcMmVVPHnjUO/mHiFMbYFC655Di rVUKlIZb6sdx2E/K+ZkZHPWvF1BAaHUO/OGh3Zzc8lVJg9KtFLAJkmOkc61VEF2MriaRlvlo VPNr50iv2TH0PgVxdV3goBL6EdAdgdwCvy23Z44v0p0QVNQt4aJKg2f49X0/N1+Gd2mEr7wX aN9DZQq5zTU7uTRif3FlXHQ4bp8TWBK3Mu/sLlqZYtF3z7GH4w3QbwyA2CWkGgTGwQwyU8Fh JQdrqXGl0w0y6JusjJWdwT1fxA6Eia3wrSw2f8Rlu6V0k0ZhsMu3s7iJASIEEAECAAwFAk8V 1NwFAwASdQAACgkQ1xC4m8pXrXzijAf7Bn+4u17NedLGKB4fWyKDvZARcys13kNUcI12KDdu i4rliaY3vXT+bnP7rdcpORal3r+SdqM5uByROHNZ+014rVJIVAY+ahhk/0RmdJTsv791JSkT FuPzjYbkthqCsLIwa2XFHLBYSZuLvZMpL8k4rSMuI529XL48etlK7QNNVDtwmHUGY+xvPvPP GOZwjmX7sHsrtEdkerjmcMuqhpvANpyPsFe8ErQCOrPhDIkZBSNcLur7zwj6m0+85eUTmcj8 1uIk4wip39tY3UrBisLzR9m4VrOd9AVw/JRoPDJFq6f4reOSOLbBd5vr7IvYtOSnTVMqxR4 4vnQcPqEcfTtb4kBIgQQAQIADAUCTzltCwUDABJ1AAAKCRCXELibyletfAo9CACWRtSxOvue Sr6Fo6TSMqlodYRtEwQYysEjcXsT5EM7pX/zLgm2fTgRgNzwaBkwFqH6Y6B4g2rfLyNExhXm NW11e/YxZqVRyMyRUEp6qGL+kYSOZR2Z23cOU+/dn58xMxGYChwj3zWJj+Cjw9U+D/6etHpw UrbHGc5hxNpyKQkEV5J+SQ5GDW0POONi/UHlkgSSmmV6mXlqEkEGrtyliFN1jpiTRLPQnzAR 198tJo3GtG5YutGFbNlTun1sXN9v/s4dzbV0mcHvAq/lW+2AT6OJDD204pp/mFxKBFi4XqF6 74HbmBzlS7zyWjjT2ZnujFDqEMKfske/OHSuGZI34qJ3iQEiBBABAqAMBQJPSpCtBQMAEnUA AAoJEJcQuJvKV618L1QH/ijaCAlgzQIvESk/QZTxQo6Hf7/ObUM3tB7iRjaIK0XWmUodBpOC 3kWWBEIVqJdxW/tbMbP8WebGidHWV4uX6R9GXDI8+egj8BY8LL807gKXkqeOxKax0NSk5vBn gpix2KVlHtWIm7azB0AiCdcFTCuVElHsIrhMAqtN6idGBVKtXHxW3//z9xiPvcIuryhj8orS IeJCtLCjji7KF2IUgCyyPJefr/YT7DTOC897E1I01E4dDymNur41NjobAogaxp6PdRNHBDum y8pfPzLvF30Y4Cv+SEa/EHmCOTHTamKaN6Jry/rpofqtueiMkwCi81RLqQd0ee6W/iui8Lwp /2 KJASIEEAECAAWFAk9V2xoFAwASdQAACgkQ1xC4m8pXrXy9UQgAsVc8HNwA7VKdBqsEvPJgxVlm6Y+9JcqdQcA77qSMClc8n6oVF1RpI2yFnFUpj1mvJuW7iiX98tRO3QKWJIMjEPovgZcS bhVhgKXiU87dtWwmcYhMsXBAYczbsSaNWhOIPwKHuQ+rYRevd0xGD0013P7pocZJR850tM9e 5809bzdsRYZpFW5MkrD7Aity5GpD65xYmAkbBwTjN4eNlp0nHVdSbVf4Fsjve6JC6yzKOGFB VU1TtAR2uPK6xxpn8ffzCNTA1vKXEM8Hqjyq4LWSdDTBIevuAqkz4T2eGJLXimhGpTXy7vz+ wnYxQ9edADrnfcqLbfz8s/wmCoH4GJAFNIkBIqQQAQIADAUCT2eDdwUDABJ1AAAKCRCXELib vletfFBEB/9RmWSSkUmPWib2EhHPuBL6Xti9NopLOmj5MFzHcLtqoommKvpOUwr1xv0cZMej  ${\tt ZenU3cW1AvvY287oJwmkFRFu9LJviLSGub9hxtQLhjd5qNaGRFLeJV8Y0Vtz+se2FWLPSvpj}$ mWFdfXppWQO/kIqVZoXcGJQrQWcetmLLqU9pxRcLASO/e5/wynFXmqSajxWzWHhMvehvJTOq siYWsOxgT/XaWOTvJHkpYJoXx4XKXnocvc8+X3OkxAFfOHCwWhYI+7CN8znDgxYuX//PKfDG 2Un0JHP1za8rponwNG7c58Eo3WKIRw0TKeSwOc1cSufnFcrPenmlh2p70EvNRAINiQEiBBAB AqAMBOJPeKdGBOMAEnUAAAoJEJcOuJvKV618YwoIAMn3uqSB4Ge1D61m0pIXJfOcC6BhCZvM mV3xTp4ZJCdCQzjRV3rZRkt0DwyOVYpLzLgDgvbRwjXjOzm0ob1DvYHFA7DnGTGUsBLDX/xZ 5gRvDtkD6w8b/+r2/eQiSu7ey/riYwB6dm3GzKR7FEbIK6bEuPOUBwvV2tYkZRqTYqXq7NBL uNv7c80GWhC/PqdvdhFn4KAvL0PjVIqr5+mdXyviKqG7uvquYBDtDUMX1qqZpi+fb7EsbJYf  $\verb|EkBR63jGQw04unqT1EXWds17gj+yp4IHbkJmEJMS8d2NIZMPbI1HmN+haTA73DwNkbVD1ata| | | | | | | | | | | | | | | | | | |$ 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  $\verb|MX20+1ybSTjjHIp3X81dYx01Sa3AqwKEBclLdg5yIyAjHq2phROd2s/gjqrWt+uJASIEEAEC||$ AAwFAk/1PVUFAwASdQAACqkQ1xC4m8pXrXwn3AqAjWUh31IxsQcXo8pdF7XniUSlqnmKYxT+ UZOP711xeaV/yjY+gwyZvf8TWT4R1Rp5IGg6aNLwLaDB31cXBGuXAANGUr+kblewviHnCY3Z +PWiuiusle+ofjbs8tFAr3LN3Abj70dME7GOhLyplP2mXIoAlnMDJ0AyrKx5EeA2jS8zCWCu ziiOj4ZwUZAesXchpSO9V9O86YiPtp+ikV0hmYqZpIXRNcHOpxnVyEW/95MFwi4qpG+VoN57 kWBXv6csfaco4BEIu9X/7y4OLbNuvzcinnHa0Pde5RnRlbEPQBBZyst2YZviWTFsbG8K2xok  $\verb|dotdZDabvrRGMhRzBUwQEokBIgQQAQIADAUCUAZhawUDABJ1AAAKCRCXELibyletfDJUCAC+| | | | | | | | | | | | | | | | | | |$ 68SXrK4aSeJY6W+4cS6xS//7YYIGDqpX4qSlW1tMIKCIWNhHkZqxKnWClnmvqGhw6VsZ2N0k YdOnIrzEPWL7qplZRiE1GDY85dRXNw0SXaGGi7A8s6J9yZPAApTvpMS/cvlJO+IveFaBRHbI RRndS30qZVXq48RH20lHep3o7c964WTB/41oZPJ7iOKqsDLdpjC1kJRf09iY0s/30rjL7nJq 5m14uY16rbqaIoL81C7iyc0UKU9sZGMcPV7H0oOIAy206A3hYSruytOtiC1PnfVZjh14ek2C q+Uc+4B8LQf5Lpha4xuB9xvp1X5Gt3wiPrMzcH89yOaxhR8490+0iQEiBBABAqAMBQJQGC19 BQMAEnUAAAoJEJcQuJvKV618CbcIAJCXDbUt96B3xGYqhOx+cUb+x8zcy91yNV8QC2xjd9Mr 02LJTQHfJfQ9Td6LfuoRb7nQHOqJK1/lWE28t9tlH7I+i7ujYwA/fWardRzqCulNXrgFEiQK ZFaDjRYyM0jWG/sA3/Rq2CMBNhBeCcTDuZ8VvRdm0xMPpyavP8D2dM9WBkPHOik4yAIILVkr hWmr0Up0JhRoelfeyqcN/6ClUgeRMIyBYthA55fk2X5+CerommlpDfJJlFQOv64VSzS68NG8 j9yf66uuL3bB00dz0MW6Yq/P9wskCDlMbYm/UnHfB5wAuxWpDeAvt/u+vU4xqqEjkUQGp03b 0v1x179maSuJASIEEgEKAAwFAlWg3HIFgweGH4AACgkQSjPs1SbI/EsPUQf/Z6Htrj7wDWU8 vLYv3Fw23ZuJ8t8U/akSNwbq6UGgwqke+5MKC1fpk90ekzu5Q6N78XUII3Qq8HnfdTU0ihYq qd3A1QmO6CG2hEz5xoxR1jJziRCbb1J7qEw8N/KzBcTkHB4+aq6bjFY9U4f9xU3TjPIu7F2V Bk1AX+cmDo8yzPjDnP4ro0Yabbg0Q9xzvaK/7pFRz+vL/u/1xW7iE7n6vXTiaY1XnIt5xAXX dwfLYmWeAqdc9KXFN1t41fuqrETtNCHme+JI+B2Tz2qHmMVLHiDV59eLC0uU/uVsOXEd26ib JC4f3KqY9kxuQm325kNzxnMxiwMPCVzsEh7lsYp+OokBMwQQAQqAHRYhBADTXowDFGilEoOK 6kPAyq+7WPawBQJasiYMAAoJEEPAyq+7WPawox0H/i96nkq1ID61ux+i20cOhVZylNJ770Vv  ${\tt 0zfXddWRN/67SuMVjLLiD/WfnDpw6ow6NM7vfEwbmvo1qeFF7rWWTPLm57uZfTk73un3fbaLlower} \\$ JiDZyrUStQKK/yhGAZmwulOQq7XBm+u8G9UcFi4XQxuoc5I/v/lUgbxXBADlxlfzpkIDwOaB s23RDiMcWZGcosUkYHXlm8scU0tRANVLQ/PHgttlUl3x2PLzrdQm3YUDKUJ9+yn02jN2sYwt laSohj4UbLnq6pI4CXWZR7XWQs+NX7P3R359FDtw7OhyKoVuIkRFZljY0i3wQgwl/Sm2DAg9 31sZDVc/avEUaOO+VuJuvJ+JATMEEAEIABOWIOOGFx4znGT7HFjpuwT3iPLIbOWZfAUCXJ70 KwAKCRD3iPLIbOWZfGoXB/wN0P3m27fY/6UXTl0Ua3H+24ueUdLipsvR8ZTwEfnwkhLrbggE 0Em7ZuhZkzv7j856qv/tOekYYqWGq1CLalD3y371LAGq1tjY3k/q2RWLxLXNdzqXEyFvaNQA  $\verb"oQa9aC2Q7FOyEMwVkkXrGa4MML7IBkrtMds9QPKtfipachPf6tQOFc12zHRjXMZi0eRWyQue" and the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the statement of the state$ 0sLLiJZPn7N8bBAJyZ9IJEpkhNrKS+9J5D1Refj++DwBKDh04kQXZFEZZhxcunqQW5oMBQqr uW2hULTLeiEV+C516OnwWJOz6XKJpOJp8PY0bO8pGqToGIYHkoX2x64yoROuZasFDv7sFGX6 7QxyiQEzBBABCAAdFiEEENOMfMPATUAxIpzAoiiOmODCOrwFalv/EJIACqkQoiiOmODCOrwq uAf+IVXpOb2S3UozWJLSOyWG0wO51qo4IBVpHv6hKUhDFj47YdUbYWO+cqGNBjC7FVz54PUM PIdxImGHE1NHH+DNR8hvvAi+YpnqqdT3g+OgZ6XoYevret5B2b5fRgN1/HWUjaJ/n5g6SMsC +3DrmdMu1FEDnKy/1HwOvOOXKt/U2rXE1ILOmVdMavRJEwkrk2SVwbdeass2EInZVsmWL+ot 9dU5hrkmLA16iHUoK6zF6WaI1oi7UU2kqUF2DNyZG/5AumsNhxE608EAs1zEdN8wibXL48vq Z4Ue9GvImokdlq/r/4BMUdF1qLEZHBkbaklK1zXx17uMiW3ZIcqpq5HqwYkBMwQQAQqAHRYh BBTHGHD/tHbA;AF4NhhrzPE15/iCBOJZ+o/oAAoJEBhrzPE15/iCyfMH/3YP3ND8;FgIWkmG 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  ${\tt Pvdq39ARyHA1rk0hXZ+OqsYBr1W7KLyPrbPA3N+/2RkMz6m+T8ZksOrEdF/90nC9Rky4Wbg4}$ SJqWQNNSMfqT0rQL2Qvne598FKmltrTJuwBtIrSeuL/dbKt+hkLqnRjnmtA5yPaf0qXvMtfU P9qoOMWD+A2BU/bXJokBMwOOAOqAHRYhBFBqHh7ZZZpG0pq7f1ToXvZveJ/LBOJbleqpAAoJ EFTOXvZveJ/LS0YH/jpcVprmEGnqlC0mYG2MlRqeK4T8Y6UnHE2zBPc125P4QcQfhqUJ98m4 0B5UkzljreFr9Zebk3pE8r4NBsamlJvi8sGbZONTsX4D3oW9ks0eicKOcTZJgtX5RmSNFh63 +EHbqTneK/NTQIuqRSCOufqCOH6QY1PVsICBlFZUPMfuxRlO7EwHKNIHPVBZNlM7AXxdjCMU kXvda8V14kActb1w7NWxWxo5q4hkQ2K3FsmbWXvz+YBhJ8FnRjdzWNUoWveggOD6u4H7GuOg kCyXn1fVnbCyJWsXQT9polJRnIAJMAtykcYVLNS/IS65U+K1cMshcF+Gil9BuGyckbRuNaSJ ATMEEAEIABOWIQRh2+o6RdTFb7cS1WG3d+zE2Q5m7gUCWdJutAAKCRC3d+zE2Q5m7rgJB/9k c+prmrnjsq/Lt6d90LqYoavvIeFkAoDhhWgQeEOAD1wgyHIpS6qoMKgvBlvda2r0bmk1kUL2 xQaiDj36wB5yJHauOnFX+3ZJ6QCYUaeoWtqO2ROHvTiuyUdVKC5NtKaHpM1/1P/j1/1ZRWay idqqH7EnwDMt+900xD02n5J29Vp9uP01GtMVsVSiJCGcOxwNBqNiXX1BpZbN4bRm5F8DAGiN v4ZI69QZFWbpj8wFVJ/rV4ouvCFPlutVEAuIlKpAj35joXDFJhMvPpnPj84iocGqYPZHKR6j a90+o8dZw3hXObFowjcxsJuQUTVkPuhzqr6kEu1ampaQ8OGpXCZHiQEzBBABCAAdFiEEZ/mR TQQxCZjglXUwgzhtKKq2evsFAltbmWkACgkQgzhtKKq2evsdrAgAubfuGlvWX3TTG/VYYrfM 1aS1Roc034ePoJHK5rLT00/TnnnObw38kJM1juyu4Ebfou+ZAlspiWgHad62R1B29Kys/6uC qG2Jvbf716da4oLXeLYd9eb+IKVEiSb2yfbsLtLLB0c/kBdcHUp6A1zz0HV811HWj1Wx8cFU MV7aAQoOfnNBbnNWLzNXXLYGHh47/QmjifE5V8r6UJZGsyv/1hP4JHsQ2nqcM8Vfj+K+HEuu nnxzgWAcQXP/0IhI11VwoWhsJ1HW+4kwW02DDopdBfLTzCtzcdOkfBcCg8hsmC4Jpxww5eHm saY6sIB32keCpikVOGwdGDbRH7+da8knzokBMwQQAQqAHRYhBG4VA/I1W5kLV/VchhLcHkBr mersBQJaX4N4AAoJEBLcHkBrmersksUH/3M0cypXBnyGI1/yE576MDa0G1xJvciup0ELeyhj 48Y7IAr7XiqDtiPt8tlIiPFF8iaw56vJw5H6UKraOcjZHOH1SwDr5gAWJgMqnqlFX/DxVKif USt81KX0tHN6t6oMESgm2jRKvcWjh6PvEZlIArxZG4IjrErqWIJjUJR86xzkLyhRVTkUL/Yk uNlli013AlaD/0CGuAnjrluUUXypadtNr7/qsBx8dG6B/VMLWToEDEon76b8BzL/Cqr0eRyq  $\texttt{Qz\,6} \texttt{KWi\,3} \texttt{hmsK+mE} \texttt{4+2} \texttt{VoDGwuHquM} \texttt{90R0uS} \texttt{9Z+7LUws24mX5QE7fz+AT9F5pthJQzN9BTVgvGc} \\ \texttt{Volume 1} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volume 2} \texttt{Volum$ kpI2sz3PNvzBL5WJATMEEAEIAB0WIQR00X0/mB27LBoNhwQL60sMns+mzQUCWoyYfgAKCRAL 60 s Mns + mzYgnB/9y + G1B/9tGDC + 9pitnVtCL2yCHGpGAg + TKhQsabXzzQfyykTgzCHhvqRQc + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1B/9tGDC + G1BXHz5NSgR0Io+kbGMUUqCaen6OlcORVxYIuivZekJOAG+9kiqWRbyTv4aR6zvh8O5wCyEhhyi ifi65PM7y9lD6i22gTt/JoDnFkP5Ri6Af/fZ9iaIaluOKJCU5xY1Lt/BorGlrGvX5KiZD8xc AjhJRATZOCJ21gbxISSxELAfH42KzGAvJw/0hARrMk1/eK0HVDpD47mcmC5h/O/HlwPYi0hn xB+6/nuwwtRqMDBufNV0StU43njxCYmGI9/I1z5Vs+zhz8ypw/xCr1U7aAPZQdSSsfEViQEz  ${\tt BBABCAAdFiEEelR80pStCJs7bhrK1TniJxBsvzsFAlv+8d0ACgkQ1TniJxBsvzsiFwf/a3ltrangler} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {\tt Calching} \\ = {$ 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 vF7wcahaXpF+0Spl9vE2.TiesST7uOobCUm1Eix.TP0vMDcO1vTf.THlbThB/f3PE3rX7TzYTdI s3Kb400NaUfNy9jYtYkCHAQQAQIABqUCVJqcUqAKCRB3MepTnaVyot2+D/9wAQ+p03lVMpYS qMWMNLqjq3z7OrN0NYNpxUXAonxECjUzZKSUPGci+fPKx13ZUenk+ruLqtqJmjmUOR6u1Dov BpDFzhfqbIpjgtMDrnY5sWqxJ+CH2Rb5okEEDJ5qE9DwIMP5iXbf4xjnB0yPiq3sp983PLvy 8ttidWe9FDf8JuhWLHRJHODQjc6LufcHSWKG9fLmCjL2KSPN1696MwR+N95EKCivLL2PlG8c f08Xd8lW1S0cJLh/6TEuZtAnVeo0NUOGUXOPPyhTPP/xhfLeKbkxjtm6rg/jBaIjuuQgUyNN hKnP96/GRWWRHvio6eBPalhUcvImSrCHnqLRpdyMxmK67ZzKZS3YsH0ixozJYE0mNevZ2hEY wB+O5HllqK22YwvJnCLH2ZZWTu2TCUjGZP8hbo2nSoyENlxZio9Gl/v4ypjdlgwrjnnZvxoM yOFeuc47AuzP5QjhtlrWv12C4hYi3YLZvkLVFD0CxAE/CDuHk/4eFG4UC4Mor6+BXwVG7NE1 4qQWrAHjLQ2/sHMpsUqY/5X7+StG/78PLP0HP+PIBCDDTa7W0+6kf0EaGVHKW43IIkVNI2Ps b44tTT+Xhc2mHk44LuzL4Axlywv+CxP9NcKLNFwK4Ck1M8Np6cAKlu+Dw6gjOY1aGHgtdsBQ cIqZj/+ETD0+9NkDXEoeDIkCHAQSAQIABqUCUliwpAAKCRCiKuTrQynFRXZdD/9vb+690GSR t456C6wMLgBl+Ocv9XeaCTiJjLgAL2G6bRH2g2VcNHnU/VMTD2YLVu0eP7ubsirVrmR7nAqL sQ1mKKWvTI+p5aAvn4sL3x3P8vzmGoDAigZ458yGuVpVsBkSPjJBMAkMDfm9kdWxCanzuKXS b591fTg4EtcHPDzoSgABntASgfioVxP2TVPfre282cibeYS+RDlaMTVH25vElrWDuF2U1CVW SMWY9mskr1+XjPnoO2jz0+jhKB7jyMMfSmJqzqcBNqezFbzX2fPmNnMZzEucVFFHmIhNVmL2 rOwc/s1tSHerG5YIdL3HOJek5xJljzjzFfDrdjmMMl+nO6nO78oePoLNdglQQSqn0yW6gZv8  $\verb|EIIQ/N1nSi/LEW60z8Ffxzo08TqxMMX9QRLbVE6p+7C0nqolhZf6UEiDIIm+PihF1vPFSV54| \\$ +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 BH+P4v2705oUXOVHZOXCWI,Gt.3v4UBOJhrDYPAAoJEAXCWI,Gt.3v4Uh2oOAMS3sK0MEnTPE+qu 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  ${\tt s4tMWM4EVJ2OygnrcMuIEJdXVsR0Ln1gJLuQ9HpWehve0d7/cI2kN7a0fqgE7bMvSPyxWL3mm} \\ {\tt s4tMWM4EVJ2OygnrcMuIEJdXVsR0Ln1gJLuQ9HpWehve0d7/cI2kN7a0fqgE7bMvSPyxWL3mm} \\ {\tt s4tMWM4EVJ2OygnrcMuIEJdXVsR0Ln1gJLuQ9HpWehve0d7/cI2kN7a0fqgE7bMvSPyxWL3mm} \\ {\tt s4tMWM4EVJ2OygnrcMuIEJdXVsR0Ln1gJLuQ9HpWehve0d7/cI2kN7a0fqgE7bMvSPyxWL3mm} \\ {\tt s4tMWm4EVJ2OygnrcMuIEJdXVsR0Ln1gJLuQ9HpWehve0d7/cI2kN7a0fqgE7bMvSPyxWL3mm} \\ {\tt s4tMWm4EVJ2OygnrcMuIEJdXVsR0Ln1gJLuQ9HpWehve0d7/cI2kN7a0fqgE7bMvSPyxWL3mm} \\ {\tt s4tMWm4EVJ2OygnrcMuIEJdXVsR0Ln1gJLuQ9HpWehve0d7/cI2kN7a0fqgE7bMvSPyxWL3mm} \\ {\tt s4tMWm4EVJ2OygnrcMuIEJdXVsR0Ln1gJLuQ9HpWehve0d7/cI2kN7a0fqgE7bMvSPyxWL3mm} \\ {\tt s4tMWm4EVJ2OygnrcMuIEJdXVsR0Ln1gJLuQ9HpWehve0d7/cI2kN7a0fqgE7bMvSPyxWL3mm} \\ {\tt s4tMWm4EVJ2OygnrcMuIEJdXVsR0Ln1gMvMehve0d7/cI2kN7a0fqgE7bMvSPyxWL3mm} \\ {\tt s4tMWm4EVJ2OygnrcMuIEJdXVsR0Ln1gMvMehve0d7/cI2kN7a0fqgE7bMvSPyxWL3mm} \\ {\tt s4tMWm4EVJ2OygnrcMuIEJdXVsR0Ln1gMvMehve0d7/cI2kN7a0fqgE7bMvSPyxWL3mm} \\ {\tt s4tMWm4EVJ2OygnrcMuIEJdXVsR0Ln1gMvMehve0d7/cI2kNfquMehve0d7/cI2kNfquMehve0d7/cI2kNfquMehve0d7/cI2kNfquMehve0d7/cI2kNfquMehve0d7/cI2kNfquMehve0d7/cI2kNfquMehve0d7/cI2kNfquMehve0d7/cI2kNfquMehve0d7/cI2kNfquMehve0d7/cI2kNfquMehve0d7/cI2kNfquMehve0d7/cI2kNfquMehve0d7/cI2kNfquMehve0d7/cI2kNfquMehve0d7/cI2kNfquMehve0d7/cI2kNfquMehve0d7/cI2kNfquMehve0d7/cI2kNfquMehve0d7/cI2kNfquMehve0d7/cI2kNfquMehve0d7/cI2kNfquMehve0d7/cI2kNfquMehve0d7/cI2kNfquMehve0d7/cI2kNfquMehve0d7/cI2kNfquMehve0d7/cI2kNfquMehve0d7/cI2kNfquMehve0d7/cI2kNfquMehve0d7/cI2kNfquMehve0d7/cI2kNfquMehve0d7/cI2kNfquMehve0d7/cI2kNfquMehve0d7/cI2kNfquMehve0d7/cI2kNfquMehve0d7/cI2kNfquMehve0d7/cI2kNfquMehve0d7/cI2kNfquMehve0d7/cI2kNfquMehve0d7/cI2kNfquMehve0d7/cI2kNfquMehve0d7/cI2kNfquMehve0d7/cI2kNfquMehve0d7/cI2kNfquMehve0d7/cI2kNfquMehve0d7/cI2kNfquMehve0d7/cI2kNfquMehve0d7/cI2kNfquMehve0d7/cI2kNfquMehve0d7/cI2kNfquMehve0d7/cI2kNfquMehve0d7/cI2kNfquMehve0d7/cI2kNfquMehve0d7/cI2kNfquMehve0d7/cI2kNfquMehve0d7/cI2kNfquMehve0d7/cI2kNfquMehve0d7/cI2kNfquMehve0d7/cI2kNfquMehve0d7/cI2kNfquMehve0d7/cI2kNfquMehve0d7/cI2kNfquMehve0d7$ yTA4FwdbrebBr2y7ix1XZ6WtX/rqTvo2HTDFLle0ZwMbbfAtoFX0M01PtXTLmJA15w1G8Nj8 bthWdN4KVFyOpqPt7OXc/G1YNLzcyYQXX5e8Uskmg40OH5cQV5OFEG8qpxTg53wANDdxXGzs NUQe84Qkoyk75nwzVfsi00/OhTZmfIC48esXcs0kTrkSPrFcHktSMoYPmHfV3dTF17ifjz5a C2SL22R+RokWuzGxxpvEaOAWIyCt6izf1a+CjnXPD2Jw3yDC/Oeq68XYiSrbeFdCRzObS9YP ipUFI1HuCiNZeGq3rFL2N2JodXq2LGORJz1RKazT7uAfRr5z7W1FtDtNeVNRTCBQYWNrYWdl IHNpZ25pbmcqa2V5ICh3d3cubX1zcWwuY29tKSA8YnVpbGRAbX1zcWwuY29tPohGBBARAqAG  ${\tt BQI/rOOvAAoJEK/FI0h4g3QP9pYAoNtSISDDAAU2HafyAY1LD/yUC4hKAJ0czMsBLbo0M/xPASMSDAAU2HafyAY1LD/yUC4hKAJ0czMsBLbo0M/xPASMSDAAU2HafyAY1LD/yUC4hKAJ0czMsBLbo0M/xPASMSDAAU2HafyAY1LD/yUC4hKAJ0czMsBLbo0M/xPASMSDAAU2HafyAY1LD/yUC4hKAJ0czMsBLbo0M/xPASMSDAAU2HafyAY1LD/yUC4hKAJ0czMsBLbo0M/xPASMSDAAU2HafyAY1LD/yUC4hKAJ0czMsBLbo0M/xPASMSDAAU2HafyAY1LD/yUC4hKAJ0czMsBLbo0M/xPASMSDAAU2HafyAY1LD/yUC4hKAJ0czMsBLbo0M/xPASMSDAAU2HafyAY1LD/yUC4hKAJ0czMsBLbo0M/xPASMSDAAU2HafyAY1LD/yUC4hKAJ0czMsBLbo0M/xPASMSDAAU2HafyAY1LD/yUC4hKAJ0czMsBLbo0M/xPASMSDAAU2HafyAY1LD/yUC4hKAJ0czMsBLbo0M/xPASMSDAAU2HafyAY1LD/yUC4hKAJ0czMsBLbo0M/xPASMSDAAU2HafyAY1LD/yUC4hKAJ0czMsBLbo0M/xPASMSDAAU2HafyAY1LD/yUC4hKAJ0czMsBLbo0M/xPASMSDAAU2HafyAY1LD/yUC4hKAJ0czMsBLbo0M/xPASMSDAAU2HafyAY1LD/yUC4hKAJ0czMsBLbo0M/xPASMSDAAU2HafyAY1LD/yUC4hKAJ0czMsBLbo0M/xPASMSDAAU2HafyAY1LD/yUC4hKAJ0czMsBLbo0M/xPASMSDAAU2HafyAY1LD/yUC4hKAJ0czMsBLbo0M/xPASMSDAAU2HafyAY1LD/yUC4hKAJ0czMsBLbo0M/xPASMSDAAU2HafyAY1LD/yUC4hKAJ0czMsBLbo0M/xPASMSDAAU2HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAGAAU4HAAU4H$ aJ60x9Q5Hmw2uIhGBBARAqAGBQI/tEN3AAoJEIWWr6swc05mxsMAnRaq9X61Yqu1kbfBiqDk u4czTd9pAJ4q5W8KZ0+2ujTrEPN55NdWtnXj4YhGBBARAqAGBQJDW7PqAAoJEIvYLm8wuUtc f3QAnRCyqF0CpMCTdIGc7bD05I7CIMhTAJ0UTGx001d/VwvdDiKWj45N2tNbYIhGBBARAqAG BOJEqG8nAAoJEAssGHlMO+b1q3AAn0LFZP1xoiExchVUNyEf91re86qTAKDYbKP3F/FVH7Nq c8T77xkt8vuUPYhGBBARAgAGBQJFMJ7XAAoJEDiOJeizQZWJMhYAmwXMOYCIotEUwybHTYri Q3LvzT6hAJ4kqvYk2i44BR2W2os1FPGq7FQqeYhGBBARAqAGBQJFoaNrAAoJELvbtoQbsCq+ m48An2u2Sujv15k9PEsrIOAxKGZyuC/VAKC1oB7mIN+cG2WMfmVE4ffHYh1P5ohGBBMRAgAG  ${\tt BQJE8TMmAAoJEPZJxPRgk1MMCnEAoIm2pP0sIcVh9Yo0YYGAqORrTOL3AJwIbcy+e8HMNSoN}$ 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  ${\tt H3xvCna/s7Teufud0JLXoLBedFXeB5Cg2KlEoxINqMo+lm/VGJmbykwqoRvxZLDfnbFag5zG2KlEoxINqMo+lm/VGJmbykwqoRvxZLDfnbFag5zG2KlEoxINqMo+lm/VGJmbykwqoRvxZLDfnbFag5zG2KlEoxINqMo+lm/VGJmbykwqoRvxZLDfnbFag5zG2KlEoxINqMo+lm/VGJmbykwqoRvxZLDfnbFag5zG2KlEoxINqMo+lm/VGJmbykwqoRvxZLDfnbFag5zG2KlEoxINqMo+lm/VGJmbykwqoRvxZLDfnbFag5zG2KlEoxINqMo+lm/VGJmbykwqoRvxZLDfnbFag5zG2KlEoxINqMo+lm/VGJmbykwqoRvxZLDfnbFag5zG2KlEoxINqMo+lm/VGJmbykwqoRvxZLDfnbFag5zG2KlEoxINqMo+lm/VGJmbykwqoRvxZLDfnbFag5zG2KlEoxINqMo+lm/VGJmbykwqoRvxZLDfnbFag5zG2KlEoxINqMo+lm/VGJmbykwqoRvxZLDfnbFag5zG2KlEoxINqMo+lm/VGJmbykwqoRvxZLDfnbFag5zG2KlEoxINqMo+lm/VGJmbykwqoRvxZLDfnbFag5zG2KlEoxINqMo+lm/VGJmbykwqoRvxZLDfnbFag5zG2KlEoxINqMo+lm/VGJmbykwqoRvxZLDfnbFag5zG2KlEoxINqMo+lm/VGJmbykwqoRvxZLDfnbFag5zG2KlEoxINqMo+lm/VGJmbykwqoRvxZLDfnbFag5zG2KlEoxINqMo+lm/VGJmbykwqoRvxZLDfnbFag5zG2KlEoxINqMo+lm/VGJmbykwqoRvxZLDfnbFag5xG2KlEoxINqMo+lm/VGJmbykwqoRvxZLDfnbFag5xG2KlEoxINqMo+lm/VGJmbykwqoRvxZLDfnbFag5xG2KlEoxINqMo+lm/VGJmbykwqoRvxZLDfnbFag5xG2KlEoxINqMo+lm/VGJmbykwqoRvxZLDfnbFag5xG2KlEoxINqMo+lm/VGJmbykwqoRvxZLDfnbFag5xG2KlEoxINqMo+lm/VGJmbykwqoRvxZLDfnbFag5xG2KlEoxINqMo+lm/VGJmbykwqoRvxZLDfnbFag5xG2KlEoxINqMo+lm/VGJmbykwqoRvxZLDfnbFag5xG2KlEoxINqMo+lm/VGJmbykwqoRvxZLDfnbFag5xG2KlEoxINqMo+lm/VGJmbykwqoRvxZLDfnbFag5xG2KlEoxINqMo+lm/VGJmbykwqoRvxZLDfnbFag5xG2KlEoxINqMo+lm/VGJmbykwqoRvxZLDfnbFag5xG2KlEoxINqMo+lm/VGJmbykwqoRvxZLDfnbFag5xG2KlEoxINqMo+lm/VGJmbykwqoRvxZLDfnbFag5xG2KlEoxINqMo+lm/VGJmbykwqoRvxZLDfnbFag5xG2KlEoxINqMo+lm/VGJmbykwqoRvxZLDfnbFag5xG2KlEoxINqMo+lm/VGJmbykwqoRvxZLDfnbFag5xG2KlEoxINqMo+lm/VGJmbykwqoRvxQ1AdxAdxAdxAdxAdxAdxAdxAdxAdxAdxAdxAdxAdxA$ 59+OWw4TC8nz1IQYIBn22YiWRk5zsCJA40O+KL1vwBiFDrREhALQc/YBJKYrRX3ZV4U/EeYD KB0NCBk1W1tXGCee3uhM0S5VFc1j7Pq58ECuntH5xOy+KMNFljiOwvWfbaFTJvCjFOS+Op1X b4kBIqQQAQIADAUCSu86VAUDABJ1AAAKCRCXELibyletfGs8CACteI2BmKs24GF80JeWTOQI cvHnCdV7hKZOltbNPBbDv6qTt3iX2GVa10iYhI5Eg3Ojt/hKFJTMlfYZyI1peFodGjv7Lk51 u7zaNBvT1pBCP+eJspi6rGpSuhtMSb4O5jPclRBmbY+w9wctLyZf1zG+slSdw8adcRXQNFqr vVIZYOmu2S8FunqLfxpjewiFiDPzAzmbWzMoO2PLCYFhwV6Eh2jO33OGbvBmyHNFZBfX5F/+ kiveT47MEhrfhvtJ6ZOdpxtX8HvbvzPZcDLOI80W6rPTG76KW06ZiZrJ81YCa6a7D01v7BYv W2HoxzYcuumjRkGF4nqK4Mw+wefCp0H/iQEiBBABAqAMBQJLAF3aBQMAEnUAAAoJEJcQuJvK V618/g0H/ibXDOG2WOmC1LoT4H+ezXjPgDg8aiuz6f4xibTmrO+L4ScMX+zK0KZVwp6Kau28 Nx+gO0oAUW8mNxhd+cl0ZaY+7RIkxEvkooKKsArBmZT+xrE6CgHlAs3D4Mc+14nfD0aZaUbE iobWvXlYLl27MELLcWyeMlgbeNoucc473JddvmHSRRM5F9Qp28CvWDEXYqhq1laoaho8+cei pvzvuO30TwiuAOghefOHzAvFrRli99MI8xzF1ZOvBct+36SuYxDXvThkSd7aG9Us01W6W5Si JYt4cDyI0JDhbhZN0tzWYKcKMZMxf8w3jW4sfQL0prhHrARqqPiU8OTUH/VNX5CJASIEEAEC AAwFAksRgasFAwASdQAACgkQlxC4m8pXrXydogf/a3lofmYFMoE3p9SqGt/v28iyO0j9A1Lm qKwEhJkxff/X/Qa7pafGQ9J90JQkxYKMxydWPspTbDFMccZWkBK132vZp9Q3FHKpnDPDLK2S 25miTReeAAQNqMMFLeyy7ZHi5YsKwLbKxcSo7/m0jlitNYlmt94imFNpq/mHGsy6O+rLeQTA opuIzP3VwN6ItL5gIFxqWPmf/V0xh/vxTwLqJ66vECD8vyHrHblUzgiXHgyYbZPxAa2SRRd3 4V38phaZ/QsTkss+Sd/QeHChWyU9d6KengWwcr/nDO+K/hhmnO5Oqz02Upwyxrgi6484HQUN /Smf44VBsSD1DBjaAKjMr4kBIqQQAQIADAUCSyNN1AUDABJ1AAAKCRCXELibyletfCWiB/9c EZtdFVcsxpE3hJzM6PBPf+1QKuJORve/7MqNEb3TMWFgBxyOfvD7uMpCJyOrqq5AbUQfZfj9 K7qmzWUMuoYceGIlbdmHFBJwtmaF0BiyHaobgY/9RbdCNcbtzrW34feiW9aDZyvCoLHEVkCC QACSv3FwdYVkkRB5eihvpwJk5tpScdIA12YLqzmVTFdhrZuYvtDdQHjqoLMO8B9s9kok7D2T SpveVzXXPH68Z3JkVubhHT7cs+n+9PRvcaVJtsX2VTUY5eFVqmGuAUVrvp2aN8cKQ+mVcCQr  ${\tt VVIhT908YB5925MUx2VJml0y0nkBQuMZyzMEOVGkuU/G+pVrRmmAiQEiBBABAgAMBQJLJyaSSMD} \\ {\tt VIhT908YB5925MUx2VJml0y0nkBQuMZyzMEOVGkuU/G+pVrRmmAiQEiBBABAgAMBQJLJyaSSMD} \\ {\tt VIhT908YB5925MUx2VJml0y0nkBQuMZyzMEOVGkuU/G+pVrRmmAiQEiBBABAgAMBQJLJyaSSMD} \\ {\tt VIhT908YB5925MUx2VJml0y0nkBQuMZyzMEOVGkuU/G+pVrRmmAiQEiBBABAgAMBQJLJyaSSMD} \\ {\tt VIhT908YB5925MUx2VJml0y0nkBQuMZyzMEOVGkuU/G+pVrRmmAiQEiBBABAgAMBQJLJyaSSMD} \\ {\tt VIhT908YB5925MUx2VJml0y0nkBQuMZyzMEOVGkuU/G+pVrRmmAiQEiBBABAgAMBQJLJyaSSMD} \\ {\tt VIHT908YB5925MUx2VJml0y0nkBQuMZyzMEOVGkuU/G+pVrRmmAiQEiBBABAgAMBQJLJyaSSMD} \\ {\tt VIHT908YB5925MUx2VJml0y0nkBQuMZyzMEOVGkuU/G+pVrRmmAiQEiBBABAgAMBQJLJyaSSMD} \\ {\tt VIHT908YB5925MUx2VJml0y0nkBQuMZyzMEOVGkuU/G+pVrRmmAiQEiBBABAgAMBQJLJyaSSMD} \\ {\tt VIHT908YB5925MUx2VJml0y0nkBQuMZyzMEOVGkuU/G+pVrRmmAiQEiBBABAgAMBQJLJyaSSMD} \\ {\tt VIHT908YB5925MUx2VJml0y0nkBQuMZyzMEOVGkuU/G+pVrRmmAiQEiBBABAgAMBQJLJyaSSMD} \\ {\tt VIHT908YB5925MUx2VJml0y0nkBQuMZyzMEOVGkuU/G+pVrRmmAiQEiBBABAgAMBQJLJyaSSMD} \\ {\tt VIHT908YB5925MUx2VJml0y0nkBQuMZyzMEOVGkuU/G+pVrRmmAiQEiBBABAgAMBQJLJyaSSMD} \\ {\tt VIHT908YB5925MUx2VJml0y0nkBQuMZyzMEOVGkuU/G+pVrRmmAiQEiBBABAgAMBQJLJyaSSMD} \\ {\tt VIHT908YB5925MUx2VJml0y0nkBQuMZyzMEOVGkuU/G+pVrRmmAiQEiBBABAgAMBQJLJyaSSMD} \\ {\tt VIHT908YB5925Mux2VJml0y0nkBQuMZyzMEOVGkuU/G+pVrRmmAiQEiBBABAgAMBQJLJyaSSMD} \\ {\tt VIHT9097MUx2MUx2MUx2MUx2MUx2MUx2MUx2MUx2MUx2MUx2$ BQMAEnUAAAoJEJcQuJvKV618eU0IAKnVh6ymId9C3ZqVyxwTnOB8RMQceJzwCLqk2RT0dPhN 5ZwUcQN71Cp9hymMutC8FdKRK/ESK21vJF2/576Pln4fleOIbycBAEvqrL14epATj53uBizo NOTuwb1kximFERuW3MP4XiFUJB0tPws2vR5UU3t6GoQJJwNoIbz9DK2L6X/Qz3Tb9if6bPSK U6JR1Yn3Hos9ogg21vWCxgMTKUuPAYhmYjSvkaH3BihXi+c17MVvE7W5GJbOHuJo+MqSxu04 4qnvDHZpf4Mzc30XcG1ohjxefNyeiY2bzdI2yCaCtmW0lCW1Sc2oiE0zw06lD4hY5XmC2Xql MLsKB5VNXJGJASIEEAECAAwFAks4Ze4FAwASdQAACqkQ1xC4m8pXrXyWXqqAon2abiNvRzx9  $7364 \texttt{Mj} \times 411 \texttt{FvM1} \\ \texttt{tVebzNb0kDwZS1ABqTDGqq/ffZA/VZrU} + \texttt{h2eL97cQyGxJEQ5kkm/v1iobE} \\ \texttt{tVebzNb0kDwZS1ABqTDGqq/ffZA/VZrU} + \texttt{h2eL97cQyGxJEQ5kkm/v1iobE} \\ \texttt{tVebzNb0kDwZS1ABqTDGqq/ffZA/VZrU} + \texttt{h2eL97cQyGxJEQ5kkm/v1iobE} \\ \texttt{tVebzNb0kDwZS1ABqTDGqq/ffZA/VZrU} + \texttt{h2eL97cQyGxJEQ5kkm/v1iobE} \\ \texttt{tVebzNb0kDwZS1ABqTDGqq/ffZA/VZrU} + \texttt{h2eL97cQyGxJEQ5kkm/v1iobE} \\ \texttt{tVebzNb0kDwZS1ABqTDGqq/ffZA/VZrU} + \texttt{h2eL97cQyGxJEQ5kkm/v1iobE} \\ \texttt{tVebzNb0kDwZS1ABqTDGqq/ffZA/VZrU} + \texttt{h2eL97cQyGxJEQ5kkm/v1iobE} \\ \texttt{tVebzNb0kDwZS1ABqTDGqq/ffZA/VZrU} + \texttt{h2eL97cQyGxJEQ5kkm/v1iobE} \\ \texttt{tVebzNb0kDwZS1ABqTDGqq/ffZA/VZrU} + \texttt{h2eL97cQyGxJEQ5kkm/v1iobE} \\ \texttt{tVebzNb0kDwZS1ABqTDGqq/ffZA/VZrU} + \texttt{h2eL97cQyGxJEQ5kkm/v1iobE} \\ \texttt{tVebzNb0kDwZS1ABqTDGqq/ffZA/VZrU} + \texttt{h2eL97cQyGxJEQ5kkm/v1iobE} \\ \texttt{tVebzNb0kDwZS1ABqTDGqq/ffZA/VZrU} + \texttt{h2eL97cQyGxJEQ5kkm/v1iobE} \\ \texttt{tVebzNb0kDwZS1ABqTDGqq/ffZA/VZrU} + \texttt{h2eL97cQyGxJEQ5kkm/v1iobE} \\ \texttt{tVebzNb0kDwZS1ABqTDGqq/ffZA/VZrU} + \texttt{h2eL97cQyGxJEQ5kkm/v1iobE} \\ \texttt{tVebzNb0kDwZS1ABqTDGqq/ffZA/VZrU} + \texttt{h2eL97cQyGxJEQ5kkm/v1iobE} \\ \texttt{tVebzNb0kDwZS1ABqTDGqq/ffZA/VZrU} + \texttt{h2eL97cQyGxJEQ5kkm/v1iobE} \\ \texttt{tVebzNb0kDwZS1ABqTDGqq/ffZA/VZrU} + \texttt{h2eL97cQyGxJEQ5kkm/v1iobE} \\ \texttt{tVebzNb0kDwZS1ABqTDGqq/ffZA/VZrU} + \texttt{h2eL97cQyGxJEQ5kkm/v1iobE} \\ \texttt{tVebzNb0kDwZS1ABqTDGqq/ffZA/VZrU} + \texttt{h2eL97cQyGxJEQ5kkm/v1iobE} \\ \texttt{tVebzNb0kDwZS1ABqTDGqq/ffZA/VZrU} + \texttt{h2eL97cQyGxJEQ6kkm/v1iobE} \\ \texttt{tVebzNb0kDwZS1ABqTDGqq/ffZA/VZrU} + \texttt{h2eL97cQyGxJEQ6kkm/v1iobE} \\ \texttt{tVebzNb0kDwZS1ABqTDGqq/ffZA/VZrU} + \texttt{h2eL97cQyGxJEQ6kkm/v1iobE} \\ \texttt{tVebzNb0kDwZS1ABqTDGqq/ffZA/VZrU} + \texttt{h2eL97cQyGxJEQ6kkm/v1iobE} \\ \texttt{tVebzNb0kDwZS1ABqTDGqq/ffZA/VZrU} + \texttt{h2eL97cQyGxJEQ6kkm/v1iobE} \\ \texttt{tVebzNb0kM} + \texttt{h2eL97cQyGxM} + \texttt{h2eL97cQyGxM} \\ \texttt{h2eL97cQyGxM} + \texttt{h2eL97cQyGxM} + \texttt{h2eL97cQyGxM} + \texttt{h2eL97cQyGxM} \\ \texttt{h2eL97cQyGxM} + \texttt{h2eL97cQyGxM} + \texttt{h2eL97cQyGxM} + \texttt{h2eL97cQyGxM} + \texttt{h2eL97cQyGxM} \\ \texttt{h2eL97cQyGxM} + \texttt{h2eL97cQyGxM} + \texttt{h2eL97cQyGxM} + \texttt{h2eL97cQyGxM} + \texttt{h2eL97cQyGxM} + \texttt{h2eL97cQyGxM} + \texttt{h2eL97cQyGxM} + \texttt{h2eL97cQyGxM} + \texttt{h$ ZEFMT0pv9WMzfidqzhdKdcpbbxdaErIjD5fBACKdjazAUeH7zce2v+bBN019LZoRiXbNuqG9 381kJ2E4ZTYYfvftL/e4RzOggR9VD/A5MzxfXFbCVharHbeT8OwZv4Oz2UDaDszHsNKoG1WN pOSf2HTMBPNcsOSY/hIBRWNxnzdYOkWt7laeLNmN1eUEwzk4J7GnlambPIctOdoEUriMSaey TkLZGejKnwi/PqARyDW1FsReKNHD753ZMViUnAsq2IkBIqOOAOIADAUCS0oyJwUDABJ1AAAK CRCXELibyletfGodCAC5hjmxwquHSb8ZL0RifIL3j3iU6U7qLK1TQKkTqgELfUzeF9f8NuNR txLmzNk1T7YI9iji6NAtnuy43v61OMbqlkV8x69qNP36Owv408wXxEt0s5ViZuVOZJAY075c YRhopgfmhkh4hbkAoKCLajOROWUEEsDHsqqj8XLJuGRREURy8TJWaB/cotXsgiJf99gt+gIw In 8 tyb 3 + WVIUHW fw 2 + Drpd 3nfcMqgeO 54 PePJo 0BWW jaar + wgC/76 Se 286 IHc YMrml/Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx Adnvx 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 uck= =yia9 ---END PGP PUBLIC KEY BLOCK----

## <span id="page-102-0"></span>2.1.5 Installation Layouts

The installation layout differs for different installation types (for example, native packages, binary tarballs, and source tarballs), which can lead to confusion when managing different systems or using different installation sources. The individual layouts are given in the corresponding installation type or platform chapter, as described following. Note that the layout of installations from vendors other than Oracle may differ from these layouts.

- Section 2.3.1, "MySQL Installation Layout on Microsoft Windows"
- Section 2.8.3, "MySQL Layout for Source Installation"
- Table 2.3, "MySQL Installation Layout for Generic Unix/Linux Binary Package"
- Table 2.12, "MySQL Installation Layout for Linux RPM Packages from the MySQL Developer Zone"
- Table 2.7, "MySQL Installation Layout on macOS"

## <span id="page-102-1"></span>2.1.6 Compiler-Specific Build Characteristics

In some cases, the compiler used to build MySQL affects the features available for use. The notes in this section apply for binary distributions provided by Oracle Corporation or that you compile yourself from source.

icc (Intel C++ Compiler) Builds

A server built with icc has these characteristics:

• SSL support is not included.

## <span id="page-103-0"></span>**2.2 Installing MySQL on Unix/Linux Using Generic Binaries**

Oracle provides a set of binary distributions of MySQL. These include generic binary distributions in the form of compressed tar files (files with a .tar.gz extension) for a number of platforms, and binaries in platform-specific package formats for selected platforms.

This section covers the installation of MySQL from a compressed tar file binary distribution on Unix/Linux platforms. For Linux-generic binary distribution installation instructions with a focus on MySQL security features, refer to the [Secure Deployment Guide](https://dev.mysql.com/doc/mysql-secure-deployment-guide/5.7/en/). For other platform-specific binary package formats, see the other platform-specific sections in this manual. For example, for Windows distributions, see [Section 2.3, "Installing MySQL on Microsoft Windows"](#page-106-0). See [Section 2.1.3, "How to](#page-86-0) [Get MySQL"](#page-86-0) on how to obtain MySQL in different distribution formats.

MySQL compressed tar file binary distributions have names of the form mysql-VERSION-OS.tar.gz, where VERSION is a number (for example, 5.7.44), and OS indicates the type of operating system for which the distribution is intended (for example, pc-linux-i686 or winx64).

![](_page_103_Picture_7.jpeg)

#### **Warnings**

• If you have previously installed MySQL using your operating system native package management system, such as Yum or APT, you may experience problems installing using a native binary. Make sure your previous MySQL installation has been removed entirely (using your package management system), and that any additional files, such as old versions of your data files, have also been removed. You should also check for configuration files such as /etc/my.cnf or the /etc/mysql directory and delete them.

For information about replacing third-party packages with official MySQL packages, see the related [APT guide](http://dev.mysql.com/doc/mysql-apt-repo-quick-guide/en/) or [Yum guide](#page-171-0).

• MySQL has a dependency on the libaio library. Data directory initialization and subsequent server startup steps fail if this library is not installed locally. If necessary, install it using the appropriate package manager. For example, on Yum-based systems:

```
$> yum search libaio # search for info
$> yum install libaio # install library
```

Or, on APT-based systems:

```
$> apt-cache search libaio # search for info
$> apt-get install libaio1 # install library
```

- For MySQL 5.7.19 and later: Support for Non-Uniform Memory Access (NUMA) has been added to the generic Linux build, which has a dependency now on the libnuma library; if the library has not been installed on your system, use you system's package manager to search for and install it (see the preceding item for some sample commands).
- **SLES 11**: As of MySQL 5.7.19, the Linux Generic tarball package format is EL6 instead of EL5. As a side effect, the MySQL client bin/mysql needs libtinfo.so.5.

```
A workaround is to create a symlink, such as ln -s
libncurses.so.5.6 /lib64/libtinfo.so.5 on 64-bit systems or ln
-s libncurses.so.5.6 /lib/libtinfo.so.5 on 32-bit systems.
```

• If no RPM or .deb file specific to your distribution is provided by Oracle (or by your Linux vendor), you can try the generic binaries. In some cases, due to library incompatibilities or other issues, these may not work with your Linux installation. In such cases, you can try to compile and install MySQL from source. See Section 2.8, "Installing MySQL from Source", for more information and instructions.

To install a compressed tar file binary distribution, unpack it at the installation location you choose (typically /usr/local/mysql). This creates the directories shown in the following table.

<span id="page-104-0"></span>**Table 2.3 MySQL Installation Layout for Generic Unix/Linux Binary Package**

| Directory     | Contents of Directory                                            |
|---------------|------------------------------------------------------------------|
| bin           | mysqld server, client and utility programs                       |
| docs          | MySQL manual in Info format                                      |
| man           | Unix manual pages                                                |
| include       | Include (header) files                                           |
| lib           | Libraries                                                        |
| share         | Error messages, dictionary, and SQL for database<br>installation |
| support-files | Miscellaneous support files                                      |

Debug versions of the mysqld binary are available as mysqld-debug. To compile your own debug version of MySQL from a source distribution, use the appropriate configuration options to enable debugging support. See Section 2.8, "Installing MySQL from Source".

To install and use a MySQL binary distribution, the command sequence looks like this:

```
$> groupadd mysql
$> useradd -r -g mysql -s /bin/false mysql
$> cd /usr/local
$> tar zxvf /path/to/mysql-VERSION-OS.tar.gz
$> ln -s full-path-to-mysql-VERSION-OS mysql
$> cd mysql
$> mkdir mysql-files
$> chown mysql:mysql mysql-files
$> chmod 750 mysql-files
$> bin/mysqld --initialize --user=mysql
$> bin/mysql_ssl_rsa_setup
$> bin/mysqld_safe --user=mysql &
# Next command is optional
$> cp support-files/mysql.server /etc/init.d/mysql.server
```

![](_page_104_Picture_8.jpeg)

#### **Note**

This procedure assumes that you have root (administrator) access to your system. Alternatively, you can prefix each command using the sudo (Linux) or pfexec (Solaris) command.

The mysql-files directory provides a convenient location to use as the value for the secure\_file\_priv system variable, which limits import and export operations to a specific directory. See Section 5.1.7, "Server System Variables".

A more detailed version of the preceding description for installing a binary distribution follows.

## **Create a mysql User and Group**

If your system does not already have a user and group to use for running mysqld, you may need to create them. The following commands add the mysql group and the mysql user. You might want to call the user and group something else instead of mysql. If so, substitute the appropriate name in the following instructions. The syntax for useradd and groupadd may differ slightly on different versions of Unix/Linux, or they may have different names such as adduser and addgroup.

```
$> groupadd mysql
$> useradd -r -g mysql -s /bin/false mysql
```

![](_page_105_Picture_3.jpeg)

#### **Note**

Because the user is required only for ownership purposes, not login purposes, the useradd command uses the -r and -s /bin/false options to create a user that does not have login permissions to your server host. Omit these options if your useradd does not support them.

## **Obtain and Unpack the Distribution**

Pick the directory under which you want to unpack the distribution and change location into it. The example here unpacks the distribution under /usr/local. The instructions, therefore, assume that you have permission to create files and directories in /usr/local. If that directory is protected, you must perform the installation as root.

```
$> cd /usr/local
```

Obtain a distribution file using the instructions in [Section 2.1.3, "How to Get MySQL"](#page-86-0). For a given release, binary distributions for all platforms are built from the same MySQL source distribution.

Unpack the distribution, which creates the installation directory. tar can uncompress and unpack the distribution if it has z option support:

```
$> tar zxvf /path/to/mysql-VERSION-OS.tar.gz
```

The tar command creates a directory named mysql-VERSION-OS.

To install MySQL from a compressed tar file binary distribution, your system must have GNU gunzip to uncompress the distribution and a reasonable tar to unpack it. If your tar program supports the z option, it can both uncompress and unpack the file.

GNU tar is known to work. The standard tar provided with some operating systems is not able to unpack the long file names in the MySQL distribution. You should download and install GNU tar, or if available, use a preinstalled version of GNU tar. Usually this is available as gnutar, gtar, or as tar within a GNU or Free Software directory, such as /usr/sfw/bin or /usr/local/bin. GNU tar is available from<http://www.gnu.org/software/tar/>.

If your tar does not have z option support, use gunzip to unpack the distribution and tar to unpack it. Replace the preceding tar command with the following alternative command to uncompress and extract the distribution:

```
$> gunzip < /path/to/mysql-VERSION-OS.tar.gz | tar xvf -
```

Next, create a symbolic link to the installation directory created by tar:

```
$> ln -s full-path-to-mysql-VERSION-OS mysql
```

The ln command makes a symbolic link to the installation directory. This enables you to refer more easily to it as /usr/local/mysql. To avoid having to type the path name of client programs always when you are working with MySQL, you can add the /usr/local/mysql/bin directory to your PATH variable:

```
$> export PATH=$PATH:/usr/local/mysql/bin
```

## **Perform Postinstallation Setup**

The remainder of the installation process involves setting distribution ownership and access permissions, initializing the data directory, starting the MySQL server, and setting up the configuration file. For instructions, see Section 2.9, "Postinstallation Setup and Testing".

## <span id="page-106-0"></span>**2.3 Installing MySQL on Microsoft Windows**

![](_page_106_Picture_2.jpeg)

### **Important**

MySQL Community 5.7 Server requires the Microsoft Visual C++ 2019 Redistributable Package to run on Windows platforms. Users should make sure the package has been installed on the system before installing the server. The package is available at the [Microsoft Download Center](http://www.microsoft.com/en-us/download/default.aspx).

This requirement changed over time: MySQL 5.7.37 and below requires the Microsoft Visual C++ 2013 Redistributable Package, MySQL 5.7.38 and 5.7.39 require both, and only the Microsoft Visual C++ 2019 Redistributable Package is required as of MySQL 5.7.40.

MySQL is available for Microsoft Windows, for both 32-bit and 64-bit versions. For supported Windows platform information, see <https://www.mysql.com/support/supportedplatforms/database.html>.

![](_page_106_Picture_7.jpeg)

#### **Important**

If your operating system is Windows 2008 R2 or Windows 7 and you do not have Service Pack 1 (SP1) installed, MySQL 5.7 regularly restarts with the following message in the MySQL server error log file:

mysqld got exception 0xc000001d

This error message occurs because you are also using a CPU that does not support the VPSRLQ instruction, indicating that the CPU instruction that was attempted is not supported.

To fix this error, you must install SP1. This adds the required operating system support for CPU capability detection and disables that support when the CPU does not have the required instructions.

Alternatively, install an older version of MySQL, such as 5.6.

There are different methods to install MySQL on Microsoft Windows.

## **MySQL Installer Method**

The simplest and recommended method is to download MySQL Installer (for Windows) and let it install and configure all of the MySQL products on your system. Here is how:

1. Download MySQL Installer from <https://dev.mysql.com/downloads/installer/> and execute it.

![](_page_106_Picture_18.jpeg)

#### **Note**

Unlike the standard MySQL Installer, the smaller "web-community" version does not bundle any MySQL applications but rather downloads the MySQL products you choose to install.

2. Choose the appropriate **Setup Type** for your system. Typically you should choose **Developer Default** to install MySQL server and other MySQL tools related to MySQL development, helpful tools like MySQL Workbench. Choose the **Custom** setup type instead to manually select your desired MySQL products.

![](_page_106_Picture_22.jpeg)

#### **Note**

Multiple versions of MySQL server can exist on a single system. You can choose one or multiple versions.

3. Complete the installation process by following the instructions. This installa several MySQL products and starts the MySQL server.

MySQL is now installed. If you configured MySQL as a service, then Windows automatically starts MySQL server every time you restart your system.

![](_page_107_Picture_2.jpeg)

#### **Note**

You probably also installed other helpful MySQL products like MySQL Workbench on your system. Consider loading Chapter 29, MySQL Workbench to check your new MySQL server connection By default, this program automatically starts after installing MySQL.

This process also installs the MySQL Installer application on your system, and later you can use MySQL Installer to upgrade or reconfigure your MySQL products.

## **Additional Installation Information**

It is possible to run MySQL as a standard application or as a Windows service. By using a service, you can monitor and control the operation of the server through the standard Windows service management tools. For more information, see [Section 2.3.4.8, "Starting MySQL as a Windows](#page-144-0) [Service".](#page-144-0)

Generally, you should install MySQL on Windows using an account that has administrator rights. Otherwise, you may encounter problems with certain operations such as editing the PATH environment variable or accessing the Service Control Manager. When installed, MySQL does not need to be executed using a user with Administrator privileges.

For a list of limitations on the use of MySQL on the Windows platform, see [Section 2.3.7, "Windows](#page-151-0) [Platform Restrictions".](#page-151-0)

In addition to the MySQL Server package, you may need or want additional components to use MySQL with your application or development environment. These include, but are not limited to:

• To connect to the MySQL server using ODBC, you must have a Connector/ODBC driver. For more information, including installation and configuration instructions, see [MySQL Connector/ODBC](https://dev.mysql.com/doc/connector-odbc/en/) [Developer Guide](https://dev.mysql.com/doc/connector-odbc/en/).

![](_page_107_Picture_12.jpeg)

#### **Note**

MySQL Installer installs and configures Connector/ODBC for you.

• To use MySQL server with .NET applications, you must have the Connector/NET driver. For more information, including installation and configuration instructions, see [MySQL Connector/NET](https://dev.mysql.com/doc/connector-net/en/) [Developer Guide](https://dev.mysql.com/doc/connector-net/en/).

![](_page_107_Picture_16.jpeg)

#### **Note**

MySQL Installer installs and configures MySQL Connector/NET for you.

MySQL distributions for Windows can be downloaded from<https://dev.mysql.com/downloads/>. See [Section 2.1.3, "How to Get MySQL".](#page-86-0)

MySQL for Windows is available in several distribution formats, detailed here. Generally speaking, you should use MySQL Installer. It contains more features and MySQL products than the older MSI, is simpler to use than the compressed file, and you need no additional tools to get MySQL up and running. MySQL Installer automatically installs MySQL Server and additional MySQL products, creates an options file, starts the server, and enables you to create default user accounts. For more information on choosing a package, see [Section 2.3.2, "Choosing an Installation Package"](#page-109-0).

• A MySQL Installer distribution includes MySQL Server and additional MySQL products, including MySQL Workbench. MySQL Installer can also be used to upgrade these products in the future.

For instructions on installing MySQL using MySQL Installer, see [Section 2.3.3, "MySQL Installer for](#page-110-0) [Windows".](#page-110-0)

• The standard binary distribution (packaged as a compressed file) contains all of the necessary files that you unpack into your chosen location. This package contains all of the files in the full Windows MSI Installer package, but does not include an installation program.

For instructions on installing MySQL using the compressed file, see [Section 2.3.4, "Installing MySQL](#page-139-0) [on Microsoft Windows Using a](#page-139-0) noinstall ZIP Archive".

• The source distribution format contains all the code and support files for building the executables using the Visual Studio compiler system.

For instructions on building MySQL from source on Windows, see Section 2.8, "Installing MySQL from Source".

## **MySQL on Windows Considerations**

• **Large Table Support**

If you need tables with a size larger than 4 GB, install MySQL on an NTFS or newer file system. Do not forget to use MAX\_ROWS and AVG\_ROW\_LENGTH when you create tables. See Section 13.1.18, "CREATE TABLE Statement".

![](_page_108_Picture_9.jpeg)

#### **Note**

InnoDB tablespace files cannot exceed 4 GB on Windows 32-bit systems.

#### • **MySQL and Virus Checking Software**

Virus-scanning software such as Norton/Symantec Anti-Virus on directories containing MySQL data and temporary tables can cause issues, both in terms of the performance of MySQL and the virusscanning software misidentifying the contents of the files as containing spam. This is due to the fingerprinting mechanism used by the virus-scanning software, and the way in which MySQL rapidly updates different files, which may be identified as a potential security risk.

After installing MySQL Server, it is recommended that you disable virus scanning on the main directory (datadir) used to store your MySQL table data. There is usually a system built into the virus-scanning software to enable specific directories to be ignored.

In addition, by default, MySQL creates temporary files in the standard Windows temporary directory. To prevent the temporary files also being scanned, configure a separate temporary directory for MySQL temporary files and add this directory to the virus scanning exclusion list. To do this, add a configuration option for the tmpdir parameter to your my.ini configuration file. For more information, see [Section 2.3.4.2, "Creating an Option File".](#page-140-0)

#### • **Running MySQL on a 4K Sector Hard Drive**

Running the MySQL server on a 4K sector hard drive on Windows is not supported with innodb\_flush\_method=async\_unbuffered, which is the default setting. The workaround is to use innodb\_flush\_method=normal.

## <span id="page-108-0"></span>**2.3.1 MySQL Installation Layout on Microsoft Windows**

For MySQL 5.7 on Windows, the default installation directory is C:\Program Files\MySQL\MySQL Server 5.7 for installations performed with MySQL Installer. If you use the ZIP archive method to install MySQL, you may prefer to install in C:\mysql. However, the layout of the subdirectories remains the same.

All of the files are located within this parent directory, using the structure shown in the following table.

**Table 2.4 Default MySQL Installation Layout for Microsoft Windows**

| Directory                                 | Contents of Directory                                                                                                                             | Notes                                                                                |
|-------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------|
| bin                                       | mysqld server, client and utility<br>programs                                                                                                     |                                                                                      |
| %PROGRAMDATA%\MySQL<br>\MySQL Server 5.7\ | Log files, databases                                                                                                                              | The Windows system variable<br>%PROGRAMDATA% defaults to C:<br>\ProgramData.         |
| docs                                      | Release documentation                                                                                                                             | With MySQL Installer, use the<br>Modify operation to select this<br>optional folder. |
| include                                   | Include (header) files                                                                                                                            |                                                                                      |
| lib                                       | Libraries                                                                                                                                         |                                                                                      |
| share                                     | Miscellaneous support files,<br>including error messages,<br>character set files, sample<br>configuration files, SQL for<br>database installation |                                                                                      |

## <span id="page-109-0"></span>**2.3.2 Choosing an Installation Package**

For MySQL 5.7, there are multiple installation package formats to choose from when installing MySQL on Windows. The package formats described in this section are:

- [MySQL Installer](#page-109-1)
- [MySQL noinstall ZIP Archives](#page-110-1)
- [MySQL Docker Images](#page-110-2)

Program Database (PDB) files (with file name extension pdb) provide information for debugging your MySQL installation in the event of a problem. These files are included in ZIP Archive distributions (but not MSI distributions) of MySQL.

### <span id="page-109-1"></span>**MySQL Installer**

This package has a file name similar to mysql-installer-community-5.7.44.0.msi or mysqlinstaller-commercial-5.7.44.0.msi, and uses MSIs to automatically install MySQL server and other products. MySQL Installer downloads and apply updates to itself, and for each of the installed products. It also configures the installed MySQL server (including a sandbox InnoDB cluster test setup) and MySQL Router. MySQL Installer is recommended for most users.

MySQL Installer can install and manage (add, modify, upgrade, and remove) many other MySQL products, including:

- Applications MySQL Workbench, MySQL for Visual Studio, MySQL Utilities, MySQL Shell, MySQL Router
- Connectors MySQL Connector/C++, MySQL Connector/NET, Connector/ODBC, MySQL Connector/Python, MySQL Connector/J, MySQL Connector/Node.js
- Documentation MySQL Manual (PDF format), samples and examples

MySQL Installer operates on all MySQL supported versions of Windows (see [https://www.mysql.com/](https://www.mysql.com/support/supportedplatforms/database.md) [support/supportedplatforms/database.html](https://www.mysql.com/support/supportedplatforms/database.md)).

![](_page_110_Picture_1.jpeg)

#### **Note**

Because MySQL Installer is not a native component of Microsoft Windows and depends on .NET, it does not work on installations with minimal options like the Server Core version of Windows Server.

For instructions on how to install MySQL using MySQL Installer, see [Section 2.3.3, "MySQL Installer for](#page-110-0) [Windows".](#page-110-0)

## <span id="page-110-1"></span>**MySQL noinstall ZIP Archives**

These packages contain the files found in the complete MySQL Server installation package, with the exception of the GUI. This format does not include an automated installer, and must be manually installed and configured.

The noinstall ZIP archives are split into two separate compressed files. The main package is named mysql-VERSION-winx64.zip for 64-bit and mysql-VERSION-win32.zip for 32-bit. This contains the components needed to use MySQL on your system. The optional MySQL test suite, MySQL benchmark suite, and debugging binaries/information components (including PDB files) are in a separate compressed file named mysql-VERSION-winx64-debug-test.zip for 64-bit and mysql-VERSION-win32-debug-test.zip for 32-bit.

If you choose to install a noinstall ZIP archive, see [Section 2.3.4, "Installing MySQL on Microsoft](#page-139-0) [Windows Using a](#page-139-0) noinstall ZIP Archive".

## <span id="page-110-2"></span>**MySQL Docker Images**

For information on using the MySQL Docker images provided by Oracle on Windows platform, see [Section 2.5.7.3, "Deploying MySQL on Windows and Other Non-Linux Platforms with Docker"](#page-189-1).

![](_page_110_Picture_11.jpeg)

#### **Warning**

The MySQL Docker images provided by Oracle are built specifically for Linux platforms. Other platforms are not supported, and users running the MySQL Docker images from Oracle on them are doing so at their own risk.

## <span id="page-110-0"></span>**2.3.3 MySQL Installer for Windows**

MySQL Installer is a standalone application designed to ease the complexity of installing and configuring MySQL products that run on Microsoft Windows. It is downloaded with and supports the following MySQL products:

• MySQL Servers

MySQL Installer can install and manage multiple, separate MySQL server instances on the same host at the same time. For example, MySQL Installer can install, configure, and upgrade separate instances of MySQL 5.7 and MySQL 8.0 on the same host. MySQL Installer does not permit server upgrades between major and minor version numbers, but does permit upgrades within a release series (such as 8.0.36 to 8.0.37).

![](_page_110_Picture_18.jpeg)

#### **Note**

MySQL Installer cannot install both Community and Commercial releases of MySQL server on the same host. If you require both releases on the same host, consider using the [ZIP archive](#page-110-1) distribution to install one of the releases.

• MySQL Applications

MySQL Workbench, MySQL Shell, and MySQL Router.

• MySQL Connectors

These are not supported, instead install from [https://dev.mysql.com/downloads/.](https://dev.mysql.com/downloads/) These connectors include MySQL Connector/NET, MySQL Connector/Python, MySQL Connector/ODBC, MySQL Connector/J, MySQL Connector/Node.js, and MySQL Connector/C++.

![](_page_111_Picture_2.jpeg)

#### **Note**

The connectors were bundled before MySQL Installer 1.6.7 (MySQL Server 8.0.34), and MySQL Installer could install each connector up to version 8.0.33 until MySQL Installer 1.6.11 (MySQL Server 8.0.37). MySQL Installer now only detects these old connector versions to uninstall them.

### **Installation Requirements**

MySQL Installer requires Microsoft .NET Framework 4.5.2 or later. If this version is not installed on the host computer, you can download it by visiting the [Microsoft website.](https://www.microsoft.com/en-us/download/details.aspx?id=42643)

To invoke MySQL Installer after a successful installation:

- 1. Right-click Windows Start, select **Run**, and then click **Browse**. Navigate to Program Files (x86) > MySQL > MySQL Installer for Windows to open the program folder.
- 2. Select one of the following files:
  - MySQLInstaller.exe to open the graphical application.
  - MySQLInstallerConsole.exe to open the command-line application.
- 3. Click **Open** and then click **OK** in the Run window. If you are prompted to allow the application to make changes to the device, select Yes.

Each time you invoke MySQL Installer, the initialization process looks for the presence of an internet connection and prompts you to enable offline mode if it finds no internet access (and offline mode is disabled). Select Yes to run MySQL Installer without internet-connection capabilities. MySQL product availability is limited to only those products currently in the product cache when you enable offline mode. To download MySQL products, click the offline mode **Disable** quick action shown on the dashboard.

An internet connection is required to download a manifest containing metadata for the latest MySQL products that are not part of a full bundle. MySQL Installer attempts to download the manifest when you start the application for the first time and then periodically in configurable intervals (see [MySQL](#page-126-0) [Installer options](#page-126-0)). Alternatively, you can retrieve an updated manifest manually by clicking **Catalog** in the [MySQL Installer dashboard.](#page-124-0)

![](_page_111_Picture_15.jpeg)

#### **Note**

If the first-time or subsequent manifest download is unsuccessful, an error is logged and you may have limited access to MySQL products during your session. MySQL Installer attempts to download the manifest with each startup until the initial manifest structure is updated. For help finding a product, see [Locating Products to Install](#page-127-0).

### **MySQL Installer Community Release**

Download software from <https://dev.mysql.com/downloads/installer/>to install the Community release of all MySQL products for Windows. Select one of the following MySQL Installer package options:

• Web: Contains MySQL Installer and configuration files only. The web package option downloads only the MySQL products you select to install, but it requires an internet connection for each download. The size of this file is approximately 2 MB. The file name has the form mysql-installercommunity-web-VERSION.N.msi in which VERSION is the MySQL server version number such as 8.0 and N is the package number, which begins at 0.

• Full or Current Bundle: Bundles all of the MySQL products for Windows (including the MySQL server). The file size is over 300 MB, and the name has the form mysql-installercommunity-VERSION.N.msi in which VERSION is the MySQL Server version number such as 8.0 and N is the package number, which begins at 0.

### <span id="page-112-1"></span>**MySQL Installer Commercial Release**

Download software from <https://edelivery.oracle.com/> to install the Commercial release (Standard or Enterprise Edition) of MySQL products for Windows. If you are logged in to your My Oracle Support (MOS) account, the Commercial release includes all of the current and previous GA versions available in the Community release, but it excludes development-milestone versions. When you are not logged in, you see only the list of bundled products that you downloaded already.

The Commercial release also includes the following products:

- Workbench SE/EE
- MySQL Enterprise Backup
- MySQL Enterprise Firewall

The Commercial release integrates with your MOS account. For knowledge-base content and patches, see [My Oracle Support](https://support.oracle.com/).

### <span id="page-112-2"></span>**2.3.3.1 MySQL Installer Initial Setup**

- [Choosing a Setup Type](#page-112-0)
- [Path Conflicts](#page-113-0)
- [Check Requirements](#page-114-0)
- [MySQL Installer Configuration Files](#page-115-0)

When you download MySQL Installer for the first time, a setup wizard guides you through the initial installation of MySQL products. As the following figure shows, the initial setup is a one-time activity in the overall process. MySQL Installer detects existing MySQL products installed on the host during its initial setup and adds them to the list of products to be managed.

**Figure 2.7 MySQL Installer Process Overview**

![](_page_112_Figure_16.jpeg)

MySQL Installer extracts configuration files (described later) to the hard drive of the host during the initial setup. Although MySQL Installer is a 32-bit application, it can install both 32-bit and 64-bit binaries.

The initial setup adds a link to the Start menu under the **MySQL** folder group. Click **Start**, **MySQL**, and **MySQL Installer - [Community | Commercial]** to open the community or commercial release of the graphical tool.

#### <span id="page-112-0"></span>**Choosing a Setup Type**

During the initial setup, you are prompted to select the MySQL products to be installed on the host. One alternative is to use a predetermined setup type that matches your setup requirements. By default, both GA and pre-release products are included in the download and installation with the **Client only**

and **Full** setup types. Select the **Only install GA products** option to restrict the product set to include GA products only when using these setup types.

![](_page_113_Picture_2.jpeg)

#### **Note**

Commercial-only MySQL products, such as MySQL Enterprise Backup, are available to select and install if you are using the Commercial version of MySQL Installer (see [MySQL Installer Commercial Release\)](#page-112-1).

Choosing one of the following setup types determines the initial installation only and does not limit your ability to install or update MySQL products for Windows later:

- **Server only**: Only install the MySQL server. This setup type installs the general availability (GA) or development release server that you selected when you downloaded MySQL Installer. It uses the default installation and data paths.
- **Client only**: Only install the most recent MySQL applications (such as MySQL Shell, MySQL Router, and MySQL Workbench). This setup type excludes MySQL server or the client programs typically bundled with the server, such as mysql or mysqladmin.
- **Full**: Install all available MySQL products, excluding MySQL connectors.
- **Custom**: The custom setup type enables you to filter and select individual MySQL products from the [MySQL Installer catalog](#page-124-1).

Use the Custom setup type to install:

- A product or product version that is not available from the usual download locations. The catalog contains all product releases, including the other releases between pre-release (or development) and GA.
- An instance of MySQL server using an alternative installation path, data path, or both. For instructions on how to adjust the paths, see [Section 2.3.3.2, "Setting Alternative Server Paths with](#page-115-1) [MySQL Installer"](#page-115-1).
- Two or more MySQL server versions on the same host at the same time (for example, 5.7 and 8.0).
- A specific combination of products and features not offered as a predetermine setup type. For example, you can install a single product, such as MySQL Workbench, instead of installing all client applications for Windows.

#### <span id="page-113-0"></span>**Path Conflicts**

When the default installation or data folder (required by MySQL server) for a product to be installed already exists on the host, the wizard displays the **Path Conflict** step to identify each conflict and enable you to take action to avoid having files in the existing folder overwritten by the new installation. You see this step in the initial setup only when MySQL Installer detects a conflict.

To resolve the path conflict, do one of the following:

- Select a product from the list to display the conflict options. A warning symbol indicates which path is in conflict. Use the browse button to choose a new path and then click **Next**.
- Click **Back** to choose a different setup type or product version, if applicable. The Custom setup type enables you to select individual product versions.
- Click **Next** to ignore the conflict and overwrite files in the existing folder.
- Delete the existing product. Click **Cancel** to stop the initial setup and close MySQL Installer. Open MySQL Installer again from the Start menu and delete the installed product from the host using the Delete operation from the [MySQL Installer dashboard.](#page-124-0)

#### <span id="page-114-0"></span>**Check Requirements**

MySQL Installer uses entries in the package-rules.xml file to determine whether the prerequisite software for each product is installed on the host. When the requirements check fails, MySQL Installer displays the **Check Requirements** step to help you update the host. Requirements are evaluated each time you download a new product (or version) for installation. The following figure identifies and describes the key areas of this step.

**Figure 2.8 Check Requirements**

![](_page_114_Figure_4.jpeg)

#### **Description of Check Requirements Elements**

- 1. Shows the current step in the initial setup. Steps in this list may change slightly depending on the products already installed on the host, the availability of prerequisite software, and the products to be installed on the host.
- 2. Lists all pending installation requirements by product and indicates the status as follows:
  - A blank space in the **Status** column means that MySQL Installer can attempt to download and install the required software for you.
  - The word Manual in the **Status** column means that you must satisfy the requirement manually. Select each product in the list to see its requirement details.
- 3. Describes the requirement in detail to assist you with each manual resolution. When possible, a download URL is provided. After you download and install the required software, click **Check** to verify that the requirement has been met.
- 4. Provides the following set operations to proceed:
  - **Back** Return to the previous step. This action enables you to select a different the setup type.
  - **Execute** Have MySQL Installer attempt to download and install the required software for all items without a manual status. Manual requirements are resolved by you and verified by clicking **Check**.
  - **Next** Do not execute the request to apply the requirements automatically and proceed to the installation without including the products that fail the check requirements step.
  - **Cancel** Stop the installation of MySQL products. Because MySQL Installer is already installed, the initial setup begins again when you open MySQL Installer from the Start menu and click **Add**

from the dashboard. For a description of the available management operations, see [Product](#page-124-1) [Catalog](#page-124-1).

#### <span id="page-115-0"></span>**MySQL Installer Configuration Files**

All MySQL Installer files are located within the C:\Program Files (x86) and C:\ProgramData folders. The following table describes the files and folders that define MySQL Installer as a standalone application.

![](_page_115_Picture_4.jpeg)

#### **Note**

Installed MySQL products are neither altered nor removed when you update or uninstall MySQL Installer.

**Table 2.5 MySQL Installer Configuration Files**

| File or Folder                 | Description                                                                                                                                                          | Folder Hierarchy                                                 |
|--------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------|
| MySQL Installer for<br>Windows | This folder contains all<br>of the files needed to<br>run MySQL Installer and<br>MySQLInstallerConsole.exe,<br>a command-line program with<br>similar functionality. | C:\Program Files (x86)                                           |
| Templates                      | The Templates folder has one<br>file for each version of MySQL<br>server. Template files contain<br>keys and formulas to calculate<br>some values dynamically.       | C:\ProgramData\MySQL<br>\MySQL Installer for<br>Windows\Manifest |
| package-rules.xml              | This file contains the<br>prerequisites for every product to<br>be installed.                                                                                        | C:\ProgramData\MySQL<br>\MySQL Installer for<br>Windows\Manifest |
| products.xml                   | The products file (or product<br>catalog) contains a list of all<br>products available for download.                                                                 | C:\ProgramData\MySQL<br>\MySQL Installer for<br>Windows\Manifest |
| Product Cache                  | The Product Cache folder<br>contains all standalone .msi<br>files bundled with the full<br>package or downloaded<br>afterward.                                       | C:\ProgramData\MySQL<br>\MySQL Installer for<br>Windows          |

### <span id="page-115-1"></span>**2.3.3.2 Setting Alternative Server Paths with MySQL Installer**

You can change the default installation path, the data path, or both when you install MySQL server. After you have installed the server, the paths cannot be altered without removing and reinstalling the server instance.

![](_page_115_Picture_11.jpeg)

### **Note**

Starting with MySQL Installer 1.4.39, if you move the data directory of an installed server manually, MySQL Installer identifies the change and can process a reconfiguration operation without errors.

#### **To change paths for MySQL server**

- 1. Identify the MySQL server to change and enable the **Advanced Options** link as follows:
  - a. Navigate to the **Select Products** page by doing one of the following:
    - i. If this is an [initial setup](#page-112-2) of MySQL Installer, select the Custom setup type and click **Next**.

- ii. If MySQL Installer is installed on your computer, click **Add** from the dashboard.
- b. Click **Edit** to apply a filter on the product list shown in **Available Products** (see [Locating](#page-127-0) [Products to Install](#page-127-0)).
- c. With the server instance selected, use the arrow to move the selected server to the **Products To Be Installed** list.
- d. Click the server to select it. When you select the server, the **Advanced Options** link is enabled below the list of products to be installed (see the following figure).
- 2. Click **Advanced Options** to open a dialog box where you can enter alternative path names. After the path names are validated, click **Next** to continue with the configuration steps.

**Figure 2.9 Change MySQL Server Path**

![](_page_116_Picture_7.jpeg)

## **2.3.3.3 Installation Workflows with MySQL Installer**

MySQL Installer provides a wizard-like tool to install and configure new MySQL products for Windows. Unlike the initial setup, which runs only once, MySQL Installer invokes the wizard each time you download or install a new product. For first-time installations, the steps of the initial setup proceed directly into the steps of the installation. For assistance with product selection, see [Locating Products to](#page-127-0) [Install](#page-127-0).

![](_page_116_Picture_10.jpeg)

#### **Note**

Full permissions are granted to the user executing MySQL Installer to all generated files, such as my.ini. This does not apply to files and directories for specific products, such as the MySQL server data directory in %ProgramData% that is owned by SYSTEM.

Products installed and configured on a host follow a general pattern that might require your input during the various steps. If you attempt to install a product that is incompatible with the existing MySQL server version (or a version selected for upgrade), you are alerted about the possible mismatch.

MySQL Installer provides the following sequence of actions that apply to different workflows:

• **Select Products.** If you selected the Custom setup type during the initial setup or clicked **Add** from the [MySQL Installer dashboard,](#page-124-0) MySQL Installer includes this action in the sidebar. From

this page, you can apply a filter to modify the Available Products list and then select one or more products to move (using arrow keys) to the Products To Be Installed list.

Select the check box on this page to activate the Select Features action where you can customize the products features after the product is downloaded.

• **Download.** If you installed the full (not web) MySQL Installer package, all .msi files were loaded to the Product Cache folder during the initial setup and are not downloaded again. Otherwise, click **Execute** to begin the download. The status of each product changes from Ready to Download, to Downloading, and then to Downloaded.

To retry a single unsuccessful download, click the **Try Again** link.

To retry all unsuccessful downloads, click **Try All**.

• **Select Features To Install (disabled by default).** After MySQL Installer downloads a product's .msi file, you can customize the features if you enabled the optional check box previously during the Select Products action.

To customize product features after the installation, click **Modify** in the [MySQL Installer dashboard](#page-124-0).

• **Installation.** The status of each product in the list changes from Ready to Install, to Installing, and lastly to Complete. During the process, click **Show Details** to view the installation actions.

If you cancel the installation at this point, the products are installed, but the server (if installed) is not yet configured. To restart the server configuration, open MySQL Installer from the Start menu and click **Reconfigure** next to the appropriate server in the dashboard.

• **Product configuration.** This step applies to MySQL Server, MySQL Router, and samples only. The status for each item in the list should indicate Ready to Configure. Click **Next** to start the configuration wizard for all items in the list. The configuration options presented during this step are specific to the version of database or router that you selected to install.

Click **Execute** to begin applying the configuration options or click **Back** (repeatedly) to return to each configuration page.

• **Installation complete.** This step finalizes the installation for products that do not require configuration. It enables you to copy the log to a clipboard and to start certain applications, such as MySQL Workbench and MySQL Shell. Click **Finish** to open the [MySQL Installer dashboard](#page-124-0).

### <span id="page-117-0"></span>**MySQL Server Configuration with MySQL Installer**

MySQL Installer performs the initial configuration of the MySQL server. For example:

- It creates the configuration file (my.ini) that is used to configure the MySQL server. The values written to this file are influenced by choices you make during the installation process. Some definitions are host dependent.
- By default, a Windows service for the MySQL server is added.
- Provides default installation and data paths for MySQL server. For instructions on how to change the default paths, see [Section 2.3.3.2, "Setting Alternative Server Paths with MySQL Installer".](#page-115-1)
- It can optionally create MySQL server user accounts with configurable permissions based on general roles, such as DB Administrator, DB Designer, and Backup Admin. It optionally creates a Windows user named MysqlSys with limited privileges, which would then run the MySQL Server.

User accounts may also be added and configured in MySQL Workbench.

• Checking **Show Advanced Options** enables additional **Logging Options** to be set. This includes defining custom file paths for the error log, general log, slow query log (including the configuration of seconds it requires to execute a query), and the binary log.

During the configuration process, click **Next** to proceed to the next step or **Back** to return to the previous step. Click **Execute** at the final step to apply the server configuration.

The sections that follow describe the server configuration options that apply to MySQL server on Windows. The server version you installed will determine which steps and options you can configure. Configuring MySQL server may include some or all of the steps.

#### **Type and Networking**

• Server Configuration Type

Choose the MySQL server configuration type that describes your setup. This setting defines the amount of system resources (memory) to assign to your MySQL server instance.

- **Development**: A computer that hosts many other applications, and typically this is your personal workstation. This setting configures MySQL to use the least amount of memory.
- **Server**: Several other applications are expected to run on this computer, such as a web server. The Server setting configures MySQL to use a medium amount of memory.
- **Dedicated**: A computer that is dedicated to running the MySQL server. Because no other major applications run on this server, this setting configures MySQL to use the majority of available memory.

#### • **Manual**

Prevents MySQL Installer from attempting to optimize the server installation, and instead, sets the default values to the server variables included in the my.ini configuration file. With the Manual type selected, MySQL Installer uses the default value of 16M for the tmp\_table\_size variable assignment.

• Connectivity

Connectivity options control how the connection to MySQL is made. Options include:

- **TCP/IP**: This option is selected by default. You may disable TCP/IP Networking to permit local host connections only. With the TCP/IP connection option selected, you can modify the following items:
  - **Port** for classic MySQL protocol connections. The default value is 3306.
  - **X Protocol Port** shown when configuring MySQL 8.0 server only. The default value is 33060
  - **Open Windows Firewall port for network access**, which is selected by default for TCP/IP connections.

If a port number is in use already, you will see the information icon ( ) next to the default value and **Next** is disabled until you provide a new port number.

• **Named Pipe**: Enable and define the pipe name, similar to setting the named\_pipe system variable. The default name is MySQL.

When you select **Named Pipe** connectivity, and then proceed to the next step, you are prompted to set the level of access control granted to client software on named-pipe connections. Some clients require only minimum access control for communication, while other clients require full access to the named pipe.

You can set the level of access control based on the Windows user (or users) running the client as follows:

• **Minimum access to all users (RECOMMENDED).** This level is enabled by default because it is the most secure.

- **Full access to members of a local group.** If the minimum-access option is too restrictive for the client software, use this option to reduce the number of users who have full access on the named pipe. The group must be established on Windows before you can select it from the list. Membership in this group should be limited and managed. Windows requires a newly added member to first log out and then log in again to join a local group.
- **Full access to all users (NOT RECOMMENDED).** This option is less secure and should be set only when other safeguards are implemented.
- **Shared Memory**: Enable and define the memory name, similar to setting the shared\_memory system variable. The default name is MySQL.
- Advanced Configuration

Check **Show Advanced and Logging Options** to set custom logging and advanced options in later steps. The Logging Options step enables you to define custom file paths for the error log, general log, slow query log (including the configuration of seconds it requires to execute a query), and the binary log. The Advanced Options step enables you to set the unique server ID required when binary logging is enabled in a replication topology.

• MySQL Enterprise Firewall (Enterprise Edition only)

The **Enable MySQL Enterprise Firewall** check box is deselected by default. Select this option to enable a security list that offers protection against certain types of attacks. Additional post-installation configuration is required (see Section 6.4.6, "MySQL Enterprise Firewall").

#### **Authentication Method**

The **Authentication Method** step is visible only during the installation or upgrade of MySQL 8.0.4 or higher. It introduces a choice between two server-side authentication options. The MySQL user accounts that you create in the next step will use the authentication method that you select in this step.

MySQL 8.0 connectors and community drivers that use libmysqlclient 8.0 now support the caching\_sha2\_password default authentication plugin. However, if you are unable to update your clients and applications to support this new authentication method, you can configure the MySQL server to use mysql\_native\_password for legacy authentication. For more information about the implications of this change, see [caching\\_sha2\\_password as the Preferred Authentication Plugin.](https://dev.mysql.com/doc/refman/8.0/en/upgrading-from-previous-series.md#upgrade-caching-sha2-password)

If you are installing or upgrading to MySQL 8.0.4 or higher, select one of the following authentication methods:

• Use Strong Password Encryption for Authentication (RECOMMENDED)

MySQL 8.0 supports a new authentication based on improved, stronger SHA256-based password methods. It is recommended that all new MySQL server installations use this method going forward.

![](_page_119_Picture_14.jpeg)

#### **Important**

The caching\_sha2\_password authentication plugin on the server requires new versions of connectors and clients, which add support for the new MySQL 8.0 default authentication.

• Use Legacy Authentication Method (Retain MySQL 5.x Compatibility)

Using the old MySQL 5.x legacy authentication method should be considered only in the following cases:

- Applications cannot be updated to use MySQL 8.0 connectors and drivers.
- Recompilation of an existing application is not feasible.

• An updated, language-specific connector or driver is not available yet.

### **Accounts and Roles**

• Root Account Password

Assigning a root password is required and you will be asked for it when performing other MySQL Installer operations. Password strength is evaluated when you repeat the password in the box provided. For descriptive information regarding password requirements or status, move your mouse

pointer over the information icon ( ) when it appears.

• MySQL User Accounts (Optional)

Click **Add User** or **Edit User** to create or modify MySQL user accounts with predefined roles. Next, enter the required account credentials:

- **User Name:** MySQL user names can be up to 32 characters long.
- **Host:** Select localhost for local connections only or <All Hosts (%)> when remote connections to the server are required.
- **Role:** Each predefined role, such as DB Admin, is configured with its own set of privileges. For example, the DB Admin role has more privileges than the DB Designer role. The **Role** dropdown list contains a description of each role.
- **Password:** Password strength assessment is performed while you type the password. Passwords must be confirmed. MySQL permits a blank or empty password (considered to be insecure).

**MySQL Installer Commercial Release Only:** MySQL Enterprise Edition for Windows, a commercial product, also supports an authentication method that performs external authentication on Windows. Accounts authenticated by the Windows operating system can access the MySQL server without providing an additional password.

To create a new MySQL account that uses Windows authentication, enter the user name and then select a value for **Host** and **Role**. Click **Windows** authentication to enable the authentication\_windows plugin. In the Windows Security Tokens area, enter a token for each Windows user (or group) who can authenticate with the MySQL user name. MySQL accounts can include security tokens for both local Windows users and Windows users that belong to a domain. Multiple security tokens are separated by the semicolon character (;) and use the following format for local and domain accounts:

• Local account

Enter the simple Windows user name as the security token for each local user or group; for example, **finley;jeffrey;admin**.

• Domain account

Use standard Windows syntax (domain\domainuser) or MySQL syntax (domain\ \domainuser) to enter Windows domain users and groups.

For domain accounts, you may need to use the credentials of an administrator within the domain if the account running MySQL Installer lacks the permissions to query the Active Directory. If this is the case, select **Validate Active Directory users with** to activate the domain administrator credentials.

Windows authentication permits you to test all of the security tokens each time you add or modify a token. Click **Test Security Tokens** to validate (or revalidate) each token. Invalid tokens generate a descriptive error message along with a red X icon and red token text. When all tokens resolve as valid (green text without an X icon), you can click **OK** to save the changes.

#### **Windows Service**

On the Windows platform, MySQL server can run as a named service managed by the operating system and be configured to start up automatically when Windows starts. Alternatively, you can configure MySQL server to run as an executable program that requires manual configuration.

• **Configure MySQL server as a Windows service** (Selected by default.)

When the default configuration option is selected, you can also select the following:

• **Start the MySQL Server at System Startup**

When selected (default), the service startup type is set to Automatic; otherwise, the startup type is set to Manual.

• **Run Windows Service as**

When **Standard System Account** is selected (default), the service logs on as Network Service.

The **Custom User** option must have privileges to log on to Microsoft Windows as a service. The **Next** button will be disabled until this user is configured with the required privileges.

A custom user account is configured in Windows by searching for "local security policy" in the Start menu. In the Local Security Policy window, select **Local Policies**, **User Rights Assignment**, and then **Log On As A Service** to open the property dialog. Click **Add User or Group** to add the custom user and then click **OK** in each dialog to save the changes.

• Deselect the Windows Service option.

### **Server File Permissions**

Optionally, permissions set on the folders and files located at C:\ProgramData\MySQL\MySQL Server 8.0\Data can be managed during the server configuration operation. You have the following options:

• MySQL Installer can configure the folders and files with full control granted exclusively to the user running the Windows service, if applicable, and to the Administrators group.

All other groups and users are denied access. This is the default option.

• Have MySQL Installer use a configuration option similar to the one just described, but also have MySQL Installer show which users could have full control.

You are then able to decide if a group or user should be given full control. If not, you can move the qualified members from this list to a second list that restricts all access.

• Have MySQL Installer skip making file-permission changes during the configuration operation.

If you select this option, you are responsible for securing the Data folder and its related files manually after the server configuration finishes.

#### **Logging Options**

This step is available if the **Show Advanced Configuration** check box was selected during the **Type and Networking** step. To enable this step now, click **Back** to return to the **Type and Networking** step and select the check box.

Advanced configuration options are related to the following MySQL log files:

• Error Log

- General Log
- Slow Query Log
- Bin Log

![](_page_122_Picture_4.jpeg)

#### **Note**

The binary log is enabled by default.

#### **Advanced Options**

This step is available if the **Show Advanced Configuration** check box was selected during the **Type and Networking** step. To enable this step now, click **Back** to return to the **Type and Networking** step and select the check box.

The advanced-configuration options include:

#### • **Server ID**

Set the unique identifier used in a replication topology. If binary logging is enabled, you must specify a server ID. The default ID value depends on the server version. For more information, see the description of the server\_id system variable.

#### • **Table Names Case**

You can set the following options during the initial and subsequent configuration the server. For the MySQL 8.0 release series, these options apply only to the initial configuration of the server.

• Lower Case

Sets the lower\_case\_table\_names option value to 1 (default), in which table names are stored in lowercase on disk and comparisons are not case-sensitive.

• Preserve Given Case

Sets the lower\_case\_table\_names option value to 2, in which table names are stored as given but compared in lowercase.

#### **Apply Server Configuration**

All configuration settings are applied to the MySQL server when you click **Execute**. Use the **Configuration Steps** tab to follow the progress of each action; the icon for each toggles from white to green (with a check mark) on success. Otherwise, the process stops and displays an error message if an individual action times out. Click the **Log** tab to view the log.

When the installation completes successfully and you click **Finish**, MySQL Installer and the installed MySQL products are added to the Microsoft Windows Start menu under the MySQL group. Opening MySQL Installer loads the [dashboard](#page-124-0) where installed MySQL products are listed and other MySQL Installer operations are available.

#### **MySQL Router Configuration with MySQL Installer**

During the [initial setup,](#page-112-2) choose any predetermined setup type, except Server only, to install the latest GA version of the tools. Use the Custom setup type to install an individual tool or specific version. If MySQL Installer is installed on the host already, use the **Add** operation to select and install tools from the MySQL Installer dashboard.

#### **MySQL Router Configuration**

MySQL Installer provides a configuration wizard that can bootstrap an installed instance of MySQL Router 8.0 to direct traffic between MySQL applications and an InnoDB Cluster. When configured, MySQL Router runs as a local Windows service.

![](_page_123_Picture_1.jpeg)

#### **Note**

You are prompted to configure MySQL Router after the initial installation and when you reconfigure an installed router explicitly. In contrast, the upgrade operation does not require or prompt you to configure the upgraded product.

To configure MySQL Router, do the following:

- 1. Set up InnoDB Cluster.
- 2. Using MySQL Installer, download and install the MySQL Router application. After the installation finishes, the configuration wizard prompts you for information. Select the **Configure MySQL Router for InnoDB Cluster** check box to begin the configuration and provide the following configuration values:
  - **Hostname:** Host name of the primary (seed) server in the InnoDB Cluster (localhost by default).
  - **Port:** The port number of the primary (seed) server in the InnoDB Cluster (3306 by default).
  - **Management User:** An administrative user with root-level privileges.
  - **Password:** The password for the management user.
  - **Classic MySQL protocol connections to InnoDB Cluster**

**Read/Write:** Set the first base port number to one that is unused (between 80 and 65532) and the wizard will select the remaining ports for you.

The figure that follows shows an example of the MySQL Router configuration page, with the first base port number specified as 6446 and the remaining ports set by the wizard to 6447, 6448, and 6449.

![](_page_123_Picture_14.jpeg)

**Figure 2.10 MySQL Router Configuration**

3. Click **Next** and then **Execute** to apply the configuration. Click **Finish** to close MySQL Installer or return to the [MySQL Installer dashboard.](#page-124-0)

After configuring MySQL Router, the root account exists in the user table as root@localhost (local) only, instead of root@% (remote). Regardless of where the router and client are located, even if both are located on the same host as the seed server, any connection that passes through the router is

viewed by server as being remote, not local. As a result, a connection made to the server using the local host (see the example that follows), does not authenticate.

\$> **\c root@localhost:6446**

### **2.3.3.4 MySQL Installer Product Catalog and Dashboard**

This section describes the MySQL Installer product catalog, the dashboard, and other actions related to product selection and upgrades.

- [Product Catalog](#page-124-1)
- [MySQL Installer Dashboard](#page-124-0)
- [Locating Products to Install](#page-127-0)
- [Upgrading MySQL Server](#page-128-0)
- [Removing MySQL Server](#page-129-0)
- [Upgrading MySQL Installer](#page-129-1)

### <span id="page-124-1"></span>**Product Catalog**

The product catalog stores the complete list of released MySQL products for Microsoft Windows that are available to download from [MySQL Downloads.](https://dev.mysql.com/downloads/) By default, and when an Internet connection is present, MySQL Installer attempts to update the catalog at startup every seven days. You can also update the catalog manually from the dashboard (described later).

An up-to-date catalog performs the following actions:

- Populates the **Available Products** pane of the Select Products page. This step appears when you select:
  - The Custom setup type during the [initial setup.](#page-112-2)
  - The **Add** operation from the dashboard.
- Identifies when product updates are available for the installed products listed in the dashboard.

The catalog includes all development releases (Pre-Release), general releases (Current GA), and minor releases (Other Releases). Products in the catalog will vary somewhat, depending on the MySQL Installer release that you download.

### <span id="page-124-0"></span>**MySQL Installer Dashboard**

The MySQL Installer dashboard is the default view that you see when you start MySQL Installer after the [initial setup](#page-112-2) finishes. If you closed MySQL Installer before the setup was finished, MySQL Installer resumes the initial setup before it displays the dashboard.

![](_page_124_Picture_21.jpeg)

### **Note**

Products covered under Oracle Lifetime Sustaining Support, if installed, may appear in the dashboard. These products, such as MySQL for Excel and MySQL Notifier, can be modified or removed only.

![](_page_125_Figure_1.jpeg)

**Figure 2.11 MySQL Installer Dashboard Elements**

#### **Description of MySQL Installer Dashboard Elements**

- 1. MySQL Installer dashboard operations provide a variety of actions that apply to installed products or products listed in the catalog. To initiate the following operations, first click the operation link and then select the product or products to manage:
  - **Add**: This operation opens the Select Products page. From there you can adjust the filter, select one or more products to download (as needed), and begin the installation. For hints about using the filter, see [Locating Products to Install](#page-127-0).

Use the directional arrows to move each product from the **Available Products** column to the **Products To Be Installed** column. To enable the Product Features page where you can customize features, click the related check box (disabled by default).

- **Modify**: Use this operation to add or remove the features associated with installed products. Features that you can modify vary in complexity by product. When the **Program Shortcut** check box is selected, the product appears in the Start menu under the MySQL group.
- **Upgrade**: This operation loads the Select Products to Upgrade page and populates it with all the upgrade candidates. An installed product can have more than one upgrade version and the operation requires a current product catalog. MySQL Installer upgrades all of the selected products in one action. Click **Show Details** to view the actions performed by MySQL Installer.
- **Remove**: This operation opens the Remove Products page and populates it with the MySQL products installed on the host. Select the MySQL products you want to remove (uninstall) and then click **Execute** to begin the removal process. During the operation, an indicator shows the number of steps that are executed as a percentage of all steps.

To select products to remove, do one of the following:

- Select the check box for one or more products.
- Select the **Product** check box to select all products.
- 2. The **Reconfigure** link in the Quick Action column next to each installed server loads the current configuration values for the server and then cycles through all configuration steps enabling you to change the options and values. You must provide credentials with root privileges to reconfigure

these items. Click the **Log** tab to show the output of each configuration step performed by MySQL Installer.

On completion, MySQL Installer stops the server, applies the configuration changes, and restarts the server for you. For a description of each configuration option, see [MySQL Server Configuration](#page-117-0) [with MySQL Installer.](#page-117-0) Installed Samples and Examples associated with a specific MySQL server version can be also be reconfigured to apply new feature settings, if any.

3. The **Catalog** link enables you to download the latest catalog of MySQL products manually and then to integrate those product changes with MySQL Installer. The catalog-download action does not perform an upgrade of the products already installed on the host. Instead, it returns to the dashboard and adds an arrow icon to the Version column for each installed product that has a newer version. Use the **Upgrade** operation to install the newer product version.

You can also use the **Catalog** link to display the current change history of each product without downloading the new catalog. Select the **Do not update at this time** check box to view the change history only.

4. The MySQL Installer About icon ( ) shows the current version of MySQL Installer and general information about MySQL. The version number is located above the **Back** button.

![](_page_126_Picture_6.jpeg)

#### **Tip**

Always include this version number when reporting a problem with MySQL Installer.

In addition to the About MySQL information ( ), you can also select the following icons from the side panel:

• License icon ( ) for MySQL Installer.

This product may include third-party software, used under license. If you are using a Commercial release of MySQL Installer, the icon opens the MySQL Installer Commercial License Information User Manual for licensing information, including licensing information relating to third-party software that may be included in this Commercial release. If you are using a Community release of MySQL Installer, the icon opens the MySQL Installer Community License Information User Manual for licensing information, including licensing information relating to third-party software that may be included in this Community release.

- Resource links icon ( ) to the latest MySQL product documentation, blogs, webinars, and more.
- <span id="page-126-0"></span>5. The MySQL Installer Options icon ( ) includes the following tabs:
  - **General**: Enables or disables the Offline mode option. If selected, this option configures MySQL Installer to run without depending on internet-connection capabilities. When running MySQL Installer in offline mode, you see a warning together with a **Disable** quick action on the dashboard. The warning serves to remind you that running MySQL Installer in offline mode prevents you from downloading the latest MySQL products and product catalog updates. Offline mode persists until you disable the option.

At startup, MySQL Installer determines whether an internet connection is present, and, if not, prompts you to enable offline mode to resume working without a connection.

• **Product Catalog**: Manages the automatic catalog updates. By default, MySQL Installer checks for catalog updates at startup every seven days. When new products or product versions are

available, MySQL Installer adds them to the catalog and then inserts an arrow icon ( ) next to the version number of installed products listed in the dashboard.

![](_page_127_Picture_2.jpeg)

Use the product catalog option to enable or disable automatic updates and to reset the number of days between automatic catalog downloads. At startup, MySQL Installer uses the number of days you set to determine whether a download should be attempted. This action is repeated during next startup if MySQL Installer encounters an error downloading the catalog.

- **Connectivity Settings**: Several operations performed by MySQL Installer require internet access. This option enables you to use a default value to validate the connection or to use a different URL, one selected from a list or added by you manually. With the **Manual** option selected, new URLs can be added and all URLs in the list can be moved or deleted. When the **Automatic** option is selected, MySQL Installer attempts to connect to each default URL in the list (in order) until a connection is made. If no connection can be made, it raises an error.
- **Proxy**: MySQL Installer provides multiple proxy modes that enable you to download MySQL products, updates, or even the product catalog in most network environments. The mode are:

#### • **No proxy**

Select this mode to prevent MySQL Installer from looking for system settings. This mode disables any proxy settings.

#### • **Automatic**

Select this mode to have MySQL Installer look for system settings and to use those settings if found, or to use no proxy if nothing is found. This mode is the default.

#### • **Manual**

Select this mode to have MySQL Installer use your authentication details to configuration proxy access to the internet. Specifically:

- A proxy-server address (http://address-to-server) and port number
- A user name and password for authentication

#### <span id="page-127-0"></span>**Locating Products to Install**

MySQL products in the catalog are listed by category: MySQL Servers, Applications, MySQL Connectors, and Documentation. Only the latest GA versions appear in the **Available Products** pane by default. If you are looking for a pre-release or older version of a product, it may not be visible in the default list.

![](_page_127_Picture_16.jpeg)

#### **Note**

Keep the product catalog up-to-date. Click **Catalog** on the MySQL Installer dashboard to download the latest manifest.

To change the default product list, click **Add** in the dashboard to open the Select Products page, and then click **Edit** to open the dialog box shown in the figure that follows. Modify the settings and then click **Filter**.

**Figure 2.12 Filter Available Products**

![](_page_128_Picture_2.jpeg)

Reset one or more of the following fields to modify the list of available products:

- Text: Filter by text.
- Category: All Software (default), MySQL Servers, Applications, MySQL Connectors, or Documentation (for samples and documentation).
- Maturity: Current Bundle (appears initially with the full package only), Pre-Release, Current GA, or Other Releases. If you see a warning, confirm that you have the most recent product manifest by clicking **Catalog** on the MySQL Installer dashboard. If MySQL Installer is unable to download the manifest, the range of products you see is limited to bundled products, standalone product MSIs located in the Product Cache folder already, or both.

![](_page_128_Picture_7.jpeg)

#### **Note**

The Commercial release of MySQL Installer does not display any MySQL products when you select the Pre-Release maturity filter. Products in development are available from the Community release of MySQL Installer only.

- Already Downloaded (the check box is deselected by default). Permits you to view and manage downloaded products only.
- Architecture: Any (default), 32-bit, or 64-bit.

#### <span id="page-128-0"></span>**Upgrading MySQL Server**

Important server upgrade conditions:

- MySQL Installer does not permit server upgrades between major release versions or minor release versions, but does permit upgrades within a release series, such as an upgrade from 8.0.36 to 8.0.37.
- Upgrades between milestone releases (or from a milestone release to a GA release) are not supported. Significant development changes take place in milestone releases and you may encounter compatibility issues or problems starting the server.
- For upgrades, a check box enables you to skip the upgrade check and process for system tables, while checking and processing data dictionary tables normally. MySQL Installer does not prompt you with the check box when the previous server upgrade was skipped or when the server was configured as a sandbox InnoDB Cluster. This behavior represents a change in how MySQL Server performs an upgrade (see [What the MySQL Upgrade Process Upgrades](https://dev.mysql.com/doc/refman/8.0/en/upgrading-what-is-upgraded.md)) and it alters the sequence of steps that MySQL Installer applies to the configuration process.

If you select **Skip system tables upgrade check and process. (Not recommended)**, MySQL Installer starts the upgraded server with the [--upgrade=MINIMAL](https://dev.mysql.com/doc/refman/8.0/en/server-options.md#option_mysqld_upgrade) server option, which upgrades the data dictionary only. If you stop and then restart the server without the [--upgrade=MINIMAL](https://dev.mysql.com/doc/refman/8.0/en/server-options.md#option_mysqld_upgrade) option, the server upgrades the system tables automatically, if needed.

The following information appears in the **Log** tab and log file after the upgrade configuration (with system tables skipped) is complete:

WARNING: The system tables upgrade was skipped after upgrading MySQL Server. The server will be started now with the --upgrade=MINIMAL option, but then each time the server is started it will attempt to upgrade the system tables, unless you modify the Windows service (command line) to add --upgrade=MINIMAL to bypass the upgrade.

FOR THE BEST RESULTS: Run mysqld.exe --upgrade=FORCE on the command line to upgrade the system tables manually.

#### To choose a new server version:

1. Click **Upgrade**. Confirm that the check box next to product name in the **Upgradeable Products** pane has a check mark. Deselect the products that you do not intend to upgrade at this time.

![](_page_129_Picture_6.jpeg)

#### **Note**

For server milestone releases in the same release series, MySQL Installer deselects the server upgrade and displays a warning to indicate that the upgrade is not supported, identifies the risks of continuing, and provides a summary of the steps to perform a logical upgrade manually. You can reselect server upgrade at your own risk. For instructions on how to perform a logical upgrade with a milestone release, see Logical Upgrade.

2. Click a product in the list to highlight it. This action populates the **Upgradeable Versions** pane with the details of each available version for the selected product: version number, published date, and a Changes link to open the release notes for that version.

#### <span id="page-129-0"></span>**Removing MySQL Server**

To remove a local MySQL server:

- 1. Determine whether the local data directory should be removed. If you retain the data directory, another server installation can reuse the data. This option is enabled by default (removes the data directory).
- 2. Click **Execute** to begin uninstalling the local server. Note that all products that you selected to remove are also uninstalled at this time.
- 3. (Optional) Click the **Log** tab to display the current actions performed by MySQL Installer.

### <span id="page-129-1"></span>**Upgrading MySQL Installer**

MySQL Installer remains installed on your computer, and like other software, MySQL Installer can be upgraded from the previous version. In some cases, other MySQL software may require that you upgrade MySQL Installer for compatibility. This section describes how to identify the current version of MySQL Installer and how to upgrade MySQL Installer manually.

#### **To locate the installed version of MySQL Installer:**

- 1. Start MySQL Installer from the search menu. The MySQL Installer dashboard opens.
- 2. Click the MySQL Installer About icon ( ). The version number is located above the **Back** button.

#### **To initiate an on-demand upgrade of MySQL Installer:**

- 1. Connect the computer with MySQL Installer installed to the internet.
- 2. Start MySQL Installer from the search menu. The MySQL Installer dashboard opens.
- 3. Click **Catalog** on the bottom of the dashboard to open the Update Catalog window.

- 4. Click **Execute** to begin the process. If the installed version of MySQL Installer can be upgraded, you will be prompted to start the upgrade.
- 5. Click **Next** to review all changes to the catalog and then click **Finish** to return to the dashboard.
- 6. Verify the (new) installed version of MySQL Installer (see the previous procedure).

### <span id="page-130-0"></span>**2.3.3.5 MySQL Installer Console Reference**

[MySQLInstallerConsole.exe](#page-130-0) provides command-line functionality that is similar to MySQL Installer. This reference includes:

- [MySQL Product Names](#page-131-0)
- [Command Syntax](#page-131-1)
- [Command Actions](#page-132-0)

The console is installed when MySQL Installer is initially executed and then available within the MySQL Installer for Windows directory. By default, the directory location is C:\Program Files (x86)\MySQL\MySQL Installer for Windows. You must run the console as administrator.

#### To use the console:

- 1. Open a command prompt with administrative privileges by selecting **Windows System** from **Start**, then right-click **Command Prompt**, select **More**, and select **Run as administrator**.
- 2. From the command line, optionally change the directory to where the [MySQLInstallerConsole.exe](#page-130-0) command is located. For example, to use the default installation location:

```
cd Program Files (x86)\MySQL\MySQL Installer for Windows
```

3. Type MySQLInstallerConsole.exe (or mysqlinstallerconsole) followed by a command action to perform a task. For example, to show the console's help:

```
MySQLInstallerConsole.exe --help
=================== Start Initialization ===================
MySQL Installer is running in Community mode
Attempting to update manifest.
Initializing product requirements.
Loading product catalog.
Checking for product packages in the bundle.
Categorizing product catalog.
Finding all installed packages.
Your product catalog was last updated at 23/08/2022 12:41:05 p. m.
Your product catalog has version number 671.
=================== End Initialization ===================
The following actions are available:
Configure - Configures one or more of your installed programs.
Help - Provides list of available command actions.
Install - Installs and configures one or more available MySQL programs.
List - Lists all available MySQL products.
Modify - Modifies the features of installed products.
Remove - Removes one or more products from your system.
Set - Configures the general options of MySQL Installer.
Status - Shows the status of all installed products.
Update - Updates the current product catalog.
Upgrade - Upgrades one or more of your installed programs.
The basic syntax for using MySQL Installer command actions. Brackets denote optional entities. 
Curly braces denote a list of possible entities.
...
```

#### <span id="page-131-0"></span>**MySQL Product Names**

Many of the [MySQLInstallerConsole](#page-130-0) command actions accept one or more abbreviated phrases that can match a MySQL product (or products) in the catalog. The current set of valid short phrases for use with commands is shown in the following table.

![](_page_131_Picture_3.jpeg)

#### **Note**

Starting with MySQL Installer 1.6.7 (8.0.34), the install, list, and upgrade command options no longer apply to MySQL for Visual Studio (now EOL), MySQL Connector/NET, MySQL Connector/ODBC, MySQL Connector/C++, MySQL Connector/Python, and MySQL Connector/J. To install newer MySQL connectors, visit https://dev.mysql.com/downloads/.

**Table 2.6 MySQL Product Phrases for use with the MySQLInstallerConsole.exe command**

<span id="page-131-2"></span>

| Phrase        | MySQL Product                                                |
|---------------|--------------------------------------------------------------|
| server        | MySQL Server                                                 |
| workbench     | MySQL Workbench                                              |
| shell         | MySQL Shell                                                  |
| visual        | MySQL for Visual Studio                                      |
| router        | MySQL Router                                                 |
| backup        | MySQL Enterprise Backup (requires the<br>commercial release) |
| net           | MySQL Connector/NET                                          |
| odbc          | MySQL Connector/ODBC                                         |
| c++           | MySQL Connector/C++                                          |
| python        | MySQL Connector/Python                                       |
| j             | MySQL Connector/J                                            |
| documentation | MySQL Server Documentation                                   |
| samples       | MySQL Samples (sakila and world databases)                   |

#### <span id="page-131-1"></span>**Command Syntax**

The [MySQLInstallerConsole.exe](#page-130-0) command can be issued with or without the file extension (.exe) and the command is not case-sensitive.

mysqlinstallerconsole[.exe] [[[--]action] [action\_blocks\_list] [options\_list]]

#### Description:

action One of the permitted operational actions. If omitted, the default action is equivalent to the --status action. Using the -- prefix is optional for all actions.

> Possible actions are: [--]configure, [--]help, [--]install, [--]list, [--]modify, [--]remove, [--]set, [--]status, [--]update, and [--]upgrade.

action\_blocks\_list A list of blocks in which each represents a different item depending on the selected action. Blocks are separated by commas.

> The --remove and --upgrade actions permit specifying an asterisk character (\*) to indicate all products. If the \* character is detected at the start of this block, it is assumed all products are to be processed and the remainder of the block is ignored.

Syntax: \*|action\_block[,action\_block] [,action\_block]...

action\_block: Contains a product selector followed by an indefinite number of argument blocks that behave differently depending on the selected action (see [Command Actions](#page-132-0)).

options\_list Zero or more options with possible values separated by spaces. See [Command Actions](#page-132-0) to identify the options permitted for the corresponding action.

> Syntax: option\_value\_pair[ option\_value\_pair][ option\_value\_pair]...

option\_value\_pair: A single option (for example, --silent) or a tuple of a key and a corresponding value with an options prefix. The key-value pair is in the form of --key[=value].

## <span id="page-132-0"></span>**Command Actions**

[MySQLInstallerConsole.exe](#page-130-0) supports the following command actions:

![](_page_132_Picture_9.jpeg)

#### **Note**

Configuration block (or arguments\_block) values that contain a colon character (:) must be wrapped in quotation marks. For example, install\_dir="C: \MySQL\MySQL Server 8.0".

• [--]configure [product1]:[configuration\_argument]=[value], [product2]: [configuration\_argument]=[value], [...]

Configures one or more MySQL products on your system. Multiple configuration\_argument=value pairs can be configured for each product.

#### Options:

| continue      | Continues processing the next product when an error is caught<br>while processing the action blocks containing arguments for each<br>product. If not specified the whole operation is aborted in case of<br>an error. |
|---------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| help          | Shows the options and available arguments for the corresponding<br>action. If present the action is not executed, only the help is<br>shown, so other action-related options are ignored as well.                     |
| show-settings | Displays the available options for the selected product by passing<br>in the product name aftershow-settings.                                                                                                         |
| silent        | Disables confirmation prompts.                                                                                                                                                                                        |
|               |                                                                                                                                                                                                                       |

#### Examples:

```
MySQLInstallerConsole --configure --show-settings server
mysqlinstallerconsole.exe --configure server:port=3307
```

• [--]help

Displays a help message with usage examples and then exits. Pass in an additional command action to receive help specific to that action.

#### Options:

--action=[action] Shows the help for a specific action. Same as using the --help option with an action.

> Permitted values are: all, configure, help (default), install, list, modify, remove, status, update, upgrade, and set.

--help Shows the options and available arguments for the corresponding action. If present the action is not executed, only the help is shown, so other action-related options are ignored as well.

#### Examples:

MySQLInstallerConsole help

MySQLInstallerConsole help --action=install

• [--]install [product1]:[features]:[config block]:[config block], [product2]:[config block], [...]

Installs one or more MySQL products on your system. If pre-release products are available, both GA and pre-release products are installed when the value of the --type option value is Client or Full. Use the --only\_ga\_products option to restrict the product set to GA products only when using these setup types.

#### Description:

[product] Each product can be specified by a [product phrase](#page-131-2) with or without a semicolon-separated version qualifier. Passing in a product keyword alone selects the latest version of the product. If multiple architectures are available for that version of the product, the command returns the first one in the manifest list for interactive confirmation. Alternatively, you can pass in the exact version and architecture (x86 or x64) after the product keyword using the - silent option.

[features] All features associated with a MySQL product are installed by default. The feature block is a semicolon-separated list of features or an asterisk character (\*) that selects all features. To remove a feature, use the modify command.

[config block] One or more configuration blocks can be specified. Each configuration block is a semicolon-separated list of key-value pairs. A block can include either a config or user type key; config is the default type if one is not defined.

> Configuration block values that contain a colon character (:) must be wrapped in quotation marks. For example, installdir="C: \MySQL\MySQL Server 8.0". Only one configuration type

block can be defined for each product. A user block should be defined for each user to be created during the product installation.

![](_page_134_Picture_2.jpeg)

#### **Note**

The user type key is not supported when a product is being reconfigured.

#### Options:

--auto-handle-prereqs If present, MySQL Installer attempts to download and install some software prerequisites, not currently present. that can be resolved with minimal intervention. If the --silent option is not present, you are presented with installation pages for each prerequisite. If the --auto-handle-prereqs options is omitted, packages with missing prerequisites are not installed.

--continue Continues processing the next product when an error is caught while processing the action blocks containing arguments for each product. If not specified the whole operation is aborted in case of an error.

--help Shows the options and available arguments for the corresponding action. If present the action is not executed, only the help is shown, so other action-related options are ignored as well.

--mos-password=password Sets the My Oracle Support (MOS) user's password for commercial versions of the MySQL Installer.

--mos-user=user\_name Specifies the My Oracle Support (MOS) user name for access to the commercial version of MySQL Installer. If not present, only the products in the bundle, if any, are available to be installed.

--only-ga-products Restricts the product set to include GA products only.

--setup-type=setup\_type Installs a predefined set of software. The setup type can be one of the following:

- Server: Installs a single MySQL server
- Client: Installs client programs and libraries (excludes MySQL connectors)
- Full: Installs everything (excludes MySQL connectors)
- Custom: Installs user-selected products. This is the default option.

![](_page_135_Picture_9.jpeg)

#### **Note**

Non-custom setup types are valid only when no other MySQL products are installed.

--show-settings Displays the available options for the selected product, by passing in the product name after -showsettings.

--silent Disable confirmation prompts.

#### Examples:

mysqlinstallerconsole.exe --install j;8.0.29, net;8.0.28 --silent

MySQLInstallerConsole install server;8.0.30:\*:port=3307;server\_id=2:type=user;user=foo

An example that passes in additional configuration blocks, separated by ^ to fit:

MySQLInstallerConsole --install server;8.0.30;x64:\*:type=config;open\_win\_firewall=true; ^ general\_log=true;bin\_log=true;server\_id=3306;tcp\_ip=true;port=3306;root\_passwd=pass; ^ install\_dir="C:\MySQL\MySQL Server 8.0":type=user;user\_name=foo;password=bar;role=DBManager • [--]list

When this action is used without options, it activates an interactive list from which all of the available MySQL products can be searched. Enter MySQLInstallerConsole --list and specify a substring to search.

#### Options:

--all Lists all available products. If this option is used, all other options are ignored. --arch=architecture Lists that contain the specified architecture. Permitted values are: x86, x64, and any (default). This option can be combined with the --name and --version options. --help Shows the options and available arguments for the corresponding action. If present the action is not executed, only the help is shown, so other action-related options are ignored as well. --name=package\_name Lists products that contain the specified name (see [product](#page-131-2) [phrase\)](#page-131-2), This option can be combined with the --version and --arch options. --version=version Lists products that contain the specified version, such as 8.0 or 5.7. This option can be combined with the --name and --arch

#### Examples:

MySQLInstallerConsole --list --name=net --version=8.0

• [--]modify [product1:-removelist|+addlist], [product2:-removelist| +addlist] [...]

options.

Modifies or displays features of a previously installed MySQL product. To display the features of a product, append the product keyword to the command, for example:

MySQLInstallerConsole --modify server

### Options:

--help Shows the options and available arguments for the corresponding

action. If present the action is not executed, only the help is shown, so other action-related options are ignored as well.

--silent Disable confirmation prompts.

#### Examples:

MySQLInstallerConsole --modify server:+documentation

MySQLInstallerConsole modify server:-debug

• [--]remove [product1], [product2] [...]

Removes one ore more products from your system. An asterisk character (\*) can be passed in to remove all MySQL products with one command.

#### Options:

--continue Continue the operation even if an error occurs. --help Shows the options and available arguments for the corresponding action. If present the action is not executed, only the help is shown, so other action-related options are ignored as well. --keep-datadir Skips the removal of the data directory when removing MySQL Server products. --silent Disable confirmation prompts.

#### Examples:

mysqlinstallerconsole.exe remove \* MySQLInstallerConsole --remove server --continue

• [--]set

Sets one or more configurable options that affect how the MySQL Installer program connects to the internet and whether the automatic products-catalog updates feature is activated.

#### Options:

--catalogupdate=bool\_value Enables (true, default) or disables (false) the automatic products catalog update. This option requires an active connection to the internet. --catalog-updatedays=int\_value Accepts an integer between 1 (default) and 365 to indicate the number of days between checks for a new catalog update when MySQL Installer is started. If --catalog-update is false, this option is ignored. --connectionvalidation=validation\_type Sets how MySQL Installer performs the check for an internet connection. Permitted values are automatic (default) and manual. --connection-validationurls=url\_list A double-quote enclosed and comma-separated string that defines the list of URLs to use for checking the internet connection when --connection-validation is set to

manual. Checks are made in the same order provided. If the first URL fails, the next URL in the list is used and so on.

--offlinemode=bool\_value Enables MySQL Installer to run with or without internet capabilities. Valid modes are:

- True to enable offline mode (run without an internet connection).
- False (default) to disable offline mode (run with an internet connection). Set this mode before downloading the product catalog or any products to install.

--proxy-mode Specifies the proxy mode. Valid modes are:

- Automatic to automatically identify the proxy based on the system settings.
- None to ensure that no proxy is configured.
- Manual to set the proxy details manually (--proxy-server, --proxy-port, --proxy-username, --proxy-password).

--proxy-password The password used to authenticate to the proxy server.

--proxy-port The port used for the proxy server.

--proxy-server The URL that point to the proxy server.

--proxy-username The user name used to authenticate to the proxy server.

--reset-defaults Resets the MySQL Installer options associated with the --set action to the default values.

#### Examples:

MySQLIntallerConsole.exe set --reset-defaults

mysqlintallerconsole.exe --set --catalog-update=false

MySQLIntallerConsole --set --catalog-update-days=3

mysqlintallerconsole --set --connection-validation=manual --connection-validation-urls="https://www.bing.com,http://www.google.com"

• [--]status

Provides a quick overview of the MySQL products that are installed on the system. Information includes product name and version, architecture, date installed, and install location.

#### Options:

--help Shows the options and available arguments for the corresponding action. If present the action is not executed, only the help is shown, so other action-related options are ignored as well.

#### Examples:

MySQLInstallerConsole status

• [--]update

Downloads the latest MySQL product catalog to your system. On success, the catalog is applied the next time either MySQLInstaller or [MySQLInstallerConsole.exe](#page-130-0) is executed.

MySQL Installer automatically checks for product catalog updates when it is started if n days have passed since the last check. Starting with MySQL Installer 1.6.4, the default value is 1 day. Previously, the default value was 7 days.

#### Options:

--help Shows the options and available arguments for the corresponding

action. If present the action is not executed, only the help is shown, so other action-related options are ignored as well.

#### Examples:

MySQLInstallerConsole update

• [--]upgrade [product1:version], [product2:version] [...]

Upgrades one or more products on your system. The following characters are permitted for this action:

\* Pass in \* to upgrade all products to the latest version, or pass in

specific products.

! Pass in ! as a version number to upgrade the MySQL product to

its latest version.

#### Options:

--continue Continue the operation even if an error occurs.

--help Shows the options and available arguments for the corresponding

action. If present the action is not executed, only the help is shown, so other action-related options are ignored as well.

--mos-password=password Sets the My Oracle Support (MOS) user's password for

commercial versions of the MySQL Installer.

--mos-user=user\_name Specifies the My Oracle Support (MOS) user name for access to

the commercial version of MySQL Installer. If not present, only the

products in the bundle, if any, are available to be installed.

--silent Disable confirmation prompts.

#### Examples:

MySQLInstallerConsole upgrade \*

MySQLInstallerConsole upgrade workbench:8.0.31

MySQLInstallerConsole upgrade workbench:!

MySQLInstallerConsole --upgrade server;8.0.30:!, j;8.0.29:!

## <span id="page-139-0"></span>**2.3.4 Installing MySQL on Microsoft Windows Using a noinstall ZIP Archive**

Users who are installing from the noinstall package can use the instructions in this section to manually install MySQL. The process for installing MySQL from a ZIP Archive package is as follows: 1. Extract the main archive to the desired install directory

Optional: also extract the debug-test archive if you plan to execute the MySQL benchmark and test suite

- 2. Create an option file
- 3. Choose a MySQL server type
- 4. Initialize MySQL
- 5. Start the MySQL server
- 6. Secure the default user accounts

This process is described in the sections that follow.

### **2.3.4.1 Extracting the Install Archive**

To install MySQL manually, do the following:

- 1. If you are upgrading from a previous version please refer to Section 2.10.8, "Upgrading MySQL on Windows", before beginning the upgrade process.
- 2. Make sure that you are logged in as a user with administrator privileges.
- 3. Choose an installation location. Traditionally, the MySQL server is installed in C:\mysql. If you do not install MySQL at C:\mysql, you must specify the path to the install directory during startup or in an option file. See [Section 2.3.4.2, "Creating an Option File"](#page-140-0).

![](_page_140_Picture_14.jpeg)

#### **Note**

The MySQL Installer installs MySQL under C:\Program Files\MySQL.

4. Extract the install archive to the chosen installation location using your preferred file-compression tool. Some tools may extract the archive to a folder within your chosen installation location. If this occurs, you can move the contents of the subfolder into the chosen installation location.

### <span id="page-140-0"></span>**2.3.4.2 Creating an Option File**

If you need to specify startup options when you run the server, you can indicate them on the command line or place them in an option file. For options that are used every time the server starts, you may find it most convenient to use an option file to specify your MySQL configuration. This is particularly true under the following circumstances:

- The installation or data directory locations are different from the default locations (C:\Program Files\MySQL\MySQL Server 5.7 and C:\Program Files\MySQL\MySQL Server 5.7\data).
- You need to tune the server settings, such as memory, cache, or InnoDB configuration information.

When the MySQL server starts on Windows, it looks for option files in several locations, such as the Windows directory, C:\, and the MySQL installation directory (for the full list of locations, see Section 4.2.2.2, "Using Option Files"). The Windows directory typically is named something like C: \WINDOWS. You can determine its exact location from the value of the WINDIR environment variable using the following command:

#### C:\> **echo %WINDIR%**

MySQL looks for options in each location first in the my.ini file, and then in the my.cnf file. However, to avoid confusion, it is best if you use only one file. If your PC uses a boot loader where C: is not the boot drive, your only option is to use the my.ini file. Whichever option file you use, it must be a plain text file.

![](_page_141_Picture_1.jpeg)

#### **Note**

When using the MySQL Installer to install MySQL Server, it creates the my.ini in the default location, and the user executing MySQL Installer is granted full permissions to this new my.ini file.

In other words, be sure that the MySQL Server user has permission to read the my.ini file.

You can also make use of the example option files included with your MySQL distribution; see Section 5.1.2, "Server Configuration Defaults".

An option file can be created and modified with any text editor, such as Notepad. For example, if MySQL is installed in E:\mysql and the data directory is in E:\mydata\data, you can create an option file containing a [mysqld] section to specify values for the basedir and datadir options:

```
[mysqld]
# set basedir to your installation path
basedir=E:/mysql
# set datadir to the location of your data directory
datadir=E:/mydata/data
```

Microsoft Windows path names are specified in option files using (forward) slashes rather than backslashes. If you do use backslashes, double them:

```
[mysqld]
# set basedir to your installation path
basedir=E:\\mysql
# set datadir to the location of your data directory
datadir=E:\\mydata\\data
```

The rules for use of backslash in option file values are given in Section 4.2.2.2, "Using Option Files".

As of MySQL 5.7.6, the ZIP archive no longer includes a data directory. To initialize a MySQL installation by creating the data directory and populating the tables in the mysql system database, initialize MySQL using either --initialize or --initialize-insecure. For additional information, see Section 2.9.1, "Initializing the Data Directory".

If you would like to use a data directory in a different location, you should copy the entire contents of the data directory to the new location. For example, if you want to use E:\mydata as the data directory instead, you must do two things:

- 1. Move the entire data directory and all of its contents from the default location (for example C: \Program Files\MySQL\MySQL Server 5.7\data) to E:\mydata.
- 2. Use a --datadir option to specify the new data directory location each time you start the server.

### <span id="page-141-0"></span>**2.3.4.3 Selecting a MySQL Server Type**

The following table shows the available servers for Windows in MySQL 5.7.

| Binary       | Description                                                                               |
|--------------|-------------------------------------------------------------------------------------------|
| mysqld       | Optimized binary with named-pipe support                                                  |
| mysqld-debug | Like mysqld, but compiled with full debugging<br>and automatic memory allocation checking |

All of the preceding binaries are optimized for modern Intel processors, but should work on any Intel i386-class or higher processor.

Each of the servers in a distribution support the same set of storage engines. The SHOW ENGINES statement displays which engines a given server supports.

All Windows MySQL 5.7 servers have support for symbolic linking of database directories.

MySQL supports TCP/IP on all Windows platforms. MySQL servers on Windows also support named pipes, if you start the server with the named\_pipe system variable enabled. It is necessary to enable this variable explicitly because some users have experienced problems with shutting down the MySQL server when named pipes were used. The default is to use TCP/IP regardless of platform because named pipes are slower than TCP/IP in many Windows configurations.

## **2.3.4.4 Initializing the Data Directory**

If you installed MySQL using the noinstall package, you may need to initialize the data directory:

- Windows distributions prior to MySQL 5.7.7 include a data directory with a set of preinitialized accounts in the mysql database.
- As of 5.7.7, Windows installation operations performed using the noinstall package do not include a data directory. To initialize the data directory, use the instructions at Section 2.9.1, "Initializing the Data Directory".

## <span id="page-142-0"></span>**2.3.4.5 Starting the Server for the First Time**

This section gives a general overview of starting the MySQL server. The following sections provide more specific information for starting the MySQL server from the command line or as a Windows service.

The information here applies primarily if you installed MySQL using the noinstall version, or if you wish to configure and test MySQL manually rather than with the GUI tools.

The examples in these sections assume that MySQL is installed under the default location of C: \Program Files\MySQL\MySQL Server 5.7. Adjust the path names shown in the examples if you have MySQL installed in a different location.

Clients have two options. They can use TCP/IP, or they can use a named pipe if the server supports named-pipe connections.

MySQL for Windows also supports shared-memory connections if the server is started with the shared\_memory system variable enabled. Clients can connect through shared memory by using the --protocol=MEMORY option.

For information about which server binary to run, see [Section 2.3.4.3, "Selecting a MySQL Server](#page-141-0) [Type".](#page-141-0)

Testing is best done from a command prompt in a console window (or "DOS window"). In this way you can have the server display status messages in the window where they are easy to see. If something is wrong with your configuration, these messages make it easier for you to identify and fix any problems.

![](_page_142_Picture_14.jpeg)

#### **Note**

The database must be initialized before MySQL can be started. For additional information about the initialization process, see Section 2.9.1, "Initializing the Data Directory".

To start the server, enter this command:

```
C:\> "C:\Program Files\MySQL\MySQL Server 5.7\bin\mysqld" --console
```

For a server that includes InnoDB support, you should see the messages similar to those following as it starts (the path names and sizes may differ):

```
InnoDB: The first specified datafile c:\ibdata\ibdata1 did not exist:
InnoDB: a new database to be created!
InnoDB: Setting file c:\ibdata\ibdata1 size to 209715200
InnoDB: Database physically writes the file full: wait...
InnoDB: Log file c:\iblogs\ib_logfile0 did not exist: new to be created
InnoDB: Setting log file c:\iblogs\ib_logfile0 size to 31457280
```

```
InnoDB: Log file c:\iblogs\ib_logfile1 did not exist: new to be created
InnoDB: Setting log file c:\iblogs\ib_logfile1 size to 31457280
InnoDB: Log file c:\iblogs\ib_logfile2 did not exist: new to be created
InnoDB: Setting log file c:\iblogs\ib_logfile2 size to 31457280
InnoDB: Doublewrite buffer not found: creating new
InnoDB: Doublewrite buffer created
InnoDB: creating foreign key constraint system tables
InnoDB: foreign key constraint system tables created
011024 10:58:25 InnoDB: Started
```

When the server finishes its startup sequence, you should see something like this, which indicates that the server is ready to service client connections:

```
mysqld: ready for connections
Version: '5.7.44' socket: '' port: 3306
```

The server continues to write to the console any further diagnostic output it produces. You can open a new console window in which to run client programs.

If you omit the --console option, the server writes diagnostic output to the error log in the data directory (C:\Program Files\MySQL\MySQL Server 5.7\data by default). The error log is the file with the .err extension, and may be set using the --log-error option.

![](_page_143_Picture_6.jpeg)

#### **Note**

The initial root account in the MySQL grant tables has no password. After starting the server, you should set up a password for it using the instructions in Section 2.9.4, "Securing the Initial MySQL Account".

### <span id="page-143-0"></span>**2.3.4.6 Starting MySQL from the Windows Command Line**

The MySQL server can be started manually from the command line. This can be done on any version of Windows.

To start the mysqld server from the command line, you should start a console window (or "DOS window") and enter this command:

```
C:\> "C:\Program Files\MySQL\MySQL Server 5.7\bin\mysqld"
```

The path to mysqld may vary depending on the install location of MySQL on your system.

You can stop the MySQL server by executing this command:

C:\> **"C:\Program Files\MySQL\MySQL Server 5.7\bin\mysqladmin" -u root shutdown**

![](_page_143_Picture_16.jpeg)

#### **Note**

If the MySQL root user account has a password, you need to invoke mysqladmin with the -p option and supply the password when prompted.

This command invokes the MySQL administrative utility mysqladmin to connect to the server and tell it to shut down. The command connects as the MySQL root user, which is the default administrative account in the MySQL grant system.

![](_page_143_Picture_20.jpeg)

### **Note**

Users in the MySQL grant system are wholly independent from any operating system users under Microsoft Windows.

If mysqld does not start, check the error log to see whether the server wrote any messages there to indicate the cause of the problem. By default, the error log is located in the C:\Program Files \MySQL\MySQL Server 5.7\data directory. It is the file with a suffix of .err, or may be specified by passing in the --log-error option. Alternatively, you can try to start the server with the - console option; in this case, the server may display some useful information on the screen to help solve the problem.

The last option is to start mysqld with the --standalone and --debug options. In this case, mysqld writes a log file C:\mysqld.trace that should contain the reason why mysqld doesn't start. See Section 5.8.3, "The DBUG Package".

Use mysqld --verbose --help to display all the options that mysqld supports.

## <span id="page-144-1"></span>**2.3.4.7 Customizing the PATH for MySQL Tools**

![](_page_144_Picture_4.jpeg)

#### **Warning**

You must exercise great care when editing your system PATH by hand; accidental deletion or modification of any portion of the existing PATH value can leave you with a malfunctioning or even unusable system.

To make it easier to invoke MySQL programs, you can add the path name of the MySQL bin directory to your Windows system PATH environment variable:

- On the Windows desktop, right-click the **My Computer** icon, and select **Properties**.
- Next select the **Advanced** tab from the **System Properties** menu that appears, and click the **Environment Variables** button.
- Under **System Variables**, select **Path**, and then click the **Edit** button. The **Edit System Variable** dialogue should appear.
- Place your cursor at the end of the text appearing in the space marked **Variable Value**. (Use the **End** key to ensure that your cursor is positioned at the very end of the text in this space.) Then enter the complete path name of your MySQL bin directory (for example, C:\Program Files\MySQL \MySQL Server 5.7\bin)

![](_page_144_Picture_12.jpeg)

#### **Note**

There must be a semicolon separating this path from any values present in this field.

Dismiss this dialogue, and each dialogue in turn, by clicking **OK** until all of the dialogues that were opened have been dismissed. The new PATH value should now be available to any new command shell you open, allowing you to invoke any MySQL executable program by typing its name at the DOS prompt from any directory on the system, without having to supply the path. This includes the servers, the mysql client, and all MySQL command-line utilities such as mysqladmin and mysqldump.

You should not add the MySQL bin directory to your Windows PATH if you are running multiple MySQL servers on the same machine.

### <span id="page-144-0"></span>**2.3.4.8 Starting MySQL as a Windows Service**

On Windows, the recommended way to run MySQL is to install it as a Windows service, so that MySQL starts and stops automatically when Windows starts and stops. A MySQL server installed as a service can also be controlled from the command line using NET commands, or with the graphical Services utility. Generally, to install MySQL as a Windows service you should be logged in using an account that has administrator rights.

The Services utility (the Windows Service Control Manager) can be found in the Windows Control Panel. To avoid conflicts, it is advisable to close the Services utility while performing server installation or removal operations from the command line.

#### **Installing the service**

Before installing MySQL as a Windows service, you should first stop the current server if it is running by using the following command:

C:\> **"C:\Program Files\MySQL\MySQL Server 5.7\bin\mysqladmin" -u root shutdown**

![](_page_145_Picture_2.jpeg)

#### **Note**

If the MySQL root user account has a password, you need to invoke mysqladmin with the -p option and supply the password when prompted.

This command invokes the MySQL administrative utility mysqladmin to connect to the server and tell it to shut down. The command connects as the MySQL root user, which is the default administrative account in the MySQL grant system.

![](_page_145_Picture_6.jpeg)

#### **Note**

Users in the MySQL grant system are wholly independent from any operating system users under Windows.

Install the server as a service using this command:

C:\> **"C:\Program Files\MySQL\MySQL Server 5.7\bin\mysqld" --install**

The service-installation command does not start the server. Instructions for that are given later in this section.

To make it easier to invoke MySQL programs, you can add the path name of the MySQL bin directory to your Windows system PATH environment variable:

- On the Windows desktop, right-click the **My Computer** icon, and select **Properties**.
- Next select the **Advanced** tab from the **System Properties** menu that appears, and click the **Environment Variables** button.
- Under **System Variables**, select **Path**, and then click the **Edit** button. The **Edit System Variable** dialogue should appear.
- Place your cursor at the end of the text appearing in the space marked **Variable Value**. (Use the **End** key to ensure that your cursor is positioned at the very end of the text in this space.) Then enter the complete path name of your MySQL bin directory (for example, C:\Program Files\MySQL \MySQL Server 5.7\bin), and there should be a semicolon separating this path from any values present in this field. Dismiss this dialogue, and each dialogue in turn, by clicking **OK** until all of the dialogues that were opened have been dismissed. You should now be able to invoke any MySQL executable program by typing its name at the DOS prompt from any directory on the system, without having to supply the path. This includes the servers, the mysql client, and all MySQL command-line utilities such as mysqladmin and mysqldump.

You should not add the MySQL bin directory to your Windows PATH if you are running multiple MySQL servers on the same machine.

![](_page_145_Picture_18.jpeg)

#### **Warning**

You must exercise great care when editing your system PATH by hand; accidental deletion or modification of any portion of the existing PATH value can leave you with a malfunctioning or even unusable system.

The following additional arguments can be used when installing the service:

- You can specify a service name immediately following the --install option. The default service name is MySQL.
- If a service name is given, it can be followed by a single option. By convention, this should be defaults-file=file\_name to specify the name of an option file from which the server should read options when it starts.

The use of a single option other than --defaults-file is possible but discouraged. - defaults-file is more flexible because it enables you to specify multiple startup options for the server by placing them in the named option file.

• You can also specify a --local-service option following the service name. This causes the server to run using the LocalService Windows account that has limited system privileges. If both --defaults-file and --local-service are given following the service name, they can be in any order.

For a MySQL server that is installed as a Windows service, the following rules determine the service name and option files that the server uses:

- If the service-installation command specifies no service name or the default service name (MySQL) following the --install option, the server uses the service name of MySQL and reads options from the [mysqld] group in the standard option files.
- If the service-installation command specifies a service name other than MySQL following the install option, the server uses that service name. It reads options from the [mysqld] group and the group that has the same name as the service in the standard option files. This enables you to use the [mysqld] group for options that should be used by all MySQL services, and an option group with the service name for use by the server installed with that service name.
- If the service-installation command specifies a --defaults-file option after the service name, the server reads options the same way as described in the previous item, except that it reads options only from the named file and ignores the standard option files.

As a more complex example, consider the following command:

```
C:\> "C:\Program Files\MySQL\MySQL Server 5.7\bin\mysqld"
 --install MySQL --defaults-file=C:\my-opts.cnf
```

Here, the default service name (MySQL) is given after the --install option. If no --defaultsfile option had been given, this command would have the effect of causing the server to read the [mysqld] group from the standard option files. However, because the --defaults-file option is present, the server reads options from the [mysqld] option group, and only from the named file.

![](_page_146_Picture_10.jpeg)

## **Note**

On Windows, if the server is started with the --defaults-file and - install options, --install must be first. Otherwise, mysqld.exe attempts to start the MySQL server.

You can also specify options as Start parameters in the Windows Services utility before you start the MySQL service.

Finally, before trying to start the MySQL service, make sure the user variables %TEMP% and %TMP% (and also %TMPDIR%, if it has ever been set) for the operating system user who is to run the service are pointing to a folder to which the user has write access. The default user for running the MySQL service is LocalSystem, and the default value for its %TEMP% and %TMP% is C:\Windows\Temp, a directory LocalSystem has write access to by default. However, if there are any changes to that default setup (for example, changes to the user who runs the service or to the mentioned user variables, or the - tmpdir option has been used to put the temporary directory somewhere else), the MySQL service might fail to run because write access to the temporary directory has not been granted to the proper user.

### **Starting the service**

After a MySQL server instance has been installed as a service, Windows starts the service automatically whenever Windows starts. The service also can be started immediately from

the Services utility, or by using an sc start mysqld\_service\_name or NET START mysqld\_service\_name command. SC and NET commands are not case-sensitive.

When run as a service, mysqld has no access to a console window, so no messages can be seen there. If mysqld does not start, check the error log to see whether the server wrote any messages there to indicate the cause of the problem. The error log is located in the MySQL data directory (for example, C:\Program Files\MySQL\MySQL Server 5.7\data). It is the file with a suffix of .err.

When a MySQL server has been installed as a service, and the service is running, Windows stops the service automatically when Windows shuts down. The server also can be stopped manually using the Services utility, the sc stop mysqld\_service\_name command, the NET STOP mysqld\_service\_name command, or the mysqladmin shutdown command.

You also have the choice of installing the server as a manual service if you do not wish for the service to be started automatically during the boot process. To do this, use the --install-manual option rather than the --install option:

```
C:\> "C:\Program Files\MySQL\MySQL Server 5.7\bin\mysqld" --install-manual
```

### **Removing the service**

To remove a server that is installed as a service, first stop it if it is running by executing SC STOP mysqld\_service\_name or NET STOP mysqld\_service\_name. Then use SC DELETE mysqld\_service\_name to remove it:

```
C:\> SC DELETE mysql
```

Alternatively, use the mysqld --remove option to remove the service.

```
C:\> "C:\Program Files\MySQL\MySQL Server 5.7\bin\mysqld" --remove
```

If mysqld is not running as a service, you can start it from the command line. For instructions, see [Section 2.3.4.6, "Starting MySQL from the Windows Command Line".](#page-143-0)

If you encounter difficulties during installation, see [Section 2.3.5, "Troubleshooting a Microsoft](#page-148-0) [Windows MySQL Server Installation".](#page-148-0)

For more information about stopping or removing a Windows service, see Section 5.7.2.2, "Starting Multiple MySQL Instances as Windows Services".

### **2.3.4.9 Testing The MySQL Installation**

You can test whether the MySQL server is working by executing any of the following commands:

```
C:\> "C:\Program Files\MySQL\MySQL Server 5.7\bin\mysqlshow"
C:\> "C:\Program Files\MySQL\MySQL Server 5.7\bin\mysqlshow" -u root mysql
C:\> "C:\Program Files\MySQL\MySQL Server 5.7\bin\mysqladmin" version status proc
C:\> "C:\Program Files\MySQL\MySQL Server 5.7\bin\mysql" test
```

If mysqld is slow to respond to TCP/IP connections from client programs, there is probably a problem with your DNS. In this case, start mysqld with the skip\_name\_resolve system variable enabled and use only localhost and IP addresses in the Host column of the MySQL grant tables. (Be sure that an account exists that specifies an IP address or you may not be able to connect.)

You can force a MySQL client to use a named-pipe connection rather than TCP/IP by specifying the - pipe or --protocol=PIPE option, or by specifying . (period) as the host name. Use the --socket option to specify the name of the pipe if you do not want to use the default pipe name.

If you have set a password for the root account, deleted the anonymous account, or created a new user account, then to connect to the MySQL server you must use the appropriate -u and -p options with the commands shown previously. See Section 4.2.4, "Connecting to the MySQL Server Using Command Options".

For more information about mysqlshow, see Section 4.5.7, "mysqlshow — Display Database, Table, and Column Information".

## <span id="page-148-0"></span>**2.3.5 Troubleshooting a Microsoft Windows MySQL Server Installation**

When installing and running MySQL for the first time, you may encounter certain errors that prevent the MySQL server from starting. This section helps you diagnose and correct some of these errors.

Your first resource when troubleshooting server issues is the error log. The MySQL server uses the error log to record information relevant to the error that prevents the server from starting. The error log is located in the data directory specified in your my.ini file. The default data directory location is C: \Program Files\MySQL\MySQL Server 5.7\data, or C:\ProgramData\Mysql on Windows 7 and Windows Server 2008. The C:\ProgramData directory is hidden by default. You need to change your folder options to see the directory and contents. For more information on the error log and understanding the content, see Section 5.4.2, "The Error Log".

For information regarding possible errors, also consult the console messages displayed when the MySQL service is starting. Use the SC START mysqld\_service\_name or NET START mysqld\_service\_name command from the command line after installing mysqld as a service to see any error messages regarding the starting of the MySQL server as a service. See [Section 2.3.4.8,](#page-144-0) ["Starting MySQL as a Windows Service"](#page-144-0).

The following examples show other common error messages you might encounter when installing MySQL and starting the server for the first time:

• If the MySQL server cannot find the mysql privileges database or other critical files, it displays these messages:

```
System error 1067 has occurred.
Fatal error: Can't open and lock privilege tables:
Table 'mysql.user' doesn't exist
```

These messages often occur when the MySQL base or data directories are installed in different locations than the default locations (C:\Program Files\MySQL\MySQL Server 5.7 and C: \Program Files\MySQL\MySQL Server 5.7\data, respectively).

This situation can occur when MySQL is upgraded and installed to a new location, but the configuration file is not updated to reflect the new location. In addition, old and new configuration files might conflict. Be sure to delete or rename any old configuration files when upgrading MySQL.

If you have installed MySQL to a directory other than C:\Program Files\MySQL\MySQL Server 5.7, ensure that the MySQL server is aware of this through the use of a configuration (my.ini) file. Put the my.ini file in your Windows directory, typically C:\WINDOWS. To determine its exact location from the value of the WINDIR environment variable, issue the following command from the command prompt:

```
C:\> echo %WINDIR%
```

You can create or modify an option file with any text editor, such as Notepad. For example, if MySQL is installed in E:\mysql and the data directory is D:\MySQLdata, you can create the option file and set up a [mysqld] section to specify values for the basedir and datadir options:

```
[mysqld]
# set basedir to your installation path
basedir=E:/mysql
# set datadir to the location of your data directory
datadir=D:/MySQLdata
```

Microsoft Windows path names are specified in option files using (forward) slashes rather than backslashes. If you do use backslashes, double them:

```
[mysqld]
```

```
# set basedir to your installation path
basedir=C:\\Program Files\\MySQL\\MySQL Server 5.7
# set datadir to the location of your data directory
datadir=D:\\MySQLdata
```

The rules for use of backslash in option file values are given in Section 4.2.2.2, "Using Option Files".

If you change the datadir value in your MySQL configuration file, you must move the contents of the existing MySQL data directory before restarting the MySQL server.

See [Section 2.3.4.2, "Creating an Option File"](#page-140-0).

• If you reinstall or upgrade MySQL without first stopping and removing the existing MySQL service and install MySQL using the MySQL Installer, you might see this error:

```
Error: Cannot create Windows service for MySql. Error: 0
```

This occurs when the Configuration Wizard tries to install the service and finds an existing service with the same name.

One solution to this problem is to choose a service name other than mysql when using the configuration wizard. This enables the new service to be installed correctly, but leaves the outdated service in place. Although this is harmless, it is best to remove old services that are no longer in use.

To permanently remove the old mysql service, execute the following command as a user with administrative privileges, on the command line:

```
C:\> SC DELETE mysql
[SC] DeleteService SUCCESS
```

If the SC utility is not available for your version of Windows, download the delsrv utility from [http://](http://www.microsoft.com/windows2000/techinfo/reskit/tools/existing/delsrv-o.asp) [www.microsoft.com/windows2000/techinfo/reskit/tools/existing/delsrv-o.asp](http://www.microsoft.com/windows2000/techinfo/reskit/tools/existing/delsrv-o.asp) and use the delsrv mysql syntax.

## <span id="page-149-0"></span>**2.3.6 Windows Postinstallation Procedures**

GUI tools exist that perform most of the tasks described in this section, including:

- [MySQL Installer](#page-110-0): Used to install and upgrade MySQL products.
- MySQL Workbench: Manages the MySQL server and edits SQL statements.

If necessary, initialize the data directory and create the MySQL grant tables. Windows distributions prior to MySQL 5.7.7 include a data directory with a set of preinitialized accounts in the mysql database. As of 5.7.7, Windows installation operations performed by MySQL Installer initialize the data directory automatically. For installation from a ZIP Archive package, initialize the data directory as described at Section 2.9.1, "Initializing the Data Directory".

Regarding passwords, if you installed MySQL using the MySQL Installer, you may have already assigned a password to the initial root account. (See [Section 2.3.3, "MySQL Installer for Windows".](#page-110-0)) Otherwise, use the password-assignment procedure given in Section 2.9.4, "Securing the Initial MySQL Account".

Before assigning a password, you might want to try running some client programs to make sure that you can connect to the server and that it is operating properly. Make sure that the server is running (see [Section 2.3.4.5, "Starting the Server for the First Time"\)](#page-142-0). You can also set up a MySQL service that runs automatically when Windows starts (see [Section 2.3.4.8, "Starting MySQL as a Windows](#page-144-0) [Service"\)](#page-144-0).

These instructions assume that your current location is the MySQL installation directory and that it has a bin subdirectory containing the MySQL programs used here. If that is not true, adjust the command path names accordingly.

If you installed MySQL using MySQL Installer (see [Section 2.3.3, "MySQL Installer for Windows"](#page-110-0)), the default installation directory is C:\Program Files\MySQL\MySQL Server 5.7:

```
C:\> cd "C:\Program Files\MySQL\MySQL Server 5.7"
```

A common installation location for installation from a ZIP archive is C:\mysql:

```
C:\> cd C:\mysql
```

Alternatively, add the bin directory to your PATH environment variable setting. That enables your command interpreter to find MySQL programs properly, so that you can run a program by typing only its name, not its path name. See [Section 2.3.4.7, "Customizing the PATH for MySQL Tools"](#page-144-1).

With the server running, issue the following commands to verify that you can retrieve information from the server. The output should be similar to that shown here.

Use mysqlshow to see what databases exist:

```
C:\> bin\mysqlshow
+--------------------+
| Databases |
+--------------------+
| information_schema |
| mysql |
| performance_schema |
| sys |
+--------------------+
```

The list of installed databases may vary, but always includes at least mysql and information\_schema. Before MySQL 5.7.7, a test database may also be created automatically.

The preceding command (and commands for other MySQL programs such as mysql) may not work if the correct MySQL account does not exist. For example, the program may fail with an error, or you may not be able to view all databases. If you install MySQL using MySQL Installer, the root user is created automatically with the password you supplied. In this case, you should use the -u root and p options. (You must use those options if you have already secured the initial MySQL accounts.) With p, the client program prompts for the root password. For example:

```
C:\> bin\mysqlshow -u root -p
Enter password: (enter root password here)
+--------------------+
| Databases |
+--------------------+
| information_schema |
| mysql |
| performance_schema |
| sys |
+--------------------+
```

If you specify a database name, mysqlshow displays a list of the tables within the database:

```
C:\> bin\mysqlshow mysql
Database: mysql
+---------------------------+
| Tables |
+---------------------------+
| columns_priv |
| db |
| engine_cost |
| event |
| func |
| general_log |
| gtid_executed |
| help_category |
| help_keyword |
| help_relation |
| help_topic |
```

```
| innodb_index_stats |
| innodb_table_stats |
| ndb_binlog_index |
| plugin |
| proc |
| procs_priv |
| proxies_priv |
| server_cost |
| servers |
| slave_master_info |
| slave_relay_log_info |
| slave_worker_info |
| slow_log |
| tables_priv |
| time_zone |
| time_zone_leap_second |
| time_zone_name |
| time_zone_transition |
| time_zone_transition_type |
| user |
+---------------------------+
```

Use the mysql program to select information from a table in the mysql database:

```
C:\> bin\mysql -e "SELECT User, Host, plugin FROM mysql.user" mysql
+------+-----------+-----------------------+
| User | Host | plugin |
+------+-----------+-----------------------+
| root | localhost | mysql_native_password |
+------+-----------+-----------------------+
```

For more information about mysql and mysqlshow, see Section 4.5.1, "mysql — The MySQL Command-Line Client", and Section 4.5.7, "mysqlshow — Display Database, Table, and Column Information".

## <span id="page-151-0"></span>**2.3.7 Windows Platform Restrictions**

The following restrictions apply to use of MySQL on the Windows platform:

#### • **Process memory**

On Windows 32-bit platforms, it is not possible by default to use more than 2GB of RAM within a single process, including MySQL. This is because the physical address limit on Windows 32-bit is 4GB and the default setting within Windows is to split the virtual address space between kernel (2GB) and user/applications (2GB).

Some versions of Windows have a boot time setting to enable larger applications by reducing the kernel application. Alternatively, to use more than 2GB, use a 64-bit version of Windows.

#### • **File system aliases**

When using MyISAM tables, you cannot use aliases within Windows link to the data files on another volume and then link back to the main MySQL datadir location.

This facility is often used to move the data and index files to a RAID or other fast solution, while retaining the main .frm files in the default data directory configured with the datadir option.

#### • **Limited number of ports**

Windows systems have about 4,000 ports available for client connections, and after a connection on a port closes, it takes two to four minutes before the port can be reused. In situations where clients connect to and disconnect from the server at a high rate, it is possible for all available ports to be used up before closed ports become available again. If this happens, the MySQL server appears to be unresponsive even though it is running. Ports may be used by other applications running on the machine as well, in which case the number of ports available to MySQL is lower.

For more information about this problem, see<https://support.microsoft.com/kb/196271>.

### • **DATA DIRECTORY and INDEX DIRECTORY**

The DATA DIRECTORY clause of the CREATE TABLE statement is supported on Windows for InnoDB tables only, as described in Section 14.6.1.2, "Creating Tables Externally". For MyISAM and other storage engines, the DATA DIRECTORY and INDEX DIRECTORY clauses for CREATE TABLE are ignored on Windows and any other platforms with a nonfunctional realpath() call.

### • **DROP DATABASE**

You cannot drop a database that is in use by another session.

### • **Case-insensitive names**

File names are not case-sensitive on Windows, so MySQL database and table names are also not case-sensitive on Windows. The only restriction is that database and table names must be specified using the same case throughout a given statement. See Section 9.2.3, "Identifier Case Sensitivity".

#### • **Directory and file names**

On Windows, MySQL Server supports only directory and file names that are compatible with the current ANSI code pages. For example, the following Japanese directory name does not work in the Western locale (code page 1252):

```
datadir="C:/私たちのプロジェクトのデータ"
```

The same limitation applies to directory and file names referred to in SQL statements, such as the data file path name in LOAD DATA.

#### • **The \ path name separator character**

Path name components in Windows are separated by the \ character, which is also the escape character in MySQL. If you are using LOAD DATA or SELECT ... INTO OUTFILE, use Unix-style file names with / characters:

```
mysql> LOAD DATA INFILE 'C:/tmp/skr.txt' INTO TABLE skr;
mysql> SELECT * INTO OUTFILE 'C:/tmp/skr.txt' FROM skr;
```

Alternatively, you must double the \ character:

```
mysql> LOAD DATA INFILE 'C:\\tmp\\skr.txt' INTO TABLE skr;
mysql> SELECT * INTO OUTFILE 'C:\\tmp\\skr.txt' FROM skr;
```

#### • **Problems with pipes**

Pipes do not work reliably from the Windows command-line prompt. If the pipe includes the character ^Z / CHAR(24), Windows thinks that it has encountered end-of-file and aborts the program.

This is mainly a problem when you try to apply a binary log as follows:

```
C:\> mysqlbinlog binary_log_file | mysql --user=root
```

If you have a problem applying the log and suspect that it is because of a ^Z / CHAR(24) character, you can use the following workaround:

```
C:\> mysqlbinlog binary_log_file --result-file=/tmp/bin.sql
C:\> mysql --user=root --execute "source /tmp/bin.sql"
```

The latter command also can be used to reliably read any SQL file that may contain binary data.

## <span id="page-152-0"></span>**2.4 Installing MySQL on macOS**

For a list of macOS versions that the MySQL server supports, see [https://www.mysql.com/support/](https://www.mysql.com/support/supportedplatforms/database.md) [supportedplatforms/database.html](https://www.mysql.com/support/supportedplatforms/database.md).

MySQL for macOS is available in a number of different forms:

- Native Package Installer, which uses the native macOS installer (DMG) to walk you through the installation of MySQL. For more information, see [Section 2.4.2, "Installing MySQL on macOS Using](#page-154-0) [Native Packages"](#page-154-0). You can use the package installer with macOS. The user you use to perform the installation must have administrator privileges.
- Compressed TAR archive, which uses a file packaged using the Unix tar and gzip commands. To use this method, you 'to open a Terminal window. You do not need administrator privileges using this method, as you can install the MySQL server anywhere using this method. For more information on using this method, you can use the generic instructions for using a tarball, [Section 2.2, "Installing](#page-103-0) [MySQL on Unix/Linux Using Generic Binaries"](#page-103-0).

In addition to the core installation, the Package Installer also includes [Section 2.4.3, "Installing a](#page-159-0) [MySQL Launch Daemon"](#page-159-0) and [Section 2.4.4, "Installing and Using the MySQL Preference Pane",](#page-162-0) both of which simplify the management of your installation.

For additional information on using MySQL on macOS, see [Section 2.4.1, "General Notes on Installing](#page-153-0) [MySQL on macOS".](#page-153-0)

## <span id="page-153-0"></span>**2.4.1 General Notes on Installing MySQL on macOS**

You should keep the following issues and notes in mind:

• As of macOS 10.14 (Majave), the macOS MySQL 5.7 Installer application requires permission to control System Events so it can display a generated (temporary) MySQL root password. Choosing "Don't Allow" means this password won't be visible for use.

If previously disallowed, the fix is enabling System Events.app for Installer.app under the Security & Privacy | Automation | Privacy tab.

- A launchd daemon is installed, and it includes MySQL configuration options. Consider editing it if needed, see the documentation below for additional information. Also, macOS 10.10 removed startup item support in favor of launchd daemons. The optional MySQL preference pane under macOS **System Preferences** uses the launchd daemon.
- You may need (or want) to create a specific mysql user to own the MySQL directory and data. You can do this through the Directory Utility, and the mysql user should already exist. For use in single user mode, an entry for \_mysql (note the underscore prefix) should already exist within the system /etc/passwd file.
- Because the MySQL package installer installs the MySQL contents into a version and platform specific directory, you can use this to upgrade and migrate your database between versions. You need either to copy the data directory from the old version to the new version, or to specify an alternative datadir value to set location of the data directory. By default, the MySQL directories are installed under /usr/local/.
- You might want to add aliases to your shell's resource file to make it easier to access commonly used programs such as mysql and mysqladmin from the command line. The syntax for bash is:

```
alias mysql=/usr/local/mysql/bin/mysql
alias mysqladmin=/usr/local/mysql/bin/mysqladmin
```

For tcsh, use:

```
alias mysql /usr/local/mysql/bin/mysql
alias mysqladmin /usr/local/mysql/bin/mysqladmin
```

Even better, add /usr/local/mysql/bin to your PATH environment variable. You can do this by modifying the appropriate startup file for your shell. For more information, see Section 4.2.1, "Invoking MySQL Programs".

• After you have copied over the MySQL database files from the previous installation and have successfully started the new server, you should consider removing the old installation files to save disk space. Additionally, you should also remove older versions of the Package Receipt directories located in /Library/Receipts/mysql-VERSION.pkg.

## <span id="page-154-0"></span>**2.4.2 Installing MySQL on macOS Using Native Packages**

The package is located inside a disk image (.dmg) file that you first need to mount by double-clicking its icon in the Finder. It should then mount the image and display its contents.

![](_page_154_Picture_5.jpeg)

#### **Note**

Before proceeding with the installation, be sure to stop all running MySQL server instances by using either the MySQL Manager Application (on macOS Server), the preference pane, or mysqladmin shutdown on the command line.

To install MySQL using the package installer:

1. Download the disk image (.dmg) file (the community version is available [here\)](https://dev.mysql.com/downloads/mysql/) that contains the MySQL package installer. Double-click the file to mount the disk image and see its contents.

**Figure 2.13 MySQL Package Installer: DMG Contents**

![](_page_154_Picture_11.jpeg)

- 2. Double-click the MySQL installer package from the disk. It is named according to the version of MySQL you have downloaded. For example, for MySQL server 5.7.44 it might be named mysql-5.7.44-macos-10.13-x86\_64.pkg.
- 3. The initial wizard introduction screen references the MySQL server version to install. Click **Continue** to begin the installation.

**Figure 2.14 MySQL Package Installer Wizard: Introduction**

![](_page_155_Picture_2.jpeg)

4. The MySQL community edition shows a copy of the relevant GNU General Public License. Click **Continue** and then **Agree** to continue.

5. From the **Installation Type** page you can either click **Install** to execute the installation wizard using all defaults, click **Customize** to alter which components to install (MySQL server, Preference Pane, Launchd Support -- all enabled by default).

![](_page_156_Picture_2.jpeg)

#### **Note**

Although the **Change Install Location** option is visible, the installation location cannot be changed.

**Figure 2.15 MySQL Package Installer Wizard: Installation Type**

![](_page_156_Picture_6.jpeg)

**Figure 2.16 MySQL Package Installer Wizard: Customize**

![](_page_157_Figure_2.jpeg)

- 6. Click **Install** to begin the installation process.
- 7. After a successful installation, the installer displays a window with your temporary root password. This cannot be recovered so you must save this password for the initial login to MySQL. For example:

**Figure 2.17 MySQL Package Installer Wizard: Temporary Root Password**

![](_page_157_Picture_6.jpeg)

![](_page_157_Picture_7.jpeg)

#### **Note**

MySQL expires this temporary root password after the initial login and requires you to create a new password.

8. **Summary** is the final step and references a successful and complete MySQL Server installation. **Close** the wizard.

**Figure 2.18 MySQL Package Installer Wizard: Summary**

![](_page_158_Picture_2.jpeg)

MySQL server is now installed, but it is not loaded (or started) by default. Use either launchctl from the command line, or start MySQL by clicking "Start" using the MySQL preference pane. For additional information, see [Section 2.4.3, "Installing a MySQL Launch Daemon",](#page-159-0) and [Section 2.4.4, "Installing and](#page-162-0) [Using the MySQL Preference Pane".](#page-162-0) Use the MySQL Preference Pane or launchd to configure MySQL to automatically start at bootup.

When installing using the package installer, the files are installed into a directory within /usr/ local matching the name of the installation version and platform. For example, the installer file mysql-5.7.44-macos10.13-x86\_64.dmg installs MySQL into /usr/local/mysql-5.7.44 macos10.13-x86\_64/ . The following table shows the layout of the installation directory.

**Table 2.7 MySQL Installation Layout on macOS**

<span id="page-158-0"></span>

| Directory     | Contents of Directory                                                                                                  |
|---------------|------------------------------------------------------------------------------------------------------------------------|
| bin           | mysqld server, client and utility programs                                                                             |
| data          | Log files, databases                                                                                                   |
| docs          | Helper documents, like the Release Notes and<br>build information                                                      |
| include       | Include (header) files                                                                                                 |
| lib           | Libraries                                                                                                              |
| man           | Unix manual pages                                                                                                      |
| mysql-test    | MySQL test suite                                                                                                       |
| share         | Miscellaneous support files, including error<br>messages, sample configuration files, SQL for<br>database installation |
| support-files | Scripts and sample configuration files                                                                                 |

| Directory       | Contents of Directory             |
|-----------------|-----------------------------------|
| /tmp/mysql.sock | Location of the MySQL Unix socket |

During the package installer process, a symbolic link from /usr/local/mysql to the version/platform specific directory created during installation is created automatically.

## <span id="page-159-0"></span>**2.4.3 Installing a MySQL Launch Daemon**

macOS uses launch daemons to automatically start, stop, and manage processes and applications such as MySQL.

By default, the installation package (DMG) on macOS installs a launchd file named /Library/ LaunchDaemons/com.oracle.oss.mysql.mysqld.plist that contains a plist definition similar to:

```
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
 <key>Label</key> <string>com.oracle.oss.mysql.mysqld</string>
 <key>ProcessType</key> <string>Interactive</string>
 <key>Disabled</key> <false/>
 <key>RunAtLoad</key> <true/>
 <key>KeepAlive</key> <true/>
 <key>SessionCreate</key> <true/>
 <key>LaunchOnlyOnce</key> <false/>
 <key>UserName</key> <string>_mysql</string>
 <key>GroupName</key> <string>_mysql</string>
 <key>ExitTimeOut</key> <integer>600</integer>
 <key>Program</key> <string>/usr/local/mysql/bin/mysqld</string>
 <key>ProgramArguments</key>
 <array>
 <string>/usr/local/mysql/bin/mysqld</string>
 <string>--user=_mysql</string>
 <string>--basedir=/usr/local/mysql</string>
 <string>--datadir=/usr/local/mysql/data</string>
 <string>--plugin-dir=/usr/local/mysql/lib/plugin</string>
 <string>--log-error=/usr/local/mysql/data/mysqld.local.err</string>
 <string>--pid-file=/usr/local/mysql/data/mysqld.local.pid</string>
 </array>
 <key>WorkingDirectory</key> <string>/usr/local/mysql</string>
</dict>
</plist>
```

![](_page_159_Picture_7.jpeg)

#### **Note**

Some users report that adding a plist DOCTYPE declaration causes the launchd operation to fail, despite it passing the lint check. We suspect it's a copy-n-paste error. The md5 checksum of a file containing the above snippet is 24710a27dc7a28fb7ee6d825129cd3cf.

To enable the launchd service, you can either:

• Click **Start MySQL Server** from the MySQL preference pane.

**Figure 2.19 MySQL Preference Pane: Location**

![](_page_160_Figure_2.jpeg)

**Figure 2.20 MySQL Preference Pane: Usage**

![](_page_161_Picture_2.jpeg)

• Or, manually load the launchd file.

```
$> cd /Library/LaunchDaemons
$> sudo launchctl load -F com.oracle.oss.mysql.mysqld.plist
```

• To configure MySQL to automatically start at bootup, you can:

\$> sudo launchctl load -w com.oracle.oss.mysql.mysqld.plist

![](_page_161_Picture_7.jpeg)

#### **Note**

When upgrading MySQL server, the launchd installation process removes the old startup items that were installed with MySQL server 5.7.7 and earlier.

Upgrading also replaces your existing launchd file of the same name.

#### Additional launchd related information:

- The plist entries override my.cnf entries, because they are passed in as command line arguments. For additional information about passing in program options, see Section 4.2.2, "Specifying Program Options".
- The **ProgramArguments** section defines the command line options that are passed into the program, which is the mysqld binary in this case.
- The default plist definition is written with less sophisticated use cases in mind. For more complicated setups, you may want to remove some of the arguments and instead rely on a MySQL configuration file, such as my.cnf.
- If you edit the plist file, then uncheck the installer option when reinstalling or upgrading MySQL. Otherwise, your edited plist file is overwritten, with the loss of any changes you have made.

Because the default plist definition defines several **ProgramArguments**, you might remove most of these arguments and instead rely upon your my.cnf MySQL configuration file to define them. For example:

```
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
 <key>Label</key> <string>com.oracle.oss.mysql.mysqld</string>
 <key>ProcessType</key> <string>Interactive</string>
 <key>Disabled</key> <false/>
 <key>RunAtLoad</key> <true/>
 <key>KeepAlive</key> <true/>
 <key>SessionCreate</key> <true/>
 <key>LaunchOnlyOnce</key> <false/>
 <key>UserName</key> <string>_mysql</string>
 <key>GroupName</key> <string>_mysql</string>
 <key>ExitTimeOut</key> <integer>600</integer>
 <key>Program</key> <string>/usr/local/mysql/bin/mysqld</string>
 <key>WorkingDirectory</key> <string>/usr/local/mysql</string>
 <key>ProgramArguments</key>
 <array>
 <string>/usr/local/mysql/bin/mysqld</string>
 <string>--user=_mysql</string>
 </array>
</dict>
</plist>
```

In this case, the basedir, datadir, plugin\_dir, log\_error, and pid\_file options were removed from the plist definition, and then you might define them in my.cnf.

## <span id="page-162-0"></span>**2.4.4 Installing and Using the MySQL Preference Pane**

The MySQL Installation Package includes a MySQL preference pane that enables you to start, stop, and control automated startup during boot of your MySQL installation.

This preference pane is installed by default, and is listed under your system's System Preferences window.

**Figure 2.21 MySQL Preference Pane: Location**

![](_page_163_Picture_2.jpeg)

#### To install the MySQL Preference Pane:

1. Download the disk image (.dmg) file (the community version is available [here\)](https://dev.mysql.com/downloads/mysql/) that contains the MySQL package installer. Double-click the file to mount the disk image and see its contents.

**Figure 2.22 MySQL Package Installer: DMG Contents**

![](_page_164_Picture_2.jpeg)

- 2. Go through the process of installing the MySQL server, as described in the documentation at [Section 2.4.2, "Installing MySQL on macOS Using Native Packages"](#page-154-0).
- 3. Click **Customize** at the **Installation Type** step. The "Preference Pane" option is listed there and enabled by default; make sure it is not deselected.

**Figure 2.23 MySQL Installer on macOS: Customize**

![](_page_164_Figure_6.jpeg)

4. Complete the MySQL server installation process.

![](_page_165_Picture_1.jpeg)

#### **Note**

The MySQL preference pane only starts and stops MySQL installation installed from the MySQL package installation that have been installed in the default location.

Once the MySQL preference pane has been installed, you can control your MySQL server instance using the preference pane. To use the preference pane, open the **System Preferences...** from the Apple menu. Select the MySQL preference pane by clicking the MySQL icon within the preference panes list.

**Figure 2.24 MySQL Preference Pane: Location**

![](_page_165_Picture_6.jpeg)

**Figure 2.25 MySQL Preference Pane: Usage**

![](_page_166_Picture_2.jpeg)

The MySQL Preference Pane shows the current status of the MySQL server, showing **stopped** (in red) if the server is not running and **running** (in green) if the server has already been started. The preference pane also shows the current setting for whether the MySQL server has been set to start automatically.

• **To start the MySQL server using the preference pane:**

Click **Start MySQL Server**. You may be prompted for the username and password of a user with administrator privileges to start the MySQL server.

• **To stop the MySQL server using the preference pane:**

Click **Stop MySQL Server**. You may be prompted for the username and password of a user with administrator privileges to stop the MySQL server.

• **To automatically start the MySQL server when the system boots:**

Check the check box next to **Automatically Start MySQL Server on Startup**.

• **To disable automatic MySQL server startup when the system boots:**

Uncheck the check box next to **Automatically Start MySQL Server on Startup**.

You can close the System Preferences... window once you have completed your settings.

## <span id="page-166-0"></span>**2.5 Installing MySQL on Linux**

Linux supports a number of different solutions for installing MySQL. We recommend that you use one of the distributions from Oracle, for which several methods for installation are available:

**Table 2.8 Linux Installation Methods and Information**

| Type | Setup Method                       | Additional Information |
|------|------------------------------------|------------------------|
| Apt  | Enable the MySQL Apt<br>repository | Documentation          |
| Yum  | Enable the MySQL Yum<br>repository | Documentation          |

| Type                                | Setup Method                                                                                                     | Additional Information |
|-------------------------------------|------------------------------------------------------------------------------------------------------------------|------------------------|
| Zypper                              | Enable the MySQL SLES<br>repository                                                                              | Documentation          |
| RPM                                 | Download a specific package                                                                                      | Documentation          |
| DEB                                 | Download a specific package                                                                                      | Documentation          |
| Generic                             | Download a generic package                                                                                       | Documentation          |
| Source                              | Compile from source                                                                                              | Documentation          |
| Docker                              | Use the Oracle Container<br>Registry. You can also use My<br>Oracle Support for the MySQL<br>Enterprise Edition. | Documentation          |
| Oracle Unbreakable Linux<br>Network | Use ULN channels                                                                                                 | Documentation          |

As an alternative, you can use the package manager on your system to automatically download and install MySQL with packages from the native software repositories of your Linux distribution. These native packages are often several versions behind the currently available release. You also normally cannot install development milestone releases (DMRs), as these are not usually made available in the native repositories. For more information on using the native package installers, see [Section 2.5.8,](#page-189-0) ["Installing MySQL on Linux from the Native Software Repositories".](#page-189-0)

![](_page_167_Picture_3.jpeg)

#### **Note**

For many Linux installations, you may want to set up MySQL to be started automatically when your machine starts. Many of the native package installations perform this operation for you, but for source, binary and RPM solutions you may need to set this up separately. The required script, mysql.server, can be found in the support-files directory under the MySQL installation directory or in a MySQL source tree. You can install it as /etc/init.d/mysql for automatic MySQL startup and shutdown. See Section 4.3.3, "mysql.server — MySQL Server Startup Script".

## <span id="page-167-0"></span>**2.5.1 Installing MySQL on Linux Using the MySQL Yum Repository**

The [MySQL Yum repository](https://dev.mysql.com/downloads/repo/yum/) for Oracle Linux, Red Hat Enterprise Linux and CentOS provides RPM packages for installing the MySQL server, client, MySQL Workbench, MySQL Utilities, MySQL Router, MySQL Shell, Connector/ODBC, Connector/Python and so on (not all packages are available for all the distributions; see [Installing Additional MySQL Products and Components with Yum](#page-170-0) for details).

### **Before You Start**

As a popular, open-source software, MySQL, in its original or re-packaged form, is widely installed on many systems from various sources, including different software download sites, software repositories, and so on. The following instructions assume that MySQL is not already installed on your system using a third-party-distributed RPM package; if that is not the case, follow the instructions given in Section 2.10.5, "Upgrading MySQL with the MySQL Yum Repository" or [Section 2.5.2, "Replacing a](#page-171-0) [Third-Party Distribution of MySQL Using the MySQL Yum Repository".](#page-171-0)

### **Steps for a Fresh Installation of MySQL**

Follow the steps below to install the latest GA version of MySQL with the MySQL Yum repository:

### <span id="page-167-1"></span>**Adding the MySQL Yum Repository** 1.

First, add the MySQL Yum repository to your system's repository list. This is a one-time operation, which can be performed by installing an RPM provided by MySQL. Follow these steps:

- a. Go to the Download MySQL Yum Repository page ([https://dev.mysql.com/downloads/repo/](https://dev.mysql.com/downloads/repo/yum/) [yum/\)](https://dev.mysql.com/downloads/repo/yum/) in the MySQL Developer Zone.
- b. Select and download the release package for your platform.
- c. Install the downloaded release package with the following command, replacing platformand-version-specific-package-name with the name of the downloaded RPM package:

```
$> sudo yum localinstall platform-and-version-specific-package-name.rpm
```

For an EL6-based system, the command is in the form of:

```
$> sudo yum localinstall mysql57-community-release-el6-{version-number}.noarch.rpm
```

For an EL7-based system:

```
$> sudo yum localinstall mysql57-community-release-el7-{version-number}.noarch.rpm
```

For an EL8-based system:

```
$> sudo yum localinstall mysql57-community-release-el8-{version-number}.noarch.rpm
```

For Fedora:

MySQL 5.7 does not support Fedora; support was removed in MySQL 5.7.30. For details, see the [MySQL Product Support EOL Announcements.](https://www.mysql.com/support/eol-notice.md)

The installation command adds the MySQL Yum repository to your system's repository list and downloads the GnuPG key to check the integrity of the software packages. See [Section 2.1.4.2,](#page-87-0) ["Signature Checking Using GnuPG"](#page-87-0) for details on GnuPG key checking.

You can check that the MySQL Yum repository has been successfully added by the following command:

```
$> yum repolist enabled | grep "mysql.*-community.*"
```

![](_page_168_Picture_16.jpeg)

#### **Note**

Once the MySQL Yum repository is enabled on your system, any systemwide update by the yum update command upgrades MySQL packages on your system and replaces any native third-party packages, if Yum finds replacements for them in the MySQL Yum repository; see Section 2.10.5, "Upgrading MySQL with the MySQL Yum Repository" and, for a discussion on some possible effects of that on your system, see Upgrading the Shared Client Libraries.

## **Selecting a Release Series** 2.

When using the MySQL Yum repository, the latest GA series (currently MySQL 5.7) is selected for installation by default. If this is what you want, you can skip to the next step, [Installing MySQL.](#page-169-0)

Within the MySQL Yum repository, different release series of the MySQL Community Server are hosted in different subrepositories. The subrepository for the latest GA series (currently MySQL 5.7) is enabled by default, and the subrepositories for all other series (for example, the MySQL 5.6 series) are disabled by default. Use this command to see all the subrepositories in the MySQL Yum repository, and see which of them are enabled or disabled:

```
$> yum repolist all | grep mysql
```

To install the latest release from the latest GA series, no configuration is needed. To install the latest release from a specific series other than the latest GA series, disable the subrepository

for the latest GA series and enable the subrepository for the specific series before running the installation command. If your platform supports yum-config-manager, you can do that by issuing these commands, which disable the subrepository for the 5.7 series and enable the one for the 5.6 series:

```
$> sudo yum-config-manager --disable mysql57-community
$> sudo yum-config-manager --enable mysql56-community
```

For Fedora platforms:

```
$> sudo dnf config-manager --disable mysql57-community
$> sudo dnf config-manager --enable mysql56-community
```

Besides using yum-config-manager or the dnf config-manager command, you can also select a release series by editing manually the /etc/yum.repos.d/mysql-community.repo file. This is a typical entry for a release series' subrepository in the file:

```
[mysql57-community]
name=MySQL 5.7 Community Server
baseurl=http://repo.mysql.com/yum/mysql-5.7-community/el/6/$basearch/
enabled=1
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-mysql
```

Find the entry for the subrepository you want to configure, and edit the enabled option. Specify enabled=0 to disable a subrepository, or enabled=1 to enable a subrepository. For example, to install MySQL 5.6, make sure you have enabled=0 for the above subrepository entry for MySQL 5.7, and have enabled=1 for the entry for the 5.6 series:

```
# Enable to use MySQL 5.6
[mysql56-community]
name=MySQL 5.6 Community Server
baseurl=http://repo.mysql.com/yum/mysql-5.6-community/el/6/$basearch/
enabled=1
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-mysql
```

You should only enable subrepository for one release series at any time. When subrepositories for more than one release series are enabled, the latest series is used by Yum.

Verify that the correct subrepositories have been enabled and disabled by running the following command and checking its output:

```
$> yum repolist enabled | grep mysql
```

## **Disabling the Default MySQL Module** 3.

(EL8 systems only) EL8-based systems such as RHEL8 and Oracle Linux 8 include a MySQL module that is enabled by default. Unless this module is disabled, it masks packages provided by MySQL repositories. To disable the included module and make the MySQL repository packages visible, use the following command (for dnf-enabled systems, replace yum in the command with dnf):

```
$> sudo yum module disable mysql
```

## <span id="page-169-0"></span>4. **Installing MySQL**

Install MySQL by the following command:

```
$> sudo yum install mysql-community-server
```

This installs the package for MySQL server (mysql-community-server) and also packages for the components required to run the server, including packages for the client (mysql-communityclient), the common error messages and character sets for client and server (mysqlcommunity-common), and the shared client libraries (mysql-community-libs).

## **Starting the MySQL Server** 5.

Start the MySQL server with the following command:

```
$> sudo service mysqld start
Starting mysqld:[ OK ]
```

You can check the status of the MySQL server with the following command:

```
$> sudo service mysqld status
mysqld (pid 3066) is running.
```

At the initial start up of the server, the following happens, given that the data directory of the server is empty:

- The server is initialized.
- SSL certificate and key files are generated in the data directory.
- validate\_password is installed and enabled.
- A superuser account 'root'@'localhost is created. A password for the superuser is set and stored in the error log file. To reveal it, use the following command:

```
$> sudo grep 'temporary password' /var/log/mysqld.log
```

Change the root password as soon as possible by logging in with the generated, temporary password and set a custom password for the superuser account:

```
$> mysql -uroot -p 
mysql> ALTER USER 'root'@'localhost' IDENTIFIED BY 'MyNewPass4!';
```

![](_page_170_Picture_15.jpeg)

#### **Note**

validate\_password is installed by default. The default password policy implemented by validate\_password requires that passwords contain at least one uppercase letter, one lowercase letter, one digit, and one special character, and that the total password length is at least 8 characters.

For more information on the postinstallation procedures, see Section 2.9, "Postinstallation Setup and Testing".

<span id="page-170-1"></span>![](_page_170_Picture_19.jpeg)

#### **Note**

Compatibility Information for EL7-based platforms: The following RPM packages from the native software repositories of the platforms are incompatible with the package from the MySQL Yum repository that installs the MySQL server. Once you have installed MySQL using the MySQL Yum repository, you cannot install these packages (and vice versa).

• akonadi-mysql

### <span id="page-170-0"></span>**Installing Additional MySQL Products and Components with Yum**

You can use Yum to install and manage individual components of MySQL. Some of these components are hosted in sub-repositories of the MySQL Yum repository: for example, the MySQL Connectors are to be found in the MySQL Connectors Community sub-repository, and the MySQL Workbench in MySQL Tools Community. You can use the following command to list the packages for all the MySQL components available for your platform from the MySQL Yum repository:

```
$> sudo yum --disablerepo=\* --enablerepo='mysql*-community*' list available
```

Install any packages of your choice with the following command, replacing package-name with name of the package:

```
$> sudo yum install package-name
```

For example, to install MySQL Workbench on Fedora:

```
$> sudo dnf install mysql-workbench-community
```

To install the shared client libraries:

```
$> sudo yum install mysql-community-libs
```

## **Updating MySQL with Yum**

Besides installation, you can also perform updates for MySQL products and components using the MySQL Yum repository. See Section 2.10.5, "Upgrading MySQL with the MySQL Yum Repository" for details.

## <span id="page-171-0"></span>**2.5.2 Replacing a Third-Party Distribution of MySQL Using the MySQL Yum Repository**

For supported Yum-based platforms (see [Section 2.5.1, "Installing MySQL on Linux Using the MySQL](#page-167-0) [Yum Repository"](#page-167-0), for a list), you can replace a third-party distribution of MySQL with the latest GA release (from the MySQL 5.7 series currently) from the MySQL Yum repository. According to how your third-party distribution of MySQL was installed, there are different steps to follow:

## **Replacing a Native Third-Party Distribution of MySQL**

If you have installed a third-party distribution of MySQL from a native software repository (that is, a software repository provided by your own Linux distribution), follow these steps:

### **Backing Up Your Database** 1.

To avoid loss of data, always back up your database before trying to replace your MySQL installation using the MySQL Yum repository. See Chapter 7, Backup and Recovery, on how to back up your database.

## **Adding the MySQL Yum Repository** 2.

Add the MySQL Yum repository to your system's repository list by following the instructions given in [Adding the MySQL Yum Repository.](#page-167-1)

### **Replacing the Native Third-Party Distribution by a Yum Update or a DNF Upgrade** 3.

By design, the MySQL Yum repository replaces your native third-party MySQL with the latest GA release (from the MySQL 5.7 series currently) from the MySQL Yum repository when you perform a yum update command on the system, or a yum update mysql-server.

After updating MySQL using the Yum repository, applications compiled with older versions of the shared client libraries should continue to work. However, if you want to recompile applications and dynamically link them with the updated libraries, see Upgrading the Shared Client Libraries, for some special considerations.

## **Replacing a Nonnative Third-Party Distribution of MySQL**

If you have installed a third-party distribution of MySQL from a nonnative software repository (that is, a software repository not provided by your own Linux distribution), follow these steps:

## **Backing Up Your Database** 1.

To avoid loss of data, always back up your database before trying to replace your MySQL installation using the MySQL Yum repository. See Chapter 7, Backup and Recovery, on how to back up your database.

## **Stopping Yum from Receiving MySQL Packages from Third-Party, Nonnative** 2. **Repositories**

Before you can use the MySQL Yum repository for installing MySQL, you must stop your system from receiving MySQL packages from any third-party, nonnative Yum repositories.

For example, if you have installed MariaDB using their own software repository, get a list of the installed MariaDB packages using the following command:

```
$> yum list installed mariadb\*
MariaDB-common.i686 10.0.4-1 @mariadb
MariaDB-compat.i686 10.0.4-1 @mariadb
MariaDB-server.i686 10.0.4-1 @mariadb
```

From the command output, we can identify the installed packages (MariaDB-common, MariaDBcompat, and MariaDB-server) and the source of them (a nonnative software repository named mariadb).

As another example, if you have installed Percona using their own software repository, get a list of the installed Percona packages using the following command:

```
$> yum list installed Percona\*
Percona-Server-client-55.i686 5.5.39-rel36.0.el6 @percona-release-i386
Percona-Server-server-55.i686 5.5.39-rel36.0.el6 @percona-release-i386
Percona-Server-shared-55.i686 5.5.39-rel36.0.el6 @percona-release-i386
percona-release.noarch 0.1-3 @/percona-release-0.1-3.noarch
```

From the command output, we can identify the installed packages (Percona-Server-client, Percona-Server-server, Percona-Server-shared, and percona-release.noarch) and the source of them (a nonnative software repository named percona-release).

If you are not sure which third-party MySQL fork you have installed, this command should reveal it and list the RPM packages installed for it, as well as the third-party repository that supplies the packages:

```
$> yum --disablerepo=\* provides mysql\*
```

The next step is to stop Yum from receiving packages from the nonnative repository. If the yumconfig-manager utility is supported on your platform, you can, for example, use this command for stopping delivery from MariaDB:

```
$> sudo yum-config-manager --disable mariadb
```

Use this command for stopping delivery from Percona:

```
$> sudo yum-config-manager --disable percona-release
```

You can perform the same task by removing the entry for the software repository existing in one of the repository files under the /etc/yum.repos.d/ directory. This is how the entry typically looks for MariaDB:

```
[mariadb] name = MariaDB
 baseurl = [base URL for repository]
 gpgkey = [URL for GPG key]
```

gpgcheck =1

The entry is usually found in the file /etc/yum.repos.d/MariaDB.repo for MariaDB—delete the file, or remove entry from it (or from the file in which you find the entry).

![](_page_173_Picture_3.jpeg)

#### **Note**

This step is not necessary for an installation that was configured with a Yum repository release package (like Percona) if you are going to remove the release package (percona-release.noarch for Percona), as shown in the uninstall command for Percona in Step 3 below.

## **Uninstalling the Nonnative Third-Party MySQL Distribution of MySQL** 3.

The nonnative third-party MySQL distribution must first be uninstalled before you can use the MySQL Yum repository to install MySQL. For the MariaDB packages found in Step 2 above, uninstall them with the following command:

\$> **sudo yum remove MariaDB-common MariaDB-compat MariaDB-server**

For the Percona packages we found in Step 2 above:

\$> **sudo yum remove Percona-Server-client-55 Percona-Server-server-55 \ Percona-Server-shared-55.i686 percona-release**

## 4. **Installing MySQL with the MySQL Yum Repository**

Then, install MySQL with the MySQL Yum repository by following the instructions given in [Section 2.5.1, "Installing MySQL on Linux Using the MySQL Yum Repository":](#page-167-0) .

![](_page_173_Picture_13.jpeg)

#### **Important**

If you have chosen to replace your third-party MySQL distribution with a newer version of MySQL from the MySQL Yum repository, remember to run mysql\_upgrade after the server starts, to check and possibly resolve any incompatibilities between the old data and the upgraded software. mysql\_upgrade also performs other functions; see Section 4.4.7, "mysql\_upgrade — Check and Upgrade MySQL Tables" for details.

For EL7-based platforms: See [Compatibility Information for EL7-based](#page-170-1) [platforms \[143\]](#page-170-1).

## <span id="page-173-0"></span>**2.5.3 Installing MySQL on Linux Using the MySQL APT Repository**

The MySQL APT repository provides deb packages for installing and managing the MySQL server, client, and other components on the current Debian and Ubuntu releases.

Instructions for using the MySQL APT Repository are available in [A Quick Guide to Using the MySQL](https://dev.mysql.com/doc/mysql-apt-repo-quick-guide/en/) [APT Repository](https://dev.mysql.com/doc/mysql-apt-repo-quick-guide/en/).

## <span id="page-173-1"></span>**2.5.4 Installing MySQL on Linux Using the MySQL SLES Repository**

The MySQL SLES repository provides RPM packages for installing and managing the MySQL server, client, and other components on SUSE Enterprise Linux Server.

Instructions for using the MySQL SLES repository are available in [A Quick Guide to Using the MySQL](https://dev.mysql.com/doc/mysql-sles-repo-quick-guide/en/) [SLES Repository](https://dev.mysql.com/doc/mysql-sles-repo-quick-guide/en/).

## <span id="page-173-2"></span>**2.5.5 Installing MySQL on Linux Using RPM Packages from Oracle**

The recommended way to install MySQL on RPM-based Linux distributions is by using the RPM packages provided by Oracle. There are two sources for obtaining them, for the Community Edition of MySQL:

- From the MySQL software repositories:
  - The MySQL Yum repository (see [Section 2.5.1, "Installing MySQL on Linux Using the MySQL Yum](#page-167-0) [Repository"](#page-167-0) for details).
  - The MySQL SLES repository (see [Section 2.5.4, "Installing MySQL on Linux Using the MySQL](#page-173-1) [SLES Repository"](#page-173-1) for details).
- From the [Download MySQL Community Server](https://dev.mysql.com/downloads/mysql/) page in the [MySQL Developer Zone](https://dev.mysql.com/).

![](_page_174_Picture_6.jpeg)

#### **Note**

RPM distributions of MySQL are also provided by other vendors. Be aware that they may differ from those built by Oracle in features, capabilities, and conventions (including communication setup), and that the installation instructions in this manual do not necessarily apply to them. The vendor's instructions should be consulted instead.

If you have such a third-party distribution of MySQL running on your system and now want to migrate to Oracle's distribution using the RPM packages downloaded from the MySQL Developer Zone, see [Compatibility with RPM](#page-177-0) [Packages from Other Vendors](#page-177-0) below. The preferred method of migration, however, is to use the [MySQL Yum repository](#page-167-0) or [MySQL SLES repository](#page-173-1).

RPM packages for MySQL are listed in the following tables:

**Table 2.9 RPM Packages for MySQL Community Edition**

| Package Name                   | Summary                                                                          |
|--------------------------------|----------------------------------------------------------------------------------|
| mysql-community-server         | Database server and related tools                                                |
| mysql-community-client         | MySQL client applications and tools                                              |
| mysql-community-common         | Common files for server and client libraries                                     |
| mysql-community-devel          | Development header files and libraries for MySQL<br>database client applications |
| mysql-community-libs           | Shared libraries for MySQL database client<br>applications                       |
| mysql-community-libs-compat    | Shared compatibility libraries for previous MySQL<br>installations               |
| mysql-community-embedded       | MySQL embedded library                                                           |
| mysql-community-embedded-devel | Development header files and libraries for MySQL<br>as an embeddable library     |
| mysql-community-test           | Test suite for the MySQL server                                                  |

**Table 2.10 RPM Packages for the MySQL Enterprise Edition**

| Package Name            | Summary                                                                          |
|-------------------------|----------------------------------------------------------------------------------|
| mysql-commercial-server | Database server and related tools                                                |
| mysql-commercial-client | MySQL client applications and tools                                              |
| mysql-commercial-common | Common files for server and client libraries                                     |
| mysql-commercial-devel  | Development header files and libraries for MySQL<br>database client applications |

| Package Name                    | Summary                                                                      |
|---------------------------------|------------------------------------------------------------------------------|
| mysql-commercial-libs           | Shared libraries for MySQL database client<br>applications                   |
| mysql-commercial-libs-compat    | Shared compatibility libraries for previous MySQL<br>installations           |
| mysql-commercial-embedded       | MySQL embedded library                                                       |
| mysql-commercial-embedded-devel | Development header files and libraries for MySQL<br>as an embeddable library |
| mysql-commercial-test           | Test suite for the MySQL server                                              |

The full names for the RPMs have the following syntax:

packagename-version-distribution-arch.rpm

The distribution and arch values indicate the Linux distribution and the processor type for which the package was built. See the table below for lists of the distribution identifiers:

**Table 2.11 MySQL Linux RPM Package Distribution Identifiers**

| distribution Value                                                                | Intended Use                                                                                                                                                |
|-----------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------|
| el{version} where {version} is the major<br>Enterprise Linux version, such as el8 | EL6 (8.0), EL7, EL8, EL9, and EL10-based<br>platforms (for example, the corresponding<br>versions of Oracle Linux, Red Hat Enterprise<br>Linux, and CentOS) |
| sles12                                                                            | SUSE Linux Enterprise Server 12                                                                                                                             |

To see all files in an RPM package (for example, mysql-community-server), use the following command:

\$> **rpm -qpl mysql-community-server-version-distribution-arch.rpm**

The discussion in the rest of this section applies only to an installation process using the RPM packages directly downloaded from Oracle, instead of through a MySQL repository.

Dependency relationships exist among some of the packages. If you plan to install many of the packages, you may wish to download the RPM bundle tar file instead, which contains all the RPM packages listed above, so that you need not download them separately.

In most cases, you need to install the mysql-community-server, mysql-community-client, mysql-community-libs, mysql-community-common, and mysql-community-libs-compat packages to get a functional, standard MySQL installation. To perform such a standard, basic installation, go to the folder that contains all those packages (and, preferably, no other RPM packages with similar names), and issue the following command for platforms other than Red Hat Enterprise Linux/Oracle Linux/CentOS:

\$> **sudo yum install mysql-community-{server,client,common,libs}-\***

Replace yum with zypper for SLES.

For Red Hat Enterprise Linux/Oracle Linux/CentOS systems:

```
$> sudo yum install mysql-community-{server,client,common,libs}-* mysql-5.*
```

While it is much preferable to use a high-level package management tool like yum to install the packages, users who prefer direct rpm commands can replace the yum install command with the rpm -Uvh command; however, using rpm -Uvh instead makes the installation process more prone to failure, due to potential dependency issues the installation process might run into.

To install only the client programs, you can skip mysql-community-server in your list of packages to install; issue the following command for platforms other than Red Hat Enterprise Linux/Oracle Linux/ CentOS:

```
$> sudo yum install mysql-community-{client,common,libs}-*
```

Replace yum with zypper for SLES.

For Red Hat Enterprise Linux/Oracle Linux/CentOS systems:

```
$> sudo yum install mysql-community-{client,common,libs}-* mysql-5.*
```

A standard installation of MySQL using the RPM packages result in files and resources created under the system directories, shown in the following table.

**Table 2.12 MySQL Installation Layout for Linux RPM Packages from the MySQL Developer Zone**

<span id="page-176-0"></span>

| Files or Resources                                                                    | Location                                                                                                 |
|---------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------|
| Client programs and scripts                                                           | /usr/bin                                                                                                 |
| mysqld server                                                                         | /usr/sbin                                                                                                |
| Configuration file                                                                    | /etc/my.cnf                                                                                              |
| Data directory                                                                        | /var/lib/mysql                                                                                           |
| Error log file                                                                        | For RHEL, Oracle Linux, CentOS or Fedora<br>platforms: /var/log/mysqld.log                               |
|                                                                                       | For SLES: /var/log/mysql/mysqld.log                                                                      |
| Value of secure_file_priv                                                             | /var/lib/mysql-files                                                                                     |
| System V init script                                                                  | For RHEL, Oracle Linux, CentOS or Fedora<br>platforms: /etc/init.d/mysqld<br>For SLES: /etc/init.d/mysql |
| Systemd service                                                                       | For RHEL, Oracle Linux, CentOS or Fedora<br>platforms: mysqld<br>For SLES: mysql                         |
| Pid file                                                                              | /var/run/mysql/mysqld.pid                                                                                |
| Socket                                                                                | /var/lib/mysql/mysql.sock                                                                                |
| Keyring directory                                                                     | /var/lib/mysql-keyring                                                                                   |
| Unix manual pages                                                                     | /usr/share/man                                                                                           |
| Include (header) files                                                                | /usr/include/mysql                                                                                       |
| Libraries                                                                             | /usr/lib/mysql                                                                                           |
| Miscellaneous support files (for example, error<br>messages, and character set files) | /usr/share/mysql                                                                                         |

The installation also creates a user named mysql and a group named mysql on the system.

![](_page_176_Picture_9.jpeg)

#### **Notes**

• The mysql user is created using the -r and -s /bin/false options of the useradd command, so that it does not have login permissions to your server host (see [Creating the mysql User and Group](https://dev.mysql.com/doc/mysql-secure-deployment-guide/5.7/en/secure-deployment-install.md#secure-deployment-mysql-user) for details). To switch to the mysql user on your OS, use the --shell=/bin/bash option for the su command:

```
su - mysql --shell=/bin/bash
```

• Installation of previous versions of MySQL using older packages might have created a configuration file named /usr/my.cnf. It is highly recommended that you examine the contents of the file and migrate the desired settings inside to the file /etc/my.cnf file, then remove /usr/my.cnf.

MySQL is not automatically started at the end of the installation process. For Red Hat Enterprise Linux, Oracle Linux, CentOS, and Fedora systems, use the following command to start MySQL:

\$> **sudo service mysqld start**

For SLES systems, the command is the same, but the service name is different:

\$> **sudo service mysql start**

If the operating system is systemd enabled, standard service commands such as stop, start, status and restart should be used to manage the MySQL server service. The mysqld service is enabled by default, and it starts at system reboot. Notice that certain things might work differently on systemd platforms: for example, changing the location of the data directory might cause issues. See [Section 2.5.10, "Managing MySQL Server with systemd"](#page-192-1) for additional information.

During an upgrade installation using RPM and DEB packages, if the MySQL server is running when the upgrade occurs then the MySQL server is stopped, the upgrade occurs, and the MySQL server is restarted. One exception: if the edition also changes during an upgrade (such as community to commercial, or vice-versa), then MySQL server is not restarted.

At the initial start up of the server, the following happens, given that the data directory of the server is empty:

- The server is initialized.
- An SSL certificate and key files are generated in the data directory.
- validate\_password is installed and enabled.
- A superuser account 'root'@'localhost' is created. A password for the superuser is set and stored in the error log file. To reveal it, use the following command for RHEL, Oracle Linux, CentOS, and Fedora systems:

\$> **sudo grep 'temporary password' /var/log/mysqld.log**

Use the following command for SLES systems:

\$> **sudo grep 'temporary password' /var/log/mysql/mysqld.log**

The next step is to log in with the generated, temporary password and set a custom password for the superuser account:

\$> **mysql -uroot -p** 

mysql> **ALTER USER 'root'@'localhost' IDENTIFIED BY 'MyNewPass4!';**

![](_page_177_Picture_18.jpeg)

#### **Note**

validate\_password is installed by default. The default password policy implemented by validate\_password requires that passwords contain at least one uppercase letter, one lowercase letter, one digit, and one special character, and that the total password length is at least 8 characters.

If something goes wrong during installation, you might find debug information in the error log file /var/ log/mysqld.log.

For some Linux distributions, it might be necessary to increase the limit on number of file descriptors available to mysqld. See Section B.3.2.16, "File Not Found and Similar Errors"

<span id="page-177-0"></span>**Compatibility with RPM Packages from Other Vendors.** If you have installed packages for MySQL from your Linux distribution's local software repository, it is much preferable to install the new, directly-downloaded packages from Oracle using the package management system of your platform (yum, dnf, or zypper), as described above. The command replaces old packages with new ones to ensure compatibility of old applications with the new installation; for example, the old mysqllibs package is replaced with the mysql-community-libs-compat package, which provides a replacement-compatible client library for applications that were using your older MySQL installation. If there was an older version of mysql-community-libs-compat on the system, it also gets replaced.

If you have installed third-party packages for MySQL that are NOT from your Linux distribution's local software repository (for example, packages directly downloaded from a vendor other than Oracle), you should uninstall all those packages before installing the new, directly-downloaded packages from Oracle. This is because conflicts may arise between those vendor's RPM packages and Oracle's: for example, a vendor's convention about which files belong with the server and which belong with the client library may differ from that used for Oracle packages. Attempts to install an Oracle RPM may then result in messages saying that files in the RPM to be installed conflict with files from an installed package.

**Installing Client Libraries from Multiple MySQL Versions.** It is possible to install multiple client library versions, such as for the case that you want to maintain compatibility with older applications linked against previous libraries. To install an older client library, use the --oldpackage option with rpm. For example, to install mysql-community-libs-5.5 on an EL6 system that has libmysqlclient.20 from MySQL 5.7, use a command like this:

```
$> rpm --oldpackage -ivh mysql-community-libs-5.5.50-2.el6.x86_64.rpm
```

**Debug Package.** A special variant of MySQL Server compiled with the debug package has been included in the server RPM packages. It performs debugging and memory allocation checks and produces a trace file when the server is running. To use that debug version, start MySQL with / usr/sbin/mysqld-debug, instead of starting it as a service or with /usr/sbin/mysqld. See Section 5.8.3, "The DBUG Package" for the debug options you can use.

![](_page_178_Picture_6.jpeg)

#### **Note**

The default plugin directory for debug builds changed from /usr/lib64/ mysql/plugin to /usr/lib64/mysql/plugin/debug in 5.7.21. Previously, it was necessary to change plugin\_dir to /usr/lib64/mysql/ plugin/debug for debug builds.

**Rebuilding RPMs from source SRPMs.** Source code SRPM packages for MySQL are available for download. They can be used as-is to rebuild the MySQL RPMs with the standard rpmbuild tool chain.

**root passwords for pre-GA releases.** For MySQL 5.7.4 and 5.7.5, the initial random root password is written to the .mysql\_secret file in the directory named by the HOME environment variable. When trying to access the file, bear in mind that depending on operating system, using a command such as sudo may cause the value of HOME to refer to the home directory of the root system user . .mysql\_secret is created with mode 600 to be accessible only to the system user for whom it is created. Before MySQL 5.7.4, the accounts (including root) created in the MySQL grant tables for an RPM installation initially have no passwords; after starting the server, you should assign passwords to them using the instructions in Section 2.9, "Postinstallation Setup and Testing"."

## <span id="page-178-0"></span>**2.5.6 Installing MySQL on Linux Using Debian Packages from Oracle**

Oracle provides Debian packages for installing MySQL on Debian or Debian-like Linux systems. The packages are available through two different channels:

- The [MySQL APT Repository](https://dev.mysql.com/downloads/repo/apt/). This is the preferred method for installing MySQL on Debian-like systems, as it provides a simple and convenient way to install and update MySQL products. For details, see [Section 2.5.3, "Installing MySQL on Linux Using the MySQL APT Repository"](#page-173-0).
- The [MySQL Developer Zone's Download Area](https://dev.mysql.com/downloads/). For details, see [Section 2.1.3, "How to Get MySQL".](#page-86-0) The following are some information on the Debian packages available there and the instructions for installing them:

• Various Debian packages are provided in the MySQL Developer Zone for installing different components of MySQL on different Debian or Ubuntu platforms. The preferred method is to use the tarball bundle, which contains the packages needed for a basic setup of MySQL. The tarball bundles have names in the format of mysql-server\_MVER-DVER\_CPU.deb-bundle.tar. MVER is the MySQL version and DVER is the Linux distribution version. The CPU value indicates the processor type or family for which the package is built, as shown in the following table:

**Table 2.13 MySQL Debian and Ubuntu Installation Packages CPU Identifiers**

| CPU Value | Intended Processor Type or Family   |
|-----------|-------------------------------------|
| i386      | Pentium processor or better, 32 bit |
| amd64     | 64-bit x86 processor                |

• After downloading the tarball, unpack it with the following command:

```
$> tar -xvf mysql-server_MVER-DVER_CPU.deb-bundle.tar
```

• You may need to install the libaio library if it is not already present on your system:

```
$> sudo apt-get install libaio1
```

• Preconfigure the MySQL server package with the following command:

```
$> sudo dpkg-preconfigure mysql-community-server_*.deb
```

You are asked to provide a password for the root user for your MySQL installation. You might also be asked other questions regarding the installation.

![](_page_179_Picture_11.jpeg)

#### **Important**

Make sure you remember the root password you set. Users who want to set a password later can leave the **password** field blank in the dialogue box and just press **OK**; in that case, root access to the server is authenticated using the MySQL Socket Peer-Credential Authentication Plugin for connections using a Unix socket file. You can set the root password later using mysql\_secure\_installation.

• For a basic installation of the MySQL server, install the database common files package, the client package, the client metapackage, the server package, and the server metapackage (in that order); you can do that with a single command:

```
$> sudo dpkg -i mysql-{common,community-client,client,community-server,server}_*.deb
```

If you are being warned of unmet dependencies by dpkg, you can fix them using apt-get:

```
sudo apt-get -f install
```

Here are where the files are installed on the system:

- All configuration files (like my.cnf) are under /etc/mysql
- All binaries, libraries, headers, etc., are under /usr/bin and /usr/sbin
- The data directory is /var/lib/mysql

![](_page_179_Picture_22.jpeg)

#### **Note**

Debian distributions of MySQL are also provided by other vendors. Be aware that they may differ from those built by Oracle in features, capabilities, and conventions (including communication setup), and that the instructions in this manual do not necessarily apply to installing them. The vendor's instructions should be consulted instead.

## <span id="page-180-0"></span>**2.5.7 Deploying MySQL on Linux with Docker**

The Docker deployment framework supports easy installation and configuration of MySQL Server. This section explains how to use a MySQL Server Docker image.

You need to have Docker installed on your system before you can use a MySQL Server Docker image. See [Install Docker](https://docs.docker.com/engine/installation/) for instructions.

![](_page_180_Picture_5.jpeg)

#### **Warning**

Beware of the security concerns with running Docker containers. See [Docker](https://docs.docker.com/engine/security/) [security](https://docs.docker.com/engine/security/) for details.

The instructions for using the MySQL Docker container are divided into two sections.

## **2.5.7.1 Basic Steps for MySQL Server Deployment with Docker**

![](_page_180_Picture_10.jpeg)

#### **Warning**

The MySQL Docker images maintained by the MySQL team are built specifically for Linux platforms. Other platforms are not supported, and users using these MySQL Docker images on them are doing so at their own risk. See [the discussion here](#page-189-1) for some known limitations for running these containers on non-Linux operating systems.

- [Downloading a MySQL Server Docker Image](#page-180-1)
- [Starting a MySQL Server Instance](#page-182-0)
- [Connecting to MySQL Server from within the Container](#page-182-1)
- [Container Shell Access](#page-183-0)
- [Stopping and Deleting a MySQL Container](#page-183-1)
- [Upgrading a MySQL Server Container](#page-183-2)
- [More Topics on Deploying MySQL Server with Docker](#page-184-0)

#### <span id="page-180-1"></span>**Downloading a MySQL Server Docker Image**

![](_page_180_Picture_21.jpeg)

#### **Important**

For users of MySQL Enterprise Edition: A subscription is required to use the Docker images for MySQL Enterprise Edition. Subscriptions work by a Bring Your Own License model; see [How to Buy MySQL Products and Services](https://www.mysql.com/buy-mysql/) for details.

Downloading the server image in a separate step is not strictly necessary; however, performing this step before you create your Docker container ensures your local image is up to date. To download the MySQL Community Edition image, run this command:

**docker pull mysql/mysql-server:tag**

The tag is the label for the image version you want to pull (for example, 5.6, 5.7, 8.0, or latest). If **:tag** is omitted, the latest label is used, and the image for the latest GA version of MySQL Community Server is downloaded. Refer to the list of tags for available versions on the [mysql/mysql](https://hub.docker.com/r/mysql/mysql-server/tags/)[server page in the Docker Hub.](https://hub.docker.com/r/mysql/mysql-server/tags/)

To download the MySQL Community Edition image from the Oracle Container Registry (OCR), run this command:

```
docker pull container-registry.oracle.com/mysql/mysql-server:tag
```

To download the MySQL Enterprise Edition image from the OCR, you need to first accept the license agreement on the OCR and log in to the container repository with your Docker client:

- Visit the OCR at<https://container-registry.oracle.com/> and choose **MySQL**.
- Under the list of MySQL repositories, choose enterprise-server.
- If you have not signed in to the OCR yet, click the **Sign in** button on the right of the page, and then enter your Oracle account credentials when prompted to.
- Follow the instructions on the right of the page to accept the license agreement.
- Log in to the OCR with your Docker client (the docker command) using the docker login command:

```
# docker login container-registry.oracle.com 
Username: Oracle-Account-ID
Password: password
Login successful.
```

Download the Docker image for MySQL Enterprise Edition from the OCR with this command:

```
docker pull container-registry.oracle.com/mysql/enterprise-server:tag
```

There are different choices for **tag**, corresponding to different versions of MySQL Docker images provided by the OCR:

- 8.0, 8.0.x (x is the latest version number in the 8.0 series), latest: MySQL 8.0, the latest GA
- 5.7, 5.7.y (y is the latest version number in the 5.7 series): MySQL 5.7

To download the MySQL Enterprise Edition image, visit the [My Oracle Support](https://support.oracle.com/) website, sign in to your Oracle account, and perform these steps once you are on the landing page:

- Select the **Patches and Updates** tab.
- Go to the **Patch Search** region and, on the **Search** tab, switch to the **Product or Family (Advanced)** subtab.
- Enter "MySQL Server" for the **Product** field, and the desired version number in the **Release** field.
- Use the dropdowns for additional filters to select **Description**—**contains**, and enter "Docker" in the text field.

The following figure shows the search settings for a MySQL Enterprise Edition image:

![](_page_181_Picture_20.jpeg)

- Click the **Search** button and, from the result list, select the version you want, and click the **Download** button.
- In the **File Download** dialogue box that appears, click and download the .zip file for the Docker image.

Unzip the downloaded .zip archive to obtain the tarball inside (mysql-enterpriseserver-version.tar), and then load the image by running this command:

```
docker load -i mysql-enterprise-server-version.tar
```

You can list downloaded Docker images with this command:

```
$> docker images
REPOSITORY TAG IMAGE ID CREATED SIZE
mysql/mysql-server latest 3157d7f55f8d 4 weeks ago 241MB
```

#### <span id="page-182-0"></span>**Starting a MySQL Server Instance**

To start a new Docker container for a MySQL Server, use the following command:

```
docker run --name=container_name -d image_name:tag
```

The image name can be obtained using the docker images command, as explained in [Downloading](#page-180-1) [a MySQL Server Docker Image.](#page-180-1) The --name option, for supplying a custom name for your server container, is optional; if no container name is supplied, a random one is generated.

For example, to start a new Docker container for the MySQL Community Server, use this command:

```
docker run --name=mysql1 -d mysql/mysql-server:5.7
```

To start a new Docker container for the MySQL Enterprise Server with a Docker image downloaded from the OCR, use this command:

```
docker run --name=mysql1 -d container-registry.oracle.com/mysql/enterprise-server:5.7
```

To start a new Docker container for the MySQL Enterprise Server with a Docker image downloaded from My Oracle Support, use this command:

```
docker run --name=mysql1 -d mysql/enterprise-server:5.7
```

If the Docker image of the specified name and tag has not been downloaded by an earlier docker pull or docker run command, the image is now downloaded. Initialization for the container begins, and the container appears in the list of running containers when you run the docker ps command. For example:

```
$> docker ps
CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES
a24888f0d6f4 mysql/mysql-server "/entrypoint.sh my..." 14 seconds ago Up 13 seconds (health: starting) 3306/tcp, 33060/tcp mysql1
```

The container initialization might take some time. When the server is ready for use, the STATUS of the container in the output of the docker ps command changes from (health: starting) to (healthy).

The -d option used in the docker run command above makes the container run in the background. Use this command to monitor the output from the container:

```
docker logs mysql1
```

Once initialization is finished, the command's output is going to contain the random password generated for the root user; check the password with, for example, this command:

```
$> docker logs mysql1 2>&1 | grep GENERATED
GENERATED ROOT PASSWORD: Axegh3kAJyDLaRuBemecis&EShOs
```

#### <span id="page-182-1"></span>**Connecting to MySQL Server from within the Container**

Once the server is ready, you can run the mysql client within the MySQL Server container you just started, and connect it to the MySQL Server. Use the docker exec -it command to start a mysql client inside the Docker container you have started, like the following:

```
docker exec -it mysql1 mysql -uroot -p
```

When asked, enter the generated root password (see the last step in [Starting a MySQL Server](#page-182-0) [Instance](#page-182-0) above on how to find the password). Because the [MYSQL\\_ONETIME\\_PASSWORD](#page-188-0) option is true by default, after you have connected a mysql client to the server, you must reset the server root password by issuing this statement:

```
mysql> ALTER USER 'root'@'localhost' IDENTIFIED BY 'password';
```

Substitute password with the password of your choice. Once the password is reset, the server is ready for use.

### <span id="page-183-0"></span>**Container Shell Access**

To have shell access to your MySQL Server container, use the docker exec -it command to start a bash shell inside the container:

```
$> docker exec -it mysql1 bash
bash-4.2#
```

You can then run Linux commands inside the container. For example, to view contents in the server's data directory inside the container, use this command:

```
bash-4.2# ls /var/lib/mysql
auto.cnf ca.pem client-key.pem ib_logfile0 ibdata1 mysql mysql.sock.lock private_key.pem server-cert.pem sys
ca-key.pem client-cert.pem ib_buffer_pool ib_logfile1 ibtmp1 mysql.sock performance_schema public_key.pem server-key.pem
```

### <span id="page-183-1"></span>**Stopping and Deleting a MySQL Container**

To stop the MySQL Server container we have created, use this command:

```
docker stop mysql1
```

docker stop sends a SIGTERM signal to the mysqld process, so that the server is shut down gracefully.

Also notice that when the main process of a container (mysqld in the case of a MySQL Server container) is stopped, the Docker container stops automatically.

To start the MySQL Server container again:

```
docker start mysql1
```

To stop and start again the MySQL Server container with a single command:

```
docker restart mysql1
```

To delete the MySQL container, stop it first, and then use the docker rm command:

```
docker stop mysql1
docker rm mysql1
```

If you want the [Docker volume for the server's data directory](#page-185-0) to be deleted at the same time, add the v option to the docker rm command.

### <span id="page-183-2"></span>**Upgrading a MySQL Server Container**

![](_page_183_Picture_22.jpeg)

#### **Important**

- Before performing any upgrade to MySQL, follow carefully the instructions in Section 2.10, "Upgrading MySQL". Among other instructions discussed there, it is especially important to back up your database before the upgrade.
- The instructions in this section require that the server's data and configuration have been persisted on the host. See [Persisting Data and Configuration](#page-185-0) [Changes](#page-185-0) for details.

Follow these steps to upgrade a Docker installation of MySQL 5.6 to 5.7:

• Stop the MySQL 5.6 server (container name is mysql56 in this example):

```
docker stop mysql56
```

- Download the MySQL 5.7 Server Docker image. See instructions in [Downloading a MySQL Server](#page-180-1) [Docker Image](#page-180-1); make sure you use the right tag for MySQL 5.7.
- Start a new MySQL 5.7 Docker container (named mysql57 in this example) with the old server data and configuration (with proper modifications if needed—see Section 2.10, "Upgrading MySQL") that have been persisted on the host (by [bind-mounting](https://docs.docker.com/engine/reference/commandline/service_create/#add-bind-mounts-or-volumes) in this example). For the MySQL Community Server, run this command:

```
docker run --name=mysql57 \
 --mount type=bind,src=/path-on-host-machine/my.cnf,dst=/etc/my.cnf \
 --mount type=bind,src=/path-on-host-machine/datadir,dst=/var/lib/mysql \
 -d mysql/mysql-server:5.7
```

If needed, adjust mysql/mysql-server to the correct image name—for example, replace it with container-registry.oracle.com/mysql/enterprise-server for MySQL Enterprise Edition images downloaded from the OCR, or mysql/enterprise-server for MySQL Enterprise Edition images downloaded from [My Oracle Support](https://support.oracle.com/).

- Wait for the server to finish startup. You can check the status of the server using the docker ps command (see [Starting a MySQL Server Instance](#page-182-0) for how to do that).
- Run the mysql\_upgrade utility in the MySQL 5.7 Server container:

```
docker exec -it mysql57 mysql_upgrade -uroot -p
```

When prompted, enter the root password for your old MySQL 5.6 Server.

• Finish the upgrade by restarting the MySQL 5.7 Server container:

```
docker restart mysql57
```

### <span id="page-184-0"></span>**More Topics on Deploying MySQL Server with Docker**

For more topics on deploying MySQL Server with Docker like server configuration, persisting data and configuration, server error log, and container environment variables, see [Section 2.5.7.2, "More Topics](#page-184-1) [on Deploying MySQL Server with Docker"](#page-184-1).

## <span id="page-184-1"></span>**2.5.7.2 More Topics on Deploying MySQL Server with Docker**

![](_page_184_Picture_16.jpeg)

#### **Note**

Most of the sample commands below have mysql/mysql-server as the Docker image repository when that has to be specified (like with the docker pull and docker run commands); change that if your image is from another repository—for example, replace it with containerregistry.oracle.com/mysql/enterprise-server for MySQL Enterprise Edition images downloaded from the Oracle Container Registry (OCR), or mysql/enterprise-server for MySQL Enterprise Edition images downloaded from [My Oracle Support](https://support.oracle.com/).

- [The Optimized MySQL Installation for Docker](#page-185-1)
- [Configuring the MySQL Server](#page-185-2)
- [Persisting Data and Configuration Changes](#page-185-0)
- [Running Additional Initialization Scripts](#page-186-0)
- [Connect to MySQL from an Application in Another Docker Container](#page-186-1)
- [Server Error Log](#page-187-0)

- [Known Issues](#page-187-1)
- [Docker Environment Variables](#page-187-2)

#### <span id="page-185-1"></span>**The Optimized MySQL Installation for Docker**

Docker images for MySQL are optimized for code size, which means they only include crucial components that are expected to be relevant for the majority of users who run MySQL instances in Docker containers. A MySQL Docker installation is different from a common, non-Docker installation in the following aspects:

- Included binaries are limited to:
  - /usr/bin/my\_print\_defaults
  - /usr/bin/mysql
  - /usr/bin/mysql\_config
  - /usr/bin/mysql\_install\_db
  - /usr/bin/mysql\_tzinfo\_to\_sql
  - /usr/bin/mysql\_upgrade
  - /usr/bin/mysqladmin
  - /usr/bin/mysqlcheck
  - /usr/bin/mysqldump
  - /usr/bin/mysqlpump
  - /usr/sbin/mysqld
- All binaries are stripped; they contain no debug information.

### <span id="page-185-2"></span>**Configuring the MySQL Server**

When you start the MySQL Docker container, you can pass configuration options to the server through the docker run command. For example:

```
docker run --name mysql1 -d mysql/mysql-server:tag --character-set-server=utf8mb4 --collation-server=utf8mb4_col
```

The command starts your MySQL Server with utf8mb4 as the default character set and utf8mb4\_col as the default collation for your databases.

Another way to configure the MySQL Server is to prepare a configuration file and mount it at the location of the server configuration file inside the container. See [Persisting Data and Configuration](#page-185-0) [Changes](#page-185-0) for details.

#### <span id="page-185-0"></span>**Persisting Data and Configuration Changes**

Docker containers are in principle ephemeral, and any data or configuration are expected to be lost if the container is deleted or corrupted (see discussions [here](https://docs.docker.com/engine/userguide/eng-image/dockerfile_best-practices/)). [Docker volumes,](https://docs.docker.com/engine/admin/volumes/volumes/) however, provides a mechanism to persist data created inside a Docker container. At its initialization, the MySQL Server container creates a Docker volume for the server data directory. The JSON output for running the docker inspect command on the container has a Mount key, whose value provides information on the data directory volume:

```
$> docker inspect mysql1
...
 "Mounts": [
 {
 "Type": "volume",
```

```
 "Name": "4f2d463cfc4bdd4baebcb098c97d7da3337195ed2c6572bc0b89f7e845d27652",
 "Source": "/var/lib/docker/volumes/4f2d463cfc4bdd4baebcb098c97d7da3337195ed2c6572bc0b89f7e845d27652/_data",
 "Destination": "/var/lib/mysql",
 "Driver": "local",
 "Mode": "",
 "RW": true,
 "Propagation": ""
 }
 ],
...
```

The output shows that the source folder /var/lib/docker/ volumes/4f2d463cfc4bdd4baebcb098c97d7da3337195ed2c6572bc0b89f7e845d27652/ \_data, in which data is persisted on the host, has been mounted at /var/lib/mysql, the server data directory inside the container.

Another way to preserve data is to [bind-mount](https://docs.docker.com/engine/reference/commandline/service_create/#add-bind-mounts-or-volumes) a host directory using the --mount option when creating the container. The same technique can be used to persist the configuration of the server. The following command creates a MySQL Server container and bind-mounts both the data directory and the server configuration file:

```
docker run --name=mysql1 \
--mount type=bind,src=/path-on-host-machine/my.cnf,dst=/etc/my.cnf \
--mount type=bind,src=/path-on-host-machine/datadir,dst=/var/lib/mysql \
-d mysql/mysql-server:tag
```

The command mounts path-on-host-machine/my.cnf at /etc/my.cnf (the server configuration file inside the container), and path-on-host-machine/datadir at /var/lib/mysql (the data directory inside the container). The following conditions must be met for the bind-mounting to work:

• The configuration file path-on-host-machine/my.cnf must already exist, and it must contain the specification for starting the server using the user mysql:

```
[mysqld]
user=mysql
```

You can also include other server configuration options in the file.

• The data directory path-on-host-machine/datadir must already exist. For server initialization to happen, the directory must be empty. You can also mount a directory prepopulated with data and start the server with it; however, you must make sure you start the Docker container with the same configuration as the server that created the data, and any host files or directories required are mounted when starting the container.

### <span id="page-186-0"></span>**Running Additional Initialization Scripts**

If there are any .sh or .sql scripts you want to run on the database immediately after it has been created, you can put them into a host directory and then mount the directory at /dockerentrypoint-initdb.d/ inside the container. For example:

```
docker run --name=mysql1 \
--mount type=bind,src=/path-on-host-machine/scripts/,dst=/docker-entrypoint-initdb.d/ \
-d mysql/mysql-server:tag
```

## <span id="page-186-1"></span>**Connect to MySQL from an Application in Another Docker Container**

By setting up a Docker network, you can allow multiple Docker containers to communicate with each other, so that a client application in another Docker container can access the MySQL Server in the server container. First, create a Docker network:

```
docker network create my-custom-net
```

Then, when you are creating and starting the server and the client containers, use the --network option to put them on network you created. For example:

```
docker run --name=mysql1 --network=my-custom-net -d mysql/mysql-server
```

**docker run --name=myapp1 --network=my-custom-net -d myapp**

The myapp1 container can then connect to the mysql1 container with the mysql1 hostname and vice versa, as Docker automatically sets up a DNS for the given container names. In the following example, we run the mysql client from inside the myapp1 container to connect to host mysql1 in its own container:

**docker exec -it myapp1 mysql --host=mysql1 --user=myuser --password**

For other networking techniques for containers, see the [Docker container networking](https://docs.docker.com/engine/userguide/networking/) section in the Docker Documentation.

### <span id="page-187-0"></span>**Server Error Log**

When the MySQL Server is first started with your server container, a server error log is NOT generated if either of the following conditions is true:

- A server configuration file from the host has been mounted, but the file does not contain the system variable log\_error (see [Persisting Data and Configuration Changes](#page-185-0) on bind-mounting a server configuration file).
- A server configuration file from the host has not been mounted, but the Docker environment variable [MYSQL\\_LOG\\_CONSOLE](#page-188-1) is true (the variable's default state for MySQL 5.7 server containers is false). The MySQL Server's error log is then redirected to stderr, so that the error log goes into the Docker container's log and is viewable using the docker logs mysqld-container command.

To make MySQL Server generate an error log when either of the two conditions is true, use the - log-error option to [configure the server](#page-185-2) to generate the error log at a specific location inside the container. To persist the error log, mount a host file at the location of the error log inside the container as explained in [Persisting Data and Configuration Changes.](#page-185-0) However, you must make sure your MySQL Server inside its container has write access to the mounted host file.

#### <span id="page-187-1"></span>**Known Issues**

• When using the server system variable audit\_log\_file to configure the audit log file name, use the loose option modifier with it, or Docker will be unable to start the server.

#### <span id="page-187-2"></span>**Docker Environment Variables**

When you create a MySQL Server container, you can configure the MySQL instance by using the - env option (-e in short) and specifying one or more of the following environment variables.

![](_page_187_Picture_14.jpeg)

#### **Notes**

- None of the variables below has any effect if the data directory you mount is not empty, as no server initialization is going to be attempted then (see [Persisting Data and Configuration Changes](#page-185-0) for more details). Any pre-existing contents in the folder, including any old server settings, are not modified during the container startup.
- The boolean variables including [MYSQL\\_RANDOM\\_ROOT\\_PASSWORD](#page-187-3), [MYSQL\\_ONETIME\\_PASSWORD](#page-188-0), [MYSQL\\_ALLOW\\_EMPTY\\_PASSWORD](#page-188-2), and [MYSQL\\_LOG\\_CONSOLE](#page-188-1) are made true by setting them with any strings of nonzero lengths. Therefore, setting them to, for example, "0", "false", or "no" does not make them false, but actually makes them true. This is a known issue of the MySQL Server containers.
- <span id="page-187-3"></span>• [MYSQL\\_RANDOM\\_ROOT\\_PASSWORD](#page-187-3): When this variable is true (which is its default state, unless [MYSQL\\_ROOT\\_PASSWORD](#page-188-3) is set or [MYSQL\\_ALLOW\\_EMPTY\\_PASSWORD](#page-188-2) is set to true), a random password for the server's root user is generated when the Docker container is started. The password is printed to stdout of the container and can be found by looking at the container's log (see [Starting](#page-182-0) [a MySQL Server Instance](#page-182-0)).

- <span id="page-188-0"></span>• [MYSQL\\_ONETIME\\_PASSWORD](#page-188-0): When the variable is true (which is its default state, unless [MYSQL\\_ROOT\\_PASSWORD](#page-188-3) is set or [MYSQL\\_ALLOW\\_EMPTY\\_PASSWORD](#page-188-2) is set to true), the root user's password is set as expired and must be changed before MySQL can be used normally.
- <span id="page-188-4"></span>• [MYSQL\\_DATABASE](#page-188-4): This variable allows you to specify the name of a database to be created on image startup. If a user name and a password are supplied with [MYSQL\\_USER](#page-188-5) and [MYSQL\\_PASSWORD](#page-188-5), the user is created and granted superuser access to this database (corresponding to GRANT ALL). The specified database is created by a CREATE DATABASE IF NOT EXIST statement, so that the variable has no effect if the database already exists.
- <span id="page-188-5"></span>• [MYSQL\\_USER](#page-188-5), [MYSQL\\_PASSWORD](#page-188-5): These variables are used in conjunction to create a user and set that user's password, and the user is granted superuser permissions for the database specified by the [MYSQL\\_DATABASE](#page-188-4) variable. Both [MYSQL\\_USER](#page-188-5) and [MYSQL\\_PASSWORD](#page-188-5) are required for a user to be created—if any of the two variables is not set, the other is ignored. If both variables are set but [MYSQL\\_DATABASE](#page-188-4) is not, the user is created without any privileges.

![](_page_188_Picture_4.jpeg)

#### **Note**

There is no need to use this mechanism to create the root superuser, which is created by default with the password set by either one of the mechanisms discussed in the descriptions for [MYSQL\\_ROOT\\_PASSWORD](#page-188-3) and [MYSQL\\_RANDOM\\_ROOT\\_PASSWORD](#page-187-3), unless [MYSQL\\_ALLOW\\_EMPTY\\_PASSWORD](#page-188-2) is true.

- <span id="page-188-6"></span>• [MYSQL\\_ROOT\\_HOST](#page-188-6): By default, MySQL creates the 'root'@'localhost' account. This account can only be connected to from inside the container as described in [Connecting to MySQL Server](#page-182-1) [from within the Container](#page-182-1). To allow root connections from other hosts, set this environment variable. For example, the value 172.17.0.1, which is the default Docker gateway IP, allows connections from the host machine that runs the container. The option accepts only one entry, but wildcards are allowed (for example, MYSQL\_ROOT\_HOST=172.\*.\*.\* or MYSQL\_ROOT\_HOST=%).
- <span id="page-188-1"></span>• [MYSQL\\_LOG\\_CONSOLE](#page-188-1): When the variable is true (the variable's default state for MySQL 5.7 server containers is false), the MySQL Server's error log is redirected to stderr, so that the error log goes into the Docker container's log and is viewable using the docker logs mysqld-container command.

![](_page_188_Picture_9.jpeg)

#### **Note**

The variable has no effect if a server configuration file from the host has been mounted (see [Persisting Data and Configuration Changes](#page-185-0) on bind-mounting a configuration file).

<span id="page-188-3"></span>• [MYSQL\\_ROOT\\_PASSWORD](#page-188-3): This variable specifies a password that is set for the MySQL root account.

![](_page_188_Picture_13.jpeg)

#### **Warning**

Setting the MySQL root user password on the command line is insecure. As an alternative to specifying the password explicitly, you can set the variable with a container file path for a password file, and then mount a file from your host that contains the password at the container file path. This is still not very secure, as the location of the password file is still exposed. It is preferable to use the default settings of [MYSQL\\_RANDOM\\_ROOT\\_PASSWORD](#page-187-3) and [MYSQL\\_ONETIME\\_PASSWORD](#page-188-0) both being true.

<span id="page-188-2"></span>• [MYSQL\\_ALLOW\\_EMPTY\\_PASSWORD](#page-188-2). Set it to true to allow the container to be started with a blank password for the root user.

![](_page_188_Picture_17.jpeg)

#### **Warning**

Setting this variable to true is insecure, because it is going to leave your MySQL instance completely unprotected, allowing anyone to gain complete superuser access. It is preferable to use the default settings of [MYSQL\\_RANDOM\\_ROOT\\_PASSWORD](#page-187-3) and [MYSQL\\_ONETIME\\_PASSWORD](#page-188-0) both being true.

## <span id="page-189-1"></span>**2.5.7.3 Deploying MySQL on Windows and Other Non-Linux Platforms with Docker**

![](_page_189_Picture_3.jpeg)

#### **Warning**

The MySQL Docker images provided by Oracle are built specifically for Linux platforms. Other platforms are not supported, and users running the MySQL Docker images from Oracle on them are doing so at their own risk. This section discusses some known issues for the images when used on non-Linux platforms.

Known Issues for using the MySQL Server Docker images from Oracle on Windows include:

• If you are bind-mounting on the container's MySQL data directory (see [Persisting Data and](#page-185-0) [Configuration Changes](#page-185-0) for details), you have to set the location of the server socket file with the - socket option to somewhere outside of the MySQL data directory; otherwise, the server fails to start. This is because the way Docker for Windows handles file mounting does not allow a host file from being bind-mounted on the socket file.

## <span id="page-189-0"></span>**2.5.8 Installing MySQL on Linux from the Native Software Repositories**

Many Linux distributions include a version of the MySQL server, client tools, and development components in their native software repositories and can be installed with the platforms' standard package management systems. This section provides basic instructions for installing MySQL using those package management systems.

![](_page_189_Picture_10.jpeg)

#### **Important**

Native packages are often several versions behind the currently available release. You also normally cannot install development milestone releases (DMRs), as these are not usually made available in the native repositories. Before proceeding, we recommend that you check out the other installation options described in [Section 2.5, "Installing MySQL on Linux"](#page-166-0).

Distribution specific instructions are shown below:

• **Red Hat Linux, Fedora, CentOS**

![](_page_189_Picture_15.jpeg)

### **Note**

For a number of Linux distributions, you can install MySQL using the MySQL Yum repository instead of the platform's native software repository. See [Section 2.5.1, "Installing MySQL on Linux Using the MySQL Yum Repository"](#page-167-0) for details.

For Red Hat and similar distributions, the MySQL distribution is divided into a number of separate packages, mysql for the client tools, mysql-server for the server and associated tools, and mysql-libs for the libraries. The libraries are required if you want to provide connectivity from different languages and environments such as Perl, Python and others.

To install, use the yum command to specify the packages that you want to install. For example:

```
#> yum install mysql mysql-server mysql-libs mysql-server
Loaded plugins: presto, refresh-packagekit
Setting up Install Process
Resolving Dependencies
--> Running transaction check
---> Package mysql.x86_64 0:5.1.48-2.fc13 set to be updated
---> Package mysql-libs.x86_64 0:5.1.48-2.fc13 set to be updated
---> Package mysql-server.x86_64 0:5.1.48-2.fc13 set to be updated
```

```
--> Processing Dependency: perl-DBD-MySQL for package: mysql-server-5.1.48-2.fc13.x86_64
--> Running transaction check
---> Package perl-DBD-MySQL.x86_64 0:4.017-1.fc13 set to be updated
--> Finished Dependency Resolution
Dependencies Resolved
================================================================================
 Package Arch Version Repository Size
================================================================================
Installing:
 mysql x86_64 5.1.48-2.fc13 updates 889 k
 mysql-libs x86_64 5.1.48-2.fc13 updates 1.2 M
 mysql-server x86_64 5.1.48-2.fc13 updates 8.1 M
Installing for dependencies:
 perl-DBD-MySQL x86_64 4.017-1.fc13 updates 136 k
Transaction Summary
================================================================================
Install 4 Package(s)
Upgrade 0 Package(s)
Total download size: 10 M
Installed size: 30 M
Is this ok [y/N]: y
Downloading Packages:
Setting up and reading Presto delta metadata
Processing delta metadata
Package(s) data still to download: 10 M
(1/4): mysql-5.1.48-2.fc13.x86_64.rpm | 889 kB 00:04
(2/4): mysql-libs-5.1.48-2.fc13.x86_64.rpm | 1.2 MB 00:06
(3/4): mysql-server-5.1.48-2.fc13.x86_64.rpm | 8.1 MB 00:40
(4/4): perl-DBD-MySQL-4.017-1.fc13.x86_64.rpm | 136 kB 00:00
--------------------------------------------------------------------------------
Total 201 kB/s | 10 MB 00:52
Running rpm_check_debug
Running Transaction Test
Transaction Test Succeeded
Running Transaction
 Installing : mysql-libs-5.1.48-2.fc13.x86_64 1/4
 Installing : mysql-5.1.48-2.fc13.x86_64 2/4
 Installing : perl-DBD-MySQL-4.017-1.fc13.x86_64 3/4
 Installing : mysql-server-5.1.48-2.fc13.x86_64 4/4
Installed:
 mysql.x86_64 0:5.1.48-2.fc13 mysql-libs.x86_64 0:5.1.48-2.fc13
 mysql-server.x86_64 0:5.1.48-2.fc13
Dependency Installed:
 perl-DBD-MySQL.x86_64 0:4.017-1.fc13
Complete!
```

MySQL and the MySQL server should now be installed. A sample configuration file is installed into / etc/my.cnf. An init script, to start and stop the server, is installed into /etc/init.d/mysqld. To start the MySQL server use service:

```
#> service mysqld start
```

To enable the server to be started and stopped automatically during boot, use chkconfig:

```
#> chkconfig --levels 235 mysqld on
```

Which enables the MySQL server to be started (and stopped) automatically at the specified the run levels.

The database tables are automatically created for you, if they do not already exist. You should, however, run mysql\_secure\_installation to set the root passwords on your server.

#### • **Debian, Ubuntu, Kubuntu**

![](_page_191_Picture_2.jpeg)

#### **Note**

On Debian, Ubuntu, and Kubuntu, MySQL can be installed using the [MySQL](https://dev.mysql.com/downloads/repo/apt/) [APT Repository](https://dev.mysql.com/downloads/repo/apt/) instead of the platform's native software repository. See [Section 2.5.3, "Installing MySQL on Linux Using the MySQL APT Repository"](#page-173-0) for details.

On Debian and related distributions, there are two packages for MySQL in their software repositories, mysql-client and mysql-server, for the client and server components respectively. You should specify an explicit version, for example mysql-client-5.1, to ensure that you install the version of MySQL that you want.

To download and install, including any dependencies, use the apt-get command, specifying the packages that you want to install.

![](_page_191_Picture_7.jpeg)

#### **Note**

Before installing, make sure that you update your apt-get index files to ensure you are downloading the latest available version.

A sample installation of the MySQL packages might look like this (some sections trimmed for clarity):

```
#> apt-get install mysql-client-5.1 mysql-server-5.1
Reading package lists... Done
Building dependency tree
Reading state information... Done
The following packages were automatically installed and are no longer required:
 linux-headers-2.6.28-11 linux-headers-2.6.28-11-generic
Use 'apt-get autoremove' to remove them.
The following extra packages will be installed:
 bsd-mailx libdbd-mysql-perl libdbi-perl libhtml-template-perl
 libmysqlclient15off libmysqlclient16 libnet-daemon-perl libplrpc-perl mailx
 mysql-common postfix
Suggested packages:
 dbishell libipc-sharedcache-perl tinyca procmail postfix-mysql postfix-pgsql
 postfix-ldap postfix-pcre sasl2-bin resolvconf postfix-cdb
The following NEW packages will be installed
 bsd-mailx libdbd-mysql-perl libdbi-perl libhtml-template-perl
 libmysqlclient15off libmysqlclient16 libnet-daemon-perl libplrpc-perl mailx
 mysql-client-5.1 mysql-common mysql-server-5.1 postfix
0 upgraded, 13 newly installed, 0 to remove and 182 not upgraded.
Need to get 1907kB/25.3MB of archives.
After this operation, 59.5MB of additional disk space will be used.
Do you want to continue [Y/n]? Y
Get: 1 http://gb.archive.ubuntu.com jaunty-updates/main mysql-common 5.1.30really5.0.75-0ubuntu10.5 [63.6kB]
Get: 2 http://gb.archive.ubuntu.com jaunty-updates/main libmysqlclient15off 5.1.30really5.0.75-0ubuntu10.5 [1843kB]
Fetched 1907kB in 9s (205kB/s)
Preconfiguring packages ...
Selecting previously deselected package mysql-common.
(Reading database ... 121260 files and directories currently installed.)
...
Processing 1 added doc-base file(s)...
Registering documents with scrollkeeper...
Setting up libnet-daemon-perl (0.43-1) ...
Setting up libplrpc-perl (0.2020-1) ...
Setting up libdbi-perl (1.607-1) ...
Setting up libmysqlclient15off (5.1.30really5.0.75-0ubuntu10.5) ...
Setting up libdbd-mysql-perl (4.008-1) ...
Setting up libmysqlclient16 (5.1.31-1ubuntu2) ...
Setting up mysql-client-5.1 (5.1.31-1ubuntu2) ...
Setting up mysql-server-5.1 (5.1.31-1ubuntu2) ...
 * Stopping MySQL database server mysqld
 ...done.
```

```
2013-09-24T13:03:09.048353Z 0 [Note] InnoDB: 5.7.44 started; log sequence number 1566036
2013-09-24T13:03:10.057269Z 0 [Note] InnoDB: Starting shutdown...
2013-09-24T13:03:10.857032Z 0 [Note] InnoDB: Shutdown completed; log sequence number 1566036
 * Starting MySQL database server mysqld
 ...done.
 * Checking for corrupt, not cleanly closed and upgrade needing tables.
...
Processing triggers for libc6 ...
ldconfig deferred processing now taking place
```

![](_page_192_Picture_2.jpeg)

#### **Note**

The apt-get command installs a number of packages, including the MySQL server, in order to provide the typical tools and application environment. This can mean that you install a large number of packages in addition to the main MySQL package.

During installation, the initial database is created, and you are prompted for the MySQL root password (and confirmation). A configuration file is created in /etc/mysql/my.cnf. An init script is created in /etc/init.d/mysql.

The server is already started. You can manually start and stop the server using:

```
#> service mysql [start|stop]
```

The service is automatically added to run levels 2, 3, and 4, with stop scripts in the single, shutdown, and restart levels.

## <span id="page-192-0"></span>**2.5.9 Installing MySQL on Linux with Juju**

The Juju deployment framework supports easy installation and configuration of MySQL servers. For instructions, see [https://jujucharms.com/mysql/.](https://jujucharms.com/mysql/)

## <span id="page-192-1"></span>**2.5.10 Managing MySQL Server with systemd**

If you install MySQL using an RPM or Debian package on the following Linux platforms, server startup and shutdown is managed by systemd:

- RPM package platforms:
  - Enterprise Linux variants version 7 and higher
  - SUSE Linux Enterprise Server 12 and higher
- Debian family platforms:
  - Debian platforms
  - Ubuntu platforms

If you install MySQL from a generic binary distribution on a platform that uses systemd, you can manually configure systemd support for MySQL following the instructions provided in the postinstallation setup section of the [MySQL 5.7 Secure Deployment Guide.](https://dev.mysql.com/doc/mysql-secure-deployment-guide/en/)

If you install MySQL from a source distribution on a platform that uses systemd, obtain systemd support for MySQL by configuring the distribution using the -DWITH\_SYSTEMD=1 CMake option. See Section 2.8.7, "MySQL Source-Configuration Options".

The following discussion covers these topics:

- [Overview of systemd](#page-193-0)
- [Configuring systemd for MySQL](#page-193-1)

- [Configuring Multiple MySQL Instances Using systemd](#page-195-0)
- [Migrating from mysqld\\_safe to systemd](#page-197-1)

![](_page_193_Picture_3.jpeg)

#### **Note**

On platforms for which systemd support for MySQL is installed, scripts such as mysqld\_safe and the System V initialization script are unnecessary and are not installed. For example, mysqld\_safe can handle server restarts, but systemd provides the same capability, and does so in a manner consistent with management of other services rather than by using an application-specific program.

One implication of the non-use of mysqld\_safe on platforms that use systemd for server management is that use of [mysqld\_safe] or [safe\_mysqld] sections in option files is not supported and might lead to unexpected behavior.

Because systemd has the capability of managing multiple MySQL instances on platforms for which systemd support for MySQL is installed, mysqld\_multi and mysqld\_multi.server are unnecessary and are not installed.

## <span id="page-193-0"></span>**Overview of systemd**

systemd provides automatic MySQL server startup and shutdown. It also enables manual server management using the systemctl command. For example:

```
systemctl {start|stop|restart|status} mysqld
```

Alternatively, use the service command (with the arguments reversed), which is compatible with System V systems:

service mysqld {start|stop|restart|status}

![](_page_193_Picture_13.jpeg)

#### **Note**

For the systemctl or service commands, if the MySQL service name is not mysqld, use the appropriate name. For example, use mysql rather than mysqld on Debian-based and SLES systems.

Support for systemd includes these files:

- mysqld.service (RPM platforms), mysql.service (Debian platforms): systemd service unit configuration file, with details about the MySQL service.
- mysqld@.service (RPM platforms), mysql@.service (Debian platforms): Like mysqld.service or mysql.service, but used for managing multiple MySQL instances.
- mysqld.tmpfiles.d: File containing information to support the tmpfiles feature. This file is installed under the name mysql.conf.
- mysqld\_pre\_systemd (RPM platforms), mysql-system-start (Debian platforms): Support script for the unit file. This script assists in creating the error log file only if the log location matches a pattern (/var/log/mysql\*.log for RPM platforms, /var/log/mysql/\*.log for Debian platforms). In other cases, the error log directory must be writable or the error log must be present and writable for the user running the mysqld process.

### <span id="page-193-1"></span>**Configuring systemd for MySQL**

To add or change systemd options for MySQL, these methods are available:

• Use a localized systemd configuration file.

- Arrange for systemd to set environment variables for the MySQL server process.
- Set the MYSQLD\_OPTS systemd variable.

To use a localized systemd configuration file, create the /etc/systemd/system/ mysqld.service.d directory if it does not exist. In that directory, create a file that contains a [Service] section listing the desired settings. For example:

```
[Service]
LimitNOFILE=max_open_files
PIDFile=/path/to/pid/file
Nice=nice_level
LimitCore=core_file_limit
Environment="LD_PRELOAD=/path/to/malloc/library"
Environment="TZ=time_zone_setting"
```

The discussion here uses override.conf as the name of this file. Newer versions of systemd support the following command, which opens an editor and permits you to edit the file:

```
systemctl edit mysqld # RPM platforms
systemctl edit mysql # Debian platforms
```

Whenever you create or change override.conf, reload the systemd configuration, then tell systemd to restart the MySQL service:

```
systemctl daemon-reload
systemctl restart mysqld # RPM platforms
systemctl restart mysql # Debian platforms
```

With systemd, the override.conf configuration method must be used for certain parameters, rather than settings in a [mysqld], [mysqld\_safe], or [safe\_mysqld] group in a MySQL option file:

- For some parameters, override.conf must be used because systemd itself must know their values and it cannot read MySQL option files to get them.
- Parameters that specify values otherwise settable only using options known to mysqld\_safe must be specified using systemd because there is no corresponding mysqld parameter.

For additional information about using systemd rather than mysqld\_safe, see [Migrating from](#page-197-1) [mysqld\\_safe to systemd](#page-197-1).

You can set the following parameters in override.conf:

- To specify the process ID file:
  - As of MySQL 5.7.10: Use override.conf and change both PIDFile and ExecStart to name the PID file path name. Any setting of the process ID file in MySQL option files is ignored. To modify ExecStart, it must first be cleared. For example:

```
[Service]
PIDFile=/var/run/mysqld/mysqld-custom.pid
ExecStart=
ExecStart=/usr/sbin/mysqld --pid-file=/var/run/mysqld/mysqld-custom.pid $MYSQLD_OPTS
```

- Before MySQL 5.7.10: Use PIDFile in override.conf rather than the --pid-file option for mysqld or mysqld\_safe. systemd must know the PID file location so that it can restart or stop the server. If the PID file value is specified in a MySQL option file, the value must match the PIDFile value or MySQL startup may fail.
- To set the number of file descriptors available to the MySQL server, use LimitNOFILE in override.conf rather than the open\_files\_limit system variable for mysqld or --openfiles-limit option for mysqld\_safe.
- To set the maximum core file size, use LimitCore in override.conf rather than the --corefile-size option for mysqld\_safe.

• To set the scheduling priority for the MySQL server, use Nice in override.conf rather than the --nice option for mysqld\_safe.

Some MySQL parameters are configured using environment variables:

- LD\_PRELOAD: Set this variable if the MySQL server should use a specific memory-allocation library.
- TZ: Set this variable to specify the default time zone for the server.

There are multiple ways to specify environment variable values for use by the MySQL server process managed by systemd:

- Use Environment lines in the override.conf file. For the syntax, see the example in the preceding discussion that describes how to use this file.
- Specify the values in the /etc/sysconfig/mysql file (create the file if it does not exist). Assign values using the following syntax:

```
LD_PRELOAD=/path/to/malloc/library
TZ=time_zone_setting
```

After modifying /etc/sysconfig/mysql, restart the server to make the changes effective:

```
systemctl restart mysqld # RPM platforms
systemctl restart mysql # Debian platforms
```

To specify options for mysqld without modifying systemd configuration files directly, set or unset the MYSQLD\_OPTS systemd variable. For example:

```
systemctl set-environment MYSQLD_OPTS="--general_log=1"
systemctl unset-environment MYSQLD_OPTS
```

MYSQLD\_OPTS can also be set in the /etc/sysconfig/mysql file.

After modifying the systemd environment, restart the server to make the changes effective:

```
systemctl restart mysqld # RPM platforms
systemctl restart mysql # Debian platforms
```

For platforms that use systemd, the data directory is initialized if empty at server startup. This might be a problem if the data directory is a remote mount that has temporarily disappeared: The mount point would appear to be an empty data directory, which then would be initialized as a new data directory. As of MySQL 5.7.20, to suppress this automatic initialization behavior, specify the following line in the / etc/sysconfig/mysql file (create the file if it does not exist):

```
NO_INIT=true
```

### <span id="page-195-0"></span>**Configuring Multiple MySQL Instances Using systemd**

This section describes how to configure systemd for multiple instances of MySQL.

![](_page_195_Picture_20.jpeg)

#### **Note**

Because systemd has the capability of managing multiple MySQL instances on platforms for which systemd support is installed, mysqld\_multi and mysqld\_multi.server are unnecessary and are not installed. This is true as of MySQL 5.7.13 for RPM platforms, 5.7.19 for Debian platforms.

To use multiple-instance capability, modify the my.cnf option file to include configuration of key options for each instance. These file locations are typical:

- /etc/my.cnf or /etc/mysql/my.cnf (RPM platforms)
- /etc/mysql/mysql.conf.d/mysqld.cnf (Debian platforms)

For example, to manage two instances named replica01 and replica02, add something like this to the option file:

#### RPM platforms:

```
[mysqld@replica01]
datadir=/var/lib/mysql-replica01
socket=/var/lib/mysql-replica01/mysql.sock
port=3307
log-error=/var/log/mysqld-replica01.log
[mysqld@replica02]
datadir=/var/lib/mysql-replica02
socket=/var/lib/mysql-replica02/mysql.sock
port=3308
log-error=/var/log/mysqld-replica02.log
```

#### Debian platforms:

```
[mysqld@replica01]
datadir=/var/lib/mysql-replica01
socket=/var/lib/mysql-replica01/mysql.sock
port=3307
log-error=/var/log/mysql/replica01.log
[mysqld@replica02]
datadir=/var/lib/mysql-replica02
socket=/var/lib/mysql-replica02/mysql.sock
port=3308
log-error=/var/log/mysql/replica02.log
```

The replica names shown here use @ as the delimiter because that is the only delimiter supported by systemd.

Instances then are managed by normal systemd commands, such as:

```
systemctl start mysqld@replica01
systemctl start mysqld@replica02
```

To enable instances to run at boot time, do this:

```
systemctl enable mysqld@replica01
systemctl enable mysqld@replica02
```

Use of wildcards is also supported. For example, this command displays the status of all replica instances:

```
systemctl status 'mysqld@replica*'
```

For management of multiple MySQL instances on the same machine, systemd automatically uses a different unit file:

- mysqld@.service rather than mysqld.service (RPM platforms)
- mysql@.service rather than mysql.service (Debian platforms)

In the unit file, %I and %i reference the parameter passed in after the @ marker and are used to manage the specific instance. For a command such as this:

```
systemctl start mysqld@replica01
```

systemd starts the server using a command such as this:

```
mysqld --defaults-group-suffix=@%I ...
```

The result is that the [server], [mysqld], and [mysqld@replica01] option groups are read and used for that instance of the service.

![](_page_197_Picture_1.jpeg)

#### **Note**

On Debian platforms, AppArmor prevents the server from reading or writing / var/lib/mysql-replica\*, or anything other than the default locations. To address this, you must customize or disable the profile in /etc/apparmor.d/ usr.sbin.mysqld.

![](_page_197_Picture_4.jpeg)

#### **Note**

On Debian platforms, the packaging scripts for MySQL uninstallation cannot currently handle mysqld@ instances. Before removing or upgrading the package, you must stop any extra instances manually first.

### <span id="page-197-1"></span>**Migrating from mysqld\_safe to systemd**

Because mysqld\_safe is not installed on platforms that use systemd to manage MySQL, options previously specified for that program (for example, in an [mysqld\_safe] or [safe\_mysqld] option group) must be specified another way:

• Some mysqld\_safe options are also understood by mysqld and can be moved from the [mysqld\_safe] or [safe\_mysqld] option group to the [mysqld] group. This does not include --pid-file, --open-files-limit, or --nice. To specify those options, use the override.conf systemd file, described previously.

![](_page_197_Picture_10.jpeg)

#### **Note**

On systemd platforms, use of [mysqld\_safe] and [safe\_mysqld] option groups is not supported and may lead to unexpected behavior.

- For some mysqld\_safe options, there are similar mysqld options. For example, the mysqld\_safe option for enabling syslog logging is --syslog, which is deprecated. For mysqld, enable the log\_syslog system variable instead. For details, see Section 5.4.2, "The Error Log".
- mysqld\_safe options not understood by mysqld can be specified in override.conf or environment variables. For example, with mysqld\_safe, if the server should use a specific memory allocation library, this is specified using the --malloc-lib option. For installations that manage the server with systemd, arrange to set the LD\_PRELOAD environment variable instead, as described previously.

## <span id="page-197-0"></span>**2.6 Installing MySQL Using Unbreakable Linux Network (ULN)**

Linux supports a number of different solutions for installing MySQL, covered in [Section 2.5,](#page-166-0) ["Installing MySQL on Linux".](#page-166-0) One of the methods, covered in this section, is installing from Oracle's Unbreakable Linux Network (ULN). You can find information about Oracle Linux and ULN under [http://](http://linux.oracle.com/) [linux.oracle.com/](http://linux.oracle.com/).

To use ULN, you need to obtain a ULN login and register the machine used for installation with ULN. This is described in detail in the [ULN FAQ](https://linux.oracle.com/uln_faq.md). The page also describes how to install and update packages. The MySQL packages are in the "MySQL for Oracle Linux 6" and "MySQL for Oracle Linux 7" channels for your system architecture on ULN.

![](_page_197_Picture_18.jpeg)

#### **Note**

ULN provides MySQL 5.7 for Oracle Linux 6 and Oracle Linux 7. Alternatively, Oracle Linux 8 supports MySQL 8.0. In addition, Enterprise packages are available as of MySQL 8.0.21.

Once MySQL has been installed using ULN, you can find information on starting and stopping the server, and more, in [this section,](#page-189-0) particularly under [Section 2.5.5, "Installing MySQL on Linux Using](#page-173-2) [RPM Packages from Oracle"](#page-173-2).

If you are changing your package source to use ULN and not changing which build of MySQL you are using, then back up your data, remove your existing binaries, and replace them with those from ULN. If a change of build is involved, we recommend the backup be a dump (mysqldump or mysqlpump or from [MySQL Shell's backup utility](https://dev.mysql.com/doc/mysql-shell/8.0/en/mysql-shell-utilities-dump-instance-schema.md)) just in case you need to rebuild your data after the new binaries are in place. If this shift to ULN crosses a version boundary, consult this section before proceeding: Section 2.10, "Upgrading MySQL".

## <span id="page-198-0"></span>**2.7 Installing MySQL on Solaris**

![](_page_198_Picture_3.jpeg)

#### **Note**

MySQL 5.7 supports Solaris 11 (Update 3 and later).

MySQL on Solaris is available in a number of different formats.

- For information on installing using the native Solaris PKG format, see [Section 2.7.1, "Installing](#page-199-0) [MySQL on Solaris Using a Solaris PKG".](#page-199-0)
- To use a standard tar binary installation, use the notes provided in [Section 2.2, "Installing MySQL](#page-103-0) [on Unix/Linux Using Generic Binaries".](#page-103-0) Check the notes and hints at the end of this section for Solaris specific notes that you may need before or after installation.

![](_page_198_Picture_9.jpeg)

#### **Important**

The installation packages have a dependency on the Oracle Developer Studio 12.5 Runtime Libraries, which must be installed before you run the MySQL installation package. See the download options for Oracle Developer Studio [here](http://www.oracle.com/technetwork/server-storage/developerstudio/downloads/index.md). The installation package enables you to install the runtime libraries only instead of the full Oracle Developer Studio; see instructions in [Installing Only](https://docs.oracle.com/cd/E60778_01/html/E60743/gozsu.md) [the Runtime Libraries on Oracle Solaris 11.](https://docs.oracle.com/cd/E60778_01/html/E60743/gozsu.md)

To obtain a binary MySQL distribution for Solaris in tarball or PKG format, [https://dev.mysql.com/](https://dev.mysql.com/downloads/mysql/5.7.md) [downloads/mysql/5.7.html](https://dev.mysql.com/downloads/mysql/5.7.md).

Additional notes to be aware of when installing and using MySQL on Solaris:

• If you want to use MySQL with the mysql user and group, use the groupadd and useradd commands:

```
groupadd mysql
useradd -g mysql -s /bin/false mysql
```

• If you install MySQL using a binary tarball distribution on Solaris, because the Solaris tar cannot handle long file names, use GNU tar (gtar) to unpack the distribution. If you do not have GNU tar on your system, install it with the following command:

```
pkg install archiver/gnu-tar
```

- You should mount any file systems on which you intend to store InnoDB files with the forcedirectio option. (By default mounting is done without this option.) Failing to do so causes a significant drop in performance when using the InnoDB storage engine on this platform.
- If you would like MySQL to start automatically, you can copy support-files/mysql.server to / etc/init.d and create a symbolic link to it named /etc/rc3.d/S99mysql.server.
- If too many processes try to connect very rapidly to mysqld, you should see this error in the MySQL log:

```
Error in accept: Protocol error
```

You might try starting the server with the --back\_log=50 option as a workaround for this.

• To configure the generation of core files on Solaris you should use the coreadm command. Because of the security implications of generating a core on a setuid() application, by default, Solaris does not support core files on setuid() programs. However, you can modify this behavior using coreadm. If you enable setuid() core files for the current user, they are generated using mode 600, and are owned by the superuser.

## <span id="page-199-0"></span>**2.7.1 Installing MySQL on Solaris Using a Solaris PKG**

You can install MySQL on Solaris using a binary package of the native Solaris PKG format instead of the binary tarball distribution.

![](_page_199_Picture_4.jpeg)

### **Important**

The installation package has a dependency on the Oracle Developer Studio 12.5 Runtime Libraries, which must be installed before you run the MySQL installation package. See the download options for Oracle Developer Studio [here](http://www.oracle.com/technetwork/server-storage/developerstudio/downloads/index.md). The installation package enables you to install the runtime libraries only instead of the full Oracle Developer Studio; see instructions in [Installing Only](https://docs.oracle.com/cd/E60778_01/html/E60743/gozsu.md) [the Runtime Libraries on Oracle Solaris 11.](https://docs.oracle.com/cd/E60778_01/html/E60743/gozsu.md)

To use this package, download the corresponding mysql-VERSION-solaris11- PLATFORM.pkg.gz file, then uncompress it. For example:

```
$> gunzip mysql-5.7.44-solaris11-x86_64.pkg.gz
```

To install a new package, use pkgadd and follow the onscreen prompts. You must have root privileges to perform this operation:

```
$> pkgadd -d mysql-5.7.44-solaris11-x86_64.pkg
The following packages are available:
 1 mysql MySQL Community Server (GPL)
 (i86pc) 5.7.44
Select package(s) you wish to process (or 'all' to process
all packages). (default: all) [?,??,q]:
```

The PKG installer installs all of the files and tools needed, and then initializes your database if one does not exist. To complete the installation, you should set the root password for MySQL as provided in the instructions at the end of the installation. Alternatively, you can run the mysql\_secure\_installation script that comes with the installation.

By default, the PKG package installs MySQL under the root path /opt/mysql. You can change only the installation root path when using pkgadd, which can be used to install MySQL in a different Solaris zone. If you need to install in a specific directory, use a binary tar file distribution.

The pkg installer copies a suitable startup script for MySQL into /etc/init.d/mysql. To enable MySQL to startup and shutdown automatically, you should create a link between this file and the init script directories. For example, to ensure safe startup and shutdown of MySQL you could use the following commands to add the right links:

```
$> ln /etc/init.d/mysql /etc/rc3.d/S91mysql
$> ln /etc/init.d/mysql /etc/rc0.d/K02mysql
```

To remove MySQL, the installed package name is mysql. You can use this in combination with the pkgrm command to remove the installation.

To upgrade when using the Solaris package file format, you must remove the existing installation before installing the updated package. Removal of the package does not delete the existing database information, only the server, binaries and support files. The typical upgrade sequence is therefore:

```
$> mysqladmin shutdown
```

```
$> pkgrm mysql
$> pkgadd -d mysql-5.7.44-solaris11-x86_64.pkg
$> mysqld_safe &
$> mysql_upgrade
```

You should check the notes in [Section 2.10, "Upgrading MySQL"](#page-45-0) before performing any upgrade.

# <span id="page-0-1"></span>**2.8 Installing MySQL from Source**

Building MySQL from the source code enables you to customize build parameters, compiler optimizations, and installation location. For a list of systems on which MySQL is known to run, see <https://www.mysql.com/support/supportedplatforms/database.html>.

Before you proceed with an installation from source, check whether Oracle produces a precompiled binary distribution for your platform and whether it works for you. We put a great deal of effort into ensuring that our binaries are built with the best possible options for optimal performance. Instructions for installing binary distributions are available in Section 2.2, "Installing MySQL on Unix/Linux Using Generic Binaries".

If you are interested in building MySQL from a source distribution using build options the same as or similar to those use by Oracle to produce binary distributions on your platform, obtain a binary distribution, unpack it, and look in the docs/INFO\_BIN file, which contains information about how that MySQL distribution was configured and compiled.

![](_page_0_Picture_7.jpeg)

#### **Warning**

Building MySQL with nonstandard options may lead to reduced functionality, performance, or security.

## **2.8.1 Source Installation Methods**

There are two methods for installing MySQL from source:

• Use a standard MySQL source distribution. To obtain a standard distribution, see Section 2.1.3, "How to Get MySQL". For instructions on building from a standard distribution, see [Section 2.8.4,](#page-2-0) ["Installing MySQL Using a Standard Source Distribution".](#page-2-0)

Standard distributions are available as compressed tar files, Zip archives, or RPM packages. Distribution files have names of the form mysql-VERSION.tar.gz, mysql-VERSION.zip, or mysql-VERSION.rpm, where VERSION is a number like 5.7.44. File names for source distributions can be distinguished from those for precompiled binary distributions in that source distribution names are generic and include no platform name, whereas binary distribution names include a platform name indicating the type of system for which the distribution is intended (for example, pc-linux-i686 or winx64).

• Use a MySQL development tree. For information on building from one of the development trees, see [Section 2.8.5, "Installing MySQL Using a Development Source Tree"](#page-6-0).

## <span id="page-0-0"></span>**2.8.2 Source Installation Prerequisites**

Installation of MySQL from source requires several development tools. Some of these tools are needed no matter whether you use a standard source distribution or a development source tree. Other tool requirements depend on which installation method you use.

To install MySQL from source, the following system requirements must be satisfied, regardless of installation method:

• CMake, which is used as the build framework on all platforms. CMake can be downloaded from [http://](http://www.cmake.org) [www.cmake.org](http://www.cmake.org).

• A good make program. Although some platforms come with their own make implementations, it is highly recommended that you use GNU make 3.75 or later. It may already be available on your system as gmake. GNU make is available from<http://www.gnu.org/software/make/>.

On Unix-like systems, including Linux, you can check your system's version of make like this:

```
$> make --version
GNU Make 4.2.1
```

- A working ANSI C++ compiler. See the description of the [FORCE\\_UNSUPPORTED\\_COMPILER](#page-21-0) option for some guidelines.
- An SSL library is required for support of encrypted connections, entropy for random number generation, and other encryption-related operations. By default, the build uses the OpenSSL library installed on the host system. To specify the library explicitly, use the [WITH\\_SSL](#page-27-0) option when you invoke CMake. For additional information, see [Section 2.8.6, "Configuring SSL Library Support"](#page-8-0).
- The Boost C++ libraries are required to build MySQL (but not to use it). Boost 1.59.0 must be installed. To obtain Boost and its installation instructions, visit [the official Boost web site](https://www.boost.org). After Boost is installed, tell the build system where the Boost files are placed according to the value set for the [WITH\\_BOOST](#page-23-0) option when you invoke CMake. For example:

```
cmake . -DWITH_BOOST=/usr/local/boost_version_number
```

Adjust the path as necessary to match your installation.

- The [ncurses](https://www.gnu.org/software/ncurses/ncurses.md) library.
- Sufficient free memory. If you encounter build errors such as internal compiler error when compiling large source files, it may be that you have too little memory. If compiling on a virtual machine, try increasing the memory allocation.
- Perl is needed if you intend to run test scripts. Most Unix-like systems include Perl. For Windows, you can use [ActiveState Perl.](https://www.activestate.com/products/perl/) or [Strawberry Perl.](https://strawberryperl.com/)

To install MySQL from a standard source distribution, one of the following tools is required to unpack the distribution file:

• For a .tar.gz compressed tar file: GNU gunzip to uncompress the distribution and a reasonable tar to unpack it. If your tar program supports the z option, it can both uncompress and unpack the file.

GNU tar is known to work. The standard tar provided with some operating systems is not able to unpack the long file names in the MySQL distribution. You should download and install GNU tar, or if available, use a preinstalled version of GNU tar. Usually this is available as gnutar, gtar, or as tar within a GNU or Free Software directory, such as /usr/sfw/bin or /usr/local/bin. GNU tar is available from [https://www.gnu.org/software/tar/.](https://www.gnu.org/software/tar/)

- For a .zip Zip archive: WinZip or another tool that can read .zip files.
- For an .rpm RPM package: The rpmbuild program used to build the distribution unpacks it.

To install MySQL from a development source tree, the following additional tools are required:

- The Git revision control system is required to obtain the development source code. [GitHub Help](https://help.github.com/) provides instructions for downloading and installing Git on different platforms.
- bison 2.1 or later, available from [http://www.gnu.org/software/bison/.](http://www.gnu.org/software/bison/) (Version 1 is no longer supported.) Use the latest version of bison where possible; if you experience problems, upgrade to a later version, rather than revert to an earlier one.

bison is available from <http://www.gnu.org/software/bison/>. bison for Windows can be downloaded from [http://gnuwin32.sourceforge.net/packages/bison.htm.](http://gnuwin32.sourceforge.net/packages/bison.md) Download the package labeled "Complete package, excluding sources". On Windows, the default location for bison is the C:\Program Files\GnuWin32 directory. Some utilities may fail to find bison because of the space in the directory name. Also, Visual Studio may simply hang if there are spaces in the path. You can resolve these problems by installing into a directory that does not contain a space (for example C: \GnuWin32).

• On Solaris Express, m4 must be installed in addition to bison. m4 is available from [http://](http://www.gnu.org/software/m4/) [www.gnu.org/software/m4/](http://www.gnu.org/software/m4/).

![](_page_2_Picture_3.jpeg)

#### **Note**

If you have to install any programs, modify your PATH environment variable to include any directories in which the programs are located. See [Section 4.2.7,](#page-143-0) ["Setting Environment Variables"](#page-143-0).

If you run into problems and need to file a bug report, please use the instructions in Section 1.5, "How to Report Bugs or Problems".

## **2.8.3 MySQL Layout for Source Installation**

By default, when you install MySQL after compiling it from source, the installation step installs files under /usr/local/mysql. The component locations under the installation directory are the same as for binary distributions. See Table 2.3, "MySQL Installation Layout for Generic Unix/Linux Binary Package", and Section 2.3.1, "MySQL Installation Layout on Microsoft Windows". To configure installation locations different from the defaults, use the options described at [Section 2.8.7, "MySQL](#page-9-0) [Source-Configuration Options"](#page-9-0).

## <span id="page-2-0"></span>**2.8.4 Installing MySQL Using a Standard Source Distribution**

To install MySQL from a standard source distribution:

- 1. Verify that your system satisfies the tool requirements listed at [Section 2.8.2, "Source Installation](#page-0-0) [Prerequisites".](#page-0-0)
- 2. Obtain a distribution file using the instructions in Section 2.1.3, "How to Get MySQL".
- 3. Configure, build, and install the distribution using the instructions in this section.
- 4. Perform postinstallation procedures using the instructions in [Section 2.9, "Postinstallation Setup](#page-32-0) [and Testing".](#page-32-0)

MySQL uses CMake as the build framework on all platforms. The instructions given here should enable you to produce a working installation. For additional information on using CMake to build MySQL, see [How to Build MySQL Server with CMake](https://dev.mysql.com/doc/internals/en/cmake.md).

If you start from a source RPM, use the following command to make a binary RPM that you can install. If you do not have rpmbuild, use rpm instead.

```
$> rpmbuild --rebuild --clean MySQL-VERSION.src.rpm
```

The result is one or more binary RPM packages that you install as indicated in Section 2.5.5, "Installing MySQL on Linux Using RPM Packages from Oracle".

The sequence for installation from a compressed tar file or Zip archive source distribution is similar to the process for installing from a generic binary distribution (see Section 2.2, "Installing MySQL on Unix/ Linux Using Generic Binaries"), except that it is used on all platforms and includes steps to configure and compile the distribution. For example, with a compressed tar file source distribution on Unix, the basic installation command sequence looks like this:

# Preconfiguration setup

```
$> groupadd mysql
$> useradd -r -g mysql -s /bin/false mysql
# Beginning of source-build specific instructions
$> tar zxvf mysql-VERSION.tar.gz
$> cd mysql-VERSION
$> mkdir bld
$> cd bld
$> cmake ..
$> make
$> make install
# End of source-build specific instructions
# Postinstallation setup
$> cd /usr/local/mysql
$> mkdir mysql-files
$> chown mysql:mysql mysql-files
$> chmod 750 mysql-files
$> bin/mysqld --initialize --user=mysql
$> bin/mysql_ssl_rsa_setup
$> bin/mysqld_safe --user=mysql &
# Next command is optional
$> cp support-files/mysql.server /etc/init.d/mysql.server
```

A more detailed version of the source-build specific instructions is shown following.

![](_page_3_Picture_3.jpeg)

#### **Note**

The procedure shown here does not set up any passwords for MySQL accounts. After following the procedure, proceed to [Section 2.9, "Postinstallation](#page-32-0) [Setup and Testing",](#page-32-0) for postinstallation setup and testing.

- [Perform Preconfiguration Setup](#page-3-0)
- [Obtain and Unpack the Distribution](#page-3-1)
- [Configure the Distribution](#page-4-0)
- [Build the Distribution](#page-5-0)
- [Install the Distribution](#page-6-1)
- [Perform Postinstallation Setup](#page-6-2)

### <span id="page-3-0"></span>**Perform Preconfiguration Setup**

On Unix, set up the mysql user that owns the database directory and that should be used to run and execute the MySQL server, and the group to which this user belongs. For details, see Create a mysql User and Group. Then perform the following steps as the mysql user, except as noted.

### <span id="page-3-1"></span>**Obtain and Unpack the Distribution**

Pick the directory under which you want to unpack the distribution and change location into it.

Obtain a distribution file using the instructions in Section 2.1.3, "How to Get MySQL".

Unpack the distribution into the current directory:

• To unpack a compressed tar file, tar can decompress and unpack the distribution if it has z option support:

```
$> tar zxvf mysql-VERSION.tar.gz
```

If your tar does not have z option support, use gunzip to decompress the distribution and tar to unpack it:

```
$> gunzip < mysql-VERSION.tar.gz | tar xvf -
```

Alternatively, CMake can decompress and unpack the distribution:

```
$> cmake -E tar zxvf mysql-VERSION.tar.gz
```

• To unpack a Zip archive, use WinZip or another tool that can read .zip files.

Unpacking the distribution file creates a directory named mysql-VERSION.

## <span id="page-4-0"></span>**Configure the Distribution**

Change location into the top-level directory of the unpacked distribution:

```
$> cd mysql-VERSION
```

Build outside of the source tree to keep the tree clean. If the top-level source directory is named mysql-src under your current working directory, you can build in a directory named build at the same level. Create the directory and go there:

```
$> mkdir bld
$> cd bld
```

Configure the build directory. The minimum configuration command includes no options to override configuration defaults:

```
$> cmake ../mysql-src
```

The build directory need not be outside the source tree. For example, you can build in a directory named build under the top-level source tree. To do this, starting with mysql-src as your current working directory, create the directory build and then go there:

```
$> mkdir build
$> cd build
```

Configure the build directory. The minimum configuration command includes no options to override configuration defaults:

```
$> cmake ..
```

If you have multiple source trees at the same level (for example, to build multiple versions of MySQL), the second strategy can be advantageous. The first strategy places all build directories at the same level, which requires that you choose a unique name for each. With the second strategy, you can use the same name for the build directory within each source tree. The following instructions assume this second strategy.

On Windows, specify the development environment. For example, the following commands configure MySQL for 32-bit or 64-bit builds, respectively:

```
$> cmake .. -G "Visual Studio 12 2013"
$> cmake .. -G "Visual Studio 12 2013 Win64"
```

On macOS, to use the Xcode IDE:

```
$> cmake .. -G Xcode
```

When you run Cmake, you might want to add options to the command line. Here are some examples:

- [-DBUILD\\_CONFIG=mysql\\_release](#page-14-0): Configure the source with the same build options used by Oracle to produce binary distributions for official MySQL releases.
- [-DCMAKE\\_INSTALL\\_PREFIX=](#page-15-0)dir\_name: Configure the distribution for installation under a particular location.

- [-DCPACK\\_MONOLITHIC\\_INSTALL=1](#page-15-1): Cause make package to generate a single installation file rather than multiple files.
- [-DWITH\\_DEBUG=1](#page-24-0): Build the distribution with debugging support.

For a more extensive list of options, see [Section 2.8.7, "MySQL Source-Configuration Options".](#page-9-0)

To list the configuration options, use one of the following commands:

```
$> cmake .. -L # overview
$> cmake .. -LH # overview with help text
$> cmake .. -LAH # all params with help text
$> ccmake .. # interactive display
```

If CMake fails, you might need to reconfigure by running it again with different options. If you do reconfigure, take note of the following:

- If CMake is run after it has previously been run, it may use information that was gathered during its previous invocation. This information is stored in CMakeCache.txt. When CMake starts, it looks for that file and reads its contents if it exists, on the assumption that the information is still correct. That assumption is invalid when you reconfigure.
- Each time you run CMake, you must run make again to recompile. However, you may want to remove old object files from previous builds first because they were compiled using different configuration options.

To prevent old object files or configuration information from being used, run these commands in the build directory on Unix before re-running CMake:

```
$> make clean
$> rm CMakeCache.txt
```

Or, on Windows:

```
$> devenv MySQL.sln /clean
$> del CMakeCache.txt
```

Before asking on the [MySQL Community Slack](https://mysqlcommunity.slack.com/), check the files in the CMakeFiles directory for useful information about the failure. To file a bug report, please use the instructions in Section 1.5, "How to Report Bugs or Problems".

### <span id="page-5-0"></span>**Build the Distribution**

On Unix:

```
$> make
$> make VERBOSE=1
```

The second command sets VERBOSE to show the commands for each compiled source.

Use gmake instead on systems where you are using GNU make and it has been installed as gmake.

On Windows:

```
$> devenv MySQL.sln /build RelWithDebInfo
```

If you have gotten to the compilation stage, but the distribution does not build, see [Section 2.8.8,](#page-30-0) ["Dealing with Problems Compiling MySQL"](#page-30-0), for help. If that does not solve the problem, please enter it into our bugs database using the instructions given in Section 1.5, "How to Report Bugs or Problems".

If you have installed the latest versions of the required tools, and they crash trying to process our configuration files, please report that also. However, if you get a command not found error or a similar problem for required tools, do not report it. Instead, make sure that all the required tools are installed and that your PATH variable is set correctly so that your shell can find them.

## <span id="page-6-1"></span>**Install the Distribution**

On Unix:

\$> **make install**

This installs the files under the configured installation directory (by default, /usr/local/mysql). You might need to run the command as root.

To install in a specific directory, add a DESTDIR parameter to the command line:

```
$> make install DESTDIR="/opt/mysql"
```

Alternatively, generate installation package files that you can install where you like:

```
$> make package
```

This operation produces one or more .tar.gz files that can be installed like generic binary distribution packages. See Section 2.2, "Installing MySQL on Unix/Linux Using Generic Binaries". If you run CMake with [-DCPACK\\_MONOLITHIC\\_INSTALL=1](#page-15-1), the operation produces a single file. Otherwise, it produces multiple files.

On Windows, generate the data directory, then create a .zip archive installation package:

```
$> devenv MySQL.sln /build RelWithDebInfo /project initial_database
$> devenv MySQL.sln /build RelWithDebInfo /project package
```

You can install the resulting .zip archive where you like. See Section 2.3.4, "Installing MySQL on Microsoft Windows Using a noinstall ZIP Archive".

### <span id="page-6-2"></span>**Perform Postinstallation Setup**

The remainder of the installation process involves setting up the configuration file, creating the core databases, and starting the MySQL server. For instructions, see [Section 2.9, "Postinstallation Setup](#page-32-0) [and Testing".](#page-32-0)

![](_page_6_Picture_16.jpeg)

#### **Note**

The accounts that are listed in the MySQL grant tables initially have no passwords. After starting the server, you should set up passwords for them using the instructions in [Section 2.9, "Postinstallation Setup and Testing".](#page-32-0)

## <span id="page-6-0"></span>**2.8.5 Installing MySQL Using a Development Source Tree**

This section describes how to install MySQL from the latest development source code, which is hosted on [GitHub](https://github.com/). To obtain the MySQL Server source code from this repository hosting service, you can set up a local MySQL Git repository.

On [GitHub](https://github.com/), MySQL Server and other MySQL projects are found on the [MySQL](https://github.com/mysql) page. The MySQL Server project is a single repository that contains branches for several MySQL series.

- [Prerequisites for Installing from Development Source](#page-7-0)
- [Setting Up a MySQL Git Repository](#page-7-1)

## <span id="page-7-0"></span>**Prerequisites for Installing from Development Source**

To install MySQL from a development source tree, your system must satisfy the tool requirements listed at [Section 2.8.2, "Source Installation Prerequisites"](#page-0-0).

## <span id="page-7-1"></span>**Setting Up a MySQL Git Repository**

To set up a MySQL Git repository on your machine:

1. Clone the MySQL Git repository to your machine. The following command clones the MySQL Git repository to a directory named mysql-server. The initial download may take some time to complete, depending on the speed of your connection.

```
$> git clone https://github.com/mysql/mysql-server.git
Cloning into 'mysql-server'...
remote: Counting objects: 1198513, done.
remote: Total 1198513 (delta 0), reused 0 (delta 0), pack-reused 1198513
Receiving objects: 100% (1198513/1198513), 1.01 GiB | 7.44 MiB/s, done.
Resolving deltas: 100% (993200/993200), done.
Checking connectivity... done.
Checking out files: 100% (25510/25510), done.
```

2. When the clone operation completes, the contents of your local MySQL Git repository appear similar to the following:

```
~> cd mysql-server
~/mysql-server> ls
client extra mysys storage
cmake include packaging strings
CMakeLists.txt INSTALL plugin support-files
components libbinlogevents README testclients
config.h.cmake libchangestreams router unittest
configure.cmake libmysql run_doxygen.cmake utilities
Docs libservices scripts VERSION
Doxyfile-ignored LICENSE share vio
Doxyfile.in man sql win
doxygen_resources mysql-test sql-common
```

3. Use the git branch -r command to view the remote tracking branches for the MySQL repository.

```
~/mysql-server> git branch -r
 origin/5.7
 origin/8.0
 origin/HEAD -> origin/trunk
 origin/cluster-7.4
 origin/cluster-7.5
 origin/cluster-7.6
 origin/trunk
```

4. To view the branch that is checked out in your local repository, issue the git branch command. When you clone the MySQL Git repository, the latest MySQL branch is checked out automatically. The asterisk identifies the active branch.

```
~/mysql-server$ git branch
* trunk
```

5. To check out an earlier MySQL branch, run the git checkout command, specifying the branch name. For example, to check out the MySQL 5.7 branch:

```
~/mysql-server$ git checkout 5.7
Checking out files: 100% (9600/9600), done.
Branch 5.7 set up to track remote branch 5.7 from origin.
Switched to a new branch '5.7'
```

6. To obtain changes made after your initial setup of the MySQL Git repository, switch to the branch you want to update and issue the git pull command:

```
~/mysql-server$ git checkout 8.0
~/mysql-server$ git pull
```

To examine the commit history, use the git log command:

```
~/mysql-server$ git log
```

You can also browse commit history and source code on the GitHub [MySQL](https://github.com/mysql) site.

If you see changes or code that you have a question about, ask on [MySQL Community Slack](https://mysqlcommunity.slack.com/).

7. After you have cloned the MySQL Git repository and have checked out the branch you want to build, you can build MySQL Server from the source code. Instructions are provided in [Section 2.8.4,](#page-2-0) ["Installing MySQL Using a Standard Source Distribution",](#page-2-0) except that you skip the part about obtaining and unpacking the distribution.

Be careful about installing a build from a distribution source tree on a production machine. The installation command may overwrite your live release installation. If you already have MySQL installed and do not want to overwrite it, run CMake with values for the [CMAKE\\_INSTALL\\_PREFIX](#page-15-0), [MYSQL\\_TCP\\_PORT](#page-22-0), and [MYSQL\\_UNIX\\_ADDR](#page-22-1) options different from those used by your production server. For additional information about preventing multiple servers from interfering with each other, see Section 5.7, "Running Multiple MySQL Instances on One Machine".

Play hard with your new installation. For example, try to make new features crash. Start by running make test. See [The MySQL Test Suite](https://dev.mysql.com/doc/extending-mysql/5.7/en/mysql-test-suite.md).

## <span id="page-8-0"></span>**2.8.6 Configuring SSL Library Support**

An SSL library is required for support of encrypted connections, entropy for random number generation, and other encryption-related operations. Your system must support either OpenSSL or yaSSL:

- All MySQL Enterprise Edition binary distributions are compiled using OpenSSL. It is not possible to use yaSSL with MySQL Enterprise Edition.
- Prior to MySQL 5.7.28, MySQL Community Edition binary distributions are compiled using yaSSL. As of MySQL 5.7.28, support for yaSSL is removed and all MySQL builds use OpenSSL.
- Prior to MySQL 5.7.28, MySQL Community Edition source distributions can be compiled using either OpenSSL or yaSSL. As of MySQL 5.7.28, support for yaSSL is removed.

If you compile MySQL from a source distribution, CMake configures the distribution to use the installed OpenSSL library by default.

To compile using OpenSSL, use this procedure:

- 1. Ensure that OpenSSL 1.0.1 or newer is installed on your system. If the installed OpenSSL version is older than 1.0.1, CMake produces an error at MySQL configuration time. If it is necessary to obtain OpenSSL, visit <http://www.openssl.org>.
- 2. The [WITH\\_SSL](#page-27-0) CMake option determines which SSL library to use for compiling MySQL (see [Section 2.8.7, "MySQL Source-Configuration Options"](#page-9-0)). The default is [-DWITH\\_SSL=system](#page-27-0), which uses OpenSSL. To make this explicit, specify that option. For example:

```
cmake . -DWITH_SSL=system
```

That command configures the distribution to use the installed OpenSSL library. Alternatively, to explicitly specify the path name to the OpenSSL installation, use the following syntax. This can be useful if you have multiple versions of OpenSSL installed, to prevent CMake from choosing the wrong one:

```
cmake . -DWITH_SSL=path_name
```

3. Compile and install the distribution.

To check whether a [mysqld](#page-144-0) server supports encrypted connections, examine the value of the have\_ssl system variable:

```
mysql> SHOW VARIABLES LIKE 'have_ssl';
+---------------+-------+
| Variable_name | Value |
+---------------+-------+
| have_ssl | YES |
+---------------+-------+
```

If the value is YES, the server supports encrypted connections. If the value is DISABLED, the server is capable of supporting encrypted connections but was not started with the appropriate --ssl-xxx options to enable encrypted connections to be used; see Section 6.3.1, "Configuring MySQL to Use Encrypted Connections".

To determine whether a server was compiled using OpenSSL or yaSSL, check the existence of any of the system or status variables that are present only for OpenSSL. See Section 6.3.4, "SSL Library-Dependent Capabilities".

## <span id="page-9-0"></span>**2.8.7 MySQL Source-Configuration Options**

The CMake program provides a great deal of control over how you configure a MySQL source distribution. Typically, you do this using options on the CMake command line. For information about options supported by CMake, run either of these commands in the top-level source directory:

```
$> cmake . -LH
$> ccmake .
```

You can also affect CMake using certain environment variables. See Section 4.9, "Environment Variables".

For boolean options, the value may be specified as 1 or ON to enable the option, or as 0 or OFF to disable the option.

Many options configure compile-time defaults that can be overridden at server startup. For example, the [CMAKE\\_INSTALL\\_PREFIX](#page-15-0), [MYSQL\\_TCP\\_PORT](#page-22-0), and [MYSQL\\_UNIX\\_ADDR](#page-22-1) options that configure the default installation base directory location, TCP/IP port number, and Unix socket file can be changed at server startup with the --basedir, --port, and --socket options for [mysqld](#page-144-0). Where applicable, configuration option descriptions indicate the corresponding [mysqld](#page-144-0) startup option.

The following sections provide more information about CMake options.

- [CMake Option Reference](#page-9-1)
- [General Options](#page-14-1)
- [Installation Layout Options](#page-15-2)
- [Storage Engine Options](#page-17-0)
- [Feature Options](#page-19-0)
- [Compiler Flags](#page-28-0)
- [CMake Options for Compiling NDB Cluster](#page-29-0)

### <span id="page-9-1"></span>**CMake Option Reference**

The following table shows the available CMake options. In the Default column, PREFIX stands for the value of the [CMAKE\\_INSTALL\\_PREFIX](#page-15-0) option, which specifies the installation base directory. This value is used as the parent location for several of the installation subdirectories.

**Table 2.14 MySQL Source-Configuration Option Reference (CMake)**

| Formats                                          | Description                                                      | Default           |
|--------------------------------------------------|------------------------------------------------------------------|-------------------|
| BUILD_CONFIG                                     | Use same build options as<br>official releases                   |                   |
| CMAKE_BUILD_TYPE                                 | Type of build to produce                                         | RelWithDebInfo    |
| CMAKE_CXX_FLAGS                                  | Flags for C++ Compiler                                           |                   |
| CMAKE_C_FLAGS                                    | Flags for C Compiler                                             |                   |
| CMAKE_INSTALL_PREFIX                             | Installation base directory                                      | /usr/local/mysql  |
| COMPILATION_COMMENT                              | Comment about compilation<br>environment                         |                   |
| CPACK_MONOLITHIC_INSTALL                         | Whether package build produces<br>single file                    | OFF               |
| DEFAULT_CHARSET                                  | The default server character set                                 | latin1            |
| DEFAULT_COLLATION                                | The default server collation                                     | latin1_swedish_ci |
| DISABLE_PSI_COND                                 | Exclude Performance Schema<br>condition instrumentation          | OFF               |
| DISABLE_PSI_FILE                                 | Exclude Performance Schema<br>file instrumentation               | OFF               |
| DISABLE_PSI_IDLE                                 | Exclude Performance Schema<br>idle instrumentation               | OFF               |
| DISABLE_PSI_MEMORY                               | Exclude Performance Schema<br>memory instrumentation             | OFF               |
| DISABLE_PSI_METADATA                             | Exclude Performance Schema<br>metadata instrumentation           | OFF               |
| DISABLE_PSI_MUTEX                                | Exclude Performance Schema<br>mutex instrumentation              | OFF               |
| DISABLE_PSI_PS                                   | Exclude the performance<br>schema prepared statements            | OFF               |
| DISABLE_PSI_RWLOCK                               | Exclude Performance Schema<br>rwlock instrumentation             | OFF               |
| DISABLE_PSI_SOCKET                               | Exclude Performance Schema<br>socket instrumentation             | OFF               |
| DISABLE_PSI_SP                                   | Exclude Performance Schema<br>stored program instrumentation     | OFF               |
| DISABLE_PSI_STAGE                                | Exclude Performance Schema<br>stage instrumentation              | OFF               |
| DISABLE_PSI_STATEMENT                            | Exclude Performance Schema<br>statement instrumentation          | OFF               |
| DISABLE_PSI_STATEMENT_DIGEST Exclude Performance | Schema statements_digest<br>instrumentation                      | OFF               |
| DISABLE_PSI_TABLE                                | Exclude Performance Schema<br>table instrumentation              | OFF               |
| DISABLE_PSI_THREAD                               | Exclude the performance<br>schema thread instrumentation         | OFF               |
| DISABLE_PSI_TRANSACTION                          | Exclude the performance<br>schema transaction<br>instrumentation | OFF               |

| Formats                                                   | Description                                                   | Default                  |
|-----------------------------------------------------------|---------------------------------------------------------------|--------------------------|
| DOWNLOAD_BOOST                                            | Whether to download the Boost<br>library                      | OFF                      |
| DOWNLOAD_BOOST_TIMEOUT                                    | Timeout in seconds for<br>downloading the Boost library       | 600                      |
| ENABLED_LOCAL_INFILE                                      | Whether to enable LOCAL for<br>LOAD DATA                      | OFF                      |
| ENABLED_PROFILING                                         | Whether to enable query profiling<br>code                     | ON                       |
| ENABLE_DOWNLOADS                                          | Whether to download optional<br>files                         | OFF                      |
| ENABLE_DTRACE                                             | Whether to include DTrace<br>support                          |                          |
| ENABLE_GCOV                                               | Whether to include gcov support                               |                          |
| ENABLE_GPROF                                              | Enable gprof (optimized Linux<br>builds only)                 | OFF                      |
| FORCE_UNSUPPORTED_COMPILERWhether to permit unsupported   | compilers                                                     | OFF                      |
| IGNORE_AIO_CHECK                                          | With -<br>DBUILD_CONFIG=mysql_release,<br>ignore libaio check | OFF                      |
| INSTALL_BINDIR                                            | User executables directory                                    | PREFIX/bin               |
| INSTALL_DOCDIR                                            | Documentation directory                                       | PREFIX/docs              |
| INSTALL_DOCREADMEDIR                                      | README file directory                                         | PREFIX                   |
| INSTALL_INCLUDEDIR                                        | Header file directory                                         | PREFIX/include           |
| INSTALL_INFODIR                                           | Info file directory                                           | PREFIX/docs              |
| INSTALL_LAYOUT                                            | Select predefined installation<br>layout                      | STANDALONE               |
| INSTALL_LIBDIR                                            | Library file directory                                        | PREFIX/lib               |
| INSTALL_MANDIR                                            | Manual page directory                                         | PREFIX/man               |
| INSTALL_MYSQLKEYRINGDIR                                   | Directory for keyring_file plugin<br>data file                | platform specific        |
| INSTALL_MYSQLSHAREDIR                                     | Shared data directory                                         | PREFIX/share             |
| INSTALL_MYSQLTESTDIR                                      | mysql-test directory                                          | PREFIX/mysql-test        |
| INSTALL_PKGCONFIGDIR                                      | Directory for mysqlclient.pc pkg<br>config file               | INSTALL_LIBDIR/pkgconfig |
| INSTALL_PLUGINDIR                                         | Plugin directory                                              | PREFIX/lib/plugin        |
| INSTALL_SBINDIR                                           | Server executable directory                                   | PREFIX/bin               |
| INSTALL_SCRIPTDIR                                         | Scripts directory                                             | PREFIX/scripts           |
| INSTALL_SECURE_FILE_PRIVDIRsecure_file_priv default value |                                                               | platform specific        |
| INSTALL_SECURE_FILE_PRIV_EMBEDDEDDIR                      | secure_file_priv default value for<br>libmysqld               |                          |
| INSTALL_SHAREDIR                                          | aclocal/mysql.m4 installation<br>directory                    | PREFIX/share             |
| INSTALL_SUPPORTFILESDIR                                   | Extra support files directory                                 | PREFIX/support-files     |
| MAX_INDEXES                                               | Maximum indexes per table                                     | 64                       |

| Formats                                                   | Description                                                                           | Default          |
|-----------------------------------------------------------|---------------------------------------------------------------------------------------|------------------|
| MUTEX_TYPE                                                | InnoDB mutex type                                                                     | event            |
| MYSQLX_TCP_PORT                                           | TCP/IP port number used by X<br>Plugin                                                | 33060            |
| MYSQLX_UNIX_ADDR                                          | Unix socket file used by X Plugin                                                     | /tmp/mysqlx.sock |
| MYSQL_DATADIR                                             | Data directory                                                                        |                  |
| MYSQL_MAINTAINER_MODE                                     | Whether to enable MySQL<br>maintainer-specific development<br>environment             | OFF              |
| MYSQL_PROJECT_NAME                                        | Windows/macOS project name                                                            | MySQL            |
| MYSQL_TCP_PORT                                            | TCP/IP port number                                                                    | 3306             |
| MYSQL_UNIX_ADDR                                           | Unix socket file                                                                      | /tmp/mysql.sock  |
| ODBC_INCLUDES                                             | ODBC includes directory                                                               |                  |
| ODBC_LIB_DIR                                              | ODBC library directory                                                                |                  |
| OPTIMIZER_TRACE                                           | Whether to support optimizer<br>tracing                                               |                  |
| REPRODUCIBLE_BUILD                                        | Take extra care to create a<br>build result independent of build<br>location and time |                  |
| SUNPRO_CXX_LIBRARY                                        | Client link library on Solaris 10+                                                    |                  |
| SYSCONFDIR                                                | Option file directory                                                                 |                  |
| SYSTEMD_PID_DIR                                           | Directory for PID file under<br>systemd                                               | /var/run/mysqld  |
| SYSTEMD_SERVICE_NAME                                      | Name of MySQL service under<br>systemd                                                | mysqld           |
| TMPDIR                                                    | tmpdir default value                                                                  |                  |
| WIN_DEBUG_NO_INLINE                                       | Whether to disable function<br>inlining                                               | OFF              |
| WITHOUT_SERVER                                            | Do not build the server; internal<br>use only                                         | OFF              |
| WITHOUT_xxx_STORAGE_ENGINEExclude storage engine xxx from | build                                                                                 |                  |
| WITH_ASAN                                                 | Enable AddressSanitizer                                                               | OFF              |
| WITH_ASAN_SCOPE                                           | Enable AddressSanitizer -<br>fsanitize-address-use-after<br>scope Clang flag          | OFF              |
| WITH_AUTHENTICATION_LDAP                                  | Whether to report error if LDAP<br>authentication plugins cannot be<br>built          | OFF              |
| WITH_AUTHENTICATION_PAM                                   | Build PAM authentication plugin                                                       | OFF              |
| WITH_AWS_SDK                                              | Location of Amazon Web<br>Services software development<br>kit                        |                  |
| WITH_BOOST                                                | The location of the Boost library<br>sources                                          |                  |

| Formats                                                          | Description                                                                                                                  | Default |
|------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------|---------|
| WITH_CLASSPATH                                                   | Classpath to use when building<br>MySQL Cluster Connector for<br>Java. Default is an empty string.                           |         |
| WITH_CLIENT_PROTOCOL_TRACING Build client-side protocol tracing  | framework                                                                                                                    | ON      |
| WITH_CURL                                                        | Location of curl library                                                                                                     |         |
| WITH_DEBUG                                                       | Whether to include debugging<br>support                                                                                      | OFF     |
| WITH_DEFAULT_COMPILER_OPTIONS Whether to use default compiler    | options                                                                                                                      | ON      |
| WITH_DEFAULT_FEATURE_SET                                         | Whether to use default feature<br>set                                                                                        | ON      |
| WITH_EDITLINE                                                    | Which libedit/editline library to<br>use                                                                                     | bundled |
| WITH_EMBEDDED_SERVER                                             | Whether to build embedded<br>server                                                                                          | OFF     |
| WITH_EMBEDDED_SHARED_LIBRARY Whether to build a shared           | embedded server library                                                                                                      | OFF     |
| WITH_ERROR_INSERT                                                | Enable error injection in the<br>NDB storage engine. Should<br>not be used for building binaries<br>intended for production. | OFF     |
| WITH_EXTRA_CHARSETS                                              | Which extra character sets to<br>include                                                                                     | all     |
| WITH_GMOCK                                                       | Path to googlemock distribution                                                                                              |         |
| WITH_INNODB_EXTRA_DEBUG                                          | Whether to include extra<br>debugging support for InnoDB.                                                                    | OFF     |
| WITH_INNODB_MEMCACHED                                            | Whether to generate<br>memcached shared libraries.                                                                           | OFF     |
| WITH_KEYRING_TEST                                                | Build the keyring test program                                                                                               | OFF     |
| WITH_LDAP                                                        | Internal use only                                                                                                            |         |
| WITH_LIBEVENT                                                    | Which libevent library to use                                                                                                | bundled |
| WITH_LIBWRAP                                                     | Whether to include libwrap (TCP<br>wrappers) support                                                                         | OFF     |
| WITH_LZ4                                                         | Type of LZ4 library support                                                                                                  | bundled |
| WITH_MECAB                                                       | Compiles MeCab                                                                                                               |         |
| WITH_MSAN                                                        | Enable MemorySanitizer                                                                                                       | OFF     |
| WITH_MSCRT_DEBUG                                                 | Enable Visual Studio CRT<br>memory leak tracing                                                                              | OFF     |
| WITH_NDBAPI_EXAMPLES                                             | Build API example programs.                                                                                                  | OFF     |
| WITH_NDBCLUSTER                                                  | NDB 8.0.30 and earlier: Build<br>NDB storage engine. NDB 8.0.31<br>and later: Deprecated; use<br>WITH_NDB instead            | ON      |
| WITH_NDBCLUSTER_STORAGE_ENGINE Prior to NDB 8.0.31, this was for | internal use only. NDB 8.0.31                                                                                                | ON      |

| Formats                 | Description                                                                                                                                                         | Default |
|-------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------|
|                         | and later: toggles (only) inclusion<br>of NDBCLUSTER storage engine                                                                                                 |         |
| WITH_NDBMTD             | Build multithreaded data node<br>binary                                                                                                                             | ON      |
| WITH_NDB_BINLOG         | Enable binary logging by default<br>by mysqld.                                                                                                                      | ON      |
| WITH_NDB_DEBUG          | Produce a debug build for testing<br>or troubleshooting.                                                                                                            | OFF     |
| WITH_NDB_JAVA           | Enable building of Java and<br>ClusterJ support. Enabled by<br>default. Supported in MySQL<br>Cluster only.                                                         | ON      |
| WITH_NDB_PORT           | Default port used by a<br>management server built with<br>this option. If this option was not<br>used to build it, the management<br>server's default port is 1186. | [none]  |
| WITH_NDB_TEST           | Include NDB API test programs.                                                                                                                                      | OFF     |
| WITH_NUMA               | Set NUMA memory allocation<br>policy                                                                                                                                |         |
| WITH_PROTOBUF           | Which Protocol Buffers package<br>to use                                                                                                                            | bundled |
| WITH_RAPID              | Whether to build rapid<br>development cycle plugins                                                                                                                 | ON      |
| WITH_SASL               | Internal use only                                                                                                                                                   |         |
| WITH_SSL                | Type of SSL support                                                                                                                                                 | system  |
| WITH_SYSTEMD            | Enable installation of systemd<br>support files                                                                                                                     | OFF     |
| WITH_TEST_TRACE_PLUGIN  | Build test protocol trace plugin                                                                                                                                    | OFF     |
| WITH_UBSAN              | Enable Undefined Behavior<br>Sanitizer                                                                                                                              | OFF     |
| WITH_UNIT_TESTS         | Compile MySQL with unit tests                                                                                                                                       | ON      |
| WITH_UNIXODBC           | Enable unixODBC support                                                                                                                                             | OFF     |
| WITH_VALGRIND           | Whether to compile in Valgrind<br>header files                                                                                                                      | OFF     |
| WITH_ZLIB               | Type of zlib support                                                                                                                                                | bundled |
| WITH_xxx_STORAGE_ENGINE | Compile storage engine xxx<br>statically into server                                                                                                                |         |

### <span id="page-14-1"></span><span id="page-14-0"></span>**General Options**

• [-DBUILD\\_CONFIG=mysql\\_release](#page-14-0)

This option configures a source distribution with the same build options used by Oracle to produce binary distributions for official MySQL releases.

<span id="page-14-2"></span>• [-DCMAKE\\_BUILD\\_TYPE=](#page-14-2)type

The type of build to produce:

- RelWithDebInfo: Enable optimizations and generate debugging information. This is the default MySQL build type.
- Debug: Disable optimizations and generate debugging information. This build type is also used if the [WITH\\_DEBUG](#page-24-0) option is enabled. That is, [-DWITH\\_DEBUG=1](#page-24-0) has the same effect as [-](#page-14-2) [DCMAKE\\_BUILD\\_TYPE=Debug](#page-14-2).
- <span id="page-15-1"></span>• [-DCPACK\\_MONOLITHIC\\_INSTALL=](#page-15-1)bool

This option affects whether the make package operation produces multiple installation package files or a single file. If disabled, the operation produces multiple installation package files, which may be useful if you want to install only a subset of a full MySQL installation. If enabled, it produces a single file for installing everything.

### <span id="page-15-2"></span>**Installation Layout Options**

The [CMAKE\\_INSTALL\\_PREFIX](#page-15-0) option indicates the base installation directory. Other options with names of the form INSTALL\_xxx that indicate component locations are interpreted relative to the prefix and their values are relative pathnames. Their values should not include the prefix.

<span id="page-15-0"></span>• [-DCMAKE\\_INSTALL\\_PREFIX=](#page-15-0)dir\_name

The installation base directory.

This value can be set at server startup using the --basedir option.

<span id="page-15-3"></span>• [-DINSTALL\\_BINDIR=](#page-15-3)dir\_name

Where to install user programs.

<span id="page-15-4"></span>• [-DINSTALL\\_DOCDIR=](#page-15-4)dir\_name

Where to install documentation.

<span id="page-15-5"></span>• [-DINSTALL\\_DOCREADMEDIR=](#page-15-5)dir\_name

Where to install README files.

<span id="page-15-6"></span>• [-DINSTALL\\_INCLUDEDIR=](#page-15-6)dir\_name

Where to install header files.

<span id="page-15-7"></span>• [-DINSTALL\\_INFODIR=](#page-15-7)dir\_name

Where to install Info files.

<span id="page-15-8"></span>• [-DINSTALL\\_LAYOUT=](#page-15-8)name

Select a predefined installation layout:

- STANDALONE: Same layout as used for .tar.gz and .zip packages. This is the default.
- RPM: Layout similar to RPM packages.
- SVR4: Solaris package layout.
- DEB: DEB package layout (experimental).

You can select a predefined layout but modify individual component installation locations by specifying other options. For example:

```
cmake . -DINSTALL_LAYOUT=SVR4 -DMYSQL_DATADIR=/var/mysql/data
```

The [INSTALL\\_LAYOUT](#page-15-8) value determines the default value of the secure\_file\_priv, keyring\_encrypted\_file\_data, and keyring\_file\_data system variables. See the descriptions of those variables in Section 5.1.7, "Server System Variables", and Section 6.4.4.12, "Keyring System Variables".

<span id="page-16-0"></span>• [-DINSTALL\\_LIBDIR=](#page-16-0)dir\_name

Where to install library files.

<span id="page-16-1"></span>• [-DINSTALL\\_MANDIR=](#page-16-1)dir\_name

Where to install manual pages.

<span id="page-16-2"></span>• [-DINSTALL\\_MYSQLKEYRINGDIR=](#page-16-2)dir\_path

The default directory to use as the location of the keyring\_file plugin data file. The default value is platform specific and depends on the value of the [INSTALL\\_LAYOUT](#page-15-8) CMake option; see the description of the keyring\_file\_data system variable in Section 5.1.7, "Server System Variables".

This option was added in MySQL 5.7.11.

<span id="page-16-3"></span>• [-DINSTALL\\_MYSQLSHAREDIR=](#page-16-3)dir\_name

Where to install shared data files.

<span id="page-16-4"></span>• [-DINSTALL\\_MYSQLTESTDIR=](#page-16-4)dir\_name

Where to install the mysql-test directory. To suppress installation of this directory, explicitly set the option to the empty value ([-DINSTALL\\_MYSQLTESTDIR=](#page-16-4)).

<span id="page-16-5"></span>• [-DINSTALL\\_PKGCONFIGDIR=](#page-16-5)dir\_name

The directory in which to install the mysqlclient.pc file for use by pkg-config. The default value is INSTALL\_LIBDIR/pkgconfig, unless [INSTALL\\_LIBDIR](#page-16-0) ends with /mysql, in which case that is removed first.

<span id="page-16-6"></span>• [-DINSTALL\\_PLUGINDIR=](#page-16-6)dir\_name

The location of the plugin directory.

This value can be set at server startup with the --plugin\_dir option.

<span id="page-16-7"></span>• [-DINSTALL\\_SBINDIR=](#page-16-7)dir\_name

Where to install the [mysqld](#page-144-0) server.

<span id="page-16-8"></span>• [-DINSTALL\\_SCRIPTDIR=](#page-16-8)dir\_name

Where to install [mysql\\_install\\_db](#page-162-0).

<span id="page-16-9"></span>• [-DINSTALL\\_SECURE\\_FILE\\_PRIVDIR=](#page-16-9)dir\_name

The default value for the secure\_file\_priv system variable. The default value is platform specific and depends on the value of the [INSTALL\\_LAYOUT](#page-15-8) CMake option; see the description of the secure\_file\_priv system variable in Section 5.1.7, "Server System Variables".

To set the value for the libmysqld embedded server, use [INSTALL\\_SECURE\\_FILE\\_PRIV\\_EMBEDDEDDIR](#page-17-1).

<span id="page-17-1"></span>• [-DINSTALL\\_SECURE\\_FILE\\_PRIV\\_EMBEDDEDDIR=](#page-17-1)dir\_name

The default value for the secure\_file\_priv system variable, for the libmysqld embedded server.

![](_page_17_Picture_3.jpeg)

#### **Note**

The libmysqld embedded server library is deprecated as of MySQL 5.7.19; expect it to be removed in MySQL 8.0.

<span id="page-17-2"></span>• [-DINSTALL\\_SHAREDIR=](#page-17-2)dir\_name

Where to install aclocal/mysql.m4.

<span id="page-17-3"></span>• [-DINSTALL\\_SUPPORTFILESDIR=](#page-17-3)dir\_name

Where to install extra support files.

<span id="page-17-4"></span>• [-DMYSQL\\_DATADIR=](#page-17-4)dir\_name

The location of the MySQL data directory.

This value can be set at server startup with the --datadir option.

<span id="page-17-5"></span>• [-DODBC\\_INCLUDES=](#page-17-5)dir\_name

The location of the ODBC includes directory, which may be used while configuring Connector/ODBC.

<span id="page-17-6"></span>• [-DODBC\\_LIB\\_DIR=](#page-17-6)dir\_name

The location of the ODBC library directory, which may be used while configuring Connector/ODBC.

<span id="page-17-7"></span>• [-DSYSCONFDIR=](#page-17-7)dir\_name

The default my.cnf option file directory.

This location cannot be set at server startup, but you can start the server with a given option file using the [--defaults-file=](#page-121-0)file\_name option, where file\_name is the full path name to the file.

<span id="page-17-8"></span>• [-DSYSTEMD\\_PID\\_DIR=](#page-17-8)dir\_name

The name of the directory in which to create the PID file when MySQL is managed by systemd. The default is /var/run/mysqld; this might be changed implicitly according to the [INSTALL\\_LAYOUT](#page-15-8) value.

This option is ignored unless [WITH\\_SYSTEMD](#page-27-1) is enabled.

<span id="page-17-9"></span>• [-DSYSTEMD\\_SERVICE\\_NAME=](#page-17-9)name

The name of the MySQL service to use when MySQL is managed by systemd. The default is mysqld; this might be changed implicitly according to the [INSTALL\\_LAYOUT](#page-15-8) value.

This option is ignored unless [WITH\\_SYSTEMD](#page-27-1) is enabled.

<span id="page-17-10"></span>• [-DTMPDIR=](#page-17-10)dir\_name

The default location to use for the tmpdir system variable. If unspecified, the value defaults to P\_tmpdir in <stdio.h>.

### <span id="page-17-0"></span>**Storage Engine Options**

Storage engines are built as plugins. You can build a plugin as a static module (compiled into the server) or a dynamic module (built as a dynamic library that must be installed into the server using the INSTALL PLUGIN statement or the --plugin-load option before it can be used). Some plugins might not support static or dynamic building.

The InnoDB, MyISAM, MERGE, MEMORY, and CSV engines are mandatory (always compiled into the server) and need not be installed explicitly.

To compile a storage engine statically into the server, use -DWITH\_engine\_STORAGE\_ENGINE=1. Some permissible engine values are ARCHIVE, BLACKHOLE, EXAMPLE, FEDERATED, and PARTITION (partitioning support). Examples:

```
-DWITH_ARCHIVE_STORAGE_ENGINE=1
-DWITH_BLACKHOLE_STORAGE_ENGINE=1
```

To build MySQL with support for NDB Cluster, use the [WITH\\_NDBCLUSTER](#page-29-4) option.

![](_page_18_Picture_6.jpeg)

#### **Note**

WITH\_NDBCLUSTER is supported only when building NDB Cluster using the NDB Cluster sources. It cannot be used to enable clustering support in other MySQL source trees or distributions. In NDB Cluster source distributions, it is enabled by default. See Section 21.3.1.4, "Building NDB Cluster from Source on Linux", and Section 21.3.2.2, "Compiling and Installing NDB Cluster from Source on Windows", for more information.

![](_page_18_Picture_9.jpeg)

#### **Note**

It is not possible to compile without Performance Schema support. If it is desired to compile without particular types of instrumentation, that can be done with the following CMake options:

```
DISABLE_PSI_COND
DISABLE_PSI_FILE
DISABLE_PSI_IDLE
DISABLE_PSI_MEMORY
DISABLE_PSI_METADATA
DISABLE_PSI_MUTEX
DISABLE_PSI_PS
DISABLE_PSI_RWLOCK
DISABLE_PSI_SOCKET
DISABLE_PSI_SP
DISABLE_PSI_STAGE
DISABLE_PSI_STATEMENT
DISABLE_PSI_STATEMENT_DIGEST
DISABLE_PSI_TABLE
DISABLE_PSI_THREAD
DISABLE_PSI_TRANSACTION
```

For example, to compile without mutex instrumentation, configure MySQL using [-DDISABLE\\_PSI\\_MUTEX=1](#page-19-9).

To exclude a storage engine from the build, use -DWITH\_engine\_STORAGE\_ENGINE=0. Examples:

```
-DWITH_EXAMPLE_STORAGE_ENGINE=0
-DWITH_FEDERATED_STORAGE_ENGINE=0
-DWITH_PARTITION_STORAGE_ENGINE=0
```

It is also possible to exclude a storage engine from the build using -

DWITHOUT\_engine\_STORAGE\_ENGINE=1 (but -DWITH\_engine\_STORAGE\_ENGINE=0 is preferred). Examples:

```
-DWITHOUT_EXAMPLE_STORAGE_ENGINE=1
-DWITHOUT_FEDERATED_STORAGE_ENGINE=1
-DWITHOUT_PARTITION_STORAGE_ENGINE=1
```

If neither -DWITH\_engine\_STORAGE\_ENGINE nor -DWITHOUT\_engine\_STORAGE\_ENGINE are specified for a given storage engine, the engine is built as a shared module, or excluded if it cannot be built as a shared module.

### <span id="page-19-1"></span><span id="page-19-0"></span>**Feature Options**

• [-DCOMPILATION\\_COMMENT=](#page-19-1)string

A descriptive comment about the compilation environment.

<span id="page-19-2"></span>• [-DDEFAULT\\_CHARSET=](#page-19-2)charset\_name

The server character set. By default, MySQL uses the latin1 (cp1252 West European) character set.

charset\_name may be one of binary, armscii8, ascii, big5, cp1250, cp1251, cp1256, cp1257, cp850, cp852, cp866, cp932, dec8, eucjpms, euckr, gb2312, gbk, geostd8, greek, hebrew, hp8, keybcs2, koi8r, koi8u, latin1, latin2, latin5, latin7, macce, macroman, sjis, swe7, tis620, ucs2, ujis, utf8, utf8mb4, utf16, utf16le, utf32. The permissible character sets are listed in the cmake/character\_sets.cmake file as the value of CHARSETS\_AVAILABLE.

This value can be set at server startup with the --character-set-server option.

<span id="page-19-3"></span>• [-DDEFAULT\\_COLLATION=](#page-19-3)collation\_name

The server collation. By default, MySQL uses latin1\_swedish\_ci. Use the SHOW COLLATION statement to determine which collations are available for each character set.

This value can be set at server startup with the --collation\_server option.

<span id="page-19-4"></span>• [-DDISABLE\\_PSI\\_COND=](#page-19-4)bool

Whether to exclude the Performance Schema condition instrumentation. The default is OFF (include).

<span id="page-19-5"></span>• [-DDISABLE\\_PSI\\_FILE=](#page-19-5)bool

Whether to exclude the Performance Schema file instrumentation. The default is OFF (include).

<span id="page-19-6"></span>• [-DDISABLE\\_PSI\\_IDLE=](#page-19-6)bool

Whether to exclude the Performance Schema idle instrumentation. The default is OFF (include).

<span id="page-19-7"></span>• [-DDISABLE\\_PSI\\_MEMORY=](#page-19-7)bool

Whether to exclude the Performance Schema memory instrumentation. The default is OFF (include).

<span id="page-19-8"></span>• [-DDISABLE\\_PSI\\_METADATA=](#page-19-8)bool

Whether to exclude the Performance Schema metadata instrumentation. The default is OFF (include).

<span id="page-19-9"></span>• [-DDISABLE\\_PSI\\_MUTEX=](#page-19-9)bool

Whether to exclude the Performance Schema mutex instrumentation. The default is OFF (include).

<span id="page-19-10"></span>• [-DDISABLE\\_PSI\\_RWLOCK=](#page-19-10)bool

Whether to exclude the Performance Schema rwlock instrumentation. The default is OFF (include).

<span id="page-19-11"></span>• [-DDISABLE\\_PSI\\_SOCKET=](#page-19-11)bool

Whether to exclude the Performance Schema socket instrumentation. The default is OFF (include).

<span id="page-19-12"></span>• [-DDISABLE\\_PSI\\_SP=](#page-19-12)bool

Whether to exclude the Performance Schema stored program instrumentation. The default is OFF (include).

<span id="page-20-1"></span>• [-DDISABLE\\_PSI\\_STAGE=](#page-20-1)bool

Whether to exclude the Performance Schema stage instrumentation. The default is OFF (include).

<span id="page-20-2"></span>• [-DDISABLE\\_PSI\\_STATEMENT=](#page-20-2)bool

Whether to exclude the Performance Schema statement instrumentation. The default is OFF (include).

<span id="page-20-3"></span>• [-DDISABLE\\_PSI\\_STATEMENT\\_DIGEST=](#page-20-3)bool

Whether to exclude the Performance Schema statement digest instrumentation. The default is OFF (include).

<span id="page-20-4"></span>• [-DDISABLE\\_PSI\\_TABLE=](#page-20-4)bool

Whether to exclude the Performance Schema table instrumentation. The default is OFF (include).

<span id="page-20-0"></span>• [-DDISABLE\\_PSI\\_PS=](#page-20-0)bool

Exclude the Performance Schema prepared statements instances instrumentation. The default is OFF (include).

<span id="page-20-5"></span>• [-DDISABLE\\_PSI\\_THREAD=](#page-20-5)bool

Exclude the Performance Schema thread instrumentation. The default is OFF (include).

Only disable threads when building without any instrumentation, because other instrumentations have a dependency on threads.

<span id="page-20-6"></span>• [-DDISABLE\\_PSI\\_TRANSACTION=](#page-20-6)bool

Exclude the Performance Schema transaction instrumentation. The default is OFF (include).

<span id="page-20-7"></span>• [-DDOWNLOAD\\_BOOST=](#page-20-7)bool

Whether to download the Boost library. The default is OFF.

See the [WITH\\_BOOST](#page-23-0) option for additional discussion about using Boost.

<span id="page-20-8"></span>• [-DDOWNLOAD\\_BOOST\\_TIMEOUT=](#page-20-8)seconds

The timeout in seconds for downloading the Boost library. The default is 600 seconds.

See the [WITH\\_BOOST](#page-23-0) option for additional discussion about using Boost.

<span id="page-20-9"></span>• [-DENABLE\\_DOWNLOADS=](#page-20-9)bool

Whether to download optional files. For example, with this option enabled, CMake downloads the Google Test distribution that is used by the test suite to run unit tests.

<span id="page-20-10"></span>• [-DENABLE\\_DTRACE=](#page-20-10)bool

Whether to include support for DTrace probes. For information about DTrace, wee Section 5.8.4, "Tracing mysqld Using DTrace"

This option is deprecated because support for DTrace is deprecated in MySQL 5.7 and is removed in MySQL 8.0.

<span id="page-20-11"></span>• [-DENABLE\\_GCOV=](#page-20-11)bool

Whether to include gcov support (Linux only).

<span id="page-20-12"></span>• [-DENABLE\\_GPROF=](#page-20-12)bool

Whether to enable gprof (optimized Linux builds only).

<span id="page-21-1"></span>• [-DENABLED\\_LOCAL\\_INFILE=](#page-21-1)bool

This option controls the compiled-in default LOCAL capability for the MySQL client library. Clients that make no explicit arrangements therefore have LOCAL capability disabled or enabled according to the [ENABLED\\_LOCAL\\_INFILE](#page-21-1) setting specified at MySQL build time.

By default, the client library in MySQL binary distributions is compiled with [ENABLED\\_LOCAL\\_INFILE](#page-21-1) disabled. (Prior to MySQL 5.7.6, it was enabled by default.) If you compile MySQL from source, configure it with [ENABLED\\_LOCAL\\_INFILE](#page-21-1) disabled or enabled based on whether clients that make no explicit arrangements should have LOCAL capability disabled or enabled, respectively.

[ENABLED\\_LOCAL\\_INFILE](#page-21-1) controls the default for client-side LOCAL capability. For the server, the local\_infile system variable controls server-side LOCAL capability. To explicitly cause the server to refuse or permit LOAD DATA LOCAL statements (regardless of how client programs and libraries are configured at build time or runtime), start [mysqld](#page-144-0) with --local-infile disabled or enabled, respectively. local\_infile can also be set at runtime. See Section 6.1.6, "Security Considerations for LOAD DATA LOCAL".

<span id="page-21-2"></span>• [-DENABLED\\_PROFILING=](#page-21-2)bool

Whether to enable query profiling code (for the SHOW PROFILE and SHOW PROFILES statements).

<span id="page-21-0"></span>• [-DFORCE\\_UNSUPPORTED\\_COMPILER=](#page-21-0)bool

By default, CMake checks for minimum versions of supported compilers: Visual Studio 2013 (Windows); GCC 4.4 or Clang 3.3 (Linux); Developer Studio 12.5 (Solaris server); Developer Studio 12.2 or GCC 4.4 (Solaris client library); Clang 3.3 (macOS), Clang 3.3 (FreeBSD). To disable this check, use [-DFORCE\\_UNSUPPORTED\\_COMPILER=ON](#page-21-0).

<span id="page-21-3"></span>• [-DIGNORE\\_AIO\\_CHECK=](#page-21-3)bool

If the [-DBUILD\\_CONFIG=mysql\\_release](#page-14-0) option is given on Linux, the libaio library must be linked in by default. If you do not have libaio or do not want to install it, you can suppress the check for it by specifying [-DIGNORE\\_AIO\\_CHECK=1](#page-21-3).

<span id="page-21-4"></span>• [-DMAX\\_INDEXES=](#page-21-4)num

The maximum number of indexes per table. The default is 64. The maximum is 255. Values smaller than 64 are ignored and the default of 64 is used.

<span id="page-21-7"></span>• [-DMYSQL\\_MAINTAINER\\_MODE=](#page-21-7)bool

Whether to enable a MySQL maintainer-specific development environment. If enabled, this option causes compiler warnings to become errors.

<span id="page-21-5"></span>• [-DMUTEX\\_TYPE=](#page-21-5)type

The mutex type used by InnoDB. Options include:

- event: Use event mutexes. This is the default value and the original InnoDB mutex implementation.
- sys: Use POSIX mutexes on UNIX systems. Use CRITICAL\_SECTION objects on Windows, if available.
- futex: Use Linux futexes instead of condition variables to schedule waiting threads.
- <span id="page-21-6"></span>• [-DMYSQLX\\_TCP\\_PORT=](#page-21-6)port\_num

The port number on which X Plugin listens for TCP/IP connections. The default is 33060.

This value can be set at server startup with the mysqlx\_port system variable.

<span id="page-22-2"></span>• [-DMYSQLX\\_UNIX\\_ADDR=](#page-22-2)file\_name

The Unix socket file path on which the server listens for X Plugin socket connections. This must be an absolute path name. The default is /tmp/mysqlx.sock.

This value can be set at server startup with the mysqlx\_port system variable.

<span id="page-22-3"></span>• [-DMYSQL\\_PROJECT\\_NAME=](#page-22-3)name

For Windows or macOS, the project name to incorporate into the project file name.

<span id="page-22-0"></span>• [-DMYSQL\\_TCP\\_PORT=](#page-22-0)port\_num

The port number on which the server listens for TCP/IP connections. The default is 3306.

This value can be set at server startup with the --port option.

<span id="page-22-1"></span>• [-DMYSQL\\_UNIX\\_ADDR=](#page-22-1)file\_name

The Unix socket file path on which the server listens for socket connections. This must be an absolute path name. The default is /tmp/mysql.sock.

This value can be set at server startup with the --socket option.

<span id="page-22-4"></span>• [-DOPTIMIZER\\_TRACE=](#page-22-4)bool

Whether to support optimizer tracing. See Section 8.15, "Tracing the Optimizer".

<span id="page-22-5"></span>• [-DREPRODUCIBLE\\_BUILD=](#page-22-5)bool

For builds on Linux systems, this option controls whether to take extra care to create a build result independent of build location and time.

This option was added in MySQL 5.7.19.

<span id="page-22-6"></span>• [-DWIN\\_DEBUG\\_NO\\_INLINE=](#page-22-6)bool

Whether to disable function inlining on Windows. The default is OFF (inlining enabled).

<span id="page-22-7"></span>• [-DWITH\\_ASAN=](#page-22-7)bool

Whether to enable the AddressSanitizer, for compilers that support it. The default is OFF.

<span id="page-22-8"></span>• [-DWITH\\_ASAN\\_SCOPE=](#page-22-8)bool

Whether to enable the AddressSanitizer -fsanitize-address-use-after-scope Clang flag for use-after-scope detection. The default is off. To use this option, -DWITH\_ASAN must also be enabled.

<span id="page-22-9"></span>• [-DWITH\\_AUTHENTICATION\\_LDAP=](#page-22-9)bool

Whether to report an error if the LDAP authentication plugins cannot be built:

- If this option is disabled (the default), the LDAP plugins are built if the required header files and libraries are found. If they are not, CMake displays a note about it.
- If this option is enabled, a failure to find the required header file and libraries causes CMake to produce an error, preventing the server from being built.

For information about LDAP authentication, see Section 6.4.1.9, "LDAP Pluggable Authentication". This option was added in MySQL 5.7.19.

<span id="page-23-1"></span>• [-DWITH\\_AUTHENTICATION\\_PAM=](#page-23-1)bool

Whether to build the PAM authentication plugin, for source trees that include this plugin. (See Section 6.4.1.7, "PAM Pluggable Authentication".) If this option is specified and the plugin cannot be compiled, the build fails.

<span id="page-23-2"></span>• [-DWITH\\_AWS\\_SDK=](#page-23-2)path\_name

The location of the Amazon Web Services software development kit.

This option was added in MySQL 5.7.19.

<span id="page-23-0"></span>• [-DWITH\\_BOOST=](#page-23-0)path\_name

The Boost library is required to build MySQL. These CMake options enable control over the library source location, and whether to download it automatically:

• [-DWITH\\_BOOST=](#page-23-0)path\_name specifies the Boost library directory location. It is also possible to specify the Boost location by setting the BOOST\_ROOT or WITH\_BOOST environment variable.

As of MySQL 5.7.11, [-DWITH\\_BOOST=system](#page-23-0) is also permitted and indicates that the correct version of Boost is installed on the compilation host in the standard location. In this case, the installed version of Boost is used rather than any version included with a MySQL source distribution.

- [-DDOWNLOAD\\_BOOST=](#page-20-7)bool specifies whether to download the Boost source if it is not present in the specified location. The default is OFF.
- [-DDOWNLOAD\\_BOOST\\_TIMEOUT=](#page-20-8)seconds the timeout in seconds for downloading the Boost library. The default is 600 seconds.

For example, if you normally build MySQL placing the object output in the bld subdirectory of your MySQL source tree, you can build with Boost like this:

```
mkdir bld
cd bld
cmake .. -DDOWNLOAD_BOOST=ON -DWITH_BOOST=$HOME/my_boost
```

This causes Boost to be downloaded into the my\_boost directory under your home directory. If the required Boost version is already there, no download is done. If the required Boost version changes, the newer version is downloaded.

If Boost is already installed locally and your compiler finds the Boost header files on its own, it may not be necessary to specify the preceding CMake options. However, if the version of Boost required by MySQL changes and the locally installed version has not been upgraded, you may have build problems. Using the CMake options should give you a successful build.

With the above settings that allow Boost download into a specified location, when the required Boost version changes, you need to remove the bld folder, recreate it, and perform the cmake step again. Otherwise, the new Boost version might not get downloaded, and compilation might fail.

<span id="page-24-1"></span>• [-DWITH\\_CLIENT\\_PROTOCOL\\_TRACING=](#page-24-1)bool

Whether to build the client-side protocol tracing framework into the client library. By default, this option is enabled.

For information about writing protocol trace client plugins, see [Writing Protocol Trace Plugins.](https://dev.mysql.com/doc/extending-mysql/5.7/en/writing-protocol-trace-plugins.md)

See also the [WITH\\_TEST\\_TRACE\\_PLUGIN](#page-27-2) option.

<span id="page-24-2"></span>• [-DWITH\\_CURL=](#page-24-2)curl\_type

The location of the curl library. curl\_type can be system (use the system curl library) or a path name to the curl library.

This option was added in MySQL 5.7.19.

<span id="page-24-0"></span>• [-DWITH\\_DEBUG=](#page-24-0)bool

Whether to include debugging support.

Configuring MySQL with debugging support enables you to use the --debug="d,parser\_debug" option when you start the server. This causes the Bison parser that is used to process SQL statements to dump a parser trace to the server's standard error output. Typically, this output is written to the error log.

Sync debug checking for the InnoDB storage engine is defined under UNIV\_DEBUG and is available when debugging support is compiled in using the [WITH\\_DEBUG](#page-24-0) option. When debugging support is compiled in, the innodb\_sync\_debug configuration option can be used to enable or disable InnoDB sync debug checking.

As of MySQL 5.7.18, enabling [WITH\\_DEBUG](#page-24-0) also enables Debug Sync. For a description of the Debug Sync facility and how to use synchronization points, see [MySQL Internals: Test](https://dev.mysql.com/doc/internals/en/test-synchronization.md) [Synchronization](https://dev.mysql.com/doc/internals/en/test-synchronization.md).

<span id="page-24-3"></span>• [-DWITH\\_DEFAULT\\_FEATURE\\_SET=](#page-24-3)bool

Whether to use the flags from cmake/build\_configurations/feature\_set.cmake.

<span id="page-24-4"></span>• [-DWITH\\_EDITLINE=](#page-24-4)value

Which libedit/editline library to use. The permitted values are bundled (the default) and system.

[WITH\\_EDITLINE](#page-24-4) replaces WITH\_LIBEDIT, which has been removed.

<span id="page-24-5"></span>• [-DWITH\\_EMBEDDED\\_SERVER=](#page-24-5)bool

Whether to build the libmysqld embedded server library.

![](_page_24_Picture_20.jpeg)

#### **Note**

The libmysqld embedded server library is deprecated as of MySQL 5.7.17 and has been removed in MySQL 8.0.

<span id="page-24-6"></span>• [-DWITH\\_EMBEDDED\\_SHARED\\_LIBRARY=](#page-24-6)bool

Whether to build a shared libmysqld embedded server library.

![](_page_24_Picture_25.jpeg)

### **Note**

The libmysqld embedded server library is deprecated as of MySQL 5.7.17 and has been removed in MySQL 8.0. 197 <span id="page-25-0"></span>• [-DWITH\\_EXTRA\\_CHARSETS=](#page-25-0)name

Which extra character sets to include:

- all: All character sets. This is the default.
- complex: Complex character sets.
- none: No extra character sets.
- <span id="page-25-1"></span>• [-DWITH\\_GMOCK=](#page-25-1)path\_name

The path to the googlemock distribution, for use with Google Test-based unit tests. The option value is the path to the distribution Zip file. Alternatively, set the WITH\_GMOCK environment variable to the path name. It is also possible to use -DENABLE\_DOWNLOADS=1, in which case CMake downloads the distribution from GitHub.

If you build MySQL without the Google Test unit tests (by configuring wihout [WITH\\_GMOCK](#page-25-1)), CMake displays a message indicating how to download it.

<span id="page-25-2"></span>• [-DWITH\\_INNODB\\_EXTRA\\_DEBUG=](#page-25-2)bool

Whether to include extra InnoDB debugging support.

Enabling WITH\_INNODB\_EXTRA\_DEBUG turns on extra InnoDB debug checks. This option can only be enabled when [WITH\\_DEBUG](#page-24-0) is enabled.

<span id="page-25-3"></span>• [-DWITH\\_INNODB\\_MEMCACHED=](#page-25-3)bool

Whether to generate memcached shared libraries (libmemcached.so and innodb\_engine.so).

<span id="page-25-4"></span>• [-DWITH\\_KEYRING\\_TEST=](#page-25-4)bool

Whether to build the test program that accompanies the keyring\_file plugin. The default is OFF. Test file source code is located in the plugin/keyring/keyring-test directory.

This option was added in MySQL 5.7.11.

<span id="page-25-5"></span>• [-DWITH\\_LDAP=](#page-25-5)value

Internal use only. This option was added in MySQL 5.7.29.

<span id="page-25-6"></span>• [-DWITH\\_LIBEVENT=](#page-25-6)string

Which libevent library to use. Permitted values are bundled (default) and system. Prior to MySQL 5.7.31, if you specify system, the system libevent library is used if present, and an error occurs otherwise. In MySQL 5.7.31 and later, if system is specified and no system libevent library can be found, an error occurs regardless, and the bundled libevent is not used.

The libevent library is required by InnoDB memcached and X Plugin.

<span id="page-25-7"></span>• [-DWITH\\_LIBWRAP=](#page-25-7)bool

Whether to include libwrap (TCP wrappers) support.

<span id="page-25-8"></span>• [-DWITH\\_LZ4=](#page-25-8)lz4\_type

The [WITH\\_LZ4](#page-25-8) option indicates the source of zlib support:

- bundled: Use the lz4 library bundled with the distribution. This is the default.
- system: Use the system lz4 library. If [WITH\\_LZ4](#page-25-8) is set to this value, the lz4\_decompress utility is not built. In this case, the system lz4 command can be used instead.

<span id="page-26-0"></span>• [-DWITH\\_MECAB={disabled|system|](#page-26-0)path\_name}

Use this option to compile the MeCab parser. If you have installed MeCab to its default installation directory, set -DWITH\_MECAB=system. The system option applies to MeCab installations performed from source or from binaries using a native package management utility. If you installed MeCab to a custom installation directory, specify the path to the MeCab installation, for example, - DWITH\_MECAB=/opt/mecab. If the system option does not work, specifying the MeCab installation path should work in all cases.

For related information, see Section 12.9.9, "MeCab Full-Text Parser Plugin".

<span id="page-26-1"></span>• [-DWITH\\_MSAN=](#page-26-1)bool

Whether to enable MemorySanitizer, for compilers that support it. The default is off.

For this option to have an effect if enabled, all libraries linked to MySQL must also have been compiled with the option enabled.

<span id="page-26-2"></span>• [-DWITH\\_MSCRT\\_DEBUG=](#page-26-2)bool

Whether to enable Visual Studio CRT memory leak tracing. The default is OFF.

<span id="page-26-3"></span>• [-DWITH\\_NUMA=](#page-26-3)bool

Explicitly set the NUMA memory allocation policy. CMake sets the default [WITH\\_NUMA](#page-26-3) value based on whether the current platform has NUMA support. For platforms without NUMA support, CMake behaves as follows:

- With no NUMA option (the normal case), CMake continues normally, producing only this warning: NUMA library missing or required version not available.
- With [-DWITH\\_NUMA=ON](#page-26-3), CMake aborts with this error: NUMA library missing or required version not available.

This option was added in MySQL 5.7.17.

<span id="page-26-4"></span>• [-DWITH\\_PROTOBUF=](#page-26-4)protobuf\_type

Which Protocol Buffers package to use. protobuf\_type can be one of the following values:

- bundled: Use the package bundled with the distribution. This is the default.
- system: Use the package installed on the system.

Other values are ignored, with a fallback to bundled.

This option was added in MySQL 5.7.12.

<span id="page-26-5"></span>• [-DWITH\\_RAPID=](#page-26-5)bool

Whether to build the rapid development cycle plugins. When enabled, a rapid directory is created in the build tree containing these plugins. When disabled, no rapid directory is created in the build tree. The default is ON, unless the rapid directory is removed from the source tree, in which case the default becomes OFF. This option was added in MySQL 5.7.12.

<span id="page-26-6"></span>• [-DWITH\\_SASL=](#page-26-6)value

Internal use only. This option was added in MySQL 5.7.29. Not supported on Windows.

<span id="page-27-0"></span>• [-DWITH\\_SSL={](#page-27-0)ssl\_type|path\_name}

For support of encrypted connections, entropy for random number generation, and other encryptionrelated operations, MySQL must be built using an SSL library. This option specifies which SSL library to use.

- ssl\_type can be one of the following values:
  - yes: Use the system OpenSSL library if present, else the library bundled with the distribution.
  - bundled: Use the SSL library bundled with the distribution. This is the default prior to MySQL 5.7.28. As of 5.7.28, this is no longer a permitted value and the default is system.
  - system: Use the system OpenSSL library. This is the default as of MySQL 5.7.28.
- path\_name is the path name to the OpenSSL installation to use. This can be preferable to using the ssl\_type value of system because it can prevent CMake from detecting and using an older or incorrect OpenSSL version installed on the system. (Another permitted way to do the same thing is to set WITH\_SSL to system and set the CMAKE\_PREFIX\_PATH option to path\_name.)

For additional information about configuring the SSL library, see [Section 2.8.6, "Configuring SSL](#page-8-0) [Library Support".](#page-8-0)

<span id="page-27-1"></span>• [-DWITH\\_SYSTEMD=](#page-27-1)bool

Whether to enable installation of systemd support files. By default, this option is disabled. When enabled, systemd support files are installed, and scripts such as [mysqld\\_safe](#page-144-1) and the System V initialization script are not installed. On platforms where systemd is not available, enabling [WITH\\_SYSTEMD](#page-27-1) results in an error from CMake.

For more information about using systemd, see Section 2.5.10, "Managing MySQL Server with systemd". That section also includes information about specifying options otherwise specified in [mysqld\_safe] option groups. Because [mysqld\\_safe](#page-144-1) is not installed when systemd is used, such options must be specified another way.

<span id="page-27-2"></span>• [-DWITH\\_TEST\\_TRACE\\_PLUGIN=](#page-27-2)bool

Whether to build the test protocol trace client plugin (see [Using the Test Protocol Trace](https://dev.mysql.com/doc/extending-mysql/5.7/en/test-protocol-trace-plugin.md) [Plugin\)](https://dev.mysql.com/doc/extending-mysql/5.7/en/test-protocol-trace-plugin.md). By default, this option is disabled. Enabling this option has no effect unless the [WITH\\_CLIENT\\_PROTOCOL\\_TRACING](#page-24-1) option is enabled. If MySQL is configured with both options enabled, the libmysqlclient client library is built with the test protocol trace plugin built in, and all the standard MySQL clients load the plugin. However, even when the test plugin is enabled, it has no effect by default. Control over the plugin is afforded using environment variables; see [Using the Test](https://dev.mysql.com/doc/extending-mysql/5.7/en/test-protocol-trace-plugin.md) [Protocol Trace Plugin.](https://dev.mysql.com/doc/extending-mysql/5.7/en/test-protocol-trace-plugin.md)

![](_page_27_Picture_14.jpeg)

#### **Note**

Do not enable the [WITH\\_TEST\\_TRACE\\_PLUGIN](#page-27-2) option if you want to use your own protocol trace plugins because only one such plugin can be loaded at a time and an error occurs for attempts to load a second one. If you have already built MySQL with the test protocol trace plugin enabled to see how it works, you must rebuild MySQL without it before you can use your own plugins.

For information about writing trace plugins, see [Writing Protocol Trace Plugins](https://dev.mysql.com/doc/extending-mysql/5.7/en/writing-protocol-trace-plugins.md).

<span id="page-27-3"></span>• [-DWITH\\_UBSAN=](#page-27-3)bool

Whether to enable the Undefined Behavior Sanitizer, for compilers that support it. The default is off.

<span id="page-28-6"></span>• [-DWITH\\_UNIT\\_TESTS={ON|OFF}](#page-28-6)

If enabled, compile MySQL with unit tests. The default is ON unless the server is not being compiled.

<span id="page-28-7"></span>• [-DWITH\\_UNIXODBC=](#page-28-7)1

Enables unixODBC support, for Connector/ODBC.

<span id="page-28-8"></span>• [-DWITH\\_VALGRIND=](#page-28-8)bool

Whether to compile in the Valgrind header files, which exposes the Valgrind API to MySQL code. The default is OFF.

To generate a Valgrind-aware debug build, [-DWITH\\_VALGRIND=1](#page-28-8) normally is combined with [-](#page-24-0) [DWITH\\_DEBUG=1](#page-24-0). See [Building Debug Configurations](https://dev.mysql.com/doc/internals/en/debug-configurations.md).

<span id="page-28-9"></span>• [-DWITH\\_ZLIB=](#page-28-9)zlib\_type

Some features require that the server be built with compression library support, such as the COMPRESS() and UNCOMPRESS() functions, and compression of the client/server protocol. The [WITH\\_ZLIB](#page-28-9) option indicates the source of zlib support:

- bundled: Use the zlib library bundled with the distribution. This is the default.
- system: Use the system zlib library.
- <span id="page-28-4"></span>• [-DWITHOUT\\_SERVER=](#page-28-4)bool

Whether to build without MySQL Server. The default is OFF, which does build the server.

This is considered an experimental option; it is preferred to build with the server.

### <span id="page-28-2"></span><span id="page-28-0"></span>**Compiler Flags**

• [-DCMAKE\\_C\\_FLAGS="](#page-28-2)flags"

Flags for the C compiler.

<span id="page-28-1"></span>• [-DCMAKE\\_CXX\\_FLAGS="](#page-28-1)flags"

Flags for the C++ compiler.

<span id="page-28-5"></span>• [-DWITH\\_DEFAULT\\_COMPILER\\_OPTIONS=](#page-28-5)bool

Whether to use the flags from cmake/build\_configurations/compiler\_options.cmake.

![](_page_28_Picture_22.jpeg)

#### **Note**

All optimization flags are carefully chosen and tested by the MySQL build team. Overriding them can lead to unexpected results and is done at your own risk.

<span id="page-28-3"></span>• [-DSUNPRO\\_CXX\\_LIBRARY="](#page-28-3)lib\_name"

Enable linking against libCstd instead of stlport4 on Solaris 10 or later. This works only for client code because the server depends on C++98.

To specify your own C and C++ compiler flags, for flags that do not affect optimization, use the [CMAKE\\_C\\_FLAGS](#page-28-2) and [CMAKE\\_CXX\\_FLAGS](#page-28-1) CMake options.

When providing your own compiler flags, you might want to specify [CMAKE\\_BUILD\\_TYPE](#page-14-2) as well.

For example, to create a 32-bit release build on a 64-bit Linux machine, do this:

```
$> mkdir build
$> cd build
$> cmake .. -DCMAKE_C_FLAGS=-m32 \
 -DCMAKE_CXX_FLAGS=-m32 \
 -DCMAKE_BUILD_TYPE=RelWithDebInfo
```

If you set flags that affect optimization (-Onumber), you must set the CMAKE\_C\_FLAGS\_build\_type and/or CMAKE\_CXX\_FLAGS\_build\_type options, where build\_type corresponds to the [CMAKE\\_BUILD\\_TYPE](#page-14-2) value. To specify a different optimization for the default build type (RelWithDebInfo) set the CMAKE\_C\_FLAGS\_RELWITHDEBINFO and CMAKE\_CXX\_FLAGS\_RELWITHDEBINFO options. For example, to compile on Linux with -O3 and with debug symbols, do this:

```
$> cmake .. -DCMAKE_C_FLAGS_RELWITHDEBINFO="-O3 -g" \
 -DCMAKE_CXX_FLAGS_RELWITHDEBINFO="-O3 -g"
```

## <span id="page-29-0"></span>**CMake Options for Compiling NDB Cluster**

The following options are for use when building NDB Cluster with the NDB Cluster sources; they are not currently supported when using sources from the MySQL 5.7 Server tree.

<span id="page-29-7"></span>• [-DMEMCACHED\\_HOME=](#page-29-7)dir\_name

NDB support for memcached was removed in NDB 7.5.21 and NDB 7.6.17; thus, this option is no longer supported for building NDB in these or later versions.

<span id="page-29-8"></span>• [-DWITH\\_BUNDLED\\_LIBEVENT={ON|OFF}](#page-29-8)

NDB support for memcached was removed in NDB 7.5.21 and NDB 7.6.17, and thus this option is no longer supported for building NDB in these or later versions.

<span id="page-29-9"></span>• [-DWITH\\_BUNDLED\\_MEMCACHED={ON|OFF}](#page-29-9)

NDB support for memcached was removed in NDB 7.5.21 and NDB 7.6.17, and thus this option is no longer supported for building NDB in these or later versions.

<span id="page-29-1"></span>• [-DWITH\\_CLASSPATH=](#page-29-1)path

Sets the classpath for building MySQL NDB Cluster Connector for Java. The default is empty. This option is ignored if [-DWITH\\_NDB\\_JAVA=OFF](#page-30-3) is used.

<span id="page-29-2"></span>• [-DWITH\\_ERROR\\_INSERT={ON|OFF}](#page-29-2)

Enables error injection in the NDB kernel. For testing only; not intended for use in building production binaries. The default is OFF.

<span id="page-29-3"></span>• [-DWITH\\_NDBAPI\\_EXAMPLES={ON|OFF}](#page-29-3)

Build NDB API example programs in storage/ndb/ndbapi-examples/. See [NDB API](https://dev.mysql.com/doc/ndbapi/en/ndb-examples.md) [Examples,](https://dev.mysql.com/doc/ndbapi/en/ndb-examples.md) for information about these.

<span id="page-29-5"></span>• [-DWITH\\_NDBCLUSTER\\_STORAGE\\_ENGINE={ON|OFF}](#page-29-5)

For internal use only; may not always work as expected. To build with NDB support, use [WITH\\_NDBCLUSTER](#page-29-4) instead.

<span id="page-29-4"></span>• [-DWITH\\_NDBCLUSTER={ON|OFF}](#page-29-4)

Build and link in support for the NDB storage engine in [mysqld](#page-144-0). The default is ON.

<span id="page-29-6"></span>• [-DWITH\\_NDBMTD={ON|OFF}](#page-29-6)

Build the multithreaded data node executable ndbmtd. The default is ON.

<span id="page-30-1"></span>• [-DWITH\\_NDB\\_BINLOG={ON|OFF}](#page-30-1)

Enable binary logging by default in the [mysqld](#page-144-0) built using this option. ON by default.

<span id="page-30-2"></span>• [-DWITH\\_NDB\\_DEBUG={ON|OFF}](#page-30-2)

Enable building the debug versions of the NDB Cluster binaries. This is OFF by default.

<span id="page-30-3"></span>• [-DWITH\\_NDB\\_JAVA={ON|OFF}](#page-30-3)

Enable building NDB Cluster with Java support, including support for ClusterJ (see [MySQL NDB](https://dev.mysql.com/doc/ndbapi/en/mccj.md) [Cluster Connector for Java\)](https://dev.mysql.com/doc/ndbapi/en/mccj.md).

This option is ON by default. If you do not wish to compile NDB Cluster with Java support, you must disable it explicitly by specifying -DWITH\_NDB\_JAVA=OFF when running CMake. Otherwise, if Java cannot be found, configuration of the build fails.

<span id="page-30-4"></span>• [-DWITH\\_NDB\\_PORT=](#page-30-4)port

Causes the NDB Cluster management server (ndb\_mgmd) that is built to use this port by default. If this option is unset, the resulting management server tries to use port 1186 by default.

• [-DWITH\\_NDB\\_TEST={ON|OFF}](#page-30-5)

If enabled, include a set of NDB API test programs. The default is OFF.

## <span id="page-30-5"></span><span id="page-30-0"></span>**2.8.8 Dealing with Problems Compiling MySQL**

The solution to many problems involves reconfiguring. If you do reconfigure, take note of the following:

- If CMake is run after it has previously been run, it may use information that was gathered during its previous invocation. This information is stored in CMakeCache.txt. When CMake starts, it looks for that file and reads its contents if it exists, on the assumption that the information is still correct. That assumption is invalid when you reconfigure.
- Each time you run CMake, you must run make again to recompile. However, you may want to remove old object files from previous builds first because they were compiled using different configuration options.

To prevent old object files or configuration information from being used, run the following commands before re-running CMake:

On Unix:

```
$> make clean
$> rm CMakeCache.txt
```

On Windows:

```
$> devenv MySQL.sln /clean
$> del CMakeCache.txt
```

If you build outside of the source tree, remove and recreate your build directory before re-running CMake. For instructions on building outside of the source tree, see [How to Build MySQL Server with](https://dev.mysql.com/doc/internals/en/cmake.md) [CMake.](https://dev.mysql.com/doc/internals/en/cmake.md)

On some systems, warnings may occur due to differences in system include files. The following list describes other problems that have been found to occur most often when compiling MySQL:

• To define which C and C++ compilers to use, you can define the CC and CXX environment variables. For example:

```
$> CC=gcc
```

```
$> CXX=g++
$> export CC CXX
```

While this can be done on the command line, as just shown, you may prefer to define these values in a build script, in which case the export command is not needed.

To specify your own C and C++ compiler flags, use the [CMAKE\\_C\\_FLAGS](#page-28-2) and [CMAKE\\_CXX\\_FLAGS](#page-28-1) CMake options. See [Compiler Flags](#page-28-0).

To see what flags you might need to specify, invoke mysql\_config with the --cflags and - cxxflags options.

- To see what commands are executed during the compile stage, after using CMake to configure MySQL, run make VERBOSE=1 rather than just make.
- If compilation fails, check whether the [MYSQL\\_MAINTAINER\\_MODE](#page-21-7) option is enabled. This mode causes compiler warnings to become errors, so disabling it may enable compilation to proceed.
- If your compile fails with errors such as any of the following, you must upgrade your version of make to GNU make:

```
make: Fatal error in reader: Makefile, line 18:
Badly formed macro assignment
Or:
make: file `Makefile' line 18: Must be a separator (:
Or:
pthread.h: No such file or directory
```

Solaris and FreeBSD are known to have troublesome make programs.

GNU make 3.75 is known to work.

• The sql\_yacc.cc file is generated from sql\_yacc.yy. Normally, the build process does not need to create sql\_yacc.cc because MySQL comes with a pregenerated copy. However, if you do need to re-create it, you might encounter this error:

```
"sql_yacc.yy", line xxx fatal: default action causes potential...
```

This is a sign that your version of yacc is deficient. You probably need to install a recent version of bison (the GNU version of yacc) and use that instead.

Versions of bison older than 1.75 may report this error:

```
sql_yacc.yy:#####: fatal error: maximum table size (32767) exceeded
```

The maximum table size is not actually exceeded; the error is caused by bugs in older versions of bison.

For information about acquiring or updating tools, see the system requirements in [Section 2.8,](#page-0-1) ["Installing MySQL from Source"](#page-0-1).