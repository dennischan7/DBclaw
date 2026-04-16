---
source: PostgreSQL 15 Reference
title: 00_Overview
---

PostgreSQL provides the standard SQL type boolean; see [Table 8.19.](#page-2-1) The boolean type can have several states: "true", "false", and a third state, "unknown", which is represented by the SQL null value.

<span id="page-2-1"></span>**Table 8.19. Boolean Data Type**

| Name    | Storage Size | Description            |
|---------|--------------|------------------------|
| boolean | 1 byte       | state of true or false |

Boolean constants can be represented in SQL queries by the SQL key words TRUE, FALSE, and NULL.

The datatype input function for type boolean accepts these string representations for the "true" state:

```
true
yes
on
1
```

and these representations for the "false" state:

```
false
no
off
0
```

Unique prefixes of these strings are also accepted, for example t or n. Leading or trailing whitespace is ignored, and case does not matter.

<span id="page-3-0"></span>The datatype output function for type boolean always emits either t or f, as shown in [Example 8.2.](#page-3-0)

### **Example 8.2. Using the boolean Type**

```
CREATE TABLE test1 (a boolean, b text);
INSERT INTO test1 VALUES (TRUE, 'sic est');
INSERT INTO test1 VALUES (FALSE, 'non est');
SELECT * FROM test1;
 a | b
---+---------
 t | sic est
 f | non est
SELECT * FROM test1 WHERE a;
 a | b
---+---------
 t | sic est
```

The key words TRUE and FALSE are the preferred (SQL-compliant) method for writing Boolean constants in SQL queries. But you can also use the string representations by following the generic string-literal constant syntax described in Section 4.1.2.7, for example 'yes'::boolean.

Note that the parser automatically understands that TRUE and FALSE are of type boolean, but this is not so for NULL because that can have any type. So in some contexts you might have to cast NULL to boolean explicitly, for example NULL::boolean. Conversely, the cast can be omitted from a string-literal Boolean value in contexts where the parser can deduce that the literal must be of type boolean.

# <span id="page-3-1"></span>**8.7. Enumerated Types**

Enumerated (enum) types are data types that comprise a static, ordered set of values. They are equivalent to the enum types supported in a number of programming languages. An example of an enum type might be the days of the week, or a set of status values for a piece of data.