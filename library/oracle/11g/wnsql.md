# Oracle 11g - wnsql
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/wnsql.htm

A number of SQL statements are constructed almost entirely of PL/SQL elements. Those statements continue to appear in this reference, but the bulk of their syntax and semantics has been moved to [Oracle Database PL/SQL Language Reference](../../appdev.112/e25519/toc.md). The following table contains links to both the abbreviated SQL syntax and semantics in this book and to the full syntax and semantics in Oracle Database PL/SQL Language Reference.

* [ALTER DATABASE](statements_1004.md#i2079942) has been enhanced as follows:

  + The clause [managed\_standby\_recovery](statements_1004.md#i2079973) has been greatly simplified. A number of subclauses have been deprecated as the database now handles much of the recovery process automatically.
  + The [supplemental\_db\_logging](statements_1004.md#i2153841) contains new syntax that lets you enable or disable supplemental logging of PL/SQL calls.
  + The [standby\_database\_clauses](statements_1004.md#i2091833) have new syntax that lets you convert a physical standby database into a snapshot standby database or convert a snapshot standby database into a physical standby database.
  + The clause [managed\_standby\_recovery](statements_1004.md#i2079973) has new `KEEP` `IDENTITY` syntax that lets you use the rolling upgrade feature provided by a logical standby and also revert to the original configuration of a primary database and a physical standby.
* [ALTER DISKGROUP](statements_1007.md#i2166968) has been enhanced as follows:
* [ALTER INDEX](statements_1010.md#i2050158) has been enhanced as follows:

  + A new `MIGRATE` parameter lets you migrate a domain index from user-managed storage tables to system-managed storage tables.
  + A new `INVISIBLE` parameter lets you modify an index so that it is invisible to the optimizer.
  + The ["PARAMETERS Clause"](statements_1010.md#BABHAICB) now lets you rebuild an XMLIndex index as well as a domain index.
* [ALTER SYSTEM](statements_2014.md#i2053602) has been enhanced as follows:

  + New syntax lets you kill a session on another instance in an Oracle Real Application Clusters (Oracle RAC) environment.
  + New [rolling\_migration\_clauses](statements_2014.md#BABFJGFH) let you prepare an Oracle ASM cluster for migration and return it to normal operation after all nodes have migrated to the same software version.
* [ALTER TABLE](statements_3001.md#CJAHHIBI) has been enhanced as follows:

  + The behavior of the [add\_column\_clause](statements_3001.md#i2198241) when you specify a `DEFAULT` value has been enhanced for improved performance.
  + The syntax for [READ ONLY | READ WRITE](statements_3001.md#BABJBAGA) lets you put a table into read-only mode, to prevent DDL or DML changes during table maintenance, and then back into read/write mode.
  + The clause [add\_table\_partition](statements_3001.md#BABFDEBD) has expanded syntax to let you add a system partition.
  + The [flashback\_archive\_clause](statements_3001.md#BABHJDBJ) lets you enable or disable historical tracking for the table.
  + The [add\_column\_clause](statements_3001.md#i2198241) now lets you add a virtual column to a table.
  + A new clause [alter\_interval\_partitioning](statements_3001.md#BABIAAFH) lets you convert a range-partitioned table to an interval\_partitioned table.
  + A new [dependent\_tables\_clause](statements_3001.md#BABDDGBB) lets you instruct the database to cascade various partition maintenance operations on a table to reference-partitioned child tables.
* [ALTER TABLESPACE](statements_3002.md#i2093894) has new syntax that lets you shrink the space taken by a temporary tablespace or an individual temp file.
* [ASSOCIATE STATISTICS](statements_4006.md#i2058947) has syntax that lets you specify that the database should manage storage of statistics collected on a system-managed domain index.
* [AUDIT](statements_4007.md#i2059073) has new syntax that lets you audit various activities on data mining models.
* [CALL](statements_4008.md#BABDEHHG) now permits positional, named, and mixed notation in the argument to the routine being called, if the routine takes any arguments.
* [COMMENT](statements_4009.md#i2119719) has a new `MINING` `MODEL` clause lets you provide descriptive comments for a data mining model.
* [CREATE DISKGROUP](statements_5008.md#i2153287) and [ALTER DISKGROUP](statements_1007.md#i2166968) have new syntax that lets you set various attributes of a disk group.
* The new statements [CREATE FLASHBACK ARCHIVE](statements_5010.md#BABIAECC), [ALTER FLASHBACK ARCHIVE](statements_1008.md#BABGBHGE), and [DROP FLASHBACK ARCHIVE](statements_8015.md#BABJAGIE) let you create, modify, and drop flashback data archives, which in turn let you track historical changes to tables.
* [CREATE INDEX](statements_5012.md#i2062403) has been enhanced as follows:
* [CREATE INDEXTYPE](statements_5013.md#g2282361) and [ALTER INDEXTYPE](statements_1011.md#i2070601) let you specify that domain indexes built on the subject indextypes can be range partitioned, and will have their storage tables and partition maintenance operations managed by the database.
* [CREATE PFILE](statements_6008.md#i2072768) has new syntax that lets you create a parameter file from current system-wide parameter settings.
* [CREATE RESTORE POINT](statements_6011.md#BABGAFFE) has new syntax that lets you create a restore point for a specified datetime or SCN in the past, and to preserve a flashback database.
* [CREATE SPFILE](statements_6016.md#i2072626) has new syntax that lets you create a system parameter file from current system-wide parameter settings.
* [CREATE TABLE](statements_7002.md#i2095331) has been enhanced as follows:

  + The [flashback\_archive\_clause](statements_7002.md#BABGIIIA) lets you create the table with tracking of historical changes enabled
  + The clause [system\_partitioning](statements_7002.md#BABJBDCC) lets you partition the table `BY` `SYSTEM`
  + A new [virtual\_column\_definition](statements_7002.md#BABIJABG) lets you create a virtual column.
  + New syntax for XML storage lets you store XML data in binary XML format.
  + A new clause [reference\_partitioning](statements_7002.md#BABFBFBC) lets you partition a table by reference to another partitioned table.
  + The [LOB\_parameters](statements_7002.md#BABFFFBE) now include a `SECUREFILE` parameter, which lets you specify a new storage for LOBs that is faster, more efficient, and allows for new features such as LOB compression, encryption, and deduplication.
  + A new [LOB\_compression\_clause](statements_7002.md#BABIJJHI) lets you enable or disable server-side LOB compression for LOBs using SecureFiles storage.
  + A new [LOB\_deduplicate\_clause](statements_7002.md#BABHHFDA) lets you coalesce duplicate data into a single shared repository, reducing storage consumption and simplifying storage management for LOBs using SecureFiles storage.
  + The [LOB\_parameters](statements_7002.md#BABFFFBE) now include `ENCRYPT` and `DECRYPT` clauses to enable and disable encryption of LOB columns for LOBs using SecureFiles storage.
* [CREATE TABLESPACE](statements_7003.md#i2231734) has new syntax which, along with a new `ENCRYPT` keyword in the [storage\_clause](clauses009.md#i997450), lets you encrypt an entire tablespace.
* [DROP DISKGROUP](statements_8013.md#i2152629) has a new `FORCE` keyword that lets you drop a disk group that can no longer be mounted by an Oracle ASM instance.
* [GRANT](statements_9013.md#i2155015) contains several new system and object privileges that enable the grantee to work with data mining models.
* [LOCK TABLE](statements_9015.md#i2064405) has new syntax that lets you specify the maximum number of seconds the statement should wait to obtain a DML lock on the table.
* [MERGE](statements_9016.md#i2081218) now supports operations on tables with domain indexes.
* [SELECT](statements_10002.md#i2065646) has new `PIVOT` syntax that lets you rotate rows into columns. A new `UNPIVOT` operation lets you query data to rotate columns into rows.

* [CUBE\_TABLE](functions042.md#CIHIHGCH) is a new built-in function that extracts data from a cube or dimension and returns it in the two-dimensional format of a relational table.
* [INSERTXMLAFTER](functions078.md#CIHIGCDA) let you add one or more nodes of any kind immediately after a target node that is not an attribute node.
* [REGEXP\_INSTR](functions148.md#i1239887) and [REGEXP\_SUBSTR](functions150.md#i1239858) now have an optional `subexpr` parameter that lets you target a particular substring of the regular expression being evaluated.
* [REGEXP\_COUNT](functions147.md#CIHDAIHJ) is a new built-in function that counts the number of occurrences of a specified regular expression pattern in a source string.
* [PREDICTION](functions132.md#CJAFCHEG), [PREDICTION\_COST](functions134.md#CJABAJED), and [PREDICTION\_SET](functions137.md#CJAJGHAI) have been enhanced. New syntax let you specify that the stored cost matrix should be used only if it is available, or to specify a cost matrix inline.
* [PREDICTION\_BOUNDS](functions133.md#CIHDDGEE) is a new function that returns the lower and upper confidence bounds for a prediction.
* [XMLCAST](functions236.md#CIHHHACJ) and [XMLEXISTS](functions243.md#CIHDEFCD) are two new functions that let you cast XML data to SQL scalar data types and determine whether an XQuery expression returns a nonempty XQuery sequence, respectively.
* [XMLDIFF](functions241.md#CIHFDJAA) and [XMLPATCH](functions247.md#CIHDAEEC) are two new functions that provide SQL interfaces to the corresponding XMLDiff and XMLPatch C APIs. They let you compare two XMLType documents and use the diff file to patch an XMLType document.