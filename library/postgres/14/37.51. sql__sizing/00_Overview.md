---
source: PostgreSQL 14 Reference
title: 00_Overview
---

The table sql\_sizing contains information about various size limits and maximum values in PostgreSQL. This information is primarily intended for use in the context of the ODBC interface; users of other interfaces will probably find this information to be of little use. For this reason, the individual sizing items are not described here; you will find them in the description of the ODBC interface.

### **Table 37.49. sql\_sizing Columns**

#### **Column Type Description**

sizing\_id cardinal\_number

Identifier of the sizing item

sizing\_name character\_data

Descriptive name of the sizing item

supported\_value cardinal\_number

Value of the sizing item, or 0 if the size is unlimited or cannot be determined, or null if the features for which the sizing item is applicable are not supported

comments character\_data

Possibly a comment pertaining to the sizing item