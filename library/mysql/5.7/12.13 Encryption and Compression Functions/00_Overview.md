---
source: MySQL 5.7 Reference
title: 00_Overview
---

**Table 12.18 Encryption Functions**

| Name                  | Description                                                 | Deprecated |
|-----------------------|-------------------------------------------------------------|------------|
| AES_DECRYPT()         | Decrypt using AES                                           |            |
| AES_ENCRYPT()         | Encrypt using AES                                           |            |
| COMPRESS()            | Return result as a binary string                            |            |
| DECODE()              | Decode a string encrypted using<br>ENCODE()                 | Yes        |
| DES_DECRYPT()         | Decrypt a string                                            | Yes        |
| DES_ENCRYPT()         | Encrypt a string                                            | Yes        |
| ENCODE()              | Encode a string                                             | Yes        |
| ENCRYPT()             | Encrypt a string                                            | Yes        |
| MD5()                 | Calculate MD5 checksum                                      |            |
| PASSWORD()            | Calculate and return a password<br>string                   | Yes        |
| RANDOM_BYTES()        | Return a random byte vector                                 |            |
| SHA1(), SHA()         | Calculate an SHA-1 160-bit<br>checksum                      |            |
| SHA2()                | Calculate an SHA-2 checksum                                 |            |
| UNCOMPRESS()          | Uncompress a string<br>compressed                           |            |
| UNCOMPRESSED_LENGTH() | Return the length of a string<br>before compression         |            |
|                       | VALIDATE_PASSWORD_STRENGTH() Determine strength of password |            |

Many encryption and compression functions return strings for which the result might contain arbitrary byte values. If you want to store these results, use a column with a VARBINARY or BLOB binary string data type. This avoids potential problems with trailing space removal or character set conversion that would change data values, such as may occur if you use a nonbinary string data type (CHAR, VARCHAR, TEXT).

