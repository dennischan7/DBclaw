---
source: PostgreSQL 16 Reference
title: 00_Overview
---

The functions shown in [Table 9.78](#page-24-1) extract comments previously stored with the COMMENT command. A null value is returned if no comment could be found for the specified parameters.

### <span id="page-24-1"></span>**Table 9.78. Comment Information Functions**

### **Function**

### **Description**

col\_description ( table oid, column integer ) → text

#### **Description**

Returns the comment for a table column, which is specified by the OID of its table and its column number. (obj\_description cannot be used for table columns, since columns do not have OIDs of their own.)

obj\_description ( object oid, catalog name ) → text

Returns the comment for a database object specified by its OID and the name of the containing system catalog. For example, obj\_description(123456, 'pg\_class') would retrieve the comment for the table with OID 123456.

obj\_description ( object oid ) → text

Returns the comment for a database object specified by its OID alone. This is *deprecated* since there is no guarantee that OIDs are unique across different system catalogs; therefore, the wrong comment might be returned.

shobj\_description ( object oid, catalog name ) → text

Returns the comment for a shared database object specified by its OID and the name of the containing system catalog. This is just like obj\_description except that it is used for retrieving comments on shared objects (that is, databases, roles, and tablespaces). Some system catalogs are global to all databases within each cluster, and the descriptions for objects in them are stored globally as well.

## <span id="page-25-0"></span>**9.26.7. Data Validity Checking Functions**

The functions shown in [Table 9.79](#page-25-0) can be helpful for checking validity of proposed input data.

### **Table 9.79. Data Validity Checking Functions**

### **Function**

### **Description Example(s)**

pg\_input\_is\_valid ( string text, type text ) → boolean

Tests whether the given string is valid input for the specified data type, returning true or false.

This function will only work as desired if the data type's input function has been updated to report invalid input as a "soft" error. Otherwise, invalid input will abort the transaction, just as if the string had been cast to the type directly.

```
pg_input_is_valid('42', 'integer') → t
pg_input_is_valid('42000000000', 'integer') → f
pg_input_is_valid('1234.567', 'numeric(7,4)') → f
```

pg\_input\_error\_info ( string text, type text ) → record ( message text, detail text, hint text, sql\_error\_code text )

Tests whether the given string is valid input for the specified data type; if not, return the details of the error that would have been thrown. If the input is valid, the results are NULL. The inputs are the same as for pg\_input\_is\_valid.

This function will only work as desired if the data type's input function has been updated to report invalid input as a "soft" error. Otherwise, invalid input will abort the transaction, just as if the string had been cast to the type directly.

```
select * from pg_input_error_info('42000000000', 'integer')
→
 message |
```

```
 detail | hint | sql_error_code
```

## **Function Description Example(s)** ------------------------------------------------------ +--------+------+--------------- value "42000000000" is out of range for type integer | | | 22003 select message, detail from pg\_input\_error\_info('1234.567', 'numeric(7,4)') → message | detail ------------------------+---------------------------------- ------------------------------------------------ numeric field overflow | A field with precision 7, scale 4 must round to an absolute value less than 10^3.