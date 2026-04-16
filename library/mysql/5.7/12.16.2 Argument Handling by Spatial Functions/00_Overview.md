---
source: MySQL 5.7 Reference
title: 00_Overview
---

Spatial values, or geometries, have the properties described in Section 11.4.2.2, "Geometry Class". The following discussion lists general spatial function argument-handling characteristics. Specific functions or groups of functions may have additional or different argument-handling characteristics, as discussed in the sections where those function descriptions occur. Where that is true, those descriptions take precedence over the general discussion here.

Spatial functions are defined only for valid geometry values. See Section 11.4.4, "Geometry Well-Formedness and Validity".

The spatial reference identifier (SRID) of a geometry identifies the coordinate space in which the geometry is defined. In MySQL, the SRID value is an integer associated with the geometry value. The maximum usable SRID value is 2<sup>32</sup> −1. If a larger value is given, only the lower 32 bits are used.

In MySQL, all computations are done assuming SRID 0, regardless of the actual SRID value. SRID 0 represents an infinite flat Cartesian plane with no units assigned to its axes. In the future, computations may use the specified SRID values. To ensure SRID 0 behavior, create geometry values using SRID 0. SRID 0 is the default for new geometry values if no SRID is specified.

Geometry values produced by any spatial function inherit the SRID of the geometry arguments.

