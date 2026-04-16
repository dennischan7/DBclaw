# Oracle 21c - REGEXP_REPLACE
Source: https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/REGEXP_REPLACE.html

The following example examines `phone_number`, looking for the pattern `xxx`.`xxx`.`xxxx`. Oracle reformats this pattern with (`xxx`) `xxx`-`xxxx`.

```
SELECT
  REGEXP_REPLACE(phone_number,
                 '([[:digit:]]{3})\.([[:digit:]]{3})\.([[:digit:]]{4})',
                 '(\1) \2-\3') "REGEXP_REPLACE"
  FROM employees
  ORDER BY "REGEXP_REPLACE";

REGEXP_REPLACE
--------------------------------------------------------------------------------
(515) 123-4444
(515) 123-4567
(515) 123-4568
(515) 123-4569
(515) 123-5555
. . .
```

The following example examines `country_name`. Oracle puts a space after each non-null character in the string.

```
SELECT
  REGEXP_REPLACE(country_name, '(.)', '\1 ') "REGEXP_REPLACE"
  FROM countries;

REGEXP_REPLACE
--------------------------------------------------------------------------------
A r g e n t i n a
A u s t r a l i a
B e l g i u m
B r a z i l
C a n a d a
. . .
```

The following example examines the string, looking for two or more spaces. Oracle replaces each occurrence of two or more spaces with a single space.

```
SELECT
  REGEXP_REPLACE('500   Oracle     Parkway,    Redwood  Shores, CA',
                 '( ){2,}', ' ') "REGEXP_REPLACE"
  FROM DUAL;

REGEXP_REPLACE
--------------------------------------
500 Oracle Parkway, Redwood Shores, CA
```

REGEXP\_REPLACE pattern matching: Examples

The following statements create a table regexp\_temp and insert values into it:

```
CREATE TABLE regexp_temp(empName varchar2(20), emailID varchar2(20));

INSERT INTO regexp_temp (empName, emailID) VALUES ('John Doe', 'johndoe@example.com');
INSERT INTO regexp_temp (empName, emailID) VALUES ('Jane Doe', 'janedoe@example.com');
```

The following statement replaces the string âJaneâ with âJohnâ:

```
SELECT empName, REGEXP_REPLACE (empName, 'Jane', 'John') "STRING_REPLACE" FROM regexp_temp;

EMPNAME		STRING_REPLACE
--------	--------------
John Doe	John Doe
Jane Doe	John Doe
```

The following statement replaces the string âJohnâ with âJaneâ:

```
SELECT empName, REGEXP_REPLACE (empName, 'John', 'Jane' ) "STRING_REPLACE" FROM regexp_temp;

EMPNAME		STRING_REPLACE
--------	--------------
John Doe	Jane Doe
Jane Doe	Jane Doe
```

REGEXP\_REPLACE: Examples

The following statement replaces all the numbers in a string:

```
WITH strings AS (   
  SELECT 'abc123' s FROM dual union all   
  SELECT '123abc' s FROM dual union all   
  SELECT 'a1b2c3' s FROM dual   
)   
  SELECT s "STRING", regexp_replace(s, '[0-9]', '') "MODIFIED_STRING"  
  FROM strings;

  STRING               MODIFIED_STRING
-------------------- --------------------
abc123               abc
123abc               abc
a1b2c3               abc
```

The following statement replaces the first numeric occurrence in a string:

```
WITH strings AS (   
  SELECT 'abc123' s from DUAL union all   
  SELECT '123abc' s from DUAL union all   
  SELECT 'a1b2c3' s from DUAL   
)   
  SELECT s "STRING", REGEXP_REPLACE(s, '[0-9]', '', 1, 1) "MODIFIED_STRING"  
  FROM   strings;

 STRING               MODIFIED_STRING
-------------------- --------------------
abc123               abc23
123abc               23abc
a1b2c3               ab2c3
```

The following statement replaces the second numeric occurrence in a string:

```
WITH strings AS (   
  SELECT 'abc123' s from DUAL union all   
  SELECT '123abc' s from DUAL union all   
  SELECT 'a1b2c3' s from DUAL   
)   
  SELECT s "STRING", REGEXP_REPLACE(s, '[0-9]', '', 1, 2) "MODIFIED_STRING"  
  FROM   strings;

STRING               MODIFIED_STRING
-------------------- --------------------
abc123               abc13
123abc               13abc
a1b2c3               a1bc3
```

The following statement replaces multiple spaces in a string with a single space:

```
WITH strings AS (   
  SELECT 'Hello  World' s FROM dual union all   
  SELECT 'Hello        World' s FROM dual union all   
  SELECT 'Hello,   World  !' s FROM dual   
)   
  SELECT s "STRING", regexp_replace(s, ' {2,}', ' ') "MODIFIED_STRING"  
  FROM   strings;

 STRING               MODIFIED_STRING
-------------------- --------------------
Hello  World         Hello World
Hello        World   Hello World
Hello,   World  !    Hello, World !
```

The following statement converts camel case strings to a string containing lower case words separated by an underscore:

```
WITH strings as (   
  SELECT 'AddressLine1' s FROM dual union all   
  SELECT 'ZipCode' s FROM dual union all   
  SELECT 'Country' s FROM dual   
)   
  SELECT s "STRING",  
         lower(regexp_replace(s, '([A-Z0-9])', '_\1', 2)) "MODIFIED_STRING"  
  FROM strings;

  STRING               MODIFIED_STRING
-------------------- --------------------
AddressLine1         address_line_1
ZipCode              zip_code
Country              country
```

The following statement converts the format of a date:

```
WITH date_strings AS (   
  SELECT  '2015-01-01' d from dual union all   
  SELECT '2000-12-31' d from dual union all   
  SELECT '900-01-01' d from dual   
)   
  SELECT d "STRING",   
         regexp_replace(d, '([[:digit:]]+)-([[:digit:]]{2})-([[:digit:]]{2})', '\3.\2.\1') "MODIFIED_STRING"  
  FROM date_strings;

  STRING               MODIFIED_STRING
-------------------- --------------------
2015-01-01           01.01.2015
2000-12-31           31.12.2000
900-01-01            01.01.900
```

The following statement replaces all the letters in a string with â1â:

```
WITH strings as (   
  SELECT 'NEW YORK' s FROM dual union all   
  SELECT 'New York' s FROM dual union all   
  SELECT 'new york' s FROM dual   
)   
  SELECT s "STRING",  
        regexp_replace(s, '[a-z]', '1', 1, 0, 'i') "CASE_INSENSITIVE",  
        regexp_replace(s, '[a-z]', '1', 1, 0, 'c') "CASE_SENSITIVE",  
        regexp_replace(s, '[a-zA-Z]', '1', 1, 0, 'c') "CASE_SENSITIVE_MATCHING"  
  FROM  strings;

  STRING     CASE_INSEN CASE_SENSI CASE_SENSI
---------- ---------- ---------- ----------
NEW YORK   111 1111   NEW YORK   111 1111
New York   111 1111   N11 Y111   111 1111
new york   111 1111   111 1111   111 1111
```