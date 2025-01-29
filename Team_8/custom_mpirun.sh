source /share/env/module_select.sh
substring_intel="Intel"
substring_GNU="GNU"
num_nodes=$1
shift
num_tasks_per_node=$1
shift
prog_name=$1
shift
if [[ "$CURR_ENV" == *"$substring_intel"* ]]; then
    module load impi
    module load intel
    mpiexec "$prog_name"  "$@"
    #-np "$num_nodes" --map-by ppr:"$num_tasks_per_node":node
elif [[ "$CURR_ENV" == *"$substring_GNU"* ]]; then
    module load foss/2023a
    srun "$prog_name" "$@"
else
    module load FJSVstclanga
    srun "$prog_name" "$@"
fi

ml purge

