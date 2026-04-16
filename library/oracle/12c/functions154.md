# Oracle 12c - functions154
Source: https://docs.oracle.com/database/121/SQLRF/functions154.htm

[Go to main content](#BEGIN)

227/555 

# PREVIOUS

Syntax

Purpose

The `PREVIOUS` function can be used only in the `model_clause` of the `SELECT` statement and then only in the `ITERATE` ... [ `UNTIL` `]` clause of the `model_rules_clause`. It returns the value of `cell_reference` at the beginning of each iteration.

Examples

The following example repeats the rules, up to 1000 times, until the difference between the values of `cur_val` at the beginning and at the end of an iteration is less than one:

```
SELECT dim_col, cur_val, num_of_iterations
  FROM (SELECT 1 AS dim_col, 10 AS cur_val FROM dual)
  MODEL
    DIMENSION BY (dim_col)
    MEASURES (cur_val, 0 num_of_iterations)
    IGNORE NAV
    UNIQUE DIMENSION
    RULES ITERATE (1000) UNTIL (PREVIOUS(cur_val[1]) - cur_val[1] < 1)
    (
      cur_val[1] = cur_val[1]/2,
      num_of_iterations[1] = num_of_iterations[1] + 1
    );

   DIM_COL    CUR_VAL NUM_OF_ITERATIONS
---------- ---------- -----------------
         1       .625                 4
```

Scripting on this page enhances content navigation, but does not change the content in any way.