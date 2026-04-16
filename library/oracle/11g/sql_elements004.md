# Oracle 11g - sql_elements004
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/sql_elements004.htm

A modifier can appear in a format model more than once. In such a case, each subsequent occurrence toggles the effects of the modifier. Its effects are enabled for the portion of the model following its first occurrence, and then disabled for the portion following its second, and then reenabled for the portion following its third, and so on.

If any portion of the character argument violates any of these conditions, then Oracle returns an error message.

### Format Model Examples

The following statement uses a date format model to return a character expression:

```
SELECT TO_CHAR(SYSDATE, 'fmDDTH') || ' of ' ||
       TO_CHAR(SYSDATE, 'fmMonth') || ', ' ||
       TO_CHAR(SYSDATE, 'YYYY') "Ides" 
  FROM DUAL; 

Ides 
------------------ 
3RD of April, 2008
```

The preceding statement also uses the `FM` modifier. If `FM` is omitted, then the month is blank-padded to nine characters:

```
SELECT TO_CHAR(SYSDATE, 'DDTH') || ' of ' ||
   TO_CHAR(SYSDATE, 'Month') || ', ' ||
   TO_CHAR(SYSDATE, 'YYYY') "Ides"
  FROM DUAL; 

Ides 
----------------------- 
03RD of April    , 2008
```

The following statement places a single quotation mark in the return value by using a date format model that includes two consecutive single quotation marks:

```
SELECT TO_CHAR(SYSDATE, 'fmDay') || '''s Special' "Menu"
  FROM DUAL; 

Menu 
----------------- 
Tuesday's Special
```

Two consecutive single quotation marks can be used for the same purpose within a character literal in a format model.

[Table 3-17](#g195443) shows whether the following statement meets the matching conditions for different values of `char` and '`fmt`' using `FX` (the table named `table` has a column `date_column` of data type `DATE`):

```
UPDATE table 
  SET date_column = TO_DATE(char, 'fmt');
```

Table 3-17 Matching Character Data and Format Models with the FX Format Model Modifier

| char | 'fmt' | Match or Error? |
| --- | --- | --- |
| `'15/ JAN /1998'` | `'DD-MON-YYYY'` | `Match` |
| `' 15! JAN % /1998'` | `'DD-MON-YYYY'` | `Error` |
| `'15/JAN/1998'` | `'FXDD-MON-YYYY'` | `Error` |
| `'15-JAN-1998'` | `'FXDD-MON-YYYY'` | `Match` |
| `'1-JAN-1998'` | `'FXDD-MON-YYYY'` | `Error` |
| `'01-JAN-1998'` | `'FXDD-MON-YYYY'` | `Match` |
| `'1-JAN-1998'` | `'FXFMDD-MON-YYYY'` | `Match` |

Format of Return Values: Examples You can use a format model to specify the format for Oracle to use to return values from the database to you.

The following statement selects the salaries of the employees in Department 80 and uses the `TO_CHAR` function to convert these salaries into character values with the format specified by the number format model '`$99,990.99`':

```
SELECT last_name employee, TO_CHAR(salary, '$99,990.99')
  FROM employees
  WHERE department_id = 80;
```

Because of this format model, Oracle returns salaries with leading dollar signs, commas every three digits, and two decimal places.

The following statement selects the date on which each employee from Department 20 was hired and uses the `TO_CHAR` function to convert these dates to character strings with the format specified by the date format model '`fmMonth` `DD,` `YYYY`':

```
SELECT last_name employee, TO_CHAR(hire_date,'fmMonth DD, YYYY') hiredate
  FROM employees
  WHERE department_id = 20;
```

With this format model, Oracle returns the hire dates without blank padding (as specified by `fm`), two digits for the day, and the century included in the year.

Supplying the Correct Format Model: Examples When you insert or update a column value, the data type of the value that you specify must correspond to the column data type of the column. You can use format models to specify the format of a value that you are converting from one data type to another data type required for a column.

For example, a value that you insert into a `DATE` column must be a value of the `DATE` data type or a character string in the default date format (Oracle implicitly converts character strings in the default date format to the `DATE` data type). If the value is in another format, then you must use the `TO_DATE` function to convert the value to the `DATE` data type. You must also use a format model to specify the format of the character string.

The following statement updates `Hunold's` hire date using the `TO_DATE` function with the format mask 'YYYY MM DD' to convert the character string '2008 05 20' to a `DATE` value:

```
UPDATE employees 
  SET hire_date = TO_DATE('2008 05 20','YYYY MM DD') 
  WHERE last_name = 'Hunold';
```