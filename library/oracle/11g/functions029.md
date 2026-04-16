# Oracle 11g - functions029
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/functions029.htm

# CLUSTER\_SET

Syntax

mining\_attribute\_clause::=

Purpose

This function is for use with clustering models created by the `DBMS_DATA_MINING` package or with Oracle Data Miner. It returns a varray of objects containing all possible clusters that a given row belongs to. Each object in the varray is a pair of scalar values containing the cluster ID and the cluster probability. The object fields are named `CLUSTER_ID` and `PROBABILITY`, and both are Oracle `NUMBER`.

* For the optional `topN` argument, specify a positive integer. Doing so restricts the set of predicted clusters to those that have one of the top `N` probability values. If you omit `topN` or set it to `NULL`, then all clusters are returned in the collection. If multiple clusters are tied for the `Nth` value, the database still returns only `N` values.
* For the optional `cutoff` argument, specify a positive integer to restrict the returned clusters to those with a probability greater than or equal to the specified cutoff. You can filter only by `cutoff` by specifying `NULL` for `topN` and the desired cutoff value for `cutoff`.

You can specify `topN` and `cutoff` together to restrict the returned clusters to those that are in the top `N` and have a probability that passes the threshold.

The `mining_attribute_clause` behaves as described for the `PREDICTION` function. Refer to [mining\_attribute\_clause](functions132.md#CJAJACJD).

Examples

The following example lists the most relevant attributes (with confidence > 55%) of each cluster to which customer 101362 belongs with > 20% likelihood.

This example, and the prerequisite data mining operations, including the creation of the `km_sh_clus_sample` model and the views and type, can be found in the demo file `$ORACLE_HOME/rdbms/demo/dmkmdemo.sql`. General information on data mining demo files is available in [Oracle Data Mining Administrator's Guide](../../datamine.112/e16807/sampleprogs.md#DMADM009). The example is presented here to illustrate the syntactic use of the function.

```
WITH
clus_tab AS (
SELECT id,
       A.attribute_name aname,
       A.conditional_operator op,
       NVL(A.attribute_str_value,
         ROUND(A.attribute_num_value),4)) val,
       A.attribute_support support,
       A.attribute_confidence confidence
  FROM TABLE(DBMS_DATA_MINING.GET_MODEL_DETAILS_KM('km_sh_clus_sample')) T,
       TABLE(T.rule.antecedent) A
 WHERE A.attribute_confidence > 0.55
),
clust AS (
SELECT id,
       CAST(COLLECT(Cattr(aname, op, TO_CHAR(val), support, confidence))
         AS Cattrs) cl_attrs
  FROM clus_tab
GROUP BY id
),
custclus AS (
SELECT T.cust_id, S.cluster_id, S.probability
  FROM (SELECT cust_id, CLUSTER_SET(km_sh_clus_sample, NULL, 0.2 USING *) pset
          FROM mining_data_apply_v
         WHERE cust_id = 101362) T,
       TABLE(T.pset) S
)
SELECT A.probability prob, A.cluster_id cl_id,
       B.attr, B.op, B.val, B.supp, B.conf
  FROM custclus A,
       (SELECT T.id, C.*
          FROM clust T,
               TABLE(T.cl_attrs) C) B
 WHERE A.cluster_id = B.id
ORDER BY prob DESC, cl_id ASC, conf DESC, attr ASC, val ASC;

   PROB      CL_ID ATTR                       OP VAL             SUPP    CONF
------- ---------- -------------------------- -- ----------- -------- -------
  .7745          8 HOUSEHOLD_SIZE             IN 9+               124   .7500
  .7745          8 CUST_MARITAL_STATUS        IN Divorc.          116   .6000
  .7745          8 CUST_MARITAL_STATUS        IN NeverM           116   .6000
  .7745          8 CUST_MARITAL_STATUS        IN Separ.           116   .6000
  .7745          8 CUST_MARITAL_STATUS        IN Widowed          116   .6000
  .2028          6 AGE                        >= 17               154   .6667
  .2028          6 AGE                        <= 31.6             154   .6667
  .2028          6 CUST_MARITAL_STATUS        IN NeverM           172   .6667
8 rows selected.
```