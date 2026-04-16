---
source: MySQL 8.4 Reference
title: 00_Overview
---

This section describes how to use the openssl command to set up the RSA key files that enable MySQL to support secure password exchange over unencrypted connections for accounts authenticated by the sha256\_password (deprecated) and caching\_sha2\_password plugins.

![](_page_89_Picture_7.jpeg)

#### **Note**

An easier alternative to generating the files required for SSL than the procedure described here is to let the server autogenerate them; see [Section 8.3.3.1,](#page-81-1) ["Creating SSL and RSA Certificates and Keys using MySQL"](#page-81-1).

To create the RSA private and public key-pair files, run these commands while logged into the system account used to run the MySQL server so that the files are owned by that account:

```
openssl genrsa -out private_key.pem 2048
openssl rsa -in private_key.pem -pubout -out public_key.pem
```

Those commands create 2,048-bit keys. To create stronger keys, use a larger value.

Then set the access modes for the key files. The private key should be readable only by the server, whereas the public key can be freely distributed to client users:

```
chmod 400 private_key.pem
chmod 444 public_key.pem
```

# <span id="page-89-0"></span>**8.3.4 Connecting to MySQL Remotely from Windows with SSH**

This section describes how to get an encrypted connection to a remote MySQL server with SSH. The information was provided by David Carlson <dcarlson@mplcomm.com>.

- 1. Install an SSH client on your Windows machine. For a comparison of SSH clients, see [http://](http://en.wikipedia.org/wiki/Comparison_of_SSH_clients) [en.wikipedia.org/wiki/Comparison\\_of\\_SSH\\_clients](http://en.wikipedia.org/wiki/Comparison_of_SSH_clients).
- 2. Start your Windows SSH client. Set Host\_Name = yourmysqlserver\_URL\_or\_IP. Set userid=your\_userid to log in to your server. This userid value might not be the same as the user name of your MySQL account.
- 3. Set up port forwarding. Either do a remote forward (Set local\_port: 3306, remote\_host: yourmysqlservername\_or\_ip, remote\_port: 3306 ) or a local forward (Set port: 3306, host: localhost, remote port: 3306).
- 4. Save everything, otherwise you must redo it the next time.
- 5. Log in to your server with the SSH session you just created.
- 6. On your Windows machine, start some ODBC application (such as Access).
- 7. Create a new file in Windows and link to MySQL using the ODBC driver the same way you normally do, except type in localhost for the MySQL host server, not yourmysqlservername.

At this point, you should have an ODBC connection to MySQL, encrypted using SSH.