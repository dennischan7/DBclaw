# Oracle 12c - ap_standard_sql013
Source: https://docs.oracle.com/database/121/SQLRF/ap_standard_sql013.htm

[Go to main content](#BEGIN)

542/555 

# Oracle Extensions to Standard SQL

Oracle supports numerous features that extend beyond standard SQL. If you are concerned with the portability of your applications to other implementations of SQL, then use Oracle's FIPS Flagger to help identify the use of Oracle extensions to Entry SQL-92 in your embedded SQL programs. The FIPS Flagger is part of the Oracle precompilers and the SQL\*Module compiler. The FIPS Flagger can also be enabled in SQL\*Plus by using `ALTER` `SESSION` `SET` `FLAGGER` `=` `ENTRY`. While SQL-92 has been superseded by SQL:2011, there has been no conformance testing authority for any version of SQL since SQL-92; hence, Entry SQL-92 offers you the most assurance of portability.

Scripting on this page enhances content navigation, but does not change the content in any way.