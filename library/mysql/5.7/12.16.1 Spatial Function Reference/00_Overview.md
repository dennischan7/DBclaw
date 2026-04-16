---
source: MySQL 5.7 Reference
title: 00_Overview
---

The following table lists each spatial function and provides a short description of each one.

**Table 12.21 Spatial Functions**

| Name                | Description                                     | Deprecated |
|---------------------|-------------------------------------------------|------------|
| Area()              | Return Polygon or MultiPolygon<br>area          | Yes        |
| AsBinary(), AsWKB() | Convert from internal geometry<br>format to WKB | Yes        |
| AsText(), AsWKT()   | Convert from internal geometry<br>format to WKT | Yes        |

| Name                                                | Description                                                      | Deprecated |
|-----------------------------------------------------|------------------------------------------------------------------|------------|
| Buffer()                                            | Return geometry of points within<br>given distance from geometry | Yes        |
| Centroid()                                          | Return centroid as a point                                       | Yes        |
| Contains()                                          | Whether MBR of one geometry<br>contains MBR of another           | Yes        |
| ConvexHull()                                        | Return convex hull of geometry                                   | Yes        |
| Crosses()                                           | Whether one geometry crosses<br>another                          | Yes        |
| Dimension()                                         | Dimension of geometry                                            | Yes        |
| Disjoint()                                          | Whether MBRs of two<br>geometries are disjoint                   | Yes        |
| EndPoint()                                          | End Point of LineString                                          | Yes        |
| Envelope()                                          | Return MBR of geometry                                           | Yes        |
| Equals()                                            | Whether MBRs of two<br>geometries are equal                      | Yes        |
| ExteriorRing()                                      | Return exterior ring of Polygon                                  | Yes        |
| GeomCollFromText(),<br>GeometryCollectionFromText() | Return geometry collection from<br>WKT                           | Yes        |
| GeomCollFromWKB(),<br>GeometryCollectionFromWKB()   | Return geometry collection from<br>WKB                           | Yes        |
| GeometryCollection()                                | Construct geometry collection<br>from geometries                 |            |
| GeometryN()                                         | Return N-th geometry from<br>geometry collection                 | Yes        |
| GeometryType()                                      | Return name of geometry type                                     | Yes        |
| GeomFromText(),<br>GeometryFromText()               | Return geometry from WKT                                         | Yes        |
| GeomFromWKB(),<br>GeometryFromWKB()                 | Return geometry from WKB                                         | Yes        |
| GLength()                                           | Return length of LineString                                      | Yes        |
| InteriorRingN()                                     | Return N-th interior ring of<br>Polygon                          | Yes        |
| Intersects()                                        | Whether MBRs of two<br>geometries intersect                      | Yes        |
| IsClosed()                                          | Whether a geometry is closed<br>and simple                       | Yes        |
| IsEmpty()                                           | Whether a geometry is empty                                      | Yes        |
| IsSimple()                                          | Whether a geometry is simple                                     | Yes        |
| LineFromText(),<br>LineStringFromText()             | Construct LineString from WKT                                    | Yes        |
| LineFromWKB(),<br>LineStringFromWKB()               | Construct LineString from WKB                                    | Yes        |
| LineString()                                        | Construct LineString from Point<br>values                        |            |
| MBRContains()                                       | Whether MBR of one geometry<br>contains MBR of another           |            |

