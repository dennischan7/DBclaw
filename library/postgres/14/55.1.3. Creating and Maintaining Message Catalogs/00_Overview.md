---
source: PostgreSQL 14 Reference
title: 00_Overview
---

OK, so how does one create a "blank" message catalog? First, go into the directory that contains the program whose messages you want to translate. If there is a file nls.mk, then this program has been prepared for translation.

If there are already some .po files, then someone has already done some translation work. The files are named language.po, where language is the [ISO 639-1 two-letter language code \(in lower](https://www.loc.gov/standards/iso639-2/php/English_list.php) [case\)](https://www.loc.gov/standards/iso639-2/php/English_list.php)<sup>1</sup> , e.g., fr.po for French. If there is really a need for more than one translation effort per language then the files can also be named language\_region.po where region is the [ISO 3166-1 two](https://www.iso.org/iso-3166-country-codes.md)[letter country code \(in upper case\)](https://www.iso.org/iso-3166-country-codes.md)<sup>2</sup> , e.g., pt\_BR.po for Portuguese in Brazil. If you find the language you wanted you can just start working on that file.

If you need to start a new translation effort, then first run the command:

```
make init-po
```

This will create a file progname.pot. (.pot to distinguish it from PO files that are "in production". The T stands for "template".) Copy this file to language.po and edit it. To make it known that the new language is available, also edit the file nls.mk and add the language (or language and country) code to the line that looks like:

```
AVAIL_LANGUAGES := de fr
```

(Other languages can appear, of course.)

As the underlying program or library changes, messages might be changed or added by the programmers. In this case you do not need to start from scratch. Instead, run the command:

```
make update-po
```

which will create a new blank message catalog file (the pot file you started with) and will merge it with the existing PO files. If the merge algorithm is not sure about a particular message it marks it "fuzzy" as explained above. The new PO file is saved with a .po.new extension.

<sup>1</sup> [https://www.loc.gov/standards/iso639-2/php/English\\_list.php](https://www.loc.gov/standards/iso639-2/php/English_list.php)

<sup>2</sup> <https://www.iso.org/iso-3166-country-codes.html>