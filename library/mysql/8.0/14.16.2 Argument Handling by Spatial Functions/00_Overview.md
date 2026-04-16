---
source: MySQL 8.0 Reference
title: 00_Overview
---

Spatial values, or geometries, have the properties described in Section 13.4.2.2, "Geometry Class". The following discussion lists general spatial function argument-handling characteristics. Specific functions or groups of functions may have additional or different argument-handling characteristics, as discussed in the sections where those function descriptions occur. Where that is true, those descriptions take precedence over the general discussion here.

Spatial functions are defined only for valid geometry values. See Section 13.4.4, "Geometry Well-Formedness and Validity".

Each geometry value is associated with a spatial reference system (SRS), which is a coordinate-based system for geographic locations. See Section 13.4.5, "Spatial Reference System Support".

The spatial reference identifier (SRID) of a geometry identifies the SRS in which the geometry is defined. In MySQL, the SRID value is an integer associated with the geometry value. The maximum usable SRID value is 2<sup>32</sup> −1. If a larger value is given, only the lower 32 bits are used.

SRID 0 represents an infinite flat Cartesian plane with no units assigned to its axes. To ensure SRID 0 behavior, create geometry values using SRID 0. SRID 0 is the default for new geometry values if no SRID is specified.

For computations on multiple geometry values, all values must be in the same SRS or an error occurs. Thus, spatial functions that take multiple geometry arguments require those arguments to be in the same SRS. If a spatial function returns [ER\\_GIS\\_DIFFERENT\\_SRIDS](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_gis_different_srids), it means that the geometry arguments were not all in the same SRS. You must modify them to have the same SRS.

A geometry returned by a spatial function is in the SRS of the geometry arguments because geometry values produced by any spatial function inherit the SRID of the geometry arguments.

