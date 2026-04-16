---
source: MySQL 8.4 Reference
title: 00_Overview
---

ENUM and SET columns provide an efficient way to define columns that can contain only a given set of values. See Section 13.3.5, "The ENUM Type", and Section 13.3.6, "The SET Type".

Unless strict mode is disabled (not recommended, but see Section 7.1.11, "Server SQL Modes"), the definition of a ENUM or SET column acts as a constraint on values entered into the column. An error occurs for values that do not satisfy these conditions:

- An ENUM value must be one of those listed in the column definition, or the internal numeric equivalent thereof. The value cannot be the error value (that is, 0 or the empty string). For a column defined as ENUM('a','b','c'), values such as '', 'd', or 'ax' are invalid and are rejected.
- A SET value must be the empty string or a value consisting only of the values listed in the column definition separated by commas. For a column defined as SET('a','b','c'), values such as 'd' or 'a,b,c,d' are invalid and are rejected.

Errors for invalid values can be suppressed in strict mode if you use INSERT IGNORE or UPDATE IGNORE. In this case, a warning is generated rather than an error. For ENUM, the value is inserted as the error member (0). For SET, the value is inserted as given except that any invalid substrings are deleted. For example, 'a,x,b,y' results in a value of 'a,b'.

# <span id="page-84-0"></span>Chapter 2 Installing MySQL

# **Table of Contents**

| 2.1 General Installation Guidance 57                                      |     |
|---------------------------------------------------------------------------|-----|
| 2.1.1 Supported Platforms 57                                              |     |
| 2.1.2 Which MySQL Version and Distribution to Install 57                  |     |
| 2.1.3 How to Get MySQL 58                                                 |     |
| 2.1.4 Verifying Package Integrity Using MD5 Checksums or GnuPG 59         |     |
| 2.1.5 Installation Layouts 74                                             |     |
| 2.1.6 Compiler-Specific Build Characteristics 75                          |     |
| 2.2 Installing MySQL on Unix/Linux Using Generic Binaries 75              |     |
| 2.3 Installing MySQL on Microsoft Windows 78                              |     |
| 2.3.1 Choosing an Installation Package 81                                 |     |
| 2.3.2 Configuration: Using MySQL Configurator                             | 82  |
| 2.3.3 Configuration: Manually 100                                         |     |
| 2.3.4 Troubleshooting a Microsoft Windows MySQL Server Installation 108   |     |
| 2.3.5 Windows Postinstallation Procedures                                 | 109 |
| 2.3.6 Windows Platform Restrictions 111                                   |     |
| 2.4 Installing MySQL on macOS 113                                         |     |
| 2.4.1 General Notes on Installing MySQL on macOS 113                      |     |
| 2.4.2 Installing MySQL on macOS Using Native Packages 114                 |     |
| 2.4.3 Installing and Using the MySQL Launch Daemon 116                    |     |
| 2.4.4 Installing and Using the MySQL Preference Pane 119                  |     |
| 2.5 Installing MySQL on Linux 123                                         |     |
| 2.5.1 Installing MySQL on Linux Using the MySQL Yum Repository 124        |     |
| 2.5.2 Installing MySQL on Linux Using the MySQL APT Repository 129        |     |
| 2.5.3 Using the MySQL SLES Repository 138                                 |     |
| 2.5.4 Installing MySQL on Linux Using RPM Packages from Oracle 143        |     |
| 2.5.5 Installing MySQL on Linux Using Debian Packages from Oracle         | 148 |
| 2.5.6 Deploying MySQL on Linux with Docker Containers 149                 |     |
| 2.5.7 Installing MySQL on Linux from the Native Software Repositories 161 |     |
| 2.5.8 Installing MySQL on Linux with Juju 163                             |     |
| 2.5.9 Managing MySQL Server with systemd 163                              |     |
| 2.6 Installing MySQL Using Unbreakable Linux Network (ULN) 168            |     |
| 2.7 Installing MySQL on Solaris 169                                       |     |
| 2.7.1 Installing MySQL on Solaris Using a Solaris PKG 169                 |     |
| 2.8 Installing MySQL from Source 170                                      |     |
| 2.8.1 Source Installation Methods 171                                     |     |
| 2.8.2 Source Installation Prerequisites 171                               |     |
| 2.8.3 MySQL Layout for Source Installation 173                            |     |
| 2.8.4 Installing MySQL Using a Standard Source Distribution 173           |     |
| 2.8.5 Installing MySQL Using a Development Source Tree 177                |     |
| 2.8.6 Configuring SSL Library Support 178                                 |     |
| 2.8.7 MySQL Source-Configuration Options 179                              |     |
| 2.8.8 Dealing with Problems Compiling MySQL 204                           |     |
| 2.8.9 MySQL Configuration and Third-Party Tools 205                       |     |
| 2.8.10 Generating MySQL Doxygen Documentation Content 205                 |     |
| 2.9 Postinstallation Setup and Testing 206                                |     |
| 2.9.1 Initializing the Data Directory                                     | 207 |
| 2.9.2 Starting the Server 212                                             |     |
| 2.9.3 Testing the Server 215                                              |     |
| 2.9.4 Securing the Initial MySQL Account 216                              |     |
| 2.9.5 Starting and Stopping MySQL Automatically 218                       |     |
| 2.10 Perl Installation Notes 219                                          |     |
| 2.10.1 Installing Perl on Unix 220                                        |     |
|                                                                           |     |

