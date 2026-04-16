---
source: MySQL 5.7 Reference
title: 00_Overview
---

MySQL supports the functions listed in this section for converting geometry values from internal geometry format to WKT or WKB format.

There are also functions to convert a string from WKT or WKB format to internal geometry format. See [Section 12.16.3, "Functions That Create Geometry Values from WKT Values",](#page-137-3) and [Section 12.16.4,](#page-140-4) ["Functions That Create Geometry Values from WKB Values"](#page-140-4).

<span id="page-143-0"></span>• [AsBinary\(](#page-143-0)g), [AsWKB\(](#page-143-0)g)

[ST\\_AsBinary\(\)](#page-144-2), [ST\\_AsWKB\(\)](#page-144-2), [AsBinary\(\)](#page-143-0), and [AsWKB\(\)](#page-143-0) are synonyms. For more information, see the description of [ST\\_AsBinary\(\)](#page-144-2).

[AsBinary\(\)](#page-143-0) and [AsWKB\(\)](#page-143-0) are deprecated; expect them to be removed in a future MySQL release. Use [ST\\_AsBinary\(\)](#page-144-2) and [ST\\_AsWKB\(\)](#page-144-2) instead.

<span id="page-144-0"></span>• [AsText\(](#page-144-0)g), [AsWKT\(](#page-144-0)g)

[ST\\_AsText\(\)](#page-144-3), [ST\\_AsWKT\(\)](#page-144-3), [AsText\(\)](#page-144-0), and [AsWKT\(\)](#page-144-0) are synonyms. For more information, see the description of [ST\\_AsText\(\)](#page-144-3).

[AsText\(\)](#page-144-0) and [AsWKT\(\)](#page-144-0) are deprecated; expect them to be removed in a future MySQL release. Use [ST\\_AsText\(\)](#page-144-3) and [ST\\_AsWKT\(\)](#page-144-3) instead.

<span id="page-144-2"></span>• [ST\\_AsBinary\(](#page-144-2)g), [ST\\_AsWKB\(](#page-144-2)g)

Converts a value in internal geometry format to its WKB representation and returns the binary result.

If the argument is NULL, the return value is NULL. If the argument is not a syntactically well-formed geometry, an [ER\\_GIS\\_INVALID\\_DATA](https://dev.mysql.com/doc/mysql-errors/5.7/en/server-error-reference.md#error_er_gis_invalid_data) error occurs.

```
SELECT ST_AsBinary(g) FROM geom;
 ST_AsBinary(), ST_AsWKB(), AsBinary(), and AsWKB() are synonyms.
• ST_AsText(g), ST_AsWKT(g)
```

<span id="page-144-3"></span>Converts a value in internal geometry format to its WKT representation and returns the string result.

If the argument is NULL, the return value is NULL. If the argument is not a syntactically well-formed geometry, an [ER\\_GIS\\_INVALID\\_DATA](https://dev.mysql.com/doc/mysql-errors/5.7/en/server-error-reference.md#error_er_gis_invalid_data) error occurs.

```
mysql> SET @g = 'LineString(1 1,2 2,3 3)';
mysql> SELECT ST_AsText(ST_GeomFromText(@g));
+--------------------------------+
| ST_AsText(ST_GeomFromText(@g)) |
+--------------------------------+
| LINESTRING(1 1,2 2,3 3) |
+--------------------------------+
```

[ST\\_AsText\(\)](#page-144-3), [ST\\_AsWKT\(\)](#page-144-3), [AsText\(\)](#page-144-0), and [AsWKT\(\)](#page-144-0) are synonyms.

Output for MultiPoint values includes parentheses around each point. For example:

```
mysql> SET @mp = 'MULTIPOINT(1 1, 2 2, 3 3)';
mysql> SELECT ST_AsText(ST_GeomFromText(@mp));
+---------------------------------+
| ST_AsText(ST_GeomFromText(@mp)) |
+---------------------------------+
| MULTIPOINT((1 1),(2 2),(3 3)) |
+---------------------------------+
```

# <span id="page-144-4"></span>**12.16.7 Geometry Property Functions**

Each function that belongs to this group takes a geometry value as its argument and returns some quantitative or qualitative property of the geometry. Some functions restrict their argument type. Such functions return NULL if the argument is of an incorrect geometry type. For example, the [ST\\_Area\(\)](#page-151-1) polygon function returns NULL if the object type is neither Polygon nor MultiPolygon.