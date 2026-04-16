# Oracle 21c - Lexical-Conventions
Source: https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/Lexical-Conventions.html

The following lexical conventions for issuing SQL statements apply specifically to the Oracle Database implementation of SQL, but are generally acceptable in other SQL implementations.

When you issue a SQL statement, you can include one or more tabs, carriage returns, spaces, or comments anywhere a space occurs within the definition of the statement. Thus, Oracle Database evaluates the following two statements in the same manner:

```
SELECT last_name,salary*12,MONTHS_BETWEEN(SYSDATE,hire_date) 
  FROM employees
  WHERE department_id = 30
  ORDER BY last_name;

SELECT last_name,
  salary * 12,
        MONTHS_BETWEEN( SYSDATE, hire_date )
FROM employees
WHERE department_id=30
ORDER BY last_name;
```

Case is insignificant in reserved words, keywords, identifiers, and parameters. However, case is significant in text literals and quoted names. Refer to [Text Literals](Literals.md#GUID-1824CBAA-6E16-4921-B2A6-112FB02248DA) for a syntax description of text literals.

Note:

SQL statements are terminated differently in different programming environments. This documentation set uses the default SQL\*Plus character, the semicolon (;).