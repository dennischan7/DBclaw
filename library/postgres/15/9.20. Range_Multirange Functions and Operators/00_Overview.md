---
source: PostgreSQL 15 Reference
title: 00_Overview
---

See [Section 8.17](#page-42-0) for an overview of range types.

[Table 9.54](#page-183-0) shows the specialized operators available for range types. [Table 9.55](#page-184-0) shows the specialized operators available for multirange types. In addition to those, the usual comparison operators shown in [Table 9.1](#page-55-0) are available for range and multirange types. The comparison operators order first by the range lower bounds, and only if those are equal do they compare the upper bounds. The multirange operators compare each range until one is unequal. This does not usually result in a useful overall ordering, but the operators are provided to allow unique indexes to be constructed on ranges.

#### <span id="page-183-0"></span>**Table 9.54. Range Operators**

```
Operator
       Description
       Example(s)
anyrange @> anyrange → boolean
       Does the first range contain the second?
       int4range(2,4) @> int4range(2,3) → t
anyrange @> anyelement → boolean
       Does the range contain the element?
       '[2011-01-01,2011-03-01)'::tsrange @> '2011-01-10'::time-
       stamp → t
anyrange <@ anyrange → boolean
       Is the first range contained by the second?
       int4range(2,4) <@ int4range(1,7) → t
anyelement <@ anyrange → boolean
       Is the element contained in the range?
       42 <@ int4range(1,7) → f
anyrange && anyrange → boolean
       Do the ranges overlap, that is, have any elements in common?
       int8range(3,7) && int8range(4,12) → t
anyrange << anyrange → boolean
       Is the first range strictly left of the second?
       int8range(1,10) << int8range(100,110) → t
anyrange >> anyrange → boolean
       Is the first range strictly right of the second?
       int8range(50,60) >> int8range(20,30) → t
anyrange &< anyrange → boolean
       Does the first range not extend to the right of the second?
       int8range(1,20) &< int8range(18,20) → t
anyrange &> anyrange → boolean
       Does the first range not extend to the left of the second?
       int8range(7,20) &> int8range(5,10) → t
anyrange -|- anyrange → boolean
```

### **Operator Description Example(s)** Are the ranges adjacent? numrange(1.1,2.2) -|- numrange(2.2,3.3) → t anyrange + anyrange → anyrange Computes the union of the ranges. The ranges must overlap or be adjacent, so that the union is a single range (but see range\_merge()). numrange(5,15) + numrange(10,20) → [5,20) anyrange \* anyrange → anyrange Computes the intersection of the ranges. int8range(5,15) \* int8range(10,20) → [10,15) anyrange - anyrange → anyrange Computes the difference of the ranges. The second range must not be contained in the first in such a way that the difference would not be a single range.

int8range(5,15) - int8range(10,20) → [5,10)

#### <span id="page-184-0"></span>**Table 9.55. Multirange Operators**

```
Operator
      Description
      Example(s)
anymultirange @> anymultirange → boolean
      Does the first multirange contain the second?
       '{[2,4)}'::int4multirange @> '{[2,3)}'::int4multirange → t
anymultirange @> anyrange → boolean
      Does the multirange contain the range?
       '{[2,4)}'::int4multirange @> int4range(2,3) → t
anymultirange @> anyelement → boolean
      Does the multirange contain the element?
       '{[2011-01-01,2011-03-01)}'::tsmultirange @>
       '2011-01-10'::timestamp → t
anyrange @> anymultirange → boolean
      Does the range contain the multirange?
       '[2,4)'::int4range @> '{[2,3)}'::int4multirange → t
anymultirange <@ anymultirange → boolean
      Is the first multirange contained by the second?
       '{[2,4)}'::int4multirange <@ '{[1,7)}'::int4multirange → t
anymultirange <@ anyrange → boolean
      Is the multirange contained by the range?
       '{[2,4)}'::int4multirange <@ int4range(1,7) → t
anyrange <@ anymultirange → boolean
      Is the range contained by the multirange?
      int4range(2,4) <@ '{[1,7)}'::int4multirange → t
anyelement <@ anymultirange → boolean
      Is the element contained by the multirange?
```

```
Operator
      Description
      Example(s)
      4 <@ '{[1,7)}'::int4multirange → t
anymultirange && anymultirange → boolean
      Do the multiranges overlap, that is, have any elements in common?
       '{[3,7)}'::int8multirange && '{[4,12)}'::int8multirange → t
anymultirange && anyrange → boolean
      Does the multirange overlap the range?
       '{[3,7)}'::int8multirange && int8range(4,12) → t
anyrange && anymultirange → boolean
      Does the range overlap the multirange?
      int8range(3,7) && '{[4,12)}'::int8multirange → t
anymultirange << anymultirange → boolean
      Is the first multirange strictly left of the second?
       '{[1,10)}'::int8multirange << '{[100,110)}'::int8multirange
      → t
anymultirange << anyrange → boolean
      Is the multirange strictly left of the range?
       '{[1,10)}'::int8multirange << int8range(100,110) → t
anyrange << anymultirange → boolean
      Is the range strictly left of the multirange?
      int8range(1,10) << '{[100,110)}'::int8multirange → t
anymultirange >> anymultirange → boolean
      Is the first multirange strictly right of the second?
       '{[50,60)}'::int8multirange >> '{[20,30)}'::int8multirange
      → t
anymultirange >> anyrange → boolean
      Is the multirange strictly right of the range?
       '{[50,60)}'::int8multirange >> int8range(20,30) → t
anyrange >> anymultirange → boolean
      Is the range strictly right of the multirange?
      int8range(50,60) >> '{[20,30)}'::int8multirange → t
anymultirange &< anymultirange → boolean
      Does the first multirange not extend to the right of the second?
       '{[1,20)}'::int8multirange &< '{[18,20)}'::int8multirange →
      t
anymultirange &< anyrange → boolean
      Does the multirange not extend to the right of the range?
       '{[1,20)}'::int8multirange &< int8range(18,20) → t
anyrange &< anymultirange → boolean
      Does the range not extend to the right of the multirange?
      int8range(1,20) &< '{[18,20)}'::int8multirange → t
anymultirange &> anymultirange → boolean
```

```
Operator
      Description
      Example(s)
      Does the first multirange not extend to the left of the second?
       '{[7,20)}'::int8multirange &> '{[5,10)}'::int8multirange → t
anymultirange &> anyrange → boolean
      Does the multirange not extend to the left of the range?
       '{[7,20)}'::int8multirange &> int8range(5,10) → t
anyrange &> anymultirange → boolean
      Does the range not extend to the left of the multirange?
      int8range(7,20) &> '{[5,10)}'::int8multirange → t
anymultirange -|- anymultirange → boolean
      Are the multiranges adjacent?
       '{[1.1,2.2)}'::nummultirange -|- '{[2.2,3.3)}'::nummulti-
      range → t
anymultirange -|- anyrange → boolean
      Is the multirange adjacent to the range?
       '{[1.1,2.2)}'::nummultirange -|- numrange(2.2,3.3) → t
anyrange -|- anymultirange → boolean
      Is the range adjacent to the multirange?
      numrange(1.1,2.2) -|- '{[2.2,3.3)}'::nummultirange → t
anymultirange + anymultirange → anymultirange
      Computes the union of the multiranges. The multiranges need not overlap or be adjacent.
       '{[5,10)}'::nummultirange + '{[15,20)}'::nummultirange →
      {[5,10), [15,20)}
anymultirange * anymultirange → anymultirange
      Computes the intersection of the multiranges.
       '{[5,15)}'::int8multirange * '{[10,20)}'::int8multirange →
      {[10,15)}
anymultirange - anymultirange → anymultirange
      Computes the difference of the multiranges.
       '{[5,20)}'::int8multirange - '{[10,15)}'::int8multirange →
      {[5,10), [15,20)}
```

The left-of/right-of/adjacent operators always return false when an empty range or multirange is involved; that is, an empty range is not considered to be either before or after any other range.

Elsewhere empty ranges and multiranges are treated as the additive identity: anything unioned with an empty value is itself. Anything minus an empty value is itself. An empty multirange has exactly the same points as an empty range. Every range contains the empty range. Every multirange contains as many empty ranges as you like.

The range union and difference operators will fail if the resulting range would need to contain two disjoint sub-ranges, as such a range cannot be represented. There are separate operators for union and difference that take multirange parameters and return a multirange, and they do not fail even if their arguments are disjoint. So if you need a union or difference operation for ranges that may be disjoint, you can avoid errors by first casting your ranges to multiranges.

[Table 9.56](#page-187-0) shows the functions available for use with range types. [Table 9.57](#page-187-1) shows the functions available for use with multirange types.

#### <span id="page-187-0"></span>**Table 9.56. Range Functions**

```
Function
       Description
       Example(s)
lower ( anyrange ) → anyelement
       Extracts the lower bound of the range (NULL if the range is empty or the lower bound is
       infinite).
       lower(numrange(1.1,2.2)) → 1.1
upper ( anyrange ) → anyelement
       Extracts the upper bound of the range (NULL if the range is empty or the upper bound is
       infinite).
       upper(numrange(1.1,2.2)) → 2.2
isempty ( anyrange ) → boolean
       Is the range empty?
       isempty(numrange(1.1,2.2)) → f
lower_inc ( anyrange ) → boolean
       Is the range's lower bound inclusive?
       lower_inc(numrange(1.1,2.2)) → t
upper_inc ( anyrange ) → boolean
       Is the range's upper bound inclusive?
       upper_inc(numrange(1.1,2.2)) → f
lower_inf ( anyrange ) → boolean
       Is the range's lower bound infinite?
       lower_inf('(,)'::daterange) → t
upper_inf ( anyrange ) → boolean
       Is the range's upper bound infinite?
       upper_inf('(,)'::daterange) → t
range_merge ( anyrange, anyrange ) → anyrange
       Computes the smallest range that includes both of the given ranges.
       range_merge('[1,2)'::int4range, '[3,4)'::int4range) → [1,4)
```

### <span id="page-187-1"></span>**Table 9.57. Multirange Functions**

```
Function
       Description
       Example(s)
lower ( anymultirange ) → anyelement
       Extracts the lower bound of the multirange (NULL if the multirange is empty or the lower
       bound is infinite).
       lower('{[1.1,2.2)}'::nummultirange) → 1.1
upper ( anymultirange ) → anyelement
       Extracts the upper bound of the multirange (NULL if the multirange is empty or the upper
       bound is infinite).
       upper('{[1.1,2.2)}'::nummultirange) → 2.2
isempty ( anymultirange ) → boolean
       Is the multirange empty?
```

```
Function
       Description
       Example(s)
       isempty('{[1.1,2.2)}'::nummultirange) → f
lower_inc ( anymultirange ) → boolean
       Is the multirange's lower bound inclusive?
       lower_inc('{[1.1,2.2)}'::nummultirange) → t
upper_inc ( anymultirange ) → boolean
       Is the multirange's upper bound inclusive?
       upper_inc('{[1.1,2.2)}'::nummultirange) → f
lower_inf ( anymultirange ) → boolean
       Is the multirange's lower bound infinite?
       lower_inf('{(,)}'::datemultirange) → t
upper_inf ( anymultirange ) → boolean
       Is the multirange's upper bound infinite?
       upper_inf('{(,)}'::datemultirange) → t
range_merge ( anymultirange ) → anyrange
       Computes the smallest range that includes the entire multirange.
       range_merge('{[1,2), [3,4)}'::int4multirange) → [1,4)
multirange ( anyrange ) → anymultirange
       Returns a multirange containing just the given range.
       multirange('[1,2)'::int4range) → {[1,2)}
unnest ( anymultirange ) → setof anyrange
       Expands a multirange into a set of ranges. The ranges are read out in storage order (as-
       cending).
       unnest('{[1,2), [3,4)}'::int4multirange) →
        [1,2)
        [3,4)
```

The lower\_inc, upper\_inc, lower\_inf, and upper\_inf functions all return false for an empty range or multirange.

# <span id="page-188-0"></span>**9.21. Aggregate Functions**

*Aggregate functions* compute a single result from a set of input values. The built-in general-purpose aggregate functions are listed in [Table 9.58](#page-189-0) while statistical aggregates are in [Table 9.59](#page-191-0). The built-in within-group ordered-set aggregate functions are listed in [Table 9.60](#page-193-0) while the built-in within-group hypothetical-set ones are in [Table 9.61.](#page-194-0) Grouping operations, which are closely related to aggregate functions, are listed in [Table 9.62.](#page-194-1) The special syntax considerations for aggregate functions are explained in Section 4.2.7. Consult Section 2.7 for additional introductory information.

Aggregate functions that support *Partial Mode* are eligible to participate in various optimizations, such as parallel aggregation.

**Table 9.58. General-Purpose Aggregate Functions**

<span id="page-189-0"></span>

| Function<br>Description                                                                                                                                                                            | Partial<br>Mode |  |  |
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------|--|--|
| array_agg ( anynonarray ) → anyarray<br>Collects all the input values, including nulls, into an array.                                                                                             |                 |  |  |
| array_agg ( anyarray ) → anyarray<br>Concatenates all the input arrays into an array of one higher dimension. (The in<br>puts must all have the same dimensionality, and cannot be empty or null.) |                 |  |  |
| avg ( smallint ) → numeric                                                                                                                                                                         | Yes             |  |  |
| avg ( integer ) → numeric                                                                                                                                                                          |                 |  |  |
| avg ( bigint ) → numeric                                                                                                                                                                           |                 |  |  |
| avg ( numeric ) → numeric                                                                                                                                                                          |                 |  |  |
| avg ( real ) → double precision                                                                                                                                                                    |                 |  |  |
| avg ( double precision ) → double precision                                                                                                                                                        |                 |  |  |
| avg ( interval ) → interval                                                                                                                                                                        |                 |  |  |
| Computes the average (arithmetic mean) of all the non-null input values.                                                                                                                           |                 |  |  |
| bit_and ( smallint ) → smallint                                                                                                                                                                    | Yes             |  |  |
| bit_and ( integer ) → integer                                                                                                                                                                      |                 |  |  |
| bit_and ( bigint ) → bigint                                                                                                                                                                        |                 |  |  |
| bit_and ( bit ) → bit                                                                                                                                                                              |                 |  |  |
| Computes the bitwise AND of all non-null input values.                                                                                                                                             |                 |  |  |
| bit_or ( smallint ) → smallint                                                                                                                                                                     | Yes             |  |  |
| bit_or ( integer ) → integer                                                                                                                                                                       |                 |  |  |
| bit_or ( bigint ) → bigint                                                                                                                                                                         |                 |  |  |
| bit_or ( bit ) → bit<br>Computes the bitwise OR of all non-null input values.                                                                                                                      |                 |  |  |
| bit_xor ( smallint ) → smallint                                                                                                                                                                    | Yes             |  |  |
| bit_xor ( integer ) → integer                                                                                                                                                                      |                 |  |  |
| bit_xor ( bigint ) → bigint                                                                                                                                                                        |                 |  |  |
| bit_xor ( bit ) → bit<br>Computes the bitwise exclusive OR of all non-null input values. Can be useful<br>as a checksum for an unordered set of values.                                            |                 |  |  |
| bool_and ( boolean ) → boolean<br>Returns true if all non-null input values are true, otherwise false.                                                                                             | Yes             |  |  |
| bool_or ( boolean ) → boolean<br>Returns true if any non-null input value is true, otherwise false.                                                                                                | Yes             |  |  |
| count ( * ) → bigint<br>Computes the number of input rows.                                                                                                                                         | Yes             |  |  |
| count ( "any" ) → bigint<br>Computes the number of input rows in which the input value is not null.                                                                                                | Yes             |  |  |
| every ( boolean ) → boolean<br>This is the SQL standard's equivalent to bool_and.                                                                                                                  | Yes             |  |  |
| json_agg ( anyelement ) → json                                                                                                                                                                     | No              |  |  |

| Function<br>Description                                                                                                                                                                                                                                    | Partial<br>Mode |  |  |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------|--|--|
| jsonb_agg ( anyelement ) → jsonb<br>Collects all the input values, including nulls, into a JSON array. Values are con<br>verted to JSON as per to_json or to_jsonb.                                                                                        |                 |  |  |
| json_object_agg ( key "any", value "any" ) → json                                                                                                                                                                                                          | No              |  |  |
| jsonb_object_agg ( key "any", value "any" ) → jsonb<br>Collects all the key/value pairs into a JSON object. Key arguments are coerced<br>to text; value arguments are converted as per to_json or to_jsonb. Values<br>can be null, but not keys.           |                 |  |  |
| max ( see text ) → same as input type<br>Computes the maximum of the non-null input values. Available for any numer<br>ic, string, date/time, or enum type, as well as inet, interval, money, oid,<br>pg_lsn, tid, xid8, and arrays of any of these types. | Yes             |  |  |
| min ( see text ) → same as input type<br>Computes the minimum of the non-null input values. Available for any numer<br>ic, string, date/time, or enum type, as well as inet, interval, money, oid,<br>pg_lsn, tid, xid8, and arrays of any of these types. |                 |  |  |
| range_agg ( value anyrange ) → anymultirange                                                                                                                                                                                                               | No              |  |  |
| range_agg ( value anymultirange ) → anymultirange<br>Computes the union of the non-null input values.                                                                                                                                                      |                 |  |  |
| range_intersect_agg ( value anyrange ) → anyrange                                                                                                                                                                                                          | No              |  |  |
| range_intersect_agg ( value anymultirange ) → anymultirange<br>Computes the intersection of the non-null input values.                                                                                                                                     |                 |  |  |
| string_agg ( value text, delimiter text ) → text                                                                                                                                                                                                           | No              |  |  |
| string_agg ( value bytea, delimiter bytea ) → bytea<br>Concatenates the non-null input values into a string. Each value after the first is<br>preceded by the corresponding delimiter (if it's not null).                                                  |                 |  |  |
| sum ( smallint ) → bigint                                                                                                                                                                                                                                  | Yes             |  |  |
| sum ( integer ) → bigint                                                                                                                                                                                                                                   |                 |  |  |
| sum ( bigint ) → numeric                                                                                                                                                                                                                                   |                 |  |  |
| sum ( numeric ) → numeric                                                                                                                                                                                                                                  |                 |  |  |
| sum ( real ) → real                                                                                                                                                                                                                                        |                 |  |  |
| sum ( double precision ) → double precision                                                                                                                                                                                                                |                 |  |  |
| sum ( interval ) → interval                                                                                                                                                                                                                                |                 |  |  |
| sum ( money ) → money<br>Computes the sum of the non-null input values.                                                                                                                                                                                    |                 |  |  |
| xmlagg ( xml ) → xml<br>Concatenates the non-null XML input values (see Section 9.15.1.7).                                                                                                                                                                 | No              |  |  |

It should be noted that except for count, these functions return a null value when no rows are selected. In particular, sum of no rows returns null, not zero as one might expect, and array\_agg returns null rather than an empty array when there are no input rows. The coalesce function can be used to substitute zero or an empty array for null when necessary.

The aggregate functions array\_agg, json\_agg, jsonb\_agg, json\_object\_agg, jsonb\_object\_agg, string\_agg, and xmlagg, as well as similar user-defined aggregate functions, produce meaningfully different result values depending on the order of the input values. This ordering is unspecified by default, but can be controlled by writing an ORDER BY clause within the aggregate call, as shown in Section 4.2.7. Alternatively, supplying the input values from a sorted subquery will usually work. For example:

```
SELECT xmlagg(x) FROM (SELECT x FROM test ORDER BY y DESC) AS tab;
```

Beware that this approach can fail if the outer query level contains additional processing, such as a join, because that might cause the subquery's output to be reordered before the aggregate is computed.

### **Note**

The boolean aggregates bool\_and and bool\_or correspond to the standard SQL aggregates every and any or some. PostgreSQL supports every, but not any or some, because there is an ambiguity built into the standard syntax:

```
SELECT b1 = ANY((SELECT b2 FROM t2 ...)) FROM t1 ...;
```

Here ANY can be considered either as introducing a subquery, or as being an aggregate function, if the subquery returns one row with a Boolean value. Thus the standard name cannot be given to these aggregates.

### **Note**

Users accustomed to working with other SQL database management systems might be disappointed by the performance of the count aggregate when it is applied to the entire table. A query like:

```
SELECT count(*) FROM sometable;
```

will require effort proportional to the size of the table: PostgreSQL will need to scan either the entire table or the entirety of an index that includes all rows in the table.

[Table 9.59](#page-191-0) shows aggregate functions typically used in statistical analysis. (These are separated out merely to avoid cluttering the listing of more-commonly-used aggregates.) Functions shown as accepting numeric\_type are available for all the types smallint, integer, bigint, numeric, real, and double precision. Where the description mentions N, it means the number of input rows for which all the input expressions are non-null. In all cases, null is returned if the computation is meaningless, for example when N is zero.

<span id="page-191-0"></span>**Table 9.59. Aggregate Functions for Statistics**

| Function<br>Description                                                                                           | Partial<br>Mode |
|-------------------------------------------------------------------------------------------------------------------|-----------------|
| corr ( Y double precision, X double precision ) → double preci<br>sion                                            | Yes             |
| Computes the correlation coefficient.                                                                             |                 |
| covar_pop ( Y double precision, X double precision ) → double<br>precision<br>Computes the population covariance. | Yes             |
| covar_samp ( Y double precision, X double precision ) → double<br>precision                                       | Yes             |

| Function<br>Description                                                                                                                                                                  | Partial<br>Mode |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------|
| Computes the sample covariance.                                                                                                                                                          |                 |
| regr_avgx ( Y double precision, X double precision ) → double<br>precision<br>Computes the average of the independent variable, sum(X)/N.                                                | Yes             |
| regr_avgy ( Y double precision, X double precision ) → double<br>precision<br>Computes the average of the dependent variable, sum(Y)/N.                                                  | Yes             |
| regr_count ( Y double precision, X double precision ) → bigint<br>Computes the number of rows in which both inputs are non-null.                                                         | Yes             |
| regr_intercept ( Y double precision, X double precision ) → dou<br>ble precision<br>Computes the y-intercept of the least-squares-fit linear equation determined by<br>the (X, Y) pairs. | Yes             |
| regr_r2 ( Y double precision, X double precision ) → double pre<br>cision                                                                                                                | Yes             |
| Computes the square of the correlation coefficient.                                                                                                                                      |                 |
| regr_slope ( Y double precision, X double precision ) → double<br>precision<br>Computes the slope of the least-squares-fit linear equation determined by the (X,<br>Y) pairs.            | Yes             |
| regr_sxx ( Y double precision, X double precision ) → double<br>precision<br>Computes the "sum of squares" of the independent variable, sum(X^2) -<br>sum(X)^2/N.                        | Yes             |
| regr_sxy ( Y double precision, X double precision ) → double<br>precision<br>Computes the "sum of products" of independent times dependent variables,<br>sum(X*Y) - sum(X) * sum(Y)/N.   | Yes             |
| regr_syy ( Y double precision, X double precision ) → double<br>precision<br>Computes the "sum of squares" of the dependent variable, sum(Y^2) -<br>sum(Y)^2/N.                          | Yes             |
| stddev ( numeric_type ) → double precision for real or double<br>precision, otherwise numeric<br>This is a historical alias for stddev_samp.                                             | Yes             |
| stddev_pop ( numeric_type ) → double precision for real or double<br>precision, otherwise numeric<br>Computes the population standard deviation of the input values.                     | Yes             |
| stddev_samp ( numeric_type ) → double precision for real or dou<br>ble precision, otherwise numeric<br>Computes the sample standard deviation of the input values.                       | Yes             |
| variance ( numeric_type ) → double precision for real or double<br>precision, otherwise numeric<br>This is a historical alias for var_samp.                                              | Yes             |

| Function<br>Description                                                                                                                                                                                  | Partial<br>Mode |
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------|
| var_pop ( numeric_type ) → double precision for real or double<br>precision, otherwise numeric<br>Computes the population variance of the input values (square of the population<br>standard deviation). | Yes             |
| var_samp ( numeric_type ) → double precision for real or double<br>precision, otherwise numeric<br>Computes the sample variance of the input values (square of the sample stan<br>dard deviation).       | Yes             |

[Table 9.60](#page-193-0) shows some aggregate functions that use the *ordered-set aggregate* syntax. These functions are sometimes referred to as "inverse distribution" functions. Their aggregated input is introduced by ORDER BY, and they may also take a *direct argument* that is not aggregated, but is computed only once. All these functions ignore null values in their aggregated input. For those that take a fraction parameter, the fraction value must be between 0 and 1; an error is thrown if not. However, a null fraction value simply produces a null result.

<span id="page-193-0"></span>**Table 9.60. Ordered-Set Aggregate Functions**

| Function<br>Description                                                                                                                                                                                                                                                                                                                                                                                                                                             | Partial<br>Mode |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------|
| mode () WITHIN GROUP ( ORDER BY anyelement ) → anyelement<br>Computes the mode, the most frequent value of the aggregated argument (arbi<br>trarily choosing the first one if there are multiple equally-frequent values). The<br>aggregated argument must be of a sortable type.                                                                                                                                                                                   | No              |
| percentile_cont ( fraction double precision ) WITHIN GROUP ( OR<br>DER BY double precision ) → double precision<br>percentile_cont ( fraction double precision ) WITHIN GROUP ( OR<br>DER BY interval ) → interval<br>Computes the continuous percentile, a value corresponding to the specified<br>fraction within the ordered set of aggregated argument values. This will in<br>terpolate between adjacent input items if needed.                                | No              |
| percentile_cont ( fractions double precision[] ) WITHIN GROUP (<br>ORDER BY double precision ) → double precision[]<br>percentile_cont ( fractions double precision[] ) WITHIN GROUP (<br>ORDER BY interval ) → interval[]<br>Computes multiple continuous percentiles. The result is an array of the same di<br>mensions as the fractions parameter, with each non-null element replaced<br>by the (possibly interpolated) value corresponding to that percentile. | No              |
| percentile_disc ( fraction double precision ) WITHIN GROUP ( OR<br>DER BY anyelement ) → anyelement<br>Computes the discrete percentile, the first value within the ordered set of ag<br>gregated argument values whose position in the ordering equals or exceeds the<br>specified fraction. The aggregated argument must be of a sortable type.                                                                                                                   | No              |
| percentile_disc ( fractions double precision[] ) WITHIN GROUP (<br>ORDER BY anyelement ) → anyarray<br>Computes multiple discrete percentiles. The result is an array of the same di<br>mensions as the fractions parameter, with each non-null element replaced<br>by the input value corresponding to that percentile. The aggregated argument<br>must be of a sortable type.                                                                                     | No              |

Each of the "hypothetical-set" aggregates listed in [Table 9.61](#page-194-0) is associated with a window function of the same name defined in [Section 9.22](#page-195-0). In each case, the aggregate's result is the value that the associated window function would have returned for the "hypothetical" row constructed from args, if such a row had been added to the sorted group of rows represented by the sorted\_args. For each of these functions, the list of direct arguments given in args must match the number and types of the aggregated arguments given in sorted\_args. Unlike most built-in aggregates, these aggregates are not strict, that is they do not drop input rows containing nulls. Null values sort according to the rule specified in the ORDER BY clause.

<span id="page-194-0"></span>**Table 9.61. Hypothetical-Set Aggregate Functions**

| Function<br>Description                                                                                                                                                                                                                           | Partial<br>Mode |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------|
| rank ( args ) WITHIN GROUP ( ORDER BY sorted_args ) → bigint<br>Computes the rank of the hypothetical row, with gaps; that is, the row number<br>of the first row in its peer group.                                                              | No              |
| dense_rank ( args ) WITHIN GROUP ( ORDER BY sorted_args ) → bigint<br>Computes the rank of the hypothetical row, without gaps; this function effec<br>tively counts peer groups.                                                                  | No              |
| percent_rank ( args ) WITHIN GROUP ( ORDER BY sorted_args ) → dou<br>ble precision<br>Computes the relative rank of the hypothetical row, that is (rank - 1) / (total<br>rows - 1). The value thus ranges from 0 to 1 inclusive.                  | No              |
| cume_dist ( args ) WITHIN GROUP ( ORDER BY sorted_args ) → double<br>precision<br>Computes the cumulative distribution, that is (number of rows preceding or<br>peers with hypothetical row) / (total rows). The value thus ranges from 1/N to 1. | No              |

### <span id="page-194-1"></span>**Table 9.62. Grouping Operations**

included.

### **Function Description** GROUPING ( group\_by\_expression(s) ) → integer Returns a bit mask indicating which GROUP BY expressions are not included in the current grouping set. Bits are assigned with the rightmost argument corresponding to the least-significant bit; each bit is 0 if the corresponding expression is included in the grouping criteria of the grouping set generating the current result row, and 1 if it is not

The grouping operations shown in [Table 9.62](#page-194-1) are used in conjunction with grouping sets (see Section 7.2.4) to distinguish result rows. The arguments to the GROUPING function are not actually evaluated, but they must exactly match expressions given in the GROUP BY clause of the associated query level. For example:

### => **SELECT \* FROM items\_sold;** make | model | sales -------+-------+------- Foo | GT | 10 Foo | Tour | 20 Bar | City | 15 Bar | Sport | 5 (4 rows)

=> **SELECT make, model, GROUPING(make,model), sum(sales) FROM items\_sold GROUP BY ROLLUP(make,model);**

| make     |  |       |  | model   grouping   sum |       |        |
|----------|--|-------|--|------------------------|-------|--------|
|          |  |       |  | +++                    |       |        |
| Foo      |  | GT    |  |                        |       | 0   10 |
| Foo      |  | Tour  |  |                        |       | 0   20 |
| Bar      |  | City  |  |                        |       | 0   15 |
| Bar      |  | Sport |  |                        | 0   5 |        |
| Foo      |  |       |  |                        |       | 1   30 |
| Bar      |  |       |  |                        |       | 1   20 |
|          |  |       |  |                        |       | 3   50 |
| (7 rows) |  |       |  |                        |       |        |

Here, the grouping value 0 in the first four rows shows that those have been grouped normally, over both the grouping columns. The value 1 indicates that model was not grouped by in the nextto-last two rows, and the value 3 indicates that neither make nor model was grouped by in the last row (which therefore is an aggregate over all the input rows).

# <span id="page-195-0"></span>**9.22. Window Functions**

*Window functions* provide the ability to perform calculations across sets of rows that are related to the current query row. See Section 3.5 for an introduction to this feature, and Section 4.2.8 for syntax details.

The built-in window functions are listed in [Table 9.63.](#page-195-1) Note that these functions *must* be invoked using window function syntax, i.e., an OVER clause is required.

In addition to these functions, any built-in or user-defined ordinary aggregate (i.e., not ordered-set or hypothetical-set aggregates) can be used as a window function; see [Section 9.21](#page-188-0) for a list of the builtin aggregates. Aggregate functions act as window functions only when an OVER clause follows the call; otherwise they act as plain aggregates and return a single row for the entire set.

<span id="page-195-1"></span>**Table 9.63. General-Purpose Window Functions**

| Function                                                                                                                                                                                                         |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Description                                                                                                                                                                                                      |
| row_number () → bigint<br>Returns the number of the current row within its partition, counting from 1.                                                                                                           |
| rank () → bigint<br>Returns the rank of the current row, with gaps; that is, the row_number of the first row<br>in its peer group.                                                                               |
| dense_rank () → bigint<br>Returns the rank of the current row, without gaps; this function effectively counts peer<br>groups.                                                                                    |
| percent_rank () → double precision<br>Returns the relative rank of the current row, that is (rank - 1) / (total partition rows - 1).<br>The value thus ranges from 0 to 1 inclusive.                             |
| cume_dist () → double precision<br>Returns the cumulative distribution, that is (number of partition rows preceding or peers<br>with current row) / (total partition rows). The value thus ranges from 1/N to 1. |
| ntile ( num_buckets integer ) → integer<br>Returns an integer ranging from 1 to the argument value, dividing the partition as equally<br>as possible.                                                            |

#### **Function**

#### **Description**

lag ( value anycompatible [, offset integer [, default anycompatible ]] ) → anycompatible

Returns value evaluated at the row that is offset rows before the current row within the partition; if there is no such row, instead returns default (which must be of a type compatible with value). Both offset and default are evaluated with respect to the current row. If omitted, offset defaults to 1 and default to NULL.

lead ( value anycompatible [, offset integer [, default anycompatible ]] ) → anycompatible

Returns value evaluated at the row that is offset rows after the current row within the partition; if there is no such row, instead returns default (which must be of a type compatible with value). Both offset and default are evaluated with respect to the current row. If omitted, offset defaults to 1 and default to NULL.

first\_value ( value anyelement ) → anyelement

Returns value evaluated at the row that is the first row of the window frame.

last\_value ( value anyelement ) → anyelement

Returns value evaluated at the row that is the last row of the window frame.

nth\_value ( value anyelement, n integer ) → anyelement

Returns value evaluated at the row that is the n'th row of the window frame (counting from 1); returns NULL if there is no such row.

All of the functions listed in [Table 9.63](#page-195-1) depend on the sort ordering specified by the ORDER BY clause of the associated window definition. Rows that are not distinct when considering only the ORDER BY columns are said to be *peers*. The four ranking functions (including cume\_dist) are defined so that they give the same answer for all rows of a peer group.

Note that first\_value, last\_value, and nth\_value consider only the rows within the "window frame", which by default contains the rows from the start of the partition through the last peer of the current row. This is likely to give unhelpful results for last\_value and sometimes also nth\_value. You can redefine the frame by adding a suitable frame specification (RANGE, ROWS or GROUPS) to the OVER clause. See Section 4.2.8 for more information about frame specifications.

When an aggregate function is used as a window function, it aggregates over the rows within the current row's window frame. An aggregate used with ORDER BY and the default window frame definition produces a "running sum" type of behavior, which may or may not be what's wanted. To obtain aggregation over the whole partition, omit ORDER BY or use ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING. Other frame specifications can be used to obtain other effects.

### **Note**

The SQL standard defines a RESPECT NULLS or IGNORE NULLS option for lead, lag, first\_value, last\_value, and nth\_value. This is not implemented in PostgreSQL: the behavior is always the same as the standard's default, namely RESPECT NULLS. Likewise, the standard's FROM FIRST or FROM LAST option for nth\_value is not implemented: only the default FROM FIRST behavior is supported. (You can achieve the result of FROM LAST by reversing the ORDER BY ordering.)