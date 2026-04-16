# Oracle 11g - functions063
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/functions063.htm

# FEATURE\_SET

Syntax

mining\_attribute\_clause:=

Purpose

This function is for use with feature extraction models created by the `DBMS_DATA_MINING` package or with Oracle Data Miner. It returns a varray of objects containing all possible features. Each object in the varray is a pair of scalar values containing the feature ID and the feature value. The object fields are named `FEATURE­_ID` and `VALUE`, and both are Oracle `NUMBER`.

The optional `topN` argument is a positive integer that restricts the set of features to those that have one of the top `N` values. If there is a tie at the `Nth` value, then the database still returns only `N` values. If you omit this argument, then the function returns all features.

The optional `cutoff` argument restricts the returned features to only those that have a feature value greater than or equal to the specified cutoff. To filter only by `cutoff`, specify `NULL` for `topN` and the desired cutoff for `cutoff`.

The `mining_attribute_clause` behaves as described for the `PREDICTION` function. Refer to [mining\_attribute\_clause](functions132.md#CJAJACJD).

Examples

The following example lists the top features corresponding to a given customer record (based on match quality), and determines the top attributes for each feature (based on coefficient > 0.25).

This example and the prerequisite data mining operations, including the creation of the model, views, and type, can be found in the demo file `$ORACLE_HOME/rdbms/demo/dmnmdemo.sql`. General information on data mining demo files is available in [Oracle Data Mining Administrator's Guide](../../datamine.112/e16807/sampleprogs.md#DMADM009). The example is presented here to illustrate the syntactic use of the function.

```
WITH
feat_tab AS (
SELECT F.feature_id fid,
       A.attribute_name attr,
       TO_CHAR(A.attribute_value) val,
       A.coefficient coeff
  FROM TABLE(DBMS_DATA_MINING.GET_MODEL_DETAILS_NMF('nmf_sh_sample')) F,
       TABLE(F.attribute_set) A
 WHERE A.coefficient > 0.25
),
feat AS (
SELECT fid,
       CAST(COLLECT(Featattr(attr, val, coeff))
         AS Featattrs) f_attrs
  FROM feat_tab
GROUP BY fid
),
cust_10_features AS (
SELECT T.cust_id, S.feature_id, S.value
  FROM (SELECT cust_id, FEATURE_SET(nmf_sh_sample, 10 USING *) pset
          FROM nmf_sh_sample_apply_prepared
         WHERE cust_id = 100002) T,
       TABLE(T.pset) S
)
SELECT A.value, A.feature_id fid,
       B.attr, B.val, B.coeff
  FROM cust_10_features A,
       (SELECT T.fid, F.*
          FROM feat T,
               TABLE(T.f_attrs) F) B
 WHERE A.feature_id = B.fid
ORDER BY A.value DESC, A.feature_id ASC, coeff DESC, attr ASC, val ASC;

   VALUE  FID ATTR                      VAL                        COEFF
-------- ---- ------------------------- ------------------------ -------
  6.8409    7 YRS_RESIDENCE                                       1.3879
  6.8409    7 BOOKKEEPING_APPLICATION                              .4388
  6.8409    7 CUST_GENDER               M                          .2956
  6.8409    7 COUNTRY_NAME              United States of America   .2848
  6.4975    3 YRS_RESIDENCE                                       1.2668
  6.4975    3 BOOKKEEPING_APPLICATION                              .3465
  6.4975    3 COUNTRY_NAME              United States of America   .2927
  6.4886    2 YRS_RESIDENCE                                       1.3285
  6.4886    2 CUST_GENDER               M                          .2819
  6.4886    2 PRINTER_SUPPLIES                                     .2704
  6.3953    4 YRS_RESIDENCE                                       1.2931
  5.9640    6 YRS_RESIDENCE                                       1.1585
  5.9640    6 HOME_THEATER_PACKAGE                                 .2576
  5.2424    5 YRS_RESIDENCE                                       1.0067
  2.4714    8 YRS_RESIDENCE                                        .3297
  2.3559    1 YRS_RESIDENCE                                        .2768
  2.3559    1 FLAT_PANEL_MONITOR                                   .2593
 
17 rows selected.
```