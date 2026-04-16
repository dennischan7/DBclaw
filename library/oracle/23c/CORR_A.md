# Oracle 23c - CORR_A
Source: https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/CORR_A.html

The `CORR` function (see [CORR](CORR.md#GUID-E73AF5E2-38A4-436A-955C-5122C079F49C)) calculates the Pearson's correlation coefficient and requires numeric expressions as input. The `CORR_`\* functions support nonparametric or rank correlation. They let you find correlations between expressions that are ordinal scaled (where a ranking of the values is possible). Correlation coefficients take on a value ranging from -1 to 1, where 1 indicates a perfect relationship, -1 a perfect inverse relationship (when one variable increases as the other decreases), and a value close to 0 means no relationship.

These functions take two mandatory arguments, `expr1` and `expr2`, and an optional third argument. The return value of the functions is a `NUMBER.`

The mandatory arguments are the two variables being analyzed. They can be of any data type that is comparable other than `LONG`, `CLOB`, `BLOB`, `BFILE`, or `VECTOR`. If the data type is a user-defined type (UDT), it must have a `MAP` or `ORDER` method to be comparable.

The third argument specifies the variant of the result returned by the functions. It is of type `VARCHAR2` and must be a constant expression, for example, a character literal. If you omit the third argument, then the default is `'COEFFICIENT'`. The allowed argument values and their meaning are shown in Table 7-2 [Table 7-5](CORR_A.md#GUID-B2DED35A-2ECE-4DF0-BDA4-28F28B7BCA23__GUID-AB5A91D9-9BA9-4F91-90A7-E0C457FDB889 "The first column lists the values you can specify for the return value of the function and the second column explains how each value is interpreted."):