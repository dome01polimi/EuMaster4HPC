#!/bin/bash

source /share/env/module_select.sh
cd && cd qmecha_beta/code
ml CMake FJSVstclanga
cmake -B build_arm_fujitsu -S . -DBLAS_LAPACK_VENDOR:String=Fujitsu_SSL2BLAMP -DCMAKE_Fortran_COMPILER=/opt/FJSVstclanga/cp-1.0.21.02a/bin/mpifrtpx -DCMAKE_Fortran_FLAGS="${CMAKE_Fortran_FLAGS} -Cpp"
cmake --build build_arm_fujitsu --target all
cmake --install build_arm_fujitsu --prefix ~/opt/arm/Fujitsu/QMeCha
ml purge
rm -rf build_arm_fujitsu