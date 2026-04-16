---
source: PostgreSQL 14 Reference
title: 00_Overview
---

The pg\_enum catalog contains entries showing the values and labels for each enum type. The internal representation of a given enum value is actually the OID of its associated row in pg\_enum.

### **Table 52.20. pg\_enum Columns**

## **Column Type**

#### **Description**

oid oid

Row identifier

enumtypid oid (references [pg\\_type](#page-45-0).oid)

The OID of the [pg\\_type](#page-45-0) entry owning this enum value

enumsortorder float4

The sort position of this enum value within its enum type

enumlabel name

The textual label for this enum value

The OIDs for pg\_enum rows follow a special rule: even-numbered OIDs are guaranteed to be ordered in the same way as the sort ordering of their enum type. That is, if two even OIDs belong to the same enum type, the smaller OID must have the smaller enumsortorder value. Odd-numbered OID values need bear no relationship to the sort order. This rule allows the enum comparison routines to avoid catalog lookups in many common cases. The routines that create and alter enum types attempt to assign even OIDs to enum values whenever possible.

When an enum type is created, its members are assigned sort-order positions 1..n. But members added later might be given negative or fractional values of enumsortorder. The only requirement on these values is that they be correctly ordered and unique within each enum type.