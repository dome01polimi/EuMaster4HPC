#!/bin/bash
#SBATCH --job-name=compile_arm_x86
#SBATCH --account=eehpc-dev-2024d08-066x
#SBATCH --time=00:30:00
#SBATCH --partition=normal-x86
#SBATCH --nodes=1
#SBATCH --output=compile_x86_Intel.out
#SBATCH --error=compile_x86_Intel.err

source /share/env/module_select.sh
cd && cd qmecha_beta/code
sed -i 's/project(QMeCha VERSION 0\.1\.0 LANGUAGES Fortran)/project(QMeCha VERSION 0.1.0 LANGUAGES Fortran C)/' CMakeLists.txt
ml CMake intel
source /eb/x86_64/software/imkl/2024.2.0/mkl/2024.2/env/vars.sh intel64
cd && cd qmecha_beta/code
cmake -B build_x86_Intel -S .  -DBLAS_LAPACK_VENDOR:String=Intel10_64lp -DCMAKE_Fortran_COMPILER=/eb/x86_64/software/impi/2021.13.0-intel-compilers-2024.2.0/mpi/2021.13/bin/mpiifort
cmake --build build_x86_Intel --target all
cmake --install build_x86_Intel --prefix ~/opt/x86/Intel/QMeCha 
ml purge
sed -i 's/project(QMeCha VERSION 0\.1\.0 LANGUAGES Fortran C)/project(QMeCha VERSION 0.1.0 LANGUAGES Fortran)/' CMakeLists.txt
rm -rf build_x86_Intel