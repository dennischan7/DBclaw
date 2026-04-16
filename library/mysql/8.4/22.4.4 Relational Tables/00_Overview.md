---
source: MySQL 8.4 Reference
title: 00_Overview
---

You can also use X DevAPI to work with relational tables. In MySQL, each relational table is associated with a particular storage engine. The examples in this section use InnoDB tables in the world\_x schema.

# **Confirm the Schema**

To show the schema that is assigned to the db global variable, issue db.

```
mysql-py> db
<Schema:world_x>
```

If the returned value is not Schema:world\_x, set the db variable as follows:

```
mysql-py> \use world_x
Schema `world_x` accessible through db.
```

# **Show All Tables**

To display all relational tables in the world\_x schema, use the get\_tables() method on the db object.

```
mysql-py> db.get_tables()
 <Table:city>,
 <Table:country>,
 <Table:countrylanguage>
```

# **Basic Table Operations**

Basic operations scoped by tables include:

| Operation form   | Description                                                              |
|------------------|--------------------------------------------------------------------------|
| db.name.insert() | The insert() method inserts one or more records<br>into the named table. |
| db.name.select() | The select() method returns some or all records in<br>the named table.   |
| db.name.update() | The update() method updates records in the<br>named table.               |
| db.name.delete() | The delete() method deletes one or more records<br>from the named table. |

# **Related Information**