Some encryption functions return strings of ASCII characters: [MD5\(\)](#page-116-2), [PASSWORD\(\)](#page-117-0), [SHA\(\)](#page-118-1), [SHA1\(\)](#page-118-1), [SHA2\(\)](#page-118-2). Their return value is a string that has a character set and collation determined by the character\_set\_connection and collation\_connection system variables. This is a nonbinary string unless the character set is binary.

If an application stores values from a function such as [MD5\(\)](#page-116-2) or [SHA1\(\)](#page-118-1) that returns a string of hex digits, more efficient storage and comparisons can be obtained by converting the hex representation to binary using [UNHEX\(\)](#page-48-1) and storing the result in a BINARY(N) column. Each pair of hexadecimal digits

requires one byte in binary form, so the value of N depends on the length of the hex string. N is 16 for an [MD5\(\)](#page-116-2) value and 20 for a [SHA1\(\)](#page-118-1) value. For [SHA2\(\)](#page-118-2), N ranges from 28 to 32 depending on the argument specifying the desired bit length of the result.

The size penalty for storing the hex string in a CHAR column is at least two times, up to eight times if the value is stored in a column that uses the utf8 character set (where each character uses 4 bytes). Storing the string also results in slower comparisons because of the larger values and the need to take character set collation rules into account.

Suppose that an application stores [MD5\(\)](#page-116-2) string values in a CHAR(32) column:

```
CREATE TABLE md5_tbl (md5_val CHAR(32), ...);
INSERT INTO md5_tbl (md5_val, ...) VALUES(MD5('abcdef'), ...);
```

To convert hex strings to more compact form, modify the application to use [UNHEX\(\)](#page-48-1) and BINARY(16) instead as follows:

```
CREATE TABLE md5_tbl (md5_val BINARY(16), ...);
INSERT INTO md5_tbl (md5_val, ...) VALUES(UNHEX(MD5('abcdef')), ...);
```

Applications should be prepared to handle the very rare case that a hashing function produces the same value for two different input values. One way to make collisions detectable is to make the hash column a primary key.

![](_page_109_Picture_8.jpeg)

#### **Note**

Exploits for the MD5 and SHA-1 algorithms have become known. You may wish to consider using another one-way encryption function described in this section instead, such as [SHA2\(\)](#page-118-2).

![](_page_109_Picture_11.jpeg)

### **Caution**

Passwords or other sensitive values supplied as arguments to encryption functions are sent as cleartext to the MySQL server unless an SSL connection is used. Also, such values appear in any MySQL logs to which they are written. To avoid these types of exposure, applications can encrypt sensitive values on the client side before sending them to the server. The same considerations apply to encryption keys. To avoid exposing these, applications can use stored procedures to encrypt and decrypt values on the server side.

<span id="page-109-0"></span>• [AES\\_DECRYPT\(](#page-109-0)crypt\_str,key\_str[,init\_vector][,kdf\_name][,salt][,info | [iterations](#page-109-0)])

This function decrypts data using the official AES (Advanced Encryption Standard) algorithm. For more information, see the description of [AES\\_ENCRYPT\(\)](#page-109-1).

Statements that use [AES\\_DECRYPT\(\)](#page-109-0) are unsafe for statement-based replication.

<span id="page-109-1"></span>• [AES\\_ENCRYPT\(](#page-109-1)str,key\_str[,init\_vector][,kdf\_name][,salt][,info | [iterations](#page-109-1)])

[AES\\_ENCRYPT\(\)](#page-109-1) and [AES\\_DECRYPT\(\)](#page-109-0) implement encryption and decryption of data using the official AES (Advanced Encryption Standard) algorithm, previously known as "Rijndael." The AES standard permits various key lengths. By default these functions implement AES with a 128-bit key length. Key lengths of 196 or 256 bits can be used, as described later. The key length is a trade off between performance and security.

[AES\\_ENCRYPT\(\)](#page-109-1) encrypts the string str using the key string key\_str, and returns a binary string containing the encrypted output. [AES\\_DECRYPT\(\)](#page-109-0) decrypts the encrypted string crypt\_str using the key string key\_str, and returns the original plaintext string. If either function argument is NULL, the function returns NULL. If [AES\\_DECRYPT\(\)](#page-109-0) detects invalid data or incorrect padding, it returns NULL. However, it is possible for [AES\\_DECRYPT\(\)](#page-109-0) to return a non-NULL value (possibly garbage) if the input data or the key is invalid.

As of MySQL 5.7.40, these functions support the use of a key derivation function (KDF) to create a cryptographically strong secret key from the information passed in key\_str. The derived key is used to encrypt and decrypt the data, and it remains in the MySQL Server instance and is not accessible to users. Using a KDF is highly recommended, as it provides better security than specifying your own premade key or deriving it by a simpler method as you use the function. The functions support HKDF (available from OpenSSL 1.1.0), for which you can specify an optional salt and context-specific information to include in the keying material, and PBKDF2 (available from OpenSSL 1.0.2), for which you can specify an optional salt and set the number of iterations used to produce the key.

[AES\\_ENCRYPT\(\)](#page-109-1) and [AES\\_DECRYPT\(\)](#page-109-0) permit control of the block encryption mode. The block\_encryption\_mode system variable controls the mode for block-based encryption algorithms. Its default value is aes-128-ecb, which signifies encryption using a key length of 128 bits and ECB mode. For a description of the permitted values of this variable, see Section 5.1.7, "Server System Variables". The optional init\_vector argument is used to provide an initialization vector for block encryption modes that require it.

Statements that use [AES\\_ENCRYPT\(\)](#page-109-1) or [AES\\_DECRYPT\(\)](#page-109-0) are unsafe for statement-based replication.

If [AES\\_ENCRYPT\(\)](#page-109-1) is invoked from within the mysql client, binary strings display using hexadecimal notation, depending on the value of the --binary-as-hex. For more information about that option, see Section 4.5.1, "mysql — The MySQL Command-Line Client".

The arguments for the [AES\\_ENCRYPT\(\)](#page-109-1) and [AES\\_DECRYPT\(\)](#page-109-0) functions are as follows:

str The string for [AES\\_ENCRYPT\(\)](#page-109-1) to encrypt using the key string key\_str, or (as of MySQL 5.7.40) the key derived from it by the specified KDF. The string can be any length. Padding is automatically added to str so it is a multiple of a block as required by block-based algorithms such as AES. This padding is automatically removed by the [AES\\_DECRYPT\(\)](#page-109-0) function.

crypt\_str The encrypted string for [AES\\_DECRYPT\(\)](#page-109-0) to decrypt using the key string key\_str, or (from MySQL 5.7.40) the key derived from it by the specified KDF. The string can be any length. The length of crypt\_str can be calculated from the length of the original string using this formula:

16 \* (trunc(string\_length / 16) + 1)

key\_str The encryption key, or the input keying material that is used as the basis for deriving a key using a key derivation function (KDF). For the same instance of data, use the same value of key\_str for encryption with [AES\\_ENCRYPT\(\)](#page-109-1) and decryption with [AES\\_DECRYPT\(\)](#page-109-0).

> If you are using a KDF, which you can from MySQL 5.7.40, key\_str can be any arbitrary information such as a password or passphrase. In the further arguments for the function, you specify the KDF name, then add further options to increase the security as appropriate for the KDF.

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

init\_vector An initialization vector, for block encryption modes that require it. The block\_encryption\_mode system variable controls the mode. For the same instance of data, use the same value of init\_vector for encryption with [AES\\_ENCRYPT\(\)](#page-109-1) and decryption with [AES\\_DECRYPT\(\)](#page-109-0).

![](_page_111_Picture_8.jpeg)

#### **Note**

If you are using a KDF, you must specify an initialization vector or a null string for this argument, in order to access the later arguments to define the KDF.

For modes that require an initialization vector, it must be 16 bytes or longer (bytes in excess of 16 are ignored). An error occurs if init\_vector is missing. For modes that do not require an initialization vector, it is ignored and a warning is generated if init\_vector is specified, unless you are using a KDF.

The default value for the block\_encryption\_mode system variable is aes-128-ecb, or ECB mode, which does not require an initialization vector. The alternative permitted block encryption modes CBC, CFB1, CFB8, CFB128, and OFB all require an initialization vector.

A random string of bytes to use for the initialization vector can be produced by calling [RANDOM\\_BYTES\(16\)](#page-118-0).

kdf\_name The name of the key derivation function (KDF) to create a key from the input keying material passed in key\_str, and other arguments as appropriate for the KDF. This optional argument is available from MySQL 5.7.40.

> For the same instance of data, use the same value of kdf\_name for encryption with [AES\\_ENCRYPT\(\)](#page-109-1) and decryption with [AES\\_DECRYPT\(\)](#page-109-0). When you specify kdf\_name, you must specify init\_vector, using either a valid initialization vector,

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

salt A salt to be passed to the key derivation function (KDF). This optional argument is available from MySQL 5.7.40. Both HKDF and PBKDF2 can use salts, and their use is recommended to help prevent attacks based on dictionaries of common passwords or rainbow tables.

> A salt consists of random data, which for security must be different for each encryption operation. A random string of bytes to use for the salt can be produced by calling [RANDOM\\_BYTES\(\)](#page-118-0). This example produces a 64-bit salt:

```
SET @salt = RANDOM_BYTES(8);
```

For the same instance of data, use the same value of salt for encryption with [AES\\_ENCRYPT\(\)](#page-109-1) and decryption with [AES\\_DECRYPT\(\)](#page-109-0). The salt can safely be stored along with the encrypted data.

info Context-specific information for HKDF to include in the keying material, such as information about the application. This optional argument is available from MySQL 5.7.40 when you specify hkdf as the KDF name. HKDF adds this information to the keying material specified in key\_str and the salt specified in salt to produce the key.

> For the same instance of data, use the same value of info for encryption with [AES\\_ENCRYPT\(\)](#page-109-1) and decryption with [AES\\_DECRYPT\(\)](#page-109-0).

iterations The iteration count for PBKDF2 to use when producing the key. This optional argument is available from MySQL 5.7.40 when you specify pbkdf2\_hmac as the KDF name. A higher count gives greater resistance to brute-force attacks because it has a greater computational cost for the attacker, but the same is necessarily true for the key derivation process. The default if you do not specify this argument is 1000, which is the minimum recommended by the OpenSSL standard.

> For the same instance of data, use the same value of iterations for encryption with [AES\\_ENCRYPT\(\)](#page-109-1) and decryption with [AES\\_DECRYPT\(\)](#page-109-0).

```
mysql> SET block_encryption_mode = 'aes-256-cbc';
mysql> SET @key_str = SHA2('My secret passphrase',512);
mysql> SET @init_vector = RANDOM_BYTES(16);
mysql> SET @crypt_str = AES_ENCRYPT('text',@key_str,@init_vector);
mysql> SELECT AES_DECRYPT(@crypt_str,@key_str,@init_vector);
+-----------------------------------------------+
| AES_DECRYPT(@crypt_str,@key_str,@init_vector) |
+-----------------------------------------------+
| text |
+-----------------------------------------------+
```

<span id="page-113-0"></span>• COMPRESS([string\\_to\\_compress](#page-113-0))

Compresses a string and returns the result as a binary string. This function requires MySQL to have been compiled with a compression library such as zlib. Otherwise, the return value is always NULL. The compressed string can be uncompressed with [UNCOMPRESS\(\)](#page-118-3).

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

If [COMPRESS\(\)](#page-113-0) is invoked from within the mysql client, binary strings display using hexadecimal notation, depending on the value of the --binary-as-hex. For more information about that option, see Section 4.5.1, "mysql — The MySQL Command-Line Client".

<span id="page-114-0"></span>• DECODE([crypt\\_str](#page-114-0),pass\_str)

[DECODE\(\)](#page-114-0) decrypts the encrypted string crypt\_str using pass\_str as the password. crypt\_str should be a string returned from [ENCODE\(\)](#page-116-0).

![](_page_114_Picture_5.jpeg)

#### **Note**

The [ENCODE\(\)](#page-116-0) and [DECODE\(\)](#page-114-0) functions are deprecated in MySQL 5.7, and should no longer be used. Expect them to be removed in a future MySQL release. Consider using [AES\\_ENCRYPT\(\)](#page-109-1) and [AES\\_DECRYPT\(\)](#page-109-0) instead.

<span id="page-114-1"></span>• [DES\\_DECRYPT\(](#page-114-1)crypt\_str[,key\_str])

Decrypts a string encrypted with [DES\\_ENCRYPT\(\)](#page-114-2). If an error occurs, this function returns NULL.

This function works only if MySQL has been configured with SSL support. See Section 6.3, "Using Encrypted Connections".

If no key\_str argument is given, [DES\\_DECRYPT\(\)](#page-114-1) examines the first byte of the encrypted string to determine the DES key number that was used to encrypt the original string, and then reads the key from the DES key file to decrypt the message. For this to work, the user must have the SUPER privilege. The key file can be specified with the --des-key-file server option.

If you pass this function a key\_str argument, that string is used as the key for decrypting the message.

If the crypt\_str argument does not appear to be an encrypted string, MySQL returns the given crypt\_str.

![](_page_114_Picture_14.jpeg)

## **Note**

The [DES\\_ENCRYPT\(\)](#page-114-2) and [DES\\_DECRYPT\(\)](#page-114-1) functions are deprecated in MySQL 5.7, are removed in MySQL 8.0, and should no longer be used. Consider using [AES\\_ENCRYPT\(\)](#page-109-1) and [AES\\_DECRYPT\(\)](#page-109-0) instead.

<span id="page-114-2"></span>• [DES\\_ENCRYPT\(](#page-114-2)str[,{key\_num|key\_str}])

Encrypts the string with the given key using the Triple-DES algorithm.

This function works only if MySQL has been configured with SSL support. See Section 6.3, "Using Encrypted Connections".

The encryption key to use is chosen based on the second argument to [DES\\_ENCRYPT\(\)](#page-114-2), if one was given. With no argument, the first key from the DES key file is used. With a key\_num argument, the

given key number (0 to 9) from the DES key file is used. With a key\_str argument, the given key string is used to encrypt str.

The key file can be specified with the --des-key-file server option.

The return string is a binary string where the first character is [CHAR\(128 |](#page-38-3) key\_num). If an error occurs, [DES\\_ENCRYPT\(\)](#page-114-2) returns NULL.

The 128 is added to make it easier to recognize an encrypted key. If you use a string key, key\_num is 127.

The string length for the result is given by this formula:

```
new_len = orig_len + (8 - (orig_len % 8)) + 1
```

Each line in the DES key file has the following format:

```
key_num des_key_str
```

Each key\_num value must be a number in the range from 0 to 9. Lines in the file may be in any order. des\_key\_str is the string that is used to encrypt the message. There should be at least one space between the number and the key. The first key is the default key that is used if you do not specify any key argument to [DES\\_ENCRYPT\(\)](#page-114-2).

You can tell MySQL to read new key values from the key file with the FLUSH DES\_KEY\_FILE statement. This requires the RELOAD privilege.

One benefit of having a set of default keys is that it gives applications a way to check for the existence of encrypted column values, without giving the end user the right to decrypt those values.

![](_page_115_Picture_12.jpeg)

#### **Note**

The [DES\\_ENCRYPT\(\)](#page-114-2) and [DES\\_DECRYPT\(\)](#page-114-1) functions are deprecated in MySQL 5.7, are removed in MySQL 8.0, and should no longer be used. Consider using [AES\\_ENCRYPT\(\)](#page-109-1) and [AES\\_DECRYPT\(\)](#page-109-0) instead.

```
mysql> SELECT customer_address FROM customer_table 
 > WHERE crypted_credit_card = DES_ENCRYPT('credit_card_number');
```

If [DES\\_ENCRYPT\(\)](#page-114-2) is invoked from within the mysql client, binary strings display using hexadecimal notation, depending on the value of the --binary-as-hex. For more information about that option, see Section 4.5.1, "mysql — The MySQL Command-Line Client".

<span id="page-116-0"></span>• ENCODE(str,[pass\\_str](#page-116-0))

[ENCODE\(\)](#page-116-0) encrypts str using pass\_str as the password. The result is a binary string of the same length as str. To decrypt the result, use [DECODE\(\)](#page-114-0).

![](_page_116_Picture_3.jpeg)

#### **Note**

The [ENCODE\(\)](#page-116-0) and [DECODE\(\)](#page-114-0) functions are deprecated in MySQL 5.7, and should no longer be used. Expect them to be removed in a future MySQL release.

If you still need to use [ENCODE\(\)](#page-116-0), a salt value must be used with it to reduce risk. For example:

```
ENCODE('cleartext', CONCAT('my_random_salt','my_secret_password'))
```

A new random salt value must be used whenever a password is updated.

If [ENCODE\(\)](#page-116-0) is invoked from within the mysql client, binary strings display using hexadecimal notation, depending on the value of the --binary-as-hex. For more information about that option, see Section 4.5.1, "mysql — The MySQL Command-Line Client".

<span id="page-116-1"></span>• [ENCRYPT\(](#page-116-1)str[,salt])

Encrypts str using the Unix crypt() system call and returns a binary string. The salt argument must be a string with at least two characters or else the result is NULL. If no salt argument is given, a random value is used.

![](_page_116_Picture_12.jpeg)

#### **Note**

The [ENCRYPT\(\)](#page-116-1) function is deprecated in MySQL 5.7, are removed in MySQL 8.0, and should no longer be used. For one-way hashing, consider using [SHA2\(\)](#page-118-2) instead.

```
mysql> SELECT ENCRYPT('hello');
 -> 'VxuFAJXVARROc'
```

[ENCRYPT\(\)](#page-116-1) ignores all but the first eight characters of str, at least on some systems. This behavior is determined by the implementation of the underlying crypt() system call.

The use of [ENCRYPT\(\)](#page-116-1) with the ucs2, utf16, utf16le, or utf32 multibyte character sets is not recommended because the system call expects a string terminated by a zero byte.

If crypt() is not available on your system (as is the case with Windows), [ENCRYPT\(\)](#page-116-1) always returns NULL.

If [ENCRYPT\(\)](#page-116-1) is invoked from within the mysql client, binary strings display using hexadecimal notation, depending on the value of the --binary-as-hex. For more information about that option, see Section 4.5.1, "mysql — The MySQL Command-Line Client".

<span id="page-116-2"></span>• [MD5\(](#page-116-2)str)

Calculates an MD5 128-bit checksum for the string. The value is returned as a string of 32 hexadecimal digits, or NULL if the argument was NULL. The return value can, for example, be used as a hash key. See the notes at the beginning of this section about storing hash values efficiently.

The return value is a string in the connection character set.

```
mysql> SELECT MD5('testing');
```

-> 'ae2b1fca515949e5d54fb22b8ed95575'

This is the "RSA Data Security, Inc. MD5 Message-Digest Algorithm."

See the note regarding the MD5 algorithm at the beginning this section.

<span id="page-117-0"></span>• [PASSWORD\(](#page-117-0)str)

![](_page_117_Picture_5.jpeg)

### **Note**

This function is deprecated in MySQL 5.7 and is removed in MySQL 8.0.

Returns a hashed password string calculated from the cleartext password str. The return value is a string in the connection character set, or NULL if the argument is NULL. This function is the SQL interface to the algorithm used by the server to encrypt MySQL passwords for storage in the mysql.user grant table.

The old\_passwords system variable controls the password hashing method used by the [PASSWORD\(\)](#page-117-0) function. It also influences password hashing performed by CREATE USER and GRANT statements that specify a password using an IDENTIFIED BY clause.

The following table shows, for each password hashing method, the permitted value of old\_passwords and which authentication plugins use the hashing method.

| Password Hashing Method  | old_passwords Value | Associated Authentication<br>Plugin |
|--------------------------|---------------------|-------------------------------------|
| MySQL 4.1 native hashing | 0                   | mysql_native_password               |
| SHA-256 hashing          | 2                   | sha256_password                     |

SHA-256 password hashing (old\_passwords=2) uses a random salt value, which makes the result from [PASSWORD\(\)](#page-117-0) nondeterministic. Consequently, statements that use this function are not safe for statement-based replication and cannot be stored in the query cache.

Encryption performed by [PASSWORD\(\)](#page-117-0) is one-way (not reversible), but it is not the same type of encryption used for Unix passwords.

![](_page_117_Picture_14.jpeg)

## **Note**

[PASSWORD\(\)](#page-117-0) is used by the authentication system in MySQL Server; you should not use it in your own applications. For that purpose, consider a more secure function such as [SHA2\(\)](#page-118-2) instead. Also see [RFC 2195, section](http://www.faqs.org/rfcs/rfc2195.md) [2 \(Challenge-Response Authentication Mechanism \(CRAM\)\),](http://www.faqs.org/rfcs/rfc2195.md) for more information about handling passwords and authentication securely in your applications.

![](_page_117_Picture_17.jpeg)

## **Caution**

Under some circumstances, statements that invoke [PASSWORD\(\)](#page-117-0) may be recorded in server logs or on the client side in a history file such as ~/.mysql\_history, which means that cleartext passwords may be read by anyone having read access to that information. For information about the conditions under which this occurs for the server logs and how to control it, see Section 6.1.2.3, "Passwords and Logging". For similar information about client-side logging, see Section 4.5.1.3, "mysql Client Logging".

### <span id="page-118-0"></span>• [RANDOM\\_BYTES\(](#page-118-0)len)

This function returns a binary string of len random bytes generated using the random number generator of the SSL library. Permitted values of len range from 1 to 1024. For values outside that range, an error occurs.

[RANDOM\\_BYTES\(\)](#page-118-0) can be used to provide the initialization vector for the [AES\\_DECRYPT\(\)](#page-109-0) and [AES\\_ENCRYPT\(\)](#page-109-1) functions. For use in that context, len must be at least 16. Larger values are permitted, but bytes in excess of 16 are ignored.

[RANDOM\\_BYTES\(\)](#page-118-0) generates a random value, which makes its result nondeterministic. Consequently, statements that use this function are unsafe for statement-based replication and cannot be stored in the query cache.

If [RANDOM\\_BYTES\(\)](#page-118-0) is invoked from within the mysql client, binary strings display using hexadecimal notation, depending on the value of the --binary-as-hex. For more information about that option, see Section 4.5.1, "mysql — The MySQL Command-Line Client".

<span id="page-118-1"></span>• [SHA1\(](#page-118-1)str), [SHA\(](#page-118-1)str)

Calculates an SHA-1 160-bit checksum for the string, as described in RFC 3174 (Secure Hash Algorithm). The value is returned as a string of 40 hexadecimal digits, or NULL if the argument was NULL. One of the possible uses for this function is as a hash key. See the notes at the beginning of this section about storing hash values efficiently. [SHA\(\)](#page-118-1) is synonymous with [SHA1\(\)](#page-118-1).

The return value is a string in the connection character set.

```
mysql> SELECT SHA1('abc');
 -> 'a9993e364706816aba3e25717850c26c9cd0d89d'
```

[SHA1\(\)](#page-118-1) can be considered a cryptographically more secure equivalent of [MD5\(\)](#page-116-2). However, see the note regarding the MD5 and SHA-1 algorithms at the beginning this section.

<span id="page-118-2"></span>• SHA2(str, [hash\\_length](#page-118-2))

Calculates the SHA-2 family of hash functions (SHA-224, SHA-256, SHA-384, and SHA-512). The first argument is the plaintext string to be hashed. The second argument indicates the desired bit length of the result, which must have a value of 224, 256, 384, 512, or 0 (which is equivalent to 256). If either argument is NULL or the hash length is not one of the permitted values, the return value is NULL. Otherwise, the function result is a hash value containing the desired number of bits. See the notes at the beginning of this section about storing hash values efficiently.

The return value is a string in the connection character set.

```
mysql> SELECT SHA2('abc', 224);
 -> '23097d223405d8228642a477bda255b32aadbce4bda0b3f7e36c9da7'
```

This function works only if MySQL has been configured with SSL support. See Section 6.3, "Using Encrypted Connections".

[SHA2\(\)](#page-118-2) can be considered cryptographically more secure than [MD5\(\)](#page-116-2) or [SHA1\(\)](#page-118-1).

<span id="page-118-3"></span>• UNCOMPRESS([string\\_to\\_uncompress](#page-118-3))

Uncompresses a string compressed by the [COMPRESS\(\)](#page-113-0) function. If the argument is not a compressed value, the result is NULL. This function requires MySQL to have been compiled with a compression library such as zlib. Otherwise, the return value is always NULL.

```
mysql> SELECT UNCOMPRESS(COMPRESS('any string'));
 -> 'any string'
mysql> SELECT UNCOMPRESS('any string');
 -> NULL
```

<span id="page-119-0"></span>• [UNCOMPRESSED\\_LENGTH\(](#page-119-0)compressed\_string)

Returns the length that the compressed string had before being compressed.

```
mysql> SELECT UNCOMPRESSED_LENGTH(COMPRESS(REPEAT('a',30)));
 -> 30
```

<span id="page-119-1"></span>• [VALIDATE\\_PASSWORD\\_STRENGTH\(](#page-119-1)str)

Given an argument representing a plaintext password, this function returns an integer to indicate how strong the password is. The return value ranges from 0 (weak) to 100 (strong).

Password assessment by [VALIDATE\\_PASSWORD\\_STRENGTH\(\)](#page-119-1) is done by the validate\_password plugin. If that plugin is not installed, the function always returns 0. For information about installing validate\_password, see Section 6.4.3, "The Password Validation Plugin". To examine or configure the parameters that affect password testing, check or set the system variables implemented by validate\_password. See Section 6.4.3.2, "Password Validation Plugin Options and Variables".

The password is subjected to increasingly strict tests and the return value reflects which tests were satisfied, as shown in the following table. In addition, if the validate\_password\_check\_user\_name system variable is enabled and the password matches the user name, [VALIDATE\\_PASSWORD\\_STRENGTH\(\)](#page-119-1) returns 0 regardless of how other validate\_password system variables are set.

| Password Test               | Return Value |
|-----------------------------|--------------|
| Length < 4                  | 0            |
| Length ≥ 4 and <            | 25           |
| validate_password_length    |              |
| Satisfies policy 1 (LOW)    | 50           |
| Satisfies policy 2 (MEDIUM) | 75           |
| Satisfies policy 3 (STRONG) | 100          |