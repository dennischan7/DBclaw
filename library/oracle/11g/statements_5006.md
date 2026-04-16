# Oracle 11g - statements_5006
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/statements_5006.htm

Semantics

schema

Specify the schema in which the dimension will be created. If you do not specify `schema`, then Oracle Database creates the dimension in your own schema.

dimension

Specify the name of the dimension. The name must be unique within its schema and satisfy the requirements listed in ["Database Object Naming Rules"](sql_elements008.md#i27570).

level\_clause

The `level_clause` defines a level in the dimension. A level defines dimension hierarchies and attributes.

level Specify the name of the level.

level\_table . level\_column Specify the columns in the level. You can specify up to 32 columns. The tables you specify in this clause must already exist.

SKIP WHEN NULL  Specify this clause to indicate that if the specified level is `NULL`, then the level is to be skipped. This clause lets you preserve the hierarchical chain of parent-child relationship by an alternative path that skips over the specified level. See [hierarchy\_clause](#i2061857) .

Restrictions on Dimension Level Columns Dimension level columns are subject to the following restrictions:

* All of the columns in a level must come from the same table.
* If columns in different levels come from different tables, then you must specify the `dimension_join_clause`.
* The set of columns you specify must be unique to this level.
* The columns you specify cannot be specified in any other dimension.
* Each `level_column` must be non-null unless the level is specified with `SKIP` `WHEN` `NULL`. The non-null columns need not have `NOT` `NULL` constraints. The column for which you specify `SKIP` `WHEN` `NULL` cannot have a `NOT` `NULL` constraint).

hierarchy\_clause

The `hierarchy_clause` defines a linear hierarchy of levels in the dimension. Each hierarchy forms a chain of parent-child relationships among the levels in the dimension. Hierarchies in a dimension are independent of each other. They may, but need not, have columns in common.

Each level in the dimension should be specified at most once in this clause, and each level must already have been named in the `level_clause.`

hierarchy Specify the name of the hierarchy. This name must be unique in the dimension.

child\_level Specify the name of a level that has an n:1 relationship with a parent level. The `level_columns` of `child_level` cannot be null, and each `child_level` value uniquely determines the value of the next named `parent_level`.

If the child `level_table` is different from the parent `level_table`, then you must specify a join relationship between them in the `dimension_join_clause`.

parent\_level Specify the name of a level.

dimension\_join\_clause

The `dimension_join_clause` lets you specify an inner equijoin relationship for a dimension whose columns are contained in multiple tables. This clause is required and permitted only when the columns specified in the hierarchy are not all in the same table.

child\_key\_column

Specify one or more columns that are join-compatible with columns in the parent level.

If you do not specify the schema and table of each `child_column`, then the schema and table are inferred from the `CHILD` `OF` relationship in the `hierarchy_clause`. If you do specify the schema and column of a `child_key_column`, then the schema and table must match the schema and table of columns in the child of `parent_level` in the `hierarchy_clause`.

parent\_level

Specify the name of a level.

Restrictions on Join Dimensions Join dimensions are subject to the following restrictions:

* You can specify only one `dimension_join_clause` for a given pair of levels in the same hierarchy.
* The `child_key_columns` must be non-null, and the parent key must be unique and non-null. You need not define constraints to enforce these conditions, but queries may return incorrect results if these conditions are not true.
* Each child key must join with a key in the `parent_level` table.
* Self-joins are not permitted. The `child_key_columns` cannot be in the same table as `parent_level`.
* All of the child key columns must come from the same table.
* The number of child key columns must match the number of columns in `parent_level`, and the columns must be joinable.
* You cannot specify multiple child key columns unless the parent level consists of multiple columns.

attribute\_clause

The `attribute_clause` lets you specify the columns that are uniquely determined by a hierarchy level. The columns in `level` must all come from the same table as the `dependent_columns`. The `dependent_columns` need not have been specified in the `level_clause`.

For example, if the hierarchy levels are `city`, `state`, and `country`, then `city` might determine `mayor`, `state` might determine `governor`, and `country` might determine `president`.

extended\_attribute\_clause

This clause lets you specify an attribute name for one or more level-to-column relations. The type of attribute you create with this clause is not different from the type of attribute created using the `attribute_clause`. The only difference is that this clause lets you assign a name to the attribute that is different from the level name.

Examples

Creating a Dimension: Examples This statement was used to create the `customers_dim` dimension in the sample schema `sh`:

```
CREATE DIMENSION customers_dim 
   LEVEL customer   IS (customers.cust_id)
   LEVEL city       IS (customers.cust_city) 
   LEVEL state      IS (customers.cust_state_province) 
   LEVEL country    IS (countries.country_id) 
   LEVEL subregion  IS (countries.country_subregion) 
   LEVEL region     IS (countries.country_region) 
   HIERARCHY geog_rollup (
      customer      CHILD OF
      city          CHILD OF 
      state         CHILD OF 
      country       CHILD OF 
      subregion     CHILD OF 
      region 
   JOIN KEY (customers.country_id) REFERENCES country
   )
   ATTRIBUTE customer DETERMINES
   (cust_first_name, cust_last_name, cust_gender, 
    cust_marital_status, cust_year_of_birth, 
    cust_income_level, cust_credit_limit) 
   ATTRIBUTE country DETERMINES (countries.country_name)
;
```

Creating a Dimension with Extended Attributes: Example Alternatively, the `extended_attribute_clause` could have been used instead of the `attribute_clause`, as shown in the following example:

```
CREATE DIMENSION customers_dim 
   LEVEL customer   IS (customers.cust_id)
   LEVEL city       IS (customers.cust_city) 
   LEVEL state      IS (customers.cust_state_province) 
   LEVEL country    IS (countries.country_id) 
   LEVEL subregion  IS (countries.country_subregion) 
   LEVEL region     IS (countries.country_region) 
   HIERARCHY geog_rollup (
      customer      CHILD OF
      city          CHILD OF 
      state         CHILD OF 
      country       CHILD OF 
      subregion     CHILD OF 
      region 
   JOIN KEY (customers.country_id) REFERENCES country
   )
   ATTRIBUTE customer_info LEVEL customer DETERMINES
   (cust_first_name, cust_last_name, cust_gender, 
    cust_marital_status, cust_year_of_birth, 
    cust_income_level, cust_credit_limit) 
   ATTRIBUTE country DETERMINES (countries.country_name);
```

Creating a Dimension with NULL Column Values: Example The following example shows how to create the dimension if one of the level columns is null and you want to preserve the hierarchical chain. The example uses the `cust_marital_status` column for simplicity because it is not a `NOT` `NULL` column. If it had such a constraint, then you would have to disable the constraint before using the `SKIP` `WHEN` `NULL` clause.

```
CREATE DIMENSION customers_dim
   LEVEL customer IS (customers.cust_id)
   LEVEL status IS (customers.cust_marital_status) SKIP WHEN NULL
   LEVEL city IS (customers.cust_city)
   LEVEL state IS (customers.cust_state_province)
   LEVEL country IS (countries.country_id)
   LEVEL subregion IS (countries.country_subregion) SKIP WHEN NULL
   LEVEL region IS (countries.country_region)
   HIERARCHY geog_rollup (
      customer CHILD OF
      city CHILD OF
      state CHILD OF
      country CHILD OF
      subregion CHILD OF
      region
   JOIN KEY (customers.country_id) REFERENCES country
   )
   ATTRIBUTE customer DETERMINES
   (cust_first_name, cust_last_name, cust_gender,
    cust_marital_status, cust_year_of_birth,
    cust_income_level, cust_credit_limit)
   ATTRIBUTE country DETERMINES (countries.country_name)
;
```