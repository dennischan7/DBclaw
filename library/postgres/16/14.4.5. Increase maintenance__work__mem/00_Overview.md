---
source: PostgreSQL 16 Reference
title: 00_Overview
---

Temporarily increasing the maintenance\_work\_mem configuration variable when loading large amounts of data can lead to improved performance. This will help to speed up CREATE INDEX commands and ALTER TABLE ADD FOREIGN KEY commands. It won't do much for COPY itself, so this advice is only useful when you are using one or both of the above techniques.