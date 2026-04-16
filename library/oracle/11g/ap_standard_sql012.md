# Oracle 11g - ap_standard_sql012
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/ap_standard_sql012.htm

[Go to main content](#BEGIN)

509/522 

# Oracle Extensions to Standard SQL

Oracle supports numerous features that extend beyond standard SQL. If you are concerned with the portability of your applications to other implementations of SQL, then use Oracle's FIPS Flagger to help identify the use of Oracle extensions to Entry SQL-92 in your embedded SQL programs. The FIPS Flagger is part of the Oracle precompilers and the SQL\*Module compiler. The FIPS Flagger can also be enabled in SQL\*Plus by using `ALTER` `SESSION` `SET` `FLAGGER` `=` `ENTRY`. While SQL-92 has been superseded by SQL:2008, there has been no conformance testing authority for any version of SQL since SQL-92; hence, Entry SQL-92 offers you the most assurance of portability.

Scripting on this page enhances content navigation, but does not change the content in any way.