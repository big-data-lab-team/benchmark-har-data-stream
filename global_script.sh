#!/bin/bash
#SBATCH --time=01:00:00
#SBATCH --job-name=verificarlo_bench
#SBATCH --account=def-glatard
#SBATCH --ntasks=3
#SBATCH --mail-type=ALL
#SBATCH --mail-user=vicuna.marc@gmail.com

# PREP
singularity build verificarlo-bench.img docker://vicuna.verificarloorpaille
# RUNNING

singularity exec verificarlo-bench.img ./run_1_verificarlo.sh 52
singularity exec verificarlo-bench.img ./run_1_verificarlo.sh 50
singularity exec verificarlo-bench.img ./run_verificarlo.sh 48


