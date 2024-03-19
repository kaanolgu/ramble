#!/bin/bash -l
#PBS -N rmb_{application_name}_{partition_per_model}_{{partition_per_model}}
#PBS -o pbs-logs/
#PBS -e pbs-logs/
#PBS -l walltime=0:5:0
#PBS -l select=1:mpiprocs=1:ncpus={{partition_per_model}}:ngpus=1:mem=10g
#PBS -q {partition}q
#
# Variables surrounded by curly braces will be expanded
# when generating a specific execution script.
# Some example variables are:
#   - experiment_run_dir (Will be replaced with the experiment directory)
#   - command (Will be replaced with the command to run the experiment)
#   - log_dir (Will be replaced with the logs directory)
#   - experiment_name (Will be replaced with the name of the experiment)
#   - workload_run_dir (Will be replaced with the directory of the workload
#   - application_name (Will be repalced with the name of the application)
#   - n_nodes (Will be replaced with the required number of nodes)
#   Any experiment parameters will be available as variables as well.

cd "{experiment_run_dir}"


{command}