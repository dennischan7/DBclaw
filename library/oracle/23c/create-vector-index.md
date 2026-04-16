# Oracle 23c - create-vector-index
Source: https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/create-vector-index.html

Purpose

Vector indexes speed up vector searches and are either exact search indexes or approximate search indexes. An exact search gives 100% accuracy at the cost of heavy compute resources. Approximate search indexes, also called vector indexes, trade accuracy for performance.

Vectors are grouped or connected together based on similarity, where similarity is determined by their relative distance to each other. Greedy searches are done across these groups and connections to find the best, closest match to the query vector being searched for. A search using a vector index is called an approximate search.

There are two vector indexes supported in vector search: IVF (Inverted File) Flat index and HNSW (Hierarchical Navigable Small Worlds) index. IVF Flat (also simply called IVF) is a partitioned-based index, while HNSW is a graph-based index. All partition based indexes are classifed as Neighbor Partition Vector Index, and all graph-based indexes are classifed as In-Memory Neighbor Graph Vector Index.

vector\_index\_organization\_clause::=

vector\_index\_parameters\_hnsw\_clause::=

vector\_index\_parameters\_ivf\_clause::=

vector\_index\_hnsw\_replication\_clause

INCLUDE

See [Included Columns](/pls/topic/lookup?ctx=en/database/oracle/oracle-database/26/sqlrf&id=VECSE-GUID-641E6D17-6B59-4860-A5BD-DF3D33793D43) of the AI Vector Search User's Guide for semantics.

vector\_index\_parameters\_hnsw\_clause

HNSW Specific Parameters

`NEIGHBORS` and `M` are equivalent and represent the maximum number of neighbors a vector can have on any layer. The last vertex has one additional flexibility that it can have up to 2M neighbors.

`EFCONSTRUCTION` represents the maximum number of closest vector candidates considered at each step of the search during insertion.

The valid range for HNSW vector index parameters are:

* `ACCURACY`: > 0 and <= 100
* `DISTANCE`: `EUCLIDEAN`, `L2_SQUARED` (aka `EUCLIDEAN_SQUARED`), `COSINE`, `DOT`, `MANHATTAN`, `HAMMING`

  If you do not specify `DISTANCE` `metric_name`, the default metric `COSINE` is used.
* `TYPE` : `HNSW`
* `NEIGHBORS`: >= 2 and <= 2048
* `EFCONSTRUCTION`: > 0 and <= 65535

`rescore_factor` Integer between 1 and 100.

`quantization_algorithm`: uniform\_quantization

vector\_index\_parameters\_ivf\_clause

IVF Parameters

`NEIGHBOR` `PARTITIONS` determines the number of centroid partitions that are created by the index.

`SAMPLES_PER_PARTITION` decides the total number of vectors that are passed to the clustering algorithm (number of samples per partition times the number of neighbor partitions). Note, that passing all the vectors would significantly increase the total time to create the index. Instead, aim to pass a subset of vectors that can capture the data distribution.

`MIN_VECTORS_PER_PARTITION` represents the target minimum number of vectors per partition. Aim to trim out any partition that can end up with fewer than 100 vectors. This may result in lesser number of centroids. Its values can range from 0 (no trimming of centroids) to num\_vectors (would result in 1 neighbor partition).

The valid range for IVF vector index parameters are:

* `ACCURACY`: > 0 and <= 100
* `DISTANCE`: `EUCLIDEAN`, `L2_SQUARED` (aka `EUCLIDEAN_SQUARED`), `COSINE`, `DOT`, `MANHATTAN`, `HAMMING`

  If you do not specify `DISTANCE` `metric_name`, the default metric `COSINE` is used.
* `TYPE` : `IVF`
* `NEIGHBOR PARTITIONS`: >= 1 and <= 10000000
* `SAMPLES_PER_PARTITION`: from 1 to (num\_vectors/neighbor\_partitions)
* `MIN_VECTORS_PER_PARTITION`: from 0 (no trimming of centroid partitions) to total number of vectors (would result in 1 centroid partition)

QUANTIZATION Clause

* `quantization_type`: SCALAR.
* `compression_ratio` indicates by how much to compress the vectors. Acceptable values are 2,4,8.

vector\_index\_hnsw\_replication\_clause

* If neither `DUPLICATE` nor `DISTRIBUTE` clause is specified, the default is `DUPLICATE ALL`.
* Specifying `DISTRIBUTE` with no other qualifiers defaults to `DISTRIBUTE AUTO`.
* In `DISTRIBUTE AUTO` mode:
* You may specify either `DUPLICATE ALL` or `DISTRIBUTE`, but not both.

See [Manage the Different Categories of Vector Indexes](/pls/topic/lookup?ctx=en/database/oracle/oracle-database/26/sqlrf&id=VECSE-GUID-5D9B6B92-C62C-4927-9FB2-7A4437F24A19)

ONLINE

Specify `ONLINE` to rebuild `HNSW` and `IVF` indexes online. This means that the indexes can remain open for updates while they are rebuilt.

Examples

```
CREATE VECTOR INDEX galaxies_hnsw_idx ON galaxies (embedding) ORGANIZATION INMEMORY NEIGHBOR GRAPH
DISTANCE COSINE
WITH TARGET ACCURACY 95;
```

```
CREATE VECTOR INDEX galaxies_hnsw_idx ON galaxies (embedding) ORGANIZATION INMEMORY NEIGHBOR GRAPH
DISTANCE COSINE
WITH TARGET ACCURACY 90 PARAMETERS (type HNSW, neighbors 40, efconstruction 500);
```

```
CREATE VECTOR INDEX galaxies_ivf_idx ON galaxies (embedding) ORGANIZATION NEIGHBOR PARTITIONS
DISTANCE COSINE
WITH TARGET ACCURACY 95;
```

```
CREATE VECTOR INDEX galaxies_ivf_idx ON galaxies (embedding) ORGANIZATION NEIGHBOR PARTITIONS
DISTANCE COSINE
WITH TARGET ACCURACY 90 PARAMETERS (type IVF, neighbor partitions 10);
```