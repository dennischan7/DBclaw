# Oracle 12c - functions003
Source: https://docs.oracle.com/database/121/SQLRF/functions003.htm

# Aggregate Functions

Aggregate functions return a single result row based on groups of rows, rather than on single rows. Aggregate functions can appear in select lists and in `ORDER` `BY` and `HAVING` clauses. They are commonly used with the `GROUP` `BY` clause in a `SELECT` statement, where Oracle Database divides the rows of a queried table or view into groups. In a query containing a `GROUP` `BY` clause, the elements of the select list can be aggregate functions, `GROUP` `BY` expressions, constants, or expressions involving one of these. Oracle applies the aggregate functions to each group of rows and returns a single result row for each group.

If you omit the `GROUP` `BY` clause, then Oracle applies aggregate functions in the select list to all the rows in the queried table or view. You use aggregate functions in the `HAVING` clause to eliminate groups from the output based on the results of the aggregate functions, rather than on the values of the individual rows of the queried table or view.

Many (but not all) aggregate functions that take a single argument accept these clauses:

* `DISTINCT` and `UNIQUE`, which are synonymous, cause an aggregate function to consider only distinct values of the argument expression. The syntax diagrams for aggregate functions in this chapter use the keyword `DISTINCT` for simplicity.
* `ALL` causes an aggregate function to consider all values, including all duplicates.

For example, the `DISTINCT` average of 1, 1, 1, and 3 is 2. The `ALL` average is 1.5. If you specify neither, then the default is `ALL`.

Some aggregate functions allow the `windowing_clause`, which is part of the syntax of analytic functions. Refer to [windowing\_clause](functions004.md#i97640) for information about this clause. In the listing of aggregate functions at the end of this section, the functions that allow the `windowing_clause` are followed by an asterisk (\*)

All aggregate functions except `COUNT`(\*), `GROUPING`, and `GROUPING_ID` ignore nulls. You can use the `NVL` function in the argument to an aggregate function to substitute a value for a null. `COUNT` and `REGR_COUNT` never return null, but return either a number or zero. For all the remaining aggregate functions, if the data set contains no rows, or contains only rows with nulls as arguments to the aggregate function, then the function returns null.

The aggregate functions `MIN`, `MAX`, `SUM`, `AVG`, `COUNT`, `VARIANCE`, and `STDDEV`, when followed by the `KEEP` keyword, can be used in conjunction with the `FIRST` or `LAST` function to operate on a set of values from a set of rows that rank as the `FIRST` or `LAST` with respect to a given sorting specification. Refer to [FIRST](functions074.md#i1000901) for more information.

You can nest aggregate functions. For example, the following example calculates the average of the maximum salaries of all the departments in the sample schema `hr`:

```
SELECT AVG(MAX(salary))
  FROM employees
  GROUP BY department_id;

AVG(MAX(SALARY))
----------------
      10926.3333
```

This calculation evaluates the inner aggregate (`MAX`(`salary`)) for each group defined by the `GROUP` `BY` clause (`department_id`), and aggregates the results again.

In the list of aggregate functions that follows, functions followed by an asterisk (\*) allow the `windowing_clause`.

[APPROX\_COUNT\_DISTINCT](functions013.md#CJAEJAGD)
[AVG](functions019.md#i82074)
[COLLECT](functions034.md#i1271564)
[CORR](functions042.md#i82637)
[CORR\_\*](functions043.md#i1293691)
[COUNT](functions046.md#i82697)
[COVAR\_POP](functions047.md#i1008854)
[COVAR\_SAMP](functions048.md#i82820)
[CUME\_DIST](functions050.md#i82886)
[DENSE\_RANK](functions060.md#i1064409)
[FIRST](functions074.md#i1000901)
[GROUP\_ID](functions079.md#i1002035)
[GROUPING](functions080.md#i77498)
[GROUPING\_ID](functions081.md#i1001964)
[LAST](functions095.md#i1000905)
[LISTAGG](functions101.md#CJABDFBD)
[MAX](functions110.md#i89072)
[MEDIAN](functions111.md#i1279886)
[MIN](functions112.md#i1280029)
[PERCENT\_RANK](functions140.md#i1043951)
[PERCENTILE\_CONT](functions141.md#i1000909)
[PERCENTILE\_DISC](functions142.md#i1000913)
[RANK](functions155.md#i1269223)
[REGR\_ (Linear Regression) Functions](functions165.md#i85922)
[STATS\_BINOMIAL\_TEST](functions184.md#i1279891)
[STATS\_CROSSTAB](functions185.md#i1333770)
[STATS\_F\_TEST](functions186.md#i1279901)
[STATS\_KS\_TEST](functions187.md#i1279906)
[STATS\_MODE](functions188.md#i1279911)
[STATS\_MW\_TEST](functions189.md#i1279921)
[STATS\_ONE\_WAY\_ANOVA](functions190.md#i1335576)
[STATS\_T\_TEST\_\*](functions191.md#i1279931)
[STATS\_WSR\_TEST](functions192.md#i1279951)
[STDDEV](functions193.md#i89108)
[STDDEV\_POP](functions194.md#i86639)
[STDDEV\_SAMP](functions195.md#i86697)
[SUM](functions197.md#i89126)
[SYS\_OP\_ZONE\_ID](functions203.md#CJABIIAF)
[SYS\_XMLAGG](functions205.md#i1006716)
[VAR\_POP](functions246.md#i87119)
[VAR\_SAMP](functions247.md#i87169)
[VARIANCE](functions248.md#i89144)
[XMLAGG](functions251.md#i1286333)