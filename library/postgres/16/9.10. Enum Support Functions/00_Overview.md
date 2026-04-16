---
source: PostgreSQL 16 Reference
title: 00_Overview
---

For enum types (described in [Section 8.7](#page-4-1)), there are several functions that allow cleaner programming without hard-coding particular values of an enum type. These are listed in [Table 9.35](#page-127-0). The examples assume an enum type created as:

```
CREATE TYPE rainbow AS ENUM ('red', 'orange', 'yellow', 'green',
 'blue', 'purple');
```

### <span id="page-127-0"></span>**Table 9.35. Enum Support Functions**

```
Function
       Description
       Example(s)
enum_first ( anyenum ) → anyenum
       Returns the first value of the input enum type.
       enum_first(null::rainbow) → red
enum_last ( anyenum ) → anyenum
       Returns the last value of the input enum type.
       enum_last(null::rainbow) → purple
enum_range ( anyenum ) → anyarray
       Returns all values of the input enum type in an ordered array.
       enum_range(null::rainbow) → {red,orange,yellow,
       green,blue,purple}
enum_range ( anyenum, anyenum ) → anyarray
       Returns the range between the two given enum values, as an ordered array. The values
       must be from the same enum type. If the first parameter is null, the result will start with
       the first value of the enum type. If the second parameter is null, the result will end with
       the last value of the enum type.
       enum_range('orange'::rainbow, 'green'::rainbow) → {or-
       ange,yellow,green}
       enum_range(NULL, 'green'::rainbow) → {red,orange,yel-
       low,green}
       enum_range('orange'::rainbow, NULL) → {orange,yellow,green,
       blue,purple}
```

Notice that except for the two-argument form of enum\_range, these functions disregard the specific value passed to them; they care only about its declared data type. Either null or a specific value of the type can be passed, with the same result. It is more common to apply these functions to a table column or function argument than to a hardwired type name as used in the examples.

# <span id="page-128-0"></span>**9.11. Geometric Functions and Operators**

The geometric types point, box, lseg, line, path, polygon, and circle have a large set of native support functions and operators, shown in [Table 9.36,](#page-128-1) [Table 9.37,](#page-131-0) and [Table 9.38](#page-132-0).

### <span id="page-128-1"></span>**Table 9.36. Geometric Operators**

```
Operator
       Description
       Example(s)
geometric_type + point → geometric_type
       Adds the coordinates of the second point to those of each point of the first argument,
       thus performing translation. Available for point, box, path, circle.
       box '(1,1),(0,0)' + point '(2,0)' → (3,1),(2,0)
path + path → path
       Concatenates two open paths (returns NULL if either path is closed).
       path '[(0,0),(1,1)]' + path '[(2,2),(3,3),(4,4)]' → [(0,0),
       (1,1),(2,2),(3,3),(4,4)]
geometric_type - point → geometric_type
       Subtracts the coordinates of the second point from those of each point of the first argu-
       ment, thus performing translation. Available for point, box, path, circle.
       box '(1,1),(0,0)' - point '(2,0)' → (-1,1),(-2,0)
geometric_type * point → geometric_type
       Multiplies each point of the first argument by the second point (treating a point as be-
       ing a complex number represented by real and imaginary parts, and performing standard
       complex multiplication). If one interprets the second point as a vector, this is equiva-
       lent to scaling the object's size and distance from the origin by the length of the vector,
       and rotating it counterclockwise around the origin by the vector's angle from the x axis.
       Available for point, box,
                               a path, circle.
       path '((0,0),(1,0),(1,1))' * point '(3.0,0)' → ((0,0),(3,0),
       (3,3))
       path '((0,0),(1,0),(1,1))' * point(cosd(45), sind(45))
       → ((0,0),(0.7071067811865475,0.7071067811865475),
       (0,1.414213562373095))
geometric_type / point → geometric_type
       Divides each point of the first argument by the second point (treating a point as being a
       complex number represented by real and imaginary parts, and performing standard com-
       plex division). If one interprets the second point as a vector, this is equivalent to scal-
       ing the object's size and distance from the origin down by the length of the vector, and
       rotating it clockwise around the origin by the vector's angle from the x axis. Available
       for point, box,
                      a path, circle.
       path '((0,0),(1,0),(1,1))' / point '(2.0,0)' → ((0,0),
       (0.5,0),(0.5,0.5))
       path '((0,0),(1,0),(1,1))' / point(cosd(45), sind(45))
       → ((0,0),(0.7071067811865476,-0.7071067811865476),
       (1.4142135623730951,0))
@-@ geometric_type → double precision
       Computes the total length. Available for lseg, path.
       @-@ path '[(0,0),(1,0),(1,1)]' → 2
@@ geometric_type → point
```

#### **Operator**

### **Description**

#### **Example(s)**

Computes the center point. Available for box, lseg, polygon, circle.

```
@@ box '(2,2),(0,0)' → (1,1)
```

# geometric\_type → integer

Returns the number of points. Available for path, polygon.

```
# path '((1,0),(0,1),(-1,0))' → 3
```

geometric\_type # geometric\_type → point

Computes the point of intersection, or NULL if there is none. Available for lseg, line.

```
lseg '[(0,0),(1,1)]' # lseg '[(1,0),(0,1)]' → (0.5,0.5)
```

box # box → box

Computes the intersection of two boxes, or NULL if there is none.

box '(2,2), 
$$(-1,-1)$$
' # box '(1,1),  $(-2,-2)$ '  $\rightarrow$  (1,1),  $(-1,-1)$ 

geometric\_type ## geometric\_type → point

Computes the closest point to the first object on the second object. Available for these pairs of types: (point, box), (point, lseg), (point, line), (lseg, box), (lseg, lseg), (line, lseg).

```
point '(0,0)' ## lseg '[(2,0),(0,2)]' → (1,1)
```

geometric\_type <-> geometric\_type → double precision

Computes the distance between the objects. Available for all seven geometric types, for all combinations of point with another geometric type, and for these additional pairs of types: (box, lseg), (lseg, line), (polygon, circle) (and the commutator cases).

```
circle '<(0,0),1>' <-> circle '<(5,0),1>' → 3
```

geometric\_type @> geometric\_type → boolean

Does first object contain second? Available for these pairs of types: (box, point), (box, box), (path, point), (polygon, point), (polygon, polygon), (circle, point), (circle, circle).

```
circle '<(0,0),2>' @> point '(1,1)' → t
```

geometric\_type <@ geometric\_type → boolean

Is first object contained in or on second? Available for these pairs of types: (point, box), (point, lseg), (point, line), (point, path), (point, polygon), (point, circle), (box, box), (lseg, box), (lseg, line), (polygon, polygon), (circle, circle).

```
point '(1,1)' <@ circle '<(0,0),2>' → t
```

geometric\_type && geometric\_type → boolean

Do these objects overlap? (One point in common makes this true.) Available for box, polygon, circle.

```
box '(1,1),(0,0)' && box '(2,2),(0,0)' → t
```

geometric\_type << geometric\_type → boolean

Is first object strictly left of second? Available for point, box, polygon, circle.

```
circle '<(0,0),1>' << circle '<(5,0),1>' → t
```

geometric\_type >> geometric\_type → boolean

Is first object strictly right of second? Available for point, box, polygon, circle.

```
circle '<(5,0),1>' >> circle '<(0,0),1>' → t
```

```
Operator
       Description
       Example(s)
geometric_type &< geometric_type → boolean
       Does first object not extend to the right of second? Available for box, polygon, cir-
       cle.
       box '(1,1),(0,0)' &< box '(2,2),(0,0)' → t
geometric_type &> geometric_type → boolean
       Does first object not extend to the left of second? Available for box, polygon, cir-
       cle.
       box '(3,3),(0,0)' &> box '(2,2),(0,0)' → t
geometric_type <<| geometric_type → boolean
       Is first object strictly below second? Available for point, box, polygon, circle.
       box '(3,3),(0,0)' <<| box '(5,5),(3,4)' → t
geometric_type |>> geometric_type → boolean
       Is first object strictly above second? Available for point, box, polygon, circle.
       box '(5,5),(3,4)' |>> box '(3,3),(0,0)' → t
geometric_type &<| geometric_type → boolean
       Does first object not extend above second? Available for box, polygon, circle.
       box '(1,1),(0,0)' &<| box '(2,2),(0,0)' → t
geometric_type |&> geometric_type → boolean
       Does first object not extend below second? Available for box, polygon, circle.
       box '(3,3),(0,0)' |&> box '(2,2),(0,0)' → t
box <^ box → boolean
       Is first object below second (allows edges to touch)?
       box '((1,1),(0,0))' <^ box '((2,2),(1,1))' → t
box >^ box → boolean
       Is first object above second (allows edges to touch)?
       box '((2,2),(1,1))' >^ box '((1,1),(0,0))' → t
geometric_type ?# geometric_type → boolean
       Do these objects intersect? Available for these pairs of types: (box, box), (lseg, box),
       (lseg, lseg), (lseg, line), (line, box), (line, line), (path, path).
       lseg '[(-1,0),(1,0)]' ?# box '(2,2),(-2,-2)' → t
?- line → boolean
?- lseg → boolean
       Is line horizontal?
       ?- lseg '[(-1,0),(1,0)]' → t
point ?- point → boolean
       Are points horizontally aligned (that is, have same y coordinate)?
       point '(1,0)' ?- point '(0,0)' → t
?| line → boolean
?| lseg → boolean
       Is line vertical?
       ?| lseg '[(-1,0),(1,0)]' → f
```

## **Operator Description Example(s)** point ?| point → boolean Are points vertically aligned (that is, have same x coordinate)? point '(0,1)' ?| point '(0,0)' → t line ?-| line → boolean lseg ?-| lseg → boolean Are lines perpendicular? lseg '[(0,0),(0,1)]' ?-| lseg '[(0,0),(1,0)]' → t line ?|| line → boolean

lseg ?|| lseg → boolean

Are lines parallel?

lseg '[(-1,0),(1,0)]' ?|| lseg '[(-1,2),(1,2)]' → t

geometric\_type ~= geometric\_type → boolean

Are these objects the same? Available for point, box, polygon, circle.

polygon '((0,0),(1,1))' ~= polygon '((1,1),(0,0))' → t

### **Caution**

Note that the "same as" operator, ~=, represents the usual notion of equality for the point, box, polygon, and circle types. Some of the geometric types also have an = operator, but = compares for equal *areas* only. The other scalar comparison operators (<= and so on), where available for these types, likewise compare areas.

### **Note**

Before PostgreSQL 14, the point is strictly below/above comparison operators point <<| point and point |>> point were respectively called <^ and >^. These names are still available, but are deprecated and will eventually be removed.

#### <span id="page-131-0"></span>**Table 9.37. Geometric Functions**

## **Function Description Example(s)** area ( geometric\_type ) → double precision Computes area. Available for box, path, circle. A path input must be closed, else NULL is returned. Also, if the path is self-intersecting, the result may be meaningless. area(box '(2,2),(0,0)') → 4 center ( geometric\_type ) → point Computes center point. Available for box, circle. center(box '(1,2),(0,0)') → (0.5,1) diagonal ( box ) → lseg Extracts box's diagonal as a line segment (same as lseg(box)).

a "Rotating" a box with these operators only moves its corner points: the box is still considered to have sides parallel to the axes. Hence the box's size is not preserved, as a true rotation would do.

```
Function
      Description
      Example(s)
      diagonal(box '(1,2),(0,0)') → [(1,2),(0,0)]
diameter ( circle ) → double precision
      Computes diameter of circle.
      diameter(circle '<(0,0),2>') → 4
height ( box ) → double precision
      Computes vertical size of box.
      height(box '(1,2),(0,0)') → 2
isclosed ( path ) → boolean
      Is path closed?
      isclosed(path '((0,0),(1,1),(2,0))') → t
isopen ( path ) → boolean
      Is path open?
      isopen(path '[(0,0),(1,1),(2,0)]') → t
length ( geometric_type ) → double precision
      Computes the total length. Available for lseg, path.
      length(path '((-1,0),(1,0))') → 4
npoints ( geometric_type ) → integer
      Returns the number of points. Available for path, polygon.
      npoints(path '[(0,0),(1,1),(2,0)]') → 3
pclose ( path ) → path
      Converts path to closed form.
      pclose(path '[(0,0),(1,1),(2,0)]') → ((0,0),(1,1),(2,0))
popen ( path ) → path
      Converts path to open form.
      popen(path '((0,0),(1,1),(2,0))') → [(0,0),(1,1),(2,0)]
radius ( circle ) → double precision
      Computes radius of circle.
      radius(circle '<(0,0),2>') → 2
slope ( point, point ) → double precision
      Computes slope of a line drawn through the two points.
      slope(point '(0,0)', point '(2,1)') → 0.5
width ( box ) → double precision
      Computes horizontal size of box.
      width(box '(1,2),(0,0)') → 1
```

#### <span id="page-132-0"></span>**Table 9.38. Geometric Type Conversion Functions**

```
Function
        Description
        Example(s)
box ( circle ) → box
        Computes box inscribed within the circle.
```

```
Function
       Description
       Example(s)
       box(circle '<(0,0),2>') →
       (1.414213562373095,1.414213562373095),
       (-1.414213562373095,-1.414213562373095)
box ( point ) → box
       Converts point to empty box.
       box(point '(1,0)') → (1,0),(1,0)
box ( point, point ) → box
       Converts any two corner points to box.
       box(point '(0,1)', point '(1,0)') → (1,1),(0,0)
box ( polygon ) → box
       Computes bounding box of polygon.
       box(polygon '((0,0),(1,1),(2,0))') → (2,1),(0,0)
bound_box ( box, box ) → box
       Computes bounding box of two boxes.
       bound_box(box '(1,1),(0,0)', box '(4,4),(3,3)') → (4,4),
       (0,0)
circle ( box ) → circle
       Computes smallest circle enclosing box.
       circle(box '(1,1),(0,0)') → <(0.5,0.5),0.7071067811865476>
circle ( point, double precision ) → circle
       Constructs circle from center and radius.
       circle(point '(0,0)', 2.0) → <(0,0),2>
circle ( polygon ) → circle
       Converts polygon to circle. The circle's center is the mean of the positions of the poly-
       gon's points, and the radius is the average distance of the polygon's points from that cen-
       ter.
       circle(polygon '((0,0),(1,3),(2,0))') →
       <(1,1),1.6094757082487299>
line ( point, point ) → line
       Converts two points to the line through them.
       line(point '(-1,0)', point '(1,0)') → {0,-1,0}
lseg ( box ) → lseg
       Extracts box's diagonal as a line segment.
       lseg(box '(1,0),(-1,0)') → [(1,0),(-1,0)]
lseg ( point, point ) → lseg
       Constructs line segment from two endpoints.
       lseg(point '(-1,0)', point '(1,0)') → [(-1,0),(1,0)]
path ( polygon ) → path
       Converts polygon to a closed path with the same list of points.
       path(polygon '((0,0),(1,1),(2,0))') → ((0,0),(1,1),(2,0))
point ( double precision, double precision ) → point
       Constructs point from its coordinates.
```

```
Function
      Description
      Example(s)
      point(23.4, -44.5) → (23.4,-44.5)
point ( box ) → point
      Computes center of box.
      point(box '(1,0),(-1,0)') → (0,0)
point ( circle ) → point
      Computes center of circle.
      point(circle '<(0,0),2>') → (0,0)
point ( lseg ) → point
      Computes center of line segment.
      point(lseg '[(-1,0),(1,0)]') → (0,0)
point ( polygon ) → point
      Computes center of polygon (the mean of the positions of the polygon's points).
      point(polygon '((0,0),(1,1),(2,0))') →
      (1,0.3333333333333333)
polygon ( box ) → polygon
      Converts box to a 4-point polygon.
      polygon(box '(1,1),(0,0)') → ((0,0),(0,1),(1,1),(1,0))
polygon ( circle ) → polygon
      Converts circle to a 12-point polygon.
      polygon(circle '<(0,0),2>') → ((-2,0),
      (-1.7320508075688774,0.9999999999999999),
      (-1.0000000000000002,1.7320508075688772),
      (-1.2246063538223773e-16,2),
      (0.9999999999999996,1.7320508075688774),
      (1.732050807568877,1.0000000000000007),
      (2,2.4492127076447545e-16),
      (1.7320508075688776,-0.9999999999999994),
      (1.0000000000000009,-1.7320508075688767),
      (3.673819061467132e-16,-2),
      (-0.9999999999999987,-1.732050807568878),
      (-1.7320508075688767,-1.0000000000000009))
polygon ( integer, circle ) → polygon
      Converts circle to an n-point polygon.
      polygon(4, circle '<(3,0),1>') → ((2,0),(3,1),
      (4,1.2246063538223773e-16),(3,-1))
polygon ( path ) → polygon
      Converts closed path to a polygon with the same list of points.
      polygon(path '((0,0),(1,1),(2,0))') → ((0,0),(1,1),(2,0))
```

It is possible to access the two component numbers of a point as though the point were an array with indexes 0 and 1. For example, if t.p is a point column then SELECT p[0] FROM t retrieves the X coordinate and UPDATE t SET p[1] = ... changes the Y coordinate. In the same way, a value of type box or lseg can be treated as an array of two point values.

# <span id="page-135-0"></span>**9.12. Network Address Functions and Operators**

The IP network address types, cidr and inet, support the usual comparison operators shown in [Table 9.1](#page-56-0) as well as the specialized operators and functions shown in [Table 9.39](#page-135-1) and [Table 9.40.](#page-136-0)

Any cidr value can be cast to inet implicitly; therefore, the operators and functions shown below as operating on inet also work on cidr values. (Where there are separate functions for inet and cidr, it is because the behavior should be different for the two cases.) Also, it is permitted to cast an inet value to cidr. When this is done, any bits to the right of the netmask are silently zeroed to create a valid cidr value.

### <span id="page-135-1"></span>**Table 9.39. IP Address Operators**

```
Operator
       Description
       Example(s)
inet << inet → boolean
       Is subnet strictly contained by subnet? This operator, and the next four, test for subnet in-
       clusion. They consider only the network parts of the two addresses (ignoring any bits to
       the right of the netmasks) and determine whether one network is identical to or a subnet
       of the other.
       inet '192.168.1.5' << inet '192.168.1/24' → t
       inet '192.168.0.5' << inet '192.168.1/24' → f
       inet '192.168.1/24' << inet '192.168.1/24' → f
inet <<= inet → boolean
       Is subnet contained by or equal to subnet?
       inet '192.168.1/24' <<= inet '192.168.1/24' → t
inet >> inet → boolean
       Does subnet strictly contain subnet?
       inet '192.168.1/24' >> inet '192.168.1.5' → t
inet >>= inet → boolean
       Does subnet contain or equal subnet?
       inet '192.168.1/24' >>= inet '192.168.1/24' → t
inet && inet → boolean
       Does either subnet contain or equal the other?
       inet '192.168.1/24' && inet '192.168.1.80/28' → t
       inet '192.168.1/24' && inet '192.168.2.0/28' → f
~ inet → inet
       Computes bitwise NOT.
       ~ inet '192.168.1.6' → 63.87.254.249
inet & inet → inet
       Computes bitwise AND.
       inet '192.168.1.6' & inet '0.0.0.255' → 0.0.0.6
inet | inet → inet
       Computes bitwise OR.
       inet '192.168.1.6' | inet '0.0.0.255' → 192.168.1.255
```

```
Operator
      Description
      Example(s)
inet + bigint → inet
      Adds an offset to an address.
      inet '192.168.1.6' + 25 → 192.168.1.31
bigint + inet → inet
      Adds an offset to an address.
      200 + inet '::ffff:fff0:1' → ::ffff:255.240.0.201
inet - bigint → inet
      Subtracts an offset from an address.
      inet '192.168.1.43' - 36 → 192.168.1.7
inet - inet → bigint
      Computes the difference of two addresses.
      inet '192.168.1.43' - inet '192.168.1.19' → 24
      inet '::1' - inet '::ffff:1' → -4294901760
```

#### <span id="page-136-0"></span>**Table 9.40. IP Address Functions**

```
Function
       Description
       Example(s)
abbrev ( inet ) → text
       Creates an abbreviated display format as text. (The result is the same as the inet output
       function produces; it is "abbreviated" only in comparison to the result of an explicit cast
       to text, which for historical reasons will never suppress the netmask part.)
       abbrev(inet '10.1.0.0/32') → 10.1.0.0
abbrev ( cidr ) → text
       Creates an abbreviated display format as text. (The abbreviation consists of dropping all-
       zero octets to the right of the netmask; more examples are in Table 8.22.)
       abbrev(cidr '10.1.0.0/16') → 10.1/16
broadcast ( inet ) → inet
       Computes the broadcast address for the address's network.
       broadcast(inet '192.168.1.5/24') → 192.168.1.255/24
family ( inet ) → integer
       Returns the address's family: 4 for IPv4, 6 for IPv6.
       family(inet '::1') → 6
host ( inet ) → text
       Returns the IP address as text, ignoring the netmask.
       host(inet '192.168.1.0/24') → 192.168.1.0
hostmask ( inet ) → inet
       Computes the host mask for the address's network.
       hostmask(inet '192.168.23.20/30') → 0.0.0.3
inet_merge ( inet, inet ) → cidr
       Computes the smallest network that includes both of the given networks.
```

## **Function Description Example(s)** inet\_merge(inet '192.168.1.5/24', inet '192.168.2.5/24') → 192.168.0.0/22 inet\_same\_family ( inet, inet ) → boolean Tests whether the addresses belong to the same IP family. inet\_same\_family(inet '192.168.1.5/24', inet '::1') → f masklen ( inet ) → integer Returns the netmask length in bits. masklen(inet '192.168.1.5/24') → 24 netmask ( inet ) → inet Computes the network mask for the address's network. netmask(inet '192.168.1.5/24') → 255.255.255.0 network ( inet ) → cidr Returns the network part of the address, zeroing out whatever is to the right of the netmask. (This is equivalent to casting the value to cidr.) network(inet '192.168.1.5/24') → 192.168.1.0/24 set\_masklen ( inet, integer ) → inet Sets the netmask length for an inet value. The address part does not change. set\_masklen(inet '192.168.1.5/24', 16) → 192.168.1.5/16 set\_masklen ( cidr, integer ) → cidr Sets the netmask length for a cidr value. Address bits to the right of the new netmask are set to zero. set\_masklen(cidr '192.168.1.0/24', 16) → 192.168.0.0/16 text ( inet ) → text Returns the unabbreviated IP address and netmask length as text. (This has the same result as an explicit cast to text.) text(inet '192.168.1.5') → 192.168.1.5/32

### **Tip**

The abbrev, host, and text functions are primarily intended to offer alternative display formats for IP addresses.

The MAC address types, macaddr and macaddr8, support the usual comparison operators shown in [Table 9.1](#page-56-0) as well as the specialized functions shown in [Table 9.41](#page-137-0). In addition, they support the bitwise logical operators ~, & and | (NOT, AND and OR), just as shown above for IP addresses.

#### <span id="page-137-0"></span>**Table 9.41. MAC Address Functions**

#### **Function Description Example(s)**

trunc ( macaddr ) → macaddr

Sets the last 3 bytes of the address to zero. The remaining prefix can be associated with a particular manufacturer (using data not included in PostgreSQL).

### **Function Description Example(s)** trunc(macaddr '12:34:56:78:90:ab') → 12:34:56:00:00:00 trunc ( macaddr8 ) → macaddr8 Sets the last 5 bytes of the address to zero. The remaining prefix can be associated with a particular manufacturer (using data not included in PostgreSQL). trunc(macaddr8 '12:34:56:78:90:ab:cd:ef') → 12:34:56:00:00:00:00:00 macaddr8\_set7bit ( macaddr8 ) → macaddr8 Sets the 7th bit of the address to one, creating what is known as modified EUI-64, for inclusion in an IPv6 address. macaddr8\_set7bit(macaddr8 '00:34:56:ab:cd:ef') → 02:34:56:ff:fe:ab:cd:ef

# <span id="page-138-0"></span>**9.13. Text Search Functions and Operators**

[Table 9.42](#page-138-1), [Table 9.43](#page-139-0) and [Table 9.44](#page-143-0) summarize the functions and operators that are provided for full text searching. See Chapter 12 for a detailed explanation of PostgreSQL's text search facility.

### <span id="page-138-1"></span>**Table 9.42. Text Search Operators**

```
Operator
       Description
       Example(s)
tsvector @@ tsquery → boolean
tsquery @@ tsvector → boolean
       Does tsvector match tsquery? (The arguments can be given in either order.)
       to_tsvector('fat cats ate rats') @@ to_tsquery('cat & rat')
       → t
text @@ tsquery → boolean
       Does text string, after implicit invocation of to_tsvector(), match tsquery?
       'fat cats ate rats' @@ to_tsquery('cat & rat') → t
tsvector @@@ tsquery → boolean
tsquery @@@ tsvector → boolean
       This is a deprecated synonym for @@.
       to_tsvector('fat cats ate rats') @@@ to_tsquery('cat &
       rat') → t
tsvector || tsvector → tsvector
       Concatenates two tsvectors. If both inputs contain lexeme positions, the second in-
       put's positions are adjusted accordingly.
       'a:1 b:2'::tsvector || 'c:1 d:2 b:3'::tsvector → 'a':1
       'b':2,5 'c':3 'd':4
tsquery && tsquery → tsquery
       ANDs two tsquerys together, producing a query that matches documents that match
       both input queries.
       'fat | rat'::tsquery && 'cat'::tsquery → ( 'fat' | 'rat' ) &
       'cat'
```

## **Operator Description Example(s)** tsquery || tsquery → tsquery ORs two tsquerys together, producing a query that matches documents that match either input query. 'fat | rat'::tsquery || 'cat'::tsquery → 'fat' | 'rat' | 'cat' !! tsquery → tsquery Negates a tsquery, producing a query that matches documents that do not match the input query. !! 'cat'::tsquery → !'cat' tsquery <-> tsquery → tsquery Constructs a phrase query, which matches if the two input queries match at successive lexemes. to\_tsquery('fat') <-> to\_tsquery('rat') → 'fat' <-> 'rat' tsquery @> tsquery → boolean Does first tsquery contain the second? (This considers only whether all the lexemes appearing in one query appear in the other, ignoring the combining operators.) 'cat'::tsquery @> 'cat & rat'::tsquery → f tsquery <@ tsquery → boolean Is first tsquery contained in the second? (This considers only whether all the lexemes appearing in one query appear in the other, ignoring the combining operators.) 'cat'::tsquery <@ 'cat & rat'::tsquery → t 'cat'::tsquery <@ '!cat & rat'::tsquery → t

In addition to these specialized operators, the usual comparison operators shown in [Table 9.1](#page-56-0) are available for types tsvector and tsquery. These are not very useful for text searching but allow, for example, unique indexes to be built on columns of these types.

#### <span id="page-139-0"></span>**Table 9.43. Text Search Functions**

```
Function
       Description
       Example(s)
array_to_tsvector ( text[] ) → tsvector
       Converts an array of text strings to a tsvector. The given strings are used as lexemes
       as-is, without further processing. Array elements must not be empty strings or NULL.
       array_to_tsvector('{fat,cat,rat}'::text[]) → 'cat' 'fat'
        'rat'
get_current_ts_config ( ) → regconfig
       Returns the OID of the current default text search configuration (as set by default_tex-
       t_search_config).
       get_current_ts_config() → english
length ( tsvector ) → integer
       Returns the number of lexemes in the tsvector.
       length('fat:2,4 cat:3 rat:5A'::tsvector) → 3
numnode ( tsquery ) → integer
       Returns the number of lexemes plus operators in the tsquery.
```

```
Function
       Description
       Example(s)
       numnode('(fat & rat) | cat'::tsquery) → 5
plainto_tsquery ( [ config regconfig, ] query text ) → tsquery
       Converts text to a tsquery, normalizing words according to the specified or default
       configuration. Any punctuation in the string is ignored (it does not determine query oper-
       ators). The resulting query matches documents containing all non-stopwords in the text.
       plainto_tsquery('english', 'The Fat Rats') → 'fat' & 'rat'
phraseto_tsquery ( [ config regconfig, ] query text ) → tsquery
       Converts text to a tsquery, normalizing words according to the specified or default
       configuration. Any punctuation in the string is ignored (it does not determine query oper-
       ators). The resulting query matches phrases containing all non-stopwords in the text.
       phraseto_tsquery('english', 'The Fat Rats') → 'fat' <->
       'rat'
       phraseto_tsquery('english', 'The Cat and Rats') → 'cat' <2>
       'rat'
websearch_to_tsquery ( [ config regconfig, ] query text ) → tsquery
       Converts text to a tsquery, normalizing words according to the specified or default
       configuration. Quoted word sequences are converted to phrase tests. The word "or" is un-
       derstood as producing an OR operator, and a dash produces a NOT operator; other punc-
       tuation is ignored. This approximates the behavior of some common web search tools.
       websearch_to_tsquery('english', '"fat rat" or cat dog') →
       'fat' <-> 'rat' | 'cat' & 'dog'
querytree ( tsquery ) → text
       Produces a representation of the indexable portion of a tsquery. A result that is empty
       or just T indicates a non-indexable query.
       querytree('foo & ! bar'::tsquery) → 'foo'
setweight ( vector tsvector, weight "char" ) → tsvector
       Assigns the specified weight to each element of the vector.
       setweight('fat:2,4 cat:3 rat:5B'::tsvector, 'A') → 'cat':3A
       'fat':2A,4A 'rat':5A
setweight ( vector tsvector, weight "char", lexemes text[] ) → tsvector
       Assigns the specified weight to elements of the vector that are listed in lexemes.
       The strings in lexemes are taken as lexemes as-is, without further processing. Strings
       that do not match any lexeme in vector are ignored.
       setweight('fat:2,4 cat:3 rat:5,6B'::tsvector, 'A',
       '{cat,rat}') → 'cat':3A 'fat':2,4 'rat':5A,6A
strip ( tsvector ) → tsvector
       Removes positions and weights from the tsvector.
       strip('fat:2,4 cat:3 rat:5A'::tsvector) → 'cat' 'fat' 'rat'
to_tsquery ( [ config regconfig, ] query text ) → tsquery
       Converts text to a tsquery, normalizing words according to the specified or default
       configuration. The words must be combined by valid tsquery operators.
       to_tsquery('english', 'The & Fat & Rats') → 'fat' & 'rat'
to_tsvector ( [ config regconfig, ] document text ) → tsvector
       Converts text to a tsvector, normalizing words according to the specified or default
       configuration. Position information is included in the result.
```

```
Description
       Example(s)
       to_tsvector('english', 'The Fat Rats') → 'fat':2 'rat':3
to_tsvector ( [ config regconfig, ] document json ) → tsvector
to_tsvector ( [ config regconfig, ] document jsonb ) → tsvector
       Converts each string value in the JSON document to a tsvector, normalizing words
       according to the specified or default configuration. The results are then concatenated in
       document order to produce the output. Position information is generated as though one
       stopword exists between each pair of string values. (Beware that "document order" of the
       fields of a JSON object is implementation-dependent when the input is jsonb; observe
       the difference in the examples.)
       to_tsvector('english', '{"aa": "The Fat Rats", "b":
       "dog"}'::json) → 'dog':5 'fat':2 'rat':3
       to_tsvector('english', '{"aa": "The Fat Rats", "b":
       "dog"}'::jsonb) → 'dog':1 'fat':4 'rat':5
json_to_tsvector ( [ config regconfig, ] document json, filter jsonb ) →
       tsvector
jsonb_to_tsvector ( [ config regconfig, ] document jsonb, filter jsonb )
       → tsvector
       Selects each item in the JSON document that is requested by the filter and converts
       each one to a tsvector, normalizing words according to the specified or default con-
       figuration. The results are then concatenated in document order to produce the output.
       Position information is generated as though one stopword exists between each pair of se-
       lected items. (Beware that "document order" of the fields of a JSON object is implemen-
       tation-dependent when the input is jsonb.) The filter must be a jsonb array con-
       taining zero or more of these keywords: "string" (to include all string values), "nu-
       meric" (to include all numeric values), "boolean" (to include all boolean values),
       "key" (to include all keys), or "all" (to include all the above). As a special case, the
       filter can also be a simple JSON value that is one of these keywords.
       json_to_tsvector('english', '{"a": "The Fat Rats", "b":
       123}'::json, '["string", "numeric"]') → '123':5 'fat':2
       'rat':3
       json_to_tsvector('english', '{"cat": "The Fat Rats", "dog":
       123}'::json, '"all"') → '123':9 'cat':1 'dog':7 'fat':4
       'rat':5
ts_delete ( vector tsvector, lexeme text ) → tsvector
       Removes any occurrence of the given lexeme from the vector. The lexeme string is
       treated as a lexeme as-is, without further processing.
       ts_delete('fat:2,4 cat:3 rat:5A'::tsvector, 'fat') → 'cat':3
       'rat':5A
ts_delete ( vector tsvector, lexemes text[] ) → tsvector
       Removes any occurrences of the lexemes in lexemes from the vector. The strings
       in lexemes are taken as lexemes as-is, without further processing. Strings that do not
       match any lexeme in vector are ignored.
       ts_delete('fat:2,4 cat:3 rat:5A'::tsvector, AR-
       RAY['fat','rat']) → 'cat':3
```

ts\_filter ( vector tsvector, weights "char"[] ) → tsvector Selects only elements with the given weights from the vector.

```
Function
       Description
       Example(s)
       ts_filter('fat:2,4 cat:3b,7c rat:5A'::tsvector, '{a,b}') →
       'cat':3B 'rat':5A
ts_headline ( [ config regconfig, ] document text, query tsquery [, options
       text ] ) → text
       Displays, in an abbreviated form, the match(es) for the query in the document, which
       must be raw text not a tsvector. Words in the document are normalized according to
       the specified or default configuration before matching to the query. Use of this function
       is discussed in Section 12.3.4, which also describes the available options.
       ts_headline('The fat cat ate the rat.', 'cat') → The fat
       <b>cat</b> ate the rat.
ts_headline ( [ config regconfig, ] document json, query tsquery [, options
       text ] ) → text
ts_headline ( [ config regconfig, ] document jsonb, query tsquery [, op-
       tions text ] ) → text
       Displays, in an abbreviated form, match(es) for the query that occur in string values
       within the JSON document. See Section 12.3.4 for more details.
       ts_headline('{"cat":"raining cats and dogs"}'::jsonb,
       'cat') → {"cat": "raining <b>cats</b> and dogs"}
ts_rank ( [ weights real[], ] vector tsvector, query tsquery [, normaliza-
       tion integer ] ) → real
       Computes a score showing how well the vector matches the query. See Sec-
       tion 12.3.3 for details.
       ts_rank(to_tsvector('raining cats and dogs'), 'cat') →
       0.06079271
ts_rank_cd ( [ weights real[], ] vector tsvector, query tsquery [, normal-
       ization integer ] ) → real
       Computes a score showing how well the vector matches the query, using a cover
       density algorithm. See Section 12.3.3 for details.
       ts_rank_cd(to_tsvector('raining cats and dogs'), 'cat') →
       0.1
ts_rewrite ( query tsquery, target tsquery, substitute tsquery ) → ts-
       query
       Replaces occurrences of target with substitute within the query. See Sec-
       tion 12.4.2.1 for details.
       ts_rewrite('a & b'::tsquery, 'a'::tsquery, 'foo|bar'::ts-
       query) → 'b' & ( 'foo' | 'bar' )
ts_rewrite ( query tsquery, select text ) → tsquery
       Replaces portions of the query according to target(s) and substitute(s) obtained by exe-
       cuting a SELECT command. See Section 12.4.2.1 for details.
       SELECT ts_rewrite('a & b'::tsquery, 'SELECT t,s FROM alias-
       es') → 'b' & ( 'foo' | 'bar' )
tsquery_phrase ( query1 tsquery, query2 tsquery ) → tsquery
       Constructs a phrase query that searches for matches of query1 and query2 at succes-
       sive lexemes (same as <-> operator).
       tsquery_phrase(to_tsquery('fat'), to_tsquery('cat')) → 'fat'
       <-> 'cat'
```

```
Function
      Description
      Example(s)
tsquery_phrase ( query1 tsquery, query2 tsquery, distance integer ) →
      tsquery
      Constructs a phrase query that searches for matches of query1 and query2 that occur
      exactly distance lexemes apart.
      tsquery_phrase(to_tsquery('fat'), to_tsquery('cat'), 10) →
      'fat' <10> 'cat'
tsvector_to_array ( tsvector ) → text[]
      Converts a tsvector to an array of lexemes.
      tsvector_to_array('fat:2,4 cat:3 rat:5A'::tsvector) →
      {cat,fat,rat}
unnest ( tsvector ) → setof record ( lexeme text, positions smallint[],
      weights text )
      Expands a tsvector into a set of rows, one per lexeme.
      select * from unnest('cat:3 fat:2,4 rat:5A'::tsvector) →
       lexeme | positions | weights
      --------+-----------+---------
       cat | {3} | {D}
       fat | {2,4} | {D,D}
       rat | {5} | {A}
```

### **Note**

All the text search functions that accept an optional regconfig argument will use the configuration specified by default\_text\_search\_config when that argument is omitted.

The functions in [Table 9.44](#page-143-0) are listed separately because they are not usually used in everyday text searching operations. They are primarily helpful for development and debugging of new text search configurations.

### <span id="page-143-0"></span>**Table 9.44. Text Search Debugging Functions**

```
Function
       Description
       Example(s)
ts_debug ( [ config regconfig, ] document text ) → setof record ( alias
       text, description text, token text, dictionaries regdictionary[],
       dictionary regdictionary, lexemes text[] )
       Extracts and normalizes tokens from the document according to the specified or default
       text search configuration, and returns information about how each token was processed.
       See Section 12.8.1 for details.
       ts_debug('english', 'The Brightest supernovaes') →
       (asciiword,"Word, all ASCII",The,{english_stem},eng-
       lish_stem,{}) ...
ts_lexize ( dict regdictionary, token text ) → text[]
       Returns an array of replacement lexemes if the input token is known to the dictionary, or
       an empty array if the token is known to the dictionary but it is a stop word, or NULL if it
       is not a known word. See Section 12.8.3 for details.
```

```
Function
       Description
       Example(s)
       ts_lexize('english_stem', 'stars') → {star}
ts_parse ( parser_name text, document text ) → setof record ( tokid in-
       teger, token text )
       Extracts tokens from the document using the named parser. See Section 12.8.2 for de-
       tails.
       ts_parse('default', 'foo - bar') → (1,foo) ...
ts_parse ( parser_oid oid, document text ) → setof record ( tokid inte-
       ger, token text )
       Extracts tokens from the document using a parser specified by OID. See Section 12.8.2
       for details.
       ts_parse(3722, 'foo - bar') → (1,foo) ...
ts_token_type ( parser_name text ) → setof record ( tokid integer, alias
       text, description text )
       Returns a table that describes each type of token the named parser can recognize. See
       Section 12.8.2 for details.
       ts_token_type('default') → (1,asciiword,"Word, all
       ASCII") ...
ts_token_type ( parser_oid oid ) → setof record ( tokid integer, alias
       text, description text )
       Returns a table that describes each type of token a parser specified by OID can recog-
       nize. See Section 12.8.2 for details.
       ts_token_type(3722) → (1,asciiword,"Word, all ASCII") ...
ts_stat ( sqlquery text [, weights text ] ) → setof record ( word text, ndoc
       integer, nentry integer )
       Executes the sqlquery, which must return a single tsvector column, and returns
       statistics about each distinct lexeme contained in the data. See Section 12.4.4 for details.
       ts_stat('SELECT vector FROM apod') → (foo,10,15) ...
```

# <span id="page-144-0"></span>**9.14. UUID Functions**

PostgreSQL includes one function to generate a UUID:

```
gen_random_uuid () → uuid
```

This function returns a version 4 (random) UUID. This is the most commonly used type of UUID and is appropriate for most applications.

The uuid-ossp module provides additional functions that implement other standard algorithms for generating UUIDs.

PostgreSQL also provides the usual comparison operators shown in [Table 9.1](#page-56-0) for UUIDs.

# <span id="page-144-1"></span>**9.15. XML Functions**

The functions and function-like expressions described in this section operate on values of type xml. See [Section 8.13](#page-15-0) for information about the xml type. The function-like expressions xmlparse and xmlserialize for converting to and from type xml are documented there, not in this section.

Use of most of these functions requires PostgreSQL to have been built with configure --withlibxml.