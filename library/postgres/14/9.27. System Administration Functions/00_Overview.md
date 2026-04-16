---
source: PostgreSQL 14 Reference
title: 00_Overview
---

The functions described in this section are used to control and monitor a PostgreSQL installation.

## <span id="page-18-3"></span>**9.27.1. Configuration Settings Functions**

[Table 9.85](#page-18-3) shows the functions available to query and alter run-time configuration parameters.

**Table 9.85. Configuration Settings Functions**

| Function                                                             |
|----------------------------------------------------------------------|
| Description<br>Example(s)                                            |
| current_setting ( setting_name text [, missing_ok boolean ] ) → text |

Returns the current value of the setting setting\_name. If there is no such setting, current\_setting throws an error unless missing\_ok is supplied and is true (in which case NULL is returned). This function corresponds to the SQL command SHOW.

### **Description Example(s)**

```
current_setting('datestyle') → ISO, MDY
```

set\_config ( setting\_name text, new\_value text, is\_local boolean ) → text

Sets the parameter setting\_name to new\_value, and returns that value. If is\_local is true, the new value will only apply during the current transaction. If you want the new value to apply for the rest of the current session, use false instead. This function corresponds to the SQL command SET.

set\_config('log\_statement\_stats', 'off', false) → off