---
source: PostgreSQL 14 Reference
title: 00_Overview
---

Geometric data types represent two-dimensional spatial objects. [Table 8.20](#page-4-0) shows the geometric types available in PostgreSQL.

<span id="page-4-0"></span>**Table 8.20. Geometric Types**

| Name    | Storage Size | Description                      | Representation                         |
|---------|--------------|----------------------------------|----------------------------------------|
| point   | 16 bytes     | Point on a plane                 | (x,y)                                  |
| line    | 24 bytes     | Infinite line                    | {A,B,C}                                |
| lseg    | 32 bytes     | Finite line segment              | ((x1,y1),(x2,y2))                      |
| box     | 32 bytes     | Rectangular box                  | ((x1,y1),(x2,y2))                      |
| path    | 16+16n bytes | Closed path (similar to polygon) | ((x1,y1),)                             |
| path    | 16+16n bytes | Open path                        | [(x1,y1),]                             |
| polygon | 40+16n bytes | Polygon (similar to closed path) | ((x1,y1),)                             |
| circle  | 24 bytes     | Circle                           | <(x,y),r> (center<br>point and radius) |

In all these types, the individual coordinates are stored as double precision (float8) numbers.

A rich set of functions and operators is available to perform various geometric operations such as scaling, translation, rotation, and determining intersections. They are explained in [Section 9.11](#page-121-0).