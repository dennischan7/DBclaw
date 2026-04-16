---
source: MySQL 8.0 Reference
title: 00_Overview
---

OpenGIS proposes a number of functions that can produce geometries. They are designed to implement spatial operators. These functions support all argument type combinations except those that are inapplicable according to the [Open Geospatial Consortium](http://www.opengeospatial.org) specification.

MySQL also implements certain functions that are extensions to OpenGIS, as noted in the function descriptions. In addition, [Section 14.16.7, "Geometry Property Functions",](#page-79-2) discusses several functions that construct new geometries from existing ones. See that section for descriptions of these functions:

```
• ST_Envelope(g)
```

- [ST\\_StartPoint\(](#page-87-2)ls)
- [ST\\_EndPoint\(](#page-84-0)ls)
- [ST\\_PointN\(](#page-87-1)ls, N)
- [ST\\_ExteriorRing\(](#page-90-0)poly)
- [ST\\_InteriorRingN\(](#page-90-2)poly, N)
- [ST\\_GeometryN\(](#page-90-1)gc, N)

Unless otherwise specified, functions in this section handle their geometry arguments as follows:

- If any argument is NULL, the return value is NULL.
- If any geometry argument is not a syntactically well-formed geometry, an [ER\\_GIS\\_INVALID\\_DATA](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_gis_invalid_data) error occurs.
- If any geometry argument is a syntactically well-formed geometry in an undefined spatial reference system (SRS), an [ER\\_SRS\\_NOT\\_FOUND](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_srs_not_found) error occurs.
- For functions that take multiple geometry arguments, if those arguments are not in the same SRS, an [ER\\_GIS\\_DIFFERENT\\_SRIDS](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_gis_different_srids) error occurs.

- If any geometry argument has an SRID value for a geographic SRS and the function does not handle geographic geometries, an [ER\\_NOT\\_IMPLEMENTED\\_FOR\\_GEOGRAPHIC\\_SRS](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_not_implemented_for_geographic_srs) error occurs.
- For geographic SRS geometry arguments, if any argument has a longitude or latitude that is out of range, an error occurs:
  - If a longitude value is not in the range (−180, 180], an [ER\\_GEOMETRY\\_PARAM\\_LONGITUDE\\_OUT\\_OF\\_RANGE](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_geometry_param_longitude_out_of_range) error occurs ([ER\\_LONGITUDE\\_OUT\\_OF\\_RANGE](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_longitude_out_of_range) prior to MySQL 8.0.12).
  - If a latitude value is not in the range [−90, 90], an [ER\\_GEOMETRY\\_PARAM\\_LATITUDE\\_OUT\\_OF\\_RANGE](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_geometry_param_latitude_out_of_range) error occurs ([ER\\_LATITUDE\\_OUT\\_OF\\_RANGE](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_latitude_out_of_range) prior to MySQL 8.0.12).

Ranges shown are in degrees. If an SRS uses another unit, the range uses the corresponding values in its unit. The exact range limits deviate slightly due to floating-point arithmetic.

• Otherwise, the return value is non-NULL.

These spatial operator functions are available:

```
• ST_Buffer(g, d [, strategy1 [, strategy2 [, strategy3]]])
```

Returns a geometry that represents all points whose distance from the geometry value g is less than or equal to a distance of d. The result is in the same SRS as the geometry argument.

If the geometry argument is empty, [ST\\_Buffer\(\)](#page-92-0) returns an empty geometry.

If the distance is 0, [ST\\_Buffer\(\)](#page-92-0) returns the geometry argument unchanged:

```
mysql> SET @pt = ST_GeomFromText('POINT(0 0)');
mysql> SELECT ST_AsText(ST_Buffer(@pt, 0));
+------------------------------+
| ST_AsText(ST_Buffer(@pt, 0)) |
+------------------------------+
| POINT(0 0) |
+------------------------------+
```

If the geometry argument is in a Cartesian SRS:

- [ST\\_Buffer\(\)](#page-92-0) supports negative distances for Polygon and MultiPolygon values, and for geometry collections containing Polygon or MultiPolygon values.
- If the result is reduced so much that it disappears, the result is an empty geometry.
- An [ER\\_WRONG\\_ARGUMENTS](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_wrong_arguments) error occurs for [ST\\_Buffer\(\)](#page-92-0) with a negative distance for Point, MultiPoint, LineString, and MultiLineString values, and for geometry collections not containing any Polygon or MultiPolygon values.

If the geometry argument is in a geographic SRS:

- Prior to MySQL 8.0.26, an [ER\\_NOT\\_IMPLEMENTED\\_FOR\\_GEOGRAPHIC\\_SRS](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_not_implemented_for_geographic_srs) error occurs.
- As of MySQL 8.0.26, Point geometries in a geographic SRS are permitted. For non-Point geometries, an [ER\\_NOT\\_IMPLEMENTED\\_FOR\\_GEOGRAPHIC\\_SRS](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_not_implemented_for_geographic_srs) error still occurs.

For MySQL versions that permit geographic Point geometries:

• If the distance is not negative and no strategies are specified, the function returns the geographic buffer of the Point in its SRS. The distance argument must be in the SRS distance unit (currently always meters).

• If the distance is negative or any strategy (except NULL) is specified, an [ER\\_WRONG\\_ARGUMENTS](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_wrong_arguments) error occurs.

[ST\\_Buffer\(\)](#page-92-0) permits up to three optional strategy arguments following the distance argument. Strategies influence buffer computation. These arguments are byte string values produced by the [ST\\_Buffer\\_Strategy\(\)](#page-93-0) function, to be used for point, join, and end strategies:

- Point strategies apply to Point and MultiPoint geometries. If no point strategy is specified, the default is [ST\\_Buffer\\_Strategy\('point\\_circle', 32\)](#page-93-0).
- Join strategies apply to LineString, MultiLineString, Polygon, and MultiPolygon geometries. If no join strategy is specified, the default is [ST\\_Buffer\\_Strategy\('join\\_round', 32\)](#page-93-0).
- End strategies apply to LineString and MultiLineString geometries. If no end strategy is specified, the default is [ST\\_Buffer\\_Strategy\('end\\_round', 32\)](#page-93-0).

Up to one strategy of each type may be specified, and they may be given in any order.

If the buffer strategies are invalid, an [ER\\_WRONG\\_ARGUMENTS](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_wrong_arguments) error occurs. Strategies are invalid under any of these circumstances:

- Multiple strategies of a given type (point, join, or end) are specified.
- A value that is not a strategy (such as an arbitrary binary string or a number) is passed as a strategy.
- A Point strategy is passed and the geometry contains no Point or MultiPoint values.
- An end or join strategy is passed and the geometry contains no LineString, Polygon, MultiLinestring or MultiPolygon values.

```
mysql> SET @pt = ST_GeomFromText('POINT(0 0)');
mysql> SET @pt_strategy = ST_Buffer_Strategy('point_square');
mysql> SELECT ST_AsText(ST_Buffer(@pt, 2, @pt_strategy));
+--------------------------------------------+
| ST_AsText(ST_Buffer(@pt, 2, @pt_strategy)) |
+--------------------------------------------+
| POLYGON((-2 -2,2 -2,2 2,-2 2,-2 -2)) |
+--------------------------------------------+
```

```
mysql> SET @ls = ST_GeomFromText('LINESTRING(0 0,0 5,5 5)');
mysql> SET @end_strategy = ST_Buffer_Strategy('end_flat');
mysql> SET @join_strategy = ST_Buffer_Strategy('join_round', 10);
mysql> SELECT ST_AsText(ST_Buffer(@ls, 5, @end_strategy, @join_strategy))
+---------------------------------------------------------------+
| ST_AsText(ST_Buffer(@ls, 5, @end_strategy, @join_strategy)) |
+---------------------------------------------------------------+
| POLYGON((5 5,5 10,0 10,-3.5355339059327373 8.535533905932738, |
| -5 5,-5 0,0 0,5 0,5 5)) |
+---------------------------------------------------------------+
```

<span id="page-93-0"></span>• [ST\\_Buffer\\_Strategy\(](#page-93-0)strategy [, points\_per\_circle])

This function returns a strategy byte string for use with [ST\\_Buffer\(\)](#page-92-0) to influence buffer computation.

Information about strategies is available at [Boost.org.](http://www.boost.org)

The first argument must be a string indicating a strategy option:

- For point strategies, permitted values are 'point\_circle' and 'point\_square'.
- For join strategies, permitted values are 'join\_round' and 'join\_miter'.

• For end strategies, permitted values are 'end\_round' and 'end\_flat'.

If the first argument is 'point\_circle', 'join\_round', 'join\_miter', or 'end\_round', the points\_per\_circle argument must be given as a positive numeric value. The maximum points\_per\_circle value is the value of the max\_points\_in\_geometry system variable.

For examples, see the description of [ST\\_Buffer\(\)](#page-92-0).

[ST\\_Buffer\\_Strategy\(\)](#page-93-0) handles its arguments as described in the introduction to this section, with these exceptions:

- If any argument is invalid, an [ER\\_WRONG\\_ARGUMENTS](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_wrong_arguments) error occurs.
- If the first argument is 'point\_square' or 'end\_flat', the points\_per\_circle argument must not be given or an [ER\\_WRONG\\_ARGUMENTS](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_wrong_arguments) error occurs.
- <span id="page-94-0"></span>• [ST\\_ConvexHull\(](#page-94-0)g)

Returns a geometry that represents the convex hull of the geometry value g.

This function computes a geometry's convex hull by first checking whether its vertex points are colinear. The function returns a linear hull if so, a polygon hull otherwise. This function processes geometry collections by extracting all vertex points of all components of the collection, creating a MultiPoint value from them, and computing its convex hull.

[ST\\_ConvexHull\(\)](#page-94-0) handles its arguments as described in the introduction to this section, with this exception:

• The return value is NULL for the additional condition that the argument is an empty geometry collection.

```
mysql> SET @g = 'MULTIPOINT(5 0,25 0,15 10,15 25)';
mysql> SELECT ST_AsText(ST_ConvexHull(ST_GeomFromText(@g)));
+-----------------------------------------------+
| ST_AsText(ST_ConvexHull(ST_GeomFromText(@g))) |
+-----------------------------------------------+
| POLYGON((5 0,25 0,15 25,5 0)) |
+-----------------------------------------------+
```

<span id="page-94-1"></span>• [ST\\_Difference\(](#page-94-1)g1, g2)

Returns a geometry that represents the point set difference of the geometry values g1 and g2. The result is in the same SRS as the geometry arguments.

As of MySQL 8.0.26, [ST\\_Difference\(\)](#page-94-1) permits arguments in either a Cartesian or a geographic SRS. Prior to MySQL 8.0.26, [ST\\_Difference\(\)](#page-94-1) permits arguments in a Cartesian SRS only; for arguments in a geographic SRS, an [ER\\_NOT\\_IMPLEMENTED\\_FOR\\_GEOGRAPHIC\\_SRS](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_not_implemented_for_geographic_srs) error occurs.

[ST\\_Difference\(\)](#page-94-1) handles its arguments as described in the introduction to this section.

```
mysql> SET @g1 = Point(1,1), @g2 = Point(2,2);
mysql> SELECT ST_AsText(ST_Difference(@g1, @g2));
+------------------------------------+
| ST_AsText(ST_Difference(@g1, @g2)) |
+------------------------------------+
| POINT(1 1) |
+------------------------------------+
```

<span id="page-95-0"></span>• [ST\\_Intersection\(](#page-95-0)g1, g2)

Returns a geometry that represents the point set intersection of the geometry values g1 and g2. The result is in the same SRS as the geometry arguments.

As of MySQL 8.0.27, [ST\\_Intersection\(\)](#page-95-0) permits arguments in either a Cartesian or a geographic SRS. Prior to MySQL 8.0.27, [ST\\_Intersection\(\)](#page-95-0) permits arguments in a Cartesian SRS only; for arguments in a geographic SRS, an [ER\\_NOT\\_IMPLEMENTED\\_FOR\\_GEOGRAPHIC\\_SRS](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_not_implemented_for_geographic_srs) error occurs.

[ST\\_Intersection\(\)](#page-95-0) handles its arguments as described in the introduction to this section.

```
mysql> SET @g1 = ST_GeomFromText('LineString(1 1, 3 3)');
mysql> SET @g2 = ST_GeomFromText('LineString(1 3, 3 1)');
mysql> SELECT ST_AsText(ST_Intersection(@g1, @g2));
+--------------------------------------+
| ST_AsText(ST_Intersection(@g1, @g2)) |
+--------------------------------------+
| POINT(2 2) |
+--------------------------------------+
```

<span id="page-95-1"></span>• [ST\\_LineInterpolatePoint\(](#page-95-1)ls, fractional\_distance)

This function takes a LineString geometry and a fractional distance in the range [0.0, 1.0] and returns the Point along the LineString at the given fraction of the distance from its start point to its endpoint. It can be used to answer questions such as which Point lies halfway along the road described by the geometry argument.

The function is implemented for LineString geometries in all spatial reference systems, both Cartesian and geographic.

If the fractional\_distance argument is 1.0, the result may not be exactly the last point of the LineString argument but a point close to it due to numerical inaccuracies in approximate-value computations.

A related function, [ST\\_LineInterpolatePoints\(\)](#page-95-2), takes similar arguments but returns a MultiPoint consisting of Point values along the LineString at each fraction of the distance from its start point to its endpoint. For examples of both functions, see the [ST\\_LineInterpolatePoints\(\)](#page-95-2) description.

[ST\\_LineInterpolatePoint\(\)](#page-95-1) handles its arguments as described in the introduction to this section, with these exceptions:

- If the geometry argument is not a LineString, an [ER\\_UNEXPECTED\\_GEOMETRY\\_TYPE](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_unexpected_geometry_type) error occurs.
- If the fractional distance argument is outside the range [0.0, 1.0], an [ER\\_DATA\\_OUT\\_OF\\_RANGE](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_data_out_of_range) error occurs.

[ST\\_LineInterpolatePoint\(\)](#page-95-1) is a MySQL extension to OpenGIS. This function was added in MySQL 8.0.24.

<span id="page-95-2"></span>• [ST\\_LineInterpolatePoints\(](#page-95-2)ls, fractional\_distance)

This function takes a LineString geometry and a fractional distance in the range (0.0, 1.0] and returns the MultiPoint consisting of the LineString start point, plus Point values along the LineString at each fraction of the distance from its start point to its endpoint. It can be used to

answer questions such as which Point values lie every 10% of the way along the road described by the geometry argument.

The function is implemented for LineString geometries in all spatial reference systems, both Cartesian and geographic.

If the fractional\_distance argument divides 1.0 with zero remainder the result may not contain the last point of the LineString argument but a point close to it due to numerical inaccuracies in approximate-value computations.

A related function, [ST\\_LineInterpolatePoint\(\)](#page-95-1), takes similar arguments but returns the Point along the LineString at the given fraction of the distance from its start point to its endpoint.

[ST\\_LineInterpolatePoints\(\)](#page-95-2) handles its arguments as described in the introduction to this section, with these exceptions:

- If the geometry argument is not a LineString, an [ER\\_UNEXPECTED\\_GEOMETRY\\_TYPE](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_unexpected_geometry_type) error occurs.
- If the fractional distance argument is outside the range [0.0, 1.0], an [ER\\_DATA\\_OUT\\_OF\\_RANGE](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_data_out_of_range) error occurs.

```
mysql> SET @ls1 = ST_GeomFromText('LINESTRING(0 0,0 5,5 5)');
mysql> SELECT ST_AsText(ST_LineInterpolatePoint(@ls1, .5));
+----------------------------------------------+
| ST_AsText(ST_LineInterpolatePoint(@ls1, .5)) |
+----------------------------------------------+
| POINT(0 5) |
+----------------------------------------------+
mysql> SELECT ST_AsText(ST_LineInterpolatePoint(@ls1, .75));
+-----------------------------------------------+
| ST_AsText(ST_LineInterpolatePoint(@ls1, .75)) |
+-----------------------------------------------+
| POINT(2.5 5) |
+-----------------------------------------------+
mysql> SELECT ST_AsText(ST_LineInterpolatePoint(@ls1, 1));
+---------------------------------------------+
| ST_AsText(ST_LineInterpolatePoint(@ls1, 1)) |
+---------------------------------------------+
| POINT(5 5) |
+---------------------------------------------+
mysql> SELECT ST_AsText(ST_LineInterpolatePoints(@ls1, .25));
+------------------------------------------------+
| ST_AsText(ST_LineInterpolatePoints(@ls1, .25)) |
+------------------------------------------------+
| MULTIPOINT((0 2.5),(0 5),(2.5 5),(5 5)) |
+------------------------------------------------+
```

[ST\\_LineInterpolatePoints\(\)](#page-95-2) is a MySQL extension to OpenGIS. This function was added in MySQL 8.0.24.

<span id="page-96-0"></span>• [ST\\_PointAtDistance\(](#page-96-0)ls, distance)

This function takes a LineString geometry and a distance in the range [0.0, [ST\\_Length\(](#page-86-0)ls)] measured in the unit of the spatial reference system (SRS) of the LineString, and returns the Point along the LineString at that distance from its start point. It can be used to answer

questions such as which Point value is 400 meters from the start of the road described by the geometry argument.

The function is implemented for LineString geometries in all spatial reference systems, both Cartesian and geographic.

[ST\\_PointAtDistance\(\)](#page-96-0) handles its arguments as described in the introduction to this section, with these exceptions:

- If the geometry argument is not a LineString, an [ER\\_UNEXPECTED\\_GEOMETRY\\_TYPE](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_unexpected_geometry_type) error occurs.
- If the fractional distance argument is outside the range [0.0, [ST\\_Length\(](#page-86-0)ls)], an [ER\\_DATA\\_OUT\\_OF\\_RANGE](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_data_out_of_range) error occurs.

[ST\\_PointAtDistance\(\)](#page-96-0) is a MySQL extension to OpenGIS. This function was added in MySQL 8.0.24.

<span id="page-97-0"></span>• [ST\\_SymDifference\(](#page-97-0)g1, g2)

Returns a geometry that represents the point set symmetric difference of the geometry values g1 and g2, which is defined as:

```
g1 symdifference g2 := (g1 union g2) difference (g1 intersection g2)
```

Or, in function call notation:

```
ST_SymDifference(g1, g2) = ST_Difference(ST_Union(g1, g2), ST_Intersection(g1, g2))
```

The result is in the same SRS as the geometry arguments.

As of MySQL 8.0.27, [ST\\_SymDifference\(\)](#page-97-0) permits arguments in either a Cartesian or a geographic SRS. Prior to MySQL 8.0.27, [ST\\_SymDifference\(\)](#page-97-0) permits arguments in a Cartesian SRS only; for arguments in a geographic SRS, an [ER\\_NOT\\_IMPLEMENTED\\_FOR\\_GEOGRAPHIC\\_SRS](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_not_implemented_for_geographic_srs) error occurs.

[ST\\_SymDifference\(\)](#page-97-0) handles its arguments as described in the introduction to this section.

```
mysql> SET @g1 = ST_GeomFromText('MULTIPOINT(5 0,15 10,15 25)');
mysql> SET @g2 = ST_GeomFromText('MULTIPOINT(1 1,15 10,15 25)');
mysql> SELECT ST_AsText(ST_SymDifference(@g1, @g2));
+---------------------------------------+
| ST_AsText(ST_SymDifference(@g1, @g2)) |
+---------------------------------------+
| MULTIPOINT((1 1),(5 0)) |
+---------------------------------------+
```

<span id="page-97-1"></span>• [ST\\_Transform\(](#page-97-1)g, target\_srid)

Transforms a geometry from one spatial reference system (SRS) to another. The return value is a geometry of the same type as the input geometry with all coordinates transformed to the target SRID, target\_srid. Prior to MySQL 8.0.30, transformation support was limited to geographic SRSs (unless the SRID of the geometry argument was the same as the target SRID value, in which case the return value was the input geometry for any valid SRS), and this function did not support Cartesian SRSs. Beginning with MySQL 8.0.30, support is provided for the Popular Visualisation Pseudo Mercator (EPSG 1024) projection method, used for WGS 84 Pseudo-Mercator (SRID 3857). In MySQL 8.0.32 and later, support is extended to all SRSs defined by EPSG except for those listed here:

- EPSG 1042 Krovak Modified
- EPSG 1043 Krovak Modified (North Orientated)

- EPSG 9816 Tunisia Mining Grid
- EPSG 9826 Lambert Conic Conformal (West Orientated)

[ST\\_Transform\(\)](#page-97-1) handles its arguments as described in the introduction to this section, with these exceptions:

- Geometry arguments that have an SRID value for a geographic SRS do not produce an error.
- If the geometry or target SRID argument has an SRID value that refers to an undefined spatial reference system (SRS), an [ER\\_SRS\\_NOT\\_FOUND](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_srs_not_found) error occurs.
- If the geometry is in an SRS that [ST\\_Transform\(\)](#page-97-1) cannot transform from, an [ER\\_TRANSFORM\\_SOURCE\\_SRS\\_NOT\\_SUPPORTED](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_transform_source_srs_not_supported) error occurs.
- If the target SRID is in an SRS that [ST\\_Transform\(\)](#page-97-1) cannot transform to, an [ER\\_TRANSFORM\\_TARGET\\_SRS\\_NOT\\_SUPPORTED](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_transform_target_srs_not_supported) error occurs.
- If the geometry is in an SRS that is not WGS 84 and has no TOWGS84 clause, an [ER\\_TRANSFORM\\_SOURCE\\_SRS\\_MISSING\\_TOWGS84](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_transform_source_srs_missing_towgs84) error occurs.
- If the target SRID is in an SRS that is not WGS 84 and has no TOWGS84 clause, an [ER\\_TRANSFORM\\_TARGET\\_SRS\\_MISSING\\_TOWGS84](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_transform_target_srs_missing_towgs84) error occurs.

ST\_SRID(g, [target\\_srid](#page-81-0)) and [ST\\_Transform\(](#page-97-1)g, target\_srid) differ as follows:

- [ST\\_SRID\(\)](#page-81-0) changes the geometry SRID value without transforming its coordinates.
- [ST\\_Transform\(\)](#page-97-1) transforms the geometry coordinates in addition to changing its SRID value.

```
mysql> SET @p = ST_GeomFromText('POINT(52.381389 13.064444)', 4326);
mysql> SELECT ST_AsText(@p);
+----------------------------+
| ST_AsText(@p) |
+----------------------------+
| POINT(52.381389 13.064444) |
+----------------------------+
mysql> SET @p = ST_Transform(@p, 4230);
mysql> SELECT ST_AsText(@p);
+---------------------------------------------+
| ST_AsText(@p) |
+---------------------------------------------+
| POINT(52.38208611407426 13.065520672345304) |
+---------------------------------------------+
```

<span id="page-98-0"></span>• [ST\\_Union\(](#page-98-0)g1, g2)

Returns a geometry that represents the point set union of the geometry values g1 and g2. The result is in the same SRS as the geometry arguments.

As of MySQL 8.0.26, [ST\\_Union\(\)](#page-98-0) permits arguments in either a Cartesian or a geographic SRS. Prior to MySQL 8.0.26, [ST\\_Union\(\)](#page-98-0) permits arguments in a Cartesian SRS only; for arguments in a geographic SRS, an [ER\\_NOT\\_IMPLEMENTED\\_FOR\\_GEOGRAPHIC\\_SRS](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_not_implemented_for_geographic_srs) error occurs.

[ST\\_Union\(\)](#page-98-0) handles its arguments as described in the introduction to this section.

```
mysql> SET @g1 = ST_GeomFromText('LineString(1 1, 3 3)');
mysql> SET @g2 = ST_GeomFromText('LineString(1 3, 3 1)');
mysql> SELECT ST_AsText(ST_Union(@g1, @g2));
+--------------------------------------+
| ST_AsText(ST_Union(@g1, @g2)) |
+--------------------------------------+
| MULTILINESTRING((1 1,3 3),(1 3,3 1)) |
+--------------------------------------+
```