| Name                                          | Description                                             | Deprecated |
|-----------------------------------------------|---------------------------------------------------------|------------|
| MBRCoveredBy()                                | Whether one MBR is covered by<br>another                |            |
| MBRCovers()                                   | Whether one MBR covers<br>another                       |            |
| MBRDisjoint()                                 | Whether MBRs of two<br>geometries are disjoint          |            |
| MBREqual()                                    | Whether MBRs of two<br>geometries are equal             | Yes        |
| MBREquals()                                   | Whether MBRs of two<br>geometries are equal             |            |
| MBRIntersects()                               | Whether MBRs of two<br>geometries intersect             |            |
| MBROverlaps()                                 | Whether MBRs of two<br>geometries overlap               |            |
| MBRTouches()                                  | Whether MBRs of two<br>geometries touch                 |            |
| MBRWithin()                                   | Whether MBR of one geometry is<br>within MBR of another |            |
| MLineFromText(),<br>MultiLineStringFromText() | Construct MultiLineString from<br>WKT                   | Yes        |
| MLineFromWKB(),<br>MultiLineStringFromWKB()   | Construct MultiLineString from<br>WKB                   | Yes        |
| MPointFromText(),<br>MultiPointFromText()     | Construct MultiPoint from WKT                           | Yes        |
| MPointFromWKB(),<br>MultiPointFromWKB()       | Construct MultiPoint from WKB                           | Yes        |
| MPolyFromText(),<br>MultiPolygonFromText()    | Construct MultiPolygon from<br>WKT                      | Yes        |
| MPolyFromWKB(),<br>MultiPolygonFromWKB()      | Construct MultiPolygon from<br>WKB                      | Yes        |
| MultiLineString()                             | Contruct MultiLineString from<br>LineString values      |            |
| MultiPoint()                                  | Construct MultiPoint from Point<br>values               |            |
| MultiPolygon()                                | Construct MultiPolygon from<br>Polygon values           |            |
| NumGeometries()                               | Return number of geometries in<br>geometry collection   | Yes        |
| NumInteriorRings()                            | Return number of interior rings in<br>Polygon           | Yes        |
| NumPoints()                                   | Return number of points in<br>LineString                | Yes        |
| Overlaps()                                    | Whether MBRs of two<br>geometries overlap               | Yes        |
| Point()                                       | Construct Point from coordinates                        |            |
| PointFromText()                               | Construct Point from WKT                                | Yes        |
| PointFromWKB()                                | Construct Point from WKB                                | Yes        |

| Name                                 | Description                                                      | Deprecated |
|--------------------------------------|------------------------------------------------------------------|------------|
| PointN()                             | Return N-th point from LineString Yes                            |            |
| PolyFromText(),<br>PolygonFromText() | Construct Polygon from WKT                                       | Yes        |
| PolyFromWKB(),<br>PolygonFromWKB()   | Construct Polygon from WKB                                       | Yes        |
| Polygon()                            | Construct Polygon from<br>LineString arguments                   |            |
| Distance()                           | The distance of one geometry<br>from another                     | Yes        |
| SRID()                               | Return spatial reference system<br>ID for geometry               | Yes        |
| ST_Area()                            | Return Polygon or MultiPolygon<br>area                           |            |
| ST_AsBinary(), ST_AsWKB()            | Convert from internal geometry<br>format to WKB                  |            |
| ST_AsGeoJSON()                       | Generate GeoJSON object from<br>geometry                         |            |
| ST_AsText(), ST_AsWKT()              | Convert from internal geometry<br>format to WKT                  |            |
| ST_Buffer()                          | Return geometry of points within<br>given distance from geometry |            |
| ST_Buffer_Strategy()                 | Produce strategy option for<br>ST_Buffer()                       |            |
| ST_Centroid()                        | Return centroid as a point                                       |            |
| ST_Contains()                        | Whether one geometry contains<br>another                         |            |
| ST_ConvexHull()                      | Return convex hull of geometry                                   |            |
| ST_Crosses()                         | Whether one geometry crosses<br>another                          |            |
| ST_Difference()                      | Return point set difference of two<br>geometries                 |            |
| ST_Dimension()                       | Dimension of geometry                                            |            |
| ST_Disjoint()                        | Whether one geometry is disjoint<br>from another                 |            |
| ST_Distance()                        | The distance of one geometry<br>from another                     |            |
| ST_Distance_Sphere()                 | Minimum distance on earth<br>between two geometries              |            |
| ST_EndPoint()                        | End Point of LineString                                          |            |
| ST_Envelope()                        | Return MBR of geometry                                           |            |
| ST_Equals()                          | Whether one geometry is equal<br>to another                      |            |
| ST_ExteriorRing()                    | Return exterior ring of Polygon                                  |            |
| ST_GeoHash()                         | Produce a geohash value                                          |            |

