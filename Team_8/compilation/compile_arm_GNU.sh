#!/bin/bash
#SBATCH --job-name=compile_arm_gnu
#SBATCH --account=eehpc-dev-2024d08-066a 
#SBATCH --time=00:30:00
#SBATCH --partition=normal-arm
#SBATCH --nodes=1
#SBATCH --output=compile_arm_GNU.out
#SBATCH --error=compile_arm_GNU.err


source /share/env/module_select.sh
cd && cd qmecha_beta/code
ml CMake foss/2023a
cmake -B build_arm_GNU -S . -DBLAS_LAPACK_VENDOR:String=OpenBLAS
cmake --build build_arm_GNU --target all
cmake --install build_arm_GNU --prefix ~/opt/arm/GNU/QMeCha
ml purge
rm -rf build_arm_GNU