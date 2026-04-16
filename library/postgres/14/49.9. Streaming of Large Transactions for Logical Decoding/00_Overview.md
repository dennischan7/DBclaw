---
source: PostgreSQL 14 Reference
title: 00_Overview
---

The basic output plugin callbacks (e.g., begin\_cb, change\_cb, commit\_cb and message\_cb) are only invoked when the transaction actually commits. The changes are still decoded from the transaction log, but are only passed to the output plugin at commit (and discarded if the transaction aborts).

This means that while the decoding happens incrementally, and may spill to disk to keep memory usage under control, all the decoded changes have to be transmitted when the transaction finally commits (or more precisely, when the commit is decoded from the transaction log). Depending on the size of the transaction and network bandwidth, the transfer time may significantly increase the apply lag.

To reduce the apply lag caused by large transactions, an output plugin may provide additional callback to support incremental streaming of in-progress transactions. There are multiple required streaming callbacks (stream\_start\_cb, stream\_stop\_cb, stream\_abort\_cb, stream\_commit\_cb and stream\_change\_cb) and two optional callbacks (stream\_message\_cb and stream\_truncate\_cb).

When streaming an in-progress transaction, the changes (and messages) are streamed in blocks demarcated by stream\_start\_cb and stream\_stop\_cb callbacks. Once all the decoded changes are transmitted, the transaction can be committed using the the stream\_commit\_cb callback (or possibly aborted using the stream\_abort\_cb callback). If two-phase commits are supported, the transaction can be prepared using the stream\_prepare\_cb callback, COMMIT PREPARED using the commit\_prepared\_cb callback or aborted using the rollback\_prepared\_cb.

One example sequence of streaming callback calls for one transaction may look like this:

```
stream_start_cb(...); <-- start of first block of changes
 stream_change_cb(...);
 stream_change_cb(...);
 stream_message_cb(...);
 stream_change_cb(...);
 ...
 stream_change_cb(...);
stream_stop_cb(...); <-- end of first block of changes
stream_start_cb(...); <-- start of second block of changes
 stream_change_cb(...);
 stream_change_cb(...);
 stream_change_cb(...);
 ...
 stream_message_cb(...);
 stream_change_cb(...);
stream_stop_cb(...); <-- end of second block of changes
stream_commit_cb(...); <-- commit of the streamed transaction
```

The actual sequence of callback calls may be more complicated, of course. There may be blocks for multiple streamed transactions, some of the transactions may get aborted, etc.

Similar to spill-to-disk behavior, streaming is triggered when the total amount of changes decoded from the WAL (for all in-progress transactions) exceeds the limit defined by logical\_decoding\_work\_mem setting. At that point, the largest top-level transaction (measured by the amount of memory currently used for decoded changes) is selected and streamed. However, in some cases we still have to spill to disk even if streaming is enabled because we exceed the memory threshold but still have not decoded the complete tuple e.g., only decoded toast table insert but not the main table insert.

Even when streaming large transactions, the changes are still applied in commit order, preserving the same guarantees as the non-streaming mode.