---
source: PostgreSQL 15 Reference
title: 00_Overview
---

This section describes the SQL-compliant conditional expressions available in PostgreSQL.

### **Tip**

If your needs go beyond the capabilities of these conditional expressions, you might want to consider writing a server-side function in a more expressive programming language.

### **Note**

Although COALESCE, GREATEST, and LEAST are syntactically similar to functions, they are not ordinary functions, and thus cannot be used with explicit VARIADIC array arguments.