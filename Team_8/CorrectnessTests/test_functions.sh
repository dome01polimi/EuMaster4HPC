#!/usr/bin/bash

compute_absolute_difference(){
  awk 'BEGIN {printf "%9.7f", sqrt(('$2' - '$1')**2)}'
}

check_test_results_2stepopt(){
  accuracy=$1
  output_file=$2
  ref_file=$3
  num_succesful_checks=0

  Energy_ref=$(grep Energy ${ref_file} | tail -1 | awk '{print $4}')
  Energy_err_ref=$(grep Energy ${ref_file} | tail -1 | awk '{print $6}')
  Number_of_active_parameters_ref=$(grep "Number of signal active" ${ref_file} | tail -1 | awk '{print $7}')	
  Maximum_force_deviation_ref=$(grep "Maximum force deviation" ${ref_file} | tail -1 | awk '{print $5}')	
  Norm_change_ref=$(grep "Wavefunction norm change" ${ref_file} | tail -1 | awk '{print $5}')	

  Energy=$(grep Energy ${output_file} | tail -1 | awk '{print $4}')
  Energy_err=$(grep Energy ${output_file} | tail -1 | awk '{print $6}')
  Number_of_active_parameters=$(grep "Number of signal active" ${output_file} | tail -1 | awk '{print $7}')	
  Maximum_force_deviation=$(grep "Maximum force deviation" ${output_file} | tail -1 | awk '{print $5}')	
  Norm_change=$(grep "Wavefunction norm change" ${output_file} | tail -1 | awk '{print $5}')	

  Difference=$(compute_absolute_difference "${Energy}" "${Energy_ref}")
  result_test=$(awk 'BEGIN {if ( '${Difference}' <= '${accuracy}' ) {print "success" } else {print "failure" }}')
  if [ ${result_test} == 'success' ] ; then 
	  num_succesful_checks=$( echo $num_succesful_checks+1 | bc -l )
  fi

 
  Difference=$(compute_absolute_difference "${Energy_err}" "${Energy_err_ref}")
  result_test=$(awk 'BEGIN {if ( '${Difference}' <= '${accuracy}' ) {print "success" } else {print "failure" }}')
  if [ ${result_test} == 'success' ] ; then 
	  num_succesful_checks=$( echo $num_succesful_checks+1 | bc -l )
  fi

  Difference=$(compute_absolute_difference "${Number_of_active_parameters}" "${Number_of_active_parameters_ref}")
  result_test=$(awk 'BEGIN {if ( '${Difference}' <= '${accuracy}' ) {print "success" } else {print "failure" }}')
  if [ ${result_test} == 'success' ] ; then 
	  num_succesful_checks=$( echo $num_succesful_checks+1 | bc -l )
  fi

  Difference=$(compute_absolute_difference "${Maximum_force_deviation}" "${Maximum_force_deviation_ref}")
  result_test=$(awk 'BEGIN {if ( '${Difference}' <= '${accuracy}' ) {print "success" } else {print "failure" }}')
  if [ ${result_test} == 'success' ] ; then 
	  num_succesful_checks=$( echo $num_succesful_checks+1 | bc -l )
  fi

  Difference=$(compute_absolute_difference "${Norm_change}" "${Norm_change_ref}")
  result_test=$(awk 'BEGIN {if ( '${Difference}' <= '${accuracy}' ) {print "success" } else {print "failure" }}')

  if [ ${result_test} == 'success' ] ; then 
	  num_succesful_checks=$( echo $num_succesful_checks+1 | bc -l )
  fi

  if [ ${num_succesful_checks} == 5 ] ; then
    exit 0
  else
    exit 1
  fi
}


check_test_results_eval(){
  accuracy=$1
  output_file=$2
  ref_file=$3
  num_succesful_checks=0

  Energy_ref=$(grep Energy ${ref_file} | tail -1 | awk '{print $4}')
  Energy_err_corr_ref=$(grep Energy ${ref_file} | head -1 | awk '{print $6}')
  Energy_err_ref=$(grep Energy ${ref_file} | tail -1 | awk '{print $6}')
  Energy=$(grep Energy ${output_file} | tail -1 | awk '{print $4}')
  Energy_err=$(grep Energy ${output_file} | tail -1 | awk '{print $6}')
  Energy_err_corr=$(grep Energy ${output_file} | head -1 | awk '{print $6}')

  Difference=$(compute_absolute_difference "${Energy}" "${Energy_ref}")
  result_test=$(awk 'BEGIN {if ( '${Difference}' <= '${accuracy}' ) {print "success" } else {print "failure" }}')
  if [ ${result_test} == 'success' ] ; then 
	  num_succesful_checks=$( echo $num_succesful_checks+1 | bc -l )
  fi
  
  Difference=$(compute_absolute_difference "${Energy_err}" "${Energy_err_ref}")
  result_test=$(awk 'BEGIN {if ( '${Difference}' <= '${accuracy}' ) {print "success" } else {print "failure" }}')
  if [ ${result_test} == 'success' ] ; then 
	  num_succesful_checks=$( echo $num_succesful_checks+1 | bc -l )
  fi

  Difference=$(compute_absolute_difference "${Energy_err_corr}" "${Energy_err_corr_ref}")
  result_test=$(awk 'BEGIN {if ( '${Difference}' <= '${accuracy}' ) {print "success" } else {print "failure" }}')
  if [ ${result_test} == 'success' ] ; then 
	  num_succesful_checks=$( echo $num_succesful_checks+1 | bc -l )
  fi

  if [ ${num_succesful_checks} == 3 ] ; then
    exit 0
  else
    exit 1
  fi
}

# Check the passed argument and call the corresponding function
if [ "$1" == "check_test_results_2stepopt" ]; then
    check_test_results_2stepopt "$2" "$3" "$4"
elif [ "$1" == "check_test_results_eval" ]; then
    check_test_results_eval "$2" "$3" "$4"
else
    echo "Invalid function name"
    exit 5
fi