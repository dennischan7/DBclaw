# Oracle 12c - functions192
Source: https://docs.oracle.com/database/121/SQLRF/functions192.htm

[Go to main content](#BEGIN)

265/555 

# STATS\_WSR\_TEST

Syntax

Purpose

`STATS_WSR_TEST` is a Wilcoxon Signed Ranks test of paired samples to determine whether the median of the differences between the samples is significantly different from zero. The absolute values of the differences are ordered and assigned ranks. Then the null hypothesis states that the sum of the ranks of the positive differences is equal to the sum of the ranks of the negative differences.

This function takes two required arguments: `expr1` and `expr2` are the two samples being analyzed. The optional third argument lets you specify the meaning of the `NUMBER` value returned by this function, as shown in [Table 7-10](#g1514203). For this argument, you can specify a text literal, or a bind variable or expression that evaluates to a constant character value. If you omit the third argument, then the default is `'TWO_SIDED_SIG'`.

Table 7-10 STATS\_WSR\_TEST\_\* Return Values

| Argument | Return Value Meaning |
| --- | --- |
| `'STATISTIC'` | The observed value of Z |
| `'ONE_SIDED_SIG'` | One-tailed significance of Z |
| `'TWO_SIDED_SIG'` | Two-tailed significance of Z |

One-sided significance is always with respect to the upper tail. The high value (the value whose rejection region is the upper tail) is `expr1`.

Scripting on this page enhances content navigation, but does not change the content in any way.