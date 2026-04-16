# Oracle 23c - REGEXP_INSTR
Source: https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/REGEXP_INSTR.html

The following example examines the string, looking for occurrences of one or more non-blank characters. Oracle begins searching at the first character in the string and returns the starting position (default) of the sixth occurrence of one or more non-blank characters.

```
SELECT
  REGEXP_INSTR('500 Oracle Parkway, Redwood Shores, CA',
               '[^ ]+', 1, 6) "REGEXP_INSTR"
  FROM DUAL;

REGEXP_INSTR
------------
          37
```

The following example examines the string, looking for occurrences of words beginning with `s`, `r`, or `p`, regardless of case, followed by any six alphabetic characters. Oracle begins searching at the third character in the string and returns the position in the string of the character following the second occurrence of a seven-letter word beginning with `s`, `r`, or `p`, regardless of case.

```
SELECT
  REGEXP_INSTR('500 Oracle Parkway, Redwood Shores, CA',
               '[s|r|p][[:alpha:]]{6}', 3, 2, 1, 'i') "REGEXP_INSTR"
  FROM DUAL;

REGEXP_INSTR
------------
          28
```

The following examples use the `subexpr` argument to search for a particular subexpression in `pattern`. The first statement returns the position in the source string of the first character in the first subexpression, which is '123':

```
SELECT REGEXP_INSTR('1234567890', '(123)(4(56)(78))', 1, 1, 0, 'i', 1) 
"REGEXP_INSTR" FROM DUAL;

REGEXP_INSTR
-------------------
1
```

The next statement returns the position in the source string of the first character in the second subexpression, which is '45678':

```
SELECT REGEXP_INSTR('1234567890', '(123)(4(56)(78))', 1, 1, 0, 'i', 2) 
"REGEXP_INSTR" FROM DUAL;

REGEXP_INSTR
-------------------
4
```

The next statement returns the position in the source string of the first character in the fourth subexpression, which is '78':

```
SELECT REGEXP_INSTR('1234567890', '(123)(4(56)(78))', 1, 1, 0, 'i', 4) 
"REGEXP_INSTR" FROM DUAL;

REGEXP_INSTR
-------------------
7
```

REGEXP\_INSTR pattern matching: Examples

The following statements create a table regexp\_temp and insert values into it:

```
CREATE TABLE regexp_temp(empName varchar2(20), emailID varchar2(20));

INSERT INTO regexp_temp (empName, emailID) VALUES ('John Doe', 'johndoe@example.com');
INSERT INTO regexp_temp (empName, emailID) VALUES ('Jane Doe', 'janedoe');
```

In the following example, the statement queries the email column and searches for valid email addresses:

```
SELECT emailID, REGEXP_INSTR(emailID, '\w+@\w+(\.\w+)+') "IS_A_VALID_EMAIL" FROM regexp_temp;

EMAILID 	     IS_A_VALID_EMAIL
-------------------- ----------------
johndoe@example.com		    1
example.com			    0
```

In the following example, the statement queries the email column and returns the count of valid email addresses:

```
EMPNAME		Valid Email			FIELD_WITH_VALID_EMAIL
--------	-------------------	----------------------
John Doe	johndoe@example.com	1
Jane Doe						
```