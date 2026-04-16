---
source: MySQL 8.0 Reference
title: 00_Overview
---

**Table 14.18 Encryption Functions**

| Name                         | Description                                      |
|------------------------------|--------------------------------------------------|
| AES_DECRYPT()                | Decrypt using AES                                |
| AES_ENCRYPT()                | Encrypt using AES                                |
| COMPRESS()                   | Return result as a binary string                 |
| MD5()                        | Calculate MD5 checksum                           |
| RANDOM_BYTES()               | Return a random byte vector                      |
| SHA1(), SHA()                | Calculate an SHA-1 160-bit checksum              |
| SHA2()                       | Calculate an SHA-2 checksum                      |
| STATEMENT_DIGEST()           | Compute statement digest hash value              |
| STATEMENT_DIGEST_TEXT()      | Compute normalized statement digest              |
| UNCOMPRESS()                 | Uncompress a string compressed                   |
| UNCOMPRESSED_LENGTH()        | Return the length of a string before compression |
| VALIDATE_PASSWORD_STRENGTH() | Determine strength of password                   |

Many encryption and compression functions return strings for which the result might contain arbitrary byte values. If you want to store these results, use a column with a VARBINARY or BLOB binary string data type. This avoids potential problems with trailing space removal or character set conversion that would change data values, such as may occur if you use a nonbinary string data type (CHAR, VARCHAR, TEXT).

