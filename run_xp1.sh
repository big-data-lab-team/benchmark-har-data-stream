#!/usr/bin/bash

result_dir="results_xp1"
rm -rf $result_dir
mkdir $result_dir
rep_count=10

#Run all out-of-memory strategy
for dataset in recofit_6 banos_6 RandomRBF_stable RandomRBF_drift covtype drift_6; do
	binary="bin/$dataset/mondrian_coarse_empty"
	mkdir $result_dir/$dataset
	for s in (seq $rep_count); do
		for t in 1 5 10 20 30 50; do
			for et in none original ghost count_only partial; do
				set f mondrian_t"$t"_"$et"
				echo "$binary $dataset.log $s 3 $s lifetime:0.5 base_measure:0.0 discount_factor:1.0 tree_management:phoenix tree_count:$t extend_type:$et"
				$binary $dataset.log $s 3 $s lifetime:0.5 base_measure:0.0 discount_factor:1.0 tree_management:phoenix tree_count:$t extend_type:$et >> $result_dir/$dataset/$f.csv
			done
		done
	done
done

#Run with unbound
for dataset in recofit_6 banos_6 RandomRBF_stable RandomRBF_drift covtype drift_6; do
	binary="bin/$dataset/mondrian_coarse_empty_unbound"
	mkdir $result_dir/$dataset
	for s in (seq $rep_count); do
		for t in 1 5 10 20 30 50; do
			for et in original; do
				f="mondrian_undound_t$t"_"$et"
				echo "$binary $dataset.log $s 3 $s lifetime:0.5 base_measure:0.0 discount_factor:1.0 tree_management:phoenix tree_count:$t extend_type:$et"
				$binary $dataset.log $s 3 $s lifetime:0.5 base_measure:0.0 discount_factor:1.0 tree_management:phoenix tree_count:$t extend_type:$et >> $result_dir/$dataset/$f.csv
			done
		done
	done
done
