---
source: PostgreSQL 16 Reference
title: 00_Overview
---

PostgreSQL provides two data types that are designed to support full text search, which is the activity of searching through a collection of natural-language *documents* to locate those that best match a *query*. The tsvector type represents a document in a form optimized for text search; the tsquery type similarly represents a text query. Chapter 12 provides a detailed explanation of this facility, and [Section 9.13](#page-138-0) summarizes the related functions and operators.