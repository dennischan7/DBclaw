---
source: PostgreSQL 14 Reference
title: 00_Overview
---

The catalog pg\_partitioned\_table stores information about how tables are partitioned.

### **Table 52.36. pg\_partitioned\_table Columns**

#### **Column Type Description**

partrelid oid (references [pg\\_class](#page-8-0).oid)

The OID of the [pg\\_class](#page-8-0) entry for this partitioned table

partstrat char

Partitioning strategy; h = hash partitioned table, l = list partitioned table, r = range partitioned table

partnatts int2

The number of columns in the partition key

partdefid oid (references [pg\\_class](#page-8-0).oid)

The OID of the [pg\\_class](#page-8-0) entry for the default partition of this partitioned table, or zero if this partitioned table does not have a default partition

partattrs int2vector (references [pg\\_attribute](#page-3-0).attnum)

This is an array of partnatts values that indicate which table columns are part of the partition key. For example, a value of 1 3 would mean that the first and the third table columns make up the partition key. A zero in this array indicates that the corresponding partition key column is an expression, rather than a simple column reference.

partclass oidvector (references [pg\\_opclass](#page-25-1).oid)

For each column in the partition key, this contains the OID of the operator class to use. See [pg\\_opclass](#page-25-1) for details.

partcollation oidvector (references [pg\\_collation](#page-10-0).oid)

For each column in the partition key, this contains the OID of the collation to use for partitioning, or zero if the column is not of a collatable data type.

partexprs pg\_node\_tree

Expression trees (in nodeToString() representation) for partition key columns that are not simple column references. This is a list with one element for each zero entry in partattrs. Null if all partition key columns are simple references.

# <span id="page-28-0"></span>**52.37. pg\_policy**

The catalog pg\_policy stores row-level security policies for tables. A policy includes the kind of command that it applies to (possibly all commands), the roles that it applies to, the expression to be added as a security-barrier qualification to queries that include the table, and the expression to be added as a WITH CHECK option for queries that attempt to add new records to the table.

### **Table 52.37. pg\_policy Columns**

### **Column Type Description**

oid oid

Row identifier

polname name

The name of the policy

polrelid oid (references [pg\\_class](#page-8-0).oid)

The table to which the policy applies

polcmd char

The command type to which the policy is applied: r for SELECT, a for INSERT, w for UPDATE, d for DELETE, or \* for all

polpermissive bool

Is the policy permissive or restrictive?

polroles oid[] (references [pg\\_authid](#page-5-0).oid)

The roles to which the policy is applied; zero means PUBLIC (and normally appears alone in the array)

polqual pg\_node\_tree

The expression tree to be added to the security barrier qualifications for queries that use the table

polwithcheck pg\_node\_tree

#### **Description**

The expression tree to be added to the WITH CHECK qualifications for queries that attempt to add rows to the table

## **Note**

Policies stored in pg\_policy are applied only when [pg\\_class](#page-8-0).relrowsecurity is set for their table.

# <span id="page-29-0"></span>**52.38. pg\_proc**

The catalog pg\_proc stores information about functions, procedures, aggregate functions, and window functions (collectively also known as routines). See CREATE FUNCTION, CREATE PROCE-DURE, and Section 38.3 for more information.

If prokind indicates that the entry is for an aggregate function, there should be a matching row in [pg\\_aggregate](#page-0-0).

### **Table 52.38. pg\_proc Columns**

### **Column Type Description**

oid oid

Row identifier

proname name

Name of the function

pronamespace oid (references [pg\\_namespace](#page-25-0).oid)

The OID of the namespace that contains this function

proowner oid (references [pg\\_authid](#page-5-0).oid)

Owner of the function

prolang oid (references [pg\\_language](#page-23-0).oid)

Implementation language or call interface of this function

procost float4

Estimated execution cost (in units of cpu\_operator\_cost); if proretset, this is cost per row returned

prorows float4

Estimated number of result rows (zero if not proretset)

provariadic oid (references [pg\\_type](#page-45-0).oid)

Data type of the variadic array parameter's elements, or zero if the function does not have a variadic parameter

prosupport regproc (references [pg\\_proc](#page-29-0).oid)

Planner support function for this function (see Section 38.11), or zero if none

prokind char

f for a normal function, p for a procedure, a for an aggregate function, or w for a window function

prosecdef bool

Function is a security definer (i.e., a "setuid" function)

proleakproof bool

#### **Description**

The function has no side effects. No information about the arguments is conveyed except via the return value. Any function that might throw an error depending on the values of its arguments is not leak-proof.

#### proisstrict bool

Function returns null if any call argument is null. In that case the function won't actually be called at all. Functions that are not "strict" must be prepared to handle null inputs.

#### proretset bool

Function returns a set (i.e., multiple values of the specified data type)

#### provolatile char

provolatile tells whether the function's result depends only on its input arguments, or is affected by outside factors. It is i for "immutable" functions, which always deliver the same result for the same inputs. It is s for "stable" functions, whose results (for fixed inputs) do not change within a scan. It is v for "volatile" functions, whose results might change at any time. (Use v also for functions with side-effects, so that calls to them cannot get optimized away.)

#### proparallel char

proparallel tells whether the function can be safely run in parallel mode. It is s for functions which are safe to run in parallel mode without restriction. It is r for functions which can be run in parallel mode, but their execution is restricted to the parallel group leader; parallel worker processes cannot invoke these functions. It is u for functions which are unsafe in parallel mode; the presence of such a function forces a serial execution plan.

#### pronargs int2

Number of input arguments

#### pronargdefaults int2

Number of arguments that have defaults

#### prorettype oid (references [pg\\_type](#page-45-0).oid)

Data type of the return value

#### proargtypes oidvector (references [pg\\_type](#page-45-0).oid)

An array of the data types of the function arguments. This includes only input arguments (including INOUT and VARIADIC arguments), and thus represents the call signature of the function.

#### proallargtypes oid[] (references [pg\\_type](#page-45-0).oid)

An array of the data types of the function arguments. This includes all arguments (including OUT and INOUT arguments); however, if all the arguments are IN arguments, this field will be null. Note that subscripting is 1-based, whereas for historical reasons proargtypes is subscripted from 0.

#### proargmodes char[]

An array of the modes of the function arguments, encoded as i for IN arguments, o for OUT arguments, b for INOUT arguments, v for VARIADIC arguments, t for TABLE arguments. If all the arguments are IN arguments, this field will be null. Note that subscripts correspond to positions of proallargtypes not proargtypes.

#### proargnames text[]

An array of the names of the function arguments. Arguments without a name are set to empty strings in the array. If none of the arguments have a name, this field will be null. Note that subscripts correspond to positions of proallargtypes not proargtypes.

#### proargdefaults pg\_node\_tree

Expression trees (in nodeToString() representation) for default values. This is a list with pronargdefaults elements, corresponding to the last N *input* arguments (i.e.,

#### **Description**

the last N proargtypes positions). If none of the arguments have defaults, this field will be null.

protrftypes oid[] (references [pg\\_type](#page-45-0).oid)

An array of the argument/result data type(s) for which to apply transforms (from the function's TRANSFORM clause). Null if none.

prosrc text

This tells the function handler how to invoke the function. It might be the actual source code of the function for interpreted languages, a link symbol, a file name, or just about anything else, depending on the implementation language/call convention.

probin text

Additional information about how to invoke the function. Again, the interpretation is language-specific.

prosqlbody pg\_node\_tree

Pre-parsed SQL function body. This is used for SQL-language functions when the body is given in SQL-standard notation rather than as a string literal. It's null in other cases.

proconfig text[]

Function's local settings for run-time configuration variables

proacl aclitem[]

Access privileges; see Section 5.7 for details

For compiled functions, both built-in and dynamically loaded, prosrc contains the function's C-language name (link symbol). For SQL-language functions, prosrc contains the function's source text if that is specified as a string literal; but if the function body is specified in SQL-standard style, prosrc is unused (typically it's an empty string) and prosqlbody contains the pre-parsed definition. For all other currently-known language types, prosrc contains the function's source text. probin is null except for dynamically-loaded C functions, for which it gives the name of the shared library file containing the function.

# <span id="page-31-0"></span>**52.39. pg\_publication**

The catalog pg\_publication contains all publications created in the database. For more on publications see Section 31.1.

### **Table 52.39. pg\_publication Columns**

### **Column Type**

### **Description**

oid oid

Row identifier

pubname name

Name of the publication

pubowner oid (references [pg\\_authid](#page-5-0).oid)

Owner of the publication

puballtables bool

If true, this publication automatically includes all tables in the database, including any that will be created in the future.

pubinsert bool

If true, INSERT operations are replicated for tables in the publication.

pubupdate bool

If true, UPDATE operations are replicated for tables in the publication.

#### **Description**

pubdelete bool

If true, DELETE operations are replicated for tables in the publication.

pubtruncate bool

If true, TRUNCATE operations are replicated for tables in the publication.

pubviaroot bool

If true, operations on a leaf partition are replicated using the identity and schema of its topmost partitioned ancestor mentioned in the publication instead of its own.

# <span id="page-32-0"></span>**52.40. pg\_publication\_rel**

The catalog pg\_publication\_rel contains the mapping between relations and publications in the database. This is a many-to-many mapping. See also [Section 52.79](#page-60-0) for a more user-friendly view of this information.

### **Table 52.40. pg\_publication\_rel Columns**

## **Column Type**

#### **Description**

oid oid

Row identifier

prpubid oid (references [pg\\_publication](#page-31-0).oid)

Reference to publication

prrelid oid (references [pg\\_class](#page-8-0).oid)

Reference to relation