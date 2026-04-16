# Oracle 23c - from_vector
Source: https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/from_vector.html

Purpose

`FROM_VECTOR` optionally takes a `RETURNING` clause to
specify the data type of the returned value.

If `VARCHAR2` is specified without size, the size of the returned
value size is 32767.

You can optionally specify the text format of the output in the
`FORMAT` clause, using the tokens `SPARSE` or
`DENSE`. Note that the input vector storage format does not need
to match the specified output format.

There is no support to convert to `CHAR`, `NCHAR`, and `NVARCHAR2`.

`FROM_VECTOR` is synonymous with `VECTOR_SERIALIZE`.

Examples

```
SELECT FROM_VECTOR(TO_VECTOR('[1, 2, 3]') );

FROM_VECTOR(TO_VECTOR('[1,2,3]'))
–---------------------------------------------------------------
[1.0E+000,2.0E+000,3.0E+000] 

1 row selected.
```

```
SELECT FROM_VECTOR(TO_VECTOR('[1.1, 2.2, 3.3]', 3, FLOAT32) );

FROM_VECTOR(TO_VECTOR('[1.1,2.2,3.3]',3,FLOAT32))
------------------------------------------------------------------
[1.10000002E+000,2.20000005E+000,3.29999995E+000] 

1 row selected.
```

```
SELECT FROM_VECTOR( TO_VECTOR('[1.1, 2.2, 3.3]', 3, FLOAT32) RETURNING VARCHAR2(1000));

FROM_VECTOR(TO_VECTOR('[1.1,2.2,3.3]',3,FLOAT32)RETURNINGVARCHAR2(1000))
--------------------------------------------------------------------------------
[1.10000002E+000,2.20000005E+000,3.29999995E+000] 

1 row selected.
```

```
SELECT FROM_VECTOR(TO_VECTOR('[1.1, 2.2, 3.3]', 3, FLOAT32) RETURNING CLOB );

FROM_VECTOR(TO_VECTOR('[1.1,2.2,3.3]',3,FLOAT32)RETURNINGCLOB)
--------------------------------------------------------------------------------
[1.10000002E+000,2.20000005E+000,3.29999995E+000] 

1 row selected.
```

```
SELECT FROM_VECTOR(TO_VECTOR('[5,[2,4],[1.0,2.0]]', 5, FLOAT64, SPARSE) RETURNING CLOB FORMAT SPARSE);

FROM_VECTOR(TO_VECTOR('[5,[2,4],[1.0,2.0]]',5,FLOAT64,SPARSE)RETURNINGCLOBFORMAT
--------------------------------------------------------------------------------
[5,[2,4],[1.0E+000,2.0E+000]]

1 row selected.
```

```
SELECT FROM_VECTOR(TO_VECTOR('[5,[2,4],[1.0,2.0]]', 5, FLOAT64, SPARSE) RETURNING CLOB FORMAT DENSE);

FROM_VECTOR(TO_VECTOR('[5,[2,4],[1.0,2.0]]',5,FLOAT64,SPARSE)RETURNINGCLOBFORMAT
--------------------------------------------------------------------------------
[0,1.0E+000,0,2.0E+000,0]

1 row selected.
```