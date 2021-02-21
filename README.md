[![GCC Conan](https://github.com/sintef-ocean/conan-coinmetis/workflows/GCC%20Conan/badge.svg)](https://github.com/sintef-ocean/conan-coinmetis/actions?query=workflow%3A"GCC+Conan")
[![Clang Conan](https://github.com/sintef-ocean/conan-coinmetis/workflows/Clang%20Conan/badge.svg)](https://github.com/sintef-ocean/conan-coinmetis/actions?query=workflow%3A"Clang+Conan")
[![MSVC Conan](https://github.com/sintef-ocean/conan-coinmetis/workflows/MSVC%20Conan/badge.svg)](https://github.com/sintef-ocean/conan-coinmetis/actions?query=workflow%3A"MSVC+Conan")
[![Download](https://api.bintray.com/packages/sintef-ocean/conan/coinmetis%3Asintef/images/download.svg)](https://bintray.com/sintef-ocean/conan/coinmetis%3Asintef/_latestVersion)


[Conan.io](https://conan.io) recipe for [metis](http://glaros.dtc.umn.edu/gkhome/metis/metis/overview).

This recipe is made with the help of `coin-or` builder repository [ThirdParty-metis](https://github.com/coin-or-tools/ThirdParty-Metis).
The recipe generates library packages, which can be found at [Bintray](https://bintray.com/sintef-ocean/conan/coinmetis%3Asintef).
The package is usually consumed using the `conan install` command or a *conanfile.txt*.

## How to use this package

1. Add remote to conan's package [registry.txt](http://docs.conan.io/en/latest/reference/config_files/registry.txt.html):

   ```bash
   $ conan remote add sintef https://api.bintray.com/conan/sintef-ocean/conan
   ```

2. Using *conanfile.txt* in your project with *cmake*

   Add a [*conanfile.txt*](http://docs.conan.io/en/latest/reference/conanfile_txt.html) to your project. This file describes dependencies and your configuration of choice, e.g.:

   ```
   [requires]
   coinmetis/[>=4.0.3]@sintef/stable

   [options]
   coinmetis:shared=False

   [imports]
   licenses, * -> ./licenses @ folder=True

   [generators]
   cmake_paths
   cmake_find_package
   ```

   Insert into your *CMakeLists.txt* something like the following lines:
   ```cmake
   cmake_minimum_required(VERSION 3.13)
   project(TheProject CXX)

   include(${CMAKE_BINARY_DIR}/conan_paths.cmake)
   find_package(coinmetis MODULE REQUIRED)

   add_executable(the_executor code.cpp)
   target_link_libraries(the_executor coinmetis::coinmetis)
   ```
   Then, do
   ```bash
   $ mkdir build && cd build
   $ conan install .. -s build_type=<build_type>
   ```
   where `<build_type>` is e.g. `Debug` or `Release`.
   You can now continue with the usual dance with cmake commands for configuration and compilation. For details on how to use conan, please consult [Conan.io docs](http://docs.conan.io/en/latest/)

## Package options

Option | Default | Values
---|---|---
shared  | True | [True, False]
fPIC | True | [True, False]

## Known recipe issues

- This packages is built with the help of `msys2` and `automake`.
- The package does not include a `test_package` and may not work as intended.
