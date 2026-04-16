---
source: Apache Hive Official Wiki
title: Home page
url: https://cwiki.apache.org/confluence/display/Hive/LanguageManual
---

# Home page

# Apache Hive

The **[Apache Hive™](http://hive.apache.org "http://hive.apache.org")** data warehouse software facilitates reading, writing, and managing large datasets residing in distributed storage and queried using SQL syntax.

* Tools to enable easy access to data via SQL, thus enabling data warehousing tasks such as extract/transform/load (ETL), reporting, and data analysis.
* A mechanism to impose structure on a variety of data formats
* Access to files stored either directly in **[Apache HDFS](http://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-hdfs/HdfsUserGuide.html "http://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-hdfs/HdfsUserGuide.html")**[™](http://hadoop.apache.org/ "http://hadoop.apache.org/")**** or in other data storage systems such as **[Apache HBase](http://hbase.apache.org "http://hbase.apache.org")**[™](http://hadoop.apache.org/ "http://hadoop.apache.org/")****
* Query execution via [Apache Tez](http://tez.apache.org/ "http://tez.apache.org/")**[™](http://hadoop.apache.org/ "http://hadoop.apache.org/")**, [Apache Spark](http://spark.apache.org/ "http://spark.apache.org/")**[™](http://hadoop.apache.org/ "http://hadoop.apache.org/")**, or [MapReduce](http://hadoop.apache.org/docs/current/hadoop-mapreduce-client/hadoop-mapreduce-client-core/MapReduceTutorial.html "http://hadoop.apache.org/docs/current/hadoop-mapreduce-client/hadoop-mapreduce-client-core/MapReduceTutorial.html")
* Procedural language with HPL-SQL
* Sub-second query retrieval via [Hive LLAP](https://cwiki.apache.org/confluence/display/Hive/LLAP "/confluence/display/Hive/LLAP"), [Apache YARN](https://hadoop.apache.org/docs/r2.7.2/hadoop-yarn/hadoop-yarn-site/YARN.html "https://hadoop.apache.org/docs/r2.7.2/hadoop-yarn/hadoop-yarn-site/YARN.html") and [Apache Slider](https://slider.incubator.apache.org/ "https://slider.incubator.apache.org/").

[Hive provides standard SQL functionality](https://cwiki.apache.org/confluence/display/Hive/Apache+Hive+SQL+Conformance "/confluence/display/Hive/Apache+Hive+SQL+Conformance"), including many of the later [SQL:2003](https://en.wikipedia.org/wiki/SQL:2003 "https://en.wikipedia.org/wiki/SQL:2003"), [SQL:2011](https://en.wikipedia.org/wiki/SQL:2011 "https://en.wikipedia.org/wiki/SQL:2011"), and [SQL:2016](https://en.wikipedia.org/wiki/SQL:2016 "https://en.wikipedia.org/wiki/SQL:2016") features for analytics.   
Hive's SQL can also be extended with user code via user defined functions (UDFs), user defined aggregates (UDAFs), and user defined table functions (UDTFs).

There is not a single "Hive format" in which data must be stored. Hive comes with built in connectors for comma and tab-separated values (CSV/TSV) text files, [Apache Parquet](http://parquet.apache.org/ "http://parquet.apache.org/")****[™](http://hadoop.apache.org/ "http://hadoop.apache.org/")****, [Apache ORC](http://orc.apache.org/ "http://orc.apache.org/")****[™](http://hadoop.apache.org/ "http://hadoop.apache.org/")****, and other formats. Users can extend Hive with connectors for other formats. Please see [File Formats](https://cwiki.apache.org/confluence/display/Hive/DeveloperGuide#DeveloperGuide-FileFormats "/confluence/display/Hive/DeveloperGuide#DeveloperGuide-FileFormats") and [Hive SerDe](https://cwiki.apache.org/confluence/display/Hive/DeveloperGuide#DeveloperGuide-HiveSerDe "/confluence/display/Hive/DeveloperGuide#DeveloperGuide-HiveSerDe") in the [Developer Guide](https://cwiki.apache.org/confluence/display/Hive/DeveloperGuide "/confluence/display/Hive/DeveloperGuide") for details.

Hive is not designed for online transaction processing (OLTP) workloads. It is best used for traditional data warehousing tasks.

Hive is designed to maximize scalability (scale out with more machines added dynamically to the Hadoop cluster), performance, extensibility, fault-tolerance, and loose-coupling with its input formats.

Components of Hive include HCatalog and WebHCat.

* **[HCatalog](https://cwiki.apache.org/confluence/display/Hive/HCatalog "/confluence/display/Hive/HCatalog")** is a table and storage management layer for Hadoop that enables users with different data processing tools — including Pig and MapReduce — to more easily read and write data on the grid.
* **[WebHCat](https://cwiki.apache.org/confluence/display/Hive/WebHCat "/confluence/display/Hive/WebHCat")** provides a service that you can use to run Hadoop MapReduce (or YARN), Pig, Hive jobs. You can also perform Hive metadata operations using an HTTP (REST style) interface.

# Hive Documentation

The links below provide access to the Apache Hive wiki documents. This list is not complete, but you can navigate through these wiki pages to find additional documents. For more information, please see the official [Hive website](http://hive.apache.org "http://hive.apache.org").

## General Information about Hive

* [Getting Started](https://cwiki.apache.org/confluence/display/Hive/GettingStarted "/confluence/display/Hive/GettingStarted")
* [Books about Hive](https://cwiki.apache.org/confluence/display/Hive/Books+about+Hive "/confluence/display/Hive/Books+about+Hive")
* [Presentations and Papers about Hive](https://cwiki.apache.org/confluence/display/Hive/Presentations "/confluence/display/Hive/Presentations")
* [Sites and Applications Powered by Hive](https://cwiki.apache.org/confluence/display/Hive/PoweredBy "/confluence/display/Hive/PoweredBy")
* [Related Projects](https://cwiki.apache.org/confluence/display/Hive/RelatedProjects "/confluence/display/Hive/RelatedProjects")
* [FAQ](https://cwiki.apache.org/confluence/display/Hive/User+FAQ "/confluence/display/Hive/User+FAQ")
* [Hive Users Mailing List](http://hive.apache.org/mailing_lists.html#Users "http://hive.apache.org/mailing_lists.html#Users")
* Hive IRC Channel: `#hive` on irc.freenode.net
* [About This Wiki](https://cwiki.apache.org/confluence/display/Hive/AboutThisWiki "/confluence/display/Hive/AboutThisWiki")

## User Documentation

* [Hive Tutorial](https://cwiki.apache.org/confluence/display/Hive/Tutorial "/confluence/display/Hive/Tutorial")
* [Hive SQL Language Manual](https://cwiki.apache.org/confluence/display/Hive/LanguageManual "/confluence/display/Hive/LanguageManual"):  [Commands](https://cwiki.apache.org/confluence/display/Hive/LanguageManual+Commands "/confluence/display/Hive/LanguageManual+Commands"), [CLIs](https://cwiki.apache.org/confluence/display/Hive/LanguageManual+Cli "/confluence/display/Hive/LanguageManual+Cli"), [Data Types](https://cwiki.apache.org/confluence/display/Hive/LanguageManual+Types "/confluence/display/Hive/LanguageManual+Types"),  
  DDL ([create/drop/alter/truncate/show/describe](https://cwiki.apache.org/confluence/display/Hive/LanguageManual+DDL "/confluence/display/Hive/LanguageManual+DDL")), [Statistics (analyze)](https://cwiki.apache.org/confluence/display/Hive/StatsDev "/confluence/display/Hive/StatsDev"), [Indexes](https://cwiki.apache.org/confluence/display/Hive/LanguageManual+Indexing "/confluence/display/Hive/LanguageManual+Indexing"), [Archiving](https://cwiki.apache.org/confluence/display/Hive/LanguageManual+Archiving "/confluence/display/Hive/LanguageManual+Archiving"),  
  DML ([load/insert/update/delete/merge](https://cwiki.apache.org/confluence/display/Hive/LanguageManual+DML "/confluence/display/Hive/LanguageManual+DML"), [import/export](https://cwiki.apache.org/confluence/display/Hive/LanguageManual+ImportExport "/confluence/display/Hive/LanguageManual+ImportExport"), [explain plan](https://cwiki.apache.org/confluence/display/Hive/LanguageManual+Explain "/confluence/display/Hive/LanguageManual+Explain")),  
  [Queries (select)](https://cwiki.apache.org/confluence/display/Hive/LanguageManual+Select "/confluence/display/Hive/LanguageManual+Select"), [Operators and UDFs](https://cwiki.apache.org/confluence/display/Hive/LanguageManual+UDF "/confluence/display/Hive/LanguageManual+UDF"), [Locks](https://cwiki.apache.org/confluence/display/Hive/LanguageManual+Locks "/confluence/display/Hive/LanguageManual+Locks"), [Authorization](https://cwiki.apache.org/confluence/display/Hive/LanguageManual+Authorization "/confluence/display/Hive/LanguageManual+Authorization")
* [File Formats and Compression](https://cwiki.apache.org/confluence/display/Hive/FileFormats "/confluence/display/Hive/FileFormats"):  [RCFile](https://cwiki.apache.org/confluence/display/Hive/RCFile "/confluence/display/Hive/RCFile"), [Avro](https://cwiki.apache.org/confluence/display/Hive/AvroSerDe "/confluence/display/Hive/AvroSerDe"), [ORC](https://cwiki.apache.org/confluence/display/Hive/LanguageManual+ORC "/confluence/display/Hive/LanguageManual+ORC"), [Parquet](https://cwiki.apache.org/confluence/display/Hive/Parquet "/confluence/display/Hive/Parquet"); [Compression](https://cwiki.apache.org/confluence/display/Hive/CompressedStorage "/confluence/display/Hive/CompressedStorage"), [LZO](https://cwiki.apache.org/confluence/display/Hive/LanguageManual+LZO "/confluence/display/Hive/LanguageManual+LZO")
* Procedural Language:   [Hive HPL/SQL](https://cwiki.apache.org/confluence/pages/viewpage.action?pageId=59690156 "/confluence/pages/viewpage.action?pageId=59690156")
* [Hive Configuration Properties](https://cwiki.apache.org/confluence/display/Hive/Configuration+Properties "/confluence/display/Hive/Configuration+Properties")
* Hive Clients
  + [Hive Client](https://cwiki.apache.org/confluence/display/Hive/HiveClient "/confluence/display/Hive/HiveClient") ([JDBC](https://cwiki.apache.org/confluence/display/Hive/HiveClient#HiveClient-JDBC "/confluence/display/Hive/HiveClient#HiveClient-JDBC"), [ODBC](https://cwiki.apache.org/confluence/display/Hive/HiveClient#HiveClient-ODBC "/confluence/display/Hive/HiveClient#HiveClient-ODBC"), [Thrift](https://cwiki.apache.org/confluence/display/Hive/HiveClient#HiveClient-ThriftJavaClient "/confluence/display/Hive/HiveClient#HiveClient-ThriftJavaClient"))
  + HiveServer2:  [Overview](https://cwiki.apache.org/confluence/display/Hive/HiveServer2+Overview "/confluence/display/Hive/HiveServer2+Overview"), [HiveServer2 Client and Beeline](https://cwiki.apache.org/confluence/display/Hive/HiveServer2+Clients "/confluence/display/Hive/HiveServer2+Clients"), [Hive Metrics](https://cwiki.apache.org/confluence/display/Hive/Hive+Metrics "/confluence/display/Hive/Hive+Metrics")
* [Hive Web Interface](https://cwiki.apache.org/confluence/display/Hive/HiveWebInterface "/confluence/display/Hive/HiveWebInterface")
* [Hive SerDes](https://cwiki.apache.org/confluence/display/Hive/SerDe "/confluence/display/Hive/SerDe"):  [Avro SerDe](https://cwiki.apache.org/confluence/display/Hive/AvroSerDe "/confluence/display/Hive/AvroSerDe"), [Parquet SerDe](https://cwiki.apache.org/confluence/display/Hive/Parquet#Parquet-HiveQLSyntax "/confluence/display/Hive/Parquet#Parquet-HiveQLSyntax"), [CSV SerDe](https://cwiki.apache.org/confluence/display/Hive/CSV+Serde "/confluence/display/Hive/CSV+Serde"), [JSON SerDe](https://cwiki.apache.org/confluence/display/Hive/LanguageManual+DDL#LanguageManualDDL-JSON "/confluence/display/Hive/LanguageManual+DDL#LanguageManualDDL-JSON")
* [Hive Accumulo Integration](https://cwiki.apache.org/confluence/display/Hive/AccumuloIntegration "/confluence/display/Hive/AccumuloIntegration")
* [Hive HBase Integration](https://cwiki.apache.org/confluence/display/Hive/HBaseIntegration "/confluence/display/Hive/HBaseIntegration")
* [Druid Integration](https://cwiki.apache.org/confluence/display/Hive/Druid+Integration "/confluence/display/Hive/Druid+Integration")
* [Kudu Integration](https://cwiki.apache.org/confluence/display/Hive/Kudu+Integration "/confluence/display/Hive/Kudu+Integration")
* [Hive Transactions](https://cwiki.apache.org/confluence/display/Hive/Hive+Transactions "/confluence/display/Hive/Hive+Transactions"), [Streaming Data Ingest](https://cwiki.apache.org/confluence/display/Hive/Streaming+Data+Ingest "/confluence/display/Hive/Streaming+Data+Ingest"), and [Streaming Mutation API](https://cwiki.apache.org/confluence/display/Hive/HCatalog+Streaming+Mutation+API "/confluence/display/Hive/HCatalog+Streaming+Mutation+API")
* [Hive Counters](https://cwiki.apache.org/confluence/display/Hive/HiveCounters "/confluence/display/Hive/HiveCounters")
* [Using TiDB as the Hive Metastore database](https://cwiki.apache.org/confluence/display/Hive/Using+TiDB+as+the+Hive+Metastore+database "/confluence/display/Hive/Using+TiDB+as+the+Hive+Metastore+database")
* [StarRocks Integration](https://cwiki.apache.org/confluence/display/Hive/StarRocks+Integration "https://cwiki.apache.org/confluence/display/Hive/StarRocks+Integration")

## Administrator Documentation

* [Installing Hive](https://cwiki.apache.org/confluence/display/Hive/AdminManual+Installation "/confluence/display/Hive/AdminManual+Installation")
* [Configuring Hive](https://cwiki.apache.org/confluence/display/Hive/AdminManual+Configuration "/confluence/display/Hive/AdminManual+Configuration")
* [Setting Up Metastore](https://cwiki.apache.org/confluence/display/Hive/AdminManual+Metastore+Administration "/confluence/display/Hive/AdminManual+Metastore+Administration")
  + [Hive Schema Tool](https://cwiki.apache.org/confluence/display/Hive/Hive+Schema+Tool "/confluence/display/Hive/Hive+Schema+Tool")
* [Setting Up Hive Web Interface](https://cwiki.apache.org/confluence/display/Hive/HiveWebInterface "/confluence/display/Hive/HiveWebInterface")
* [Setting Up Hive Server](https://cwiki.apache.org/confluence/display/Hive/AdminManual+SettingUpHiveServer "/confluence/display/Hive/AdminManual+SettingUpHiveServer") ([JDBC](https://cwiki.apache.org/confluence/display/Hive/HiveJDBCInterface "/confluence/display/Hive/HiveJDBCInterface"), [ODBC](https://cwiki.apache.org/confluence/display/Hive/HiveODBC "/confluence/display/Hive/HiveODBC"), [Thrift](https://cwiki.apache.org/confluence/display/Hive/HiveServer "/confluence/display/Hive/HiveServer"), [HiveServer2](https://cwiki.apache.org/confluence/display/Hive/Setting+Up+HiveServer2 "/confluence/display/Hive/Setting+Up+HiveServer2"))
* [Hive Replication](https://cwiki.apache.org/confluence/display/Hive/Replication "/confluence/display/Hive/Replication")
* [Hive on Amazon Web Services](https://cwiki.apache.org/confluence/display/Hive/HiveAws "/confluence/display/Hive/HiveAws")
* [Hive on Amazon Elastic MapReduce](https://cwiki.apache.org/confluence/display/Hive/HiveAmazonElasticMapReduce "/confluence/display/Hive/HiveAmazonElasticMapReduce")
* [Hive on Spark: Getting Started](https://cwiki.apache.org/confluence/display/Hive/Hive+on+Spark%3A+Getting+Started "/confluence/display/Hive/Hive+on+Spark%3A+Getting+Started")

## HCatalog and WebHCat Documentation

* [HCatalog](https://cwiki.apache.org/confluence/display/Hive/HCatalog "/confluence/display/Hive/HCatalog")
* [WebHCat (Templeton)](https://cwiki.apache.org/confluence/display/Hive/WebHCat "/confluence/display/Hive/WebHCat")

## Resources for Contributors

* [How to Contribute](https://cwiki.apache.org/confluence/display/Hive/HowToContribute "/confluence/display/Hive/HowToContribute")
* [Hive Contributors Meetings](https://cwiki.apache.org/confluence/display/Hive/Development+ContributorsMeetings "/confluence/display/Hive/Development+ContributorsMeetings")
* [Hive Developer Docs](https://cwiki.apache.org/confluence/display/Hive/DeveloperDocs "/confluence/display/Hive/DeveloperDocs")
  + [Hive Developer Guide](https://cwiki.apache.org/confluence/display/Hive/DeveloperGuide "/confluence/display/Hive/DeveloperGuide") ([code organization](https://cwiki.apache.org/confluence/display/Hive/DeveloperGuide#DeveloperGuide-CodeOrganizationandaBriefArchitecture "/confluence/display/Hive/DeveloperGuide#DeveloperGuide-CodeOrganizationandaBriefArchitecture"), [compile and run Hive](https://cwiki.apache.org/confluence/display/Hive/DeveloperGuide#DeveloperGuide-CompilingandRunningHive "/confluence/display/Hive/DeveloperGuide#DeveloperGuide-CompilingandRunningHive"), [unit tests](https://cwiki.apache.org/confluence/display/Hive/DeveloperGuide#DeveloperGuide-Unittestsanddebugging "/confluence/display/Hive/DeveloperGuide#DeveloperGuide-Unittestsanddebugging"), [debug](https://cwiki.apache.org/confluence/display/Hive/DeveloperGuide#DeveloperGuide-DebuggingHiveCode "/confluence/display/Hive/DeveloperGuide#DeveloperGuide-DebuggingHiveCode"), [pluggable interfaces](https://cwiki.apache.org/confluence/display/Hive/DeveloperGuide#DeveloperGuide-Pluggableinterfaces "/confluence/display/Hive/DeveloperGuide#DeveloperGuide-Pluggableinterfaces"))
  + [Hive Developer FAQ](https://cwiki.apache.org/confluence/display/Hive/HiveDeveloperFAQ "/confluence/display/Hive/HiveDeveloperFAQ") ([move files](https://cwiki.apache.org/confluence/display/Hive/HiveDeveloperFAQ#HiveDeveloperFAQ-HowdoImovesomefiles? "/confluence/display/Hive/HiveDeveloperFAQ#HiveDeveloperFAQ-HowdoImovesomefiles?"), [build Hive](https://cwiki.apache.org/confluence/display/Hive/HiveDeveloperFAQ#HiveDeveloperFAQ-Building "/confluence/display/Hive/HiveDeveloperFAQ#HiveDeveloperFAQ-Building"), [test Hive](https://cwiki.apache.org/confluence/display/Hive/HiveDeveloperFAQ#HiveDeveloperFAQ-Testing "/confluence/display/Hive/HiveDeveloperFAQ#HiveDeveloperFAQ-Testing"), [MiniDriver and Beeline tests](https://cwiki.apache.org/confluence/display/Hive/MiniDriver+Tests "/confluence/display/Hive/MiniDriver+Tests"))
  + [Plugin Developer Kit](https://cwiki.apache.org/confluence/display/Hive/PluginDeveloperKit "/confluence/display/Hive/PluginDeveloperKit")
  + [Writing UDTFs](https://cwiki.apache.org/confluence/display/Hive/DeveloperGuide+UDTF "/confluence/display/Hive/DeveloperGuide+UDTF")
  + [Hive APIs Overview](https://cwiki.apache.org/confluence/display/Hive/Hive+APIs+Overview "/confluence/display/Hive/Hive+APIs+Overview")
* [Hive Testing Docs](https://cwiki.apache.org/confluence/display/Hive/TestingDocs "/confluence/display/Hive/TestingDocs")
  + [FAQ: Testing](https://cwiki.apache.org/confluence/display/Hive/HiveDeveloperFAQ#HiveDeveloperFAQ-Testing "/confluence/display/Hive/HiveDeveloperFAQ#HiveDeveloperFAQ-Testing")
  + [Developer Guide: Unit Tests](https://cwiki.apache.org/confluence/display/Hive/DeveloperGuide#DeveloperGuide-Unittestsanddebugging "/confluence/display/Hive/DeveloperGuide#DeveloperGuide-Unittestsanddebugging")
  + [Unit Testing Hive SQL](https://cwiki.apache.org/confluence/display/Hive/Unit+Testing+Hive+SQL "/confluence/display/Hive/Unit+Testing+Hive+SQL")
  + [Unit Test Parallel Execution](https://cwiki.apache.org/confluence/display/Hive/Unit+Test+Parallel+Execution "/confluence/display/Hive/Unit+Test+Parallel+Execution")
  + [Tips for Adding New Tests](https://cwiki.apache.org/confluence/display/Hive/TipsForAddingNewTests "/confluence/display/Hive/TipsForAddingNewTests")
  + [Hive PTest2 Infrastructure](https://cwiki.apache.org/confluence/display/Hive/Hive+PTest2+Infrastructure "/confluence/display/Hive/Hive+PTest2+Infrastructure")
  + [Hive PreCommit Patch Testing](https://cwiki.apache.org/confluence/display/Hive/Hive+PreCommit+Patch+Testing "/confluence/display/Hive/Hive+PreCommit+Patch+Testing")
  + [MiniDriver Tests](https://cwiki.apache.org/confluence/display/Hive/MiniDriver+Tests "/confluence/display/Hive/MiniDriver+Tests")
  + [Running Yetus](https://cwiki.apache.org/confluence/display/Hive/Running+Yetus "/confluence/display/Hive/Running+Yetus")
  + [MetaStore API Tests](https://cwiki.apache.org/confluence/display/Hive/MetaStore+API+Tests "/confluence/display/Hive/MetaStore+API+Tests")
* [Hive Performance](https://cwiki.apache.org/confluence/display/Hive/Performance "/confluence/display/Hive/Performance")
* [Hive Architecture Overview](https://cwiki.apache.org/confluence/display/Hive/Design "/confluence/display/Hive/Design")
* [Hive Design Docs](https://cwiki.apache.org/confluence/display/Hive/DesignDocs "/confluence/display/Hive/DesignDocs"):  [Completed](https://cwiki.apache.org/confluence/display/Hive/DesignDocs#DesignDocs-Completed "/confluence/display/Hive/DesignDocs#DesignDocs-Completed"); [In Progress](https://cwiki.apache.org/confluence/display/Hive/DesignDocs#DesignDocs-InProgress "/confluence/display/Hive/DesignDocs#DesignDocs-InProgress"); [Proposed](https://cwiki.apache.org/confluence/display/Hive/DesignDocs#DesignDocs-Proposed "/confluence/display/Hive/DesignDocs#DesignDocs-Proposed"); [Incomplete, Abandoned, Other](https://cwiki.apache.org/confluence/display/Hive/DesignDocs#DesignDocs-Incomplete "/confluence/display/Hive/DesignDocs#DesignDocs-Incomplete")
* [Roadmap/Call to Add More Features](https://cwiki.apache.org/confluence/display/Hive/Roadmap "/confluence/display/Hive/Roadmap")
* [Full-Text Search over All Hive Resources](http://search-hadoop.com/Hive "http://search-hadoop.com/Hive")
* [How to edit the website](https://cwiki.apache.org/confluence/display/Hive/How+to+edit+the+website "/confluence/display/Hive/How+to+edit+the+website")
* [Becoming a Committer](https://cwiki.apache.org/confluence/display/Hive/BecomingACommitter "/confluence/display/Hive/BecomingACommitter")
* [How to Commit](https://cwiki.apache.org/confluence/display/Hive/HowToCommit "/confluence/display/Hive/HowToCommit")
* [How to Release](https://cwiki.apache.org/confluence/display/Hive/HowToRelease "/confluence/display/Hive/HowToRelease")
* [Project Bylaws](https://cwiki.apache.org/confluence/display/Hive/Bylaws "/confluence/display/Hive/Bylaws")

# Hive Versions and Branches

Recent versions of Hive are available on the [Downloads](http://hive.apache.org/downloads.html "http://hive.apache.org/downloads.html") page of the Hive website. For each version, the page provides the release date and a link to the change log. If you want a change log for an earlier version (or a development branch), use the [Configure Release Notes](https://issues.apache.org/jira/secure/ConfigureReleaseNote.jspa?projectId=12310843&version=12329278 "https://issues.apache.org/jira/secure/ConfigureReleaseNote.jspa?projectId=12310843&version=12329278") page.

The [Apache Hive JIRA](https://issues.apache.org/jira/browse/HIVE "https://issues.apache.org/jira/browse/HIVE") keeps track of changes to Hive code, documentation, infrastructure, etc. The version number or branch for each resolved JIRA issue is shown in the "Fix Version/s" field in the Details section at the top of the issue page. For example, [HIVE-5107](https://issues.apache.org/jira/browse/HIVE-5107 "https://issues.apache.org/jira/browse/HIVE-5107") has a fix version of 0.13.0.

Sometimes a version number changes before the release. When that happens, the original number might still be found in JIRA, wiki, and [mailing list](http://hive.apache.org/mailing_lists.html "http://hive.apache.org/mailing_lists.html") discussions. For example:

| Release Number | Original Number |
| --- | --- |
| 1.0.0 | 0.14.1 |
| 1.1.0 | 0.15.0 |
| 2.3.0 | 2.2.0 |

More information about Hive branches is available in How to Contribute: [Understanding Hive Branches](https://cwiki.apache.org/confluence/display/Hive/HowToContribute#HowToContribute-UnderstandingHiveBranches "/confluence/display/Hive/HowToContribute#HowToContribute-UnderstandingHiveBranches").

*Apache Hive, Apache Hadoop, Apache HBase, Apache HDFS, Apache, the Apache feather logo, and the Apache Hive project logo are trademarks of The Apache Software Foundation.*