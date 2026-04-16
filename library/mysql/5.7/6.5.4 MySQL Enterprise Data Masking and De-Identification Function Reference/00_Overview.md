---
source: MySQL 5.7 Reference
title: 00_Overview
---

**Table 6.35 MySQL Enterprise Data Masking and De-Identification Functions**

| Name                  | Description                         |
|-----------------------|-------------------------------------|
| gen_blacklist()       | Perform dictionary term replacement |
| gen_dictionary_drop() | Remove dictionary from registry     |
| gen_dictionary_load() | Load dictionary into registry       |
| gen_dictionary()      | Return random term from dictionary  |
| gen_range()           | Generate random number within range |

| Name               | Description                                                |
|--------------------|------------------------------------------------------------|
| gen_rnd_email()    | Generate random email address                              |
| gen_rnd_pan()      | Generate random payment card Primary Account<br>Number     |
| gen_rnd_ssn()      | Generate random US Social Security Number                  |
| gen_rnd_us_phone() | Generate random US phone number                            |
| mask_inner()       | Mask interior part of string                               |
| mask_outer()       | Mask left and right parts of string                        |
| mask_pan()         | Mask payment card Primary Account Number part<br>of string |
| mask_pan_relaxed() | Mask payment card Primary Account Number part<br>of string |
| mask_ssn()         | Mask US Social Security Number                             |

# <span id="page-121-0"></span>**6.5.5 MySQL Enterprise Data Masking and De-Identification Function Descriptions**

The MySQL Enterprise Data Masking and De-Identification plugin library includes several functions, which may be grouped into these categories:

