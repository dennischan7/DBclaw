---
source: PostgreSQL 15 Reference
title: 00_Overview
---

#### 69.1. Introduction

SP-GiST is an abbreviation for space-partitioned GiST. SP-GiST supports partitioned search trees, which facilitate development of a wide range of different non-balanced data structures, such as quadtrees, k-d trees, and radix trees (tries). The common feature of these structures is that they repeatedly divide the search space into partitions that need not be of equal size. Searches that are well matched to the partitioning rule can be very fast.

These popular data structures were originally developed for in-memory usage. In main memory, they are usually designed as a set of dynamically allocated nodes linked by pointers. This is not suitable for direct storing on disk, since these chains of pointers can be rather long which would require too many disk accesses. In contrast, disk-based data structures should have a high fanout to minimize I/O. The challenge addressed by SP-GiST is to map search tree nodes to disk pages in such a way that a search need access only a few disk pages, even if it traverses many nodes.

Like GiST, SP-GiST is meant to allow the development of custom data types with the appropriate access methods, by an expert in the domain of the data type, rather than a database expert.

Some of the information here is derived from Purdue University's SP-GiST Indexing Project web site<sup>1</sup>. The SP-GiST implementation in PostgreSQL is primarily maintained by Teodor Sigaev and Oleg Bartunov, and there is more information on their web site<sup>2</sup>.

## <span id="page-75-0"></span>69.2. Built-in Operator Classes

The core PostgreSQL distribution includes the SP-GiST operator classes shown in Table 69.1.

Table 69.1. Built-in SP-GiST Operator Classes

| Name     | Indexable Operators        | Ordering Operators |
|----------|----------------------------|--------------------|
|          | << (box,box)               |                    |
|          | &< (box,box)               |                    |
|          | &> (box,box)               |                    |
|          | >> (box,box)               |                    |
|          | <@ (box,box)               |                    |
| how one  | <pre>@&gt; (box,box)</pre> | <-> (box,point)    |
| box_ops  | ~= (box,box)               | (DOX, POINC)       |
|          | && (box,box)               |                    |
|          | <<  (box,box)              |                    |
|          | &<  (box,box)              |                    |
|          | &> (box,box)               |                    |
|          | >> (box,box)               |                    |
|          | << (inet,inet)             |                    |
|          | <<= (inet,inet)            |                    |
| inet_ops | >> (inet,inet)             |                    |
|          | >>= (inet,inet)            |                    |
|          | = (inet,inet)              |                    |

<sup>1</sup> https://www.cs.purdue.edu/spgist/

<sup>2</sup> http://www.sai.msu.su/~megera/wiki/spgist\_dev

| Name           | Indexable Operators          | Ordering Operators  |
|----------------|------------------------------|---------------------|
|                | <> (inet,inet)               |                     |
|                | < (inet,inet)                |                     |
|                | <= (inet,inet)               |                     |
|                | > (inet,inet)                |                     |
|                | >= (inet,inet)               |                     |
|                | && (inet,inet)               |                     |
|                | >> (point,point)             |                     |
|                | << (point,point)             |                     |
|                | >> (point,point)             |                     |
| kd_point_ops   | <<  (point,point)            | <-> (point,point)   |
|                | ~= (point,point)             |                     |
|                | <@ (point,box)               |                     |
|                | << (polygon,polygon)         |                     |
|                | &< (polygon,polygon)         |                     |
|                | &> (polygon,polygon)         |                     |
|                | >> (polygon,polygon)         |                     |
|                | <@ (polygon,polygon)         |                     |
|                | @> (polygon,polygon)         |                     |
| poly_ops       | ~= (polygon,polygon)         | <-> (polygon,point) |
|                | && (polygon,polygon)         |                     |
|                | <<  (polygon,polygon)        |                     |
|                | &<  (polygon,polygon)        |                     |
|                | >> (polygon,polygon)         |                     |
|                | &> (polygon,polygon)         |                     |
|                | >> (point,point)             |                     |
|                | << (point,point)             |                     |
| quad_point_ops | >> (point,point)             | <-> (point,point)   |
|                | <<  (point,point)            |                     |
|                | ~= (point,point)             |                     |
|                | <@ (point,box)               |                     |
|                | = (anyrange,anyrange)        |                     |
|                | &&<br>(anyrange,anyrange)    |                     |
|                | @> (anyrange,anyele<br>ment) |                     |
| range_ops      | @><br>(anyrange,anyrange)    |                     |
|                | <@<br>(anyrange,anyrange)    |                     |
|                | <<<br>(anyrange,anyrange)    |                     |

| Name     | Indexable Operators | Ordering Operators |
|----------|---------------------|--------------------|
|          | >>                  |                    |
|          | (anyrange,anyrange) |                    |
|          | &<                  |                    |
|          | (anyrange,anyrange) |                    |
|          | &>                  |                    |
|          | (anyrange,anyrange) |                    |
|          | - -                 |                    |
|          | (anyrange,anyrange) |                    |
|          | = (text,text)       |                    |
|          | < (text,text)       |                    |
|          | <= (text,text)      |                    |
|          | > (text,text)       |                    |
| text_ops | >= (text,text)      |                    |
|          | ~<~ (text,text)     |                    |
|          | ~<=~ (text,text)    |                    |
|          | ~>=~ (text,text)    |                    |
|          | ~>~ (text,text)     |                    |
|          | ^@ (text,text)      |                    |

Of the two operator classes for type point, quad\_point\_ops is the default. kd\_point\_ops supports the same operators but uses a different index data structure that may offer better performance in some applications.

The quad\_point\_ops, kd\_point\_ops and poly\_ops operator classes support the <-> ordering operator, which enables the k-nearest neighbor (k-NN) search over indexed point or polygon data sets.