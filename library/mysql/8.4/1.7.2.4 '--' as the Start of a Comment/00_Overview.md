---
source: MySQL 8.4 Reference
title: 00_Overview
---

Standard SQL uses the C syntax /\* this is a comment \*/ for comments, and MySQL Server supports this syntax as well. MySQL also support extensions to this syntax that enable MySQL-specific SQL to be embedded in the comment; see Section 11.7, "Comments".

MySQL Server also uses # as the start comment character. This is nonstandard.

Standard SQL also uses "--" as a start-comment sequence. MySQL Server supports a variant of the -- comment style; the -- start-comment sequence is accepted as such, but must be followed by a whitespace character such as a space or newline. The space is intended to prevent problems with generated SQL queries that use constructs such as the following, which updates the balance to reflect a charge:

```
UPDATE account SET balance=balance-charge
WHERE account_id=user_id
```

Consider what happens when charge has a negative value such as -1, which might be the case when an amount is credited to the account. In this case, the generated statement looks like this:

```
UPDATE account SET balance=balance--1
WHERE account_id=5752;
```

balance--1 is valid standard SQL, but -- is interpreted as the start of a comment, and part of the expression is discarded. The result is a statement that has a completely different meaning than intended:

```
UPDATE account SET balance=balance
WHERE account_id=5752;
```

This statement produces no change in value at all. To keep this from happening, MySQL requires a whitespace character following the -- for it to be recognized as a start-comment sequence in MySQL Server, so that an expression such as balance--1 is always safe to use.

# <span id="page-81-0"></span>**1.7.3 How MySQL Deals with Constraints**

MySQL enables you to work both with transactional tables that permit rollback and with nontransactional tables that do not. Because of this, constraint handling is a bit different in MySQL than in other DBMSs. We must handle the case when you have inserted or updated a lot of rows in a nontransactional table for which changes cannot be rolled back when an error occurs.

The basic philosophy is that MySQL Server tries to produce an error for anything that it can detect while parsing a statement to be executed, and tries to recover from any errors that occur while executing the statement. We do this in most cases, but not yet for all.

The options MySQL has when an error occurs are to stop the statement in the middle or to recover as well as possible from the problem and continue. By default, the server follows the latter course. This means, for example, that the server may coerce invalid values to the closest valid values.

Several SQL mode options are available to provide greater control over handling of bad data values and whether to continue statement execution or abort when errors occur. Using these options, you can configure MySQL Server to act in a more traditional fashion that is like other DBMSs that reject improper input. The SQL mode can be set globally at server startup to affect all clients. Individual clients can set the SQL mode at runtime, which enables each client to select the behavior most appropriate for its requirements. See Section 7.1.11, "Server SQL Modes".

The following sections describe how MySQL Server handles different types of constraints.