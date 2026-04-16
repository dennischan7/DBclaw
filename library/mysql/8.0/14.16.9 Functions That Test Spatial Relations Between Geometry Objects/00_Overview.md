---
source: MySQL 8.0 Reference
title: 00_Overview
---

The functions described in this section take two geometries as arguments and return a qualitative or quantitative relation between them.

MySQL implements two sets of functions using function names defined by the OpenGIS specification. One set tests the relationship between two geometry values using precise object shapes, the other set uses object minimum bounding rectangles (MBRs).

### **14.16.9.1 Spatial Relation Functions That Use Object Shapes**

The OpenGIS specification defines the following functions to test the relationship between two geometry values g1 and g2, using precise object shapes. The return values 1 and 0 indicate true and false, respectively, except that distance functions return distance values.

Functions in this section detect arguments in either Cartesian or geographic spatial reference systems (SRSs), and return results appropriate to the SRS.

Unless otherwise specified, functions in this section handle their geometry arguments as follows:

- If any argument is NULL or any geometry argument is an empty geometry, the return value is NULL.
- If any geometry argument is not a syntactically well-formed geometry, an [ER\\_GIS\\_INVALID\\_DATA](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_gis_invalid_data) error occurs.
- If any geometry argument is a syntactically well-formed geometry in an undefined spatial reference system (SRS), an [ER\\_SRS\\_NOT\\_FOUND](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_srs_not_found) error occurs.
- For functions that take multiple geometry arguments, if those arguments are not in the same SRS, an [ER\\_GIS\\_DIFFERENT\\_SRIDS](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_gis_different_srids) error occurs.
- If any geometry argument is geometrically invalid, either the result is true or false (it is undefined which), or an error occurs.
- For geographic SRS geometry arguments, if any argument has a longitude or latitude that is out of range, an error occurs:
  - If a longitude value is not in the range (−180, 180], an [ER\\_GEOMETRY\\_PARAM\\_LONGITUDE\\_OUT\\_OF\\_RANGE](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_geometry_param_longitude_out_of_range) error occurs ([ER\\_LONGITUDE\\_OUT\\_OF\\_RANGE](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_longitude_out_of_range) prior to MySQL 8.0.12).
  - If a latitude value is not in the range [−90, 90], an [ER\\_GEOMETRY\\_PARAM\\_LATITUDE\\_OUT\\_OF\\_RANGE](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_geometry_param_latitude_out_of_range) error occurs ([ER\\_LATITUDE\\_OUT\\_OF\\_RANGE](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_latitude_out_of_range) prior to MySQL 8.0.12).

Ranges shown are in degrees. If an SRS uses another unit, the range uses the corresponding values in its unit. The exact range limits deviate slightly due to floating-point arithmetic.

• Otherwise, the return value is non-NULL.

Some functions in this section permit a unit argument that specifies the length unit for the return value. Unless otherwise specified, functions handle their unit argument as follows:

- A unit is supported if it is found in the INFORMATION\_SCHEMA ST\_UNITS\_OF\_MEASURE table. See Section 28.3.37, "The INFORMATION\_SCHEMA ST\_UNITS\_OF\_MEASURE Table".
- If a unit is specified but not supported by MySQL, an [ER\\_UNIT\\_NOT\\_FOUND](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_unit_not_found) error occurs.
- If a supported linear unit is specified and the SRID is 0, an [ER\\_GEOMETRY\\_IN\\_UNKNOWN\\_LENGTH\\_UNIT](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_geometry_in_unknown_length_unit) error occurs.
- If a supported linear unit is specified and the SRID is not 0, the result is in that unit.

• If a unit is not specified, the result is in the unit of the SRS of the geometries, whether Cartesian or geographic. Currently, all MySQL SRSs are expressed in meters.

These object-shape functions are available for testing geometry relationships:

