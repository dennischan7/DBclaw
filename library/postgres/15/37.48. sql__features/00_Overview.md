---
source: PostgreSQL 15 Reference
title: 00_Overview
---

The table sql\_features contains information about which formal features defined in the SQL standard are supported by PostgreSQL. This is the same information that is presented in Appendix D. There you can also find some additional background information.

### **Table 37.46. sql\_features Columns**

## **Column Type Description** feature\_id character\_data Identifier string of the feature feature\_name character\_data

## **Column Type**

#### **Description**

Descriptive name of the feature

sub\_feature\_id character\_data

Identifier string of the subfeature, or a zero-length string if not a subfeature

sub\_feature\_name character\_data

Descriptive name of the subfeature, or a zero-length string if not a subfeature

is\_supported yes\_or\_no

YES if the feature is fully supported by the current version of PostgreSQL, NO if not

is\_verified\_by character\_data

Always null, since the PostgreSQL development group does not perform formal testing of feature conformance

comments character\_data

Possibly a comment about the supported status of the feature