- [Data Masking Functions](#page-121-2)
- [Random Data Generation Functions](#page-124-2)
- [Random Data Dictionary-Based Functions](#page-127-2)

These functions treat string arguments as binary strings (which means they do not distinguish lettercase), and string return values are binary strings. If a string return value should be in a different character set, convert it. The following example shows how to convert the result of [gen\\_rnd\\_email\(\)](#page-125-0) to the utf8mb4 character set:

```
SET @email = CONVERT(gen_rnd_email() USING utf8mb4);
```

It may also be necessary to convert string arguments, as illustrated in [Using Masked Data for](#page-119-0) [Customer Identification](#page-119-0).

If a MySQL Enterprise Data Masking and De-Identification function is invoked from within the mysql client, binary string results display using hexadecimal notation, depending on the value of the - binary-as-hex. For more information about that option, see Section 4.5.1, "mysql — The MySQL Command-Line Client".

## <span id="page-121-2"></span>**Data Masking Functions**

Each function in this section performs a masking operation on its string argument and returns the masked result.

<span id="page-121-1"></span>• [mask\\_inner\(](#page-121-1)str, margin1, margin2 [, mask\_char])

Masks the interior part of a string, leaving the ends untouched, and returns the result. An optional masking character can be specified.

#### Arguments:

- str: The string to mask.
- margin1: A nonnegative integer that specifies the number of characters on the left end of the string to remain unmasked. If the value is 0, no left end characters remain unmasked.

- margin2: A nonnegative integer that specifies the number of characters on the right end of the string to remain unmasked. If the value is 0, no right end characters remain unmasked.
- mask\_char: (Optional) The single character to use for masking. The default is 'X' if mask\_char is not given.

The masking character must be a single-byte character. Attempts to use a multibyte character produce an error.

#### Return value:

The masked string, or NULL if either margin is negative.

If the sum of the margin values is larger than the argument length, no masking occurs and the argument is returned unchanged.

#### Example:

```
mysql> SELECT mask_inner('abcdef', 1, 2), mask_inner('abcdef',0, 5);
+----------------------------+---------------------------+
| mask_inner('abcdef', 1, 2) | mask_inner('abcdef',0, 5) |
+----------------------------+---------------------------+
| aXXXef | Xbcdef |
+----------------------------+---------------------------+
mysql> SELECT mask_inner('abcdef', 1, 2, '*'), mask_inner('abcdef',0, 5, '#');
+---------------------------------+--------------------------------+
| mask_inner('abcdef', 1, 2, '*') | mask_inner('abcdef',0, 5, '#') |
+---------------------------------+--------------------------------+
| a***ef | #bcdef |
+---------------------------------+--------------------------------+
```

<span id="page-122-0"></span>• [mask\\_outer\(](#page-122-0)str, margin1, margin2 [, mask\_char])

Masks the left and right ends of a string, leaving the interior unmasked, and returns the result. An optional masking character can be specified.

#### Arguments:

- str: The string to mask.
- margin1: A nonnegative integer that specifies the number of characters on the left end of the string to mask. If the value is 0, no left end characters are masked.
- margin2: A nonnegative integer that specifies the number of characters on the right end of the string to mask. If the value is 0, no right end characters are masked.
- mask\_char: (Optional) The single character to use for masking. The default is 'X' if mask\_char is not given.

The masking character must be a single-byte character. Attempts to use a multibyte character produce an error.

#### Return value:

The masked string, or NULL if either margin is negative.

If the sum of the margin values is larger than the argument length, the entire argument is masked.

```
mysql> SELECT mask_outer('abcdef', 1, 2), mask_outer('abcdef',0, 5);
+----------------------------+---------------------------+
| mask_outer('abcdef', 1, 2) | mask_outer('abcdef',0, 5) |
+----------------------------+---------------------------+
```

```
| XbcdXX | aXXXXX |
+----------------------------+---------------------------+
mysql> SELECT mask_outer('abcdef', 1, 2, '*'), mask_outer('abcdef',0, 5, '#');
+---------------------------------+--------------------------------+
| mask_outer('abcdef', 1, 2, '*') | mask_outer('abcdef',0, 5, '#') |
+---------------------------------+--------------------------------+
| *bcd** | a##### |
+---------------------------------+--------------------------------+
```

<span id="page-123-0"></span>• [mask\\_pan\(](#page-123-0)str)

Masks a payment card Primary Account Number and returns the number with all but the last four digits replaced by 'X' characters.

#### Arguments:

• str: The string to mask. The string must be a suitable length for the Primary Account Number, but is not otherwise checked.

#### Return value:

The masked payment number as a string. If the argument is shorter than required, it is returned unchanged.

#### Example:

```
mysql> SELECT mask_pan(gen_rnd_pan());
+-------------------------+
| mask_pan(gen_rnd_pan()) |
+-------------------------+
| XXXXXXXXXXXX9102 |
+-------------------------+
mysql> SELECT mask_pan(gen_rnd_pan(19));
+---------------------------+
| mask_pan(gen_rnd_pan(19)) |
+---------------------------+
| XXXXXXXXXXXXXXX8268 |
+---------------------------+
mysql> SELECT mask_pan('a*Z');
+-----------------+
| mask_pan('a*Z') |
+-----------------+
| a*Z |
+-----------------+
```

<span id="page-123-1"></span>• [mask\\_pan\\_relaxed\(](#page-123-1)str)

Masks a payment card Primary Account Number and returns the number with all but the first six and last four digits replaced by 'X' characters. The first six digits indicate the payment card issuer.

#### Arguments:

• str: The string to mask. The string must be a suitable length for the Primary Account Number, but is not otherwise checked.

#### Return value:

The masked payment number as a string. If the argument is shorter than required, it is returned unchanged.

```
mysql> SELECT mask_pan_relaxed(gen_rnd_pan());
+---------------------------------+
| mask_pan_relaxed(gen_rnd_pan()) |
+---------------------------------+
| 551279XXXXXX3108 |
```

```
+---------------------------------+
mysql> SELECT mask_pan_relaxed(gen_rnd_pan(19));
+-----------------------------------+
| mask_pan_relaxed(gen_rnd_pan(19)) |
+-----------------------------------+
| 462634XXXXXXXXX6739 |
+-----------------------------------+
mysql> SELECT mask_pan_relaxed('a*Z');
+-------------------------+
| mask_pan_relaxed('a*Z') |
+-------------------------+
| a*Z |
+-------------------------+
```

<span id="page-124-0"></span>• [mask\\_ssn\(](#page-124-0)str)

Masks a US Social Security number and returns the number with all but the last four digits replaced by 'X' characters.

#### Arguments:

• str: The string to mask. The string must be 11 characters long, but is not otherwise checked.

#### Return value:

The masked Social Security number as a string, or NULL if the argument is not the correct length.

#### Example:

```
mysql> SELECT mask_ssn('909-63-6922'), mask_ssn('abcdefghijk');
+-------------------------+-------------------------+
| mask_ssn('909-63-6922') | mask_ssn('abcdefghijk') |
+-------------------------+-------------------------+
| XXX-XX-6922 | XXX-XX-hijk |
+-------------------------+-------------------------+
mysql> SELECT mask_ssn('909');
+-----------------+
| mask_ssn('909') |
+-----------------+
| NULL |
+-----------------+
```

## <span id="page-124-2"></span>**Random Data Generation Functions**

The functions in this section generate random values for different types of data. When possible, generated values have characteristics reserved for demonstration or test values, to avoid having them mistaken for legitimate data. For example, [gen\\_rnd\\_us\\_phone\(\)](#page-126-1) returns a US phone number that uses the 555 area code, which is not assigned to phone numbers in actual use. Individual function descriptions describe any exceptions to this principle.

<span id="page-124-1"></span>• [gen\\_range\(](#page-124-1)lower, upper)

Generates a random number chosen from a specified range.

#### Arguments:

- lower: An integer that specifies the lower boundary of the range.
- upper: An integer that specifies the upper boundary of the range, which must not be less than the lower boundary.

## Return value:

A random integer in the range from lower to upper, inclusive, or NULL if the upper argument is less than lower.

#### Example:

```
mysql> SELECT gen_range(100, 200), gen_range(-1000, -800);
+---------------------+------------------------+
| gen_range(100, 200) | gen_range(-1000, -800) |
+---------------------+------------------------+
| 177 | -917 |
+---------------------+------------------------+
mysql> SELECT gen_range(1, 0);
+-----------------+
| gen_range(1, 0) |
+-----------------+
| NULL |
+-----------------+
```

<span id="page-125-0"></span>• [gen\\_rnd\\_email\(\)](#page-125-0)

Generates a random email address in the example.com domain.

Arguments:

None.

Return value:

A random email address as a string.

#### Example:

```
mysql> SELECT gen_rnd_email();
+---------------------------+
| gen_rnd_email() |
+---------------------------+
| ijocv.mwvhhuf@example.com |
+---------------------------+
```

<span id="page-125-1"></span>• [gen\\_rnd\\_pan\(\[](#page-125-1)size])

Generates a random payment card Primary Account Number. The number passes the Luhn check (an algorithm that performs a checksum verification against a check digit).

![](_page_125_Picture_13.jpeg)

#### **Warning**

Values returned from [gen\\_rnd\\_pan\(\)](#page-125-1) should be used only for test purposes, and are not suitable for publication. There is no way to guarantee that a given return value is not assigned to a legitimate payment account. Should it be necessary to publish a [gen\\_rnd\\_pan\(\)](#page-125-1) result, consider masking it with [mask\\_pan\(\)](#page-123-0) or [mask\\_pan\\_relaxed\(\)](#page-123-1).

#### Arguments:

• size: (Optional) An integer that specifies the size of the result. The default is 16 if size is not given. If given, size must be an integer in the range from 12 to 19.

#### Return value:

A random payment number as a string, or NULL if a size argument outside the permitted range is given.

```
mysql> SELECT mask_pan(gen_rnd_pan());
+-------------------------+
| mask_pan(gen_rnd_pan()) |
+-------------------------+
```

```
| XXXXXXXXXXXX5805 |
+-------------------------+
mysql> SELECT mask_pan(gen_rnd_pan(19));
+---------------------------+
| mask_pan(gen_rnd_pan(19)) |
+---------------------------+
| XXXXXXXXXXXXXXX5067 |
+---------------------------+
mysql> SELECT mask_pan_relaxed(gen_rnd_pan());
+---------------------------------+
| mask_pan_relaxed(gen_rnd_pan()) |
+---------------------------------+
| 398403XXXXXX9547 |
+---------------------------------+
mysql> SELECT mask_pan_relaxed(gen_rnd_pan(19));
+-----------------------------------+
| mask_pan_relaxed(gen_rnd_pan(19)) |
+-----------------------------------+
| 578416XXXXXXXXX6509 |
+-----------------------------------+
mysql> SELECT gen_rnd_pan(11), gen_rnd_pan(20);
+-----------------+-----------------+
| gen_rnd_pan(11) | gen_rnd_pan(20) |
+-----------------+-----------------+
| NULL | NULL |
+-----------------+-----------------+
```

<span id="page-126-0"></span>• [gen\\_rnd\\_ssn\(\)](#page-126-0)

Generates a random US Social Security number in AAA-BB-CCCC format. The AAA part is greater than 900 and the BB part is less than 70; these values are outside the ranges used for legitimate Social Security numbers.

Arguments:

None.

Return value:

A random Social Security number as a string.

#### Example:

```
mysql> SELECT gen_rnd_ssn();
+---------------+
| gen_rnd_ssn() |
+---------------+
| 951-26-0058 |
+---------------+
```

<span id="page-126-1"></span>• [gen\\_rnd\\_us\\_phone\(\)](#page-126-1)

Generates a random US phone number in 1-555-AAA-BBBB format. The 555 area code is not used for legitimate phone numbers.

Arguments:

None.

Return value:

A random US phone number as a string.

```
mysql> SELECT gen_rnd_us_phone();
+--------------------+
| gen_rnd_us_phone() |
```

```
+--------------------+
| 1-555-682-5423 |
+--------------------+
```

## <span id="page-127-2"></span>**Random Data Dictionary-Based Functions**

The functions in this section manipulate dictionaries of terms and perform generation and masking operations based on them. Some of these functions require the SUPER privilege.

When a dictionary is loaded, it becomes part of the dictionary registry and is assigned a name to be used by other dictionary functions. Dictionaries are loaded from plain text files containing one term per line. Empty lines are ignored. To be valid, a dictionary file must contain at least one nonempty line.

<span id="page-127-1"></span>• gen\_blacklist(str, dictionary\_name, [replacement\\_dictionary\\_name](#page-127-1))

Replaces a term present in one dictionary with a term from a second dictionary and returns the replacement term. This masks the original term by substitution.

#### Arguments:

- str: A string that indicates the term to replace.
- dictionary\_name: A string that names the dictionary containing the term to replace.
- replacement\_dictionary\_name: A string that names the dictionary from which to choose the replacement term.

#### Return value:

A string randomly chosen from replacement\_dictionary\_name as a replacement for str, or str if it does not appear in dictionary\_name, or NULL if either dictionary name is not in the dictionary registry.

If the term to replace appears in both dictionaries, it is possible for the return value to be the same term.

#### Example:

```
mysql> SELECT gen_blacklist('Berlin', 'DE_Cities', 'US_Cities');
+---------------------------------------------------+
| gen_blacklist('Berlin', 'DE_Cities', 'US_Cities') |
+---------------------------------------------------+
| Phoenix |
+---------------------------------------------------+
```

<span id="page-127-0"></span>• [gen\\_dictionary\(](#page-127-0)dictionary\_name)

Returns a random term from a dictionary.

#### Arguments:

• dictionary\_name: A string that names the dictionary from which to choose the term.

## Return value:

A random term from the dictionary as a string, or NULL if the dictionary name is not in the dictionary registry.

```
mysql> SELECT gen_dictionary('mydict');
+--------------------------+
| gen_dictionary('mydict') |
+--------------------------+
| My term |
```

```
+--------------------------+
mysql> SELECT gen_dictionary('no-such-dict');
+--------------------------------+
| gen_dictionary('no-such-dict') |
+--------------------------------+
| NULL |
+--------------------------------+
```

<span id="page-128-0"></span>• [gen\\_dictionary\\_drop\(](#page-128-0)dictionary\_name)

Removes a dictionary from the dictionary registry.

This function requires the SUPER privilege.

#### Arguments:

• dictionary\_name: A string that names the dictionary to remove from the dictionary registry.

#### Return value:

A string that indicates whether the drop operation succeeded. Dictionary removed indicates success. Dictionary removal error indicates failure.

```
mysql> SELECT gen_dictionary_drop('mydict');
+-------------------------------+
| gen_dictionary_drop('mydict') |
+-------------------------------+
| Dictionary removed |
+-------------------------------+
mysql> SELECT gen_dictionary_drop('no-such-dict');
+-------------------------------------+
| gen_dictionary_drop('no-such-dict') |
+-------------------------------------+
| Dictionary removal error |
+-------------------------------------+
```

<span id="page-129-0"></span>• [gen\\_dictionary\\_load\(](#page-129-0)dictionary\_path, dictionary\_name)

Loads a file into the dictionary registry and assigns the dictionary a name to be used with other functions that require a dictionary name argument.

This function requires the SUPER privilege.

![](_page_129_Picture_4.jpeg)

#### **Important**

Dictionaries are not persistent. Any dictionary used by applications must be loaded for each server startup.

Once loaded into the registry, a dictionary is used as is, even if the underlying dictionary file changes. To reload a dictionary, first drop it with [gen\\_dictionary\\_drop\(\)](#page-128-0), then load it again with [gen\\_dictionary\\_load\(\)](#page-129-0).

### Arguments:

- dictionary\_path: A string that specifies the path name of the dictionary file.
- dictionary\_name: A string that provides a name for the dictionary.

#### Return value:

A string that indicates whether the load operation succeeded. Dictionary load success indicates success. Dictionary load error indicates failure. Dictionary load failure can occur for several reasons, including:

- A dictionary with the given name is already loaded.
- The dictionary file is not found.
- The dictionary file contains no terms.
- The secure\_file\_priv system variable is set and the dictionary file is not located in the directory named by the variable.

#### Example:

```
mysql> SELECT gen_dictionary_load('/usr/local/mysql/mysql-files/mydict','mydict');
+---------------------------------------------------------------------+
| gen_dictionary_load('/usr/local/mysql/mysql-files/mydict','mydict') |
+---------------------------------------------------------------------+
| Dictionary load success |
+---------------------------------------------------------------------+
mysql> SELECT gen_dictionary_load('/dev/null','null');
+-----------------------------------------+
| gen_dictionary_load('/dev/null','null') |
+-----------------------------------------+
| Dictionary load error |
+-----------------------------------------+
```