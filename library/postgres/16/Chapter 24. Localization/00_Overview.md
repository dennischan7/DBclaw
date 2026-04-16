---
source: PostgreSQL 16 Reference
title: 00_Overview
---

This chapter describes the available localization features from the point of view of the administrator. PostgreSQL supports two localization facilities:

- Using the locale features of the operating system to provide locale-specific collation order, number formatting, translated messages, and other aspects. This is covered in [Section 24.1](#page-161-0) and [Section 24.2.](#page-165-0)
- Providing a number of different character sets to support storing text in all kinds of languages, and providing character set translation between client and server. This is covered in [Section 24.3.](#page-175-0)

# <span id="page-161-0"></span>**24.1. Locale Support**

*Locale* support refers to an application respecting cultural preferences regarding alphabets, sorting, number formatting, etc. PostgreSQL uses the standard ISO C and POSIX locale facilities provided by the server operating system. For additional information refer to the documentation of your system.