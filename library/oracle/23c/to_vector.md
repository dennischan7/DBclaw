# Oracle 23c - to_vector
Source: https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/to_vector.html

Examples

```
SELECT TO_VECTOR('[34.6, 77.8]');

TO_VECTOR('[34.6,77.8]')
---------------------------------------------------------
[3.45999985E+001,7.78000031E+001]

SELECT TO_VECTOR('[34.6, 77.8]', 2, FLOAT32);

TO_VECTOR('[34.6,77.8]',2,FLOAT32)
---------------------------------------------------------
[3.45999985E+001,7.78000031E+001]

SELECT TO_VECTOR('[34.6, 77.8, -89.34]', 3, FLOAT32);

TO_VECTOR('[34.6,77.8,-89.34]',3,FLOAT32)
-----------------------------------------------------------
[3.45999985E+001,7.78000031E+001,-8.93399963E+001]

SELECT TO_VECTOR('[34.6, 77.8, -89.34]', 3, FLOAT32, DENSE);

TO_VECTOR('[34.6,77.8,-89.34]',3,FLOAT32,DENSE)
---------------------------------------------------------------------
[3.45999985E+001,7.78000031E+001,-8.93399963E+001]
```

Note:

* For applications using Oracle Client libraries prior to 26ai connected to Oracle Database 26ai, use the `TO_VECTOR` function to insert vector data. For example:

  ```
  INSERT INTO vecTab VALUES(TO_VECTOR('[1.1, 2.9, 3.14]'));
  ```
* Applications using Oracle Client 26ai libraries or Thin mode drivers can insert vector data directly as a string or a `CLOB`. For example:

  ```
  INSERT INTO vecTab VALUES ('[1.1, 2.9, 3.14]');
  ```