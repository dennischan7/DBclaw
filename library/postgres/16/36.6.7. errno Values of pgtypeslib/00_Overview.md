---
source: PostgreSQL 16 Reference
title: 00_Overview
---

```
PGTYPES_NUM_BAD_NUMERIC
```

An argument should contain a numeric variable (or point to a numeric variable) but in fact its inmemory representation was invalid.

```
PGTYPES_NUM_OVERFLOW
```

An overflow occurred. Since the numeric type can deal with almost arbitrary precision, converting a numeric variable into other types might cause overflow.

```
PGTYPES_NUM_UNDERFLOW
```

An underflow occurred. Since the numeric type can deal with almost arbitrary precision, converting a numeric variable into other types might cause underflow.

```
PGTYPES_NUM_DIVIDE_ZERO
```

A division by zero has been attempted.

```
PGTYPES_DATE_BAD_DATE
```

An invalid date string was passed to the PGTYPESdate\_from\_asc function.

```
PGTYPES_DATE_ERR_EARGS
```

Invalid arguments were passed to the PGTYPESdate\_defmt\_asc function.

```
PGTYPES_DATE_ERR_ENOSHORTDATE
```

An invalid token in the input string was found by the PGTYPESdate\_defmt\_asc function.

```
PGTYPES_INTVL_BAD_INTERVAL
```

An invalid interval string was passed to the PGTYPESinterval\_from\_asc function, or an invalid interval value was passed to the PGTYPESinterval\_to\_asc function.

```
PGTYPES_DATE_ERR_ENOTDMY
```

There was a mismatch in the day/month/year assignment in the PGTYPESdate\_defmt\_asc function.

```
PGTYPES_DATE_BAD_DAY
```

An invalid day of the month value was found by the PGTYPESdate\_defmt\_asc function.

```
PGTYPES_DATE_BAD_MONTH
```

An invalid month value was found by the PGTYPESdate\_defmt\_asc function.

```
PGTYPES_TS_BAD_TIMESTAMP
```

An invalid timestamp string pass passed to the PGTYPEStimestamp\_from\_asc function, or an invalid timestamp value was passed to the PGTYPEStimestamp\_to\_asc function.

```
PGTYPES_TS_ERR_EINFTIME
```

An infinite timestamp value was encountered in a context that cannot handle it.

## <span id="page-83-1"></span>**36.6.8. Special Constants of pgtypeslib**

PGTYPESInvalidTimestamp

A value of type timestamp representing an invalid time stamp. This is returned by the function PGTYPEStimestamp\_from\_asc on parse error. Note that due to the internal representation of the timestamp data type, PGTYPESInvalidTimestamp is also a valid timestamp at the same time. It is set to 1899-12-31 23:59:59. In order to detect errors, make sure that your application does not only test for PGTYPESInvalidTimestamp but also for errno != 0 after each call to PGTYPEStimestamp\_from\_asc.

# <span id="page-83-0"></span>**36.7. Using Descriptor Areas**

An SQL descriptor area is a more sophisticated method for processing the result of a SELECT, FETCH or a DESCRIBE statement. An SQL descriptor area groups the data of one row of data together with metadata items into one data structure. The metadata is particularly useful when executing dynamic SQL statements, where the nature of the result columns might not be known ahead of time. PostgreSQL provides two ways to use Descriptor Areas: the named SQL Descriptor Areas and the C-structure SQLDAs.

# <span id="page-83-2"></span>**36.7.1. Named SQL Descriptor Areas**

A named SQL descriptor area consists of a header, which contains information concerning the entire descriptor, and one or more item descriptor areas, which basically each describe one column in the result row.

Before you can use an SQL descriptor area, you need to allocate one:

```
EXEC SQL ALLOCATE DESCRIPTOR identifier;
```

The identifier serves as the "variable name" of the descriptor area. When you don't need the descriptor anymore, you should deallocate it:

```
EXEC SQL DEALLOCATE DESCRIPTOR identifier;
```

To use a descriptor area, specify it as the storage target in an INTO clause, instead of listing host variables:

```
EXEC SQL FETCH NEXT FROM mycursor INTO SQL DESCRIPTOR mydesc;
```

If the result set is empty, the Descriptor Area will still contain the metadata from the query, i.e., the field names.

For not yet executed prepared queries, the DESCRIBE statement can be used to get the metadata of the result set:

```
EXEC SQL BEGIN DECLARE SECTION;
```

```
char *sql_stmt = "SELECT * FROM table1";
EXEC SQL END DECLARE SECTION;
EXEC SQL PREPARE stmt1 FROM :sql_stmt;
EXEC SQL DESCRIBE stmt1 INTO SQL DESCRIPTOR mydesc;
```