| 2.10.2 Installing ActiveState Perl on Windows 220    |  |
|------------------------------------------------------|--|
| 2.10.3 Problems Using the Perl DBI/DBD Interface 221 |  |

This chapter describes how to obtain and install MySQL. A summary of the procedure follows and later sections provide the details. If you plan to upgrade an existing version of MySQL to a newer version rather than install MySQL for the first time, see Chapter 3, Upgrading MySQL, for information about upgrade procedures and about issues that you should consider before upgrading.

If you are interested in migrating to MySQL from another database system, see Section A.8, "MySQL 8.4 FAQ: Migration", which contains answers to some common questions concerning migration issues.

Installation of MySQL generally follows the steps outlined here:

### 1. **Determine whether MySQL runs and is supported on your platform.**

Please note that not all platforms are equally suitable for running MySQL, and that not all platforms on which MySQL is known to run are officially supported by Oracle Corporation. For information about those platforms that are officially supported, see [https://www.mysql.com/support/](https://www.mysql.com/support/supportedplatforms/database.md) [supportedplatforms/database.html](https://www.mysql.com/support/supportedplatforms/database.md) on the MySQL website.

### 2. **Choose which track to install.**

MySQL offers an LTS series, such as MySQL 8.4, and an Innovation series. They address different use cases as described at [Section 1.3, "MySQL Releases: Innovation and LTS".](#page-38-0)

### 3. **Choose which distribution to install.**

Several versions of MySQL are available, and most are available in several distribution formats. You can choose from pre-packaged distributions containing binary (precompiled) programs or source code. When in doubt, use a binary distribution. Oracle also provides access to the MySQL source code for those who want to see recent developments and test new code. To determine which version and type of distribution you should use, see [Section 2.1.2, "Which MySQL Version](#page-86-2) [and Distribution to Install".](#page-86-2)

### 4. **Download the distribution that you want to install.**

For instructions, see [Section 2.1.3, "How to Get MySQL".](#page-87-0) To verify the integrity of the distribution, use the instructions in [Section 2.1.4, "Verifying Package Integrity Using MD5 Checksums or](#page-88-0) [GnuPG".](#page-88-0)

### 5. **Install the distribution.**

To install MySQL from a binary distribution, use the instructions in [Section 2.2, "Installing MySQL](#page-104-1) [on Unix/Linux Using Generic Binaries".](#page-104-1) Alternatively, use the [Secure Deployment Guide](https://dev.mysql.com/doc/mysql-secure-deployment-guide/en/), which provides procedures for deploying a generic binary distribution of MySQL Enterprise Edition Server with features for managing the security of your MySQL installation.

To install MySQL from a source distribution or from the current development source tree, use the instructions in [Section 2.8, "Installing MySQL from Source".](#page-199-0)

### 6. **Perform any necessary postinstallation setup.**

After installing MySQL, see Section 2.9, "Postinstallation Setup and Testing", for information about making sure the MySQL server is working properly. Also refer to the information provided in Section 2.9.4, "Securing the Initial MySQL Account". This section describes how to secure the initial MySQL root user account, which has no password until you assign one. The section applies whether you install MySQL using a binary or source distribution.

7. If you want to run the MySQL benchmark scripts, Perl support for MySQL must be available. See Section 2.10, "Perl Installation Notes".

Instructions for installing MySQL on different platforms and environments is available on a platform by platform basis:

### • **Unix, Linux**

For instructions on installing MySQL on most Linux and Unix platforms using a generic binary (for example, a .tar.gz package), see [Section 2.2, "Installing MySQL on Unix/Linux Using Generic](#page-104-1) [Binaries"](#page-104-1).

For information on building MySQL entirely from the source code distributions or the source code repositories, see [Section 2.8, "Installing MySQL from Source"](#page-199-0)

For specific platform help on installation, configuration, and building from source see the corresponding platform section:

- Linux, including notes on distribution specific methods, see [Section 2.5, "Installing MySQL on](#page-152-0) [Linux"](#page-152-0).
- IBM AIX, see [Section 2.7, "Installing MySQL on Solaris"](#page-198-0).

### • **Microsoft Windows**

For instructions on installing MySQL on Microsoft Windows, using either the MSI installer or Zipped binary, see [Section 2.3, "Installing MySQL on Microsoft Windows"](#page-107-0).

For details and instructions on building MySQL from source code, see [Section 2.8, "Installing MySQL](#page-199-0) [from Source".](#page-199-0)

### • **macOS**

For installation on macOS, including using both the binary package and native PKG formats, see [Section 2.4, "Installing MySQL on macOS".](#page-142-0)

For information on making use of an macOS Launch Daemon to automatically start and stop MySQL, see [Section 2.4.3, "Installing and Using the MySQL Launch Daemon".](#page-145-0)

For information on the MySQL Preference Pane, see [Section 2.4.4, "Installing and Using the MySQL](#page-148-0) [Preference Pane"](#page-148-0).

# <span id="page-86-0"></span>**2.1 General Installation Guidance**

The immediately following sections contain the information necessary to choose, download, and verify your distribution. The instructions in later sections of the chapter describe how to install the distribution that you choose. For binary distributions, see the instructions at [Section 2.2, "Installing MySQL on](#page-104-1) [Unix/Linux Using Generic Binaries"](#page-104-1) or the corresponding section for your platform if available. To build MySQL from source, use the instructions in [Section 2.8, "Installing MySQL from Source"](#page-199-0).

# <span id="page-86-1"></span>**2.1.1 Supported Platforms**

MySQL platform support evolves over time; please refer to [https://www.mysql.com/support/](https://www.mysql.com/support/supportedplatforms/database.md) [supportedplatforms/database.html](https://www.mysql.com/support/supportedplatforms/database.md) for the latest updates. To learn more about MySQL Support, see <https://www.mysql.com/support/>.

# <span id="page-86-2"></span>**2.1.2 Which MySQL Version and Distribution to Install**

When preparing to install MySQL, decide which version and distribution format (binary or source) to use.

First, decide whether to install from an LTS series like MySQL 8.4, or install from an Innovation series like MySQL 9.6. Both tracks include bug fixes while innovation releases includes the latest new features and changes. For additional details, see [Section 1.3, "MySQL Releases: Innovation and LTS".](#page-38-0) The naming scheme in MySQL 8.4 uses release names that consist of three numbers and an optional suffix (for example, **mysql-8.4.0**). The numbers within the release name are interpreted as follows:

- The first number (**8**) is the major version number.
- The second number (**4**) is the minor version number. The minor version number does not change for an LTS series, but it does change for an Innovation series.
- The third number (**0**) is the version number within an LTS series. This is incremented for each new LTS release, but is likely always 0 for innovation releases.

After choosing which MySQL version to install, decide which distribution format to install for your operating system. For most use cases, a binary distribution is the right choice. Binary distributions are available in native format for many platforms, such as RPM packages for Linux or DMG packages for macOS. Distributions are also available in more generic formats such as Zip archives or compressed tar files. On Windows, you might use an MSI to install a binary distribution.

Under some circumstances, it may be preferable to install MySQL from a source distribution:

- You want to install MySQL at some explicit location. The standard binary distributions are ready to run at any installation location, but you might require even more flexibility to place MySQL components where you want.
- You want to configure mysqld with features that might not be included in the standard binary distributions. Here is a list of the most common extra options used to ensure feature availability:
  - -DWITH\_LIBWRAP=1 for TCP wrappers support.
  - -DWITH\_ZLIB={system|bundled} for features that depend on compression
  - -DWITH\_DEBUG=1 for debugging support

For additional information, see Section 2.8.7, "MySQL Source-Configuration Options".

- You want to configure mysqld without some features that are included in the standard binary distributions.
- You want to read or modify the C and C++ code that makes up MySQL. For this purpose, obtain a source distribution.
- Source distributions contain more tests and examples than binary distributions.

# <span id="page-87-0"></span>**2.1.3 How to Get MySQL**

Check our downloads page at<https://dev.mysql.com/downloads/> for information about the current version of MySQL and for downloading instructions.

For RPM-based Linux platforms that use Yum as their package management system, MySQL can be installed using the [MySQL Yum Repository](https://dev.mysql.com/downloads/repo/yum/). See [Section 2.5.1, "Installing MySQL on Linux Using the](#page-153-0) [MySQL Yum Repository"](#page-153-0) for details.

For Debian-based Linux platforms, MySQL can be installed using the [MySQL APT Repository](https://dev.mysql.com/downloads/repo/apt/). See [Section 2.5.2, "Installing MySQL on Linux Using the MySQL APT Repository"](#page-158-0) for details.

For SUSE Linux Enterprise Server (SLES) platforms, MySQL can be installed using the [MySQL SLES](https://dev.mysql.com/downloads/repo/suse/) [Repository.](https://dev.mysql.com/downloads/repo/suse/) See [Section 2.5.3, "Using the MySQL SLES Repository"](#page-167-0) for details.

To obtain the latest development source, see Section 2.8.5, "Installing MySQL Using a Development Source Tree".

# <span id="page-88-0"></span>**2.1.4 Verifying Package Integrity Using MD5 Checksums or GnuPG**

After downloading the MySQL package that suits your needs and before attempting to install it, make sure that it is intact and has not been tampered with. There are three means of integrity checking:

- MD5 checksums
- Cryptographic signatures using GnuPG, the GNU Privacy Guard
- For RPM packages, the built-in RPM integrity verification mechanism

The following sections describe how to use these methods.

If you notice that the MD5 checksum or GPG signatures do not match, first try to download the respective package one more time, perhaps from another mirror site.

# <span id="page-88-1"></span>**2.1.4.1 Verifying the MD5 Checksum**

After you have downloaded a MySQL package, you should make sure that its MD5 checksum matches the one provided on the MySQL download pages. Each package has an individual checksum that you can verify against the package that you downloaded. The correct MD5 checksum is listed on the downloads page for each MySQL product; you should compare it against the MD5 checksum of the file (product) that you download.

Each operating system and setup offers its own version of tools for checking the MD5 checksum. Typically the command is named md5sum, or it may be named md5, and some operating systems do not ship it at all. On Linux, it is part of the **GNU Text Utilities** package, which is available for a wide range of platforms. You can also download the source code from<http://www.gnu.org/software/textutils/>. If you have OpenSSL installed, you can use the command openssl md5 package\_name instead. A Windows implementation of the md5 command line utility is available from [http://www.fourmilab.ch/](http://www.fourmilab.ch/md5/) [md5/](http://www.fourmilab.ch/md5/). winMd5Sum is a graphical MD5 checking tool that can be obtained from [http://www.nullriver.com/](http://www.nullriver.com/index/products/winmd5sum) [index/products/winmd5sum](http://www.nullriver.com/index/products/winmd5sum). Our Microsoft Windows examples assume the name md5.exe.

Linux and Microsoft Windows examples:

```
$> md5sum mysql-standard-8.4.8-linux-i686.tar.gz
aaab65abbec64d5e907dcd41b8699945 mysql-standard-8.4.8-linux-i686.tar.gz
$> md5.exe mysql-installer-community-8.4.8.msi
aaab65abbec64d5e907dcd41b8699945 mysql-installer-community-8.4.8.msi
```

You should verify that the resulting checksum (the string of hexadecimal digits) matches the one displayed on the download page immediately below the respective package.

![](_page_88_Picture_14.jpeg)

### **Note**

Make sure to verify the checksum of the archive file (for example, the .zip, .tar.gz, or .msi file) and not of the files that are contained inside of the archive. In other words, verify the file before extracting its contents.

# <span id="page-88-2"></span>**2.1.4.2 Signature Checking Using GnuPG**

Another method of verifying the integrity and authenticity of a package is to use cryptographic signatures. This is more reliable than using [MD5 checksums,](#page-88-1) but requires more work.

We sign MySQL downloadable packages with GnuPG (GNU Privacy Guard). GnuPG is an Open Source alternative to the well-known Pretty Good Privacy (PGP) by Phil Zimmermann. Most Linux distributions ship with GnuPG installed by default. Otherwise, see<http://www.gnupg.org/>for more information about GnuPG and how to obtain and install it.

To verify the signature for a specific package, you first need to obtain a copy of our public GPG build key, which you can download from [http://pgp.mit.edu/.](http://pgp.mit.edu/) The key that you want to obtain is named

mysql-build@oss.oracle.com. The keyID for MySQL 8.0.44 packages and higher, MySQL 8.4.7 and higher, and MySQL 9.5.0 and higher is B7B3B788A8D3785C. After obtaining this key, you should compare it with the key following value before using it verify MySQL packages. Alternatively, you can copy and paste the key directly from the text below.

![](_page_89_Picture_2.jpeg)

### **Note**

The public GPG build key for earlier MySQL release packages (keyID A8D3785C, 5072E1F5 or 3A79BD29), see [Section 2.1.4.5, "GPG Public Build](#page-93-0) [Key for Archived Packages".](#page-93-0)

-----BEGIN PGP PUBLIC KEY BLOCK---- mQINBGU2rNoBEACSi5t0nL6/Hj3d0PwsbdnbY+SqLUIZ3uWZQm6tsNhvTnahvPPZ BGdl99iWYTt2KmXp0KeN2s9pmLKkGAbacQP1RqzMFnoHawSMf0qTUVjAvhnI4+qz MDjTNSBq9fa3nHmOYxownnrRkpiQUM/yD7/JmVENgwWb6akZeGYrXch9jd4XV3t8 OD6TGzTedTki0TDNr6YZYhC7jUm9fK9Zs299pzOXSxRRNGd+3H9gbXizrBu4L/3l UrNf//rM7OvV9Ho7u9YYyAQ3L3+OABK9FKHNhrpi8Q0cbhvWkD4oCKJ+YZ54XrOG 0YTg/YUAs5/3//FATI1sWdtLjJ5pSb0onV3LIbarRTN8lC4Le/5kd3lcot9J8b3E MXL5p9OGW7wBfmNVRSUI74Vmwt+v9gyp0Hd0keRCUn8lo/1V0YD9i92KsE+/IqoY Tjnya/5kX41jB8vr1ebkHFuJ404+G6ETd0owwxq64jLIcsp/GBZHGU0RKKAo9DRL H7rpQ7PVlnw8TDNlOtWt5EJlBXFcPL+NgWbqkADAyA/XSNeWlqonvPlYfmasnAHA pMd9NhPQhC7hJTjCiAwG8UyWpV8Dj07DHFQ5xBbkTnKH2OrJtguPqSNYtTASbsWz 09S8ujoTDXFT17NbFM2dMIiq0a4VQB3SzH13H2io9Cbg/TzJrJGmwgoXgwARAQAB tDZNeVNRTCBSZWxlYXNlIEVuZ2luZWVyaW5nIDxteXNxbC1idWlsZEBvc3Mub3Jh Y2xlLmNvbT6JAlQEEwEIAD4CGwMFCwkIBwIGFQoJCAsCBBYCAwECHgECF4AWIQS8 pDQXw7SF3RKOxtS3s7eIqNN4XAUCaPoZowUJB4XTyQAKCRC3s7eIqNN4XAIED/9F 8cSgF+VHilpXe8gSTbVn5sNRnAsIYgMonsGqsrzUOv+3Gy4+e4guhRLe3m1PpQJq yIQ/upbGptP48YsIY8ix2pyzYr1dB8W1TcNUYcQvTdb8/Exd1nDpLzdwoil7b5W2 r3jpsor/b1cou7vju/ObBbkU5xai4waCMqO9llp3ePQTJBa1RwV01taryGZJa2xR Ke7k1lwdWINALICIQ0aSfy3Q24lWlj0CRiDxAE7UdbtBaqyr5omqUnOXR5kZdnOf jyAbsofMuQNSLTUg1hoSunp9llv/ayeaCu54qkmkqG8U5gKUDNnYhLTIto7uf2A8 6Ufr2/P1hiJ6MzvHKEI+xtvalKDm5M+/kwSXTnT4e2ERJ0eBnfxwfJlThcYCWOsy M1jyRaFqXYKxF+r/bfvXga/C+n7VbDEV9VdXfTEjDiSjoeLzaNkNNaDqrp5k4VSk ekeGluOhYdXOiBI2oSDAP2dvIcpQYuQIrU3TW2YHRLhrN57IaTeFYCA7ij6k8GdQ YL15Hub9SavhMQ1qwLTLRp0QeKTvw2y1cZ9yJD3rih3NZq0Ul3rZel7TfDG+TX6n 57mBk2z0zmNGuqLirQr6TUUM0Fvl26Zael5w4n5wRKsUdj3/GjchMGWLlu52s+0M KuB9nNowTIejuhT57x7H67Ho88eIZaWmFC9psvCHJLkCDQRlNqzaARAAsdvBo8WR qZ5WVVk6lReD8b6Zx83eJUkV254YX9zn5t8KDRjYOySwS75mJIaZLsv0YQjJk+5r t10tejyCrJIFo9CMvCmjUKtVbgmhfS5+fUDRrYCEZBBSa0Dvn68EBLiHugr+SPXF 6o1hXEUqdMCpB6oVp6X45JVQroCKIH5vsCtw2jU8S2/IjjV0V+E/zitGCiZaoZ1f 6NG7ozyFep1CSAReZu/sssk0pCLlfCebRd9Rz3QjSrQhWYuJa+eJmiF4oahnpUGk txMD632I9aG+IMfjtNJNtX32MbO+Se+cCtVc3cxSa/pR+89a3cb9IBA5tFF2Qoek hqo/1mmLi93Xn6uDUhl5tVxTnB217dBT27tw+p0hjd9hXZRQbrIZUTyh3+8EMfmA jNSIeR+th86xRd9XFRr9EOqrydnALOUr9cT7TfXWGEkFvn6ljQX7f4RvjJOTbc4j JgVFyu8K+VU6u1NnFJgDiNGsWvnYxAf7gDDbUSXEuC2anhWvxPvpLGmsspngge4y l+3nv+UqZ9sm6LCebR/7UZ67tYz3p6xzAOVgYsYcxoIUuEZXjHQtsYfTZZhrjUWB J09jrMvlKUHLnS437SLbgoXVYZmcqwAWpVNOLZf+fFm4IE5aGBG5Dho2CZ6ujngW 9Zkn98T1d4N0MEwwXa2V6T1ijzcqD7GApZUAEQEAAYkCPAQYAQgAJgIbDBYhBLyk NBfDtIXdEo7G1Lezt4io03hcBQJo+hmtBQkHhdPTAAoJELezt4io03hcOTAP/2Js Mj7a1xIeWN35+lvnsVE1t68hhipLUO0/Cj7pV8QsBUlIrs9u6cQ2Qzz5VGTHTd6Y hrX5xsPP8TUh50DWBx74IeFf8o5WxKlZ3eH0WnO0O96qNKW5BpQRsWNjF1kBWx6l nSyduMZRUTV4+2EeEciwXiBDPl5kHqW/Q7bGoV0YokwF1CC2igdCmHM+MY97Fpt8 cbzakl8kp2U4Z+fJ9oX467FF355pnEAxO0msZqjgyxolP/EcgIiqufzuRSYXk8te RsaC7elR+Bpi51CBgyl9EIEpoX/PfIBN3buEbb5zwMNL0PGw6b44oams6P5cMpbz GWikFGnDJyikVXlJuvaQdAQv7xMBvYU7HcLiYcM4Pt9uVGNEU321QIovFLhx/vH5 7Df+Fxx8FfHFP3MjVPzmldGHL67tUvquCTSxB/8fwEfA4b5abZwNy3E10DYhL4w5 PjzXl4/kbnVpZwtuyS5qMNg9n6cEWiSo15ldzV5iHTyprXx3RhO6krpJUFAcbCEw r2LmI2XYZguvGCSFm3LCuf4g7GDJ1u3RAtivCNCQ4sVgTLPoCNGW90Unf44s3vzm WDREXgkzSZthslxJHPE5y3Kh0qM1jQSuN+VNVHLGriOaOlYRtZoGGStONYhlBCoJ udMv77etKsN/mPdhJotVLMUpzeespcu5G2qqc5zt =6wRS -----END PGP PUBLIC KEY BLOCK-----

To import the build key into your personal public GPG keyring, use gpg --import. For example, if you have saved the key in a file named mysql\_pubkey.asc, the import command looks like this:

```
$> gpg --import mysql_pubkey.asc
gpg: key B7B3B788A8D3785C: public key "MySQL Release Engineering
<mysql-build@oss.oracle.com>" imported
```

```
gpg: Total number processed: 1
gpg: imported: 1
```

You can also download the key from the public keyserver using the public key id, A8D3785C:

```
$> gpg --recv-keys B7B3B788A8D3785C
gpg: requesting key B7B3B788A8D3785C from hkp server keys.gnupg.net
gpg: key B7B3B788A8D3785C: "MySQL Release Engineering <mysql-build@oss.oracle.com>"
1 new user ID
gpg: key B7B3B788A8D3785C: "MySQL Release Engineering <mysql-build@oss.oracle.com>"
53 new signatures
gpg: no ultimately trusted keys found
gpg: Total number processed: 1
gpg: new user IDs: 1
gpg: new signatures: 53
```

If you want to import the key into your RPM configuration to validate RPM install packages, you should be able to import the key directly:

```
$> rpm --import mysql_pubkey.asc
```

If you experience problems or require RPM specific information, see [Section 2.1.4.4, "Signature](#page-93-1) [Checking Using RPM"](#page-93-1).

After you have downloaded and imported the public build key, download your desired MySQL package and the corresponding signature, which also is available from the download page. The signature file has the same name as the distribution file with an .asc extension, as shown by the examples in the following table.

**Table 2.1 MySQL Package and Signature Files for Source files**

| File Type         | File Name                                         |
|-------------------|---------------------------------------------------|
| Distribution file | mysql-8.4.8-linux-glibc2.28-<br>x86_64.tar.xz     |
| Signature file    | mysql-8.4.8-linux-glibc2.28-<br>x86_64.tar.xz.asc |

Make sure that both files are stored in the same directory and then run the following command to verify the signature for the distribution file:

```
$> gpg --verify package_name.asc
```

If the downloaded package is valid, you should see a Good signature message similar to this:

```
$> gpg --verify mysql-8.4.8-linux-glibc2.28-x86_64.tar.xz.asc
gpg: Signature made Fri 15 Dec 2023 06:55:13 AM EST
gpg: using RSA key BCA43417C3B485DD128EC6D4B7B3B788A8D3785C
gpg: Good signature from "MySQL Release Engineering <mysql-build@oss.oracle.com>"
```

The Good signature message indicates that the file signature is valid, when compared to the signature listed on our site. But you might also see warnings, like so:

```
$> gpg --verify mysql-8.4.8-linux-glibc2.28-x86_64.tar.xz.asc
gpg: Signature made Fri 15 Dec 2023 06:55:13 AM EST
gpg: using RSA key BCA43417C3B485DD128EC6D4B7B3B788A8D3785C
gpg: Good signature from "MySQL Release Engineering <mysql-build@oss.oracle.com>"
gpg: WARNING: This key is not certified with a trusted signature!
gpg: There is no indication that the signature belongs to the owner.
Primary key fingerprint: BCA4 3417 C3B4 85DD 128E C6D4 B7B3 B788 A8D3 785C
```

That is normal, as they depend on your setup and configuration. Here are explanations for these warnings:

- gpg: no ultimately trusted keys found: This means that the specific key is not "ultimately trusted" by you or your web of trust, which is okay for the purposes of verifying file signatures.
- WARNING: This key is not certified with a trusted signature! There is no indication that the signature belongs to the owner.: This refers to your level of trust in your belief that you possess our real public key. This is a personal decision. Ideally, a MySQL developer would hand you the key in person, but more commonly, you downloaded it. Was the download tampered with? Probably not, but this decision is up to you. Setting up a web of trust is one method for trusting them.

See the GPG documentation for more information on how to work with public keys.