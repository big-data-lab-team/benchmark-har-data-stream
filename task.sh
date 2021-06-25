#!/bin/bash
#SBATCH --time=30:00:00
#SBATCH --mem-per-cpu=10G
#SBATCH --job-name=veripaille
#SBATCH --account=YOUR_ACCOUNT
echo This_is_Run_p${1}_e${2}
module load singularity
singularity exec --writable -B {{YOUR_BINDING_DIRECTORY}}:/opt/veripaille/verificarlo_results --pwd=/opt/veripaille {{YOUR SINGULARITY IMAGE}} ./run_1_verificarlo.sh $1 $2

