---
source: PostgreSQL 16 Reference
title: 00_Overview
---

pg\_event\_trigger\_dropped\_objects () → setof record

pg\_event\_trigger\_dropped\_objects returns a list of all objects dropped by the command in whose sql\_drop event it is called. If called in any other context, an error is raised. This function returns the following columns:

| Name            | Type    | Description                                                                                                                                                                                                  |
|-----------------|---------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| classid         | oid     | OID of catalog the object be<br>longed in                                                                                                                                                                    |
| objid           | oid     | OID of the object itself                                                                                                                                                                                     |
| objsubid        | integer | Sub-object ID (e.g., attribute<br>number for a column)                                                                                                                                                       |
| original        | boolean | True if this was one of the root<br>object(s) of the deletion                                                                                                                                                |
| normal          | boolean | True if there was a normal de<br>pendency relationship in the de<br>pendency graph leading to this<br>object                                                                                                 |
| is_temporary    | boolean | True if this was a temporary ob<br>ject                                                                                                                                                                      |
| object_type     | text    | Type of the object                                                                                                                                                                                           |
| schema_name     | text    | Name of the schema the object<br>belonged in, if any; otherwise<br>NULL. No quoting is applied.                                                                                                              |
| object_name     | text    | Name of the object, if the com<br>bination of schema and name<br>can be used as a unique iden<br>tifier for the object; otherwise<br>NULL. No quoting is applied,<br>and name is never schema-qual<br>ified. |
| object_identity | text    | Text rendering of the object<br>identity, schema-qualified. Each<br>identifier included in the identi<br>ty is quoted if necessary.                                                                          |
| address_names   | text[]  | An array that, together with<br>object_type and ad<br>dress_args, can be used by<br>the pg_get_object_ad<br>dress function to recreate<br>the object address in a remote                                     |

| Name         | Type   | Description                                                        |
|--------------|--------|--------------------------------------------------------------------|
|              |        | server containing an identically<br>named object of the same kind. |
| address_args | text[] | Complement for ad<br>dress_names                                   |

The pg\_event\_trigger\_dropped\_objects function can be used in an event trigger like this:

```
CREATE FUNCTION test_event_trigger_for_drops()
 RETURNS event_trigger LANGUAGE plpgsql AS $$
DECLARE
 obj record;
BEGIN
 FOR obj IN SELECT * FROM pg_event_trigger_dropped_objects()
 LOOP
 RAISE NOTICE '% dropped object: % %.% %',
 tg_tag,
 obj.object_type,
 obj.schema_name,
 obj.object_name,
 obj.object_identity;
 END LOOP;
END;
$$;
CREATE EVENT TRIGGER test_event_trigger_for_drops
 ON sql_drop
 EXECUTE FUNCTION test_event_trigger_for_drops();
```