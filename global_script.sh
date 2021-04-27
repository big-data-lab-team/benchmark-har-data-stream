#!/bin/bash
#SBATCH --time=10:00:00
#SBATCH --mem-per-cpu=10G
#SBATCH --job-name=veripaille_exponent
#SBATCH --account=rrg-glatard
#SBATCH --mail-type=ALL
#SBATCH --mail-user=vicuna.marc@gmail.com
echo THIS_IS_NODE_52
module load singularity
singularity exec --writable -B bench_bind/node_results:/opt/benchmark-har-data-stream/verificarlo_results --pwd=/opt/benchmark-har-data-stream veripaille_node ./run_1_verificarlo.sh $1 $2

