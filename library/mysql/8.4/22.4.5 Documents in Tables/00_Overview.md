---
source: MySQL 8.4 Reference
title: 00_Overview
---

In MySQL, a table may contain traditional relational data, JSON values, or both. You can combine traditional data with JSON documents by storing the documents in columns having a native JSON data type.

Examples in this section use the city table in the world\_x schema.

# **city Table Description**

The city table has five columns (or fields).

| Field                                                 | Type                                                       | Null   Key                          |                        | Default   Extra               | +++++++<br>                                                                         |
|-------------------------------------------------------|------------------------------------------------------------|-------------------------------------|------------------------|-------------------------------|-------------------------------------------------------------------------------------|
| ID<br>  Name<br>  CountryCode<br>  District<br>  Info | int(11)<br>  char(35)<br>  char(3)<br>  char(20)<br>  json | NO<br>  NO<br>  NO<br>  NO<br>  YES | PRI<br> <br> <br> <br> | null<br> <br> <br> <br>  null | +++++++<br>  auto_increment<br> <br> <br> <br> <br> <br> <br> <br> <br> <br>+++++++ |

# **Insert a Record**

To insert a document into the column of a table, pass to the values() method a well-formed JSON document in the correct order. In the following example, a document is passed as the final value to be inserted into the Info column.

```
mysql-py> db.city.insert().values(
None, "San Francisco", "USA", "California", '{"Population":830000}')
```

# **Select a Record**

You can issue a query with a search condition that evaluates document values in the expression.

```
mysql-py> db.city.select(["ID", "Name", "CountryCode", "District", "Info"]).where(
"CountryCode = :country and Info->'$.Population' > 1000000").bind(
'country', 'USA')
+------+----------------+-------------+----------------+-----------------------------+
| ID | Name | CountryCode | District | Info |
+------+----------------+-------------+----------------+-----------------------------+
| 3793 | New York | USA | New York | {"Population": 8008278} |
| 3794 | Los Angeles | USA | California | {"Population": 3694820} |
| 3795 | Chicago | USA | Illinois | {"Population": 2896016} |
| 3796 | Houston | USA | Texas | {"Population": 1953631} |
| 3797 | Philadelphia | USA | Pennsylvania | {"Population": 1517550} |
| 3798 | Phoenix | USA | Arizona | {"Population": 1321045} |
| 3799 | San Diego | USA | California | {"Population": 1223400} |
| 3800 | Dallas | USA | Texas | {"Population": 1188580} |
| 3801 | San Antonio | USA | Texas | {"Population": 1144646} |
+------+----------------+-------------+----------------+-----------------------------+
```

```
9 rows in set (0.01 sec)
```

# **Related Information**

- See [Working with Relational Tables and Documents](https://dev.mysql.com/doc/x-devapi-userguide/en/devapi-users-working-with-relational-tables-and-documents.md) for more information.
- See Section 13.5, "The JSON Data Type" for a detailed description of the data type.