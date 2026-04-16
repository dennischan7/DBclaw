---
source: MySQL 8.0 Reference
title: 00_Overview
---

By default, when you install MySQL after compiling it from source, the installation step installs files under /usr/local/mysql. The component locations under the installation directory are the same as for binary distributions. See Table 2.3, "MySQL Installation Layout for Generic Unix/Linux Binary Package", and Section 2.3.1, "MySQL Installation Layout on Microsoft Windows". To configure installation locations different from the defaults, use the options described at [Section 2.8.7, "MySQL](#page-63-0) [Source-Configuration Options"](#page-63-0).

# <span id="page-57-0"></span>**2.8.4 Installing MySQL Using a Standard Source Distribution**

To install MySQL from a standard source distribution:

- 1. Verify that your system satisfies the tool requirements listed at [Section 2.8.2, "Source Installation](#page-55-0) [Prerequisites".](#page-55-0)
- 2. Obtain a distribution file using the instructions in Section 2.1.3, "How to Get MySQL".
- 3. Configure, build, and install the distribution using the instructions in this section.
- 4. Perform postinstallation procedures using the instructions in [Section 2.9, "Postinstallation Setup](#page-94-1) [and Testing".](#page-94-1)

MySQL uses CMake as the build framework on all platforms. The instructions given here should enable you to produce a working installation. For additional information on using CMake to build MySQL, see [How to Build MySQL Server with CMake](https://dev.mysql.com/doc/internals/en/cmake.md).

If you start from a source RPM, use the following command to make a binary RPM that you can install. If you do not have rpmbuild, use rpm instead.

```
$> rpmbuild --rebuild --clean MySQL-VERSION.src.rpm
```

The result is one or more binary RPM packages that you install as indicated in [Section 2.5.4, "Installing](#page-26-1) [MySQL on Linux Using RPM Packages from Oracle"](#page-26-1).

The sequence for installation from a compressed tar file or Zip archive source distribution is similar to the process for installing from a generic binary distribution (see Section 2.2, "Installing MySQL on Unix/ Linux Using Generic Binaries"), except that it is used on all platforms and includes steps to configure and compile the distribution. For example, with a compressed tar file source distribution on Unix, the basic installation command sequence looks like this:

```
# Preconfiguration setup
$> groupadd mysql
$> useradd -r -g mysql -s /bin/false mysql
# Beginning of source-build specific instructions
$> tar zxvf mysql-VERSION.tar.gz
$> cd mysql-VERSION
$> mkdir bld
$> cd bld
$> cmake ..
$> make
$> make install
# End of source-build specific instructions
# Postinstallation setup
$> cd /usr/local/mysql
$> mkdir mysql-files
$> chown mysql:mysql mysql-files
$> chmod 750 mysql-files
$> bin/mysqld --initialize --user=mysql
$> bin/mysql_ssl_rsa_setup
$> bin/mysqld_safe --user=mysql &
# Next command is optional
$> cp support-files/mysql.server /etc/init.d/mysql.server
```

A more detailed version of the source-build specific instructions is shown following.

![](_page_58_Picture_1.jpeg)

### **Note**

The procedure shown here does not set up any passwords for MySQL accounts. After following the procedure, proceed to [Section 2.9, "Postinstallation](#page-94-1) [Setup and Testing",](#page-94-1) for postinstallation setup and testing.

- [Perform Preconfiguration Setup](#page-58-0)
- [Obtain and Unpack the Distribution](#page-58-1)
- [Configure the Distribution](#page-58-2)
- [Build the Distribution](#page-60-0)
- [Install the Distribution](#page-60-1)
- [Perform Postinstallation Setup](#page-61-1)

## <span id="page-58-0"></span>**Perform Preconfiguration Setup**

On Unix, set up the mysql user that owns the database directory and that should be used to run and execute the MySQL server, and the group to which this user belongs. For details, see Create a mysql User and Group. Then perform the following steps as the mysql user, except as noted.

### <span id="page-58-1"></span>**Obtain and Unpack the Distribution**

Pick the directory under which you want to unpack the distribution and change location into it.

Obtain a distribution file using the instructions in Section 2.1.3, "How to Get MySQL".

Unpack the distribution into the current directory:

• To unpack a compressed tar file, tar can decompress and unpack the distribution if it has z option support:

```
$> tar zxvf mysql-VERSION.tar.gz
```

If your tar does not have z option support, use gunzip to decompress the distribution and tar to unpack it:

```
$> gunzip < mysql-VERSION.tar.gz | tar xvf -
```

Alternatively, CMake can decompress and unpack the distribution:

```
$> cmake -E tar zxvf mysql-VERSION.tar.gz
```

• To unpack a Zip archive, use WinZip or another tool that can read .zip files.

Unpacking the distribution file creates a directory named mysql-VERSION.

### <span id="page-58-2"></span>**Configure the Distribution**

Change location into the top-level directory of the unpacked distribution:

```
$> cd mysql-VERSION
```

Build outside of the source tree to keep the tree clean. If the top-level source directory is named mysql-src under your current working directory, you can build in a directory named build at the same level. Create the directory and go there:

```
$> mkdir bld
$> cd bld
```

Configure the build directory. The minimum configuration command includes no options to override configuration defaults:

```
$> cmake ../mysql-src
```

The build directory need not be outside the source tree. For example, you can build in a directory named build under the top-level source tree. To do this, starting with mysql-src as your current working directory, create the directory build and then go there:

```
$> mkdir build
$> cd build
```

Configure the build directory. The minimum configuration command includes no options to override configuration defaults:

```
$> cmake ..
```

If you have multiple source trees at the same level (for example, to build multiple versions of MySQL), the second strategy can be advantageous. The first strategy places all build directories at the same level, which requires that you choose a unique name for each. With the second strategy, you can use the same name for the build directory within each source tree. The following instructions assume this second strategy.

On Windows, specify the development environment. For example, the following commands configure MySQL for 32-bit or 64-bit builds, respectively:

```
$> cmake .. -G "Visual Studio 12 2013"
$> cmake .. -G "Visual Studio 12 2013 Win64"
```

On macOS, to use the Xcode IDE:

```
$> cmake .. -G Xcode
```

When you run Cmake, you might want to add options to the command line. Here are some examples:

- [-DBUILD\\_CONFIG=mysql\\_release](#page-70-0): Configure the source with the same build options used by Oracle to produce binary distributions for official MySQL releases.
- [-DCMAKE\\_INSTALL\\_PREFIX=](#page-71-0)dir\_name: Configure the distribution for installation under a particular location.
- [-DCPACK\\_MONOLITHIC\\_INSTALL=1](#page-71-1): Cause make package to generate a single installation file rather than multiple files.
- [-DWITH\\_DEBUG=1](#page-82-0): Build the distribution with debugging support.

For a more extensive list of options, see [Section 2.8.7, "MySQL Source-Configuration Options".](#page-63-0)

To list the configuration options, use one of the following commands:

```
$> cmake .. -L # overview
$> cmake .. -LH # overview with help text
$> cmake .. -LAH # all params with help text
$> ccmake .. # interactive display
```

If CMake fails, you might need to reconfigure by running it again with different options. If you do reconfigure, take note of the following:

- If CMake is run after it has previously been run, it may use information that was gathered during its previous invocation. This information is stored in CMakeCache.txt. When CMake starts, it looks for that file and reads its contents if it exists, on the assumption that the information is still correct. That assumption is invalid when you reconfigure.
- Each time you run CMake, you must run make again to recompile. However, you may want to remove old object files from previous builds first because they were compiled using different configuration options.

To prevent old object files or configuration information from being used, run these commands in the build directory on Unix before re-running CMake:

```
$> make clean
$> rm CMakeCache.txt
```

Or, on Windows:

```
$> devenv MySQL.sln /clean
$> del CMakeCache.txt
```

Before asking on the [MySQL Community Slack](https://mysqlcommunity.slack.com/), check the files in the CMakeFiles directory for useful information about the failure. To file a bug report, please use the instructions in Section 1.5, "How to Report Bugs or Problems".

## <span id="page-60-0"></span>**Build the Distribution**

On Unix:

```
$> make
$> make VERBOSE=1
```

The second command sets VERBOSE to show the commands for each compiled source.

Use gmake instead on systems where you are using GNU make and it has been installed as gmake.

On Windows:

```
$> devenv MySQL.sln /build RelWithDebInfo
```

If you have gotten to the compilation stage, but the distribution does not build, see [Section 2.8.8,](#page-91-0) ["Dealing with Problems Compiling MySQL"](#page-91-0), for help. If that does not solve the problem, please enter it into our bugs database using the instructions given in Section 1.5, "How to Report Bugs or Problems". If you have installed the latest versions of the required tools, and they crash trying to process our configuration files, please report that also. However, if you get a command not found error or a similar problem for required tools, do not report it. Instead, make sure that all the required tools are installed and that your PATH variable is set correctly so that your shell can find them.

### <span id="page-60-1"></span>**Install the Distribution**

On Unix:

```
$> make install
```

This installs the files under the configured installation directory (by default, /usr/local/mysql). You might need to run the command as root.

To install in a specific directory, add a DESTDIR parameter to the command line:

```
$> make install DESTDIR="/opt/mysql"
```

Alternatively, generate installation package files that you can install where you like:

```
$> make package
```

This operation produces one or more .tar.gz files that can be installed like generic binary distribution packages. See Section 2.2, "Installing MySQL on Unix/Linux Using Generic Binaries". If you run CMake with [-DCPACK\\_MONOLITHIC\\_INSTALL=1](#page-71-1), the operation produces a single file. Otherwise, it produces multiple files.

On Windows, generate the data directory, then create a .zip archive installation package:

```
$> devenv MySQL.sln /build RelWithDebInfo /project initial_database
$> devenv MySQL.sln /build RelWithDebInfo /project package
```

You can install the resulting .zip archive where you like. See Section 2.3.4, "Installing MySQL on Microsoft Windows Using a noinstall ZIP Archive".

## <span id="page-61-1"></span>**Perform Postinstallation Setup**

The remainder of the installation process involves setting up the configuration file, creating the core databases, and starting the MySQL server. For instructions, see [Section 2.9, "Postinstallation Setup](#page-94-1) [and Testing".](#page-94-1)

![](_page_61_Picture_4.jpeg)

#### **Note**

The accounts that are listed in the MySQL grant tables initially have no passwords. After starting the server, you should set up passwords for them using the instructions in [Section 2.9, "Postinstallation Setup and Testing".](#page-94-1)

# <span id="page-61-0"></span>**2.8.5 Installing MySQL Using a Development Source Tree**

This section describes how to install MySQL from the latest development source code, which is hosted on [GitHub](https://github.com/). To obtain the MySQL Server source code from this repository hosting service, you can set up a local MySQL Git repository.

On [GitHub](https://github.com/), MySQL Server and other MySQL projects are found on the [MySQL](https://github.com/mysql) page. The MySQL Server project is a single repository that contains branches for several MySQL series.

- [Prerequisites for Installing from Development Source](#page-61-2)
- [Setting Up a MySQL Git Repository](#page-61-3)

## <span id="page-61-2"></span>**Prerequisites for Installing from Development Source**

To install MySQL from a development source tree, your system must satisfy the tool requirements listed at [Section 2.8.2, "Source Installation Prerequisites"](#page-55-0).

### <span id="page-61-3"></span>**Setting Up a MySQL Git Repository**

To set up a MySQL Git repository on your machine:

1. Clone the MySQL Git repository to your machine. The following command clones the MySQL Git repository to a directory named mysql-server. The initial download may take some time to complete, depending on the speed of your connection.

```
$> git clone https://github.com/mysql/mysql-server.git
Cloning into 'mysql-server'...
remote: Counting objects: 1198513, done.
remote: Total 1198513 (delta 0), reused 0 (delta 0), pack-reused 1198513
Receiving objects: 100% (1198513/1198513), 1.01 GiB | 7.44 MiB/s, done.
Resolving deltas: 100% (993200/993200), done.
Checking connectivity... done.
Checking out files: 100% (25510/25510), done.
```

2. When the clone operation completes, the contents of your local MySQL Git repository appear similar to the following:

```
~> cd mysql-server
~/mysql-server> ls
client extra mysys storage
cmake include packaging strings
CMakeLists.txt INSTALL plugin support-files
components libbinlogevents README testclients
config.h.cmake libchangestreams router unittest
configure.cmake libmysql run_doxygen.cmake utilities
Docs libservices scripts VERSION
Doxyfile-ignored LICENSE share vio
Doxyfile.in man sql win
doxygen_resources mysql-test sql-common
```

3. Use the git branch -r command to view the remote tracking branches for the MySQL repository.

```
~/mysql-server> git branch -r
 origin/5.7
 origin/8.0
 origin/HEAD -> origin/trunk
 origin/cluster-7.4
 origin/cluster-7.5
 origin/cluster-7.6
 origin/trunk
```

4. To view the branch that is checked out in your local repository, issue the git branch command. When you clone the MySQL Git repository, the latest MySQL branch is checked out automatically. The asterisk identifies the active branch.

```
~/mysql-server$ git branch
* trunk
```

5. To check out an earlier MySQL branch, run the git checkout command, specifying the branch name. For example, to check out the MySQL 5.7 branch:

```
~/mysql-server$ git checkout 5.7
Checking out files: 100% (9600/9600), done.
Branch 5.7 set up to track remote branch 5.7 from origin.
Switched to a new branch '5.7'
```

6. To obtain changes made after your initial setup of the MySQL Git repository, switch to the branch you want to update and issue the git pull command:

```
~/mysql-server$ git checkout 8.0
~/mysql-server$ git pull
```

To examine the commit history, use the git log command:

```
~/mysql-server$ git log
```

You can also browse commit history and source code on the GitHub [MySQL](https://github.com/mysql) site.

If you see changes or code that you have a question about, ask on [MySQL Community Slack](https://mysqlcommunity.slack.com/).

7. After you have cloned the MySQL Git repository and have checked out the branch you want to build, you can build MySQL Server from the source code. Instructions are provided in [Section 2.8.4,](#page-57-0) ["Installing MySQL Using a Standard Source Distribution",](#page-57-0) except that you skip the part about obtaining and unpacking the distribution.

Be careful about installing a build from a distribution source tree on a production machine. The installation command may overwrite your live release installation. If you already have MySQL installed and do not want to overwrite it, run CMake with values for the [CMAKE\\_INSTALL\\_PREFIX](#page-71-0), [MYSQL\\_TCP\\_PORT](#page-79-0), and [MYSQL\\_UNIX\\_ADDR](#page-79-1) options different from those used by your production server. For additional information about preventing multiple servers from interfering with each other, see Section 7.8, "Running Multiple MySQL Instances on One Machine".

Play hard with your new installation. For example, try to make new features crash. Start by running make test. See [The MySQL Test Suite](https://dev.mysql.com/doc/extending-mysql/8.0/en/mysql-test-suite.md).

# <span id="page-62-0"></span>**2.8.6 Configuring SSL Library Support**

An SSL library is required for support of encrypted connections, entropy for random number generation, and other encryption-related operations.

If you compile MySQL from a source distribution, CMake configures the distribution to use the installed OpenSSL library by default.

To compile using OpenSSL, use this procedure:

- 1. Ensure that OpenSSL 1.0.1 or newer is installed on your system. If the installed OpenSSL version is older than 1.0.1, CMake produces an error at MySQL configuration time. If it is necessary to obtain OpenSSL, visit <http://www.openssl.org>.
- 2. The [WITH\\_SSL](#page-86-0) CMake option determines which SSL library to use for compiling MySQL (see [Section 2.8.7, "MySQL Source-Configuration Options"](#page-63-0)). The default is [-DWITH\\_SSL=system](#page-86-0), which uses OpenSSL. To make this explicit, specify that option. For example:

```
cmake . -DWITH_SSL=system
```

That command configures the distribution to use the installed OpenSSL library. Alternatively, to explicitly specify the path name to the OpenSSL installation, use the following syntax. This can be useful if you have multiple versions of OpenSSL installed, to prevent CMake from choosing the wrong one:

```
cmake . -DWITH_SSL=path_name
```

Alternative OpenSSL system packages are supported as of MySQL 8.0.30 by using WITH\_SSL=openssl11 on EL7 or WITH\_SSL=openssl3 on EL8. Authentication plugins, such as LDAP and Kerberos, are disabled since they do not support these alternative versions of OpenSSL.

3. Compile and install the distribution.

To check whether a mysqld server supports encrypted connections, examine the value of the have\_ssl system variable:

```
mysql> SHOW VARIABLES LIKE 'have_ssl';
+---------------+-------+
| Variable_name | Value |
+---------------+-------+
| have_ssl | YES |
+---------------+-------+
```

If the value is YES, the server supports encrypted connections. If the value is DISABLED, the server is capable of supporting encrypted connections but was not started with the appropriate --ssl-xxx options to enable encrypted connections to be used; see Section 8.3.1, "Configuring MySQL to Use Encrypted Connections".

# <span id="page-63-0"></span>**2.8.7 MySQL Source-Configuration Options**

The CMake program provides a great deal of control over how you configure a MySQL source distribution. Typically, you do this using options on the CMake command line. For information about options supported by CMake, run either of these commands in the top-level source directory:

```
$> cmake . -LH
$> ccmake .
```

You can also affect CMake using certain environment variables. See Section 6.9, "Environment Variables".

For boolean options, the value may be specified as 1 or ON to enable the option, or as 0 or OFF to disable the option.

Many options configure compile-time defaults that can be overridden at server startup. For example, the [CMAKE\\_INSTALL\\_PREFIX](#page-71-0), [MYSQL\\_TCP\\_PORT](#page-79-0), and [MYSQL\\_UNIX\\_ADDR](#page-79-1) options that configure the default installation base directory location, TCP/IP port number, and Unix socket file can be changed at server startup with the --basedir, --port, and --socket options for mysqld. Where applicable, configuration option descriptions indicate the corresponding mysqld startup option.

The following sections provide more information about CMake options.

• [CMake Option Reference](#page-64-0)

- [General Options](#page-70-1)
- [Installation Layout Options](#page-71-2)
- [Storage Engine Options](#page-74-0)
- [Feature Options](#page-75-0)
- [Compiler Flags](#page-89-0)
- [CMake Options for Compiling NDB Cluster](#page-89-1)

### <span id="page-64-0"></span>**CMake Option Reference**

The following table shows the available CMake options. In the Default column, PREFIX stands for the value of the [CMAKE\\_INSTALL\\_PREFIX](#page-71-0) option, which specifies the installation base directory. This value is used as the parent location for several of the installation subdirectories.

**Table 2.14 MySQL Source-Configuration Option Reference (CMake)**

| Formats                                             | Description                                                                 | Default            |
|-----------------------------------------------------|-----------------------------------------------------------------------------|--------------------|
| ADD_GDB_INDEX                                       | Whether to enable generation<br>of .gdb_index section in binaries           |                    |
| BUILD_CONFIG                                        | Use same build options as<br>official releases                              |                    |
| BUNDLE_RUNTIME_LIBRARIES                            | Bundle runtime libraries with<br>server MSI and Zip packages for<br>Windows | OFF                |
| CMAKE_BUILD_TYPE                                    | Type of build to produce                                                    | RelWithDebInfo     |
| CMAKE_CXX_FLAGS                                     | Flags for C++ Compiler                                                      |                    |
| CMAKE_C_FLAGS                                       | Flags for C Compiler                                                        |                    |
| CMAKE_INSTALL_PREFIX                                | Installation base directory                                                 | /usr/local/mysql   |
| COMPILATION_COMMENT                                 | Comment about compilation<br>environment                                    |                    |
| COMPILATION_COMMENT_SERVERComment about compilation | environment for use by mysqld                                               |                    |
| COMPRESS_DEBUG_SECTIONS                             | Compress debug sections of<br>binary executables                            | OFF                |
| CPACK_MONOLITHIC_INSTALL                            | Whether package build produces<br>single file                               | OFF                |
| DEFAULT_CHARSET                                     | The default server character set                                            | utf8mb4            |
| DEFAULT_COLLATION                                   | The default server collation                                                | utf8mb4_0900_ai_ci |
| DISABLE_PSI_COND                                    | Exclude Performance Schema<br>condition instrumentation                     | OFF                |
| DISABLE_PSI_DATA_LOCK                               | Exclude the performance<br>schema data lock<br>instrumentation              | OFF                |
| DISABLE_PSI_ERROR                                   | Exclude the performance<br>schema server error<br>instrumentation           | OFF                |
| DISABLE_PSI_FILE                                    | Exclude Performance Schema<br>file instrumentation                          | OFF                |
| DISABLE_PSI_IDLE                                    | Exclude Performance Schema<br>idle instrumentation                          | OFF                |

| Formats                                                 | Description                                                                           | Default |
|---------------------------------------------------------|---------------------------------------------------------------------------------------|---------|
| DISABLE_PSI_MEMORY                                      | Exclude Performance Schema<br>memory instrumentation                                  | OFF     |
| DISABLE_PSI_METADATA                                    | Exclude Performance Schema<br>metadata instrumentation                                | OFF     |
| DISABLE_PSI_MUTEX                                       | Exclude Performance Schema<br>mutex instrumentation                                   | OFF     |
| DISABLE_PSI_PS                                          | Exclude the performance<br>schema prepared statements                                 | OFF     |
| DISABLE_PSI_RWLOCK                                      | Exclude Performance Schema<br>rwlock instrumentation                                  | OFF     |
| DISABLE_PSI_SOCKET                                      | Exclude Performance Schema<br>socket instrumentation                                  | OFF     |
| DISABLE_PSI_SP                                          | Exclude Performance Schema<br>stored program instrumentation                          | OFF     |
| DISABLE_PSI_STAGE                                       | Exclude Performance Schema<br>stage instrumentation                                   | OFF     |
| DISABLE_PSI_STATEMENT                                   | Exclude Performance Schema<br>statement instrumentation                               | OFF     |
| DISABLE_PSI_STATEMENT_DIGEST Exclude Performance        | Schema statements_digest<br>instrumentation                                           | OFF     |
| DISABLE_PSI_TABLE                                       | Exclude Performance Schema<br>table instrumentation                                   | OFF     |
| DISABLE_PSI_THREAD                                      | Exclude the performance<br>schema thread instrumentation                              | OFF     |
| DISABLE_PSI_TRANSACTION                                 | Exclude the performance<br>schema transaction<br>instrumentation                      | OFF     |
| DOWNLOAD_BOOST                                          | Whether to download the Boost<br>library                                              | OFF     |
| DOWNLOAD_BOOST_TIMEOUT                                  | Timeout in seconds for<br>downloading the Boost library                               | 600     |
| ENABLED_LOCAL_INFILE                                    | Whether to enable LOCAL for<br>LOAD DATA                                              | OFF     |
| ENABLED_PROFILING                                       | Whether to enable query profiling<br>code                                             | ON      |
|                                                         | ENABLE_EXPERIMENTAL_SYSVARSWhether to enabled experimental<br>InnoDB system variables | OFF     |
| ENABLE_GCOV                                             | Whether to include gcov support                                                       |         |
| ENABLE_GPROF                                            | Enable gprof (optimized Linux<br>builds only)                                         | OFF     |
| FORCE_COLORED_OUTPUT                                    | Whether to colorize compiler<br>output                                                | OFF     |
| FORCE_INSOURCE_BUILD                                    | Whether to force an in-source<br>build                                                | OFF     |
| FORCE_UNSUPPORTED_COMPILERWhether to permit unsupported | compilers                                                                             | OFF     |

| Formats                                                   | Description                                                                                                  | Default                  |
|-----------------------------------------------------------|--------------------------------------------------------------------------------------------------------------|--------------------------|
| FPROFILE_GENERATE                                         | Whether to generate profile<br>guided optimization data                                                      | OFF                      |
| FPROFILE_USE                                              | Whether to use profile guided<br>optimization data                                                           | OFF                      |
| HAVE_PSI_MEMORY_INTERFACE Enable performance schema       | memory tracing module for<br>memory allocation functions<br>used in dynamic storage of over<br>aligned types | OFF                      |
| IGNORE_AIO_CHECK                                          | With -<br>DBUILD_CONFIG=mysql_release,<br>ignore libaio check                                                | OFF                      |
| INSTALL_BINDIR                                            | User executables directory                                                                                   | PREFIX/bin               |
| INSTALL_DOCDIR                                            | Documentation directory                                                                                      | PREFIX/docs              |
| INSTALL_DOCREADMEDIR                                      | README file directory                                                                                        | PREFIX                   |
| INSTALL_INCLUDEDIR                                        | Header file directory                                                                                        | PREFIX/include           |
| INSTALL_INFODIR                                           | Info file directory                                                                                          | PREFIX/docs              |
| INSTALL_LAYOUT                                            | Select predefined installation<br>layout                                                                     | STANDALONE               |
| INSTALL_LIBDIR                                            | Library file directory                                                                                       | PREFIX/lib               |
| INSTALL_MANDIR                                            | Manual page directory                                                                                        | PREFIX/man               |
| INSTALL_MYSQLKEYRINGDIR                                   | Directory for keyring_file plugin<br>data file                                                               | platform specific        |
| INSTALL_MYSQLSHAREDIR                                     | Shared data directory                                                                                        | PREFIX/share             |
| INSTALL_MYSQLTESTDIR                                      | mysql-test directory                                                                                         | PREFIX/mysql-test        |
| INSTALL_PKGCONFIGDIR                                      | Directory for mysqlclient.pc pkg<br>config file                                                              | INSTALL_LIBDIR/pkgconfig |
| INSTALL_PLUGINDIR                                         | Plugin directory                                                                                             | PREFIX/lib/plugin        |
| INSTALL_PRIV_LIBDIR                                       | Installation private library<br>directory                                                                    |                          |
| INSTALL_SBINDIR                                           | Server executable directory                                                                                  | PREFIX/bin               |
| INSTALL_SECURE_FILE_PRIVDIRsecure_file_priv default value |                                                                                                              | platform specific        |
| INSTALL_SHAREDIR                                          | aclocal/mysql.m4 installation<br>directory                                                                   | PREFIX/share             |
| INSTALL_STATIC_LIBRARIES                                  | Whether to install static libraries                                                                          | ON                       |
| INSTALL_SUPPORTFILESDIR                                   | Extra support files directory                                                                                | PREFIX/support-files     |
| LINK_RANDOMIZE                                            | Whether to randomize order of<br>symbols in mysqld binary                                                    | OFF                      |
| LINK_RANDOMIZE_SEED                                       | Seed value for<br>LINK_RANDOMIZE option                                                                      | mysql                    |
| MAX_INDEXES                                               | Maximum indexes per table                                                                                    | 64                       |
| MSVC_CPPCHECK                                             | Enable MSVC code analysis.                                                                                   | OFF                      |
| MUTEX_TYPE                                                | InnoDB mutex type                                                                                            | event                    |
| MYSQLX_TCP_PORT                                           | TCP/IP port number used by X<br>Plugin                                                                       | 33060                    |

| Formats                                                     | Description                                                                              | Default          |
|-------------------------------------------------------------|------------------------------------------------------------------------------------------|------------------|
| MYSQLX_UNIX_ADDR                                            | Unix socket file used by X Plugin                                                        | /tmp/mysqlx.sock |
| MYSQL_DATADIR                                               | Data directory                                                                           |                  |
| MYSQL_MAINTAINER_MODE                                       | Whether to enable MySQL<br>maintainer-specific development<br>environment                | OFF              |
| MYSQL_PROJECT_NAME                                          | Windows/macOS project name                                                               | MySQL            |
| MYSQL_TCP_PORT                                              | TCP/IP port number                                                                       | 3306             |
| MYSQL_UNIX_ADDR                                             | Unix socket file                                                                         | /tmp/mysql.sock  |
| NDB_UTILS_LINK_DYNAMIC                                      | Cause NDB tools to be<br>dynamically linked to ndbclient                                 |                  |
| ODBC_INCLUDES                                               | ODBC includes directory                                                                  |                  |
| ODBC_LIB_DIR                                                | ODBC library directory                                                                   |                  |
| OPTIMIZER_TRACE                                             | Whether to support optimizer<br>tracing                                                  |                  |
| OPTIMIZE_SANITIZER_BUILDS Whether to optimize sanitizer     | builds                                                                                   | ON               |
| REPRODUCIBLE_BUILD                                          | Take extra care to create a<br>build result independent of build<br>location and time    |                  |
| SHOW_SUPPRESSED_COMPILER_WARNING Whether to show suppressed | compiler warnings and not fail<br>with -Werror.                                          | OFF              |
| SYSCONFDIR                                                  | Option file directory                                                                    |                  |
| SYSTEMD_PID_DIR                                             | Directory for PID file under<br>systemd                                                  | /var/run/mysqld  |
| SYSTEMD_SERVICE_NAME                                        | Name of MySQL service under<br>systemd                                                   | mysqld           |
| TMPDIR                                                      | tmpdir default value                                                                     |                  |
| USE_LD_LLD                                                  | Whether to use LLVM lld linker                                                           | ON               |
| WIN_DEBUG_NO_INLINE                                         | Whether to disable function<br>inlining                                                  | OFF              |
| WITHOUT_SERVER                                              | Do not build the server; internal<br>use only                                            | OFF              |
| WITHOUT_xxx_STORAGE_ENGINEExclude storage engine xxx from   | build                                                                                    |                  |
| WITH_ANT                                                    | Path to Ant for building GCS<br>Java wrapper                                             |                  |
| WITH_ASAN                                                   | Enable AddressSanitizer                                                                  | OFF              |
| WITH_ASAN_SCOPE                                             | Enable AddressSanitizer -<br>fsanitize-address-use-after<br>scope Clang flag             | OFF              |
| WITH_AUTHENTICATION_CLIENT_PLUGINS                          | Enabled automatically if<br>any corresponding server<br>authentication plugins are built |                  |
| WITH_AUTHENTICATION_LDAP                                    | Whether to report error if LDAP<br>authentication plugins cannot be<br>built             | OFF              |

| Formats                                                         | Description                                                                                                                       | Default |
|-----------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------|---------|
| WITH_AUTHENTICATION_PAM                                         | Build PAM authentication plugin                                                                                                   | OFF     |
| WITH_AWS_SDK                                                    | Location of Amazon Web<br>Services software development<br>kit                                                                    |         |
| WITH_BOOST                                                      | The location of the Boost library<br>sources                                                                                      |         |
| WITH_BUILD_ID                                                   | On Linux systems, generate a<br>unique build ID                                                                                   | ON      |
| WITH_CLASSPATH                                                  | Classpath to use when building<br>MySQL Cluster Connector for<br>Java. Default is an empty string.                                |         |
| WITH_CLIENT_PROTOCOL_TRACING Build client-side protocol tracing | framework                                                                                                                         | ON      |
| WITH_CURL                                                       | Location of curl library                                                                                                          |         |
| WITH_DEBUG                                                      | Whether to include debugging<br>support                                                                                           | OFF     |
| WITH_DEFAULT_COMPILER_OPTIONS Whether to use default compiler   | options                                                                                                                           | ON      |
| WITH_DEVELOPER_ENTITLEMENTSWhether to add the 'get              | task-allow' entitlement to all<br>executables on macOS to<br>generate a core dump in the<br>event of an unexpected server<br>halt | OFF     |
| WITH_EDITLINE                                                   | Which libedit/editline library to<br>use                                                                                          | bundled |
| WITH_ERROR_INSERT                                               | Enable error injection in the<br>NDB storage engine. Should<br>not be used for building binaries<br>intended for production.      | OFF     |
| WITH_FIDO                                                       | Type of FIDO library support                                                                                                      | bundled |
| WITH_ICU                                                        | Type of ICU support                                                                                                               | bundled |
| WITH_INNODB_EXTRA_DEBUG                                         | Whether to include extra<br>debugging support for InnoDB.                                                                         | OFF     |
| WITH_INNODB_MEMCACHED                                           | Whether to generate<br>memcached shared libraries.                                                                                | OFF     |
| WITH_JEMALLOC                                                   | Whether to link with -ljemalloc                                                                                                   | OFF     |
| WITH_KEYRING_TEST                                               | Build the keyring test program                                                                                                    | OFF     |
| WITH_LIBEVENT                                                   | Which libevent library to use                                                                                                     | bundled |
| WITH_LIBWRAP                                                    | Whether to include libwrap (TCP<br>wrappers) support                                                                              | OFF     |
| WITH_LOCK_ORDER                                                 | Whether to enable<br>LOCK_ORDER tooling                                                                                           | OFF     |
| WITH_LSAN                                                       | Whether to run LeakSanitizer,<br>without AddressSanitizer                                                                         | OFF     |
| WITH_LTO                                                        | Enable link-time optimizer                                                                                                        | OFF     |
| WITH_LZ4                                                        | Type of LZ4 library support                                                                                                       | bundled |

| Formats                                                          | Description                                                                                                                                                         | Default |
|------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------|
| WITH_MECAB                                                       | Compiles MeCab                                                                                                                                                      |         |
| WITH_MSAN                                                        | Enable MemorySanitizer                                                                                                                                              | OFF     |
| WITH_MSCRT_DEBUG                                                 | Enable Visual Studio CRT<br>memory leak tracing                                                                                                                     | OFF     |
| WITH_MYSQLX                                                      | Whether to disable X Protocol                                                                                                                                       | ON      |
| WITH_NDB                                                         | Build MySQL NDB Cluster,<br>including NDB storage engine<br>and all NDB programs                                                                                    | OFF     |
| WITH_NDBAPI_EXAMPLES                                             | Build API example programs.                                                                                                                                         | OFF     |
| WITH_NDBCLUSTER                                                  | NDB 8.0.30 and earlier: Build<br>NDB storage engine. NDB 8.0.31<br>and later: Deprecated; use<br>WITH_NDB instead                                                   | OFF     |
| WITH_NDBCLUSTER_STORAGE_ENGINE Prior to NDB 8.0.31, this was for | internal use only. NDB 8.0.31<br>and later: toggles (only) inclusion<br>of NDBCLUSTER storage engine                                                                | ON      |
| WITH_NDBMTD                                                      | Build multithreaded data node<br>binary                                                                                                                             | ON      |
| WITH_NDB_DEBUG                                                   | Produce a debug build for testing<br>or troubleshooting.                                                                                                            | OFF     |
| WITH_NDB_JAVA                                                    | Enable building of Java and<br>ClusterJ support. Enabled by<br>default. Supported in MySQL<br>Cluster only.                                                         | ON      |
| WITH_NDB_PORT                                                    | Default port used by a<br>management server built with<br>this option. If this option was not<br>used to build it, the management<br>server's default port is 1186. | [none]  |
| WITH_NDB_TEST                                                    | Include NDB API test programs.                                                                                                                                      | OFF     |
| WITH_NUMA                                                        | Set NUMA memory allocation<br>policy                                                                                                                                |         |
| WITH_PACKAGE_FLAGS                                               | For flags typically used for RPM/<br>DEB packages, whether to add<br>them to standalone builds on<br>those platforms                                                |         |
| WITH_PROTOBUF                                                    | Which Protocol Buffers package<br>to use                                                                                                                            | bundled |
| WITH_RAPID                                                       | Whether to build rapid<br>development cycle plugins                                                                                                                 | ON      |
| WITH_RAPIDJSON                                                   | Type of RapidJSON support                                                                                                                                           | bundled |
| WITH_ROUTER                                                      | Whether to build MySQL Router                                                                                                                                       | ON      |
| WITH_SASL                                                        | Internal use only                                                                                                                                                   |         |
| WITH_SSL                                                         | Type of SSL support                                                                                                                                                 | system  |
| WITH_SYSTEMD                                                     | Enable installation of systemd<br>support files                                                                                                                     | OFF     |

| Formats                 | Description                                                               | Default |
|-------------------------|---------------------------------------------------------------------------|---------|
| WITH_SYSTEMD_DEBUG      | Enable additional systemd debug<br>information                            | OFF     |
| WITH_SYSTEM_LIBS        | Set system value of library<br>options not set explicitly                 | OFF     |
| WITH_TCMALLOC           | Whether to link with -ltcmalloc.<br>BUNDLED is supported on Linux<br>only | OFF     |
| WITH_TEST_TRACE_PLUGIN  | Build test protocol trace plugin                                          | OFF     |
| WITH_TSAN               | Enable ThreadSanitizer                                                    | OFF     |
| WITH_UBSAN              | Enable Undefined Behavior<br>Sanitizer                                    | OFF     |
| WITH_UNIT_TESTS         | Compile MySQL with unit tests                                             | ON      |
| WITH_UNIXODBC           | Enable unixODBC support                                                   | OFF     |
| WITH_VALGRIND           | Whether to compile in Valgrind<br>header files                            | OFF     |
| WITH_WIN_JEMALLOC       | Path to directory containing<br>jemalloc.dll                              |         |
| WITH_ZLIB               | Type of zlib support                                                      | bundled |
| WITH_ZSTD               | Type of zstd support                                                      | bundled |
| WITH_xxx_STORAGE_ENGINE | Compile storage engine xxx<br>statically into server                      |         |

### <span id="page-70-1"></span><span id="page-70-0"></span>**General Options**

• [-DBUILD\\_CONFIG=mysql\\_release](#page-70-0)

This option configures a source distribution with the same build options used by Oracle to produce binary distributions for official MySQL releases.

<span id="page-70-4"></span>• [-DWITH\\_BUILD\\_ID=](#page-70-4)bool

On Linux systems, generates a unique build ID which is used as the value of the build\_id system variable and written to the MySQL server log on startup. Set this option to OFF to disable this feature.

Added in MySQL 8.0.31, this option has no effect on platforms other than Linux.

<span id="page-70-2"></span>• [-DBUNDLE\\_RUNTIME\\_LIBRARIES=](#page-70-2)bool

Whether to bundle runtime libraries with server MSI and Zip packages for Windows.

<span id="page-70-3"></span>• [-DCMAKE\\_BUILD\\_TYPE=](#page-70-3)type

The type of build to produce:

- RelWithDebInfo: Enable optimizations and generate debugging information. This is the default MySQL build type.
- Release: Enable optimizations but omit debugging information to reduce the build size. This build type was added in MySQL 8.0.13.
- Debug: Disable optimizations and generate debugging information. This build type is also used if the [WITH\\_DEBUG](#page-82-0) option is enabled. That is, [-DWITH\\_DEBUG=1](#page-82-0) has the same effect as [-](#page-70-3) [DCMAKE\\_BUILD\\_TYPE=Debug](#page-70-3).

The option values None and MinSizeRel are not supported.

<span id="page-71-1"></span>• [-DCPACK\\_MONOLITHIC\\_INSTALL=](#page-71-1)bool

This option affects whether the make package operation produces multiple installation package files or a single file. If disabled, the operation produces multiple installation package files, which may be useful if you want to install only a subset of a full MySQL installation. If enabled, it produces a single file for installing everything.

<span id="page-71-4"></span>• [-DFORCE\\_INSOURCE\\_BUILD=](#page-71-4)bool

Defines whether to force an in-source build. Out-of-source builds are recommended, as they permit multiple builds from the same source, and cleanup can be performed quickly by removing the build directory. To force an in-source build, invoke CMake with [-DFORCE\\_INSOURCE\\_BUILD=ON](#page-71-4).

<span id="page-71-3"></span>• [-DFORCE\\_COLORED\\_OUTPUT=](#page-71-3)bool

Defines whether to enable colorized compiler output for gcc and clang when compiling on the command line. Defaults to OFF.

## <span id="page-71-2"></span>**Installation Layout Options**

The [CMAKE\\_INSTALL\\_PREFIX](#page-71-0) option indicates the base installation directory. Other options with names of the form INSTALL\_xxx that indicate component locations are interpreted relative to the prefix and their values are relative pathnames. Their values should not include the prefix.

<span id="page-71-0"></span>• [-DCMAKE\\_INSTALL\\_PREFIX=](#page-71-0)dir\_name

The installation base directory.

This value can be set at server startup using the --basedir option.

<span id="page-71-5"></span>• [-DINSTALL\\_BINDIR=](#page-71-5)dir\_name

Where to install user programs.

<span id="page-71-6"></span>• [-DINSTALL\\_DOCDIR=](#page-71-6)dir\_name

Where to install documentation.

<span id="page-71-7"></span>• [-DINSTALL\\_DOCREADMEDIR=](#page-71-7)dir\_name

Where to install README files.

<span id="page-71-8"></span>• [-DINSTALL\\_INCLUDEDIR=](#page-71-8)dir\_name

Where to install header files.

<span id="page-71-9"></span>• [-DINSTALL\\_INFODIR=](#page-71-9)dir\_name

Where to install Info files.

<span id="page-71-10"></span>• [-DINSTALL\\_LAYOUT=](#page-71-10)name

Select a predefined installation layout:

- STANDALONE: Same layout as used for .tar.gz and .zip packages. This is the default.
- RPM: Layout similar to RPM packages.
- SVR4: Solaris package layout.
- DEB: DEB package layout (experimental).

You can select a predefined layout but modify individual component installation locations by specifying other options. For example:

```
cmake . -DINSTALL_LAYOUT=SVR4 -DMYSQL_DATADIR=/var/mysql/data
```

The [INSTALL\\_LAYOUT](#page-71-10) value determines the default value of the secure\_file\_priv, keyring\_encrypted\_file\_data, and keyring\_file\_data system variables. See the descriptions of those variables in Section 7.1.8, "Server System Variables", and Section 8.4.4.19, "Keyring System Variables".

<span id="page-72-0"></span>• [-DINSTALL\\_LIBDIR=](#page-72-0)dir\_name

Where to install library files.

<span id="page-72-1"></span>• [-DINSTALL\\_MANDIR=](#page-72-1)dir\_name

Where to install manual pages.

<span id="page-72-2"></span>• [-DINSTALL\\_MYSQLKEYRINGDIR=](#page-72-2)dir\_path

The default directory to use as the location of the keyring\_file plugin data file. The default value is platform specific and depends on the value of the [INSTALL\\_LAYOUT](#page-71-10) CMake option; see the description of the keyring\_file\_data system variable in Section 7.1.8, "Server System Variables".

<span id="page-72-3"></span>• [-DINSTALL\\_MYSQLSHAREDIR=](#page-72-3)dir\_name

Where to install shared data files.

<span id="page-72-4"></span>• [-DINSTALL\\_MYSQLTESTDIR=](#page-72-4)dir\_name

Where to install the mysql-test directory. To suppress installation of this directory, explicitly set the option to the empty value ([-DINSTALL\\_MYSQLTESTDIR=](#page-72-4)).

<span id="page-72-5"></span>• [-DINSTALL\\_PKGCONFIGDIR=](#page-72-5)dir\_name

The directory in which to install the mysqlclient.pc file for use by pkg-config. The default value is INSTALL\_LIBDIR/pkgconfig, unless [INSTALL\\_LIBDIR](#page-72-0) ends with /mysql, in which case that is removed first.

<span id="page-72-6"></span>• [-DINSTALL\\_PLUGINDIR=](#page-72-6)dir\_name

The location of the plugin directory.

This value can be set at server startup with the --plugin\_dir option.

<span id="page-72-7"></span>• [-DINSTALL\\_PRIV\\_LIBDIR=](#page-72-7)dir\_name

The location of the dynamic library directory.

**Default location.** For RPM builds, this is /usr/lib64/mysql/private/, for DEB it is /usr/ lib/mysql/private/, and for TAR it is lib/private/.

**Protobuf.** Because this is a private location, the loader (such as ld-linux.so on Linux) may not find the libprotobuf.so files without help. To guide the loader, RPATH=\$ORIGIN/../ \$INSTALL\_PRIV\_LIBDIR is added to mysqld and mysqlxtest. This works for most cases but when using the Resource Group feature, mysqld is setsuid, and the loader ignores any RPATH which contains \$ORIGIN. To overcome this, an explicit full path to the directory is set in the DEB and RPM versions of mysqld, since the target destination is known. For tarball installs, patching of mysqld with a tool like patchelf is required.

This option was added in MySQL 8.0.18.

<span id="page-73-0"></span>• [-DINSTALL\\_SBINDIR=](#page-73-0)dir\_name

Where to install the mysqld server.

<span id="page-73-1"></span>• [-DINSTALL\\_SECURE\\_FILE\\_PRIVDIR=](#page-73-1)dir\_name

The default value for the secure\_file\_priv system variable. The default value is platform specific and depends on the value of the [INSTALL\\_LAYOUT](#page-71-10) CMake option; see the description of the secure\_file\_priv system variable in Section 7.1.8, "Server System Variables".

<span id="page-73-2"></span>• [-DINSTALL\\_SHAREDIR=](#page-73-2)dir\_name

Where to install aclocal/mysql.m4.

<span id="page-73-3"></span>• [-DINSTALL\\_STATIC\\_LIBRARIES=](#page-73-3)bool

Whether to install static libraries. The default is ON. If set to OFF, these library files are not installed: libmysqlclient.a, libmysqlservices.a.

<span id="page-73-4"></span>• [-DINSTALL\\_SUPPORTFILESDIR=](#page-73-4)dir\_name

Where to install extra support files.

<span id="page-73-5"></span>• [-DLINK\\_RANDOMIZE=](#page-73-5)bool

Whether to randomize the order of symbols in the mysqld binary. The default is OFF. This option should be enabled only for debugging purposes.

<span id="page-73-6"></span>• [-DLINK\\_RANDOMIZE\\_SEED=](#page-73-6)val

Seed value for the [LINK\\_RANDOMIZE](#page-73-5) option. The value is a string. The default is mysql, an arbitrary choice.

<span id="page-73-7"></span>• [-DMYSQL\\_DATADIR=](#page-73-7)dir\_name

The location of the MySQL data directory.

This value can be set at server startup with the --datadir option.

<span id="page-73-8"></span>• [-DODBC\\_INCLUDES=](#page-73-8)dir\_name

The location of the ODBC includes directory, which may be used while configuring Connector/ODBC.

<span id="page-73-9"></span>• [-DODBC\\_LIB\\_DIR=](#page-73-9)dir\_name

The location of the ODBC library directory, which may be used while configuring Connector/ODBC.

<span id="page-73-10"></span>• [-DSYSCONFDIR=](#page-73-10)dir\_name

The default my.cnf option file directory.

This location cannot be set at server startup, but you can start the server with a given option file using the --defaults-file=file\_name option, where file\_name is the full path name to the file.

<span id="page-73-11"></span>• [-DSYSTEMD\\_PID\\_DIR=](#page-73-11)dir\_name

The name of the directory in which to create the PID file when MySQL is managed by systemd. The default is /var/run/mysqld; this might be changed implicitly according to the [INSTALL\\_LAYOUT](#page-71-10) value.

This option is ignored unless [WITH\\_SYSTEMD](#page-87-0) is enabled.

<span id="page-73-12"></span>• [-DSYSTEMD\\_SERVICE\\_NAME=](#page-73-12)name

The name of the MySQL service to use when MySQL is managed by systemd. The default is mysqld; this might be changed implicitly according to the [INSTALL\\_LAYOUT](#page-71-10) value.

This option is ignored unless [WITH\\_SYSTEMD](#page-87-0) is enabled.

<span id="page-74-1"></span>• [-DTMPDIR=](#page-74-1)dir\_name

The default location to use for the tmpdir system variable. If unspecified, the value defaults to P\_tmpdir in <stdio.h>.

## <span id="page-74-0"></span>**Storage Engine Options**

Storage engines are built as plugins. You can build a plugin as a static module (compiled into the server) or a dynamic module (built as a dynamic library that must be installed into the server using the INSTALL PLUGIN statement or the --plugin-load option before it can be used). Some plugins might not support static or dynamic building.

The InnoDB, MyISAM, MERGE, MEMORY, and CSV engines are mandatory (always compiled into the server) and need not be installed explicitly.

To compile a storage engine statically into the server, use -DWITH\_engine\_STORAGE\_ENGINE=1. Some permissible engine values are ARCHIVE, BLACKHOLE, EXAMPLE, and FEDERATED. Examples:

```
-DWITH_ARCHIVE_STORAGE_ENGINE=1
-DWITH_BLACKHOLE_STORAGE_ENGINE=1
```

To build MySQL with support for NDB Cluster, use the [WITH\\_NDB](#page-90-3) option. (NDB 8.0.30 and earlier: Use [WITH\\_NDBCLUSTER](#page-90-5).)

![](_page_74_Picture_11.jpeg)

#### **Note**

It is not possible to compile without Performance Schema support. If it is desired to compile without particular types of instrumentation, that can be done with the following CMake options:

```
DISABLE_PSI_COND
DISABLE_PSI_DATA_LOCK
DISABLE_PSI_ERROR
DISABLE_PSI_FILE
DISABLE_PSI_IDLE
DISABLE_PSI_MEMORY
DISABLE_PSI_METADATA
DISABLE_PSI_MUTEX
DISABLE_PSI_PS
DISABLE_PSI_RWLOCK
DISABLE_PSI_SOCKET
DISABLE_PSI_SP
DISABLE_PSI_STAGE
DISABLE_PSI_STATEMENT
DISABLE_PSI_STATEMENT_DIGEST
DISABLE_PSI_TABLE
DISABLE_PSI_THREAD
DISABLE_PSI_TRANSACTION
```

For example, to compile without mutex instrumentation, configure MySQL using [-DDISABLE\\_PSI\\_MUTEX=1](#page-76-3).

To exclude a storage engine from the build, use -DWITH\_engine\_STORAGE\_ENGINE=0. Examples:

```
-DWITH_ARCHIVE_STORAGE_ENGINE=0
-DWITH_EXAMPLE_STORAGE_ENGINE=0
-DWITH_FEDERATED_STORAGE_ENGINE=0
```

It is also possible to exclude a storage engine from the build using - DWITHOUT\_engine\_STORAGE\_ENGINE=1 (but -DWITH\_engine\_STORAGE\_ENGINE=0 is preferred). Examples:

```
-DWITHOUT_ARCHIVE_STORAGE_ENGINE=1
-DWITHOUT_EXAMPLE_STORAGE_ENGINE=1
-DWITHOUT_FEDERATED_STORAGE_ENGINE=1
```

If neither -DWITH\_engine\_STORAGE\_ENGINE nor -DWITHOUT\_engine\_STORAGE\_ENGINE are specified for a given storage engine, the engine is built as a shared module, or excluded if it cannot be built as a shared module.

## <span id="page-75-1"></span><span id="page-75-0"></span>**Feature Options**

• [-DADD\\_GDB\\_INDEX=](#page-75-1)bool

This option determines whether to enable generation of a .gdb\_index section in binaries, which makes loading them in a debugger faster. The option is disabled by default. lld linker is used, and is disabled by It has no effect if a linker other than lld or GNU gold is used.

This option was added in MySQL 8.0.18.

<span id="page-75-2"></span>• [-DCOMPILATION\\_COMMENT=](#page-75-2)string

A descriptive comment about the compilation environment. As of MySQL 8.0.14, mysqld uses [COMPILATION\\_COMMENT\\_SERVER](#page-75-3). Other programs continue to use [COMPILATION\\_COMMENT](#page-75-2).

<span id="page-75-4"></span>• [-DCOMPRESS\\_DEBUG\\_SECTIONS=](#page-75-4)bool

Whether to compress the debug sections of binary executables (Linux only). Compressing executable debug sections saves space at the cost of extra CPU time during the build process.

The default is OFF. If this option is not set explicitly but the COMPRESS\_DEBUG\_SECTIONS environment variable is set, the option takes its value from that variable.

This option was added in MySQL 8.0.22.

<span id="page-75-3"></span>• [-DCOMPILATION\\_COMMENT\\_SERVER=](#page-75-3)string

A descriptive comment about the compilation environment for use by mysqld (for example, to set the version\_comment system variable). This option was added in MySQL 8.0.14. Prior to 8.0.14, the server uses [COMPILATION\\_COMMENT](#page-75-2).

<span id="page-75-5"></span>• [-DDEFAULT\\_CHARSET=](#page-75-5)charset\_name

The server character set. By default, MySQL uses the utf8mb4 character set.

charset\_name may be one of binary, armscii8, ascii, big5, cp1250, cp1251, cp1256, cp1257, cp850, cp852, cp866, cp932, dec8, eucjpms, euckr, gb2312, gbk, geostd8, greek, hebrew, hp8, keybcs2, koi8r, koi8u, latin1, latin2, latin5, latin7, macce, macroman, sjis, swe7, tis620, ucs2, ujis, utf8mb3, utf8mb4, utf16, utf16le, utf32.

This value can be set at server startup with the --character-set-server option.

<span id="page-75-6"></span>• [-DDEFAULT\\_COLLATION=](#page-75-6)collation\_name

The server collation. By default, MySQL uses utf8mb4\_0900\_ai\_ci. Use the SHOW COLLATION statement to determine which collations are available for each character set.

This value can be set at server startup with the --collation\_server option.

<span id="page-75-7"></span>• [-DDISABLE\\_PSI\\_COND=](#page-75-7)bool

Whether to exclude the Performance Schema condition instrumentation. The default is OFF (include).

<span id="page-75-8"></span>• [-DDISABLE\\_PSI\\_FILE=](#page-75-8)bool

Whether to exclude the Performance Schema file instrumentation. The default is OFF (include).

<span id="page-76-0"></span>• [-DDISABLE\\_PSI\\_IDLE=](#page-76-0)bool

Whether to exclude the Performance Schema idle instrumentation. The default is OFF (include).

<span id="page-76-1"></span>• [-DDISABLE\\_PSI\\_MEMORY=](#page-76-1)bool

Whether to exclude the Performance Schema memory instrumentation. The default is OFF (include).

<span id="page-76-2"></span>• [-DDISABLE\\_PSI\\_METADATA=](#page-76-2)bool

Whether to exclude the Performance Schema metadata instrumentation. The default is OFF (include).

<span id="page-76-3"></span>• [-DDISABLE\\_PSI\\_MUTEX=](#page-76-3)bool

Whether to exclude the Performance Schema mutex instrumentation. The default is OFF (include).

<span id="page-76-5"></span>• [-DDISABLE\\_PSI\\_RWLOCK=](#page-76-5)bool

Whether to exclude the Performance Schema rwlock instrumentation. The default is OFF (include).

<span id="page-76-6"></span>• [-DDISABLE\\_PSI\\_SOCKET=](#page-76-6)bool

Whether to exclude the Performance Schema socket instrumentation. The default is OFF (include).

<span id="page-76-7"></span>• [-DDISABLE\\_PSI\\_SP=](#page-76-7)bool

Whether to exclude the Performance Schema stored program instrumentation. The default is OFF (include).

<span id="page-76-8"></span>• [-DDISABLE\\_PSI\\_STAGE=](#page-76-8)bool

Whether to exclude the Performance Schema stage instrumentation. The default is OFF (include).

<span id="page-76-9"></span>• [-DDISABLE\\_PSI\\_STATEMENT=](#page-76-9)bool

Whether to exclude the Performance Schema statement instrumentation. The default is OFF (include).

<span id="page-76-10"></span>• [-DDISABLE\\_PSI\\_STATEMENT\\_DIGEST=](#page-76-10)bool

Whether to exclude the Performance Schema statement digest instrumentation. The default is OFF (include).

<span id="page-76-11"></span>• [-DDISABLE\\_PSI\\_TABLE=](#page-76-11)bool

Whether to exclude the Performance Schema table instrumentation. The default is OFF (include).

<span id="page-76-13"></span>• [-DDISABLE\\_SHARED=](#page-76-13)bool

Whether to disable building build shared libraries and compile position-dependent code. The default is OFF (compile position-independent code).

This option is unused, and was removed in MySQL 8.0.18.

<span id="page-76-4"></span>• [-DDISABLE\\_PSI\\_PS=](#page-76-4)bool

Exclude the Performance Schema prepared statements instances instrumentation. The default is OFF (include).

<span id="page-76-12"></span>• [-DDISABLE\\_PSI\\_THREAD=](#page-76-12)bool

Exclude the Performance Schema thread instrumentation. The default is OFF (include).

Only disable threads when building without any instrumentation, because other instrumentations have a dependency on threads.

<span id="page-77-2"></span>• [-DDISABLE\\_PSI\\_TRANSACTION=](#page-77-2)bool

Exclude the Performance Schema transaction instrumentation. The default is OFF (include).

<span id="page-77-0"></span>• [-DDISABLE\\_PSI\\_DATA\\_LOCK=](#page-77-0)bool

Exclude the performance schema data lock instrumentation. The default is OFF (include).

<span id="page-77-1"></span>• [-DDISABLE\\_PSI\\_ERROR=](#page-77-1)bool

Exclude the performance schema server error instrumentation. The default is OFF (include).

<span id="page-77-3"></span>• [-DDOWNLOAD\\_BOOST=](#page-77-3)bool

Whether to download the Boost library. The default is OFF.

See the [WITH\\_BOOST](#page-81-0) option for additional discussion about using Boost.

<span id="page-77-4"></span>• [-DDOWNLOAD\\_BOOST\\_TIMEOUT=](#page-77-4)seconds

The timeout in seconds for downloading the Boost library. The default is 600 seconds.

See the [WITH\\_BOOST](#page-81-0) option for additional discussion about using Boost.

<span id="page-77-9"></span>• [-DENABLE\\_DOWNLOADS=](#page-77-9)bool

Whether to download optional files. For example, with this option enabled, CMake downloads the Google Test distribution that is used by the test suite to run unit tests, or Ant and JUnit, required for building the GCS Java wrapper.

As of MySQL 8.0.26, MySQL source distributions bundle the Google Test source code used to run unit tests. Consequently, as of that version the [WITH\\_GMOCK](#page-83-5) and [ENABLE\\_DOWNLOADS](#page-77-9) CMake options are removed and are ignored if specified.

<span id="page-77-6"></span>• [-DENABLE\\_EXPERIMENTAL\\_SYSVARS=](#page-77-6)bool

Whether to enable experimental InnoDB system variables. Experimental system variables are intended for those engaged in MySQL development, should only be used in a development or test environment, and may be removed without notice in a future MySQL release. For information about experimental system variables, refer to /storage/innobase/handler/ha\_innodb.cc in the MySQL source tree. Experimental system variables can be identified by searching for "PLUGIN\_VAR\_EXPERIMENTAL".

<span id="page-77-7"></span>• [-DENABLE\\_GCOV=](#page-77-7)bool

Whether to include gcov support (Linux only).

<span id="page-77-8"></span>• [-DENABLE\\_GPROF=](#page-77-8)bool

Whether to enable gprof (optimized Linux builds only).

<span id="page-77-5"></span>• [-DENABLED\\_LOCAL\\_INFILE=](#page-77-5)bool

This option controls the compiled-in default LOCAL capability for the MySQL client library. Clients that make no explicit arrangements therefore have LOCAL capability disabled or enabled according to the [ENABLED\\_LOCAL\\_INFILE](#page-77-5) setting specified at MySQL build time.

By default, the client library in MySQL binary distributions is compiled with [ENABLED\\_LOCAL\\_INFILE](#page-77-5) disabled. If you compile MySQL from source, configure it with [ENABLED\\_LOCAL\\_INFILE](#page-77-5) disabled or enabled based on whether clients that make no explicit arrangements should have LOCAL capability disabled or enabled, respectively.

[ENABLED\\_LOCAL\\_INFILE](#page-77-5) controls the default for client-side LOCAL capability. For the server, the local\_infile system variable controls server-side LOCAL capability. To explicitly cause the server to refuse or permit LOAD DATA LOCAL statements (regardless of how client programs and libraries are configured at build time or runtime), start mysqld with --local-infile disabled or enabled, respectively. local\_infile can also be set at runtime. See Section 8.1.6, "Security Considerations for LOAD DATA LOCAL".

<span id="page-78-0"></span>• [-DENABLED\\_PROFILING=](#page-78-0)bool

Whether to enable query profiling code (for the SHOW PROFILE and SHOW PROFILES statements).

<span id="page-78-1"></span>• [-DFORCE\\_UNSUPPORTED\\_COMPILER=](#page-78-1)bool

By default, CMake checks for minimum versions of [supported compilers;](#page-55-0) to disable this check, use [-](#page-78-1) [DFORCE\\_UNSUPPORTED\\_COMPILER=ON](#page-78-1).

<span id="page-78-2"></span>• [-DFPROFILE\\_GENERATE=](#page-78-2)bool

Whether to generate profile guided optimization (PGO) data. This option is available for experimenting with PGO with GCC. See cmake/fprofile.cmake in the MySQL source distribution for information about using [FPROFILE\\_GENERATE](#page-78-2) and [FPROFILE\\_USE](#page-78-3). These options have been tested with GCC 8 and 9.

This option was added in MySQL 8.0.19.

<span id="page-78-3"></span>• [-DFPROFILE\\_USE=](#page-78-3)bool

Whether to use profile guided optimization (PGO) data. This option is available for experimenting with PGO with GCC. See the cmake/fprofile.cmake file in a MySQL source distribution for information about using [FPROFILE\\_GENERATE](#page-78-2) and [FPROFILE\\_USE](#page-78-3). These options have been tested with GCC 8 and 9.

Enabling [FPROFILE\\_USE](#page-78-3) also enables [WITH\\_LTO](#page-84-4).

This option was added in MySQL 8.0.19.

<span id="page-78-4"></span>• [-DHAVE\\_PSI\\_MEMORY\\_INTERFACE=](#page-78-4)bool

Whether to enable the performance schema memory tracing module for memory allocation functions (ut::aligned\_name library functions) used in dynamic storage of over-aligned types.

<span id="page-78-5"></span>• [-DIGNORE\\_AIO\\_CHECK=](#page-78-5)bool

If the [-DBUILD\\_CONFIG=mysql\\_release](#page-70-0) option is given on Linux, the libaio library must be linked in by default. If you do not have libaio or do not want to install it, you can suppress the check for it by specifying [-DIGNORE\\_AIO\\_CHECK=1](#page-78-5).

<span id="page-78-6"></span>• [-DMAX\\_INDEXES=](#page-78-6)num

The maximum number of indexes per table. The default is 64. The maximum is 255. Values smaller than 64 are ignored and the default of 64 is used.

<span id="page-78-7"></span>• [-DMYSQL\\_MAINTAINER\\_MODE=](#page-78-7)bool

Whether to enable a MySQL maintainer-specific development environment. If enabled, this option causes compiler warnings to become errors.

<span id="page-79-7"></span>• [-DWITH\\_DEVELOPER\\_ENTITLEMENTS=](#page-79-7)bool

Whether to add the get-task-allow entitlement to all executables to generate a core dump in the event of an unexpected server halt.

On macOS 11+, core dumps are limited to processes with the com.apple.security.get-taskallow entitlement, which this CMake option enables. The entitlement allows other processes to attach and read/modify the processes memory, and allows --core-file to function as expected.

This option was added in MySQL 8.0.30.

<span id="page-79-2"></span>• [-DMUTEX\\_TYPE=](#page-79-2)type

The mutex type used by InnoDB. Options include:

- event: Use event mutexes. This is the default value and the original InnoDB mutex implementation.
- sys: Use POSIX mutexes on UNIX systems. Use CRITICAL\_SECTION objects on Windows, if available.
- futex: Use Linux futexes instead of condition variables to schedule waiting threads.
- <span id="page-79-3"></span>• [-DMYSQLX\\_TCP\\_PORT=](#page-79-3)port\_num

The port number on which X Plugin listens for TCP/IP connections. The default is 33060.

This value can be set at server startup with the mysqlx\_port system variable.

<span id="page-79-4"></span>• [-DMYSQLX\\_UNIX\\_ADDR=](#page-79-4)file\_name

The Unix socket file path on which the server listens for X Plugin socket connections. This must be an absolute path name. The default is /tmp/mysqlx.sock.

This value can be set at server startup with the mysqlx\_port system variable.

<span id="page-79-5"></span>• [-DMYSQL\\_PROJECT\\_NAME=](#page-79-5)name

For Windows or macOS, the project name to incorporate into the project file name.

<span id="page-79-0"></span>• [-DMYSQL\\_TCP\\_PORT=](#page-79-0)port\_num

The port number on which the server listens for TCP/IP connections. The default is 3306.

This value can be set at server startup with the --port option.

<span id="page-79-1"></span>• [-DMYSQL\\_UNIX\\_ADDR=](#page-79-1)file\_name

The Unix socket file path on which the server listens for socket connections. This must be an absolute path name. The default is /tmp/mysql.sock.

This value can be set at server startup with the --socket option.

<span id="page-79-6"></span>• [-DOPTIMIZER\\_TRACE=](#page-79-6)bool

Whether to support optimizer tracing. See Section 10.15, "Tracing the Optimizer".

<span id="page-80-0"></span>• [-DREPRODUCIBLE\\_BUILD=](#page-80-0)bool

For builds on Linux systems, this option controls whether to take extra care to create a build result independent of build location and time.

This option was added in MySQL 8.0.11. As of MySQL 8.0.12, it defaults to ON for RelWithDebInfo builds.

<span id="page-80-1"></span>• [-DSHOW\\_SUPPRESSED\\_COMPILER\\_WARNINGS=](#page-80-1)bool

Show suppressed compiler warnings, and do so without failing with -Werror. Defaults to OFF.

This option was added in MySQL 8.0.30.

<span id="page-80-8"></span>• [-DUSE\\_LD\\_GOLD=](#page-80-8)bool

GNU gold linker support was removed in MySQL 8.0.31; this CMake option was also removed.

CMake causes the build process to link with the GNU gold linker if it is available and not explicitly disabled. To disable use of this linker, specify the [-DUSE\\_LD\\_GOLD=OFF](#page-80-8) option.

<span id="page-80-2"></span>• [-DUSE\\_LD\\_LLD=](#page-80-2)bool

CMake causes the build process to link using the LLVM lld linker for Clang if it is available and not explicitly disabled. To disable use of this linker, specify the [-DUSE\\_LD\\_LLD=OFF](#page-80-2) option.

This option was added in MySQL 8.0.16.

<span id="page-80-3"></span>• [-DWIN\\_DEBUG\\_NO\\_INLINE=](#page-80-3)bool

Whether to disable function inlining on Windows. The default is OFF (inlining enabled).

<span id="page-80-4"></span>• [-DWITH\\_ANT=](#page-80-4)path\_name

Set the path to Ant, required when building GCS Java wrapper. Set [WITH\\_ANT](#page-80-4) to the path of a directory where the Ant tarball or unpacked archive is saved. When [WITH\\_ANT](#page-80-4) is not set, or is set with the special value system, the build process assumes a binary ant exists in \$PATH.

<span id="page-80-5"></span>• [-DWITH\\_ASAN=](#page-80-5)bool

Whether to enable the AddressSanitizer, for compilers that support it. The default is OFF.

<span id="page-80-6"></span>• [-DWITH\\_ASAN\\_SCOPE=](#page-80-6)bool

Whether to enable the AddressSanitizer -fsanitize-address-use-after-scope Clang flag for use-after-scope detection. The default is off. To use this option, -DWITH\_ASAN must also be enabled.

<span id="page-80-7"></span>• [-DWITH\\_AUTHENTICATION\\_CLIENT\\_PLUGINS=](#page-80-7)bool

This option is enabled automatically if any corresponding server authentication plugins are built. Its value thus depends on other CMake options and it should not be set explicitly.

This option was added in MySQL 8.0.26.

<span id="page-81-1"></span>• [-DWITH\\_AUTHENTICATION\\_LDAP=](#page-81-1)bool

Whether to report an error if the LDAP authentication plugins cannot be built:

- If this option is disabled (the default), the LDAP plugins are built if the required header files and libraries are found. If they are not, CMake displays a note about it.
- If this option is enabled, a failure to find the required header file and libraries causes CMake to produce an error, preventing the server from being built.

For information about LDAP authentication, see Section 8.4.1.7, "LDAP Pluggable Authentication".

<span id="page-81-2"></span>• [-DWITH\\_AUTHENTICATION\\_PAM=](#page-81-2)bool

Whether to build the PAM authentication plugin, for source trees that include this plugin. (See Section 8.4.1.5, "PAM Pluggable Authentication".) If this option is specified and the plugin cannot be compiled, the build fails.

<span id="page-81-3"></span>• [-DWITH\\_AWS\\_SDK=](#page-81-3)path\_name

The location of the Amazon Web Services software development kit.

<span id="page-81-0"></span>• [-DWITH\\_BOOST=](#page-81-0)path\_name

The Boost library is required to build MySQL. These CMake options enable control over the library source location, and whether to download it automatically:

- [-DWITH\\_BOOST=](#page-81-0)path\_name specifies the Boost library directory location. It is also possible to specify the Boost location by setting the BOOST\_ROOT or WITH\_BOOST environment variable.
  - [-DWITH\\_BOOST=system](#page-81-0) is also permitted and indicates that the correct version of Boost is installed on the compilation host in the standard location. In this case, the installed version of Boost is used rather than any version included with a MySQL source distribution.
- [-DDOWNLOAD\\_BOOST=](#page-77-3)bool specifies whether to download the Boost source if it is not present in the specified location. The default is OFF.
- [-DDOWNLOAD\\_BOOST\\_TIMEOUT=](#page-77-4)seconds the timeout in seconds for downloading the Boost library. The default is 600 seconds.

For example, if you normally build MySQL placing the object output in the bld subdirectory of your MySQL source tree, you can build with Boost like this:

```
mkdir bld
cd bld
cmake .. -DDOWNLOAD_BOOST=ON -DWITH_BOOST=$HOME/my_boost
```

This causes Boost to be downloaded into the my\_boost directory under your home directory. If the required Boost version is already there, no download is done. If the required Boost version changes, the newer version is downloaded.

If Boost is already installed locally and your compiler finds the Boost header files on its own, it may not be necessary to specify the preceding CMake options. However, if the version of Boost required by MySQL changes and the locally installed version has not been upgraded, you may have build problems. Using the CMake options should give you a successful build.

With the above settings that allow Boost download into a specified location, when the required Boost version changes, you need to remove the bld folder, recreate it, and perform the cmake step again. Otherwise, the new Boost version might not get downloaded, and compilation might fail.

<span id="page-82-1"></span>• [-DWITH\\_CLIENT\\_PROTOCOL\\_TRACING=](#page-82-1)bool

Whether to build the client-side protocol tracing framework into the client library. By default, this option is enabled.

For information about writing protocol trace client plugins, see [Writing Protocol Trace Plugins.](https://dev.mysql.com/doc/extending-mysql/8.0/en/writing-protocol-trace-plugins.md)

See also the [WITH\\_TEST\\_TRACE\\_PLUGIN](#page-87-4) option.

<span id="page-82-2"></span>• [-DWITH\\_CURL=](#page-82-2)curl\_type

The location of the curl library. curl\_type can be system (use the system curl library) or a path name to the curl library.

<span id="page-82-0"></span>• [-DWITH\\_DEBUG=](#page-82-0)bool

Whether to include debugging support.

Configuring MySQL with debugging support enables you to use the --debug="d,parser\_debug" option when you start the server. This causes the Bison parser that is used to process SQL statements to dump a parser trace to the server's standard error output. Typically, this output is written to the error log.

Sync debug checking for the InnoDB storage engine is defined under UNIV\_DEBUG and is available when debugging support is compiled in using the [WITH\\_DEBUG](#page-82-0) option. When debugging support is compiled in, the innodb\_sync\_debug configuration option can be used to enable or disable InnoDB sync debug checking.

Enabling [WITH\\_DEBUG](#page-82-0) also enables Debug Sync. This facility is used for testing and debugging. When compiled in, Debug Sync is disabled by default at runtime. To enable it, start mysqld with the --debug-sync-timeout=N option, where N is a timeout value greater than 0. (The default value is 0, which disables Debug Sync.) N becomes the default timeout for individual synchronization points.

Sync debug checking for the InnoDB storage engine is available when debugging support is compiled in using the [WITH\\_DEBUG](#page-82-0) option.

For a description of the Debug Sync facility and how to use synchronization points, see [MySQL](https://dev.mysql.com/doc/internals/en/test-synchronization.md) [Internals: Test Synchronization](https://dev.mysql.com/doc/internals/en/test-synchronization.md).

<span id="page-82-5"></span>• [-DWITH\\_DEFAULT\\_FEATURE\\_SET=](#page-82-5)bool

Whether to use the flags from cmake/build\_configurations/feature\_set.cmake. This option was removed in MySQL 8.0.22.

<span id="page-82-3"></span>• [-DWITH\\_EDITLINE=](#page-82-3)value

Which libedit/editline library to use. The permitted values are bundled (the default) and system.

<span id="page-82-4"></span>• [-DWITH\\_FIDO=](#page-82-4)fido\_type

The authentication\_fido authentication plugin is implemented using a FIDO library (see Section 8.4.1.11, "FIDO Pluggable Authentication"). The [WITH\\_FIDO](#page-82-4) option indicates the source of FIDO support:

• bundled: Use the FIDO library bundled with the distribution. This is the default.

As of MySQL 8.0.30, MySQL includes fido2 version 1.8.0. (Prior releases used fido2 1.5.0).

• system: Use the system FIDO library.

[WITH\\_FIDO](#page-82-4) is disabled (set to none) if all authentication plugins are disabled.

This option was added in MySQL 8.0.27.

<span id="page-83-5"></span>• [-DWITH\\_GMOCK=](#page-83-5)path\_name

The path to the googlemock distribution, for use with Google Test-based unit tests. The option value is the path to the distribution zip file. Alternatively, set the WITH\_GMOCK environment variable to the path name. It is also possible to use -DENABLE\_DOWNLOADS=1, so that CMake downloads the distribution from GitHub.

If you build MySQL without the Google Test unit tests (by configuring without [WITH\\_GMOCK](#page-83-5)), CMake displays a message indicating how to download it.

As of MySQL 8.0.26, MySQL source distributions bundle the Google Test source code. Consequently, as of that version, the [WITH\\_GMOCK](#page-83-5) and [ENABLE\\_DOWNLOADS](#page-77-9) CMake options are removed and are ignored if specified.

<span id="page-83-0"></span>• [-DWITH\\_ICU={](#page-83-0)icu\_type|path\_name}

MySQL uses International Components for Unicode (ICU) to support regular expression operations. The WITH\_ICU option indicates the type of ICU support to include or the path name to the ICU installation to use.

- icu\_type can be one of the following values:
  - bundled: Use the ICU library bundled with the distribution. This is the default, and is the only supported option for Windows.
  - system: Use the system ICU library.
- path\_name is the path name to the ICU installation to use. This can be preferable to using the icu\_type value of system because it can prevent CMake from detecting and using an older or incorrect ICU version installed on the system. (Another permitted way to do the same thing is to set WITH\_ICU to system and set the CMAKE\_PREFIX\_PATH option to path\_name.)
- <span id="page-83-1"></span>• [-DWITH\\_INNODB\\_EXTRA\\_DEBUG=](#page-83-1)bool

Whether to include extra InnoDB debugging support.

Enabling WITH\_INNODB\_EXTRA\_DEBUG turns on extra InnoDB debug checks. This option can only be enabled when [WITH\\_DEBUG](#page-82-0) is enabled.

<span id="page-83-2"></span>• [-DWITH\\_INNODB\\_MEMCACHED=](#page-83-2)bool

Whether to generate memcached shared libraries (libmemcached.so and innodb\_engine.so).

<span id="page-83-3"></span>• [-DWITH\\_JEMALLOC=](#page-83-3)bool

Whether to link with -ljemalloc. If enabled, built-in malloc(), calloc(), realloc(), and free() routines are disabled. The default is OFF.

[WITH\\_JEMALLOC](#page-83-3) and [WITH\\_TCMALLOC](#page-87-3) are mutually exclusive.

This option was added in MySQL 8.0.16.

<span id="page-83-4"></span>• [-DWITH\\_KEYRING\\_TEST=](#page-83-4)bool

Whether to build the test program that accompanies the keyring\_file plugin. The default is OFF. Test file source code is located in the plugin/keyring/keyring-test directory.

<span id="page-84-0"></span>• [-DWITH\\_LIBEVENT=](#page-84-0)string

Which libevent library to use. Permitted values are bundled (default) and system. Prior to MySQL 8.0.21, if you specify system, the system libevent library is used if present, and an error occurs otherwise. In MySQL 8.0.21 and later, if system is specified and no system libevent library can be found, an error occurs regardless, and the bundled libevent is not used.

The libevent library is required by InnoDB memcached, X Plugin, and MySQL Router.

<span id="page-84-1"></span>• [-DWITH\\_LIBWRAP=](#page-84-1)bool

Whether to include libwrap (TCP wrappers) support.

<span id="page-84-2"></span>• [-DWITH\\_LOCK\\_ORDER=](#page-84-2)bool

Whether to enable LOCK\_ORDER tooling. By default, this option is disabled and server builds contain no tooling. If tooling is enabled, the LOCK\_ORDER tool is available and can be used as described in Section 7.9.3, "The LOCK\_ORDER Tool".

![](_page_84_Picture_8.jpeg)

#### **Note**

With the [WITH\\_LOCK\\_ORDER](#page-84-2) option enabled, MySQL builds require the flex program.

This option was added in MySQL 8.0.17.

<span id="page-84-3"></span>• [-DWITH\\_LSAN=](#page-84-3)bool

Whether to run LeakSanitizer, without AddressSanitizer. The default is OFF.

This option was added in MySQL 8.0.16.

<span id="page-84-4"></span>• [-DWITH\\_LTO=](#page-84-4)bool

Whether to enable the link-time optimizer, if the compiler supports it. The default is OFF unless [FPROFILE\\_USE](#page-78-3) is enabled.

This option was added in MySQL 8.0.13.

<span id="page-84-5"></span>• [-DWITH\\_LZ4=](#page-84-5)lz4\_type

The [WITH\\_LZ4](#page-84-5) option indicates the source of zlib support:

- bundled: Use the lz4 library bundled with the distribution. This is the default.
- system: Use the system lz4 library. If [WITH\\_LZ4](#page-84-5) is set to this value, the lz4\_decompress utility is not built. In this case, the system lz4 command can be used instead.
- <span id="page-84-7"></span>• [-DWITH\\_LZMA=](#page-84-7)lzma\_type

The type of LZMA library support to include. lzma\_type can be one of the following values:

- bundled: Use the LZMA library bundled with the distribution. This is the default.
- system: Use the system LZMA library.

This option was removed in MySQL 8.0.16.

<span id="page-84-6"></span>• [-DWITH\\_MECAB={disabled|system|](#page-84-6)path\_name}

Use this option to compile the MeCab parser. If you have installed MeCab to its default installation directory, set -DWITH\_MECAB=system. The system option applies to MeCab installations performed from source or from binaries using a native package management utility. If you installed MeCab to a custom installation directory, specify the path to the MeCab installation, for example, - DWITH\_MECAB=/opt/mecab. If the system option does not work, specifying the MeCab installation path should work in all cases.

For related information, see Section 14.9.9, "MeCab Full-Text Parser Plugin".

<span id="page-85-1"></span>• [-DWITH\\_MSAN=](#page-85-1)bool

Whether to enable MemorySanitizer, for compilers that support it. The default is off.

For this option to have an effect if enabled, all libraries linked to MySQL must also have been compiled with the option enabled.

<span id="page-85-2"></span>• [-DWITH\\_MSCRT\\_DEBUG=](#page-85-2)bool

Whether to enable Visual Studio CRT memory leak tracing. The default is OFF.

<span id="page-85-0"></span>• [-DMSVC\\_CPPCHECK=](#page-85-0)bool

Whether to enable MSVC code analysis. The default is OFF.

<span id="page-85-3"></span>• [-DWITH\\_MYSQLX=](#page-85-3)bool

Whether to build with support for X Plugin. The default is ON. See Chapter 22, Using MySQL as a Document Store.

<span id="page-85-4"></span>• [-DWITH\\_NUMA=](#page-85-4)bool

Explicitly set the NUMA memory allocation policy. CMake sets the default [WITH\\_NUMA](#page-85-4) value based on whether the current platform has NUMA support. For platforms without NUMA support, CMake behaves as follows:

- With no NUMA option (the normal case), CMake continues normally, producing only this warning: NUMA library missing or required version not available.
- With [-DWITH\\_NUMA=ON](#page-85-4), CMake aborts with this error: NUMA library missing or required version not available.
- <span id="page-85-5"></span>• [-DWITH\\_PACKAGE\\_FLAGS=](#page-85-5)bool

For flags typically used for RPM and Debian packages, whether to add them to standalone builds on those platforms. The default is ON for nondebug builds.

This option was added in MySQL 8.0.26.

<span id="page-85-6"></span>• [-DWITH\\_PROTOBUF=](#page-85-6)protobuf\_type

Which Protocol Buffers package to use. protobuf\_type can be one of the following values:

- bundled: Use the package bundled with the distribution. This is the default. Optionally use [INSTALL\\_PRIV\\_LIBDIR](#page-72-7) to modify the dynamic Protobuf library directory.
- system: Use the package installed on the system.

Other values are ignored, with a fallback to bundled.

<span id="page-85-7"></span>• [-DWITH\\_RAPID=](#page-85-7)bool

Whether to build the rapid development cycle plugins. When enabled, a rapid directory is created in the build tree containing these plugins. When disabled, no rapid directory is created in the build tree. The default is ON, unless the rapid directory is removed from the source tree, in which case the default becomes OFF.

<span id="page-86-1"></span>• [-DWITH\\_RAPIDJSON=](#page-86-1)rapidjson\_type

The type of RapidJSON library support to include. rapidjson\_type can be one of the following values:

- bundled: Use the RapidJSON library bundled with the distribution. This is the default.
- system: Use the system RapidJSON library. Version 1.1.0 or later is required.

This option was added in MySQL 8.0.13.

<span id="page-86-4"></span>• [-DWITH\\_RE2=](#page-86-4)re2\_type

The type of RE2 library support to include. re2\_type can be one of the following values:

- bundled: Use the RE2 library bundled with the distribution. This is the default.
- system: Use the system RE2 library.

As of MySQL 8.0.18, MySQL no longer uses the RE2 library, and this option has been removed.

<span id="page-86-2"></span>• [-DWITH\\_ROUTER=](#page-86-2)bool

Whether to build MySQL Router. The default is ON.

This option was added in MySQL 8.0.16.

<span id="page-86-3"></span>• [-DWITH\\_SASL=](#page-86-3)value

Internal use only. This option was added in 8.0.20. Not supported on Windows.

<span id="page-86-0"></span>• [-DWITH\\_SSL={](#page-86-0)ssl\_type|path\_name}

For support of encrypted connections, entropy for random number generation, and other encryptionrelated operations, MySQL must be built using an SSL library. This option specifies which SSL library to use.

- ssl\_type can be one of the following values:
  - system: Use the system OpenSSL library. This is the default.

On macOS and Windows, using system configures MySQL to build as if CMake was invoked with path\_name points to a manually installed OpenSSL library. This is because they do not have system SSL libraries. On macOS, brew install openssl installs to /usr/local/opt/ openssl so that system can find it. On Windows, it checks %ProgramFiles%/OpenSSL, %ProgramFiles%/OpenSSL-Win32, %ProgramFiles%/OpenSSL-Win64, C:/OpenSSL, C:/OpenSSL-Win32, and C:/OpenSSL-Win64.

- yes: This is a synonym for system.
- opensslversion: (MySQL 8.0.30 and later:) Use an alternate OpenSSL system package such as openssl11 on EL7, or openssl3 on EL8.

Authentication plugins, such as LDAP and Kerberos, are disabled as they do not support these alternative versions of OpenSSL.

• path\_name is the path name to the OpenSSL installation to use. This can be preferable to using the ssl\_type value of system because it can prevent CMake from detecting and using an older or incorrect OpenSSL version installed on the system. (Another permitted way to do the same thing is to set WITH\_SSL to system and set the CMAKE\_PREFIX\_PATH option to path\_name.)

For additional information about configuring the SSL library, see [Section 2.8.6, "Configuring SSL](#page-62-0) [Library Support".](#page-62-0)

<span id="page-87-0"></span>• [-DWITH\\_SYSTEMD=](#page-87-0)bool

Whether to enable installation of systemd support files. By default, this option is disabled. When enabled, systemd support files are installed, and scripts such as mysqld\_safe and the System V initialization script are not installed. On platforms where systemd is not available, enabling [WITH\\_SYSTEMD](#page-87-0) results in an error from CMake.

For more information about using systemd, see [Section 2.5.9, "Managing MySQL Server with](#page-47-0) [systemd".](#page-47-0) That section also includes information about specifying options otherwise specified in [mysqld\_safe] option groups. Because mysqld\_safe is not installed when systemd is used, such options must be specified another way.

<span id="page-87-2"></span>• [-DWITH\\_SYSTEM\\_LIBS=](#page-87-2)bool

This option serves as an "umbrella" option to set the system value of any of the following CMake options that are not set explicitly: [WITH\\_CURL](#page-82-2), [WITH\\_EDITLINE](#page-82-3), [WITH\\_FIDO](#page-82-4), [WITH\\_ICU](#page-83-0), [WITH\\_LIBEVENT](#page-84-0), [WITH\\_LZ4](#page-84-5), [WITH\\_LZMA](#page-84-7), [WITH\\_PROTOBUF](#page-85-6), [WITH\\_RE2](#page-86-4), [WITH\\_SSL](#page-86-0), [WITH\\_ZSTD](#page-88-7).

[WITH\\_ZLIB](#page-88-6) was included here priot MySQL 8.0.30.

<span id="page-87-1"></span>• [-DWITH\\_SYSTEMD\\_DEBUG=](#page-87-1)bool

Whether to produce additional systemd debugging information, for platforms on which systemd is used to run MySQL. The default is OFF.

This option was added in MySQL 8.0.22.

<span id="page-87-3"></span>• [-DWITH\\_TCMALLOC=](#page-87-3)bool

Whether to link with -ltcmalloc. If enabled, built-in malloc(), calloc(), realloc(), and free() routines are disabled. The default is OFF.

Beginning with MySQL 8.0.38, a tcmalloc library is included in the source; you can cause the build to use the bundled version by setting this option to BUNDLED. BUNDLED is supported on Linux systems only.

[WITH\\_TCMALLOC](#page-87-3) and [WITH\\_JEMALLOC](#page-83-3) are mutually exclusive.

This option was added in MySQL 8.0.22.

<span id="page-87-4"></span>• [-DWITH\\_TEST\\_TRACE\\_PLUGIN=](#page-87-4)bool

Whether to build the test protocol trace client plugin (see [Using the Test Protocol Trace](https://dev.mysql.com/doc/extending-mysql/8.0/en/test-protocol-trace-plugin.md) [Plugin\)](https://dev.mysql.com/doc/extending-mysql/8.0/en/test-protocol-trace-plugin.md). By default, this option is disabled. Enabling this option has no effect unless the [WITH\\_CLIENT\\_PROTOCOL\\_TRACING](#page-82-1) option is enabled. If MySQL is configured with both options enabled, the libmysqlclient client library is built with the test protocol trace plugin built in, and all the standard MySQL clients load the plugin. However, even when the test plugin is enabled, it has no effect by default. Control over the plugin is afforded using environment variables; see [Using the Test](https://dev.mysql.com/doc/extending-mysql/8.0/en/test-protocol-trace-plugin.md) [Protocol Trace Plugin.](https://dev.mysql.com/doc/extending-mysql/8.0/en/test-protocol-trace-plugin.md)

![](_page_87_Picture_19.jpeg)

#### **Note**

Do not enable the [WITH\\_TEST\\_TRACE\\_PLUGIN](#page-87-4) option if you want to use your own protocol trace plugins because only one such plugin can be loaded at a time and an error occurs for attempts to load a second one. If you have already built MySQL with the test protocol trace plugin enabled to see how

it works, you must rebuild MySQL without it before you can use your own plugins.

For information about writing trace plugins, see [Writing Protocol Trace Plugins](https://dev.mysql.com/doc/extending-mysql/8.0/en/writing-protocol-trace-plugins.md).

<span id="page-88-0"></span>• [-DWITH\\_TSAN=](#page-88-0)bool

Whether to enable the ThreadSanitizer, for compilers that support it. The default is off.

<span id="page-88-1"></span>• [-DWITH\\_UBSAN=](#page-88-1)bool

Whether to enable the Undefined Behavior Sanitizer, for compilers that support it. The default is off.

<span id="page-88-2"></span>• [-DWITH\\_UNIT\\_TESTS={ON|OFF}](#page-88-2)

If enabled, compile MySQL with unit tests. The default is ON unless the server is not being compiled.

<span id="page-88-3"></span>• [-DWITH\\_UNIXODBC=](#page-88-3)1

Enables unixODBC support, for Connector/ODBC.

<span id="page-88-4"></span>• [-DWITH\\_VALGRIND=](#page-88-4)bool

Whether to compile in the Valgrind header files, which exposes the Valgrind API to MySQL code. The default is OFF.

To generate a Valgrind-aware debug build, [-DWITH\\_VALGRIND=1](#page-88-4) normally is combined with [-](#page-82-0) [DWITH\\_DEBUG=1](#page-82-0). See [Building Debug Configurations](https://dev.mysql.com/doc/internals/en/debug-configurations.md).

<span id="page-88-5"></span>• [-DWITH\\_WIN\\_JEMALLOC=](#page-88-5)string

On Windows, pass in a path to a directory containing jemalloc.dll to enable jemalloc functionality. The build system copies jemalloc.dll to the same directory as mysqld.exe and/ or mysqld-debug.exe and utilizes it for memory management operations. Standard memory functions are used if jemalloc.dll is not found or does not export the required functions. An INFORMATION level log message records whether or not jemalloc is found and used.

This option is enabled for official MySQL binaries for Windows.

This option was added in MySQL 8.0.29.

<span id="page-88-6"></span>• [-DWITH\\_ZLIB=](#page-88-6)zlib\_type

Some features require that the server be built with compression library support, such as the COMPRESS() and UNCOMPRESS() functions, and compression of the client/server protocol. The [WITH\\_ZLIB](#page-88-6) option indicates the source of zlib support:

In MYSQL 8.0.32 and later, the minimum supported version of zlib is 1.2.13.

- bundled: Use the zlib library bundled with the distribution. This is the default.
- system: Use the system zlib library. If [WITH\\_ZLIB](#page-88-6) is set to this value, the zlib\_decompress utility is not built. In this case, the system openssl zlib command can be used instead.
- <span id="page-88-7"></span>• [-DWITH\\_ZSTD=](#page-88-7)zstd\_type

Connection compression using the zstd algorithm (see Section 6.2.8, "Connection Compression Control") requires that the server be built with zstd library support. The [WITH\\_ZSTD](#page-88-7) option indicates the source of zstd support:

- bundled: Use the zstd library bundled with the distribution. This is the default.
- system: Use the system zstd library.

This option was added in MySQL 8.0.18.

<span id="page-89-5"></span>• [-DWITHOUT\\_SERVER=](#page-89-5)bool

Whether to build without MySQL Server. The default is OFF, which does build the server.

This is considered an experimental option; it is preferred to build with the server.

This option also prevents building of the NDB storage engine or any NDB binaries including management and data node programs.

## <span id="page-89-3"></span><span id="page-89-0"></span>**Compiler Flags**

• [-DCMAKE\\_C\\_FLAGS="](#page-89-3)flags"

Flags for the C compiler.

<span id="page-89-2"></span>• [-DCMAKE\\_CXX\\_FLAGS="](#page-89-2)flags"

Flags for the C++ compiler.

<span id="page-89-6"></span>• [-DWITH\\_DEFAULT\\_COMPILER\\_OPTIONS=](#page-89-6)bool

Whether to use the flags from cmake/build\_configurations/compiler\_options.cmake.

![](_page_89_Picture_13.jpeg)

#### **Note**

All optimization flags are carefully chosen and tested by the MySQL build team. Overriding them can lead to unexpected results and is done at your own risk.

<span id="page-89-4"></span>• [-DOPTIMIZE\\_SANITIZER\\_BUILDS=](#page-89-4)bool

Whether to add -O1 -fno-inline to sanitizer builds. The default is ON.

To specify your own C and C++ compiler flags, for flags that do not affect optimization, use the [CMAKE\\_C\\_FLAGS](#page-89-3) and [CMAKE\\_CXX\\_FLAGS](#page-89-2) CMake options.

When providing your own compiler flags, you might want to specify [CMAKE\\_BUILD\\_TYPE](#page-70-3) as well.

For example, to create a 32-bit release build on a 64-bit Linux machine, do this:

```
$> mkdir build
$> cd build
$> cmake .. -DCMAKE_C_FLAGS=-m32 \
 -DCMAKE_CXX_FLAGS=-m32 \
 -DCMAKE_BUILD_TYPE=RelWithDebInfo
```

If you set flags that affect optimization (-Onumber), you must set the CMAKE\_C\_FLAGS\_build\_type and/or CMAKE\_CXX\_FLAGS\_build\_type options, where build\_type corresponds to the [CMAKE\\_BUILD\\_TYPE](#page-70-3) value. To specify a different optimization for the default build type (RelWithDebInfo) set the CMAKE\_C\_FLAGS\_RELWITHDEBINFO and CMAKE\_CXX\_FLAGS\_RELWITHDEBINFO options. For example, to compile on Linux with -O3 and with debug symbols, do this:

```
$> cmake .. -DCMAKE_C_FLAGS_RELWITHDEBINFO="-O3 -g" \
 -DCMAKE_CXX_FLAGS_RELWITHDEBINFO="-O3 -g"
```

### <span id="page-89-1"></span>**CMake Options for Compiling NDB Cluster**

To compile with support for NDB Cluster, you can use [-DWITH\\_NDB](#page-90-3), which causes the build to include the NDB storage engine and all NDB programs. This option is enabled by default. To prevent building

of the NDB storage engine plugin, use [-DWITH\\_NDBCLUSTER\\_STORAGE\\_ENGINE=OFF](#page-90-6). Other aspects of the build can be controlled using the other options listed in this section.

The following options apply when building the MySQL sources with NDB Cluster support.

<span id="page-90-7"></span>• [-DMEMCACHED\\_HOME=](#page-90-7)dir\_name

NDB support for memcached was removed in NDB 8.0.23; thus, this option is no longer supported for building NDB in this or later versions.

<span id="page-90-0"></span>• [-DNDB\\_UTILS\\_LINK\\_DYNAMIC={ON|OFF}](#page-90-0)

Controls whether NDB utilities such as ndb\_drop\_table are linked with ndbclient statically (OFF) or dynamically (ON); OFF (static linking) is the default. Normally static linking is used when building these to avoid problems with LD\_LIBRARY\_PATH, or when multiple versions of ndbclient are installed. This option is intended for creating Docker images and possibly other cases in which the target environment is subject to precise control and it is desirable to reduce image size.

Added in NDB 8.0.22.

<span id="page-90-8"></span>• [-DWITH\\_BUNDLED\\_LIBEVENT={ON|OFF}](#page-90-8)

NDB support for memcached was removed in NDB 8.0.23; thus, this option is no longer supported for building NDB in this or later versions.

<span id="page-90-9"></span>• [-DWITH\\_BUNDLED\\_MEMCACHED={ON|OFF}](#page-90-9)

NDB support for memcached was removed in NDB 8.0.23; thus, this option is no longer supported for building NDB in this or later versions.

<span id="page-90-1"></span>• [-DWITH\\_CLASSPATH=](#page-90-1)path

Sets the classpath for building MySQL NDB Cluster Connector for Java. The default is empty. This option is ignored if [-DWITH\\_NDB\\_JAVA=OFF](#page-91-3) is used.

<span id="page-90-2"></span>• [-DWITH\\_ERROR\\_INSERT={ON|OFF}](#page-90-2)

Enables error injection in the NDB kernel. For testing only; not intended for use in building production binaries. The default is OFF.

<span id="page-90-3"></span>• [-DWITH\\_NDB={ON|OFF}](#page-90-3)

Build MySQL NDB Cluster; build the NDB plugin and all NDB Cluster programs.

Added in NDB 8.0.31.

<span id="page-90-4"></span>• [-DWITH\\_NDBAPI\\_EXAMPLES={ON|OFF}](#page-90-4)

Build NDB API example programs in storage/ndb/ndbapi-examples/. See [NDB API](https://dev.mysql.com/doc/ndbapi/en/ndb-examples.md) [Examples,](https://dev.mysql.com/doc/ndbapi/en/ndb-examples.md) for information about these.

<span id="page-90-6"></span>• [-DWITH\\_NDBCLUSTER\\_STORAGE\\_ENGINE={ON|OFF}](#page-90-6)

NDB 8.0.30 and earlier: For internal use only; may not always work as expected. To build with NDB support, use [WITH\\_NDBCLUSTER](#page-90-5) instead.

NDB 8.0.31 and later: Controls (only) whether the NDBCLUSTER storage engine is included in the build; [WITH\\_NDB](#page-90-3) enables this option automatically, so it is recommended that you use WITH\_NDB instead.

<span id="page-90-5"></span>• [-DWITH\\_NDBCLUSTER={ON|OFF}](#page-90-5) (DEPRECATED)

Build and link in support for the NDB storage engine in mysqld.

This option is deprecated as of NDB 8.0.31, and subject to eventual removal; use [WITH\\_NDB](#page-90-3) instead.

<span id="page-91-1"></span>• [-DWITH\\_NDBMTD={ON|OFF}](#page-91-1)

Build the multithreaded data node executable ndbmtd. The default is ON.

<span id="page-91-2"></span>• [-DWITH\\_NDB\\_DEBUG={ON|OFF}](#page-91-2)

Enable building the debug versions of the NDB Cluster binaries. This is OFF by default.

<span id="page-91-3"></span>• [-DWITH\\_NDB\\_JAVA={ON|OFF}](#page-91-3)

Enable building NDB Cluster with Java support, including support for ClusterJ (see [MySQL NDB](https://dev.mysql.com/doc/ndbapi/en/mccj.md) [Cluster Connector for Java\)](https://dev.mysql.com/doc/ndbapi/en/mccj.md).

This option is ON by default. If you do not wish to compile NDB Cluster with Java support, you must disable it explicitly by specifying -DWITH\_NDB\_JAVA=OFF when running CMake. Otherwise, if Java cannot be found, configuration of the build fails.

<span id="page-91-4"></span>• [-DWITH\\_NDB\\_PORT=](#page-91-4)port

Causes the NDB Cluster management server (ndb\_mgmd) that is built to use this port by default. If this option is unset, the resulting management server tries to use port 1186 by default.

<span id="page-91-5"></span>• [-DWITH\\_NDB\\_TEST={ON|OFF}](#page-91-5)

If enabled, include a set of NDB API test programs. The default is OFF.

<span id="page-91-6"></span>• [-DWITH\\_PLUGIN\\_NDBCLUSTER={ON|OFF}](#page-91-6)

For internal use only; may not always work as expected. This option was removed in NDB 8.0.31; use [WITH\\_NDB](#page-90-3) instead to build MySQL NDB Cluster. (NDB 8.0.30 and earlier: Use [WITH\\_NDBCLUSTER](#page-90-5).)

# <span id="page-91-0"></span>**2.8.8 Dealing with Problems Compiling MySQL**

The solution to many problems involves reconfiguring. If you do reconfigure, take note of the following:

- If CMake is run after it has previously been run, it may use information that was gathered during its previous invocation. This information is stored in CMakeCache.txt. When CMake starts, it looks for that file and reads its contents if it exists, on the assumption that the information is still correct. That assumption is invalid when you reconfigure.
- Each time you run CMake, you must run make again to recompile. However, you may want to remove old object files from previous builds first because they were compiled using different configuration options.

To prevent old object files or configuration information from being used, run the following commands before re-running CMake:

On Unix:

```
$> make clean
$> rm CMakeCache.txt
```

On Windows:

```
$> devenv MySQL.sln /clean
$> del CMakeCache.txt
```

If you build outside of the source tree, remove and recreate your build directory before re-running CMake. For instructions on building outside of the source tree, see [How to Build MySQL Server with](https://dev.mysql.com/doc/internals/en/cmake.md) [CMake.](https://dev.mysql.com/doc/internals/en/cmake.md)

On some systems, warnings may occur due to differences in system include files. The following list describes other problems that have been found to occur most often when compiling MySQL:

• To define which C and C++ compilers to use, you can define the CC and CXX environment variables. For example:

```
$> CC=gcc
$> CXX=g++
$> export CC CXX
```

While this can be done on the command line, as just shown, you may prefer to define these values in a build script, in which case the export command is not needed.

To specify your own C and C++ compiler flags, use the [CMAKE\\_C\\_FLAGS](#page-89-3) and [CMAKE\\_CXX\\_FLAGS](#page-89-2) CMake options. See [Compiler Flags](#page-89-0).

To see what flags you might need to specify, invoke mysql\_config with the --cflags and - cxxflags options.

- To see what commands are executed during the compile stage, after using CMake to configure MySQL, run make VERBOSE=1 rather than just make.
- If compilation fails, check whether the [MYSQL\\_MAINTAINER\\_MODE](#page-78-7) option is enabled. This mode causes compiler warnings to become errors, so disabling it may enable compilation to proceed.
- If your compile fails with errors such as any of the following, you must upgrade your version of make to GNU make:

```
make: Fatal error in reader: Makefile, line 18:
Badly formed macro assignment
Or:
make: file `Makefile' line 18: Must be a separator (:
Or:
pthread.h: No such file or directory
```

Solaris and FreeBSD are known to have troublesome make programs.

GNU make 3.75 is known to work.

• The sql\_yacc.cc file is generated from sql\_yacc.yy. Normally, the build process does not need to create sql\_yacc.cc because MySQL comes with a pregenerated copy. However, if you do need to re-create it, you might encounter this error:

```
"sql_yacc.yy", line xxx fatal: default action causes potential...
```

This is a sign that your version of yacc is deficient. You probably need to install a recent version of bison (the GNU version of yacc) and use that instead.

Versions of bison older than 1.75 may report this error:

```
sql_yacc.yy:#####: fatal error: maximum table size (32767) exceeded
```

The maximum table size is not actually exceeded; the error is caused by bugs in older versions of bison.

For information about acquiring or updating tools, see the system requirements in [Section 2.8,](#page-54-0) ["Installing MySQL from Source"](#page-54-0).