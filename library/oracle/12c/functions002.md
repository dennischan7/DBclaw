# Oracle 12c - functions002
Source: https://docs.oracle.com/database/121/SQLRF/functions002.htm

# Single-Row Functions

Single-row functions return a single result row for every row of a queried table or view. These functions can appear in select lists, `WHERE` clauses, `START` `WITH` and `CONNECT` `BY` clauses, and `HAVING` clauses.

## Numeric Functions

Numeric functions accept numeric input and return numeric values. Most numeric functions return `NUMBER` values that are accurate to 38 decimal digits. The transcendental functions `COS`, `COSH`, `EXP`, `LN`, `LOG`, `SIN`, `SINH`, `SQRT`, `TAN`, and `TANH` are accurate to 36 decimal digits. The transcendental functions `ACOS`, `ASIN`, `ATAN`, and `ATAN2` are accurate to 30 decimal digits. The numeric functions are:

[ABS](functions009.md#i81802)
[ACOS](functions010.md#i76693)
[ASIN](functions016.md#i1056765)
[ATAN](functions017.md#i76792)
[ATAN2](functions018.md#i76816)
[BITAND](functions022.md#i98000)
[CEIL](functions025.md#i97801)
[COS](functions044.md#i77138)
[COSH](functions045.md#i82384)
[EXP](functions066.md#i1017093)
[FLOOR](functions076.md#i77449)
[LN](functions102.md#i83932)
[LOG](functions105.md#i84140)
[MOD](functions113.md#i77996)
[NANVL](functions115.md#i1273120)
[POWER](functions143.md#i78493)
[REMAINDER](functions166.md#i1300767)
[ROUND (number)](functions169.md#i78633)
[SIGN](functions178.md#i90056)
[SIN](functions179.md#i78804)
[SINH](functions180.md#i78829)
[SQRT](functions182.md#i1009289)
[TAN](functions209.md#i79242)
[TANH](functions210.md#i79267)
[TRUNC (number)](functions237.md#i79729)
[WIDTH\_BUCKET](functions250.md#i1001630)

## Character Functions Returning Character Values

Character functions that return character values return values of the following data types unless otherwise documented:

* If the input argument is `CHAR` or `VARCHAR2`, then the value returned is `VARCHAR2`.
* If the input argument is `NCHAR` or `NVARCHAR2`, then the value returned is `NVARCHAR2`.

The length of the value returned by the function is limited by the maximum length of the data type returned.

* For functions that return `CHAR` or `VARCHAR2`, if the length of the return value exceeds the limit, then Oracle Database truncates it and returns the result without an error message.
* For functions that return `CLOB` values, if the length of the return values exceeds the limit, then Oracle raises an error and returns no data.

The character functions that return character values are:

[CHR](functions027.md#i76965)
[CONCAT](functions040.md#i77004)
[INITCAP](functions083.md#i77574)
[LOWER](functions106.md#i1043828)
[LPAD](functions107.md#i1371196)
[LTRIM](functions108.md#i77875)
[NCHR](functions116.md#i1273067)
[NLS\_INITCAP](functions122.md#i89841)
[NLS\_LOWER](functions123.md#i78373)
[NLS\_UPPER](functions124.md#i89889)
[NLSSORT](functions125.md#i78399)
[REGEXP\_REPLACE](functions163.md#i1305521)
[REGEXP\_SUBSTR](functions164.md#i1239858)
[REPLACE](functions167.md#i78608)
[RPAD](functions173.md#i78723)
[RTRIM](functions174.md#i1018967)
[SOUNDEX](functions181.md#i78853)
[SUBSTR](functions196.md#i87066)
[TRANSLATE](functions232.md#i1501659)
[TRANSLATE ... USING](functions233.md#i79617)
[TRIM](functions235.md#i79689)
[UPPER](functions242.md#i90176)

## Character Functions Returning Number Values

Character functions that return number values can take as their argument any character data type. The character functions that return number values are:

[ASCII](functions014.md#i1152151)
[INSTR](functions089.md#i77598)
[LENGTH](functions100.md#i77725)
[REGEXP\_COUNT](functions161.md#CIHDAIHJ)
[REGEXP\_INSTR](functions162.md#i1239887)

## Datetime Functions

Datetime functions operate on date (`DATE`), timestamp (`TIMESTAMP`, `TIMESTAMP` `WITH` `TIME` `ZONE`, and `TIMESTAMP` `WITH` `LOCAL` `TIME` `ZONE`), and interval (`INTERVAL` `DAY` `TO` `SECOND`, `INTERVAL` `YEAR` `TO` `MONTH`) values.

Some of the datetime functions were designed for the Oracle `DATE` data type (`ADD_MONTHS`, `CURRENT_DATE`, `LAST_DAY`, `NEW_TIME`, and `NEXT_DAY`). If you provide a timestamp value as their argument, then Oracle Database internally converts the input type to a `DATE` value and returns a `DATE` value. The exceptions are the `MONTHS_BETWEEN` function, which returns a number, and the `ROUND` and `TRUNC` functions, which do not accept timestamp or interval values at all.

The remaining datetime functions were designed to accept any of the three types of data (date, timestamp, and interval) and to return a value of one of these types.

All of the datetime functions that return current system datetime information, such as `SYSDATE`, `SYSTIMESTAMP`, `CURRENT_TIMESTAMP`, and so forth, are evaluated once for each SQL statement, regardless how many times they are referenced in that statement.

The datetime functions are:

[ADD\_MONTHS](functions011.md#i76717)
[CURRENT\_DATE](functions051.md#i999792)
[CURRENT\_TIMESTAMP](functions052.md#i999217)
[DBTIMEZONE](functions056.md#i1327612)
[EXTRACT (datetime)](functions067.md#i1017161)
[FROM\_TZ](functions077.md#i999803)
[LAST\_DAY](functions096.md#i83733)
[LOCALTIMESTAMP](functions104.md#i999873)
[MONTHS\_BETWEEN](functions114.md#i78039)
[NEW\_TIME](functions117.md#i1004085)
[NEXT\_DAY](functions118.md#i78154)
[NUMTODSINTERVAL](functions129.md#i88258)
[NUMTOYMINTERVAL](functions130.md#i89943)
[ORA\_DST\_AFFECTED](functions133.md#CJACAGAI)
[ORA\_DST\_CONVERT](functions134.md#CJAGGAGA)
[ORA\_DST\_ERROR](functions135.md#CJAGGCAB)
[ROUND (date)](functions168.md#i78665)
[SESSIONTIMEZONE](functions176.md#i999827)
[SYS\_EXTRACT\_UTC](functions201.md#i999831)
[SYSDATE](functions207.md#i79216)
[SYSTIMESTAMP](functions208.md#i999835)
[TO\_CHAR (datetime)](functions216.md#i1009324)
[TO\_DSINTERVAL](functions220.md#i1014645)
[TO\_TIMESTAMP](functions229.md#i999843)
[TO\_TIMESTAMP\_TZ](functions230.md#i999847)
[TO\_YMINTERVAL](functions231.md#i999851)
[TRUNC (date)](functions236.md#i79761)
[TZ\_OFFSET](functions238.md#i1001830)

## General Comparison Functions

The general comparison functions determine the greatest and or least value from a set of values. The general comparison functions are:

[GREATEST](functions078.md#i77473)
[LEAST](functions099.md#i77700)

## Hierarchical Functions

Hierarchical functions applies hierarchical path information to a result set. The hierarchical function is:

[SYS\_CONNECT\_BY\_PATH](functions198.md#i1038266)

## Encoding and Decoding Functions

The encoding and decoding functions let you inspect and decode data in the database. The encoding and decoding functions are:

[DECODE](functions057.md#i1017437)
[DUMP](functions063.md#i77278)
[ORA\_HASH](functions136.md#i1235081)
[STANDARD\_HASH](functions183.md#BABCCAFF)
[VSIZE](functions249.md#i80071)