Some encryption functions return strings of ASCII characters: [MD5\(\)](#page-53-0), [SHA\(\)](#page-53-2), [SHA1\(\)](#page-53-2), [SHA2\(\)](#page-53-3), [STATEMENT\\_DIGEST\(\)](#page-54-0), [STATEMENT\\_DIGEST\\_TEXT\(\)](#page-54-1). Their return value is a string that has a character set and collation determined by the character\_set\_connection and collation\_connection system variables. This is a nonbinary string unless the character set is binary.

If an application stores values from a function such as [MD5\(\)](#page-53-0) or [SHA1\(\)](#page-53-2) that returns a string of hex digits, more efficient storage and comparisons can be obtained by converting the hex representation to binary using UNHEX() and storing the result in a BINARY(N) column. Each pair of hexadecimal digits requires one byte in binary form, so the value of N depends on the length of the hex string. N is 16 for an [MD5\(\)](#page-53-0) value and 20 for a [SHA1\(\)](#page-53-2) value. For [SHA2\(\)](#page-53-3), N ranges from 28 to 32 depending on the argument specifying the desired bit length of the result.

The size penalty for storing the hex string in a CHAR column is at least two times, up to eight times if the value is stored in a column that uses the utf8mb4 character set (where each character uses 4 bytes). Storing the string also results in slower comparisons because of the larger values and the need to take character set collation rules into account.

Suppose that an application stores [MD5\(\)](#page-53-0) string values in a CHAR(32) column:

```
CREATE TABLE md5_tbl (md5_val CHAR(32), ...);
INSERT INTO md5_tbl (md5_val, ...) VALUES(MD5('abcdef'), ...);
```

To convert hex strings to more compact form, modify the application to use UNHEX() and BINARY(16) instead as follows:

```
CREATE TABLE md5_tbl (md5_val BINARY(16), ...);
INSERT INTO md5_tbl (md5_val, ...) VALUES(UNHEX(MD5('abcdef')), ...);
```

Applications should be prepared to handle the very rare case that a hashing function produces the same value for two different input values. One way to make collisions detectable is to make the hash column a primary key.

![](_page_48_Picture_4.jpeg)

### **Note**

Exploits for the MD5 and SHA-1 algorithms have become known. You may wish to consider using another one-way encryption function described in this section instead, such as [SHA2\(\)](#page-53-3).

![](_page_48_Picture_7.jpeg)

### **Caution**

Passwords or other sensitive values supplied as arguments to encryption functions are sent as cleartext to the MySQL server unless an SSL connection is used. Also, such values appear in any MySQL logs to which they are written. To avoid these types of exposure, applications can encrypt sensitive values on the client side before sending them to the server. The same considerations apply to encryption keys. To avoid exposing these, applications can use stored procedures to encrypt and decrypt values on the server side.

<span id="page-48-0"></span>• [AES\\_DECRYPT\(](#page-48-0)crypt\_str,key\_str[,init\_vector][,kdf\_name][,salt][,info | [iterations](#page-48-0)])

This function decrypts data using the official AES (Advanced Encryption Standard) algorithm. For more information, see the description of [AES\\_ENCRYPT\(\)](#page-48-1).

Statements that use [AES\\_DECRYPT\(\)](#page-48-0) are unsafe for statement-based replication.

<span id="page-48-1"></span>• [AES\\_ENCRYPT\(](#page-48-1)str,key\_str[,init\_vector][,kdf\_name][,salt][,info | [iterations](#page-48-1)])

[AES\\_ENCRYPT\(\)](#page-48-1) and [AES\\_DECRYPT\(\)](#page-48-0) implement encryption and decryption of data using the official AES (Advanced Encryption Standard) algorithm, previously known as "Rijndael." The AES standard permits various key lengths. By default these functions implement AES with a 128-bit key length. Key lengths of 196 or 256 bits can be used, as described later. The key length is a trade off between performance and security.

[AES\\_ENCRYPT\(\)](#page-48-1) encrypts the string str using the key string key\_str, and returns a binary string containing the encrypted output. [AES\\_DECRYPT\(\)](#page-48-0) decrypts the encrypted string crypt\_str using the key string key\_str, and returns the original (binary) string in hexadecimal format. (To obtain the string as plaintext, cast the result to CHAR. Alternatively, start the mysql client with --skipbinary-as-hex to cause all binary values to be displayed as text.) If either function argument is NULL, the function returns NULL. If [AES\\_DECRYPT\(\)](#page-48-0) detects invalid data or incorrect padding, it returns NULL. However, it is possible for [AES\\_DECRYPT\(\)](#page-48-0) to return a non-NULL value (possibly garbage) if the input data or the key is invalid.

As of MySQL 8.0.30, these functions support the use of a key derivation function (KDF) to create a cryptographically strong secret key from the information passed in key\_str. The derived key is used to encrypt and decrypt the data, and it remains in the MySQL Server instance and is not accessible to users. Using a KDF is highly recommended, as it provides better security than specifying your own premade key or deriving it by a simpler method as you use the function. The functions support HKDF (available from OpenSSL 1.1.0), for which you can specify an optional salt and context-specific information to include in the keying material, and PBKDF2 (available from OpenSSL 1.0.2), for which you can specify an optional salt and set the number of iterations used to produce the key.

If you do not use a KDF, the key size should be less than 16 bytes. [AES\\_ENCRYPT\(\)](#page-48-1) does the following by default when a KDF is not used:

- Sets the full 16-byte key to 0s.
- XORs the supplied key into the internal key for as long as there is data.
- If the supplied key is longer than the required key, it wraps around at the start of the result key and keeps XORing until there is data in the supplied key.

[AES\\_ENCRYPT\(\)](#page-48-1) and [AES\\_DECRYPT\(\)](#page-48-0) permit control of the block encryption mode. The block\_encryption\_mode system variable controls the mode for block-based encryption algorithms. Its default value is aes-128-ecb, which signifies encryption using a key length of 128 bits and ECB mode. For a description of the permitted values of this variable, see Section 7.1.8, "Server System Variables". The optional init\_vector argument is used to provide an initialization vector for block encryption modes that require it.

Statements that use [AES\\_ENCRYPT\(\)](#page-48-1) or [AES\\_DECRYPT\(\)](#page-48-0) are unsafe for statement-based replication.

If [AES\\_ENCRYPT\(\)](#page-48-1) is invoked from within the mysql client, binary strings display using hexadecimal notation, depending on the value of the --binary-as-hex. For more information about that option, see Section 6.5.1, "mysql — The MySQL Command-Line Client".

The arguments for the [AES\\_ENCRYPT\(\)](#page-48-1) and [AES\\_DECRYPT\(\)](#page-48-0) functions are as follows:

str The string for [AES\\_ENCRYPT\(\)](#page-48-1) to encrypt using the key string key\_str, or (from MySQL 8.0.30) the key derived from it by the specified KDF. The string can be any length. Padding is automatically added to str so it is a multiple of a block as required by block-based algorithms such as AES. This padding is automatically removed by the [AES\\_DECRYPT\(\)](#page-48-0) function.

crypt\_str The encrypted string for [AES\\_DECRYPT\(\)](#page-48-0) to decrypt using the key string key\_str, or (from MySQL 8.0.30) the key derived from it by the specified KDF. The string can be any length. The length of crypt\_str can be calculated from the length of the original string using this formula:

16 \* (trunc(string\_length / 16) + 1)

key\_str The encryption key, or the input keying material that is used as the basis for deriving a key using a key derivation function (KDF). For the same instance of data, use the same value of key\_str for encryption with [AES\\_ENCRYPT\(\)](#page-48-1) and decryption with [AES\\_DECRYPT\(\)](#page-48-0).

> If you are using a KDF, which you can from MySQL 8.0.30, key\_str can be any arbitrary information such as a password or passphrase. In the further arguments for the function, you specify the KDF name, then add further options to increase the security as appropriate for the KDF.

When you use a KDF, the function creates a cryptographically strong secret key from the information passed in key\_str and any salt or additional information that you provide in the other arguments. The derived key is used to encrypt and decrypt the data, and it remains in the MySQL Server instance and is not accessible to users. Using a KDF is highly recommended, as it

provides better security than specifying your own premade key or deriving it by a simpler method as you use the function.

If you are not using a KDF, for a key length of 128 bits, the most secure way to pass a key to the key\_str argument is to create a truly random 128-bit value and pass it as a binary value. For example:

```
INSERT INTO t
VALUES (1,AES_ENCRYPT('text',UNHEX('F3229A0B371ED2D9441B830D21A390C3')));
```

A passphrase can be used to generate an AES key by hashing the passphrase. For example:

```
INSERT INTO t
VALUES (1,AES_ENCRYPT('text', UNHEX(SHA2('My secret passphrase',512))));
```

If you exceed the maximum key length of 128 bits, a warning is returned. If you are not using a KDF, do not pass a password or passphrase directly to key\_str, hash it first. Previous versions of this documentation suggested the former approach, but it is no longer recommended as the examples shown here are more secure.

init\_vector An initialization vector, for block encryption modes that require it. The block\_encryption\_mode system variable controls the mode. For the same instance of data, use the same value of init\_vector for encryption with [AES\\_ENCRYPT\(\)](#page-48-1) and decryption with [AES\\_DECRYPT\(\)](#page-48-0).

![](_page_50_Picture_8.jpeg)

### **Note**

If you are using a KDF, you must specify an initialization vector or a null string for this argument, in order to access the later arguments to define the KDF.

For modes that require an initialization vector, it must be 16 bytes or longer (bytes in excess of 16 are ignored). An error occurs if init\_vector is missing. For modes that do not require an initialization vector, it is ignored and a warning is generated if init\_vector is specified, unless you are using a KDF.

The default value for the block\_encryption\_mode system variable is aes-128-ecb, or ECB mode, which does not require an initialization vector. The alternative permitted block encryption modes CBC, CFB1, CFB8, CFB128, and OFB all require an initialization vector.

A random string of bytes to use for the initialization vector can be produced by calling [RANDOM\\_BYTES\(16\)](#page-53-1).

kdf\_name The name of the key derivation function (KDF) to create a key from the input keying material passed in key\_str, and other arguments as appropriate for the KDF. This optional argument is available from MySQL 8.0.30.

> For the same instance of data, use the same value of kdf\_name for encryption with [AES\\_ENCRYPT\(\)](#page-48-1) and decryption with [AES\\_DECRYPT\(\)](#page-48-0). When you specify kdf\_name, you must specify init\_vector, using either a valid initialization vector,

or a null string if the encryption mode does not require an initialization vector.

The following values are supported:

hkdf HKDF, which is available from OpenSSL 1.1.0. HKDF extracts a pseudorandom key from the keying material then expands it into additional keys. With HKDF, you can specify an optional salt (salt) and context-specific information such as application details (info) to include in the keying material.

pbkdf2\_hmac PBKDF2, which is available from OpenSSL 1.0.2. PBKDF2 applies a pseudorandom function to the keying material, and repeats this process a large number of times to produce the key. With PBKDF2, you can specify an optional salt (salt) to include in the keying material, and set the number of iterations used to produce the key (iterations).

In this example, HKDF is specified as the key derivation function, and a salt and context information are provided. The argument for the initialization vector is included but is the empty string:

```
SELECT AES_ENCRYPT('mytext','mykeystring', '', 'hkdf', 'salt', 'info');
```

In this example, PBKDF2 is specified as the key derivation function, a salt is provided, and the number of iterations is doubled from the recommended minimum:

```
SELECT AES_ENCRYPT('mytext','mykeystring', '', 'pbkdf2_hmac','salt', '2000');
```

salt A salt to be passed to the key derivation function (KDF). This optional argument is available from MySQL 8.0.30. Both HKDF and PBKDF2 can use salts, and their use is recommended to help prevent attacks based on dictionaries of common passwords or rainbow tables.

> A salt consists of random data, which for security must be different for each encryption operation. A random string of bytes to use for the salt can be produced by calling [RANDOM\\_BYTES\(\)](#page-53-1). This example produces a 64-bit salt:

```
SET @salt = RANDOM_BYTES(8);
```

For the same instance of data, use the same value of salt for encryption with [AES\\_ENCRYPT\(\)](#page-48-1) and decryption with [AES\\_DECRYPT\(\)](#page-48-0). The salt can safely be stored along with the encrypted data.

info Context-specific information for HKDF to include in the keying material, such as information about the application. This optional argument is available from MySQL 8.0.30 when you specify hkdf as the KDF name. HKDF adds this information to the keying material specified in key\_str and the salt specified in salt to produce the key.

> For the same instance of data, use the same value of info for encryption with [AES\\_ENCRYPT\(\)](#page-48-1) and decryption with [AES\\_DECRYPT\(\)](#page-48-0).

iterations The iteration count for PBKDF2 to use when producing the key. This optional argument is available from MySQL 8.0.30 when you specify pbkdf2\_hmac as the KDF name. A higher count gives greater resistance to brute-force attacks because it has a greater computational cost for the attacker, but the same is necessarily true for the key derivation process. The default if you do not specify this argument is 1000, which is the minimum recommended by the OpenSSL standard.

> For the same instance of data, use the same value of iterations for encryption with [AES\\_ENCRYPT\(\)](#page-48-1) and decryption with [AES\\_DECRYPT\(\)](#page-48-0).

```
mysql> SET block_encryption_mode = 'aes-256-cbc';
mysql> SET @key_str = SHA2('My secret passphrase',512);
mysql> SET @init_vector = RANDOM_BYTES(16);
mysql> SET @crypt_str = AES_ENCRYPT('text',@key_str,@init_vector);
mysql> SELECT CAST(AES_DECRYPT(@crypt_str,@key_str,@init_vector) AS CHAR);
+-------------------------------------------------------------+
| CAST(AES_DECRYPT(@crypt_str,@key_str,@init_vector) AS CHAR) |
+-------------------------------------------------------------+
| text |
+-------------------------------------------------------------+
```

<span id="page-52-0"></span>• COMPRESS([string\\_to\\_compress](#page-52-0))

Compresses a string and returns the result as a binary string. This function requires MySQL to have been compiled with a compression library such as zlib. Otherwise, the return value is always NULL. The return value is also NULL if string\_to\_compress is NULL. The compressed string can be uncompressed with [UNCOMPRESS\(\)](#page-54-2).

```
mysql> SELECT LENGTH(COMPRESS(REPEAT('a',1000)));
 -> 21
mysql> SELECT LENGTH(COMPRESS(''));
 -> 0
mysql> SELECT LENGTH(COMPRESS('a'));
 -> 13
mysql> SELECT LENGTH(COMPRESS(REPEAT('a',16)));
 -> 15
```

The compressed string contents are stored the following way:

- Empty strings are stored as empty strings.
- Nonempty strings are stored as a 4-byte length of the uncompressed string (low byte first), followed by the compressed string. If the string ends with space, an extra . character is added to avoid problems with endspace trimming should the result be stored in a CHAR or VARCHAR column. (However, use of nonbinary string data types such as CHAR or VARCHAR to store

compressed strings is not recommended anyway because character set conversion may occur. Use a VARBINARY or BLOB binary string column instead.)

If [COMPRESS\(\)](#page-52-0) is invoked from within the mysql client, binary strings display using hexadecimal notation, depending on the value of the --binary-as-hex. For more information about that option, see Section 6.5.1, "mysql — The MySQL Command-Line Client".

<span id="page-53-0"></span>• [MD5\(](#page-53-0)str)

Calculates an MD5 128-bit checksum for the string. The value is returned as a string of 32 hexadecimal digits, or NULL if the argument was NULL. The return value can, for example, be used as a hash key. See the notes at the beginning of this section about storing hash values efficiently.

The return value is a string in the connection character set.

If FIPS mode is enabled, MD5() returns NULL. See Section 8.8, "FIPS Support".

```
mysql> SELECT MD5('testing');
 -> 'ae2b1fca515949e5d54fb22b8ed95575'
```

This is the "RSA Data Security, Inc. MD5 Message-Digest Algorithm."

See the note regarding the MD5 algorithm at the beginning this section.

<span id="page-53-1"></span>• [RANDOM\\_BYTES\(](#page-53-1)len)

This function returns a binary string of len random bytes generated using the random number generator of the SSL library. Permitted values of len range from 1 to 1024. For values outside that range, an error occurs. Returns NULL if len is NULL.

[RANDOM\\_BYTES\(\)](#page-53-1) can be used to provide the initialization vector for the [AES\\_DECRYPT\(\)](#page-48-0) and [AES\\_ENCRYPT\(\)](#page-48-1) functions. For use in that context, len must be at least 16. Larger values are permitted, but bytes in excess of 16 are ignored.

[RANDOM\\_BYTES\(\)](#page-53-1) generates a random value, which makes its result nondeterministic. Consequently, statements that use this function are unsafe for statement-based replication.

If [RANDOM\\_BYTES\(\)](#page-53-1) is invoked from within the mysql client, binary strings display using hexadecimal notation, depending on the value of the --binary-as-hex. For more information about that option, see Section 6.5.1, "mysql — The MySQL Command-Line Client".

<span id="page-53-2"></span>• [SHA1\(](#page-53-2)str), [SHA\(](#page-53-2)str)

Calculates an SHA-1 160-bit checksum for the string, as described in RFC 3174 (Secure Hash Algorithm). The value is returned as a string of 40 hexadecimal digits, or NULL if the argument is NULL. One of the possible uses for this function is as a hash key. See the notes at the beginning of this section about storing hash values efficiently. [SHA\(\)](#page-53-2) is synonymous with [SHA1\(\)](#page-53-2).

The return value is a string in the connection character set.

```
mysql> SELECT SHA1('abc');
 -> 'a9993e364706816aba3e25717850c26c9cd0d89d'
```

[SHA1\(\)](#page-53-2) can be considered a cryptographically more secure equivalent of [MD5\(\)](#page-53-0). However, see the note regarding the MD5 and SHA-1 algorithms at the beginning this section.

<span id="page-53-3"></span>• SHA2(str, [hash\\_length](#page-53-3))

Calculates the SHA-2 family of hash functions (SHA-224, SHA-256, SHA-384, and SHA-512). The first argument is the plaintext string to be hashed. The second argument indicates the desired bit length of the result, which must have a value of 224, 256, 384, 512, or 0 (which is equivalent to 256). If either argument is NULL or the hash length is not one of the permitted values, the return value is

NULL. Otherwise, the function result is a hash value containing the desired number of bits. See the notes at the beginning of this section about storing hash values efficiently.

The return value is a string in the connection character set.

```
mysql> SELECT SHA2('abc', 224);
 -> '23097d223405d8228642a477bda255b32aadbce4bda0b3f7e36c9da7'
```

This function works only if MySQL has been configured with SSL support. See Section 8.3, "Using Encrypted Connections".

[SHA2\(\)](#page-53-3) can be considered cryptographically more secure than [MD5\(\)](#page-53-0) or [SHA1\(\)](#page-53-2).

<span id="page-54-0"></span>• [STATEMENT\\_DIGEST\(](#page-54-0)statement)

Given an SQL statement as a string, returns the statement digest hash value as a string in the connection character set, or NULL if the argument is NULL. The related [STATEMENT\\_DIGEST\\_TEXT\(\)](#page-54-1) function returns the normalized statement digest. For information about statement digesting, see Section 29.10, "Performance Schema Statement Digests and Sampling".

Both functions use the MySQL parser to parse the statement. If parsing fails, an error occurs. The error message includes the parse error only if the statement is provided as a literal string.

The max\_digest\_length system variable determines the maximum number of bytes available to these functions for computing normalized statement digests.

```
mysql> SET @stmt = 'SELECT * FROM mytable WHERE cola = 10 AND colb = 20';
mysql> SELECT STATEMENT_DIGEST(@stmt);
+------------------------------------------------------------------+
| STATEMENT_DIGEST(@stmt) |
+------------------------------------------------------------------+
| 3bb95eeade896657c4526e74ff2a2862039d0a0fe8a9e7155b5fe492cbd78387 |
+------------------------------------------------------------------+
mysql> SELECT STATEMENT_DIGEST_TEXT(@stmt);
+----------------------------------------------------------+
| STATEMENT_DIGEST_TEXT(@stmt) |
+----------------------------------------------------------+
| SELECT * FROM `mytable` WHERE `cola` = ? AND `colb` = ? |
+----------------------------------------------------------+
```

<span id="page-54-1"></span>• [STATEMENT\\_DIGEST\\_TEXT\(](#page-54-1)statement)

Given an SQL statement as a string, returns the normalized statement digest as a string in the connection character set, or NULL if the argument is NULL. For additional discussion and examples, see the description of the related [STATEMENT\\_DIGEST\(\)](#page-54-0) function.

<span id="page-54-2"></span>• UNCOMPRESS([string\\_to\\_uncompress](#page-54-2))

Uncompresses a string compressed by the [COMPRESS\(\)](#page-52-0) function. If the argument is not a compressed value, the result is NULL; if string\_to\_uncompress is NULL, the result is also NULL. This function requires MySQL to have been compiled with a compression library such as zlib. Otherwise, the return value is always NULL.

```
mysql> SELECT UNCOMPRESS(COMPRESS('any string'));
 -> 'any string'
mysql> SELECT UNCOMPRESS('any string');
 -> NULL
```

<span id="page-54-3"></span>• [UNCOMPRESSED\\_LENGTH\(](#page-54-3)compressed\_string)

Returns the length that the compressed string had before being compressed. Returns NULL if compressed\_string is NULL.

```
mysql> SELECT UNCOMPRESSED_LENGTH(COMPRESS(REPEAT('a',30)));
```

-> 30

<span id="page-55-0"></span>• [VALIDATE\\_PASSWORD\\_STRENGTH\(](#page-55-0)str)

Given an argument representing a plaintext password, this function returns an integer to indicate how strong the password is, or NULL if the argument is NULL. The return value ranges from 0 (weak) to 100 (strong).

Password assessment by [VALIDATE\\_PASSWORD\\_STRENGTH\(\)](#page-55-0) is done by the validate\_password component. If that component is not installed, the function always returns 0. For information about installing validate\_password, see Section 8.4.3, "The Password Validation Component". To examine or configure the parameters that affect password testing, check or set the system variables implemented by validate\_password. See Section 8.4.3.2, "Password Validation Options and Variables".

The password is subjected to increasingly strict tests and the return value reflects which tests were satisfied, as shown in the following table. In addition, if the validate\_password.check\_user\_name system variable is enabled and the password matches the user name, [VALIDATE\\_PASSWORD\\_STRENGTH\(\)](#page-55-0) returns 0 regardless of how other validate\_password system variables are set.

| Password Test               | Return Value |
|-----------------------------|--------------|
| Length < 4                  | 0            |
| Length ≥ 4 and <            | 25           |
| validate_password.length    |              |
| Satisfies policy 1 (LOW)    | 50           |
| Satisfies policy 2 (MEDIUM) | 75           |
| Satisfies policy 3 (STRONG) | 100          |