Before PostgreSQL 9.0, the SQL keyword was optional, so using DESCRIPTOR and SQL DESCRIP-TOR produced named SQL Descriptor Areas. Now it is mandatory, omitting the SQL keyword produces SQLDA Descriptor Areas, see [Section 36.7.2.](#page-85-0)

In DESCRIBE and FETCH statements, the INTO and USING keywords can be used to similarly: they produce the result set and the metadata in a Descriptor Area.

Now how do you get the data out of the descriptor area? You can think of the descriptor area as a structure with named fields. To retrieve the value of a field from the header and store it into a host variable, use the following command:

```
EXEC SQL GET DESCRIPTOR name :hostvar = field;
```

Currently, there is only one header field defined: COUNT, which tells how many item descriptor areas exist (that is, how many columns are contained in the result). The host variable needs to be of an

```
integer type. To get a field from the item descriptor area, use the following command:
EXEC SQL GET DESCRIPTOR name VALUE num :hostvar = field;
num can be a literal integer or a host variable containing an integer. Possible fields are:
CARDINALITY (integer)
    number of rows in the result set
DATA
    actual data item (therefore, the data type of this field depends on the query)
DATETIME_INTERVAL_CODE (integer)
    When TYPE is 9, DATETIME_INTERVAL_CODE will have a value of 1 for DATE, 2 for TIME,
    3 for TIMESTAMP, 4 for TIME WITH TIME ZONE, or 5 for TIMESTAMP WITH TIME ZONE.
DATETIME_INTERVAL_PRECISION (integer)
    not implemented
INDICATOR (integer)
    the indicator (indicating a null value or a value truncation)
KEY_MEMBER (integer)
    not implemented
LENGTH (integer)
    length of the datum in characters
NAME (string)
    name of the column
```

NULLABLE (integer)

not implemented

```
OCTET_LENGTH (integer)
    length of the character representation of the datum in bytes
PRECISION (integer)
    precision (for type numeric)
RETURNED_LENGTH (integer)
    length of the datum in characters
RETURNED_OCTET_LENGTH (integer)
    length of the character representation of the datum in bytes
SCALE (integer)
    scale (for type numeric)
TYPE (integer)
```

numeric code of the data type of the column

In EXECUTE, DECLARE and OPEN statements, the effect of the INTO and USING keywords are

different. A Descriptor Area can also be manually built to provide the input parameters for a query or a cursor and USING SQL DESCRIPTOR name is the way to pass the input parameters into a parameterized query. The statement to build a named SQL Descriptor Area is below:

```
EXEC SQL SET DESCRIPTOR name VALUE num field = :hostvar;
```

PostgreSQL supports retrieving more that one record in one FETCH statement and storing the data in host variables in this case assumes that the variable is an array. E.g.:

```
EXEC SQL BEGIN DECLARE SECTION;
int id[5];
EXEC SQL END DECLARE SECTION;
EXEC SQL FETCH 5 FROM mycursor INTO SQL DESCRIPTOR mydesc;
EXEC SQL GET DESCRIPTOR mydesc VALUE 1 :id = DATA;
```

## <span id="page-85-0"></span>**36.7.2. SQLDA Descriptor Areas**

An SQLDA Descriptor Area is a C language structure which can be also used to get the result set and the metadata of a query. One structure stores one record from the result set.

```
EXEC SQL include sqlda.h;
sqlda_t *mysqlda;
EXEC SQL FETCH 3 FROM mycursor INTO DESCRIPTOR mysqlda;
```

Note that the SQL keyword is omitted. The paragraphs about the use cases of the INTO and USING keywords in [Section 36.7.1](#page-83-2) also apply here with an addition. In a DESCRIBE statement the DESCRIPTOR keyword can be completely omitted if the INTO keyword is used:

```
EXEC SQL DESCRIBE prepared_statement INTO mysqlda;
```

The general flow of a program that uses SQLDA is:

- 1. Prepare a query, and declare a cursor for it.
- 2. Declare an SQLDA for the result rows.
- 3. Declare an SQLDA for the input parameters, and initialize them (memory allocation, parameter settings).
- 4. Open a cursor with the input SQLDA.
- 5. Fetch rows from the cursor, and store them into an output SQLDA.
- 6. Read values from the output SQLDA into the host variables (with conversion if necessary).
- 7. Close the cursor.
- 8. Free the memory area allocated for the input SQLDA.

### **36.7.2.1. SQLDA Data Structure**

SQLDA uses three data structure types: sqlda\_t, sqlvar\_t, and struct sqlname.

### **Tip**

PostgreSQL's SQLDA has a similar data structure to the one in IBM DB2 Universal Database, so some technical information on DB2's SQLDA could help understanding PostgreSQL's one better.

#### **36.7.2.1.1. sqlda\_t Structure**

The structure type sqlda\_t is the type of the actual SQLDA. It holds one record. And two or more sqlda\_t structures can be connected in a linked list with the pointer in the desc\_next field, thus representing an ordered collection of rows. So, when two or more rows are fetched, the application can read them by following the desc\_next pointer in each sqlda\_t node.

The definition of sqlda\_t is:

```
struct sqlda_struct
{
 char sqldaid[8];
 long sqldabc;
 short sqln;
 short sqld;
 struct sqlda_struct *desc_next;
 struct sqlvar_struct sqlvar[1];
};
typedef struct sqlda_struct sqlda_t;
The meaning of the fields is:
sqldaid
  It contains the literal string "SQLDA ".
sqldabc
```

It contains the size of the allocated space in bytes.

sqln

It contains the number of input parameters for a parameterized query in case it's passed into OPEN, DECLARE or EXECUTE statements using the USING keyword. In case it's used as output of SELECT, EXECUTE or FETCH statements, its value is the same as sqld statement

sqld

It contains the number of fields in a result set.

```
desc_next
```

If the query returns more than one record, multiple linked SQLDA structures are returned, and desc\_next holds a pointer to the next entry in the list.

sqlvar

This is the array of the columns in the result set.

#### **36.7.2.1.2. sqlvar\_t Structure**

The structure type sqlvar\_t holds a column value and metadata such as type and length. The definition of the type is:

```
struct sqlvar_struct
{
 short sqltype;
 short sqllen;
 char *sqldata;
 short *sqlind;
 struct sqlname sqlname;
};
typedef struct sqlvar_struct sqlvar_t;
The meaning of the fields is:
sqltype
```

Contains the type identifier of the field. For values, see enum ECPGttype in ecpgtype.h.

sqllen

Contains the binary length of the field. e.g., 4 bytes for ECPGt\_int.

sqldata

Points to the data. The format of the data is described in [Section 36.4.4.](#page-55-1)

sqlind

Points to the null indicator. 0 means not null, -1 means null.

sqlname

The name of the field.

#### **36.7.2.1.3. struct sqlname Structure**

A struct sqlname structure holds a column name. It is used as a member of the sqlvar\_t structure. The definition of the structure is:

```
#define NAMEDATALEN 64
struct sqlname
{
 short length;
 char data[NAMEDATALEN];
};
```

The meaning of the fields is:

length

Contains the length of the field name.

data

Contains the actual field name.

### **36.7.2.2. Retrieving a Result Set Using an SQLDA**

The general steps to retrieve a query result set through an SQLDA are:

- 1. Declare an sqlda\_t structure to receive the result set.
- 2. Execute FETCH/EXECUTE/DESCRIBE commands to process a query specifying the declared SQLDA.
- 3. Check the number of records in the result set by looking at sqln, a member of the sqlda\_t structure.
- 4. Get the values of each column from sqlvar[0], sqlvar[1], etc., members of the sqlda\_t structure.
- 5. Go to next row (sqlda\_t structure) by following the desc\_next pointer, a member of the sqlda\_t structure.
- 6. Repeat above as you need.

Here is an example retrieving a result set through an SQLDA.

First, declare a sqlda\_t structure to receive the result set.

```
sqlda_t *sqlda1;
```

Next, specify the SQLDA in a command. This is a FETCH command example.

```
EXEC SQL FETCH NEXT FROM cur1 INTO DESCRIPTOR sqlda1;
```

Run a loop following the linked list to retrieve the rows.

```
sqlda_t *cur_sqlda;
for (cur_sqlda = sqlda1;
 cur_sqlda != NULL;
 cur_sqlda = cur_sqlda->desc_next)
{
 ...
```

}

Inside the loop, run another loop to retrieve each column data (sqlvar\_t structure) of the row.

```
for (i = 0; i < cur_sqlda->sqld; i++)
{
 sqlvar_t v = cur_sqlda->sqlvar[i];
 char *sqldata = v.sqldata;
 short sqllen = v.sqllen;
 ...
}
```

To get a column value, check the sqltype value, a member of the sqlvar\_t structure. Then, switch to an appropriate way, depending on the column type, to copy data from the sqlvar field to a host variable.

```
char var_buf[1024];
switch (v.sqltype)
{
 case ECPGt_char:
 memset(&var_buf, 0, sizeof(var_buf));
 memcpy(&var_buf, sqldata, (sizeof(var_buf) <= sqllen ?
 sizeof(var_buf) - 1 : sqllen));
 break;
 case ECPGt_int: /* integer */
 memcpy(&intval, sqldata, sqllen);
 snprintf(var_buf, sizeof(var_buf), "%d", intval);
 break;
 ...
}
```