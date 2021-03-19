#!/bin/bash
#SBATCH --time=01:00:00
#SBATCH --job-name=verificarlo_bench$1
#SBATCH --account=rrg-glatard
#SBATCH --mail-type=ALL
#SBATCH --mail-user=vicuna.marc@gmail.com
#SBATCH global_script.sh 52
#singularity build verificarlo-bench.img docker://vicuna.verificarloorpaille
#RUNNING
singualrity exec -B bench_bind:/opt/benchmark-har-data-stream ./run_1_verificarlo.sh $1