- See [Working with Relational Tables](https://dev.mysql.com/doc/x-devapi-userguide/en/devapi-users-working-with-relational-tables.md) for more information.
- [CRUD EBNF Definitions](https://dev.mysql.com/doc/x-devapi-userguide/en/mysql-x-crud-ebnf-definitions.md) provides a complete list of operations.
- See [Section 22.4.2, "Download and Import world\\_x Database"](#page-0-0) for instructions on setting up the world\_x schema sample.

# <span id="page-12-0"></span>**22.4.4.1 Insert Records into Tables**

You can use the insert() method with the values() method to insert records into an existing relational table. The insert() method accepts individual columns or all columns in the table. Use one or more values() methods to specify the values to be inserted.

### **Insert a Complete Record**

To insert a complete record, pass to the insert() method all columns in the table. Then pass to the values() method one value for each column. For example, to add a new record to the city table in the world\_x database, insert the following record and press **Enter** twice.

```
mysql-py> db.city.insert("ID", "Name", "CountryCode", "District", "Info").values(
None, "Olympia", "USA", "Washington", '{"Population": 5000}')
```

The city table has five columns: ID, Name, CountryCode, District, and Info. Each value must match the data type of the column it represents.

# **Insert a Partial Record**

The following example inserts values into the ID, Name, and CountryCode columns of the city table.

```
mysql-py> db.city.insert("ID", "Name", "CountryCode").values(
```

```
None, "Little Falls", "USA").values(None, "Happy Valley", "USA")
```

When you specify columns using the insert() method, the number of values must match the number of columns. In the previous example, you must supply three values to match the three columns specified.

# **Related Information**

• See [TableInsertFunction](https://dev.mysql.com/doc/x-devapi-userguide/en/crud-ebnf-table-crud-functions.md#crud-ebnf-tableinsertfunction) for the full syntax definition.

# <span id="page-13-0"></span>**22.4.4.2 Select Tables**

You can use the select() method to query for and return records from a table in a database. The X DevAPI provides additional methods to use with the select() method to filter and sort the returned records.

MySQL provides the following operators to specify search conditions: OR (||), AND (&&), XOR, IS, NOT, BETWEEN, IN, LIKE, !=, <>, >, >=, <, <=, &, |, <<, >>, +, -, \*, /, ~, and %.

# **Select All Records**

To issue a query that returns all records from an existing table, use the select() method without specifying search conditions. The following example selects all records from the city table in the world\_x database.

![](_page_13_Picture_10.jpeg)

#### **Note**

Limit the use of the empty select() method to interactive statements. Always use explicit column-name selections in your application code.

```
mysql-py> db.city.select()
+------+------------+-------------+------------+-------------------------+
| ID | Name | CountryCode | District | Info |
+------+------------+-------------+------------+-------------------------+
| 1 | Kabul | AFG | Kabol |{"Population": 1780000} |
| 2 | Qandahar | AFG | Qandahar |{"Population": 237500} |
| 3 | Herat | AFG | Herat |{"Population": 186800} |
... ... ... ... ...
| 4079 | Rafah | PSE | Rafah |{"Population": 92020} |
+------+------- ----+-------------+------------+-------------------------+
4082 rows in set (0.01 sec)
```

An empty set (no matching records) returns the following information:

```
Empty set (0.00 sec)
```

### **Filter Searches**

To issue a query that returns a set of table columns, use the select() method and specify the columns to return between square brackets. This query returns the Name and CountryCode columns from the city table.

```
mysql-py> db.city.select(["Name", "CountryCode"])
+-------------------+-------------+
| Name | CountryCode |
+-------------------+-------------+
| Kabul | AFG |
| Qandahar | AFG |
| Herat | AFG |
| Mazar-e-Sharif | AFG |
| Amsterdam | NLD |
... ...
| Rafah | PSE |
| Olympia | USA |
| Little Falls | USA |
```

```
| Happy Valley | USA |
+-------------------+-------------+
4082 rows in set (0.00 sec)
```

To issue a query that returns rows matching specific search conditions, use the where() method to include those conditions. For example, the following example returns the names and country codes of the cities that start with the letter Z.

```
mysql-py> db.city.select(["Name", "CountryCode"]).where("Name like 'Z%'")
+-------------------+-------------+
| Name | CountryCode |
+-------------------+-------------+
| Zaanstad | NLD |
| Zoetermeer | NLD |
| Zwolle | NLD |
| Zenica | BIH |
| Zagazig | EGY |
| Zaragoza | ESP |
| Zamboanga | PHL |
| Zahedan | IRN |
| Zanjan | IRN |
| Zabol | IRN |
| Zama | JPN |
| Zhezqazghan | KAZ |
| Zhengzhou | CHN |
... ...
| Zeleznogorsk | RUS |
+-------------------+-------------+
59 rows in set (0.00 sec)
```

You can separate a value from the search condition by using the bind() method. For example, instead of using "Name = 'Z%' " as the condition, substitute a named placeholder consisting of a colon followed by a name that begins with a letter, such as name. Then include the placeholder and value in the bind() method as follows:

```
mysql-py> db.city.select(["Name", "CountryCode"]).where(
"Name like :name").bind("name", "Z%")
```

![](_page_14_Picture_6.jpeg)

#### **Tip**

Within a program, binding enables you to specify placeholders in your expressions, which are filled in with values before execution and can benefit from automatic escaping, as appropriate.

Always use binding to sanitize input. Avoid introducing values in queries using string concatenation, which can produce invalid input and, in some cases, can cause security issues.

### **Project Results**

To issue a query using the AND operator, add the operator between search conditions in the where() method.

```
mysql-py> db.city.select(["Name", "CountryCode"]).where(
"Name like 'Z%' and CountryCode = 'CHN'")
+----------------+-------------+
| Name | CountryCode |
+----------------+-------------+
| Zhengzhou | CHN |
| Zibo | CHN |
| Zhangjiakou | CHN |
| Zhuzhou | CHN |
| Zhangjiang | CHN |
| Zigong | CHN |
| Zaozhuang | CHN |
... ...
| Zhangjiagang | CHN |
+----------------+-------------+
```

```
22 rows in set (0.01 sec)
```

To specify multiple conditional operators, you can enclose the search conditions in parenthesis to change the operator precedence. The following example demonstrates the placement of AND and OR operators.

```
mysql-py> db.city.select(["Name", "CountryCode"]).where(
"Name like 'Z%' and (CountryCode = 'CHN' or CountryCode = 'RUS')")
+-------------------+-------------+
| Name | CountryCode |
+-------------------+-------------+
| Zhengzhou | CHN |
| Zibo | CHN |
| Zhangjiakou | CHN |
| Zhuzhou | CHN |
... ...
| Zeleznogorsk | RUS |
+-------------------+-------------+
29 rows in set (0.01 sec)
```

# **Limit, Order, and Offset Results**

You can apply the limit(), order\_by(), and offset() methods to manage the number and order of records returned by the select() method.

To specify the number of records included in a result set, append the limit() method with a value to the select() method. For example, the following query returns the first five records in the country table.

```
mysql-py> db.country.select(["Code", "Name"]).limit(5)
+------+-------------+
| Code | Name |
+------+-------------+
| ABW | Aruba |
| AFG | Afghanistan |
| AGO | Angola |
| AIA | Anguilla |
| ALB | Albania |
+------+-------------+
5 rows in set (0.00 sec)
```

To specify an order for the results, append the order\_by() method to the select() method. Pass to the order\_by() method a list of one or more columns to sort by and, optionally, the descending (desc) or ascending (asc) attribute as appropriate. Ascending order is the default order type.

For example, the following query sorts all records by the Name column and then returns the first three records in descending order .

```
mysql-py> db.country.select(["Code", "Name"]).order_by(["Name desc"]).limit(3)
+------+------------+
| Code | Name |
+------+------------+
| ZWE | Zimbabwe |
| ZMB | Zambia |
| YUG | Yugoslavia |
+------+------------+
3 rows in set (0.00 sec)
```

By default, the limit() method starts from the first record in the table. You can use the offset() method to change the starting record. For example, to ignore the first record and return the next three records matching the condition, pass to the offset() method a value of 1.

```
mysql-py> db.country.select(["Code", "Name"]).order_by(["Name desc"]).limit(3).offset(1)
+------+------------+
| Code | Name |
+------+------------+
| ZMB | Zambia |
| YUG | Yugoslavia |
```

```
| YEM | Yemen |
+------+------------+
3 rows in set (0.00 sec)
```

# **Related Information**

- The MySQL Reference Manual provides detailed documentation on functions and operators.
- See [TableSelectFunction](https://dev.mysql.com/doc/x-devapi-userguide/en/crud-ebnf-table-crud-functions.md#crud-ebnf-tableselectfunction) for the full syntax definition.

# <span id="page-16-0"></span>**22.4.4.3 Update Tables**

You can use the update() method to modify one or more records in a table. The update() method works by filtering a query to include only the records to be updated and then applying the operations you specify to those records.

To replace a city name in the city table, pass to the set() method the new city name. Then, pass to the where() method the city name to locate and replace. The following example replaces the city Peking with Beijing.

```
mysql-py> db.city.update().set("Name", "Beijing").where("Name = 'Peking'")
```

Use the select() method to verify the change.

```
mysql-py> db.city.select(["ID", "Name", "CountryCode", "District", "Info"]).where("Name = 'Beijing'")
+------+-----------+-------------+----------+-----------------------------+
| ID | Name | CountryCode | District | Info |
+------+-----------+-------------+----------+-----------------------------+
| 1891 | Beijing | CHN | Peking | {"Population": 7472000} |
+------+-----------+-------------+----------+-----------------------------+
1 row in set (0.00 sec)
```

# **Related Information**

• See [TableUpdateFunction](https://dev.mysql.com/doc/x-devapi-userguide/en/crud-ebnf-table-crud-functions.md#crud-ebnf-tableupdatefunction) for the full syntax definition.

# <span id="page-16-1"></span>**22.4.4.4 Delete Tables**

You can use the delete() method to remove some or all records from a table in a database. The X DevAPI provides additional methods to use with the delete() method to filter and order the records to be deleted.

### **Delete Records Using Conditions**

The example that follows passes search conditions to the delete() method. All records matching the condition are deleted from the city table. In this example, one record matches the condition.

```
mysql-py> db.city.delete().where("Name = 'Olympia'")
```

### **Delete the First Record**

To delete the first record in the city table, use the limit() method with a value of 1.

```
mysql-py> db.city.delete().limit(1)
```

# **Delete All Records in a Table**

You can delete all records in a table. To do so, use the delete() method without specifying a search condition.

![](_page_16_Picture_23.jpeg)

# **Caution**

Use care when you delete records without specifying a search condition; doing so deletes all records from the table.

### **Drop a Table**

The drop\_collection() method is also used in MySQL Shell to drop a relational table from a database. For example, to drop the citytest table from the world\_x database, issue:

```
mysql-py> db.drop_collection("citytest")
```

# **Related Information**

- See [TableDeleteFunction](https://dev.mysql.com/doc/x-devapi-userguide/en/crud-ebnf-table-crud-functions.md#crud-ebnf-tabledeletefunction) for the full syntax definition.
- See [Section 22.4.2, "Download and Import world\\_x Database"](#page-0-0) for instructions to recreate the world\_x database.