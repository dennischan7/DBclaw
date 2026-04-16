# Oracle 21c - STATS_F_TEST
Source: https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/STATS_F_TEST.html

`STATS_F_TEST` tests whether two variances are significantly different. The observed value of f is the ratio of one variance to the other, so values very different from 1 usually indicate significant differences.

This function takes two required arguments: `expr1` is the grouping or independent variable and `expr2` is the sample of values. The optional third argument lets you specify the meaning of the `NUMBER` value returned by this function, as shown in [Table 7-5](STATS_F_TEST.md#GUID-9E2A91FC-5BB3-449A-810C-DA6CB52B56ED__G1514122 "The first column lists the values you can specify for the argument of the function and the second column explains the return value meanings."). For this argument, you can specify a text literal, or a bind variable or expression that evaluates to a constant character value. If you omit the third argument, then the default is `'TWO_SIDED_SIG'`.

The one-tailed significance is always in relation to the upper tail. The final argument, `expr3`, indicates which of the two groups specified by `expr1` is the high value or numerator (the value whose rejection region is the upper tail).

The observed value of f is the ratio of the variance of one group to the variance of the second group. The significance of the observed value of f is the probability that the variances are different just by chanceâa number between 0 and 1. A small value for the significance indicates that the variances are significantly different. The degree of freedom for each of the variances is the number of observations in the sample minus 1.

The following example determines whether the variance in credit limit between men and women is significantly different. The results, a p\_value not close to zero, and an f\_statistic close to 1, indicate that the difference between credit limits for men and women are not significant.

```
SELECT VARIANCE(DECODE(cust_gender, 'M', cust_credit_limit, null)) var_men,
       VARIANCE(DECODE(cust_gender, 'F', cust_credit_limit, null)) var_women,
       STATS_F_TEST(cust_gender, cust_credit_limit, 'STATISTIC', 'F') f_statistic,
       STATS_F_TEST(cust_gender, cust_credit_limit) two_sided_p_value
  FROM sh.customers;

   VAR_MEN  VAR_WOMEN F_STATISTIC TWO_SIDED_P_VALUE
---------- ---------- ----------- -----------------
12879896.7   13046865  1.01296348        .311928071
```