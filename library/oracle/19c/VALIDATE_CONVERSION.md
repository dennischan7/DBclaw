# Oracle 19c - VALIDATE_CONVERSION
Source: https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/VALIDATE_CONVERSION.html

* `BINARY_DOUBLE`

  If you specify `BINARY_DOUBLE`, then `expr` can be any expression that evaluates to a character string of `CHAR`, `VARCHAR2`, `NCHAR`, or `NVARCHAR2` data type, or a numeric value of type `NUMBER`, `BINARY_FLOAT`, or `BINARY_DOUBLE`. The optional `fmt` and `nlsparam` arguments serve the same purpose as for the `TO_BINARY_DOUBLE` function. Refer to [TO\_BINARY\_DOUBLE](TO_BINARY_DOUBLE.md#GUID-0BA2E065-8006-426C-A3CB-1F6B0C8F283C) for more information.
* `BINARY_FLOAT`

  If you specify `BINARY_FLOAT`, then `expr` can be any expression that evaluates to a character string of `CHAR`, `VARCHAR2`, `NCHAR`, or `NVARCHAR2` data type, or a numeric value of type `NUMBER`, `BINARY_FLOAT`, or `BINARY_DOUBLE`. The optional `fmt` and `nlsparam` arguments serve the same purpose as for the `TO_BINARY_FLOAT` function. Refer to [TO\_BINARY\_FLOAT](TO_BINARY_FLOAT.md#GUID-66A51BE2-BE4A-4B99-9C37-73B110452D27) for more information.
* `DATE`

  If you specify `DATE`, then `expr` can be any expression that evaluates to a character string of `CHAR`, `VARCHAR2`, `NCHAR`, or `NVARCHAR2` data type. The optional `fmt` and `nlsparam` arguments serve the same purpose as for the `TO_DATE` function. Refer to [TO\_DATE](TO_DATE.md#GUID-D226FA7C-F7AD-41A0-BB1D-BD8EF9440118) for more information.
* `INTERVAL` `DAY` `TO` `SECOND`

  If you specify `INTERVAL` `DAY` `TO` `SECOND`, then `expr` can be any expression that evaluates to a character string of `CHAR`, `VARCHAR2`, `NCHAR`, or `NVARCHAR2` data type, and must contain a value in either the SQL interval format or the ISO duration format. The optional `fmt` and `nlsparam` arguments do not apply for this data type. Refer to [TO\_DSINTERVAL](TO_DSINTERVAL.md#GUID-DEBB41BD-9438-4558-A53E-428CE93C05D3) for more information on the SQL interval format and the ISO duration format.
* `INTERVAL` `YEAR` `TO` `MONTH`

  If you specify `INTERVAL` `YEAR` `TO` `MONTH`, then `expr` can be any expression that evaluates to a character string of `CHAR`, `VARCHAR2`, `NCHAR`, or `NVARCHAR2` data type, and must contain a value in either the SQL interval format or the ISO duration format. The optional `fmt` and `nlsparam` arguments do not apply for this data type. Refer to [TO\_YMINTERVAL](TO_YMINTERVAL.md#GUID-5DEBA096-7AC3-4B18-A4BE-D36FC9BDB450) for more information on the SQL interval format and the ISO duration format.
* `NUMBER`

  If you specify `NUMBER`, then `expr` can be any expression that evaluates to a character string of `CHAR`, `VARCHAR2`, `NCHAR`, or `NVARCHAR2` data type, or a numeric value of type `NUMBER`, `BINARY_FLOAT`, or `BINARY_DOUBLE`. The optional `fmt` and `nlsparam` arguments serve the same purpose as for the `TO_NUMBER` function. Refer to [TO\_NUMBER](TO_NUMBER.md#GUID-D4807212-AFD7-48A7-9AED-BEC3E8809866) for more information.

  If `expr` is a value of type `NUMBER`, then the `VALIDATE_CONVERSION` function verifies that `expr` is a legal numeric value. If `expr` is not a legal numeric value, then the function returns 0. This enables you to identify corrupt numeric values in your database.
* `TIMESTAMP`

  If you specify `TIMESTAMP`, then `expr` can be any expression that evaluates to a character string of `CHAR`, `VARCHAR2`, `NCHAR`, or `NVARCHAR2` data type. The optional `fmt` and `nlsparam` arguments serve the same purpose as for the `TO_TIMESTAMP` function. If you omit `fmt`, then `expr` must be in the default format of the `TIMESTAMP` data type, which is determined by the `NLS_TIMESTAMP_FORMAT` initialization parameter. Refer to [TO\_TIMESTAMP](TO_TIMESTAMP.md#GUID-57E09334-E3CC-4CA2-809E-F0909458BCFA) for more information.
* `TIMESTAMP` `WITH` `TIME` `ZONE`

  If you specify `TIMESTAMP` `WITH` `TIME` `ZONE`, then `expr` can be any expression that evaluates to a character string of `CHAR`, `VARCHAR2`, `NCHAR`, or `NVARCHAR2` data type. The optional `fmt` and `nlsparam` arguments serve the same purpose as for the `TO_TIMESTAMP_TZ` function. If you omit `fmt`, then `expr` must be in the default format of the `TIMESTAMP` `WITH` `TIME` `ZONE` data type, which is determined by the `NLS_TIMESTAMP_TZ_FORMAT` initialization parameter. Refer to [TO\_TIMESTAMP\_TZ](TO_TIMESTAMP_TZ.md#GUID-3999303B-89CA-4AA3-9817-458F36ADC9DC) for more information.
* `TIMESTAMP` `WITH` `LOCAL` `TIME` `ZONE`

  If you specify `TIMESTAMP`, then `expr` can be any expression that evaluates to a character string of `CHAR`, `VARCHAR2`, `NCHAR`, or `NVARCHAR2` data type. The optional `fmt` and `nlsparam` arguments serve the same purpose as for the `TO_TIMESTAMP` function. If you omit `fmt`, then `expr` must be in the default format of the `TIMESTAMP` data type, which is determined by the `NLS_TIMESTAMP_FORMAT` initialization parameter. Refer to [TO\_TIMESTAMP](TO_TIMESTAMP.md#GUID-57E09334-E3CC-4CA2-809E-F0909458BCFA) for more information.