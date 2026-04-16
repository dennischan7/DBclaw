---
source: PostgreSQL 14 Reference
title: 00_Overview
---

The individual protocol messages are discussed in the following subsections. Individual messages are described in [Section 53.9](#page-120-0).

All top-level protocol messages begin with a message type byte. While represented in code as a character, this is a signed byte with no associated encoding.

Since the streaming replication protocol supplies a message length there is no need for top-level protocol messages to embed a length in their header.