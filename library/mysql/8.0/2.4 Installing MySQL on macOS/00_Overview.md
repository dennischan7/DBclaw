---
source: MySQL 8.0 Reference
title: 00_Overview
---

For a list of macOS versions that the MySQL server supports, see [https://www.mysql.com/support/](https://www.mysql.com/support/supportedplatforms/database.md) [supportedplatforms/database.html](https://www.mysql.com/support/supportedplatforms/database.md).

MySQL for macOS is available in a number of different forms:

- Native Package Installer, which uses the native macOS installer (DMG) to walk you through the installation of MySQL. For more information, see [Section 2.4.2, "Installing MySQL on macOS Using](#page-7-0) [Native Packages"](#page-7-0). You can use the package installer with macOS. The user you use to perform the installation must have administrator privileges.
- Compressed TAR archive, which uses a file packaged using the Unix tar and gzip commands. To use this method, you need to open a Terminal window. You do not need administrator privileges using this method; you can install the MySQL server anywhere using this method. For

more information on using this method, you can use the generic instructions for using a tarball, Section 2.2, "Installing MySQL on Unix/Linux Using Generic Binaries".

In addition to the core installation, the Package Installer also includes [Section 2.4.3, "Installing and](#page-11-0) [Using the MySQL Launch Daemon"](#page-11-0) and [Section 2.4.4, "Installing and Using the MySQL Preference](#page-15-0) [Pane"](#page-15-0) to simplify the management of your installation.

For additional information on using MySQL on macOS, see [Section 2.4.1, "General Notes on Installing](#page-6-0) [MySQL on macOS".](#page-6-0)

# <span id="page-6-0"></span>**2.4.1 General Notes on Installing MySQL on macOS**

You should keep the following issues and notes in mind:

• **Other MySQL installations**: The installation procedure does not recognize MySQL installations by package managers such as Homebrew. The installation and upgrade process is for MySQL packages provided by us. If other installations are present, then consider stopping them before executing this installer to avoid port conflicts.

**Homebrew**: For example, if you installed MySQL Server using Homebrew to its default location then the MySQL installer installs to a different location and won't upgrade the version from Homebrew. In this scenario you would end up with multiple MySQL installations that, by default, attempt to use the same ports. Stop the other MySQL Server instances before running this installer, such as executing brew services stop mysql to stop the Homebrew's MySQL service.

- **Launchd**: A launchd daemon is installed that alters MySQL configuration options. Consider editing it if needed, see the documentation below for additional information. Also, macOS 10.10 removed startup item support in favor of launchd daemons. The optional MySQL preference pane under macOS **System Preferences** uses the launchd daemon.
- **Users**: You may need (or want) to create a specific mysql user to own the MySQL directory and data. You can do this through the Directory Utility, and the mysql user should already exist. For use in single user mode, an entry for \_mysql (note the underscore prefix) should already exist within the system /etc/passwd file.
- **Data**: Because the MySQL package installer installs the MySQL contents into a version and platform specific directory, you can use this to upgrade and migrate your database between versions. You need either to copy the data directory from the old version to the new version, or to specify an alternative datadir value to set location of the data directory. By default, the MySQL directories are installed under /usr/local/.
- **Aliases**: You might want to add aliases to your shell's resource file to make it easier to access commonly used programs such as mysql and mysqladmin from the command line. The syntax for bash is:

```
alias mysql=/usr/local/mysql/bin/mysql
alias mysqladmin=/usr/local/mysql/bin/mysqladmin
```

For tcsh, use:

```
alias mysql /usr/local/mysql/bin/mysql
alias mysqladmin /usr/local/mysql/bin/mysqladmin
```

Even better, add /usr/local/mysql/bin to your PATH environment variable. You can do this by modifying the appropriate startup file for your shell. For more information, see [Section 6.2.1,](#page-193-0) ["Invoking MySQL Programs"](#page-193-0).

• **Removing**: After you have copied over the MySQL database files from the previous installation and have successfully started the new server, you should consider removing the old installation files to save disk space. Additionally, you should also remove older versions of the Package Receipt directories located in /Library/Receipts/mysql-VERSION.pkg.

# <span id="page-7-0"></span>**2.4.2 Installing MySQL on macOS Using Native Packages**

The package is located inside a disk image (.dmg) file that you first need to mount by double-clicking its icon in the Finder. It should then mount the image and display its contents.

![](_page_7_Picture_3.jpeg)

#### **Note**

Before proceeding with the installation, be sure to stop all running MySQL server instances by using either the MySQL Manager Application (on macOS Server), the preference pane, or mysqladmin shutdown on the command line.

To install MySQL using the package installer:

1. Download the disk image (.dmg) file (the community version is available [here\)](https://dev.mysql.com/downloads/mysql/) that contains the MySQL package installer. Double-click the file to mount the disk image and see its contents.

Double-click the MySQL installer package from the disk. It is named according to the version of MySQL you have downloaded. For example, for MySQL server 8.0.45 it might be named mysql-8.0.45-macos-10.13-x86\_64.pkg.

2. The initial wizard introduction screen references the MySQL server version to install. Click **Continue** to begin the installation.

The MySQL community edition shows a copy of the relevant GNU General Public License. Click **Continue** and then **Agree** to continue.

3. From the **Installation Type** page you can either click **Install** to execute the installation wizard using all defaults, click **Customize** to alter which components to install (MySQL server, MySQL Test, Preference Pane, Launchd Support -- all but MySQL Test are enabled by default).

![](_page_7_Picture_12.jpeg)

### **Note**

Although the **Change Install Location** option is visible, the installation location cannot be changed.

**Figure 2.13 MySQL Package Installer Wizard: Installation Type**

![](_page_8_Figure_2.jpeg)

**Figure 2.14 MySQL Package Installer Wizard: Customize**

![](_page_8_Figure_4.jpeg)

- 4. Click **Install** to install MySQL Server. The installation process ends here if upgrading a current MySQL Server installation, otherwise follow the wizard's additional configuration steps for your new MySQL Server installation.
- 5. After a successful new MySQL Server installation, complete the configuration steps by choosing the default encryption type for passwords, define the root password, and also enable (or disable) MySQL server at startup.
- 6. The default MySQL 8.0 password mechanism is caching\_sha2\_password (Strong), and this step allows you to change it to mysql\_native\_password (Legacy).

**Figure 2.15 MySQL Package Installer Wizard: Choose a Password Encryption Type**

![](_page_9_Picture_5.jpeg)

Choosing the legacy password mechanism alters the generated launchd file to set - default\_authentication\_plugin=mysql\_native\_password under ProgramArguments. Choosing strong password encryption does not set --default\_authentication\_plugin because the default MySQL Server value is used, which is caching\_sha2\_password.

7. Define a password for the root user, and also toggle whether MySQL Server should start after the configuration step is complete.

**Figure 2.16 MySQL Package Installer Wizard: Define Root Password**

![](_page_10_Picture_3.jpeg)

8. **Summary** is the final step and references a successful and complete MySQL Server installation. **Close** the wizard.

**Figure 2.17 MySQL Package Installer Wizard: Summary**

![](_page_10_Figure_6.jpeg)

MySQL server is now installed. If you chose to not start MySQL, then use either launchctl from the command line or start MySQL by clicking "Start" using the MySQL preference pane. For additional information, see [Section 2.4.3, "Installing and Using the MySQL Launch Daemon",](#page-11-0) and [Section 2.4.4,](#page-15-0) ["Installing and Using the MySQL Preference Pane".](#page-15-0) Use the MySQL Preference Pane or launchd to configure MySQL to automatically start at bootup.

When installing using the package installer, the files are installed into a directory within /usr/ local matching the name of the installation version and platform. For example, the installer file mysql-8.0.45-macos10.15-x86\_64.dmg installs MySQL into /usr/local/mysql-8.0.45 macos10.15-x86\_64/ with a symlink to /usr/local/mysql. The following table shows the layout of this MySQL installation directory.

![](_page_11_Picture_3.jpeg)

### **Note**

The macOS installation process does not create nor install a sample my.cnf MySQL configuration file.

**Table 2.7 MySQL Installation Layout on macOS**

| Directory       | Contents of Directory                                                                                                               |
|-----------------|-------------------------------------------------------------------------------------------------------------------------------------|
| bin             | mysqld server, client and utility programs                                                                                          |
| data            | Log files, databases, where /usr/local/<br>mysql/data/mysqld.local.err is the default<br>error log                                  |
| docs            | Helper documents, like the Release Notes and<br>build information                                                                   |
| include         | Include (header) files                                                                                                              |
| lib             | Libraries                                                                                                                           |
| man             | Unix manual pages                                                                                                                   |
| mysql-test      | MySQL test suite ('MySQL Test' is disabled by<br>default during the installation process when using<br>the installer package (DMG)) |
| share           | Miscellaneous support files, including error<br>messages, dictionary.txt, and rewriter SQL                                          |
| support-files   | Support scripts, such as<br>mysqld_multi.server, mysql.server, and<br>mysql-log-rotate.                                             |
| /tmp/mysql.sock | Location of the MySQL Unix socket                                                                                                   |

# <span id="page-11-0"></span>**2.4.3 Installing and Using the MySQL Launch Daemon**

macOS uses launch daemons to automatically start, stop, and manage processes and applications such as MySQL.

By default, the installation package (DMG) on macOS installs a launchd file named /Library/ LaunchDaemons/com.oracle.oss.mysql.mysqld.plist that contains a plist definition similar to:

```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
 <key>Label</key> <string>com.oracle.oss.mysql.mysqld</string>
 <key>ProcessType</key> <string>Interactive</string>
 <key>Disabled</key> <false/>
```

```
 <key>RunAtLoad</key> <true/>
 <key>KeepAlive</key> <true/>
 <key>SessionCreate</key> <true/>
 <key>LaunchOnlyOnce</key> <false/>
 <key>UserName</key> <string>_mysql</string>
 <key>GroupName</key> <string>_mysql</string>
 <key>ExitTimeOut</key> <integer>600</integer>
 <key>Program</key> <string>/usr/local/mysql/bin/mysqld</string>
 <key>ProgramArguments</key>
 <array>
 <string>/usr/local/mysql/bin/mysqld</string>
 <string>--user=_mysql</string>
 <string>--basedir=/usr/local/mysql</string>
 <string>--datadir=/usr/local/mysql/data</string>
 <string>--plugin-dir=/usr/local/mysql/lib/plugin</string>
 <string>--log-error=/usr/local/mysql/data/mysqld.local.err</string>
 <string>--pid-file=/usr/local/mysql/data/mysqld.local.pid</string>
 <string>--keyring-file-data=/usr/local/mysql/keyring/keyring</string>
 <string>--early-plugin-load=keyring_file=keyring_file.so</string>
 </array>
 <key>WorkingDirectory</key> <string>/usr/local/mysql</string>
</dict>
</plist>
```

![](_page_12_Picture_2.jpeg)

### **Note**

Some users report that adding a plist DOCTYPE declaration causes the launchd operation to fail, despite it passing the lint check. We suspect it's a copy-n-paste error. The md5 checksum of a file containing the above snippet is d925f05f6d1b6ee5ce5451b596d6baed.

To enable the launchd service, you can either:

• Open macOS system preferences and select the MySQL preference panel, and then execute **Start MySQL Server**.

**Figure 2.18 MySQL Preference Pane: Location**

The **Instances** page includes an option to start or stop MySQL, and **Initialize Database** recreates the data/ directory. **Uninstall** uninstalls MySQL Server and optionally the MySQL preference panel and launchd information.

**Figure 2.19 MySQL Preference Pane: Instances**

![](_page_14_Picture_2.jpeg)

• Or, manually load the launchd file.

```
$> cd /Library/LaunchDaemons
$> sudo launchctl load -F com.oracle.oss.mysql.mysqld.plist
```

• To configure MySQL to automatically start at bootup, you can:

```
$> sudo launchctl load -w com.oracle.oss.mysql.mysqld.plist
```

![](_page_14_Picture_7.jpeg)

### **Note**

When upgrading MySQL server, the launchd installation process removes the old startup items that were installed with MySQL server 5.7.7 and below.

Upgrading also replaces your existing launchd file named com.oracle.oss.mysql.mysqld.plist.

### Additional launchd related information:

- The plist entries override my.cnf entries, because they are passed in as command line arguments. For additional information about passing in program options, see [Section 6.2.2, "Specifying Program](#page-193-1) [Options".](#page-193-1)
- The **ProgramArguments** section defines the command line options that are passed into the program, which is the mysqld binary in this case.

- The default plist definition is written with less sophisticated use cases in mind. For more complicated setups, you may want to remove some of the arguments and instead rely on a MySQL configuration file, such as my.cnf.
- If you edit the plist file, then uncheck the installer option when reinstalling or upgrading MySQL. Otherwise, your edited plist file is overwritten, and all edits are lost.

Because the default plist definition defines several **ProgramArguments**, you might remove most of these arguments and instead rely upon your my.cnf MySQL configuration file to define them. For example:

```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
 <key>Label</key> <string>com.oracle.oss.mysql.mysqld</string>
 <key>ProcessType</key> <string>Interactive</string>
 <key>Disabled</key> <false/>
 <key>RunAtLoad</key> <true/>
 <key>KeepAlive</key> <true/>
 <key>SessionCreate</key> <true/>
 <key>LaunchOnlyOnce</key> <false/>
 <key>UserName</key> <string>_mysql</string>
 <key>GroupName</key> <string>_mysql</string>
 <key>ExitTimeOut</key> <integer>600</integer>
 <key>Program</key> <string>/usr/local/mysql/bin/mysqld</string>
 <key>ProgramArguments</key>
 <array>
 <string>/usr/local/mysql/bin/mysqld</string>
 <string>--user=_mysql</string>
 <string>--basedir=/usr/local/mysql</string>
 <string>--datadir=/usr/local/mysql/data</string>
 <string>--plugin-dir=/usr/local/mysql/lib/plugin</string>
 <string>--log-error=/usr/local/mysql/data/mysqld.local.err</string>
 <string>--pid-file=/usr/local/mysql/data/mysqld.local.pid</string>
 <string>--keyring-file-data=/usr/local/mysql/keyring/keyring</string>
 <string>--early-plugin-load=keyring_file=keyring_file.so</string>
 </array>
 <key>WorkingDirectory</key> <string>/usr/local/mysql</string>
</dict>
</plist>
```

In this case, the basedir, datadir, plugin\_dir, log\_error, pid\_file, keyring\_file\_data, and --early-plugin-load options were removed from the default plist ProgramArguments definition, which you might have defined in my.cnf instead.

# <span id="page-15-0"></span>**2.4.4 Installing and Using the MySQL Preference Pane**

The MySQL Installation Package includes a MySQL preference pane that enables you to start, stop, and control automated startup during boot of your MySQL installation.

This preference pane is installed by default, and is listed under your system's System Preferences window.

**Figure 2.20 MySQL Preference Pane: Location**

The MySQL preference pane is installed with the same DMG file that installs MySQL Server. Typically it is installed with MySQL Server but it can be installed by itself too.

To install the MySQL preference pane:

- 1. Go through the process of installing the MySQL server, as described in the documentation at [Section 2.4.2, "Installing MySQL on macOS Using Native Packages"](#page-7-0).
- 2. Click **Customize** at the **Installation Type** step. The "Preference Pane" option is listed there and enabled by default; make sure it is not deselected. The other options, such as MySQL Server, can be selected or deselected.

**Figure 2.21 MySQL Package Installer Wizard: Customize**

![](_page_17_Figure_2.jpeg)

3. Complete the installation process.

![](_page_17_Picture_4.jpeg)

#### **Note**

The MySQL preference pane only starts and stops MySQL installation installed from the MySQL package installation that have been installed in the default location.

Once the MySQL preference pane has been installed, you can control your MySQL server instance using this preference pane.

The **Instances** page includes an option to start or stop MySQL, and **Initialize Database** recreates the data/ directory. **Uninstall** uninstalls MySQL Server and optionally the MySQL preference panel and launchd information.

**Figure 2.22 MySQL Preference Pane: Instances**

![](_page_18_Figure_2.jpeg)

**Figure 2.23 MySQL Preference Pane: Initialize Database**

![](_page_19_Picture_2.jpeg)

The **Configuration** page shows MySQL Server options including the path to the MySQL configuration file.

**Figure 2.24 MySQL Preference Pane: Configuration**

![](_page_20_Picture_2.jpeg)

The MySQL Preference Pane shows the current status of the MySQL server, showing **stopped** (in red) if the server is not running and **running** (in green) if the server has already been started. The preference pane also shows the current setting for whether the MySQL server has been set to start automatically.

# <span id="page-20-0"></span>**2.5 Installing MySQL on Linux**

Linux supports a number of different solutions for installing MySQL. We recommend that you use one of the distributions from Oracle, for which several methods for installation are available:

**Table 2.8 Linux Installation Methods and Information**

| Type    | Setup Method                        | Additional Information |
|---------|-------------------------------------|------------------------|
| Apt     | Enable the MySQL Apt<br>repository  | Documentation          |
| Yum     | Enable the MySQL Yum<br>repository  | Documentation          |
| Zypper  | Enable the MySQL SLES<br>repository | Documentation          |
| RPM     | Download a specific package         | Documentation          |
| DEB     | Download a specific package         | Documentation          |
| Generic | Download a generic package          | Documentation          |

| Type                                | Setup Method                                                                                                     | Additional Information |
|-------------------------------------|------------------------------------------------------------------------------------------------------------------|------------------------|
| Source                              | Compile from source                                                                                              | Documentation          |
| Docker                              | Use the Oracle Container<br>Registry. You can also use My<br>Oracle Support for the MySQL<br>Enterprise Edition. | Documentation          |
| Oracle Unbreakable Linux<br>Network | Use ULN channels                                                                                                 | Documentation          |

As an alternative, you can use the package manager on your system to automatically download and install MySQL with packages from the native software repositories of your Linux distribution. These native packages are often several versions behind the currently available release. You are also normally unable to install innovation releases, since these are not usually made available in the native repositories. For more information on using the native package installers, see [Section 2.5.7, "Installing](#page-44-0) [MySQL on Linux from the Native Software Repositories"](#page-44-0).

![](_page_21_Picture_3.jpeg)

#### **Note**

For many Linux installations, you want to set up MySQL to be started automatically when your machine starts. Many of the native package installations perform this operation for you, but for source, binary and RPM solutions you may need to set this up separately. The required script, mysql.server, can be found in the support-files directory under the MySQL installation directory or in a MySQL source tree. You can install it as /etc/init.d/mysql for automatic MySQL startup and shutdown. See Section 6.3.3, "mysql.server — MySQL Server Startup Script".

## <span id="page-21-0"></span>**2.5.1 Installing MySQL on Linux Using the MySQL Yum Repository**

The [MySQL Yum repository](https://dev.mysql.com/downloads/repo/yum/) for Oracle Linux, Red Hat Enterprise Linux, CentOS, and Fedora provides RPM packages for installing the MySQL server, client, MySQL Workbench, MySQL Utilities, MySQL Router, MySQL Shell, Connector/ODBC, Connector/Python and so on (not all packages are available for all the distributions; see [Installing Additional MySQL Products and Components with Yum](#page-25-1) for details).

### **Before You Start**

As a popular, open-source software, MySQL, in its original or re-packaged form, is widely installed on many systems from various sources, including different software download sites, software repositories, and so on. The following instructions assume that MySQL is not already installed on your system using a third-party-distributed RPM package; if that is not the case, follow the instructions given in [Section 3.8, "Upgrading MySQL with the MySQL Yum Repository"](#page-143-0) or [Replacing a Third-Party](https://dev.mysql.com/doc/refman/5.7/en/replace-third-party-yum.md) [Distribution of MySQL Using the MySQL Yum Repository](https://dev.mysql.com/doc/refman/5.7/en/replace-third-party-yum.md).

![](_page_21_Picture_10.jpeg)

### **Important**

Repository setup RPM file names begin with mysql-84-lts-community to highlight the default active MySQL subrepository, which is MySQL 8.4 today. MySQL 8.0 must be manually enabled via your local repository configuration to install MySQL 8.0 instead of MySQL 8.4.

### **Steps for a Fresh Installation of MySQL**

Follow the steps below to install the latest GA version of MySQL with the MySQL Yum repository:

## <span id="page-21-1"></span>**Adding the MySQL Yum Repository** 1.

First, add the MySQL Yum repository to your system's repository list. This is a one-time operation, which can be performed by installing an RPM provided by MySQL. Follow these steps:

- a. Go to the Download MySQL Yum Repository page ([https://dev.mysql.com/downloads/repo/](https://dev.mysql.com/downloads/repo/yum/) [yum/\)](https://dev.mysql.com/downloads/repo/yum/) in the MySQL Developer Zone.
- b. Select and download the release package for your platform.
- c. Install the downloaded release package with the following command, replacing platformand-version-specific-package-name with the name of the downloaded RPM package:

```
$> sudo yum install platform-and-version-specific-package-name.rpm
```

For an EL6-based system, the command is in the form of (note the mysql80 prefix instead of mysql84 because EL6-based systems do not support MySQL 8.4):

```
$> sudo yum install mysql80-community-release-el6-{version-number}.noarch.rpm
```

For an EL7-based system:

```
$> sudo yum install mysql84-community-release-el7-{version-number}.noarch.rpm
```

Fpr EL8 or later, change el7 to the version number of your Enterprise Linux.

For Fedora 41 and 42:

```
$> sudo dnf install mysql84-community-release-fcnn-{rpm-version-number}.noarch.rpm
```

Replace nn with the Fedora version and {rpm-version-number} with the rpm's version number. For example, for:

```
mysql84-community-release-fc42-1.noarch.rpm
```

The installation command adds the MySQL Yum repository to your system's repository list and downloads the GnuPG key to check the integrity of the software packages. See Section 2.1.4.2, "Signature Checking Using GnuPG" for details on GnuPG key checking.

You can check that the MySQL Yum repository has been successfully added by the following command (for dnf-enabled systems, replace yum in the command with dnf):

```
$> yum repolist enabled | grep "mysql.*-community.*"
```

![](_page_22_Picture_17.jpeg)

#### **Note**

Once the MySQL Yum repository is enabled on your system, any systemwide update by the yum update command (or dnf upgrade for dnfenabled systems) upgrades MySQL packages on your system and replaces any native third-party packages, if Yum finds replacements for them in the MySQL Yum repository; see [Section 3.8, "Upgrading MySQL with the](#page-143-0) [MySQL Yum Repository",](#page-143-0) for a discussion on some possible effects of that on your system, see [Upgrading the Shared Client Libraries.](#page-145-0)

### <span id="page-22-0"></span>**Selecting a Release Series** 2.

When using the MySQL Yum repository, the latest LTS series (currently MySQL 8.4) is selected for installation by default. If you want to install MySQL 8.4 instead of 8.0 then skip this step.

Within the MySQL Yum repository, different release series of the MySQL Community Server are hosted in different subrepositories. The subrepository for the latest GA series (currently MySQL 8.4) is enabled by default, and the subrepositories for all other series (for example, the MySQL 8.0 series) are disabled by default. Use this command to see all the subrepositories in the MySQL Yum repository, and see which of them are enabled or disabled (for dnf-enabled systems, replace yum in the command with dnf):

```
$> yum repolist all | grep mysql
```

To install the latest release from the latest LTS series, no configuration is needed. To install the latest release from a specific series other than the latest LTS series, disable the subrepository for the latest LTS series and enable the subrepository for the specific series before running the installation command. If your platform supports yum-config-manager, you can do that by issuing these commands, which disable the subrepository for the 8.4 series and enable the one for the 8.0 series:

```
$> sudo yum-config-manager --disable mysql-8.4-lts-community
$> sudo yum-config-manager --disable mysql-tools-8.4-lts-community
$> sudo yum-config-manager --enable mysql80-community
$> sudo yum-config-manager --enable mysql-tools-community
```

For dnf-enabled platforms:

```
$> sudo dnf config-manager --disable mysql-8.4-lts-community
$> sudo dnf config-manager --disable mysql-tools-8.4-lts-community
$> sudo dnf config-manager --enable mysql80-community
$> sudo dnf config-manager --enable mysql-tools-community
```

Besides using yum-config-manager or the dnf config-manager command, you can also select a release series by editing manually the /etc/yum.repos.d/mysql-community.repo file. This is a typical entry for a MySQL 8.0 subrepository:

```
[mysql80-community]
name=MySQL 8.0 Community Server
baseurl=http://repo.mysql.com/yum/mysql-8.0-community/el/9/$basearch/
enabled=1
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-mysql-2023
```

Find the entry for the subrepository you want to configure, and edit the enabled option. Specify enabled=0 to disable a subrepository, or enabled=1 to enable a subrepository. For example, to install MySQL 8.0, make sure you have enabled=0 for the other MySQL series entries and enabled=1 for MySQL 8.0.

You should only enable subrepository for one release series at any time. When subrepositories for more than one release series are enabled, Yum uses the latest series.

Verify that the correct subrepositories have been enabled and disabled by running the following command and checking its output (for dnf-enabled systems, replace yum in the command with dnf):

```
$> yum repolist enabled | grep mysql
```

### **Disabling the Default MySQL Module** 3.

(EL8 systems only) EL8-based systems such as RHEL8 and Oracle Linux 8 include a MySQL module that is enabled by default. Unless this module is disabled, it masks packages provided by MySQL repositories. To disable the included module and make the MySQL repository packages visible, use the following command (for dnf-enabled systems, replace yum in the command with dnf):

```
$> sudo yum module disable mysql
```

## 4. **Installing MySQL**

Install MySQL by the following command (for dnf-enabled systems, replace yum in the command with dnf):

```
$> sudo yum install mysql-community-server
```

This installs the package for MySQL server (mysql-community-server) and also packages for the components required to run the server, including packages for the client (mysql-communityclient), the common error messages and character sets for client and server (mysqlcommunity-common), and the shared client libraries (mysql-community-libs).

## **Starting the MySQL Server** 5.

Start the MySQL server with the following command:

```
$> systemctl start mysqld
```

You can check the status of the MySQL server with the following command:

```
$> systemctl status mysqld
```

If the operating system is systemd enabled, standard systemctl (or alternatively, service with the arguments reversed) commands such as stop, start, status, and restart should be used to manage the MySQL server service. The mysqld service is enabled by default, and it starts at system reboot. See [Section 2.5.9, "Managing MySQL Server with systemd"](#page-47-0) for additional information.

At the initial start up of the server, the following happens, given that the data directory of the server is empty:

- The server is initialized.
- SSL certificate and key files are generated in the data directory.
- validate\_password is installed and enabled.
- A superuser account 'root'@'localhost is created. A password for the superuser is set and stored in the error log file. To reveal it, use the following command:

```
$> sudo grep 'temporary password' /var/log/mysqld.log
```

Change the root password as soon as possible by logging in with the generated, temporary password and set a custom password for the superuser account:

```
$> mysql -uroot -p
```

mysql> **ALTER USER 'root'@'localhost' IDENTIFIED BY 'MyNewPass4!';**

![](_page_24_Picture_20.jpeg)

### **Note**

validate\_password is installed by default. The default password policy implemented by validate\_password requires that passwords contain at least one uppercase letter, one lowercase letter, one digit, and one special character, and that the total password length is at least 8 characters.

For more information on the postinstallation procedures, see [Section 2.9, "Postinstallation Setup and](#page-94-1) [Testing"](#page-94-1).

![](_page_24_Picture_24.jpeg)

#### **Note**

Compatibility Information for EL7-based platforms: The following RPM packages from the native software repositories of the platforms are incompatible with the package from the MySQL Yum repository that installs the MySQL server. Once

you have installed MySQL using the MySQL Yum repository, you cannot install these packages (and vice versa).

• akonadi-mysql

## <span id="page-25-1"></span>**Installing Additional MySQL Products and Components with Yum**

You can use Yum to install and manage individual components of MySQL. Some of these components are hosted in sub-repositories of the MySQL Yum repository: for example, the MySQL Connectors are to be found in the MySQL Connectors Community sub-repository, and the MySQL Workbench in MySQL Tools Community. You can use the following command to list the packages for all the MySQL components available for your platform from the MySQL Yum repository (for dnf-enabled systems, replace yum in the command with dnf):

```
$> sudo yum --disablerepo=\* --enablerepo='mysql*-community*' list available
```

Install any packages of your choice with the following command, replacing package-name with name of the package (for dnf-enabled systems, replace yum in the command with dnf):

```
$> sudo yum install package-name
```

For example, to install MySQL Workbench on Fedora:

```
$> sudo dnf install mysql-workbench-community
```

To install the shared client libraries (for dnf-enabled systems, replace yum in the command with dnf):

```
$> sudo yum install mysql-community-libs
```

## **Platform Specific Notes**

ARM Support

ARM 64-bit (aarch64) is supported on Oracle Linux 7 and requires the Oracle Linux 7 Software Collections Repository (ol7\_software\_collections). For example, to install the server:

```
$> yum-config-manager --enable ol7_software_collections
$> yum install mysql-community-server
```

![](_page_25_Picture_16.jpeg)

## **Note**

ARM 64-bit (aarch64) is supported on Oracle Linux 7 as of MySQL 8.0.12.

![](_page_25_Picture_19.jpeg)

#### **Known Limitation**

The 8.0.12 release requires you to adjust the libstdc++7 path by executing ln -s /opt/oracle/oracle-armtoolset-1/root/usr/lib64 /usr/ lib64/gcc7 after executing the yum install step.

### **Updating MySQL with Yum**

Besides installation, you can also perform updates for MySQL products and components using the MySQL Yum repository. See [Section 3.8, "Upgrading MySQL with the MySQL Yum Repository"](#page-143-0) for details.

# <span id="page-25-0"></span>**2.5.2 Installing MySQL on Linux Using the MySQL APT Repository**

The MySQL APT repository provides deb packages for installing and managing the MySQL server, client, and other components on the current Debian and Ubuntu releases.

Instructions for using the MySQL APT Repository are available in [A Quick Guide to Using the MySQL](https://dev.mysql.com/doc/mysql-apt-repo-quick-guide/en/) [APT Repository](https://dev.mysql.com/doc/mysql-apt-repo-quick-guide/en/).

# <span id="page-26-0"></span>**2.5.3 Installing MySQL on Linux Using the MySQL SLES Repository**

The MySQL SLES repository provides RPM packages for installing and managing the MySQL server, client, and other components on SUSE Enterprise Linux Server.

Instructions for using the MySQL SLES repository are available in [A Quick Guide to Using the MySQL](https://dev.mysql.com/doc/mysql-sles-repo-quick-guide/en/) [SLES Repository](https://dev.mysql.com/doc/mysql-sles-repo-quick-guide/en/).

# <span id="page-26-1"></span>**2.5.4 Installing MySQL on Linux Using RPM Packages from Oracle**

The recommended way to install MySQL on RPM-based Linux distributions is by using the RPM packages provided by Oracle. There are two sources for obtaining them, for the Community Edition of MySQL:

- From the MySQL software repositories:
  - The MySQL Yum repository (see [Section 2.5.1, "Installing MySQL on Linux Using the MySQL Yum](#page-21-0) [Repository"](#page-21-0) for details).
  - The MySQL SLES repository (see [Section 2.5.3, "Installing MySQL on Linux Using the MySQL](#page-26-0) [SLES Repository"](#page-26-0) for details).
- From the [Download MySQL Community Server](https://dev.mysql.com/downloads/mysql/) page in the [MySQL Developer Zone](https://dev.mysql.com/).

![](_page_26_Picture_10.jpeg)

#### **Note**

RPM distributions of MySQL are also provided by other vendors. Be aware that they may differ from those built by Oracle in features, capabilities, and conventions (including communication setup), and that the installation instructions in this manual do not necessarily apply to them. The vendor's instructions should be consulted instead.

## **MySQL RPM Packages**

**Table 2.9 RPM Packages for MySQL Community Edition**

| Package Name                    | Summary                                                                                                                                      |
|---------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------|
| mysql-community-client          | MySQL client applications and tools                                                                                                          |
| mysql-community-client-plugins  | Shared plugins for MySQL client applications                                                                                                 |
| mysql-community-common          | Common files for server and client libraries                                                                                                 |
| mysql-community-devel           | Development header files and libraries for MySQL<br>database client applications                                                             |
| mysql-community-embedded-compat | MySQL server as an embedded library with<br>compatibility for applications using version 18 of<br>the library                                |
| mysql-community-icu-data-files  | MySQL packaging of ICU data files needed by<br>MySQL regular expressions                                                                     |
| mysql-community-libs            | Shared libraries for MySQL database client<br>applications                                                                                   |
| mysql-community-libs-compat     | Shared compatibility libraries for previous MySQL<br>installations; only present if previous MySQL<br>versions are supported by the platform |
| mysql-community-server          | Database server and related tools                                                                                                            |
| mysql-community-server-debug    | Debug server and plugin binaries                                                                                                             |
| mysql-community-test            | Test suite for the MySQL server                                                                                                              |

| Package Name                | Summary                                                                                                                                                                                                                         |
|-----------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| mysql-community             | The source code RPM looks similar to mysql<br>community-8.0.45-1.el7.src.rpm, depending on<br>selected OS                                                                                                                       |
| Additional *debuginfo* RPMs | There are several debuginfo packages: mysql<br>community-client-debuginfo, mysql-community<br>libs-debuginfo mysql-community-server-debug<br>debuginfo mysql-community-server-debuginfo,<br>and mysql-community-test-debuginfo. |

**Table 2.10 RPM Packages for the MySQL Enterprise Edition**

| Package Name                     | Summary                                                                                                                                                                                                                                                                          |
|----------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| mysql-commercial-backup          | MySQL Enterprise Backup (added in 8.0.11)                                                                                                                                                                                                                                        |
| mysql-commercial-client          | MySQL client applications and tools                                                                                                                                                                                                                                              |
| mysql-commercial-client-plugins  | Shared plugins for MySQL client applications                                                                                                                                                                                                                                     |
| mysql-commercial-common          | Common files for server and client libraries                                                                                                                                                                                                                                     |
| mysql-commercial-devel           | Development header files and libraries for MySQL<br>database client applications                                                                                                                                                                                                 |
| mysql-commercial-embedded-compat | MySQL server as an embedded library with<br>compatibility for applications using version 18 of<br>the library                                                                                                                                                                    |
| mysql-commercial-icu-data-files  | MySQL packaging of ICU data files needed by<br>MySQL regular expressions                                                                                                                                                                                                         |
| mysql-commercial-libs            | Shared libraries for MySQL database client<br>applications                                                                                                                                                                                                                       |
| mysql-commercial-libs-compat     | Shared compatibility libraries for previous MySQL<br>installations; only present if previous MySQL<br>versions are supported by the platform. The<br>version of the libraries matches the version of the<br>libraries installed by default by the distribution you<br>are using. |
| mysql-commercial-server          | Database server and related tools                                                                                                                                                                                                                                                |
| mysql-commercial-test            | Test suite for the MySQL server                                                                                                                                                                                                                                                  |
| Additional *debuginfo* RPMs      | There are several debuginfo packages: mysql<br>commercial-client-debuginfo, mysql-commercial<br>libs-debuginfo mysql-commercial-server-debug<br>debuginfo mysql-commercial-server-debuginfo,<br>and mysql-commercial-test-debuginfo.                                             |

The full names for the RPMs have the following syntax:

packagename-version-distribution-arch.rpm

The distribution and arch values indicate the Linux distribution and the processor type for which the package was built. See the table below for lists of the distribution identifiers:

**Table 2.11 MySQL Linux RPM Package Distribution Identifiers**

| Distribution Value                       | Intended Use                              |
|------------------------------------------|-------------------------------------------|
| el{version} where {version} is the major | EL6 (8.0), EL7, EL8, EL9, and EL10-based  |
| Enterprise Linux version, such as el8    | platforms (for example, the corresponding |

| Distribution Value                                                       | Intended Use                                                       |
|--------------------------------------------------------------------------|--------------------------------------------------------------------|
|                                                                          | versions of Oracle Linux, Red Hat Enterprise<br>Linux, and CentOS) |
| fc{version} where {version} is the major<br>Fedora version, such as fc37 | Fedora 41 and 42                                                   |
| sles12                                                                   | SUSE Linux Enterprise Server 12                                    |

To see all files in an RPM package (for example, mysql-community-server), use the following command:

```
$> rpm -qpl mysql-community-server-version-distribution-arch.rpm
```

The discussion in the rest of this section applies only to an installation process using the RPM packages directly downloaded from Oracle, instead of through a MySQL repository.

Dependency relationships exist among some of the packages. If you plan to install many of the packages, you may wish to download the RPM bundle tar file instead, which contains all the RPM packages listed above, so that you need not download them separately.

In most cases, you need to install the mysql-community-server, mysql-community-client, mysql-community-client-plugins, mysql-community-libs, mysql-community-icudata-files, mysql-community-common, and mysql-community-libs-compat packages to get a functional, standard MySQL installation. To perform such a standard, basic installation, go to the folder that contains all those packages (and, preferably, no other RPM packages with similar names), and issue the following command:

```
$> sudo yum install mysql-community-{server,client,client-plugins,icu-data-files,common,libs}-*
```

Replace yum with zypper for SLES, and with dnf for Fedora.

While it is much preferable to use a high-level package management tool like yum to install the packages, users who prefer direct rpm commands can replace the yum install command with the rpm -Uvh command; however, using rpm -Uvh instead makes the installation process more prone to failure, due to potential dependency issues the installation process might run into.

To install only the client programs, you can skip mysql-community-server in your list of packages to install; issue the following command:

```
$> sudo yum install mysql-community-{client,client-plugins,common,libs}-*
```

Replace yum with zypper for SLES, and with dnf for Fedora.

A standard installation of MySQL using the RPM packages result in files and resources created under the system directories, shown in the following table.

**Table 2.12 MySQL Installation Layout for Linux RPM Packages from the MySQL Developer Zone**

| Files or Resources          | Location                                                                   |
|-----------------------------|----------------------------------------------------------------------------|
| Client programs and scripts | /usr/bin                                                                   |
| mysqld server               | /usr/sbin                                                                  |
| Configuration file          | /etc/my.cnf                                                                |
| Data directory              | /var/lib/mysql                                                             |
| Error log file              | For RHEL, Oracle Linux, CentOS or Fedora<br>platforms: /var/log/mysqld.log |
|                             | For SLES: /var/log/mysql/mysqld.log                                        |

| Files or Resources                                                                    | Location                                                                                                 |  |
|---------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------|--|
| Value of secure_file_priv                                                             | /var/lib/mysql-files                                                                                     |  |
| System V init script                                                                  | For RHEL, Oracle Linux, CentOS or Fedora<br>platforms: /etc/init.d/mysqld<br>For SLES: /etc/init.d/mysql |  |
| Systemd service                                                                       | For RHEL, Oracle Linux, CentOS or Fedora<br>platforms: mysqld<br>For SLES: mysql                         |  |
| Pid file                                                                              | /var/run/mysql/mysqld.pid                                                                                |  |
| Socket                                                                                | /var/lib/mysql/mysql.sock                                                                                |  |
| Keyring directory                                                                     | /var/lib/mysql-keyring                                                                                   |  |
| Unix manual pages                                                                     | /usr/share/man                                                                                           |  |
| Include (header) files                                                                | /usr/include/mysql                                                                                       |  |
| Libraries                                                                             | /usr/lib/mysql                                                                                           |  |
| Miscellaneous support files (for example, error<br>messages, and character set files) | /usr/share/mysql                                                                                         |  |

The installation also creates a user named mysql and a group named mysql on the system.

![](_page_29_Picture_3.jpeg)

#### **Notes**

• The mysql user is created using the -r and -s /bin/false options of the useradd command, so that it does not have login permissions to your server host (see [Creating the mysql User and Group](https://dev.mysql.com/doc/mysql-secure-deployment-guide/8.0/en/secure-deployment-install.md#secure-deployment-mysql-user) for details). To switch to the mysql user on your OS, use the --shell=/bin/bash option for the su command:

```
su - mysql --shell=/bin/bash
```

• Installation of previous versions of MySQL using older packages might have created a configuration file named /usr/my.cnf. It is highly recommended that you examine the contents of the file and migrate the desired settings inside to the file /etc/my.cnf file, then remove /usr/my.cnf.

MySQL is NOT automatically started at the end of the installation process. For Red Hat Enterprise Linux, Oracle Linux, CentOS, and Fedora systems, use the following command to start MySQL:

```
$> systemctl start mysqld
```

For SLES systems, the command is the same, but the service name is different:

```
$> systemctl start mysql
```

If the operating system is systemd enabled, standard systemctl (or alternatively, service with the arguments reversed) commands such as stop, start, status, and restart should be used to manage the MySQL server service. The mysqld service is enabled by default, and it starts at system reboot. Notice that certain things might work differently on systemd platforms: for example, changing the location of the data directory might cause issues. See [Section 2.5.9, "Managing MySQL Server with](#page-47-0) [systemd"](#page-47-0) for additional information.

During an upgrade installation using RPM and DEB packages, if the MySQL server is running when the upgrade occurs then the MySQL server is stopped, the upgrade occurs, and the MySQL server is restarted. One exception: if the edition also changes during an upgrade (such as community to commercial, or vice-versa), then MySQL server is not restarted.

At the initial start up of the server, the following happens, given that the data directory of the server is empty:

- The server is initialized.
- An SSL certificate and key files are generated in the data directory.
- validate\_password is installed and enabled.
- A superuser account 'root'@'localhost' is created. A password for the superuser is set and stored in the error log file. To reveal it, use the following command for RHEL, Oracle Linux, CentOS, and Fedora systems:

```
$> sudo grep 'temporary password' /var/log/mysqld.log
```

Use the following command for SLES systems:

```
$> sudo grep 'temporary password' /var/log/mysql/mysqld.log
```

The next step is to log in with the generated, temporary password and set a custom password for the superuser account:

```
$> mysql -uroot -p
```

mysql> **ALTER USER 'root'@'localhost' IDENTIFIED BY 'MyNewPass4!';**

![](_page_30_Picture_12.jpeg)

#### **Note**

validate\_password is installed by default. The default password policy implemented by validate\_password requires that passwords contain at least one uppercase letter, one lowercase letter, one digit, and one special character, and that the total password length is at least 8 characters.

If something goes wrong during installation, you might find debug information in the error log file /var/ log/mysqld.log.

For some Linux distributions, it might be necessary to increase the limit on number of file descriptors available to mysqld. See Section B.3.2.16, "File Not Found and Similar Errors"

**Installing Client Libraries from Multiple MySQL Versions.** It is possible to install multiple client library versions, such as for the case that you want to maintain compatibility with older applications linked against previous libraries. To install an older client library, use the --oldpackage option with rpm. For example, to install mysql-community-libs-5.5 on an EL6 system that has libmysqlclient.21 from MySQL 8.0, use a command like this:

```
$> rpm --oldpackage -ivh mysql-community-libs-5.5.50-2.el6.x86_64.rpm
```

**Debug Package.** A special variant of MySQL Server compiled with the debug package has been included in the server RPM packages. It performs debugging and memory allocation checks and produces a trace file when the server is running. To use that debug version, start MySQL with / usr/sbin/mysqld-debug, instead of starting it as a service or with /usr/sbin/mysqld. See Section 7.9.4, "The DBUG Package" for the debug options you can use.

![](_page_30_Picture_20.jpeg)

### **Note**

The default plugin directory for debug builds changed from /usr/lib64/ mysql/plugin to /usr/lib64/mysql/plugin/debug in MySQL 8.0.4. Previously, it was necessary to change plugin\_dir to /usr/lib64/mysql/ plugin/debug for debug builds.

**Rebuilding RPMs from source SRPMs.** Source code SRPM packages for MySQL are available for download. They can be used as-is to rebuild the MySQL RPMs with the standard rpmbuild tool chain.

# <span id="page-31-0"></span>**2.5.5 Installing MySQL on Linux Using Debian Packages from Oracle**

Oracle provides Debian packages for installing MySQL on Debian or Debian-like Linux systems. The packages are available through two different channels:

- The [MySQL APT Repository](https://dev.mysql.com/downloads/repo/apt/). This is the preferred method for installing MySQL on Debian-like systems, as it provides a simple and convenient way to install and update MySQL products. For details, see [Section 2.5.2, "Installing MySQL on Linux Using the MySQL APT Repository"](#page-25-0).
- The [MySQL Developer Zone's Download Area](https://dev.mysql.com/downloads/). For details, see Section 2.1.3, "How to Get MySQL". The following are some information on the Debian packages available there and the instructions for installing them:
  - Various Debian packages are provided in the MySQL Developer Zone for installing different components of MySQL on the current Debian and Ubuntu platforms. The preferred method is to use the tarball bundle, which contains the packages needed for a basic setup of MySQL. The tarball bundles have names in the format of mysql-server\_MVER-DVER\_CPU.debbundle.tar. MVER is the MySQL version and DVER is the Linux distribution version. The CPU value indicates the processor type or family for which the package is built, as shown in the following table:

**Table 2.13 MySQL Debian and Ubuntu Installation Packages CPU Identifiers**

| CPU Value | Intended Processor Type or Family   |  |
|-----------|-------------------------------------|--|
| i386      | Pentium processor or better, 32 bit |  |
| amd64     | 64-bit x86 processor                |  |

• After downloading the tarball, unpack it with the following command:

\$> **tar -xvf mysql-server\_MVER-DVER\_CPU.deb-bundle.tar**

• You may need to install the libaio library if it is not already present on your system:

\$> **sudo apt-get install libaio1**

• Preconfigure the MySQL server package with the following command:

\$> **sudo dpkg-preconfigure mysql-community-server\_\*.deb**

You are asked to provide a password for the root user for your MySQL installation. You might also be asked other questions regarding the installation.

![](_page_31_Picture_15.jpeg)

### **Important**

Make sure you remember the root password you set. Users who want to set a password later can leave the **password** field blank in the dialogue box and just press **OK**; in that case, root access to the server is authenticated using the MySQL Socket Peer-Credential Authentication Plugin for connections using a Unix socket file. You can set the root password later using mysql\_secure\_installation.

• For a basic installation of the MySQL server, install the database common files package, the client package, the client metapackage, the server package, and the server metapackage (in that order); you can do that with a single command:

\$> **sudo dpkg -i mysql-{common,community-client-plugins,community-client-core,community-client,client,community-server-core,community-server,server}\_\*.deb**

There are also packages with server-core and client-core in the package names. These contain binaries only and are installed automatically by the standard packages. Installing them by themselves does not result in a functioning MySQL setup.

If you are being warned of unmet dependencies by dpkg (such as libmecab2), you can fix them using apt-get:

**sudo apt-get -f install**

Here are where the files are installed on the system:

- All configuration files (like my.cnf) are under /etc/mysql
- All binaries, libraries, headers, etc., are under /usr/bin and /usr/sbin
- The data directory is under /var/lib/mysql

![](_page_32_Picture_7.jpeg)

#### **Note**

Debian distributions of MySQL are also provided by other vendors. Be aware that they may differ from those built by Oracle in features, capabilities, and conventions (including communication setup), and that the instructions in this manual do not necessarily apply to installing them. The vendor's instructions should be consulted instead.

## <span id="page-32-0"></span>**2.5.6 Deploying MySQL on Linux with Docker Containers**

This section explains how to deploy MySQL Server using Docker containers.

While the docker client is used in the following instructions for demonstration purposes, in general, the MySQL container images provided by Oracle work with any container tools that are compliant with the [OCI 1.0 specification](https://opencontainers.org/posts/announcements/2021-05-04-oci-dist-spec-v1/).

![](_page_32_Picture_13.jpeg)

#### **Warning**

Before deploying MySQL with Docker containers, make sure you understand the security risks of running containers and mitigate them properly.

## <span id="page-32-1"></span>**2.5.6.1 Basic Steps for MySQL Server Deployment with Docker**

![](_page_32_Picture_17.jpeg)

### **Warning**

The MySQL Docker images maintained by the MySQL team are built specifically for Linux platforms. Other platforms are not supported, and users using these MySQL Docker images on them are doing so at their own risk. See [the discussion here](#page-44-1) for some known limitations for running these containers on non-Linux operating systems.

- [Downloading a MySQL Server Docker Image](#page-33-0)
- [Starting a MySQL Server Instance](#page-34-0)
- [Connecting to MySQL Server from within the Container](#page-35-0)
- [Container Shell Access](#page-35-1)
- [Stopping and Deleting a MySQL Container](#page-35-2)
- [Upgrading a MySQL Server Container](#page-36-0)
- [More Topics on Deploying MySQL Server with Docker](#page-37-0)

### <span id="page-33-0"></span>**Downloading a MySQL Server Docker Image**

![](_page_33_Picture_2.jpeg)

### **Important**

For users of MySQL Enterprise Edition: A subscription is required to use the Docker images for MySQL Enterprise Edition. Subscriptions work by a Bring Your Own License model; see [How to Buy MySQL Products and Services](https://www.mysql.com/buy-mysql/) for details.

Downloading the server image in a separate step is not strictly necessary; however, performing this step before you create your Docker container ensures your local image is up to date. To download the MySQL Community Edition image from the [Oracle Container Registry \(OCR\),](https://container-registry.oracle.com/) run this command:

```
docker pull container-registry.oracle.com/mysql/community-server:tag
```

The tag is the label for the image version you want to pull (for example, 5.7, 8.0, or latest). If **:tag** is omitted, the latest label is used, and the image for the latest GA version of MySQL Community Server is downloaded.

To download the MySQL Enterprise Edition image from the OCR, you need to first accept the license agreement on the OCR and log in to the container repository with your Docker client. Follow these steps:

- Visit the OCR at<https://container-registry.oracle.com/> and choose **MySQL**.
- Under the list of MySQL repositories, choose enterprise-server.
- If you have not signed in to the OCR yet, click the **Sign in** button on the right of the page, and then enter your Oracle account credentials when prompted to.
- Follow the instructions on the right of the page to accept the license agreement.
- Log in to the OCR with your container client using, for example, the docker login command:

```
# docker login container-registry.oracle.com 
Username: Oracle-Account-ID
Password: password
Login successful.
```

Download the Docker image for MySQL Enterprise Edition from the OCR with this command:

```
docker pull container-registry.oracle.com/mysql/enterprise-server:tag
```

To download the MySQL Enterprise Edition image from [My Oracle Support](https://support.oracle.com/) website, go onto the website, sign in to your Oracle account, and perform these steps once you are on the landing page:

- Select the **Patches and Updates** tab.
- Go to the **Patch Search** region and, on the **Search** tab, switch to the **Product or Family (Advanced)** subtab.
- Enter "MySQL Server" for the **Product** field, and the desired version number in the **Release** field.
- Use the dropdowns for additional filters to select **Description**—**contains**, and enter "Docker" in the text field.

The following figure shows the search settings for the MySQL Enterprise Edition image for MySQL Server 8.0:

![](_page_34_Figure_1.jpeg)

- Click the **Search** button and, from the result list, select the version you want, and click the **Download** button.
- In the **File Download** dialogue box that appears, click and download the .zip file for the Docker image.

Unzip the downloaded .zip archive to obtain the tarball inside (mysql-enterpriseserver-version.tar), and then load the image by running this command:

```
docker load -i mysql-enterprise-server-version.tar
```

You can list downloaded Docker images with this command:

```
$> docker images
REPOSITORY TAG IMAGE ID CREATED SIZE
container-registry.oracle.com/mysql/community-server latest 1d9c2219ff69 2 months ago 496MB
```

### <span id="page-34-0"></span>**Starting a MySQL Server Instance**

To start a new Docker container for a MySQL Server, use the following command:

```
docker run --name=container_name --restart on-failure -d image_name:tag
```

image\_name is the name of the image to be used to start the container; see [Downloading a MySQL](#page-33-0) [Server Docker Image](#page-33-0) for more information.

The --name option, for supplying a custom name for your server container, is optional; if no container name is supplied, a random one is generated.

The --restart option is for configuring the [restart policy](https://docs.docker.com/config/containers/start-containers-automatically/) for your container; it should be set to the value on-failure, to enable support for server restart within a client session (which happens, for example, when the RESTART statement is executed by a client or during the [configuration of an](https://dev.mysql.com/doc/mysql-shell/8.0/en/configuring-production-instances.md#configuring-local-instances) [InnoDB cluster instance\)](https://dev.mysql.com/doc/mysql-shell/8.0/en/configuring-production-instances.md#configuring-local-instances). With the support for restart enabled, issuing a restart within a client session causes the server and the container to stop and then restart. Support for server restart is available for MySQL 8.0.21 and later.

For example, to start a new Docker container for the MySQL Community Server, use this command:

```
docker run --name=mysql1 --restart on-failure -d container-registry.oracle.com/mysql/community-server:latest
```

To start a new Docker container for the MySQL Enterprise Server with a Docker image downloaded from the OCR, use this command:

```
docker run --name=mysql1 --restart on-failure -d container-registry.oracle.com/mysql/enterprise-server:latest
```

To start a new Docker container for the MySQL Enterprise Server with a Docker image downloaded from My Oracle Support, use this command:

```
docker run --name=mysql1 --restart on-failure -d mysql/enterprise-server:latest
```

If the Docker image of the specified name and tag has not been downloaded by an earlier docker pull or docker run command, the image is now downloaded. Initialization for the container begins, and the container appears in the list of running containers when you run the docker ps command. For example:

```
$> docker ps
CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES
4cd4129b3211 container-registry.oracle.com/mysql/community-server:latest "/entrypoint.sh mysq…" 8 seconds ago Up 7 seconds (health: starting) 3306/tcp, 33060-33061/tcp mysql1
```

The container initialization might take some time. When the server is ready for use, the STATUS of the container in the output of the docker ps command changes from (health: starting) to (healthy).

The -d option used in the docker run command above makes the container run in the background. Use this command to monitor the output from the container:

```
docker logs mysql1
```

Once initialization is finished, the command's output is going to contain the random password generated for the root user; check the password with, for example, this command:

```
$> docker logs mysql1 2>&1 | grep GENERATED
GENERATED ROOT PASSWORD: Axegh3kAJyDLaRuBemecis&EShOs
```

### <span id="page-35-0"></span>**Connecting to MySQL Server from within the Container**

Once the server is ready, you can run the mysql client within the MySQL Server container you just started, and connect it to the MySQL Server. Use the docker exec -it command to start a mysql client inside the Docker container you have started, like the following:

```
docker exec -it mysql1 mysql -uroot -p
```

When asked, enter the generated root password (see the last step in [Starting a MySQL Server](#page-34-0) [Instance](#page-34-0) above on how to find the password). Because the [MYSQL\\_ONETIME\\_PASSWORD](#page-43-0) option is true by default, after you have connected a mysql client to the server, you must reset the server root password by issuing this statement:

```
mysql> ALTER USER 'root'@'localhost' IDENTIFIED BY 'password';
```

Substitute password with the password of your choice. Once the password is reset, the server is ready for use.

## <span id="page-35-1"></span>**Container Shell Access**

To have shell access to your MySQL Server container, use the docker exec -it command to start a bash shell inside the container:

```
$> docker exec -it mysql1 bash
bash-4.2#
```

You can then run Linux commands inside the container. For example, to view contents in the server's data directory inside the container, use this command:

```
bash-4.2# ls /var/lib/mysql
auto.cnf ca.pem client-key.pem ib_logfile0 ibdata1 mysql mysql.sock.lock private_key.pem server-cert.pem sys
ca-key.pem client-cert.pem ib_buffer_pool ib_logfile1 ibtmp1 mysql.sock performance_schema public_key.pem server-key.pem
```

### <span id="page-35-2"></span>**Stopping and Deleting a MySQL Container**

To stop the MySQL Server container we have created, use this command:

```
docker stop mysql1
```

docker stop sends a SIGTERM signal to the mysqld process, so that the server is shut down gracefully.

Also notice that when the main process of a container (mysqld in the case of a MySQL Server container) is stopped, the Docker container stops automatically.

To start the MySQL Server container again:

```
docker start mysql1
```

To stop and start again the MySQL Server container with a single command:

```
docker restart mysql1
```

To delete the MySQL container, stop it first, and then use the docker rm command:

```
docker stop mysql1
docker rm mysql1
```

If you want the [Docker volume for the server's data directory](#page-38-0) to be deleted at the same time, add the v option to the docker rm command.

## <span id="page-36-0"></span>**Upgrading a MySQL Server Container**

![](_page_36_Picture_8.jpeg)

#### **Important**

- Before performing any upgrade to MySQL, follow carefully the instructions in Chapter 3, [Upgrading MySQL](#page-110-0). Among other instructions discussed there, it is especially important to back up your database before the upgrade.
- The instructions in this section require that the server's data and configuration have been persisted on the host. See [Persisting Data and Configuration](#page-38-0) [Changes](#page-38-0) for details.

Follow these steps to upgrade a Docker installation of MySQL 5.7 to 8.0:

• Stop the MySQL 5.7 server (container name is mysql57 in this example):

```
docker stop mysql57
```

- Download the MySQL 8.0 Server Docker image. See instructions in [Downloading a MySQL Server](#page-33-0) [Docker Image](#page-33-0). Make sure you use the right tag for MySQL 8.0.
- Start a new MySQL 8.0 Docker container (named mysql80 in this example) with the old server data and configuration (with proper modifications if needed—see Chapter 3, [Upgrading MySQL](#page-110-0)) that have been persisted on the host (by [bind-mounting](https://docs.docker.com/engine/reference/commandline/service_create/#add-bind-mounts-or-volumes) in this example). For the MySQL Community Server, run this command:

```
docker run --name=mysql80 \
 --mount type=bind,src=/path-on-host-machine/my.cnf,dst=/etc/my.cnf \
 --mount type=bind,src=/path-on-host-machine/datadir,dst=/var/lib/mysql \
 -d container-registry.oracle.com/mysql/community-server:8.0
```

If needed, adjust container-registry.oracle.com/mysql/community-server to the correct image name—for example, replace it with container-registry.oracle.com/mysql/ enterprise-server for MySQL Enterprise Edition images downloaded from the OCR, or mysql/ enterprise-server for MySQL Enterprise Edition images downloaded from My Oracle Support.

• Wait for the server to finish startup. You can check the status of the server using the docker ps command (see [Starting a MySQL Server Instance](#page-34-0) for how to do that).

Follow the same steps for upgrading within the 8.0 series (that is, from release 8.0.x to 8.0.y): stop the original container, and start a new one with a newer image on the old server data and configuration. If you used the 8.0 or the latest tag when starting your original container and there is now a new MySQL 8.0 release you want to upgrade to it, you must first pull the image for the new release with the command:

```
docker pull container-registry.oracle.com/mysql/community-server:8.0
```

You can then upgrade by starting a new container with the same tag on the old data and configuration (adjust the image name if you are using the MySQL Enterprise Edition; see [Downloading a MySQL](#page-33-0) [Server Docker Image](#page-33-0)):

```
docker run --name=mysql80new \
 --mount type=bind,src=/path-on-host-machine/my.cnf,dst=/etc/my.cnf \
 --mount type=bind,src=/path-on-host-machine/datadir,dst=/var/lib/mysql \
 -d container-registry.oracle.com/mysql/community-server:8.0
```

![](_page_37_Picture_2.jpeg)

#### **Note**

For MySQL 8.0.15 and earlier: You need to complete the upgrade process by running the mysql\_upgrade utility in the MySQL 8.0 Server container (the step is not required for MySQL 8.0.16 and later):

```
• docker exec -it mysql80 mysql_upgrade -uroot -p
```

When prompted, enter the root password for your old server.

• Finish the upgrade by restarting the new container:

```
docker restart mysql80
```

### <span id="page-37-0"></span>**More Topics on Deploying MySQL Server with Docker**

For more topics on deploying MySQL Server with Docker like server configuration, persisting data and configuration, server error log, and container environment variables, see [Section 2.5.6.2, "More Topics](#page-37-1) [on Deploying MySQL Server with Docker"](#page-37-1).

### <span id="page-37-1"></span>**2.5.6.2 More Topics on Deploying MySQL Server with Docker**

![](_page_37_Picture_12.jpeg)

#### **Note**

Most of the following sample commands have containerregistry.oracle.com/mysql/community-server as the Docker image being used (like with the docker pull and docker run commands); change that if your image is from another repository—for example, replace it with container-registry.oracle.com/mysql/enterprise-server for MySQL Enterprise Edition images downloaded from the Oracle Container Registry (OCR), or mysql/enterprise-server for MySQL Enterprise Edition images downloaded from [My Oracle Support](https://support.oracle.com/).

- [The Optimized MySQL Installation for Docker](#page-37-2)
- [Configuring the MySQL Server](#page-38-1)
- [Persisting Data and Configuration Changes](#page-38-0)
- [Running Additional Initialization Scripts](#page-39-0)
- [Connect to MySQL from an Application in Another Docker Container](#page-39-1)
- [Server Error Log](#page-39-2)
- [Using MySQL Enterprise Backup with Docker](#page-40-0)
- [Using mysqldump with Docker](#page-42-0)
- [Known Issues](#page-43-1)
- [Docker Environment Variables](#page-43-2)

### <span id="page-37-2"></span>**The Optimized MySQL Installation for Docker**

Docker images for MySQL are optimized for code size, which means they only include crucial components that are expected to be relevant for the majority of users who run MySQL instances in Docker containers. A MySQL Docker installation is different from a common, non-Docker installation in the following aspects:

- Only a limited number of binaries are included.
- All binaries are stripped; they contain no debug information.

![](_page_38_Picture_4.jpeg)

#### **Warning**

Any software updates or installations users perform to the Docker container (including those for MySQL components) may conflict with the optimized MySQL installation created by the Docker image. Oracle does not provide support for MySQL products running in such an altered container, or a container created from an altered Docker image.

### <span id="page-38-1"></span>**Configuring the MySQL Server**

When you start the MySQL Docker container, you can pass configuration options to the server through the docker run command. For example:

```
docker run --name mysql1 -d container-registry.oracle.com/mysql/community-server:tag --character-set-server=utf8mb4 --collation-server=utf8mb4_col
```

The command starts the MySQL Server with utf8mb4 as the default character set and utf8mb4\_col as the default collation for databases.

Another way to configure the MySQL Server is to prepare a configuration file and mount it at the location of the server configuration file inside the container. See [Persisting Data and Configuration](#page-38-0) [Changes](#page-38-0) for details.

### <span id="page-38-0"></span>**Persisting Data and Configuration Changes**

Docker containers are in principle ephemeral, and any data or configuration are expected to be lost if the container is deleted or corrupted (see discussions [here\)](https://docs.docker.com/engine/userguide/eng-image/dockerfile_best-practices/). [Docker volumes](https://docs.docker.com/engine/admin/volumes/volumes/) provides a mechanism to persist data created inside a Docker container. At its initialization, the MySQL Server container creates a Docker volume for the server data directory. The JSON output from the docker inspect command on the container includes a Mount key, whose value provides information on the data directory volume:

```
$> docker inspect mysql1
...
 "Mounts": [
 {
 "Type": "volume",
 "Name": "4f2d463cfc4bdd4baebcb098c97d7da3337195ed2c6572bc0b89f7e845d27652",
 "Source": "/var/lib/docker/volumes/4f2d463cfc4bdd4baebcb098c97d7da3337195ed2c6572bc0b89f7e845d27652/_data",
 "Destination": "/var/lib/mysql",
 "Driver": "local",
 "Mode": "",
 "RW": true,
 "Propagation": ""
 }
 ],
...
```

The output shows that the source directory /var/lib/docker/ volumes/4f2d463cfc4bdd4baebcb098c97d7da3337195ed2c6572bc0b89f7e845d27652/ \_data, in which data is persisted on the host, has been mounted at /var/lib/mysql, the server data directory inside the container.

Another way to preserve data is to [bind-mount](https://docs.docker.com/engine/reference/commandline/service_create/#add-bind-mounts-volumes-or-memory-filesystems) a host directory using the --mount option when creating the container. The same technique can be used to persist the configuration of the server. The following command creates a MySQL Server container and bind-mounts both the data directory and the server configuration file:

```
docker run --name=mysql1 \
--mount type=bind,src=/path-on-host-machine/my.cnf,dst=/etc/my.cnf \
```

```
--mount type=bind,src=/path-on-host-machine/datadir,dst=/var/lib/mysql \
-d container-registry.oracle.com/mysql/community-server:tag
```

The command mounts path-on-host-machine/my.cnf at /etc/my.cnf (the server configuration file inside the container), and path-on-host-machine/datadir at /var/lib/mysql (the data directory inside the container). The following conditions must be met for the bind-mounting to work:

• The configuration file path-on-host-machine/my.cnf must already exist, and it must contain the specification for starting the server by the user mysql:

```
[mysqld]
user=mysql
```

You can also include other server configuration options in the file.

• The data directory path-on-host-machine/datadir must already exist. For server initialization to happen, the directory must be empty. You can also mount a directory prepopulated with data and start the server with it; however, you must make sure you start the Docker container with the same configuration as the server that created the data, and any host files or directories required are mounted when starting the container.

### <span id="page-39-0"></span>**Running Additional Initialization Scripts**

If there are any .sh or .sql scripts you want to run on the database immediately after it has been created, you can put them into a host directory and then mount the directory at /dockerentrypoint-initdb.d/ inside the container. For example:

```
docker run --name=mysql1 \
--mount type=bind,src=/path-on-host-machine/scripts/,dst=/docker-entrypoint-initdb.d/ \
-d container-registry.oracle.com/mysql/community-server:tag
```

### <span id="page-39-1"></span>**Connect to MySQL from an Application in Another Docker Container**

By setting up a Docker network, you can allow multiple Docker containers to communicate with each other, so that a client application in another Docker container can access the MySQL Server in the server container. First, create a Docker network:

```
docker network create my-custom-net
```

Then, when you are creating and starting the server and the client containers, use the --network option to put them on network you created. For example:

```
docker run --name=mysql1 --network=my-custom-net -d container-registry.oracle.com/mysql/community-server
```

```
docker run --name=myapp1 --network=my-custom-net -d myapp
```

The myapp1 container can then connect to the mysql1 container with the mysql1 hostname and vice versa, as Docker automatically sets up a DNS for the given container names. In the following example, we run the mysql client from inside the myapp1 container to connect to host mysql1 in its own container:

```
docker exec -it myapp1 mysql --host=mysql1 --user=myuser --password
```

For other networking techniques for containers, see the [Docker container networking](https://docs.docker.com/engine/userguide/networking/) section in the Docker Documentation.

### <span id="page-39-2"></span>**Server Error Log**

When the MySQL Server is first started with your server container, a server error log is NOT generated if either of the following conditions is true:

• A server configuration file from the host has been mounted, but the file does not contain the system variable log\_error (see [Persisting Data and Configuration Changes](#page-38-0) on bind-mounting a server configuration file).

• A server configuration file from the host has not been mounted, but the Docker environment variable [MYSQL\\_LOG\\_CONSOLE](#page-43-3) is true (which is the variable's default state for MySQL 8.0 server containers). The MySQL Server's error log is then redirected to stderr, so that the error log goes into the Docker container's log and is viewable using the docker logs mysqld-container command.

To make MySQL Server generate an error log when either of the two conditions is true, use the - log-error option to [configure the server](#page-38-1) to generate the error log at a specific location inside the container. To persist the error log, mount a host file at the location of the error log inside the container as explained in [Persisting Data and Configuration Changes.](#page-38-0) However, you must make sure your MySQL Server inside its container has write access to the mounted host file.

### <span id="page-40-0"></span>**Using MySQL Enterprise Backup with Docker**

[MySQL Enterprise Backup](https://dev.mysql.com/doc/mysql-enterprise-backup/8.0/en/) is a commercially-licensed backup utility for MySQL Server, available with [MySQL Enterprise Edition](https://www.mysql.com/products/enterprise/). MySQL Enterprise Backup is included in the Docker installation of MySQL Enterprise Edition.

In the following example, we assume that you already have a MySQL Server running in a Docker container (see [Section 2.5.6.1, "Basic Steps for MySQL Server Deployment with Docker"](#page-32-1) on how to start a MySQL Server instance with Docker). For MySQL Enterprise Backup to back up the MySQL Server, it must have access to the server's data directory. This can be achieved by, for example, [bind](#page-38-0)[mounting a host directory on the data directory of the MySQL Server](#page-38-0) when you start the server:

```
docker run --name=mysqlserver \
--mount type=bind,src=/path-on-host-machine/datadir/,dst=/var/lib/mysql \
-d mysql/enterprise-server:8.0
```

With this command, the MySQL Server is started with a Docker image of the MySQL Enterprise Edition, and the host directory /path-on-host-machine/datadir/ has been mounted onto the server's data directory (/var/lib/mysql) inside the server container. We also assume that, after the server has been started, the required privileges have also been set up for MySQL Enterprise Backup to access the server (see [Grant MySQL Privileges to Backup Administrator,](https://dev.mysql.com/doc/mysql-enterprise-backup/8.0/en/mysqlbackup.privileges.md) for details). Use the following steps to back up and restore a MySQL Server instance.

To back up a MySQL Server instance running in a Docker container using MySQL Enterprise Backup with Docker, follow the steps listed here:

1. On the same host where the MySQL Server container is running, start another container with an image of MySQL Enterprise Edition to perform a back up with the MySQL Enterprise Backup command [backup-to-image](https://dev.mysql.com/doc/mysql-enterprise-backup/8.0/en/backup-commands-backup.md#option_meb_backup-to-image). Provide access to the server's data directory using the bind mount we created in the last step. Also, mount a host directory (/path-on-host-machine/backups/ in this example) onto the storage folder for backups in the container (/data/backups in the example) to persist the backups we are creating. Here is a sample command for this step, in which MySQL Enterprise Backup is started with a Docker image downloaded from [My Oracle Support](https://support.oracle.com/):

```
$> docker run \
--mount type=bind,src=/path-on-host-machine/datadir/,dst=/var/lib/mysql \
--mount type=bind,src=/path-on-host-machine/backups/,dst=/data/backups \
--rm mysql/enterprise-server:8.0 \
mysqlbackup -umysqlbackup -ppassword --backup-dir=/tmp/backup-tmp --with-timestamp \
--backup-image=/data/backups/db.mbi backup-to-image
[Entrypoint] MySQL Docker Image 8.0.11-1.1.5
MySQL Enterprise Backup version 8.0.11 Linux-4.1.12-61.1.16.el7uek.x86_64-x86_64 [2018-04-08 07:06:45]
Copyright (c) 2003, 2018, Oracle and/or its affiliates. All Rights Reserved.
180921 17:27:25 MAIN INFO: A thread created with Id '140594390935680'
180921 17:27:25 MAIN INFO: Starting with following command line ...
...
-------------------------------------------------------------
 Parameters Summary
-------------------------------------------------------------
```

211

```
 Start LSN : 29615616
 End LSN : 29651854
-------------------------------------------------------------
mysqlbackup completed OK!
```

It is important to check the end of the output by mysqlbackup to make sure the backup has been completed successfully.

2. The container exits once the backup job is finished and, with the --rm option used to start it, it is removed after it exits. An image backup has been created, and can be found in the host directory mounted in the last step for storing backups, as shown here:

```
$> ls /tmp/backups
db.mbi
```

To restore a MySQL Server instance in a Docker container using MySQL Enterprise Backup with Docker, follow the steps listed here:

1. Stop the MySQL Server container, which also stops the MySQL Server running inside:

```
docker stop mysqlserver
```

2. On the host, delete all contents in the bind mount for the MySQL Server data directory:

```
rm -rf /path-on-host-machine/datadir/*
```

3. Start a container with an image of MySQL Enterprise Edition to perform the restore with the MySQL Enterprise Backup command [copy-back-and-apply-log](https://dev.mysql.com/doc/mysql-enterprise-backup/8.0/en/backup-commands-restore.md#option_meb_copy-back-and-apply-log). Bind-mount the server's data directory and the storage folder for the backups, like what we did when we backed up the server:

```
$> docker run \
--mount type=bind,src=/path-on-host-machine/datadir/,dst=/var/lib/mysql \
--mount type=bind,src=/path-on-host-machine/backups/,dst=/data/backups \
--rm mysql/enterprise-server:8.0 \
mysqlbackup --backup-dir=/tmp/backup-tmp --with-timestamp \
--datadir=/var/lib/mysql --backup-image=/data/backups/db.mbi copy-back-and-apply-log
[Entrypoint] MySQL Docker Image 8.0.11-1.1.5
MySQL Enterprise Backup version 8.0.11 Linux-4.1.12-61.1.16.el7uek.x86_64-x86_64 [2018-04-08 07:06:45]
Copyright (c) 2003, 2018, Oracle and/or its affiliates. All Rights Reserved.
180921 22:06:52 MAIN INFO: A thread created with Id '139768047519872'
180921 22:06:52 MAIN INFO: Starting with following command line ...
...
180921 22:06:52 PCR1 INFO: We were able to parse ibbackup_logfile up to
 lsn 29680612.
180921 22:06:52 PCR1 INFO: Last MySQL binlog file position 0 155, file name binlog.000003
180921 22:06:52 PCR1 INFO: The first data file is '/var/lib/mysql/ibdata1'
 and the new created log files are at '/var/lib/mysql'
180921 22:06:52 MAIN INFO: No Keyring file to process.
180921 22:06:52 MAIN INFO: Apply-log operation completed successfully.
180921 22:06:52 MAIN INFO: Full Backup has been restored successfully.
mysqlbackup completed OK! with 3 warnings
```

The container exits once the backup job is finished and, with the --rm option used when starting it, it is removed after it exits.

4. Restart the server container, which also restarts the restored server, using the following command:

```
docker restart mysqlserver
```

Or, start a new MySQL Server on the restored data directory, as shown here:

```
docker run --name=mysqlserver2 \
--mount type=bind,src=/path-on-host-machine/datadir/,dst=/var/lib/mysql \
-d mysql/enterprise-server:8.0
```

Log on to the server to check that the server is running with the restored data.

## <span id="page-42-0"></span>**Using mysqldump with Docker**

Besides [using MySQL Enterprise Backup to back up a MySQL Server running in a Docker container,](#page-40-0) you can perform a logical backup of your server by using the mysqldump utility, run inside a Docker container.

The following instructions assume that you already have a MySQL Server running in a Docker container and, when the container was first started, a host directory /path-on-host-machine/ datadir/ has been mounted onto the server's data directory /var/lib/mysql (see [bind-mounting](#page-38-0) [a host directory on the data directory of the MySQL Server](#page-38-0) for details), which contains the Unix socket file by which mysqldump and mysql can connect to the server. We also assume that, after the server has been started, a user with the proper privileges (admin in this example) has been created, with which mysqldump can access the server. Use the following steps to back up and restore MySQL Server data:

Backing up MySQL Server data using mysqldump with Docker:

1. On the same host where the MySQL Server container is running, start another container with an image of MySQL Server to perform a backup with the mysqldump utility (see documentation of the utility for its functionality, options, and limitations). Provide access to the server's data directory by bind mounting /path-on-host-machine/datadir/. Also, mount a host directory (/pathon-host-machine/backups/ in this example) onto a storage folder for backups inside the container (/data/backups is used in this example) to persist the backups you are creating. Here is a sample command for backing up all databases on the server using this setup:

```
$> docker run --entrypoint "/bin/sh" \ 
--mount type=bind,src=/path-on-host-machine/datadir/,dst=/var/lib/mysql \
--mount type=bind,src=/path-on-host-machine/backups/,dst=/data/backups \
--rm container-registry.oracle.com/mysql/community-server:8.0 \
-c "mysqldump -uadmin --password='password' --all-databases > /data/backups/all-databases.sql"
```

In the command, the --entrypoint option is used so that the system shell is invoked after the container is started, and the -c option is used to specify the mysqldump command to be run in the shell, whose output is redirected to the file all-databases.sql in the backup directory.

2. The container exits once the backup job is finished and, with the --rm option used to start it, it is removed after it exits. A logical backup been created, and can be found in the host directory mounted for storing the backup, as shown here:

```
$> ls /path-on-host-machine/backups/
all-databases.sql
```

Restoring MySQL Server data using mysqldump with Docker:

- 1. Make sure you have a MySQL Server running in a container, onto which you want your backed-up data to be restored.
- 2. Start a container with an image of MySQL Server to perform the restore with a mysql client. Bindmount the server's data directory, as well as the storage folder that contains your backup:

```
$> docker run \
--mount type=bind,src=/path-on-host-machine/datadir/,dst=/var/lib/mysql \
--mount type=bind,src=/path-on-host-machine/backups/,dst=/data/backups \
--rm container-registry.oracle.com/mysql/community-server:8.0 \
mysql -uadmin --password='password' -e "source /data/backups/all-databases.sql"
```

The container exits once the backup job is finished and, with the --rm option used when starting it, it is removed after it exits.

3. Log on to the server to check that the restored data is now on the server.

### <span id="page-43-1"></span>**Known Issues**

• When using the server system variable audit\_log\_file to configure the audit log file name, use the loose option modifier with it; otherwise, Docker cannot start the server.

### <span id="page-43-2"></span>**Docker Environment Variables**

When you create a MySQL Server container, you can configure the MySQL instance by using the - env option (short form -e) and specifying one or more environment variables. No server initialization is performed if the mounted data directory is not empty, in which case setting any of these variables has no effect (see [Persisting Data and Configuration Changes\)](#page-38-0), and no existing contents of the directory, including server settings, are modified during container startup.

Environment variables which can be used to configure a MySQL instance are listed here:

- The boolean variables including [MYSQL\\_RANDOM\\_ROOT\\_PASSWORD](#page-43-4), [MYSQL\\_ONETIME\\_PASSWORD](#page-43-0), [MYSQL\\_ALLOW\\_EMPTY\\_PASSWORD](#page-44-2), and [MYSQL\\_LOG\\_CONSOLE](#page-43-3) are made true by setting them with any strings of nonzero lengths. Therefore, setting them to, for example, "0", "false", or "no" does not make them false, but actually makes them true. This is a known issue.
- <span id="page-43-4"></span>• [MYSQL\\_RANDOM\\_ROOT\\_PASSWORD](#page-43-4): When this variable is true (which is its default state, unless [MYSQL\\_ROOT\\_PASSWORD](#page-44-3) is set or [MYSQL\\_ALLOW\\_EMPTY\\_PASSWORD](#page-44-2) is set to true), a random password for the server's root user is generated when the Docker container is started. The password is printed to stdout of the container and can be found by looking at the container's log (see [Starting](#page-34-0) [a MySQL Server Instance](#page-34-0)).
- <span id="page-43-0"></span>• [MYSQL\\_ONETIME\\_PASSWORD](#page-43-0): When the variable is true (which is its default state, unless [MYSQL\\_ROOT\\_PASSWORD](#page-44-3) is set or [MYSQL\\_ALLOW\\_EMPTY\\_PASSWORD](#page-44-2) is set to true), the root user's password is set as expired and must be changed before MySQL can be used normally.
- <span id="page-43-5"></span>• [MYSQL\\_DATABASE](#page-43-5): This variable allows you to specify the name of a database to be created on image startup. If a user name and a password are supplied with [MYSQL\\_USER](#page-43-6) and [MYSQL\\_PASSWORD](#page-43-6), the user is created and granted superuser access to this database (corresponding to GRANT ALL). The specified database is created by a CREATE DATABASE IF NOT EXIST statement, so that the variable has no effect if the database already exists.
- <span id="page-43-6"></span>• [MYSQL\\_USER](#page-43-6), [MYSQL\\_PASSWORD](#page-43-6): These variables are used in conjunction to create a user and set that user's password, and the user is granted superuser permissions for the database specified by the [MYSQL\\_DATABASE](#page-43-5) variable. Both [MYSQL\\_USER](#page-43-6) and [MYSQL\\_PASSWORD](#page-43-6) are required for a user to be created—if any of the two variables is not set, the other is ignored. If both variables are set but [MYSQL\\_DATABASE](#page-43-5) is not, the user is created without any privileges.

![](_page_43_Picture_11.jpeg)

#### **Note**

There is no need to use this mechanism to create the root superuser, which is created by default with the password set by either one of the mechanisms discussed in the descriptions for [MYSQL\\_ROOT\\_PASSWORD](#page-44-3) and [MYSQL\\_RANDOM\\_ROOT\\_PASSWORD](#page-43-4), unless [MYSQL\\_ALLOW\\_EMPTY\\_PASSWORD](#page-44-2) is true.

- <span id="page-43-7"></span>• [MYSQL\\_ROOT\\_HOST](#page-43-7): By default, MySQL creates the 'root'@'localhost' account. This account can only be connected to from inside the container as described in [Connecting to MySQL Server](#page-35-0) [from within the Container](#page-35-0). To allow root connections from other hosts, set this environment variable. For example, the value 172.17.0.1, which is the default Docker gateway IP, allows connections from the host machine that runs the container. The option accepts only one entry, but wildcards are allowed (for example, MYSQL\_ROOT\_HOST=172.\*.\*.\* or MYSQL\_ROOT\_HOST=%).
- <span id="page-43-3"></span>• [MYSQL\\_LOG\\_CONSOLE](#page-43-3): When the variable is true (which is its default state for MySQL 8.0 server containers), the MySQL Server's error log is redirected to stderr, so that the error log goes into the Docker container's log and is viewable using the docker logs mysqld-container command.

![](_page_44_Picture_1.jpeg)

### **Note**

The variable has no effect if a server configuration file from the host has been mounted (see [Persisting Data and Configuration Changes](#page-38-0) on bind-mounting a configuration file).

<span id="page-44-3"></span>• [MYSQL\\_ROOT\\_PASSWORD](#page-44-3): This variable specifies a password that is set for the MySQL root account.

![](_page_44_Picture_5.jpeg)

#### **Warning**

Setting the MySQL root user password on the command line is insecure. As an alternative to specifying the password explicitly, you can set the variable with a container file path for a password file, and then mount a file from your host that contains the password at the container file path. This is still not very secure, as the location of the password file is still exposed. It is preferable to use the default settings of [MYSQL\\_RANDOM\\_ROOT\\_PASSWORD](#page-43-4) and [MYSQL\\_ONETIME\\_PASSWORD](#page-43-0) both being true.

<span id="page-44-2"></span>• [MYSQL\\_ALLOW\\_EMPTY\\_PASSWORD](#page-44-2). Set it to true to allow the container to be started with a blank password for the root user.

![](_page_44_Picture_9.jpeg)

#### **Warning**

Setting this variable to true is insecure, because it is going to leave your MySQL instance completely unprotected, allowing anyone to gain complete superuser access. It is preferable to use the default settings of [MYSQL\\_RANDOM\\_ROOT\\_PASSWORD](#page-43-4) and [MYSQL\\_ONETIME\\_PASSWORD](#page-43-0) both being true.

## <span id="page-44-1"></span>**2.5.6.3 Deploying MySQL on Windows and Other Non-Linux Platforms with Docker**

![](_page_44_Picture_13.jpeg)

### **Warning**

The MySQL Docker images provided by Oracle are built specifically for Linux platforms. Other platforms are not supported, and users running the MySQL Docker images from Oracle on them are doing so at their own risk. This section discusses some known issues for the images when used on non-Linux platforms.

Known Issues for using the MySQL Server Docker images from Oracle on Windows include:

• If you are bind-mounting on the container's MySQL data directory (see [Persisting Data and](#page-38-0) [Configuration Changes](#page-38-0) for details), you have to set the location of the server socket file with the - socket option to somewhere outside of the MySQL data directory; otherwise, the server fails to start. This is because the way Docker for Windows handles file mounting does not allow a host file from being bind-mounted on the socket file.

## <span id="page-44-0"></span>**2.5.7 Installing MySQL on Linux from the Native Software Repositories**

Many Linux distributions include a version of the MySQL server, client tools, and development components in their native software repositories and can be installed with the platforms' standard package management systems. This section provides basic instructions for installing MySQL using those package management systems.

![](_page_44_Picture_20.jpeg)

### **Important**

Native packages are often several versions behind the currently available release. You are also normally unable to install development milestone releases (DMRs), since these are not usually made available in the native repositories.

Before proceeding, we recommend that you check out the other installation options described in [Section 2.5, "Installing MySQL on Linux"](#page-20-0).

Distribution specific instructions are shown below:

• **Red Hat Linux, Fedora, CentOS**

![](_page_45_Picture_4.jpeg)

#### **Note**

For a number of Linux distributions, you can install MySQL using the MySQL Yum repository instead of the platform's native software repository. See [Section 2.5.1, "Installing MySQL on Linux Using the MySQL Yum Repository"](#page-21-0) for details.

For Red Hat and similar distributions, the MySQL distribution is divided into a number of separate packages, mysql for the client tools, mysql-server for the server and associated tools, and mysql-libs for the libraries. The libraries are required if you want to provide connectivity from different languages and environments such as Perl, Python and others.

To install, use the yum command to specify the packages that you want to install. For example:

```
#> yum install mysql mysql-server mysql-libs mysql-server
Loaded plugins: presto, refresh-packagekit
Setting up Install Process
Resolving Dependencies
--> Running transaction check
---> Package mysql.x86_64 0:5.1.48-2.fc13 set to be updated
---> Package mysql-libs.x86_64 0:5.1.48-2.fc13 set to be updated
---> Package mysql-server.x86_64 0:5.1.48-2.fc13 set to be updated
--> Processing Dependency: perl-DBD-MySQL for package: mysql-server-5.1.48-2.fc13.x86_64
--> Running transaction check
---> Package perl-DBD-MySQL.x86_64 0:4.017-1.fc13 set to be updated
--> Finished Dependency Resolution
Dependencies Resolved
================================================================================
 Package Arch Version Repository Size
================================================================================
Installing:
 mysql x86_64 5.1.48-2.fc13 updates 889 k
 mysql-libs x86_64 5.1.48-2.fc13 updates 1.2 M
 mysql-server x86_64 5.1.48-2.fc13 updates 8.1 M
Installing for dependencies:
 perl-DBD-MySQL x86_64 4.017-1.fc13 updates 136 k
Transaction Summary
================================================================================
Install 4 Package(s)
Upgrade 0 Package(s)
Total download size: 10 M
Installed size: 30 M
Is this ok [y/N]: y
Downloading Packages:
Setting up and reading Presto delta metadata
Processing delta metadata
Package(s) data still to download: 10 M
(1/4): mysql-5.1.48-2.fc13.x86_64.rpm | 889 kB 00:04
(2/4): mysql-libs-5.1.48-2.fc13.x86_64.rpm | 1.2 MB 00:06
(3/4): mysql-server-5.1.48-2.fc13.x86_64.rpm | 8.1 MB 00:40
(4/4): perl-DBD-MySQL-4.017-1.fc13.x86_64.rpm | 136 kB 00:00
--------------------------------------------------------------------------------
Total 201 kB/s | 10 MB 00:52
Running rpm_check_debug
Running Transaction Test
Transaction Test Succeeded
Running Transaction
 Installing : mysql-libs-5.1.48-2.fc13.x86_64 1/4
```

```
 Installing : mysql-5.1.48-2.fc13.x86_64 2/4
 Installing : perl-DBD-MySQL-4.017-1.fc13.x86_64 3/4
 Installing : mysql-server-5.1.48-2.fc13.x86_64 4/4
Installed:
 mysql.x86_64 0:5.1.48-2.fc13 mysql-libs.x86_64 0:5.1.48-2.fc13
 mysql-server.x86_64 0:5.1.48-2.fc13
Dependency Installed:
 perl-DBD-MySQL.x86_64 0:4.017-1.fc13
Complete!
```

MySQL and the MySQL server should now be installed. A sample configuration file is installed into / etc/my.cnf. To start the MySQL server use systemctl:

```
$> systemctl start mysqld
```

The database tables are automatically created for you, if they do not already exist. You should, however, run mysql\_secure\_installation to set the root passwords on your server.

• **Debian, Ubuntu, Kubuntu**

![](_page_46_Picture_6.jpeg)

#### **Note**

For supported Debian and Ubuntu versions, MySQL can be installed using the [MySQL APT Repository](https://dev.mysql.com/downloads/repo/apt/) instead of the platform's native software repository. See [Section 2.5.2, "Installing MySQL on Linux Using the MySQL](#page-25-0) [APT Repository"](#page-25-0) for details.

On Debian and related distributions, there are two packages for MySQL in their software repositories, mysql-client and mysql-server, for the client and server components respectively. You should specify an explicit version, for example mysql-client-5.1, to ensure that you install the version of MySQL that you want.

To download and install, including any dependencies, use the apt-get command, specifying the packages that you want to install.

![](_page_46_Picture_11.jpeg)

### **Note**

Before installing, make sure that you update your apt-get index files to ensure you are downloading the latest available version.

![](_page_46_Picture_14.jpeg)

### **Note**

The apt-get command installs a number of packages, including the MySQL server, in order to provide the typical tools and application environment. This can mean that you install a large number of packages in addition to the main MySQL package.

During installation, the initial database is created, and you are prompted for the MySQL root password (and confirmation). A configuration file is created in /etc/mysql/my.cnf. An init script is created in /etc/init.d/mysql.

The server should already be started. You can manually start and stop the server using:

```
#> service mysql [start|stop]
```

The service is automatically added to the 2, 3 and 4 run levels, with stop scripts in the single, shutdown and restart levels.