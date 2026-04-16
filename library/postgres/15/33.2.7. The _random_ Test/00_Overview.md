---
source: PostgreSQL 15 Reference
title: 00_Overview
---

The random test script is intended to produce random results. In very rare cases, this causes that regression test to fail. Typing:

diff results/random.out expected/random.out

should produce only one or a few lines of differences. You need not worry unless the random test fails repeatedly.