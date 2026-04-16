---
source: PostgreSQL 16 Reference
title: 00_Overview
---

This section describes functions and operators for examining and manipulating binary strings, that is values of type bytea. Many of these are equivalent, in purpose and syntax, to the text-string functions described in the previous section.

SQL defines some string functions that use key words, rather than commas, to separate arguments. Details are in [Table 9.11](#page-78-0). PostgreSQL also provides versions of these functions that use the regular function invocation syntax (see [Table 9.12\)](#page-79-0).

#### <span id="page-78-0"></span>**Table 9.11. SQL Binary String Functions and Operators**

```
Function/Operator
       Description
       Example(s)
bytea || bytea → bytea
       Concatenates the two binary strings.
       '\x123456'::bytea || '\x789a00bcde'::bytea →
       \x123456789a00bcde
bit_length ( bytea ) → integer
       Returns number of bits in the binary string (8 times the octet_length).
       bit_length('\x123456'::bytea) → 24
btrim ( bytes bytea, bytesremoved bytea ) → bytea
       Removes the longest string containing only bytes appearing in bytesremoved from
       the start and end of bytes.
       btrim('\x1234567890'::bytea, '\x9012'::bytea) → \x345678
ltrim ( bytes bytea, bytesremoved bytea ) → bytea
       Removes the longest string containing only bytes appearing in bytesremoved from
       the start of bytes.
       ltrim('\x1234567890'::bytea, '\x9012'::bytea) → \x34567890
octet_length ( bytea ) → integer
       Returns number of bytes in the binary string.
       octet_length('\x123456'::bytea) → 3
overlay ( bytes bytea PLACING newsubstring bytea FROM start integer [
       FOR count integer ] ) → bytea
       Replaces the substring of bytes that starts at the start'th byte and extends for count
       bytes with newsubstring. If count is omitted, it defaults to the length of newsub-
       string.
       overlay('\x1234567890'::bytea placing '\002\003'::bytea
       from 2 for 3) → \x12020390
position ( substring bytea IN bytes bytea ) → integer
       Returns first starting index of the specified substring within bytes, or zero if it's
       not present.
       position('\x5678'::bytea in '\x1234567890'::bytea) → 3
```

### **Function/Operator Description Example(s)** rtrim ( bytes bytea, bytesremoved bytea ) → bytea Removes the longest string containing only bytes appearing in bytesremoved from the end of bytes. rtrim('\x1234567890'::bytea, '\x9012'::bytea) → \x12345678 substring ( bytes bytea [ FROM start integer ] [ FOR count integer ] ) → bytea Extracts the substring of bytes starting at the start'th byte if that is specified, and stopping after count bytes if that is specified. Provide at least one of start and count. substring('\x1234567890'::bytea from 3 for 2) → \x5678 trim ( [ LEADING | TRAILING | BOTH ] bytesremoved bytea FROM bytes bytea ) → bytea Removes the longest string containing only bytes appearing in bytesremoved from the start, end, or both ends (BOTH is the default) of bytes. trim('\x9012'::bytea from '\x1234567890'::bytea) → \x345678 trim ( [ LEADING | TRAILING | BOTH ] [ FROM ] bytes bytea, bytesremoved bytea ) → bytea This is a non-standard syntax for trim(). trim(both from '\x1234567890'::bytea, '\x9012'::bytea) → \x345678

Additional binary string manipulation functions are available and are listed in [Table 9.12](#page-79-0). Some of them are used internally to implement the SQL-standard string functions listed in [Table 9.11.](#page-78-0)

#### <span id="page-79-0"></span>**Table 9.12. Other Binary String Functions**

```
Function
       Description
       Example(s)
 bit_count ( bytes bytea ) → bigint
       Returns the number of bits set in the binary string (also known as "popcount").
       bit_count('\x1234567890'::bytea) → 15
get_bit ( bytes bytea, n bigint ) → integer
       Extracts n'th bit from binary string.
       get_bit('\x1234567890'::bytea, 30) → 1
get_byte ( bytes bytea, n integer ) → integer
       Extracts n'th byte from binary string.
       get_byte('\x1234567890'::bytea, 4) → 144
 length ( bytea ) → integer
       Returns the number of bytes in the binary string.
       length('\x1234567890'::bytea) → 5
length ( bytes bytea, encoding name ) → integer
       Returns the number of characters in the binary string, assuming that it is text in the given
       encoding.
       length('jose'::bytea, 'UTF8') → 4
```

```
Function
      Description
      Example(s)
md5 ( bytea ) → text
      Computes the MD5 hash of the binary string, with the result written in hexadecimal.
      md5('Th\000omas'::bytea) → 8ab2d3c9689aaf18b4958c334c82d8b1
set_bit ( bytes bytea, n bigint, newvalue integer ) → bytea
      Sets n'th bit in binary string to newvalue.
      set_bit('\x1234567890'::bytea, 30, 0) → \x1234563890
set_byte ( bytes bytea, n integer, newvalue integer ) → bytea
      Sets n'th byte in binary string to newvalue.
      set_byte('\x1234567890'::bytea, 4, 64) → \x1234567840
sha224 ( bytea ) → bytea
      Computes the SHA-224 hash of the binary string.
      sha224('abc'::bytea) → \x23097d223405d8228642a477bda2
      55b32aadbce4bda0b3f7e36c9da7
sha256 ( bytea ) → bytea
      Computes the SHA-256 hash of the binary string.
      sha256('abc'::bytea) → \xba7816bf8f01cfea414140de5dae2223
      b00361a396177a9cb410ff61f20015ad
sha384 ( bytea ) → bytea
      Computes the SHA-384 hash of the binary string.
      sha384('abc'::bytea) → \xcb00753f45a35e8bb5a03d699ac65007
      272c32ab0eded1631a8b605a43ff5bed8086072ba1e7cc2358bae-
      ca134c825a7
sha512 ( bytea ) → bytea
      Computes the SHA-512 hash of the binary string.
      sha512('abc'::bytea) → \xddaf35a193617abac-
      c417349ae20413112e6fa4e89a97ea20a9eeee64b55d39a
      2192992a274fc1a836ba3c23a3feebbd
      454d4423643ce80e2a9ac94fa54ca49f
substr ( bytes bytea, start integer [, count integer ] ) → bytea
      Extracts the substring of bytes starting at the start'th byte, and extending for
      count bytes if that is specified. (Same as substring(bytes from start for
      count).)
      substr('\x1234567890'::bytea, 3, 2) → \x5678
```

<span id="page-80-1"></span>Functions get\_byte and set\_byte number the first byte of a binary string as byte 0. Functions get\_bit and set\_bit number bits from the right within each byte; for example bit 0 is the least significant bit of the first byte, and bit 15 is the most significant bit of the second byte.

<span id="page-80-0"></span>For historical reasons, the function md5 returns a hex-encoded value of type text whereas the SHA-2 functions return type bytea. Use the functions [encode](#page-81-1) and [decode](#page-81-2) to convert between the two. For example write encode(sha256('abc'), 'hex') to get a hex-encoded text representation, or decode(md5('abc'), 'hex') to get a bytea value.

 Functions for converting strings between different character sets (encodings), and for representing arbitrary binary data in textual form, are shown in [Table 9.13.](#page-81-0) For these functions, an argument or result of type text is expressed in the database's default encoding, while arguments or results of type bytea are in an encoding named by another argument.

#### <span id="page-81-0"></span>**Table 9.13. Text/Binary String Conversion Functions**

## **Function Description Example(s)** convert ( bytes bytea, src\_encoding name, dest\_encoding name ) → bytea Converts a binary string representing text in encoding src\_encoding to a binary string in encoding dest\_encoding (see Section 24.3.4 for available conversions). convert('text\_in\_utf8', 'UTF8', 'LATIN1') → \x746578745f696e5f75746638 convert\_from ( bytes bytea, src\_encoding name ) → text Converts a binary string representing text in encoding src\_encoding to text in the database encoding (see Section 24.3.4 for available conversions). convert\_from('text\_in\_utf8', 'UTF8') → text\_in\_utf8 convert\_to ( string text, dest\_encoding name ) → bytea Converts a text string (in the database encoding) to a binary string encoded in encoding dest\_encoding (see Section 24.3.4 for available conversions). convert\_to('some\_text', 'UTF8') → \x736f6d655f74657874 encode ( bytes bytea, format text ) → text Encodes binary data into a textual representation; supported format values are: [base64](#page-81-3), [escape](#page-81-4), [hex](#page-81-5). encode('123\000\001', 'base64') → MTIzAAE= decode ( string text, format text ) → bytea Decodes binary data from a textual representation; supported format values are the

The encode and decode functions support the following textual formats:

decode('MTIzAAE=', 'base64') → \x3132330001

<span id="page-81-2"></span><span id="page-81-1"></span>same as for encode.

### <span id="page-81-3"></span>base64

The base64 format is that of [RFC 2045 Section 6.8](https://datatracker.ietf.org/doc/html/rfc2045#section-6.8)<sup>1</sup> . As per the RFC, encoded lines are broken at 76 characters. However instead of the MIME CRLF end-of-line marker, only a newline is used for end-of-line. The decode function ignores carriage-return, newline, space, and tab characters. Otherwise, an error is raised when decode is supplied invalid base64 data — including when trailing padding is incorrect.

#### <span id="page-81-4"></span>escape

The escape format converts zero bytes and bytes with the high bit set into octal escape sequences (\nnn), and it doubles backslashes. Other byte values are represented literally. The decode function will raise an error if a backslash is not followed by either a second backslash or three octal digits; it accepts other byte values unchanged.

#### <span id="page-81-5"></span>hex

The hex format represents each 4 bits of data as one hexadecimal digit, 0 through f, writing the higher-order digit of each byte first. The encode function outputs the a-f hex digits in lower case. Because the smallest unit of data is 8 bits, there are always an even number of characters returned by encode. The decode function accepts the a-f characters in either upper or lower case. An error is raised when decode is given invalid hex data — including when given an odd number of characters.

<sup>1</sup> <https://datatracker.ietf.org/doc/html/rfc2045#section-6.8>

See also the aggregate function string\_agg in [Section 9.21](#page-192-0) and the large object functions in Section 35.4.

# <span id="page-82-0"></span>**9.6. Bit String Functions and Operators**

This section describes functions and operators for examining and manipulating bit strings, that is values of the types bit and bit varying. (While only type bit is mentioned in these tables, values of type bit varying can be used interchangeably.) Bit strings support the usual comparison operators shown in [Table 9.1](#page-56-0), as well as the operators shown in [Table 9.14.](#page-82-1)

#### <span id="page-82-1"></span>**Table 9.14. Bit String Operators**

```
Operator
       Description
       Example(s)
bit || bit → bit
       Concatenation
       B'10001' || B'011' → 10001011
bit & bit → bit
       Bitwise AND (inputs must be of equal length)
       B'10001' & B'01101' → 00001
bit | bit → bit
       Bitwise OR (inputs must be of equal length)
       B'10001' | B'01101' → 11101
bit # bit → bit
       Bitwise exclusive OR (inputs must be of equal length)
       B'10001' # B'01101' → 11100
~ bit → bit
       Bitwise NOT
       ~ B'10001' → 01110
bit << integer → bit
       Bitwise shift left (string length is preserved)
       B'10001' << 3 → 01000
bit >> integer → bit
       Bitwise shift right (string length is preserved)
       B'10001' >> 2 → 00100
```

Some of the functions available for binary strings are also available for bit strings, as shown in [Ta](#page-82-2)[ble 9.15](#page-82-2).

### <span id="page-82-2"></span>**Table 9.15. Bit String Functions**

```
Function
       Description
       Example(s)
bit_count ( bit ) → bigint
       Returns the number of bits set in the bit string (also known as "popcount").
       bit_count(B'10111') → 4
bit_length ( bit ) → integer
```

```
Function
       Description
       Example(s)
       Returns number of bits in the bit string.
       bit_length(B'10111') → 5
 length ( bit ) → integer
       Returns number of bits in the bit string.
       length(B'10111') → 5
octet_length ( bit ) → integer
       Returns number of bytes in the bit string.
       octet_length(B'1011111011') → 2
overlay ( bits bit PLACING newsubstring bit FROM start integer [ FOR
       count integer ] ) → bit
       Replaces the substring of bits that starts at the start'th bit and extends for count
       bits with newsubstring. If count is omitted, it defaults to the length of newsub-
       string.
       overlay(B'01010101010101010' placing B'11111' from 2 for 3)
       → 0111110101010101010
position ( substring bit IN bits bit ) → integer
       Returns first starting index of the specified substring within bits, or zero if it's not
       present.
       position(B'010' in B'000001101011') → 8
substring ( bits bit [ FROM start integer ] [ FOR count integer ] ) → bit
       Extracts the substring of bits starting at the start'th bit if that is specified, and stop-
       ping after count bits if that is specified. Provide at least one of start and count.
       substring(B'110010111111' from 3 for 2) → 00
get_bit ( bits bit, n integer ) → integer
       Extracts n'th bit from bit string; the first (leftmost) bit is bit 0.
       get_bit(B'101010101010101010', 6) → 1
set_bit ( bits bit, n integer, newvalue integer ) → bit
       Sets n'th bit in bit string to newvalue; the first (leftmost) bit is bit 0.
       set_bit(B'101010101010101010', 6, 0) → 101010001010101010
```

In addition, it is possible to cast integral values to and from type bit. Casting an integer to bit(n) copies the rightmost n bits. Casting an integer to a bit string width wider than the integer itself will sign-extend on the left. Some examples:

```
44::bit(10) 0000101100
44::bit(3) 100
cast(-44 as bit(12)) 111111010100
'1110'::bit(4)::integer 14
```

Note that casting to just "bit" means casting to bit(1), and so will deliver only the least significant bit of the integer.

# <span id="page-83-0"></span>**9.7. Pattern Matching**

There are three separate approaches to pattern matching provided by PostgreSQL: the traditional SQL LIKE operator, the more recent SIMILAR TO operator (added in SQL:1999), and POSIX-style regular expressions. Aside from the basic "does this string match this pattern?" operators, functions are available to extract or replace matching substrings and to split a string at matching locations.

### **Tip**

If you have pattern matching needs that go beyond this, consider writing a user-defined function in Perl or Tcl.

## **Caution**

While most regular-expression searches can be executed very quickly, regular expressions can be contrived that take arbitrary amounts of time and memory to process. Be wary of accepting regular-expression search patterns from hostile sources. If you must do so, it is advisable to impose a statement timeout.

Searches using SIMILAR TO patterns have the same security hazards, since SIMILAR TO provides many of the same capabilities as POSIX-style regular expressions.

LIKE searches, being much simpler than the other two options, are safer to use with possibly-hostile pattern sources.

The pattern matching operators of all three kinds do not support nondeterministic collations. If required, apply a different collation to the expression to work around this limitation.