# Oracle 19c - ROWID-Pseudocolumn
Source: https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/ROWID-Pseudocolumn.html

For each row in the database, the `ROWID` pseudocolumn returns the address of the row. Oracle Database rowid values contain information necessary to locate a row:

* The data object number of the object
* The data block in the data file in which the row resides
* The position of the row in the data block (first row is 0)
* The data file in which the row resides (first file is 1). The file number is relative to the tablespace.

Usually, a rowid value uniquely identifies a row in the database. However, rows in different tables that are stored together in the same cluster can have the same rowid.

Values of the `ROWID` pseudocolumn have the data type `ROWID` or `UROWID`. Refer to [Rowid Data Types](Data-Types.md#GUID-4231B94A-97E9-4B59-91EB-E7B2D0DA438C) and [UROWID Data Type](Data-Types.md#GUID-E9F3AE1C-AA6D-4262-A15F-778833251361) for more information.

Rowid values have several important uses:

* They are the fastest way to access a single row.
* They can show you how the rows in a table are stored.
* They are unique identifiers for rows in a table.

You should not use `ROWID` as the primary key of a table. If you delete and reinsert a row with the Import and Export utilities, for example, then its rowid may change. If you delete a row, then Oracle may reassign its rowid to a new row inserted later.

Although you can use the `ROWID` pseudocolumn in the `SELECT` and `WHERE` clause of a query, these pseudocolumn values are not actually stored in the database. You cannot insert, update, or delete a value of the `ROWID` pseudocolumn.

This statement selects the address of all rows that contain data for employees in department 20:

```
SELECT ROWID, last_name
  FROM employees
  WHERE department_id = 20;
```