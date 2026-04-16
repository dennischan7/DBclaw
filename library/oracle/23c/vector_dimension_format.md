# Oracle 23c - vector_dimension_format
Source: https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/vector_dimension_format.html

Parameters

`expr` must evaluate to a vector.

If `expr` is NULL, NULL is returned.

Examples

```
SELECT VECTOR_DIMENSION_FORMAT(TO_VECTOR('[34.6, 77.8]', 2, FLOAT64));

VECTOR_DIMENSION_FORMAT(TO_VECTOR('[34.6,77.8]',2,
--------------------------------------------------
FLOAT64

SELECT VECTOR_DIMENSION_FORMAT(TO_VECTOR('[34.6, 77.8, 9]', 3, FLOAT32));

VECTOR_DIMENSION_FORMAT(TO_VECTOR('[34.6,77.8,9]',
--------------------------------------------------
FLOAT32

SELECT VECTOR_DIMENSION_FORMAT(TO_VECTOR('[34.6, 77.8, 9.10]', 3, INT8));

VECTOR_DIMENSION_FORMAT(TO_VECTOR('[34.6,77.8,9.10
--------------------------------------------------
INT8

SELECT VECTOR_DIMENSION_FORMAT(TO_VECTOR('[206, 32]', 16, BINARY));

VECTOR_DIMENSION_FORMAT(TO_VECTOR('[206,32]',16,BI
--------------------------------------------------
BINARY

SELECT VECTOR_DIMENSION_FORMAT(TO_VECTOR('[34.6, 77.8, 9, 10]', 3, INT8));

SELECT VECTOR_DIMENSION_FORMAT(TO_VECTOR('[34.6, 77.8, 9, 10]', 3, INT8))
                               *
ERROR at line 1:
ORA-51803: Vector dimension count must match the dimension count specified in
the column definition (expected 3 dimensions, specified 4 dimensions).
```