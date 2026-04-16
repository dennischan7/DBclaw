---
source: PostgreSQL 15 Reference
title: 00_Overview
---

The view sequences contains all sequences defined in the current database. Only those sequences are shown that the current user has access to (by way of being the owner or having some privilege).

### **Table 37.45. sequences Columns**

### **Column Type Description** sequence\_catalog sql\_identifier Name of the database that contains the sequence (always the current database) sequence\_schema sql\_identifier Name of the schema that contains the sequence sequence\_name sql\_identifier Name of the sequence data\_type character\_data The data type of the sequence. numeric\_precision cardinal\_number This column contains the (declared or implicit) precision of the sequence data type (see above). The precision indicates the number of significant digits. It can be expressed in decimal (base 10) or binary (base 2) terms, as specified in the column numeric\_precision\_radix. numeric\_precision\_radix cardinal\_number This column indicates in which base the values in the columns numeric\_precision and numeric\_scale are expressed. The value is either 2 or 10. numeric\_scale cardinal\_number This column contains the (declared or implicit) scale of the sequence data type (see above). The scale indicates the number of significant digits to the right of the decimal point. It can be expressed in decimal (base 10) or binary (base 2) terms, as specified in the column numeric\_precision\_radix. start\_value character\_data The start value of the sequence minimum\_value character\_data

The minimum value of the sequence

maximum\_value character\_data

The maximum value of the sequence

increment character\_data

The increment of the sequence

cycle\_option yes\_or\_no

YES if the sequence cycles, else NO

Note that in accordance with the SQL standard, the start, minimum, maximum, and increment values are returned as character strings.