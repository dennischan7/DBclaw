---
source: MySQL 8.0 Reference
title: 00_Overview
---

![](_page_172_Picture_20.jpeg)

#### **Note**

MySQL Enterprise Encryption is an extension included in MySQL Enterprise Edition, a commercial product. To learn more about commercial products, <https://www.mysql.com/products/>.

MySQL Enterprise Edition includes a set of encryption functions that expose OpenSSL capabilities at the SQL level. The functions enable Enterprise applications to perform the following operations:

• Implement added data protection using public-key asymmetric cryptography

- Create public and private keys and digital signatures
- Perform asymmetric encryption and decryption
- Use cryptographic hashing for digital signing and data verification and validation

In releases before MySQL 8.0.30, these functions are based on the openssl\_udf shared library. From MySQL 8.0.30, they are provided by a MySQL component component\_enterprise\_encryption.