<span id="page-100-0"></span>• [ST\\_Contains\(](#page-100-0)g1, g2)

Returns 1 or 0 to indicate whether g1 completely contains g2 (this means that g1 and g2 must not intersect). This relationship is the inverse of that tested by [ST\\_Within\(\)](#page-104-2).

[ST\\_Contains\(\)](#page-100-0) handles its arguments as described in the introduction to this section.

```
mysql> SET @g1 = ST_GeomFromText('Polygon((0 0,0 3,3 3,3 0,0 0))'),
 -> @p1 = ST_GeomFromText('Point(1 1)'),
 -> @p2 = ST_GeomFromText('Point(3 3)'),
 -> @p3 = ST_GeomFromText('Point(5 5)');
Query OK, 0 rows affected (0.00 sec)
mysql> SELECT
 -> ST_Contains(@g1, @p1), ST_Within(@p1, @g1),
 -> ST_Disjoint(@g1, @p1), ST_Intersects(@g1, @p1)\G
*************************** 1. row ***************************
 ST_Contains(@g1, @p1): 1
 ST_Within(@p1, @g1): 1
 ST_Disjoint(@g1, @p1): 0
ST_Intersects(@g1, @p1): 1
1 row in set (0.00 sec)
mysql> SELECT
 -> ST_Contains(@g1, @p2), ST_Within(@p2, @g1),
 -> ST_Disjoint(@g1, @p2), ST_Intersects(@g1, @p2)\G
*************************** 1. row ***************************
 ST_Contains(@g1, @p2): 0
 ST_Within(@p2, @g1): 0
 ST_Disjoint(@g1, @p2): 0
ST_Intersects(@g1, @p2): 1
1 row in set (0.00 sec)
mysql> 
 -> SELECT
 -> ST_Contains(@g1, @p3), ST_Within(@p3, @g1),
 -> ST_Disjoint(@g1, @p3), ST_Intersects(@g1, @p3)\G
*************************** 1. row ***************************
 ST_Contains(@g1, @p3): 0
 ST_Within(@p3, @g1): 0
 ST_Disjoint(@g1, @p3): 1
ST_Intersects(@g1, @p3): 0
1 row in set (0.00 sec)
```

<span id="page-100-1"></span>• [ST\\_Crosses\(](#page-100-1)g1, g2)

Two geometries spatially cross if their spatial relation has the following properties:

- Unless g1 and g2 are both of dimension 1: g1 crosses g2 if the interior of g2 has points in common with the interior of g1, but g2 does not cover the entire interior of g1.
- If both g1 and g2 are of dimension 1: If the lines cross each other in a finite number of points (that is, no common line segments, only single points in common).

This function returns 1 or 0 to indicate whether g1 spatially crosses g2.

[ST\\_Crosses\(\)](#page-100-1) handles its arguments as described in the introduction to this section except that the return value is NULL for these additional conditions:

- g1 is of dimension 2 (Polygon or MultiPolygon).
- g2 is of dimension 1 (Point or MultiPoint).

<span id="page-101-0"></span>• [ST\\_Disjoint\(](#page-101-0)g1, g2)

Returns 1 or 0 to indicate whether g1 is spatially disjoint from (does not intersect) g2.

[ST\\_Disjoint\(\)](#page-101-0) handles its arguments as described in the introduction to this section.

<span id="page-101-1"></span>• [ST\\_Distance\(](#page-101-1)g1, g2 [, unit])

Returns the distance between g1 and g2, measured in the length unit of the spatial reference system (SRS) of the geometry arguments, or in the unit of the optional unit argument if that is specified.

This function processes geometry collections by returning the shortest distance among all combinations of the components of the two geometry arguments.

[ST\\_Distance\(\)](#page-101-1) handles its geometry arguments as described in the introduction to this section, with these exceptions:

- [ST\\_Distance\(\)](#page-101-1) detects arguments in a geographic (ellipsoidal) spatial reference system and returns the geodetic distance on the ellipsoid. As of MySQL 8.0.18, [ST\\_Distance\(\)](#page-101-1) supports distance calculations for geographic SRS arguments of all geometry types. Prior to MySQL 8.0.18, the only permitted geographic argument types are Point and Point, or Point and MultiPoint (in any argument order). If called with other geometry type argument combinations in a geographic SRS, an [ER\\_NOT\\_IMPLEMENTED\\_FOR\\_GEOGRAPHIC\\_SRS](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_not_implemented_for_geographic_srs) error occurs.
- If any argument is geometrically invalid, either the result is an undefined distance (that is, it can be any number), or an error occurs.
- If an intermediate or final result produces NaN or a negative number, an [ER\\_GIS\\_INVALID\\_DATA](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_gis_invalid_data) error occurs.

As of MySQL 8.0.14, [ST\\_Distance\(\)](#page-101-1) permits an optional unit argument that specifies the linear unit for the returned distance value. [ST\\_Distance\(\)](#page-101-1) handles its unit argument as described in the introduction to this section.

```
mysql> SET @g1 = ST_GeomFromText('POINT(1 1)');
mysql> SET @g2 = ST_GeomFromText('POINT(2 2)');
mysql> SELECT ST_Distance(@g1, @g2);
+-----------------------+
| ST_Distance(@g1, @g2) |
+-----------------------+
| 1.4142135623730951 |
+-----------------------+
mysql> SET @g1 = ST_GeomFromText('POINT(1 1)', 4326);
mysql> SET @g2 = ST_GeomFromText('POINT(2 2)', 4326);
mysql> SELECT ST_Distance(@g1, @g2);
+-----------------------+
| ST_Distance(@g1, @g2) |
+-----------------------+
| 156874.3859490455 |
+-----------------------+
mysql> SELECT ST_Distance(@g1, @g2, 'metre');
+--------------------------------+
| ST_Distance(@g1, @g2, 'metre') |
+--------------------------------+
| 156874.3859490455 |
+--------------------------------+
mysql> SELECT ST_Distance(@g1, @g2, 'foot');
+-------------------------------+
| ST_Distance(@g1, @g2, 'foot') |
+-------------------------------+
| 514679.7439273146 |
+-------------------------------+
```

For the special case of distance calculations on a sphere, see the [ST\\_Distance\\_Sphere\(\)](#page-115-0) function.

<span id="page-102-0"></span>• [ST\\_Equals\(](#page-102-0)g1, g2)

Returns 1 or 0 to indicate whether g1 is spatially equal to g2.

[ST\\_Equals\(\)](#page-102-0) handles its arguments as described in the introduction to this section, except that it does not return NULL for empty geometry arguments.

```
mysql> SET @g1 = Point(1,1), @g2 = Point(2,2);
mysql> SELECT ST_Equals(@g1, @g1), ST_Equals(@g1, @g2);
+---------------------+---------------------+
| ST_Equals(@g1, @g1) | ST_Equals(@g1, @g2) |
+---------------------+---------------------+
| 1 | 0 |
+---------------------+---------------------+
```

<span id="page-102-1"></span>• [ST\\_FrechetDistance\(](#page-102-1)g1, g2 [, unit])

Returns the discrete Fréchet distance between two geometries, reflecting how similar the geometries are. The result is a double-precision number measured in the length unit of the spatial reference system (SRS) of the geometry arguments, or in the length unit of the unit argument if that argument is given.

This function implements the discrete Fréchet distance, which means it is restricted to distances between the points of the geometries. For example, given two LineString arguments, only the points explicitly mentioned in the geometries are considered. Points on the line segments between these points are not considered.

[ST\\_FrechetDistance\(\)](#page-102-1) handles its geometry arguments as described in the introduction to this section, with these exceptions:

• The geometries may have a Cartesian or geographic SRS, but only LineString values are supported. If the arguments are in the same Cartesian or geographic SRS, but either is not a LineString, an [ER\\_NOT\\_IMPLEMENTED\\_FOR\\_CARTESIAN\\_SRS](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_not_implemented_for_cartesian_srs) or [ER\\_NOT\\_IMPLEMENTED\\_FOR\\_GEOGRAPHIC\\_SRS](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_not_implemented_for_geographic_srs) error occurs, depending on the SRS type.

[ST\\_FrechetDistance\(\)](#page-102-1) handles its optional unit argument as described in the introduction to this section.

```
mysql> SET @ls1 = ST_GeomFromText('LINESTRING(0 0,0 5,5 5)');
mysql> SET @ls2 = ST_GeomFromText('LINESTRING(0 1,0 6,3 3,5 6)');
mysql> SELECT ST_FrechetDistance(@ls1, @ls2);
+--------------------------------+
| ST_FrechetDistance(@ls1, @ls2) |
+--------------------------------+
| 2.8284271247461903 |
+--------------------------------+
mysql> SET @ls1 = ST_GeomFromText('LINESTRING(0 0,0 5,5 5)', 4326);
mysql> SET @ls2 = ST_GeomFromText('LINESTRING(0 1,0 6,3 3,5 6)', 4326);
mysql> SELECT ST_FrechetDistance(@ls1, @ls2);
+--------------------------------+
| ST_FrechetDistance(@ls1, @ls2) |
+--------------------------------+
| 313421.1999416798 |
+--------------------------------+
mysql> SELECT ST_FrechetDistance(@ls1, @ls2, 'foot');
+----------------------------------------+
| ST_FrechetDistance(@ls1, @ls2, 'foot') |
+----------------------------------------+
| 1028284.7767115477 |
+----------------------------------------+
```

This function was added in MySQL 8.0.23.

<span id="page-103-0"></span>• [ST\\_HausdorffDistance\(](#page-103-0)g1, g2 [, unit])

Returns the discrete Hausdorff distance between two geometries, reflecting how similar the geometries are. The result is a double-precision number measured in the length unit of the spatial reference system (SRS) of the geometry arguments, or in the length unit of the unit argument if that argument is given.

This function implements the discrete Hausdorff distance, which means it is restricted to distances between the points of the geometries. For example, given two LineString arguments, only the points explicitly mentioned in the geometries are considered. Points on the line segments between these points are not considered.

[ST\\_HausdorffDistance\(\)](#page-103-0) handles its geometry arguments as described in the introduction to this section, with these exceptions:

- If the geometry arguments are in the same Cartesian or geographic SRS, but are not in a supported combination, an [ER\\_NOT\\_IMPLEMENTED\\_FOR\\_CARTESIAN\\_SRS](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_not_implemented_for_cartesian_srs) or [ER\\_NOT\\_IMPLEMENTED\\_FOR\\_GEOGRAPHIC\\_SRS](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_not_implemented_for_geographic_srs) error occurs, depending on the SRS type. These combinations are supported:
  - LineString and LineString
  - Point and MultiPoint
  - LineString and MultiLineString
  - MultiPoint and MultiPoint
  - MultiLineString and MultiLineString

[ST\\_HausdorffDistance\(\)](#page-103-0) handles its optional unit argument as described in the introduction to this section.

```
mysql> SET @ls1 = ST_GeomFromText('LINESTRING(0 0,0 5,5 5)');
mysql> SET @ls2 = ST_GeomFromText('LINESTRING(0 1,0 6,3 3,5 6)');
mysql> SELECT ST_HausdorffDistance(@ls1, @ls2);
+----------------------------------+
| ST_HausdorffDistance(@ls1, @ls2) |
+----------------------------------+
| 1 |
+----------------------------------+
mysql> SET @ls1 = ST_GeomFromText('LINESTRING(0 0,0 5,5 5)', 4326);
mysql> SET @ls2 = ST_GeomFromText('LINESTRING(0 1,0 6,3 3,5 6)', 4326);
mysql> SELECT ST_HausdorffDistance(@ls1, @ls2);
+----------------------------------+
| ST_HausdorffDistance(@ls1, @ls2) |
+----------------------------------+
| 111319.49079326246 |
+----------------------------------+
mysql> SELECT ST_HausdorffDistance(@ls1, @ls2, 'foot');
+------------------------------------------+
| ST_HausdorffDistance(@ls1, @ls2, 'foot') |
+------------------------------------------+
| 365221.4264870815 |
+------------------------------------------+
```

This function was added in MySQL 8.0.23.

<span id="page-103-1"></span>• [ST\\_Intersects\(](#page-103-1)g1, g2)

Returns 1 or 0 to indicate whether g1 spatially intersects g2.

[ST\\_Intersects\(\)](#page-103-1) handles its arguments as described in the introduction to this section.

<span id="page-104-0"></span>• [ST\\_Overlaps\(](#page-104-0)g1, g2)

Two geometries spatially overlap if they intersect and their intersection results in a geometry of the same dimension but not equal to either of the given geometries.

This function returns 1 or 0 to indicate whether g1 spatially overlaps g2.

[ST\\_Overlaps\(\)](#page-104-0) handles its arguments as described in the introduction to this section except that the return value is NULL for the additional condition that the dimensions of the two geometries are not equal.

<span id="page-104-1"></span>• [ST\\_Touches\(](#page-104-1)g1, g2)

Two geometries spatially touch if their interiors do not intersect, but the boundary of one of the geometries intersects either the boundary or the interior of the other.

This function returns 1 or 0 to indicate whether g1 spatially touches g2.

[ST\\_Touches\(\)](#page-104-1) handles its arguments as described in the introduction to this section except that the return value is NULL for the additional condition that both geometries are of dimension 0 (Point or MultiPoint).

<span id="page-104-2"></span>• [ST\\_Within\(](#page-104-2)g1, g2)

Returns 1 or 0 to indicate whether g1 is spatially within g2. This tests the opposite relationship as [ST\\_Contains\(\)](#page-100-0).

[ST\\_Within\(\)](#page-104-2) handles its arguments as described in the introduction to this section.

### **14.16.9.2 Spatial Relation Functions That Use Minimum Bounding Rectangles**

MySQL provides several MySQL-specific functions that test the relationship between minimum bounding rectangles (MBRs) of two geometries g1 and g2. The return values 1 and 0 indicate true and false, respectively.

The bounding box of a point is interpreted as a point that is both boundary and interior.

The bounding box of a straight horizontal or vertical line is interpreted as a line where the interior of the line is also boundary. The endpoints are boundary points.

If any of the parameters are geometry collections, the interior, boundary, and exterior of those parameters are those of the union of all elements in the collection.

Functions in this section detect arguments in either Cartesian or geographic spatial reference systems (SRSs), and return results appropriate to the SRS.

Unless otherwise specified, functions in this section handle their geometry arguments as follows:

- If any argument is NULL or an empty geometry, the return value is NULL.
- If any geometry argument is not a syntactically well-formed geometry, an [ER\\_GIS\\_INVALID\\_DATA](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_gis_invalid_data) error occurs.
- If any geometry argument is a syntactically well-formed geometry in an undefined spatial reference system (SRS), an [ER\\_SRS\\_NOT\\_FOUND](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_srs_not_found) error occurs.
- For functions that take multiple geometry arguments, if those arguments are not in the same SRS, an [ER\\_GIS\\_DIFFERENT\\_SRIDS](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_gis_different_srids) error occurs.
- If any argument is geometrically invalid, either the result is true or false (it is undefined which), or an error occurs.

- For geographic SRS geometry arguments, if any argument has a longitude or latitude that is out of range, an error occurs:
  - If a longitude value is not in the range (−180, 180], an [ER\\_GEOMETRY\\_PARAM\\_LONGITUDE\\_OUT\\_OF\\_RANGE](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_geometry_param_longitude_out_of_range) error occurs ([ER\\_LONGITUDE\\_OUT\\_OF\\_RANGE](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_longitude_out_of_range) prior to MySQL 8.0.12).
  - If a latitude value is not in the range [−90, 90], an [ER\\_GEOMETRY\\_PARAM\\_LATITUDE\\_OUT\\_OF\\_RANGE](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_geometry_param_latitude_out_of_range) error occurs ([ER\\_LATITUDE\\_OUT\\_OF\\_RANGE](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_latitude_out_of_range) prior to MySQL 8.0.12).

Ranges shown are in degrees. If an SRS uses another unit, the range uses the corresponding values in its unit. The exact range limits deviate slightly due to floating-point arithmetic.

• Otherwise, the return value is non-NULL.

These MBR functions are available for testing geometry relationships:

<span id="page-105-0"></span>• [MBRContains\(](#page-105-0)g1, g2)

Returns 1 or 0 to indicate whether the minimum bounding rectangle of g1 contains the minimum bounding rectangle of g2. This tests the opposite relationship as [MBRWithin\(\)](#page-108-2).

[MBRContains\(\)](#page-105-0) handles its arguments as described in the introduction to this section.

```
mysql> SET
 -> @g1 = ST_GeomFromText('Polygon((0 0,0 3,3 3,3 0,0 0))'),
 -> @g2 = ST_GeomFromText('Polygon((1 1,1 2,2 2,2 1,1 1))'),
 -> @g3 = ST_GeomFromText('Polygon((0 0,0 5,5 5,5 0,0 0))'),
 -> @g4 = ST_GeomFromText('Polygon((5 5,5 10,10 10,10 5,5 5))'),
 -> @p1 = ST_GeomFromText('Point(1 1)'),
 -> @p2 = ST_GeomFromText('Point(3 3)');
 -> @p3 = ST_GeomFromText('Point(5 5)');
Query OK, 0 rows affected (0.00 sec)
mysql> SELECT
 -> MBRContains(@g1, @g2), MBRContains(@g1, @g4),
 -> MBRContains(@g2, @g1), MBRContains(@g2, @g4),
 -> MBRContains(@g2, @g3), MBRContains(@g3, @g4),
 -> MBRContains(@g3, @g1), MBRContains(@g1, @g3),
 -> MBRContains(@g1, @p1), MBRContains(@p1, @g1),
 -> MBRContains(@g1, @p1), MBRContains(@p1, @g1),
 -> MBRContains(@g2, @p2), MBRContains(@g2, @p3),
 -> MBRContains(@g3, @p1), MBRContains(@g3, @p2),
 -> MBRContains(@g3, @p3), MBRContains(@g4, @p1),
 -> MBRContains(@g4, @p2), MBRContains(@g4, @p3)\G
*************************** 1. row ***************************
MBRContains(@g1, @g2): 1
MBRContains(@g1, @g4): 0
MBRContains(@g2, @g1): 0
MBRContains(@g2, @g4): 0
MBRContains(@g2, @g3): 0
MBRContains(@g3, @g4): 0
MBRContains(@g3, @g1): 1
MBRContains(@g1, @g3): 0
MBRContains(@g1, @p1): 1
MBRContains(@p1, @g1): 0
MBRContains(@g1, @p1): 1
MBRContains(@p1, @g1): 0
MBRContains(@g2, @p2): 0
MBRContains(@g2, @p3): 0
MBRContains(@g3, @p1): 1
MBRContains(@g3, @p2): 1
MBRContains(@g3, @p3): 0
MBRContains(@g4, @p1): 0
MBRContains(@g4, @p2): 0
MBRContains(@g4, @p3): 0
1 row in set (0.00 sec)
```

<span id="page-106-0"></span>• [MBRCoveredBy\(](#page-106-0)g1, g2)

Returns 1 or 0 to indicate whether the minimum bounding rectangle of g1 is covered by the minimum bounding rectangle of g2. This tests the opposite relationship as [MBRCovers\(\)](#page-106-1).

[MBRCoveredBy\(\)](#page-106-0) handles its arguments as described in the introduction to this section.

```
mysql> SET @g1 = ST_GeomFromText('Polygon((0 0,0 3,3 3,3 0,0 0))');
mysql> SET @g2 = ST_GeomFromText('Point(1 1)');
mysql> SELECT MBRCovers(@g1,@g2), MBRCoveredby(@g1,@g2);
+--------------------+-----------------------+
| MBRCovers(@g1,@g2) | MBRCoveredby(@g1,@g2) |
+--------------------+-----------------------+
| 1 | 0 |
+--------------------+-----------------------+
mysql> SELECT MBRCovers(@g2,@g1), MBRCoveredby(@g2,@g1);
+--------------------+-----------------------+
| MBRCovers(@g2,@g1) | MBRCoveredby(@g2,@g1) |
+--------------------+-----------------------+
| 0 | 1 |
+--------------------+-----------------------+
```

See the description of the [MBRCovers\(\)](#page-106-1) function for additional examples.

<span id="page-106-1"></span>• [MBRCovers\(](#page-106-1)g1, g2)

Returns 1 or 0 to indicate whether the minimum bounding rectangle of g1 covers the minimum bounding rectangle of g2. This tests the opposite relationship as [MBRCoveredBy\(\)](#page-106-0). See the description of [MBRCoveredBy\(\)](#page-106-0) for additional examples.

[MBRCovers\(\)](#page-106-1) handles its arguments as described in the introduction to this section.

```
mysql> SET
 -> @g1 = ST_GeomFromText('Polygon((0 0,0 3,3 3,3 0,0 0))'),
 -> @g2 = ST_GeomFromText('Polygon((1 1,1 2,2 2,2 1,1 1))'),
 -> @p1 = ST_GeomFromText('Point(1 1)'),
 -> @p2 = ST_GeomFromText('Point(3 3)'),
 -> @p3 = ST_GeomFromText('Point(5 5)');
Query OK, 0 rows affected (0.02 sec)
mysql> SELECT
 -> MBRCovers(@g1, @p1), MBRCovers(@g1, @p2),
 -> MBRCovers(@g1, @g2), MBRCovers(@g1, @p3)\G
*************************** 1. row ***************************
MBRCovers(@g1, @p1): 1
MBRCovers(@g1, @p2): 1
MBRCovers(@g1, @g2): 1
MBRCovers(@g1, @p3): 0
1 row in set (0.00 sec)
```

<span id="page-106-2"></span>• [MBRDisjoint\(](#page-106-2)g1, g2)

Returns 1 or 0 to indicate whether the minimum bounding rectangles of the two geometries g1 and g2 are disjoint (do not intersect).

[MBRDisjoint\(\)](#page-106-2) handles its arguments as described in the introduction to this section.

```
mysql> SET
 -> @g1 = ST_GeomFromText('Polygon((0 0,0 3,3 3,3 0,0 0))'),
 -> @g2 = ST_GeomFromText('Polygon((1 1,1 2,2 2,2 1,1 1))'),
 -> @g3 = ST_GeomFromText('Polygon((0 0,0 5,5 5,5 0,0 0))'),
 -> @g4 = ST_GeomFromText('Polygon((5 5,5 10,10 10,10 5,5 5))'),
 -> @p1 = ST_GeomFromText('Point(1 1)'),
 -> @p2 = ST_GeomFromText('Point(3 3)'),
 -> @p3 = ST_GeomFromText('Point(5 5)');
Query OK, 0 rows affected (0.00 sec)
mysql> SELECT
 -> MBRDisjoint(@g1, @g4), MBRDisjoint(@g2, @g4),
```

```
 -> MBRDisjoint(@g3, @g4), MBRDisjoint(@g4, @g4),
 -> MBRDisjoint(@g1, @p1), MBRDisjoint(@g1, @p2),
 -> MBRDisjoint(@g1, @p3)\G
*************************** 1. row ***************************
MBRDisjoint(@g1, @g4): 1
MBRDisjoint(@g2, @g4): 1
MBRDisjoint(@g3, @g4): 0
MBRDisjoint(@g4, @g4): 0
MBRDisjoint(@g1, @p1): 0
MBRDisjoint(@g1, @p2): 0
MBRDisjoint(@g1, @p3): 1
1 row in set (0.00 sec)
```

<span id="page-107-0"></span>• [MBREquals\(](#page-107-0)g1, g2)

Returns 1 or 0 to indicate whether the minimum bounding rectangles of the two geometries g1 and g2 are the same.

[MBREquals\(\)](#page-107-0) handles its arguments as described in the introduction to this section, except that it does not return NULL for empty geometry arguments.

```
mysql> SET
 -> @g1 = ST_GeomFromText('Polygon((0 0,0 3,3 3,3 0,0 0))'),
 -> @g2 = ST_GeomFromText('Polygon((1 1,1 2,2 2,2 1,1 1))'),
 -> @p1 = ST_GeomFromText('Point(1 1)'),
 -> @p2 = ST_GeomFromText('Point(3 3)'),
 -> @p3 = ST_GeomFromText('Point(5 5)');
Query OK, 0 rows affected (0.00 sec)
mysql> SELECT
 -> MBREquals(@g1, @g1), MBREquals(@g1, @g2),
 -> MBREquals(@g1, @p1), MBREquals(@g1, @p2), MBREquals(@g2, @g2),
 -> MBREquals(@p1, @p1), MBREquals(@p1, @p2), MBREquals(@p2, @p2)\G
*************************** 1. row ***************************
MBREquals(@g1, @g1): 1
MBREquals(@g1, @g2): 0
MBREquals(@g1, @p1): 0
MBREquals(@g1, @p2): 0
MBREquals(@g2, @g2): 1
MBREquals(@p1, @p1): 1
MBREquals(@p1, @p2): 0
MBREquals(@p2, @p2): 1
1 row in set (0.00 sec)
```

<span id="page-107-1"></span>• [MBRIntersects\(](#page-107-1)g1, g2)

Returns 1 or 0 to indicate whether the minimum bounding rectangles of the two geometries g1 and g2 intersect.

[MBRIntersects\(\)](#page-107-1) handles its arguments as described in the introduction to this section.

```
mysql> SET
 -> @g1 = ST_GeomFromText('Polygon((0 0,0 3,3 3,3 0,0 0))'),
 -> @g2 = ST_GeomFromText('Polygon((1 1,1 2,2 2,2 1,1 1))'),
 -> @g3 = ST_GeomFromText('Polygon((0 0,0 5,5 5,5 0,0 0))'),
 -> @g4 = ST_GeomFromText('Polygon((5 5,5 10,10 10,10 5,5 5))'),
 -> @g5 = ST_GeomFromText('Polygon((2 2,2 8,8 8,8 2,2 2))'),
 -> @p1 = ST_GeomFromText('Point(1 1)'),
 -> @p2 = ST_GeomFromText('Point(3 3)'),
 -> @p3 = ST_GeomFromText('Point(5 5)');
Query OK, 0 rows affected (0.00 sec)
mysql> SELECT
 -> MBRIntersects(@g1, @g1), MBRIntersects(@g1, @g2),
 -> MBRIntersects(@g1, @g3), MBRIntersects(@g1, @g4), MBRIntersects(@g1, @g5), 
 -> MBRIntersects(@g1, @p1), MBRIntersects(@g1, @p2), MBRIntersects(@g1, @p3), 
 -> MBRIntersects(@g2, @p1), MBRIntersects(@g2, @p2), MBRIntersects(@g2, @p3)\G
*************************** 1. row ***************************
MBRIntersects(@g1, @g1): 1
MBRIntersects(@g1, @g2): 1
```

```
MBRIntersects(@g1, @g3): 1
MBRIntersects(@g1, @g4): 0
MBRIntersects(@g1, @g5): 1
MBRIntersects(@g1, @p1): 1
MBRIntersects(@g1, @p2): 1
MBRIntersects(@g1, @p3): 0
MBRIntersects(@g2, @p1): 1
MBRIntersects(@g2, @p2): 0
MBRIntersects(@g2, @p3): 0
1 row in set (0.00 sec)
```

<span id="page-108-0"></span>• [MBROverlaps\(](#page-108-0)g1, g2)

Two geometries spatially overlap if they intersect and their intersection results in a geometry of the same dimension but not equal to either of the given geometries.

This function returns 1 or 0 to indicate whether the minimum bounding rectangles of the two geometries g1 and g2 overlap.

[MBROverlaps\(\)](#page-108-0) handles its arguments as described in the introduction to this section.

<span id="page-108-1"></span>• [MBRTouches\(](#page-108-1)g1, g2)

Two geometries spatially touch if their interiors do not intersect, but the boundary of one of the geometries intersects either the boundary or the interior of the other.

This function returns 1 or 0 to indicate whether the minimum bounding rectangles of the two geometries g1 and g2 touch.

[MBRTouches\(\)](#page-108-1) handles its arguments as described in the introduction to this section.

<span id="page-108-2"></span>• [MBRWithin\(](#page-108-2)g1, g2)

Returns 1 or 0 to indicate whether the minimum bounding rectangle of g1 is within the minimum bounding rectangle of g2. This tests the opposite relationship as [MBRContains\(\)](#page-105-0).

[MBRWithin\(\)](#page-108-2) handles its arguments as described in the introduction to this section.

```
mysql> SET
 -> @g1 = ST_GeomFromText('Polygon((0 0,0 3,3 3,3 0,0 0))'),
 -> @g2 = ST_GeomFromText('Polygon((1 1,1 2,2 2,2 1,1 1))'),
 -> @g3 = ST_GeomFromText('Polygon((0 0,0 5,5 5,5 0,0 0))'),
 -> @g4 = ST_GeomFromText('Polygon((5 5,5 10,10 10,10 5,5 5))'),
 -> @p1 = ST_GeomFromText('Point(1 1)'),
 -> @p2 = ST_GeomFromText('Point(3 3)');
 -> @p3 = ST_GeomFromText('Point(5 5)');
Query OK, 0 rows affected (0.00 sec)
mysql> SELECT
 -> MBRWithin(@g1, @g2), MBRWithin(@g1, @g4),
 -> MBRWithin(@g2, @g1), MBRWithin(@g2, @g4),
 -> MBRWithin(@g2, @g3), MBRWithin(@g3, @g4),
 -> MBRWithin(@g1, @p1), MBRWithin(@p1, @g1),
 -> MBRWithin(@g1, @p1), MBRWithin(@p1, @g1),
 -> MBRWithin(@g2, @p2), MBRWithin(@g2, @p3)\G
*************************** 1. row ***************************
MBRWithin(@g1, @g2): 0
MBRWithin(@g1, @g4): 0
MBRWithin(@g2, @g1): 1
MBRWithin(@g2, @g4): 0
MBRWithin(@g2, @g3): 1
MBRWithin(@g3, @g4): 0
MBRWithin(@g1, @p1): 0
MBRWithin(@p1, @g1): 1
MBRWithin(@g1, @p1): 0
MBRWithin(@p1, @g1): 1
MBRWithin(@g2, @p2): 0
MBRWithin(@g2, @p3): 0
```

```
1 row in set (0.00 sec)
```