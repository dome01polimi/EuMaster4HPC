#!/bin/bash
#SBATCH --job-name=compile_arm_x86
#SBATCH --account=eehpc-dev-2024d08-066x
#SBATCH --time=00:30:00
#SBATCH --partition=normal-x86
#SBATCH --nodes=1
#SBATCH --output=compile_x86_GNU.out
#SBATCH --error=compile_x86_GNU.err


source /share/env/module_select.sh
cd && cd qmecha_beta/code
ml CMake foss/2023a
cd && cd qmecha_beta/code
cmake -B build_x86_GNU -S . -DBLAS_LAPACK_VENDOR:String=OpenBLAS
cmake --build build_x86_GNU --target all
cmake --install build_x86_GNU --prefix ~/opt/x86/GNU/QMeCha
ml purge
rm -rf build_x86_GNU