#!/usr/bin/bash

result_dir="results_xp1"
rm -rf $result_dir
mkdir $result_dir
rep_count=10

runny()
{
	local seed=$1
	local tree_count=$2
	local extend_type=$3
	local dataset=$4
	local memory=$5
	local binary="bin/$dataset/mondrian_coarse_empty_"$memory
	local f="mondrian_t$tree_count"_"$extend_type"_"$memory"
	$binary $dataset.log $seed 3 $seed lifetime:0.5 base_measure:0.0 discount_factor:1.0 tree_management:phoenix tree_count:$tree_count extend_type:$extend_type >> $result_dir/$dataset/$f.csv

}

#Run all out-of-memory strategy
for s in `seq $rep_count`; do
	for memory in '0.6M' '1M' '10M' '50M' '100M' '200M'; do
		for dataset in recofit_6 banos_6 RandomRBF_stable RandomRBF_drift covtype drift_6; do
			mkdir $result_dir/$dataset
			echo "memory $memory"
			for t in 1 5 10 20 30 50; do
				for et in none original count_only partial ghost; do
					runny $s $t $et $dataset $memory &
				done
			done
			wait
		done
	done
done

#Run with unbound
for dataset in recofit_6 banos_6 RandomRBF_stable RandomRBF_drift covtype drift_6; do
	binary="bin/$dataset/mondrian_coarse_empty_2G"
	mkdir $result_dir/$dataset
	for s in `seq $rep_count`; do
		for t in 1 5 10 20 30 50; do
			for et in original; do
				f="mondrian_undound_t$t"_"$et"
				echo "$binary $dataset.log $s 3 $s lifetime:0.5 base_measure:0.0 discount_factor:1.0 tree_management:phoenix tree_count:$t extend_type:$et"
				$binary $dataset.log $s 3 $s lifetime:0.5 base_measure:0.0 discount_factor:1.0 tree_management:phoenix tree_count:$t extend_type:$et >> $result_dir/$dataset/$f.csv
			done
		done
	done
done
