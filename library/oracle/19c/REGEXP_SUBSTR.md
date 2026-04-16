# Oracle 19c - REGEXP_SUBSTR
Source: https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/REGEXP_SUBSTR.html

The following example examines the string, looking for the first substring bounded by commas. Oracle Database searches for a comma followed by one or more occurrences of non-comma characters followed by a comma. Oracle returns the substring, including the leading and trailing commas.

```
SELECT
  REGEXP_SUBSTR('500 Oracle Parkway, Redwood Shores, CA',
                ',[^,]+,') "REGEXPR_SUBSTR"
  FROM DUAL;

REGEXPR_SUBSTR
-----------------
, Redwood Shores,
```

The following example examines the string, looking for `http://` followed by a substring of one or more alphanumeric characters and optionally, a period (`.`). Oracle searches for a minimum of three and a maximum of four occurrences of this substring between `http://` and either a slash (`/`) or the end of the string.

```
SELECT
  REGEXP_SUBSTR('http://www.example.com/products',
                'http://([[:alnum:]]+\.?){3,4}/?') "REGEXP_SUBSTR"
  FROM DUAL;

REGEXP_SUBSTR
----------------------
http://www.example.com/
```

The next two examples use the `subexpr` argument to return a specific subexpression of `pattern`. The first statement returns the first subexpression in `pattern`:

```
SELECT REGEXP_SUBSTR('1234567890', '(123)(4(56)(78))', 1, 1, 'i', 1) 
"REGEXP_SUBSTR" FROM DUAL;

REGEXP_SUBSTR
-------------------
123
```

The next statement returns the fourth subexpression in `pattern`:

```
SELECT REGEXP_SUBSTR('1234567890', '(123)(4(56)(78))', 1, 1, 'i', 4) 
"REGEXP_SUBSTR" FROM DUAL;

REGEXP_SUBSTR
-------------------
78
```

REGEXP\_SUBSTR pattern matching: Examples

The following statements create a table regexp\_temp and insert values into it:

```
CREATE TABLE regexp_temp(empName varchar2(20), emailID varchar2(20));

INSERT INTO regexp_temp (empName, emailID) VALUES ('John Doe', 'johndoe@example.com');
INSERT INTO regexp_temp (empName, emailID) VALUES ('Jane Doe', 'janedoe');
```

In the following example, the statement queries the email column and searches for valid email addresses:

```
SELECT empName, REGEXP_SUBSTR(emailID, '[[:alnum:]]+\@[[:alnum:]]+\.[[:alnum:]]+') "Valid Email" FROM regexp_temp;

EMPNAME  Valid Email
-------- -------------------
John Doe johndoe@example.com
Jane Doe
```

In the following example, the statement queries the email column and returns the count of valid email addresses:

```
SELECT empName, REGEXP_SUBSTR(emailID, '[[:alnum:]]+\@[[:alnum:]]+\.[[:alnum:]]+') "Valid Email", REGEXP_INSTR(emailID, '\w+@\w+(\.\w+)+') "FIELD_WITH_VALID_EMAIL" FROM regexp_temp;

EMPNAME		Valid Email			FIELD_WITH_VALID_EMAIL
--------	-------------------	----------------------
John Doe	johndoe@example.com	1
Jane Doe	
```

In the following example, numbers and alphabets are extracted from a string:

```
with strings as (   
  select 'ABC123' str from dual union all   
  select 'A1B2C3' str from dual union all   
  select '123ABC' str from dual union all   
  select '1A2B3C' str from dual   
)   
  select regexp_substr(str, '[0-9]') First_Occurrence_of_Number,    
         regexp_substr(str, '[0-9].*') Num_Followed_by_String,   
         regexp_substr(str, '[A-Z][0-9]') Letter_Followed_by_String   
  from strings;

FIRST_OCCURRENCE_OF_NUMB NUM_FOLLOWED_BY_STRING   LETTER_FOLLOWED_BY_STRIN
------------------------ ------------------------ ------------------------
1			 123			  C1
1			 1B2C3			  A1
1			 123ABC
1			 1A2B3C 		  A2
```

In the following example, passenger names and flight information are extracted from a string:

```
with strings as (    
  select 'LHRJFK/010315/JOHNDOE' str from dual union all    
  select 'CDGLAX/050515/JANEDOE' str from dual union all    
  select 'LAXCDG/220515/JOHNDOE' str from dual union all    
  select 'SFOJFK/010615/JANEDOE' str from dual    
)    
  SELECT regexp_substr(str, '[A-Z]{6}') String_of_6_characters,   
         regexp_substr(str, '[0-9]+') First_Matching_Numbers,   
         regexp_substr(str, '[A-Z].*$') Letter_by_other_characters,     
         regexp_substr(str, '/[A-Z].*$') Slash_letter_and_characters     
  FROM strings;

STRING_OF_6_CHARACTERS	FIRST_MATCHING_NUMBERS	LETTER_BY_OTHER_CHARACTERS	SLASH_LETTER_AND_CHARACTERS
----------------------	----------------------	--------------------------	---------------------------
LHRJFK	                010315	                LHRJFK/010315/JOHNDOE	      	/JOHNDOE
CDGLAX	                050515	                CDGLAX/050515/JANEDOE	      	/JANEDOE
LAXCDG	                220515	                LAXCDG/220515/JOHNDOE	      	/JOHNDOE
SFOJFK	                010615	                SFOJFK/010615/JANEDOE	      	/JANEDOE
```