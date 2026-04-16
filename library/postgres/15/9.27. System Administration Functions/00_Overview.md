---
source: PostgreSQL 15 Reference
title: 00_Overview
---

The functions described in this section are used to control and monitor a PostgreSQL installation.

## <span id="page-24-0"></span>**9.27.1. Configuration Settings Functions**

[Table 9.87](#page-24-0) shows the functions available to query and alter run-time configuration parameters.

### **Table 9.87. Configuration Settings Functions**

| Function |                                                                                                                                                                                                                                                                                                                                                                                                  |
|----------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|          | Description<br>Example(s)                                                                                                                                                                                                                                                                                                                                                                        |
|          | current_setting ( setting_name text [, missing_ok boolean ] ) → text<br>Returns the current value of the setting setting_name. If there is no such setting,<br>current_setting throws an error unless missing_ok is supplied and is true (in<br>which case NULL is returned). This function corresponds to the SQL command SHOW.<br>current_setting('datestyle') → ISO, MDY                      |
|          | set_config ( setting_name text, new_value text, is_local boolean ) →<br>text<br>Sets the parameter setting_name to new_value, and returns that value. If is_lo<br>cal is true, the new value will only apply during the current transaction. If you want<br>the new value to apply for the rest of the current session, use false instead. This func<br>tion corresponds to the SQL command SET. |
|          | set_config('log_statement_stats', 'off', false) → off                                                                                                                                                                                                                                                                                                                                            |