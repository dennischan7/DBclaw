# Oracle 23c - Tools-Support
Source: https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/Tools-Support.html

Oracle provides a number of utilities to facilitate your SQL development process:

* Oracle SQL Developer is a graphical tool that lets you browse, create, edit, and delete (drop) database objects, edit and debug PL/SQL code, run SQL statements and scripts, manipulate and export data, and create and view reports.

  Use SQL Developer to connect to a database schema using standard database authentication. DBAs can also use SQL Developer to administer and monitor their database, with interfaces for Data Pump, RMAN, and Auditing also included.

  Once connected, you can perform operations on objects in the database. You can also connect to schemas for selected databases, such as MySQL, Microsoft SQL Server, and Amazon Redshift, view metadata and data in these databases, and migrate these databases to an Oracle database.
* Oracle SQL Developer Command Line (SQLcl) is a free command line interface for the database. It allows you to interactively or batch execute SQL and PL/SQL.

  SQLcl offers integrated Oracle Cloud (OCI) support, client side scripting with JavaScript, custom commands, and updated SQL\*Plus commands (INFO vs DESC). Additionally, SQLcl provides native vi or Emacs editing, statement completion, and persistent command recall for a feature-rich experience, all while supporting your previously written SQL\*Plus scripts.
* Database Actions delivers the database desktop toolâs features and experience to your web browser. Delivered as a single-page web application, Database Actions is powered by Oracle REST Data Services (ORDS).

  Database Actions offers a worksheet for running queries and scripts, the ability to manage and browse your data dictionary, a REST development environment for your REST APIs and AUTOREST enabled objects, an interface for Oracleâs JSON Document Store (SODA), a DBA console for managing the database, a data model reporting solution, and access to PerfHub. Database Actions is also available automatically for any Oracle Autonomous Database OCI Service.
* SQL\*Plus is an interactive and batch query tool that is installed with every database server or client installation. It has a command-line user interface.

The Oracle Call Interface and Oracle precompilers let you embed standard SQL statements within a procedure programming language.

Most (but not all) Oracle tools also support all features of Oracle SQL. This reference describes the complete functionality of SQL. If the Oracle tool that you are using does not support this complete functionality, then you can find a discussion of the restrictions in the manual describing the tool, such as [SQL\*Plus User's Guide and
Reference](/pls/topic/lookup?ctx=en/database/oracle/oracle-database/26/sqlrf&id=SQPUG).