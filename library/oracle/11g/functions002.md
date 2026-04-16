# Oracle 11g - functions002
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/functions002.htm

# Single-Row Functions

Single-row functions return a single result row for every row of a queried table or view. These functions can appear in select lists, `WHERE` clauses, `START` `WITH` and `CONNECT` `BY` clauses, and `HAVING` clauses.

## Numeric Functions

Numeric functions accept numeric input and return numeric values. Most numeric functions return `NUMBER` values that are accurate to 38 decimal digits. The transcendental functions `COS`, `COSH`, `EXP`, `LN`, `LOG`, `SIN`, `SINH`, `SQRT`, `TAN`, and `TANH` are accurate to 36 decimal digits. The transcendental functions `ACOS`, `ASIN`, `ATAN`, and `ATAN2` are accurate to 30 decimal digits. The numeric functions are:

[ABS](functions009.md#i81802)
[ACOS](functions010.md#i76693)
[ASIN](functions015.md#i1056765)
[ATAN](functions016.md#i76792)
[ATAN2](functions017.md#i76816)
[BITAND](functions021.md#i98000)
[CEIL](functions024.md#i97801)
[COS](functions037.md#i77138)
[COSH](functions038.md#i82384)
[EXP](functions058.md#i1017093)
[FLOOR](functions067.md#i77449)
[LN](functions090.md#i83932)
[LOG](functions093.md#i84140)
[MOD](functions101.md#i77996)
[NANVL](functions103.md#i1273120)
[POWER](functions129.md#i78493)
[REMAINDER](functions152.md#i1300767)
[ROUND (number)](functions155.md#i78633)
[SIGN](functions164.md#i90056)
[SIN](functions165.md#i78804)
[SINH](functions166.md#i78829)
[SQRT](functions168.md#i1009289)
[TAN](functions193.md#i79242)
[TANH](functions194.md#i79267)
[TRUNC (number)](functions221.md#i79729)
[WIDTH\_BUCKET](functions234.md#i1001630)

## Character Functions Returning Character Values

Character functions that return character values return values of the following data types unless otherwise documented:

* If the input argument is `CHAR` or `VARCHAR2`, then the value returned is `VARCHAR2`.
* If the input argument is `NCHAR` or `NVARCHAR2`, then the value returned is `NVARCHAR2`.

The length of the value returned by the function is limited by the maximum length of the data type returned.

* For functions that return `CHAR` or `VARCHAR2`, if the length of the return value exceeds the limit, then Oracle Database truncates it and returns the result without an error message.
* For functions that return `CLOB` values, if the length of the return values exceeds the limit, then Oracle raises an error and returns no data.

The character functions that return character values are:

[CHR](functions026.md#i76965)
[CONCAT](functions033.md#i77004)
[INITCAP](functions074.md#i77574)
[LOWER](functions094.md#i1043828)
[LPAD](functions095.md#i1371196)
[LTRIM](functions096.md#i77875)
[NCHR](functions104.md#i1273067)
[NLS\_INITCAP](functions110.md#i89841)
[NLS\_LOWER](functions111.md#i78373)
[NLS\_UPPER](functions112.md#i89889)
[NLSSORT](functions113.md#i78399)
[REGEXP\_REPLACE](functions149.md#i1305521)
[REGEXP\_SUBSTR](functions150.md#i1239858)
[REPLACE](functions153.md#i78608)
[RPAD](functions159.md#i78723)
[RTRIM](functions160.md#i1018967)
[SOUNDEX](functions167.md#i78853)
[SUBSTR](functions181.md#i87066)
[TRANSLATE](functions216.md#i1501659)
[TRANSLATE ... USING](functions217.md#i79617)
[TRIM](functions219.md#i79689)
[UPPER](functions226.md#i90176)

## Character Functions Returning Number Values

Character functions that return number values can take as their argument any character data type. The character functions that return number values are:

[ASCII](functions013.md#i1152151)
[INSTR](functions080.md#i77598)
[LENGTH](functions088.md#i77725)
[REGEXP\_COUNT](functions147.md#CIHDAIHJ)
[REGEXP\_INSTR](functions148.md#i1239887)

## Datetime Functions

Datetime functions operate on date (`DATE`), timestamp (`TIMESTAMP`, `TIMESTAMP` `WITH` `TIME` `ZONE`, and `TIMESTAMP` `WITH` `LOCAL` `TIME` `ZONE`), and interval (`INTERVAL` `DAY` `TO` `SECOND`, `INTERVAL` `YEAR` `TO` `MONTH`) values.

Some of the datetime functions were designed for the Oracle `DATE` data type (`ADD_MONTHS`, `CURRENT_DATE`, `LAST_DAY`, `NEW_TIME`, and `NEXT_DAY`). If you provide a timestamp value as their argument, then Oracle Database internally converts the input type to a `DATE` value and returns a `DATE` value. The exceptions are the `MONTHS_BETWEEN` function, which returns a number, and the `ROUND` and `TRUNC` functions, which do not accept timestamp or interval values at all.

The remaining datetime functions were designed to accept any of the three types of data (date, timestamp, and interval) and to return a value of one of these types.

All of the datetime functions that return current system datetime information, such as `SYSDATE`, `SYSTIMESTAMP`, `CURRENT_TIMESTAMP`, and so forth, are evaluated once for each SQL statement, regardless how many times they are referenced in that statement.

The datetime functions are:

[ADD\_MONTHS](functions011.md#i76717)
[CURRENT\_DATE](functions044.md#i999792)
[CURRENT\_TIMESTAMP](functions045.md#i999217)
[DBTIMEZONE](functions048.md#i1327612)
[EXTRACT (datetime)](functions059.md#i1017161)
[FROM\_TZ](functions068.md#i999803)
[LAST\_DAY](functions084.md#i83733)
[LOCALTIMESTAMP](functions092.md#i999873)
[MONTHS\_BETWEEN](functions102.md#i78039)
[NEW\_TIME](functions105.md#i1004085)
[NEXT\_DAY](functions106.md#i78154)
[NUMTODSINTERVAL](functions117.md#i88258)
[NUMTOYMINTERVAL](functions118.md#i89943)
[ORA\_DST\_AFFECTED](functions121.md#CJACAGAI)
[ORA\_DST\_CONVERT](functions122.md#CJAGGAGA)
[ORA\_DST\_ERROR](functions123.md#CJAGGCAB)
[ROUND (date)](functions154.md#i78665)
[SESSIONTIMEZONE](functions162.md#i999827)
[SYS\_EXTRACT\_UTC](functions186.md#i999831)
[SYSDATE](functions191.md#i79216)
[SYSTIMESTAMP](functions192.md#i999835)
[TO\_CHAR (datetime)](functions200.md#i1009324)
[TO\_DSINTERVAL](functions204.md#i1014645)
[TO\_TIMESTAMP](functions213.md#i999843)
[TO\_TIMESTAMP\_TZ](functions214.md#i999847)
[TO\_YMINTERVAL](functions215.md#i999851)
[TRUNC (date)](functions220.md#i79761)
[TZ\_OFFSET](functions222.md#i1001830)

## General Comparison Functions

The general comparison functions determine the greatest and or least value from a set of values. The general comparison functions are:

[GREATEST](functions069.md#i77473)
[LEAST](functions087.md#i77700)

## Hierarchical Functions

Hierarchical functions applies hierarchical path information to a result set. The hierarchical function is:

[SYS\_CONNECT\_BY\_PATH](functions183.md#i1038266)

## Encoding and Decoding Functions

The encoding and decoding functions let you inspect and decode data in the database. The encoding and decoding functions are:

[DECODE](functions049.md#i1017437)
[DUMP](functions055.md#i77278)
[ORA\_HASH](functions124.md#i1235081)
[VSIZE](functions233.md#i80071)

## Environment and Identifier Functions

The environment and identifier functions provide information about the instance and session. The environment and identifier functions are:

[SYS\_CONTEXT](functions184.md#i1038176)
[SYS\_GUID](functions187.md#i79194)
[SYS\_TYPEID](functions188.md#i1044156)
[UID](functions223.md#i79792)
[USER](functions227.md#i79833)
[USERENV](functions228.md#i79862)