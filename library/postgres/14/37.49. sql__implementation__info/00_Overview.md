---
source: PostgreSQL 14 Reference
title: 00_Overview
---

The table sql\_implementation\_info contains information about various aspects that are left implementation-defined by the SQL standard. This information is primarily intended for use in the context of the ODBC interface; users of other interfaces will probably find this information to be of little use. For this reason, the individual implementation information items are not described here; you will find them in the description of the ODBC interface.

### **Table 37.47. sql\_implementation\_info Columns**

### **Column Type**

#### **Description**

implementation\_info\_id character\_data

Identifier string of the implementation information item

implementation\_info\_name character\_data

Descriptive name of the implementation information item

integer\_value cardinal\_number

Value of the implementation information item, or null if the value is contained in the column character\_value

character\_value character\_data

Value of the implementation information item, or null if the value is contained in the column integer\_value

comments character\_data

Possibly a comment pertaining to the implementation information item