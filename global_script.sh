#!/bin/bash
#SBATCH --time=01:00:00
#SBATCH --job-name=verificarlo_bench
#SBATCH --account=def-glatard
#SBATCH --mail-type=ALL
#SBATCH --mail-user=vicuna.marc@gmail.com
#sbatch global_script.sh 52
# PREP
# singularity build verificarlo-bench.img docker://vicuna.verificarloorpaille
# RUNNING
./run_1_verificarlo.sh $1

