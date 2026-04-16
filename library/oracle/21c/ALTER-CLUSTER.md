# Oracle 21c - ALTER-CLUSTER
Source: https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/ALTER-CLUSTER.html

physical\_attributes\_clause

Use this clause to change the values of the `PCTUSED`, `PCTFREE`, and `INITRANS` parameters of the cluster.

Use the `STORAGE` clause to change the storage characteristics of the cluster.

Restriction on Physical Attributes

You cannot change the values of the storage parameters `INITIAL` and `MINEXTENTS` for a cluster.

Examples

The following examples modify the clusters that were created in the `CREATE` `CLUSTER` "[Examples](CREATE-CLUSTER.md#GUID-4DBC701F-AFC3-486D-AA32-B5CB1D6946F7__I2105031)".

Modifying a Cluster: Example

The next statement alters the `personnel` cluster:

```
ALTER CLUSTER personnel
   SIZE 1024 CACHE;
```

Oracle Database allocates 1024 bytes for each cluster key value and enables the cache attribute. Assuming a data block size of 2 kilobytes, future data blocks within this cluster contain 2 cluster keys in each data block, or 2 kilobytes divided by 1024 bytes.

Deallocating Unused Space: Example

The following statement deallocates unused space from the `language` cluster, keeping 30 kilobytes of unused space for future use:

```
ALTER CLUSTER language 
   DEALLOCATE UNUSED KEEP 30 K;
```

Altering Clusters: Example

The following statement creates a cluster with the default key size (600):

```
CREATE CLUSTER EMP_DEPT (DEPTNO NUMBER(3))   
   SIZE 600   
   TABLESPACE USERS   
   STORAGE (INITIAL 200K   
      NEXT 300K   
      MINEXTENTS 2   
      PCTINCREASE 33);
```

The following statement queries `USER_CLUSTERS` to display the cluster metadata:

```
SELECT CLUSTER_NAME, TABLESPACE_NAME, KEY_SIZE, CLUSTER_TYPE, AVG_BLOCKS_PER_KEY, MIN_EXTENTS, MAX_EXTENTS FROM USER_CLUSTERS;

CLUSTER_NAME    TABLESPACE_NAME                  KEY_SIZE CLUST AVG_BLOCKS_PER_KEY MIN_EXTENTS MAX_EXTENTS
--------------- ------------------------------ ---------- ----- ------------------ ----------- -----------
EMP_DEPT        USERS                                 600 INDEX                              1  2147483645
```

The following statement modifies the cluster key size:

```
ALTER CLUSTER EMP_DEPT SIZE 1024;
```

The following statement displays the metadata of the modified cluster:

```
SELECT CLUSTER_NAME, TABLESPACE_NAME, KEY_SIZE, CLUSTER_TYPE, AVG_BLOCKS_PER_KEY, MIN_EXTENTS, MAX_EXTENTS FROM USER_CLUSTERS;

CLUSTER_NAME    TABLESPACE_NAME                  KEY_SIZE CLUST AVG_BLOCKS_PER_KEY MIN_EXTENTS MAX_EXTENTS
--------------- ------------------------------ ---------- ----- ------------------ ----------- -----------
EMP_DEPT        USERS                                1024 INDEX                              1  2147483645
```

The following statement deallocates unused space from the `EMP_DEPT` cluster, keeping 30 kilobytes of unused space for future use:

```
ALTER CLUSTER EMP_DEPT DEALLOCATE UNUSED KEEP 30 K;
```

The following statement displays the metadata of the modified cluster:

```
SELECT CLUSTER_NAME, TABLESPACE_NAME, KEY_SIZE, CLUSTER_TYPE, AVG_BLOCKS_PER_KEY, MIN_EXTENTS, MAX_EXTENTS FROM USER_CLUSTERS;

CLUSTER_NAME    TABLESPACE_NAME                  KEY_SIZE CLUST AVG_BLOCKS_PER_KEY MIN_EXTENTS MAX_EXTENTS
--------------- ------------------------------ ---------- ----- ------------------ ----------- -----------
EMP_DEPT        USERS                                1024 INDEX                              1  2147483645
```