The [Open Geospatial Consortium](http://www.opengeospatial.org) guidelines require that input polygons already be closed, so unclosed polygons are rejected as invalid rather than being closed.

Empty geometry-collection handling is as follows: An empty WKT input geometry collection may be specified as 'GEOMETRYCOLLECTION()'. This is also the output WKT resulting from a spatial operation that produces an empty geometry collection.

During parsing of a nested geometry collection, the collection is flattened and its basic components are used in various GIS operations to compute results. This provides additional flexibility to users because it is unnecessary to be concerned about the uniqueness of geometry data. Nested geometry collections may be produced from nested GIS function calls without having to be explicitly flattened first.

## <span id="page-137-3"></span>**12.16.3 Functions That Create Geometry Values from WKT Values**

These functions take as arguments a Well-Known Text (WKT) representation and, optionally, a spatial reference system identifier (SRID). They return the corresponding geometry.

[ST\\_GeomFromText\(\)](#page-139-0) accepts a WKT value of any geometry type as its first argument. Other functions provide type-specific construction functions for construction of geometry values of each geometry type.

For a description of WKT format, see Well-Known Text (WKT) Format.

```
• GeomCollFromText(wkt [, srid]), GeometryCollectionFromText(wkt [, srid])
```

[ST\\_GeomCollFromText\(\)](#page-138-5), [ST\\_GeometryCollectionFromText\(\)](#page-138-5), [ST\\_GeomCollFromTxt\(\)](#page-138-5), [GeomCollFromText\(\)](#page-137-0), and [GeometryCollectionFromText\(\)](#page-137-0) are synonyms. For more information, see the description of [ST\\_GeomCollFromText\(\)](#page-138-5).

[GeomCollFromText\(\)](#page-137-0) and [GeometryCollectionFromText\(\)](#page-137-0) are deprecated; expect them to be removed in a future MySQL release. Use [ST\\_GeomCollFromText\(\)](#page-138-5) and [ST\\_GeometryCollectionFromText\(\)](#page-138-5) instead.

<span id="page-137-1"></span>• [GeomFromText\(](#page-137-1)wkt [, srid]), [GeometryFromText\(](#page-137-1)wkt [, srid])

```
ST_GeomFromText(), ST_GeometryFromText(), GeomFromText(), and
GeometryFromText() are synonyms. For more information, see the description of
ST_GeomFromText().
```

[GeomFromText\(\)](#page-137-1) and [GeometryFromText\(\)](#page-137-1) are deprecated; expect them to be removed in a future MySQL release. Use [ST\\_GeomFromText\(\)](#page-139-0) and [ST\\_GeometryFromText\(\)](#page-139-0) instead.

```
• LineFromText(wkt [, srid]), LineStringFromText(wkt [, srid])
```

```
ST_LineFromText(), ST_LineStringFromText(), LineFromText(), and
LineStringFromText() are synonyms. For more information, see the description of
ST_LineFromText().
```

[LineFromText\(\)](#page-137-2) and [LineStringFromText\(\)](#page-137-2) are deprecated; expect them to be removed in a future MySQL release. Use [ST\\_LineFromText\(\)](#page-139-1) and [ST\\_LineStringFromText\(\)](#page-139-1) instead.

<span id="page-138-0"></span>• [MLineFromText\(](#page-138-0)wkt [, srid]), [MultiLineStringFromText\(](#page-138-0)wkt [, srid])

[ST\\_MLineFromText\(\)](#page-139-2), [ST\\_MultiLineStringFromText\(\)](#page-139-2), [MLineFromText\(\)](#page-138-0), and [MultiLineStringFromText\(\)](#page-138-0) are synonyms. For more information, see the description of [ST\\_MLineFromText\(\)](#page-139-2).

[MLineFromText\(\)](#page-138-0) and [MultiLineStringFromText\(\)](#page-138-0) are deprecated; expect them to be removed in a future MySQL release. Use [ST\\_MLineFromText\(\)](#page-139-2) and [ST\\_MultiLineStringFromText\(\)](#page-139-2) instead.

<span id="page-138-1"></span>• [MPointFromText\(](#page-138-1)wkt [, srid]), [MultiPointFromText\(](#page-138-1)wkt [, srid])

[ST\\_MPointFromText\(\)](#page-139-3), [ST\\_MultiPointFromText\(\)](#page-139-3), [MPointFromText\(\)](#page-138-1), and [MultiPointFromText\(\)](#page-138-1) are synonyms. For more information, see the description of [ST\\_MPointFromText\(\)](#page-139-3).

[MPointFromText\(\)](#page-138-1) and [MultiPointFromText\(\)](#page-138-1) are deprecated; expect them to be removed in a future MySQL release. Use [ST\\_MPointFromText\(\)](#page-139-3) and [ST\\_MultiPointFromText\(\)](#page-139-3) instead.

<span id="page-138-2"></span>• [MPolyFromText\(](#page-138-2)wkt [, srid]), [MultiPolygonFromText\(](#page-138-2)wkt [, srid])

[ST\\_MPolyFromText\(\)](#page-139-4), [ST\\_MultiPolygonFromText\(\)](#page-139-4), [MPolyFromText\(\)](#page-138-2), and [MultiPolygonFromText\(\)](#page-138-2) are synonyms. For more information, see the description of [ST\\_MPolyFromText\(\)](#page-139-4).

[MPolyFromText\(\)](#page-138-2) and [MultiPolygonFromText\(\)](#page-138-2) are deprecated; expect them to be removed in a future MySQL release. Use [ST\\_MPolyFromText\(\)](#page-139-4) and [ST\\_MultiPolygonFromText\(\)](#page-139-4) instead.

<span id="page-138-3"></span>• [PointFromText\(](#page-138-3)wkt [, srid])

[ST\\_PointFromText\(\)](#page-139-5) and [PointFromText\(\)](#page-138-3) are synonyms. For more information, see the description of [ST\\_PointFromText\(\)](#page-139-5).

[PointFromText\(\)](#page-138-3) is deprecated; expect it to be removed in a future MySQL release. Use [ST\\_PointFromText\(\)](#page-139-5) instead.

<span id="page-138-4"></span>• [PolyFromText\(](#page-138-4)wkt [, srid]), [PolygonFromText\(](#page-138-4)wkt [, srid])

[ST\\_PolyFromText\(\)](#page-140-3), [ST\\_PolygonFromText\(\)](#page-140-3), [PolyFromText\(\)](#page-138-4), and [PolygonFromText\(\)](#page-138-4) are synonyms. For more information, see the description of [ST\\_PolyFromText\(\)](#page-140-3).

[PolyFromText\(\)](#page-138-4) and [PolygonFromText\(\)](#page-138-4) are deprecated; expect them to be removed in a future MySQL release. Use [ST\\_PolyFromText\(\)](#page-140-3) and [ST\\_PolygonFromText\(\)](#page-140-3) instead.

<span id="page-138-5"></span>• [ST\\_GeomCollFromText\(](#page-138-5)wkt [, srid]), [ST\\_GeometryCollectionFromText\(](#page-138-5)wkt [, [srid](#page-138-5)]), [ST\\_GeomCollFromTxt\(](#page-138-5)wkt [, srid])

Constructs a GeometryCollection value using its WKT representation and SRID.

If the geometry argument is NULL or not a syntactically well-formed geometry, or if the SRID argument is NULL, the return value is NULL.

```
mysql> SET @g = "MULTILINESTRING((10 10, 11 11), (9 9, 10 10))";
mysql> SELECT ST_AsText(ST_GeomCollFromText(@g));
+--------------------------------------------+
| ST_AsText(ST_GeomCollFromText(@g)) |
+--------------------------------------------+
| MULTILINESTRING((10 10,11 11),(9 9,10 10)) |
```

+--------------------------------------------+

```
ST_GeomCollFromText(), ST_GeometryCollectionFromText(), ST_GeomCollFromTxt(),
GeomCollFromText(), and GeometryCollectionFromText() are synonyms.
```

<span id="page-139-0"></span>• [ST\\_GeomFromText\(](#page-139-0)wkt [, srid]), [ST\\_GeometryFromText\(](#page-139-0)wkt [, srid])

Constructs a geometry value of any type using its WKT representation and SRID.

If the geometry argument is NULL or not a syntactically well-formed geometry, or if the SRID argument is NULL, the return value is NULL.

```
ST_GeomFromText(), ST_GeometryFromText(), GeomFromText(), and
GeometryFromText() are synonyms.
```

<span id="page-139-1"></span>• [ST\\_LineFromText\(](#page-139-1)wkt [, srid]), [ST\\_LineStringFromText\(](#page-139-1)wkt [, srid])

Constructs a LineString value using its WKT representation and SRID.

If the geometry argument is NULL or not a syntactically well-formed geometry, or if the SRID argument is NULL, the return value is NULL.

```
ST_LineFromText(), ST_LineStringFromText(), LineFromText(), and
LineStringFromText() are synonyms.
```

<span id="page-139-2"></span>• [ST\\_MLineFromText\(](#page-139-2)wkt [, srid]), [ST\\_MultiLineStringFromText\(](#page-139-2)wkt [, srid])

Constructs a MultiLineString value using its WKT representation and SRID.

If the geometry argument is NULL or not a syntactically well-formed geometry, or if the SRID argument is NULL, the return value is NULL.

```
ST_MLineFromText(), ST_MultiLineStringFromText(), MLineFromText(), and
MultiLineStringFromText() are synonyms.
```

<span id="page-139-3"></span>• [ST\\_MPointFromText\(](#page-139-3)wkt [, srid]), [ST\\_MultiPointFromText\(](#page-139-3)wkt [, srid])

Constructs a MultiPoint value using its WKT representation and SRID.

If the geometry argument is NULL or not a syntactically well-formed geometry, or if the SRID argument is NULL, the return value is NULL.

Functions such as [ST\\_MPointFromText\(\)](#page-139-3) and [ST\\_GeomFromText\(\)](#page-139-0) that accept WKT-format representations of MultiPoint values permit individual points within values to be surrounded by parentheses. For example, both of the following function calls are valid:

```
ST_MPointFromText('MULTIPOINT (1 1, 2 2, 3 3)')
ST_MPointFromText('MULTIPOINT ((1 1), (2 2), (3 3))')
```

[ST\\_MPointFromText\(\)](#page-139-3), [ST\\_MultiPointFromText\(\)](#page-139-3), [MPointFromText\(\)](#page-138-1), and [MultiPointFromText\(\)](#page-138-1) are synonyms.

<span id="page-139-4"></span>• [ST\\_MPolyFromText\(](#page-139-4)wkt [, srid]), [ST\\_MultiPolygonFromText\(](#page-139-4)wkt [, srid])

Constructs a MultiPolygon value using its WKT representation and SRID.

If the geometry argument is NULL or not a syntactically well-formed geometry, or if the SRID argument is NULL, the return value is NULL.

```
ST_MPolyFromText(), ST_MultiPolygonFromText(), MPolyFromText(), and
MultiPolygonFromText() are synonyms.
```

<span id="page-139-5"></span>• [ST\\_PointFromText\(](#page-139-5)wkt [, srid])

Constructs a Point value using its WKT representation and SRID.

If the geometry argument is NULL or not a syntactically well-formed geometry, or if the SRID argument is NULL, the return value is NULL.

```
ST_PointFromText() and PointFromText() are synonyms.
```

<span id="page-140-3"></span>• [ST\\_PolyFromText\(](#page-140-3)wkt [, srid]), [ST\\_PolygonFromText\(](#page-140-3)wkt [, srid])

Constructs a Polygon value using its WKT representation and SRID.

If the geometry argument is NULL or not a syntactically well-formed geometry, or if the SRID argument is NULL, the return value is NULL.

[ST\\_PolyFromText\(\)](#page-140-3), [ST\\_PolygonFromText\(\)](#page-140-3), [PolyFromText\(\)](#page-138-4), and [PolygonFromText\(\)](#page-138-4) are synonyms.

## <span id="page-140-4"></span>**12.16.4 Functions That Create Geometry Values from WKB Values**

These functions take as arguments a BLOB containing a Well-Known Binary (WKB) representation and, optionally, a spatial reference system identifier (SRID). They return the corresponding geometry.

[ST\\_GeomFromWKB\(\)](#page-142-0) accepts a WKB value of any geometry type as its first argument. Other functions provide type-specific construction functions for construction of geometry values of each geometry type.

These functions also accept geometry objects as returned by the functions in [Section 12.16.5,](#page-143-8) ["MySQL-Specific Functions That Create Geometry Values"](#page-143-8). Thus, those functions may be used to provide the first argument to the functions in this section. However, as of MySQL 5.7.19, use of geometry arguments is deprecated and generates a warning. Geometry arguments are not accepted in MySQL 8.0. To migrate calls from using geometry arguments to using WKB arguments, follow these guidelines:

For a description of WKB format, see Well-Known Binary (WKB) Format.

- Rewrite constructs such as ST\_GeomFromWKB(Point(0, 0)) as Point(0, 0).
- Rewrite constructs such as ST\_GeomFromWKB(Point(0, 0), 4326) as ST\_GeomFromWKB(ST\_AsWKB(Point(0, 0)), 4326). (Alternatively, in MySQL 8.0, you can use ST\_SRID(Point(0, 0), 4326).)
- <span id="page-140-0"></span>• [GeomCollFromWKB\(](#page-140-0)wkb [, srid]), [GeometryCollectionFromWKB\(](#page-140-0)wkb [, srid])

[ST\\_GeomCollFromWKB\(\)](#page-141-5), [ST\\_GeometryCollectionFromWKB\(\)](#page-141-5), [GeomCollFromWKB\(\)](#page-140-0), and [GeometryCollectionFromWKB\(\)](#page-140-0) are synonyms. For more information, see the description of [ST\\_GeomCollFromWKB\(\)](#page-141-5).

[GeomCollFromWKB\(\)](#page-140-0) and [GeometryCollectionFromWKB\(\)](#page-140-0) are deprecated; expect them to be removed in a future MySQL release. Use [ST\\_GeomCollFromWKB\(\)](#page-141-5) and [ST\\_GeometryCollectionFromWKB\(\)](#page-141-5) instead.

<span id="page-140-1"></span>• [GeomFromWKB\(](#page-140-1)wkb [, srid]), [GeometryFromWKB\(](#page-140-1)wkb [, srid])

[ST\\_GeomFromWKB\(\)](#page-142-0), [ST\\_GeometryFromWKB\(\)](#page-142-0), [GeomFromWKB\(\)](#page-140-1), and [GeometryFromWKB\(\)](#page-140-1) are synonyms. For more information, see the description of [ST\\_GeomFromWKB\(\)](#page-142-0).

[GeomFromWKB\(\)](#page-140-1) and [GeometryFromWKB\(\)](#page-140-1) are deprecated; expect them to be removed in a future MySQL release. Use [ST\\_GeomFromWKB\(\)](#page-142-0) and [ST\\_GeometryFromWKB\(\)](#page-142-0) instead.

<span id="page-140-2"></span>• [LineFromWKB\(](#page-140-2)wkb [, srid]), [LineStringFromWKB\(](#page-140-2)wkb [, srid])

```
ST_LineFromWKB(), ST_LineStringFromWKB(), LineFromWKB(), and
LineStringFromWKB() are synonyms. For more information, see the description of
ST_LineFromWKB().
```

[LineFromWKB\(\)](#page-140-2) and [LineStringFromWKB\(\)](#page-140-2) are deprecated; expect them to be removed in a future MySQL release. Use [ST\\_LineFromWKB\(\)](#page-142-1) and [ST\\_LineStringFromWKB\(\)](#page-142-1) instead.

<span id="page-141-0"></span>• [MLineFromWKB\(](#page-141-0)wkb [, srid]), [MultiLineStringFromWKB\(](#page-141-0)wkb [, srid])

[ST\\_MLineFromWKB\(\)](#page-142-2), [ST\\_MultiLineStringFromWKB\(\)](#page-142-2), [MLineFromWKB\(\)](#page-141-0), and [MultiLineStringFromWKB\(\)](#page-141-0) are synonyms. For more information, see the description of [ST\\_MLineFromWKB\(\)](#page-142-2).

[MLineFromWKB\(\)](#page-141-0) and [MultiLineStringFromWKB\(\)](#page-141-0) are deprecated; expect them to be removed in a future MySQL release. Use [ST\\_MLineFromWKB\(\)](#page-142-2) and [ST\\_MultiLineStringFromWKB\(\)](#page-142-2) instead.

<span id="page-141-1"></span>• [MPointFromWKB\(](#page-141-1)wkb [, srid]), [MultiPointFromWKB\(](#page-141-1)wkb [, srid])

[ST\\_MPointFromWKB\(\)](#page-142-3), [ST\\_MultiPointFromWKB\(\)](#page-142-3), [MPointFromWKB\(\)](#page-141-1), and [MultiPointFromWKB\(\)](#page-141-1) are synonyms. For more information, see the description of [ST\\_MPointFromWKB\(\)](#page-142-3).

[MPointFromWKB\(\)](#page-141-1) and [MultiPointFromWKB\(\)](#page-141-1) are deprecated; expect them to be removed in a future MySQL release. Use [ST\\_MPointFromWKB\(\)](#page-142-3) and [ST\\_MultiPointFromWKB\(\)](#page-142-3) instead.

<span id="page-141-2"></span>• [MPolyFromWKB\(](#page-141-2)wkb [, srid]), [MultiPolygonFromWKB\(](#page-141-2)wkb [, srid])

[ST\\_MPolyFromWKB\(\)](#page-142-4), [ST\\_MultiPolygonFromWKB\(\)](#page-142-4), [MPolyFromWKB\(\)](#page-141-2), and [MultiPolygonFromWKB\(\)](#page-141-2) are synonyms. For more information, see the description of [ST\\_MPolyFromWKB\(\)](#page-142-4).

[MPolyFromWKB\(\)](#page-141-2) and [MultiPolygonFromWKB\(\)](#page-141-2) are deprecated; expect them to be removed in a future MySQL release. Use [ST\\_MPolyFromWKB\(\)](#page-142-4) and [ST\\_MultiPolygonFromWKB\(\)](#page-142-4) instead.

<span id="page-141-3"></span>• [PointFromWKB\(](#page-141-3)wkb [, srid])

[ST\\_PointFromWKB\(\)](#page-142-5) and [PointFromWKB\(\)](#page-141-3) are synonyms. For more information, see the description of [ST\\_PointFromWKB\(\)](#page-142-5).

[PointFromWKB\(\)](#page-141-3) is deprecated; expect it to be removed in a future MySQL release. Use [ST\\_PointFromWKB\(\)](#page-142-5) instead.

<span id="page-141-4"></span>• [PolyFromWKB\(](#page-141-4)wkb [, srid]), [PolygonFromWKB\(](#page-141-4)wkb [, srid])

[ST\\_PolyFromWKB\(\)](#page-142-6), [ST\\_PolygonFromWKB\(\)](#page-142-6), [PolyFromWKB\(\)](#page-141-4), and [PolygonFromWKB\(\)](#page-141-4) are synonyms. For more information, see the description of [ST\\_PolyFromWKB\(\)](#page-142-6).

[PolyFromWKB\(\)](#page-141-4) and [PolygonFromWKB\(\)](#page-141-4) are deprecated; expect them to be removed in a future MySQL release. Use [ST\\_PolyFromWKB\(\)](#page-142-6) and [ST\\_PolygonFromWKB\(\)](#page-142-6) instead.

<span id="page-141-5"></span>• [ST\\_GeomCollFromWKB\(](#page-141-5)wkb [, srid]), [ST\\_GeometryCollectionFromWKB\(](#page-141-5)wkb [, [srid](#page-141-5)])

Constructs a GeometryCollection value using its WKB representation and SRID.

The result is NULL if the WKB or SRID argument is NULL.

[ST\\_GeomCollFromWKB\(\)](#page-141-5), [ST\\_GeometryCollectionFromWKB\(\)](#page-141-5), [GeomCollFromWKB\(\)](#page-140-0), and [GeometryCollectionFromWKB\(\)](#page-140-0) are synonyms.

```
• ST_GeomFromWKB(wkb [, srid]), ST_GeometryFromWKB(wkb [, srid])
 Constructs a geometry value of any type using its WKB representation and SRID.
 The result is NULL if the WKB or SRID argument is NULL.
 ST_GeomFromWKB(), ST_GeometryFromWKB(), GeomFromWKB(), and GeometryFromWKB()
 are synonyms.
• ST_LineFromWKB(wkb [, srid]), ST_LineStringFromWKB(wkb [, srid])
 Constructs a LineString value using its WKB representation and SRID.
 The result is NULL if the WKB or SRID argument is NULL.
 ST_LineFromWKB(), ST_LineStringFromWKB(), LineFromWKB(), and
 LineStringFromWKB() are synonyms.
• ST_MLineFromWKB(wkb [, srid]), ST_MultiLineStringFromWKB(wkb [, srid])
 Constructs a MultiLineString value using its WKB representation and SRID.
 The result is NULL if the WKB or SRID argument is NULL.
 ST_MLineFromWKB(), ST_MultiLineStringFromWKB(), MLineFromWKB(), and
 MultiLineStringFromWKB() are synonyms.
• ST_MPointFromWKB(wkb [, srid]), ST_MultiPointFromWKB(wkb [, srid])
 Constructs a MultiPoint value using its WKB representation and SRID.
 The result is NULL if the WKB or SRID argument is NULL.
 ST_MPointFromWKB(), ST_MultiPointFromWKB(), MPointFromWKB(), and
 MultiPointFromWKB() are synonyms.
• ST_MPolyFromWKB(wkb [, srid]), ST_MultiPolygonFromWKB(wkb [, srid])
 Constructs a MultiPolygon value using its WKB representation and SRID.
 The result is NULL if the WKB or SRID argument is NULL.
 ST_MPolyFromWKB(), ST_MultiPolygonFromWKB(), MPolyFromWKB(), and
 MultiPolygonFromWKB() are synonyms.
• ST_PointFromWKB(wkb [, srid])
 Constructs a Point value using its WKB representation and SRID.
 The result is NULL if the WKB or SRID argument is NULL.
 ST_PointFromWKB() and PointFromWKB() are synonyms.
• ST_PolyFromWKB(wkb [, srid]), ST_PolygonFromWKB(wkb [, srid])
 Constructs a Polygon value using its WKB representation and SRID.
 The result is NULL if the WKB or SRID argument is NULL.
 ST_PolyFromWKB(), ST_PolygonFromWKB(), PolyFromWKB(), and PolygonFromWKB() are
```

<span id="page-142-6"></span><span id="page-142-5"></span><span id="page-142-4"></span>synonyms.

## <span id="page-143-8"></span>**12.16.5 MySQL-Specific Functions That Create Geometry Values**

MySQL provides a set of useful nonstandard functions for creating geometry values. The functions described in this section are MySQL extensions to the OpenGIS specification.

These functions produce geometry objects from either WKB values or geometry objects as arguments. If any argument is not a proper WKB or geometry representation of the proper object type, the return value is NULL.

For example, you can insert the geometry return value from [Point\(\)](#page-143-6) directly into a POINT column:

```
INSERT INTO t1 (pt_col) VALUES(Point(1,2));
```

<span id="page-143-1"></span>• [GeometryCollection\(](#page-143-1)g [, g] ...)

Constructs a GeometryCollection value from the geometry arguments.

[GeometryCollection\(\)](#page-143-1) returns all the proper geometries contained in the arguments even if a nonsupported geometry is present.

[GeometryCollection\(\)](#page-143-1) with no arguments is permitted as a way to create an empty geometry.

<span id="page-143-2"></span>• [LineString\(](#page-143-2)pt [, pt] ...)

Constructs a LineString value from a number of Point or WKB Point arguments. If the number of arguments is less than two, the return value is NULL.

<span id="page-143-3"></span>• [MultiLineString\(](#page-143-3)ls [, ls] ...)

Constructs a MultiLineString value using LineString or WKB LineString arguments.

<span id="page-143-4"></span>• [MultiPoint\(](#page-143-4)pt [, pt2] ...)

Constructs a MultiPoint value using Point or WKB Point arguments.

<span id="page-143-5"></span>• [MultiPolygon\(](#page-143-5)poly [, poly] ...)

Constructs a MultiPolygon value from a set of Polygon or WKB Polygon arguments.

<span id="page-143-6"></span>• [Point\(](#page-143-6)x, y)

Constructs a Point using its coordinates.

<span id="page-143-7"></span>• [Polygon\(](#page-143-7)ls [, ls] ...)

Constructs a Polygon value from a number of LineString or WKB LineString arguments. If any argument does not represent a LinearRing (that is, not a closed and simple LineString), the return value is NULL.