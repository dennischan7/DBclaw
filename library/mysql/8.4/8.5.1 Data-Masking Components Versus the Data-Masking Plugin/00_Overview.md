---
source: MySQL 8.4 Reference
title: 00_Overview
---

Previously, MySQL enabled masking and de-identification capabilities using a server-side plugin, but transitioned to use the component infrastructure as an alternative implementation. The following table briefly compares MySQL Enterprise Data Masking and De-Identification components and the plugin library to provide an overview of their differences. It may assist you in making the transition from the plugin to components.

![](_page_180_Picture_3.jpeg)

#### **Note**

Only the data-masking components or the plugin should be enabled at a time. Enabling both components and the plugin is unsupported and results may not be as anticipated.

**Table 8.45 Comparison Between Data-Masking Components and Plugin Elements**

<span id="page-180-0"></span>

| Category                                                                                       | Components                                                      | Plugin                        |
|------------------------------------------------------------------------------------------------|-----------------------------------------------------------------|-------------------------------|
| Interface                                                                                      | Service functions,<br>loadable functions                        | Loadable functions            |
| Support for multibyte character sets                                                           | Yes, for general<br>purpose masking<br>functions                | No                            |
| General-purpose masking functions                                                              | mask_inner(),<br>mask_outer()                                   | mask_inner(),<br>mask_outer() |
| Masking of specific types                                                                      | PAN, SSN, IBAN, UUID,<br>Canada SIN, UK NIN                     | PAN, SSN                      |
| Random generation, specific types                                                              | email, US phone, PAN,<br>SSN, IBAN, UUID,<br>Canada SIN, UK NIN | email, US phone, PAN,<br>SSN  |
| Random generation of integer from given range                                                  | Yes                                                             | Yes                           |
| Persisting substitution dictionaries                                                           | Database                                                        | File                          |
| Privilege to manage dictionaries                                                               | Dedicated privilege                                             | FILE                          |
| Automated loadable-function registration/<br>deregistration during installation/uninstallation | Yes                                                             | No                            |
| Enhancements to existing functions                                                             | More arguments<br>added to the<br>gen_rnd_email()<br>function   | N/A                           |