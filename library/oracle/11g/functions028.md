# Oracle 11g - functions028
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/functions028.htm

# CLUSTER\_PROBABILITY

Syntax

mining\_attribute\_clause::=

Purpose

This function is for use with clustering models created by the `DBMS_DATA_MINING` package or with Oracle Data Miner. It returns a measure of the degree of confidence of membership of an input row in a cluster associated with the specified model.

* For `cluster_id`, specify the identifier of the cluster in the model. The function returns the probability for the specified cluster. If you omit this clause, then the function returns the probability associated with the best predicted cluster. You can use the form without `cluster_id` in conjunction with the `CLUSTER_ID` function to obtain the best predicted pair of cluster ID and probability.
* The `mining_attribute_clause` behaves as described for the `PREDICTION` function. Refer to [mining\_attribute\_clause](functions132.md#CJAJACJD)

Examples

The following example determines the ten most representative customers, based on likelihood, in cluster 2.

This example, and the prerequisite data mining operations, including the creation of the `km_sh_clus_sample` model and the `mining_data_apply_v` view, can be found in the demo file `$ORACLE_HOME/rdbms/demo/dmkmdemo.sql`. General information on data mining demo files is available in [Oracle Data Mining Administrator's Guide](../../datamine.112/e16807/sampleprogs.md#DMADM009). The example is presented here to illustrate the syntactic use of the function.

```
SELECT *
  FROM (SELECT cust_id, CLUSTER_PROBABILITY(km_sh_clus_sample, 2 USING *) prob
          FROM mining_data_apply_v
          ORDER BY prob DESC)
  WHERE ROWNUM < 11;

   CUST_ID       PROB
---------- ----------
    100256 .999387471
    100988  .99936194
    100889 .999335107
    101086  .99928882
    101215 .999266521
    100390 .999264718
    100985 .999251722
    101026 .999247906
    100601 .999242089
    100672 .999235711
 
10 rows selected.
```