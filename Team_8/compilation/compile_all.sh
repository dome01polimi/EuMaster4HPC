#!/bin/bash

# Define the scripts to be called
scripts=(
    "compile_arm_GNU"
    "compile_x86_GNU"
    "compile_x86_Intel"
)

echo "==============================================="
for script in "${scripts[@]}"; do
    echo "-----------------------------------------------"
    echo "Starting ${script}"
    sbatch ./"${script}.sh" > "${script}.out"
    echo -e "Please find the compilation output in:\n${script}.out."
    echo "-----------------------------------------------"
done
echo "Starting compile_arm_Fujitsu"
./compile_arm_Fujitsu.sh > compile_arm_Fujitsu.out 2> compile_arm_Fujitsu.err
echo -e "Please find the compilation output in:\ncompile_arm_Fujitsu.out."
echo "-----------------------------------------------"
echo "==============================================="