| Name                                                     | Description                                        | Deprecated |
|----------------------------------------------------------|----------------------------------------------------|------------|
| ST_GeomCollFromText(),                                   | Return geometry collection from                    |            |
| ST_GeometryCollectionFromText(),<br>ST_GeomCollFromTxt() | WKT                                                |            |
| ST_GeomCollFromWKB(),                                    | Return geometry collection from                    |            |
| ST_GeometryCollectionFromWKB()                           | WKB                                                |            |
| ST_GeometryN()                                           | Return N-th geometry from<br>geometry collection   |            |
| ST_GeometryType()                                        | Return name of geometry type                       |            |
| ST_GeomFromGeoJSON()                                     | Generate geometry from<br>GeoJSON object           |            |
| ST_GeomFromText(),<br>ST_GeometryFromText()              | Return geometry from WKT                           |            |
| ST_GeomFromWKB(),<br>ST_GeometryFromWKB()                | Return geometry from WKB                           |            |
| ST_InteriorRingN()                                       | Return N-th interior ring of<br>Polygon            |            |
| ST_Intersection()                                        | Return point set intersection of<br>two geometries |            |
| ST_Intersects()                                          | Whether one geometry intersects<br>another         |            |
| ST_IsClosed()                                            | Whether a geometry is closed<br>and simple         |            |
| ST_IsEmpty()                                             | Whether a geometry is empty                        |            |
| ST_IsSimple()                                            | Whether a geometry is simple                       |            |
| ST_IsValid()                                             | Whether a geometry is valid                        |            |
| ST_LatFromGeoHash()                                      | Return latitude from geohash<br>value              |            |
| ST_Length()                                              | Return length of LineString                        |            |
| ST_LineFromText(),<br>ST_LineStringFromText()            | Construct LineString from WKT                      |            |
| ST_LineFromWKB(),                                        | Construct LineString from WKB                      |            |
| ST_LineStringFromWKB()                                   |                                                    |            |
| ST_LongFromGeoHash()                                     | Return longitude from geohash<br>value             |            |
| ST_MakeEnvelope()                                        | Rectangle around two points                        |            |
| ST_MLineFromText(),<br>ST_MultiLineStringFromText()      | Construct MultiLineString from<br>WKT              |            |
| ST_MLineFromWKB(),<br>ST_MultiLineStringFromWKB()        | Construct MultiLineString from<br>WKB              |            |
| ST_MPointFromText(),<br>ST_MultiPointFromText()          | Construct MultiPoint from WKT                      |            |
| ST_MPointFromWKB(),<br>ST_MultiPointFromWKB()            | Construct MultiPoint from WKB                      |            |
| ST_MPolyFromText(),<br>ST_MultiPolygonFromText()         | Construct MultiPolygon from<br>WKT                 |            |
| ST_MPolyFromWKB(),<br>ST_MultiPolygonFromWKB()           | Construct MultiPolygon from<br>WKB                 |            |

| Name                                           | Description                                                | Deprecated |
|------------------------------------------------|------------------------------------------------------------|------------|
| ST_NumGeometries()                             | Return number of geometries in<br>geometry collection      |            |
| ST_NumInteriorRing(),<br>ST_NumInteriorRings() | Return number of interior rings in<br>Polygon              |            |
| ST_NumPoints()                                 | Return number of points in<br>LineString                   |            |
| ST_Overlaps()                                  | Whether one geometry overlaps<br>another                   |            |
| ST_PointFromGeoHash()                          | Convert geohash value to POINT<br>value                    |            |
| ST_PointFromText()                             | Construct Point from WKT                                   |            |
| ST_PointFromWKB()                              | Construct Point from WKB                                   |            |
| ST_PointN()                                    | Return N-th point from LineString                          |            |
| ST_PolyFromText(),<br>ST_PolygonFromText()     | Construct Polygon from WKT                                 |            |
| ST_PolyFromWKB(),<br>ST_PolygonFromWKB()       | Construct Polygon from WKB                                 |            |
| ST_Simplify()                                  | Return simplified geometry                                 |            |
| ST_SRID()                                      | Return spatial reference system<br>ID for geometry         |            |
| ST_StartPoint()                                | Start Point of LineString                                  |            |
| ST_SymDifference()                             | Return point set symmetric<br>difference of two geometries |            |
| ST_Touches()                                   | Whether one geometry touches<br>another                    |            |
| ST_Union()                                     | Return point set union of two<br>geometries                |            |
| ST_Validate()                                  | Return validated geometry                                  |            |
| ST_Within()                                    | Whether one geometry is within<br>another                  |            |
| ST_X()                                         | Return X coordinate of Point                               |            |
| ST_Y()                                         | Return Y coordinate of Point                               |            |
| StartPoint()                                   | Start Point of LineString                                  | Yes        |
| Touches()                                      | Whether one geometry touches<br>another                    | Yes        |
| Within()                                       | Whether MBR of one geometry is<br>within MBR of another    | Yes        |
| X()                                            | Return X coordinate of Point                               | Yes        |
| Y()                                            | Return Y coordinate of Point                               | Yes        |