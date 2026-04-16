---
source: MySQL 8.0 Reference
title: 00_Overview
---

#### **Table 14.32 Internal Functions**

| Name                                 | Description       |
|--------------------------------------|-------------------|
| CAN_ACCESS_COLUMN()                  | Internal use only |
| CAN_ACCESS_DATABASE()                | Internal use only |
| CAN_ACCESS_TABLE()                   | Internal use only |
| CAN_ACCESS_USER()                    | Internal use only |
| CAN_ACCESS_VIEW()                    | Internal use only |
| GET_DD_COLUMN_PRIVILEGES()           | Internal use only |
| GET_DD_CREATE_OPTIONS()              | Internal use only |
| GET_DD_INDEX_SUB_PART_LENGTH()       | Internal use only |
| INTERNAL_AUTO_INCREMENT()            | Internal use only |
| INTERNAL_AVG_ROW_LENGTH()            | Internal use only |
| INTERNAL_CHECK_TIME()                | Internal use only |
| INTERNAL_CHECKSUM()                  | Internal use only |
| INTERNAL_DATA_FREE()                 | Internal use only |
| INTERNAL_DATA_LENGTH()               | Internal use only |
| INTERNAL_DD_CHAR_LENGTH()            | Internal use only |
| INTERNAL_GET_COMMENT_OR_ERROR()      | Internal use only |
| INTERNAL_GET_ENABLED_ROLE_JSON()     | Internal use only |
| INTERNAL_GET_HOSTNAME()              | Internal use only |
| INTERNAL_GET_USERNAME()              | Internal use only |
| INTERNAL_GET_VIEW_WARNING_OR_ERROR() | Internal use only |
| INTERNAL_INDEX_COLUMN_CARDINALITY()  | Internal use only |
| INTERNAL_INDEX_LENGTH()              | Internal use only |
| INTERNAL_IS_ENABLED_ROLE()           | Internal use only |
| INTERNAL_IS_MANDATORY_ROLE()         | Internal use only |

| Name                       | Description       |
|----------------------------|-------------------|
| INTERNAL_KEYS_DISABLED()   | Internal use only |
| INTERNAL_MAX_DATA_LENGTH() | Internal use only |
| INTERNAL_TABLE_ROWS()      | Internal use only |
| INTERNAL_UPDATE_TIME()     | Internal use only |

The functions listed in this section are intended only for internal use by the server. Attempts by users to invoke them result in an error.

- <span id="page-22-0"></span>• [CAN\\_ACCESS\\_COLUMN\(](#page-22-0)ARGS)
- <span id="page-22-1"></span>• [CAN\\_ACCESS\\_DATABASE\(](#page-22-1)ARGS)
- <span id="page-22-2"></span>• [CAN\\_ACCESS\\_TABLE\(](#page-22-2)ARGS)
- <span id="page-22-3"></span>• [CAN\\_ACCESS\\_USER\(](#page-22-3)ARGS)
- <span id="page-22-4"></span>• [CAN\\_ACCESS\\_VIEW\(](#page-22-4)ARGS)
- <span id="page-22-5"></span>• [GET\\_DD\\_COLUMN\\_PRIVILEGES\(](#page-22-5)ARGS)
- <span id="page-22-6"></span>• [GET\\_DD\\_CREATE\\_OPTIONS\(](#page-22-6)ARGS)
- <span id="page-22-7"></span>• [GET\\_DD\\_INDEX\\_SUB\\_PART\\_LENGTH\(](#page-22-7)ARGS)
- <span id="page-22-8"></span>• [INTERNAL\\_AUTO\\_INCREMENT\(](#page-22-8)ARGS)
- <span id="page-22-9"></span>• [INTERNAL\\_AVG\\_ROW\\_LENGTH\(](#page-22-9)ARGS)
- <span id="page-22-10"></span>• [INTERNAL\\_CHECK\\_TIME\(](#page-22-10)ARGS)
- <span id="page-22-11"></span>• [INTERNAL\\_CHECKSUM\(](#page-22-11)ARGS)
- <span id="page-22-12"></span>• [INTERNAL\\_DATA\\_FREE\(](#page-22-12)ARGS)
- <span id="page-22-13"></span>• [INTERNAL\\_DATA\\_LENGTH\(](#page-22-13)ARGS)
- <span id="page-22-14"></span>• [INTERNAL\\_DD\\_CHAR\\_LENGTH\(](#page-22-14)ARGS)
- <span id="page-22-15"></span>• [INTERNAL\\_GET\\_COMMENT\\_OR\\_ERROR\(](#page-22-15)ARGS)
- <span id="page-22-16"></span>• [INTERNAL\\_GET\\_ENABLED\\_ROLE\\_JSON\(](#page-22-16)ARGS)
- <span id="page-22-17"></span>• [INTERNAL\\_GET\\_HOSTNAME\(](#page-22-17)ARGS)
- <span id="page-22-18"></span>• [INTERNAL\\_GET\\_USERNAME\(](#page-22-18)ARGS)
- <span id="page-22-19"></span>• [INTERNAL\\_GET\\_VIEW\\_WARNING\\_OR\\_ERROR\(](#page-22-19)ARGS)
- <span id="page-22-20"></span>• [INTERNAL\\_INDEX\\_COLUMN\\_CARDINALITY\(](#page-22-20)ARGS)
- <span id="page-22-21"></span>• [INTERNAL\\_INDEX\\_LENGTH\(](#page-22-21)ARGS)
- <span id="page-22-22"></span>• [INTERNAL\\_IS\\_ENABLED\\_ROLE\(](#page-22-22)ARGS)
- <span id="page-22-23"></span>• [INTERNAL\\_IS\\_MANDATORY\\_ROLE\(](#page-22-23)ARGS)
- <span id="page-22-24"></span>• [INTERNAL\\_KEYS\\_DISABLED\(](#page-22-24)ARGS)
- <span id="page-22-25"></span>• [INTERNAL\\_MAX\\_DATA\\_LENGTH\(](#page-22-25)ARGS)
- <span id="page-22-26"></span>• [INTERNAL\\_TABLE\\_ROWS\(](#page-22-26)ARGS)
- <span id="page-22-27"></span>• [INTERNAL\\_UPDATE\\_TIME\(](#page-22-27)ARGS)
- <span id="page-22-28"></span>• [IS\\_VISIBLE\\_DD\\_OBJECT\(](#page-22-28)ARGS)