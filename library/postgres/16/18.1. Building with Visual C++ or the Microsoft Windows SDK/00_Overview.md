---
source: PostgreSQL 16 Reference
title: 00_Overview
---

PostgreSQL can be built using the Visual C++ compiler suite from Microsoft. These compilers can be either from Visual Studio, Visual Studio Express or some versions of the Microsoft Windows SDK. If you do not already have a Visual Studio environment set up, the easiest ways are to use the compilers from Visual Studio 2022 or those in the Windows SDK 10, which are both free downloads from Microsoft.

Both 32-bit and 64-bit builds are possible with the Microsoft Compiler suite. 32-bit PostgreSQL builds are possible with Visual Studio 2015 to Visual Studio 2022, as well as standalone Windows SDK releases 10 and above. 64-bit PostgreSQL builds are supported with Microsoft Windows SDK version 10 and above or Visual Studio 2015 and above.

The tools for building using Visual C++ or Platform SDK are in the src\tools\msvc directory. When building, make sure there are no tools from MinGW or Cygwin present in your system PATH. Also, make sure you have all the required Visual C++ tools available in the PATH. In Visual Studio, start the Visual Studio Command Prompt. If you wish to build a 64-bit version, you must use the 64-bit version of the command, and vice versa. Starting with Visual Studio 2017 this can be done from the command line using VsDevCmd.bat, see -help for the available options and their default values. vsvars32.bat is available in Visual Studio 2015 and earlier versions for the same purpose. From the Visual Studio Command Prompt, you can change the targeted CPU architecture, build type, and target OS by using the vcvarsall.bat command, e.g., vcvarsall.bat x64 10.0.10240.0 to target Windows 10 with a 64-bit release build. See -help for the other options of vcvarsall.bat. All commands should be run from the src\tools\msvc directory.

Before you build, you can create the file config.pl to reflect any configuration options you want to change, or the paths to any third party libraries to use. The complete configuration is determined by first reading and parsing the file config\_default.pl, and then apply any changes from config.pl. For example, to specify the location of your Python installation, put the following in config.pl:

#### Installation from Source Code on Windows

```
$config->{python} = 'c:\python310';
```

You only need to specify those parameters that are different from what's in config\_default.pl.

If you need to set any other environment variables, create a file called buildenv.pl and put the required commands there. For example, to add the path for bison when it's not in the PATH, create a file containing:

```
$ENV{PATH}=$ENV{PATH} . ';c:\some\where\bison\bin';
```

To pass additional command line arguments to the Visual Studio build command (msbuild or vcbuild):

```
$ENV{MSBFLAGS}="/m";
```