The [Open Geospatial Consortium](http://www.opengeospatial.org) guidelines require that input polygons already be closed, so unclosed polygons are rejected as invalid rather than being closed.

In MySQL, the only valid empty geometry is represented in the form of an empty geometry collection. Empty geometry collection handling is as follows: An empty WKT input geometry collection may be specified as 'GEOMETRYCOLLECTION()'. This is also the output WKT resulting from a spatial operation that produces an empty geometry collection.

During parsing of a nested geometry collection, the collection is flattened and its basic components are used in various GIS operations to compute results. This provides additional flexibility to users because it is unnecessary to be concerned about the uniqueness of geometry data. Nested geometry collections may be produced from nested GIS function calls without having to be explicitly flattened first.

# <span id="page-72-0"></span>**14.16.3 Functions That Create Geometry Values from WKT Values**

These functions take as arguments a Well-Known Text (WKT) representation and, optionally, a spatial reference system identifier (SRID). They return the corresponding geometry. For a description of WKT format, see Well-Known Text (WKT) Format.

Functions in this section detect arguments in either Cartesian or geographic spatial reference systems (SRSs), and return results appropriate to the SRS.

[ST\\_GeomFromText\(\)](#page-73-1) accepts a WKT value of any geometry type as its first argument. Other functions provide type-specific construction functions for construction of geometry values of each geometry type.

Functions such as [ST\\_MPointFromText\(\)](#page-74-1) and [ST\\_GeomFromText\(\)](#page-73-1) that accept WKT-format representations of MultiPoint values permit individual points within values to be surrounded by parentheses. For example, both of the following function calls are valid:

```
ST_MPointFromText('MULTIPOINT (1 1, 2 2, 3 3)')
ST_MPointFromText('MULTIPOINT ((1 1), (2 2), (3 3))')
```

Functions such as [ST\\_GeomFromText\(\)](#page-73-1) that accept WKT geometry collection arguments understand both OpenGIS 'GEOMETRYCOLLECTION EMPTY' standard syntax and MySQL 'GEOMETRYCOLLECTION()' nonstandard syntax. Functions such as [ST\\_AsWKT\(\)](#page-78-1) that produce WKT values produce 'GEOMETRYCOLLECTION EMPTY' standard syntax:

```
mysql> SET @s1 = ST_GeomFromText('GEOMETRYCOLLECTION()');
mysql> SET @s2 = ST_GeomFromText('GEOMETRYCOLLECTION EMPTY');
mysql> SELECT ST_AsWKT(@s1), ST_AsWKT(@s2);
```

```
+--------------------------+--------------------------+
| ST_AsWKT(@s1) | ST_AsWKT(@s2) |
+--------------------------+--------------------------+
| GEOMETRYCOLLECTION EMPTY | GEOMETRYCOLLECTION EMPTY |
+--------------------------+--------------------------+
```

Unless otherwise specified, functions in this section handle their geometry arguments as follows:

- If any geometry argument is NULL or is not a syntactically well-formed geometry, or if the SRID argument is NULL, the return value is NULL.
- By default, geographic coordinates (latitude, longitude) are interpreted as in the order specified by the spatial reference system of geometry arguments. An optional options argument may be given to override the default axis order. options consists of a list of comma-separated key=value. The only permitted key value is axis-order, with permitted values of lat-long, long-lat and srid-defined (the default).

If the options argument is NULL, the return value is NULL. If the options argument is invalid, an error occurs to indicate why.

- If an SRID argument refers to an undefined spatial reference system (SRS), an [ER\\_SRS\\_NOT\\_FOUND](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_srs_not_found) error occurs.
- For geographic SRS geometry arguments, if any argument has a longitude or latitude that is out of range, an error occurs:
  - If a longitude value is not in the range (−180, 180], an [ER\\_LONGITUDE\\_OUT\\_OF\\_RANGE](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_longitude_out_of_range) error occurs.
  - If a latitude value is not in the range [−90, 90], an [ER\\_LATITUDE\\_OUT\\_OF\\_RANGE](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_latitude_out_of_range) error occurs.

Ranges shown are in degrees. If an SRS uses another unit, the range uses the corresponding values in its unit. The exact range limits deviate slightly due to floating-point arithmetic.

These functions are available for creating geometries from WKT values:

```
• ST_GeomCollFromText(wkt [, srid [, options]]),
 ST_GeometryCollectionFromText(wkt [, srid [, options]]),
 ST_GeomCollFromTxt(wkt [, srid [, options]])
```

Constructs a GeometryCollection value using its WKT representation and SRID.

These functions handle their arguments as described in the introduction to this section.

```
mysql> SET @g = "MULTILINESTRING((10 10, 11 11), (9 9, 10 10))";
mysql> SELECT ST_AsText(ST_GeomCollFromText(@g));
+--------------------------------------------+
| ST_AsText(ST_GeomCollFromText(@g)) |
+--------------------------------------------+
| MULTILINESTRING((10 10,11 11),(9 9,10 10)) |
+--------------------------------------------+
```

<span id="page-73-1"></span>• [ST\\_GeomFromText\(](#page-73-1)wkt [, srid [, options]]), [ST\\_GeometryFromText\(](#page-73-1)wkt [, srid [, [options](#page-73-1)]])

Constructs a geometry value of any type using its WKT representation and SRID.

These functions handle their arguments as described in the introduction to this section.

<span id="page-73-2"></span>• [ST\\_LineFromText\(](#page-73-2)wkt [, srid [, options]]), [ST\\_LineStringFromText\(](#page-73-2)wkt [, srid [, [options](#page-73-2)]])

Constructs a LineString value using its WKT representation and SRID.

These functions handle their arguments as described in the introduction to this section.

<span id="page-74-0"></span>• [ST\\_MLineFromText\(](#page-74-0)wkt [, srid [, options]]), [ST\\_MultiLineStringFromText\(](#page-74-0)wkt [, srid [, [options](#page-74-0)]])

Constructs a MultiLineString value using its WKT representation and SRID.

These functions handle their arguments as described in the introduction to this section.

<span id="page-74-1"></span>• [ST\\_MPointFromText\(](#page-74-1)wkt [, srid [, options]]), [ST\\_MultiPointFromText\(](#page-74-1)wkt [, srid [, [options](#page-74-1)]])

Constructs a MultiPoint value using its WKT representation and SRID.

These functions handle their arguments as described in the introduction to this section.

<span id="page-74-2"></span>• [ST\\_MPolyFromText\(](#page-74-2)wkt [, srid [, options]]), [ST\\_MultiPolygonFromText\(](#page-74-2)wkt [, srid [, [options](#page-74-2)]])

Constructs a MultiPolygon value using its WKT representation and SRID.

These functions handle their arguments as described in the introduction to this section.

<span id="page-74-3"></span>• [ST\\_PointFromText\(](#page-74-3)wkt [, srid [, options]])

Constructs a Point value using its WKT representation and SRID.

[ST\\_PointFromText\(\)](#page-74-3) handles its arguments as described in the introduction to this section.

<span id="page-74-4"></span>• [ST\\_PolyFromText\(](#page-74-4)wkt [, srid [, options]]), [ST\\_PolygonFromText\(](#page-74-4)wkt [, srid [, [options](#page-74-4)]])

Constructs a Polygon value using its WKT representation and SRID.

These functions handle their arguments as described in the introduction to this section.

# <span id="page-74-5"></span>**14.16.4 Functions That Create Geometry Values from WKB Values**

These functions take as arguments a BLOB containing a Well-Known Binary (WKB) representation and, optionally, a spatial reference system identifier (SRID). They return the corresponding geometry. For a description of WKB format, see Well-Known Binary (WKB) Format.

Functions in this section detect arguments in either Cartesian or geographic spatial reference systems (SRSs), and return results appropriate to the SRS.

[ST\\_GeomFromWKB\(\)](#page-75-1) accepts a WKB value of any geometry type as its first argument. Other functions provide type-specific construction functions for construction of geometry values of each geometry type.

Prior to MySQL 8.0, these functions also accepted geometry objects as returned by the functions in [Section 14.16.5, "MySQL-Specific Functions That Create Geometry Values"](#page-76-6). Geometry arguments are no longer permitted and produce an error. To migrate calls from using geometry arguments to using WKB arguments, follow these guidelines:

- Rewrite constructs such as ST\_GeomFromWKB(Point(0, 0)) as Point(0, 0).
- Rewrite constructs such as ST\_GeomFromWKB(Point(0, 0), 4326) as ST\_SRID(Point(0, 0), 4326) or ST\_GeomFromWKB(ST\_AsWKB(Point(0, 0)), 4326).

Unless otherwise specified, functions in this section handle their geometry arguments as follows:

- If the WKB or SRID argument is NULL, the return value is NULL.
- By default, geographic coordinates (latitude, longitude) are interpreted as in the order specified by the spatial reference system of geometry arguments. An optional options argument may be given to override the default axis order. options consists of a list of comma-separated key=value.

The only permitted key value is axis-order, with permitted values of lat-long, long-lat and srid-defined (the default).

If the options argument is NULL, the return value is NULL. If the options argument is invalid, an error occurs to indicate why.

- If an SRID argument refers to an undefined spatial reference system (SRS), an [ER\\_SRS\\_NOT\\_FOUND](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_srs_not_found) error occurs.
- For geographic SRS geometry arguments, if any argument has a longitude or latitude that is out of range, an error occurs:
  - If a longitude value is not in the range (−180, 180], an [ER\\_LONGITUDE\\_OUT\\_OF\\_RANGE](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_longitude_out_of_range) error occurs.
  - If a latitude value is not in the range [−90, 90], an [ER\\_LATITUDE\\_OUT\\_OF\\_RANGE](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_latitude_out_of_range) error occurs.

Ranges shown are in degrees. If an SRS uses another unit, the range uses the corresponding values in its unit. The exact range limits deviate slightly due to floating-point arithmetic.

These functions are available for creating geometries from WKB values:

```
• ST_GeomCollFromWKB(wkb [, srid [, options]]),
 ST_GeometryCollectionFromWKB(wkb [, srid [, options]])
```

Constructs a GeometryCollection value using its WKB representation and SRID.

These functions handle their arguments as described in the introduction to this section.

<span id="page-75-1"></span>• [ST\\_GeomFromWKB\(](#page-75-1)wkb [, srid [, options]]), [ST\\_GeometryFromWKB\(](#page-75-1)wkb [, srid [, [options](#page-75-1)]])

Constructs a geometry value of any type using its WKB representation and SRID.

These functions handle their arguments as described in the introduction to this section.

```
• ST_LineFromWKB(wkb [, srid [, options]]), ST_LineStringFromWKB(wkb [, srid
 [, options]])
```

Constructs a LineString value using its WKB representation and SRID.

These functions handle their arguments as described in the introduction to this section.

```
• ST_MLineFromWKB(wkb [, srid [, options]]), ST_MultiLineStringFromWKB(wkb [,
 srid [, options]])
```

Constructs a MultiLineString value using its WKB representation and SRID.

These functions handle their arguments as described in the introduction to this section.

```
• ST_MPointFromWKB(wkb [, srid [, options]]), ST_MultiPointFromWKB(wkb [,
 srid [, options]])
```

Constructs a MultiPoint value using its WKB representation and SRID.

These functions handle their arguments as described in the introduction to this section.

```
• ST_MPolyFromWKB(wkb [, srid [, options]]), ST_MultiPolygonFromWKB(wkb [,
 srid [, options]])
```

Constructs a MultiPolygon value using its WKB representation and SRID.

These functions handle their arguments as described in the introduction to this section.

<span id="page-76-4"></span>• [ST\\_PointFromWKB\(](#page-76-4)wkb [, srid [, options]])

Constructs a Point value using its WKB representation and SRID.

[ST\\_PointFromWKB\(\)](#page-76-4) handles its arguments as described in the introduction to this section.

<span id="page-76-5"></span>• [ST\\_PolyFromWKB\(](#page-76-5)wkb [, srid [, options]]), [ST\\_PolygonFromWKB\(](#page-76-5)wkb [, srid [, [options](#page-76-5)]])

Constructs a Polygon value using its WKB representation and SRID.

These functions handle their arguments as described in the introduction to this section.

# <span id="page-76-6"></span>**14.16.5 MySQL-Specific Functions That Create Geometry Values**

MySQL provides a set of useful nonstandard functions for creating geometry values. The functions described in this section are MySQL extensions to the OpenGIS specification.

These functions produce geometry objects from either WKB values or geometry objects as arguments. If any argument is not a proper WKB or geometry representation of the proper object type, the return value is NULL.

For example, you can insert the geometry return value from [Point\(\)](#page-77-2) directly into a POINT column:

```
INSERT INTO t1 (pt_col) VALUES(Point(1,2));
```

<span id="page-76-0"></span>• [GeomCollection\(](#page-76-0)g [, g] ...)

Constructs a GeomCollection value from the geometry arguments.

[GeomCollection\(\)](#page-76-0) returns all the proper geometries contained in the arguments even if a nonsupported geometry is present.

[GeomCollection\(\)](#page-76-0) with no arguments is permitted as a way to create an empty geometry. Also, functions such as [ST\\_GeomFromText\(\)](#page-73-1) that accept WKT geometry collection arguments understand both OpenGIS 'GEOMETRYCOLLECTION EMPTY' standard syntax and MySQL 'GEOMETRYCOLLECTION()' nonstandard syntax.

[GeomCollection\(\)](#page-76-0) and [GeometryCollection\(\)](#page-76-1) are synonymous, with [GeomCollection\(\)](#page-76-0) the preferred function.

<span id="page-76-1"></span>• [GeometryCollection\(](#page-76-1)g [, g] ...)

Constructs a GeomCollection value from the geometry arguments.

[GeometryCollection\(\)](#page-76-1) returns all the proper geometries contained in the arguments even if a nonsupported geometry is present.

[GeometryCollection\(\)](#page-76-1) with no arguments is permitted as a way to create an empty geometry. Also, functions such as [ST\\_GeomFromText\(\)](#page-73-1) that accept WKT geometry collection arguments understand both OpenGIS 'GEOMETRYCOLLECTION EMPTY' standard syntax and MySQL 'GEOMETRYCOLLECTION()' nonstandard syntax.

[GeomCollection\(\)](#page-76-0) and [GeometryCollection\(\)](#page-76-1) are synonymous, with [GeomCollection\(\)](#page-76-0) the preferred function.

<span id="page-76-2"></span>• [LineString\(](#page-76-2)pt [, pt] ...)

Constructs a LineString value from a number of Point or WKB Point arguments. If the number of arguments is less than two, the return value is NULL.

<span id="page-76-3"></span>• [MultiLineString\(](#page-76-3)ls [, ls] ...)

Constructs a MultiLineString value using LineString or WKB LineString arguments.

<span id="page-77-0"></span>• [MultiPoint\(](#page-77-0)pt [, pt2] ...)

Constructs a MultiPoint value using Point or WKB Point arguments.

<span id="page-77-1"></span>• [MultiPolygon\(](#page-77-1)poly [, poly] ...)

Constructs a MultiPolygon value from a set of Polygon or WKB Polygon arguments.

<span id="page-77-2"></span>• [Point\(](#page-77-2)x, y)

Constructs a Point using its coordinates.

<span id="page-77-3"></span>• [Polygon\(](#page-77-3)ls [, ls] ...)

Constructs a Polygon value from a number of LineString or WKB LineString arguments. If any argument does not represent a LinearRing (that is, not a closed and simple LineString), the return value is NULL.